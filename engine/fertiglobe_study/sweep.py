"""Fertiglobe plc (FERTIGLB, ADX) — four-ring Information Sweep register.

Runs BEFORE any forecast driver is set. Every mandatory category of every ring is
closed by a dated finding or a dated negative search.

SOURCING NOTE: the company's own website and investor-relations archive were reachable
from this environment, and every historical financial figure in the study traces to a
PwC-signed consolidated financial statement downloaded from that archive. Four complete
audited fiscal years were obtained (FY2022, FY2023, FY2024, FY2025), plus both quarters
of the study year already on the public record (Q1-2026 and Q2-2026). No aggregator,
broker note or press extract appears anywhere in the build path for a company-reported
historical figure.
"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from research_sweep import (SweepRegister, AssetClass, Ring, FindingClass,
                            SourceType, DriverMode)

SWEEP_DATE = "2026-08-09"
R = SweepRegister("FERTIGLB", AssetClass.STOCK, SWEEP_DATE)
CO, IR, REG, PMD, PRESS, AGG = (SourceType.COMPANY_OFFICIAL, SourceType.COMPANY_IR,
                                SourceType.REGULATOR_OFFICIAL, SourceType.PRIMARY_MARKET_DATA,
                                SourceType.REPUTABLE_PRESS, SourceType.AGGREGATOR)

FS25 = "Fertiglobe plc, Consolidated Financial Statements FY2025, PwC-signed 4-Mar-2026"
FS24 = "Fertiglobe plc, Consolidated Financial Statements FY2024, signed 18-Mar-2025"
FS23 = "Fertiglobe plc, Consolidated Financial Statements FY2023, signed"
FS22 = "Fertiglobe plc, Consolidated Financial Statements FY2022"
Q1FS = "Fertiglobe plc, Interim Financial Statements, three months ended 31-Mar-2026"
Q2FS = "Fertiglobe plc, Interim Financial Statements, six months ended 30-Jun-2026"
MDA25 = "Fertiglobe Q4 2025 Results MD&A Report"
MDA26 = "Fertiglobe Q2 2026 Results MD&A Report"
IP26 = "Fertiglobe Q2 2026 Investor Presentation"
TRX26 = "Fertiglobe Q2 2026 Results Call Transcript"

# ---- primary access log (attempted and logged whether or not it succeeded) ----
R.record_primary_access("https://fertiglobe.com/investor-relations/", True, SWEEP_DATE,
                        "Investor relations landing page reachable; HTTP 200.")
R.record_primary_access("https://fertiglobe.com/investor-relations/results-reports/", True,
                        SWEEP_DATE,
                        "Full results archive reachable — annual reports, audited consolidated "
                        "financial statements, quarterly statements, MD&A reports, investor "
                        "presentations and results-call transcripts from FY2021 to Q2-2026.")
R.record_primary_access("https://fertiglobe.com/wp-content/uploads/2026/03/"
                        "Fertiglobe-plc-Consolidated-FS-4Mar26-no-nav.pdf", True, SWEEP_DATE,
                        "FY2025 audited consolidated financial statements downloaded and parsed "
                        "(86 pages).")
R.record_primary_access("https://fertiglobe.com/wp-content/uploads/2025/03/"
                        "En_Fertiglobe-plc-Consolidated-Financial-Statements-2024-18-March-2025-"
                        "Signed.pdf", True, SWEEP_DATE,
                        "FY2024 audited consolidated financial statements downloaded and parsed "
                        "(80 pages).")
R.record_primary_access("https://fertiglobe.com/wp-content/uploads/2024/07/"
                        "EN-Consolidated-FY23-Financial-Statements-signed-FINAL.pdf", True,
                        SWEEP_DATE,
                        "FY2023 audited consolidated financial statements downloaded and parsed "
                        "(75 pages).")
R.record_primary_access("https://fertiglobe.com/wp-content/uploads/2024/03/"
                        "Fertiglobe-Consolidated-2022-Financial-Statements-vF.pdf", True,
                        SWEEP_DATE,
                        "FY2022 audited consolidated financial statements downloaded and parsed "
                        "(74 pages) — the fourth complete audited year.")

R.declare_study_year("2026", ["Q1-2026", "Q2-2026"])

# ================================================================ RING 1 GLOBAL
f_rates = R.add(Ring.GLOBAL, "rate cycle & USD/FX regime", FindingClass.S,
    "The US 10-year Treasury yield stands at 4.69% and the overnight secured financing "
    "rate at 3.65%. Because the dirham is hard-pegged to the dollar and the company both "
    "reports and borrows in dollars, the US curve is the currency-matched base for the "
    "cost of capital rather than a foreign proxy",
    "Federal Reserve Bank of St Louis, FRED series DGS10; New York Federal Reserve",
    REG, "2026-08-06",
    url="https://fred.stlouisfed.org/series/DGS10",
    model_impact="Sets the risk-free base of the cost of capital. The Abu Dhabi dollar "
                 "sovereign is built as the Treasury yield plus the emirate's own credit "
                 "spread, then normalised by removing that same spread so sovereign risk "
                 "is counted once, inside the equity risk premium.")

f_gas = R.add(Ring.GLOBAL, "commodity complex (input/output)", FindingClass.B,
    "European gas rallied to over $20/MMBtu, lifting the marginal cost of European "
    "nitrogen production above prevailing import prices and putting a cost floor under "
    "ammonia; ammonia averaged $866/t delivered north-west Europe in the second quarter "
    "of 2026 against $452/t a year earlier",
    MDA26 + "; " + TRX26, IR, "2026-08-06",
    model_impact="Sets the price floor argument in the mid-cycle anchor. European "
                 "marginal cost is what stops the modelled price path reverting below "
                 "roughly $430/t of urea, and it is the reason framing B is a live "
                 "possibility rather than a courtesy.")

f_trade = R.add(Ring.GLOBAL, "trade / sanctions / supply chains", FindingClass.B,
    "Conflict in the Middle East closed the Strait of Hormuz to normal traffic during "
    "the second quarter of 2026 — a route carrying over 21% of global ammonia trade and "
    "around 30% of global urea exports. The company exported volumes from the UAE "
    "equivalent to only 56% of quarterly production and moved the balance by alternative "
    "overland and sea routes at higher cost",
    MDA26 + "; " + TRX26, IR, "2026-08-06",
    model_impact="Explains both the 2026 price spike and the step-up in freight and "
                 "logistics cost per tonne. Both are modelled as unwinding rather than "
                 "permanent, which is the conservative side of the central judgement.")

f_gdem = R.add(Ring.GLOBAL, "global sector demand", FindingClass.S,
    "Global urea demand growth outside China of about 11.4 million tonnes to 2030 is "
    "expected to outpace capacity additions of about 9.1 million tonnes, on the company's "
    "own compilation of projects that have reached a final investment decision",
    IP26, IR, "2026-07-28",
    model_impact="This is the evidence base for framing B — the structurally tight "
                 "reading of the price path. It is the company's own view of its own "
                 "market and is treated as an interested source, which is why it is "
                 "carried as one of two framings and not as the base case.")

# =============================================================== RING 2 COUNTRY
f_uae = R.add(Ring.COUNTRY, "sovereign macro (inflation, policy rate, FX/deval risk)",
    FindingClass.S,
    "Abu Dhabi is rated Aa2 with an adjusted default spread of 0.42% and a sovereign "
    "credit default swap of 0.46%; Egypt is rated Caa1 with a 6.37% default spread; "
    "Algeria is unrated with a 3.83% assessed spread. The dirham peg at 3.6725 to the "
    "dollar has held since 1997",
    "A. Damodaran, country default spreads and risk premiums; UAE central bank",
    REG, "2026-08-09",
    url="https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/ctryprem.html",
    model_impact="Each operating country is priced off its own row. The equity risk "
                 "premium is weighted by where the plants actually sit — 50.7% UAE, "
                 "31.1% Egypt, 16.1% Algeria — giving 8.51%, far above the 4.87% that "
                 "treating the company as purely Emirati would have produced.")

f_tax = R.add(Ring.COUNTRY, "regulatory environment (regulator, caps, tariffs, tax/subsidy)",
    FindingClass.S,
    "The statutory UAE rate is 9%, but the group's own statutory rate ranges from 0% to "
    "25% because certain entities hold qualified free-zone status while others are subject "
    "to emirate-level taxation. The reported effective rate was 4.0% in 2025 and 7.0% in "
    "2024, both flattered by items that do not recur",
    FS25 + ", income taxes note", CO, "2026-03-04",
    is_fs_data=True, fiscal_period="FY2025",
    model_impact="The forecast tax rate is not taken from any single reported year. It "
                 "is the average of three independently sourced estimates — the four-year "
                 "aggregate effective rate, the four-year aggregate cash rate, and a "
                 "jurisdiction-weighted statutory build — which the workbook computes on "
                 "the sheet rather than asserting.")

f_eu = R.add(Ring.COUNTRY, "fiscal / political events with sector read-through", FindingClass.S,
    "European Union tariffs on Russian and Belarusian fertilisers rose to EUR 60 per tonne "
    "in July 2026 from EUR 40, on top of an existing 6.5% duty, with annual increases "
    "scheduled to reach EUR 315 per tonne by 2028. Egyptian and Algerian product remains "
    "duty free. France announced support of at least EUR 50 per tonne for farmers buying "
    "nitrogen fertiliser through September 2026",
    MDA26, IR, "2026-07-28",
    model_impact="Supports the realised-price-to-benchmark ratio holding at about 1.00 "
                 "rather than eroding. The company's North African plants sell into Europe "
                 "duty free against a rising tariff wall on the largest competing supplier.")

# ============================================================== RING 3 INDUSTRY
f_bal = R.add(Ring.INDUSTRY, "demand drivers & capacity/supply balance", FindingClass.S,
    "No material new urea capacity is scheduled for several years, and India completed "
    "three urea tenders in the first half of 2026 seeking 5.5 million tonnes — around 60% "
    "of its full prior-year import volume — in half a year",
    IP26 + "; " + MDA26, IR, "2026-07-28",
    model_impact="Supports holding forecast utilisation at or above recent levels rather "
                 "than assuming volume competition from new entrants.")

f_price = R.add(Ring.INDUSTRY, "pricing", FindingClass.B,
    "Granular urea free on board Egypt averaged $637/t in the first half of 2026 against "
    "$440/t for 2025 and $357/t for 2024; ammonia free on board the Middle East averaged "
    "$594/t against $343/t and $349/t. Urea then normalised and stood at $555/t in mid-July "
    "2026",
    MDA26 + " and " + MDA25 + ", benchmark price tables (source: CRU, MMSA, ICIS, Bloomberg)",
    IR, "2026-07-28",
    model_impact="These are the price anchors for both framings. Framing A reverts toward "
                 "a marginal-cost anchor of about $435/t of urea by 2028; framing B holds "
                 "near $550/t. The gap between them is the study's central question.")

f_entrants = R.add(Ring.INDUSTRY, "new entrants (named-competitor level)", FindingClass.C,
    "New nitrogen supply is concentrated in the United States Gulf Coast, where it "
    "continues to ramp, and in Iran, whose production has been limited by the same "
    "regional disruption. Chinese exports were absent until the government issued quota "
    "guidance in May 2026 and remain minimal",
    MDA26 + "; " + IP26, IR, "2026-07-28",
    model_impact="Chinese export policy is the single largest swing factor on the supply "
                 "side and is named in the section on what would change our mind.")

f_tech = R.add(Ring.INDUSTRY, "technology substitution", FindingClass.S,
    "The European carbon border adjustment mechanism entered its definitive phase on "
    "1 January 2026 alongside the phase-out of free emissions allowances, which supports "
    "demand for lower-carbon ammonia. The company is building a one-million-tonne "
    "lower-carbon ammonia plant for under $500 million of total project cost, with "
    "operations expected in 2027",
    MDA26 + "; " + IP26, IR, "2026-07-28",
    model_impact="Excluded from the base case. The parent is warehousing the project and "
                 "the company holds only an option to move to 54% ownership after "
                 "completion, so it is not a consolidated cash flow today. It is carried "
                 "as an unpriced option and named as an upside catalyst.")

f_comp = R.add(Ring.INDUSTRY, "competitor capacity / price moves (named)", FindingClass.C,
    "The comparable set spans Nutrien, CF Industries, Yara International and OCI Global "
    "in the West, and Industries Qatar and SABIC Agri-Nutrients in the Gulf. Gulf-listed "
    "nitrogen producers carry materially higher enterprise multiples than Western peers "
    "on comparable assets",
    "Peer enterprise value to EBITDA multiples compiled for the relative lens", AGG,
    "2026-08-09",
    model_impact="Sets the relative multiple. The multiple applied sits below the Gulf "
                 "peers and above the European ones, because the company earns Gulf "
                 "gas economics but carries Egyptian and Algerian country risk.")

# =============================================================== RING 4 COMPANY
f_fs25 = R.add(Ring.COMPANY, "official financial statements", FindingClass.D,
    "FY2025 audited consolidated statements: revenue $2,827.4m, gross profit $885.4m, "
    "operating profit $727.3m, profit for the year $588.5m of which $433.9m attributable "
    "to owners, total assets $4,949.5m, total equity $1,799.8m, gross interest-bearing "
    "debt $1,740.6m",
    FS25, CO, "2026-03-04", is_fs_data=True, fiscal_period="FY2025",
    url="https://fertiglobe.com/wp-content/uploads/2026/03/"
        "Fertiglobe-plc-Consolidated-FS-4Mar26-no-nav.pdf",
    model_impact="The whole historical income statement, balance sheet and cash flow are "
                 "constructed from this filing and its two predecessors. Every recomputed "
                 "subtotal was asserted back against the filed figure.")

f_fs24 = R.add(Ring.COMPANY, "official financial statements", FindingClass.D,
    "FY2024 audited consolidated statements: revenue $2,009.2m, profit for the year "
    "$213.6m, and a Key Audit Matter on the accrual for increased Sorfert gas cost",
    FS24, CO, "2025-03-18", is_fs_data=True, fiscal_period="FY2024",
    model_impact="Supplies the FY2024 comparative column used for the three-year historical "
                 "income statement and balance sheet, and the FY2024 segment revenue and "
                 "EBITDA that form the earliest of the three observations behind the cost "
                 "pass-through calibration.")

f_fs23 = R.add(Ring.COMPANY, "official financial statements", FindingClass.D,
    "FY2023 audited consolidated statements: revenue $2,416.2m, profit for the year "
    "$505.0m, with FY2022 carried as the comparative (revenue $5,027.5m)",
    FS23, CO, "2024-04-29", is_fs_data=True, fiscal_period="FY2023",
    model_impact="Supplies the FY2023 historical year and, through its own comparative "
                 "column, the FY2022 cycle peak. Both feed the four-year aggregate "
                 "effective and cash tax rates that set the forecast tax rate, and the "
                 "three-year average margin behind the normalised earnings power lens.")

f_fs22 = R.add(Ring.COMPANY, "official financial statements", FindingClass.C,
    "FY2022 audited consolidated statements — the fourth complete audited year, and the "
    "cycle peak against which the current period is judged: revenue $5,027.5m and profit "
    "for the year $1,820.4m",
    FS22, CO, "2023-02-14", is_fs_data=True, fiscal_period="FY2022")

f_q1 = R.add(Ring.COMPANY, "regular disclosures", FindingClass.B,
    "First-quarter 2026 interim statements, with the accrual for increased Sorfert gas "
    "cost at $422.4m",
    Q1FS, CO, "2026-04-29", is_fs_data=True, fiscal_period="Q1-2026",
    model_impact="Confirms the gas accrual is still building quarter by quarter rather "
                 "than having settled.")

f_q2 = R.add(Ring.COMPANY, "regular disclosures", FindingClass.B,
    "First-half 2026 interim statements: revenue $2,001.0m, gross profit $624.9m, profit "
    "attributable to owners $312.4m, net debt down to $621.2m from $1,005.5m at the year "
    "end, and the Sorfert gas accrual at $468.8m",
    Q2FS + "; " + MDA26, CO, "2026-07-28", is_fs_data=True, fiscal_period="Q2-2026",
    model_impact="The 2026 forecast year is built as this reported half plus a modelled "
                 "second half, rather than as a modelled full year. Half of the study "
                 "year is already fact and is carried as fact.")

f_gaslink = R.add(Ring.COMPANY, "IR communications (calls, presentations, releases)",
    FindingClass.B,
    "The chief executive stated on the second-quarter results call that gas pricing in "
    "Egypt and Algeria is product-linked: 'we have gas-linked — sorry, product-linked gas "
    "pricing effectively in both Egypt as well as Algeria. So, product prices are very "
    "strong. We'll see a higher gas cost.' The delivered gas price in the second quarter "
    "of 2026 was $6/MMBtu, or $8/MMBtu including the Algerian profit-share",
    TRX26, IR, "2026-08-06",
    model_impact="This is the single most consequential finding in the sweep and it "
                 "contradicts the audited segment note, which describes the gas offtake "
                 "agreements as carrying 'no/limited price exposure'. It converts the cost "
                 "side from an inflation-escalated stack into a function of the product "
                 "price, and it is calibrated from disclosed segment economics rather than "
                 "assumed — every incremental dollar of realised price carries about 48 "
                 "cents of cost with it.")

f_vols = R.add(Ring.COMPANY, "IR communications (calls, presentations, releases)",
    FindingClass.D,
    "Product sales volumes are disclosed quarterly by product: own-produced urea 4,228kt "
    "and ammonia 1,267kt in 2025; 2,045kt and 523kt in the first half of 2026. Urea "
    "utilisation ran at 92% across the platform in the first half of 2026. Installed "
    "capacity is 5.1 million tonnes of urea and 1.5 million tonnes of merchant ammonia",
    MDA25 + "; " + MDA26 + "; " + IP26, IR, "2026-07-28",
    model_impact="Converts the revenue forecast from a top-down growth rate into a genuine "
                 "unit build — capacity times utilisation gives volume, benchmark price "
                 "times a realisation ratio gives price, and the two multiply. The "
                 "realisation ratio was measured at 1.015, 0.999 and 0.989 across three "
                 "independent disclosed periods.")

f_sorfert = R.add(Ring.COMPANY, "one-off base-resetting transactions", FindingClass.B,
    "Sorfert operates under a 20-year gas supply contract with Sonatrach whose price was "
    "fixed for ten years; that period lapsed at the end of 2023 and the replacement price "
    "applies retrospectively from then. The accrued liability has built from $7.2m at the "
    "end of 2023 to $182.8m, $386.3m, $422.4m and $468.8m at 30 June 2026. Negotiations "
    "are unconcluded and no payment schedule exists",
    FS24 + " (Key Audit Matter); " + FS25 + "; " + Q2FS + "; " + TRX26, CO, "2026-07-28",
    is_fs_data=True, fiscal_period="Q2-2026",
    model_impact="Charged through cost of sales each period, so it is inside the "
                 "calibrated cost pass-through. Stripping it out changes the pass-through "
                 "slope by less than a percentage point, which is what makes the "
                 "calibration robust rather than an artefact of this one item. The "
                 "unsettled balance is carried as a disclosed liability and named as a "
                 "risk, because the final formula is not yet known.")

f_own = R.add(Ring.COMPANY, "ownership / stake changes (named-transaction rule)",
    FindingClass.S,
    "Abu Dhabi National Oil Company completed its acquisition of OCI N.V.'s entire "
    "shareholding on 15 October 2024, taking 86.2%. As of the FY2025 reporting date the "
    "parent holds 87.4% and the free float is 12.6%",
    FS25 + ", note 1", CO, "2026-03-04", is_fs_data=True, fiscal_period="FY2025",
    model_impact="A 12.6% free float is a liquidity and governance fact that belongs in "
                 "the caveats, and it is one reason the share's returns track the local "
                 "index so weakly. It does not change a forecast driver.")

f_cap = R.add(Ring.COMPANY, "management & capital actions", FindingClass.S,
    "Dividends of $250m were paid for 2025 and a buyback programme of up to 2.5% of "
    "shares was approved in April 2025, of which 1.34% had been repurchased for $74m by "
    "30 June 2026. First-half 2026 dividends of at least $150m were proposed",
    FS25 + "; " + MDA26, CO, "2026-07-28", is_fs_data=True, fiscal_period="FY2025",
    model_impact="Sets the 80% distribution assumption in the balance-sheet roll-forward, "
                 "measured from actual distributions against attributable profit rather "
                 "than assumed.")

f_strat = R.add(Ring.COMPANY, "strategic plans & guidance", FindingClass.C,
    "The company operates a Manufacturing Improvement Plan and a Financial Improvement "
    "Plan with stated incremental targets, and describes a 'Grow 2030' strategy backed by "
    "the parent's international investment arm",
    IP26 + "; " + MDA26, IR, "2026-07-28",
    model_impact="Supports the utilisation glide from 82.3% to 88.8% over the forecast "
                 "period. The company gives no numeric volume or price guidance, so no "
                 "guidance figure is carried as a driver.")

# ---- negative searches, dated -------------------------------------------------
R.add_negative(Ring.COMPANY, "one-off base-resetting transactions",
               "searched the FY2025 statements and both 2026 interim filings for "
               "impairments, discontinued operations, restatements or disposals beyond "
               "the Wengfu Australia acquisition — none found", SWEEP_DATE)

f_neg_3p = R.add_negative(Ring.COMPANY, "regular disclosures",
               "searched the FY2023, FY2024 and FY2025 audited statements, both 2026 "
               "interim filings, every MD&A report and the results-call transcript for a "
               "purchase price, cost per tonne or gross margin per tonne on third-party "
               "traded product. Volumes are disclosed by product but no purchase-side unit "
               "economics are given anywhere — only segment revenue and segment EBITDA",
               SWEEP_DATE)

f_neg_gasbase = R.add_negative(Ring.COMPANY, "IR communications (calls, presentations, releases)",
               "searched all four audited filings, both interim filings and every MD&A "
               "report for a disclosed delivered gas price per MMBtu for any period before "
               "the second quarter of 2026, and for the Sonatrach and Egyptian gas pricing "
               "formulas themselves. Only the single Q2-2026 figure on the results call was "
               "found; no formula and no historical series is published",
               SWEEP_DATE)

# ---- driver gate --------------------------------------------------------------
R.add_driver("Own-produced sales volume (kt, by product)", DriverMode.BOTTOM_UP,
             "Installed capacity by plant and product is disclosed, and quarterly sales "
             "volumes are disclosed by product. Volume is capacity times utilisation, "
             "both sourced.", [f_vols])
R.add_driver("Realised price per tonne ($/t, by product)", DriverMode.BOTTOM_UP,
             "Published benchmark prices by product and region, multiplied by a "
             "realisation ratio measured against disclosed segment revenue over three "
             "independent periods.", [f_price, f_vols])
R.add_driver("Cash cost per tonne ($/t)", DriverMode.BOTTOM_UP,
             "Calibrated against realised price from disclosed segment revenue and EBITDA "
             "over three periods, and cross-checked physically against gas consumption "
             "intensity and the disclosed delivered gas price.", [f_gaslink, f_sorfert]),
R.add_driver("Third-party trading revenue and margin", DriverMode.TOP_DOWN,
             "Volumes are disclosed but purchase prices are not, so the leg is carried at "
             "a segment margin measured from disclosed segment EBITDA. The gap is flagged: "
             "this is the one leg not built from unit economics.", [f_fs25, f_neg_3p])
R.add_driver("Forecast tax rate", DriverMode.BOTTOM_UP,
             "Average of three sourced estimates computed on the workbook sheet — "
             "four-year aggregate effective, four-year aggregate cash, and a "
             "jurisdiction-weighted statutory build on disclosed asset weights.", [f_tax])
R.add_driver("Working capital", DriverMode.BOTTOM_UP,
             "Projected from the receivable, inventory and payable days measured off the "
             "filed statements, with the gas accrual removed from payables because it is "
             "not a trade payable in the ordinary course.", [f_fs25, f_sorfert])
R.add_driver("Equity risk premium", DriverMode.BOTTOM_UP,
             "Each operating country priced off its own published sovereign row and "
             "weighted by disclosed non-current assets by country.", [f_uae, f_fs25])
R.add_driver("Cost of debt", DriverMode.BOTTOM_UP,
             "The company's own most recent borrowings, tranche by tranche, at their "
             "disclosed margins over the reference rate.", [f_fs25])
R.add_driver("Beta", DriverMode.BOTTOM_UP,
             "Regression of the share's own weekly returns against an equal-weight "
             "composite of the local market over the full listed history.", [f_own])

errors, warnings = R.validate()
print(f"Sweep register — {R.ticker}, {SWEEP_DATE}")
print(f"  {R.counts()}")
print(f"  primary access attempts: {len(R.primary_access)} "
      f"({sum(1 for a in R.primary_access if a.reachable)} reachable)")
print(f"  study year {R.study_year}, quarters disclosed {R.study_quarters_disclosed}")
if errors:
    print("  ERRORS:")
    for e in errors:
        print("   -", e)
if warnings:
    print("  warnings:")
    for w in warnings:
        print("   -", w)
print("  " + R.qc_line())
R.to_json(os.path.join(HERE, 'sweep_register.json'))
assert not errors, f"sweep register FAILED validation: {errors}"
print("  sweep register validated — wrote sweep_register.json")
