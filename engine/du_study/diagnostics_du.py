#!/usr/bin/env python3
"""DU — the two output records [R-ENF-05], COMPUTED rather than remembered.

WHAT THIS WRITES, AND WHY IT IS A SCRIPT RATHER THAN A FILE. diagnostics.json and
contested_judgements.json are read by an outside gate and by nobody else. An artefact
every reader reads and nothing writes is a number frozen at the date somebody last typed
it [R-ENF-06], so both are generated here, from this study's own model, at every run.

THE REVERSE READ. This study states what IT believes and nowhere states what the PRICE
believes, and the two are the same model read backwards. THE QUANTITY IS THIS STUDY'S OWN
CRUX, in the study's own words: "THE JUDGEMENT THAT IS LIVE, AND THE ONE THE WHOLE STUDY
TURNS ON, IS THE REQUIRED RETURN". So the headline solve is THE SINGLE FLAT DISCOUNT RATE
that reproduces the traded price on this study's own free cash flows, terminal value and
bridge — which is also the shared instrument (engine/reverse_read.py), so this name carries
the one number comparable across the book. TWO MORE ARE SOLVED BESIDE IT, because the
headline rate has no exact company-disclosed counterpart and these do: the BETA the price
implies, against a measured regression a reader can check, and the TERMINAL GROWTH the price
implies, against the 2% du's own audited accounts disclose in note 9 of the FY2025 statements.

THE COMPANY'S OWN NUMBERS COME FROM THE COMPANY'S OWN FILING. Note 9 of the FY2025 audited
consolidated financial statements (KPMG Lower Gulf, unmodified opinion 9 February 2026),
held at src/FS_FY2025.pdf with its extracted text beside it, states the goodwill
impairment test's key assumptions: "a pre-tax discount rate of 8.84% (2024: 8.40%) based
on the Company's weighted-average cost of capital" and "terminal growth rate of 2%". Those
are read out of that file at run time rather than typed here, so a changed filing breaks
the build instead of printing a stale figure. THE DISCOUNT RATE IS PRE-TAX AND THE STUDY'S
IS POST-TAX; that basis break is stated wherever the figure appears and NO CONVERSION IS
MADE, because the company publishes neither the cash-flow stream nor the tax profile the
gross-up would need, and an invented conversion is worse than a named gap [R-ENF-04].

THE SOLVE MOVES ONE THING. Every driver stays at its published value and only the solved
quantity moves, until this study's own chain reproduces the traded price. The chain is the
SHIPPED one — compute.py is imported and called, or re-run through its own audit-override
harness, never re-implemented, because a reverse read on a re-implementation grades a
different model.

IT IS A DIAGNOSTIC AND NOTHING READS IT BACK. A quantity solved from a price and then used
in the valuation is the reverse-engineered rate the protocol prohibits outright, arriving
through a side door; assert_reverse_dcf() refuses any study whose builders read this file,
and this generator additionally asserts before writing that no solved value appears
anywhere in study_numbers.json.

THE SIGN TEST. Any single contested choice is defensible; a study resolving every one of
them the same way and never noticing is not. Every alternative below is priced by RE-RUNNING
this study's own model with that one choice changed and everything else held at its
published value, through the same leases, cash, investees, share count, accretion and
dividend deduction as the adopted figure — so what is measured is the CHOICE and not a
second construction. WHERE THE STUDY ALREADY PUBLISHES AN ALTERNATIVE ON THE TERMINAL
CONSTRUCTION IT RETIRED, THE LIKE-FOR-LIKE FIGURE IS COMPUTED HERE AND THE PUBLISHED ONE IS
NAMED BESIDE IT, because comparing a sanctioned terminal with a retired one measures the
terminal rather than the choice.

NOTHING HERE MOVES THE STUDY. compute.py is imported with its output redirected to a
temporary file, and study_numbers.json is required to be byte-identical before and after
AND to equal what that import produces.

    python3 diagnostics_du.py     writes diagnostics.json + contested_judgements.json
"""
import contextlib
import io
import json
import math
import os
import re
import subprocess
import sys
import tempfile
from math import comb

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, ENGINE)

NUMBERS = os.path.join(HERE, 'study_numbers.json')
FS_FY2025_TEXT = os.path.join(HERE, 'src', 'FS_FY2025.txt')
AS_OF = '2026-09-06'
TMP = tempfile.mkdtemp(prefix='du_diag_')


def _numbers_bytes():
    with open(NUMBERS, 'rb') as fh:
        return fh.read()


# THE IMPORT IS ALSO A WRITE, AND IT IS SENT SOMEWHERE ELSE RATHER THAN TRUSTED.
# compute.py writes its numbers file at import; DU_OUT redirects that write to a scratch
# path so the committed file is not touched at all, and the two are then compared — if
# importing the model to measure it failed to reproduce the model, this stops.
_BEFORE = _numbers_bytes()
os.environ['DU_OUT'] = os.path.join(TMP, 'import_check.json')
_cwd = os.getcwd()
os.chdir(HERE)
with contextlib.redirect_stdout(io.StringIO()):
    import compute as CP                                              # noqa: E402
os.chdir(_cwd)
import reverse_read as RR                                             # noqa: E402

assert _numbers_bytes() == _BEFORE, (
    'importing compute.py changed study_numbers.json. This record measures the study; it '
    'does not move it.')
with open(os.environ['DU_OUT'], 'rb') as fh:
    assert fh.read() == _BEFORE, (
        'importing compute.py does not reproduce the committed study byte for byte, so '
        'nothing measured here is a measurement of the delivered answer.')

N = json.loads(_BEFORE)
V = CP.V
SPOT = float(N['spot'])
CENTRAL = float(N['central'])
BASE = float(CP.dcf_ps)
assert abs(BASE - CENTRAL) < 1e-12, (BASE, CENTRAL)


# ---------------------------------------------------------------------------
# the two ways of re-running this study with one choice changed
# ---------------------------------------------------------------------------
def price_inputs(**inputs):
    """Re-run the WHOLE chain through compute.py's own audit-override harness.

    The harness writes beside the committed file and never over it; DU_OUT sends even
    that copy to scratch. Used for every input the register carries, so the cost of
    capital, the glide, the terminal and the accretion are all re-derived by the study's
    own code rather than patched by this one.
    """
    out = os.path.join(TMP, 'ovr.json')
    env = dict(os.environ,
               DU_OVERRIDE=json.dumps({'inputs': inputs, 'flags': {}}),
               DU_OUT=out)
    r = subprocess.run([sys.executable, 'compute.py'], cwd=HERE, env=env,
                       capture_output=True)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.decode()[-800:])
    with open(out, encoding='utf-8') as fh:
        return float(json.load(fh)['central'])


def bridge(ev):
    """This study's OWN bridge, accretion and dividend deduction, on a new enterprise value."""
    return ((ev - CP.LEASE + CP.NETCASH + CP.INVEST) / CP.SH) * CP.ROLL - V['div_between']


@contextlib.contextmanager
def patched(**attrs):
    old = {k: getattr(CP, k) for k in attrs}
    for k, val in attrs.items():
        setattr(CP, k, val)
    try:
        yield
    finally:
        for k, val in old.items():
            setattr(CP, k, val)


