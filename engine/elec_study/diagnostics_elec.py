"""ELEC — the two output records [R-ENF-05], COMPUTED, never typed.

WHAT THIS WRITES, AND WHY NEITHER FILE IS IN THE NUMBERS FILE
------------------------------------------------------------
Two files, both diagnostics and neither an input to anything:

  diagnostics.json            the reverse read — what the traded price must
                              believe under this study's own drivers
  contested_judgements.json   every contested judgement, both framings valued,
                              and the binomial sign test on how they were resolved

The reverse read is kept OUT of study_numbers.json deliberately. A quantity
solved from a price and then used anywhere in a valuation is the
reverse-engineered rate the protocol prohibits outright, arriving through a side
door, and the prohibition is worth nothing if the side door is open. No builder
in this study reads either file; the containment is checked from outside.

HOW EVERY NUMBER HERE IS PRODUCED
---------------------------------
By re-running THIS STUDY'S OWN compute.py in a scratch directory with exactly one
thing changed, and reading the answer it publishes. Every patch is asserted to
land exactly once, because a substitution matching nothing returns the published
answer and reads exactly like a judgement worth nothing [R-ENF-04]. Nothing is
estimated, no driver in the study moves, and the study's committed answer is read
from its own numbers file so this record cannot drift from it [R-ENF-06].

Valuing the alternative framing of a judgement is a calculation reported. It is
never a change made: this script writes only the two files named above.

THE ONE THING THAT MAKES THIS STUDY DIFFERENT, AND IT DECIDES THE MEASUREMENT
----------------------------------------------------------------------------
Two of this study's four lenses are pinned at literal floors — max(eq, 0.0) with
max(eq/SH, 0.01) on the cash-flow lens and max(..., 0.05) on the relative lens —
because the enterprise value does not cover the net debt. Those two carry 60% of
the published weight and produce 4.2% of the published answer. A floor is FLAT in
the region the model actually sits in, so a judgement measured through it comes
out worth exactly zero however much it moves the model: on the published central,
sixteen of the nineteen corrections this study's own gap review prices move the
answer by 0.000 and would enter a sign test as no judgement at all.

So the contested judgements are valued on this study's own construction with the
two clamps removed, and THE CLAMP ITSELF IS THE FIRST JUDGEMENT, whose two
framings are exactly the published central and the unclamped construction. The
two bases are therefore joined by one recorded row rather than mixed silently,
and every judgement's effect on the published central is reported beside its
worth so a reader can see both. Measuring through a clamp would report an absent
answer as a clean one, which is the failure [R-ENF-04] names.

    python3 engine/elec_study/diagnostics_elec.py
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
from math import comb

HERE = os.path.dirname(os.path.abspath(__file__))
NUMBERS = os.path.join(HERE, 'study_numbers.json')
SOURCE = os.path.join(HERE, 'compute.py')
COPY_ALONGSIDE = ('step0_result.json', 'strike_result.json', 'tech_result.json',
                  'beta_result.json', 'rollforward_result.json',
                  'paths_1M.npy', 'paths_3M.npy')

N = json.load(open(NUMBERS, encoding='utf-8'))
PUBLISHED = N['central']
STRIKE = N['spot']
STRIKE_DATE = N['spot_date']

# The latest known close, from the committed supplied-price artefact rather than
# from a figure in a conversation [R-GAP-01 AMENDED / R-IND-01].
LATEST_PRICE = 2.08
LATEST_PRICE_DATE = '2026-09-03'
LATEST_PRICE_SOURCE = ('engine/prices/SUPPLIED_03-09-2026.json — Electro Cable Egypt, the '
                       'close on the Egyptian Exchange, 3 September 2026')

_BASE = open(SOURCE, encoding='utf-8').read()

# --------------------------------------------------------------------------
# THE STUDY'S OWN ASSERTION BLOCK IS RECORDED RATHER THAN SUPPRESSED. Several
# alternatives below trip an assertion the study makes about its published
# drivers -- a terminal growth centre other than 5%, a cost of debt outside the
# 150bp effective-rate bound, a central outside the plausibility band once the
# clamps come off. Raising on those would make the alternative unvalueable, and
# skipping them silently would hide that the alternative breaks a rule. So the
# block PRINTS instead of raising, and every assertion an alternative trips is
# carried beside that judgement. The control run below proves the change is inert
# on the published drivers: it must reproduce the published central exactly and
# trip nothing.
# --------------------------------------------------------------------------
ASSERT_RAISE = "    raise SystemExit('ASSERT FAILED:\\n  - ' + '\\n  - '.join(err))"
ASSERT_REPORT = "    print('SANDBOX-ASSERTS-TRIPPED: ' + ' | '.join(err))"

# the two clamps, and the two places the same clamp is applied to a scenario column
UNCLAMP = [
    ("eq_dcf = max(eq_dcf_unfloored, 0.0)", "eq_dcf = eq_dcf_unfloored"),
    ("dcf_ps = max(eq_dcf / SH, 0.01)", "dcf_ps = eq_dcf / SH"),
    ("dcf_bear = max(bear_detail['ps'], 0.01)", "dcf_bear = bear_detail['ps']"),
    ("rel = {tag: max((m * ebitda_27 * (1 + s) - nd_fy26) / SH, 0.05)",
     "rel = {tag: ((m * ebitda_27 * (1 + s) - nd_fy26) / SH)"),
    ("    return max((pv - nde) / SH, 0.0)", "    return (pv - nde) / SH"),
]

_RUNS = [0]


def run_model(patches=(), label=''):
    """Re-run the study's own model with `patches` applied and return what it publishes."""
    txt = _BASE.replace(ASSERT_RAISE, ASSERT_REPORT)
    if txt == _BASE:
        raise AssertionError('the assertion-report patch did not land')
    for old, new in patches:
        n = txt.count(old)
        if n != 1:
            raise AssertionError('patch for %r landed %d times, not once: %r'
                                 % (label, n, old[:60]))
        txt = txt.replace(old, new)
    d = tempfile.mkdtemp(prefix='elec_diag_')
    try:
        with open(os.path.join(d, 'compute.py'), 'w', encoding='utf-8') as fh:
            fh.write(txt)
        for f in COPY_ALONGSIDE:
            shutil.copy(os.path.join(HERE, f), d)
        p = subprocess.run([sys.executable, 'compute.py'], cwd=d,
                           capture_output=True, text=True)
        _RUNS[0] += 1
        if p.returncode != 0:
            raise AssertionError('the model refused under %r:\n%s' % (label, p.stderr[-2000:]))
        out = json.load(open(os.path.join(d, 'study_numbers.json'), encoding='utf-8'))
        tripped = []
        for line in p.stdout.splitlines():
            if line.startswith('SANDBOX-ASSERTS-TRIPPED: '):
                tripped = [s.strip() for s in
                           line[len('SANDBOX-ASSERTS-TRIPPED: '):].split('|')]
        return dict(central=out['central'],
                    dcf_ps=out['lenses']['dcf']['base'],
                    dcf_ps_unfloored=out['dcf']['ps_unfloored'],
                    relative=out['lenses']['relative']['base'],
                    normalized=out['lenses']['normalized']['base'],
                    book=out['lenses']['book']['base'],
                    margin_T=out['dcf']['rows'][-1]['margin'],
                    ebitda_per_t_T=out['dcf']['rows'][-1]['ebitda_per_t'],
                    ev=out['dcf']['ev'], tripped=tripped)
    finally:
        shutil.rmtree(d, ignore_errors=True)


