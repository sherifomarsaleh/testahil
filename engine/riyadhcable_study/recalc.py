"""Recalculate the delivered xlsx and reconcile it against study_numbers.json.
Independent evaluator (xlcalc.py) over the formula set the builder emits; anything it
cannot parse is a FAILURE, never a skip. Three gates, increasing strength:
  1. every formula evaluates;
  2. every formula cell reproduces the model's own value (xlsx_expected.json) AND every
     formula cell is covered by the expected map — no unchecked formulas;
  3. headline reconciliations against study_numbers.json.
"""
import json, os
import openpyxl
import xlcalc

HERE = os.path.dirname(os.path.abspath(__file__))
XLSX = os.path.join(HERE, 'RIYADHCABLE_Valuation_Model_18082026_public.xlsx')
wb = openpyxl.load_workbook(XLSX)
D = json.load(open(os.path.join(HERE, 'study_numbers.json')))
XP = json.load(open(os.path.join(HERE, 'xlsx_expected.json')))
EXPECT = XP['expected']
DCF, LN, F, HI, HB = D['dcf'], D['lenses'], D['fcst'], D['hist_is'], D['hist_bs']
SPOT = D['meta']['spot']

BK = xlcalc.Book(wb)
cv = BK.cell_value

# gate 1
nform, errors = 0, []
for sh, coord in BK.formula_cells():
    nform += 1
    try:
        cv(sh, coord)
    except Exception as ex:
        errors.append(f'{sh}!{coord}: {ex}')
print(f'formulas: {nform}, unresolvable: {len(errors)}')
for e in errors[:25]:
    print('  ', e)

# gate 2
def tol_for(v):
    return max(2e-4, abs(v) * 5e-6)

nchk, drift = 0, []
for sh, cells in EXPECT.items():
    for coord, want in cells.items():
        nchk += 1
        got = cv(sh, coord)
        if not isinstance(got, (int, float)) or abs(float(got) - want) > tol_for(want):
            drift.append((sh, coord, got, want))
print(f'formula cells checked against the model: {nchk}, disagreements: {len(drift)}')
for sh, coord, got, want in drift[:30]:
    g = f'{got:,.6f}' if isinstance(got, (int, float)) else repr(got)
    print(f'   {sh}!{coord}: workbook={g} model={want:,.6f}')

uncovered = [f'{sh}!{coord}' for sh, coord in BK.formula_cells()
             if coord not in EXPECT.get(sh, {})]
print(f'formula cells with no expected value recorded: {len(uncovered)}')
for u in uncovered[:20]:
    print('  ', u)

# gate 3 — headline reconciliations
checks = [
    ('DCF enterprise value', ('DCF', 'C41'), DCF['ev'], 1.0),
    ('DCF terminal value share', ('DCF', 'C42'), DCF['tv_share'], 0.002),
    ('DCF value per share at anchor', ('DCF', 'C51'), DCF['ps'], 0.02),
    ('DCF WACC explicit', ('DCF', 'C10'), D['wacc']['wacc'], 0.0002),
    ('DCF WACC terminal', ('DCF', 'C13'), D['wacc']['wacc_term'], 0.0002),
    ('Bridge equity attributable', ('SOTP Bridge', 'C10'), DCF['eq_attr'], 1.0),
    ('Bridge terminal value share', ('SOTP Bridge', 'C6'), DCF['tv_share'], 0.002),
    ('Fundamental — DCF lens', ('Fundamental Valuation', 'C5'), LN['dcf']['base'], 0.02),
    ('Fundamental — relative lens', ('Fundamental Valuation', 'C6'), LN['relative']['base'], 0.02),
    ('Fundamental — normalised lens', ('Fundamental Valuation', 'C7'), LN['normalized']['base'], 0.02),
    ('Fundamental — book lens', ('Fundamental Valuation', 'C8'), LN['book']['base'], 0.02),
    ('Fundamental — weighted central', ('Fundamental Valuation', 'C9'), D['central'], 0.02),
    ('Summary weighted central', ('Summary', 'C9'), D['central'], 0.02),
    ('Summary terminal value share', ('Summary', 'C10'), DCF['tv_share'], 0.002),
    ('Segments FY2026E revenue', ('Segments', 'C12'), F['rev'][0], 1.0),
    ('Segments FY2026E gross margin', ('Segments', 'C11'), F['gm'][0], 0.0005),
    ('Income statement FY2025 EBITDA', ('Income Statement', 'E9'), HI['FY25']['ebitda'], 1.0),
    ('Income statement FY2030E attributable profit', ('Income Statement', 'J16'), F['np_attr'][4], 1.0),
    ('Balance sheet FY2030E net debt', ('Balance Sheet', 'J13'), F['net_debt'][4], 1.0),
    ('Cash flow FY2026E FCFF', ('Cash Flow', 'C9'), F['fcff'][0], 1.0),
    ('Relative lens implied value', ('Relative & Normalized', 'C8'), LN['relative']['base'], 0.02),
]
bad = 0
for name, (sh, coord), want, tol in checks:
    got = cv(sh, coord)
    ok = isinstance(got, (int, float)) and abs(float(got) - float(want)) <= tol
    if not ok:
        bad += 1
    print(f"  [{'OK ' if ok else 'BAD'}] {name}: workbook={got if not isinstance(got,(int,float)) else round(got,4)} model={round(float(want),4)}")

assert not errors, f'{len(errors)} unresolvable formulas'
assert not drift, f'{len(drift)} formula cells disagree with the model'
assert not uncovered, f'{len(uncovered)} formula cells not checked against the model'
assert bad == 0, f'{bad} reconciliation mismatches'
print(f'\nRECALC OK — {nform} formulas, 0 unresolvable, {nchk} cell-level agreements with the model, '
      f'{len(checks)} headline reconciliations passed')
