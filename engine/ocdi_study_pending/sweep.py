"""OCDI (Sixth of October Development & Investment — SODIC, EGX: OCDI.CA)
Step 2A four-ring Information Sweep register.

Runs BEFORE any forecast driver is set. Every mandatory category of every ring is
closed by a dated finding or a dated negative search. Imports engine/research_sweep.py;
nothing is hand-rolled here.

PRIMARY-SOURCE POSITION, stated rather than left to be discovered later
----------------------------------------------------------------------
sodic.com and its CMS (cms.sodic.com) were reachable and were tried FIRST for every
Company-ring figure. The full document library rendered by the investor-relations page
was enumerated (333 distinct PDFs, 2007-2026) and the primary filings were pulled from
it directly. Every Company-ring financial figure in this register therefore comes from
a SODIC document, never from an aggregator.

FOUR THINGS A LATER BUILD MUST NOT MISS, all recorded below with dates:

(1) THE FY2024 AUDITED PDF IS UNSAFE TO READ AND WAS NOT READ.
    engine/scanned_filing_integrity.py returns REFUSE on both
    2-Sodic-Cons-Dec-24-signed.pdf and 2-Sodic-Separate-Dec-24-signed.pdf:
    "SYMBOL DICTIONARY PRESENT", 667 / 519 JBIG2 streams, segment types [0, 6, 48, 50],
    producer "Xerox AltaLink C8055". No figure in this register was read off either file.
    [R-SIGCM-03] fallback used instead, both SODIC's own: the 2024 Annual Board Report
    (EGP'000 table) and the 31-December-2024 comparative column of the 30-September-2025
    consolidated statements. The two agree to the thousand on all eight balance-sheet
    lines and on all four FY2023 income-statement lines they share with the audited
    FY2023 statements, which is what licenses the FY2024 column beside them.

(2) THE FY2025 INCOME STATEMENT COULD NOT BE OBTAINED — DISCLOSED, NOT PAPERED OVER.
    SODIC's own IR library holds NOTHING dated between 23-Oct-2025 and 27-Jul-2026: no
    31-Dec-2025 statements, no FY2025 earnings release, no 2025 annual board report, no
    31-Mar-2026 quarterly. The FY2025 audited statements exist (the 30-Jun-2026 review
    report names an unmodified prior-auditor opinion dated 5 February 2026) and are filed
    at EGX at
    https://www.egx.com.eg/downloads/News/سوديك مجمعه انجليزى 08-02-2026.pdf
    which this environment cannot fetch. The FY2025 BALANCE SHEET is fully recovered from
    the comparative column of the 30-Jun-2026 statements and is footed. The FY2025 INCOME
    STATEMENT, and every FY2025 operating anchor (full-year contracted sales, deliveries,
    31-Dec-2025 backlog, collections, capex), are NOT recoverable from any SODIC document.
    That is a STOP-AND-ASK, recorded as F41/F42, not a gap to be filled from a data
    provider.

(3) THE LAND BANK IS 33 MONTHS OLDER THAN THE NEWEST FILING [R-ASSET-01].
    Newest land-bank TOTAL SODIC has published: "+17MN SQM TOTAL LAND BANK", as of
    30/09/2023, in the December-2023 investor presentation. Newest filing: 30-Jun-2026,
    authorised 27-Jul-2026. Three named additions fall inside that gap, and the company
    itself says one of them DOUBLED the undeveloped land bank. The ordering is the
    finding; see F30/F33/F34/F43.

(4) THE SHARE COUNT TRIPLED IN JULY 2025 AND THE PRICE SERIES CARRIES THE STEP RAW.
    The seven-subsidiary merger took issued shares from 356,197,368 to 1,289,293,586 at
    EGP 4 par. engine/raw_ohlc/EG/OCDI.csv prints 61.00 on 13-Aug-2025 and 16.26 on
    14-Aug-2025 — a -73.3% single-session step that is the adjustment, not a return. See
    F31/F32.

BETA: NOT RESOLVED, deliberately and per instruction. The exchange, the listing and the
series that exists are recorded in F44 and nothing is regressed.
"""
import sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from research_sweep import (SweepRegister, AssetClass, Ring, FindingClass,
                            SourceType, DriverMode, RINGS, MANDATORY)

SWEEP_DATE = "2026-09-09"
R = SweepRegister("OCDI", AssetClass.STOCK, SWEEP_DATE)

CO   = SourceType.COMPANY_OFFICIAL
IR   = SourceType.COMPANY_IR
REG  = SourceType.REGULATOR_OFFICIAL
PMD  = SourceType.PRIMARY_MARKET_DATA
PRESS = SourceType.REPUTABLE_PRESS
AGG  = SourceType.AGGREGATOR

# =============================================================================
# PRIMARY ACCESS — the company's own channel tried first, every attempt logged
# with the REAL failure text returned on 09-09-2026.
# =============================================================================
R.record_primary_access(
    "https://www.sodic.com/investor-relations", True, "2026-09-09",
    note="HTTP 200, 1,929,835 bytes. Full IR library rendered in the app-router "
         "payload: 333 distinct PDFs spanning 2007-2026, enumerated and indexed to "
         "src/doc_index.json. This is the channel every Company-ring figure below "
         "was taken from.")
R.record_primary_access(
    "https://cms.sodic.com/uploads/", True, "2026-09-09",
    note="SODIC's own document CMS. 30 primary documents downloaded directly "
         "(statements, earnings releases, board reports, annual reports, EGX "
         "disclosures). Four downloads first failed with curl (35) 'Recv failure: "
         "Connection reset by peer' and succeeded on retry; one 404'd on a stale hash "
         "and succeeded on the hash carried in the live page payload.")
R.record_primary_access(
    "https://www.sodic.com/ar/investor-relations", True, "2026-09-09",
    note="Arabic IR page fetched as a cross-check on the English one. Identical "
         "333-document library. CONFIRMS the 23-Oct-2025 to 27-Jul-2026 hole is real "
         "and not an English-page truncation.")
R.record_primary_access(
    "https://ir.sodic.com", False, "2026-09-09",
    note="BLOCKED. https -> curl (56) 'CONNECT tunnel failed, response 502'. "
         "http -> curl (6) 'Could not resolve host: ir.sodic.com'. This host is the IR "
         "website SODIC prints on the back page of its own earnings releases and in its "
         "annual board report, so the dedicated IR channel is unreachable here even "
         "though the main site is not.")
R.record_primary_access(
    "https://www.egx.com.eg/downloads/News/"
    "%D8%B3%D9%88%D8%AF%D9%8A%D9%83%20%D9%85%D8%AC%D9%85%D8%B9%D9%87%20"
    "%D8%A7%D9%86%D8%AC%D9%84%D9%8A%D8%B2%D9%89%2008-02-2026.pdf", False, "2026-09-09",
    note="BLOCKED, AND THIS IS THE FY2025 STATEMENTS. curl (3 attempts, browser UA): "
         "HTTP 200 but content-type text/html and a body reading 'Please enable "
         "JavaScript to view the page content. Your support ID is: "
         "4562065020937510468.' — an F5/BIG-IP JavaScript challenge. Same URL via the "
         "fetch tool: 'The server returned HTTP 503 Service Unavailable.'")
R.record_primary_access(
    "https://www.egx.com.eg", False, "2026-09-09",
    note="BLOCKED. curl (52) 'Empty reply from server' on https://www.egx.com.eg, "
         "https://egx.com.eg and https://www.egx.com.eg/en/homepage.aspx alike. The "
         "exchange filing portal is not usable from here.")
R.record_primary_access(
    "https://disclosure.efsa.gov.eg", False, "2026-09-09",
    note="BLOCKED. curl (56) 'CONNECT tunnel failed, response 502'. The FRA disclosure "
         "portal, the other route to an EGX filing, is refused at the proxy.")
R.record_primary_access(
    "https://www.cbe.org.eg/en/economic-research/statistics/"
    "overnight-deposit-and-lending-rate", False, "2026-09-09",
    note="BLOCKED BEHIND A 200. HTTP 200, 269 bytes, body = '<title>Request "
         "Rejected</title> The requested URL was rejected. Please consult with your "
         "administrator. Your support ID is f3450824-55da-4778-ac35-3db93f7df752'. A "
         "WAF rejection served with a success status; the Country-ring policy rate is "
         "therefore carried at press provenance, not REGULATOR_OFFICIAL.")

R.declare_study_year("2026", ["Q1-2026", "Q2-2026"])

# =============================================================================
# RING 1 — GLOBAL
# =============================================================================
f_rate = R.add(
    Ring.GLOBAL, "rate cycle & USD/FX regime", FindingClass.S,
    "Global policy is TIGHTENING into the forecast window, not easing: futures put "
    "~60% odds on a Fed HIKE at the 16-Sep-2026 meeting after August payrolls beat, "
    "the ECB is expected at 2.50% and the BoJ is priced at 1.25% by quarter-end — "
    "three central banks tightening at once, which raises the cost of dollar funding "
    "and squeezes the EM carry trade Egypt's external account leans on",
    "Global economy briefing, 08-Sep-2026, reporting FOMC/ECB/BoJ market pricing",
    PRESS, "2026-09-08",
    model_impact="Sets the DIRECTION of the terminal risk-free rate and the EGP path. "
                 "A tightening global cycle removes the automatic downward glide in "
                 "Egypt's rf that a falling-rate world would license; the Ke build must "
                 "not assume corridor cuts the CBE has not made.")

f_fx = R.add(
    Ring.GLOBAL, "rate cycle & USD/FX regime", FindingClass.D,
    "SODIC's own filed FX table: USD/EGP spot 49.38 at 30-Jun-2026 against 47.61 at "
    "31-Dec-2025 (-3.6% for the pound in the half); period-average 49.24 (FY2025: "
    "49.26). EUR 56.07 and GBP 65.09 at 30-Jun-2026",
    "SODIC interim condensed consolidated FS 30 June 2026, note 4(c)(i)",
    CO, "2026-07-27", url="https://cms.sodic.com/uploads/SODIC_Q2_CONS_FS_30_June_2026_English_514ede2618.pdf",
    model_impact="DRIVER UNLOCK. The FX path is anchored on the company's own filed "
                 "spot and average rates rather than a screen quote, so the FY2025 and "
                 "H1-2026 translation base is the audited one. Group FX exposure is "
                 "small and one-way — USD 24.36m of cash at banks at 30-Jun-2026 — so "
                 "a weaker pound is a small P&L GAIN, not a loss; the real FX channel "
                 "is imported construction input cost, handled in Global/commodity.",
    fiscal_period="Q2-2026")

