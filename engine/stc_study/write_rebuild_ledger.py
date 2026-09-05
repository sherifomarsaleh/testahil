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
    'R-TERM-01':  'a8f1f4026c24385e06d9bc493f6f74e7607de52f',     # lever 5
    'R-BRIDGE-01': '7a10176ffdf65947f599b3d472061fc917a4168c',    # lever 5b
    'R-LENS-03':  'accc82d745bccf22f5455d0504c92c7043ee3f56',     # lever 6
    'R-GAP-01':   '750bd6e18d39cea57ea19a6ab096b3335ea9a849',     # lever 7
    'R-SIGCM-02': '57db3fcf6dfac4036f449aa0769d451e6e872ab8',     # the segment rebuild
    'R-SIGCM-02:units': '4996c2f5097ef20628960e14bab1a9a00c2a2ac7',   # the unit build, SAME RULE, so it groups with it
    'R-FCAL-01': '52aade4029cfc181a84069d9e6fabcf92cf2662e',          # capex measured rather than guided
    'R-ANCHOR-01': '34e74f311f05c0e535037cee70d5111a5bbc8c27',    # lever 11
    'R-BRIDGE-01:spectrum': '0a1e324ca29d129c25dc5da50fbcd3b9909decea',   # lever 12
    'R-SIGCM-02:workingcapital': None,                           # the working tree, latest
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
AFTER_TERM = at(LANDED['R-TERM-01'])
AFTER_BRIDGE = at(LANDED['R-BRIDGE-01'])
AFTER_LENS = at(LANDED['R-LENS-03'])
AFTER_GAP = at(LANDED['R-GAP-01'])
AFTER_SEG = at(LANDED['R-SIGCM-02'])
AFTER_UNITS = at(LANDED['R-SIGCM-02:units'])
AFTER_CAPEX = at(LANDED['R-FCAL-01'])
AFTER_ANCHOR = at(LANDED['R-ANCHOR-01'])
AFTER_SPECTRUM = at(LANDED['R-BRIDGE-01:spectrum'])
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
    after=AFTER_TERM['lenses']['central']['base'],
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
        % (AFTER_TERM['dcf']['terminal_life_years'], AFTER_TERM['dcf']['terminal_age_years'],
           format(AFTER_TERM['dcf']['terminal_maintenance'], ',.0f'),
           format(AFTER_TERM['dcf']['rows'][-1]['dna'], ',.0f'),
           100 * AFTER_TERM['dcf']['tv_pct'],
           AFTER_MACRO['lenses']['dcf']['base'], AFTER_TERM['lenses']['dcf']['base'],
           AFTER_MACRO['lenses']['central']['base'],
           AFTER_TERM['lenses']['central']['base'],
           100 * (AFTER_TERM['lenses']['central']['base']
                  / AFTER_MACRO['lenses']['central']['base'] - 1))),
)

