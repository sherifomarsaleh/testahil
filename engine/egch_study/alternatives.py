"""EGCH — the contested constructions, each PRICED rather than described.

The model study publishes, for every choice in the build that a competent analyst could
legitimately make differently, what the answer would have been on the alternative. This
module produces that table. Every row is a full re-run of the model through
compute.run_case() with ONE component moved — never a hand-adjusted rate, never an
interpolation, never a description of a direction.

It also produces the bear-base-bull SPAN of each of the four lenses, so the valuation
summary can carry a range and a central for every read rather than a single point.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
sys.path.insert(0, HERE)

import compute as C                    # re-runs the model and rewrites study_numbers.json
from inputs import V

D = C.D
SPOT, SH = V('spot_price'), V('shares_outstanding')
BASELINE = C.CASES['base']['bridge']['per_share']
BASELINE_HALT = C.CASES['halt']['bridge']['per_share']


def reprice(case="base", glide=False, **patch):
    """Move one component, rebuild the rate structure if the component is a rate input,
    re-run the case end to end, then restore. Returns EGP per share."""
    saved = {k: D[k] for k in patch}
    saved_rates = (list(D['wacc_path']), D['wacc_terminal'], D['ke_terminal'],
                   list(D['rf_star_path']), list(D['kd_path']), D['rf_star_terminal'],
                   D['kd_local_equiv_terminal'])
    D.update(patch)
    if glide:
        C.set_glide()
    ps = C.run_case(case)['bridge']['per_share']
    D.update(saved)
    (D['wacc_path'], D['wacc_terminal'], D['ke_terminal'], D['rf_star_path'],
     D['kd_path'], D['rf_star_terminal'], D['kd_local_equiv_terminal']) = saved_rates
    return ps


# ---------------------------------------------------------------------------
# 1. THE CONTESTED CONSTRUCTIONS
# ---------------------------------------------------------------------------
W = C.WACC
flat_spot = reprice(wacc_path=[D['wacc_spot']] * 5, wacc_terminal=D['wacc_spot'])
cds_basis = reprice(glide=True, rf_star_spot=W['rf_star_cds'], erp=W['erp_cds'])
g_low = reprice(g_terminal=V('g_terminal_alt'))
beta_dimson = reprice(glide=True, beta=V('dimson_sum_beta'))
gas_contract = reprice(gas_usd_mmbtu=V('gas_contract_usd_mmbtu'))
util_bull = reprice(anna_util_base=V('anna_util_bull'))
capex_low = reprice(maint_capex_pct_rev=V('maint_capex_pct') * 2 / 3)

ALTS = [
    dict(key="premium_basis",
         made="Country risk priced off the sovereign's credit rating",
         alt="Priced off the sovereign's traded default swap instead, which is the "
             "narrower of the two spreads",
         value=cds_basis,
         why="The rating basis is the wider spread and therefore the more conservative "
             "equity premium. Both are published in full in section 1.8 and neither is "
             "ever mixed with the other's risk-free rate."),
    dict(key="glide",
         made="A cost of capital that glides from its spot build to a terminal rate made "
              "from its own long-run components",
         alt="One flat spot rate applied to every explicit year and to the perpetuity",
         value=flat_spot,
         why="A spot rate carries today's inflation print into a perpetuity growing at "
             "the central bank's target. That is a units mismatch, and on a company "
             "whose value sits in its terminal year it would be the largest single error "
             "in the study."),
    dict(key="terminal_growth",
         made=f"Terminal growth at the central bank's medium-term inflation target",
         alt="Two percentage points below it, which is negative real maintenance growth",
         value=g_low,
         why="Nominal maintenance growth with no real growth is the neutral assumption "
             "for a single plant at steady state. Below inflation implies the asset "
             "shrinks in real terms every year forever, which the maintenance capital "
             "expenditure in the model is sized to prevent."),
    dict(key="beta",
         made="Beta from the five-year weekly regression of the share against its own "
              "local index",
         alt="The Dimson sum-beta from the same regression, which corrects for co-movement "
             "booked late because the share does not trade every session",
         value=beta_dimson,
         why="The regression passes all three conditions of the usability test and the "
             "sum-beta sits inside its confidence interval, so the direct estimate is "
             "adopted and the correction is disclosed rather than substituted."),
    dict(key="gas",
         made="Gas at the realised price the company's own loss disclosure implies",
         alt="The contract formula price in the operating agreement, which is higher",
         value=gas_contract,
         why="The realised price is what the company actually paid on its own numbers. "
             "The contract price is carried as the downside case rather than as the "
             "central assumption, because a company that has been paying less than its "
             "contract for three years is evidence, not an exception."),
    dict(key="utilisation",
         made="The new complex earning at half its derived nameplate in the terminal year",
         alt="Seventy per cent, which is what a well-run nitrate line achieves",
         value=util_bull,
         why="Half is the observed record of the existing plant against its own plate "
             "under the same gas constraint. Assuming the new line does better than the "
             "old one on the same feedstock would need evidence no filing provides."),
    dict(key="maintenance_capex",
         made="Maintenance capital expenditure at three per cent of revenue",
         alt="Two per cent, nearer the company's own pre-project observed spend",
         value=capex_low,
         why="The observed pre-project run was abnormally low on a plant that had just "
             "been built. Three per cent is the mature-plant standard, and no guidance "
             "exists, which is why it is sensitised here rather than asserted."),
]
for a in ALTS:
    a['delta'] = a['value'] - BASELINE

# ---------------------------------------------------------------------------
# 2. THE SPAN OF EACH LENS — bear, base, bull
# ---------------------------------------------------------------------------
LN = json.load(open('lenses.json'))
B = C.CASES
SPANS = {
    "cashflow_carry": dict(
        label="Cash flow — programme carried through",
        basis="Five-year free cash flow to the firm on a cost of capital gliding from "
              f"{D['wacc_path'][0]*100:.1f}% to {D['wacc_terminal']*100:.1f}%, terminal "
              f"growth {D['g_terminal']*100:.1f}%",
        bear=B['bear']['bridge']['per_share'], base=B['base']['bridge']['per_share'],
        bull=B['bull']['bridge']['per_share']),
    "cashflow_stopped": dict(
        label="Cash flow — programme stopped",
        basis="The same model with the capital programme wound down in the first forecast "
              "year and the plant run as it stands",
        bear=reprice("halt", gas_usd_mmbtu=V('gas_contract_usd_mmbtu')),
        base=BASELINE_HALT,
        bull=reprice("halt", maint_capex_pct_rev=V('maint_capex_pct') * 2 / 3)),
    "book": dict(
        label="Book value and sustainable return",
        basis=f"Book equity of EGP {LN['book']['book_per_share']:.2f} a share at the "
              f"multiple a {LN['book']['roe_sustainable']*100:.1f}% sustainable return on "
              f"equity justifies against a {LN['book']['ke']*100:.1f}% cost of equity",
        bear=0.0, base=LN['book']['value_per_share'], bull=0.0),
    "relative": dict(
        label="Relative multiples",
        basis=f"Forward operating profit before depreciation at "
              f"{LN['relative']['mult_low']:.1f}x to {LN['relative']['mult_high']:.1f}x, "
              f"the Egyptian industrial range, with {LN['relative']['mult_mid']:.1f}x central",
        bear=LN['relative']['value_low'], base=LN['relative']['value_per_share'],
        bull=LN['relative']['value_high']),
    "normalised": dict(
        label="Normalised earnings power",
        basis=f"Mid-cycle profit after tax of EGP {LN['normalised']['nopat']:,.0f}m at "
              f"{LN['normalised']['mult_low']:.0f}x to {LN['normalised']['mult_high']:.0f}x, "
              f"{LN['normalised']['mult']:.0f}x central",
        bear=LN['normalised']['value_low'], base=LN['normalised']['value_per_share'],
        bull=LN['normalised']['value_high']),
}
for s in SPANS.values():
    s['low'], s['high'] = min(s['bear'], s['bull']), max(s['bear'], s['bull'])
    s['vs_spot'] = s['base'] / SPOT - 1

# ---------------------------------------------------------------------------
# 3. THE CAPITAL PROGRAMME, PRICED IN ITS OWN UNITS
# ---------------------------------------------------------------------------
prog = dict(
    approved_egp=V('anna_cost_egp'), approved_usd=V('anna_cost_usd'),
    approved_total=D['anna_total_cost'],
    spent=D['anna_spent'],
    spent_pct=D['anna_spent'] / D['anna_total_cost'],
    progress=V('anna_progress_sep2025'), plan=V('anna_plan_sep2025'),
    remaining=D['anna_total_cost'] - D['anna_spent'],
    nameplate=D['anna_nameplate_an_t'],
    capital_per_tonne=D['anna_total_cost'] * 1e6 / D['anna_nameplate_an_t'],
    market_cap=SPOT * SH / 1e6,
    pct_market_cap=D['anna_total_cost'] / (SPOT * SH / 1e6),
    terminal_ebit=C.CASES['base']['terminal']['anna_ebit'],
    terminal_util=D['anna_util_base'],
)
prog['return_on_cost'] = (prog['terminal_ebit'] * (1 - D['tax_rate'])) / prog['approved_total']
prog['gap_to_wacc'] = prog['return_on_cost'] - D['wacc_terminal']

# ---------------------------------------------------------------------------
# 4. THE ASSET-CONVERSION CYCLE — disclosed, then projected from it
# ---------------------------------------------------------------------------
cyc_hist = []
for tag, yr in [("FY2022/23", "FY2223"), ("FY2023/24", "FY2324"), ("FY2024/25", "FY2425")]:
    rev = V(f'is_revenue_{yr}')
    cogs = V(f'is_cogs_{yr}')
    rec, inv, pay = (V(f'bs_receivables_{yr}'), V(f'bs_inventory_{yr}'),
                     V(f'bs_payables_{yr}'))
    cyc_hist.append(dict(year=tag, dso=rec / rev * 365, dio=inv / cogs * 365,
                         dpo=pay / cogs * 365,
                         ccc=rec / rev * 365 + inv / cogs * 365 - pay / cogs * 365,
                         wc=rec + inv - pay, wc_pct_rev=(rec + inv - pay) / rev))
cyc_fwd = [dict(year=r['year'], wc=r['wc'], dwc=r['dwc'], wc_pct_rev=r['wc'] / r['revenue'])
           for r in C.CASES['base']['rows']]

OUT = dict(baseline=BASELINE, baseline_halt=BASELINE_HALT, spot=SPOT,
           alternatives=ALTS, spans=SPANS, programme=prog,
           cycle_hist=cyc_hist, cycle_fwd=cyc_fwd)
json.dump(OUT, open('alternatives.json', 'w'), indent=1, default=float)

print(f"baseline EGP {BASELINE:.2f} (carried through), EGP {BASELINE_HALT:.2f} (stopped)\n")
for a in ALTS:
    print(f"  {a['key']:18s} EGP {a['value']:6.2f}  delta {a['delta']:+6.2f}")
print()
for k, s in SPANS.items():
    print(f"  {k:18s} {s['low']:6.2f} .. {s['high']:6.2f}  base {s['base']:6.2f}  "
          f"vs spot {s['vs_spot']*100:+6.1f}%")
print(f"\nprogramme: approved EGP {prog['approved_total']:,.0f}m = "
      f"{prog['pct_market_cap']*100:.0f}% of market cap; spent {prog['spent_pct']*100:.1f}%; "
      f"return on cost {prog['return_on_cost']*100:.1f}% against a terminal cost of capital "
      f"of {D['wacc_terminal']*100:.1f}%")
print("wrote alternatives.json")
