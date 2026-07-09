"""mc_v2.py — Testahil YZ-HAR Monte Carlo engine (v2).
Width : pooled log-HAR cascade (variance lags 1/5/22) on a gap-aware
        Yang-Zhang variance proxy (overnight^2 + Rogers-Satchell),
        projecting the average daily variance over the next H sessions.
Shape : unit-variance Student-t(5) via a per-path chi-square variance
        mixture on the Gaussian diffusion (60-day aggregate exactly t5).
Drift : asset-class-conditional — expanding-window mean daily log-return
        (secular) when enabled; zero otherwise. No kvol floor.
"""
import numpy as np
import pandas as pd


def load_ohlc(path):
    df = pd.read_csv(path)
    df.columns = [c.replace('\ufeff', '').strip() for c in df.columns]
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
    df = df.sort_values('Date').reset_index(drop=True)
    for c in ['Price', 'Open', 'High', 'Low']:
        df[c] = pd.to_numeric(df[c].astype(str).str.replace(',', ''), errors='coerce')
    df = df.dropna(subset=['Price', 'Open', 'High', 'Low']).reset_index(drop=True)
    return df


def yz_variance_proxy(df):
    """Gap-aware daily variance proxy: overnight-return^2 + Rogers-Satchell."""
    o, h, l, c = df['Open'].values, df['High'].values, df['Low'].values, df['Price'].values
    c_prev = np.roll(c, 1)
    with np.errstate(divide='ignore', invalid='ignore'):
        overnight = np.log(o / c_prev)
        rs = np.log(h / c) * np.log(h / o) + np.log(l / c) * np.log(l / o)
    v = overnight ** 2 + rs
    v[0] = np.nan
    v = np.where(v <= 0, np.nan, v)  # guard degenerate bars
    return pd.Series(v, index=df.index)


def har_features(v, idx):
    """log variance averages at lags 1 / 5 / 22 ending at idx (inclusive)."""
    if idx < 22:
        return None
    w = v.iloc[:idx + 1].ffill()
    v1 = w.iloc[-1]
    v5 = w.iloc[-5:].mean()
    v22 = w.iloc[-22:].mean()
    if not np.all(np.isfinite([v1, v5, v22])) or min(v1, v5, v22) <= 0:
        return None
    return np.log([v1, v5, v22])


def fit_har(v, end_idx, horizon=60, min_obs=60):
    """Fit log-HAR: log(mean var over next `horizon` d) ~ log v1,v5,v22.
    Uses only data up to end_idx (walk-forward safe)."""
    X, y = [], []
    vv = v.ffill()
    for t in range(22, end_idx - horizon):
        f = har_features(v, t)
        if f is None:
            continue
        fut = vv.iloc[t + 1:t + 1 + horizon]
        m = fut.mean()
        if np.isfinite(m) and m > 0:
            X.append(f)
            y.append(np.log(m))
    if len(y) < min_obs:
        return None
    X = np.column_stack([np.ones(len(y)), np.array(X)])
    beta, *_ = np.linalg.lstsq(X, np.array(y), rcond=None)
    return beta


def har_forecast_daily_var(v, origin_idx, beta, horizon=60):
    f = har_features(v, origin_idx)
    if f is None or beta is None:
        w = v.ffill().iloc[max(0, origin_idx - 251):origin_idx + 1]
        return float(w.mean())
    return float(np.exp(beta[0] + beta[1:] @ f))


def simulate_terminal(spot, daily_var, horizon, drift_daily=0.0,
                      n_paths=50000, seed=42, nu=5):
    """Terminal-price distribution at T+horizon under the YZ-HAR width,
    unit-variance t(nu) shape (per-path chi-square mixture), given drift."""
    rng = np.random.default_rng(seed)
    sigma_h = np.sqrt(daily_var * horizon)
    z = rng.standard_normal(n_paths)
    chi = rng.chisquare(nu, n_paths)
    mix = np.sqrt((nu - 2) / chi)          # unit-variance t(nu) multiplier
    shocks = z * mix * sigma_h
    logret = drift_daily * horizon + shocks
    return spot * np.exp(logret)


