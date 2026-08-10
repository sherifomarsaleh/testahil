"""Recalculate the delivered workbook and reconcile it cell-by-cell against the model.

Recalculation runs through the explicit evaluator in xlcalc.py, independently of the library
that wrote the file. Anything the evaluator cannot parse is a FAILURE, never a skip.

Three gates, in increasing strength:
  1. every formula in the workbook must evaluate;
  2. EVERY formula cell must reproduce the value the model itself computed for it, and no
     formula cell may be left unchecked;
  3. a hand-written set of headline reconciliations against study_numbers.json, as an
     independent cross-check on the expected map itself.
"""
import json, os
import openpyxl
import xlcalc

HERE = os.path.dirname(os.path.abspath(__file__))
XLSX = os.path.join(HERE, 'AMR_Valuation_Model_09082026_public.xlsx')
wb = openpyxl.load_workbook(XLSX)
D = json.load(open(os.path.join(HERE, 'study_numbers.json')))
XP = json.load(open(os.path.join(HERE, 'xlsx_expected.json')))
EXPECT = XP['expected']
M, H, F, W, DCF = D['meta'], D['history'], D['forecast'], D['wacc'], D['dcf']
LN, C, U = D['lenses'], D['contested'], D['unit_build']
FX, SH = M['fx'], M['shares_mn']

BK = xlcalc.Book(wb)
cv = BK.cell_value

nform, errors = 0, []
for sh, coord in BK.formula_cells():
    nform += 1
    try:
        cv(sh, coord)
    except Exception as ex:
        errors.append(f'{sh}!{coord}: {ex}')
print(f'formula cells: {nform}, unresolvable: {len(errors)}')
for e in errors[:25]:
    print('   ', e)

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

