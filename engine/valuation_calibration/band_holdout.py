"""Would the far-year ranges have held? Walk-forward, on five names.

[R-FCAL-01] requires a study carrying a fundamental walk-forward to publish years
three to five as RANGES from that record's own driver-error distribution. All five
runs do. NOTHING HAD EVER TESTED WHETHER THOSE RANGES HOLD.

THE OBVIOUS TEST CANNOT, AND THE SECOND-OBVIOUS TEST CANNOT EITHER. In-sample is
hopeless -- every run states its band as the observed span of the very cells the
band is built from, so coverage is 100% by construction. The first draft of this
file therefore used LEAVE-ONE-ORIGIN-OUT, the discipline this repository applies
to every fitted parameter, and IT MEASURED NOTHING: for a group of k+1 origins
each contributing one cell, the held-out value falls inside the min-max of the
other k exactly when it is not the overall minimum or maximum, so across all k+1
hold-outs exactly two fail, every time, whatever the data. Coverage is (k-1)/(k+1)
BY ARITHMETIC. It was caught only because the benchmark was computed rather than
typed, and it agreed with the observed figure to the last decimal place on five
names and five horizons -- five rows too clean to be a measurement.

THE TEST THAT WORKS IS THE ONE THAT MATCHES HOW A BAND IS USED. At each origin
the band is built from the origins STRICTLY BEFORE it and the next outturn is
asked whether it lands inside. Time-ordering breaks the symmetry that made the
leave-one-out version an identity, and it is also the only honest question: a
study published in 2022 could not have used 2024's error to set its band.

THE NULL IS THE SAME FORMULA AND NOW IT IS A NULL. If the errors were
exchangeable, a fresh draw falls inside the min-max span of k previous draws with
probability (k-1)/(k+1). It is computed per cell on that cell's own k, never
typed, because k varies by driver, horizon and name. Reading these against 90%
is the mistake this guards against: a span of four observations is not a 90%
interval however a document labels it.

Read live: python3 engine/valuation_calibration/band_holdout.py
"""
import os, sys, json, math

HERE = os.path.dirname(os.path.abspath(__file__))
ENG = os.path.dirname(HERE)
MIN_PRIOR = 3          # a band from two points is the two points

RUNS = {
    "ARCC": ("arcc_walkforward", "driver", "horizon", "log_error", "setting", "asknown", "origin"),
    "AMOC": ("amoc_walkforward", "driver", "horizon", "log_error", "setting", "asknown", "origin"),
    "EGCH": ("egch_walkforward", "driver", "horizon", "log_error", "setting", "asknown", "origin"),
    "TMGH": ("tmgh_walkforward", "driver", "horizon", "log_error", "setting", "asknown", "origin"),
    "PHDC": ("phdc_walkforward", "field", "h", "e", "setting", "as_known", "origin"),
}

PUBLISHED = {"revenue", "net_sales", "total_revenue", "new_sales", "sales",
             "cost_of_sales", "cos", "gross_profit", "pbt", "net_profit",
             "npat", "net", "majority", "volume_t", "urea_t", "vol_total"}


def _yr(o):
    d = "".join(c for c in str(o) if c.isdigit())
    return int(d[-4:]) if len(d) >= 4 else None


def load(name):
    d, dk, hk, ek, sk, sv, ok = RUNS[name]
    path = os.path.join(ENG, d, "error_cells.json")
    if not os.path.exists(path):
        return None
    raw = json.load(open(path))
    rows = []
    if isinstance(raw, dict):
        for setting, lst in raw.items():
            if setting == sv:
                rows.extend(lst)
    else:
        rows = [r for r in raw if r.get(sk) == sv]
    out = []
    for r in rows:
        e, drv = r.get(ek), str(r.get(dk, ""))
        y = _yr(r.get(ok))
        if e is None or drv not in PUBLISHED or y is None:
            continue
        out.append({"origin": y, "h": r.get(hk), "driver": drv, "e": float(e)})
    return out or None


def walk(cells):
    """Expanding-window band test. Returns per-cell records."""
    by = {}
    for c in cells:
        by.setdefault((c["driver"], c["h"]), {}).setdefault(c["origin"], []).append(c["e"])
    recs, thin = [], 0
    for (drv, h), origins in by.items():
        order = sorted(origins)
        for i, o in enumerate(order):
            prior = [v for oo in order[:i] for v in origins[oo]]
            k = i
            if k < MIN_PRIOR or not prior:
                thin += len(origins[o])
                continue
            lo, hi = min(prior), max(prior)
            for v in origins[o]:
                recs.append({"driver": drv, "h": h, "origin": o, "k": k,
                             "target": o + (h if isinstance(h, int) else 0),
                             "inside": lo <= v <= hi,
                             "expected": (k - 1.0) / (k + 1.0),
                             "below": v < lo, "above": v > hi})
    return recs, thin


