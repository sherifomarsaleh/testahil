"""Recalculate the DELIVERED workbook and reconcile it cell-by-cell against the model.

Three gates, in increasing strength:

  1. every formula in the workbook must evaluate — anything the evaluator cannot parse is a
     FAILURE, never a skip;
  2. EVERY formula cell must reproduce the value the model itself computed for it. The builder
     records those as it writes, in xlsx_expected.json. This is what makes a formula-driven
     workbook safe: a formula that computes the right thing the wrong way, or points one row
     off, fails here rather than silently shipping a different number from the study;
  3. a hand-written set of headline reconciliations against study_numbers.json, kept as an
     independent cross-check on the expected map itself.

Recalculation runs through the explicit evaluator in xlcalc.py rather than through the library
that wrote the file: an independent reimplementation that has to agree cell-for-cell is the
stronger check.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import openpyxl
import xlcalc

XLSX = os.path.join(HERE, 'AMOC_Valuation_Model_06082026_public.xlsx')
wb = openpyxl.load_workbook(XLSX)
D = json.load(open(os.path.join(HERE, 'study_numbers.json')))
XP = json.load(open(os.path.join(HERE, 'xlsx_expected.json')))
EXPECT = XP['expected']
DCF, LN, F, BASE, W = D['dcf'], D['lenses'], D['fcst'], D['base'], D['wacc']
REL, NRM, BK, U = D['rel'], D['norm'], D['book'], D['unit']
SH = D['meta']['shares_mn']

BK_ = xlcalc.Book(wb)
g = BK_.cell_value

# ---- gate 1 -----------------------------------------------------------------
nform, errors = 0, []
for sh, coord in BK_.formula_cells():
    nform += 1
    try:
        g(sh, coord)
    except Exception as ex:
        errors.append(f'{sh}!{coord}: {ex}')
print(f'formulas: {nform}, unresolvable: {len(errors)}')
for e in errors[:20]:
    print('  ', e)


# ---- gate 2 -----------------------------------------------------------------
def tol_for(v):
    return max(2e-4, abs(v) * 5e-6)


nchk, drift = 0, []
for sh, cells in EXPECT.items():
    for coord, want in cells.items():
        nchk += 1
        got = g(sh, coord)
        if not isinstance(got, (int, float)) or abs(float(got) - want) > tol_for(want):
            drift.append((sh, coord, got, want))
print(f'formula cells checked against the model: {nchk}, disagreements: {len(drift)}')
for sh, coord, got, want in drift[:30]:
    gs = f'{got:,.6f}' if isinstance(got, (int, float)) else repr(got)
    print(f'   {sh}!{coord}: workbook={gs} model={want:,.6f}')

uncovered = [f'{sh}!{coord}' for sh, coord in BK_.formula_cells()
             if coord not in EXPECT.get(sh, {})]
print(f'formula cells with no expected value recorded: {len(uncovered)}')
for u in uncovered[:20]:
    print('  ', u)

# ---- gate 3 -----------------------------------------------------------------
# Addresses come from the builder's own anchor map, never hand-guessed: a cross-check that
# points at the wrong cell is the same defect class gate 2 exists to catch.
AN = XP['anchors']
LG_, DC, BR, IS_, BS_, CF_, RN, FV, SU = (AN['legs'], AN['dcf'], AN['bridge'], AN['is'],
                                          AN['bs'], AN['cf'], AN['rn'], AN['fv'], AN['sum'])
CD_, UC_, HCC, FCC = AN['cols']['cd'], AN['cols']['uc'], AN['cols']['hist'], AN['cols']['fcst']
checks = [
    ('Enterprise value', g('DCF', f"B{DC['ev']}"), DCF['ev'], 1.0),
    ('Terminal value as a share of enterprise value', g('DCF', f"B{DC['tv_share']}"),
     DCF['tv_share'], 0.002),
    ('Cost of capital — explicit window', g('DCF', f"B{DC['wacc_exp']}"), W['wacc_exp'], 0.0002),
    ('Cost of capital — terminal', g('DCF', f"B{DC['wacc_term']}"), W['wacc_term'], 0.0002),
    ('Cost of equity — explicit window', g('DCF', f"B{DC['ke']}"), W['ke_exp'], 0.0002),
    ('2026E free cash flow to the firm (DCF sheet)', g('DCF', f"B{DC['fcff']}"), F['fcff'][0], 1.0),
    ('2030E present value of free cash flow', g('DCF', f"F{DC['pv']}"), F['pv'][4], 1.0),
    ('2030E EBITDA', g('DCF', f"F{DC['ebitda']}"), F['ebitda'][4], 1.0),
    ('Bridge — equity attributable', g('EV Bridge', f"B{BR['eq']}"), DCF['eq_attr'], 1.0),
    ('Bridge — fair value per share', g('EV Bridge', f"B{BR['ps']}"), DCF['ps'], 0.02),
    ('Bridge — terminal value share', g('EV Bridge', f"B{BR['tv_share']}"), DCF['tv_share'], 0.002),
    ('Summary — weighted central fair value', g('Summary', f"C{SU['central']}"), D['central'], 0.02),
    ('Summary — terminal value share beside the DCF lens', g('Summary', 'G6'),
     DCF['tv_share'], 0.002),
    ('Fundamental — DCF lens', g('Fundamental Valuation', f"C{FV['rows']['dcf']}"),
     LN['dcf']['base'], 0.02),
    ('Fundamental — relative lens', g('Fundamental Valuation', f"C{FV['rows']['relative']}"),
     LN['relative']['base'], 0.02),
    ('Fundamental — normalised lens', g('Fundamental Valuation', f"C{FV['rows']['normalized']}"),
     LN['normalized']['base'], 0.02),
    ('Fundamental — book lens', g('Fundamental Valuation', f"C{FV['rows']['book']}"),
     LN['book']['base'], 0.02),
    ('Fundamental — weighted central', g('Fundamental Valuation', f"C{FV['central']}"),
     D['central'], 0.02),
    ('Product legs — calendar 2025 revenue', g('Product Legs', f"B{LG_['rev_cy25']}"),
     BASE['rev_cy25'], 1.0),
    ('Product legs — calendar 2025 profit after tax', g('Product Legs', f"B{LG_['pat_cy25']}"),
     BASE['pat_cy25'], 1.0),
    ('Product legs — 2030E total revenue', g('Product Legs', f"{UC_[4]}{LG_['rev']}"),
     F['rev'][4], 1.0),
    ('Income statement — 2030E attributable profit', g('Income Statement', f"{FCC[4]}{IS_['npa']}"),
     F['np_attr'][4], 1.0),
    ('Income statement — calendar 2025 EBITDA', g('Income Statement', f"{HCC[3]}{IS_['ebitda']}"),
     D['hist_is']['CY25']['ebitda'], 1.0),
    ('Income statement — 2030E earnings per share', g('Income Statement', f"{FCC[4]}{IS_['eps']}"),
     F['np_attr'][4] / SH, 0.01),
    ('Balance sheet — 2030E net debt', g('Balance Sheet', f"{FCC[4]}{BS_['nd']}"),
     F['net_debt'][4], 1.0),
    ('Balance sheet — calendar 2025 net working capital',
     g('Balance Sheet', f"{HCC[3]}{BS_['nwc']}"), BASE['nwc_cy25'], 1.0),
    ('Cash flow — 2026E free cash flow to the firm', g('Cash Flow', f"B{CF_['fcff']}"),
     F['fcff'][0], 1.0),
    ('Cash flow — 2030E closing attributable equity', g('Cash Flow', f"F{CF_['ceq']}"),
     F['equity'][4], 1.0),
    ('Relative lens implied value', g('Relative & Normalized', f"B{RN['rel']}"),
     LN['relative']['base'], 0.02),
    ('Normalised lens implied value', g('Relative & Normalized', f"B{RN['norm']}"),
     LN['normalized']['base'], 0.02),
    ('Book lens implied value', g('Relative & Normalized', f"B{RN['book']}"),
     LN['book']['base'], 0.02),
]
bad = 0
for name, got, want, tol in checks:
    ok = got is not None and abs(float(got) - float(want)) <= tol
    if not ok:
        bad += 1
    print(f"  [{'OK ' if ok else 'BAD'}] {name}: workbook={float(got):,.4f} "
          f"model={float(want):,.4f}")

# The condensed balance sheet is a reconstruction and its two sides are built from
# different drivers, so it is checked rather than assumed to foot.
for i, lab in enumerate(('FY2022/23', 'FY2023/24', 'FY2024/25', 'CY2025')):
    diff = g('Balance Sheet', f"{HCC[i]}{BS_['chk']}")
    print(f'balance check {lab}: {float(diff):,.2f}')
    assert abs(float(diff)) < 1.0, f'balance sheet does not foot in {lab}'

assert not errors, f'{len(errors)} unresolvable formulas'
assert not drift, f'{len(drift)} formula cells disagree with the model'
assert not uncovered, f'{len(uncovered)} formula cells are not checked against the model'
assert bad == 0, f'{bad} reconciliation mismatches'
print(f'\nRECALC OK — {nform} of {nform} formula cells reproduce the model, 0 unresolvable, '
      f'0 unchecked; {len(checks)} headline reconciliations passed')
