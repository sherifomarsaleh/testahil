"""SWDY — forward cone strike via the identical production chain
(Step 0.0 gate -> YZ proxy -> fit_har_v3 -> har_forecast_v3 -> carry_log_h ->
simulate_paths_v3, 50k paths, seed 42, live EG fit), local CSV, no site write."""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import numpy as np
import pandas as pd
from primitives import load_ohlc
from data_quality import clean_ohlc
from mc_v3 import fit_har_v3, har_forecast_v3, carry_log_h, signal_alpha, simulate_paths_v3
import market_profiles as MP
import horizons as HZ
import adaptive_width as AW

Q_ANNUAL = 0.0095   # FY24 DPS EGP 1.00 paid 2025; none declared on FY25 profits per available record

prof = MP.PROFILES['EG']
# THE REPOSITORY'S OWN LIBRARY, NOT THE STUDY-LOCAL FILE.
#
# SWDY_Stock_Price_History.csv ends 5 August 2026 at 105.20, and this study's own
# compute.py records why that file cannot be trusted: the supplied figure "first arrived
# as 90.50 and was CORRECTED to 130.00 on 6 September 2026 after it disagreed with this
# name's own price library on all 35 overlapping sessions after 14 June 2026, including
# the 5 August close of 105.20". The study acted on that finding for its SPOT and left
# the strike reading the same discredited file.
#
# WHAT IT COST, and it is six findings with one cause. The whole price map was struck on
# the 5-August anchor: section 2's moving-average stack, section 3's cone, the percentile
# table, the one-month band whose check date of 6 September had already passed, and a
# "probability above spot" of 56% and 61% which is the probability above 105.20 — against
# the 130.00 the study publishes it is 5.7% and 18.1%. Figure 5 drew a cone opening at
# 105.20 under a line labelled "spot 130.00".
#
# The library is the source every other name in this book strikes on, and it carries the
# study's own valuation date. NOTHING HERE TOUCHES THE FAIR VALUE: the cone, the technical read and
# the percentile map are the price lens, and [R-LENS-01] keeps them out of the
# fundamentals entirely.
raw = load_ohlc(os.path.join(HERE, '..', 'raw_ohlc', 'EG', 'SWDY.csv'))
df, rep = clean_ohlc(raw, 'SWDY', verbose=False, market='EG')
df = df.reset_index(drop=True)
dates = pd.to_datetime(df['Date'])
close = df['Price'].to_numpy(dtype=float)

# ONE DOCUMENT, ONE DATE. The cone is anchored at the study's OWN valuation date, read
# from study_numbers.json, not at whatever row the library happens to end on. The fair
# value is measured against the price of 3 September 2026; a cone struck three sessions
# later describes a different price, and the reader has no way to see that from the page.
# The library's close on that date must BE the spot the study publishes, or this stops:
# a cone that opens somewhere other than the study's own spot is the defect this file
# was just repaired for, arriving from the other side.
with open(os.path.join(HERE, 'study_numbers.json')) as _f:
    _meta = json.load(_f)['meta']
asof = pd.Timestamp(_meta['asof'])
_hit = dates.index[dates == asof]
if len(_hit) != 1:
    raise SystemExit('the price library carries no single row for the study\'s valuation '
                     'date %s; the cone cannot be anchored where the value is measured'
                     % _meta['asof'])
i = int(_hit[0])
anchor_date = dates.iloc[i]
spot = float(close[i])
if abs(spot - float(_meta['spot'])) > 0.005:
    raise SystemExit('the library closes at %.4f on %s and the study publishes a spot of '
                     '%.4f; one of the two is wrong and neither may be assumed'
                     % (spot, _meta['asof'], float(_meta['spot'])))
v_ = __import__('primitives').yz_variance_proxy(df)
plan = HZ.cohort_plan('EG', anchor_date)
width_mult = AW.live_width_mult(df, prof)
nu, cal = prof.nu, prof.width_cal

out = dict(anchor_date=str(anchor_date.date()), spot=spot, nu=nu,
           width_cal=cal, width_overlay_mult=float(width_mult),
           rf_live=prof.rf_live, q_annual=Q_ANNUAL, horizons={})
paths_store = {}
for short, hz in plan['horizons'].items():
    h = int(hz['horizon_days'])
    months = 1 if short == '1M' else 3
    beta, s2 = fit_har_v3(v_, i, horizon=h)
    dvar = har_forecast_v3(v_, i, beta, s2, horizon=h)
    cal_eff = cal * width_mult
    sigma_h = float(np.sqrt(dvar * h) * cal_eff)
    drift = carry_log_h(prof, anchor_date, Q_ANNUAL, h, yearfrac=months / 12.0)
    alpha, z = signal_alpha(prof, close, i, sigma_h)
    paths = simulate_paths_v3(spot, dvar, h, drift + alpha, nu=nu,
                              n_paths=50000, seed=42, width_cal=cal_eff)
    term = paths[:, -1]
    paths_store[short] = paths
    out['horizons'][short] = dict(
        h=h, target_date=hz['target_date'], grade_date=hz['grade_date'],
        anchor_vol_ann=float(np.sqrt(dvar * 252)), sigma_h=sigma_h,
        drift_log_h=float(drift),
        pct={f'p{p}': float(np.percentile(term, p)) for p in (5, 25, 50, 75, 95)},
        p_above=float(np.mean(term > spot)),
        p_up10=float(np.mean(term >= spot * 1.10)),
        p_dn10=float(np.mean(term <= spot * 0.90)),
        touch_up10=float(np.mean(paths.max(axis=1) >= spot * 1.10)),
        touch_dn10=float(np.mean(paths.min(axis=1) <= spot * 0.90)),
    )

np.save(os.path.join(HERE, 'paths_1M.npy'), paths_store['1M'][:20000])
np.save(os.path.join(HERE, 'paths_3M.npy'), paths_store['3M'][:20000])
with open(os.path.join(HERE, 'strike_result.json'), 'w') as f:
    json.dump(out, f, indent=1)
for short, hzd in out['horizons'].items():
    print(short, hzd['h'], 'sess to', hzd['grade_date'],
          '| vol', round(hzd['anchor_vol_ann'], 3),
          '| pct', {k: round(v, 3) for k, v in hzd['pct'].items()},
          '| P(above)', round(hzd['p_above'], 2))
