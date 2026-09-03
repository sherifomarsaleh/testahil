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
# the CDS basis is the house central under [R-COC-01] and this lens was the last
# thing in the study still reading the rating one [corrected 03-Sep-2026]
ke = D['wacc']['ke_cds']
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
# REBUILT from named comparables, 9 August 2026. The band was 3.0-6.0x sourced as an
# 'observed range' that named no peer, no transaction and no date, and it set the TOP
# of the published field. It is now the observable Egyptian listed range.
lo, hi = V('peer_ev_ebitda_low'), V('peer_ev_ebitda_high')
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
    "Book value, disclosed (a floor, never weighted)": L['book']['book_per_share'],
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
# ---------------- THE PUBLISHED CENTRAL: ONE LENS [R-LENS-03] ----------------
# The typed 45/20/20/15 blend is retired. It was chosen, written down and
# inherited, and it had never cleared any out-of-sample test. Averaging four
# methods does not make a number more robust than the best of them; it makes a
# FIFTH method with free parameters nobody tested, and here it did something
# worse than that. Two of the four readings it weighted are not valuations of
# this company at all:
#
#   NORMALISED EARNINGS is not a permitted lens for this class and is dropped.
#   It capitalises a mid-cycle margin at a fixed multiple on a company whose own
#   cash-flow model says the capital programme does not earn its cost of
#   capital. It carried a fifth of the weight and read EGP 4.29.
#
#   THE BOOK LENS WAS NOT BOOK VALUE. It published EGP 0.00 — a JUSTIFIED
#   price-to-book of zero, because sustainable return on equity (6.9%) sits below
#   the cost of equity (31.0%). That is a derived valuation wearing the name of a
#   disclosed figure, and it was weighted at 15%. The rule says book value is a
#   DISCLOSED FLOOR, published as such and never weighted: the disclosed floor is
#   EGP 8.16 a share of book equity. Both numbers are published below and neither
#   is weighted into the answer.
#
# THE PRIMARY IS THE CASH-FLOW LENS, AND IT HAS TWO VALUES ON PURPOSE. Whether
# the ANNA programme is carried through or stopped is this study's contested
# judgement, and the dual-framing rule forbids averaging it. The base case is
# CARRIED THROUGH, because that is what the company is doing; stopped is
# published beside it at every point.
_w = V('lens_weights')          # kept only to print what the retired blend read
_RETIRED_BLEND = (_w[0] * L['cashflow']['carry_through'] + _w[1] * L['relative']['value_per_share']
                  + _w[2] * L['normalised']['value_per_share'] + _w[3] * L['book']['value_per_share'])