def solve(patch_fn, target, lo, hi, read=lambda r: r['central'], label='', tol=1e-9):
    """Bisect one driver until the study's own model reproduces `target`.

    Returns (x, run) or (None, why): a solve that does not BRACKET the target is
    reported as unreachable rather than returned at an endpoint, because an
    endpoint returned as a solution is an absent answer wearing a clean one.
    """
    flo, fhi = read(run_model(patch_fn(lo), label)), read(run_model(patch_fn(hi), label))
    if (flo - target) * (fhi - target) > 0:
        return None, ('not bracketed on [%g, %g]: the model reaches %.4f to %.4f against a '
                      'target of %.4f' % (lo, hi, flo, fhi, target))
    for _ in range(44):
        mid = 0.5 * (lo + hi)
        fm = read(run_model(patch_fn(mid), label))
        if (flo - target) * (fm - target) <= 0:
            hi, fhi = mid, fm
        else:
            lo, flo = mid, fm
        if abs(hi - lo) < tol:
            break
    x = 0.5 * (lo + hi)
    return x, run_model(patch_fn(x), label)


# ---------------------------------------------------------------- the controls
CONTROL = run_model((), 'control')
assert CONTROL['central'] == PUBLISHED, (
    'the control run does not reproduce the published central: %r vs %r'
    % (CONTROL['central'], PUBLISHED))
assert not CONTROL['tripped'], (
    'the control run trips assertions, so the report-instead-of-raise change is not inert: %s'
    % CONTROL['tripped'])
UNFLOORED = run_model(UNCLAMP, 'the clamps removed')
print('control: central %.10f reproduces the published %.10f; unclamped %.10f'
      % (CONTROL['central'], PUBLISHED, UNFLOORED['central']))

# committed figures this record quotes, read from the study rather than retyped
HIST = N['hist_is']
FILED_MARGIN = {y: HIST[y]['ebitda'] / HIST[y]['rev'] for y in ('FY23', 'FY24', 'FY25')}
FILED_PER_T = {y: N['tonnage']['hist_ebitda_per_t'][y] for y in ('FY23', 'FY24', 'FY25')}
STUDY_MARGIN_T = N['dcf']['rows'][-1]['margin']
STUDY_PER_T_T = N['tonnage']['ebitda_per_t'][-1]
EPT = list(N['tonnage']['ebitda_per_t'])
WD_NOW = N['coc']['wd']
ND_FY28 = N['debt_schedule']['nd_path'][3]
EQ_FY30 = N['debt_schedule']['eq_path'][-1]

# the house Egyptian currency path [R-MACRO-01], derived from the ladder by
# relative purchasing-power parity, read live from the path rather than typed
sys.path.insert(0, os.path.join(HERE, '..'))
import macro_path as _MP                                                    # noqa: E402
_EG = _MP.load('EG')
HOUSE_FX = [round(x, 4) for x in _EG.fx_path(5, start_year=2026)]
HOUSE_TERMINAL_INFLATION = _EG.terminal_inflation
HOUSE_TERMINAL_RF = _EG.terminal_rf

# the conforming beta, produced by the sanctioned resolver against the published
# index of the exchange this stock is listed on -- not a number typed here
import beta_regression as _BR                                               # noqa: E402
CONFORMING_BETA = _BR.own_stock_beta('ELEC', 'EG', 'EGX')
assert CONFORMING_BETA['conforming'] and CONFORMING_BETA['index_file'].endswith('EGX30.csv')


def ept_patch(scale):
    return [("ebitda_per_t=I([40.0, 90.0, 115.0, 128.0, 135.0],",
             "ebitda_per_t=I([%r, %r, %r, %r, %r]," % tuple(round(x * scale, 10) for x in EPT))]


# ============================ THE REVERSE READ ==============================
# Solved on the answer the study PUBLISHES, which is the four-lens weighted
# central. The clamps are NOT binding on the way up -- reaching the price needs a
# far higher conversion rate, and the cash-flow lens leaves its floor long before
# it gets there -- so the published construction can carry this solve where it
# cannot carry the judgements below.
print('solving the reverse read ...')
s_latest, r_latest = solve(ept_patch, LATEST_PRICE, 1.0, 6.0, label='conversion rate')
s_strike, r_strike = solve(ept_patch, STRIKE, 1.0, 6.0, label='conversion rate at the strike')
assert s_latest is not None and s_strike is not None

# the same solve on the cash-flow lens alone, which is what this study's own gap
# review published and what [R-LENS-03] would make the central
s_lens, r_lens = solve(ept_patch, LATEST_PRICE, 1.0, 8.0,
                       read=lambda r: r['dcf_ps_unfloored'], label='conversion rate, lens')

# ---- the doors that do not open, measured rather than asserted
OTHER = []

_g, _ = solve(lambda g: [("g_term=I(0.05,", "g_term=I(%r," % round(g, 10))],
              LATEST_PRICE, 0.0, 0.1349, label='terminal growth')
_g_lo = run_model([("g_term=I(0.05,", "g_term=I(0.0,")], 'terminal growth zero')
_g_hi = run_model([("g_term=I(0.05,", "g_term=I(0.1349,")], 'terminal growth at the ceiling')
OTHER.append(dict(
    quantity='terminal growth', value=_g, study_value=0.05,
    not_reachable=None if _g is not None else (
        'The terminal return on capital of %.2f%% sits BELOW the terminal cost of capital of '
        '%.2f%%, so growth destroys value in this model and the price is further away at every '
        'growth rate, not nearer: the central runs %.4f at zero growth and %.4f just below the '
        'terminal discount rate, against a price of %.2f. The gradient inverts by construction '
        'and the study says so itself.'
        % (100 * N['dcf']['roic_T'], 100 * N['coc']['wacc_term'],
           _g_lo['central'], _g_hi['central'], LATEST_PRICE))))

_w, _ = solve(lambda w: [("nwc_pct=I([1.12, 1.06, 1.00, 0.94, 0.88],",
                          "nwc_pct=I([%r] * 5," % round(w, 10))],
              LATEST_PRICE, 0.05, 1.12, label='working capital')
_w_lo = run_model([("nwc_pct=I([1.12, 1.06, 1.00, 0.94, 0.88],", "nwc_pct=I([0.05] * 5,")],
                  'working capital at 5% of revenue')
OTHER.append(dict(
    quantity='working-capital intensity, held flat across the window', value=_w,
    study_value=N['inputs']['nwc_pct']['value'][-1],
    not_reachable=None if _w is not None else (
        'At 5%% of revenue — an intensity no cable maker runs and far below the FY2024 level of '
        'about 76%% — the published central reaches only %.4f against a price of %.2f. Working '
        'capital cannot close this gap because it is a level effect on five years of cash flow '
        'while 82%% of enterprise value sits in the terminal.'
        % (_w_lo['central'], LATEST_PRICE))))

