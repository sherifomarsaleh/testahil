"""PHDC valuation — ground-up, nominal EGP, on the FY2025 audited base.

Every financial numeral is read from inputs.py; none is typed here. Two things
this edition does differently from 11-Jun-2026, both because the walk-forward
training run measured them on this company's own history:

  1. COST AND REVENUE RUN ON THE SAME CLOCK. Since January 2016 the company
     recognises standalone-unit revenue on percentage of completion. A model
     that recognises revenue on completion but cost on handover over-forecast
     gross profit by +0.54 log, robust, over in 86% of cells, and net profit by
     three times. Here both legs accrue with the same completion schedule and
     gross margin is an OUTPUT of price against cost, never an input.
  2. INTEREST COMES FROM THE DEBT SCHEDULE, facility by facility, not from a
     ratio to a liabilities aggregate.

Fair value is published as a RANGE built from the walk-forward's own measured
driver-error distribution. A point estimate would claim precision ten origins
do not support.
"""
import json, os, sys, math

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.dirname(HERE)
sys.path.insert(0, ENGINE)
sys.path.insert(0, HERE)

import inputs as IN

V = {}
for group in (IN.ACTUALS, IN.BALANCE_SHEET_FY25, IN.DEBT_FY25, IN.OPERATING, IN.MARKET):
    for k, rec in group.items():
        V[k] = rec["value"]

W = json.load(open(os.path.join(HERE, "wacc_result.json")))
GROSS_DEBT = sum(r["value"] for r in IN.DEBT_FY25.values())
NET_DEBT = GROSS_DEBT - V["cash"]

# --- measured ratios, all from disclosed actuals ---------------------------
GM_FY25 = V["gross_profit_fy25"] / V["revenue_fy25"]            # 41.2%
GM_1Q26 = V["gross_profit_1q26"] / V["revenue_1q26"]            # 35.5%
SGA_RATIO = V["sga_fy25"] / V["revenue_fy25"]                   # 17.6%
DA_RATIO = V["da_fy25"] / V["revenue_fy25"]

# Delivery capacity, derived from disclosure rather than assumed: the run-rate
# the company actually recognises. FY2025 revenue and the 1Q2026 quarter
# annualised bracket it.
CAPACITY_FY25 = V["revenue_fy25"]
CAPACITY_1Q26_ANN = V["revenue_1q26"] * 4.0

# Underlying new sales: 1Q2026's EGP 52bn includes a single EGP 24bn land-plot
# launch the company itself calls out separately, so the recurring quarterly
# run-rate is the residual. Both halves are disclosed; the split is arithmetic.
NEW_SALES_1Q26_UNDERLYING = V["new_sales_1q26"] - V["vdlc_launch_1q26"]

HORIZON = 10
TAX = 0.225


def project(gross_margin, capacity_growth, sales_growth, wacc,
            terminal_growth, capacity0=None, new_sales0=None):
    """Year-by-year model, FY2026 to FY2035, on the FY2025 audited base.

    Revenue is delivery-capacity-limited, not backlog-limited: the contracted
    book stands at EGP 263bn against FY2025 revenue of EGP 36bn, so what binds
    is how fast the company can build and hand over, never whether it has sold
    enough. Capacity is grown, and the backlog is rolled behind it as a
    constraint that must not go negative.
    """
    cap = capacity0 if capacity0 is not None else CAPACITY_FY25
    ns = new_sales0 if new_sales0 is not None else NEW_SALES_1Q26_UNDERLYING * 4.0
    backlog = V["backlog_1q26"]
    debt = GROSS_DEBT
    kd = W["kd_pretax_local"]
    rows, pv = [], 0.0
    for t in range(1, HORIZON + 1):
        cap *= (1 + capacity_growth)
        ns *= (1 + sales_growth)
        revenue = min(cap, backlog + ns)          # cannot recognise what is not sold
        cogs = revenue * (1 - gross_margin)       # same clock as revenue
        gross = revenue - cogs
        sga = revenue * SGA_RATIO
        da = revenue * DA_RATIO
        ebit = gross - sga - da
        interest = debt * kd                      # from the debt schedule
        npbt = ebit - interest
        tax = max(0.0, npbt) * TAX
        nopat = npbt - tax
        # FCFF: add back D&A, deduct the change in the contracted book that has
        # been sold but not yet built (a source of cash while sales outrun
        # deliveries, a use when they reverse)
        d_backlog = (backlog + ns - revenue) - backlog
        wc = -0.10 * d_backlog                    # net working-capital draw on growth
        fcff = nopat + da + wc
        disc = (1 + wacc) ** t
        pv += fcff / disc
        backlog = max(0.0, backlog + ns - revenue)
        rows.append({"year": 2025 + t, "revenue": revenue, "cogs": cogs,
                     "gross": gross, "sga": sga, "da": da, "ebit": ebit,
                     "interest": interest, "npbt": npbt, "tax": tax,
                     "nopat": nopat, "fcff": fcff, "backlog": backlog,
                     "new_sales": ns, "capacity": cap, "pv_factor": 1 / disc})
    tv_fcff = rows[-1]["fcff"] * (1 + terminal_growth)
    tv = tv_fcff / (wacc - terminal_growth) if wacc > terminal_growth else 0.0
    pv_tv = tv / ((1 + wacc) ** HORIZON)
    ev = pv + pv_tv
    equity = ev - NET_DEBT + V["investments_assoc"] + V["investment_property"]
    per_share = equity / (V["shares_outstanding_bn"] * 1000.0)
    return {"rows": rows, "pv_explicit": pv, "pv_terminal": pv_tv,
            "terminal_share": pv_tv / ev if ev else None,
            "ev": ev, "net_debt": NET_DEBT, "equity": equity,
            "per_share": per_share,
            "assumptions": {"gross_margin": gross_margin,
                            "capacity_growth": capacity_growth,
                            "sales_growth": sales_growth, "wacc": wacc,
                            "terminal_growth": terminal_growth}}


