"""EGCH (KIMA) walk-forward — diagnosis.

Four jobs, none of which chooses anything:

  1. Decompose the net-profit error into its lines, and the revenue error into
     realisation (all years) and volume vs realisation (unit window).
  2. A SCALE-FREE profit error — (projected − actual) / actual revenue — so that the
     cells the log score must exclude (B-3: a non-positive side) are still visible.
     This is a DIAGNOSTIC specified after the pre-registered record existed (L-042):
     it is reported beside the log record and never replaces it.
  3. The currency-path test: the pre-registered knowable path moves the pound by PPP;
     Egypt held the pound through FY2017–FY2021 and then devalued in steps. Every origin
     is re-run with the currency FROZEN (AMOC's defect, here as the counterfactual) so
     the cost of the coherent path is measured rather than asserted.
  4. The plant-replacement split: the same record with every cell whose target lies in
     FY2020–FY2022 (the commissioning years) set aside, so the reader can see how much of
     the error is the method and how much is a business that ceased to exist.
"""
import os, sys, json, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import panel as P
import bottom_up as B
import score as S

LINES = ["revenue", "cost_of_sales", "selling", "admin", "provisions", "other_bucket", "fx",
         "investment_income", "credit_interest", "debit_interest", "tax_current"]
SIGN = {"revenue": 1, "cost_of_sales": -1, "selling": -1, "admin": -1, "provisions": -1,
        "other_bucket": 1, "fx": 1, "investment_income": 1, "credit_interest": 1,
        "debit_interest": -1, "tax_current": -1}


def frozen_fx_project(origin, h):
    """The AMOC-style path: domestic CPI compounds, the currency and urea stay flat."""
    o = P.actual(origin)
    cpi = B.cpi_path(origin, h)
    out = dict(revenue=o["revenue"], cost_of_sales=o["cost_of_sales"] * cpi,
               selling=(o["selling"] * cpi) if o["selling"] else o["selling"],
               admin=o["admin"] * cpi, provisions=o["provisions"], other_bucket=o["other_bucket"],
               fx=0.0, investment_income=o["investment_income"], credit_interest=o["credit_interest"])
    r = B.borrowing_rate(origin)
    Bt = P.borrowings_total(origin)
    out["debit_interest"] = o["debit_interest"] if (r is None or Bt is None) else r * Bt
    out["gross_profit"] = out["revenue"] - out["cost_of_sales"]
    if any(out[k] is None for k in LINES if k != "tax_current"):
        out["pbt"] = out["net"] = None
        return out
    out["pbt"] = sum(SIGN[k] * out[k] for k in LINES if k != "tax_current")
    out["tax_current"] = P.TAX_REGIME[origin] * max(out["pbt"], 0)
    out["net"] = out["pbt"] - out["tax_current"]
    return out


def scaled(rows_proj, key="net"):
    """(proj − actual) / actual revenue, over every cell where both exist."""
    v = []
    for o, h, t in B.cells():
        p, a = rows_proj(o, h), P.actual(t)
        if p.get(key) is None or a.get(key) is None:
            continue
        v.append({"origin": o, "h": h, "target": t, "err": (p[key] - a[key]) / a["revenue"]})
    return v


def summarise(v):
    if not v:
        return None
    x = [r["err"] for r in v]
    return {"n": len(x), "bias": sum(x) / len(x), "mae": sum(abs(e) for e in x) / len(x),
            "share_over": sum(1 for e in x if e > 0) / len(x)}


