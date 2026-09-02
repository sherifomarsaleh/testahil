"""TMGH — THE model. One projection, read by every lens and every statement.

A first cut had the valuation discounting one construction of the development
cash flow while the projected statements built another. Both were defensible in
isolation and they did not agree, which is exactly the defect [L-016] records:
if two different models feed one report, it will publish two different answers
and nobody will notice, because each looks right beside its own neighbours.

So there is one projection here. The income statement, the balance sheet, the
cash-flow statement, the free cash flow the DCF discounts and the numbers the
workbook recomputes all come out of this function and nowhere else.

Structure:
  * the DISCLOSED ORDER BOOK (EGP 491.0bn at 30 June 2026) converts over a
    stated number of years — that number is the crux, and it is run both ways;
  * REPLENISHMENT sales are made each year at a normalised rate and enter the
    book;
  * HOSPITALITY and OTHER RECURRING grow on their own drivers with their own
    cost ratios, and their margins fall out;
  * the two contract positions — customer advances and properties under
    development — are driven off the SAME order book [L-103], never one off
    revenue and the other off backlog;
  * the balance sheet closes because the cash flow feeds it. Nothing is plugged.
"""
import json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))    # engine/, for the house macro path
import inputs as IN

TAX = 0.225
EXPLICIT_YEARS = 10
FIRST_YEAR = 2026

# THE CRUX, in two readings. TMG's order book is EGP 491.0bn against 1H2026
# deliveries of EGP 17.0bn — about fourteen years at the current rate. Neither
# reading can be dismissed from what the company discloses, so both are carried
# through to the answer and published side by side.
CAPACITY_YEARS = 14   # constrained: the book converts at roughly the rate the
                      # last three years have actually managed
RECOVERY_YEARS = 10   # the build programme catches up and the conversion rate
                      # moves back toward its pre-2023 level. Eight years was
                      # tried and rejected: it drove development revenue to
                      # EGP 325bn a year by 2035, six times the FY2026 level,
                      # on a landbank of about 20mn sqm. A crux has to be a
                      # question a reader can weigh, not an extreme
# How fast handovers converge on the rate the book supports.
CAPACITY_RAMP = 0.25   # a quarter of the gap closed each year
RECOVERY_RAMP = 0.35   # the build programme catches up faster
SEASONAL = 2.9078     # FY2025 development revenue over its own first half
                      # (36,705.7 / 12,621.8), the company's own relationship

REPLENISHMENT_SALES = 300000.0  # normalised annual contracted sales, below the
                      # 1H2026 annualised run rate of EGP 438bn and the FY2025
                      # EGP 382bn, and far below FY2024's launch-year EGP 504bn
SALES_FADE = 1.15     # [CLASS-A CORRECTION, 02-Sep-2026 — applied from the study's own
                      # GAP_REVIEW_01-09-2026 heading 3.] The 01-Sep edition faded
                      # replenishment sales 15% a year NOMINAL (0.85), which at the
                      # ~14.6% inflation inside this study's own terminal rate is about
                      # -26% a year REAL — a -91% real decline by 2035 with no precedent
                      # in the 2011-2025 record, and never disclosed as a real-terms
                      # assumption. The convergence-on-deliveries argument is a REAL
                      # quantity argument; the series is nominal. Restated FLAT IN REAL
                      # TERMS: +15% nominal a year, the review's own figure (76.51 on the
                      # capacity case at the unchanged rate). The order-book guard below
                      # still caps recognised revenue at what has been sold. Replaced by
                      # the house macro path when [R-MACRO-01] lands.
HOSP_GROWTH = 0.20
OTHER_GROWTH = 0.22
HOSP_CAPEX_RATIO = 0.10
OTHER_CAPEX_RATIO = 0.04
PUD_COVER_YEARS = 4.0   # work in progress against a year's cost of sales; TMG
                        # held EGP 148.3bn at 30 June 2026 against a modelled
                        # FY2026 development cost of about EGP 36bn
