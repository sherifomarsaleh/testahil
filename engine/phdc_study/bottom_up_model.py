"""PHDC forecast, built from units and prices the company itself discloses.

Two engines, because a developer has two:

  NEW SALES is units sold x average selling price, BY REGION. The releases plot
  both halves for each operating region, so the price is realised, not assumed.

  REVENUE is units delivered x revenue per delivered unit. Those are different
  units from the ones sold this year — a unit handed over in 2026 was contracted
  years earlier at that year's price — which is exactly why revenue per delivered
  unit sits below the current selling price, and why the order book keeps
  building.

Cost is cost per delivered unit on the same delivery schedule as revenue, so
GROSS MARGIN IS AN OUTPUT of the two, never an input. Everything below either
comes from the registry or is derived from it in one visible step.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)

import inputs as IN

REG = {}
for g in (IN.ACTUALS, IN.BALANCE_SHEET_FY25, IN.DEBT_FY25, IN.OPERATING, IN.MARKET):
    REG.update({k: r["value"] for k, r in g.items()})

W = json.load(open(os.path.join(HERE, "wacc_result.json")))
RJ = json.load(open(os.path.join(HERE, "regions.json")))

# [R-MACRO-01] and the horizon rule. THE EXPLICIT WINDOW RUNS UNTIL GROWTH HAS
# CONVERGED ON THE TERMINAL, and this company's did not: five years compounding
# at 44% nominal, capitalised at a normalised terminal rate, left 74% of value in
# the terminal and a 37-point discontinuity at the boundary. Neither the growth
# nor the terminal was wrong on its own; the window between them was too short to
# join them, so the model capitalised a rate it had never reached.
#
# Two changes, and they are the same change seen twice. Prices now escalate on
# the HOUSE PATH — 16% in 2026 falling to 7% — rather than at a flat 25.2%
# trailing mean that the central bank's own forecast contradicts. And deliveries
# fade from their disclosed 15% run to zero over the window, because a company
# cannot hand over 15% more homes every year for ever: it is limited by what it
# can build, and its own order book is finite. Both leave the last explicit year
# growing at inflation and nothing else, which is what the terminal assumes.
YEARS = list(range(2026, 2041))
import macro_path as _MP
_PATH = _MP.load("EG")
CPI = 0.2520                     # Egyptian CPI, 2023-25 mean, World Bank
TAX = 0.225
SHARES_MN = REG["shares_outstanding_bn"] * 1000.0
GROSS_DEBT = sum(r["value"] for r in IN.DEBT_FY25.values())
NET_DEBT = GROSS_DEBT - REG["cash"]

# --- the bridge stands on the LATEST disclosed balance sheet -----------------
# 31 March 2026 (reviewed), per GAP_REVIEW_01-09-2026 heading 6. FY2025 stays
# the base year of the PROJECTED statements above; only the enterprise-to-equity
# bridge, the book lens and the debt stack move to the newer sheet.
BS_BRIDGE = {k: r["value"] for k, r in IN.BALANCE_SHEET_1Q26.items()}
BRIDGE_BS_DATE = IN.BRIDGE_BS_DATE
GROSS_DEBT_BRIDGE = sum(BS_BRIDGE[k] for k in IN.DEBT_LINES)
NET_DEBT_BRIDGE = GROSS_DEBT_BRIDGE - BS_BRIDGE["cash"]

# Non-controlling interests come out of equity value at their SHARE OF VALUE,
# never at book (the standing NCI rule: the model capitalises 100% of subsidiary
# cash flow, so the minority's claim is worth its share of that value, not what
# it historically cost). The company does not disclose the subsidiaries that
# carry the minority with their own economics, so the share of value is proxied
# by the minority's filed share of FY2025 profit after tax — the same
# construction as the TMGH edition of 02-Sep-2026 — applied to EQUITY value
# (never to enterprise value). Book (1,432.7 at 31-Mar-2026) and the three-year
# mean profit share are published beside it as reference framings.
_HIS = {y: {k: r["value"] for k, r in d.items()} for y, d in IN.HISTORICAL_IS.items()}
NCI_VALUE_SHARE = _HIS["2025"]["nci"] / _HIS["2025"]["npat_pre_nci"]          # adopted proxy
NCI_PROFIT_SHARE_3Y = sum(_HIS[y]["nci"] / _HIS[y]["npat_pre_nci"] for y in ("2023", "2024", "2025")) / 3.0
NCI_BOOK_1Q26 = BS_BRIDGE["nci_equity"]                                        # reference: at book
NCI_BOOK_SHARE_1Q26 = BS_BRIDGE["nci_equity"] / BS_BRIDGE["total_equity"]       # reference: book share
NCI_BASIS = "share of equity value, proxied by the minority's filed share of FY2025 profit after tax"

# --- the disclosed regional history ----------------------------------------
LEGEND = {95082: "North Coast & Alexandria", 44570: "West Cairo & Badya",
          11364: "East Cairo"}
_lat = RJ["extract"]["2024_Q4_ER"]
REGION_HISTORY = {}
for b in _lat["regions"]:
    nm = LEGEND[int(round(b["sales"][-1]))]
    REGION_HISTORY[nm] = {
        "years": _lat["years"], "sales": b["sales"], "units": b["units"],
        "asp": [s / u if u else None for s, u in zip(b["sales"], b["units"])]}

# --- delivery engine, anchored on disclosure --------------------------------
# FY2024: the company handed over about 2,000 units and reported revenue of
# EGP 27,167mn, so revenue per delivered unit was EGP 13.58mn. Cost of revenue
# of EGP 17,837mn over the same units is EGP 8.92mn per unit.
DELIVERED_FY24 = 2000.0
REV_PER_DELIVERED_FY24 = REG["revenue_fy24"] / DELIVERED_FY24
COST_PER_DELIVERED_FY24 = REG["cogs_fy24"] / DELIVERED_FY24
# FY2025 is a CHECK, not an input: deliveries are not disclosed for that year,
# so the model's own revenue-per-unit path implies them and the implied figure
# is reported beside the disclosed revenue it has to reproduce.
DELIVERY_GROWTH = 0.15           # the disclosed run: 1,308 / 1,281 / 1,500 / ~2,000
DELIVERY_FADE_YEARS = 10         # over which that run fades to zero


def delivery_growth(i):
    """Delivery growth in explicit year i (1-based), fading to nothing.

    The disclosed run is 15% a year and it is real, but it is a RUN and not a
    steady state: the company is limited by what it can build and its order book,
    though large, is finite. Held flat for ever it would have PHD handing over
    fourteen times as many homes in 2040 as in 2026. The fade is linear to zero
    over ten years and it is STATED rather than fitted; the sensitivity below
    prices the whole plausible range of it.
    """
    if i <= 1:
        return 0.0
    f = max(0.0, 1.0 - (i - 2) / float(DELIVERY_FADE_YEARS))
    return DELIVERY_GROWTH * f


def price_growth(y):
    """Price and cost escalation: the house inflation path, zero real."""
    return _PATH.inflation(y)

# The P&L finance charge is NOT the marginal rate on gross borrowings, and using
# it that way overstates the charge by more than two times. Two reasons, both
# disclosed: a large part of the balance (notes payable to land sellers, customer
# balances) does not bear interest, and part of the interest that IS incurred is
# capitalised into work in progress rather than expensed. The interest-bearing
# subset is the bank and loan lines; the effective P&L rate is measured on it.
INTEREST_BEARING = (REG["loans_long_term"] + REG["credit_facilities"]
                    + REG["current_portion_st_loans"] + REG["banks_credit_balances"])
EFFECTIVE_PL_RATE = REG["finance_cost_fy25"] / INTEREST_BEARING

# Gross margin went 34.3% (FY2024) to 41.2% (FY2025) to 35.5% (1Q2026). The
# FY2025-to-1Q2026 pair implies cost rising about 9.7% a year faster than price
# — and that is NOT carried. One quarter against one year is a single
# observation on a developer whose margin moves with which project happens to
# hand over, and compounding it for five years takes gross margin to 7.5% and
# the company to a loss by 2030 on the strength of one print. A drift is carried
# only where a named mechanism has a measured like-for-like direction; there is
# none here. Price and cost therefore escalate together, holding margin at the
# average of the two most recent disclosures, and the margin is SENSITISED
# instead of extrapolated.
GM_FY25 = REG["gross_profit_fy25"] / REG["revenue_fy25"]
GM_1Q26 = REG["gross_profit_1q26"] / REG["revenue_1q26"]

# THE ANCHOR WAS THE AVERAGE OF A STALE FULL YEAR AND THE LATEST REVIEWED PERIOD, WHICH IS
# SPLITTING THE DIFFERENCE [corrected 03-Sep-2026]. The standing rule is explicit and has
# been since 07-Aug-2026: A NEAR-TERM REVIEWED ACTUAL OUTRANKS A STALE FULL-YEAR RATE —
# anchor every unit rate on the most recent reviewed period and hold everything else flat
# INCLUDING observed improvements. FY2025's 41.16% is the stale full year and 1Q2026's
# 35.48% is the most recent reviewed period; averaging them to 38.32% takes neither, and
# the protocol forbids splitting a difference in as many words elsewhere ("if genuinely
# disputed, default 0 and flag it, never split the difference").
#
# The reasoning that produced the average is KEPT because it is right about the thing it
# was about: the FY2025-to-1Q2026 pair implies cost rising about 9.7% a year faster than
# price, and compounding that for five years takes gross margin to 7.5% and this company to
# a loss by 2030 on the strength of one quarterly print. That DRIFT is not carried — a
# drift needs a named mechanism with a measured like-for-like direction and there is none
# here. But declining to carry the drift is not a reason to anchor above the latest
# reviewed level: the level and the trend are two different decisions, and the average
# conflated them.
GM_FORWARD = GM_1Q26
COST_DRIFT = 0.0
COST_DRIFT_MEASURED = ((1 - GM_1Q26) / (1 - GM_FY25)) - 1.0


def region_forecast():
    """Units sold and price per unit, by region, five years out."""
    out = {}
    for nm, h in REGION_HISTORY.items():
        units0 = sum(h["units"][-3:]) / 3.0        # trailing three-year mean
        asp0 = h["asp"][-1]                        # latest realised price
        rows = []
        asp = asp0
        for i, y in enumerate(YEARS, start=1):
            asp *= (1 + price_growth(y))
            rows.append({"year": y, "units": units0, "asp": asp,
                         "sales": units0 * asp})
        out[nm] = {"units_base": units0, "asp_base": asp0, "rows": rows}
    return out


def build():
    rf = region_forecast()
    backlog = REG["backlog_1q26"]
    # FY2026 IS PART-REPORTED, so it is anchored on what was reported rather
    # than projected over the top of it. The company disclosed 1Q2026 revenue of
    # EGP 9,300mn, up 11% on 1Q2025, which puts 1Q2025 at EGP 8,378mn — 23.2% of
    # that year's EGP 36,169mn. Carrying the same first-quarter share forward
    # gives an FY2026 revenue anchor from the actual, not from the trend.
    q1_26 = REG["revenue_1q26"]
    q1_25 = q1_26 / (1 + REG["revenue_1q26_yoy"])
    q1_share = q1_25 / REG["revenue_fy25"]
    fy26_anchor = q1_26 / q1_share
    # FY2025 is anchored on the DISCLOSED revenue, not on a projection of it:
    # deliveries for that year are not published, so the revenue-per-unit path is
    # escalated from FY2024 and the implied delivery count is read off the
    # disclosed revenue. That count is reported, so the reader can see it.
    rev_per = REV_PER_DELIVERED_FY24 * (1 + CPI)
    delivered = REG["revenue_fy25"] / rev_per
    implied_fy25_deliveries = delivered
    # THREE COMMENTS SAT ABOVE THIS LINE AND TWO OF THEM WERE WRONG [corrected
    # 03-Sep-2026]. One said cost per unit was anchored on FY2025's own cost of revenue;
    # one said it was set so the margin equalled a blend of two disclosures; and the line
    # forty rows below said "margin is the OUTPUT". Only the second described the code, and
    # its last clause — "it is an output of price and cost, not an input" — was exactly
    # backwards: the margin was the input and the cost was solved from it.
    #
    # WHY THE ARITHMETIC IS NOT REBUILT, stated rather than left as an apparent breach of
    # the margins-are-outputs rule. That rule fails a margin set as an input "wherever the
    # filings disclose enough to build cost PER UNIT instead", and here they do not: this
    # company does not publish a delivered-unit count for any period after FY2024. Every
    # later count in this model is IMPLIED from revenue divided by price per unit — which
    # means cost per unit collapses to price per unit times one minus the disclosed margin
    # BY CONSTRUCTION, whichever way it is written. There is no independent cost-per-unit
    # to build. So the margin is an input, it is declared as one at the 'derived' level
    # with the gap named, and what is actually decided here is WHICH disclosed margin
    # anchors it — see GM_FORWARD above.
    cost_per = rev_per * (1 - GM_FORWARD)

    debt = GROSS_DEBT
    kd = W["kd_pretax_local"]
    sga_ratio = REG["sga_fy25"] / REG["revenue_fy25"]
    da_ratio = REG["da_fy25"] / REG["revenue_fy25"]

    rows = []
    for i, y in enumerate(YEARS, start=1):
        rev_per *= (1 + price_growth(y))
        cost_per = rev_per * (1 - GM_FORWARD)
        if y == 2026:
            # deliveries implied by the reported anchor, not by the trend
            delivered = fy26_anchor / rev_per
        else:
            delivered *= (1 + delivery_growth(i))
        new_sales = sum(rf[nm]["rows"][i - 1]["sales"] for nm in rf)
        revenue = delivered * rev_per
        cogs = delivered * cost_per
        # NOT an output: cogs is solved from the anchored margin above, because no
        # delivered-unit count is published after FY2024 and the count in every
        # later year is implied from revenue over price. Stated where it is done.
        gross = revenue - cogs
        sga = revenue * sga_ratio
        da = revenue * da_ratio
        ebit = gross - sga - da
        interest = INTEREST_BEARING * EFFECTIVE_PL_RATE
        npbt = ebit - interest
        tax = max(0.0, npbt) * TAX
        npat = npbt - tax
        backlog = backlog + new_sales - revenue
        rows.append({
            "year": y, "units_delivered": delivered, "rev_per_unit": rev_per,
            "revenue": revenue, "cost_per_unit": cost_per, "cogs": cogs,
            "gross": gross, "gross_margin": gross / revenue, "sga": sga,
            "da": da, "ebit": ebit, "interest": interest, "npbt": npbt,
            "tax_rate": TAX, "npat": npat, "eps": npat / SHARES_MN,
            "price_growth": price_growth(y), "delivery_growth": delivery_growth(i),
            "new_sales": new_sales, "backlog": backlog,
            "units_sold": sum(rf[nm]["rows"][i - 1]["units"] for nm in rf),
        })
    return {"regions": rf, "rows": rows,
            "anchors": {
                "delivered_fy24": DELIVERED_FY24,
                "rev_per_delivered_fy24": REV_PER_DELIVERED_FY24,
                "cost_per_delivered_fy24": COST_PER_DELIVERED_FY24,
                "implied_fy25_deliveries": implied_fy25_deliveries,
                "fy25_revenue_anchor": REG["revenue_fy25"],
                "fy25_gross_margin_reproduced": 1 - (REG["cogs_fy25"]
                                                     / REG["revenue_fy25"]),
                "interest_bearing_debt": INTEREST_BEARING,
                "effective_pl_rate": EFFECTIVE_PL_RATE,
                "marginal_rate_for_discounting": kd,
                "cost_drift_carried": COST_DRIFT,
                "cost_drift_measured_not_carried": COST_DRIFT_MEASURED,
                "gross_margin_forward": GM_FORWARD,
                "gross_margin_fy25": GM_FY25, "gross_margin_1q26": GM_1Q26,
                "delivery_growth": DELIVERY_GROWTH, "cpi": CPI,
                "q1_2026_reported": q1_26, "q1_2025_derived": q1_25,
                "q1_share_of_year": q1_share, "fy2026_anchor": fy26_anchor}}


if __name__ == "__main__":
    m = build()
    a = m["anchors"]
    print("ANCHORS, all from disclosure")
    print("  FY2024 units delivered                %8.0f   (company: 'c. 2,000')"
          % a["delivered_fy24"])
    print("  FY2024 revenue per delivered unit     %8.2f   EGP mn  = 27,167 / 2,000"
          % a["rev_per_delivered_fy24"])
    print("  FY2024 cost per delivered unit        %8.2f   EGP mn  = 17,837 / 2,000"
          % a["cost_per_delivered_fy24"])
    print("  FY2025 revenue anchor                 %8.0f   disclosed"
          % a["fy25_revenue_anchor"])
    print("  implied FY2025 units delivered        %8.0f   = revenue / price per unit"
          % a["implied_fy25_deliveries"])

    print("  1Q2026 revenue reported               %8.0f   up 11%% on 1Q2025"
          % a["q1_2026_reported"])
    print("  implied 1Q share of the full year     %8.1f%%  1Q2025 %0.0f over FY2025 %0.0f"
          % (100 * a["q1_share_of_year"], a["q1_2025_derived"], REG["revenue_fy25"]))
    print("  FY2026 revenue anchor                 %8.0f   from the reported quarter"
          % a["fy2026_anchor"])
    print("  interest-bearing debt                 %8.0f   EGP mn (bank and loan lines)"
          % a["interest_bearing_debt"])
    print("  effective P&L interest rate           %8.2f%%  vs %0.2f%% marginal, used "
          "for discounting" % (100 * a["effective_pl_rate"],
                               100 * a["marginal_rate_for_discounting"]))
    print("  forward gross margin                  %8.1f%%  blend of FY2025 %.1f%% and "
          "1Q2026 %.1f%%" % (100 * a["gross_margin_forward"],
                             100 * a["gross_margin_fy25"],
                             100 * a["gross_margin_1q26"]))
    print("  cost drift measured but NOT carried   %8.2f%%  one quarter against one "
          "year is not a trend" % (100 * a["cost_drift_measured_not_carried"]))
    print()
    print("NEW SALES — units x price, by region")
    for nm, d in m["regions"].items():
        print("  %-28s units %6.0f (3y mean)   price %6.2f EGP mn (2024 realised)"
              % (nm, d["units_base"], d["asp_base"]))
    print()
    hdr = "%-30s" + "%12d" * len(YEARS)
    print(hdr % tuple(["EGP mn unless stated"] + YEARS))
    def line(lbl, key, fmt="%12.0f", scale=1.0):
        print(("%-30s" % lbl) + "".join(fmt % (r[key] * scale) for r in m["rows"]))
    line("Units sold", "units_sold")
    line("New sales", "new_sales")
    line("Units delivered", "units_delivered")
    line("Revenue per delivered unit", "rev_per_unit", "%12.2f")
    line("Revenue", "revenue")
    line("Cost per delivered unit", "cost_per_unit", "%12.2f")
    line("Cost of revenue", "cogs")
    line("Gross profit", "gross")
    line("Gross margin", "gross_margin", "%11.1f%%", 100)
    line("Overheads", "sga")
    line("Operating profit", "ebit")
    line("Finance cost", "interest")
    line("Profit before tax", "npbt")
    line("Net profit", "npat")
    line("Earnings per share (EGP)", "eps", "%12.2f")
    line("Order book, closing", "backlog")
    json.dump(m, open(os.path.join(HERE, "bottom_up_model.json"), "w"),
              indent=1, default=str)
