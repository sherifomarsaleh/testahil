"""compute_xpt.py — all numbers for the XPT/USD (platinum) full study.
Production chain only: repo engine code, XPT provisional self-fit (Gaussian sentinel
250, width_cal=0.853), carry ln(1+rf)·h/252 with rf=0.0363 (METALS anchor), q=0,
signal off, 50k paths, seed 42. Outputs study_numbers_xpt.json.
"""
import sys, os, json
sys.path.insert(0, os.path.abspath('repo/engine'))
import numpy as np, pandas as pd
from market_profiles import MarketProfile, FED_SCHEDULE
from mc_v2 import load_ohlc as raw_load, yz_variance_proxy
from mc_v3 import fit_har_v3, har_forecast_v3, carry_log_h, simulate_paths_v3

R2 = lambda x: float(np.round(x, 2))
R4 = lambda x: float(np.round(x, 4))

XPT = MarketProfile("XPT", "Platinum (USD)", FED_SCHEDULE, 0.0363,
    "USD cost-of-carry anchor (Fed funds midpoint schedule), q=0.",
    None, +1, 0.0, False, nu=250.0, width_cal=0.853, breaks=[])
NU, CAL = 250.0, 0.853          # adopted PROVISIONAL self-fit (flagged circular)
NU_L, CAL_L = 20.0, 1.035       # LONO gold+silver fit (dual-framing sensitivity)
SEED, NPATHS = 42, 50000

df = pd.read_csv('XPT_clean_staged.csv', parse_dates=['Date'])
close = df['Price'].values; dates = pd.DatetimeIndex(df['Date'])
spot = float(close[-1]); spot_date = str(dates[-1].date())
assert abs(spot - 1608.37) < 0.01, spot

out = {'meta': dict(ticker='XPTUSD', name='Platinum', ccy='USD', unit='USD/oz',
                    spot=spot, spot_date=spot_date, rows=len(df),
                    first=str(dates[0].date()), last=spot_date,
                    engine='mc_v3 carry-anchored YZ-HAR-t', nu='Gaussian (sentinel 250.0)',
                    width_cal=CAL, rf_live=0.0363, q_annual=0.0, seed=SEED, n_paths=NPATHS)}

# ---------------------------------------------------------------- price stats
lr = np.diff(np.log(close))
def ret(nd):
    return R4(close[-1] / close[-1 - nd] - 1) if len(close) > nd else None
i2026 = dates.get_indexer([pd.Timestamp('2025-12-31')], method='ffill')[0]
ath_i = int(np.argmax(close))
out['price'] = dict(
    r1m=ret(21), r3m=ret(63), r6m=ret(126), r12m=ret(252),
    ytd=R4(close[-1] / close[i2026] - 1),
    from_2024_end=R4(close[-1] / close[dates.get_indexer([pd.Timestamp('2024-12-31')], method='ffill')[0]] - 1),
    hi52=R2(close[-252:].max()), lo52=R2(close[-252:].min()),
    hi52_date=str(dates[-252:][np.argmax(close[-252:])].date()),
    lo52_date=str(dates[-252:][np.argmin(close[-252:])].date()),
    ath_close=R2(close[ath_i]), ath_date=str(dates[ath_i].date()),
    off_ath=R4(close[-1] / close[ath_i] - 1),
    vol30=R4(np.std(lr[-30:], ddof=1) * np.sqrt(252)),
    vol90=R4(np.std(lr[-90:], ddof=1) * np.sqrt(252)),
    vol252=R4(np.std(lr[-252:], ddof=1) * np.sqrt(252)),
    worst_day=dict(date=str(dates[1:][np.argmin(lr)].date()), r=R4(np.exp(lr.min()) - 1)),
    best_day=dict(date=str(dates[1:][np.argmax(lr)].date()), r=R4(np.exp(lr.max()) - 1)),
    avg_true_range_pct_30d=R4(np.mean((df['High'].values[-30:] - df['Low'].values[-30:]) / close[-30:])),
)
# 2025 path landmarks
y25 = (dates.year == 2025); y26 = (dates.year == 2026)
out['path'] = dict(end2024=R2(close[dates.get_indexer([pd.Timestamp('2024-12-31')], method='ffill')[0]]),
                   hi2025=R2(close[y25].max()), hi2025_date=str(dates[y25][np.argmax(close[y25])].date()),
                   hi2026=R2(close[y26].max()), hi2026_date=str(dates[y26][np.argmax(close[y26])].date()),
                   lo2026=R2(close[y26].min()), lo2026_date=str(dates[y26][np.argmin(close[y26])].date()),
                   ret2025=R4(close[y25][-1] / close[dates.get_indexer([pd.Timestamp('2024-12-31')], method='ffill')[0]] - 1))

