#!/usr/bin/env python3
"""EMPOWER — the two output records [R-ENF-05], COMPUTED rather than remembered.

WHAT THIS WRITES. diagnostics.json and contested_judgements.json, both read by an outside
gate and by nobody else. An artefact every reader reads and nothing writes is a number
frozen at the date somebody last typed it [R-ENF-06], so both are generated here, from
this study's own model, at every run.

THE REVERSE READ, AND WHY THE QUANTITY IS THE CONNECTION PIPELINE. This study states what
IT believes and nowhere states what the PRICE believes, and the two are the same model
read backwards. The quantity has to be one a reader can CHECK, and on a district-cooling
network that is CONNECTED CAPACITY: the company discloses it every year, guides it for the
year ahead, and publishes a contracted-but-not-yet-connected book beside it. So the
headline solve is the average annual CHANGE in connected capacity, in thousand
refrigeration tonnes, that makes this study's own published central reproduce the traded
price — every other driver held exactly where the study published it.

THE OBVIOUS ALTERNATIVE QUANTITY IS SOLVED BESIDE IT AND IS NOT THE HEADLINE. The flat
discount rate is the number comparable across the book, and it is reported; it is not the
headline because no disclosure of this company's cost of capital exists to check it
against, while three independent disclosures bear on the pipeline.

THE SHARED INSTRUMENT (engine/reverse_read.py) IS DELIBERATELY NOT CALLED FOR THAT RATE.
It recovers the terminal cash flow by the identity TV = FCFF/(WACC - g). THIS STUDY'S
TERMINAL IS TWO-STAGE — ten explicit fade years and then a perpetuity — so that identity
does not hold here, and using it would put a real error into the answer while looking
exactly like a comparable number. The rate is therefore solved by re-running compute.dcf()
itself, which is the same model read backwards rather than a second model.

THE SOLVE MOVES ONE THING. compute.py is IMPORTED and its own functions called, never
re-implemented: a reverse read on a re-implementation grades a different model. Every
helper below asserts that it reproduces the study's published figure before it is used to
produce anything else.

IT IS A DIAGNOSTIC AND NOTHING READS IT BACK. A quantity solved from a price and then used
in the valuation is the reverse-engineered rate the protocol prohibits outright, arriving
through a side door. assert_reverse_dcf() refuses any study whose builders read this file;
this generator additionally (i) asserts before writing that no solved value appears
anywhere in study_numbers.json, and (ii) restores study_numbers.json byte-for-byte if
importing the model moved it, so running the diagnostic cannot move the valuation.

THE SIGN TEST. Any single contested choice is defensible; a study resolving every one of
them the same way and never noticing is not. Every alternative below is priced by
RE-RUNNING this study's own model with that one choice changed and everything else held.

MATERIALITY IS MEASURED ON THE PUBLISHED ANSWER, WHICH IS THE FOUR-LENS BLEND, and that
DAMPENS every fork that touches only the cash-flow lens by about half. Nothing is hidden
by it: each judgement also carries its value on the primary lens alone, so a reader can
see which forks the blend is muffling and by how much.

    python3 diagnostics_empower.py      writes diagnostics.json + contested_judgements.json
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))

NUMBERS = os.path.join(HERE, 'study_numbers.json')
_BEFORE = open(NUMBERS, 'rb').read()

import compute as C                                                     # noqa: E402
import terminal_value as TERMVAL                                        # noqa: E402

# (ii) the model is deterministic and rebuilds the numbers file unchanged; if it ever
# stops being, this diagnostic must not be the thing that moves a delivered artefact.
if open(NUMBERS, 'rb').read() != _BEFORE:
    open(NUMBERS, 'wb').write(_BEFORE)
    raise SystemExit('REFUSED: importing the model moved study_numbers.json. Restored. '
                     'A diagnostic may not move the valuation it is measuring.')

V, W = C.V, C.WACC
SPOT = float(V['spot'])
NCI_KEEP = 1.0 - V['nci_pat_fy25'] / V['pat_fy25']
BRIDGE = V['recv_jun26'] + V['invprop_jun26'] + V['fvtpl_jun26'] + V['fvoci_jun26']
RT_ADDS = [105.0, 100.0, 90.0, 80.0, 70.0]          # the published connection pipeline
RT0, RTA0 = dict(C.rt_path), dict(C.rt_avg)
YRS = C.YRS_F


# --------------------------------------------------------------------------------------
# helpers, each asserted against the study's OWN published figure before use
# --------------------------------------------------------------------------------------
def ps_from_ev(ev, bridge=None):
    """This study's own enterprise-to-equity bridge, per share."""
    bridge = BRIDGE if bridge is None else bridge
    return (ev - C.net_debt + bridge) * NCI_KEEP / V['shares_mn']


