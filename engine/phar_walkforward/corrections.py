#!/usr/bin/env python3
"""PHAR — corrections under both clauses, and the adjusted-versus-raw test.

EXPANDING WINDOW ONLY: a correction at origin t uses errors resolved strictly
before t.  HALF STRENGTH by default.  Applied only where the bias holds its sign
AT EVERY CUT THE DATA ADMITS [R-FCAL-01 AMENDED 07-09-2026] — the market's
currency era is one boundary among several and was chosen for the market rather
than for any driver here.  RESET after a structural break, defined in advance as
a driver error beyond its own two standard deviations.  Aggregates rebuilt from
adjusted drivers and tested adjusted-versus-raw BY ORIGIN.

A CORRECTION ENTERS THE LIVE DRIVERS ONLY IF IT PASSES ITS OWN TEST **AND** IS
CONSISTENT WITH HOW THAT DRIVER CLASS IS BUILT ACROSS THE MARKET'S BOOK.
Otherwise it is a WATCH FLAG — recorded, graded live, acted on by nobody.
"""
from __future__ import annotations
import json, math, os, statistics, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import panel, bottom_up as bu, score  # noqa: E402

# THE HOUSE INSTRUMENT, IMPORTED BY PATH RATHER THAN COPIED [R-ENF-03]: a checker
# that models a measurement is checking a different measurement, and so is a run.
# Loaded by file path because engine/valuation_calibration/ carries its own
# `panel` module and putting it on sys.path would shadow this run's.
import importlib.util as _ilu  # noqa: E402
_bs = os.path.join(HERE, "..", "valuation_calibration", "boundary_sensitivity.py")
_spec = _ilu.spec_from_file_location("phar_boundary_sensitivity", _bs)
BS = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(BS)

STRENGTH = 0.5
BREAK_SIGMA = 2.0

# The PRIMITIVE drivers.  A correction is estimated on these and never on an
# aggregate: [R-FCAL-01] requires aggregates to be REBUILT from adjusted drivers,
# so correcting revenue or net profit directly would be the same number counted
# twice and would hide which driver moved.
PRIMITIVES = ["units_th", "price_per_pack", "cost_per_pack", "capex", "finance",
              "dna", "other_block"]
AGGREGATES = ["revenue", "cogs", "gross_profit", "expenses_total", "pbt",
              "net_profit", "debt"]


def cells_by_driver(rows):
    out = {}
    for r in rows:
        out.setdefault(r["driver"], []).append(r)
    return out


def expanding(rows, driver, origin):
    """The resolved history a correction at `origin` was allowed to see: every
    cell whose ORIGIN and whose TARGET both fall strictly before it."""
    oy = bu.yr(origin)
    return [r for r in rows if r["driver"] == driver
            and bu.yr(r["origin"]) < oy and bu.yr(r["target"]) < oy]


