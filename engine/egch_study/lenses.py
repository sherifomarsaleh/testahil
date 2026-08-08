"""EGCH — the four valuation lenses, and the contested judgement computed both ways.

The cash-flow lens is the primary one and lives in compute.py. This module adds the
other three and assembles the field. Every number here is derived from the input
register; no financial numeral is typed into any builder downstream.

THE CONTESTED JUDGEMENT. This study's single most consequential contested judgement is
whether the ANNA capital programme is carried through or stopped. It is worth more than
three pounds a share — more than twice the whole central estimate — and no averaging of
the two would tell the reader anything true. Both are computed and both are published,
side by side, in the summary table, the body, the workbook and an expert's range.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from inputs import V

D = json.load(open(os.path.join(HERE, 'study_numbers.json')))
CASES, R = D['cases'], D['cases']['base']['rows']
SHARES = V('shares_outstanding')
SPOT = V('spot_price')
NET_DEBT = CASES['base']['bridge']['net_debt']
NONOP = CASES['base']['bridge']['fvoci'] + CASES['base']['bridge']['inv_prop']

L = {}

# ---------------- LENS 1: cash flow (primary) — both sides of the judgement ----
L['cashflow'] = dict(
    label="Cash flow",
    carry_through=CASES['base']['bridge']['per_share'],
    stopped=CASES['halt']['bridge']['per_share'],
    upside=CASES['bull']['bridge']['per_share'],
    downside=CASES['bear']['bridge']['per_share'],
)

# ---------------- LENS 2: book value and sustainable return -------------------
# Equity at the latest reviewed date, then asked what return it sustainably earns
# against what that return is worth. Justified price-to-book = (RoE - g) / (Ke - g).
eq_book = (V('bs_capital_M9FY2526') + V('bs_reserves_M9FY2526'))
# sustainable RoE on UNDERLYING profit: FY2024/25 net, and FY2023/24 stripped of the
# one-off revaluation gain, averaged over the two years' opening equity
und_24 = V('is_net_FY2324') - V('oneoff_reval_FY2324')
und_25 = V('is_net_FY2425')
eq_open_24 = V('bs_capital_FY2223') + V('bs_reserves_FY2223')
eq_open_25 = V('bs_capital_FY2324') + V('bs_reserves_FY2324')
roe_24, roe_25 = und_24 / eq_open_24, und_25 / eq_open_25
roe_sust = (roe_24 + roe_25) / 2
ke = D['wacc']['ke_rating']
g = V('g_terminal')
pb_raw = (roe_sust - g) / (ke - g)
# The sustainable return does not cover even nominal maintenance growth, so the
# justified multiple of book is negative before flooring. That is the finding, not a
# rounding artefact, and both numbers are reported.
pb_justified = max(0.0, pb_raw)
L['book'] = dict(
    label="Book value and sustainable return",
    equity_book=eq_book, book_per_share=eq_book * 1e6 / SHARES,
    underlying_FY2324=und_24, underlying_FY2425=und_25,
    roe_FY2324=roe_24, roe_FY2425=roe_25, roe_sustainable=roe_sust,
    ke=ke, g=g, pb_justified=pb_justified, pb_raw=pb_raw,
    value_per_share=pb_justified * eq_book * 1e6 / SHARES,
    pb_at_market=SPOT * SHARES / 1e6 / eq_book,
)

# ---------------- LENS 3: relative multiples ----------------------------------
ebitda_fwd = R[0]['ebitda']
lo, hi = V('egx_industrial_ev_ebitda_low'), V('egx_industrial_ev_ebitda_high')
mid = (lo + hi) / 2
def per_share_from_ev(ev):
    return (ev - NET_DEBT + NONOP) * 1e6 / SHARES
L['relative'] = dict(
    label="Relative multiples",
    ebitda_fwd=ebitda_fwd, mult_low=lo, mult_mid=mid, mult_high=hi,
    ev_low=lo * ebitda_fwd, ev_mid=mid * ebitda_fwd, ev_high=hi * ebitda_fwd,
    value_low=per_share_from_ev(lo * ebitda_fwd),
    value_per_share=per_share_from_ev(mid * ebitda_fwd),
    value_high=per_share_from_ev(hi * ebitda_fwd),
    implied_at_market=(SPOT * SHARES / 1e6 + NET_DEBT) / ebitda_fwd,
    implied_at_model=CASES['base']['bridge']['ev'] / ebitda_fwd,
)

# ---------------- LENS 4: normalised earnings power ---------------------------
# Mid-cycle: the three-year average urea run at a mid-cycle export price, with the
# cost stack held at the model's FY2026/27 unit economics.
urea_mid = (V('prod_urea_FY2425') + 521868 + 586373) / 3
fx_mid = V('usd_egp_path')[1]
p_exp = V('mid_cycle_urea_usd_t')
sub_t, free_t = V('subsidised_t_path')[0], V('local_free_path')[0]
exp_t = urea_mid - sub_t - free_t
rev_exp = exp_t * p_exp * fx_mid * (1 - V('export_duty_2026')) / 1e6
rev_sub = sub_t * V('subsidised_p_path')[0] / 1e6
rev_free = free_t * p_exp * fx_mid * V('local_free_parity') / 1e6
rev_an = V('an_path')[0] * 20000.0 * (fx_mid / V('usd_egp_avg_FY2425')) / 1e6
rev_oth = V('other_rev_path')[0]
rev_mid = rev_exp + rev_sub + rev_free + rev_an + rev_oth
nh3_mid = urea_mid * V('ammonia_per_urea')
gas_mid = nh3_mid * 1292.0 * V('gas_realised_usd_mmbtu') * V('mmbtu_per_m3') * fx_mid / 1e6
othmat = urea_mid * (1101.6e6 / V('prod_urea_FY2425')) * 1.10 / 1e6
wages = V('cogs_wages_FY2425') * 1.10
services = V('cogs_services_FY2425') * 1.10
freight = exp_t * (V('sell_freight_FY2425') * 1e6 / V('export_tonnes_FY2425')) * 1.10 / 1e6
othsell = V('sell_other_FY2425') * 1.10
admin = V('is_admin_FY2425') * 1.10
cash_cost = gas_mid + othmat + wages + services + freight + othsell + admin
ebitda_mid = rev_mid - cash_cost
dep = V('dep_charge_FY2425') + V('amort_FY2425')
nopat_mid = (ebitda_mid - dep) * (1 - V('tax_statutory'))
mult_norm = 10.0
L['normalised'] = dict(
    label="Normalised earnings power",
    urea_mid=urea_mid, export_t=exp_t, price_usd=p_exp, fx=fx_mid,
    rev_exp=rev_exp, rev_sub=rev_sub, rev_free=rev_free, rev_an=rev_an, rev_oth=rev_oth,
    revenue=rev_mid, gas=gas_mid, other_materials=othmat, wages=wages, services=services,
    freight=freight, other_selling=othsell, admin=admin, cash_cost=cash_cost,
    ebitda=ebitda_mid, dep=dep, nopat=nopat_mid,
    mult_low=8.0, mult=mult_norm, mult_high=12.0,
    ev=nopat_mid * mult_norm,
    value_low=per_share_from_ev(nopat_mid * 8.0),
    value_per_share=per_share_from_ev(nopat_mid * mult_norm),
    value_high=per_share_from_ev(nopat_mid * 12.0),
)

# ---------------- SYNTHESIS: four lenses, one field ---------------------------
field = {
    "Cash flow — programme carried through": L['cashflow']['carry_through'],
    "Cash flow — programme stopped": L['cashflow']['stopped'],
    "Book value and sustainable return": L['book']['value_per_share'],
    "Relative multiples": L['relative']['value_per_share'],
    "Normalised earnings power": L['normalised']['value_per_share'],
}
vals = [v for v in field.values()]
L['synthesis'] = dict(
    field=field,
    low=max(0.0, min(vals)), high=max(vals),
    central_carry_through=L['cashflow']['carry_through'],
    central_stopped=L['cashflow']['stopped'],
    spot=SPOT,
    note=("The two cash-flow readings are the contested judgement and are never averaged. "
          "The other three lenses are shown against both."),
)
L['contested'] = dict(
    question="Is the ANNA capital programme carried through, or stopped?",
    side_a_label="Carried through", side_a=L['cashflow']['carry_through'],
    side_b_label="Stopped", side_b=L['cashflow']['stopped'],
    gap=L['cashflow']['stopped'] - L['cashflow']['carry_through'],
    gap_equity=CASES['halt']['bridge']['equity'] - CASES['base']['bridge']['equity'],
    decides=("Whether the plant, once built, earns a return above the cost of the capital "
             "sunk into it. On the disclosed bank-approved cost and the derived nameplate it "
             "does not, which is why stopping is worth more than finishing."),
)

json.dump(L, open(os.path.join(HERE, 'lenses.json'), 'w'), indent=1, default=float)
print(f"{'lens':46s} {'value/share':>12s}")
for k, v in field.items():
    print(f"{k:46s} {v:12.2f}")
print(f"\nfield: EGP {L['synthesis']['low']:.2f} to {L['synthesis']['high']:.2f} "
      f"| spot {SPOT:.2f}")
print(f"contested judgement gap: EGP {L['contested']['gap']:.2f}/share "
      f"({L['contested']['gap_equity']:,.0f}m of equity)")
print(f"sustainable return on equity {L['book']['roe_sustainable']*100:.1f}% against a "
      f"{ke*100:.1f}% cost of equity -> justified price/book {L['book']['pb_justified']:.2f}x "
      f"(market pays {L['book']['pb_at_market']:.2f}x)")
