"""The mis-specified driver rules on AMOC, fixed and measured.

WHY THIS RUN AND WHY THIS RULE. engine/valuation_calibration/macro_share.py
measured, on cells scoreable in every setting, that AMOC's devaluation-year MAE
is 51% macro -- handed the realised Brent and the realised pound the bias goes
from -0.707 to +0.327 -- while ARCC's is not macro at all. The transmission is
sound; what is wrong is the KNOWABLE path.

THE DEFECT, IN THE MODULE'S OWN CODE. bottom_up.brent_ratio() returns exactly 1.0
outside foresight, so crude-in-EGP is held FLAT -- and crude is both this
company's product and, as feedstock, most of its cost of sales. Only salaries,
supporting materials, other cost of sales, G&A and marketing compound cpi_path().

IT IS A NOMINAL FREEZE, NOT AN ASYMMETRY, AND THE FIRST DRAFT OF THIS FILE SAID
OTHERWISE. That draft called it [L-048] -- costs escalating while revenue sits
still, one event counted once and ignored once -- which is the shape this house
has seen most often and is the wrong diagnosis here. Measured rather than read
(engine/valuation_calibration/clock_test.py): over three years AMOC's projected
revenue escalates x1.00 and its cost of sales x1.02, against the model's own
cumulative inflation of x1.24. BOTH SIDES ARE FROZEN. The two clocks differ by
two points; what differs by twenty-four is the whole model against the economy
it says it believes in. Across the book no run has a two-clock gap wider than
0.11, and AMOC alone sits near 0.82 on BOTH clocks where EGCH, ARCC and TMGH sit
at or above 0.92 -- so the defect is a level, not a mismatch, and it is this run
that carries it. A company standing still in nominal terms inside an
economy inflating at 7.4% a year is declining in real terms by construction,
which is [R-MACRO-01]'s terminal-growth-below-inflation defect arriving in the
explicit window.

That also explains the setting that looks strangest: perfect CPI alone is WORSE
than knowing nothing (-1.136 against -0.707), because it raises the only lines
that were moving and leaves the frozen 88% exactly where it was, widening the
gap rather than closing it.

THE DIAGNOSIS IS MEASURED SEPARATELY FROM THE REMEDY, because they are two
different claims. Putting crude on the model's own inflation path -- not a claim
that consumer inflation is the right escalator for crude, simply a path instead
of a freeze -- takes the bias from -0.774 to -0.258 on 63 common cells. So most
of this run's lean is the freeze itself, before any question of which path is
right.

THE REMEDY INVENTS NO PARAMETER. [R-MACRO-01] already states the house currency
identity: relative purchasing-power parity on the path's own inflation against
long-run foreign inflation. The sister run EGCH implements exactly that
(fx_level(), relative PPP on the last published CPI differential) in the same
house, the same market and the same week. AMOC does not, and no reason for the
difference is recorded anywhere. So:

    crude in EGP moves by the PPP currency implied by THIS model's OWN inflation
    path, with the DOLLAR price of crude held flat.

Every piece is already committed or published: the Egyptian inflation path is
the model's own, the identity is the house's, and the only new input is US
consumer inflation, fetched by macro_us.py into its own file so that adding it
cannot re-fetch and silently move a delivered run's Egyptian series.

Holding the dollar price flat is ARCC's own registered reason, unchanged: a
commodity price has no drift, and assuming one would be a forecast rather than a
rule.

THE ADOPTED FIX SCORES WORSE THAN THE DIAGNOSTIC AND IS ADOPTED ANYWAY. On the
63 cells scoreable in every variant the freeze test comes out at -0.258 and
F8 at -0.443, both far better than the -0.774 as shipped. The freeze test is
NOT a candidate rule and must never become one: it escalates crude at Egyptian
consumer inflation, which is not a claim anybody would defend, and it scores
better only because that rate happens to compound faster than the PPP
differential over these particular years. Adopting it because it scores better
is the CRPS-selection mistake the promotion rule forbids, in a new costume. F8
is adopted because it is the house identity, and the diagnostic is kept beside
it because the gap between them is evidence about what remains unexplained.

WHAT REMAINS AFTER F8 IS THE USEFUL PART. The implied PPP currency path runs
1.06x over three years from FY2021 against a realised 2.42x, and 1.09x from
FY2022 against 2.72x. Relative purchasing-power parity is directionally right
and under-predicts a step devaluation by a factor of two to two and a half at
three years -- and nothing this house has is better, because a devaluation is a
policy decision rather than a drift. The residual -0.443 is therefore not a rule
waiting to be fixed. It is the size of the interval years three to five should
carry, which [R-FCAL-01] already requires and which is where this run's next
work goes.

    python3 driver_fixes.py
"""
from __future__ import annotations

import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bottom_up as B  # noqa: E402
import panel as P      # noqa: E402

DRIVERS = ["net_sales", "cost_of_sales", "gross_profit", "operating_profit",
           "pbt", "npat", "majority"]
DEVAL = {2022, 2023, 2024, 2025}

_US = json.load(open(os.path.join(HERE, "macro_us.json")))["cpi_us_pct_cy"]