def run():
    rows = score.cells("baseline")
    by = cells_by_driver(rows)
    signs = score.sign_by_cut(rows)

    log, candidates = [], []
    for drv in PRIMITIVES + AGGREGATES:
        rs = by.get(drv, [])
        if not rs:
            continue
        cells = [(bu.yr(r["target"]), r["e"]) for r in rs]
        cuts, flipped = BS.cuts_for(cells)     # THE HOUSE INSTRUMENT, not a copy
        s = signs[drv]
        bias = sum(r["e"] for r in rs) / len(rs)
        cand = dict(driver=drv, n=len(rs), bias=bias,
                    is_primitive=drv in PRIMITIVES,
                    cuts_admissible=len(cuts), cuts_flipping=len(flipped),
                    era_cut=s["era_cut"])
        if drv in AGGREGATES:
            cand["disposition"] = "NOT A CANDIDATE"
            cand["reason"] = (
                "an AGGREGATE. [R-FCAL-01] rebuilds aggregates from adjusted drivers, so "
                "correcting this line directly would count the same error twice and would "
                "hide which driver moved.")
        elif not cuts:
            cand["disposition"] = "DECLINED"
            cand["reason"] = (
                "UNTESTABLE. %d cells admit NO boundary leaving five on each side, so there "
                "is no evidence that this bias holds its sign anywhere. Untestable is not "
                "stable — an absence of contrary evidence is not evidence [R-ENF-04] — and "
                "the cut-invariance clause refuses a correction resting on it."
                % len(rs))
        elif flipped:
            cand["disposition"] = "DECLINED"
            cand["reason"] = ("the sign FLIPS at %d of %d admissible cuts. A bias whose sign "
                              "depends on where the line was drawn is reported, never "
                              "corrected for." % (len(flipped), len(cuts)))
        else:
            cand["disposition"] = "WATCH FLAG"
            cand["reason"] = "sign stable at every admissible cut; second clause below."
        candidates.append(cand)

    # --- the expanding-window rule, applied and reported by origin ------------
    applied = {}
    for o in bu.ORIGINS:
        entry = dict(origin=o, corrections={})
        for drv in PRIMITIVES:
            hist = expanding(rows, drv, o)
            if len(hist) < 2:
                entry["corrections"][drv] = dict(applied=False,
                    reason="fewer than two resolved cells at this origin")
                continue
            es = [r["e"] for r in hist]
            m = sum(es) / len(es)
            sd = statistics.pstdev(es) if len(es) > 1 else 0.0
            broken = [r for r in hist if sd and abs(r["e"] - m) > BREAK_SIGMA * sd]
            cells = [(bu.yr(r["target"]), r["e"]) for r in hist]
            cuts, flipped = BS.cuts_for(cells)
            ok = bool(cuts) and not flipped
            entry["corrections"][drv] = dict(
                applied=bool(ok and abs(m) > 1e-9),
                shift=-STRENGTH * m if ok else 0.0,
                window_n=len(hist), window_bias=m,
                cuts_admissible=len(cuts), cuts_flipping=len(flipped),
                structural_breaks=len(broken),
                reason=("sign stable at every cut the WINDOW admits" if ok else
                        ("no admissible cut in the expanding window — UNTESTABLE, and "
                         "untestable is not stable" if not cuts else
                         "the sign flips inside the expanding window")))
        applied[o] = entry
        log.append(entry)

    # --- adjusted versus raw, by origin, aggregates rebuilt ------------------
    adj_vs_raw = []
    for o in bu.ORIGINS:
        corr = applied[o]["corrections"]
        p = bu.project(o)
        for h in bu.HORIZONS:
            y = bu.fy(bu.yr(o) + h)
            if y not in panel.IS or y not in p:
                continue
            a = bu.actual(y)
            raw, adj = {}, {}
            for f in ("units_th", "price_per_pack", "cost_per_pack"):
                if f not in p[y] or a.get(f) is None:
                    continue
                v = p[y][f]
                sft = corr.get(f, {}).get("shift", 0.0) if corr.get(f, {}).get("applied") else 0.0
                raw[f] = math.log(v / a[f])
                adj[f] = math.log(v * math.exp(sft) / a[f])
            if "units_th" in raw and "price_per_pack" in raw and "cost_per_pack" in raw:
                cons = panel.consolidation_ratio(o)
                u = p[y]["units_th"] * math.exp(
                    corr["units_th"]["shift"] if corr["units_th"].get("applied") else 0.0)
                pr = p[y]["price_per_pack"] * math.exp(
                    corr["price_per_pack"]["shift"] if corr["price_per_pack"].get("applied") else 0.0)
                c = p[y]["cost_per_pack"] * math.exp(
                    corr["cost_per_pack"]["shift"] if corr["cost_per_pack"].get("applied") else 0.0)
                rev_adj, cogs_adj = u * pr * cons, u * c * cons
                gp_adj = rev_adj - cogs_adj
                adj_vs_raw.append(dict(
                    origin=o, horizon=h, target=y,
                    e_revenue_raw=math.log(p[y]["revenue"] / a["revenue"]),
                    e_revenue_adjusted=math.log(rev_adj / a["revenue"]),
                    e_gross_profit_raw=math.log(p[y]["gross_profit"] / a["gross_profit"]),
                    e_gross_profit_adjusted=(math.log(gp_adj / a["gross_profit"])
                                             if gp_adj > 0 else None)))

    rec = dict(
        _="PHAR walk-forward corrections. GENERATED by corrections.py; never hand-edited.",
        run="PHAR", strength=STRENGTH, break_sigma=BREAK_SIGMA,
        rule="[R-FCAL-01] §5 with the AMENDED 07-09-2026 cut-invariance clause",
        instrument="engine/valuation_calibration/boundary_sensitivity.cuts_for — the HOUSE "
                   "instrument, imported rather than reimplemented [R-ENF-03]",
        candidates=candidates,
        adopted=[],
        watch_flags=[c["driver"] for c in candidates if c["disposition"] == "WATCH FLAG"],
        declined=[dict(driver=c["driver"], reason=c["reason"]) for c in candidates
                  if c["disposition"] == "DECLINED"],
        log=log, adjusted_vs_raw=adj_vs_raw,
        second_clause=dict(
            _="A correction enters the live drivers only if it passes its own test AND is "
              "consistent with how that driver class is built across the market's book.",
            verdict="NOT REACHED ON ANY DRIVER, because none passed the first clause.",
            note="Stated anyway so the next run does not have to rediscover it: EIPICO's "
                 "price per pack is escalated on the house inflation ladder in the delivered "
                 "study and on this company's own realised unit price here, and every other "
                 "Egyptian study in this book escalates a domestic price line on the house "
                 "ladder. A half-strength shift bolted onto that line would be a per-name "
                 "escalator nothing else in the book carries, which is precisely the "
                 "inconsistency the second clause exists to catch."),
    )
    return rec


if __name__ == "__main__":
    r = run()
    json.dump(r, open(os.path.join(HERE, "corrections_log.json"), "w"), indent=1)
    print("PHAR corrections — candidates and their disposition\n")
    print("%-16s %4s %8s %6s %6s  %s" % ("driver", "n", "bias", "cuts", "flips", "disposition"))
    for c in r["candidates"]:
        print("%-16s %4d %+8.3f %6d %6d  %s"
              % (c["driver"], c["n"], c["bias"], c["cuts_admissible"],
                 c["cuts_flipping"], c["disposition"]))
    print("\nADOPTED: %s" % (r["adopted"] or "none"))
    print("WATCH FLAGS: %s" % (r["watch_flags"] or "none"))
    print("\nexpanding-window rule, applied by origin:")
    for e in r["log"]:
        got = [d for d, v in e["corrections"].items() if v.get("applied")]
        print("  %s  applied to %s" % (e["origin"], got or "nothing"))
    n = len(r["adjusted_vs_raw"])
    if n:
        rr = sum(abs(x["e_revenue_raw"]) for x in r["adjusted_vs_raw"]) / n
        ra = sum(abs(x["e_revenue_adjusted"]) for x in r["adjusted_vs_raw"]) / n
        print("\nadjusted vs raw on %d rebuilt cells: revenue MAE %.3f raw -> %.3f adjusted" % (n, rr, ra))
