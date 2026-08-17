"""Recalculate the delivered xlsx and reconcile it cell-by-cell against
study_numbers.json. Fails loudly on any unresolvable formula or mismatch.

Three gates, in increasing strength: (1) every formula must evaluate; (2) EVERY
formula cell must reproduce the value the model itself computed for that cell
(xlsx_expected.json, written by the builder); (3) a hand-written set of headline
reconciliations against study_numbers.json, an independent cross-check on the
expected map itself. Anything the evaluator cannot parse is a FAILURE, never a
skip.
"""
import json, os
import openpyxl
import xlcalc

HERE = os.path.dirname(os.path.abspath(__file__))
XLSX = os.path.join(HERE, 'AIRARABIA_Valuation_Model_09082026_public.xlsx')
wb = openpyxl.load_workbook(XLSX)
D = json.load(open(os.path.join(HERE, 'study_numbers.json')))
XP = json.load(open(os.path.join(HERE, 'xlsx_expected.json')))
EXPECT = XP['expected']
DCF, LN, HI, HB, F = D['dcf'], D['lenses'], D['hist_is'], D['hist_bs'], D['fcst']
W = D['wacc']
SH = D['meta']['shares_mn']

BK = xlcalc.Book(wb)
cell_value = BK.cell_value

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

def g(sheet, cell):
    return cell_value(sheet, cell)

checks = [
    ('DCF enterprise value', g('DCF', 'C56'), DCF['ev'], 1.0),
    ('DCF PV of explicit years', g('DCF', 'C55'), DCF['pv_explicit'], 1.0),
    ('DCF PV of terminal value', g('DCF', 'C54'), DCF['pv_tv'], 1.0),
    ('DCF terminal value share', g('DCF', 'C57'), DCF['tv_share'], 0.002),
    ('DCF fair value at 31-Dec-2025', g('DCF', 'C60'), DCF['ps_dec'], 0.02),
    ('DCF anchor accretion factor', g('DCF', 'C61'), DCF['roll'], 0.0005),
    ('DCF fair value at the anchor (split roll)', g('DCF', 'C64'), DCF['ps'], 0.02),
    ('DCF beta at the neutral benchmark switch', g('DCF', 'C8'), W['beta']['beta'], 0.0005),
    ('DCF cost of equity — explicit', g('DCF', 'C10'), W['ke_exp'], 0.0002),
    ('DCF cost of capital — explicit', g('DCF', 'C17'), W['wacc_exp'], 0.0002),
    ('DCF cost of capital — terminal', g('DCF', 'C24'), W['wacc_term'], 0.0002),
    ('DCF terminal return on capital', g('DCF', 'C51'), DCF['roic_term'], 0.001),
    ('Bridge equity attributable', g('SOTP Bridge', 'C13'), DCF['eq_attr'], 1.0),
    ('Bridge net cash', g('SOTP Bridge', 'C6'), -HB['FY25']['nd'], 0.5),
    ('Bridge split-roll per share', g('SOTP Bridge', 'C15'), DCF['ps'], 0.02),
    ('Bridge JV-capitalised per share', g('SOTP Bridge', 'C20'), DCF['ps_jvcap'], 0.02),
    ('Fundamental — DCF lens', g('Fundamental Valuation', 'C5'), DCF['ps'], 0.02),
    ('Fundamental — relative lens', g('Fundamental Valuation', 'C6'), LN['relative']['base'], 0.02),
    ('Fundamental — normalised lens', g('Fundamental Valuation', 'C7'), LN['normalized']['base'], 0.02),
    ('Fundamental — book lens', g('Fundamental Valuation', 'C8'), LN['book']['base'], 0.02),
    ('Fundamental — panel median', g('Fundamental Valuation', 'C23'), D['panel_centre'], 0.02),
    ('Summary weighted central', g('Summary', 'C9'), D['central'], 0.02),
    ('Summary central on the JV-capitalised framing', g('Summary', 'C11'), D['central_jvcap'], 0.02),
    ('Summary terminal value share', g('Summary', 'C12'), DCF['tv_share'], 0.002),
    ('Segments FY2026E revenue', g('Segments', 'B14'), F['rev'][0], 1.0),
    ('Segments FY2030E revenue', g('Segments', 'F14'), F['rev'][4], 1.0),
    ('Segments FY2026E EBITDA', g('Segments', 'B27'), F['ebitda'][0], 1.0),
    ('Segments FY2026E EBITDA margin', g('Segments', 'B30'), F['ebitda_margin'][0], 0.0005),
    ('Income statement FY2025 EBITDA', g('Income Statement', 'D9'), HI['FY25']['ebitda'], 1.0),
    ('Income statement FY2025 operating profit', g('Income Statement', 'D11'), HI['FY25']['ebit'], 1.0),
    ('Income statement FY2025 profit before tax', g('Income Statement', 'D16'), HI['FY25']['ebt'], 1.0),
    ('Cash flow FY2030E closing gross debt', g('Cash Flow', 'F18'), F['debt'][4], 1.0),
    ('Relative lens fee-stream value', g('Relative & Normalized', 'C7'), D['rel']['fee_value'], 1.0),
    ('Summary weighted bear', g('Summary', 'B9'), D['lenses']['central']['bear'], 0.02),
    ('Summary weighted bull', g('Summary', 'D9'), D['lenses']['central']['bull'], 0.02),
    ('Expert 1 live leg', g('Fundamental Valuation', 'C19'), D['experts']['e1']['base'], 0.02),
    ('Expert 2 live leg', g('Fundamental Valuation', 'C20'), D['experts']['e2']['base'], 0.02),
    ('Income statement FY2030E attributable profit', g('Income Statement', 'I20'), F['np_attr'][4], 1.0),
    ('Balance sheet FY2025 net cash', g('Balance Sheet', 'D17'), HB['FY25']['nd'], 1.0),
    ('Balance sheet FY2030E net debt', g('Balance Sheet', 'I17'), F['net_debt'][4], 1.0),
    ('Balance sheet FY2030E equity', g('Balance Sheet', 'I15'), F['equity'][4], 1.0),
    ('Cash flow FY2026E FCFF', g('Cash Flow', 'B9'), F['fcff'][0], 1.0),
    ('Cash flow FY2030E closing net debt', g('Cash Flow', 'F16'), F['net_debt'][4], 1.0),
    ('Summary financials FY2030E invested capital', g('Summary Financials', 'I13'), F['ic'][4], 1.0),
    ('Relative & Normalized — normalised EPS', g('Relative & Normalized', 'C28'), D['norm']['eps'], 0.002),
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