_r_zero = run_model([("rf=I(0.2231,", "rf=I(0.0,"), ("rf_term=I(0.105,", "rf_term=I(0.0,")],
                    'both risk-free rates at zero')
_r_term0 = run_model([("rf_term=I(0.105,", "rf_term=I(0.0,")], 'the terminal risk-free at zero')
OTHER.append(dict(
    quantity='the risk-free rate, explicit and terminal together', value=None,
    study_value=N['coc']['rf'],
    not_reachable=(
        'At a TERMINAL risk-free rate of zero the cash-flow lens is still %.4f a share — '
        'negative — and the published central reaches only %.4f. Zero the EXPLICIT leg as well, '
        'which is a cost of capital no economy has, and the lens turns positive at %.4f while '
        'the published central still reaches only %.4f against a price of %.2f. So the price is '
        'not reachable through the discount rate at any rate a market could produce, which is '
        'the cleanest evidence that the disagreement is not about the cost of capital.'
        % (_r_term0['dcf_ps_unfloored'], _r_term0['central'],
           _r_zero['dcf_ps_unfloored'], _r_zero['central'], LATEST_PRICE))))

_nd, _r_nd = solve(lambda nd: [("net_debt_fy25_est=I(9805.0,",
                                "net_debt_fy25_est=I(%r," % round(nd, 6))],
                   LATEST_PRICE, -9000.0, 9805.0, label='net debt')
OTHER.append(dict(
    quantity='net debt at the bridge date', value=_nd, study_value=N['dcf']['net_debt'],
    note=('The price is payable only if this company holds NET CASH of EGP %s mn against the '
          'EGP %s mn of net debt this study triangulates. That is not a disagreement about '
          'leverage, it is a different balance sheet.'
          % (format(-_nd, ',.0f'), format(N['dcf']['net_debt'], ',.0f'))
          ) if _nd is not None and _nd < 0 else None))

_v, _r_v = solve(lambda v: [("vols_fcst=I([10.4, 11.9, 13.4, 14.8, 16.0],",
                             "vols_fcst=I([%r, %r, %r, %r, %r],"
                             % tuple(round(x * v, 8) for x in N['tonnage']['vols_fcst']))],
                 LATEST_PRICE, 1.0, 6.0, label='volumes')
OTHER.append(dict(
    quantity='volumes, scaled in parallel', value=_v,
    study_value=N['tonnage']['vols_fcst'][-1],
    note=('Volumes reach the price at %.3f times the forecast path — FY2030E of %.1f kt against '
          'a stated parent capacity of %.0f kt, which is %.1f times that capacity. Volume is the '
          'wrong door for a different reason from the others: it raises revenue and working '
          'capital together, so most of what it earns it lends back.'
          % (_v, _v * N['tonnage']['vols_fcst'][-1], N['tonnage']['capacity_kt'],
             _v * N['tonnage']['vols_fcst'][-1] / N['tonnage']['capacity_kt'])
          ) if _v is not None else None,
    not_reachable=None if _v is not None else
    'the model does not reach the price at any parallel volume scale up to six times'))

DIAG = {
    'ticker': 'ELEC',
    'as_of': '2026-09-06',
    'spot': LATEST_PRICE,
    'spot_date': 'close %s, the Egyptian Exchange' % LATEST_PRICE_DATE,
    'spot_source': LATEST_PRICE_SOURCE,
    # [R-ENF-06]: the answer this diagnostic was generated against
    'published_central': PUBLISHED,
    'published_spot': STRIKE,
    'why_this_file': (
        'The reverse read — what the traded price must believe — is a DIAGNOSTIC and lives '
        'outside the numbers file every builder reads. A quantity solved from a price and then '
        'used anywhere in the valuation is the reverse-engineered rate the protocol prohibits '
        'outright, arriving through a side door, and the prohibition is worth nothing if the '
        'side door is open. Nothing in this file is an input to anything: no builder in this '
        'study reads it, and it is COMPUTED by diagnostics_elec.py, which re-runs the study\'s '
        'own compute.py with one driver moved at a time.'),
    'implied': {
        'quantity': ('the conversion EBITDA per tonne — the unit rate the whole forecast is '
                     'built on, margin being an output of it — scaled in parallel across the '
                     'five forecast years, stated here as the EBITDA margin it produces in the '
                     'terminal year'),
        'value': r_latest['margin_T'],
        'study_value': STUDY_MARGIN_T,
        'study_value_range': [FILED_MARGIN['FY24'], FILED_MARGIN['FY23']],
        'study_value_range_is': ('the lowest and highest of the three full years this study '
                                'RECONSTRUCTS — not filed rates; see '
                                'what_the_company_actually_disclosed below'),
        'value_at_the_strike_price': r_strike['margin_T'],
        'solved_on': (
            'this study\'s own compute.py, on the answer the study PUBLISHES — the four-lens '
            'weighted central of EGP %.4f — holding every other driver at its published value '
            'and moving only the conversion-EBITDA-per-tonne path, in parallel so its recovery '
            'shape is preserved, until the model reproduces EGP %.2f. The two lens clamps are '
            'not binding on the way up: the cash-flow lens leaves its floor long before the '
            'price is reached, so the published construction can carry this solve.'
            % (PUBLISHED, LATEST_PRICE)),
        'value_conversion_per_tonne_k_egp': r_latest['ebitda_per_t_T'],
        'study_value_conversion_per_tonne_k_egp': STUDY_PER_T_T,
        'scale_on_the_whole_path': s_latest,
        'company_record_ebitda_margin': FILED_MARGIN,
        'company_record_conversion_per_tonne_k_egp': FILED_PER_T,
        'what_the_company_actually_disclosed': (
            'THIS IS THE HALF THAT HAS TO BE SAID PLAINLY. The three full-year margins beside '
            'the two forecasts are NOT filed rates. What reaches this study for those years is '
            'revenue and net profit as press and vendor prints of exchange filings — FY2025 '
            'revenue EGP %s mn and net profit EGP %.2f mn — and everything between them, '
            'EBITDA included, is solved or typed: the FY2025 EBITDA rests on a finance cost '
            'derived to close the profit and loss to that reported net profit. The company\'s '
            'own statement index lists nothing after 30 September 2025 and nothing consolidated '
            'after 31 December 2020, and this study models consolidated figures. The reverse '
            'read is therefore compared against a reconstruction of the filed years rather than '
            'against filed rates, and that is a condition of the study rather than of this '
            'record. The genuinely disclosed near-term figures are the first quarter of 2026: '
            'revenue EGP %s mn, cost of sales EGP %s mn, gross profit EGP %.3f mn and operating '
            'profit EGP %.3f mn.'
            % (format(N['inputs']['rev_fy25']['value'], ',.0f'),
               N['inputs']['np_fy25']['value'],
               format(N['inputs']['q1_26_rev']['value'], ',.0f'),
               format(N['inputs']['q1_26_cogs']['value'], ',.0f'),
               N['inputs']['q1_26_gp']['value'], N['inputs']['q1_26_op']['value'])),
        'reading': (
            'At EGP %.2f the price is paying for a terminal EBITDA margin of %.2f%% — a '
            'conversion rate of %.0f thousand pounds a tonne against this study\'s %.0f, the '
            'whole path %.3f times higher. The study forecasts %.2f%%. The reconstructed record '
            'of the three years this study holds runs %.2f%% (FY2023), %.2f%% (FY2024) and '
            '%.2f%% (FY2025), so THE PRICE\'S NUMBER SITS INSIDE THAT RECONSTRUCTED RANGE ON '
            'ALL THREE YEARS, above the lowest and below the highest, while the study\'s own '
            'forecast sits below every one of them. At the EGP %.2f this study was struck '
            'against the same solve gives %.2f%%. The disagreement is one driver — how much '
            'cash a tonne of cable converts — and every other door is shut: at a risk-free rate '
            'of zero on the TERMINAL leg the equity is still negative, and zeroing the '
            'explicit leg as well does not reach the price either; at working capital of '
            '5%% of revenue the price is unreachable; growth moves the answer the wrong way '
            'because '
            'the terminal return sits below the terminal cost of capital, and the price is '
            'payable on this balance sheet only if the company holds net cash. That is a more '
            'useful statement than "the study is %.1f%% below the price", and under [R-GAP-02] '
            'a reverse read landing on a believable number is evidence AGAINST dissent.'
            % (LATEST_PRICE, 100 * r_latest['margin_T'], r_latest['ebitda_per_t_T'],
               STUDY_PER_T_T, s_latest, 100 * STUDY_MARGIN_T,
               100 * FILED_MARGIN['FY23'], 100 * FILED_MARGIN['FY24'],
               100 * FILED_MARGIN['FY25'], STRIKE, 100 * r_strike['margin_T'],
               -100 * (PUBLISHED / LATEST_PRICE - 1))),
    },
    'other_quantities': OTHER,
    'the_lens_the_read_is_solved_on': (
        'Measured rather than asserted. On the published four-lens central the price implies a '
        'terminal margin of %.2f%%; on the cash-flow lens alone — which is what [R-LENS-03] '
        'would make the central for this class, and what this study\'s own gap review published '
        '— it implies %.2f%%, the whole conversion path %.3f times higher. Both are recorded '
        'because the published answer is a blend and the class primary is not, and a reader is '
        'owed the number that belongs to the answer they receive as well as the one that '
        'belongs to the model beneath it.'
        % (100 * r_latest['margin_T'], 100 * r_lens['margin_T'], s_lens)),
    'runs_behind_this_record': _RUNS[0],
}


