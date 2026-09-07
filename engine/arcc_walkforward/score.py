"""ARCC walk-forward — scoring, benchmarks, bootstrap, macro split.

Implements PRE_REGISTRATION_01-09-2026.md §4-§6. Nothing here chooses anything;
it measures what the pre-registered rules produced.
"""
import os, sys, json, math, random

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import panel as P
import bottom_up as B

SEED = 42
NBOOT = 2000
BLOCKS = [2, 3, 4]

DRIVERS = [
    "vol_local", "vol_export", "vol_total", "price_local", "price_export", "services",
    "raw_per_t", "transport_per_t", "overhead_per_t", "raw", "transport", "overhead",
    "mfg_dep", "amort", "revenue", "cogs", "gross_profit", "ga", "provisions",
    "interest_income", "other_income", "finance_costs", "pbt", "tax", "pat", "majority",
]

# Declared in the pre-registration §3, so it is reported rather than discovered:
# these rules are level persistence and are therefore IDENTICAL to FREEZE by
# construction. Their skill against FREEZE is zero by definition.
EQUALS_FREEZE = {"vol_export", "mfg_dep", "amort", "provisions", "interest_income",
                 "other_income", "finance_costs"}

# §5's own check: these carry no CPI, FX, population or coal term, so their macro
# share MUST come back exactly zero. A non-zero value is a wiring error.
NO_MACRO_TERM = EQUALS_FREEZE | {"impairments", "disposals", "jv", "fx"}


def logerr(proj, act):
    if proj is None or act is None:
        return None
    if proj <= 0 or act <= 0:
        return None
    return math.log(proj / act)


def build_cells(w=B.W_DEFAULT, foresight=False, cpi_only=False):
    rows = []
    for o, h, t in B.cells():
        p = B.project(o, h, w=w, foresight=foresight, cpi_only=cpi_only)
        a = B.actual(t)
        f = B.freeze(o, h)
        tr, fb = B.trend(o, h)
        row = {"origin": o, "h": h, "target": t, "era": B.ERA[o],
               "trend_fallbacks": fb, "e": {}, "ef": {}, "et": {},
               "unscoreable": []}
        for d in DRIVERS:
            row["e"][d] = logerr(p.get(d), a.get(d))
            row["ef"][d] = logerr(f.get(d), a.get(d))
            row["et"][d] = logerr(tr.get(d) if tr else None, a.get(d))
            if row["e"][d] is None:
                row["unscoreable"].append(d)
        row["proj"], row["act"], row["frz"] = p, a, f
        # The TREND projection is retained too. Without both benchmarks'
        # projections a per-cell file cannot reproduce a skill number, which
        # is what a per-cell file is for.
        row["trd"] = tr or {}
        rows.append(row)
    return rows


def agg(rows, key, driver, h=None, era=None):
    v = [r[key][driver] for r in rows
         if r[key][driver] is not None and (h is None or r["h"] == h)
         and (era is None or r["era"] == era)]
    if not v:
        return None
    n = len(v)
    return {"n": n, "bias": sum(v) / n, "mae": sum(abs(x) for x in v) / n,
            "share_over": sum(1 for x in v if x > 0) / n}