led.apply(
    name='the bridge moved onto the latest disclosed balance sheet',
    rule='R-BRIDGE-01',
    after=AFTER_BRIDGE['lenses']['central']['base'],
    why=(
        'The bridge stood on a first-quarter net-debt figure and a 31 March 2026 minority '
        'while a REVIEWED 30 June 2026 balance sheet was already published, in the same '
        'document set this rebuild had just read to source the debt book. The largest line '
        'was not stale but WRONG BY MORE THAN HALF: associates and joint ventures were '
        'carried at SAR 4,641mn against a filed 12,909.648mn, a figure from before February '
        '2025, when the group contributed the whole of its towers business to DIIC in '
        'exchange for 43.06% of it. The towers business the entire 2024 restatement was '
        'about had left the subsidiaries and arrived in the associates, and this bridge had '
        'followed it into neither. Three further lines were corrected on the same sheet: '
        'the listed equity investment is taken at the fair value the company itself '
        'discloses rather than at a mark typed here; the investment funds it holds at fair '
        'value were omitted altogether; and the minority now comes out at its SHARE OF '
        'EQUITY VALUE rather than at historical cost, because the model capitalises 100% of '
        'subsidiary cash flow.'),
    evidence=(
        'Associates and joint ventures 4,641 to %s at book (note 8.1.4, all unlisted); the '
        'listed equity investment %s at its own disclosed Level 1 fair value against a '
        'typed 8,630; investment funds and unlisted equity %s added; net debt %s, built '
        'from borrowings %s and leases %s less non-bank cash %s, short-term murabahas %s, '
        'sukuk %s and treasury bills %s. The minority is %.3f%% of equity value — its own '
        'disclosed share of profit, note 25 — deducting %s against a book of %s. The share '
        'count is 4,993.024mn, footed against par: issued capital of SAR 50,000,000 '
        'thousand at SAR 10 gives the 5,000,000 thousand shares note 17 states, less 6,976 '
        'thousand in treasury. The cash-flow read moves %.4f to %.4f and the blend %.4f to '
        '%.4f, %+.2f%%.'
        % (format(AFTER_BRIDGE['bridge_record']['associates']['value'], ',.3f'),
           format(AFTER_BRIDGE['bridge_record']['lines'][2]['value'], ',.3f'),
           format(AFTER_BRIDGE['bridge_record']['lines'][3]['value'], ',.3f'),
           format(AFTER_BRIDGE['bridge_record']['net_debt_build']['net'], ',.3f'),
           format(AFTER_BRIDGE['bridge_record']['net_debt_build']['borrowings'], ',.3f'),
           format(AFTER_BRIDGE['bridge_record']['net_debt_build']['leases'], ',.3f'),
           format(AFTER_BRIDGE['bridge_record']['net_debt_build']['cash_non_bank'], ',.3f'),
           format(AFTER_BRIDGE['bridge_record']['net_debt_build']['murabahas'], ',.3f'),
           format(AFTER_BRIDGE['bridge_record']['net_debt_build']['sukuk'], ',.3f'),
           format(AFTER_BRIDGE['bridge_record']['net_debt_build']['treasury_bills'], ',.3f'),
           100 * AFTER_BRIDGE['bridge_record']['nci']['profit_share'],
           format(AFTER_BRIDGE['bridge_record']['nci']['deduction'], ',.3f'),
           format(AFTER_BRIDGE['bridge_record']['nci']['book'], ',.3f'),
           AFTER_TERM['lenses']['dcf']['base'], AFTER_BRIDGE['lenses']['dcf']['base'],
           AFTER_TERM['lenses']['central']['base'],
           AFTER_BRIDGE['lenses']['central']['base'],
           100 * (AFTER_BRIDGE['lenses']['central']['base']
                  / AFTER_TERM['lenses']['central']['base'] - 1))),
)

led.apply(
    name='the four-lens blend retired for the class primary',
    rule='R-LENS-03',
    after=AFTER_LENS['lenses']['central']['base'],
    why=(
        'The delivered central was a BLEND of four lenses at typed weights — 35% cash flow, '
        '25% dividend discount, 20% relative multiple, 20% normalised earnings — that '
        'nobody chose on evidence and no out-of-sample test ever cleared. Two of those four '
        'are not permitted cross-checks for a telecom operator at all and carried 45% of '
        'the answer between them. A number produced by averaging several methods is not '
        'more robust than the best of them: it is a NEW method with free parameters nobody '
        'tested, wearing the appearance of caution, and it imports every weakness of the '
        'weakest lens at whatever weight somebody typed. The registry gives this class a '
        'CASH-FLOW primary cross-checked on an EV/EBITDA multiple from its own history and '
        'on book value, so the cash-flow read IS the central and the others are published '
        'beside it.'),
    evidence=(
        'The central becomes the cash-flow read at %.4f, from a blend of %.4f. The '
        'dividend-discount read of %.4f and the normalised-earnings read of %.4f come out '
        'of the answer entirely. THE MULTIPLE IS NOW COMPUTED RATHER THAN TYPED: the study '
        'used 8.0 / 9.0 / 10.0 with no source of any kind, and its base of 9.0 sat within a '
        'rounding of the %.3fx the shares trade at today — which values the company at what '
        'it already trades at. The adopted %.3fx is the mean of this company\'s own trailing '
        'EV/EBITDA at the last three year ends (%.3fx, %.3fx, %.3fx), each computed from '
        "that year-end's own close in the persistent price library, the shares in issue and "
        "that year's net debt and EBITDA from the filings. Every one of the three sits BELOW "
        'the traded multiple, so the lens can be SEEN not to be anchored on the price. Book '
        'value of %.4f is published as the disclosed floor it is and is never weighted. The '
        'bear and bull are flexed on capital intensity between the 15.0%% and 17.5%% of '
        'revenue management guides to, with the macro path standing still across all three '
        "— the delivered study's corners moved the cost of capital by 100 and 70 basis "
        'points and terminal growth between 2.0%% and 3.0%% as well, which makes each corner '
        'an economy nothing describes.'
        % (AFTER_LENS['lenses']['central']['base'],
           AFTER_BRIDGE['lenses']['central']['base'],
           AFTER_LENS['lenses']['ddm']['base'],
           AFTER_LENS['lenses']['normalized']['base'],
           AFTER_LENS['lens_record']['cross_checks'][0]['circularity']['traded_multiple'],
           AFTER_LENS['rel_basis']['evx']['base'],
           AFTER_LENS['lenses']['own_history_evx'][0]['x'],
           AFTER_LENS['lenses']['own_history_evx'][1]['x'],
           AFTER_LENS['lenses']['own_history_evx'][2]['x'],
           AFTER_LENS['lenses']['book_value'])),
)

