"""BOROUGE — four-ring Information Sweep register.

Runs BEFORE any forecast driver is set. Every mandatory category of every ring is
closed by a dated finding or a dated negative search.

SOURCING NOTE: the company's own investor-relations document library was reachable
throughout this build. All twenty-one Borouge documents the study reads were
re-fetched from borouge.com and are byte-for-byte identical to the copies in src/
(verify_sources.py, source_access.json). No aggregator or press summary is a source
for any figure Borouge itself reports.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from research_sweep import (SweepRegister, AssetClass, Ring, FindingClass,   # noqa: E402
                            SourceType, DriverMode)

SWEEP_DATE = "2026-08-09"
R = SweepRegister("BOROUGE", AssetClass.STOCK, SWEEP_DATE)
CO, IR, REG, PMD, PRESS, AGG = (SourceType.COMPANY_OFFICIAL, SourceType.COMPANY_IR,
                                SourceType.REGULATOR_OFFICIAL, SourceType.PRIMARY_MARKET_DATA,
                                SourceType.REPUTABLE_PRESS, SourceType.AGGREGATOR)

IRLIB = "https://www.borouge.com/en/investor-relations/Pages/reports-results.aspx"

# ============================================================== PRIMARY ACCESS
for url, ok, note in [
    (IRLIB, True,
     "Company investor-relations document library — the index every statement below "
     "was taken from. Reachable; 105 published documents enumerated."),
    ("https://www.borouge.com/en/investor-relations/IRResults/FYQ4-25/"
     "Q4%202025%20Financial%20Statements%20-%20statutory.pdf", True,
     "FY2025 audited statutory financial statements. Re-fetched and byte-identical "
     "to the copy the build reads (SHA-256 match)."),
    ("https://www.borouge.com/en/investor-relations/Documents/IR%20Documents/"
     "Borouge-Q4-2024-EN%20Borouge%20Financial%20Statement.pdf", True,
     "FY2024 audited statutory financial statements. Re-fetched, byte-identical."),
    ("https://www.borouge.com/en/investor-relations/Documents/IR%20Documents/"
     "Borouge-Q4-2023-EN%20Financial%20Statements.pdf", True,
     "FY2023 audited statutory financial statements. Re-fetched, byte-identical."),
    ("https://www.borouge.com/en/investor-relations/Documents/IR%20Documents/"
     "Borouge-Q4-2022-EN%20Financial%20Statements.pdf", True,
     "FY2022 audited statutory financial statements — the fourth complete year, held "
     "as the depth check on the three the model carries. Re-fetched, byte-identical."),
    ("https://www.borouge.com/en/investor-relations/Documents/IR%20Documents/"
     "Q1%202026%20Financial%20Statements%20-%20statutory%20-%20English.pdf", True,
     "Q1-2026 reviewed interim statements. Re-fetched, byte-identical."),
    ("https://www.borouge.com/en/investor-relations/Documents/IR%20Documents/"
     "Borouge-Q2-2026-EN%20Borouge%20Financial%20Statements.pdf", True,
     "H1-2026 reviewed interim statements. Re-fetched, byte-identical."),
    ("https://www.adx.ae/english/pages/default.aspx", False,
     "Abu Dhabi Securities Exchange web portal — HTTP 403 at the egress proxy on every "
     "attempt. Not needed: the exchange's own monthly market-statistics workbooks were "
     "obtained separately and are used only to cross-check traded shares and market "
     "capitalisation, never as a source for a reported figure."),
]:
    R.record_primary_access(url, ok, SWEEP_DATE, note)

R.declare_study_year("2026", ["Q1 2026", "Q2 2026"])

# ---------------------------------------------------------------- RING 1 GLOBAL
f_rate = R.add(Ring.GLOBAL, "rate cycle & USD/FX regime", FindingClass.S,
    "Secured Overnight Financing Rate 3.65% and the US 10-year Treasury note at 4.65%. "
    "The dirham is hard-pegged to the dollar at 3.6725 and the Central Bank of the UAE "
    "Base Rate has tracked the Federal Reserve to 3.65%, held since 17 June 2026",
    "Federal Reserve Bank of New York SOFR publication; US Treasury constant-maturity "
    "yields; Central Bank of the UAE Base Rate", REG, "2026-08-06",
    model_impact="Borouge reports and is financed in dollars, so the peg makes the "
                 "dollar the natural valuation currency. The 10-year sets the risk-free "
                 "rate and the floating leg of the debt book prices off SOFR.")

f_oversupply = R.add(Ring.GLOBAL, "commodity complex (input/output)", FindingClass.B,
    "Global polyethylene nameplate capacity rises 22% between 2026 and 2034, from 158 "
    "to 193 million tonnes; polypropylene rises 20%, from 125 to 151 million tonnes. "
    "Producer consensus on the return to the 1992-2021 average operating rate has moved "
    "out to 2032, from 2030 a year earlier",
    "OPIS, Asia Petrochemical Industry Conference briefing (capacity); ICIS Asian "
    "Chemical Connections (operating-rate consensus)", PRESS, "2026-05-29",
    model_impact="BASE CHANGER, and the reason the forecast price path settles BELOW the "
                 "2023-24 level rather than back at it. Structural oversupply is "
                 "untouched by the regional disruption, so benchmark prices give back "
                 "the shortage premium and then keep drifting.")

f_brent = R.add(Ring.GLOBAL, "commodity complex (input/output)", FindingClass.S,
    "Brent averaged USD 69/bbl in 2025 and is expected to average USD 82/bbl in 2026 "
    "and USD 65/bbl in 2027, the 2026 figure lifted by the Strait of Hormuz disruption",
    "US Energy Information Administration, Short-Term Energy Outlook, July 2026",
    REG, "2026-07-31",
    model_impact="Sets the shape of the naphtha-linked marginal cost that anchors the "
                 "polyolefin benchmark: a 2026 spike that unwinds, not a new level.")

f_demand = R.add(Ring.GLOBAL, "global sector demand", FindingClass.S,
    "World real output growing about 3.0% in 2026 on the July update, revised up on "
    "front-loaded trade but with the Fund flagging war and technology crosscurrents",
    "International Monetary Fund, World Economic Outlook Update, July 2026",
    REG, "2026-07-08",
    model_impact="Polyolefin demand grows roughly with world output; carried as the "
                 "backdrop against which capacity growth of 20-22% is the binding side "
                 "of the balance, not demand.")

f_hormuz = R.add(Ring.GLOBAL, "trade / sanctions / supply chains", FindingClass.B,
    "The Strait of Hormuz was disrupted through the first half of 2026. A United "
    "States-Iran memorandum of understanding was signed on 18 June 2026 to end the "
    "conflict and reopen the strait; the Energy Information Administration's July "
    "outlook expects most shut-in production back by the end of 2026",
    "US Energy Information Administration, Short-Term Energy Outlook, July 2026, "
    "recording the 18 June 2026 memorandum", REG, "2026-06-18",
    model_impact="BASE CHANGER and the study's first contested judgement. Ruwais ships "
                 "through Hormuz; the strait is the single variable separating the two "
                 "published forecast constructions. Whether it reopens on the "
                 "memorandum's timetable is not knowable, so both paths are carried.")

# --------------------------------------------------------------- RING 2 COUNTRY
f_uae_macro = R.add(Ring.COUNTRY, "sovereign macro (inflation, policy rate, FX/deval risk)",
    FindingClass.D,
    "Central Bank of the UAE Quarterly Economic Review, June 2026: inflation forecast "
    "2.3% for 2026 and 1.9% for 2027; real GDP growth 6.2% actual for 2025, forecast "
    "1.7% for 2026 and 9.8% for 2027. The IMF's April 2026 vintage carries 3.1% for "
    "2026, cut from 5.0% in October",
    "Central Bank of the UAE, Quarterly Economic Review, June 2026; International "
    "Monetary Fund country page, April 2026 vintage", REG, "2026-06-30",
    model_impact="The 2.1% inflation average escalates the domestic fixed-cost leg of "
                 "the unit build — and only that leg. Traded inputs escalate on their "
                 "own commodity paths, never on this index.")

f_sovereign = R.add(Ring.COUNTRY, "sovereign macro (inflation, policy rate, FX/deval risk)",
    FindingClass.D,
    "United Arab Emirates: Aa2 rating, adjusted default spread 0.42%, country risk "
    "premium 0.64%, total equity risk premium 4.87% against a mature-market 4.23%. No "
    "sovereign credit-default-swap quote is carried in the file for the UAE",
    "Aswath Damodaran, 'Country Default Spreads and Risk Premiums', "
    "pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/ctryprem.html, file dated "
    "5 January 2026, United Arab Emirates row read fresh", PMD, "2026-01-05",
    model_impact="Country risk enters ONCE, inside the equity risk premium. The "
                 "risk-free rate is normalised by the sovereign's own default spread so "
                 "the same risk is not charged twice. Both equity-risk-premium bases are "
                 "published because the CDS basis is unavailable for this sovereign.")

f_uae_bond = R.add(Ring.COUNTRY, "sovereign macro (inflation, policy rate, FX/deval risk)",
    FindingClass.S,
    "UAE Ministry of Finance dirham Treasury bond and sukuk auction, July 2026: the "
    "January-2031 T-Bond cleared at 4.48%. The same programme's January 2026 final "
    "terms carried a 3.90% coupon",
    "UAE Ministry of Finance auction result reported by the Emirates News Agency (WAM); "
    "Ministry of Finance Treasury Bonds Programme Final Terms, 29 January 2026",
    REG, "2026-07-30",
    model_impact="The dirham construction of the risk-free rate. It sits 0.36% below "
                 "the dollar construction after each is normalised, and under a hard peg "
                 "that gap is reported rather than reconciled away.")

f_tax = R.add(Ring.COUNTRY, "regulatory environment (regulator, caps, tariffs, tax/subsidy)",
    FindingClass.D,
    "United Arab Emirates headline corporate income tax 9%. Borouge's own effective "
    "rate ran 28.57%, 29.01% and 28.62% across the three audited years, because the "
    "group's profits are taxed under the Abu Dhabi emirate-level fiscal regime that "
    "pre-dates the federal tax, not at the 9% federal headline",
    "Damodaran country file corporate-tax column (headline); Borouge plc audited "
    "consolidated financial statements FY2023-FY2025, tax note (the rate that binds)",
    CO, "2025-12-31",
    model_impact="The forecast carries the company's OWN three-year mean effective rate "
                 "of 28.74%, not the 9% headline. Using the headline would overstate "
                 "net operating profit after tax by roughly a fifth.")

f_fiscal = R.add(Ring.COUNTRY, "fiscal / political events with sector read-through",
    FindingClass.B,
    "ADNOC and OMV completed the formation of Borouge Group International AG on 31 "
    "March 2026, each holding 46.94%, combining Borouge and Borealis and acquiring Nova "
    "Chemicals. Borouge plc remains separately listed on the Abu Dhabi Securities "
    "Exchange; a tender offer converting Borouge plc shares into Borouge Group "
    "International AG shares is expected in 2027, subject to market conditions and UAE "
    "Capital Market Authority approval",
    "ADNOC press release 19 March 2026; OMV press release 31 March 2026; Borouge plc "
    "H1-2026 earnings release", CO, "2026-03-31",
    model_impact="Sets the terminal horizon of the security being valued: this study "
                 "values Borouge plc as it stands, on the assets it owns. The tender "
                 "offer is carried as a catalyst and a caveat, not as a driver, because "
                 "no exchange ratio has been published.")

# -------------------------------------------------------------- RING 3 INDUSTRY
f_balance = R.add(Ring.INDUSTRY, "demand drivers & capacity/supply balance", FindingClass.B,
    "The polyolefin cycle is in a capacity-led trough: 20-22% of new nameplate capacity "
    "arriving to 2034 against demand growing with world output, and the industry's own "
    "consensus on recovery pushed to 2032",
    "OPIS capacity outlook; ICIS Asian Chemical Connections operating-rate consensus",
    PRESS, "2026-05-29",
    model_impact="Drives the benchmark price path DOWN through the explicit window and "
                 "caps the terminal margin. It is the reason the normalisation "
                 "construction does not return prices to the 2023-24 level.")

f_price = R.add(Ring.INDUSTRY, "pricing", FindingClass.D,
    "Borouge discloses its own realised benchmark and premium for each product every "
    "quarter. Across the three audited years polyethylene revenue per tonne ran 1.0676 "
    "times the benchmark-plus-premium construct and polypropylene 1.0321 times; in "
    "H1-2026 those residuals widened to 1.0947 and 1.0186",
    "Borouge plc Management Discussion & Analysis, FY2023, FY2024, FY2025 and H1-2026, "
    "reconciled against the audited revenue line in each year",
    IR, "2026-07-27",
    model_impact="The realisation residual is the bridge from a published benchmark to "
                 "the company's own printed top line. The forecast carries the audited "
                 "three-year mean, NOT the wider half-year figure, because the H1-2026 "
                 "widening is a shortage artefact.")

f_entrants = R.add(Ring.INDUSTRY, "new entrants (named-competitor level)", FindingClass.S,
    "Borouge 4 at Ruwais adds 1.4 million tonnes a year of polyethylene and makes the "
    "site the world's largest single polyolefin complex. It is owned 70% by ADNOC and "
    "30% by OMV — Borouge plc owns none of it",
    "ADNOC press release, 19 March 2026; ADNOC and OMV completion announcement, "
    "31 March 2026", CO, "2026-03-19",
    model_impact="Decisive for terminal growth. The largest capacity addition in the "
                 "company's own back yard accrues to its parents, not to it, so terminal "
                 "growth is set at long-run inflation and no volume ramp is modelled.")

f_tech = R.add(Ring.INDUSTRY, "technology substitution", FindingClass.C,
    "No substitution threat to polyolefins over the valuation horizon: the pressure is "
    "regulatory (recycled-content mandates, single-use restrictions) and shows up as "
    "demand-growth drag and reinvestment need rather than displacement of the polymer",
    "Borouge plc Annual Report 2025, sustainability and circular-economy discussion",
    CO, "2025-12-31", model_impact="")

f_competitors = R.add(Ring.INDUSTRY, "competitor capacity / price moves (named)",
    FindingClass.S,
    "Eleven listed polyolefin and diversified-chemical peers observed: SABIC, Saudi "
    "Kayan, Yansab, Industries Qatar, LyondellBasell, Dow, Westlake, Braskem, Formosa "
    "Plastics, LG Chem and Petronas Chemicals. NINE of the eleven are loss-making on "
    "trailing net income and two carry no defined enterprise-value-to-EBITDA multiple",
    "stockanalysis.com company statistics pages (nine of eleven); TradingView and "
    "PitchBook company profile (Industries Qatar)", AGG, "2026-08-09",
    model_impact="CROSS-CHECK ONLY, never a source for a Borouge figure. It is the "
                 "evidence that kills the naive peer median: a 13.4x median built on "
                 "collapsed trough EBITDA is a denominator artefact, so the relative "
                 "lens is rebuilt on three through-cycle anchors instead.")

# --------------------------------------------------------------- RING 4 COMPANY
f_fs = R.add(Ring.COMPANY, "official financial statements", FindingClass.D,
    "FY2025 audited statutory financial statements — full set with auditor's report, "
    "statement of financial position, statement of profit or loss and other "
    "comprehensive income, statement of changes in equity, statement of cash flows and "
    "notes. Operating profit and profit before tax rebuild to the filed figure to the "
    "dollar",
    "Borouge plc audited consolidated financial statements for the year ended 31 "
    "December 2025 (Ernst & Young), read from borouge.com and verified byte-identical",
    CO, "2025-12-31", is_fs_data=True, fiscal_period="FY2025", url=IRLIB,
    model_impact="The FY2025 historical column of the income statement, balance sheet "
                 "and cash flow, and the opening balance sheet the forecast rolls "
                 "forward from.")

f_fs24 = R.add(Ring.COMPANY, "official financial statements", FindingClass.D,
    "FY2024 audited statutory financial statements — full set, and the comparative "
    "column against which the FY2025 filing is checked. Rebuilds to the filed operating "
    "profit and profit before tax to the dollar",
    "Borouge plc audited consolidated financial statements for the year ended 31 "
    "December 2024 (Ernst & Young), read from borouge.com and verified byte-identical",
    CO, "2024-12-31", is_fs_data=True, fiscal_period="FY2024", url=IRLIB,
    model_impact="The FY2024 historical column, and one of the three years the "
                 "per-tonne cost stack and the realisation residual are measured over.")

f_fs23 = R.add(Ring.COMPANY, "official financial statements", FindingClass.D,
    "FY2023 audited statutory financial statements — full set, signed 31 January 2024. "
    "Rebuilds to the filed operating profit and profit before tax to the dollar",
    "Borouge plc audited consolidated financial statements for the year ended 31 "
    "December 2023 (Ernst & Young), read from borouge.com and verified byte-identical",
    CO, "2023-12-31", is_fs_data=True, fiscal_period="FY2023", url=IRLIB,
    model_impact="The FY2023 historical column and the earliest of the three years the "
                 "cost stack, the tax rate and the asset-conversion cycle are measured "
                 "over.")

f_fs22 = R.add(Ring.COMPANY, "official financial statements", FindingClass.D,
    "FY2022 audited statutory financial statements — a fourth complete year, obtained "
    "and read but deliberately NOT carried as a model column: 2022 is the post-listing "
    "peak-price year and including it would flatter every through-cycle average the "
    "study takes",
    "Borouge plc audited consolidated financial statements for the year ended 31 "
    "December 2022 (Ernst & Young), read from borouge.com and verified byte-identical",
    CO, "2022-12-31", is_fs_data=True, fiscal_period="FY2022", url=IRLIB,
    model_impact="Held as the depth check on the three carried years rather than as a "
                 "fourth column. Its exclusion is a stated judgement, not a gap.")

f_q1 = R.add(Ring.COMPANY, "regular disclosures", FindingClass.D,
    "Q1-2026 reviewed interim statements and Management Discussion & Analysis: the "
    "first quarter of the study year, swept in before the build, not discovered after. "
    "It carries the first disclosed evidence of the feedstock step-up and the logistics "
    "cost increase",
    "Borouge plc Q1-2026 condensed consolidated interim financial statements (reviewed) "
    "and Q1-2026 Management Discussion & Analysis", CO, "2026-03-31",
    is_fs_data=True, fiscal_period="Q1 2026", url=IRLIB,
    model_impact="Sets the starting point of the 2026 forecast year and, with H1, fixes "
                 "the disruption-year cost levels the two constructions diverge from.")

f_h1 = R.add(Ring.COMPANY, "regular disclosures", FindingClass.D,
    "H1-2026 reviewed interim statements and Management Discussion & Analysis: "
    "feedstock at USD 395 per tonne of production against USD 265, 247 and 256 in the "
    "three audited years, a 54% step the company attributes to buying propylene at "
    "market prices while the Olefins Conversion Unit was idled for want of ethane; "
    "selling and distribution at USD 177 per tonne against USD 78, 88 and 77, on "
    "alternative logistics routes; the interim effective tax rate at 25.10%",
    "Borouge plc condensed consolidated interim financial statements for the six months "
    "ended 30 June 2026 (reviewed) and Q2-2026 Management Discussion & Analysis",
    CO, "2026-06-30", is_fs_data=True, fiscal_period="Q2 2026", url=IRLIB,
    model_impact="Every disruption-year cost level in the forecast, and the evidence "
                 "that the step is mechanism-specific — an idled conversion unit and a "
                 "re-routed shipping lane — rather than a permanent margin reset.")

f_ir = R.add(Ring.COMPANY, "IR communications (calls, presentations, releases)",
    FindingClass.D,
    "Earnings presentations and releases for FY2023, FY2024, FY2025 and H1-2026 carry "
    "the physical unit build no financial statement discloses: tonnes produced and "
    "sold by product, utilisation, the benchmark price and the premium Borouge realises "
    "over it, and the split of production cost. H1-2026 total sales of 873kt in Q2 "
    "include 54kt sourced from Borealis and the China compounding plant",
    "Borouge plc earnings presentations and earnings releases, FY2023, FY2024, FY2025 "
    "and Q2-2026", IR, "2026-07-27", url=IRLIB,
    model_impact="Volume, price and per-unit cost — the whole ground-up revenue and "
                 "cost build. The audited statements confirm the money totals those "
                 "physicals roll up to, and compute.py asserts the reconciliation.")

f_guidance = R.add(Ring.COMPANY, "strategic plans & guidance", FindingClass.D,
    "H1-2026 outlook: second-half utilisation recovery depends on free movement through "
    "the Strait of Hormuz, with facilities positioned for a fast recovery subject to "
    "feedstock; realised pricing expected to stay elevated in the short term and "
    "logistics costs to remain high. The annual dividend intention of 16.2 fils per "
    "share remains in place",
    "Borouge plc H1-2026 earnings release, outlook section", CO, "2026-07-27",
    model_impact="The company's own words are the source of the two-construction split: "
                 "it names the strait as the binding variable and declines to guide "
                 "past it. The dividend intention supports the terminal payout.")

f_b4 = R.add(Ring.COMPANY, "one-off base-resetting transactions", FindingClass.B,
    "Under the Asset Usage Agreement signed in March 2026, Borouge plc operates the "
    "Borouge 4 assets it does not own. ADNOC expects the agreement to deliver Borouge "
    "plc about USD 400 million of cumulative net profit over three years and roughly "
    "10% annual earnings accretion after ramp-up; recontribution of Borouge 4 into "
    "Borouge Group International is not expected before 2029, deferred from an earlier "
    "date",
    "ADNOC press release, 19 March 2026; Borouge plc H1-2026 interim financial "
    "statements and Q2-2026 Management Discussion & Analysis", CO, "2026-03-19",
    model_impact="Borouge plc's ownership of Borouge 4 is carried at ZERO, because that "
                 "is what the agreement says. The fee stream is real but is neither "
                 "capitalised as owned capacity nor extrapolated past the disclosed "
                 "three-year figure.")

f_own = R.add(Ring.COMPANY, "ownership / stake changes (named-transaction rule)",
    FindingClass.B,
    "Named transaction searched and found: ADNOC and OMV completed the formation of "
    "Borouge Group International AG on 31 March 2026, each holding 46.94% of the "
    "combined entity. Borouge plc has been majority-held by Borouge International "
    "since March 2026; the free float remains listed on the Abu Dhabi Securities "
    "Exchange under BOROUGE, ISIN AEE01072B225",
    "OMV press release, 'OMV and XRG complete transactions to create Borouge "
    "International', 31 March 2026; Borouge plc H1-2026 earnings release",
    CO, "2026-03-31",
    model_impact="No stake percentage is estimated anywhere in this study — the specific "
                 "transaction was searched and its published terms carried. Confirms "
                 "the minority interest on the balance sheet is a 0.9% subsidiary "
                 "minority, not a stake in the parent structure.")

f_capital = R.add(Ring.COMPANY, "management & capital actions", FindingClass.D,
    "30,057,691,583 ordinary shares of USD 0.16 in issue; weighted average 29,937,557,774 "
    "for FY2025 after treasury purchases, whose cumulative cost reached USD 216.7 "
    "million by 30 June 2026 from USD 158.2 million at the FY2025 year end. Related-party "
    "term facilities of USD 2.8 billion and a drawn revolving facility with Borouge "
    "Group International AG",
    "Borouge plc FY2025 audited financial statements, notes 14, 29 and 31; H1-2026 "
    "interim statements, note 11(iv)", CO, "2026-06-30", is_fs_data=True,
    model_impact="Share count for every per-share figure, and the debt book that the "
                 "cost-of-debt test prices: the related-party facilities at 5.52% "
                 "against an arm's-length 5.55%, inside by 0.03%.")

# ------------------------------------------------------------- NEGATIVE RESULTS
f_neg_ethane = R.add_negative(Ring.COMPANY, "strategic plans & guidance",
    "Borouge ethane feedstock pricing formula, ADNOC supply agreement terms, contracted "
    "feedstock price escalation — searched across all four annual reports, all audited "
    "statements and every Management Discussion & Analysis. The company discloses the "
    "cost per tonne it incurred but never the formula or the contract term, so no "
    "forward escalator can be built from a source. Real escalation is therefore carried "
    "at zero and flagged, not invented", SWEEP_DATE)

f_neg_segment = R.add_negative(Ring.COMPANY, "regular disclosures",
    "Borouge segmental profitability by product — polyethylene versus polypropylene "
    "operating profit, segment assets, segment capital employed. The company reports as "
    "a single operating segment; volume and price are disclosed by product but cost and "
    "profit are not. The unit build therefore allocates cost across products on the "
    "disclosed physical drivers and the gap is stated", SWEEP_DATE)

f_neg_cds = R.add_negative(Ring.COUNTRY, "sovereign macro (inflation, policy rate, "
    "FX/deval risk)",
    "United Arab Emirates sovereign credit-default-swap quote — no CDS-based spread is "
    "carried for the UAE in the Damodaran country file. Both equity-risk-premium bases "
    "are published on the rating basis and the absence is stated rather than filled "
    "with a neighbouring sovereign's quote", SWEEP_DATE)

f_neg_tender = R.add_negative(Ring.COMPANY, "one-off base-resetting transactions",
    "Borouge Group International tender offer exchange ratio, valuation terms or "
    "prospectus — searched at ADNOC, OMV and Borouge investor relations. No ratio has "
    "been published; the offer is expected in 2027 subject to market conditions and "
    "regulatory approval. It is therefore carried as a catalyst and a caveat, and no "
    "conversion value enters any lens", SWEEP_DATE)

f_neg_capex = R.add_negative(Ring.COMPANY, "strategic plans & guidance",
    "Borouge plc multi-year capital-expenditure plan beyond the current year — the "
    "company guides the year ahead but publishes no medium-term programme. Steady-state "
    "maintenance capital expenditure is therefore set from the company's own three-year "
    "outturn of USD 199m, 167m and 308m against a below-USD-300m guide, and sensitised",
    SWEEP_DATE)

# ------------------------------------------------------------- DRIVER GATE TABLE
R.add_driver("Sales volume by product (kt)", DriverMode.BOTTOM_UP,
    "Nameplate capacity by product times a disclosed utilisation path. Utilisation, "
    "tonnes produced and tonnes sold are all published by product in the company's own "
    "Management Discussion & Analysis, and the forecast path is anchored on the rates "
    "the plant actually demonstrated in 2024 and 2025.",
    [f_ir, f_fs, f_fs24, f_fs23, f_guidance, f_hormuz])

R.add_driver("Realised price by product (USD/t)", DriverMode.BOTTOM_UP,
    "Published benchmark plus the company's own published premium, times a realisation "
    "residual measured against three years of audited revenue. Every leg is disclosed; "
    "nothing is solved backwards out of a target.",
    [f_price, f_ir, f_oversupply, f_brent])

R.add_driver("Feedstock cost (USD/t of production)", DriverMode.BOTTOM_UP,
    "Cost per tonne of production from the disclosed cost line over disclosed tonnes, "
    "split into the contracted ethane leg and the market-priced propylene leg, with "
    "the market share of the mix as the forecast driver. The traded leg escalates on "
    "its own price path, never on the domestic inflation index.",
    [f_h1, f_q1, f_ir, f_brent])

R.add_driver("Other production cost (fixed and variable)", DriverMode.BOTTOM_UP,
    "Regressed across the three audited years into a USD 663m fixed leg and a USD 201 "
    "per-tonne variable leg. The fixed leg escalates on UAE consumer inflation — the "
    "only leg that does — and the variable leg moves with tonnes.",
    [f_fs, f_fs24, f_fs23, f_ir, f_uae_macro])

R.add_driver("Selling and distribution (USD/t sold)", DriverMode.BOTTOM_UP,
    "Per tonne sold from the disclosed line, at USD 78, 88 and 77 across the audited "
    "years against USD 177 in H1-2026 on re-routed shipping. The forecast path is the "
    "route decision, which is why it is the second variable the two constructions split "
    "on.",
    [f_h1, f_ir, f_hormuz])

R.add_driver("Effective tax rate", DriverMode.BOTTOM_UP,
    "The company's own three-year mean of 28.74%, taken from the tax note, not the 9% "
    "federal headline. The H1-2026 interim rate of 25.10% is disclosed and deliberately "
    "not carried forward.",
    [f_tax, f_fs, f_h1])

R.add_driver("Working capital and the balance-sheet roll-forward", DriverMode.BOTTOM_UP,
    "Days sales outstanding 51, days inventory 62, days payable 92, a 20-day cash cycle, "
    "each measured from the audited statements. Receivables, inventory and payables are "
    "projected from those days against forecast revenue and cost — no plug.",
    [f_fs, f_capital])

R.add_driver("Cost of capital", DriverMode.BOTTOM_UP,
    "Risk-free rate normalised by the sovereign's own default spread; equity risk "
    "premium from the sovereign's own row; beta from the stock's own five-year weekly "
    "regression against its own market, published beside a sector bottom-up beta "
    "because the own-stock estimate is weak; marginal cost of debt tested against the "
    "sovereign and against the related-party facilities actually in place.",
    [f_sovereign, f_uae_bond, f_rate, f_capital])

R.add_driver("Terminal growth", DriverMode.BOTTOM_UP,
    "Long-run dollar inflation, on the specific ground that Borouge plc's owned capacity "
    "is fixed: the 1.4 million tonne Borouge 4 expansion next door is owned by its "
    "parents, not by it. This is a driver read off a named transaction, not a convention.",
    [f_entrants, f_b4, f_fiscal])

R.add_driver("Maintenance capital expenditure", DriverMode.TOP_DOWN,
    "No medium-term capital programme is published, so steady-state maintenance capital "
    "expenditure is set from the company's own three-year outturn against its "
    "current-year guide, and sensitised. Flagged as the one materially top-down driver "
    "in the build.",
    [f_neg_capex, f_fs])

R.add_driver("Ethane contract escalation", DriverMode.TOP_DOWN,
    "Carried at zero real escalation because the pricing formula is not disclosed. The "
    "gap is flagged rather than filled with an assumed formula, and the sensitivity "
    "shows what a non-zero escalator would cost.",
    [f_neg_ethane])

# ------------------------------------------------------------------------ OUTPUT
if __name__ == '__main__':
    errors, warnings = R.validate()
    R.to_json(os.path.join(HERE, 'sweep_register.json'))
    print(R.qc_line())
    print(f"\nfindings: {len(R.findings)} | drivers: {len(R.drivers)} | "
          f"primary-access attempts: {len(R.primary_access)}")
    if errors:
        print(f"\nVALIDATOR ERRORS ({len(errors)}) — disclosed, not suppressed:")
        for e in errors:
            print(f"  ! {e}")
    if warnings:
        print(f"\nwarnings ({len(warnings)}):")
        for w in warnings:
            print(f"  - {w}")
    fr = R.check_freshness("2026-08-09")
    print(f"\nfreshness: {fr or 'OK — sweep and delivery same day'}")
    if errors:
        sys.exit(1)
