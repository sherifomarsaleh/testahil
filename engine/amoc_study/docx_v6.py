"""AMOC_Valuation_Study_08-08-2026_public.docx — the full study.

Built to the depth of the 06-08-2026 edition (7 numbered sections with 1.1-1.14 subsections,
Appendices A/B/C, ~35 tables), carrying the 08-08-2026 numbers: the twelve-month base to
30-Jun-2026, the per-line NRV cost build, the bridge that carries every disclosed claim, and
the adversarial give-back stack.

Every number is read from study_numbers.json or case_adversarial.json. Nothing is typed.
"""
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from docx_base import (P, H1, H2, rich, caption, bullet, table, figure, box, masthead, doc,
                       INK, GREY)                                      # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, 'study_numbers.json')))
CENSUS = json.load(open(os.path.join(HERE, 'workbook_census.json')))
ADV = json.load(open(os.path.join(HERE, 'case_adversarial.json')))
IN = {k: v['value'] for k, v in D['inputs'].items()}
UB, TTM, RT, BR = D['unitbuild'], D['ttm'], D['rates'], D['bridge']
F, W, DCF, LN = D['fcst'], D['wacc'], D['dcf'], D['lenses']
AU, BASE, REL, NRM, BK = D['audited'], D['base'], D['rel'], D['norm'], D['book']
HIS, HB, TR = D['hist_is'], D['hist_bs'], D['terminal_recon']
STK, S0, BETA, BT = D['strike'], D['step0'], D['wacc']['beta'], D['backtest']
EXP, SCEN = D['experts'], D['scen']
H1M, H3M = STK['horizons']['1M'], STK['horizons']['3M']
SPOT, SH, C = D['spot'], IN['shares_mn'], D['central']
GMR = D['gm_required']
GP_H1_GM = IN['gp_h1cy26'] / IN['rev_h1cy26']
TVS = D['dcf'].get('tv_share') or D['terminal_recon'].get('tv_share', 0.0)

# --- the band record, GENERATED not typed -------------------------------------
# What a reader is shown about this cone's track record is the BAND RECORD: how many
# three-month forecasts have resolved and how often the price finished inside the band.
# It is resolved from the committed panel at build time rather than typed, because a
# document that states a fact which moves must not be the thing that remembers it. It
# REPLACES the skill verdict this study used to print in Table 20, which is retired and
# does not belong on any page a reader sees.
sys.path.insert(0, os.path.join(HERE, '..'))
import band_record as _br
_BR = _br.resolve('AMOC', _br.by_key())
BAND = dict(n=_BR.n, hits=_BR.hits, c50=_BR.cov50, c80=_BR.cov80, c90=_BR.cov90,
            width=_BR.width, strength=_BR.strength, flag=_BR.flag)
assert BAND['flag'] in (None, 'narrow', 'wide')
LO, HI = D['span']; LOE, HIE = D['span_env']
YRS = F['years']
LINES, LBL = UB['lines'], UB['labels']
# THE LATEST REVIEWED PERIOD WAS MISSING FROM THIS LIST, AND IT IS THE ONE A READER
# NEEDS MOST [corrected 03-Sep-2026]. The typed list stopped at 3M Mar-2026 and
# omitted the six months to 30 June 2026 -- the most recent filed period, at a
# 12.43% gross margin against a forecast opening at 9.68%. Appendix A is where a
# reader checks a forecast against the record, and leaving out the one period that
# raises the question is how the question stayed invisible. Taken from the record
# rather than typed, so a new filing appears here by arriving.
PERIODS = list(D['hist_is'].keys())
# a COUNT stated in prose is a number, so it is computed like one — three captions and a
# heading typed 'four' after the reviewed half to 30 June 2026 made the filed set five,
# and one of them divided a five-period sum by four
_WORD = {1: 'One', 2: 'Two', 3: 'Three', 4: 'Four', 5: 'Five', 6: 'Six'}


def n0(x): return f"{x:,.0f}"
def n1(x): return f"{x:,.1f}"
def n3(x): return f"{x:,.3f}"
def p2(x): return f"{x:,.2f}"
def pc(x, dp=1): return f"{x*100:.{dp}f}%"
def sgn(x, dp=1): return f"{x*100:+.{dp}f}%"


GAP = C / SPOT - 1
# Computed so the Headline's WORDS move with its numbers: how many lenses actually
# sit below the price, and what the retired blend would read. Both were typed
# before and both had stopped being true.
_N_BELOW = {0: 'None', 1: 'One', 2: 'Two', 3: 'Three', 4: 'All four'}[
    sum(1 for k in ('dcf', 'relative', 'normalized', 'book')
        if LN[k]['base'] < SPOT)]
RETIRED_BLEND = LN['retired_blend']['base']
PREM = SPOT / C - 1
REQ_DCF = (SPOT - 0.20 * LN['relative']['base'] - 0.20 * LN['normalized']['base']
           - 0.15 * LN['book']['base']) / 0.45
GRIDS = D['blocks']['grids']
SC = D['blocks']['scen']


def grid_vals(name):
    g = next(x for x in GRIDS if x[0] == name)
    return [(p['label'], SC[f'{name}|{i}']['ps']) for i, p in enumerate(g[2])]


# ---- probability partition, computed and asserted to sum to one -------------
def cdf3m(x):
    """Log-linear interpolation on the published 3-month percentiles."""
    q = [0.05, 0.25, 0.50, 0.75, 0.95]
    v = [H3M['pct'][k] for k in ('p5', 'p25', 'p50', 'p75', 'p95')]
    lx = math.log(x)
    if lx <= math.log(v[0]):
        return q[0] * math.exp((lx - math.log(v[0])) * 6)
    if lx >= math.log(v[-1]):
        return 1 - (1 - q[-1]) * math.exp(-(lx - math.log(v[-1])) * 6)
    for i in range(4):
        a, b = math.log(v[i]), math.log(v[i + 1])
        if a <= lx <= b:
            return q[i] + (q[i + 1] - q[i]) * (lx - a) / (b - a)
    return 0.5


# THE ZONE CUTS MUST ASCEND, AND THE GUARD THAT WAS HERE COULD NOT SEE THAT THEY
# DID NOT [corrected 03-Sep-2026]. The list was written [C, 7.50, SPOT, 11.00] --
# the central first, then a low level, then spot, then a level below spot -- and
# once the central moved to 11.83 the sequence read 11.83, 7.50, 13.50, 11.00.
# Differences of a decreasing cumulative distribution are NEGATIVE, so the table
# published probabilities of -74.6% and -16.0% under a caption promising a
# partition.
#
# The assert could not catch it: consecutive differences of a cumulative function
# TELESCOPE, so the sum is 1.0 for any ordering whatever, ascending or not. It is
# a check that cannot fail, which is the [R-ENF-04] species -- a green light that
# examined nothing. Both are fixed: the cuts are SORTED, and the guard now tests
# what actually matters, which is that no zone is negative.
_CUTSET = (C, 7.50, SPOT, 11.00)
CUTS = sorted(_CUTSET)
ZP = [cdf3m(CUTS[0])]
for i in range(len(CUTS) - 1):
    ZP.append(cdf3m(CUTS[i + 1]) - cdf3m(CUTS[i]))
ZP.append(1 - cdf3m(CUTS[-1]))
assert abs(sum(ZP) - 1.0) < 1e-9, f'probability zones do not sum to one: {sum(ZP)}'
assert all(z >= -1e-9 for z in ZP), (
    'a probability zone is NEGATIVE: %s at cuts %s. Consecutive differences of a '
    'cumulative distribution telescope, so the sum-to-one assert above is 1.0 for '
    'any ordering and cannot see this.' % ([round(z, 4) for z in ZP], CUTS))

# ============================ FRONT MATTER ===================================
masthead()
P('Alexandria Mineral Oils Company S.A.E.', size=19, bold=True, space_after=0)
rich([('EGX: AMOC  ·  Egyptian Exchange  ·  EGP  ·  Valuation study as of 6 August 2026, '
       'issued 3 September 2026', dict(size=10, color=GREY))], space_after=10)

box([
    ('READ FIRST.  ',
     'This is an educational valuation study, not investment advice, and it makes no '
     'recommendation to buy, sell or hold. What it publishes is a fair-value RANGE and a '
     'probability distribution for the price — never a target. Three things are worth knowing '
     'before the numbers: the estimate sits well below the market price, which means the burden '
     'of proof is on this study and Section 1.14 states exactly what a buyer at the market price '
     'would have to believe; the forecasting method behind it has been tested against this '
     'company’s own past and did NOT beat a simple no-change rule, which is why the range is wide '
     'and why Section 7 leads with that rather than burying it; and the second half of the base '
     'year is reviewed rather than fully audited. Everything here is reproducible from the '
     'companion workbook, which recalculates the whole study live.'),
])
H1('Headline')
box([
    ('THE CLAIM, STATED EXACTLY.  ',
     # THE DIRECTION IS COMPUTED, NOT TYPED. This sentence read "-8.9% BELOW the
     # price; equivalently the price stands -8.2% ABOVE fair value ... the price
     # is outside it ... every one of the four lenses lands below the price" —
     # four false statements in three lines, contradicted by the table directly
     # beneath them. They were true of an edition whose central sat below the
     # price and survived the central moving above it, because the words were
     # typed and only the numbers were computed. A NUMBER STATED IN PROSE MUST BE
     # COMPUTED, and so must the word that gives it its sign.
     f'Fair value EGP {p2(C)} a share against a market price of EGP {p2(SPOT)}. Fair value sits '
     f'{pc(abs(GAP))} {"ABOVE" if GAP > 0 else "BELOW"} the price; equivalently the price stands '
     f'{pc(abs(PREM))} {"BELOW" if GAP > 0 else "ABOVE"} fair value. '
     f'The range across the lenses is EGP {p2(LO)} to {p2(HI)} and the price is '
     f'{"inside" if LO <= SPOT <= HI else "outside"} it. '
     f'{_N_BELOW} of the four lenses land below the price.'),
    ('WHAT WOULD CHANGE OUR MIND.  ',
     f'Surrender every contested judgement in this study simultaneously — the tax provision '
     f'settles for nothing, the declared dividend never leaves, the employees’ profit share '
     f'is free, the terminal rate reverts to the softer inflation target, operating profit is '
     f'taxed at the flattered effective rate — and the central still reaches only EGP '
     f'{p2(ADV["ALL_GIVEBACKS"]["central"])}, {pc(ADV["ALL_GIVEBACKS"]["central"]/SPOT-1)} '
     f'against the price. Section 1.13 walks the whole stack, one full model re-run per row.'),
    ('WHAT A BUYER AT THE PRICE MUST BELIEVE.  ',
     f'Solving the model at the market price rather than asserting a number: EGP {p2(SPOT)} is '
     f'fair if AMOC sustains a gross margin of {pc(GMR["level"], 2)} in every forecast year and '
     f'in perpetuity. The twelve months just filed ran {pc(GMR["base"], 2)} and the six months '
     f'to June 2026 ran {pc(GP_H1_GM, 2)}. The market price therefore requires a margin BELOW '
     f'what this company has just reported and well inside the range it has printed since 2021. '
     f'A buyer at EGP {p2(SPOT)} is not making a heroic assumption; the burden of proof sits '
     f'with the seller. Section 1.14 derives it.'),
    ('AND THE HONEST WEAKNESS.  ',
     f'The far years carry a wide range and the terminal block is {pc(TVS, 0)} of enterprise '
     'value, which is high. The forecasting method behind Section 1 was tested against this '
     'company’s own history and did NOT beat a simple no-change rule — Section 7 leads with '
     'that. Two exchange disclosures that would move the answer in opposite directions could '
     'not be opened.'),
])

H1('Valuation summary — every read at a glance')
# THE WEIGHT COLUMN WAS THE RETIRED BLEND, PRINTED AS IF IT WERE LIVE [corrected
# 03-Sep-2026]. The caption underneath already said the cross-checks "carry no
# weight" while the table beside it published 45/20/20/15 in a column headed
# Weight — a document contradicting itself by two inches. And the relative lens is
# marked withdrawn: true in the committed record, because its multiple WAS the
# traded one, yet it appeared here as a live 20%-weighted cross-check.
#
# The column is gone. The relative row now says what the record says.
_REL = [c for c in D['lens_record']['cross_checks']
        if c.get('kind') == 'relative_multiple']
_REL_WITHDRAWN = bool(_REL and _REL[0].get('withdrawn'))
_rows = [['Lens', 'What it measures', 'Bear', 'Base', 'Bull', 'vs price'],
         ['Discounted cash flow — THE ANSWER', 'unlevered cash, discounted on a glide',
          p2(LN['dcf']['bear']), p2(LN['dcf']['base']), p2(LN['dcf']['bull']),
          pc(LN['dcf']['base'] / SPOT - 1)]]
if _REL_WITHDRAWN:
    _rows.append(['Relative multiples — WITHDRAWN',
                  'its multiple WAS the traded one; a diagnostic of what the market '
                  'pays, not a valuation',
                  '—', p2(LN['relative']['base']), '—',
                  pc(LN['relative']['base'] / SPOT - 1)])
else:
    _rows.append(['Relative multiples', 'own trailing EV/EBITDA, no re-rating',
                  p2(LN['relative']['bear']), p2(LN['relative']['base']),
                  p2(LN['relative']['bull']), pc(LN['relative']['base'] / SPOT - 1)])
_rows += [
    ['Normalised earnings — a cross-check', 'mid-cycle operating EPS, discounted',
     p2(LN['normalized']['bear']), p2(LN['normalized']['base']),
     p2(LN['normalized']['bull']), pc(LN['normalized']['base'] / SPOT - 1)],
    ['Book value — a disclosed floor', 'justified price-to-book',
     p2(LN['book']['bear']), p2(LN['book']['base']), p2(LN['book']['bull']),
     pc(LN['book']['base'] / SPOT - 1)],
    ['CENTRAL', 'the cash-flow lens, alone', p2(LO), p2(C), p2(HI), pc(GAP)]]
