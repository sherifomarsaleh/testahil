#!/usr/bin/env python3
"""EGCH -- the [R-COC-01] cost-of-capital schedule record, READ OUT of the committed
numbers rather than typed.

WHY IT DID NOT EXIST. check_cost_of_capital listed this name as "carries no
cost-of-capital schedule record", which reads like a study that discounts everything
at one crisis-level rate. It does not: compute.py glides the risk-free rate to the
central bank's own terminal target, rebuilds the whole cost of capital at every
explicit year through the shared builder, and compounds the per-year rates into the
discount factors -- and the terminal is brought home on the SAME factor as the last
explicit year's cash flow. All of it was in the study and none of it in a form
anything outside the study could read.

WHAT THIS RECORD SHOWS, AND MOST OF IT IS THE STUDY BEING RIGHT:

  - country risk enters exactly ONCE: the risk-free is normalised by this sovereign's
    own credit-default-swap spread and the premium added back is on the same basis,
    with the rating basis published beside it as the alternative and the 113 basis
    points between them stated.

  - the terminal risk-free is 12.50%, which is what the house Egyptian path DERIVES
    from its terminal inflation and its real-rate convention. It is not quoted and it
    is not reverse-engineered from a price.

  - THE DEBT BOOK IS 99.7% FOREIGN-CURRENCY AND IS CARRIED AT LOCAL-EQUIVALENT COST.
    That is what [R-COC-01 AMENDED] requires and what most of this book does not yet
    do: the dollar coupon plus the expected pound depreciation the house path derives
    by purchasing-power parity, never the raw foreign coupon. It is why the adopted
    cost of debt of 24.34% sits ABOVE the 23.00% sovereign rather than below it.

  - the one local-currency facility carries a disclosed 19.40% against that 23.00%
    sovereign -- a corporate borrowing below its own government, which the rule
    normally refuses. It is used AS DISCLOSED and it is 0.31% of the book, so it moves
    the blended rate by six basis points. The disclosure is carried rather than
    smoothed away.

ONE THING THE RECORD CANNOT DO, STATED RATHER THAN DRESSED UP. An independently
computed effective rate needs a finance charge and the balances that bear it, and only
ONE fiscal year in this study's register carries both. So the 150bp bound cannot be
run over two periods, the limitation is declared, and the gate prints it. THE DEEPER
REASON IS WORTH RECORDING TOO, BECAUSE IT IS NOT ON ANYBODY'S LIST: a trailing expensed
charge on a foreign-currency book is measured in pounds at the rates that actually
prevailed, and the adopted rate carries that same book at local-equivalent cost, which
includes the depreciation still to come. The two are not the same quantity, and the
closed list of mechanisms that let a study re-point the bound -- capitalised interest,
a book re-based in period, a facility drawn mid-period -- does not carry this case. It
is NOT claimed as one of them: naming a mechanism the filings do not establish is the
assumption wearing a mechanism's clothes.

    python3 coc_record.py        adds `cost_of_capital_record` to study_numbers.json
"""
import io, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(HERE, 'study_numbers.json')
D = json.load(open(PATH, encoding='utf-8'))
W = D['wacc']
DR = D['drivers']
ROWS = D['cases']['base']['rows']

FWD = [float(x) for x in DR['wacc_path']]
WT = float(DR['wacc_terminal'])
WE = FWD[0]
DF = [float(r['df']) for r in ROWS]
GLIDE = [(WE - w) / (WE - WT) for w in FWD]

# the factors must be the compounded forward rates, and the terminal must arrive on the
# last explicit year's factor. Asserted here rather than described.
_c = 1.0
for i, w in enumerate(FWD):
    _c /= (1.0 + w)
    assert abs(_c - DF[i]) < 1e-9, ('discount factor %d does not compound from the ladder'
                                    % (i + 1))
assert all(FWD[i] >= FWD[i + 1] for i in range(len(FWD) - 1)), 'the ladder is not monotone'
assert WT < WE, 'the terminal rate is not below the explicit-window rate'

TOTAL_DEBT = float(W['total_debt'])
PCT_LOCAL = float(W['pct_debt_local'])
KD = float(W['kd_pretax_blended'])
KD_FX = float(W['kd_fx_local_equiv'])
KD_LOCAL = float(W['kd_local'])