def at_cost_of_capital(we, wt, ke):
    """The study's own scenario engine at a different cost of capital.

    The accretion to the price anchor is rebuilt too: this study values at 31 December
    2025 and rolls forward at its own cost of equity, so a cost-of-capital alternative
    that left the roll alone would price two different rates in one answer.
    """
    with patched(wacc_exp=we, wacc_term=wt, ROLL=(1.0 + ke) ** CP.T_ANCHOR):
        return CP.dcf_scenario()


def at_rf(rf_):
    """A parallel shift of the whole risk-free path, on the study's own construction."""
    d = rf_ - V['rf']
    ke = (rf_ - V['sov_spread_market_observed']) + V['beta'] * V['erp_market_basis']
    we = CP.we_exp * ke + CP.wd_exp * CP.kd_at
    ket = ((V['rf_term'] + d) - V['sov_spread_market_observed']) + V['beta'] * V['erp_term']
    wt = (1 - V['wd_term']) * ket + V['wd_term'] * CP.kd_term_at
    return at_cost_of_capital(we, wt, ke)


def at_g(g_nom):
    """A different terminal growth through the sanctioned terminal module and this
    study's own explicit window, which does not depend on the terminal rate."""
    return bridge(CP.pv_explicit + CP._terminal_at(g_nom).tv * CP.df[-1])


# EVERY INSTRUMENT IS PROVED AGAINST THE COMMITTED ANSWER BEFORE ANY ALTERNATIVE IS
# BELIEVED. A harness that does not reproduce the study at the study's own parameters is
# measuring something else, and the difference would read as a disagreement.
assert abs(bridge(CP.ev) - BASE) < 1e-12, bridge(CP.ev)
assert abs(at_cost_of_capital(CP.wacc_exp, CP.wacc_term, CP.ke_exp) - BASE) < 1e-12
assert abs(at_rf(V['rf']) - BASE) < 1e-12, at_rf(V['rf'])
assert abs(at_g(V['g_term']) - BASE) < 1e-9, at_g(V['g_term'])
assert abs(CP.dcf_scenario() - BASE) < 0.02
assert abs(price_inputs(beta=V['beta']) - BASE) < 1e-12


# ---------------------------------------------------------------------------
# what the company itself discloses, read out of its own audited filing
# ---------------------------------------------------------------------------
with open(FS_FY2025_TEXT, encoding='utf-8', errors='ignore') as _fh:
    FILING_TEXT = _fh.read()


def in_filing(x):
    """A figure this record quotes from the accounts must appear IN the accounts, printed
    as the filing prints it. Cheaper than re-parsing a table and it fails just as loudly:
    a remembered number that has drifted stops the build instead of reaching a reader."""
    s = format(x, ',.0f')
    assert s in FILING_TEXT, 'the FY2025 filing does not print %s' % s
    return x


# Note 7's own figures for the right-of-use book, verified against the filing, and the
# life they imply on the same identity the study uses for every other asset class.
ROU_GROSS = in_filing(3726888.0)
ROU_CHARGE = in_filing(364063.0)
ROU_LIFE_DERIVED = ROU_GROSS / ROU_CHARGE
_lt = re.search(r'average lease term is ([\d.]+) years', FILING_TEXT)
assert _lt, 'note 7 no longer states an average lease term; do not carry a remembered one'
LEASE_TERM_DISCLOSED = float(_lt.group(1))


def _disclosed_note9():
    """Note 9, FY2025 audited consolidated financial statements, read at run time.

    Typed here the figures would be a memory; read out of the filing they break the build
    if the filing changes. SIGCM clause 1: the company's own statements, never a vendor.
    """
    txt = FILING_TEXT
    m = re.search(r'pre-tax discount rate of ([\d.]+)%\s*\((\d{4}):\s*([\d.]+)%\)', txt)
    g = re.search(r'terminal growth rate of ([\d.]+)%', txt)
    assert m and g, 'note 9 no longer reads as it did; do not carry a remembered figure'
    return {
        'pre_tax_discount_rate_fy2025': float(m.group(1)) / 100.0,
        'pre_tax_discount_rate_fy2024': float(m.group(3)) / 100.0,
        'terminal_growth_rate': float(g.group(1)) / 100.0,
        'source': ('note 9 (Goodwill), audited consolidated financial statements for the '
                   'year ended 31 December 2025, KPMG Lower Gulf, unmodified opinion '
                   '9 February 2026, held at src/FS_FY2025.pdf — the key assumptions of '
                   'the fixed-line cash-generating unit value-in-use calculation, quoted '
                   'by the company as "a pre-tax discount rate of 8.84% (2024: 8.40%) '
                   'based on the Company\'s weighted-average cost of capital" and '
                   '"terminal growth rate of 2%, determined based on management\'s '
                   'estimate of the long-term cash flow growth rate"'),
        'basis_warning': ('THE DISCOUNT RATE IS PRE-TAX AND ON ONE CASH-GENERATING UNIT; '
                          'this study discounts group cash flows at a post-tax weighted '
                          'cost of capital. No conversion is made and none is derivable: '
                          'the gross-up defined by the accounting standard needs the '
                          'unit\'s own cash flows and tax profile, which the company does '
                          'not publish. It is reported as disclosed. The TERMINAL GROWTH '
                          'rate carries no such break — it is the same quantity this '
                          'study states, and the company states the same number.'),
    }


DISCLOSED = _disclosed_note9()


# ===========================================================================
# 1. THE REVERSE READ
# ===========================================================================
# (a) THE SHARED INSTRUMENT: the single flat discount rate.
#
# The price is carried back to the study's own valuation date before it is compared with
# the study's own cash flows. This study values at 31 December 2025 and accretes 246 days
# to the 3 September 2026 price anchor, deducting the dividends that went ex in between,
# so the traded price has to travel the same road backwards or the two are dated
# differently and the rate absorbs the difference.
SPOT_AT_VALUATION_DATE = (SPOT + V['div_between']) / CP.ROLL
T_MID, TIMES_HOW = RR.resolve_times({}, CP.df, CP.fwd)
FLAT = RR.read(fcff=CP.fcff, t_mid=T_MID, tv=CP.tv, wacc_terminal=CP.wacc_term,
               g=V['g_term'], df_last=CP.df[-1], df_tv=CP.df[-1],
               ev_study=CP.ev, equity_study=CP.eq_val, shares_mn=CP.SH,
               spot=SPOT_AT_VALUATION_DATE)
# the check that the two rates are one quantity measured twice: the rate reproducing the
# study's own enterprise value must sit inside the study's own glide
assert CP.wacc_term - 1e-6 <= FLAT['implied_rate_at_study_value'] <= CP.wacc_exp + 1e-6, FLAT

# (b) THE BETA the price is paying for, solved on the whole chain.
#
# Bisection rather than a solver with a starting guess: value falls monotonically in beta
# over this interval, so the root is unique and the answer cannot depend on where the
# search began.
def _solve_beta(lo=V['beta'], hi=2.0):
    assert price_inputs(beta=lo) > SPOT > price_inputs(beta=hi)
    for _ in range(48):
        mid = 0.5 * (lo + hi)
        if price_inputs(beta=mid) > SPOT:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


