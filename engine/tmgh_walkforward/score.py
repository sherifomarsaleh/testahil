"""TMGH walk-forward — scoring, exactly as §6 of the pre-registration fixed it.

Log error per driver per horizon; bias and MAE; a moving-block bootstrap over
origins at block lengths {2,3,4} with a bias called robust only where its sign
holds across all three; over- and under-forecast shares; sign by era; the
macro/company split from the as-known and perfect-foresight pair; and skill
against BOTH naive benchmarks at every horizon.

Sign cases — where either side is <= 0 and the log is undefined — are neither
dropped nor patched. They are counted separately and scored on a relative
difference, and never pooled into the log statistics.
"""
import json, math, os, random, sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bottom_up as BU

DRIVERS = ["new_sales", "dev_revenue", "dev_cost", "recurring_revenue", "recurring_cost",
           "total_revenue", "gross_profit", "sga", "da", "finance_cost", "net_profit",
           "customer_advances", "development_properties", "backlog", "ppe"]
BLOCKS = [2, 3, 4]
RESAMPLES = 2000
ERAS = [("E1 pre-float", 2011, 2015), ("E2 post-float", 2016, 2021),
        ("E3 devaluation", 2022, 2025)]
# Drivers whose rule carries no inflation term. Their macro share must come back
# as exactly zero by construction; the check is printed, never asserted.
NO_INFLATION_TERM = ["finance_cost"]


# Cost and expense lines are stored with the company's own sign, which is
# negative. That sign is a presentation convention, not information: a cost
# forecast is right or wrong by its MAGNITUDE. Scoring them on the raw signed
# value would make every cost cell an undefined log and quietly drop the entire
# cost side of the model from the record.
MAGNITUDE = {"dev_cost", "recurring_cost", "sga", "da", "finance_cost"}


def _cell(o, h, y, d, setting, p, a):
    rec = {"origin": o, "horizon": h, "year": y, "driver": d,
           "setting": setting, "projected": p, "actual": a, "era": era_of(y)}
    pp, aa = (abs(p), abs(a)) if d in MAGNITUDE else (p, a)
    if d in MAGNITUDE:
        rec["scored_on"] = "magnitude"
    if pp > 0 and aa > 0:
        rec["log_error"] = math.log(pp / aa)
    else:
        rec["sign_case"] = True
        rec["rel_error"] = (p - a) / abs(a) if a else None
    return rec


def era_of(y):
    for name, lo, hi in ERAS:
        if lo <= y <= hi:
            return name
    return "?"


def cells(bujson):
    """Every (origin, horizon, driver) cell, on both macro settings."""
    A = {int(k): v for k, v in bujson["actuals"].items()}
    out = []
    for key, run in bujson["runs"].items():
        o, setting = key.split("|")
        o = int(o)
        for h, f in run["projection"].items():
            h = int(h)
            y = o + h
            if y > bujson["last_actual"]:
                continue
            for d in DRIVERS:
                p, a = f.get(d), A.get(y, {}).get(d)
                if p is None or a is None:
                    continue
                out.append(_cell(o, h, y, d, setting, p, a))
    return out, A


def bench(bujson, A):
    """freeze and trend, for the same cells."""
    out = []
    for o in range(bujson["first_origin"], bujson["last_origin"] + 1):
        for h in BU.HORIZONS:
            y = o + h
            if y > bujson["last_actual"]:
                continue
            for d in DRIVERS:
                a = A.get(y, {}).get(d)
                if a is None:
                    continue
                for nm, fn in (("freeze", BU.freeze), ("trend", BU.trend)):
                    p = fn(A, o, d, h)
                    if p is None:
                        continue
                    out.append(_cell(o, h, y, d, nm, p, a))
    return out


