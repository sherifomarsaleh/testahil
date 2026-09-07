"""EGCH (KIMA) walk-forward — scoring.

Implements PRE_REGISTRATION_01-09-2026.md §3-§5. Nothing here chooses anything; it
measures what the pre-registered rules produced. Emits scores.json in the shape
lessons_harvest.py reads (by_driver / by_horizon / macro_split / by_era).
"""
import os, sys, json, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import panel as P
import bottom_up as B

SEED = 42
NBOOT = 2000
BLOCKS = [2, 3, 4]

DRIVERS = ["revenue", "urea_t", "cost_of_sales", "gross_profit", "selling", "admin", "provisions",
           "other_bucket", "fx", "investment_income", "credit_interest", "debit_interest",
           "pbt", "tax_current", "net"]
CAN_BE_NEGATIVE = {"gross_profit", "other_bucket", "fx", "pbt", "net", "tax_current"}

ERA = {}
for o in B.ORIGINS:
    n = B.y(o)
    ERA[o] = ("E1 old plant, pre-float" if n <= 2016 else
              "E2 old plant post-float / transition" if n <= 2020 else
              "E3 KIMA-2 operating, devaluations")


def logerr(proj, act):
    if proj is None or act is None or proj <= 0 or act <= 0:
        return None
    return math.log(proj / act)


def sign_hit(proj, act):
    if proj is None or act is None:
        return None
    return (proj > 0) == (act > 0)


def build_cells(**kw):
    rows = []
    for o, h, t in B.cells():
        p = B.project(o, h, **kw)
        a = P.actual(t)
        f = B.freeze(o, h)
        tr, win = B.trend(o, h)
        row = {"origin": o, "h": h, "target": t, "era": ERA[o], "trend_window": win,
               "e": {}, "ef": {}, "et": {}, "sign": {}, "excluded": {}}
        for d in DRIVERS:
            pv, av = p.get(d), a.get(d)
            row["e"][d] = logerr(pv, av)
            row["ef"][d] = logerr(f.get(d), av)
            row["et"][d] = logerr(tr.get(d) if tr else None, av)
            row["sign"][d] = sign_hit(pv, av)
            row["excluded"][d] = (pv is not None and av is not None and (pv <= 0 or av <= 0))
        row["proj"], row["act"] = p, a
        # Both benchmarks' projections are retained, not only the errors they
        # produce: without them a per-cell file cannot reproduce a skill
        # number, which is what a per-cell file is for.
        row["frz"], row["trd"] = f, (tr or {})
        rows.append(row)
    return rows


def agg(rows, key, driver, h=None, era=None):
    v = [r[key][driver] for r in rows
         if r[key][driver] is not None and (h is None or r["h"] == h)
         and (era is None or r["era"] == era)]
    if not v:
        return None
    n = len(v)
    excl = sum(1 for r in rows if r["excluded"][driver] and (h is None or r["h"] == h)
               and (era is None or r["era"] == era))
    sg = [r["sign"][driver] for r in rows if r["sign"][driver] is not None
          and (h is None or r["h"] == h) and (era is None or r["era"] == era)]
    return {"n": n, "bias": sum(v) / n, "mae": sum(abs(x) for x in v) / n,
            "share_over": sum(1 for x in v if x > 0) / n, "excluded_nonpositive": excl,
            "sign_hit_rate": (sum(sg) / len(sg)) if sg else None, "sign_n": len(sg)}


def block_bootstrap(rows, driver, key="e", blocks=BLOCKS, nboot=NBOOT, seed=SEED):
    out = {}
    by_o = {o: [r[key][driver] for r in rows if r["origin"] == o and r[key][driver] is not None]
            for o in B.ORIGINS}
    have = [o for o in B.ORIGINS if by_o[o]]
    for L in blocks:
        if len(have) < L + 1:
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
            stats.append(sum(vals) / len(vals))
        stats.sort()
        lo = stats[int(0.05 * len(stats))]
        hi = stats[int(0.95 * len(stats)) - 1]
        out[L] = {"lo": lo, "hi": hi, "same_sign": (lo > 0 and hi > 0) or (lo < 0 and hi < 0)}
    return out


def skill_pairs(rows, driver, key_bench, h=None):
    pairs = [(r["e"][driver], r[key_bench][driver]) for r in rows
             if r["e"][driver] is not None and r[key_bench][driver] is not None
             and (h is None or r["h"] == h)]
    if not pairs:
        return None
    m = sum(abs(a) for a, _ in pairs) / len(pairs)
    b = sum(abs(b) for _, b in pairs) / len(pairs)
    if b == 0:
        return None
    return {"n": len(pairs), "model_mae": round(m, 4), "bench_mae": round(b, 4),
            "skill": round(1.0 - m / b, 4)}



