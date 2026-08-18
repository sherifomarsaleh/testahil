"""SAVOLA — forward cone strike via the identical production chain
(Step 0.0 gate -> YZ proxy -> fit_har_v3 -> har_forecast_v3 -> carry_log_h ->
simulate_paths_v3, 50k paths, seed 42, live SA fit), local CSV, no site write.

q_annual = 0.0, SOURCED AND FLAGGED (not assumed): the FY2025 dividend of SAR
1.70 went EX on 07-May-2026 and was paid during H1-2026 (company H1 release);
no interim has been declared for FY2026, and under the stated annual-final
policy the next expected ex-date (~May-2027, after the FY2026 AGM) falls
outside both the 1-month and 3-month windows struck here.
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

Q_ANNUAL = 0.0   # see module docstring — sourced ex-date calendar, not an assumption

prof = MP.PROFILES['SA']
raw = load_ohlc(os.path.join(HERE, '../raw_ohlc/SA/SAVOLA.csv'))
df, rep = clean_ohlc(raw, 'SAVOLA', verbose=False, market='SA')
df = df.reset_index(drop=True)
dates = pd.to_datetime(df['Date'])
close = df['Price'].to_numpy(dtype=float)
i = len(df) - 1
anchor_date = dates.iloc[i]
spot = float(close[i])
v_ = yz_variance_proxy(df)
plan = HZ.cohort_plan('SA', anchor_date)
width_mult = AW.live_width_mult(df, prof)
assert width_mult == 1.0, "SA carries no width overlay — anything else is a bug"
nu, cal = prof.nu, prof.width_cal

out = dict(anchor_date=str(anchor_date.date()), spot=spot, nu=nu,
           width_cal=cal, width_overlay_mult=float(width_mult),
           rf_carry=float(prof.carry_rate(anchor_date)), q_annual=Q_ANNUAL, horizons={})
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
    assert alpha == 0.0, "SA signal is OFF in the live profile"
    paths = simulate_paths_v3(spot, dvar, h, drift + alpha, nu=nu,
                              n_paths=50000, seed=42, width_cal=cal_eff)
    term = paths[:, -1]
    paths_store[short] = paths
    out['horizons'][short] = dict(
        h=h, target_date=hz['target_date'], grade_date=hz['grade_date'],
        basis=hz['basis'],
        anchor_vol_ann=float(np.sqrt(dvar * 252)), sigma_h=sigma_h,
        drift_log_h=float(drift),
        pct={f'p{p}': float(np.percentile(term, p)) for p in (5, 25, 50, 75, 95)},
        p_above=float(np.mean(term > spot)),
        p_up5=float(np.mean(term >= spot * 1.05)),
        p_dn5=float(np.mean(term <= spot * 0.95)),
        p_up10=float(np.mean(term >= spot * 1.10)),
        p_dn10=float(np.mean(term <= spot * 0.90)),
        touch_up5=float(np.mean(paths.max(axis=1) >= spot * 1.05)),
        touch_dn5=float(np.mean(paths.min(axis=1) <= spot * 0.95)),
        touch_up10=float(np.mean(paths.max(axis=1) >= spot * 1.10)),
        touch_dn10=float(np.mean(paths.min(axis=1) <= spot * 0.90)),
        touch_up15=float(np.mean(paths.max(axis=1) >= spot * 1.15)),
        touch_dn15=float(np.mean(paths.min(axis=1) <= spot * 0.85)),
        touch_up20=float(np.mean(paths.max(axis=1) >= spot * 1.20)),
        touch_dn20=float(np.mean(paths.min(axis=1) <= spot * 0.80)),
    )

np.save(os.path.join(HERE, 'paths_1M.npy'), paths_store['1M'][:20000])
np.save(os.path.join(HERE, 'paths_3M.npy'), paths_store['3M'][:20000])
with open(os.path.join(HERE, 'strike_result.json'), 'w') as f:
    json.dump(out, f, indent=1)
for short, hzd in out['horizons'].items():
    print(short, hzd['h'], 'sess to', hzd['grade_date'], f"({hzd['basis']})",
          '| vol', round(hzd['anchor_vol_ann'], 3),
          '| pct', {k: round(v, 2) for k, v in hzd['pct'].items()},
          '| P(above)', round(hzd['p_above'], 2))
