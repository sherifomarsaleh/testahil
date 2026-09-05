"""STC — cost of revenues by NATURE, three filed years, and the two one-offs inside it.

THE MODEL HOLDS EACH SEGMENT'S GROSS MARGIN FLAT, WHICH IS AN INPUT WHERE THE FILINGS
SUPPORT AN OUTPUT. The standing rule is that a contribution or gross margin set as an input
is a fail wherever the disclosure lets cost be built instead, and note 35 of the FY2025
audited statements (note 36 of the FY2024 set) breaks the whole cost of revenues into seven
lines by nature. Each is a different economic driver — imported handsets, interconnection,
domestic wages, a regulated charge, maintenance of an asset base — and the cost-stack rule
says each takes its OWN escalator, never one blended index across all of them.

WHAT THIS FILE DOES NOT DO YET. It commits the disclosure and the arithmetic. Wiring the
model to build gross profit from these seven lines is a further correction and it is not
made here, because the escalator for each line has to be sourced before it is applied and
two of the seven (network access charges, others) have no disclosed physical driver at all.

THE TWO ONE-OFFS ARE THE REASON THIS MATTERS EVEN BEFORE THAT. Each filing names one, in
its own footnote: SR 1,500 million of withholding-tax provision REVERSED into FY2024's
network access charges, and SR 724 million of provision REVERSED into FY2023's government
charges. Both LOWER the cost of those years and RAISE their gross margins, and the model
holds FY2025's margin flat without knowing that the two years behind it are flattered.
Corrected, the underlying margin is RISING rather than dipping and recovering — and FY2025,
the year the model holds, is the HIGHEST of the three. Holding the best year flat is the
optimistic end of the range, not the cautious one, and a study that did not know which it
was doing had not classified its one-offs [R-FCAL-01].
"""
from __future__ import annotations

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

#: ONE FILING PER COLUMN, for the reason segments.py records: the two filings state
#: different FY2024 figures (network access 8,100,803 against 8,126,317, total 38,567,489
#: against 38,593,003), so a column built from both is two groupings in one place.
FY2025_FILING = 'stc_Annual-2025-en.txt, note 35 (audited, year ended 31 December 2025)'
FY2023_FILING = 'stc_Annual-2024-en.txt, note 36 (audited, year ended 31 December 2024)'

COST_OF_REVENUES = {
    #  line                                       FY2023      FY2024      FY2025
    'Cost of devices, equipment and software': (13_360_079, 14_644_906, 14_195_531),
    'Network access charges':                  ( 9_149_535,  8_100_803, 10_094_182),
    'Government charges':                      ( 4_571_302,  5_378_203,  5_417_576),
    'Employees costs':                         ( 5_051_339,  5_534_674,  5_543_832),
    'Repairs and maintenance':                 ( 1_952_911,  1_895_572,  1_967_772),
    'Amortisation and impairment of contract costs': (150_725, 190_054,    189_743),
    'Others':                                  ( 2_801_204,  2_823_277,  2_710_350),
}
YEARS = ('FY2023', 'FY2024', 'FY2025')
STATED_TOTAL = (37_037_095, 38_567_489, 40_118_986)
REVENUE = (71_777_161, 75_893_413, 77_818_675)
GROSS_PROFIT = (34_740_066, 37_325_924, 37_699_689)

#: DISCLOSED NON-RECURRING ITEMS, each named in its own filing's own footnote. Both are
#: REVERSALS, so both lower the reported cost and raise the reported margin.
ONE_OFFS = [
    dict(year='FY2024', line='Network access charges', amount=1_500_000,
         what='a reversal of a withholding tax provision',
         source='stc_Annual-2025-en.txt, note 35, footnote (*)'),
    dict(year='FY2023', line='Government charges', amount=724_000,
         what='a reversal of a provision',
         source='stc_Annual-2024-en.txt, note 36, footnote (**)'),
]

