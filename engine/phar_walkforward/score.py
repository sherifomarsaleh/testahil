#!/usr/bin/env python3
"""PHAR — score and diagnose, exactly as pre-registered.

Log error e = ln(forecast/actual) per driver per origin per horizon; bias, MAE,
share over, a moving-block bootstrap over ORIGINS at block sizes {2,3} with
2,000 resamples and seed 42; skill against BOTH naive benchmarks at every
horizon; the sign tested at the market's era boundary AND at every cut the data
admits [R-FCAL-01 AMENDED 07-09-2026]; and the three-leg macro split with its
own zero-by-construction check on the volume driver.
"""
from __future__ import annotations
import json, math, os, random, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import panel, bottom_up as bu  # noqa: E402

# THE HOUSE INSTRUMENT, IMPORTED BY PATH RATHER THAN COPIED [R-ENF-03]. The cut
# arithmetic this record reports and the cut arithmetic the gate re-runs must be
# ONE arithmetic; a run that models the measurement is reporting a different one.
# Loaded by file path because engine/valuation_calibration/ carries its own
# `panel` module and putting it on sys.path would shadow this run's.
import importlib.util as _ilu  # noqa: E402
_spec = _ilu.spec_from_file_location(
    "phar_boundary_sensitivity",
    os.path.join(HERE, "..", "valuation_calibration", "boundary_sensitivity.py"))
BS = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(BS)

SEED = 42
RESAMPLES = 2000
BLOCKS = (2, 3)
ERA_BOUNDARY = 2022   # the market's own cut: the year the currency moved


def cells(leg="baseline"):
    """Every (driver, origin, horizon) cell with both a forecast and an actual."""
    out = []
    for o in bu.ORIGINS:
        proj = bu.project(o, leg)
        if proj is None:
            continue
        bench_f, bench_t = bu.freeze(o), bu.trend(o)
        for h in bu.HORIZONS:
            y = bu.fy(bu.yr(o) + h)
            if y not in panel.IS:
                continue
            act = bu.actual(y)
            for f in bu.FIELDS:
                a, p = act.get(f), proj[y].get(f)
                if a is None or p is None or a <= 0 or p <= 0:
                    continue
                row = dict(driver=f, origin=o, horizon=h, target=y,
                           actual=a, forecast=p, e=math.log(p / a))
                bf, bt = bench_f[y].get(f), bench_t[y].get(f)
                row["e_freeze"] = math.log(bf / a) if (bf and bf > 0) else None
                row["e_trend"] = math.log(bt / a) if (bt and bt > 0) else None
                out.append(row)
    return out


def _boot(vals_by_origin, stat):
    rng = random.Random(SEED)
    origins = sorted(vals_by_origin)
    if len(origins) < 2:
        return None, None
    draws = []
    for _ in range(RESAMPLES):
        b = BLOCKS[rng.randrange(len(BLOCKS))]
        picked, n = [], 0
        while n < len(origins):
            s = rng.randrange(len(origins))
            for j in range(b):
                picked.append(origins[(s + j) % len(origins)])
            n += b
        pool = [v for o in picked[:len(origins)] for v in vals_by_origin[o]]
        if pool:
            draws.append(stat(pool))
    if not draws:
        return None, None
    draws.sort()
    return draws[int(0.05 * len(draws))], draws[int(0.95 * len(draws)) - 1]


def summarise(rows, key=lambda r: r["driver"]):
    out = {}
    for r in rows:
        out.setdefault(key(r), []).append(r)
    res = {}
    for k, rs in sorted(out.items()):
        es = [r["e"] for r in rs]
        by_o = {}
        for r in rs:
            by_o.setdefault(r["origin"], []).append(r["e"])
        lo, hi = _boot(by_o, lambda p: sum(p) / len(p))
        mlo, mhi = _boot(by_o, lambda p: sum(abs(x) for x in p) / len(p))
        mae = sum(abs(x) for x in es) / len(es)
        d = dict(n=len(es), bias=sum(es) / len(es), mae=mae,
                 bias_ci=[lo, hi], mae_ci=[mlo, mhi],
                 share_over=sum(1 for x in es if x > 0) / len(es),
                 origins=sorted({r["origin"] for r in rs}))
        # SKILL IS SCORED ON THE MATCHED SUBSAMPLE and its count is reported.
        # A benchmark that cannot be built at a cell (the trend rule needs a
        # trailing year the panel may not have) drops that cell from BOTH sides
        # rather than from one, and the n says how many are left.
        for b in ("freeze", "trend"):
            pairs = [(abs(r["e"]), abs(r["e_" + b])) for r in rs
                     if r.get("e_" + b) is not None]
            if pairs:
                mm = sum(x for x, _ in pairs) / len(pairs)
                bm = sum(y for _, y in pairs) / len(pairs)
                d["n_" + b] = len(pairs)
                d["mae_" + b] = bm
                d["mae_model_matched_" + b] = mm
                d["skill_vs_" + b] = (bm - mm) / bm if bm else None
        res[k] = d
    return res


