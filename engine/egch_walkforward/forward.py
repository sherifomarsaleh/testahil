"""EGCH (KIMA) walk-forward — what this record licenses the study to say about years 3–5.

[R-FCAL-01] requires the delivered study to publish years 3–5 as RANGES built from this
record's own driver-error distribution, never as points. Fifty-five cells over thirteen
origins give 13/12/11/10/9 observations at horizons 1–5 on the lines that are always
positive (revenue, cost of sales) and fewer on the profit lines (B-3). Empirical 10th
and 90th percentiles are printed where a horizon holds at least NINE observations and
refused below that; the bias ± MAE band and the min/max span are printed everywhere,
with the count beside every figure.

Two bands per line and horizon: the FULL record (evidence of record) and the KIMA-2 era
alone (origins FY2021+, the business the study actually values — few cells). The study
carries the WIDER of the two; a diagnostic may widen a published range and may never
narrow one.
"""
import os, sys, json, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import panel as P
import bottom_up as B
import score as S

KEYS = ["revenue", "cost_of_sales", "gross_profit", "pbt", "net"]
MIN_FOR_PCTL = 9


def band(vals):
    v = sorted(x for x in vals if x is not None)
    if not v:
        return None
    n = len(v)
    bias = sum(v) / n
    mae = sum(abs(x) for x in v) / n
    out = {"n": n, "bias": bias, "mae": mae, "min": v[0], "max": v[-1],
           "low_factor": math.exp(bias - mae), "high_factor": math.exp(bias + mae),
           "span_low_factor": math.exp(v[0]), "span_high_factor": math.exp(v[-1])}
    if n >= MIN_FOR_PCTL:
        def q(p):
            k = (n - 1) * p
            f, c = math.floor(k), math.ceil(k)
            return v[f] + (v[c] - v[f]) * (k - f)
        out["p10_factor"], out["p90_factor"] = math.exp(q(0.10)), math.exp(q(0.90))
    return out


def errors_by_h(rows, origins=None):
    out = {h: {k: [] for k in KEYS} for h in B.HORIZONS}
    for r in rows:
        if origins and r["origin"] not in origins:
            continue
        for k in KEYS:
            out[r["h"]][k].append(r["e"][k])
    return out


def main():
    rows = S.build_cells()
    e_all = errors_by_h(rows)
    e_k2 = errors_by_h(rows, origins=[o for o in B.ORIGINS if B.y(o) >= 2021])
    res = {"note": ("Ranges are MULTIPLIERS to apply to a point projection. A factor below 1.0 means the "
                    "record says the method came in BELOW the outturn and the point should be read as a "
                    "floor. Every figure carries its count; percentiles are printed only at n >= %d." % MIN_FOR_PCTL),
           "full_record": {str(h): {k: band(e_all[h][k]) for k in KEYS} for h in B.HORIZONS},
           "kima2_era": {str(h): {k: band(e_k2[h][k]) for k in KEYS} for h in B.HORIZONS}}
    pub = {}
    for h in B.HORIZONS:
        pub[str(h)] = {}
        for k in KEYS:
            a, b = res["full_record"][str(h)][k], res["kima2_era"][str(h)][k]
            if not a:
                continue
            lo = a.get("p10_factor", a["low_factor"])
            hi = a.get("p90_factor", a["high_factor"])
            if b:
                lo, hi = min(lo, b["low_factor"]), max(hi, b["high_factor"])
            pub[str(h)][k] = {"n_full": a["n"], "n_kima2": b["n"] if b else 0, "low_factor": lo,
                              "high_factor": hi, "width_x": hi / lo,
                              "basis": ("p10-p90 of the full record" if "p10_factor" in a else "bias +/- MAE of the full record")
                                       + ", widened by the KIMA-2-era bias +/- MAE band where that is wider"}
    res["published_band"] = pub
    res["published_band_rule"] = ("The wider of the full-record band and the KIMA-2-era band, per horizon per line. "
                                  "The full record is the evidence; the era band cannot narrow a published range.")
    json.dump(res, open(os.path.join(HERE, "forward_ranges.json"), "w"), indent=1, default=str)
    return res


if __name__ == "__main__":
    r = main()
    print("FORWARD RANGES — multiplicative bands this record supports\n")
    print("%-14s %-2s %-34s %-30s %-24s" % ("line", "h", "full record", "KIMA-2 era", "PUBLISHED"))
    for k in KEYS:
        for h in ("1", "2", "3", "4", "5"):
            a, b, p = r["full_record"][h][k], r["kima2_era"][h][k], r["published_band"][h].get(k)
            fa = ("x%.2f-x%.2f p10-p90 (n=%d)" % (a["p10_factor"], a["p90_factor"], a["n"]) if a and "p10_factor" in a
                  else ("x%.2f-x%.2f bias+/-MAE (n=%d)" % (a["low_factor"], a["high_factor"], a["n"]) if a else "n/a"))
            fb = ("x%.2f-x%.2f (n=%d)" % (b["low_factor"], b["high_factor"], b["n"])) if b else "n/a"
            fp = ("x%.2f-x%.2f (%.1fx)" % (p["low_factor"], p["high_factor"], p["width_x"])) if p else "n/a"
            print("%-14s %-2s %-34s %-30s %-24s" % (k if h == "1" else "", h, fa, fb, fp))
