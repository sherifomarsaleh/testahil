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
import primitives as m
from wacc_builder import WaccInputs, build_wacc, RegressionBetaAttempt

# Imported here rather than beside the cost-of-capital block because the LATEST KNOWN
# price it reads is needed by the market capitalisation long before the schedule is built.
import coc_run as COCRUN

HERE = os.path.dirname(os.path.abspath(__file__))
OHLC = os.path.join(HERE, '..', 'raw_ohlc', 'SA', 'STC.csv')

df = m.load_ohlc(OHLC)
close = df['Price'].values
spot = float(close[-1])
spot_date = str(df['Date'].iloc[-1].date())
N = len(df)

# ---------------- Step 0 backtest (zero drift = house default for non-EGX) ---
res, summ = m.backtest(df, horizon=60, secular_drift=False)          # adopted config
res_sec, summ_sec = m.backtest(df, horizon=60, secular_drift=True)   # rejected diagnostic
res21, summ21 = m.backtest(df, horizon=60, step=21, secular_drift=False)
pit_hist = np.histogram(res['pit'], bins=10, range=(0, 1))[0].tolist()
# block bootstrap CI on CRPS skill (n windows, resample with replacement)
rng_bs = np.random.default_rng(7)
sk = []
c, cb = res['crps'].values, res['crps_bench'].values
for _ in range(4000):
    idx = rng_bs.integers(0, len(c), len(c))
    sk.append(1 - c[idx].sum() / cb[idx].sum())
sk = np.array(sk)
boot = dict(lo90=float(np.percentile(sk, 5)), hi90=float(np.percentile(sk, 95)),
            p_pos=float(np.mean(sk > 0)))

# ---------------- Forward run parameters ------------------------------------
v = m.yz_variance_proxy(df)
beta_har = m.fit_har(v, N - 1, horizon=60)
dv = m.har_forecast_daily_var(v, N - 1, beta_har, horizon=60)
anchor_vol = float(np.sqrt(dv * 252))
drift_daily = 0.0   # zero-drift class: international/GCC name (Step 0-adopted)

# ---------------- 16-factor stack (7 continuous + 9 discrete) ---------------
continuous = [
    ("SAMA/Fed policy-rate path (easing)", "+"),
    ("Oil price / fiscal impulse (govt ICT & mega-project spend)", "+"),
    ("Vision 2030 / non-oil GDP digital demand", "+"),
    ("KSA mobile competition (Mobily/Zain share & price pressure)", "−"),
    ("Data-centre / AI buildout economics (center3–HUMAIN)", "±"),
    ("Subsidiary drag→contribution (stc bank, solutions, intl)", "±"),
    ("TASI flows / index weight (free float 38%)", "±"),
]
cont_drift_q = 0.002
discrete = [
    ("2Q26 results (~late Jul 2026)",                  0.90, 0.004),
    ("Special dividend announced with 2Q/3Q results",  0.20, 0.020),
    ("SAMA/Fed cut ≥25bp (Sep/Oct)",                   0.55, 0.006),
    ("center3/HUMAIN AI-DC milestone (toward 1GW)",    0.35, 0.010),
    ("TAWAL/DIIC monetization event",                  0.10, 0.015),
    ("Telefónica mark deterioration spillover",        0.25, -0.006),
    ("KSA mobile price-war escalation / weak prints",  0.20, -0.015),
    ("Regional geopolitical escalation",               0.25, -0.020),
    ("PIF further sell-down / index-flow event",       0.10, -0.012),
]
disc_drift_q = sum(p * i for _, p, i in discrete)
factor_drift_q = cont_drift_q + disc_drift_q