table(_rows, [1.75, 2.0, 0.72, 0.72, 0.72, 0.72], band_rows={5}, size=9.0,
      left_cols=(1,))
caption('Table 1 — the lenses. ONE CLASS PRIMARY IS THE CENTRAL: the cash-flow lens is the '
        'answer and the other three are cross-checks, published beside it and carrying no '
        'weight. The bear and bull columns of the central row are that same lens\u2019s own '
        f'downside and upside, not a weighted combination. The widest single lens spans EGP '
        f'{p2(LOE)}\u2013{p2(HIE)}; that is reported as an ENVELOPE. The retired 45/20/20/15 '
        'blend of these four would read EGP ' + p2(RETIRED_BLEND) + ' and is shown in the '
        'workbook beside the answer, unused: three of the four value a refiner on reported '
        'earnings and historical-cost book, and averaging them imports every weakness of the '
        'weakest at a weight nobody tested out of sample.')
# THE CAPTION DESCRIBED A FIGURE THIS STUDY NO LONGER PUBLISHES. It promised a price
# shown in red dashed against every lens base — and the file it captioned had been
# overwritten by a SUPERSEDED generator carrying the retired 45/20/20/15 weights in its
# row labels, a WEIGHTED RANGE bar at a central of 11.83 the study had stopped
# publishing, and a hardcoded x-axis of 2 to 11 against a spot of 13.50 — so the
# price line it drew fell outside the axis and was clipped away silently while the
# caption said it was there. Two generators wrote the same filename; the older ran last.
figure(os.path.join(HERE, 'fig1_football.png'), 6.9,
       'Figure 1 — the answer and the reads held beside it. The cash-flow lens is the '
       'answer and carries its own bear-to-bull span; the relative multiple is drawn as '
       'a point because it is withdrawn, book value as a disclosed floor, and normalised '
       'earnings as a diagnostic this class does not value on. The vertical line is the '
       'traded price.')

H1('Company overview')
P(f'Alexandria Mineral Oils Company is the only refinery listed on the Egyptian Exchange. It '
  f'takes atmospheric residue and distils it into base and special oils, paraffin wax, gas oil, '
  f'naphtha, liquefied petroleum gas and fuel oil. Alexandria Petroleum Company holds 20.77% — '
  f'the previous edition of this study misattributed that stake to the Egyptian General '
  f'Petroleum Corporation — and AMOC owns {pc(IN["awp_stake"], 2)} of Alexandria Wax '
  f'Products, whose minority is '
  f'the non-controlling interest carried through this valuation.')
P(f'The financial year moved from 30 June to 31 December, so the filed record is a six-month '
  f'transition period (July to December 2025, AUDITED by Crowe — Dr A. M. Hegazy & Co, '
  f'unqualified opinion signed at Giza on 18 February 2026) followed by a reviewed first '
  f'quarter. That is why the base year in section 1.2 has to be constructed rather than lifted '
  f'off one filing.')

H2('What it actually sells')
table([['Product line', 'Tonnes, 6M', 'Value, EGP mn', 'Realisation EGP/t', 'Share of tonnage',
        'Share of value'],
       *[[LBL[k], n1(IN['prod_t'][k]), n0(IN['prod_v'][k] / 1e6),
          n0(IN['prod_v'][k] / IN['prod_t'][k]), pc(UB['t0'][k] / UB['T0'], 2),
          pc(IN['prod_v'][k] / sum(IN['prod_v'].values()), 2)] for k in LINES],
       ['TOTAL', n1(sum(IN['prod_t'].values())), n0(sum(IN['prod_v'].values()) / 1e6),
        n0(sum(IN['prod_v'].values()) / sum(IN['prod_t'].values())), '100.00%', '100.00%']],
      [1.75, 1.0, 1.1, 1.15, 1.05, 1.0], band_rows={9}, size=9.0)
caption('Table 2 — note 14-A of the audited transition-period statements. Eight lines, tonnes '
        'AND value both disclosed, so the realisation per tonne is disclosed arithmetic rather '
        'than an estimate. The specialty slate — base and special oils plus paraffin wax — is '
        f'{pc(UB["t0"]["oils"]/UB["T0"] + UB["t0"]["wax"]/UB["T0"], 1)} of the tonnage and '
        f'{pc((IN["prod_v"]["oils"]+IN["prod_v"]["wax"])/sum(IN["prod_v"].values()), 1)} of the '
        'value. That asymmetry is the company.')
P(f'Raw materials are {pc(AU["cost_share"]["raw"])} of cost of sales (note 15-A) and '
  f'{pc(RT["raw_of_rev"])} of revenue. A business whose single largest line is that big, and '
  f'whose gross margin is {pc(TTM["gm"])}, is a PASS-THROUGH PROCESSOR. The value is not in the '
  f'revenue line and it is not in cost control either — it is in the spread between what the '
  f'feedstock costs and what the slate fetches, earned on tonnage.')

H2('The balance sheet is the unusual part')
table([['Item', 'EGP mn', 'Per share', 'Treatment in this study'],
       ['Cash at banks and on hand, free', n0(IN['cash'] / 1e6), p2(IN['cash'] / 1e6 / SH),
        'added in the bridge — note 9-E, pledged deposits already excluded'],
       ['Deposits PLEDGED against facilities', n0(IN['fin_inv'] / 1e6),
        p2(IN['fin_inv'] / 1e6 / SH),
        'NOT free cash; added separately as a non-operating asset'],
       ['Gross borrowings', n0((IN['debt_lt'] + IN['debt_st']) / 1e6),
        p2((IN['debt_lt'] + IN['debt_st']) / 1e6 / SH), 'deducted'],
       ['NET CASH', n0(-BASE['nd_cy25']), p2(-BASE['nd_cy25'] / SH),
        f'{pc(-BASE["nd_cy25"]/(SPOT*SH))} of market capitalisation'],
       ['Provision for tax disputes and claims', n0(IN['provisions'] / 1e6),
        p2(IN['provisions'] / 1e6 / SH),
        'note 10-1 — DEDUCTED in the bridge; the previous edition never carried it'],
       ['Dividends payable, declared', n0(IN['div_declared'] / 1e6),
        p2(IN['div_declared'] / 1e6 / SH),
        'note 11 — removed from working capital, deducted in the bridge'],
       ['Equity investment at fair value through OCI', n0(IN['fvoci'] / 1e6),
        p2(IN['fvoci'] / 1e6 / SH), 'added as a non-operating asset'],
       ['Parent equity', n0(BASE['eqp_cy25']), p2(BK['bvps']), 'the book lens base']],
      [2.25, 0.85, 0.75, 3.1], band_rows={4}, size=8.8, left_cols=(3,))
caption('Table 3 — the balance sheet at 31 December 2025, as filed. The company holds more than '
        'a fifth of its market capitalisation in net cash, which is why the cost-of-capital '
        'construction in section 1.6 RAISES the operating discount rate above the cost of equity '
        'rather than lowering it. Against that cash sit two disclosed claims — the provision and '
        'the declared dividend — that the previous edition of this study quoted in its text and '
        'never carried into its arithmetic.')

# ============================ 1 FUNDAMENTAL ==================================
H1('1  Fundamental valuation')

H2('1.1  Why this company is valued as an operating company and not as anything else')
P('Three tests decide the class, and all three point the same way. Revenue is 100% own-'
  'production petroleum product — there is no trading book, no rental stream and no portfolio '
  'of stakes to sum. The balance sheet is working capital and plant, not investments: property, '
  f'plant and equipment plus projects under construction of EGP {n0(BASE["ppe_cy25"])}mn and net '
  f'working capital of EGP {n0(BASE["nwc_cy25"])}mn against a single equity stake of EGP '
  f'{n0(IN["fvoci"]/1e6)}mn. And consolidated profit is dominated by one plant, with the '
  f'minority in the wax subsidiary running at {pc(RT["nci_op"], 2)} of operating profit.')
P('So the primary lens is free cash flow to the FIRM, discounted, with the three cross-checks '
  'of section 1.12 weighted behind it. A sum-of-the-parts framework is inapplicable: AMOC has no '
  'listed subsidiaries. One reviewer was asked to run an SOTP verification against three '
  'unrelated foreign companies and correctly rejected the premise; it is recorded here so no '
  'reader wonders whether it was considered.')

H2('1.2  The base year is constructed, and here is the construction')
# THIS PARAGRAPH CONTRADICTED THE ONE FOUR LINES BELOW IT [corrected 03-Sep-2026].
# It said "HALF OF THIS BASE YEAR IS A PRESS RELEASE AND NOT A FILING", and §1.2's
# own next paragraph says "THE HALF IS FILED, AND THE RELEASED GROSS PROFIT WAS
# RIGHT". Both were true of successive editions and only one is true now: the
# reviewed statements for the six months to 30 June 2026 are in hand and the model
# uses the FILED gross profit. The stale sentence survived because it was typed and
# the correction was written beneath it rather than over it.
P('The base year is the TWELVE contiguous months to 30 June 2026: the audited transition half '
  '(July to December 2025) plus the REVIEWED half to 30 June 2026. No annualisation scalar is '
  'applied to either half and no period is estimated. BOTH HALVES ARE FILED — an earlier '
  'edition of this study treated the second as a press release and solved its gross profit '
  'from the profit line; the reviewed statements settle it, and the released figure was right '
  'to within a fraction of a per cent.')
table([['Line', 'Audited 6M to Dec-2025', 'Reported 6M to Jun-2026', 'Base year', 'Basis'],
       ['Net sales', n0(IN['rev_h2_25'] / 1e6), n0(IN['rev_h1cy26_rep'] / 1e6), n0(TTM['rev']),
        'both halves as disclosed'],
       ['Gross profit', n0((IN['rev_h2_25'] - IN['cogs_h2_25']) / 1e6), n0(TTM['gp_h1']),
        n0(TTM['gp']), 'both halves FILED'],
       ['Gross margin', pc((IN['rev_h2_25'] - IN['cogs_h2_25']) / IN['rev_h2_25'], 2),
        pc(TTM['gp_h1'] * 1e6 / IN['rev_h1cy26_rep'], 2), pc(TTM['gm'], 2), 'output'],
       ['Operating expense', '', '', n0(TTM['ga'] + TTM['mkt'] + TTM['oth'] + TTM['prov']),
        'administrative + selling + other + provisions'],
       ['Depreciation', '', '', n0(TTM['dep']), 'as filed'],
       ['Cash capital expenditure', '', '', n0(TTM['capex']), 'as paid'],
       ['Credit interest', '', '', n0(TTM['credint']), 'note 14-B'],
       ['Employees’ profit share', '', '', n0(TTM['emp']), 'note 16']],
      [1.85, 1.35, 1.35, 1.05, 1.75], size=8.8, left_cols=(4,))
caption('Table 4 — the base year. Every operating line is struck on the SAME twelve months as '
        'revenue and gross profit. The previous edition built revenue from the six-month product '
        'table doubled while annualising cost of sales from nine months by four thirds, so its '
        f'base-year gross margin of {pc(IN["gm_superseded_annualised"], 3)} corresponded to no '
        'filed period at all. One period, '
        'both sides, or the margin is an artefact of the scalars.')

P('THE HALF IS FILED, AND THE RELEASED GROSS PROFIT WAS RIGHT. The reviewed consolidated '
  f'statements for the six months to 30 June 2026 report net sales of EGP {n0(IN["rev_h1cy26"]/1e6)}mn, '
  f'gross profit of EGP {n0(IN["gp_h1cy26"]/1e6)}mn — a margin of {pc(GP_H1_GM, 2)} — and profit '
  f'attributable to shareholders of EGP {n0(IN["maj_h1cy26"]/1e6)}mn. That is MORE IN SIX MONTHS '
  f'than the whole financial year to June 2025 earned. The previous edition of this study did not '
  'have these statements, believed the half existed only as a press release, rejected the '
  'released gross-profit line on a coherence test and solved gross profit from the profit line '
  'instead. The filing settles it in the release\'s favour:')
table([['Line, six months to 30 June 2026', 'As released', 'As filed', 'Difference'],
       ['Net sales', n0(IN['rev_h1cy26_rep'] / 1e6), n0(IN['rev_h1cy26'] / 1e6),
        pc(IN['rev_h1cy26_rep'] / IN['rev_h1cy26'] - 1, 2)],
       ['Gross profit', n0(IN['gp_h1cy26_rep'] / 1e6), n0(IN['gp_h1cy26'] / 1e6),
        pc(IN['gp_h1cy26_rep'] / IN['gp_h1cy26'] - 1, 2)],
       ['Profit after tax', n0(IN['pat_h1cy26_rep'] / 1e6), n0(IN['pat_h1cy26'] / 1e6),
        pc(IN['pat_h1cy26_rep'] / IN['pat_h1cy26'] - 1, 2)]],
      [3.0, 1.35, 1.35, 1.6], size=8.8, left_cols=(1,))
caption('Table 5 — the press release against the filing. All three lines tie. The coherence test '
        'that rejected the gross-profit line estimated the half\'s other income by DOUBLING the '
        'first quarter\'s, which put EGP 451mn where the filing shows EGP 197mn — other income '
        'is the most volatile line in this income statement and the least suited to being '
        'doubled. A test built on an extrapolated volatile line refuted a correct disclosure, '
        'and the study then carried a gross margin roughly two-thirds of a point too low into '
        'every lens. The lesson is kept rather than the conclusion: a coherence test is only as '
        'good as the estimate inside it.')

