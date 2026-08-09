"""Recalculate the delivered xlsx and reconcile it cell-by-cell against
study_numbers.json. Fails loudly on any unresolvable formula or mismatch.

Three gates, in increasing strength:
  1. every formula in the workbook must evaluate;
  2. EVERY formula cell must reproduce the value the model itself computed for
     that cell (xlsx_expected.json, written by the builder);
  3. a hand-written set of headline reconciliations against study_numbers.json,
     kept as an independent cross-check on the expected map itself.
"""
import json, os
import openpyxl
import xlcalc

HERE = os.path.dirname(os.path.abspath(__file__))
XLSX = os.path.join(HERE, 'DU_Valuation_Model_09082026_public.xlsx')
wb = openpyxl.load_workbook(XLSX)
D = json.load(open(os.path.join(HERE, 'study_numbers.json')))
XP = json.load(open(os.path.join(HERE, 'xlsx_expected.json')))
EXPECT, ANCH = XP['expected'], XP['anchors']
DCF, LN, HI, HB, F, W = D['dcf'], D['lenses'], D['hist_is'], D['hist_bs'], D['fcst'], D['wacc']
SH = D['meta']['shares_mn']

BK = xlcalc.Book(wb)
cell_value = BK.cell_value

# ---- gate 1: every formula must evaluate -------------------------------------
nform, errors = 0, []
for sh, coord in BK.formula_cells():
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

uncovered = [f'{sh}!{coord}' for sh, coord in BK.formula_cells()
             if coord not in EXPECT.get(sh, {})]
print(f'formula cells with no expected value recorded: {len(uncovered)}')
for u in uncovered[:20]:
    print('  ', u)

# ---- gate 3: headline reconciliations against study_numbers.json --------------
def g(sheet, cell):
    return cell_value(sheet, cell)

SEG_REV, SEG_EB, SEG_MG = ANCH['seg_rev_tot'], ANCH['seg_ebitda_tot'], ANCH['seg_ebitda_mgn']
checks = [
    ('DCF enterprise value', g('DCF', 'C30'), DCF['ev'], 1.0),
    ('DCF present value of explicit years', g('DCF', 'C27'), DCF['pv_explicit'], 1.0),
    ('DCF present value of terminal value', g('DCF', 'C28'), DCF['pv_tv'], 1.0),
    ('DCF terminal value share', g('DCF', 'C29'), DCF['tv_share'], 0.002),
    ('DCF fair value per share at 31-Dec-2025', g('DCF', 'C32'), DCF['ps_dec'], 0.02),
    ('DCF anchor accretion factor', g('DCF', 'C62'), DCF['roll'], 0.0005),
    ('DCF fair value per share at the anchor', g('DCF', 'C63'), DCF['ps'], 0.02),
    ('DCF cost of capital — explicit window', g('DCF', 'C47'), W['wacc_exp'], 0.0002),
    ('DCF cost of capital — terminal', g('DCF', 'C54'), W['wacc_term'], 0.0002),
    ('DCF terminal return on invested capital', g('DCF', 'C22'), DCF['roic_term'], 0.001),
    ('Bridge equity value', g('SOTP Bridge', 'C11'), DCF['eq_val'], 1.0),
    ('Bridge enterprise value', g('SOTP Bridge', 'C7'), DCF['ev'], 1.0),
    ('Fundamental — DCF lens', g('Fundamental Valuation', 'C5'), DCF['ps'], 0.02),
    ('Fundamental — relative lens', g('Fundamental Valuation', 'C8'), LN['relative']['base'], 0.02),
    ('Fundamental — normalised lens', g('Fundamental Valuation', 'C9'),
     LN['normalized']['base'], 0.02),
    ('Fundamental — book lens', g('Fundamental Valuation', 'C10'), LN['book']['base'], 0.02),
    ('Fundamental — panel median', g('Fundamental Valuation', 'C27'), D['panel_centre'], 0.02),
    ('Fundamental — Framing A vs B gap', g('Fundamental Valuation', 'C20'),
     DCF['ps'] - DCF['ps_framing_b'], 0.02),
    ('Summary weighted central', g('Summary', 'C9'), D['central'], 0.02),
    ('Summary terminal value share', g('Summary', 'C12'), DCF['tv_share'], 0.002),
    ('Summary Framing B alternative', g('Summary', 'C11'), DCF['ps_framing_b'], 0.02),
    ('Summary market capitalisation', g('Summary', ANCH['summary_mktcap']),
     D['meta']['mktcap'], 1.0),
    ('Relative lens implied value', g('Relative & Normalized', 'C11'),
     LN['relative']['base'], 0.02),
    ('Normalised lens implied value', g('Relative & Normalized', 'C27'),
     LN['normalized']['base'], 0.02),
    ('Book lens implied value', g('Relative & Normalized', 'C35'), LN['book']['base'], 0.02),
    ('Segments total FY2025 revenue', g('Segments', f'B{SEG_REV}'), HI['FY25']['rev'], 1.0),
    ('Segments group EBITDA FY2026E', g('Segments', f'B{SEG_EB}'), F['ebitda'][0], 1.0),
    ('Segments FY2025 share sums to 100%', g('Segments', f'C{SEG_REV}'), 1.0, 0.0005),
    ('Segments group EBITDA margin FY2026E', g('Segments', f'B{SEG_MG}'),
     F['ebitda_margin'][0], 0.0005),
    ('Income statement FY2025 EBITDA', g('Income Statement', 'D9'), HI['FY25']['ebitda'], 1.0),
    ('Income statement FY2030E net profit', g('Income Statement', 'I18'), F['np'][4], 1.0),
    ('Income statement FY2024 EBITDA margin', g('Income Statement', 'C10'),
     HI['FY24']['ebitda'] / HI['FY24']['rev'], 0.001),
    ('Balance sheet FY2030E cash and deposits', g('Balance Sheet', 'I12'),
     F['net_cash'][4], 1.0),
    ('Balance sheet FY2025 net cash after leases', g('Balance Sheet', 'D15'),
     HB['FY25']['net_cash'] - HB['FY25']['lease'], 1.0),
    ('Cash flow FY2026E free cash flow to the firm', g('Cash Flow', 'D14'), F['fcff'][0], 1.0),
    ('Summary financials FY2030E invested capital', g('Summary Financials', 'I13'),
     F['ic'][4], 1.0),
]
bad = 0
for name, got, want, tol in checks:
    ok = got is not None and abs(float(got) - float(want)) <= tol
    if not ok:
        bad += 1
    print(f"  [{'OK ' if ok else 'BAD'}] {name}: workbook={got:,.4f} model={float(want):,.4f}")

assert not errors, f'{len(errors)} unresolvable formulas'
assert not drift, f'{len(drift)} formula cells disagree with the model'
assert not uncovered, f'{len(uncovered)} formula cells are not checked against the model'
assert bad == 0, f'{bad} reconciliation mismatches'
print(f'RECALC OK — {nform} formulas, 0 unresolvable, {nchk} cell-level agreements with the '
      f'model, {len(checks)} headline reconciliations passed')
