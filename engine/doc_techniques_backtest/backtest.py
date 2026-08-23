"""backtest.py — the 23-Aug-2026 uploaded document's techniques, seriously tried.

STATUS: RESEARCH ONLY. Nothing adopted, nothing published, no engine config
touched. Requested by Sherif 23-Aug-2026: "seriously try the techniques of the
document I sent you and back test them for the stocks over the last 15 years."

Source document: "State-of-the-Art Developments in MC Forecasting Systems"
(uploaded 23-Aug-2026). Its implementable market-forecasting techniques, each
mapped to a walk-forward model here, on the full cleaned raw_ohlc library:

  doc technique                          -> model key
  ------------------------------------------------------------------
  GBM Monte Carlo, drift from long       -> gbm_exp   (expanding-mean drift)
    historical windows (Part III)           gbm_36m   (rolling 36-month drift)
  ARIMA family (Part III)                -> ar_aic    (AR(p<=3), OLS, AIC-picked
                                            in-window; MA terms add ~nothing on
                                            monthly equity returns and are noted)
  LSTM / deep-learning forecasting       -> mlp       (pooled per-market neural
    (Parts I, III)                          net on a 12-month lag window + vol
                                            features; an LSTM's sequence memory
                                            over monthly data reduces to this
                                            lag window — torch-scale training is
                                            out of scope for this environment
                                            and the substitution is stated)
                                            gbr       (gradient boosting, the
                                            generic "ML" of the document)
  Fuzzy time series as Markov states     -> markov5   (5 quantile states, smoothed
    with K-means partitioning (Part III)    transition matrix, chain-composed)
  State-space / data-assimilation        -> kalman    (local-level Kalman filter,
    (Part V, particle-filter family)        adaptive mean of returns)
  Component decomposition (Part III,     -> seasonal  (month-of-year mean from
    annual/monthly/daily SMP model)         the training window)
  Model averaging "SAM" (Part V)         -> ens       (mean of the above)
  Chaos-theory delay embedding (Part III)   folded into mlp/gbr feature windows
                                            (a lag window IS a delay embedding)
  Mass-conserving LSTM (Part I)             NOT RUN — prices obey no conservation
                                            law; nothing to conserve. Stated, not
                                            silently skipped.
  EEMD-SVD-MA denoising (Part V)            NOT RUN — needs PyEMD-scale tooling;
                                            listed as unrun, not judged.

Benchmarks: carry (predict zero excess return — today's engine center) and
mom_ref (the 23-Aug tournament's momentum lean; its IC was measured on data
overlapping this sample, so it is an IN-SAMPLE REFERENCE, flagged as such).

All models predict the EXCESS-of-carry return (so no model is credited for
the risk-free rate), walk-forward, strictly point-in-time: a training row is
used only when its target had resolved by the forecast origin.

WIDTH AXIS — the investor's "the cone is too wide" tested as a question:
which volatility technique yields the narrowest band that still contains
reality at the promised rate? Models: roll63 (63-session daily-return std —
engine-like proxy), ewma (lambda 0.94), hist_flat (all-history-to-date std —
the document's own long-window spec), roll12m (monthly-return std). Bands are
carry-centered with each market's own fitted (nu, width_cal); scored on
realized 50%/90% coverage, average width, and Winkler-90 skill vs roll63.
Also computed, because it is the honest floor: the realized distribution of
3-month moves per market — no 50% band can average narrower than the middle
half of what the stocks actually did.

Usage:
    python3 engine/doc_techniques_backtest/backtest.py \
        --json RESULTS.json --md RESULTS.md --generated 2026-08-23
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import warnings

import numpy as np
import pandas as pd
from scipy import stats

warnings.filterwarnings("ignore")

ENG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ENG)
sys.path.insert(0, os.path.join(ENG, "direction_tournament"))

from market_profiles import PROFILES                   # noqa: E402
from data_quality import clean_ohlc                    # noqa: E402
from tournament import (load_clean, month_end_grid,    # noqa: E402
                        block_boot_mean, split_half)

RAW = os.path.join(ENG, "raw_ohlc")
TRAIN_MIN = 60          # months of history before the first forecast
LAGS = 12               # delay-embedding window for ML models
K_STATES = 5            # Markov/fuzzy states
REFIT_EVERY = 12        # pooled ML refit cadence (origins)
SEED = 42
CORE = ("EG", "AE", "SA")


# ----------------------------------------------------------------- data prep
def name_series(market: str, ticker: str):
    """Monthly origin grid with raw price, excess monthly return, daily tail."""
    df = load_clean(market, ticker)
    if df is None:
        return None
    grid = month_end_grid(df)
    if len(grid) < TRAIN_MIN + 6:
        return None
    prof = PROFILES.get(market)
    d = grid.reset_index(drop=True)
    r = np.log(d["Price"]).diff()
    carry = np.array([np.log(1 + (prof.carry_rate(t) if prof else 0.0)) / 12
                      for t in d["Date"]])
    x = (r - carry).values                       # excess-of-carry monthly return
    daily = df.set_index("Date")["Price"]
    return {"dates": d["Date"].values, "price": d["Price"].values,
            "x": x, "daily": daily, "name": ticker}


# ------------------------------------------------------- center-model library
def ar_aic_forecast(x, h):
    """AR(p<=3) by OLS, AIC-selected on the window; h-step iterated sum."""
    x = x[~np.isnan(x)]
    n = len(x)
    if n < 24:
        return 0.0
    best, best_aic = None, np.inf
    for p in (1, 2, 3):
        Y = x[p:]
        X = np.column_stack([x[p - k - 1: n - k - 1] for k in range(p)])
        X = np.column_stack([np.ones(len(Y)), X])
        beta, res, *_ = np.linalg.lstsq(X, Y, rcond=None)
        eps = Y - X @ beta
        s2 = max(np.mean(eps ** 2), 1e-12)
        aic = len(Y) * np.log(s2) + 2 * (p + 1)
        if aic < best_aic:
            best_aic, best = aic, (p, beta)
    p, beta = best
    hist = list(x[-p:])
    total = 0.0
    for _ in range(h):
        nxt = beta[0] + sum(beta[1 + k] * hist[-1 - k] for k in range(p))
        total += nxt
        hist.append(nxt)
    return float(total)


def kalman_forecast(x, h):
    """Local-level filter: adaptive mean of the excess return."""
    x = x[~np.isnan(x)]
    if len(x) < 24:
        return 0.0
    r_var = np.var(x)
    if r_var <= 0:
        return 0.0
    q_var = r_var / 50.0                          # slow-moving level
    m, P = 0.0, r_var
    for obs in x:
        P = P + q_var
        k = P / (P + r_var)
        m = m + k * (obs - m)
        P = (1 - k) * P
    return float(m * h)


def markov_forecast(x, h):
    """Quantile states + smoothed transitions, chain-composed h steps."""
    x = x[~np.isnan(x)]
    if len(x) < 40:
        return 0.0
    qs = np.quantile(x, np.linspace(0, 1, K_STATES + 1)[1:-1])
    st = np.searchsorted(qs, x)
    cent = np.array([x[st == s].mean() if (st == s).any() else 0.0
                     for s in range(K_STATES)])
    T = np.ones((K_STATES, K_STATES))            # Laplace smoothing
    for a, b in zip(st[:-1], st[1:]):
        T[a, b] += 1
    T = T / T.sum(axis=1, keepdims=True)
    v = np.zeros(K_STATES)
    v[st[-1]] = 1.0
    total = 0.0
    for _ in range(h):
        v = v @ T
        total += float(v @ cent)
    return total


def seasonal_forecast(x, months, origin_month, h):
    out = 0.0
    ok = ~np.isnan(x)
    for step in range(1, h + 1):
        m = (origin_month + step - 1) % 12 + 1
        sel = ok & (months == m)
        out += float(x[sel].mean()) if sel.sum() >= 3 else 0.0
    return out


def ml_features(x, i):
    """Delay-embedding window + vol features at origin i (uses data <= i)."""
    w = x[i - LAGS + 1: i + 1]
    if len(w) < LAGS or np.isnan(w).any():
        return None
    v3 = np.std(x[max(0, i - 2): i + 1])
    v12 = np.std(w)
    return list(w) + [v3, v12]


# ---------------------------------------------------------------- width axis
def width_models(daily: pd.Series, origin, h_days):
    d = daily[daily.index <= origin]
    lr = np.diff(np.log(d.values))
    if len(lr) < 130:
        return None
    out = {}
    out["roll63"] = float(np.std(lr[-63:]) * np.sqrt(h_days))
    out["hist_flat"] = float(np.std(lr) * np.sqrt(h_days))
    lam = 0.94
    w = lam ** np.arange(len(lr) - 1, -1, -1)
    ew_var = float(np.sum(w * lr ** 2) / np.sum(w))
    out["ewma"] = float(np.sqrt(ew_var * h_days))
    return out


def tqv(p, nu):
    return float(np.sqrt((nu - 2) / nu) * stats.t.ppf(p, nu))


# ------------------------------------------------------------------- scoring
def score_center(pred, real, dates, label):
    pred, real = np.asarray(pred, float), np.asarray(real, float)
    ok = np.isfinite(pred) & np.isfinite(real)
    pred, real, dts = pred[ok], real[ok], np.asarray(dates)[ok]
    n = len(pred)
    if n < 60:
        return {"model": label, "n": n, "note": "insufficient"}
    ic = stats.spearmanr(pred, real).statistic if np.std(pred) > 0 else np.nan
    nz = np.abs(pred) > 1e-9
    hit = (np.sign(pred[nz]) == np.sign(real[nz])).mean() if nz.sum() > 30 else np.nan
    mae_m = np.mean(np.abs(real - pred))
    mae_0 = np.mean(np.abs(real))
    skill = 1 - mae_m / mae_0 if mae_0 > 0 else np.nan
    diffs = np.abs(real) - np.abs(real - pred)     # per-obs gain vs carry
    lo, hi = block_boot_mean(diffs, 3)
    h1, h2 = split_half(dts.astype("datetime64[ns]"),
                        np.sign(pred) * real if np.std(pred) > 0 else real * 0)
    return {"model": label, "n": int(n),
            "ic": float(ic) if ic == ic else None,
            "hit_rate": float(hit) if hit == hit else None,
            "mae_skill_vs_carry": float(skill),
            "mae_gain_ci_b3": [float(lo), float(hi)],
            "beats_carry_robust": bool(lo > 0),
            "hurts_vs_carry_robust": bool(hi < 0),
            "split_half_signret": [h1, h2],
            "split_half_same_sign": bool(np.sign(h1) == np.sign(h2)
                                         and h1 == h1 and h2 == h2)}


# ---------------------------------------------------------------- market run
def run_market(market: str, tickers: list[str], sk) -> dict:
    series = []
    for t in tickers:
        try:
            s = name_series(market, t)
        except Exception:
            s = None
        if s is not None:
            series.append(s)
    if not series:
        return {"market": market, "names": 0}
    prof = PROFILES.get(market)
    nu = prof.nu if prof and prof.nu else 12.0
    wcal = prof.width_cal if prof else 1.0

    preds = {h: {} for h in (1, 3)}     # h -> model -> list
    reals = {h: [] for h in (1, 3)}
    dates_h = {h: [] for h in (1, 3)}
    ml_rows = {h: [] for h in (1, 3)}   # pooled training pool (i, feats, target, name-idx)
    width_rows = []
    realized3 = []

    # ---- pass 1: everything except pooled-ML predictions -------------------
    for si, s in enumerate(series):
        x, dts = s["x"], pd.to_datetime(s["dates"])
        months = np.array([d.month for d in dts])
        n = len(x)
        for i in range(TRAIN_MIN, n):
            for h in (1, 3):
                if i + h >= n:
                    continue
                if h == 3 and dts[i].month not in (3, 6, 9, 12):
                    continue
                real = float(np.nansum(x[i + 1: i + h + 1]))
                if not np.isfinite(real):
                    continue
                tr = x[1: i + 1]
                row = {
                    "carry": 0.0,
                    "gbm_exp": float(np.nanmean(tr)) * h,
                    "gbm_36m": float(np.nanmean(tr[-36:])) * h,
                    "ar_aic": ar_aic_forecast(tr, h),
                    "kalman": kalman_forecast(tr, h),
                    "markov5": markov_forecast(tr, h),
                    "seasonal": seasonal_forecast(x[:i + 1], months[:i + 1],
                                                  dts[i].month, h),
                }
                for k, v in row.items():
                    preds[h].setdefault(k, []).append(v)
                reals[h].append(real)
                dates_h[h].append(dts[i].to_datetime64())
                f = ml_features(x, i)
                ml_rows[h].append((si, i, f, real, dts[i]))
                # width axis (3M only, core markets, every other origin)
                if h == 3 and market in CORE and (i % 2 == 0):
                    wm = width_models(s["daily"], dts[i], 63)
                    if wm:
                        width_rows.append((wm, real))
                if h == 3:
                    realized3.append(real)

    # ---- pass 2: pooled per-market ML (walk-forward, refit yearly) ---------
    for h in (1, 3):
        rows = ml_rows[h]
        mlp_pred = [np.nan] * len(rows)
        gbr_pred = [np.nan] * len(rows)
        order = sorted(range(len(rows)), key=lambda k: rows[k][4])
        dates_sorted = [rows[k][4] for k in order]
        uniq = sorted(set(dates_sorted))
        if sk is not None and len(rows) > 300:
            from sklearn.neural_network import MLPRegressor
            from sklearn.ensemble import GradientBoostingRegressor
            from sklearn.preprocessing import StandardScaler
            for start in range(0, len(uniq), REFIT_EVERY):
                block = set(uniq[start: start + REFIT_EVERY])
                cutoff = min(block)
                trainX, trainY = [], []
                for (si, i, f, real, dt) in rows:
                    # target must have RESOLVED before the earliest forecast
                    if f is not None and dt < cutoff - pd.DateOffset(months=h):
                        trainX.append(f)
                        trainY.append(real)
                if len(trainX) < 300:
                    continue
                sc = StandardScaler().fit(trainX)
                Xt = sc.transform(trainX)
                mlp = MLPRegressor(hidden_layer_sizes=(16, 8), max_iter=300,
                                   random_state=SEED, early_stopping=True)
                gbr = GradientBoostingRegressor(n_estimators=120, max_depth=2,
                                                learning_rate=0.05,
                                                subsample=0.7,
                                                random_state=SEED)
                mlp.fit(Xt, trainY)
                gbr.fit(trainX, trainY)
                for k, (si, i, f, real, dt) in enumerate(rows):
                    if dt in block and f is not None:
                        mlp_pred[k] = float(mlp.predict(sc.transform([f]))[0])
                        gbr_pred[k] = float(gbr.predict([f])[0])
        preds[h]["mlp"] = mlp_pred
        preds[h]["gbr"] = gbr_pred
        parts = [preds[h][k] for k in
                 ("gbm_36m", "ar_aic", "kalman", "markov5", "seasonal",
                  "mlp", "gbr")]
        ens = []
        for vals in zip(*parts):
            v = [p for p in vals if p == p]
            ens.append(float(np.mean(v)) if v else np.nan)
        preds[h]["ens"] = ens

    out = {"market": market, "names": len(series),
           "center": {}, "width": None, "reality_floor": None}
    for h in (1, 3):
        out["center"][f"{h}M"] = [
            score_center(preds[h][m], reals[h], dates_h[h], m)
            for m in preds[h]]

    # ---- width scoring ------------------------------------------------------
    if width_rows:
        wsc = {}
        q90, q75 = tqv(0.95, nu), tqv(0.75, nu)
        for key in ("roll63", "ewma", "hist_flat"):
            sig = np.array([w[0][key] for w in width_rows])
            real = np.array([w[1] for w in width_rows])
            half90 = wcal * q90 * sig
            half50 = wcal * q75 * sig
            cov90 = float(np.mean(np.abs(real) <= half90))
            cov50 = float(np.mean(np.abs(real) <= half50))
            wid90 = float(np.mean(np.exp(half90) - np.exp(-half90)))
            wid50 = float(np.mean(np.exp(half50) - np.exp(-half50)))
            wk = half90 * 2 + np.where(np.abs(real) > half90,
                                       (np.abs(real) - half90) * 2 / 0.10, 0)
            wsc[key] = {"cov90": cov90, "cov50": cov50,
                        "avg_width90_pct": wid90 * 100,
                        "avg_width50_pct": wid50 * 100,
                        "winkler90": float(np.mean(wk))}
        base = wsc["roll63"]["winkler90"]
        for key in wsc:
            wsc[key]["winkler90_skill_vs_roll63"] = 1 - wsc[key]["winkler90"] / base
        out["width"] = {"n": len(width_rows), "models": wsc}

    if realized3:
        r3 = np.abs(np.array(realized3))
        out["reality_floor"] = {
            "n_3m_moves": len(r3),
            "median_abs_3m_move_pct": float(np.median(np.exp(r3) - 1) * 100),
            "iqr_width_floor_pct": float(
                (np.exp(np.quantile(np.array(realized3), 0.75))
                 - np.exp(np.quantile(np.array(realized3), 0.25))) * 100)}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", required=True)
    ap.add_argument("--md", required=True)
    ap.add_argument("--generated", default="2026-08-23")
    args = ap.parse_args()

    try:
        import sklearn as sk
    except ImportError:
        sk = None

    markets = []
    for market in sorted(os.listdir(RAW)):
        folder = os.path.join(RAW, market)
        if not os.path.isdir(folder):
            continue
        tickers = sorted(f[:-4] for f in os.listdir(folder) if f.endswith(".csv"))
        if not tickers:
            continue
        print(f"[{market}] {len(tickers)} names …", flush=True)
        markets.append(run_market(market, tickers, sk))

    payload = {"generated": args.generated, "seed": SEED,
               "status": "RESEARCH ONLY — document-techniques backtest",
               "sklearn": bool(sk), "markets": markets}
    with open(args.json, "w") as f:
        json.dump(payload, f, indent=1, default=str)

    # ---------- markdown ----------
    MW = {"carry": "carry (today's engine)", "gbm_exp": "GBM drift, all history",
          "gbm_36m": "GBM drift, 36m window", "ar_aic": "ARIMA-family (AR, AIC)",
          "kalman": "Kalman adaptive drift", "markov5": "Markov/fuzzy 5-state",
          "seasonal": "seasonal (month-of-year)", "mlp": "neural net (pooled)",
          "gbr": "gradient boosting (pooled)", "ens": "ensemble average"}
    L = ["# Document-techniques backtest — RESULTS (research only)", "",
         f"Generated {args.generated}. Walk-forward, first forecast after "
         f"{TRAIN_MIN} months of history, targets are EXCESS of each market's "
         "carry. 'MAE skill vs carry' > 0 = the technique's center forecast "
         "beats today's engine center; 'robust' = the block-bootstrap CI of "
         "the per-observation gain clears zero.", ""]
    for mk in markets:
        if not mk.get("center"):
            continue
        L.append(f"## {mk['market']} — {mk['names']} names")
        L.append("")
        L.append("| technique | clock | obs | rank skill (IC) | hit rate | "
                 "MAE skill vs carry | robustly better? | robustly worse? | "
                 "split-half OK |")
        L.append("|---|---|---|---|---|---|---|---|---|")
        for h in ("1M", "3M"):
            for r in mk["center"][h]:
                if r.get("note"):
                    continue
                L.append("| {m} | {h} | {n} | {ic} | {hit} | {sk} | {rb} | {rw} | {sh} |".format(
                    m=MW.get(r["model"], r["model"]), h=h, n=r["n"],
                    ic=f"{r['ic']:+.3f}" if r["ic"] is not None else "—",
                    hit=f"{r['hit_rate']:.0%}" if r["hit_rate"] is not None else "—",
                    sk=f"{r['mae_skill_vs_carry']:+.2%}",
                    rb="YES" if r["beats_carry_robust"] else "no",
                    rw="YES" if r["hurts_vs_carry_robust"] else "no",
                    sh="yes" if r["split_half_same_sign"] else "no"))
        if mk.get("width"):
            L += ["", f"**Width (3M, n={mk['width']['n']}):** "
                  "band = carry-centered, market's own (nu, width_cal), "
                  "volatility per technique.", "",
                  "| vol technique | 90% band avg width | realized coverage | "
                  "50% band avg width | realized coverage | Winkler-90 skill |",
                  "|---|---|---|---|---|---|"]
            for k, w in mk["width"]["models"].items():
                L.append(f"| {k} | {w['avg_width90_pct']:.1f}% | "
                         f"{w['cov90']:.0%} | {w['avg_width50_pct']:.1f}% | "
                         f"{w['cov50']:.0%} | "
                         f"{w['winkler90_skill_vs_roll63']:+.2%} |")
        if mk.get("reality_floor"):
            rf = mk["reality_floor"]
            L += ["", f"**Reality floor:** across {rf['n_3m_moves']} real "
                  f"3-month windows, the median move was "
                  f"±{rf['median_abs_3m_move_pct']:.1f}% and the middle half "
                  f"of outcomes spans {rf['iqr_width_floor_pct']:.1f}% of "
                  "price — no honest 50% band can average narrower than "
                  "that, whatever the technique.", ""]
        L.append("")
    with open(args.md, "w") as f:
        f.write("\n".join(L))
    print(f"wrote {args.json}\nwrote {args.md}")


if __name__ == "__main__":
    main()