led.apply(
    name='the answer and the price it is measured against, published where they can be read',
    rule='R-GAP-01',
    after=AFTER_GAP['lenses']['central']['base'],
    why=(
        'THE MOVE IS ZERO AND THAT IS THE FINDING RATHER THAN AN OMISSION. The rule wants '
        'the central put against the LATEST KNOWN price before any delivery, and the '
        'valuation has been struck on that price since the cost-of-capital lever, because '
        'the schedule reads the supplied close register directly — so there was nothing '
        'left to re-strike by the time this lever arrived. What WAS missing is that neither '
        'the answer nor the price appeared anywhere a reader or a checker could find them: '
        'the study exposed no central at all, so every gate that audits an ANSWER rather '
        'than a step reported it unreadable, and an unreadable study is not a clean one — '
        'it is the cheapest possible route past an audit. Both are now published at the top '
        'level of the committed record.'),
    evidence=(
        'Central %.4f against the latest known close of SAR %.2f on %s, a gap of %+.2f%%, '
        'inside the ten per cent band either way, so no eight-heading review is owed and '
        'the publication block does not fire on the gap. TWO CLOCKS ARE NOW NAMED RATHER '
        'THAN CONFLATED: the valuation is struck against that latest known close, and the '
        'Monte Carlo cone against SAR %.2f on %s, the last session in the persistent price '
        'library, because a cone has to start where its own price series ends. Publishing '
        'one number for both would either strike the cone on a session that is not in its '
        'series or measure the gap against a price the market has already left. STC comes '
        'off the valuation-gap ratchet, which now carries no breaching study at all and one '
        'unreadable one.'
        % (AFTER_GAP['lenses']['central']['base'], AFTER_GAP['spot'],
           AFTER_GAP['spot_date'],
           100 * (AFTER_GAP['lenses']['central']['base'] / AFTER_GAP['spot'] - 1),
           AFTER_GAP['cone_anchor'], AFTER_GAP['cone_anchor_date'])),
)

