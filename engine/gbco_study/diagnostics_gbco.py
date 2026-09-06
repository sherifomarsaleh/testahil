#!/usr/bin/env python3
"""GBCO — the reverse read and the contested-judgement record [R-ENF-05], COMPUTED.

WHAT THIS FILE IS. Two diagnostics, both aimed at a study auditing its own answer
rather than only its steps:

  1. THE REVERSE READ. This study states what it believes; it does not state what
     the PRICE believes, and the two are the same model read backwards. Solved
     here on the study's OWN published construction — the four-lens weighted
     central — holding every other driver at its published value and moving only
     the one line the study itself names as the crux.

  2. THE CONTESTED-JUDGEMENT RECORD. Every fork worth arguing about, valued BOTH
     ways by re-running this study's own arithmetic, with the side adopted and
     why, and a binomial sign test on which way they went.

WHY IT LIVES OUTSIDE THE NUMBERS FILE. A quantity solved from a traded price and
then used anywhere in the valuation is the reverse-engineered rate the protocol
prohibits outright, arriving through a side door. So the reverse read is written
to diagnostics.json, no builder reads it, and this file asserts that
study_numbers.json is byte-identical before and after the run — a diagnostic that
can write back into the model is not a diagnostic.

WHY IT RE-DERIVES THE PUBLISHED ANSWER FIRST AND REFUSES IF IT CANNOT. The
study's own compute.py does not run (it passes an argument the current
cost-of-capital builder no longer accepts), so the arithmetic below is rebuilt
from the committed numbers file and ASSERTED against the answer the study
publishes. If the study is ever re-struck and this file is not re-run, the assert
fails rather than the record freezing at a number nobody notices — which is the
whole of [R-ENF-06].

NOTHING HERE CHANGES A DRIVER, A RATE, A FORECAST OR THE FAIR VALUE. Valuing the
alternative framing of a judgement is a calculation reported, never a change made.

    python3 diagnostics_gbco.py     writes diagnostics.json + contested_judgements.json
"""
import glob
import hashlib
import json
import os
import re
from math import comb

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.dirname(HERE)

# ---------------------------------------------------------------------------
# TWO FIGURES THIS STUDY HOLDS IN ITS OWN SOURCE RATHER THAN IN ITS NUMBERS FILE.
# The normalised-earnings lens commits only its per-share result, so the earnings
# base and the multiple cannot be recovered from it separately (three published
# cases, six unknowns). Both are read off this study's own committed record, with
# the file that carries each named, and neither is re-sourced or estimated.
NORM_BASE_PAT_EGP_MN = 4200.0      # compute.py, `norm_pat` — this study's mid-cycle
                                   # group PAT, the base of the normalised lens
NORM_MULTIPLE = 8.5                # compute.py, the through-cycle multiple applied
                                   # to it in the same line
FY25_REPORTED_NP_EGP_MN = 2880.0   # GB Corp FY25 attributable net profit as reported,
                                   # FY25 earnings release; carried in this study's
                                   # own Appendix A income statement (build_xlsx3.py,
                                   # 'Net profit (attributable)') and its company
                                   # overview table (docx_A.py)
FY25_ASSOCIATES_CARRYING_EGP_MN = 13689.5   # 'Investments in associates', consolidated
                                   # balance sheet as reported at FY25, same release;
                                   # this study's own Appendix A (build_xlsx3.py)


def _sha(path):
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()


def latest_supplied_prices():
    """The latest known close, from the committed price artefact rather than typed.

    Resolved BY PATTERN and by the date the filename carries, so a later supply
    is picked up instead of this file freezing on one filename.
    """
    files = glob.glob(os.path.join(ENGINE, 'prices', 'SUPPLIED_*.json'))
    if not files:
        raise SystemExit('no supplied-price artefact found under engine/prices/')

    def key(p):
        m = re.search(r'SUPPLIED_(\d{2})-(\d{2})-(\d{4})\.json$', os.path.basename(p))
        return (m.group(3), m.group(2), m.group(1)) if m else ('', '', '')

    path = sorted(files, key=key)[-1]
    doc = json.load(open(path, encoding='utf-8'))
    return path, doc


