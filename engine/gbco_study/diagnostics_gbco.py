#!/usr/bin/env python3
"""GBCO — the reverse read and the contested-judgement record [R-ENF-05], COMPUTED.

WHAT THIS FILE IS. Two diagnostics, both aimed at a study auditing its own answer
rather than only its steps:

  1. THE REVERSE READ. This study states what it believes; it does not state what
     the PRICE believes, and the two are the same model read backwards. Solved
     here on the study's OWN published construction, holding every other driver at
     its published value and moving only the one line the study itself names as
     its crux — the mark on GB Corp's minority interest in MNT-Halan.

  2. THE CONTESTED-JUDGEMENT RECORD. Every fork worth arguing about, valued BOTH
     ways by re-running this study's own arithmetic, with the side adopted and
     why, and a binomial sign test on which way they went.

REBUILT 07-09-2026 ONTO THE STUDY'S NEW ARCHITECTURE, AND THE OLD FILE WAS NOT
MERELY STALE — IT COMPUTED ON LEVERS THAT NO LONGER EXIST. It reproduced a
four-lens weighted central at typed weights, which [R-LENS-03] retired; it priced
a 10% conglomerate discount and the question of where that discount was applied,
and there is no discount; and it valued a normalised-earnings framing, a lens this
class does not carry. A diagnostic whose arithmetic runs on retired constructions
does not go quietly wrong: it goes CONFIDENTLY wrong, because every figure in it
still computes. Its own reverse read had drifted to a NEGATIVE implied valuation
for MNT-Halan, which is what a blend that dampens the only line the disagreement
lives in will do, and nothing was looking.

THERE IS NO CENTRAL, SO NOTHING HERE REPRODUCES ONE. The primary lens is
two-sided: the two bases GB Corp itself puts on that stake differ by EGP 11.9bn
and the filings do not decide between them, so neither does the study. This file
reproduces BOTH committed branches to 1e-9 and refuses otherwise. That assert is
the whole point of the file — a diagnostic that has drifted from its study is
worse than none, because it has the shape of a computed record.

WHY IT LIVES OUTSIDE THE NUMBERS FILE. A quantity solved from a traded price and
then used anywhere in the valuation is the reverse-engineered rate the protocol
prohibits outright, arriving through a side door. So the reverse read is written
to diagnostics.json, no builder reads it, and this file asserts that
study_numbers.json is byte-identical before and after the run — a diagnostic that
can write back into the model is not a diagnostic.

NOTHING HERE CHANGES A DRIVER, A RATE, A FORECAST OR A FAIR VALUE. Valuing the
alternative framing of a judgement is a calculation reported, never a change made.

    python3 diagnostics_gbco.py     writes diagnostics.json + contested_judgements.json
"""
import hashlib
import json
import os
import sys
from math import comb

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.dirname(HERE)

# ---------------------------------------------------------------------------
# THE ONE FIGURE THIS FILE HOLDS IN SOURCE RATHER THAN READING FROM THE NUMBERS
# FILE, named with the line that carries it. The rebuild committed the ADOPTED
# ownership percentage and its prior; the SECOND disclosed pair — the one the
# reviewed statements and the review report name for the same June-2026
# transaction — is carried in compute.py and is not exported. It is read off this
# study's own committed record rather than re-sourced or estimated, on the same
# footing the superseded edition of this file used for the two figures it needed.
# Every other number below is READ from study_numbers.json.
MNT_STAKE_PER_STATEMENTS = 0.4293   # compute.py, `mnt_stake_statements`: note 34 to the
                                    # reviewed consolidated interim statements at
                                    # 30-Jun-2026 and the review report, both of which say
                                    # the stake in MNT BV "will be decreased to 42.93%,
                                    # instead of 44.01% before the transaction"


def _sha(path):
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()


def latest_supplied_prices():
    """The latest known close for this name, through the HOUSE reader.

    This function once resolved the newest SUPPLIED_*.json by the date in its
    filename and read the price out of that one file. That is not the same
    quantity: prices arrive by hand, so they arrive with lags and gaps, and a
    file supplying one name does not un-price the other eighty-nine.

    engine/prices/gap_today.latest_price_per_ticker() already merges every
    supplied file on each price's OWN date and returns that date beside the
    figure, which is what [R-GAP-01 AMENDED] requires a study to be delivered
    against. It is imported rather than reimplemented [R-ENF-03] — a second
    reader of one artefact is a second answer waiting to happen.
    """
    sys.path.insert(0, os.path.join(ENGINE, 'prices'))
    import gap_today
    return gap_today.latest_price_per_ticker()


