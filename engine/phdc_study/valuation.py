"""PHDC fair value — nominal EGP, FY2025 audited base, published as a RANGE.

Structure, and where each leg sits on the ground-up ladder (R-SIGCM-02):

  revenue        UNIT-adjacent. Revenue is delivery-capacity-limited, not
                 backlog-limited: the contracted book is EGP 263bn against
                 FY2025 revenue of EGP 36bn, so what binds is how fast the
                 company can build and hand over. Capacity is grown on
                 construction inflation and the backlog is rolled behind it.
  gross margin   OUTPUT, never an input — price against cost on the SAME
                 completion clock, the correction the walk-forward earned.
  cash           TOPDOWN, and flagged as such. The collection schedule (down
                 payment, instalment tenor, post-handover tail) is NOT
                 disclosed by the company, so cash conversion is measured from
                 the three years of disclosed cash-flow statements instead of
                 built from a schedule. This is the study's crux and it is
                 sensitised across its full observed range.
  interest       from the FY2025 debt schedule, facility by facility.

No point estimate is published. The walk-forward record on this name measured
a net-profit error of +1.12 log over ten origins; a single number would claim
a precision that record does not support.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)
import inputs as IN

IN.assert_balance_sheet_foots()

V = {}
for g in (IN.ACTUALS, IN.BALANCE_SHEET_FY25, IN.DEBT_FY25, IN.OPERATING, IN.MARKET):
    for k, r in g.items():
        V[k] = r["value"]
W = json.load(open(os.path.join(HERE, "wacc_result.json")))

GROSS_DEBT = sum(r["value"] for r in IN.DEBT_FY25.values())
NET_DEBT = GROSS_DEBT - V["cash"]
SHARES_MN = V["shares_outstanding_bn"] * 1000.0

GM_FY25 = V["gross_profit_fy25"] / V["revenue_fy25"]
GM_1Q26 = V["gross_profit_1q26"] / V["revenue_1q26"]
SGA_RATIO = V["sga_fy25"] / V["revenue_fy25"]

# --- the crux: cash conversion, MEASURED, not assumed -----------------------
CFO_MARGINS = {
    2023: V["cfo_fy23"] / V["revenue_fy23"],
    2024: V["cfo_fy24"] / V["revenue_fy24"],
    2025: V["cfo_fy25"] / V["revenue_fy25"],
}
CFO_LO, CFO_HI = min(CFO_MARGINS.values()), max(CFO_MARGINS.values())
CFO_MID = sum(CFO_MARGINS.values()) / len(CFO_MARGINS)

CPI3 = 0.2520          # Egypt CPI 2023-25 mean, World Bank WDI (exogenous)
HORIZON = 10
TAX = 0.225
# Backlog cannot compound without limit: the company sells ahead, but the ratio
# of contracted book to revenue has to settle. It was 3.4x at FY2023 and 5.4x at
# FY2024 and is 7.3x now, so the model converges it back to the FY2024 level.
TARGET_BACKLOG_MULT = V["backlog_fy24"] / V["revenue_fy24"]


def run(cfo_margin, capacity_growth, wacc, terminal_growth):
    cap = V["revenue_fy25"]
    backlog = V["backlog_1q26"]
    debt = GROSS_DEBT
    kd = W["kd_pretax_local"]
    rows, pv = [], 0.0
    for t in range(1, HORIZON + 1):
        cap *= (1 + capacity_growth)
        revenue = min(cap, backlog)
        # new sales are set by the convergence target, not by a free growth rate
        target_backlog = revenue * TARGET_BACKLOG_MULT
        new_sales = max(0.0, target_backlog - (backlog - revenue))
        backlog = backlog - revenue + new_sales
        gross = revenue * ((GM_FY25 + GM_1Q26) / 2)
        sga = revenue * SGA_RATIO
        interest = debt * kd
        npbt = gross - sga - interest
        tax = max(0.0, npbt) * TAX
        cfo = revenue * cfo_margin
        # FCFF = operating cash before financing, less tax already inside CFO,
        # plus the after-tax interest CFO is struck after
        fcff = cfo + interest * (1 - TAX) - revenue * 0.01     # maintenance capex
        pv += fcff / ((1 + wacc) ** t)
        rows.append({"year": 2025 + t, "revenue": revenue, "new_sales": new_sales,
                     "backlog": backlog, "gross": gross, "npbt": npbt,
                     "tax": tax, "cfo": cfo, "fcff": fcff})
    tv = rows[-1]["fcff"] * (1 + terminal_growth) / (wacc - terminal_growth)
    pv_tv = tv / ((1 + wacc) ** HORIZON)
    ev = pv + pv_tv
    equity = ev - NET_DEBT + V["investments_assoc"] + V["investment_property"]
    return {"ev": ev, "equity": equity, "per_share": equity / SHARES_MN,
            "pv_explicit": pv, "pv_terminal": pv_tv,
            "terminal_share": pv_tv / ev if ev else None, "rows": rows,
            "inputs": {"cfo_margin": cfo_margin, "capacity_growth": capacity_growth,
                       "wacc": wacc, "terminal_growth": terminal_growth}}


def main():
    wr, wc = W["wacc_rating"], W["wacc_cds"]
    cases = {
        "bear":  run(CFO_LO,  CPI3 - 0.08, wr + 0.02, 0.10),
        "base":  run(CFO_MID, CPI3,        wr,        0.12),
        "base_cds_erp": run(CFO_MID, CPI3, wc,        0.12),
        "bull":  run(CFO_HI,  CPI3 + 0.05, wc - 0.01, 0.14),
    }
    print("=" * 78)
    print("PHDC — FAIR VALUE RANGE  ·  nominal EGP  ·  FY2025 audited base")
    print("=" * 78)
    print("WACC  rating-ERP %.2f%%   CDS-ERP %.2f%%      (11-Jun-2026 edition used 18.00%%)"
          % (wr * 100, wc * 100))
    print("net debt %.0f   shares %.4fbn   spot EGP %.2f   book equity/share EGP %.2f"
          % (NET_DEBT, V["shares_outstanding_bn"], V["spot"],
             V["total_equity"] / SHARES_MN))
    print()
    print("THE CRUX — cash conversion, measured from the disclosed cash-flow statements")
    for y, m in sorted(CFO_MARGINS.items()):
        print("   FY%d  CFO / revenue = %5.1f%%" % (y, m * 100))
    print("   range used: %.1f%% (bear) / %.1f%% (base) / %.1f%% (bull)"
          % (CFO_LO * 100, CFO_MID * 100, CFO_HI * 100))
    print()
    print("%-15s %11s %11s %11s %10s %9s" %
          ("case", "EV", "equity", "per share", "terminal%", "WACC"))
    for k, r in cases.items():
        print("%-15s %11.0f %11.0f %11.2f %9.0f%% %8.2f%%" %
              (k, r["ev"], r["equity"], r["per_share"],
               100 * (r["terminal_share"] or 0), 100 * r["inputs"]["wacc"]))
    ps = sorted(r["per_share"] for r in cases.values())
    print()
    print("FAIR-VALUE RANGE  EGP %.2f – %.2f per share   (spot EGP %.2f)"
          % (ps[0], ps[-1], V["spot"]))
    json.dump({k: {kk: vv for kk, vv in r.items() if kk != "rows"} | {"rows": r["rows"]}
               for k, r in cases.items()},
              open(os.path.join(HERE, "valuation.json"), "w"), indent=1)
    print("\nBASE CASE")
    print("%6s %10s %10s %11s %10s %10s" %
          ("year", "revenue", "new sales", "backlog", "cfo", "fcff"))
    for row in cases["base"]["rows"]:
        print("%6d %10.0f %10.0f %11.0f %10.0f %10.0f" %
              (row["year"], row["revenue"], row["new_sales"], row["backlog"],
               row["cfo"], row["fcff"]))


if __name__ == "__main__":
    main()


def sensitivity():
    """The crux, priced in real observable units.

    Value here is dominated by one quantity the company does not disclose the
    mechanics of: how fast contracted sales convert to cash. The three years of
    disclosed cash-flow statements put it at 3.9%, 17.9% and 3.9% of revenue —
    a spread wide enough that it, not the discount rate, decides the answer.
    That is the finding, and this grid is the evidence for it.
    """
    wr = W["wacc_rating"]
    grid, cfos = [], [0.039, 0.060, 0.087, 0.120, 0.179]
    waccs = [wr - 0.04, wr - 0.02, wr, wr + 0.02, wr + 0.04]
    for c in cfos:
        row = []
        for w in waccs:
            row.append(run(c, CPI3, w, 0.12)["per_share"])
        grid.append((c, row))
    return waccs, grid


def print_sensitivity():
    waccs, grid = sensitivity()
    print()
    print("=" * 78)
    print("SENSITIVITY — fair value per share (EGP), spot EGP %.2f" % V["spot"])
    print("=" * 78)
    print("%-22s" % "cash conversion \\ WACC" + "".join("%10.2f%%" % (w * 100) for w in waccs))
    for c, row in grid:
        tag = ""
        if abs(c - 0.039) < 1e-9:
            tag = "  <- FY2023 and FY2025 actual"
        if abs(c - 0.179) < 1e-9:
            tag = "  <- FY2024 actual"
        if abs(c - 0.087) < 1e-9:
            tag = "  <- three-year mean"
        print("%-22s" % ("CFO/revenue %5.1f%%" % (c * 100))
              + "".join("%11.2f" % v for v in row) + tag)
    lo = min(v for _, r in grid for v in r)
    hi = max(v for _, r in grid for v in r)
    print()
    print("Across the observed range of the crux alone, value spans EGP %.2f to %.2f "
          "per share." % (lo, hi))
    print("The discount rate moves it by far less than the cash-conversion "
          "assumption does.")
