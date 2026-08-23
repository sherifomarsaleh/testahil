"""tournament.py — Direction-Signal Tournament (23-Aug-2026).

STATUS: RESEARCH ONLY. Nothing here is adopted, promoted, or published. No
engine config, no published cone, no ledger row, and no site surface is
touched. Adoption of ANY finding requires the standing promotion rule
(out-of-sample gate + review PR), exactly as for every prior candidate.

WHY THIS EXISTS
---------------
Client critique (relayed 23-Aug-2026): the published cones are very wide and
carry no direction. Both observations are correct — the center of every live
cone is the interest-rate carry and nothing else, because every directional
candidate ever tested was switched off. But the recorded verdicts have a
documented gap (`direction_score.py` header, integration protocol §7):
signals were ablated under CRPS, a distributional loss close to blind to
direction. Phase B built the direction-aware referee; it has never been
pointed at a broad candidate set. This tournament is that sweep.

Prior art, so nothing is re-discovered or contradicted silently:
  * lab_round7_signedtrend.py (23-Jul-2026): corr(trailing trend, fwd 60d)
    ~ 0 on the EG panel, negative for 19/30 names.
  * lab_round7b_reversal.py: the sign-flipped candidate, CRPS-scored.
  * EGYPT.fit_meta: rev_1m empirical IC +0.018 (prior sign refuted),
    ablated under CRPS. IN/US momentum priors likewise off.
This tournament extends: all markets, six price-computable candidates,
calendar 1M/3M horizons, direction-first scoring, split-half confirmation.

WHAT IT RUNS
------------
Candidates (all point-in-time, price-only, no fitted parameters):
  mom_12_1   12-month return, skipping the most recent month
  mom_6_1    6-month return, skipping the most recent month
  rev_1m     most recent 1-month return (reversal reads as robust NEGATIVE)
  near52h    log distance of price from its 52-week high (always <= 0)
  trend200   log distance of price from its own 200-session average
  rsi14      Wilder RSI(14) minus 50 (the house technicals.py computation)

Two framings, because investors ask two different questions:
  XS  cross-sectional ("which of these names") — per date with >=8 names,
      Spearman rank IC across names + top-minus-bottom tercile spread.
  TS  pooled time-series ("which way is this one going") — per-name features
      z-scored against that name's OWN PRIOR history (min 18 prior monthly
      points, strictly before t), scored by direction_score.score() with its
      block bootstrap, LONO and MIN_N=100 power gate.

Forward returns are EXCESS OF CARRY (profile.carry_rate at the origin), so a
candidate is never credited for the risk-free rate. Dividends are NOT netted
(q=0) — flagged: this slightly penalises high-dividend names in level, but
rank/sign scoring is materially unaffected.

HONESTY RULES BUILT IN
----------------------
* Every series passes data_quality.clean_ohlc (Step 0.0) before use.
* 6 features x 2 horizons x 2 framings x ~10 markets is a multiple-testing
  minefield: a single PASS cell is noise until proven otherwise. A candidate
  is a SURVIVOR only if, in at least one market with pooled n>=100:
  robust same-sign CI across blocks {2,3,4} AND LONO sign-stable AND
  split-half same-sign AND the XS framing (where defined) agrees in sign.
* Survivors are still only CANDIDATES: promotion needs the standing gate.

Usage
-----
    python3 engine/direction_tournament/tournament.py \
        --json RESULTS.json --md RESULTS.md
"""
from __future__ import annotations

import argparse
import json
import os
import sys

import numpy as np
import pandas as pd
from scipy import stats

ENG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ENG)

from data_quality import clean_ohlc            # noqa: E402  Step 0.0 gate
from market_profiles import PROFILES           # noqa: E402
import direction_score as ds                   # noqa: E402  Phase B referee
import technicals                              # noqa: E402  house RSI/SMA math

RAW = os.path.join(ENG, "raw_ohlc")

FEATURES = ("mom_12_1", "mom_6_1", "rev_1m", "near52h", "trend200", "rsi14")
HORIZONS = {"1M": 1, "3M": 3}

