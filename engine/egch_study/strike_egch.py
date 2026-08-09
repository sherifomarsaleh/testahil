"""EGCH — forward price map via the identical production chain
(Step 0.0 gate -> YZ proxy -> fit_har_v3 -> har_forecast_v3 -> carry_log_h ->
simulate_paths_v3, 50k paths, seed 42, live EG fit), local CSV, no site write.

q_annual = 0: SOURCED, not assumed. The proposed appropriation statements in both the
FY2023/24 and FY2024/25 audited accounts distribute nothing — the whole distributable
profit is retained after the legal reserve. A price forecast must not carry a dividend
drift the shares do not pay.
"""
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

sys.path.insert(0, HERE)
from inputs import V

Q_ANNUAL = 0.0

prof = MP.PROFILES['EG']
raw = load_ohlc(os.path.join(HERE, 'EGCH_Stock_Price_History.csv'))
df, rep = clean_ohlc(raw, 'EGCH', verbose=False, market='EG')
df = df.reset_index(drop=True)
dates = pd.to_datetime(df['Date'])
close = df['Price'].to_numpy(dtype=float)
i = len(df) - 1
anchor_date = dates.iloc[i]
spot = float(close[i])
v_ = yz_variance_proxy(df)
plan = HZ.cohort_plan('EG', anchor_date)
width_mult = AW.live_width_mult(df, prof)
nu, cal = prof.nu, prof.width_cal

out = dict(anchor_date=str(anchor_date.date()), spot=spot, nu=nu,
           width_cal=cal, width_overlay_mult=float(width_mult),
           rf_live=prof.rf_live, q_annual=Q_ANNUAL,
           q_source=("Proposed appropriation statements, audited FY2023/24 and FY2024/25 — "
                     "nothing distributed in either year"),
           signal_active=prof.signal_active, horizons={})
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
    # level-touch ladder at the SAME absolute relative levels the house uses
    ladder = {}
    for pct in (5, 10, 15, 20):
        ladder[f'touch_up{pct}'] = float(np.mean(paths.max(axis=1) >= spot * (1 + pct / 100)))
        ladder[f'touch_dn{pct}'] = float(np.mean(paths.min(axis=1) <= spot * (1 - pct / 100)))
    for pct in (5, 10):
        ladder[f'end_up{pct}'] = float(np.mean(term >= spot * (1 + pct / 100)))
        ladder[f'end_dn{pct}'] = float(np.mean(term <= spot * (1 - pct / 100)))
    out['horizons'][short] = dict(
        h=h, target_date=hz['target_date'], grade_date=hz['grade_date'],
        anchor_vol_ann=float(np.sqrt(dvar * 252)), sigma_h=sigma_h,
        drift_log_h=float(drift),
        pct={f'p{p}': round(float(np.percentile(term, p)), 2) for p in (5, 25, 50, 75, 95)},
        p_above=float(np.mean(term > spot)),
        ladder=ladder)

np.save(os.path.join(HERE, 'paths_1M.npy'), paths_store['1M'][:20000])
np.save(os.path.join(HERE, 'paths_3M.npy'), paths_store['3M'][:20000])
json.dump(out, open(os.path.join(HERE, 'strike_result.json'), 'w'), indent=1)
for short, hzd in out['horizons'].items():
    print(short, hzd['h'], 'sessions to', hzd['grade_date'],
          '| annualised vol', round(hzd['anchor_vol_ann'], 3),
          '| percentiles', hzd['pct'],
          '| P(above spot)', round(hzd['p_above'], 3))