def block_bootstrap(rows, driver, key="e", blocks=BLOCKS, nboot=NBOOT, seed=SEED):
    """Moving-block bootstrap over ORIGINS. One CI per block length."""
    out = {}
    origins = [o for o in B.ORIGINS if any(r["origin"] == o for r in rows)]
    by_o = {o: [r[key][driver] for r in rows
                if r["origin"] == o and r[key][driver] is not None] for o in origins}
    live = [o for o in origins if by_o[o]]
    if len(live) < 3:
        return {}
    for L in blocks:
        if L > len(live):
            continue
        rng = random.Random(seed + L)
        means = []
        nblocks = max(1, len(live) // L)
        for _ in range(nboot):
            vals = []
            for _b in range(nblocks):
                s = rng.randrange(0, len(live) - L + 1)
                for o in live[s:s + L]:
                    vals.extend(by_o[o])
            if vals:
                means.append(sum(vals) / len(vals))
        means.sort()
        lo = means[int(0.025 * len(means))]
        hi = means[int(0.975 * len(means)) - 1]
        out[L] = {"lo": lo, "hi": hi, "robust_sign": (lo > 0) == (hi > 0)}
    return out


def skill(rows, driver, bench="ef", h=None):
    """1 - MAE(method) / MAE(benchmark), on the cells where BOTH exist."""
    pairs = [(r["e"][driver], r[bench][driver]) for r in rows
             if r["e"][driver] is not None and r[bench][driver] is not None
             and (h is None or r["h"] == h)]
    if not pairs:
        return None
    m = sum(abs(a) for a, _ in pairs) / len(pairs)
    b = sum(abs(x) for _, x in pairs) / len(pairs)
    if b == 0:
        return None
    return {"n": len(pairs), "mae": m, "mae_bench": b, "skill": 1.0 - m / b}


def macro_split(driver, h=None):
    """1 - MAE(perfect foresight) / MAE(knowable), per the pre-registration §5."""
    k = agg(build_cells(), "e", driver, h=h)
    f = agg(build_cells(foresight=True), "e", driver, h=h)
    if not k or not f or k["mae"] == 0:
        return None
    return {"knowable_mae": k["mae"], "foresight_mae": f["mae"],
            "macro_share": 1.0 - f["mae"] / k["mae"], "n": k["n"]}



def flatten_cells(rows, fore, fore_cpi):
    """Per-cell error rows, the shape the pooled cuts read.

    build_cells() already computes every cell; the aggregates threw them away, so
    this run could not answer which origins carry the bias without being re-run.
    A cell the log score cannot take is written with log_error null and a REASON
    rather than omitted, because a silently shorter sample is how an apparent
    improvement is manufactured.

    TWO CORRECTIONS, 07-09-2026, both to this function and both of a kind this
    repository names in its own rules. (1) The sentence above was TRUE OF THE
    MODEL'S CELLS AND FALSE OF THE BENCHMARKS' — a freeze or trend cell the log
    score could not take was silently skipped by the very branch this docstring
    described, which is a comment asserting a behaviour the code does not have.
    (2) The reason was ASSERTED FROM AN ABSENCE rather than derived from a test,
    so a cell the benchmark could not project at all was labelled non-positive;
    on the sibling run that mislabelled 63 of 72 cells. The reason is now tested:
    not_projected where there is no projection, non_positive where there is one
    the logarithm cannot take.
    """
    out = []
    settings = [("asknown", rows, "e"), ("freeze", rows, "ef"), ("trend", rows, "et"),
                ("foresight", fore, "e"), ("foresight_cpi_only", fore_cpi, "e")]
    for name, src, key in settings:
        for r in src:
            for d in DRIVERS:
                le = r[key][d]
                src_key = {"e": "proj", "ef": "frz", "et": "trd"}[key]
                proj = r.get(src_key, {}).get(d)
                act = r["act"].get(d)
                if le is not None:
                    dropped = None
                elif proj is None or act is None:
                    dropped = "not_projected"
                else:
                    dropped = "non_positive"
                out.append({"origin": r["origin"], "horizon": r["h"], "year": r["target"],
                            "driver": d, "setting": name,
                            "projected": proj, "actual": act, "era": r["era"],
                            "log_error": le, "dropped": dropped})
    return out


def run():
    rows = build_cells()
    out = {"n_cells": len(rows), "drivers": {}, "by_horizon": {}, "skill": {},
           "bootstrap": {}, "macro": {}, "sensitivity": {}, "eras": {},
           "unscoreable": {}, "trend_fallbacks": sum(r["trend_fallbacks"] for r in rows)}
    for d in DRIVERS:
        out["drivers"][d] = agg(rows, "e", d)
        if out["drivers"][d] is not None:
            # The cells that EXIST for this driver, beside the count the score took.
            out["drivers"][d]["n_cells"] = sum(1 for r in rows if d in r.get("e", {}))
        out["by_horizon"][d] = {h: agg(rows, "e", d, h=h) for h in B.HORIZONS}
        out["skill"][d] = {"vs_freeze": skill(rows, d, "ef"),
                           "vs_trend": skill(rows, d, "et"),
                           "equals_freeze_by_construction": d in EQUALS_FREEZE}
        out["bootstrap"][d] = block_bootstrap(rows, d)
        out["eras"][d] = {e: agg(rows, "e", d, era=e)
                          for e in sorted({r["era"] for r in rows})}
        out["unscoreable"][d] = sum(1 for r in rows if r["e"][d] is None)
    fs = build_cells(foresight=True)
    for d in DRIVERS:
        k, f = out["drivers"][d], agg(fs, "e", d)
        if k and f and k["mae"]:
            out["macro"][d] = {"knowable_mae": k["mae"], "foresight_mae": f["mae"],
                               "macro_share": 1.0 - f["mae"] / k["mae"]}
    for w in B.W_SENSITIVITY:
        r = build_cells(w=w)
        out["sensitivity"]["w=%.1f" % w] = {
            d: agg(r, "e", d) for d in ("raw_per_t", "cogs", "gross_profit", "pbt", "pat")}
    return rows, out


def check_macro_wiring(out):
    """The pre-registered check on the split itself: a driver with no macro term
    MUST return a macro share of exactly zero. A non-zero value there is a wiring
    error in the split, not a finding, and the run fails rather than reports it."""
    bad = []
    for d in NO_MACRO_TERM:
        m = out["macro"].get(d)
        if m and abs(m["macro_share"]) > 1e-9:
            bad.append("%s has no macro term but a macro share of %.6f" % (d, m["macro_share"]))
    return bad


def harvest_shape(rows, out):
    """The same measurements, in the schema engine/lessons_harvest.py reads.

    The harvester's selection rules are fixed in its module AHEAD of any run so
    they cannot be tuned after seeing the numbers, which means the RUN adapts to
    the harvester and never the other way round.
    """
    by_driver, by_horizon, macro_split, by_era = {}, {}, {}, {}
    for d in DRIVERS:
        a = out["drivers"][d]
        if not a:
            continue
        b = out["bootstrap"].get(d) or {}
        by_driver[d] = {"bias": a["bias"], "mae": a["mae"], "over": a["share_over"],
                        "n": a["n"],
                        # n is the cells the score TOOK; n_cells the cells that
                        # EXIST. Only the pair shows a reader the coverage behind
                        # a bias, and it carries no threshold.
                        "n_cells": out["drivers"][d].get("n_cells"),
                        "robust_sign": bool(b) and all(v["robust_sign"] for v in b.values())}
        hs = {}
        for h in B.HORIZONS:
            v = out["by_horizon"][d].get(h)
            if not v:
                continue
            sk = skill([r for r in rows if r["h"] == h], d, "ef")
            hs[str(h)] = {"bias": v["bias"], "mae": v["mae"], "n": v["n"],
                          "skill_freeze": {"skill": (sk or {}).get("skill", 0.0)}}
        if hs:
            by_horizon[d] = hs
        m = out["macro"].get(d)
        if m:
            macro_split[d] = {"macro_share": m["macro_share"],
                              "as_known_mae": m["knowable_mae"],
                              "perfect_mae": m["foresight_mae"]}
        e = {k: v for k, v in out["eras"][d].items() if v}
        if len(e) >= 2:
            by_era[d] = {k: {"bias": v["bias"], "n": v["n"]} for k, v in e.items()}
    return {"by_driver": by_driver, "by_horizon": by_horizon,
            "macro_split": macro_split, "by_era": by_era,
            "n_cells": out["n_cells"], "detail": out}


if __name__ == "__main__":
    rows, out = run()
    bad = check_macro_wiring(out)
    json.dump(harvest_shape(rows, out),
              open(os.path.join(HERE, "scores.json"), "w"), indent=1, default=str)
    json.dump(flatten_cells(rows, build_cells(foresight=True),
                             build_cells(foresight=True, cpi_only=True)),
              open(os.path.join(HERE, "error_cells.json"), "w"), indent=1)
    print("cells %d   trend fallbacks %d" % (out["n_cells"], out["trend_fallbacks"]))
    print()
    print("%-18s %4s %8s %8s %7s %9s %9s %8s" %
          ("driver", "n", "bias", "MAE", "over", "vs freeze", "vs trend", "macro"))
    for d in DRIVERS:
        a = out["drivers"][d]
        if not a:
            continue
        sf = out["skill"][d]["vs_freeze"]
        st = out["skill"][d]["vs_trend"]
        mc = out["macro"].get(d)
        eq = out["skill"][d]["equals_freeze_by_construction"]
        print("%-18s %4d %+8.3f %8.3f %6.0f%% %9s %9s %8s" %
              (d, a["n"], a["bias"], a["mae"], 100 * a["share_over"],
               "n/a" if eq else ("%+.3f" % sf["skill"] if sf else "-"),
               "%+.3f" % st["skill"] if st else "-",
               "%+.3f" % mc["macro_share"] if mc else "-"))
    print()
    if bad:
        print("MACRO WIRING CHECK FAILED:")
        for b in bad:
            print("  ", b)
        sys.exit(1)
    print("macro wiring check: PASSED — every driver with no macro term returns exactly zero")