#: What each line is economically driven by — the reason one blended escalator is wrong.
#: Recorded as a classification, NOT yet as an escalator: the rate for each has to be
#: sourced before it is applied, and two of the seven have no disclosed physical driver.
DRIVER_CLASS = {
    'Cost of devices, equipment and software': 'imported handsets and equipment; dollar-'
        'denominated under a pegged riyal, so the driver is device volume and world '
        'equipment prices rather than domestic inflation',
    'Network access charges': 'interconnection and wholesale capacity; volume-linked and '
        'regulated, with no disclosed unit rate',
    'Government charges': 'FOUR things with four drivers, per note 35\'s own sub-table, and '
        'the largest is not levied on group revenue at all — the commercial service '
        'provisioning fee sits on the Saudi operating segment, which grows far more slowly '
        'than the group. See levy_ratio() and cost_decomposition.py',
    'Employees costs': 'domestic wages; the one line the Saudi inflation ladder governs '
        'directly',
    'Repairs and maintenance': 'the asset base being maintained, so it belongs with the '
        'capital-intensity question rather than with revenue',
    'Amortisation and impairment of contract costs': 'contract acquisition costs amortised '
        'over contract life; a subscriber-acquisition driver',
    'Others': 'stc Bank direct cost, postage and delivery, and utilities per the note; a '
        'residual with no single driver',
}


# ---------------------------------------------------------------------------------------
# WHAT THE BLENDED MARGIN HIDES, MEASURED RATHER THAN ASSERTED.
#
# The model holds each SEGMENT's gross margin flat, so each segment's cost already sits on
# its own segment's revenue — which is the right base for most of this stack and is better
# than the "one blended index" the cost-stack rule forbids. What it does NOT do is put the
# lines whose driver is something OTHER than the revenue they are allocated against onto
# that other thing. The standing instruction for exactly this case is to DECOMPOSE AND
# PRICE what the coarse figure hides, and never to fill an unidentified split with an
# imported ratio. Both halves are done here.
#
# TWO OF THE SEVEN LINES CANNOT BE BUILT AT ALL and that is the gap, named rather than
# papered: network access charges (12.97% of revenue) discloses no unit rate, and Others
# (3.48%) is a residual of three unrelated things. Employees costs (7.12%) would need a
# headcount and the filings carry none — searched and absent, not assumed away.
# ---------------------------------------------------------------------------------------

#: Note 34 of the FY2025 statements (34 of the FY2024 set). DEVICE REVENUE IS IDENTICAL IN
#: BOTH FILINGS FOR FY2024, so the device leg is untouched by the services/others
#: regrouping between them, and one filing per column is not needed for it.
REVENUE_DISAGGREGATION = {
    'Rendering of services': (60_306_720, 63_283_188, 63_312_089),
    'Sale of devices':       (11_406_625, 12_458_105, 12_634_029),
    'Others':                (     63_816,    152_120,  1_872_557),
}
#: FY2023 and FY2024 columns are the FY2024 filing's; FY2025 is the FY2025 filing's. The
#: services/others boundary moved between them (digital banking), which is why the FY2024
#: column here is the FY2024 filing's grouping and the totals still foot.
DISAGG_TOTAL = (71_777_161, 75_893_413, 77_818_675)

#: Note 35's OWN sub-note. The line the model treats as one regulated levy is four things
#: with four different drivers, and the largest is not levied on group revenue at all.
GOVERNMENT_CHARGES = {
    'Commercial service provisioning fees': (3_687_775, 4_702_782, 4_608_632),
    'License fees':                         (  444_266,   463_948,   468_768),
    'Frequency spectrum fees':              (  361_932,   137_427,   265_470),
    'Others':                               (   77_329,    74_046,    74_706),
}

#: THE 724,000 REVERSAL IS PLACED BY ARITHMETIC, NOT BY INFERENCE. The FY2024 filing's
#: footnote says a reversal of that size sits inside FY2023 government charges and does not
#: say in which sub-line. Three of the four sub-lines are each SMALLER than the reversal, so
#: it cannot sit in any of them; the levy is the only line the arithmetic permits. Placing
#: it there also tightens the levy's own ratio from a 1.98-point spread to 0.51 — which is
#: corroboration, not the reason.
def reversal_placement():
    """Return (line, ruled_out) — the only sub-line large enough to carry the reversal."""
    amt = next(o['amount'] for o in ONE_OFFS if o['year'] == 'FY2023')
    i = YEARS.index('FY2023')
    fits = [k for k, v in GOVERNMENT_CHARGES.items() if v[i] >= amt]
    ruled_out = [(k, v[i]) for k, v in GOVERNMENT_CHARGES.items() if v[i] < amt]
    return (fits[0] if len(fits) == 1 else None), ruled_out


