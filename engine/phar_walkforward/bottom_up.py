#!/usr/bin/env python3
"""PHAR — the ground-up build at every origin, exactly as pre-registered.

Rules R1-R13 of PRE_REGISTRATION_07-09-2026.md, implemented here and nowhere
else.  NO JUDGEMENT DRIVERS: every input to every rule is a figure published on
or before its own origin.

TWO TRAPS, OBEYED STRUCTURALLY RATHER THAN REMEMBERED:
  (i)  interest comes from panel.interest_bearing_debt() and from nothing else;
  (ii) revenue per pack and cost per pack take THE SAME escalator argument, so
       they cannot drift apart and the gross margin is an OUTPUT.
"""
from __future__ import annotations
import math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import panel, macro  # noqa: E402

ORIGINS = ["FY2020", "FY2021", "FY2022", "FY2023", "FY2024"]
HORIZONS = [1, 2, 3]
LAST = "FY2025"
UNIT_BAND = 0.02          # R1, stated in the pre-registration, not varied
ITERATIONS = 2            # R7, stated
PANEL_YEARS = sorted(panel.IS)


def yr(y):
    return int(y[2:6])


def fy(n):
    return "FY%d" % n


def k_at(o, series="panel"):
    """The trailing window, k = min(3, years of history available at the origin) —
    PER SERIES, exactly as the pre-registration's own parenthetical states it.

    Read as: the OLDEST year available within three years of the origin.  It is
    1 at FY2020 for an accounting driver, because the panel's earliest statement
    year is FY2019; 3 there for a KPI driver, because the FY2019 report publishes
    FY2018 and FY2017 is not needed.  THE PACKS SERIES HAS A HOLE AT FY2020 — the
    condensed COVID-year report publishes no packs figure — so at FY2023 the
    window is 2 rather than 3.  A hole SHORTENS the window; it is never bridged
    by interpolation, which would fabricate the very cell the error is scored on.
    """
    oy = yr(o)
    if series == "kpi":
        avail = {y for y in panel.KPI if panel.KPI[y]["packs_th"]}
    else:
        avail = set(panel.IS)
    for s in (3, 2, 1):
        if fy(oy - s) in avail:
            return s
    return 0


def cagr(series, o, k, field):
    a, b = fy(yr(o) - k), o
    va, vb = series[a][field], series[b][field]
    if not va or not vb or va <= 0 or vb <= 0:
        return None
    return (vb / va) ** (1.0 / k) - 1.0


def mean_ratio(o, k, num, den):
    """Trailing k-year mean of num/den, over the years INSIDE the driver's own
    definition window.  A year the driver does not exist in is skipped and the
    window shortens; the count is returned beside the mean so the record can say
    how many years each ratio rests on.  Zero years returns None, never a guess."""
    vals = []
    for n in range(yr(o) - k + 1, yr(o) + 1):
        y = fy(n)
        if y not in panel.IS:
            continue
        a, b = num(y), den(y)
        if a is None or b in (None, 0):
            continue
        vals.append(a / b)
    return (sum(vals) / len(vals)) if vals else None


