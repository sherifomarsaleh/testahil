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
import inputs as IN

TAX = 0.225
# THE WINDOW MUST BE LONG ENOUGH TO DELIVER THE BOOK IT CAN SEE. The order book
# converts over 10-14 years, so a 10-year window pushed the majority of a
# FINITE, CONTRACTED, ALREADY-SOLD pipeline into a terminal stub -- and at a
# 35.79% discount rate a stub starting in year 11 is worth almost nothing. The
# model valued EGP 1.6 TRILLION of contracted book at about EGP 9bn. Twenty
# years lets the current book and one replenishment cycle actually be built,
# handed over and collected inside the explicit period, which is what the
# company will in fact do.
EXPLICIT_YEARS = 20
FIRST_YEAR = 2026

# THE CRUX, in two readings. TMG's order book is EGP 491.0bn against 1H2026
# deliveries of EGP 17.0bn — about fourteen years at the current rate. Neither
# reading can be dismissed from what the company discloses, so both are carried
# through to the answer and published side by side.
# THE CRUX, RESTATED. It was "how many years does a STATIC book take to
# convert", which forced deliveries to a fraction of a book that kept growing
# and made the company shrink in real terms. The binding constraint on a
# developer with more demand than capacity is HOW FAST IT CAN BUILD AND HAND
# OVER, and TMG's own record answers it: development revenue went EGP 8,152mn
# (2019) to EGP 36,706mn (2025), a compound 28.5% a year in nominal terms,
# about 7% real. Meanwhile cover -- the book divided by a year's deliveries --
# went from 5.2 years (2021) to 12.0 (2025), because it sold far faster than it
# built.
#
# So deliveries are now the DRIVER and contracted sales the BALANCING ITEM: the
# company sells what keeps its book at a stated cover, which is what a developer
# with demand in excess of capacity actually does.
DELIVERY_GROWTH_CAPACITY = 0.20    # inflation only -- no real scaling at all
DELIVERY_GROWTH_RECOVERY = 0.285   # its own 2019-2025 compound rate
# ONE CRUX, NOT TWO. Cover is held at the same level in both readings so the
# crux is a single question a reader can weigh -- how fast can TMG build? -- and
# 10 years is between the 5.2 it ran in 2021 and the 12.0 it reached in 2025.
# Letting cover FALL was its own error: a shrinking book starves the customer
# advances that fund construction, so the faster reading turned cash-negative
# while building more, which is backwards for a company paid up front.
COVER_TARGET_CAPACITY = 10.0
COVER_TARGET_RECOVERY = 10.0
COVER_ADJUST_YEARS = 6
FADE_START = 10        # years 1-10 at the crux rate, 11-20 fading to the economy

CAPACITY_YEARS = 14   # retained only for the residual annuity below
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

# REPLENISHMENT SALES ARE ANCHORED ON THE LAST REPORTED YEAR AND HELD THERE.
# [R-SANITY-01] The first cut set this to 300,000 -- BELOW every year the
# company has reported -- and then faded it 15% a year to 96,173 by 2033. In an
# economy running near 20% inflation that is a real decline of about a third a
# year, for a company whose order book is at a record. It was not a forecast
# about the business; it was a guard added to stop an earlier version's book
# exploding, which kept going until it became an assumption.
#
# The anchor is now the LAST FULL REPORTED YEAR and nothing else is invented:
# FY2025 contracted sales, from the company's own results release. Held FLAT IN
# NOMINAL TERMS, which is already conservative -- it is a real decline at
# Egyptian inflation -- and is the "freeze" benchmark this name's own
# walk-forward found the method could not beat at one year out.
REPLENISHMENT_SALES = 382200.0   # FY2025 contracted sales, as reported
# EVERY NOMINAL DRIVER INFLATES AT THE SAME RATE OR THE MODEL IS FORECASTING A
# REAL DECLINE IT NEVER DECIDED ON. Hospitality grows at 20% and other recurring
# at 22% -- both roughly Egyptian nominal growth. Contracted sales were held at
# 0%, which in a 20%-inflation economy is an 84% REAL decline across the window:
# the model was saying TMG's new business shrinks to a sixth of its size while
# its hotels grow with the price level. That is not a view anyone formed; it is
# the 15% fade again, wearing inflation instead of a parameter.
SALES_GROWTH = 0.20              # the same nominal rate the recurring legs use