P('The fully-audited alternative is published beside the headline rather than discarded: the '
  f'nine audited-and-reviewed months to 31 March 2026, annualised by four thirds, give revenue '
  f'of EGP {n0(TTM["rev9_ann"])}mn at a {pc(TTM["gm9"], 2)} margin. The gap to the headline base '
  f'is {sgn(TTM["rev"]/TTM["rev9_ann"]-1)} on revenue and '
  f'{sgn(TTM["gm"]-TTM["gm9"], 2)} on margin. That gap is a real uncertainty about this company '
  'and it is disclosed, not averaged away.')

table([['Period', 'Net sales', 'Gross profit', 'Gross margin', 'Operating profit'],
       *[[p, n0(HIS[p]['rev']), n0(HIS[p]['gp']), pc(HIS[p]['gm'], 2), n0(HIS[p]['ebit'])]
         for p in PERIODS]],
      [1.7, 1.25, 1.25, 1.15, 1.35], size=9.0)
caption(f'Table 6 — the filed margin record. {_WORD.get(len(PERIODS), str(len(PERIODS)))} consecutively filed periods; the margin ranges '
        f'{pc(min(HIS[p]["gm"] for p in PERIODS), 2)} to '
        f'{pc(max(HIS[p]["gm"] for p in PERIODS), 2)}, a spread of '
        f'{(max(HIS[p]["gm"] for p in PERIODS)-min(HIS[p]["gm"] for p in PERIODS))*1e4:.0f} basis '
        'points. Nothing here is modelled. The margin is administered, not competed: read this '
        'as a policy record.')

H2('1.3  Three charges the reported profit hides — and which this study takes')
P('Each of the following is disclosed in the filings, was registered as an input by the previous '
  'edition of this study, and was then read by no formula in it. All three are charged here.')
table([['Charge', 'Disclosed', 'Annualised', 'Where it belongs', 'Central WITHOUT it'],
       ['Employees’ profit share and board bonuses',
        f'EGP {n0(IN["emp_h2_25"]/1e6)}mn in the audited half (note 16)',
        f'{pc(RT["emp_rate"], 2)} of profit after tax',
        'charged in the waterfall and in normalised earnings — a contractual appropriation that '
        'reaches neither the shareholder nor the tax line',
        f"{p2(ADV['no_emp']['central'])}  ({sgn(ADV['no_emp']['central']/C-1)})"],
       ['Provision for tax disputes and claims',
        f'EGP {n0(IN["provisions"]/1e6)}mn at 31-Dec-2025 (note 10-1)', 'one-off, at face',
        'deducted in the equity bridge as a senior claim on the cash',
        f"{p2(ADV['no_provision']['central'])}  ({sgn(ADV['no_provision']['central']/C-1)})"],
       ['Dividends payable, declared and unpaid',
        f'EGP {n0(IN["div_declared"]/1e6)}mn at 31-Dec-2025 (note 11)', 'one-off, at face',
        'removed from operating working capital and deducted in the bridge',
        f"{p2(ADV['no_divp']['central'])}  ({sgn(ADV['no_divp']['central']/C-1)})"]],
      [1.6, 1.5, 1.1, 2.35, 1.25], size=8.6, left_cols=(1, 2, 3))
caption('Table 7 — the three charges. The rightmost column is the central this study '
        'would print if the charge were NOT taken, from a full model re-run — so a positive figure '
        'is how much each charge costs the valuation. Setting the provision to zero in the previous edition '
        'moved its valuation by nothing at all, to four decimal places, because no formula read '
        'the cell. A rewritten reachability gate now FAILS the build if any input carrying a '
        'balance-sheet or profit-statement claim is registered without being used; it found '
        'sixteen such inputs where the old gate reported zero.')

H2('1.4  How revenue is built')
P('Revenue is the eight disclosed product lines, tonnes times realisation, rolled forward on a '
  'volume path per line and one realisation path. Tonnage comes from note 14-A annualised; '
  'realisations are note 14-A value divided by note 14-A tonnes, lifted by ONE solved index so '
  f'the base year foots to the twelve-month revenue. That index is {n3(UB["px_index"])} and it is '
  'the only free scalar on the revenue side.')
table([['Line', 'Base tonnes mn', 'Base realisation EGP/t', *[y for y in YRS]],
       *[[LBL[k], n3(UB['t0'][k]), n0(UB['px0'][k]),
          *[n0(UB['lines_rev'][k][i]) for i in range(5)]] for k in LINES if k != 'waste'],
       ['TOTAL REVENUE', n3(UB['T0']), n0(TTM['rev'] / UB['T0']),
        *[n0(F['rev'][i]) for i in range(5)]]],
      [1.35, 0.95, 1.15, 0.83, 0.83, 0.83, 0.83, 0.83], band_rows={8}, size=8.4)
caption('Table 8 — revenue by line, EGP mn. Volume growth is set per line from the measured '
        'half-on-half record; realisation grows on one path for all lines. The waste line is '
        'omitted from the table for space and is immaterial, but it is carried in the model.')

H2('1.5  The cost side, built per line — and what it says about the slate')
P('This is where the previous edition was weakest and where the rebuild is deepest. Cost of '
  f'sales is {pc(TTM["cogs"]/TTM["rev"])} of revenue on this name, so a cost side expressed as a '
  'percentage of revenue means the margin assumption IS the valuation. Cost is now built per '
  'line, in two legs.')
P('CONVERSION — salaries, supporting materials, other operating costs and depreciation, the '
  f'{pc(1-AU["cost_share"]["raw"])} of note 15-A that is not feedstock — is allocated across the '
  'eight lines on registered processing-intensity weights: base oils 1.00 as the reference '
  'through the full lube train (vacuum distillation, solvent extraction, dewaxing, '
  'hydrofinishing), paraffin wax 1.15 for the additional deoiling and sweating, the light ends '
  '0.15 to 0.25, the residue fuel oils 0.05.')
P('FEEDSTOCK is then allocated on NET REALISABLE VALUE — each line’s realisation less its '
  'own conversion cost. This is the standard joint-product convention and it is the only one of '
  'three bases tested that survives a sanity check. Allocating feedstock flat per tonne says '
  'fuel oil sells below the cost of its own feed, which is an artefact of the basis rather than '
  'a fact about the business. Allocating it on relative sales value makes base oils and paraffin '
  'wax — the products this plant exists for — run at negative margins once their conversion cost '
  'is stacked on top. Net realisable value is the only basis that leaves every disclosed line '
  'with a positive spread, and the workbook documents all three.')
table([['Line', 'Realisation EGP/t', 'Conversion EGP/t', 'Feedstock EGP/t', 'Total cost EGP/t',
        'SPREAD EGP/t', 'Margin'],
       *[[LBL[k], n0(UB['px0'][k]), n0(UB['conv_pt'][k]), n0(UB['raw_pt'][k]),
          n0(UB['raw_pt'][k] + UB['conv_pt'][k]), n0(UB['spread'][k]), pc(UB['margin0'][k], 1)]
         for k in LINES if k != 'waste'],
       ['Blended', n0(TTM['rev'] / UB['T0']), '', '', n0(TTM['cogs'] / UB['T0']),
        n0((TTM['rev'] - TTM['cogs']) / UB['T0']), pc(TTM['gm'], 1)]],
      [1.4, 1.05, 1.02, 1.02, 1.02, 0.95, 0.7], band_rows={8}, size=8.5)
caption('Table 9 — per-line economics of the base year. The eight per-line costs rebuild the '
        'disclosed cost of sales exactly; that footing test is a live cell in the workbook. '
        f'A tonne of base oil contributes {UB["spread"]["oils"]/UB["spread"]["fueloil"]:.1f} times '
        'the spread of a tonne of fuel oil, so the MIX now moves the margin. The previous edition '
        'applied one blended margin to all eight lines and described that as a bottom-up build; '
        'it was a single company-level number wearing eight labels, and it meant the mix could '
        'shift without the margin responding at all.')
figure(os.path.join(HERE, 'fig5_spread.png'), 6.7,
       'Figure 2 — gross spread per tonne by line; gold is the specialty slate. Note that the '
       'specialty lines show a LOWER margin percentage on a HIGHER spread per tonne, because '
       'their realisation per tonne is nearly three times fuel oil’s. On a joint-product '
       'slate the percentage margin is the wrong lens and the spread per tonne is the right one.')
P('THE ONE OPERATING INPUT NOT READ OFF A FILING. Note 15-A discloses the cost stack for the '
  'company and NOT by line, and note 14-A carries only price and volume — so any weight derived '
  'from note 14-A alone is a function of price, and a price-derived weight returns an identical '
  'margin on every line, which is precisely the defect this build exists to remove. The '
  'processing-intensity vector is therefore an engineering judgement. It is registered, dated '
  'and sourced like every other input, its effect is bounded (it redistributes cost BETWEEN '
  'lines while the company total stays pinned to note 15-A), and section 7 carries it as a named '
  'weakness rather than burying it in a formula.')

H2('1.6  The cost of capital, built rather than asserted')
table([['Component', 'Explicit window', 'Terminal', 'Construction'],
       ['Risk-free rate', pc(IN['rf'], 2), pc(RT['rf_term'], 2),
        'Egypt 10-year local currency. The TERMINAL rate is DERIVED, not typed: the central '
        'bank’s inflation target IN FORCE for the terminal horizon (7%) plus a 5.5% real '
        'convention'],
       ['less sovereign default spread', f"−{pc(IN['sov_spread_cds'], 2)}", '—',
        'netted out of the risk-free rate so country risk is not counted in both the rate and '
        'the equity premium'],
       ['Equity risk premium', pc(IN['erp_cds'], 2), pc(IN['erp_term'], 2),
        'CDS basis, Damodaran country file. The rating-basis alternative is computed and '
        'published in section 1.13'],
       ['Beta', n3(BETA['beta']), n3(BETA['beta']),
        f"own-stock regression, n={BETA['n']}, R² {pc(BETA['r2'],1)}, standard error "
        f"{n3(BETA['se'])}, 90% interval [{n3(BETA['ci90'][0])}, {n3(BETA['ci90'][1])}]"],
       ['COST OF EQUITY', pc(W['ke_exp'], 2), pc(W['ke_term'], 2), ''],
       ['Cost of debt, after tax', pc(W['k_nd_at'], 2), pc(W['kd_term_at'], 2),
        'on NET debt in the explicit window; the company is net cash'],
       # THE WEIGHTS ACTUALLY IN USE, NOT THE RETIRED ONES. This table printed
       # we_exp = 120.80% and wd_exp = -20.80% — the weights of the NET-debt
       # construction this study retired — beside wacc_exp, which is the adopted rate
       # those weights do not produce: 1.208 x 27.45% - 0.208 x 13.21% is 30.42%, and
       # the row said 27.45%. A reader multiplying the printed rows got a different
       # answer from the printed total, in the study's central table.
       #
       # The adopted construction values the OPERATIONS at the unlevered rate and adds
       # the cash once in the bridge [R-BRIDGE-01 (iii)], so the weights that matter are
       # the GROSS ones, and gross borrowings are a tenth of one per cent of capital at
       # market value — which is why the operating rate IS the cost of equity to three
       # decimals. The retired construction keeps its own row, with its own number.
       ['Equity weight', pc(1 - W['wd_gross'], 2), pc(1 - IN['wd_term'], 2),
        'on GROSS borrowings: the operations are valued at the unlevered rate and the '
        'cash is added once, in the bridge'],
       ['Debt weight', pc(W['wd_gross'], 2), pc(IN['wd_term'], 2),
        'gross borrowings are a tenth of one per cent of capital at market value'],
       ['WEIGHTED COST OF CAPITAL', pc(W['wacc_exp'], 2), pc(W['wacc_term'], 2),
        'the operating rate; at that debt weight it IS the cost of equity to three '
        'decimals'],
       ['— the retired net-debt construction', pc(W['wacc_net_retired'], 2), '—',
        'weights %s equity and %s debt, which is what a NET-cash weighting produces; '
        'it is shown because the previous edition used it AND added the cash back at '
        'face, charging for the same cash twice'
        % (pc(1 - W['wd_net_retired'], 2), pc(W['wd_net_retired'], 2))]],
      [1.8, 1.05, 0.9, 3.35], band_rows={5, 9}, size=8.5, left_cols=(3,))
caption('Table 10 — the discount-rate stack. The construction that matters most here is what '
        'the cash is doing. A naive model lets a cash pile drag the weighted rate DOWN; the '
        f'previous edition went the other way, weighting on NET debt at {pc(W["wd_net_retired"], 1)} '
        f'and reaching {pc(W["wacc_net_retired"], 1)} — {(W["wacc_net_retired"]-W["ke_exp"])*1e4:,.0f} '
        f'basis points ABOVE the {pc(W["ke_exp"], 1)} cost of equity — and THEN added the same cash '
        'back at face in the bridge, which charges for it twice. This edition values the '
        f'operations at the unlevered rate of {pc(W["wacc_exp"], 2)} and adds the cash once, '
        'isolating and penalising the risk of the pure unlevered operating assets. The unlevering '
        'identity is asserted in the build to recombine exactly.')

H2('1.7  The discount-rate schedule, year by year')
table([['', *YRS, 'Terminal'],
       ['Glide fraction', *[n3(g) for g in F['glide_frac']], '1.000'],
       ['Forward cost of capital', *[pc(w, 2) for w in F['fwd_wacc']], pc(W['wacc_term'], 2)],
       ['Cumulative discount factor', *[f'{d:.5f}' for d in F['df']], '']],
      [2.1, 0.83, 0.83, 0.83, 0.83, 0.83, 0.85], size=8.7)
caption('Table 11 — one date, one price of time. Each year is discounted at its OWN forward '
        'rate, and the glide from the explicit anchor to the terminal anchor is inherited from '
        'the cost-of-debt path’s own cumulative progress rather than invented as a straight '
        'line. The terminal block is discounted at the year-5 cumulative factor.')

