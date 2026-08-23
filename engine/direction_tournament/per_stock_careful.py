"""per_stock_careful.py — the committed-drift signal, per stock, at the house
evidential standard (23-Aug-2026, per instruction: "Do it per stock. This is
a delicate exercise and needs to be done carefully").

What "carefully" means here, pre-registered BEFORE the numbers were computed:

  * Per stock x horizon: the EXACT production signal (mc_v3.signal_z with the
    market's adopted signal_type), month-end origins, non-overlapping
    forwards, excess of the market's own carry.
  * Statistics per stock: Spearman rank IC with the house block-bootstrap
    verdict across blocks {2,3,4} (direction_score.robust_ic_verdict — PASS
    only if every block's CI clears zero above, FAIL only if every block
    clears below); direction hit rate with a Wilson interval; split-half
    consistency; conditional call record (mean forward return after UP calls
    vs after DOWN calls). Below n=24 no verdict is issued at all.
  * THE DISPOSITION RULE, fixed in advance: a stock's tilt is SUPPRESSED
    (alpha forced to 0; the call still prints, flagged low-confidence) if and
    only if, at either horizon: robust FAIL across all blocks AND split-half
    both-halves-negative AND n >= 40. Anything weaker — a contrary point
    estimate, a single-block excursion, an inconsistent split — is a WATCH
    FLAG: recorded, graded live, revisited at every refit, but not acted on.
    Rationale: with ~156 stock-horizon tests at 90% CIs, a few false robust
    reads are expected by chance alone; the joint rule keeps the expected
    false-suppression count well under one, and suppressing on less would be
    per-name curve-fitting — the exact failure mode the standing promotion
    rule exists to prevent.
  * Names too young for the signal are reported as such, never guessed.

Usage:
    python3 engine/direction_tournament/per_stock_careful.py \
        --json OUT.json --md OUT.md
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

from market_profiles import PROFILES                     # noqa: E402
from mc_v3 import signal_z                               # noqa: E402
from tournament import load_clean, month_end_grid, split_half  # noqa: E402
import direction_score as ds                             # noqa: E402

MIN_N_VERDICT = 24
MIN_N_SUPPRESS = 40
COMMITTED = ("AE", "EG", "SA")   # markets where the tilt is adopted
RAW = os.path.join(ENG, "raw_ohlc")
# All 93 covered tickers are tested. In non-committed markets the same
# momentum-family construction (mom_combo) is tested per stock as an
# EVIDENCE RECORD ONLY — it documents both each stock's own read and why
# those markets carry no committed tilt.
MARKETS = tuple(sorted(m for m in os.listdir(RAW)
                       if os.path.isdir(os.path.join(RAW, m))
                       and any(f.endswith(".csv")
                               for f in os.listdir(os.path.join(RAW, m)))))


def market_kind(market: str) -> str:
    if market in COMMITTED:
        return PROFILES[market].signal_type
    return "mom_combo"


def series_obs(market: str, ticker: str):
    df = load_clean(market, ticker)
    if df is None:
        return None
    grid = month_end_grid(df)
    if len(grid) < 14:
        return None
    prof = PROFILES[market]
    kind = market_kind(market)
    dates = df["Date"].values
    close = df["Price"].values.astype(float)
    gd = grid["Date"].values
    gp = grid["Price"].values.astype(float)
    didx = np.searchsorted(dates, gd)
    out = {}
    for h, step in ((1, 1), (3, 3)):
        zs, fw, dts = [], [], []
        for i in range(0, len(gd) - h, step):
            j = int(didx[i])
            z = signal_z(close, j, kind)
            if z == 0.0 and j < 260:
                continue
            d0, d1 = pd.Timestamp(gd[i]), pd.Timestamp(gd[i + h])
            rf = prof.carry_rate(d0)
            carry = np.log(1 + rf) * ((d1 - d0).days / 365.25)
            fwd = float(np.log(gp[i + h] / gp[i]) - carry)
            if np.isfinite(fwd) and z != 0.0:
                zs.append(z)
                fw.append(fwd)
                dts.append(d0)
        out[f"{h}M"] = (np.asarray(zs), np.asarray(fw),
                        np.asarray(dts, dtype="datetime64[ns]"))
    return out


def score_stock(zs, fw, dts):
    n = len(zs)
    rec = {"n": int(n)}
    if n < 8:
        rec["verdict"] = "insufficient"
        return rec
    ic = float(stats.spearmanr(zs, fw).statistic)
    hits = int(np.sum(np.sign(zs) == np.sign(fw)))
    lo_h, hi_h = ds.wilson(hits, n)
    up, dn = fw[zs > 0], fw[zs < 0]
    rec.update(
        ic=round(ic, 3),
        hit=round(hits / n, 3), hit_ci=[round(lo_h, 3), round(hi_h, 3)],
        after_up_pct=round(float(np.expm1(np.mean(up)) * 100), 2) if len(up) >= 5 else None,
        after_down_pct=round(float(np.expm1(np.mean(dn)) * 100), 2) if len(dn) >= 5 else None,
    )
    verdict, detail = ds.robust_ic_verdict(zs, fw)
    rec["blocks"] = {str(b): {"lo": round(detail[b][0], 3),
                              "hi": round(detail[b][1], 3),
                              "v": detail[b][2]} for b in ds.BOOT_BLOCKS}
    h1, h2 = split_half(dts, np.sign(zs) * fw)
    rec["split_half"] = [round(h1, 4), round(h2, 4)]
    rec["split_both_neg"] = bool(h1 < 0 and h2 < 0)
    rec["split_same_sign"] = bool(np.sign(h1) == np.sign(h2))
    if n < MIN_N_VERDICT:
        rec["verdict"] = "short history"
    elif verdict == "PASS":
        rec["verdict"] = "supports (robust)"
    elif verdict == "FAIL":
        rec["verdict"] = "contrary (robust)"
    elif verdict.startswith("BOUNDARY"):
        rec["verdict"] = "borderline"
    else:
        rec["verdict"] = "indeterminate"
    rec["suppress_test"] = bool(verdict == "FAIL" and rec["split_both_neg"]
                                and n >= MIN_N_SUPPRESS)
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", required=True)
    ap.add_argument("--md", required=True)
    args = ap.parse_args()

    results, suppress, watch = {}, [], []
    for market in MARKETS:
        folder = os.path.join(ENG, "raw_ohlc", market)
        results[market] = {"signal": market_kind(market),
                           "committed": market in COMMITTED, "names": {}}
        for f in sorted(os.listdir(folder)):
            if not f.endswith(".csv"):
                continue
            tk = f[:-4]
            obs = series_obs(market, tk)
            if obs is None:
                results[market]["names"][tk] = {"note": "series too short"}
                continue
            rec = {}
            for hz, (zs, fw, dts) in obs.items():
                rec[hz] = score_stock(zs, fw, dts)
            results[market]["names"][tk] = rec
            trig = [hz for hz in ("1M", "3M")
                    if rec.get(hz, {}).get("suppress_test")
                    and market in COMMITTED]
            if trig:
                suppress.append({"market": market, "ticker": tk, "at": trig,
                                 "detail": {hz: rec[hz] for hz in trig}})
            else:
                for hz in ("1M", "3M"):
                    v = rec.get(hz, {}).get("verdict", "")
                    if v in ("contrary (robust)", "borderline") or \
                       (v == "indeterminate" and (rec[hz].get("ic") or 0) < -0.05):
                        watch.append({"market": market, "ticker": tk,
                                      "horizon": hz, "ic": rec[hz].get("ic"),
                                      "verdict": v})
            print(market, tk, "done", flush=True)

    payload = {"generated": "2026-08-23",
               "rule": ("suppress iff robust FAIL all blocks + split-half both "
                        "halves negative + n>=40, at either horizon; else "
                        "watch-flag only"),
               "suppressions": suppress, "watch_flags": watch,
               "markets": results}
    with open(args.json, "w") as fh:
        json.dump(payload, fh, indent=1)

    # ---------- markdown ----------
    L = ["# Committed drift — careful per-stock dossier (23-Aug-2026)", "",
         "Exact production signal per market; per stock: rank skill with the "
         "house robust bootstrap (blocks {2,3,4}), direction hit rate with a "
         "Wilson interval, split-half consistency, and the plain call record "
         "(average move after UP calls vs after DOWN calls, per period, "
         "above cash). Disposition rule fixed BEFORE computing: suppress a "
         "stock's tilt only on robust-contrary + both-halves-negative + "
         "n≥40; weaker contrary reads are watch-flags, graded live.", ""]
    for market in MARKETS:
        blk = results[market]
        tag = ("committed tilt" if blk["committed"]
               else "NOT committed — evidence record only")
        L.append(f"## {market} — signal {blk['signal']} — {tag}")
        L.append("")
        L.append("| stock | clock | obs | rank skill | robust verdict | "
                 "hit rate (95% CI) | after UP calls | after DOWN calls | "
                 "split-half OK |")
        L.append("|---|---|---|---|---|---|---|---|---|")
        for tk in sorted(blk["names"]):
            rec = blk["names"][tk]
            if "note" in rec:
                L.append(f"| {tk} | — | — | — | {rec['note']} | — | — | — | — |")
                continue
            for hz in ("1M", "3M"):
                r = rec.get(hz, {})
                if r.get("verdict") == "insufficient" or "ic" not in r:
                    L.append(f"| {tk} | {hz} | {r.get('n', 0)} | — | "
                             f"insufficient | — | — | — | — |")
                    continue
                L.append("| {tk} | {hz} | {n} | {ic:+.3f} | {v} | "
                         "{hit:.0%} ({lo:.0%}–{hi:.0%}) | {au} | {ad} | {sh} |".format(
                             tk=tk, hz=hz, n=r["n"], ic=r["ic"], v=r["verdict"],
                             hit=r["hit"], lo=r["hit_ci"][0], hi=r["hit_ci"][1],
                             au=f"{r['after_up_pct']:+.1f}%" if r["after_up_pct"] is not None else "—",
                             ad=f"{r['after_down_pct']:+.1f}%" if r["after_down_pct"] is not None else "—",
                             sh="yes" if r["split_same_sign"] else "no"))
        L.append("")
    L.append("## Dispositions")
    L.append("")
    if suppress:
        for s in suppress:
            L.append(f"- **SUPPRESS TILT — {s['ticker']} ({s['market']})** at "
                     f"{', '.join(s['at'])}: robust-contrary on every test at "
                     "once. Tilt forced to zero; call still prints, flagged "
                     "low-confidence; revisited at every refit.")
    else:
        L.append("- **No stock met the suppression bar.** No tilt is switched "
                 "off; the market-level signal stands for every name.")
    if watch:
        L.append("")
        L.append("Watch-flags (contrary or borderline, below the bar — "
                 "recorded and graded live, not acted on):")
        for w in watch:
            L.append(f"  - {w['ticker']} ({w['market']}, {w['horizon']}): "
                     f"rank skill {w['ic']:+.3f}, {w['verdict']}")
    L.append("")
    L.append(f"Multiplicity note: ~{sum(len(b['names']) for b in results.values()) * 2} "
             "stock-horizon tests at 90% CIs imply a handful of false single-test "
             "excursions by chance; the joint suppression rule keeps the expected "
             "false-suppression count well under one.")
    with open(args.md, "w") as fh:
        fh.write("\n".join(L))
    print(f"wrote {args.json}\nwrote {args.md}")
    print(f"suppressions: {len(suppress)}; watch flags: {len(watch)}")


if __name__ == "__main__":
    main()