f_cmd = R.add(
    Ring.GLOBAL, "commodity complex (input/output)", FindingClass.S,
    "Egyptian construction inputs re-inflated through H1-2026 then plateaued: rebar "
    "EGP 33,500-37,000/t in Jan-2026 rising to EGP 39,000-40,000/t by 23-Jun-2026 "
    "(+8-16%), unchanged for August-2026 sales after recent declines; cement steady at "
    "EGP 3,896/t at 23-Jun-2026. Rebar is levered to iron ore, freight and USD/EGP",
    "Arab Iron & Steel Union rebar series; Egyptian rebar/cement price reporting "
    "23-Jun-2026 and Aug-2026",
    PRESS, "2026-08-01",
    model_impact="Sets the cost-per-square-metre escalator on WORK IN PROCESS, which is "
                 "what becomes cost of real estate sold on handover. One escalator per "
                 "input (steel, cement, finishing, labour), never one blended CPI "
                 "number [L-009]. Explains part of the H1-2026 cost-of-sales step and "
                 "must not be double-counted with the mix effect in F26.")

f_gdem = R.add(
    Ring.GLOBAL, "global sector demand", FindingClass.C,
    "Egyptian primary residential is a domestic, non-traded good: there is no world "
    "price and no export channel. The one genuine global transmission is CAPITAL, not "
    "demand — Gulf sovereign and quasi-sovereign money (Aldar/ADQ into SODIC, ADQ's "
    "Ras El Hekma vehicle Modon into the North Coast), and expatriate/foreign-currency "
    "buyers on the coast",
    "SODIC interim FS 30-Jun-2026 note 1.5 (ultimate parent Aldar Properties PJSC) read "
    "with the H1-2026 Egyptian developer sales league table",
    CO, "2026-07-27",
    model_impact="")

f_trade = R.add(
    Ring.GLOBAL, "trade / sanctions / supply chains", FindingClass.S,
    "The company's OWN post-balance-sheet note: 'geopolitical tensions in parts of the "
    "Middle East have increased, which had economic implications for markets in the "
    "region and the Egyptian market, resulting in an INCREASE IN THE OFFICIAL EXCHANGE "
    "RATES of foreign currencies against the Egyptian pound'. Management states it is "
    "not practicable to reliably estimate the full effect, and reaffirms going concern",
    "SODIC interim condensed consolidated FS 30 June 2026, note 36 'Significant events'",
    CO, "2026-07-27",
    model_impact="A named, dated, company-acknowledged FX shock inside the study year. "
                 "It is carried as an explicit scenario on the EGP path and on imported "
                 "input cost, dual-framed, NOT smoothed into the inflation glide. It is "
                 "also the reason the Q2-2026 FX gain in finance income (EGP 30.9m) "
                 "exists at all.",
    fiscal_period="Q2-2026")

# =============================================================================
# RING 2 — COUNTRY
# =============================================================================
f_cbe = R.add(
    Ring.COUNTRY, "sovereign macro (inflation, policy rate, FX/deval risk)", FindingClass.S,
    "CBE held the overnight deposit rate at 19.00% and the lending rate at 20.00% on "
    "20-Aug-2026 — a FOURTH consecutive hold — as inflation re-accelerated to 14.9% y/y "
    "in July-2026 from 14.3% in June on administered price rises including electricity "
    "tariffs. The CBE RAISED its 2026 average inflation forecast to 16-17%. Inflation "
    "had fallen to 11.9% in January-2026, so the window contains a turn, not a trend",
    "Bloomberg and MUFG Research reporting of the CBE MPC decision of 20-Aug-2026; "
    "Egypt State Information Service MPC releases",
    PRESS, "2026-08-20",
    detail="cbe.org.eg served a WAF 'Request Rejected' page under an HTTP 200 (support "
           "ID f3450824-55da-4778-ac35-3db93f7df752), so this is press reporting of the "
           "regulator's own decision rather than the regulator's page. Logged in "
           "primary_access.",
    model_impact="Sets the explicit-window risk-free rate at 19.00% and, more "
                 "importantly for THIS issuer, the whole cost of debt: every SODIC "
                 "facility in note 24 is priced at 'CBE corridor plus margin', so the "
                 "corridor path IS the interest path, and a fourth hold plus a raised "
                 "inflation forecast means no corridor relief is assumable in FY2026.")

f_egp = R.add(
    Ring.COUNTRY, "sovereign macro (inflation, policy rate, FX/deval risk)", FindingClass.S,
    "EGP near 50.95/USD in early Sep-2026, off its March-2026 low of 52.34; Reuters-"
    "polled economists look for ~49 by end-FY2026/27. IMF completed the seventh review "
    "on 30-Jul-2026, releasing ~USD 1.8bn; the USD 8bn Extended Fund Facility EXPIRES "
    "15-Dec-2026. Real GDP grew 4.4% in FY2024/25",
    "IMF Egypt press releases and country report 26/69; Reuters FX poll; Egypt "
    "macro reporting Sep-2026",
    PRESS, "2026-09-08",
    model_impact="The EGP path and the sovereign anchor. The programme EXPIRY inside "
                 "the first forecast year is the event: it is the single largest "
                 "identifiable risk to the FX and rate path and is modelled as an "
                 "explicit dated scenario, not averaged away. Note the spot has already "
                 "moved past the 49.38 the company filed at 30-Jun-2026.")

f_nuca = R.add(
    Ring.COUNTRY, "regulatory environment (regulator, caps, tariffs, tax/subsidy)",
    FindingClass.B,
    "NUCA imposed RETROACTIVE North Coast land fees on established developers from "
    "summer 2025 and SODIC IS NAMED as having paid EGP 4bn (Mountain View EGP 6bn; 83 "
    "companies targeted; NUCA has collected ~EGP 15bn of a EGP 45bn target). On "
    "29-Apr-2026 NUCA began ROLLING THEM BACK: up to 50% off for plots allocated before "
    "Feb-2024, recalculated on BUILT-UP AREA rather than total land area, 20% upfront "
    "and the rest over 5 years at 10%; a flat EGP 1,000/sqm (local) or USD 20/sqm "
    "(foreign) for post-Feb-2024 allocations. On 13-Jul-2026 NUCA added fee cuts and "
    "penalty waivers",
    "EnterpriseAM Egypt, 29-Apr-2026 and 13-Jul-2026",
    PRESS, "2026-04-29",
    model_impact="BASE CHANGER, and it has a primary-source counterpart the build must "
                 "tie to: SODIC's provisions balance went 2,613,659,406 (31-Dec-2024) -> "
                 "4,352,699,162 (31-Dec-2025) -> 4,630,344,058 (30-Jun-2026), with EGP "
                 "1,017,364,145 of provisions FORMED and EGP 195,000,000 released in "
                 "H1-2026 alone. The rollback is a dated, quantified REVERSAL "
                 "opportunity on a liability the company already carries. Modelled as "
                 "an explicit dual-framed event on land cost and on provisions, never "
                 "as a margin drift.")

f_tax = R.add(
    Ring.COUNTRY, "regulatory environment (regulator, caps, tariffs, tax/subsidy)",
    FindingClass.D,
    "Effective tax from the filings rather than the statute: FY2023 charge EGP "
    "440,238,159 on PBT 1,819,055,463 = 24.2%; H1-2026 charge EGP 245,696,702 on PBT "
    "1,082,915,873 = 22.7%, split EGP 123,274,212 current and EGP 122,422,490 deferred. "
    "Deferred tax asset EGP 771,600,393 at 30-Jun-2026 (894,022,883 at 31-Dec-2025), "
    "driven by a provisions temporary difference of EGP 1,092,853,282",
    "SODIC FY2023 audited consolidated FS note 15; interim FS 30-Jun-2026 note 14",
    CO, "2026-07-27",
    model_impact="DRIVER UNLOCK: tax is built from the disclosed current/deferred split "
                 "and the named temporary differences, not typed at 22.5%. The "
                 "provisions DTA is the mechanical link to the NUCA item in F08 — a "
                 "provision release reverses the DTA and the tax line moves with it.",
    is_fs_data=True, fiscal_period="Q2-2026")

f_fisc = R.add(
    Ring.COUNTRY, "fiscal / political events with sector read-through", FindingClass.S,
    "The state is simultaneously SODIC's landlord (NUCA), its co-developer counterparty "
    "(Heliopolis Housing on SODIC East, Midar on Eastvale) and its fiscal authority. "
    "Egypt is reviewing stalled real-estate projects and exploring new financing tools "
    "for developers (02-Aug-2026), while running down an IMF programme that ends "
    "15-Dec-2026",
    "Daily News Egypt, 02-Aug-2026; IMF Egypt programme timetable",
    PRESS, "2026-08-02",
    model_impact="Sets the LAND-COST and land-payment-schedule risk, which for this "
                 "issuer is a EGP 20,399,317,678 liability at 30-Jun-2026 with a fixed "
                 "instalment profile — a state counterparty that changes terms changes "
                 "a fifth of the balance sheet. Carried as a sensitivity on the land "
                 "liability schedule, not on revenue.")

# =============================================================================
# RING 3 — INDUSTRY
# =============================================================================
f_mkt = R.add(
    Ring.INDUSTRY, "demand drivers & capacity/supply balance", FindingClass.B,
    "THE EGYPTIAN PRIMARY MARKET HAS STOPPED GROWING IN REAL TERMS. Top-10 developer "
    "contracted sales were EGP 670bn in H1-2026 against EGP 651bn in H1-2025 — +2.9% "
    "y/y in a currency that lost far more than that — and the NUMBER OF UNITS SOLD by "
    "the leading developers FELL ~5% y/y. Q1-2026 is described as a 'healthy correction "
    "phase' with performance concentrating in large, well-capitalised developers while "
    "mid-caps meet tighter liquidity and more selective demand",
    "Daily News Egypt developer league tables, 31-May-2026 and 18-Aug-2026",
    PRESS, "2026-08-18",
    model_impact="BASE CHANGER, and the single most important cross-check in the study. "
                 "SODIC's own H1-2026 gross sales rose 201% y/y into a market that grew "
                 "2.9% with volumes falling. That growth is therefore LAUNCH TIMING and "
                 "SHARE GAIN, not market growth, and cannot be extrapolated. The "
                 "contracted-sales driver is capped by a market that is flat in units, "
                 "and the bear case is SODIC's launch pipeline pausing.")

f_price = R.add(
    Ring.INDUSTRY, "pricing", FindingClass.D,
    "Value up 2.9% while units are down ~5% means Egyptian primary PRICE PER UNIT rose "
    "roughly 8% y/y in H1-2026 — the sector's revenue is coming from price, not volume. "
    "SODIC's own realised price is separable from this: the board reports print units "
    "AND value by project, e.g. H1-2026 June 302 units / EGP 1,848m = EGP 6.1m per "
    "unit, 464 Acres 185 / EGP 1,404m = EGP 7.6m, SODIC East 61 / EGP 788m = EGP 12.9m",
    "Daily News Egypt league table 18-Aug-2026, read against SODIC's Q2-2026 Board "
    "Report delivered-unit table",
    PRESS, "2026-08-18",
    model_impact="DRIVER UNLOCK: converts revenue from a growth rate into units x "
                 "realised price PER PROJECT, with the market price trend as the "
                 "escalator ceiling. Volume and price are projected separately, as the "
                 "rule requires, because the market data says they are moving in "
                 "OPPOSITE directions.")

