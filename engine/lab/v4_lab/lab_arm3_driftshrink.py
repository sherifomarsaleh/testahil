"""
lab_arm3_driftshrink.py — Equation Lab, Round 5 (continuation of Rounds 0-4,
23-Jul-2026). Tests the ONE untested lever flagged by the MC Family Survey
(claude/mc_survey/MC_Family_Survey_and_Verdict_20260723.md): Bayes-Stein /
hierarchical shrinkage of per-name DRIFT toward the panel's own cross-sectional
grand mean, replacing carry-only. Shape (HAR vol, nu, width_cal) UNCHANGED —
this is a center-only candidate, per the survey's own framing.

Lab-only: production files untouched. Same binding anti-overfitting protocol
as Rounds 0-4: sweep w on DEV (origin date < 2025-07-01) only; ONE FINAL shot
(>= 2025-07-01) on the winner, logged regardless of outcome.

own_mean_i(origin)  = expanding-window mean daily log return, close[0..origin]
                       (identical construction to mc_v2.backtest's retired
                       "secular_drift" — same estimator, now shrunk)
grand_mean(date)     = LONO cross-sectional mean of other names' own_mean,
                       asof `date`, requiring >=130 sessions of their own
                       history (avoids noisy brand-new listings polluting it)
mu_i(origin, w)      = grand_mean + w*(own_mean_i - grand_mean)
drift_i(origin, w)   = mu_i(origin, w) * horizon        (daily -> horizon log)

Benchmark, HAR vol fit, nu, width_cal, scoring: ALL identical to mc_v3.backtest_v3
(imported, not reimplemented) so results are directly comparable to Round 0.
"""
import sys, os, time
import numpy as np
import pandas as pd

sys.path.insert(0, '/home/claude/testahil_repo/engine')
from mc_v2 import load_ohlc, crps_sample, winkler, trailing_cc_vol, yz_variance_proxy
from mc_v3 import fit_har_v3, har_forecast_v3, simulate_terminal_v3, carry_log_h, pooled_scores, block_bootstrap_ci, verdict
from data_quality import clean_ohlc
from market_profiles import EGYPT

PROFILE = EGYPT
HORIZON = 60
MIN_HISTORY = 260
MIN_FOR_GRANDMEAN = 130
N_PATHS = 20000
SEED = 42
Q_ANNUAL = 0.0
BREAK = pd.Timestamp(max(PROFILE.breaks))          # adopted 2022-03-21 cut (shape-fit sample only)
APPLY_BREAK_TO_BACKTEST = False    # backtest_v3 itself has no break-filter logic (confirmed by reading
                                    # source): nu/width_cal are FIXED constants fit once on the
                                    # break-filtered sample, then applied over the FULL walk-forward.
                                    # Round 0-4's 538-window count only reconciles with the unfiltered
                                    # history, so match that here for a like-for-like comparison.
DEV_CUTOFF = pd.Timestamp('2025-07-01')
W_GRID = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0]
NU = PROFILE.nu
WIDTH_CAL = PROFILE.width_cal

print(f"profile EGYPT: nu={NU} width_cal={WIDTH_CAL} break_cut={BREAK.date()} signal_active={PROFILE.signal_active}")

d = '/home/claude/testahil_repo/engine/raw_ohlc/EG'
names = sorted(f[:-4] for f in os.listdir(d) if f.endswith('.csv'))
print(f"{len(names)} EG raw files: {names}")

# ---------------------------------------------------------------- load & prep
panels = {}
for t in names:
    df = load_ohlc(os.path.join(d, f'{t}.csv'))
    df, _ = clean_ohlc(df, t, verbose=False, market='EG')
    df = df.sort_values('Date').reset_index(drop=True)
    if APPLY_BREAK_TO_BACKTEST:
        df = df[df['Date'] >= BREAK].reset_index(drop=True)
    if len(df) < MIN_HISTORY + HORIZON + 1:
        continue
    v = yz_variance_proxy(df)
    close = df['Price'].values
    dates = pd.DatetimeIndex(df['Date'].values)
    n = len(close)
    lr = np.diff(np.log(close))
    exp_mean = np.full(n, np.nan)
    if n > 1:
        exp_mean[1:] = np.cumsum(lr) / np.arange(1, n)
    # grand-mean lookup arrays: only entries with >= MIN_FOR_GRANDMEAN own history
    valid = np.arange(n) >= MIN_FOR_GRANDMEAN
    gm_dates = dates[valid].values.astype('datetime64[ns]')
    gm_vals = exp_mean[valid]
    ok = ~np.isnan(gm_vals)
    gm_dates, gm_vals = gm_dates[ok], gm_vals[ok]
    panels[t] = dict(df=df, v=v, close=close, dates=dates, exp_mean=exp_mean,
                      gm_dates=gm_dates, gm_vals=gm_vals)

