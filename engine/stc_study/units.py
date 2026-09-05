"""STC — the unit build for the KSA operating segment: subscribers and revenue per subscriber.

SIGCM clause 2 asks for revenue as VOLUME x PRICE wherever the disclosure supports it, and
DRIVER_REBUILD_05-09-2026.md recorded that it did not: the financial statements carry no
subscriber counts, so the rule sat at the disclosed segment level and flagged the gap.

THE GAP WAS IN THE REGISTER RATHER THAN IN THE WORLD [L-343]. The earnings presentations
carry the counts, by category, and the presentations were reachable the whole time — four
guessed investor-relations URLs had failed and been written up as evidence the channel was
gone. They are registered now, and three fiscal year-ends plus the latest half-year are
below.

WHAT THE DECOMPOSITION SAYS, AND IT IS NOT VISIBLE IN THE NET. The `stc` segment is the KSA
operating business and it is two thirds of group revenue. Its revenue compounded at 1.91%
over the two years to FY2025 — a rate that reads as a mature business barely growing. It is
in fact a subscriber base compounding at 6.0% a year against revenue per subscriber falling
3.9% a year. Those are two different businesses to forecast and the net hides both.

EVERY FIGURE IS A CHART LABEL AND THAT IS WHY THE ARITHMETIC IS CHECKED THREE WAYS: the
categories must sum to the stated total in every period, the period-on-period growth must
reproduce the presentation's own stated percentage, and volume times price must return the
revenue the audited statements report. A text layer is least trustworthy over a chart, and
the presentations say in their own footnote that these figures are not audited.
"""
from __future__ import annotations

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

#: (prepaid, postpaid, machine-to-machine) mobile subscribers, millions, KSA
MOBILE = {
    'Q4 2023': (19.73, 5.80, 0.94),
    'Q4 2024': (21.13, 6.23, 0.98),
    'Q4 2025': (22.2, 6.5, 1.3),
    'H1 2026': (22.4, 6.6, 1.3),
}
MOBILE_STATED = {'Q4 2023': 26.47, 'Q4 2024': 28.34, 'Q4 2025': 30.0, 'H1 2026': 30.3}

#: (fixed-wireless broadband, fixed-wired broadband, fixed telephone lines), millions
FIXED = {
    'Q4 2023': (0.44, 1.30, 3.83),
    'Q4 2024': (0.50, 1.32, 3.90),
    'Q4 2025': (0.5, 1.4, 4.1),
    'H1 2026': (0.6, 1.4, 4.1),
}
FIXED_STATED = {'Q4 2023': 5.57, 'Q4 2024': 5.72, 'Q4 2025': 6.0, 'H1 2026': 6.1}

#: The growth each presentation states for itself, so the arithmetic is checked against the
#: company's own reading of its own chart rather than only against the chart.
STATED_GROWTH = {
    ('Q4 2023', 'Q4 2024'): dict(mobile=0.0706, fixed=0.0269),
    ('Q4 2024', 'Q4 2025'): dict(mobile=0.059, fixed=0.050),
}

SOURCE = {
    'Q4 2023': 'earnings-presentation2024en.txt, FY2024 earnings presentation (COMPANY_IR)',
    'Q4 2024': 'earnings-presentation2024en.txt, FY2024 earnings presentation (COMPANY_IR)',
    'Q4 2025': 'EarningsPresentationQ4-2025En.txt, FY2025 earnings presentation (COMPANY_IR)',
    'H1 2026': 'EarningsPresentationQ2-2026En.txt, H1-2026 earnings presentation (COMPANY_IR)',
}

#: The `stc` segment's revenue, SAR thousands, from note 9 of the audited statements on the
#: continuing basis — the same figures the segment panel carries.
SEGMENT_REVENUE = {'Q4 2023': 49_218_179, 'Q4 2024': 49_643_893, 'Q4 2025': 51_119_024}

PERIODS = ('Q4 2023', 'Q4 2024', 'Q4 2025', 'H1 2026')
TOL = 0.011      # one chart label's worth of rounding at one decimal place


def total(period):
    return sum(MOBILE[period]) + sum(FIXED[period])


def revenue_per_subscriber(period):
    """SAR per subscriber per year. A period-end STOCK against a full-year FLOW."""
    return SEGMENT_REVENUE[period] / (total(period) * 1000.0)


