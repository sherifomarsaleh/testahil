"""The recognition-clock defect on PHDC, measured in both framings.

WHY THIS RUN. PHDC is the one name of five that OVER-forecasts its own history
(+0.468 pooled on 160 cells here) and the one whose published central sits well
above the market. Every other name in this book under-forecasts. Whatever is
wrong here runs the opposite way to everything the reassessment was built around,
which is why it is worth locating precisely rather than corrected in bulk.

TWO OBSERVATIONS FIX THE SHAPE OF IT BEFORE ANY FIX IS TRIED.

 * THE BIAS DOES NOT COMPOUND. +0.459, +0.475, +0.479, +0.484, +0.439 at horizons
   one to five. A rate error compounds with the horizon -- that is what the
   under-forecasting names do, and it is the signature [R-TERM-01] was adopted
   on. A flat bias at every horizon is a LEVEL error: something multiplies the
   answer once and keeps multiplying it by the same amount.

 * THE LEVEL IS THE RECOGNITION RATE. delta = revenue / (opening backlog + new
   sales) is a trailing three-year mean held FLAT forward, which is the correct
   mechanical choice a priori and no judgement is involved. This company's
   realised delta fell monotonically from 0.3393 (2016) to 0.1104 (2024) as its
   backlog compounded far faster than it could deliver -- new sales went 8,194 to
   151,016 while revenue went 5,631 to 27,167 -- so the denominator grew 14.8x
   against revenue's 4.8x and the rate had to fall arithmetically. Every origin
   used a delta above what happened: 0.3336 against a realised 0.1436 three years
   out, 0.3244 against 0.1596, 0.2811 against 0.2041. Eight origins of eight in
   the same direction.

THE DEFECT IS [R-FCAL-01]'s TRAP (ii), NAMED IN THE STANDING RULE. Revenue is
delta x (backlog + new sales) -- a backlog-release clock. Cost is unit cost x
DELIVERIES -- a delivery clock. Two clocks, and the rule says in terms that
where revenue is recognised as work completes, cost must be too, or operating
leverage on a thin residual turns a gross-profit bias into a net-profit forecast
several times too high. That is exactly what is measured: revenue's own bias is
+0.107 and gross profit's is +0.540.

NEITHER DIRECTION IS ADOPTED HERE, AND THAT IS DELIBERATE. One clock can be
reached from either end and both are defensible, so both are published and
neither is averaged into the other -- the dual-framing rule. Choosing between
them changes a delivered study's answer and is a ruling, not a measurement.

    python3 driver_fixes.py
"""
from __future__ import annotations

import collections
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bottom_up as B  # noqa: E402

FIELDS = ["is.revenue", "is.cogs", "is.gross_profit", "is.npbt", "is.npat_mi"]
ORIGINS = range(2015, 2024)
MODES = ("shipped", "rev_on_deliveries", "cost_on_revenue")


def build(panel, mode):
    """Every cell under one framing. A mutation that fails to land RAISES rather
    than returning the shipped answer under a fix's label -- the negative-control
    discipline this repository applies to its gates, applied to its own
    measurements. An earlier draft of this file negated the cost line and the
    mutation silently produced non-positive cells that the log score dropped;
    the common-cell count fell from 160 to 39 and the table read as 'no change'."""
    out, landed = {}, 0
    for o in ORIGINS:
        try:
            pr = B.project(panel, o)
        except Exception:
            continue
        for h, f in (pr or {}).items():
            f = dict(f)
            d, a = f.get("units_delivered"), f.get("asp")
            rev0, cog0 = f.get("is.revenue"), f.get("is.cogs")
            if mode == "rev_on_deliveries" and d and a and rev0:
                new = d * a
                shift = new - rev0
                f["is.revenue"] = new
                landed += 1
                for k in ("is.gross_profit", "is.npbt", "is.npat_mi"):
                    if f.get(k) is not None:
                        f[k] = f[k] + shift
            elif mode == "cost_on_revenue" and d and a and rev0 and cog0:
                cpu = cog0 / d                  # the model's own unit cost that year
                new = cpu * (rev0 / a)          # costed on the units the revenue implies
                shift = new - cog0
                f["is.cogs"] = new
                landed += 1
                for k in ("is.gross_profit", "is.npbt", "is.npat_mi"):
                    if f.get(k) is not None:
                        f[k] = f[k] - shift
            for dd in FIELDS:
                pv = f.get(dd)
                av = (panel.get(o + h) or {}).get(dd)
                out[(o, h, dd)] = (math.log(pv / av)
                                   if (pv and av and pv > 0 and av > 0) else None)
    if mode != "shipped" and landed < 20:
        raise RuntimeError("mutation %r did not land (%d cells)" % (mode, landed))
    return out


