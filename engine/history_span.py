"""history_span.py — is more history actually better? Test it, never assume it.

STANDING PRINCIPLE (user, 28-Jul-2026): history is INSTRUMENTAL. It is kept for
exactly two reasons — a tighter cone and a better-centred drift, at unchanged
accuracy. History that does not earn its place on those terms is not used. A
longer library is not a virtue; it is a hypothesis, and it goes through the same
out-of-sample promotion rule as every other engine parameter.

WHAT THIS MODULE ISOLATES
-------------------------
Two different levers get called "history" and conflating them produces nonsense:

  calibration sample   WHICH WINDOWS train (nu, width_cal). Governed by
                       `breaks` + apply_breaks. Already tested (EG, 26-Jul).

  HAR lookback         HOW MUCH PAST each per-origin variance forecast may see.
                       NOT break-aware, never tested, and it is what actually
                       sets the width of a cone struck today. <-- THIS MODULE

The lever here is a ROLLING TRAILING WINDOW, not a fixed start date. A fixed
start is a break filter and it silently lengthens as the calendar advances: a
"2011+" rule means 5 years of lookback in 2016 and 15 in 2026, so it can never
be a stationary description of how much past the model should weigh. A trailing
K-year window is the same object at every origin, which is the only form in
which "the span that gives the best results" is a well-posed question.

HOW IT IS SCORED — and why not simply "narrowest wins"
------------------------------------------------------
Narrowness alone is trivially gamed: divide every cone by two and sharpness
improves right up until coverage collapses. The objective is therefore CRPS,
which is a PROPER scoring rule — it is already, by construction, "sharpness
subject to calibration", and it cannot be improved by a cone that is narrow in
the wrong place. Sharpness (mean 90% width) and coverage are reported alongside
as diagnostics, never as the selection criterion.

Every candidate is scored on THE SAME ORIGINS against THE SAME benchmark (the
carry-anchored trailing-vol lognormal RW). Only the HAR training set differs.

THE GUARD (why this is not the rejected CRPS-selection idea)
------------------------------------------------------------
The house has already been burned selecting a parameter by maximising skill:
choosing (nu, width_cal) by CRPS grid search beat MLE in-sample and LOST under
LONO. REJECTED, do-not-revive. Selecting a lookback by CRPS is the same class of
move, so it carries the same guard and is not adopted without all of it:

  1. held-out / cross-fitted scoring, never in-sample
  2. the winner must hold across bootstrap block sizes {2,3,4}
  3. a drop-one-name jackknife must not flip it
  4. 80/90% coverage and PIT centring must not degrade
  5. the change must clear the 5% materiality gate to move a live cone

A candidate that wins on skill while coverage falls is REJECTED — that is
buying narrowness with accuracy, which is the one trade this explicitly forbids.
"""

# TESTAHIL OVERRIDING AIM (user, standing — supersedes every mechanic in this file)
#
#     BETTER DRIFT PREDICTION AND SMALLER CONE SIZE WITHOUT COMPROMISING THE
#     ACCURACY. IF THE ACCURACY IS COMPROMISED THEN STICK TO THE TIME SPAN THAT
#     OFFERS THE BEST RESULTS.
#
# Every parameter, span, fit and gate in this engine exists to serve that sentence.
# Where a mechanic and the aim disagree, the AIM WINS and the mechanic is fixed.
#
# The aim carries its own guard: "smaller cone" and "without compromising accuracy"
# are a PAIR. A narrower cone bought with coverage is not progress — it is the same
# forecast with the uncertainty hidden. So every candidate is tested on both halves
# at once: does it narrow the cone, AND does calibration hold (CRPS, 80/90%
# coverage, PIT centring, std_u toward 1.0)? Narrower with coverage intact ->
# adopt. Narrower with coverage slipping -> REJECT. Neither -> keep whatever span
# performs best.

from __future__ import annotations

import os
import sys
import warnings

warnings.filterwarnings('ignore')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np                                        # noqa: E402
import pandas as pd                                       # noqa: E402

from data_quality import clean_ohlc                       # noqa: E402
from mc_v2 import (load_ohlc, yz_variance_proxy, har_features,  # noqa: E402
                   crps_sample, trailing_cc_vol)