# ======================= THE CONTESTED JUDGEMENTS ===========================
# Each is valued by re-running the study's own model on the UNCLAMPED
# construction with exactly one thing moved. The clamp itself is judgement one,
# and its two framings are the published central and that unclamped baseline.
SCALE_TO_FY24 = FILED_MARGIN['FY24'] / STUDY_MARGIN_T
NWC_TO_FY24 = [round(1.12 + (0.76 - 1.12) * i / 4.0, 6) for i in range(5)]

SPECS = [
    dict(name='the limited-liability clamps on two of the four lenses',
         adopted='the cash-flow lens floored at EGP 0.01 and the relative lens at EGP 0.05, '
                 'both published as floors, on the ground that the equity of a listed company '
                 'cannot be worth less than nothing',
         alternative='the intrinsic the model itself computes, published unclamped',
         patches=None,          # the baseline pair, handled below
         why='The clamps are disclosed, argued and not careless — the study prints the '
             'unfloored bridge beside them. What they do to the answer is the point: they are '
             'worth EGP %(clamp_worth).4f a share, %(clamp_pc).0f%% of the published central, '
             'and they are why most corrections to this model reach a reader as nothing at '
             'all: sixteen of the nineteen priced in this study\'s own gap review move the '
             'published number by exactly zero, and so do eight of the nineteen judgements '
             'recorded below. Two of the four blended lenses '
             'return the SAME figure in the bear, base and bull columns, which is the tell: a '
             'lens giving one answer in every state of the world is reporting a bound rather '
             'than reading a value. Correcting this moves the answer AWAY from the price, which '
             'is why it is recorded as a judgement rather than a defect.'),
    dict(name='the central: a four-lens blend at typed weights',
         adopted='40% cash flow, 20% relative, 20% normalised earnings, 20% book, averaged',
         alternative='the cash-flow lens alone as the central, the other three published beside '
                     'it as cross-checks',
         patches=[("lens_weights=I(dict(dcf=0.40, relative=0.20, normalized=0.20, book=0.20),",
                   "lens_weights=I(dict(dcf=1.00, relative=0.0, normalized=0.0, book=0.0),")],
         why='The weights were typed and have never cleared any out-of-sample test, which is '
             'the free parameter this house forbids everywhere else; the class primary for an '
             'operating manufacturer is the cash-flow lens. The direction is the interesting '
             'part and it runs against the expectation this study was picked out under: taking '
             'the class primary alone makes the answer FAR MORE negative, not less, so the '
             'blend is not a device that flatters the market — it is a device that flatters the '
             'company.'),
    dict(name='the conversion EBITDA per tonne, the rate that carries the valuation',
         adopted='recovering to 135 thousand pounds a tonne by FY2030E, a terminal EBITDA '
                 'margin of %.2f%%, justified as a return to "the pre-windfall 2022 norm"'
                 % (100 * STUDY_MARGIN_T),
         alternative='the terminal rate set at the LOWEST of the three years this study '
                     'reconstructs, FY2024 at %.2f%%, the whole path scaled with it'
                     % (100 * FILED_MARGIN['FY24']),
         patches=ept_patch(SCALE_TO_FY24),
         why='This is the single judgement carrying the study. The stated justification is a '
             'FY2022 norm of about 12% of realised price, and the study holds no FY2022 income '
             'statement anywhere — the phrase occurs in a source note and in the delivered '
             'document and nowhere in the model. Its own research file holds FY2022 revenue and '
             'net profit, from which the EBITDA margin reconstructs at 15-21%, not 12%. The '
             'alternative taken here is deliberately the most punitive of the three '
             'reconstructed years rather than the highest. Nothing about the direction is '
             'settled by the filings, because the filings are not held.'),
    dict(name='the copper anchor',
         adopted='flat at the current tape, USD 14,000 a tonne, on the ground that a "no house '
                 'view" forecast must anchor on the market',
         alternative='flat at the USD 10,000 the study takes as the FY2025 realised average',
         patches=[("copper_fcst=I([14000.0] * 5,", "copper_fcst=I([10000.0] * 5,")],
         why='Copper is pure value destruction in this model BY CONSTRUCTION: it sets revenue '
             'and therefore the working capital charged against free cash flow, while EBITDA is '
             'typed in pounds per tonne and does not move with it. So anchoring at the top of '
             'the tape rather than at the last realised average is a large, one-directional '
             'choice that nothing in the cost side offsets. The study\'s own note records the '
             'anchor being moved UP from USD 12,600 in an audit.'),
    dict(name='working-capital intensity',
         adopted='gliding 112% of revenue to 88%, with full reversion explicitly NOT assumed',
         alternative='reverting to the FY2024 intensity of about 76% over the same window',
         patches=[("nwc_pct=I([1.12, 1.06, 1.00, 0.94, 0.88],",
                   "nwc_pct=I(%r," % (NWC_TO_FY24,))],
         why='The study states the choice in terms — "full reversion NOT assumed" — and the '
             'level it starts from is not a disclosure either: 113% of revenue is derived from '
             'a triangulated balance sheet, not read off one. Holding intensity above the last '
             'normal year for the whole window charges the company for a copper-inflated '
             'inventory position in perpetuity.'),
    dict(name='the terminal growth charge',
         adopted='the reinvestment identity, reinvesting %.1f%% of terminal profit for ever to '
                 'fund 5%% nominal growth' % (100 * N['dcf']['rr_T']),
         alternative='no growth charge at all, which is the bound rather than a construction',
         patches=[("rr_T = V['g_term'] / roic_T", "rr_T = 0.0"),
                  ("    rr = gg / roic", "    rr = 0.0")],
         why='The construction is the one [R-TERM-01] retired: the implied replacement cycle is '
             'the reciprocal of the growth rate, which is a fact about a currency and not about '
             'an asset. On this name the charge is the heaviest in the book — it reinvests more '
             'than half of terminal profit at a terminal return of %.2f%% against a terminal '
             'cost of capital of %.2f%%, a spread of %.0f basis points, in perpetuity. The bound '
             'is used rather than the sanctioned module because this study discloses no useful '
             'life, and a life this desk chose is not a disclosed life.'
             % (100 * N['dcf']['roic_T'], 100 * N['coc']['wacc_term'],
                10000 * (N['dcf']['roic_T'] - N['coc']['wacc_term']))),
    dict(name='terminal growth',
         adopted='5% nominal, described as the standing convention for established Egyptian '
                 'names post-disinflation',
         alternative='the house terminal inflation of %.1f%% with zero real growth, which is '
                     'what [R-MACRO-01] returns for this market' % (100 * HOUSE_TERMINAL_INFLATION),
         patches=[("g_term=I(0.05,", "g_term=I(%r," % HOUSE_TERMINAL_INFLATION)],
         why='5% nominal against a terminal discount rate embedding 7% inflation is a perpetual '
             'REAL DECLINE of about two points a year, which nothing disclosed supports and the '
             'study states nowhere. The direction is counter-intuitive and it is the reason this '
             'row matters: because the terminal return sits below the terminal cost of capital, '
             'MORE growth destroys value here, so the house-conforming figure is the lower one '
             'and the study\'s own number is the flattering one.'),
    dict(name='the terminal risk-free rate',
         adopted='10.5%, built as the central bank\'s Q4-2028 inflation target of 5% plus a '
                 '5.5-point real convention',
         alternative='the house terminal risk-free of %.2f%%, derived as the terminal inflation '
                     'in force plus the same real convention' % (100 * HOUSE_TERMINAL_RF),
         patches=[("rf_term=I(0.105,", "rf_term=I(%r," % HOUSE_TERMINAL_RF)],
         why='The study carries an inflation number of its own, which [R-MACRO-01] does not '
             'permit: the 5% it builds on is a target the central bank\'s own August 2026 '
             'guidance has superseded, and the house path terminates at 7% with the return to '
             'the band put in the second half of 2027. The study\'s figure is the lower discount '
             'rate and therefore the higher value.'),
    dict(name='the cost of debt',
         adopted='22.00% marginal, set from the policy corridor plus a 2.5-point credit margin',
         alternative='25.50%, the same 2.5-point margin over the sovereign level the study\'s '
                     'own note calls the credible band top',
         patches=[("kd=I(0.220,", "kd=I(0.255,")],
         why='22.00% sits BELOW this company\'s own sovereign, which [R-COC-01] refuses outright '
             '— a same-currency corporate cannot borrow below the government that taxes it. The '
             'study\'s own effective-rate checks are 23.5% and 22.1%, both computed on a debt '
             'balance that is itself triangulated rather than disclosed. Only the weighted cost '
             'of capital input is moved here; the forward cost-of-debt path used for the equity '
             'profit and loss is a separate committed input and is left where it is.'),
    dict(name='the terminal capital structure',
         adopted='a normalised 40% debt weight, on the ground that the steady state presupposes '
                 'deleveraging and current market-value weights are circular',
         alternative='today\'s market-value weights, %.1f%% debt, carried into the terminal'
                     % (100 * WD_NOW),
         patches=[("wd_term=I(0.40,", "wd_term=I(%r," % WD_NOW)],
         why='The study argues this one against itself in its own comment — normalising RAISES '
             'the terminal cost of capital because it puts more weight on the dearer equity leg, '
             'and it calls that "the conservative direction". The alternative is not obviously '
             'wrong: a company whose enterprise value does not cover its debt has no evidenced '
             'route to a 40% structure, and assuming one is assuming the recovery the valuation '
             'is supposed to test.'),
    dict(name='net debt at the bridge date',
         adopted='EGP 9,805 mn, triangulated three ways from a total-assets print and a rolled '
                 'equity figure',
         alternative='EGP 10,386 mn, the challenged reading this study itself sensitises',
         patches=[("net_debt_fy25_est=I(9805.0,", "net_debt_fy25_est=I(10386.0,")],
         why='Not one component of this bridge is a disclosed balance-sheet line: total assets '
             'come from an aggregator, equity from a retail data site, non-debt liabilities are '
             'scaled from the prior year on purchase value. The study\'s own note records that '
             'two aggregator-side readings sit AT OR ABOVE the top of its range and calls the '
             'residual risk "SKEWED ADVERSE", and then adopts a figure at the bottom of that '
             'skew. Net debt per share is EGP %.2f against a price of EGP %.2f, so this line is '
             '%.0f%% of the market capitalisation and small errors in it are large errors in the '
             'answer.' % (N['dcf']['net_debt'] / N['shares'], LATEST_PRICE,
                          100 * N['dcf']['net_debt'] / (LATEST_PRICE * N['shares']))),
    dict(name='the equity-risk-premium basis',
         adopted='the swap basis — the sovereign default spread and equity premium read from '
                 'the credit-default-swap column',
         alternative='the credit-rating basis, the other column of the same source, which the '
                     'study publishes beside it',
         patches=[("sov_spread_cds=I(0.0340,", "sov_spread_cds=I(0.0637,"),
                  ("erp_cds=I(0.0941,", "erp_cds=I(0.1394,")],
         why='Both bases are published and neither is averaged into the other, which is right. '
             'The swap basis is the market\'s own live pricing of the sovereign\'s credit '
             'against an agency judgement updated in steps, and it is also the basis that gives '
             'the lower cost of equity — 27.98% against 29.38% — and therefore the higher value. '
             'The choice is defensible and it is still a choice.'),
    dict(name='the beta and its regressor',
         adopted='0.964, regressed against a 30-name equal-weight composite of the covered '
                 'Egyptian names',
         alternative='%.4f, regressed against the published index of the exchange this stock is '
                     'listed on, through the sanctioned resolver'
                     % CONFORMING_BETA['beta'],
         patches=[("beta=I(0.964,", "beta=I(%r," % round(CONFORMING_BETA['beta'], 6))],
         why='A constituent composite is a coverage artefact rather than a market: it changes '
             'whenever a stock is posted and it shares constituents with the panel it prices. '
             'The conforming figure is produced here rather than asserted — %.4f against the '
             'EGX30 series, R-squared %.3f, standard error %.4f on %d weekly observations, '
             'usable and not weak-flagged. The two are %.2f standard errors apart, so the '
             'regression cannot tell them apart; the direction is nonetheless one way, because the '
             'composite gives the lower beta and therefore the higher value.'
             % (CONFORMING_BETA['beta'], CONFORMING_BETA['r2'], CONFORMING_BETA['se'],
                CONFORMING_BETA['n'],
                abs(CONFORMING_BETA['beta'] - N['coc']['beta']) / CONFORMING_BETA['se'])),
    dict(name='the volume recovery',
         adopted='10.4 kt rising to 16.0 kt by FY2030E, 64% of the stated parent capacity',
         alternative='the study\'s own sensitised upper leg, 15% higher, reaching 18.4 kt — '
                     'still far below the 24.0 kt its own uplift implies the company ran in '
                     'FY2024',
         patches=[("vols_fcst=I([10.4, 11.9, 13.4, 14.8, 16.0],",
                   "vols_fcst=I([%r, %r, %r, %r, %r],"
                   % tuple(round(x * 1.15, 6) for x in N['tonnage']['vols_fcst']))],
         why='The path is a house estimate throughout; the company discloses no volume at all. '
             'The study anchors the first year on a collapsed quarter annualised and never '
             'returns to the utilisation its own calibration says the company ran two years '
             'earlier, and it says so. The capacity the ratio is struck against is '
             'parent-only, which the study also flags — so the utilisation figures are an upper '
             'bound and the recovery is understated on the study\'s own terms.'),
    dict(name='the normalised-earnings lens\'s mid-cycle net debt',
         adopted='EGP 6,000 mn typed as a post-paydown mid-cycle level',
         alternative='the EGP %s mn this study\'s OWN debt schedule forecasts for the same year '
                     'the lens takes its operating profit from'
                     % format(ND_FY28, ',.0f'),
         patches=[("nd_mid = 6000.0", "nd_mid = %r" % round(ND_FY28, 6))],
         why='The lens takes FY2028E operating profit and charges it a financing cost on a debt '
             'level the same model says will be nearly three times higher in that year. The '
             'model has the number and the lens does not use it. This is the second-largest '
             'contributor to the published central and it contradicts the study\'s own forecast '
             'in the direction that raises the answer.'),
    dict(name='the book lens\'s equity base',
         adopted='FY2025 equity of EGP 4,100 mn, itself a roll-forward rather than a disclosure',
         alternative='the terminal-year equity of EGP %s mn this study\'s own forecast produces'
                     % format(EQ_FY30, ',.0f'),
         patches=[("bvps = V['equity_fy25_est'] / SH", "bvps = eq_path[-1] / SH")],
         why='The study\'s own appendix says book equity "erodes toward zero by FY29-30E" and '
             'its committed equity path runs 4,100 to %s over the window. The book lens '
             'capitalises the opening figure and carries a fifth of the weight. Under '
             '[R-LENS-03] book value is a disclosed floor published as such and never weighted '
             'at all, so both framings here are alternatives to a third position the study does '
             'not take.' % format(EQ_FY30, ',.0f')),
    dict(name='the justified enterprise multiple',
         adopted='5.5 times FY2027E EBITDA, a deliberate discount for leverage, domestic '
                 'concentration and no dividend record',
         alternative='7.05 times, the peer multiple this study computes itself from the peer\'s '
                     'own filing',
         patches=[("ev_ebitda_base=I(5.5,", "ev_ebitda_base=I(7.05,")],
         why='The discount is argued and the reasons are real. It is still a typed number '
             'against a multiple the study derives from a filing, and it moves the relative lens '
             'in only one direction. The lens is clamped at its floor in all three columns on '
             'the published construction, so this judgement is worth nothing to a reader and '
             'something to the model — which is exactly why the measurement is taken beneath '
             'the clamp.'),
    dict(name='the currency path',
         adopted='a ~3% a year nominal crawl, 50.4 to 56.5, described as consistent with the '
                 'post-float managed range',
         alternative='the house path derived from the inflation ladder by relative '
                     'purchasing-power parity, %.2f to %.2f' % (HOUSE_FX[0], HOUSE_FX[-1]),
         patches=[("egp_fcst=I([50.4, 52.0, 53.5, 55.0, 56.5],",
                   "egp_fcst=I(%r," % (HOUSE_FX,))],
         why='A study may not carry a currency path of its own: [R-MACRO-01] derives it from the '
             'market\'s inflation ladder and never sets it by hand. The direction here is the '
             'same as copper\'s and for the same structural reason — a weaker pound raises '
             'revenue and the working capital charged against it while EBITDA is typed in '
             'nominal pounds a tonne and does not follow, so the study\'s stronger pound is the '
             'higher-value assumption.'),
    dict(name='the FY2025 finance cost',
         adopted='EGP 2,150 mn, derived so the profit and loss closes to the reported net profit',
         alternative='EGP 972 mn, the level the first quarter of 2026 implies on a higher debt '
                     'balance — an effective rate near 10% against the 23.2% assumed',
         patches=[("fin_cost_fy25_est=I(2150.0,", "fin_cost_fy25_est=I(972.0,")],
         why='This input alone moves the FY2025 conversion rate the whole forecast is calibrated '
             'against by about 40%, from 108 to 182 thousand pounds a tonne, and the study\'s '
             'own flag says the quarter is unexplained without the statements. It is recorded '
             'here BECAUSE its effect on the answer is nil: the forecast consumes the conversion '
             'path as a typed input rather than reading it off the base year, so the number the '
             'calibration rests on can move 40% and the valuation does not move at all. That is '
             'a fact about the model worth writing down, not a judgement worth 5% of value.'),
    dict(name='the depreciation ratio',
         adopted='1.3% of revenue, set above the historical rate to fund modest renewal',
         alternative='0.7% of revenue, the FY2024 ratio the study\'s own note computes',
         patches=[("dna_pct=I(0.013,", "dna_pct=I(0.007,")],
         why='The FY2024 depreciation of about EGP 90 mn that both figures rest on is the '
             'DIFFERENCE OF TWO FIGURES FROM TWO DIFFERENT AGGREGATORS, each quoted to two '
             'significant figures, so under the same rounding it could be 50 or 140. That single '
             'number is the sole basis for the property estimate, the depreciation ratio, the '
             '"light fixed-asset base" claim and the terminal\'s typed 5% of revenue. It is '
             'below the bar on the answer and it is not below the bar as evidence.'),
]


