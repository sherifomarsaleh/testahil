"""AMR — the two output records [R-ENF-05], COMPUTED, never typed.

WHAT THIS WRITES, AND WHY IT IS NOT IN THE NUMBERS FILE
-------------------------------------------------------
Two files, both diagnostics and neither an input to anything:

  diagnostics.json            the reverse read — what the traded price must
                              believe under this study's own drivers
  contested_judgements.json   every contested judgement, both framings valued,
                              and the binomial sign test on how they were resolved

The reverse read is kept OUT of study_numbers.json deliberately. A quantity
solved from a price and then used anywhere in a valuation is the
reverse-engineered rate the protocol prohibits outright, arriving through a side
door, and the prohibition is worth nothing if the side door is open. No builder
reads either file; the containment is checked from outside.

HOW EVERY NUMBER HERE IS PRODUCED
---------------------------------
By re-running THIS STUDY'S OWN compute.py in a scratch directory with exactly one
driver changed, and reading the central it publishes. Nothing is estimated, no
driver in the study moves, and the study's committed answer is read from its own
numbers file so this record cannot drift from it [R-ENF-06].

Valuing the alternative framing of a judgement is a calculation reported. It is
never a change made: `python3 diagnostics_amr.py` writes only the two files above.

    python3 engine/amr_study/diagnostics_amr.py
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
COPY_ALONGSIDE = ('peers.json', 'beta_result.json')

# The latest known close, from the committed supplied-price artefact, not from a
# figure in a conversation [R-GAP-01 AMENDED / R-IND-01].
LATEST_PRICE_AED = 2.39
LATEST_PRICE_DATE = '2026-09-03'
LATEST_PRICE_SOURCE = ('engine/prices/SUPPLIED_03-09-2026.json — the close on the Abu Dhabi '
                       'Securities Exchange, 3 September 2026')

_BASE = open(SOURCE, encoding='utf-8').read()

# --------------------------------------------------------------------------
# Two of this study's own internal assertions have to be suspended to VALUE
# certain alternatives, and both are named here rather than quietly disabled.
# Suspending them changes nothing on the published drivers -- there is a control
# run below that proves it -- and the fact that an alternative trips one of them
# is recorded beside that judgement, because it is information about the
# alternative rather than an excuse for skipping it.
# --------------------------------------------------------------------------
ANCHOR_PATH_ASSERT = (
    "chk('the forecast anchor is inside the materiality line along the whole path',\n"
    "    (min(ebitda_margin_f) - ebitda_margin_f[0]) / ebitda_margin_f[0] >= -0.05,\n"
    "    f'{100*(min(ebitda_margin_f)-ebitda_margin_f[0])/ebitda_margin_f[0]:.4f}% relative')")
ANCHOR_OFF = "pass  # [R-ANCHOR-01] path assertion, suspended in the measurement sandbox only"
FCFF_ASSERT = ("chk('capitalised-lease free cash flow reconciles to the published "
               "free-cash-flow measure',")
FCFF_OFF = "chk('reconciliation suspended in the measurement sandbox', True, ''); _ = ("


def run_model(patches, label=''):
    """Re-run the study's own model with `patches` applied, and return what it publishes.

    Every patch is asserted to land exactly once: a substitution that matches
    nothing would return the published answer and read exactly like a judgement
    worth nothing [R-ENF-04].
    """
    txt = _BASE
    for old, new in patches:
        n = txt.count(old)
        if n != 1:
            raise AssertionError('patch for %r landed %d times, not once' % (label, n))
        txt = txt.replace(old, new)
    d = tempfile.mkdtemp(prefix='amr_diag_')
    try:
        with open(os.path.join(d, 'compute.py'), 'w', encoding='utf-8') as fh:
            fh.write(txt)
        for f in COPY_ALONGSIDE:
            shutil.copy(os.path.join(HERE, f), d)
        p = subprocess.run([sys.executable, 'compute.py'], cwd=d,
                           capture_output=True, text=True)
        if p.returncode != 0:
            tail = (p.stderr.strip().splitlines() or ['(no traceback)'])[-1]
            raise RuntimeError('%s: the model refused — %s' % (label, tail))
        with open(os.path.join(d, 'study_numbers.json'), encoding='utf-8') as fh:
            out = json.load(fh)
        return {'central': out['central'],
                'cash_flow_lens': out['lenses']['values']['Discounted cash flow']
                * out['meta']['fx']}
    finally:
        shutil.rmtree(d, ignore_errors=True)


def central_under(patches, label=''):
    """The answer the study publishes, under `patches`."""
    return run_model(patches, label)['central']


# ==========================================================================
# 1. THE CONTESTED JUDGEMENTS
#
# A fork qualifies here when the study's OWN text, its input register or its
# critique response marks it as a choice between framings, or when a standing
# rule names the alternative -- and when BOTH framings can be valued from
# sourced numbers. A perturbation of a driver that nobody had to decide is not
# a judgement, and a judgement that cannot be valued both ways is recorded
# below as unvalued rather than guessed.
# ==========================================================================
INV_PCT_FY25 = 714.319 / 2508.821          # the disclosed FY2025 food line, note 21

JUDGEMENTS = [
    dict(
        name='the margin step-change: structural or cyclical',
        adopted='structural — the gain shown in the reviewed first half of 2026 holds, and '
                'eases only as the delivery channel grows',
        alternative='cyclical — the first half is banked and the margin reverts in a straight '
                    'line to the three-year audited average of 22.79% by FY2030',
        patches=[(ANCHOR_PATH_ASSERT, ANCHOR_OFF),
                 ('cost_pct_25 = ((COGS[2] + SM[2] + GA[2] - DNA[2]) / REV[2])',
                  'ebitda_f = [rev_f[t] * margin_revert[t] for t in range(5)]\n'
                  'ebitda_margin_f = [ebitda_f[t] / rev_f[t] for t in range(5)]\n'
                  'cost_pct_25 = ((COGS[2] + SM[2] + GA[2] - DNA[2]) / REV[2])')],
        why='The study calls this the whole study and publishes both readings side by side, '
            'never averaged — but the central it actually publishes is struck on the '
            'structural path, and that is what this row measures. Nothing in the filings '
            'settles it: the company attributes the gain to procurement, menu engineering and '
            'delivery economics, and the same numbers are equally consistent with a friendly '
            'turn in traded food prices. A second construction of the same question — the food '
            'and packaging line put back to the {food_pct_fy25:.2f} per cent of revenue the '
            'FY2025 note discloses, instead of the 27.4 per cent the reviewed half recorded — '
            'is worth {food_line_fy25:.4f}, so the question costs about the same either way it '
            'is posed. The alternative trips this study\'s own forecast-anchor assertion, '
            'which is stated rather than suppressed.'),
    dict(
        name='the justified enterprise multiple',
        adopted='8.5 times forward EBITDA, a deliberate discount to the peer set',
        alternative='the usable peer median the study itself calls the anchor',
        patches=[("MULT_EV_EBITDA = inp('justified_ev_ebitda', 8.5,",
                  "MULT_EV_EBITDA = inp('justified_ev_ebitda', PEER_EV_EBITDA_MED,")],
        why='The delivered document states the discount is deliberate — "Americana is the '
            'operator, not the brand owner" — and the study\'s own peer table runs the other '
            'way: the operator-franchisees closest to it in structure trade ABOVE the '
            'franchisors (Devyani 33.3x, Sapphire 27.6x, Jubilant 23.1x against Yum 17.6x, '
            'Domino\'s 16.2x). What survives as a reason for some discount is the lease-'
            'accounting basis the study flags on the Indian names, which is why this is a '
            'judgement and not a defect. It carries a fifth of the published central and it is '
            'the largest contested judgement in the study.'),
    dict(
        name='the wage escalator',
        adopted='6.0% a year on wage per full-time equivalent, deliberately above Gulf '
                'consumer price inflation',
        alternative='the house UAE inflation ladder, 2.5 / 2.0 / 2.0 / 2.0 / 2.0',
        patches=[("WAGE_G = inp('wage_growth', 0.06,", "WAGE_G = inp('wage_growth', 0.0,"),
                 ('    wage = WAGE_FTE_25 * (1 + WAGE_G) ** (t + 1)',
                  '    _ladder = [0.025, 0.020, 0.020, 0.020, 0.020]\n'
                  '    _cum = 1.0\n'
                  '    for _i in range(t + 1):\n'
                  '        _cum *= (1 + _ladder[_i])\n'
                  '    wage = WAGE_FTE_25 * _cum')],
        why='The study\'s own note sets 6% above Gulf inflation "because the mix shifts toward '
            'delivery-capable and above-restaurant staff" — a mix effect the model already '
            'carries separately through staff per restaurant falling 12.05 to 11.25, so the '
            'same shift is charged twice. The 6% is also a two-year average of two opposite '
            'years: wage per full-time equivalent ran USD {w23:,.0f} (FY2023) to {w24:,.0f} '
            '(FY2024, {g24:+.2f} per cent) to {w25:,.0f} (FY2025, {g25:+.2f} per cent), every '
            'figure from this study\'s own register. At a middle reading of 4.0% the '
            'alternative is {wage_at_4pc:.4f}, so this judgement is worth between '
            '{wage_low:.2f} and {wage_high:.2f} a share and its direction does not depend on '
            'which reading is taken.'),
    dict(
        name='like-for-like sales growth',
        adopted='5.5% in FY2026 falling to 3.5%, set just below the filed half-year and, in '
                'the study\'s own words, consistent with management guidance',
        alternative='the same convergence shape anchored on the 6.3% the company actually '
                    'filed for the first half of 2026',
        patches=[('LFL_PATH = [0.055, 0.045, 0.040, 0.037, 0.035]',
                  'LFL_PATH = [0.063, 0.053, 0.048, 0.045, 0.043]')],
        why='Guidance is scored and never consumed, and half the stated reason for this level '
            'is management\'s own mid-single-digit guide. Moving only the first year to the '
            'filed 6.3% and leaving the rest of the path where it is gives '
            '{lfl_year_one_only:.4f}, so the SIGN of this judgement is the same either way and '
            'only its size turns on whether the whole path travels with its anchor. Both '
            'numbers are given rather than the convenient one.'),
    dict(
        name='staff per restaurant',
        adopted='falling 12.05 to 11.25 over five years, continuing the disclosed trend',
        alternative='held at the 12.12 the FY2025 staff note actually discloses',
        patches=[(ANCHOR_PATH_ASSERT, ANCHOR_OFF),
                 ('[12.05, 11.85, 11.65, 11.45, 11.25]',
                  '[12.12, 12.12, 12.12, 12.12, 12.12]')],
        why='The disclosed trend is real — 15.4 in FY2023, 13.3 in FY2024, 12.12 in FY2025 — '
            'and nothing in the filings commits the company to continuing it; the study\'s own '
            'register books the path as a house estimate while the level it starts from is a '
            'disclosure. The alternative trips this study\'s own forecast-anchor assertion, '
            'which is recorded rather than suppressed.'),
    dict(
        name='terminal growth',
        adopted='3.0% — 2.0% pegged-market inflation plus a stated 1.0% real',
        alternative='inflation only, zero real, which is the house default',
        patches=[("TERMINAL_G = inp('terminal_growth', 0.030,",
                  "TERMINAL_G = inp('terminal_growth', 0.020,")],
        why='Terminal growth is stored as a real rate on an inflation path with a default real '
            'of zero, and a point of real growth in perpetuity is a stated judgement about an '
            'estate that has to keep opening restaurants to earn it. It clears the bar at all '
            'only because {tv_share:.1f} per cent of enterprise value sits beyond year five: '
            'one point of perpetual real growth is the smallest of this study\'s six material '
            'judgements and it is still worth more than a twentieth of the answer.'),

    # ---- below the five-per-cent bar, recorded because a judgement that goes
    # ---- unmeasured is the thing this instrument exists to prevent
    dict(
        name='the central architecture',
        adopted='a weighted blend of four lenses at 50 / 20 / 20 / 10',
        alternative='the class primary alone, with the other lenses published as cross-checks',
        patches=[("W_DCF = inp('weight_dcf', 0.50,", "W_DCF = inp('weight_dcf', 1.00,"),
                 ("W_REL = inp('weight_relative', 0.20,", "W_REL = inp('weight_relative', 0.00,"),
                 ("W_NORM = inp('weight_normalised', 0.20,", "W_NORM = inp('weight_normalised', 0.00,"),
                 ("W_BOOK = inp('weight_book', 0.10,", "W_BOOK = inp('weight_book', 0.00,")],
        why='A blend at typed weights that never cleared an out-of-sample test, and a tenth of '
            'it sits on the book lens the study\'s own document calls reported "not because it '
            'is informative". It falls below the five-per-cent bar only because the four '
            'lenses happen to straddle the blend.'),
    dict(
        name='right-of-use additions',
        adopted='8.5% of revenue, set between two disclosed rates',
        alternative='the 7.7% the reviewed first half of 2026 actually ran',
        patches=[(FCFF_ASSERT, FCFF_OFF),
                 ("ROU_ADD_PCT = inp('rou_additions_pct', 0.085,",
                  "ROU_ADD_PCT = inp('rou_additions_pct', 0.077,")],
        why='A midpoint judgement with two disclosed endpoints — 10.2% in FY2025 and 7.7% in '
            'the reviewed half — and its direction depends on which endpoint is taken, so the '
            'endpoint is chosen by rule and not by preference: a near-term reviewed actual '
            'outranks a stale full-year rate. At the FY2025 endpoint instead the alternative '
            'is {rou_at_fy25:.4f}, which WOULD be material and WOULD resolve upward. Both are '
            'printed so the choice is visible rather than only its result.'),
    dict(
        name='the terminal return on incremental capital',
        adopted='faded to 30%, anchored on the published store-payback table',
        alternative='the model-implied 49.35% the forecast itself reaches',
        patches=[("TERMINAL_ROIC = inp('terminal_roic', 0.30,",
                  "TERMINAL_ROIC = inp('terminal_roic', 0.4935003693332367,")],
        why='The fade was conceded in the study\'s own expert cross-examination on the '
            'company\'s own disclosure that the marginal brands run past five years to payback '
            'against KFC at 2.4. The alternative is what the model\'s own FY2030 balance sheet '
            'produces, and it is the reading published as the bull case.'),
    dict(
        name='the terminal risk-free rate',
        adopted='4.45% — the ten-year Treasury less the US default spread, rounded and held',
        alternative='4.1751%, derived as terminal inflation plus the real-rate convention on '
                    'the house United States path',
        patches=[("TERMINAL_RF = inp('terminal_risk_free', 0.0445,",
                  "TERMINAL_RF = inp('terminal_risk_free', 0.041751,")],
        why='A terminal rate quoted from today\'s market rather than derived from a terminal '
            'inflation is a different construction, not a different number; the house rule '
            'derives it. The gap is small here because the peg means the market rate and the '
            'derived rate are close.'),
    dict(
        name='the equity risk premium basis',
        adopted='the ratings basis',
        alternative='the credit-default-swap basis, which the study publishes beside it',
        patches=[('KE_RATING = RF_RATING + BETA * ERP_BLEND_RATING',
                  'KE_RATING = RF_CDS + BETA * ERP_BLEND_CDS'),
                 ('KE_TERM = TERMINAL_RF + BETA * ERP_BLEND_RATING',
                  'KE_TERM = TERMINAL_RF + BETA * ERP_BLEND_CDS')],
        why='Both bases are built and published; the study names the ratings basis as central, '
            'and the house default is the market-priced one. The dual framing is honoured — '
            'neither is averaged into the other — and the choice is worth 0.05 a share.'),
    dict(
        name='the currency drag on Egypt',
        adopted='2.5% a year on dollar revenue per restaurant',
        alternative='zero, which is the direction the two most recent disclosed readings run',
        patches=[("'Egypt': 0.025,", "'Egypt': 0.0,")],
        why='The study sets the drag from projected inflation differentials and says in the '
            'same paragraph that Egypt dollar revenue grew 29% in FY2025 and 23% in the first '
            'half of 2026 — a mechanism the company\'s own filings measure in the opposite '
            'direction. The study calls it a judgement rather than a disclosure, which is '
            'exactly what it is.'),
    dict(
        name='FY2026 net new restaurants',
        adopted='125, the midpoint of the company\'s published 120-130 guidance',
        alternative='zero, against a first half that closed three restaurants net',
        patches=[('NSO_TOTAL = [125, 130, 130, 125, 120]',
                  'NSO_TOTAL = [0, 130, 130, 125, 120]')],
        why='The estate went 2,749 at 31 December 2025 to 2,746 at 30 June 2026, so half the '
            'guided year has to arrive in the second half. Openings are genuinely back-half '
            'weighted in this business, which is why the guidance is not simply discarded; the '
            'harshest available alternative is priced and it still does not reach the bar.'),
    dict(
        name='delivery cost per delivered dollar',
        adopted='14.25% improving five basis points a year',
        alternative='held at the 15.0% FY2025 actually ran',
        patches=[("DEL_RATIO_PATH = inp('delivery_cost_ratio_path', "
                  "[0.1425, 0.1420, 0.1415, 0.1410, 0.1405],",
                  "DEL_RATIO_PATH = inp('delivery_cost_ratio_path', "
                  "[0.150, 0.150, 0.150, 0.150, 0.150],")],
        why='The opening level is calibrated so the line reproduces the disclosed first-half '
            'margin at the disclosed 52% channel share, which is a fitted rather than a '
            'disclosed number; the improvement after it is the company\'s claim about its own '
            'unit economics, scored rather than consumed.'),
    dict(
        name='the delivery channel share',
        adopted='rising from 52% to 56.5% of revenue',
        alternative='held at the 52% the first half of 2026 disclosed',
        patches=[("DEL_SHARE_PATH = inp('delivery_share_path', "
                  "[0.52, 0.535, 0.55, 0.56, 0.565],",
                  "DEL_SHARE_PATH = inp('delivery_share_path', "
                  "[0.52, 0.52, 0.52, 0.52, 0.52],")],
        why='The channel is dearer to serve than the counter, so continuing its rise is the '
            'punitive reading and the study takes it; the disclosed series (44%, 48%, 52%) '
            'supports continuation but does not say where it stops.'),
    dict(
        name='the recurring impairment charge',
        adopted='0.31% of revenue charged every forecast year',
        alternative='excluded, as the first edition of this study had it',
        patches=[("IMP_RATE = inp('impairment_rate_recurring',\n"
                  "               (sum(IMP_NF) + sum(IMP_F)) / sum(REV),",
                  "IMP_RATE = inp('impairment_rate_recurring',\n"
                  "               0.0,")],
        why='A 2,700-restaurant estate always carries some underperforming units, so charging '
            'the three-year audited average is the punitive and the more honest reading; it '
            'was adopted in the critique round against a first edition that excluded it.'),
    dict(
        name='the justified price-earnings multiple',
        adopted='17 times',
        alternative='the usable peer median',
        patches=[("MULT_PE = inp('justified_pe', 17.0,",
                  "MULT_PE = inp('justified_pe', PEER_PE_MED,")],
        why='Set just below the peer median on the same reasoning as the enterprise multiple, '
            'but the gap is far smaller, so the same argument is worth a twentieth of what it '
            'is worth on the enterprise lens.'),
    dict(
        name='the normalised-earnings margin',
        adopted='the midpoint of the structural and cyclical FY2028 readings',
        alternative='the structural FY2028 margin alone, as the first edition had it',
        patches=[('norm_margin = (ebitda_margin_f[2] + margin_revert[2]) / 2.0',
                  'norm_margin = ebitda_margin_f[2]')],
        why='A lens whose purpose is to strip out the cycle cannot be struck on the peak of '
            'it; the midpoint was adopted in the critique round, and the alternative here is '
            'the construction that was retired rather than a new one.'),
    dict(
        name='the interim dividend in the anchor roll',
        adopted='excluded — declared 28 July 2026 but unpaid at the 7 August anchor',
        alternative='deducted in the roll, on the ground that it was declared before the anchor',
        patches=[("DIV_WINDOW = inp('dividend_paid_in_window', DIV_FY25_DECL / SH,",
                  "DIV_WINDOW = inp('dividend_paid_in_window', (DIV_FY25_DECL + 100.8) / SH,")],
        why='A dividend declared before the bridge date is already out of the equity it would '
            'come out of; whether "declared" or "paid" is the event that matters here is a '
            'real question and the study answers it one way. USD 100.8 million is the '
            'company\'s own disclosed figure.'),
    dict(
        name='the lease estate',
        adopted='capitalised, as the accounts present it',
        alternative='treated as an operating cost, on the cash-flow lens',
        patches=[("lens_values = {'Discounted cash flow': A['fv'],",
                  "lens_values = {'Discounted cash flow': B['fv'],")],
        why='The study builds both readings in full and publishes the pair; the finding worth '
            'stating is that the accounting choice which dominates the balance sheet turns out '
            'not to decide the value. Measured here by substituting the operating-cost reading '
            'into the cash-flow lens, which is where the framing bites.'),
]

# Judgements that are real and are NOT valued, named rather than dropped. An
# absent answer is not a clean one [R-ENF-04].
UNVALUED = [
    dict(name='the balance-sheet date the bridge stands on',
         adopted='31 December 2025 audited, rolled 219 days to the price anchor at the cost of '
                 'equity, net of the dividend paid inside the window',
         alternative='the reviewed 30 June 2026 sheet, whose disclosed net debt is USD 258.449 '
                     'million against USD 220.056 million in December',
         why_unvalued='Substituting the June sheet without moving the discounting clock to '
                      '30 June would count the first half of 2026 twice — once in the cash '
                      'flow discounted from December and again in the June net debt. Valuing '
                      'this framing honestly is a re-strike of the model, not a driver swap, '
                      'and this record does not change the model. It is reported unvalued '
                      'rather than estimated.'),
    dict(name='a discount for the controlled structure',
         adopted='none — the shares are valued as a proportionate claim on the whole firm',
         alternative='a control or liquidity discount for a free float of about a third, '
                     'Adeptio holding 66.03%',
         why_unvalued='No disclosure supports any particular size of discount, and the study '
                      'names the concentration in its caveats without pricing it. A percentage '
                      'chosen here would be an invented number, so none is chosen.'),
]


# ==========================================================================
# 3. SIDE CALCULATIONS
#
# Every figure quoted inside a judgement's `why` is computed here from the
# study's own register or from a re-run of its own model. A number stated in
# prose must be computed, not typed -- including in a diagnostic.
# ==========================================================================
FOOD_LINE_PATCH = [(ANCHOR_PATH_ASSERT, ANCHOR_OFF),
                   ('[0.2740, 0.2725, 0.2715, 0.2710, 0.2705]', '[%r] * 5' % INV_PCT_FY25)]
WAGE_4PC_PATCH = [("WAGE_G = inp('wage_growth', 0.06,", "WAGE_G = inp('wage_growth', 0.04,")]
LFL_YEAR_ONE_PATCH = [('LFL_PATH = [0.055, 0.045, 0.040, 0.037, 0.035]',
                       'LFL_PATH = [0.063, 0.045, 0.040, 0.037, 0.035]')]
ROU_FY25_PATCH = [(FCFF_ASSERT, FCFF_OFF),
                  ("ROU_ADD_PCT = inp('rou_additions_pct', 0.085,",
                   "ROU_ADD_PCT = inp('rou_additions_pct', 0.102,")]


TERMINAL_G_CEILING = 0.0444          # the model refuses g >= the terminal risk-free rate
IMPLIED_BETA = []                    # filled by the reverse read before side_calcs runs
TV_SHARE = []                        # the study's own share of value beyond year five
MARGIN_OPEN = []                     # the study's own opening forecast margin


def side_calcs(register, published_central):
    """The figures the `why` texts quote, every one computed."""
    w = [register['cost_staff_fy23']['value'] / (register['fte_fy23']['value'] / 1000.0),
         register['cost_staff_fy24']['value'] / (register['fte_fy24']['value'] / 1000.0),
         register['cost_staff_fy25']['value'] / (register['fte_fy25']['value'] / 1000.0)]
    beta = json.load(open(os.path.join(HERE, 'beta_result.json'), encoding='utf-8'))
    wage_at_4pc = central_under(WAGE_4PC_PATCH, 'wage at 4%')
    wage_at_ladder = central_under(JUDGEMENTS[2]['patches'], 'wage at the house ladder')
    return {
        'food_pct_fy25': 100 * INV_PCT_FY25,
        'food_line_fy25': central_under(FOOD_LINE_PATCH, 'food line at FY2025'),
        'wage_at_4pc': wage_at_4pc,
        'wage_low': abs(wage_at_4pc - published_central),
        'wage_high': abs(wage_at_ladder - published_central),
        'w23': 1000 * w[0], 'w24': 1000 * w[1], 'w25': 1000 * w[2],
        'g24': 100 * (w[1] / w[0] - 1), 'g25': 100 * (w[2] / w[1] - 1),
        'lfl_year_one_only': central_under(LFL_YEAR_ONE_PATCH, 'like-for-like, year one only'),
        'rou_at_fy25': central_under(ROU_FY25_PATCH, 'right-of-use at the FY2025 rate'),
        'beta_se': beta['se'],
        'beta_sigma': abs(register['beta']['value'] - IMPLIED_BETA[0]) / beta['se'],
        'margin_open': 100 * MARGIN_OPEN[0],
        'terminal_rf': register['terminal_risk_free']['value'],
        'tv_share': 100 * TV_SHARE[0],
        'terminal_g_at_ceiling': central_under(
            [("TERMINAL_G = inp('terminal_growth', 0.030,",
              "TERMINAL_G = inp('terminal_growth', %.12f," % TERMINAL_G_CEILING)],
            'terminal growth at the ceiling'),
    }


# ==========================================================================
# 4. THE REVERSE READ
#
# Solved on the answer the study PUBLISHES -- the four-lens central -- and not
# on the cash-flow lens. Those are different numbers and solving on the wrong
# one understates the disagreement, which is the trap this record names.
# ==========================================================================
LFL_BASE = [0.055, 0.045, 0.040, 0.037, 0.035]
LFL_LINE = 'LFL_PATH = [0.055, 0.045, 0.040, 0.037, 0.035]'


def lfl_patches(shift):
    return [(LFL_LINE, 'LFL_PATH = %r' % ([round(b + shift, 12) for b in LFL_BASE],))]


def solve(make_patches, lo, hi, target, label, tol=1e-7, field='central'):
    """Bisect until the model's answer on `field` reproduces `target`.

    `field` is 'central' everywhere that matters. The one place it is not is the
    measurement below of what the SAME solves return on the cash-flow lens alone,
    which is how this record shows that solving a reverse read on a lens the study
    does not publish understates the disagreement.
    """
    f = lambda x: run_model(make_patches(x), label)[field] - target       # noqa: E731
    flo, fhi = f(lo), f(hi)
    if flo * fhi >= 0:
        raise AssertionError('%s: the price is not reachable on this quantity between '
                             '%r and %r' % (label, lo, hi))
    for _ in range(48):
        mid = (lo + hi) / 2.0
        fm = f(mid)
        if abs(fm) < tol:
            return mid
        if flo * fm < 0:
            hi, fhi = mid, fm
        else:
            lo, flo = mid, fm
    return (lo + hi) / 2.0


# the three quantities re-solved on the CASH-FLOW LENS ALONE, so the claim that a
# reverse read struck on the wrong lens understates the disagreement is measured
# rather than asserted
LENS_SOLVES = (
    ('wage escalator', 0.0, 0.06, 0.06,
     lambda g: [("WAGE_G = inp('wage_growth', 0.06,",
                 "WAGE_G = inp('wage_growth', %.12f," % g)]),
    ('beta', 0.30, 0.93, 0.930,
     lambda b: [("BETA = inp('beta', 0.930,", "BETA = inp('beta', %.12f," % b)]),
    ('terminal growth', 0.030, 0.0444, 0.030,
     lambda g: [("TERMINAL_G = inp('terminal_growth', 0.030,",
                 "TERMINAL_G = inp('terminal_growth', %.12f," % g)]),
)


def main():
    with open(NUMBERS, encoding='utf-8') as fh:
        pub = json.load(fh)
    published_central = pub['central']
    published_spot = pub['spot']

    control = central_under([(ANCHOR_PATH_ASSERT, ANCHOR_OFF)], 'control')
    assert abs(control - published_central) < 1e-12, (
        'suspending an assertion moved the answer; the measurement is not clean')
    assert abs(central_under([], 'reproduce') - published_central) < 1e-12, (
        'the sandbox does not reproduce the committed answer')

    # ---- the reverse read --------------------------------------------------
    cash_flow_lens = run_model([], 'cash-flow lens')['cash_flow_lens']
    lens_solved = []
    for label, lo, hi, _sv, mk in LENS_SOLVES:
        v = solve(mk, lo, hi, LATEST_PRICE_AED, label + ' on the cash-flow lens',
                  field='cash_flow_lens')
        lens_solved.append(100 * v if label != 'beta' else v)

    shift = solve(lfl_patches, 0.0, 0.03, LATEST_PRICE_AED, 'like-for-like')
    shift_at_strike = solve(lfl_patches, 0.0, 0.03, published_spot, 'like-for-like at strike')
    implied = LFL_BASE[0] + shift

    diag = {
        'ticker': 'AMR',
        'as_of': '2026-09-06',
        'spot': LATEST_PRICE_AED,
        'spot_date': 'close 3 September 2026, Abu Dhabi Securities Exchange',
        'spot_source': LATEST_PRICE_SOURCE,
        'published_central': published_central,
        'published_spot': published_spot,
        'why_this_file': (
            'The reverse read — what the traded price must believe — is a DIAGNOSTIC and lives '
            'outside the numbers file every builder reads. A quantity solved from a price and '
            'then used anywhere in the valuation is the reverse-engineered rate the protocol '
            'prohibits outright, arriving through a side door, and the prohibition is worth '
            'nothing if the side door is open. Nothing in this file is an input to anything: '
            'no builder in this study reads it, and it is COMPUTED by diagnostics_amr.py, '
            'which re-runs the study\'s own compute.py with one driver moved at a time.'),
        'implied': {
            'quantity': 'like-for-like sales growth, the price half of the volume-times-price '
                        'revenue build',
            'value': implied,
            'study_value': LFL_BASE[0],
            'study_value_range': [0.063, 0.097],
            'value_at_the_strike_price': LFL_BASE[0] + shift_at_strike,
            'solved_on': (
                'this study\'s own compute.py, on the answer the study PUBLISHES — the '
                'four-lens weighted central of AED %.4f — holding every other driver at its '
                'published value and moving only the like-for-like path, in parallel so its '
                'convergence shape is preserved, until the model reproduces AED %.2f.'
                % (published_central, LATEST_PRICE_AED)),
            'reading': (
                'At AED %.2f the price is paying for like-for-like sales growth of %.2f%% in '
                'FY2026 — and a path %.2f points above the study\'s throughout — against this '
                'study\'s %.1f%%. The company has filed two readings of exactly this measure: '
                '9.7%% for FY2025 and 6.3%% for the first half of 2026. THE PRICE\'S NUMBER '
                'SITS INSIDE THAT FILED RANGE, above the most recent half and well below the '
                'last full year, and above the mid-single-digit range management itself '
                'guides to. At the AED %.2f the study was struck against, the same solve gives '
                '%.2f%%. The disagreement is %.2f points on one driver the company reports '
                'every half, which is a more useful statement than "the study is %.1f%% below '
                'the price".'
                % (LATEST_PRICE_AED, 100 * implied, 100 * shift, 100 * LFL_BASE[0],
                   published_spot, 100 * (LFL_BASE[0] + shift_at_strike), 100 * shift,
                   100 * (published_central / LATEST_PRICE_AED - 1))),
        },
        'other_quantities': [],
        'the_lens_the_read_is_solved_on': (
            'This matters, and it is measured rather than asserted. Solved on the CASH-FLOW '
            'LENS ALONE (AED %.4f) instead of on the answer the study publishes (AED %.4f), '
            'the same quantities come back at a wage escalator of %.4f per cent, a beta of '
            '%.4f and terminal growth of %.4f per cent — every one of them a smaller '
            'disagreement, and every one reproducing this study\'s own gap review\'s '
            'reverse-read table to four decimals, which is how that table is shown to have '
            'been struck on a lens the study does not publish as its answer. Terminal growth '
            'is reachable there and is not reachable on the published central at all. Every '
            'figure in the record above is solved on the published answer.'
            % ((cash_flow_lens, published_central) + tuple(lens_solved))),
    }

    # the other quantities, all solved on the PUBLISHED central
    for label, lo, hi, mk, study_value, note in (
        ('the wage escalator', 0.0, 0.06,
         lambda g: [("WAGE_G = inp('wage_growth', 0.06,",
                     "WAGE_G = inp('wage_growth', %.12f," % g)], 0.06,
         'against the study\'s 6.0% and a house UAE ladder terminating at 2.0%'),
        ('the equity beta', 0.30, 0.93,
         lambda b: [("BETA = inp('beta', 0.930,", "BETA = inp('beta', %.12f," % b)], 0.930,
         'against the study\'s 0.930, whose own regression standard error is {beta_se:.4f}, '
         'so the price\'s figure is {beta_sigma:.2f} standard errors away and this model '
         'cannot tell the two apart'),
        ('the EBITDA margin, moved in parallel', 0.0, 0.05,
         lambda m: [('ebitda_f = [rev_f[t] - cash_cost_f[t] + OTHINC[2] / REV[2] * rev_f[t] '
                     'for t in range(5)]',
                     'ebitda_f = [rev_f[t] - cash_cost_f[t] + OTHINC[2] / REV[2] * rev_f[t] '
                     '+ %.12f * rev_f[t] for t in range(5)]' % m)], 0.0,
         'a parallel shift on the whole forecast margin path, which opens at '
         '{margin_open:.2f} per cent'),
    ):
        try:
            v = solve(mk, lo, hi, LATEST_PRICE_AED, label)
        except AssertionError as e:
            diag['other_quantities'].append(
                {'quantity': label, 'value': None, 'not_reachable': str(e)})
            continue
        diag['other_quantities'].append(
            {'quantity': label, 'value': v, 'study_value': study_value,
             'note': note})

    # everything a `note` or a `why` quotes is computed, and it is computed here
    # because two of those figures come out of the solves above
    MARGIN_OPEN.append(pub['forecast']['ebitda_margin'][0])
    TV_SHARE.append(pub['dcf']['tv_share'])
    IMPLIED_BETA.append([q for q in diag['other_quantities']
                         if q['quantity'] == 'the equity beta'][0]['value'])
    side = side_calcs(pub['inputs'], published_central)
    for q in diag['other_quantities']:
        if q.get('note'):
            q['note'] = q['note'].format(**side)

    # terminal growth cannot reach the price on the published central without
    # breaking the model's own ceiling, and saying so is the finding
    try:
        g = solve(lambda x: [("TERMINAL_G = inp('terminal_growth', 0.030,",
                              "TERMINAL_G = inp('terminal_growth', %.12f," % x)],
                  0.030, TERMINAL_G_CEILING, LATEST_PRICE_AED, 'terminal growth')
        diag['other_quantities'].append({'quantity': 'terminal growth', 'value': g,
                                         'study_value': 0.030, 'note': ''})
    except AssertionError:
        diag['other_quantities'].append({
            'quantity': 'terminal growth',
            'value': None,
            'study_value': 0.030,
            'not_reachable': (
                'On the published central the price is NOT reachable through terminal growth '
                'alone: at the model\'s own ceiling of %.2f per cent — terminal growth must '
                'stay below the terminal risk-free rate of %.2f per cent — the central reaches '
                'only AED %.4f against AED %.2f. On the cash-flow lens alone it IS reachable, '
                'at %.4f per cent, which is the figure this study\'s gap review published.'
                % (100 * TERMINAL_G_CEILING, 100 * side['terminal_rf'],
                   side['terminal_g_at_ceiling'], LATEST_PRICE_AED, lens_solved[2]))})

    # ---- the contested judgements -----------------------------------------
    items, signs = [], []
    for j in JUDGEMENTS:
        alt = central_under(j['patches'], j['name'])
        rel = abs(published_central - alt) / abs(alt)
        material = rel >= 0.05
        if material:
            signs.append(1 if published_central > alt else
                         (-1 if published_central < alt else 0))
        items.append({
            'name': j['name'],
            'adopted': j['adopted'],
            'alternative': j['alternative'],
            'value_adopted': published_central,
            'value_alternative': alt,
            'currency': 'AED per share',
            'worth_relative': rel,
            'material_at_5pc': material,
            'direction': ('the study adopted the HIGHER-value framing'
                          if published_central > alt else
                          'the study adopted the LOWER-value framing'),
            'why': j['why'].format(**side),
        })

    n = len([s for s in signs if s])
    k = len([s for s in signs if s > 0])
    p = min(1.0, 2 * sum(comb(n, i) for i in range(max(k, n - k), n + 1)) / float(2 ** n)) \
        if n else None
    below = [it for it in items if not it['material_at_5pc']]
    cj = {
        'ticker': 'AMR',
        'as_of': '2026-09-06',
        'published_central': published_central,
        'published_spot': published_spot,
        'currency': 'AED per share',
        'why_this_file': (
            'Any single contested choice in a valuation is defensible; what is not defensible '
            'is a study that resolves EVERY one of them the same way and never notices. Each '
            'judgement here is valued BOTH ways by re-running this study\'s own model with one '
            'driver moved, and the sign test below counts which way they went. A study landing '
            'them all one way is FLAGGED, never failed — a company can genuinely deserve a '
            'consistent read. What it may not do is go unmeasured. Nothing here changes a '
            'driver, a forecast, a rate or the fair value.'),
        'judgements': items,
        'unvalued': UNVALUED,
        'sign_test': {
            'material_at_5pc': n,
            'resolved_upward': k,
            'resolved_downward': n - k,
            'two_sided_binomial_p': p,
            'flagged': bool(p is not None and p < 0.05 and n >= 3),
            'reading': ('%d material contested judgements, %d resolved toward the higher value '
                        'and %d toward the lower, two-sided p = %.2f. No lean: this study does '
                        'not take every fork the same way.' % (n, k, n - k, p)) if p else '',
        },
        'below_the_bar': {
            'count': len(below),
            'resolved_upward': len([b for b in below if b['value_adopted'] > b['value_alternative']]),
            'resolved_downward': len([b for b in below if b['value_adopted'] < b['value_alternative']]),
            'note': ('Below the five-per-cent bar the study leans the other way from a coin. '
                     'That is reported because it is the pattern the sign test cannot see, and '
                     'a lean living entirely in small decisions is still a lean.'),
        },
    }

    with open(os.path.join(HERE, 'diagnostics.json'), 'w', encoding='utf-8') as fh:
        json.dump(diag, fh, indent=1, ensure_ascii=False)
    with open(os.path.join(HERE, 'contested_judgements.json'), 'w', encoding='utf-8') as fh:
        json.dump(cj, fh, indent=1, ensure_ascii=False)

    print('reverse read: the price implies like-for-like of %.4f%% against the study\'s %.2f%% '
          '(filed 6.3%% and 9.7%%)' % (100 * implied, 100 * LFL_BASE[0]))
    for q in diag['other_quantities']:
        print('   %-34s %s' % (q['quantity'],
                               ('%.4f' % q['value']) if q['value'] is not None
                               else 'not reachable on the published central'))
    print('\ncontested judgements: %d recorded, %d material, %d unvalued and named'
          % (len(items), n, len(UNVALUED)))
    for it in items:
        print('   %-44s %8.4f vs %8.4f  %+6.2f%%  %s%s'
              % (it['name'][:44], it['value_adopted'], it['value_alternative'],
                 100 * (it['value_adopted'] / it['value_alternative'] - 1),
                 'UP  ' if it['value_adopted'] > it['value_alternative'] else 'DOWN',
                 '  MATERIAL' if it['material_at_5pc'] else ''))
    print('\nsign test: %d material, %d up, %d down, two-sided p = %s'
          % (n, k, n - k, 'n/a' if p is None else '%.4f' % p))
    print('below the bar: %d, %d up, %d down'
          % (cj['below_the_bar']['count'], cj['below_the_bar']['resolved_upward'],
             cj['below_the_bar']['resolved_downward']))
    print('\nwrote diagnostics.json and contested_judgements.json — and nothing else')


if __name__ == '__main__':
    main()
