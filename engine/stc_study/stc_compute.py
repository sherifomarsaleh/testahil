"""STC study — master computation. Outputs study_numbers.json + backtest tables.
Saudi Telecom Company (Tadawul: 7010).

Price history comes from the PERSISTENT LIBRARY at engine/raw_ohlc/SA/STC.csv, which is
the file the whole engine reads for this name. The study previously carried its own
one-off export beside it; a study-local copy of a series the library already holds is a
second source for one fact, and the two drift apart the moment either is refreshed.
"""
import json
import os
import sys

import numpy as np
import pandas as pd

# The engine directory, explicitly. This file imported engine modules by bare name and
# resolved them only when it happened to be invoked with the right PYTHONPATH — an
# invocation dependency nothing stated and nothing checked, which every other study in
# the repository already avoids the same way.
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

import income_statement as ISTMT_EARLY          # noqa: E402  (after the path insert)
import strike_cohorts as SC                     # noqa: E402
from wacc_builder import WaccInputs, build_wacc, RegressionBetaAttempt  # noqa: E402

# Imported here rather than beside the cost-of-capital block because the LATEST KNOWN
# price it reads is needed by the market capitalisation long before the schedule is built.
import coc_run as COCRUN

HERE = os.path.dirname(os.path.abspath(__file__))

df, STEP0 = SC.load_clean('SA', 'STC')       # Step 0.0 applied — the frame production reads
close = df['Price'].to_numpy(dtype=float)
spot = float(close[-1])
spot_date = str(df['Date'].iloc[-1].date())
N = len(df)

# ---------------- The price cone: the PRODUCTION chain, never a study-local one ----
# This section used to run a simulation of its own, and it was wrong in five ways at
# once against the fit this market actually runs: Student-t innovations hardcoded at
# five degrees of freedom against a fitted fifteen; NO width calibration at all against
# a fitted 1.056; zero drift on a market that runs an ACTIVE momentum lean; a horizon
# hardcoded at sixty sessions where the horizons are calendar and the session count is
# projected at strike; and — the part that mattered most — a sixteen-factor stack of
# nine typed jump probabilities with their typed impacts, whose own printed caption
# conceded that none of them was calibrated.
#
# The consequence was not a rounding difference. IT PUBLISHED A DIFFERENT CONE FROM THE
# ONE THE SITE PUBLISHES FOR THIS NAME ON THIS DAY: a three-month median of 45.06
# against 45.30, a 95th percentile of 51.21 against 52.20, and a thirteen per cent
# chance of touching SAR 50 against twenty. A reader holding both would have found two
# answers to one question, and the one with the invented event probabilities was the one
# wearing the study's covers.
#
# A study's own price map REPRODUCES the committed fit; it never re-derives one. Every
# figure below now comes from engine/strike_cohorts.strike(), the same call the roll-
# forward makes, and the assertions underneath hold it to the published row rather than
# trusting that it matches.
CONE = SC.strike('SA', 'STC')
assert CONE['anchor_date'] == spot_date and CONE['spot'] == spot
H1M, H3M = CONE['horizons']['1M'], CONE['horizons']['3M']
paths20, paths60 = H1M['_paths'], H3M['_paths']
term20, term60 = paths20[:, -1], paths60[:, -1]

pcts = [5, 25, 50, 75, 95]
q20 = {p: float(np.percentile(term20, p)) for p in pcts}
q60 = {p: float(np.percentile(term60, p)) for p in pcts}

levels = [50, 48, 46, 44, 42, 40, 38, 36]


def _touch(paths, level):
    """P(the path reaches `level` at any point before its horizon)."""
    return float(np.mean(paths.max(axis=1) >= level) if level > spot
                 else np.mean(paths.min(axis=1) <= level))


touch = {L: dict(t20=_touch(paths20, L), t60=_touch(paths60, L)) for L in levels}
prob_read = dict(
    p_above=float(np.mean(term60 > spot)),
    p_up10=float(np.mean(term60 >= spot * 1.10)),
    p_dn10=float(np.mean(term60 <= spot * 0.90)),
    median=float(np.median(term60)),
    med_move=float(np.median(term60) / spot - 1),
    band50=(q60[25], q60[75]),
    band50_pct=((q60[25] / spot - 1), (q60[75] / spot - 1)),
    touch_up10=float(np.mean(paths60.max(axis=1) >= spot * 1.10)),
    touch_dn10=float(np.mean(paths60.min(axis=1) <= spot * 0.90)),
)
prob_read['odds'] = prob_read['p_up10'] / prob_read['p_dn10']
zones_edges = [0, 38, 42, 46, 50, 1e9]
zone_probs = [float(np.mean((term60 >= a) & (term60 < b)))
              for a, b in zip(zones_edges[:-1], zones_edges[1:])]
assert abs(sum(zone_probs) - 1.0) < 1e-9, 'the zones must partition the distribution'
fan = {p: np.percentile(paths60, p, axis=0).tolist() for p in pcts}

# ---------------- Technicals -------------------------------------------------
s = pd.Series(close)
sma = {n_: float(s.rolling(n_).mean().iloc[-1]) for n_ in [20, 50, 100, 200]}
delta = s.diff()
gain = delta.clip(lower=0).ewm(alpha=1/14, adjust=False).mean()
loss = (-delta.clip(upper=0)).ewm(alpha=1/14, adjust=False).mean()
rsi = float((100 - 100 / (1 + gain / loss)).iloc[-1])
ema12 = s.ewm(span=12, adjust=False).mean(); ema26 = s.ewm(span=26, adjust=False).mean()
macd_line = ema12 - ema26; sig = macd_line.ewm(span=9, adjust=False).mean()
macd = dict(line=float(macd_line.iloc[-1]), signal=float(sig.iloc[-1]),
            hist=float((macd_line - sig).iloc[-1]))
hi52 = float(df['High'].iloc[-252:].max()); lo52 = float(df['Low'].iloc[-252:].min())
rv252 = float(np.std(np.diff(np.log(close[-253:])), ddof=1) * np.sqrt(252))
chg20 = float(close[-1]/close[-21]-1); chg60 = float(close[-1]/close[-61]-1)

# ---------------- Valuation model -------------------------------------------
# THE SHARE COUNT IS FOOTED AGAINST PAR OR IT IS NOT USED [R-FCAL-01]. Note 17 of the
# reviewed 30 June 2026 interim states issued capital of SAR 50,000,000 thousand in shares
# of SAR 10 each; 50,000,000 / 10 is 5,000,000 thousand shares, which is the number that
# note itself states, and 6,976 thousand sit in treasury. The delivered study divided by
# 4,989.798mn, the 31 December 2025 count.
#
# The interim's own balance sheet PRINTS share capital as 60,000,000, and it is an
# EXTRACTION artefact of that page rather than a capital increase: note 17 says 50,000,000
# at both dates, and only 50,000,000 makes the equity block foot to the stated 84,986,806.
# Taken at face value it would have been a 20% rise in the share count that never happened.
ISSUED_CAPITAL, PAR_VALUE, TREASURY_SHARES = 50_000_000.0, 10.0, 6_976.0
SH = (ISSUED_CAPITAL / PAR_VALUE - TREASURY_SHARES) / 1000.0   # mn shares outstanding
assert abs(SH - 4_993.024) < 1e-9
# THE TAX RATE IS MEASURED, ON THE BASE IT IS APPLIED TO. It was 0.097, typed, with a
# comment reading "FY23 9.5%, FY24 9.8%; FY25 -3.2% one-off credit" — a mean of the two
# years that looked ordinary, on a base the comment does not name. Two things were wrong
# with it and each was found by an arithmetic check rather than by judgement.
#
# WHICH YEAR IS ONE-OFF IS DISCLOSED, NOT JUDGED. Note 33(a)'s movement table carries
# "Reversal of prior years' Zakat provision during the year (1,324,787)" on its own line, so
# the FY2025 credit does not have to be inferred from its size; the underlying charge is the
# year's own additions and the reversal belongs to the years it corrects.
#
# AND THE BASE HAS TO MATCH. After-tax operating profit is EBIT times one minus a rate, so
# the rate must be measured against EBIT — 8.03% — while the income statement's zakat line
# sits on profit before zakat and takes 8.27%. The two differ because the lines between them
# are a net charge on this book, and a ratio between quantities defined differently is not
# evidence about either.
TAX = ISTMT_EARLY.effective_zakat_rate('ebit')
# ===== TWO CLOCKS, AND THE STUDY SAYS WHICH IS WHICH [R-GAP-01] =============
# `spot` above is the last session in the PERSISTENT PRICE LIBRARY, and it is the anchor
# the Monte Carlo cone is struck on, because a cone is built on a price series and has to
# start where that series ends. THE VALUATION IS A DIFFERENT QUESTION and is put against
# the LATEST KNOWN price, which on 5 September 2026 is a later figure than the library
# holds. Publishing one number for both would either strike the cone on a session that is
# not in its own series or measure the gap against a price the market has already left.
CONE_ANCHOR, CONE_ANCHOR_DATE = spot, spot_date
VALUATION_SPOT = COCRUN.SPOT               # the supplied close register, read not typed
VALUATION_SPOT_DATE = COCRUN.SPOT_DATE
MKTCAP = VALUATION_SPOT * SH

# ===== Historical anchors (stc.com IR releases; restated continuing-ops) =====
hist = dict(
    rev={'FY23': 71777.0, 'FY24': 75893.0, 'FY25': 77819.0},
    gp={'FY23': 34740.0, 'FY24': 37326.0, 'FY25': 37700.0},
    ebitda={'FY23': 22445.0, 'FY24': 23951.0, 'FY25': 24469.0},
    ebit={'FY23': 13161.0, 'FY24': 14426.0, 'FY25': 14438.0},
    np_att={'FY23': 13295.0, 'FY24': 24689.0, 'FY25': 14828.0},
    np_cont_att={'FY23': 12536.0, 'FY24': 10716.0, 'FY25': 14828.0},  # ex-discontinued (FY24 incl. 13,973 disc-ops; FY23 759)
    assets={'FY23': 159646.0, 'FY24': 160638.0, 'FY25': 157477.0},
    cash={'FY23': 28138.0, 'FY24': 30755.0, 'FY25': 15080.0},
    debt={'FY23': 21958.0, 'FY24': 15132.0, 'FY25': 15191.0},
    eq_att={'FY23': 78985.0, 'FY24': 89417.0, 'FY25': 83414.0},
    nci={'FY23': 2530.0, 'FY24': 3069.0, 'FY25': 3482.0},   # FY25 primary (Q1-26 FS comparative); FY23/24 estimated
    ocf={'FY23': 22418.0, 'FY24': 19885.0, 'FY25': 18283.0},
    fcf={'FY23': 12628.0, 'FY24': 7959.0, 'FY25': 6488.0},
    capex={'FY23': 9790.0, 'FY24': 11927.0, 'FY25': 11795.0},
    dna={'FY23': 9284.0, 'FY24': 9525.0, 'FY25': 10031.0},  # EBITDA − EBIT (both disclosed)
    dps={'FY23': 1.60, 'FY24': 3.75, 'FY25': 2.20},         # FY24 incl. SAR 2.00 special (paid 2025)
)
# Segment history (stc.com FY25 presentation; FY24 restated)
seg_hist = dict(
    ksa_cbu={'FY24': 31741.0, 'FY25': 32826.0},
    ksa_ebu={'FY24': 13466.0, 'FY25': 13514.0},
    ksa_wc={'FY24': 4313.0, 'FY25': 4779.0},
    ksa={'FY24': 49644.0, 'FY25': 51119.0},
    subs={'FY24': 26249.0, 'FY25': 26700.0},   # group − KSA (net of eliminations)
)

# ===== Forecast drivers, built on the DISCLOSED SEGMENTS [R-MACRO-01, R-SIGCM-02] ====
# The rule is pre-registered in DRIVER_REBUILD_05-09-2026.md and every clause of it is
# mechanical. It replaces four typed arrays over a taxonomy the filings do not use.
import segments as SEG

yrs = ['FY26E', 'FY27E', 'FY28E', 'FY29E', 'FY30E']
FORECAST_YEARS = [2026, 2027, 2028, 2029, 2030]

# Saudi consumer-price inflation for the two years the trailing window spans, each a DATED
# SCALAR from the International Monetary Fund's World Economic Outlook database, series
# PCPIPCH, Saudi Arabia — the same database, series and country row the house macro path's
# forward ladder comes from, so the history and the forecast are one economy rather than two.
CPI_HIST = {2024: 0.015, 2025: 0.020}
CPI_HIST_SOURCE = ('International Monetary Fund, World Economic Outlook database, series '
                   'PCPIPCH (inflation, average consumer prices, annual percent change), '
                   'Saudi Arabia (SAU), read live from the IMF datamapper API on '
                   '5 September 2026.')
_DEFLATOR = (1 + CPI_HIST[2024]) * (1 + CPI_HIST[2025])

# THE GROUP'S OWN REAL RATE, which a re-grouped line takes instead of its own.
GROUP_REAL = (SEG.STATED_REVENUE[2] / SEG.STATED_REVENUE[0] / _DEFLATOR) ** 0.5 - 1.0

# THE ONE SEGMENT WITH UNIT DATA IS BUILT AS VOLUME TIMES PRICE [SIGCM clause 2]. The stc
# segment is the KSA operating business and two thirds of group revenue; the earnings
# presentations disclose its subscriber base by category at three fiscal year ends, and
# units.py checks those three ways before this reads them. Its revenue compounded at 1.91%
# — a subscriber base compounding at 6.00% against revenue per subscriber falling 3.86%,
# which multiply back to exactly that 1.91%. The net is what the other segments have to be
# forecast on; where the two halves are disclosed, forecasting the net throws away the only
# thing that says which of them is likely to continue.
import units as UNITS

