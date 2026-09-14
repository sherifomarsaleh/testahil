#!/usr/bin/env python3
"""PHAR — decomposition, one-offs, the per-origin income statements, and the
error cells in the shared instrument's own shape.

Writes error_cells.json (read by engine/valuation_calibration/boundary_sensitivity.py
and by scripts/check_correction_boundary.py through a named adapter),
diagnostics.json, and phar_IS_projected_vs_actual_all_origins.md.
"""
from __future__ import annotations
import json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import panel, bottom_up as bu, score  # noqa: E402


def error_cells():
    rows = []
    for leg, tag in (("baseline", "asknown"), ("foresight", "foresight"),
                     ("knowable", "knowable")):
        for r in score.cells(leg):
            rows.append(dict(driver=r["driver"], origin=r["origin"], year=r["target"],
                             horizon=r["horizon"], log_error=r["e"], setting=tag,
                             forecast=r["forecast"], actual=r["actual"]))
    return rows


def decompose():
    """Revenue and net-profit errors, taken apart into the drivers that make them.

    Revenue = units x price x the consolidation ratio, so ln(err_revenue) is the
    SUM of the three log errors exactly — an identity, not a regression, and the
    residual is printed so a reader can see it is zero.
    """
    out = {"revenue": [], "net_profit": []}
    for o in bu.ORIGINS:
        p = bu.project(o)
        for h in bu.HORIZONS:
            y = bu.fy(bu.yr(o) + h)
            if y not in panel.IS or "units_th" not in p.get(y, {}):
                continue
            a = bu.actual(y)
            eu = math.log(p[y]["units_th"] / a["units_th"])
            ep = math.log(p[y]["price_per_pack"] / a["price_per_pack"])
            er = math.log(p[y]["revenue"] / a["revenue"])
            out["revenue"].append(dict(origin=o, horizon=h, target=y, e_revenue=er,
                                       e_units=eu, e_price=ep,
                                       residual_consolidation=er - eu - ep))
        for h in bu.HORIZONS:
            y = bu.fy(bu.yr(o) + h)
            if y not in panel.IS:
                continue
            a, f = bu.actual(y), p.get(y)
            if not f:
                continue
            out["net_profit"].append(dict(
                origin=o, horizon=h, target=y,
                e_net_profit=math.log(f["net_profit"] / a["net_profit"]),
                e_gross_profit=math.log(f["gross_profit"] / a["gross_profit"]),
                e_expenses=math.log(f["expenses_total"] / a["expenses_total"]),
                e_other=math.log(f["other_block"] / a["other_block"]),
                below_the_line_actual=panel.IS[y]["below_line"],
                below_the_line_forecast=0.0,
                below_the_line_share_of_actual_pbt=panel.IS[y]["below_line"] / panel.IS[y]["pbt"]))
    return out


ONE_OFFS = [
    dict(year="FY2022", item="foreign-exchange result", value=286404665,
         share_of_pbt=0.356, classification="MACRO, NOT COMPANY",
         why="the March, May and October 2022 devaluations revaluing the company's own "
             "foreign-currency balances. The mechanical rule sets it to zero at every origin "
             "(R11), so its whole size is carried in the measured net-profit error rather "
             "than hidden by a driver that quietly forecasts a currency view."),
    dict(year="FY2023", item="foreign-exchange result", value=139625936, share_of_pbt=0.129,
         classification="MACRO, NOT COMPANY", why="the January 2023 devaluation, same treatment."),
    dict(year="FY2024", item="foreign-exchange result", value=699879896, share_of_pbt=0.457,
         classification="MACRO, NOT COMPANY",
         why="the March 2024 float. NEARLY HALF OF THAT YEAR'S PROFIT BEFORE TAX is a "
             "currency revaluation, which is the single largest reason the net-profit error "
             "is bigger than the gross-profit error at every origin."),
    dict(year="FY2025", item="share of associates", value=495499218, share_of_pbt=0.276,
         classification="COMPANY, RECURRING BUT STEP-CHANGED",
         why="the associates line went 74.5mn (FY2023) -> 151.6mn (FY2024) -> 495.5mn "
             "(FY2025), a 3.3x step in one year on stakes the company was adding to "
             "throughout. The mechanical rule holds the block at its trailing mean share of "
             "revenue and cannot see a step; this is a real driver miss and is scored as one."),
    dict(year="FY2020", item="the condensed COVID-year report", value=None, share_of_pbt=None,
         classification="DISCLOSURE, NOT EARNINGS",
         why="not a one-off in the accounts but a one-off in the ARCHIVE: the FY2020 edition "
             "publishes no packs figure, no consolidated depreciation and no consolidated "
             "capex. It is classified here because it is the reason one of five origins runs "
             "on a coarser driver set, and a reader of the error table needs to know that."),
    dict(year="FY2025", item="the actuarial reserve", value=-328929846, share_of_pbt=-0.183,
         classification="COMPANY, BELOW THE LINE",
         why="a 328.9mn actuarial loss on employee-benefit schemes taken through other "
             "comprehensive income, first appearing in FY2025. It does not touch profit and "
             "so does not touch any error cell; it is recorded because it moves equity and "
             "would move a book-value lens."),
]