def block_bootstrap(rows, key="log_error", seed=42):
    """Moving-block bootstrap over ORIGINS, at each block length."""
    origins = sorted({r["origin"] for r in rows})
    by = defaultdict(list)
    for r in rows:
        if key in r:
            by[r["origin"]].append(r[key])
    if len(origins) < 2:
        return {}
    out = {}
    for L in BLOCKS:
        rnd = random.Random(seed + L)
        means = []
        nblocks = max(1, len(origins) // L)
        starts = list(range(0, max(1, len(origins) - L + 1)))
        for _ in range(RESAMPLES):
            vals = []
            for _b in range(nblocks):
                s = rnd.choice(starts)
                for o in origins[s:s + L]:
                    vals += by.get(o, [])
            if vals:
                means.append(sum(vals) / len(vals))
        if not means:
            continue
        means.sort()
        out["block_%d" % L] = {
            "mean": sum(means) / len(means),
            "ci_lo": means[int(0.025 * len(means))],
            "ci_hi": means[int(0.975 * len(means)) - 1]}
    return out


def summarise(rows, label):
    logs = [r["log_error"] for r in rows if "log_error" in r]
    signs = [r for r in rows if r.get("sign_case")]
    if not logs:
        return None
    bias = sum(logs) / len(logs)
    mae = sum(abs(x) for x in logs) / len(logs)
    bs = block_bootstrap(rows)
    robust = (len(bs) == len(BLOCKS)
              and len({1 if v["ci_lo"] > 0 else (-1 if v["ci_hi"] < 0 else 0)
                       for v in bs.values()}) == 1
              and all(v["ci_lo"] > 0 or v["ci_hi"] < 0 for v in bs.values()))
    by_era = {}
    for name, _, _ in ERAS:
        e = [r["log_error"] for r in rows if r.get("era") == name and "log_error" in r]
        if e:
            by_era[name] = {"n": len(e), "bias": sum(e) / len(e)}
    return {"label": label, "n": len(logs), "n_sign_cases": len(signs),
            "bias": bias, "mae": mae,
            "share_over": sum(1 for x in logs if x > 0) / len(logs),
            "share_under": sum(1 for x in logs if x < 0) / len(logs),
            "bootstrap": bs, "robust_sign": robust,
            "sign_holds_across_eras": (len({1 if v["bias"] > 0 else -1
                                            for v in by_era.values()}) == 1
                                       if len(by_era) > 1 else None),
            "by_era": by_era}


def main():
    bj = json.load(open(os.path.join(HERE, "bottom_up.json")))
    rows, A = cells(bj)
    rows += bench(bj, A)
    json.dump(rows, open(os.path.join(HERE, "error_cells.json"), "w"), indent=1)

    scores = {}
    for setting in ("asknown", "foresight", "freeze", "trend"):
        for d in DRIVERS:
            sel = [r for r in rows if r["setting"] == setting and r["driver"] == d]
            s = summarise(sel, "%s/%s/all" % (setting, d))
            if s:
                scores["%s|%s|all" % (setting, d)] = s
            for h in BU.HORIZONS:
                sh = summarise([r for r in sel if r["horizon"] == h],
                               "%s/%s/h%d" % (setting, d, h))
                if sh:
                    scores["%s|%s|h%d" % (setting, d, h)] = sh
    json.dump(scores, open(os.path.join(HERE, "scores.json"), "w"), indent=1)

    print("=== per driver, pooled over horizons, as-known macro ===")
    print("%-24s %4s %8s %8s %7s %8s %s" % ("driver", "n", "bias", "MAE",
                                            "over%", "robust", "era signs"))
    for d in DRIVERS:
        s = scores.get("asknown|%s|all" % d)
        if not s:
            continue
        eras = " ".join("%s%+0.2f" % (k.split()[0], v["bias"])
                        for k, v in s["by_era"].items())
        print("%-24s %4d %+8.3f %8.3f %6.0f%% %8s %s"
              % (d, s["n"], s["bias"], s["mae"], 100 * s["share_over"],
                 "YES" if s["robust_sign"] else "no", eras))

    print("\n=== skill against the naive benchmarks (MAE, lower is better) ===")
    print("%-20s %5s %9s %9s %9s   %s" % ("driver", "h", "model", "freeze", "trend", "verdict"))
    for d in ("total_revenue", "dev_revenue", "gross_profit", "net_profit", "new_sales"):
        for h in BU.HORIZONS:
            m = scores.get("asknown|%s|h%d" % (d, h))
            f = scores.get("freeze|%s|h%d" % (d, h))
            t = scores.get("trend|%s|h%d" % (d, h))
            if not (m and f):
                continue
            beats = []
            if m["mae"] < f["mae"]:
                beats.append("freeze")
            if t and m["mae"] < t["mae"]:
                beats.append("trend")
            print("%-20s %5d %9.3f %9.3f %9s   %s"
                  % (d, h, m["mae"], f["mae"],
                     ("%.3f" % t["mae"]) if t else "-",
                     ("beats " + "+".join(beats)) if beats else "BEATS NEITHER"))

    print("\n=== macro vs company split (bias, as-known minus perfect foresight) ===")
    print("%-24s %10s %10s %10s   %s" % ("driver", "as-known", "foresight",
                                         "macro part", "check"))
    for d in DRIVERS:
        a = scores.get("asknown|%s|all" % d)
        f = scores.get("foresight|%s|all" % d)
        if not (a and f):
            continue
        chk = ""
        if d in NO_INFLATION_TERM:
            chk = ("zero by construction: OK" if abs(a["bias"] - f["bias"]) < 1e-9
                   else "NON-ZERO - the rule has an inflation term it should not have")
        print("%-24s %+10.3f %+10.3f %+10.3f   %s"
              % (d, a["bias"], f["bias"], a["bias"] - f["bias"], chk))


if __name__ == "__main__":
    main()
