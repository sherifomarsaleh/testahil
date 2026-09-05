"""STC — the consolidated income statement below EBITDA, three filed years.

WHY THIS FILE EXISTS. The rebuilt model stops at EBITDA and then goes straight to NOPAT,
because free cash flow to the firm needs nothing else: EBIT times one minus a tax rate. That
is correct for the valuation and it means the model has never projected a finance charge, a
zakat charge or a net profit — so Appendix A's income statement cannot be written from it,
and nor can the dividend lens be checked against a payout the company could actually make.
It is [R-FCAL-01]'s own amendment from another direction: what a process commits decides
what can be asked of it later, and nobody notices the missing field until the question
arrives.

WHERE IT COMES FROM. Note 9's own reconciliation of segment revenue to net profit from
continuing operations, which is the only place these lines appear together, in the FY2025
audited statements (2025 and 2024 columns) and the FY2024 set (2023 column). It FOOTS TO THE
RIYAL in all three years and the check below is that arithmetic, not a reading.

THE TWO LINES A FORECAST HAS TO DECIDE ABOUT, both stated rather than smoothed away:

  THE EARLY RETIREMENT PROGRAMME ran 862,842 / 2,577,256 / 823,801 — a threefold swing with
  no year resembling another. It is a real recurring cost of a company restructuring its
  workforce and it is NOT a one-off anybody has named as such, so it is normalised to its own
  three-year mean rather than dropped, and both readings are published.

  ZAKAT WENT TO A CREDIT IN FY2025. The charge was 1,326,610 then 1,191,564 and then a
  RELEASE of 466,436, which no forecast should extrapolate in either direction. The effective
  rate is therefore taken over the three years TOGETHER against profit before zakat over the
  same three years — one ratio from one window, rather than a mean of three ratios one of
  which is negative.

NOTE THE COST-OF-OPERATIONS FIGURE IS NOT cost_stack's TOTAL and that is not an error: this
reconciliation nets the operating-expense notes into one line, while cost_stack reads cost of
revenues and the two expense notes separately. Both foot to the same EBITDA, which is the
check that crosses them.
"""
from __future__ import annotations

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

YEARS = ('FY2023', 'FY2024', 'FY2025')

#: FY2023 is the FY2024 filing's column; FY2024 and FY2025 are the FY2025 filing's. The one
#: filing per column discipline segments.py and cost_stack.py both keep — and it matters
#: here, because the two filings state FY2024 cost of operations differently (51,967,812
#: against 51,942,298) and depreciation differently (9,499,963 against 9,525,477).
FY2025_FILING = 'stc_Annual-2025-en.txt, note 9 (audited, year ended 31 December 2025)'
FY2023_FILING = 'stc_Annual-2024-en.txt, note 9 (audited, year ended 31 December 2024)'

REVENUE = (71_777_161, 75_893_413, 77_818_675)
COST_OF_OPERATIONS = (-49_331_772, -51_942_298, -53_349_240)
DNA = (-9_284_098, -9_525_477, -10_031_171)
EARLY_RETIREMENT = (-862_842, -2_577_256, -823_801)
FINANCE_INCOME = (1_482_016, 1_717_851, 1_276_442)
FINANCE_COST = (-1_068_102, -1_233_679, -1_125_361)
NET_OTHER = (-110_976, -61_263, 7_042)
ASSOCIATES = (52_579, -665_913, 295_160)
OTHER_GAINS = (1_333_077, 529_069, 654_896)
ZAKAT = (-1_326_610, -1_191_564, 466_436)
NET_PROFIT_CONTINUING = (12_660_433, 10_942_883, 15_189_078)

#: EBITDA as cost_stack computes it from the cost note and the two expense notes, held here
#: so the two routes can be crossed rather than trusted.
EBITDA_FROM_NOTES = (22_445_389, 23_951_115, 24_469_435)

LINES = [
    ('Total revenues', REVENUE),
    ('Cost of operations, excluding depreciation and amortisation', COST_OF_OPERATIONS),
    ('Depreciation, amortisation and impairment', DNA),
    ('Cost of the early retirement programme', EARLY_RETIREMENT),
    ('Finance income', FINANCE_INCOME),
    ('Finance cost', FINANCE_COST),
    ('Net other income and expenses', NET_OTHER),
    ('Net share in associates and joint ventures', ASSOCIATES),
    ('Net other gains', OTHER_GAINS),
    ('Zakat and income tax', ZAKAT),
]


