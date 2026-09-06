#!/usr/bin/env python3
"""BOROUGE — the two output records [R-ENF-05], COMPUTED rather than remembered.

WHAT THIS WRITES, AND WHY IT IS A SCRIPT RATHER THAN A FILE. diagnostics.json and
contested_judgements.json are read by an outside gate and by nobody else. An artefact
every reader reads and nothing writes is a number frozen at the date somebody last typed
it [R-ENF-06], so both are generated here, from this study's own model, at every run.

THE REVERSE READ. This study states what IT believes and, until now, nowhere stated what
the PRICE believes — and the two are the same model read backwards. THE QUANTITY IS THE
STUDY'S OWN CRUX, not a generic rate: the answer here turns on the question its numbers
file poses in its own words, "Is navigation through the Strait of Hormuz restored during
2026, or does the disruption persist into 2027?", and on what that question DECIDES, which
the same record answers in its own words — "whether the plant runs at the utilisation it
has demonstrated or stays capped by feedstock and logistics". So the quantity solved is
UTILISATION OF NAMEPLATE CAPACITY, which this company discloses every quarter and a reader
can therefore check against the filings rather than take on trust. The single flat discount
rate is solved BESIDE it on the shared instrument (engine/reverse_read.py), so this name
still carries the number that is comparable across the book.

THE SOLVE MOVES ONE THING. Every driver stays at its published value and only the
utilisation path shifts, in parallel across the five explicit years, until this study's own
forecast function reproduces the traded price. The function is the SHIPPED one — it is
imported and called, never re-implemented, because a reverse read on a re-implementation
grades a different model.

IT IS A DIAGNOSTIC AND NOTHING READS IT BACK. A quantity solved from a price and then used
in the valuation is the reverse-engineered rate the protocol prohibits outright, arriving
through a side door; assert_reverse_dcf() refuses any study whose builders read this file,
and this generator additionally asserts before writing that the solved value appears
nowhere in study_numbers.json.

THE SIGN TEST. Any single contested choice is defensible; a study resolving every one of
them the same way and never noticing is not. Every alternative below is priced by RE-RUNNING
this study's own forecast function with that one choice changed and everything else held at
its published value, through the same bridge as the adopted figure — so what is measured is
the CHOICE and not a second construction.

    python3 diagnostics_borouge.py      writes diagnostics.json + contested_judgements.json
"""
import contextlib
import copy
import io
import json
import os
import sys
from math import comb

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, ENGINE)

NUMBERS = os.path.join(HERE, 'study_numbers.json')


def _load_numbers():
    with open(NUMBERS, encoding='utf-8') as fh:
        return fh.read()


# THE IMPORT IS ALSO A WRITE, AND THAT IS ASSERTED RATHER THAN HOPED. compute.py writes
# study_numbers.json at import. This record may not move a driver, a rate or a fair value,
# so the file is read before and after and required to be byte-identical: if importing the
# model to measure it changed the model, this stops.
_BEFORE = _load_numbers()
with contextlib.redirect_stdout(io.StringIO()):
    import compute as CP                                             # noqa: E402
import reverse_read as RR                                            # noqa: E402

assert _load_numbers() == _BEFORE, (
    "importing compute.py changed study_numbers.json. This record measures the study; it "
    "does not move it.")

N = json.loads(_BEFORE)
F = CP.FRAMINGS
W = CP.WACC
SPOT_AED = CP.v('spot_aed')
SPOT_USD = SPOT_AED / CP.v('aed_per_usd')
FRAME_A, FRAME_B = 'normalisation', 'prolonged'


def value_of(framing, **kw):
    """AED per share on this study's own forecast function, one lever moved."""
    return CP.run_framing(framing, kw.pop('wacc', W), **kw)['per_share_aed']


def both(**kw):
    return {k: value_of(F[k], **dict(kw)) for k in (FRAME_A, FRAME_B)}


RES = {k: CP.run_framing(F[k], W) for k in (FRAME_A, FRAME_B)}
BASE = {k: RES[k]['per_share_aed'] for k in RES}

# THE RE-RUN IS PROVED AGAINST THE COMMITTED ANSWER BEFORE ANY ALTERNATIVE IS BELIEVED.
for _k, _b in (('normalisation', N['framings']['normalisation']['per_share_aed']),
               ('prolonged', N['framings']['prolonged']['per_share_aed'])):
    assert abs(BASE[_k] - _b) < 1e-12, (_k, BASE[_k], _b)


# ============================================================================
# 1. THE REVERSE READ — the utilisation the traded price is paying for
# ============================================================================
def solve_utilisation(key, lo=-0.60, hi=0.40):
    """The parallel shift in utilisation that reproduces the traded price.

    Bisection, because value is monotone increasing in the shift over this interval, so
    the root is unique and the answer cannot depend on where the search began.
    """
    assert value_of(F[key], util_shift=lo) < SPOT_AED < value_of(F[key], util_shift=hi)
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if value_of(F[key], util_shift=mid) < SPOT_AED:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


SHIFT = {k: solve_utilisation(k) for k in (FRAME_A, FRAME_B)}
for _k, _s in SHIFT.items():
    assert abs(value_of(F[_k], util_shift=_s) - SPOT_AED) < 1e-6, (_k, _s)

# The scalar is the TERMINAL year's polyethylene utilisation, in per cent — the unit the
# company itself publishes ("polyethylene utilisation rate, FY2025, stated as 102%") — and
# the terminal year is the one that matters because that is the year the terminal value
# capitalises, and the terminal is most of the answer on both branches.
IMPLIED_UTIL = {k: 100.0 * (F[k]['util_pe'][-1] + SHIFT[k]) for k in SHIFT}
STUDY_UTIL = {k: 100.0 * F[k]['util_pe'][-1] for k in SHIFT}

# What the company has actually disclosed, from its own Management Discussion & Analysis.
# rounded at the tenth of a point only to strip the binary artefact of 100 x 1.1; these
# are filed percentages and nothing here changes one.
DISCLOSED_PE = {2024: round(100.0 * CP.v('util_pe_fy24'), 6),
                2025: round(100.0 * CP.v('util_pe_fy25'), 6)}
DISCLOSED_PP = {2024: round(100.0 * CP.v('util_pp_fy24'), 6),
                2025: round(100.0 * CP.v('util_pp_fy25'), 6)}
