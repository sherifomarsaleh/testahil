"""ABUK fundamental walk-forward — scoring, exactly as pre-registered.

Log error per driver per horizon; bias, MAE, over-share, sign by era, and a
block bootstrap whose block is a WHOLE ORIGIN, so overlapping horizons are not
counted as independent evidence.
"""
import json, math, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
ORIGINS = ["FY2019", "FY2020", "FY2021", "FY2022", "FY2023", "FY2024"]
DRIVERS = ["vol_proxy", "rev", "cogs", "gp", "sell", "admin", "nonop", "pbt", "np"]
ERA = {"FY2020": "pre", "FY2021": "pre", "FY2022": "post", "FY2023": "post",
       "FY2024": "post", "FY2025": "post"}
NBOOT = 5000
random.seed(20260909)


def cells(panel, proj):
    """[(origin, target, h, driver, log-error)] for one projection set."""
    out = []
    for o in ORIGINS:
        for t, row in sorted(proj[o].items()):
            act = panel["years"][t]
            for d in DRIVERS:
                p, a = row.get(d), act.get(d)
                if p is None or a is None:
                    continue
                if p <= 0 or a <= 0:
                    out.append((o, t, row["h"], d, None))
                    continue
                out.append((o, t, row["h"], d, math.log(p / a)))
    return out


def _stats(es):
    es = [e for e in es if e is not None]
    if not es:
        return None
    n = len(es)
    bias = sum(es) / n
    mae = sum(abs(e) for e in es) / n
    over = sum(1 for e in es if e > 0) / n
    return dict(n=n, bias=bias, mae=mae, over=over)


def bootstrap(by_origin):
    """Resample WHOLE ORIGINS with replacement; return the 5-95 band on bias."""
    keys = [k for k in by_origin if by_origin[k]]
    if len(keys) < 2:
        return None
    out = []
    for _ in range(NBOOT):
        pick = [random.choice(keys) for _ in keys]
        pool = [e for k in pick for e in by_origin[k]]
        if pool:
            out.append(sum(pool) / len(pool))
    out.sort()
    return [out[int(0.05 * len(out))], out[int(0.95 * len(out))]]


def summarise(panel, proj, label):
    cs = cells(panel, proj)
    res = {}
    for d in DRIVERS:
        sel = [c for c in cs if c[3] == d]
        by_o = {}
        for o, t, h, _, e in sel:
            by_o.setdefault(o, [])
            if e is not None:
                by_o[o].append(e)
        s = _stats([c[4] for c in sel]) or {}
        s["ci90_bias"] = bootstrap(by_o)
        s["by_h"] = {}
        for h in range(1, 6):
            s["by_h"][h] = _stats([c[4] for c in sel if c[2] == h])
        s["by_era"] = {}
        for era in ("pre", "post"):
            s["by_era"][era] = _stats([c[4] for c in sel
                                       if ERA.get(c[1]) == era])
        res[d] = s
    return {"label": label, "drivers": res,
            "cells": [dict(origin=o, target=t, h=h, driver=d, logerr=e)
                      for o, t, h, d, e in cs]}


def main():
    panel = json.load(open(os.path.join(HERE, "panel.json")))
    proj = json.load(open(os.path.join(HERE, "projections.json")))
    out = {}
    for key, label in [("model", "pre-registered ground-up model"),
                       ("freeze", "naive benchmark FREEZE (flat at last actual)"),
                       ("trend", "naive benchmark TREND (trailing 3y CAGR)"),
                       ("macro_perfect", "model on the actual macro path"),
                       ("foresight", "model on perfect foresight")]:
        out[key] = summarise(panel, proj[key], label)
    json.dump(out, open(os.path.join(HERE, "scores.json"), "w"), indent=1,
              sort_keys=True, default=float)
    return out


if __name__ == "__main__":
    o = main()
    hdr = "%-10s %8s %8s %8s %8s %8s %8s" % (
        "driver", "n", "bias", "MAE", "over%", "freezeMAE", "trendMAE")
    print(hdr); print("-" * len(hdr))
    for d in DRIVERS:
        m, f, t = o["model"]["drivers"][d], o["freeze"]["drivers"][d], o["trend"]["drivers"][d]
        print("%-10s %8d %8.3f %8.3f %7.0f%% %9.3f %9.3f" % (
            d, m["n"], m["bias"], m["mae"], 100 * m["over"], f["mae"], t["mae"]))
    print()
    print("skill by horizon — model MAE vs freeze / trend, on revenue and net profit")
    for d in ("rev", "np"):
        for h in range(1, 6):
            m = o["model"]["drivers"][d]["by_h"][h]
            f = o["freeze"]["drivers"][d]["by_h"][h]
            t = o["trend"]["drivers"][d]["by_h"][h]
            if not m:
                continue
            print("  %-4s h=%d n=%d  model %.3f  freeze %.3f  trend %.3f   %s" % (
                d, h, m["n"], m["mae"], f["mae"], t["mae"],
                "BEATS BOTH" if m["mae"] < f["mae"] and m["mae"] < t["mae"]
                else ("beats freeze" if m["mae"] < f["mae"] else
                      ("beats trend" if m["mae"] < t["mae"] else "beats neither"))))