def ebitda(i):
    return REVENUE[i] + COST_OF_OPERATIONS[i]


def ebit(i):
    return ebitda(i) + DNA[i]


def net_finance(i):
    return FINANCE_INCOME[i] + FINANCE_COST[i]


def pbz(i):
    """Profit before zakat: everything above the zakat line."""
    return NET_PROFIT_CONTINUING[i] - ZAKAT[i]


#: THE FILING NAMES THE REVERSAL, so it does not have to be judged one-off — note 33's own
#: movement table carries "Reversal of prior years' Zakat provision during the year
#: (1,324,787)" on its own line. That is a correction of provisions taken in EARLIER years,
#: and a forecast that carries it forward assumes the company keeps discovering it has
#: over-provided, for ever.
ZAKAT_REVERSAL_FY2025 = 1_324_787
ZAKAT_REVERSAL_SOURCE = ("stc_Annual-2025-en.txt, note 33(a), the movement of the zakat "
                         "provision: \"Reversal of prior years' Zakat provision during the "
                         "year\"")


def underlying_zakat(i):
    """The charge with the disclosed prior-year reversal put back."""
    z = -ZAKAT[i]
    if YEARS[i] == 'FY2025':
        z += ZAKAT_REVERSAL_FY2025
    return z


def effective_zakat_rate(base='pbz'):
    """One ratio over the three years together, on a NAMED base, excluding the reversal.

    TWO THINGS HAD TO BE SEPARATED HERE AND EACH WAS FOUND BY AN ARITHMETIC CHECK RATHER
    THAN BY JUDGEMENT.

    First, the reversal. A rate taken over the three years together correctly avoids
    averaging three ratios one of which is negative — but it still CARRIES the release into
    perpetuity, which is the same defect wearing a different hat: 5.02% against 8.27%
    underlying. The filing names the reversal on its own line, so this is a disclosure
    rather than a call.

    Second, the DENOMINATOR. A rate measured against profit before zakat cannot be applied
    to EBIT, and the model's after-tax operating profit needs the second. The two differ
    (8.27% and 8.03%) because the lines between them are a net charge on this book. A ratio
    between quantities defined differently is not evidence about either, so both are
    computed and each is used only where its own base is.
    """
    if base == 'pbz':
        den = sum(pbz(i) for i in range(3))
    elif base == 'ebit':
        den = sum(ebit(i) for i in range(3))
    else:
        raise ValueError('base must be pbz or ebit: %r' % base)
    return sum(underlying_zakat(i) for i in range(3)) / den


def early_retirement_mean():
    return sum(EARLY_RETIREMENT) / len(EARLY_RETIREMENT)


def check():
    problems = []
    for i, y in enumerate(YEARS):
        # THE STATEMENT MUST FOOT: every line above the net-profit line must sum to it.
        got = sum(v[i] for _, v in LINES)
        if got != NET_PROFIT_CONTINUING[i]:
            problems.append('%s the reconciliation sums to %s against a stated net profit '
                            'of %s' % (y, f'{got:,}', f'{NET_PROFIT_CONTINUING[i]:,}'))
        # AND IT MUST CROSS THE COST NOTES: revenue less cost of operations is EBITDA, and
        # cost_stack reaches the same figure by an entirely different route — the cost note
        # plus the two operating-expense notes. A mis-keyed line survives one check and not
        # both.
        if ebitda(i) != EBITDA_FROM_NOTES[i]:
            problems.append('%s EBITDA from this reconciliation is %s against %s from the '
                            'cost and expense notes'
                            % (y, f'{ebitda(i):,}', f'{EBITDA_FROM_NOTES[i]:,}'))
    for _b in ('pbz', 'ebit'):
        if not 0.0 < effective_zakat_rate(_b) < 0.25:
            problems.append('the effective zakat rate on %s computes to %.4f, which is '
                            'outside any rate this regime levies — the sign convention or '
                            'the profit base is wrong' % (_b, effective_zakat_rate(_b)))
    # The reversal must stay INSIDE the year it is disclosed against, or the underlying
    # charge stops being the charge.
    if underlying_zakat(2) <= 0:
        problems.append('the underlying FY2025 zakat is not positive once the disclosed '
                        'reversal is put back, which cannot be right for a profitable year')
    return problems


