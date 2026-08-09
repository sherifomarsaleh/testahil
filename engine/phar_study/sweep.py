"""PHAR (EIPICO) — four-ring Information Sweep register.

Runs BEFORE any forecast driver is set. Every mandatory category of every ring is
closed by a dated finding or a dated negative search.

SOURCING NOTE, recorded rather than hidden: the company's OWN website and investor-
relations pages were reachable and are the build source for every historical figure —
seven complete audited financial years (FY2019-FY2025) plus the investor presentation
and the board's own operating statistics. The exchange's disclosure portal was NOT
reachable: every request, scripted or browser-rendered, is answered with a bot-defence
challenge page. That is why the FY2026 first-quarter interim is carried as a NEGATIVE
result and as a labelled cross-check, and is not in the build path.
"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from research_sweep import (SweepRegister, AssetClass, Ring, FindingClass,
                            SourceType, DriverMode)

SWEEP_DATE = "2026-08-09"
R = SweepRegister("PHAR", AssetClass.STOCK, SWEEP_DATE)
CO, IR, REG, PMD, PRESS, AGG = (SourceType.COMPANY_OFFICIAL, SourceType.COMPANY_IR,
                                SourceType.REGULATOR_OFFICIAL, SourceType.PRIMARY_MARKET_DATA,
                                SourceType.REPUTABLE_PRESS, SourceType.AGGREGATOR)
SITE = "https://www.eipico.com.eg/"
AR25 = "https://www.eipico.com.eg/DataImages/HTML/File1699.pdf"
AR24 = "https://www.eipico.com.eg/DataImages/HTML/File1536.pdf"
AR23 = "https://www.eipico.com.eg/DataImages/HTML/File1138.pdf"
AR22 = "https://www.eipico.com.eg/DataImages/HTML/File1202.pdf"
DECK = "https://www.eipico.com.eg/DataImages/HTML/File1585.pdf"

# ---- primary-source access, logged whether it succeeded or failed -------------
R.record_primary_access(SITE, True, SWEEP_DATE,
                        "Corporate site reachable; Investor Relations -> Annual Reports carries "
                        "FY2019 through FY2025 as complete PDFs, each containing the auditor's "
                        "report and both the separate and the consolidated financial statements "
                        "with full notes.")
R.record_primary_access("https://www.eipico.com.eg/HTML.aspx?name=Eipico3_AnnualReports", True,
                        SWEEP_DATE, "Seven annual reports downloaded; FY2022-FY2025 used.")
R.record_primary_access(DECK, True, SWEEP_DATE,
                        "Investor presentation downloaded — production lines and capacities per "
                        "shift, export pack volumes, market ranks, EIPICO 3 and Arab API detail.")
R.record_primary_access("company-supplied issued financial statements", True, "2026-08-11",
                        "The reviewed FY2026 first-quarter interim and the separately issued "
                        "FY2023 and FY2024 audited consolidated statements, all English "
                        "translations issued by the auditor, were supplied directly after the "
                        "first issue of this study. This CLOSES the study-year quarter that "
                        "could not be reached online.")
R.record_primary_access("https://www.egx.com.eg/en/DisclosureNews.aspx", False, SWEEP_DATE,
                        "Exchange disclosure portal NOT reachable. Every request returns a "
                        "48KB bot-defence challenge page instead of content; a headless-browser "
                        "render was also attempted and the browser could not be routed through "
                        "this environment's egress proxy. Consequence: the FY2026 first-quarter "
                        "interim could not be obtained from an official home.")
R.record_primary_access("https://disclosure.efsa.gov.eg/", False, SWEEP_DATE,
                        "Regulator disclosure sub-domain refused at the egress proxy "
                        "(connect_rejected, gateway 502).")
R.record_primary_access("https://www.cbe.org.eg/en/auctions/egp-t-bonds-fixed-coupon", False,
                        SWEEP_DATE,
                        "Central bank fixed-coupon treasury bond auction page rejected the "
                        "request at its own web application firewall. The ten-year local-currency "
                        "yield is therefore carried from the dated house reference print and "
                        "sensitised rather than re-read live.")

R.declare_study_year("2026", ["Q1-2026"])

# ---------------------------------------------------------------- RING 1 GLOBAL
f_rate = R.add(Ring.GLOBAL, "rate cycle & USD/FX regime", FindingClass.S,
    "Global easing under way, against which Egypt's own policy rate normalises. Egypt's "
    "sovereign credit-default-swap spread stands at 3.41% and its adjusted default spread "
    "on the Caa1 rating basis at 6.37%, with a total equity risk premium of 9.41% on the "
    "swap basis and 13.94% on the rating basis",
    "Country default spreads and risk premiums file, Egypt row, last updated 5 January 2026, "
    "read live on 9 August 2026", REG, "2026-01-05",
    url="https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/ctryprem.html",
    model_impact="Sets the entire cost-of-capital build: the sovereign swap spread is netted "
                 "out of the local-currency risk-free rate and the equity risk premium is "
                 "taken from the same row, so country risk is charged exactly once. Both the "
                 "swap and the rating construction are published.")

f_api = R.add(Ring.GLOBAL, "commodity complex (input/output)", FindingClass.S,
    "Active pharmaceutical ingredients are the dominant input and are imported. Raw materials "
    "are 54.9% of the company's own disclosed production cost and packaging materials a "
    "further 24.6%; both are priced in hard currency at the point of purchase",
    "Cost of sales note (26), audited consolidated financial statements FY2025", CO,
    "2026-03-01", url=AR25, is_fs_data=True, fiscal_period="FY2025",
    model_impact="Forces the cost stack to carry ONE ESCALATOR PER DRIVER CLASS: imported "
                 "ingredients and the imported share of packaging escalate on a hard-currency "
                 "price path passed through the model's own exchange-rate path, never on a "
                 "domestic inflation proxy. Applying a single blended index across "
                 "physically distinct cost lines is precisely the error this rule exists to "
                 "prevent.")

f_gdem = R.add(Ring.GLOBAL, "global sector demand", FindingClass.S,
    "The company exports to more than 60 countries and reports 60 million packs a year of "
    "export volume, worth USD 60 million in FY2025 against USD 54.7 million in FY2024 — 10% "
    "growth in hard currency against 19% in Egyptian pounds",
    "Investor presentation, export reach page; board of directors' report FY2025", IR,
    "2026-03-28", url=DECK,
    model_impact="Export revenue is forecast as pack volume times a US-dollar price times the "
                 "model's own exchange-rate path — NOT extrapolated from its Egyptian-pound "
                 "growth rate, which was inflated by translation.")

f_trade = R.add(Ring.GLOBAL, "trade / sanctions / supply chains", FindingClass.S,
    "The company holds a strategic raw-material stockpile it states is sufficient for at "
    "least eight months, taken deliberately in response to regional supply-chain risk",
    "Chairman's statement to the ordinary general assembly, 28 March 2026, reproduced on the "
    "company's own press-release page", IR, "2026-03-28",
    url="https://www.eipico.com.eg/NWSDetails.aspx?id=262",
    model_impact="Explains and justifies 268 days of inventory. The working-capital forecast "
                 "unwinds inventory days only slowly because the position is a stated policy "
                 "choice, not a failure of control.")

# ---------------------------------------------------------------- RING 2 COUNTRY
f_macro = R.add(Ring.COUNTRY, "sovereign macro (inflation, policy rate, FX/deval risk)",
    FindingClass.S,
    "The Egyptian pound averaged 47.74 to the US dollar in FY2024 and 49.48 in FY2025, "
    "closing at 50.89 and 49.52 respectively — a 3.6% average-rate move and a small "
    "year-end appreciation, after the step devaluation of March 2024",
    "Foreign-currency risk note (36), audited consolidated financial statements FY2025 and "
    "FY2024", CO, "2026-03-01", url=AR25, is_fs_data=True, fiscal_period="FY2025",
    model_impact="Anchors the exchange-rate path. Because the real exchange rate appreciated "
                 "while domestic inflation ran far above the United States', the path assumes "
                 "a partial reversal at about 4% a year narrowing to 3%.")

f_reg = R.add(Ring.COUNTRY, "regulatory environment (regulator, caps, tariffs, tax/subsidy)",
    FindingClass.S,
    "Medicine prices in Egypt are set administratively by the Egyptian Drug Authority; the "
    "authority also licences manufacturing facilities. It granted the biologicals plant its "
    "licence in December 2025. The Egyptian corporate income tax rate is 22.5%",
    "Company announcement of the drug authority licence, December 2025; corporate tax-rate "
    "column of the country risk-premium file", REG, "2025-12-11",
    url="https://www.eipico.com.eg/NWSDetails.aspx?id=256",
    model_impact="Two consequences. Domestic price per pack is forecast to track inflation "
                 "with no real gain, because the company cannot set its own domestic price. "
                 "And the December-2025 licence is what makes the construction balance start "
                 "depreciating in the forecast — the largest single mechanical change in it.")

f_fiscal = R.add(Ring.COUNTRY, "fiscal / political events with sector read-through",
    FindingClass.S,
    "Pharmaceutical localisation is explicit Egyptian industrial policy. The deputy prime "
    "minister for industrial development attended the foundation-stone ceremony for the "
    "active-ingredient plant in the Suez Canal Economic Zone in January 2026, a USD 165 "
    "million project the company chairs",
    "Company press release, 15 January 2026", IR, "2026-01-15",
    url="https://www.eipico.com.eg/NWSDetails.aspx?id=258",
    model_impact="Supports the export and volume path and the assumption that the company "
                 "faces no policy risk to its capacity expansion; the associated plant is a "
                 "separate legal entity and is NOT consolidated, so it enters only through "
                 "the associate line.")

# --------------------------------------------------------------- RING 3 INDUSTRY
f_demand = R.add(Ring.INDUSTRY, "demand drivers & capacity/supply balance", FindingClass.S,
    "The company produced 2,208 million units in FY2025 against 3,383 million of its own "
    "disclosed available capacity — 65% utilisation, up from 63% — and holds 54 production "
    "lines across three plants. Utilisation by dosage form ranges from 11% (soft capsules) "
    "to 221% (lyophilised ampoules, run beyond nameplate)",
    "Comparative statement of production quantities by pharmaceutical dosage form, board of "
    "directors' report FY2025", CO, "2026-03-28", url=AR25, fiscal_period="FY2025",
    model_impact="The volume path is NOT capacity-constrained, so incremental volume needs "
                 "little capital. This is why forecast capital expenditure falls from 14.3% "
                 "of revenue in FY2025 to about 3%.")

f_price = R.add(Ring.INDUSTRY, "pricing", FindingClass.S,
    "Realised price per domestic pack was EGP 21.54 in FY2025 against EGP 19.77 in FY2024, "
    "up 9.0%, while domestic pack volume rose 19.5%. Export realised price was USD 1.00 a "
    "pack",
    "Derived from the board's own disclosed pack volumes and the revenue note (25) channel "
    "split, audited FY2025 and FY2024", CO, "2026-03-28", url=AR25, fiscal_period="FY2025",
    model_impact="Splits revenue growth into its volume and price components separately for "
                 "the domestic and export books, which is what the ground-up rule requires "
                 "and what a blended growth rate would hide.")

f_entrants = R.add(Ring.INDUSTRY, "new entrants (named-competitor level)", FindingClass.C,
    "The company reports itself first in the Egyptian market by units sold and, for the "
    "first time in its history, second by value in January 2026, on independent prescription-"
    "audit data. It cites a 6.4% share of the local pharmacy and warehouse market",
    "Company results release citing the January-2026 independent market audit", IR,
    "2026-03-01", url="https://www.eipico.com.eg/NWSDetails.aspx?id=261",
    model_impact="")

f_tech = R.add(Ring.INDUSTRY, "technology substitution", FindingClass.S,
    "Biosimilars are the substitution event, and the company has moved to be on the right "
    "side of it: the new plant is described as the first in Egypt to manufacture biologicals "
    "and biosimilars from cell culture through to finished product, with a USD 100 million "
    "investment, and it launched its first biosimilar in December 2025. The published "
    "pipeline names trastuzumab, rituximab and adalimumab equivalents",
    "Company announcements of the plant licence and first biosimilar launch; investor "
    "presentation pipeline page", IR, "2025-12-11", url=DECK,
    model_impact="THE CRUX. The forecast charges this plant's depreciation and its interest "
                 "because both follow mechanically from the licence date, but carries NO "
                 "revenue line for it, because the company has published no volume, price or "
                 "utilisation guidance. The study therefore states in observable units how "
                 "much the plant must sell to justify the market price, rather than assuming "
                 "an answer.")

f_comp = R.add(Ring.INDUSTRY, "competitor capacity / price moves (named)", FindingClass.C,
    "The company is the largest Egyptian pharmaceutical exporter with 26% of national "
    "pharmaceutical export value; it is the largest operating subsidiary of the Arab Company "
    "for Drug Industries and Medical Appliances, which holds 51.34% of its shares",
    "Board of directors' report FY2025 and the shareholder-structure table in capital note "
    "(13)", CO, "2026-03-28", url=AR25, fiscal_period="FY2025",
    model_impact="")

# ---------------------------------------------------------------- RING 4 COMPANY
f_fs = R.add(Ring.COMPANY, "official financial statements", FindingClass.B,
    "Complete audited separate AND consolidated financial statements with the auditor's "
    "report and full notes for FY2022, FY2023, FY2024 and FY2025 — four consecutive audited "
    "years, three more than the floor and one more than the study standard requires — "
    "obtained from the company's own investor-relations page. FY2019 through FY2021 are also "
    "on the same page and were downloaded",
    "Annual Reports FY2022-FY2025, company investor-relations page", CO, "2026-03-01",
    url=AR25, is_fs_data=True, fiscal_period="FY2025",
    model_impact="Every historical income-statement, balance-sheet and cash-flow line in this "
                 "study is the audited consolidated figure or a disclosed note to it. The "
                 "income statement reconstructs to disclosed pre-tax profit within EGP 0.02 "
                 "million in each of the three modelled years.")

f_fs24 = R.add(Ring.COMPANY, "official financial statements", FindingClass.B,
    "FY2024 audited consolidated statements, cross-confirmed against the comparative column "
    "of the FY2025 filing", "Annual Report FY2024", CO, "2025-03-01", url=AR24,
    is_fs_data=True, fiscal_period="FY2024",
    model_impact="Second of the three modelled history years.")

f_fs23 = R.add(Ring.COMPANY, "official financial statements", FindingClass.B,
    "FY2023 audited consolidated statements, cross-confirmed against the comparative column "
    "of the FY2024 filing", "Annual Report FY2023", CO, "2024-03-01", url=AR23,
    is_fs_data=True, fiscal_period="FY2023",
    model_impact="Third of the three modelled history years.")

f_fs22 = R.add(Ring.COMPANY, "official financial statements", FindingClass.B,
    "FY2022 audited consolidated statements, carried as the fourth year for the traded-"
    "multiple history", "Annual Report FY2022", CO, "2023-03-01", url=AR22,
    is_fs_data=True, fiscal_period="FY2022",
    model_impact="Supplies FY2022 attributable profit for the company's own price-earnings "
                 "history, which anchors the relative lens.")

f_guid = R.add(Ring.COMPANY, "strategic plans & guidance", FindingClass.S,
    "The chairman told the March-2026 general assembly the company had reached a production "
    "value of EGP 10.8 billion and sales of EGP 9.8 billion, that the active-ingredient "
    "project is on schedule, and that the strategic raw-material stockpile covers at least "
    "eight months. No numerical revenue or earnings guidance for FY2026 was given",
    "General assembly report, company press-release page", IR, "2026-03-28",
    url="https://www.eipico.com.eg/NWSDetails.aspx?id=262",
    model_impact="No guidance exists to anchor the forecast to, so every forecast driver in "
                 "this study is built from disclosed history and stated policy. That absence "
                 "is itself the reason the crux is posed as a reverse valuation.")

f_disc = R.add(Ring.COMPANY, "regular disclosures", FindingClass.B,
    "The board's own report inside each annual report carries a full operating dataset that "
    "appears in no financial statement: production and sales by value and by pack, the "
    "channel split, production quantities and available capacity for twenty-one dosage "
    "forms, headcount, productivity, leverage ratios and a quarterly income summary",
    "Board of directors' report FY2025 and FY2024", CO, "2026-03-28", url=AR25,
    fiscal_period="FY2025",
    model_impact="This is what makes a genuine volume-times-price build possible rather than "
                 "a percentage-growth assertion.")

f_ir = R.add(Ring.COMPANY, "IR communications (calls, presentations, releases)", FindingClass.S,
    "Investor presentation giving 54 production lines with capacity per shift per year by "
    "dosage form, 414 products across 27 therapeutic groups, 1,238 products registered in 61 "
    "countries, about 5,000 employees, export reach of 60 million packs and USD 60 million a "
    "year, and the biologicals and active-ingredient project descriptions",
    "Company investor presentation, corporate website", IR, "2026-08-09", url=DECK,
    model_impact="Supplies the export pack volume that splits the export book into volume and "
                 "price, and the capacity detail behind the utilisation constraint. This is "
                 "the single most useful non-financial-statement source in the build.")

f_oneoff = R.add(Ring.COMPANY, "one-off base-resetting transactions", FindingClass.B,
    "The share count changed: the exchange's listing committee approved on 23 July 2025 an "
    "increase in issued and paid capital from EGP 1,487,557,500 to EGP 1,687,557,500 through "
    "20 million new shares, raising EGP 1,000 million. Weighted average shares for FY2025 "
    "were therefore 162.016 million against 168.756 million now in issue",
    "Capital note (13) and earnings-per-share note (34), audited FY2025", CO, "2026-03-01",
    url=AR25, is_fs_data=True, fiscal_period="FY2025",
    model_impact="Per-share values use the 168.756 million shares now in issue, not the "
                 "weighted average, because the valuation is of the company as it stands.")

f_stake = R.add(Ring.COMPANY, "ownership / stake changes (named-transaction rule)",
    FindingClass.B,
    "Named holdings, from the company's own register: the Arab Company for Drug Industries "
    "and Medical Appliances 51.34% (86,647,861 shares); the Medical Professions Investment "
    "Company 3.68%; the Federation of Medical Professions Syndicates 3.50%; its pension and "
    "benefits fund 4.84%; other shareholders 36.64%. On the other side, the company holds a "
    "named 30% interest in Batterjee Pharmaceutical (Saudi Arabia), fully paid at SAR "
    "35,900,976 equivalent, and a named 9.77%-plus interest in the Medical Professions "
    "Company for Pharmaceuticals acquired for EGP 211,167,305",
    "Capital note (13) shareholder table and investments note (8/3), audited FY2025", CO,
    "2026-03-01", url=AR25, is_fs_data=True, fiscal_period="FY2025",
    model_impact="No ownership driver is estimated. The associate stake is valued in the "
                 "enterprise-to-equity bridge on its normalised earnings rather than its "
                 "carrying value, because the carrying value of EGP 676 million sits against "
                 "an FY2025 contribution of EGP 495 million.")

f_capital = R.add(Ring.COMPANY, "management & capital actions", FindingClass.B,
    "The board proposed a dividend of exactly EGP 3.50 a share for FY2025 (EGP 590,645,125 "
    "on 168,755,750 shares), against exactly EGP 3.00 for FY2024 (EGP 446,267,250 on "
    "148,755,750 shares) — payout ratios of 41.0% and 40.7% of attributable profit",
    "Proposed profit-distribution table, board of directors' report FY2025", CO, "2026-03-28",
    url=AR25, is_fs_data=True, fiscal_period="FY2025",
    model_impact="Sets the 40% payout in the equity roll-forward and the 2.69% dividend yield "
                 "used as the carry offset in the probability map.")

# ---- negative results, recorded rather than hidden ----------------------------
f_q1 = R.add(Ring.COMPANY, "regular disclosures", FindingClass.B,
    "Reviewed consolidated interim financial statements for the three months ended 31 March "
    "2026, obtained. Net sales 2,532.834 (+10.1%), gross margin 42.4% against 45.7%, "
    "attributable profit 283.954 (-10.9%). Fixed assets rose 1,139.916 and projects under "
    "construction fell 917.600 in the quarter; the depreciation and amortisation charge more "
    "than doubled to 56.209. THE REVIEW CONCLUSION IS QUALIFIED on three matters: the "
    "associates' own periodic statements were not received; the active-ingredient company was "
    "recognised at cost following loss of control rather than remeasured and equity-accounted; "
    "and NO expected-credit-loss charge was recognised for the period",
    "Reviewed consolidated interim financial statements, three months ended 31 March 2026, "
    "English translation issued by the auditor, review report dated 14 May 2026", CO,
    "2026-05-14", is_fs_data=True, fiscal_period="Q1-2026",
    model_impact="Resets the FY2026 revenue, capital-expenditure and finance-cost paths to the "
                 "quarter's outturn; lowers the normalised associate contribution; replaces "
                 "the non-controlling interest deducted in the bridge with the "
                 "post-deconsolidation figure and adds the active-ingredient company at "
                 "carrying cost. CONFIRMS the study's central mechanism — the construction "
                 "balance is transferring and the depreciation step has arrived.")

f_q1fs = R.add(Ring.COMPANY, "official financial statements", FindingClass.B,
    "Separately issued audited consolidated financial statements for FY2023 and FY2024, "
    "English translations issued by the auditor. Every line ties to the Arabic annual reports "
    "already used, with one presentation difference: these show dividend-distribution tax on "
    "its own line where the annual reports fold it into general and administrative expense "
    "(FY2023) or into the associates line (FY2024)",
    "Audited consolidated financial statements FY2023 and FY2024, English translation issued "
    "by the auditor", CO, "2025-03-01", is_fs_data=True, fiscal_period="FY2024",
    model_impact="Adopts the filings' own presentation, which lifts FY2023 operating profit by "
                 "4.124 (0.34%) and states the dividend-distribution tax as its own line in "
                 "all three history years.")

f_bio = R.add_negative(Ring.INDUSTRY, "pricing",
    "Volume, price or utilisation guidance for the biologicals facility, sought across the "
    "company's annual reports, its investor presentation and every 2026 press release on its "
    "own site. The plant's products and investment are described; nothing quantifies its "
    "expected revenue", SWEEP_DATE)

f_ageing = R.add_negative(Ring.COMPANY, "official financial statements",
    "A counterparty-level or ageing-bucket breakdown of the expected-credit-loss allowance, "
    "sought in notes 10, 20, 31 and 36 of the audited FY2025 consolidated statements and in "
    "their FY2024 and FY2023 equivalents. The charge is disclosed in total and split by type "
    "(credit losses, inventory write-down, other provisions, and within that disputed taxes, "
    "claims and end-of-service), but never by counterparty, ageing band or geography, so no "
    "bottom-up build of it is possible from disclosure", SWEEP_DATE)

f_assocfs = R.add_negative(Ring.COMPANY, "official financial statements",
    "Separate financial statements, revenue or balance sheet for either equity-accounted "
    "associate, sought in the investments notes (8/2 and 8/3) of the FY2023, FY2024 and "
    "FY2025 filings and on the company's own website. Only the carrying value, the ownership "
    "percentage and the share of result are disclosed; no underlying accounts are published "
    "through this company, so the associate stream can only be normalised, not built up",
    SWEEP_DATE)

# ---- driver gate ---------------------------------------------------------------
R.add_driver("Domestic pack volume", DriverMode.BOTTOM_UP,
             "Packs sold of the company's own preparations are disclosed for FY2023, FY2024 "
             "and FY2025; export packs are disclosed in the investor presentation; the "
             "difference is the domestic book, and it is grown as a volume in its own right "
             "against a disclosed 65% capacity utilisation.",
             [f_demand, f_disc, f_ir])
R.add_driver("Domestic realised price per pack", DriverMode.BOTTOM_UP,
             "Domestic channel revenue divided by domestic packs, computed separately for "
             "FY2024 and FY2025 from the revenue note and the board's pack disclosure, then "
             "grown on the domestic inflation path because the price is set administratively.",
             [f_price, f_reg])
R.add_driver("Export volume and price", DriverMode.BOTTOM_UP,
             "Export packs and export US-dollar value are both disclosed, giving a realised "
             "US-dollar price per pack. Volume and price are grown separately in dollars and "
             "translated on the model's own exchange-rate path.",
             [f_gdem, f_price, f_macro])
R.add_driver("Cost of sales", DriverMode.BOTTOM_UP,
             "Built as a cash cost per pack from the audited cost-of-sales note's own line "
             "items, with one escalator per physically distinct driver class: imported "
             "ingredients and imported packaging on a hard-currency path through the exchange "
             "rate, labour on wage growth, energy on the regulated tariff schedule, domestic "
             "services on consumer inflation. Depreciation is excluded here and enters once "
             "from the property roll-forward.",
             [f_api, f_macro])
R.add_driver("Depreciation", DriverMode.BOTTOM_UP,
             "Projected from a property roll-forward that transfers the disclosed construction "
             "balance into depreciable assets on the company's own disclosed licensing "
             "timetable.",
             [f_tech, f_reg, f_fs])
R.add_driver("Working capital", DriverMode.BOTTOM_UP,
             "Inventory, receivable and payable days computed from the audited balance sheet "
             "and projected as ratios, with the inventory position explained by the company's "
             "stated eight-month stockpile policy.",
             [f_trade, f_fs])
R.add_driver("Credit-loss and provision charge", DriverMode.TOP_DOWN,
             "Carried as a percentage of revenue because the company discloses the charge in "
             "total and by type but not by counterparty or ageing bucket. This is the study's "
             "single most consequential contested judgement and it is computed BOTH WAYS and "
             "published side by side rather than resolved.",
             [f_fs, f_ageing])
R.add_driver("Associate contribution", DriverMode.TOP_DOWN,
             "Normalised from three disclosed years rather than built up, because the "
             "associates publish no separate accounts through this company's filings.",
             [f_stake, f_assocfs])
R.add_driver("Biologicals facility revenue", DriverMode.TOP_DOWN,
             "NOT FORECAST. The company has published nothing that would support a bottom-up "
             "build and this study does not invent one; the required contribution is instead "
             "solved for and published as the crux.",
             [f_bio, f_tech])
R.add_driver("FY2026 revenue, capital expenditure and finance cost", DriverMode.BOTTOM_UP,
             "Each reset to the reviewed first quarter of 2026 rather than left at the "
             "pre-quarter estimate: net sales grew 10.1% not the 17.5% first assumed, capital "
             "payments ran at an annual rate of about 1,299 not 832, and finance cost at about "
             "1,251 not 1,548.",
             [f_q1])

errors, warnings = R.validate()
print(f"Sweep register: {R.counts()}")
print(R.qc_line())
if warnings:
    print('\nWARNINGS:')
    for w in warnings:
        print('  -', w)
if errors:
    print('\nERRORS:')
    for e in errors:
        print('  -', e)
R.to_json(os.path.join(HERE, 'sweep_register.json'))
print('\nwrote sweep_register.json')
assert not errors, f'{len(errors)} sweep errors — build must not proceed'
