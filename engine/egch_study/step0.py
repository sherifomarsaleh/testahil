"""EGCH (KIMA) study — Step 0.0 data-quality gate + Step 0 calibration gate.

Production-identical per the engine-reconciliation rule: the live EG fit is read
from engine/fitted_configs.json (never quoted from memory), every production
transform is applied (data_quality.clean_ohlc -> backtest_v3 on the calendar
3-month horizon -> apply_breaks -> scale-normalisation crps/spot ->
robust_verdict across bootstrap blocks {2,3,4}). EGCH is NEW coverage: it has
no committed fitted_configs entry to reconcile a verdict against, so the
reconciliation ASSERT here is on the FIT ITSELF — the (nu, width_cal) used must
be exactly the committed EG production fit. The skill verdict is RETIRED
[R-CAL-03] and is read for the archive only; it is not a gate and this script no
longer asserts a value for it.
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
# THE SKILL VERDICT IS RETIRED AND THIS ASSERT WAS STILL DEMANDING IT. [R-CAL-03] retired
# PASS/PARITY/FAIL outright on 25 August 2026 — no gate, no materiality trigger, nothing on
# any public surface — after measuring that it had never excluded a market and disagreed
# with the band record on 40% of the book. This line went on asserting 'PASS' against a
# registry that now prints PARITY, so step0 ABORTED before it ran a single check: a script
# holding a retired standard does not report the standard is gone, it reports a failure.
# Found by an audit run from outside the study on 5 September 2026.
#
# What replaces it is the thing that IS the gate: the fit this study simulates on must be
# the committed EG production fit, cell for cell, which the assert above already checks.
# The verdict is recorded for the archive and asserted on only for its PRESENCE, because a
# registry that stopped carrying one would mean the mirror had changed shape.
assert reg.get('market_verdict'), 'the registry carries no market verdict at all'
_RETIRED_VERDICT = reg['market_verdict']
# EGCH WAS NEW COVERAGE WHEN THIS STUDY WAS WRITTEN AND IS NOT ANY MORE. The line here
# asserted its ABSENCE from the EG panel, which was true in August and stopped being true
# when the name was posted — so this script aborted on a fact about the world having
# changed in the direction the project wanted. A study-local assert that encodes a
# transient state ages into a false alarm, and a false alarm on a data-quality gate is
# worse than none because the gate stops running at all.
#
# It is inverted into what it was always trying to establish: the fit this study simulates
# on is the live production one. Now that EGCH sits in the panel, the reconciliation is
# STRONGER than it was — the name is inside the very panel the (nu, width_cal) above were
# fitted on, so the fit is not merely current, it is this stock's own.
_IN_PANEL = 'EGCH' in reg['panel_names']
print("Step 0 reconciliation: EGCH is %s the committed EG panel of %d names; the fit used "
      "here (nu=%s, width_cal=%s) is the live production one either way."
      % ('INSIDE' if _IN_PANEL else 'NOT YET IN', len(reg['panel_names']), NU, CAL))

# ---- Step 0.0 — data-quality gate ----------------------------------------
df_raw = raw_load(os.path.join(HERE, 'EGCH_Stock_Price_History.csv'))
df, dq_log = clean_ohlc(df_raw, 'EGCH', verbose=True, market='EG')
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