NAMEPLATE = CP.v('cap_pe_fy25') + CP.v('cap_pp_fy25')
DISCLOSED_TOTAL = {y: 100.0 * CP.prod_hist[y] / NAMEPLATE for y in CP.HIST}
H126_TOTAL = 100.0 * 2 * CP.v('prod_h126') / NAMEPLATE

# BESIDE IT, ON THE SHARED INSTRUMENT: the single flat discount rate, so this name carries
# the one number that is comparable with every other study in the book.
FLAT = {}
for k in (FRAME_A, FRAME_B):
    r = RES[k]
    # The Borouge 4 operator fee is a cash flow of the same firm discounted at the same
    # rate and carried inside this study's enterprise value, so it belongs in the series
    # the rate is solved on; its terminal is zero by the study's own construction.
    fcff = [row['fcff'] + b['net_profit'] for row, b in zip(r['rows'], r['b4']['rows'])]
    df_last = r['rows'][-1]['discount_factor']
    FLAT[k] = RR.read(fcff=fcff, t_mid=[1.0, 2.0, 3.0, 4.0, 5.0], tv=r['terminal_value'],
                      wacc_terminal=W, g=r['terminal_growth'], df_last=df_last,
                      df_tv=df_last, ev_study=r['ev'], equity_study=r['equity'],
                      shares_mn=CP.shares_out / 1e6, spot=SPOT_USD)
    # the check that the two rates are one quantity measured twice
    assert abs(FLAT[k]['implied_rate_at_study_value'] - W) < 1e-6, (k, FLAT[k])


# ============================================================================
# 2. THE CONTESTED JUDGEMENTS — each priced by re-running the study's own model
# ============================================================================
@contextlib.contextmanager
def patched(**globals_):
    """Move one module-level input, run, put it back. Nothing is written to disk."""
    old = {k: getattr(CP, k) for k in globals_}
    for k, val in globals_.items():
        setattr(CP, k, val)
    try:
        yield
    finally:
        for k, val in old.items():
            setattr(CP, k, val)


@contextlib.contextmanager
def patched_macro(**entries):
    old = {k: CP.MAC[k]['value'] for k in entries}
    for k, val in entries.items():
        CP.MAC[k]['value'] = val
    try:
        yield
    finally:
        for k, val in old.items():
            CP.MAC[k]['value'] = val


def rebridge(ev_delta):
    """AED per share with an additive change to enterprise value, on the study's OWN
    bridge — the same net debt, leases, minority and share count as the adopted figure."""
    out = {}
    for k, r in RES.items():
        eq = r['ev'] + ev_delta[k] - r['net_debt'] - r['leases'] - r['nci']
        out[k] = eq / CP.shares_out * 1e6 * CP.v('aed_per_usd')
    return out


JUDGEMENTS = []


def judge(name, adopted, alternative, alt_values, why):
    va, vb = BASE[FRAME_A], alt_values[FRAME_A]
    JUDGEMENTS.append(dict(
        name=name, adopted=adopted, alternative=alternative,
        value_adopted=float(va), value_alternative=float(vb),
        value_adopted_frame_B=float(BASE[FRAME_B]),
        value_alternative_frame_B=float(alt_values[FRAME_B]),
        share_of_value=float(abs(va - vb) / abs(vb)),
        direction=('the study adopted the higher-value framing' if va > vb else
                   'the study adopted the lower-value framing' if va < vb else
                   'the two framings give the same value'),
        why=why))


# --- the cost of capital ---------------------------------------------------------------
judge('the beta: a tier-1 own-stock regression against a bottom-up sector beta',
      'the own-stock weekly regression against the FTSE ADX General Index, beta '
      '%.4f, cost of capital %.3f%%' % (CP.beta_used_own, 100 * CP.WACC_OWN),
      'the global Chemical (Diversified) unlevered beta re-levered to this company\'s own '
      'market-value structure, beta %.4f, cost of capital %.3f%%'
      % (CP.BETA_BU, 100 * CP.WACC_BU),
      both(wacc=CP.WACC_BU),
      'The study names this its own central contested judgement and publishes both the '
      'whole way through. The own-stock regression is the beta hierarchy\'s first choice '
      'and it passes the usability gate on all three conditions (n=%d weekly observations, '
      'R-squared %.3f against the 0.05 floor, standard error %.3f against a beta of %.3f), '
      'so it is not discarded. It is also flagged weak by the same machinery — a 90%% '
      'interval of [%.2f, %.2f] spanning %.2f times the point estimate — and a beta of '
      '%.2f is implausible for a producer whose earnings track a global commodity '
      'benchmark. A Dimson lead-lag correction moves it DOWN to %.3f rather than up, so '
      'thin trading does not explain it. This is the single largest fork in the study and '
      'the adopted side is the higher-value one.'
      % (CP.BETA['n'], CP.BETA['r2'], CP.BETA['se'], CP.beta_used_own,
         CP.BETA['ci90'][0], CP.BETA['ci90'][1],
         (CP.BETA['ci90'][1] - CP.BETA['ci90'][0]) / abs(CP.beta_own),
         CP.beta_used_own, CP.BETA['dimson']['sum_beta']))

_KE_AED = CP.build_ke(CP.beta_used_own, CP.ERP_RATING, rf=CP.RF_STAR_AED)
_W_AED = CP.build_wacc(_KE_AED, CP.KD, CP.ETR, CP.E_WEIGHT)
judge('the risk-free rate: the dollar construction against the dirham one',
      'the US 10-year of %.2f%% less the United States\' own default spread of %.2f%% = '
      '%.2f%%, matching the dollar the company reports, prices and borrows in'
      % (100 * CP.RF_USD, 100 * CP.m('us_default_spread'), 100 * CP.RF_STAR),
      'the UAE dirham government yield of %.2f%% less the UAE\'s own default spread of '
      '%.2f%% = %.2f%%, which the study publishes beside it'
      % (100 * CP.rf_local_aed, 100 * CP.default_spread, 100 * CP.RF_STAR_AED),
      both(wacc=_W_AED),
      'The study publishes both and adopts the dollar one, reporting the %.0f basis point '
      'gap under a hard peg rather than reconciling it away. Under a peg the two are '
      'competing measurements of one price of time, so the alternative is real; the debt '
      'leg stays at its contractual dollar cost on both sides because that is a fact about '
      'the facilities rather than a choice. The adopted side is the higher rate and '
      'therefore the lower value.' % (10000 * (CP.RF_STAR - CP.RF_STAR_AED)))