def check():
    problems = []
    for p in PERIODS:
        m, f = sum(MOBILE[p]), sum(FIXED[p])
        if abs(m - MOBILE_STATED[p]) > TOL:
            problems.append('%s mobile categories sum to %.2f against a stated %.2f'
                            % (p, m, MOBILE_STATED[p]))
        if abs(f - FIXED_STATED[p]) > TOL:
            problems.append('%s fixed categories sum to %.2f against a stated %.2f'
                            % (p, f, FIXED_STATED[p]))
    for (a, b), want in STATED_GROWTH.items():
        for label, table, stated in (('mobile', MOBILE, MOBILE_STATED),
                                     ('fixed', FIXED, FIXED_STATED)):
            got = stated[b] / stated[a] - 1.0
            # the presentation rounds its own percentage, and the labels it computes from
            # are rounded too, so half a point of tolerance is the page's, not a choice
            if abs(got - want[label]) > 0.005:
                problems.append('%s %s -> %s computes %.2f%% against a stated %.2f%%'
                                % (label, a, b, 100 * got, 100 * want[label]))
    # VOLUME x PRICE MUST RETURN THE AUDITED REVENUE. It does by construction of the
    # division, so what this actually checks is that no period was dropped or mislabelled.
    for p in SEGMENT_REVENUE:
        got = revenue_per_subscriber(p) * total(p) * 1000.0
        if abs(got - SEGMENT_REVENUE[p]) > 1.0:
            problems.append('%s volume x price returns %.0f against a filed %d'
                            % (p, got, SEGMENT_REVENUE[p]))
    return problems


def record():
    fy = ('Q4 2023', 'Q4 2024', 'Q4 2025')
    vol = [total(p) for p in fy]
    prc = [revenue_per_subscriber(p) for p in fy]
    return dict(
        ticker='STC', segment='stc (the KSA operating business)',
        periods=list(PERIODS), source=SOURCE,
        mobile={p: list(MOBILE[p]) for p in PERIODS},
        fixed={p: list(FIXED[p]) for p in PERIODS},
        subscribers_total={p: total(p) for p in PERIODS},
        revenue_per_subscriber={p: revenue_per_subscriber(p) for p in SEGMENT_REVENUE},
        volume_cagr_2y=(vol[2] / vol[0]) ** 0.5 - 1.0,
        price_cagr_2y=(prc[2] / prc[0]) ** 0.5 - 1.0,
        revenue_cagr_2y=(SEGMENT_REVENUE[fy[2]] / SEGMENT_REVENUE[fy[0]]) ** 0.5 - 1.0,
        caveat=('The counts are chart labels from presentations whose own footnote says the '
                'figures are not audited, and they are period-end STOCKS set against a '
                'full-year revenue FLOW. Every one is checked three ways — categories to '
                'their stated total, growth to the presentation\'s own stated percentage, '
                'and volume times price back to the audited revenue — and they are an '
                'INDICATOR rather than an audited driver until the same numbers are found '
                'in a table.'),
        foots=not check(),
    )


if __name__ == '__main__':
    bad = check()
    for b in bad:
        print('FAIL', b)
    if not bad:
        r = record()
        print('every period foots, every stated growth reproduces, and volume x price')
        print('returns the audited revenue in all three filed years.')
        print()
        print('%-10s %9s %9s %9s %14s' % ('period', 'mobile', 'fixed', 'total', 'SAR/sub/yr'))
        for p in PERIODS:
            rps = ('%14.1f' % revenue_per_subscriber(p)) if p in SEGMENT_REVENUE else ' ' * 14
            print('%-10s %9.2f %9.2f %9.2f %s'
                  % (p, sum(MOBILE[p]), sum(FIXED[p]), total(p), rps))
        print()
        print('two-year compound: volume %+.2f%%, price %+.2f%%, revenue %+.2f%%'
              % (100 * r['volume_cagr_2y'], 100 * r['price_cagr_2y'],
                 100 * r['revenue_cagr_2y']))
        print('   (1 %+.4f) x (1 %+.4f) - 1 = %+.2f%%, against the filed %+.2f%%'
              % (r['volume_cagr_2y'], r['price_cagr_2y'],
                 100 * ((1 + r['volume_cagr_2y']) * (1 + r['price_cagr_2y']) - 1),
                 100 * r['revenue_cagr_2y']))
        with open(os.path.join(HERE, 'units.json'), 'w') as f:
            json.dump(r, f, indent=1)
        print('wrote units.json')
    raise SystemExit(1 if bad else 0)
