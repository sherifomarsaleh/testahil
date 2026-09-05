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
    'Government charges': 'a regulated levy; note 35 breaks it out further and it runs '
        'about 7% of revenue',
    'Employees costs': 'domestic wages; the one line the Saudi inflation ladder governs '
        'directly',
    'Repairs and maintenance': 'the asset base being maintained, so it belongs with the '
        'capital-intensity question rather than with revenue',
    'Amortisation and impairment of contract costs': 'contract acquisition costs amortised '
        'over contract life; a subscriber-acquisition driver',
    'Others': 'stc Bank direct cost, postage and delivery, and utilities per the note; a '
        'residual with no single driver',
}


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
    return problems


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
        with open(os.path.join(HERE, 'cost_stack.json'), 'w') as f:
            json.dump(r, f, indent=1)
        print('\nwrote cost_stack.json')
    raise SystemExit(1 if bad else 0)
