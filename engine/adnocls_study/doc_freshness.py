"""Do the delivered documents actually carry the delivered numbers?

recalc.py ties the workbook to study_numbers.json cell by cell. Nothing tied the Word
documents to it at all, so a study rebuilt from a stale numbers file would pass the
vocabulary scrub, the table-width check, the figure check and the label gate while
quoting a fair value the model no longer produces. That is exactly the failure the
beta rebuild could have shipped.

Three assertions, and the distinction between the second and third is the whole point.
Every headline figure the model currently produces must appear in the rendered text —
that proves the rebuild ran. Every figure of the ALTERNATIVE construction must also
appear — the study publishes both legs and dropping one would be a silent retreat from
the dual framing. Only the FRAMING the rebuild replaced is banned, never a number: the
alternative leg's cost of capital and terminal share look exactly like the superseded
edition's, because on that leg they still are its numbers.
"""
import os, re, sys, json, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, 'study_numbers.json')))
STUDY = os.path.join(HERE, 'ADNOCLS_Valuation_Study_09-08-2026_public.pdf')
BIB = os.path.join(HERE, 'ADNOCLS_Bibliography_09-08-2026.pdf')


def text(pdf):
    return subprocess.run(['pdftotext', '-layout', pdf, '-'],
                          capture_output=True, text=True).stdout


def money(x):
    return f'{x:,.2f}'


bf = D['beta_framing']
W, FL, BK, REL, FIN = D['wacc'], D['fleet'], D['book'], D['rel'], D['fin']
IN = {k: v['value'] for k, v in D['inputs'].items()}
PEERS = REL['peers']
# figures the SECOND round of corrections produced, derived here exactly as the builders
# derive them, so a document that carries a stale version of any of them is caught
BLEND_PE_TTM = ((1 - REL['spot_weight']) * PEERS[0]['pe_ttm']
                + REL['spot_weight'] * PEERS[1]['pe_ttm'])
OWN_PE_FWD = D['meta']['mktcap_usd000'] / REL['npa_ord_26']
PB_MARKET_ORD = W['mktcap'] / IN['q1_26_eqp']
NET_DEBT_TOTAL = (D['bridge']['net_debt_company'] + D['bridge']['deferred']
                  + IN['acq_2026_cost'])
SN = D['sens']
BETA_ONLY_BEAR = SN['grid_beta_g'][SN['betas'].index(bf['ci90'][1])][
    SN['gs'].index(IN['g_terminal'])]

# The two superseded editions' headline figures, recovered from the register the reviews
# were adjudicated in — the same recovery the study builder does, so the running total the
# study prints is checked against the file it came from rather than against itself.
_ADJ = json.load(open(os.path.join(HERE, 'critique_adjudication.json')))
N_FINDINGS = len(_ADJ)


def _prior(field, key):
    counts = {}
    for r in _ADJ:
        for chunk in re.split(r';', r.get(field) or ''):
            if key in chunk.lower():
                m = re.search(r'(\d+\.\d\d)\s*(?:→|->)', chunk)
                if m:
                    counts[m.group(1)] = counts.get(m.group(1), 0) + 1
                break
    assert counts, f'no prior {key} recoverable from the review register'
    return float(max(counts, key=counts.get))


CENTRAL_ED1 = _prior('claimed_impact', 'weighted central')
_ed2 = {}
for _r in _ADJ:
    _m = re.search(r'central from (\d+\.\d+) to', _r.get('evidence') or '')
    if _m:
        _ed2[_m.group(1)] = _ed2.get(_m.group(1), 0) + 1
assert _ed2, 'no second-edition central recoverable from the review register'
CENTRAL_ED2 = float(max(_ed2, key=_ed2.get))

