"""Score the PHDC walk-forward record, exactly as pre-registered.

Log error e = ln(projected / actual) per driver per horizon; cells where either
side is <= 0 are counted separately and scored as (P-A)/|A|, never pooled into
the log statistics. Uncertainty from a moving-block bootstrap over ORIGINS at
block lengths {2,3,4} — a bias is called robust only if its sign holds at all
three. Skill is reported against freeze and trend. The macro share of each miss
is the gap between the as-known and perfect-foresight runs.
"""
import json, os, math, random, statistics as st
import bottom_up as B

HERE = os.path.dirname(os.path.abspath(__file__))
ORIGINS = list(range(2015, 2025))
LAST_ACTUAL = 2025
ERAS = {"E1 pre-float": range(2011, 2017),
        "E2 post-float": range(2017, 2022),
        "E3 devaluation": range(2022, 2026)}


def era_of(y):
    for name, rng in ERAS.items():
        if y in rng:
            return name
    return "?"


def cells(panel, model="bottom_up", macro="as_known"):
    """One row per (origin, horizon, field) that actually resolves."""
    rows = []
    for o in ORIGINS:
        if model == "bottom_up":
            proj = B.project(panel, o, macro=macro)
        elif model == "freeze":
            proj = B.freeze(panel, o)
        else:
            proj = B.trend(panel, o)
        for h in B.HORIZONS:
            t = o + h
            if t > LAST_ACTUAL:
                continue
            for f in B.BENCH_FIELDS:
                p = proj.get(h, {}).get(f)
                a = B.actual(panel, t, f)
                if p is None or a is None:
                    continue
                row = {"origin": o, "h": h, "target": t, "field": f,
                       "proj": p, "actual": a, "era": era_of(t)}
                if p > 0 and a > 0:
                    row["e"] = math.log(p / a)
                    row["dropped"] = None
                else:
                    row["sign_case"] = True
                    row["rel"] = (p - a) / abs(a) if a else None
                    row["e"] = None
                    row["dropped"] = ("not_projected" if (p is None or a is None)
                                      else "non_positive")
                # `dropped` IS PRESENT ON EVERY ROW, INCLUDING THE SCOREABLE ONES.
                # A file whose rows carry the key can EXPRESS a drop, so a file with
                # none means none occurred; a file where the key appears only when a
                # drop happens cannot be told apart from one that discards them. The
                # pooled census reported this run UNMEASURABLE for exactly that
                # reason, on a ground true of the file and false of the writer — this
                # run drops NOTHING, 403 of 403 cells scoreable, and could not say so.
                # THE SCHEMA IS THE DECLARATION [R-ENF-06 species].
                rows.append(row)
    return rows


def block_bootstrap(vals_by_origin, blocks=(2, 3, 4), n=2000, seed=42):
    """Moving-block bootstrap over origins. Returns per-block-length CIs."""
    rng = random.Random(seed)
    origins = sorted(vals_by_origin)
    out = {}
    for L in blocks:
        if len(origins) < L:
            continue
        means = []
        for _ in range(n):
            picked = []
            while len(picked) < len(origins):
                s = rng.randrange(0, len(origins) - L + 1)
                picked.extend(origins[s:s + L])
            picked = picked[:len(origins)]
            pool = [v for o in picked for v in vals_by_origin[o]]
            if pool:
                means.append(sum(pool) / len(pool))
        if means:
            means.sort()
            out[L] = {"lo": round(means[int(0.025 * len(means))], 4),
                      "hi": round(means[int(0.975 * len(means))], 4)}
    return out


def summarise(rows, field=None, h=None):
    sel = [r for r in rows if r.get("e") is not None
           and (field is None or r["field"] == field)
           and (h is None or r["h"] == h)]
    if not sel:
        return None
    es = [r["e"] for r in sel]
    by_o = {}
    for r in sel:
        by_o.setdefault(r["origin"], []).append(r["e"])
    boot = block_bootstrap(by_o)
    robust = bool(boot) and all(
        (v["lo"] > 0 and v["hi"] > 0) or (v["lo"] < 0 and v["hi"] < 0)
        for v in boot.values())
    # n IS THE CELLS THE SCORE TOOK; n_cells IS THE CELLS THAT EXIST. A record
    # carrying only the first cannot show a reader that a driver was scored on
    # half its history — one driver in this book publishes a bias computed on NONE
    # of its fifty cells — and the coverage was recoverable only by running a
    # census by hand. The pair carries no threshold and makes no judgement; it
    # makes the fraction visible in the record that quotes the bias.
    exists = sum(1 for r in rows
                 if (field is None or r["field"] == field)
                 and (h is None or r["h"] == h))
    return {"n": len(es), "n_cells": exists,
            "bias": round(sum(es) / len(es), 4),
            "mae": round(sum(abs(e) for e in es) / len(es), 4),
            "median": round(st.median(es), 4),
            "over": round(sum(1 for e in es if e > 0) / len(es), 3),
            "boot": boot, "robust_sign": robust}


