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
    # TESTED AGAINST THE NEWER DISCLOSURE ON 10-09-2026 AND IT IS WORTH NOTHING.
    # A half-year release of 18 August 2026 puts the backlog at EGP 284bn at 30 June,
    # 40% up on the year, and a further EGP 75bn was sold at Hacienda Ras El Hekma in
    # the fortnight after that. Swapping 263,000 for 284,000 and rebuilding moves the
    # central by ZERO: 21.0897 either way. That is not a defect in the test, it is this
    # model's central claim arriving as a measurement — revenue here is limited by how
    # fast this company can DELIVER, never by how much it has sold, and the book is
    # already further ahead of the build programme than the programme can close.
    # SO THE ANCHOR STAYS ON THE COMPANY'S OWN QUARTERLY RELEASE rather than moving to
    # a wire report of a release this study has not read. Swapping a company-sourced
    # figure for a secondary one buys nothing when the number changes nothing.
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
    # EXACT, FROM THE RELEASE'S OWN INCOME STATEMENT, NOT ITS HEADLINE [17-09-2026].
    # Every 1Q2026 figure below was carried at the rounded billions the bullet points
    # print — 9,300 / 3,300 / 1,200 / "up 11%" — while page 8 of the same release prints
    # the statement in thousands. The rounding is not cosmetic: 9,300 understates the
    # quarter by 0.49%, and because FY2026 is anchored on that quarter divided by 1Q2025's
    # share of FY2025, the error compounds through all fifteen forecast years. A margin
    # taken as 3.3/9.3 = 35.4839% likewise is not the margin: 3,309,973/9,346,133 is
    # 35.4171%. THE HEADLINE IS A SUMMARY OF THE STATEMENT AND NEVER A SUBSTITUTE FOR IT.
    "revenue_1q26":     I(9346.133,  ER26Q1 + " — Consolidated Income Statement, "
                          "\"Revenue 9,346,133\" EGP thousand", "2026-03-31", "A"),
    "revenue_1q25":     I(8392.553,  ER26Q1 + " — Consolidated Income Statement, "
                          "prior-year column, \"Revenue 8,392,553\" EGP thousand. The "
                          "prior-year quarter is DISCLOSED, so the FY2026 anchor no longer "
                          "derives it from a rounded YoY percentage", "2025-03-31", "A"),
    "gross_profit_1q26": I(3309.973, ER26Q1 + " — Consolidated Income Statement, "
                           "\"Gross Profit 3,309,973\" EGP thousand (the release's own "
                           "headline rounds the margin to 35% versus 45% in 1Q2025)",
                           "2026-03-31", "A"),
    "cost_of_revenue_1q26": I(6036.161, ER26Q1 + " — Consolidated Income Statement, "
                              "\"Cost of Revenue (6,036,161)\" EGP thousand",
                              "2026-03-31", "A"),
    # THE QUARTERLY CASH CONVERSION, NEWLY CONSUMED [17-09-2026]. The release publishes a
    # cash-flow statement in three totals, and 1Q2026 operating cash of 1,766,705 over
    # revenue of 9,346,133 is 18.90% — far above the three full-year rates. It is NOT the
    # forecast anchor and the reason is the study's own: a quarter is not a year for a
    # company whose collections and construction both swing with which project completes,
    # and 1Q2025's own 12.07% against FY2025's 3.94% measures that seasonality directly.
    # Recorded and reported so the reader sees the newest observation and why it is not used.
    "cfo_1q26":         I(1766.705,  ER26Q1 + " — Consolidated Cash Flow Statement, "
                          "\"Cash Flows from Operating Activities 1,766,705\" EGP thousand",
                          "2026-03-31", "A"),
    "cfo_1q25":         I(1013.148,  ER26Q1 + " — Consolidated Cash Flow Statement, "
                          "prior-year column, \"1,013,148\" EGP thousand", "2025-03-31", "A"),
    "revenue_1q26_yoy": I(0.11,    ER26Q1 + " — \"Revenue reached EGP 9.3 billion in "
                          "1Q2026, up 11% YoY\"", "2026-03-31", "A", unit="YoY"),
    "npat_1q26":        I(1205.253, ER26Q1 + " — Consolidated Income Statement, \"Net "
                          "Profit After Tax & Minority Interest 1,205,253\" EGP thousand",
                          "2026-03-31", "A"),
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
    # THE COMPANY'S OWN FY2026 HANDOVER DISCLOSURE, REGISTERED RATHER THAN PASSED OVER
    # [17-09-2026]. The forecast's 2026 delivery count is IMPLIED from the disclosed
    # revenue anchor divided by the escalated price per unit, and the company separately
    # publishes a figure for the same year. The two are not the same measure — "ready to
    # be handed over" is inventory available, not deliveries booked, and the identical
    # 1,200 appears in the 3Q2025 release for end-9M2025, so the company is repeating it
    # rather than updating it — but a study that anchors on deliveries owes the reader the
    # company's own number and the reason it is not the anchor. Registered so it prints.
    "units_rtm_fy26":   I(1200.0,   ER26Q1 + " — Operational Review, \"A total of 1,200 "
                          "contractual units were ready to be handed over in FY2026\"",
                          "2026-03-31", "A", unit="units"),
    "units_delivered_fy24": I(2000.0, "PHD 4Q2024 earnings release — \"handed over units "
                              "exceeding c. 2,000 units during the period\". The count is "
                              "DISCLOSED, approximately, and the register previously said "
                              "FY2024 unit counts were absent; corrected 17-09-2026",
                              "2024-12-31", "A", unit="units"),
    "units_rtm_fy24":   I(111.0,    "PHD 4Q2024 earnings release — \"Ready-to-Move "
                          "inventory reached EGP3.5 billion, representing 111 units "
                          "across all regions\"", "2024-12-31", "A", unit="units"),
    # FY2025 REGIONAL NEW SALES — DISCLOSED ON A PAGE THIS STUDY ALREADY CITES, AND THE
    # YEAR THE STUDY'S OWN RECONCILIATION BREAKS ON [17-09-2026]. The 1Q2026 release
    # charts new sales by region for 2023, 2024, 2025, 1Q2025 and 1Q2026. The study's
    # integrity check — the three regions summing to the all-regions figure the same
    # release prints — holds EXACTLY in 2024 (151,016) and 1Q2026 (52,059) and BREAKS in
    # FY2025: 88,337 + 20,751 + 54,904 = 163,992 against 215,384, a gap of 51,392mn
    # (23.9%) attributed to no charted region. The check is kept and the break is
    # published; a check that is only run on the years it passes is not a check.
    "new_sales_fy25_west":  I(88337.0, ER26Q1 + " — West Cairo & Badya chart, 2025",
                              "2025-12-31", "A"),
    "new_sales_fy25_east":  I(20751.0, ER26Q1 + " — East Cairo chart, 2025",
                              "2025-12-31", "A"),
    "new_sales_fy25_north": I(54904.0, ER26Q1 + " — North Coast & Alexandria chart, 2025",
                              "2025-12-31", "A"),
    "new_sales_fy25_all":   I(215384.0, ER26Q1 + " — New Sales, All Regions chart, 2025. "
                              "The three regions above sum to 163,992, so 51,392mn (23.9%) "
                              "of the disclosed group total is not attributed to any "
                              "charted region in FY2025", "2025-12-31", "A"),
    "construction_1q26": I(4600.0,  ER26Q1 + " — \"The Company spent EGP4.6 billion on "
                           "construction activities during 1Q2026, a growth of 60% YoY\"",
                           "2026-03-31", "A"),
    "units_sold_fy23":  I(5300.0,   "PHD FY2023 earnings release, chart series",
                          "2023-12-31", "A", unit="units"),
}

