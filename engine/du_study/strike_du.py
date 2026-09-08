"""DU — forward cone strike via the identical production chain
(Step 0.0 gate -> YZ proxy -> fit_har_v3 -> har_forecast_v3 -> carry_log_h ->
simulate_paths_v3, 50k paths, seed 42, live AE fit), local CSV, no site write."""
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

# THE DIVIDEND YIELD IS STRUCK ON THE SAME PRICE AS THE CONE, not on a superseded one.
# Corrected 08-09-2026 with the study's re-strike: this line divided the declared cash stream
# by AED 12.30, the 7-August close, while the cone itself was seeded at whatever session the
# library ended on. A carry drift is rf less q, so a q struck on the wrong price is a drift
# struck on the wrong price.
_SPOT_FOR_Q = None   # set below, from the session the cone is actually struck at
DPS_DECLARED = 0.66  # FY2025 final AED 0.40 paid 28-Apr-2026 + H1-2026 interim AED 0.26,
                     # ex 31-Jul-2026, paid 21-Aug-2026 (FS/ER, investors.du.ae)

prof = MP.PROFILES['AE']
raw = load_ohlc(os.path.join(HERE, '../raw_ohlc/AE/DU.csv'))
df, rep = clean_ohlc(raw, 'DU', verbose=False, market='AE')
df = df.reset_index(drop=True)
dates = pd.to_datetime(df['Date'])
close = df['Price'].to_numpy(dtype=float)
i = len(df) - 1
anchor_date = dates.iloc[i]
spot = float(close[i])
Q_ANNUAL = DPS_DECLARED / spot     # struck on the SAME price as the cone, never on a stale one
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
    # THE PER-HORIZON IC, as the production strike passes it [R-DRIFT-01]. This line read
    # signal_alpha(prof, close, i, sigma_h) until 08-09-2026 and therefore carried the
    # ONE-MONTH ic across to the three-month horizon, which the rule names explicitly as
    # something that must at least be disclosed and is better not done: it understated the
    # 3M tilt by about three quarters of a point and made this study's published cone
    # differ from the one the site strikes for the same name on the same session.
    alpha, z = signal_alpha(prof, close, i, sigma_h,
                            ic=(getattr(prof, 'ic_by_h', None) or {}).get(short))
    paths = simulate_paths_v3(spot, dvar, h, drift + alpha, nu=nu,
                              n_paths=50000, seed=42, width_cal=cal_eff)
    term = paths[:, -1]
    paths_store[short] = paths
    out['horizons'][short] = dict(
        h=h, target_date=hz['target_date'], grade_date=hz['grade_date'],
        anchor_vol_ann=float(np.sqrt(dvar * 252)), sigma_h=sigma_h,
        drift_log_h=float(drift),
        pct={f'p{p}': float(np.percentile(term, p)) for p in (5, 25, 50, 75, 95)},
        signal_alpha=float(alpha), signal_z=float(z),
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