led.apply(
    name='revenue and margin rebuilt on the eleven disclosed segments',
    rule='R-SIGCM-02',
    after=AFTER_SEG['lenses']['central']['base'],
    why=(
        'A SECOND STAGE, DECLARED IN DRIVER_REBUILD_05-09-2026.md BEFORE IT WAS CODED, with '
        'its own audit point after the whole rebuild rather than inside it. The seven levers '
        'of the plan are landed; this is not a reshaping of them. The study forecast four '
        'typed arrays over a taxonomy the filings do not use, with no source, date or layer '
        'on any of them. The company discloses eleven to thirteen operating segments with '
        'revenue AND gross profit for every one, three filed years, all six columns footing '
        "to their own filing's stated total. Each segment now grows at its own MEASURED real "
        'rate, deflated by a published price index from the same database the house ladder '
        'comes from, fading to zero real by the last explicit year so that no segment is '
        'capitalised at a rate it never reached. And the margin becomes an OUTPUT: gross '
        'profit is built per segment at its own disclosed rate and EBITDA is that less one '
        "cost line at its own three-year average share of revenue, instead of a margin path "
        'typed above them.'),
    evidence=(
        'Revenue compounds at %.2f%% nominal against the delivered arrays\' %.2f%%, because '
        'the measured rates are lower than the typed ones: stc, two thirds of revenue, grows '
        '+0.16%% real, Channels -2.10%%, Solutions +5.53%%, the group +2.33%%. The EBITDA '
        'margin comes out at %.2f%% in the first forecast year against a filed %.2f%% — a '
        'relative gap of %.2f%%, well inside [R-ANCHOR-01]\'s five per cent trigger, so the '
        'forecast does not open materially below the latest filed period and owes no '
        'mechanism. The answer falls %.4f to %.4f, %+.2f%%, and the gap against the latest '
        'known price goes %+.1f%% to %+.1f%% — past [R-GAP-01]\'s trigger, so the '
        'eight-heading review is written and committed as GAP_REVIEW_05-09-2026.md. THE SIZE '
        'WAS DECLARED UNPREDICTED IN ADVANCE and it was: group real growth of +2.33%% '
        'trailing is close to what the delivered arrays imply in aggregate, and what changed '
        'is the COMPOSITION, because four aggregates do not map onto eleven segments and a '
        'segment growing at its own rate compounds differently from a blend growing at an '
        'average of them.'
        % (100 * ((AFTER_SEG['forecast']['FY30E']['rev'] / 77_818.675) ** 0.2 - 1),
           100 * ((93_373.0 / 77_818.675) ** 0.2 - 1),
           100 * AFTER_SEG['forecast']['FY26E']['ebitda_margin'],
           100 * 24_469.435 / 77_818.675,
           100 * (AFTER_SEG['forecast']['FY26E']['ebitda_margin']
                  / (24_469.435 / 77_818.675) - 1),
           AFTER_GAP['lenses']['central']['base'],
           AFTER_SEG['lenses']['central']['base'],
           100 * (AFTER_SEG['lenses']['central']['base']
                  / AFTER_GAP['lenses']['central']['base'] - 1),
           100 * (AFTER_GAP['lenses']['central']['base'] / AFTER_SEG['spot'] - 1),
           100 * (AFTER_SEG['lenses']['central']['base'] / AFTER_SEG['spot'] - 1))),
)

led.apply(
    name='the one segment with unit data built as volume times price',
    # THE SAME RULE AS THE LEVER ABOVE, deliberately: two levers serving one rule are ONE
    # piece of evidence, and keying this one differently would let a reader count the
    # segment rebuild and the unit build as two independent confirmations of a single
    # correction, which is exactly what by_rule() exists to prevent.
    rule='R-SIGCM-02',
    after=AFTER_UNITS['lenses']['central']['base'],
    why=(
        'The stage above sat at the disclosed segment level and flagged that volume times '
        'price was out of reach because the financial statements carry no subscriber '
        'counts. THE GAP WAS IN THE REGISTER RATHER THAN IN THE WORLD: four guessed '
        'investor-relations URLs had failed and been written up as evidence the channel '
        'was gone, and the earnings presentations were one sitemap away, carrying the '
        'subscriber base by category at three fiscal year ends. The stc segment — the KSA '
        'operating business, two thirds of group revenue — is now built from its two '
        'halves, each faded on the same schedule and MULTIPLIED, which is the identity '
        'revenue actually obeys.'),
    evidence=(
        'Subscribers compound at %+.2f%% a year and revenue per subscriber falls %+.2f%% '
        'nominal, and (1 %+.4f) x (1 %+.4f) - 1 returns exactly the +1.91%% the audited '
        'statements report for that segment. THE ANSWER BARELY MOVES AND IT WAS NOT '
        'EXPECTED TO: fading the net drops the cross-term the product keeps, worth about '
        'five basis points a year, so %.4f becomes %.4f, %+.2f%%. The gain is not the five '
        'basis points — it is that the forecast now rests on a volume line and a price line '
        'a reader can see and disagree with separately, where before it rested on one net '
        'rate that showed neither. Saudi mobile penetration is already far above one line '
        'per person and the two are not equally likely to persist, which is a judgement a '
        'later edition can now make with a reason.'
        % (100 * AFTER_UNITS['drivers']['unit_volume_real'],
           100 * ((1 + AFTER_UNITS['drivers']['unit_price_real']) * (1.0175) - 1),
           AFTER_UNITS['drivers']['unit_volume_real'],
           (1 + AFTER_UNITS['drivers']['unit_price_real']) * 1.0175 - 1,
           AFTER_SEG['lenses']['central']['base'],
           AFTER_UNITS['lenses']['central']['base'],
           100 * (AFTER_UNITS['lenses']['central']['base']
                  / AFTER_SEG['lenses']['central']['base'] - 1))),
)

