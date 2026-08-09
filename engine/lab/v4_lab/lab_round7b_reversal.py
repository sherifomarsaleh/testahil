"""
lab_round7b_reversal.py -- quick follow-up to Round 7's trend-continuation
result. Diagnostic (corr(trailing trend, fwd 60d return) ~ 0, and NEGATIVE
for 19/30 names -- consistent with EGYPT profile's own already-validated
rev_1m/signal_sign=-1 finding: "no EGX momentum; overreaction/short-term
reversal supported") suggests the panel may reward FADING the trend, not
following it. Tests the sign-flipped candidate: tilt = -w_i * trend_i.
Reuses the Round 7 precompute (/tmp/lab_round7_precomp.csv) -- no refit needed.

NOTE: this is a DIFFERENT construction than literally what Sherif described
(follow the trend) -- flagged explicitly, not adopted silently, in the writeup.
"""
import sys, zlib
import numpy as np
import pandas as pd

sys.path.insert(0, '/home/claude/testahil_repo/engine')
from mc_v2 import crps_sample, winkler
from mc_v3 import simulate_terminal_v3, pooled_scores

HORIZON = 60
N_PATHS = 20000
SEED = 42
DEV_CUTOFF = pd.Timestamp('2025-07-01')

pre = pd.read_csv('/tmp/lab_round7_precomp.csv', parse_dates=['date'])
dev_rows = pre[pre['date'] < DEV_CUTOFF].reset_index(drop=True)


def stable_seed(ticker, oi):
    return SEED + int(oi) + zlib.crc32(ticker.encode()) % 1000


def run_variant(rows_df, drift_fn):
    out = []
    for _, r in rows_df.iterrows():
        drift = drift_fn(r)
        seed = stable_seed(r['ticker'], r['origin_idx'])
        samp = simulate_terminal_v3(r['spot'], r['sigma_h'], drift, nu=4.0, n_paths=N_PATHS, seed=seed)
        rngb = np.random.default_rng(seed + 1)
        bench = r['spot'] * np.exp(r['carry_b'] + r['sig_b'] * rngb.standard_normal(N_PATHS))
        q_e = np.percentile(samp, [5, 25, 50, 75, 95]); q_b = np.percentile(bench, [5, 25, 50, 75, 95]); y = r['realized']
        out.append(dict(origin=r['date'], ticker=r['ticker'], spot=r['spot'], realized=y, drift=drift,
            crps=crps_sample(samp, y), crps_b=crps_sample(bench, y),
            pin50=0.5*abs(y-q_e[2]), pin50_b=0.5*abs(y-q_b[2]),
            wink=winkler(q_e[0], q_e[4], y), wink_b=winkler(q_b[0], q_b[4], y),
            pit=float(np.mean(samp <= y)),
            in50=q_e[1] <= y <= q_e[3], in80=np.percentile(samp,10) <= y <= np.percentile(samp,90), in90=q_e[0] <= y <= q_e[4],
            w90=(q_e[4]-q_e[0])/r['spot'], w90_b=(q_b[4]-q_b[0])/r['spot'], med_disp=(q_e[2]/r['spot']-1)))
    return pd.DataFrame(out)


def cov_flag(cov90):
    return "OK" if 0.88 <= cov90 <= 0.92 else "OUT-OF-RANGE"


print("=== B2: REVERSAL-flipped signed trend (carry - s*tilt) -- exploratory, diagnostic-driven ===")
results = []
import time
t0 = time.time()
for w in [126, 252]:
    for k in [1, 4, 9]:
        for s in [0.0, 0.25, 0.5, 0.75, 1.0]:
            def drift_fn(r, w=w, k=k, s=s):
                t2 = r[f'tstat_{w}'] ** 2
                wgt = t2 / (t2 + k)
                tilt = wgt * r[f'dmean_{w}'] * HORIZON
                return r['carry_b'] - s * tilt          # <-- sign flipped vs Round 7 B1
            res = run_variant(dev_rows, drift_fn)
            sc, _ = pooled_scores([res])
            results.append(dict(family='reversal', window=w, k=k, s=s, **sc))
            print(f"  [w={w:3d} k={k} s={s:.2f}]  crps_skill={sc['crps_skill']:+.4f}  "
                  f"cov90={sc['cov90']:.3f} [{cov_flag(sc['cov90'])}]  pit={sc['pit_mean']:.3f}  "
                  f"w90_ratio={sc['w90_ratio']:.3f}  ({time.time()-t0:.0f}s)")

res_df = pd.DataFrame(results)
res_df.to_csv('/tmp/lab_round7b_dev_sweep.csv', index=False)
print(f"\ntotal runtime: {time.time()-t0:.0f}s")
best = res_df.sort_values('crps_skill', ascending=False).head(5)
print("\ntop 5 by crps_skill:")
print(best.to_string(index=False, float_format=lambda x: f'{x:8.4f}'))
