"""STC — the asset-conversion cycle, measured from the filed statements.

SIGCM CLAUSE 4 requires days sales outstanding, days inventory and days payable to be
studied from the statements and the balance sheet and cash flow PROJECTED from them, with no
unexplained plugs where the drivers are disclosed. The rebuilt model does none of that: it
carries a working-capital OUTFLOW as a share of revenue, a single number per year with no
balance sheet behind it, which is the plug the clause forbids.

WHAT THE FILINGS ACTUALLY DISCLOSE, and it is more than the usual three lines:

  RECEIVABLES come with an ageing analysis and an expected-credit-loss rate per bucket, and
  the note states how much sits with government and government-related entities — 22,577
  million of 30,086,398 gross in FY2025, three quarters of the book. A telecom whose
  receivable book is mostly sovereign does not collect on ordinary commercial terms and the
  measured days say so.

  INVENTORY carries its OWN cost base: "inventories recognised as an expense within cost of
  sales during the year amounted to 11,899 million (2024: 11,939 million)". That is the
  denominator days-inventory actually wants, disclosed, rather than a cost of revenues total
  that includes network access charges and government levies no inventory passes through.
  Using the wrong denominator here understates the days by a factor of about four.

  PAYABLES carry a DISCLOSED SETTLEMENT RANGE — "normally settled by the Group on average
  range of 90-107 days" — which is a sourced anchor rather than an inference, and holding
  the measured days against it produced the most useful result in this file. THEY DO NOT
  RECONCILE, AND THE DISCLOSURE IS NOT WHAT IS WRONG: measured against the inventory cost
  base the trade payable runs 161, 185 and 229 days, roughly twice the stated range and
  rising. The reason is that trade payables are not bought only against inventory — network
  access, contractors and services are on trade terms too — so the denominator is too narrow
  and the ratio is measuring a payable against a fraction of what it pays for. The purchases
  actually bought on trade terms are not disclosed, so the RIGHT denominator cannot be
  built. That is recorded rather than repaired: the disclosed range is the sourced figure,
  the computed days are a diagnostic that says so, and the balance-sheet projection uses the
  WHOLE payables line against cost of revenues, which is at least a consistent pair.

TRADE PAYABLES ARE SEPARATED FROM THE REST OF THE PAYABLES LINE, deliberately. The balance
sheet's 22,259,436 is five things: accrued expenses, trade payables, employee accruals,
notes payable and others. Only the trade portion is bought on supplier terms, and computing
days payable on the whole line would divide a figure containing employee accruals by a cost
of goods, which is two different things over each other. The measured trade days are
published beside the disclosed range so the two can be compared honestly.
"""
from __future__ import annotations

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
YEARS = ('FY2023', 'FY2024', 'FY2025')

FY2025_FILING = 'stc_Annual-2025-en.txt, notes 17, 18 and 32 (audited, 31 December 2025)'
FY2023_FILING = 'stc_Annual-2024-en.txt, notes 17, 18 and 32 (audited, 31 December 2024)'

#: Trade receivables NET of the impairment allowance — what the balance sheet carries.
TRADE_RECEIVABLES = (21_401_271, 22_223_164, 26_727_198)
TRADE_RECEIVABLES_GROSS = (23_786_025, 25_602_745, 30_086_398)
RECEIVABLES_ALLOWANCE = (-2_384_754, -3_379_581, -3_359_200)

#: Inventories net of the slow-moving allowance.
INVENTORIES = (1_904_971, 1_889_227, 1_923_203)
#: The note's OWN cost base for them, in SAR THOUSANDS (the note states millions).
INVENTORY_EXPENSE = (11_023_000, 11_939_000, 11_899_000)

#: The whole payables line, and the trade portion inside it.
PAYABLES_TOTAL = (21_823_200, 22_627_472, 22_259_436)
TRADE_PAYABLES = (4_875_450, 6_048_267, 7_452_911)

