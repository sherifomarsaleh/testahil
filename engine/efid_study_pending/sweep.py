"""EFID — Edita Food Industries S.A.E. (EGX) — four-ring Step 2A Information Sweep.

Runs BEFORE any forecast driver is set. Every mandatory category of every ring is
closed by a dated finding or a dated negative search. Nothing in this module builds a
valuation, a driver model or a document; it records what was found, where, and what it
would touch.

WRITE LOCATION. This module and its JSON live in `engine/efid_study_pending/`, which is
deliberately OUTSIDE the `engine/*_study` glob every repository gate walks. There is no
`engine/efid_study/` and none should be created until a study is actually built.

CROSS-REFERENCES. Prose below cites other findings by SYMBOLIC token ("{f_vol}"), not by
a hand-typed "F25". A resolution pass at the bottom substitutes the real ids and asserts
that none is left dangling, so a reordered or inserted finding can never silently point
a reader at the wrong evidence.

PRIMARY SOURCE ACCESS, recorded rather than hidden.
  REACHED, and everything the company reports about itself comes from here:
    - https://ir.edita.com.eg/            (company IR site, HTTP 200)
    - https://edita.com.eg/               (corporate site, HTTP 200)
    - https://irfiles.technologyverse.com/efid/*.pdf  (the IR site's own file host —
      audited statements, interims, earnings releases, annual reports)
  BLOCKED, with the actual failure text:
    - https://www.egx.com.eg/... and https://egx.com.eg/  -> "curl: (52) Empty reply
      from server" (http=000). The EGX disclosure portal itself is unreachable from this
      environment.
    - https://www.cbe.org.eg/en/...       -> HTTP 200 carrying an F5 WAF interstitial:
      "<title>Request Rejected</title> The requested URL was rejected. Please consult
      with your administrator. Your support ID is 0ec309e4-...". A 200 that is not a page.
    - https://sis.gov.eg/...              -> "curl: (60) SSL certificate problem: unable
      to get local issuer certificate"
    - https://www.capmas.gov.eg/          -> HTTP 200 but a 1,421-byte JavaScript shell;
      no statistical content served without a browser.
  [R-SIGCM-03] NAMED FALLBACK USED: because egx.com.eg is unreachable, the EGX filing
  feed was read from the company's OWN mirror of it at
  https://ir.edita.com.eg/en/news-and-disclosures (Edita reproduces the EGX disclosure
  wire verbatim on its IR site, ISIN EGS305I1C011, Reuters code EFID.CA). That is the
  company's own document, not an aggregator, not a broker and not the press. No company
  figure in this register comes from any aggregator, broker or press source.

SCANNED FILINGS AND THE ARITHMETIC ARBITER.
  Every annual and interim statement set is image-only: pdftotext returns 0 characters
  for the first 12 pages of all eight annual PDFs and both 2026 interims. Every figure
  below was read off pixels rendered at 300-340 dpi with PyMuPDF, then RE-ADDED against
  the filing's own printed subtotals in Python. Two reads disagreed and arithmetic
  settled both:
    (a) FY2022 revenue. A 200/85-dpi render gave 7,678,100,869; a 320-dpi render gave
        7,671,100,869. Only 7,671,100,869 - 5,063,343,087 reproduces the printed gross
        profit of 2,607,757,782. An 8 had been read where a 1 is printed. The FY2023
        filing's own FY2022 comparative column independently prints 7,671,100,869.
    (b) FY2025 EAS note 20, total borrowings. A 62-dpi render gave 3,700,995,014; a
        340-dpi render gave 3,700,595,014. Only 3,700,595,014 + 771,424,343 reproduces
        the printed "Total Loans and overdraft" of 4,472,019,357. A 9 had been read
        where a 5 is printed — the same failure the protocol names.
    (c) FY2025 EAS financial-risk note, interest-rate sensitivity. A 62-dpi render gave
        42,727,096; renders at 400 and 700 dpi both give 42,727,098. A 6 had been read
        where an 8 is printed. Found on the re-read pass, and it corrected a figure this
        register had already published.
  Every other statement column re-added to the pound on the first read. The FX sensitivity
  note was re-read at 340-700 dpi on a second pass and re-added against its own exposure
  table; that pass found three defects in the FILINGS themselves, all listed in
  FOOTING_CHECKS below.

NO BETA IS RESOLVED HERE, by instruction. The exchange, the listing structure and the
price series that exists are recorded as a finding; the regressor ruling is not this
sweep's to take. Note that EFID carries a SECOND listing — GDRs on the London Stock
Exchange, one GDR = five ordinary shares — so the dual-listing trap is live and is
flagged rather than assumed away.
"""
import sys, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from research_sweep import (SweepRegister, AssetClass, Ring, FindingClass,
                            SourceType, DriverMode)

SWEEP_DATE = "2026-09-09"
R = SweepRegister("EFID", AssetClass.STOCK, SWEEP_DATE)
CO, IR, REG, PMD, PRESS, AGG = (SourceType.COMPANY_OFFICIAL, SourceType.COMPANY_IR,
                                SourceType.REGULATOR_OFFICIAL, SourceType.PRIMARY_MARKET_DATA,
                                SourceType.REPUTABLE_PRESS, SourceType.AGGREGATOR)

IRF = "https://irfiles.technologyverse.com/efid"

# ---------------------------------------------------------------- PRIMARY ACCESS
R.record_primary_access("https://ir.edita.com.eg/", True, "2026-09-09",
    "HTTP 200. Full IR library served: Results Center (192 statement/release PDFs back "
    "to FY2012), Publications, News & Disclosures (the EGX wire mirrored by the "
    "company), Listing Information, Share & Corporate Information, Dividends, IR "
    "Calendar, Analyst Coverage. Every Company-ring figure in this register came from "
    "here or from its file host.")
R.record_primary_access("https://edita.com.eg/", True, "2026-09-09",
    "HTTP 200 (www.edita.com.eg 301s to the apex). Corporate site; IR content lives on "
    "the ir. subdomain.")
R.record_primary_access(f"{IRF}/Edita-Food-Industries-FY-2025-IFRS.pdf", True, "2026-09-09",
    "HTTP 200, 9,682,104 bytes, application/pdf, 85 pages. The company's own IR file "
    "host. Same host served FY2024/FY2023/FY2022 IFRS and EAS sets, both 2026 interims, "
    "every earnings release and the 2024 Annual Report.")
R.record_primary_access("https://www.egx.com.eg/downloads/Bulletins/341550_1.pdf", False,
    "2026-09-09",
    "BLOCKED. Verbatim: 'curl: (52) Empty reply from server', http=000, size=0. This is "
    "the 30-Jun-2026 Article-30 Disclosure Form for the BoD and shareholders' structure. "
    "Retried over http:// (proxy upgrades to https) — same failure.")
R.record_primary_access("https://egx.com.eg/", False, "2026-09-09",
    "BLOCKED. Verbatim: 'curl: (52) Empty reply from server', http=000. The EGX portal "
    "root is unreachable, so no EGX-hosted PDF can be retrieved. [R-SIGCM-03] fallback "
    "taken: the EGX disclosure wire was read from Edita's own mirror of it at "
    "https://ir.edita.com.eg/en/news-and-disclosures.")
R.record_primary_access("https://www.cbe.org.eg/en/economic-research/statistics/cbe-rates",
    False, "2026-09-09",
    "BLOCKED BY WAF. HTTP 200 but the body is 269 bytes of F5 interstitial, verbatim: "
    "'<html><head><title>Request Rejected</title></head><body>The requested URL was "
    "rejected. Please consult with your administrator.<br/><br/>Your support ID is "
    "0ec309e4-7b64-4e2f-bf0b-6b1225bd6617'. Same response for /en, for the inflation-"
    "rates page and for the overnight-deposit-and-lending-rate page. No CBE primary "
    "series could be read.")
R.record_primary_access("https://sis.gov.eg/en/media-center/news/central-bank-of-egypt-maintains-key-interest-rates/",
    False, "2026-09-09",
    "BLOCKED. Verbatim: 'curl: (60) SSL certificate problem: unable to get local issuer "
    "certificate'. State Information Service, tried as a second official route to the "
    "CBE decision after cbe.org.eg was refused.")
R.record_primary_access("https://www.capmas.gov.eg/", False, "2026-09-09",
    "REACHED BUT EMPTY. HTTP 200, 1,421 bytes — a React shell with no statistical "
    "content rendered server-side. The July-2026 CPI release could not be read from "
    "CAPMAS itself; the figure below is carried at press provenance and labelled.")

# -------------------------------------------------------------- STUDY-YEAR SCOPE
# FY2026 is the study year. Two quarters are on the public record as of the sweep date:
# Q1-2026 (filed 18-May-2026) and Q2-2026 (filed 13-Aug-2026). Q3-2026 is not yet due.
R.declare_study_year("2026", ["Q1-2026", "Q2-2026"])

# ================================================================ RING 1 — GLOBAL
f_fx = R.add(Ring.GLOBAL, "rate cycle & USD/FX regime", FindingClass.S,
    "EGP trades near 51/USD in early Sep-2026, broadly stable since the Mar-2024 float; "
    "the weekly range 30-Aug to 02-Sep-2026 was USD 0.0200059-0.0195351 per EGP. The "
    "global rate cycle is easing while Egypt's own policy rate is still 19.00-20.00%",
    "Wise / XE published EGP:USD series (market data only — never used for a company "
    "figure)", AGG, "2026-09-02",
    model_impact="Sets the translation rate for the two foreign-currency earnings legs "
                 "(Edita Morocco, MAD; Edita Iraq/Ahramat El Nile, IQD) and the EGP cost "
                 "of the imported quarter of the direct-material bill. {f_fxsens} locates "
                 "the company's OWN per-currency plus/minus 10% sensitivity, so this ring "
                 "sets the shock and the company's note sizes it — the study must not "
                 "invent its own elasticity.")

f_inputs = R.add(Ring.GLOBAL, "commodity complex (input/output)", FindingClass.S,
    "Soft-commodity input complex through Aug-2026: Egyptian sugar ~USD 0.61/kg, DOWN "
    "15.0% y/y; palm oil USD 1.15/kg SE Asia and USD 1.39/kg NE Asia; Egyptian flour "
    "prices set inside a state-linked milling system that lifted mill flour from EGP "
    "11,800/t to EGP 16,000/t in Aug-2024 and remains policy-driven",
    "IMARC palm-oil pricing report; Selina Wamucii Egypt sugar price series; Trendtype / "
    "IFPRI on Egyptian flour policy", PRESS, "2026-08-31",
    model_impact="These are the exogenous half of the cost-per-unit build. The COMPANY "
                 "half is {f_costmix}: direct material fell to 55.0% of revenue in 1H2026 "
                 "from 56.2% in 1H2025, and is 76% locally sourced / 24% imported. Cost "
                 "per pack must be built from {f_costmix} escalated on THESE indices one "
                 "at a time — one escalator per input, never a single blended CPI [L-009].")

f_gdem = R.add(Ring.GLOBAL, "global sector demand", FindingClass.C,
    "Packaged sweet snacks is a domestically-consumed, locally-manufactured category: "
    "there is no world clearing price for a packaged cake, and Edita's exports run to "
    "named regional markets rather than into a global market. c.90% of 1H2026 revenue "
    "was Egypt, c.10% regional export",
    "Edita 2Q2026 Earnings Release, 'About Edita' section", IR, "2026-08-12",
    model_impact="")

