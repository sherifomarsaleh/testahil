"""
engine/history_span.py — adaptive per-name HAR-lookback selection.

Objective (Sherif, 29-Jul-2026): keep all history on disk always (never
truncate the raw library), but let each NAME choose, on the evidence, how
much of its own trailing history actually feeds the HAR variance forecast.
Some names are hurt by deep history (regime drift); some are helped or
indifferent. This replaces a single global "use everything" default with
a per-name, re-testable choice.

Selection rule, directly restating the standing OVERRIDING AIM:
    Better drift prediction and SMALLER cone size, WITHOUT compromising
    accuracy. Narrower bought with worse calibration is not progress.

So: among candidate spans whose skill is not robustly worse than the best
candidate (bootstrap CI over blocks {2,3,4} does not clear zero against it),
pick the one with the smallest mean cone width. If none of the shorter
candidates clears that bar, "unlimited" (all available history) wins by
default -- the same null-is-a-real-result posture as the 28-Jul test.

This module does not hardcode per-name decisions. `recommend()` is meant
to be re-run at every library ingest, per the standing rule: "Run the span
test on every market, at every library ingest, and record the verdict --
including the nulls." A precomputed table (history_span_overrides.json) is
a CACHE of the last run, not the source of truth -- same relationship as
fitted_configs.json to market_profiles.py.
"""
from __future__ import annotations
import numpy as np
import pandas as pd

CANDIDATE_YEARS = (2, 3, 5, 7, 10, None)   # None = unlimited (all available)
MIN_HISTORY = 260     # sessions of trailing data required before an origin counts
MIN_WINDOWS = 8        # below this, a span can't be evaluated at all -- too few origins


def _feature_matrix(v: pd.Series):
    """Vectorized log-HAR features (v1, v5, v22), identical in value to
    mc_v3.har_features called at every index -- verified bit-for-bit
    against the production function before this module was adopted."""
    vv = v.ffill()
    a = vv.values.astype(float)
    s = pd.Series(a)
    v1 = a.copy()
    v5 = s.rolling(5).mean().values
    v22 = s.rolling(22).mean().values
    F = np.column_stack([v1, v5, v22])
    ok = np.isfinite(F).all(1) & (F.min(1) > 0)
    ok[:22] = False
    with np.errstate(divide="ignore", invalid="ignore"):
        logF = np.log(F)
    return logF, ok, a


def _fit_window(logF, ok, a, dates, end_idx, horizon, lookback_years, min_obs=60):
    """log-HAR fit restricted to a ROLLING trailing window ending at end_idx.

    Per the standing rule: 'The lookback is a rolling trailing window, not
    a fixed start date. A fixed start is a break filter and it silently
    lengthens as the calendar advances.' lookback_years=None means all
    history up to end_idx (the current, unrestricted default)."""
    if lookback_years is None:
        train_lo = 0
    else:
        cutoff = dates.iloc[end_idx] - pd.DateOffset(years=lookback_years)
        train_lo = int(dates.searchsorted(cutoff, side="left"))
    hi = end_idx - horizon
    lo = max(22, train_lo + 22)
    if hi <= lo:
        return None, None
    ts = np.arange(lo, hi)
    ts = ts[ok[ts]]
    if len(ts) == 0:
        return None, None
    csum = np.concatenate([[0.0], np.nancumsum(a)])
    starts = ts + 1
    ends = np.minimum(ts + 1 + horizon, len(a))
    means = (csum[ends] - csum[starts]) / np.maximum(ends - starts, 1)
    good = np.isfinite(means) & (means > 0)
    ts, means = ts[good], means[good]
    if len(ts) < min_obs:
        return None, None
    X = np.column_stack([np.ones(len(ts)), logF[ts]])
    y = np.log(means)
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    return beta, float(np.var(resid, ddof=X.shape[1]))


def _forecast(logF, ok, a, origin_idx, beta, s2, shrink=0.8):
    lo = max(0, origin_idx - 251)
    v_trail = float(np.nanmean(a[lo:origin_idx + 1]))
    if beta is None or not ok[origin_idx]:
        return v_trail
    pred = beta[0] + beta[1:] @ logF[origin_idx]
    if s2 is not None:
        pred = pred + 0.5 * s2
    logv = shrink * pred + (1 - shrink) * np.log(max(v_trail, 1e-12))
    return float(np.exp(logv))


def _block_ci(d, block, n_boot=4000, seed=42, alpha=0.10):
    rng = np.random.default_rng(seed)
    n = len(d)
    if n < block + 2:
        return (np.nan, np.nan)
    nblk = int(np.ceil(n / block))
    starts = np.arange(n - block + 1)
    out = np.empty(n_boot)
    for b in range(n_boot):
        idx = rng.choice(starts, nblk)
        samp = np.concatenate([d[s:s + block] for s in idx])[:n]
        out[b] = samp.mean()
    return np.percentile(out, [100 * alpha / 2, 100 * (1 - alpha / 2)])


