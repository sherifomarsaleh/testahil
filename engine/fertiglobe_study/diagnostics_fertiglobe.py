#!/usr/bin/env python3
"""FERTIGLOBE — the reverse read and the sign test.  [R-ENF-05]

    python3 diagnostics_fertiglobe.py     writes diagnostics.json and
                                          contested_judgements.json

WHY THESE RECORDS ARE COMPUTED AND NOT TYPED. Both answer questions the committed
numbers do not contain: what the traded price must believe, and what each contested
framing is worth. A record built by reading figures off the model can only report
choices somebody has already priced. This module RE-RUNS the study's own model for
every framing it prices — the same build_frame -> run_dcf -> bridge chain the study
publishes on — so every figure below is a full re-run rather than an interpolation,
and an artefact that no generator writes is a number frozen at the date somebody
last typed it.

WHY THE QUANTITY SOLVED IS A PRICE AND NOT A DISCOUNT RATE. A reverse read exists so
a reader can judge the DISAGREEMENT rather than the conclusion, which means it has to
land in a unit the reader can check against something the company or its market has
actually printed. This company's value turns on one question the study itself names
as its central contested judgement — whether nitrogen prices revert toward the
marginal cost of the swing supplier or hold near current levels — and that question
is denominated in dollars per tonne, quoted by a market and disclosed in the
company's own results reports for four separate periods. So the solved quantity is
THE MID-CYCLE UREA BENCHMARK, and the axis it is solved along is the study's own two
published price paths rather than one invented here. The flat discount rate the
shared instrument solves is kept BESIDE it as a second reading, because it says
something the price axis cannot: on the higher of the two framings the market and
this study agree about the price of time to within a few basis points, so what is
left of the disagreement is the price of urea and nothing else.

THE ANSWER IS TWO-SIDED AND BOTH SIDES ARE SOLVED. The study publishes framing A and
framing B and refuses to average them. Solving on one side only, or pricing the
judgements on one side only, would quietly make the choice the study declined to
make — so every judgement below is priced on BOTH branches and the record states
whether any of them changes direction between them.

CONTAINMENT, ENFORCED HERE RATHER THAN REMEMBERED. Nothing solved here may re-enter
the valuation: a quantity solved from a price and then used is the reverse-engineered
rate the protocol prohibits outright, arriving through a side door. main() ASSERTS
that the solved value does not appear in study_numbers.json before it writes
anything, and no builder in this directory reads either file this module writes.

THE COMMITTED NUMBERS FILE IS NOT TOUCHED. compute.py writes study_numbers.json at
import, so importing it to re-run the model would restamp the study's own committed
record. The file's bytes are held before the import and restored immediately after,
and the restoration is asserted byte-for-byte. This module also asserts that the
re-run reproduces the committed per-share answers exactly: a diagnostic measured
against a model that has drifted from the delivered one measures something else.
"""
import json
import os
import sys
from math import comb

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))

NUM = os.path.join(HERE, 'study_numbers.json')
_BYTES = open(NUM, 'rb').read()
COMMITTED = json.loads(_BYTES.decode('utf-8'))

import compute as C                              # noqa: E402  re-runs the study's own model
import macro_path as MP                          # noqa: E402  the house path
import reverse_read as RR                        # noqa: E402  the shared reverse-read instrument

if open(NUM, 'rb').read() != _BYTES:             # the import above rewrote it
    open(NUM, 'wb').write(_BYTES)
assert open(NUM, 'rb').read() == _BYTES, 'the committed numbers file was not restored'

AS_OF = '2026-09-06'
A = float(C.br_A['ps_aed'])           # framing A — the branch read as this study's central
B = float(C.br_B['ps_aed'])           # framing B
SPOT_STRIKE = float(C.SPOT_AED)       # AED 2.54, ADX close 7 August 2026, the strike price
SPOT_LATEST = 2.67                    # AED, ADX close 3 September 2026, the latest known price
SPOT_LATEST_DATE = 'close 3 September 2026'

for _l, _got, _want in (('A', A, COMMITTED['bridge_A']['ps_aed']),
                        ('B', B, COMMITTED['bridge_B']['ps_aed'])):
    assert abs(_got - float(_want)) < 1e-12, (
        'the re-run does not reproduce the committed framing %s (%r against %r)' % (_l, _got, _want))


# ---------------------------------------------------------------------------
# THE MODEL, RE-RUN. Every figure in both records comes through one of these.
# ---------------------------------------------------------------------------
def branch(pu, pn):
    """One complete pass of the study's own chain on a given price path."""
    f = C.build_frame(pu, pn, 'alt')
    d = C.run_dcf(f, C.wacc_rating, C.wacc_term_rating)
    return f, d, C.bridge(d)


def bridge_ps(ev, extra_debt=0.0, extra_equity=0.0, nci_basis='earnings'):
    """The study's own bridge with one line moved."""
    eq_total = ev - C.V['netdebt_h1_26'] - extra_debt
    nci = eq_total * C.NCI_SHARE if nci_basis == 'earnings' else C.V['eqnci_fy25']
    return float((eq_total - nci + extra_equity) / C.SHARES * C.FX)


def with_drivers(pu, pn, **drivers):
    """A branch re-run with module-level drivers replaced, then restored."""
    saved = {k: getattr(C, k) for k in drivers}
    try:
        for k, v in drivers.items():
            setattr(C, k, v)
        return float(branch(pu, pn)[2]['ps_aed'])
    finally:
        for k, v in saved.items():
            setattr(C, k, v)


def at_rates(pu, pn, wacc_exp=None, wacc_term=None, **kw):
    return float(C.dcf_ps(pu, pn,
                          C.wacc_rating if wacc_exp is None else wacc_exp,
                          C.wacc_term_rating if wacc_term is None else wacc_term, **kw))


def with_ke(pu, pn, ke, ke_term=None):
    kt = ke if ke_term is None else ke_term
    return at_rates(pu, pn, C.WE * ke + (1 - C.WE) * C.KD_AT,
                    (1 - C.WD_TERM) * kt + C.WD_TERM * C.KD_AT)


def with_wc_accrual_inside(pu, pn):
    """The accrual left in payables — both the days measure and the opening base."""
    saved = (C.DPO, C.V['sorfert_accr_fy25'])
    try:
        C.DPO = C.ccc['FY25']['dpo']
        C.V['sorfert_accr_fy25'] = 0.0
        return float(branch(pu, pn)[2]['ps_aed'])
    finally:
        C.DPO, C.V['sorfert_accr_fy25'] = saved


assert abs(branch(C.PRICE_A_UREA, C.PRICE_A_NH3)[2]['ps_aed'] - A) < 1e-12, \
    'the re-runner does not reproduce the base case'