f_trade = R.add(Ring.GLOBAL, "trade / sanctions / supply chains", FindingClass.S,
    "Red Sea diversions remain the default routing into 2026 and are expected by the "
    "industry to persist through at least 2027: Asia-Europe rates 25-40% above normal "
    "and a Red Sea premium of about USD 800-1,500 per container plus USD 300-500 of "
    "insurance and surcharges; regional port congestion adds transit delays",
    "Zencargo / Suaid Global / Hillebrand Gori Red Sea trackers; USDA FAS on Egyptian "
    "export disruption", PRESS, "2026-08-31",
    model_impact="Prices the 24% imported share of the direct-material bill ({f_costmix}) "
                 "and the landed cost of imported machinery under the EGP 320m four-line "
                 "purchase ({f_lines}). Carried as a cost-per-unit adder on the imported "
                 "leg only, never smeared across the whole COGS line.")

# =============================================================== RING 2 — COUNTRY
f_cbe = R.add(Ring.COUNTRY, "sovereign macro (inflation, policy rate, FX/deval risk)",
    FindingClass.S,
    "CBE held on 20-Aug-2026 for the fourth consecutive meeting: overnight deposit "
    "19.00%, overnight lending 20.00%, main operation 19.50%. Rates have been unchanged "
    "since a 100bp cut in Feb-2026. Annual urban headline inflation accelerated to 14.9% "
    "in Jul-2026 from 14.3% in Jun-2026 (core 14.7%), the first rise since March",
    "CBE MPC decision 20-Aug-2026 and CAPMAS Jul-2026 CPI release, both read via "
    "EnterpriseAM / Daily News Egypt / Bloomberg because cbe.org.eg returned a WAF "
    "'Request Rejected' page and capmas.gov.eg served an empty JS shell (see the "
    "primary-access log)", PRESS, "2026-08-20",
    model_impact="Two places. (1) The explicit-window risk-free rate and the direction "
                 "of the Kd path against which Edita's own floating-rate book is priced "
                 "— {f_debt} gives the company's audited 1% rate sensitivity (EGP 42.7m "
                 "of post-tax profit at 31-Dec-2025), so the shock is exogenous and the "
                 "impact is the company's own number. (2) The price-per-pack path: "
                 "Edita's FY2025 average price per pack rose 31.3% against ~14-15% CPI, "
                 "so the price driver is NOT an inflation pass-through and must not be "
                 "modelled as one.")

f_tax = R.add(Ring.COUNTRY, "regulatory environment (regulator, caps, tariffs, tax/subsidy)",
    FindingClass.S,
    "Egyptian corporate income tax 22.5%; VAT standard 14% with a reduced 5% rate on "
    "machinery and equipment used to establish production lines, and basic foodstuffs "
    "exempt or zero-rated. No snack, sugar or HFSS tax is in force",
    "PwC Worldwide Tax Summaries — Egypt, corporate income and other taxes",
    REG, "2026-01-01",
    model_impact="Sets the statutory tax rate. It does NOT set the effective rate: "
                 "Edita's audited FY2025 IFRS charge of EGP 1,008,535,910 on PBT of "
                 "3,450,812,023 is 29.2%, and on the EAS PBT of 3,703,837,580 is 27.2% "
                 "— both well above statutory. The tax driver is built from the filed "
                 "charge, with the statutory rate as a floor, and the gap named. The 5% "
                 "machinery VAT rate is a real cash item on the EGP 320m line purchase.")

f_pol = R.add(Ring.COUNTRY, "fiscal / political events with sector read-through", FindingClass.S,
    "Egyptian household purchasing power is the demand-side variable: subsidised bread "
    "was repriced for the first time since 1989 and mill flour prices were raised under "
    "the IMF-linked consolidation, which raises the price of the untreated staple "
    "alternative to a packaged snack while squeezing the same consumer's wallet",
    "IFPRI analysis of the Egyptian bread subsidy reform; Trendtype on the 2024 flour "
    "repricing", PRESS, "2026-08-31",
    model_impact="Sits behind the packs-sold path. Edita's own record shows the tension "
                 "resolved by MIX rather than by units: FY2025 total packs FELL 1.4% to "
                 "3,788mn while tons ROSE 19.3% to 154.7k and average price per pack rose "
                 "31.3% ({f_vol}). Any volume driver that assumes packs track population "
                 "or real income is contradicted by the company's own FY2025.")

# ============================================================== RING 3 — INDUSTRY
f_mkt = R.add(Ring.INDUSTRY, "demand drivers & capacity/supply balance", FindingClass.S,
    "Egyptian snacks retail value sales rose 17% in 2026 to EGP 118,947mn. Edita's "
    "FY2025 revenue of EGP 20,915mn is roughly a sixth of that pool on a not-like-for-"
    "like basis (retail value vs ex-factory net sales), so the figure bounds the market "
    "rather than measuring Edita's share",
    "Euromonitor International, Snacks in Egypt (country report)", AGG, "2026-06-30",
    model_impact="Bounds the top-down sanity check ONLY. The volume build is bottom-up "
                 "off {f_vol}'s per-segment packs and tons; this finding is the ceiling "
                 "test the bottom-up build must not breach, not an input to it.")

f_price = R.add(Ring.INDUSTRY, "pricing", FindingClass.D,
    "Edita discloses average price per pack every quarter, by segment and in total: FY2025 "
    "EGP 5.52 (+31.3% y/y), 1H2026 EGP 5.95 (+12.8%), 2Q2026 EGP 6.14 (+12.0%). Segment "
    "2Q2026: Cakes 5.22 (+10.0%), Bakery 8.33 (+6.1%), Rusks 9.78 (+21.9%), Wafers 5.44 "
    "(+24.6%), Candy 6.58 (+8.4%), Biscuits 7.25 (+45.4%), Frozen 88.56 (+5.3%)",
    "Edita 2Q2026 and FY2025 Earnings Releases, 'Segment Volumes and Prices' table",
    IR, "2026-08-12",
    model_impact="DRIVER UNLOCK. Converts revenue from a growth rate into price x volume "
                 "at SEGMENT level, in BOTH legs, with the price leg sourced quarter by "
                 "quarter. The mechanism the company names for the price rise is "
                 "'price-point migration' — moving SKUs up named price ladders (Molto "
                 "Gold at EGP 20, TODO BOMB at EGP 15, HoHos Coated and Freska Chocobar "
                 "at EGP 10) — which is a mix effect, so the price path must be built as "
                 "ladder migration and not as an inflation index.")

f_entrants = R.add(Ring.INDUSTRY, "new entrants (named-competitor level)", FindingClass.C,
    "Named share holders in the adjacent Egyptian snack pools: Chipsy (PepsiCo) 44% of "
    "savoury snacks against Egypt Food Co at 13%; Ocean Foods leads sweet biscuits and "
    "bars at 15% with Bisco Misr (Egyptian Co for Food) at 13%. Mondelez, Nestle Middle "
    "East and Americana are the named multinational participants. No new entrant into "
    "Edita's core packaged-cake and bakery pools was found",
    "Euromonitor International, Savoury Snacks in Egypt and Sweet Biscuits/Snack Bars in "
    "Egypt; Ken Research MENA premium packaged snacks", AGG, "2026-06-30",
    model_impact="")

f_neg_tech = R.add_negative(Ring.INDUSTRY, "technology substitution",
    "searched: 'Egypt packaged snacks technology substitution 2026', 'packaged cake "
    "croissant substitute alternative protein 3D printed shelf-stable bakery Egypt', "
    "'quick commerce disintermediation Egyptian snack distribution' — no substitution "
    "threat to packaged sweet baked snacks was found on any horizon a five-year forecast "
    "reaches. The live technology questions in Edita's own disclosures are all COST-side "
    "(ISO 50001 energy management awarded Jul-2026, a 390 kWp rooftop PV station begun "
    "May-2026 at the Sheikh Zayed HQ, and the Feb-2026 Shift EV fleet-electrification "
    "partnership), not demand-side substitution", SWEEP_DATE)

f_comp = R.add(Ring.INDUSTRY, "competitor capacity / price moves (named)", FindingClass.S,
    "The single named competitor capacity move in the window is Edita's own purchase: in "
    "Oct-2025 it signed an asset purchase agreement with an UNNAMED 'regional food "
    "company' for two cake and two bakery production lines for EGP 320m, moving that "
    "capacity out of a competitor's hands and into Edita's. The counterparty is not "
    "named in any company document swept",
    "Edita FY2025 Earnings Release, Operational Developments", IR, "2026-03-11",
    model_impact="Capacity driver, both directions. It adds ~15% to Edita's core-segment "
                 "capacity ({f_lines}) AND removes four lines of competing supply. The "
                 "study must model the capacity add and must NOT also assume the vendor "
                 "replaces the lines, because the counterparty is unidentified and the "
                 "replacement cannot be sourced.")

# =============================================================== RING 4 — COMPANY
# ---- official financial statements (audited, scanned, re-added) ----------------
f_fs25 = R.add(Ring.COMPANY, "official financial statements", FindingClass.D,
    "FY2025 audited IFRS consolidated: revenue EGP 20,915,072,432; cost of sales "
    "(13,829,224,507); gross profit 7,085,847,925 (33.88%); PBT 3,450,812,023; tax "
    "(1,008,535,910); net profit 2,442,276,113, of which owners 2,496,545,788 and NCI "
    "(54,269,675); EPS 2.16. Balance sheet: total assets 14,827,856,625, total "
    "liabilities 8,949,200,854, total equity 5,878,655,771",
    "EDITA Food Industries (S.A.E.) and its Subsidiaries, Consolidated Financial "
    "Statements prepared in accordance with IFRS for the year ended December 31, 2025 — "
    "Independent Auditor's Report, Saleh, Barsoum & Abdel Aziz (Grant Thornton Egypt), "
    "unmodified opinion; approved by the Board 10-Mar-2026",
    CO, "2026-03-10", url=f"{IRF}/Edita-Food-Industries-FY-2025-IFRS.pdf",
    is_fs_data=True, fiscal_period="FY2025",
    detail="Image-only scan, no text layer. Read at 300 dpi off rendered pixels. Every "
           "line re-added: gross profit, PBT, NPAT, the owners/NCI split, both asset "
           "subtotals, total assets, equity attributable, total equity, both liability "
           "subtotals, total liabilities and equity-plus-liabilities all FOOT exactly to "
           "the printed subtotals, in BOTH the 2025 and the restated 2024 columns.",
    model_impact="The FY2025 base every forecast rolls forward from. Revenue, COGS and "
                 "each opex line are carried as printed; nothing between them is derived.")

f_fs24r = R.add(Ring.COMPANY, "official financial statements", FindingClass.B,
    "FY2024 IS RESTATED. As originally filed (17-Apr-2025) FY2024 IFRS net profit was "
    "1,415,374,273 on an FX gain of 69,662,331. The FY2025 filing presents FY2024 as "
    "'Restated' with net profit 1,446,757,252 on an FX gain of 101,045,310. The entire "
    "EGP 31,382,979 restatement sits in the foreign-exchange line: PBT moves by exactly "
    "31,382,979 and the tax charge is unchanged at 556,329,772",
    "FY2025 IFRS consolidated statements (2024 Restated column) read against the FY2024 "
    "IFRS consolidated statements as filed", CO, "2026-03-10",
    url=f"{IRF}/EDITA-FOOD-INDUSTRIES-SAE-CONSO-DEC-2024.pdf",
    is_fs_data=True, fiscal_period="FY2024",
    detail="Both columns re-added independently and both foot. The delta was isolated by "
           "differencing line by line, not asserted. FY2024 revenue (16,146,545,699), "
           "cost of sales (11,240,232,913) and gross profit (4,906,312,786) are IDENTICAL "
           "in both versions — the restatement is below the operating line only.",
    model_impact="BASE CHANGER for the history table. The FY2024 comparative a later "
                 "build reads depends on which filing it opens, and the two differ by "
                 "2.2% of net profit. The study carries the RESTATED FY2024 (1,446.8m) "
                 "for continuity with FY2025, states that it does, and must not compute "
                 "an FY2025 growth rate off the as-filed 1,415.4m — that would overstate "
                 "growth by 2.2pp.")