MUST = [
    ('the adopted beta', f"{D['inputs']['beta']['value']:.3f}"),
    ('the alternative beta', f"{D['inputs']['beta_composite']['value']:.3f}"),
    ('the cash-flow lens', money(D['lenses']['dcf']['base'])),
    ('the alternative cash-flow lens', money(D['lenses']['dcf_beta_alt']['base'])),
    ('the weighted central', money(D['central'])),
    ('the alternative central', money(D['central_beta_alt'])),
    ('the relative lens', money(D['lenses']['relative']['base'])),
    ('the normalised lens', money(D['lenses']['normalized']['base'])),
    ('the book lens', money(D['lenses']['book']['base'])),
    ('the market price', money(D['meta']['spot_aed'])),
    ('the cost of equity', f"{bf['primary']['ke'] * 100:.2f}"),
    ('the cost of capital', f"{W['wacc'] * 100:.2f}"),
    ('the terminal cost of capital', f"{W['wacc_term'] * 100:.2f}%"),
    ('the terminal-value share', f"{D['dcf']['tv_share'] * 100:.0f}%"),
    # the rebuilt tanker leg — the published blend and the rate solved out of it must BOTH
    # be present, because the whole correction is the difference between them
    ('the published first-quarter blend', f"{FL['blend_q1_26']['vlcc']:,.0f}"),
    ('the implied first-quarter spot', f"{FL['spot_q1_26']['vlcc']:,.0f}"),
    ('the implied second-quarter spot', f"{FL['spot_q2_26']['vlcc']:,.0f}"),
    ('the charter count', f"{len(FL['charters'])}"),
    # the perpetual securities now carry a weight as well as a deduction
    ('the perpetual weight', f"{W['wh'] * 100:.1f}%"),
    ('the perpetual coupon rate', f"{W['kh'] * 100:.2f}%"),
    ('the ordinary equity weight', f"{W['we'] * 100:.1f}%"),
    # the asset lens is residual income, so its fade and its terminal share must show
    ('the residual-income fade', f"{BK['fade'] * 100:.0f}%"),
    # the enterprise multiple, published on both bases
    ('the enterprise multiple, market basis', f"{REL['own_ev_ebitda_26']:.2f}"),
    ('the enterprise multiple, bridge basis', f"{REL['own_ev_ebitda_26_bridge']:.2f}"),
    # earnings per share struck after the coupon, with the pre-coupon figure as a memo
    ('earnings per share after the coupon', f"{FIN['eps'][0]:.3f}"),
    ('earnings per share before the coupon', f"{FIN['eps_pre_coupon'][0]:.3f}"),
    # the minority deduction is neither book nor a flat share of value
    ('the minority deduction', f"{D['dcf']['nci'] / 1000.0:,.0f}"),
    ('the contracted minority at book', f"{D['dcf']['nci_navig8'] / 1000.0:,.0f}"),
    # ---- the second round of corrections. Each of these was a defect in the previous
    # edition and each has exactly one figure that proves it has been acted on.
    # The vessel purchase the previous edition omitted altogether: its cost has to appear
    # in the bridge, and the bridge total has to be the three components added.
    ('the August purchase, in the bridge', f"{IN['acq_2026_cost'] / 1000.0:,.0f}"),
    ('the bridge deduction, all three components',
     f"{NET_DEBT_TOTAL / 1000.0:,.0f}"),
    ('the crude carriers bought', f"{IN['acq_2026_vlcc']:,.0f}"),
    # the smallest tankers, no longer carried at a rate that moved the opposite way
    ('the handysize scaling', f"{IN['handysize_relative']:.2f}×"),
    # receivable days, on both the basis they were calibrated on and the one they are used on
    ('receivable days, re-based', f"{IN['dso_days']:,.1f}"),
    ('receivable days, as reported', f"{IN['dso_days_reported']:,.1f}"),
    # the cost of debt, published as the average it is AND as the weighted figure it is not
    ('the cost of debt, the average adopted', f"{W['kd'] * 100:.2f}%"),
    ('the cost of debt, balance-weighted',
     f"{W['kd_balance_weighted'] * 100:.2f}%"),
    # the depreciation rate kept, with the rate a reviewer proposed and the disclosed lives
    ('the depreciation rate used', f"{IN['dep_rate_ppe'] * 100:.2f}%"),
    ('the realised depreciation rate a reviewer proposed',
     f"{IN['dep_rate_realised_fy25'] * 100:.2f}%"),
    ('the disclosed useful lives', 'depreciated straight line'),
    # the earnings multiple, on both bases
    ('the earnings multiple, forward', f"{REL['blend_pe']:.2f}×"),
    ('the earnings multiple, trailing', f"{BLEND_PE_TTM:.2f}×"),
    ("the company's own multiple, forward", f"{OWN_PE_FWD:.2f}×"),
    # price to book on the SAME book the asset lens values
    ('price to book, ordinary equity', f"{PB_MARKET_ORD:.2f}×"),
    # the bear bound with the beta on its own, so the composite bound cannot be
    # re-described as the statistics alone
    ('the beta-only bear', f"{BETA_ONLY_BEAR:,.2f}"),
    # the running total across both rounds of review
    ('the review count', f"{N_FINDINGS:,}"),
    ('the first edition central', f"{CENTRAL_ED1:,.2f}"),
    ('the second edition central', f"{CENTRAL_ED2:,.2f}"),
]