from mc_v3 import (har_forecast_v3, carry_log_h, simulate_terminal_v3,  # noqa: E402
                   calendar_horizons, block_bootstrap_ci, verdict)
import market_profiles as MP                              # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, 'raw_ohlc')
SESSIONS_PER_YEAR = 250

# Candidate trailing lookbacks, in years. None = unlimited (today's behaviour).
CANDIDATES = (3.0, 5.0, 7.0, 10.0, None)


def har_design(v, horizon):
    """Cache the HAR design matrix ONCE per (series, horizon).

    The naive implementation recomputes har_features for every training row of
    every origin of every candidate lookback — O(origins x candidates x n)
    feature builds, which made a 3-name market take 5+ minutes. The features at
    row t do not depend on the origin or the lookback, only on t, so they are
    built once and every fit below is a slice plus an lstsq.

    Returns (t_index, X, y) where row k is training row t_index[k]. Verified
    against fit_har_v3 bit-for-bit in self_check().
    """
    vv = v.ffill()
    fut_mean = vv.rolling(horizon).mean().shift(-horizon).values
    ts, X, y = [], [], []
    for t in range(22, len(v) - horizon):
        f = har_features(v, t)
        if f is None:
            continue
        m = fut_mean[t]
        if np.isfinite(m) and m > 0:
            ts.append(t)
            X.append(f)
            y.append(np.log(m))
    if not ts:
        return np.array([]), np.zeros((0, 4)), np.array([])
    Xd = np.column_stack([np.ones(len(y)), np.array(X)])
    return np.array(ts), Xd, np.array(y)


def fit_har_cached(design, end_idx, horizon, lookback_years=None, min_obs=60):
    """log-HAR fit restricted to a trailing window — the lever under test.

    Same estimator as mc_v3.fit_har_v3; the training rows simply start at
    `end_idx - lookback_years * SESSIONS_PER_YEAR` instead of at 22. With
    lookback_years=None it reduces to fit_har_v3 exactly.

    WALK-FORWARD SAFETY: the upper bound is `end_idx - horizon`, NOT `end_idx`.
    Training row t carries a target built from rows [t+1, t+horizon], so any t
    within `horizon` of the origin would peek past it. Dropping the `- horizon`
    here is a silent lookahead leak — it was in the first draft of this module
    and was caught only because the cached fit stopped reproducing fit_har_v3.
    That non-reproduction was the bug reporting itself; self_check() below
    exists to keep it that way.
    """
    ts, Xd, ya = design
    if len(ts) == 0:
        return None, None
    start = 22
    if lookback_years is not None:
        start = max(22, int(end_idx - lookback_years * SESSIONS_PER_YEAR))
    m = (ts >= start) & (ts < end_idx - horizon)
    if m.sum() < min_obs:
        return None, None
    Xs, ys = Xd[m], ya[m]
    beta, *_ = np.linalg.lstsq(Xs, ys, rcond=None)
    resid = ys - Xs @ beta
    return beta, float(np.var(resid, ddof=Xs.shape[1]))


