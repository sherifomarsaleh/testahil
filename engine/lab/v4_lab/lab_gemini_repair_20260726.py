"""repaired.py — PASS 1 (expensive): repair every defect in the Gemini proposal,
then store per-origin components so arms can be scored cheaply in pass 2.

REPAIRS
  (a) "HARQ" harmonic-mean-of-nested-variances  ->  TRUE HARQ (Bollerslev-Patton-
      Quaedvlieg): HAR on daily/weekly/monthly variance with the DAILY coefficient
      attenuated by measured realized quarticity.  Two variants:
        harq_lvl : BPQ in levels,  v_fwd = b0 + (b1 + b1q*sqrtRQ_std)*v_d + b2*v_w + b3*v_m
        harq_log : same interaction, in log space + lognormal bias correction
                   (so it is directly comparable to production's log-HAR)
      RQ proxy (daily data, no intraday): RQ_t = (n/3) * sum(v_i^2) over 5 days,
      the standard RV-based quarticity estimator applied to the YZ per-day variance
      proxy. FLAGGED: without intraday data RQ is only weakly identified.
  (b) t-shocks never renormalized (sd = sqrt(5/3) = 1.291)  ->  unit-variance
      mixture sqrt((nu-2)/chi), and the skew-normal core renormalized AFTER the
      mixture, not before.
  (c) Hurst-gated raw drift (zero 86% of the time)  ->  carry anchor
      ln(1+rf) - ln(1+q) from the MarketProfile, identical to production.
  (d) tail-only, in-sample ACI  ->  full-cone WIDTH multiplier, walk-forward
      (updated only from windows that have already resolved). Two learners,
      applied in pass 2:
        aci  : multiplicative ACI on coverage misses, m *= exp(lr*(miss - 0.10))
        rms  : shrunk running RMS of past standardized residuals u
  (+) Step 0.0 data-quality gate applied to every series (was absent entirely).
"""
import sys, os, glob
sys.path.insert(0, '/tmp/mcrev/testahil/engine')
import numpy as np, pandas as pd
from panel_refresh import load_ohlc, apply_breaks
from market_profiles import PROFILES
from mc_v2 import yz_variance_proxy, crps_sample, trailing_cc_vol, har_features
from mc_v3 import fit_har_v3, har_forecast_v3, carry_log_h

H = 60; MINHIST = 260; SEED = 42
MARKET = sys.argv[1] if len(sys.argv) > 1 else 'EG'
prof = PROFILES[MARKET]


def rq_series(v, win=5):
    """Realized quarticity proxy from the per-day YZ variance proxy.
    RQ_t = (n/3) * sum_{i} v_i^2  over the trailing `win` days (standard RV-based
    quarticity estimator). sqrt(RQ) is the HARQ attenuation regressor."""
    vv = v.ffill().values
    out = np.full(len(vv), np.nan)
    for t in range(win - 1, len(vv)):
        w = vv[t - win + 1:t + 1]
        out[t] = (win / 3.0) * np.nansum(w ** 2)
    return pd.Series(np.sqrt(np.maximum(out, 0.0)), index=v.index)


def harq_design(v, sq, t):
    """[v_d, v_w, v_m, sqrtRQ_t * v_d]  — BPQ interaction on the DAILY lag only."""
    f = har_features(v, t)          # returns log([v1, v5, v22])
    if f is None or not np.isfinite(sq.iloc[t]):
        return None
    lv = np.exp(f)                  # back to levels
    return np.array([lv[0], lv[1], lv[2], sq.iloc[t] * lv[0]])


def harq_design_log(v, sq, t, sq_med):
    """log-space analogue: log lags + interaction of the daily lag with a
    standardized sqrt(RQ). Standardizing keeps the interaction on a sane scale."""
    f = har_features(v, t)
    if f is None or not np.isfinite(sq.iloc[t]) or sq_med <= 0:
        return None
    z = np.log(max(sq.iloc[t], 1e-18) / sq_med)
    return np.array([f[0], f[1], f[2], z * f[0], z])