#: CONTRACT ASSETS AND LIABILITIES, which on a telecom are working capital and are not
#: optional: unbilled revenue on services, device instalment plans and network installation
#: sits in contract assets, and prepaid cards and loyalty points sit in contract
#: liabilities. Leaving them out would model the working capital of a company that bills in
#: advance and settles in cash, which this is not. Contract assets rose 1,543,491 inside the
#: reviewed half alone — larger than every other working-capital movement in it put together.
CONTRACT_ASSETS = (7_963_387, 8_722_920, 9_224_434)
CONTRACT_LIABILITIES = (5_244_341, 5_237_420, 5_359_851)

REVENUE = (71_777_161, 75_893_413, 77_818_675)

#: THE LATEST DISCLOSED SHEET — the reviewed interim at 30 June 2026, which is what the
#: bridge already stands on and therefore what the days must be anchored on [R-ANCHOR-01].
#: Receivables are essentially UNCHANGED across the half (26,727,198 to 26,727,997, eight
#: hundred thousand on a twenty-seven billion book) while revenue grew, so days sales
#: outstanding falls on its own without anything being assumed.
H1_2026 = dict(trade_receivables=26_727_997, inventories=1_781_441,
               payables_total=21_198_207,
               contract_assets=9_971_423 + 1_287_416,
               contract_liabilities=3_727_610 + 680_466,
               date='2026-06-30',
               source='the reviewed interim to 30 June 2026, statement of financial '
                      'position and notes 10 and 14')
#: Cost of revenues as the cost note states it — the denominator for the payables the note
#: does NOT break out, and published beside the inventory-specific one rather than instead.
COST_OF_REVENUES = (37_037_095, 38_567_489, 40_118_986)

#: DISCLOSED, not inferred: note 32's own statement of settlement terms.
DISCLOSED_PAYMENT_DAYS = (90, 107)
DISCLOSED_PAYMENT_SOURCE = ('note 32 of the FY2025 audited statements: trade payables "are '
                            'non-interest bearing and are normally settled by the Group on '
                            'average range of 90-107 days"')

#: Receivables owed by government and government-related entities, gross.
GOVERNMENT_RECEIVABLES = (None, 18_567_000, 22_577_000)

DAYS = 365


def dso(i):
    """Days sales outstanding on the NET receivable against revenue."""
    return DAYS * TRADE_RECEIVABLES[i] / REVENUE[i]


def dio(i):
    """Days inventory on the note's OWN cost base, never on cost of revenues.

    Cost of revenues carries network access charges, government levies and employee costs,
    none of which passes through inventory; dividing by it would understate the days by
    roughly a factor of four and would be measuring nothing.
    """
    return DAYS * INVENTORIES[i] / INVENTORY_EXPENSE[i]


def dpo_trade(i):
    """Days payable on the TRADE portion alone, against the inventory cost base."""
    return DAYS * TRADE_PAYABLES[i] / INVENTORY_EXPENSE[i]


def dpo_total(i):
    """The whole payables line against cost of revenues — a different quantity, published
    beside the trade measure because the balance sheet projection needs the whole line."""
    return DAYS * PAYABLES_TOTAL[i] / COST_OF_REVENUES[i]


def dco(i):
    """Days of contract asset — unbilled revenue — against revenue."""
    return DAYS * CONTRACT_ASSETS[i] / REVENUE[i]


def dcl(i):
    """Days of contract liability — billed in advance — against revenue."""
    return DAYS * CONTRACT_LIABILITIES[i] / REVENUE[i]


def cash_cycle(i):
    """The conventional cycle, contract balances included.

    IT MIXES DENOMINATORS AND THAT IS THE STANDARD CONSTRUCTION, not a defect — days sales
    outstanding sits on revenue while days inventory and days payable sit on cost — but it
    means THIS NUMBER IS NOT NET WORKING CAPITAL IN DAYS OF REVENUE and must never be read
    as one. On this book the two differ by a factor of three: the cycle computes to about
    nineteen days at the latest sheet while net working capital is seventeen and a half per
    cent of revenue, which is sixty-four days. A ratio between quantities defined
    differently is not evidence about either, so both are published and the PROJECTION uses
    the second, because that is the one an actual balance sheet obeys.
    """
    return dso(i) + dio(i) + dco(i) - dpo_total(i) - dcl(i)


