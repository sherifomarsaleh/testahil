#!/usr/bin/env python3
"""The rebuild ledger for the H1 2026 re-strike [R-REBUILD-01].

The levers in the ORDER APPLIED, each with the answer either side of it, each naming the
rule it serves, and the audit point declared BEFORE the first lever ran.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from rebuild_ledger import Ledger, assert_rebuild, render

D = json.load(open(os.path.join(HERE, 'study_numbers.json')))

L = Ledger(
    ticker='ADNOCLS', started_at='2026-09-07',
    start_value=5.605379, start_spot=6.80,
    audit_after=(
        'the tanker cost and scale rebuild — lever five — and BEFORE any smaller unit is '
        'touched. DECLARED BEFORE THE FIRST LEVER RAN, and the reasoning is that levers '
        'one to three are record and balance-sheet moves whose direction is known and '
        'bounded (net debt falls 162,549 thousand, which is about eight fils a share), '
        'while levers four and five carry the whole scale correction and PULL OPPOSITE '
        'WAYS: the second quarter the company actually reported is far above the estimate '
        'the delivered edition carried for it, and the third quarter it has disclosed is '
        'far BELOW the second, so the reversion now starts lower; and the cost rebuild '
        'moves the tanker unit\'s earnings leverage off the 1.0 the delivered '
        'construction assumed. The place to stop is where the scale correction has landed '
        'and before anything smaller is touched, because if the answer has moved a long '
        'way it must be the tanker leg and nothing else, and that is only checkable at '
        'that point.'))

L.apply('the four half-year documents swept in', 'SIGCM clause 1 / Step 2A', 5.605379,
        why='The reviewed six-month statements, the management discussion, the earnings '
            'release and the first-half earnings presentation — all dated 10 or 11 August '
            '2026 and public for twenty-seven days — were registered, read and footed. '
            'THE RULE IS THAT EVERY DISCLOSED QUARTER IS SWEPT IN BEFORE THE BUILD '
            'STARTS, and the edition delivered earlier the same day declared its '
            'information set closed at the first quarter. The sweep is a record move and '
            'moves no number by itself.',
        evidence='sweep_register.json: findings P3b, P3c, P3d and P4b; study year FY2026 '
                 'declared with quarters Q1 2026 and Q2 2026; a fourth primary-access '
                 'attempt logged with the miss stated in it')
L.apply('the base period moves from the quarter to the reviewed half', 'R-ANCHOR-01',
        5.484,
        why='Valuation date 31 March 2026 → 30 June 2026, so the discounting stub falls '
            'from 0.75 of a year to 0.50 and the free cash flow already inside the '
            'balance sheet rises from the quarter\'s 130,000 to the half\'s 598,095. The '
            'depreciation rate and the non-vessel depreciation run rate are re-solved on '
            'the half rather than the quarter. IT COSTS 0.12 A SHARE AND THE REASON IS '
            'THE COMPANY DISTRIBUTING CASH: the half generated 598,095 and paid out '
            '166,563 of dividends, 49,633 of perpetual coupons and 28,530 to minorities, '
            'and a buyer at 30 June does not receive what was paid before it.',
        evidence='STUB 0.50, BASE_FCF = h1_26_fcf = 598,095; dep_rate_ppe re-solved on '
                 'the half\'s own average balance')
L.apply('the bridge onto the 30 June 2026 balance sheet', 'R-BRIDGE-01', 5.353,
        why='Net debt 419,867 → 257,318, deferred consideration 301,462 → 304,297, '
            'perpetual securities, minorities, joint ventures at book, cash, intangibles, '
            'goodwill and working capital all re-read at 30 June. THE VALUE FALLS DESPITE '
            'NET DEBT FALLING 162,549, and the reason is worth stating because it is the '
            'opposite of the obvious reading: the drawn debt in the market-value weights '
            'falls from 1,115,212 to 800,000, so the equity weight rises, so the weighted '
            'cost of capital rises — and on a company this lightly levered that is worth '
            'more than the debt reduction.',
        evidence='bridge_record.balance_sheet_date 2026-06-30; the disclosed net debt is '
                 'FOOTED rather than taken — the stated definition omits loans and other '
                 'borrowings and only including them reproduces the published 257,318')
L.apply('the tanker price driver: the reported quarters and the disclosed third',
        'R-ANCHOR-01', 5.660,
        why='The delivered edition estimated the second quarter of 2026 off the May '
            'earnings call — 260,000 a day for a very large crude carrier against a '
            'published 291,145, and 55,000 for an LR1 against 80,206. Those are now '
            'reported. The third quarter is DISCLOSED to 11 August with the share of '
            'vessel days already contracted, and is taken on those days with the balance '
            'at the mid-cycle rate; the fourth reverts halfway from there on the SAME '
            'reversion weight of 0.50 the delivered edition carried — the parameter is '
            'unchanged and only its anchor moved. The charter book is re-read: eight of '
            'the eleven fixtures carry LATER expiries in the first-half deck.',
        evidence='tce_*_q2_26_actual, tce_*_q3_26 with cover_*_q3_26; CHARTER_TABLE '
                 'rebuilt from the first-half deck; measured with the delivered cost '
                 'construction held fixed, so this lever is the price move alone')
L.apply('the tanker cost stack and the revenue gross-up, both measured',
        'R-ANCHOR-01 / margins-are-outputs', 6.610,
        why='THE DELIVERED CONSTRUCTION IS FALSIFIED BY THE COMPANY\'S OWN HALF. It set '
            'tanker earnings equal to the owned fleet\'s charter-equivalent revenue less '
            'one running cost per vessel-day solved on 2025 — an earnings leverage of '
            'exactly 1.0 on the rate. At the published rates those 52 ships earned '
            '805,808 in the six months to 30 June 2026 and the unit reported EARNINGS of '
            '994,166, more than the fleet can earn before any cost at all, because it '
            'also trades chartered-in tonnage and serves the parent. The cost side is '
            'rebuilt as a fixed base plus a variable component per unit of fleet '
            'charter-equivalent revenue, both solved from the audited 2025 year and the '
            'reviewed half TOGETHER, with the reviewed first half of 2025 HELD OUT and '
            'reproduced to within 10.7 per cent, understating it. The revenue gross-up '
            'moves from 1.60 — inferred from one quarter — to the half\'s measured 2.609; '
            'the year says 2.734 and the prior half 2.794, so THE QUARTER WAS THE '
            'OUTLIER, at 1.51 against the second quarter\'s 3.16.',
        evidence='tnk_cost_fixed, tnk_cost_var, tnk_grossup_26, tnk_holdout_ebitda_error; '
                 'four assertions in compute.py, including that the reviewed half earned '
                 'more than its owned fleet could')
L.apply('the remaining units re-anchored on the reviewed half', 'R-ANCHOR-01', 6.270,
        why='Every unit\'s 2026 is now the REPORTED half plus a second half at the margin '
            'that half itself delivered. Four typed margins meet four measured ones and '
            'they move in both directions: Offshore Contracting 0.385 against a half of '
            '0.316 (0.388 before the disclosed credit-loss provision, which is named and '
            'removed), Offshore Services 0.287 against 0.241, Dry-Bulk 0.184 against '
            '0.355, Services 0.200 against 0.275. OFFSHORE PROJECTS IS THE LARGE ONE: the '
            'delivered edition carried 125,000 of 2026 revenue recovering to 300,000 by '
            '2030 on a company range the half has falsified — the unit earned 1,884 in '
            'six months and lost 16,959 — so it is held flat at the half\'s own level '
            'with no margin, because NO NEW AWARD IS DISCLOSED and a recovery nothing '
            'discloses is not forecast. Dry-bulk reverts to its 2025 outcome by 2030 on '
            'the same mechanism as the charter rates, because its rates spiked the same '
            'way and the company publishes the series that shows it.',
        evidence='DRV rebuilt from H1_SEG; SEG_ONEOFF_26 names the one removal; '
                 'SEG_REVERT_FY25 names the one reverting unit')
L.apply('the gas unit: the margin measured, the volume path held and priced both ways',
        'R-ANCHOR-01 / SIGCM clause 8', 5.339,
        why='THE MARGIN WAS A TYPED INPUT AND IS NOW MEASURED: 0.70, set "near the 2025 '
            'outcome", against a reviewed half of 0.4966 on revenue up 128 per cent — the '
            'new carriers entered on chartering terms rather than the 2025 book\'s. That '
            'is most of this lever. THE VOLUME PATH IS NOT REBUILT and the reason is '
            'SIGCM clause 8: the first-half deck prints the same contract table as April '
            'with the four liquefied-natural-gas carriers\' firm period ending in June '
            '2026, which would cut consolidated vessel-years from 12.0/18.0/26.25/30.0 to '
            '10.0/13.0/17.5/20.75 — but the table\'s own heading reads "No. of Vessels '
            'CONTRACTED" and a bullet on the same slide describes five Das carriers being '
            'moved onto long-term contracts from the same month, so whether those ships '
            'stop EARNING or stop being COUNTED is not decidable from the page. The '
            'April composition is kept, the first half is taken from the two quarters the '
            'tables agree on, and the difference is priced as a contested judgement at '
            '-14.6 per cent rather than resolved silently.',
        evidence='gas_margin measured on the half; GAS_VY_H1D published beside GAS_VY; '
                 'gas_vy_alt_fv 4.5614 in the contested record')
L.apply('the strike moves to the latest known price', 'R-GAP-01 AMENDED', 5.338,
        why='AED 6.16 as at 7 August 2026 → AED 6.80 as at 7 September 2026, read from '
            'engine/prices/SUPPLIED_07-09-2026.json rather than typed. A higher price '
            'raises the market-value equity weight and therefore the cost of capital, '
            'which is why moving the strike moves the value at all. TWO CLOCKS ARE KEPT '
            'APART: the probability cone and the technical read stand on the daily series '
            'this repository holds, which ends 7 August 2026, and a fundamental rebuild '
            'does not re-strike a cone. Both dates are published.',
        evidence='spot_aed read from the committed price file; price_close_engine carries '
                 'the cone\'s own close of 6.16 with its date')
L.apply('the interim dividend declared after the balance-sheet date', 'R-BRIDGE-01', 5.338,
        why='The board approved an interim cash dividend of USD 85.3 million for the '
            'second quarter on a record date of 20 August 2026 — after the sheet this '
            'bridge stands on and before the price this study is delivered against, so a '
            'buyer at that price does not receive it. Worth about two fils a share and '
            'deducted from EQUITY value rather than from enterprise value.',
        evidence='div_declared_q2_26; a printed line in the bridge, the sum-of-the-parts '
                 'bridge and both alternative bridges, all of which foot')

assert abs(L.value - D['central']) < 0.005, (
    f"the ledger's last lever must reach the published answer: {L.value} vs {D['central']}")

_asd = __import__('dataclasses').asdict(L)
for _lv, _obj in zip(_asd['levers'], L.levers):
    _lv['move'] = _obj.move
REC = dict(
    **_asd,
    value=L.value, cumulative_move=L.cumulative, rules=L.by_rule(),
    distinct_rules=len(L.by_rule()),
    start_gap=L.start_value / L.start_spot - 1.0,
    note=(
        'A RE-STRIKE ON FILINGS THE PREVIOUS EDITION NEVER OPENED. Nine levers, five '
        'rules. The cumulative move is small — 5.6054 to 5.3385, minus 4.8 per cent — and '
        'that is the least interesting thing in this ledger, because the route runs '
        '5.6054 down to 5.3530 on the balance sheet, up to 6.6100 on the tanker rebuild '
        'and back down to 5.3385 on the smaller units. TWO CORRECTIONS OF SIMILAR SIZE '
        'PULLING OPPOSITE WAYS IS NOT THE SAME EVIDENCE AS TWO SMALL ONES, and a rebuild '
        'reporting only the net would have published a number nobody could decompose.'),
    audit=dict(
        reached='the declared audit point — after the tanker cost and scale rebuild and '
                'before any smaller unit was touched.',
        finding=(
            'THE SCALE CORRECTION LANDED WHERE IT WAS PREDICTED TO AND NOWHERE ELSE. At '
            'the audit point the answer stood at 6.610 against a start of 5.6054, and the '
            'whole of the rise is levers four and five: +0.31 from the rates the company '
            'has published since, +0.95 from the cost stack. Levers one to three moved it '
            'DOWN by 0.25, which was not predicted in direction — the base-period move '
            'costs 0.12 because the company distributed cash in the second quarter, and '
            'the bridge costs another 0.13 because de-levering raises a market-value '
            'weighted cost of capital by more than the debt reduction is worth. THE '
            'PREDICTION THAT LEVERS 4 AND 5 WOULD PULL OPPOSITE WAYS WAS WRONG: both '
            'raised the answer, because the disclosed third-quarter rate is still far '
            'above mid-cycle and the leverage correction reaches every forecast year.'),
        consequence=(
            'At the audit point the gap was -2.8 per cent against 6.80 — inside [R-GAP-01]'
            '\'s band. It did not stay there, and that is the reason the audit point is '
            'declared in advance rather than chosen: the four levers after it took the '
            'answer to 5.3385 and the gap to -21.5 per cent. NOTHING WAS FITTED TO THE '
            'PRICE IN EITHER DIRECTION — the price enters no driver, every parameter is '
            'solved from the audited 2025 year or the reviewed 2026 half, the one free '
            'parameter in the rate path was left at its delivered value of 0.50 and only '
            'its anchor moved, and the held-out half is UNDER-reproduced by 10.7 per '
            'cent. The gap owes its eight-heading review and gets one.'),
        after_the_audit_point=(
            'FOUR FURTHER LEVERS, and the audit point earned its place. Two of them — the '
            'remaining units and the gas margin — took 1.27 off the answer between them, '
            'more than the balance-sheet levers and the price move combined, and neither '
            'was expected to be material when the order was fixed. A ledger that recorded '
            'only the net would have shown a -4.8 per cent rebuild and hidden a 1.27 '
            'swing inside it.')),
)
json.dump(REC, open(os.path.join(HERE, 'rebuild_ledger.json'), 'w'), indent=1, default=float)
assert_rebuild(REC, ticker='ADNOCLS')
print(render(REC))
print(f"\nledger written — {len(L.levers)} levers, {len(L.by_rule())} rules, "
      f"cumulative {L.cumulative:+.2%}")