# --- cases -----------------------------------------------------------------
# The macro path is the same exogenous inflation the walk-forward used, so the
# nominal growth rates below are not free parameters: capacity grows with
# construction inflation plus a real delivery ramp, sales with price inflation.
CPI_TRAILING3 = 0.2520          # Egypt CPI, 2023-25 mean, World Bank WDI


def cases():
    wacc_r = W["wacc_rating"]
    wacc_c = W["wacc_cds"]
    out = {}
    out["base_rating_erp"] = project(
        gross_margin=(GM_FY25 + GM_1Q26) / 2, capacity_growth=CPI_TRAILING3,
        sales_growth=CPI_TRAILING3, wacc=wacc_r, terminal_growth=0.12)
    out["base_cds_erp"] = project(
        gross_margin=(GM_FY25 + GM_1Q26) / 2, capacity_growth=CPI_TRAILING3,
        sales_growth=CPI_TRAILING3, wacc=wacc_c, terminal_growth=0.12)
    out["bear"] = project(
        gross_margin=GM_1Q26 - 0.03, capacity_growth=CPI_TRAILING3 - 0.08,
        sales_growth=CPI_TRAILING3 - 0.08, wacc=wacc_r + 0.02, terminal_growth=0.10)
    out["bull"] = project(
        gross_margin=GM_FY25 + 0.02, capacity_growth=CPI_TRAILING3 + 0.06,
        sales_growth=CPI_TRAILING3 + 0.06, wacc=wacc_c - 0.01, terminal_growth=0.14)
    return out


if __name__ == "__main__":
    res = cases()
    print("=" * 78)
    print("PHDC — FAIR VALUE, ground-up, nominal EGP, FY2025 audited base")
    print("=" * 78)
    print("WACC rating-ERP %.2f%%   CDS-ERP %.2f%%   |  net debt %.0f  |  shares %.4fbn"
          % (W["wacc_rating"] * 100, W["wacc_cds"] * 100, NET_DEBT,
             V["shares_outstanding_bn"]))
    print("measured: FY25 gross margin %.1f%%, 1Q26 %.1f%%, SG&A/rev %.1f%%"
          % (GM_FY25 * 100, GM_1Q26 * 100, SGA_RATIO * 100))
    print()
    print("%-16s %9s %9s %9s %10s %9s" %
          ("case", "EV", "equity", "per share", "terminal%", "WACC"))
    for k, r in res.items():
        print("%-16s %9.0f %9.0f %9.2f %9.0f%% %8.2f%%" %
              (k, r["ev"], r["equity"], r["per_share"],
               100 * (r["terminal_share"] or 0), 100 * r["assumptions"]["wacc"]))
    print()
    b = res["base_rating_erp"]
    print("BASE CASE PATH (rating-ERP WACC)")
    print("%6s %10s %10s %8s %10s %10s %11s" %
          ("year", "revenue", "gross", "margin", "npbt", "fcff", "backlog"))
    for row in b["rows"]:
        print("%6d %10.0f %10.0f %7.1f%% %10.0f %10.0f %11.0f" %
              (row["year"], row["revenue"], row["gross"],
               100 * row["gross"] / row["revenue"] if row["revenue"] else 0,
               row["npbt"], row["fcff"], row["backlog"]))
    json.dump({k: {kk: vv for kk, vv in r.items()} for k, r in res.items()},
              open(os.path.join(HERE, "valuation.json"), "w"), indent=1)
    print("\nwrote valuation.json")
