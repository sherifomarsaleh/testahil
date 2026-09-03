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
    "cash":                I(6372.4,  FS25 + " (comparative)", "2024-12-31", "A"),
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
    "revenue_1q26_yoy": I(0.11,    ER26Q1 + " — \"Revenue reached EGP 9.3 billion in "
                          "1Q2026, up 11% YoY\"", "2026-03-31", "A", unit="YoY"),
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
    "spot":                  I(14.40, "Egyptian Exchange closing price for PHDC, 3 September 2026. The previous edition was struck on the 23 August close of 15.20; no study in this series is delivered against a stale price, because a fair value published beside a month-old quote is a comparison a reader cannot use",
                               "2026-08-23", "B", unit="EGP/share"),
}

# ---------------------------------------------------------------------------
# GAPS — disclosed nowhere, and therefore NOT filled. Each names what closes it.
GAPS = {
    "cash_flow_statement_detail": (
        "The FY2025 cash-flow statement is published in its three totals only "
        "(operating EGP 1,424.2mn, investing EGP -4,031.7mn, financing "
        "EGP 5,628.8mn); no line-by-line statement is posted. Working capital "
        "on the two audited balance sheets rose EGP 20,084.7mn in 2025 while "
        "net profit plus depreciation less operating cash implies a rise of "
        "EGP 3,146.2mn — a wedge of EGP 16,938.5mn, 46.8% of revenue, which "
        "CANNOT be decomposed from what is disclosed and is therefore not "
        "decomposed. It is why the projection is published in two framings "
        "rather than one. Closed by: the full FY2025 cash-flow statement."),
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
# The LATEST disclosed balance sheet — 31 March 2026, reviewed — registered from
# bs_1q2026.json, the four-field record the [R-GAP-01] review of 01-Sep-2026
# read off the company's own interim statements (a scan; OCR at 300dpi, every
# subtotal held to the statement's own arithmetic). The bridge, the book lens and
# the debt stack stand on THIS sheet [GAP_REVIEW_01-09-2026 heading 6]; the
# projected statements keep FY2025 as their audited base year, because a
# working-capital cycle measured on full years is not restarted from a quarter.
import json as _json, os as _os
_BS26 = _json.load(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)),
                                     "bs_1q2026.json")))
BRIDGE_BS_DATE = _BS26["as_of"]
BALANCE_SHEET_1Q26 = {k: {"value": r["value"], "source": r["source"], "date": r["date"],
                          "tier": r["tier"], "unit": r.get("unit", "EGP mn"),
                          **({"note": r["note"]} if r.get("note") else {})}
                      for k, r in _BS26["lines"].items()}
# the same eight interest-bearing lines the FY2025 debt stack is built on, so the
# two dates are compared like for like (the review reproduced FY2025 gross debt
# of 33,552.7 from exactly these lines)
DEBT_LINES = ["loans_long_term", "notes_payable_long_term", "credit_facilities",
              "banks_credit_balances", "current_portion_st_loans",
              "notes_payable_short_term", "lease_liabilities_lt", "lease_liabilities_st"]
assert set(DEBT_LINES) == set(DEBT_FY25), "the FY2025 debt stack and DEBT_LINES have drifted apart"


