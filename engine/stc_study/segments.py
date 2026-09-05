"""STC — the disclosed segment panel, three filed years, revenue and gross profit.

WHY THIS EXISTS. The delivered study forecast four typed growth arrays — g_cbu, g_ebu,
g_wc, g_sub — with no source, date or layer on any of them, and their implied REAL growth
wanders from 0.68% to 0.00% across five years with nothing saying why. SIGCM clause 2 asks
for the finest sourced level, and this company discloses eleven to thirteen operating
segments with revenue AND gross profit for every one of them, in note 9 of each year's own
statements. That is materially finer than four arrays and it is disclosed rather than
assumed.

THE PANEL IS NOT A SINGLE TABLE AND SAYING SO IS THE POINT. Two things move between
filings and both are registered rather than smoothed:

  (i)  THE PERIMETER. FY2023 exists on two bases. As originally reported it includes TAWAL
       as a segment at 3,343,350 of revenue; as restated in the FY2024 filing, TAWAL is a
       discontinued operation and absent from the segment list altogether. The forward
       basis is the CONTINUING one, because TAWAL was sold and a forecast built on revenue
       the company no longer earns is a forecast of something that does not exist. The
       as-filed column is kept beside it because [R-FCAL-01] requires each origin to see
       what was published at the time, as originally reported.

  (ii) THE GROUPING. Segments are re-grouped between filings. Intigral is disclosed
       separately in the FY2023 and FY2024 statements and is inside "Other operating
       segments" in the FY2025 statements; iot2 and SCCC appear separately from FY2024.
       A growth rate computed across a re-grouping is a growth rate of two different
       things, so every line carries the filing each figure came from and any line whose
       composition changed is flagged rather than joined.

Every figure is read from the company's own note 9 and each column foots to the stated
total, which is asserted below rather than said in prose.
"""
from __future__ import annotations

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

#: source = the filing each column was read from. SAR thousands.
FY2025_FILING = 'stc_Annual-2025-en.txt, note 9 (audited, year ended 31 December 2025)'
FY2024_FILING = 'stc_Annual-2024-en.txt, note 9 (audited, year ended 31 December 2024)'
FY2023_FILING = 'STC_FY2023_FS_en.txt, note 9 (audited, year ended 31 December 2023)'

# ---------------------------------------------------------------------------------------
# CONTINUING-OPERATIONS BASIS. FY2025 and FY2024 from the FY2025 filing; FY2023 from the
# FY2024 filing, which is the only place a continuing-basis FY2023 exists.
# ---------------------------------------------------------------------------------------
REVENUE = {
    #  segment            FY2023       FY2024       FY2025
    'stc':              (49_218_179, 49_643_893, 51_119_024),
    'Channels':         (14_194_210, 15_110_606, 14_085_195),
    'Solutions':        (11_040_493, 12_063_897, 12_730_189),
    'stc Kuwait':        (3_986_034,  4_105_483,  4_179_842),
    'stc Bahrain':       (1_913_287,  1_927_967,  1_967_830),
    'Center 3':          (1_089_218,  1_911_716,  1_961_666),
    'stc Bank':          (1_063_006,  1_261_646,  1_401_027),
    'Sirar':               (588_606,    732_675,    826_545),
    'Specialized':         (397_492,    371_763,    355_306),
    'iot2':                 (72_539,    301_434,    321_668),
    'SCCC':                 (72_150,    187_904,    303_969),
    # Intigral is disclosed separately in FY2023 and FY2024 and sits inside "Other" in
    # FY2025, so the FY2025 filing's own FY2024 comparative already folds it in. The
    # FY2023 and FY2024 figures below are the FY2024 filing's, and are NOT comparable
    # across the grouping change — flagged, never joined.
    'Other operating segments': (66_529 + 643_314, 729_345, 65_059),
    'Eliminations / adjustments': (-12_567_896, -12_454_916, -11_498_645),
}
GROSS_PROFIT = {
    'stc':              (29_973_976, 31_178_645, 30_628_607),
    'Channels':          (3_083_568,  3_365_489,  3_429_410),
    'Solutions':         (2_792_163,  2_981_285,  2_932_415),
    'stc Kuwait':        (2_061_419,  2_019_660,  2_139_245),
    'stc Bahrain':         (878_634,    949_684,  1_008_601),
    'Center 3':            (483_553,    747_048,    818_319),
    'stc Bank':            (207_653,    344_985,    724_914),
    'Sirar':               (173_207,    268_317,    283_341),
    'Specialized':         (178_078,    185_327,    135_410),
    'iot2':                 (26_948,     88_538,     71_617),
    'SCCC':                (-70_021,    -18_539,     78_538),
    'Other operating segments': (60_808 + 445_684, 505_609, 34_055),
    'Eliminations / adjustments': (-5_555_604, -5_290_124, -4_584_783),
}
YEARS = ('FY2023', 'FY2024', 'FY2025')
STATED_REVENUE = (71_777_161, 75_893_413, 77_818_675)
STATED_GROSS_PROFIT = (34_740_066, 37_325_924, 37_699_689)