print(f"{len(panels)}/{len(names)} names pass post-break min-history filter (>= {MIN_HISTORY+HORIZON+1} rows after {BREAK.date()})")


def grand_mean_lookup(query_date, exclude):
    """LONO cross-sectional mean of other names' own_mean, asof query_date."""
    qd = np.datetime64(query_date)
    vals = []
    for t2, p2 in panels.items():
        if t2 == exclude or len(p2['gm_dates']) == 0:
            continue
        pos = np.searchsorted(p2['gm_dates'], qd, side='right') - 1
        if pos >= 0:
            vals.append(p2['gm_vals'][pos])
    return float(np.mean(vals)) if vals else np.nan


# ---------------------------------------------------------------- Phase 1: per-(name,origin) precompute
# sigma_h, own_mean, carry benchmark draws-independent stats -- ALL independent of w.
t0 = time.time()
precomp = []   # list of dict rows
for t, p in panels.items():
    df, v, close, dates = p['df'], p['v'], p['close'], p['dates']
    n = len(df)
    origin = MIN_HISTORY
    while origin + HORIZON < n:
        date = df['Date'].iloc[origin]
        spot = close[origin]
        y = close[origin + HORIZON]
        beta, s2 = fit_har_v3(v, origin, horizon=HORIZON)
        dv = har_forecast_v3(v, origin, beta, s2, horizon=HORIZON)
        sigma_h = np.sqrt(dv * HORIZON) * WIDTH_CAL
        own_mean = p['exp_mean'][origin]
        gmean = grand_mean_lookup(date, exclude=t)
        carry_b = carry_log_h(PROFILE, date, Q_ANNUAL, HORIZON)
        sig_b = trailing_cc_vol(close, origin) * np.sqrt(HORIZON)
        precomp.append(dict(ticker=t, origin_idx=origin, date=date, spot=spot, realized=y,
                             sigma_h=sigma_h, own_mean=own_mean, grand_mean=gmean,
                             carry_b=carry_b, sig_b=sig_b))
        origin += HORIZON

pre = pd.DataFrame(precomp)
print(f"Phase 1 (HAR fit + own/grand mean) done: {len(pre)} (name,origin) windows in {time.time()-t0:.1f}s")
n_dev = (pre['date'] < DEV_CUTOFF).sum(); n_final = (pre['date'] >= DEV_CUTOFF).sum()
print(f"DEV windows (< {DEV_CUTOFF.date()}): {n_dev}  |  FINAL windows (>=): {n_final}")
pre.to_csv('/tmp/lab_arm3_precomp.csv', index=False)


# ---------------------------------------------------------------- Phase 2: per-w simulate + score
def run_w(w, rows_df, seed_offset=0):
    """Vectorized-ish loop over precomputed rows for one candidate w. Returns
    a DataFrame matching backtest_v3's row schema so pooled_scores works unchanged."""
    out = []
    for _, r in rows_df.iterrows():
        mu = r['grand_mean'] + w * (r['own_mean'] - r['grand_mean'])
        drift = mu * HORIZON
        seed = SEED + int(r['origin_idx']) + seed_offset + hash(r['ticker']) % 1000
        samp = simulate_terminal_v3(r['spot'], r['sigma_h'], drift, nu=NU,
                                     n_paths=N_PATHS, seed=seed)
        rngb = np.random.default_rng(seed + 1)
        bench = r['spot'] * np.exp(r['carry_b'] + r['sig_b'] * rngb.standard_normal(N_PATHS))
        q_e = np.percentile(samp, [5, 25, 50, 75, 95])
        q_b = np.percentile(bench, [5, 25, 50, 75, 95])
        y = r['realized']
        out.append(dict(
            origin=r['date'], spot=r['spot'], realized=y, drift=drift, sigma_h=r['sigma_h'],
            crps=crps_sample(samp, y), crps_b=crps_sample(bench, y),
            pin50=0.5 * abs(y - q_e[2]), pin50_b=0.5 * abs(y - q_b[2]),
            wink=winkler(q_e[0], q_e[4], y), wink_b=winkler(q_b[0], q_b[4], y),
            pit=float(np.mean(samp <= y)),
            in50=q_e[1] <= y <= q_e[3], in80=np.percentile(samp, 10) <= y <= np.percentile(samp, 90),
            in90=q_e[0] <= y <= q_e[4],
            w90=(q_e[4] - q_e[0]) / r['spot'], w90_b=(q_b[4] - q_b[0]) / r['spot'],
            med_disp=(q_e[2] / r['spot'] - 1),
        ))
    return pd.DataFrame(out)