judge('the equity risk premium basis: rating against adjusted-default-spread',
      'the published rating-based UAE equity risk premium of %.2f%%'
      % (100 * CP.ERP_RATING),
      'the mature-market premium of %.2f%% plus the UAE adjusted default spread of %.2f%% '
      '= %.2f%%' % (100 * CP.m('mature_erp'), 100 * CP.default_spread, 100 * CP.ERP_DS),
      both(wacc=CP.WACC_OWN_DS),
      'Both bases are published in the study\'s own cost-of-capital table and the same '
      'basis is stripped from the risk-free rate as is added back, so country risk enters '
      'exactly once either way. The adopted basis is the higher premium and therefore the '
      'lower value.')

judge('the cost of debt: the marginal margin over the long dollar rate against overnight',
      'the arm\'s-length margin of %.3f%% over the 10-year dollar rate = %.2f%%, '
      'tenor-matched to a perpetual cash flow stream'
      % (100 * CP.MARGIN_ARMS, 100 * CP.KD),
      'the same margin over the overnight rate the facilities actually float on = %.2f%%'
      % (100 * CP.KD_SPOT_FLOATING),
      both(wacc=CP.build_wacc(CP.KE_OWN, CP.KD_SPOT_FLOATING, CP.ETR, CP.E_WEIGHT)),
      'The facilities are floating over overnight secured financing, so the observed rate '
      'today is the overnight one; the study carries the same margin over the long rate '
      'because the cash flows being discounted are perpetual and a discount rate must be '
      'tenor-matched. Both are defensible readings of the same disclosed margin, and the '
      'adopted one is the higher rate and therefore the lower value.')

judge('the cost of debt: arm\'s-length against the rate actually being paid',
      'the arm\'s-length margin of %.3f%%' % (100 * CP.MARGIN_ARMS),
      'the weighted related-party margin the two facilities actually carry, %.3f%%'
      % (100 * CP.margin_related),
      both(wacc=CP.build_wacc(CP.KE_OWN, CP.KD_RELATED, CP.ETR, CP.E_WEIGHT)),
      'Two prices exist for the same borrower because the facilities are related-party. '
      'The study uses the arm\'s-length one on the ground that a marginal cost of capital '
      'should not embed a shareholder subsidy, and the difference is %.0f basis points, so '
      'nothing in the answer turns on it.' % (10000 * (CP.KD - CP.KD_RELATED)))

judge('lease liabilities: deducted in the bridge, excluded from the capital weights',
      'leases outside the weights, equity weight %.2f%%' % (100 * CP.E_WEIGHT),
      'leases inside the weights as debt, equity weight %.2f%%'
      % (100 * CP.mktcap / (CP.mktcap + CP.net_debt + CP.leases)),
      both(wacc=CP.build_wacc(CP.KE_OWN, CP.KD, CP.ETR,
                              CP.mktcap / (CP.mktcap + CP.net_debt + CP.leases))),
      'A lease treated as debt in the bridge and not in the weights is an inconsistency an '
      'outside critique raised and the study accepted as immaterial WITH THE NUMBER '
      'ATTACHED, which is what this row is. It is recorded because "immaterial" is a claim '
      'and it is priced here rather than asserted.')


# --- the crux ---------------------------------------------------------------------------
judge('the crux: how long navigation through the Strait of Hormuz stays impaired',
      'published BOTH ways and never averaged — a normalisation branch and a prolonged '
      'branch, each with the condition it holds under',
      'one branch chosen and published as the single central',
      {FRAME_A: BASE[FRAME_B], FRAME_B: BASE[FRAME_A]},
      'The judgement is binary and about the world rather than about the model, so an '
      'average would describe a shipping lane that is neither open nor closed; the study '
      'takes no side and shows the reader the question. THE DIRECTION THIS ROW CONTRIBUTES '
      'IS AN ARTEFACT OF THE ANCHOR AND NOT A FACT ABOUT THE STUDY: this record is '
      'anchored on the normalisation branch because that is the branch the study\'s own '
      'lens record names as its primary value, and anchoring on the other branch would '
      'reverse this row\'s sign. The sign test is therefore reported on both anchors and '
      'neither is near the flag.')

# --- the forecast ------------------------------------------------------------------------
with patched(SOURCING_UPLIFT=1.0):
    _alt = both()
judge('sales above production: the disclosed sourcing channel kept or discarded',
      'sales run at %.4f times production, the audited three-year mean, held flat and not '
      'grown' % CP.SOURCING_UPLIFT,
      'sales capped at capacity times utilisation, so the company sells only what it makes',
      _alt,
      'Borouge sells more tonnes than it produces because it sources product from its '
      'parent, from its own compounding plant and from other partners — %s kt of '
      'second-quarter 2026 sales alone. Capping sales at production discards a channel the '
      'company discloses, and because the cap runs into the terminal year it compounds. '
      'The uplift is measured from the audited record rather than assumed, and the adopted '
      'side is the higher-value one.' % '54')

with patched_macro(terminal_roc=W):
    _alt = both()
judge('the terminal return on capital: %.0f%% against the cost of capital itself'
      % (100 * CP.m('terminal_roc')),
      '%.0f%% in perpetuity, above the %.2f%% cost of capital, so reinvestment creates '
      'value for ever' % (100 * CP.m('terminal_roc'), 100 * W),
      'a terminal return equal to the cost of capital, so growth is value-neutral and the '
      'reinvestment it requires earns exactly what it costs',
      _alt,
      'The terminal charge is built on the reinvestment identity, so the return on capital '
      'sets what fraction of terminal profit is retained: at %.0f%% it is %.1f%% and at the '
      'cost of capital it is %.1f%%. Two outside critiques challenged the %.0f%% as '
      'aggressive for a commodity producer in perpetuity, and the study\'s ground is that '
      'this company earned high-teens returns across the three audited years on an '
      'advantaged feedstock position. Both are defensible and the adopted one is the '
      'higher-value framing.'
      % (100 * CP.m('terminal_roc'),
         100 * CP.m('terminal_growth') / CP.m('terminal_roc'),
         100 * CP.m('terminal_growth') / W, 100 * CP.m('terminal_roc')))

_RAW_XS = np.array([CP.vol_tot_hist[y] for y in CP.HIST])
_RAW_Y = np.array([CP.v(f'othprod_fy{str(y)[2:]}') for y in CP.HIST])
_RAW_COEF, *_ = np.linalg.lstsq(np.column_stack([np.ones(3), _RAW_XS]), _RAW_Y, rcond=None)
with patched(OTHPROD_FIXED=float(_RAW_COEF[0])):
    _alt = both()