# ---------------------------------------------------------------------------
# Market data
MARKET = {
    "shares_outstanding_bn": I(2.85992, "Share capital per FY2025 balance sheet and the "
                               "share count carried on the covered-name record",
                               "2025-12-31", "A", unit="bn shares"),
    # ONE PRICE, THE LATEST THIS REPOSITORY HOLDS, CORRECTLY DATED AND SOURCED TO THE
    # CHANNEL IT ACTUALLY CAME FROM [17-09-2026].
    #
    # WHAT WAS WRONG WAS THE DATE, NOT THE NUMBER, and an intermediate pass of this
    # correction got that backwards — recorded here because the mistake is instructive.
    # The row read: 14.40, "closing price for PHDC, 3 September 2026", date field
    # "2026-08-23", tier B. Three of those four claims are right. The price is real and
    # dated: engine/prices/SUPPLIED_03-09-2026.json registers PHDC at 14.40 on 2026-09-03,
    # committed, and that is the register [R-GAP-01]'s own checker reads as the latest
    # known price. What was false was the STRUCTURED DATE — 2026-08-23, which is the date
    # of the 15.20 close named one clause later in the same prose — and the tier, which
    # called a committed house register a B.
    #
    # THE DEFECT THAT REMAINS REAL IS THAT TWO READERS OF ONE FACT DISAGREED [R-ENF-03].
    # The persistent price library ends 23-Aug-2026 at 15.200 and has no September
    # observation, and it is what section 2's moving averages, section 3's distribution
    # and the ticker page on the site are computed from — so the site displays 15.20 while
    # the valuation compared itself against 14.40, and the same resistance level was
    # "1.2 per cent above the close" in one section and "6.8 per cent away" in another.
    # Neither number was invented; nothing reconciled them.
    #
    # THE RULE DECIDES IT. [R-GAP-01] compares a fair value against THE LATEST KNOWN
    # MARKET PRICE, which is the newer of the supplied register and the library: 14.40 of
    # 3 September, not 15.20 of 23 August. That is also the stricter comparison — it widens
    # the gap this study has to defend from +37.4% to +45.0% — and the instruction to use
    # the latest price points the same way. So the valuation strikes against 14.40, dated
    # to its own close and sourced to the register that holds it, and the LIBRARY's date is
    # registered separately below so the document can say plainly that its cone and its
    # trend read stand on 23 August. One comparison price, two vintages, both named.
    "spot":                  I(14.40, "the Egyptian Exchange close for PHDC on 3 September "
                               "2026, from this study's own supplied-price register "
                               "(SUPPLIED_03-09-2026). It is the latest close this "
                               "repository holds and the one [R-GAP-01] measures the gap "
                               "against; the persistent price history ends earlier, on "
                               "23 August 2026 at 15.200, and that is the vintage the "
                               "trend read and the distribution are computed from",
                               "2026-09-03", "A", unit="EGP/share"),
    # The library's own last close, registered so no section can quietly treat the two
    # dates as one. This is the price the site's ticker page displays.
    "price_library_last":    I(15.20, "the last close in this study's persistent price "
                               "history: 23 August 2026 at 15.200. Section 2's moving "
                               "averages and section 3's distribution are computed from "
                               "this history, so they carry this date and the document "
                               "says so. It is also the close the site's ticker page "
                               "shows, which is why that page reads 15.20 while the "
                               "valuation compares itself against the newer 3 September "
                               "close of 14.40",
                               "2026-08-23", "A", unit="EGP/share"),
    # A LATER OBSERVATION STILL, REGISTERED AS EVIDENCE ABOUT STALENESS AND READ BY
    # NOTHING. The market has moved since both dates above, and a study that publishes a
    # gap should say so rather than let the reader discover it.
    "spot_later_observed":   I(13.77, "PHDC close of 16 September 2026 per african-markets "
                               "(EGX:PHDC), read live 17-09-2026: 13.77 EGP, previous "
                               "close 13.81, volume 3,252,373. A third-party feed, "
                               "recorded to SIZE how far the market has moved beyond the "
                               "prices this repository holds — 4.4% below the 3 September "
                               "close and 9.4% below the library's last row — and used in "
                               "no calculation. egx.com.eg returned an empty reply from "
                               "this environment and Mubasher HTTP 403",
                               "2026-09-16", "C", unit="EGP/share"),
    # Third-party share count, registered because it CONTRADICTS a claim made against this
    # study. An external audit asserts PHDC publishes an "Outstanding shares" figure net of
    # treasury — 2,839,980,164 at 31-Mar-2026 — against the 2,859,914,173 issued count this
    # study divides by. Neither of the company's own releases carries a share count at all
    # (checked live, 17-09-2026), and the one third-party source reachable from here reports
    # 2,859.91mn, which AGREES with this study's divisor. The claim is therefore unresolved,
    # not accepted and not dismissed, and it is registered with both figures so the next
    # reader starts from the evidence rather than from either assertion.
    "shares_third_party":    I(2859.91, "african-markets (EGX:PHDC), \"Shares Outstanding "
                               "2,859.91 mln\", read live 17-09-2026. An external audit "
                               "asserts a treasury-net count of 2,839.980164mn at "
                               "31-Mar-2026; no company document reachable from here "
                               "carries either figure", "2026-09-16", "C", unit="mn shares"),
}

