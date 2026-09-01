"""ARCC walk-forward — decomposition, the macro/company split, and the
projected-versus-actual income statement for EVERY origin.

Implements PRE_REGISTRATION_01-09-2026.md §4 and §5. Measurement only.
"""
import os, sys, json, math

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import panel as P
import bottom_up as B
import score as S


def revenue_decomposition():
    """Split the revenue error into volume, channel mix and realised price.

    Done by SUBSTITUTION, one factor at a time, from the projection toward the
    actual: the residual is reported rather than distributed, so a reader can
    see how much of the revenue miss the three factors do not explain.
    """
    out = []
    for o, h, t in B.cells():
        p, a = B.project(o, h), B.actual(t)
        if not (p["revenue"] > 0 and a["revenue"] > 0):
            continue
        total = math.log(p["revenue"] / a["revenue"])

        def rev(vl, ve, pl, pe, sv):
            return pl * vl * 1000.0 + pe * ve * 1000.0 + sv

        base = rev(p["vol_local"], p["vol_export"], p["price_local"], p["price_export"], p["services"])
        f_vol = rev(a["vol_local"], a["vol_export"], p["price_local"], p["price_export"], p["services"])
        f_price = rev(a["vol_local"], a["vol_export"], a["price_local"], a["price_export"], p["services"])
        f_svc = rev(a["vol_local"], a["vol_export"], a["price_local"], a["price_export"], a["services"])
        out.append({
            "origin": o, "h": h, "target": t, "total_log_err": total,
            "volume": math.log(base / f_vol) if f_vol > 0 else None,
            "price": math.log(f_vol / f_price) if f_price > 0 else None,
            "services": math.log(f_price / f_svc) if f_svc > 0 else None,
            "residual": total - math.log(base / f_svc) if f_svc > 0 else None,
        })
    return out


def profit_decomposition():
    """Split the profit-before-tax error into the lines that produce it.

    In EGP rather than in logs: a profit error is a sum of line errors and the
    sum is the honest object. Logs are reported beside it for the drivers.
    """
    out = []
    for o, h, t in B.cells():
        p, a = B.project(o, h), B.actual(t)
        out.append({
            "origin": o, "h": h, "target": t,
            "pbt_projected": p["pbt"], "pbt_actual": a["pbt"],
            "pbt_error": p["pbt"] - a["pbt"],
            "from_revenue": p["revenue"] - a["revenue"],
            "from_cogs": -(p["cogs"] - a["cogs"]),
            "from_ga": -(p["ga"] - a["ga"]),
            "from_fx": -(p["fx"] - a["fx"]),
            "from_other": ((p["provisions"] - a["provisions"]) * -1
                           + (p["reversals"] - a["reversals"])
                           + (p["interest_income"] - a["interest_income"])
                           + (p["other_income"] - a["other_income"])
                           + (p["impairments"] - a["impairments"]) * -1
                           + (p["finance_costs"] - a["finance_costs"]) * -1
                           + (p["disposals"] - a["disposals"])
                           + (p["jv"] - a["jv"])),
        })
    return out


IS_LINES = [
    ("revenue", "Revenue"), ("cogs", "Cost of sales"), ("gross_profit", "Gross profit"),
    ("ga", "General and administration"), ("provisions", "Provisions"),
    ("interest_income", "Interest income"), ("other_income", "Other income"),
    ("finance_costs", "Finance costs"), ("fx", "Foreign exchange"),
    ("pbt", "Profit before tax"), ("tax", "Income tax"), ("pat", "Profit after tax"),
]