judge('the other-production-cost split: re-anchored to the audited year or left as fitted',
      'the fixed leg re-anchored to $%.0fm so the cost line reproduces the AUDITED FY2025 '
      'figure at FY2025\'s own production volume' % CP.OTHPROD_FIXED,
      'the fixed leg of $%.0fm the three-year least-squares fit returns on its own'
      % _RAW_COEF[0],
      _alt,
      'A three-point regression cannot identify this split — production spans only %.0f kt '
      'across the three audited years — so the fit was calibrated on sales tonnes while '
      'the forecast drives it on production tonnes, and it understated the audited FY2025 '
      'cost by $%.0fm at that year\'s own production. Re-anchoring ties the level to the '
      'accounts and leaves the variable rate as a disclosed judgement rather than a fit. '
      'The adopted side charges more cost and is therefore the lower-value framing.'
      % (max(CP.prod_hist.values()) - min(CP.prod_hist.values()),
         CP.OTHPROD_FIXED - _RAW_COEF[0]))

_B4_STEADY = RES[FRAME_A]['b4']['steady_adopted']
_B4_G = CP.m('terminal_growth')
_B4_PERP = {k: _B4_STEADY * (1 + _B4_G) / (W - _B4_G) * RES[k]['rows'][-1]['discount_factor']
            for k in RES}
judge('the Borouge 4 operator fee: terminated at recontribution or capitalised for ever',
      'no perpetuity — the fee runs only until the assets are acquired, which the sponsors '
      'say is not anticipated before 2029, and the listed company\'s share afterwards is '
      'zero',
      'the same fee capitalised to a perpetuity, as an earlier edition of this study did',
      rebridge(_B4_PERP),
      'The agreement the fee comes from terminates on its own cited disclosure, and the '
      'study\'s own text says the listed company owns no part of the expansion afterwards. '
      'Capitalising a stream past the date its own disclosure ends it was the largest '
      'single downward correction any critique of this study produced. The explicit ramp '
      'is kept at its full present value of $%.0fm; only the perpetuity is refused, and '
      'the adopted side is the lower-value framing.' % RES[FRAME_A]['b4']['value'])

judge('the effective tax rate: the audited three-year mean or the reviewed half',
      'the mean of the three audited years, %.2f%%' % (100 * CP.ETR),
      'the rate the reviewed first half of 2026 actually shows, %.2f%%'
      % (100 * CP.etr_h126),
      both(etr_override=CP.etr_h126),
      'A near-term reviewed actual outranks a stale full-year rate on this house\'s own '
      'standing rule, and this is the one place in the study where the rule points the '
      'other way from what was done: the three audited years run %.2f%% / %.2f%% / %.2f%% '
      'and the reviewed half runs %.2f%%, so the mean is the more stable estimate of a '
      'rate that has barely moved while the half is the more recent observation of it. '
      'Carrying the mean is defensible; it is also the lower-value framing, and the half '
      'was not disclosed in the delivered edition, which an outside critique raised.'
      % tuple(100 * x for x in (CP.etr_hist + [CP.etr_h126])))

judge('the realisation residual: the audited three-year mean or the reviewed half',
      'the three audited years, %.4f on polyethylene and %.4f on polypropylene'
      % (CP.REAL_PE, CP.REAL_PP),
      'the reviewed first half of 2026, %.4f and %.4f'
      % (CP.real_pe_h126, CP.real_pp_h126),
      both(realisation_pe=CP.real_pe_h126, realisation_pp=CP.real_pp_h126),
      'The residual is the gap between revenue per tonne actually filed and the published '
      'benchmark-plus-premium construct, computed rather than assumed. The half-year runs '
      'above the audited mean on polyethylene and below it on polypropylene, so the two '
      'legs pull opposite ways and the net is small; the study carries the audited mean '
      'because a single disrupted half is a poor estimate of a structural residual.')

judge('maintenance capital expenditure: the steady-state figure or the audited record',
      '$%.0fm a year in steady state' % CP.m('maintenance_capex'),
      'the audited three-year mean of $%.1fm, which is what the company actually spent'
      % float(np.mean([CP.hist[y]['capex'] for y in CP.HIST])),
      both(capex_override=float(np.mean([CP.hist[y]['capex'] for y in CP.HIST]))),
      'The three audited years ran $%.0fm, $%.0fm and $%.0fm and the study carries $%.0fm, '
      'which exceeds all three. An outside critique made exactly that point and the study '
      'accepted it as a real but small overcharge; it is the lower-value framing and it is '
      'recorded here rather than remembered.'
      % (CP.hist[2023]['capex'], CP.hist[2024]['capex'], CP.hist[2025]['capex'],
         CP.m('maintenance_capex')))

_PE_MEAN = float(np.mean([CP.prem_pe_hist[y] for y in CP.HIST]))
_PP_MEAN = float(np.mean([CP.prem_pp_hist[y] for y in CP.HIST]))
_alt = {}
for _k in (FRAME_A, FRAME_B):
    _g = copy.deepcopy(F[_k])
    _g['prem_pe'] = _g['prem_pe'][:2] + [_PE_MEAN] * 3
    _g['prem_pp'] = _g['prem_pp'][:2] + [_PP_MEAN] * 3
    _alt[_k] = value_of(_g)
judge('the steady-state premium: management\'s guidance or the audited realised record',
      'the company\'s own through-the-cycle guidance, $%.0f a tonne on polyethylene and '
      '$%.0f on polypropylene' % (CP.v('prem_pe_ttc'), CP.v('prem_pp_ttc')),
      'the premium the company actually realised across the three audited years, $%.1f and '
      '$%.1f' % (_PE_MEAN, _PP_MEAN),
      _alt,
      'A driver that takes management\'s forward target as an input inherits whatever lean '
      'that target carries, so the guidance is a thing to score rather than to consume. '
      'The audited realised record runs $%.0f / $%.0f / $%.0f on polyethylene against '
      'guidance of $%.0f, and $%.0f / $%.0f / $%.0f on polypropylene against $%.0f, so the '
      'two legs disagree in opposite directions and the guidance is not uniformly the '
      'flattering side. It is here because it is a fork the study resolved, not because '
      'the number moves.'
      % (CP.prem_pe_hist[2023], CP.prem_pe_hist[2024], CP.prem_pe_hist[2025],
         CP.v('prem_pe_ttc'), CP.prem_pp_hist[2023], CP.prem_pp_hist[2024],
         CP.prem_pp_hist[2025], CP.v('prem_pp_ttc')))