checks = [
    ('Enterprise value', ('DCF', 'C31'), DCF['ev'], 0.5),
    ('Present value of the explicit years', ('DCF', 'C29'), DCF['sum_pv'], 0.5),
    ('Present value of the terminal value', ('DCF', 'C30'), DCF['pv_tv'], 0.5),
    ('Terminal value share of enterprise value', ('DCF', 'C32'), DCF['tv_share'], 0.0005),
    ('Equity value', ('DCF', 'C37'), DCF['equity'], 0.5),
    ('Fair value per share at 31 December 2025, USD', ('DCF', 'C38'), DCF['fv_unrolled'], 0.002),
    ('Fair value per share rolled to the anchor, AED', ('DCF', 'C39'), DCF['fv'] * FX, 0.005),
    ('Cyclical reading, live block, AED', ('DCF', 'C79'), C['way_b']['value_aed'], 0.005),
    ('Terminal ROIC is the faded target', ('DCF', 'C25'), W['terminal_roic'], 1e-9),
    ('Expert 1 formula leg', ('Fundamental Valuation', 'C26'), D['experts'][0]['base'] * FX, 0.005),
    ('Expert 3 formula leg', ('Fundamental Valuation', 'C28'), D['experts'][2]['base'] * FX, 0.005),
    ('Weighted bear', ('Summary', 'B10'), sum(LN['ranges'][k][0] * LN['weights'][k] for k in ['Discounted cash flow', 'Relative multiples', 'Normalised earnings power', 'Book value and sustainable return']) * FX, 0.005),
    ('Terminal return on invested capital', ('DCF', 'C25'), DCF['roic_term'], 0.0005),
    ('Reinvestment rate', ('DCF', 'C26'), DCF['rr_term'], 0.0005),
    ('Cost of equity', ('DCF', 'C52'), W['ke_rating'], 0.0002),
    ('Cost of capital, explicit window', ('DCF', 'C46'), W['wacc_rating'], 0.0002),
    ('Cost of capital, terminal', ('DCF', 'C53'), W['wacc_terminal'], 0.0002),
    ('Cost of capital, credit-default-swap basis', ('DCF', 'C68'), W['wacc_cds'], 0.0002),
    ('Market capitalisation', ('DCF', 'C56'), M['mktcap'], 0.5),
    ('Bridge — enterprise value', ('SOTP Bridge', 'B7'), DCF['ev'], 0.5),
    ('Bridge — equity value', ('SOTP Bridge', 'B12'), DCF['equity'], 0.5),
    ('Bridge — terminal value share', ('SOTP Bridge', 'B14'), DCF['tv_share'], 0.0005),
    ('Summary — terminal value share beside the cash-flow lens', ('Summary', 'G5'),
     DCF['tv_share'], 0.0005),
    ('Summary — weighted central', ('Summary', 'C10'), LN['central'] * FX, 0.005),
    ('Summary — cash-flow lens', ('Summary', 'C5'),
     LN['values']['Discounted cash flow'] * FX, 0.005),
    ('Summary — relative lens', ('Summary', 'C6'), LN['values']['Relative multiples'] * FX, 0.005),
    ('Summary — normalised lens', ('Summary', 'C7'),
     LN['values']['Normalised earnings power'] * FX, 0.005),
    ('Summary — book lens', ('Summary', 'C8'),
     LN['values']['Book value and sustainable return'] * FX, 0.005),
    ('Summary — weights sum to one', ('Summary', 'E10'), 1.0, 1e-9),
    ('Unit build — FY2025 revenue before eliminations', ('Segments', 'D32'), 2540.744, 0.01),
    ('Unit build — FY2026E revenue adopted', ('Segments', 'E36'), F['revenue'][0], 0.05),
    ('Unit build — FY2030E revenue', ('Segments', 'I36'), F['revenue'][4], 0.05),
    ('Unit build — total restaurants FY2030E', ('Segments', 'G12'), F['stores'][4], 0.5),
    ('Income statement — FY2025 EBITDA margin', ('Income Statement', 'D9'),
     H['ebitda_margin'][2], 0.0005),
    ('Income statement — FY2030E profit', ('Income Statement', 'I17'), F['pat'][4], 0.5),
    ('Income statement — FY2023 profit attributable', ('Income Statement', 'B19'),
     H['pat_shareholders'][0], 0.01),
    ('Balance sheet — FY2030E equity', ('Balance Sheet', 'I14'), F['equity'][4], 0.5),
    ('Balance sheet — FY2030E invested capital', ('Balance Sheet', 'I18'),
     F['invested_capital'][4], 0.5),
    ('Balance sheet — FY2025 net debt', ('Balance Sheet', 'D17'), H['net_debt'][2], 0.01),
    ('Cash flow — FY2026E free cash flow to the firm', ('Cash Flow', 'E15'), F['fcff'][0], 0.5),
    ('Cash flow — FY2030E capital expenditure including leases', ('Cash Flow', 'I12'),
     F['capex_total'][4], 0.5),
    ('Relative lens — implied value per share', ('Relative & Normalized', 'B12'),
     LN['values']['Relative multiples'] * FX, 0.005),
    ('Normalised lens — implied value per share', ('Relative & Normalized', 'B31'),
     LN['values']['Normalised earnings power'] * FX, 0.005),
    ('Book lens — implied value per share', ('Relative & Normalized', 'B40'),
     LN['values']['Book value and sustainable return'] * FX, 0.005),
    ('Trailing enterprise value / EBITDA', ('Relative & Normalized', 'B16'),
     D['trailing']['ev_ebitda'], 0.01),
    ('Expert panel median', ('Fundamental Valuation', 'C29'), LN['expert_median'] * FX, 0.005),
    ('The contested judgement — the gap', ('Fundamental Valuation', 'C15'), C['gap_pct'], 0.0005),
    ('Per-share — FY2025 earnings per share, USD', ('Per-Share & Ratios', 'D5'),
     H['eps'][2], 0.0005),
    ('Per-share — FY2030E return on invested capital', ('Per-Share & Ratios', 'I14'),
     F['roic'][4], 0.0005),
]
bad = 0
for name, (sh, cd), want, tol in checks:
    try:
        got = cv(sh, cd)
    except Exception:
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
print(f'\nRECALC OK — {nform} of {nform} formula cells reproduce the model, 0 unresolvable, '
      f'0 unchecked; {len(checks)} headline reconciliations passed')
json.dump(dict(n_formula=nform, unresolvable=0, unchecked=0, disagreements=0,
               headline_checks=len(checks), n_pasted=XP['n_pasted'],
               pasted_audited=len(XP['pasted']['audited']),
               pasted_engine=len(XP['pasted']['engine']),
               pasted_grid=len(XP['pasted']['grid'])),
          open(os.path.join(HERE, 'recalc_result.json'), 'w'), indent=1)
