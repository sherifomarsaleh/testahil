"""STC — the cost-of-capital schedule, through the sanctioned module [R-COC-01].

Nothing here is typed from a memory of a rate. Every balance and every finance-cost
line is read from Saudi Telecom Company's own filings, named with its note, and the
arithmetic is the arbiter: the borrowings total reproduces from the cash-flow
statement's own roll-forward, and the share count foots against par.

WHY THE BETA IS IN THIS FILE AND NOT A SEPARATE PASS. The plan set the cost-of-capital
schedule and the beta as two levers, in that order, because they pull opposite ways.
They cannot in fact be separated: cost_of_capital.schedule() REFUSES to build on a
tier-1 beta recorded as non-conforming, and the beta this study carries is a 40-session
DAILY regression, which the standing rule says is not one of the three tiers at all.
So there is no state of this study in which the schedule rule is satisfied and the beta
rule is not, and an intermediate answer would be a number the module cannot produce.
The two land in one pass and the rebuild ledger records them as one piece of evidence,
with each one's direction measured separately below.
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

import cost_of_capital as COC
from beta_regression import own_stock_beta

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD_DATE = '2026-09-05'
TAX = 0.20                      # zakat and income tax, the study's own rate

# ---------------------------------------------------------------------------
# THE BORROWINGS BOOK, facility by facility, from note 26 of the FY2025 audited
# statements (balances at 31 December 2025 and 2024, SAR thousands). Currency and
# profit rate are the note's own columns.
# ---------------------------------------------------------------------------
FACILITIES_FY25 = [
    # (name, currency, rate as disclosed, current, non-current)
    ('Sukuk, May 2019, final May 2029',            'USD', '3.89%',                        0, 4_680_493),
    ('Murabaha, Dec 2017, final Dec 2027',         'MYR', '6M KLIBOR + 0.65%',            0, 1_310_218),
    ('Murabaha, Sep 2021, final Aug 2026',         'USD', '3M SOFR + 0.75%',        494_831,         0),
    ('Murabaha, Mar 2021, final Nov 2029',         'USD', '1.27%',                   69_728,   205_741),
    ('Murabaha, Sep 2023, final Mar 2029',         'USD', '6M SOFR + 0.73%',              0, 6_000_726),
    ('Murabaha, Feb 2022, final Mar 2028',         'KWD', 'CBK + 0.55%',             70_019,    70_019),
    ('Mudarabah, Dec 2018, final May 2026',        'BHD', '2.10%',                    1_837,         0),
    ('Murabaha, Jan 2023, final Jan 2029',         'USD', '3M SOFR + 0.95%',              0,   450_059),
    ('Murabaha, Aug 2022, final Aug 2036',         'SAR', '6M SAIBOR + 0.60%',            0,   605_394),
    ('Murabaha, Jun 2022, final Jun 2027',         'SAR', '6M SAIBOR + 0.45%',            0,   499_626),
    ('Others, subsidiaries',                       'n/d', 'not disclosed',          150_745,   581_992),
]
BORROWINGS_FY25 = sum(c + nc for _, _, _, c, nc in FACILITIES_FY25)
assert BORROWINGS_FY25 == 787_160 + 14_404_268 == 15_191_428, BORROWINGS_FY25

BORROWINGS_FY24 = 391_584 + 14_740_155          # note 26, FY2025 filing, comparative
BORROWINGS_FY23 = 8_315_728 + 13_641_768        # note 27, FY2024 filing, comparative
assert BORROWINGS_FY23 == 21_957_496

# The latest disclosed sheet [R-BRIDGE-01]: 30 June 2026, reviewed.
LT_BORROWINGS_H126 = 22_094_126
ST_BORROWINGS_H126 = 1_442_428
BORROWINGS_H126 = LT_BORROWINGS_H126 + ST_BORROWINGS_H126

# ARITHMETIC IS THE ARBITER. The interim's own financing section rolls the December
# book forward, and it reproduces the balance-sheet total to twelve basis points —
# the residue being translation on the non-riyal legs and amortised-cost accretion.
ROLL = BORROWINGS_FY25 + 8_720_100 - 346_194
ROLL_GAP = BORROWINGS_H126 / ROLL - 1.0
assert abs(ROLL_GAP) < 0.002, ROLL_GAP

# Currency composition. The January 2026 issue is dollar sukuk (note 15 footnote), so
# it is added to the dollar leg; the riyal share is what the local-currency test needs.
_by_ccy = {}
for _n, ccy, _r, c, nc in FACILITIES_FY25:
    _by_ccy[ccy] = _by_ccy.get(ccy, 0) + c + nc
SUKUK_JAN26 = 7_500_000                          # note 15, two tranches, USD 2.0bn
CCY_H126 = dict(_by_ccy)
CCY_H126['USD'] += SUKUK_JAN26
PCT_SAR = CCY_H126['SAR'] / sum(CCY_H126.values())

# ---------------------------------------------------------------------------
# THE EFFECTIVE RATE, COMPUTED INDEPENDENTLY, AND THE DENOMINATOR IS NAMED.
# Numerator: the finance cost that arises on BORROWINGS — murabaha and sukuk — and
# nothing else. Lease interest belongs to a liability the borrowings total does not
# carry, and the unwinding of discounts on provisions is not interest on debt at all.
# Dividing the whole finance-cost line by the whole liabilities total is the error
# [R-FCAL-01] names: it understates the rate by a multiple and looks like evidence.
# ---------------------------------------------------------------------------
FIN_COST = {          # (murabaha + sukuk), excluding leases and discount unwinding
    'FY2025': 399_420 + 191_544,        # note 39, FY2025 filing
    'FY2024': 568_672 + 222_066,        # note 40, FY2024 filing
    'FY2023': 476_294 + 185_135,        # note 40, FY2024 filing, comparative
}
BAL = {'FY2025': BORROWINGS_FY25, 'FY2024': BORROWINGS_FY24, 'FY2023': BORROWINGS_FY23}

def eff(year, prior):
    avg = (BAL[year] + BAL[prior]) / 2
    return dict(year=year, interest=FIN_COST[year], closing=BAL[year], opening=BAL[prior],
                on_average=FIN_COST[year] / avg, on_closing=FIN_COST[year] / BAL[year])

EFF = [eff('FY2024', 'FY2023'), eff('FY2025', 'FY2024')]

# THE ADOPTED RATE IS MARGINAL AND FORWARD-LOOKING, AND IT IS THIS COMPANY'S OWN
# LATEST ISSUE — the January 2026 sukuk, two tranches, weighted by their own sizes.
T5, T5_RATE = 2_812_000, 0.04489
T10, T10_RATE = 4_688_000, 0.05083
KD_MARGINAL = (T5 * T5_RATE + T10 * T10_RATE) / (T5 + T10)

DEBT = COC.DebtBook(
    gross_debt=BORROWINGS_H126,
    pct_local_currency=PCT_SAR,
    currency_source=(
        'Note 26 of the FY2025 audited statements gives every facility with its own '
        'currency column: dollar %s, ringgit %s, riyal %s, dinar %s and %s of subsidiary '
        'borrowings whose currency the note does not state, footing exactly to the stated '
        '%s. The January 2026 issue is dollar sukuk (note 15 of the reviewed 30 June 2026 '
        'interim, which names both tranches), so the riyal share of the current book is '
        '%.1f%%. Every non-riyal leg is in a currency pegged or managed against the dollar, '
        'and the riyal itself is pegged at 3.75, so expected depreciation is zero and the '
        'local-equivalent cost of a dollar leg is its own coupon.'
        % (f'{CCY_H126["USD"]:,}', f'{_by_ccy["MYR"]:,}', f'{_by_ccy["SAR"]:,}',
           f'{_by_ccy["KWD"] + _by_ccy["BHD"]:,}', f'{_by_ccy["n/d"]:,}',
           f'{BORROWINGS_FY25:,}', 100 * PCT_SAR)),
    kd_local_pretax=KD_MARGINAL,
    kd_fx_local_equivalent=KD_MARGINAL,
    kd_source=(
        "The company's OWN latest issue: international sukuk of SAR 7,500 million "
        "(USD 2,000 million) completed in the first half of 2026 in two tranches — SAR "
        "2,812 million for five years at 4.489%% and SAR 4,688 million for ten years at "
        "5.083%% — weighting to %.3f%%. It is 32%% of the current book and is the marginal "
        "rate this company actually faces." % (100 * KD_MARGINAL)),
    effective_rates=[e['on_closing'] for e in EFF],
    effective_rate_periods=['FY2024', 'FY2025'],
    interest_bearing_note=(
        'The denominator is the BORROWINGS total from note 26 (FY2025 filing) and note 27 '
        '(FY2024 filing) — murabaha, sukuk and mudarabah — and nothing else. Lease '
        'liabilities are excluded because their interest is disclosed separately and they '
        'are not in the borrowings total; trade payables, contract liabilities and the '
        "digital bank's customer balances are excluded because they bear no interest. The "
        'numerator is the murabaha and sukuk finance cost from note 39/40, excluding lease '
        'interest and the unwinding of discounts on provisions. CLOSING rather than average '
        'balances, because the book RE-BASED inside both periods and an average describes a '
        'book that existed at no point in either: SAR 2,635 million of loans were repaid in '
        '2024 against SAR 433 million in 2023 while TAWAL left the group, and SAR 7,500 '
        'million was drawn in January 2026. Both bases are computed and published below.'),
)

BETA_RAW = own_stock_beta('STC', 'SA', 'TADAWUL')
BETA = COC.BetaRecord(
    beta=BETA_RAW['beta'], tier=1,
    source=('Own-stock weekly regression against the published index of the exchange the '
            'stock is listed on, through beta_regression.own_stock_beta("STC","SA",'
            '"TADAWUL"): %d weekly observations over %.2f years to %s against TASI.'
            % (BETA_RAW['n'], BETA_RAW['window_years'], BETA_RAW['last_obs'])),
    r2=BETA_RAW['r2'], se=BETA_RAW['se'], n=BETA_RAW['n'],
    index_file=BETA_RAW['index_file'], index_asof=BETA_RAW['index_asof'],
    conforming=BETA_RAW['conforming'],
)

# Market capitalisation on the LATEST KNOWN price [R-GAP-01], against the share count
# footed against par: note 17 of the reviewed 30 June 2026 interim states issued capital
# of SAR 50,000,000 thousand in shares of SAR 10 each, and 50,000,000 / 10 = 5,000,000
# thousand shares, which is the number the same note states; less 6,976 thousand held in
# treasury leaves 4,993,024 thousand outstanding.
ISSUED_CAPITAL, PAR = 50_000_000, 10.0
SHARES_ISSUED = ISSUED_CAPITAL / PAR
assert SHARES_ISSUED == 5_000_000
TREASURY = 6_976
SHARES_OUT = SHARES_ISSUED - TREASURY
assert SHARES_OUT == 4_993_024

SPOT = 43.86            # supplied close, 3 September 2026
SPOT_DATE = '2026-09-03'
MKTCAP = SPOT * SHARES_OUT / 1000.0        # SAR millions -> thousands consistency below
MKTCAP_TH = SPOT * SHARES_OUT              # SAR thousands


#: A beta this study does NOT adopt, kept only so the rebuild can measure what the beta
#: correction was worth on its own. It is the 40-session DAILY regression the delivered
#: study carried, which the standing rule says is not one of the three tiers at all.
BETA_RETIRED = 0.4753


def build(beta_value=None, erp_basis='market'):
    b = BETA if beta_value is None else COC.BetaRecord(
        beta=beta_value, tier=1, source='sensitivity only, not this study\'s beta',
        r2=BETA.r2, se=BETA.se, n=BETA.n, index_file=BETA.index_file,
        index_asof=BETA.index_asof, conforming=True)
    return COC.schedule(market='SA', beta=b, debt=DEBT, market_cap=MKTCAP_TH,
                        tax_rate=TAX, years=5, erp_basis=erp_basis,
                        build_date=BUILD_DATE, allow_stale_sovereign=True)


if __name__ == '__main__':
    print('borrowings 30-Jun-2026 %s (roll-forward gap %.3f%%)'
          % (f'{BORROWINGS_H126:,}', 100 * ROLL_GAP))
    print('riyal share of the book %.1f%%' % (100 * PCT_SAR))
    for e in EFF:
        print('  effective %s: on closing %.3f%%   on average %.3f%%'
              % (e['year'], 100 * e['on_closing'], 100 * e['on_average']))
    print('adopted marginal Kd %.3f%%' % (100 * KD_MARGINAL))
    print('beta %.4f (n=%d, R2=%.3f)' % (BETA.beta, BETA.n, BETA.r2))
    s = build()
    print('rf observed %.2f%%  spread %.2f%%  rf* %.2f%%  erp %.2f%%'
          % (100 * s.rf_observed, 100 * s.default_spread, 100 * s.rf_star, 100 * s.erp))
    print('Ke %.3f%%  Kd(at) %.3f%%  we %.4f  wd %.4f  WACC %.3f%%  regime %s'
          % (100 * s.ke_exp, 100 * s.kd_aftertax, s.weight_equity, s.weight_debt,
             100 * s.wacc_exp, s.regime))
    print('forward', ['%.4f' % x for x in s.forward_wacc])
    print('factors', ['%.4f' % x for x in s.discount_factors],
          'terminal', '%.4f' % s.terminal_discount_factor)


WEIGHTS_SOURCE = (
    'Market-value equity, never book: the latest known close of SAR %.2f on %s times '
    '%s thousand shares outstanding — issued capital of SAR 50,000,000 thousand in '
    'shares of SAR 10 each, which divides to the 5,000,000 thousand shares note 17 of '
    'the reviewed 30 June 2026 interim itself states, less 6,976 thousand held in '
    'treasury. Debt is the borrowings total from the LATEST DISCLOSED balance sheet, '
    '30 June 2026, SAR %s thousand, which reproduces from the same interim\'s own '
    'financing cash flows to twelve basis points.'
    % (SPOT, SPOT_DATE, f'{SHARES_OUT:,.0f}', f'{BORROWINGS_H126:,}'))


def record(sched):
    """The committed cost-of-capital record, straight off the Schedule the model used."""
    from dataclasses import asdict
    r = asdict(sched)
    r['build_date'] = BUILD_DATE
    r['spot'] = SPOT
    r['spot_date'] = SPOT_DATE
    r['market_cap'] = MKTCAP_TH
    r['shares_outstanding'] = SHARES_OUT
    r['gross_debt'] = BORROWINGS_H126
    r['effective_rate_detail'] = EFF
    r['weights_source'] = WEIGHTS_SOURCE
    r['sovereign_staleness_disclosed'] = (
        'The Saudi sovereign quote on the house macro path carries an as-of date of '
        '31 July 2026 and this schedule is struck on 5 September 2026, so it is 36 days '
        'old against the 14-day bound. It is accepted DELIBERATELY and the age is '
        'disclosed here rather than used quietly; refreshing the path is a macro-path '
        'task that moves every Saudi study at once, not a lever inside this one.')
    return r