def record():
    return dict(
        ticker='STC', years=list(YEARS),
        sources=dict(FY2025=FY2025_FILING, FY2024=FY2025_FILING, FY2023=FY2023_FILING),
        lines={name: list(v) for name, v in LINES},
        net_profit_continuing=list(NET_PROFIT_CONTINUING),
        ebitda=[ebitda(i) for i in range(3)],
        ebit=[ebit(i) for i in range(3)],
        net_finance=[net_finance(i) for i in range(3)],
        profit_before_zakat=[pbz(i) for i in range(3)],
        effective_zakat_rate=effective_zakat_rate('pbz'),
        effective_zakat_rate_on_ebit=effective_zakat_rate('ebit'),
        zakat_reversal_fy2025=ZAKAT_REVERSAL_FY2025,
        zakat_reversal_source=ZAKAT_REVERSAL_SOURCE,
        underlying_zakat=[underlying_zakat(i) for i in range(3)],
        zakat_rate_carrying_the_reversal=-sum(ZAKAT) / sum(pbz(i) for i in range(3)),
        early_retirement_mean=early_retirement_mean(),
        finding=(
            'The two lines a forecast has to decide about are the early retirement '
            'programme and zakat, and neither can be read off the latest year. The '
            'programme ran %s, %s and %s — a threefold swing with no year resembling '
            'another — so it is normalised to its own three-year mean rather than dropped, '
            'because it is a real recurring cost of a company restructuring its workforce '
            'and no filing calls it non-recurring. Zakat went to a RELEASE of %s in FY2025 '
            'after charges of %s and %s, so the effective rate is taken over the three '
            'years TOGETHER (%.2f%%) rather than as a mean of three ratios one of which is '
            'negative.'
            % (f'{-EARLY_RETIREMENT[0]:,}', f'{-EARLY_RETIREMENT[1]:,}',
               f'{-EARLY_RETIREMENT[2]:,}', f'{ZAKAT[2]:,}', f'{-ZAKAT[0]:,}',
               f'{-ZAKAT[1]:,}', 100 * effective_zakat_rate('pbz'))),
    )


if __name__ == '__main__':
    bad = check()
    for b in bad:
        print('FAIL', b)
    if not bad:
        r = record()
        print('all three columns foot to their own stated net profit, and EBITDA agrees')
        print('with the entirely separate route through the cost and expense notes.\n')
        w = 58
        print('%-*s %14s %14s %14s' % (w, 'SAR thousands', *YEARS))
        for name, v in LINES:
            print('%-*s %14s %14s %14s' % (w, name[:w], *[f'{x:,}' for x in v]))
        print('%-*s %14s %14s %14s' % (w, 'Net profit from continuing operations',
                                       *[f'{x:,}' for x in NET_PROFIT_CONTINUING]))
        print()
        print('  EBITDA        %s' % '  '.join(f'{ebitda(i):,}' for i in range(3)))
        print('  EBIT          %s' % '  '.join(f'{ebit(i):,}' for i in range(3)))
        print('  net finance   %s' % '  '.join(f'{net_finance(i):,}' for i in range(3)))
        print('  effective zakat rate, three years together, the disclosed prior-year')
        print('  reversal of %s put back:' % f'{ZAKAT_REVERSAL_FY2025:,}')
        print('    on profit before zakat  %.2f%%   (carrying the reversal: %.2f%%)'
              % (100 * r['effective_zakat_rate'],
                 100 * r['zakat_rate_carrying_the_reversal']))
        print('    on EBIT                 %.2f%%   — the base after-tax operating profit '
              'needs' % (100 * r['effective_zakat_rate_on_ebit']))
        with open(os.path.join(HERE, 'income_statement.json'), 'w') as f:
            json.dump(r, f, indent=1)
        print('\nwrote income_statement.json')
    raise SystemExit(1 if bad else 0)