def side_by_side(path):
    """The projected-versus-actual income statement for EVERY origin and horizon.

    [R-FCAL-01] §4 requires this and it is not a summary: twenty-five statements,
    line by line, so a reader can see WHERE a profit miss came from rather than
    being told how large it was.
    """
    lines = ["# ARCC — projected versus actual income statement, every origin",
             "",
             "Every cell of the walk-forward, line by line, in EGP millions. `proj` is the",
             "pre-registered mechanical build standing at the origin; `act` is what the company",
             "reported for that year, as first reported. Internal evidence — never shown to a",
             "reader of the study.", ""]
    for o in B.ORIGINS:
        cs = [(oo, h, t) for (oo, h, t) in B.cells() if oo == o]
        if not cs:
            lines += ["## Origin %s — no horizon has matured" % o, ""]
            continue
        lines += ["## Origin %s (%s)" % (o, B.ERA[o]), ""]
        head = "| line | " + " | ".join("h%d %s proj | h%d act" % (h, t[2:], h)
                                        for _, h, t in cs) + " |"
        lines += [head, "|" + "---|" * (1 + 2 * len(cs))]
        proj = {h: B.project(o, h) for _, h, _ in cs}
        act = {h: B.actual(t) for _, h, t in cs}
        for key, label in IS_LINES:
            cells = []
            for _, h, _ in cs:
                cells.append("%.0f" % (proj[h][key] / 1e6))
                cells.append("%.0f" % (act[h][key] / 1e6))
            lines.append("| %s | %s |" % (label, " | ".join(cells)))
        lines.append("")
    open(path, "w").write("\n".join(lines))
    return path


def run():
    rows, out = S.run()
    diag = {
        "revenue_decomposition": revenue_decomposition(),
        "profit_decomposition": profit_decomposition(),
        "macro_wiring_check": S.check_macro_wiring(out),
    }
    # A driver whose bias holds its sign across BOTH eras and survives the
    # bootstrap at ALL THREE block lengths is a CANDIDATE for §7. Nothing is
    # adopted here; this only lists what clears the pre-registered bar.
    cands = []
    for d in S.DRIVERS:
        e = out["eras"][d]
        ks = sorted(e)
        if len(ks) < 2 or not e[ks[0]] or not e[ks[1]]:
            continue
        same = (e[ks[0]]["bias"] > 0) == (e[ks[1]]["bias"] > 0)
        b = out["bootstrap"][d]
        robust = bool(b) and all(v["robust_sign"] for v in b.values())
        cands.append({"driver": d, "bias": out["drivers"][d]["bias"],
                      "era1": e[ks[0]]["bias"], "era2": e[ks[1]]["bias"],
                      "same_sign_both_eras": same, "robust_all_blocks": robust,
                      "clears_bar": bool(same and robust),
                      "skill_vs_freeze": (out["skill"][d]["vs_freeze"] or {}).get("skill"),
                      "equals_freeze": out["skill"][d]["equals_freeze_by_construction"]})
    diag["correction_candidates"] = cands
    return out, diag


if __name__ == "__main__":
    out, diag = run()
    json.dump(diag, open(os.path.join(HERE, "diagnostics.json"), "w"), indent=1, default=str)
    p = side_by_side(os.path.join(HERE, "arcc_IS_projected_vs_actual_all_origins.md"))
    print("wrote", os.path.basename(p))
    print()
    print("CORRECTION CANDIDATES — the pre-registered bar is same sign in BOTH eras")
    print("AND a robust sign at all three bootstrap block lengths.")
    print()
    print("%-18s %8s %8s %8s %6s %7s %10s %s" %
          ("driver", "bias", "era1", "era2", "eras", "robust", "vs freeze", "clears"))
    for c in diag["correction_candidates"]:
        print("%-18s %+8.3f %+8.3f %+8.3f %6s %7s %10s %s" %
              (c["driver"], c["bias"], c["era1"], c["era2"],
               "same" if c["same_sign_both_eras"] else "FLIP",
               "yes" if c["robust_all_blocks"] else "no",
               "n/a" if c["equals_freeze"] else
               ("%+.3f" % c["skill_vs_freeze"] if c["skill_vs_freeze"] is not None else "-"),
               "YES" if c["clears_bar"] else ""))