# ---------------------------------------------------------------------------
# 1. THE REVERSE READ — the mid-cycle urea price the traded price is paying for
# ---------------------------------------------------------------------------
# THE AXIS IS THE STUDY'S OWN. Framing A and framing B are two complete price paths
# the study publishes; the solve moves along the line between them, and off either
# end if it has to, so the quantity varied is the nitrogen price basis and nothing
# else. Every other driver — tonnes, the calibrated cost pass-through, the
# cost-of-capital schedule, the terminal, the bridge — stays at its published value.
def price_path(lam):
    return ([a + lam * (b - a) for a, b in zip(C.PRICE_A_UREA, C.PRICE_B_UREA)],
            [a + lam * (b - a) for a, b in zip(C.PRICE_A_NH3, C.PRICE_B_NH3)])


def value_at(lam):
    return float(C.dcf_ps(*price_path(lam)))


def mid_cycle(path):
    """The study's own definition of mid-cycle — the average of the last three
    forecast years, which is what its own relative lens applies its multiple to."""
    return float(sum(path[2:]) / 3.0)


def feasible(lam):
    """The value at one point on the axis, or None where the sanctioned terminal
    REFUSES. A price path low enough to make terminal free cash flow negative is a
    liquidation rather than a going concern, and the module says so rather than
    returning a number — so the solve's own bracket has to stay inside the region
    where the study's model is defined, and that region is FOUND rather than assumed."""
    try:
        return value_at(lam)
    except Exception:                                                   # noqa: BLE001
        return None


def feasible_bracket(step=0.05, limit=6.0):
    """The widest interval around the study's own two paths on which the model builds.
    Walking outward from 0 and 1 rather than guessing an interval, because a bracket
    that reaches into the refusal region turns a refusal into a crash and a bracket
    chosen to contain the answer is not a bracket."""
    lo = 0.0
    while lo - step >= -limit and feasible(lo - step) is not None:
        lo -= step
    hi = 1.0
    while hi + step <= limit and feasible(hi + step) is not None:
        hi += step
    return lo, hi


LO, HI = feasible_bracket()


def solve_lambda(target):
    """Bisection. Value is monotone in the price basis, so the root is unique and the
    answer cannot depend on where the search began. THE BRACKET IS ASSERTED: a solve
    that ran off its own end must raise rather than return an endpoint, which would
    look exactly like an answer."""
    lo, hi = LO, HI
    assert value_at(lo) < target < value_at(hi), (
        'the traded price of AED %.4f lies outside the interval the study\'s own model '
        'is defined on (AED %.4f to AED %.4f), so there is no reverse read to report '
        'and an endpoint must not be returned as one'
        % (target, value_at(lo), value_at(hi)))
    for _ in range(400):
        mid = 0.5 * (lo + hi)
        if value_at(mid) < target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def read_price(target):
    lam = solve_lambda(target)
    u, n = price_path(lam)
    return dict(lam=float(lam), value_reproduced=value_at(lam),
                mid_cycle_urea=mid_cycle(u), mid_cycle_ammonia=mid_cycle(n),
                urea_2030=float(u[-1]), ammonia_2030=float(n[-1]))


PX_LATEST = read_price(SPOT_LATEST)
PX_STRIKE = read_price(SPOT_STRIKE)
MID_A, MID_B = mid_cycle(C.PRICE_A_UREA), mid_cycle(C.PRICE_B_UREA)

# THE SECOND READING — the flat discount rate, through the SHARED instrument rather
# than one written here, so the number is comparable with every other study's.
_coc = COMMITTED['cost_of_capital_record']
_times, _how = RR.resolve_times(_coc, C.dcf_A['df'], _coc['forward_wacc'])


def flat_rate(frame, dcf, br, target):
    return RR.read(frame['fcff'], _times, dcf['tv'], dcf['wacc_term'], dcf['g'],
                   dcf['df'][-1], dcf['df'][-1], dcf['ev'], br['eq_attr'],
                   C.SHARES, target / C.FX)


RATE_A = flat_rate(C.frame_A, C.dcf_A, C.br_A, SPOT_LATEST)
RATE_B = flat_rate(C.frame_B, C.dcf_B, C.br_B, SPOT_LATEST)

# what the company and its own cited price reporters have actually printed
DISCLOSED = [('FY2024 average, granular urea free on board Egypt', C.V['bm_urea_eg_fy24']),
             ('FY2025 average', C.V['bm_urea_eg_fy25']),
             ('first half 2026 average', C.V['bm_urea_eg_h1_26']),
             ('July 2026', C.V['bm_urea_eg_jul26'])]


# ---------------------------------------------------------------------------
# 2. THE CONTESTED JUDGEMENTS — every one priced by re-running the model
# ---------------------------------------------------------------------------
# THE BASE IS FRAMING A AND THE CHOICE IS DECLARED RATHER THAN CONVENIENT. The study
# is two-sided, so every alternative has to be priced against one of its two branches.
# Framing A is the branch this study's own gap review audits, the branch the
# repository's gap reader takes as its central, and the branch a reader is handed
# whenever one number is wanted. Every judgement is ALSO priced on framing B and the
# directions compared, so the base cannot be quietly doing the work: the record states
# whether any material judgement changes sign between the two branches.
#
# THE HUNT WAS THE STUDY'S OWN JUDGEMENTS TABLE FIRST — sixteen rows in the delivered
# source document, each already naming what was chosen and what would overturn it —
# and then the places a table like that does not reach: the bridge, the terminal
# rate, terminal leverage, and the two constructions the study's own gap review had
# already conceded. Two forks are named and NOT priced, because pricing them would
# have meant choosing a number nobody has published; they are in `examined_not_priced`
# rather than left out, since an absent answer is not a clean one.
LCA_CAPACITY_KT = 1000.0        # one-million-tonne lower-carbon ammonia plant, sweep register
LCA_STAKE = 0.54                # the option is to move to 54% ownership after completion
LCA_COST_PER_T = 500.0          # the company's own disclosed cost: under $500m of project cost

_GD_STUDY = C.V['debt_usd_fy25'] + C.V['debt_aud_fy25'] + C.V['debt_dzd_fy25']
_WE_GROSS = C.MKTCAP_USD / (C.MKTCAP_USD + _GD_STUDY)
_KE_TERM_NORM = MP.load('AE').terminal_rf + C.BETA * C.erp_rating
_M26 = C.V['seg_3p_ebitda_h1_26'] / C.V['seg_3p_rev_h1_26']
_UTIL_U = [C.UTIL_UREA[0]] * 5
_UTIL_N = [C.UTIL_NH3[0]] * 5
_VU = [C.V['cap_urea'] * u for u in _UTIL_U]
_VN = [C.V['cap_nh3_merchant'] * u for u in _UTIL_N]
_LCA_ADD = LCA_CAPACITY_KT * LCA_COST_PER_T / 1000.0 * LCA_STAKE
_LCA_ADD_REPL = LCA_CAPACITY_KT * C.REPLACEMENT_PER_T / 1000.0 * LCA_STAKE