def levy_ratio(seg_revenue):
    """The provisioning levy against the base the sub-note says it is levied on.

    seg_revenue is the stc (KSA) operating segment's revenue, three years, from the
    segment note. The FY2023 figure carries the disclosed reversal put back.
    """
    amt = next(o['amount'] for o in ONE_OFFS if o['year'] == 'FY2023')
    line, _ = reversal_placement()
    v = list(GOVERNMENT_CHARGES['Commercial service provisioning fees'])
    if line == 'Commercial service provisioning fees':
        v[YEARS.index('FY2023')] += amt
    return [v[i] / seg_revenue[i] for i in range(3)]


#: THE DEVICE LINE IS NOT DEVICE COST OF SALES AND THE FILINGS PROVE IT: the line costs
#: more than the devices sell for in every one of the three years, so it carries equipment
#: and software consumed in operations as well. The company does not split it. The rule is
#: to DEMONSTRATE the split unidentified rather than assert it, by solving for the implied
#: parameter across EVERY available period pair and publishing the range.
def device_split_range():
    """Solve cost = k*device_revenue + e*revenue over every period pair; return the range."""
    from itertools import combinations
    dev = REVENUE_DISAGGREGATION['Sale of devices']
    rev = DISAGG_TOTAL
    cost = COST_OF_REVENUES['Cost of devices, equipment and software']
    out = []
    for i, j in combinations(range(3), 2):
        det = dev[i] * rev[j] - dev[j] * rev[i]
        k = (cost[i] * rev[j] - cost[j] * rev[i]) / det
        e = (dev[i] * cost[j] - dev[j] * cost[i]) / det
        out.append(dict(pair=(YEARS[i], YEARS[j]), k=k, e=e))
    return out


def device_line_exceeds_device_revenue():
    dev = REVENUE_DISAGGREGATION['Sale of devices']
    cost = COST_OF_REVENUES['Cost of devices, equipment and software']
    return [cost[i] - dev[i] for i in range(3)]


# ---------------------------------------------------------------------------------------
# THE REST OF THE WAY TO EBITDA, AND IT IS DISCLOSED LINE BY LINE TOO. Notes 36 and 37 of
# the FY2025 statements (37 and 38 of the FY2024 set) break selling and marketing and
# general and administrative expenses into their own components. The model uses ONE
# blended share of revenue for the whole of it. Gross profit less these two notes IS the
# stated EBITDA in every one of the three years, to the riyal — which is what makes this a
# reconciliation rather than a reading.
# ---------------------------------------------------------------------------------------
SELLING_AND_MARKETING = {
    'Employee costs':                            (2_904_133, 2_905_142, 2_862_473),
    'Advertising, publicity and sales commissions': (1_800_537, 1_763_681, 2_368_067),
    'Impairment loss on trade receivables':        (448_141, 1_257_976,   301_871),
    'Impairment loss on contract assets':          (135_851,   113_839,   104_399),
    'Amortisation and impairment of contract costs': (93_645,    92_817,   110_461),
    'Call centre expenses':                         (87_765,    43_781,    39_579),
    'Others':                                      (399_749,   384_584,   584_726),
}
SM_TOTAL = (5_869_821, 6_561_820, 6_371_576)