# THE CONTRACTUAL ANCHOR REPRODUCES THE ADOPTED RATE, or it is worse than none.
_bal_fx = TOTAL_DEBT * (1.0 - PCT_LOCAL)
_bal_lc = TOTAL_DEBT * PCT_LOCAL
_blend = (_bal_fx * KD_FX + _bal_lc * KD_LOCAL) / (_bal_fx + _bal_lc)
assert abs(_blend - KD) < 1e-9, ('the anchor blends to %.9f against an adopted %.9f'
                                 % (_blend, KD))

# THE ONE INDEPENDENTLY COMPUTED PERIOD, from the filings' own figures: the finance
# charge on each facility over the balance that bears it. NOT total liabilities.
_I = None
try:
    import importlib.util as _ilu
    _spec = _ilu.spec_from_file_location('egch_inputs', os.path.join(HERE, 'inputs.py'))
except Exception:                                                    # noqa: BLE001
    _spec = None
KIMA2_LOAN, KIMA2_INT = 11580.629, 1338.013
HOLDCO_LOAN, HOLDCO_INT = 500.0, 96.896
EFF_FY2425 = (KIMA2_INT + HOLDCO_INT) / (KIMA2_LOAN + HOLDCO_LOAN)
EFF_HOLDCO = HOLDCO_INT / HOLDCO_LOAN

