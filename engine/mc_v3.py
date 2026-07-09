"""mc_v3.py — Testahil Monte Carlo engine v3 ("carry-anchored YZ-HAR-t").

Drift : carry anchor  ln(1+rf) - ln(1+q)  scaled to horizon (forward-consistent
        null for a PRICE forecast; rf from the MarketProfile schedule)
        + shrunk signal alpha  IC * sigma_H * sign * clip(z)  (dead zone 0.5,
        clip ±2, hard cap ±0.5*sigma_H), active per profile fallback rule.
Width : gap-aware Yang-Zhang proxy + pooled log-HAR (lags 1/5/22) forecasting
        mean forward daily variance, WITH the lognormal half-variance bias
        correction exp(s^2/2) and a 0.8/0.2 log-space shrink toward the
        trailing-252d proxy mean. Multiplied by a cross-fitted width_cal.
Shape : unit-variance Student-t(nu) via per-path chi-square mixture; nu fitted
        per market on pooled standardized 60d residuals (LONO cross-fitted),
        replacing the hard-coded t(5).
Bench : carry-anchored lognormal random walk, trailing 252d cc vol — the same
        carry as the engine, so skill isolates signal + width, never the anchor.
Gate  : pooled panel CRPS skill with a calendar-block bootstrap 90% CI ->
        PASS (CI>0) / PARITY (straddles 0) / FAIL (CI<0); pinball-0.5 and
        Winkler-90 skills reported alongside.
"""
import numpy as np
import pandas as pd
from mc_v2 import load_ohlc, yz_variance_proxy, crps_sample, winkler, trailing_cc_vol


# ---------------------------------------------------------------- width (HAR+)
def fit_har_v3(v, end_idx, horizon=60, min_obs=60):
    """log-HAR fit as in v2 but also returns residual variance s2 for the
    lognormal bias correction. Walk-forward safe (data up to end_idx only)."""
    from mc_v2 import har_features
    X, y = [], []
    vv = v.ffill()
    for t in range(22, end_idx - horizon):
        f = har_features(v, t)
        if f is None:
            continue
        fut = vv.iloc[t + 1:t + 1 + horizon]
        m = fut.mean()
        if np.isfinite(m) and m > 0:
            X.append(f); y.append(np.log(m))
    if len(y) < min_obs:
        return None, None
    Xd = np.column_stack([np.ones(len(y)), np.array(X)])
    ya = np.array(y)
    beta, *_ = np.linalg.lstsq(Xd, ya, rcond=None)
    resid = ya - Xd @ beta
    s2 = float(np.var(resid, ddof=Xd.shape[1]))
    return beta, s2


def har_forecast_v3(v, origin_idx, beta, s2, horizon=60,
                    shrink=0.8, bias_correct=True):
    """Bias-corrected, shrunk forecast of mean forward daily variance."""
    from mc_v2 import har_features
    w = v.ffill().iloc[max(0, origin_idx - 251):origin_idx + 1]
    v_trail = float(w.mean())
    f = har_features(v, origin_idx)
    if f is None or beta is None:
        return v_trail
    pred = beta[0] + beta[1:] @ f
    if bias_correct and s2 is not None:
        pred = pred + 0.5 * s2
    # 0.8/0.2 log-space shrink toward the trailing proxy mean (noise control)
    logv = shrink * pred + (1 - shrink) * np.log(max(v_trail, 1e-12))
    return float(np.exp(logv))


# ---------------------------------------------------------------- drift
def carry_log_h(profile, date, q_annual, horizon):
    rf = profile.carry_rate(date)
    return (np.log1p(rf) - np.log1p(q_annual)) * horizon / 252.0


def signal_z(close, idx, kind):
    """Standardized signal at origin idx (walk-forward safe)."""
    if kind is None or idx < 260:
        return 0.0
    lr = np.diff(np.log(close[max(0, idx - 251):idx + 1]))
    sd = np.std(lr, ddof=1)
    if not np.isfinite(sd) or sd <= 0:
        return 0.0
    if kind == "mom_12_1":
        if idx < 252:
            return 0.0
        r = np.log(close[idx - 21] / close[idx - 252])
        return float(r / (sd * np.sqrt(231)))
    if kind == "rev_1m":
        r = np.log(close[idx] / close[idx - 21])
        return float(r / (sd * np.sqrt(21)))
    return 0.0