def blend(dcf_ps, rel=None, norm=None, book=None):
    """This study's own published central: the four lenses at the weights it publishes."""
    return (0.50 * dcf_ps
            + 0.20 * (C.ps_rel if rel is None else rel)
            + 0.15 * (C.ps_norm if norm is None else norm)
            + 0.15 * (C.ps_book if book is None else book))


def lenses_at_ke(ke):
    """The two cost-of-equity-driven lenses, on this study's own expressions."""
    pe_j = (1.0 - C.rr_eq) / (ke - V['g_term'])
    pb_j = (C.roe_sust - V['g_term']) / (ke - V['g_term'])
    return C.eps_norm * pe_j, C.bvps * pb_j


assert abs(ps_from_ev(C.D_base_ct['ev']) - C.D_base_ct['ps']) < 1e-13, 'bridge unfaithful'
assert abs(blend(C.D_base_ct['ps']) - C.central_ct) < 1e-13, 'blend unfaithful'
_n, _b = lenses_at_ke(C.ke_rating)
assert abs(_n - C.ps_norm) < 1e-12 and abs(_b - C.ps_book) < 1e-12, 'ke lenses unfaithful'

ADOPTED = float(C.central_ct)            # recovery consumption / 9% corporate rate
ADOPTED_PRIMARY = float(C.D_base_ct['ps'])


# --------------------------------------------------------------------------------------
# THE REVERSE READ — the connection pipeline the price is paying for
# --------------------------------------------------------------------------------------
def at_pipeline(scale, floor_capex=False):
    """The study's own published central with ONLY the connection pipeline moved.

    `floor_capex` holds capital expenditure at the maintenance charge instead of letting
    the study's own per-tonne capex driver run negative on a shrinking network. The
    unfloored run CREDITS a shrinking company with releasing growth capital, which a
    chilled-water network cannot do, and that credit makes the implied shrinkage look
    LARGER than it is — so the floored figure is the conservative statement of it and
    both are published.
    """
    path, prev = {'FY25': C.rt25}, C.rt25
    for y, add in zip(YRS, RT_ADDS):
        prev += add * scale
        path[y] = prev
    C.rt_path.clear(); C.rt_path.update(path)
    C.rt_avg.clear()
    prev = path['FY25']
    for y in YRS:
        C.rt_avg[y] = (prev + path[y]) / 2.0
        prev = path[y]
    try:
        rev, cons, cap, pipes = C.revenue_path('base')
        eb, ew, oc, ga, intco, oi = C.ebitda_build(rev, cons)
        ppe, dna, capex = C.capital_block(rev)
        if floor_capex:
            ppe2, capex2, open_ = {}, {}, C.PPE25
            for y in YRS:
                capex2[y] = max(capex[y], C.MAINT_PCT * open_)
                ppe2[y] = open_ + capex2[y] - (dna[y] - C.AMORT_FLAT)
                open_ = ppe2[y]
            ppe, capex = ppe2, capex2
        nwc, dnwc = C.nwc_block(rev)
        D = C.dcf(rev, eb, dna, capex, dnwc, V['tax_ct'], W['rating_ct'],
                  'pipeline', ppe_d=ppe, nwc_d=nwc)
        # the normalised-earnings lens moves with the pipeline too; the relative and book
        # lenses do not, so they stay exactly where the study published them
        rev_n = C.cons_per_rt25 * C.rt_avg['FY26'] + cap['FY26'] + V['pipes_rev_fy25']
        eb_n = (rev_n + intco['FY26'] + V['rental_fy25']
                - C.EW_RATIO * C.cons_per_rt25 * C.rt_avg['FY26']
                - oc['FY26'] - ga['FY26'] + C.OI_OP)
        npa_n = ((eb_n - dna['FY26'] + C.fin_net26) * (1 - V['tax_ct'])) * NCI_KEEP
        norm = (npa_n / V['shares_mn']) * C.pe_just
    finally:
        C.rt_path.clear(); C.rt_path.update(RT0)
        C.rt_avg.clear(); C.rt_avg.update(RTA0)
    return blend(D['ps'], norm=norm), D['ps'], path


assert abs(at_pipeline(1.0)[0] - ADOPTED) < 1e-12, 'pipeline solver unfaithful'
assert abs(at_pipeline(1.0)[1] - ADOPTED_PRIMARY) < 1e-12, 'pipeline solver unfaithful'


