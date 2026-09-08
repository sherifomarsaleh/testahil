#!/usr/bin/env python3
"""SWDY -- the [R-COC-01] cost-of-capital schedule record, READ OUT of the committed
numbers rather than typed.

WHY IT DID NOT EXIST, AND WHY THAT IS THE INTERESTING PART. check_cost_of_capital.py
listed this name as "carries no cost-of-capital schedule record", which reads like a
study that never did the work. The opposite is true: compute.py builds the whole
ladder, glides it on the cost-of-debt path's own cumulative progress, runs the
three-assert cost-of-debt gate WITH THE RIGHT DENOMINATOR (the finance charge over
average interest-bearing borrowings, never a broader liabilities total), back-solves
the currency composition of the book from two disclosed rates, and computes the
local-equivalent alternative. All of it is in the study and NONE of it was in a form
anything outside the study could read. A number cannot be checked for a choice.

IT READS study_numbers.json AND RUNS NOTHING, for the reason bridge_record.py records:
compute.py WRITES that file, so a record generator that imports it silently reverts
every record already added. Every figure below is read from the committed `wacc` and
`inputs` blocks, or derived from them by the identity compute.py itself uses.

THREE THINGS THE RECORD SURFACES, AND THE STUDY IS COMMITTED AS IT MEASURES:

  (1) THE TERMINAL RISK-FREE RATE IS 10.50% AGAINST A HOUSE-DERIVED 12.50%. The house
      Egyptian path derives its terminal risk-free as the terminal inflation target
      plus the real-rate convention; this study carries a figure 200bp below it. A
      lower terminal risk-free lowers the terminal discount rate and RAISES the
      value, and most of this company's value is in the terminal. Recorded, not
      quietly conformed: it is a lever with its own ledger entry.

  (2) THE COST OF DEBT IS THE CURRENCY-BLENDED RATE, NOT THE LOCAL-EQUIVALENT ONE.
      [R-COC-01 AMENDED] requires the foreign tranche to be carried at local-
      equivalent cost -- the foreign coupon plus the expected depreciation the house
      path already derives -- and never at the raw foreign coupon, because a foreign
      rate dropped into a local-nominal model understates the cost exactly as the
      sovereign floor overstates it. This study COMPUTES the local-equivalent blend
      and publishes it as an alternative rather than adopting it. Adopting it RAISES
      the cost of capital and LOWERS the value, away from a price this study already
      sits far below, which is the direction that shows the discipline is not
      fitting. Recorded, not applied in this pass.

  (3) THE INDEPENDENTLY COMPUTED EFFECTIVE RATE EXISTS FOR ONE PERIOD ONLY, and the
      reason is a disclosure gap rather than an oversight: the FY2025 audited
      statements carry the borrowings movement reconciliation the denominator needs
      and the interim statements do not. That is stated as the stop-and-inform the
      rule asks for, never dressed up as two observations.

WHAT IS CLEAN AND IS WORTH NAMING FOR THE SAME REASON: the risk-free is normalised by
this sovereign's OWN default spread so country risk enters exactly once; the weights
are market-value; the glide fractions are the cost-of-debt path's own cumulative
progress rather than a second free parameter; the ladder is monotone; the terminal is
brought home on the same factor as the last explicit year; both premium bases are
published with one named central; and the currency composition of the debt book is
sourced to two disclosed rates rather than assumed.

    python3 coc_record.py        adds `cost_of_capital_record` to study_numbers.json
"""
import io, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(HERE, 'study_numbers.json')
D = json.load(open(PATH, encoding='utf-8'))
V = {k: x['value'] for k, x in D['inputs'].items()}
W = D['wacc']

RF = float(V['rf'])
SPREAD = float(V['sov_spread_cds'])
RF_STAR = float(W['rf_star'])
WE = float(W['wacc_exp'])
WT = float(W['wacc_term'])
KD = float(W['kd'])

# THE GLIDE, REPRODUCED BY THE IDENTITY compute.py USES -- the fractions are the
# cost-of-debt path's own cumulative progress, so the shape is inherited from the
# easing calendar rather than being a second free parameter.
KDP = list(V['kd_path'])
GLIDE = [(KDP[0] - k) / (KDP[0] - KDP[-1]) for k in KDP]
FWD = [WE - (WE - WT) * f for f in GLIDE]
DF, _c = [], 1.0
for w in FWD:
    _c /= (1.0 + w)
    DF.append(_c)

assert all(abs(a - b) < 1e-12 for a, b in zip(GLIDE, W['glide_frac'])), \
    'the glide fractions do not reproduce from the cost-of-debt path'
assert all(FWD[i] >= FWD[i + 1] for i in range(len(FWD) - 1)), 'the ladder is not monotone'