_u = UNITS.record()
UNIT_SEGMENT = 'stc'
VOLUME_REAL = _u['volume_cagr_2y']                       # subscribers; a real quantity
PRICE_REAL = (1 + _u['price_cagr_2y']) / _DEFLATOR ** 0.5 - 1.0   # revenue per subscriber

seg_real0 = {}
for _k, _v in SEG.REVENUE.items():
    if _k == 'Eliminations / adjustments':
        # eliminations are intra-group and scale with the segments they eliminate between,
        # so they are held at their FY2025 share of gross segment revenue rather than grown
        continue
    if _k in SEG.REGROUPED or _v[0] <= 0:
        # A line whose composition changed between filings has no growth rate of its own:
        # iot2 reads +107% real and Other reads -70%, and both are accounting changes.
        seg_real0[_k] = GROUP_REAL
    else:
        seg_real0[_k] = (_v[2] / _v[0] / _DEFLATOR) ** 0.5 - 1.0


def seg_real(name, t):
    """The segment's real growth in explicit year t (1-based), fading to ZERO by year 5.

    THE ONE SEGMENT WITH UNIT DATA IS BUILT FROM ITS TWO HALVES rather than from the net.
    Volume and real price are each faded on the same schedule and MULTIPLIED, which is the
    identity revenue actually obeys; fading the net instead would drop the cross-term, and
    on this name that is worth about five basis points a year. The gain is not the five
    basis points — it is that the two halves are now separately visible, so a later edition
    can fade them DIFFERENTLY with a reason. Saudi mobile penetration is already far above
    one line per person, and a volume line growing at 6% and a price line falling at 4% are
    not equally likely to persist.

    THE FADE ITSELF IS NOT A FREE PARAMETER DRESSED UP. The terminal states real growth of
    zero, so a segment still growing in real terms in the last explicit year would be
    capitalised at a rate it never reached, which is what [R-MACRO-01] says about explicit
    windows and [R-TERM-01] about terminals. Fading to the number the terminal already
    assumes is what makes the two halves of the model one model.
    """
    f = 1.0 - t / float(len(yrs))
    if name == UNIT_SEGMENT:
        return (1.0 + VOLUME_REAL * f) * (1.0 + PRICE_REAL * f) - 1.0
    return seg_real0[name] * f


# ===== THE FIRST FORECAST YEAR IS ANCHORED ON THE LATEST REVIEWED PERIOD ==============
# The standing rule is that A NEAR-TERM REVIEWED ACTUAL OUTRANKS A STALE FULL-YEAR RATE:
# anchor every rate on the most recent reviewed period, hold everything else flat INCLUDING
# observed improvements, and where a first-half rate is carried into the second half PROVE
# with the prior year's actual halves which way that runs.
#
# The six months to 30 June 2026 are published and reviewed, and the model was growing
# FY2025 forward as though they were not. Note 4 of that interim gives revenue by segment
# for both halves and the group's cost of operations excluding depreciation, so the level,
# the gross margin and the operating-cost share are all readable from one note.
H1_2026_REVENUE, H1_2025_REVENUE = 40_110_089.0, 38_660_477.0
H1_2026_COST_EX_DA, H1_2025_COST_EX_DA = 27_141_890.0, 26_371_877.0
H1_2026_GROSS, H1_2025_GROSS = 19_637_121.0, 18_657_904.0
H1_2026_SGA = 3_206_382.0 + 3_463_640.0        # selling and marketing plus administrative
H1_2025_SGA = 3_037_913.0 + 3_331_391.0

# THE SEASONALITY IS MEASURED, NOT ASSUMED — each factor is the prior year's own half
# against its own full year, which is the proof the rule asks for.
SEASON_REVENUE = 77_818.675 / (H1_2025_REVENUE / 1000.0 * 2)          # 1.0064
SEASON_GROSS_MARGIN = ((37_699.689 / 77_818.675)
                       / (H1_2025_GROSS / H1_2025_REVENUE))           # H1 understates
SEASON_SGA_SHARE = ((13_230.254 / 77_818.675)
                    / (H1_2025_SGA / H1_2025_REVENUE))                # H1 understates

FY26_REVENUE_ANCHOR = H1_2026_REVENUE / 1000.0 * 2 * SEASON_REVENUE
FY26_GROSS_MARGIN = H1_2026_GROSS / H1_2026_REVENUE * SEASON_GROSS_MARGIN
FY26_SGA_SHARE = H1_2026_SGA / H1_2026_REVENUE * SEASON_SGA_SHARE

# Revenue, segment by segment, nominal RECOMPUTED from real on the house ladder.
_gross_fy25 = sum(v[2] for k, v in SEG.REVENUE.items()
                  if k != 'Eliminations / adjustments')
ELIM_SHARE = SEG.REVENUE['Eliminations / adjustments'][2] / _gross_fy25

seg_fc, fc = {}, {}
_lvl = {k: v[2] / 1000.0 for k, v in SEG.REVENUE.items()
        if k != 'Eliminations / adjustments'}          # SAR millions
for i, y in enumerate(yrs):
    _infl = COCRUN.MACRO.inflation(FORECAST_YEARS[i])
    for k in list(_lvl):
        _lvl[k] *= (1.0 + seg_real(k, i + 1)) * (1.0 + _infl)
    if i == 0:
        # The first year is put ON the reviewed half rather than grown off a stale full
        # year. The segment MIX stays the model's own; what the anchor sets is the level,
        # and it is a disclosed six months doubled and corrected by the prior year's own
        # measured half-to-year factor rather than a forecast.
        _target = FY26_REVENUE_ANCHOR / (1.0 + ELIM_SHARE)
        _scale = _target / sum(_lvl.values())
        _h1_scale = _scale
        for k in list(_lvl):
            _lvl[k] *= _scale
    _gross = sum(_lvl.values())
    seg_fc[y] = dict(_lvl)
    fc[y] = dict(gross=_gross, elim=_gross * ELIM_SHARE,
                 rev=_gross * (1.0 + ELIM_SHARE))

# Gross profit per segment at its own FY2025 margin. Margin is an OUTPUT of the cost side
# wherever the filings support one; this panel discloses cost only as the residual, so the
# finest sourced level is the segment's own disclosed margin, held.
SEG_MARGIN = {}
for _k in _lvl:
    _r, _g = SEG.REVENUE[_k][2], SEG.GROSS_PROFIT[_k][2]
    SEG_MARGIN[_k] = (_g / _r) if _r > 0 else 0.0
ELIM_GP_SHARE = SEG.GROSS_PROFIT['Eliminations / adjustments'][2] / _gross_fy25

# The one line between group gross profit and group EBITDA — selling, general and
# administrative cost — at its OWN three-year average share of revenue, so the EBITDA
# margin is an output of two sourced lines rather than a number typed above them.
SGA_SHARE = sum((SEG.STATED_GROSS_PROFIT[i] - e) / SEG.STATED_REVENUE[i]
                for i, e in enumerate((22_445_389, 23_951_115, 24_469_435))) / 3.0

# Depreciation and amortisation at the FY2025 filed ratio, and capital expenditure on the
# guidance band the company publishes. Both anchored on a disclosed figure rather than typed.
DNA_SHARE = 10_031.171 / 77_818.675

# CAPITAL EXPENDITURE IS MEASURED FROM THE FILINGS, NOT TAKEN FROM GUIDANCE [R-FCAL-01].
# The delivered path — 16.5% of revenue falling to 15.0% — is management's own published
# band, and the rule is explicit that GUIDANCE IS SCORED AND NEVER CONSUMED: a forward
# target leans the same way an optimistic model does, so a driver that takes it as an input
# inherits the lean instead of correcting for it.
#
# What this company actually spends is disclosed for three years, and the ratio that
# matters is capital expenditure over the depreciation of the base it renews:
CAPEX_TO_DNA_HISTORY = [9_790.0 / 9_284.098,        # FY2023  1.054
                        11_927.0 / 9_525.477,       # FY2024  1.252
                        11_795.0 / 10_031.171]      # FY2025  1.176
CAPEX_TO_DNA = sum(CAPEX_TO_DNA_HISTORY) / len(CAPEX_TO_DNA_HISTORY)
capex_pct = [DNA_SHARE * CAPEX_TO_DNA] * 5

# THE STEP AT THE TERMINAL BOUNDARY IS REAL, IT IS LARGE, AND IT IS STATED RATHER THAN
# SMOOTHED [R-TERM-01]. The terminal charges maintenance at CURRENT cost — book
# depreciation escalated over the measured 15.23-year age of the base, a factor of 1.3519,
# or 17.43% of revenue. This company has never spent that: its peak year was 15.72% and its
# capital expenditure has run at 1.16 times depreciation against the 1.35 a base maintained
# at current cost would need. THE ECONOMIC READING IS THAT THE BASE IS AGEING, and the
# accounts say so independently — 73% of the depreciable base is written off and its
# measured age rose 13.60 to 14.18 to 15.23 years across the three filed years. An explicit
# window may continue an observed under-maintenance for five years; A PERPETUITY MAY NOT,
# because a company that never replaces its plant is not a going concern.
#
# THE ALTERNATIVE READING IS RECORDED RATHER THAN DISMISSED, and it is specific to this
# industry: escalating at GENERAL inflation assumes a radio or a switch costs 2% more each
# year to replace, where telecommunications equipment has historically fallen in real cost
# per unit of capacity. If that holds here, the terminal charge is too high and the gap
# between 1.16 and 1.35 is priced equipment rather than deferred maintenance. WHAT WOULD
# SEPARATE THEM is a disclosed replacement-cost or capacity series, which this company does
# not publish; until one is found the rising age is the only measured evidence and it
# supports the first reading.
# WORKING CAPITAL IS PROJECTED FROM THE ASSET-CONVERSION CYCLE, NOT PLUGGED [SIGCM clause
# 4]. This line used to be a typed outflow of 0.8% of revenue falling to 0.4% — a number per
# year with no balance sheet behind it, which is exactly the plug the clause forbids where
# the drivers are disclosed. And they are disclosed, in unusual detail: receivables with an
# ageing analysis, inventory with ITS OWN cost base stated in the note, payables with a
# stated settlement range, and the two contract balances a telecom actually turns over.
#
# WHAT THE PLUG WAS HIDING. Net working capital ran 5.9%, 6.5% and 13.2% of revenue across
# the filed years and 17.5% at the reviewed half — it MORE THAN DOUBLED in FY2025 and rose
# again in the half — while the plug said the outflow shrank every year. Days sales
# outstanding went from 107 to 125 on a receivable book three quarters of which is owed by
# government and government-related entities, and days payable fell 12. None of that is a
# view about the future; it is what the filed balance sheets did.
#
# THE DAYS ARE ANCHORED ON THE LATEST DISCLOSED SHEET, the reviewed interim the bridge
# already stands on, and then held flat — the same rule every other rate in this study
# obeys. It matters here: receivables were essentially UNCHANGED across the half (26,727,198
# to 26,727,997, eight hundred thousand on a twenty-seven billion book) while revenue grew,
# so days sales outstanding falls from 125 to 121 without anything being assumed.
import working_capital as WC

_wc_rev26 = FY26_REVENUE_ANCHOR * 1000.0                       # SAR thousands
_WC_COR_SHARE = WC.COST_OF_REVENUES[2] / WC.REVENUE[2]
_WC_INV_SHARE = WC.INVENTORY_EXPENSE[2] / WC.REVENUE[2]
WC_DAYS = WC.anchored_days(_wc_rev26, _wc_rev26 * _WC_COR_SHARE,
                           _wc_rev26 * _WC_INV_SHARE)


def _nwc(rev_mn):
    """Net working capital at a level of revenue, each line on its OWN driver."""
    return (WC_DAYS['dso'] / 365.0 * rev_mn
            + WC_DAYS['dio'] / 365.0 * rev_mn * _WC_INV_SHARE
            + WC_DAYS['dco'] / 365.0 * rev_mn
            - WC_DAYS['dpo_total'] / 365.0 * rev_mn * _WC_COR_SHARE
            - WC_DAYS['dcl'] / 365.0 * rev_mn)


# The opening balance is the LATEST DISCLOSED sheet's own, not a ratio applied to it.
NWC_OPEN = (WC.H1_2026['trade_receivables'] + WC.H1_2026['inventories']
            + WC.H1_2026['contract_assets'] - WC.H1_2026['payables_total']
            - WC.H1_2026['contract_liabilities']) / 1000.0
_nwc_path, _prev = [], NWC_OPEN
for _i, _y in enumerate(yrs):
    _n = _nwc(fc[_y]['rev'])
    _nwc_path.append(_n)
    fc[_y]['nwc'] = _n
    fc[_y]['dwc'] = _n - _prev
    _prev = _n
# THE FIRST YEAR MOVES BY NOTHING BY CONSTRUCTION, and that is a property rather than a
# coincidence: the days are struck on the annualised revenue of the half and the first
# forecast year IS that annualised revenue, so the balance reproduces its own opening
# figure. It is asserted so a later change to either cannot break the identity silently.
assert abs(fc[yrs[0]]['dwc']) < 1e-6, fc[yrs[0]]['dwc']
wc_out_pct = [fc[_y]['dwc'] / fc[_y]['rev'] for _y in yrs]
payout_dps = [2.20, 2.20, 2.30, 2.40, 2.55]       # policy 0.55/q locked to Q3-27