def walk(df, profile, lookback_years, horizon_months=3, q_annual=0.0,
         n_paths=20000, seed=42, min_history=260, origins=None,
         design_cache=None):
    """Walk-forward exactly as backtest_v3, with the HAR lookback restricted.

    `origins` pins the origin set so every candidate is scored on identical
    windows — without it a shorter lookback would be scored on a different
    sample and the comparison would be meaningless.
    """
    v = yz_variance_proxy(df)
    close = df['Price'].values
    dates = pd.to_datetime(df['Date']).dt.normalize().reset_index(drop=True)
    n = len(df)
    design_cache = {} if design_cache is None else design_cache
    rows, o = [], min_history
    while o < n:
        got = calendar_horizons(dates, o, horizon_months)
        if got is None:
            break
        h_grade, h_size = got
        if h_grade < 1 or o + h_grade >= n:
            break
        if origins is None or o in origins:
            date = df['Date'].iloc[o]
            spot, y = close[o], close[o + h_grade]
            if h_size not in design_cache:
                design_cache[h_size] = har_design(v, h_size)
            beta, s2 = fit_har_cached(design_cache[h_size], o, h_size,
                                      lookback_years)
            dv = har_forecast_v3(v, o, beta, s2, horizon=h_size)
            sigma_h = np.sqrt(dv * h_size) * profile.width_cal
            yf = horizon_months / 12.0
            drift = carry_log_h(profile, date, q_annual, h_size, yearfrac=yf)
            samp = simulate_terminal_v3(spot, sigma_h, drift, nu=profile.nu,
                                        n_paths=n_paths, seed=seed + o)
            sig_b = trailing_cc_vol(close, o) * np.sqrt(h_size)
            rngb = np.random.default_rng(seed + o + 1)
            bench = spot * np.exp(drift + sig_b * rngb.standard_normal(n_paths))
            q = np.percentile(samp, [5, 10, 50, 90, 95])
            rows.append(dict(
                origin=date, origin_idx=o,
                crps=crps_sample(samp, y), crps_b=crps_sample(bench, y),
                w90=(q[4] - q[0]) / spot,
                in90=bool(q[0] <= y <= q[4]), in80=bool(q[1] <= y <= q[3]),
                pit=float(np.mean(samp <= y)),
                u=(np.log(y / spot) - drift) / sigma_h if sigma_h > 0 else np.nan))
        o += h_grade
    return pd.DataFrame(rows)


def load(market, ticker):
    df, _ = clean_ohlc(load_ohlc(os.path.join(RAW, market, f'{ticker}.csv')),
                       ticker, verbose=False, market=market)
    return df.reset_index(drop=True)


def score_market(market, horizon_months=3, candidates=CANDIDATES, names=None,
                 n_paths=20000, verbose=True):
    """Score every candidate lookback on identical origins, pooled per market."""
    prof = MP.PROFILES[market]
    if names is None:
        names = sorted(os.path.splitext(f)[0]
                       for f in os.listdir(os.path.join(RAW, market))
                       if f.endswith('.csv'))
    per_name = {}
    for t in names:
        df = load(market, t)
        # origin set from the most restrictive candidate: a lookback needs
        # enough training rows to fit at all, so pin origins to their
        # intersection rather than letting each candidate pick its own sample.
        base = walk(df, prof, min(c for c in candidates if c is not None),
                    horizon_months, n_paths=1000)
        if base.empty:
            continue
        origins = set(base['origin_idx'])
        cache = {}
        per_name[t] = {c: walk(df, prof, c, horizon_months, n_paths=n_paths,
                               origins=origins, design_cache=cache)
                       for c in candidates}
        if verbose:
            print(f"  {market}/{t:<13} {len(origins):>4} common origins")
    return per_name


def pooled(per_name, cand):
    r = pd.concat([v[cand] for v in per_name.values() if not v[cand].empty],
                  ignore_index=True)
    u = r['u'].dropna()
    return dict(
        n=len(r),
        crps_skill=1 - r['crps'].sum() / r['crps_b'].sum(),
        mean_w90=float(r['w90'].mean()),
        cov80=float(r['in80'].mean()), cov90=float(r['in90'].mean()),
        pit=float(r['pit'].mean()), std_u=float(u.std()),
        rel=(1 - r['crps'] / r['crps_b']).values)


def report(per_name, candidates=CANDIDATES, label=''):
    print(f"\n{'lookback':<11}{'n':>5}{'CRPS skill':>12}{'mean 90% width':>16}"
          f"{'cov80':>8}{'cov90':>8}{'PIT':>7}{'std_u':>8}   {label}")
    out = {}
    for c in candidates:
        p = pooled(per_name, c)
        out[c] = p
        tag = 'unlimited' if c is None else f'{c:g} yr'
        print(f"{tag:<11}{p['n']:>5}{p['crps_skill']:>+12.4f}"
              f"{p['mean_w90'] * 100:>15.1f}%{p['cov80']:>8.3f}"
              f"{p['cov90']:>8.3f}{p['pit']:>7.3f}{p['std_u']:>8.3f}")
    return out
