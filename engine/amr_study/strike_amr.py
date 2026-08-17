"""AMR — forward cone strike via the identical production chain
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

Q_ANNUAL = (0.024 * 3.6725) / 2.23   # The board declared USD 201.6 million against FY2025,
                                     # USD 0.024 a share, and has already declared USD 0.012 as
                                     # an interim against 2026. At the 3.6725 peg that is AED
                                     # 0.0881 against a close of AED 2.23, a yield of 3.95%. The
                                     # carry anchor is ln(1+rf) - ln(1+q): this is a PRICE
                                     # forecast, and the shares do not earn the dividend they pay
                                     # away.

prof = MP.PROFILES['AE']
raw = load_ohlc(os.path.join(HERE, 'AMR_Stock_Price_History.csv'))
df, rep = clean_ohlc(raw, 'AMR', verbose=False, market='AE')
df = df.reset_index(drop=True)
dates = pd.to_datetime(df['Date'])
close = df['Price'].to_numpy(dtype=float)
i = len(df) - 1
anchor_date = dates.iloc[i]
spot = float(close[i])
v_ = __import__('primitives').yz_variance_proxy(df)
plan = HZ.cohort_plan('AE', anchor_date)
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