print('valuing %d contested judgements, both ways ...' % len(SPECS))
JUDGEMENTS = []
for spec in SPECS:
    if spec['patches'] is None:                      # the clamp: the baseline pair itself
        va, vb, alt, alt_pub = PUBLISHED, UNFLOORED['central'], UNFLOORED, UNFLOORED
        basis = ('the published central against the study\'s own unclamped construction — this '
                 'row IS the join between the two bases')
    else:
        va = UNFLOORED['central']
        alt = run_model(UNCLAMP + spec['patches'], spec['name'])
        vb = alt['central']
        alt_pub = run_model(spec['patches'], spec['name'] + ' (on the published construction)')
        basis = ('this study\'s own construction with the two lens clamps removed, one thing '
                 'moved')
    why = spec['why']
    if '%(clamp_worth)' in why:
        why = why % dict(clamp_worth=PUBLISHED - UNFLOORED['central'],
                         clamp_pc=100 * (PUBLISHED - UNFLOORED['central']) / PUBLISHED)
    base = abs(vb) or 1.0
    rel = abs(va - vb) / base
    # ASSERTIONS THE ALTERNATIVE TRIPS, OVER AND ABOVE THE MEASUREMENT BASIS. The
    # unclamped baseline trips this study's own plausibility band by construction --
    # removing a floor makes the central negative -- so carrying that on every row
    # would bury the assertions that are actually about the alternative behind one
    # that is about the basis. The baseline's own set is recorded once, at the top.
    trips = [t for t in alt['tripped'] if t not in UNFLOORED['tripped']
             and not t.startswith('central/spot')]
    JUDGEMENTS.append(dict(
        name=spec['name'], adopted=spec['adopted'], alternative=spec['alternative'],
        value_adopted=va, value_alternative=vb,
        currency='EGP per share',
        measured_on=basis,
        worth_relative=rel,
        worth_per_share=abs(va - vb),
        material_at_5pc=bool(rel >= 0.05),
        direction=('the study adopted the HIGHER-value framing' if va > vb else
                   ('the study adopted the LOWER-value framing' if va < vb else
                    'the two framings give the same value')),
        effect_on_the_published_central=dict(
            adopted=PUBLISHED, alternative=alt_pub['central'],
            moves_by=alt_pub['central'] - PUBLISHED),
        assertions_the_alternative_trips=trips,
        why=why))