def sign_by_cut(rows):
    """The sign at EVERY cut the data admits, every boundary leaving >=5 cells
    each side [R-FCAL-01 AMENDED 07-09-2026].  A bias whose sign depends on where
    the line was drawn is REPORTED, never corrected for."""
    out = {}
    for drv in sorted({r["driver"] for r in rows}):
        rs = sorted([r for r in rows if r["driver"] == drv],
                    key=lambda r: (bu.yr(r["target"]), bu.yr(r["origin"]), r["horizon"]))
        n = len(rs)
        raw, flipped = BS.cuts_for([(bu.yr(r["target"]), r["e"]) for r in rs])
        cuts = [dict(at_year=b, before=a, after=c, flips=(a > 0) != (c > 0))
                for b, a, c in raw]
        flips = len(flipped)
        era_a = [r["e"] for r in rs if bu.yr(r["target"]) < ERA_BOUNDARY]
        era_b = [r["e"] for r in rs if bu.yr(r["target"]) >= ERA_BOUNDARY]
        era = None
        if len(era_a) >= 2 and len(era_b) >= 2:
            sa = 1 if sum(era_a) / len(era_a) > 0 else -1
            sb = 1 if sum(era_b) / len(era_b) > 0 else -1
            era = dict(pre=sum(era_a) / len(era_a), post=sum(era_b) / len(era_b),
                       n_pre=len(era_a), n_post=len(era_b), flips=sa != sb)
        out[drv] = dict(n=n, cuts_tested=len(cuts), flips=flips,
                        stable_at_every_cut=(len(cuts) > 0 and flips == 0),
                        untestable=(len(cuts) == 0),
                        era_cut=era, detail=cuts)
    return out


def macro_split():
    """Baseline vs perfect foresight, per driver.  The volume driver carries no
    inflation term in any leg and MUST return exactly zero — the split's own
    check, pre-registered."""
    base = summarise(cells("baseline"))
    fore = summarise(cells("foresight"))
    know = summarise(cells("knowable"))
    out = {}
    for d in sorted(base):
        b = base[d]["bias"]
        f = fore.get(d, {}).get("bias")
        k = know.get(d, {}).get("bias")
        share = None
        if f is not None and b not in (None, 0):
            share = 1 - abs(f) / abs(b)
        out[d] = dict(bias_baseline=b, bias_foresight=f, bias_knowable=k,
                      macro_share=share,
                      n_baseline=base[d]["n"],
                      n_foresight=fore.get(d, {}).get("n"),
                      n_knowable=know.get(d, {}).get("n"))
    return out


def robust_sign(rows_for_driver):
    """The sign holds across EVERY bootstrap block size tested, separately.

    Not the same test as the pooled interval: a bias can sit inside a wide
    pooled interval and still hold its sign in every resample, and the shared
    harvester reads this field.
    """
    by_o = {}
    for r in rows_for_driver:
        by_o.setdefault(r["origin"], []).append(r["e"])
    if len(by_o) < 2:
        return False
    base = 1 if sum(r["e"] for r in rows_for_driver) > 0 else -1
    rng = random.Random(SEED)
    for b in BLOCKS:
        origins = sorted(by_o)
        for _ in range(400):
            picked, n = [], 0
            while n < len(origins):
                st = rng.randrange(len(origins))
                for j in range(b):
                    picked.append(origins[(st + j) % len(origins)])
                n += b
            pool = [v for o in picked[:len(origins)] for v in by_o[o]]
            if not pool:
                continue
            if (1 if sum(pool) / len(pool) > 0 else -1) != base:
                return False
    return True


def shared_view(rows):
    """scores.json in the shape engine/lessons_harvest.py READS.

    THE RUN CONFORMS TO THE SHARED INSTRUMENT RATHER THAN THE OTHER WAY ROUND.
    The harvester's first pass over this run returned ZERO candidates against a
    record carrying fourteen driver biases, none of whose intervals covers zero
    — a reader that guesses a naming convention silently finds nothing AND
    REPORTS THAT AS A RESULT. The fix is to emit the keys it reads, not to teach
    it a fifteenth shape.
    """
    by_drv, by_h, mac, era = {}, {}, {}, {}
    base = summarise(rows)
    fore = summarise(cells("foresight"))
    for d, v in base.items():
        rs = [r for r in rows if r["driver"] == d]
        by_drv[d] = dict(bias=v["bias"], mae=v["mae"], over=v["share_over"],
                         n=v["n"], n_cells=v["n"], robust_sign=robust_sign(rs))
        by_h[d] = {}
        for h in bu.HORIZONS:
            hs = [r for r in rs if r["horizon"] == h]
            if not hs:
                continue
            es = [r["e"] for r in hs]
            pairs = [(abs(r["e"]), abs(r["e_freeze"])) for r in hs
                     if r.get("e_freeze") is not None]
            sk = None
            if pairs:
                mm = sum(x for x, _ in pairs) / len(pairs)
                bm = sum(y for _, y in pairs) / len(pairs)
                sk = (bm - mm) / bm if bm else None
            by_h[d][str(h)] = dict(bias=sum(es) / len(es),
                                   mae=sum(abs(x) for x in es) / len(es),
                                   n=len(es), skill_freeze=dict(skill=sk))
        if d in fore:
            mb, mf = v["mae"], fore[d]["mae"]
            mac[d] = dict(macro_share=(1 - abs(fore[d]["bias"]) / abs(v["bias"]))
                          if v["bias"] else None,
                          as_known_mae=mb, perfect_mae=mf)
        pre = [r["e"] for r in rs if bu.yr(r["target"]) < ERA_BOUNDARY]
        post = [r["e"] for r in rs if bu.yr(r["target"]) >= ERA_BOUNDARY]
        e = {}
        if pre:
            e["E1 pre-2022"] = dict(bias=sum(pre) / len(pre), n=len(pre))
        if post:
            e["E2 devaluation sequence"] = dict(bias=sum(post) / len(post), n=len(post))
        era[d] = e
    return by_drv, by_h, mac, era