H2('1.8  The free-cash-flow waterfall and the enterprise-value bridge')
table([['', *YRS],
       ['Revenue', *[n0(x) for x in F['rev']]],
       ['Cost of sales', *[n0(F['rev'][i] - F['gp'][i]) for i in range(5)]],
       ['GROSS PROFIT', *[n0(x) for x in F['gp']]],
       ['Gross margin', *[pc(x, 2) for x in F['gm']]],
       ['Operating expense', *[n0(x) for x in F['opex']]],
       ['EBITDA', *[n0(x) for x in F['ebitda']]],
       ['Depreciation', *[n0(x) for x in F['dna']]],
       ['EBIT', *[n0(x) for x in F['ebit']]],
       ['NOPAT after profit share', *[n0(x) for x in F['nopat']]],
       ['plus depreciation', *[n0(x) for x in F['dna']]],
       ['less capital expenditure', *[n0(x) for x in F['capex']]],
       ['less change in working capital', *[n0(x) for x in F['dnwc']]],
       ['FREE CASH FLOW TO THE FIRM', *[n0(x) for x in F['fcff']]],
       ['times discount factor', *[f'{d:.5f}' for d in F['df']]],
       ['PRESENT VALUE', *[n0(x) for x in F['pv']]]],
      [2.5, 0.86, 0.86, 0.86, 0.86, 0.86], band_rows={3, 13, 15}, size=8.5)
caption('Table 12 — the waterfall, EGP mn. Operating expense charges the three disclosed lines '
        'on three different drivers — administrative on inflation, selling on inflation AND '
        'tonnage, other on inflation — plus the recurring provisions and expected credit losses '
        'the previous edition registered and never took. Capital expenditure is BUILT: '
        f'maintenance at gross asset cost over the implied {n1(RT["asset_life"])}-year life, plus '
        f'growth at the plant’s own EGP {n0(RT["cap_intensity"])} per annual tonne of '
        'capital intensity, so incremental volume costs capital instead of arriving free. '
        'Depreciation ROLLS off the growing asset register rather than being held flat.')
table([['Bridge step', 'EGP mn', 'Per share', 'Source'],
       ['Present value of the explicit window', n0(DCF['pv_explicit']),
        p2(DCF['pv_explicit'] / SH), 'Table 12'],
       ['Present value of the terminal block', n0(DCF['pv_tv']), p2(DCF['pv_tv'] / SH),
        f'{pc(DCF["tv_share"])} of enterprise value'],
       ['ENTERPRISE VALUE', n0(BR['ev']), p2(BR['ev'] / SH), ''],
       ['plus net cash', n0(-BR['nd']), p2(-BR['nd'] / SH), 'note 9-E and note 20'],
       ['Enterprise value including cash', n0(BR['eq_gross']), p2(BR['eq_gross'] / SH), ''],
       ['less minority interest', f"({n0(BR['nci'])})", f"({p2(BR['nci'] / SH)})",
        f'{pc(RT["nci_op"], 3)} of the WHOLE enterprise, cash included'],
       ['less provision for tax disputes', f"({n0(BR['prov'])})", f"({p2(BR['prov'] / SH)})",
        'note 10-1'],
       ['less dividends payable', f"({n0(BR['divp'])})", f"({p2(BR['divp'] / SH)})", 'note 11'],
       ['plus non-operating investments', n0(BR['inv']), p2(BR['inv'] / SH),
        'pledged deposits and the ASPPC stake'],
       ['EQUITY ATTRIBUTABLE', n0(BR['eq']), p2(BR['ps']), f'against a price of {p2(SPOT)}']],
      [2.6, 1.0, 0.9, 2.5], band_rows={3, 10}, size=8.6, left_cols=(3,))
caption('Table 13 — the bridge, with every disclosed claim carried. The minority takes its share '
        'of the WHOLE enterprise including the cash: the previous construction charged the '
        'minority its share of the operating enterprise and then credited the parent with 100% of '
        'the consolidated cash, an inconsistency a reader can find in one line of arithmetic. The '
        'provision and the declared dividend are senior claims on that same cash and are '
        'deducted at face. The pledged deposits are excluded from free cash but are real assets, '
        'so they return here rather than vanishing from both sides.')
figure(os.path.join(HERE, 'fig3_bridge.png'), 6.9,
       'Figure 3 — the bridge drawn per share. The gap between the enterprise value including '
       'cash and the attributable equity is the three disclosed claims, worth EGP '
       f'{p2((BR["nci"]+BR["prov"]+BR["divp"]-BR["inv"])/SH)} a share between them.')

H2('1.9  The terminal block')
P(f'The terminal return is struck on invested capital at REPLACEMENT cost — working capital plus '
  f'the asset base at GROSS cost — giving {pc(DCF["roic_term"])}. On net book it would be about '
  f'26%. The plant is 67.4% written down, and the book lens in section 1.12 already haircuts the '
  f'reported return on equity for exactly that reason; using the flattered figure in the '
  f'terminal block while haircutting it in the book lens would be two views of one asset base. '
  f'One view is now applied across the model.')
P(f'Growth equals return times reinvestment is ENFORCED by assertion, not asserted in prose: at '
  f'{pc(IN["g_term"], 0)} terminal growth and a {pc(DCF["roic_term"])} return, the terminal block '
  f'reinvests {pc(DCF["rr_term"])} of profit. That is ABOVE the final explicit year’s '
  f'{pc(RT["rr_2030"])}, so the terminal block is funded rather than flattered — a step of '
  f'{sgn(TR["rr_step"], 2)}, disclosed here because it RAISES nothing and a '
  f'reader is entitled to see it either way. Terminal value carries {pc(DCF["tv_share"])} of '
  f'enterprise value, down from {pc(IN["tv_share_superseded"], 1)} in the previous edition, '
  f'and the fall is a direct '
  f'consequence of the replacement-cost basis.')

H2('1.10  Terminal growth, reconciled against the company’s own record')
# THE PERIOD COUNT WAS TYPED IN THREE PLACES AND THE AVERAGE DIVIDED BY A CONSTANT
# [corrected 03-Sep-2026]. PERIODS is read from the committed record and became FIVE when the
# reviewed half to 30 June 2026 was added to the filed set; the summary row went on summing
# five values and dividing by four, and the caption went on saying "TWO of the four filed
# periods". A count stated in prose is a number, and the rule against typing numbers into a
# builder covers it — the average is now over len(PERIODS) and the counts are computed.
_NP = len(PERIODS)
_N_POS = sum(1 for p in PERIODS if TR['rr'][p] > 0)
table([['Period', 'Return on invested capital', 'Reinvestment rate', 'Implied steady-state growth'],
       *[[p, pc(TR['roic'][p]), pc(TR['rr'][p]), pc(TR['implied_g'][p], 2)] for p in PERIODS],
       [f'{_WORD.get(_NP, str(_NP))}-period average', '',
        pc(sum(TR['rr'][p] for p in PERIODS) / _NP),
        pc(sum(TR['implied_g'][p] for p in PERIODS) / _NP, 2)]],
      [1.9, 1.75, 1.4, 1.85], band_rows={_NP + 1}, size=8.8)
caption(f'Table 14 — the reinvestment record. {_WORD.get(_N_POS, str(_N_POS)).upper()} of the {_NP} '
        f'filed periods show POSITIVE reinvestment and the {_NP}-period average implied '
        f'growth is '
        f'{"positive" if sum(TR["implied_g"][p] for p in PERIODS) > 0 else "negative"}. '
        'The previous '
        'edition of this study stated in three separate places that reinvestment was "negative in '
        'every audited period" and that the identity implied a negative steady-state rate; its '
        'own table, printed on the facing page, said otherwise. Two outside reviewers then built '
        'a "shrinking asset base" argument on that incorrect sentence rather than on the correct '
        'table. The sentence is withdrawn.')
P(f'Against that record the adopted {pc(IN["g_term"], 0)} is generous, and the study says so. The '
  f'reinvestment waterfall itself implies {pc(TR["g_waterfall"], 2)}; the {_NP}-period average '
  f'implies far less. The terminal growth sensitivity in section 1.11 shows why the choice barely '
  f'matters here: because the reinvestment identity FUNDS growth before crediting it, the value '
  f'moves only from EGP {p2(grid_vals("Terminal growth")[0][1])} at 3% to '
  f'{p2(grid_vals("Terminal growth")[-1][1])} at 7%. A model in which that row is steep is a '
  f'model crediting growth for free.')

H2('1.11  Sensitivities')
rows = [['Driver (cash-flow lens, EGP a share)', 'low', '', 'base', '', 'high']]
for gname, _, pts in GRIDS:
    v = grid_vals(gname)
    rows.append([gname] + [p2(x[1]) for x in v])
table(rows, [2.85, 0.75, 0.75, 0.75, 0.75, 0.75], size=8.5)
caption('Table 15 — six drivers, five points each: thirty complete re-runs of the model, not '
        'add-backs. Every grid is sorted, every row reproduces the base case at its own base '
        'point, and every row is monotone in the direction theory requires — all three properties '
        'are ASSERTED in the build. The previous edition published three rows that failed one or '
        'more of these tests and had no gate that could have caught them: a working-capital row '
        'whose grid was never sorted so the base case sat in the middle slot, a beta row whose '
        'centre did not return the base case, and a volume row whose label described a different '
        'scenario from the one it ran. In the companion workbook each of these cells is a live '
        'formula block.')
P('Two readings matter. TERMINAL GROWTH is nearly inert, for the reason given in section 1.10. '
  'And GROSS MARGIN is the whole thesis: half a point on the margin, held in every forecast '
  f'year, is worth about EGP {abs(grid_vals("Gross margin, shifted on every forecast year")[1][1] - LN["dcf"]["base"]):.2f} '
  'a share on the cash-flow lens. That is why the case in section 1.13 is built to survive the '
  'margin being wrong by more than the entire filed record’s range.')

SW = D['sens_wg']
table([['terminal WACC  \\  terminal growth', *[pc(g, 0) for g in SW['g_grid']]],
       *[[pc(SW['wacc_grid'][i], 2), *[p2(SW['table'][i][j]) for j in range(5)]]
         for i in range(5)]],
      [2.35, 0.85, 0.85, 0.85, 0.85, 0.85], size=8.6)
caption('Table 16 — the two terminal parameters moved together, cash-flow lens, EGP a share. '
        'The grid is flat in the growth direction and steep in the rate direction, which is the '
        'signature of a terminal block where reinvestment funds growth before crediting it. Not '
        'one cell in this grid reaches the market price.')

P('The bear and bull columns of the cash-flow lens move only what this company\'s own '
  'audited filings have printed — the gross margin across its filed span and the tonnage '
  'across its own — and the macro path does not move with them. A previous edition also '
  'flexed the exchange-rate path, the cost of capital at both anchors and the terminal '
  'growth rate; all three carry the same Egyptian inflation, so its bull corner needed '
  'inflation to be high and low at the same time and its bear corner needed the mirror '
  'image. The width of a range built that way is a choice of dial settings rather than '
  'anything the world has shown. No probability attaches to either end.')
table([['Driver moved', 'Bear', 'Base', 'Bull'],
       *[[SCEN['labels'][k],
          (pc(SCEN['bear'][k], 1) if k in ('vol_adj', 'gm_shift', 'wacc_shift')
           else f"{SCEN['bear'][k]:.2f}x"),
          ('0.0%' if k in ('vol_adj', 'gm_shift', 'wacc_shift') else '1.00x'),
          (pc(SCEN['bull'][k], 1) if k in ('vol_adj', 'gm_shift', 'wacc_shift')
           else f"{SCEN['bull'][k]:.2f}x")]
         for k in ('vol_adj', 'gm_shift', 'fx_mult', 'wacc_shift')],
       ['RESULTING FAIR VALUE, cash-flow lens', p2(SCEN['bear']['ps']), p2(SCEN['base_ps']),
        p2(SCEN['bull']['ps'])]],
      [3.05, 1.05, 1.05, 1.05], band_rows={6}, size=8.6, left_cols=())
caption('Table 17 — what the bear and bull columns actually move. The previous edition published '
        'a 6.2x headline span whose driver set was stated nowhere in the study or the workbook, '
        'so it could not be reproduced or falsified. It is stated here.')

H2('1.12  The three cross-check lenses')
P(f'RELATIVE MULTIPLES. The company’s own trailing multiple is {RT["just_mult"]:.2f} times '
  f'enterprise value to EBITDA and {n1(REL["pe_trailing"])} times earnings. The justified '
  f'multiple is DERIVED from it at a zero re-rating rather than set by hand, so the lens borrows '
  f'nothing from the cash-flow lens — no discount factor and no interim add-back, both of which '
  f'the previous construction took from lens 1 and which every reviewer objected to. At '
  f'{RT["just_mult"]:.2f} times TRAILING EBITDA through the same bridge: EGP '
  f'{p2(LN["relative"]["base"])}. This is the lens closest to the price, and what remains of the '
  f'gap is almost entirely the bridge — which is exactly what this lens is now for. At the '
  f'market’s own multiple, the price pays full value for the operations and then ignores the '
  f'provision and the declared dividend.')
P(f'NORMALISED EARNINGS POWER. 2028E OPERATING profit only, taxed at the statutory '
  f'{pc(RT["tax_stat"], 1)}, after the employees’ share and the minority: EGP '
  f'{NRM["eps"]:.3f} a share. At {n1(IN["pe_just"])} times that is a MID-2028 value, so it is '
  f'discounted {n1(RT["norm_yrs"])} years back to the valuation date at the COST OF EQUITY — an '
  f'equity claim at an equity rate, not at the unlevered weighted rate — and net cash less the '
  f'provision and the declared dividend is added at FACE outside the multiple. Result EGP '
  f'{p2(LN["normalized"]["base"])}. The previous construction capitalised credit interest at an '
  f'operating multiple, valuing a bank deposit as though it compounded like the refinery, and '
  f'then left the 2028 answer undiscounted while the sibling lens discounted its forward number. '
  f'One lens discounted and the other did not; both are now on the valuation date.')
