"""PHDC valuation inputs — every figure with value, source, date, provenance tier.

Tier A = the company's own audited statements or its own IR documents.
Tier C = credible third party (used only for exogenous macro and market prices).

No financial numeral is typed into a builder anywhere else in this study; the
builders read this registry. Anything not disclosed is recorded here as a GAP
with what would close it, never filled with an estimate that reads like a fact.
"""
IR = "https://ir.palmhillsdevelopments.com/en-us/financial/resultcenter"


def I(value, source, date, tier, unit="EGP mn", gap=None):
    return {"value": value, "source": source, "date": date, "tier": tier,
            "unit": unit, **({"gap": gap} if gap else {})}


# ---------------------------------------------------------------------------
# FY2025 audited results — read from the consolidated statements, which foot:
# total assets 172,129.8 = total liabilities 153,364.1 + total equity 18,765.8
FS25 = "PHD consolidated financial statements FY2025 (31 Dec 2025), via " + IR
ER26Q1 = "PHD 1Q2026 earnings release, 20 May 2026, via " + IR

ACTUALS = {
    "revenue_fy25":        I(36169.3, FS25, "2025-12-31", "A"),
    "cogs_fy25":           I(21118.9, FS25, "2025-12-31", "A"),
    "gross_profit_fy25":   I(14887.6, FS25, "2025-12-31", "A"),
    "sga_fy25":            I(6365.6,  FS25, "2025-12-31", "A"),
    "da_fy25":             I(353.7,   FS25, "2025-12-31", "A"),
    "finance_cost_fy25":   I(3347.5,  FS25, "2025-12-31", "A"),
    "npbt_fy25":           I(6251.1,  FS25, "2025-12-31", "A"),
    "tax_fy25":            I(1827.2,  FS25, "2025-12-31", "A"),
    "npat_mi_fy25":        I(4216.7,  FS25, "2025-12-31", "A"),
    "revenue_fy24":        I(27167.3, FS25 + " (comparative column)", "2024-12-31", "A"),
    # Cash-flow statement, FY2025 filing. Closing cash ties to the balance sheet.
    "cfo_fy25":            I(1424.2,  FS25 + " (statement of cash flows)", "2025-12-31", "A"),
    "cfi_fy25":            I(-4031.7, FS25 + " (statement of cash flows)", "2025-12-31", "A"),
    "cff_fy25":            I(5628.8,  FS25 + " (statement of cash flows)", "2025-12-31", "A"),
    "cfo_fy24":            I(4854.8,  FS25 + " (statement of cash flows, comparative) "
                            "— NOTE this RESTATES the EGP 3,131.9mn the FY2024 results "
                            "release reported for the same year; the filing is used",
                            "2024-12-31", "A"),
    "cfo_fy23":            I(756.7,   "PHD FY2024 earnings release (comparative)",
                            "2023-12-31", "A"),
    "revenue_fy23":        I(17462.1, "PHD FY2023 consolidated financial statements",
                            "2023-12-31", "A"),
    "cogs_fy24":           I(17837.2, "PHD FY2024 earnings release", "2024-12-31", "A"),
}

BALANCE_SHEET_FY25 = {
    "total_assets":        I(172129.8, FS25, "2025-12-31", "A"),
    "total_liabilities":   I(153364.1, FS25, "2025-12-31", "A"),
    "total_equity":        I(18765.8,  FS25, "2025-12-31", "A"),
    "equity_parent":       I(17431.4,  FS25, "2025-12-31", "A"),
    "nci_equity":          I(1334.3,   FS25, "2025-12-31", "A"),
    "cash":                I(9419.5,   FS25, "2025-12-31", "A"),
    "work_in_progress":    I(17570.9,  FS25, "2025-12-31", "A"),
    "accounts_receivable": I(28118.1,  FS25, "2025-12-31", "A"),
    "notes_recv_st":       I(18137.7,  FS25, "2025-12-31", "A"),
    "notes_recv_lt":       I(54801.3,  FS25, "2025-12-31", "A"),
    "notes_recv_st_undel": I(935.3,    FS25, "2025-12-31", "A"),
    "notes_recv_lt_undel": I(1518.5,   FS25, "2025-12-31", "A"),
    "advances_customers":  I(69354.1,  FS25, "2025-12-31", "A"),
    "suppliers":           I(3807.0,   FS25, "2025-12-31", "A"),
    "investments_assoc":   I(3611.6,   FS25, "2025-12-31", "A"),
    "investment_property": I(1032.5,   FS25, "2025-12-31", "A"),
    "fixed_assets":        I(4522.0,   FS25, "2025-12-31", "A"),
    "fin_inv_amortised":   I(9581.5,   FS25, "2025-12-31", "A"),
    "debtors_other":       I(12922.0,  FS25, "2025-12-31", "A"),
    "due_from_related":    I(335.7,    FS25, "2025-12-31", "A"),
    "inv_fair_value":      I(152.7,    FS25, "2025-12-31", "A"),
    "suppliers_advances":  I(9056.2,   FS25, "2025-12-31", "A"),
    "total_noncurrent_assets": I(65900.2, FS25, "2025-12-31", "A"),
    "total_current_assets":    I(106229.6, FS25, "2025-12-31", "A"),
    "deferred_revenue":    I(731.2,    FS25, "2025-12-31", "A"),
    "checks_undelivered":  I(2453.7,   FS25, "2025-12-31", "A"),
    "creditors_other":     I(5121.7,   FS25, "2025-12-31", "A"),
}

