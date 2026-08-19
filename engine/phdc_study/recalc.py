"""Recalculate the delivered workbook and reconcile it against study_numbers.json.

Three gates, in increasing strength:
  1. every formula in the workbook must evaluate — anything unparseable is a FAILURE,
     never a skip;
  2. every formula cell must reproduce the value the model itself computed for that cell
     (xlsx_expected.json, written by the builder), and every formula cell must be covered;
  3. a hand-written set of headline reconciliations straight off study_numbers.json, as an
     independent check on the expected map itself.

The evaluator is a reimplementation, not the application that wrote the file: asking a
spreadsheet engine to confirm its own arithmetic proves nothing.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'du_study'))
os.chdir(HERE)
import openpyxl
import xlcalc

XLSX = 'PHDC_Valuation_Model_19082026_public.xlsx'
wb = openpyxl.load_workbook(XLSX)
D = json.load(open('study_numbers.json'))
XP = json.load(open('xlsx_expected.json'))
EXPECT, ANCH = XP['expected'], XP['anchors']
H, W, L, SYN, DCF = D['hist'], D['wacc'], D['lenses'], D['synthesis'], D['dcf']
A, B, M, INP = DCF['framing_A'], DCF['framing_B'], D['meta'], D['inputs']

BK = xlcalc.Book(wb)
cell_value = BK.cell_value

# ---- gate 1 -----------------------------------------------------------------
nform, errors = 0, []
for sh, coord in BK.formula_cells():
    nform += 1
    try:
        cell_value(sh, coord)
    except Exception as ex:
        errors.append('%s!%s: %s' % (sh, coord, ex))
print('formulas: %d, unresolvable: %d' % (nform, len(errors)))
for e in errors[:20]:
    print('  ', e)

# ---- gate 2 -----------------------------------------------------------------
def tol_for(v):
    return max(2e-4, abs(v) * 5e-6)

nchk, drift = 0, []
for sh, cells in EXPECT.items():
    for coord, want in cells.items():
        nchk += 1
        got = cell_value(sh, coord)
        if not isinstance(got, (int, float)) or abs(float(got) - want) > tol_for(want):
            drift.append((sh, coord, got, want))
print('formula cells checked against the model: %d, disagreements: %d' % (nchk, len(drift)))
for sh, coord, got, want in drift[:30]:
    g = ('%.6f' % got) if isinstance(got, (int, float)) else repr(got)
    print('   %s!%s: workbook=%s model=%.6f' % (sh, coord, g, want))

uncovered = ['%s!%s' % (sh, coord) for sh, coord in BK.formula_cells()
             if coord not in EXPECT.get(sh, {})]
print('formula cells with no expected value recorded: %d' % len(uncovered))
for u in uncovered[:40]:
    print('  ', u)

# ---- gate 3: headline reconciliations straight off the model ------------------
def find(sheet, label, col='B'):
    ws = wb[sheet]
    for row in ws.iter_rows(min_col=1, max_col=1):
        c = row[0]
        if isinstance(c.value, str) and c.value.strip().lower() == label.strip().lower():
            return cell_value(sheet, '%s%d' % (col, c.row))
    raise KeyError('%s!%s not found' % (sheet, label))

recon, fails = [], []
def check(name, got, want, tol=None):
    t = tol if tol is not None else tol_for(want)
    ok = isinstance(got, (int, float)) and abs(float(got) - want) <= t
    recon.append((name, got, want, ok))
    if not ok:
        fails.append(name)

check('value per share, framing A', find('Fundamental Valuation', 'VALUE PER SHARE, EGP', 'B'),
      A['bridge']['vps'])
check('value per share, framing B', find('Fundamental Valuation', 'VALUE PER SHARE, EGP', 'C'),
      B['bridge']['vps'])
check('enterprise value, framing A', find('Fundamental Valuation', 'ENTERPRISE VALUE', 'B'), A['ev'])
check('enterprise value, framing B', find('Fundamental Valuation', 'ENTERPRISE VALUE', 'C'), B['ev'])
check('equity value, framing A', find('Fundamental Valuation', 'EQUITY VALUE', 'B'),
      A['bridge']['equity'])
check('DCF present value of the explicit forecast',
      find('DCF', 'Present value', 'H'), A['pv_explicit'])
check('DCF enterprise value', find('DCF', 'ENTERPRISE VALUE, EGP mn', 'H'), A['ev'])
check('balance sheet identity, June', find('Balance Sheet',
      'CHECK: total liabilities plus equity less total assets', 'B'), 0.0, tol=1e-3)
check('balance sheet identity, December', find('Balance Sheet',
      'CHECK: total liabilities plus equity less total assets', 'C'), 0.0, tol=1e-3)
check('segment revenue foots to the income statement', find('Segments', 'TOTAL', 'B'),
      INP['rev_h126']['value'])
check('segment cost foots to the income statement', find('Segments', 'TOTAL', 'D'),
      INP['cogs_h126']['value'])
check('operating cash flow without the float, H1-2026', find('Cash Flow', 'H1-2026', 'D'),
      H['ocf_ex_ra_h126'])
check('operating cash flow without the float, FY2024', find('Cash Flow', 'FY2024', 'D'),
      H['ocf_ex_ra_fy24'])
check('summary base against market', find('Summary', 'Base against market', 'B'),
      SYN['framing_A']['base'] / M['spot'] - 1)

print('\nheadline reconciliations: %d, failures: %d' % (len(recon), len(fails)))
for nm, got, want, ok in recon:
    g = ('%.6f' % got) if isinstance(got, (int, float)) else repr(got)
    print('  %-52s %-16s vs %-16.6f %s' % (nm, g, want, 'OK' if ok else 'FAIL'))

bad = bool(errors) or bool(drift) or bool(uncovered) or bool(fails)
print('\nRECALC %s' % ('FAILED' if bad else 'CLEAN'))
sys.exit(1 if bad else 0)