def fit_harq(v, sq, end_idx, horizon=H, min_obs=60, log_space=False, sq_med=None):
    X, y = [], []
    vv = v.ffill()
    for t in range(22, end_idx - horizon):
        d = (harq_design_log(v, sq, t, sq_med) if log_space
             else harq_design(v, sq, t))
        if d is None:
            continue
        m = vv.iloc[t + 1:t + 1 + horizon].mean()
        if np.isfinite(m) and m > 0:
            X.append(d); y.append(np.log(m) if log_space else m)
    if len(y) < min_obs:
        return None, None
    Xd = np.column_stack([np.ones(len(y)), np.array(X)])
    ya = np.array(y)
    beta, *_ = np.linalg.lstsq(Xd, ya, rcond=None)
    resid = ya - Xd @ beta
    s2 = float(np.var(resid, ddof=Xd.shape[1]))
    return beta, s2


def harq_forecast(v, sq, o, beta, s2, log_space=False, sq_med=None, shrink=0.8):
    vtr = float(v.ffill().iloc[max(0, o - 251):o + 1].mean())
    d = (harq_design_log(v, sq, o, sq_med) if log_space else harq_design(v, sq, o))
    if d is None or beta is None:
        return vtr
    pred = beta[0] + beta[1:] @ d
    if log_space:
        pred = pred + 0.5 * s2                       # lognormal bias correction
        logv = shrink * pred + (1 - shrink) * np.log(max(vtr, 1e-12))
        return float(np.exp(logv))
    # levels: shrink in log space too, for a like-for-like comparison
    pred = max(pred, 1e-12)
    logv = shrink * np.log(pred) + (1 - shrink) * np.log(max(vtr, 1e-12))
    return float(np.exp(logv))


rows = []
for f in sorted(glob.glob(f'/tmp/mcrev/testahil/engine/raw_ohlc/{MARKET}/*.csv')):
    tk = os.path.basename(f)[:-4]
    df = load_ohlc(f, tk, market=MARKET)          # <- Step 0.0 gate
    n = len(df)
    if n < MINHIST + H + 1:
        continue
    v = yz_variance_proxy(df); sq = rq_series(v); close = df['Price'].values
    rr = []
    o = MINHIST
    while o + H < n:
        date = df['Date'].iloc[o]; spot = close[o]; y = close[o + H]
        carry = carry_log_h(prof, date, 0.0, H)      # repair (c)

        b3, s3 = fit_har_v3(v, o, horizon=H)
        dv_prod = har_forecast_v3(v, o, b3, s3, horizon=H)

        sqm = float(np.nanmedian(sq.iloc[:o + 1]))
        bl, sl = fit_harq(v, sq, o, log_space=False)
        dv_hl = harq_forecast(v, sq, o, bl, sl, log_space=False)
        bg, sg = fit_harq(v, sq, o, log_space=True, sq_med=sqm)
        dv_hg = harq_forecast(v, sq, o, bg, sg, log_space=True, sq_med=sqm)

        sig_b = trailing_cc_vol(close, o) * np.sqrt(H)
        bench = spot * np.exp(carry + sig_b *
                              np.random.default_rng(SEED + o + 1).standard_normal(20000))
        r252 = np.diff(np.log(close[max(0, o - 252):o + 1]))
        rr.append(dict(ticker=tk, origin=date, origin_idx=o, spot=spot, realized=y,
                       drift=carry,
                       sh_prod=np.sqrt(dv_prod * H),
                       sh_harq_lvl=np.sqrt(max(dv_hl, 1e-16) * H),
                       sh_harq_log=np.sqrt(max(dv_hg, 1e-16) * H),
                       sh_trail=sig_b,
                       alpha_skew=float(np.clip(pd.Series(r252).skew() * 2.0, -2, 2)),
                       crps_b=crps_sample(bench, y)))
        o += H
    r = apply_breaks(pd.DataFrame(rr), prof)
    if len(r):
        rows.append(r); print(f"  {tk:6s} n={len(r):3d}")

R = pd.concat(rows, ignore_index=True)
R.to_csv(f'/tmp/mcrev/comp_{MARKET}.csv', index=False)
print(f"\nstored {len(R)} windows / {R.ticker.nunique()} names -> comp_{MARKET}.csv")
for c in ['sh_prod', 'sh_harq_lvl', 'sh_harq_log', 'sh_trail']:
    print(f"  {c:12s} median {R[c].median():.4f}")
