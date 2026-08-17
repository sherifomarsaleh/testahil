"""BOROUGE — forward cone strike via the identical production chain
(Step 0.0 gate -> YZ proxy -> fit_har_v3 -> har_forecast_v3 -> carry_log_h ->
simulate_paths_v3, 50k paths, seed 42, live AE fit), local CSV, no site write.

The dividend yield is SOURCED, not defaulted: Borouge plc's H1-2026 earnings release
restates an annual dividend intention of 16.2 fils per share, which on the 7 August
2026 close of AED 2.40 is 6.75%. That carry matters — at a 3.65% risk-free rate the
dividend exceeds it, so the carry-anchored drift is NEGATIVE and the benchmark the
cone is scored against knows it.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import numpy as np                                          # noqa: E402
import pandas as pd                                         # noqa: E402
import adaptive_width as AW                                  # noqa: E402
import horizons as HZ                                        # noqa: E402
import market_profiles as MP                                 # noqa: E402
from data_quality import clean_ohlc                          # noqa: E402
from mc_v3 import (carry_log_h, fit_har_v3, har_forecast_v3,  # noqa: E402
                   signal_alpha, simulate_paths_v3)
from primitives import load_ohlc, yz_variance_proxy          # noqa: E402

DPS_AED = 0.162   # Borouge plc H1-2026 earnings release: "annual dividend intention of
                  # 16.2 fils per share remains in place".

prof = MP.PROFILES['AE']
raw = load_ohlc(os.path.join(HERE, 'BOROUGE_Stock_Price_History.csv'))
df, rep = clean_ohlc(raw, 'BOROUGE', verbose=False, market='AE')
df = df.reset_index(drop=True)
dates = pd.to_datetime(df['Date'])
close = df['Price'].to_numpy(dtype=float)
i = len(df) - 1
anchor_date = dates.iloc[i]
spot = float(close[i])
Q_ANNUAL = DPS_AED / spot

v_ = yz_variance_proxy(df)
plan = HZ.cohort_plan('AE', anchor_date)
width_mult = AW.live_width_mult(df, prof)
nu, cal = prof.nu, prof.width_cal

out = dict(anchor_date=str(anchor_date.date()), spot=spot, nu=nu,
           width_cal=cal, width_overlay_mult=float(width_mult),
           rf_live=prof.rf_live, q_annual=Q_ANNUAL, dps_aed=DPS_AED,
           q_source="Borouge plc H1-2026 earnings release, 27 July 2026 — annual "
                    "dividend intention of 16.2 fils per share, on the 2.40 close",
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
    lo = paths.min(axis=1)
    hi = paths.max(axis=1)
    out['horizons'][short] = dict(
        h=h, target_date=hz['target_date'], grade_date=hz['grade_date'],
        anchor_vol_ann=float(np.sqrt(dvar * 252)), sigma_h=sigma_h,
        drift_log_h=float(drift),
        pct={f'p{p}': float(np.percentile(term, p)) for p in (5, 25, 50, 75, 95)},
        p_above=float(np.mean(term > spot)),
        p_up10=float(np.mean(term >= spot * 1.10)),
        p_dn10=float(np.mean(term <= spot * 0.90)),
        touch_up={f'{int(k * 100)}': float(np.mean(hi >= spot * (1 + k)))
                  for k in (0.05, 0.10, 0.15, 0.20)},
        touch_dn={f'{int(k * 100)}': float(np.mean(lo <= spot * (1 - k)))
                  for k in (0.05, 0.10, 0.15, 0.20)},
        touch_up10=float(np.mean(hi >= spot * 1.10)),
        touch_dn10=float(np.mean(lo <= spot * 0.90)),
    )

np.save(os.path.join(HERE, 'paths_1M.npy'), paths_store['1M'][:20000])
np.save(os.path.join(HERE, 'paths_3M.npy'), paths_store['3M'][:20000])
with open(os.path.join(HERE, 'strike_result.json'), 'w') as f:
    json.dump(out, f, indent=1)

print(f"anchor {out['anchor_date']} spot {spot:.2f} AED | nu {nu} width_cal {cal} "
      f"overlay x{width_mult:.3f}")
print(f"carry: rf {prof.rf_live:.2%} less dividend yield {Q_ANNUAL:.2%} "
      f"= {prof.rf_live - Q_ANNUAL:+.2%} a year")
for short, hzd in out['horizons'].items():
    print(short, hzd['h'], 'sessions to', hzd['grade_date'],
          '| vol', round(hzd['anchor_vol_ann'], 3),
          '| pct', {k: round(v, 3) for k, v in hzd['pct'].items()},
          '| P(above)', round(hzd['p_above'], 2))