def main():
    res = {}
    # --- 1. decomposition of the net-profit error, in EGP thousand scaled by target revenue
    dec = []
    for o, h, t in B.cells():
        p, a = B.project(o, h), P.actual(t)
        if p.get("net") is None or a.get("net") is None:
            continue
        rev = a["revenue"]
        d = {k: SIGN[k] * (p[k] - a[k]) / rev for k in LINES}
        d["reval_gain"] = -a["reval_gain"] / rev
        d["total"] = (p["net"] - a["net"]) / rev
        d.update(origin=o, h=h, target=t)
        dec.append(d)
    res["net_decomposition_cells"] = dec
    res["net_decomposition_mean"] = {k: sum(r[k] for r in dec) / len(dec) for k in LINES + ["reval_gain", "total"]}
    res["net_decomposition_mean_abs"] = {k: sum(abs(r[k]) for r in dec) / len(dec) for k in LINES + ["reval_gain", "total"]}

    # revenue: realisation only (no tonnes outside the unit window); unit window volume vs realisation
    unit = []
    for o, h, t in B.cells():
        if o in P.UREA_TONNES and t in P.UREA_TONNES:
            to, tt = P.UREA_TONNES[o]["t"], P.UREA_TONNES[t]["t"]
            ro, rt = P.actual(o)["revenue"] / to, P.actual(t)["revenue"] / tt
            unit.append({"origin": o, "h": h, "target": t, "volume_effect": math.log(tt / to),
                         "realisation_effect": math.log(rt / ro), "total": math.log(P.actual(t)["revenue"] / P.actual(o)["revenue"])})
    res["revenue_unit_window"] = unit

    # --- 2. scale-free profit error, three bases
    bases = {"prereg": lambda o, h: B.project(o, h),
             "foresight": lambda o, h: B.project(o, h, foresight=True),
             "frozen_fx": frozen_fx_project,
             "freeze": lambda o, h: B.freeze(o, h)}
    res["scaled_profit_error"] = {}
    for name, fn in bases.items():
        res["scaled_profit_error"][name] = {k: summarise(scaled(fn, k)) for k in ("gross_profit", "pbt", "net")}
    # skill on the scaled error against freeze
    res["scaled_skill_vs_freeze"] = {}
    for k in ("gross_profit", "pbt", "net"):
        fz = res["scaled_profit_error"]["freeze"][k]["mae"]
        res["scaled_skill_vs_freeze"][k] = {b: 1 - res["scaled_profit_error"][b][k]["mae"] / fz
                                            for b in ("prereg", "foresight", "frozen_fx")}

    # --- 3. currency-path test on the log record
    keys = ["revenue", "cost_of_sales", "gross_profit", "pbt", "net"]
    comp = {k: {"prereg": [], "frozen_fx": [], "foresight": []} for k in keys}
    for o, h, t in B.cells():
        a = P.actual(t)
        for name, fn in (("prereg", lambda: B.project(o, h)), ("frozen_fx", lambda: frozen_fx_project(o, h)),
                         ("foresight", lambda: B.project(o, h, foresight=True))):
            p = fn()
            for k in keys:
                comp[k][name].append(S.logerr(p.get(k), a.get(k)))
    spec = {}
    for k in keys:
        spec[k] = {}
        for basis in ("prereg", "frozen_fx", "foresight"):
            v = [x for x in comp[k][basis] if x is not None]
            spec[k][basis] = {"n": len(v), "bias": sum(v) / len(v), "mae": sum(abs(x) for x in v) / len(v),
                              "share_over": sum(1 for x in v if x > 0) / len(v)} if v else None
    res["currency_path_test"] = spec

    # --- 4. the plant-replacement split
    def stats(cells, key, basis):
        v = []
        for o, h, t in cells:
            p = B.project(o, h) if basis == "prereg" else B.freeze(o, h)
            v.append(S.logerr(p.get(key), P.actual(t).get(key)))
        v = [x for x in v if x is not None]
        return {"n": len(v), "bias": sum(v) / len(v), "mae": sum(abs(x) for x in v) / len(v)} if v else None
    commissioning = {"FY2020", "FY2021", "FY2022"}
    ex = [c for c in B.cells() if c[2] not in commissioning and c[0] not in commissioning]
    res["plant_replacement_split"] = {
        "excluded_targets_and_origins": sorted(commissioning),
        "all_cells": {k: {"model": stats(B.cells(), k, "prereg"), "freeze": stats(B.cells(), k, "freeze")} for k in keys},
        "ex_commissioning": {k: {"model": stats(ex, k, "prereg"), "freeze": stats(ex, k, "freeze")} for k in keys},
        "cells_ex": len(ex)}

    # --- the guidance ledger: the company's own 9M FY2026 budget vs outturn (scored, never consumed)
    bud = {"revenue": 7_150_675, "cost_of_sales": 4_728_534, "gross_profit": 2_422_141,
           "operating": 1_597_385, "pbt": 977_697, "net": 1_021_912}
    act = P.INTERIM["9M_FY2026"]
    res["guidance_ledger"] = {k: {"budget": bud[k], "actual": act.get(k) if k != "gross_profit" else act["revenue"] - act["cost_of_sales"],
                                  "budget_vs_actual_log": None} for k in ("revenue", "cost_of_sales", "gross_profit", "pbt", "net")}
    for k, v in res["guidance_ledger"].items():
        if v["actual"] and v["actual"] > 0:
            v["budget_vs_actual_log"] = math.log(v["budget"] / v["actual"])
    res["guidance_note"] = ("The company's budget column in the 9M FY2025/26 interim. Scored here; consumed by "
                            "no driver.")
    json.dump(res, open(os.path.join(HERE, "diagnostics.json"), "w"), indent=1, default=str)
    return res


