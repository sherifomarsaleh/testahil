"""Estimate driver corrections on resolved history only, then test them.

The rule was fixed in the pre-registration and is not relaxed here:

  * expanding window — a correction used at origin o is estimated only from
    forecasts that had already RESOLVED before o;
  * half strength — the applied correction is 0.5 x the estimated bias;
  * applied only where the bias holds its sign across eras;
  * reset after a structural break, defined as a driver error beyond its own
    two sigma.

Corrections are applied to the DRIVERS and the aggregates are rebuilt from
them, so a correction cannot quietly become a fudge on the bottom line.
"""
import json, os, math, statistics as st
import bottom_up as B
import score as S

HERE = os.path.dirname(os.path.abspath(__file__))
CORRECTABLE = ["units_sold", "asp", "units_delivered", "is.sga", "is.finance_cost"]
HALF = 0.5
BREAK_SIGMA = 2.0


def resolved_errors(panel, before_year):
    """Every (origin, horizon) log error whose target resolved strictly before
    `before_year`. This is the whole information set a correction may use."""
    out = {}
    for o in S.ORIGINS:
        if o >= before_year:
            continue
        proj = B.project(panel, o)
        for h in B.HORIZONS:
            t = o + h
            if t >= before_year or t > S.LAST_ACTUAL:
                continue
            for f in B.BENCH_FIELDS:
                p, a = proj[h].get(f), B.actual(panel, t, f)
                if p is None or a is None or p <= 0 or a <= 0:
                    continue
                out.setdefault(f, []).append({"origin": o, "h": h, "target": t,
                                              "e": math.log(p / a),
                                              "era": S.era_of(t)})
    return out


def estimate(panel, origin):
    """The correction each driver earns at this origin, and why."""
    hist = resolved_errors(panel, origin)
    out = {}
    for f in CORRECTABLE:
        rows = hist.get(f, [])
        if len(rows) < 3:
            out[f] = {"applied": 0.0, "reason": "fewer than three resolved errors",
                      "n": len(rows)}
            continue
        es = [r["e"] for r in rows]
        bias = sum(es) / len(es)
        by_era = {}
        for r in rows:
            by_era.setdefault(r["era"], []).append(r["e"])
        era_means = {k: sum(v) / len(v) for k, v in by_era.items() if len(v) >= 2}
        signs = {(1 if m > 0 else -1) for m in era_means.values()}
        stable = len(era_means) >= 2 and len(signs) == 1
        # structural break: the most recent error beyond the driver's own 2 sigma
        sd = st.pstdev(es) if len(es) > 1 else 0.0
        latest = max(rows, key=lambda r: (r["target"], r["h"]))
        broke = sd > 0 and abs(latest["e"] - bias) > BREAK_SIGMA * sd
        if broke:
            out[f] = {"applied": 0.0, "bias": round(bias, 4), "n": len(rows),
                      "reason": "reset — most recent error beyond the driver's own "
                                "two sigma (%.2f vs %.2f)" % (latest["e"], BREAK_SIGMA * sd),
                      "era_means": {k: round(v, 4) for k, v in era_means.items()}}
        elif not stable:
            out[f] = {"applied": 0.0, "bias": round(bias, 4), "n": len(rows),
                      "reason": "bias does not hold its sign across eras"
                                if len(era_means) >= 2 else
                                "only one era has two or more resolved errors",
                      "era_means": {k: round(v, 4) for k, v in era_means.items()}}
        else:
            out[f] = {"applied": round(HALF * bias, 4), "bias": round(bias, 4),
                      "n": len(rows), "reason": "sign stable across eras; half strength",
                      "era_means": {k: round(v, 4) for k, v in era_means.items()}}
    return out