def skill(rows_model, rows_bench, field=None, h=None):
    """Reduction in mean absolute log error against a benchmark, on the cells
    BOTH resolve — a model scored on a different sample from its benchmark is
    not being compared to it."""
    key = lambda r: (r["origin"], r["h"], r["field"])
    m = {key(r): r for r in rows_model if r.get("e") is not None}
    b = {key(r): r for r in rows_bench if r.get("e") is not None}
    shared = [k for k in m if k in b
              and (field is None or k[2] == field)
              and (h is None or k[1] == h)]
    if not shared:
        return None
    mm = sum(abs(m[k]["e"]) for k in shared) / len(shared)
    bb = sum(abs(b[k]["e"]) for k in shared) / len(shared)
    return {"n": len(shared), "model_mae": round(mm, 4), "bench_mae": round(bb, 4),
            "skill": round(1 - mm / bb, 4) if bb else None}


def main():
    panel = B.load()
    res = {}
    rows_bu = cells(panel, "bottom_up", "as_known")
    rows_pf = cells(panel, "bottom_up", "perfect_foresight")
    rows_fz = cells(panel, "freeze")
    rows_tr = cells(panel, "trend")
    json.dump({"as_known": rows_bu, "perfect_foresight": rows_pf,
               "freeze": rows_fz, "trend": rows_tr},
              open(os.path.join(HERE, "error_cells.json"), "w"), indent=1)

    fields = sorted({r["field"] for r in rows_bu})
    print("=" * 78)
    print("PER-DRIVER RECORD, all horizons pooled (as-known macro)")
    print("%-20s %4s %8s %8s %7s %-22s" % ("driver", "n", "bias", "MAE", "over", "block CIs {2,3,4}"))
    for f in fields:
        s = summarise(rows_bu, f)
        if not s:
            continue
        ci = " ".join("%.2f/%.2f" % (v["lo"], v["hi"]) for v in s["boot"].values())
        print("%-20s %4d %8.3f %8.3f %7.2f %-22s %s" %
              (f, s["n"], s["bias"], s["mae"], s["over"], ci,
               "ROBUST" if s["robust_sign"] else ""))
        res.setdefault("by_driver", {})[f] = s

    print()
    print("=" * 78)
    print("BY HORIZON — revenue and net profit (as-known macro)")
    print("%-16s %2s %4s %8s %8s   %-14s %-14s" %
          ("driver", "h", "n", "bias", "MAE", "skill vs freeze", "skill vs trend"))
    for f in ("is.revenue", "is.npat_mi", "new_sales", "units_sold"):
        for h in B.HORIZONS:
            s = summarise(rows_bu, f, h)
            if not s:
                continue
            sf = skill(rows_bu, rows_fz, f, h)
            stn = skill(rows_bu, rows_tr, f, h)
            print("%-16s %2d %4d %8.3f %8.3f   %-14s %-14s" %
                  (f, h, s["n"], s["bias"], s["mae"],
                   "-" if not sf else "%+.3f" % sf["skill"],
                   "-" if not stn else "%+.3f" % stn["skill"]))
            res.setdefault("by_horizon", {}).setdefault(f, {})[h] = {
                "summary": s, "skill_freeze": sf, "skill_trend": stn}

    print()
    print("=" * 78)
    print("MACRO vs COMPANY split — perfect foresight isolates the company error")
    print("%-20s %9s %9s %9s" % ("driver", "as-known", "perfect", "macro share"))
    for f in fields:
        a = summarise(rows_bu, f)
        b = summarise(rows_pf, f)
        if not a or not b:
            continue
        share = None
        if a["mae"] > 0:
            share = round((a["mae"] - b["mae"]) / a["mae"], 3)
        print("%-20s %9.3f %9.3f %9s" % (f, a["mae"], b["mae"],
                                         "-" if share is None else "%+.1f%%" % (100 * share)))
        res.setdefault("macro_split", {})[f] = {"as_known_mae": a["mae"],
                                                "perfect_mae": b["mae"],
                                                "macro_share": share}

    print()
    print("=" * 78)
    print("BY ERA — revenue bias (sign stability is what gates a correction)")
    print("%-16s %-16s %4s %8s %8s" % ("driver", "era", "n", "bias", "MAE"))
    for f in ("is.revenue", "new_sales", "units_sold", "asp", "is.npat_mi"):
        for era in ERAS:
            sel = [r for r in rows_bu
                   if r["field"] == f and r["era"] == era
                   and r.get("e") is not None]
            if not sel:
                continue
            es = [r["e"] for r in sel]
            print("%-16s %-16s %4d %8.3f %8.3f" %
                  (f, era, len(es), sum(es) / len(es),
                   sum(abs(e) for e in es) / len(es)))
            res.setdefault("by_era", {}).setdefault(f, {})[era] = {
                "n": len(es), "bias": round(sum(es) / len(es), 4),
                "mae": round(sum(abs(e) for e in es) / len(es), 4)}

    sign_cases = [r for r in rows_bu if r.get("sign_case")]
    res["sign_cases"] = len(sign_cases)
    print("\nsign cases (log undefined, scored and reported separately): %d"
          % len(sign_cases))
    json.dump(res, open(os.path.join(HERE, "scores.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
