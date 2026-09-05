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
# THE ALTERNATIVE RE-RAN THE BASE CASE AND SCORED +0.00 BY CONSTRUCTION. This priced the
# CDS basis as the alternative, and the study's base case ALREADY uses the CDS basis:
# rf_star_spot is rf_star_cds and the published cost of capital is wacc_cds. So the first
# row of the contested-constructions table — the table whose entire purpose is to show what
# each choice is worth — moved nothing, and reported that as a finding. A zero delta reads
# as "this choice does not matter", which is the one answer nobody checks.
#
# The labels were reversed with it: the study CHOOSES the swap basis and the ALTERNATIVE is
# the rating basis, not the other way round.
rating_basis = reprice(glide=True, rf_star_spot=W['rf_star_rating'], erp=W['erp_rating'])
g_low = reprice(g_terminal=V('g_terminal_alt'))
beta_low = reprice(glide=True, beta=V('beta_ci90_low'))
gas_contract = reprice(gas_usd_mmbtu=V('gas_contract_usd_mmbtu'))
util_bull = reprice(anna_util_base=V('anna_util_bull'))
capex_replacement = reprice(maint_capex_pct_rev=V('maint_capex_pct_replacement'))
capex_house = reprice(maint_capex_pct_rev=0.030)          # the superseded house standard
age_assumed = reprice(terminal_force_half_life=True)
kd_floored = reprice(glide=True, kd_floor=W['sovereign_floor'])
project_faster = reprice(anna_capex_path=[3000.0, 3500.0, 3500.0, 3000.0, 2000.0])

ALTS = [
    dict(key="premium_basis",
         made="Country risk priced off the sovereign's traded default swap",
         alt="Priced off the sovereign's credit rating instead, which is the wider of "
             "the two spreads and gives a cost of capital %d basis points higher"
             % round((W['wacc_rating'] - W['wacc_cds']) * 1e4),
         value=rating_basis,
         why="The swap basis is the market's own live pricing of this sovereign's credit, "
             "against a rating judgement updated in steps. It is the NARROWER spread, so "
             "this is not the conservative choice and is not made on that ground; the "
             "rating basis is priced here rather than argued about. Both are published in "
             "full in section 1.8 and neither is ever mixed with the other's risk-free "
             "rate."),
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
    dict(key="cost_of_debt_floor",
         made=(f"The cost of debt at the company's own disclosed rates — {W['kd_local']*100:.1f}% on the "
               f"local facility, {W['kd_usd_nominal']*100:.1f}% in dollars on the project loan carried at "
               f"local-equivalent cost on the derived currency path, {W['kd_fx_path'][0]*100:.1f}% in year "
               f"one gliding to {D['kd_local_equiv_terminal']*100:.1f}% at the terminal"),
         alt=(f"Every leg floored at the {W['sovereign_floor']*100:.2f}% sovereign ten-year yield — the "
              f"company's own facilities print no spread above the policy rate, so no spread is added"),
         value=kd_floored,
         why=(f"A same-currency corporate cannot normally borrow below its sovereign, and the local "
              f"facility does (its dollar leg sits below the normalised risk-free rate in "
              f"{len(W['years_fx_leg_below_rf_star'])} of the five explicit years). The disclosed rates are "
              f"what the company actually pays on state-bank facilities and are used as disclosed; the "
              f"floored construction is published beside them, not averaged in.")),
    dict(key="beta",
         made="Beta from the five-year weekly regression of the share against the published "
              "EGX30 index",
         alt="The lower bound of that regression's own 90% confidence interval",
         value=beta_low,
         why="The regression passes all three conditions of the usability test, so the point "
             "estimate is adopted; the interval is wide because the share is thinly traded, "
             "and the lower bound is priced here rather than argued away."),
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
         made="Maintenance capital expenditure at the company's own observed pre-project "
              "rate of 1.12% of revenue",
         alt="Replacement-rate maintenance: gross fixed assets at the disclosed 3.95% "
             "machinery depreciation rate, or 6.11% of revenue",
         value=capex_replacement,
         why="The observed rate is what this company has actually paid to keep this plant "
             "running in the two years when it was not building anything. The "
             "replacement-rate framing is the honest upper bound — a plant cannot spend a "
             "fifth of its depreciation forever — and it is carried as the downside case "
             "rather than averaged into the central."),
    dict(key="terminal_asset_age",
         made="Capital maintenance charged at what replacing the plant costs today, on "
              f"the {V('fa_avg_age_years'):.2f}-year average age the accounts MEASURE — "
              "accumulated depreciation over the year's own charge",
         alt=f"Half the {V('fa_life_implied_years'):.1f}-year life the same accounts "
             f"imply, {V('fa_life_implied_years') / 2:.2f} years, which is what has to be "
             "assumed where a company does not disclose enough to measure it",
         value=age_assumed,
         why="This is the largest single contested number in the study and it is a "
             "question about THIS BASE rather than about method. Half the life is the "
             "right assumption for a plant in steady state, where the average asset is "
             "half worn out. This one is not: only 1.3% of the base is fully depreciated "
             "and still in production, and a second complex is still being built, so the "
             "measured age is a quarter of the life rather than half. The measured figure "
             "is adopted BECAUSE it is measured, and the assumed one is published beside "
             "it so a reader can see what the disclosure is worth. THIS ROW REPLACED THE "
             "TERMINAL REINVESTMENT ROW, which priced a return on capital that no longer "
             "enters the terminal at all: under the sanctioned construction there is no "
             "reinvestment rate to contest, and this module's own gate caught the dead "
             "alternative the moment it scored zero."),
    dict(key="project_profile",
         made="Project spending anchored on the observed run rate: the nine-month actual "
              "extended to a full year",
         alt="The faster profile the first issue of this study used, opening at EGP 3,000m",
         value=project_faster,
         why="The company has never spent EGP 3,000m in a year on this project. The "
             "observed rate is a disclosed, dated figure and the total still completes the "
             "approved cost inside the forecast window."),
]
for a in ALTS:
    a['delta'] = a['value'] - BASELINE
    # AN ALTERNATIVE THAT MOVES NOTHING HAS NOT BEEN PRICED, IT HAS BEEN RE-RUN. The
    # premium-basis row scored exactly +0.00 for a full edition because it repriced the
    # basis the base case already uses; a zero delta reads as "this choice does not
    # matter", which is the one answer nobody checks. Priced correctly it was worth
    # -1.05 a share, the third largest of the ten. Exact zero is the signature, because
    # a genuine coincidence to the fifth decimal does not happen across a whole model.
    assert abs(a['delta']) > 1e-6, (
        "alternative %r scored exactly zero: it re-ran the base case rather than moving "
        "anything. Check that the value being patched in is not the one already in use."
        % a['key'])

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