def signal_alpha(profile, close, idx, sigma_h, dead=0.5, clipz=2.0):
    if not profile.signal_active or profile.signal_type is None:
        return 0.0, 0.0
    z = signal_z(close, idx, profile.signal_type)
    if abs(z) < dead:
        return 0.0, z
    a = profile.ic * sigma_h * profile.signal_sign * float(np.clip(z, -clipz, clipz))
    a = float(np.clip(a, -0.5 * sigma_h, 0.5 * sigma_h))
    return a, z


# ---------------------------------------------------------------- simulation
def simulate_terminal_v3(spot, sigma_h, drift_log_h, nu=8.0,
                         n_paths=50000, seed=42):
    rng = np.random.default_rng(seed)
    z = rng.standard_normal(n_paths)
    if nu is None or nu > 200:
        mix = 1.0
    else:
        chi = rng.chisquare(nu, n_paths)
        mix = np.sqrt((nu - 2) / chi)
    return spot * np.exp(drift_log_h + z * mix * sigma_h)


def simulate_paths_v3(spot, daily_var, horizon, drift_log_h, nu=8.0,
                      n_paths=50000, seed=42, width_cal=1.0):
    rng = np.random.default_rng(seed)
    sd = np.sqrt(daily_var) * width_cal
    z = rng.standard_normal((n_paths, horizon))
    if nu is None or nu > 200:
        mix = np.ones((n_paths, 1))
    else:
        chi = rng.chisquare(nu, n_paths)
        mix = np.sqrt((nu - 2) / chi)[:, None]
    incr = drift_log_h / horizon + z * mix * sd
    logp = np.cumsum(incr, axis=1)
    paths = np.empty((n_paths, horizon + 1))
    paths[:, 0] = spot
    paths[:, 1:] = spot * np.exp(logp)
    return paths


# ---------------------------------------------------------------- backtest
def backtest_v3(df, profile, horizon=60, q_annual=0.0, use_signal=True,
                nu=8.0, width_cal=1.0, n_paths=20000, seed=42,
                min_history=260, legacy_mode=None):
    """Walk-forward, non-overlapping. legacy_mode replicates v2 for the ladder:
      'v2_egx_dev' -> t5, zero carry, expanding-mean secular drift (old EGX dev)
      'v2_zero'    -> t5, zero carry, zero drift (old non-EGX)
    Benchmark is ALWAYS the carry-anchored trailing-vol lognormal RW (new null).
    """
    v = yz_variance_proxy(df)
    close = df['Price'].values
    n = len(df)
    rows = []
    origin = min_history
    while origin + horizon < n:
        date = df['Date'].iloc[origin]
        spot = close[origin]
        y = close[origin + horizon]

        # --- engine drift & width per rung ---
        if legacy_mode is not None:
            from mc_v2 import fit_har, har_forecast_daily_var
            beta = fit_har(v, origin, horizon=horizon)
            dv = har_forecast_daily_var(v, origin, beta, horizon=horizon)
            sigma_h = np.sqrt(dv * horizon)
            if legacy_mode == 'v2_egx_dev':
                drift = float(np.mean(np.diff(np.log(close[:origin + 1])))) * horizon
            else:
                drift = 0.0
            nu_use, z = 5.0, 0.0
            alpha = 0.0
        else:
            beta, s2 = fit_har_v3(v, origin, horizon=horizon)
            dv = har_forecast_v3(v, origin, beta, s2, horizon=horizon)
            sigma_h = np.sqrt(dv * horizon) * width_cal
            carry = carry_log_h(profile, date, q_annual, horizon)
            alpha, z = (signal_alpha(profile, close, origin, sigma_h)
                        if use_signal else (0.0, signal_z(close, origin, profile.signal_type)))
            drift = carry + alpha
            nu_use = nu

        samp = simulate_terminal_v3(spot, sigma_h, drift, nu=nu_use,
                                    n_paths=n_paths, seed=seed + origin)

        # --- carry-anchored benchmark (fixed null across all rungs) ---
        carry_b = carry_log_h(profile, date, q_annual, horizon)
        sig_b = trailing_cc_vol(close, origin) * np.sqrt(horizon)
        rngb = np.random.default_rng(seed + origin + 1)
        bench = spot * np.exp(carry_b + sig_b * rngb.standard_normal(n_paths))

        q_e = np.percentile(samp, [5, 25, 50, 75, 95])
        q_b = np.percentile(bench, [5, 25, 50, 75, 95])
        rows.append(dict(
            origin=date, spot=spot, realized=y, z=z, alpha=alpha,
            drift=drift, sigma_h=sigma_h,
            crps=crps_sample(samp, y), crps_b=crps_sample(bench, y),
            pin50=0.5 * abs(y - q_e[2]), pin50_b=0.5 * abs(y - q_b[2]),
            wink=winkler(q_e[0], q_e[4], y), wink_b=winkler(q_b[0], q_b[4], y),
            pit=float(np.mean(samp <= y)),
            in50=q_e[1] <= y <= q_e[3], in80=np.percentile(samp, 10) <= y <= np.percentile(samp, 90),
            in90=q_e[0] <= y <= q_e[4],
            w90=(q_e[4] - q_e[0]) / spot, w90_b=(q_b[4] - q_b[0]) / spot,
            med_disp=(q_e[2] / spot - 1),
            u=(np.log(y / spot) - drift) / sigma_h if sigma_h > 0 else np.nan,
        ))
        origin += horizon
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- pooled gate
def pooled_scores(frames):
    r = pd.concat(frames, ignore_index=True)
    out = dict(
        n=len(r),
        crps_skill=1 - r['crps'].sum() / r['crps_b'].sum(),
        pin50_skill=1 - r['pin50'].sum() / r['pin50_b'].sum(),
        wink_skill=1 - r['wink'].sum() / r['wink_b'].sum(),
        cov50=r['in50'].mean(), cov80=r['in80'].mean(), cov90=r['in90'].mean(),
        pit_mean=r['pit'].mean(),
        w90_ratio=(r['w90'] / r['w90_b']).mean(),
        med_abs_disp=r['med_disp'].abs().mean(),
    )
    return out, r