def bisect(target, fn, lo=-3.0, hi=3.0, n=200):
    """Monotone in the pipeline above the shrinkage floor, so the root is unique and the
    answer cannot depend on where the search began."""
    for _ in range(n):
        mid = 0.5 * (lo + hi)
        if fn(mid) < target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def annual(path):
    return (path['FY30'] - C.rt25) / float(len(YRS))


s_blend = bisect(SPOT, lambda x: at_pipeline(x)[0])
s_floor = bisect(SPOT, lambda x: at_pipeline(x, floor_capex=True)[0])
s_prim = bisect(SPOT, lambda x: at_pipeline(x)[1])
IMPLIED = annual(at_pipeline(s_blend)[2])
IMPLIED_FLOOR = annual(at_pipeline(s_floor, floor_capex=True)[2])
IMPLIED_PRIM = annual(at_pipeline(s_prim)[2])
STUDY_PIPE = annual(RT0)

# the flat discount rate, for comparability across the book — solved on the study's own
# chain, which already runs ONE flat rate (no glide: the dirham is pegged, so the
# explicit-window rate and the terminal rate are the same number and the study says so)
IMPLIED_RATE = bisect(
    -SPOT,
    lambda w: -blend(C.dcf(C.rev_b, C.eb_b, C.dna_b, C.capex_b, C.dnwc_b,
                           V['tax_ct'], w, 'rate')['ps']),
    0.0765, 0.40)
IMPLIED_RATE_PRIM = bisect(
    -SPOT,
    lambda w: -C.dcf(C.rev_b, C.eb_b, C.dna_b, C.capex_b, C.dnwc_b,
                     V['tax_ct'], w, 'rate')['ps'],
    0.0765, 0.40)

CONN = V['rt_conn']
H1_ADDS = CONN['H1_2026'] - CONN['2025']
BACKLOG = V['rt_contracted'] - CONN['H1_2026']


# --------------------------------------------------------------------------------------
# THE CONTESTED JUDGEMENTS — each priced by re-running the study's own model
# --------------------------------------------------------------------------------------
J = []


def add(name, adopted, alternative, blend_alt, primary_alt, why):
    J.append({
        'name': name, 'adopted': adopted, 'alternative': alternative,
        'value_adopted': ADOPTED, 'value_alternative': float(blend_alt),
        'value_adopted_primary_lens': ADOPTED_PRIMARY,
        'value_alternative_primary_lens': float(primary_alt),
        'moves_the_answer_by': abs(ADOPTED - float(blend_alt)) / abs(float(blend_alt)),
        'direction': 'the study took the higher value' if ADOPTED > blend_alt
                     else 'the study took the lower value',
        'why': why})


# 1 — the central lens architecture
add('the construction of the central',
    'a weighted blend of four lenses at typed weights, 50/20/15/15',
    'the cash-flow lens alone as the class primary, the other three published beside it '
    'as cross-checks',
    C.D_base_ct['ps'], C.D_base_ct['ps'],
    'the weights were typed and have never cleared any out-of-sample test, and three of '
    'the four lenses read this business off reported earnings, historical-cost book and a '
    'war-discounted peer group rather than valuing it; the house standard [R-LENS-03] '
    'makes the class primary the central and publishes the rest beside it. The adopted '
    'construction is both the retired one and the lower one, and it is what the delivered '
    'edition publishes, so it is recorded as adopted rather than as corrected.')

# 2 — the tax framing
add('whether the minimum top-up tax reaches the group',
    'published BOTH ways and never averaged; the 9% audited effective rate is the branch '
    'this record is measured against',
    'the 15% domestic minimum top-up rate as the single answer',
    C.central_dmtt, C.D_base_dmtt['ps'],
    '9% is the audited 2025 effective rate and 15% is the top-up that would apply if the '
    'group is consolidated into its parent for the global minimum tax; the determination '
    'has not been made about this group, so neither branch can be settled from what is '
    'disclosed, and averaging them describes a company that pays 12%, which no rule '
    'provides for.')

# 3 — the beta's regressor
_n_dfm, _b_dfm = lenses_at_ke(C.ke_dfm)
add("the index the beta is regressed against",
    'the FTSE ADX General index, the registered regressor for names listed on the Dubai '
    'market, beta 0.863',
    'the DFM General index, held in the repository and deliberately not registered, '
    'beta 0.652',
    blend(C.D_base_dfm['ps'], norm=_n_dfm, book=_b_dfm), C.D_base_dfm['ps'],
    'the exchange resolver registers FTSE ADX General for Dubai-listed names as a '
    'LABELLED interim and the DFM General series is held unregistered, so the adopted '
    'regressor is the one the method requires rather than the one this desk preferred. It '
    'is also much the more punitive of the two, and the study prices the declined index as '
    'a full parallel valuation rather than mentioning it.')