MIN_XS_NAMES = 8       # cross-sectional date needs at least this many names
TERCILE_MIN = 9        # tercile spread needs at least 3 per bucket
Z_MIN_PRIOR = 18       # monthly points of a name's own history before z is defined
ORIGIN_TOL_DAYS = 7    # last session must sit within this of month-end
BOOT_BLOCKS = ds.BOOT_BLOCKS
N_BOOT = ds.N_BOOT
SEED = ds.SEED
SURVIVOR_MIN_ABS_IC = 0.05


# ------------------------------------------------------------------ loading
def load_clean(market: str, ticker: str) -> pd.DataFrame | None:
    path = os.path.join(RAW, market, f"{ticker}.csv")
    df = pd.read_csv(path)
    df["Date"] = pd.to_datetime(df["Date"], format="%m/%d/%Y")
    for c in ("Price", "Open", "High", "Low"):
        df[c] = df[c].astype(str).str.replace(",", "", regex=False).astype(float)
    df = df.sort_values("Date").reset_index(drop=True)
    df, _log = clean_ohlc(df, ticker=ticker, verbose=False, market=market)
    if df is None or len(df) < 260:
        return None
    return df[["Date", "Price"]].reset_index(drop=True)


def month_end_grid(df: pd.DataFrame) -> pd.DataFrame:
    """Last session of each calendar month, dropped if stale vs month-end."""
    d = df.copy()
    d["ym"] = d["Date"].dt.to_period("M")
    g = d.groupby("ym").tail(1).reset_index(drop=True)
    eom = g["ym"].dt.to_timestamp("M")
    g = g[(eom - g["Date"]).dt.days <= ORIGIN_TOL_DAYS].reset_index(drop=True)
    return g[["Date", "Price", "ym"]]


# ----------------------------------------------------------------- features
def build_name_rows(market: str, ticker: str) -> pd.DataFrame | None:
    df = load_clean(market, ticker)
    if df is None:
        return None
    grid = month_end_grid(df)
    if len(grid) < 16:
        return None
    dates = df["Date"].values
    px = df["Price"].values.astype(float)
    rows = []
    gd, gp = grid["Date"].values, grid["Price"].values.astype(float)
    # map each grid date to its daily index
    didx = np.searchsorted(dates, gd)
    for i in range(len(grid)):
        j = int(didx[i])          # index of origin session in the daily series
        t = pd.Timestamp(gd[i])
        p0 = gp[i]
        feat = {}
        if i >= 12:
            feat["mom_12_1"] = float(np.log(gp[i - 1] / gp[i - 12]))
        if i >= 6:
            feat["mom_6_1"] = float(np.log(gp[i - 1] / gp[i - 6]))
        if i >= 1:
            feat["rev_1m"] = float(np.log(p0 / gp[i - 1]))
        # daily-window features
        w52 = px[max(0, j - 251): j + 1]
        if len(w52) >= 200:
            feat["near52h"] = float(np.log(p0 / np.max(w52)))
        if j + 1 >= 200:
            sma = technicals._sma(px[: j + 1], 200)
            if sma:
                feat["trend200"] = float(np.log(p0 / sma))
        wr = px[max(0, j - 99): j + 1]
        if len(wr) >= 30:
            rsi = technicals._rsi_wilder(wr, 14)
            if rsi is not None:
                feat["rsi14"] = float(rsi - 50.0)
        if not feat:
            continue
        rows.append({"name": ticker, "date": t, "i": i, "price": p0, **feat})
    out = pd.DataFrame(rows)
    if out.empty:
        return None
    # forwards, excess of carry
    prof = PROFILES.get(market)
    grid_by_i = {int(r["i"]): (pd.Timestamp(gd[int(r["i"])]), gp[int(r["i"])])
                 for _, r in out.iterrows()}
    full_grid = {i: (pd.Timestamp(gd[i]), gp[i]) for i in range(len(grid))}
    for label, k in HORIZONS.items():
        fwd = []
        for _, r in out.iterrows():
            i = int(r["i"])
            if i + k in full_grid:
                d1, p1 = full_grid[i + k]
                days = (d1 - r["date"]).days
                rf = prof.carry_rate(r["date"]) if prof else 0.0
                carry = np.log(1 + rf) * (days / 365.25)
                fwd.append(float(np.log(p1 / r["price"]) - carry))
            else:
                fwd.append(np.nan)
        out[f"fwd_{label}"] = fwd
    return out.drop(columns=["i"])