# ---------------------------------------------------------------------------
# COST-OF-CAPITAL AND MACRO INPUTS — REGISTERED [17-09-2026].
#
# THESE HAD NO REGISTER ROWS AT ALL, and that was the one class of input the study's own
# Appendix B.3 singled out as third-party: "The only third-party inputs are the exogenous
# macroeconomic series and the market price." The register held 125 rows and not one of
# them carried the government bond yield, either sovereign spread, either equity risk
# premium, the beta, the tax rate, the cost of debt or the inflation path — the inputs
# behind the largest single number in the valuation. A figure that reaches the answer and
# has no row is not sourced, however defensible it is, and the discount rate was the
# largest such figure in this study. Values are READ FROM wacc_result.json at build time
# so these rows carry provenance and never a second copy of the number.
COST_OF_CAPITAL_SOURCES = {
    "rf_observed": ("Egyptian ten-year government bond yield. LIMITATION, STATED: the "
                    "Central Bank of Egypt has auctioned no ten-year EGP benchmark since "
                    "31 May 2022 and nothing above five years since 2023, so this is a "
                    "secondary-market quote and not an auction clearing level. cbe.org.eg's "
                    "auction pages return an empty shell from this environment "
                    "(269 bytes, 17-09-2026). The tenors that do clear are shorter and the "
                    "curve is inverted, so a rate built from them would be HIGHER, not "
                    "lower. Closed by: a dated secondary-market quote from the EGX, the "
                    "CBE yield curve, or the Ministry of Finance.", "C"),
    "sovereign_spread_rating": ("Damodaran country-risk file, January 2026, Egypt row, "
                                "\"Adj. Default Spread\"", "C"),
    "sovereign_spread_cds": ("Damodaran country-risk file, January 2026, Egypt row, "
                             "sovereign CDS net of the Swiss CDS", "C"),
    "erp_rating": ("Damodaran January 2026: mature-market ERP scaled by the rating-based "
                   "default spread and the relative-volatility factor", "C"),
    "erp_cds": ("Damodaran January 2026: mature-market ERP plus the CDS-based country "
                "premium. THE ADOPTED BASIS, and section 1.8 marks it so", "C"),
    "beta": ("PHDC's own weekly returns regressed on the EGX30 published index through "
             "the house regression routine, which resolves the index itself; the "
             "regression, its window, its "
             "observation count and its standard error are published in Appendix B and "
             "the estimator is named there", "A"),
    "tax_rate": ("PHD FY2025 consolidated financial statements, tax note: current tax "
                 "computed at 22.5% of net taxable profit in FY2025 and FY2024", "A"),
    "kd_pretax": ("The sovereign yield above plus a stated corporate spread. NOT SOURCED "
                  "and flagged as the study's one unsourced cost-of-capital input: the "
                  "EGP 2.015bn securitisation of 4-Feb-2026 discloses tranche sizes, "
                  "tenors and national-scale ratings and NO coupon. Closed by: a coupon "
                  "on any tranche.", "D"),
    "inflation_path": ("the house Egyptian macro path [R-MACRO-01], "
                       "shared across every EG study; the terminal rate is the Central "
                       "Bank of Egypt's published Q4-2026 inflation target", "C"),
}

