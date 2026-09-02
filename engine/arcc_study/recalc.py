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
XLSX = os.path.join(HERE, 'ARCC_Valuation_Model_02092026_public.xlsx')
wb = openpyxl.load_workbook(XLSX)
D = json.load(open(os.path.join(HERE, 'study_numbers.json')))
XP = json.load(open(os.path.join(HERE, 'xlsx_expected.json')))
EXPECT = XP
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
    ('DCF enterprise value', ('DCF', 'B33'), DCF['ev'], 1.0),
    ('DCF present value of explicit years', ('DCF', 'B31'), DCF['sum_pv'], 1.0),
    ('DCF present value of terminal value', ('DCF', 'B32'), DCF['pv_tv'], 1.0),
    ('DCF terminal value share of EV', ('DCF', 'B34'), DCF['tv_share'], 0.001),
    ('DCF cash at the valuation date', ('DCF', 'B38'), DCF['cash_at_val'], 1.0),
    ('DCF net cash', ('DCF', 'B40'), DCF['net_cash'], 1.0),
    ('DCF equity value', ('DCF', 'B42'), DCF['equity'], 1.0),
    ('DCF shares outstanding', ('DCF', 'B43'), D['meta']['shares_mn'], 0.0001),
    ('DCF fair value per share', ('DCF', 'B44'), DCF['fv'], 0.02),
    ('DCF terminal return on capital, replacement basis', ('DCF', 'B24'),
     DCF['roic_term'], 0.0005),
    ('DCF return on BOOK capital, FY2025', ('DCF', 'B25'),
     D['terminal_reconciliation']['roic_book_fy25'], 0.002),
    ('DCF reinvestment rate', ('DCF', 'B26'), DCF['rr_term'], 0.0005),
    ('Cost of equity', ('DCF', 'C39'), W['ke_exp'], 0.0002),
    ('WACC — explicit window', ('DCF', 'C40'), W['wacc_exp'], 0.0002),
    ('Cost of debt blended by currency', ('DCF', 'C41'), W['kd'], 0.0002),
    ('Euro share of the debt book', ('DCF', 'C46'), W['eur_share'], 0.001),
    ('WACC — terminal', ('DCF', 'C50'), W['wacc_term'], 0.0002),
    ('Terminal beta re-levered', ('DCF', 'C47'), W['beta_term'], 0.001),
    ('Market capitalisation', ('DCF', 'C45'), D['meta']['mktcap'], 1.0),
    ('Total interest-bearing debt', ('DCF', 'C44'), W['debt_total'], 0.01),
    ('Kd gate: FY2025 effective rate', ('DCF', 'B61'), D['kd_gate']['eff_fy25'], 0.0005),
    ('Kd gate: pound-equivalent cost of debt', ('DCF', 'B63'),
     D['kd_gate']['kd_egp_equivalent'], 0.0005),
    ('Bridge enterprise value', ('SOTP Bridge', 'B7'), DCF['ev'], 1.0),
    ('Bridge equity value', ('SOTP Bridge', 'B10'), DCF['equity'], 1.0),
    ('Bridge terminal value share', ('SOTP Bridge', 'B12'), DCF['tv_share'], 0.001),
    ('Unit build: FY2025 total despatches', ('Segments', 'B18'),
     D['unit_calibration']['vol_fy25'], 0.001),
    ('Unit build: mill utilisation', ('Segments', 'B14'),
     D['unit_calibration']['util_fy25'], 0.001),
    ('Unit build: clinker produced (Mt)', ('Segments', 'B7'),
     D['unit_calibration']['clk_prod'], 0.001),
    ('Unit build: cement produced (Mt)', ('Segments', 'B12'),
     D['unit_calibration']['cem_prod'], 0.001),
    ('Unit build: LOCAL CEMENT PRICE, derived', ('Segments', 'B22'),
     D['unit_calibration']['price_loc_derived'], 1.0),
    ('Unit build: EXPORT CEMENT PRICE USD, derived', ('Segments', 'B26'),
     D['unit_calibration']['price_exp_cem_usd'], 0.1),
    ('Unit build: EXPORT CLINKER PRICE USD, derived', ('Segments', 'B27'),
     D['unit_calibration']['price_exp_clk_usd'], 0.1),
    ('Unit build: cement exports inside the 30% cap', ('Segments', 'B28'),
     D['unit_calibration']['vol_cem_exp'] / D['unit_calibration']['cem_prod'], 0.001),
    ('Unit build: FY2025 cash cost per tonne sold', ('Segments', 'B38'),
     D['unit_calibration']['cash_cost_t'], 0.5),
    ('Unit build: reconstructed FY2025 revenue', ('Segments', 'B76'),
     D['bottom_up'][0]['rev'], 1.0),
    ('Unit build: revenue residual against AUDITED', ('Segments', 'B78'),
     D['bottom_up'][0]['rev'] / D['inputs']['rev_fy25']['value'] - 1, 0.001),
    ('Unit build: EBITDA residual against AUDITED', ('Segments', 'B81'),
     D['bottom_up'][0]['ebitda'] / H['ebitda'][2] - 1, 0.001),
    ('Unit build: peak kiln utilisation stays below 100%', ('Segments', 'B94'),
     max(b['kiln_util'] for b in D['bottom_up'][1:]), 0.001),
    ('Unit build: peak mill utilisation stays below 100%', ('Segments', 'B98'),
     max(b['mill_util'] for b in D['bottom_up'][1:]), 0.001),
    ('Income statement FY2025 operating profit', ('Income Statement', 'D11'),
     H['ebit'][2], 0.01),
    ('Income statement FY2025 EBITDA', ('Income Statement', 'D14'), H['ebitda'][2], 0.01),
    ('Income statement FY2023 EBITDA', ('Income Statement', 'B14'), H['ebitda'][0], 0.01),
    ('Income statement FY2030E profit', ('Income Statement', 'I20'), F['pat'][4], 1.0),
    ('Balance sheet closes to zero', ('Balance Sheet', 'B25'), 0.0, 0.001),
    ('Balance sheet FY2030E equity', ('Balance Sheet', 'I15'), F['equity'][4], 1.0),
    ('Cash flow FY2026E free cash flow to the firm', ('Cash Flow', 'C13'), F['fcff'][0], 1.0),
    ('Relative lens implied value', ('Relative & Normalized', 'B23'),
     LN['values']['Relative multiples'], 0.02),
    ('Normalised earnings, the DIAGNOSTIC this class does not weight',
     ('Relative & Normalized', 'B31'),
     LN['diagnostic']['Normalised earnings (diagnostic, not a lens for this class)'], 0.02),
    ('Asset lens implied value', ('Fundamental Valuation', 'B13'),
     LN['values']['Asset / replacement cost'], 0.02),
    ('Asset lens EV per tonne at spot', ('Fundamental Valuation', 'B14'),
     LN['ev_per_t_spot'], 0.5),
    ('Share reconciliation: shares outstanding', ('Per-Share & Ratios', 'B16'),
     D['meta']['shares_mn'], 0.0001),
    ('Share reconciliation: dividend-implied difference', ('Per-Share & Ratios', 'B18'),
     D['share_triangulation']['from_fy25_dividend'] / D['meta']['shares_mn'] - 1, 0.0001),
    ('Summary — DCF lens', ('Summary', 'B5'), LN['values']['DCF (cash flow)'], 0.02),
    ('Summary — the central IS the cash-flow lens, not a blend',
     ('Summary', 'B9'), LN['central'], 0.02),
    ('Summary — the retired 50/20/22/8 blend, published but unused',
     ('Summary', 'B14'),
     0.50 * LN['values']['DCF (cash flow)'] + 0.20 * LN['values']['Relative multiples']
     + 0.22 * LN['diagnostic']['Normalised earnings (diagnostic, not a lens for this class)']
     + 0.08 * LN['values']['Asset / replacement cost'], 0.02),
    ('Summary — terminal value share beside the DCF lens', ('Summary', 'E5'),
     DCF['tv_share'], 0.001),
    ('Peer sheet — subject price/earnings recomputed', ('Peer & Sector', 'E5'),
     D['peers']['self']['pe'], 0.01),
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
