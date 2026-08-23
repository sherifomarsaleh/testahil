"""merge_tilt_results.py — combine the committed-market (78) and hypothetical
(15) tilt backtests into the single 93-ticker report (23-Aug-2026).

Also fixes a rendering gap in tilt_backtest_93.to_md, which only drew
COMMITTED-market sections: here every market actually run is rendered, with
hypothetical markets clearly labelled.
"""
from __future__ import annotations

import argparse
import json

import numpy as np

ORDER = ("AE", "EG", "SA", "IN", "KR", "QA", "US", "XAU", "XPT")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--main", required=True, help="committed-market JSON")
    ap.add_argument("--extra", required=True, help="hypothetical JSON")
    ap.add_argument("--json", required=True)
    ap.add_argument("--md", required=True)
    args = ap.parse_args()

    with open(args.main) as f:
        a = json.load(f)
    with open(args.extra) as f:
        b = json.load(f)
    rows = a["committed"] + b["committed"]      # field name from the runner
    payload = {"generated": "2026-08-23",
               "status": "full 93-ticker tilt backtest (production config for "
                         "AE/EG/SA; hypothetical, labelled, elsewhere)",
               "n_paths": a["n_paths"], "results": rows}
    with open(args.json, "w") as f:
        json.dump(payload, f, indent=1)

    L = ["# Committed tilt — full backtest, all 93 tickers (23-Aug-2026)", "",
         "The engine's own walk-forward backtest, per ticker, both calendar "
         "clocks, tilt ON vs OFF, seed-paired, full history. AE/EG/SA run "
         "the ADOPTED production configuration. The six other markets run "
         "the technique HYPOTHETICALLY at the most conservative adopted "
         "strength — production applies no tilt there; those rows are "
         "evidence about extending the commitment, not live behavior. "
         "'CRPS gain' / 'center gain': per-origin improvement from the tilt "
         "in units of price (positive = tilt helped). cov90 shows the bands "
         "stay honest under the tilt.", ""]
    pooled = {}
    n_total, n_err = 0, 0
    for mkt in ORDER:
        sect = sorted((r for r in rows if r["market"] == mkt),
                      key=lambda r: r["ticker"])
        if not sect:
            continue
        hypo = any(r.get("hypothetical") for r in sect)
        L.append(f"## {mkt} — {len(sect)} tickers — "
                 + ("HYPOTHETICAL (not committed in production)" if hypo
                    else "production configuration"))
        L.append("")
        L.append("| stock | clock | obs | tilted share | CRPS gain | "
                 "center gain | call hit (tilted) | cov90 ON | cov90 OFF |")
        L.append("|---|---|---|---|---|---|---|---|---|")
        for r in sect:
            n_total += 1
            if "error" in r:
                n_err += 1
                L.append(f"| {r['ticker']} | — | — | — | error | — | — | — | — |")
                continue
            for hz in ("1M", "3M"):
                h = r["horizons"].get(hz, {})
                if "n" not in h or h.get("note") or h.get("error"):
                    L.append(f"| {r['ticker']} | {hz} | {h.get('n', '—')} | — "
                             f"| — | — | — | — | — |")
                    continue
                pooled.setdefault((mkt, hz, hypo), []).append(h)
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
    L.append("## Pooled summary")
    L.append("")
    L.append("| market | mode | clock | stocks | CRPS gain (mean) | center "
             "gain (mean) | stocks helped | call hit (pooled) | cov90 ON |")
    L.append("|---|---|---|---|---|---|---|---|---|")
    for (mkt, hz, hypo), hs in sorted(pooled.items(),
                                      key=lambda kv: (ORDER.index(kv[0][0]),
                                                      kv[0][1])):
        cg = [h["crps_gain_per_spot"] for h in hs]
        pg = [h["pin50_gain_per_spot"] for h in hs]
        hits = [(h["call_hit_tilted"], h["n"] * h["tilted_share"])
                for h in hs if h["call_hit_tilted"] is not None]
        ph = (sum(x * w for x, w in hits) / sum(w for _, w in hits)
              if hits else None)
        L.append("| {m} | {mode} | {hz} | {k} | {cg:+.5f} | {pg:+.5f} | "
                 "{hp}/{k} | {hit} | {c9:.0%} |".format(
                     m=mkt, mode="hypo" if hypo else "prod", hz=hz, k=len(hs),
                     cg=float(np.mean(cg)), pg=float(np.mean(pg)),
                     hp=sum(1 for x in cg if x > 0),
                     hit=f"{ph:.0%}" if ph is not None else "—",
                     c9=float(np.mean([h["cov90_on"] for h in hs]))))
    L.append("")
    L.append(f"Tickers covered: {n_total} (errors: {n_err}). Caveat: signal "
             "direction is out-of-sample validated; tilt magnitudes are "
             "in-sample calibrated — live monthly grading is their forward "
             "test.")
    with open(args.md, "w") as f:
        f.write("\n".join(L))
    print(f"wrote {args.json}\nwrote {args.md}\ntickers: {n_total}, errors: {n_err}")


if __name__ == "__main__":
    main()
