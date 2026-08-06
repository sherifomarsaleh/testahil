"""Recalculate the delivered xlsx and reconcile it cell-by-cell against the model.

Recalculation runs through the explicit evaluator in xlcalc.py, independently of the
library that wrote the file. Anything the evaluator cannot parse is a FAILURE, never a
skip — a permissive verifier is worse than no verifier.

Three gates, in increasing strength:
  1. every formula in the workbook must evaluate;
  2. EVERY formula cell must reproduce the value the model itself computed for it (the
     builder records them into xlsx_expected.json as it writes), AND no formula cell may
     be left unchecked;
  3. a hand-written set of headline reconciliations against study_numbers.json, as an
     independent cross-check on the expected map itself.
"""
import json, os, sys
import openpyxl
import xlcalc

HERE = os.path.dirname(os.path.abspath(__file__))
XLSX = os.path.join(HERE, 'SCEM_Valuation_Model_06082026_public.xlsx')
wb = openpyxl.load_workbook(XLSX)
D = json.load(open(os.path.join(HERE, 'study_numbers.json')))
XP = json.load(open(os.path.join(HERE, 'xlsx_expected.json')))
EXPECT = XP['expected']
DCF, LN, W, H, F = D['dcf'], D['lenses'], D['wacc'], D['history'], D['forecast']
M = D['meta']
SH, SPOT = M['shares_mn'], M['spot']

BK = xlcalc.Book(wb)
cv = BK.cell_value

# ---- gate 1: every formula must evaluate ------------------------------------
nform, errors = 0, []
for sh, coord in BK.formula_cells():
    nform += 1
    try:
        cv(sh, coord)
    except Exception as ex:
        errors.append(f'{sh}!{coord}: {ex}')
print(f'formulas: {nform}, unresolvable: {len(errors)}')
for e in errors[:25]:
    print('   ', e)

# ---- gate 2: every formula cell reproduces the model ------------------------
def tol_for(v):
    return max(2e-4, abs(v) * 5e-6)

nchk, drift = 0, []
for sh, cells in EXPECT.items():
    for coord, want in cells.items():
        nchk += 1
        try:
            got = cv(sh, coord)
        except Exception:
            continue
        if not isinstance(got, (int, float)) or abs(float(got) - want) > tol_for(want):
            drift.append((sh, coord, got, want))
print(f'formula cells checked against the model: {nchk}, disagreements: {len(drift)}')
for sh, coord, got, want in drift[:40]:
    g = f'{got:,.6f}' if isinstance(got, (int, float)) else repr(got)
    print(f'   {sh}!{coord}: workbook={g} model={want:,.6f}')

uncovered = [f'{sh}!{coord}' for sh, coord in BK.formula_cells()
             if coord not in EXPECT.get(sh, {})]
print(f'formula cells with no expected value recorded: {len(uncovered)}')
for u in uncovered[:25]:
    print('   ', u)