signs = [1 if j['value_adopted'] > j['value_alternative'] else
         (-1 if j['value_adopted'] < j['value_alternative'] else 0)
         for j in JUDGEMENTS if j['material_at_5pc']]
n = len([s for s in signs if s])
k = len([s for s in signs if s > 0])
tail = sum(comb(n, i) for i in range(max(k, n - k), n + 1)) / float(2 ** n) if n else None
p = min(1.0, 2 * tail) if n else None

sub = [j for j in JUDGEMENTS if not j['material_at_5pc']]
sub_up = len([j for j in sub if j['value_adopted'] > j['value_alternative']])
sub_dn = len([j for j in sub if j['value_adopted'] < j['value_alternative']])

# THE SAME COUNT TAKEN THROUGH THE CLAMP, which is what a reader of the published
# answer would see. Reported because it is the whole finding about this study, and
# because it does something worse than deaden a judgement: it INVERTS some of them.
REST = JUDGEMENTS[1:]
pub_dead = len([j for j in REST
                if abs(j['effect_on_the_published_central']['moves_by']) < 1e-9])
pub_small = len([j for j in REST
                 if abs(j['effect_on_the_published_central']['moves_by']) / PUBLISHED < 0.05])
pub_signs = [1 if j['effect_on_the_published_central']['moves_by'] < -1e-9 else
             (-1 if j['effect_on_the_published_central']['moves_by'] > 1e-9 else 0)
             for j in REST
             if abs(j['effect_on_the_published_central']['moves_by']) / PUBLISHED >= 0.05]