def block_bootstrap_ci(r, B=3000, seed=0, block='6M', level=90):
    """Calendar-block bootstrap of pooled CRPS skill: resample half-year blocks
    jointly across names (preserves cross-sectional dependence)."""
    rng = np.random.default_rng(seed)
    blk = pd.PeriodIndex(pd.DatetimeIndex(r['origin']), freq=block.replace('M', 'M'))
    r = r.assign(_blk=pd.DatetimeIndex(r['origin']).to_period('2Q').astype(str))
    blocks = r['_blk'].unique()
    nb = len(blocks)
    g = {b: r[r['_blk'] == b] for b in blocks}
    bs = []
    for _ in range(B):
        pick = rng.choice(blocks, nb, replace=True)
        c = sum(g[b]['crps'].sum() for b in pick)
        cb = sum(g[b]['crps_b'].sum() for b in pick)
        bs.append(1 - c / cb)
    bs = np.array(bs)
    lo, hi = np.percentile(bs, [(100 - level) / 2, 100 - (100 - level) / 2])
    return float(lo), float(hi), float(np.mean(bs > 0))


def verdict(lo, hi):
    if lo > 0:
        return "PASS"
    if hi < 0:
        return "FAIL"
    return "PARITY"


# ---------------------------------------------------------------- shape fit
def fit_nu_scale(u, nu_grid=(4, 5, 6, 8, 10, 12, 15, 20, 30, 1e9),
                 s_grid=np.linspace(0.75, 1.40, 66)):
    """MLE over (nu, scale) for standardized 60d residuals u; unit-variance
    t(nu) parameterization (scale multiplies the unit-variance t)."""
    from scipy import stats
    u = np.asarray(u, float)
    u = u[np.isfinite(u)]
    best = (-np.inf, 8.0, 1.0)
    for nu in nu_grid:
        if nu > 200:
            for s in s_grid:
                ll = stats.norm.logpdf(u / s).sum() - len(u) * np.log(s)
                if ll > best[0]:
                    best = (ll, float(nu), float(s))
        else:
            k = np.sqrt(nu / (nu - 2))  # unit-variance t: x = t_nu / k
            for s in s_grid:
                ll = stats.t.logpdf(u * k / s, nu).sum() + len(u) * (np.log(k) - np.log(s))
                if ll > best[0]:
                    best = (ll, float(nu), float(s))
    return best[1], best[2]


def shrink_cal(s, w=0.7, lo=0.85, hi=1.30):
    return float(np.clip(1 + w * (s - 1), lo, hi))
