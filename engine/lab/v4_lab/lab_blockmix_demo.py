"""
lab_blockmix_demo.py — consolidated demo/validation for the block-mixture fix
(23-Jul-2026). See claude/v4_lab/MC_TailInstability_BlockMix_20260723.md.

Runs three checks against the PRODUCTION construction (simulate_paths_v3):
  1. h=60 equivalence: block-mix is bit-for-bit identical at the fitted horizon.
  2. Long-horizon tail taming: max path / mean / median / p5-p95 at 1/2/3yr.
  3. Seed lottery: 3yr EV across seeds 42-46, production vs block-mix.

Lab-only; imports production modules read-only.
"""
import sys
import numpy as np
import pandas as pd

sys.path.insert(0, '/home/claude/testahil_repo/engine')
from mc_v2 import load_ohlc, yz_variance_proxy
from mc_v3 import fit_har_v3, har_forecast_v3, carry_log_h, simulate_paths_v3
from data_quality import clean_ohlc
import market_profiles as mp

prof = mp.EGYPT
TODAY = pd.Timestamp('2026-07-22')


def simulate_paths_blockmix(spot, daily_var, horizon, drift_log_h, nu,
                            n_paths, seed, width_cal, block=60):
    """Identical to simulate_paths_v3 EXCEPT the t-mixture is redrawn per
    `block` sessions (the horizon nu was fitted on) instead of once per path.
    At horizon <= block this reproduces production bit-for-bit (same RNG
    consumption order: z first, then n_paths chi-square draws)."""
    rng = np.random.default_rng(seed)
    sd = np.sqrt(daily_var) * width_cal
    z = rng.standard_normal((n_paths, horizon))
    if nu is None or nu > 200:
        mix = np.ones((n_paths, horizon))
    else:
        n_blocks = int(np.ceil(horizon / block))
        chi = rng.chisquare(nu, (n_paths, n_blocks))
        mix = np.repeat(np.sqrt((nu - 2) / chi), block, axis=1)[:, :horizon]
    incr = drift_log_h / horizon + z * mix * sd
    logp = np.cumsum(incr, axis=1)
    paths = np.empty((n_paths, horizon + 1))
    paths[:, 0] = spot
    paths[:, 1:] = spot * np.exp(logp)
    return paths


if __name__ == '__main__':
    tkr, spot = 'ISPH', 11.77
    df = load_ohlc(f'/home/claude/testahil_repo/engine/raw_ohlc/EG/{tkr}.csv')
    df, _ = clean_ohlc(df, tkr, verbose=False, market='EG')
    v = yz_variance_proxy(df)
    o = len(df) - 1

    # --- 1+2: horizon table ------------------------------------------------
    print(f"{'':17s} {'max path':>10s} {'mean tot':>9s} {'median':>8s} {'p5':>7s} {'p95':>8s}")
    for H, label in [(60, 'T+60'), (240, '1yr'), (500, '2yr'), (750, '3yr')]:
        beta, s2 = fit_har_v3(v, o, horizon=min(H, 252))
        dv = har_forecast_v3(v, o, beta, s2, horizon=min(H, 252))
        drift = carry_log_h(prof, TODAY, 0.0, H)
        for name, fn in [('production', simulate_paths_v3),
                         ('block-mix', simulate_paths_blockmix)]:
            p = fn(spot, dv, H, drift, nu=prof.nu, n_paths=50000, seed=42,
                   width_cal=prof.width_cal)
            t = p[:, -1]; r = t / spot - 1
            print(f"{label:6s} {name:10s} {t.max()/spot:9.1f}x {r.mean()*100:8.1f}% "
                  f"{np.median(r)*100:7.1f}% {np.percentile(r,5)*100:6.1f}% "
                  f"{np.percentile(r,95)*100:7.1f}%")
        print()

    # --- 3: seed lottery at 3yr -------------------------------------------
    beta, s2 = fit_har_v3(v, o, horizon=252)
    dv = har_forecast_v3(v, o, beta, s2, horizon=252)
    drift = carry_log_h(prof, TODAY, 0.0, 750)
    print("seed lottery, 3yr (H=750) annualized EV:")
    for seed in [42, 43, 44, 45, 46]:
        p1 = simulate_paths_v3(spot, dv, 750, drift, nu=prof.nu, n_paths=50000,
                               seed=seed, width_cal=prof.width_cal)
        p2 = simulate_paths_blockmix(spot, dv, 750, drift, nu=prof.nu,
                                     n_paths=50000, seed=seed,
                                     width_cal=prof.width_cal)
        r1 = p1[:, -1] / spot - 1; r2 = p2[:, -1] / spot - 1
        print(f"  seed {seed}: production {((1+r1.mean())**(1/3)-1)*100:6.1f}%  "
              f"block-mix {((1+r2.mean())**(1/3)-1)*100:5.1f}%  "
              f"medians {((1+np.median(r1))**(1/3)-1)*100:.1f}%/"
              f"{((1+np.median(r2))**(1/3)-1)*100:.1f}%")
