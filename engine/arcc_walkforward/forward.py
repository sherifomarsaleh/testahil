"""ARCC walk-forward — the ranges years 3 to 5 are published as.

[R-FCAL-01] §6: the rebuilt study publishes years 3-5 as RANGES built from this
record's own driver-error distribution, never as points. This module computes
those ranges and nothing else.

THE RANGES ARE WIDE AND THEY REST ON VERY FEW OBSERVATIONS. At h=5 there are
three resolved cells; at h=4 there are four. A percentile of three numbers is
not a distribution, so the range at those horizons is reported as the MIN-MAX of
what was actually observed, with its count printed beside it, and the study says
so in the reader's own words. A number that cannot separate an honest forecast
from a broken one is not published as if it could.
"""
import os, sys, json, math

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bottom_up as B
import score as S

# The lines a reader of the study actually sees a forward number for.
PUBLISHED = ["revenue", "cogs", "gross_profit", "pbt", "pat", "vol_total",
             "price_local", "price_export", "raw_per_t"]


def errors_by_horizon(rows, driver):
    out = {}
    for h in B.HORIZONS:
        v = sorted(r["e"][driver] for r in rows
                   if r["h"] == h and r["e"][driver] is not None)
        if v:
            out[h] = v
    return out


def band(v):
    """The multiplicative band a projection should carry at this horizon.

    With this many observations a quantile is a fiction, so the band is the
    OBSERVED RANGE: the projection divided by the largest over-forecast and by
    the largest under-forecast. Reported with n, always."""
    lo, hi = min(v), max(v)
    return {"n": len(v), "mult_low": math.exp(-hi), "mult_high": math.exp(-lo),
            "median_mult": math.exp(-sorted(v)[len(v) // 2]),
            "mean_log_err": sum(v) / len(v)}


def run():
    rows, _ = S.run()
    out = {}
    for d in PUBLISHED:
        e = errors_by_horizon(rows, d)
        out[d] = {str(h): band(v) for h, v in e.items()}
    return out


if __name__ == "__main__":
    out = run()
    json.dump(out, open(os.path.join(HERE, "forward_ranges.json"), "w"), indent=1)
    print("Multipliers to apply to a mechanical projection, from THIS record's own errors.")
    print("A projection of X at horizon h should be read as the range")
    print("X x mult_low  ..  X x mult_high.  n is the number of resolved cells behind it.")
    print()
    print("%-14s %3s %5s %11s %11s %11s" % ("line", "h", "n", "mult_low", "median", "mult_high"))
    for d in PUBLISHED:
        for h in sorted(out[d], key=int):
            b = out[d][h]
            print("%-14s %3s %5d %11.3f %11.3f %11.3f"
                  % (d, h, b["n"], b["mult_low"], b["median_mult"], b["mult_high"]))
        print()
