"""Recalculate the delivered xlsx and reconcile it cell-by-cell against
study_numbers.json. Fails loudly on any unresolvable formula or mismatch.

Three gates, in increasing strength:
  1. every formula in the workbook must evaluate (anything unparseable = FAILURE);
  2. EVERY formula cell must reproduce the value the model itself computed for that
     cell (recorded in xlsx_expected.json by the builder as it wrote);
  3. a hand-written set of headline reconciliations against study_numbers.json, an
     independent cross-check on the expected map itself."""
import json, os
import openpyxl
import xlcalc

HERE = os.path.dirname(os.path.abspath(__file__))
XLSX = os.path.join(HERE, 'MODON_Valuation_Model_09082026_public.xlsx')
wb = openpyxl.load_workbook(XLSX)
D = json.load(open(os.path.join(HERE, 'study_numbers.json')))
XP = json.load(open(os.path.join(HERE, 'xlsx_expected.json')))
EXPECT, ANCH = XP['expected'], XP['anchors']
DCF, LN, HI, HB, F = D['dcf'], D['lenses'], D['hist_is'], D['hist_bs'], D['fcst']
W, REL, NRM, BK = D['wacc'], D['rel'], D['norm'], D['book']
SH = D['meta']['shares_mn']
AD = ANCH['dcf']

BK_ = xlcalc.Book(wb)
cell_value = BK_.cell_value

# ---- gate 1: every formula must evaluate -------------------------------------
nform, errors = 0, []
for sh, coord in BK_.formula_cells():
    nform += 1
    try:
        cell_value(sh, coord)
    except Exception as ex:
        errors.append(f'{sh}!{coord}: {ex}')
print(f'formulas: {nform}, unresolvable: {len(errors)}')
for e in errors[:20]:
    print('  ', e)

# ---- gate 2: every formula cell must reproduce the model's own value ----------
def tol_for(v):
    return max(2e-4, abs(v) * 5e-6)

nchk, drift = 0, []
for sh, cells in EXPECT.items():
    for coord, want in cells.items():
        nchk += 1
        got = cell_value(sh, coord)
        if not isinstance(got, (int, float)) or abs(float(got) - want) > tol_for(want):
            drift.append((sh, coord, got, want))
print(f'formula cells checked against the model: {nchk}, disagreements: {len(drift)}')
for sh, coord, got, want in drift[:25]:
    g = f'{got:,.6f}' if isinstance(got, (int, float)) else repr(got)
    print(f'   {sh}!{coord}: workbook={g} model={want:,.6f}')

# every formula cell must be covered by the expected map — no unchecked formulas
uncovered = [f'{sh}!{coord}' for sh, coord in BK_.formula_cells()
             if coord not in EXPECT.get(sh, {})]
print(f'formula cells with no expected value recorded: {len(uncovered)}')
for u in uncovered[:20]:
    print('  ', u)

# ---- gate 3: headline reconciliations against study_numbers.json --------------
def g(sheet, cell):
    return cell_value(sheet, cell)