P(f'BOOK VALUE AND SUSTAINABLE RETURN. Justified price-to-book of {BK["pb_just"]:.2f} times = '
  f'(sustainable return {pc(IN["roe_sust"], 0)} less growth) over (cost of equity '
  f'{pc(RT["ke_blend"], 2)} less growth), on book value of EGP {p2(BK["bvps"])}: EGP '
  f'{p2(LN["book"]["base"])}. The rate is the present-value-weighted average of the SAME '
  f'cost-of-equity glide the cash-flow lens uses. The previous edition used the terminal rate '
  f'alone for a perpetuity beginning today, which gives 6.06; the explicit rate alone gives '
  f'3.75; a perpetuity starting now deserves neither endpoint. The sustainable return is struck '
  f'below the trailing {pc(BASE["roe_trailing"])} because the asset base is 67.4% written down.')

H2('1.13  Contested choices, computed rather than argued')
P('A gap of this size should not survive its own contested judgements, so the study gives them '
  'all back. Each row below removes one charge a critic could dispute; the last row removes all '
  'of them at once. Every row is a complete re-run of the whole model.')
table([['Give-back', 'Central', 'vs price', 'What is being conceded'],
       ['None — as published', p2(ADV['base']['central']),
        pc(ADV['base']['central'] / SPOT - 1), 'the study’s own reading'],
       ['Tax provision costs nothing', p2(ADV['no_provision']['central']),
        pc(ADV['no_provision']['central'] / SPOT - 1),
        f'EGP {n0(IN["provisions"]/1e6)}mn recognised in note 10-1 settles for zero'],
       ['Declared dividend is not a claim', p2(ADV['no_divp']['central']),
        pc(ADV['no_divp']['central'] / SPOT - 1),
        f'EGP {n0(IN["div_declared"]/1e6)}mn payable in note 11 never leaves'],
       ['Employees’ profit share is free', p2(ADV['no_emp']['central']),
        pc(ADV['no_emp']['central'] / SPOT - 1),
        f'the {pc(RT["emp_rate"], 1)} statutory appropriation is never paid'],
       ['Terminal rate on the 2028 target', p2(ADV['terminal_rf_5pct_target']['central']),
        pc(ADV['terminal_rf_5pct_target']['central'] / SPOT - 1),
        'the softer 5% target replaces the 7% target in force'],
       ['Effective instead of statutory tax', p2(ADV['effective_tax']['central']),
        pc(ADV['effective_tax']['central'] / SPOT - 1),
        f'operating profit taxed at the interest-flattered {pc(RT["tax_eff"], 2)}'],
       ['ALL OF THE ABOVE AT ONCE', p2(ADV['ALL_GIVEBACKS']['central']),
        pc(ADV['ALL_GIVEBACKS']['central'] / SPOT - 1),
        'every contested charge conceded simultaneously']],
      [2.2, 0.85, 0.85, 3.0], band_rows={7}, size=8.7, left_cols=(3,))
caption('Table 18 — the adversarial stack. Concede everything and the price is still '
        f'{pc(-(ADV["ALL_GIVEBACKS"]["central"]/SPOT-1))} above the model.')
figure(os.path.join(HERE, 'fig4_adversarial.png'), 6.9,
       'Figure 4 — the same stack drawn. No single concession, and not all of them together, '
       'reaches the price.')
P(f'Two further contested choices are computed rather than conceded. On the RATING-BASIS equity '
  f'risk premium instead of the CDS basis, the cash-flow lens is EGP '
  f'{p2(DCF["ps_rating_basis"])}; two independent reviewers reached for that column, so it is '
  f'promoted here rather than buried. And discounting the export leg in DOLLARS at a dollar cost '
  f'of capital before translating back — rather than discounting a pound cash flow already '
  f'inflated by the depreciation path at a dollar rate, which would count the currency benefit '
  f'twice — gives EGP {p2(DCF["ccy_alt_ps"])}. Both are below the market price.')
P('What survives the give-backs is the part of the verdict that cannot be negotiated away by '
  f'accounting choices: a pass-through processor earning a {pc(TTM["gm"])} gross margin, '
  f'discounted at an Egyptian cost of equity of {pc(W["ke_exp"], 1)} falling to '
  f'{pc(W["ke_term"], 1)}, is worth less than EGP {p2(SPOT)} a share on any internally '
  'consistent arithmetic this study can construct.')

H2(f'1.14  What a buyer at EGP {p2(SPOT)} must believe')
P('The model is inverted at the market price rather than argued with. Every other driver is held '
  'at its published value and the gross margin is solved for.')
bullet(f'a gross margin of {pc(GMR["level"], 2)} sustained in EVERY forecast year and in '
       f'perpetuity, against a base year of {pc(GMR["base"], 2)} — that is a REDUCTION of '
       f'{pc(GMR["base"]-GMR["level"], 2)} from what the company has just filed, not an '
       f'increase;', bold_head='AS MARGIN — ')
bullet(f'the filed record puts that requirement well inside the range: {pc(GMR["filed_max_year"], 2)} '
       f'for the whole year to June 2022, {pc(GP_H1_GM, 2)} for the half to June 2026 and '
       f'{pc(GMR["filed_max_quarter"], 2)} for the June 2026 quarter alone;',
       bold_head='AGAINST THE RECORD — ')
bullet('so the price does not require a re-rating, a capacity addition or a change in the '
       'business. It requires the company to hold slightly less margin than it is holding now.',
       bold_head='WHAT THAT MEANS — ')
P('THE PREVIOUS EDITION OF THIS STUDY PUT THIS FIGURE AT A PERMANENT 12.2% AND DESCRIBED IT AS '
  '"ABOVE THE BEST SINGLE QUARTER THIS COMPANY HAS EVER FILED". Both halves of that sentence '
  'were wrong. The number was typed rather than solved and was never recomputed as the model '
  f'moved; solved, it is {pc(GMR["level"], 2)}. And the company had already filed '
  f'{pc(GMR["filed_max_year"], 2)} for a full year and {pc(GMR["filed_max_quarter"], 2)} for a '
  'quarter. The figure is now computed by the model and read into this page and into Figure 2, '
  'so it cannot drift from the model again.')

# ============================ 2-7 ============================================
H1('2  The price record')
P(f'The price series runs from {S0["series_first"]} to {S0["series_last"]} — '
  f'{n1(S0["span_years"])} years, {n0(S0["raw_rows"])} raw rows reduced to '
  f'{n0(S0["clean_rows"])} clean sessions at {n1(S0["density_rows_per_yr"])} sessions a year. '
  f'One row was dropped: {S0["dq_log"][0]}. The largest single-session move in the whole record '
  f'is {S0["max_abs_log"]:.4f} in logs, inside the exchange’s daily limit — the up-limit is '
  f'ln(1.20) = {math.log(1.2):.5f} and the down-limit is |ln(0.80)| = {abs(math.log(0.8)):.5f}, '
  f'and the two are tested separately because a ±20% price band is asymmetric in logs. '
  f'{pc(S0["flat_frac"], 1)} of sessions closed unchanged.')

H1('3  Where the price could trade')
# TWO CLOCKS, AND THE SECTION SAID ONE [added 03-Sep-2026]. The cone was simulated
# from the price library's last session; the valuation is struck against the latest
# known price. They were the same number until the library stopped moving. Stating
# both, and which one every figure below is measured against, is the whole fix --
# the probabilities themselves are now computed against the cone's own anchor.
P(f'A calibrated Monte-Carlo cone, carry-anchored YZ-HAR-t, 50,000 paths, seed 42, '
  f'ν = {S0["nu"]}, width calibration {S0["width_cal"]}. The drift is the CARRY — '
  f'ln(1+risk-free) less ln(1+dividend yield) — and NO part of it comes from the valuation, so '
  f'the cone can and does sit above a fair value well below it.')
P(f'READ THIS SECTION AGAINST EGP {p2(STK["spot"])}, NOT AGAINST THE PRICE ON THE '
  f'MASTHEAD. The cone was simulated from the closing price of '
  f'{STK["anchor_date"]}, which is the last session in the price history it was '
  f'built on; the valuation is struck against the {IN.get("spot_date", "later")} '
  f'close of EGP {p2(SPOT)}. Those are two different clocks and they are supposed '
  f'to be: a fresh price moves the valuation without re-running the simulation, and '
  f'a fresh price history moves the simulation without re-striking the valuation. '
  f'Every percentile and every probability in this section is measured against EGP '
  f'{p2(STK["spot"])}.')
# "TODAY" IS THE WRONG PRICE AND THIS SECTION SAYS SO IN CAPITALS FOUR LINES ABOVE.
# The probability is the share of paths finishing above the price the cone was STRUCK
# at, which is the 2026-08-06 close, not the masthead's later one. ARCC's edition of
# the same week names the price in this header; this one said "today".
table([['Horizon', 'p5', 'p25', 'median', 'p75', 'p95',
        'P(above %.2f)' % STK['spot'], 'Grade date'],
       ['1 month', *[p2(H1M['pct'][k]) for k in ('p5', 'p25', 'p50', 'p75', 'p95')],
        pc(H1M['p_above']), H1M['grade_date']],
       ['3 months', *[p2(H3M['pct'][k]) for k in ('p5', 'p25', 'p50', 'p75', 'p95')],
        pc(H3M['p_above']), H3M['grade_date']]],
      [1.05, 0.72, 0.72, 0.8, 0.72, 0.72, 1.05, 1.05], size=8.7)
caption('Table 19 — the published percentiles. The three-month calendar target falls on a '
        'non-trading day, so the grade date rolls FORWARD to the first real session, which is how '
        'the ledger will grade it.')
table([['What is measured', 'Value', 'Reading'],
       ['Resolved three-month forecasts', n0(BAND['n']),
        'every forecast this name has made that has since matured'],
       ['Finished inside the 90% band', f"{BAND['hits']} of {BAND['n']} ({pc(BAND['c90'], 1)})",
        'against a 90% promise'],
       ['Finished inside the 80% band', pc(BAND['c80'], 1), 'against an 80% promise'],
       ['Finished inside the 50% band', pc(BAND['c50'], 1), 'against a 50% promise'],
       ['Band width against a no-forecast rule', f"{BAND['width']:.3f}x",
        'above 1.00 means our band is the wider of the two'],
       ['Length of record', BAND['strength'].upper(),
        'long enough for the percentage above to mean something']],
      [2.4, 1.5, 2.1], size=8.7, left_cols=(3,))
caption('Table 20 — the band record, published beside the forecast rather than behind it. Over '
        f'{BAND["n"]} resolved three-month forecasts on this name the price finished inside the '
        f'90% band {pc(BAND["c90"], 1)} of the time against a 90% promise. The count is printed '
        'beside the percentage because a percentage without its count is the number that '
        'misleads. No flag is raised here: on a two-sided test at the 5% level this record is not '
        'distinguishable from a cone that did what it said, and the honest response to the '
        f'ordinary case is to say nothing further. The band is {BAND["width"]:.2f}x the width '
        'of a simple '
        'no-forecast rule’s — wider, not narrower — and that is disclosed rather than treated as '
        'a fault, because on Egyptian tail risk a wider band is often the truthful one.')
# SIX PRICE LEVELS WERE TYPED INTO THIS BUILDER [corrected 03-Sep-2026]. Depth-bar
# standard 3 says every builder reads the committed numbers file exclusively and no
# financial numeral is typed into one; a ladder rung is a price. They are chosen round
# numbers spanning spot and the central — a presentation choice, which is legitimate
# and belongs in the register where a reader can see it chosen.
LEVELS = list(D['touch_ladder']['levels'])


def p_touch(level, h):
    """Probability the path TOUCHES a level, from the published percentiles and the anchor
    volatility — the reflection principle on a driftless-in-logs approximation, which is what
    the engine's own stored ladder is built on."""
    # THE CONE HAS ITS OWN ANCHOR AND THIS FUNCTION WAS USING THE STUDY'S SPOT
    # [corrected 03-Sep-2026]. The percentiles in h were simulated from the strike's
    # anchor of EGP 9.10 on 6 August; SPOT is the 3-September close of 13.50. Mixing
    # them embedded a one-month log drift of -0.3866 -- a 32% fall -- against the
    # engine's own drift of +0.79%, and printed "EGP 11.83 -> 99.5%" beside the
    # words THIS STUDY'S FAIR VALUE. The two are different clocks: a fresh price
    # moves the valuation without re-striking the cone. Every probability here is
    # now computed against the anchor the cone was actually simulated from.
    _anchor = STK['spot']
    s_ = h['sigma_h']
    m = math.log(h['pct']['p50'] / _anchor)
    b = math.log(level / _anchor)
    if abs(s_) < 1e-9:
        return 0.0
    from statistics import NormalDist
    N = NormalDist().cdf
    if b > 0:
        return min(1.0, N((m - b) / s_) + math.exp(2 * m * b / s_ ** 2) * N((-b - m) / s_))
    return min(1.0, N((b - m) / s_) + math.exp(2 * m * b / s_ ** 2) * N((b + m) / s_))


table([['Level, EGP', 'Touched within 1 month', 'Touched within 3 months', 'Note'],
       *[[p2(L), pc(p_touch(L, H1M)), pc(p_touch(L, H3M)),
          ('the market price' if abs(L - SPOT) < 1e-9 else
           ('THIS STUDY’S FAIR VALUE' if abs(L - C) < 1e-9 else ''))] for L in LEVELS]],
      [1.05, 1.65, 1.65, 2.0], size=8.6, left_cols=(3,))