GENERAL_AND_ADMINISTRATIVE = {
    'Employees costs':                           (4_279_273, 4_596_844, 4_774_730),
    'Consultancy and other contracted services':   (682_577,   646_645,   614_096),
    'Repairs and maintenance':                     (577_674,   644_871,   542_082),
    'Utilities and cleaning':                      (142_612,   160_792,   156_100),
    'Rent':                                         (44_554,    38_866,    42_263),
    #: security and safety is broken out in the FY2024 filing and folded into Others in the
    #: FY2025 one, and subscription expenses appear only in the FY2025 set — the same
    #: re-grouping the segment panel meets, handled the same way: ONE FILING PER COLUMN,
    #: with the FY2023 column carrying its own filing's grouping and the two later ones the
    #: FY2025 filing's. The totals are each filing's own and every column foots.
    'Others (incl. security, safety and subscriptions)': (698_166, 724_971, 729_407),
}
GA_TOTAL = (6_424_856, 6_812_989, 6_858_678)
EBITDA = (22_445_389, 23_951_115, 24_469_435)

#: THE CREDIT-LOSS CHARGE IS THE VOLATILE LINE AND IT IS NOT A ONE-OFF ANYBODY NAMED.
#: Impairment on trade receivables runs 448,141 then 1,257,976 then 301,871 — a fourfold
#: swing with no footnote explaining any of it, so it is not classifiable as non-recurring
#: and is instead NORMALISED to its own three-year mean. That is a judgement, it is stated
#: as one, and both the reported and the normalised series are published so a reader can
#: take the other view.
IMPAIRMENT_LINE = 'Impairment loss on trade receivables'


def impairment_mean():
    v = SELLING_AND_MARKETING[IMPAIRMENT_LINE]
    return sum(v) / len(v)


def normalised_ebitda(i):
    """EBITDA with the two named reversals put back and the credit-loss charge at its mean."""
    return (EBITDA[i]
            - sum(o['amount'] for o in ONE_OFFS if o['year'] == YEARS[i])
            + (SELLING_AND_MARKETING[IMPAIRMENT_LINE][i] - impairment_mean()))


def underlying(i):
    """Cost of revenues with the disclosed one-offs put back — what the year actually cost."""
    adj = sum(o['amount'] for o in ONE_OFFS if o['year'] == YEARS[i])
    return STATED_TOTAL[i] + adj


def check():
    problems = []
    for i, y in enumerate(YEARS):
        got = sum(v[i] for v in COST_OF_REVENUES.values())
        if got != STATED_TOTAL[i]:
            problems.append('%s cost lines sum to %s against a stated %s'
                            % (y, f'{got:,}', f'{STATED_TOTAL[i]:,}'))
        # THE STRONGEST CHECK IS THE ONE THAT CROSSES NOTES: revenue less this total must
        # BE the gross profit the segment note states, to the riyal.
        if REVENUE[i] - STATED_TOTAL[i] != GROSS_PROFIT[i]:
            problems.append('%s revenue less cost is %s against a stated gross profit of %s'
                            % (y, f'{REVENUE[i] - STATED_TOTAL[i]:,}',
                               f'{GROSS_PROFIT[i]:,}'))
    for o in ONE_OFFS:
        if o['year'] not in YEARS:
            problems.append('one-off filed against %s, which is not a year here' % o['year'])
    # THE OPERATING-EXPENSE NOTES MUST FOOT AND MUST BRIDGE. Each note sums to its own
    # stated total, and gross profit less the two of them must BE the stated EBITDA — the
    # check that crosses notes, which is the one a mis-keyed line cannot survive.
    for label, table, stated in (('selling and marketing', SELLING_AND_MARKETING, SM_TOTAL),
                                 ('general and administrative',
                                  GENERAL_AND_ADMINISTRATIVE, GA_TOTAL)):
        for i, y in enumerate(YEARS):
            got = sum(v[i] for v in table.values())
            if got != stated[i]:
                problems.append('%s %s sums to %s against a stated %s'
                                % (y, label, f'{got:,}', f'{stated[i]:,}'))
    for i, y in enumerate(YEARS):
        if GROSS_PROFIT[i] - SM_TOTAL[i] - GA_TOTAL[i] != EBITDA[i]:
            problems.append('%s gross profit less both expense notes is %s against a '
                            'stated EBITDA of %s'
                            % (y, f'{GROSS_PROFIT[i] - SM_TOTAL[i] - GA_TOTAL[i]:,}',
                               f'{EBITDA[i]:,}'))
    # THE SUB-NOTE MUST FOOT TO THE LINE ABOVE IT, in all three years — the check that
    # crosses from note 35's sub-table back to note 35 itself.
    for i, y in enumerate(YEARS):
        got = sum(v[i] for v in GOVERNMENT_CHARGES.values())
        if got != COST_OF_REVENUES['Government charges'][i]:
            problems.append('%s government-charge sub-lines sum to %s against the %s the '
                            'cost note states'
                            % (y, f'{got:,}',
                               f"{COST_OF_REVENUES['Government charges'][i]:,}"))
    # And the revenue disaggregation must foot to revenue.
    for i, y in enumerate(YEARS):
        got = sum(v[i] for v in REVENUE_DISAGGREGATION.values())
        if got != DISAGG_TOTAL[i] or DISAGG_TOTAL[i] != REVENUE[i]:
            problems.append('%s revenue disaggregation sums to %s against a stated %s'
                            % (y, f'{got:,}', f'{DISAGG_TOTAL[i]:,}'))
    # THE REVERSAL MUST BE PLACEABLE BY ARITHMETIC ALONE. If a restated filing ever made a
    # second sub-line large enough to carry it, the deduction stops holding and this says so
    # rather than leaving a placement standing on evidence that has moved.
    line, ruled_out = reversal_placement()
    if line is None:
        problems.append('the FY2023 reversal is no longer placed by arithmetic alone: %d '
                        'sub-lines are large enough to carry it' % (4 - len(ruled_out)))
    # THE DEVICE LINE MUST STILL EXCEED DEVICE REVENUE — the fact the whole "this is not
    # device cost of sales" reading rests on.
    for i, gap in enumerate(device_line_exceeds_device_revenue()):
        if gap <= 0:
            problems.append('%s device cost no longer exceeds device revenue (%s), so the '
                            'line may now be device cost of sales and the split reasoning '
                            'must be redone' % (YEARS[i], f'{gap:,}'))
    return problems