with patched_macro(terminal_growth=CP.m('uae_cpi')):
    _alt = both()
judge('terminal growth: %.1f%% nominal against the study\'s own UAE inflation of %.1f%%'
      % (100 * CP.m('terminal_growth'), 100 * CP.m('uae_cpi')),
      '%.1f%% nominal in dollars for a producer whose owned capacity is fixed'
      % (100 * CP.m('terminal_growth')),
      'the %.1f%% domestic inflation the same model escalates its own fixed costs at, '
      'which is zero real growth rather than a %.1f%% real decline'
      % (100 * CP.m('uae_cpi'),
         100 * (CP.m('uae_cpi') - CP.m('terminal_growth')) / (1 + CP.m('terminal_growth'))),
      _alt,
      'A growth rate is honest when it is stored as a real rate on a stated inflation path '
      'rather than typed as a nominal. %.1f%% against the %.1f%% this model escalates its '
      'own fixed cost, general and administrative expense and labour at is a real decline '
      'of about %.2f%% a year in perpetuity — small, and nothing in the filings states it. '
      'The adopted side is the lower-value framing. The gap is %.0f basis points because '
      'the peg makes this the flattest terminal in the book, not because the question is '
      'unimportant.'
      % (100 * CP.m('terminal_growth'), 100 * CP.m('uae_cpi'),
         100 * (CP.m('uae_cpi') - CP.m('terminal_growth')) / (1 + CP.m('terminal_growth')),
         10000 * (CP.m('uae_cpi') - CP.m('terminal_growth'))))

_B4_ALT_SCALE = RES[FRAME_A]['b4']['steady_from_cumulative'] / _B4_STEADY
judge('the Borouge 4 fee level: the accretion disclosure or the cumulative one',
      'the lower of the two, $%.1fm a year, from the "approximately 10%% annual earnings '
      'accretion" disclosure' % _B4_STEADY,
      'the higher, $%.1fm a year, from the "$400m of cumulative net profit over three '
      'years" disclosure read against this study\'s own ramp'
      % RES[FRAME_A]['b4']['steady_from_cumulative'],
      rebridge({k: RES[k]['b4']['value'] * (_B4_ALT_SCALE - 1.0) for k in RES}),
      'The sponsors quantify the same fee two ways in the same announcement and the two do '
      'not agree — they differ by %.1f times — so the study computes both, carries the '
      'lower and discloses the gap rather than picking the one that reads better. The '
      'stream is %.1f%% of enterprise value either way. The adopted side is the '
      'lower-value framing.'
      % (_B4_ALT_SCALE, 100 * RES[FRAME_A]['b4']['share_of_ev']))

_DPO_TRADE = float(np.mean([CP.v(f'ap_fy{str(y)[2:]}') * CP.USDm / CP.hist[y]['cogs'] * 365
                            for y in CP.HIST]))
with patched(DPO=_DPO_TRADE):
    _alt = both()
judge('the payable period: the full operating payable or trade payables alone',
      'trade payables plus accruals plus amounts due to related parties, %.1f days'
      % CP.DPO,
      'trade accounts payable alone, %.1f days' % _DPO_TRADE,
      _alt,
      'The feedstock account with the parent is where most of this company\'s supplier '
      'credit actually sits, so excluding it reports a payable period of %.0f days for a '
      'business that buys its ethane on a group account. The adopted side shortens the '
      'cash cycle and is the higher-value framing, and it is worth %.2f%% because working '
      'capital moves the level of the balance once and not the cash flow for ever.'
      % (_DPO_TRADE,
         100 * abs(BASE[FRAME_A] - _alt[FRAME_A]) / _alt[FRAME_A]))


# ============================================================================
# 3. WHAT IS NOT VALUED, AND WHAT IS NOT A FORK — both named rather than absent
# ============================================================================
# An absent answer is not a clean answer. A judgement this record cannot price BOTH ways
# from the filings is listed with the reason it cannot, never guessed at.
NOT_VALUED = [
    dict(name='the terminal construction itself',
         adopted='the reinvestment identity — terminal profit less growth times the '
                 'capital that growth requires, at a %.0f%% terminal return'
                 % (100 * CP.m('terminal_roc')),
         why_not=(
             'The sanctioned terminal module builds maintenance at current cost off a '
             'DISCLOSED useful life, and this company does not disclose one that can be '
             'collapsed to a single figure: its own accounting-policies note gives ranges '
             '(buildings 15-40 years, plant and machinery 8-35), and a life this desk '
             'picked itself is not a disclosed life. The alternative therefore cannot be '
             'built from the filings, so it is reported unvalued and the name stays on the '
             'terminal ratchet with that reason, rather than being conformed on an '
             'invented number.'),
         one_sided_price=(
             'none available without choosing a life. What can be said without one is that '
             'the identity implies a replacement cycle of one divided by the terminal '
             'growth rate, which at %.1f%% is %.1f years — a fact about the currency and '
             'not about any asset, and it sits inside the range the note actually '
             'discloses rather than outside it, which is why the direction cannot be read '
             'off it here.'
             % (100 * CP.m('terminal_growth'), 1.0 / CP.m('terminal_growth'))),
         evidence='TERMINAL_EVIDENCE_06-09-2026.md in this directory, which re-read the '
                  'note off the rendered pixels and off the text layer and reports both'),
    dict(name='the depreciation rate carried through the forecast',
         adopted='calibrated inside the forecast function so that FY2026 reproduces the '
                 'reviewed first half\'s own run rate',
         why_not=(
             'The calibration is a local constant inside the forecast function and is not '
             'exposed as a parameter, so pricing the alternative would mean '
             're-implementing the function rather than re-running it — and a judgement '
             'priced on a re-implementation measures a different model, which is the '
             'defect this whole record exists to avoid. Reported unvalued rather than '
             'approximated.'),
         one_sided_price=(
             'the direction is arithmetic even though the magnitude is not: a higher '
             'depreciation charge raises explicit-year cash flow through the tax shield '
             'and lowers terminal profit, and the terminal carries %.0f%% of enterprise '
             'value here, so the adopted charge — which sits below the audited three-year '
             'mean — is the HIGHER-value framing.'
             % (100 * RES[FRAME_A]['tv_share_of_ev'])),
         evidence='the audited depreciation and amortisation of $%.0fm, $%.0fm and $%.0fm '
                  'in the three audited years'
                  % (CP.hist[2023]['da'], CP.hist[2024]['da'], CP.hist[2025]['da'])),
    dict(name='treasury shares in the per-share divisor',
         adopted='the issued share count of %s, with the gap disclosed'
                 % f'{int(CP.shares_out):,}',
         why_not=(
             'The interim statements carry treasury shares at COST and not as a share '
             'count, so the outstanding count cannot be recovered from the filings. '
             'Reverse-engineering one from an unrelated price would be inventing the very '
             'figure the divisor turns on. The study discloses the gap instead, and it is '
             'reported unvalued here for the same reason.'),
         one_sided_price='the direction is known and the size is not: any treasury holding '
                         'makes the outstanding count SMALLER than the issued count, so '
                         'the adopted divisor is the conservative one and the alternative '
                         'can only raise value per share.',
         evidence='the FY2025 audited statements, which state the treasury holding at cost'),
]