# ---------------------------------------------------------------------------
# 5. WHAT THE COMPANY ACTUALLY SPENDS — the capex record, from the cash-flow
#    statements. Two clean pre-project years, then the build.
# ---------------------------------------------------------------------------
CAPEX_HIST = []
for tag, ck, rk, note in [
        ("FY2021/22", 'capex_paid_FY2122', 'is_revenue_FY2122', "Before the project"),
        ("FY2022/23", 'capex_paid_FY2223', 'is_revenue_FY2223', "Before the project"),
        ("FY2023/24", 'capex_paid_FY2324', 'is_revenue_FY2324', "The build begins"),
        ("FY2024/25", 'capex_paid_FY2425', 'is_revenue_FY2425', "Building"),
]:
    CAPEX_HIST.append(dict(year=tag, capex=V(ck), revenue=V(rk),
                           pct=V(ck) / V(rk), note=note))
CAPEX_HIST.append(dict(year="9M FY2025/26", capex=V('capex_paid_9M_FY2526'),
                       revenue=V('is_revenue_9M'),
                       pct=V('capex_paid_9M_FY2526') / V('is_revenue_9M'),
                       note="Nine months actual; a full year at this rate is EGP "
                            f"{V('capex_run_rate_FY2526E'):,.0f}m"))
capex_block = dict(history=CAPEX_HIST,
                   pre_project_pooled=V('maint_capex_pct'),
                   replacement_rate=V('maint_capex_pct_replacement'),
                   house_standard=0.030,
                   house_standard_value=capex_house,
                   run_rate=V('capex_run_rate_FY2526E'),
                   forecast_path=D['anna_capex_path'],
                   forecast_total=sum(D['anna_capex_path']),
                   remaining=D['anna_total_cost'] - D['anna_spent'],
                   machinery_dep_rate=V('dep_rate_kima2_machinery'),
                   implied_asset_life=1 / V('dep_rate_kima2_machinery'))

OUT = dict(baseline=BASELINE, capex=capex_block, baseline_halt=BASELINE_HALT, spot=SPOT,
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
print("\ncapex record (EGP m):")
for r in CAPEX_HIST:
    print(f"  {r['year']:14s} {r['capex']:10,.1f}  {r['pct']*100:6.2f}% of revenue   {r['note']}")
print(f"  pre-project pooled maintenance {V('maint_capex_pct')*100:.2f}% of revenue; "
      f"replacement rate {V('maint_capex_pct_replacement')*100:.2f}%; "
      f"superseded house standard 3.00% would give EGP {capex_house:.2f}")
print(f"\nprogramme: approved EGP {prog['approved_total']:,.0f}m = "
      f"{prog['pct_market_cap']*100:.0f}% of market cap; spent {prog['spent_pct']*100:.1f}%; "
      f"return on cost {prog['return_on_cost']*100:.1f}% against a terminal cost of capital "
      f"of {D['wacc_terminal']*100:.1f}%")
print("wrote alternatives.json")