# 4 — the cost-of-capital weights
add('the weights in the cost of capital',
    'net-debt target weights at the company policy structure, cost of debt at the '
    'facility rate',
    'gross-debt weights, the standard textbook frame',
    blend(C.D_base_gross['ps']), C.D_base_gross['ps'],
    'the company runs a stated policy leverage and pays out roughly its free cash flow to '
    'equity, so the cash pile is transient and net weights describe the structure it '
    'actually holds; the gross frame is priced rather than argued away.')

# 5 — the date the peer marks are struck at
_mult_jun = C.TABREED_EV_EBITDA / (2.46 / 2.72)
_ps_rel_jun = ((_mult_jun * C.ebitda_trail - C.net_debt + BRIDGE)
               * NCI_KEEP / V['shares_mn'])
add('the date the peer multiples are struck at',
    "the subject's own anchor date, at which the primary peer closed 2.46",
    'the earlier marks the first edition carried, at which the same peer closed 2.72',
    blend(ADOPTED_PRIMARY, rel=_ps_rel_jun), ADOPTED_PRIMARY,
    'a relative lens compares two prices, so both must be read on the same day; the peer '
    'had fallen 9.6% between the two dates and restriking at the anchor is the like-for-'
    'like reading, which is also the lower one.')

# 6 — the cost of net debt
add('the cost carried on net debt',
    'the marginal facility rate on borrowings',
    'a blended cost of NET debt, charging the negative carry on the cash pile',
    blend(C.D_base_carry['ps']), C.D_base_carry['ps'],
    'the deposit yield sits below the borrowing rate, so netting the two raises the cost '
    'of the net position; the study discounts at the facility rate and prices the carry '
    'construction beside it.')

# 7 — the consumption crux
add('whether consumption recovers or the loss is structural',
    'published BOTH ways as equals; the recovery case is the branch this record is '
    'measured against',
    'the continuation case, in which usage per connected tonne never recovers',
    # the study's own expression for the continuation central: only the cash-flow
    # lens moves, because the other three do not read the shocked consumption path
    C.central_ct - 0.5 * (C.D_base_ct['ps'] - C.D_pers_ct['ps']), C.D_pers_ct['ps'],
    'the recovery requires a de-escalation that had not occurred at the anchor date, so '
    'the continuation case is published as an equal rather than beneath it as a '
    'sensitivity; the pass-through structure means the whole question is worth under two '
    'per cent of the answer, which is itself the finding.')

# 8 — the related-party receivables
_eb_alt = {y: C.eb_b[y] + C.intco_b[y] for y in YRS}
_D_recv = C.dcf(C.rev_b, _eb_alt, C.dna_b, C.capex_b, C.dnwc_b, V['tax_ct'],
                W['rating_ct'], 'recv')
_ps_recv = ps_from_ev(_D_recv['ev'], bridge=BRIDGE - V['recv_jun26'])
add('how the related-party acquisition receivables are carried',
    'the interest they earn is OUTSIDE operating cash flow and the balance is added at '
    'book in the bridge',
    'the interest is capitalised INSIDE operating cash flow and no balance is added back',
    blend(_ps_recv), _ps_recv,
    'the receivables are a financial asset rather than an operating one, so capitalising '
    'their interest inside an operating multiple and then adding the principal would '
    'count them twice; carrying them at book is the cleaner treatment and, on this '
    'balance, also the lower one.')

# 9 — working capital
_D_nwc = C.dcf(C.rev_b, C.eb_b, C.dna_b, C.capex_b, {y: 0.0 for y in YRS}, V['tax_ct'],
               W['rating_ct'], 'nwcflat', nwc_d={y: C.NWC25 for y in YRS})
add('whether the negative working capital keeps releasing cash',
    'net working capital held at its filed ratio to revenue, so growth keeps releasing '
    'cash',
    'net working capital frozen at its filed absolute level, so growth releases nothing '
    'further',
    blend(_D_nwc['ps']), _D_nwc['ps'],
    'customer deposits and payment terms to the related-party supplier fund the cycle and '
    'have scaled with revenue across the filed record, so the ratio is the disclosed '
    'behaviour rather than an assumption; freezing it is the more cautious reading and is '
    'priced.')

# 10 — the age of the depreciable base
_orig_build = TERMVAL.build
AGE_MEASURED = 10.29


def _aged(inp):
    inp.average_age_years = AGE_MEASURED
    inp.average_age_source = ('Audited consolidated financial statements for the year '
                              'ended 31 December 2025, notes 5, 6 and 7 — gross cost over '
                              "the year's own charge, an identity, labelled as derived")
    return _orig_build(inp)