def _blend(ctx):
    """The retired four-lens blend rebuilt on ONE branch, so the entry measures the
    lens architecture alone and does not re-count the price framing a second time."""
    return float(0.45 * ctx['base'] + 0.20 * C.rel_ps_aed
                 + 0.20 * C.norm_ps_aed + 0.15 * C.book_ps_aed)


JUDGEMENTS = [
    dict(
        name="the nitrogen price path — the study's own central contested judgement",
        adopted='both framings computed in full and published side by side, never '
                'averaged; framing A — reversion toward the marginal cost of the swing '
                'supplier — is the branch read as this study\'s central',
        alternative='framing B, the structurally-tight reading, on the same tonnes, the '
                    'same calibrated cost stack and the same discount schedule',
        alt=lambda ctx: ctx['other'],
        why='the study settles this nowhere and says so. Framing A treats the 2026 spike '
            'as a war premium on a marginal-cost anchor set by European gas; framing B '
            'rests on the company\'s own sourced balance — demand growth outside China of '
            'about 11.4 million tonnes to 2030 against about 9.1 million tonnes of '
            'additions — plus the rising European tariff wall on Russian product. It is '
            'recorded because it is by far the largest fork in the study AND because the '
            'branch a reader is handed when one number is wanted is the lower of the two, '
            'which is exactly the kind of fact this record exists to make countable.'),
    dict(
        name='the lens architecture',
        adopted='one lens is the answer — the cash-flow lens, with the enterprise '
                'multiple and book value published beside it as cross-checks and never '
                'weighted into it',
        alternative='the retired 45/20/20/15 blend of cash flow, enterprise multiple, '
                    'normalised earnings and book, rebuilt on this branch alone',
        alt=_blend,
        why='the weights were typed, inherited and had never cleared an out-of-sample '
            'test, and a blend imports the weakest lens at whatever number somebody wrote '
            'down: book value here is depreciated historical cost on plants whose worth '
            'turns on a gas position, and the normalised-earnings lens capitalised a '
            'mid-cycle profit on a multiple of 11.0 that nobody sourced. Priced on one '
            'branch alone deliberately — the blend the study actually retired ALSO '
            'averaged the two price framings, and counting that here would price the '
            'same choice twice.'),
    dict(
        name='non-controlling interests',
        adopted='deducted at their share of equity VALUE, proxied by their disclosed '
                '26.3% share of group profit',
        alternative='deducted at the book carrying amount of those interests, $443.3m',
        alt=lambda ctx: bridge_ps(ctx['ev'], nci_basis='book'),
        why='the model capitalises 100% of subsidiary cash flow, so the minority\'s claim '
            'is worth its share of THAT value rather than its historical cost — and the '
            'two outside stakes (49.01% of the Algerian producer, 25.0% of the Egyptian '
            'one) sit in the group\'s most profitable assets, so they take far more of '
            'the profit than of the book. The study calls its own choice the more '
            'conservative of the two and publishes both. It is the largest single step in '
            'the bridge.'),
    dict(
        name='the equity risk premium — which country',
        adopted='blended across the countries the plants are in, weighted by disclosed '
                'non-current assets — 50.9% UAE, 31.1% Egypt, 16.1% Algeria — giving 8.51%',
        alternative="the listing domicile alone: Abu Dhabi's own published premium of "
                    '4.87%, the convention that prices a company where its shares trade',
        alt=lambda ctx: with_ke(ctx['pu'], ctx['pn'],
                                C.rf_star_rating + C.BETA * C.V['ad_erp']),
        why='nearly half the asset base sits in Egypt and Algeria, so pricing the whole '
            'group on an Abu Dhabi premium would charge it for country risk it does not '
            'carry and credit it with safety it does not have. This is the largest '
            'cost-of-capital fork in the study, the study takes the more expensive side '
            'of it, and it is priced here rather than argued away.'),
    dict(
        name='the equity risk premium — which basis',
        adopted='the credit-rating basis, 8.51%',
        alternative="the sovereign default-swap basis, 7.14% — the market's own live "
                    'pricing of the same credit, against an agency judgement updated in '
                    'steps',
        alt=lambda ctx: float(ctx['cds']),
        why='both bases are published in the study and neither is averaged into the '
            'other. The swap basis is the NARROWER premium here, so adopting the rating '
            'basis is the more punitive of the two — which is worth saying plainly, '
            'because a cautious-sounding choice is still a claim about the world.'),
    dict(
        name='the unsettled Algerian gas accrual, in the BRIDGE',
        adopted='not deducted: it is charged through the cost line as it accrues and is '
                'excluded from working capital, and the bridge deducts only net debt',
        alternative='deducted from equity value as a debt-like obligation — $468.8m '
                    'accrued at 30 June 2026, retrospective to November 2023, with no '
                    'agreed payment schedule and treated by the auditors as a key audit '
                    'matter',
        alt=lambda ctx: bridge_ps(ctx['ev'], extra_debt=C.V['sorfert_accr_h1_26']),
        why='the study\'s own judgements table settles how this accrual is treated in '
            'WORKING CAPITAL and is silent on whether the accumulated balance is a claim '
            'on enterprise value. On one reading it is a real unsettled obligation that '
            'has to come out of the bridge; on the other it is an estimate that will keep '
            'being trued up through the cost line the model already charges. This is the '
            'largest fork in the study that runs in the study\'s own favour.'),
    dict(
        name='the lower-carbon ammonia project',
        adopted='excluded from the valuation entirely — no cash flow, no capital and no '
                'value; named as an unpriced upside catalyst instead',
        alternative="carried at the company's own disclosed capital cost for the "
                    'one-million-tonne plant — under $500m of total project cost — at the '
                    '54% interest the option describes, added to attributable equity',
        alt=lambda ctx: ctx['base'] + _LCA_ADD / C.SHARES * C.FX,
        why='the parent is warehousing the project and the company holds an option, not '
            'an asset, so nothing is consolidated today. THE ALTERNATIVE IS AN UPPER '
            'BOUND AND IS LABELLED ONE: the consideration payable on exercise is '
            'disclosed nowhere, so the option is priced here as though it were free, '
            'which it will not be. Valued instead on this study\'s own replacement cost '
            'of $1,250 a tonne of installed capacity the same construction gives '
            'AED %.4f a share; the company\'s own disclosed project cost is used because '
            'a figure the company published outranks one this desk assumed.'
            % (A + _LCA_ADD_REPL / C.SHARES * C.FX)),
    dict(
        name='the terminal risk-free rate',
        adopted="today's Abu Dhabi sovereign yield less that sovereign's own default "
                'spread, 4.73%, held flat into the terminal',
        alternative='the terminal risk-free rate the house macro path derives from its '
                    'inflation anchor and real-rate convention, 3.98%',
        alt=lambda ctx: at_rates(ctx['pu'], ctx['pn'],
                                 wacc_term=(1 - C.WD_TERM) * _KE_TERM_NORM
                                 + C.WD_TERM * C.KD_AT),
        why='a pegged market gets a flat cost-of-capital schedule, and flat should mean '
            'flat at the NORM rather than flat at today\'s spot. THIS IS A CONCEDED '
            'DEFECT RATHER THAN A DEFENDED FORK: the study\'s own gap review names it, '
            'prices it at about 75 basis points, records that correcting it RAISES the '
            'value, and registers it for a deliberate cost-of-capital pass rather than '
            'stacking it on the terminal rebuild in one edition. It is recorded here '
            'because it is a material choice standing at the lower value, whatever the '
            'reason for the delay.'),
    dict(
        name='terminal leverage',
        adopted='the debt weight normalises to 20%, where merchant nitrogen producers '
                "actually run, above the group's currently light net leverage",
        alternative="the group's current 9.8% net-debt weight carried into the terminal, "
                    'which collapses the glide and capitalises the perpetuity at the '
                    'explicit-window rate',
        alt=lambda ctx: at_rates(ctx['pu'], ctx['pn'],
                                 wacc_term=(1 - C.WD) * C.ke_rating + C.WD * C.KD_AT),
        why='a mature plant base running 9.8% net leverage is under-levered against its '
            'own sector and normalising it is the ordinary construction — but the '
            'terminal carries 56% of enterprise value here, so the choice is worth more '
            'than it looks, and it runs in the study\'s own favour.'),
    dict(
        name='the utilisation path',
        adopted='urea utilisation glides from 82.3% in 2026 to 88.8% by 2030 and merchant '
                "ammonia from 71.5% to 84.7%, on the company's stated manufacturing "
                'improvement programme, with installed capacity held flat because no '
                'additions are announced',
        alternative='utilisation held flat at the 2026 level across the whole window — no '
                    'improvement credited at all, which is what a reader who declines to '
                    'price an unquantified programme would do',
        alt=lambda ctx: with_drivers(ctx['pu'], ctx['pn'], UTIL_UREA=_UTIL_U,
                                     UTIL_NH3=_UTIL_N, vol_urea=_VU, vol_nh3=_VN,
                                     vol_own=[a + b for a, b in zip(_VU, _VN)]),
        why='the company gives no numeric volume guidance, so no guidance figure is '
            'carried and the glide is anchored on the 92% urea utilisation actually '
            'reported for the first half of 2026. It is the second most powerful driver '
            'after price and it runs in the study\'s own favour.'),
    dict(
        name='the terminal construction',
        adopted='built through the sanctioned terminal — maintenance at replacement cost '
                'over the composite 22.04-year asset life DERIVED from the company\'s own '
                'property note, with book depreciation added back',
        alternative='the retired reinvestment identity, terminal profit times one less '
                    'growth over return on capital, which charges the whole capital base '
                    'every 1/g years and so implies a fifty-year replacement cycle at a '
                    '2% terminal',
        alt=lambda ctx: bridge_ps(ctx['dcf']['pv_explicit']
                                  + ctx['dcf']['tv_retired'] * ctx['dcf']['df'][-1]),
        why='the retired construction makes the implied asset life a fact about the '
            'currency rather than about the plant. Nobody predicted which way rebuilding '
            'it would move the value and it is recorded as a measurement rather than a '
            'prediction: here it raises it, by less than the five per cent this record '
            'counts as material.'),
    dict(
        name='the cost-of-capital weights',
        adopted='struck on NET debt',
        alternative='struck on GROSS debt, which is one of the two coherent conventions '
                    "the study's own gap review names",
        alt=lambda ctx: at_rates(ctx['pu'], ctx['pn'],
                                 wacc_exp=_WE_GROSS * C.ke_rating
                                 + (1 - _WE_GROSS) * C.KD_AT),
        why='the cash lightens the debt weight, raising the rate the operations are '
            'discounted at, and then comes back a second time through the net-debt '
            'deduction in the bridge. A CONCEDED DEFECT, registered in the study\'s own '
            'records and worth about 105 basis points of cost of capital — which turns '
            'out to be under two per cent of value, so it does not reach this record\'s '
            'materiality bar. The rate effect and the value effect are different sizes '
            'and only one of them is what this record measures.'),
    dict(
        name='the forecast tax rate',
        adopted='13.1%, the mean of three independently constructed estimates — the '
                'four-year aggregate reported effective rate, the four-year aggregate '
                'cash rate and a jurisdiction-weighted statutory build',
        alternative='the four-year aggregate reported effective rate alone, 10.4%, which '
                    'is the leg a reader would compute straight off the filed statements',
        alt=lambda ctx: at_rates(ctx['pu'], ctx['pn'], tax=C.tax_agg_eff),
        why="no single reported year is usable: the group's statutory rate runs from zero "
            'to 25% on free-zone status, and the reported 4.0% in 2025 and 7.0% in 2024 '
            'were flattered by items that do not recur. The three legs span 10.4% to '
            '15.7% and the whole span is worth under four per cent of value in either '
            'direction, so the triangulation is not where this answer is decided.'),
    dict(
        name='beta',
        adopted='0.931, the point estimate from 242 weekly observations against the '
                'published index of the exchange the share is listed on, used as measured',
        alternative='0.954, the same regression adjusted toward one on the conventional '
                    'shrinkage — the alternative the study itself publishes',
        alt=lambda ctx: with_ke(ctx['pu'], ctx['pn'],
                                C.rf_star_rating + C.wacc['beta_blume'] * C.erp_rating),
        why='the regression passes the usability gate, so the point estimate is what the '
            'hierarchy takes; the fit is weak — 10.0% of variance — for an economic '
            'reason the study states plainly, and the shrinkage convention is shown '
            'rather than argued away. Worth under two per cent of value. The regression\'s '
            'own 90% interval is far wider than this and is a two-sided sensitivity, not '
            'a framing a study could adopt; it is recorded in `examined_not_priced` '
            'rather than turned into a one-sided judgement here.'),
    dict(
        name='the third-party trading margin',
        adopted='7.5% of traded revenue — the one leg not built from volume times price '
                'less cost per tonne, because no purchase-side unit economics are '
                'disclosed anywhere in any filing',
        alternative='the margin the company actually reported for the first half of 2026, '
                    '10.8%',
        alt=lambda ctx: with_drivers(ctx['pu'], ctx['pn'], TRADE_MARGIN=_M26),
        why='the disclosed segment margins run 1.9% in 2024, 3.8% in 2025 and 10.8% in '
            'the first half of 2026, so 7.5% sits inside the observed range rather than '
            'at either end. The leg is small and the whole observed span moves the value '
            'under four per cent.'),
    dict(
        name='the capital expenditure path',
        adopted='capex converges on depreciation but stays below it throughout the '
                'window, against disclosed maintenance capital expenditure of $143.6m '
                'for 2025',
        alternative='capex set equal to depreciation and amortisation in every year — '
                    'full replacement of the asset base as it is consumed',
        alt=lambda ctx: with_drivers(ctx['pu'], ctx['pn'], CAPEX=list(C.D_AND_A)),
        why='the plant base is mature and urea capacity is flat, so the company is not '
            'spending to grow — but an asset base depreciated faster than it is replaced '
            'cannot support the volume path indefinitely, which is the reading the '
            'alternative takes. Worth four per cent of value.'),
    dict(
        name='working capital and the gas accrual',
        adopted='projected from the conversion cycle with the accrual removed from '
                'payables — receivable days 64, inventory days 63, payable days 82',
        alternative='the accrual left inside payables, which puts payable days at 154 and '
                    'makes the cash conversion cycle permanently negative',
        alt=lambda ctx: with_wc_accrual_inside(ctx['pu'], ctx['pn']),
        why='the accrued gas catch-up is not a trade payable arising in the ordinary '
            'course; leaving it in would show the company financing itself on supplier '
            'credit it has not negotiated. Worth four per cent of value, and it runs '
            'against the study rather than for it.'),
    dict(
        name='terminal real growth',
        adopted='zero real growth STATED, so the terminal grows with inflation alone and '
                'is charged no growth capital',
        alternative='one point of real growth a year in perpetuity, charged the '
                    'incremental capital at replacement cost that a point of real output '
                    'needs',
        alt=lambda ctx: at_rates(ctx['pu'], ctx['pn'], real_growth=0.01),
        why='real growth is not free in the sanctioned terminal: it costs capital, and on '
            'this company\'s replacement cost a point of it costs more than it brings. So '
            'stating zero is the HIGHER value rather than the prudent one, and the axis '
            'runs downward from the study\'s own choice. Worth three per cent.'),
]