BETA_IMPLIED = _solve_beta()
assert abs(price_inputs(beta=BETA_IMPLIED) - SPOT) < 1e-4

# (c) THE TERMINAL GROWTH the price is paying for, on the sanctioned terminal module.
#
# The module REFUSES below a certain growth rate — at that point the terminal free cash
# flow exceeds terminal profit and a going concern would be distributing more than it
# earns for ever — so the floor is found first and the solve runs inside it. The floor is
# reported: a reverse read that quietly stops at an arbitrary bound is not one.
def _lowest_buildable_g(lo=-0.20, hi=V['g_term']):
    for _ in range(120):
        mid = 0.5 * (lo + hi)
        try:
            at_g(mid)
            hi = mid
        except CP.TERMVAL.TerminalRefused:
            lo = mid
    return hi


G_FLOOR = _lowest_buildable_g()
G_FLOOR_VALUE = at_g(G_FLOOR)
assert G_FLOOR_VALUE < SPOT, (
    'the price cannot be reached by terminal growth alone; say so rather than reporting a '
    'bound as an answer')


def _solve_g(lo, hi):
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if at_g(mid) < SPOT:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


G_IMPLIED_NOM = _solve_g(G_FLOOR, V['g_term'])
G_IMPLIED_REAL = (1.0 + G_IMPLIED_NOM) / (1.0 + CP.PI_TERM) - 1.0
assert abs(at_g(G_IMPLIED_NOM) - SPOT) < 1e-4


# ===========================================================================
# 2. THE CONTESTED JUDGEMENTS
# ===========================================================================
JUDGEMENTS = []


def judge(name, adopted, alternative, value_alternative, why, **extra):
    va, vb = BASE, float(value_alternative)
    row = dict(name=name, adopted=adopted, alternative=alternative,
               value_adopted=va, value_alternative=vb,
               share_of_value=abs(va - vb) / abs(vb),
               direction=('the study adopted the higher-value framing' if va > vb else
                          'the study adopted the lower-value framing' if va < vb else
                          'the two framings give the same value'),
               why=why)
    row.update(extra)
    JUDGEMENTS.append(row)


# --- the architecture ------------------------------------------------------
judge('the central: one lens against the retired four-lens blend',
      'the cash-flow lens alone IS the central, AED %.4f, with the relative multiple and '
      'the book floor published beside it as cross-checks' % BASE,
      'the retired %d/%d/%d/%d blend of cash flow, relative multiple, normalised earnings '
      'power and book, AED %.4f'
      % (round(100 * CP.RETIRED_BLEND_W['dcf']), round(100 * CP.RETIRED_BLEND_W['relative']),
         round(100 * CP.RETIRED_BLEND_W['normalized']), round(100 * CP.RETIRED_BLEND_W['book']),
         CP.RETIRED_BLEND_VALUE),
      CP.RETIRED_BLEND_VALUE,
      'The weights were typed, they had never cleared an out-of-sample test, and two of the '
      'four lenses they weighted are not among the permitted cross-checks for this class at '
      'all. This is the single largest fork in the record and the adopted side is the '
      'higher-value one by AED %.2f a share. What the blend concealed here was the SIZE of '
      'the disagreement rather than its direction: it reported a fifth of the gap this '
      'study\'s own primary lens holds against the market.'
      % (BASE - CP.RETIRED_BLEND_VALUE))

judge('the crux: the required return, as the study itself frames it',
      'du\'s own measured beta of %.4f sets the cost of equity and the terminal is '
      'capitalised at the resulting rate, whose exit multiple is %.2fx forward EBITDA'
      % (V['beta'], CP.tv_implied_mult),
      'no re-rating: du\'s OWN current trailing enterprise multiple of %.2fx held into '
      'perpetuity instead, which is the market\'s own required return revealed'
      % CP.ev_ebitda_now,
      CP.dcf_ps_mkt_term,
      'The study names this "the judgement that is live, and the one the whole study turns '
      'on", computes both and publishes them side by side without averaging. The adopted '
      'side asks a reader to believe a %+.0f%% re-rating of the multiple du trades on today '
      'and is worth AED %.2f a share more than refusing to. Both readings sit on the same '
      'explicit window, the same bridge and the same accretion, so this row measures the '
      'terminal capitalisation and nothing else.'
      % (100 * (CP.tv_implied_mult / CP.ev_ebitda_now - 1), BASE - CP.dcf_ps_mkt_term))

# --- the fiscal regime -----------------------------------------------------
_TAXB = CP.taxB_path
_PS_B_LIKE = CP.dcf_scenario(tax=_TAXB[0])
judge('the post-2029 fiscal regime',
      'the current construction persists — a 38%% federal royalty plus 9%% corporate income '
      'tax, a combined %.2f%% of pre-royalty profit, which is the audited FY2025 rate and '
      'which the company itself disclosed as extended to 2027-2029 on the same structure'
      % (100 * CP.TAX),
      'reversion to the pre-2024 construction — 15%% of regulated revenue plus 30%% of '
      'regulated profit, an effective %.1f%% falling to %.1f%%, which is what it actually '
      'took in FY2023' % (100 * _TAXB[0], 100 * _TAXB[-1]),
      _PS_B_LIKE,
      'The legislation runs to 2026 on the face of du\'s own H1-2026 notes, so the tail '
      'beyond the disclosed extension is genuinely open and the adopted side is the '
      'higher-value one by AED %.2f a share. THE FIGURE RECORDED HERE IS NOT THE ONE THE '
      'STUDY PUBLISHES and the difference is a basis break rather than a disagreement: the '
      'study\'s published AED %.4f is computed on the terminal construction this house '
      'retired, whose own base case is AED %.4f rather than AED %.4f, so comparing it with '
      'the adopted figure would measure the terminal rather than the regime. The like-for-'
      'like figure above holds the fiscal take flat at framing B\'s own first-year rate '
      'through the sanctioned terminal; at its last-year rate of %.1f%% it is AED %.4f, so '
      'nothing here turns on which year is used.'
      % (BASE - _PS_B_LIKE, CP.dcf_ps_B,
         CP.dcf_at(CP.wacc_exp, CP.wacc_term, V['g_term']), BASE,
         100 * _TAXB[-1], CP.dcf_scenario(tax=_TAXB[-1])),
      value_alternative_as_the_study_publishes_it=float(CP.dcf_ps_B),
      like_for_like_note=('priced on the sanctioned terminal so the row measures the '
                          'regime, not the terminal construction'))