f_fs23 = R.add(Ring.COMPANY, "official financial statements", FindingClass.D,
    "FY2023 audited IFRS consolidated: revenue EGP 12,125,997,046; cost of sales "
    "(8,200,709,717); gross profit 3,925,287,329 (32.37%); PBT 2,050,622,094; tax "
    "(544,046,655); net profit 1,506,575,439; EPS 2.17 (pre-bonus basis)",
    "EDITA Food Industries (S.A.E.) and its Subsidiaries, IFRS Consolidated Financial "
    "Statements for the year ended December 31, 2023 — Grant Thornton UAE (Dubai "
    "branch), Dr. Osama El Bakry, unmodified opinion signed 21-Apr-2024",
    CO, "2024-04-21", url=f"{IRF}/EDITA-FOOD-INDUSTRIES-SAE-CONSO-DEC-2023-FINAL.pdf",
    is_fs_data=True, fiscal_period="FY2023",
    detail="Scanned. Gross profit, PBT and NPAT all re-added and FOOT. Cross-checked "
           "against the FY2024 filing's FY2023 comparative column, which prints the same "
           "figures to the pound.",
    model_impact="Third historical year. FY2023 net profit (1,506.6m) is HIGHER than "
                 "FY2024's (1,446.8m restated) on 33% more revenue, so the history is "
                 "not monotonic and a growth-glide base picked off FY2024 alone would "
                 "start from a trough.")

f_fs22 = R.add(Ring.COMPANY, "official financial statements", FindingClass.D,
    "FY2022 audited IFRS consolidated: revenue EGP 7,671,100,869; cost of sales "
    "(5,063,343,087); gross profit 2,607,757,782 (33.99%); PBT 1,270,783,958; tax "
    "(311,351,887); net profit 959,432,071; EPS 1.36 (pre-bonus basis). FY2021 "
    "comparative: revenue 5,251,219,991, net profit 471,903,603",
    "EDITA Food Industries (S.A.E.) and its Subsidiaries, IFRS Consolidated Financial "
    "Statements for the year ended December 31, 2022 — Grant Thornton UAE (Dubai "
    "branch), unmodified opinion signed 30-Apr-2023",
    CO, "2023-04-30", url=f"{IRF}/EDITA-FOOD-INDUSTRIES-IFRS-2022.pdf",
    is_fs_data=True, fiscal_period="FY2022",
    detail="Scanned. THIS IS THE PAGE WHERE THE TWO READS DISAGREED. A low-dpi render "
           "gave revenue 7,678,100,869 and a JV-derecognition gain of 32,635,049; the "
           "320-dpi render gave 7,671,100,869 and 32,615,049. Arithmetic settled both: "
           "only 7,671,100,869 reproduces the printed gross profit and only 32,615,049 "
           "reproduces the printed PBT. The FY2023 filing's FY2022 comparative column "
           "confirms 7,671,100,869 independently. Both routes are recorded here rather "
           "than the winner alone.",
    model_impact="Fourth historical year, meeting the four-year target. Its FY2021 "
                 "comparative extends the disclosed revenue series to five points "
                 "(5,251 / 7,671 / 12,126 / 16,147 / 20,915 EGPmn) without leaving the "
                 "audited filings.")

f_fs25eas = R.add(Ring.COMPANY, "official financial statements", FindingClass.B,
    "TWO AUDITED FY2025 NET PROFITS EXIST AND BOTH ARE CORRECT. The EAS consolidated "
    "statements (the set filed to EGX, auditor's report signed Cairo 11-Mar-2026) print "
    "revenue 20,915,072,432 — identical — but cost of sales (13,723,015,211), gross "
    "profit 7,192,057,221 (34.39%), PBT 3,703,837,580 and NET PROFIT 2,695,301,670, "
    "EPS 2.18. Against IFRS the gaps are exactly 106,209,296 on COGS/gross profit and "
    "253,025,557 on PBT and on net profit, with the tax charge identical",
    "EDITA Food Industries (S.A.E.) and its Subsidiaries, EAS Consolidated Financial "
    "Statements for the year ended 31 December 2025 — Saleh, Barsoum & Abdel Aziz "
    "(Grant Thornton), Kamel Magdy Saleh FCA, unmodified opinion, Cairo 11-Mar-2026",
    CO, "2026-03-11", url=f"{IRF}/Edita-consolidated-English-Signed-FY25.pdf",
    is_fs_data=True, fiscal_period="FY2025",
    detail="Scanned; every column re-added and FOOTS. The difference is employees' profit "
           "share, expensed under IFRS and treated as a distribution under EAS. The "
           "company's own FY2025 release publishes the bridge and gives the profit-share "
           "adjustment as EGP 253.5m against a measured 253,025,557 — a 0.5m rounding in "
           "the release, not a discrepancy in the filings. The EGX wire reports the EAS "
           "number (2,695,301,670) as 'Net Profit' for FY2025.",
    model_impact="BASE CHANGER, AND A PRECONDITION: THIS IS RESOLVED BEFORE ANY DRIVER IS "
                 "SET, NOT CARRIED AS CONTEXT. The two bases differ by 10.4% of net profit "
                 "and 0.5pp of gross margin. The 2026 INTERIMS ARE FILED UNDER EAS "
                 "({f_q1}, {f_q2}) while the EARNINGS RELEASES ARE IFRS ({f_vol}, "
                 "{f_segp}, {f_costmix}). A study that anchors history on IFRS and rolls "
                 "it forward on interim EAS actuals, or that quotes a release margin "
                 "beside a statement margin, is WRONG BY CONSTRUCTION — and no gate in "
                 "this repository would catch it, because every individual figure is "
                 "company-official, audited and correct. Declare one basis in writing "
                 "before the first driver is set, carry it throughout, and reconcile the "
                 "other with the company's own published bridge.")

# ---- study-year quarters: BOTH filed, both re-added ----------------------------
f_q1 = R.add(Ring.COMPANY, "official financial statements", FindingClass.D,
    "Q1-2026 (three months to 31-Mar-2026), reviewed EAS condensed consolidated: revenue "
    "EGP 5,770,498,985; cost of sales (3,739,501,996); gross profit 2,030,996,989 "
    "(35.20%); finance income 265,616,554; PBT 1,142,904,331; tax (290,850,602); net "
    "profit 852,053,729, owners 873,819,839 and NCI (21,766,110); EPS 0.59. Total assets "
    "16,804,565,333 against 14,723,822,091 at 31-Dec-2025",
    "EDITA Food Industries (S.A.E.) and its Subsidiaries, Review Report and Condensed "
    "Consolidated Interim Financial Statements for the three months ended 31 March 2026 "
    "— Saleh, Barsoum & Abdel Aziz (Grant Thornton), Kamel M. Saleh FCA, Cairo "
    "17-May-2026, EAS No. 30",
    CO, "2026-05-18",
    url=f"{IRF}/Edita-Food-Industries-Consolidated-Condesned-Q1-2026-English-Signed-Version.pdf",
    is_fs_data=True, fiscal_period="Q1-2026",
    detail="Scanned. Re-added and FOOTS. Independently cross-checked by subtraction from "
           "the Q2-2026 filing: 6M revenue 12,250,402,687 minus 3M revenue 6,479,903,702 "
           "= 5,770,498,985 exactly, and the same identity holds for COGS, gross profit "
           "and net profit. Two separately-filed documents agree to the pound. NOTE the "
           "EAS/IFRS balance-sheet gap here too: this filing states 31-Dec-2025 total "
           "assets of 14,723,822,091 where the IFRS set states 14,827,856,625.",
    model_impact="First actual of the study year. Its 35.20% EAS gross margin is ABOVE "
                 "the FY2025 EAS full-year 34.39% — the ARCC failure pattern in reverse. "
                 "Any forecast margin path must start above the prior-year average, not "
                 "at it.")

f_q2 = R.add(Ring.COMPANY, "official financial statements", FindingClass.D,
    "Q2-2026 and 1H-2026, reviewed EAS condensed consolidated. Six months to 30-Jun-2026: "
    "revenue EGP 12,250,402,687; cost of sales (8,064,324,965); gross profit 4,186,077,722 "
    "(34.17%); finance income 489,674,337; finance cost (343,636,937); PBT 2,131,992,606; "
    "tax (518,083,162); net profit 1,613,909,444, owners 1,669,909,443 and NCI "
    "(55,999,999); EPS 1.12. Three months to 30-Jun-2026 standalone: revenue "
    "6,479,903,702; gross profit 2,155,080,733 (33.26%); net profit 761,855,715; EPS 0.53",
    "EDITA Food Industries (S.A.E.) and its Subsidiaries, Review Report and Condensed "
    "Consolidated Interim Financial Statements for the six months ended 30 June 2026 — "
    "Saleh, Barsoum & Abdel Aziz (Grant Thornton), Kamel M. Saleh FCA, Cairo Aug-2026; "
    "approved by the Board 12-Aug-2026, EAS No. 30",
    CO, "2026-08-13", url=f"{IRF}/Edita-Consolidated-English-Q2-2026.pdf",
    is_fs_data=True, fiscal_period="Q2-2026",
    detail="Scanned. All FOUR printed columns (6M-26, 6M-25, 3M-26, 3M-25) were re-added "
           "line by line and every one FOOTS to its printed gross profit, PBT, net profit "
           "and owners/NCI split. Prior-year comparatives inside this filing: 6M-2025 "
           "revenue 9,247,121,351 and net profit 1,017,686,279; 3M-2025 revenue "
           "4,963,742,378 and net profit 587,903,803. Subsidiary ownership at 30-Jun-2026 "
           "is disclosed entity by entity: Edita for Trade and Distribution 99.8%, Edita "
           "Confectionery Industries 99.98%, Edita Participation Cyprus 100%, Edita Food "
           "Industries-Morocco 78.67%, Edita For Food Investments 100%, Edita Frozen Food "
           "Industries 100%, Edita International LTD (UAE) 100%, Edita Investment Holding "
           "LTD (UAE) 100%, Edita TJA LTD (UAE) 51%, Ahramat El Nile For Trading and Food "
           "Industries (Iraq) 49%.",
    model_impact="Second actual of the study year, and the one that resets the base. "
                 "1H-2026 revenue is 58.6% of the whole of FY2025 and 1H-2026 net profit "
                 "is 59.9% of FY2025's EAS net profit. Q2 EAS margin (33.26%) is BELOW "
                 "Q1's (35.20%): the intra-year margin path is not flat and must be "
                 "modelled quarterly, not annually.")

# ---- regular disclosures --------------------------------------------------------
f_bs = R.add(Ring.COMPANY, "regular disclosures", FindingClass.D,
    "FY2025 audited IFRS balance sheet in full: PP&E 5,473,026,194; right-of-use "
    "469,758,484; intangibles and goodwill 457,686,035; deferred tax assets 90,941,886; "
    "inventories 2,315,050,051; trade and other receivables 1,280,278,007; treasury bills "
    "at amortised cost 3,445,357,884; cash and equivalents 716,765,194; FVTPL financial "
    "assets 578,992,890. Liabilities: non-current borrowings and government grants "
    "2,904,566,838; lease liabilities 511,267,558; bank overdraft 771,424,343; trade and "
    "other payables 2,728,430,277; current portion of borrowings 816,456,335",
    "FY2025 IFRS consolidated statement of financial position, printed page 6",
    CO, "2026-03-10", url=f"{IRF}/Edita-Food-Industries-FY-2025-IFRS.pdf",
    is_fs_data=True, fiscal_period="FY2025",
    detail="Both columns re-added; every subtotal FOOTS. Note the inventory direction: "
           "FY2024 3,034,025,532 fell to FY2025 2,315,050,051 while revenue rose 29.5%, "
           "which is why FY2025 operating cash flow (4,377,352,771) is 5.1x FY2024's "
           "(854,487,748) on 69% more net profit.",
    model_impact="Sets the opening balance sheet, the working-capital driver and the "
                 "EV-to-equity bridge. The T-bill and FVTPL holdings (4,024,350,774 "
                 "combined) are the reason {f_netdebt}'s net-debt definition matters.")