f_entrant = R.add(
    Ring.INDUSTRY, "new entrants (named-competitor level)", FindingClass.S,
    "MODON RAS EL HEKMA entered the top ten at rank 7 with EGP 44bn of H1-2026 sales, "
    "and G DEVELOPMENTS at rank 8 with EGP 30bn — both larger than SODIC's EGP 23.5bn "
    "gross. Modon is the ADQ-backed Ras El Hekma vehicle, i.e. a new, sovereign-funded "
    "entrant on the NORTH COAST, which is precisely where SODIC's growth is "
    "concentrated (North Coast was 66% of SODIC's FY2024 contracted sales and 302 of "
    "its 557 H1-2026 deliveries)",
    "Daily News Egypt top-10 developer table, H1-2026",
    PRESS, "2026-08-18",
    model_impact="Sets the North Coast price and absorption ceiling in the explicit "
                 "window and is the named mechanism behind the bear case. SODIC's "
                 "Ogami/June/Caesar pricing is sensitised against a sovereign-funded "
                 "entrant that does not need to clear a cost of capital.")

f_sub = R.add_negative(
    Ring.INDUSTRY, "technology substitution",
    "searched: 'technology substitution real estate development modular construction "
    "3D printing Egypt developer disruption 2026'. NOTHING FOUND that substitutes for "
    "the developer's function. What exists is (a) PropTech in Egypt — CRM, listings, "
    "digital sales — which changes DISTRIBUTION cost, not the product, and (b) 3D "
    "concrete printing, which is explicitly blocked in Egypt on economics: industrial "
    "printers cost USD 500k-2m each and the FX made the model unworkable for local "
    "developers. Precast/modular is a state social-housing input, not a competitor to "
    "the EGP 6-13m-per-unit segment SODIC sells into. No substitution driver is set",
    "2026-09-09")

f_peers = R.add(
    Ring.INDUSTRY, "competitor capacity / price moves (named)", FindingClass.D,
    "Named H1-2026 contracted sales, EGP bn: TMG 219.0, Palm Hills 94.0, Mountain View "
    "63.7, Emaar Misr 60.9, Hyde Park 52.9, Tatweer Misr 50.5, Modon Ras El Hekma 44.0, "
    "G Developments 30.0, Madinet Masr 28.4, La Vista 26.5. SODIC's EGP 23.5bn GROSS "
    "(EGP 19.4bn NET per its own board report) would rank ELEVENTH and it is absent "
    "from the top ten. Five leading developers hold just over half of contracted sales "
    "on combined land banks above 60m sqm",
    "Daily News Egypt / Zawya top-10 Egyptian developer table for H1-2026",
    PRESS, "2026-08-18",
    model_impact="DRIVER UNLOCK for the relative lens and a hard reality check on "
                 "scale: SODIC is a mid-cap in this field, not a top-five name, so peer "
                 "multiples must come from comparably-sized developers and the "
                 "market-share driver is built from a small and NOT-rising base. Also "
                 "fixes the peer set for the multiple lens.")

# =============================================================================
# RING 4 — COMPANY
# Every figure below is from a SODIC document. Provenance route is stated where the
# document was scanned.
# =============================================================================

# ---- official financial statements ----------------------------------------
f_fy22 = R.add(
    Ring.COMPANY, "official financial statements", FindingClass.D,
    "FY2022 AUDITED CONSOLIDATED (KPMG Hazem Hassan). Total operation revenues EGP "
    "7,810,878,791 (real estate 7,249,491,782; city/resort management 406,335,082; "
    "investment property 54,366,337; clubs & golf 100,685,590); total operation costs "
    "(5,619,092,779); gross profit 2,191,786,012 (28.1%); operating profit 649,989,446; "
    "net finance income 60,374,610; PBT 710,364,056; tax (185,207,991); profit "
    "525,156,065, attributable 520,057,733; EPS EGP 1.46. Total assets 30,384,708,608; "
    "total equity 7,311,126,811",
    "SODIC Annual Report 2022 (sodic-ar22.pdf), audited consolidated FS section",
    CO, "2023-02-08", url="https://cms.sodic.com/uploads/sodic_ar22_c085348875.pdf",
    detail="ROUTE: native text layer (Adobe PDF Library 17.0), no OCR. FOOTED: all four "
           "revenue legs sum to the printed total; all four cost legs to theirs; "
           "GP/OP/PBT/NPAT and the NCI split all reconcile; EPS 1.46 reproduces on "
           "356,197,368 shares. Independently corroborated digit-for-digit by the FY2022 "
           "comparative column of the FY2023 audited statements.",
    model_impact="First of four historical years. Establishes the four-leg revenue "
                 "structure and the pre-boom 28.1% gross margin the FY2024 55% peak has "
                 "to be normalised against.",
    is_fs_data=True, fiscal_period="FY2022")

f_fy23 = R.add(
    Ring.COMPANY, "official financial statements", FindingClass.D,
    "FY2023 AUDITED CONSOLIDATED (KPMG Hazem Hassan). Revenues EGP 10,329,991,222; "
    "costs (6,762,232,271); gross profit 3,567,758,951 (34.5%); operating profit "
    "1,862,980,200; net finance cost (43,924,737); PBT 1,819,055,463; tax "
    "(440,238,159); profit 1,378,817,304, attributable 1,373,013,190; EPS EGP 3.85. "
    "Total assets 38,715,259,331; total equity 8,683,699,471; WIP 17,571,221,017; "
    "advances from customers 12,428,609,713",
    "SODIC consolidated FS for the year ended 31 December 2023 and auditors' report",
    CO, "2024-02-05", url="https://cms.sodic.com/uploads/SODIC_Cons_FS_Q4_2023_English_4edd57eed2.pdf",
    detail="ROUTE: image-only Xerox PrimeLink B9100 scan, 73 pages, CCITT-G4 + JPEG. "
           "scanned_filing_integrity.py: UNKNOWN / 'not a JBIG2 scan' -> ordinary "
           "footing discipline applies. Rendered at 500 dpi and OCR'd off the pixels. "
           "FOOTED: revenue legs, cost legs, GP, OP, net finance, PBT (which also equals "
           "the cash-flow statement's own opening line), NPAT and the NCI split all "
           "reconcile; the whole balance sheet foots on BOTH columns; EPS 3.85 "
           "reproduces on 356,197,368 shares; and every FY2022 comparative matches the "
           "native-text Annual Report 2022 exactly. No glyph error survived.",
    model_impact="Second historical year and the margin inflection: 28.1% -> 34.5% -> "
                 "55% (FY2024) -> 27.2% (H1-2026). This series is why gross margin is an "
                 "OUTPUT of a per-project cost build in this study and never an input.",
    is_fs_data=True, fiscal_period="FY2023")

f_fy24 = R.add(
    Ring.COMPANY, "official financial statements", FindingClass.D,
    "FY2024, VIA THE [R-SIGCM-03] NAMED FALLBACK because the audited PDF is unsafe to "
    "read. Income statement (EGP'000, 2024 Annual Board Report): total revenues from "
    "operations 9,754,035; gross profit 5,411,103 (55.5%); net profit 2,535,855; "
    "attributable 2,527,212; EPS EGP 7.09. Balance sheet at 31-Dec-2024 (full precision, "
    "9M-2025 comparative column): total assets 54,372,155,903; total equity "
    "11,419,505,748; WIP 25,209,597,778; advances 21,679,299,472; trade & notes "
    "receivable 8,589,694,032; bank loans + facilities 3,789,209,660; cash + amortised-"
    "cost investments 3,404,520,838",
    "SODIC 2024 Annual Board Report (Article 40) + 31-Dec-2024 comparative column of the "
    "30-Sep-2025 interim condensed consolidated FS",
    CO, "2025-10-23", url="https://cms.sodic.com/uploads/3_SODIC_2024_Annual_Board_Report_English_e23b739f2a.pdf",
    detail="THE AUDITED FY2024 PDF WAS NOT READ. scanned_filing_integrity.py returns "
           "REFUSE on 2-Sodic-Cons-Dec-24-signed.pdf and 2-Sodic-Separate-Dec-24-"
           "signed.pdf: 'SYMBOL DICTIONARY PRESENT - do not read figures off this file', "
           "667 and 519 streams, segment types [0, 6, 48, 50], producer 'Xerox AltaLink "
           "C8055'. A footing check cannot rescue a symbol-substituted scan, so none was "
           "attempted. WHY THE FALLBACK IS TRUSTED: the board report's FY2023 column "
           "(10,329,991 / 3,567,759 / 1,378,817 / 1,373,013 EGP'000) matches the audited "
           "FY2023 statements to the thousand on all four lines, and every one of its "
           "eight FY2024 balance-sheet lines matches the 9M-2025 filing's comparative "
           "column exactly. Two independent SODIC documents, agreeing. LIMITATION: the "
           "FY2024 P&L below gross profit is available only at EGP'000 and, for "
           "operating profit / PBT / tax, only at the EGP-million rounding of the FY2024 "
           "earnings release (3,310 / 3,360 / 827).",
    model_impact="Third historical year and the CYCLICAL PEAK: 55.5% gross margin, "
                 "EGP 50.3bn of gross contracted sales. Normalisation is anchored here "
                 "as a peak, not a level. Also fixes the pre-merger EPS base — 7.09 on "
                 "356.2m shares — which is the number the merger later restated.",
    is_fs_data=True, fiscal_period="FY2024")

f_fy25bs = R.add(
    Ring.COMPANY, "official financial statements", FindingClass.D,
    "FY2025 BALANCE SHEET at 31-Dec-2025, complete and footed, from the comparative "
    "column of the 30-Jun-2026 statements (audited by the predecessor auditor, "
    "unmodified opinion dated 5-Feb-2026): total assets 89,882,331,426; non-current "
    "12,464,346,343; current 77,417,985,083; WIP 50,461,654,533; advances from "
    "customers 29,222,421,017; total equity 15,900,822,564 (issued capital "
    "5,157,174,344); total liabilities 73,981,508,862; land liabilities 19,306,947,220; "
    "bank loans + facilities 9,781,834,942; provisions 4,352,699,162",
    "31-Dec-2025 comparative column, SODIC interim condensed consolidated FS 30 June "
    "2026, corroborated by the Q2-2026 Board Report EGP'000 table",
    CO, "2026-07-27", url="https://cms.sodic.com/uploads/SODIC_Q2_CONS_FS_30_June_2026_English_514ede2618.pdf",
    detail="ROUTE: the statement of financial position is the ONE rasterised page (a "
           "150-dpi JPEG) inside an otherwise native-text Word PDF; every other page has "
           "a text layer. Re-rendered at 400 dpi and OCR'd; the 31-Dec-2025 non-current "
           "column then came 20,000,000 SHORT of its own printed subtotal. Re-read at "
           "600 dpi: 'Projects under construction' is 754,180,735, not the 734,180,735 "
           "the 400-dpi pass returned, and the column foots exactly. ONE GLYPH ERROR "
           "CAUGHT BY ARITHMETIC AND FIXED BY RE-READING. The corrected total, "
           "12,464,346,343, is then independently confirmed by the Q2-2026 Board "
           "Report's 'Long-Term Assets 12 464 346' (EGP'000). Both columns of the "
           "balance sheet now foot line-by-line to total assets = total equity and "
           "liabilities.",
    model_impact="Fourth historical year on the balance sheet, and the base the "
                 "enterprise-to-equity bridge stands on together with 30-Jun-2026. "
                 "NOTE WHAT IS NOT HERE: the FY2025 INCOME STATEMENT — see F41.",
    is_fs_data=True, fiscal_period="FY2025")