# --- the cost of capital ---------------------------------------------------
_PS_RF_LONG = at_rf(V['rf_alt_long'])
_PS_RF_SHORT = at_rf(V['rf_alt'])
judge('the risk-free tenor',
      'the January-2031 federal AED Treasury bond at %.2f%%, the live anchor at the '
      'valuation date' % (100 * V['rf']),
      'the February-2033 AED Islamic Treasury Sukuk second tap at %.2f%%, the longest '
      'federal AED tenor held and the one closest to matching a perpetual cash-flow stream'
      % (100 * V['rf_alt_long']),
      _PS_RF_LONG,
      'There is no liquid ten-year AED point, so the tenor choice is a real range and the '
      'study publishes it as one — the adopted rate sits BETWEEN its two alternatives, and '
      'the other reading, the peg-extrapolated %.2f%%, is worth AED %.4f, which puts the '
      'adopted side on the HIGHER-value half of that pair. The alternative recorded here is '
      'the longer-tenor one because a perpetuity is discounted at a tenor-matched rate, and '
      'on that reading the adopted side is the lower-value one by AED %.2f a share. ONE '
      'THING CUTS FOR THE ADOPTED SIDE AND IT IS THIS STUDY\'S OWN: run end to end, the '
      'longer-tenor rate nets to a DEFAULT-FREE risk-free of %.2f%%, below the matched-tenor US '
      'Treasury of %.2f%%, which the study\'s own no-arbitrage floor refuses under a hard '
      'peg — so the figure above is what the alternative is worth, not a construction this '
      'study could adopt.'
      % (100 * V['rf_alt'], _PS_RF_SHORT, _PS_RF_LONG - BASE,
         100 * (V['rf_alt_long'] - V['sov_spread_market_observed']),
         100 * V['ust_matched']),
      value_alternative_other_reading=float(_PS_RF_SHORT),
      other_reading=('the peg-extrapolated ten-year AED proxy at %.2f%%, the third rate the '
                     'study prices' % (100 * V['rf_alt'])))

_KE_ALT = CP.ke_mkt_alt
_KET_ALT = ((V['rf_term'] - V['sov_spread_damodaran_rating'])
            + V['beta'] * V['erp_rating_basis'])
_WT_ALT = (1 - V['wd_term']) * _KET_ALT + V['wd_term'] * CP.kd_term_at
_PS_ERP_ALT = at_cost_of_capital(CP.wacc_exp_mkt, _WT_ALT, _KE_ALT)
judge('the equity-risk-premium basis',
      'the market-spread basis: a %.2f%% premium against a %.2f%% observed sovereign spread '
      'stripped from the risk-free rate, so country risk enters exactly once'
      % (100 * V['erp_market_basis'], 100 * V['sov_spread_market_observed']),
      'the credit-rating basis: a %.2f%% premium against the %.2f%% published adjusted '
      'default spread, stripped on the same basis'
      % (100 * V['erp_rating_basis'], 100 * V['sov_spread_damodaran_rating']),
      _PS_ERP_ALT,
      'Both bases are published in the study\'s own cost-of-capital table, as the method '
      'requires, and the same basis is stripped as is added back on either side. The '
      'adopted one gives the HIGHER cost of equity — %.2f%% against %.2f%% — and therefore '
      'the LOWER value, by AED %.2f a share. The alternative is nonetheless one the study '
      'refuses end to end: netting the %.2f%% rating spread drives the DEFAULT-FREE '
      'risk-free rate to %.2f%%, through the matched-tenor US Treasury of %.2f%%, which '
      'cannot happen '
      'under a hard peg.'
      % (100 * CP.ke_exp, 100 * _KE_ALT, abs(BASE - _PS_ERP_ALT),
         100 * V['sov_spread_damodaran_rating'],
         100 * (V['rf'] - V['sov_spread_damodaran_rating']), 100 * V['ust_matched']))

_BETA_MEASURED = N['wacc']['beta']['beta']
_BETA_DFM = N['wacc']['beta']['dfm_alt']['beta']
_BETA_COMP = N['wacc']['beta']['composite_alt']['beta']
_PS_BETA_DFM = price_inputs(beta=_BETA_DFM)
_PS_BETA_COMP = price_inputs(beta=_BETA_COMP)
judge('the beta\'s regressor',
      'the FTSE ADX General Index, the registered regressor for this market, beta %.4f '
      '(R-squared %.3f, standard error %.4f, %d weekly observations), carried in the model '
      'at the registered %.3f — with its own standing disclosure that this is an interim '
      'regressor for a Dubai-listed name'
      % (_BETA_MEASURED, N['wacc']['beta']['r2'], N['wacc']['beta']['se'],
         N['wacc']['beta']['n'], V['beta']),
      'the DFM General Index, du\'s OWN listing venue, beta %.4f at a tighter fit '
      '(R-squared %.3f, standard error %.4f)'
      % (_BETA_DFM, N['wacc']['beta']['dfm_alt']['r2'], N['wacc']['beta']['dfm_alt']['se']),
      _PS_BETA_DFM,
      'The listing venue\'s own index explains du better and gives a LOWER beta, so the '
      'adopted regressor is the lower-value side by AED %.2f a share. The equal-weight '
      'library composite is lower still at %.4f, worth AED %.4f, and is a cross-check '
      'rather than a regressor. Every alternative here points the same way: none of them '
      'closes the disagreement with the price, all of them widen it.'
      % (_PS_BETA_DFM - BASE, _BETA_COMP, _PS_BETA_COMP),
      value_alternative_composite=float(_PS_BETA_COMP))

_PS_WD = price_inputs(wd_term=CP.wd_exp)
judge('the terminal debt weight',
      'a %.0f%% terminal debt weight, one notch above the disclosed structure, on the '
      'reasoning that a leases-only balance sheet is not a permanent target'
      % (100 * V['wd_term']),
      'the disclosed lease share of enterprise value, %.2f%%, carried into the terminal'
      % (100 * CP.wd_exp),
      _PS_WD,
      'Lease debt is cheaper after tax than equity here, so a higher assumed debt weight '
      'lowers the terminal rate and raises the value; the adopted side is the higher-value '
      'one by AED %.2f a share. The company has no drawn borrowings in any year studied, so '
      'neither figure rests on an observed capital structure.' % (BASE - _PS_WD))

# --- the terminal ----------------------------------------------------------
_G_RETIRED_NOM = 0.025
_PS_G_ALT = at_g(_G_RETIRED_NOM)
judge('terminal growth',
      'REAL growth of zero on the house inflation path, giving %.2f%% nominal — and du\'s '
      'own audited note 9 discloses a terminal growth rate of %.0f%% for its goodwill test'
      % (100 * V['g_term'], 100 * DISCLOSED['terminal_growth_rate']),
      'the %.2f%% nominal the previous edition carried, which against %.1f%% terminal '
      'inflation is real growth of %+.2f%%'
      % (100 * _G_RETIRED_NOM, 100 * CP.PI_TERM,
         100 * ((1 + _G_RETIRED_NOM) / (1 + CP.PI_TERM) - 1)),
      _PS_G_ALT,
      'The adopted side is the LOWER-value one by AED %.2f a share, and it is the one the '
      'company\'s own audited disclosure agrees with to the basis point. The alternative is '
      'a real growth rate nobody quantified — the previous edition argued the nominal figure '
      'as population growth plus inflation less price erosion, which names two real forces '
      'pointing opposite ways and puts a number on neither. A positive real terminal growth '
      'is a legitimate framing and it is priced here rather than dismissed; what it is not '
      'is a free one, because this model charges real growth for the capital it consumes at '
      'AED %smn per unit of growth.'
      % (abs(BASE - _PS_G_ALT), format(CP.INC_CAP, ',.0f')))