# ---------------------------------------------------------------- utilities
def block_boot_mean(series: np.ndarray, block: int,
                    n_boot: int = N_BOOT, seed: int = SEED):
    """Moving-block bootstrap CI for the MEAN of an autocorrelated series.

    Same conventions as direction_score._ic_ci: blocks {2,3,4}, 5/95
    percentiles, seed 42 — applied to a per-date statistic series (date-IC or
    tercile spread), which _ic_ci does not cover.
    """
    n = len(series)
    if n < block + 1:
        return float("nan"), float("nan")
    rng = np.random.default_rng(seed)
    means = []
    for _ in range(n_boot):
        starts = rng.integers(0, n - block + 1, size=int(np.ceil(n / block)))
        idx = np.concatenate([np.arange(s, s + block) for s in starts])[:n]
        means.append(float(np.mean(series[idx])))
    lo, hi = np.percentile(means, [5, 95])
    return float(lo), float(hi)


def robust_sign_verdict(series: np.ndarray) -> tuple[str, dict]:
    """SIGNAL+ / SIGNAL- only if every block's CI clears zero on the same side."""
    detail = {}
    verds = []
    for b in BOOT_BLOCKS:
        lo, hi = block_boot_mean(series, b)
        v = ("SIGNAL+" if lo > 0 else ("SIGNAL-" if hi < 0 else "PARITY"))
        if np.isnan(lo):
            v = "NOBLOCK"
        detail[b] = {"lo": lo, "hi": hi, "verdict": v}
        verds.append(v)
    if "NOBLOCK" in verds:
        return "PROVISIONAL(insufficient-dates)", detail
    if all(v == "SIGNAL+" for v in verds):
        return "SIGNAL+", detail
    if all(v == "SIGNAL-" for v in verds):
        return "SIGNAL-", detail
    if len(set(verds)) > 1:
        return "BOUNDARY", detail
    return "PARITY", detail


def split_half(dates: np.ndarray, values: np.ndarray):
    cut = np.median(dates.astype("datetime64[D]").astype(int))
    a = values[dates.astype("datetime64[D]").astype(int) <= cut]
    b = values[dates.astype("datetime64[D]").astype(int) > cut]
    return (float(np.mean(a)) if len(a) else float("nan"),
            float(np.mean(b)) if len(b) else float("nan"))


def expanding_z(g: pd.DataFrame, col: str) -> pd.Series:
    """z of feature vs the name's OWN strictly-prior history (min Z_MIN_PRIOR)."""
    x = g[col]
    mu = x.expanding().mean().shift(1)
    sd = x.expanding().std().shift(1)
    cnt = x.expanding().count().shift(1)
    z = (x - mu) / sd
    z[(cnt < Z_MIN_PRIOR) | (sd == 0)] = np.nan
    return z