def statements_md():
    L = ["# PHAR — projected versus actual income statement, EVERY origin",
         "",
         "**INTERNAL.** The training record, the panel and these tables are never shown to a",
         "reader [R-FCAL-01].",
         "",
         "Consolidated, EGP millions, as first reported. `proj` is the mechanical build of",
         "`bottom_up.py` at that origin under the rules fixed in",
         "`PRE_REGISTRATION_07-09-2026.md`; `act` is what EIPICO reported.",
         "",
         "Below-the-line items — capital gains, the foreign-exchange result and other income —",
         "are SET TO ZERO by rule R11 at every origin, so `proj` profit before tax is",
         "structurally short of `act` in every year the pound moved. That is the rule working,",
         "not a defect: a mechanical rule that forecast a currency result would be scoring a",
         "currency view rather than a driver model.",
         ""]
    M = 1e6
    for o in bu.ORIGINS:
        p = bu.project(o)
        L += ["## Origin %s (trailing window k=%d accounting, k=%d KPI)"
              % (o, bu.k_at(o), bu.k_at(o, "kpi")), ""]
        ys = [bu.fy(bu.yr(o) + h) for h in bu.HORIZONS if bu.fy(bu.yr(o) + h) in panel.IS]
        L.append("| line | " + " | ".join("%s proj | %s act | err" % (y, y) for y in ys) + " |")
        L.append("|---|" + "---|" * (3 * len(ys)))
        for f, lab in (("revenue", "Revenue"), ("cogs", "Cost of sales"),
                       ("gross_profit", "Gross profit"),
                       ("expenses_total", "Charges below gross profit"),
                       ("other_block", "Associates and interest income"),
                       ("pbt", "Profit before tax"), ("net_profit", "Net profit")):
            cs = []
            for y in ys:
                a = bu.actual(y).get(f)
                v = p[y].get(f)
                e = math.log(v / a) if (a and v and a > 0 and v > 0) else None
                cs += ["%.0f" % (v / M) if v else "—", "%.0f" % (a / M) if a else "—",
                       "%+.3f" % e if e is not None else "—"]
            L.append("| %s | %s |" % (lab, " | ".join(cs)))
        blt = " · ".join("%s %+.0f" % (y, panel.IS[y]["below_line"] / M) for y in ys)
        L += ["", "*Below the line, set to zero by rule and reported here: %s (EGP mn).*" % blt, ""]
    return "\n".join(L)


if __name__ == "__main__":
    panel.assert_all()
    ec = error_cells()
    json.dump(ec, open(os.path.join(HERE, "error_cells.json"), "w"), indent=1)
    dec = decompose()
    d = dict(_="PHAR walk-forward diagnostics. GENERATED by diagnose.py; never hand-edited.",
             run="PHAR", decomposition=dec, one_offs=ONE_OFFS,
             n_error_cells=len(ec))
    json.dump(d, open(os.path.join(HERE, "diagnostics.json"), "w"), indent=1)
    open(os.path.join(HERE, "phar_IS_projected_vs_actual_all_origins.md"), "w").write(statements_md())
    r = dec["revenue"]
    print("error cells written: %d (three legs)" % len(ec))
    print("\nrevenue error taken apart (identity: e_rev = e_units + e_price + e_consolidation):")
    print("  mean e_revenue %+.3f = e_units %+.3f + e_price %+.3f + residual %+.4f"
          % (sum(x["e_revenue"] for x in r) / len(r),
             sum(x["e_units"] for x in r) / len(r),
             sum(x["e_price"] for x in r) / len(r),
             sum(x["residual_consolidation"] for x in r) / len(r)))
    n = dec["net_profit"]
    print("\nnet-profit error, and the line the rule sets to zero:")
    print("  mean e_net_profit %+.3f  e_gross_profit %+.3f  e_expenses %+.3f  e_other %+.3f"
          % (sum(x["e_net_profit"] for x in n) / len(n),
             sum(x["e_gross_profit"] for x in n) / len(n),
             sum(x["e_expenses"] for x in n) / len(n),
             sum(x["e_other"] for x in n) / len(n)))
    print("  below-the-line as a share of ACTUAL profit before tax, mean %.1f%%, max %.1f%%"
          % (100 * sum(x["below_the_line_share_of_actual_pbt"] for x in n) / len(n),
             100 * max(x["below_the_line_share_of_actual_pbt"] for x in n)))
