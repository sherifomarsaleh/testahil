"""TMGH valuation inputs — every figure with value, source, date, provenance tier.

Tier A = the company's own audited or reviewed statements, or its own IR documents.
Tier C = credible third party (used ONLY for exogenous macro and market prices).

No financial numeral is typed into a builder anywhere else in this study; the
builders read this registry. Anything not disclosed is recorded here as a GAP
with what would close it, never filled with an estimate that reads like a fact.

Every statement figure below was footed against the statement's own arithmetic
before it was entered — see engine/tmgh_walkforward/panel.py, which does the same
check mechanically across the whole fifteen-year panel.
"""
IR = "https://talaatmoustafa.com/investor-relations/"
FS25 = ("TMG Holding consolidated financial statements for the year ended "
        "31 December 2025 (English translation of the Arabic original), via " + IR)
FS26H1 = ("TMG Holding interim consolidated financial statements for the three and "
          "six months ended 30 June 2026 (reviewed), via " + IR)
ER26H1 = "TMG Holding 1H 2026 earnings release, Cairo, 12 August 2026, via " + IR
ER25 = "TMG Holding FY2025 earnings release, via " + IR
FS24 = ("TMG Holding consolidated financial statements for the year ended "
        "31 December 2024, via " + IR)
FS23 = ("TMG Holding consolidated financial statements for the year ended "
        "31 December 2023, via " + IR)
WF = "engine/tmgh_walkforward — this name's own fundamental walk-forward, 1 Sep 2026"


def I(value, source, date, tier, unit="EGP mn", gap=None, note=None):
    d = {"value": value, "source": source, "date": date, "tier": tier, "unit": unit}
    if gap:
        d["gap"] = gap
    if note:
        d["note"] = note
    return d


# ---------------------------------------------------------------------------
# FY2025 consolidated income statement — as reported. Foots: the three segment
# gross profits sum to 20,855.4, and the waterfall closes to net profit 18,202.0.
IS = {
    "dev_revenue_fy25":   I(36705.7, FS25, "2025-12-31", "A"),
    "dev_cost_fy25":      I(26645.4, FS25, "2025-12-31", "A"),
    "hosp_revenue_fy25":  I(14889.7, FS25, "2025-12-31", "A"),
    "hosp_cost_fy25":     I(7800.6,  FS25, "2025-12-31", "A"),
    "other_revenue_fy25": I(10899.7, FS25, "2025-12-31", "A"),
    "other_cost_fy25":    I(7193.7,  FS25, "2025-12-31", "A"),
    "gross_profit_fy25":  I(20855.4, FS25, "2025-12-31", "A"),
    "ip_revaluation_fy25": I(3952.5, FS25, "2025-12-31", "A",
                             note="non-cash fair-value gain on investment property; "
                                  "excluded from the cash-flow lens"),
    "other_income_fy25":  I(3653.8,  FS25, "2025-12-31", "A"),
    "ga_fy25":            I(2132.9,  FS25, "2025-12-31", "A"),
    "marketing_fy25":     I(745.8,   FS25, "2025-12-31", "A"),
    "fx_fy25":            I(-85.7,   FS25, "2025-12-31", "A"),
    "govt_donations_fy25": I(1340.4, FS25, "2025-12-31", "A"),
    "provisions_ecl_fy25": I(407.6,  FS25, "2025-12-31", "A"),
    "operating_income_fy25": I(23749.3, FS25, "2025-12-31", "A"),
    "finance_income_fy25": I(4230.0, FS25, "2025-12-31", "A"),
    "finance_cost_fy25":  I(3936.5,  FS25, "2025-12-31", "A",
                            note="finance expenses 3,820.4 + bank charges 116.2 per "
                                 "note 37. NOT interest on borrowings alone — see the "
                                 "walk-forward's blocked correction"),
    "associates_fy25":    I(38.1,    FS25, "2025-12-31", "A"),
    "da_fy25":            I(427.3,   FS25, "2025-12-31", "A"),
    "pbt_fy25":           I(23653.6, FS25, "2025-12-31", "A"),
    "tax_fy25":           I(4334.2,  FS25, "2025-12-31", "A"),
    "deferred_tax_fy25":  I(1117.4,  FS25, "2025-12-31", "A"),
    "net_profit_fy25":    I(18202.0, FS25, "2025-12-31", "A"),
    "npat_parent_fy25":   I(14383.9, FS25, "2025-12-31", "A"),
    "nci_profit_fy25":    I(3818.1,  FS25, "2025-12-31", "A"),
    "eps_fy25":           I(6.98,    FS25, "2025-12-31", "A", unit="EGP/share"),
    # FY2024 AS FIRST REPORTED. The FY2025 statements restate this year for a
    # purchase-price allocation completed inside the measurement period; the
    # restated column is shown beside it and never substituted for it.
    "dev_revenue_fy24":   I(24518.3, FS24, "2024-12-31", "A"),
    "hosp_revenue_fy24":  I(11496.5, FS24, "2024-12-31", "A"),
    "other_revenue_fy24": I(6655.5,  FS24, "2024-12-31", "A"),
    "gross_profit_fy24":  I(15300.2, FS24, "2024-12-31", "A"),
    "net_profit_fy24":    I(14467.5, FS24, "2024-12-31", "A"),
    "npat_parent_fy24":   I(10723.1, FS24, "2024-12-31", "A"),
    "gross_profit_fy24_restated": I(14002.2, FS25 + " (comparative, marked Restated)",
                                    "2024-12-31", "A"),
    "net_profit_fy24_restated": I(12769.5, FS25 + " (comparative, marked Restated)",
                                  "2024-12-31", "A"),
    "npat_parent_fy24_restated": I(9025.1, FS25 + " (comparative, marked Restated)",
                                   "2024-12-31", "A"),
    "dev_revenue_fy23":   I(21578.7, FS23, "2023-12-31", "A"),
    "hosp_revenue_fy23":  I(3540.9,  FS23, "2023-12-31", "A"),
    "other_revenue_fy23": I(3311.7,  FS23, "2023-12-31", "A"),
    "gross_profit_fy23":  I(8637.3,  FS23, "2023-12-31", "A"),
    "net_profit_fy23":    I(3347.3,  FS23, "2023-12-31", "A"),
    "npat_parent_fy23":   I(3313.3,  FS23, "2023-12-31", "A"),
}

