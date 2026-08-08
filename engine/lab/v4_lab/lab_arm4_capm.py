"""
lab_arm4_capm.py — Equation Lab, Round 6 (23-Jul-2026). NEW angle, not a
re-slice of trailing returns: CAPM-style per-name drift, Ke_i = rf* + beta_i x ERP,
using (a) beta estimated from each stock's OWN weekly-return co-movement with the
panel (a genuinely different statistic than a trailing MEAN return — it is a
second-moment/co-movement estimator, structurally distinct from the six dead
mean-return-based drift families), and (b) an EXOGENOUS, non-trailing ERP
(Damodaran's Egypt country row, already sourced and cached in
Cost_of_Capital_Reference.md for the WACC pipeline) instead of a trailing panel
estimate — this is the direct fix to Round 4a's diagnosed failure mode ("the
mis-centering is forward-looking; a trailing estimator points backward").

No EGX30 index series is available in this environment (checked project files,
uploads, and the repo — only an "INTERIM ... EGX30-ETF, n=49" one-off exists,
too short/ad hoc to reuse). Market proxy: equal-weighted average weekly return
across the SAME 30-name panel already used for calibration (a standard
market-model substitute when an official cap-weighted index isn't accessible;
flagged here as a simplification, not hidden).

rf*/ERP: Cost_of_Capital_Reference.md, Egypt row, CDS-basis (primary per house
convention) -- rf*=18.91%, ERP=9.41%, "as of" 21-Jul-2026 vintage. Applied as a
STATIC snapshot across the whole 2016-2026 backtest window -- the same kind of
gate-neutral backtest simplification the existing carry_schedule/breaks already
use elsewhere in this system (a live-publish version would need a full
historical ERP schedule, which does not exist yet). Rating-basis (rf*=15.94%,
ERP=13.94%) run alongside as a cross-check.

Beta: trailing weekly regression, own return vs panel-average return, up to 5yr
(260 weeks), walk-forward safe (only weeks ending before the origin). Usability
gate matches wacc_builder.py's RegressionBetaAttempt: n>=24, R^2>=5%,
SE(beta)<|beta|; fallback beta=1.0 (documented house default) when not usable.

Shape (HAR vol, nu, width_cal) and benchmark: UNCHANGED, identical to Round 0/5.
w/s grid swept on DEV only; ONE FINAL shot reserved for a genuinely promising s,
per the binding anti-overfitting protocol.
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
N_PATHS = 20000
SEED = 42
Q_ANNUAL = 0.0
DEV_CUTOFF = pd.Timestamp('2025-07-01')
NU = PROFILE.nu
WIDTH_CAL = PROFILE.width_cal

# Cost_of_Capital_Reference.md, Egypt row (21-Jul-2026 vintage, CDS-basis primary)
RF_STAR_CDS, ERP_CDS = 0.1891, 0.0941
RF_STAR_RATING, ERP_RATING = 0.1594, 0.1394
S_GRID = [0.0, 0.25, 0.5, 0.75, 1.0]   # 0=carry only, 1=full Ke replacement

print(f"profile EGYPT: nu={NU} width_cal={WIDTH_CAL} signal_active={PROFILE.signal_active}")
print(f"CDS-basis: rf*={RF_STAR_CDS:.4f} ERP={ERP_CDS:.4f}  |  rating-basis: rf*={RF_STAR_RATING:.4f} ERP={ERP_RATING:.4f}")

d = '/home/claude/testahil_repo/engine/raw_ohlc/EG'
names = sorted(f[:-4] for f in os.listdir(d) if f.endswith('.csv'))

# ---------------------------------------------------------------- load & prep (unfiltered history, matches Round 0)
panels = {}
for t in names:
    df = load_ohlc(os.path.join(d, f'{t}.csv'))
    df, _ = clean_ohlc(df, t, verbose=False, market='EG')
    df = df.sort_values('Date').reset_index(drop=True)
    if len(df) < MIN_HISTORY + HORIZON + 1:
        continue
    v = yz_variance_proxy(df)
    close = df['Price'].values
    dates = pd.DatetimeIndex(df['Date'].values)
    s = pd.Series(close, index=dates)
    wk = s.resample('W-THU').last().dropna()          # EGX week ends Thursday
    wk_lr = np.log(wk / wk.shift(1)).dropna()
    panels[t] = dict(df=df, v=v, close=close, dates=dates, wk_lr=wk_lr)

print(f"{len(panels)}/{len(names)} names loaded")

# ---------------------------------------------------------------- market proxy: equal-weighted panel weekly return
wk_frame = pd.DataFrame({t: p['wk_lr'] for t, p in panels.items()})
market_wk = wk_frame.mean(axis=1, skipna=True).dropna()
print(f"market proxy: {len(market_wk)} weekly obs, {market_wk.index.min().date()} .. {market_wk.index.max().date()}")


def beta_at(ticker, origin_date, max_weeks=260, min_n=24, min_r2=0.05):
    """Walk-forward beta: stock's own weekly log return vs the equal-weighted
    panel proxy, trailing up to 5yr, weeks strictly before origin_date."""
    own = panels[ticker]['wk_lr']
    own = own[own.index < origin_date].tail(max_weeks)
    mkt = market_wk[market_wk.index < origin_date].tail(max_weeks)
    both = pd.concat([own.rename('own'), mkt.rename('mkt')], axis=1).dropna()
    n = len(both)
    if n < min_n:
        return 1.0, n, np.nan, np.nan, 'fallback_n'
    x = both['mkt'].values
    y = both['own'].values
    xm, ym = x.mean(), y.mean()
    sxx = np.sum((x - xm) ** 2)
    if sxx <= 0:
        return 1.0, n, np.nan, np.nan, 'fallback_degenerate'
    beta = np.sum((x - xm) * (y - ym)) / sxx
    yhat = ym + beta * (x - xm)
    resid = y - yhat
    sse = np.sum(resid ** 2)
    sst = np.sum((y - ym) ** 2)
    r2 = 1 - sse / sst if sst > 0 else 0.0
    dof = n - 2
    se_beta = np.sqrt(sse / dof / sxx) if dof > 0 and sxx > 0 else np.inf
    if r2 < min_r2 or se_beta >= abs(beta):
        return 1.0, n, r2, se_beta, 'fallback_gate'
    return float(beta), n, float(r2), float(se_beta), 'own_regression'


# ---------------------------------------------------------------- Phase 1: per-(name,origin) precompute (as Round 5)
t0 = time.time()
precomp = []
for t, p in panels.items():
    df, v, close = p['df'], p['v'], p['close']
    n = len(df)
    origin = MIN_HISTORY
    while origin + HORIZON < n:
        date = df['Date'].iloc[origin]
        spot = close[origin]
        y = close[origin + HORIZON]
        beta_fit, s2 = fit_har_v3(v, origin, horizon=HORIZON)
        dv = har_forecast_v3(v, origin, beta_fit, s2, horizon=HORIZON)
        sigma_h = np.sqrt(dv * HORIZON) * WIDTH_CAL
        carry_b = carry_log_h(PROFILE, date, Q_ANNUAL, HORIZON)
        sig_b = trailing_cc_vol(close, origin) * np.sqrt(HORIZON)
        b, nb, r2b, seb, src = beta_at(t, date)
        precomp.append(dict(ticker=t, origin_idx=origin, date=date, spot=spot, realized=y,
                             sigma_h=sigma_h, carry_b=carry_b, sig_b=sig_b,
                             beta=b, beta_n=nb, beta_r2=r2b, beta_se=seb, beta_src=src))
        origin += HORIZON

pre = pd.DataFrame(precomp)
print(f"Phase 1 done: {len(pre)} windows in {time.time()-t0:.1f}s")
n_dev = (pre['date'] < DEV_CUTOFF).sum(); n_final = (pre['date'] >= DEV_CUTOFF).sum()
print(f"DEV: {n_dev}  FINAL: {n_final}")
print(f"beta source counts:\n{pre['beta_src'].value_counts()}")
beta_by_name = pre.groupby('ticker')['beta'].mean().sort_values()
print(f"\nper-name mean beta (own-regression where usable, else 1.0 fallback):\n{beta_by_name.to_string()}")
pre.to_csv('/tmp/lab_arm4_precomp.csv', index=False)


# ---------------------------------------------------------------- Phase 2: sweep s (carry -> full Ke) x ERP basis
def run_variant(rows_df, s, rf_star, erp):
    out = []
    for _, r in rows_df.iterrows():
        ke_log_h = np.log1p(rf_star + r['beta'] * erp) * HORIZON / 252.0
        drift = r['carry_b'] + s * (ke_log_h - r['carry_b'])
        seed = SEED + int(r['origin_idx']) + hash(r['ticker']) % 1000
        samp = simulate_terminal_v3(r['spot'], r['sigma_h'], drift, nu=NU, n_paths=N_PATHS, seed=seed)
        rngb = np.random.default_rng(seed + 1)
        bench = r['spot'] * np.exp(r['carry_b'] + r['sig_b'] * rngb.standard_normal(N_PATHS))
        q_e = np.percentile(samp, [5, 25, 50, 75, 95]); q_b = np.percentile(bench, [5, 25, 50, 75, 95]); y = r['realized']
        out.append(dict(origin=r['date'], spot=r['spot'], realized=y, drift=drift, sigma_h=r['sigma_h'],
            crps=crps_sample(samp, y), crps_b=crps_sample(bench, y),
            pin50=0.5*abs(y-q_e[2]), pin50_b=0.5*abs(y-q_b[2]),
            wink=winkler(q_e[0], q_e[4], y), wink_b=winkler(q_b[0], q_b[4], y),
            pit=float(np.mean(samp <= y)),
            in50=q_e[1] <= y <= q_e[3], in80=np.percentile(samp,10) <= y <= np.percentile(samp,90), in90=q_e[0] <= y <= q_e[4],
            w90=(q_e[4]-q_e[0])/r['spot'], w90_b=(q_b[4]-q_b[0])/r['spot'], med_disp=(q_e[2]/r['spot']-1)))
    return pd.DataFrame(out)


dev_rows = pre[pre['date'] < DEV_CUTOFF].reset_index(drop=True)
results = []
t0 = time.time()
for basis, rf_star, erp in [('CDS', RF_STAR_CDS, ERP_CDS), ('rating', RF_STAR_RATING, ERP_RATING)]:
    for s in S_GRID:
        r = run_variant(dev_rows, s, rf_star, erp)
        sc, _ = pooled_scores([r])
        results.append(dict(basis=basis, s=s, **sc))
        print(f"  [{basis}] s={s:.2f}  crps_skill={sc['crps_skill']:+.4f}  cov90={sc['cov90']:.3f}  "
              f"pit={sc['pit_mean']:.3f}  w90_ratio={sc['w90_ratio']:.3f}  ({time.time()-t0:.0f}s)")

res_df = pd.DataFrame(results)
res_df.to_csv('/tmp/lab_arm4_dev_sweep.csv', index=False)
print("\n=== DEV sweep summary (CAPM beta x Damodaran ERP, blended with carry at weight s) ===")
print(res_df.to_string(index=False, float_format=lambda x: f'{x:8.4f}'))

# same-harness carry-only baseline for reference (s=0 rows above already equal this, sanity print anyway)
base_r = run_variant(dev_rows, 0.0, RF_STAR_CDS, ERP_CDS)
base_sc, _ = pooled_scores([base_r])
print(f"\ncarry-only baseline (s=0, same harness): {base_sc}")
print(f"\nTotal Phase-2 runtime: {time.time()-t0:.0f}s")