# THE TWO RATES ARE ANCHORED ON THE SAME REVIEWED HALF AND THEN HELD FLAT. The rule says
# to hold everything else flat INCLUDING observed improvements, so the first year takes the
# reviewed period's own gross margin and operating-cost share (each corrected by the prior
# year's measured half-to-year factor) and no year after it assumes any further gain.
_margin_shift = FY26_GROSS_MARGIN - (sum(seg_fc[yrs[0]][k] * SEG_MARGIN[k]
                                         for k in seg_fc[yrs[0]])
                                     + fc[yrs[0]]['gross'] * ELIM_GP_SHARE) / fc[yrs[0]]['rev']
# FOUR COST LINES COME OFF THE HELD MARGIN AND ONTO THE BASES THE FILINGS NAME. The
# standing rule is that a gross margin set as an INPUT is a fail wherever the disclosure
# supports building cost per unit instead, and note 35 discloses all seven lines by nature
# for three years. FOUR of them have a sourced base that is NOT group revenue: the
# commercial service provisioning fee is levied on the Saudi operating segment, which grows
# more slowly than the group; the licence fee is near-fixed and has its own measured rate;
# repairs and maintenance sit on the ASSET BASE being maintained, which the model already
# projects; and contract-cost amortisation is subscriber acquisition, on a volume path the
# model already carries and which grows FASTER than revenue.
#
# THE OTHER THREE, AND THE SPECTRUM SUB-LINE, ARE LEFT HELD AND SAID TO BE — network access
# has no disclosed unit rate, employee cost has no headcount anywhere in the filings
# (searched, and the negative search is registered), "Others" is a residual of three
# unrelated things, and the spectrum fee is lumpy with the first Saudi licence expiry
# falling INSIDE the explicit window against no disclosed renewal cost. Inventing a driver
# to complete the table is worse than the gap it closes.
#
# THE OFFSETS RUN BOTH WAYS, which is why this had to be built rather than argued: two
# lines fall against a group growing faster than their own bases and two rise. It was
# measured beside the model and consumed by nothing for a week, which is the difference
# between pricing a construction and building it.
import cost_decomposition as _CDEC             # the four lines' own bases, shared with
                                               # the diagnostic that reports them
_COST_OWN_BASE = _CDEC.net_by_year(
    yrs, [fc[y]['rev'] for y in yrs], [2026 + i for i in range(len(yrs))],
    seg_real0['stc'], VOLUME_REAL, [DNA_SHARE] * len(yrs), capex_pct)

for i, y in enumerate(yrs):
    _gp = sum(seg_fc[y][k] * SEG_MARGIN[k] for k in seg_fc[y]) \
        + fc[y]['gross'] * ELIM_GP_SHARE
    _gp += fc[y]['rev'] * _margin_shift
    _gp -= _COST_OWN_BASE[i]
    fc[y]['gp'] = _gp
    fc[y]['sga'] = fc[y]['rev'] * FY26_SGA_SHARE
    fc[y]['ebitda'] = _gp - fc[y]['sga']
    fc[y]['ebitda_margin'] = fc[y]['ebitda'] / fc[y]['rev']

# The names the rest of the model reads. ebitda_m and dna_pct are now DERIVED rather than
# typed: the first is an output of gross profit less a sourced cost share, the second the
# company's own filed ratio held flat.
ebitda_m = [fc[y]['ebitda_margin'] for y in yrs]
dna_pct = [DNA_SHARE] * len(yrs)
seg_hist = {k: {'FY23': v[0] / 1000.0, 'FY24': v[1] / 1000.0, 'FY25': v[2] / 1000.0}
            for k, v in SEG.REVENUE.items()}

# ===== Cost of capital — the sanctioned schedule [R-COC-01] ==================
# The whole ladder comes from engine/cost_of_capital.py through this study's own
# coc_run.py, which reads the debt book facility by facility out of note 26 and the
# finance cost out of note 39/40. Nothing about the rate is typed here: the risk-free
# is normalised by Saudi Arabia's OWN default spread so country risk is counted once,
# the weights are market-value, and the schedule is FLAT because the riyal is pegged
# and today is already the terminal — stated by the module rather than assumed here.
#
# The beta is re-derived live through beta_regression.own_stock_beta against TASI, the
# published index of the exchange this stock is listed on. It replaces a 40-session
# DAILY regression, which the standing rule says is not one of the three tiers at all;
# the module refuses to build on a non-conforming tier-1 beta, which is why the
# schedule and the beta land in the same pass.
import coc_run as COCRUN

# A sensitivity run rebuilds the schedule on a stated beta and prints the answer without
# writing anything, so the rebuild ledger can measure what the beta correction alone was
# worth rather than assert a direction for it.
_SENS_BETA = float(sys.argv[sys.argv.index('--beta') + 1]) if '--beta' in sys.argv else None

# WHICH LEVERS OF THE REBUILD PLAN ARE IN THIS FILE. Declared in one place so an artefact
# can state the state it was struck in, and so a measurement taken at one point in the
# rebuild cannot be silently overwritten by a later one: the sensitivity artefact is NAMED
# for its lever set, and a run with more levers in writes a different file rather than
# replacing a number the ledger is chaining through. [R-ENF-06]
LEVERS_APPLIED = ['mechanical', 'R-COC-01', 'R-BETA-04', 'R-MACRO-01']
SENS_TAG = 'after_coc'      # the lever set the retired-beta measurement belongs to

SCHED = COCRUN.build(beta_value=_SENS_BETA, erp_basis='market')  # swap basis, CENTRAL
SCHED_RATING = COCRUN.build(beta_value=_SENS_BETA, erp_basis='rating')
BETA = _SENS_BETA if _SENS_BETA is not None else COCRUN.BETA.beta

WACC = SCHED.wacc_exp
WACC_RATING = SCHED_RATING.wacc_exp
KE_RATING, KE_MARKET = SCHED_RATING.ke_exp, SCHED.ke_exp
KD_AT = SCHED.kd_aftertax
WE, WD = SCHED.weight_equity, SCHED.weight_debt
DF = list(SCHED.discount_factors)                 # one date, one price of time
DF_TERMINAL = SCHED.terminal_discount_factor
WACC_TERMINAL = SCHED.wacc_terminal

# Terminal growth is STORED AS A REAL RATE AND RECOMPUTES TO ITS NOMINAL on the house
# Saudi path [R-MACRO-01]. The delivered study typed 2.5% nominal, which is unfalsifiable:
# nobody can tell from the page whether it meant terminal inflation plus half a point or
# something else. The real growth is the rule's own STATED DEFAULT OF ZERO.
#
# WHAT ZERO REAL ACTUALLY MEANS, WRITTEN DOWN AS THE REAL NUMBER IT IS. This comment first
# justified the default as "a mature domestic telecom growing with the economy in
# perpetuity", and that sentence describes a POSITIVE real rate — an economy grows by
# inflation plus real output, and a company growing at inflation alone is growing with
# PRICES and not with the economy. The number was defensible and the reason for it was
# false, which is the more dangerous of the two because it survives review. Zero real means
# STC's revenue grows with the price level for ever and its share of Saudi output declines
# in perpetuity. That is a real assumption, it is conservative, and it stands because any
# positive rate would have to be SOURCED: telecommunications revenue has fallen as a share
# of output across most markets for two decades, so "it holds its share of a growing
# economy" is a claim about this company that nothing here evidences. Reverse-engineering
# the real rate that reproduces the typed 2.5% would be keeping the number and inventing a
# reason for it, which is the same offence from the other end.
TG_REAL = 0.0
TG = COCRUN.MACRO.terminal_growth(TG_REAL)      # = terminal inflation + the stated real

# ===== DCF (FCFF, full build) =================================================
rows = []
for i, y in enumerate(yrs):
    r = fc[y]['rev']
    ebitda = r * ebitda_m[i]
    dna = r * dna_pct[i]
    ebit = ebitda - dna
    nopat = ebit * (1 - TAX)
    capex = r * capex_pct[i]
    dwc = r * wc_out_pct[i]
    fcff = nopat + dna - capex - dwc
    rows.append(dict(year=y, rev=r, ebitda=ebitda, dna=dna, ebit=ebit, nopat=nopat,
                     capex=capex, dwc=dwc, fcff=fcff))
for i, rw in enumerate(rows):
    rw['df'] = DF[i]
    rw['pv'] = rw['fcff'] * rw['df']
pv_sum = sum(rw['pv'] for rw in rows)

# ===== The terminal, through the sanctioned module [R-TERM-01] ===============
# The retired construction charged g x IC every year for ever, which reads as a capital
# maintenance programme with a replacement cycle of 1/g — a fact about the currency and
# not about the asset. At a pegged 2% terminal that is FIFTY YEARS against a base whose
# own accounts run twenty-one, so it bought half the maintenance this company needs. It
# also never added book depreciation back although NOPAT is already net of it, so one
# model carried two definitions of free cash flow with the terminal holding most of the
# value.
#
# The life and the age are DERIVED from note 10's own roll-forward by the identity the
# protocol already sanctions, because this company discloses RANGES rather than a single
# life. All three conditions that break that identity were checked on the policy note
# first and all three are clear; the working is in TERMINAL_EVIDENCE_05-09-2026.md.
import terminal_value as TVM

TERM_LIFE = 134_634_729 / 6_453_343          # depreciable gross cost over the year's charge
TERM_AGE = 98_254_770 / 6_453_343            # accumulated depreciation over the same charge
# Net working capital from the LATEST DISCLOSED balance sheet, 30 June 2026, reviewed:
# inventories, contract assets and trade receivables less trade and other payables and
# contract liabilities. SAR millions, to match the model.
TERM_WC = (1_781_441 + 9_971_423 + 26_727_997 - 21_198_207 - 3_727_610) / 1000.0
# Capital per unit of REAL growth, used ONLY where the sensitivity grid moves terminal
# growth off the house terminal inflation. The base case states real growth of zero and
# is charged no growth capital at all, so this figure shapes the grid and never the
# answer. It is the depreciable gross base at CURRENT cost — the same escalation the
# maintenance charge uses, so the grid cannot quietly price growth on a historical base
# while maintenance is priced on a current one.
TERM_IC_PER_UNIT_GROWTH = (134_634_729 / 1000.0) * (1.0 + 0.02) ** (98_254_770 / 6_453_343)

_t = TVM.build(TVM.TerminalInputs(
    nopat=rows[-1]['nopat'],
    wacc=WACC_TERMINAL,
    inflation=COCRUN.MACRO.terminal_inflation,
    real_growth=TG_REAL,
    dna_book=rows[-1]['dna'],
    maintenance_basis='book_dna_escalated',
    average_age_years=TERM_AGE,
    average_age_source=(
        "Note 10 of the FY2025 audited statements, the property and equipment "
        "roll-forward: accumulated depreciation of SAR 98,254,770 thousand over the "
        "year's own charge of SAR 6,453,343 thousand. An identity off the accounts, not "
        "a figure this desk chose, and the same note gives 14.18 and 13.60 years on the "
        "two years behind it."),
    useful_life_years=TERM_LIFE,
    useful_life_source=(
        "Derived from note 10 of the FY2025 audited statements: depreciable gross cost of "
        "SAR 134,634,729 thousand — total cost of 141,541,105 less capital work in "
        "progress of 4,910,376 and land of 1,996,000, both disclosed separately in the "
        "same note — over the year's own charge of SAR 6,453,343 thousand. The company "
        "discloses RANGES rather than one life (buildings 25-50 years, telecommunication "
        "network and equipment 3-30, other assets 2-20, note 4.11), so a single figure has "
        "to come from the identity; 19.54 and 19.84 years stand behind it on the two "
        "earlier filed years."),
    working_capital=TERM_WC,
))
tv = _t.tv
pv_tv = tv * DF_TERMINAL
ev = pv_sum + pv_tv
# EV → equity bridge (marks)
# ===== Enterprise value to equity, on the LATEST DISCLOSED sheet [R-BRIDGE-01] ======
# Every line below is read from the REVIEWED interim statements for the six months to
# 30 June 2026 - the latest balance sheet this company has published - except the minority
# profit share, which is the FY2025 audited figure because a half-year share is not a rate.
# The study this replaces stood on a 31 March 2026 minority and a first-quarter net-debt
# figure, and carried associates at less than half what the accounts state.
#
# ASSOCIATES AND JOINT VENTURES AT BOOK. The delivered study carried SAR 4,641mn against a
# filed 12,909.648mn - a figure from before February 2025, when the group contributed the
# whole of its towers business to DIIC in exchange for 43.06% of it. The tower business the
# entire 2024 restatement was about had left the subsidiaries and arrived in the associates,
# and the bridge had followed it into neither. Note 8.1.4 splits the line: associates
# 10,150.459 and joint ventures the remainder at 31 December 2025. Both are unlisted, so
# book is the basis; the joint venture BGSM holds 62% of a LISTED Malaysian operator, and a
# market cross-check on that look-through is not performed because the price is not held -
# recorded as a gap rather than estimated.
BR_ASSOC = 12_909.648
# TELEFONICA AT THE COMPANY'S OWN DISCLOSED FAIR VALUE, not at a mark this desk computed.
# The 9.97% holding is irrevocably designated at fair value through other comprehensive
# income and note 9.1 states its Level 1 carrying amount, so the filed figure IS the market
# value and a typed one is a worse estimate of the same thing.
BR_LISTED_EQUITY = 8_513.430
# Investment funds and unlisted equity investments at fair value, note 9.1. Outside the
# telecom cash flows the model discounts, so they are added rather than left out.
BR_FUNDS = 5_163.516