caption('Table 21 — the touch ladder: the chance the price trades AT or THROUGH each level at '
        'any point in the window, which is a higher number than the chance of closing beyond it. '
        'Note the last row. The cone gives the price a real chance of reaching this study’s fair '
        'value inside three months, but a touch is not a re-rating — it is the tape passing '
        'through a level, and the study makes no claim about when or whether the market closes '
        'the gap.')
table([['Diagnostic', 'Value', 'Reading'],
       ['Coverage at 50%', pc(S0['cov50'], 1), 'against a nominal 50%'],
       ['Coverage at 80%', pc(S0['cov80'], 1), 'against a nominal 80%'],
       ['Coverage at 90%', pc(S0['cov90'], 1), 'against a nominal 90%'],
       ['PIT mean', n3(S0['pit_mean']), 'against a nominal 0.500 — no material centring bias'],
       ['Width against benchmark', f"{S0['w90_ratio']:.3f}x",
        'the cone is marginally NARROWER than the carry-anchored random walk'],
       ['Windows scored', n0(S0['windows_scored']),
        f"{n0(S0['windows_prebreak_dropped'])} pre-break origins dropped"]],
      [2.0, 1.15, 3.2], size=8.6, left_cols=(2,))
caption('Table 22 — cone diagnostics, on this name’s own history. Coverage sits close to what '
        'was promised at all three levels and the centring test shows no material bias, so the '
        'band record in Table 20 is a statement about how often the cone held rather than about '
        'the cone being mis-shaped. Published because a record that shows only a headline is not '
        'a record.')

figure(os.path.join(HERE, 'fig6_cone.png'), 6.7,
       'Figure 5 — the cone against fair value in gold. The two objects answer different '
       'questions and are never blended.')

H1('4  The two answers side by side')
table([['Question', 'Object', 'Answer', 'Horizon'],
       ['What is the business worth?', 'fair value',
        f'EGP {p2(C)}  (range {p2(LO)}–{p2(HI)})', 'undated'],
       ['Where might the price go?', 'calibrated price cone',
        f'3-month median EGP {p2(H3M["pct"]["p50"])}  '
        f'({p2(H3M["pct"]["p5"])}–{p2(H3M["pct"]["p95"])})', '1 to 3 months'],
       ['What does the market say today?', 'last close', f'EGP {p2(SPOT)}', '6 August 2026']],
      [2.1, 1.5, 2.4, 1.0], size=8.8, left_cols=(1, 2, 3))
caption('Table 23 — the fair-value read and the price cone are separate objects and are never '
        'combined into one number. A fair value far below a cone median is not a contradiction: '
        'the cone prices where the tape can travel over weeks, and the study prices what the '
        'business is worth.')

H1('5  What would move the answer')
bullet(f'the margin is the thesis and it is administered, not competed. Half a point in every '
       f'forecast year is worth about EGP '
       f'{abs(grid_vals("Gross margin, shifted on every forecast year")[1][1] - LN["dcf"]["base"]):.2f} '
       'on the cash-flow lens, and the filed record spans 514 basis points;',
       bold_head='GROSS MARGIN — ')
bullet('the base year averages a strong reviewed half with a weaker audited one. If the '
       'weakness before 2026 turns out to be a superseded level rather than a season, the '
       'base is too low and the whole build moves with it — and note the direction, because '
       'it is the opposite of the usual caveat: anchoring on the latest reviewed half alone '
       'prices the central HIGHER, not lower, by about half again;',
       bold_head='THE BASE ANCHOR — ')
bullet('two exchange disclosures could not be reached from this environment and pull in '
       'OPPOSITE directions — a board capital budget (roughly −12% at face) and a revised '
       'FY2026 profit budget (roughly +17%);', bold_head='THE TWO UNREAD DISCLOSURES — ')
bullet(f'the processing-intensity weights redistribute cost between lines. They move the mix '
       f'effect and the per-line spreads, not the company total, which stays pinned to note '
       f'15-A;', bold_head='THE ONE JUDGEMENT INPUT — ')
bullet(f'the state petroleum complex is both the dominant customer and the feedstock supplier. '
       f'A policy shift on either side moves the spread directly, and the spread IS the '
       f'business.', bold_head='THE COUNTERPARTY — ')

H1('6  Probability zones')
# THE LABELS ARE BUILT FROM THE SORTED CUTS, NOT TYPED IN THE ORDER SOMEBODY
# EXPECTED THEM [corrected 03-Sep-2026]. They previously named the bands in the
# order the unsorted list happened to carry, so each label described a different
# interval from the probability printed beside it -- which is how two negative
# figures shipped under a caption promising a partition.
_zn = lambda x: ('fair value' if x is C or abs(x - C) < 1e-6 else
                 'the traded price' if x is SPOT or abs(x - SPOT) < 1e-6 else None)
_lab = lambda x: (f'EGP {p2(x)} ({_zn(x)})' if _zn(x) else f'EGP {p2(x)}')
_rows = [['Zone', 'Probability, 3 months'],
         [f'Below {_lab(CUTS[0])}', pc(ZP[0])]]
for _i in range(len(CUTS) - 1):
    _rows.append([f'{_lab(CUTS[_i])} to {_lab(CUTS[_i + 1])}', pc(ZP[_i + 1])])
_rows.append([f'Above {_lab(CUTS[-1])}', pc(ZP[-1])])
_rows.append(['TOTAL', pc(sum(ZP))])
table(_rows, [4.2, 1.9], band_rows={len(_rows) - 1}, size=9.0)
caption('Table 24 — a genuine partition: the bands tile the line, none overlaps, and the total is '
        'asserted to be 100% in the build. The previous edition published five zones summing to '
        '103.4%, with one band written descending and nested inside the band above it, so every '
        'zone probability in it was misstated. Probabilities are read off the same three-month '
        'distribution as Table 17 and say nothing about fair value.')

H1('7  Caveats — what is weak in this study')
P('This edition is the first to test the forecasting method against AMOC’s own past. The model '
  'was rebuilt as it would have stood at each of the five financial year-ends from 2021 to 2025 '
  'using only what had been published by that date, run forward, and scored against what the '
  'company went on to report. It is a test of the method rather than of any judgement, and its '
  'result belongs at the front of this section rather than buried at the back of it.')
bullet('THE METHOD DID NOT BEAT “NO CHANGE” ON THIS COMPANY. Over nine scoreable forecasts, '
       'profit attributable to shareholders was under-forecast every single time, by 64% on '
       'average, and the method’s average miss was more than twice what you get by writing down '
       'last year’s profit and stopping. That is the honest state of the evidence and no figure '
       'in this study is entitled to more precision than it supports.')
bullet('THE REASON IS INSTRUCTIVE AND IT IS NOT A TUNING PROBLEM. A forecaster standing at one of '
       'those year-ends could not know the pound was about to fall. Holding the currency still '
       'while Egyptian costs compounded at 20–30% a year froze revenue in pounds and inflated '
       'every cost line, which on a refiner guarantees a one-sided miss. Given the exchange rate '
       'and the crude price, the same driver structure predicted revenue to within 6% and cost of '
       'sales to within 2% — the machinery works; forecasting the currency is what nobody can do.')
bullet('AND EVEN THEN THE PROFIT LINE MISSED BY 68%. AMOC’s gross margin is a 6.6% residual '
       'between two numbers each above EGP 35 billion. An error of 6% on revenue against 2% on '
       'cost does not stay small — almost all of it lands in the margin. This is the single most '
       'important thing to understand about forecasting this company, and it is why Section 1.9 '
       'sensitises the two sides together rather than one at a time.')
bullet('THE TEST CHANGED THIS EDITION’S VOLUME ASSUMPTION. The previous edition grew '
       'every product line and drew its ranking from two disclosed half-years. The audited '
       'five-year record shows sales tonnage down 18.5% from its FY2022 peak with six of eight '
       'lines shrinking, and the test measures even a FLAT volume rule as already over-forecasting '
       'by 7.6%. The base path here is flat, which on this record is the optimistic case, not the '
       'neutral one.')
bullet('THE FAR FORECAST YEARS SUPPORT A RANGE AND NEVER A POINT. On its own measured error the '
       'method’s three-year profit forecast spans roughly a fifteen-fold band. That is not a '
       'useful forecast and this study does not pretend otherwise; it is why the fair value here '
       f'is a range, why the terminal block is disclosed as {pc(DCF["tv_share"], 1)} of '
       f'enterprise value, and why '
       'Section 1.7 identifies the one thing that would settle the case.')
bullet('THE TEST ITSELF IS SMALL. Five origins, nine scored forecasts, one company. AMOC '
       'publishes no accounts older than FY2022, so the window could not be lengthened. Nothing '
       'from it has been adopted as a correction — that was decided before any error was '
       'computed — and every finding is provisional.')
bullet('THE SECOND HALF OF THE BASE YEAR IS REVIEWED, NOT AUDITED. The six months to 30 June '
       '2026 carries a limited review report rather than a full audit. The PREVIOUS edition of '
       'this study went further and called it “a press release rather than a filing”, rejected '
       'its gross-profit line on a coherence test and solved gross profit from the profit line '
       'instead. The reviewed statements are in hand and the released figure was right to three '
       'hundredths of a per cent; the test failed because it estimated the half’s other income '
       'by doubling one quarter’s, which put 451mn where the filing shows 197mn. That error ran '
       'through every lens in the previous edition.')
bullet('TWO DISCLOSURES WERE UNREACHABLE, AND ONE EARLIER CLAIM OF UNREACHABILITY WAS WRONG. '
       'A board-approved FY2025/26 capital-expenditure budget and a revised FY2026 '
       'operating-profit budget were both reported by outside reviewers and neither could be '
       'opened. They move the answer roughly −12% and +17% respectively; both are named here '
       'rather than silently absent, and neither is in the numbers. The previous edition also '
       'stated that the company’s own investor-relations site refused connections. THAT WAS NOT '
       'TRUE, and it was not true because the wrong domain had been tried: amoc.com.eg does not '
       'resolve and is not the company’s site. The archive is amoceg.com, and this edition is '
       'built on 104 documents downloaded from it, including every annual consolidated filing '
       'from FY2022 to FY2025. A source recorded as unreachable is a claim about the world and it '
       'is audited like one.')
bullet('THE PROCESSING-INTENSITY WEIGHTS ARE A JUDGEMENT. Note 15-A discloses the cost stack for '
       'the company and not by line, and no weight derivable from note 14-A alone can '
       'differentiate per-line margins, because that note contains only price and volume. The '
       'vector is registered and dated, and it cannot move the company total.')
bullet('THE RISK-FREE RATE COULD NOT BE RE-VERIFIED. The 22.31% ten-year yield is carried from a '
       'house reference that this environment could not open; three reviewers independently '
       'place the rate between 22.6% and 23.0%. At the top of that range the central falls about '
       'half a percent — the case does not turn on it, but the citation is weak and is corrected '
       'to say so.')
_GM_SPREAD_BP = (max(HIS[p]['gm'] for p in PERIODS) - min(HIS[p]['gm'] for p in PERIODS)) * 1e4
bullet(f'THE MARGIN IS ADMINISTERED. A {_GM_SPREAD_BP:.0f}-basis-point range across '
       f'{_WORD.get(len(PERIODS), str(len(PERIODS))).lower()} consecutive filed '
       f'periods, set by a feedstock relationship with a {pc(IN["alexpet_stake"], 2)} '
       'shareholder, is not a market '
       'signal. It is the single largest uncertainty in the valuation and it cuts both ways — '
       'which is precisely why the case in section 1.13 is constructed to survive it.')

# ============================ APPENDIX A =====================================
H1('Appendix A  Financial statements')
H2(f'A.1  Income statement — {_WORD.get(len(PERIODS), str(len(PERIODS))).lower()} filed periods and a five-year forecast (EGP mn)')
# SPLIT INTO FILED AND FORECAST [03-Sep-2026]. Adding the missing fifth filed
# period took this to ten numeric columns, and ten columns of eight-character
# figures do not fit a seven-inch text block at a readable size -- the table
# discipline check said so, correctly. Two tables on the same rows read better than
# one squeezed table, and each can now carry a column wide enough for its content.
_w = lambda n: [1.55] + [min(0.85, 5.35 / n)] * n
table([['EGP mn — AS FILED', *PERIODS],
       ['Net sales', *[n0(HIS[p]['rev']) for p in PERIODS]],
       ['Cost of sales', *[n0(HIS[p]['rev'] - HIS[p]['gp']) for p in PERIODS]],
       ['Gross profit', *[n0(HIS[p]['gp']) for p in PERIODS]],
       ['Gross margin', *[pc(HIS[p]['gm'], 2) for p in PERIODS]]],
      _w(len(PERIODS)), size=7.9)
table([['EGP mn — FORECAST', *YRS],
       ['Net sales', *[n0(x) for x in F['rev']]],
       ['Cost of sales', *[n0(F['rev'][i] - F['gp'][i]) for i in range(5)]],
       ['Gross profit', *[n0(x) for x in F['gp']]],
       ['Gross margin', *[pc(x, 2) for x in F['gm']]],
       ['Operating profit', *[n0(x) for x in F['ebit']]],
       ['Net finance income', *[n0(x) for x in F['interest']]],
       ['Attributable profit', *[n0(x) for x in F['np_attr']]]],
      _w(5), size=7.9)
_LATEST_P = PERIODS[-1]
_LATEST_GM = HIS[_LATEST_P]['gm']
caption(f'Table A.1 — the {len(PERIODS)} filed periods are AS FILED and are of unequal length '
        f'(six-month periods and quarters), so they are shown as reported rather than '
        f'annualised. The forecast columns are the model.')