# The alternative construction is PUBLISHED, not superseded, so its figures must be
# present. Only the framing the rebuild replaced is banned. Getting this distinction
# wrong is how a freshness check starts failing correct documents: 7.31% and an 84%
# terminal share are not stale numbers, they are the alternative leg's own numbers and
# the study is required to carry them.
ALTERNATIVE = [
    ('the alternative beta', f"{D['inputs']['beta_composite']['value']:.3f}"),
    ('the alternative cost of capital',
     f"{D['dcf_beta_alt']['wacc'] * 100:.2f}%"),
    ('the alternative terminal share',
     f"{D['dcf_beta_alt']['tv_share'] * 100:.0f}% of enterprise value"),
]
# Framing the rebuild replaced. A sentence carrying one of these has not been reached,
# however clean everything else looks.
# Regexes, not substrings, and the reason is a bug this check produced on itself:
# 'beta of 1.0' matches the PREFIX of 'beta of 1.085', so a plain substring test failed
# the document for containing the very figure it is supposed to contain. Every pattern
# here ends on a boundary.
SUPERSEDED = [
    ('asset-risk beta wording', r'asset-risk beta'),
    ('asset beta wording', r'asset beta'),
    ('beta-of-one wording', r'beta of one\b'),
    ('beta-of-1.0 wording', r'beta of 1\.0(?!\d)'),
    ('beta-of-1 wording', r'beta of 1(?![\d.])'),
    # The four corrections this edition makes each had a sentence that justified the
    # superseded construction. Those sentences are what must not survive — not the numbers,
    # and not the words used to DESCRIBE the superseded construction in the section that
    # exists to describe it. Each pattern below is a justification, never a description.
    ('the old excuse for leaving the perpetuals out of the weights',
     r'rather than carried in the weights'),
    ('the old excuse, second half', r'do not enter the cost of capital twice'),
    ('the justified-multiple lens presented as the method',
     r'a justified [\d.]+. book value on'),
    ('the justified-multiple formula presented as the method',
     r'A justified price-to-book multiple is the sustainable return'),
    ('the published class rate presented as a spot rate',
     r'trade at spot rates and \d+ sit on'),
    # ---- the second round. Same rule as above and it bites harder here, because two of
    # these corrections work by REPRINTING the superseded claim next to the correction. A
    # pattern that cannot tell the assertion from the quotation of it would fail the very
    # document that does the right thing, so each one below is anchored on something only
    # the assertion carries.
    #
    # The gross-up caveat. The corrected text carries the same words — deliberately, because
    # the claim is reprinted rather than deleted — but sets the conclusion in CAPITALS
    # before correcting it. These patterns are matched case-sensitively (re.findall with no
    # flags), so the lowercase assertion is banned and the capitalised quotation of it is
    # not. That is the whole distinction, and it is the reason this pattern is not folded
    # into a case-insensitive scan.
    ('the gross-up claimed to be unable to reach the valuation',
     r'so it cannot\s+affect\s+the\s+valuation'),
    ('the gross-up caveat headed as merely presentational',
     r'gross-up for the tanker fleet is presentational\.'),
    # The cost of debt described as weighted. The correction quotes the superseded phrase
    # inside typographic quotation marks, so the ban is on the phrase used bare.
    ('the average cost of debt described as weighted',
     r'(?<![“"])weighted across the drawn book'),
    # The handysize substitution. The corrected build says "carried at the medium-range rate
    # SCALED BY", and the description of the superseded build says "carried THEM at the
    # medium-range rate unadjusted"; only the superseded assertion reads "and are carried at".
    ('the handysize substitution asserted as the build',
     r'and are carried at the medium-range rate'),
    # Two conventions spliced into one series, and a table that did not foot
    ('return on equity spliced across two conventions',
     r'and the five forecast years average'),
    ('guidance presented as published dollar figures',
     r'Guidance is the midpoint of the ranges the company published'),
]