def assert_balance_sheet_1q26_foots():
    """The 31-Mar-2026 parse is accepted only if the statement's own subtotals
    reconcile: assets = liabilities + equity, parent equity + NCI = total equity,
    and each side's subtotals sum to the totals printed beside them."""
    q = {k: r["value"] for k, r in BALANCE_SHEET_1Q26.items()}
    assert abs(q["total_assets"] - (q["total_liabilities"] + q["total_equity"])) < 0.5, "1Q26: A != L + E"
    assert abs(q["total_noncurrent_assets"] + q["total_current_assets"] - q["total_assets"]) < 0.5
    assert abs(q["total_noncurrent_liabs"] + q["total_current_liabs"] - q["total_liabilities"]) < 0.5
    assert abs(q["equity_parent"] + q["nci_equity"] - q["total_equity"]) < 0.5, "1Q26: parent + NCI != equity"
    ca = sum(q[k] for k in ("work_in_progress", "accounts_receivable", "debtors_other",
                            "suppliers_advances", "due_from_related", "fin_inv_amortised",
                            "inv_fair_value", "notes_recv_st", "notes_recv_st_undel", "cash"))
    assert abs(ca - q["total_current_assets"]) < 0.5, "1Q26 current assets do not foot: %.3f vs %.3f" % (ca, q["total_current_assets"])
    for k in DEBT_LINES:
        assert k in q, "1Q26 sheet lacks debt line %s" % k
    return {"gross_debt": round(sum(q[k] for k in DEBT_LINES), 3), "cash": q["cash"],
            "net_debt": round(sum(q[k] for k in DEBT_LINES) - q["cash"], 3)}


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

# ---------------------------------------------------------------------------
# The reported income statement, three years, so Appendix A carries no numeral
# typed into a builder. FY2023 and FY2024 are read from the FY2024 statements;
# FY2025 from the FY2024 comparative in the FY2025 statements. Cost of revenue
# is shown on its own line and the cash discount separately, because the
# company reports gross profit after both: revenue less cost of revenue less
# cash discount foots to reported gross profit in all three years.
FS23 = "PHD consolidated financial statements FY2023 (31 Dec 2023), via " + IR
FS24 = "PHD consolidated financial statements FY2024 (31 Dec 2024), via " + IR

HISTORICAL_IS = {
    "2023": {
        "revenue":        I(17462.1, FS23, "2023-12-31", "A"),
        "cogs":           I(11907.2, FS23, "2023-12-31", "A"),
        "cash_discount":  I(47.2,    FS23, "2023-12-31", "A"),
        "gross_profit":   I(5507.6,  FS23, "2023-12-31", "A"),
        "sga":            I(2060.5,  FS23, "2023-12-31", "A"),
        "da":             I(178.6,   FS23, "2023-12-31", "A"),
        "npbt":           I(2300.7,  FS23, "2023-12-31", "A"),
        "tax_total":      I(567.3,   FS23, "2023-12-31", "A"),
        "npat_pre_nci":   I(1733.4,  FS23, "2023-12-31", "A"),
        "nci":            I(151.9,   FS23, "2023-12-31", "A"),
        "npat_mi":        I(1581.5,  FS23, "2023-12-31", "A"),
    },
    "2024": {
        "revenue":        I(27167.3, FS24, "2024-12-31", "A"),
        "cogs":           I(17739.9, FS24, "2024-12-31", "A"),
        "cash_discount":  I(97.3,    FS24, "2024-12-31", "A"),
        "gross_profit":   I(9330.1,  FS24, "2024-12-31", "A"),
        "sga":            I(3435.8,  FS24, "2024-12-31", "A"),
        "da":             I(239.9,   FS24, "2024-12-31", "A"),
        "finance_cost":   I(2311.4,  FS24, "2024-12-31", "A"),
        "npbt":           I(4320.6,  FS24, "2024-12-31", "A"),
        "tax_total":      I(917.1,   FS24, "2024-12-31", "A"),
        "npat_pre_nci":   I(3403.5,  FS24, "2024-12-31", "A"),
        "nci":            I(148.5,   FS24, "2024-12-31", "A"),
        "npat_mi":        I(3254.9,  FS24, "2024-12-31", "A"),
    },
    "2025": {
        "revenue":        I(36169.3, FS25, "2025-12-31", "A"),
        "cogs":           I(21118.9, FS25, "2025-12-31", "A"),
        "cash_discount":  I(162.8,   FS25, "2025-12-31", "A"),
        "gross_profit":   I(14887.6, FS25, "2025-12-31", "A"),
        "sga":            I(6365.6,  FS25, "2025-12-31", "A"),
        "da":             I(353.7,   FS25, "2025-12-31", "A"),
        "finance_cost":   I(3347.5,  FS25, "2025-12-31", "A"),
        "npbt":           I(6251.1,  FS25, "2025-12-31", "A"),
        "tax_total":      I(1827.2,  FS25, "2025-12-31", "A"),
        "npat_pre_nci":   I(4423.8,  FS25, "2025-12-31", "A"),
        "nci":            I(207.2,   FS25, "2025-12-31", "A"),
        "npat_mi":        I(4216.7,  FS25, "2025-12-31", "A"),
    },
}