# ---------------------------------------------------------------------------
# 3. PRICE EVERY JUDGEMENT, ON BOTH BRANCHES
# ---------------------------------------------------------------------------
THRESHOLD = 0.05          # the same five per cent the gate applies
CONCEDED = {'the terminal risk-free rate', 'the cost-of-capital weights'}


def context(which):
    if which == 'A':
        return dict(pu=C.PRICE_A_UREA, pn=C.PRICE_A_NH3, ev=C.dcf_A['ev'], dcf=C.dcf_A,
                    base=A, other=B, cds=C.br_A_cds['ps_aed'])
    return dict(pu=C.PRICE_B_UREA, pn=C.PRICE_B_NH3, ev=C.dcf_B['ev'], dcf=C.dcf_B,
                base=B, other=A, cds=C.br_B_cds['ps_aed'])


def price_all(which):
    ctx = context(which)
    out = []
    for j in JUDGEMENTS:
        va, vb = float(ctx['base']), float(j['alt'](ctx))
        out.append(dict(name=j['name'], value_adopted=va, value_alternative=vb,
                        material=abs(va - vb) / (abs(vb) or 1.0) >= THRESHOLD,
                        direction='up' if va > vb else ('down' if va < vb else 'flat')))
    return out


PRICED_A, PRICED_B = price_all('A'), price_all('B')