# FY2024 comparatives, same page, used only to MEASURE the working-capital cycle
BALANCE_SHEET_FY24 = {
    "work_in_progress":    I(13209.8, FS25 + " (comparative)", "2024-12-31", "A"),
    "accounts_receivable": I(15561.1, FS25 + " (comparative)", "2024-12-31", "A"),
    "notes_recv_lt":       I(43213.4, FS25 + " (comparative)", "2024-12-31", "A"),
    "notes_recv_lt_undel": I(3095.7,  FS25 + " (comparative)", "2024-12-31", "A"),
    "notes_recv_st":       I(13429.8, FS25 + " (comparative)", "2024-12-31", "A"),
    "notes_recv_st_undel": I(1718.6,  FS25 + " (comparative)", "2024-12-31", "A"),
    "debtors_other":       I(7541.5,  FS25 + " (comparative)", "2024-12-31", "A"),
    "suppliers_advances":  I(4791.0,  FS25 + " (comparative)", "2024-12-31", "A"),
    "advances_customers":  I(47403.8, FS25 + " (comparative)", "2024-12-31", "A"),
    "suppliers":           I(3426.7,  FS25 + " (comparative)", "2024-12-31", "A"),
    "creditors_other":     I(4677.3,  FS25 + " (comparative)", "2024-12-31", "A"),
    "checks_undelivered":  I(4814.3,  FS25 + " (comparative)", "2024-12-31", "A"),
}

# interest-bearing debt, itemised from the same balance sheet
DEBT_FY25 = {
    "loans_long_term":              I(10543.1, FS25, "2025-12-31", "A"),
    "notes_payable_long_term":      I(4505.0,  FS25, "2025-12-31", "A"),
    "credit_facilities":            I(11337.5, FS25, "2025-12-31", "A"),
    "banks_credit_balances":        I(938.8,   FS25, "2025-12-31", "A"),
    "current_portion_st_loans":     I(1250.0,  FS25, "2025-12-31", "A"),
    "notes_payable_short_term":     I(4875.7,  FS25, "2025-12-31", "A"),
    "lease_liabilities_lt":         I(60.7,    FS25, "2025-12-31", "A"),
    "lease_liabilities_st":         I(41.9,    FS25, "2025-12-31", "A"),
}

# ---------------------------------------------------------------------------
# Operating drivers. These come from the results releases, because no financial
# statement carries units, prices or backlog.
OPERATING = {
    "backlog_1q26":     I(263000.0, ER26Q1 + " — \"the company's backlog of units sold "
                          "and not yet delivered reached EGP263 billion up from EGP190 "
                          "billion in 1Q2025\"", "2026-03-31", "A"),
    "backlog_fy24":     I(147000.0, "PHD FY2024 earnings release", "2024-12-31", "A"),
    "backlog_fy23":     I(60000.0,  "PHD FY2024 earnings release (comparative)",
                          "2023-12-31", "A"),
    "new_sales_1q26":   I(52000.0,  ER26Q1 + " — \"New sales recorded EGP 52 billion in "
                          "1Q2026\"", "2026-03-31", "A"),
    "new_sales_fy24":   I(151016.0, "PHD FY2024 earnings release, chart series",
                          "2024-12-31", "A"),
    "vdlc_launch_1q26": I(24000.0,  ER26Q1 + " — \"the company launched its strategic "
                          "land plot Village de La Capitale in New administrative "
                          "Capital with total sales of EGP24 billion\"",
                          "2026-03-31", "A"),
    "revenue_1q26":     I(9300.0,   ER26Q1, "2026-03-31", "A"),
    "gross_profit_1q26": I(3300.0,  ER26Q1 + " — margin 35% versus 44% in 1Q2025",
                           "2026-03-31", "A"),
    "npat_1q26":        I(1200.0,   ER26Q1, "2026-03-31", "A"),
    "construction_fy24": I(8500.0,  "PHD FY2024 earnings release — \"The Company spent "
                           "EGP8.5 billion on construction activities during FY2024\"",
                           "2024-12-31", "A"),
    "construction_fy23": I(7500.0,  "PHD FY2023 earnings release", "2023-12-31", "A"),
    "collections_fy24": I(25400.0,  "PHD FY2024 earnings release", "2024-12-31", "A"),
    "land_bank_sqm_mn": I(33.0,     "PHD FY2024 earnings release — land bank \"spreading "
                          "over 33 million square meters\"", "2024-12-31", "A",
                          unit="mn sqm"),
    "units_delivered_fy23": I(1500.0, "PHD FY2023 earnings release", "2023-12-31", "A",
                              unit="units"),
    "units_sold_fy23":  I(5300.0,   "PHD FY2023 earnings release, chart series",
                          "2023-12-31", "A", unit="units"),
}

