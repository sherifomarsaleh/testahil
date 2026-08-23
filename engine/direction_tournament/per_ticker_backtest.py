"""per_ticker_backtest.py — the ADOPTED committed-drift signal, backtested for
each and every covered ticker in the three active markets (23-Aug-2026).

Investor due-diligence question: "have we backtested this technique for each
and every ticker?" This produces the per-name record of the EXACT production
construction — mc_v3.signal_z with each market's adopted signal_type
(mom_combo in AE/EG, mom_12_1 in SA) — at month-end origins, non-overlapping
forwards, excess of the market's own carry.

Honesty note baked into the output: a single name's history holds far fewer
observations than a market panel, so per-name numbers are DESCRIPTIVE — the
market-pooled tournament (with its leave-one-name-out check, so no single
name carries the verdict) is the statistical basis of the adoption. A name
whose own history reads contrary is listed plainly, not hidden.

Usage:
    python3 engine/direction_tournament/per_ticker_backtest.py \
        --json PER_TICKER.json --md PER_TICKER.md
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

from market_profiles import PROFILES        # noqa: E402
from mc_v3 import signal_z                  # noqa: E402
from tournament import load_clean, month_end_grid  # noqa: E402

MIN_N = 24            # below this a per-name read is "short history", full stop
FLAT_BAND = 0.03      # |IC| under this reads as flat


def run_name(market: str, ticker: str):
    df = load_clean(market, ticker)
    if df is None:
        return None
    grid = month_end_grid(df)
    if len(grid) < 14:
        return None
    prof = PROFILES[market]
    dates = df["Date"].values
    close = df["Price"].values.astype(float)
    gd = grid["Date"].values
    gp = grid["Price"].values.astype(float)
    didx = np.searchsorted(dates, gd)
    out = {}
    for h in (1, 3):
        zs, fw = [], []
        step = 1 if h == 1 else 3
        for i in range(0, len(gd) - h, step):
            j = int(didx[i])
            z = signal_z(close, j, prof.signal_type)
            if z == 0.0 and j < 260:
                continue                       # signal not yet defined
            d0, d1 = pd.Timestamp(gd[i]), pd.Timestamp(gd[i + h])
            rf = prof.carry_rate(d0)
            carry = np.log(1 + rf) * ((d1 - d0).days / 365.25)
            fwd = float(np.log(gp[i + h] / gp[i]) - carry)
            if np.isfinite(fwd):
                zs.append(z)
                fw.append(fwd)
        n = len(zs)
        if n < 8:
            out[f"{h}M"] = {"n": n, "verdict": "short history"}
            continue
        zs_a, fw_a = np.asarray(zs), np.asarray(fw)
        ic = float(stats.spearmanr(zs_a, fw_a).statistic)
        nz = zs_a != 0
        hit = float((np.sign(zs_a[nz]) == np.sign(fw_a[nz])).mean())
        if n < MIN_N:
            verdict = "short history"
        elif ic > FLAT_BAND:
            verdict = "supports"
        elif ic < -FLAT_BAND:
            verdict = "contrary"
        else:
            verdict = "flat"
        out[f"{h}M"] = {"n": n, "ic": round(ic, 3), "hit": round(hit, 3),
                        "verdict": verdict}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", required=True)
    ap.add_argument("--md", required=True)
    args = ap.parse_args()

    results = {}
    for market in ("AE", "EG", "SA"):
        folder = os.path.join(ENG, "raw_ohlc", market)
        results[market] = {"signal": PROFILES[market].signal_type, "names": {}}
        for f in sorted(os.listdir(folder)):
            if not f.endswith(".csv"):
                continue
            tk = f[:-4]
            try:
                r = run_name(market, tk)
            except Exception as e:
                r = {"error": str(e)}
            if r is not None:
                results[market]["names"][tk] = r
            print(market, tk, "done", flush=True)

    with open(args.json, "w") as fh:
        json.dump({"generated": "2026-08-23",
                   "status": "per-ticker record of the adopted signal",
                   "markets": results}, fh, indent=1)

    L = ["# Committed drift — per-ticker backtest (23-Aug-2026)", "",
         "The exact production signal per market (AE/EG: combined 6+12-month "
         "momentum; SA: 12-month momentum), each name's own full cleaned "
         "history, month-end origins, non-overlapping forwards, excess of "
         "carry. Per-name samples are small by nature — the market-pooled "
         "tournament (leave-one-name-out checked) is the statistical basis "
         "of the adoption; this table is the per-name due-diligence record, "
         "contrary names included.", ""]
    for market, blk in results.items():
        rows = blk["names"]
        L.append(f"## {market} — signal {blk['signal']} — {len(rows)} tickers")
        L.append("")
        L.append("| ticker | 1M obs | 1M hit | 1M rank skill | 1M verdict | "
                 "3M obs | 3M hit | 3M rank skill | 3M verdict |")
        L.append("|---|---|---|---|---|---|---|---|---|")
        counts = {"supports": 0, "flat": 0, "contrary": 0, "short history": 0}
        for tk in sorted(rows):
            r = rows[tk]
            if "error" in r:
                L.append(f"| {tk} | — | — | — | error | — | — | — | error |")
                continue
            c1, c3 = r.get("1M", {}), r.get("3M", {})
            counts[c3.get("verdict", "short history")] = \
                counts.get(c3.get("verdict", "short history"), 0) + 1
            L.append("| {tk} | {n1} | {h1} | {i1} | {v1} | {n3} | {h3} | {i3} | {v3} |".format(
                tk=tk,
                n1=c1.get("n", "—"),
                h1=f"{c1['hit']:.0%}" if "hit" in c1 else "—",
                i1=f"{c1['ic']:+.3f}" if "ic" in c1 else "—",
                v1=c1.get("verdict", "—"),
                n3=c3.get("n", "—"),
                h3=f"{c3['hit']:.0%}" if "hit" in c3 else "—",
                i3=f"{c3['ic']:+.3f}" if "ic" in c3 else "—",
                v3=c3.get("verdict", "—")))
        L.append("")
        L.append(f"3M summary: {counts['supports']} support · {counts['flat']} "
                 f"flat · {counts['contrary']} contrary · "
                 f"{counts['short history']} short-history")
        L.append("")
    with open(args.md, "w") as fh:
        fh.write("\n".join(L))
    print(f"wrote {args.json}\nwrote {args.md}")


if __name__ == "__main__":
    main()