def sign_test(rows):
    signs = [1 if r['direction'] == 'up' else -1 for r in rows
             if r['material'] and r['direction'] != 'flat']
    n, k = len(signs), len([s for s in signs if s > 0])
    if not n:
        return dict(material=0, resolved_upward=0, resolved_downward=0,
                    p_two_sided=None, flagged=False)
    tail = sum(comb(n, i) for i in range(max(k, n - k), n + 1)) / float(2 ** n)
    p = min(1.0, 2 * tail)
    return dict(material=n, resolved_upward=k, resolved_downward=n - k,
                p_two_sided=p, flagged=bool(p < 0.05 and n >= 3))


ST_A, ST_B = sign_test(PRICED_A), sign_test(PRICED_B)
ST_DEFENDED = sign_test([r for r in PRICED_A if r['name'] not in CONCEDED])

# THE CRUX FLIPS BY CONSTRUCTION AND THAT IS NOT EVIDENCE OF ANYTHING. On a two-sided
# answer the price-path entry is the A-against-B comparison itself, so whichever branch
# is the base, the other branch is "the alternative" and the direction reverses. It is
# named here so a reader does not read a definitional flip as an instability.
_CRUX = JUDGEMENTS[0]['name']
FLIPS = [dict(name=a['name'],
              on_framing_A=a['direction'], on_framing_B=b['direction'],
              material_on_A=a['material'], material_on_B=b['material'],
              definitional=(a['name'] == _CRUX))
         for a, b in zip(PRICED_A, PRICED_B) if a['direction'] != b['direction']]
SIGN_STABLE = not [f for f in FLIPS
                   if not f['definitional'] and (f['material_on_A'] or f['material_on_B'])]


# ---------------------------------------------------------------------------
# 4. NAMED AND NOT PRICED — an absent answer is not a clean one
# ---------------------------------------------------------------------------
def _refusal(**drivers):
    try:
        return 'value AED %.4f' % with_drivers(C.PRICE_A_UREA, C.PRICE_A_NH3, **drivers)
    except Exception as exc:                                            # noqa: BLE001
        return 'REFUSED by the sanctioned terminal: %s' % exc