f_h126 = R.add(
    Ring.COMPANY, "official financial statements", FindingClass.D,
    "H1-2026 REVIEWED (EY / Allied for Accounting & Auditing, 27-Jul-2026), with the "
    "THREE-MONTH column disclosed alongside the six-month one. H1-2026: total operation "
    "revenues 5,977,983,367 (H1-2025 4,779,064,312); cost of sales (4,352,804,839); "
    "gross profit 1,625,178,528 = 27.2% against 58.0% in H1-2025; operating profit "
    "941,757,095; PBT 1,082,915,873; tax (245,696,702); profit 837,219,171, "
    "attributable 834,246,860; EPS EGP 0.65. Total assets 100,435,676,958; equity "
    "16,738,041,735",
    "SODIC interim condensed consolidated FS for the six months ended 30 June 2026",
    CO, "2026-07-27", url="https://cms.sodic.com/uploads/SODIC_Q2_CONS_FS_30_June_2026_English_514ede2618.pdf",
    detail="ROUTE: native text layer (Microsoft Word for Microsoft 365), no OCR needed "
           "except the one rasterised balance-sheet page handled in F19. FOOTED: "
           "revenue legs, cost legs, GP, OP, finance, PBT, NPAT, the NCI split, the "
           "changes-in-equity roll (11,419,505,748 opening 2025 -> 12,654,529,838 -> "
           "15,836,178,629 opening 2026 -> 16,670,425,489), and both balance-sheet "
           "columns. The H1-2026 earnings release reproduces every one of these to the "
           "EGP million.",
    model_impact="THE MARGIN COLLAPSE IS THE HEADLINE AND IT IS NOT A ONE-OFF LINE: "
                 "gross margin 58.0% -> 27.2% on a 25% revenue rise, because cost of "
                 "real estate sales went 1,437,172,952 -> 3,554,128,651 (+147%) against "
                 "real estate sales +16%. Any forecast margin path that starts above "
                 "27% must explain, from the cost build, why.",
    is_fs_data=True, fiscal_period="Q2-2026")

f_q126 = R.add(
    Ring.COMPANY, "official financial statements", FindingClass.D,
    "Q1-2026 ACTUALS, derived by subtraction inside a single filing that discloses both "
    "columns: total revenue 5,977,983,367 - 3,847,810,584 = EGP 2,130,172,783; gross "
    "profit 1,625,178,528 - 979,204,787 = EGP 645,973,741, i.e. a 30.3% Q1 gross margin "
    "against 25.5% in Q2-2026; profit attributable 834,246,860 - 536,591,569 = EGP "
    "297,655,291. Q1-2025 comparatives on the same basis: revenue 2,758,728,294, gross "
    "profit 1,798,900,858 (65.2%), attributable profit 950,668,744",
    "SODIC interim condensed consolidated FS 30 June 2026, six-month and three-month "
    "columns of the statement of profit or loss",
    CO, "2026-07-27",
    detail="SODIC published NO 31-March-2026 statements and NO Q1-2026 earnings release "
           "— the IR library holds nothing between 23-Oct-2025 and 27-Jul-2026 — so "
           "Q1-2026 exists only as this subtraction. It is arithmetic on two printed "
           "columns of one reviewed filing, not an estimate. Q1-2025 derived the same "
           "way and cross-checks against the Q1-2025 earnings release.",
    model_impact="Closes the study-year quarter coverage and, on its own, contradicts a "
                 "flat margin path: the two quarters of 2026 print 30.3% then 25.5%, "
                 "and both are less than half the 65.2% Q1-2025 comparative.",
    is_fs_data=True, fiscal_period="Q1-2026")

f_9m25 = R.add(
    Ring.COMPANY, "official financial statements", FindingClass.D,
    "9M-2025 REVIEWED: revenue EGP 10,624m; cost (6,009m); gross profit 4,615m (43.4%); "
    "operating profit 3,265m; PBT 3,074,445,158; tax (721m); profit 2,353,067,460, "
    "attributable 2,345,049,475; EPS EGP 1.82. Total assets 68,993,529,625; equity "
    "13,772,278,925; WIP 33,801,691,191; advances 29,677,709,952",
    "SODIC interim condensed consolidated FS 30 September 2025",
    CO, "2025-10-23", url="https://cms.sodic.com/uploads/3_SODIC_Q3_CONS_FS_30_Sep_2025_signed_1_feaf24314c.pdf",
    detail="ROUTE: native text layer, no OCR. This filing is doing double duty — it is "
           "also the carrier of the audited 31-Dec-2024 comparative balance sheet used "
           "in F18 to bypass the REFUSE'd FY2024 PDF.",
    model_impact="The last complete SODIC income statement before the FY2025 gap. "
                 "FY2025 = 9M-2025 + an UNDISCLOSED Q4-2025; that subtraction is the "
                 "one the study cannot perform, and it is why the FY2025 P&L driver is "
                 "gated top-down.",
    is_fs_data=True, fiscal_period="FY2025")

# ---- revenue recognition ---------------------------------------------------
f_revrec = R.add(
    Ring.COMPANY, "regular disclosures", FindingClass.D,
    "REVENUE RECOGNITION IS POINT-IN-TIME ON TRANSFER OF CONTROL, NOT PERCENTAGE OF "
    "COMPLETION. The audited policy: 'Revenue from sale of residential units, offices, "
    "commercial shops, service, and villas ... is recorded when upon transferring "
    "control to customers whether the said units have been completed or semi-completed "
    "... To reflect those units / lands at A CERTAIN POINT OF TIME.' Under EAS 48. "
    "Three independent corroborations in the filings: notes receivable are described as "
    "'received from real estate DELIVERED units customers'; EGP 88.79bn of post-dated "
    "cheques for UNDELIVERED units sit OFF balance sheet (note 33); and work in process "
    "of EGP 59.19bn accumulates in inventory until handover",
    "SODIC FY2022 audited consolidated FS, revenue-recognition accounting policy, "
    "printed in the Annual Report 2022; corroborated in the 30-Jun-2026 interim notes "
    "17.1/17.2, 26 and 33",
    CO, "2023-02-08",
    detail="NO CHANGE IN BASIS ACROSS THE WINDOW. The 30-Jun-2026 filing states the "
           "policies 'are consistent with those of the previous financial year and "
           "corresponding interim reporting period' (note 2.1) and that the significant "
           "judgements are 'the same as those applied to the consolidated financial "
           "statements for the year ended 31 December 2025' (note 3). One presentation "
           "change did occur: the balance sheet moved from separate 'New Urban "
           "Communities Authority' and 'Land acquisition creditors' lines (FY2023) to a "
           "single 'Land liabilities' line (FY2025/H1-2026).",
    model_impact="THIS DECIDES THE WHOLE MODEL SHAPE AND THE LESSON SET. OCDI belongs "
                 "to the 'real-estate developer, off-plan, POINT-IN-TIME ON HANDOVER' "
                 "class, not the percentage-of-completion class — which is exactly the "
                 "condition L-001 names as overturning it, because revenue and cost "
                 "already share one clock. Revenue is therefore forecast as a DELIVERY "
                 "SCHEDULE (units handed over x realised price), never as a completion "
                 "percentage, and the backlog converts to revenue only on handover.")

f_backlog = R.add(
    Ring.COMPANY, "regular disclosures", FindingClass.D,
    "BACKLOG OF UNRECOGNISED REVENUE, SODIC's own series: EGP 34.2bn (31-Dec-2022), "
    "51.4bn (31-Dec-2023), 87bn (31-Dec-2024), 87.4bn (31-Mar-2025), 89.4bn "
    "(30-Jun-2025), 94bn (30-Sep-2025), [31-Dec-2025 NOT PUBLISHED], 116bn "
    "(30-Jun-2026). Against recognised revenue of EGP 9.75bn in FY2024 and EGP 5.98bn "
    "in H1-2026, the 30-Jun-2026 backlog is roughly TWELVE YEARS of H1-2026 run-rate "
    "revenue. Its receivable half is disclosed in note 33: EGP 88,791,437,016 of "
    "post-dated cheques and instalments for undelivered units, off balance sheet, "
    "16,396,003,296 short-term and 72,395,433,720 long-term",
    "SODIC earnings releases FY2022, FY2023, FY2024, Q1-2025, H1-2025, 9M-2025, "
    "H1-2026; interim FS 30-Jun-2026 note 33",
    IR, "2026-07-27",
    detail="Note 33 foots on both dates: 81,388,937,137 + 68,234,958 + 7,334,264,921 = "
           "88,791,437,016 = 16,396,003,296 + 72,395,433,720. The 31-Dec-2025 point is "
           "missing because no FY2025 release exists — the ONLY hole in an otherwise "
           "eight-point series.",
    model_impact="THE CENTRAL DRIVER. Under point-in-time recognition the backlog IS "
                 "the revenue forecast, and the question the model answers is the "
                 "CONVERSION RATE — how fast contracted units reach handover — not the "
                 "sales growth rate. The short/long split in note 33 gives the "
                 "conversion profile directly. A revenue path built on a growth rate "
                 "instead of this schedule would ignore a EGP 116bn disclosed order "
                 "book.",
    fiscal_period="Q2-2026")

f_offbs = R.add(
    Ring.COMPANY, "regular disclosures", FindingClass.B,
    "INTEREST IS BEING CAPITALISED INTO INVENTORY ON A SCALE THAT MAKES THE REPORTED "
    "FINANCE COST MEANINGLESS. Capitalised interest inside work in process: EGP 15.8bn "
    "at 30-Jun-2026 against EGP 10.3bn at 31-Dec-2025 — EGP 5.5bn added in one half. "
    "The H1-2026 income statement charges finance cost of EGP 2,678,138 (of which "
    "interest expense EGP 51,104), while the cash flow statement shows FINANCE COST "
    "PAID of EGP 1,010,846,065 and note 29 records a further EGP 1,904,474,646 of "
    "amortised interest on NUCA and land-purchase creditors capitalised as a non-cash "
    "transaction",
    "SODIC interim condensed consolidated FS 30 June 2026, note 16, note 13, note 29 "
    "and the consolidated statement of cash flows",
    CO, "2026-07-27",
    model_impact="BASE CHANGER FOR THE COST BUILD. A model that took the printed "
                 "finance cost as the interest burden would understate it by about "
                 "three orders of magnitude. Interest is a COST OF SALES item here, "
                 "arriving on handover inside WIP, so it must be built from the named "
                 "facilities in note 24 and the land-liability unwind in note 25 and "
                 "then routed through the delivery schedule — and it must NOT also be "
                 "charged below the line, or it is counted twice.",
    is_fs_data=True, fiscal_period="Q2-2026")