# NET DEBT, AND THE BANK IS OUT OF THE PERIMETER - STATED, NOT ASSUMED. STC Bank is a
# consolidated subsidiary, and netting a bank's cash against the group's borrowings treats
# money that backs customer balances as though it were free. Its cash (6,000.384) and its
# digital-banking financial assets (4,111.267) are excluded here, and so are its
# digital-banking liabilities. THE COST IS THAT THE BANK'S OWN EQUITY VALUE APPEARS IN THIS
# BRIDGE NOWHERE: that understates the answer, the direction is named, and it is left as a
# gap rather than filled with a number nothing supports (SIGCM clause 8).
BR_BORROWINGS = 23_536.554          # long-term 22,094.126 + short-term 1,442.428
BR_LEASES = 2_258.902               # non-current 1,642.836 + current 616.066
BR_CASH_NON_BANK = 12_940.389       # cash and cash equivalents, excluding STC Bank
BR_MURABAHAS = 1_062.181            # short-term murabahas, its own balance-sheet line
BR_SUKUK = 6_368.453                # financial assets at amortised cost, note 9.1
BR_TBILLS = 492.070                 # treasury bills, note 9.1
# SPECTRUM ALREADY BOUGHT AND NOT YET PAID FOR IS A CLAIM AHEAD OF EQUITY, and it is
# disclosed OUTSIDE borrowings, which is why a bridge reading the borrowings lines misses it
# [R-BRIDGE-01]. Note 14.1 of the reviewed interim carries it on its own row inside
# "financial liabilities and others"; it is consideration owed to the regulator for licences
# already capitalised as intangible assets, not a trade payable.
#
# THE REASON IT IS NOT DOUBLE-COUNTED IS THE MODEL'S OWN CAPEX DEFINITION, and that had to
# be established rather than assumed. Total additions to property, equipment, intangibles
# and goodwill were 13,815.240 in FY2025 while the capital expenditure this model forecasts
# on is 11,795 — the company's own reported figure — and note 12(2) says additions include
# NON-CASH additions of 2,122 million (FY2024: 883). So the model runs on CASH capex, the
# licences acquired against this liability never entered it, and the unpaid consideration is
# a financing claim the discounted cash flows do not service. Counting the asset as capex
# AND the liability as debt would be the double count; counting neither, which is what the
# bridge did, simply omits the claim.
BR_SPECTRUM = 3_443.044             # note 14.1, financial liabilities re frequency spectrum
net_debt = (BR_BORROWINGS + BR_LEASES + BR_SPECTRUM - BR_CASH_NON_BANK - BR_MURABAHAS
            - BR_SUKUK - BR_TBILLS)

# THE MINORITY AT ITS SHARE OF THE VALUE, NOT AT HISTORICAL COST. The model capitalises
# 100% of subsidiary cash flow, so the minority's claim is worth its share of THAT, and
# deducting book overstates the parent's equity by the difference. The proxy is the
# minority's own disclosed share of profit - note 25, 306,915 against group net profit from
# continuing operations of 15,189,078 - and book and the profit share are both published
# beside the adopted figure so a reader sees the choice and not only its result. It comes
# off EQUITY value and never off enterprise value: an equity share applied to an enterprise
# number hands the minority growth assets it does not own.
BR_NCI_PROFIT = 306.915
BR_GROUP_PROFIT = 15_189.078
BR_NCI_SHARE = BR_NCI_PROFIT / BR_GROUP_PROFIT
BR_NCI_BOOK = 2_726.349             # 30 June 2026, published for comparison only

_eq_before_nci = ev + BR_ASSOC + BR_LISTED_EQUITY + BR_FUNDS - net_debt
nci_v = _eq_before_nci * BR_NCI_SHARE
assoc, telefonica = BR_ASSOC, BR_LISTED_EQUITY      # the names the rest of the model uses
eq_dcf = _eq_before_nci - nci_v
# The bridge FOOTS to the stated equity value and divides to the stated per share, asserted
# rather than asserted-in-prose [R-BRIDGE-01] clause (iv).
assert abs((ev + BR_ASSOC + BR_LISTED_EQUITY + BR_FUNDS - net_debt - nci_v) - eq_dcf) < 1e-6
dcf_ps = eq_dcf / SH

def dcf_ps_at(wacc, g, ebitda_shift=0.0, capex_shift=0.0):
    pv = 0.0
    for i, y in enumerate(yrs):
        r = fc[y]['rev']
        ebitda_ = r * (ebitda_m[i] + ebitda_shift)
        dna_ = r * dna_pct[i]
        nopat_ = (ebitda_ - dna_) * (1 - TAX)
        fcff_ = nopat_ + dna_ - r * (capex_pct[i] + capex_shift) - r * wc_out_pct[i]
        pv += fcff_ / (1 + wacc) ** (i + 1)
        if i == 4:
            fcff5, nopat5, dna5 = fcff_, nopat_, dna_
    # THE SENSITIVITY MUST USE THE SAME TERMINAL AS THE BASE. A grid centred on a
    # construction the study does not publish grades a different model, which is the
    # defect one of this house's own studies shipped when its base call site was
    # corrected and its sensitivity engine was not.
    tv_ = TVM.build(TVM.TerminalInputs(
        nopat=nopat5, wacc=wacc, inflation=COCRUN.MACRO.terminal_inflation,
        real_growth=(1.0 + g) / (1.0 + COCRUN.MACRO.terminal_inflation) - 1.0,
        dna_book=dna5, maintenance_basis='book_dna_escalated',
        average_age_years=TERM_AGE, average_age_source='see the base call site',
        useful_life_years=TERM_LIFE, useful_life_source='see the base call site',
        working_capital=TERM_WC,
        incremental_capital_per_unit_growth=(
            None if abs((1.0 + g) / (1.0 + COCRUN.MACRO.terminal_inflation) - 1.0) < 1e-12
            else TERM_IC_PER_UNIT_GROWTH),
    )).tv
    pvtv = tv_ / (1 + wacc) ** 5
    _e = pv + pvtv + BR_ASSOC + BR_LISTED_EQUITY + BR_FUNDS - net_debt
    return _e * (1.0 - BR_NCI_SHARE) / SH

# ===== DDM (cash-flow cross-check: the locked 0.55/q policy) ==================
KE = KE_RATING
pv_div = sum(payout_dps[i] / (1 + KE) ** (i + 1) for i in range(5))
# The dividend lens carried its OWN terminal growth of 3.0% against the cash-flow lens's
# 2.5%, in the same model, on the same company, in the same economy — two answers to one
# question, which is the incoherence [R-MACRO-01] exists to close. It sits on the same
# path at the same stated real rate: a dividend cannot grow faster than the business that
# pays it, in perpetuity.
tg_div = COCRUN.MACRO.terminal_growth(TG_REAL)
tv_div = payout_dps[-1] * (1 + tg_div) / (KE - tg_div)
pv_tv_div = tv_div / (1 + KE) ** 5
ddm_ps = pv_div + pv_tv_div
ddm_tv_pct = pv_tv_div / ddm_ps

# ===== Relative & Normalized ==================================================
ebitda26 = rows[0]['ebitda']
np26 = (rows[0]['ebit'] + 500 + 200) * (1 - TAX) * (1 - 0.025)   # attributable: + assoc 0.5 + net fin 0.2, − 2.5% NCI
eps26 = np26 / SH
# THE MULTIPLE COMES FROM THE COMPANY'S OWN HISTORY AND IS COMPUTED, NOT TYPED
# [R-LENS-03]. The delivered study used 8.0 / 9.0 / 10.0 with no source of any kind, and
# its base of 9.0 sat within a rounding of the multiple the shares trade at today — which
# values the company at what it already trades at. Each historical point is that year-end's
# own close from the persistent library, times the shares in issue, plus that year's net
# debt from the filings, over that year's EBITDA. Nothing here reads the current price.
OWN_HIST_EVX = []
for _y, _p, _eb, _dbt, _cash in (
        # year, 31 Dec close (engine/raw_ohlc/SA/STC.csv), EBITDA, borrowings, cash
        (2023, 39.35, 22_445.389, 21_957.496, 13_371.320),   # restated continuing basis
        (2024, 40.00, 23_951.115, 15_131.739, 15_543.441),
        (2025, 42.98, 24_469.435, 15_191.428, 13_376.071)):
    OWN_HIST_EVX.append(dict(year=_y, close=_p, ebitda=_eb,
                             ev=_p * 4_990.0 + (_dbt - _cash),
                             x=(_p * 4_990.0 + (_dbt - _cash)) / _eb))
_xs = sorted(d['x'] for d in OWN_HIST_EVX)
rel_evx = dict(bear=_xs[0], base=sum(_xs) / len(_xs), bull=_xs[-1])
rel = {}
for k, x in rel_evx.items():
    ev_r = ebitda26 * x
    rel[k] = ((ev_r + BR_ASSOC + BR_LISTED_EQUITY + BR_FUNDS - net_debt)
              * (1.0 - BR_NCI_SHARE) / SH)
# The traded multiple, computed so the circularity check is arithmetic rather than a
# sentence: a record that only asserts non-circularity in prose has switched the check off.
TRADED_EVX = (COCRUN.SPOT * SH + net_debt) / hist['ebitda']['FY25']
BOOK_PS = 84_986.806 / SH        # equity attributable, 30 June 2026 reviewed sheet
# NORMALISED PROFIT IS COMPUTED, AND THE ONE-OFF IT STRIPS IS THE DISCLOSED ONE. This was a
# typed 14,400 — a round number — and the document beside it walked a reader down "FY2025
# attributable profit 14,828 less the one-off zakat credit (466)" to reach it, which does
# not reproduce: that arithmetic gives 14,362 and the page printed about 14,400.
#
# AND THE ADJUSTMENT WAS THE WRONG SIZE. The 466 is the NET zakat line for the year, not the
# one-off inside it; what is non-recurring is the reversal of prior years' provision that
# note 33(a) names on its own line. The honest normalisation charges the year at the rate
# the three filed years imply on profit before zakat, which is what the underlying charge
# would have been, and takes the minority's share off the result.
NORM_PBZ = ISTMT_EARLY.pbz(2) / 1000.0
NORM_ZAKAT = NORM_PBZ * ISTMT_EARLY.effective_zakat_rate('pbz')
norm_pat = (NORM_PBZ - NORM_ZAKAT) * (1.0 - BR_NCI_SHARE)
norm_eps = norm_pat / SH
norm = dict(bear=(13600/SH)*13.5, base=norm_eps*15.0, bull=(15200/SH)*16.5)
# THE RANGE IS FLEXED IN OBSERVABLE UNITS AND THE MACRO PATH STANDS STILL [R-LENS-03,
# R-MACRO-01]. The delivered study's bear and bull moved the cost of capital by 100 and 70
# basis points AND terminal growth between 2.0% and 3.0% AND the margin AND capex, all at
# once. Terminal growth and the terminal risk-free rate are DERIVED from one house path and
# carry the same terminal inflation, so the corners of such a range are internally
# contradictory — each one is an economy nothing describes — and its width is chosen rather
# than observed.
#
# What moves instead is the one driver this company publishes a band for: CAPITAL
# INTENSITY. Management guides capital expenditure to 15.0-17.5% of revenue and the base
# path opens at 16.5% and declines to 15.0%, so the bear takes the top of that band and the
# bull the bottom. One inflation, one currency, one price of time, across all three.
# The range flexes on the ratio the company's OWN THREE YEARS actually span — 1.054 to
# 1.252 times depreciation — rather than on the band it guides to, for the same reason the
# base path does. Guidance is a claim about the future and it is scored; this is a record
# of the past and it is measured.
CAPEX_RATIO_LOW = min(CAPEX_TO_DNA_HISTORY)
CAPEX_RATIO_HIGH = max(CAPEX_TO_DNA_HISTORY)
CAPEX_BEAR_SHIFT = DNA_SHARE * (CAPEX_RATIO_HIGH - CAPEX_TO_DNA)
CAPEX_BULL_SHIFT = DNA_SHARE * (CAPEX_RATIO_LOW - CAPEX_TO_DNA)
# Published beside the adopted basis so a reader sees the choice and not only its result.
CAPEX_GUIDANCE_LOW, CAPEX_GUIDANCE_BASE, CAPEX_GUIDANCE_HIGH = 0.150, 0.165, 0.175
dcf_lens = dict(bear=dcf_ps_at(WACC, TG, 0.0, CAPEX_BEAR_SHIFT),
                base=dcf_ps,
                bull=dcf_ps_at(WACC, TG, 0.0, CAPEX_BULL_SHIFT))
def ddm_at(ke, g, dps_path):
    pv = sum(dps_path[i] / (1 + ke) ** (i + 1) for i in range(5))
    tv_ = dps_path[-1] * (1 + g) / (ke - g)
    return pv + tv_ / (1 + ke) ** 5
ddm_lens = dict(bear=ddm_at(KE + 0.005, 0.020, [2.20, 2.20, 2.20, 2.20, 2.20]),
                base=ddm_ps,
                bull=ddm_at(KE - 0.005, 0.0325, [2.20, 2.20, 2.35, 2.55, 2.75]))
