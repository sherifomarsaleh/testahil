"""ELEC study — Step 0.0 data-quality gate + Step 0 calibration gate.

Production-identical per the engine-reconciliation rule: the live EG fit is read
from engine/fitted_configs.json (never quoted from memory), every production
transform is applied (data_quality.clean_ohlc -> backtest_v3 on the calendar
3-month horizon -> apply_breaks -> scale-normalisation crps/spot ->
robust_verdict across bootstrap blocks {2,3,4}). ELEC is NEW coverage: it has
no committed fitted_configs entry to reconcile a verdict against, so the
reconciliation ASSERT here is on the FIT ITSELF — the (nu, width_cal) used must
be exactly the committed EG production fit, and the market-panel gate verdict
must match the committed registry (PASS).
"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import numpy as np
import pandas as pd
from primitives import load_ohlc as raw_load
from data_quality import clean_ohlc, screen, jump_threshold
from mc_v3 import backtest_v3
from panel_refresh import apply_breaks, robust_verdict
from market_profiles import PROFILES

EG = PROFILES['EG']

# ---- engine reconciliation: read the LIVE committed fit, assert it is what we use
with open(os.path.join(HERE, '..', 'fitted_configs.json')) as f:
    reg = json.load(f)['EG']
NU, CAL = float(reg['nu']), float(reg['width_cal'])
assert (NU, CAL) == (float(EG.nu), float(EG.width_cal)), \
    f"registry ({NU},{CAL}) != profile ({EG.nu},{EG.width_cal}) — mirror out of sync"
assert reg['market_verdict'] == 'PASS', reg['market_verdict']
assert 'ELEC' not in reg['panel_names'], "ELEC already covered — not new coverage"

# ---- Step 0.0 — data-quality gate ----------------------------------------
df_raw = raw_load(os.path.join(HERE, 'ELEC_Stock_Price_History.csv'))
df, dq_log = clean_ohlc(df_raw, 'ELEC', verbose=True, market='EG')
scr = screen(df)
span_yr = (df['Date'].iloc[-1] - df['Date'].iloc[0]).days / 365.25
density = len(df) / span_yr
print(f"Step 0.0: raw {len(df_raw)} rows -> clean {len(df)} rows | "
      f"{df['Date'].iloc[0].date()} .. {df['Date'].iloc[-1].date()} "
      f"({span_yr:.1f} yr, {density:.1f} rows/yr) | max |log move| {scr['max_abs_log']:.3f} "
      f"(EG artifact threshold {jump_threshold('EG'):.3f}) | flat_frac {scr['flat_frac']:.3f}")

# ---- Step 0 — calibration gate (calendar 3m, carry-anchored, live EG fit) --
r = backtest_v3(df, EG, horizon_months=3, nu=NU, width_cal=CAL,
                use_signal=EG.signal_active, n_paths=20000, seed=42,
                min_history=260)
n_all = len(r)
r = apply_breaks(r, EG)
r['crps_n'] = r['crps'] / r['spot']
r['crps_b_n'] = r['crps_b'] / r['spot']
skill = 1 - r['crps_n'].sum() / r['crps_b_n'].sum()
skill_raw = 1 - r['crps'].sum() / r['crps_b'].sum()
verd, detail = robust_verdict(r['crps_n'].values, r['crps_b_n'].values)
pit = r['pit'].values
pit_hist = np.histogram(pit, bins=10, range=(0, 1))[0].tolist()
summ = dict(
    windows_scored=int(len(r)), windows_prebreak_dropped=int(n_all - len(r)),
    first_origin=str(r['origin'].iloc[0].date()), last_origin=str(r['origin'].iloc[-1].date()),
    nu=NU, width_cal=CAL,
    skill_norm=float(skill), skill_raw=float(skill_raw),
    verdict=verd,
    ci_blocks={str(b): [float(detail[b][0]), float(detail[b][1]), detail[b][2]]
               for b in (2, 3, 4)},
    cov50=float(r['in50'].mean()), cov80=float(r['in80'].mean()),
    cov90=float(r['in90'].mean()), pit_mean=float(pit.mean()),
    pit_hist=pit_hist,
    w90_ratio=float((r['w90'] / r['w90_b']).mean()),
    market_gate=dict(verdict=reg['market_verdict'], skill=reg['market_skill'],
                     ci90=reg['market_ci90'], fit_date=reg['fit_date'],
                     panel_names=len(reg['panel_names']), windows=reg['windows']),
    dq_log=dq_log, clean_rows=int(len(df)), density_rows_per_yr=float(density),
    span_years=float(span_yr),
)
r.to_csv(os.path.join(HERE, 'backtest_rows.csv'), index=False)
with open(os.path.join(HERE, 'step0_result.json'), 'w') as f:
    json.dump(summ, f, indent=1)
print(f"\nStep 0: {len(r)} post-break windows ({n_all - len(r)} pre-break dropped) | "
      f"nu={NU} cal={CAL}")
print(f"  skill (scale-norm) {skill:+.4f} | raw basis {skill_raw:+.4f} | verdict {verd}")
for b in (2, 3, 4):
    print(f"  block={b}: CI90 [{detail[b][0]:+.4f}, {detail[b][1]:+.4f}] {detail[b][2]}")
print(f"  cov50 {r['in50'].mean():.2f} cov80 {r['in80'].mean():.2f} cov90 {r['in90'].mean():.2f} "
      f"| PIT mean {pit.mean():.3f} | pit_hist {pit_hist} | w90 ratio {summ['w90_ratio']:.3f}")
print(f"  market gate: {reg['market_verdict']} {reg['market_skill']:+.4f} CI {reg['market_ci90']}")
