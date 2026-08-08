"""
lab_round7c_dated_capm.py -- Task 27 payoff: rerun Round 6's CAPM level-fix
candidate with the DATED Egypt ERP/rf* schedule (Part A of Round 7) instead
of the static Jul-2026 snapshot, to see if the "carry anchor is too low"
finding survives, strengthens, or weakens once the ERP is allowed to vary
with the actual macro regime at each origin date (esp. the 2022-23 spike).
Reuses the Round 7 precompute (beta, carry_b, sigma_h, sig_b, rf_star_dated,
erp_dated already computed per-row, walk-forward-safe).
"""
import sys, zlib, time
import numpy as np
import pandas as pd

sys.path.insert(0, '/home/claude/testahil_repo/engine')
from mc_v2 import crps_sample, winkler
from mc_v3 import simulate_terminal_v3, pooled_scores

HORIZON = 60
N_PATHS = 20000
SEED = 42
DEV_CUTOFF = pd.Timestamp('2025-07-01')
RF_STAR_STATIC, ERP_STATIC = 0.1594, 0.1394   # Round 6 snapshot, for direct comparison

pre = pd.read_csv('/tmp/lab_round7_precomp.csv', parse_dates=['date'])
dev_rows = pre[pre['date'] < DEV_CUTOFF].reset_index(drop=True)
print(f"DEV rows: {len(dev_rows)}")


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


t0 = time.time()
results = []
print("\n=== static snapshot (Round 6 replica, rating-basis) vs DATED schedule (Round 7) ===")
for variant, rf_fn, erp_fn in [
    ('static_snapshot', lambda r: RF_STAR_STATIC, lambda r: ERP_STATIC),
    ('dated_schedule',  lambda r: r['rf_star_dated'], lambda r: r['erp_dated']),
]:
    for s in [0.0, 0.25, 0.5, 0.75, 1.0]:
        def drift_fn(r, rf_fn=rf_fn, erp_fn=erp_fn, s=s):
            ke_log_h = np.log1p(rf_fn(r) + r['beta'] * erp_fn(r)) * HORIZON / 252.0
            return r['carry_b'] + s * (ke_log_h - r['carry_b'])
        res = run_variant(dev_rows, drift_fn)
        sc, _ = pooled_scores([res])
        results.append(dict(variant=variant, s=s, **sc))
        print(f"  [{variant:16s} s={s:.2f}]  crps_skill={sc['crps_skill']:+.4f}  "
              f"cov90={sc['cov90']:.3f} [{cov_flag(sc['cov90'])}]  pit={sc['pit_mean']:.3f}  "
              f"w90_ratio={sc['w90_ratio']:.3f}  ({time.time()-t0:.0f}s)")

res_df = pd.DataFrame(results)
res_df.to_csv('/tmp/lab_round7c_dev_sweep.csv', index=False)
print(f"\ntotal runtime: {time.time()-t0:.0f}s")
print(res_df.to_string(index=False, float_format=lambda x: f'{x:8.4f}'))

# decomposition check, dated schedule, s=1.0: real beta vs flat beta=1.0 (mirrors Round 6's check)
print("\n=== decomposition check on the DATED schedule (mirrors Round 6) ===")
for label, beta_col in [('real per-name beta', 'beta')]:
    def drift_fn(r, beta_col=beta_col):
        ke_log_h = np.log1p(r['rf_star_dated'] + r[beta_col] * r['erp_dated']) * HORIZON / 252.0
        return r['carry_b'] + 1.0 * (ke_log_h - r['carry_b'])
    res = run_variant(dev_rows, drift_fn)
    sc, _ = pooled_scores([res])
    print(f"  [{label:20s}]  crps_skill={sc['crps_skill']:+.4f}  cov90={sc['cov90']:.3f}  pit={sc['pit_mean']:.3f}")


def drift_flat(r):
    ke_log_h = np.log1p(r['rf_star_dated'] + 1.0 * r['erp_dated']) * HORIZON / 252.0
    return r['carry_b'] + 1.0 * (ke_log_h - r['carry_b'])


res_flat = run_variant(dev_rows, drift_flat)
sc_flat, _ = pooled_scores([res_flat])
print(f"  [{'flat beta=1.0':20s}]  crps_skill={sc_flat['crps_skill']:+.4f}  cov90={sc_flat['cov90']:.3f}  pit={sc_flat['pit_mean']:.3f}")