def net_working_capital(i):
    return (TRADE_RECEIVABLES[i] + INVENTORIES[i] + CONTRACT_ASSETS[i]
            - PAYABLES_TOTAL[i] - CONTRACT_LIABILITIES[i])


def nwc_share(i):
    """Net working capital as a share of revenue — what the projection actually runs on."""
    return net_working_capital(i) / REVENUE[i]


def anchored_days(annualised_revenue, annualised_cost, annualised_inventory_cost):
    """The days as at the LATEST DISCLOSED sheet, each against its own annualised driver.

    Anchored on the reviewed half rather than on the last full year, which is the same rule
    the rest of this study's rates obey: a near-term reviewed actual outranks a stale
    full-year figure, and here it moves the answer because receivables stood still through a
    half in which revenue grew.
    """
    h = H1_2026
    return dict(
        dso=DAYS * h['trade_receivables'] / annualised_revenue,
        dio=DAYS * h['inventories'] / annualised_inventory_cost,
        dpo_total=DAYS * h['payables_total'] / annualised_cost,
        dco=DAYS * h['contract_assets'] / annualised_revenue,
        dcl=DAYS * h['contract_liabilities'] / annualised_revenue,
        anchored_on=h['date'], source=h['source'])


def government_share(i):
    g = GOVERNMENT_RECEIVABLES[i]
    return None if g is None else g / TRADE_RECEIVABLES_GROSS[i]


def check():
    problems = []
    for i, y in enumerate(YEARS):
        if TRADE_RECEIVABLES_GROSS[i] + RECEIVABLES_ALLOWANCE[i] != TRADE_RECEIVABLES[i]:
            problems.append('%s receivables gross less the allowance is %s against a net %s'
                            % (y, f'{TRADE_RECEIVABLES_GROSS[i] + RECEIVABLES_ALLOWANCE[i]:,}',
                               f'{TRADE_RECEIVABLES[i]:,}'))
        if TRADE_PAYABLES[i] >= PAYABLES_TOTAL[i]:
            problems.append('%s trade payables are not inside the payables line' % y)
        if not 0 < dio(i) < 365:
            problems.append('%s days inventory computes to %.1f' % (y, dio(i)))
    # THE DISCLOSED RANGE IS A CHECK ON THE MEASUREMENT, not a substitute for it, and on
    # this book the two do not reconcile — which is a finding about the DENOMINATOR rather
    # than an error to correct. It has to be VISIBLE, which is what this records.
    outside = [YEARS[i] for i in range(3)
               if not DISCLOSED_PAYMENT_DAYS[0] <= dpo_trade(i) <= DISCLOSED_PAYMENT_DAYS[1]]
    return problems, outside