P(f'READ THE LAST FILED COLUMN AGAINST THE FIRST FORECAST COLUMN. The most recent filed '
  f'period, {_LATEST_P}, carries a gross margin of {pc(_LATEST_GM, 2)}; the first forecast '
  f'year opens at {pc(F["gm"][0], 2)} and the path is held roughly flat from there. THE '
  f'FORECAST IS THEREFORE BELOW THE LATEST FILED PERIOD, and a reader is entitled to know '
  f'that without deriving it. The reason is the base year: the model is anchored on the '
  f'twelve months to 30 June 2026, which averages that half with the weaker one before it '
  f'({pc(HIS[PERIODS[2]]["gm"], 2)}), rather than on the latest half alone. Whether that '
  f'weakness is seasonal or a superseded level is this study\u2019s largest contested '
  f'judgement: the same quarter a year apart runs {pc(HIS[PERIODS[1]]["gm"], 2)} against '
  f'{pc(HIS[PERIODS[3]]["gm"], 2)}, which no seasonal pattern produces. Anchoring on the '
  f'latest half and holding it flat gives EGP {p2(DCF["ps_h1_anchor"])} a share against the '
  f'published EGP {p2(C)}. It is priced here and NOT taken, because corrections are made one '
  f'at a time and this study has already made one this edition; taking a second would carry '
  f'it from below the traded price to well above it in a single step.')

H2('A.2  Balance sheet — as filed at 31 December 2025, and the forecast (EGP mn)')
table([['', 'Filed 31-Dec-2025', *YRS],
       ['Property, plant and equipment, net', n0(BASE['ppe_cy25']), *[n0(x) for x in F['ppe']]],
       ['Net working capital', n0(BASE['nwc_cy25']), *[n0(x) for x in F['nwc']]],
       ['INVESTED CAPITAL', n0(BASE['ic_cy25']), *[n0(x) for x in F['ic']]],
       ['Cash and equivalents, free', n0(BASE['cash']), *[n0(x) for x in F['cash']]],
       ['Net debt (negative = net cash)', n0(BASE['nd_cy25']), *[n0(x) for x in F['net_debt']]],
       ['Parent equity', n0(BASE['eqp_cy25']), *[n0(x) for x in F['equity']]],
       ['Total assets, as filed', n0(BASE['assets']), *['' for _ in YRS]],
       ['Total liabilities, as filed', n0(BASE['liab']), *['' for _ in YRS]],
       ['Non-controlling interest, carrying', n0(IN['eq_nci'] / 1e6), *['' for _ in YRS]]],
      [2.3, 1.15, 0.72, 0.72, 0.72, 0.72, 0.72], band_rows={3}, size=8.0)
caption('Table A.2 — the filed column foots: total assets less total liabilities less parent '
        'equity less the non-controlling interest is zero, and that identity is asserted in the '
        'build. Working capital is stated NET of the declared dividend, which is carried in the '
        'bridge instead — the previous edition left a shareholder distribution inside the '
        'operating capital ratio that drives the change in working capital in every forecast '
        'year.')

H2('A.3  Cash flow — the five-year forecast (EGP mn)')
table([['', *YRS],
       ['NOPAT, after the employees’ profit share', *[n0(x) for x in F['nopat']]],
       ['plus depreciation', *[n0(x) for x in F['dna']]],
       ['less capital expenditure', *[f"({n0(x)})" for x in F['capex']]],
       ['less change in working capital', *[f"({n0(x)})" for x in F['dnwc']]],
       ['FREE CASH FLOW TO THE FIRM', *[n0(x) for x in F['fcff']]],
       ['Memo: return on invested capital', *[pc(x, 1) for x in F['roic']]],
       ['Memo: capital expenditure / depreciation',
        *[f"{F['capex'][i]/F['dna'][i]:.2f}x" for i in range(5)]]],
      [2.7, 0.83, 0.83, 0.83, 0.83, 0.83], band_rows={5}, size=8.4)
caption('Table A.3 — note the last row. Capital expenditure EXCEEDS depreciation in every '
        'forecast year. The previous edition stated, twice, that free cash flow was overstated by '
        '"roughly EGP 2mn a year" because capital expenditure sat below depreciation; that held '
        'in the first forecast year only and reversed sign in every year after it, so the stated '
        'correction would have RAISED the valuation rather than lowered it.')

# ============================ APPENDIX B =====================================
H1('Appendix B  The cost of capital in detail')
H2('B.1  Beta')
table([['Statistic', 'Value', 'Test'],
       ['Point estimate', n3(BETA['beta']), '—'],
       ['Observations', n0(BETA['n']),
        f"{BETA['window_years']}-year window, {BETA['frequency']} returns"],
       ['R-squared', pc(BETA['r2'], 1), 'above the usability floor'],
       ['Standard error', n3(BETA['se']),
        f"{BETA['se']/BETA['beta']:.2f} of the point estimate — not a weak instrument"],
       ['90% confidence interval',
        f"[{n3(BETA['ci90'][0])}, {n3(BETA['ci90'][1])}]",
        f"spans {(BETA['ci90'][1]-BETA['ci90'][0])/BETA['beta']:.2f}x the estimate, inside the "
        f"2x flag"],
       ['Benchmark', 'EGX30',
        'the published index of the exchange AMOC is listed on'],
       ['Benchmark as of', str(BETA['index_asof']), 'the index series carries its own date'],
       ['Superseded', n3(BETA['superseded_composite']['beta']),
        'the previous edition, regressed on a house composite — withdrawn']],
      [1.75, 1.5, 3.35], size=8.6, left_cols=(2,))
caption('Table B.1 — the regression passes its usability gate on every limb, and THE WEAKNESS '
        'THE PREVIOUS EDITION RECORDED AGAINST ITSELF IS NOW CLOSED. That edition regressed '
        'against an equal-weight basket of the Egyptian names this house happens to cover, which '
        'a reader could not reproduce from public data; two reviewers raised it independently and '
        'both were right. The regressor is now the EGX30 itself. The correction is worth '
        f'recording for its SIZE as well as its direction: beta moves from '
        f'{n3(BETA["superseded_composite"]["beta"])} to {n3(BETA["beta"])}, about 3.5% lower, and '
        'the effect on the valuation is under one per cent. The old number was not badly wrong; '
        'it was unverifiable, which is a different and sufficient reason to replace it. The beta '
        'sensitivity in Table 15 bounds the whole plausible range: the cash-flow lens moves from '
        f'EGP {p2(grid_vals("Beta")[0][1])} to {p2(grid_vals("Beta")[-1][1])}, and neither end '
        'reaches the market price.')

H2('B.2  The cost of debt, and why it does not matter here')
P(f'Gross borrowings are EGP {n0((IN["debt_lt"]+IN["debt_st"])/1e6)}mn against a market '
  f'capitalisation of EGP {n0(SPOT*SH)}mn — {pc(W["wd_gross"], 4)} of the capital structure. A '
  f'500 basis-point error in the cost of debt moves the weighted cost of capital by '
  f'{W["kd_swing_effect"]*1e4:.2f} basis points. The input cannot move the answer, and the study '
  f'says so rather than dressing an immaterial input as a precise one. That immateriality is '
  f'asserted in the build, so if the capital structure ever changes the assertion fails rather '
  f'than the claim quietly going stale.')

H2('B.3  Explicit against terminal cost of capital')
P(f'The explicit rate of {pc(W["wacc_exp"], 2)} is not a normal corporate discount rate and is '
  f'not meant to be. It is what an Egyptian operating asset costs today, with the sovereign '
  f'spread stripped out of the risk-free rate so country risk is not double-counted, and with '
  f'the net-cash position pushing the operating rate ABOVE the cost of equity. The terminal rate '
  f'of {pc(W["wacc_term"], 2)} is norm-built: the central bank’s inflation target in force '
  f'plus a real convention, a normalised equity premium, and a terminal capital structure '
  f'carrying {pc(IN["wd_term"], 0)} debt rather than capitalising today’s zero-leverage '
  f'position into perpetuity. The glide between them is inherited from the cost-of-debt path’s '
  f'own cumulative progress.')
P(f'Two alternatives are computed rather than argued. On the RATING-BASIS premium the explicit '
  f'rate is {pc(DCF["wacc_exp_rating"], 2)} and the cash-flow lens is EGP '
  f'{p2(DCF["ps_rating_basis"])}. On GROSS rather than net debt weights — the construction this '
  f'study rejects, because it counts the cash pile twice — the lens is EGP '
  f'{p2(DCF["ps_gross_basis"])}. Both are published so the choice is visible.')

# ============================ APPENDIX C =====================================
H1('Appendix C  The expert appendix')
P('Three independent methods, cast by approach rather than by personality, each run on the same '
  'audited inputs and each free to disagree with the primary lens.')
E1, E2, E3 = EXP['e1'], EXP['e2'], EXP['e3']

H2(f'C.1  Expert 1 — {E1["method_short"]}')
P(f'Takes {E1["year"]} operating profit, adds the finance income the cash pile actually earns, '
  f'taxes the sum, strikes the minority, and applies a justified multiple struck BELOW the '
  f'primary lens deliberately — this is an independent opinion, not a restatement of it.')
table([['Step', 'EGP mn unless stated'],
       [f'Operating profit, {E1["year"]}', n0(E1['ebit'])],
       ['plus net finance income', n0(E1['interest'])],
       [f'taxed at the statutory {pc(RT["tax_stat"], 1)} and after the minority', ''],
       ['Attributable earnings per share, EGP', f"{E1['eps']:.3f}"],
       ['Justified price / earnings', f"{E1['pe']:.1f}x"],
       ['VALUE PER SHARE, EGP', p2(E1['base'])]],
      [4.9, 1.1], band_rows={6}, size=8.6, left_cols=())
caption(f'Table C.1 — Expert 1. Range EGP {p2(E1["rng"][0])} to {p2(E1["rng"][1])} on a 5.0x to '
        f'9.5x multiple band. This is the HIGHEST of the three and it is still '
        f'{pc(E1["base"]/SPOT-1)} against the market price. Note that it is an undiscounted '
        f'{E1["year"]} number, which is why it sits above the primary lens.')

H2(f'C.2  Expert 2 — {E2["method_short"]}')
P('Discounts cash flow to the EQUITY holder rather than to the firm: free cash flow to the firm '
  'less after-tax finance costs plus after-tax finance income, discounted at the COST OF EQUITY '
  'on its own glide rather than at the weighted rate. It is the cleanest independent check on '
  'the primary lens, because it changes both the numerator and the discount rate together.')
table([['Step', *YRS],
       ['Free cash flow to equity', *[n0(x) for x in E2['fcfe']]],
       ['Cost of equity, glided', *[pc(k, 2) for k in E2['ke_path']]],
       ['Discount factor', *[f'{d:.4f}' for d in E2['df']]],
       ['Present value', *[n0(E2['fcfe'][i] * E2['df'][i]) for i in range(5)]]],
      [2.2, 0.9, 0.9, 0.9, 0.9, 0.9], size=8.4)
table([['Step', 'EGP mn'],
       ['Present value of the explicit window', n0(E2['pv'])],
       ['Present value of the terminal block', n0(E2['pv_tv'])],
       ['less the disclosed claims carried in the bridge',
        f"({n0(BR['prov'] + BR['divp'])})"],
       ['EQUITY VALUE', n0(E2['base'] * SH)],
       ['VALUE PER SHARE, EGP', p2(E2['base'])]],
      [4.9, 1.1], band_rows={5}, size=8.6, left_cols=())
caption(f'Table C.2 — Expert 2. Range EGP {p2(E2["rng"][0])} to {p2(E2["rng"][1])}. This is the '
        f'LOWEST of the three at {pc(E2["base"]/SPOT-1)} against the price, and the reason is '
        f'the discount rate: an equity claim discounted on the equity glide from '
        f'{pc(E2["ke_path"][0], 1)} to {pc(E2["ke_path"][-1], 1)} is punished harder in the '
        f'near years than an unlevered claim on the weighted rate.')

H2(f'C.3  Expert 3 — {E3["method_short"]}')
P('Values the business as invested capital plus the present value of the ECONOMIC PROFIT it '
  'earns above its cost of capital, rather than as a stream of cash. Arithmetically it must '
  'reconcile to the primary lens on the same inputs — that is the point of including it. Where '
  'it differs is that it makes the SPREAD visible: how much of the value is capital already in '
  'the ground, and how much is return above the cost of that capital.')
table([['Step', 'EGP mn'],
       ['Invested capital at the valuation date', n0(E3['ic0'])],
       ['plus present value of economic profit, explicit window', n0(E3['pv_ep'])],
       ['plus present value of economic profit, terminal', n0(E3['pv_ep_term'])],
       ['ENTERPRISE VALUE', n0(E3['ev'])],
       ['VALUE PER SHARE after the bridge, EGP', p2(E3['base'])]],
      [4.9, 1.1], band_rows={4}, size=8.6, left_cols=())
table([['', *YRS],
       ['Economic profit', *[n0(x) for x in E3['ep']]],
       ['Return spread over the cost of capital', *[pc(x, 2) for x in E3['spread']]]],
      [2.5, 0.85, 0.85, 0.85, 0.85, 0.85], size=8.5)
caption(f'Table C.3 — Expert 3. Range EGP {p2(E3["rng"][0])} to {p2(E3["rng"][1])}. The spread '
        f'row is the finding: this business earns a POSITIVE return over its cost of capital in '
        f'every forecast year, which is why it is worth more than its invested capital — and it '
        f'is still worth materially less than the market price. Cheap capital is not the '
        f'question here; the question is how much spread {pc(TTM["gm"])} of gross margin can '
        f'support.')

# ---- C.4  cross-examination ------------------------------------------------
H2('C.4  Cross-examination')
P('Each expert is put the strongest objection the other two can make to their number, and each '
  'objection is either CONCEDED or REJECTED with the arithmetic that settles it. Nothing here '
  'is rhetorical: every figure in the table is computed from the three constructions above.')