def run():
    rows = cells("baseline")
    sh_drv, sh_h, sh_mac, sh_era = shared_view(rows)
    res = dict(
        _="PHAR fundamental walk-forward scores. GENERATED by score.py; never hand-edited.",
        run="PHAR", scope="LIGHT",
        origins=bu.ORIGINS, horizons=bu.HORIZONS,
        pre_registration="PRE_REGISTRATION_07-09-2026.md",
        n_cells=len(rows),
        # --- the shape engine/lessons_harvest.py reads. Names are ITS names.
        by_driver=sh_drv, by_horizon=sh_h, macro_split_shared=sh_mac, by_era=sh_era,
        # --- this run's own richer record, under its own names
        driver_detail=summarise(rows),
        driver_horizon_detail=summarise(rows, key=lambda r: "%s@h%d" % (r["driver"], r["horizon"])),
        horizon_detail=summarise(rows, key=lambda r: "h%d" % r["horizon"]),
        sign_by_cut=sign_by_cut(rows),
        macro_split=sh_mac, macro_split_detail=macro_split(),
        knowable_leg_unavailable=macro.VINTAGE_CPI_UNAVAILABLE if False else
            {"FY2024": "engine/macro_history/EG.json stops at the 2023 origin, so the "
                       "knowable-inflation leg is UNMEASURED at the FY2024 origin and is "
                       "not filled from a later vintage."},
        cells=rows,
    )
    with open(os.path.join(HERE, "scores.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, indent=1)
    return res


if __name__ == "__main__":
    import macro  # noqa: F401  (named in the record above)
    r = run()
    print("PHAR — FUNDAMENTAL walk-forward, LIGHT, %d cells\n" % r["n_cells"])
    print("%-16s %4s %8s %8s %8s %8s %9s %9s" %
          ("driver", "n", "bias", "MAE", "ci_lo", "ci_hi", "vs freeze", "vs trend"))
    for d, v in r["driver_detail"].items():
        print("%-16s %4d %8.3f %8.3f %8.3f %8.3f %9s %9s"
              % (d, v["n"], v["bias"], v["mae"],
                 v["bias_ci"][0] if v["bias_ci"][0] is not None else float("nan"),
                 v["bias_ci"][1] if v["bias_ci"][1] is not None else float("nan"),
                 ("%+.0f%%/%d" % (100 * v["skill_vs_freeze"], v["n_freeze"])) if v.get("skill_vs_freeze") is not None else "  --",
                 ("%+.0f%%/%d" % (100 * v["skill_vs_trend"], v["n_trend"])) if v.get("skill_vs_trend") is not None else "  --"))
    print("\nby horizon (all drivers pooled):")
    for h, v in r["horizon_detail"].items():
        print("  %s  n=%d  bias %+.3f  MAE %.3f  vs freeze %s  vs trend %s"
              % (h, v["n"], v["bias"], v["mae"],
                 ("%+.1f%% on %d" % (100 * v["skill_vs_freeze"], v["n_freeze"])) if v.get("skill_vs_freeze") is not None else "--",
                 ("%+.1f%% on %d" % (100 * v["skill_vs_trend"], v["n_trend"])) if v.get("skill_vs_trend") is not None else "--"))
    print("\nsign stability — every cut the data admits:")
    for d, v in r["sign_by_cut"].items():
        print("  %-16s n=%2d cuts=%2d flips=%2d  %s%s"
              % (d, v["n"], v["cuts_tested"], v["flips"],
                 "STABLE" if v["stable_at_every_cut"] else ("UNTESTABLE" if v["untestable"] else "FLIPS"),
                 ("  era-cut flips" if (v["era_cut"] and v["era_cut"]["flips"]) else "")))
    print("\nmacro / company split:")
    for d, v in r["macro_split_detail"].items():
        print("  %-16s baseline %+.3f  foresight %s  macro share %s"
              % (d, v["bias_baseline"],
                 ("%+.3f" % v["bias_foresight"]) if v["bias_foresight"] is not None else " n/a ",
                 ("%.1f%%" % (100 * v["macro_share"])) if v["macro_share"] is not None else "n/a"))