def record():
    problems, outside = check()
    return dict(
        ticker='STC', years=list(YEARS),
        sources=dict(FY2025=FY2025_FILING, FY2024=FY2025_FILING, FY2023=FY2023_FILING),
        trade_receivables=list(TRADE_RECEIVABLES),
        inventories=list(INVENTORIES),
        inventory_expense=list(INVENTORY_EXPENSE),
        payables_total=list(PAYABLES_TOTAL), trade_payables=list(TRADE_PAYABLES),
        dso=[dso(i) for i in range(3)],
        dio=[dio(i) for i in range(3)],
        dpo_trade=[dpo_trade(i) for i in range(3)],
        dpo_total=[dpo_total(i) for i in range(3)],
        contract_assets=list(CONTRACT_ASSETS),
        contract_liabilities=list(CONTRACT_LIABILITIES),
        dco=[dco(i) for i in range(3)], dcl=[dcl(i) for i in range(3)],
        cash_cycle=[cash_cycle(i) for i in range(3)],
        net_working_capital=[net_working_capital(i) for i in range(3)],
        nwc_share_of_revenue=[nwc_share(i) for i in range(3)],
        latest_disclosed=H1_2026,
        denominator_caveat=(
            'The conventional cash conversion cycle mixes denominators — receivable days on '
            'revenue, inventory and payable days on cost — which is the standard '
            'construction and is NOT net working capital in days of revenue. On this book '
            'the two differ by a factor of three, so both are published and the projection '
            'runs on net working capital as a share of revenue, which is the one an actual '
            'balance sheet obeys.'),
        disclosed_payment_days=list(DISCLOSED_PAYMENT_DAYS),
        disclosed_payment_source=DISCLOSED_PAYMENT_SOURCE,
        measured_trade_days_outside_disclosed_range=outside,
        government_receivable_share=[government_share(i) for i in range(3)],
        finding=(
            'Days sales outstanding runs %.1f, %.1f and %.1f — RISING, and the receivable '
            'book is mostly sovereign: government and government-related entities owed '
            '%s million of %s million gross in FY2025, %.0f%% of the book. A telecom '
            'collecting three quarters of its receivables from the state does not collect '
            'on commercial terms, and the days say so rather than the study assuming a '
            "norm. Days inventory is %.1f on the note's OWN cost base and would read %.1f "
            'against cost of revenues — a factor of %.1f, which is the difference between '
            'measuring a real cycle and dividing two unrelated numbers.'
            % (dso(0), dso(1), dso(2),
               f'{GOVERNMENT_RECEIVABLES[2] // 1000:,}',
               f'{TRADE_RECEIVABLES_GROSS[2] // 1000:,}',
               100 * government_share(2), dio(2),
               DAYS * INVENTORIES[2] / COST_OF_REVENUES[2],
               dio(2) / (DAYS * INVENTORIES[2] / COST_OF_REVENUES[2]))),
        payables_finding=(
            'The measured trade payable days — %.1f, %.1f, %.1f — do not reconcile with the '
            'settlement range the filings state, 90 to 107 days, and the disclosure is not '
            'what is wrong. Trade payables are not bought only against inventory: network '
            'access, contractors and services sit on trade terms too, so the inventory cost '
            'base is a fraction of what the payable pays for and the ratio runs about twice '
            'the stated range. The purchases actually on trade terms are not disclosed, so '
            'the right denominator cannot be built and is not invented; the balance-sheet '
            'projection uses the WHOLE payables line against cost of revenues, which is at '
            'least a consistent pair.'
            % (dpo_trade(0), dpo_trade(1), dpo_trade(2))),
    )


if __name__ == '__main__':
    problems, outside = check()
    for p in problems:
        print('FAIL', p)
    if not problems:
        print('%-34s %10s %10s %10s' % ('', *YEARS))
        for lab, fn in (('days sales outstanding', dso), ('days inventory', dio),
                        ('days of contract asset', dco),
                        ('days payable, trade only', dpo_trade),
                        ('days payable, whole line', dpo_total),
                        ('days of contract liability', dcl),
                        ('cash conversion cycle (mixed bases)', cash_cycle),
                        ('net working capital, % of revenue',
                         lambda i: 100 * nwc_share(i))):
            print('%-34s %10.1f %10.1f %10.1f' % (lab, *[fn(i) for i in range(3)]))
        print()
        print('  the filings state trade payables settle on 90-107 days; the measured trade')
        print('  days are %s' % ', '.join('%.1f' % dpo_trade(i) for i in range(3))
              + (' — outside that range in %s' % ', '.join(outside) if outside
                 else ' — inside it in every year'))
        print('  government and related entities owe %.0f%% of the gross book (FY2025)'
              % (100 * government_share(2)))
        with open(os.path.join(HERE, 'working_capital.json'), 'w') as f:
            json.dump(record(), f, indent=1)
        print('\nwrote working_capital.json')
    raise SystemExit(1 if problems else 0)
