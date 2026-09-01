"""AMOC walk-forward — diagnosis.

Three jobs:

  1. Decompose the revenue and net-profit errors into their drivers (§4).
  2. Test the SPECIFICATION defect the scored record exposes — a "knowable"
     macro path that compounds domestic inflation while holding the currency and
     crude flat is not a coherent scenario, and on a pass-through refiner it
     guarantees a one-sided profit miss.
  3. Report the beta sensitivity where beta can actually bite.

ON (2), AND IT MATTERS: the PPP-consistent path below was specified AFTER the
pre-registered record existed. It is therefore a DIAGNOSTIC and carries no
weight as evidence — it is here to identify a wiring error, not to improve a
score. Under L-042, before any error is computed a change is a choice and
afterwards the identical change is tuning, so the pre-registered rule STANDS and
its result stands with it. Nothing in the delivered study rests on this run.

ON THE BETA SENSITIVITY: under the pre-registered knowable path the crude ratio
is 1.0 by construction, so beta multiplies nothing and the sensitivity is
vacuous — every beta returns an identical bias. That is a property of the
scenario, not a finding about pass-through, and reporting three identical
numbers as a sensitivity would be theatre. It is reported here on the
perfect-foresight path, where beta is the quantity it was meant to test.
"""
import os, sys, json, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import panel as P
import bottom_up as B
import score as S


def ppp_project(origin, h, beta=B.BETA_DEFAULT):
    """The internally consistent knowable path.

    Same rules as the pre-registration, one change: the currency is not assumed
    frozen while domestic prices compound. Crude is held flat in USD — nobody at
    the origin can forecast it — and the EGP is assumed to depreciate at the
    inflation rate carried forward, which is the same assumption already being
    made about domestic costs. Crude-in-EGP therefore moves with CPI.
    """
    o = P.IS[origin]
    lines_o = P.common_lines(origin)
    cost_o = P.COST_STACK[origin]
    orev_o = P.OTHER_REVENUE[origin]
    tonnes_o = P.PRODUCTS[origin]["total"][0]
    cpi = B.cpi_path(origin, h)
    br = cpi                                   # <- the only line that differs

    tonnes = tonnes_o
    net_sales = sum(t * (e / t if t else 0) * (br ** beta) for t, e in lines_o.values())
    raw = (cost_o["raw_materials"] / tonnes_o) * tonnes * (br ** beta)
    salaries = cost_o["salaries"] * cpi
    supporting = (cost_o["supporting_materials"] / tonnes_o) * tonnes * cpi
    other_cos = (cost_o["other"] / tonnes_o) * tonnes * cpi
    depreciation = cost_o["depreciation"]
    cos = raw + salaries + supporting + depreciation + other_cos
    gp = net_sales - cos
    ga = o["ga"] * cpi
    marketing = (o["marketing"] / tonnes_o) * tonnes * cpi
    op = gp - ga - marketing - o["other_expenses"]
    pbt = (op - o["claims_provision"] - o.get("finance_expenses", 0)
           + orev_o["credit_interest"] * cpi + o["investment_revenues"])
    npat = pbt - B.TAX_RATE * pbt
    nci = (o["nci"] / o["npat"] if o["npat"] else 0) * npat
    return dict(volume_t=tonnes, net_sales=net_sales, cost_of_sales=cos, gross_profit=gp,
                operating_profit=op, pbt=pbt, npat=npat, majority=npat - nci)


def decompose_revenue():
    """Revenue error into volume, mix and realisation, per cell."""
    out = []
    for o, h, t in B.cells():
        lo, lt = P.common_lines(o), P.common_lines(t)
        vol_o = sum(v[0] for v in lo.values())
        vol_t = sum(v[0] for v in lt.values())
        # realisation held at the origin's, applied to the origin's mix and volume
        r_o = {k: (v[1] / v[0] if v[0] else 0) for k, v in lo.items()}
        r_t = {k: (v[1] / v[0] if v[0] else 0) for k, v in lt.items()}
        share_o = {k: (v[0] / vol_o) for k, v in lo.items()}
        share_t = {k: (v[0] / vol_t) for k, v in lt.items()}
        base = sum(vol_o * share_o[k] * r_o[k] for k in lo)
        step_vol = sum(vol_t * share_o[k] * r_o[k] for k in lo)
        step_mix = sum(vol_t * share_t[k] * r_o[k] for k in lo)
        actual = sum(vol_t * share_t[k] * r_t[k] for k in lo)
        out.append({"origin": o, "h": h, "target": t,
                    "volume_effect": math.log(step_vol / base),
                    "mix_effect": math.log(step_mix / step_vol),
                    "realisation_effect": math.log(actual / step_mix),
                    "total": math.log(actual / base)})
    return out