# ---------------------------------------------------------------- the model
def project(o, leg="baseline"):
    """Build FY(o+1..o+3) at origin o under one of the three pre-registered legs."""
    k = k_at(o)
    kk = k_at(o, "kpi")
    oy = yr(o)
    IS, BS, CF, KPI = panel.IS, panel.BS, panel.CF, panel.KPI
    out = {}

    unit_build = KPI[o]["packs_th"] is not None and not IS[o]["condensed"]

    # --- R2/R5a escalator, per leg -------------------------------------
    def esc(h):
        if leg == "baseline":
            return base_esc
        if leg == "foresight" and (oy + h) not in macro.REALISED_CPI:
            return None      # beyond the realised series; the horizon is not built
        return macro.cpi_leg("knowable" if leg == "knowable" else "foresight", oy, oy + h)

    if leg == "baseline":
        if unit_build:
            base_esc = cagr({y: dict(p=KPI[y]["sales_th"] * 1000.0 / KPI[y]["packs_th"])
                             for y in sorted(KPI) if KPI[y]["packs_th"]}, o, kk, "p")
        else:
            base_esc = None
    else:
        base_esc = None
        if leg == "knowable" and macro.VINTAGE_CPI.get(oy) is None:
            return None      # UNMEASURED at this origin, by construction

    # --- R1 volume ------------------------------------------------------
    if unit_build:
        g_own = cagr(KPI, o, kk, "packs_th")
        g_pop = macro.population_growth(oy)
        g_units = max(g_pop - UNIT_BAND, min(g_pop + UNIT_BAND, g_own))
    else:
        g_units = None

    # --- R3 value-level revenue growth (FY2020 origin only) -------------
    if not unit_build:
        g_local = cagr({y: dict(v=KPI[y]["sales_th"] - KPI[y]["exports_th"])
                        for y in sorted(KPI) if KPI[y]["sales_th"]}, o, kk, "v")
        g_export = cagr(KPI, o, kk, "exports_th")

    # --- ratios held at the origin, or trailing means --------------------
    cons = panel.consolidation_ratio(o)                                   # R4
    p0 = (KPI[o]["sales_th"] * 1000.0 / KPI[o]["packs_th"]) if unit_build else None
    c0 = (IS[o]["cogs"] / cons / KPI[o]["packs_th"]) if unit_build else None
    cogs_ratio = IS[o]["cogs"] / IS[o]["revenue"]                         # R5b
    mkt_r = mean_ratio(o, k, lambda y: IS[y].get("marketing"), lambda y: IS[y]["revenue"])
    prov_r = mean_ratio(o, k, lambda y: IS[y].get("provisions"), lambda y: IS[y]["revenue"])
    exp_r = mean_ratio(o, k, lambda y: IS[y]["expenses_total"], lambda y: IS[y]["revenue"])
    other_r = mean_ratio(o, k, lambda y: IS[y]["other_block"], lambda y: IS[y]["revenue"])
    capex_r = mean_ratio(o, k, lambda y: CF[y]["capex"], lambda y: IS[y]["revenue"])
    wc_r = mean_ratio(o, k, lambda y: _wc(y), lambda y: IS[y]["revenue"])
    tax_r = mean_ratio(o, k, lambda y: IS[y]["income_tax"] + IS[y]["deferred_tax"] + IS[y]["takaful"],
                       lambda y: IS[y]["pbt"])
    admin0 = (IS[o].get("rnd", 0) + IS[o].get("ga", 0) + IS[o].get("board", 0)) or None
    debt0 = panel.interest_bearing_debt(o)
    dna0 = panel.dna(o)
    base0 = BS[o]["ppe"] + BS[o]["cip"]
    base_prev = BS[fy(oy - 1)]["ppe"] + BS[fy(oy - 1)]["cip"] if fy(oy - 1) in BS else None
    d_rate = (dna0 / base_prev) if (dna0 and base_prev) else None
    payout = mean_ratio(o, min(k, 3), lambda y: CF[y].get("dividends_paid"),
                        lambda y: IS[fy(yr(y) - 1)]["net_profit"] if fy(yr(y) - 1) in IS else None)
    r_debt = None
    if IS[o].get("finance") and debt0 and fy(oy - 1) in BS:
        r_debt = IS[o]["finance"] / ((debt0 + panel.interest_bearing_debt(fy(oy - 1))) / 2.0)

    # --- march the horizons ---------------------------------------------
    rev_prev, base_prev_h, debt_prev, np_prev = IS[o]["revenue"], base0, debt0, IS[o]["net_profit"]
    for h in HORIZONS:
        e = esc(h)
        if leg != "baseline" and e is None:
            break            # the escalator series ends here; earlier horizons stand
        row = {}
        # revenue
        if unit_build:
            if base_esc is None and leg == "baseline":
                return None
            u = KPI[o]["packs_th"] * (1 + g_units) ** h
            p = p0 * math.prod([(1 + esc(i)) for i in range(1, h + 1)])
            parent_rev = u * p
            row["units_th"] = u
            row["price_per_pack"] = p
        else:
            loc = (KPI[o]["sales_th"] - KPI[o]["exports_th"]) * (1 + g_local) ** h
            exp_ = KPI[o]["exports_th"] * (1 + g_export) ** h
            parent_rev = (loc + exp_) * 1000.0
        rev = parent_rev * cons
        row["revenue"] = rev
        # cost of sales, SAME clock
        if unit_build:
            c = c0 * math.prod([(1 + esc(i)) for i in range(1, h + 1)])
            row["cost_per_pack"] = c
            cogs = u * c * cons
        else:
            cogs = rev * cogs_ratio
        row["cogs"] = cogs
        row["gross_profit"] = rev - cogs        # AN OUTPUT
        # capex, capital base and D&A
        capex = capex_r * rev if capex_r else None
        row["capex"] = capex
        if d_rate is not None and capex is not None:
            dna = d_rate * base_prev_h
            base_now = base_prev_h + capex - dna
        else:
            dna, base_now = None, base_prev_h
        row["dna"] = dna
        # charges below gross profit, with the debt identity iterated
        debt_h, fin = debt_prev, None
        for _ in range(ITERATIONS):
            if r_debt is not None and debt_h is not None:
                fin = r_debt * ((debt_prev + debt_h) / 2.0)
            if IS[o]["condensed"]:
                expenses = exp_r * rev
            else:
                admin = admin0 * math.prod([(1 + esc(i)) for i in range(1, h + 1)])
                expenses = (mkt_r * rev) + admin + (prov_r * rev) + (fin or 0.0)
            other = other_r * rev
            pbt = (rev - cogs) - expenses + other        # R11: below-the-line is ZERO
            npf = pbt * (1 - tax_r)
            if capex is not None and wc_r is not None and dna is not None:
                div = (payout or 0.0) * np_prev
                dwc = wc_r * (rev - rev_prev)
                debt_h = max(0.0, debt_prev + capex + div + dwc - npf - dna)
        row["finance"] = fin
        row["expenses_total"] = expenses
        row["other_block"] = other
        row["pbt"] = pbt
        row["net_profit"] = npf
        row["debt"] = debt_h
        out[fy(oy + h)] = row
        rev_prev, base_prev_h, debt_prev, np_prev = rev, base_now, debt_h, npf
    return out