f_netdebt = R.add(Ring.COMPANY, "regular disclosures", FindingClass.B,
    "TWO COMPANY-OFFICIAL NET-DEBT FIGURES FOR THE SAME DATE, EGP 4.02bn APART. The "
    "audited EAS gearing note prints, at 31-Dec-2025: total borrowings 3,700,595,014 "
    "plus bank overdraft 771,424,343 = total loans and overdraft 4,472,019,357, less "
    "cash and bank balances 716,765,194 = NET DEBT 3,755,254,163, against total equity "
    "6,092,319,199, total capital 9,847,573,362, gearing 38% (2024: 41%). The FY2025 "
    "earnings release, same date, reports NET CASH of EGP 266.5m, because it counts "
    "'cash balance' as 4,741.1m — cash 716,765,194 plus treasury bills 3,445,357,884 "
    "plus FVTPL assets 578,992,890",
    "FY2025 EAS consolidated statements, capital-risk-management note (gearing ratio and "
    "loan covenants), read against the FY2025 Earnings Release balance-sheet commentary",
    CO, "2026-03-11", url=f"{IRF}/Edita-consolidated-English-Signed-FY25.pdf",
    is_fs_data=True, fiscal_period="FY2025",
    detail="GLYPH ERROR CAUGHT HERE. A 62-dpi render read total borrowings as "
           "3,700,995,014, which does not add to the printed total; the 340-dpi render "
           "gives 3,700,595,014, and 3,700,595,014 + 771,424,343 = 4,472,019,357 exactly "
           "as printed. A 9 had been read where a 5 is printed. Both routes recorded. "
           "The release's own arithmetic was verified too: 716,765,194 + 3,445,357,884 + "
           "578,992,890 = 4,741,115,968, and 4,741,115,968 - 4,474,600,000 = 266,515,968, "
           "reproducing the release's 266.5m to the pound. The release's 'total loans and "
           "borrowings' of 4,474.6m differs from the note's 4,472,019,357 by 2,580,643, "
           "which is the government-grant element.",
    model_impact="BASE CHANGER, AND A PRECONDITION: THIS IS RESOLVED BEFORE ANY DRIVER IS "
                 "SET, NOT CARRIED AS CONTEXT. On the note's definition Edita is 38% "
                 "geared; on the release's definition it is net cash. Both are "
                 "company-official, both reconcile exactly, and they differ by EGP 4.02bn "
                 "on the same date — enough to move the WACC weights, the equity bridge "
                 "and the terminal structure at once. No gate in this repository would "
                 "catch a study that used one for the weights and the other for the "
                 "bridge. The study states which definition it uses before the first "
                 "driver is set, uses the company's own release definition for the bridge "
                 "(the T-bills are the treasury asset generating the 575,446,672 of "
                 "FY2025 finance income), and must NOT let a 38% gearing ratio drive the "
                 "debt weight while a net-cash bridge adds the same T-bills back.")

f_cf = R.add(Ring.COMPANY, "regular disclosures", FindingClass.D,
    "FY2025 audited IFRS cash flow: net cash from operations 4,377,352,771 (FY2024 "
    "854,487,748); payment for purchase of PP&E (1,020,200,150) and of intangibles "
    "(61,564,140); proceeds from PP&E disposal 33,352,073; interest received 438,515,575; "
    "purchase of treasury bills (8,476,385,549); interest paid (564,286,847); income tax "
    "paid (575,275,777)",
    "FY2025 IFRS consolidated statement of cash flows, printed page 11",
    CO, "2026-03-10", url=f"{IRF}/Edita-Food-Industries-FY-2025-IFRS.pdf",
    is_fs_data=True, fiscal_period="FY2025",
    detail="Read at 300 dpi. NOTE A DEFINITION GAP the study must not paper over: the "
           "FY2025 release states 'Total CAPEX ... EGP 1,392.8 million' while the audited "
           "cash-flow capex lines sum to 1,081,764,290. The company's capex figure is on "
           "an accrual basis; the interims say so explicitly — Q1-2026 notes EGP "
           "60,632,474 and Q2-2026 notes EGP 59,241,027 of credit purchases of PP&E "
           "eliminated as non-cash. The two numbers are not interchangeable.",
    model_impact="Sets the capex driver and the D&A roll-forward. Whichever capex "
                 "definition is chosen must be the one the FCF bridge subtracts, and the "
                 "reconciling accrual must be named.")

f_fxsens = R.add(Ring.COMPANY, "regular disclosures", FindingClass.D,
    "PER-CURRENCY FX EXPOSURE AND SENSITIVITY, READ AT 340-700 DPI AND RE-ADDED. Net "
    "monetary position at 31-Dec-2025 (assets less liabilities): EUR +12,263,029 "
    "(171,339,160 less 159,076,131); USD -379,016,579 (1,773,924,906 less 2,152,941,485); "
    "MAD -453,138,562 (91,401,415 less 544,539,977); GBP +6,053,624 (6,079,005 less "
    "25,381); IQD -132,391,422 (2,159,318 less 134,550,740). Prior-year nets: EUR "
    "+73,409,680; USD -842,986,857; MAD -183,432,207; GBP +4,779,750; IQD nil. The stated "
    "effect of a 10% move, per currency, 2025 (2024): EUR 1,226,303 (7,340,968); USD "
    "37,901,658 (84,298,686); MAD 45,313,856 (18,343,221); GBP 605,362 (447,975); IQD "
    "13,239,142 (nil). Also disclosed: net FX loss in P&L (9,406,494) against a 2024 gain "
    "of 100,318,882, translation differences in OCI +66,673,936 against (104,127,255), no "
    "quoted equity investments, and a counterparty credit-rating table naming QNB, Credit "
    "Agricole Egypt, CIB, NBK, ADIB, Citibank Egypt, NBE, Banque du Caire, Standard "
    "Chartered, Bank of Iraq, BNP Paribas Morocco and Bank of Cyprus",
    "FY2025 EAS consolidated statements, financial-risk-management note — market risk "
    "(foreign-exchange and interest-rate), price risk, credit risk", CO, "2026-03-11",
    url=f"{IRF}/Edita-consolidated-English-Signed-FY25.pdf",
    is_fs_data=True, fiscal_period="FY2025",
    detail="RE-READ AND FOOTED, replacing the earlier 'located but unverified' entry. "
           "All five exposure rows foot: assets less liabilities equals the printed net, "
           "exactly, in both years. Each sensitivity was then tested against 10% of its "
           "OWN net exposure and EIGHT OF NINE reproduce to the pound. TWO DEFECTS IN THE "
           "FILING FALL OUT OF THAT TEST. (1) THE 'POST-TAX' LABEL IS WRONG. Every "
           "paragraph says 'post-tax profit for the year would have been ...', but every "
           "figure is exactly 10% of the net monetary exposure with NO tax gross-down: "
           "12,263,029 x 10% = 1,226,303; 379,016,579 x 10% = 37,901,658; 453,138,562 x "
           "10% = 45,313,856; and the same on all four 2024 cells that foot. At the FY2025 "
           "effective rate of 29.23% a genuine post-tax EUR figure would be 867,903, not "
           "1,226,303. The disclosed numbers are PRE-TAX. Taken at face value as post-tax "
           "they overstate the after-tax effect by 1/(1-t) = 1.413x. (2) THE GBP 2024 "
           "COMPARATIVE IS A TRANSPOSITION. The exposure table prints a 2024 GBP net of "
           "4,779,750, whose 10% is 477,975; the sentence prints 447,975. Both figures "
           "were re-rendered at 600 dpi and both are as described, so this is the "
           "FILING's typo, not the reader's — a 4 and a 7 swapped, EGP 30,000, immaterial "
           "to any model but proof that the prior-year comparatives in this note are "
           "hand-keyed. The same hand shows in the Moroccan Dirham paragraph, which dates "
           "its comparative '31 December 2023' while the figure it prints (18,343,221) is "
           "exactly 10% of the 31-December-2024 net exposure.",
    model_impact="DRIVER UNLOCK, now unconditional. The FX driver is built on the "
                 "company's own measured per-currency exposure instead of a house shock, "
                 "WITH the two corrections above applied: the sensitivities are used as "
                 "PRE-TAX and taxed by the model, and GBP 2024 is carried at 477,975. The "
                 "shape matters as much as the size — the USD and MAD books are net "
                 "LIABILITIES (-379.0m and -453.1m) while EUR and GBP are net assets, so "
                 "a weaker pound HURTS on the dollar and dirham legs and helps on the "
                 "euro and sterling legs. A single-signed FX assumption would be wrong "
                 "on two of the four legs. The note also gives the counterparty quality "
                 "behind the EGP 4.02bn treasury book that {f_netdebt} turns on.")

f_series = R.add(Ring.COMPANY, "regular disclosures", FindingClass.C,
    "PRICE SERIES AND LISTING, RECORDED, NO BETA RESOLVED. EFID.CA on the EGX, ISIN "
    "EGS305I1C011, sector Food/Beverages/Tobacco, listed 11-Dec-2014, first trading day "
    "02-Apr-2015 at an offer price of EGP 18.50. 1,400,027,312 listed shares at EGP 0.20 "
    "par. The repository holds engine/raw_ohlc/EG/EFID.csv, 2,555 daily EGP bars from "
    "02-Apr-2015 to 23-Aug-2026 (last close 33.20, range 3.30-34.92), and the EGX index "
    "at engine/raw_indices/EG/EGX30.csv running to 08-Sep-2026",
    "Edita IR, Share and Corporate Information + Listing Information; repository price "
    "and index files", CO, "2026-09-09",
    url="https://ir.edita.com.eg/en/share-corporate-information-overview",
    detail="THE REGRESSOR RULING IS NOT TAKEN HERE, by instruction. Two things a later "
           "build must settle before it does. (1) DUAL LISTING: Edita also has GDRs on "
           "the LONDON STOCK EXCHANGE, one GDR = five ordinary shares, priced at USD "
           "12.28 at IPO against EGP 18.50 per ordinary share; the FY2022-FY2024 IFRS "
           "audit reports state the IFRS accounts exist specifically for 'the Group "
           "meeting its continuing obligations under the Listing Rules of the London "
           "Stock Exchange'. Same issuer, two venues, two legitimate regressors — the "
           "series' currency and magnitude must be checked against the venue it is filed "
           "under. The held series is EGP and matches the EGX ordinary line, so market "
           "'EG' / exchange 'EGX' is the indicated pairing, but the ruling is the build's "
           "to take through own_stock_beta(). (2) BONUS ADJUSTMENT: issued capital went "
           "72,536,290 -> 140,002,731 -> 280,005,462 via two bonus issues, a 3.86x "
           "cumulative increase in share count, and the held series starts at 5.37 "
           "against an 18.50 offer price, so it is provider-adjusted. Its first row also "
           "carries a Change% of -81.80%, which is a first-row artefact, not a price "
           "move. Step 0.0 must run before any use.",
    model_impact="")