# ---------------------------------------------------------------- technicals
s = pd.Series(close)
sma20, sma50, sma200 = [float(s.rolling(w).mean().iloc[-1]) for w in (20, 50, 200)]
d = s.diff(); up = d.clip(lower=0).rolling(14).mean(); dn = (-d.clip(upper=0)).rolling(14).mean()
rsi = float((100 - 100 / (1 + up / dn)).iloc[-1])
e12, e26 = s.ewm(span=12, adjust=False).mean(), s.ewm(span=26, adjust=False).mean()
macd = e12 - e26; sig = macd.ewm(span=9, adjust=False).mean()
hist = macd - sig
out['tech'] = dict(sma20=R2(sma20), sma50=R2(sma50), sma200=R2(sma200),
    vs20=R4(spot / sma20 - 1), vs50=R4(spot / sma50 - 1), vs200=R4(spot / sma200 - 1),
    rsi14=R2(rsi), macd=R2(float(macd.iloc[-1])), macd_sig=R2(float(sig.iloc[-1])),
    macd_hist=R2(float(hist.iloc[-1])), macd_hist_prev5=[R2(float(h)) for h in hist.iloc[-5:]],
    cross='golden' if sma50 > sma200 else 'death',
    sup=[R2(x) for x in (1539.60, 1500.0, 1348.20)],
    res=[R2(x) for x in (sma50, 1750.0, 1990.50)],
    notes="sup: 01-Jul-2026 swing low; round 1,500; Feb-2021 breakout shelf 1,348.20. "
          "res: 50-day average; 1,750 June shelf; May-2026 recovery high 1,990.50.")

# ---------------------------------------------------------------- Pt/Au ratio lens
g = raw_load('repo/engine/raw_ohlc/XAU/GOLD.csv')
gm = pd.Series(g['Price'].values, index=pd.DatetimeIndex(g['Date']))
xm = pd.Series(close, index=dates)
al = pd.concat([xm.rename('pt'), gm.rename('au')], axis=1).dropna()
ratio = al['pt'] / al['au']
GOLD_SPOT, GOLD_DATE = 3972.0, '2026-07-17'      # Fortune/spot, 17-Jul-2026
PD_SPOT, PD_DATE = 1239.0, '2026-07-17'
r_now = spot / GOLD_SPOT
win = lambda y: ratio[ratio.index >= ratio.index[-1] - pd.DateOffset(years=y)]
out['ratio'] = dict(now=R4(r_now), gold_spot=GOLD_SPOT, gold_date=GOLD_DATE,
    pd_spot=PD_SPOT, pt_pd=R4(spot / PD_SPOT),
    mean_full=R4(ratio.mean()), mean_10y=R4(win(10).mean()),
    mean_5y=R4(win(5).mean()), mean_2y=R4(win(2).mean()),
    mean_post2016=R4(ratio[ratio.index >= '2016-01-01'].mean()),
    min_full=R4(ratio.min()), min_date=str(ratio.idxmin().date()),
    max_full=R4(ratio.max()), max_date=str(ratio.idxmax().date()),
    pctile_now_post2016=R4((ratio[ratio.index >= '2016-01-01'] <= r_now).mean()),
    ratio_end=str(al.index[-1].date()))