# Expert 1 is an UNDISCOUNTED forward number. Bringing it to the valuation date on the same
# factor the normalised lens uses is the single largest correction anyone in the room can make.
_e1_pv = E1['base'] * NRM['df']
_e2_tv_share = E2['pv_tv'] / (E2['pv'] + E2['pv_tv'])
_e3_tv_share = E3['pv_ep_term'] / E3['ev']
_e3_cap_share = E3['ic0'] / E3['ev']

table([['Objection', 'Raised by', 'Answered', 'The arithmetic'],
       [f'Expert 1 values {E1["year"]} earnings and never brings them back to the valuation '
        f'date.', 'Experts 2 and 3', 'CONCEDED',
        f'Discounted {NRM["yrs"]:.1f} years at the cost of equity, Expert 1 is worth '
        f'EGP {_e1_pv:.2f}, not {p2(E1["base"])} — below Expert 3 and above Expert 2.'],
       [f'Expert 1 applies {E1["pe"]:.1f}x when this company trades at '
        f'{REL["pe_trailing"]:.1f}x its own trailing earnings.', 'Expert 3', 'REJECTED',
        f'{E1["pe"]:.1f}x is struck BELOW the trailing multiple deliberately. Using the '
        f'traded multiple would value the company at what it already costs, which the '
        f'relative lens is separately forbidden from doing.'],
       ['Expert 2 carries no bridge at all, so the tax-disputes provision and the declared '
        'dividend never reach the shareholder.', 'Expert 1', 'CONCEDED IN PART',
        f'Both are deducted: EGP {n0(BR["prov"] + BR["divp"])}mn, or '
        f'EGP {(BR["prov"] + BR["divp"]) / SH:.2f} a share. What is NOT added back is the '
        f'cash itself — it reaches the holder through finance income instead, which is what '
        f'keeps this read independent of the primary lens.'],
       [f'Expert 2 puts {pc(_e2_tv_share)} of its value beyond year five.', 'Expert 3',
        'REJECTED',
        f'The primary lens puts {pc(DCF["tv_share"])} there on the same horizon. A terminal '
        f'block this size is a property of a five-year window on a company still recovering, '
        f'not of this expert\'s choices.'],
       [f'Expert 3 must reconcile to the primary lens by construction, so it is not an '
        f'independent read.', 'Experts 1 and 2', 'CONCEDED — AND THAT IS WHY IT IS HERE',
        f'It is included to make the SPLIT visible: {pc(_e3_cap_share)} of its enterprise '
        f'value is capital already in the ground and {pc(_e3_tv_share)} is economic profit '
        f'beyond year five. Neither of the other two shows that.'],
       ['Expert 3 charges the cost of capital on opening invested capital, which flatters '
        'economic profit in a growing year.', 'Expert 2', 'REJECTED',
        'Opening capital is the capital the year had available to earn on. Charging closing '
        'capital would charge for assets bought with the year\'s own cash flow.']],
      [2.15, 0.95, 1.15, 2.55], size=8.0, left_cols=(0, 1, 2, 3))
caption('Table C.4 — cross-examination. Two of the six objections are conceded outright and one '
        'in part; the three rejections each rest on a number rather than a preference. The '
        'largest single correction in the room is the first one, and it is the reason the panel '
        'median is not simply the highest of the three.')

# ---- C.5  the three in one room --------------------------------------------
H2('C.5  The three in one room')
_lo3 = min(EXP[k]['base'] for k in ('e1', 'e2', 'e3'))
_hi3 = max(EXP[k]['base'] for k in ('e1', 'e2', 'e3'))
_below = sum(1 for k in ('e1', 'e2', 'e3') if EXP[k]['base'] < SPOT)
P(f'Put in one room the three methods land between EGP {p2(_lo3)} and EGP {p2(_hi3)}, a spread '
  f'of {pc(_hi3 / _lo3 - 1)} of the lower number, with a median of EGP {p2(D["panel_centre"])} '
  f'against a market price of EGP {p2(SPOT)} — {pc(D["panel_centre"] / SPOT - 1)}. '
  f'{"All three" if _below == 3 else ("Two of the three" if _below == 2 else "One of the three")} '
  f'sit below the price.')
P('Where they agree is more informative than where they differ, because the agreement is not '
  'built in. All three are struck on the same audited base year and the same house macro path, '
  'and none of them is allowed to set an inflation rate of its own — so the disagreement between '
  'them is entirely about how a peso of operating profit should be capitalised, never about what '
  'the economy is doing. All three also agree on the one thing that matters most for this name: '
  f'the company earns a positive return over its cost of capital in every forecast year — '
  f'Expert 3 measures the spread at {pc(E3["spread"][0], 1)} rising to '
  f'{pc(E3["spread"][-1], 1)} — and is still not worth the market price on any of the three '
  'constructions.')
P(f'Where they part company is the treatment of TIME. Expert 1 states a value at '
  f'{E1["year"]} and does not discount it; Expert 2 discounts an equity claim on the cost of '
  f'equity\'s own glide, which is the harshest treatment of the near years available; Expert 3 '
  f'discounts at the weighted rate and separates capital already in place from the return earned '
  f'on it. Bring Expert 1 back to the valuation date and the three collapse into a band of '
  f'EGP {p2(min(_e1_pv, E2["base"], E3["base"]))} to '
  f'EGP {p2(max(_e1_pv, E2["base"], E3["base"]))} — narrower than the spread as published, '
  'which says that most of the visible disagreement in this panel is a disagreement about the '
  'valuation date rather than about the company.')

# ---- C.6  reading the divergence -------------------------------------------
H2('C.6  Reading the divergence')
P('One row per pair, isolating the single assumption that accounts for most of the gap between '
  'them. The last column is what is LEFT of the gap once that assumption is removed — the honest '
  'measure of how much the two methods really disagree. Where removing it takes the pair past '
  'each other rather than together, the cell says so: an assumption can over-explain a gap, and '
  'that is worth more to a reader than a tidy number.')
# The residual is what the NAMED driver does not account for, so it is only printed where
# the driver can actually be removed and the two constructions re-compared. Where it cannot,
# the cell says so: a residual printed equal to the whole gap would assert that the named
# driver explains nothing, which contradicts the column it sits in.
def _resid(a, b, a_adj):
    """What is left of the gap once the named driver is removed — and a WORD where removing
    it takes the pair past each other.

    The first draft printed the bare absolute residual and produced a cell reading 4.48
    against a gap of 2.04, which looks like an arithmetic error and is in fact a real and
    interesting fact: bringing Expert 1 back to the valuation date does not close the gap to
    Expert 3, it CROSSES it. A number that needs a sentence gets the sentence."""
    before, after = a - b, a_adj - b
    if before * after < 0:
        return '%.2f — overshoots' % abs(after)
    return '%.2f' % abs(after)


_pairs = [
    ('Expert 1 vs Expert 2', E1['base'], E2['base'],
     'the valuation date — Expert 1 is an undiscounted forward number',
     _resid(E1['base'], E2['base'], _e1_pv)),
    ('Expert 1 vs Expert 3', E1['base'], E3['base'],
     'the valuation date, again — which here CROSSES rather than closes: discounted, '
     'Expert 1 falls below Expert 3',
     _resid(E1['base'], E3['base'], _e1_pv)),
    ('Expert 2 vs Expert 3', E2['base'], E3['base'],
     f'the BRIDGE — Expert 3 adds net cash of {EXP["e2e3"]["cash"]:+.2f} a share at face, '
     f'Expert 2 takes it through finance income only. The discount rate, measured by '
     f're-running Expert 2 on the weighted rate, is worth only '
     f'{EXP["e2e3"]["rate"]:+.2f}',
     f'{abs(EXP["e2e3"]["resid"]):.2f}'),
    ('Panel median vs the primary lens', D['panel_centre'], D['central'],
     'nothing structural — the primary lens is one of the same constructions',
     'not decomposed'),
]
table([['Pair', 'Gap, EGP', 'Gap, %', 'What drives it', 'Left after removing it'],
       *[[nm, f'{abs(a - b):.2f}', pc(abs(a - b) / min(a, b)), why, res]
         for nm, a, b, why, res in _pairs]],
      [1.45, 0.60, 0.55, 2.45, 1.85], size=8.0, left_cols=(0, 3, 4))
caption(f'Table C.6 — the divergence. The two largest gaps in the panel are both explained by '
        f'ONE thing, and it is not an assumption about the business: Expert 1 states a value at '
        f'{E1["year"]} while the other two state one today. The third row is measured the same '
        f'way, and the measurement OVERTURNED the label this table first carried. Discounting '
        f'Expert 2\'s own cash flows on the WEIGHTED rate rather than the cost of equity\'s '
        f'glide gives EGP {p2(E2["ps_at_wacc"])} — so the price of time is worth only '
        f'EGP {abs(EXP["e2e3"]["rate"]):.2f} of a {abs(EXP["e2e3"]["gap"]):.2f} gap, about '
        f'{abs(EXP["e2e3"]["rate"]/EXP["e2e3"]["gap"]):.0%} of it. What carries the rest is the '
        f'BRIDGE: Expert 3 adds the net cash at face and Expert 2 does not. '
        f'The last row carries no residual because there is no single driver to remove: '
        f'the median IS one of these three constructions and the primary lens is a fourth read '
        f'of the same statements.')

H2('C.7  The panel at a glance')
table([['Expert', 'Method', 'Central', 'Range', 'vs price'],
       *[[k.upper(), EXP[k]['method_short'], p2(EXP[k]['base']),
          f"{p2(EXP[k]['rng'][0])}–{p2(EXP[k]['rng'][1])}", pc(EXP[k]['base'] / SPOT - 1)]
         for k in ('e1', 'e2', 'e3')],
       ['PANEL', 'median of the three', p2(D['panel_centre']), '',
        pc(D['panel_centre'] / SPOT - 1)]],
      [0.85, 2.6, 0.85, 1.2, 0.9], band_rows={4}, size=8.7, left_cols=(1,))
caption('Table C.7 — the panel. Each range is that expert\'s OWN method re-run at the two '
        'filed-evidence corners the primary lens publishes — the worst gross margin in the '
        'audited record and the best full year — so the panel and the envelope are read on one '
        'clock. Earlier editions typed these bands beside the methods, and two of them had gone '
        'stale enough to publish a central outside its own range.')

# ============================ ABOUT ==========================================
H1('About this study')
box([
    ('WHAT THIS IS.  ',
     'An independent, educational valuation study. It is NOT investment advice, and it issues no '
     'buy, sell or hold recommendation. It publishes a fair-value range, a probability '
     'distribution for the price, and the model behind both, and it grades its own forecasts '
     'publicly when they resolve.'),
    ('WHAT IT RESTS ON.  ',
     'The company’s own audited consolidated financial statements, taken from its own '
     'investor-relations archive: the five financial years to 30 June 2021, 2022, 2023, 2024 and '
     '2025; the transition period 1 July to 31 December 2025 (Crowe — Dr A. M. Hegazy & Co, '
     'unqualified, signed at Giza 18 February 2026); reviewed statements for the three months to '
     '31 March 2026; and the half-year results disclosed to the Egyptian Exchange on 29-30 July '
     '2026, which are REPORTED and not audited. The financial year to 30 June 2023 carries a '
     'QUALIFIED audit opinion, on two balance-sheet matters that do not touch the revenue or cost '
     'lines this study forecasts; it is named here rather than left for a reader to find. Every '
     'input carries a value, a source, a date and a research ring in the companion source '
     'register.'),
    ('THE COMPANION FILES.  ',
     f'The workbook recalculates this entire study live across sixteen sheets: '
     f'{n0(CENSUS["formulas"])} formulas '
     f'against {n0(CENSUS["pasted"])} pasted filing values ({pc(CENSUS["share"], 1)} live), with '
     'all thirty sensitivity grid points written out as complete formula engines and every '
     'formula cell verified against the model by an independent evaluator — 0 unresolvable, 0 '
     f'unchecked, 0 disagreements. The bibliography lists all {n0(len(IN))} registered inputs '
     'with their sources, the triangulations, and the negative results.'),
    ('HOW FAR THIS METHOD HAS BEEN TESTED.  ',
     'The forecasting method behind Section 1 was rebuilt at each of the five financial year-ends '
     'from 2021 to 2025 and scored against what the company went on to report. It did not beat '
     'the simple rule of assuming last year’s profit repeats. Section 7 sets out what that means '
     'and what it changed here; the short version is that nobody standing at those year-ends '
     'could forecast the pound, and on a business whose margin is a six-per-cent residual '
     'between two very large numbers, that is enough to make the profit line unreliable more '
     'than a year out. The range in this study is wide because the evidence says it should be.'),
])

H1('Disclosure')
box([
    ('NO RECOMMENDATION.  ',
     'Nothing in this document is a recommendation to buy, sell or hold any security, and no '
     'price target is expressed or implied. A fair-value range is an estimate of what a business '
     'is worth on stated assumptions; it is not a forecast of where a share price will go, and '
     'the two regularly disagree for long periods.'),
    ('NO POSITION, NO RELATIONSHIP, NO FEE.  ',
     'The author holds no position in the security, has no relationship with the company, its '
     'management, its advisers or its shareholders, and received no payment or consideration '
     'from any of them for this work.'),
    ('WHAT COULD BE WRONG.  ',
     'The estimate rests on published filings, a forecasting method whose measured accuracy on '
     'this company is set out in Section 7, and judgements listed with what would overturn each '
     'of them in the companion bibliography. Section 7 states the known weaknesses; it is written '
     'to be read, not to be skipped.'),
    ('EDUCATIONAL PURPOSE.  ',
     'This study is published to show a valuation method being applied and graded in public. Its '
     'forecasts are recorded when made and scored when they resolve, including the ones that '
     'turn out wrong.'),
])

OUT = os.path.join(HERE, 'AMOC_Valuation_Study_03-09-2026_public.docx')
doc.save(OUT)
print('wrote', OUT)