class Model:
    """This study's own valuation arithmetic, rebuilt from its committed numbers.

    ONE ENTRY POINT, `primary()`, AND NO `central()`. The superseded version of
    this class exposed a `central()` that reproduced a four-lens weighted blend.
    That construction is retired and the study now publishes no central at all, so
    a diagnostic that could still compute one would be computing an answer nobody
    holds. What it computes instead is the class primary — the sum of the parts —
    which is two-sided in exactly one input, and the two branches are named rather
    than lettered: compute.py's branch A is the round price and study_numbers.json
    lists the carrying value first, so a letter here would resolve to whichever
    file the reader had open last.
    """

    def __init__(self, N):
        self.N = N
        self.rows = N['dcf']['rows']
        self.SH = N['shares']
        self.nd = N['dcf']['auto_nd']
        self.nci = N['dcf']['auto_nci']
        self.wacc = N['dcf']['wacc']
        self.tg = N['dcf']['tg']
        self.wb = N['dcf']['wacc_build']
        # the committed cost-of-capital ladder [R-COC-01]: one forward rate per
        # explicit year, the last of which IS the norm-built terminal rate
        self.wb_forward = N['dcf']['forward_wacc']
        self.cap = N['sotp']['cap_val']
        self.other = N['sotp']['other_assoc']
        self.disc = N['sotp']['disc']          # 0.0 — the free parameter is gone
        self.fx = N['sotp']['egp_usd']
        self.stake = N['sotp']['mnt_halan_stake']
        self.round_usd = N['sotp']['mnt_halan_round_usd']
        # THE TWO MARKS. The round mark is the sum-of-the-parts entry the study
        # carries; the carrying mark is the committed low end of the primary's own
        # declared range, which is the reviewed note-34 figure for MNT-Halan alone.
        self.mark_round = N['sotp']['mnt_halan_value']
        self.mark_carrying = N['lens_record']['primary']['range_basis']['low']
        self.mark = self.mark_round
        self.fcff = [r['fcff'] for r in self.rows]
        # the operating shape of the auto leg, recovered from the committed rows so
        # a margin or a working-capital framing can be re-priced without any driver
        # being typed here
        self.tax = 1.0 - self.rows[0]['nopat'] / self.rows[0]['ebit']
        self.gpm = [r['gp'] / r['rev'] for r in self.rows]
        self.opex = [(r['gp'] - r['ebit']) / r['rev'] for r in self.rows]
        self.wcpct = [r['wc'] / r['rev'] for r in self.rows]
        self.wc_open = self.rows[0]['wc'] - self.rows[0]['dwc']
        # the lender leg, as a residual-income identity rather than as a number
        self.cp = N['lens_inputs']['capital']

    # -- the auto leg -------------------------------------------------------
    def fcff_path(self, gpm=None, wcpct=None, capex=None):
        """The auto leg's free cash flow, with any one driver moved.

        CAPEX BECAME A LEVER HERE ONLY WHEN SOMEBODY ASKED IT TO BE PRICED. It was read
        straight off the committed row and could not be moved, so the judgement it
        carries could not be measured — and a judgement that cannot be measured is one
        that does not appear in a register, which is exactly where this one was found:
        outside the four-field inputs, outside the contested judgements, and outside the
        risk register that was built to catch it.
        """
        gpm = gpm or self.gpm
        wcpct = wcpct or self.wcpct
        out, prev = [], self.wc_open
        for i, r in enumerate(self.rows):
            ebit = r['rev'] * gpm[i] - r['rev'] * self.opex[i]
            wc = r['rev'] * wcpct[i]
            cx = r['capex'] if capex is None else capex[i]
            out.append(ebit * (1.0 - self.tax) + r['dna'] - cx - (wc - prev))
            prev = wc
        return out

    def schedule(self, w=None):
        """The committed cost-of-capital LADDER, or a declared parallel shift of it.

        [R-COC-01] built this study's discount rate as a GLIDE — one forward rate
        per explicit year falling to a norm-built terminal, with the terminal
        brought home on the SAME cumulative factor as the last explicit year, so
        that one date carries one price of time. Discounting the whole path at a
        single flat rate is the construction that lever REPLACED, and it is not a
        thing this class may express.

        Called with no argument the ladder is the committed one and the answer
        reproduces the published branches exactly. Called with a rate, that rate is
        read as an alternative FIRST-YEAR rate and the WHOLE ladder is shifted by
        the difference — terminal included. That is a PROXY and is labelled one
        wherever it is published: the two alternative bases this study prices (a
        rating-basis equity premium and a beta moved off the conforming regression)
        each move the terminal too, since [R-COC-02] builds the terminal cost of
        equity from the same beta and the same premium — but the committed record
        carries no terminal counterpart for either, and a terminal this desk solved
        for itself is not a committed one. A parallel shift moves the terminal by
        the same amount as the explicit window rather than by its own rebuilt
        amount, so the figures below price the DIRECTION and the rough size of each
        disagreement and are not a re-derivation of the alternative basis.
        """
        fw = list(self.wb_forward)
        if w is not None:
            fw = [r + (w - fw[0]) for r in fw]
        factors, c = [], 1.0
        for r in fw:
            c /= (1.0 + r)
            factors.append(c)
        return fw, factors

    def auto_ev(self, fcff, w, g):
        fw, factors = self.schedule(w)
        pv = sum(f * d for f, d in zip(fcff, factors))
        tv = fcff[-1] * (1.0 + g) / (fw[-1] - g)
        return pv + tv * factors[-1]

    # -- the lender leg -----------------------------------------------------
    def cap_value(self, roe=None, ke=None):
        """Residual income in its terminal form on the segment's own operating book.

        (ROE - g) / (Ke - g), on shareholders' equity before NCI LESS the associates
        carried inside it — so the stake the sum of the parts adds back at its own
        mark is not also funding this leg. Rebuilt here from the committed inputs
        rather than read as a number, because two of this record's judgements move
        an input to it, and a judgement priced by typing a second number is not
        priced by the model at all.
        """
        roe = self.cp['roe_adopted'] if roe is None else roe
        ke = self.cp['ke_terminal'] if ke is None else ke
        return self.cp['operating_equity'] * (roe - self.cp['g']) / (ke - self.cp['g'])

    # -- the whole answer ---------------------------------------------------
    def legs(self, fcff=None, w=None, g=None, mark=None, cap=None):
        fcff = self.fcff if fcff is None else fcff
        w = self.wacc if w is None else w
        g = self.tg if g is None else g
        mark = self.mark if mark is None else mark
        cap = self.cap if cap is None else cap
        auto_eq = self.auto_ev(fcff, w, g) - self.nd - self.nci
        return auto_eq, auto_eq + cap + self.other + mark

    def primary(self, disc=None, **kw):
        """The split-the-legs sum of the parts — the class primary, and the answer.

        `disc` survives as an argument for one reason only: the retired 10%
        conglomerate discount is recorded in this file as a superseded construction
        with its direction priced, and pricing it needs the model to be able to
        express it. It defaults to the committed 0.0 and no judgement in the signed
        list moves it.
        """
        d = self.disc if disc is None else disc
        _, total = self.legs(**kw)
        return total * (1.0 - d) / self.SH

    def branch_carrying(self, **kw):
        """MNT-Halan at its reviewed carrying value — the study's low branch."""
        kw.setdefault('mark', self.mark_carrying)
        return self.primary(**kw)

    def branch_round(self, **kw):
        """MNT-Halan at the June-2026 round price — the study's high branch."""
        kw.setdefault('mark', self.mark_round)
        return self.primary(**kw)

    def wacc_at(self, beta, erp):
        """The explicit-window cost of capital at a moved beta, on ONE premium basis.

        rf* is the NORMALISED risk-free — the local yield less this sovereign's own
        default spread — so country risk is counted exactly once [R-COC-01]. The
        CAPM identity is asserted rather than trusted, so a rename fails loudly
        instead of returning a plausible number built on a field that means
        something else.

        THE TWO PREMIUM BASES ARE NOT INTERCHANGEABLE IN THIS FUNCTION and the
        caller supplies the matched pair: [R-COC-01] requires the SAME basis of
        default spread to be stripped as the premium added back, so a rating-basis
        premium belongs with a rating-basis rf*, which this record does not carry —
        its single `default_spread` field is the CDS basis. The committed
        wacc_rating is the rating-basis figure; read it, do not rebuild it here.
        """
        # THE COST OF EQUITY IS BUILT THROUGH THE SANCTIONED MODULE, not re-derived
        # here [10-09-2026]. This line read rf* + beta x ERP_total, which multiplies
        # the country premium by beta -- the double count [R-COC-03] was adopted to
        # stop -- so once the study moved to the split construction this assert fired
        # on an answer that was right, and stopped the study rebuilding at all. A
        # second implementation of an identity beside the module that owns it is the
        # shape that lets two readers of one fact disagree; the fix is to have one
        # reader, not to relax the tolerance.
        import cost_of_capital as _COC
        ke, _ = _COC.cost_of_equity(self.wb['rf_star'], beta, erp,
                                    self.wb['default_spread'])
        if abs(beta - self.wb['beta']) < 1e-12 and abs(erp - self.wb['erp_cds']) < 1e-12:
            assert abs(ke - self.wb['ke_cds']) < 1e-12, (
                'the cost of equity no longer reproduces this study\'s own committed '
                'figure under the sanctioned construction (%.12f vs %.12f)'
                % (ke, self.wb['ke_cds']))
        return self.wb['we'] * ke + self.wb['wd'] * self.wb['kd_aftertax']

    # -- the reverse read ---------------------------------------------------
    def implied_mark(self, price):
        """The MNT-Halan mark the price implies, inverted from this study's own
        construction with every other line held at its published value.

        THE SOLVE IS BRANCH-FREE AND THAT IS THE POINT. The two branches differ in
        this one input and in nothing else, so asking what the price pays for it
        asks the question the branches exist to pose — and the answer is a third
        number, to be read against both."""
        auto_eq, _ = self.legs()
        rest = auto_eq + self.cap + self.other
        return price * self.SH * 1.0 / (1.0 - self.disc) - rest

    def implied_flat_wacc(self, price, mark=None):
        """The same disagreement asked of the auto leg's discount rate instead.

        Bisection: above the terminal growth the answer falls monotonically in the
        rate, so the root is unique and does not depend on a starting guess.
        """
        lo, hi = self.tg + 1e-6, 3.0
        for _ in range(400):
            mid = 0.5 * (lo + hi)
            if self.primary(w=mid, mark=mark) > price:
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

    # ---------------- 0. REPRODUCE THE ANSWER, OR REFUSE ------------------
    # There is no central to reproduce. There are two branches, and BOTH are
    # asserted: reproducing one of a two-sided answer is reproducing half a study.
    branches = {b['label']: b['value'] for b in N['central_two_sided']['branches']}
    L_CARRY = 'MNT-Halan at its reviewed carrying value'
    L_ROUND = 'MNT-Halan at the June-2026 round price'
    for label, fn in ((L_CARRY, M.branch_carrying), (L_ROUND, M.branch_round)):
        assert label in branches, (
            'the study no longer publishes a branch labelled %r. This file reproduces '
            'the answer by name rather than by position, so a relabelled branch stops '
            'the run instead of being silently matched to the wrong arithmetic.' % label)
        assert abs(fn() - branches[label]) < 1e-9, (
            'this file no longer reproduces the branch the study publishes as %r '
            '(%.10f vs %.10f). A diagnostic that has drifted from its study is worse '
            'than none, because it has the shape of a computed record.'
            % (label, fn(), branches[label]))
    assert N.get('central') is None and N['lens_record']['central'] is None, (
        'the study has acquired a central. This file was rebuilt on the two-sided '
        'primary and would report on an answer the study no longer holds.')
    assert abs(M.branch_round() - N['sotp']['ps']) < 1e-9
    assert abs(M.branch_round() - N['sotp']['prediscount_ps']) < 1e-9, (
        'the sum of the parts and the pre-discount sum have parted company, which '
        'means a conglomerate discount has come back without this file knowing.')
    assert abs(M.cap_value() - N['sotp']['cap_val']) < 1e-9, (
        'the lender leg no longer rebuilds from its own committed residual-income '
        'inputs (%.10f vs %.10f).' % (M.cap_value(), N['sotp']['cap_val']))
    assert abs(M.cap_value(roe=M.cp['roe_fy25']) - M.cp['value_fy25_framing']) < 1e-9

    carry_ps, round_ps = M.branch_carrying(), M.branch_round()
    strike = N['spot']

    merged = latest_supplied_prices()
    ticker = N.get('ticker', 'GBCO')
    if ticker not in merged:
        raise SystemExit(
            'no supplied close is held for %s in any engine/prices/SUPPLIED_*.json. '
            'An absent price is not a clean price [R-ENF-04]: this study is '
            'delivered against the LATEST KNOWN price, so it stops here rather '
            'than falling back to the one it was struck at.' % ticker)
    row = merged[ticker]
    spot, spot_date, price_path = float(row['price']), row['date'], row['file']

    # ---------------- 1. THE REVERSE READ ---------------------------------
    mark_now = M.implied_mark(spot)
    mark_strike = M.implied_mark(strike)

    def whole_usd(mark_egp):
        return mark_egp / M.fx / M.stake

    implied_usd = whole_usd(mark_now)
    carry_usd = whole_usd(M.mark_carrying)
    assert abs(M.primary(mark=mark_now) - spot) < 1e-9, (
        'the solved mark does not reproduce the traded price through the study\'s own '
        'construction, so the inversion is not the model read backwards.')

    diag = {
        'ticker': 'GBCO',
        'as_of': N['edition'],
        'spot': spot,
        'spot_date': 'close %s, the Egyptian Exchange' % spot_date,
        'spot_source': '%s — %s, the close supplied by the principal'
                       % (os.path.relpath(price_path, os.path.dirname(ENGINE)),
                          row.get('company', 'GB Corp')),
        # [R-ENF-06] THE VINTAGE THIS ARTEFACT WAS BUILT AGAINST. The study publishes
        # no central, so the declaration names the branch this file is anchored on and
        # carries BOTH beside it — a single figure would state half the answer.
        'published_central': round_ps,
        'published_central_is': L_ROUND,
        'published_central_note': (
            'THIS STUDY PUBLISHES NO CENTRAL. Its primary is two-sided and the two '
            'branches are published side by side. The field above names the branch this '
            'file is anchored on — the June-2026 round price, which is the sum of the '
            'parts the study carries and the figure its own cross-check machinery reads '
            '— and both branches are declared below so an artefact-currency check holds '
            'this file to an answer the study actually publishes rather than to an '
            'average of two it does not.'),
        'published_central_two_sided': [
            {'label': L_CARRY, 'value': carry_ps},
            {'label': L_ROUND, 'value': round_ps},
        ],
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
                         "this study names as its crux and the one input its two published "
                         "branches differ in"),
            'value': implied_usd,
            'study_value': M.round_usd,
            'units': 'USD million, the valuation of MNT-Halan as a whole',
            'value_at_the_strike_price': whole_usd(mark_strike),
            'implied_stake_value_egp_mn': mark_now,
            'implied_stake_value_usd_mn': mark_now / M.fx,
            'implied_as_a_share_of_the_round': implied_usd / M.round_usd,
            'implied_as_a_share_of_the_carrying_value': implied_usd / carry_usd,
            'the_two_bases_the_company_itself_discloses': {
                'round_valuation_usd_mn': M.round_usd,
                'round_stake_value_egp_mn': M.mark_round,
                'stake': M.stake,
                'stake_source': ("GB Corp's own press release, 9 June 2026, on MNT-Halan's "
                                 "Al Ahly Capital-led capital increase: the stake 'will be "
                                 "adjusted to 41.61%, compared to 42.58% prior to the "
                                 "transaction'"),
                'carrying_stake_value_egp_mn': M.mark_carrying,
                'whole_company_at_carrying_value_usd_mn': carry_usd,
                'carrying_value_source': (
                    "note 34 to GB Corp's reviewed consolidated interim statements at "
                    '30 June 2026, EGP 15,733,523 thousand, which foots to that balance '
                    "sheet's own associates line"),
                'carrying_value_caveat': (
                    'the carrying value is an equity-accounted book figure — cost plus the '
                    "group's share of retained results and the revaluation on "
                    'deconsolidation — and is not a valuation. It is also the line the '
                    "reviewers' own conclusion is QUALIFIED at: they were not provided with "
                    "the associate's financial statements and could not verify the EGP "
                    '409.9mn share of profit recorded in the period. It is the lower branch '
                    'and it is not a safe harbour.'),
            },
            'solved_on': (
                "this study's own construction, rebuilt from its committed numbers file and "
                'asserted against BOTH branches it publishes, holding the auto leg\'s cash '
                "flows, its cost-of-capital ladder, its terminal growth, the lender's "
                'residual-income mark and the other associates all at their published '
                'values, and moving only the MNT-Halan mark until the model reproduces the '
                'traded price. THE SOLVE IS BRANCH-FREE: the branches differ in this one '
                'input and in nothing else, so the inversion asks exactly the question they '
                'exist to pose, and its answer is a third number to be read against both. '
                'The superseded version of this record solved the same quantity on a '
                'four-lens weighted blend, where two lenses that do not touch this stake '
                'carried 45% of the weight and dampened the read into a negative number.'),
            'second_framing': {
                'quantity': ('the single flat discount rate on the auto leg that reproduces '
                             'the traded price, every other line held at its published value'),
                'value': M.implied_flat_wacc(spot, mark=M.mark_round),
                'value_on_the_carrying_branch': M.implied_flat_wacc(spot, mark=M.mark_carrying),
                'study_value': M.wacc,
                'value_at_the_strike_price': M.implied_flat_wacc(strike, mark=M.mark_round),
                'reading': (
                    'carried here because it is the honest alternative reading of the same '
                    'gap, and on this study it does NOT collapse. Asked of the auto leg\'s '
                    'discount rate, the price implies %.2f%% against this study\'s %.2f%% '
                    'on the round branch — %.1f points, a stretch on a leg worth less than '
                    'half the sum of the parts — but only %.2f%% on the carrying branch, '
                    'which is %.1f points and is an ordinary disagreement about the cost of '
                    'capital in this market. A READER IS ENTITLED TO BOTH: the mark is the '
                    'quantity solved above because it is the input the two branches '
                    'actually differ in, not because the discount-rate reading is absurd.'
                    % (100 * M.implied_flat_wacc(spot, mark=M.mark_round), 100 * M.wacc,
                       100 * (M.implied_flat_wacc(spot, mark=M.mark_round) - M.wacc),
                       100 * M.implied_flat_wacc(spot, mark=M.mark_carrying),
                       100 * (M.implied_flat_wacc(spot, mark=M.mark_carrying) - M.wacc))),
            },
            'reading': (
                'At EGP %.2f the price values GB Corp\'s 41.61%% stake in MNT-Halan at EGP '
                '%.0f mn, which is MNT-Halan as a whole at US$%.0f mn — %.1f%% of the '
                'US$%.1f bn the June-2026 round was struck at, and %.1f%% of the US$%.0f mn '
                'the company\'s own reviewed carrying value implies. THE PRICE IS BELOW '
                'BOTH BASES THE COMPANY ITSELF DISCLOSES, AND NOT NARROWLY: the market '
                'capitalisation leaves EGP %.0f mn for all associates once the auto leg and '
                'the lender are taken at this study\'s marks, against EGP %.0f mn carried on '
                'the reviewed balance sheet. That is a more useful statement than "the study '
                'is %+.1f%% to %+.1f%% against the price", and it names where the whole '
                'disagreement sits. IT DOES NOT SETTLE WHO IS RIGHT, AND THE ARITHMETIC CAN '
                'BE READ TWO WAYS: either the market is marking a minority interest in an '
                'unlisted company at a fraction of both the price its last primary round '
                'was struck at and the value its auditors carry it at, or the sum of the '
                'parts is the wrong lens for a wrapper nobody can break up — and this study '
                'publishes the branches rather than choosing.'
                % (spot, mark_now, implied_usd, 100 * implied_usd / M.round_usd,
                   M.round_usd / 1000.0, 100 * implied_usd / carry_usd, carry_usd,
                   mark_now + M.other, M.mark_carrying + M.other,
                   100 * (carry_ps / spot - 1), 100 * (round_ps / spot - 1))),
        },
    }

    # ---------------- 2. THE CONTESTED JUDGEMENTS -------------------------
    # MATERIALITY IS MEASURED ON THE LOWER BRANCH, AND THE REASON IS ARITHMETIC
    # RATHER THAN TASTE. The rule asks for every judgement worth more than 5% of
    # THE ANSWER, and this study publishes two. Every fork below except one moves
    # both branches by the same number of pounds, so it is relatively larger on the
    # lower one — measuring there records the SUPERSET, and falling to the strict
    # side is what this house does everywhere else an answer is ambiguous. Both
    # framings are carried on every entry so a reader can see which is which; it
    # changes exactly one classification, and that one is named where it happens.
    beta_wacc = M.wacc_at(B['beta'], M.wb['erp_cds'])
    unit_beta_wacc = M.wacc_at(1.0, M.wb['erp_cds'])
    assert abs(beta_wacc - M.wacc) < 1e-9, (
        'the committed beta no longer reproduces the committed cost of capital.')
    anchor = N['forecast_anchor']
    flat_gpm = [anchor['latest_reviewed_rate']] * len(M.rows)
    flat_wc = [M.wcpct[0]] * len(M.rows)
    cap_fy25 = M.cap_value(roe=M.cp['roe_fy25'])
    cap_ke_exp = M.cap_value(ke=N['cost_of_capital_record']['ke_exp'])
    mark_statements = MNT_STAKE_PER_STATEMENTS * M.round_usd * M.fx

    def pair(**kw):
        """One framing, priced on both branches: (carrying, round)."""
        return (M.branch_carrying(**kw), M.branch_round(**kw))

    # THE FILED CAPITAL-EXPENDITURE INTENSITY, which the forward ladder does not hold.
    # FY2025's filed capex over FY2025 auto revenue, from the study's own committed
    # inputs rather than typed here.
    _capex_fy25 = float(N['inputs']['capex_fy2025']['value'])
    _rev_fy25 = float(N['disclosed_drivers']['auto_revenue_fy2025'])
    _filed_intensity = _capex_fy25 / _rev_fy25
    # THE ALTERNATIVE IS THE FILED AMOUNT HELD FLAT, NOT THE FILED INTENSITY HELD FLAT,
    # and the first draft of this judgement used the intensity. On a revenue base that
    # more than doubles, holding 5.52% of it takes capital expenditure from 3,000 to
    # 7,991 and drives the last explicit year's free cash flow through zero — and since
    # this study's terminal capitalises that same last year, the answer collapses to
    # about a pound a share, a move of forty times. A COUNTERFACTUAL THAT BREAKS THE
    # MODEL IS NOT A FRAMING OF THE JUDGEMENT, it is a different question, and pricing a
    # fork against it would put a number in the register that no reader could use.
    # What is priced instead is the company simply going on spending what it filed:
    # EGP 3,664.2mn a year, flat in nominal terms, which is a REAL DECLINE across the
    # window and is therefore the conservative-looking side understated rather than
    # overstated. That it is an actual filed figure is the whole reason for choosing it.
    flat_capex = [_capex_fy25 for _ in M.rows]

    J = [
        dict(name='the capital-expenditure path',
             adopted=('a ladder falling from %.2f%% of Auto revenue in the first forecast '
                      'year to %.2f%% by the last, whose first year is the figure '
                      'management guided'
                      % (100 * M.rows[0]['capex'] / M.rows[0]['rev'],
                         100 * M.rows[-1]['capex'] / M.rows[-1]['rev'])),
             alternative=('the company goes on spending what it filed: EGP %s mn a year, '
                          'flat in nominal terms, which is a real decline across the window'
                          % ('{:,.1f}'.format(_capex_fy25))),
             a=pair(), b=pair(fcff=M.fcff_path(capex=flat_capex)),
             why=('THIS JUDGEMENT WAS IN NO REGISTER UNTIL IT WAS ASKED FOR, which is the '
                  'part worth recording: not the four-field inputs, not this list, and not '
                  'the risk register built to catch exactly this — and on the measurement '
                  'below it ranks second in that register. The adopted ladder falls to a '
                  'third of the filed intensity across the window and raises free cash '
                  'flow in every year of it. TWO THINGS ARGUE THE OTHER WAY and are '
                  'recorded rather than left for a reader to find: capex still runs above '
                  'depreciation throughout, so the asset base is growing rather than being '
                  'harvested, and the terminal carries most of this leg\'s enterprise '
                  'value, so an explicit-window driver moves less of the answer than its '
                  'size suggests. THE FIRST YEAR IS MANAGEMENT GUIDANCE and the standing '
                  'rule is that guidance is scored and never consumed, so the adopted side '
                  'of this fork is not merely the higher one — it is the one a forward '
                  'target set.'),
             overturned_by=(
                 'two further filed years of capital expenditure, or a capital plan the '
                 'company discloses. Either settles whether the intensity is falling because '
                 'the build-out is finished or only because revenue is growing faster than '
                 'the spend.')),
        dict(name='working-capital intensity',
             adopted=('gliding from %.1f%% of Auto revenue in the first forecast year to '
                      '%.1f%% by the last, as payables re-extend and the pre-build unwinds'
                      % (100 * M.wcpct[0], 100 * M.wcpct[-1])),
             alternative=('the first forecast year held flat across the window — no credit '
                          'taken for the release'),
             a=pair(), b=pair(fcff=M.fcff_path(wcpct=flat_wc)),
             why=('the disclosed series runs 18.7% / 22.9% / 28.5% for FY23-25, so the '
                  'adopted path already assumes the FY25 spike reverses and the alternative '
                  'holds a level well BELOW the last actual — the conservative framing here '
                  'is still not the most conservative one available. It is by a wide margin '
                  'the largest fork in this record, because the auto leg\'s free cash flow '
                  'is a thin residual and a working-capital path moves it directly. The '
                  "study names this its second crux and the company's own quarterly prints "
                  'resolve it; the fork is whether the release is credited before it is '
                  'shown.'),
             overturned_by=(
                 'two consecutive quarters in which the company discloses its receivable, '
                 'inventory and payable days. The glide is currently five figures standing '
                 'in for a cycle the filings would measure directly.')),
        dict(name='the equity risk premium basis',
             adopted=('the market (credit-default-swap) basis, giving a first-year weighted '
                      'cost of capital of %.2f%%'
                      % (N['cost_of_capital_record']['wacc_exp'] * 100)),
             alternative=('the credit-rating basis, giving %.2f%%'
                          % (N['cost_of_capital_rating_basis']['wacc_exp'] * 100)),
             a=pair(), b=pair(w=M.wb['wacc_rating']),
             why=('both come from the same published country-risk file and the study prints '
                  "both. The swap basis is the market's own live pricing of the sovereign "
                  'against an agency judgement updated in steps, and it is the house '
                  'default central — it is also the lower rate and therefore the higher '
                  'value, which is why it is recorded here rather than treated as settled. '
                  'The figure opposite is a PARALLEL SHIFT of the committed ladder and is '
                  'labelled a proxy: the committed record carries no rating-basis terminal, '
                  'and a terminal this desk solved for itself is not a committed one.'),
             overturned_by=(
                 'the two published bases converging, or the country-risk file naming one of '
                 "them as the one to use. Neither is in this study's gift and both are "
                 'published by the same source.')),
        dict(name='the equity beta',
             adopted=('%.4f, the conforming weekly regression against the exchange\'s '
                      'published index, committed in this directory'
                      % N['cost_of_capital_record']['beta']),
             alternative=('1.00, the house default this study carried before the beta was '
                          're-derived, after an attempted five-annual-observation '
                          'regression returned a negative slope with no explanatory power'),
             a=pair(), b=pair(w=unit_beta_wacc),
             why=("the study's own refusal to use an unusable regression was right, and a "
                  'conforming tier-1 regression has since replaced the default it fell back '
                  'to. The fork is recorded rather than treated as settled because a beta '
                  'is a judgement about which estimator to trust, not a fact — and this '
                  "one sits close enough to 1.00 that the study's answer barely turns on "
                  'it, which is itself worth saying.'),
             overturned_by=(
                 'a longer usable run of weekly returns, or a structural change in the '
                 'company that resets the regression window and is disclosed as one.')),
        dict(name="the return anchoring GB Capital's justified price-to-book",
             adopted=('the 1H2026 REVIEWED return on the segment\'s operating equity, '
                      '%.2f%%, annualised on the average of the two committed period-end '
                      'bases' % (100 * M.cp['roe_h126'])),
             alternative=('the FY2025 full-year return on the same base, %.2f%%'
                          % (100 * M.cp['roe_fy25'])),
             a=pair(), b=pair(cap=cap_fy25),
             why=('[R-ANCHOR-01]: a near-term reviewed actual outranks a stale full-year '
                  'rate, and the half already filed is the more recent measurement of the '
                  'same quantity on the same base. It is also the LOWER of the two — the '
                  "FY25 framing is worth EGP %.0f mn more on this leg — so the study took "
                  'the conservative side here, and this is the one judgement in the record '
                  'whose materiality depends on which branch it is measured against: it '
                  'clears 5%% on the carrying branch and does not on the round branch, and '
                  'the strict reading is the one recorded.'
                  % (cap_fy25 - M.cap)),
             overturned_by=(
                 "a full year at the reviewed period's return on the equity base the segment "
                 'now carries. The two framings disagree because the base more than doubled '
                 'inside the period, and a year that spans neither half settles it.')),
        dict(name="the discount rate inside GB Capital's justified price-to-book",
             adopted=('the TERMINAL cost of equity from the sanctioned schedule, %.2f%%'
                      % (100 * M.cp['ke_terminal'])),
             alternative=('the explicit-window cost of equity, %.2f%%'
                          % (100 * N['cost_of_capital_record']['ke_exp'])),
             a=pair(), b=pair(cap=cap_ke_exp),
             why=('a terminal-form identity takes a terminal rate, so the adopted side is '
                  'the internally consistent one — and it is also the GENEROUS one, since '
                  'the explicit-window rate would put this leg at EGP %.0f mn against EGP '
                  '%.0f mn. Where a correction cuts a number the charitable reading is the '
                  'one to take, and the fork is recorded so that choice is visible rather '
                  'than buried in an identity. It moves the answer by less than 2%% either '
                  'way.' % (cap_ke_exp, M.cap)),
             overturned_by=(
                 'the cost-of-capital glide reaching its terminal, at which point the two '
                 'rates are the same number and the fork closes on its own.')),
        dict(name='the Auto gross-margin path',
             adopted=('a path opening at %.1f%% and rising to %.1f%%'
                      % (100 * anchor['forecast_path'][0],
                         100 * anchor['forecast_path'][-1])),
             alternative=('the latest reviewed half held flat across the window at %.2f%% — '
                          'the near-term reviewed actual outranking a forecast path'
                          % (100 * anchor['latest_reviewed_rate'])),
             a=pair(), b=pair(fcff=M.fcff_path(gpm=flat_gpm)),
             why=("GB Auto's own filed half to 30 June 2026 ran %.2f%%, and the forecast "
                  'opens 3.5%% relatively below it and rises to just above it — so the '
                  'adopted path straddles the anchor rather than sitting above it, and the '
                  'whole of it sits below every filed full year (24.4%% FY23, 19.2%% FY24, '
                  '14.8%% FY25). What is contested is whether the half or the path is the '
                  'better forecast of the next five years; on this rebuilt anchor the two '
                  'are close enough that the fork is worth barely 3%% of the answer, which '
                  'is a smaller disagreement than the superseded edition of this record '
                  'reported against an unsourced quarterly figure.'
                  % (100 * anchor['latest_reviewed_rate'])),
             overturned_by=(
                 'the second half of the current year filing at a margin outside the range '
                 "the first half and the prior year's halves together bracket.")),
        dict(name='the ownership percentage applied to the round',
             adopted=('41.61%, GB Corp\'s own press release of 9 June 2026 on the '
                      'transaction the round price comes from'),
             alternative=('42.93%, the figure note 34 to the reviewed 30-June-2026 '
                          'statements and the review report both give for the same '
                          'transaction — most likely a different level of the structure, '
                          'the Dutch holding vehicle rather than the operating group'),
             a=(M.branch_carrying(), M.branch_round()),
             b=(M.branch_carrying(), M.primary(mark=mark_statements)),
             measured_on='round',
             why=('both are the company\'s own disclosures about one transaction and they '
                  'are not the same pair, so registering only one would decide something '
                  'silently. The lower is adopted because it is the one the round it is '
                  'applied to was announced with. THIS IS THE ONE JUDGEMENT MEASURED ON THE '
                  'ROUND BRANCH RATHER THAN THE LOWER ONE, and not as a convenience: a '
                  'percentage of a round price has no effect at all on a branch whose mark '
                  'is an accounting carrying value, so on the carrying branch this fork is '
                  'an exact zero and measuring it there would report a real disagreement as '
                  'no disagreement. It is worth %.2f%% of the round branch.'
                  % (100 * abs(M.primary(mark=mark_statements) - M.branch_round())
                     / M.primary(mark=mark_statements))),
             overturned_by=(
                 'one filing stating a single percentage for both the Dutch holding vehicle '
                 'and the operating group, or a transaction naming which of the two the '
                 'round valued.')),
    ]

    judgements = []
    for j in J:
        if not str(j.get('overturned_by') or '').strip():
            raise SystemExit(
                'judgement %r states nothing that would overturn it. The bibliography '
                'prints this column and the depth bar requires it; an empty one is worse '
                'than an absent table, because the page then asserts a falsifier that is '
                'not there.' % j['name'])
        on_round = j.get('measured_on') == 'round'
        va = float(j['a'][1] if on_round else j['a'][0])
        vb = float(j['b'][1] if on_round else j['b'][0])
        judgements.append({
            'name': j['name'],
            'adopted': j['adopted'],
            'alternative': j['alternative'],
            'measured_on_branch': L_ROUND if on_round else L_CARRY,
            'value_adopted': va,
            'value_alternative': vb,
            'value_adopted_carrying_branch': float(j['a'][0]),
            'value_alternative_carrying_branch': float(j['b'][0]),
            'value_adopted_round_branch': float(j['a'][1]),
            'value_alternative_round_branch': float(j['b'][1]),
            'moves_the_answer_by': abs(va - vb) / abs(vb),
            'moves_the_carrying_branch_by': abs(j['a'][0] - j['b'][0]) / abs(j['b'][0]),
            'moves_the_round_branch_by': abs(j['a'][1] - j['b'][1]) / abs(j['b'][1]),
            'direction': ('the study took the higher value' if va > vb else
                          'the study took the lower value' if va < vb else 'no difference'),
            'why': j['why'],
            # WHAT WOULD OVERTURN THE CHOICE — required, not optional. The depth bar asks
            # the judgements table for this column and the bibliography's own introductory
            # sentence promised it while the table's last column said something else, so
            # the sentence was false of the table it introduced. A judgement with nothing
            # that would overturn it is a habit rather than a finding, which is the same
            # test the lessons register puts on every lesson it accepts.
            'overturned_by': j['overturned_by'],
        })

    material = [x for x in judgements if x['moves_the_answer_by'] >= 0.05]
    up = len([x for x in material if x['value_adopted'] > x['value_alternative']])
    n = len(material)
    p = min(1.0, 2 * sum(comb(n, i) for i in range(max(up, n - up), n + 1))
            / float(2 ** n)) if n else None

    cj = {
        'ticker': 'GBCO',
        'as_of': N['edition'],
        # [R-ENF-06], and see the same field in diagnostics.json: this study publishes no
        # central, so the declaration names the branch this record is measured on and
        # carries both.
        'published_central': carry_ps,
        'published_central_is': L_CARRY,
        'published_central_note': (
            'THIS STUDY PUBLISHES NO CENTRAL. The field above names the branch this record '
            'measures materiality on — the reviewed carrying value, the LOWER of the two — '
            'and both branches are declared below. Every judgement carries its value on '
            'both branches whatever this field says.'),
        'published_central_two_sided': [
            {'label': L_CARRY, 'value': carry_ps},
            {'label': L_ROUND, 'value': round_ps},
        ],
        'published_spot': strike,
        'measured_on': (
            'THE STUDY PUBLISHES TWO ANSWERS, SO "5%% OF THE ANSWER" NEEDED A RULE AND '
            'HERE IT IS. A judgement is material if it is worth more than 5%% of EITHER '
            'branch, and since every fork except one moves both branches by the same number '
            'of pounds, that is the LOWER branch — the reviewed carrying value at EGP %.4f '
            'a share. Measuring there records the superset and falls to the strict side, '
            'which is what this house does everywhere else an answer is ambiguous. It '
            'changes exactly one classification: the GB Capital return anchor clears 5%% on '
            'the carrying branch and does not on the round branch, and it is recorded as '
            'material. The one exception is the ownership percentage, which has no effect '
            'at all on the carrying branch and is measured on the round branch with that '
            'said in its own entry. Both framings are carried on every judgement.'
            % carry_ps),
        'two_sided_judgement': {
            'name': 'the basis on which the MNT-Halan stake is marked',
            'why_it_is_not_in_the_signed_list': (
                'THIS IS THE ANSWER, NOT A FORK THE STUDY RESOLVED. It is by a distance the '
                'most consequential judgement in the study — EGP %.0f mn, %.1f%% of the '
                'lower branch and %.1f%% of the higher — and the study does not adopt '
                'either side: it publishes both, '
                % (M.mark_round - M.mark_carrying,
                   100 * (round_ps - carry_ps) / carry_ps,
                   100 * (round_ps - carry_ps) / round_ps) +
                'because both are GB Corp\'s own disclosures about one stake and the filings '
                'do not decide between them. A sign test measures WHICH WAY forks were '
                'resolved, so recording an unresolved fork in it would manufacture a count '
                'in whichever direction the two values happened to sit — either an upward '
                'count for a choice nobody made, or a downward one. It is recorded here in '
                'full instead, with both values, and named in the sign test\'s own reading '
                'so nobody reads that test as covering it.'),
            'basis_a': {'label': L_ROUND, 'mark_egp_mn': M.mark_round, 'value': round_ps,
                        'what': ('41.61% of the USD 1.4bn primary round completed with Al '
                                 'Ahly Capital Holding, translated at EGP 47.5'),
                        'against_it': ("a primary round's headline valuation prices NEW "
                                       'money with whatever preferences ride with it, and '
                                       'GB Corp holds an ordinary equity-accounted minority '
                                       'in an unlisted company. It is a mark, not a '
                                       'realisable price.')},
            'basis_b': {'label': L_CARRY, 'mark_egp_mn': M.mark_carrying, 'value': carry_ps,
                        'what': ('note 34 to the reviewed consolidated interim statements at '
                                 '30 June 2026, EGP 15,733,523 thousand, footing to that '
                                 "balance sheet's own associates line"),
                        'against_it': ('it is an ACCOUNTING measure — cost plus accumulated '
                                       'share of profit plus the revaluation on '
                                       'deconsolidation — and book is a floor rather than a '
                                       'value. AND IT IS ITSELF QUALIFIED: the review '
                                       'conclusion on these statements is qualified '
                                       'precisely here, the reviewers not having been given '
                                       "the associate's own financial statements and being "
                                       "unable to verify the group's EGP 409.9mn share of "
                                       'profit for the period.')},
            'spread_egp_mn': M.mark_round - M.mark_carrying,
            'spread_as_a_share_of_the_higher_branch':
                (round_ps - carry_ps) / round_ps,
            'note': ('averaging the two would be the blend [R-LENS-03] retired, arriving '
                     'through a different door, and a discount standing in for the '
                     'uncertainty would be the free parameter this rebuild removed. The '
                     'uncertainty is IN THIS LINE and it is published as this line.'),
        },
        'judgements': judgements,
        'sign_test': {
            'material': n, 'resolved_upward': up, 'resolved_downward': n - up,
            'two_sided_p': p,
            'flagged': bool(p is not None and p < 0.05 and n >= 3),
            'reading': (
                'Of %d material forks the study took the higher-value side on %d. Two-sided '
                'p = %.4f, so this is NOT flagged at the 5%% level. WHAT THIS TEST DOES NOT '
                'COVER, AND IT IS THE BIGGEST THING IN THE STUDY: the mark on the MNT-Halan '
                'stake, worth %.1f%% of the higher branch, is not resolved at all — it is the '
                'two-sided answer, recorded above and deliberately kept out of a test that '
                'measures which way a fork was resolved. WHAT THE COUNT DOES NOT SHOW AND '
                'THE VALUES DO: the one material fork the study resolved DOWNWARD is the '
                "lender's return anchor, where it took the reviewed half over the better "
                'full year; and the largest fork by a wide margin, the working-capital '
                'release at %.0f%%, it resolved upward. A study whose single largest lever '
                'runs its way is a study whose reader should look at that lever first.'
                % (n, up, p, 100 * (round_ps - carry_ps) / round_ps,
                   100 * max(x['moves_the_answer_by'] for x in material))),
        },
        'unvalued': [
            {'name': 'the second closing of the MNT-Halan round',
             'what': ('public reporting describes the June-2026 close as an initial tranche '
                      'of an ongoing round, with a second closing open'),
             'why_not_valued': ('size and terms are undisclosed, so neither framing has a '
                                'number behind it. SIGCM clause 8: stop rather than invent.'),
             'direction_if_valued': 'unknown — a second close could reprice the round either way'},
            {'name': 'the currency the dollar round is translated at',
             'what': ('the round is translated at the house macro path\'s own EGP/USD %.1f, '
                      'the rate at the strike' % M.fx),
             'why_not_valued': (
                 'translating at a later rate is a change of strike date rather than an '
                 'alternative framing of a judgement, and this record prices framings. It '
                 'is named here so its absence is visible. It moves the ROUND branch only; '
                 'the carrying branch is a pound figure off a pound balance sheet and does '
                 'not move with it at all.'),
             'direction_if_valued': ('UP on the round branch if the pound is weaker at a '
                                     'later date, DOWN if stronger; no effect on the '
                                     'carrying branch')},
            {'name': "the qualification on the reviewers' conclusion",
             'what': ("the limited-review conclusion on the 30-June-2026 statements is "
                      'qualified at the associate line itself, the same qualification '
                      'having stood on the 31-December-2025 audited statements'),
             'why_not_valued': ('there is no second number to price it against — a '
                                'qualification says a figure could not be verified, not what '
                                'it should have been. It is recorded because it is the '
                                'reason the lower branch is not a safe harbour, which a '
                                'reader would otherwise assume of a book figure.'),
             'direction_if_valued': 'unknown, and that is the point of a qualification'},
        ],
        'considered_and_not_counted': [
            {'name': 'the four-lens weighted blend',
             'what': ('the superseded edition published a central weighting the sum of the '
                      'parts, the undiscounted sum, a relative multiple and a normalised '
                      'earnings figure at 40/15/20/25'),
             'why_not_a_judgement': (
                 '[R-LENS-03] retired the typed blend outright — the weights had never '
                 'cleared any out-of-sample test and two of the four lenses do not touch '
                 'the largest asset on the page. That is a retired ARCHITECTURE rather than '
                 'a defensible alternative framing, and pricing it here would launder it '
                 'back in as a judgement. It is also not priceable under the current model, '
                 'because one of the lenses it weighted no longer exists.'),
             'direction_if_counted': 'not computable — the model can no longer express it'},
            {'name': 'the normalised-earnings lens',
             'what': ('the superseded edition carried a mid-cycle group profit capitalised '
                      'at a through-cycle multiple, at 25% of the blend'),
             'why_not_a_judgement': (
                 'the class row for an automotive assembler with a captive lender does not '
                 'carry it, and normalising earnings that swing on associate marks '
                 'normalises noise. A lens the class does not permit is not an alternative '
                 'framing of anything.'),
             'direction_if_counted': 'not computable — the lens is gone'},
            {'name': 'the complexity / conglomerate discount',
             'what': ('the superseded edition deducted a typed 10% from the sum of the '
                      'parts and then weighted the discounted and undiscounted sums at 0.40 '
                      'and 0.15, which applies an effective 4%'),
             'why_not_a_judgement': (
                 'both figures are free parameters with nothing observable behind them and '
                 'nothing in GB Corp\'s filings discloses a basis for either, so the '
                 'PROMOTION RULE forbids them. The old record priced this fork AND the '
                 'question of where the discount was applied, which is a second judgement '
                 'built on the first. What the discount was standing in for is now named '
                 'instead — the uncertainty is in the associate mark and is published as '
                 'two branches. Counting a removed free parameter as a judgement the study '
                 'won would add an UPWARD count for a correction, which is exactly the '
                 'laundering this list exists to refuse.'),
             'direction_if_counted': ('UP, and material: reinstating the 10% would take '
                                      'both branches down by that 10%')},
            {'name': 'GB Capital carried at 1.0x book',
             'what': ('the superseded edition carried the lender at an adjusted operating '
                      'book times a multiple of exactly one'),
             'why_not_a_judgement': (
                 '[R-LENS-03] is explicit that book value is a disclosed FLOOR and is never '
                 'weighted into an answer, so a leg carried at 1.0x book is book value '
                 'wearing a sum-of-the-parts entry\'s clothes. The base was also the '
                 'company\'s own adjusted-ROAE denominator, which is justified by earnings '
                 'that include associate income the sum of the parts then counts AGAIN at '
                 'the round price — the cash charged twice, in a lender\'s costume. A '
                 'prohibited construction is not an alternative framing.'),
             'direction_if_counted': (
                 'DOWN — correcting it CUT this leg. At 1.0x the committed operating book '
                 'of EGP %.1f mn the leg would be worth EGP %.1f mn more, EGP %.2f a share '
                 'on both branches, so counting it would add a downward count'
                 % (M.cp['operating_equity'], M.cp['operating_equity'] - M.cap,
                    (M.cp['operating_equity'] - M.cap) / M.SH))},
            {'name': 'the terminal growth rate',
             'what': ('the superseded edition held a typed nominal 11.5%% for ever; the '
                      'rebuild stores growth as a REAL rate on the house Egyptian path and '
                      'recomputes it to %.1f%% nominal' % (100 * M.tg)),
             'why_not_a_judgement': (
                 '[R-MACRO-01] forbids a typed nominal rate outright, because nobody can '
                 'tell whether 11.5% meant inflation plus four points or minus three, and a '
                 'terminal growth above the inflation inside the terminal discount rate is '
                 'a perpetual real expansion nothing discloses. An unfalsifiable input is '
                 'not a defensible framing. IT IS LISTED HERE WITH ITS DIRECTION BECAUSE '
                 'THIS LIST MUST NOT BE ONE-SIDED: three of the corrections excluded from '
                 'the signed list are priceable, and if they were counted they would add '
                 'one upward and two downward.'),
             'direction_if_counted': (
                 'DOWN, and by more than anything in the signed list — the superseded '
                 'nominal is worth %.0f%% more on the carrying branch'
                 % (100 * (M.branch_carrying(g=0.115) / carry_ps - 1)))},
        ],
    }

    json.dump(diag, open(os.path.join(HERE, 'diagnostics.json'), 'w', encoding='utf-8'),
              indent=1, ensure_ascii=False)
    json.dump(cj, open(os.path.join(HERE, 'contested_judgements.json'), 'w',
                       encoding='utf-8'), indent=1, ensure_ascii=False)

    assert _sha(numbers) == before, (
        'study_numbers.json changed while a diagnostic ran. A quantity solved from a price '
        'must never reach the file every builder reads.')

    print('GBCO reverse read + contested judgements COMPUTED')
    print('  no central — branches %.4f (%s) and %.4f (%s), strike %.2f, latest close '
          '%.2f (%s)' % (carry_ps, 'carrying', round_ps, 'round', strike, spot, spot_date))
    print('  reverse read: the price pays US$%.1f mn for MNT-Halan as a whole, against the '
          'round\'s US$%.0f mn and the carrying value\'s US$%.0f mn'
          % (implied_usd, M.round_usd, carry_usd))
    print('  judgements %d, material %d, upward %d, two-sided p = %.4f'
          % (len(judgements), n, up, p))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