# ----------------------------------------------------------------- scoring
def run_market(market: str, tickers: list[str]) -> dict:
    frames = []
    used, skipped = [], []
    for t in tickers:
        try:
            f = build_name_rows(market, t)
        except Exception as e:               # a broken export must not kill the sweep
            skipped.append(f"{t}: {e}")
            continue
        if f is None:
            skipped.append(f"{t}: too short after Step 0.0")
            continue
        frames.append(f)
        used.append(t)
    if not frames:
        return {"market": market, "names": 0, "note": "no usable series"}
    panel = pd.concat(frames, ignore_index=True)
    out = {"market": market, "names": len(used), "used": used, "skipped": skipped,
           "date_range": [str(panel["date"].min().date()),
                          str(panel["date"].max().date())],
           "results": {}}
    for label, k in HORIZONS.items():
        fwd_col = f"fwd_{label}"
        for feat in FEATURES:
            cell = {}
            sub = panel.dropna(subset=[feat, fwd_col])
            # ---- XS framing (overlapping monthly dates; block boot handles it)
            ics, spreads, xs_dates = [], [], []
            for dt, g in sub.groupby("date"):
                if len(g) >= MIN_XS_NAMES and g[feat].std() > 0:
                    ics.append(stats.spearmanr(g[feat], g[fwd_col]).statistic)
                    xs_dates.append(dt)
                    if len(g) >= TERCILE_MIN:
                        q = g[feat].rank(pct=True)
                        top = g.loc[q > 2 / 3, fwd_col].mean()
                        bot = g.loc[q <= 1 / 3, fwd_col].mean()
                        spreads.append(top - bot)
            if len(ics) >= 8:
                ics_a = np.asarray(ics, float)
                v, det = robust_sign_verdict(ics_a)
                h1, h2 = split_half(np.asarray(xs_dates, dtype="datetime64[ns]"),
                                    ics_a)
                cell["XS"] = {
                    "n_dates": len(ics_a), "mean_ic": float(np.mean(ics_a)),
                    "verdict": v,
                    "ci_by_block": det,
                    "split_half_ic": [h1, h2],
                    "split_half_same_sign": bool(np.sign(h1) == np.sign(h2)
                                                 and h1 == h1 and h2 == h2),
                }
                if len(spreads) >= 8:
                    sp = np.asarray(spreads, float)
                    lo, hi = block_boot_mean(sp, 2)
                    cell["XS"]["tercile_spread_mean_pct"] = float(np.mean(sp)) * 100
                    cell["XS"]["tercile_spread_ci_pct"] = [lo * 100, hi * 100]
            # ---- TS framing (per-name z vs own prior history)
            ts = sub.sort_values(["name", "date"]).copy()
            if label == "3M":   # non-overlapping: calendar quarter-end origins only
                ts = ts[ts["date"].dt.month.isin((3, 6, 9, 12))]
            zs = []
            for _, g in ts.groupby("name", sort=False):
                zs.append(expanding_z(g, feat))
            ts["z"] = pd.concat(zs).reindex(ts.index)
            ts = ts.dropna(subset=["z", fwd_col])
            if len(ts) >= 30:
                res = ds.score(ts["z"].values, ts[fwd_col].values,
                               names=ts["name"].values)
                h1, h2 = split_half(ts["date"].values.astype("datetime64[ns]"),
                                    np.sign(ts["z"].values)
                                    * ts[fwd_col].values)
                res["split_half_signreturn"] = [h1, h2]
                res["split_half_same_sign"] = bool(np.sign(h1) == np.sign(h2)
                                                   and h1 == h1 and h2 == h2)
                res.pop("required_n_at_ic", None)
                cell["TS"] = res
            if cell:
                out["results"][f"{feat}|{label}"] = cell
    return out


# ---------------------------------------------------------------- survivors
def survivors(all_markets: list[dict]) -> list[dict]:
    surv = []
    for mk in all_markets:
        for key, cell in (mk.get("results") or {}).items():
            ts = cell.get("TS") or {}
            xs = cell.get("XS") or {}
            if ts.get("verdict") in ("PASS", "FAIL"):        # robust nonzero
                ic = ts.get("ic_spearman", 0.0)
                if abs(ic) < SURVIVOR_MIN_ABS_IC:
                    continue
                lono_ok = (ts.get("lono_ic") or {}).get("sign_stable", False)
                sh_ok = ts.get("split_half_same_sign", False)
                xs_ok = True
                if xs:
                    xs_ok = np.sign(xs.get("mean_ic", 0.0)) == np.sign(ic)
                if lono_ok and sh_ok and xs_ok:
                    feat, hz = key.split("|")
                    surv.append({"market": mk["market"], "feature": feat,
                                 "horizon": hz, "pooled_ic": ic,
                                 "n": ts.get("n"),
                                 "hit_rate": ts.get("hit_rate"),
                                 "xs_mean_ic": xs.get("mean_ic"),
                                 "tercile_spread_pct":
                                     xs.get("tercile_spread_mean_pct")})
    return surv


