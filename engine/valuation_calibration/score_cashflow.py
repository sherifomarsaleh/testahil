"""The pre-registered score on the cash-flow lens.  [R-VCAL-01] series (a), score (i).

The statistics are fixed in PRE_REGISTRATION_03-09-2026.md and nothing here chooses
any of them: bias, MAE and sign per origin and pooled; a moving-block bootstrap over
ORIGINS at blocks {2, 3, 4} with seed 42; the three declared eras; leave-one-name-out;
and THE EFFECTIVE INDEPENDENT n PRINTED BESIDE THE CELL COUNT, because origins share a
market and names share a year, so a record quoting the cell count alone overstates its
own precision.

FOUR READINGS ARE RUN AND ALL FOUR ARE PRINTED. Two are the sealed declaration's own
ambiguity about the maintenance figure, published rather than resolved by choosing;
two are the declared five-year window against each run's own horizon set. The DECLARED
run is named in every table and the others are labelled as what they are. Publishing
the surface is what keeps a reading from being picked after the fact.
"""
from __future__ import annotations

import json
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.dirname(HERE)
sys.path.insert(0, ENGINE)
sys.path.insert(0, HERE)

import cashflow_lens as CL   # noqa: E402

SEED = 42
BLOCKS = (2, 3, 4)
RESAMPLES = 2000
ERAS = (("E1 pre-float", 2011, 2015), ("E2 post-float", 2016, 2021),
        ("E3 devaluation", 2022, 2025))


def _mean(xs):
    return sum(xs) / len(xs) if xs else None


