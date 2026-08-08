"""
lab_silver_dual_fit.py -- prep for the silver-calibration decision (23-Jul-2026).

Sherif's silver history (raw_ohlc/XAG/SILVER.csv, ~5.7y) is in the library but
invisible to the pipeline ('XAG' is not a profile code). Two candidate designs
were flagged in the Shrinkage_v2 appendix; this script computes BOTH end-to-end
so the decision simply selects one:

  A. POOLED 3-metal fit (recommended there): pool standardized residuals u
     across GOLD + SILVER + PLATINUM, one (nu, width_cal) for the metals
     complex, leave-one-metal-out (LOMO) per-metal verdicts -- this
     de-circularizes gold (currently a self-fit) AND gives silver a real fit
     (currently it borrows gold's with zero validation).
  B. SILVER SELF-FIT: silver fits on its own residuals (same circularity
     flag as gold's current PROVISIONAL).

Lab-only: builds the silver panel in /home/claude/labwork (NOT engine/panels),
touches no production file. Silver panel built with the METALS profile
(Fed-based carry, no signal, no breaks) -- same conventions as gold's panel.
"""
import sys, os
import numpy as np
import pandas as pd

sys.path.insert(0, '/home/claude/testahil_repo/engine')
from mc_v2 import load_ohlc as _raw_load
from mc_v3 import backtest_v3, fit_nu_scale, shrink_cal, simulate_terminal_v3
from mc_v2 import crps_sample
from data_quality import clean_ohlc
from market_profiles import METALS
from panel_refresh import robust_verdict, verdict_ci

N_PATHS, SEED, MIN_HISTORY = 20000, 42, 260
ENG = '/home/claude/testahil_repo/engine'

# ---------------------------------------------------------------- build silver panel (lab copy)
df = _raw_load(os.path.join(ENG, 'raw_ohlc/XAG/SILVER.csv'))
df, log = clean_ohlc(df, 'SILVER', verbose=True, market=None)
rows = backtest_v3(df, METALS, horizon=60, nu=8.0, width_cal=1.0,
                   use_signal=METALS.signal_active,
                   n_paths=N_PATHS, seed=SEED, min_history=MIN_HISTORY)
sil = pd.DataFrame(rows)
sil['origin_idx'] = MIN_HISTORY + np.arange(len(sil)) * 60
sil.to_csv('/home/claude/labwork/XAG_SILVER_60d_LAB.csv', index=False)
print(f"\nSILVER panel: {len(sil)} windows, origins {sil['origin'].iloc[0]} .. {sil['origin'].iloc[-1]}")

gold = pd.read_csv(os.path.join(ENG, 'panels/XAU_GOLD_60d.csv'))
plat = pd.read_csv(os.path.join(ENG, 'panels/XPT_PLATINUM_60d.csv'))
panels = {'GOLD': gold, 'SILVER': sil, 'PLATINUM': plat}
for k, p in panels.items():
    print(f"{k}: {len(p)} windows")


def rescore_panel(r, nu, cal):
    carry = r['drift'].values - r['alpha'].values
    sigma = r['sigma_h'].values * cal
    drift = carry + r['alpha'].values * cal
    out = np.empty(len(r))
    for i in range(len(r)):
        out[i] = crps_sample(simulate_terminal_v3(r['spot'].values[i], sigma[i], drift[i],
                             nu=nu, n_paths=N_PATHS, seed=int(SEED + r['origin_idx'].values[i])),
                             r['realized'].values[i])
    return out


def name_verdict(r, nu, cal):
    c = rescore_panel(r, nu, cal)
    cb = r['crps_b'].values
    spot = r['spot'].values
    cn, cbn = c / spot, cb / spot
    sk = float(1 - cn.sum() / cbn.sum())
    verd, detail = robust_verdict(cn, cbn)
    return sk, verd, cn, cbn


def fmt_nu(nu):
    return 'Gaussian' if nu >= 200 else f'{nu:.1f}'


# ---------------------------------------------------------------- A: pooled 3-metal
print("\n=== A. POOLED 3-metal fit (LOMO verdicts) ===")
pooled_u = np.concatenate([p['u'].values for p in panels.values()])
nu_p, s_p = fit_nu_scale(pooled_u)
cal_p = shrink_cal(s_p)
print(f"pooled fit on {len(pooled_u)} windows: nu={fmt_nu(nu_p)}, width_cal={cal_p:.3f} (mle_scale={s_p:.3f})")

allc, allb = [], []
for k, p in panels.items():
    others = np.concatenate([q['u'].values for m, q in panels.items() if m != k])
    nu_l, s_l = fit_nu_scale(others)
    cal_l = shrink_cal(s_l)
    sk, verd, cn, cbn = name_verdict(p, nu_l, cal_l)
    allc.append(cn); allb.append(cbn)
    print(f"  {k:9s} LOMO fit (nu={fmt_nu(nu_l)}, cal={cal_l:.3f}): skill={sk:+.4f}  {verd}")
ac, ab = np.concatenate(allc), np.concatenate(allb)
lo, hi, mv = verdict_ci(ac, ab, block=6)
print(f"  COMPLEX pooled verdict: skill={1-ac.sum()/ab.sum():+.4f} CI90=[{lo:+.3f},{hi:+.3f}] {mv}")

# ---------------------------------------------------------------- B: silver self-fit
print("\n=== B. SILVER self-fit (circular, gold-style PROVISIONAL) ===")
nu_s, s_s = fit_nu_scale(sil['u'].values)
cal_s = shrink_cal(s_s)
sk_s, verd_s, _, _ = name_verdict(sil, nu_s, cal_s)
print(f"self fit on {len(sil)} windows: nu={fmt_nu(nu_s)}, width_cal={cal_s:.3f} -> skill={sk_s:+.4f}  {verd_s}  [CIRCULAR]")

# what silver runs TODAY (borrowed gold config nu=250/cal=1.0 -- published with no fit of its own)
sk_b, verd_b, _, _ = name_verdict(sil, 250.0, 1.0)
print(f"current borrowed-gold config (nu=Gaussian, cal=1.0): skill={sk_b:+.4f}  {verd_b}")

# cone comparison at today's silver spot
spot = float(sil['spot'].values[-1])
print(f"\n90% cone half-width comparison (x sigma_h units, q95 x cal):")
from scipy import stats
for label, nu_x, cal_x in [('borrowed-gold (today)', 250.0, 1.0),
                            ('pooled 3-metal', nu_p, cal_p),
                            ('self-fit', nu_s, cal_s)]:
    q = 1.6449 if nu_x >= 200 else float(stats.t.ppf(0.95, nu_x) / np.sqrt(nu_x / (nu_x - 2)))
    print(f"  {label:22s} nu={fmt_nu(nu_x):9s} cal={cal_x:.3f}  half-width={q*cal_x:.3f}")