# fair-value grid: Pt = gold × ratio
gold_sc = [3600, 3972, 4400, 4800]
ratio_sc = [0.32, 0.36, 0.405, 0.45, 0.50]
out['ratio_grid'] = dict(gold=gold_sc, ratio=ratio_sc,
    fv=[[R2(gsc * rsc) for gsc in gold_sc] for rsc in ratio_sc])

# ---------------------------------------------------------------- fair-value anchors & zone
anchors = dict(
    ratio=dict(bear=R2(0.36 * 3600), base=R2(out['ratio']['mean_5y'] * GOLD_SPOT), bull=R2(0.45 * 4400),
               note='post-2016-regime Pt/Au band × gold scenarios; base = 5y-mean ratio × spot gold'),
    consensus=dict(bear=1500.0, base=1750.0, bull=2222.0,
               note='UBS 29-Jun-2026 $1,700 (Sep/Dec-26) & $1,800 (Mar/Jun-27) — set BELOW-crash-aware; '
                    'LBMA Jan-2026 survey avg $2,222 — set at the peak, stale-high; bear = UBS surplus scenario'),
    balance=dict(bear=1350.0, base=1500.0, bull=1990.0,
               note='4th consecutive deficit (297 koz 2026f), AGS 1,747 koz ≈ 11 weeks — structural floor '
                    'band over the 1,348 breakout shelf; bull = tightness re-squeeze toward the May-2026 1,990 high'),
    cost=dict(bear=1006.0, base=1300.0, bull=2400.0,
               note='S&P AISC 2026f $1,006 (+7.7%) = deep-bear bound; base = AISC + normal margin; '
                    'bull = Valterra long-term incentive planning range $2,300–2,500 midpoint'),
    carry=dict(bear=None, base=None, bull=None,
               note='real 10Y ~1.9–2.0%, hawkish near-term = cap; 2027 easing = the re-rating option — a tilt, not a level'),
)
w = dict(ratio=0.30, consensus=0.30, balance=0.20, cost=0.20)   # judgment — Driver Ledger row
zc = sum(w[k] * anchors[k]['base'] for k in w)
zl = sum(w[k] * anchors[k]['bear'] for k in w)
zh = sum(w[k] * anchors[k]['bull'] for k in w)
out['anchors'] = anchors
out['zone'] = dict(lo=R2(zl), centre=R2(zc), hi=R2(zh), weights=w,
                   spot_vs_centre=R4(spot / zc - 1))