# ---------------------------------------------------------------------------
# Market data
MARKET = {
    "shares_outstanding_bn": I(2.85992, "Share capital per FY2025 balance sheet and the "
                               "share count carried on the covered-name record",
                               "2025-12-31", "A", unit="bn shares"),
    "spot":                  I(15.20, "EGX close 23 Aug 2026, engine/raw_ohlc/EG/PHDC.csv",
                               "2026-08-23", "B", unit="EGP/share"),
}

# ---------------------------------------------------------------------------
# GAPS — disclosed nowhere, and therefore NOT filled. Each names what closes it.
GAPS = {
    "fy2025_results_release": "PHD has published FY2025 consolidated statements but NO "
        "FY2025 full-year results release. The release is where units sold, new sales, "
        "deliveries and construction spend are disclosed, so FY2025 has audited "
        "financials and NO operating drivers. Closed by: the FY2025 release, or the "
        "company confirming the figures directly.",
    "h1_2026_results": "As at this build date (30-Aug-2026) no 2Q/H1-2026 statements or "
        "release are posted to the result centre; the newest disclosure of any kind is "
        "1Q2026 (posted 25-Jun-2026). The study's information set therefore ends at "
        "1Q2026. Closed by: the H1-2026 filing.",
    "securitisation_pricing": "The EGP 2.015bn securitisation of 4-Feb-2026 discloses "
        "tranche sizes, tenors and national-scale ratings but NO coupon on any tranche, "
        "so the company's own marginal cost of debt cannot be read. Closed by: the "
        "offering circular or a disclosed coupon.",
    "per_project_pricing": "The company does not disclose per-project unit mix, average "
        "unit area, price per square metre or construction cost per square metre. The "
        "11-Jun-2026 edition carried a full per-project table of those figures; they are "
        "NOT sourced to any company document. This study does not reuse them. Closed by: "
        "an investor presentation or project-level disclosure carrying unit economics.",
    "backlog_cost_to_complete": "Remaining construction cost against the EGP 263bn "
        "backlog is not disclosed as a single figure. It is inferred in the model from "
        "the realised gross margin and flagged where used.",
}


# ---------------------------------------------------------------------------
def assert_balance_sheet_foots():
    """The parse is accepted only if the statement's own subtotals reconcile.

    Both routes through the scan get individual rows wrong in different places —
    at 300 dpi notes receivable long term read 801.3 against a true 54,801.3, and
    at 400 dpi fixed assets read 5.0 against a true 4,522.0. Neither resolution
    is trustworthy on its own, so the arbiter is arithmetic: every component
    list must sum to the subtotal the company printed beside it.
    """
    b = BALANCE_SHEET_FY25
    nc = (b["investments_assoc"]["value"] + b["investment_property"]["value"]
          + b["fixed_assets"]["value"] + 182.6 + 26.9 + 101.5 + 102.5
          + b["notes_recv_lt"]["value"] + b["notes_recv_lt_undel"]["value"] + 0.7)
    assert abs(nc - b["total_noncurrent_assets"]["value"]) < 1.0, (
        "non-current assets do not foot: components %.1f vs stated %.1f"
        % (nc, b["total_noncurrent_assets"]["value"]))
    ca = (b["work_in_progress"]["value"] + b["accounts_receivable"]["value"]
          + b["debtors_other"]["value"] + b["suppliers_advances"]["value"]
          + b["due_from_related"]["value"] + b["fin_inv_amortised"]["value"]
          + b["inv_fair_value"]["value"] + b["notes_recv_st"]["value"]
          + b["notes_recv_st_undel"]["value"] + b["cash"]["value"])
    assert abs(ca - b["total_current_assets"]["value"]) < 1.0, (
        "current assets do not foot: components %.1f vs stated %.1f"
        % (ca, b["total_current_assets"]["value"]))
    assert abs(b["total_assets"]["value"]
               - (b["total_liabilities"]["value"] + b["total_equity"]["value"])) < 1.0
    return {"non_current_assets": round(nc, 1), "current_assets": round(ca, 1)}