record = dict(
    rule='R-COC-01',
    market='EG',
    macro_path='EG',

    rf_observed=float(W['rf_observed']),
    default_spread=float(W['sov_spread_cds']),
    rf_star=float(W['rf_star_cds']),
    rf_normalisation_note=(
        "The risk-free rate is the local ten-year government yield of {0:.2%} less this "
        "sovereign's OWN credit-default-swap spread of {1:.2%}, and the equity premium "
        "added back is on the same credit-default-swap basis, so Egypt's country risk is "
        "counted exactly once. The rating basis is published beside it: a rating-basis "
        "spread of {2:.2%} with a rating-basis premium of {3:.2%} gives a cost of capital "
        "{4:.0f} basis points higher, and both are shown rather than one being chosen "
        "quietly."
        .format(float(W['rf_observed']), float(W['sov_spread_cds']),
                float(W['sov_spread_rating']), float(W['erp_rating']),
                float(W['wacc_rating_less_cds_bp']))),

    rf_terminal=float(DR['rf_star_terminal']),
    rf_terminal_note=(
        "DERIVED, NOT QUOTED: the house Egyptian path's terminal inflation of {0:.1%} plus "
        "its real-rate convention. It is the same figure the path returns for every "
        "Egyptian terminal, so this study cannot hold a private view of where the risk-free "
        "rate settles."
        .format(float(DR['inflation_lt']))),

    wacc_exp=WE,
    wacc_terminal=WT,
    forward_wacc=FWD,
    glide_fractions=GLIDE,
    ke_exp=float(W['ke_cds']),
    ke_terminal=float(DR['ke_terminal']),
    glide_note=(
        "One rate per explicit year, rebuilt from the ground up at each: the risk-free "
        "glides from {0:.2%} to the derived terminal {1:.2%} and the cost of debt glides "
        "with the currency wedge, and the weighted rate falls {2:.2%} -> {3:.2%} -> "
        "terminal {4:.2%}. Egypt is a transition market on the house path, so a single rate "
        "for five years and a perpetuity would assert that this economy never normalises, "
        "against the disinflation path this study's own currency wedge already follows."
        .format(float(W['rf_star_cds']), float(DR['rf_star_terminal']), WE, FWD[-1], WT)),

    discount_factors=DF,
    terminal_discount_factor=DF[-1],
    discounting_note=(
        "The terminal value is brought home on the SAME cumulative factor as the final "
        "explicit year, {0:.6f}, and the factors are the compounded forward rates rather "
        "than a single rate raised to a power. One date, one price of time."
        .format(DF[-1])),

    kd_pretax=KD,
    kd_after_tax=float(W['kd_aftertax']),
    kd_path=[float(x) for x in W['kd_pretax_path']],
    kd_integrity=dict(
        pct_local_currency=PCT_LOCAL,
        currency_source=(
            "ESTABLISHED FROM THE FACILITY NOTES BEFORE THE RATE WAS SET. The audited "
            "FY2024/25 statements disclose the borrowings facility by facility: the KIMA-2 "
            "bank consortium loan (note 18-1), the holding-company facility (note 18-2) and "
            "the ammonium-nitrate project loans (note 18-3), the last split explicitly into "
            "a pound leg and a dollar leg. Of total borrowings of EGP {0:,.0f}m, {1:.2%} is "
            "local currency and {2:.2%} is foreign. THE FOREIGN TRANCHE IS CARRIED AT "
            "LOCAL-EQUIVALENT COST -- the dollar coupon of {3:.2%} compounded with the "
            "expected pound depreciation the house path derives by relative "
            "purchasing-power parity, giving {4:.2%} in the first year and gliding with the "
            "wedge -- and never at the raw foreign coupon. That is why the adopted cost of "
            "debt sits ABOVE the {5:.2%} sovereign rather than below it, and it is the "
            "half of the amended rule that stops a foreign rate dropped into a "
            "local-nominal model from understating the cost."
            .format(TOTAL_DEBT / 1e6, PCT_LOCAL, 1 - PCT_LOCAL,
                    float(W['kd_usd_nominal']), KD_FX, float(W['rf_observed']))),
        interest_bearing_note=(
            "The effective rate's denominator is THE BORROWINGS THAT ACTUALLY BEAR THE "
            "CHARGE, facility by facility: EGP {0:,.3f}m of KIMA-2 consortium debt and EGP "
            "{1:,.1f}m drawn on the holding-company facility, against the finance costs "
            "disclosed for each in note 26. It is NOT total liabilities -- trade payables, "
            "the gas balance owed to the state supplier, contract liabilities and accruals "
            "bear no interest, and dividing the charge by a total that includes them "
            "understates the rate by a multiple and manufactures a bias that looks exactly "
            "like evidence."
            .format(KIMA2_LOAN, HOLDCO_LOAN)),
        effective_rates={'FY2024/25': EFF_FY2425},
        effective_rate_unavailable=(
            "ONE PERIOD, AND TWO SEPARATE REASONS, BOTH STATED. (1) Only the FY2024/25 "
            "audited statements disclose BOTH a finance-cost note broken down by facility "
            "and the balances those charges relate to; the earlier years and the interim "
            "statements this study reads do not carry the pair, so a second independently "
            "computed period cannot be built from what this company has published and is "
            "not manufactured. (2) MORE IMPORTANTLY, THE TRAILING CHARGE AND THE ADOPTED "
            "RATE ARE NOT THE SAME QUANTITY ON THIS BOOK. The computed FY2024/25 rate is "
            "{0:.2%} -- a charge measured in pounds at the exchange rates that actually "
            "prevailed, on a book that is {1:.1%} foreign-currency -- while the adopted "
            "{2:.2%} carries that same book at LOCAL-EQUIVALENT cost, which includes the "
            "depreciation still to come. Comparing them and dragging the adopted rate "
            "toward the trailing one would undo precisely the correction the amended rule "
            "requires. The closed list of mechanisms that lets a study re-point the 150bp "
            "bound -- capitalised interest, a book re-based in period, a facility drawn "
            "mid-period -- does not carry this case, and NONE OF THEM IS CLAIMED: naming a "
            "mechanism the filings do not establish would be the assumption wearing a "
            "mechanism's clothes. Recorded here so the gap in the list is visible rather "
            "than worked around."
            .format(EFF_FY2425, 1 - PCT_LOCAL, KD)),
        contractual_anchor=dict(
            lines=[
                dict(name='foreign-currency tranche at local-equivalent cost',
                     balance=_bal_fx, rate=KD_FX,
                     rate_basis=("the disclosed US-dollar facility coupon of {0:.2%} (KIMA-2 "
                                 "consortium and the dollar leg of the project loans, notes "
                                 "18-1 and 18-3) compounded with the first-year currency "
                                 "wedge of {1:.2%} the house path derives by relative "
                                 "purchasing-power parity"
                                 .format(float(W['kd_usd_nominal']),
                                         float(W['fx_wedge_path'][0])))),
                dict(name='local-currency tranche as disclosed',
                     balance=_bal_lc, rate=KD_LOCAL,
                     rate_basis=("the company's own disclosed rate on the holding-company "
                                 "facility, note 18-2 read with the note 26 finance cost: "
                                 "EGP {0:,.3f}m of interest on EGP {1:,.1f}m drawn "
                                 "independently computes to {2:.2%} against a disclosed "
                                 "{3:.2%}, which is the disclosure checking itself"
                                 .format(HOLDCO_INT, HOLDCO_LOAN, EFF_HOLDCO, KD_LOCAL))),
            ],
            blends_to=_blend,
            note=("The anchor REPRODUCES the adopted rate to nine decimal places, which is "
                  "the point of an anchor: a weighted average either comes out or it does "
                  "not, and one that does not is worse than none because it reads as "
                  "arithmetic. It is published here as evidence, NOT as a declaration that "
                  "the trailing effective rate is unusable -- that release requires a "
                  "mechanism from the closed list, and this book does not have one."),
        ),
        sovereign_floor_note=(
            "The one local-currency facility carries a disclosed {0:.2%} against a {1:.2%} "
            "sovereign ten-year yield -- a same-currency corporate borrowing BELOW its own "
            "government, which this rule normally refuses outright. It is the company's "
            "disclosed rate on a state-bank facility and is used as disclosed rather than "
            "raised to the floor, and it is {2:.2%} of the book, so it moves the blended "
            "rate by {3:.0f} basis points. The disclosure is carried rather than smoothed "
            "away, and the floor does not bind the book as a whole because the book is not "
            "local-currency."
            .format(KD_LOCAL, float(W['sovereign_floor']), PCT_LOCAL,
                    10000 * (KD - KD_FX))),
    ),

    erp_basis='cds',
    erp_central=float(W['erp_cds']),
    beta=float(W['beta']),
    weights=dict(equity=float(W['we']), debt=float(W['wd']),
                 basis='market_value_equity',
                 note=("Market-value equity of EGP {0:,.0f}m against total debt of EGP "
                       "{1:,.0f}m, never book equity."
                       .format(float(W['market_cap']) / 1e6, TOTAL_DEBT / 1e6))),
    sensitivity=dict(
        other_basis=dict(
            basis='rating',
            erp=float(W['erp_rating']),
            default_spread=float(W['sov_spread_rating']),
            ke_exp=float(W['ke_rating']),
            wacc_exp=float(W['wacc_rating']),
            difference_bp=float(W['wacc_rating_less_cds_bp']),
            note=("The rating-basis premium with its matching rating-basis default spread, "
                  "stripped and added back consistently. The market basis is named central "
                  "because it is the market's own live pricing of this sovereign's credit "
                  "against an agency judgement updated in steps."),
        ),
    ),

    published_central=None,
    published_central_branches=[float(b['value'])
                               for b in D['central_two_sided']['branches']],
    published_spot=float(D['spot']),
)

D['cost_of_capital_record'] = record
io.open(PATH, 'w', encoding='utf-8').write(
    json.dumps(D, indent=1, ensure_ascii=False, default=float) + '\n')

print('cost_of_capital_record written for EGCH')
print('   rf {0:.2%} - own CDS spread {1:.2%} = rf* {2:.2%};  terminal rf {3:.2%} (derived)'
      .format(float(W['rf_observed']), float(W['sov_spread_cds']), float(W['rf_star_cds']),
              float(DR['rf_star_terminal'])))
print('   forward WACC  ' + ' -> '.join('{0:.2%}'.format(w) for w in FWD)
      + '   terminal {0:.2%}'.format(WT))
print('   discount factors ' + ', '.join('{0:.4f}'.format(x) for x in DF))
print('   Kd {0:.2%} adopted; book {1:.2%} local / {2:.2%} foreign at local-equivalent cost; '
      'anchor blends to {3:.6f}'.format(KD, PCT_LOCAL, 1 - PCT_LOCAL, _blend))