def _y(o):
    return int(str(o)[2:])


def us_cpi_fy(fy_end_year):
    """US inflation on AMOC's own July-June fiscal convention -- the mean of the
    two calendar years the year spans, the identical DERIVED mapping macro.py
    already applies to every Egyptian series. Using a calendar rate against a
    fiscal one would put the two legs of a ratio on different clocks, which is
    the defect this whole file is about, one level down."""
    a, b = _US.get(str(fy_end_year - 1)), _US.get(str(fy_end_year))
    if a is None or b is None:
        return None
    return (a + b) / 200.0


def ppp_fx(origin, h):
    """EGP/USD(o+h) / EGP/USD(o) under relative PPP on the KNOWABLE differential.

    Knowable means the origin's own last published rates on both sides, held
    forward -- the same construction cpi_path() already uses for Egypt, so the
    two legs of the differential sit on the same vintage. An origin that cannot
    source one side returns None and the cell is left as shipped rather than
    filled (SIGCM clause 8: shorten the window, never invent the cell)."""
    pi_eg = B.FY[origin]["cpi_pct"] / 100.0
    pi_us = us_cpi_fy(_y(origin))
    if pi_us is None:
        return None
    return ((1.0 + pi_eg) / (1.0 + pi_us)) ** h


# ------------------------------------------------------------------ measurement
def _cells(brent_fn):
    orig = B.brent_ratio
    B.brent_ratio = brent_fn
    try:
        out = {}
        for o, h, t in B.cells():
            p = B.project(o, h)
            a = B.actual(t)
            for d in DRIVERS:
                pv, av = p.get(d), a.get(d)
                out[(o, h, d)] = (math.log(pv / av)
                                  if (pv and av and pv > 0 and av > 0) else None)
    finally:
        B.brent_ratio = orig
    return out


def _as_shipped(origin, h, foresight=False):
    return B._SHIPPED_BRENT(origin, h, foresight=foresight)


def _on_cpi(origin, h, foresight=False):
    if foresight:
        return B._SHIPPED_BRENT(origin, h, foresight=True)
    return B.cpi_path(origin, h, foresight=False)


def _on_ppp(origin, h, foresight=False):
    """F8 -- crude in EGP carries the currency the model's own inflation implies."""
    if foresight:
        return B._SHIPPED_BRENT(origin, h, foresight=True)
    m = ppp_fx(origin, h)
    return 1.0 if m is None else m


B._SHIPPED_BRENT = B.brent_ratio


def summarise(cells, keys):
    v = [cells[k] for k in keys]
    dv = [cells[k] for k in keys if _y(k[0]) + k[1] in DEVAL]
    other = [cells[k] for k in keys if _y(k[0]) + k[1] not in DEVAL]
    mn = lambda x: sum(x) / len(x) if x else None
    ma = lambda x: sum(abs(i) for i in x) / len(x) if x else None
    return {"n": len(v), "bias": mn(v), "mae": ma(v),
            "n_deval": len(dv), "bias_deval": mn(dv), "mae_deval": ma(dv),
            "n_other": len(other), "bias_other": mn(other), "mae_other": ma(other)}


def main():
    variants = [("as shipped (crude frozen in EGP)", _as_shipped),
                ("freeze test: crude on own CPI", _on_cpi),
                ("F8: crude on the PPP currency", _on_ppp)]
    got = {lab: _cells(fn) for lab, fn in variants}
    keys = [k for k in got[variants[0][0]]
            if all(got[lab][k] is not None for lab, _ in variants)]
    if not keys:
        raise SystemExit("FAIL: no cell is scoreable in every variant")

    res = {lab: summarise(got[lab], keys) for lab, _ in variants}
    print("AMOC driver fixes -- %d cells scoreable in every variant\n" % len(keys))
    print("%-34s %7s %6s | %7s %6s" % ("", "bias", "mae", "bias_dv", "mae_dv"))
    for lab, _ in variants:
        r = res[lab]
        f = lambda x: ("%+.3f" % x) if x is not None else "  -  "
        g = lambda x: ("%.3f" % x) if x is not None else "  -  "
        print("%-34s %7s %6s | %7s %6s"
              % (lab, f(r["bias"]), g(r["mae"]), f(r["bias_deval"]), g(r["mae_deval"])))

    print("\nThe PPP path this implies, against what happened:")
    print("%-8s %3s %10s %10s %8s" % ("origin", "h", "ppp mult", "realised", "ratio"))
    for o in B.ORIGINS:
        for h in (1, 3):
            m = ppp_fx(o, h)
            t = "FY%d" % (_y(o) + h)
            if m is None or t not in B.FY or "egp_usd" not in B.FY[t]:
                continue
            real = B.FY[t]["egp_usd"] / B.FY[o]["egp_usd"]
            print("%-8s %3d %10.3f %10.3f %8.2f" % (o, h, m, real, real / m))

    json.dump({"cells": len(keys), "variants": res},
              open(os.path.join(HERE, "driver_fixes.json"), "w"), indent=1)
    return res


if __name__ == "__main__":
    main()