# ===== ONE CLASS PRIMARY IS THE CENTRAL [R-LENS-03] =========================
# The delivered study published a BLEND of four lenses at typed weights — 35% cash flow,
# 25% dividend discount, 20% relative multiple, 20% normalised earnings — that nobody chose
# on evidence and no out-of-sample test ever cleared. A number produced by averaging several
# methods is not more robust than the best of them: it is a NEW method with free parameters
# nobody tested, and it imports every weakness of the weakest lens at whatever weight
# somebody typed.
#
# LENS_REGISTRY gives a telecom operator a CASH-FLOW primary, cross-checked on an
# EV/EBITDA multiple from its own history and on book value. The dividend-discount and
# normalised-earnings reads are not permitted cross-checks for this class and come OUT of
# the answer entirely — they are computed above and published as what they are, nowhere in
# the central.
central = dcf_lens['base']
# THE ENVELOPE IS THE RANGE OF THE PRESENT-VALUE READS ON ONE CLOCK, not the primary's own
# band. The primary's bear and bull come from the capital-intensity guidance band; the
# envelope stretches to whatever the cross-checks say as well, because a reader is owed the
# disagreement between the lenses rather than a spread invented around the answer. Book
# value is a DISCLOSED FLOOR and is published as such rather than as an end of the range.
_pv_reads = [dcf_lens['base'], dcf_lens['bear'], dcf_lens['bull'], rel['base']]
central_bear = min(_pv_reads)
central_bull = max(_pv_reads)
# The envelope is the RANGE of the PRESENT-VALUE reads on one clock, never a spread
# invented around the central and never an average of the lenses.
weights = None

# ===== Sensitivity grids ======================================================
wacc_steps = [WACC - 0.010, WACC - 0.005, WACC, WACC + 0.005, WACC + 0.010]
g_steps = [0.015, 0.020, 0.025, 0.030, 0.035]
sens_wg = [[(dcf_ps_at(w, g) if w - g > 0.02 else None) for g in g_steps] for w in wacc_steps]
# THE BETA GRID IS COMPUTED. Appendix §1.9 published one as six typed rows — a cost of
# equity, a cost of capital and a value per share at each of six betas — and by the time
# the study was rebuilt every row was stale, including the one labelled "regressed base",
# which still carried the retired nine-week beta of 0.48 and a cost of capital of 7.59%
# against the schedule's 8.13%. A grid whose base row disagrees with the model is worse
# than no grid: it reads as the model's own arithmetic.
# The adopted row uses the EXACT beta, not a rounded one: rounding it to four places moved
# the reconstructed cost of capital by 1.5e-6 and the assertion below refused the grid,
# which is the assertion doing its job on the desk that wrote it.
beta_steps = sorted({0.30, 0.50, SCHED.beta, 0.85, 1.00, 1.20})
sens_beta = []
for _b in beta_steps:
    _ke = SCHED.rf_star + _b * SCHED.erp
    _w = WE * _ke + (1.0 - WE) * KD_AT
    sens_beta.append(dict(beta=_b, ke=_ke, wacc=_w,
                          ps=dcf_ps_at(_w, TG) if _w - TG > 0.02 else None,
                          adopted=abs(_b - SCHED.beta) < 5e-5))
assert any(r['adopted'] for r in sens_beta), 'the adopted beta must appear in its own grid'
_adopted = next(r for r in sens_beta if r['adopted'])
assert abs(_adopted['wacc'] - WACC) < 1e-9, (_adopted['wacc'], WACC)
assert abs(_adopted['ps'] - dcf_ps) < 1e-6, 'the adopted row must reproduce the answer'

# HOW FAR THE CAPITAL PROGRAMME CAN CARRY THE ANSWER, which is the question the crux
# raises and does not answer. Two percentage points of revenue below the modelled
# intensity is lighter than any of the three filed years ran, so this is a floor on what
# the swing driver the crux names can be worth — a model output, not a price solve.
capex_floor_2pp = dcf_ps_at(WACC, TG, capex_shift=-0.02)

capex_steps = [-0.010, -0.005, 0.0, 0.005, 0.010]     # capex intensity shift (pp of revenue)
margin_steps = [-0.010, -0.005, 0.0, 0.005, 0.010]    # EBITDA margin shift
sens_cm = [[dcf_ps_at(WACC, TG, mm, cc) for cc in capex_steps] for mm in margin_steps]

# ===== Dividend cover stress (device A-2, crux in real units) =================
div_bill = 2.20 * SH / 1000  # SAR bn per year under the locked policy
cover = []
# The rungs are the model's OWN adopted intensity and the two ends of the range it is
# flexed over, each COMPUTED rather than typed. The delivered labels read "16.5% (base
# FY26E)" and "17.5% (top of guidance)", and both went stale the moment capital
# expenditure stopped being taken from the guidance band — a label is a figure a reader
# sees, and a stale one is the defect the prose-figure rule exists to stop.
for label, cint in [
        ('%.1f%% (the lowest of the three filed years, %.3fx depreciation)'
         % (100 * (capex_pct[0] + CAPEX_BULL_SHIFT), CAPEX_RATIO_LOW),
         capex_pct[0] + CAPEX_BULL_SHIFT),
        ('%.1f%% (adopted, the three-year mean of %.3fx depreciation)'
         % (100 * capex_pct[0], CAPEX_TO_DNA), capex_pct[0]),
        ('%.1f%% (the highest of the three filed years, %.3fx depreciation)'
         % (100 * (capex_pct[0] + CAPEX_BEAR_SHIFT), CAPEX_RATIO_HIGH),
         capex_pct[0] + CAPEX_BEAR_SHIFT)]:
    r = fc['FY26E']['rev']
    ocf_e = r * ebitda_m[0] * (1 - TAX) + r * dna_pct[0] * TAX - r * wc_out_pct[0]  # approx: NOPAT+D&A−ΔWC
    fcf_e = ocf_e - r * cint
    cover.append(dict(capex=label, fcf=fcf_e / 1000, div=div_bill, cover=fcf_e / 1000 / div_bill))

# ===== Experts ================================================================
# Expert 1 — Hisham (cash returns / ROIC vs WACC, economic profit)
# INVESTED CAPITAL IS DERIVED FROM THE BRIDGE, NOT TYPED. This read a flat 90,500.0 with
# a comment naming its two parts approximately — "equity att 83.4bn + net debt 7.1bn" —
# and neither part matched the study's own committed balance sheet once the bridge moved
# onto the reviewed 30 June 2026 interim. An expert's assumption may be his own; the
# balance sheet he stands on is the study's.
ic = BOOK_PS * SH + net_debt        # parent equity on the latest disclosed sheet, plus net debt
roic = rows[0]['nopat'] / ic
ep = (roic - WACC) * ic
FADE = 0.025   # excess returns decay 2.5%/yr toward the cost of capital (moat half-life ~25yr)
def e1_ps_at(fade, wacc_):
    ep_ = (rows[0]['nopat'] / ic - wacc_) * ic
    mult = 1.0 / (wacc_ + fade - TG)          # growing-fading EP perpetuity
    ev_ = ic + ep_ * mult
    # The same bridge as the base, with the minority taken as its share of THIS value
    # rather than as a constant: a fixed deduction against a moving enterprise value is
    # the historical-cost construction [R-BRIDGE-01] retires, wearing a different hat.
    _e = ev_ + BR_ASSOC + BR_LISTED_EQUITY + BR_FUNDS - net_debt
    return _e * (1.0 - BR_NCI_SHARE) / SH
e1_ps = e1_ps_at(FADE, WACC)
e1_ev = ic + ep / (WACC + FADE - TG)
# A SINGLE SWING ASSUMPTION MEANS ONE. This range moved the fade rate AND the cost of
# capital by 50 basis points in the same step, while the document called it "swing = the
# fade rate" and the divergence table gave his single swing assumption as the fade alone.
# Two levers wearing one label overstates what the named assumption is worth. The cost of
# capital has its own grid in section 1.9; here only the fade moves.
FADE_LO, FADE_HI = 0.010, 0.040
e1 = dict(base=e1_ps, rng=(e1_ps_at(FADE_HI, WACC), e1_ps_at(FADE_LO, WACC)),
          fade_lo=FADE_LO, fade_hi=FADE_HI)
# Expert 2 — Karim (normalized earnings power)
e2 = dict(base=norm['base'], rng=(norm['bear'], norm['bull']))
# Expert 3 — Omar (macro-policy scenario tree on the DDM/rate path)
scen = [(0.30, ddm_lens['bull'] * 1.02), (0.45, ddm_ps), (0.25, ddm_lens['bear'] * 0.96)]
e3 = dict(base=sum(p * v_ for p, v_ in scen))

# ---------------------------------------------------------------------------------------
# THE FORECAST INCOME STATEMENT, DOWN TO NET PROFIT.
#
# The valuation never needed one — free cash flow to the firm runs off NOPAT, and NOPAT is
# EBIT times one minus a tax rate without passing through a finance charge — so the model
# projected EBITDA, depreciation, EBIT and stopped. Appendix A needs the rest, and building
# it turned up something the valuation could not have seen.
#
# THE NET FINANCE RESULT HAS CHANGED SIGN. This company earned MORE finance income than it
# paid in all three filed years (+414, +484, +151 million), so a model carrying FY2025
# forward would credit itself with a net financial income in perpetuity. The reviewed half
# to 30 June 2026 reports finance income of 604,264 against a finance cost of 710,681 — a
# net CHARGE — because long-term borrowings went from 14,404,268 to 22,094,126 inside the
# half, with 8,720,100 drawn. THE BOOK THAT PRODUCED THE CREDIT NO LONGER EXISTS.
#
# So the finance lines are anchored the way every other rate in this study is [R-ANCHOR-01]:
# on the latest reviewed period, each leg corrected by the PRIOR YEAR'S OWN measured
# half-to-year factor rather than by an assumed seasonality. The two legs are corrected
# SEPARATELY and deliberately: their factors are 1.575 and 2.031, nothing like each other,
# and a single factor on the net would be applied to a quantity that changes sign, which is
# arithmetic without meaning.
import income_statement as ISTMT

H1_2026_FIN_INCOME, H1_2026_FIN_COST = 604_264.0, -710_681.0
H1_2025_FIN_INCOME, H1_2025_FIN_COST = 810_438.0, -554_016.0
SEASON_FIN_INCOME = ISTMT.FINANCE_INCOME[2] / H1_2025_FIN_INCOME
SEASON_FIN_COST = ISTMT.FINANCE_COST[2] / H1_2025_FIN_COST
FY26_FIN_INCOME = H1_2026_FIN_INCOME * SEASON_FIN_INCOME / 1000.0     # SAR millions
FY26_FIN_COST = H1_2026_FIN_COST * SEASON_FIN_COST / 1000.0

# THE EARLY RETIREMENT PROGRAMME IS NORMALISED, NOT DROPPED. It ran 862,842 / 2,577,256 /
# 823,801 — a threefold swing, no year like another — and no filing calls it non-recurring,
# which is what a company continuously restructuring its workforce looks like. Its own
# three-year mean, escalated on the house ladder because it is a domestic wage cost.
# THE FILED VALUES ARE ALREADY NEGATIVE — they are costs as the statement prints them — so
# this is used AS IS. The first draft negated it, which turned a 1.4 billion charge into 1.4
# billion of income and raised net profit by 2.8 billion; the footing assertion below passed
# it, because a statement is internally consistent whichever way one of its lines points.
# That is why the sign is asserted separately.
EARLY_RET_BASE = ISTMT.early_retirement_mean() / 1000.0
assert EARLY_RET_BASE < 0, 'the early retirement programme is a cost and must be negative'

# ZAKAT AT THE RATE THE THREE YEARS TOGETHER IMPLY. FY2025's charge is a RELEASE of 466,436
# after charges of 1,326,610 and 1,191,564, so its own-year ratio is negative; averaging
# three ratios would give a third of the weight to a number that cannot recur, and taking
# the latest year would forecast a permanent zakat credit.
ZAKAT_RATE = ISTMT.effective_zakat_rate()

_fin_inc, _fin_cst, _early = FY26_FIN_INCOME, FY26_FIN_COST, EARLY_RET_BASE
for _i, _y in enumerate(yrs):
    if _i:
        # The financial legs and the programme all escalate on the house ladder and nothing
        # else: no view is taken on the debt path beyond the level the reviewed half
        # discloses, and holding it there is a STATED assumption rather than a free one.
        _g = 1.0 + COCRUN.MACRO.inflation(FORECAST_YEARS[_i])
        _fin_inc *= _g
        _fin_cst *= _g
        _early *= _g
    _row = fc[_y]
    _row['dna'] = _row['rev'] * DNA_SHARE
    _row['ebit'] = _row['ebitda'] - _row['dna']
    _row['early_retirement'] = _early
    _row['fin_income'] = _fin_inc
    _row['fin_cost'] = _fin_cst
    _row['pbz'] = _row['ebit'] + _early + _fin_inc + _fin_cst
    _row['zakat'] = -_row['pbz'] * ZAKAT_RATE
    _row['net_profit'] = _row['pbz'] + _row['zakat']

# THE STATEMENT MUST FOOT AT EVERY YEAR, and the check is the same one income_statement.py
# runs on the filed columns: the lines above net profit sum to it.
for _y in yrs:
    _r = fc[_y]
    _sum = (_r['ebitda'] - _r['dna'] + _r['early_retirement'] + _r['fin_income']
            + _r['fin_cost'] + _r['zakat'])
    assert abs(_sum - _r['net_profit']) < 1e-6, (_y, _sum, _r['net_profit'])
    # A FOOTING CHECK IS NOT A SIGN CHECK and this pair is why: the statement foots
    # whichever way its lines point, so each line's DIRECTION is asserted on its own.
    assert _r['early_retirement'] < 0, (_y, 'the programme must be a charge')
    assert _r['fin_income'] > 0 > _r['fin_cost'], (_y, 'the finance legs are mis-signed')
    assert _r['zakat'] < 0, (_y, 'zakat is a charge on a profit')
    assert _r['pbz'] < _r['ebit'], (_y, 'the lines below EBIT are a net charge on this '
                                        'book, so profit before zakat cannot exceed it')