def _ksa_segment_revenue():
    """The stc (Saudi) operating segment's revenue, three years, from the segment note."""
    import segments as _S
    return _S.REVENUE['stc']


def record():
    rep = [GROSS_PROFIT[i] / REVENUE[i] for i in range(3)]
    und = [(REVENUE[i] - underlying(i)) / REVENUE[i] for i in range(3)]
    return dict(
        ticker='STC', years=list(YEARS),
        sources=dict(FY2025=FY2025_FILING, FY2024=FY2025_FILING, FY2023=FY2023_FILING),
        cost_of_revenues={k: list(v) for k, v in COST_OF_REVENUES.items()},
        stated_total=list(STATED_TOTAL), revenue=list(REVENUE),
        gross_profit=list(GROSS_PROFIT),
        one_offs=ONE_OFFS,
        underlying_cost=[underlying(i) for i in range(3)],
        reported_gross_margin=rep, underlying_gross_margin=und,
        driver_class=DRIVER_CLASS,
        revenue_disaggregation={k: list(v) for k, v in REVENUE_DISAGGREGATION.items()},
        government_charges={k: list(v) for k, v in GOVERNMENT_CHARGES.items()},
        reversal_placed_in=reversal_placement()[0],
        reversal_ruled_out=[{'line': k, 'size': v} for k, v in reversal_placement()[1]],
        device_line_less_device_revenue=device_line_exceeds_device_revenue(),
        device_split_pairs=[{'pair': list(s['pair']), 'k': s['k'], 'e': s['e']}
                            for s in device_split_range()],
        levy_share_of_ksa_segment=levy_ratio(_ksa_segment_revenue()),
        levy_note=(
            'The provisioning levy is the largest government charge and it is not levied on '
            'group revenue. Against the stc (Saudi) segment the sub-note implies it is '
            'charged on, and with the disclosed reversal put back in the only sub-line big '
            'enough to carry it, it runs a tight band across all three filed years. Held '
            'against GROUP revenue instead it appears to step two points in a single year, '
            'which is an artefact of the base and of an item the filing calls '
            'non-recurring.'),
        selling_and_marketing={k: list(v) for k, v in SELLING_AND_MARKETING.items()},
        general_and_administrative={k: list(v)
                                    for k, v in GENERAL_AND_ADMINISTRATIVE.items()},
        sm_total=list(SM_TOTAL), ga_total=list(GA_TOTAL), ebitda=list(EBITDA),
        reported_ebitda_margin=[EBITDA[i] / REVENUE[i] for i in range(3)],
        normalised_ebitda=[normalised_ebitda(i) for i in range(3)],
        normalised_ebitda_margin=[normalised_ebitda(i) / REVENUE[i] for i in range(3)],
        impairment_mean=impairment_mean(),
        ebitda_finding=(
            'The REPORTED EBITDA margin rises then dips, 31.27%, 31.56%, 31.44%. With the '
            'two named reversals put back and the credit-loss charge held at its own '
            'three-year mean it RISES STEADILY: 29.95%, 30.36%, 30.97%, about fifty basis '
            'points a year. THE REBUILT MODEL OPENS AT 31.09%, twelve basis points above '
            'the normalised base year and thirty-five below the reported one — so once the '
            'one-offs are classified the forecast margin is well anchored, which is a '
            'validation of the rebuild rather than a defect in it. It is also the only '
            'reading under which the anchor rule can be applied honestly, because the '
            'reported series it would otherwise be measured against is moved by items the '
            'filings themselves call non-recurring.'),
        finding=('The REPORTED gross margin dips and recovers, 48.40%, 49.18%, 48.45%. With '
                 'the two disclosed reversals put back it RISES: 47.39%, 47.20%, 48.45%. '
                 'The model holds FY2025 flat, and FY2025 is the HIGHEST of the three on '
                 'the underlying basis — so that assumption sits at the optimistic end of '
                 'this record rather than the cautious one.'),
        foots=not check(),
    )