# ---------------- Forward simulation (50,000 paths, seed 42) ----------------
H = 60
rng = np.random.default_rng(42)
n_paths = 50000
sd = np.sqrt(dv)
z = rng.standard_normal((n_paths, H))
chi = rng.chisquare(5, n_paths)
mix = np.sqrt(3.0 / chi)[:, None]
incr = drift_daily + cont_drift_q / H + z * mix * sd
for name, p, imp in discrete:
    fire = rng.random(n_paths) < p
    day = rng.integers(0, H, n_paths)
    size = rng.normal(imp, abs(imp) / 2, n_paths)
    add = np.zeros((n_paths, H))
    add[np.arange(n_paths)[fire], day[fire]] = size[fire]
    incr += add
logp = np.cumsum(incr, axis=1)
paths = np.empty((n_paths, H + 1))
paths[:, 0] = spot
paths[:, 1:] = spot * np.exp(logp)

pT20, pT60 = paths[:, 20], paths[:, 60]
pcts = [5, 25, 50, 75, 95]
q20 = {p: float(np.percentile(pT20, p)) for p in pcts}
q60 = {p: float(np.percentile(pT60, p)) for p in pcts}
run_max = paths.max(axis=1); run_min = paths.min(axis=1)
run_max20 = paths[:, :21].max(axis=1); run_min20 = paths[:, :21].min(axis=1)
levels = [50, 48, 46, 44, 42, 40, 38, 36]
touch = {L: dict(t20=float(np.mean(run_max20 >= L) if L > spot else np.mean(run_min20 <= L)),
                 t60=float(np.mean(run_max >= L) if L > spot else np.mean(run_min <= L)))
         for L in levels}
prob_read = dict(
    p_above=float(np.mean(pT60 > spot)),
    p_up10=float(np.mean(pT60 >= spot * 1.10)),
    p_dn10=float(np.mean(pT60 <= spot * 0.90)),
    median=float(np.median(pT60)),
    med_move=float(np.median(pT60) / spot - 1),
    band50=(q60[25], q60[75]),
    band50_pct=((q60[25] / spot - 1), (q60[75] / spot - 1)),
    touch_up10=float(np.mean(run_max >= spot * 1.10)),
    touch_dn10=float(np.mean(run_min <= spot * 0.90)),
)
prob_read['odds'] = prob_read['p_up10'] / prob_read['p_dn10']
zones_edges = [0, 38, 42, 46, 50, 1e9]
zone_probs = [float(np.mean((pT60 >= a) & (pT60 < b))) for a, b in zip(zones_edges[:-1], zones_edges[1:])]
fan = {p: np.percentile(paths, p, axis=0).tolist() for p in pcts}

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
TAX = 0.097          # normalized effective zakat+tax (FY23 9.5%, FY24 9.8%; FY25 −3.2% one-off credit)
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
wc_out_pct = [0.008, 0.006, 0.005, 0.004, 0.004]
payout_dps = [2.20, 2.20, 2.30, 2.40, 2.55]       # policy 0.55/q locked to Q3-27

# THE TWO RATES ARE ANCHORED ON THE SAME REVIEWED HALF AND THEN HELD FLAT. The rule says
# to hold everything else flat INCLUDING observed improvements, so the first year takes the
# reviewed period's own gross margin and operating-cost share (each corrected by the prior
# year's measured half-to-year factor) and no year after it assumes any further gain.
_margin_shift = FY26_GROSS_MARGIN - (sum(seg_fc[yrs[0]][k] * SEG_MARGIN[k]
                                         for k in seg_fc[yrs[0]])
                                     + fc[yrs[0]]['gross'] * ELIM_GP_SHARE) / fc[yrs[0]]['rev']