def main():
    rows = S.build_cells()
    res = {}

    # --- 1. decompositions
    res["revenue_decomposition"] = decompose_revenue()
    rd = res["revenue_decomposition"]
    res["revenue_decomposition_mean"] = {
        k: sum(r[k] for r in rd) / len(rd)
        for k in ("volume_effect", "mix_effect", "realisation_effect", "total")}

    # --- 2. the specification test
    keys = ["net_sales", "cost_of_sales", "gross_profit", "pbt", "majority"]
    comp = {k: {"prereg": [], "ppp": [], "foresight": []} for k in keys}
    for o, h, t in B.cells():
        a = B.actual(t)
        pre = B.project(o, h)
        ppp = ppp_project(o, h)
        fore = B.project(o, h, foresight=True)
        for k in keys:
            comp[k]["prereg"].append(S.logerr(pre[k], a[k]))
            comp[k]["ppp"].append(S.logerr(ppp[k], a[k]))
            comp[k]["foresight"].append(S.logerr(fore[k], a[k]))
    spec = {}
    for k in keys:
        spec[k] = {}
        for basis in ("prereg", "ppp", "foresight"):
            v = [x for x in comp[k][basis] if x is not None]
            spec[k][basis] = {"n": len(v), "bias": sum(v) / len(v),
                              "mae": sum(abs(x) for x in v) / len(v),
                              "share_over": sum(1 for x in v if x > 0) / len(v)}
    res["specification_test"] = spec

    # skill of each basis against freeze, on majority profit
    fr = [S.logerr(B.freeze(o, h)["majority"], B.actual(t)["majority"]) for o, h, t in B.cells()]
    fr = [x for x in fr if x is not None]
    mae_fr = sum(abs(x) for x in fr) / len(fr)
    res["skill_vs_freeze_majority"] = {
        basis: 1.0 - spec["majority"][basis]["mae"] / mae_fr
        for basis in ("prereg", "ppp", "foresight")}
    res["mae_freeze_majority"] = mae_fr

    # --- 3. beta sensitivity where beta bites
    bs = {}
    for beta in (0.8, 1.0, 1.2):
        r2 = S.build_cells(beta=beta, foresight=True)
        bs["beta_%.1f" % beta] = {d: S.agg(r2, "e", d) for d in keys}
    res["beta_sensitivity_on_foresight"] = bs
    res["beta_note"] = ("Under the pre-registered knowable path the crude ratio is 1.0, so beta "
                        "multiplies nothing and all three values are identical. Reported here on "
                        "perfect foresight, where beta is the quantity it was meant to test.")

    json.dump(res, open(os.path.join(HERE, "diagnostics.json"), "w"), indent=1, default=str)
    return res


def pct(x):
    return "%+.1f%%" % ((math.exp(x) - 1) * 100)


if __name__ == "__main__":
    r = main()
    m = r["revenue_decomposition_mean"]
    print("REVENUE ERROR DECOMPOSITION (mean log effect over 9 cells)")
    print("  volume       %s" % pct(m["volume_effect"]))
    print("  mix          %s" % pct(m["mix_effect"]))
    print("  realisation  %s" % pct(m["realisation_effect"]))
    print("  total        %s\n" % pct(m["total"]))

    print("SPECIFICATION TEST — same rules, three macro scenarios")
    print("%-16s %-28s %-28s %-28s" % ("", "pre-registered (FX frozen)", "PPP-consistent (diagnostic)",
                                       "perfect foresight"))
    for k in ("net_sales", "cost_of_sales", "gross_profit", "pbt", "majority"):
        s = r["specification_test"][k]
        cells = []
        for b in ("prereg", "ppp", "foresight"):
            cells.append("bias %8s MAE %7s" % (pct(s[b]["bias"]), pct(s[b]["mae"])))
        print("%-16s %-28s %-28s %-28s" % (k, cells[0], cells[1], cells[2]))
    print("\nSKILL vs FREEZE on majority profit (positive = better than 'no change'):")
    for b, v in r["skill_vs_freeze_majority"].items():
        print("  %-10s %+.3f" % (b, v))
    print("\nBETA SENSITIVITY on the perfect-foresight path (bias):")
    for b, v in r["beta_sensitivity_on_foresight"].items():
        print("  %-9s sales %8s  cost %8s  gross %8s  majority %8s"
              % (b, pct(v["net_sales"]["bias"]), pct(v["cost_of_sales"]["bias"]),
                 pct(v["gross_profit"]["bias"]), pct(v["majority"]["bias"])))