# 1H2026 reviewed interim — the most recent actual, and the anchor for FY2026.
H1_26 = {
    "dev_revenue":      I(16967.2, FS26H1, "2026-06-30", "A"),
    "dev_cost":         I(12457.5, FS26H1, "2026-06-30", "A"),
    "hosp_revenue":     I(7512.9,  FS26H1, "2026-06-30", "A"),
    "hosp_cost":        I(4104.2,  FS26H1, "2026-06-30", "A"),
    "other_revenue":    I(5711.9,  FS26H1, "2026-06-30", "A"),
    "other_cost":       I(3889.2,  FS26H1, "2026-06-30", "A"),
    "gross_profit":     I(9741.1,  FS26H1, "2026-06-30", "A"),
    "operating_income": I(12931.6, FS26H1, "2026-06-30", "A"),
    "finance_income":   I(1037.3,  FS26H1, "2026-06-30", "A"),
    "finance_cost":     I(1006.2,  FS26H1, "2026-06-30", "A"),
    "da":               I(259.8,   FS26H1, "2026-06-30", "A"),
    "pbt":              I(12745.7, FS26H1, "2026-06-30", "A"),
    "tax":              I(2542.7,  FS26H1, "2026-06-30", "A"),
    "deferred_tax":     I(257.2,   FS26H1, "2026-06-30", "A"),
    "net_profit":       I(9945.8,  FS26H1, "2026-06-30", "A"),
    "npat_parent":      I(7477.4,  FS26H1, "2026-06-30", "A"),
    "nci_profit":       I(2468.3,  FS26H1, "2026-06-30", "A"),
    "eps":              I(3.63,    FS26H1, "2026-06-30", "A", unit="EGP/share"),
    "h1_25_dev_revenue": I(12621.8, FS26H1 + " (comparative)", "2025-06-30", "A"),
    "h1_25_net_profit":  I(8111.2,  FS26H1 + " (comparative)", "2025-06-30", "A"),
}