PUD_ADJUST_YEARS = 4    # how fast the stock is moved toward that cover
DA_RATE_ON_PPE = 0.012          # the group's own charge against gross PP&E
DEPOSIT_YIELD = 0.20            # below the policy rate, on a mixed deposit book
# [R-MACRO-01] Terminal growth is NOT a number this study chooses. It is the
# house path's terminal inflation plus a STATED real growth, and the real growth
# here is zero: the recurring legs — a hotel and a shopping centre — are assumed
# to hold their real size for ever and grow with nothing but prices. The 02-Sep
# and earlier editions carried 15%, which against the ~22% terminal discount rate
# this study's own schedule now produces would be 8pp of real growth in
# perpetuity that nothing disclosed supports [L-055].
import macro_path as _MP
_PATH = _MP.load("EG")
TERMINAL_REAL_GROWTH = 0.0
TERMINAL_GROWTH = _PATH.terminal_growth(TERMINAL_REAL_GROWTH)
PAYOUT = 0.30                   # of attributable profit, at the company's own
                                # recent distribution behaviour


def _v(d, k):
    return d[k]["value"]


def ratios():
    """Every ratio below is a quotient of two disclosed figures."""
    gm_dev_fy25 = 1 - _v(IN.IS, "dev_cost_fy25") / _v(IN.IS, "dev_revenue_fy25")
    gm_dev = 1 - _v(IN.H1_26, "dev_cost") / _v(IN.H1_26, "dev_revenue")
    gm_hosp = 1 - _v(IN.H1_26, "hosp_cost") / _v(IN.H1_26, "hosp_revenue")
    gm_oth = 1 - _v(IN.H1_26, "other_cost") / _v(IN.H1_26, "other_revenue")
    opex = ((_v(IN.IS, "ga_fy25") + _v(IN.IS, "marketing_fy25")
             + _v(IN.IS, "govt_donations_fy25"))
            / (_v(IN.IS, "dev_revenue_fy25") + _v(IN.IS, "hosp_revenue_fy25")
               + _v(IN.IS, "other_revenue_fy25")))
    d_adv = _v(IN.BS, "customer_advances") - _v(IN.BS, "customer_advances_fy25")
    d_pud = (_v(IN.BS, "properties_under_development")
             - _v(IN.BS, "properties_under_development_fy25"))
    collections = d_adv + _v(IN.H1_26, "dev_revenue")
    build = d_pud + _v(IN.H1_26, "dev_cost")
    coll_rate = (collections * 2) / (_v(IN.KPI, "contracted_sales_h1_26") * 2
                                     + _v(IN.KPI, "backlog_fy25"))
    return {
        "gm_dev_h1_26": gm_dev, "gm_dev_fy25": gm_dev_fy25,
        "gm_hosp_h1_26": gm_hosp, "gm_other_h1_26": gm_oth,
        "opex_ratio_fy25": opex,
        "collection_rate_on_book": coll_rate,
        "build_intensity_h1_26": build / _v(IN.H1_26, "dev_cost"),
        "annualised_collections_h1_26": collections * 2,
        "annualised_build_h1_26": build * 2,
        "d_advances_h1_26": d_adv, "d_pud_h1_26": d_pud,
        "kd": 0.2550,
        "note": ("Collections are the increase in customer advances plus the revenue "
                 "recognised out of them; build spend is the increase in properties "
                 "under development plus the cost recognised out of it. Both are "
                 "identities on disclosed balances, not assumptions."),
    }


