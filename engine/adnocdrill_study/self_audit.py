"""Self-audit: price every defect found in the study before judging it.

Each entry re-runs the valuation with ONE thing changed and reports the move in
the weighted central, in dirhams per share and as a percentage of it. Nothing is
called immaterial here without a number beside the word.

The harness imports compute.py's own objects so the alternatives are computed by
the same code that produced the delivered answer, not by a re-implementation.
"""
import json, os, sys, importlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..'))
import numpy as np
import compute as C

BASE = C.central
SPOT = C.V('spot_aed')
FINDINGS = []


def price(tag, what, new_central, note=''):
    d = new_central - BASE
    FINDINGS.append(dict(tag=tag, what=what, central=new_central, delta=d,
                         pct_of_central=d / BASE, note=note))
    print(f"{tag:5s} {what[:66]:66s} AED {new_central:5.2f}  {d:+5.2f}  "
          f"{d/BASE*100:+6.1f}%")


def reweight(fair):
    return sum(fair[k] * C.LENS_WEIGHT[k] for k in fair)


print(f"BASE weighted central AED {BASE:.2f} against a market price of AED {SPOT:.2f}\n")
print(f"{'':5s} {'':66s} {'central':>9s} {'move':>6s} {'':>7s}")

# ---------------------------------------------------------------- A. WORKING CAPITAL
# The three-year average is 5.91% of revenue. The most recent balance sheet —
# 30 June 2026, which the study already uses for the bridge — implies 9.01% on
# annualised revenue. The model's own first forecast year is therefore below the
# latest observed level.
wc_1h26 = (342783.0 + 233060.0 + 1418236.0) - (1197504.0 + 40533.0) - 312862.0
wc_pct_1h26 = wc_1h26 / (C.V('rev_1h26') * 2)
orig_wc = C.WC_PCT_REVENUE
for label, pct in (('A1', wc_pct_1h26), ('A2', (orig_wc + wc_pct_1h26) / 2)):
    C.WC_PCT_REVENUE = pct
    cases = {c: C.build_case(c) for c in ('A', 'B')}
    fair = dict(C.FAIR)
    fair['dcf_A'] = cases['A']['value_per_share_aed']
    fair['dcf_B'] = cases['B']['value_per_share_aed']
    price(label, f'working capital at {pct*100:.2f}% of revenue '
                 f'({"the 1H-2026 actual" if label == "A1" else "midway to it"})',
          reweight(fair))
C.WC_PCT_REVENUE = orig_wc

# ---------------------------------------------------------------- B. TERMINAL RATE
# The terminal value is discounted at today's cost of capital, which carries a
# 7.7% debt weight. The model's own forecast has net debt turning NEGATIVE by
# 2030, so the terminal firm is all-equity and should be discounted at the cost
# of equity.
orig_wacc = C.WACC
for label, w, desc in (('B1', C.ke_rating, 'terminal discounted at the cost of equity '
                        '(the model\'s own 2030 firm is net cash)'),):
    C.WACC = w
    cases = {c: C.build_case(c) for c in ('A', 'B')}
    fair = dict(C.FAIR)
    fair['dcf_A'] = cases['A']['value_per_share_aed']
    fair['dcf_B'] = cases['B']['value_per_share_aed']
    # the normalised lens also capitalises at WACC - g
    nev = C.norm_nopat / (w - C.V('terminal_growth_B'))
    neq = (nev + C.V('jvinv_1h26') + C.V('cash_1h26') - C.V('debt_1h26')
           - C.V('lease_1h26') - C.V('nci_1h26') - C.V('finliab_1h26'))
    fair['normalised'] = neq / C.shares_out_k * C.V('fx_aed_usd')
    price(label, desc, reweight(fair))
C.WACC = orig_wacc