led.apply(
    name='capital expenditure measured from the filings instead of taken from guidance',
    rule='R-FCAL-01',
    after=AFTER_CAPEX['lenses']['central']['base'],
    why=(
        "The capital-expenditure path was management's OWN PUBLISHED GUIDANCE BAND — 16.5% "
        'of revenue falling to 15.0% — taken straight in as an input. The rule is explicit '
        'that GUIDANCE IS SCORED AND NEVER CONSUMED, because a forward target leans the '
        'same way an optimistic model does and a driver that takes it inherits the lean '
        'instead of correcting for it. What this company actually spends is disclosed for '
        'three years, and the ratio that matters is capital expenditure over the '
        'depreciation of the base it renews. THE GAP REVIEW NAMED THIS AS THE SUSPECT HALF '
        'BEFORE ANYONE KNEW WHICH WAY THE CORRECTION WOULD RUN, which is the review working '
        'rather than a coincidence.'),
    evidence=(
        'The filed ratio runs %.3fx, %.3fx and %.3fx, a mean of %.3fx against the 1.352x a '
        'base maintained at CURRENT cost would need — so the adopted path is %.2f%% of '
        'revenue, BELOW the guided one, and the answer RISES %.4f to %.4f, %+.2f%%. The step '
        'at the terminal boundary is therefore larger rather than smaller and is stated with '
        'its reason: an explicit window may continue an observed under-maintenance for five '
        'years and a perpetuity may not, because a company that never replaces its plant is '
        'not a going concern — and the accounts support that independently, with 73%% of the '
        'depreciable base written off and its measured age rising 13.60 to 14.18 to 15.23 '
        'years. The industry-specific alternative is recorded rather than dismissed: if '
        'telecommunications equipment falls in real cost per unit of capacity, the terminal '
        'charge is too high and the gap is priced equipment rather than deferred '
        'maintenance. No disclosed replacement-cost series exists to separate them. The '
        'dividend-cover rungs are recomputed from the same measured ratio, because their '
        'old labels named a guidance band the model had stopped using.'
        % (AFTER_CAPEX['drivers']['capex_to_dna_history'][0],
           AFTER_CAPEX['drivers']['capex_to_dna_history'][1],
           AFTER_CAPEX['drivers']['capex_to_dna_history'][2],
           AFTER_CAPEX['drivers']['capex_to_dna_adopted'],
           100 * AFTER_CAPEX['drivers']['capex_pct'][0],
           AFTER_UNITS['lenses']['central']['base'],
           AFTER_CAPEX['lenses']['central']['base'],
           100 * (AFTER_CAPEX['lenses']['central']['base']
                  / AFTER_UNITS['lenses']['central']['base'] - 1))),
)

