"""Recalculate the DELIVERED workbook and reconcile it against the model.

Verification runs on the delivered file, not on the builder. The evaluator in
xlcalc.py is an independent reimplementation of the formula set: anything it
cannot parse is reported as a FAILURE, never skipped.

Three gates, in increasing strength:
  1. every formula in the workbook must evaluate;
  2. EVERY formula cell must reproduce the value the model itself computed for
     it — the builder records those as it writes — and no formula cell may be
     left unchecked. This is the gate that makes a formula-driven workbook safe:
     a formula that computes the right thing the wrong way, or points one row
     off, fails here rather than shipping a different number from the study;
  3. a hand-written set of headline reconciliations straight against
     study_numbers.json, as an independent cross-check on the expected map.
"""
import json, os
import openpyxl
import xlcalc

HERE = os.path.dirname(os.path.abspath(__file__))
XLSX = os.path.join(HERE, 'ADNOCDRILL_Valuation_Model_09082026.xlsx')
wb = openpyxl.load_workbook(XLSX)
D = json.load(open(os.path.join(HERE, 'study_numbers.json')))
XP = json.load(open(os.path.join(HERE, 'xlsx_expected.json')))
EXPECT, ANCH = XP['expected'], XP['anchors']
CA, CB = D['cases']['A'], D['cases']['B']
W, M, FV, REL, NORM, BOOK, H = (D['wacc'], D['market'], D['fair_value'], D['relative'],
                                D['normalised'], D['book'], D['history'])

BK = xlcalc.Book(wb)
g = BK.cell_value

# ---- gate 1: every formula must evaluate ------------------------------------
nform, errors = 0, []
for sh, coord in BK.formula_cells():
    nform += 1
    try:
        g(sh, coord)
    except Exception as ex:
        errors.append(f'{sh}!{coord}: {ex}')
print(f'formulas: {nform}, unresolvable: {len(errors)}')
for e in errors[:20]:
    print('  ', e)


def tol_for(v):
    return max(2e-4, abs(v) * 5e-6)


# ---- gate 2: every formula cell must reproduce the model ---------------------
nchk, drift = 0, []
for sh, cells in EXPECT.items():
    for coord, want in cells.items():
        nchk += 1
        got = g(sh, coord)
        if not isinstance(got, (int, float)) or abs(float(got) - want) > tol_for(want):
            drift.append((sh, coord, got, want))
print(f'formula cells checked against the model: {nchk}, disagreements: {len(drift)}')
for sh, coord, got, want in drift[:25]:
    gg = f'{got:,.6f}' if isinstance(got, (int, float)) else repr(got)
    print(f'   {sh}!{coord}: workbook={gg} model={want:,.6f}')

uncovered = [f'{sh}!{coord}' for sh, coord in BK.formula_cells()
             if coord not in EXPECT.get(sh, {})]
print(f'formula cells with no expected value recorded: {len(uncovered)}')
for u in uncovered[:20]:
    print('  ', u)

# ---- gate 3: headline reconciliations ---------------------------------------
DR, TR, BT, GR, NR, LV = (ANCH['dcf'], ANCH['terminal'], ANCH['plateau'], ANCH['bridge'],
                          ANCH['relnorm'], ANCH['lens_rows'])