# ---------------------------------------------------------------- C. BOOK LENS
# The lens uses a 36.74% sustainable return on equity. The model's OWN forecast
# has the return falling from 33.8% to 29.2% across the window, because equity
# compounds faster than profit under the guided dividend floor.
rows = C.CASE['A']['rows']
prev = C.H[2025]['equity']
roes = []
for r in rows:
    eq = r['balance_sheet']['equity_residual']
    roes.append(r['pat'] / ((prev + eq) / 2))
    prev = eq
for label, roe, desc in (('C1', roes[-1], 'book lens at the return the model itself forecasts '
                          'for 2030'),
                         ('C2', float(np.mean(roes)), 'book lens at the average forecast return')):
    pb = (roe - C.g_book) / (C.ke_rating - C.g_book)
    fair = dict(C.FAIR)
    fair['book'] = pb * C.book_equity_now / C.shares_out_k * C.V('fx_aed_usd')
    price(label, f'{desc} ({roe*100:.1f}%)', reweight(fair))

# ---------------------------------------------------------------- D. NORMALISED LENS
# (i) The lens is described as crediting no growth, but capitalises at the cost
# of capital LESS a 1.5% terminal growth rate. (ii) Its depreciation charge sits
# midway between maintenance capex and the 2030 charge, while the fleet it prices
# is the 2026 fleet.
fair = dict(C.FAIR)
ev = C.norm_nopat / C.WACC
eq = (ev + C.V('jvinv_1h26') + C.V('cash_1h26') - C.V('debt_1h26') - C.V('lease_1h26')
      - C.V('nci_1h26') - C.V('finliab_1h26'))
fair['normalised'] = eq / C.shares_out_k * C.V('fx_aed_usd')
price('D1', 'normalised lens with genuinely no growth (capitalised at the cost of capital)',
      reweight(fair))

fair = dict(C.FAIR)
dna_full = rows[0]['dna']          # the depreciation the 2026 fleet actually carries
ev = (C.norm_ebitda - dna_full) * (1 - C.V('tax_rate')) / (C.WACC - C.V('terminal_growth_B'))
eq = (ev + C.V('jvinv_1h26') + C.V('cash_1h26') - C.V('debt_1h26') - C.V('lease_1h26')
      - C.V('nci_1h26') - C.V('finliab_1h26'))
fair['normalised'] = eq / C.shares_out_k * C.V('fx_aed_usd')
price('D2', f'normalised lens at the depreciation the priced fleet carries '
            f'({dna_full/1e3:,.0f}m, not {C.norm_dna/1e3:,.0f}m)', reweight(fair))

# ---------------------------------------------------------------- E. NCI
# The bridge deducts non-controlling interests at book value while the forecast
# consolidates 100% of the regional businesses' earnings. Deducting the minority
# on an EARNINGS basis is the coherent treatment.
seg_rev_regional = rows[0]['rev_regional']
minority_share = 0.25          # 30% of SLDC, 20% of MBPS — weighted by rig count
mult = C.CASE['A']['enterprise_value'] / rows[0]['ebitda_ex_jv']
# the regional book earns roughly the group conventional margin
nci_earnings_basis = seg_rev_regional * rows[0]['ebitda_ex_jv'] / rows[0]['revenue'] \
    * minority_share * mult
for label, v, desc in (('E1', nci_earnings_basis,
                        'minorities deducted on an earnings basis, not at book'),):
    for c in ('A', 'B'):
        pass
    fair = dict(C.FAIR)
    for k, case in (('dcf_A', C.CASE['A']), ('dcf_B', C.CASE['B'])):
        eqv = (case['enterprise_value'] + C.V('jvinv_1h26') + C.V('cash_1h26')
               - C.V('debt_1h26') - C.V('lease_1h26') - v - C.V('finliab_1h26'))
        fair[k] = eqv / C.shares_out_k * C.V('fx_aed_usd')
    price(label, f'{desc} ({v/1e3:,.0f}m vs {C.V("nci_1h26")/1e3:,.0f}m book)', reweight(fair))