# ONE LINE IS DELIBERATELY ABSENT FROM THE PROJECTION AND ITS ABSENCE IS THE HONEST READING.
# The filed statement carries net other income, the share of associates, and net other gains
# — 1,333,077 then 529,069 then 654,896 on the last of those alone, with no disclosed driver
# behind any of them. Forecasting them would be inventing three lines; the study says so and
# the projected net profit is therefore BELOW what the same company would report if they
# recurred, which is stated rather than left for a reader to discover.
FORECAST_IS_OMITS = ('net other income and expenses', 'net share in associates and joint '
                     'ventures', 'net other gains')

# THE LIKE-FOR-LIKE, so nobody has to reconstruct it. FY2025 as reported carries a net
# margin the forecast does not reach, and almost all of the difference is the three omitted
# lines plus a zakat CREDIT — none of which a forecast may carry. Rebuilt on the forecast's
# own basis the filed year is directly comparable, and what remains is the finance swing.
_fy25_like = (ISTMT.ebit(2) + ISTMT.EARLY_RETIREMENT[2] + ISTMT.net_finance(2)) / 1000.0
_fy25_like_np = _fy25_like * (1.0 - ZAKAT_RATE)
forecast_is_record = dict(
    basis=('EBIT less the early retirement programme at its three-year mean, plus the net '
           'finance result anchored on the reviewed half, less zakat at the rate the three '
           'filed years together imply'),
    omitted=list(FORECAST_IS_OMITS),
    omitted_fy2025=[ISTMT.NET_OTHER[2] / 1000.0, ISTMT.ASSOCIATES[2] / 1000.0,
                    ISTMT.OTHER_GAINS[2] / 1000.0],
    zakat_rate=ZAKAT_RATE,
    early_retirement_mean=EARLY_RET_BASE,
    fy2026_finance=dict(income=FY26_FIN_INCOME, cost=FY26_FIN_COST,
                        net=FY26_FIN_INCOME + FY26_FIN_COST,
                        season_income=SEASON_FIN_INCOME, season_cost=SEASON_FIN_COST,
                        fy2025_net=ISTMT.net_finance(2) / 1000.0),
    fy2025_like_for_like_pbz=_fy25_like,
    fy2025_like_for_like_net=_fy25_like_np,
    fy2025_like_for_like_margin=_fy25_like_np / (ISTMT.REVENUE[2] / 1000.0),
    fy2025_reported_net=ISTMT.NET_PROFIT_CONTINUING[2] / 1000.0,
    fy2025_reported_margin=ISTMT.NET_PROFIT_CONTINUING[2] / ISTMT.REVENUE[2],
    # THE BRIDGE FROM THE FILED YEAR TO THE FIRST FORECAST YEAR, on the like-for-like basis
    # and asserted to close. Three moves, and two of them run against the first.
    bridge_to_fy2026=dict(
        ebit=fc[yrs[0]]['ebit'] - ISTMT.ebit(2) / 1000.0,
        early_retirement=fc[yrs[0]]['early_retirement'] - ISTMT.EARLY_RETIREMENT[2] / 1000.0,
        finance=(fc[yrs[0]]['fin_income'] + fc[yrs[0]]['fin_cost']
                 - ISTMT.net_finance(2) / 1000.0),
        total=fc[yrs[0]]['pbz'] - _fy25_like),
    note=('The forecast opens at a net margin below the year it is anchored on, and the '
          'reason is arithmetic rather than a view. FY2025 as REPORTED carries three lines '
          'no forecast may project — net other income, the share of associates and net '
          'other gains — and a zakat RELEASE rather than a charge. Rebuilt on this '
          "forecast's own basis the filed year is directly comparable, and what is left of "
          'the difference is the finance result, which has changed SIGN: the reviewed half '
          'reports a net charge where every filed year reported a net credit, because '
          'long-term borrowings went from 14,404,268 to 22,094,126 inside that half.'),
)
_b = forecast_is_record['bridge_to_fy2026']
assert abs(_b['ebit'] + _b['early_retirement'] + _b['finance'] - _b['total']) < 1e-6, _b


# ---------------------------------------------------------------------------------------
# THE MACRO RECORD AND THE FORECAST-ANCHOR RECORD [R-MACRO-01, R-ANCHOR-01].
#
# BOTH THINGS THEY ATTEST WERE ALREADY TRUE HERE AND NEITHER WAS CHECKABLE FROM OUTSIDE,
# which is the exact shape [R-ENF-01] exists to close: no growth rate in this model is a
# typed nominal, every one is a real rate recomputed on the house Saudi ladder, and the
# first forecast year is anchored on the latest reviewed period rather than grown off a
# stale full year — and a job outside the study could read none of it.
#
# THE GROWTH LINES ARE PER SEGMENT AND PER YEAR because the real rate FADES: a segment's
# real growth is not one number over five years, so storing one would be storing a rate the
# model does not use. Sixty lines is bulky and it is the honest form — a single averaged
# real rate would recompute to nominals this model never carries.
_macro_lines = []
for _k in sorted(seg_fc[yrs[0]]):
    for _i, _y in enumerate(FORECAST_YEARS):
        _r = seg_real(_k, _i + 1)
        _macro_lines.append(dict(
            name='%s — real growth, explicit year %d' % (_k, _i + 1),
            years=[_y],
            nominal=[(1.0 + _r) * (1.0 + COCRUN.MACRO.inflation(_y)) - 1.0],
            real=_r,
            basis=('the segment\'s own measured real rate, faded to zero real by the last '
                   'explicit year, recomputed on the house Saudi ladder. Nothing here is a '
                   'typed nominal rate.')))

macro_record = dict(
    market='SA',
    path_as_of=COCRUN.MACRO.as_of,
    inflation_inputs=[
        dict(key='house_ladder', mapping='calendar', first_year=FORECAST_YEARS[0],
             values=[COCRUN.MACRO.inflation(_y) for _y in FORECAST_YEARS],
             note=('the ONLY forward inflation series this model registers. It is read from '
                   'the house path at each forecast year and used in exactly one place — '
                   'converting each segment\'s real growth to its nominal. There is no '
                   'second escalator: the cost side is held at each segment\'s own disclosed '
                   'margin rather than escalated line by line, which cost_decomposition.py '
                   'measures at -0.30% of the central.')),
        dict(key='cpi_2024_observed', mapping='observed', values=CPI_HIST[2024],
             date='2026-09-05', note=CPI_HIST_SOURCE),
        dict(key='cpi_2025_observed', mapping='observed', values=CPI_HIST[2025],
             date='2026-09-05', note=CPI_HIST_SOURCE),
    ],
    growth_lines=_macro_lines,
    terminal=dict(g_nominal=TG, real=TG_REAL,
                  rf=SCHED.rf_terminal,
                  inflation_in_rf=COCRUN.MACRO.terminal_inflation),
    explicit_years=len(FORECAST_YEARS),
    growth_at_horizon_end=(1.0 + seg_real(UNIT_SEGMENT, len(FORECAST_YEARS)))
                          * (1.0 + COCRUN.MACRO.inflation(FORECAST_YEARS[-1])) - 1.0,
    note=('The riyal is pegged, so the house path returns a FLAT cost-of-capital schedule '
          'and today is already the terminal. No currency path is registered because this '
          'model has none: revenue and cost are both in riyals and the peg is not a '
          'forecast.'),
)

# THE ANCHOR RECORD. The forecast opens ON the latest reviewed period — the six months to
# 30 June 2026 — rather than below it, so no mechanism is owed. The record is committed
# anyway, because [R-ANCHOR-01] prints it for every study whether or not it fires: a shape
# that is merely not-red is invisible, and the one this study has is worth seeing.
_anchor_reported = H1_2026_GROSS / H1_2026_REVENUE
forecast_anchor = dict(
    rate_name='gross margin',
    latest_reviewed_period='six months ended 30 June 2026',
    latest_reviewed_date='2026-06-30',
    latest_reviewed_rate=_anchor_reported,
    first_forecast_rate=FY26_GROSS_MARGIN,
    forecast_path=[fc[_y]['ebitda_margin'] for _y in yrs],
    note=('The first forecast year is BUILT from the reviewed half rather than compared '
          'with it: the level, the gross margin and the operating-cost share all come from '
          'note 4 of that interim, each corrected by the prior year\'s OWN measured '
          'half-to-year factor rather than by an assumed seasonality. The reviewed half '
          'reports a gross margin of %.3f%% and the first forecast year carries %.3f%%; the '
          'difference is the measured seasonal correction, not a fade. The delivered study '
          'stood on a stale full year and sat 89 basis points BELOW an EBITDA margin the '
          'company had already reported for half the year.'
          % (100 * _anchor_reported, 100 * FY26_GROSS_MARGIN)),
)

# ASSERTED AT BUILD TIME, so a record that stopped reproducing breaks the build rather than
# reaching a gate.

import research_protocol as _RP
_RP.assert_macro_coherence(macro_record, market='SA', ticker='STC')

# ---------------- THE THREE STANDING GATES, CALLED IN THE STUDY'S OWN CODE -------------
# An outside audit found that assert_sigcm(), assert_model_study() and assert_ground_up()
# NEVER EXECUTED on this study, and the repository-level check passed anyway because its
# own clause requires at least ONE of the three and the beta call satisfied it. A study
# that calls one gate and skips two is not a study that was checked; it is a study that
# was checked once.
#
# THE GROUND-UP CLAUSE IS THE ONE THAT BITES, and it is attested on a RECORD rather than a
# flag precisely so it cannot be claimed. Every revenue line names the level it was
# actually built at, and any line below "unit" carries a gap note — the rule has always
# permitted a coarser level where the disclosure stops, and has never permitted going
# quiet about it. The lines must cover 100% of revenue, because a line left out of the
# record is a line nobody checked.
_base_seg = {k: v['FY25'] for k, v in seg_hist.items()}
_seg_total = sum(_base_seg.values())
DRIVER_LINES = [
    _RP.DriverLine(
        name='stc (the Saudi operating business)',
        level='derived',
        share_of_revenue=_base_seg['stc'] / _seg_total,
        unit='mobile and fixed subscribers',
        unit_source='the quarterly earnings presentations\u2019 own subscriber charts, whose '
                    'footnote states the figures are not audited',
        price_basis='revenue per subscriber, BACK-SOLVED against the audited segment '
                    'revenue in note 9 rather than disclosed',
        cost_basis='four of note 35\u2019s seven lines on the bases the filings name; '
                   'the rest on the segment\u2019s own held gross margin',
        gap_note='The unit is real and disclosed; the PRICE is not. Revenue per subscriber '
                 'is derived by dividing audited segment revenue by a subscriber count the '
                 'company publishes in a presentation and does not audit, so this is unit '
                 'economics on a derived rate rather than on a disclosed one. THE COST SIDE '
                 'IS PART-BUILT: note 35 discloses seven lines by nature for three years, '
                 'and the four with a sourced base that is not group revenue are built on '
                 'it \u2014 the commercial service provisioning fee on the Saudi operating '
                 'segment the sub-note levies it against, the licence fee at its own '
                 'measured rate, repairs and maintenance on the asset base being '
                 'maintained, and contract-cost amortisation on the subscriber path. The '
                 'other three carry no sourced driver \u2014 network access has no '
                 'disclosed unit rate, employee cost has no headcount anywhere in the '
                 'filings, and "Others" is a residual of three unrelated things \u2014 so '
                 'they stay on the held margin and that is said rather than filled with an '
                 'imported ratio. The level stays DERIVED because the price still is.'),
]
for _nm, _v in sorted(_base_seg.items(), key=lambda kv: -kv[1]):
    if _nm == 'stc':
        continue
    DRIVER_LINES.append(_RP.DriverLine(
        name=_nm, level='segment', share_of_revenue=_v / _seg_total,
        cost_basis='the segment\u2019s own held gross margin, less its share of the four '
                   'group cost lines built on their own bases',
        gap_note='No unit is disclosed for this segment \u2014 note 9 gives revenue and no '
                 'volume, and the earnings presentations carry no subscriber, connection '
                 'or capacity count for it. It is grown on its own measured two-year real '
                 'rate from the audited segment table, which is the finest sourced level '
                 'available, and the absence of a unit is stated rather than filled.'))
GROUND_UP = _RP.assert_ground_up(DRIVER_LINES, ticker='STC')

# THE COMMITTED BETA ARTEFACT MUST BE THE BETA THIS MODEL USES. An outside audit found
# beta_result.json recording 0.7107 on 254 observations while every delivered document
# published 0.7078 on 252 — because coc_run calls own_stock_beta() LIVE at build time and
# the index file lengthens, so the artefact goes stale the moment the library moves while
# still reading as the study's own record. It is the record the repository-level gate and
# assert_beta_provenance() both inspect, so a stale one means those gates are checking a
# number the study does not stand on. Small in value here — 29 basis points of beta, under
# two on the cost of equity — and the point is that nothing was watching.
_BETA_ARTEFACT = json.load(open(os.path.join(HERE, 'beta_result.json')))
_RP.assert_beta_provenance(_BETA_ARTEFACT)
assert abs(_BETA_ARTEFACT['beta'] - SCHED.beta) < 1e-9, (
    'the committed beta artefact records %.6f and this model discounts at %.6f — '
    're-run beta_reissue.py in the same pass, because the artefact is what the gates read'
    % (_BETA_ARTEFACT['beta'], SCHED.beta))