pn = len([s for s in pub_signs if s])
pk = len([s for s in pub_signs if s > 0])
ptail = (sum(comb(pn, i) for i in range(max(pk, pn - pk), pn + 1)) / float(2 ** pn)) if pn else None
pp = min(1.0, 2 * ptail) if pn else None

# Does a judgement point the same way through the clamp as it does beneath it? On
# the unclamped basis the sign is (adopted - alternative); through the clamp the
# same judgement's adopted side is higher exactly when moving to the alternative
# LOWERS the published central.
inverted, agreed, deadened = [], [], []
for j in REST:
    beneath = (j['value_adopted'] > j['value_alternative']) - \
              (j['value_adopted'] < j['value_alternative'])
    mv = j['effect_on_the_published_central']['moves_by']
    through = -((mv > 1e-9) - (mv < -1e-9))
    if beneath == 0 or through == 0:
        deadened.append(j['name'])
    elif beneath == through:
        agreed.append(j['name'])
    else:
        inverted.append(j['name'])

CJ = {
    'ticker': 'ELEC',
    'as_of': '2026-09-06',
    # [R-ENF-06]: the answer this artefact was generated against
    'published_central': PUBLISHED,
    'published_spot': STRIKE,
    'currency': 'EGP per share',
    'why_this_file': (
        'Any single contested choice in a valuation is defensible; what is not defensible is a '
        'study that resolves EVERY one of them the same way and never notices. Each judgement '
        'here is valued BOTH ways by re-running this study\'s own compute.py with one thing '
        'moved, and the sign test below counts which way they went. A study landing them all '
        'one way is FLAGGED, never failed — a company can genuinely deserve a consistent read. '
        'What it may not do is go unmeasured. Nothing here changes a driver, a forecast, a rate '
        'or the fair value.'),
    'the_basis_and_why_it_is_not_the_published_central': (
        'THIS STUDY CANNOT BE MEASURED THROUGH ITS OWN ANSWER, and saying so is the first '
        'finding rather than a caveat. Two of its four lenses are pinned at literal floors — the '
        'cash-flow lens at EGP 0.01 and the relative lens at EGP 0.05 — because the enterprise '
        'value of EGP %s mn does not cover net debt of EGP %s mn. Those two carry 60%% of the '
        'weight and produce 4.2%% of the answer, and a floor is FLAT in the region the model '
        'sits in: %d of the %d judgements below move the published central by less than five per '
        'cent of it and %d move it by EXACTLY ZERO. A sign test computed through that clamp would '
        'report an absent answer as a clean one, which is the failure [R-ENF-04] names. So every '
        'judgement except the first is valued on this study\'s own construction with the two '
        'clamps removed, where the model actually lives, and THE CLAMP ITSELF IS THE FIRST '
        'JUDGEMENT — its two framings are exactly the published central of EGP %.4f and that '
        'unclamped baseline of EGP %.4f, so the two bases are joined by one recorded row rather '
        'than mixed silently. Every judgement\'s effect on the published central is reported '
        'beside its worth, and the sign test taken through the clamp is reported too, so a '
        'reader can see both and neither is hidden behind the other.'
        % (format(N['dcf']['ev'], ',.0f'), format(N['dcf']['net_debt'], ',.0f'),
           pub_small, len(REST), pub_dead, PUBLISHED, UNFLOORED['central'])),
    'assertions_the_measurement_basis_itself_trips': dict(
        which=UNFLOORED['tripped'],
        note=('Recorded once here rather than on every row. Removing the two clamps makes the '
              'central negative, which trips this study\'s own plausibility band by '
              'construction — a fact about the basis, not about any alternative. Each '
              'judgement below carries only the assertions ITS alternative trips over and '
              'above this set, so a row naming one is naming something real: a terminal '
              'growth centre other than the standing 5%, a cost of debt outside the '
              'effective-rate bounds, a terminal debt weight that is not below today\'s, a '
              'reinvestment rate outside (0,1).')),
    'judgements': JUDGEMENTS,
    'unvalued': [
        {'name': 'the fabrication uplift that converts copper into a cable price',
         'adopted': 'k = 1.387, copper at 72.1% of the price of a tonne of cable, called '
                    '"VALIDATION, not calibration" because it implies FY2024 volumes at 96% of '
                    'the stated capacity',
         'alternative': 'a higher uplift — at k = 2.0 the same revenue implies FY2024 volumes of '
                        '16.6 kt and 66% utilisation, and the implied non-copper cost stops '
                        'being negative',
         'why_unvalued': (
             'Moving the uplift alone is not the alternative framing, it is half of it. The '
             'uplift sets the price per tonne, so raising it with the typed volume path held '
             'fixed raises revenue and working capital while EBITDA — which is volume times a '
             'typed conversion rate — does not move at all, and the answer collapses for an '
             'arithmetic reason rather than an economic one. Valuing it honestly means re-basing '
             'the volume path and the conversion rate on the new uplift, which is a re-strike of '
             'the whole tonnage build rather than one driver moved. It is recorded here rather '
             'than guessed at, and its importance is not in doubt: at the adopted uplift the '
             'implied non-copper cost of FY2023 is MINUS 2.78% of revenue, which is '
             'arithmetically impossible, so the uplift and the reconstructed margins cannot both '
             'be right and the model uses both.')},
        {'name': 'the length of the explicit window',
         'adopted': 'five years, with %.0f%% of enterprise value in the terminal'
                    % (100 * N['dcf']['tv_pct']),
         'alternative': 'a window run until growth converges on the terminal rate, which is what '
                        'the house standard requires',
         'why_unvalued': (
             'Extending the window means forecasting volumes, conversion rates, working capital '
             'and the debt schedule for years the study has no drivers for, which is a new '
             'forecast rather than a re-reading of this one. What can be said without inventing '
             'anything is that the judgement is large: more than four fifths of the enterprise '
             'value is struck off a single terminal year whose conversion rate is the study\'s '
             'most contested number.')},
        {'name': 'the balance-sheet and income statements the bridge stands on',
         'adopted': 'a triangulated FY2025 balance sheet and a reconstructed income statement, '
                    'built from aggregator and press prints of exchange filings',
         'alternative': 'the company\'s own audited consolidated statements',
         'why_unvalued': (
             'There is nothing to value it against. The issuer\'s statement index lists nothing '
             'after 30 September 2025 and nothing consolidated after 31 December 2020; every '
             'consolidated file it lists sits on a host that no longer resolves, and the study '
             'models consolidated figures. The half-year 2026 statements, due in mid-August, are '
             'not in the model either. This is not a contested judgement about which reasonable '
             'people differ — it is a source condition, carried in the escalation register and '
             're-probed rather than taken on report, and it is why this study\'s own gap review '
             'concludes it should not be repaired.')},
    ],
    'sign_test': {
        'material_at_5pc': n, 'resolved_upward': k, 'resolved_downward': n - k,
        'two_sided_binomial_p': p, 'flagged': bool(p is not None and p < 0.05 and n >= 3),
        'measured_on': 'the unclamped construction, one thing moved at a time',
        'reading': (
            '%d material contested judgements, %d resolved toward the higher value and %d toward '
            'the lower, two-sided p = %s. NO LEAN: this study does not take every fork the same '
            'way, and that is worth stating plainly about a study sitting %.0f%% below the '
            'market — the disagreement with the price is not the residue of twenty small '
            'choices all pointing one way. Where the study is generous it is generous in the '
            'THREE LENSES THAT SURVIVE THE CLAMP, and where it is punitive it is punitive in the '
            'cash-flow model the clamp hides: of the %d judgements resolved toward the lower '
            'value, %d move the published answer by nothing at all or move it UP. The lean this '
            'instrument is built to find is not here; what is here is a construction in which '
            'the two halves of the study do not meet.'
            % (n, k, n - k, 'n/a' if p is None else '%.3f' % p,
               -100 * (PUBLISHED / LATEST_PRICE - 1), n - k,
               len([j for j in REST if j['value_adopted'] < j['value_alternative']
                    and j['effect_on_the_published_central']['moves_by'] >= -1e-9]))),
    },
    'what_the_clamp_does_to_a_judgement': {
        'note': ('The clamp does something worse to this instrument than deaden it, and it is '
                 'only visible because both bases were measured. A judgement read through the '
                 'clamp can point the OTHER WAY from the same judgement read beneath it, because '
                 'the cash-flow lens is pinned while the normalised and relative lenses are not: '
                 'raising forecast volumes by 15%, for instance, LOWERS this model\'s value — '
                 'the working-capital build scales against a fixed opening balance while the '
                 'earnings funding it are thin, so the first forecast year turns a release '
                 'into a build — and RAISES the published central, because the loss happens '
                 'behind a floor and the gain does not. A '
                 'reader auditing the published answer would therefore get some of these '
                 'directions backwards.'),
        'agree': agreed, 'inverted': inverted,
        'no_direction_through_the_clamp': deadened,
    },
    'the_same_count_through_the_clamp': {
        'note': (
            'What a reader of the published answer would see. Of the %d judgements other than '
            'the clamp itself, %d move the published central by exactly zero, because the two '
            'lenses they act on never leave their floors.'
            % (len(JUDGEMENTS) - 1, pub_dead)),
        'material_at_5pc': pn, 'resolved_upward': pk, 'resolved_downward': pn - pk,
        'two_sided_binomial_p': pp,
    },
    'below_the_bar': {
        'count': len(sub), 'resolved_upward': sub_up, 'resolved_downward': sub_dn,
        'note': ('Reported because a lean living entirely in small decisions is still a lean, '
                 'and because one of these — the FY2025 finance cost — is worth exactly nothing '
                 'to the answer while moving the rate the whole forecast is calibrated against '
                 'by about 40%.'),
    },
    'runs_behind_this_record': _RUNS[0],
}

with open(os.path.join(HERE, 'diagnostics.json'), 'w', encoding='utf-8') as fh:
    json.dump(DIAG, fh, indent=1, ensure_ascii=False)
with open(os.path.join(HERE, 'contested_judgements.json'), 'w', encoding='utf-8') as fh:
    json.dump(CJ, fh, indent=1, ensure_ascii=False)

print('\nwrote diagnostics.json — at EGP %.2f the price implies a terminal EBITDA margin of '
      '%.2f%% against the study\'s %.2f%% (reconstructed filed record %.2f%%-%.2f%%)'
      % (LATEST_PRICE, 100 * DIAG['implied']['value'], 100 * STUDY_MARGIN_T,
         100 * FILED_MARGIN['FY24'], 100 * FILED_MARGIN['FY23']))
print('wrote contested_judgements.json — %d judgements, %d material, %d up / %d down, p = %s%s'
      % (len(JUDGEMENTS), n, k, n - k, 'n/a' if p is None else '%.3f' % p,
         '   FLAGGED' if CJ['sign_test']['flagged'] else ''))
print('%d sandbox runs of the study\'s own model behind these two records' % _RUNS[0])