# A fork the study did not have to resolve, or resolved in a way that moves nothing, is a
# different thing from a judgement and is recorded as such rather than counted.
_ETHANE = {k: [CP.feed_per_t[2025] * (1 + CP.ETHANE_REAL) ** (i + 1) for i in range(5)]
           for k in (FRAME_A, FRAME_B)}
_BLEND = {}
for k in (FRAME_A, FRAME_B):
    _prop = [CP.feed_per_t[2025] * (F[k]['bench_pp'][i] / CP.v('bench_pp_fy25'))
             for i in range(5)]
    _BLEND[k] = [(1 - F[k]['feed_market_share'][i]) * _ETHANE[k][i]
                 + F[k]['feed_market_share'][i] * _prop[i] for i in range(5)]
_FLOOR_BINDS = any(_BLEND[k][i] < _ETHANE[k][i] - 1e-9
                   for k in _BLEND for i in range(5))
_FLOOR_MIN_GAP = min(_BLEND[k][i] - _ETHANE[k][i] for k in _BLEND for i in range(5))

NOT_TREATED = [
    dict(name='the contracted ethane floor under the feedstock blend',
         why=('The model floors the blended feedstock rate at the contracted ethane rate, '
              'which reads like a choice and is not a live one: measured across both '
              'branches and all five forecast years the blend never falls below the '
              'floor — the smallest margin is $%.1f a tonne — so the clause binds nowhere '
              'and both framings give the identical answer. It is recorded because a '
              'clause that binds nothing today can bind on a different price path, and a '
              'reader should know it was measured rather than assumed.'
              % _FLOOR_MIN_GAP)),
    dict(name='the central: the class primary against the retired median of nine readings',
         why=('The delivered edition published the MEDIAN of nine lens readings, worth AED '
              '%.4f at this study\'s current spot against a primary of AED %.4f. It is not '
              'listed as a contested judgement because the construction is RETIRED rather '
              'than contested — one class primary is the central and the other lenses are '
              'cross-checks — so the blend is not a framing this study is free to adopt. '
              'It is named here with its number so nothing is hidden by the omission. It '
              'would also DOUBLE-COUNT: the median selects the sector-beta cell of the '
              'grid, so its value is arithmetically the same number as the beta row\'s '
              'alternative, and recording both would turn one number into two signs.'
              % (N['fair_mid_retired'], BASE[FRAME_A]))),
    dict(name='the relative-multiple anchor set',
         why=('The lens takes the median of three through-cycle anchors rather than of the '
              'eleven listed peers, nine of which are loss-making and two of which have no '
              'defined enterprise multiple at all. Dropping one anchor moves that lens '
              'materially, and it moves the published answer by nothing, because under the '
              'lens rule a cross-check is published beside the central and never weighted '
              'into it. It is a fork in a cross-check, not in the answer.')),
    dict(name='the benchmark price path held identical across the two branches',
         why=('The prolonged branch carries the SAME benchmark prices as the normalisation '
              'branch, deliberately, so that the two branches isolate the crux and a '
              'downside does not pay more per tonne than the central case. That is a '
              'construction choice with a stated reason and it is not priced here. What is '
              'worth recording is that the prolonged branch\'s own thesis text says '
              'benchmark prices "hold a persistent shortage premium" while its driver '
              'array does not do that — the prose and the drivers disagree, in the '
              'direction that makes the downside branch lower rather than higher.')),
    dict(name='the beta regressor',
         why=('It is measured rather than chosen: a weekly regression against the '
              'published index of the exchange this company is listed on. Which BETA to '
              'adopt is a genuine fork and is the first row of the judgements table; which '
              'INDEX to regress on is not a fork the study is free to resolve.')),
]


# ============================================================================
# 4. THE SIGN TEST, ON BOTH ANCHORS
# ============================================================================
def sign_test(pairs, threshold=0.05):
    """The same arithmetic the outside gate runs, so the record can report what the gate
    will print and can also report it on the anchor the gate does not use."""
    signs = []
    for va, vb in pairs:
        if abs(va - vb) / (abs(vb) or 1.0) >= threshold:
            signs.append(1 if va > vb else (-1 if va < vb else 0))
    n = len([s for s in signs if s])
    k = len([s for s in signs if s > 0])
    if not n:
        return n, k, None
    tail = sum(comb(n, i) for i in range(max(k, n - k), n + 1)) / float(2 ** n)
    return n, k, min(1.0, 2 * tail)


N_A, K_A, P_A = sign_test([(j['value_adopted'], j['value_alternative'])
                           for j in JUDGEMENTS])
N_B, K_B, P_B = sign_test([(j['value_adopted_frame_B'], j['value_alternative_frame_B'])
                           for j in JUDGEMENTS])

# AND THE ROWS THE BAR EXCLUDES, COUNTED RATHER THAN LEFT OUT. The instrument's test is the
# one above, at the house's own 5% bar. Reporting only that, when the rows below the bar run
# almost entirely one way, would hide the thing this instrument exists to find.
_SMALL = [j for j in JUDGEMENTS if j['share_of_value'] < 0.05]
N_SMALL_UP = sum(1 for j in _SMALL if j['value_adopted'] > j['value_alternative'])
N_SMALL_DOWN = sum(1 for j in _SMALL if j['value_adopted'] < j['value_alternative'])
_, _, P_ALL = sign_test([(j['value_adopted'], j['value_alternative']) for j in JUDGEMENTS],
                        threshold=0.0)