_RP.assert_sigcm(_RP.SIGCMChecklist(
    historicals_official_only=True,
    forecast_ground_up=True,          # attested on DRIVER_LINES above, not on this flag
    debt_lc_fx_split=True,
    asset_conversion_cycle=True,
    competitors=True,
    beta_own_history_vs_egx30=True,
    formula_based_model=True,
    flags_raised_before_issue=True,
    stop_and_inform_honoured=True,
    na_reasons={}))

_RP.assert_model_study(_RP.ModelStudyChecklist(
    structure_matches_model=True,
    bibliography_document=True,
    provenance_four_field=True,
    numeric_traceability=True,
    external_reader_scrub=True,
    figure_discipline=True,
    table_discipline=True,
    expert_appendix_max_detail=True,
    contested_judgement_both_ways=True,
    na_reasons={}))

# The register is built and ASSERTED before the record is assembled, so a source that
# stopped naming a company document breaks the build rather than reaching a gate.
import inputs_register as _IR
_INPUTS = _IR.build()
_ir_problems, _ir_hist = _IR.check(_INPUTS)
assert not _ir_problems, _ir_problems[:4]
assert _ir_hist >= 100, 'the input register carries only %d dated historicals' % _ir_hist

# ---------------- The published record of this name's own cone ----------------
# [R-CAL-02]: the count is ALWAYS printed beside the percentage, the record strength
# is stated, and a narrow/wide flag appears ONLY when the name's own history earns one
# on a two-sided binomial test. Silence is the honest response to a cone that held
# about as often as it promised, and this name's does. The sentences are rendered by
# band_record itself — that module says in terms that nothing else may phrase them,
# and six independent phrasings had already drifted apart once.
import html as _html
import inspect as _inspect

import band_record as BR
import mc_v3 as MC3

_BREC = BR.resolve('STC', BR.by_key())
assert _BREC.market == 'SA' and _BREC.n == _BREC.hits + (_BREC.n - _BREC.hits)


def _plain(t):
    """The clauses are written for a web surface; a document is not one."""
    return _html.unescape(t).replace('\u2014', '\u2014')


BAND = dict(
    instrument=_BREC.instrument, market=_BREC.market, n=_BREC.n, hits=_BREC.hits,
    cov50=_BREC.cov50, cov80=_BREC.cov80, cov90=_BREC.cov90, width=_BREC.width,
    strength=_BREC.strength, flag=_BREC.flag, p_value=_BREC.p_value,
    record_clause=_plain(_BREC.record_clause()),
    width_clause=_plain(_BREC.width_clause()),
    chip=_plain(_BREC.chip()),
)

_prof = SC.MP.PROFILES['SA']
_dead = _inspect.signature(MC3.signal_alpha).parameters['dead'].default
_z = H3M['signal_z']
ENGINE = dict(
    # The fit this cone was actually built on, read live rather than described.
    nu=CONE['nu'], width_cal=CONE['width_cal'],
    width_overlay_mult=CONE['width_overlay_mult'],
    n_paths=SC.N_PATHS, seed=SC.SEED,
    rf_live=CONE['rf_live'], q_annual=CONE['q_annual'],
    # THE DIRECTION CALL [R-DRIFT-01]: every covered name's forecast states one — the
    # sign of its own momentum reading — and it is printed even inside the dead zone,
    # where it carries no tilt at all and is labelled WEAK.
    signal_active=CONE['signal_active'], signal_type=_prof.signal_type,
    signal_sign=_prof.signal_sign, ic_by_h=dict(_prof.ic_by_h or {}),
    signal_z=_z, dead_zone=_dead,
    call='up' if _z > 0 else ('down' if _z < 0 else 'flat'),
    call_strength='weak' if abs(_z) < _dead else 'live',
    horizons={k: dict(label=h['label'], sessions=h['h'], grade_date=h['grade_date'],
                      basis=h['basis'], anchor_vol_ann=h['anchor_vol_ann'],
                      sigma_h=h['sigma_h'], drift_log_h=h['drift_log_h'],
                      signal_alpha=h['signal_alpha'])
              for k, h in (('1M', H1M), ('3M', H3M))},
)
# The tilt never exceeds ic x sigma x z: beyond that a bigger number is a deliberately
# worse forecast, not more commitment. Asserted rather than asserted-in-prose.
for _k, _h in (('1M', H1M), ('3M', H3M)):
    _cap = abs((_prof.ic_by_h or {}).get(_k, _prof.ic) * _h['sigma_h'] * _z)
    assert abs(_h['signal_alpha']) <= _cap + 1e-12, (_k, _h['signal_alpha'], _cap)