TERMVAL.build = _aged
C.TERMVAL.build = _aged
try:
    _D_age = C.dcf(C.rev_b, C.eb_b, C.dna_b, C.capex_b, C.dnwc_b, V['tax_ct'],
                   W['rating_ct'], 'age')
finally:
    TERMVAL.build = _orig_build
    C.TERMVAL.build = _orig_build
assert abs(C.dcf(C.rev_b, C.eb_b, C.dna_b, C.capex_b, C.dnwc_b, V['tax_ct'],
                 W['rating_ct'], 'x')['ps'] - ADOPTED_PRIMARY) < 1e-13, 'not reverted'
add('the age of the depreciable base the maintenance charge escalates over',
    'half the derived 28.10-year life, 14.05 years',
    "the 10.29 years the notes' own cost and charge columns measure",
    blend(_D_age['ps']), _D_age['ps'],
    'the measured identity returns an age only where the annual charge is cost divided by '
    'life, and the policy note states the charge is struck on cost LESS a residual, so '
    '10.29 years overstates the age rather than measuring it; the adopted figure is an '
    'assumption, is labelled as one, and is the more punitive of the two.')

# 11 — the capital a unit of real growth needs
_ob = TERMVAL.build


def _mk(inc):
    def _b(i):
        if i.incremental_capital_per_unit_growth not in (0.0, None):
            i.incremental_capital_per_unit_growth = inc
        return _ob(i)
    return _b


TERMVAL.build = _mk(C.D_base_ct['inc_cap_marginal'])
C.TERMVAL.build = TERMVAL.build
try:
    _D_inc = C.dcf(C.rev_b, C.eb_b, C.dna_b, C.capex_b, C.dnwc_b, V['tax_ct'],
                   W['rating_ct'], 'inc')
finally:
    TERMVAL.build = _ob
    C.TERMVAL.build = _ob
assert abs(C.dcf(C.rev_b, C.eb_b, C.dna_b, C.capex_b, C.dnwc_b, V['tax_ct'],
                 W['rating_ct'], 'x')['ps'] - ADOPTED_PRIMARY) < 1e-13, 'not reverted'
add('the capital a unit of real growth is charged for',
    'the capital intensity the business already runs at, the terminal invested capital',
    'the marginal reading used elsewhere in this programme, which comes out NEGATIVE here',
    blend(_D_inc['ps']), _D_inc['ps'],
    'over these five years the existing plant is written down faster than capital '
    'expenditure replaces it and the working capital is negative and growing, so the '
    'marginal reading CREDITS the company for growing — which a chilled-water network '
    'cannot do, because another unit of demand needs another plant. The adopted reading '
    'charges more and is worth about four tenths of a per cent.')

# 12 — terminal real growth
_g = (V['g1_real'], V['g2_real'], V['g_term'], V['g_term2'])
V['g1_real'] = V['g2_real'] = 0.0
V['g_term'] = V['g_term2'] = C.PI_TERM
try:
    _D_g = C.dcf(C.rev_b, C.eb_b, C.dna_b, C.capex_b, C.dnwc_b, V['tax_ct'],
                 W['rating_ct'], 'g0')
    _pe0 = (1 - V['g_term'] / C.roe_sust) / (C.ke_rating - V['g_term'])
    _pb0 = (C.roe_sust - V['g_term']) / (C.ke_rating - V['g_term'])
    _blend_g = blend(_D_g['ps'], norm=C.eps_norm * _pe0, book=C.bvps * _pb0)
finally:
    V['g1_real'], V['g2_real'], V['g_term'], V['g_term2'] = _g
assert abs(C.dcf(C.rev_b, C.eb_b, C.dna_b, C.capex_b, C.dnwc_b, V['tax_ct'],
                 W['rating_ct'], 'x')['ps'] - ADOPTED_PRIMARY) < 1e-13, 'not reverted'
add('the real growth carried into the terminal',
    'a fade at +0.49% real for ten years and then a perpetuity at -0.49% real',
    'zero real growth in both stages, the house default',
    _blend_g, _D_g['ps'],
    'the regulated tariff carries no indexation, so nominal growth here IS volume growth '
    'and the perpetuity is a stated real DECLINE rather than a rounding of zero; on the '
    'cash-flow lens alone the adopted reading is the lower one by two per cent, and the '
    'blend muffles it because the same rate raises the two lenses that capitalise '
    'earnings.')