def _binom_p(hits, n, p):
    """Two-sided exact binomial tail, the same test [R-CAL-02] publishes."""
    if n == 0:
        return None
    def pmf(i):
        return math.comb(n, i) * p ** i * (1 - p) ** (n - i)
    obs = pmf(hits)
    return min(1.0, sum(pmf(i) for i in range(n + 1) if pmf(i) <= obs * (1 + 1e-12)))


def summarise(recs):
    n = len(recs)
    if not n:
        return None
    inside = sum(1 for r in recs if r["inside"])
    exp = sum(r["expected"] for r in recs) / n
    return {"n": n, "inside": inside, "cov": inside / n, "expected": exp,
            "skill_pp": 100 * (inside / n - exp),
            "below": sum(1 for r in recs if r["below"]),
            "above": sum(1 for r in recs if r["above"]),
            "p": _binom_p(inside, n, exp)}


def main():
    allrecs, thin_total, missing = [], 0, []
    per_name = {}
    for name in sorted(RUNS):
        cells = load(name)
        if cells is None:
            missing.append(name)
            continue
        recs, thin = walk(cells)
        thin_total += thin
        per_name[name] = (summarise(recs), thin)
        allrecs.extend(recs)

    if not allrecs:
        raise SystemExit("FAIL: no cell was testable -- that is not a clean result")

    print("Walk-forward coverage of the published driver ranges")
    print("Band built from origins STRICTLY BEFORE each one; at least %d prior origins.\n" % MIN_PRIOR)
    print("%-6s %6s %7s %9s %9s %8s %7s %6s %6s   %s" %
          ("name", "n", "inside", "coverage", "expected", "skill", "p", "below", "above", "untestable"))
    for name in sorted(per_name):
        s, thin = per_name[name]
        if s is None:
            print("%-6s no testable cell (%d untestable)" % (name, thin)); continue
        print("%-6s %6d %7d %8.1f%% %8.1f%% %+7.1fpp %7s %6d %6d   %d" %
              (name, s["n"], s["inside"], 100 * s["cov"], 100 * s["expected"],
               s["skill_pp"], ("%.3f" % s["p"]) if s["p"] is not None else "-",
               s["below"], s["above"], thin))
    for name in missing:
        print("%-6s NOT READ -- no per-cell file" % name)

    p = summarise(allrecs)
    print("\nPOOLED  %d tested, %d inside, %.1f%% against an expected %.1f%%  (%+.1fpp, p=%.3f)"
          % (p["n"], p["inside"], 100 * p["cov"], 100 * p["expected"], p["skill_pp"], p["p"]))
    print("        misses: %d BELOW the band, %d above" % (p["below"], p["above"]))
    print("        %d cells untestable -- fewer than %d prior origins" % (thin_total, MIN_PRIOR))

    print("\nBy horizon:")
    print("%-5s %6s %7s %9s %9s %8s %6s %6s" %
          ("h", "n", "inside", "coverage", "expected", "skill", "below", "above"))
    for h in sorted({r["h"] for r in allrecs}, key=lambda x: (x is None, x)):
        s = summarise([r for r in allrecs if r["h"] == h])
        print("h=%-3s %6d %7d %8.1f%% %8.1f%% %+7.1fpp %6d %6d" %
              (h, s["n"], s["inside"], 100 * s["cov"], 100 * s["expected"],
               s["skill_pp"], s["below"], s["above"]))

    # THE BAND TEST IS NOT INDEPENDENT OF THE BREAK EFFECT AND SAYING SO IS THE
    # POINT. A band needs prior origins, so only the LATER origins are testable --
    # and on an Egyptian book the later origins are disproportionately the ones
    # whose windows ran into the devaluations. A pooled failure could therefore be
    # the band being too narrow, or simply the same break effect arriving in a new
    # instrument. Split it and the two are told apart.
    print("\nSplit by whether the year forecast was a devaluation year (2022-2025):")
    print("%-16s %6s %7s %9s %9s %8s %6s %6s" %
          ("", "n", "inside", "coverage", "expected", "skill", "below", "above"))
    for lab, sel in (("devaluation", lambda r: r["target"] in (2022, 2023, 2024, 2025)),
                     ("other years", lambda r: r["target"] not in (2022, 2023, 2024, 2025))):
        sub = [r for r in allrecs if sel(r)]
        if not sub:
            print("%-16s no cell" % lab); continue
        s2 = summarise(sub)
        print("%-16s %6d %7d %8.1f%% %8.1f%% %+7.1fpp %6d %6d" %
              (lab, s2["n"], s2["inside"], 100 * s2["cov"], 100 * s2["expected"],
               s2["skill_pp"], s2["below"], s2["above"]))

    print("\nEXPECTED is not 90%, and reading it as 90% is the mistake this guards against.")
    json.dump({"pooled": p, "per_name": {k: v[0] for k, v in per_name.items()},
               "untestable": thin_total, "min_prior": MIN_PRIOR},
              open(os.path.join(HERE, "band_holdout.json"), "w"), indent=1)
    return p


if __name__ == "__main__":
    main()