for i, y in enumerate(yrs):
    _gp = sum(seg_fc[y][k] * SEG_MARGIN[k] for k in seg_fc[y]) \
        + fc[y]['gross'] * ELIM_GP_SHARE
    _gp += fc[y]['rev'] * _margin_shift
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
net_debt = (BR_BORROWINGS + BR_LEASES - BR_CASH_NON_BANK - BR_MURABAHAS
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
norm_pat = 14400.0
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
ic = 90500.0   # invested capital ≈ equity att 83.4bn + net debt 7.1bn (FY25/Q1-26)
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
e1 = dict(base=e1_ps, rng=(e1_ps_at(0.040, WACC + 0.005), e1_ps_at(0.010, WACC - 0.005)))
# Expert 2 — Karim (normalized earnings power)
e2 = dict(base=norm['base'], rng=(norm['bear'], norm['bull']))
# Expert 3 — Omar (macro-policy scenario tree on the DDM/rate path)
scen = [(0.30, ddm_lens['bull'] * 1.02), (0.45, ddm_ps), (0.25, ddm_lens['bear'] * 0.96)]
e3 = dict(base=sum(p * v_ for p, v_ in scen))

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
    step0=dict(nonoverlap=summ, monthly=summ21, secular=summ_sec,
               pit_hist=pit_hist, n_rows=len(res), boot=boot),
    engine=dict(anchor_vol=anchor_vol, drift_daily=drift_daily,
                drift_q=drift_daily * 60, factor_drift_q=factor_drift_q,
                cont_drift_q=cont_drift_q, disc_drift_q=disc_drift_q),
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
                            cash_non_bank=BR_CASH_NON_BANK, murabahas=BR_MURABAHAS,
                            sukuk=BR_SUKUK, treasury_bills=BR_TBILLS, net=net_debt),
    ),
    terminal_record=_t.record,
    hist=hist, seg_hist=seg_hist,
    drivers=dict(
        # Per-segment REAL growth, measured from the company's own note 9 and deflated by
        # a published price index, fading to zero real by the last explicit year. Nominal
        # recomputes on the house ladder; nothing here is a typed nominal rate.
        segment_real_growth={k: round(v, 6) for k, v in seg_real0.items()},
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
              margin_steps=margin_steps, capex_steps=capex_steps, table_cm=sens_cm),
    cover=cover, div_bill=div_bill,
    experts=dict(e1=e1, e2=e2, e3=e3, e1_roic=roic, e1_ic=ic, e1_ep=ep),
)
res.to_csv('backtest_rows.csv', index=False)
np.save('fan.npy', np.array([fan[p] for p in pcts]))
np.save('pT20.npy', pT20[:20000]); np.save('pT60.npy', pT60[:20000])
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
print('spot', spot, spot_date, '| anchor_vol', round(anchor_vol, 4), '| factor_q', round(factor_drift_q * 100, 2), '%')
print('Step0 zero-drift non-overlap:', {k: round(v_, 4) if isinstance(v_, float) else v_ for k, v_ in summ.items()})
print('boot:', boot)
print('WACC market %.3f%% | rating %.3f%% | Ke %.3f/%.3f | Kd_at %.3f | We %.3f'
      % (WACC*100, WACC_RATING*100, KE_MARKET*100, KE_RATING*100, KD_AT*100, WE))
print('T60:', {k: round(v_, 1) for k, v_ in q60.items()}, '| P(up)=%.3f odds=%.2f' % (prob_read['p_above'], prob_read['odds']))
print('DCF: EV %.0f TV%% %.0f%% eq %.0f ps %.2f | DDM %.2f (TV %.0f%%) | rel %.1f | norm %.1f | central %.1f [%.1f-%.1f]' %
      (ev, 100 * pv_tv / ev, eq_dcf, dcf_ps, ddm_ps, ddm_tv_pct * 100, rel['base'], norm['base'], central, central_bear, central_bull))
print('FCFF path:', [round(r['fcff']) for r in rows])
print('rev path:', [round(r['rev']) for r in rows])
print('cover:', [(c['capex'], round(c['fcf'], 1), round(c['cover'], 2)) for c in cover])
print('experts:', round(e1['base'], 1), round(e2['base'], 1), round(e3['base'], 1), '| ROIC %.1f%%' % (roic * 100))
