"""Recalculate the delivered xlsx and reconcile it cell-by-cell against
study_numbers.json. Fails loudly on any unresolvable formula or mismatch.

Recalculation is done by the explicit evaluator in xlcalc.py over the formula set
this builder actually emits, independently of the library that wrote the file.
Anything the evaluator does not understand is reported as a failure rather than
skipped. (It began as a workaround for a LibreOffice install whose import filters
were missing; that is fixed, and the evaluator is kept because an independent
reimplementation is the stronger check.)

Three gates run here, in increasing strength:

  1. every formula in the workbook must evaluate;
  2. EVERY formula cell must reproduce the value the model itself computed for that
     cell — the builder records them in xlsx_expected.json as it writes. This is the
     gate that makes a formula-driven workbook safe: a formula that computes the right
     thing the wrong way, or points one row off, fails here rather than silently
     shipping a different number from the study;
  3. a hand-written set of headline reconciliations against study_numbers.json, kept
     as an independent cross-check on the expected map itself.
"""
import json, os
import openpyxl
import xlcalc

HERE = os.path.dirname(os.path.abspath(__file__))
XLSX = os.path.join(HERE, 'SWDY_Valuation_Model_05082026_public.xlsx')
wb = openpyxl.load_workbook(XLSX)
D = json.load(open(os.path.join(HERE, 'study_numbers.json')))
XP = json.load(open(os.path.join(HERE, 'xlsx_expected.json')))
EXPECT, ANCH = XP['expected'], XP['anchors']
DCF, LN, HI, HB, F = D['dcf'], D['lenses'], D['hist_is'], D['hist_bs'], D['fcst']
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

# every formula cell must be covered by the expected map — no unchecked formulas
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
    ('DCF enterprise value', g('DCF', 'C29'), DCF['ev'], 1.0),
    ('DCF present value of explicit years', g('DCF', 'C26'), DCF['pv_explicit'], 1.0),
    ('DCF present value of terminal value', g('DCF', 'C27'), DCF['pv_tv'], 1.0),
    ('DCF terminal value share', g('DCF', 'C28'), DCF['tv_share'], 0.002),
    ('DCF fair value per share', g('DCF', 'C31'), DCF['ps'], 0.02),
    ('DCF cost of capital — explicit window', g('DCF', 'C46'), D['wacc']['wacc_exp'], 0.0002),
    ('DCF cost of capital — terminal', g('DCF', 'C53'), D['wacc']['wacc_term'], 0.0002),
    ('DCF terminal return on invested capital', g('DCF', 'C21'), DCF['roic_term'], 0.001),
    ('Bridge equity attributable', g('SOTP Bridge', 'C12'), DCF['eq_attr'], 1.0),
    ('Bridge enterprise value', g('SOTP Bridge', 'C7'), DCF['ev'], 1.0),
    ('Bridge minority share of group profit', g('SOTP Bridge', 'C15'), DCF['nci_share'], 0.0005),
    ('Fundamental — DCF lens', g('Fundamental Valuation', 'C5'), DCF['ps'], 0.02),
    ('Fundamental — relative lens', g('Fundamental Valuation', 'C8'), LN['relative']['base'], 0.02),
    ('Fundamental — normalised lens', g('Fundamental Valuation', 'C9'), LN['normalized']['base'], 0.02),
    ('Fundamental — book lens', g('Fundamental Valuation', 'C10'), LN['book']['base'], 0.02),
    ('Fundamental — panel median', g('Fundamental Valuation', 'C26'), D['panel_centre'], 0.02),
    ('Fundamental — currency alternative', g('Fundamental Valuation', 'C18'), DCF['ccy_alt_ps'], 0.02),
    ('Summary weighted central', g('Summary', 'C9'), D['central'], 0.02),
    ('Summary terminal value share', g('Summary', 'C12'), DCF['tv_share'], 0.002),
    ('Summary panel median', g('Summary', 'C13'), D['panel_centre'], 0.02),
    ('Summary market capitalisation', g('Summary', ANCH['summary_mktcap']), D['meta']['mktcap'], 1.0),
    ('Relative lens implied value', g('Relative & Normalized', 'C11'), LN['relative']['base'], 0.02),
    ('Normalised lens implied value', g('Relative & Normalized', 'C28'), LN['normalized']['base'], 0.02),
    ('Book lens implied value', g('Relative & Normalized', 'C36'), LN['book']['base'], 0.02),
    ('Segments total FY2025 revenue', g('Segments', f'B{SEG_REV}'), HI['FY25']['rev'], 1.0),
    ('Segments group EBITDA FY2026E', g('Segments', f'B{SEG_EB}'), F['ebitda'][0], 1.0),
    ('Segments FY2025 share sums to 100%', g('Segments', f'C{SEG_REV}'), 1.0, 0.0005),
    ('Segments group EBITDA margin FY2026E', g('Segments', f'B{SEG_MG}'), F['ebitda_margin'][0], 0.0005),
    ('Income statement FY2025 EBITDA', g('Income Statement', 'D7'), HI['FY25']['ebitda'], 1.0),
    ('Income statement FY2030E attributable profit', g('Income Statement', 'I17'), F['np_attr'][4], 1.0),
    ('Income statement FY2024 EBITDA margin', g('Income Statement', 'C8'),
     HI['FY24']['ebitda'] / HI['FY24']['rev'], 0.001),
    ('Balance sheet FY2025 gross debt (audited)', g('Balance Sheet', 'D11'),
     HB['FY25']['debt'], 1.0),
    ('Balance sheet FY2030E net debt', g('Balance Sheet', 'I17'), F['net_debt'][4], 1.0),
    ('Balance sheet FY2024 net debt / EBITDA', g('Balance Sheet', 'C18'),
     HB['FY24']['nd'] / HI['FY24']['ebitda'], 0.01),
    ('Cash flow FY2026E free cash flow to the firm', g('Cash Flow', 'D13'), F['fcff'][0], 1.0),
    ('Summary financials FY2030E invested capital', g('Summary Financials', 'I13'), F['ic'][4], 1.0),
]
bad = 0
for name, got, want, tol in checks:
    ok = got is not None and abs(float(got) - float(want)) <= tol
    if not ok:
        bad += 1
    print(f"  [{'OK ' if ok else 'BAD'}] {name}: workbook={got:,.4f} model={float(want):,.4f}")

# The condensed balance sheet does not foot to zero by construction; the residual is the
# block of other liabilities, provisions and deferred tax. Check it against the audited
# FY2024 figures rather than asserting a cosmetic zero.
bc = [g('Balance Sheet', f'{c}19') for c in ('B', 'C')]   # FY2025 column is n/a
audited_other_fy24 = 13439.559 + 942.646 + 3669.893 + 2050.078 + 94.612 + 2631.482
print(f'condensed-balance residual FY2023/FY2024: {[round(float(v)) for v in bc]}')
print(f'  FY2024 residual {float(bc[1]):,.0f} vs audited other liabilities '
      f'{audited_other_fy24:,.0f} (gap {float(bc[1])-audited_other_fy24:+,.0f})')
assert abs(float(bc[1]) - audited_other_fy24) < 5.0, 'FY2024 condensed residual does not reconcile'
assert not errors, f'{len(errors)} unresolvable formulas'
assert not drift, f'{len(drift)} formula cells disagree with the model'
assert not uncovered, f'{len(uncovered)} formula cells are not checked against the model'
assert bad == 0, f'{bad} reconciliation mismatches'
print(f'RECALC OK — {nform} formulas, 0 unresolvable, {nchk} cell-level agreements with the '
      f'model, {len(checks)} headline reconciliations passed')