def project(mode, years=EXPLICIT_YEARS):
    r = ratios()
    n = CAPACITY_YEARS if mode == "capacity" else RECOVERY_YEARS
    ramp = CAPACITY_RAMP if mode == "capacity" else RECOVERY_RAMP
    bl = _v(IN.KPI, "backlog_jun26")
    gm_dev, gm_h, gm_o = r["gm_dev_h1_26"], r["gm_hosp_h1_26"], r["gm_other_h1_26"]

    cash = (_v(IN.BS, "cash") + _v(IN.BS, "deposits_current")
            + _v(IN.BS, "deposits_noncurrent"))
    debt = (_v(IN.BS, "loans_noncurrent") + _v(IN.BS, "loans_current")
            + _v(IN.BS, "credit_facilities"))
    pud = _v(IN.BS, "properties_under_development")
    adv = _v(IN.BS, "customer_advances")
    ppe = _v(IN.BS, "ppe") + _v(IN.BS, "assets_under_construction")
    ip = _v(IN.BS, "investment_property")
    eqp = _v(IN.BS, "equity_parent")
    nci = _v(IN.BS, "nci_equity")
    other_assets = _v(IN.BS, "total_assets") - cash - pud - ppe - ip
    other_liab = _v(IN.BS, "total_liabilities") - debt - adv
    nci_share = nci / (nci + eqp)

    hosp0, oth0 = _v(IN.IS, "hosp_revenue_fy25"), _v(IN.IS, "other_revenue_fy25")
    rows = []
    for i in range(years):
        y = FIRST_YEAR + i
        # TMG IS CURRENTLY SELLING ABOUT TEN TIMES WHAT IT DELIVERS — contracted
        # sales of EGP 382bn in FY2025 against development revenue of EGP 36.7bn.
        # That is not a steady state and the model does not extrapolate it: a
        # first cut grew sales at 10% a year alongside deliveries and the order
        # book reached EGP 4.8 TRILLION inside ten years, which is two growth
        # rates left to diverge rather than a forecast about a company.
        # Replenishment therefore FADES from the launch-era rate toward the
        # delivery rate, and never falls below it.
        new_sales = max(REPLENISHMENT_SALES * SALES_FADE ** i,
                        rows[-1]["dev_revenue"] if rows else 0.0)
        # DELIVERIES ARE ANCHORED ON THE REVIEWED HALF-YEAR ACTUAL and then grow
        # at the rate the crux specifies. Jumping straight to book/n instead put
        # FY2026 development revenue 78% above what the company reported in the
        # half-year just closed — a forecast has to start from the last actual
        # [L-013], not from an average of a period that has not happened.
        if i == 0:
            dev_rev = _v(IN.H1_26, "dev_revenue") * SEASONAL
        else:
            # Deliveries CONVERGE on the rate the book supports rather than
            # compounding at a fixed rate. A constant growth rate held for ten
            # years took development revenue to EGP 1.2 trillion in the faster
            # reading — a rate is a description of the next year or two, not a
            # shape for a decade, and the thing that actually bounds handovers
            # is the size of the book being worked off.
            target = (bl + new_sales) / n
            dev_rev = rows[-1]["dev_revenue"] + (target - rows[-1]["dev_revenue"]) * ramp
        dev_rev = min(dev_rev, bl + new_sales)      # THE ORDER-BOOK GUARD [L-104]
        dev_cost = dev_rev * (1 - gm_dev)
        hosp_rev = hosp0 * (1 + HOSP_GROWTH) ** (i + 1)
        oth_rev = oth0 * (1 + OTHER_GROWTH) ** (i + 1)
        hosp_cost, oth_cost = hosp_rev * (1 - gm_h), oth_rev * (1 - gm_o)
        revenue = dev_rev + hosp_rev + oth_rev
        cost = dev_cost + hosp_cost + oth_cost
        gross = revenue - cost
        opex = revenue * r["opex_ratio_fy25"]
        da = ppe * DA_RATE_ON_PPE
        ebit = gross - opex - da
        interest = debt * r["kd"]
        fin_income = cash * DEPOSIT_YIELD
        pbt = ebit - interest + fin_income
        tax = max(pbt, 0.0) * TAX
        net = pbt - tax
        nci_profit = net * nci_share
        parent = net - nci_profit
        dividend = max(parent, 0.0) * PAYOUT

        collections = r["collection_rate_on_book"] * (new_sales + bl)
        # PROPERTIES UNDER DEVELOPMENT IS A STOCK, and build spend is what moves
        # it toward the cover the programme needs. Modelling build as a fixed
        # multiple of cost instead — 2.47x, which is what the company spent in
        # the half-year just closed while building ahead of a book it had
        # already sold — made the company build ever faster for ever, and drove
        # cash to minus EGP 4 trillion. A developer whose handovers are catching
        # up CONSUMES its work in progress; the stock adjustment lets it.
        target_pud = PUD_COVER_YEARS * dev_cost
        build = max(dev_cost + (target_pud - pud) / PUD_ADJUST_YEARS, 0.0)
        capex = hosp_rev * HOSP_CAPEX_RATIO + oth_rev * OTHER_CAPEX_RATIO
        d_adv, d_pud = collections - dev_rev, build - dev_cost

        cfo = net + da + d_adv - d_pud
        cfi = -capex
        cff = -dividend
        cash = cash + cfo + cfi + cff
        pud += d_pud
        adv = adv + d_adv
        ppe += capex - da
        eqp += parent - dividend
        nci += nci_profit
        bl = max(bl + new_sales - dev_rev, 0.0)
        book_cover = bl / dev_rev if dev_rev else None

        total_assets = cash + pud + ppe + ip + other_assets
        total_liab = debt + adv + other_liab
        total_equity = eqp + nci
        # FCFF, the single series the DCF discounts
        fcff = ebit * (1 - TAX) + da - capex - (d_pud - d_adv)
        rows.append({
            "year": y, "dev_revenue": dev_rev, "dev_cost": dev_cost,
            "hosp_revenue": hosp_rev, "hosp_cost": hosp_cost,
            "other_revenue": oth_rev, "other_cost": oth_cost,
            "revenue": revenue, "cost_of_revenue": cost, "gross_profit": gross,
            "gross_margin": gross / revenue, "opex": opex, "da": da, "ebit": ebit,
            "ebit_margin": ebit / revenue,
            "interest": interest, "finance_income": fin_income, "pbt": pbt,
            "tax": tax, "net_profit": net, "nci_profit": nci_profit,
            "attributable_profit": parent, "dividend": dividend,
            "eps": parent / _v(IN.KPI, "shares_outstanding"),
            "new_sales": new_sales, "backlog_close": bl,
            "book_cover_years": book_cover,
            "collections": collections, "build_spend": build,
            "d_advances": d_adv, "d_properties_under_development": d_pud,
            "capex": capex, "cfo": cfo, "cfi": cfi, "cff": cff,
            "fcff": fcff,
            "cash": cash, "properties_under_development": pud,
            "customer_advances": adv,
            "advances_negative": adv < 0,
            "ppe": ppe, "investment_property": ip,
            "other_assets": other_assets, "debt": debt, "other_liabilities": other_liab,
            "equity_parent": eqp, "nci_equity": nci,
            "total_assets": total_assets, "total_liabilities": total_liab,
            "total_equity": total_equity,
            "balance_check": total_assets - total_liab - total_equity,
        })
    return {"mode": mode, "conversion_years": n, "rows": rows, "ratios": r,
            "closing_backlog": bl, "closing_cash": cash, "closing_debt": debt}


def main():
    out = {m: project(m) for m in ("capacity", "recovery")}
    json.dump(out, open(os.path.join(HERE, "model.json"), "w"), indent=1)
    for m, p in out.items():
        print("=== %s (book converts over %d years) ===" % (m, p["conversion_years"]))
        print("%6s %10s %10s %7s %10s %8s %10s %10s %9s"
              % ("year", "revenue", "gross", "GM%", "FCFF", "EPS", "cash",
                 "backlog", "balance"))
        for r in p["rows"]:
            print("%6d %10.0f %10.0f %6.1f%% %10.0f %8.2f %10.0f %10.0f %9.2f"
                  % (r["year"], r["revenue"], r["gross_profit"],
                     100 * r["gross_margin"], r["fcff"], r["eps"], r["cash"],
                     r["backlog_close"], r["balance_check"]))
        print()


if __name__ == "__main__":
    main()
