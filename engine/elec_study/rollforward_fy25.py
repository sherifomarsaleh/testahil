"""ELEC — FY25 balance-sheet roll-forward triangulation (per instruction).

Question: is FY25 net debt really ~10.2bn? The prior anchor leaned on one ambiguous
press sentence ('obtained credit facilities of EGP 10.9bn during 2025'), which could
mean the drawn year-end balance OR facility limits granted. This script estimates
FY25 net debt WITHOUT that sentence, by rolling the FY24 audited balance sheet
(held with confidence: twice-sourced, and the company's own FY25 filing repeats the
comparatives) forward through the four hard disclosed FY25 points:
    total assets 16,460 / net profit 500.3 / revenue 10,819 / no dividend.

Three estimators:
  A. balance-sheet residual  — debt = (assets - equity) - non-debt liabilities,
     with non-debt liabilities rolled from FY24 on purchase value
  B. cash-flow roll-forward  — ND_25 = ND_24 + interest + tax + capex + dWC - EBITDA
  C. the facilities reading  — 10,900 - cash (the prior anchor, kept as comparison)

A and B are independent of the facilities sentence; C is retained as an upper
cross-check. The reverse test kills the low FY24-vintage alternative (8,172):
holding debt at ~9.0bn forces FY25 non-debt liabilities to ~3.4bn (+39% while
purchase value fell ~21%) — implausible for LC/bank-financed copper imports.

Writes rollforward_result.json; compute.py inputs cite this file as provenance.
"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))

def I(value, source, date, ring):
    return dict(value=value, source=source, date=date, ring=ring)

INP = dict(
    # ---- FY24 actuals (held with confidence) ----
    assets_fy24=I(14970.0, "Zawya/Decypha FY2025 note (comparative) + SWS (15.0bn) — twice-sourced", "2026-03", "Company"),
    debt_fy24=I(8960.0, "Company's own FY25-filing comparative ('vs 8.96bn in 2024'); SWS independent print ~9.0bn", "2026-03-18", "Company"),
    cash_fy24=I(827.6, "Simply Wall St health page (cash & ST investments)", "2025-05-22", "Company"),
    equity_fy24=I(3600.0, "Simply Wall St health page (total shareholder equity)", "2025-05-22", "Company"),
    # ---- FY25 hard disclosed points ----
    assets_fy25=I(16460.0, "Zawya/Decypha FY2025 results (total assets, +9.9%)", "2026-03", "Company"),
    np_fy25=I(500.31, "Arab Finance FY2025 (attributable)", "2026-03", "Company"),
    rev_fy25=I(10819.0, "Arab Finance/Zawya FY2025 (net sales)", "2026-03", "Company"),
    rev_fy24=I(13778.2, "MarketScreener/Mubasher FY2024 consolidated results", "2025-03", "Company"),
    dividends_fy25=I(0.0, "AGM: FY25 profits carried forward, no distribution; no dividend record any year", "2026-05-06", "Company"),
    facilities_fy25=I(10900.0, "'obtained credit facilities of EGP 10.9bn during 2025' — the ambiguous sentence under test", "2026-03-18", "Company"),
    # ---- flow estimates reused from the study (P&L closure chain) ----
    ebitda_fy25=I(2871.0, "P&L closure: EBT 645.6 (=NP/(1-22.5%)) + fin cost 2,150 + D&A ~76 — corroborated by Q1-25 implied ~542/qtr finance", "2026-08-05", "House"),
    fin_cost_fy25=I(2150.0, "House derivation closing FY25 P&L to reported NP (see compute.py)", "2026-08-05", "House"),
    tax_paid_fy25=I(145.3, "EBT 645.6 - NP 500.3 (cash tax ~ current charge assumed)", "2026-08-05", "House"),
    capex_fy25=I(210.0, "Maintenance norm ~EGP 8-9k/t of 25kt capacity (no disclosed capex — flagged)", "2026-08-05", "House"),
    dna_fy25=I(76.0, "0.7% of revenue (FY24 EBITDA-EBIT gap norm)", "2026-08-05", "House"),
    ppe_other_fy25=I(1660.0, "PP&E ~680 + other non-current ~980 (light fixed base, D&A-corroborated)", "2026-08-05", "House"),
    cash_fy25_lo=I(500.0, "Stress floor — minimal operating cash for a name conserving liquidity (no dividend)", "2026-08-05", "House"),
    cash_fy25_hi=I(830.0, "FY24 level held flat", "2026-08-05", "House"),
)
for k, rec in INP.items():
    assert set(rec) == {'value', 'source', 'date', 'ring'} and rec['source'], k
V = {k: r['value'] for k, r in INP.items()}

# ---- step 1: FY25 equity, rolled (no dividend, no revaluation-reserve history) ----
equity_fy25 = V['equity_fy24'] + V['np_fy25'] - V['dividends_fy25']          # 4,100
liab_fy25 = V['assets_fy25'] - equity_fy25                                    # 12,360
non_debt_fy24 = (V['assets_fy24'] - V['equity_fy24']) - V['debt_fy24']        # 2,410

# ---- method A: balance-sheet residual ----
# non-debt liabilities (payables/accruals) scale with purchase value: volume fell
# ~34% while copper-in-EGP rose ~20% => purchase value ~ revenue ratio (~0.785).
purch_scale = V['rev_fy25'] / V['rev_fy24']                                   # 0.785
nd_liab_scaled = non_debt_fy24 * purch_scale                                  # ~1,893
scenarios_A = {
    'flat (2,410)': liab_fy25 - non_debt_fy24,                                # 9,950
    'scaled with purchases (~1,890)': liab_fy25 - nd_liab_scaled,             # ~10,467
    'supplier-credit squeeze (1,500)': liab_fy25 - 1500.0,                    # 10,860
}
debt_A = liab_fy25 - nd_liab_scaled          # central: scaled roll — 10,467
cash_mid = 0.5 * (V['cash_fy25_lo'] + V['cash_fy25_hi'])                      # 665
nd_A = debt_A - cash_mid
nd_A_lo = scenarios_A['flat (2,410)'] - V['cash_fy25_hi']
nd_A_hi = scenarios_A['supplier-credit squeeze (1,500)'] - V['cash_fy25_lo']

# ---- method B: cash-flow roll-forward ----
nd_open = V['debt_fy24'] - V['cash_fy24']                                     # 8,132
d_assets = V['assets_fy25'] - V['assets_fy24']                                # +1,490
d_cash = cash_mid - V['cash_fy24']                                            # ~-163
d_ppe = V['capex_fy25'] - V['dna_fy25']                                       # ~+134
d_gross_wc = d_assets - d_cash - d_ppe                                        # ~+1,519
d_nwc = d_gross_wc - (nd_liab_scaled - non_debt_fy24)                         # ~+2,036
d_nd = (V['fin_cost_fy25'] + V['tax_paid_fy25'] + V['capex_fy25'] + d_nwc
        + V['dividends_fy25'] - V['ebitda_fy25'])
nd_B = nd_open + d_nd

# ---- method C: the facilities reading (prior anchor, comparison only) ----
nd_C = V['facilities_fy25'] - cash_mid

# ---- reverse test on the FY24-vintage low alternative ----
nd_liab_required_if_debt_flat = liab_fy25 - V['debt_fy24']                    # 3,400
growth_required = nd_liab_required_if_debt_flat / non_debt_fy24 - 1           # +41%

# ---- triangulation ----
# central = mean of A and B (independent of the ambiguous sentence); C is the
# soft upper anchor. Rounded to the nearest 5.
nd_central = round((nd_A + nd_B) / 2 / 5) * 5
debt_central = round(debt_A / 5) * 5
out = dict(
    inputs=INP,
    equity_fy25=equity_fy25, liab_fy25=liab_fy25, non_debt_fy24=non_debt_fy24,
    method_A=dict(scenarios=scenarios_A, debt_central=debt_A, cash_mid=cash_mid,
                  nd=nd_A, nd_range=[nd_A_lo, nd_A_hi]),
    method_B=dict(nd_open=nd_open, d_assets=d_assets, d_gross_wc=d_gross_wc,
                  d_nwc=d_nwc, d_nd=d_nd, nd=nd_B),
    method_C=dict(nd=nd_C, note='facilities sentence read as drawn balance — comparison only'),
    reverse_test=dict(non_debt_required=nd_liab_required_if_debt_flat,
                      growth_required=growth_required,
                      verdict='FY24-vintage alternative (ND 8,172) rejected: requires non-debt '
                              'liabilities +41% while purchase value fell 21%'),
    triangulated=dict(net_debt=nd_central, debt=debt_central, cash=cash_mid,
                      non_debt_liab=round(nd_liab_scaled / 5) * 5,
                      nd_range=[round(nd_A_lo / 5) * 5, round(nd_A_hi / 5) * 5]),
)
with open(os.path.join(HERE, 'rollforward_result.json'), 'w') as f:
    json.dump(out, f, indent=1, default=float)

print('FY25 NET-DEBT TRIANGULATION (independent of the facilities sentence)')
print(f'  equity FY25 rolled: {V["equity_fy24"]:,.0f} + NP {V["np_fy25"]:,.1f} - div 0 = {equity_fy25:,.0f}')
print(f'  total liabilities FY25 = assets {V["assets_fy25"]:,.0f} - equity {equity_fy25:,.0f} = {liab_fy25:,.0f}')
print(f'  A. balance-sheet residual: debt {debt_A:,.0f} (non-debt rolled {nd_liab_scaled:,.0f}) - cash {cash_mid:,.0f} => ND {nd_A:,.0f}  [range {nd_A_lo:,.0f}-{nd_A_hi:,.0f}]')
print(f'  B. cash-flow roll-forward: {nd_open:,.0f} + int {V["fin_cost_fy25"]:,.0f} + tax {V["tax_paid_fy25"]:,.0f} + capex {V["capex_fy25"]:,.0f} + dNWC {d_nwc:,.0f} - EBITDA {V["ebitda_fy25"]:,.0f} => ND {nd_B:,.0f}')
print(f'  C. facilities-as-drawn (prior anchor): 10,900 - {cash_mid:,.0f} = {nd_C:,.0f}')
print(f'  reverse test: debt flat at 8,960 needs non-debt liabs {nd_liab_required_if_debt_flat:,.0f} '
      f'(+{growth_required*100:.0f}% while purchases fell 21%) — REJECTED')
print(f'  TRIANGULATED: net debt {nd_central:,.0f}  (debt {debt_central:,.0f}, cash {cash_mid:,.0f});'
      f' range {round(nd_A_lo/5)*5:,.0f}-{round(nd_A_hi/5)*5:,.0f}')
print('rollforward_result.json written')