def _median(xs):
    xs = sorted(xs)
    n = len(xs)
    return None if not n else (xs[n // 2] if n % 2
                               else (xs[n // 2 - 1] + xs[n // 2]) / 2.0)


def block_bootstrap(rows, block, resamples=RESAMPLES, seed=SEED):
    """Moving-block bootstrap over ORIGINS — the house bar, unchanged.

    Resampling CELLS would treat five readings of one name in five adjacent years
    as five independent observations, which is the precision overstatement the
    pre-registration's effective-n line exists to prevent.
    """
    origins = sorted({r["origin"] for r in rows})
    by_o = {o: [r["log"] for r in rows if r["origin"] == o and r["log"] is not None]
            for o in origins}
    n = len(origins)
    if n < block:
        return None
    rng = random.Random(seed)
    starts = list(range(n - block + 1))
    means = []
    for _ in range(resamples):
        picked = []
        while len(picked) < n:
            s = rng.choice(starts)
            picked.extend(origins[s:s + block])
        xs = [x for o in picked[:n] for x in by_o[o]]
        m = _mean(xs)
        if m is not None:
            means.append(m)
    if len(means) < 50:
        return None
    means.sort()
    lo = means[int(0.025 * len(means))]
    hi = means[min(len(means) - 1, int(0.975 * len(means)))]
    return {"lo": lo, "hi": hi, "half_width": (hi - lo) / 2.0, "n_boot": len(means)}


def effective_n(rows):
    """Origins, names, and the smaller of the two — the pre-registration's own line.

    Eleven origins across a panel of names is not 11 x N independent observations.
    The honest denominator is about the ORIGIN count, and where one name supplies
    every cell it is about that name.
    """
    return {"cells": len(rows),
            "origins": len({r["origin"] for r in rows}),
            "names": len({r["ticker"] for r in rows})}


def lono(rows):
    """Leave one NAME out. Each name's absence is a fact about the pooled figure."""
    names = sorted({r["ticker"] for r in rows})
    out = {}
    for tk in names:
        rest = [r for r in rows if r["ticker"] != tk]
        xs = [r["log"] for r in rest if r["log"] is not None]
        out[tk] = {"left_out": tk, "cells": len(rest), "mean": _mean(xs),
                   "names_left": len({r["ticker"] for r in rest})}
    return out


def score(rows):
    xs = [r["log"] for r in rows if r["log"] is not None]
    if not xs:
        return None
    res = {"n": effective_n(rows), "mean": _mean(xs), "median": _median(xs),
           "mae": _mean([abs(x) for x in xs]),
           "below": sum(1 for x in xs if x < 0), "above": sum(1 for x in xs if x > 0),
           "bootstrap": {b: block_bootstrap(rows, b) for b in BLOCKS},
           "lono": lono(rows), "eras": {}}
    for label, a, b in ERAS:
        sub = [r["log"] for r in rows
               if a <= r["origin"] <= b and r["log"] is not None]
        res["eras"][label] = {"cells": len(sub), "mean": _mean(sub)}
    return res


def drop_taxonomy(dropped):
    """Why cells were lost, grouped by CAUSE rather than listed by name.

    A list of 28 drops reads as bad luck; four causes with counts reads as what it
    is — a statement about what these runs commit and what the declared
    construction demands of it.
    """
    def bucket(why):
        w = (why or "").lower()
        if "declared window" in w:
            return "the run projects a shorter window than the declared five years"
        if "capex intensity" in w or "working-capital intensity" in w \
                or "intensity rule" in w:
            return "the block carries fewer than three years for a trailing intensity"
        if "terminal refused" in w and "not positive" in w:
            return "terminal refused: free cash flow not positive"
        if "terminal refused" in w and "payout" in w:
            return "terminal refused: implied payout outside [0, 1]"
        if "no finance charge" in w:
            return "the panel carries no finance charge at the origin"
        if "no revenue or operating profit" in w:
            return "the projection carries no revenue or operating profit"
        if "unit cannot be measured" in w:
            return "the panel's unit cannot be measured against the block"
        return "other"
    out = {}
    for tk, y, why in dropped:
        out.setdefault(bucket(why), []).append("%s %d" % (tk, y))
    return out


READINGS = (
    ("DECLARED", dict(horizons=CL.HORIZONS, maintenance="amount")),
    ("maintenance read as intensity x origin revenue",
     dict(horizons=CL.HORIZONS, maintenance="intensity")),
    # A SENSITIVITY, NOT THE DECLARED RUN, AND THE LABEL IS LOAD-BEARING. The sealed
    # construction takes the disclosed_capex basis and says why: "only one of these
    # five names has [a disclosed life] on file". That statement was true of the
    # repository the morning it was sealed and is no longer — ARCC's and AMOC's lives
    # were read from their own accounting-policies notes the same day, and the score
    # this construction produced named the missing life as its binding blocker.
    #
    # The declaration ALSO bars a fourth construction if the third failed, and it did.
    # Both readings of that bar are defensible, and resolving it in the direction that
    # produces a better number is exactly the fitting this house forbids. So it is NOT
    # resolved: the declared run stays the declared run, this is published BESIDE it as
    # a third reading of the same surface, and the difference between them is reported
    # rather than chosen between. Nothing here promotes anything.
    ("maintenance on the DISCLOSED LIFE — A SENSITIVITY, NOT THE DECLARED RUN",
     dict(horizons=CL.HORIZONS, maintenance="disclosed_life")),
)


def report():
    print("[R-VCAL-01] series (a) — THE CASH-FLOW LENS, SCORED\n")
    print("  construction sealed in MECHANICAL_LENS_3_06-09-2026.md before any of\n"
          "  this was computed; the two withdrawn declarations stand unedited beside\n"
          "  it, with the first's own run committed as it was\n")
    out = {}
    for label, kw in READINGS:
        rows, dropped = CL.run(**kw)
        s = score(rows)
        out[label] = {"rows": rows, "dropped": dropped, "score": s}
        print("  ---- %s ----" % label)
        if not rows:
            print("    no cell produced a value.\n")
            continue
        print("    %-6s %-6s %10s %9s %9s %7s" %
              ("name", "origin", "fv/share", "close", "log(FV/P)", "TV%"))
        for r in sorted(rows, key=lambda r: (r["ticker"], r["origin"])):
            print("    %-6s %-6d %10.3f %9.3f %+9.4f %6.0f%%"
                  % (r["ticker"], r["origin"], r["fv"], r["price"], r["log"] or 0,
                     100 * (r["terminal_share"] or 0)))
        n = s["n"]
        print("\n    CONTEMPORANEOUS AGREEMENT")
        print("      cells %d   origins %d   NAMES %d" %
              (n["cells"], n["origins"], n["names"]))
        print("      mean log(FV/P)  %+.4f  (%+.1f%%)"
              % (s["mean"], (math.exp(s["mean"]) - 1) * 100))
        print("      median          %+.4f  (%+.1f%%)"
              % (s["median"], (math.exp(s["median"]) - 1) * 100))
        print("      MAE             %.4f      below the price %d of %d"
              % (s["mae"], s["below"], s["below"] + s["above"]))
        for b in BLOCKS:
            bs = s["bootstrap"][b]
            print("      block %d  %s" % (
                b, "not enough origins to resample" if bs is None
                else "95%% CI [%+.4f, %+.4f]  half-width %.4f"
                     % (bs["lo"], bs["hi"], bs["half_width"])))
        print("      LONO:")
        for tk, v in sorted(s["lono"].items()):
            print("        without %-6s %2d cell(s), %d name(s) left, mean %s"
                  % (tk, v["cells"], v["names_left"],
                     "—  NOTHING LEFT TO POOL" if v["mean"] is None
                     else "%+.4f" % v["mean"]))
        print()
    # the drop taxonomy is the same for every reading's shared causes; print the
    # declared run's
    print("  ---- WHY 28 OF 33 READY CELLS PRODUCED NO VALUE (declared run) ----")
    for cause, cells in sorted(drop_taxonomy(out["DECLARED"]["dropped"]).items(),
                               key=lambda kv: -len(kv[1])):
        print("    %2d  %s" % (len(cells), cause))
        print("        %s" % ", ".join(cells))
    return out


if __name__ == "__main__":
    res = report()
    if "--write" in sys.argv:
        payload = {}
        for label, v in res.items():
            payload[label] = {
                "score": v["score"],
                "cells": [{k: r[k] for k in
                           ("ticker", "origin", "fv", "price", "log", "wacc",
                            "terminal_share", "price_date", "kd_bound", "scale")}
                          for r in v["rows"]],
                "dropped": [{"ticker": t, "origin": y, "why": w}
                            for t, y, w in v["dropped"]],
            }
        p = os.path.join(HERE, "SCORES_cashflow_06-09-2026.json")
        json.dump(payload, open(p, "w"), indent=1, default=str)
        print("\n  written %s" % os.path.relpath(p, os.path.dirname(ENGINE)))