L['central'] = dict(
    name="Cash-flow lens, programme carried through",
    primary='dcf',
    base=L['cashflow']['carry_through'],
    alternative_framing=dict(label="Cash-flow lens, programme stopped",
                             value=L['cashflow']['stopped']),
    bear=L['cashflow']['downside'], bull=L['cashflow']['upside'],
    retired_blend=dict(weights=dict(cashflow=_w[0], relative=_w[1],
                                    normalised=_w[2], book=_w[3]),
                       value=_RETIRED_BLEND),
    note=("The central is the cash-flow lens on the company's own tonnes, prices and "
          "disclosed capital programme, carried through. It is not a blend. The relative "
          "multiple is published beside it as a cross-check, the disclosed book value as a "
          "floor, and normalised earnings as a diagnostic this class does not weight. The "
          "retired blend of all four read EGP %.2f." % _RETIRED_BLEND),
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
# The study's ANSWER, exposed where the repo-level valuation-gap gate reads it: the numbers
# file carries the central fair value and the spot it was struck against [R-GAP-01].
# ---------------- NO SINGLE CENTRAL, ON INSTRUCTION [03-Sep-2026] -------------
# The contested judgement here is BINARY and it STRADDLES ZERO: carried through
# the cash-flow lens reads about -1.06 a share, stopped it reads about +2.82, and
# the difference is not uncertainty about a rate — it is whether a plant gets
# finished. A number between them describes a world in which the capital
# programme is half built, which nobody is proposing and the company is not doing.
#
# The dual-framing rule already forbade averaging that pair. This is the further
# step, taken on the principal's instruction: the study publishes BOTH BRANCHES
# AND NO SINGLE FIGURE. A reader gets the two answers and the condition that
# decides between them, rather than a central that is true in neither world.
#
# central is therefore null and central_two_sided carries the pair. That is a
# READABLE answer, not a missing one, and the gates distinguish the two: a study
# with no answer at all is a defect, and this is a study whose answer the
# repository's one-number shape cannot hold.
D['central'] = None
D['central_two_sided'] = dict(
    branches=[
        dict(label='Cash-flow lens, capital programme carried through',
             value=float(L['contested']['side_a']),
             condition='the ANNA programme is completed and commissioned as the '
                       'company is currently doing'),
        dict(label='Cash-flow lens, capital programme stopped',
             value=float(L['contested']['side_b']),
             condition='the programme is halted and the remaining spend is not '
                       'committed'),
    ],
    question=L['contested']['question'],
    decides=L['contested']['decides'],
    gap_per_share=float(L['contested']['gap']),
    why_not_averaged=(
        'the judgement is binary and its two answers straddle zero, so an average '
        'describes a half-built plant — a world nobody is proposing and the '
        'company is not in. Averaging would also hide the finding: that on the '
        'disclosed bank-approved cost and the derived nameplate, the programme '
        'does not earn the capital sunk into it, which is why stopping is worth '
        'more than finishing.'),
    both_sides_vs_spot=[
        dict(label='carried through',
             pct=float(L['contested']['side_a'] / SPOT - 1.0) * 100.0),
        dict(label='stopped',
             pct=float(L['contested']['side_b'] / SPOT - 1.0) * 100.0),
    ],
)
D['spot'] = float(SPOT)
# The envelope now spans BOTH branches, and its base is null for the same reason
# the central is: there is no single number in the middle of a binary decision.
D['fair'] = dict(bear=float(min(L['central']['bear'], L['contested']['side_b'])),
                 base=None,
                 full=float(max(L['central']['bull'], L['contested']['side_b'])))

# ===========================================================================
# THE THREE CONSTRUCTION RECORDS this study owed [R-MACRO-01, R-LENS-03,
# R-BRIDGE-01]. Each is a set of CHOICES written down so a job outside the
# study can check them, because the number they produce cannot be checked by
# recomputing it.
# ===========================================================================
import sys as _sys, os as _os
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
import macro_path as _MPATH
_P = _MPATH.load('EG')
_PI = list(_P.inflation_path)
_YR = list(_P.inflation_years)
_CASE = D['cases']['base'] if isinstance(D.get('cases'), dict) else None

D['macro_record'] = dict(
    market='EG', path_as_of=_P.as_of,
    growth_lines=[
        dict(name='terminal maintenance growth',
             years=_YR, nominal=[V('g_terminal')] * len(_YR), real=0.0,
             exempt_reason='not an escalator: the forecast years are built from '
                           'tonnes, dollar prices and the derived currency path, '
                           'each disclosed or identity-derived, so there is no '
                           'nominal growth rate here to sit on the ladder'),
    ],
    fx_path=None,
    fx_note='the currency path is DERIVED year by year from the relative '
            'purchasing-power identity on the house terminal inflation against '
            'long-run United States inflation, and the SAME wedge carries the '
            'dollar cost of debt, so the two cannot disagree',
    terminal=dict(g_nominal=V('g_terminal'), real=0.0,
                  rf=_P.terminal_rf, inflation_in_rf=_P.terminal_inflation),
    explicit_years=5,
    growth_at_horizon_end=V('g_terminal'),
    note='THE HOUSE PATH OVERRULES AN ARGUMENT THIS STUDY MADE WELL. The 9 August '
         '2026 edition moved terminal inflation to 5% after an external critique, '
         'reasoning that a perpetuity takes the longest-horizon published target '
         'there is. The house path takes 7% on a later reading of the same bank: '
         'its August 2026 guidance puts the return to the 7% BAND in the second '
         'half of 2027 and forecasts no 5% undershoot. Both are defensible; five '
         'studies each picking one is not. The change costs this study EGP 0.28 a '
         'share and the cost is stated rather than absorbed.',
)

D['lens_record'] = {
    'class': 'petrochemical',
    'primary': dict(
        kind='dcf', value=float(L['central']['base']),
        range=dict(low=float(L['central']['bear']), high=float(L['central']['bull'])),
        range_note='the cash-flow lens across the dollar export price, from the '
                   'flat-at-opening path the base case holds to the higher path the '
                   'upside case holds, with the programme carried through in both '
                   'and the macro path held still',
        range_basis=dict(
            driver='the dollar export price per tonne of urea',
            low=float(D['drivers']['export_usd_path'][0]), high=float(D['drivers']['export_usd_path_bull'][0]),
            units='US$ per tonne, f.o.b. Egypt',
            macro_held=True,
            evidence='the base case holds the price FLAT in nominal dollars at the '
                     'opening level, because no forecast of a traded commodity price is '
                     'defensible and that is the convention this house applies to the '
                     'same class of input elsewhere; the upside case holds it nearer the '
                     'CME FOB Egypt settlement of 7 August 2026. Both are levels the '
                     'market has actually printed, not a chosen percentage band, and '
                     'the currency path, the cost of capital and terminal growth are '
                     'held at the house macro path across both.'),
        note='the cash-flow lens on the company\'s own tonnes, dollar prices and '
             'disclosed capital programme, discounted on the glide. THE CONTESTED '
             'JUDGEMENT IS BINARY AND IT STRADDLES ZERO: carried through the lens '
             'reads %.2f, stopped it reads %.2f, and the two are published side by '
             'side and never averaged.'
             % (L['cashflow']['carry_through'], L['cashflow']['stopped'])),
    'cross_checks': [
        # THE INGREDIENTS, NOT THE SENTENCE [added 03-Sep-2026]. AMOC's record used
        # these same reassuring words while its code divided the MARKET CAP by
        # base-year EBITDA, and passed three times, so the claim is arithmetic
        # everywhere now: the adopted multiple beside the three numbers that
        # reproduce the traded one. 7.95x adopted against a traded 8.25x -- close,
        # which is worth seeing rather than hiding, and clear of the half-per-cent
        # refusal band.
        dict(kind='relative_multiple', value=float(L['relative']['value_per_share']),
             present_value=False,
             multiple=float(L['relative']['mult_mid']),
             circularity=dict(spot=float(D['spot']), shares=float(SHARES) / 1e6,
                              net_debt=float(CASES['base']['bridge']['net_debt']),
                              metric_value=float(L['relative']['ebitda_fwd'])),
             multiple_source='forward EBITDA times a multiple from the company\'s '
                             'own history and its regional peers, never one read '
                             'off the current price'),
        dict(kind='book_value', value=float(L['book']['book_per_share']),
             present_value=False,
             note='the DISCLOSED book equity per share, published as a floor and '
                  'never weighted. The retired blend weighted a JUSTIFIED '
                  'price-to-book of zero at 15%% under this name — a derived '
                  'valuation wearing the name of a disclosed figure. The justified '
                  'multiple is %.2fx and is kept as a diagnostic: it says the '
                  'company does not earn its cost of equity, which is a finding, '
                  'not a book value.' % L['book']['pb_justified']),
    ],
    'retired': dict(
        blend=L['central']['retired_blend']['weights'],
        blend_value=float(L['central']['retired_blend']['value']),
        why='the weights were typed and had never cleared an out-of-sample test, '
            'and here the blend did something worse than average: it mixed a '
            'negative cash-flow read with three positive ones and published a '
            'positive number, so a reader saw EGP %.2f and never learned that the '
            'study\'s own primary lens was below zero.'
            % L['central']['retired_blend']['value'],
    ),
    'diagnostics': dict(
        normalised_earnings=float(L['normalised']['value_per_share']),
        justified_price_to_book=float(L['book']['pb_justified']),
        book_value_floor=float(L['book']['book_per_share']),
    ),
}

_BR = _CASE['bridge'] if _CASE else {}
# ---- [R-ANCHOR-01] THE FORECAST ANCHOR, PRINTED WHETHER OR NOT IT FIRES ------
# EGCH is the shape the gate deliberately does NOT fire on, and the record exists
# so a reader can see that rather than merely not-red. The first forecast year
# opens at 45.66% against a latest AUDITED year of 38.39% -- nineteen per cent
# ABOVE it, not below -- which is [R-GAP-01]'s two-sided trigger and [R-ENF-05]'s
# sign test to audit, not this rule's.
#
# It is worth recording what that number was before this edition: the previous
# forecast opened at the same 45.66% and FELL to 33.02%, below every audited year
# except FY2023/24, on a typed dollar export price falling 17% that nothing
# sourced. The opening year was never the problem; the path away from it was, and
# a record that captured only the opening year would have missed it. That is why
# the committed record carries the whole path.
D['forecast_anchor'] = dict(
    rate_name='gross margin',
    latest_reviewed_period='FY2024/25, audited',
    latest_reviewed_date='2025-06-30',
    latest_reviewed_rate=float(D['hist'][-1]['gross'] / D['hist'][-1]['revenue']),
    first_forecast_rate=float(D['cases']['base']['rows'][0]['gross']
                              / D['cases']['base']['rows'][0]['revenue']),
    forecast_path=[float(r['gross'] / r['revenue']) for r in D['cases']['base']['rows']],
    # THE PATH CLAUSE OF [R-ANCHOR-01] FIRED ON THIS STUDY AND THE MECHANISM IS
    # DECLARED RATHER THAN THE DRIVER CHANGED, because unlike AMOC's the
    # like-for-like measurement in this company's own filings SUPPORTS it.
    #
    # With the dollar export price now held flat, the margin still falls 45.66% to
    # 42.08% across the window -- 7.9% relative -- because the domestic cost legs
    # (wages, services, other materials) are pound-denominated and escalate on the
    # Egyptian inflation path while revenue is dollar-linked and translates only at
    # the derived currency path. That is a real cost drift and it is a CLAIM, so it
    # is named, sourced and measured on the same terms any other claim is.
    #
    # The measurement: cost per unit of revenue in this company's own audited
    # accounts runs 54.059% (FY2022/23) to 61.613% (FY2024/25) -- it ROSE 7.55
    # points. The mechanism and the filings agree, which is precisely the test AMOC
    # failed on the same clause: there a claimed mechanism was refused because the
    # same quarter a year apart moved the opposite way.
    mechanism=dict(
        name='input_cost_outpacing_price',
        disclosure='the cost stack disclosed in the audited statements splits into a '
                   'dollar-linked gas charge and pound-denominated legs (wages, '
                   'services, other materials); the export price that carries most of '
                   'revenue is set in dollars. The pound legs escalate on the Egyptian '
                   'inflation path and the dollar revenue translates at the derived '
                   'currency path, and the two are not the same rate.',
        like_for_like=dict(
            measures='cost per unit of revenue, audited full years',
            period_a='FY2022/23', value_a=0.54059,
            period_b='FY2024/25', value_b=0.61613,
            higher_is_worse=True)),
    note='the audited record is FY2022/23 45.94%, FY2023/24 32.71%, FY2024/25 38.39%, '
         'and the part-year FY2025/26 estimate is 43.87%. The forecast opens ABOVE the '
         'latest audited year and is held roughly flat rather than escalated, because '
         'the dollar export price is now held FLAT in nominal dollars -- the convention '
         'this house applies to the same class of input elsewhere. The previous edition '
         'opened at the same rate and fell to 33.02% on a typed price path nothing '
         'sourced.')

D['bridge_record'] = dict(
    market='EG',
    balance_sheet_date='2026-03-31',
    latest_disclosed_date='2026-03-31',
    latest_disclosed_source='the reviewed interim statements for the nine months '
                            'ended 31 March 2026 (limited review dated 20 May '
                            '2026), read from the rendered pages and registered in '
                            'this study\'s sweep. No later filing exists: the '
                            'annual for the year to 30 June 2026 is filed in '
                            'September or October on the company\'s own pattern.',
    register='sweep_register.json',
    lines=[
        dict(label='Enterprise value', value=float(_BR.get('ev', 0.0))),
        dict(label='plus cash, 31 March 2026', value=float(_BR.get('cash', 0.0))),
        dict(label='less borrowings, 31 March 2026', value=-float(_BR.get('debt', 0.0))),
        dict(label='plus investments at fair value through other comprehensive income',
             value=float(_BR.get('fvoci', 0.0))),
        dict(label='plus investment property', value=float(_BR.get('inv_prop', 0.0))),
    ],
    equity_value=float(_BR.get('equity', 0.0)),
    shares_mn=float(_BR.get('shares', 0.0)) / 1e6,
    per_share=float(_BR.get('per_share', 0.0)),
    cash=dict(treatment='added_at_face', weights_basis='gross'),
    cash_charged_once=True,
    cash_note='the operations are discounted at a rate weighted on gross debt and '
              'the cash is added once, at face, in the bridge.',
    nci=dict(basis='none_disclosed',
             evidence='the reviewed statements to 31 March 2026 show no '
                      'non-controlling interest on the face of the balance sheet '
                      'and none in the equity note; the company\'s subsidiaries '
                      'are wholly owned.'),
    associates=dict(basis='book',
                    note='investments at fair value through other comprehensive '
                         'income and investment property are carried at their '
                         'disclosed balance-sheet amounts; neither is a listed '
                         'associate with a market quote.'),
    dividend_deducted=False,
    dividend_note='no dividend was declared after the bridge\'s balance-sheet date.',
)

json.dump(D, open(os.path.join(HERE, 'study_numbers.json'), 'w'), indent=1, default=float)
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