# FY2024 cost of revenue is EGP 17,739.9mn as the company reported it for that
# year and EGP 17,837.2mn in the FY2025 comparative column — a restatement of
# EGP 97.3mn, equal to that year's cash discount, which the FY2025 presentation
# folds into cost. The forecast model is built on the FY2025-comparative basis
# throughout; the appendix shows each year as that year's statements reported
# it. Both figures are correct on their own basis and neither is an error.
FY24_COGS_AS_REPORTED = 17739.9
FY24_COGS_FY25_BASIS = 17837.2

# The reported balance-sheet subtotals, both years, on the FY2025 presentation.
BALANCE_SHEET_SUBTOTALS = {
    "2025": {
        "total_noncurrent_assets": I(65900.2, FS25, "2025-12-31", "A"),
        "total_current_assets":    I(106229.6, FS25, "2025-12-31", "A"),
        "total_assets":            I(172129.8, FS25, "2025-12-31", "A"),
        "total_current_liabs":     I(105099.0, FS25, "2025-12-31", "A"),
        "total_noncurrent_liabs":  I(48265.1, FS25, "2025-12-31", "A"),
        "total_liabilities":       I(153364.1, FS25, "2025-12-31", "A"),
        "total_equity":            I(18765.8, FS25, "2025-12-31", "A"),
    },
    "2024": {
        "total_noncurrent_assets": I(54166.4, FS25 + " (comparative)",
                                     "2024-12-31", "A"),
        "total_current_assets":    I(69270.9, FS25 + " (comparative)",
                                     "2024-12-31", "A"),
        "total_assets":            I(123437.3, FS25 + " (comparative)",
                                     "2024-12-31", "A"),
        "total_current_liabs":     I(74496.9, FS25 + " (comparative)",
                                     "2024-12-31", "A"),
        "total_noncurrent_liabs":  I(34315.7, FS25 + " (comparative)",
                                     "2024-12-31", "A"),
        "total_liabilities":       I(108812.6, FS25 + " (comparative)",
                                     "2024-12-31", "A"),
        "total_equity":            I(14624.7, FS25 + " (comparative)",
                                     "2024-12-31", "A"),
    },
}


def assert_historicals_foot():
    """Each reported year must foot on its own lines, or it is not usable."""
    out = []
    for y, d in HISTORICAL_IS.items():
        g = d["revenue"]["value"] - d["cogs"]["value"] - d["cash_discount"]["value"]
        assert abs(g - d["gross_profit"]["value"]) < 0.2, (y, g)
        n = d["npbt"]["value"] - d["tax_total"]["value"]
        assert abs(n - d["npat_pre_nci"]["value"]) < 0.2, (y, n)
        m = d["npat_pre_nci"]["value"] - d["nci"]["value"]
        assert abs(m - d["npat_mi"]["value"]) < 0.2, (y, m)
        out.append((y, "gross profit, profit after tax and minority all foot"))
    for y, d in BALANCE_SHEET_SUBTOTALS.items():
        a = d["total_noncurrent_assets"]["value"] + d["total_current_assets"]["value"]
        assert abs(a - d["total_assets"]["value"]) < 0.2, (y, a)
        l = d["total_current_liabs"]["value"] + d["total_noncurrent_liabs"]["value"]
        assert abs(l - d["total_liabilities"]["value"]) < 0.2, (y, l)
        e = d["total_liabilities"]["value"] + d["total_equity"]["value"]
        assert abs(e - d["total_assets"]["value"]) < 0.2, (y, e)
        out.append((y, "assets, liabilities and equity all foot"))
    return out