f_egxwire = R.add(Ring.COMPANY, "regular disclosures", FindingClass.C,
    "The EGX disclosure wire for EFID.CA, mirrored on the company's own IR site, is "
    "complete and current: FY2025 consolidated results filed 12-Mar-2026 (EAS net profit "
    "2,695,301,670 against 1,606,727,698); Q1-2026 filed 18-May-2026 (852,053,729 against "
    "429,782,476); 1H-2026 filed 13-Aug-2026 (consolidated 1,613,909,444 against "
    "1,017,686,279; standalone 1,515,542,650 against 938,788,090); EGM decisions "
    "16-Aug-2026 and certified minutes 01-Sep-2026 for the assembly of 13-Aug-2026",
    "Edita IR, News and Disclosures — the EGX wire reproduced verbatim by the company "
    "([R-SIGCM-03] named fallback: egx.com.eg itself returns 'curl: (52) Empty reply "
    "from server')", CO, "2026-09-01",
    url="https://ir.edita.com.eg/en/news-and-disclosures",
    detail="The FY2024 EAS comparative on the wire is 1,606,727,698, which is neither of "
           "the two IFRS FY2024 figures (1,415,374,273 as filed, 1,446,757,252 restated). "
           "Three FY2024 net profits are in circulation, all company-official, on two "
           "accounting bases and two vintages. Two 2026 items are flagged as NOT read "
           "because their attachments sit on the blocked EGX host: the 15-Jul-2026 FRA "
           "no-objection to an Article-48 disclosure report on the board meeting of "
           "12-Jul-2026, and the 13-Aug-2026 EGM decisions. Article 48 is the material-"
           "transaction gate, so the build should retry that document before it opens.",
    model_impact="")

# ---- IR communications (COMPANY_IR — mandatory) ---------------------------------
f_vol = R.add(Ring.COMPANY, "IR communications (calls, presentations, releases)",
    FindingClass.D,
    "FULL VOLUME AND PRICE DISCLOSURE, quarterly, per segment. 2Q2026: total packs "
    "1,055.8mn (+16.6%), total tons 44.5k (+23.9%), average price per pack EGP 6.14 "
    "(+12.0%). By segment in 2Q2026 — Cakes 655.5mn packs / 23.8k tons / EGP 5.22; "
    "Bakery 234.0 / 14.4 / 8.33; Wafers 99.4 / 2.5 / 5.44; Rusks 27.2 / 1.9 / 9.78; "
    "Candy 26.7 / 1.3 / 6.58; Biscuits 10.4 / 0.5 / 7.25; Frozen 0.3 / 0.1 / 88.56. "
    "FY2025: 3,788mn packs (-1.4%), 154.7k tons (+19.3%), EGP 5.52 per pack (+31.3%)",
    "Edita 2Q2026 Earnings Release, 'Segment Volumes and Prices'; Edita FY2025 Earnings "
    "Release, same table", IR, "2026-08-12",
    url=f"{IRF}/Edita-2Q2026-Earnings-Release-E2.pdf", fiscal_period="Q2-2026",
    model_impact="DRIVER UNLOCK, and the one that makes a genuine bottom-up build "
                 "possible. Volume x price at the finest disclosed level (segment, "
                 "quarterly, in packs AND tons AND price per pack) with growth projected "
                 "in both legs. No financial statement carries any of this. The pack/ton "
                 "divergence is the whole story and must be modelled: FY2025 packs fell "
                 "1.4% while tons rose 19.3%, i.e. pack SIZE grew ~21%, so a packs-only "
                 "volume driver would show a shrinking business.")

f_segp = R.add(Ring.COMPANY, "IR communications (calls, presentations, releases)",
    FindingClass.D,
    "SEGMENT REVENUE AND GROSS PROFIT, disclosed quarterly. 2Q2026 revenue: Cakes "
    "3,421.7 / Bakery 1,949.0 / Wafers 540.4 / Rusks 265.8 / Candy 175.4 / Biscuits 75.6 "
    "/ Frozen 22.8 / Other 29.4 EGPmn. 2Q2026 gross profit: Cakes 1,218.0 (35.6%) / "
    "Bakery 625.7 (32.1%) / Wafers 141.6 (26.2%) / Rusks 78.2 (29.4%) / Candy 54.6 "
    "(31.1%) / Biscuits 25.0 (33.1%) / Frozen (11.3) / Other 5.1. Wafers margin fell "
    "8.7pp y/y while Biscuits rose from 6.1% to 33.1%",
    "Edita 2Q2026 Earnings Release, 'Revenue and Gross Profitability by Segment'",
    IR, "2026-08-12", url=f"{IRF}/Edita-2Q2026-Earnings-Release-E2.pdf",
    fiscal_period="Q2-2026",
    model_impact="DRIVER UNLOCK for the COST side, which is what makes margin an output "
                 "rather than an input [L-005]. Segment revenue divided by segment tons "
                 "gives revenue per ton; segment gross profit subtracted gives COST PER "
                 "TON by segment. The build sets cost per ton and lets the margin fall "
                 "out. A blended or held gross margin on this name is a QC FAIL, because "
                 "the filings plainly support cost per unit.")

f_costmix = R.add(Ring.COMPANY, "IR communications (calls, presentations, releases)",
    FindingClass.D,
    "COST STRUCTURE IN PERCENTAGE-OF-SALES TERMS, and the EAS-to-IFRS bridge, both "
    "disclosed. 1H2026: direct material 55.0% of revenue (1H2025 56.2%), manufacturing "
    "overhead 9.8% (9.9%), industrial depreciation 1.3% (1.5%); total SG&A 17.3% of "
    "revenue (16.7%). The 1H2026 bridge names each line: selling and distribution 696.4 "
    "EAS / 720.2 IFRS, advertising and marketing 473.0 both, general and administrative "
    "865.5 EAS / 921.1 IFRS, other operations 170.5. Direct material is 76% locally "
    "sourced and 24% imported",
    "Edita 2Q2026 Earnings Release, cost commentary, 'Egyptian Accounting Standards "
    "Reconciliation to IFRS' table and the imported-vs-local direct-material chart",
    IR, "2026-08-12", url=f"{IRF}/Edita-2Q2026-Earnings-Release-E2.pdf",
    fiscal_period="Q2-2026",
    model_impact="DRIVER UNLOCK for opex. Splits SG&A into three separately-disclosed "
                 "legs so each gets its own driver instead of one percentage-of-sales "
                 "glide, and splits direct material 76/24 local/imported so the FX and "
                 "freight shocks ({f_fx}, {f_trade}) hit only the leg they actually "
                 "touch. The advertising and marketing leg is IDENTICAL under both bases, "
                 "so it is the one opex line that needs no basis decision.")

f_call = R.add(Ring.COMPANY, "IR communications (calls, presentations, releases)",
    FindingClass.C,
    "Edita runs a published quarterly earnings-call calendar: 2Q26 call 17-Aug-2026, "
    "1Q26 call 20-May-2026, 4Q25 call 18-Mar-2026, OGM 19-Apr-2026. Sell-side coverage "
    "is named on the IR site: EFG Hermes, CI Capital, Citi, HSBC, Beltone, Arqaam, "
    "Renaissance Capital, Exotix, Naeem, Pharos. IR contact Omar El Abhar, Senior IR and "
    "Investment Analysis Manager",
    "Edita IR Calendar and Analyst Coverage pages", IR, "2026-08-17",
    url="https://ir.edita.com.eg/en/ir-calendar",
    detail="NO CALL TRANSCRIPT OR SLIDE DECK IS PUBLISHED. The Publications section holds "
           "Annual Reports and Sustainability Reports only; there is no presentations "
           "archive. The calls happen and are dated, but their content is not on the "
           "public record, so nothing from a call enters this register.",
    model_impact="")

f_ar = R.add(Ring.COMPANY, "IR communications (calls, presentations, releases)",
    FindingClass.D,
    "PHYSICAL ASSET BASE, from the company's own annual report: 36 production lines "
    "across 7 facilities plus Morocco and Iraq, 7,000+ employees, 170+ SKUs across seven "
    "segments, 20+ export destinations. Line-by-line: E06 6th October (1997, croissants/"
    "cakes/rusks, 8 lines), E07 6th October Halls A&B (2012, croissants/cakes/wafers/"
    "rusks, 10 lines), E08 6th October (2017, wafers/biscuits, 4 lines with space for "
    "nine more), E09 (acquired 2023, frozen, 2 lines), E10 10th Ramadan (2003, cakes, 4 "
    "lines), E15 Beni Suef (2011, candy, 4 lines), Morocco (2021, cakes, 2 lines with "
    "room for a third, capacity 14,400 tons, MAD 140m paid-in), Iraq (acquired 2024, "
    "cakes and biscuits, 3 lines)",
    "EDITA Annual Report 2024, 'At a Glance' and 'Production Facilities'",
    IR, "2025-09-14", url=f"{IRF}/EDITA-Annual-Report-2024-Screen-Res-compressed-1-.pdf",
    detail="This is the vintage the asset-base ordering test [R-ASSET-01] must run "
           "against. NOTE THE STALENESS: the 2024 Annual Report is the LATEST — no FY2025 "
           "Annual Report has been published as of the sweep date, so the newest full "
           "asset-base description is 12 months older than the newest financials, and it "
           "PREDATES the four lines bought in Oct-2025 ({f_lines}). The line count a "
           "build uses must be 36 plus those four, not 36.",
    model_impact="Anchors capacity and the utilisation denominator per segment, and gives "
                 "the D&A base a physical counterpart. Tons per line per segment is the "
                 "capacity ceiling the volume driver may not breach.")

# ---- one-off base-resetting transactions ----------------------------------------
f_lines = R.add(Ring.COMPANY, "one-off base-resetting transactions", FindingClass.B,
    "In Oct-2025 Edita signed an asset purchase agreement with a regional food company "
    "for two cake and two bakery production lines, total consideration EGP 320 million, "
    "expected to expand total production capacity by around 15% across the core "
    "segments. Two of the four are already ramped: the Cakes line reached full "
    "utilisation in 1Q2026 and the Bakery line by April, at full utilisation through "
    "2Q2026",
    "Edita FY2025 Earnings Release (Operational Developments) and 2Q2026 Earnings Release "
    "(Industrial Operations)", IR, "2026-08-12",
    url=f"{IRF}/Edita-2Q2026-Earnings-Release-E2.pdf",
    model_impact="BASE CHANGER, modelled explicitly and dual-framed: two lines live in "
                 "1H2026 and two still to come, against a +15% total capacity step. This "
                 "is the mechanism behind Bakery's 42.4% y/y 2Q2026 revenue growth and "
                 "34.3% pack growth, and it is dated, so it must be an explicit step in "
                 "the volume driver — not smoothed into a growth glide. The dual frame is "
                 "with and without the two lines not yet ramped.")

f_htt = R.add(Ring.COMPANY, "one-off base-resetting transactions", FindingClass.B,
    "In Jan-2026 Edita finalised an agreement with Hostess Brands LLC (a wholly-owned "
    "subsidiary of The J. M. Smucker Company) acquiring the trademarks, brand names and "
    "brand reputation of Ho Hos, Twinkies and Tiger Tail across the REST OF AFRICA — more "
    "than 45 additional countries beyond the existing MENA territory. The FY2025 audited "
    "intangibles note prints the pre-existing HOHOS, Twinkies and Tiger Tail trademark "
    "at EGP 131,480,647, acquired under the 18-April-2015 contract for USD 68,618,558",
    "Edita release to the EGX 15-Jan-2026 (mirrored on the company IR site); FY2025 EAS "
    "consolidated statements, intangible-assets note", CO, "2026-01-15",
    url="https://ir.edita.com.eg/en/news-and-disclosures",
    model_impact="BASE CHANGER on two lines. It steps intangibles (IFRS intangibles and "
                 "goodwill rose from 343,070,835 to 457,686,035 across FY2025, and FY2025 "
                 "intangible purchases were 61,564,140 against 228,000 in FY2024), and it "
                 "opens a named, dated addressable market that did not exist in the "
                 "FY2025 base. Modelled as an explicit dated event with the export "
                 "revenue leg framed both with and without it — Edita's export sales are "
                 "already growing 52.3% y/y in 1H2026 and this is the stated reason to "
                 "expect that to continue.")

