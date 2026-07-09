"""
Testahil — Monte Carlo engine v2 ("YZ-HAR").

Drop-in for monte_carlo.run: same call signature, same MCResult output, same factor
semantics. Three changes vs v1, per the Standing Research Protocol:

  WIDTH  — a pooled log-HAR cascade (variance lags 1 / 5 / 22) projecting the AVERAGE daily
           variance over the next `horizon` sessions, built on a gap-aware Yang-Zhang variance
           proxy (overnight-return squared + Rogers-Satchell from the OHLC). Regime-conditional
           by construction: tight in calm tape, wide in storm. The old x1.15 / x1.30 kvol floor
           is retired (it over-covered and cost CRPS). If no OHLC is supplied, falls back to the
           flat annualized `realized_vol` passed in (so it is still a valid drop-in).

  SHAPE  — unit-variance Student-t(5) innovations, implemented as a per-PATH chi-square variance
           mixture on the Gaussian diffusion so the `horizon`-day AGGREGATE is exactly
           unit-variance t5. (Independent daily t-draws would CLT back to Gaussian and lose the
           tails; one shared chi-square scale per path preserves the t-structure of the sum.)
           Tighter interquartile body, honest tails.

  DRIFT  — asset-class-conditional. Secular drift (the expanding-window mean daily log-return of
           the name's OWN history) is ON for EGX developers (a genuine 5-yr secular uptrend) and
           OFF (zero) for international names and metals — a confident trend drift breaks at a
           regime turn. The 16 factors layer on top of this diffusion unchanged, and the §1
           fundamental value gap never enters the drift (lens independence).

Outputs are identical to v1 (MCResult), so viz.py / ledger_scorer.py / study_runner consume it
unchanged. `run(...)` accepts the same positional args as monte_carlo.run plus optional keyword
args (ohlc, asset_class, secular_drift_daily, enable_secular_drift, nu).
"""
from __future__ import annotations
from typing import Optional, Sequence
import numpy as np

from monte_carlo import MCResult, TRADING_DAYS  # reuse the identical output type

# EGX developers are the only class carrying secular drift (see protocol / factor_library).
_SECULAR_DRIFT_CLASSES = {"egx_developer"}


# --------------------------------------------------------------------------- Yang-Zhang proxy
def yang_zhang_daily_var(open_, high, low, close) -> np.ndarray:
    """
    Gap-aware daily variance proxy = overnight-return^2 + Rogers-Satchell intraday term.

    Rogers-Satchell is drift-independent, so the proxy captures both the close-to-open gap and the
    intraday range without assuming zero drift. Returns a length-(n-1) series (needs prior close).
    """
    o = np.asarray(open_, float); h = np.asarray(high, float)
    l = np.asarray(low, float);   c = np.asarray(close, float)
    c_prev = c[:-1]
    o_, h_, l_, c_ = o[1:], h[1:], l[1:], c[1:]
    overnight = np.log(o_ / c_prev)
    rs = (np.log(h_ / c_) * np.log(h_ / o_) + np.log(l_ / c_) * np.log(l_ / o_))
    v = overnight ** 2 + rs
    return np.clip(v, 1e-8, None)  # positivity for the log-HAR fit


# --------------------------------------------------------------------------- pooled log-HAR
def har_project_daily_var(v: np.ndarray, horizon: int = 60):
    """
    Pooled log-HAR (variance components 1/5/22) projecting the AVERAGE daily variance over the next
    `horizon` sessions. Returns (avg_daily_var, beta).

    Uses a DIRECT h-step regression — the target is the realized average daily variance over the
    next `horizon` days, regressed on today's daily / weekly / monthly log-variance components — so
    there is no forward iteration to compound bias, and a Jensen correction (+0.5 * residual
    variance) converts the log-space fit from a median to a mean. Falls back to the sample mean of
    the proxy when history is too short for the direct fit.
    """
    v = np.asarray(v, float)
    n = len(v)
    if n < 22 + horizon + 10:
        return float(np.mean(v)), None

    # HAR components (inclusive of today t): daily = v[t], weekly = mean last 5, monthly = mean 22
    w = np.array([v[max(0, t - 4):t + 1].mean() for t in range(n)])
    m = np.array([v[max(0, t - 21):t + 1].mean() for t in range(n)])

    X, Y = [], []
    for t in range(22, n - horizon):                         # direct h-step target
        X.append([1.0, np.log(v[t]), np.log(w[t]), np.log(m[t])])
        Y.append(np.log(v[t + 1:t + 1 + horizon].mean()))
    X = np.array(X); Y = np.array(Y)
    beta, *_ = np.linalg.lstsq(X, Y, rcond=None)
    resid_var = float((Y - X @ beta).var())

    xT = np.array([1.0, np.log(v[-1]), np.log(w[-1]), np.log(m[-1])])
    avg_daily_var = float(np.exp(xT @ beta + 0.5 * resid_var))  # Jensen: median -> mean
    return avg_daily_var, beta