def project_adjusted(panel, origin, corr):
    """Re-run the projection with each driver divided by exp(its correction),
    then rebuild every aggregate from the adjusted drivers."""
    raw = B.project(panel, origin)
    v = B.View(panel, origin)
    tax_rate = 0.225 if origin >= 2015 else 0.25
    cpu0 = v.ttm_ratio("is.cogs", "units_delivered", 3)
    delta = B.recognition_rate(v)
    bl = B.rolled_backlog(v).get(origin)
    out = {}
    for h in B.HORIZONS:
        r = dict(raw[h])
        for f in CORRECTABLE:
            c = corr.get(f, {}).get("applied", 0.0)
            if c and r.get(f) is not None:
                r[f] = r[f] * math.exp(-c)
        # rebuild from adjusted drivers, in the same order the projection built them
        if r.get("units_sold") is not None and r.get("asp") is not None:
            r["new_sales"] = r["units_sold"] * r["asp"]
        if delta is not None and bl is not None and r.get("new_sales") is not None:
            r["is.revenue"] = delta * (bl + r["new_sales"])
            bl = bl + r["new_sales"] - r["is.revenue"]
        if r.get("units_delivered") and raw[h].get("units_delivered"):
            # cost scales with the adjusted delivery volume, on the same cost
            # per unit the raw projection used
            r["is.cogs"] = raw[h]["is.cogs"] * (r["units_delivered"] /
                                                raw[h]["units_delivered"])
        if r.get("is.revenue") is not None and r.get("is.cogs") is not None:
            r["is.gross_profit"] = r["is.revenue"] - r["is.cogs"]
        if r.get("is.gross_profit") is not None and r.get("is.sga") is not None \
                and r.get("is.finance_cost") is not None:
            npbt = r["is.gross_profit"] - r["is.sga"] - (r.get("is.admin_depr") or 0.0) \
                - r["is.finance_cost"]
            r["is.npbt"] = npbt
            r["is.npat_mi"] = npbt * (1 - tax_rate) if npbt > 0 else npbt
        out[h] = r
    return out


def main():
    panel = B.load()
    log, rows_raw, rows_adj = [], [], []
    for o in S.ORIGINS:
        corr = estimate(panel, o)
        applied = {k: v["applied"] for k, v in corr.items() if v["applied"]}
        log.append({"origin": o, "corrections": corr, "any_applied": bool(applied)})
        if not applied:
            continue
        adj = project_adjusted(panel, o, corr)
        raw = B.project(panel, o)
        for h in B.HORIZONS:
            t = o + h
            if t > S.LAST_ACTUAL:
                continue
            for f in B.BENCH_FIELDS:
                a = B.actual(panel, t, f)
                pr, pa = raw[h].get(f), adj[h].get(f)
                if a is None or a <= 0:
                    continue
                if pr and pr > 0:
                    rows_raw.append({"origin": o, "h": h, "field": f,
                                     "e": math.log(pr / a)})
                if pa and pa > 0:
                    rows_adj.append({"origin": o, "h": h, "field": f,
                                     "e": math.log(pa / a)})
    json.dump({"log": log}, open(os.path.join(HERE, "corrections_log.json"), "w"),
              indent=1)

    print("WHAT EACH DRIVER EARNED, ORIGIN BY ORIGIN (expanding window)")
    print("%-6s %-18s %5s %8s %9s  %s" % ("origin", "driver", "n", "bias",
                                          "applied", "reason"))
    for entry in log:
        for f, c in entry["corrections"].items():
            if c["n"] < 3:
                continue
            print("%-6d %-18s %5d %8s %9.4f  %s" %
                  (entry["origin"], f, c["n"],
                   "%.4f" % c.get("bias", 0), c["applied"], c["reason"][:58]))

    print()
    print("ADJUSTED vs RAW, on the origins that carried a correction")
    key = lambda r: (r["origin"], r["h"], r["field"])
    R = {key(r): r["e"] for r in rows_raw}
    A = {key(r): r["e"] for r in rows_adj}
    shared = [k for k in R if k in A]
    fields = sorted({k[2] for k in shared})
    print("%-20s %5s %10s %10s %9s" % ("driver", "n", "raw MAE", "adj MAE", "change"))
    for f in fields:
        ks = [k for k in shared if k[2] == f]
        r = sum(abs(R[k]) for k in ks) / len(ks)
        a = sum(abs(A[k]) for k in ks) / len(ks)
        print("%-20s %5d %10.4f %10.4f %+9.4f" % (f, len(ks), r, a, a - r))
    print()
    print("BY ORIGIN — mean absolute log error across all drivers")
    print("%-8s %5s %10s %10s %9s" % ("origin", "n", "raw", "adjusted", "change"))
    for o in sorted({k[0] for k in shared}):
        ks = [k for k in shared if k[0] == o]
        r = sum(abs(R[k]) for k in ks) / len(ks)
        a = sum(abs(A[k]) for k in ks) / len(ks)
        print("%-8d %5d %10.4f %10.4f %+9.4f" % (o, len(ks), r, a, a - r))


if __name__ == "__main__":
    main()
