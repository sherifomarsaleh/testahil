"""AMOC walk-forward — scoring and diagnosis.

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
BLOCKS = [2, 3]

DRIVERS = ["volume_t", "net_sales", "raw_materials", "salaries", "supporting_materials",
           "depreciation", "other_cos", "cost_of_sales", "gross_profit", "ga", "marketing",
           "other_expenses", "operating_profit", "claims_provision", "other_revenues",
           "credit_interest", "investment_revenues", "pbt", "income_tax", "npat", "majority"]

# Eras: the fiscal years containing Egypt's devaluations (B-9). FY2021 is the
# last pre-float year in this window; FY2022-FY2024 each contain a devaluation.
ERA = {"FY2021": "E1 pre-devaluation", "FY2022": "E2 devaluation",
       "FY2023": "E2 devaluation", "FY2024": "E2 devaluation", "FY2025": "E2 devaluation"}


def logerr(proj, act):
    if proj is None or act is None:
        return None
    if proj <= 0 or act <= 0:
        return None
    return math.log(proj / act)


def build_cells(beta=B.BETA_DEFAULT, foresight=False, foresight_cpi_only=False):
    rows = []
    for o, h, t in B.cells():
        p = B.project(o, h, beta=beta, foresight=foresight, foresight_cpi_only=foresight_cpi_only)
        a = B.actual(t)
        f = B.freeze(o, h)
        tr = B.trend(o, h)
        row = {"origin": o, "h": h, "target": t, "era": ERA[o], "e": {}, "ef": {}, "et": {}}
        for d in DRIVERS:
            row["e"][d] = logerr(p.get(d), a.get(d))
            row["ef"][d] = logerr(f.get(d), a.get(d))
            row["et"][d] = logerr(tr.get(d) if tr else None, a.get(d))
        row["proj"], row["act"] = p, a
        rows.append(row)
    return rows


def agg(rows, key, driver, h=None, era=None):
    v = [r[key][driver] for r in rows
         if r[key][driver] is not None and (h is None or r["h"] == h)
         and (era is None or r["era"] == era)]
    if not v:
        return None
    n = len(v)
    bias = sum(v) / n
    mae = sum(abs(x) for x in v) / n
    over = sum(1 for x in v if x > 0) / n
    return {"n": n, "bias": bias, "mae": mae, "share_over": over}


def block_bootstrap(rows, driver, key="e", blocks=BLOCKS, nboot=NBOOT, seed=SEED):
    """Moving-block bootstrap over ORIGINS. Returns a CI per block length."""
    out = {}
    origins = B.ORIGINS
    by_o = {o: [r[key][driver] for r in rows if r["origin"] == o and r[key][driver] is not None]
            for o in origins}
    have = [o for o in origins if by_o[o]]
    for L in blocks:
        if len(have) < L:
            out[L] = None
            continue
        rnd = random.Random(seed + L)
        starts = list(range(0, len(have) - L + 1))
        stats = []
        for _ in range(nboot):
            vals = []
            while len(vals) < len(have):
                s = rnd.choice(starts)
                for o in have[s:s + L]:
                    vals.extend(by_o[o])
            if vals:
                stats.append(sum(vals) / len(vals))
        stats.sort()
        lo = stats[int(0.05 * len(stats))]
        hi = stats[int(0.95 * len(stats)) - 1]
        out[L] = {"lo": lo, "hi": hi, "same_sign": (lo > 0 and hi > 0) or (lo < 0 and hi < 0)}
    return out


def skill(rows, driver, key_bench="ef"):
    """1 - MAE(model)/MAE(benchmark), on the cells where BOTH exist."""
    pairs = [(r["e"][driver], r[key_bench][driver]) for r in rows
             if r["e"][driver] is not None and r[key_bench][driver] is not None]
    if not pairs:
        return None
    m = sum(abs(a) for a, _ in pairs) / len(pairs)
    b = sum(abs(b) for _, b in pairs) / len(pairs)
    if b == 0:
        return None
    return {"n": len(pairs), "mae_model": m, "mae_bench": b, "skill": 1.0 - m / b}



def flatten_cells(rows, fore, fore_cpi):
    """Per-cell error rows, the shape the pooled cuts read [R-ENF-06 species].

    build_cells() already computes every cell; the first version of this module
    aggregated them away and wrote only the summaries, so a later question about
    WHICH origins carry the bias had no answer here at all. The projections and
    actuals are already in each row; this only writes them down.
    """
    out = []
    settings = [("asknown", rows, "e"), ("freeze", rows, "ef"), ("trend", rows, "et"),
                ("foresight", fore, "e"), ("foresight_cpi_only", fore_cpi, "e")]
    for name, src, key in settings:
        for r in src:
            for d in DRIVERS:
                le = r[key][d]
                if le is None:
                    continue
                out.append({"origin": r["origin"], "horizon": r["h"], "year": r["target"],
                            "driver": d, "setting": name,
                            "projected": r["proj"].get(d) if key == "e" else None,
                            "actual": r["act"].get(d), "era": r["era"], "log_error": le})
    return out


def main():
    rows = build_cells()
    fore = build_cells(foresight=True)
    fore_cpi = build_cells(foresight_cpi_only=True)

    res = {"cells": len(rows), "seed": SEED, "nboot": NBOOT, "blocks": BLOCKS,
           "drivers": {}, "sensitivity": {}, "macro_check": {}, "by_horizon": {}}

    for d in DRIVERS:
        a = agg(rows, "e", d)
        if a is None:
            continue
        rec = {"overall": a,
               "by_h": {h: agg(rows, "e", d, h=h) for h in B.HORIZONS},
               "by_era": {e: agg(rows, "e", d, era=e) for e in sorted(set(ERA.values()))},
               "bootstrap": block_bootstrap(rows, d),
               "skill_vs_freeze": skill(rows, d, "ef"),
               "skill_vs_trend": skill(rows, d, "et"),
               "freeze_equivalent": d in B.FREEZE_EQUIVALENT or d == "net_sales"}
        # macro split
        af = agg(fore, "e", d)
        rec["mae_knowable"] = a["mae"]
        rec["mae_foresight"] = af["mae"] if af else None
        rec["macro_share"] = (1.0 - af["mae"] / a["mae"]) if (af and a["mae"] > 0) else None
        acpi = agg(fore_cpi, "e", d)
        rec["mae_foresight_cpi_only"] = acpi["mae"] if acpi else None
        # sign stability across eras
        eras = [v for v in rec["by_era"].values() if v]
        rec["sign_flips"] = (len(set(1 if e["bias"] > 0 else -1 for e in eras)) > 1) if len(eras) > 1 else False
        res["drivers"][d] = rec

    # THE SPLIT'S OWN CHECK: drivers with no CPI and no Brent term must return a
    # macro share of exactly zero. A non-zero value is a wiring error, not a finding.
    bad = []
    for d in sorted(B.NO_MACRO_TERM):
        ms = res["drivers"].get(d, {}).get("macro_share")
        if ms is not None and abs(ms) > 1e-9:
            bad.append((d, ms))
    res["macro_check"] = {"zero_by_construction": sorted(B.NO_MACRO_TERM), "violations": bad}
    assert not bad, "macro split is mis-wired: %s" % bad

    # beta sensitivity, reported never selected
    for beta in (0.8, 1.0, 1.2):
        r2 = build_cells(beta=beta)
        res["sensitivity"]["beta_%.1f" % beta] = {
            d: agg(r2, "e", d) for d in ("net_sales", "cost_of_sales", "gross_profit", "majority")}

    # ---- the shape lessons_harvest.py reads ---------------------------------
    # The harvester keys on by_driver / by_horizon / macro_split / by_era. The first
    # version of this module emitted a richer shape under different names, so the
    # harvest matched NOTHING and reported "0 candidates" — an absent answer wearing
    # the costume of a clean one, which is exactly the failure [R-ENF-04] names. The
    # contract is met here rather than worked around by writing lessons out by hand.
    res["by_driver"] = {}
    res["by_horizon"] = {}
    res["macro_split"] = {}
    res["by_era"] = {}
    for d, rec in res["drivers"].items():
        a = rec["overall"]
        bs = rec["bootstrap"]
        robust = all(bs.get(L) and bs[L]["same_sign"] for L in (2, 3))
        res["by_driver"][d] = {"n": a["n"], "bias": round(a["bias"], 4),
                               "mae": round(a["mae"], 4), "over": round(a["share_over"], 3),
                               "boot": {str(L): ({"lo": round(bs[L]["lo"], 4),
                                                  "hi": round(bs[L]["hi"], 4)} if bs.get(L) else None)
                                        for L in BLOCKS},
                               "robust_sign": bool(robust)}
        hh = {}
        for h in B.HORIZONS:
            v = rec["by_h"].get(h)
            if not v:
                continue
            pairs_f = [(r["e"][d], r["ef"][d]) for r in rows
                       if r["h"] == h and r["e"][d] is not None and r["ef"][d] is not None]
            pairs_t = [(r["e"][d], r["et"][d]) for r in rows
                       if r["h"] == h and r["e"][d] is not None and r["et"][d] is not None]

            def _sk(pairs):
                if not pairs:
                    return None
                m = sum(abs(x) for x, _ in pairs) / len(pairs)
                b = sum(abs(y) for _, y in pairs) / len(pairs)
                if b == 0:
                    return None
                return {"n": len(pairs), "model_mae": round(m, 4),
                        "bench_mae": round(b, 4), "skill": round(1 - m / b, 4)}

            ent = {"summary": {"n": v["n"], "bias": round(v["bias"], 4),
                               "mae": round(v["mae"], 4), "over": round(v["share_over"], 3),
                               "robust_sign": bool(robust)}}
            # A rule that IS the benchmark cannot be scored against it. Declared in the
            # pre-registration; recorded here so the harvester cannot read a structural
            # zero as a measured defeat.
            if not rec["freeze_equivalent"]:
                sf = _sk(pairs_f)
                if sf:
                    ent["skill_freeze"] = sf
            st = _sk(pairs_t)
            if st:
                ent["skill_trend"] = st
            hh[str(h)] = ent
        res["by_horizon"][d] = hh
        res["macro_split"][d] = {"as_known_mae": round(rec["mae_knowable"], 4),
                                 "perfect_mae": (round(rec["mae_foresight"], 4)
                                                 if rec["mae_foresight"] is not None else None),
                                 "macro_share": (round(rec["macro_share"], 3)
                                                 if rec["macro_share"] is not None else None)}
        res["by_era"][d] = {e: {"n": v["n"], "bias": round(v["bias"], 4)}
                            for e, v in rec["by_era"].items() if v}

    json.dump(res, open(os.path.join(HERE, "scores.json"), "w"), indent=1, default=str)
    json.dump(flatten_cells(rows, fore, fore_cpi),
              open(os.path.join(HERE, "error_cells.json"), "w"), indent=1)
    return res, rows


def pct(x):
    return "%+.1f%%" % ((math.exp(x) - 1) * 100) if x is not None else "   n/a"


if __name__ == "__main__":
    res, rows = main()
    print("AMOC fundamental walk-forward — %d scoreable cells, LIGHT scope\n" % res["cells"])
    hdr = "%-22s %4s %10s %10s %8s  %-22s %-22s"
    print(hdr % ("driver", "n", "bias", "MAE", "over%", "skill vs freeze", "skill vs trend"))
    print("-" * 118)
    for d in DRIVERS:
        r = res["drivers"].get(d)
        if not r:
            continue
        a = r["overall"]
        sf = r["skill_vs_freeze"]; st = r["skill_vs_trend"]
        sfs = ("n/a rule=benchmark" if r["freeze_equivalent"]
               else ("%+.3f" % sf["skill"] if sf else "n/a"))
        sts = ("%+.3f (n=%d)" % (st["skill"], st["n"])) if st else "n/a"
        print(hdr % (d, a["n"], pct(a["bias"]), pct(a["mae"]), "%.0f%%" % (100*a["share_over"]), sfs, sts))
    print("\nmacro split check — drivers that must return exactly zero: %s"
          % ", ".join(res["macro_check"]["zero_by_construction"]))
    print("violations: %s" % (res["macro_check"]["violations"] or "none"))