f_iraq = R.add(Ring.COMPANY, "one-off base-resetting transactions", FindingClass.B,
    "Iraq went from zero to a revenue line inside the study year. The cake line commenced "
    "operations at the end of March 2026 and generated EGP 72.5m of net sales in 2Q2026; "
    "a second line, dedicated to bakery, started in July 2026 — AFTER the 30-Jun-2026 "
    "balance-sheet date. The vehicle is Ahramat El Nile For Trading and Food Industries, "
    "49% held with 51% NCI, consolidated because control was established through a "
    "strategic partnership agreement with Tuma Jabr Abbas",
    "Edita 2Q2026 Earnings Release; FY2025 EAS consolidated statements, business-"
    "combinations and subsidiaries notes", IR, "2026-08-12",
    url=f"{IRF}/Edita-2Q2026-Earnings-Release-E2.pdf", fiscal_period="Q2-2026",
    model_impact="BASE CHANGER for the NCI line and for the export/regional revenue leg. "
                 "Two consequences a build gets wrong if it misses this: (1) the July-2026 "
                 "bakery line is a POST-BALANCE-SHEET event, so 2Q2026 run-rating Iraq "
                 "understates 2H2026; (2) at 49%/51% the NCI drag grows with Iraq, and "
                 "1H2026 NCI is already (55,999,999) against (8,745,156) a year earlier. "
                 "Modelled as a dated ramp, dual-framed one line versus two.")

f_morocco = R.add(Ring.COMPANY, "one-off base-resetting transactions", FindingClass.B,
    "Edita Morocco was CONSOLIDATED FOR THE FIRST TIME IN FY2022. Ownership rose to 77% "
    "and the minority's substantive veto rights were removed by revision of the "
    "shareholders' agreement, so the investment moved from equity-method joint venture to "
    "acquisition-method subsidiary, producing a gain on derecognition of the joint "
    "venture of EGP 32,615,049 and a loss on disposal of FVTPL assets of EGP 22,172,000 "
    "in FY2022. Holding is 78.67% at 30-Jun-2026. Morocco revenue: EGP 476m in FY2024, "
    "571.9m in FY2025 (+20.3%), 301.3m in 1H2026 (+7.2%)",
    "FY2022 IFRS consolidated statements, key audit matter 'Change in control of "
    "investment in Edita Food Industries Morocco'; Annual Report 2024; FY2025 and 2Q2026 "
    "Earnings Releases", CO, "2023-04-30", url=f"{IRF}/EDITA-FOOD-INDUSTRIES-IFRS-2022.pdf",
    model_impact="BASE CHANGER for the history, and the reason FY2022 is not comparable "
                 "with FY2021 on a like-for-like basis. Any FY2021-to-FY2022 growth rate "
                 "conflates organic growth with a consolidation step, and the FY2022 "
                 "profit contains EGP 10.4m net of non-recurring derecognition items. "
                 "Morocco's growth has also decelerated hard — +20.3% FY2025 to +7.2% in "
                 "1H2026 — so its forward path is set on the recent half, not the "
                 "full-year rate [L-013].")

f_fancy = R.add(Ring.COMPANY, "one-off base-resetting transactions", FindingClass.S,
    "Edita entered frozen bakery in May-2023 by acquiring Fancy Foods for EGP 380 "
    "million: two production lines, machinery, land and distribution assets, 10,609 sqm, "
    "8 SKUs, operated as the Forni brand at facility E09. The segment still loses money "
    "at the gross line: a gross LOSS of EGP 11.3m in 2Q2026 against 8.5m in 2Q2025, and "
    "18.4m in 1H2026 at a gross margin of negative 45.7%",
    "EDITA Annual Report 2024 (Frozen section); Edita 2Q2026 Earnings Release",
    IR, "2026-08-12", url=f"{IRF}/Edita-2Q2026-Earnings-Release-E2.pdf",
    model_impact="Frozen is the one segment where a positive-margin assumption would be "
                 "invented rather than sourced. Its cost per ton is built like every "
                 "other segment and the resulting NEGATIVE gross margin is carried, with "
                 "breakeven modelled only against a dated, disclosed mechanism (the 2Q2026 "
                 "B2B partnership and the SKU rationalisation) — never assumed.")

# ---- ownership / stake changes (named-transaction rule) --------------------------
f_own = R.add(Ring.COMPANY, "ownership / stake changes (named-transaction rule)",
    FindingClass.D,
    "AUDITED SHAREHOLDER REGISTER AT 31-DEC-2025, share by share: Quantum Investment BV "
    "682,523,990 shares / EGP 136,504,798 / 48.75%; Kingsway Fund Frontier Consumer "
    "Franchises 72,412,940 / 14,482,588 / 5.17%; RIMCO E G T Investment LLC 141,127,054 / "
    "28,225,411 / 10.08%; Others (public stocks) 503,963,328 / 100,792,665 / 36.00%; "
    "total 1,400,027,312 shares / EGP 280,005,462 / 100%. Quantum is wholly owned by the "
    "Berzi family",
    "FY2025 EAS consolidated statements, share-capital note; Edita IR Share and Corporate "
    "Information page", CO, "2026-03-11",
    url=f"{IRF}/Edita-consolidated-English-Signed-FY25.pdf",
    is_fs_data=True, fiscal_period="FY2025",
    detail="Re-added: the share column, the value column and the percentage column all "
           "FOOT exactly, and every holding reconciles to par at EGP 0.20. THREE COMPANY "
           "SOURCES DISAGREE ON THE SUMMARY and only this one is audited. The FY2025 "
           "earnings release pie shows Quantum 49 / Kingsway 5 / Others 46 (folding RIMCO "
           "into Others); the 2Q2026 release pie shows Quantum 49 / RIMCO 10 / Others 41 "
           "(folding Kingsway into Others); the static IR page shows Quantum 49 / "
           "Kingsway 6 / Free float 45 and is STALE. All three are simplifications of "
           "this table, not contradictions of it — but a build reading only the releases "
           "would conclude a 10% holder appeared during 1H2026, and none did.",
    model_impact="Fixes the free float at 36.00% (not the 41-46% the release pies imply) "
                 "and the share count at 1,400,027,312 for every per-share figure. A free "
                 "float read off a release pie would be overstated by 5-10pp.")

f_bonus = R.add(Ring.COMPANY, "ownership / stake changes (named-transaction rule)",
    FindingClass.B,
    "The EGM of 16-Apr-2025 approved an issued-capital increase from EGP 140,002,731 to "
    "EGP 280,005,462 — 700,013,656 new shares at EGP 0.20 par, financed from FY2024 "
    "retained earnings, ONE FREE SHARE FOR EACH ORIGINAL SHARE. Authorised in the "
    "commercial register 7-May-2025 and announced to the market 20-May-2025. Separately, "
    "the EGM of 26-Nov-2023 approved writing off 23,044,783 treasury shares",
    "FY2025 EAS consolidated statements, share-capital note; Edita EGX disclosures of "
    "16-Apr-2025 and 20-May-2025 (company IR mirror)", CO, "2026-03-11",
    url=f"{IRF}/Edita-consolidated-English-Signed-FY25.pdf",
    is_fs_data=True, fiscal_period="FY2025",
    model_impact="BASE CHANGER for every per-share number in the history table. EPS is "
                 "reported 2.16 for FY2025 and 1.05 for restated FY2024 on the post-bonus "
                 "count, while the FY2024 filing itself printed 2.06 and the FY2023 "
                 "filing 2.17 on the PRE-bonus count. Dividends per share are on the same "
                 "two bases. Any DPS or EPS series stitched across the 2025 bonus without "
                 "restating the earlier years is wrong by roughly 2x, and the held price "
                 "series appears provider-adjusted for the same event ({f_series}).")

f_neg_rimco = R.add_negative(Ring.COMPANY, "ownership / stake changes (named-transaction rule)",
    "searched, as a SPECIFIC NAMED TRANSACTION and never as an estimate: 'RIMCO E G T "
    "Investment LLC Edita stake acquisition', 'RIMCO Investments EFID 10% purchase', "
    "'Kingsway Fund Frontier Consumer Franchises Edita sale', across the company's own "
    "EGX disclosure mirror (every Article-29 and Article-30 filing listed from 2015 to "
    "01-Sep-2026), the Insider Transactions page and the audited share-capital notes. "
    "RIMCO's 10.08% is PRESENT in the 31-Dec-2025 audited register and ABSENT from the "
    "FY2025 release pie, but no dated purchase disclosure naming RIMCO as buyer or "
    "Kingsway as seller could be retrieved — the Article-30 Disclosure Forms that would "
    "carry it are hosted on egx.com.eg, which returns 'curl: (52) Empty reply from "
    "server'. The stake is recorded; the transaction behind it is NOT sourced",
    SWEEP_DATE)

# ---- management & capital actions ------------------------------------------------
f_debt = R.add(Ring.COMPANY, "management & capital actions", FindingClass.D,
    "NAMED DEBT FACILITIES AND THE COMPANY'S OWN RATE SENSITIVITY. Signed in the study "
    "year: a 7-year medium-term loan of EGP 600 million (announced 19-Apr-2026) and a "
    "7-year medium-term loan of EGP 500 million (announced 03-May-2026). Earlier: a USD "
    "45 million IFC loan (Oct-2023) and a loan agreement of May-2024. At 31-Dec-2025 "
    "variable-rate borrowings were EGP 3,552,268,699 (2024: 2,186,887,887) against an "
    "overdraft of 771,424,343 (2024: 808,368,965), and the audited sensitivity states "
    "that a 1% move in EGP rates changes profit by EGP 42,727,098 (2024: 29,952,569)",
    "Edita EGX releases 19-Apr-2026 and 03-May-2026 (company IR mirror); FY2025 EAS "
    "consolidated statements, financial-risk-management note", CO, "2026-05-03",
    url="https://ir.edita.com.eg/en/news-and-disclosures",
    is_fs_data=True, fiscal_period="FY2025",
    detail="THE SENSITIVITY FIGURE WAS CORRECTED ON RE-READ. A 62-dpi render gave "
           "42,727,096; renders at 400 and 700 dpi both give 42,727,098. A 6 had been "
           "read where an 8 is printed — the third glyph error caught on this name, after "
           "the FY2022 revenue 8-for-1 and the gearing-note 5-for-9. The variable-rate "
           "borrowing and overdraft figures were re-rendered at 700 dpi and stand. "
           "PARTIAL RECONCILIATION, recorded rather than forced: the 2024 comparative "
           "reproduces EXACTLY as 1% of variable-rate borrowings plus overdraft "
           "(2,186,887,887 + 808,368,965 = 2,995,256,852; 1% = 29,952,569), which "
           "validates the reading method and shows the intended base. The 2025 figure "
           "does NOT: 3,552,268,699 + 771,424,343 = 4,323,693,042 and 1% of that is "
           "43,236,930, leaving EGP 509,832 — 1.19% of the figure — unexplained by the "
           "two disclosed lines. Like every sensitivity in this note the label says "
           "'post-tax' and the arithmetic is PRE-TAX (a genuine post-tax 2024 figure "
           "would be 21,194,382, not 29,952,569). The study uses the printed 42,727,098, "
           "treats it as pre-tax, and states that its 2025 base is not fully "
           "reconcilable from the disclosed lines.",
    model_impact="DRIVER UNLOCK for interest. The debt is built facility by facility off "
                 "named tranches, not as a ratio on a liabilities base — the exact "
                 "mis-specification the PHDC walk-forward recorded as a defect [L-002, "
                 "Driver Ledger PHDC decision 2]. The 1% sensitivity converts the CBE "
                 "path ({f_cbe}) into a profit effect using the company's own elasticity.")