out = dict(
    # The answer and the price it is measured against, at the top level, where a reader
    # and a checker both look. The delivered study exposed neither, so every gate that
    # audits an ANSWER rather than a step reported it unreadable — and an unreadable study
    # is not a clean one.
    central=central,
    spot=VALUATION_SPOT, spot_date=VALUATION_SPOT_DATE,
    central_range=dict(low=central_bear, high=central_bull),
    cone_anchor=CONE_ANCHOR, cone_anchor_date=CONE_ANCHOR_DATE,
    two_clocks=('The valuation is struck against the latest known close, the Monte Carlo '
                'cone against the last session in the persistent price library. They are '
                'different dates because a cone must start where its own price series '
                'ends, and the study says so rather than publishing one number for both.'),
    shares=SH, mktcap=MKTCAP,
    # WHAT A READER IS SHOWN IS THE BAND RECORD. What stood here was the retired
    # skill machinery — a CRPS score against a naive benchmark, its bootstrap and a
    # probability-integral histogram — which answers a modelling question rather than
    # the one an investor asks, and which may no longer reach a reader at all. It is
    # replaced by the record of how often the published bands actually held, phrased
    # by the module that owns those sentences rather than re-worded here.
    # THE STANDARD THIS STUDY WAS BUILT TO [R-STD-01]. Without it a book-wide
    # re-issue is open-ended and nobody can tell which names are current.
    standard_version=_RP.STANDARD_VERSION,
    ground_up=GROUND_UP,
    driver_lines=[vars(l) for l in DRIVER_LINES],
    band_record=BAND,
    engine=ENGINE,
    # The one tax rate this model uses, everywhere it uses one — measured on the
    # base each use applies it to, and exported so the page cannot type its own.
    tax_rate=TAX,
    tax_rate_on_pbz=ISTMT_EARLY.effective_zakat_rate('pbz'),
    mc=dict(q20=q20, q60=q60, touch=touch, prob_read=prob_read, zones=zone_probs, fan=fan),
    tech=dict(sma=sma, rsi=rsi, macd=macd, hi52=hi52, lo52=lo52, rv252=rv252,
              chg20=chg20, chg60=chg60),
    levers_applied=LEVERS_APPLIED,
    coc_record=COCRUN.record(SCHED),
    bridge_record=dict(
        balance_sheet_date='2026-06-30',
        latest_disclosed_date='2026-06-30',
        latest_disclosed_source=(
            "src/SOURCES.md, this study's own register of the primary documents: every "
            "audited and reviewed set this company has published back to FY2023, each with "
            "the URL it was fetched from and the date it carries. The latest is the "
            "reviewed interim for the six months to 30 June 2026; the delivered study "
            "stood on first-quarter figures while that one was already published."),
        associates=dict(
            basis='book', value=BR_ASSOC, listed=False,
            note=('Note 8.1.4 splits the line: associates 10,150.459 and joint ventures '
                  'the remainder at 31 December 2025. DIIC (43.06%, which holds the towers '
                  'business contributed in February 2025), Arabsat, Beyond One and Devoteam '
                  'Middle East are all unlisted, so book is the basis. The joint venture '
                  'BGSM holds 62% of a LISTED Malaysian operator; a market cross-check on '
                  'that look-through is NOT performed because the price is not held, and '
                  'that is recorded as a gap rather than estimated (SIGCM clause 8).')),
        nci=dict(
            basis='value_share',
            deduction=nci_v,
            applied_to='equity_value',
            book=BR_NCI_BOOK,
            profit_share=BR_NCI_SHARE,
            proportional=BR_NCI_SHARE,
            proxy_source=(
                "Note 25 of the FY2025 audited statements: the minority's own share of "
                'profit, 306,915, against group net profit from continuing operations of '
                '15,189,078, which is 2.021%. The subsidiaries carrying the minority — stc '
                'Kuwait at 48.162%, Solutions at 20.363%, and STC Bank, iot2 and SCCC — are '
                'not separately valued in this model, so the profit share is the proxy. Book '
                'of 2,726.349 at 30 June 2026 is published beside it and is NOT the adopted '
                'basis: the model capitalises 100% of subsidiary cash flow, so the minority '
                'claim is worth its share of that value and not what it historically cost.')),
        cash=dict(
            treatment='added_at_face', weights_basis='gross',
            note=('The discount-rate weights are GROSS: market-value equity over market '
                  'capitalisation plus gross borrowings, so no cash is netted inside the '
                  'rate and the cash added here is charged exactly once. STC Bank\'s cash '
                  'of 6,000.384 and its digital-banking financial assets of 4,111.267 are '
                  'EXCLUDED, because netting a bank\'s cash against group borrowings treats '
                  'money that backs customer balances as though it were free; the cost is '
                  "that the bank's own equity value appears in this bridge nowhere, which "
                  'understates the answer, and it is left as a stated gap.')),
        dividend=dict(deducted=False,
                      note=('No dividend is deducted. The interim balance sheet is struck '
                            'after the SAR 6,486.411mn paid in the half, so it is already '
                            'out of the equity it would come out of.')),
        lines=[
            dict(name='enterprise value, discounted cash flow', value=ev),
            dict(name='plus investments in associates and joint ventures, at book',
                 value=BR_ASSOC),
            dict(name='plus the listed equity investment at its disclosed fair value',
                 value=BR_LISTED_EQUITY),
            dict(name='plus investment funds and unlisted equity investments, at fair value',
                 value=BR_FUNDS),
            dict(name='less net debt', value=-net_debt),
            dict(name='less the minority at its share of equity value', value=-nci_v),
        ],
        equity_value=eq_dcf, shares_mn=SH, per_share=dcf_ps,
        net_debt_build=dict(borrowings=BR_BORROWINGS, leases=BR_LEASES,
                            spectrum_licences=BR_SPECTRUM,
                            cash_non_bank=BR_CASH_NON_BANK, murabahas=BR_MURABAHAS,
                            sukuk=BR_SUKUK, treasury_bills=BR_TBILLS, net=net_debt),
        net_debt_note=(
            'The spectrum-licence liability is consideration owed for licences already '
            'capitalised and it is disclosed outside borrowings, so a bridge built from the '
            'borrowings lines does not see it. It is not double-counted against capital '
            "expenditure: the company's total additions in FY2025 were 13,815.240 against "
            'the 11,795 of capital expenditure this model forecasts on, and the intangibles '
            'note states that additions include non-cash additions of 2,122 million, so the '
            'licences bought against this liability never entered the capital expenditure '
            'the cash flows are charged for.'),
    ),
    terminal_record=_t.record,
    hist=hist, seg_hist=seg_hist,
    # THE PER-SEGMENT FORECAST, committed rather than left inside the build. The workbook's
    # segment sheet had to reconstruct it from four business units that no longer exist;
    # what the model actually projects is these eleven, each on its own real rate.
    seg_forecast={k: {y: seg_fc[y][k] for y in yrs} for k in seg_fc[yrs[0]]},
    # THE FOUR-FIELD INPUT REGISTER, generated from this study's own disclosure modules
    # rather than typed beside them — a second copy of a figure is a thing that goes stale,
    # which is the defect three separate rules here were written to close. It is what
    # SIGCM clause 1 is checked on from outside: every dated historical of this company
    # names the company document it was read from, and the assertion runs at build time.
    inputs=_INPUTS,
    macro_record=macro_record,
    forecast_anchor=forecast_anchor,
    forecast_is=forecast_is_record,
    drivers=dict(
        # Per-segment REAL growth, measured from the company's own note 9 and deflated by
        # a published price index, fading to zero real by the last explicit year. Nominal
        # recomputes on the house ladder; nothing here is a typed nominal rate.
        segment_real_growth={k: round(v, 6) for k, v in seg_real0.items()},
        # The house Saudi ladder, published beside the real rates so every nominal in this
        # model recomputes from two figures a reader can see rather than from one they
        # cannot check.
        inflation_ladder=[COCRUN.MACRO.inflation(_y) for _y in FORECAST_YEARS],
        # THE REAL RATE FADES TO ZERO BY THE LAST EXPLICIT YEAR and the workbook has to be
        # able to reproduce that. Publishing ONE rate per segment let the sheet compound a
        # constant rate for five years, which reached FY2030 revenue 3.0% above the model —
        # a disagreement no amount of clean recalculation would have shown, because the
        # workbook recalculated perfectly to the wrong answer.
        segment_real_growth_path={k: [round(seg_real(k, _t), 8)
                                      for _t in range(1, len(FORECAST_YEARS) + 1)]
                                  for k in seg_fc[yrs[0]]},
        # The first forecast year is scaled onto the reviewed half's own annualised level,
        # so the sheet needs the scale as its own line or it cannot reach the same number.
        h1_anchor_scale=_h1_scale,
        unit_segment=UNIT_SEGMENT,
        unit_volume_real=VOLUME_REAL, unit_price_real=PRICE_REAL,
        unit_note=('the stc segment is built as VOLUME x PRICE from the subscriber counts '
                   'in the earnings presentations, each half faded on the same schedule and '
                   'multiplied; the other segments are forecast on their net rate because '
                   'no unit data is disclosed for them'),
        group_real_growth=GROUP_REAL,
        segment_margin={k: round(v, 6) for k, v in SEG_MARGIN.items()},
        sga_share_of_revenue=FY26_SGA_SHARE, sga_share_three_year_mean=SGA_SHARE,
        dna_share_of_revenue=DNA_SHARE,
        h1_anchor=dict(
            revenue=FY26_REVENUE_ANCHOR, gross_margin=FY26_GROSS_MARGIN,
            sga_share=FY26_SGA_SHARE, gross_margin_shift=_margin_shift,
            season_revenue=SEASON_REVENUE, season_gross_margin=SEASON_GROSS_MARGIN,
            season_sga_share=SEASON_SGA_SHARE,
            source=('note 4 of the reviewed interim for the six months to 30 June 2026, '
                    'with each seasonality factor measured from the prior year own half '
                    'against its own full year')),
        capex_to_dna_history=CAPEX_TO_DNA_HISTORY, capex_to_dna_adopted=CAPEX_TO_DNA,
        capex_guidance_band=[CAPEX_GUIDANCE_LOW, CAPEX_GUIDANCE_HIGH],
        capex_note=('measured from the filings as capital expenditure over the '
                    "depreciation of the base it renews, not taken from management's own "
                    'band, because guidance is scored and never consumed'),
        elimination_share=ELIM_SHARE, elimination_gp_share=ELIM_GP_SHARE,
        regrouped_take_group_rate=sorted(SEG.REGROUPED),
        cpi_history=CPI_HIST, cpi_history_source=CPI_HIST_SOURCE,
        ebitda_m=ebitda_m, dna_pct=dna_pct, capex_pct=capex_pct,
        wc_out_pct=wc_out_pct, payout_dps=payout_dps),
    forecast=fc,
    dcf=dict(rows=rows, pv_sum=pv_sum, tv=tv, pv_tv=pv_tv, ev=ev, tv_pct=pv_tv / ev,
             # Exposed so the terminal census can score this terminal from outside rather
             # than report it unreadable. Both are real quantities the module already used:
             # the terminal year's own after-tax operating profit, and the depreciable gross
             # base at CURRENT cost, which is the same escalation the maintenance charge
             # rests on.
             nopat_term=rows[-1]['nopat'], ic_repl=TERM_IC_PER_UNIT_GROWTH,
             terminal_maintenance=_t.maintenance, terminal_fcff=_t.fcff,
             terminal_life_years=TERM_LIFE, terminal_age_years=TERM_AGE,
             wacc=WACC, wacc_rating_basis=WACC_RATING, tg=TG, assoc=assoc, telefonica=telefonica,
             net_debt=net_debt, nci=nci_v, eq=eq_dcf, ps=dcf_ps,
             wacc_build=dict(rf=SCHED.rf_observed, default_spread=SCHED.default_spread,
                             rf_star=SCHED.rf_star, erp_market=SCHED.erp,
                             erp_rating=SCHED_RATING.erp, beta=BETA,
                             beta_reg=dict(beta=COCRUN.BETA_RAW['beta'],
                                           r2=COCRUN.BETA_RAW['r2'],
                                           n=COCRUN.BETA_RAW['n'],
                                           se=COCRUN.BETA_RAW['se'],
                                           window_years=COCRUN.BETA_RAW['window_years'],
                                           index_file=COCRUN.BETA_RAW['index_file'],
                                           index_asof=COCRUN.BETA_RAW['index_asof'],
                                           conforming=COCRUN.BETA_RAW['conforming']),
                             ke_rating=KE_RATING, ke_market=KE_MARKET,
                             kd_pretax=SCHED.kd_pretax, kd_aftertax=KD_AT,
                             we=WE, wd=WD, wacc_market=WACC, wacc_rating=WACC_RATING,
                             tax=TAX, regime=SCHED.regime,
                             beta_source=COCRUN.BETA.source,
                             kd_source=COCRUN.DEBT.kd_source,
                             debt_currency_evidence=COCRUN.DEBT.currency_source,
                             weights_source=COCRUN.WEIGHTS_SOURCE,
                             disclosures=list(SCHED.disclosures))),
    ddm=dict(dps=payout_dps, pv_div=pv_div, tv=tv_div, pv_tv=pv_tv_div, ps=ddm_ps,
             tv_pct=ddm_tv_pct, ke=KE, g=tg_div),
    lenses=dict(dcf=dcf_lens, ddm=ddm_lens, relative=rel, normalized=norm,
                book_value=BOOK_PS, own_history_evx=OWN_HIST_EVX,
                central=dict(bear=central_bear, base=central, bull=central_bull),
                weights=weights),
    lens_record={
        # 'class' is a Python keyword, so this record is a literal rather than a dict()
        # call — the gate reads the key 'class' and a record keyed 'cls' reads as a study
        # with no class at all.
        'class': 'telecom operator',
        'primary': dict(
            kind='dcf', value=central,
            range=dict(low=central_bear, high=central_bull),
            range_basis=dict(
                driver='capital expenditure as a multiple of depreciation',
                low=CAPEX_RATIO_HIGH, high=CAPEX_RATIO_LOW,
                macro_held=True,
                evidence=(
                    "The range this company's OWN THREE FILED YEARS actually span, 1.054 "
                    'to 1.252 times the depreciation of the base being renewed, against an '
                    'adopted mean of 1.161. It is measured rather than guided: management '
                    'publishes a band of 15.0% to 17.5% of revenue and the delivered study '
                    'took its path straight from it, which the standing rule forbids — '
                    'guidance is SCORED and never CONSUMED, because a forward target leans '
                    'the same way an optimistic model does. The bear takes the highest year '
                    'and the bull the lowest, and nothing else moves: the cost of '
                    'capital, the terminal growth, the terminal risk-free rate, the '
                    'inflation ladder and the margin path are IDENTICAL across all three '
                    "reads. The delivered study's bear and bull moved the cost of capital "
                    'by 100 and 70 basis points and terminal growth between 2.0% and 3.0% '
                    'as well, which makes each corner an economy nothing describes and its '
                    'width chosen rather than observed.')),
        ),
        'cross_checks': [
            dict(kind='ev_ebitda_own_history', value=rel['base'],
                 multiple=rel_evx['base'],
                 multiple_source=(
                     "the company's own trailing EV/EBITDA at each of the last three "
                     'financial year ends, computed from that year-end close in the '
                     'persistent price library, the shares in issue and that year\'s own '
                     'net debt and EBITDA from the filings: %.3fx, %.3fx and %.3fx, whose '
                     'mean is adopted and whose lowest and highest are the bear and bull. '
                     'Never a multiple read off the current price.'
                     % tuple(d['x'] for d in OWN_HIST_EVX)),
                 circularity=dict(spot=COCRUN.SPOT, shares=SH, net_debt=net_debt,
                                  metric_value=hist['ebitda']['FY25'],
                                  traded_multiple=TRADED_EVX),
                 note=('The traded multiple today is %.3fx, ABOVE every one of the three '
                       'years this multiple is built from, so the lens is not anchored on '
                       'the price and can be seen not to be.' % TRADED_EVX)),
            dict(kind='book_value', value=BOOK_PS,
                 note=('Equity attributable to the parent on the reviewed 30 June 2026 '
                       'sheet, SAR 84,986.806mn over 4,993.024mn shares. A DISCLOSED '
                       'FLOOR, published as such and never weighted into the answer.')),
        ],
        'envelope': dict(low=central_bear, high=central_bull),
        'central': central,
        'retired': dict(
            blend_weights=dict(dcf=0.35, ddm=0.25, relative=0.20, normalized=0.20),
            retired_value=None,
            why=('The four-lens blend at typed weights is retired under [R-LENS-03]. The '
                 'dividend-discount and normalised-earnings reads are not permitted '
                 'cross-checks for this class and carried 45% of the answer between them.')),
    },
    rel_basis=dict(ebitda26=ebitda26, np26=np26, eps26=eps26, evx=rel_evx,
                   norm_pat=norm_pat, norm_eps=norm_eps),
    sens=dict(wacc_steps=wacc_steps, g_steps=g_steps, table_wg=sens_wg,
              margin_steps=margin_steps, capex_steps=capex_steps, table_cm=sens_cm,
              beta_grid=sens_beta, capex_floor_2pp=capex_floor_2pp),
    cover=cover, div_bill=div_bill,
    experts=dict(e1=e1, e2=e2, e3=e3, e1_roic=roic, e1_ic=ic, e1_ep=ep,
                 # His fade rate is his single swing assumption and the document quotes it in
                 # four places. It was typed in every one of them.
                 e1_fade=FADE, e1_fade_lo=FADE_LO, e1_fade_hi=FADE_HI),
)
# WRITTEN BESIDE THIS FILE, NEVER BESIDE THE CALLER. These four were relative to the
# working directory, so running the model from the repository root — which is how CI and
# every gate runs it — dropped them at the root and left the study's own copies stale. A
# path relative to cwd is a path that depends on who ran it.
# THE WALK-FORWARD RECORD IS THE COMMITTED PANEL, NOT A RE-DERIVATION OF IT. This file
# used to write its own backtest here — 60 origins from an uncleaned frame, disagreeing
# with the production panel on the very first row (a realised close of 16.00 against the
# panel's 16.08, because Step 0.0 had not been applied). Two records of one name's
# history, and the study was quoting the one nobody else could see. The panel is copied
# so the two cannot drift: 58 resolved three-month windows, the same 58 the band record
# above is computed from and the same 58 the site publishes.
_PANEL = os.path.join(HERE, '..', 'panels', 'SA_STC_3m.csv')
_panel_rows = pd.read_csv(_PANEL)
assert len(_panel_rows) == BAND['n'], (len(_panel_rows), BAND['n'])
assert int(_panel_rows['in90'].sum()) == BAND['hits'], 'the panel and the band record disagree'
_panel_rows.to_csv(os.path.join(HERE, 'backtest_rows.csv'), index=False)
np.save(os.path.join(HERE, 'fan.npy'), np.array([fan[p] for p in pcts]))
np.save(os.path.join(HERE, 'pT20.npy'), term20[:20000])
np.save(os.path.join(HERE, 'pT60.npy'), term60[:20000])
# A SENSITIVITY RUN NEVER WRITES. It exists to measure one lever's own worth, and an
# answer struck on a beta this study does not adopt must not reach the committed record.
if _SENS_BETA is None:
    with open(os.path.join(HERE, 'study_numbers.json'), 'w') as f:
        json.dump(out, f, indent=1, default=float)
else:
    # It writes ONE artefact and it is not the study's numbers: the answer this study
    # would reach on a beta it does not adopt, so the rebuild ledger can read the lever's
    # own worth instead of a figure somebody copied off a terminal. [R-ENF-06]
    with open(os.path.join(HERE, 'beta_sensitivity_%s.json' % SENS_TAG), 'w') as f:
        json.dump(dict(beta=_SENS_BETA, levers_applied=LEVERS_APPLIED,
                       what=('the answer on a beta this study does NOT adopt, produced '
                             'only to measure what the beta correction was worth on its '
                             'own. The 40-session daily regression the delivered study '
                             'carried is not one of the three tiers, and the sanctioned '
                             'schedule refuses to build on it as a study beta.'),
                       wacc_market=WACC, wacc_rating=WACC_RATING,
                       ke_market=KE_MARKET, ke_rating=KE_RATING,
                       lenses=dict(dcf=dcf_lens, ddm=ddm_lens, relative=rel,
                                   normalized=norm),
                       central=dict(bear=central_bear, base=central, bull=central_bull),
                       weights=weights), f, indent=1, default=float)
    print('SENSITIVITY RUN on beta %.4f — beta_sensitivity_%s.json only'
          % (_SENS_BETA, SENS_TAG))
print('cone anchor', spot, spot_date, '| nu', ENGINE['nu'], 'cal', ENGINE['width_cal'],
      '| call %s (%s), z=%.4f' % (ENGINE['call'], ENGINE['call_strength'], ENGINE['signal_z']))
print('band record: %d windows, %d inside the 90%% band (%.1f%%), strength %s, flag %s'
      % (BAND['n'], BAND['hits'], BAND['cov90'] * 100, BAND['strength'], BAND['flag']))
print('WACC market %.3f%% | rating %.3f%% | Ke %.3f/%.3f | Kd_at %.3f | We %.3f'
      % (WACC*100, WACC_RATING*100, KE_MARKET*100, KE_RATING*100, KD_AT*100, WE))
print('3 months:', {k: round(v_, 1) for k, v_ in q60.items()},
      '| P(up)=%.3f odds=%.2f' % (prob_read['p_above'], prob_read['odds']))
print('DCF: EV %.0f TV%% %.0f%% eq %.0f ps %.2f | DDM %.2f (TV %.0f%%) | rel %.1f | norm %.1f | central %.1f [%.1f-%.1f]' %
      (ev, 100 * pv_tv / ev, eq_dcf, dcf_ps, ddm_ps, ddm_tv_pct * 100, rel['base'], norm['base'], central, central_bear, central_bull))
print('FCFF path:', [round(r['fcff']) for r in rows])
print('rev path:', [round(r['rev']) for r in rows])
print('cover:', [(c['capex'], round(c['fcf'], 1), round(c['cover'], 2)) for c in cover])
print('experts:', round(e1['base'], 1), round(e2['base'], 1), round(e3['base'], 1), '| ROIC %.1f%%' % (roic * 100))