rw = ANCH['dcf_rw']
checks = [
    ('DCF enterprise value', g('DCF', f"C{AD['ev']}"), DCF['ev'], 1.0),
    ('DCF present value of explicit years', g('DCF', f"C{AD['pex']}"), DCF['pv_explicit'], 1.0),
    ('DCF present value of terminal value', g('DCF', f"C{AD['ptv']}"), DCF['pv_tv'], 1.0),
    ('DCF terminal value share', g('DCF', f"C{AD['tvs']}"), DCF['tv_share'], 0.002),
    ('DCF fair value per share at 31-Dec-2025', g('DCF', f"C{AD['psd']}"), DCF['ps_dec'], 0.02),
    ('DCF anchor accretion factor', g('DCF', f"C{AD['roll']}"), DCF['roll'], 0.0005),
    ('DCF fair value per share at the anchor', g('DCF', f"C{AD['ps']}"), DCF['ps'], 0.02),
    ('DCF cost of capital — explicit window', g('DCF', f"C{AD['wacc']}"), W['wacc_exp'], 0.0002),
    ('DCF cost of capital — terminal', g('DCF', f"C{AD['wt']}"), W['wacc_term'], 0.0002),
    ('DCF cost of equity', g('DCF', f"C{AD['ke']}"), W['ke_exp'], 0.0002),
    ('DCF reinvestment rate = g/ROIC', g('DCF', f"C{AD['rr']}"), DCF['rr_term'], 0.001),
    ('DCF terminal value', g('DCF', f"C{AD['tv']}"), DCF['tv'], 1.0),
    ('Bridge equity attributable', g('SOTP Bridge', 'C17'), DCF['eq_attr'], 1.0),
    ('Bridge enterprise value', g('SOTP Bridge', 'C9'), DCF['ev'], 1.0),
    ('Fundamental — DCF lens', g('Fundamental Valuation', 'C5'), DCF['ps'], 0.02),
    ('Fundamental — relative lens', g('Fundamental Valuation', 'C9'), LN['relative']['base'], 0.02),
    ('Fundamental — normalised lens', g('Fundamental Valuation', 'C10'), LN['normalized']['base'], 0.02),
    ('Fundamental — book lens', g('Fundamental Valuation', 'C11'), LN['book']['base'], 0.02),
    ('Summary weighted central', g('Summary', 'C9'), D['central'], 0.02),
    ('Summary terminal value share', g('Summary', 'C12'), DCF['tv_share'], 0.002),
    ('Summary market capitalisation', g('Summary', ANCH['summary_mktcap']),
     D['meta']['mktcap'], 1.0),
    ('Relative lens implied value', g('Relative & Normalized', 'C11'), LN['relative']['base'], 0.02),
    ('Normalised lens implied value', g('Relative & Normalized', 'C28'), LN['normalized']['base'], 0.02),
    ('Book lens implied value', g('Relative & Normalized', 'C36'), LN['book']['base'], 0.02),
    ('Segments group FY2025 revenue', g('Segments', f"B{ANCH['seg_rev_tot']}"),
     HI['FY25']['rev'], 1.0),
    ('Segments FY2026E group revenue', g('Segments', f"B{ANCH['seg_fcst_rev'] + 5}"),
     F['rev'][0], 1.0),
    ('Segments FY2030E closing backlog', g('Segments', f"F{ANCH['bl_row'] + 3}"),
     F['bl_close'][4], 1.0),
    ('Income statement FY2025 EBITDA', g('Income Statement', 'D7'), HI['FY25']['ebitda'], 1.0),
    ('Income statement FY2030E attributable profit', g('Income Statement', 'I17'),
     F['np_attr'][4], 1.0),
    ('Income statement FY2024 EBITDA margin', g('Income Statement', 'C8'),
     HI['FY24']['ebitda'] / HI['FY24']['rev'], 0.001),
    ('Balance sheet FY2025 gross debt (audited)', g('Balance Sheet', 'D11'),
     HB['FY25']['debt'], 1.0),
    ('Balance sheet FY2030E net debt', g('Balance Sheet', 'I15'), F['net_debt'][4], 1.5),
    ('Balance sheet FY2030E cash', g('Balance Sheet', 'I9'), F['cash'][4], 1.5),
    ('Cash flow FY2026E free cash flow to the firm', g('Cash Flow', 'D14'), F['fcff'][0], 1.0),
    ('Summary financials FY2030E invested capital', g('Summary Financials', 'I13'),
     F['ic'][4], 1.0),
    ('Peer sheet trailing P/E (MODON row)', g('Peer & Sector', 'E8'),
     D['meta']['mktcap'] / D['inputs']['pat_fy25']['value'], 0.02),
]
bad = 0
for name, got, want, tol in checks:
    ok = got is not None and abs(float(got) - float(want)) <= tol
    if not ok:
        bad += 1
    print(f"  [{'OK ' if ok else 'BAD'}] {name}: workbook={float(got):,.4f} model={float(want):,.4f}")

assert not errors, f'{len(errors)} unresolvable formulas'
assert not drift, f'{len(drift)} formula cells disagree with the model'
assert not uncovered, f'{len(uncovered)} formula cells are not checked against the model'
assert bad == 0, f'{bad} reconciliation mismatches'
print(f'RECALC OK — {nform} formulas, 0 unresolvable, {nchk} cell-level agreements with the '
      f'model, {len(checks)} headline reconciliations passed')