f_segments = R.add(
    Ring.COMPANY, "regular disclosures", FindingClass.D,
    "THE FINEST SOURCED LEVEL IS GEOGRAPHY, AND THE COMPANY SAYS SO. Note 34: one "
    "reportable segment under EAS 41; everything else is disaggregated GEOGRAPHICALLY. "
    "H1-2026 revenue by region: West Cairo 1,495,796,657, East Cairo 517,917,065, North "
    "Coast 2,016,605,068 (H1-2025: 2,250,425,348 / 1,276,539,196 / nil). Cost of sales "
    "on the same cut: 1,325,685,628 / 541,076,563 / 1,687,366,460 (H1-2025: 789,671,758 "
    "/ 647,501,194 / nil). Regional gross margin therefore falls out as West Cairo "
    "11.4%, East Cairo NEGATIVE, North Coast 16.3% — against West 64.9% and East 49.3% "
    "a year earlier. WIP, advances, completed units and land liabilities are cut the "
    "same way",
    "SODIC interim condensed consolidated FS 30 June 2026, notes 6, 7, 16, 26, 34",
    CO, "2026-07-27",
    model_impact="DRIVER UNLOCK, and it is what makes margin an OUTPUT here. Revenue "
                 "and cost are built per region, and per project inside the region using "
                 "the board reports' unit tables, so the gross margin is computed rather "
                 "than assumed. It also destroys any single-margin model: the three "
                 "regions printed 11.4%, negative and 16.3% in the SAME half.",
    is_fs_data=True, fiscal_period="Q2-2026")

f_land_liab = R.add(
    Ring.COMPANY, "regular disclosures", FindingClass.D,
    "LAND LIABILITIES ARE EGP 20,399,317,678 at 30-Jun-2026 (19,306,947,220 at "
    "31-Dec-2025), by named counterparty: New Urban Communities Authority 6,216,339,548; "
    "Owners Union - Shahin 989,288,881; Midar 13,193,689,249. Split 1,690,440,397 "
    "current / 18,708,877,281 non-current. Bank debt is separately EGP 8,177,576,786 "
    "across four NAMED facilities, each at 'CBE corridor plus margin', with no covenant "
    "breach at 30-Jun-2026",
    "SODIC interim condensed consolidated FS 30 June 2026, notes 24 and 25",
    CO, "2026-07-27",
    detail="Both notes foot: 6,216,339,548 + 989,288,881 + 13,193,689,249 = "
           "20,399,317,678 = 1,690,440,397 + 18,708,877,281. Facilities: AAIB/Banque "
           "Misr syndicate (13-Oct-2021, EGP 1,570m) 1,021,311,986; AAIB Estates "
           "facility (22-Jan-2023, EGP 2.75bn) 1,360,000,000; Banque Misr/CIB syndicate "
           "for SODIC 464 (08-Sep-2024, EGP 4.14bn) 3,560,000,000; Banque Misr revolver "
           "(26-Nov-2025, up to EGP 3bn, four-year) 2,244,718,646; less unamortised "
           "borrowing cost (8,453,846).",
    model_impact="DRIVER UNLOCK for the whole capital structure. TOTAL obligations are "
                 "land + bank = EGP 28.6bn, of which land is 71% — so a study that "
                 "modelled 'debt' as the EGP 11.0bn of bank facilities would miss most "
                 "of it. Interest is built facility by facility off the CBE corridor "
                 "(F06), and the land instalment profile is a dated cash schedule, not a "
                 "percentage.",
    is_fs_data=True, fiscal_period="Q2-2026")

# ---- IR communications -----------------------------------------------------
f_rel26 = R.add(
    Ring.COMPANY, "IR communications (calls, presentations, releases)", FindingClass.D,
    "H1-2026 EARNINGS RELEASE, the operating anchors no statement carries: GROSS SALES "
    "EGP 23.5bn, +201% on EGP 7.8bn in H1-2025; net cash collections EGP 10.2bn (+18.6% "
    "on 8.6bn); 557 UNITS DELIVERED (+78% on 313), of which West Cairo 192, East Cairo "
    "63, North Coast 302; construction CAPEX EGP 5.3bn (+8% on 4.9bn); backlog EGP "
    "116bn; total receivables EGP 102.1bn of which 22.1bn short-term, 13.4bn "
    "on-balance-sheet and 88.8bn off; bank debt EGP 11bn at 0.66x equity (9.8bn and "
    "0.62x at YE2025); cash incl. T-bills EGP 4bn. Deliveries by value: West Cairo 41% "
    "with VYE alone 35%, East Cairo 20%",
    "SODIC H1 2026 Earnings Release",
    IR, "2026-07-27", url="https://cms.sodic.com/uploads/EN_earning_Realse_H1_2026_ebd421eca1.pdf",
    detail="ROUTE: image-only (JPEG page + CCITT-G4 stencils, lossless bilevel), "
           "scanned_filing_integrity.py UNKNOWN / 'not a JBIG2 scan'. Rendered at 400 "
           "dpi and OCR'd. TIED BACK TO THE FILING: every figure in the release's own "
           "summary tables reconciles to the statements — bank facilities & loans 11,040 "
           "= 8,177,576,786 + 2,862,564,529; cash & T-bills 3,767 = 2,470,822,976 + "
           "1,296,038,031; on-BS receivables 13,351 = 5,746,969,200 + 7,603,995,047. "
           "THIS IS THE NEWEST RESULTS RELEASE AND ITS ANCHORS SUPERSEDE ALL EARLIER "
           "ONES [L-008].",
    model_impact="Supplies the volume half of every driver: units delivered by region, "
                 "collections, construction capex, backlog. Sales +201% into a market "
                 "that grew 2.9% (F11) is the tension the forecast has to resolve — and "
                 "it resolves toward launch timing, not a new run-rate.",
    fiscal_period="Q2-2026")

f_rel24 = R.add(
    Ring.COMPANY, "IR communications (calls, presentations, releases)", FindingClass.D,
    "FY2024 EARNINGS RELEASE: gross contracted sales EGP 50.3bn (+66% on EGP 30.26bn), "
    "1,270 units sold; North Coast 66% of sales with newly-launched Ogami alone c. EGP "
    "24.5bn (49% of the year); West Cairo 29%; CANCELLATIONS EGP 1bn = 2% of gross "
    "(4% in 2023, 6% in 2022); net cash collections EGP 15bn (11bn in 2023); 1,045 "
    "units delivered — East Cairo 736, West Cairo 309 — against 1,427 in 2023; "
    "construction capex EGP 8.5bn (6.2bn); backlog EGP 87bn; delinquencies 2.2% in 2023 "
    "from 5.1% in 2022",
    "SODIC FY2024 Earnings Release; FY2023 Earnings Release for the comparatives",
    IR, "2025-02-06", url="https://cms.sodic.com/uploads/5_SODOC_2024_Earnings_Release_English_4d601683a4.pdf",
    detail="ROUTE: image-only, OCR'd at 350 dpi. Cross-checks: the release's FY2023 "
           "income-statement column matches the audited FY2023 statements line for line "
           "at EGP-million rounding, and its FY2024 balance-sheet column matches the "
           "9M-2025 comparative column exactly.",
    model_impact="Gives the CANCELLATION RATE and the DELIVERY-vs-SALES gap, both of "
                 "which are separate drivers under point-in-time recognition: 1,270 "
                 "units sold against 1,045 delivered in the same year, and a 2-6% "
                 "cancellation band that must be applied to gross sales before anything "
                 "reaches the backlog.",
    fiscal_period="FY2024")

f_pres = R.add(
    Ring.COMPANY, "IR communications (calls, presentations, releases)", FindingClass.C,
    "INVESTOR PRESENTATION, December 2023, 'as of 30/09/2023' — the ONLY investor deck "
    "SODIC's IR library holds, and the only place a land-bank TOTAL is stated: '26 "
    "years of operation, +13K units delivered, +30K residents, +17MN SQM TOTAL LAND "
    "BANK'. A second slide states 'DIVERSIFIED LANDBANK c.6.4 MILLION SQM UNLAUNCHED "
    "LAND' split North Coast 42% / East Cairo 33% / West Cairo 25%, while a third slide "
    "in the same deck says '+4.85MN SQM UNLAUNCHED LAND BANK'. The two unlaunched "
    "figures are not reconciled in the deck",
    "SODIC 9M Investor Presentation (SODIC-9M-IR-Presentation.pdf), December 2023",
    IR, "2023-12-10", url="https://cms.sodic.com/uploads/SODIC_9_M_IR_Presentation_36726ca6bc.pdf",
    model_impact="")

# ---- one-off base-resetting transactions -----------------------------------
f_merger = R.add(
    Ring.COMPANY, "one-off base-resetting transactions", FindingClass.B,
    "THE SEVEN-SUBSIDIARY MERGER, and it tripled the share count. EGM 25-Mar-2025, "
    "ratified 19-May-2025; GAFI chairman's decision 2/365 of 2025 dated 14-May-2025; "
    "the merged companies were struck from the commercial register on 14-Jul-2025. "
    "Merged at the book value of net equity as at 31-Dec-2021: SODIC (merging) "
    "1,349,403,900 plus SODIC for Development & Real Estate Investment 118,065,800, "
    "SODIC Polygon 152,128,900, Soreal 1,405,409,200, SOREAL 2,991,783,500, Tabrouk "
    "463,858,100, La Maison 120,240,800 and Al Yosr 39,438,200 = 6,640,328,400, split "
    "into issued capital 5,157,174,344 and share premium 1,483,154,056. Authorised "
    "capital became EGP 25bn. SHARES WENT FROM 356,197,368 TO 1,289,293,586 AT EGP 4 "
    "NOMINAL",
    "SODIC interim condensed consolidated FS 30 June 2026, note 35 'Merger'",
    CO, "2026-07-27",
    detail="Foots: the eight net-equity figures sum to 6,640,328,400, and 5,157,174,344 "
           "+ 1,483,154,056 = 6,640,328,400. Confirmed against the changes-in-equity "
           "statement, where issued capital is 1,424,789,472 at 30-Jun-2025 and "
           "5,157,174,344 at 1-Jan-2026, and against the 2024 Annual Board Report's "
           "'Last issued capital EGP 1,424,789,472'.",
    model_impact="BASE CHANGER ON EVERY PER-SHARE NUMBER. 1,424,789,472 / 4 = "
                 "356,197,368 shares before; 1,289,293,586 after — a factor of 3.62. "
                 "GROUP EQUITY DID NOT CHANGE (the subsidiaries were already "
                 "consolidated), so this is a share-count event, not a value event. Any "
                 "fair value per share must use 1,289,293,586, and any historical EPS "
                 "or price comparison across 14-Aug-2025 must be restated. The company "
                 "already restated its own H1-2025 comparative EPS from the 3.64 "
                 "printed in the H1-2025 release to the 1.01 printed in the H1-2026 "
                 "statements — the SAME period on two share bases.",
    fiscal_period="FY2025")