# 13 — the equity risk premium basis
_n_cds, _b_cds = lenses_at_ke(C.ke_cds)
add('the basis the equity risk premium is built on',
    'the credit-rating basis',
    'the credit-default-swap basis, the market\'s own live pricing of the sovereign',
    blend(C.D_base_cds['ps'], norm=_n_cds, book=_b_cds), C.D_base_cds['ps'],
    'both are computed and they converge to within thirty basis points of cost of equity, '
    'which is the useful finding: on this sovereign the choice is worth about half a per '
    'cent and neither basis is doing any work.')

# 14 — the terminal construction
_ev_ret = C.D_base_ct['pv_explicit'] + C.D_base_ct['tv_retired'] * C.D_base_ct['df']['FY30']
add('the construction of the terminal',
    'capital maintenance at replacement cost on a life derived from the audited notes',
    'the retired form, charging reinvestment as growth over the return on capital',
    blend(ps_from_ev(_ev_ret)), ps_from_ev(_ev_ret),
    'the retired identity implies rebuilding the whole capital base every 1/g years — '
    'fifty in the fade and sixty-seven in the perpetuity — which is a fact about the '
    "dirham's peg rather than about a chilled-water plant the company's own notes turn "
    'over in 28.10 years. On this name the two constructions land within a fifth of a per '
    'cent of each other, which is worth recording precisely because it is the exception.')

# 15 — the size of the 2026 consumption shock
def _shocked(sh):
    ca = {y: C.cons_per_rt25 for y in YRS}
    ca['FY26'] = C.cons_per_rt25 * (1 + sh)
    rev = {y: ca[y] * C.rt_avg[y] + C.cap_per_rt25 * C.rt_avg[y] + V['pipes_rev_fy25']
           for y in YRS}
    cons = {y: ca[y] * C.rt_avg[y] for y in YRS}
    eb, *_ = C.ebitda_build(rev, cons)
    nwc, dnwc = C.nwc_block(rev)
    return C.dcf(rev, eb, C.dna_b, C.capex_b, dnwc, V['tax_ct'], W['rating_ct'],
                 'shock', nwc_d=nwc)


assert abs(_shocked(C.CRUX_SHOCK)['ps'] - ADOPTED_PRIMARY) < 1e-13, 'shock helper unfaithful'
_D_sh = _shocked(-0.09)
add('the size of the 2026 consumption shock',
    'a 6% full-year fall in usage per connected tonne',
    'the 9% fall in equivalent full-load hours the first half actually printed, carried '
    'across the full year',
    blend(_D_sh['ps']), _D_sh['ps'],
    'the second half of 2025 was itself already soft, so the full-year fall against a '
    'full-year base is smaller than the half-on-half print. The deeper shock is worth two '
    'hundredths of a per cent and comes out marginally HIGHER, which is an artefact rather '
    'than economics: the valuation clock counts 2026 as a half-year stub, so half of that '
    "year's working-capital movement is counted and its mirror in 2027 is counted whole.")

# 16 — the basis the revenue split is struck on
_cons_alt = 0.49 * V['rev_fy25']
_cpr_alt = _cons_alt / C.rt_avg25
_capr_alt = (V['rev_fy25'] - _cons_alt - V['pipes_rev_fy25']) / C.rt_avg25
_ew0 = C.EW_RATIO
C.EW_RATIO = V['ew_cost_fy25'] / _cons_alt
try:
    _ca = {y: _cpr_alt for y in YRS}
    _ca['FY26'] = _cpr_alt * (1 + C.CRUX_SHOCK)
    _rev_s = {y: _ca[y] * C.rt_avg[y] + _capr_alt * C.rt_avg[y] + V['pipes_rev_fy25']
              for y in YRS}
    _cons_s = {y: _ca[y] * C.rt_avg[y] for y in YRS}
    _eb_s, *_ = C.ebitda_build(_rev_s, _cons_s)
    _nwc_s, _dnwc_s = C.nwc_block(_rev_s)
    _D_sp = C.dcf(_rev_s, _eb_s, C.dna_b, C.capex_b, _dnwc_s, V['tax_ct'],
                  W['rating_ct'], 'split', nwc_d=_nwc_s)
finally:
    C.EW_RATIO = _ew0
add('the basis the two-leg revenue split is struck on',
    "the audited key-audit-matter figures, which put consumption at 56.3% of 2025 revenue",
    "the first-half earnings deck's 49% consumption share",
    blend(_D_sp['ps']), _D_sp['ps'],
    'the second half carries the summer cooling peak, so a full-year share always runs '
    'above a first-half share and the two are not the same measurement; the audited basis '
    'is the right one and the choice turns out to be worth a hundredth of a per cent, '
    'because the pass-through ratio moves with the split and offsets it.')