#: A line whose composition CHANGED between the filings this panel spans. A growth rate
#: computed across one of these is a growth rate of two different things.
REGROUPED = {
    'Other operating segments': (
        'Intigral is disclosed separately in the FY2023 and FY2024 statements (643,314 and '
        '686,001 of revenue) and sits inside this line in the FY2025 statements. The FY2023 '
        'and FY2024 figures here ADD Intigral back so the column foots to the stated total, '
        'and no growth rate may be taken across the change.'),
    'Center 3': (
        'Revenue rises from 1,089,218 to 1,911,716 between FY2023 and FY2024, a step of 76% '
        'that is a scale-up of a new data-centre business rather than a growth rate to '
        "project. Its FY2024 gross profit ALSO differs between the two filings — 721,534 in "
        'the FY2024 statements against 747,048 in the FY2025 comparative — which is why ONE '
        'FILING PER COLUMN is a rule here and not a preference: mixing them was this '
        "panel's own first-draft error, and the footing check found it in the same minute."),
    'iot2': 'Revenue rises fourfold between FY2023 and FY2024 from a base under 0.1% of group.',
    'SCCC': 'Gross profit is NEGATIVE in FY2023 and FY2024, so a margin is not defined.',
}

#: The FY2023 column as ORIGINALLY REPORTED, for the point-in-time record [R-FCAL-01].
#: It carries TAWAL, which the continuing basis above does not.
AS_FILED_FY2023 = {
    'revenue': {
        'stc': 49_218_179, 'Channels': 14_194_210, 'Solutions': 11_040_493,
        'stc Kuwait': 4_278_282, 'Tawal': 3_343_350, 'stc Bahrain': 1_913_287,
        'stc Bank': 1_063_006, 'Intigral': 643_314, 'Sirar': 588_606,
        'Specialized': 397_492, 'Other operating segments': 1_300_436,
        'Eliminations / adjustments': -15_644_044,
    },
    'stated_total': 72_336_611,
    'source': FY2023_FILING,
}


def check():
    """Every column foots to the total its own filing states. Arithmetic is the arbiter."""
    problems = []
    for label, table, stated in (('revenue', REVENUE, STATED_REVENUE),
                                 ('gross profit', GROSS_PROFIT, STATED_GROSS_PROFIT)):
        for i, y in enumerate(YEARS):
            got = sum(v[i] for v in table.values())
            if got != stated[i]:
                problems.append('%s %s sums to %s against a stated %s (out by %s)'
                                % (label, y, f'{got:,}', f'{stated[i]:,}',
                                   f'{got - stated[i]:,}'))
    got = sum(AS_FILED_FY2023['revenue'].values())
    if got != AS_FILED_FY2023['stated_total']:
        problems.append('as-filed FY2023 revenue sums to %s against a stated %s'
                        % (f'{got:,}', f"{AS_FILED_FY2023['stated_total']:,}"))
    if set(REVENUE) != set(GROSS_PROFIT):
        problems.append('the revenue and gross-profit tables do not carry the same lines')
    return problems


def record():
    return dict(
        ticker='STC', years=list(YEARS),
        basis=('continuing operations, which is the basis the company reports on after the '
               'TAWAL disposal and the basis a forward valuation needs'),
        sources=dict(FY2025=FY2025_FILING, FY2024=FY2024_FILING, FY2023=FY2024_FILING,
                     FY2023_as_filed=FY2023_FILING),
        revenue={k: list(v) for k, v in REVENUE.items()},
        gross_profit={k: list(v) for k, v in GROSS_PROFIT.items()},
        stated_totals=dict(revenue=list(STATED_REVENUE),
                           gross_profit=list(STATED_GROSS_PROFIT)),
        regrouped=REGROUPED,
        as_filed_fy2023=AS_FILED_FY2023,
        foots=not check(),
    )


if __name__ == '__main__':
    bad = check()
    for b in bad:
        print('FAIL', b)
    if not bad:
        print('all six columns foot to their own filing\'s stated total,')
        print('and the as-filed FY2023 column foots to 72,336,611.')
        for i, y in enumerate(YEARS):
            print('  %s revenue %14s   gross profit %13s   margin %6.2f%%'
                  % (y, f'{STATED_REVENUE[i]:,}', f'{STATED_GROSS_PROFIT[i]:,}',
                     100.0 * STATED_GROSS_PROFIT[i] / STATED_REVENUE[i]))
        with open(os.path.join(HERE, 'segments.json'), 'w') as f:
            json.dump(record(), f, indent=1)
        print('wrote segments.json')
    raise SystemExit(1 if bad else 0)
