"""ABUK fundamental walk-forward — the calibrated ranges the study must publish.

[R-FCAL-01] says years 3-5 are published as RANGES built from THIS record's own
driver-error distribution, never as points.  This file produces those bands.

They are multiplicative and horizon-specific: a band for horizon h is the
empirical 10th and 90th percentile of exp(-e) over the cells at that horizon,
where e is the log error the model actually made.  exp(-e) rather than exp(e)
because the band is applied to a FORECAST to bracket the OUTCOME, and the error
was measured forecast-over-actual.

THE BANDS ARE WIDE AND THAT IS THE POINT.  A five-year band on net profit that
runs from a third to three times the central is what six origins of measured
error on this name actually support; publishing a point would assert a precision
the record does not contain.
"""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
DRIVERS = ["vol_proxy", "rev", "cogs", "gp", "sell", "admin", "nonop", "pbt", "np"]


def pct(xs, p):
    xs = sorted(xs)
    if not xs:
        return None
    if len(xs) == 1:
        return xs[0]
    k = p * (len(xs) - 1)
    lo, hi = int(math.floor(k)), int(math.ceil(k))
    return xs[lo] + (xs[hi] - xs[lo]) * (k - lo)


def main():
    sc = json.load(open(os.path.join(HERE, "scores.json")))
    cells = sc["model"]["cells"]
    cells_mp = sc["macro_perfect"]["cells"]
    out = {"_what_this_is": (
        "Multiplicative bands on a forecast, from this run's own measured error. "
        "Apply band[driver][h] to the study's central path for that driver at "
        "horizon h. Built from 20 scoreable cells across six origins; at h=4 and "
        "h=5 the cell count is 3 and 2, so those bands rest on very few "
        "observations and the study says so beside them."),
        "_which_band_the_study_uses": (
        "TWO bands are produced and the study must not choose freely between "
        "them. `bands` is the RAW error, and on this name it is dominated by the "
        "pound: the model held the exchange rate flat at each origin while the "
        "currency went from 17.3 to 47.3 to the dollar, so the raw band says "
        "'multiply by two to four' when what it means is 'the currency will "
        "devalue again'. A forward model that already carries an explicit "
        "exchange-rate path and applies the raw band would count the same "
        "devaluation twice. `bands_macro_conditioned` is the error measured with "
        "the actual macro path substituted — the COMPANY-only error — and that is "
        "the band a study with its own FX path must use. The raw band applies "
        "only to a model whose currency assumption is itself a flat random walk."),
        "bands": {}, "bands_macro_conditioned": {}, "pooled_3_to_5": {},
        "pooled_3_to_5_macro_conditioned": {}}
    for src, bkey, pkey in (("raw", "bands", "pooled_3_to_5"),
                            ("mp", "bands_macro_conditioned",
                             "pooled_3_to_5_macro_conditioned")):
     use = cells if src == "raw" else cells_mp
     for d in DRIVERS:
        out[bkey][d] = {}
        pooled = []
        for h in range(1, 6):
            es = [c["logerr"] for c in use
                  if c["driver"] == d and c["h"] == h and c["logerr"] is not None]
            if not es:
                continue
            r = [math.exp(-e) for e in es]
            out[bkey][d][h] = dict(n=len(es), low=pct(r, 0.10), mid=pct(r, 0.50),
                                      high=pct(r, 0.90))
            if h >= 3:
                pooled += r
        if pooled:
            out[pkey][d] = dict(n=len(pooled), low=pct(pooled, 0.10),
                                           mid=pct(pooled, 0.50),
                                           high=pct(pooled, 0.90))
    json.dump(out, open(os.path.join(HERE, "forward_ranges.json"), "w"),
              indent=1, sort_keys=True, default=float)
    return out


if __name__ == "__main__":
    o = main()
    print("multiplicative band on the central forecast, by driver and horizon")
    print("%-10s %-24s %-24s %-24s" % ("driver", "h=1 (n=6)", "h=3 (n=4)", "h=5 (n=2)"))
    for d in DRIVERS:
        b = o["bands"][d]
        def f(h):
            if h not in b:
                return "-"
            return "%.2f - %.2f (mid %.2f)" % (b[h]["low"], b[h]["high"], b[h]["mid"])
        print("%-10s %-24s %-24s %-24s" % (d, f(1), f(3), f(5)))
    print("\npooled over horizons 3 to 5 — RAW band (a flat-FX model only)")
    for d in ("rev", "gp", "np"):
        p = o["pooled_3_to_5"][d]
        print("  %-4s n=%d  x%.2f to x%.2f, median x%.2f" % (
            d, p["n"], p["low"], p["high"], p["mid"]))
    print("\npooled over horizons 3 to 5 — MACRO-CONDITIONED band, which is what a")
    print("study carrying its own exchange-rate path must apply")
    for d in ("rev", "gp", "np"):
        p = o["pooled_3_to_5_macro_conditioned"][d]
        print("  %-4s n=%d  x%.2f to x%.2f, median x%.2f" % (
            d, p["n"], p["low"], p["high"], p["mid"]))