f_cov = R.add(Ring.COMPANY, "management & capital actions", FindingClass.S,
    "BINDING FINANCIAL COVENANTS, disclosed and currently met. Under the major borrowing "
    "facilities: bank debt-to-equity not more than 1:1; debt service ratio not below 1.2; "
    "leverage ratio not to exceed 1:2; current ratio not less than 1; liabilities to "
    "tangible net worth not to exceed 1:2; net financial debt to EBITDA not more than 1.8 "
    "(a second covenant states 2.5); peak debt service coverage not less than 1.4. The "
    "Group was in compliance at 31-Dec-2025 at 38% gearing",
    "FY2025 EAS consolidated statements, capital-risk-management note, 'Loan covenants'",
    CO, "2026-03-11", url=f"{IRF}/Edita-consolidated-English-Signed-FY25.pdf",
    is_fs_data=True, fiscal_period="FY2025",
    model_impact="Caps the debt-funded capex path and therefore the capacity path. A "
                 "forecast that funds the remaining two acquired lines and the Iraq ramp "
                 "with borrowing must be tested against net financial debt to EBITDA of "
                 "1.8, not left unconstrained. It also bounds the terminal capital "
                 "structure used in the WACC.")

f_div = R.add(Ring.COMPANY, "management & capital actions", FindingClass.D,
    "Dividend policy is a stated 35-50% payout. The most recent declaration: coupon 24, "
    "EGP 0.8639177376 per share, dividend date 11-May-2026, paid 14-May-2026, following "
    "the AGM of 19-Apr-2026. Prior cash-outs: two payments of EGP 0.57 in 2025 (30-Apr "
    "and 10-Sep), 0.43 and 0.57 in 2024, 0.57 and 0.43 in 2023",
    "Edita IR Dividends page; Edita EGX dividend declaration 27-Apr-2026 (company IR "
    "mirror)", CO, "2026-04-27", url="https://ir.edita.com.eg/en/dividends",
    model_impact="DRIVER UNLOCK for the payout and the cash bridge: EGP 0.8639177376 x "
                 "1,400,027,312 shares is EGP 1,209.5m, which against FY2025 EAS net "
                 "profit attributable of 2,749.6m is a 44.0% payout — inside the stated "
                 "35-50% band and therefore usable as a forward rule. The per-share "
                 "history straddles the 2025 bonus ({f_bonus}) and must be restated "
                 "before any DPS series is drawn.")

f_audit = R.add(Ring.COMPANY, "management & capital actions", FindingClass.S,
    "THE AUDITOR CHANGED. FY2022, FY2023 and FY2024 IFRS consolidated statements were "
    "audited by Grant Thornton UAE (Dubai branch), Dr. Osama El Bakry, reg. 935 — the "
    "FY2024 opinion is dated 17-Apr-2025. FY2025 IFRS was audited by Saleh, Barsoum & "
    "Abdel Aziz (Grant Thornton Egypt), and the FY2025 report states explicitly that the "
    "FY2024 IFRS statements 'were audited by another auditor who expressed an unmodified "
    "opinion on those statements on April 17, 2025'. All opinions across FY2022-FY2025 "
    "are unmodified",
    "FY2025 and FY2024 IFRS consolidated statements, Independent Auditor's Reports",
    CO, "2026-03-10", url=f"{IRF}/Edita-Food-Industries-FY-2025-IFRS.pdf",
    model_impact="Explains why the FY2024 comparative moved ({f_fs24r}) without any "
                 "accounting-policy change being announced, and is the reason the study "
                 "reconciles the FY2024 column across two filings rather than trusting "
                 "one. No forecast driver changes; the history table's provenance does.")

# ---- strategic plans & guidance ---------------------------------------------------
f_strat = R.add(Ring.COMPANY, "strategic plans & guidance", FindingClass.S,
    "DIRECTIONAL STRATEGY, ALL OF IT DATED AND NONE OF IT NUMERIC. Named, dated moves: "
    "the Oct-2025 four-line purchase (+15% core capacity); the Jan-2026 Hostess Africa "
    "rights; Iraq line 1 from Mar-2026 and line 2 from Jul-2026; the Feb-2026 Shift EV "
    "partnership to electrify the ETD distribution fleet; a 390 kWp rooftop PV station "
    "begun May-2026 at the Sheikh Zayed HQ; ISO 50001:2018 energy certification awarded "
    "Jul-2026 covering five of Edita Egypt's six factories; continuing price-point "
    "migration with named SKUs at named prices",
    "Edita FY2025 and 2Q2026 Earnings Releases (Operational Developments); Edita press "
    "release on the solar PV project", IR, "2026-08-12",
    url=f"{IRF}/Edita-Press-Release-Solar-PV-Project-E.pdf",
    model_impact="Each item is a dated, explicit event in the volume or cost driver "
                 "rather than a growth assumption. The energy items (PV, ISO 50001, EV "
                 "fleet) land in manufacturing overhead and distribution cost, which are "
                 "separately disclosed ({f_costmix}), so their effect is testable against "
                 "a disclosed line rather than asserted.")

f_neg_guid = R.add_negative(Ring.COMPANY, "strategic plans & guidance",
    "searched: the FY2025 and both 2026 earnings releases end to end, the 2024 Annual "
    "Report's Chairman and CEO statements, every board-resolution and release title on "
    "the company's EGX disclosure mirror from Jan-2025 to 01-Sep-2026, and the IR "
    "Calendar, for any numeric forward target — revenue guidance, volume guidance, margin "
    "guidance, a capex budget, a medium-term plan. NONE IS PUBLISHED. Edita gives dated "
    "operational facts and no forward numbers at all. Consistent with [L-012] this is the "
    "cleaner case: there is no management target to import and therefore none to score",
    SWEEP_DATE)

# ============================================================ DRIVER GATE TABLE
# Modes are earned, not assumed. Bottom-up rows cite the company-official disclosure or
# D-finding that unlocked them; top-down rows cite the negative search that forced them.
R.add_driver("Volume — packs and tons, by segment, quarterly", DriverMode.BOTTOM_UP,
    "Edita discloses packs sold, tons sold and average price per pack for every one of "
    "seven segments every quarter ({f_vol}). Built at segment level in BOTH packs and "
    "tons, because the two diverge violently — FY2025 packs -1.4% against tons +19.3% — "
    "and a packs-only build would show a shrinking business. Capacity ceiling per segment "
    "comes from the 36-line facility register ({f_ar}) plus the four lines bought in "
    "Oct-2025 ({f_lines}).",
    [f_vol, f_ar, f_lines, f_q2])

R.add_driver("Price per pack, by segment, as ladder migration", DriverMode.BOTTOM_UP,
    "Disclosed per segment per quarter ({f_price}, {f_vol}). Projected as price-point "
    "migration up named ladders (Molto Gold EGP 20, TODO BOMB EGP 15, HoHos Coated and "
    "Freska Chocobar EGP 10), which is the mechanism the company itself names, NOT as a "
    "CPI pass-through — FY2025 price per pack rose 31.3% against ~14-15% inflation "
    "({f_cbe}), so an inflation index would have missed more than half the move.",
    [f_price, f_vol, f_cbe])

R.add_driver("Cost per ton, by segment — margin is the OUTPUT", DriverMode.BOTTOM_UP,
    "Segment revenue and segment gross profit are both disclosed quarterly ({f_segp}), "
    "and segment tons with them ({f_vol}), so cost per ton is a subtraction, not an "
    "assumption. Gross margin is COMPUTED from the volume x price and cost-per-ton legs "
    "and is never set as an input [L-005]. Escalated one input at a time on {f_inputs}'s "
    "separate sugar, palm oil and flour indices with the 76/24 local/imported split from "
    "{f_costmix} — never one blended rate [L-009].",
    [f_segp, f_vol, f_costmix, f_inputs])

R.add_driver("SG&A — three separate legs", DriverMode.BOTTOM_UP,
    "The EAS-to-IFRS bridge breaks total SG&A into selling and distribution, advertising "
    "and marketing, and general and administrative, each printed separately every quarter "
    "({f_costmix}). Each gets its own driver. Advertising and marketing is identical under "
    "both accounting bases, so it needs no basis decision; the other two do.",
    [f_costmix, f_q2, f_fs25])

R.add_driver("Interest expense — facility by facility", DriverMode.BOTTOM_UP,
    "Built off the named tranches (EGP 600m 7-year, EGP 500m 7-year, IFC USD 45m) and the "
    "disclosed EGP 3,552,268,699 of variable-rate borrowing, with the CBE path ({f_cbe}) "
    "moving only the variable leg and the company's own 1% sensitivity (EGP 42,727,098, "
    "verified at 700 dpi) sizing the shock. That sensitivity is used PRE-TAX and taxed by "
    "the model, because the note's 'post-tax' label is arithmetically wrong ({f_debt}). "
    "Explicitly NOT a ratio on a liabilities base — that is the recorded PHDC defect "
    "[L-002].",
    [f_debt, f_cbe, f_bs])

R.add_driver("Finance income on the treasury book", DriverMode.BOTTOM_UP,
    "The asset is disclosed and dated: EGP 3,445,357,884 of treasury bills at amortised "
    "cost plus EGP 578,992,890 of FVTPL assets at 31-Dec-2025, generating FY2025 finance "
    "income of EGP 575,446,672 and 1H2026 finance income of EGP 489,674,337. Yield is "
    "solved from the disclosed pair and rolled on the CBE path.",
    [f_bs, f_fs25, f_q2, f_cbe])

R.add_driver("Capex and the D&A roll-forward", DriverMode.BOTTOM_UP,
    "Company-disclosed totals (FY2025 EGP 1,392.8m; 1H2026 EGP 726m) plus the named EGP "
    "320m four-line purchase and the 390 kWp PV station. THE DEFINITION MUST BE STATED: "
    "the release figure is accrual and the audited cash-flow lines sum to EGP 1,081.8m, a "
    "gap the interims attribute to credit purchases of PP&E (EGP 60,632,474 in Q1-2026, "
    "EGP 59,241,027 in Q2-2026). Whichever basis the FCF bridge subtracts, the reconciling "
    "accrual is named ({f_cf}).",
    [f_cf, f_lines, f_strat])

R.add_driver("Tax", DriverMode.BOTTOM_UP,
    "Built from the filed charge, not the statutory rate. FY2025 IFRS: EGP 1,008,535,910 "
    "on PBT 3,450,812,023 = 29.2% effective, against a 22.5% statutory rate ({f_tax}); on "
    "the EAS PBT the same charge is 27.2%. The gap is real and persistent and the study "
    "names it rather than defaulting to 22.5%.",
    [f_fs25, f_fs25eas, f_tax])