# CONTRACTED SALES AND THE ORDER BOOK ARE NOT ON THE SAME BASIS, AND THE FIRST
# CUT FED ONE STRAIGHT INTO THE OTHER.  Measured on the company's own two
# disclosed series, the share of a year's contracted sales that shows up in the
# book -- the rise in backlog plus the development revenue recognised out of it
# -- is nowhere near all of it:
#
#     FY2021 75.3%   FY2022 87.3%   FY2023 62.5%   FY2024 34.4%   FY2025 48.1%
#
# FY2024 is the clearest case: EGP 504,000mn of sales against a backlog that
# rose EGP 149,000mn. Feeding sales in one-for-one is arithmetically impossible
# against what the company reports, and it is what drove the book to EGP 3.2
# TRILLION when the fade that had been hiding it was removed. The 15% fade was
# never a view about the business; it was compensating for this.
#
# Anchored on the MOST RECENT FULL YEAR rather than an average across a
# definition that is visibly moving -- the near-term-actual rule -- and
# sensitised across the whole observed range, which is wide and is published as
# such rather than smoothed away.
BACKLOG_CAPTURE = 0.481          # FY2025: (147,200 + 36,706) / 382,200
CAPTURE_OBSERVED = (0.344, 0.873)   # FY2024 low, FY2022 high
HOSP_GROWTH = 0.20
OTHER_GROWTH = 0.22
HOSP_CAPEX_RATIO = 0.10
OTHER_CAPEX_RATIO = 0.04
# CUSTOMER ADVANCES AGAINST THE ORDER BOOK, from the company's own balance
# sheet: EGP 133,993.1mn of advances at 30 June 2026 against a book of EGP
# 491,000mn. A disclosed ratio, not a chosen one.
# ADVANCES SIT AGAINST WORK IN PROGRESS, NOT AGAINST THE WHOLE BOOK. At 30 June
# 2026 customer advances were EGP 133,993.1mn against properties under
# development of EGP 148,315.4mn -- 90.3%. The company's construction is very
# nearly funded by the people who will live in it, which is what off-plan IS.
# Tying advances to the BOOK instead made growth cash-CONSUMPTIVE: work in
# progress grew with deliveries while advances grew with a book whose cover was
# falling, so profits rose and free cash flow did not. That is contradicted by
# the balance sheet -- TMG holds EGP 47bn of cash and deposits against EGP 17bn
# of borrowings and pays dividends, while growing deliveries 28.5% a year. A
# company financing growth out of its own pocket does not look like that.
ADV_COVER_ON_PUD = 133993.1 / 148315.4      # 90.3%
# ADVANCES TRACK CONSTRUCTION CONTEMPORANEOUSLY. A four-year adjustment lag
# meant the company built now and collected a quarter of it a year for four
# years, which is not how a payment plan works and is not what the disclosed
# 90.3% relationship shows -- that ratio holds at the balance-sheet date, not
# four years after it. The lag alone was the drag that kept free cash flow at a
# fifth of net profit while the company grew.
ADV_ADJUST_YEARS = 1

PUD_COVER_YEARS = 4.0   # work in progress against a year's cost of sales; TMG
                        # held EGP 148.3bn at 30 June 2026 against a modelled
                        # FY2026 development cost of about EGP 36bn
PUD_ADJUST_YEARS = 4    # how fast the stock is moved toward that cover
DA_RATE_ON_PPE = 0.012          # the group's own charge against gross PP&E
DEPOSIT_YIELD = 0.20            # below the policy rate, on a mixed deposit book
# A terminal rate BELOW inflation is a perpetual real decline. 15% against ~20%
# nominal growth shrank the recurring legs for ever, again without anyone
# deciding to.
TERMINAL_GROWTH = 0.20
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