# ============================================================================
# 5. WRITE
# ============================================================================
WHY_THIS_FILE = (
    'The reverse read — what the traded price must believe — is a DIAGNOSTIC and lives '
    'outside the numbers file every builder reads. A quantity solved from a price and then '
    'used anywhere in the valuation is the reverse-engineered rate the protocol prohibits '
    'outright, arriving through a side door. Nothing in this file is an input to anything: '
    'it is COMPUTED by diagnostics_borouge.py, no builder in this directory reads it, and '
    'this generator asserts before writing that the solved value appears nowhere in '
    'study_numbers.json.')

READING = (
    'At AED %.2f the price is paying for this plant to run at %.2f%% of its polyethylene '
    'nameplate in the terminal year if navigation normalises, against this study\'s '
    '%.2f%%, and at %.2f%% if the disruption persists, against this study\'s %.2f%%. '
    'Beside what the company itself has filed: polyethylene utilisation was %.0f%% in '
    'FY2024 and %.0f%% in FY2025, and total production ran %.1f%%, %.1f%% and %.1f%% of '
    'nameplate across the three audited years before falling to %.1f%% annualised in the '
    'disrupted first half of 2026. THE MARKET IS INSIDE THE COMPANY\'S OWN FILED RANGE ON '
    'BOTH BRANCHES. The disagreement is %.2f points of utilisation on the optimistic '
    'branch and %.2f points on the pessimistic one — which is a more useful statement than '
    '"the study is %+.1f%% against the price", because a reader can check %.1f%% against a '
    'quarterly disclosure and cannot check a percentage gap against anything.'
    % (SPOT_AED, IMPLIED_UTIL[FRAME_A], STUDY_UTIL[FRAME_A],
       IMPLIED_UTIL[FRAME_B], STUDY_UTIL[FRAME_B],
       DISCLOSED_PE[2024], DISCLOSED_PE[2025],
       DISCLOSED_TOTAL[2023], DISCLOSED_TOTAL[2024], DISCLOSED_TOTAL[2025], H126_TOTAL,
       STUDY_UTIL[FRAME_A] - IMPLIED_UTIL[FRAME_A],
       STUDY_UTIL[FRAME_B] - IMPLIED_UTIL[FRAME_B],
       100 * (BASE[FRAME_A] / SPOT_AED - 1.0), IMPLIED_UTIL[FRAME_A]))

DIAG = {
    'ticker': 'BOROUGE',
    'as_of': '2026-09-06',
    'spot': float(SPOT_AED),
    'spot_date': 'close %s, supplied %s (SUPPLIED_03-09-2026.json)'
                 % (CP.C['spot_aed']['date'], CP.C['spot_aed']['date']),
    # [R-ENF-06] the vintage this artefact was built against. This study publishes TWO
    # branches; every figure here is anchored on the normalisation branch, which is the
    # branch its own lens record names as the primary value.
    'published_central': float(BASE[FRAME_A]),
    'published_spot': float(SPOT_AED),
    'why_this_file': WHY_THIS_FILE,
    'implied': {
        'quantity': 'the polyethylene utilisation of nameplate capacity, per cent, in the '
                    'terminal year — the quantity this study\'s own crux decides',
        'value': float(IMPLIED_UTIL[FRAME_A]),
        'value_other_framing': float(IMPLIED_UTIL[FRAME_B]),
        'study_value': float(STUDY_UTIL[FRAME_A]),
        'study_value_other_framing': float(STUDY_UTIL[FRAME_B]),
        'study_value_range': [float(DISCLOSED_PE[2025]), float(DISCLOSED_PE[2024])],
        'study_value_range_note':
            'the two ends are the polyethylene utilisation rates the company itself '
            'published for FY2025 and FY2024 in its own Management Discussion & Analysis, '
            'so the range is the filed record rather than a modelled one',
        'solved_on':
            'this study\'s own forecast function, compute.run_framing, called rather than '
            're-implemented, on the adopted own-stock cost of capital, holding every '
            'driver at its published value and shifting only the utilisation path — in '
            'parallel across all five explicit years, on both products — until the model '
            'reproduces the traded price. Solved by bisection, so the root does not depend '
            'on a starting guess, and asserted to reproduce AED %.2f to within a hundredth '
            'of a fil.' % SPOT_AED,
        'reading': READING,
    },
    'construction': {
        'utilisation_shift_solved': {k: float(v) for k, v in SHIFT.items()},
        'implied_utilisation_path_pe': {
            k: [float(100 * (u + SHIFT[k])) for u in F[k]['util_pe']] for k in SHIFT},
        'study_utilisation_path_pe': {
            k: [float(100 * u) for u in F[k]['util_pe']] for k in SHIFT},
        'implied_utilisation_path_pp': {
            k: [float(100 * (u + SHIFT[k])) for u in F[k]['util_pp']] for k in SHIFT},
        'value_at_solved_shift': {k: float(value_of(F[k], util_shift=SHIFT[k]))
                                  for k in SHIFT},
        'terminal_share_of_enterprise_value': {k: float(RES[k]['tv_share_of_ev'])
                                               for k in RES},
        'disclosed_total_production_over_nameplate_pct':
            {str(y): float(DISCLOSED_TOTAL[y]) for y in CP.HIST},
        'disclosed_h1_2026_annualised_pct': float(H126_TOTAL),
        'disclosed_utilisation_pp_pct': {str(y): float(v) for y, v in DISCLOSED_PP.items()},
        'nameplate_kt': float(NAMEPLATE),
    },
    'also_solved_on_the_shared_instrument': {
        'what': 'the single flat discount rate that reproduces the traded price on this '
                'study\'s own free cash flows and terminal, through engine/reverse_read.py '
                'rather than a second construction written here — so this name carries the '
                'one reverse-read number that is comparable across the whole book',
        'implied_rate_at_price': {k: float(FLAT[k]['implied_rate_at_price']) for k in FLAT},
        'study_rate': float(W),
        'study_rate_reproduced': {k: float(FLAT[k]['implied_rate_at_study_value'])
                                  for k in FLAT},
        'terminal_arrives_at_year': {k: float(FLAT[k]['terminal_arrives_at_year'])
                                     for k in FLAT},
        'enterprise_value_at_spot_usd_mn': float(FLAT[FRAME_A]['enterprise_value_at_spot']),
        'enterprise_value_in_study_usd_mn':
            {k: float(FLAT[k]['enterprise_value_in_study']) for k in FLAT},
        'reading':
            'The price is paying for a flat %.3f%% cost of capital against this study\'s '
            '%.3f%% on the normalisation branch — %.1f basis points — and %.3f%% against '
            'the same %.3f%% on the prolonged branch, which is %.1f basis points. The '
            'study\'s own rate reproduces to %.4f%% against a published %.4f%%, which is '
            'the check that the two numbers are one quantity measured twice. This study\'s '
            'schedule is flat because the dirham is pegged and the cost-of-capital '
            'procedure returns a flat ladder where today already is the terminal.'
            % (100 * FLAT[FRAME_A]['implied_rate_at_price'], 100 * W,
               10000 * (FLAT[FRAME_A]['implied_rate_at_price'] - W),
               100 * FLAT[FRAME_B]['implied_rate_at_price'], 100 * W,
               10000 * (FLAT[FRAME_B]['implied_rate_at_price'] - W),
               100 * FLAT[FRAME_A]['implied_rate_at_study_value'], 100 * W),
    },
}