# ---------------------------------------------------------------- MC v3 (production chain)
v = yz_variance_proxy(df)
n = len(df); origin = n - 1
res_mc = {}
for h in (20, 21, 60, 63, 252):
    beta, s2 = fit_har_v3(v, origin, horizon=h)
    dv = har_forecast_v3(v, origin, beta, s2, horizon=h)
    drift = carry_log_h(XPT, dates[-1], 0.0, h)
    paths = simulate_paths_v3(spot, dv, h, drift, nu=NU, n_paths=NPATHS, seed=SEED, width_cal=CAL)
    term = paths[:, -1]
    q = np.percentile(term, [5, 25, 50, 75, 95])
    ann_vol = float(np.sqrt(dv * 252)) * CAL
    zones = dict(
        below_m20=float((term < spot * 0.80).mean()), m10_m20=float(((term >= spot * .80) & (term < spot * .90)).mean()),
        m5_m10=float(((term >= spot * .90) & (term < spot * .95)).mean()), pm5=float(((term >= spot * .95) & (term <= spot * 1.05)).mean()),
        p5_p10=float(((term > spot * 1.05) & (term <= spot * 1.10)).mean()), p10_p20=float(((term > spot * 1.10) & (term <= spot * 1.20)).mean()),
        above_p20=float((term > spot * 1.20).mean()))
    rmax, rmin = paths.max(axis=1), paths.min(axis=1)
    touch_rel = {f"+{p}%": float((rmax >= spot * (1 + p / 100)).mean()) for p in (5, 10, 15, 20)}
    touch_rel.update({f"-{p}%": float((rmin <= spot * (1 - p / 100)).mean()) for p in (5, 10, 15, 20)})
    lv_up = [1700, 1750, 1990.5, 2222, 2400, 2925]
    lv_dn = [1539.6, 1500, 1348.2, 1200, 1006]
    touch_abs = {str(l): float((rmax >= l).mean()) for l in lv_up}
    touch_abs.update({str(l): float((rmin <= l).mean()) for l in lv_dn})
    res_mc[f"t{h}"] = dict(p5=R2(q[0]), p25=R2(q[1]), p50=R2(q[2]), p75=R2(q[3]), p95=R2(q[4]),
        mean=R2(term.mean()), p_below_spot=R4((term < spot).mean()),
        ann_fwd_vol=R4(ann_vol), sigma_h=R4(np.sqrt(dv * h) * CAL), drift_log=R4(drift),
        zones={k: R4(vv) for k, vv in zones.items()},
        touch_rel={k: R4(vv) for k, vv in touch_rel.items()},
        touch_abs={k: R4(vv) for k, vv in touch_abs.items()},
        w90_pct_spot=R4((q[4] - q[0]) / spot))
    if h == 63:   # dual-framing: LONO config cone at the study's central horizon
        p2 = simulate_paths_v3(spot, dv, h, drift, nu=NU_L, n_paths=NPATHS, seed=SEED, width_cal=CAL_L)
        q2 = np.percentile(p2[:, -1], [5, 25, 50, 75, 95])
        res_mc['t63_lono'] = dict(p5=R2(q2[0]), p25=R2(q2[1]), p50=R2(q2[2]), p75=R2(q2[3]), p95=R2(q2[4]),
                                  note='same HAR width, LONO gold+silver shape (nu=20, cal=1.035)')
out['mc'] = res_mc

# trailing benchmark vol for the "mean-reverting from" phrase
out['mc']['trailing_vol_252'] = out['price']['vol252']
out['mc']['trailing_vol_90'] = out['price']['vol90']

# ---------------------------------------------------------------- ledger cohorts (T+20/T+60, Mon–Fri weekmask)
def busadd(d0, nbd):
    return str(np.busday_offset(np.datetime64(d0, 'D'), nbd, roll='forward', weekmask='1111100'))
coh = []
for h, lab in ((20, '1 month (T+20)'), (60, '3 months (T+60)')):
    m = res_mc[f"t{h}"]
    coh.append(dict(instrument='XPTUSD', asset_class='metal', anchor_date=spot_date,
        anchor_price=spot, ccy='USD', horizon_label=lab, horizon_days=h,
        grade_date=busadd(spot_date, h), cycle_no=1,
        p5=m['p5'], p25=m['p25'], p50=m['p50'], p75=m['p75'], p95=m['p95'],
        touch={k: m['touch_rel'][k] for k in ('+5%', '+10%', '-5%', '-10%')},
        anchor_vol=m['ann_fwd_vol'],
        engine='mc_v3 carry-anchored YZ-HAR-t, nu=Gaussian, width_cal=0.853 (provisional self-fit), seed 42, 50k'))
out['cohorts'] = coh
out['t252_resolve'] = busadd(spot_date, 252)

json.dump(out, open('study_numbers_xpt.json', 'w'), indent=1)
print(json.dumps(out['price'], indent=1))
print(json.dumps(out['path'], indent=1))
print(json.dumps(out['tech'], indent=1))
print(json.dumps(out['ratio'], indent=1))
print(json.dumps(out['zone'], indent=1))
for k in ('t20', 't60', 't63', 't252', 't63_lono'):
    print(k, json.dumps(out['mc'][k] if k != 't63_lono' else out['mc'][k]))
print('cohorts:', json.dumps(coh, indent=1))