led.apply(
    name='the first forecast year anchored on the latest reviewed period',
    rule='R-ANCHOR-01',
    after=AFTER_ANCHOR['lenses']['central']['base'],
    why=(
        'THE MOST RECENT REVIEWED PERIOD HAD BEEN READ AND WAS NOT USED. The six months to '
        '30 June 2026 are published and reviewed, and the model was growing FY2025 forward '
        'as though they were not. The standing rule is that a near-term reviewed actual '
        'OUTRANKS a stale full-year rate: anchor every rate on the most recent reviewed '
        'period, hold everything else flat INCLUDING observed improvements, and where a '
        "first-half rate is carried into the second half PROVE with the prior year's actual "
        'halves which way it runs. Note 4 of that interim gives revenue by segment for both '
        "halves and the group's cost of operations excluding depreciation, so the level and "
        'both rates come from one note, and every seasonality factor is the prior year own '
        'half against its own full year — measured rather than assumed.'),
    evidence=(
        'The reviewed half reports revenue of SAR 40,110mn and an EBITDA margin of 32.33%%. '
        'Corrected by the prior year measured half-to-year factors (%.5f on revenue, %.5f '
        'on the gross margin, %.5f on the operating-cost share) that anchors FY2026 at '
        'revenue %.0f and an EBITDA margin of %.2f%%. THE MODEL HAD %.2f%% AND 80,224 — '
        'eighty-nine basis points below a margin the company had ALREADY REPORTED for half '
        'the year, and 0.6%% below the revenue that half implies. The answer rises %.4f to '
        '%.4f, %+.2f%%, and the gap narrows %+.1f%% to %+.1f%%. It is the strongest '
        'evidence in the whole review because it is not a forecast at all: it is a '
        'disclosed actual the model had not been shown. Nothing after the first year '
        'assumes any further gain — the rule says hold flat including observed '
        'improvements, and the margin drifts DOWN on mix from there.'
        % (AFTER_ANCHOR['drivers']['h1_anchor']['season_revenue'],
           AFTER_ANCHOR['drivers']['h1_anchor']['season_gross_margin'],
           AFTER_ANCHOR['drivers']['h1_anchor']['season_sga_share'],
           AFTER_ANCHOR['drivers']['h1_anchor']['revenue'],
           100 * AFTER_ANCHOR['forecast']['FY26E']['ebitda_margin'],
           100 * 0.310873,
           AFTER_CAPEX['lenses']['central']['base'],
           AFTER_ANCHOR['lenses']['central']['base'],
           100 * (AFTER_ANCHOR['lenses']['central']['base']
                  / AFTER_CAPEX['lenses']['central']['base'] - 1),
           100 * (AFTER_CAPEX['lenses']['central']['base'] / NOW['spot'] - 1),
           100 * (AFTER_ANCHOR['lenses']['central']['base'] / NOW['spot'] - 1))),
)

led.apply(
    name='the spectrum-licence liability into net debt, a claim disclosed outside borrowings',
    rule='R-BRIDGE-01',
    after=AFTER_SPECTRUM['lenses']['central']['base'],
    why=(
        'A CLAIM AHEAD OF EQUITY WAS DISCLOSED IN A NOTE THE BRIDGE DID NOT OPEN. The '
        'bridge already stood on the latest disclosed sheet and read its borrowings, its '
        'leases and its cash correctly; what it did not read is note 14.1, where '
        'consideration owed to the regulator for spectrum licences ALREADY capitalised as '
        'intangible assets sits on its own row inside "financial liabilities and others", '
        'nowhere near the borrowings lines. This is the same shape as the two other '
        'defects this rebuild found — the associates line and the reviewed half — a figure '
        'in a note the build did not open, in a document it had already fetched. Two of '
        'the three raised the answer and this one lowers it, so the pattern is a reading '
        'habit rather than a lean.'),
    evidence=(
        'Note 14.1 of the reviewed interim to 30 June 2026 carries financial liabilities '
        'related to frequency spectrum licences of %s (31 December 2025: 3,803.108). Net '
        'debt goes %s to %s. IT IS NOT DOUBLE-COUNTED AGAINST CAPITAL EXPENDITURE and that '
        "was established rather than assumed: the company's total additions to property, "
        'equipment, intangibles and goodwill were 13,815.240 in FY2025 against the 11,795 '
        'of capital expenditure this model forecasts on, and note 12(2) states that '
        'additions include NON-CASH additions of 2,122 million (FY2024: 883). The model '
        'therefore runs on CASH capital expenditure, the licences bought against this '
        'liability never entered it, and the unpaid consideration is a financing claim the '
        'discounted cash flows do not service. The answer falls %.4f to %.4f, %+.2f%%, and '
        'the gap widens to %+.1f%%.'
        % ('%.3f' % AFTER_SPECTRUM['bridge_record']['net_debt_build']['spectrum_licences'],
           '%.3f' % (AFTER_SPECTRUM['bridge_record']['net_debt_build']['net']
                     - AFTER_SPECTRUM['bridge_record']['net_debt_build']['spectrum_licences']),
           '%.3f' % AFTER_SPECTRUM['bridge_record']['net_debt_build']['net'],
           AFTER_ANCHOR['lenses']['central']['base'],
           AFTER_SPECTRUM['lenses']['central']['base'],
           100 * (AFTER_SPECTRUM['lenses']['central']['base']
                  / AFTER_ANCHOR['lenses']['central']['base'] - 1),
           100 * (AFTER_SPECTRUM['lenses']['central']['base'] / NOW['spot'] - 1))),
)