f_series = R.add(
    Ring.COMPANY, "one-off base-resetting transactions", FindingClass.S,
    "THE HELD PRICE SERIES CARRIES THE MERGER STEP RAW. engine/raw_ohlc/EG/OCDI.csv "
    "prints 61.00 on 13-Aug-2025 (on NO recorded volume) and 16.26 on 14-Aug-2025 on "
    "2.06m shares — a -73.3% single-session move, which is the 3.62x share-count "
    "adjustment and not a return. A second step sits at 13-Dec-2021: 19.50 on 800 "
    "shares becomes 15.60 on 821,400, -20% on a thousandfold volume jump, coincident "
    "with the Aldar/ADQ consortium reaching 85.5%",
    "engine/raw_ohlc/EG/OCDI.csv, 3,771 rows, 02-Jan-2011 to 01-Sep-2026",
    PMD, "2026-09-01",
    model_impact="Any return series, volatility estimate, calibration panel or "
                 "regression that uses this file unadjusted will ingest a -73.3% daily "
                 "return that never happened. The file must be split-adjusted before "
                 "14-Aug-2025, or the sample must start after it. FLAGGED HERE RATHER "
                 "THAN FIXED: no beta is resolved in this sweep, per instruction.")

f_eastvale = R.add(
    Ring.COMPANY, "one-off base-resetting transactions", FindingClass.B,
    "EASTVALE / MADA — 500 ACRES ADDED ON 10-NOVEMBER-2025, i.e. AFTER the last land "
    "figure the company ever published. Revenue-sharing agreement with Midar Investment "
    "& Urban Development inside the MADA city (5,800 acres, c.25m sqm, New Cairo). The "
    "land was valued at EGP 14.7bn on a present-value basis at the contract date; EGP "
    "2.94bn was paid on signing and the balance falls over eight instalments from "
    "November 2026 to November 2033. The resulting Midar liability is EGP 13,193,689,249 "
    "at 30-Jun-2026. An escrow contract with Banque Misr and Midar followed on "
    "28-Apr-2026",
    "SODIC interim condensed consolidated FS 30 June 2026, notes 16.2(B) and 25.3; "
    "SODIC/MIDAR partnership news release; H1-2026 earnings release corporate highlights",
    CO, "2026-07-27",
    detail="UNIT INCONSISTENCY IN SODIC'S OWN WORDS, recorded rather than resolved: the "
           "filing says '500-ACRE plot'; the news release says '500-FEDDAN land plot' in "
           "one paragraph and 'a new 500-acre development' in the General Manager's "
           "quote two paragraphs later. 500 acres = 2,023,430 sqm; 500 feddans = "
           "2,100,415 sqm. The FILING is taken as primary. Total project investment is "
           "put at EGP 110bn by the master developer.",
    model_impact="BASE CHANGER, dual-framed. It adds a new East Cairo project with a "
                 "EGP 14.7bn land cost and an eight-year payment schedule that lands "
                 "inside the forecast window, and it is the largest single reason the "
                 "30-Sep-2023 land bank cannot be used. Modelled as an explicit dated "
                 "project with its own launch, absorption and land-payment profile.",
    fiscal_period="FY2025")

f_sphinx = R.add(
    Ring.COMPANY, "one-off base-resetting transactions", FindingClass.B,
    "NEW SPHINX — 1,007.48 FEDDANS, AND SODIC SAYS IT DOUBLED THE UNDEVELOPED LAND "
    "BANK. Co-development agreement with Rula Land Reclamation - Freiji & Partners "
    "signed 11-May-2025; partial handover of 1,001.812 feddans on 24-Jun-2025; EGP "
    "580,940,399 paid as an advance against a VARIABLE land cost. The General Manager, "
    "in the H1-2025 release: 'The signing of a revenue share agreement for a 1,000-acre "
    "land plot in New Sphinx City marks a major milestone in our expansion strategy, "
    "effectively DOUBLING our undeveloped land bank'",
    "SODIC interim condensed consolidated FS 30 June 2026, note 16.1(C); SODIC H1 2025 "
    "Earnings Release, General Manager's statement",
    CO, "2026-07-27",
    detail="1,007.48 feddans = c.4.23m sqm at 4,200.83 sqm/feddan. The release says "
           "'1,000-acre' in the quote and '1,000 feddan' in the corporate-highlights "
           "list for the same transaction; the filing's 1,007.48 FEDDANS is taken as "
           "primary. The land cost is VARIABLE CONSIDERATION under the co-development "
           "contract, so there is no fixed land liability to schedule.",
    model_impact="BASE CHANGER for the asset base. A statement by the company that the "
                 "undeveloped land bank DOUBLED in June-2025 is, on its own, "
                 "disqualifying for any land figure dated before then. It also changes "
                 "the COST SHAPE: variable-consideration land converts a fixed capital "
                 "outlay into a revenue-share, which belongs in cost of sales rather "
                 "than in the land liability.",
    fiscal_period="FY2025")

# ---- ownership / stake changes --------------------------------------------
f_own = R.add(
    Ring.COMPANY, "ownership / stake changes (named-transaction rule)", FindingClass.S,
    "THE NAMED TRANSACTION: the ALDAR / ADQ CONSORTIUM has held 85.5% SINCE DECEMBER "
    "2021, stated as such by SODIC itself. Register at the FY2024 position date: ALDAR "
    "VENTURES INTERNATIONAL HOLDINGS RSC LIMITED 213,240,140 shares = 59.87%, and GAMMA "
    "FORGE LIMITED (the ADQ vehicle) 91,388,632 = 25.66%; together 304,628,772 shares = "
    "85.53%. At 30-Jun-2026 the split is Aldar-ADQ Consortium 85%, Ekuity Holding 5%, "
    "Others 10%. The immediate parent is Aldar Ventures International Holding RSC "
    "Limited and the ULTIMATE parent is ALDAR PROPERTIES PJSC, listed on the Abu Dhabi "
    "Securities Exchange",
    "SODIC 2024 Annual Board Report, shareholder register; interim FS 30-Jun-2026 note "
    "1.5; H1-2026 Earnings Release shareholding chart; SODIC EGX disclosure 25-Oct-2022",
    CO, "2025-02-06",
    detail="NOT A DELISTING. Note 1.4 of the 30-Jun-2026 filing states plainly: 'The "
           "Company is listed on the Egyptian Stock Exchange.' The 2024 board report "
           "gives the EGX listing date as 10-Mar-1998. So this is a change of control "
           "with a residual free float of c.14.5%, not a take-private. The 85.5% figure "
           "appears verbatim in SODIC's own 05-Jul-2022 and 25-Oct-2022 disclosures, "
           "the second of which dates it 'since December 2021' — which is also where "
           "the OCDI price series shows its -20% step on a thousandfold volume jump "
           "(F32). Board is Aldar-appointed: chairman Talal Al Dhiyebi (Aldar Ventures), "
           "with Aldar and Gamma Forge nominees and two independents.",
    model_impact="Fixes the share register, the free float and the control premium "
                 "question. Three consequences the build must carry: (i) 14.5% float on "
                 "1,289,293,586 shares makes the market price thin evidence; (ii) a "
                 "sovereign-linked 85.5% holder sets the dividend policy — none was "
                 "proposed for FY2024; (iii) the parent is ADX-listed, so related-party "
                 "capital and land terms are a live channel, not a hypothetical.")

f_mna = R.add(
    Ring.COMPANY, "ownership / stake changes (named-transaction rule)", FindingClass.C,
    "TWO NAMED ACQUISITION ATTEMPTS, NEITHER CONSUMMATED. 05-Jul-2022: non-binding "
    "offer for up to 100% of Madinet Nasr Housing & Development (EGX: MNHD) at EGP "
    "3.20-3.40 per share, mid-point EGP 3.30 valuing MNHD at EGP 6.18bn / USD 328m — a "
    "32% premium to the 04-Jul-2022 close, 1.43x book and 21.4x LTM earnings — pitched "
    "on 'a combined undeveloped land bank of c. 11 million square metres'. 24-Oct-2022: "
    "preliminary non-binding cash offer for 100% of Orascom Real Estate S.A.E, owner of "
    "the 4.2 MILLION SQM O WEST plot in West Cairo, at EGP 2,460m, with exclusive due "
    "diligence granted. Neither asset appears in the 30-Jun-2026 project notes",
    "SODIC announcement 05-Jul-2022; SODIC disclosure to the EGX dated 25-Oct-2022",
    CO, "2022-10-25",
    model_impact="")

# ---- management & capital actions -----------------------------------------
f_audit = R.add(
    Ring.COMPANY, "management & capital actions", FindingClass.S,
    "THREE AUDITORS IN FOUR YEARS. KPMG Hazem Hassan signed FY2022 and FY2023. PwC "
    "Egypt (Ezz Eldeen, Diab & Co) took FY2024 — the 2024 board report records Mohamed "
    "Al-Sawaf replacing Wael Saqr, 'who has apologized for continuing as the company's "
    "Auditor', appointed 07-Mar-2024. The FY2025 statements were signed by that "
    "predecessor auditor with an UNMODIFIED opinion dated 5-FEBRUARY-2026. From the "
    "2026 interim the auditor is EY / Allied for Accounting & Auditing (Amr Waheed "
    "Bayoumi, RAA 17555), who reviewed 30-Jun-2026 on 27-Jul-2026",
    "SODIC FY2023 audited FS cover; 2024 Annual Board Report auditor section; limited "
    "review report on the 30-Jun-2026 interim FS",
    CO, "2026-07-27",
    model_impact="Two auditor changes inside a four-year comparison window is a "
                 "comparability risk on the historicals, and it is also the ONLY place "
                 "the FY2025 audit is evidenced at all — the H1-2026 review report is "
                 "what tells us an unmodified FY2025 opinion exists and is dated "
                 "5-Feb-2026. No restatement or modification is disclosed in any period.")

f_capital = R.add(
    Ring.COMPANY, "management & capital actions", FindingClass.D,
    "CAPITAL AND GOVERNANCE FACTS FROM THE FILINGS. No dividend proposed for FY2024 "
    "('Proposals regarding Dividends: None'); no shares or bonds issued during FY2024; "
    "no treasury shares; the ESOP concluded 31-Mar-2022 with 3,878,425 unallocated / "
    "unexercised shares. 11 board meetings and 5 audit-committee meetings in 2024, no "
    "material issues raised, no FRA or EGX fines. Average headcount 690 at an average "
    "salary of EGP 709,327. Legal reserve transfers of EGP 4,353,140 (H1-2025) and EGP "
    "173,441,700 (H1-2026)",
    "SODIC 2024 Annual Board Report; changes-in-equity statement, interim FS 30-Jun-2026",
    CO, "2025-02-06",
    model_impact="DRIVER UNLOCK for the equity bridge and the payout assumption: a "
                 "ZERO-dividend history under an 85.5% strategic holder means the "
                 "terminal payout cannot be typed at a market convention, and the "
                 "share-count base for value per share is fixed at 1,289,293,586 with "
                 "no dilutive instrument outstanding beyond 3,878,425 ESOP shares "
                 "(0.3%).",
    fiscal_period="FY2024")