_LIFE_ALT = N['sens']['life_variant_years']
judge('the terminal asset life',
      '%.2f years, derived by identity from notes 6, 7 and 8 as the gross cost of every '
      'depreciable class over the year\'s own charge — a route that validates itself, since '
      'its right-of-use component derives %.2f years against the %.1f-year average lease '
      'term note 7 states outright'
      % (V['asset_life_years'], ROU_LIFE_DERIVED, LEASE_TERM_DISCLOSED),
      'the second reading of the same notes: accumulated depreciation over the same charge '
      'says the base has already taken %.2f years, which the escalation formula reaches at '
      'a life of %.2f years'
      % (V['accum_dep_owned_fy25'] / V['dep_charge_owned_fy25'], _LIFE_ALT),
      N['sens']['ps_life_variant'],
      'A longer life makes the asset base older, so the escalation of the book charge to '
      'replacement cost is larger and the terminal charge higher; the adopted side is the '
      'higher-value one by AED %.2f a share. Both readings come out of the same audited '
      'notes and neither is arbitrary. The whole grid, from %.1f to %.1f years, moves the '
      'answer about %.0f%% end to end on a terminal carrying %.0f%% of enterprise value, '
      'which is the argument for sourcing the life rather than choosing it.'
      % (BASE - N['sens']['ps_life_variant'], N['sens']['life_grid'][0],
         N['sens']['life_grid'][-1],
         100 * (N['sens']['grid_life'][0] / N['sens']['grid_life'][-1] - 1),
         100 * CP.tv_share))

with patched(rou_repl=list(CP.rou_repl_retired)):
    _PS_LEASE = CP.dcf_scenario()
judge('the lease renewal in the explicit window',
      'no lease-replacement capital charge in free cash flow, because the lease liability '
      'is deducted as debt in the bridge and charging renewal there too would bill the '
      'existing obligation twice; the renewal is carried instead inside the terminal\'s '
      'blended asset life, where the right-of-use book enters at its own %.2f years'
      % ROU_LIFE_DERIVED,
      'the retired construction: a replacement charge equal to right-of-use depreciation in '
      'every explicit year, AED %smn falling to AED %smn'
      % (format(CP.rou_repl_retired[0], ',.0f'), format(CP.rou_repl_retired[-1], ',.0f')),
      _PS_LEASE,
      'The adopted side is the higher-value one by AED %.2f a share. It is defensible on '
      'the double-charging argument and it is the looser of the two readings; the study\'s '
      'own register records actual FY2025 lease additions of AED 96mn against a right-of-'
      'use depreciation charge of AED %smn, so the retired construction was itself well '
      'above what the company spent.'
      % (BASE - _PS_LEASE, format(CP.V['rou_dep_path'][0], ',.0f')))

# --- the operating drivers -------------------------------------------------
judge('the mobile ARPU path against the mix decomposition',
      'the registered blended ARPU path, held with no drift — the disclosed subscriber and '
      'ARPU series carried forward as they stand',
      'the per-leg erosion the study\'s own mix decomposition implies, %.2f%% a year, on '
      'the finding that the flat blended ARPU is a postpaid mix tailwind offsetting '
      'underlying erosion and that the tailwind exhausts as prepaid recovers'
      % (100 * CP.leg_erosion),
      CP.dcf_mix_exhaust,
      'This is the largest operating fork in the study and the adopted side is the higher-'
      'value one by AED %.2f a share. The decomposition is the study\'s own and it is '
      'explicit that the subscriber path assumes prepaid recovers, which is exactly what '
      'removes the tailwind — so the risk is identified, priced and then not taken into the '
      'base. The split it rests on is demonstrated UNIDENTIFIED across all 21 available '
      'quarter pairs, so neither side can be settled from what the company publishes.'
      % (BASE - CP.dcf_mix_exhaust))

_UC = N['unitcost']['hist']
_FIXED_MEASURED = _UC['FY25']['fixed_cap'] / _UC['FY24']['fixed_cap'] - 1.0
_PS_FIXED = price_inputs(esc_dc_fixed=_FIXED_MEASURED)
judge('the fixed-capacity unit cost',
      'held FLAT at the reviewed H1-2026 rate, with the measured improvement stopped dead '
      'rather than projected',
      'the improvement projected at the rate the audited full years measured, %.2f%% a year '
      '(AED %.2f per subscriber per month in FY2024 against AED %.2f in FY2025)'
      % (100 * _FIXED_MEASURED, _UC['FY24']['fixed_cap'], _UC['FY25']['fixed_cap']),
      _PS_FIXED,
      'The mechanism — fibre and fixed-wireless scale plus enterprise mix — is real and the '
      'study says so; what it declines to do is project a decay rate it cannot measure. The '
      'adopted side is the lower-value one by AED %.2f a share.' % abs(BASE - _PS_FIXED))

_PS_WHOLE = price_inputs(dc_rate_wholesale=_UC['FY25']['whl_rate'])
judge('the wholesale direct-cost rate',
      'held FLAT at the reviewed H1-2026 rate of %.2f%%, the worst observation in the '
      'series, taking no credit for the recovery du\'s own commentary implies'
      % (100 * V['dc_rate_wholesale']),
      'the FY2025 audited rate of %.2f%%, the last full year' % (100 * _UC['FY25']['whl_rate']),
      _PS_WHOLE,
      'The series worsens at every observation (FY2024 %.2f%%, FY2025 %.2f%%, H1-2025 '
      '%.2f%%, H1-2026 %.2f%%) and du attributes it to a conflict-hit '
      'roaming and transit mix. Anchoring on the latest reviewed period rather than the '
      'last audited year is the house rule and here it is the lower-value side, by AED '
      '%.2f a share.'
      % (100 * _UC['FY24']['whl_rate'], 100 * _UC['FY25']['whl_rate'],
         100 * _UC['H125']['whl_rate'], 100 * _UC['H126']['whl_rate'],
         abs(BASE - _PS_WHOLE)))

_PS_ICT = price_inputs(dc_rate_ict=_UC['FY25']['ict_rate'])
judge('the ICT direct-cost rate',
      'held FLAT at the reviewed H1-2026 rate of %.2f%%, the best observation in the series'
      % (100 * V['dc_rate_ict']),
      'the FY2025 audited rate of %.2f%%, the last full year' % (100 * _UC['FY25']['ict_rate']),
      _PS_ICT,
      'The same anchoring rule as the wholesale row, applied to a series that moves the '
      'other way — FY2024 %.2f%%, FY2025 %.2f%%, H1-2026 %.2f%%, no trend in either '
      'direction. Here the rule lands on the higher-value side, by AED %.2f a share, which '
      'is the point of recording both: one rule, two directions.'
      % (100 * _UC['FY24']['ict_rate'], 100 * _UC['FY25']['ict_rate'],
         100 * _UC['H126']['ict_rate'], BASE - _PS_ICT))