def evaluate_span(df, nu, width_cal, carry_fn, years, horizon=60,
                   n_paths=20000, seed=42, origin_start=None):
    """Walk-forward score for ONE candidate span, using a ROLLING lookback.
    `years=None` means unlimited (all history up to each origin).
    `origin_start` must be passed by the caller and held FIXED across every
    candidate in a comparison -- origins never depend on which span is being
    tested, only the training window at each origin does. Returns a dict of
    skill/width/coverage, or None if there isn't enough data at all."""
    from mc_v2 import yz_variance_proxy, crps_sample, trailing_cc_vol
    from mc_v3 import simulate_terminal_v3

    dates = pd.to_datetime(df["Date"])
    close = df["Price"].values
    n = len(df)
    v = yz_variance_proxy(df)
    logF, ok, a = _feature_matrix(v)

    start = MIN_HISTORY if origin_start is None else origin_start
    rows = []
    origin = start
    while origin + horizon < n:
        date = df["Date"].iloc[origin]
        spot, y = close[origin], close[origin + horizon]
        beta, s2 = _fit_window(logF, ok, a, dates, origin, horizon, years)
        dv = _forecast(logF, ok, a, origin, beta, s2)
        sigma_h = np.sqrt(dv * horizon) * width_cal
        carry = carry_fn(date, horizon)
        sig_b = trailing_cc_vol(close, origin) * np.sqrt(horizon)
        rngb = np.random.default_rng(seed + origin + 1)
        bench = spot * np.exp(carry + sig_b * rngb.standard_normal(n_paths))
        samp = simulate_terminal_v3(spot, sigma_h, carry, nu=nu,
                                    n_paths=n_paths, seed=seed + origin)
        q = np.percentile(samp, [5, 10, 25, 50, 75, 90, 95])
        rows.append(dict(
            crps=crps_sample(samp, y), crps_b=crps_sample(bench, y),
            in90=q[0] <= y <= q[6], w90=(q[6] - q[0]) / spot, spot=spot,
        ))
        origin += horizon

    if len(rows) < MIN_WINDOWS:
        return None
    out = pd.DataFrame(rows)
    return dict(
        years="unlimited" if years is None else years,
        n=len(out),
        skill=1 - (out.crps / out.spot).sum() / (out.crps_b / out.spot).sum(),
        width_pct=out.w90.mean() * 100,
        coverage_pct=out.in90.mean() * 100,
        crps_n=(out.crps / out.spot).values,   # kept for pairwise bootstrap
    )


def recommend(df, nu, width_cal, carry_fn, horizon=60,
              candidates=CANDIDATE_YEARS, materiality_floor=0.005):
    """Evaluate every candidate span and pick the best per the standing
    rule. Returns (chosen, evidence) -- evidence is every candidate's
    result, so the choice is always auditable, never a bare number."""
    results = {}
    for yrs in candidates:
        r = evaluate_span(df, nu, width_cal, carry_fn, yrs, horizon=horizon,
                          origin_start=MIN_HISTORY)
        if r is not None:
            results[r["years"]] = r
    if not results:
        return "unlimited", {}

    if "unlimited" not in results:
        # can't even evaluate the null -- not enough data to choose; default safe
        best = min(results, key=lambda k: 0 if k == "unlimited" else 1)
        return best, results

    base = results["unlimited"]
    candidates_ok = {"unlimited": base}
    for yrs, r in results.items():
        if yrs == "unlimited":
            continue
        # paired diff vs unlimited on shared window count (truncate to min length)
        n = min(len(r["crps_n"]), len(base["crps_n"]))
        d = base["crps_n"][-n:] - r["crps_n"][-n:]   # positive = shorter span better
        robust_ok = True
        for blk in (2, 3, 4):
            lo, hi = _block_ci(d, blk)
            if np.isnan(lo):
                continue
            if hi < 0:          # shorter span is ROBUSTLY WORSE on skill -> reject it
                robust_ok = False
                break
        if robust_ok:
            candidates_ok[yrs] = r

    # among candidates that don't robustly lose on skill, pick smallest width,
    # subject to the materiality floor actually mattering
    chosen = min(candidates_ok, key=lambda k: candidates_ok[k]["width_pct"])
    if chosen != "unlimited":
        move = (candidates_ok[chosen]["width_pct"] / base["width_pct"]) - 1
        if abs(move) < materiality_floor * 100:
            chosen = "unlimited"   # too small a difference to bother
    return chosen, results