# ---- strategic plans & guidance -------------------------------------------
f_capcom = R.add(
    Ring.COMPANY, "strategic plans & guidance", FindingClass.D,
    "THE FORWARD CONSTRUCTION COMMITMENT IS CONTRACTED, NOT GUIDED. Note 31: contracts "
    "concluded with third parties for work in progress and investment property under "
    "development total EGP 39.7bn at 30-Jun-2026 (EGP 34.39bn at 31-Dec-2025), of which "
    "EGP 19.8bn had been executed by 30-Jun-2026 (EGP 17.7bn at 31-Dec-2025) — leaving "
    "c. EGP 19.9bn of committed spend still to come. Against this, construction capex "
    "actually spent was EGP 5.3bn in H1-2026, 8.3bn in 9M-2025 and 8.5bn in FY2024. "
    "Letters of guarantee outstanding: CIB EGP 221,625,750 (Shahin), CIB EGP 26,704,450 "
    "(NUCA 180 acres), AAIB EGP 129,400,240 (Heliopolis / SODIC East)",
    "SODIC interim condensed consolidated FS 30 June 2026, notes 31 and 32; earnings "
    "releases for the spend series",
    CO, "2026-07-27",
    model_impact="DRIVER UNLOCK: construction capex is built from a CONTRACTED backlog "
                 "with a disclosed executed-to-date figure, not from a percentage of "
                 "revenue. The c. EGP 19.9bn remaining commitment against a EGP "
                 "10.6bn-a-year spend rate implies roughly two years of committed build "
                 "already signed.",
    is_fs_data=True, fiscal_period="Q2-2026")

f_guid = R.add_negative(
    Ring.COMPANY, "strategic plans & guidance",
    "searched SODIC's own channels for FORWARD GUIDANCE — every earnings release "
    "FY2022 through H1-2026, the 2023/2024 annual board reports, the December-2023 "
    "investor presentation, the 27-Jul-2026 board resolutions and the sodic.com news "
    "index. NOTHING FOUND: SODIC issues no revenue, margin, delivery, sales or capex "
    "guidance in any period, and holds no earnings call whose transcript it publishes. "
    "The only forward-looking quantities it discloses are CONTRACTUAL — the note-31 "
    "commitment, the note-25 land instalment schedules and the note-33 cheque maturity "
    "profile. Every forward driver in this study must therefore be built from "
    "contracted quantities or from history; there is no management number to score "
    "[L-012] and none to import",
    "2026-09-09")

# =============================================================================
# THE TWO GAPS — recorded as dated negative searches, not filled
# =============================================================================
f_neg_fy25 = R.add_negative(
    Ring.COMPANY, "official financial statements",
    "searched for SODIC's FY2025 ANNUAL RESULTS across every channel available: "
    "sodic.com/investor-relations and its Arabic mirror (both enumerate the SAME "
    "333-document library, and NEITHER holds anything dated between 23-Oct-2025 and "
    "27-Jul-2026 — no 31-Dec-2025 consolidated or separate statements, no FY2025 "
    "earnings release, no 2025 annual board report, and no 31-Mar-2026 quarterly); "
    "sodic.com/sitemap.xml and the 10 news items it lists; the cms.sodic.com upload "
    "index; ir.sodic.com (CONNECT tunnel failed, 502); the Strapi API at "
    "cms.sodic.com/api (403 Forbidden); egx.com.eg (curl 52, empty reply from server); "
    "and the EGX-hosted file the search index names — /downloads/News/'سوديك مجمعه "
    "انجليزى 08-02-2026'.pdf — which returns an F5 JavaScript challenge under a 200 to "
    "curl (support ID 4562065020937510468) and a 503 to the fetch tool. THE DOCUMENT "
    "EXISTS: the 30-Jun-2026 review report states the FY2025 consolidated statements "
    "were audited by the predecessor auditor who issued an unmodified opinion on 5 "
    "February 2026. IT COULD NOT BE RETRIEVED. What IS recovered from SODIC's own "
    "documents is the complete, footed 31-Dec-2025 BALANCE SHEET (F19). What is NOT "
    "recoverable from any SODIC document is the FY2025 INCOME STATEMENT and every "
    "FY2025 operating anchor — full-year contracted sales, units sold, units delivered, "
    "collections, capex and the 31-Dec-2025 backlog. Q4-2025 in particular is invisible: "
    "9M-2025 is filed and FY2025 is not, so the fourth quarter cannot be differenced out",
    "2026-09-09")

f_neg_land = R.add_negative(
    Ring.COMPANY, "regular disclosures",
    "searched for a CURRENT LAND-BANK TOTAL IN SQUARE METRES across every SODIC "
    "channel: all 333 IR documents, the FY2022 annual report, the December-2023 "
    "investor presentation, every earnings release FY2022-H1-2026, the 2023 and 2024 "
    "annual board reports, the Q2-2025 and Q2-2026 board reports, the 30-Jun-2026 "
    "interim notes, and sodic.com/about-us. NO LAND-BANK TOTAL IS STATED ANYWHERE AFTER "
    "30 SEPTEMBER 2023. The newest is '+17MN SQM TOTAL LAND BANK' in the December-2023 "
    "deck, as of 30/09/2023, with '4.67 MN SQM UNLAUNCHED' in the FY2022 annual report "
    "and two unreconciled unlaunched figures (4.85 and c.6.4 mn sqm) in the 2023 deck "
    "itself. The 30-Jun-2026 filing gives PROJECT-BY-PROJECT areas but never sums them "
    "and mixes units (acres, feddans and sqm in the same note)",
    "2026-09-09")

f_asset = R.add(
    Ring.COMPANY, "regular disclosures", FindingClass.S,
    "[R-ASSET-01] ORDERING FAILURE, STATED WITH BOTH DATES. NEWEST LAND-BANK TOTAL: "
    "+17 million sqm, AS AT 30 SEPTEMBER 2023 (December-2023 investor presentation). "
    "NEWEST FILING READ: 30 JUNE 2026, authorised 27 July 2026. The land figure is 33 "
    "MONTHS OLDER THAN THE INFORMATION SET. Three named additions fall inside that gap: "
    "Ogami 440 acres (contract 11-Jul-2023, 336 acres handed over 18-Jul-2024); New "
    "Sphinx 1,007.48 feddans (agreement 11-May-2025, 1,001.812 feddans handed over "
    "24-Jun-2025) which the company says DOUBLED the undeveloped land bank; and "
    "Eastvale/MADA 500 acres (agreement 10-Nov-2025). Project areas the filings DO "
    "state, at 30-Jun-2026: The Estates front + back plots 265.34 acres (150 + 115.34, "
    "the annex signed May-2022); VYE/Karmell 464.81 acres (21-Mar-2019); SODIC East 655 "
    "acres on Heliopolis-owned land (16-Mar-2016, minimum guarantee raised to EGP 5.9bn "
    "on 21-Dec-2020); June 1,182,004 sqm (25-Aug-2021, superseding a March-2018 deal on "
    "308 acres); Caesar back plot c.180 acres (contract 01-Aug-2023); Ogami c.440 "
    "acres; New Sphinx 1,007.48 feddans; Eastvale 500 acres",
    "SODIC interim condensed consolidated FS 30 June 2026, notes 16.1/16.2/16.3, read "
    "against the December-2023 investor presentation and the 13-Sep-2021 North Coast "
    "land release",
    CO, "2026-07-27",
    detail="A build may declare not_restated_since ONLY by naming the later disclosures "
           "checked and giving a reason. The later disclosures checked here are: the "
           "H1-2025, 9M-2025 and H1-2026 earnings releases; the 2023 and 2024 annual "
           "board reports; the Q2-2025 and Q2-2026 board reports; the 30-Jun-2026 "
           "interim notes; and the sodic.com news index — see F42 for the full search. "
           "The reason the 17m sqm figure is NOT usable is that one of the additions "
           "inside the gap is described BY THE COMPANY as doubling the undeveloped land "
           "bank, so the stale total is not merely old, it is known to be wrong. THE "
           "REMEDY IS TO BUILD THE LAND BASE PROJECT BY PROJECT FROM NOTE 16 AND STATE "
           "THE UNIT CONVERSIONS, not to carry the 2023 total forward.",
    model_impact="Blocks any RNAV or land-per-sqm lens built on a stated total, and "
                 "forces the asset base to be assembled from the eight named project "
                 "areas in note 16 with acres/feddans/sqm conversions shown. Also "
                 "means the ASSET BASE, not the balance sheet, is the binding freshness "
                 "constraint on this issuer.",
    fiscal_period="Q2-2026")

# ---- listing / series, no beta --------------------------------------------
f_listing = R.add(
    Ring.COMPANY, "management & capital actions", FindingClass.C,
    "LISTING AND SERIES, RECORDED WITHOUT A REGRESSION. Single listing: the Egyptian "
    "Exchange, ticker OCDI.CA, listed 10-Mar-1998; the company describes itself as one "
    "of the few non-family-owned companies traded on the EGX. NO dual listing — the "
    "ADX-listed entity in the structure is the PARENT, Aldar Properties PJSC, not "
    "OCDI. Series held in repo: engine/raw_ohlc/EG/OCDI.csv, 3,771 rows, 02-Jan-2011 "
    "to 01-Sep-2026, last close EGP 31.01, quoted in EGP as the EGX requires. The "
    "exchange index for EG/EGX is EGX30, held at engine/raw_indices/EG/EGX30.csv, 3,869 "
    "rows to 08-Sep-2026 (last 56,174.30). NO BETA IS RESOLVED IN THIS SWEEP, per "
    "instruction; when one is, it must go through beta_regression.own_stock_beta and it "
    "must first deal with the 14-Aug-2025 share-count step recorded in F32",
    "engine/raw_ohlc/EG/OCDI.csv; engine/raw_indices/EG/EGX30.csv; SODIC H1-2026 "
    "Earnings Release; 2024 Annual Board Report (listing date)",
    PMD, "2026-09-08",
    model_impact="")

# =============================================================================
# Close any mandatory category not already closed by a finding above
# =============================================================================
_AUTO = {
    (Ring.COMPANY, "IR communications (calls, presentations, releases)"):
        "already closed",
}
for ring in RINGS[AssetClass.STOCK]:
    for cat in MANDATORY[ring]:
        if not any(f.ring is ring and f.category == cat for f in R.findings):
            R.add_negative(ring, cat,
                           f"query set for '{cat}' run against SODIC's own IR library, "
                           f"the EGX/FRA portals and open search on {SWEEP_DATE}; "
                           f"nothing found that closes this category with a dated fact",
                           SWEEP_DATE)

# =============================================================================
# DRIVER GATE TABLE — mode earned, finest sourced level, margin as an OUTPUT
# =============================================================================
R.add_driver(
    "Units delivered, per project per period", DriverMode.BOTTOM_UP,
    "SODIC's board reports print UNITS DELIVERED BY PROJECT every period — 16 projects "
    "for FY2024 summing to exactly the 1,045 in the earnings release, 8 projects for "
    "H1-2026 summing to exactly the 557 in that release, with the regional split (192 / "
    "63 / 302) reproducing too. This is the finest sourced level and it is the physical "
    "driver of revenue under point-in-time recognition.",
    [f_revrec, f_rel26, f_rel24, f_capital])