EXAMINED_NOT_PRICED = [
    dict(
        name='the gas cost pass-through — the conflict between two company sources',
        status='named, bracketed, NOT priced',
        note='THE LARGEST UNPRICED FORK IN THE STUDY, and it is unpriced because pricing '
             'it would mean choosing a number nobody has published. The audited FY2025 '
             'segment note describes the gas offtake agreements as carrying "no/limited '
             'price exposure"; on the results call of 6 August 2026 the chief executive '
             'said the company has product-linked gas pricing in both Egypt and Algeria. '
             'Both are company sources and they cannot both describe the same '
             'arrangement. The study resolves it in favour of the call — more recent by '
             'five months, more specific, and corroborated by the $6/MMBtu delivered gas '
             'price disclosed for the second quarter and by a three-period fit of 0.960 — '
             'and calibrates the slope at 0.481 of every dollar of realised price. The '
             'accounting-note reading implies a LOWER slope, but no filing states one, so '
             'there is no alternative value to compute: inventing one to fill this cell '
             'would be worse than leaving it named. What can be reported is the study\'s '
             'own sensitivity axis, run here: a slope of 0.30 gives AED %.4f a share and '
             'a slope of 0.65 gives AED %.4f, against AED %.4f at the calibrated 0.481. '
             'Stripping the Algerian catch-up accrual moves the fitted slope only to '
             '0.489, worth AED %.4f, so the calibration is not an artefact of that item. '
             'A reader should treat this as the place where this study could be most '
             'wrong in either direction.'
             % (at_rates(C.PRICE_A_UREA, C.PRICE_A_NH3, passth=0.30),
                at_rates(C.PRICE_A_UREA, C.PRICE_A_NH3, passth=0.65), A,
                at_rates(C.PRICE_A_UREA, C.PRICE_A_NH3, passth=C.passthru_ex['slope']))),
    dict(
        name="beta's confidence interval",
        status='measured in both directions, NOT a judgement',
        note='the 90%% interval on the regression runs from 0.47 to 1.40 and is worth '
             'AED %.4f and AED %.4f a share against the point estimate\'s AED %.4f. That '
             'is enormous, and it is a two-sided SENSITIVITY rather than a framing a '
             'study could adopt: the hierarchy takes the point estimate when the '
             'regression passes its usability gate, and picking one end of an interval to '
             'record as "the alternative" would be choosing a direction rather than '
             'measuring one. The interval is published in the study\'s own sensitivity '
             'table, which is where it belongs.'
             % (with_ke(C.PRICE_A_UREA, C.PRICE_A_NH3,
                        C.rf_star_rating + C.wacc['beta_ci90'][0] * C.erp_rating),
                with_ke(C.PRICE_A_UREA, C.PRICE_A_NH3,
                        C.rf_star_rating + C.wacc['beta_ci90'][1] * C.erp_rating), A)),
    dict(
        name='the replacement cost of installed nitrogen capacity',
        status='attempted in both directions, ONE SIDE REFUSED',
        note='$1,250 a tonne sets the capital base the terminal charges maintenance on, '
             'and it is this desk\'s figure rather than a disclosed one. The only capital '
             'cost per tonne of nitrogen capacity the company itself publishes is the '
             'lower-carbon plant\'s — under $500m for one million tonnes — and the '
             'sanctioned terminal REFUSES at that level and at $1,000: the maintenance '
             'charge falls so far that terminal cash flow exceeds terminal profit and the '
             'implied payout passes one, which is a liquidation rather than a going '
             'concern. At $500/t: %s. At $1,000/t: %s. In the other direction $1,500/t '
             'gives %s. So the judgement cannot be priced downward at all and is recorded '
             'here rather than as a one-sided fork.'
             % (_refusal(REPLACEMENT_PER_T=500.0), _refusal(REPLACEMENT_PER_T=1000.0),
                _refusal(REPLACEMENT_PER_T=1500.0))),
    dict(
        name='the terminal return on capital',
        status='inert by construction',
        note='the study triangulates it — the final-year book return, the return on '
             'replacement cost and a long-run sector return — and publishes it as a '
             'diagnostic. It does NOT enter the terminal, which is built from the capital '
             'the plants need to be kept whole on the disclosed asset life, so no assumed '
             'return sets the charge. Moving it moves nothing, which is why it is not a '
             'judgement worth any percentage of value.'),
    dict(
        name='the 2026 base year',
        status='arithmetic, not judgement',
        note='the first half is the disclosed actual — 2,571kt of own-produced volume on '
             '$1,597m of segment revenue — and only the second half is modelled. The '
             "study's own judgements table records that nothing would overturn this "
             'because carrying a modelled full year over a period the company has already '
             'reported would discard evidence that exists.'),
    dict(
        name='the enterprise multiple used in the relative lens',
        status='a cross-check, not the answer',
        note='5.8 times mid-cycle EBITDA against a peer set trading from 5.2 to 10.4 '
             'times. Under the lens architecture this is published beside the cash-flow '
             'lens and never weighted into it, so moving it cannot move the answer this '
             'record measures. Book value is treated the same way, as a disclosed floor.'),
]


# ---------------------------------------------------------------------------
# 5. CONTAINMENT — asserted before anything is written
# ---------------------------------------------------------------------------
def _appears_in_numbers(value, node, trail=''):
    if isinstance(node, dict):
        for k, v in node.items():
            hit = _appears_in_numbers(value, v, trail + '/' + str(k))
            if hit:
                return hit
    elif isinstance(node, list):
        for i, v in enumerate(node):
            hit = _appears_in_numbers(value, v, trail + '[%d]' % i)
            if hit:
                return hit
    elif isinstance(node, float) and node == value:
        return trail
    return None