# Balance sheet — 30 June 2026 (reviewed) with 31 December 2025 beside it.
BS = {
    "ppe":                I(73322.7,  FS26H1, "2026-06-30", "A"),
    "investment_property": I(25228.0, FS26H1, "2026-06-30", "A"),
    "assets_under_construction": I(21901.5, FS26H1, "2026-06-30", "A"),
    "intangibles":        I(84.6,     FS26H1, "2026-06-30", "A"),
    "right_of_use":       I(481.4,    FS26H1, "2026-06-30", "A"),
    "goodwill":           I(12665.3,  FS26H1, "2026-06-30", "A"),
    "associates":         I(1496.6,   FS26H1, "2026-06-30", "A"),
    "fvoci":              I(1802.8,   FS26H1, "2026-06-30", "A"),
    "deposits_noncurrent": I(9393.9,  FS26H1, "2026-06-30", "A"),
    "deferred_tax_asset": I(182.0,    FS26H1, "2026-06-30", "A"),
    "total_noncurrent_assets": I(146558.8, FS26H1, "2026-06-30", "A"),
    "properties_under_development": I(148315.4, FS26H1, "2026-06-30", "A"),
    "work_in_progress":   I(23.6,     FS26H1, "2026-06-30", "A"),
    "inventories":        I(4592.3,   FS26H1, "2026-06-30", "A"),
    "trade_notes_receivable": I(24007.1, FS26H1, "2026-06-30", "A"),
    "nr_undelivered":     I(13769.5,  FS26H1, "2026-06-30", "A"),
    "other_current_assets": I(72647.7, FS26H1, "2026-06-30", "A"),
    "fvtpl":              I(1603.9,   FS26H1, "2026-06-30", "A"),
    "deposits_current":   I(19273.2,  FS26H1, "2026-06-30", "A"),
    "cash":               I(47106.3,  FS26H1, "2026-06-30", "A"),
    "total_current_assets": I(331339.1, FS26H1, "2026-06-30", "A"),
    "total_assets":       I(477897.9, FS26H1, "2026-06-30", "A"),
    "paid_capital":       I(20606.5,  FS26H1, "2026-06-30", "A"),
    "retained_earnings":  I(65680.9,  FS26H1, "2026-06-30", "A"),
    "equity_parent":      I(91670.9,  FS26H1, "2026-06-30", "A"),
    "nci_equity":         I(75652.8,  FS26H1, "2026-06-30", "A"),
    "total_equity":       I(167323.6, FS26H1, "2026-06-30", "A"),
    "other_noncurrent_liab": I(51439.9, FS26H1, "2026-06-30", "A"),
    "loans_noncurrent":   I(13813.5,  FS26H1, "2026-06-30", "A"),
    "lease_noncurrent":   I(271.7,    FS26H1, "2026-06-30", "A"),
    "deferred_tax_liab":  I(3239.6,   FS26H1, "2026-06-30", "A"),
    "total_noncurrent_liab": I(68764.8, FS26H1, "2026-06-30", "A"),
    "credit_facilities":  I(1661.6,   FS26H1, "2026-06-30", "A"),
    "loans_current":      I(1017.9,   FS26H1, "2026-06-30", "A"),
    "lease_current":      I(242.2,    FS26H1, "2026-06-30", "A"),
    "suppliers_contractors": I(45167.2, FS26H1, "2026-06-30", "A"),
    "customer_advances":  I(133993.1, FS26H1, "2026-06-30", "A"),
    "obligations_nr_undelivered": I(13769.5, FS26H1, "2026-06-30", "A"),
    "dividends_payable":  I(376.6,    FS26H1, "2026-06-30", "A"),
    "provisions":         I(1145.8,   FS26H1, "2026-06-30", "A"),
    "creditors_other":    I(41920.8,  FS26H1, "2026-06-30", "A"),
    "tax_payable":        I(2514.8,   FS26H1, "2026-06-30", "A"),
    "total_current_liab": I(241809.5, FS26H1, "2026-06-30", "A"),
    "total_liabilities":  I(310574.2, FS26H1, "2026-06-30", "A"),
    "postdated_cheques_offbs": I(210448.8, FS26H1 + " (note 18/3)", "2026-06-30", "A",
                                 note="post-dated cheques for sold and undelivered "
                                      "units, deliberately NOT on the balance sheet"),
    # FY2025 comparatives, used for the three-year history and the roll-forward
    "cash_fy25":          I(44846.5,  FS25, "2025-12-31", "A"),
    "deposits_current_fy25": I(20085.6, FS25, "2025-12-31", "A"),
    "deposits_noncurrent_fy25": I(8978.1, FS25, "2025-12-31", "A"),
    "loans_noncurrent_fy25": I(9737.7, FS25, "2025-12-31", "A"),
    "loans_current_fy25": I(791.1,    FS25, "2025-12-31", "A"),
    "credit_facilities_fy25": I(1273.4, FS25, "2025-12-31", "A"),
    "customer_advances_fy25": I(117676.2, FS25, "2025-12-31", "A"),
    "properties_under_development_fy25": I(130058.9, FS25, "2025-12-31", "A"),
    "equity_parent_fy25": I(81047.6,  FS25, "2025-12-31", "A"),
    "nci_equity_fy25":    I(76660.6,  FS25, "2025-12-31", "A"),
    "total_equity_fy25":  I(157708.1, FS25, "2025-12-31", "A"),
    "total_assets_fy25":  I(436222.2, FS25, "2025-12-31", "A"),
}