checks = [
    ('Normalised risk-free rate', g('DCF', f"C{DR['rf_star']}"), W['rf_star'], 1e-9),
    ('Cost of equity — rating basis', g('DCF', f"C{DR['ke_r']}"), W['ke_rating'], 1e-9),
    ('Cost of equity — CDS basis', g('DCF', f"C{DR['ke_c']}"), W['ke_cds'], 1e-9),
    ('Marginal cost of debt, pre-tax', g('DCF', f"C{DR['kd_pre']}"), W['kd_pretax'], 1e-9),
    ('Sovereign floor', g('DCF', f"C{DR['sov']}"), W['sovereign_floor'], 1e-9),
    ('Weight of equity', g('DCF', f"C{DR['we']}"), W['weight_equity'], 1e-6),
    ('WACC — rating basis', g('DCF', f"C{DR['wacc_r']}"), W['wacc_rating'], 1e-9),
    ('WACC — CDS basis', g('DCF', f"C{DR['wacc_c']}"), W['wacc_cds'], 1e-9),
    ('Present value of the explicit five years', g('DCF', f"C{TR['pv_exp']}"),
     CA['pv_explicit'], 1.0),
    ('Present value of the terminal value', g('DCF', f"C{TR['pv_tv']}"), CA['pv_terminal'], 1.0),
    ('Enterprise value — continued expansion', g('DCF', f"C{TR['ev']}"),
     CA['enterprise_value'], 1.0),
    ('Terminal value share of enterprise value — expansion', g('DCF', f"C{TR['tvshare']}"),
     CA['tv_pct_of_ev'], 1e-6),
    ('Enterprise value — capacity plateau', g('DCF', f"C{BT['ev']}"), CB['enterprise_value'], 1.0),
    ('Terminal value share of enterprise value — plateau', g('DCF', f"C{BT['tvshare']}"),
     CB['tv_pct_of_ev'], 1e-6),
    ('Bridge equity value — expansion', g('SOTP Bridge', f"B{GR['eq']}"), CA['equity_value'], 1.0),
    ('Bridge equity value — plateau', g('SOTP Bridge', f"C{GR['eq']}"), CB['equity_value'], 1.0),
    ('Value per share (AED) — expansion', g('SOTP Bridge', f"B{GR['ps_aed']}"),
     CA['value_per_share_aed'], 0.005),
    ('Value per share (AED) — plateau', g('SOTP Bridge', f"C{GR['ps_aed']}"),
     CB['value_per_share_aed'], 0.005),
    ('Relative lens value per share', g('Relative & Normalized', f"C{NR['ps']}"),
     REL['value_per_share_aed'], 0.005),
    ('Segment-weighted peer multiple', g('Relative & Normalized', f"C{NR['blend']}"),
     REL['blended_multiple'], 0.005),
    ("The company's own EV/EBITDA", g('Relative & Normalized', f"C{NR['own']}"),
     REL['implied_own_ev_ebitda'], 0.005),
    ('Normalised lens value per share', g('Relative & Normalized', f"C{NR['nps']}"),
     NORM['value_per_share_aed'], 0.005),
    ('Book lens value per share', g('Relative & Normalized', f"C{NR['bps']}"),
     BOOK['value_per_share_aed'], 0.005),
    ('Justified price / book', g('Relative & Normalized', f"C{NR['pb']}"),
     BOOK['justified_pb'], 0.005),
    ('Weighted central fair value', g('Summary', f"B{ANCH['central_row']}"), FV['central'], 0.005),
    ('Weighted central — Fundamental Valuation sheet',
     g('Fundamental Valuation', f"B{ANCH['fundamental_central']}"), FV['central'], 0.005),
    ('Lens weights sum to one', g('Fundamental Valuation',
                                  f"C{ANCH['fundamental_central']}"), 1.0, 1e-9),
    ('Market capitalisation', g('DCF', f"C{DR['mcap']}"), M['market_cap_usd_k'], 1.0),
    ('FY2025 revenue', g('Income Statement', f"D{ANCH['income']['revenue']}"),
     H['2025']['revenue'], 1.0),
    ('FY2025 EBITDA', g('Income Statement', f"D{ANCH['income']['ebitda']}"),
     H['2025']['ebitda'], 1.0),
    ('FY2025 profit after tax', g('Income Statement', f"D{ANCH['income']['pat']}"),
     H['2025']['pat'], 1.0),
    ('FY2025 total assets', g('Balance Sheet', f"D{ANCH['balance']['total_assets']}"),
     H['2025']['total_assets'], 1.0),
    ('FY2026E revenue', g('Segments', f"E{ANCH['segments']['revenue']}"),
     CA['rows'][0]['revenue'], 1.0),
    ('FY2026E EBITDA', g('Segments', f"E{ANCH['segments']['ebitda']}"),
     CA['rows'][0]['ebitda'], 1.0),
    ('FY2030E free cash flow to the firm', g('Cash Flow', f"I{ANCH['cash']['fcff']}"),
     CA['rows'][-1]['fcff'], 1.0),
    ('FY2030E closing cash', g('Cash Flow', f"I{ANCH['cash']['close']}"),
     CA['rows'][-1]['cash_close'], 1.0),
]
bad = 0
for name, got, want, tol in checks:
    ok = got is not None and abs(float(got) - float(want)) <= tol
    bad += 0 if ok else 1
    print(f"  [{'OK ' if ok else 'BAD'}] {name}: workbook={float(got):,.6f} "
          f"model={float(want):,.6f}")

# ---- the forecast balance sheet must balance in the DELIVERED file -----------
BALR, EQR, TLR = (ANCH['balance']['total_assets'], ANCH['balance']['equity'],
                  ANCH['balance']['total_liabilities'])
bal_gap = []
for col in ('E', 'F', 'G', 'H', 'I'):
    ta, tl, eq = (g('Balance Sheet', f'{col}{BALR}'), g('Balance Sheet', f'{col}{TLR}'),
                  g('Balance Sheet', f'{col}{EQR}'))
    if abs(ta - (tl + eq)) > 1.0:
        bal_gap.append((col, ta, tl + eq))
print(f'forecast balance sheet balances in every year: {not bal_gap}')

assert not errors, f'{len(errors)} unresolvable formulas'
assert not drift, f'{len(drift)} formula cells disagree with the model'
assert not uncovered, f'{len(uncovered)} formula cells are not checked against the model'
assert bad == 0, f'{bad} reconciliation mismatches'
assert not bal_gap, f'balance sheet does not balance: {bal_gap}'
print(f'RECALC OK — {nform} of {nform} formula cells reproduce the model, 0 unresolvable, '
      f'0 unchecked; {len(checks)} headline reconciliations passed')
