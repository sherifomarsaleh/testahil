"""How much of the break-era error is MACRO, on identical cells.

[R-FCAL-01] already requires each run to split its error macro-versus-company by
re-running every origin on the knowable inflation path and on perfect foresight.
Each run does that for itself and reports one pooled share. This asks the
question the pooled share cannot answer: how much of the DEVALUATION-YEAR error
is macro, name by name, on the SAME cells in every setting.

THE IDENTICAL-CELL CLAUSE IS NOT A DETAIL. Log scoring silently drops a cell
whose projection turns non-positive, and the settings drop DIFFERENT cells --
on EGCH the three settings score 61, 54 and 66 cells. Comparing those three
means comparing three samples, and a setting that happens to drop the worst
cells looks like an improvement. Every figure here is on the intersection.

Read live: python3 engine/valuation_calibration/macro_share.py
"""
import os, sys, math, json

HERE = os.path.dirname(os.path.abspath(__file__))
ENG = os.path.dirname(HERE)
DEVAL = {2022, 2023, 2024, 2025}

# (directory, drivers, settings). The settings are each run's OWN pre-registered
# macro settings, called by that run's own keyword names -- not renamed to a
# common vocabulary, because a rename is where a caller's mistake hides.
RUNS = [
    ("EGCH", "egch_walkforward",
     ["revenue", "cost_of_sales", "gross_profit", "pbt", "net"],
     [("asknown", {}), ("cpi_only", {"foresight_cpi_only": True}),
      ("foresight", {"foresight": True})]),
    ("AMOC", "amoc_walkforward",
     ["net_sales", "cost_of_sales", "gross_profit", "operating_profit", "pbt",
      "npat", "majority"],
     [("asknown", {}), ("cpi_only", {"foresight_cpi_only": True}),
      ("foresight", {"foresight": True})]),
    ("ARCC", "arcc_walkforward",
     ["revenue", "gross_profit", "pbt", "majority"],
     [("asknown", {}), ("cpi_only", {"foresight": True, "cpi_only": True}),
      ("foresight", {"foresight": True})]),
]


def _yr(o):
    d = "".join(c for c in str(o) if c.isdigit())
    return int(d[-4:]) if len(d) >= 4 else None


def measure(d, drivers, settings):
    path = os.path.join(ENG, d)
    sys.path.insert(0, path)
    for m in ("bottom_up", "panel", "score", "macro"):
        sys.modules.pop(m, None)
    import bottom_up as B
    P = None
    try:
        import panel as P
    except Exception:
        pass
    S = {}
    for lab, kw in settings:
        m = {}
        for o, h, t in B.cells():
            p = B.project(o, h, **kw)
            a = B.actual(t) if hasattr(B, "actual") else P.actual(t)
            for dr in drivers:
                pv, av = p.get(dr), a.get(dr)
                m[(o, h, dr)] = (math.log(pv / av)
                                 if (pv and av and pv > 0 and av > 0) else None)
        S[lab] = m
    sys.path.remove(path)
    keys = [k for k in S[settings[0][0]] if all(S[l][k] is not None for l in S)]
    out = {"common_cells": len(keys)}
    for lab, _ in settings:
        hit = [S[lab][k] for k in keys if _yr(k[0]) + k[1] in DEVAL]
        rest = [S[lab][k] for k in keys if _yr(k[0]) + k[1] not in DEVAL]
        mn = lambda v: sum(v) / len(v) if v else None
        ma = lambda v: sum(abs(x) for x in v) / len(v) if v else None
        out[lab] = {"n_deval": len(hit), "bias_deval": mn(hit), "mae_deval": ma(hit),
                    "n_other": len(rest), "bias_other": mn(rest), "mae_other": ma(rest)}
    return out


def main():
    res = {}
    for name, d, drivers, settings in RUNS:
        if not os.path.isdir(os.path.join(ENG, d)):
            continue
        res[name] = measure(d, drivers, settings)
    if not res:
        raise SystemExit("FAIL: no runs measured")

    print("Macro share of the devaluation-year error -- identical cells in every setting\n")
    f = lambda x: ("%+.3f" % x) if x is not None else "  -  "
    g = lambda x: ("%.3f" % x) if x is not None else "  -  "
    print("%-6s %-10s %5s %7s %6s %5s %7s %6s" %
          ("name", "setting", "n", "bias", "mae", "n", "bias", "mae"))
    print("%-6s %-10s %s %s" % ("", "", " " * 6 + "devaluation years", " " * 5 + "other years"))
    for n in res:
        r = res[n]
        for lab in ("asknown", "cpi_only", "foresight"):
            v = r.get(lab)
            if not v:
                continue
            print("%-6s %-10s %5d %7s %6s %5d %7s %6s" %
                  (n if lab == "asknown" else "", lab, v["n_deval"],
                   f(v["bias_deval"]), g(v["mae_deval"]), v["n_other"],
                   f(v["bias_other"]), g(v["mae_other"])))
        ak, fo = r["asknown"], r["foresight"]
        if ak["mae_deval"] and fo["mae_deval"]:
            print("%-6s macro share of the devaluation MAE: %.0f%%   (%d common cells)"
                  % ("", 100 * (1 - fo["mae_deval"] / ak["mae_deval"]), r["common_cells"]))
        print()
    json.dump(res, open(os.path.join(HERE, "macro_share.json"), "w"), indent=1)
    return res


if __name__ == "__main__":
    main()