def _wc(y):
    b = panel.BS[y]
    return (b["inventory"] + b["ar"] + b["other_rec"]) - (b["ap"] + b["other_cl"])


# ---------------------------------------------------------------- benchmarks
FIELDS = ["revenue", "cogs", "gross_profit", "expenses_total", "other_block",
          "pbt", "net_profit", "units_th", "price_per_pack", "cost_per_pack",
          "finance", "capex", "dna", "debt"]


def actual(y):
    IS, CF, KPI = panel.IS, panel.CF, panel.KPI
    cons = panel.consolidation_ratio(y)
    a = dict(revenue=IS[y]["revenue"], cogs=IS[y]["cogs"], gross_profit=IS[y]["gross_profit"],
             expenses_total=IS[y]["expenses_total"], other_block=IS[y]["other_block"],
             pbt=IS[y]["pbt"], net_profit=IS[y]["net_profit"],
             finance=IS[y].get("finance"), capex=CF[y]["capex"], dna=panel.dna(y),
             debt=panel.interest_bearing_debt(y))
    if KPI[y]["packs_th"]:
        a["units_th"] = KPI[y]["packs_th"]
        a["price_per_pack"] = KPI[y]["sales_th"] * 1000.0 / KPI[y]["packs_th"]
        a["cost_per_pack"] = IS[y]["cogs"] / cons / KPI[y]["packs_th"]
    return a


def freeze(o):
    a = actual(o)
    return {fy(yr(o) + h): dict(a) for h in HORIZONS}


def trend(o):
    """Every line grown at its own trailing k-year compound growth rate."""
    k, oy = k_at(o), yr(o)
    out = {}
    a0 = actual(o)
    g = {}
    for f, v in a0.items():
        kf = k if f not in ("units_th", "price_per_pack") else k_at(o, "kpi")
        if fy(oy - kf) not in panel.IS:
            g[f] = None
            continue
        prev = actual(fy(oy - kf)).get(f)
        g[f] = ((v / prev) ** (1.0 / kf) - 1.0) if (v and prev and v > 0 and prev > 0) else None
    for h in HORIZONS:
        out[fy(oy + h)] = {f: (v * (1 + g[f]) ** h if (v is not None and g.get(f) is not None)
                               else None) for f, v in a0.items()}
    return out


if __name__ == "__main__":
    panel.assert_all()
    for o in ORIGINS:
        p = project(o)
        print("=== origin %s  (k=%d)" % (o, k_at(o)))
        for y, r in p.items():
            if y not in panel.IS:
                continue
            a = actual(y)
            print("   %s  rev %12.0f vs %12.0f   gp %12.0f vs %12.0f   np %11.0f vs %11.0f"
                  % (y, r["revenue"], a["revenue"], r["gross_profit"], a["gross_profit"],
                     r["net_profit"], a["net_profit"]))
