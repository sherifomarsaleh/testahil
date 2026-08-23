"""tilt_backtest_93.py — the adopted committed-drift tilt, backtested through
the PRODUCTION engine for the full 93-ticker library over its whole history
(23-Aug-2026, per instruction).

What runs: mc_v3.backtest_v3 — the same walk-forward machinery the standing
calibration gate uses — per ticker, per calendar horizon (1M and 3M), twice:
signal ON (the adopted config: mom_combo in AE/EG, mom_12_1 in SA, per-horizon
ic via profile.ic_by_h, dead 0.25 / clip 2.5 / cap 0.75σ) and signal OFF
(carry-only, the pre-adoption engine). Seeds are per-origin inside
backtest_v3, so the ON-vs-OFF difference is seed-paired by construction.

Reported per stock and pooled per market:
  * CRPS skill difference ON−OFF (scale-normalised per origin) — does the
    tilt help or hurt the whole distribution;
  * pinball@50 difference — does the tilted CENTER beat the carry center;
  * coverage of the 50/80/90 bands under ON — the tilt must not break
    calibration;
  * call hit rate on tilted origins (sign of alpha vs realised excess move)
    and the tilted share of origins.

The six non-committed markets (IN/KR/QA/US/XAU/XPT) run carry-only in
production — their tilt backtest is identical to OFF by construction, so they
are listed as such rather than burned as compute; their signal-level per-stock
record lives in PER_STOCK_CAREFUL_23-08-2026.

HONESTY CAVEAT, stated up front: the signal's DIRECTION is out-of-sample
validated (tournament: split-half, LONO, blocks). The IC MAGNITUDES used for
the tilt were measured on this same 15-year sample, so the tilt sizes are
in-sample-calibrated; the live monthly grading is their forward test. This
file measures whether the adopted tilt would have helped or hurt the
production forecasts over history — it is a fidelity check, not a second
independent discovery.

Usage:
    python3 engine/direction_tournament/tilt_backtest_93.py \
        --json OUT.json --md OUT.md [--n-paths 6000] [--workers N]
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import warnings
from multiprocessing import Pool, cpu_count

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
ENG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ENG)

COMMITTED = ("AE", "EG", "SA")
NOT_COMMITTED = ("IN", "KR", "QA", "US", "XAU", "XPT")
N_PATHS = 6000


def _load(mkt, tk):
    from data_quality import clean_ohlc
    df = pd.read_csv(os.path.join(ENG, "raw_ohlc", mkt, f"{tk}.csv"))
    df["Date"] = pd.to_datetime(df["Date"], format="%m/%d/%Y")
    for c in ("Price", "Open", "High", "Low"):
        df[c] = df[c].astype(str).str.replace(",", "", regex=False).astype(float)
    df = df.sort_values("Date").reset_index(drop=True)
    df, _ = clean_ohlc(df, ticker=tk, verbose=False, market=mkt)
    return df


def run_one(job):
    mkt, tk, n_paths = job
    from market_profiles import PROFILES
    from mc_v3 import backtest_v3
    prof = PROFILES[mkt]
    try:
        df = _load(mkt, tk)
    except Exception as e:
        return {"market": mkt, "ticker": tk, "error": str(e)}
    out = {"market": mkt, "ticker": tk, "horizons": {}}
    for hm in (1, 3):
        try:
            r_on = backtest_v3(df, prof, horizon_months=hm, use_signal=True,
                               n_paths=n_paths)
            r_off = backtest_v3(df, prof, horizon_months=hm, use_signal=False,
                                n_paths=n_paths)
        except Exception as e:
            out["horizons"][f"{hm}M"] = {"error": str(e)}
            continue
        n = min(len(r_on), len(r_off))
        if n < 8:
            out["horizons"][f"{hm}M"] = {"n": int(n), "note": "insufficient"}
            continue
        a, b = r_on.iloc[:n], r_off.iloc[:n]
        spot = a["spot"].values
        d_crps = float(np.mean((b["crps"].values - a["crps"].values) / spot))
        d_pin = float(np.mean((b["pin50"].values - a["pin50"].values) / spot))
        act = a[a["alpha"] != 0]
        hit = None
        if len(act) >= 5:
            ex = np.log(act["realized"].values / act["spot"].values) \
                - (act["drift"].values - act["alpha"].values)
            hit = float(np.mean(np.sign(act["alpha"].values) == np.sign(ex)))
        out["horizons"][f"{hm}M"] = {
            "n": int(n),
            "tilted_share": round(float(len(act)) / n, 3),
            "crps_gain_per_spot": round(d_crps, 5),
            "pin50_gain_per_spot": round(d_pin, 5),
            "cov50_on": round(float(a["in50"].mean()), 3),
            "cov80_on": round(float(a["in80"].mean()), 3),
            "cov90_on": round(float(a["in90"].mean()), 3),
            "cov90_off": round(float(b["in90"].mean()), 3),
            "call_hit_tilted": round(hit, 3) if hit is not None else None,
        }
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", required=True)
    ap.add_argument("--md", required=True)
    ap.add_argument("--n-paths", type=int, default=N_PATHS)
    ap.add_argument("--workers", type=int, default=max(2, cpu_count() - 2))
    args = ap.parse_args()

    jobs = []
    for mkt in COMMITTED:
        for f in sorted(os.listdir(os.path.join(ENG, "raw_ohlc", mkt))):
            if f.endswith(".csv"):
                jobs.append((mkt, f[:-4], args.n_paths))
    print(f"{len(jobs)} committed-market tickers, {args.workers} workers, "
          f"{args.n_paths} paths", flush=True)

    results = []
    with Pool(args.workers) as pool:
        for i, res in enumerate(pool.imap_unordered(run_one, jobs), 1):
            results.append(res)
            print(f"[{i}/{len(jobs)}] {res['market']} {res['ticker']} done",
                  flush=True)

    skipped = [{"market": m, "ticker": f[:-4],
                "note": "carry-only in production — no tilt adopted (no "
                        "robust market-level evidence); ON==OFF by construction"}
               for m in NOT_COMMITTED
               if os.path.isdir(os.path.join(ENG, "raw_ohlc", m))
               for f in sorted(os.listdir(os.path.join(ENG, "raw_ohlc", m)))
               if f.endswith(".csv")]

    payload = {"generated": "2026-08-23", "n_paths": args.n_paths,
               "status": "production-fidelity backtest of the adopted tilt",
               "committed": results, "not_committed": skipped}
    with open(args.json, "w") as fh:
        json.dump(payload, fh, indent=1)

    # ---------------- markdown ----------------
    L = ["# Committed tilt — full production backtest, 93 tickers (23-Aug-2026)",
         "",
         "The engine's own walk-forward backtest (backtest_v3), per ticker, "
         "both calendar clocks, signal ON (adopted config) vs OFF "
         "(carry-only), seed-paired. 'CRPS gain' and 'center gain' are "
         "per-origin improvements from the tilt, in units of price (positive "
         "= the tilt helped). Coverage under ON shows the tilt does not "
         "break the bands. The six non-committed markets run carry-only in "
         "production (tilt backtest identical to OFF by construction) — "
         "signal-level per-stock records for them are in "
         "PER_STOCK_CAREFUL_23-08-2026.", ""]
    grand = {}
    for mkt in COMMITTED:
        rows = sorted((r for r in results if r["market"] == mkt and
                       "error" not in r), key=lambda r: r["ticker"])
        errs = [r for r in results if r["market"] == mkt and "error" in r]
        L.append(f"## {mkt} — {len(rows)} tickers"
                 + (f" ({len(errs)} errored)" if errs else ""))
        L.append("")
        L.append("| stock | clock | obs | tilted share | CRPS gain | "
                 "center gain | call hit (tilted) | cov90 ON | cov90 OFF |")
        L.append("|---|---|---|---|---|---|---|---|---|")
        for r in rows:
            for hz in ("1M", "3M"):
                h = r["horizons"].get(hz, {})
                if "n" not in h or h.get("note"):
                    L.append(f"| {r['ticker']} | {hz} | {h.get('n', '—')} | — "
                             f"| — | — | — | — | — |")
                    continue
                grand.setdefault((mkt, hz), []).append(h)
                L.append("| {t} | {hz} | {n} | {ts:.0%} | {cg:+.5f} | "
                         "{pg:+.5f} | {hit} | {c9:.0%} | {c9o:.0%} |".format(
                             t=r["ticker"], hz=hz, n=h["n"],
                             ts=h["tilted_share"],
                             cg=h["crps_gain_per_spot"],
                             pg=h["pin50_gain_per_spot"],
                             hit=f"{h['call_hit_tilted']:.0%}"
                                 if h["call_hit_tilted"] is not None else "—",
                             c9=h["cov90_on"], c9o=h["cov90_off"]))
        L.append("")
    L.append("## Pooled summary (committed markets)")
    L.append("")
    L.append("| market | clock | stocks | CRPS gain (mean) | center gain "
             "(mean) | stocks helped | call hit (pooled) | cov90 ON (mean) |")
    L.append("|---|---|---|---|---|---|---|---|")
    for (mkt, hz), hs in sorted(grand.items()):
        cg = [h["crps_gain_per_spot"] for h in hs]
        pg = [h["pin50_gain_per_spot"] for h in hs]
        hits = [(h["call_hit_tilted"], h["n"] * h["tilted_share"])
                for h in hs if h["call_hit_tilted"] is not None]
        pooled_hit = (sum(h * w for h, w in hits) / sum(w for _, w in hits)
                      if hits else None)
        L.append("| {m} | {hz} | {k} | {cg:+.5f} | {pg:+.5f} | {help}/{k} | "
                 "{hit} | {c9:.0%} |".format(
                     m=mkt, hz=hz, k=len(hs),
                     cg=float(np.mean(cg)), pg=float(np.mean(pg)),
                     help=sum(1 for x in cg if x > 0),
                     hit=f"{pooled_hit:.0%}" if pooled_hit is not None else "—",
                     c9=float(np.mean([h["cov90_on"] for h in hs]))))
    L.append("")
    L.append("Caveat (stated in the file header too): direction is "
             "out-of-sample validated; tilt magnitudes are in-sample "
             "calibrated — live monthly grading is their forward test.")
    with open(args.md, "w") as fh:
        fh.write("\n".join(L))
    print(f"wrote {args.json}\nwrote {args.md}")


if __name__ == "__main__":
    main()
