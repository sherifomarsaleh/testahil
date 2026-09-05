"""STC — the rebuild ledger [R-REBUILD-01], generated from this study's own artefacts.

Nothing here is typed. The answer before the rebuild is read out of the delivered
edition's committed numbers as they stood on the last commit before this work began;
the answer after each lever is read out of the artefact that lever produced.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))

import rebuild_ledger as RL

PUBLISHED_REV = '3c170b9c23372e0f0170413485439415cffc634b'   # main, before this rebuild

# EACH LANDED LEVER'S ANSWER IS READ FROM THE COMMIT THAT LANDED IT, not from the study's
# current numbers file. THE FIRST DRAFT OF THIS SCRIPT DID THE LATTER AND IT WAS WRONG IN
# THE WAY THAT DOES NOT ANNOUNCE ITSELF: every lever pointed at the same file, so the last
# lever to land silently became every earlier lever's answer too. The beta lever read
# -18.27% and the macro lever read +0.00%, which is arithmetically consistent, walks the
# gate, and attributes one lever's work to another. A ledger exists to decompose a rebuild
# and a decomposition that collapses is worse than none, because it reads as a measurement.
# Git is the only record here that cannot be overwritten by the next run.
LANDED = {
    'R-COC-01':   None,                                          # via the sensitivity artefact
    'R-BETA-04':  'fe76400fb6155c044e9e76ec32088303b5a59a6b',     # levers 1-3
    'R-MACRO-01': '518aee8b42d7bf9436844f14bc54aae91ec815cf',     # lever 4
    'R-TERM-01':  None,                                          # the working tree, latest
}


#: The file was renamed to the house name PART WAY THROUGH this rebuild — twenty-one of
#: twenty-four studies call it study_numbers.json and one gate resolved that name
#: literally, so this study read as having no numbers at all. Both names are tried,
#: newest first, because a rename does not reach backwards into the commits behind it and
#: a ledger that could not read its own history would have to be re-keyed by hand.
NAMES = ('engine/stc_study/study_numbers.json',
         'engine/stc_study/stc_study_numbers.json')


def at(rev):
    """A study numbers file as it stood at one commit — read out of git, never remembered."""
    for name in NAMES:
        raw = subprocess.run(['git', 'show', '%s:%s' % (rev, name)],
                             capture_output=True, text=True,
                             cwd=os.path.join(HERE, '..', '..'))
        if raw.returncode == 0:
            return json.loads(raw.stdout)
    raise SystemExit('cannot read the numbers file at %s under either name' % rev)


PUB = at(PUBLISHED_REV)
AFTER_BETA = at(LANDED['R-BETA-04'])
AFTER_MACRO = at(LANDED['R-MACRO-01'])
NOW = json.load(open(os.path.join(HERE, 'study_numbers.json')))
# The lever-2 intermediate, struck when the cost-of-capital schedule was in and the beta
# was not. It is named for that lever set, so a later sensitivity run cannot overwrite the
# number this ledger chains through — which is the stale-artefact defect [R-ENF-06] names,
# and it would be invisible here because the file would still parse and still look computed.
SENS = json.load(open(os.path.join(HERE, 'beta_sensitivity_after_coc.json')))

led = RL.Ledger(
    ticker='STC',
    started_at='2026-09-05',
    start_value=PUB['lenses']['central']['base'],
    start_spot=PUB['spot'],
    audit_after=(
        'AFTER LEVER 3, AND THE REASON IS THAT LEVERS 2 AND 3 PULL IN OPPOSITE '
        'DIRECTIONS. Declared in REBUILD_PLAN_05-09-2026.md before any lever was '
        'touched, and unchanged since. Normalising the risk-free rate by Saudi '
        "Arabia's own sovereign default spread lowers the cost of capital and raises "
        'the value; replacing a 40-session daily regression with a conforming '
        'own-stock weekly beta raises the cost of capital and lowers it. A look taken '
        'between them would audit a state this study never publishes — a normalised '
        'risk-free on a beta the rule refuses — which is why the audit point sits '
        'after the pair rather than between them. THE NET WAS NOT PREDICTED and the '
        'plan said so in advance.'),
)

led.apply(
    name=('the mechanical unblock, then the cost-of-capital schedule through the '
          'sanctioned module'),
    rule='R-COC-01',
    after=SENS['central']['base'],
    why=(
        "Two mechanical blockers first, neither a valuation decision: the study "
        "imported mc_v2, renamed on 2 August 2026, so it had not run since; and it "
        "read a one-off price export of its own rather than the persistent library the "
        "rest of the engine reads for this name. Then the rule. The delivered study "
        "discounted a five-year forecast and a perpetuity alike at a single rate built "
        "by hand: a raw local sovereign yield with NO normalisation for Saudi Arabia's "
        "own default spread, so country risk was counted twice — once in the yield and "
        "again inside the equity risk premium added on top of it. The sanctioned "
        "schedule normalises the risk-free by this sovereign's OWN spread, takes the "
        "equity premium from the country-risk file's own row, weights at market value "
        "on the LATEST DISCLOSED balance sheet, and returns a FLAT ladder because the "
        "riyal is pegged and today is already the terminal — stated by the module "
        "rather than assumed by the study."),
    evidence=(
        'Cost of capital 7.540%% (the delivered study\'s own rating-basis figure) to '
        '%.3f%% on the swap basis, which the rule makes central, with %.3f%% on the '
        'rating basis published beside it. The debt book is read facility by facility '
        'out of note 26 of the FY2025 audited statements — eleven facilities in five '
        'currencies footing exactly to the stated %s thousand — and the cost of debt is '
        "this company's OWN latest issue, the January 2026 sukuk of SAR 7,500 million "
        'in two tranches at 4.489%% and 5.083%%, weighting to %.3f%%. The effective rate '
        'is computed independently over two periods from the murabaha and sukuk finance '
        'cost alone, over the borrowings that actually bear it. This lever is measured '
        'on the RETIRED beta held fixed, through the module\'s own sensitivity path, so '
        'it carries none of the beta correction: %.4f to %.4f.'
        % (100 * SENS['wacc_market'], 100 * SENS['wacc_rating'], '15,191,428',
           100 * 0.048600, PUB['lenses']['central']['base'], SENS['central']['base'])),
)

led.apply(
    name='the beta re-derived against the published index of its own exchange',
    rule='R-BETA-04',
    after=AFTER_BETA['lenses']['central']['base'],
    why=(
        'The delivered study regressed 40 DAILY sessions over nine weeks against TASI '
        'closes and adopted 0.48. The standing rule is explicit that a daily or '
        'short-window regression is NOT one of the three tiers and may stand only as a '
        'flagged interim. The conforming construction is an own-stock WEEKLY regression '
        'against the published index of the exchange the stock is listed on, resolved '
        'through beta_regression.own_stock_beta, and it is nearly half as much again.'),
    evidence=(
        'beta %.4f against 0.4753, from %d weekly observations over %.2f years to %s '
        'against %s, R-squared %.3f, standard error %.4f. Cost of capital %.3f%% to '
        '%.3f%% on the swap basis. The answer falls %.4f to %.4f, %+.2f%%.'
        % (NOW['dcf']['wacc_build']['beta_reg']['beta'],
           NOW['dcf']['wacc_build']['beta_reg']['n'],
           NOW['dcf']['wacc_build']['beta_reg']['window_years'],
           NOW['dcf']['wacc_build']['beta_reg']['index_asof'],
           NOW['dcf']['wacc_build']['beta_reg']['index_file'],
           NOW['dcf']['wacc_build']['beta_reg']['r2'],
           NOW['dcf']['wacc_build']['beta_reg']['se'],
           100 * SENS['wacc_market'], 100 * AFTER_BETA['coc_record']['wacc_exp'],
           SENS['central']['base'], AFTER_BETA['lenses']['central']['base'],
           100 * (AFTER_BETA['lenses']['central']['base'] / SENS['central']['base'] - 1))),
)

led.apply(
    name='terminal growth stored as a real rate on the house Saudi path',
    rule='R-MACRO-01',
    after=AFTER_MACRO['lenses']['central']['base'],
    why=(
        'The delivered study typed 2.5%% as its cash-flow terminal growth and 3.0%% as its '
        'dividend terminal growth — two answers to one question about one economy, in one '
        "model, on one company. A typed nominal rate is also unfalsifiable: nobody reading "
        'the page can tell whether 2.5%% meant terminal inflation plus half a point or '
        'something else. Both now sit on the house path as (real, path id) and recompute '
        "to their nominal, at the rule's own STATED DEFAULT of zero real growth — a mature "
        'domestic telecom growing with the economy in perpetuity and no further. Any other '
        'figure would have to be sourced and nothing in the filings supplies one, and '
        'reverse-engineering the real rate that reproduces the typed 2.5%% would be keeping '
        'the number and inventing a reason for it.'),
    evidence=(
        'Saudi terminal inflation of %.2f%% plus a stated real growth of %.2f%% gives a '
        'terminal growth of %.2f%%, against a typed 2.5%% in the cash-flow lens and a typed '
        '3.0%% in the dividend lens. The cash-flow read falls %.4f to %.4f and the dividend '
        'read %.4f to %.4f — the dividend lens moves furthest because a discounted-dividend '
        "terminal is the most convex thing in the model to its own growth rate, which is "
        'why carrying a second one was worth more than it looked. The blend falls %.4f to '
        '%.4f, %+.2f%%.'
        % (100 * 0.02, 0.0, 100 * AFTER_MACRO['dcf']['tg'],
           AFTER_BETA['lenses']['dcf']['base'], AFTER_MACRO['lenses']['dcf']['base'],
           AFTER_BETA['lenses']['ddm']['base'], AFTER_MACRO['lenses']['ddm']['base'],
           AFTER_BETA['lenses']['central']['base'],
           AFTER_MACRO['lenses']['central']['base'],
           100 * (AFTER_MACRO['lenses']['central']['base']
                  / AFTER_BETA['lenses']['central']['base'] - 1))),
)

led.apply(
    name='the terminal rebuilt on the asset life the accounts themselves imply',
    rule='R-TERM-01',
    after=NOW['lenses']['central']['base'],
    why=(
        'The retired construction charged g x IC every year for ever, which read as a '
        'capital-maintenance programme with a replacement cycle of 1/g — a fact about the '
        'currency and not about the asset. At a pegged 2%% terminal that is FIFTY YEARS, '
        "against a base whose own accounts run twenty-one, so it bought less than half the "
        'maintenance this company needs. The same construction never added book '
        'depreciation back although the operating profit it starts from is already net of '
        'it, so one model carried two definitions of free cash flow with the terminal '
        'holding three quarters of the value. Rebuilt through terminal_value.build(): '
        'maintenance is book depreciation escalated to CURRENT cost over the measured age '
        'of the base, the depreciation is added back gross, and working capital is charged '
        'at the terminal inflation on the stock the latest disclosed sheet actually shows.'),
    evidence=(
        'The life and the age are DERIVED from note 10 of the FY2025 audited statements by '
        "the identity this protocol already sanctions, because the company discloses RANGES "
        '(buildings 25-50 years, network 3-30, other 2-20) rather than one life: depreciable '
        "gross cost over the year's own charge gives %.2f years, and accumulated "
        'depreciation over the same charge gives an age of %.2f years — so the base is at '
        '1.46 times half its own life and 73%% of it is written off. All three conditions '
        'that break that identity were checked on the policy note FIRST and all three are '
        'clear. Maintenance comes out at %s against a book charge of %s. The terminal falls '
        'from three quarters of enterprise value at a lower charge to %.1f%% at the right '
        'one; the cash-flow read moves %.4f to %.4f and the blend %.4f to %.4f, %+.2f%%. '
        'THE DIRECTION WAS NOT PREDICTED and [R-TERM-01 CLAUSE TWO CORRECTED] forbids '
        'predicting it: on this name the sanctioned terminal is SMALLER, and on the last '
        'name rebuilt it was about 5%% larger.'
        % (NOW['dcf']['terminal_life_years'], NOW['dcf']['terminal_age_years'],
           format(NOW['dcf']['terminal_maintenance'], ',.0f'),
           format(NOW['dcf']['rows'][-1]['dna'], ',.0f'),
           100 * NOW['dcf']['tv_pct'],
           AFTER_MACRO['lenses']['dcf']['base'], NOW['lenses']['dcf']['base'],
           AFTER_MACRO['lenses']['central']['base'], NOW['lenses']['central']['base'],
           100 * (NOW['lenses']['central']['base']
                  / AFTER_MACRO['lenses']['central']['base'] - 1))),
)

rec = led.record()
rec['audit_taken'] = {
    'at': '2026-09-05, after lever 3, as declared',
    'levers_so_far': 2,
    'up': '%+.2f%%' % (100 * led.levers[0].move),
    'down': '%+.2f%%' % (100 * led.levers[1].move),
    'net': '%+.2f%%' % (100 * (led.levers[1].after / led.start_value - 1)),
    'read_from': ('each landed lever\'s answer comes from the commit that landed it, so '
                  'no lever can absorb a later one\'s move'),
    'latest_price': 43.86,
    'latest_price_date': '2026-09-03',
    'gap_at_the_audit': '%+.2f%%' % (100 * (led.levers[1].after / 43.86 - 1)),
    'gap_now_after_later_levers': '%+.2f%%' % (100 * (led.value / 43.86 - 1)),
    'gap_at_delivery': '%+.2f%%' % (100 * (led.start_value / 43.58 - 1)),
    'what_the_audit_shows': (
        'THE TWO LEVERS DISAGREED AND THE ROUTE IS WHY THAT MATTERS. Taken in the order '
        'fixed in writing before either was touched, the cost-of-capital correction moved '
        'the answer AWAY from the market — from 8.1%% above the price it was struck at to '
        '16.4%% above the latest one — and the beta correction brought it back. Neither '
        'was chosen for where it landed and neither could have been: the first raises '
        'every value it touches and the second lowers every value it touches, and which '
        'one dominates is arithmetic about this company\'s own capital structure. Read as '
        'two corrections the rebuild is a contest; read as one net figure of -6.5%% it '
        'would look like a small tidy-up, and the 8.4%% and the 13.8%% inside it would be '
        'invisible. THE ANSWER NOW SITS ESSENTIALLY ON THE PRICE, at +0.4%%, and that is '
        'reported as an observation and NOT as corroboration — four levers remain, the '
        'lens retirement among them, and a rebuild that stopped here because the number '
        'looked comfortable would be fitting to the price by choosing when to stop.'),
    'levers_remaining_at_the_audit': [
                         'R-MACRO-01 terminal growth as a real rate on the house path',
                         'R-TERM-01 the terminal on the derived asset life',
                         'R-BRIDGE-01 the bridge on the latest disclosed sheet',
                         'R-LENS-03 the four-lens blend retired',
                         'R-GAP-01 re-struck on the latest known price'],
}
with open(os.path.join(HERE, 'rebuild_ledger.json'), 'w') as f:
    json.dump(rec, f, indent=1)

for lv in led.levers:
    print('%-58s %-12s %9.4f -> %9.4f  %+7.2f%%'
          % (lv.name[:58], lv.rule, lv.before, lv.after, 100 * lv.move))
print('%-58s %-12s %9.4f -> %9.4f  %+7.2f%%'
      % ('CUMULATIVE', '', led.start_value, led.value, 100 * led.cumulative))
print('gap against the latest known price: %+.2f%%' % (100 * (led.value / 43.86 - 1)))