dev_rows = pre[pre['date'] < DEV_CUTOFF].reset_index(drop=True)
t0 = time.time()
sweep_results = []
for w in W_GRID:
    r = run_w(w, dev_rows)
    scores, _ = pooled_scores([r])
    # individuality metric: cross-sectional std of the per-window drift/horizon (annualized-ish, daily units*252)
    mu_per_row = dev_rows['grand_mean'] + w * (dev_rows['own_mean'] - dev_rows['grand_mean'])
    drift_disp = float(mu_per_row.groupby(dev_rows['ticker']).mean().std()) * 252 * 100  # ppt/yr std across names
    sweep_results.append(dict(w=w, **scores, drift_disp_ann_pct=drift_disp))
    print(f"  w={w:.2f}  crps_skill={scores['crps_skill']:+.4f}  cov90={scores['cov90']:.3f}  "
          f"pit={scores['pit_mean']:.3f}  w90_ratio={scores['w90_ratio']:.3f}  "
          f"drift_disp={drift_disp:.1f}ppt/yr  ({time.time()-t0:.0f}s elapsed)")

sweep_df = pd.DataFrame(sweep_results)
sweep_df.to_csv('/tmp/lab_arm3_dev_sweep.csv', index=False)
print("\n=== DEV sweep summary ===")
print(sweep_df.to_string(index=False, float_format=lambda x: f'{x:8.4f}'))

# baseline (carry-only, i.e. production drift) on the SAME dev_rows/sigma_h for a clean same-harness comparison
base_rows = []
for _, r in dev_rows.iterrows():
    drift = r['carry_b']  # carry-only, no signal (EGYPT signal_active=False)
    seed = SEED + int(r['origin_idx']) + hash(r['ticker']) % 1000
    samp = simulate_terminal_v3(r['spot'], r['sigma_h'], drift, nu=NU, n_paths=N_PATHS, seed=seed)
    rngb = np.random.default_rng(seed + 1)
    bench = r['spot'] * np.exp(r['carry_b'] + r['sig_b'] * rngb.standard_normal(N_PATHS))
    q_e = np.percentile(samp, [5, 25, 50, 75, 95]); q_b = np.percentile(bench, [5, 25, 50, 75, 95]); y = r['realized']
    base_rows.append(dict(origin=r['date'], spot=r['spot'], realized=y, drift=drift, sigma_h=r['sigma_h'],
        crps=crps_sample(samp, y), crps_b=crps_sample(bench, y),
        pin50=0.5*abs(y-q_e[2]), pin50_b=0.5*abs(y-q_b[2]),
        wink=winkler(q_e[0], q_e[4], y), wink_b=winkler(q_b[0], q_b[4], y),
        pit=float(np.mean(samp <= y)),
        in50=q_e[1] <= y <= q_e[3], in80=np.percentile(samp,10) <= y <= np.percentile(samp,90), in90=q_e[0] <= y <= q_e[4],
        w90=(q_e[4]-q_e[0])/r['spot'], w90_b=(q_b[4]-q_b[0])/r['spot'], med_disp=(q_e[2]/r['spot']-1)))
base_df = pd.DataFrame(base_rows)
base_scores, _ = pooled_scores([base_df])
print(f"\n=== DEV baseline (carry-only, same harness/paths) ===\n{base_scores}")

print(f"\nTotal Phase-2 runtime: {time.time()-t0:.0f}s")