# --------------------------------------------------------------------------------------
# (i) containment: no solved value may sit in the numbers file every builder reads
# --------------------------------------------------------------------------------------
_doc = json.load(open(NUMBERS, encoding='utf-8'))


def _hunt(node, needle, trail=''):
    if isinstance(node, dict):
        for k, v in node.items():
            r = _hunt(v, needle, trail + '/' + str(k))
            if r:
                return r
    elif isinstance(node, list):
        for i, v in enumerate(node):
            r = _hunt(v, needle, trail + '[%d]' % i)
            if r:
                return r
    elif isinstance(node, float) and node == needle:
        return trail
    return None


for _name, _val in (('implied pipeline', IMPLIED), ('floored', IMPLIED_FLOOR),
                    ('primary-lens pipeline', IMPLIED_PRIM),
                    ('implied rate', IMPLIED_RATE), ('implied rate, primary lens',
                                                     IMPLIED_RATE_PRIM)):
    _where = _hunt(_doc, _val)
    assert _where is None, (
        'the %s solved from the traded price is committed in study_numbers.json at %s. A '
        'quantity solved from a price must not sit in the file every builder reads.'
        % (_name, _where))

# --------------------------------------------------------------------------------------
# write
# --------------------------------------------------------------------------------------
WHY = ('The reverse read — what the traded price must believe — is a DIAGNOSTIC and lives '
       'outside the numbers file every builder reads. A quantity solved from a price and '
       'then used anywhere in the valuation is the reverse-engineered rate the protocol '
       'prohibits outright, arriving through a side door. Nothing in this file is an '
       'input to anything: no builder in this study reads it, this generator asserts '
       'before writing that none of its solved values appears in study_numbers.json, and '
       'it restores that file byte-for-byte if importing the model moves it.')

diag = {
    'ticker': 'EMPOWER',
    'as_of': V['spot_date'] if 'spot_date' in V else C.INP['spot']['date'],
    'spot': SPOT,
    'spot_date': C.INP['spot']['date'],
    'published_central': ADOPTED,
    'published_spot': SPOT,
    'published_branches': [b['value'] for b in
                           json.loads(json.dumps(_doc['central_two_sided']['branches']))],
    'why_this_file': WHY,
    'implied': {
        'quantity': ('the average annual change in connected capacity, thousand '
                     'refrigeration tonnes a year, over the explicit window'),
        'value': float(IMPLIED),
        'study_value': float(STUDY_PIPE),
        'value_capex_floored': float(IMPLIED_FLOOR),
        'value_primary_lens_only': float(IMPLIED_PRIM),
        'company_disclosed': {
            'guidance_2026_additions_k_rt': list(V['rt_guid_2026']),
            'first_half_2026_additions_k_rt': float(H1_ADDS),
            'first_half_2026_annualised_k_rt': float(2 * H1_ADDS),
            'connected_capacity_k_rt_by_year': dict(CONN),
            'contracted_not_yet_connected_k_rt': float(BACKLOG)},
        'solved_on': (
            "this study's own model, by importing compute.py and calling its own "
            "revenue_path, ebitda_build, capital_block, nwc_block and dcf, holding every "
            "driver at its published value and moving only the connection pipeline until "
            "the published four-lens central reproduces the traded price; the solver is "
            "asserted to reproduce the published central and the published cash-flow lens "
            "exactly at the published pipeline before it is used to solve anything"),
        'value_other_framing': float(IMPLIED_RATE),
        'study_value_other_framing': float(W['rating_ct']),
        'other_framing_quantity': (
            'the single flat discount rate reproducing the price on the same model — this '
            'study already runs one flat rate, because the dirham is pegged and the '
            'explicit-window and terminal rates are the same number. Solved by re-running '
            "the study's own dcf() rather than through the shared instrument, whose "
            'terminal identity TV = FCFF/(WACC - g) does not hold on this two-stage '
            'terminal and would have put a real error into a number that looked comparable'),
        'value_other_framing_primary_lens': float(IMPLIED_RATE_PRIM),
        'reading': (
            'At AED %.2f the price is paying for a network that SHRINKS: connected '
            'capacity falling by about %.1f thousand refrigeration tonnes a year across '
            'the window, against this study\'s %.1f. Three disclosures bear on that '
            'number and all three point the other way — the company guides %.0f to %.0f '
            'thousand tonnes of additions for 2026, it actually connected %.0f in the '
            'first half (%.0f annualised), and %.0f thousand tonnes sit CONTRACTED and '
            'not yet connected, %.0f%% above what is connected today. Connected capacity '
            'has risen in every year the company has disclosed. The solve is conservative '
            'in the one place it could flatter: letting the study\'s own per-tonne capital '
            'driver run negative CREDITS a shrinking network with releasing capital, and '
            'holding capital expenditure at the maintenance charge instead still requires '
            '%.1f thousand tonnes a year of disconnection. The same disagreement read as a '
            'discount rate is %.2f%% against the study\'s %.2f%%, %.0f basis points — but '
            'that number has no disclosure to check it against, and the pipeline has '
            'three. What this rules out is that the price is a view on the connection '
            'pipeline; where the disagreement actually sits is in the cost of capital, or '
            'in whether an 80%%-owned utility with a fifth of its shares in issue is '
            'priced on its cash flows at all.'
            % (SPOT, abs(IMPLIED), STUDY_PIPE, V['rt_guid_2026'][0], V['rt_guid_2026'][1],
               H1_ADDS, 2 * H1_ADDS, BACKLOG, 100.0 * BACKLOG / CONN['H1_2026'],
               abs(IMPLIED_FLOOR), 100 * IMPLIED_RATE, 100 * W['rating_ct'],
               1e4 * (IMPLIED_RATE - W['rating_ct'])))}}