def flatten_cells(rows, fore, fore_cpi):
    """Per-cell error rows, the shape the pooled cuts read.

    build_cells() already computes every cell and the aggregates threw them away,
    so a question about WHICH origins carry the bias had no answer in this run.
    A cell the log score cannot take is written with log_error null and a REASON
    rather than omitted, because a silently shorter sample is how an apparent
    improvement is manufactured.

    TWO CORRECTIONS, 07-09-2026, both to this function. (1) The sentence above was
    TRUE OF THE MODEL'S CELLS AND FALSE OF THE BENCHMARKS' — a freeze or trend cell
    the log score could not take was silently skipped by the branch this docstring
    described, a comment asserting a behaviour the code does not have. (2) The
    reason was ASSERTED rather than derived: it is now tested, not_projected where
    there is no projection and non_positive where there is one the logarithm
    cannot take. The run's own `excluded` flag still records the same distinction
    on the model's cells and the two must agree.
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
                # The two routes to the same fact must agree on the model's cells.
                if key == "e" and r["excluded"].get(d):
                    assert dropped == "non_positive", (r["origin"], r["h"], d)
                out.append({"origin": r["origin"], "horizon": r["h"], "year": r["target"],
                            "driver": d, "setting": name,
                            "projected": proj, "actual": act, "era": r["era"],
                            "log_error": le, "dropped": dropped})
    return out


def main():
    rows = build_cells()
    fore = build_cells(foresight=True)
    fore_cpi = build_cells(foresight_cpi_only=True)
    res = {"cells": len(rows), "origins": B.ORIGINS, "horizons": B.HORIZONS, "seed": SEED,
           "nboot": NBOOT, "blocks": BLOCKS, "drivers": {}, "sensitivity": {}, "macro_check": {}}
    eras = sorted(set(ERA.values()))
    for d in DRIVERS:
        a = agg(rows, "e", d)
        if a is None:
            continue
        rec = {"overall": a,
               # n IS THE CELLS THE SCORE TOOK; n_cells IS THE CELLS THAT EXIST.
               # A record carrying only the first cannot show a reader that a
               # driver was scored on half its history — one driver in this book
               # publishes a bias computed on NONE of its fifty cells — and the
               # coverage was recoverable only by running a census by hand. The
               # pair carries no threshold and makes no judgement; it makes the
               # fraction visible in the record that quotes the bias.
               "n_cells": sum(1 for r in rows if d in r.get("e", {})),
               "by_h": {h: agg(rows, "e", d, h=h) for h in B.HORIZONS},
               "by_era": {e: agg(rows, "e", d, era=e) for e in eras},
               "bootstrap": block_bootstrap(rows, d),
               "skill_vs_freeze": skill_pairs(rows, d, "ef"),
               "skill_vs_trend": skill_pairs(rows, d, "et"),
               "freeze_equivalent": d in B.FREEZE_EQUIVALENT}
        af = agg(fore, "e", d)
        acpi = agg(fore_cpi, "e", d)
        rec["mae_knowable"] = a["mae"]
        rec["mae_foresight"] = af["mae"] if af else None
        rec["mae_foresight_cpi_only"] = acpi["mae"] if acpi else None
        rec["macro_share"] = (1.0 - af["mae"] / a["mae"]) if (af and a["mae"] > 0) else None
        ev = [v for v in rec["by_era"].values() if v]
        rec["sign_flips"] = len(set(1 if e["bias"] > 0 else -1 for e in ev)) > 1 if len(ev) > 1 else False
        res["drivers"][d] = rec

    bad = []
    for d in sorted(B.NO_MACRO_TERM):
        ms = res["drivers"].get(d, {}).get("macro_share")
        if ms is not None and abs(ms) > 1e-9:
            bad.append((d, ms))
    res["macro_check"] = {"zero_by_construction": sorted(B.NO_MACRO_TERM), "violations": bad}
    assert not bad, "macro split is mis-wired: %s" % bad

    for beta in (0.5, 1.0):
        r2 = build_cells(beta=beta)
        res["sensitivity"]["beta_%.1f" % beta] = {
            d: agg(r2, "e", d) for d in ("revenue", "gross_profit", "pbt", "net")}
    r3 = build_cells(cost_on_fx=True)
    res["sensitivity"]["cost_on_fx"] = {d: agg(r3, "e", d) for d in ("cost_of_sales", "gross_profit", "pbt", "net")}

    # ---- the harvester's shape ---------------------------------------------
    res["by_driver"], res["by_horizon"], res["macro_split"], res["by_era"] = {}, {}, {}, {}
    for d, rec in res["drivers"].items():
        a, bs = rec["overall"], rec["bootstrap"]
        robust = all(bs.get(L) and bs[L]["same_sign"] for L in BLOCKS)
        res["by_driver"][d] = {"n": a["n"], "n_cells": rec.get("n_cells"),
                               # THE PAIR GOES WHERE THE READER LOOKS. The first
                               # cut put n_cells on the internal `drivers` block
                               # and every census reads THIS one — the disclosure
                               # in the working papers and not on the page, which
                               # is the defect this field exists to close.
                               "bias": round(a["bias"], 4), "mae": round(a["mae"], 4),
                               "over": round(a["share_over"], 3),
                               "excluded_nonpositive": a["excluded_nonpositive"],
                               "boot": {str(L): ({"lo": round(bs[L]["lo"], 4), "hi": round(bs[L]["hi"], 4)}
                                                 if bs.get(L) else None) for L in BLOCKS},
                               "robust_sign": bool(robust)}
        hh = {}
        for h in B.HORIZONS:
            v = rec["by_h"].get(h)
            if not v:
                continue
            ent = {"summary": {"n": v["n"], "bias": round(v["bias"], 4), "mae": round(v["mae"], 4),
                               "over": round(v["share_over"], 3), "robust_sign": bool(robust)}}
            if not rec["freeze_equivalent"]:
                sf = skill_pairs(rows, d, "ef", h=h)
                if sf:
                    ent["skill_freeze"] = sf
            st = skill_pairs(rows, d, "et", h=h)
            if st:
                ent["skill_trend"] = st
            hh[str(h)] = ent
        res["by_horizon"][d] = hh
        res["macro_split"][d] = {"as_known_mae": round(rec["mae_knowable"], 4),
                                 "perfect_mae": round(rec["mae_foresight"], 4) if rec["mae_foresight"] is not None else None,
                                 "cpi_only_mae": round(rec["mae_foresight_cpi_only"], 4) if rec["mae_foresight_cpi_only"] is not None else None,
                                 "macro_share": round(rec["macro_share"], 3) if rec["macro_share"] is not None else None}
        res["by_era"][d] = {e: {"n": v["n"], "bias": round(v["bias"], 4)} for e, v in rec["by_era"].items() if v}
    json.dump(res, open(os.path.join(HERE, "scores.json"), "w"), indent=1, default=str)
    json.dump(flatten_cells(rows, fore, fore_cpi),
              open(os.path.join(HERE, "error_cells.json"), "w"), indent=1)
    return res, rows


def pct(x):
    return "%+.1f%%" % ((math.exp(x) - 1) * 100) if x is not None else "   n/a"


if __name__ == "__main__":
    res, rows = main()
    print("EGCH fundamental walk-forward — %d cells, %d origins, FULL scope\n" % (res["cells"], len(res["origins"])))
    hdr = "%-18s %3s %4s %9s %8s %6s %7s  %-20s %-20s"
    print(hdr % ("driver", "n", "excl", "bias", "MAE", "over%", "macro%", "skill vs freeze", "skill vs trend"))
    print("-" * 118)
    for d in DRIVERS:
        r = res["drivers"].get(d)
        if not r:
            continue
        a = r["overall"]; sf = r["skill_vs_freeze"]; st = r["skill_vs_trend"]
        sfs = "n/a rule=benchmark" if r["freeze_equivalent"] else ("%+.3f (n=%d)" % (sf["skill"], sf["n"]) if sf else "n/a")
        sts = ("%+.3f (n=%d)" % (st["skill"], st["n"])) if st else "n/a"
        ms = "%.0f%%" % (100 * r["macro_share"]) if r["macro_share"] is not None else "n/a"
        print(hdr % (d, a["n"], a["excluded_nonpositive"], pct(a["bias"]), pct(a["mae"]),
                     "%.0f%%" % (100 * a["share_over"]), ms, sfs, sts))
    print("\nby era (bias, n):")
    for d in ("revenue", "gross_profit", "cost_of_sales", "debit_interest", "fx", "pbt", "net"):
        print("  %-16s %s" % (d, "  ".join("%s %s n=%d" % (e[:2], pct(v["bias"]), v["n"]) for e, v in res["by_era"].get(d, {}).items()) or "no positive pairs"))
    print("\nmacro check — zero by construction: %s; violations: %s"
          % (", ".join(res["macro_check"]["zero_by_construction"]), res["macro_check"]["violations"] or "none"))
    print("\nby horizon, net profit:")
    for h, v in res["by_horizon"]["net"].items():
        print("  h=%s n=%d bias %s mae %s skill_f %s skill_t %s" % (h, v["summary"]["n"], pct(v["summary"]["bias"]), pct(v["summary"]["mae"]),
              v.get("skill_freeze", {}).get("skill"), v.get("skill_trend", {}).get("skill")))
    print("\nsensitivity:")
    for k, v in res["sensitivity"].items():
        print("  %-12s %s" % (k, "  ".join("%s bias %s" % (d, pct(x["bias"])) for d, x in v.items() if x)))
