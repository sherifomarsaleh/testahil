"""ADIB-Egypt — forward cone struck through the IDENTICAL production chain.

Step 0.0 data-quality gate -> Yang-Zhang variance proxy -> fit_har_v3 ->
har_forecast_v3 -> carry_log_h -> simulate_paths_v3, 50,000 paths, seed 42, on the LIVE
EG fit read from the engine registry. No parameter is chosen here and none is written
back to the site.

THIS IS THE PRICE-ENGINE LENS. It is not the fundamental walk-forward beneath this study
and it is not the technical calibration; the three are different tests and this study
names which is which every time.
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

# FY2025 dividends PAID per the consolidated cash-flow statement, EGP 1,055.866 million,
# over the market capitalisation at the study's own spot (EGP 52.05 x 1,500mn shares).
# A trailing cash yield on today's capitalisation, which is what the carry drift wants.
Q_ANNUAL = 1055.866 / (52.05 * 1500.0)

prof = MP.PROFILES['EG']
raw = load_ohlc(os.path.join(HERE, 'ADIB_Stock_Price_History.csv'))
df, rep = clean_ohlc(raw, 'ADIB', verbose=False, market='EG')
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

out = dict(anchor_date=str(anchor_date.date()), spot=spot, nu=nu, width_cal=cal,
           width_overlay_mult=float(width_mult), rf_live=prof.rf_live,
           q_annual=Q_ANNUAL, rows=len(df), dq=rep if isinstance(rep, dict) else str(rep),
           horizons={})
for short, hz in plan['horizons'].items():
    h = int(hz['horizon_days'])
    months = 1 if short == '1M' else 3
    beta, s2 = fit_har_v3(v_, i, horizon=h)
    dvar = har_forecast_v3(v_, i, beta, s2, horizon=h)
    cal_eff = cal * width_mult
    sigma_h = float(np.sqrt(dvar * h) * cal_eff)
    drift = carry_log_h(prof, anchor_date, Q_ANNUAL, h, yearfrac=months / 12.0)
    alpha, z = signal_alpha(prof, close, i, sigma_h)
    paths = simulate_paths_v3(spot, dvar, h, drift + alpha, nu=nu, n_paths=50000,
                              seed=42, width_cal=cal_eff)
    term = paths[:, -1]
    out['horizons'][short] = dict(
        h=h, target_date=hz['target_date'], grade_date=hz['grade_date'],
        sigma_h=sigma_h, drift=float(drift), signal_alpha=float(alpha),
        signal_z=float(z),
        p5=float(np.percentile(term, 5)), p25=float(np.percentile(term, 25)),
        p50=float(np.percentile(term, 50)), p75=float(np.percentile(term, 75)),
        p95=float(np.percentile(term, 95)),
        p_up=float((term > spot).mean()))
json.dump(out, open(os.path.join(HERE, 'strike_result.json'), 'w'), indent=1, default=str)
print('anchor %s  spot %.2f  rows %d  nu %.1f  width_cal %.3f  overlay %.4f  q %.4f%%'
      % (out['anchor_date'], spot, len(df), nu, cal, width_mult, 100 * Q_ANNUAL))
for k, v in out['horizons'].items():
    print('  %-3s h=%d  p5 %.2f  p25 %.2f  p50 %.2f  p75 %.2f  p95 %.2f  P(up) %.1f%%'
          % (k, v['h'], v['p5'], v['p25'], v['p50'], v['p75'], v['p95'], 100 * v['p_up']))
