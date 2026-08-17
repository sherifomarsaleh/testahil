"""FERTIGLB — forward cone strike via the identical production chain
(Step 0.0 gate -> YZ proxy -> fit_har_v3 -> har_forecast_v3 -> carry_log_h ->
simulate_paths_v3, 50k paths, seed 42, live AE fit). No site write."""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import numpy as np
import pandas as pd
from primitives import load_ohlc, yz_variance_proxy
from data_quality import clean_ohlc
from mc_v3 import fit_har_v3, har_forecast_v3, carry_log_h, signal_alpha, simulate_paths_v3
import market_profiles as MP
import horizons as HZ
import adaptive_width as AW

# FY2025 dividends of $250m ($0.030/share) on 8,249.6m shares; H1 2026 proposed at a
# minimum of $150m (6.73 fils/share) per the Q2 2026 MD&A. Annualised on the AED price.
Q_ANNUAL = 0.0530

prof = MP.PROFILES['AE']
raw = load_ohlc(os.path.join(HERE, '..', 'raw_ohlc', 'AE', 'FERTIGLB.csv'))
df, rep = clean_ohlc(raw, 'FERTIGLB', verbose=False, market='AE')
df = df.reset_index(drop=True)
dates = pd.to_datetime(df['Date'])
close = df['Price'].to_numpy(dtype=float)
i = len(df) - 1
anchor_date = dates.iloc[i]
spot = float(close[i])
v_ = yz_variance_proxy(df)
plan = HZ.cohort_plan('AE', anchor_date)
width_mult = AW.live_width_mult(df, prof)
nu, cal = prof.nu, prof.width_cal

out = dict(anchor_date=str(anchor_date.date()), spot=spot, nu=nu,
           width_cal=cal, width_overlay_mult=float(width_mult),
           rf_live=prof.rf_live, q_annual=Q_ANNUAL, signal_active=prof.signal_active,
           horizons={})
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
    d = dict(h=h, target_date=hz['target_date'], grade_date=hz['grade_date'],
             anchor_vol_ann=float(np.sqrt(dvar * 252)), sigma_h=sigma_h,
             drift_log_h=float(drift),
             pct={f'p{p}': float(np.percentile(term, p)) for p in (5, 25, 50, 75, 95)},
             p_above=float(np.mean(term > spot)))
    for pc in (5, 10, 15, 20):
        d[f'touch_up{pc}'] = float(np.mean(paths.max(axis=1) >= spot * (1 + pc / 100)))
        d[f'touch_dn{pc}'] = float(np.mean(paths.min(axis=1) <= spot * (1 - pc / 100)))
    for pc in (5, 10):
        d[f'end_up{pc}'] = float(np.mean(term >= spot * (1 + pc / 100)))
        d[f'end_dn{pc}'] = float(np.mean(term <= spot * (1 - pc / 100)))
    out['horizons'][short] = d

np.save(os.path.join(HERE, 'paths_1M.npy'), paths_store['1M'][:20000])
np.save(os.path.join(HERE, 'paths_3M.npy'), paths_store['3M'][:20000])
with open(os.path.join(HERE, 'strike_result.json'), 'w') as f:
    json.dump(out, f, indent=1)
print(f"anchor {out['anchor_date']} spot {spot} | nu {nu} cal {cal} overlay {width_mult} "
      f"| signal_active {prof.signal_active} | rf_live {prof.rf_live} q {Q_ANNUAL}")
for short, hzd in out['horizons'].items():
    print(short, hzd['h'], 'sessions to', hzd['grade_date'],
          '| ann vol', round(hzd['anchor_vol_ann'], 3),
          '| pct', {k: round(v, 3) for k, v in hzd['pct'].items()},
          '| P(above)', round(hzd['p_above'], 3))