# ----------------------------------------------------------------- markdown
def to_md(payload: dict) -> str:
    L = ["# Direction-Signal Tournament — RESULTS (research only, not adopted)",
         "", f"Generated {payload['generated']}. Seed {SEED}, blocks "
         f"{list(BOOT_BLOCKS)}, {N_BOOT} bootstrap draws. Forward returns are "
         "excess of each market's own carry; dividends not netted (flagged).",
         "", "Verdict language: SIGNAL+/- = CI clear of zero on the same side "
         "across ALL blocks; PARITY = indistinguishable from zero; BOUNDARY = "
         "block-dependent; INSUFFICIENT-POWER = below the MIN_N=100 gate.", ""]
    for mk in payload["markets"]:
        if not mk.get("results"):
            L.append(f"## {mk['market']} — {mk.get('note', 'no results')}\n")
            continue
        L.append(f"## {mk['market']} — {mk['names']} names, "
                 f"{mk['date_range'][0]} → {mk['date_range'][1]}")
        if mk.get("skipped"):
            L.append(f"  (skipped: {len(mk['skipped'])})")
        L.append("")
        L.append("| candidate | horizon | pooled IC (TS) | TS verdict | hit rate "
                 "| XS mean IC | XS verdict | tercile spread %/period | "
                 "split-half OK |")
        L.append("|---|---|---|---|---|---|---|---|---|")
        for key, cell in mk["results"].items():
            feat, hz = key.split("|")
            ts, xs = cell.get("TS") or {}, cell.get("XS") or {}
            sh = ts.get("split_half_same_sign", xs.get("split_half_same_sign"))
            L.append("| {f} | {h} | {ic} | {tv} | {hr} | {xic} | {xv} | {sp} | {sh} |".format(
                f=feat, h=hz,
                ic=f"{ts['ic_spearman']:+.3f} (n={ts['n']})" if "ic_spearman" in ts else "—",
                tv=ts.get("verdict", "—"),
                hr=f"{ts['hit_rate']:.0%}" if "hit_rate" in ts else "—",
                xic=f"{xs['mean_ic']:+.3f} ({xs['n_dates']}d)" if xs else "—",
                xv=xs.get("verdict", "—"),
                sp=(f"{xs['tercile_spread_mean_pct']:+.2f} "
                    f"[{xs['tercile_spread_ci_pct'][0]:+.2f},"
                    f"{xs['tercile_spread_ci_pct'][1]:+.2f}]")
                    if xs.get("tercile_spread_mean_pct") is not None else "—",
                sh="yes" if sh else ("no" if sh is not None else "—")))
        L.append("")
    L.append("## Survivors (all four tests at once)")
    L.append("")
    if payload["survivors"]:
        for s in payload["survivors"]:
            L.append(f"- **{s['feature']} @ {s['horizon']} in {s['market']}** — "
                     f"pooled IC {s['pooled_ic']:+.3f} on n={s['n']}, hit rate "
                     f"{s['hit_rate']:.0%}, cross-sectional IC "
                     f"{(s['xs_mean_ic'] or float('nan')):+.3f}, tercile spread "
                     f"{s['tercile_spread_pct'] if s['tercile_spread_pct'] is not None else float('nan'):+.2f}%/period.")
    else:
        L.append("- NONE. No candidate cleared robustness + LONO stability + "
                 "split-half consistency + cross-framing agreement in any "
                 "market at pooled n>=100.")
    L += ["", "A survivor here is a CANDIDATE for the standing promotion gate, "
          "never an adoption."
          + ("" if payload["survivors"] else
             " An empty list is itself a publishable finding: short-horizon "
             "direction is not recoverable from price history in these "
             "markets by these six constructions."), ""]
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", default=os.path.join(ENG, "direction_tournament",
                                                   "RESULTS.json"))
    ap.add_argument("--md", default=os.path.join(ENG, "direction_tournament",
                                                 "RESULTS.md"))
    ap.add_argument("--generated", default=None,
                    help="ISO date stamped into the output (defaults to git's "
                         "view of today via the environment)")
    args = ap.parse_args()
    generated = args.generated or str(pd.Timestamp.now().date())

    markets = []
    for market in sorted(os.listdir(RAW)):
        folder = os.path.join(RAW, market)
        if not os.path.isdir(folder):
            continue
        tickers = sorted(f[:-4] for f in os.listdir(folder) if f.endswith(".csv"))
        if not tickers:
            continue
        print(f"[{market}] {len(tickers)} names …", flush=True)
        markets.append(run_market(market, tickers))

    payload = {"generated": generated, "seed": SEED,
               "boot": {"blocks": list(BOOT_BLOCKS), "draws": N_BOOT},
               "status": "RESEARCH ONLY — not adopted, not published",
               "markets": markets, "survivors": survivors(markets)}
    with open(args.json, "w") as f:
        json.dump(payload, f, indent=1, default=str)
    with open(args.md, "w") as f:
        f.write(to_md(payload))
    print(f"wrote {args.json}\nwrote {args.md}")
    print(f"survivors: {len(payload['survivors'])}")


if __name__ == "__main__":
    main()