cj = {
    'ticker': 'EMPOWER',
    'as_of': C.INP['spot']['date'],
    'published_central': ADOPTED,
    'published_spot': SPOT,
    'measured_on': (
        "The published answer is the four-lens blend, so materiality is measured on it. "
        "That construction DAMPENS every fork touching only the cash-flow lens by about "
        "half, and offsetting moves across lenses can cancel entirely — terminal real "
        "growth is worth 2.0% on the primary lens and 0.6% on the blend, because the same "
        "rate that lowers the discounted cash flow raises the two lenses that capitalise "
        "earnings. Nothing is hidden by that: every judgement carries its value on the "
        "primary lens alone beside its value on the blend."),
    'judgements': J,
    'unvalued': [
        {'name': 'the disclosed control transaction',
         'what': ('the parent bought 24% at AED 2.16 in February 2026, and the study '
                  'reports it as a reference point rather than as evidence of value'),
         'why_not_valued': ('a related-party CONTROL price is not the same quantity as a '
                            'minority fair value, so pricing "adopt it as the answer" '
                            'against this model would compare two different things. It is '
                            'recorded unvalued rather than guessed [R-ENF-04].')},
        {'name': 'the terminal maintenance basis',
         'what': ('the terminal escalates BOOK depreciation, which the shared module '
                  'labels a cross-check, rather than dividing a replacement-cost capital '
                  'base by the disclosed life, which it labels the standard'),
         'why_not_valued': ('the standard basis needs a replacement-cost capital base and '
                            'the filings disclose none; a base this desk chose is not a '
                            'disclosed one (SIGCM clause 1), so the fork is named rather '
                            'than filled with an invented figure.')},
        {'name': 'a cut to the regulated tariff cap',
         'what': ('the flat tariff underwrites the capacity charge that carries 77.9% of '
                  'enterprise value into the terminal, and the model contains no machinery '
                  'for a cap cut'),
         'why_not_valued': ('the current instrument bars indexation of capacity charges '
                            'and the achieved rate already sits at the cap, so the upward '
                            'fork is settled by disclosure rather than contested; the '
                            'downward one is an unmodelled risk the study names, not a '
                            'choice it resolved.')}]}

json.dump(diag, open(os.path.join(HERE, 'diagnostics.json'), 'w', encoding='utf-8'),
          indent=1, ensure_ascii=False, default=float)
json.dump(cj, open(os.path.join(HERE, 'contested_judgements.json'), 'w', encoding='utf-8'),
          indent=1, ensure_ascii=False, default=float)

assert open(NUMBERS, 'rb').read() == _BEFORE, 'study_numbers.json moved — refusing'

print('diagnostics.json + contested_judgements.json written')
print('implied pipeline %+.2f k RT/yr (floored %+.2f, primary lens %+.2f) vs study %+.2f'
      % (IMPLIED, IMPLIED_FLOOR, IMPLIED_PRIM, STUDY_PIPE))
print('implied flat rate %.4f%% vs study %.4f%%' % (100 * IMPLIED_RATE,
                                                    100 * W['rating_ct']))
_m = [j for j in J if abs(j['value_adopted'] - j['value_alternative'])
      / abs(j['value_alternative']) >= 0.05]
print('%d judgements, %d material: %s'
      % (len(J), len(_m), ', '.join('%s %s' % (j['name'][:34],
         'UP' if j['value_adopted'] > j['value_alternative'] else 'DOWN') for j in _m)))