def recognition_record(panel):
    """The realised delta by year, and the delta each origin actually used."""
    class V:
        def __init__(s, p, o):
            s.p, s.origin = p, o

        def get(s, y, f):
            return s.p.get(y, {}).get(f)

        def series(s, f):
            return {y: v[f] for y, v in s.p.items() if v.get(f) is not None}

    bl = B.rolled_backlog(V(panel, max(panel)))
    realised = {}
    for y in sorted(panel):
        rev, ns, b0 = (panel[y].get("is.revenue"), panel[y].get("new_sales"),
                       bl.get(y - 1))
        if rev is not None and ns is not None and b0 is not None and (b0 + ns) > 0:
            realised[y] = rev / (b0 + ns)
    used = {}
    for o in ORIGINS:
        try:
            r = B.recognition_rate(V(panel, o))
        except Exception:
            r = None
        # An origin with too little history to form the trailing mean returns
        # None. It is recorded as unavailable rather than dropped, so the table
        # says which origins could not form a rate [R-ENF-04].
        used[o] = r
    return realised, used


def main():
    panel = B.load()
    S = {m: build(panel, m) for m in MODES}
    keys = [k for k in S["shipped"] if all(S[m][k] is not None for m in MODES)]
    if not keys:
        raise SystemExit("FAIL: no cell scoreable in every framing")
    mn = lambda v: sum(v) / len(v)
    ma = lambda v: sum(abs(x) for x in v) / len(v)

    print("PHDC recognition clock -- %d cells scoreable in every framing\n" % len(keys))
    print("%-20s %8s %7s" % ("", "bias", "mae"))
    for m in MODES:
        v = [S[m][k] for k in keys]
        print("%-20s %+8.3f %7.3f" % (m, mn(v), ma(v)))

    print("\n%-18s %3s %9s %9s %9s" % ("driver", "n", "shipped", "rev-clk", "cost-clk"))
    for dd in FIELDS:
        sub = [k for k in keys if k[2] == dd]
        if not sub:
            continue
        print("%-18s %3d %9s %9s %9s"
              % (dd, len(sub),
                 *["%+.3f" % mn([S[m][k] for k in sub]) for m in MODES]))

    print("\n%-6s %3s %9s %9s %9s" % ("h", "n", "shipped", "rev-clk", "cost-clk"))
    by = collections.defaultdict(list)
    for k in keys:
        by[k[1]].append(k)
    for h in sorted(by):
        print("h=%-4s %3d %9s %9s %9s"
              % (h, len(by[h]),
                 *["%+.3f" % mn([S[m][k] for k in by[h]]) for m in MODES]))

    realised, used = recognition_record(panel)
    print("\nThe recognition rate, realised and used:")
    print("%-8s %10s %12s %12s" % ("origin", "used", "realised h1", "realised h3"))
    for o in sorted(used):
        print("%-8d %10s %12s %12s"
              % (o, ("%.4f" % used[o]) if used[o] is not None else "no history",
                 ("%.4f" % realised[o + 1]) if o + 1 in realised else "-",
                 ("%.4f" % realised[o + 3]) if o + 3 in realised else "-"))

    json.dump({"cells": len(keys),
               "framings": {m: {"bias": mn([S[m][k] for k in keys]),
                                "mae": ma([S[m][k] for k in keys])} for m in MODES},
               "recognition_realised": realised, "recognition_used": used},
              open(os.path.join(HERE, "driver_fixes.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