# ---------------------------------------------------------------------------
# GAPS — disclosed nowhere, and therefore NOT filled. Each names what closes it.
GAPS = {
    # THE CLAIM WAS WIDER THAN THE SEARCH BEHIND IT [corrected 17-09-2026]. This row said
    # the FY2025 cash-flow statement "is published in its three totals only". What was
    # actually established is that PHD's EARNINGS RELEASES print the cash-flow statement in
    # three totals — verified again 17-09-2026 on the 1Q2026 release (operating 1,766,705,
    # investing (1,891,835), financing (571,788)) and the 4Q2024 release (3,131,882 /
    # (3,092,025) / 3,143,286). The AUDITED statements are a scan with no text layer; this
    # study read the balance sheet and income statement off it by OCR and never extracted a
    # cash-flow page. An external audit reports that the audited FY2025 statement carries a
    # full indirect-method statement of roughly 45 lines, two of which — Residents'
    # Association +9,646.5 and notes payable +4,466.0 — would cover EGP 14,112.5mn of the
    # wedge. THAT IS A LEAD AND IT IS RECORDED AS ONE. The wedge is still not split, but the
    # reason is now the true one: this study has not read the statement, not that the
    # statement does not exist. The distinction matters because the whole two-framing
    # architecture of Appendix A.3 rests on it.
    "cash_flow_statement_detail": (
        "PHD's earnings releases publish the cash-flow statement in three totals only — "
        "re-verified 17-09-2026 on the 1Q2026 and 4Q2024 releases — and FY2025 has no "
        "release at all, so the three FY2025 totals this study holds (operating "
        "EGP 1,424.2mn, investing EGP -4,031.7mn, financing EGP 5,628.8mn) come from the "
        "audited statements. THE AUDITED STATEMENTS ARE A SCAN WITH NO TEXT LAYER and this "
        "study extracted the balance sheet and income statement from it, never a cash-flow "
        "page; an external audit reports that a full indirect-method statement of roughly "
        "45 lines is printed there, including two operating movements that would cover "
        "EGP 14,112.5mn of the wedge below. That is a lead this study has not verified, so "
        "the wedge is not split — because the line detail has not been READ, not because it "
        "is unpublished. Working capital "
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
    # THE H1-2026 FILING: WHAT WAS SEARCHED, ON WHICH CHANNEL, AND WHAT CAME BACK
    # [rewritten 17-09-2026 from searches run that day, not from a prior edition's text].
    #
    # A previous rebuild of this study CONSUMED 30-June-2026 figures — a net debt of
    # 27,471.2, associates of 3,898.5, investment property of 1,008.4 — and printed them
    # under a column headed "31 Mar 2026 (reviewed)". This edition does not carry them, and
    # the reason is a sourcing rule rather than a doubt about the numbers: they could not be
    # obtained from any channel reachable here, and a figure this study cannot read is not a
    # figure this study publishes, however well attested it is elsewhere.
    #
    # SEARCHED 17-09-2026, both channels, results recorded either way:
    #   - the company's own result centre, fetched live (HTTP 200, 102,142 bytes): the
    #     newest documents of any kind are "PHD Consolidated FS Q1 2026 (English).pdf" and
    #     "PHD - 1Q2026 Earnings Release - English.pdf". Of 86 PDFs on the page not one is
    #     a 2Q/H1-2026 statement or release. The IR presentations paths return HTTP 404.
    #   - egx.com.eg: empty reply from the server, twice. Mubasher: HTTP 403.
    #
    # REPORTED BUT NOT HELD: an external audit of this study states that PHDC filed reviewed
    # consolidated statements to 30 June 2026 with the Exchange on 18 August 2026, and
    # reports figures from the attachment. The trade press reports an order book of EGP 284bn
    # at 30 June and a further EGP 75bn sold at Hacienda Ras El Hekma in the fortnight after.
    # BOTH ARE LEADS AND NEITHER IS A SOURCE. The information set of this edition therefore
    # ends at 1Q2026 and every date-bearing claim in the document says 31 March 2026 and
    # means it. If the reported figures hold, the order book is ahead of what this study
    # carries — and the study's own measurement is that the backlog is not the binding
    # constraint, so being behind on it moves the answer by nothing.
    # Closed by: the H1-2026 filing itself, from the company or the Exchange.
    "h1_2026_results": "PHD's reviewed consolidated statements to 30 June 2026 are "
        "REPORTED to have been filed with the Egyptian Exchange on 18 August 2026, and an "
        "external audit of this study quotes figures from that attachment. This study has "
        "NOT obtained the filing. Searched 17-09-2026: the company's own result centre was "
        "fetched live and its newest documents of any kind are the 1Q2026 statements and "
        "the 1Q2026 release — of 86 PDFs on the page, none is a 2Q or H1-2026 document; "
        "egx.com.eg returned an empty reply and Mubasher HTTP 403. A report of a disclosure "
        "is a lead and never a source, so nothing from it is used and the information set "
        "ends at 1Q2026. Closed by: the H1-2026 filing itself.",
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
# DATED NEGATIVE SEARCHES — a register, NOT a disclosure gap [R-PRIME-01].
#
# KEPT SEPARATE FROM GAPS ON PURPOSE, and the build caught the conflation. GAPS is the
# six-row table section 7 prints: things the COMPANY does not disclose. A negative search
# is something THIS STUDY looked for and did not find, which is a fact about the search and
# not about the issuer — and section 7's own count is asserted at six, so a research record
# filed among them breaks the document rather than informing it.
#
# WHY IT IS RECORDED AT ALL. A claim that something is not disclosed is a claim about a
# search, and a search with no date and no channel is not evidence. The superseded edition
# asserted that no half-year filing existed; the search behind that assertion was never
# written down, so nothing could tell a later reader whether the filing was absent or
# merely unlooked-for. It was the latter.
    # DATED NEGATIVE SEARCHES, RECORDED SO THE NEXT EDITION STARTS FROM WHAT WAS TRIED
    # RATHER THAN REPEATING IT [R-PRIME-01]. A claim that something is not disclosed is a
    # claim about a search, and a search with no date and no channel is not evidence.
NEGATIVE_SEARCHES = {
    "17-09-2026": (
        "Run 17-09-2026, each with its channel and its result. "
        "(1) PHDC IR result centre — HTTP 200, 86 PDFs, newest of any kind is 1Q2026; no "
        "2Q/H1-2026 statement or release. "
        "(2) PHDC IR presentations — HTTP 404 on both candidate paths, so the September "
        "2022 investor presentation and the corporate brochure an external audit cites for "
        "price and construction cost per square metre, per-project unit mix and a "
        "disclosed 5-7 year receivable life COULD NOT BE REACHED from here. They are "
        "therefore neither consumed nor denied: the register no longer says those series "
        "are undisclosed, it says this study has not read them. "
        "(3) egx.com.eg — empty reply from the server, twice; the Exchange's own filing "
        "record, its treasury-share disclosures and its board-resolution and Article-48 "
        "filings are unreachable, so any claim about what PHDC has or has not filed with "
        "the Exchange is outside this study's evidence. "
        "(4) english.mubasher.info — HTTP 403. "
        "(5) cbe.org.eg auction pages — HTTP 200 but a 269-byte empty shell, so no "
        "Egyptian auction curve could be read; the ten-year yield's limitation is stated "
        "in COST_OF_CAPITAL_SOURCES rather than papered over. "
        "(6) A company-published share count net of treasury — absent from both the "
        "1Q2026 and 4Q2024 releases, which carry no share count at all."),
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