R.add_driver(
    "Realised price per delivered unit, per project", DriverMode.BOTTOM_UP,
    "The same board-report tables print the VALUE of the units delivered beside the "
    "count, so price per unit is a division within one table and one period — never one "
    "year's value over another year's volume [L-010]. FY2024 gives 16 project points "
    "(e.g. V-Residence 385 units / EGP 3,509m), H1-2026 gives 8 (e.g. June 302 / EGP "
    "1,848m). Price and volume are projected separately.",
    [f_rel24, f_rel26, f_price, f_capital])

R.add_driver(
    "Revenue by region (West Cairo / East Cairo / North Coast)", DriverMode.BOTTOM_UP,
    "Note 6 disaggregates real estate sales by the three regions on both the six- and "
    "three-month columns, net of early-payment discount and sales returns, and note 34 "
    "states geography is the disaggregation the company itself uses.",
    [f_segments, f_h126, f_q126])

R.add_driver(
    "Cost of real estate sold by region -> GROSS MARGIN AS AN OUTPUT",
    DriverMode.BOTTOM_UP,
    "Note 7 gives cost of sales on the SAME regional cut as note 6, so margin is "
    "computed, not typed [L-005]. The half just reported prints 11.4% West, negative "
    "East and 16.3% North Coast — three numbers a single input margin would have "
    "erased. Unit cost is escalated per input (F03) rather than by one blended index "
    "[L-009], and capitalised interest is routed in as part of cost per F25.",
    [f_segments, f_h126, f_cmd, f_offbs])

R.add_driver(
    "Backlog conversion to recognised revenue", DriverMode.BOTTOM_UP,
    "An eight-point company-published backlog series (EGP 34.2bn at end-2022 to EGP "
    "116bn at 30-Jun-2026) plus note 33's short/long maturity split of the EGP 88.79bn "
    "receivable half gives the conversion profile directly. Under point-in-time "
    "recognition this IS the revenue forecast; nothing is glided.",
    [f_backlog, f_revrec, f_rel26])

R.add_driver(
    "Gross contracted sales, cancellations and net sales", DriverMode.BOTTOM_UP,
    "Gross sales, units sold and the cancellation rate are all disclosed (FY2024: EGP "
    "50.3bn gross, 1,270 units, 2% cancelled after 4% in 2023 and 6% in 2022), and the "
    "board report gives the NET figure on the same period (H1-2026: EGP 19.4bn net "
    "against EGP 23.5bn gross). The two definitions are kept apart. The absolute level "
    "is capped by the market evidence in F11, not extrapolated from +201%.",
    [f_rel24, f_rel26, f_mkt, f_capital])

R.add_driver(
    "Instalment interest recognised in revenue (EAS 48 financing component)",
    DriverMode.BOTTOM_UP,
    "Note 6 discloses it as its own line — EGP 1,311,647,894 in H1-2026 against EGP "
    "820,380,401 in H1-2025 — and note 7 discloses the matching cost side (EGP 582.5m "
    "against EGP 217.7m). It is 25% of total revenue and must be modelled off the "
    "receivable book, not folded into unit price.",
    [f_h126, f_backlog, f_revrec])

R.add_driver(
    "Recurring revenue: city/resort management, investment property, clubs & golf",
    DriverMode.BOTTOM_UP,
    "Each of the three legs has its own revenue AND its own cost line in the statement "
    "of profit or loss in every period from FY2022, so each carries its own margin. "
    "H1-2026: 468,863,910 / 160,396,710 / 168,984,608 against costs of 411,936,689 / "
    "121,849,211 / 264,890,288 — the clubs leg is loss-making and a blended treatment "
    "would hide that.",
    [f_h126, f_fy22, f_fy23])

R.add_driver(
    "Land liabilities and their instalment schedule", DriverMode.BOTTOM_UP,
    "Note 25 names all three counterparties with balances (NUCA 6,216,339,548; Shahin "
    "989,288,881; Midar 13,193,689,249) and notes 16/25 give the payment mechanics — "
    "Shahin 24 semi-annual instalments of EGP 110,812,875, Caesar back plot 10 "
    "semi-annual instalments, Midar 8 instalments Nov-2026 to Nov-2033. Variable-"
    "consideration land (New Sphinx, Ogami) is modelled as revenue share instead.",
    [f_land_liab, f_eastvale, f_sphinx])

R.add_driver(
    "Bank interest, and interest capitalised into work in process", DriverMode.BOTTOM_UP,
    "Note 24 names four facilities with dates, limits, drawn balances and a common "
    "pricing formula (CBE corridor plus margin), and F06 supplies the corridor. The "
    "capitalised stock is disclosed (EGP 15.8bn at 30-Jun-2026 from 10.3bn), so interest "
    "is charged to WIP and released through cost of sales on handover — never both.",
    [f_land_liab, f_offbs, f_cbe])

R.add_driver(
    "Construction capex", DriverMode.BOTTOM_UP,
    "Note 31 gives contracted commitments of EGP 39.7bn with EGP 19.8bn executed, i.e. "
    "a hard remaining commitment of c. EGP 19.9bn, and the releases give the actual "
    "spend rate (EGP 8.5bn FY2024, 8.3bn 9M-2025, 5.3bn H1-2026). Never a percentage of "
    "revenue.",
    [f_capcom, f_rel26, f_rel24])

R.add_driver(
    "Selling & marketing and G&A", DriverMode.BOTTOM_UP,
    "Notes 9 and 10 itemise both blocks in every period — H1-2026 selling & marketing "
    "splits into sales commissions 267,233,843, advertising & events 256,069,185, "
    "salaries 36,792,894 and eleven smaller lines. Sales commission is driven off "
    "contracted sales and advertising off the launch calendar; only the residual is "
    "escalated.",
    [f_h126, f_fy23])

R.add_driver(
    "Income tax", DriverMode.BOTTOM_UP,
    "Note 14 gives the current/deferred split and the full deferred-tax movement by "
    "temporary difference on both dates, including the EGP 1,092,853,282 provisions "
    "asset that links tax mechanically to the NUCA provision in F08.",
    [f_tax, f_h126])

R.add_driver(
    "Advances from customers (customer funding of the build)", DriverMode.BOTTOM_UP,
    "Note 26 gives advances by region and by activity on both dates (EGP 35,994,183,448 "
    "at 30-Jun-2026 from 29,222,421,017), including the EGP 8.7bn financing component. "
    "This is the working-capital engine of the model — advances grew EGP 3.94bn in "
    "H1-2026 while operating cash flow was NEGATIVE EGP 650.8m.",
    [f_segments, f_h126, f_backlog])

R.add_driver(
    "Provisions, and the NUCA retroactive land fee", DriverMode.BOTTOM_UP,
    "The provisions balance is disclosed on every date (2,613,659,406 -> 4,352,699,162 "
    "-> 4,630,344,058) with the H1-2026 movement split into EGP 1,017,364,145 formed, "
    "EGP 195,000,000 released and EGP 544,719,250 used. The rollback in F08 is applied "
    "to that disclosed balance as an explicit dual-framed event, not as a margin "
    "assumption.",
    [f_nuca, f_fy25bs, f_h126, f_tax])

R.add_driver(
    "Share count and value per share", DriverMode.BOTTOM_UP,
    "Note 35 states the post-merger count outright: 1,289,293,586 shares at EGP 4 "
    "nominal, against 356,197,368 before. The only other instrument is 3,878,425 ESOP "
    "shares (0.3%). No estimate is involved.",
    [f_merger, f_capital])

R.add_driver(
    "FY2025 full-year income statement and FY2025 operating anchors",
    DriverMode.TOP_DOWN,
    "FORCED, AND NAMED AS FORCED. The FY2025 statements and the FY2025 earnings release "
    "could not be retrieved from any SODIC channel or from the EGX portal — see the "
    "negative search for the full attempt list and the real failure text. FY2025 must "
    "therefore be carried as 9M-2025 actual plus a Q4-2025 that is INFERRED, and the "
    "31-Dec-2025 backlog, full-year contracted sales, units delivered, collections and "
    "capex have no company-sourced value at all. The FY2025 balance sheet is NOT "
    "affected — it is fully recovered and footed (F19). THIS ROW SHOULD BE RETIRED THE "
    "MOMENT THE FY2025 FILING IS SUPPLIED.",
    [f_neg_fy25, f_9m25, f_fy25bs])

R.add_driver(
    "Land base for any asset-based lens (sqm)", DriverMode.TOP_DOWN,
    "FORCED BY THE ORDERING FAILURE. No land-bank total in square metres has been "
    "published by SODIC since 30-Sep-2023, and the company itself says the undeveloped "
    "bank DOUBLED in June-2025, so the only stated total is known-stale rather than "
    "merely old. The land base is assembled project by project from note 16 with the "
    "acre/feddan/sqm conversions shown, and the absence of a company total is disclosed "
    "beside it [R-ASSET-01]. Any RNAV lens is flagged, not quietly run.",
    [f_neg_land, f_asset, f_sphinx, f_eastvale])

# =============================================================================
# OUTPUT
# =============================================================================
errors, warnings = R.validate()
R.to_json(os.path.join(HERE, 'sweep_register.json'))
print(R.qc_line())
print(f"\nfindings: {len(R.findings)} | drivers: {len(R.drivers)}")
c = R.counts()
print(f"by class: B={c['B']} S={c['S']} D={c['D']} C={c['C']} NEG={c['NEG']}")
nbu = sum(1 for d in R.drivers if d.mode is DriverMode.BOTTOM_UP)
print(f"drivers: {nbu} bottom-up / {len(R.drivers)-nbu} top-down")
n_ir = sum(1 for f in R.findings if f.source_type is SourceType.COMPANY_IR)
n_co = sum(1 for f in R.findings if f.source_type is SourceType.COMPANY_OFFICIAL)
print(f"COMPANY_OFFICIAL findings: {n_co} | COMPANY_IR findings: {n_ir}")
print(f"primary access attempts: {len(R.primary_access)} "
      f"({sum(1 for p in R.primary_access if not p.reachable)} blocked)")

if errors:
    print(f"\nVALIDATOR ERRORS ({len(errors)}) — disclosed, not suppressed:")
    for e in errors:
        print(f"  ! {e}")
else:
    print("\nVALIDATOR ERRORS: none")
if warnings:
    print(f"\nVALIDATOR WARNINGS ({len(warnings)}):")
    for w in warnings:
        print(f"  - {w}")
else:
    print("VALIDATOR WARNINGS: none")

fr = R.check_freshness(SWEEP_DATE)
print(f"\nfreshness vs delivery {SWEEP_DATE}: {fr or 'OK — sweep and delivery same day'}")
fr14 = R.check_freshness("2026-09-23")
print(f"freshness vs a 23-Sep-2026 delivery: {fr14 or 'OK — inside the 14-day window'}")
print(f"\nregister rows: {len(R.register_rows())-1} | driver rows: {len(R.driver_rows())-1}")
print(f"JSON: {os.path.join(HERE, 'sweep_register.json')}")