def pct(x):
    return "%+.1f%%" % ((math.exp(x) - 1) * 100) if x is not None else "n/a"


if __name__ == "__main__":
    r = main()
    print("NET-PROFIT ERROR DECOMPOSITION (mean signed contribution, %% of target revenue, %d cells)" % len(r["net_decomposition_cells"]))
    for k, v in r["net_decomposition_mean"].items():
        print("  %-18s %+7.1f%%   |mean abs| %6.1f%%" % (k, 100 * v, 100 * r["net_decomposition_mean_abs"][k]))
    print("\nSCALED PROFIT ERROR ((proj-actual)/revenue), all cells with both sides:")
    for b, v in r["scaled_profit_error"].items():
        print("  %-10s " % b + "  ".join("%s n=%d bias %+.1f%% mae %.1f%%" % (k, x["n"], 100 * x["bias"], 100 * x["mae"]) for k, x in v.items()))
    print("  skill vs freeze on the scaled error:", {k: {b: round(s, 3) for b, s in v.items()} for k, v in r["scaled_skill_vs_freeze"].items()})
    print("\nCURRENCY-PATH TEST (log record):")
    for k, v in r["currency_path_test"].items():
        print("  %-14s " % k + "  ".join("%s n=%d bias %s mae %s" % (b, x["n"], pct(x["bias"]), pct(x["mae"])) for b, x in v.items() if x))
    print("\nPLANT-REPLACEMENT SPLIT (log record, model vs freeze):")
    for k in ("revenue", "gross_profit", "pbt", "net"):
        a = r["plant_replacement_split"]["all_cells"][k]; e = r["plant_replacement_split"]["ex_commissioning"][k]
        print("  %-14s all: model n=%d mae %s / freeze mae %s   ex-commissioning: model n=%d mae %s / freeze mae %s"
              % (k, a["model"]["n"], pct(a["model"]["mae"]), pct(a["freeze"]["mae"]), e["model"]["n"], pct(e["model"]["mae"]), pct(e["freeze"]["mae"])))
    print("\nGUIDANCE LEDGER (9M FY2026 budget vs outturn):")
    for k, v in r["guidance_ledger"].items():
        print("  %-14s budget %10s actual %10s  %s" % (k, v["budget"], "%.0f" % v["actual"] if v["actual"] is not None else "n/a", pct(v["budget_vs_actual_log"])))
    print("\nUNIT WINDOW (revenue: volume vs realisation):", [(u["origin"], u["h"], pct(u["volume_effect"]), pct(u["realisation_effect"])) for u in r["revenue_unit_window"]])