fails = []
t = text(STUDY)
print('=' * 74)
print('the study carries the numbers the model currently produces')
for label, needle in MUST:
    hit = needle in t
    print(f'  {"OK  " if hit else "MISS"}  {label:<32} {needle}')
    if not hit:
        fails.append(f'{label} ({needle}) missing from the study')

print('=' * 74)
print('the alternative construction is carried, not dropped')
for label, needle in ALTERNATIVE:
    hit = needle in t
    print(f'  {"OK  " if hit else "MISS"}  {label:<32} {needle}')
    if not hit:
        fails.append(f'{label} ({needle}) missing — the alternative leg must be published')

print('=' * 74)
print('no superseded framing survives in the text')
for label, needle in SUPERSEDED:
    n = len(re.findall(needle, t))
    print(f'  {"OK  " if n == 0 else "FAIL"}  {label:<32} {needle!r} appears {n}x')
    if n:
        fails.append(f'{label}: {needle!r} appears {n}x and should not')

print('=' * 74)
print('the bibliography agrees with the same file')
tb = text(BIB)
n_inputs = len(D['inputs'])
for label, needle in [('the input count', f'{n_inputs:,}'),
                      ('the adopted beta', f"{D['inputs']['beta']['value']:.3f}"),
                      ('the alternative beta',
                       f"{D['inputs']['beta_composite']['value']:.3f}"),
                      # the three judgements added in this edition, and the quotation the
                      # tanker rebuild rests on, must all reach the delivered register
                      ('the implied first-quarter spot',
                       f"{D['fleet']['spot_q1_26']['vlcc']:,.0f}"),
                      ('the published first-quarter blend',
                       f"{D['fleet']['blend_q1_26']['vlcc']:,.0f}"),
                      ('the blended-rate quotation', 'blended rate that we give there'),
                      ('the residual-income fade',
                       f"{D['book']['fade'] * 100:.0f}%"),
                      ('the minority deduction',
                       f"{D['dcf']['nci'] / 1000.0:,.1f}m"),
                      # the second round: the purchase as a primary source, the three new
                      # judgements, and the discrepancy row that records a claim this study
                      # made and later falsified
                      ('the August purchase as a source',
                       f"{IN['acq_2026_cost'] / 1000.0:,.0f}m"),
                      ('the crude carriers bought', f"{IN['acq_2026_vlcc']:,.0f} very large"),
                      ('the handysize scaling judgement',
                       f"{IN['handysize_relative']:.2f}"),
                      ('the receivable re-basing judgement',
                       f"{IN['dso_days']:,.1f}"),
                      ('the receivable basis it was re-based from',
                       f"{IN['dso_days_reported']:,.1f}"),
                      ('the falsified gross-up claim, recorded',
                       'so it cannot affect the valuation'),
                      ('the cost of debt, balance-weighted',
                       f"{W['kd_balance_weighted'] * 100:.2f}%")]:
    hit = needle in tb
    print(f'  {"OK  " if hit else "MISS"}  {label:<32} {needle}')
    if not hit:
        fails.append(f'{label} ({needle}) missing from the bibliography')

print('=' * 74)
if fails:
    print('DOCUMENT FRESHNESS FAILED:')
    for f in fails:
        print('  -', f)
    sys.exit(1)
print(f'DOCUMENTS ARE CURRENT — {len(MUST)} headline figures found, '
      f'{len(ALTERNATIVE)} alternative-construction figures carried, '
      f'{len(SUPERSEDED)} superseded phrasings absent')