def project(mode, years=EXPLICIT_YEARS, capture=BACKLOG_CAPTURE):
    r = ratios()
    n = CAPACITY_YEARS if mode == "capacity" else RECOVERY_YEARS
    ramp = CAPACITY_RAMP if mode == "capacity" else RECOVERY_RAMP
    delivery_growth = (DELIVERY_GROWTH_CAPACITY if mode == "capacity"
                       else DELIVERY_GROWTH_RECOVERY)
    cover_target = (COVER_TARGET_CAPACITY if mode == "capacity"
                    else COVER_TARGET_RECOVERY)
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
        # DELIVERIES ARE THE DRIVER. Anchored on the reviewed half-year actual
        # in the first year [L-013], then growing at the rate the crux states.
        if i == 0:
            dev_rev = _v(IN.H1_26, "dev_revenue") * SEASONAL
        else:
            # GROWTH FADES TO THE ECONOMY'S. Holding the crux rate for ever
            # would capitalise a scaling phase as a permanent state; dropping
            # straight to nominal GDP at year 11 pretends a company mid-build
            # stops the day the window closes. Neither is what happens. Years
            # 1-10 run at the crux rate, years 11-20 fade linearly to the
            # long-run nominal rate, and the perpetuity picks up there -- the
            # ordinary two-stage treatment, stated rather than assumed.
            if i < FADE_START:
                g_i = delivery_growth
            else:
                k = (i - FADE_START + 1) / float(EXPLICIT_YEARS - FADE_START)
                g_i = delivery_growth + (TERMINAL_GROWTH - delivery_growth) * k
            dev_rev = rows[-1]["dev_revenue"] * (1 + g_i)
        # CONTRACTED SALES ARE THE BALANCING ITEM: enough to hold the book at
        # the cover this reading specifies. TMG has demonstrated demand far in
        # excess of what it can build -- it sold about ten times its deliveries
        # in FY2025 -- so what bounds the business is construction, not orders,
        # and the model now says so instead of letting two independent growth
        # rates diverge into a book of EGP 27 trillion.
        target_book = cover_target * dev_rev
        new_sales = max(dev_rev + (target_book - bl) / COVER_ADJUST_YEARS, 0.0)
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

        # COLLECTIONS AND BUILD SPEND MUST SIT ON THE SAME CLOCK.  The first
        # cut set collections as a flat rate on the ORDER BOOK while build
        # spend moved with DELIVERIES, so accelerating handovers spent cash
        # faster than it collected any and the faster reading's free cash flow
        # went NEGATIVE from 2029 -- building a home became value-destroying.
        # For an off-plan developer that is backwards: the customer pays AS
        # CONSTRUCTION PROGRESSES, which is why the advances are there.
        #
        # This module's own docstring already stated the rule ("the two
        # contract positions -- customer advances and properties under
        # development -- are driven off the SAME order book, never one off
        # revenue and the other off backlog") and the code did not obey it.
        # Advances are now driven off the book on their own disclosed cover,
        # and collections fall out of the identity the ratios block uses on the
        # actual half-year: collections = revenue recognised + the rise in
        # advances.
        # WORK IN PROGRESS FIRST, THEN THE ADVANCES THAT FUND IT. Order
        # matters: reading advances off the OPENING stock collects against
        # construction that has not been done yet and lags a year behind the
        # build every year of the window.
        #
        # PROPERTIES UNDER DEVELOPMENT IS A STOCK, and build spend is what moves
        # it toward the cover the programme needs. Modelling build as a fixed
        # multiple of cost instead — 2.47x, which is what the company spent in
        # the half-year just closed while building ahead of a book it had
        # already sold — made the company build ever faster for ever, and drove
        # cash to minus EGP 4 trillion. A developer whose handovers are catching
        # up CONSUMES its work in progress; the stock adjustment lets it.
        target_pud = PUD_COVER_YEARS * dev_cost
        build = max(dev_cost + (target_pud - pud) / PUD_ADJUST_YEARS, 0.0)
        pud_close = pud + build - dev_cost
        target_adv = ADV_COVER_ON_PUD * pud_close
        d_adv_target = (target_adv - adv) / ADV_ADJUST_YEARS
        collections = dev_rev + d_adv_target
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