_CAPEX_FY25 = V['capex_cash_hist']['FY25'] / V['rev_fy25']
_PS_CAPEX = price_inputs(capex_pct=[_CAPEX_FY25] * 5)
judge('capital intensity',
      'the registered path falling from %.1f%% of revenue to %.1f%% as the 5G build '
      'completes' % (100 * V['capex_pct'][0], 100 * V['capex_pct'][-1]),
      'held flat at the FY2025 actual cash capital intensity of %.2f%% of revenue'
      % (100 * _CAPEX_FY25),
      _PS_CAPEX,
      'The adopted path opens ABOVE the trailing actual and ends below it, so it is not a '
      'uniformly generous assumption; over the five years together it spends less, and the '
      'adopted side is the higher-value one by AED %.2f a share.' % (BASE - _PS_CAPEX))

judge('revenue against the company\'s own guidance',
      'the ground-up build at +%.1f%% FY2026 revenue growth, driven by disclosed subscriber '
      'and ARPU paths' % (100 * N['sens']['cc3']['g_build']),
      'the midpoint of du\'s own guided 4-6%% range, +%.1f%%, won on price'
      % (100 * N['sens']['cc3']['g_mid']),
      N['sens']['cc3']['price'],
      'The adopted side is the lower-value one by AED %.2f a share on the price route and '
      'AED %.2f on the volume route. Guidance is scored here and never consumed: a driver '
      'that takes a management target as an input inherits its lean instead of measuring '
      'it, so the build stays where the disclosed drivers put it and the reader is shown '
      'what the midpoint would be worth.'
      % (abs(BASE - N['sens']['cc3']['price']), abs(BASE - N['sens']['cc3']['vol'])),
      value_alternative_won_on_volume=float(N['sens']['cc3']['vol']))

_NWC_FY24 = N['nwc_hist']['FY24'] / V['rev_fy24']
_PS_NWC = CP.dcf_scenario(nwc=_NWC_FY24)
judge('working capital',
      'the FY2025 component days held constant, so net working capital stays at %.2f%% of '
      'revenue and growth RELEASES cash' % (100 * CP.nwc_pct),
      'the FY2024 audited level of %.2f%% of revenue, the most negative of the three years '
      'studied' % (100 * _NWC_FY24),
      _PS_NWC,
      'Both are audited outturns of the same structurally negative telecom working-capital '
      'cycle and the whole plausible range is worth well under a per cent; the adopted side '
      'is the lower-value one by AED %.2f a share.' % abs(BASE - _PS_NWC))

# --- the conventions -------------------------------------------------------
_EV_MID = sum(CP.fcff[i] * CP.df[i] * math.sqrt(1 + CP.fwd[i]) for i in range(5)) \
    + CP.tv * CP.df[-1]
_PS_MID = bridge(_EV_MID)
judge('the discounting convention',
      'full-year end-of-period factors on the explicit window, with the terminal brought '
      'home on the year-five factor',
      'mid-year factors on the explicit window, the terminal unchanged',
      _PS_MID,
      'Cash arrives through the year rather than on its last day, so the mid-year reading '
      'is the more usual one and it is worth AED %.2f a share more; the study calls it the '
      'less conservative choice and does not adopt it. The adopted side is the lower-value '
      'one. Computed on the study\'s own committed cash flows, forward rates and bridge.'
      % (_PS_MID - BASE))

_PS_DIV = price_inputs(div_between=0.40)
judge('the dividends stripped between the valuation date and the price anchor',
      'both distributions, AED 0.66 — the FY2025 final of AED 0.40 and the H1-2026 interim '
      'of AED 0.26, whose ex-date of 31 July 2026 falls before the anchor',
      'the FY2025 final alone, AED 0.40, on the reading that a declared but unpaid interim '
      'stays in the share',
      _PS_DIV,
      'The ex-date settles it: a share bought at the anchor does not carry a distribution '
      'that already went ex. The adopted side is the lower-value one by AED %.2f a share, '
      'and it is a correction the study made to itself.' % abs(BASE - _PS_DIV))


# ===========================================================================
# 3. WHAT COULD NOT BE VALUED, AND WHAT IS NOT A JUDGEMENT
# ===========================================================================
NOT_VALUED = [
    {'name': 'the terminal maintenance basis',
     'adopted': 'the book depreciation charge escalated to current cost over half the '
                'derived life',
     'alternative': 'replacement-cost invested capital divided by the disclosed life',
     'why_not_valued': 'the sanctioned terminal module REFUSES the alternative on this '
                       'study, in its own words, because maintenance on a disclosed life '
                       'needs BOTH a replacement-cost capital base and the life, and this '
                       'model commits no replacement-cost base: the notes give gross '
                       'HISTORICAL cost on a base about 70% depreciated. A life this desk '
                       'chose is not a disclosed life. Rather than invent the missing base '
                       'to produce a number, the fork is recorded unvalued.'},
    {'name': 'the balance-sheet date the bridge stands on',
     'adopted': 'the 31 December 2025 audited sheet, with the equity value accreted %d '
                'days to the price anchor at the cost of equity and the dividends that '
                'went ex in between deducted' % int(V['anchor_days']),
     'alternative': 'the reviewed 30 June 2026 sheet, which shows term deposits run down '
                    'to nil and lease liabilities of AED 1,735mn',
     'why_not_valued': 'moving the bridge onto the June sheet means re-cutting the '
                       'explicit window to start mid-year and dropping the accretion and '
                       'the dividend deduction with it. That is a rebuild of the model '
                       'rather than one lever moved on it, so it cannot be priced on this '
                       'study\'s own chain and is not guessed at. The study\'s own gap '
                       'review addresses it in prose: sheet, valuation date and roll agree '
                       'as they stand, and moving the sheet while still deducting the '
                       'dividends would charge the same distribution twice.'},
    {'name': 'the FY2026 EBITDA margin against the company\'s guided range',
     'adopted': 'the unit-built margin of %.2f%%, above du\'s guided 46-47%%, defended on '
                'the implied second half of %.2f%%'
                % (100 * CP.ebitda_margin[0], 100 * CP._ANCH_H2),
     'alternative': 'the guided full-year midpoint',
     'why_not_valued': 'the company guides ONE full year and every cost lever in this '
                       'model moves the whole five-year window, so imposing the guided '
                       'margin through the cost stack would price a permanent claim '
                       'against a one-year target and the two are not the same '
                       'proposition. The revenue half of the same guidance IS valued '
                       'above. The study\'s own forecast-anchor record prints the implied '
                       'second half instead, which is the testable form of the question.'},
]

NOT_A_JUDGEMENT = [
    {'name': 'the peer earnings multiple, the peer dividend yield and the sustainable '
             'return on equity',
     'why': 'they move only the cross-check lenses. The central here IS the cash-flow lens '
            'and nothing is blended into it, so these choices are worth exactly zero on '
            'the published answer; recording them as judgements at zero would pad the '
            'count with rows that cannot move it.'},
    {'name': 'the payout ratio',
     'why': 'it moves the dividend and net-cash paths and therefore the profit line '
            'through interest income, but no line of free cash flow to the firm, which is '
            'what the central is built on.'},
]


# ===========================================================================
# 4. THE SIGN TEST
# ===========================================================================
MATERIALITY = 0.05
signs = []
for j in JUDGEMENTS:
    j['material'] = abs(j['value_adopted'] - j['value_alternative']) \
        / abs(j['value_alternative']) >= MATERIALITY
    if j['material']:
        signs.append(1 if j['value_adopted'] > j['value_alternative'] else
                     (-1 if j['value_adopted'] < j['value_alternative'] else 0))