def main():
    solved = float(PX_LATEST['mid_cycle_urea'])
    where = _appears_in_numbers(solved, COMMITTED)
    assert where is None, (
        'the reverse read\'s own value is committed in study_numbers.json at %s. A '
        'quantity solved from the traded price must not sit in the numbers file every '
        'builder reads: that is the reverse-engineered rate arriving through a side '
        'door, and the prohibition is worth nothing if the side door is open.' % where)

    diag = {
        'ticker': 'FERTIGLOBE',
        'as_of': AS_OF,
        'spot': SPOT_LATEST,
        'spot_date': SPOT_LATEST_DATE,
        'spot_at_strike': SPOT_STRIKE,
        'published_central': A,
        'published_spot': SPOT_STRIKE,
        'published_answer_is_two_sided': {'branch_A': A, 'branch_B': B},
        'why_this_file': (
            'The reverse read — what the traded price must believe — is a DIAGNOSTIC and '
            'lives outside the numbers file every builder reads. A quantity solved from a '
            'price and then used anywhere in the valuation is the reverse-engineered rate '
            'the protocol prohibits outright, arriving through a side door. Nothing in '
            'this file is an input to anything and nothing reads it back: it is solved '
            'here by re-running the study\'s own model and written out, and '
            'diagnostics_fertiglobe.main() refuses to write if the solved value appears '
            'in study_numbers.json.'),
        'implied': {
            'quantity': (
                'the mid-cycle urea benchmark price — granular urea free on board Egypt, '
                'averaged over the last three forecast years — that reproduces the traded '
                'price on this study\'s own drivers'),
            'value': float(PX_LATEST['mid_cycle_urea']),
            'study_value': float(MID_A),
            'study_value_range': [float(MID_A), float(MID_B)],
            'company_disclosed': [float(v) for _, v in DISCLOSED],
            'company_disclosed_detail': [{'period': p, 'usd_per_tonne': float(v)}
                                         for p, v in DISCLOSED],
            'solved_on': (
                'this study\'s own model, re-run end to end at every trial price through '
                'the same build_frame -> run_dcf -> bridge chain the study publishes on. '
                'The axis is the study\'s OWN two published price paths: the solve moves '
                'along the line between framing A and framing B, and off either end if it '
                'has to, so the only quantity varied is the nitrogen price basis. Tonnes, '
                'the calibrated cost pass-through, the cost-of-capital schedule, the '
                'terminal and the bridge all stay at their published values. The bracket '
                'is asserted, so a solve that ran off its own end raises rather than '
                'returning an endpoint that looks exactly like an answer.'),
            'reading': (
                'At AED %.2f — the latest known close, 3 September 2026 — the price is '
                'paying for urea at about US$%.0f a tonne from 2028 onward, with ammonia '
                'at about US$%.0f. This study\'s framing A holds US$%.0f and its framing B '
                'US$%.0f, so the market sits within a couple of dollars of framing B and '
                'US$%.0f above framing A. The company\'s own results reports put the '
                'benchmark at US$357 in 2024, US$440 in 2025, US$637 across the first '
                'half of 2026 and US$555 in July 2026 — so the price is paying for '
                'roughly the level printing today, held for the rest of the decade, and '
                'well below the first half\'s average. THE WHOLE DISAGREEMENT IS ONE '
                'QUESTION: at AED %.2f a share this study\'s low branch asserts that '
                'nitrogen reverts toward the marginal cost of the swing supplier, and the '
                'market is not paying for that reversion. Struck instead at the study\'s '
                'own price date of 7 August 2026 (AED %.2f) the same solve gives '
                'US$%.0f a tonne.'
                % (SPOT_LATEST, PX_LATEST['mid_cycle_urea'], PX_LATEST['mid_cycle_ammonia'],
                   MID_A, MID_B, PX_LATEST['mid_cycle_urea'] - MID_A, A, SPOT_STRIKE,
                   PX_STRIKE['mid_cycle_urea'])),
        },
        'construction': {
            'at_latest_price': PX_LATEST,
            'at_strike_price': PX_STRIKE,
            'study_mid_cycle_urea': {'framing_A': float(MID_A), 'framing_B': float(MID_B)},
            'study_mid_cycle_ammonia': {
                'framing_A': mid_cycle(C.PRICE_A_NH3),
                'framing_B': mid_cycle(C.PRICE_B_NH3)},
            'mid_cycle_definition': (
                "the average of the last three forecast years, which is the study's own "
                'definition — it is what the relative lens applies its multiple to'),
            'note': ('every figure here is a full re-run of the study\'s own chain, never '
                     'an interpolation of a fixed cash-flow series'),
        },
        'second_reading_flat_discount_rate': {
            'why_kept': (
                'the price axis cannot say whether the disagreement is about the business '
                'or about the price of time. This one can, and the answer is unusually '
                'clean: on framing B the market and this study differ by %.0f basis '
                'points on a flat equivalent rate, which is nothing. The disagreement is '
                'not about risk or time — it is about the price of urea.'
                % abs(10000 * (RATE_B['implied_rate_at_price']
                               - RATE_B['implied_rate_at_study_value']))),
            'instrument': ('engine/reverse_read.py, the shared construction, so the number '
                           'is comparable with every other study rather than to this one '
                           'alone'),
            'discounting_times': _how,
            'framing_A': {'implied_by_price': RATE_A['implied_rate_at_price'],
                          'study_flat_equivalent': RATE_A['implied_rate_at_study_value'],
                          'terminal_cash_flow': RATE_A['terminal_cash_flow'],
                          'terminal_arrives_at_year': RATE_A['terminal_arrives_at_year'],
                          'enterprise_value_at_spot': RATE_A['enterprise_value_at_spot'],
                          'enterprise_value_in_study': RATE_A['enterprise_value_in_study']},
            'framing_B': {'implied_by_price': RATE_B['implied_rate_at_price'],
                          'study_flat_equivalent': RATE_B['implied_rate_at_study_value'],
                          'terminal_cash_flow': RATE_B['terminal_cash_flow'],
                          'terminal_arrives_at_year': RATE_B['terminal_arrives_at_year'],
                          'enterprise_value_at_spot': RATE_B['enterprise_value_at_spot'],
                          'enterprise_value_in_study': RATE_B['enterprise_value_in_study']},
            'study_schedule': {'explicit': C.wacc_rating, 'terminal': C.wacc_term_rating},
            'reading': (
                'On framing A the price implies a flat %.2f%% against this study\'s own '
                'flat equivalent of %.2f%% — %.0f basis points, which is a real '
                'disagreement about the price of time, and it is close to what one of '
                'the judgements below would supply on its own: pricing the equity risk '
                'premium on Abu Dhabi alone rather than on the countries the plants are '
                'in reaches AED %.4f a share against the AED %.2f close. On framing B '
                'the price implies %.2f%% against %.2f%%, a difference of %.0f basis '
                'points. A reader can therefore locate the disagreement precisely: it '
                'lives in the price path, and only secondarily in the rate.'
                % (100 * RATE_A['implied_rate_at_price'],
                   100 * RATE_A['implied_rate_at_study_value'],
                   abs(10000 * (RATE_A['implied_rate_at_price']
                                - RATE_A['implied_rate_at_study_value'])),
                   [r['value_alternative'] for r in PRICED_A
                    if r['name'] == 'the equity risk premium — which country'][0],
                   SPOT_LATEST,
                   100 * RATE_B['implied_rate_at_price'],
                   100 * RATE_B['implied_rate_at_study_value'],
                   abs(10000 * (RATE_B['implied_rate_at_price']
                                - RATE_B['implied_rate_at_study_value'])))),
        },
        'containment': {
            'solved_value_in_numbers_file': False,
            'asserted_by': ('diagnostics_fertiglobe.main(), which refuses to write if the '
                            'solved value appears in study_numbers.json'),
            'builders_reading_this_file': 'none — no builder in this directory opens it',
            'numbers_file_untouched': ('compute.py writes study_numbers.json at import, so '
                                       'its bytes are held before the import and restored '
                                       'after, asserted byte-for-byte'),
        },
    }

    cj = {
        'ticker': 'FERTIGLOBE',
        'as_of': AS_OF,
        'published_central': A,
        'published_spot': SPOT_STRIKE,
        'published_answer_is_two_sided': {'branch_A': A, 'branch_B': B},
        'why_this_file': (
            'Any single contested choice in a valuation is defensible. What is not is a '
            'study that resolves EVERY contested choice the same way and never notices. '
            'Each is recorded with BOTH framings\' values, the side adopted and why, and '
            'a two-sided binomial sign test is printed over the ones worth more than five '
            'per cent of value. A study that lands them all one way is FLAGGED, never '
            'failed — a company can genuinely deserve a consistent read. What it may not '
            'do is go unmeasured.'),
        'how_the_framings_were_valued': (
            'Every alternative below is a full re-run of the study\'s own model — '
            'build_frame, run_dcf and the study\'s own bridge — with ONE construction '
            'moved and everything else at its published value, restored afterwards. No '
            'figure here is typed, interpolated or read off a table.'),
        'which_branch_and_why': (
            'THE ANSWER IS TWO-SIDED, so every alternative has to be priced against one '
            'of the two branches, and the choice is declared rather than convenient. '
            'Framing A is the base: it is the branch this study\'s own gap review audits, '
            'the branch the repository\'s gap reader takes as the central, and the branch '
            'a reader is handed whenever one number is wanted. Every judgement was ALSO '
            'priced on framing B and the directions compared, so the base cannot be '
            'quietly doing the work — `sign_test_on_framing_B` and '
            '`sign_stable_across_branches` below report what happens if the other branch '
            'is used.'),
        'what_this_record_measures': (
            '%d judgements, %d of them worth five per cent of value or more; %d resolved '
            'toward the higher value and %d toward the lower, two-sided binomial p=%.2f. '
            'THE LEAN IS TOWARD THE LOWER VALUE AND IT IS NOT SIGNIFICANT, so the flag is '
            'not raised and the honest reading is that this study does not resolve its '
            'forks one way. Where the lean sits is worth naming, and '
            '`largest_material_each_way` carries the ordering. The biggest downward '
            'entry is the price path itself; behind it are two constructions where the '
            'study deliberately took the more expensive side of a real choice — pricing '
            'the group on the countries its plants are in rather than on its listing '
            'domicile, and deducting the minority at its share of value rather than at '
            'book. The biggest upward entries are operating and balance-sheet ones: the '
            'utilisation glide, the unsettled gas accrual left out of the bridge, and '
            'terminal leverage normalised to the sector. ONE MATERIAL ENTRY IS A '
            'CONCEDED DEFECT RATHER THAN A '
            'DEFENDED FORK (the terminal risk-free rate, named in the study\'s own gap '
            'review and registered for a later cost-of-capital pass); the other conceded '
            'construction, the net-debt weighting, turns out to be worth under two per '
            'cent of value and never reaches the test at all. Without both, p=%.2f — the '
            'answer does not turn on them. THE LARGEST FORK IN THE STUDY IS NOT IN THIS '
            'LIST: the gas cost pass-through is named in `examined_not_priced`, because '
            'the alternative reading of it is a conflict between two company sources and '
            'neither of them states a number, so pricing it would have meant inventing '
            'one.'
            % (len(JUDGEMENTS), ST_A['material'], ST_A['resolved_upward'],
               ST_A['resolved_downward'], ST_A['p_two_sided'],
               ST_DEFENDED['p_two_sided'])),
        'largest_material_each_way': {
            'downward': [dict(name=r['name'],
                              value_adopted=r['value_adopted'],
                              value_alternative=r['value_alternative'])
                         for r in sorted([x for x in PRICED_A
                                          if x['material'] and x['direction'] == 'down'],
                                         key=lambda x: x['value_alternative']
                                         - x['value_adopted'], reverse=True)[:3]],
            'upward': [dict(name=r['name'],
                            value_adopted=r['value_adopted'],
                            value_alternative=r['value_alternative'])
                       for r in sorted([x for x in PRICED_A
                                        if x['material'] and x['direction'] == 'up'],
                                       key=lambda x: x['value_adopted']
                                       - x['value_alternative'], reverse=True)[:3]],
        },
        'judgements': [],
        'sign_test': ST_A,
        'sign_test_excluding_conceded_defects': dict(
            ST_DEFENDED, excluded=sorted(CONCEDED),
            note='a conceded defect is a choice standing at the lower value for a stated '
                 'reason rather than a framing the study defends; both readings are '
                 'printed so nobody has to take this record\'s word for which is fair'),
        'sign_test_on_framing_B': ST_B,
        'sign_stability_across_branches': {
            'stable_on_material_judgements': SIGN_STABLE,
            'flips': FLIPS,
            'note': (
                'Every judgement was priced on BOTH branches so the choice of base could '
                'be checked rather than trusted. Three entries change direction. The '
                'price path itself is DEFINITIONAL — on a two-sided answer that entry is '
                'the A-against-B comparison, so it reverses whichever branch is the base, '
                'and reading that as instability would be reading the arithmetic of the '
                'record rather than the study. Terminal real growth flips and is '
                'immaterial on both branches, so it never enters the test. THE ONE THAT '
                'MATTERS IS THE LENS ARCHITECTURE: the retired blend pulls toward the '
                'cross-checks, which sit between the two branches, so it RAISES the low '
                'branch and LOWERS the high one. That is a real fact about the '
                'construction and is why it is reported rather than smoothed — the '
                'blend does not lean in a direction, it leans toward the middle, and the '
                'study publishes the two ends instead.'),
        },
        'examined_not_priced': EXAMINED_NOT_PRICED,
    }

    for spec, a_row, b_row in zip(JUDGEMENTS, PRICED_A, PRICED_B):
        cj['judgements'].append({
            'name': spec['name'],
            'adopted': spec['adopted'],
            'alternative': spec['alternative'],
            'value_adopted': a_row['value_adopted'],
            'value_alternative': a_row['value_alternative'],
            'why': spec['why'],
            'material': a_row['material'],
            'direction': a_row['direction'],
            'on_framing_B': {'value_adopted': b_row['value_adopted'],
                             'value_alternative': b_row['value_alternative'],
                             'material': b_row['material'],
                             'direction': b_row['direction']},
            'conceded_defect': spec['name'] in CONCEDED,
        })

    with open(os.path.join(HERE, 'diagnostics.json'), 'w', encoding='utf-8') as fh:
        json.dump(diag, fh, indent=1, ensure_ascii=False)
    with open(os.path.join(HERE, 'contested_judgements.json'), 'w', encoding='utf-8') as fh:
        json.dump(cj, fh, indent=1, ensure_ascii=False)

    assert open(NUM, 'rb').read() == _BYTES, 'study_numbers.json was modified'

    print('FERTIGLOBE reverse read — at AED %.2f the price pays for mid-cycle urea of '
          'US$%.2f/t against the study\'s US$%.2f (A) and US$%.2f (B)'
          % (SPOT_LATEST, PX_LATEST['mid_cycle_urea'], MID_A, MID_B))
    print('  second reading: flat rate %.2f%% (A) / %.2f%% (B) against %.2f%% / %.2f%%'
          % (100 * RATE_A['implied_rate_at_price'], 100 * RATE_B['implied_rate_at_price'],
             100 * RATE_A['implied_rate_at_study_value'],
             100 * RATE_B['implied_rate_at_study_value']))
    print('  sign test: %d judgements, %d material, %d up / %d down, p=%.4f%s'
          % (len(JUDGEMENTS), ST_A['material'], ST_A['resolved_upward'],
             ST_A['resolved_downward'], ST_A['p_two_sided'],
             '  FLAGGED' if ST_A['flagged'] else ''))
    print('  excluding the two conceded defects: %d material, p=%.4f'
          % (ST_DEFENDED['material'], ST_DEFENDED['p_two_sided']))
    print('  on framing B: %d material, %d up / %d down, p=%.4f; stable on material '
          'judgements: %s (%d flips, %d definitional)'
          % (ST_B['material'], ST_B['resolved_upward'], ST_B['resolved_downward'],
             ST_B['p_two_sided'], SIGN_STABLE, len(FLIPS),
             len([f for f in FLIPS if f['definitional']])))
    for r in PRICED_A:
        print('   %-62s %7.4f vs %7.4f  %-5s %s'
              % (r['name'][:62], r['value_adopted'], r['value_alternative'],
                 r['direction'], 'MATERIAL' if r['material'] else ''))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
