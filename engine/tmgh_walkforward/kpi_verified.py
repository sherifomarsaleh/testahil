"""The operating drivers, one cell at a time, each read against its own sentence.

The automatic pass (parse_kpi.py + kpi_panel.py) proposes; this file disposes.
Every cell below was read in the sentence the release actually prints, and the
sentence is carried with it. That is deliberate and not a shortcut: a mode vote
over prose put FY2023's CORE sales figure in the headline slot, read a sentence
about 37,000 units still to be delivered as 12,000 units sold, and took a
delivery count for a sales count — three wrong cells that every arithmetic
check in the panel would have accepted, because prose has no arithmetic.

WHAT TMG DISCLOSES, AND WHAT IT DOES NOT. New sales value and backlog run the
whole span. Units sold and units delivered are published only occasionally and
never as a continuous series, so THE UNIT LEVEL IS NOT AVAILABLE for this
issuer and the driver build stands at segment level with that gap stated —
[R-SIGCM-02]'s "segment" level, not "unit". Backlog before FY2018 is disclosed
only as an approximation ("approximately EGP 20 BN"), which is recorded as
such rather than carried at false precision.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
A = "A"          # company's own document

# (value in EGP mn, document, page, the sentence as printed, precision)
NEW_SALES = {
    2011: (3012.0, "TMG_Holding_full_year_and_fourth_quarter_ending_December_31_2012_Earning_Release", 2,
           "new sales of real estate units amounted to EGP 4,482 MN for 12M -12, compared to "
           "EGP 3,012 MN for the same period last year", "exact", "prior-year column of the FY2012 release"),
    2012: (4482.0, "TMG_Holding_full_year_and_fourth_quarter_ending_December_31_2012_Earning_Release", 2,
           "Total new sales of real estate units amounted to EGP 4,482 MN for 12M -12", "exact", None),
    2013: (6581.0, "TMG_full_year_and_fourth_quarter_2013_Earning_Release", 2,
           "Total new sales of real estate units amounted to EGP 6,581 mn for 12M -13", "exact", None),
    2014: (6585.0, "TMG_full_year_and_fourth_quarter_2014_Earning_Release", 2,
           "Total new sales of real estate units amounted to EGP 6,585 MN for 12M -14", "exact", None),
    2015: (6260.0, "TMG_Holding_Full_Year_and_Fourth_Quarter_ending_December_31_2015", 2,
           "Total new sales of real estate units amounted to EGP 6.26 BN for 12M -15", "0.01bn", None),
    2016: (7400.0, "TMG_Holding_Full_Year_and_Fourth_Quarter_ending_December_31_2016", 2,
           "Total new sales of real estate units witnessed an increase of 17% amounted to "
           "EGP 7.4 BN for 12M-16", "0.1bn", None),
    2018: (21300.0, "TMG_Holding_FY2018_earnings_release", 1,
           "Total presales came in at a record-high EGP21.3bn in FY2018, growing 62% y-o-y", "0.1bn", None),
    2019: (20400.0, "TMG_Holding_market_update_on_FY2019_sales_6_January_2020_", 1,
           "TMG Holding records total sales of EGP20.4bn in FY2019", "0.1bn", None),
    2020: (16600.0, "TMG_Holding_FY2020_earnings_release", 1,
           "net sales of EGP16.6bn", "0.1bn", None),
    2021: (32400.0, "TMG_Holding_FY2021_earnings_release", 1,
           "New sales surpass EGP32.4bn", "0.1bn", None),
    2022: (33200.0, "TMG_Holding_FY2022_Earnings_Release", 1,
           "EGP33.2bn in new net sales", "0.1bn", None),
    2023: (142800.0, "TMG_Holding_4Q23_earnings_release", 2,
           "Total new sales in FY2023 soared to an unprecedented EGP142.8bn, marking the "
           "highest sales ever recorded in the history of the company", "0.1bn",
           "TOTAL, not the EGP94.9bn core figure the same release quotes beside it; the "
           "difference is a large non-core land transaction and is a basis break, "
           "recorded in BASIS_BREAKS"),
    2024: (504000.0, "TMG_Holding_FY24_earnings_release_vFINAL", 1,
           "recorded unprecedented sales of over EGP 504 billion (approximately USD 10 billion), "
           "tripling the previous", "1bn",
           "cross-checks against the FY25 release's stated 24% decline to EGP 382.2bn"),
    2025: (382200.0, "TMG_Holding_FY25_ER_-_EN", 1,
           "EGP 382.2 bn Contracted Sales  24% YoY", "0.1bn", None),
}

BACKLOG = {
    2012: (18000.0, "TMG_Holding_full_year_and_fourth_quarter_ending_December_31_2012_Earning_Release", 2,
           "the backlog of sold but unrecognized units is approximately EGP 18 BN", "approximate", None),
    2013: (19950.0, "TMG_full_year_and_fourth_quarter_2013_Earning_Release", 2,
           "the backlog of sold but unrecognized units is approximately EGP 19.95 bn", "approximate", None),
    2014: (20000.0, "TMG_full_year_and_fourth_quarter_2014_Earning_Release", 2,
           "the backlog of sold but unrecognized units is approximately EGP 20 Bn", "approximate", None),
    2015: (20600.0, "TMG_Holding_Full_Year_and_Fourth_Quarter_ending_December_31_2015", 2,
           "the backlog of sold but unrecognized units is approximately EGP 20.6 BN", "approximate", None),
    2016: (22000.0, "TMG_Holding_Full_Year_and_Fourth_Quarter_ending_December_31_2016", 2,
           "the backlog of sold but unrecognized units is approximately EGP 22 BN", "approximate", None),
    2017: (30000.0, "TMG_Holding_FY2018_earnings_release", 2,
           "Our backlog stood at an unmatched EGP41.7bn as at end FY2018, compared to "
           "EGP30bn as at end-FY2017", "1bn", "prior-year figure stated in the FY2018 release"),
    2018: (41700.0, "TMG_Holding_FY2018_earnings_release", 1, "backlog of EGP41.7bn", "0.1bn", None),
    2019: (49500.0, "TMG_Holding_FY2019_earnings_release", 1, "backlog of EGP49.5bn", "0.1bn", None),
    2020: (50800.0, "TMG_Holding_FY2020_earnings_release", 1, "backlog of EGP50.8bn", "0.1bn", None),
    2021: (63100.0, "TMG_Holding_FY2021_earnings_release", 1, "backlog of EGP63.1bn", "0.1bn", None),
    2022: (77400.0, "TMG_Holding_FY2022_Earnings_Release", 1,
           "backlog stood at an unmatched EGP77.4bn", "0.1bn", None),
    2023: (145000.0, "TMG_Holding_4Q23_earnings_release", 1,
           "backlog of sold but not yet delivered units stood at a remarkable EGP145bn", "1bn", None),
    2024: (294000.0, "TMG_Holding_FY24_earnings_release_vFINAL", 2,
           "the Group's backlog of recorded and yet undelivered sales (sales backlog) "
           "amounted to EGP 294 billion", "1bn", None),
    2025: (441200.0, "TMG_Holding_FY25_ER_-_EN", 2,
           "Backlog build-up to EGP 441.2 billion", "0.1bn", None),
}

# Published only occasionally. NOT a series, and deliberately not treated as one.
UNITS_DELIVERED = {
    2021: (2991.0, "TMG_Holding_FY2021_earnings_release", 1,
           "delivery of 2,991 residential and non-residential units", "exact", None),
    2022: (4091.0, "TMG_Holding_FY2022_Earnings_Release", 1,
           "delivery of 4,091 residential and non-residential units during the period", "exact", None),
    2023: (2661.0, "TMG_Holding_4Q23_earnings_release", 1,
           "delivery of 2,661 residential and non-residential units", "exact", None),
    2025: (3196.0, "TMG_Holding_FY25_ER_-_EN", 2,
           "3,196 units delivered across three projects", "exact", None),
}
UNITS_SOLD = {
    2022: (6102.0, "TMG_Holding_FY2022_Earnings_Release", 2,
           "representing some 6,102 units", "exact", None),
}

NOT_DISCLOSED = {
    "new_sales_value": {
        2009: "no full-year sales figure survives in a readable release",
        2010: "the FY2010 release states EGP 4.144bn of new sales, but its own summary "
              "table does not resolve and the year is excluded from the panel",
        2017: "no FY2017 sales total is stated in any release held. The FY2018 release "
              "gives 62% growth, from which 13.1bn follows arithmetically — that is an "
              "INFERENCE, not a disclosure, and the cell is left empty rather than filled",
    },
    "backlog": {
        2009: "not stated in a readable release",
        2010: "stated only as 'exceeds the level of EGP 22 bn' — a floor, not a figure",
        2011: "not stated in the FY2011 release",
    },
    "units_sold": {
        "all_but_2022": "TMG does not publish a continuous unit-count series. Occasional "
                        "mentions exist and are not a series; building a price-per-unit "
                        "driver on them would divide one year's value by another year's "
                        "count, which is the arithmetic error L-010 records."},
    "units_delivered": {
        "all_but_2021_2023_2025": "same — occasional, not continuous"},
}


def _rows(d, field):
    out = {}
    for y, (v, doc, page, sent, prec, note) in d.items():
        out[str(y)] = {"value": v, "unit": "EGP mn" if field in
                       ("new_sales_value", "backlog") else "units",
                       "source": doc, "page": page, "sentence": sent,
                       "precision": prec, "tier": A, "note": note,
                       "read": "verified against the sentence as printed"}
    return out


def build():
    return {
        "new_sales_value": _rows(NEW_SALES, "new_sales_value"),
        "backlog": _rows(BACKLOG, "backlog"),
        "units_delivered": _rows(UNITS_DELIVERED, "units_delivered"),
        "units_sold": _rows(UNITS_SOLD, "units_sold"),
        "not_disclosed": NOT_DISCLOSED,
        "_note": __doc__,
    }


if __name__ == "__main__":
    d = build()
    json.dump(d, open(os.path.join(HERE, "panel_kpi_verified.json"), "w"), indent=1)
    print("%-6s %12s %12s %10s %10s" % ("year", "new sales", "backlog",
                                        "delivered", "units sold"))
    for y in range(2009, 2026):
        s = d["new_sales_value"].get(str(y), {}).get("value")
        b = d["backlog"].get(str(y), {}).get("value")
        u = d["units_delivered"].get(str(y), {}).get("value")
        q = d["units_sold"].get(str(y), {}).get("value")
        print("%-6d %12s %12s %10s %10s"
              % (y, "%.0f" % s if s else "-", "%.0f" % b if b else "-",
                 "%.0f" % u if u else "-", "%.0f" % q if q else "-"))