_n = len([s for s in signs if s])
_k = len([s for s in signs if s > 0])
_tail = sum(comb(_n, i) for i in range(max(_k, _n - _k), _n + 1)) / float(2 ** _n)
SIGN_P = min(1.0, 2 * _tail) if _n else None


# ===========================================================================
# 5. WRITE — after asserting nothing solved from the price is in the numbers file
# ===========================================================================
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


for _label, _val in (('the flat discount rate', FLAT['implied_rate_at_price']),
                     ('the beta', BETA_IMPLIED),
                     ('the terminal growth', G_IMPLIED_NOM)):
    _where = _hunt(N, _val)
    assert _where is None, (
        'the reverse read\'s solved %s appears in study_numbers.json at %s. A quantity '
        'solved from the traded price must not sit in the file every builder reads.'
        % (_label, _where))

DIAG = {
    'ticker': 'DU',
    'as_of': AS_OF,
    'spot': SPOT,
    'spot_date': 'DFM close, 3 September 2026, the price this edition is struck at',
    'published_central': CENTRAL,
    'published_spot': SPOT,
    'why_this_file': (
        'The reverse read — what the traded price must believe — is a DIAGNOSTIC and lives '
        'outside the numbers file every builder reads. A rate, a beta or a growth solved '
        'from a price and then used anywhere in the valuation is the reverse-engineered '
        'rate the protocol prohibits outright, arriving through a side door. Nothing in '
        'this file is an input to anything. It is COMPUTED by diagnostics_du.py, which '
        'imports the shipped model with its output redirected to scratch and asserts the '
        'committed numbers file is byte-identical before and after.'),
    'implied': {
        'quantity': ('the single flat discount rate that reproduces the traded price on '
                     'this study\'s own free cash flows, terminal value and bridge'),
        'value': FLAT['implied_rate_at_price'],
        'study_value': FLAT['implied_rate_at_study_value'],
        'study_value_schedule': [CP.wacc_exp, CP.wacc_term],
        'company_disclosed': DISCLOSED,
        'solved_on': (
            'the shared construction in engine/reverse_read.py, called rather than '
            're-implemented, on this study\'s OWN committed free cash flows, its own '
            'terminal value inverted by the identity it was built with, its own '
            'discounting times recovered from its own factors (%s) and its own '
            'enterprise-to-equity bridge — holding every driver at its published value and '
            'varying only the rate. Solved by bisection, so the root does not depend on a '
            'starting guess. THE PRICE IS CARRIED BACK TO THE STUDY\'S OWN VALUATION DATE '
            'FIRST: this study values at 31 December 2025 and accretes %d days to the '
            'price anchor while deducting the AED %.2f of dividends that went ex in '
            'between, so the traded AED %.2f is travelled backwards down the same road to '
            'AED %.4f before it meets the cash flows, or the two would be dated '
            'differently and the rate would absorb the difference. The rate solved against '
            'the study\'s OWN enterprise value is reported beside it and sits inside the '
            'study\'s own glide, which is the check that the two are one quantity measured '
            'twice.'
            % (TIMES_HOW, int(V['anchor_days']), V['div_between'], SPOT,
               SPOT_AT_VALUATION_DATE)),
        'reading': (
            'At AED %.2f the price is paying for a flat %.2f%% on this study\'s own cash '
            'flows, against the %.2f%% flat-equivalent of the schedule the study actually '
            'discounts at (%.2f%% in the explicit window gliding to %.2f%% in the '
            'terminal). The disagreement is %d basis points on ONE parameter, which is a '
            'more useful statement than "the study is %+.0f%% against the price". BESIDE '
            'IT, WHAT THE COMPANY ITSELF PUBLISHES: du\'s own audited note 9 tests its '
            'goodwill at a PRE-TAX discount rate of %.2f%% (2024: %.2f%%), described as '
            'based on the company\'s weighted-average cost of capital. That is a different '
            'basis from either figure above and no conversion is made — but it bounds the '
            'company\'s own post-tax rate from above, and both the study\'s %.2f%% and the '
            'price\'s %.2f%% sit below that bound. ON DU\'S OWN DISCLOSURE THE '
            'DISAGREEMENT IS NOT SETTLED EITHER WAY, and saying so is worth more than a '
            'comparison manufactured out of a gross-up the company gives no way to '
            'compute.'
            % (SPOT, 100 * FLAT['implied_rate_at_price'],
               100 * FLAT['implied_rate_at_study_value'],
               100 * CP.wacc_exp, 100 * CP.wacc_term,
               round(10000 * (FLAT['implied_rate_at_price']
                              - FLAT['implied_rate_at_study_value'])),
               100 * (CENTRAL / SPOT - 1),
               100 * DISCLOSED['pre_tax_discount_rate_fy2025'],
               100 * DISCLOSED['pre_tax_discount_rate_fy2024'],
               100 * FLAT['implied_rate_at_study_value'],
               100 * FLAT['implied_rate_at_price'])),
        'arithmetic': FLAT,
    },
    'also_solved_on_the_study_s_own_chain': {
        'why': ('The headline rate is comparable across the book and has no exact '
                'company-disclosed counterpart. These two do: a beta a reader can check '
                'against a measured regression, and a terminal growth the company itself '
                'states in its audited accounts. Each is solved by moving that one '
                'quantity and nothing else until the study\'s own model reproduces the '
                'traded price.'),
        'beta': {
            'quantity': 'the equity beta the traded price implies',
            'implied_by_price': BETA_IMPLIED,
            'study_value': V['beta'],
            'measured': {'beta': _BETA_MEASURED, 'r2': N['wacc']['beta']['r2'],
                         'se': N['wacc']['beta']['se'], 'n': N['wacc']['beta']['n'],
                         'ci90': N['wacc']['beta']['ci90'],
                         'window': '5 years of weekly returns',
                         'carried_in_the_model_at': V['beta'],
                         'note': ('the register rounds the regression to three decimals '
                                  'and the model runs on the rounded figure; both are '
                                  'shown so neither stands in for the other')},
            'alternatives_the_study_holds': {
                'dfm_general_own_listing_venue': _BETA_DFM,
                'equal_weight_library_composite': _BETA_COMP},
            'solved_how': (
                'bisection on compute.py\'s own audit-override harness — the whole chain '
                're-run at each step, so the cost of equity, the weights, the glide, the '
                'terminal and the accretion are all re-derived by the study\'s own code '
                'rather than patched by the diagnostic. Every other input held at its '
                'published value.'),
            'standard_errors_above_measured':
                (BETA_IMPLIED - _BETA_MEASURED) / N['wacc']['beta']['se'],
            'reading': (
                'At AED %.2f the price is paying for a beta of %.3f against a measured '
                '%.4f — %.1f standard errors above it and outside the 90%% interval of '
                '%.3f to %.3f. The company discloses no beta, so what this is put beside '
                'is a measurement: du\'s own weekly returns over five years, %d '
                'observations. Both alternative regressors the study holds give a LOWER '
                'beta (%.4f on du\'s own listing venue, %.4f on the library composite), so '
                'nothing in the regressor choice moves toward the price. A beta near one '
                'is an entirely ordinary telecom number, which is why this is recorded as '
                'a disagreement a reader can judge rather than as a defect found.'
                % (SPOT, BETA_IMPLIED, _BETA_MEASURED,
                   (BETA_IMPLIED - _BETA_MEASURED) / N['wacc']['beta']['se'],
                   N['wacc']['beta']['ci90'][0], N['wacc']['beta']['ci90'][1],
                   N['wacc']['beta']['n'], _BETA_DFM, _BETA_COMP)),
        },
        'terminal_growth': {
            'quantity': 'the terminal growth rate the traded price implies',
            'implied_by_price_nominal': G_IMPLIED_NOM,
            'implied_by_price_real': G_IMPLIED_REAL,
            'study_value_nominal': V['g_term'],
            'study_value_real': V['g_term_real'],
            'company_disclosed': DISCLOSED['terminal_growth_rate'],
            'house_terminal_inflation': CP.PI_TERM,
            'lowest_buildable_growth': G_FLOOR,
            'value_at_that_floor': G_FLOOR_VALUE,
            'solved_how': (
                'bisection on the sanctioned terminal module, called through compute.py\'s '
                'own _terminal_at, with the explicit window (which does not depend on the '
                'terminal rate) and the bridge held exactly as committed. The module '
                'refuses below %.4f%% nominal, where terminal free cash flow would exceed '
                'terminal profit and a going concern would distribute more than it earns '
                'for ever; the floor is stated and the solve runs inside it, and the value '
                'at the floor (AED %.2f) is below the price, so the root is real rather '
                'than a bound reported as an answer.'
                % (100 * G_FLOOR, G_FLOOR_VALUE)),
            'reading': (
                'At AED %.2f the price is paying for terminal growth of %.2f%% nominal — '
                'against %.1f%% terminal inflation, a REAL DECLINE of %.2f%% a year for '
                'ever. The study assumes real growth of exactly zero, and DU\'S OWN '
                'AUDITED ACCOUNTS DISCLOSE THE SAME %.0f%% TERMINAL GROWTH the study uses, '
                'in note 9\'s goodwill impairment test, "determined based on management\'s '
                'estimate of the long-term cash flow growth rate, consistent with the '
                'assumption that a market participant would make". This is the one '
                'framing where the company\'s number and the study\'s number are the same '
                'quantity on the same basis, and they agree. What the price is paying for '
                'is not on that page.'
                % (SPOT, 100 * G_IMPLIED_NOM, 100 * CP.PI_TERM, -100 * G_IMPLIED_REAL,
                   100 * DISCLOSED['terminal_growth_rate'])),
        },
    },
}