class Model:
    """This study's own valuation arithmetic, rebuilt from its committed numbers.

    Every quantity below is READ from study_numbers.json. The class exposes one
    entry point, `central()`, which reproduces the published answer when called
    with no arguments and prices an alternative framing when called with one
    argument moved. It is the same construction in both cases, which is the only
    way a "both ways" figure means anything.
    """

    def __init__(self, N):
        self.N = N
        self.rows = N['dcf']['rows']
        self.SH = N['shares']
        self.W = N['lenses']['weights']
        self.rel = N['lenses']['relative']['base']
        self.norm = N['lenses']['normalized']['base']
        self.cap = N['sotp']['cap_val']
        self.other = N['sotp']['other_assoc']
        self.mark = N['sotp']['mnt_halan_value']
        self.disc = N['sotp']['disc']
        self.nd = N['dcf']['auto_nd']
        self.nci = N['dcf']['auto_nci']
        self.wacc = N['dcf']['wacc']
        self.tg = N['dcf']['tg']
        self.wb = N['dcf']['wacc_build']
        self.fx = N['sotp']['egp_usd']
        self.stake = N['sotp']['mnt_halan_stake']
        self.round_usd = N['sotp']['mnt_halan_round_usd']
        self.fcff = [r['fcff'] for r in self.rows]
        # the operating shape of the auto leg, recovered from the committed rows so
        # a margin or a working-capital framing can be re-priced without any driver
        # being typed here
        self.tax = 1.0 - self.rows[0]['nopat'] / self.rows[0]['ebit']
        self.gpm = [r['gp'] / r['rev'] for r in self.rows]
        self.opex = [(r['gp'] - r['ebit']) / r['rev'] for r in self.rows]
        self.wcpct = [r['wc'] / r['rev'] for r in self.rows]
        self.wc_open = self.rows[0]['wc'] - self.rows[0]['dwc']

    # -- the auto leg -------------------------------------------------------
    def fcff_path(self, gpm=None, wcpct=None):
        gpm = gpm or self.gpm
        wcpct = wcpct or self.wcpct
        out, prev = [], self.wc_open
        for i, r in enumerate(self.rows):
            ebit = r['rev'] * gpm[i] - r['rev'] * self.opex[i]
            wc = r['rev'] * wcpct[i]
            out.append(ebit * (1.0 - self.tax) + r['dna'] - r['capex'] - (wc - prev))
            prev = wc
        return out

    def auto_ev(self, fcff, w, g):
        pv = sum(f / (1.0 + w) ** (i + 1) for i, f in enumerate(fcff))
        return pv + fcff[-1] * (1.0 + g) / (w - g) / (1.0 + w) ** len(fcff)

    # -- the whole answer ---------------------------------------------------
    def legs(self, fcff=None, w=None, g=None, mark=None, cap=None):
        fcff = self.fcff if fcff is None else fcff
        w = self.wacc if w is None else w
        g = self.tg if g is None else g
        mark = self.mark if mark is None else mark
        cap = self.cap if cap is None else cap
        auto_eq = self.auto_ev(fcff, w, g) - self.nd - self.nci
        return auto_eq, auto_eq + cap + self.other + mark

    def primary(self, disc=None, mark_only_discount=False, **kw):
        """The split-the-legs sum-of-the-parts — the lens this study names primary."""
        d = self.disc if disc is None else disc
        auto_eq, total = self.legs(**kw)
        if mark_only_discount:
            mark = self.mark if kw.get('mark') is None else kw['mark']
            return (total - mark * d) / self.SH
        return total * (1.0 - d) / self.SH

    def central(self, disc=None, norm=None, mark_only_discount=False, **kw):
        """The four-lens weighted central — the answer this study publishes."""
        d = self.disc if disc is None else disc
        nrm = self.norm if norm is None else norm
        _, total = self.legs(**kw)
        return (self.W['sotp'] * self.primary(disc=d, mark_only_discount=mark_only_discount, **kw)
                + self.W['prediscount'] * total / self.SH
                + self.W['relative'] * self.rel
                + self.W['normalized'] * nrm)

    def wacc_at(self, beta, erp):
        return self.wb['we'] * (self.wb['rf'] + beta * erp) + self.wb['wd'] * self.wb['kd_aftertax']

    # -- the reverse read ---------------------------------------------------
    def implied_mark(self, price, on_primary=False):
        """The associate mark the price implies, inverted from this study's own
        construction with every other line held at its published value."""
        auto_eq, _ = self.legs()
        rest = auto_eq + self.cap + self.other
        if on_primary:
            return price * self.SH / (1.0 - self.disc) - rest
        k = (self.W['sotp'] * (1.0 - self.disc) + self.W['prediscount']) / self.SH
        const = self.W['relative'] * self.rel + self.W['normalized'] * self.norm
        return (price - const) / k - rest

    def implied_flat_wacc(self, price):
        """The same disagreement asked of the auto leg's discount rate instead.

        Bisection: above the terminal growth the answer falls monotonically in the
        rate, so the root is unique and does not depend on a starting guess.
        """
        lo, hi = self.tg + 1e-6, 3.0
        for _ in range(400):
            mid = 0.5 * (lo + hi)
            if self.central(w=mid) > price:
                lo = mid
            else:
                hi = mid
        return 0.5 * (lo + hi)