# ---------------------------------------------------------------- F. REGIONAL RAMP
# The average-deployed convention opens the regional fleet at ZERO for 2025 and
# averages to the 2026 year-end count, giving 15 rig-years. The rigs were
# actually consolidated in January and during the first half of 2026, and the
# 1H-2026 accounts already carry roughly 19 of them.
orig_fleet = C.FLEET['A']['regional'][2026], C.FLEET['B']['regional'][2026]
print('       (the model books 15.0 regional rig-years in 2026 against roughly 19 '
      'already consolidated in 1H-2026)')

# ---------------------------------------------------------------- G. FY26 MARGIN
g26_margin = rows[0]['ebitda'] / rows[0]['revenue']
lo = C.V('g26_ebitda_lo') / C.V('g26_revenue')
hi = C.V('g26_ebitda_hi') / C.V('g26_revenue')
print(f"\nG1    FY2026 built margin {g26_margin*100:.2f}% against guidance of "
      f"{lo*100:.0f}-{hi*100:.0f}% — ABOVE the guided range")

# ---------------------------------------------------------------- H. RELATIVE LENS
# The peer multiples are enterprise value over LAST TWELVE MONTHS EBITDA. They
# are applied to ADNOC Drilling's FORWARD guided EBITDA. Applying a trailing
# multiple to a forward number is a mismatch in the company's favour.
fair = dict(C.FAIR)
rel_ev = C.blended_multiple * C.H[2025]['ebitda']
rel_eq = (rel_ev + C.V('jvinv_1h26') + C.V('cash_1h26') - C.V('debt_1h26')
          - C.V('lease_1h26') - C.V('nci_1h26') - C.V('finliab_1h26'))
fair['relative'] = rel_eq / C.shares_out_k * C.V('fx_aed_usd')
price('H1', 'relative lens on trailing EBITDA, matching the trailing peer multiples',
      reweight(fair))

# ---------------------------------------------------------------- I. JV CASH
# Equity-accounted income is in forecast profit and therefore in forecast cash,
# but no joint-venture distribution is modelled. This does not touch enterprise
# value; it overstates the forecast cash balance.
jv_cum = sum(r['jv_share'] for r in rows)
print(f"\nI1    joint-venture income in forecast profit but never received as cash: "
      f"{jv_cum/1e3:,.0f}m cumulative to 2030 — overstates the forecast cash balance "
      f"({rows[-1]['cash_close']/1e3:,.0f}m), not enterprise value")

# ---------------------------------------------------------------- combined
C.WC_PCT_REVENUE = (orig_wc + wc_pct_1h26) / 2
C.WACC = C.ke_rating
cases = {c: C.build_case(c) for c in ('A', 'B')}
fair = dict(C.FAIR)
fair['dcf_A'] = cases['A']['value_per_share_aed']
fair['dcf_B'] = cases['B']['value_per_share_aed']
pb = (float(np.mean(roes)) - C.g_book) / (C.ke_rating - C.g_book)
fair['book'] = pb * C.book_equity_now / C.shares_out_k * C.V('fx_aed_usd')
ev = (C.norm_ebitda - dna_full) * (1 - C.V('tax_rate')) / (C.ke_rating - C.V('terminal_growth_B'))
eq = (ev + C.V('jvinv_1h26') + C.V('cash_1h26') - C.V('debt_1h26') - C.V('lease_1h26')
      - C.V('nci_1h26') - C.V('finliab_1h26'))
fair['normalised'] = eq / C.shares_out_k * C.V('fx_aed_usd')
price('ALL', 'every accepted correction applied together', reweight(fair))
C.WC_PCT_REVENUE, C.WACC = orig_wc, orig_wacc

json.dump(dict(base_central=BASE, spot=SPOT, findings=FINDINGS),
          open(os.path.join(HERE, 'self_audit.json'), 'w'), indent=1)