CJ = {
    'ticker': 'DU',
    'as_of': AS_OF,
    'published_central': CENTRAL,
    'published_spot': SPOT,
    'the_answer_this_record_is_anchored_on': (
        'The published central is a single lens — the cash-flow lens — so every row below '
        'is valued against AED %.4f and a driver change moves the published figure by its '
        'full effect, with nothing damped by a blend.' % CENTRAL),
    'how_each_alternative_is_priced': (
        'By RE-RUNNING this study\'s own model with that one choice changed and everything '
        'else held at its published value, through the same leases, cash, investees, share '
        'count, accretion and dividend deduction as the adopted figure — so what is '
        'measured is the CHOICE and not a second construction. Two routes are used and '
        'both are proved against the committed answer before any alternative is believed: '
        'compute.py\'s own audit-override harness, which re-derives the whole chain from a '
        'changed input, and the study\'s own scenario engine and terminal module called in '
        'process. WHERE THE STUDY PUBLISHES AN ALTERNATIVE COMPUTED ON THE TERMINAL '
        'CONSTRUCTION IT RETIRED, the like-for-like figure is computed here and the '
        'published one is named beside it, because comparing a sanctioned terminal against '
        'a retired one measures the terminal rather than the choice.'),
    'how_the_alternative_is_chosen': (
        'The alternative is the competing construction THE STUDY ITSELF NAMES — in its '
        'input register, its derivation log, its critique response or its gap review — '
        'taken as that source states it. Where the study names two competing constructions '
        'for one input, the sign is taken on the methodologically stronger one and the '
        'other is recorded on the same row, so the choice of framing is visible rather '
        'than silently favourable.'),
    'materiality': (
        'A judgement is material where the two framings differ by more than %.0f%% of '
        'value, measured against the alternative. %d of the %d rows below clear that bar.'
        % (100 * MATERIALITY, _n, len(JUDGEMENTS))),
    'judgements': JUDGEMENTS,
    'sign_test': {
        'material': _n, 'resolved_upward': _k, 'resolved_downward': _n - _k,
        'two_sided_binomial_p': SIGN_P,
        'flag': bool(SIGN_P is not None and SIGN_P < 0.05 and _n >= 3),
        'reading': (
            'Of the %d material contested judgements, %d were resolved toward the '
            'higher-value framing and %d toward the lower; the two-sided sign test gives '
            'p = %.2f, so this study is NOT flagged. The four largest forks do all run the '
            'same way — the lens architecture, the mix decomposition, the terminal '
            'capitalisation and the fiscal tail — and that is worth seeing. The two that '
            'run the other way are the risk-free tenor and the terminal growth rate, and '
            'those are not minor rows: the terminal carries %.0f%% of enterprise value and '
            'the discount rate is what this study\'s own gap review calls the single '
            'parameter of its disagreement with the market. A study resolving every '
            'material fork one way would be FLAGGED, not failed, because a company can '
            'genuinely deserve a consistent read; what this instrument reports here is '
            'that the choices are not uniform, on a name whose central sits %+.0f%% against '
            'the price.'
            % (_n, _k, _n - _k, SIGN_P if SIGN_P is not None else float('nan'),
               100 * CP.tv_share, 100 * (CENTRAL / SPOT - 1))),
    },
    'not_valued': NOT_VALUED,
    'not_treated_as_a_contested_judgement': NOT_A_JUDGEMENT,
}

for path, doc in ((os.path.join(HERE, 'diagnostics.json'), DIAG),
                  (os.path.join(HERE, 'contested_judgements.json'), CJ)):
    with open(path, 'w', encoding='utf-8') as fh:
        json.dump(doc, fh, indent=1, ensure_ascii=False, default=float)
    print('wrote %s' % os.path.basename(path))

assert _numbers_bytes() == _BEFORE, 'the committed numbers file moved. It must not.'
print('reverse read: the price implies a flat %.4f%% against the study\'s %.4f%%; '
      'a beta of %.4f against a measured %.4f; terminal growth of %.4f%% nominal against '
      '%.4f%% and the company\'s own disclosed %.2f%%'
      % (100 * FLAT['implied_rate_at_price'], 100 * FLAT['implied_rate_at_study_value'],
         BETA_IMPLIED, V['beta'], 100 * G_IMPLIED_NOM, 100 * V['g_term'],
         100 * DISCLOSED['terminal_growth_rate']))
print('sign test: %d judgements, %d material, %d up / %d down, p = %.4f%s'
      % (len(JUDGEMENTS), _n, _k, _n - _k, SIGN_P, '  FLAGGED' if CJ['sign_test']['flag'] else ''))