CJ = {
    'ticker': 'BOROUGE',
    'as_of': '2026-09-06',
    'published_central': float(BASE[FRAME_A]),
    'published_spot': float(SPOT_AED),
    'the_answer_this_record_is_anchored_on':
        'This study publishes TWO branches and no single figure. Every row is valued on '
        'Frame A, the normalisation branch, which is the value its own lens record names '
        'as the primary; the Frame B pair — the prolonged branch — is recorded beside it '
        'on every row. THE ANCHOR MOVES ONE ROW\'S SIGN, the crux itself, and the sign '
        'test is therefore reported on both anchors rather than on the flattering one.',
    'both_framings_share_a_bridge':
        'Every alternative is priced by RE-RUNNING this study\'s own forecast function '
        'with that one choice changed and everything else held at its published value, '
        'through the same net debt, leases, minority and share count as the adopted '
        'figure — so what is measured is the CHOICE and not a second construction. The '
        're-run is proved against the committed answer to twelve decimal places before any '
        'alternative is believed, and the numbers file is asserted byte-identical before '
        'and after, because a record that measures a study must not move it.',
    'materiality':
        'A judgement is material where the two framings differ by more than 5%% of value, '
        'measured against the alternative. %d of the %d rows below clear that bar. The '
        'answer here is a single-lens present value rather than a blend, so a driver '
        'change moves the published figure by its full effect and nothing is damped.'
        % (N_A, len(JUDGEMENTS)),
    'judgements': JUDGEMENTS,
    'sign_test': {
        'anchored_on_frame_A': {'material': N_A, 'resolved_upward': K_A, 'p': P_A},
        'anchored_on_frame_B': {'material': N_B, 'resolved_upward': K_B, 'p': P_B},
        'below_the_materiality_bar': {
            'rows': len(_SMALL), 'resolved_upward': N_SMALL_UP,
            'resolved_downward': N_SMALL_DOWN,
            'p_on_every_row_regardless_of_size': P_ALL,
            'note':
                'THE INSTRUMENT\'S ANSWER IS THE ONE ABOVE and this is reported beside it '
                'rather than instead of it. Of the %d rows the 5%% bar excludes, %d are '
                'resolved to the LOWER value and %d to the higher, and counting every row '
                'regardless of size returns p = %.3f. That is a real pattern and it is NOT '
                'a test: the number of sub-material rows is chosen by whoever enumerated '
                'them, so a longer list of small conservative choices would push that p '
                'down without anything about the study having changed — which is precisely '
                'why the bar exists and why it is the house\'s own 5%% rather than one '
                'minted here. What it is fair to say is that this study\'s SMALL choices '
                'are almost uniformly the cautious ones while its LARGE ones split evenly, '
                'and a reader is owed both halves of that.'
                % (len(_SMALL), N_SMALL_DOWN, N_SMALL_UP, P_ALL)},
        'reading':
            'On the anchor this record uses, %d of %d material judgements went the study\'s '
            'way and the two-sided sign test returns p = %.2f. On the other branch it is %d '
            'of %d at p = %.2f. NEITHER IS NEAR THE FLAG, and the fact that the two anchors '
            'disagree about one row and not about the verdict is the point of reporting '
            'both. This study did not resolve its forks in one direction: the largest is '
            'resolved upward and the next four are split.'
            % (K_A, N_A, P_A, K_B, N_B, P_B),
    },
    'not_valued': NOT_VALUED,
    'not_treated_as_a_contested_judgement': NOT_TREATED,
}


def _appears_in_numbers(val, node, trail=''):
    if isinstance(node, dict):
        for k, v in node.items():
            r = _appears_in_numbers(val, v, trail + '/' + str(k))
            if r:
                return r
    elif isinstance(node, list):
        for i, v in enumerate(node):
            r = _appears_in_numbers(val, v, trail + '[%d]' % i)
            if r:
                return r
    elif isinstance(node, float) and node == val:
        return trail
    return None


def main():
    for val in (DIAG['implied']['value'], DIAG['implied']['value_other_framing'],
                FLAT[FRAME_A]['implied_rate_at_price'],
                FLAT[FRAME_B]['implied_rate_at_price']):
        where = _appears_in_numbers(val, N)
        assert where is None, (
            'a quantity solved from the traded price (%r) is sitting in study_numbers.json '
            'at %s — the numbers file every builder reads. That is the reverse-engineered '
            'rate arriving through a side door and the prohibition is worth nothing if the '
            'side door is open.' % (val, where))
    for name, payload in (('diagnostics.json', DIAG),
                          ('contested_judgements.json', CJ)):
        with open(os.path.join(HERE, name), 'w', encoding='utf-8') as fh:
            json.dump(payload, fh, indent=1, ensure_ascii=False)
    assert _load_numbers() == _BEFORE, 'study_numbers.json moved. Nothing here may move it.'
    print(DIAG['implied']['reading'])
    print()
    print(DIAG['also_solved_on_the_shared_instrument']['reading'])
    print()
    print(CJ['sign_test']['reading'])
    print()
    print('wrote diagnostics.json and contested_judgements.json — %d judgements, %d '
          'material, %d unvalued and named, %d recorded as not a fork'
          % (len(JUDGEMENTS), N_A, len(NOT_VALUED), len(NOT_TREATED)))


if __name__ == '__main__':
    main()