# ---- gate 3: headline reconciliations ---------------------------------------
checks = [
    ('DCF enterprise value', ('DCF', 'B32'), DCF['ev'], 1.0),
    ('DCF present value of explicit years', ('DCF', 'B30'), DCF['sum_pv'], 1.0),
    ('DCF present value of terminal value', ('DCF', 'B31'), DCF['pv_tv'], 1.0),
    ('DCF terminal value share of EV', ('DCF', 'B33'), DCF['tv_share'], 0.001),
    ('DCF net cash', ('DCF', 'B36'), DCF['net_cash'], 1.0),
    ('DCF equity value', ('DCF', 'B37'), DCF['equity'], 1.0),
    ('DCF fair value per share', ('DCF', 'B39'), DCF['fv'], 0.02),
    ('DCF terminal return on invested capital', ('DCF', 'B24'), DCF['roic_term'], 0.0005),
    ('DCF reinvestment rate', ('DCF', 'B25'), DCF['rr_term'], 0.0005),
    ('Cost of equity — explicit', ('DCF', 'C45'), W['ke_exp'], 0.0002),
    ('WACC — explicit window', ('DCF', 'C46'), W['wacc_exp'], 0.0002),
    ('WACC — terminal', ('DCF', 'C53'), W['wacc_term'], 0.0002),
    ('Market capitalisation', ('DCF', 'C50'), M['mktcap'], 1.0),
    ('Bridge enterprise value', ('EV Bridge', 'B7'), DCF['ev'], 1.0),
    ('Bridge equity value', ('EV Bridge', 'B9'), DCF['equity'], 1.0),
    ('Bridge terminal value share', ('EV Bridge', 'B11'), DCF['tv_share'], 0.001),
    ('Fundamental — DCF lens', ('Fundamental Valuation', 'B5'), LN['values']['DCF (cash flow)'], 0.02),
    ('Fundamental — relative lens', ('Fundamental Valuation', 'B6'),
     LN['values']['Relative multiples'], 0.02),
    ('Fundamental — normalised lens', ('Fundamental Valuation', 'B7'),
     LN['values']['Normalised earnings'], 0.02),
    ('Fundamental — asset lens', ('Fundamental Valuation', 'B8'),
     LN['values']['Asset / replacement cost'], 0.02),
    ('Fundamental — weighted central', ('Fundamental Valuation', 'D10'), LN['central'], 0.02),
    ('Fundamental — terminal value share', ('Fundamental Valuation', 'B16'), DCF['tv_share'], 0.001),
    ('Summary — weighted central', ('Summary', 'B17'), LN['central'], 0.02),
    ('Summary — terminal value share beside the DCF lens', ('Summary', 'E13'), DCF['tv_share'], 0.001),
    ('Summary — terminal value share in the cost-of-capital block', ('Summary', 'B27'),
     DCF['tv_share'], 0.001),
    ('Summary — market capitalisation', ('Summary', 'B7'), M['mktcap'], 1.0),
    ('Unit build reproduces FY2025 revenue', ('Unit Build', 'D10'), H['revenue'][2], 0.5),
    ('Unit build FY2025 residual is zero', ('Unit Build', 'D12'), 0.0, 0.01),
    ('Unit build FY2025 realised price', ('Unit Build', 'D9'), H['price_t'][2], 1.0),
    ('Income statement FY2025 EBITDA', ('Income Statement', 'D6'), H['ebitda'][2], 1.0),
    ('Income statement FY2030E profit after tax', ('Income Statement', 'I14'), F['pat'][4], 1.0),
    ('Balance sheet FY2024 equity (disclosed triple)', ('Balance Sheet', 'C12'), 4775.06, 0.05),
    ('Balance sheet FY2030E equity', ('Balance Sheet', 'I12'), F['equity'][4], 1.0),
    ('Cash flow FY2026E free cash flow to the firm', ('Cash Flow', 'E13'), F['fcff'][0], 1.0),
    ('Relative lens implied value', ('Relative & Normalized', 'B12'),
     LN['values']['Relative multiples'], 0.02),
    ('Normalised lens implied value', ('Relative & Normalized', 'B22'),
     LN['values']['Normalised earnings'], 0.02),
    ('Asset lens implied value', ('Relative & Normalized', 'B33'),
     LN['values']['Asset / replacement cost'], 0.02),
    ('Asset lens EV per tonne at spot', ('Relative & Normalized', 'B27'), LN['ev_per_t_spot'], 0.5),
]
bad = 0
for name, (sh, cd), want, tol in checks:
    try:
        got = cv(sh, cd)
    except Exception as ex:
        got = None
    ok = isinstance(got, (int, float)) and abs(float(got) - float(want)) <= tol
    if not ok:
        bad += 1
    gs = f'{got:,.4f}' if isinstance(got, (int, float)) else repr(got)
    print(f"  [{'OK ' if ok else 'BAD'}] {name}: workbook={gs} model={float(want):,.4f}")

assert not errors, f'{len(errors)} unresolvable formulas'
assert not drift, f'{len(drift)} formula cells disagree with the model'
assert not uncovered, f'{len(uncovered)} formula cells are not checked against the model'
assert bad == 0, f'{bad} reconciliation mismatches'
print(f'\nRECALC OK — {nform} of {nform} formula cells reproduce the model, '
      f'0 unresolvable, 0 unchecked; {len(checks)} headline reconciliations passed')