def simulate_paths(spot, daily_var, horizon, drift_daily=0.0,
                   n_paths=50000, seed=42, nu=5):
    """Full path array (n_paths, horizon+1) for fan charts / touch ladders."""
    rng = np.random.default_rng(seed)
    sd = np.sqrt(daily_var)
    z = rng.standard_normal((n_paths, horizon))
    chi = rng.chisquare(nu, n_paths)
    mix = np.sqrt((nu - 2) / chi)[:, None]
    incr = drift_daily + z * mix * sd
    logp = np.cumsum(incr, axis=1)
    paths = np.empty((n_paths, horizon + 1))
    paths[:, 0] = spot
    paths[:, 1:] = spot * np.exp(logp)
    return paths


def crps_sample(samples, y):
    """Sample CRPS: E|X−y| − 0.5·E|X−X'| (unbiased pairwise form)."""
    s = np.sort(np.asarray(samples, dtype=float))
    n = len(s)
    t1 = np.mean(np.abs(s - y))
    i = np.arange(1, n + 1)
    t2 = 2.0 / (n * n) * np.sum((2 * i - n - 1) * s)
    return t1 - 0.5 * t2


def winkler(lo, hi, y, alpha=0.10):
    w = hi - lo
    if y < lo:
        w += 2.0 / alpha * (lo - y)
    elif y > hi:
        w += 2.0 / alpha * (y - hi)
    return w


def trailing_cc_vol(close, idx, window=252):
    lr = np.diff(np.log(close[max(0, idx - window):idx + 1]))
    return float(np.std(lr, ddof=1))


def backtest(df, horizon=60, step=None, secular_drift=False,
             n_paths=8000, seed=42, min_history=260):
    """Walk-forward Step 0 backtest. Non-overlapping when step=horizon."""
    if step is None:
        step = horizon
    v = yz_variance_proxy(df)
    close = df['Price'].values
    n = len(df)
    rows = []
    origin = min_history
    while origin + horizon < n:
        beta = fit_har(v, origin, horizon=horizon)
        dv = har_forecast_daily_var(v, origin, beta, horizon=horizon)
        spot = close[origin]
        drift = 0.0
        if secular_drift:
            lr = np.diff(np.log(close[:origin + 1]))
            drift = float(np.mean(lr))
        samp = simulate_terminal(spot, dv, horizon, drift_daily=drift,
                                 n_paths=n_paths, seed=seed + origin)
        y = close[origin + horizon]
        # benchmark: zero-drift lognormal random walk, trailing cc vol
        sig_b = trailing_cc_vol(close, origin)
        rngb = np.random.default_rng(seed + origin + 1)
        bench = spot * np.exp(sig_b * np.sqrt(horizon) * rngb.standard_normal(n_paths))
        q = np.percentile(samp, [5, 10, 25, 50, 75, 90, 95])
        qb = np.percentile(bench, [5, 95])
        pit = float(np.mean(samp <= y))
        rows.append(dict(
            origin=df['Date'].iloc[origin], spot=spot, realized=y,
            crps=crps_sample(samp, y), crps_bench=crps_sample(bench, y),
            wink=winkler(q[0], q[6], y), wink_bench=winkler(qb[0], qb[1], y),
            pit=pit,
            in50=q[2] <= y <= q[4], in80=q[1] <= y <= q[5], in90=q[0] <= y <= q[6],
            p5=q[0], p25=q[2], p50=q[3], p75=q[4], p95=q[6],
            anchor_vol=np.sqrt(dv * 252), drift_daily=drift,
        ))
        origin += step
    r = pd.DataFrame(rows)
    if len(r) == 0:
        return r, {}
    skill = 1 - r['crps'].sum() / r['crps_bench'].sum()
    iskill = 1 - r['wink'].sum() / r['wink_bench'].sum()
    summary = dict(n=len(r), crps_skill=skill, interval_skill=iskill,
                   cov50=r['in50'].mean(), cov80=r['in80'].mean(),
                   cov90=r['in90'].mean(), pit_mean=r['pit'].mean())
    return r, summary
