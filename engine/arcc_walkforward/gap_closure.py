"""Does disagreeing with the price carry information?  [R-VCAL-01] series (ii).

THE QUESTION THIS ANSWERS, AND IT IS NOT THE ONE THE PROGRAMME HAS BEEN ANSWERING.
Every gate and criterion in this repository asks whether a fair value AGREES with
today's price. That is series (i), and the pre-registration is explicit that it
cannot settle anything on its own: "a house can be systematically pessimistic and
right; it can also be systematically pessimistic and merely wrong. Only this series
separates them."

Series (ii) asks the question that matters if a price is GUIDANCE rather than a
target: when the model disagrees with the market, does the market come to the model?
A price can sit away from fair value while sentiment runs, and the claim is that the
divergence is temporary. That claim is testable, and it is testable ON HISTORY —
not in June 2027, which is when the house's own PUBLISHED vintages mature.

THE INSTRUMENT IS DELIBERATELY SIMPLE AND SAYS SO. This is not the house valuation:
it is a fixed, transparent wrapper around the forecast — five years of projected
profit discounted at the origin's own cost of equity, a terminal at that rate against
the inflation the origin knew, and the net cash the balance sheet showed. Every
parameter is point-in-time and none is fitted. A simple wrapper is the right
instrument here BECAUSE the question is whether the FORECAST carries information; a
richer valuation would mix that with the judgement layered on top of it.

IT IS RUN TWICE — on the model's rules as they stand, and on the corrected rules of
driver_fixes.py — because "did fixing the drivers make the disagreement more
informative" is the only test of those fixes that speaks to what the house is for.
"""
from __future__ import annotations

import csv
import datetime as dt
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, ENGINE)

import bottom_up as B          # noqa: E402
import driver_fixes as F       # noqa: E402
import macro_history as MH     # noqa: E402

BETA = 1.00          # fixed, as everywhere else in this calibration
HZ = [1, 2, 3, 4, 5]


def prices():
    rows = []
    p = os.path.join(ENGINE, "raw_ohlc", "EG", "ARCC.csv")
    for r in csv.DictReader(open(p, encoding="utf-8-sig")):
        try:
            d = dt.datetime.strptime(r["Date"].strip().strip('"'), "%m/%d/%Y").date()
            rows.append((d, float(r["Price"].replace(",", ""))))
        except Exception:
            pass
    return sorted(rows)


PX = prices()


def close_at(year):
    """The last close on or before 31 December. Never forward into the next year."""
    cut = dt.date(year, 12, 31)
    best = None
    for d, v in PX:
        if d <= cut and (best is None or d > best[0]):
            best = (d, v)
    return best[1] if best else None


def cost_of_equity(year):
    v = MH.origin("EG", year)
    n = v.require("sovereign_10y", "default_spread", "erp")
    return n["sovereign_10y"] - n["default_spread"] + BETA * n["erp"]


def terminal_inflation(year):
    v = MH.origin("EG", year)
    fwd = (v.extras.get("cpi_annual") or {}).get("forward_path") or {}
    last = str(year + max(HZ))
    x = fwd.get(last)
    if x is None and fwd:
        x = fwd[max(fwd, key=lambda k: int(k))]
    return None if x is None else float(x)


def fair_value(A, o, fixed):
    """Five projected profits, a terminal, the balance sheet's net cash, per share."""
    oy = B._y(o)
    try:
        ke = cost_of_equity(oy)
    except Exception:
        return None, "no point-in-time cost of equity at this origin"
    g = terminal_inflation(oy)
    if g is None or ke - g <= 0:
        return None, "no usable terminal at this origin"
    cash, debt = F.blk(o, "cash"), F.blk(o, "debt")
    sh = (F.BLOCK.get(o) or {}).get("shares", {}).get("value")
    if cash is None or debt is None or not sh:
        return None, "the block carries no bridge at this origin"

    pv = 0.0
    last = None
    for h in HZ:
        try:
            p = dict(B.project(o, h))
        except Exception:
            return None, "the projection fails at horizon %d" % h
        p["_fx"] = 0.0
        if fixed:
            for _n, fn in F.FIXES:
                fn(A, o, h, p)
            p = F.rebuild(p, A, o)
        if p.get("pat") is None:
            return None, "no profit at horizon %d" % h
        pv += p["pat"] / (1 + ke) ** h
        last = p["pat"]
    tv = last * (1 + g) / (ke - g)
    pv += tv / (1 + ke) ** max(HZ)
    equity = pv + cash - debt
    return equity / sh, "ke %.1f%%, terminal g %.1f%%" % (100 * ke, 100 * g)


def run(fixed):
    A = {}
    for o in B.ORIGINS:
        try:
            A[o] = B.actual(o)
        except Exception:
            pass
    out = []
    for o in B.ORIGINS:
        oy = B._y(o)
        fv, why = fair_value(A, o, fixed)
        p0 = close_at(oy)
        if fv is None or not p0 or fv <= 0:
            continue
        gap = math.log(fv / p0)
        fwd = {}
        for h in (1, 2, 3):
            p1 = close_at(oy + h)
            if p1:
                fwd[h] = math.log(p1 / p0)
        out.append({"origin": oy, "fv": fv, "px": p0, "gap": gap, "fwd": fwd})
    return out


def corr(xs, ys):
    n = len(xs)
    if n < 3:
        return None
    mx, my = sum(xs) / n, sum(ys) / n
    sx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    sy = math.sqrt(sum((y - my) ** 2 for y in ys))
    if sx == 0 or sy == 0:
        return None
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / (sx * sy)


def report():
    print("DOES DISAGREEING WITH THE PRICE CARRY INFORMATION?  [R-VCAL-01] series (ii)\n")
    print("  A deliberately simple wrapper around the forecast — five projected")
    print("  profits at the origin's own cost of equity, a terminal on the inflation")
    print("  it knew, the balance sheet's net cash. Not the house valuation; the")
    print("  question is whether the FORECAST carries information.\n")
    for fixed in (False, True):
        rows = run(fixed)
        lab = "WITH THE CORRECTED DRIVER RULES" if fixed else "ON THE RULES AS THEY STAND"
        print("  ---- %s ----" % lab)
        if not rows:
            print("    no origin produced a value.\n")
            continue
        print("    %-7s %10s %9s %9s   %s"
              % ("origin", "fair value", "close", "gap", "return over 1 / 2 / 3 years"))
        for r in rows:
            f = " ".join(("%+6.0f%%" % (100 * (math.exp(r["fwd"][h]) - 1)))
                         if h in r["fwd"] else "      -" for h in (1, 2, 3))
            print("    %-7d %10.2f %9.2f %+8.0f%%   %s"
                  % (r["origin"], r["fv"], r["px"],
                     100 * (math.exp(r["gap"]) - 1), f))
        print()
        for h in (1, 2, 3):
            xs = [r["gap"] for r in rows if h in r["fwd"]]
            ys = [r["fwd"][h] for r in rows if h in r["fwd"]]
            c = corr(xs, ys)
            same = sum(1 for x, y in zip(xs, ys) if (x > 0) == (y > 0))
            print("      %d-year: %d origin(s), correlation %s, gap and return agree in "
                  "sign on %d of %d"
                  % (h, len(xs), ("%+.2f" % c) if c is not None else "n/a — too few",
                     same, len(xs)))
        print()


if __name__ == "__main__":
    report()