led.apply(
    name='working capital projected from the asset-conversion cycle instead of plugged',
    rule='R-SIGCM-02',
    after=NOW['lenses']['central']['base'],
    why=(
        'SIGCM CLAUSE 4 REQUIRES THE CYCLE TO BE STUDIED AND THE BALANCE SHEET PROJECTED '
        'FROM IT, with no unexplained plugs where the drivers are disclosed. This study '
        'carried a typed working-capital outflow of 0.8%% of revenue falling to 0.4%% — a '
        'number per year with no balance sheet behind it, which is the plug the clause names. '
        'And the drivers ARE disclosed, in unusual detail: receivables with an ageing '
        'analysis and the government share of the book, inventory with ITS OWN cost base '
        'stated in the note, payables with a stated settlement range, and the two contract '
        'balances a telecom actually turns over and which no cash-cycle built from three '
        'lines would see.'),
    evidence=(
        'WHAT THE PLUG WAS HIDING: net working capital ran 5.9%%, 6.5%% and 13.2%% of revenue '
        'across the filed years and 17.5%% at the reviewed half — it MORE THAN DOUBLED in '
        'FY2025 and rose again in the half — while the plug said the outflow shrank every '
        'year. Days sales outstanding went 108.8 to 106.9 to 125.4 on a book where '
        'government and government-related entities owe 75%% of the gross receivable, and '
        'days payable fell 11.6. The days are anchored on the LATEST DISCLOSED sheet and '
        'then held flat, which matters: receivables were essentially unchanged across the '
        'half (26,727,198 to 26,727,997) while revenue grew, so the days fall to 120.8 '
        'without anything being assumed. Projected, the five-year outflow is %.0f against '
        'the plug\'s %.0f. The answer rises %.4f to %.4f, %+.2f%%, and the gap narrows to '
        '%+.1f%%. TWO THINGS ARE RECORDED RATHER THAN REPAIRED: the measured trade payable '
        'days (161, 185, 229) do not reconcile with the 90-107 the filings state, because '
        'trade payables are not bought only against inventory and the purchases actually on '
        'trade terms are not disclosed — so the right denominator cannot be built and is not '
        'invented; and the conventional cash cycle MIXES DENOMINATORS, so at 18.6 days it is '
        'not net working capital in days of revenue, which is 64. Both are published and the '
        'projection runs on the second.'
        % (sum(r['dwc'] for r in NOW['dcf']['rows']),
           sum(r['dwc'] for r in AFTER_SPECTRUM['dcf']['rows']),
           AFTER_SPECTRUM['lenses']['central']['base'], NOW['lenses']['central']['base'],
           100 * (NOW['lenses']['central']['base']
                  / AFTER_SPECTRUM['lenses']['central']['base'] - 1),
           100 * (NOW['lenses']['central']['base'] / NOW['spot'] - 1))),
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