R.add_driver("Non-controlling interest", DriverMode.BOTTOM_UP,
    "Ownership is disclosed entity by entity in the interim notes ({f_q2}): Edita Morocco "
    "78.67% (21.33% NCI), Ahramat El Nile Iraq 49% (51% NCI), Edita TJA LTD 51%, Edita "
    "for Trade and Distribution 99.8%, Edita Confectionery 99.98%. The NCI drag scales "
    "with the Iraq ramp — 1H2026 NCI is (55,999,999) against (8,745,156) a year earlier — "
    "so it is projected off the Iraq volume path, not held flat.",
    [f_q2, f_iraq, f_morocco])

R.add_driver("Free float and share count", DriverMode.BOTTOM_UP,
    "1,400,027,312 shares at EGP 0.20 par, free float 36.00%, from the audited "
    "share-capital note that foots share-by-share ({f_own}) — NOT from the release pie "
    "charts, which fold different holders into 'Others' in different quarters and would "
    "put the float at 41-46%. Every per-share series is restated across the 2025 "
    "one-for-one bonus ({f_bonus}) before it is drawn.",
    [f_own, f_bonus])

R.add_driver("Dividend payout", DriverMode.BOTTOM_UP,
    "Stated policy 35-50%, and the latest declaration lands inside it: EGP 0.8639177376 x "
    "1,400,027,312 shares = EGP 1,209.5m against FY2025 EAS attributable profit of "
    "2,749.6m, i.e. 44.0%. The rule is the company's own band anchored on its own most "
    "recent actual ({f_div}).",
    [f_div, f_fs25eas, f_own])

R.add_driver("Frozen (Forni) segment path", DriverMode.BOTTOM_UP,
    "Built on the same cost-per-ton method as every other segment, which yields a NEGATIVE "
    "gross margin (1H2026 gross loss EGP 18.4m, margin -45.7%) and that negative is "
    "carried ({f_fancy}). Breakeven is modelled only against the dated mechanisms the "
    "company names — the 2Q2026 B2B partnership and the SKU rationalisation — and never "
    "assumed.",
    [f_fancy, f_segp, f_vol])

R.add_driver("FX, per currency, on the disclosed net monetary position", DriverMode.BOTTOM_UP,
    "UNCONDITIONAL. The company publishes its net monetary position and a 10% sensitivity "
    "for EUR, USD, MAD, GBP and IQD; the note has been read at 340-700 dpi and every "
    "exposure row and eight of nine sensitivity cells re-add exactly ({f_fxsens}). Built "
    "per currency on the disclosed net, with the market rate from the Global ring "
    "({f_fx}) and the shape the note actually shows: USD -379.0m and MAD -453.1m are net "
    "LIABILITIES while EUR +12.3m and GBP +6.1m are net assets, so a weaker pound cuts "
    "two legs and helps two. TWO CORRECTIONS ARE APPLIED, both evidenced in {f_fxsens}: "
    "the sensitivities are PRE-TAX despite the note's 'post-tax' wording and are taxed by "
    "the model, and GBP 2024 is carried at 477,975 rather than the printed 447,975.",
    [f_fxsens, f_fx, f_q2])

R.add_driver("PRECONDITION 1 — accounting basis for the whole model (EAS vs IFRS)",
    DriverMode.BOTTOM_UP,
    "NOT A FORECAST DRIVER: A GATE EVERY OTHER DRIVER PASSES THROUGH, AND IT IS SETTLED "
    "IN WRITING BEFORE THE FIRST DRIVER IS SET. FY2025 differs by EGP 253,025,557 of net "
    "profit and 0.5pp of gross margin between the two audited bases ({f_fs25eas}); the "
    "2026 interims are EAS ({f_q1}, {f_q2}) and the earnings releases are IFRS ({f_vol}, "
    "{f_costmix}). Anchoring history on IFRS and rolling forward on EAS interims is wrong "
    "by construction and every repository gate would pass it, because each figure is "
    "audited and correct on its own basis. One basis is declared, carried throughout, and "
    "the other reconciled using the company's own published bridge.",
    [f_fs25, f_fs25eas, f_q1, f_q2, f_costmix])

R.add_driver("PRECONDITION 2 — net-debt definition for the bridge and the WACC weights",
    DriverMode.BOTTOM_UP,
    "NOT A FORECAST DRIVER: A GATE, SETTLED BEFORE THE FIRST DRIVER IS SET. Two "
    "company-official net-debt figures exist for 31-Dec-2025 and both reconcile exactly "
    "({f_netdebt}): the audited gearing note's NET DEBT of 3,755,254,163 at 38% gearing, "
    "which counts only cash and bank balances, and the release's NET CASH of 266.5m, "
    "which counts the EGP 4,024,350,774 treasury-bill and FVTPL book as cash. The gap is "
    "EGP 4.02bn on one date. One definition is declared and used for BOTH the WACC "
    "weights and the equity bridge; using one for each is the failure this row exists to "
    "stop, and no gate would catch it.",
    [f_netdebt, f_bs, f_cf, f_cov])

R.add_driver("Ownership/stake overhang", DriverMode.TOP_DOWN,
    "The 31-Dec-2025 register is audited and exact ({f_own}), but the TRANSACTION that "
    "put RIMCO E G T Investment LLC at 10.08% and moved Kingsway is not sourced: the "
    "Article-30 Disclosure Forms that would carry it sit on egx.com.eg, which returns "
    "'curl: (52) Empty reply from server' ({f_neg_rimco}). Per the named-transaction rule "
    "the stake is carried at its audited level and any lock-up, overhang or follow-on "
    "assumption is refused rather than estimated.",
    [f_neg_rimco, f_own])

R.add_driver("Management guidance", DriverMode.TOP_DOWN,
    "There is none to consume. The negative search ({f_neg_guid}) covers both 2026 "
    "releases, the FY2025 release, the 2024 Annual Report and every EGX release title "
    "from Jan-2025 to 01-Sep-2026: Edita publishes no numeric forward target of any kind. "
    "Every forward number in the model is therefore the model's own, which is the [L-012] "
    "condition met by construction rather than by discipline.",
    [f_neg_guid, f_strat])

R.add_driver("Technology-substitution risk to the category", DriverMode.TOP_DOWN,
    "Closed by dated negative search ({f_neg_tech}). No substitution threat to packaged "
    "sweet baked snacks was found on any horizon a five-year forecast reaches; the live "
    "technology items in Edita's own disclosures are cost-side (solar PV, ISO 50001, EV "
    "fleet). Carried as zero in the demand driver, with the absence recorded rather than "
    "assumed.",
    [f_neg_tech, f_strat])

# ------------------------------------------------ RESOLVE SYMBOLIC CROSS-REFERENCES
# Prose above cites findings as "{f_name}". Substitute the real ids and assert that
# nothing is left dangling, so an inserted or reordered finding can never point a
# reader at the wrong evidence.
_FIDS = {k: v for k, v in list(globals().items())
         if k.startswith('f_') and isinstance(v, str) and re.fullmatch(r'F\d+', v)}


def _resolve(text: str) -> str:
    for _name, _fid in _FIDS.items():
        text = text.replace('{' + _name + '}', _fid)
    return text


for _f in R.findings:
    _f.headline = _resolve(_f.headline)
    _f.detail = _resolve(_f.detail)
    _f.model_impact = _resolve(_f.model_impact)
for _d in R.drivers:
    _d.justification = _resolve(_d.justification)

_dangling = set()
for _t in ([f.headline + f.detail + f.model_impact for f in R.findings] +
           [d.justification for d in R.drivers]):
    _dangling |= set(re.findall(r'\{f_[a-z0-9_]+\}', _t))
assert not _dangling, f"unresolved sweep cross-references: {sorted(_dangling)}"

# ------------------------------------------------------------------------ OUTPUT
FOOTING_CHECKS = """
Every figure below was re-added in Python against the filing's own printed subtotals.
  FY2025 IFRS  P&L  gross profit / PBT / NPAT / owners+NCI split ......... FOOTS (both cols)
  FY2025 IFRS  BS   4 subtotals + total assets + equity + liabilities + A=E+L  FOOTS (both cols)
  FY2024 IFRS  P&L  as filed, gross profit / PBT / NPAT ................... FOOTS
  FY2023       P&L  gross profit / PBT / NPAT ............................. FOOTS
  FY2022 IFRS  P&L  gross profit / PBT / NPAT, both cols .................. FOOTS after glyph arbitration
  FY2025 EAS   P&L  gross profit / PBT / NPAT / attribution ............... FOOTS
  FY2025 EAS   note gearing: loans+OD / net debt / total capital, both cols  FOOTS after glyph arbitration
  FY2025 EAS   note share register: shares / value / percent ............... FOOTS
  Q1-2026 EAS  P&L  gross profit / PBT / NPAT / attribution ............... FOOTS
  Q2-2026 EAS  P&L  all FOUR columns, gross profit / PBT / NPAT / split ... FOOTS
  Q1-2026 vs Q2-2026 cross-document identity (6M minus 3M) ................ EXACT, to the pound
  FY2025 EAS-to-IFRS bridge vs the company's published reconciliation ...... EXACT (253,025,557)
  FY2025 release net-cash arithmetic vs the audited balance sheet .......... EXACT (266,515,968)
  FY2025 EAS   note FX exposure: assets - liabilities = net, 5 currencies x 2 yrs  FOOTS
  FY2025 EAS   note FX sensitivity vs 10% of its own net exposure .......... 8 of 9 EXACT
                 the ninth (GBP 2024) DISAGREES by 30,000 — see below

THREE DEFECTS IN THE FILINGS, all found by re-adding rather than by reading:
  1. GBP 2024 sensitivity. Exposure table net 4,779,750 -> 10% = 477,975; the sentence
     prints 447,975. Both re-rendered at 600 dpi; both are as described. A 4/7
     transposition in the FILING, EGP 30,000, immaterial but proof the prior-year
     comparatives in that note are hand-keyed. The same hand dates the Moroccan Dirham
     comparative "31 December 2023" while its figure is exactly 10% of the 2024 net.
  2. "Post-tax profit" is the wrong label on every sensitivity in that note. All nine FX
     cells and both interest-rate cells are 10% (or 1%) of the exposure with NO tax
     gross-down. At the 29.23% FY2025 effective rate a true post-tax EUR figure would be
     867,903 against the printed 1,226,303. Used as post-tax they overstate by 1.413x.
  3. The FY2025 interest-rate sensitivity base does not fully reconcile. The 2024 cell is
     EXACTLY 1% of variable borrowings plus overdraft (2,186,887,887 + 808,368,965);
     the 2025 cell leaves EGP 509,832 unexplained against the same construction.

THREE GLYPH ERRORS CAUGHT BY THE SAME METHOD, each recorded with both routes:
  FY2022 revenue 7,678,100,869 -> 7,671,100,869 (8 read where 1 is printed)
  FY2025 EAS total borrowings 3,700,995,014 -> 3,700,595,014 (9 read where 5 is printed)
  FY2025 EAS rate sensitivity 42,727,096 -> 42,727,098 (6 read where 8 is printed)
"""

errors, warnings = R.validate()
R.to_json(os.path.join(HERE, 'sweep_register.json'))
print(R.qc_line())
print(f"\nfindings: {len(R.findings)} | drivers: {len(R.drivers)}")
print(FOOTING_CHECKS)
if errors:
    print(f"VALIDATOR ERRORS ({len(errors)}) — disclosed, not suppressed:")
    for e in errors:
        print(f"  ! {e}")
else:
    print("VALIDATOR ERRORS: none")
if warnings:
    print(f"\nVALIDATOR WARNINGS ({len(warnings)}):")
    for w in warnings:
        print(f"  - {w}")
else:
    print("VALIDATOR WARNINGS: none")
fr = R.check_freshness(SWEEP_DATE)
print(f"\nfreshness (delivery {SWEEP_DATE}): {fr or 'OK — sweep and intended delivery same day'}")