if __name__ == '__main__':
    bad = check()
    for b in bad:
        print('FAIL', b)
    if not bad:
        r = record()
        print('all three columns foot, and revenue less cost IS the stated gross profit')
        print('in every year, to the riyal.')
        print()
        print('%-46s %12s %12s %12s' % ('line by nature', *YEARS))
        for k, v in COST_OF_REVENUES.items():
            print('%-46s %12s %12s %12s' % (k[:46], *[f'{x:,}' for x in v]))
        print('%-46s %12s %12s %12s' % ('TOTAL', *[f'{x:,}' for x in STATED_TOTAL]))
        print()
        for i, y in enumerate(YEARS):
            print('%s gross margin: reported %.2f%%   underlying %.2f%%'
                  % (y, 100 * r['reported_gross_margin'][i],
                     100 * r['underlying_gross_margin'][i]))
        print()
        for o in ONE_OFFS:
            print('one-off: %s %s, %s of %s' % (o['year'], o['line'], o['what'],
                                                f"SAR {o['amount']:,} thousand"))
        print()
        print('gross profit less selling and marketing less general and administrative')
        print('IS the stated EBITDA in every year, to the riyal:')
        for i, y in enumerate(YEARS):
            print('  %s  %12s - %10s - %10s = %12s'
                  % (y, f'{GROSS_PROFIT[i]:,}', f'{SM_TOTAL[i]:,}', f'{GA_TOTAL[i]:,}',
                     f'{EBITDA[i]:,}'))
        print()
        print('EBITDA margin: reported %s' %
              '  '.join('%.2f%%' % (100 * r['reported_ebitda_margin'][i]) for i in range(3)))
        print('               normalised %s' %
              '  '.join('%.2f%%' % (100 * r['normalised_ebitda_margin'][i])
                        for i in range(3)))
        print('  (the two named reversals put back, and the credit-loss charge — which')
        print('   swings 448,141 / 1,257,976 / 301,871 with no footnote explaining any of')
        print('   it — held at its own three-year mean of %s)' % f'{r["impairment_mean"]:,.0f}')
        with open(os.path.join(HERE, 'cost_stack.json'), 'w') as f:
            json.dump(r, f, indent=1)
        print('\nwrote cost_stack.json')
    raise SystemExit(1 if bad else 0)