# Operating KPIs — the company's own disclosures.
KPI = {
    "backlog_jun26":      I(491000.0, ER26H1, "2026-06-30", "A",
                            note="sold but not yet recognised"),
    "backlog_mar26":      I(457900.0, ER26H1, "2026-03-31", "A"),
    "backlog_jun25":      I(363800.0, ER26H1, "2025-06-30", "A"),
    "backlog_fy25":       I(441200.0, ER25, "2025-12-31", "A"),
    "contracted_sales_h1_26": I(219100.0, ER26H1, "2026-06-30", "A"),
    "contracted_sales_q2_26": I(170100.0, ER26H1, "2026-06-30", "A"),
    "contracted_sales_fy25": I(382200.0, ER25, "2025-12-31", "A"),
    "contracted_sales_fy24": I(504000.0, "TMG Holding FY2024 earnings release, via " + IR,
                               "2024-12-31", "A"),
    "landbank_msqm":      I(20.0, ER26H1, "2026-06-30", "A", unit="mn sqm",
                            note="stated as 'c.20 mn sqm' on the release's own "
                                 "indicator panel"),
    "hotel_keys_operating": I(3500.0, ER26H1, "2026-06-30", "A", unit="keys",
                              note="stated as 'c.3,500'"),
    "hotel_keys_under_construction": I(1500.0, ER26H1, "2026-06-30", "A", unit="keys"),
    "hotel_arr_h1_26":    I(13209.0, ER26H1, "2026-06-30", "A", unit="EGP/room-night"),
    "hospitality_ebitda_h1_26": I(3900.0, ER26H1, "2026-06-30", "A"),
    "hospitality_ebitda_margin_h1_26": I(0.519, ER26H1, "2026-06-30", "A", unit="fraction"),
    "southmed_cumulative_sales": I(500000.0, ER26H1, "2026-06-30", "A",
                                   note="since launch to 30 June 2026"),
    "spine_sales_since_launch": I(33800.0, ER26H1, "2026-06-30", "A",
                                  note="launched April 2026"),
    "banan_share_of_re_revenue_h1_26": I(0.525, ER26H1, "2026-06-30", "A", unit="fraction",
                                         note="the percentage-of-completion leg"),
    "units_delivered_fy25": I(3196.0, ER25, "2025-12-31", "A", unit="units"),
    "shares_outstanding": I(2060.6538, FS25, "2025-12-31", "A", unit="mn shares",
                            note="paid-up capital EGP 20,606,537,860 at EGP 10 par. "
                                 "Cross-checks: FY2025 attributable profit 14,383.9 / "
                                 "EPS 6.98 = 2,060.7mn"),
}

# GAPS — recorded, never filled.
GAPS = {
    "unit_economics": I(None, "TMG Holding results releases and statements", "2026-08-12",
                        "A", unit="n/a",
                        gap="TMG publishes unit counts only occasionally (3,196 delivered "
                            "in FY2025; 6,102 units sold in FY2022) and never as a "
                            "continuous series, and publishes no average unit area, price "
                            "per sqm or construction cost per sqm. Unit economics cannot be "
                            "built without inventing them. WHAT WOULD CLOSE IT: a "
                            "disclosure of units sold and delivered by project with average "
                            "areas, as several regional peers publish."),
    "finance_cost_split": I(None, FS25 + " note 37", "2025-12-31", "A", unit="n/a",
                            gap="Finance cost is disclosed as finance expenses plus bank "
                                "charges, with no split between interest on borrowings and "
                                "the unwinding of the significant financing component on "
                                "customer contracts. The implied 44% on opening "
                                "interest-bearing debt is therefore not a borrowing rate. "
                                "WHAT WOULD CLOSE IT: the split, or a disclosed weighted "
                                "average borrowing rate."),
    "segment_capex": I(None, FS25, "2025-12-31", "A", unit="n/a",
                       gap="Capital expenditure is not disclosed by segment, so the "
                           "hospitality build programme cannot be separated from the "
                           "development one. WHAT WOULD CLOSE IT: a segment note carrying "
                           "additions to fixed assets and assets under construction."),
    "banan_economics": I(None, FS25 + "; " + ER26H1, "2026-08-12", "A", unit="n/a",
                         gap="The Saudi project's contract value, cost to complete and "
                             "margin are not disclosed separately, only its share of "
                             "segment revenue. WHAT WOULD CLOSE IT: a geographic segment "
                             "note."),
}