def har_annualized_sigma(open_, high, low, close, horizon: int = 60) -> float:
    """Convenience: OHLC -> annualized diffusion sigma the HAR projects for the horizon."""
    v = yang_zhang_daily_var(open_, high, low, close)
    avg_daily_var, _ = har_project_daily_var(v, horizon)
    return float(np.sqrt(avg_daily_var * TRADING_DAYS))


# --------------------------------------------------------------------------- the engine
def run(
    anchor: float,
    realized_vol: float,                 # annualized fallback if `ohlc` is None
    continuous,                          # list[factor_library.Factor] tier 'C'
    events,                             # list[factor_library.Factor] tier 'M'/'E'
    horizon: int = 60,
    n_paths: int = 50_000,
    seed: int = 42,
    vol_floor: float = 0.05,
    *,
    ohlc: Optional[dict] = None,         # {'open':..,'high':..,'low':..,'close':..} for YZ-HAR width
    asset_class: Optional[str] = None,   # drives the secular-drift switch
    secular_drift_daily: Optional[float] = None,  # explicit override (per-day log-return)
    enable_secular_drift: Optional[bool] = None,  # override the class default
    nu: int = 5,                        # Student-t degrees of freedom
) -> MCResult:
    rng = np.random.default_rng(seed)

    # ---- WIDTH: YZ-HAR projected sigma if OHLC given, else flat realized_vol -------------
    if ohlc is not None:
        sigma = har_annualized_sigma(ohlc["open"], ohlc["high"], ohlc["low"], ohlc["close"], horizon)
    else:
        sigma = float(realized_vol)
    sigma = max(sigma, vol_floor)
    daily_var = (sigma ** 2) / TRADING_DAYS
    daily_sigma = np.sqrt(daily_var)

    # ---- DRIFT: asset-class-conditional secular drift + factor drift ----------------------
    if enable_secular_drift is None:
        enable_secular_drift = (asset_class in _SECULAR_DRIFT_CLASSES)
    if secular_drift_daily is None:
        if enable_secular_drift and ohlc is not None:
            c = np.asarray(ohlc["close"], float)
            secular_drift_daily = float(np.mean(np.diff(np.log(c))))  # expanding-window mean
        else:
            secular_drift_daily = 0.0
    if not enable_secular_drift:
        secular_drift_daily = 0.0

    net_drift_3m = float(sum((f.drift_3m or 0.0) for f in continuous))
    factor_daily_drift = np.log1p(net_drift_3m) / horizon
    daily_drift = secular_drift_daily + factor_daily_drift

    # ---- SHAPE: unit-variance t5 via one shared chi-square scale per path -----------------
    # base Gaussian sigma s0 chosen so that after the per-path scale g the realized daily
    # variance equals daily_var:  Var(g * s0 * Z) = (nu/(nu-2)) * s0^2 = daily_var.
    s0 = daily_sigma * np.sqrt((nu - 2) / nu)
    Z = rng.standard_normal((n_paths, horizon))
    W = rng.chisquare(nu, size=n_paths)          # ONE per path -> preserves t5 in the aggregate
    g = np.sqrt(nu / W)[:, None]
    # lognormal drift correction uses the realized per-day variance (daily_var)
    log_incr = (daily_drift - 0.5 * daily_var) + g * s0 * Z
    log_paths = np.concatenate([np.zeros((n_paths, 1)), np.cumsum(log_incr, axis=1)], axis=1)

    # ---- discrete events: identical semantics to v1 (level shift from a random session) ---
    for f in events:
        if not f.prob:
            continue
        hit = rng.random(n_paths) < f.prob
        k = int(hit.sum())
        if k == 0:
            continue
        impacts = rng.normal(f.impact_mean or 0.0, f.impact_spread or 0.0, size=k)
        days = rng.integers(1, horizon + 1, size=k)
        log_impacts = np.log1p(np.clip(impacts, -0.95, None))
        idx = np.where(hit)[0]
        for j, p_idx in enumerate(idx):
            log_paths[p_idx, days[j]:] += log_impacts[j]

    paths = anchor * np.exp(log_paths)
    dlr = np.diff(np.log(paths), axis=1)
    ann_path_vol = float(dlr.std() * np.sqrt(TRADING_DAYS))

    return MCResult(anchor, horizon, n_paths, seed, paths, sigma, ann_path_vol, net_drift_3m)


def expected_factor_contribution(continuous, events) -> float:
    """Net expected 3M contribution = sum(C drifts) + sum(prob*impact_mean). Same as v1."""
    c = sum((f.drift_3m or 0.0) for f in continuous)
    e = sum((f.prob or 0.0) * (f.impact_mean or 0.0) for f in events)
    return c + e