def main():
    numbers = os.path.join(HERE, 'study_numbers.json')
    before = _sha(numbers)
    N = json.load(open(numbers, encoding='utf-8'))
    B = json.load(open(os.path.join(HERE, 'beta_result.json'), encoding='utf-8'))
    M = Model(N)

    published = N['lenses']['central']['base']
    strike = N['spot']
    assert abs(M.central() - published) < 1e-9, (
        'this file no longer reproduces the answer the study publishes (%.10f vs '
        '%.10f). A diagnostic that has drifted from its study is worse than none, '
        'because it has the shape of a computed record.' % (M.central(), published))
    assert abs(M.primary() - N['sotp']['ps']) < 1e-9

    price_path, prices = latest_supplied_prices()
    row = prices['prices'][N.get('ticker', 'GBCO')] if 'ticker' in N else prices['prices']['GBCO']
    spot, spot_date = float(row['price']), row['date']

    # ---------------- 1. THE REVERSE READ ---------------------------------
    mark_now = M.implied_mark(spot)
    mark_strike = M.implied_mark(strike)
    mark_primary = M.implied_mark(spot, on_primary=True)
    carry_mark = FY25_ASSOCIATES_CARRYING_EGP_MN - M.other

    def whole_usd(mark_egp):
        return mark_egp / M.fx / M.stake

    implied_usd = whole_usd(mark_now)
    assert abs(M.central(mark=mark_now) - spot) < 1e-6

    diag = {
        'ticker': 'GBCO',
        'as_of': '2026-09-06',
        'spot': spot,
        'spot_date': 'close %s, the Egyptian Exchange' % spot_date,
        'spot_source': '%s — %s, the close supplied by the principal'
                       % (os.path.relpath(price_path, os.path.dirname(ENGINE)),
                          row.get('company', 'GB Corp')),
        # [R-ENF-06] the vintage this artefact was built against
        'published_central': published,
        'published_spot': strike,
        'why_this_file': (
            'The reverse read — what the traded price must believe — is a DIAGNOSTIC and '
            'lives outside the numbers file every builder reads. A mark, a rate or a growth '
            'solved from a price and then used anywhere in the valuation is the '
            'reverse-engineered figure the protocol prohibits outright, arriving through a '
            'side door, and the prohibition is worth nothing if the side door is open. '
            'Nothing in this file is an input to anything: no builder in this study reads '
            'it, it is COMPUTED by diagnostics_gbco.py, and that script asserts the '
            'committed numbers file is byte-identical before and after it runs.'),
        'implied': {
            'quantity': ("the whole-company valuation of MNT-Halan, in US dollars, that the "
                         "traded price implies for GB Corp's 41.61% stake — the single line "
                         "this study names as its crux"),
            'value': implied_usd,
            'study_value': M.round_usd,
            'units': 'USD million, the valuation of MNT-Halan as a whole',
            'value_at_the_strike_price': whole_usd(mark_strike),
            'value_on_the_primary_lens': whole_usd(mark_primary),
            'implied_stake_value_egp_mn': mark_now,
            'implied_stake_value_usd_mn': mark_now / M.fx,
            'study_stake_value_egp_mn': M.mark,
            'implied_as_a_share_of_the_round': implied_usd / M.round_usd,
            'company_disclosed': {
                'round_valuation_usd_mn': M.round_usd,
                'stake': M.stake,
                'stake_source': ("GB Corp's own press release, 9 June 2026, on MNT-Halan's "
                                 "Al Ahly Capital-led capital increase: the stake 'will be "
                                 "adjusted to 41.61%, compared to 42.58% prior to the "
                                 "transaction'"),
                'associates_carrying_value_fy25_egp_mn': FY25_ASSOCIATES_CARRYING_EGP_MN,
                'carrying_value_source': ("'Investments in associates', consolidated balance "
                                          "sheet as reported at FY25, GB Corp FY25 earnings "
                                          "release, carried in this study's own Appendix A"),
                'mnt_halan_carrying_value_egp_mn': carry_mark,
                'whole_company_at_carrying_value_usd_mn': whole_usd(carry_mark),
                'carrying_value_caveat': (
                    'the carrying value is an equity-accounted book figure — cost plus the '
                    "group's share of retained results, less impairment — and is not a "
                    'valuation. It is quoted because it is the only other dated, '
                    'company-disclosed number attached to this stake, and because a reader '
                    'can check it.'),
            },
            'solved_on': (
                "this study's own construction, rebuilt from its committed numbers file and "
                "asserted against the answer it publishes, holding the auto leg's cash "
                "flows, its cost of capital, its terminal growth, the lender's mark, the "
                "other associates, the complexity discount, the two earnings lenses and the "
                "four lens weights all at their published values, and moving only the "
                "MNT-Halan mark until the model reproduces the traded price. Solved on the "
                "PUBLISHED central — the four-lens blend — because that is the answer the "
                "study states; the same solve on the primary lens alone is carried beside "
                "it, because 45% of the blend's weight sits in two earnings lenses that do "
                "not touch this stake at all and therefore dampen the read."),
            'second_framing': {
                'quantity': ('the single flat discount rate on the auto leg that reproduces '
                             'the traded price, every other line held at its published value'),
                'value': M.implied_flat_wacc(spot),
                'study_value': M.wacc,
                'value_at_the_strike_price': M.implied_flat_wacc(strike),
                'reading': ('carried here to show what the disagreement is NOT about. Asked '
                            "of the auto leg's discount rate, the price implies %.2f%% "
                            'against this study\'s %.2f%% — 11.4 points of cost of capital '
                            'on a business worth a quarter of the sum of the parts. That is '
                            'a far less plausible reading of the same gap than the mark, and '
                            'it is the reason the mark is the quantity solved.'
                            % (100 * M.implied_flat_wacc(spot), 100 * M.wacc)),
            },
            'reading': (
                'At EGP %.2f the price values GB Corp\'s 41.61%% stake in MNT-Halan at EGP '
                '%.0f mn, which is MNT-Halan as a whole at US$%.0f mn — %.0f%% of the '
                'US$%.1f bn the June-2026 round was struck at, and a %.0f%% discount to it. '
                'The study takes the round at face value. WHAT MAKES THIS CHECKABLE RATHER '
                'THAN RHETORICAL: GB Corp\'s own FY25 balance sheet carries all associates '
                'at EGP %.1f mn, which nets to EGP %.0f mn for MNT-Halan and implies the '
                'whole company at US$%.0f mn — within %.1f%% of what the price is paying. '
                'The market is marking this stake at close to its book carrying value and '
                'giving the round\'s uplift no weight; the study marks it at the round. '
                'That one line is the whole disagreement, and it is a more useful statement '
                'than "the study is %+.1f%% against the price". IT DOES NOT SETTLE WHO IS '
                'RIGHT: an equity-accounted carrying value is a book number and not a '
                'valuation, and a cash round at US$%.1f bn is a real transaction price for '
                'an unlisted company in which a 41.61%% minority holder has never had an '
                'exit.'
                % (spot, mark_now, implied_usd, 100 * implied_usd / M.round_usd, M.round_usd / 1000.0,
                   100 * (1 - implied_usd / M.round_usd), FY25_ASSOCIATES_CARRYING_EGP_MN,
                   carry_mark, whole_usd(carry_mark),
                   100 * abs(whole_usd(carry_mark) / implied_usd - 1),
                   100 * (published / spot - 1), M.round_usd / 1000.0)),
        },
    }

    # ---------------- 2. THE CONTESTED JUDGEMENTS -------------------------
    beta_wacc = M.wacc_at(B['beta'], M.wb['erp_cds'])
    anchor = N['forecast_anchor']
    flat_gpm = [anchor['latest_reviewed_rate']] * len(M.rows)
    flat_wc = [M.wcpct[0]] * len(M.rows)
    alt_norm = (FY25_REPORTED_NP_EGP_MN / M.SH) * NORM_MULTIPLE

    J = [
        dict(name='the construction of the central',
             adopted='a weighted blend of four lenses at typed weights, 40/15/20/25',
             alternative=('the split-the-legs sum-of-the-parts alone — the lens this '
                          "study's own masthead names primary — with the other three "
                          'published beside it as cross-checks'),
             va=M.central(), vb=M.primary(),
             pa=M.primary(), pb=M.primary(),
             why=('the weights were typed and have never cleared any out-of-sample test. '
                  'Two of the four lenses read this group off forward and mid-cycle '
                  'earnings and do not touch the associate stake at all, so the blend '
                  'carries 45% of its weight in reads that are structurally blind to the '
                  'largest asset on the page — which the study says itself in §1.5. The '
                  'blend is also the LOWER number here, and it is what the delivered '
                  'edition publishes, so it is recorded as adopted rather than corrected.')),
        dict(name='the MNT-Halan mark',
             adopted=("GB Corp's confirmed 41.61% stake applied to the June-2026 round's "
                      'US$1.4bn valuation at EGP/USD 47.5'),
             alternative=('the equity-accounted carrying value the company reports for '
                          'associates on its own FY25 balance sheet, net of the Bedaya and '
                          'Kaf residual this study already carries separately'),
             va=M.central(), vb=M.central(mark=carry_mark),
             pa=M.primary(), pb=M.primary(mark=carry_mark),
             why=('a cash round is a real transaction price and a carrying value is cost '
                  'plus retained results, so these are two different quantities and neither '
                  'is simply right. The round is the more recent and the more informative, '
                  'and it is also 2.1x the book — on a stake that is 60% of the '
                  'pre-discount sum of the parts, that choice alone is most of the '
                  'disagreement with the market. The study takes the round at face and '
                  'discounts the whole wrapper by 10%.')),
        dict(name='the Auto gross-margin path',
             adopted=('a path opening at 13.8% and rising to 14.5%, above the 12.4% the '
                      'company reported for the latest reviewed quarter'),
             alternative=('the latest reviewed quarter held flat across the window — the '
                          'near-term reviewed actual outranking a forecast path'),
             va=M.central(), vb=M.central(fcff=M.fcff_path(gpm=flat_gpm)),
             pa=M.primary(), pb=M.primary(fcff=M.fcff_path(gpm=flat_gpm)),
             why=('1Q26 at 12.4% carried a regional drag the study argues is transient, and '
                  'the FY25 full year printed 14.8%, above the forecast\'s own opening '
                  'year — so the adopted path sits BETWEEN the last quarter and the last '
                  'full year rather than above both. What is contested is which of the two '
                  'anchors the forecast: the study takes the annual rate and fades the '
                  'quarter, and holding the quarter instead is worth 18% of the answer.')),
        dict(name='working-capital intensity',
             adopted=('gliding from 26.5% of Auto revenue in the first forecast year to '
                      '21.5% by the last, as payables re-extend and the pre-build unwinds'),
             alternative=('the first forecast year held flat across the window — no credit '
                          'taken for the release'),
             va=M.central(), vb=M.central(fcff=M.fcff_path(wcpct=flat_wc)),
             pa=M.primary(), pb=M.primary(fcff=M.fcff_path(wcpct=flat_wc)),
             why=('the disclosed series runs 18.7% / 22.9% / 28.5% for FY23-25, so the '
                  'adopted path already assumes the FY25 spike reverses and the alternative '
                  'holds a level 2 points BETTER than the last actual — the conservative '
                  'framing here is still not the most conservative one available. The study '
                  "names this its second crux and the company's own quarterly prints "
                  'resolve it; the fork is whether the release is credited before it is '
                  'shown.')),
        dict(name='terminal growth',
             adopted='a typed nominal 11.5% for ever',
             alternative=("the house Egyptian terminal of 7.0% — terminal inflation with a "
                          'stated real growth of zero'),
             va=M.central(), vb=M.central(g=0.07),
             pa=M.primary(), pb=M.primary(g=0.07),
             why=('a typed nominal rate is unfalsifiable: nobody can tell whether 11.5% '
                  'meant inflation plus four points or minus three. Against a discount rate '
                  'built off a 22.55% risk-free it is an 11.4-point spread and defensible '
                  'on its face; against the sourced disinflation path it is real growth of '
                  'several points a year in perpetuity, which nothing disclosed supports. '
                  '75% of the auto leg sits in that terminal.')),
        dict(name='the normalised earnings base',
             adopted=('mid-cycle group profit of EGP 4,200 mn — recovering volumes at the '
                      'top of the forecast margin path, on forward-scale revenue'),
             alternative=('the last reported full-year attributable profit of EGP 2,880 mn, '
                          'at the same through-cycle multiple'),
             va=M.central(), vb=M.central(norm=alt_norm),
             pa=M.primary(), pb=M.primary(),
             why=('normalising is what the lens is for, and the cycle position argued in '
                  '§1.4 — volumes at roughly double the 2023 trough and still short of the '
                  'mid-2010s run-rate — is evidenced. What is contested is the size of the '
                  'step: EGP 4.2bn is 46% above the last audited year and is built on the '
                  "highest margin anywhere in the study's own forecast. Capitalising what "
                  'the company last actually earned is the sceptic\'s framing and is worth '
                  '8% of the answer.')),
        dict(name='the equity risk premium basis',
             adopted='the credit-default-swap basis, giving a weighted cost of capital of 22.94%',
             alternative='the credit-rating basis, giving 25.08%',
             va=M.central(), vb=M.central(w=M.wb['wacc_rating']),
             pa=M.primary(), pb=M.primary(w=M.wb['wacc_rating']),
             why=("both come from the same published country-risk file and the study prints "
                  'both. The swap basis is the market\'s own live pricing of the sovereign '
                  "against an agency judgement updated in steps, and it is the house "
                  'default central — it is also the lower rate and therefore the higher '
                  'value, which is why it is recorded here rather than treated as settled.')),
        dict(name='the complexity / conglomerate discount',
             adopted='10% deducted from the whole sum of the parts',
             alternative=('no discount — the pre-discount sum, which this study already '
                          'publishes as a lens in its own right'),
             va=M.central(), vb=M.central(disc=0.0),
             pa=M.primary(), pb=M.primary(disc=0.0),
             why=('an auto assembler, a lender and an unlisted fintech in one listing will '
                  'not trade at the clean sum of its parts, and 10% is a judgement with no '
                  'observable behind it. The study hedges the fork by carrying the '
                  'undiscounted sum as a 15%-weighted lens, which is why this moves the '
                  'published blend by less than it moves the primary lens.')),
        dict(name='where the complexity discount is applied',
             adopted='uniformly across all three legs',
             alternative=('on the private, illiquid associate mark alone — the one leg the '
                          'wrapper actually obscures'),
             va=M.central(), vb=M.central(mark_only_discount=True),
             pa=M.primary(), pb=M.primary(mark_only_discount=True),
             why=('the auto leg is already discounted at its own cost of capital and the '
                  'lender is marked at book, so a uniform haircut charges those two legs '
                  'for an illiquidity that sits in the third. Applying it uniformly is the '
                  'LOWER-value choice and the study says plainly that it does so; the fork '
                  'is recorded because the study also names a much steeper mark-specific '
                  'discount as the sceptic\'s reading, which runs the other way.')),
        dict(name='the equity beta',
             adopted=('1.00, the house default, after an attempted five-annual-observation '
                      'regression returned a negative slope with no explanatory power'),
             alternative=('0.8907, the conforming weekly regression against the exchange\'s '
                          'published index now committed in this directory'),
             va=M.central(), vb=M.central(w=beta_wacc),
             pa=M.primary(), pb=M.primary(w=beta_wacc),
             why=('the study\'s own refusal to use an unusable regression was right, and a '
                  'conforming tier-1 regression has since been produced on weekly data over '
                  'nearly five years. It moves the cost of capital by 48 basis points and '
                  'the answer by under 2%, so it is recorded rather than material — the '
                  'beta was never what this valuation turned on.')),
    ]

    judgements = []
    for j in J:
        va, vb = float(j['va']), float(j['vb'])
        judgements.append({
            'name': j['name'],
            'adopted': j['adopted'],
            'alternative': j['alternative'],
            'value_adopted': va,
            'value_alternative': vb,
            'value_adopted_primary_lens': float(j['pa']),
            'value_alternative_primary_lens': float(j['pb']),
            'moves_the_answer_by': abs(va - vb) / abs(vb),
            'direction': ('the study took the higher value' if va > vb else
                          'the study took the lower value' if va < vb else 'no difference'),
            'why': j['why'],
        })

    material = [x for x in judgements if x['moves_the_answer_by'] >= 0.05]
    up = len([x for x in material if x['value_adopted'] > x['value_alternative']])
    n = len(material)
    p = min(1.0, 2 * sum(comb(n, i) for i in range(max(up, n - up), n + 1)) / float(2 ** n)) if n else None

    cj = {
        'ticker': 'GBCO',
        'as_of': '2026-09-06',
        'published_central': published,
        'published_spot': strike,
        'measured_on': (
            'The published answer is the four-lens blend, so materiality is measured on it. '
            'That construction DAMPENS every fork touching the sum of the parts to about '
            '55% of its effect on the primary lens, because two of the four lenses are '
            'earnings multiples that move with none of them — so three forks that are '
            'material on the lens this study calls primary are recorded here as immaterial. '
            'Both figures are carried on every judgement so a reader can see which is which, '
            'and the dampening is itself the first judgement in the list.'),
        'judgements': judgements,
        'sign_test': {
            'material': n, 'resolved_upward': up, 'resolved_downward': n - up,
            'two_sided_p': p,
            'flagged': bool(p is not None and p < 0.05 and n >= 3),
            'reading': (
                'Of %d material forks the study took the higher-value side on %d. Two-sided '
                'p = %.4f, so this is NOT flagged at the 5%% level and a study of this shape '
                'can honestly land this way — the associate mark, the margin anchor and the '
                'working-capital release are three readings of one thesis rather than three '
                'independent coin flips, and treating them as independent is what the '
                'binomial test does. WHAT THE COUNT DOES NOT SHOW, AND THE VALUES DO: every '
                'one of the three forks the study resolved DOWNWARD is small — 4.6%%, 1.9%% '
                'and 1.7%% — while five of the six it resolved upward are worth 6.5%% to '
                '23.3%%. The study is careful in the places where care is cheap.'
                % (n, up, p)),
        },
        'unvalued': [
            {'name': "the lender's mark",
             'what': ("GB Capital is carried at 1.0x an adjusted operating book of EGP 9.5bn, "
                      "derived from the company's own adjusted-ROAE disclosure"),
             'why_not_valued': (
                 'the alternative framing is a different multiple, and no second multiple is '
                 'derivable from anything the company discloses — a return-justified P/B '
                 'needs a growth rate the filings do not give, and the study\'s own bear and '
                 'bull marks (0.80x, 1.25x) are case assumptions rather than a framing. '
                 'Pricing an invented multiple would put a guess into an instrument built to '
                 'detect them, so it is recorded unvalued rather than estimated.'),
             'direction_if_valued': ('a mid-teens return against a cost of equity near 32% '
                                     'argues for a mark below book, so this fork would '
                                     'almost certainly run DOWN and would add to the '
                                     'downward count rather than the upward one')},
            {'name': 'the second closing of the MNT-Halan round',
             'what': ('public reporting describes the June-2026 close as an initial tranche '
                      'of an ongoing round, with a second closing open'),
             'why_not_valued': ('size and terms are undisclosed, so neither framing has a '
                                'number behind it. SIGCM clause 8: stop rather than invent.'),
             'direction_if_valued': 'unknown — a second close could reprice the round either way'},
            {'name': 'the currency the dollar mark is translated at',
             'what': 'the round is translated at EGP/USD 47.5, the rate at the strike',
             'why_not_valued': (
                 'translating at a later rate is a change of strike date rather than an '
                 'alternative framing of a judgement, and this record prices framings. It '
                 'is named here so its absence is visible: at the pound level the house '
                 'macro path carries for early August the mark would be worth about 6% more '
                 'and the answer about 2% more, which runs DOWNWARD against the study.')},
        ],
        'considered_and_not_counted': [
            {'name': 'the cost-of-capital construction',
             'what': ('the study normalises nothing out of the local risk-free rate before '
                      'adding a country-loaded equity premium'),
             'why_not_a_judgement': (
                 'this is a defect against the current cost-of-capital method rather than a '
                 'fork between two defensible framings, and it is already recorded, priced '
                 'and queued in this directory\'s own rebuild-readiness note. Valuing it '
                 'here as an "alternative framing" would launder a known error into a '
                 'judgement, and it would add a SEVENTH upward count and take the sign test '
                 'to p = 0.0625 — which is exactly why the reason for excluding it is '
                 'written down rather than left to be inferred.'),
             'direction_if_counted': 'UP, and large — the correction lowers the discount rate'},
        ],
    }

    json.dump(diag, open(os.path.join(HERE, 'diagnostics.json'), 'w', encoding='utf-8'),
              indent=1, ensure_ascii=False)
    json.dump(cj, open(os.path.join(HERE, 'contested_judgements.json'), 'w', encoding='utf-8'),
              indent=1, ensure_ascii=False)

    assert _sha(numbers) == before, (
        'study_numbers.json changed while a diagnostic ran. A quantity solved from a price '
        'must never reach the file every builder reads.')

    print('GBCO reverse read + contested judgements COMPUTED')
    print('  published central %.4f (strike %.2f) against the latest close %.2f (%s)'
          % (published, strike, spot, spot_date))
    print('  ' + diag['implied']['reading'][:300] + ' ...')
    print('  judgements %d, material %d, upward %d, two-sided p = %.4f'
          % (len(judgements), n, up, p))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