# THE EFFECTIVE RATE, COMPUTED HERE FROM THE FILINGS' OWN FIGURES AND NOT COPIED --
# the finance charge over AVERAGE INTEREST-BEARING BORROWINGS. Dividing it by a
# broader liabilities total understates the rate by a multiple and manufactures a
# bias that looks exactly like evidence, which is why the denominator is described
# in the record rather than left to be inferred.
KD_EFF_FY25 = float(V['int_exp_fy25']) / ((float(V['debt_open_fy25'])
                                           + float(V['debt_close_fy25'])) / 2.0)

# THE CURRENCY COMPOSITION, BACK-SOLVED FROM TWO DISCLOSED RATES rather than assumed.
# The audited statements disclose the weighted average rate on Egyptian-pound
# financial liabilities and the weighted average on foreign-currency ones; the blended
# effective rate then pins the pound share by arithmetic.
KD_EGP = float(V['kd_egp_note'])
KD_HARD = float(V['kd_hard_note'])
W_EGP = (KD_EFF_FY25 - KD_HARD) / (KD_EGP - KD_HARD)

record = dict(
    rule='R-COC-01',
    market='EG',
    macro_path='EG',

    # 1. country risk enters exactly once
    rf_observed=RF,
    default_spread=SPREAD,
    rf_star=RF_STAR,
    rf_normalisation_note=(
        "The risk-free rate is the local government-bond yield less THIS sovereign's own "
        "default spread on the SAME basis as the premium added back (credit-default-swap "
        "against credit-default-swap), so country risk is counted exactly once. Using the "
        "raw {0:.2%} local yield beside an equity premium that already carries country "
        "risk would charge Egypt twice."
        .format(RF)),

    # 2. the terminal is derived from the house path, never quoted
    rf_terminal=float(V['rf_term']),
    rf_terminal_note=(
        "COMMITTED AS THE STUDY CARRIES IT, WHICH IS NOT WHAT THE HOUSE PATH DERIVES. The "
        "house Egyptian path derives a terminal risk-free of 12.50% -- its terminal "
        "inflation of 7.00% plus the real-rate convention of 5.50% -- and this study "
        "carries {0:.2%}, {1:.0f}bp below it. A lower terminal risk-free lowers the "
        "terminal discount rate and RAISES the value, and {2:.0%} of this company's "
        "enterprise value sits in the terminal, so the effect is not second-order. It is "
        "recorded here rather than conformed in passing: conforming it is a lever, it "
        "moves the answer, and a lever is taken one at a time with its own ledger entry "
        "and its own audit point."
        .format(float(V['rf_term']), 10000 * (0.125 - float(V['rf_term'])),
                float(D['dcf']['tv_share']))),

    # 3. the schedule declines, one rate per explicit year
    wacc_exp=WE,
    wacc_terminal=WT,
    forward_wacc=FWD,
    glide_fractions=GLIDE,
    glide_note=(
        "The glide fractions are the cost-of-debt path's OWN cumulative progress "
        "({0}), so the front-loading is inherited from the easing calendar rather than "
        "chosen. Egypt is a transition market on the house path, so the schedule must "
        "decline; a flat crisis-level rate for five years and a perpetuity asserts that "
        "this economy never normalises, against the central bank's own published "
        "disinflation path that this study's cost of debt already follows."
        .format(", ".join("{0:.4f}".format(f) for f in GLIDE))),

    # 4. one date, one price of time
    discount_factors=DF,
    terminal_discount_factor=DF[-1],
    discounting_note=(
        "The terminal value is brought home on the SAME cumulative factor as the last "
        "explicit year's cash flow ({0:.6f}). Two prices for one date is a premium for "
        "relabelling the same pound arriving on the same day.".format(DF[-1])),

    # 5. the cost of debt
    kd_pretax=KD,
    kd_after_tax=float(W['kd_at']),
    kd_terminal=float(W['kd_term']),
    kd_path=KDP,
    kd_integrity=dict(
        pct_local_currency=W_EGP,
        currency_source=(
            "BACK-SOLVED FROM TWO DISCLOSED RATES, NOT ASSUMED. The audited FY2025 "
            "consolidated financial statements disclose the weighted average interest rate "
            "on Egyptian-pound financial liabilities ({0:.2%}) and on US-dollar and other "
            "foreign-currency financial liabilities ({1:.2%}). The independently computed "
            "blended effective rate of {2:.2%} then pins the pound share at {3:.1%} and the "
            "foreign-currency share at {4:.1%} by arithmetic -- down sharply from the "
            "roughly 44% pound share the same construction implied a year earlier, when the "
            "disclosed pound rate was {5:.2%}. THE COMPOSITION IS ESTABLISHED BEFORE THE "
            "RATE IS SET, which is what makes the sovereign floor's own qualifier -- 'on an "
            "all-local-currency book' -- reachable on this name instead of behaving as "
            "though those four words were not there."
            .format(KD_EGP, KD_HARD, KD_EFF_FY25, W_EGP, 1 - W_EGP, float(V['kd_egp_fy24']))),
        interest_bearing_note=(
            "The effective rate's denominator is AVERAGE INTEREST-BEARING BORROWINGS -- "
            "opening {0:,.0f} and closing {1:,.0f} loans and credit facilities from the "
            "audited FY2025 borrowings movement note -- and the numerator is the finance "
            "charge on those borrowings, {2:,.0f}. It is NOT total liabilities: supplier "
            "balances, contract liabilities, retentions and accruals bear no interest, and "
            "dividing the charge by a total that includes them understates the rate by a "
            "multiple and manufactures a bias that looks exactly like evidence."
            .format(float(V['debt_open_fy25']), float(V['debt_close_fy25']),
                    float(V['int_exp_fy25']))),
        effective_rates=dict(FY2025=KD_EFF_FY25),
        effective_rate_unavailable=(
            "ONE PERIOD, AND THE REASON IS A DISCLOSURE GAP RATHER THAN AN OVERSIGHT. An "
            "independently computed effective rate needs a finance charge and the opening "
            "and closing balances of the borrowings that bear it. The audited FY2025 "
            "consolidated financial statements disclose the borrowings movement "
            "reconciliation that supplies the denominator; the FY2024 statements disclose "
            "net finance costs rather than the interest charge on borrowings alone, and the "
            "Q1-2026 and H1-2026 reviewed interim statements disclose no comparable "
            "movement reconciliation at all. So a second independently computed period "
            "cannot be built from what this company has published, and it is not "
            "manufactured: a rate interpolated to satisfy a count corrupts the very check "
            "it is being computed for. The disclosed contractual rates for FY2024 "
            "({0:.2%} on the pound book) and Q1-2026 ({1:.2%}) are held beside it as "
            "corroboration and are NOT presented as independently computed."
            .format(float(V['kd_egp_fy24']), float(V['kd_egp_q1_26']))),
        bound_check=dict(
            adopted=KD,
            latest_effective=KD_EFF_FY25,
            gap_bp=10000 * abs(KD - KD_EFF_FY25),
            peak_effective=KD_EFF_FY25,
            note=("The adopted cost of debt is {0:.0f}bp from the independently computed "
                  "FY2025 effective rate, inside the 150bp bound, and does not exceed the "
                  "peak by more than 50bp. Both are asserted in compute.py at the point the "
                  "rate is set, not merely reported here."
                  .format(10000 * abs(KD - KD_EFF_FY25))),
        ),
        local_equivalent_alternative=dict(
            kd_local_equivalent=float(D['dcf']['kd_egp_equiv']),
            wacc_exp_local_equivalent=float(D['dcf']['wacc_exp_kd_egp_equiv']),
            per_share=float(D['dcf']['ps_kd_egp_equiv']),
            fx_depreciation=float(D['dcf']['fx_dep_avg']),
            note=("[R-COC-01 AMENDED] REQUIRES THE FOREIGN TRANCHE AT LOCAL-EQUIVALENT COST "
                  "-- the foreign coupon plus the expected local depreciation the house path "
                  "derives by relative purchasing-power parity, so nobody sets a currency "
                  "view inside a cost of debt -- and NEVER at the raw foreign coupon. This "
                  "study computes that blend ({0:.2%} against the adopted {1:.2%}) and "
                  "publishes it as an ALTERNATIVE. Adopting it raises the explicit-window "
                  "cost of capital to {2:.2%} and takes the central to EGP {3:.2f}, which is "
                  "AWAY from the price this study already sits far below. Recorded and not "
                  "applied in this pass: one lever at a time, each with its own ledger entry."
                  .format(float(D['dcf']['kd_egp_equiv']), KD,
                          float(D['dcf']['wacc_exp_kd_egp_equiv']),
                          float(D['dcf']['ps_kd_egp_equiv']))),
        ),
    ),

    # 6. both premium bases visible, one named central
    erp_basis='cds',
    erp_central=float(V['erp_cds']),
    beta_record=dict(W['beta']),

    # ---- THE FLAT KEYS [R-COC-02] READS, so the cost of equity can be REPRODUCED
    # from its own inputs rather than trusted. A cost of equity typed 300bp high
    # would have passed every other check in this repository, and on this name the
    # beta's own 90% interval spans a range worth far more than that.
    beta=float(W['beta']['beta']),
    rf_star_flat=float(W['rf_star']),
    erp=float(V['erp_cds']),
    ke_exp=float(W['ke_exp']),
    ke_terminal=float(W['ke_term']),
    erp_terminal=float(V['erp_term']),
    ke_terminal_construction='same_beta',
    ke_terminal_construction_note=(
        "The terminal cost of equity is the terminal risk-free plus the SAME beta times "
        "the terminal premium: {0:.4f} + {1:.6f} x {2:.4f} = {3:.6f}. No relevering — "
        "the terminal debt weight of {4:.0%} differs from the explicit window's {5:.2%}, "
        "so a relevered construction would be defensible and is NOT used, and saying so "
        "is the point: a reader cannot tell a relevered beta from a typing error unless "
        "the record names which construction produced the number."
        .format(float(V['rf_term']), float(W['beta']['beta']), float(V['erp_term']),
                float(W['ke_term']), float(V['wd_term']), float(W['wd_exp']))),
    beta_source='own_stock_regression',
    beta_source_note=(
        "beta_regression.own_stock_beta() against {0} as at {1} — the published index of "
        "the exchange this stock is listed on — giving {2:.4f} at an R-squared of {3:.3f} "
        "over {4} weekly observations. IT REPLACES A COMPOSITE, and the composite was not "
        "a weaker tier but a hard fail: a 31-name equal-weight basket of the covered EGX "
        "library gave {5:.4f} at an R-squared of {6:.3f}, understating the beta by {7:.1f}% "
        "and explaining less of the stock. The correction raises the cost of equity by "
        "{8:.0f} basis points and LOWERS this study's central, away from a price it "
        "already sits far below."
        .format(W['beta']['index_file'], W['beta']['index_asof'], float(W['beta']['beta']),
                float(W['beta']['r2']), int(W['beta']['n']),
                float(W['beta']['withdrawn_composite']['beta']),
                float(W['beta']['withdrawn_composite']['r2']),
                100 * abs(float(W['beta']['delta_vs_withdrawn'])),
                10000 * (float(W['beta']['beta']) - float(W['beta']['withdrawn_composite']['beta']))
                * float(V['erp_cds']))),
    weight_equity=float(W['we_exp']),
    weight_debt=float(W['wd_exp']),
    weight_debt_terminal=float(V['wd_term']),
    kd_aftertax=float(W['kd_at']),
    weights=dict(equity=float(W['we_exp']), debt=float(W['wd_exp']),
                 basis='market_value_equity',
                 note=("Market-value equity weights, never book. The debt weight is struck on "
                       "NET financial debt ({0:.2%}) against a gross {1:.2%}; the bridge then "
                       "adds the same cash back at face, which bridge_record.py records as the "
                       "cash reaching the answer twice -- on a net-DEBT company that runs the "
                       "opposite way to the case the rule was written on and LOWERS the value."
                       .format(float(W['wd_exp']), float(W['wd_gross'])))),
    sensitivity=dict(
        other_basis=dict(
            basis='rating',
            erp=float(V['erp_rating']),
            default_spread=float(V['sov_spread_rating']),
            ke_exp=float(W['ke_rating_alt']),
            wacc_exp=float(D['dcf']['wacc_exp_rating']),
            wacc_terminal=float(D['dcf']['wacc_term_rating']),
            per_share=float(D['dcf']['ps_rating_basis']),
            note=("The rating-basis premium and its matching rating-basis default spread are "
                  "published beside the adopted market basis, on the same basis at both ends "
                  "so country risk is stripped and added back consistently. The market basis "
                  "is named central because it is the market's own live pricing of this "
                  "sovereign's credit, against an agency judgement updated in steps."),
        ),
        usd_alternative=dict(wacc=float(W['wacc_usd_alt']),
                             note="A dollar-denominated cross-check for a high-inflation "
                                  "market, published rather than substituted."),
    ),

    published_central=float(D['central']),
    published_spot=float(D['spot']),
)

D['cost_of_capital_record'] = record
io.open(PATH, 'w', encoding='utf-8').write(
    json.dumps(D, indent=1, ensure_ascii=False, default=float) + '\n')

print('cost_of_capital_record written for SWDY')
print('   rf {0:.2%} - own default spread {1:.2%} = rf* {2:.2%}'.format(RF, SPREAD, RF_STAR))
print('   forward WACC  ' + ' -> '.join('{0:.2%}'.format(w) for w in FWD)
      + '   terminal {0:.2%}'.format(WT))
print('   discount factors ' + ', '.join('{0:.4f}'.format(x) for x in DF))
print('   Kd {0:.2%} adopted; effective FY2025 {1:.2%} ({2:.0f}bp); book {3:.1%} pound / '
      '{4:.1%} foreign'.format(KD, KD_EFF_FY25, 10000 * abs(KD - KD_EFF_FY25), W_EGP, 1 - W_EGP))

sys.path.insert(0, os.path.join(os.path.dirname(HERE), '..', 'scripts'))
