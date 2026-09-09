"""CLHO (Cleopatra Hospitals Group, EGX:CLHO) — Step 2A four-ring Information Sweep.

Runs BEFORE any forecast driver is set. Every mandatory category of every ring is
closed by a dated finding or a dated negative search. Imports engine/research_sweep.py;
no study-local register is hand-rolled.

WRITTEN TO engine/clho_study_pending/ DELIBERATELY. `_pending` sits outside the
`engine/*_study` glob the repository gates walk, so a half-built study directory cannot
turn those gates red. Nothing here builds a valuation, a driver model or a document.

PRIMARY SOURCE ACCESS — the company's own IR channel was REACHED IN FULL.
https://www.cleopatrahospitals.com/en/investors/ returned HTTP 200 and carries the
complete document library: audited consolidated statements FY2016-FY2025, reviewed
interims through Q2-2026, earnings releases through H1-2026 (6 Sep 2026), IR
presentations through Q1-2026, conference-call materials and press releases. EVERY
financial-statement figure in this register was taken from that channel. No aggregator,
broker or press report is the source of any CLHO-reported historical figure.
The subdomain https://ir.cleopatrahospitals.com/ is NOT reachable (curl 56, CONNECT
tunnel failed, response 502) and https://www.cleopatrahospitals.com/investor-relations/
returns 404 — both are logged rather than passed over, because the working path is
/en/investors/ and a later run that guesses the other two will conclude the IR channel
is down when it is not.

BLOCKED HOSTS, with the real failure text, all logged via record_primary_access:
  egx.com.eg              curl (52) Empty reply from server  — every path, incl. the
                          /downloads/ PDFs that mirror CLHO's own releases
  fra.gov.eg              curl (35) Recv failure: Connection reset by peer
  uhia.gov.eg             curl (60) SSL certificate problem: unable to get local
                          issuer certificate
  cbe.org.eg (rates page) HTTP 200 carrying a WAF interstitial: "Request Rejected —
                          The requested URL was rejected. Please consult with your
                          administrator."
[R-SIGCM-03] fallback applied ONLY where it is permitted: for the exchange filings the
company's OWN documents, retrieved direct from cleopatrahospitals.com, are the named
fallback for the unreachable EGX mirror — they are the same documents. Where a figure
is NOT a CLHO-reported figure (CBE policy rate, CAPMAS inflation, competitor beds) a
non-company source is used and is tagged as such; no aggregator is the source of any
CLHO historical.

SCANNED-FILING HANDLING. The Q1-2026 reviewed interim (chc-consolidated-fs-31-march-
2026.pdf) has NO text layer at all — 31 pages, 0 extractable characters. Its statements
were rendered at 250 dpi and read off the pixels. In every FY filing FY2022-FY2025 the
consolidated statement of financial position is likewise an image inside an otherwise
text-bearing PDF and was read the same way. Every column so read was RE-ADDED against
the filing's own printed subtotals; all footed. Two routes disagreed once and the
disagreement is recorded in F31 (capitalised interest: a 250-dpi visual read gave
837,680,937, the text layer gave 837,689,037; a 600-dpi re-render of that single line
settled it in favour of 837,689,037, and an implied-interest-rate check on average debt
independently agrees). One printed row does NOT foot and is recorded rather than
silently corrected — F27.

NOT DONE HERE, DELIBERATELY: no beta is resolved. The exchange, the listing and the
price series that exists are recorded in F62; the regressor ruling is not this sweep's
to take.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))

from research_sweep import (SweepRegister, AssetClass, Ring, FindingClass,   # noqa: E402
                           SourceType, DriverMode)

SWEEP_DATE = "2026-09-09"
R = SweepRegister("CLHO", AssetClass.STOCK, SWEEP_DATE)

CO = SourceType.COMPANY_OFFICIAL
IR = SourceType.COMPANY_IR
REG = SourceType.REGULATOR_OFFICIAL
PMD = SourceType.PRIMARY_MARKET_DATA
PRESS = SourceType.REPUTABLE_PRESS

IRBASE = "https://www.cleopatrahospitals.com"

# ---------------------------------------------------------------------------
# PRIMARY ACCESS LOG — logged whether it succeeded or was blocked
# ---------------------------------------------------------------------------
R.record_primary_access(
    "https://www.cleopatrahospitals.com/", True, "2026-09-09",
    "HTTP 200. Corporate site reachable; the only IR link on the homepage is /en/investors/.")
R.record_primary_access(
    "https://www.cleopatrahospitals.com/en/investors/", True, "2026-09-09",
    "HTTP 200, 380,418 bytes. THE working IR path. Complete library: audited consolidated "
    "and standalone statements FY2016-FY2025 (EN and AR), reviewed interims to Q2-2026, "
    "earnings releases 1Q2016-H1 2026, IR presentations 2Q2016-Q1 2026, results-call "
    "materials, sustainability reports and press releases. Every CLHO figure in this "
    "register came from here.")
R.record_primary_access(
    "https://ir.cleopatrahospitals.com/", False, "2026-09-09",
    "curl (56) CONNECT tunnel failed, response 502. No IR subdomain exists; logged so a "
    "later run does not read this as the IR channel being down.")
R.record_primary_access(
    "https://www.cleopatrahospitals.com/investor-relations/", False, "2026-09-09",
    "HTTP 404. The guessable English IR path is wrong; the live one is /en/investors/.")
R.record_primary_access(
    "https://www.egx.com.eg/en/homepage.aspx", False, "2026-09-09",
    "curl (52) Empty reply from server. EGX is unreachable on every path tried, including "
    "https://www.egx.com.eg/downloads/Bulletins/335381_2.pdf and "
    "https://www.egx.com.eg/downloads/News/188896_091217.pdf, which mirror CLHO's own FY2025 "
    "and 1Q2026 releases. [R-SIGCM-03] fallback: those same documents were taken direct from "
    "cleopatrahospitals.com. No aggregator was substituted.")
R.record_primary_access(
    "https://fra.gov.eg/en/", False, "2026-09-09",
    "curl (35) Recv failure: Connection reset by peer. The Financial Regulatory Authority "
    "portal could not be reached, so the FRA file on the Cairo Specialized Hospital "
    "57%->90% transaction (F58) could not be inspected at source.")
R.record_primary_access(
    "https://www.cbe.org.eg/en/economic-research/statistics/cbe-rates", False, "2026-09-09",
    "HTTP 200 but the body is a WAF interstitial: '<html><head><title>Request Rejected"
    "</title></head><body>The requested URL was rejected. Please consult with your "
    "administrator.<br/><br/>Your support ID is 5ba6fa76-7a3b-4be4-ab7b-bb039ef7b3e0'. "
    "The CBE policy rate in F06 is therefore relayed, not read at source.")
R.record_primary_access(
    "https://uhia.gov.eg/", False, "2026-09-09",
    "curl (60) SSL certificate problem: unable to get local issuer certificate. The "
    "Universal Health Insurance Authority's own site could not be verified; UHIA rollout "
    "figures in F09 are relayed.")
R.record_primary_access(
    "https://www.capmas.gov.eg/", True, "2026-09-09",
    "HTTP 200 but only 1,421 bytes — a JS shell, no statistics served to a plain client. "
    "The CAPMAS inflation print in F07 is relayed rather than read from the release.")

# ---------------------------------------------------------------------------
# STUDY YEAR
# ---------------------------------------------------------------------------
R.declare_study_year("2026", ["Q1-2026", "Q2-2026"])

# ===========================================================================
# RING 1 — GLOBAL
# ===========================================================================
f_fed = R.add(
    Ring.GLOBAL, "rate cycle & USD/FX regime", FindingClass.S,
    "US federal funds target range 3.50-3.75%, effective 29 Jul 2026; three FOMC members "
    "dissented for a 25bp HIKE and the 15-16 Sep 2026 meeting is live in both directions",
    "Federal Reserve Board, FOMC statement 17 Jun 2026 and minutes of the 28-29 Jul 2026 meeting",
    REG, "2026-07-29",
    url="https://www.federalreserve.gov/monetarypolicy/fomcminutes20260729.htm",
    model_impact="Sets the global anchor under which Egypt's own easing path is assumed. "
                 "CLHO's entire debt book prices off the CBE lending rate (F35), so the "
                 "direction of the terminal risk-free rate and the Kd glide inherits from "
                 "this. A US HIKE, which is live, is the adverse case for the EGP and for "
                 "the assumed CBE cuts — the WACC glide must be sensitised UPWARD, not only "
                 "down.")

f_fx = R.add(
    Ring.GLOBAL, "rate cycle & USD/FX regime", FindingClass.C,
    "USD/EGP ~50.95 on 7 Sep 2026 (50.9515 on 4 Sep), broadly flat through 2026 after the "
    "2024 devaluation",
    "USD/EGP spot series", PMD, "2026-09-07",
    detail="Recorded for the FX-regime category. CLHO's functional and presentation currency "
           "is EGP for the parent and every subsidiary (Q2-2026 reviewed statements, note 2.2), "
           "and its debt book is 100% EGP, so there is no direct translation exposure. The "
           "exposure is indirect, through imported medical supplies and equipment — see F03.",
    model_impact="")

f_supp = R.add(
    Ring.GLOBAL, "commodity complex (input/output)", FindingClass.S,
    "Medical and pharmaceutical supplies are CLHO's single largest cost line — EGP "
    "1,650,595,778 in FY2025, 37.8% of cost of revenue and 22.8% of revenue — and Egypt "
    "imports c.USD 2.94bn of pharmaceutical product a year; on 8 Sep 2026 the government "
    "overhauled drug pricing with an FX band, a smaller reference basket and a local-"
    "production advantage",
    "CLHO FY2025 audited consolidated statements note 26 (cost figure); Egyptian drug-pricing "
    "reform and pharmaceutical import bill (external)", PRESS, "2026-09-08",
    detail="The cost figure is company-official and audited; the pricing-reform and import-bill "
           "context is external and is what makes this a GLOBAL-ring finding rather than a "
           "company one. The reform landed one day before this sweep and its pass-through to "
           "hospital consumable cost is not yet observable.",
    model_impact="Medical-supplies cost per case is the largest single input in the cost-per-"
                 "unit build. The FX band caps the devaluation channel into consumable cost but "
                 "does not remove it. Build medical supplies as EGP per case with an explicit "
                 "inflation path, never as a fixed percentage of revenue — CLHO's own quarterly "
                 "disclosure already moves it (21.5% of sales in Q1-2026 to 21.2% in Q2-2026).")

f_medtour = R.add(
    Ring.GLOBAL, "global sector demand", FindingClass.C,
    "Egypt inbound medical tourism is real but immaterial at CLHO's scale: c.USD 10mn of "
    "revenue and c.42,000 international patients across General Authority for Healthcare "
    "hospitals to Aug-2026 (+37% y/y), against a national 2030 target of 200,000 patients a year",
    "Egyptian State Information Service and Egyptian press coverage of GAH medical-tourism "
    "revenue", PRESS, "2026-08-19",
    detail="USD 10mn is c.EGP 510mn at 50.95, i.e. c.7% of CLHO's FY2025 revenue — and that is "
           "the whole GAH public-sector figure, not CLHO's share. CLHO markets medical tourism "
           "(a /en/medicaltourism/ page and a stated medical-value-tourism ambition for Cleopatra "
           "October) but discloses NO medical-tourism revenue line. See the negative search F49.",
    model_impact="")

f_iran = R.add(
    Ring.GLOBAL, "trade / sanctions / supply chains", FindingClass.S,
    "CLHO's OWN reviewed statements carry a subsequent-events note on the 28 Feb 2026 direct "
    "military confrontation between the United States and Israel and Iran, with engagements "
    "involving certain Gulf countries, which management says is expected to have a significant "
    "economic impact on the Middle East region",
    "CLHO interim condensed consolidated financial statements for the six months ended 30 June "
    "2026, note 21.3 'Impact of Military Conflict'", CO, "2026-09-03",
    url=f"{IRBASE}/media/lu2hhgwg/chc-consolidated-fs-30-june-2026.pdf",
    detail="Quantified nowhere. Management states it is monitoring. Egyptian press separately "
           "attributes higher fuel, electricity and shipping costs partly to 'Iran-war fallout'. "
           "This is the only geopolitical item CLHO itself has put in a filing.",
    model_impact="An unquantified downside on the import-cost line (F03) and on the Egyptian "
                 "macro path (F06, F07). Carry it as a named scenario in the sensitivity grid — "
                 "supply-chain cost shock plus a slower CBE easing path — not as a haircut to "
                 "the central case.")

# ===========================================================================
# RING 2 — COUNTRY
# ===========================================================================
f_cbe = R.add(
    Ring.COUNTRY, "sovereign macro (inflation, policy rate, FX/deval risk)", FindingClass.D,
    "CBE held policy rates on 20 Aug 2026 for the fourth consecutive meeting: overnight "
    "deposit 19.00%, overnight LENDING 20.00%. The last move was a 100bp cut in Feb-2026",
    "Central Bank of Egypt MPC decision 20 Aug 2026, relayed by Egyptian State Information "
    "Service and EnterpriseAM after cbe.org.eg refused the request at source",
    PRESS, "2026-08-20",
    detail="cbe.org.eg returned a WAF 'Request Rejected' interstitial (logged in the primary-"
           "access record), so this is relayed rather than read at source. It is NOT a CLHO "
           "figure, so no aggregator rule is breached. THE LENDING RATE IS THE ONE THAT MATTERS "
           "HERE, not the deposit rate: every CLHO facility is contractually priced off 'the "
           "lending rate announced by the Central Bank of Egypt' (F35).",
    model_impact="DRIVER UNLOCK. Kd is not estimated: it is 20.00% + the contractual margin, "
                 "5bp to 80bp depending on facility (F35). The explicit-window risk-free rate "
                 "and the Kd glide both key off the published CBE path, and the terminal rf is "
                 "norm-built off the CBE's own medium-term inflation target, never averaged "
                 "from history.")

f_cpi = R.add(
    Ring.COUNTRY, "sovereign macro (inflation, policy rate, FX/deval risk)", FindingClass.S,
    "Egypt annual urban inflation ACCELERATED to 14.9% in July 2026 from 14.3% in June — the "
    "first re-acceleration since March — on housing, transport and education; all-Egypt "
    "headline 13.0% vs 12.2%",
    "CAPMAS July 2026 CPI release, relayed by Egyptian and international press after "
    "capmas.gov.eg served no data to a plain client", PRESS, "2026-08-10",
    detail="This is why the CBE has held four times. It bears directly on CLHO because CLHO's "
           "revenue growth is explicitly built on 'the annual strategic price adjustment "
           "implemented at the start of the year' (F14) — a once-a-year price reset against a "
           "cost base that reprices continuously.",
    model_impact="Sets the ceiling on the average-revenue-per-case (ARP) growth path and the "
                 "floor under the cost-per-case path. Model ARP growth and cost inflation as "
                 "SEPARATE series with a within-year timing lag; do not net them into a margin "
                 "assumption.")

f_uhia = R.add(
    Ring.COUNTRY, "regulatory environment (regulator, caps, tariffs, tax/subsidy)", FindingClass.S,
    "Universal Health Insurance is scaling: Phase 1 covers six governorates (Port Said, "
    "Ismailia, Luxor, Suez, South Sinai, Aswan) with 5.2mn beneficiaries at an 82% registration "
    "rate as of Mar-2026; Phase 2 adds five governorates against a Cabinet target of 12-13mn "
    "more. The UHIA has contracted 526 providers, of which the PRIVATE sector is 32% of the "
    "network, and private providers are expected to supply 30-40% of hospital beds. GAHAR "
    "accreditation is a precondition of contracting",
    "Egyptian Universal Health Insurance Authority programme reporting and Egyptian press "
    "(EnterpriseAM, Mada Masr, Egypt Today) after uhia.gov.eg failed TLS verification",
    PRESS, "2026-08-11",
    detail="SUEZ IS A PHASE-1 GOVERNORATE and CLHO operates there: the Suez Polyclinic and Suez "
           "Cath Lab, and the 15-year Petroleum-sector Medical Center agreement (F20), feed "
           "Cairo Specialized Hospital. CLHO does not disclose whether any facility is "
           "GAHAR-accredited or UHIA-contracted — see the negative search F50.",
    model_impact="Two-sided and unresolved. Upside: a contracted payer with 12-18mn covered "
                 "lives is a volume channel CLHO's payer-mix disclosure is silent on. Downside: "
                 "UHIA is a TARIFF-SETTING payer, so mix-shift toward it compresses ARP. Because "
                 "CLHO discloses no payer mix (F48), this cannot be modelled bottom-up and must "
                 "be a named scenario on the ARP driver, stated as unquantifiable from disclosure.")

f_tax = R.add(
    Ring.COUNTRY, "regulatory environment (regulator, caps, tariffs, tax/subsidy)", FindingClass.D,
    "CLHO's EFFECTIVE tax rate is well above Egypt's 22.5% statutory rate and is RISING: "
    "20.7% FY2022, 22.3% FY2023, 24.6% FY2024, 26.6% FY2025, 30.1% H1-2026, computed from the "
    "audited and reviewed current-plus-deferred tax charge over profit before tax",
    "CLHO audited consolidated statements FY2022-FY2025 and reviewed interim to 30 June 2026, "
    "statements of profit or loss", CO, "2026-09-03",
    detail="FY2025: (383,914,976 current less 32,681,909 deferred credit) / 1,319,099,384 = 26.6%. "
           "H1-2026: (160,012,466 less 12,535,900) / 489,515,277 = 30.1%. The widening gap tracks "
           "the growth of items that are unlikely to be deductible — the LTIP mark-to-market "
           "charge (F55) and CTH pre-operating costs (F53).",
    is_fs_data=True, fiscal_period="FY2025",
    model_impact="Tax is a BUILT driver, not the 22.5% statutory rate. Build it as statutory rate "
                 "on taxable profit plus an explicit non-deductible add-back keyed to the LTIP and "
                 "pre-operating lines, and show the effective rate the model produces against the "
                 "20.7%-30.1% realised range. A model that runs 22.5% overstates after-tax cash by "
                 "roughly 5-10% of profit before tax at the current run-rate.")

f_ppp = R.add(
    Ring.COUNTRY, "fiscal / political events with sector read-through", FindingClass.S,
    "The Egyptian state is putting a large hospital pipeline into private hands: in Feb-2026 the "
    "Health Ministry and the Sovereign Fund of Egypt widened the offering from 7 to 62 healthcare "
    "projects for private management and operation; in Aug-2026 the Prime Minister reviewed two "
    "integrated medical cities (New Administrative Capital c.USD 2.8bn, New Alamein c.USD 2.5bn); "
    "in Jul-2026 a 4,200-bed integrated medical complex in Cairo was explored under PPP",
    "EnterpriseAM Egypt (23 Feb 2026), Business Today Egypt / AGBI, HealthCare Middle East & "
    "Africa (30 Jul 2026)", PRESS, "2026-07-30",
    detail="This is the same asset-light, operate-someone-else's-building model CLHO already runs "
           "at Cleopatra October (F39) and Cleopatra El Tagamoa (F38) and named in the H1-2026 "
           "release as its stated preference. It is simultaneously CLHO's pipeline and its "
           "competitors' — Alameda signed exactly such a PPP with the Egyptian Atomic Energy "
           "Authority in Apr-2026 (F16).",
    model_impact="Sets the credibility of the post-2028 growth leg. CLHO's disclosed capacity "
                 "pipeline stops at the 200-bed Cleopatra October extension for 2027-28 (F52); "
                 "anything beyond that is unnamed and unsigned. Model the explicit window on "
                 "NAMED, CONTRACTED capacity only and put unnamed pipeline in the terminal "
                 "growth rate, dual-framed.")

# ===========================================================================
# RING 3 — INDUSTRY
# ===========================================================================
f_beds = R.add(
    Ring.INDUSTRY, "demand drivers & capacity/supply balance", FindingClass.S,
    "Egypt is structurally short of beds and the private sector already carries most of them: "
    "CLHO's own FY2025 IR presentation states the private sector is 45.1% of Egypt's beds and "
    "46.3% of its hospitals, that Egypt sits below regional benchmarks on beds per 1,000 "
    "population, and that Egypt requires c.38,000 new beds on a 1.3 beds/1,000 ratio; the "
    "private market is highly fragmented at an average 31 beds per hospital",
    "CLHO FY2025 Investor Presentation, market-context section", IR, "2026-03-17",
    url=f"{IRBASE}/media/qcxjlaq4/chg-irp-fy2025.pdf",
    detail="Company-sourced market context, tagged COMPANY_IR rather than COMPANY_OFFICIAL "
           "because it is the company's characterisation of its market, not an audited figure. "
           "Independent reporting puts the 38,000-bed requirement at a USD 8-13bn investment need "
           "by 2030, which is consistent.",
    model_impact="Supports a demand-led occupancy ramp on new beds rather than a price-led one, "
                 "and is the reason the volume leg of the build can be run at capacity-times-"
                 "utilisation rather than at a market-share assumption. Fragmentation at 31 beds "
                 "per hospital is also the argument for the consolidation optionality that the "
                 "study must NOT capitalise into the central case.")

f_price = R.add(
    Ring.INDUSTRY, "pricing", FindingClass.D,
    "CLHO prices on an ANNUAL reset, and discloses the realised per-segment ARP moves. H1-2026 "
    "vs H1-2025 average revenue per unit: surgical procedure EGP 29,720 -> 34,517 (+16.1%); "
    "inpatient EGP 22,818 -> 25,389 (+11.3%); paid consultation EGP 520 -> 544 (+4.6%); ER visit "
    "EGP 1,310 -> 1,505 (+14.9%); catheterisation EGP 78,574 -> 85,522 (+8.8%). Physiotherapy ARP "
    "rose 63% in H1 and 66% in Q2, the largest of any segment, with growth 'driven by pricing "
    "rather than volumes'",
    "CLHO H1 2026 Earnings Release, KPI panel and Revenue Breakdown by Segment", IR, "2026-09-06",
    url=f"{IRBASE}/media/sufdt2ur/cleopatra-earnings-release-2q2026.pdf",
    fiscal_period="Q2-2026",
    detail="ARITHMETIC CHECK PASSED: each disclosed segment revenue growth reproduces from the "
           "disclosed volume growth times the disclosed ARP growth. Surgeries 1.0485 x 1.1614 = "
           "1.218 vs the release's stated +22%; inpatients 1.1471 x 1.1127 = 1.276 vs +28%; "
           "outpatient 1.1383 x 1.046 = 1.191 vs +19%; ER 1.0818 x 1.1489 = 1.243 vs +24%. The "
           "volume-times-price grid is internally consistent and is safe to build on.",
    model_impact="DRIVER UNLOCK, and the reason revenue is built bottom-up as volume x ARP per "
                 "service line rather than as a growth rate. ARP is projected per line against "
                 "the inflation path in F07; the annual-reset mechanic means the price step lands "
                 "in Q1 of each year, not evenly.")

f_alameda = R.add(
    Ring.INDUSTRY, "new entrants (named-competitor level)", FindingClass.S,
    "Alameda Healthcare is the named competitor that changed in the study window: Development "
    "Partners International COMPLETED a USD 190mn investment in Feb-2026, the largest healthcare "
    "investment of its kind in Egypt. Alameda runs 1,023 beds and 128 clinics across four Greater "
    "Cairo facilities including the JCI-accredited As-Salam International and Dar Al Fouad, "
    "signed a multi-year partnership with Houston Methodist in Jan-2026 centred on Madinaty "
    "Hospital in NEW CAIRO, a PPP with the Egyptian Atomic Energy Authority in Apr-2026, and is "
    "taking its specialised-clinic network from seven to nine sites by end-2026",
    "Development Partners International completion announcement (19 Feb 2026); Alameda Healthcare "
    "corporate announcements; HealthCare Middle East & Africa (1 Sep 2026)",
    PRESS, "2026-09-01",
    detail="MADINATY AND NEW CAIRO ARE CLEOPATRA EL TAGAMOA'S CATCHMENT. CTH launched 27 Jan 2026 "
           "into East Cairo and its ramp (F53) is the single largest swing factor in the forecast. "
           "Alameda at 1,023 beds is larger than CLHO's 780 operating beds at end-2025 (F51), "
           "which qualifies CLHO's own 'largest private hospital group in Egypt by number of beds' "
           "claim — the claim is about hospitals plus beds across a 7-hospital network, and both "
           "definitions should be stated wherever the claim is repeated.",
    model_impact="Caps the CTH occupancy ramp and the ARP path in East Cairo. The bull case for "
                 "CTH (management's 'ahead of expectations', EGP 1.2bn annualised, F54) must be "
                 "run against a named, funded, JCI-accredited competitor adding capacity into the "
                 "same catchment in the same year. Sensitise the CTH ramp, do not extrapolate it.")

f_tech = R.add(
    Ring.INDUSTRY, "technology substitution", FindingClass.C,
    "Egypt's digital-health build-out is real but is not substituting for acute inpatient, "
    "surgical or catheterisation capacity inside the forecast window: the AI-in-healthcare-"
    "diagnostics market is c.USD 31mn, telemedicine runs through c.200 Distance Medical Diagnosis "
    "Units, and the digitisation under UHIS is of family-medicine centres, labs, radiology and "
    "outpatient clinics",
    "Ken Research Egypt AI in Healthcare Diagnostics and Telemedicine market coverage; Egyptian "
    "State Information Service; Middle East Observer (6 Aug 2026)", PRESS, "2026-08-06",
    detail="The exposed lines are the LOW-ARP ones — outpatient consultations at EGP 544 per visit "
           "and diagnostics — not the EGP 34,517-per-procedure surgical line or the EGP 25,389-"
           "per-case inpatient line that together are 41% of revenue. Outpatient clinics were 9% "
           "of FY2025 revenue and laboratories 11%.",
    model_impact="")

f_peers = R.add(
    Ring.INDUSTRY, "competitor capacity / price moves (named)", FindingClass.S,
    "Named private-hospital capacity moving in Egypt beyond Alameda: Andalusia Group (Egyptian "
    "holding owned by the Saudi Zagzoug family) operates three tertiary hospitals at 229 beds and "
    "is expanding to 445; Saudi German Hospitals Group operates in Egypt as part of a ten-hospital "
    "MENA network; Emirates Healthcare Group has announced an expansion into Egypt",
    "Andalusia Group corporate disclosure and African Development Bank project documentation; "
    "Saudi German Hospitals Group corporate site; Global Growth Markets", PRESS, "2026-08-19",
    detail="Andalusia's 229 -> 445 beds is a +216-bed addition, on the same order as CLHO's own "
           "+270 for 2026. Aggregate named private additions in Egypt over 2026-2028 from Alameda, "
           "Andalusia and the 62-project PPP pipeline (F11) are large relative to CLHO's +440.",
    model_impact="Bounds the market-share assumption implicit in the volume ramp. Every bed CLHO "
                 "adds is being added against a named set of competing additions, so the "
                 "utilisation path on new beds is set BELOW the mature-network utilisation of the "
                 "existing hospitals, and the gap is stated rather than assumed away.")

# ===========================================================================
# RING 4 — COMPANY : official financial statements
# ===========================================================================
f_fy22 = R.add(
    Ring.COMPANY, "official financial statements", FindingClass.D,
    "FY2022 audited consolidated statements, signed Cairo 16 March 2023. Revenue EGP "
    "2,614,421,170; cost of revenue 1,741,106,085; gross profit 873,315,085 (33.4%); operating "
    "profit 448,342,196; profit before tax 449,665,198; net profit 356,731,839; attributable "
    "325,762,928; NCI 30,968,911; EPS 0.17. Total assets 3,283,368,957; total equity 2,027,350,565; "
    "total liabilities 1,256,018,392. Signed by Ahmed Adel Badreldin (Chairman), Dr Ahmed Ezz "
    "Eldin Mahmoud (CEO) and Ahmed Gamal (Group CFO)",
    "CLEOPATRA HOSPITAL COMPANY 'S.A.E.' AND ITS SUBSIDIARIES, consolidated financial statements "
    "for the year ended 31 December 2022", CO, "2023-03-16",
    url=f"{IRBASE}/media/kuah450j/chg-cons-fy2022.pdf",
    is_fs_data=True, fiscal_period="FY2022",
    detail="ROUTE: profit-or-loss read from the PDF text layer; statement of financial position is "
           "an IMAGE (PDF page 5 carries zero extractable characters) and was rendered at 400 dpi "
           "and read off the pixels. BOTH re-added against the filing's own printed subtotals and "
           "both foot exactly, in every column and both years.",
    model_impact="First of four historical years. FY2022 is the pre-expansion baseline: gross "
                 "margin 33.4%, no CTH, Cleopatra October only two months old.")

f_fy23 = R.add(
    Ring.COMPANY, "official financial statements", FindingClass.D,
    "FY2023 audited consolidated statements, signed Cairo 14 March 2024. Revenue EGP "
    "3,595,299,364; cost 2,386,677,071; gross profit 1,208,622,293 (33.6%); operating profit "
    "650,841,324; net profit 469,299,689 after a 4,262,386 loss from discontinued operations; "
    "attributable 418,180,515; EPS 0.22. Total assets 4,488,027,205; total equity 2,446,250,009. "
    "CFO now Adel Elmistikawi",
    "CLEOPATRA HOSPITAL COMPANY 'S.A.E.', consolidated financial statements for the financial year "
    "ended 31 December 2023", CO, "2024-03-14",
    url=f"{IRBASE}/media/xfujfe55/m-cleopatra-cons-dec-23.pdf",
    is_fs_data=True, fiscal_period="FY2023",
    detail="ROUTE: same split — P&L from the text layer, balance sheet from 400-dpi pixels. Both "
           "columns re-added; every subtotal foots.",
    model_impact="Second historical year. Confirms the pre-expansion gross margin plateau at "
                 "c.33.5% before it steps up in FY2024-25.")

f_fy24 = R.add(
    Ring.COMPANY, "official financial statements", FindingClass.D,
    "FY2024 audited consolidated statements, signed 20 March 2025. Revenue EGP 5,420,396,411 "
    "(+50.8%); cost 3,407,053,062; gross profit 2,013,343,349 (37.1%); operating profit "
    "1,162,776,858; profit before tax 1,083,665,759; net profit 817,011,989; attributable "
    "723,346,615; NCI 93,665,374; EPS 0.39. Total assets 7,589,752,547; equity 3,177,797,400; "
    "total liabilities 4,411,955,147. CFO Adel Al-Mestakawi",
    "CLEOPATRA HOSPITAL COMPANY 'S.A.E.', consolidated financial statements for the financial year "
    "ended 31 December 2024", CO, "2025-03-20",
    url=f"{IRBASE}/media/sqjd44yj/chc-consolidated-fs-31-dec-2024.pdf",
    is_fs_data=True, fiscal_period="FY2024",
    detail="ROUTE: P&L text layer, balance sheet 400-dpi pixels; all columns re-added and foot. "
           "The FY2023 comparative column reproduces the FY2023 filing exactly, line for line — no "
           "restatement between those two years.",
    model_impact="Third historical year and the margin inflection: gross margin steps from 33.6% "
                 "to 37.1% on a 51% revenue rise, which is the operating-leverage evidence the "
                 "forward margin path is anchored to.")

f_fy25 = R.add(
    Ring.COMPANY, "official financial statements", FindingClass.D,
    "FY2025 audited consolidated statements, signed 16 March 2026. Revenue EGP 7,227,264,460 "
    "(+33.3%); cost 4,368,794,593; gross profit 2,858,469,867 (39.6%); operating profit "
    "1,490,050,629; finance income 46,632,479, finance EXPENSE 227,319,411; equity-method income "
    "10,065,687; profit before tax 1,319,099,384; net profit 967,866,317; attributable 823,881,689; "
    "NCI 143,984,628; EPS 0.46. Total assets 10,241,259,285; equity 4,040,365,543 (attributable "
    "3,622,337,333, NCI 418,028,210); total liabilities 6,200,893,742. CFO now Amr Al Rashid",
    "CLEOPATRA HOSPITAL COMPANY 'S.A.E.', consolidated financial statements for the financial year "
    "ended 31 December 2025", CO, "2026-03-16",
    url=f"{IRBASE}/media/pj0ldhq3/chc-consolidated-31-dec-2025.pdf",
    is_fs_data=True, fiscal_period="FY2025",
    detail="ROUTE: P&L text layer, balance sheet 400-dpi pixels. Re-added in full: non-current "
           "assets 7,877,933,359, current 2,363,325,926, total 10,241,259,285 = total equity and "
           "liabilities; every subtotal foots to the pound on both the 2025 and 2024 columns. Note "
           "the text layer renders some negatives as ')n(' and some 2024 figures with dot "
           "thousands separators (e.g. '749.796.569'); those are RTL/typography artefacts, not "
           "glyph errors — each was re-added and each is correct.",
    model_impact="The base year. Every driver level is struck here and rolled forward on the "
                 "physical grid.")

f_restate22 = R.add(
    Ring.COMPANY, "official financial statements", FindingClass.S,
    "FY2022 IS RESTATED in the FY2023 comparatives and a build that mixes the two gets the FY22-23 "
    "growth rate wrong. As filed FY2022 revenue was EGP 2,614,421,170; the FY2023 filing's FY2022 "
    "comparative is EGP 2,584,032,374, EGP 30,388,796 lower, with a matching 'discontinued "
    "operations' line of (1,501,962). Net profit is IDENTICAL on both presentations at "
    "356,731,839. Total assets are also restated: 3,283,368,957 as filed vs 3,264,343,210, an "
    "EGP 19,025,747 offset of a receivable against a payable with equity unchanged",
    "CLHO FY2022 audited statements compared line-by-line with the FY2022 comparative column of the "
    "FY2023 audited statements", CO, "2024-03-14",
    url=f"{IRBASE}/media/xfujfe55/m-cleopatra-cons-dec-23.pdf",
    is_fs_data=True, fiscal_period="FY2022",
    detail="Arithmetic settles it in both directions: 2,584,032,374 + 30,388,796 = 2,614,421,170; "
           "trade receivables 505,356,134 as filed less 486,330,387 restated = 19,025,747 = trade "
           "payables 530,750,517 less 511,724,770 = the exact total-asset difference. BOTH "
           "presentations foot internally. Separately, CLHO's own FY2023 earnings release "
           "quarterly table (1Q22 637 + 2Q22 605 + 3Q22 661 + 4Q22 712 = EGP 2,615mn) ties to the "
           "AS-FILED basis, not the restated one.",
    model_impact="Pick ONE basis for the FY2022 revenue base and say which. Growth FY22->FY23 is "
                 "+39.1% on the restated base and +37.5% on the as-filed base. The volume/ARP grid "
                 "in F47 is on the as-filed basis, so the physical build must use as-filed FY2022 "
                 "or restate the grid.")

f_reclass24 = R.add(
    Ring.COMPANY, "official financial statements", FindingClass.S,
    "FY2024 OPERATING PROFIT has two different published values and neither is wrong. As filed: "
    "EGP 1,162,776,858, with equity-method income inside 'other revenues' (22,349,269) and "
    "acquisition consulting expense above the operating line. As restated in the FY2025 "
    "comparative: EGP 1,158,972,725, with equity-method income shown separately (4,709,037), other "
    "revenues reduced to 17,640,232 and consulting expense moved below operating profit. Net "
    "profit is identical at 817,011,989",
    "CLHO FY2024 audited statements compared with the FY2024 comparative column of the FY2025 "
    "audited statements", CO, "2026-03-16",
    url=f"{IRBASE}/media/pj0ldhq3/chc-consolidated-31-dec-2025.pdf",
    is_fs_data=True, fiscal_period="FY2024",
    detail="22,349,269 less 17,640,232 = 4,709,037, exactly the equity-method line; the operating-"
           "profit difference of 3,804,133 = 4,709,037 less 904,904 consulting. A pure "
           "presentation reclass, verified by arithmetic.",
    model_impact="Any FY2024 EBIT or EBITDA margin quoted in the study must name which "
                 "presentation. On the FY2025-comparative basis the FY2024 operating margin is "
                 "21.4%; on the as-filed basis 21.5%.")

f_revnote = R.add(
    Ring.COMPANY, "official financial statements", FindingClass.D,
    "THE AUDITED REVENUE NOTE IS THE FINEST SOURCED LEVEL AND IT COVERS FOUR YEARS. Fifteen "
    "service lines, FY2025 / FY2024: residency and medical supervision (inpatient) 1,583,244,138 / "
    "1,233,265,771; surgeries 1,359,734,909 / 1,100,684,402; laboratories 786,970,168 / "
    "509,020,271; outpatient clinics 667,565,609 / 497,640,710; service charge 542,606,995 / "
    "439,045,444; radiology 525,213,413 / 335,664,111; pharmacy 501,505,451 / 346,628,992; cardiac "
    "catheterisation 467,408,288 / 391,893,335; emergency 266,014,679 / 182,107,126; physiotherapy "
    "209,706,872 / 148,698,126; cardiac tests 74,604,038 / 47,422,252; fluoroscopes 68,327,960 / "
    "49,903,335; oncology 56,223,486 / 37,273,741; dental 20,618,644 / 18,768,204; other 97,519,810 "
    "/ 82,380,591. The FY2023 filing gives the same fifteen lines for FY2023 and FY2022",
    "CLHO FY2025 audited consolidated statements note 25 'Revenue'; FY2023 audited statements note "
    "24 'Revenue'", CO, "2026-03-16",
    url=f"{IRBASE}/media/pj0ldhq3/chc-consolidated-31-dec-2025.pdf",
    is_fs_data=True, fiscal_period="FY2025",
    detail="ALL FOUR YEARS RE-ADDED AND EXACT: FY2025 sums to 7,227,264,460; FY2024 to "
           "5,420,396,411; FY2023 to 3,595,299,364; FY2022 to 2,584,032,374. The note also splits "
           "point-in-time (5,644,020,322 FY2025) from over-time recognition (inpatient, "
           "1,583,244,138). 'Service charge' is disclosed as NOT a separate performance obligation "
           "but a fixed-percentage surcharge on every stream except medicine sales — so it is a "
           "MARK-UP on the other lines, not a line to grow independently.",
    model_impact="DRIVER UNLOCK, and the reason the revenue build is at service-line level rather "
                 "than segment level. Combined with the IR volume grid (F47) it gives audited "
                 "revenue per unit for the five lines that have a disclosed volume. Service charge "
                 "is modelled as a percentage of the other lines, never grown on its own — doing "
                 "so double-counts.")

f_segnote = R.add(
    Ring.COMPANY, "official financial statements", FindingClass.D,
    "THE AUDITED SEGMENT NOTE IS A PER-ENTITY P&L AND BALANCE SHEET. FY2025 revenue by entity: "
    "Cleopatra Hospital 2,461,037,749; Cairo Specialised 1,579,063,693; Al Shorouk 1,074,090,828; "
    "Nile Badrawy 1,056,561,565; Cleopatra Heaven (October) 404,518,175; ElKateb 350,388,230; CHG "
    "Medical Services 205,154,327; Bedaya 166,098,826; CHG Pharma 117,727,831; CHG for Hospitals "
    "3,789,997; CHG SKY (El Tagamoa) ZERO; consolidation entries (191,166,761). Profit by entity "
    "shows CHG SKY at a loss of 133,926,040 and Cleopatra Heaven at a loss of 60,597,347 despite "
    "EGP 92,422,789 of gross profit",
    "CLHO FY2025 audited consolidated statements note 6 'Segment reporting'", CO, "2026-03-16",
    url=f"{IRBASE}/media/pj0ldhq3/chc-consolidated-31-dec-2025.pdf",
    is_fs_data=True, fiscal_period="FY2025",
    detail="RE-ADDED: FY2025 revenue row sums to 7,227,264,460 exactly; gross profit row to "
           "2,858,469,867 exactly; profit row to 967,866,314 against a printed 967,866,317, a "
           "3 EGP rounding; depreciation row to 217,627,002 exactly, which reconciles to notes 26 "
           "+ 27 (189,035,104 + 28,591,899). FY2024 revenue row sums to 5,420,396,411 exactly.",
    model_impact="DRIVER UNLOCK for a per-hospital build and for the minority-interest bridge. It "
                 "gives Cairo Specialized Hospital's standalone equity (EGP 935,810,254) against "
                 "which the 42.99% NCI is carried, so the NCI can be deducted at a fair value "
                 "derived from CSH's own earnings rather than at book.")

f_footfail = R.add(
    Ring.COMPANY, "official financial statements", FindingClass.S,
    "ONE PRINTED ROW DOES NOT FOOT, AND IT MATTERS. In the FY2025 filing's FY2024 segment "
    "comparative, the 'Capital expenditures' row prints a DASH for CHG SKY Hospital but a total of "
    "EGP 2,648,894,145. The visible cells sum to EGP 746,376,706 — a gap of EGP 1,902,517,439",
    "CLHO FY2025 audited consolidated statements note 6, FY2024 segment table, read off the "
    "rendered page at 500 dpi to confirm the dash is printed rather than an extraction artefact",
    CO, "2026-03-16",
    url=f"{IRBASE}/media/pj0ldhq3/chc-consolidated-31-dec-2025.pdf",
    is_fs_data=True, fiscal_period="FY2024",
    detail="ARITHMETIC IS THE ARBITER AND IT SETTLES IT: the FY2024 filing's own fixed-asset note "
           "shows total additions of EGP 2,648,894,145 of which 2,370,110,733 went to projects in "
           "progress, and CHG SKY's non-current assets rose to 2,090,342,154 by end-2024 from "
           "near zero. The TOTAL is right; the missing cell belongs to CHG SKY. A build that reads "
           "the row as printed will understate FY2024 group capex by 72%.",
    model_impact="FY2024 capex is EGP 2,648,894,145, not the EGP 746,376,706 the row appears to "
                 "show. This is the denominator of the 'capex 49% of sales in 2024' claim in F52 "
                 "(2,648.9 / 5,420.4 = 48.9%), which confirms the total and the correction.")

f_q1fs = R.add(
    Ring.COMPANY, "official financial statements", FindingClass.D,
    "Q1-2026 reviewed interim condensed consolidated statements at 31 March 2026. Revenue EGP "
    "1,972,518,001 (Q1-2025: 1,618,657,555); cost 1,327,929,734; gross profit 644,588,267 (32.7%); "
    "G&A 327,049,341; impairment 31,410,667; operating profit 278,786,462 (Q1-2025: 348,723,100); "
    "finance income 11,432,241; finance expense 71,000,964; PBT 219,217,739; net profit 152,908,590 "
    "(Q1-2025: 232,289,270); attributable 118,094,800; EPS 0.08. Total assets 10,984,688,836; "
    "equity 4,209,623,882; total liabilities 6,775,064,954",
    "CLEOPATRA HOSPITAL COMPANY 'S.A.E.' AND ITS SUBSIDIARIES, interim condensed consolidated "
    "financial statements for the three months ended 31 March 2026", CO, "2026-06-04",
    url=f"{IRBASE}/media/wtoefjbp/chc-consolidated-fs-31-march-2026.pdf",
    is_fs_data=True, fiscal_period="Q1-2026",
    detail="THIS FILING IS IMAGE-ONLY: 31 pages, ZERO extractable text characters. Rendered at "
           "250 dpi and read off the pixels. EVERY column re-added against the filing's own "
           "printed subtotals and every one foots: non-current assets 8,179,293,869 + current "
           "2,805,394,967 = 10,984,688,836 = equity 4,209,623,882 + liabilities 6,775,064,954. "
           "Limited review by PricewaterhouseCoopers Ezzeldeen, Diab & Co., Mohamed Elsawaf "
           "(R.A.A. 39521, F.R.A. 419), 4 June 2026, unmodified conclusion under Egyptian "
           "Accounting Standard 30.",
    model_impact="First quarter of the study year, and the first quarter of CTH consolidation. "
                 "The gross margin trough (32.7%) and the operating-profit fall (-20% y/y despite "
                 "+22% revenue) are the launch-cost signature the forecast must model explicitly, "
                 "not smooth.")

f_q2fs = R.add(
    Ring.COMPANY, "official financial statements", FindingClass.D,
    "H1/Q2-2026 reviewed interim condensed consolidated statements at 30 June 2026, signed 3 "
    "September 2026. H1: revenue EGP 4,309,172,850; cost 2,842,493,175; gross profit 1,466,679,675 "
    "(34.0%); G&A 785,072,835; impairment 43,037,092; other expenses 16,852,993; operating profit "
    "621,716,755; finance expense 148,516,638; PBT 489,515,277; net profit 342,038,711; "
    "attributable 270,723,576; NCI 71,315,135; EPS 0.19. Q2 alone: revenue 2,336,654,849; gross "
    "profit 822,091,408 (35.2%); net profit 189,130,121; EPS 0.11. Total assets 11,193,301,434; "
    "equity 4,262,989,226; liabilities 6,930,312,208",
    "CLEOPATRA HOSPITAL COMPANY 'S.A.E.' AND ITS SUBSIDIARIES, interim condensed consolidated "
    "financial statements for the six months ended 30 June 2026", CO, "2026-09-03",
    url=f"{IRBASE}/media/lu2hhgwg/chc-consolidated-fs-30-june-2026.pdf",
    is_fs_data=True, fiscal_period="Q2-2026",
    detail="ROUTE: P&L, equity and notes from the text layer; the statement of financial position "
           "is again an image and was read at 250 dpi. Both re-added; every column foots: "
           "8,416,081,432 + 2,777,220,002 = 11,193,301,434 = 4,262,989,226 + 6,930,312,208. The "
           "31-Dec-2025 comparative column reproduces the audited FY2025 balance sheet exactly.",
    model_impact="Second and latest quarter of the study year. Q2 gross margin recovers 250bp from "
                 "Q1 to 35.2%, which is the evidence for the margin-recovery path, and net profit "
                 "is still down 35% y/y, which is the evidence against extrapolating it.")

f_capint = R.add(
    Ring.COMPANY, "official financial statements", FindingClass.S,
    "INTEREST IS BEING CAPITALISED AT SCALE AND REPORTED EARNINGS DO NOT SHOW IT. Capitalised "
    "interest on projects under construction, cumulative in projects-in-progress: EGP 40,645,800 "
    "at 31-Dec-2023, EGP 386,226,438 at 31-Dec-2024, EGP 837,689,037 at 31-Dec-2025. The amounts "
    "capitalised DURING the year are therefore c.EGP 345.6mn in 2024 and c.EGP 451.5mn in 2025, "
    "against P&L finance expense of only EGP 122,045,000 and EGP 227,319,411",
    "CLHO FY2025 audited consolidated statements, note 7 'Fixed assets', closing sentence; FY2024 "
    "audited statements, same note", CO, "2026-03-16",
    url=f"{IRBASE}/media/pj0ldhq3/chc-consolidated-31-dec-2025.pdf",
    is_fs_data=True, fiscal_period="FY2025",
    detail="TWO ROUTES DISAGREED HERE AND THE DISAGREEMENT IS RECORDED. A 250-dpi visual read of "
           "the page gave 837,680,937; the PDF text layer gave 837,689,037. A 600-dpi re-render of "
           "that single line settled it: 837,689,037. Arithmetic agrees independently — total "
           "FY2025 interest of 227.3mn expensed plus 451.5mn capitalised on average gross debt of "
           "EGP 2,937,811,066 implies 23.1%, consistent with the CBE lending rate plus a thin "
           "margin (F35); the alternative reading (838mn capitalised in-year) would imply 36% and "
           "is impossible.",
    model_impact="FY2025 reported finance expense of EGP 227mn understates the true interest cost "
                 "by c.EGP 451mn. The FCFF build must add capitalised interest back to interest "
                 "paid or it will double-count the benefit — once in a low interest charge and "
                 "again in a capitalised asset. The company's own 'normalized net profit' adds "
                 "back only the EXPENSED interest, so EGP 1,162mn for FY2025 (F45) is not a "
                 "measure of interest-free earnings.")

f_fixed = R.add(
    Ring.COMPANY, "official financial statements", FindingClass.S,
    "TWO-THIRDS OF THE FIXED-ASSET BASE IS NOT YET EARNING OR DEPRECIATING, AND THE LAND IS TINY. "
    "At 31-Dec-2025 net fixed assets of EGP 7,072,923,092 comprise projects in progress "
    "4,738,267,842 (67.0%), buildings 1,259,957,999, machinery and equipment 719,073,258, land "
    "173,240,262, furniture 113,444,181, transport 35,251,656, computers 33,687,894. FY2025 "
    "additions were EGP 2,651,593,225, of which 2,491,030,253 went into projects in progress",
    "CLHO FY2025 audited consolidated statements, note 7 'Fixed assets'", CO, "2026-03-16",
    url=f"{IRBASE}/media/pj0ldhq3/chc-consolidated-31-dec-2025.pdf",
    is_fs_data=True, fiscal_period="FY2025",
    detail="RE-ADDED AND EXACT in every direction: components sum to 7,072,923,092; cost "
           "8,278,631,622 less accumulated depreciation 1,205,708,530 = the same; additions sum to "
           "2,651,593,225; depreciation for the year sums to 217,627,002; transfers from projects "
           "in progress net to zero. DIRECTLY QUALIFIES THE MANAGEMENT NARRATIVE in the H1-2026 "
           "release, which invites the reader to value 'the property that houses' the group at "
           "EGP 7.6bn of fixed assets carried at historical cost: land at cost is EGP 173mn, and "
           "the bulk of the EGP 7.6bn is construction in progress on land the group does NOT own — "
           "Cleopatra October and Cleopatra El Tagamoa are both operated under revenue-share "
           "contracts on someone else's land (F38, F39), with the complex returned on expiry.",
    model_impact="Two hard consequences. (1) Depreciation will step up sharply as EGP 4.7bn "
                 "transfers out of projects in progress — FY2025 depreciation of EGP 217.6mn is "
                 "not a run-rate. (2) Any per-bed or asset-backed lens must NOT treat the fixed-"
                 "asset base as owned real estate; state the split explicitly.")

f_auditor = R.add(
    Ring.COMPANY, "official financial statements", FindingClass.C,
    "Auditor is PricewaterhouseCoopers Ezzeldeen, Diab & Co. (PwC Egypt), signing partner Mohamed "
    "Elsawaf, R.A.A. 39521, F.R.A. 419. Limited review conclusions on the Q1-2026 (4 Jun 2026) and "
    "H1-2026 (3 Sep 2026) interims are unmodified, under Egyptian Accounting Standard 30 and the "
    "Egyptian Standard on Limited Review Engagements 2410",
    "CLHO Q1-2026 and H1-2026 interim condensed consolidated financial statements, limited review "
    "reports", CO, "2026-09-03",
    url=f"{IRBASE}/media/wtoefjbp/chc-consolidated-fs-31-march-2026.pdf",
    detail="Read off the rendered pixels of the scanned Q1-2026 report. Note the reporting "
           "framework is EGYPTIAN Accounting Standards, not IFRS as issued by the IASB — relevant "
           "wherever the study benchmarks CLHO against IFRS-reporting regional peers.",
    model_impact="")

f_eps = R.add(
    Ring.COMPANY, "official financial statements", FindingClass.S,
    "CLHO PUBLISHES THREE DIFFERENT EPS FOR THE SAME PERIOD AND A BUILD THAT MIXES THEM IS WRONG. "
    "(a) Annual audited note: (attributable profit less employee and board dividends) / weighted "
    "average shares — FY2025 (823,881,689 - 154,056,861) / 1,441,509,083 = EGP 0.46; FY2024 0.39. "
    "(b) Interim reviewed note: attributable profit / weighted average shares, with NO employee-"
    "dividend deduction — Q1-2026 0.08, Q2-2026 0.11, H1-2026 0.19. (c) Earnings release and IR "
    "presentation: GROUP net profit INCLUDING minority interest / shares outstanding — FY2025 EGP "
    "0.67, Q1-2026 EGP 0.11",
    "CLHO FY2025 audited statements note 34; H1-2026 reviewed statements note 19; FY2025 Earnings "
    "Release and FY2025 Investor Presentation", CO, "2026-03-16",
    url=f"{IRBASE}/media/pj0ldhq3/chc-consolidated-31-dec-2025.pdf",
    is_fs_data=True, fiscal_period="FY2025",
    detail="Verified: 968mn / 1,449mn shares = 0.67, which is the release figure and includes the "
           "EGP 143,984,628 that belongs to minorities. Attributable profit over shares "
           "outstanding is 0.568. The audited 0.46 is the only IAS-33 figure. The interim note "
           "additionally MISLABELS its deduction: it calls EGP 71,315,135 'Dividends for employees "
           "and the board of directors' when that is exactly the H1-2026 non-controlling interest, "
           "and the same holds in all four interim columns. The number is right (the numerator is "
           "attributable profit); the label is wrong. Interim EPS therefore does NOT sum to annual "
           "EPS.",
    model_impact="Fix the EPS convention before any multiple lens is struck. At the EGP 17.71 "
                 "close, trailing P/E is 26x on the release's 0.67 and 38x on the audited 0.46 — "
                 "a 45% difference in the headline multiple from a definitional choice alone. Use "
                 "the audited attributable basis and state it.")

# ---------------------------------------------------------------------------
# RING 4 — COMPANY : regular disclosures
# ---------------------------------------------------------------------------
f_cogs = R.add(
    Ring.COMPANY, "regular disclosures", FindingClass.D,
    "COST OF REVENUE IS DISCLOSED BY NATURE, SO COST PER CASE IS BUILDABLE AND MARGIN IS AN "
    "OUTPUT. FY2025 / FY2024: medical and pharmaceutical supplies 1,650,595,778 / 1,187,422,589; "
    "employees' wages and benefits 1,045,589,981 / 818,835,091; doctors' fees 900,546,805 / "
    "753,129,443; maintenance, spares and energy 220,121,782 / 189,401,497; fixed-asset "
    "depreciation 189,035,104 / 150,163,840; external services 119,790,755 / 93,331,981; "
    "consumables 117,124,121 / 103,388,921; right-of-use depreciation 22,692,367 / 44,594,142; "
    "rent-prepayment amortisation 1,440,000 / nil; miscellaneous 101,857,900 / 66,785,558",
    "CLHO FY2025 audited consolidated statements note 26 'Cost of obtaining revenue'; the H1-2026 "
    "reviewed statements repeat the same eleven-line split at note 16", CO, "2026-03-16",
    url=f"{IRBASE}/media/pj0ldhq3/chc-consolidated-31-dec-2025.pdf",
    is_fs_data=True, fiscal_period="FY2025",
    detail="RE-ADDED AND EXACT: FY2025 sums to 4,368,794,593; FY2024 to 3,407,053,062. Against "
           "1,472,534 cases served, FY2025 medical supplies are EGP 1,121 per case. The H1-2026 "
           "note gives the same lines quarterly, and the release's cost ratios reconcile to it: "
           "Q2-2026 doctor fees 13.0% + salaries 16.4% + medical consumables 21.2% + other 14.4% "
           "= 65.0% of revenue against a 64.8% cost ratio implied by the 35.2% gross margin.",
    model_impact="DRIVER UNLOCK, AND THE REASON GROSS MARGIN IS NEVER AN INPUT. Build medical "
                 "supplies and consumables as EGP per case, doctors' fees as a percentage of the "
                 "procedure lines they attach to, salaries as a staffing cost that steps with beds "
                 "opened, and let the margin fall out. Setting a contribution or gross margin "
                 "directly would be a QC FAIL on this name because the filings disclose enough to "
                 "build the cost per unit instead.")

f_ga = R.add(
    Ring.COMPANY, "regular disclosures", FindingClass.D,
    "G&A IS ALSO DISCLOSED BY NATURE. FY2025 / FY2024: employees' wages and benefits 606,746,595 / "
    "354,852,617; marketing 153,267,608 / 70,071,533; IT programs 120,482,329 / 68,203,797; "
    "external services 88,056,812 / 58,644,936; professional and consulting fees 55,741,547 / "
    "41,933,843; maintenance, spares and energy 33,462,608 / 18,516,419; fixed-asset depreciation "
    "28,591,899 / 32,022,158; right-of-use depreciation 10,353,567 / 8,392,379; consumables "
    "8,272,803 / 5,907,495; intangible amortisation 2,069,284 / 2,069,284; miscellaneous "
    "122,285,987 / 89,182,108",
    "CLHO FY2025 audited consolidated statements note 27; H1-2026 reviewed statements note 17",
    CO, "2026-03-16",
    url=f"{IRBASE}/media/pj0ldhq3/chc-consolidated-31-dec-2025.pdf",
    is_fs_data=True, fiscal_period="FY2025",
    detail="RE-ADDED AND EXACT: FY2025 sums to 1,229,331,039; FY2024 to 749,796,569 (the FY2024 "
           "filing's face prints 749,796,568, a 1 EGP rounding). MAPPING WARNING: the earnings "
           "release's 'General & administrative expenses' is NOT this line. Release H1-2026 G&A of "
           "EGP 828.1mn = statutory G&A 785,072,835 + net impairment losses 43,037,092 = "
           "828,109,927. The release's 'Provisions (21.0)' and 'Other income 4.1' are a gross-up "
           "of the statutory 'Other expenses (16,852,993)'.",
    model_impact="Build G&A in two pieces because they behave differently: a headcount-and-"
                 "marketing base that scales with the network, and the LTIP mark-to-market charge "
                 "(F55), which is a function of CLHO's own share price and must NOT be projected "
                 "as an operating cost ratio. Map release lines to statutory lines before using "
                 "either.")

f_loans = R.add(
    Ring.COMPANY, "regular disclosures", FindingClass.D,
    "EVERY BORROWING IS CONTRACTUALLY PRICED OFF THE CBE LENDING RATE, SO Kd IS SOURCED, NOT "
    "ESTIMATED. Kuwait Finance House facility (27 Oct 2021, raised to a EGP 740mn limit across "
    "Cleopatra Hospital, Cairo Specialized and Nile Badrawy): CBE lending rate + 0.65%. Nile "
    "Badrawy clinics facility (7 Oct 2025, EGP 140mn): CBE lending rate + 0.80%. Commercial "
    "International Bank facility to CHG Sky (5 Jun 2023, EGP 1,339,573,000 raised to "
    "EGP 2,194,600,000): CBE lending rate + 0.05% for nine months then + 0.09%. Total loans EGP "
    "3,135,813,053 at FY2025 and EGP 3,202,878,438 at 30 Jun 2026",
    "CLHO FY2025 audited consolidated statements note 17 'Loans'; H1-2026 reviewed statements "
    "note 12", CO, "2026-09-03",
    url=f"{IRBASE}/media/lu2hhgwg/chc-consolidated-fs-30-june-2026.pdf",
    is_fs_data=True, fiscal_period="FY2025",
    detail="At the CBE overnight lending rate of 20.00% (F06) this is a contractual Kd of 20.05% "
           "to 20.80% depending on facility. The all-in effective rate on average FY2025 gross "
           "debt, including capitalised interest, is 23.1% (F31) — higher because the CBE lending "
           "rate averaged above 20% through 2025 and overdrafts price differently. The book is "
           "100% EGP (note 2.2): no FX exposure in the debt.",
    model_impact="DRIVER UNLOCK. Kd = published CBE lending rate + the disclosed contractual "
                 "margin, weighted by facility, glided on the CBE path — never a market spread "
                 "assumption. The overdraft balance (EGP 608,992,576 at 30 Jun 2026) prices "
                 "separately and must be modelled separately.")

f_cov = R.add(
    Ring.COMPANY, "regular disclosures", FindingClass.S,
    "THE CIB FACILITY CARRIES A DATED COVENANT SCHEDULE AND ITS AMORTISATION STARTS THIS QUARTER. "
    "Financial leverage must not exceed 5.18x in 2026, 2.85x 2027, 1.98x 2028, 1.34x 2029, 0.94x "
    "2030, 0.65x 2031, 0.46x 2032; debt-service ratio must not fall below 1; capex is capped on a "
    "stated annual schedule. The grace period ended 30 June 2026 and repayment runs 27 quarterly "
    "instalments from 30 September 2026 to 31 December 2032",
    "CLHO H1-2026 reviewed interim statements, note 12 'Loans (continued)', CIB Loan (CHG Sky "
    "Company), 'Financial ratios'", CO, "2026-09-03",
    url=f"{IRBASE}/media/lu2hhgwg/chc-consolidated-fs-30-june-2026.pdf",
    is_fs_data=True, fiscal_period="Q2-2026",
    detail="The capex-cap schedule prints as 6,838,000 / 8,117,000 / 9,404,000 / 10,663,000 / "
           "12,252,000 / 13,960,000 / 17,291,000 'EGP'. Taken literally an EGP 6.8mn 2026 cap is "
           "impossible against H1-2026 capex of EGP 813mn, so the units are almost certainly EGP "
           "thousands. THE UNITS ARE NOT STATED IN THE FILING and the study must not guess: flag "
           "it and, if the capex cap is load-bearing, ask the company. The leverage schedule "
           "against management's own guidance is the tighter test — net debt / annualised H1-2026 "
           "adjusted EBITDA is c.1.50x (F44), comfortably inside 5.18x for 2026 but the 2027 step "
           "to 2.85x is a real constraint on further debt-funded expansion.",
    model_impact="Sets a hard floor under debt repayment from Q3-2026 and a hard ceiling over "
                 "incremental leverage from 2027. The debt schedule in the model is CONTRACTUAL "
                 "from this note, not a plug, and any expansion beyond the named pipeline must be "
                 "financed inside the leverage ladder or by equity.")

f_commit = R.add(
    Ring.COMPANY, "regular disclosures", FindingClass.D,
    "THE CAPEX CYCLE IS CLOSING AND THE COMMITMENT BALANCE PROVES IT: capital commitments not yet "
    "due were EGP 487,283,142 at 31-Dec-2024, EGP 151,017,672 at 31-Dec-2025 and EGP 13,340,800 at "
    "30 June 2026 — a 97% fall in eighteen months",
    "CLHO FY2025 audited consolidated statements note 36 'Commitments'; H1-2026 reviewed statements "
    "note 20", CO, "2026-09-03",
    url=f"{IRBASE}/media/lu2hhgwg/chc-consolidated-fs-30-june-2026.pdf",
    is_fs_data=True, fiscal_period="Q2-2026",
    detail="Corroborates management's guided capex path of 49% of sales in 2024, 37% in 2025 and "
           "c.10% in 2026 (F52) with an audited, contractual number rather than a forecast. H1-2026 "
           "capex was EGP 813mn (payments under capital commitments 721.6 + fixed-asset purchases "
           "91.5), which is 18.9% of H1 revenue — so the full-year c.10% guidance requires a very "
           "light H2.",
    model_impact="DRIVER UNLOCK for the capex driver: the near-zero commitment balance is hard "
                 "evidence that maintenance capex, not growth capex, is the FY2027+ level. But "
                 "H1-2026 actuals at 18.9% of sales are well above the 10% full-year guide, so the "
                 "FY2026 capex line is built from H1 actual plus a guided H2, and the gap is "
                 "flagged rather than averaged.")

f_nci = R.add(
    Ring.COMPANY, "regular disclosures", FindingClass.D,
    "MINORITY INTERESTS ARE CONCENTRATED IN ONE HOSPITAL AND THE NOTE GIVES ITS STANDALONE "
    "BALANCE SHEET. NCI percentages at FY2025: Cairo Specialised Hospital 42.99%, CHG Medical "
    "Services 40.00%, CHG Pharma 2.00%, Nile Badrawy 0.01%, Al Shorouk 0.01%. CSH standalone: "
    "current assets 808,183,514, current liabilities 403,380,576, non-current assets 608,969,751, "
    "non-current liabilities 77,962,435, equity 935,810,254. Total NCI on the group balance sheet "
    "EGP 418,028,210 at FY2025 and EGP 480,076,147 at 30 Jun 2026",
    "CLHO FY2025 audited consolidated statements note 24 'Non-controlling interests'", CO,
    "2026-03-16",
    url=f"{IRBASE}/media/pj0ldhq3/chc-consolidated-31-dec-2025.pdf",
    is_fs_data=True, fiscal_period="FY2025",
    detail="RE-ADDED AND EXACT: each subsidiary's net current and net non-current assets sum to its "
           "stated equity, and the NCI roll-forward closes (278,208,598 - 4,166,834 + 1,818 + "
           "143,984,628 = 418,028,210). CSH equity 935,810,254 x 42.99% = EGP 402.4mn, which is "
           "96% of the group NCI.",
    model_impact="The equity bridge deducts NCI at FAIR value, not book. CSH's own FY2025 revenue "
                 "(EGP 1,579,063,693, F23) and profit (EGP 284,817,902) are disclosed, so the 42.99% "
                 "minority can be valued on CSH's own earnings. Deducting the EGP 418mn book "
                 "figure would understate the deduction materially.")

f_subs = R.add(
    Ring.COMPANY, "regular disclosures", FindingClass.S,
    "SUBSIDIARY OWNERSHIP AT 30 JUNE 2026 IS UNCHANGED FROM 31 DECEMBER 2025, AND CAIRO SPECIALIZED "
    "IS STILL 57.01%. Al-Shorouk 99.99%, Nile Badrawi 99.99%, Cairo Specialised 57.01%, CHG for "
    "Medical Services 20% (preferred shares), CHG Pharma 98%, CHG for hospitals 99.99%, Bedaya El "
    "Gedida 60%, CHG Sky Hospital 99.99%, Cleopatra Heaven Hospital 99.99%",
    "CLHO H1-2026 reviewed interim statements, note 2.1 subsidiary schedule", CO, "2026-09-03",
    url=f"{IRBASE}/media/lu2hhgwg/chc-consolidated-fs-30-june-2026.pdf",
    is_fs_data=True, fiscal_period="Q2-2026",
    detail="THIS IS THE COMPANY-OFFICIAL EVIDENCE THAT THE MAY-2025 CAIRO SPECIALIZED TRANSACTION "
           "(F58) HAD NOT COMPLETED AS AT 30 JUNE 2026. Note also that CHG for Medical Services is "
           "consolidated as a subsidiary on a 20% PREFERRED-share holding with a 40% NCI — a "
           "control-not-ownership structure that a proportionate build would get wrong.",
    model_impact="Fixes the consolidation perimeter for the forecast: CSH consolidates in full with "
                 "a 42.99% minority throughout the explicit window unless and until the transaction "
                 "completes, in which case it is a dated, dual-framed event (F58), never a smoothed "
                 "step-up.")

f_cth_contract = R.add(
    Ring.COMPANY, "regular disclosures", FindingClass.D,
    "CLEOPATRA EL TAGAMOA IS NOT OWNED — IT IS A 27-YEAR OPERATING RIGHT WITH A STEPPED REVENUE "
    "SHARE. Agreement of 29 December 2021 between the Housing and Social Services Fund for "
    "Petroleum Sector Workers, GASCO and Town Gas (first party) and CHG (second party): 27 calendar "
    "years from signing; CHG completes all construction, electromechanical and interior finishing "
    "and equips the hospital at its own expense; the hospital including all equipment is delivered "
    "to the first party on expiry. Revenue share: 2% of total annual revenue in operating years 1-2, "
    "3% from year 3 to year 6, 4% from year 7 to the end",
    "CLHO H1-2026 reviewed interim statements, note 21.2 'Right of use, management and operation "
    "contract for CHG Sky Hospital SAE'", CO, "2026-09-03",
    url=f"{IRBASE}/media/lu2hhgwg/chc-consolidated-fs-30-june-2026.pdf",
    is_fs_data=True, fiscal_period="Q2-2026",
    detail="27 years from 29 Dec 2021 ends 2048. The revenue share is a real, contractual, STEPPING "
           "cost that does not appear as a separate P&L line and is not in any earnings-release "
           "margin bridge.",
    model_impact="DRIVER UNLOCK and a terminal-value constraint. Model the CTH revenue share "
                 "explicitly at 2% / 3% / 4% on CTH revenue with the step dates, and cap the "
                 "terminal value: CLHO hands the asset back in 2048, so a perpetuity on CTH cash "
                 "flow is wrong. This also settles what the 'owned real estate' narrative in F32 "
                 "can and cannot mean.")

f_coh_contract = R.add(
    Ring.COMPANY, "regular disclosures", FindingClass.D,
    "CLEOPATRA OCTOBER IS ALSO A CONTRACT, IT WAS RE-CUT IN FEB-2025, AND ITS REVENUE SHARE IS "
    "HIGHER. The 31 October 2022 usufruct was mutually TERMINATED and replaced on 6 February 2025 "
    "by a 25-year partnership with the Fund for Improving Social and Healthcare Services for Police "
    "Officers and Their Families, running 25 years from the date of obtaining the operating licence "
    "and renewable. The Fund builds and completes the complex; CHG equips and operates at its own "
    "cost and returns everything on expiry. CHG paid EGP 250,000,000 within 30 days of signing as "
    "an advance amortised against the participation percentages, and forfeited the EGP 36,000,000 "
    "advance paid under the old usufruct. Revenue share: 8% of total revenue in years 1-5, 9% in "
    "years 5-6, 10% for the remaining term",
    "CLHO H1-2026 reviewed interim statements, note 6 'Advance payments / Revenue share'", CO,
    "2026-09-03",
    url=f"{IRBASE}/media/lu2hhgwg/chc-consolidated-fs-30-june-2026.pdf",
    is_fs_data=True, fiscal_period="Q2-2026",
    detail="The balance rolls exactly: additions 286,000,000 in FY2025 (250 + 36) less 1,440,000 "
           "used less 34,223,894 revenue share = 250,336,106; less 720,000 less 10,226,432 in "
           "H1-2026 = 239,389,674. RESOLVES the 18-year-vs-25-year contradiction between the "
           "1 Nov 2022 Haven press release ('18-year concession agreement') and the FY2025 IR "
           "presentation ('25-year revenue-share agreement') — the agreement was replaced. NOTE "
           "the H1-2026 revenue-share consumption of EGP 10,226,432 is only c.3.9% of an estimated "
           "EGP 259mn of COH H1 revenue, not 8%: the licence-date trigger appears not to have run "
           "for the full period. Resolve this before modelling.",
    model_impact="DRIVER UNLOCK. The COH revenue share is 8% stepping to 10% — twice CTH's — and "
                 "runs on the FULL Haven Medical Complex revenue once the 200-bed extension opens, "
                 "so the cost scales with the very expansion that drives the revenue. The EGP "
                 "250mn advance is a prepaid credit that runs out; after it does, the 8% is paid "
                 "in cash. Both must be in the model. Terminal value is again capped by the "
                 "25-year term.")

f_bslabel = R.add(
    Ring.COMPANY, "regular disclosures", FindingClass.S,
    "THE H1-2026 EARNINGS RELEASE SWAPS TWO BALANCE-SHEET LABELS AND A BUILD THAT TRUSTS IT PUTS "
    "EGP 242mn IN THE WRONG BUCKET. The release's 30-June-2026 column shows 'Current Portion of "
    "Long-term incentive plan 241.9' and 'Current income tax 116.6'. The reviewed statement shows "
    "Employees stock ownership Plan (current) EGP 116,599,651 and Current income tax liabilities "
    "EGP 241,854,674 — the reverse",
    "CLHO H1-2026 Earnings Release, Consolidated Statement of Financial Position, compared with the "
    "reviewed interim statements at 30 June 2026", CO, "2026-09-06",
    url=f"{IRBASE}/media/sufdt2ur/cleopatra-earnings-release-2q2026.pdf",
    is_fs_data=True, fiscal_period="Q2-2026",
    detail="The release's own 31-Dec-2025 column (LTIP 74.0, current income tax 284.2) matches the "
           "audited FY2025 balance sheet correctly, so the error is confined to the June-2026 "
           "column. Total current liabilities are unaffected. THE REVIEWED STATEMENT GOVERNS.",
    model_impact="Working-capital and tax-payable modelling must use the reviewed statement, not "
                 "the release table. More broadly: where the release and the reviewed statement "
                 "disagree, the statement wins and the disagreement is recorded.")

f_div = R.add(
    Ring.COMPANY, "regular disclosures", FindingClass.S,
    "CLHO PAYS NO ORDINARY SHAREHOLDER DIVIDEND. The 'Dividends' line in the statement of changes "
    "in equity is the employee and board profit share: EGP 142,179,178 to parent-company retained "
    "earnings plus EGP 4,166,834 from NCI in FY2025, and EGP 144,107,006 plus EGP 9,269,573 in "
    "H1-2026. The FY2025 EPS note deducts a different figure, EGP 154,056,861, for the same item. "
    "The Board said on 6 Sep 2026 it 'may in time consider the merits of a dividend policy'",
    "CLHO FY2025 audited statements, consolidated statement of changes in equity and note 34; "
    "H1-2026 reviewed statements, statement of changes in equity; H1-2026 Earnings Release "
    "management comment", CO, "2026-09-06",
    url=f"{IRBASE}/media/lu2hhgwg/chc-consolidated-fs-30-june-2026.pdf",
    is_fs_data=True, fiscal_period="FY2025",
    detail="Cash flow confirms the outflow is real: 'Dividends paid out' EGP 146.3mn in H1-2025 and "
           "EGP 143.4mn in H1-2026. The 142,179,178 vs 154,056,861 gap is accrual-versus-payment "
           "timing and should be reconciled before either is used.",
    model_impact="Two consequences. (1) No dividend-discount lens is available and no dividend "
                 "yield exists — say so rather than showing a zero. (2) The employee and board "
                 "profit share is a RECURRING c.EGP 145-155mn annual cash outflow ahead of "
                 "shareholders and must sit in the equity free-cash-flow build, not be netted "
                 "into equity movements.")

# ---------------------------------------------------------------------------
# RING 4 — COMPANY : IR communications
# ---------------------------------------------------------------------------
f_er25 = R.add(
    Ring.COMPANY, "IR communications (calls, presentations, releases)", FindingClass.D,
    "FY2025 Earnings Release (17 March 2026) carries the FULL-YEAR PHYSICAL GRID no financial "
    "statement holds. Volumes FY2024 -> FY2025 with revenue in EGP mn: outpatient visits 1,068k -> "
    "1,205k (+13%), revenue 498 -> 668 (+34%); surgeries by patient 29,207 -> 32,201 (+10%) and by "
    "procedure 42,558 -> 43,415 (+2%), revenue 1,101 -> 1,360 (+24%); inpatients 66,859 -> 75,107 "
    "(+12%), revenue 1,233 -> 1,583 (+28%); emergency visits 174,597 -> 192,620 (+10%), revenue "
    "182 -> 266 (+46%); catheterisation 5,510 -> 6,089 (+11%), revenue 392 -> 467 (+19%); "
    "laboratory tests 1,846k -> 2,182k (+18%), revenue 509 -> 787 (+55%); radiology tests 325k -> "
    "385k (+19%), revenue 336 -> 525 (+56%). Cases served 1,472,534 (+12%). Quarterly revenue 1Q24 "
    "1,181, 2Q24 1,191, 3Q24 1,460, 4Q24 1,588, 1Q25 1,619, 2Q25 1,763, 3Q25 1,938, 4Q25 1,907",
    "CLHO FY2025 Earnings Release, 'Core Business Performance' and 'Quarterly Revenue Progression'",
    IR, "2026-03-17",
    url=f"{IRBASE}/media/130p5q30/cleopatra-earnings-release-fy2025.pdf",
    fiscal_period="FY2025",
    detail="TIES TO THE AUDITED NOTE: every revenue figure in this table reproduces the audited "
           "revenue note (F23) rounded to EGP mn, and the quarterly revenues sum to 5,420 for FY24 "
           "and 7,227 for FY25 — the audited totals exactly. The FY2025 KPI panel adds average "
           "revenue per unit: rev/procedure EGP 24,951 -> 30,086; rev/visit 457 -> 506; "
           "rev/inpatient 18,446 -> 21,266; rev/ER visit 1,043 -> 1,348; rev/catheterisation "
           "71,124 -> 78,253. The KPI panel is stated to exclude Bedaya and to be net of "
           "elimination entries, so it runs 3-4% below revenue divided by volume from the table; "
           "use one basis and say which.",
    model_impact="THE CORE DRIVER SET. Volume and ARP are separately disclosed for five service "
                 "lines and volume alone for two more, which is what makes a volume x price build "
                 "possible at service-line level rather than a segment-level approximation.")

f_er_q1 = R.add(
    Ring.COMPANY, "IR communications (calls, presentations, releases)", FindingClass.D,
    "Q1-2026 Earnings Release (7 June 2026): revenue EGP 1,973mn (+22%), gross profit 645mn (33% "
    "margin), adjusted EBITDA 497mn (25%), EBIT 279mn (14%), net profit 153mn (8%, -34%), "
    "normalised net profit 216mn (11%), cases served 355,035 (+9%), EPS EGP 0.11. CTH contributed "
    "EGP 154mn in its inaugural quarter; excluding CTH, organic revenue growth was c.12% against a "
    "Ramadan and extended-Eid quarter. Q1 KPI grid Q1-2025 -> Q1-2026: surgical procedures 9,334 -> "
    "9,301 with rev/procedure EGP 29,792 -> 34,254; paid consultations 265,619 -> 289,368 at EGP "
    "535 -> 549; inpatients 15,803 -> 17,508 at EGP 24,788 -> 26,495; ER visits 43,912 -> 48,159 at "
    "EGP 1,338 -> 1,505; catheterisations 1,467 -> 1,495 at EGP 76,817 -> 95,855",
    "CLHO Q1 2026 Earnings Release", IR, "2026-06-07",
    url=f"{IRBASE}/media/5xajea03/cleopatra-earnings-release-1q2026.pdf",
    fiscal_period="Q1-2026",
    detail="Revenue ties to the reviewed statement (EGP 1,972,518,001). SURGICAL VOLUME FELL 0.4% "
           "in Q1-2026 — the only volume line to fall — and the Q2 recovery to +9% is what carries "
           "the H1 figure to +5%. The quarterly grid subtracts cleanly to Q2 and reproduces the "
           "H1-2026 release's stated Q2 growth rates, so the two releases are consistent.",
    model_impact="First study-year quarter, swept in before the build. Establishes the Ramadan/Eid "
                 "seasonal drag on Q1 volumes, which the forecast must carry as a quarterly "
                 "seasonality pattern rather than a straight-line quarter.")

f_er_h1 = R.add(
    Ring.COMPANY, "IR communications (calls, presentations, releases)", FindingClass.B,
    "H1-2026 Earnings Release (6 September 2026) IS THE NEWEST OPERATING ANCHOR AND IT SUPERSEDES "
    "EVERY EARLIER ONE. Q2-2026: revenue EGP 2,337mn (+33%), gross profit 822mn (35.2%), adjusted "
    "EBITDA 679mn (29.1%), net profit 189mn (8%, -35%), normalised net profit 266mn (11%), cases "
    "served 424,256 (+16%). H1-2026: revenue 4,309mn (+27%), gross profit 1,467mn (34.0%), adjusted "
    "EBITDA 1,176mn (27.3%), net profit 342mn (-34%), cases served 783,451 (+13%). Volumes: "
    "inpatients +18% Q2 / +15% H1, outpatient consultations +17% / +14%, surgical procedures +9% / "
    "+5%. H1 KPI grid H1-2025 -> H1-2026: surgical procedures 20,076 -> 21,049 at EGP 29,720 -> "
    "34,517; paid consultations 565,695 -> 643,906 at EGP 520 -> 544; inpatients 34,485 -> 39,558 "
    "at EGP 22,818 -> 25,389; ER visits 92,396 -> 99,957 at EGP 1,310 -> 1,505; catheterisations "
    "2,990 -> 3,252 at EGP 78,574 -> 85,522. Revenue by hospital H1-2026: Cleopatra Hospital EGP "
    "1,297mn (30%), Cairo Specialized 863mn (20%), Al Shorouk 576mn (13%), Nile Badrawi 541mn "
    "(12%), Cleopatra El Tagamoa 10%, Cleopatra October 6%, El Katib 164mn (4%)",
    "CLHO H1 2026 Earnings Release", IR, "2026-09-06",
    url=f"{IRBASE}/media/sufdt2ur/cleopatra-earnings-release-2q2026.pdf",
    fiscal_period="Q2-2026",
    detail="Three days old at the sweep date. Also carries the per-hospital margin grid — Cairo "
           "Specialized gross margin 38% Q2 / 39% H1 and adjusted EBITDA 25% / 28%; Al Shorouk 37% "
           "and 23% / 24%; Nile Badrawi 34% Q2 / 31% H1 and 19%; Cleopatra October 18% Q1 -> 24% "
           "Q2; Cleopatra El Tagamoa -25% Q1 -> +10% Q2 gross and 8% EBITDA in Q2 — and the "
           "ex-CTH core portfolio at 38.7% gross and 32.0% adjusted EBITDA in Q2. Net financial "
           "debt EGP 3.53bn at June 2026 from EGP 3.16bn at FY2025, c.1.50x annualised H1 adjusted "
           "EBITDA and c.1.60x on a last-twelve-month basis; H1 capex EGP 813mn.",
    model_impact="BASE CHANGER, DUAL-FRAMED. The H1-2026 anchors supersede the FY2025 release and "
                 "the Q1-2026 IR presentation everywhere they conflict, and the study states so. "
                 "The base resets on three things at once: a 33% Q2 revenue step, a 35% net-profit "
                 "FALL on the same quarter, and a capacity base that is 35% larger by year end. "
                 "Model the revenue step and the profit fall as the SAME event — a greenfield "
                 "launch — with an explicit start date, not as a growth glide with a margin dip.")

f_irp25 = R.add(
    Ring.COMPANY, "IR communications (calls, presentations, releases)", FindingClass.D,
    "FY2025 Investor Presentation gives the per-hospital ramp history no release repeats. Cleopatra "
    "October bed trajectory: 36 beds Q1-2023, 42 Q4-2023, 45 Q4-2024, 68 Q3-2025, 80 Q4-2025, 280 "
    "planned FY2026. Cleopatra October revenue EGP 64.6mn FY2023, 248.2mn FY2024, 404.5mn FY2025; "
    "gross profit -3.3 / 34.4 (14%) / 92.4 (23%); EBITDA -23.3 / 3.2 (1%) / 16.9 (4%); cases served "
    "3,447 / 41,592 / 77,670. Cleopatra El Tagamoa: EGP 3.3bn investment, 700mn+ of medical "
    "technology, 240+ beds, 7 operating rooms plus 2 cardiac cath labs, 1mn patient capacity, "
    "2,000+ new jobs when fully operational",
    "CLHO FY2025 Investor Presentation", IR, "2026-03-17",
    url=f"{IRBASE}/media/qcxjlaq4/chg-irp-fy2025.pdf",
    fiscal_period="FY2025",
    detail="Cleopatra October's FY2025 revenue of EGP 404.5mn ties EXACTLY to the audited segment "
           "note's Cleopatra Heaven line (404,518,175), and FY2024's 248.2 to 248,166,411 — so the "
           "presentation's per-hospital series is company-official-grade and can be relied on. "
           "The quarterly revenue figures sum to EGP 291.9mn for 9M-2025 against the stated "
           "'EGP 292mn', and cases to c.54,000 against the stated 'approximately 54,000'.",
    model_impact="DRIVER UNLOCK for a per-bed ramp curve. Cleopatra October gives four years of "
                 "bed count against revenue, gross profit, EBITDA and cases at the same facility — "
                 "an observed, company-specific greenfield ramp function that the Cleopatra El "
                 "Tagamoa forecast can be calibrated against instead of an assumed S-curve.")

f_beds_conflict = R.add(
    Ring.COMPANY, "IR communications (calls, presentations, releases)", FindingClass.S,
    "CLHO'S OWN TWO IR DOCUMENTS DISAGREE ABOUT ITS BED COUNT BY 28%. The FY2025 Investor "
    "Presentation states '1000 beds — Number of Operating Beds as of FY 2025' and '+200 beds as of "
    "FY2026' on its results snapshot, and 'c. 1000 Beds' with '+200 beds to be introduced by "
    "FY26/27' on its cover. The H1-2026 Earnings Release states 'Group operating beds stood at 780 "
    "at the end of 2025 and are expected to reach approximately 1,050 by the end of 2026, an "
    "increase of 35%, with a further 200 beds under construction at Cleopatra October Hospital for "
    "delivery in 2027 and 2028'",
    "CLHO FY2025 Investor Presentation, page 8, read off the rendered page; CLHO H1 2026 Earnings "
    "Release, management comment", IR, "2026-09-06",
    url=f"{IRBASE}/media/sufdt2ur/cleopatra-earnings-release-2q2026.pdf",
    fiscal_period="FY2025",
    detail="Neither is a typo — both are repeated within their own document. The reconciliation "
           "that fits is that the presentation's 1,000 counts Cleopatra El Tagamoa's FULL 240-bed "
           "target as capacity (780 + 240 = 1,020) while the release counts beds actually "
           "OPERATING. The same document set also disagrees on CTH's share of group capacity, "
           "saying 'approximately 24% of Group capacity' in the management comment and "
           "'approximately 30% of the Group's total bed capacity' in the strategy section three "
           "pages later, and on facility count, '16 Facilities' on the presentation cover against "
           "'17 facilities' in its own opening paragraph.",
    model_impact="A per-bed or EV-per-bed lens is 28% different depending on which number is taken. "
                 "USE THE RELEASE'S OPERATING-BED SERIES (780 end-2025, c.1,050 end-2026, +200 "
                 "2027-28) because it is the newer document and it is the one that distinguishes "
                 "operating from planned; state the presentation's 1,000 beside it and say why it "
                 "was not used.")

f_hist_vols = R.add(
    Ring.COMPANY, "IR communications (calls, presentations, releases)", FindingClass.D,
    "The FY2023 Earnings Release extends the physical history back to FY2022 quarter by quarter. "
    "Revenue EGP mn: 1Q22 637, 2Q22 605, 3Q22 661, 4Q22 712, 1Q23 777, 2Q23 808, 3Q23 948, 4Q23 "
    "1,063. Paid outpatients: 200,275 / 189,744 / 214,647 / 238,977 then 219,011 / 217,799 / "
    "250,208 / 252,365. Surgical procedures: 8,206 / 8,732 / 10,252 / 10,362 then 9,109 / 8,921 / "
    "10,856 / 10,598. Inpatients: 12,366 / 12,941 / 14,734 / 15,147 then 14,067 / 13,944 / 16,081 / "
    "16,230. Cath lab patients: 1,214 / 1,103 / 1,000 / 1,271 then 1,289 / 1,240 / 1,341 / 1,467",
    "CLHO FY2023 Earnings Release, 'Quarterly Revenue & Core Business Progression'", IR,
    "2024-03-14",
    url=f"{IRBASE}/media/wu1ftyi0/cleopatra-er-4q2023-e.pdf",
    fiscal_period="FY2022",
    detail="Annual sums: FY2022 revenue EGP 2,615mn, outpatients 843,643, surgical procedures "
           "37,552, inpatients 55,188, cath 4,588; FY2023 revenue EGP 3,596mn, outpatients 939,383, "
           "surgical procedures 39,484, inpatients 60,322, cath 5,337. NOTE THE FY2022 REVENUE SUM "
           "TIES TO THE AS-FILED BASIS (EGP 2,614,421,170), not the restated EGP 2,584,032,374 — "
           "see F21. Bridges to the FY2025 release's FY2024 volumes without a gap.",
    model_impact="Extends the volume history to four complete years, FY2022-FY2025, which is what "
                 "lets the volume driver be fitted rather than assumed. Also gives the quarterly "
                 "seasonal shape (Q3 and Q4 strongest, Q1 and Q2 weakest) that the study year's "
                 "forecast is phased on.")

f_call = R.add(
    Ring.COMPANY, "IR communications (calls, presentations, releases)", FindingClass.C,
    "CLHO holds hosted results calls and the 2Q2026 call took place on Tuesday 8 September 2026 at "
    "15:00 Cairo time, chaired by Hassan Sadek of Beltone Holding, with Dr Ahmed Ezzeldin (CEO), "
    "Hassan Fikry (Chief Strategy & New Businesses Officer), Amr El Rashid (CFO) and Farah Sami "
    "(Associate Director, Corporate Strategy & IR)",
    "CLHO 2Q2026 results conference call invitation, published on the IR page", IR, "2026-09-08",
    url=f"{IRBASE}/media/swmlqmu5/cleopatra-hospitals-group-2q2026-results-conference-call.pdf",
    fiscal_period="Q2-2026",
    detail="THE CALL WAS YESTERDAY AND ONLY THE INVITATION IS PUBLISHED. CLHO's IR page carries "
           "invitations for the 1Q2025, 3Q2025, 2Q2024, 3Q2024, FY2024 and 2Q2026 calls but NO "
           "transcripts or recordings for any of them. A build run after this sweep should re-check "
           "the IR page for 2Q2026 call materials before striking a number — see the negative "
           "search F51.",
    model_impact="")

# ---------------------------------------------------------------------------
# RING 4 — COMPANY : strategic plans & guidance
# ---------------------------------------------------------------------------
f_pipeline = R.add(
    Ring.COMPANY, "strategic plans & guidance", FindingClass.D,
    "MANAGEMENT HAS GUIDED THE CAPACITY, CAPEX AND RETURN PATH EXPLICITLY. Group operating beds 780 "
    "at end-2025 rising to approximately 1,050 by end-2026 (+35%), with a further 200 beds under "
    "construction at Cleopatra October for delivery in 2027 and 2028. Cleopatra El Tagamoa opened "
    "its fifth floor at end-July 2026 adding c.50 beds and is expected to reach 240 beds by year "
    "end. Cleopatra October operated 80 beds through H1-2026, added a cath lab in July 2026, and "
    "its 200-bed build-to-suit extension takes it to approximately 300. Capital expenditure was 49% "
    "of sales in 2024 and 37% in 2025 and is expected to fall to approximately 10% in 2026. Return "
    "on equity improved from 25.4% in 2022 to 43.5% in 2025 and is expected to exceed 45% in 2026",
    "CLHO H1 2026 Earnings Release, management comment and strategy overview", IR, "2026-09-06",
    url=f"{IRBASE}/media/sufdt2ur/cleopatra-earnings-release-2q2026.pdf",
    fiscal_period="Q2-2026",
    detail="Capex ratios check against the filings: FY2024 additions EGP 2,648,894,145 / revenue "
           "5,420,396,411 = 48.9% (which is also the check that settles the non-footing segment row, "
           "F27); FY2025 additions 2,651,593,225 / 7,227,264,460 = 36.7%. RoE checks: FY2025 net "
           "profit 967,866,317 / average total equity ((3,177,797,400 + 4,040,365,543)/2 = "
           "3,609,081,472) = 26.8% on total equity — the 43.5% figure must be on a different base "
           "(attributable profit over opening attributable equity gives 823,881,689 / 2,899,588,802 "
           "= 28.4%; group profit over opening attributable equity gives 33.4%). THE 43.5% RoE "
           "DEFINITION DOES NOT REPRODUCE FROM THE STATEMENTS on any obvious basis and should not "
           "be repeated in the study without one.",
    model_impact="DRIVER UNLOCK for the capacity leg: beds are a guided, dated, named series and "
                 "the volume build runs on beds x occupancy x cases per bed rather than on a "
                 "revenue growth rate. The capex guidance is corroborated by the audited commitment "
                 "balance (F37). The RoE guidance is NOT reproducible and must not be used as an "
                 "input to any lens.")

f_flash = R.add(
    Ring.COMPANY, "strategic plans & guidance", FindingClass.D,
    "THE H1-2026 RELEASE CARRIES A Q3 TRADING FLASH THAT IS THE FRESHEST NUMBER IN THE FILE. "
    "Revenue reached EGP 878mn in July 2026 (+35% y/y) and EGP 905mn in August 2026 (+42% y/y); "
    "year-to-date consolidated revenue growth reached 30% through August, up from 27% at H1. "
    "Cleopatra El Tagamoa contributed EGP 123mn in July and EGP 134mn in August and, at its current "
    "run rate, is expected to reach annual revenues of at least EGP 1.2bn",
    "CLHO H1 2026 Earnings Release, 'Q3 Flash Performance'", IR, "2026-09-06",
    url=f"{IRBASE}/media/sufdt2ur/cleopatra-earnings-release-2q2026.pdf",
    fiscal_period="Q2-2026",
    detail="July plus August is EGP 1,783mn against EGP 1,938mn for the whole of Q3-2025, so Q3-2026 "
           "is tracking c.+38% on two of three months. CTH's disclosed monthly path is EGP 68mn "
           "March, 81 April, 95 May, 112 June, 123 July, 134 August — a clean, unbroken ramp. The "
           "EGP 1.2bn annualised expectation against an August run-rate of EGP 134mn implies "
           "c.EGP 100mn a month average across a partial year, i.e. it is an FY2027-shape number.",
    model_impact="Sets the FY2026 revenue landing zone directly and is the single most current "
                 "input to the study year. Two months of Q3 actuals plus the H1 actual cover eight "
                 "of twelve months of FY2026, so FY2026 revenue is largely OBSERVED, not forecast — "
                 "build it that way and reserve the forecasting to FY2027 onward.")

f_strategy = R.add(
    Ring.COMPANY, "strategic plans & guidance", FindingClass.S,
    "THE BOARD HAS AN OPEN STRATEGIC REVIEW AIMED AT THE SHARE PRICE. Management states that 'the "
    "Group's current market capitalisation does not yet reflect either this capacity or the value "
    "of the property that houses it', that 'the Board and management are continuing the strategic "
    "review now under way to identify the most effective route to close the gap between the Group's "
    "intrinsic value and its market valuation, and to optimise value for all shareholders', and "
    "that 'the Board may in time consider the merits of a dividend policy'. The stated expansion "
    "criterion across all opportunities is 'a preference for asset-light models requiring minimal "
    "capital expenditure'",
    "CLHO H1 2026 Earnings Release, management comment by Dr Ahmed Ezzeldin, Group CEO", IR,
    "2026-09-06",
    url=f"{IRBASE}/media/sufdt2ur/cleopatra-earnings-release-2q2026.pdf",
    fiscal_period="Q2-2026",
    detail="No form, counterparty, price or timetable is disclosed, and nothing has been filed "
           "beyond this paragraph — see the negative search F59. The 'value of the property' claim "
           "is directly qualified by the fixed-asset note (F32): land at cost is EGP 173mn and the "
           "two newest hospitals sit on land the group does not own and hands back (F38, F39).",
    model_impact="A named, dated, company-official corporate-action possibility with no terms. It "
                 "is NOT a valuation input and must not be capitalised into the central case. Carry "
                 "it as a disclosed, dated overhang or optionality in the risk section, and note "
                 "that the market may already be pricing it — the LTIP charge quadrupled on a "
                 "c.100% rise in market capitalisation over H1-2026 (F55).")

f_capex_pr = R.add(
    Ring.COMPANY, "strategic plans & guidance", FindingClass.C,
    "The 2024 Capital Investment Strategy Update (31 January 2024) set out the programme that is "
    "now completing: c.EGP 2bn of growth capex over 18 months on Sky Hospital phases 1 and 2 in "
    "East Cairo, the Cleopatra October expansion in West Cairo and polyclinic expansion across "
    "Greater Cairo, adding more than 300 beds and over 750 new roles, financed entirely through "
    "internal sources and existing banking lines, and excluding potential acquisitions of operating "
    "hospitals outside Greater Cairo",
    "CLHO press release, '2024 Capital Investment Strategy Update'", IR, "2024-01-31",
    url=f"{IRBASE}/media/y0nfk4tp/chg-press-release-31122024-e.pdf",
    detail="The programme overran the guided figure substantially: actual additions were EGP "
           "2,648,894,145 in FY2024 alone and EGP 2,651,593,225 in FY2025, c.EGP 5.3bn against a "
           "'c.EGP 2bn over 18 months' guide. The funding claim also did not hold in full — gross "
           "loans rose from EGP 488,932,256 at FY2023 to EGP 3,135,813,053 at FY2025. The file name "
           "reads 31122024 while the document is dated 31 January 2024.",
    model_impact="")

# ---------------------------------------------------------------------------
# RING 4 — COMPANY : one-off base-resetting transactions
# ---------------------------------------------------------------------------
f_cth = R.add(
    Ring.COMPANY, "one-off base-resetting transactions", FindingClass.B,
    "CLEOPATRA EL TAGAMOA IS THE BASE CHANGER. Soft-launched December 2025, officially opened 27 "
    "January 2026, inaugurated by the Prime Minister. In FY2025 CHG Sky Hospital carried ZERO "
    "revenue, a loss of EGP 133,926,040, non-current assets of EGP 3,835,639,044, total assets of "
    "EGP 3,957,762,659 and total liabilities of EGP 3,050,968,800, and absorbed EGP 1,745,207,327 "
    "of the group's EGP 2,651,593,225 FY2025 capex. In 2026 it contributed EGP 154mn in Q1 and EGP "
    "291mn in Q2 (12% of group revenue), served over 54,000 cases in five months, moved from a -25% "
    "gross margin and -24% EBITDA margin in Q1 to +10% and +8% in Q2, and reached an 18% EBITDA "
    "margin in the month of June alone",
    "CLHO FY2025 audited consolidated statements note 6 (segment) for the FY2025 figures; CLHO Q1 "
    "2026 and H1 2026 Earnings Releases for the 2026 figures", CO, "2026-09-06",
    url=f"{IRBASE}/media/pj0ldhq3/chc-consolidated-31-dec-2025.pdf",
    is_fs_data=True, fiscal_period="FY2025",
    detail="This is why FY2025 and FY2026 are not comparable and why FY2026 net profit fell 34% on "
           "27% revenue growth. Of the EGP 364mn Q1-to-Q2 group revenue increase, CTH alone was "
           "38%. The FY2025 accounts carry the whole EGP 3.96bn asset with no revenue against it, "
           "which is exactly why the FY2025 return and asset-turn ratios cannot be projected "
           "forward.",
    model_impact="BASE CHANGER, MODELLED AS AN EXPLICIT DATED EVENT AND DUAL-FRAMED. Build CTH as "
                 "its own line — beds ramping to 240, occupancy, cases, ARP, cost per case, the 2% "
                 "revenue share (F38) and its own depreciation once projects in progress transfer "
                 "(F32) — and show the group with and without it. Never smooth it into a group "
                 "growth or margin glide.")

f_coh_reset = R.add(
    Ring.COMPANY, "one-off base-resetting transactions", FindingClass.B,
    "CLEOPATRA OCTOBER WAS RE-CONTRACTED IN FEBRUARY 2025 AND THAT RESETS ITS ECONOMICS. The "
    "31 October 2022 usufruct was terminated and replaced by a 25-year partnership; CHG paid EGP "
    "250mn up front, forfeited a EGP 36mn earlier advance, and the counterparty took on building "
    "and finishing the 200-bed extension while CHG equips and operates. Announced 16 February 2025 "
    "as a build-to-suit lease taking capacity to up to 300 beds",
    "CLHO press release 'Cleopatra Hospitals Group Secures Major Extension for Cleopatra October "
    "Hospital' (16 Feb 2025); CLHO H1-2026 reviewed statements note 6 for the contract terms",
    IR, "2025-02-16",
    url=f"{IRBASE}/media/dthjw3hu/chg-press-release-16022025-en-final.pdf",
    fiscal_period="FY2025",
    detail="The press release does not disclose the EGP 250mn payment, the EGP 36mn forfeiture or "
           "the 8%/9%/10% revenue share — those come only from the reviewed statements (F39). A "
           "study built from the press releases alone would model this as a free 200-bed "
           "expansion.",
    model_impact="BASE CHANGER, DUAL-FRAMED. FY2025 Cleopatra October carries an EGP 286mn "
                 "capitalised advance and an EGP 60,597,347 loss despite EGP 92.4mn of gross "
                 "profit. Model the 200-bed extension as a dated step in 2026-27 with its own "
                 "occupancy ramp, its own equipping capex, and the 8%-to-10% revenue share on the "
                 "FULL complex revenue once the advance is consumed.")

f_ltip = R.add(
    Ring.COMPANY, "one-off base-resetting transactions", FindingClass.B,
    "THE LTIP CHARGE IS A SHARE-PRICE DERIVATIVE INSIDE THE INCOME STATEMENT AND IT QUADRUPLED. "
    "The charge recognised in H1-2026 was EGP 202mn against EGP 60mn in H1-2025, and the release "
    "states it 'rose in line with the scheme's mark-to-market mechanics, reflecting the increase in "
    "CHG's market capitalization over the period', which grew by approximately 100%. The current "
    "LTIP liability on the balance sheet went from EGP 73,961,551 at FY2025 to EGP 116,599,651 at "
    "30 June 2026, and the equity-carried employee-incentive balance from EGP 32,699,496 to EGP "
    "66,661,047",
    "CLHO H1 2026 Earnings Release, G&A discussion; CLHO H1-2026 reviewed statements, statement of "
    "changes in equity and note 13", CO, "2026-09-06",
    url=f"{IRBASE}/media/lu2hhgwg/chc-consolidated-fs-30-june-2026.pdf",
    is_fs_data=True, fiscal_period="Q2-2026",
    detail="The cash-flow statement confirms the size: 'Share-based payments financial liabilities' "
           "of EGP 201.9mn in H1-2026 against EGP 60.0mn in H1-2025. The FY2025 accounts value the "
           "three-year programme at EGP 540,039,928 while stating estimated annual dues of EGP "
           "106,661,048 — those two are internally inconsistent (540,039,928 / 3 = 180,013,309) and "
           "the note should not be relied on for the forward charge without clarification.",
    model_impact="BASE CHANGER AND A MODELLING TRAP. The LTIP is a NEGATIVE FEEDBACK from the share "
                 "price into earnings: a higher price raises the charge, which lowers reported "
                 "profit, which lowers any earnings multiple applied to it. It must be stripped "
                 "from the operating cost base and modelled separately as a function of the "
                 "modelled equity value, or the valuation becomes circular. It is also the single "
                 "largest driver of the FY2026 net-profit fall after interest.")

# ---------------------------------------------------------------------------
# RING 4 — COMPANY : ownership / stake changes
# ---------------------------------------------------------------------------
f_owners = R.add(
    Ring.COMPANY, "ownership / stake changes (named-transaction rule)", FindingClass.D,
    "THE AUDITED SHAREHOLDER REGISTER, NOT A SUMMARY. At 31 December 2025: Care Health Care 32.01% "
    "(464,000,000 shares, EGP 232,000,000 nominal); MCI Capital Health Care 30.68% (444,688,538, "
    "EGP 222,344,269); Goldman Sachs International 5.10% (73,971,205, EGP 36,985,603); other "
    "shareholders 32.21% (466,790,341, EGP 233,395,170). Total 1,449,450,084 shares, EGP "
    "724,725,042 paid-up capital, par EGP 0.50. At 31 December 2024 the same three held 32.10%, "
    "30.77% and 5.12% of 1,445,434,202 shares",
    "CLHO FY2025 audited consolidated statements, note 21 'Share capital'", CO, "2026-03-16",
    url=f"{IRBASE}/media/pj0ldhq3/chc-consolidated-31-dec-2025.pdf",
    is_fs_data=True, fiscal_period="FY2025",
    detail="RE-ADDED: share counts sum to 1,449,450,084 and each percentage reproduces to two "
           "decimals; 1,449,450,084 x EGP 0.50 = 724,725,042. NO NAMED HOLDER CHANGED between "
           "FY2024 and FY2025 — the small percentage moves are pure dilution from the 5,664,458-"
           "share employee issue. The H1-2026 release's shareholder pie (Care Healthcare 32%, MCI "
           "Healthcare Partners 31%, free float 37%) is the same register with Goldman Sachs "
           "counted inside free float: 5.10% + 32.21% = 37.31%.",
    model_impact="Fixes the share count at 1,449,450,084 and the free float at 37.3% for the "
                 "per-share bridge and any liquidity discussion. Control is 62.7% in two hands, "
                 "which is the structural fact behind the strategic review (F60).")

f_csh = R.add(
    Ring.COMPANY, "ownership / stake changes (named-transaction rule)", FindingClass.S,
    "NAMED TRANSACTION, SEARCHED BY NAME AND STILL OPEN: on 5 May 2025 CHG announced it had secured "
    "all necessary regulatory approvals to increase its ownership in CAIRO SPECIALIZED HOSPITAL "
    "from 57% to UP TO 90%, stating that 'a final value has not yet been determined' and that it is "
    "committed to Article 44 of the Listing and Delisting Rules. As at 30 June 2026 the reviewed "
    "statements still show 57.01%, so the transaction has NOT completed",
    "CLHO press release, 'Cleopatra Hospitals Group Secures Regulatory Approvals to Acquire up to "
    "90% in Cairo Specialized Hospital' (5 May 2025); CLHO H1-2026 reviewed statements, subsidiary "
    "schedule at 30 June 2026", CO, "2026-09-03",
    url=f"{IRBASE}/media/20kb3bbl/chg-press-release-05052025-en-final.pdf",
    fiscal_period="Q2-2026",
    detail="Searched by name, not estimated: query 'Cairo Specialized Hospital Cleopatra "
           "acquisition 90% stake 2026 completed valuation FRA approval'. Nothing was found "
           "recording completion or a price, and fra.gov.eg could not be reached to inspect the "
           "file (curl 35, connection reset by peer). The press release also discloses CSH's "
           "operating scale: c.190 beds, nearly 300,000 patients annually, revenue CAGR 37% and net "
           "profit CAGR 47% over the prior three years.",
    model_impact="A dated, named, PENDING transaction over the asset that carries 96% of group "
                 "minority interest. Model it as an OPTION, not a certainty: the base case "
                 "consolidates CSH at 57.01% with a 42.99% minority throughout, and the completion "
                 "case is a separate dual-framed run with the incremental 33 percentage points "
                 "bought at a stated assumed price. Because 'a final value has not yet been "
                 "determined', the price is an assumption and must be labelled one and sensitised.")

f_neg_stake = R.add_negative(
    Ring.COMPANY, "ownership / stake changes (named-transaction rule)",
    "searched: 'Cleopatra Hospitals CLHO strategic review 2026 stake sale Care Healthcare MCI "
    "offer'; 'Cleopatra Hospitals Group 2026 news EGX disclosure board strategic review value gap'; "
    "and a full read of the News & Disclosures section of cleopatrahospitals.com/en/investors/. "
    "NOTHING FOUND: no 2026 change in the Care Health Care 32.01%, MCI Capital Health Care 30.68% "
    "or Goldman Sachs International 5.10% holdings, no tender offer, no mandatory offer, no block "
    "trade and no disclosed counterparty to the strategic review. The only stake transactions on "
    "the record are MCI Capital's December 2021 acquisition of c.26% for EGP 2.1bn and the pending "
    "Cairo Specialized transaction in F58. egx.com.eg (curl 52, empty reply) and fra.gov.eg (curl "
    "35, connection reset) could not be searched at source",
    SWEEP_DATE)

# ---------------------------------------------------------------------------
# RING 4 — COMPANY : management & capital actions
# ---------------------------------------------------------------------------
f_capital = R.add(
    Ring.COMPANY, "management & capital actions", FindingClass.D,
    "TWO CAPITAL ACTIONS IN 2025, BOTH NON-CASH AND BOTH FOR THE EMPLOYEE SCHEME. On 17 July 2025 "
    "the General Assembly approved a REDUCTION of issued capital by cancelling 1,648,577 treasury "
    "shares at par, EGP 824,288, taking issued capital to EGP 721,892,813. On 8 September 2025 the "
    "General Assembly approved an INCREASE of EGP 2,832,229, being 5,664,458 shares at EGP 0.50 "
    "par, funded from retained earnings and allocated in full to the Employees Incentive Plan for "
    "employees, managers and executive board members. Issued capital ended the year at EGP "
    "724,725,042 over 1,449,450,084 shares, with treasury shares at nil",
    "CLHO FY2025 audited consolidated statements, notes 21 'Share capital' and 38 'Treasury "
    "shares', and the consolidated statement of changes in equity", CO, "2026-03-16",
    url=f"{IRBASE}/media/pj0ldhq3/chc-consolidated-31-dec-2025.pdf",
    is_fs_data=True, fiscal_period="FY2025",
    detail="721,892,813 + 2,832,229 = 724,725,042 exactly. The share count reconciles to within one "
           "share (1,445,434,202 - 1,648,577 + 5,664,458 = 1,449,450,083 against a stated "
           "1,449,450,084), a rounding on the EGP 0.50 par. Weighted average shares for FY2025 EPS "
           "were 1,441,509,083 basic and 1,443,807,866 diluted.",
    model_impact="DRIVER UNLOCK for the per-share bridge: 1,449,450,084 shares outstanding, no "
                 "treasury, and a running annual dilution of c.0.4% from the employee scheme that "
                 "the model should carry forward rather than holding the count flat.")

f_cfo = R.add(
    Ring.COMPANY, "management & capital actions", FindingClass.S,
    "THREE GROUP CFOs SIGNED FOUR CONSECUTIVE AUDITED YEARS. FY2022 was signed by Mr Ahmed Gamal as "
    "Group CFO; FY2023 and FY2024 by Mr Adel Elmistikawi / Adel Al-Mestakawi as Chief Financial "
    "Officer; FY2025, Q1-2026 and H1-2026 by Mr Amr Al Rashid as Chief Financial Officer. Dr Ahmed "
    "Ezz El Dien Mahmoud has signed as CEO and Managing Director throughout, and Mr Ahmed Adel Badr "
    "El Dien as Non-Executive Chairman throughout",
    "Signature blocks of CLHO's audited consolidated statements FY2022, FY2023, FY2024, FY2025 and "
    "of the Q1-2026 and H1-2026 reviewed interims, read off the rendered pages", CO, "2026-09-03",
    url=f"{IRBASE}/media/pj0ldhq3/chc-consolidated-31-dec-2025.pdf",
    is_fs_data=True, fiscal_period="FY2025",
    detail="Two CFO changes in four years alongside continuity in the CEO and Chair. This is not "
           "flagged anywhere in the IR materials and is visible only from the signature blocks. It "
           "sits alongside the restatement in F21, the presentation reclass in F22, the "
           "non-footing segment row in F27, the mislabelled interim EPS deduction in F34 and the "
           "swapped balance-sheet labels in F41.",
    model_impact="Raises the required standard of proof on every reported figure rather than "
                 "changing any driver. It is the reason this sweep re-added every column against "
                 "the filings' own subtotals rather than trusting an extraction, and the reason "
                 "the study should reconcile any release figure to the statement before using it.")

f_eip = R.add(
    Ring.COMPANY, "management & capital actions", FindingClass.S,
    "THE EMPLOYEE INCENTIVE SCHEME IS PRICE-LINKED AND ITS OWN NOTE IS INTERNALLY INCONSISTENT. The "
    "balance is computed as the difference between the weighted average price for the month before "
    "grant and the month before maturity one year later, multiplied by units granted and divided by "
    "the maturity price. The FY2025 note states an estimated current value for the three-year "
    "incentive and bonus programme of EGP 540,039,928, estimated dues per year of EGP 106,661,048, "
    "and a value recorded in equity of EGP 32,699,496",
    "CLHO FY2025 audited consolidated statements, note 22 'Employee reward plan'", CO, "2026-03-16",
    url=f"{IRBASE}/media/pj0ldhq3/chc-consolidated-31-dec-2025.pdf",
    is_fs_data=True, fiscal_period="FY2025",
    detail="EGP 540,039,928 over three years is EGP 180,013,309 a year, not the stated EGP "
           "106,661,048 — the note does not reconcile with itself. The H1-2026 charge alone was EGP "
           "202mn (F55), already above the annual figure the note states, which is consistent with "
           "the mark-to-market mechanic and inconsistent with the note's own estimate.",
    model_impact="Do not use the note's EGP 106,661,048 as the forward LTIP charge. Model the LTIP "
                 "from the disclosed mechanic against the modelled share price, and disclose that "
                 "the company's own estimate is both internally inconsistent and already exceeded.")

# ---------------------------------------------------------------------------
# RING 4 — COMPANY : listing and price series (free-form; NO beta resolved)
# ---------------------------------------------------------------------------
f_listing = R.add(
    Ring.COMPANY, "listing, exchange and price series", FindingClass.C,
    "CLHO trades on the EGYPTIAN EXCHANGE (EGX) as CLHO.CA, ISIN EGS729J1C018, listed June 2016, "
    "quoted in EGP, 1,449,450,084 shares outstanding. NO second listing, GDR or depositary line was "
    "found. The repository holds engine/raw_ohlc/EG/CLHO.csv: 2,499 daily rows from 14 April 2016 "
    "to 23 August 2026, last close EGP 17.71 on 23 Aug 2026, range EGP 0.07 to 18.32. The "
    "registered index for EG/EGX in engine/raw_indices/EG/EGX30.csv runs to 8 September 2026",
    "CLHO H1 2026 Earnings Release shareholder-information block for the listing facts; "
    "engine/raw_ohlc/EG/CLHO.csv and engine/raw_indices/EG/EGX30.csv for the series", PMD,
    "2026-09-06",
    detail="NO BETA IS RESOLVED HERE AND NO REGRESSOR IS CHOSEN — that ruling is not this sweep's "
           "to take. Recorded for whoever does take it: (1) the price series is 17 calendar days "
           "STALE against this sweep date while the EGX30 series is current to 8 Sep, so the two "
           "do not currently span the same window; (2) the series carries EGP 0.07 prints in April "
           "2016 with a -98.66% change on 14 Apr 2016, before the stated June-2016 listing, which "
           "a Step 0.0 data-quality run must resolve before the series is used for anything; (3) "
           "the currency and magnitude are consistent with an EGX-filed EGP line, so there is no "
           "dual-listing ambiguity of the Orascom Construction kind. Market capitalisation at the "
           "EGP 17.71 close is EGP 25.67bn.",
    model_impact="")

# ---------------------------------------------------------------------------
# RING 4 — COMPANY : dated negative searches
# ---------------------------------------------------------------------------
f_neg_payer = R.add_negative(
    Ring.COMPANY, "regular disclosures",
    "PAYER MIX. searched: case-insensitive regex 'payor mix|payer mix|% of revenue.*insur|"
    "insurance.*% of|cash pay|self-pay|contractual (patients|clients)|corporate account' across "
    "every CLHO document retrieved — audited statements FY2022-FY2025, reviewed interims Q1 and "
    "Q2-2026, earnings releases FY2022/FY2023/FY2024/FY2025/Q1-2026/H1-2026, IR presentations "
    "FY2024/FY2025/Q1-2026, and all seven press releases. NOTHING FOUND. CLHO discloses NO split "
    "of revenue between cash-pay, private insurance, corporate contracts and state schemes "
    "anywhere. The only payer references are qualitative: 'Payor Recognition' as a Centre of "
    "Excellence pillar in the FY2025 presentation, and the Petroleum-sector Fund described as "
    "'a key payor' covering over 1 million people in the December 2022 Suez release. THIS IS THE "
    "LARGEST DISCLOSURE GAP ON THE NAME and it is what makes the UHIA tariff exposure in F09 "
    "unmodellable bottom-up",
    SWEEP_DATE)

f_neg_occ = R.add_negative(
    Ring.COMPANY, "regular disclosures",
    "BED OCCUPANCY AND LENGTH OF STAY. searched: 'occupancy (rate|level|of)|bed occupancy|"
    "utili[sz]ation rate|ALOS|average length of stay' across the same complete document set. NO "
    "OCCUPANCY PERCENTAGE, NO AVERAGE LENGTH OF STAY AND NO BED-DAY COUNT IS DISCLOSED IN ANY "
    "PERIOD. The only references are qualitative — 'steadily increasing occupancy levels' and "
    "'accelerating occupancy levels across all service lines' in the Q1-2026 release and "
    "presentation, and 'despite very high occupancy and utilization levels' for Cleopatra Hospital "
    "in the FY2025 release. Bed counts ARE disclosed (F51, F52) and inpatient case counts ARE "
    "disclosed (F44, F47), so occupancy can be DERIVED as cases per bed, but the length-of-stay "
    "term needed to convert that into a true occupancy percentage is not disclosed",
    SWEEP_DATE)

f_neg_head = R.add_negative(
    Ring.COMPANY, "regular disclosures",
    "HEADCOUNT AND STAFFING. searched: 'number of employees|headcount|[0-9]{4,} (employees|staff)|"
    "employees at (31|the end)' across the complete document set. NO EMPLOYEE, DOCTOR, NURSE OR "
    "BED-TO-STAFF COUNT IS DISCLOSED IN ANY PERIOD. Employment costs ARE disclosed in full — EGP "
    "1,045,589,981 in cost of revenue plus EGP 606,746,595 in G&A for FY2025 (F30, F31), and "
    "doctors' fees separately at EGP 900,546,805 — but there is no denominator, so cost per "
    "employee cannot be built and the staffing step-up for c.270 new beds in 2026 cannot be checked "
    "against a headcount plan. The only related figures are forward-looking job-creation claims: "
    "'over 750 new roles' in the 2024 capital-strategy release and '2,000+ New Jobs Created (once "
    "fully operational)' for Cleopatra El Tagamoa in the FY2025 presentation",
    SWEEP_DATE)

f_neg_call = R.add_negative(
    Ring.COMPANY, "IR communications (calls, presentations, releases)",
    "2Q2026 CALL MATERIALS AND A Q2-2026 IR PRESENTATION. searched: the full document listing at "
    "cleopatrahospitals.com/en/investors/ on 9 Sep 2026, one day after the 8 Sep 2026 2Q26 results "
    "call. NEITHER EXISTS YET. The Investor Relations Presentations list ends at Q1 2026 "
    "(chg-irp-1q2026.pdf) — there is no FY/H1-2026 presentation — and the News & Disclosures list "
    "carries the 2Q2026 call INVITATION but no transcript, recording or slide deck for it, nor for "
    "any of the 1Q2025, 3Q2025, FY2024, 2Q2024 or 3Q2024 calls whose invitations are also posted. "
    "A build should re-check the IR page before striking a number: a Q2-2026 presentation would "
    "carry the bed and occupancy detail the release does not",
    SWEEP_DATE)

f_neg_saudi = R.add_negative(
    Ring.COMPANY, "one-off base-resetting transactions",
    "SAUDI JOINT VENTURE STATUS. searched: 'Mumtada' and 'Saudi' across every CLHO document "
    "retrieved, plus the FY2025 subsidiary schedule, the segment note and the associates note. The "
    "28 April 2024 press release announced CHG as operating partner for a 200-bed rehabilitation "
    "and long-term post-acute facility in Riyadh with Mumtada Medical Company, asset-light, "
    "'expected to commence operations in late 2024', citing an 18,000-bed / USD 14bn Saudi gap by "
    "2030. NO SUBSEQUENT MENTION EXISTS ANYWHERE: not in the FY2024 or FY2025 audited statements, "
    "not in the FY2024, FY2025 or Q1-2026 presentations, not in any 2025 or 2026 earnings release, "
    "and not in the subsidiary or associate schedules. Investments in associates are EGP 18,585,651 "
    "and flat since FY2025. The venture contributes nothing to any disclosed number",
    SWEEP_DATE)

f_neg_medtour = R.add_negative(
    Ring.COMPANY, "strategic plans & guidance",
    "MEDICAL TOURISM REVENUE. searched: 'medical tourism|medical value|international patients|"
    "inbound patients' across the complete CLHO document set. NO MEDICAL-TOURISM REVENUE, PATIENT "
    "COUNT OR TARGET IS DISCLOSED. CLHO runs a /en/medicaltourism/ page and the FY2025 presentation "
    "describes Cleopatra October as intended to be 'a hub for medical value tourism for West "
    "Cairo', but no figure is attached in any period. The segment cannot be sized from company "
    "disclosure",
    SWEEP_DATE)

f_neg_guid = R.add_negative(
    Ring.COMPANY, "strategic plans & guidance",
    "NUMERIC FINANCIAL GUIDANCE. searched: 'guidance|guide to|we expect revenue of|target revenue|"
    "outlook for (2026|2027)|EBITDA target|margin target' across the FY2024, FY2025, Q1-2026 and "
    "H1-2026 releases and presentations. CLHO ISSUES NO REVENUE, EBITDA OR EARNINGS GUIDANCE. What "
    "it does issue is narrower and is captured separately: a bed count (780 -> c.1,050 -> +200), a "
    "capex ratio (49% -> 37% -> c.10% of sales), an RoE expectation (>45% in 2026, on a basis that "
    "does not reproduce from the statements), a Cleopatra El Tagamoa annual revenue expectation of "
    "at least EGP 1.2bn, and two months of Q3-2026 actual revenue. Nothing at group revenue or "
    "profit level",
    SWEEP_DATE)

f_neg_tariff = R.add_negative(
    Ring.COUNTRY, "regulatory environment (regulator, caps, tariffs, tax/subsidy)",
    "PRIVATE HOSPITAL PRICE CONTROLS. searched: 'Egypt private hospital tariff cap|price control "
    "private healthcare Egypt 2026|medical fee regulation Egypt|hospital pricing cap Ministry of "
    "Health' together with the complete CLHO document set. NO PRICE CAP, TARIFF CEILING OR FEE "
    "SCHEDULE BINDING ON PRIVATE, CASH-PAY OR PRIVATELY-INSURED HOSPITAL CARE IN EGYPT WAS FOUND, "
    "and CLHO discloses none. CLHO's ability to run an annual across-the-board price reset (F14) "
    "and to take physiotherapy ARP up 63% in a single half-year is consistent with an unregulated "
    "private tariff. Two regulated perimeters DO exist and are separate: UHIA-contracted care, "
    "where the authority sets the tariff (F09), and drug prices, overhauled on 8 Sep 2026 (F03). "
    "Neither currently binds CLHO's disclosed revenue because it discloses no UHIA exposure (F48)",
    SWEEP_DATE)

f_neg_gahar = R.add_negative(
    Ring.COUNTRY, "regulatory environment (regulator, caps, tariffs, tax/subsidy)",
    "GAHAR / UHIA ACCREDITATION AND CONTRACTING STATUS. searched: 'GAHAR|accreditation|accredited|"
    "JCI|universal health insurance|UHIA' across the complete CLHO document set. NOTHING FOUND for "
    "GAHAR, UHIA or universal health insurance in any CLHO document, and no accreditation of any "
    "kind is claimed for any CLHO facility in any period. GAHAR accreditation is a precondition of "
    "UHIA contracting (F09), and named competitors do publicise JCI accreditation (F16), so this is "
    "an absence with a competitive as well as a regulatory reading. fra.gov.eg (curl 35, connection "
    "reset) and uhia.gov.eg (curl 60, SSL certificate problem: unable to get local issuer "
    "certificate) could not be searched at source",
    SWEEP_DATE)

f_neg_subst = R.add_negative(
    Ring.INDUSTRY, "technology substitution",
    "SUBSTITUTION OF CLHO'S OWN ACUTE BASE. searched: 'Egypt telemedicine AI diagnostics day "
    "surgery outpatient shift substitution hospital inpatient demand 2026' and, across the complete "
    "CLHO document set, 'telemedicine|telehealth|remote consultation|virtual care|day case|"
    "ambulatory surgery'. NO EVIDENCE FOUND of substitution away from inpatient admission, surgical "
    "procedures or catheterisation — the lines that are 41% of CLHO's revenue — inside the forecast "
    "window, and CLHO itself makes no telemedicine or virtual-care disclosure of any kind. What "
    "does exist in Egypt is digitisation of primary care, labs, radiology and outpatient clinics "
    "under UHIS, and an AI-diagnostics market of c.USD 31mn, which touches CLHO's lower-ARP lines "
    "only (F17)",
    SWEEP_DATE)

f_neg_compprice = R.add_negative(
    Ring.INDUSTRY, "competitor capacity / price moves (named)",
    "COMPETITOR PRICING. searched: 'Egypt private hospital prices 2026 Alameda Andalusia Saudi "
    "German tariff increase' and each named competitor by name against 'price|tariff|fee "
    "increase'. NO PUBLISHED PRICE OR TARIFF MOVE BY ANY NAMED EGYPTIAN PRIVATE HOSPITAL OPERATOR "
    "WAS FOUND. Egyptian private hospitals do not publish tariffs and none of the named competitors "
    "is listed, so there is no filing obligation. Competitor CAPACITY moves are well documented and "
    "are captured in F16 and F18; competitor PRICE moves are not observable, so the ARP path in the "
    "model is set from CLHO's own disclosed ARP history and the inflation path, with no competitive "
    "price-response term",
    SWEEP_DATE)

# ===========================================================================
# DRIVER GATE TABLE — every row earns its mode
# ===========================================================================
R.add_driver(
    "Inpatient admissions (cases) x average revenue per inpatient (EGP)",
    DriverMode.BOTTOM_UP,
    "Both legs are separately disclosed by the company for four years and reconcile to the audited "
    "revenue note. Volumes FY2022 55,188 -> FY2023 60,322 -> FY2024 66,859 -> FY2025 75,107 -> "
    "H1-2026 39,558; ARP FY2024 EGP 18,446 -> FY2025 21,266 -> H1-2026 25,389. Audited inpatient "
    "revenue (residency and medical supervision) EGP 1,233,265,771 FY2024 and 1,583,244,138 FY2025 "
    "reproduces from volume x ARP. Projected in BOTH legs: volume from beds x utilisation, ARP "
    "against the inflation path.",
    [f_revnote, f_er25, f_er_h1, f_hist_vols, f_price])

R.add_driver(
    "Surgical procedures (count) x average revenue per procedure (EGP)",
    DriverMode.BOTTOM_UP,
    "Disclosed at both patient and procedure level with ARP for four years: procedures FY2022 "
    "37,552 -> FY2023 39,484 -> FY2024 42,558 -> FY2025 43,415 -> H1-2026 21,049; ARP FY2024 EGP "
    "24,951 -> FY2025 30,086 -> H1-2026 34,517. Ties to audited surgeries revenue of EGP "
    "1,100,684,402 FY2024 and 1,359,734,909 FY2025. Volume growth has stalled (+2% FY2025, -0.4% "
    "Q1-2026) while ARP runs +16%, so the two legs must be projected separately or the line is "
    "mis-forecast.",
    [f_revnote, f_er25, f_er_q1, f_er_h1, f_hist_vols])

R.add_driver(
    "Outpatient consultations (visits) x average revenue per visit (EGP)",
    DriverMode.BOTTOM_UP,
    "Volumes FY2022 843,643 -> FY2023 939,383 -> FY2024 1,068,211 -> FY2025 1,204,807 -> H1-2026 "
    "643,906; ARP FY2024 EGP 457 -> FY2025 506 -> H1-2026 544. Ties to audited outpatient clinics "
    "revenue of EGP 497,640,710 FY2024 and 667,565,609 FY2025. This is also the line the polyclinic "
    "network feeds and the line most exposed to the digital-health shift in F17.",
    [f_revnote, f_er25, f_er_h1, f_hist_vols])

R.add_driver(
    "Emergency room visits x average revenue per visit (EGP)",
    DriverMode.BOTTOM_UP,
    "Volumes FY2024 174,597 -> FY2025 192,620 -> H1-2026 99,957; ARP EGP 1,043 -> 1,348 -> 1,505. "
    "Ties to audited emergency revenue of EGP 182,107,126 FY2024 and 266,014,679 FY2025. The +29% "
    "FY2025 ARP step is the largest of the volume-disclosed lines and must be treated as a level "
    "reset, not a trend.",
    [f_revnote, f_er25, f_er_h1])

R.add_driver(
    "Cardiac catheterisations x average revenue per catheterisation (EGP)",
    DriverMode.BOTTOM_UP,
    "Volumes FY2022 4,588 -> FY2023 5,337 -> FY2024 5,510 -> FY2025 6,089 -> H1-2026 3,252; ARP "
    "FY2024 EGP 71,124 -> FY2025 78,253 -> H1-2026 85,522. Ties to audited cardiac catheterisation "
    "revenue of EGP 391,893,335 FY2024 and 467,408,288 FY2025. New cath labs at Suez (2025) and "
    "Cleopatra October (July 2026) are named, dated capacity additions to this line.",
    [f_revnote, f_er25, f_er_h1, f_hist_vols, f_pipeline])

R.add_driver(
    "Laboratory tests and radiology tests (volumes) x revenue per test (EGP)",
    DriverMode.BOTTOM_UP,
    "Volumes are disclosed for both lines (laboratory 1,846k -> 2,182k, radiology 325k -> 385k for "
    "FY2024 -> FY2025) against audited revenue of EGP 509,020,271 -> 786,970,168 and 335,664,111 -> "
    "525,213,413. Revenue per test is derived rather than printed, so the level is built from the "
    "audited revenue divided by the disclosed volume and both legs are then projected. Diagnostics "
    "were 18% of FY2025 revenue and grew fastest of any disclosed line.",
    [f_revnote, f_er25])

R.add_driver(
    "Pharmacy, physiotherapy, oncology, dental, cardiac tests, fluoroscopes and other divisions "
    "(revenue lines with no disclosed volume)",
    DriverMode.BOTTOM_UP,
    "No volume is disclosed for these seven lines, so the build DROPS A LEVEL and says so: they are "
    "modelled as audited revenue levels growing on the network's case growth and the ARP inflation "
    "path, not as volume x price. They are EGP 1,028,506,261 of FY2025 revenue (14.2%) and the "
    "coarser treatment is FLAGGED rather than passed over. The mode is still bottom-up because the "
    "audited revenue note gives each line separately for four years.",
    [f_revnote, f_er25])

R.add_driver(
    "Service charge revenue (surcharge on all other lines)",
    DriverMode.BOTTOM_UP,
    "The audited note states service charge is NOT a separate performance obligation but a "
    "fixed-percentage surcharge applied to every revenue stream except medicine sales. It is "
    "therefore modelled as a percentage of the other lines: EGP 542,606,995 FY2025 over "
    "(7,227,264,460 - 542,606,995 - 501,505,451 pharmacy) = 8.8%. Growing it independently would "
    "double-count.",
    [f_revnote])

R.add_driver(
    "Operating beds and the per-bed occupancy ramp (Cleopatra El Tagamoa and Cleopatra October)",
    DriverMode.BOTTOM_UP,
    "Bed counts are disclosed and dated: group 780 at end-2025 to c.1,050 at end-2026 plus 200 in "
    "2027-28; Cleopatra El Tagamoa to 240 by end-2026 with a fifth floor added end-July 2026; "
    "Cleopatra October 36 -> 42 -> 45 -> 68 -> 80 -> 280. The ramp function is calibrated on "
    "Cleopatra October's own four-year history of beds against revenue, gross profit, EBITDA and "
    "cases at the same facility. USE THE H1-2026 OPERATING-BED SERIES, NOT the FY2025 "
    "presentation's 1,000, and state why (F51).",
    [f_pipeline, f_irp25, f_beds_conflict, f_cth])

R.add_driver(
    "Medical and pharmaceutical supplies cost per case (EGP)",
    DriverMode.BOTTOM_UP,
    "The audited cost-of-revenue note discloses the line separately for four years (EGP "
    "1,650,595,778 FY2025, 1,187,422,589 FY2024) and cases served is disclosed (1,472,534 FY2025), "
    "giving EGP 1,121 per case. The company also discloses it quarterly as a percentage of revenue "
    "(21.5% Q1-2026, 21.2% Q2-2026), which is the cross-check. Projected against the Egyptian drug-"
    "pricing and import-cost path.",
    [f_cogs, f_supp, f_er_h1, f_er25])

R.add_driver(
    "Doctors' fees",
    DriverMode.BOTTOM_UP,
    "Disclosed separately in the audited cost note (EGP 900,546,805 FY2025, 753,129,443 FY2024) and "
    "quarterly as 13.0% of revenue in both Q1 and Q2-2026. Modelled as a percentage of the "
    "procedure-bearing revenue lines it attaches to, which is what makes it move with case mix "
    "rather than with total revenue.",
    [f_cogs, f_er_h1])

R.add_driver(
    "Salaries, wages and benefits (cost of revenue and G&A)",
    DriverMode.BOTTOM_UP,
    "Disclosed separately in both the cost note (EGP 1,045,589,981 FY2025) and the G&A note (EGP "
    "606,746,595 FY2025), and quarterly as a percentage of revenue (17.8% Q1-2026 falling to 16.4% "
    "Q2-2026 in cost of revenue). Stepped with beds opened rather than grown with revenue. THE GAP "
    "IS FLAGGED: no headcount is disclosed in any period, so cost per employee cannot be built and "
    "the staffing step for c.270 new beds cannot be checked against a plan.",
    [f_cogs, f_ga, f_neg_head, f_er_h1])

R.add_driver(
    "Gross margin and adjusted EBITDA margin",
    DriverMode.BOTTOM_UP,
    "OUTPUTS, NOT INPUTS. The filings disclose eleven cost-of-revenue lines and eleven G&A lines by "
    "nature for four years, plus case volumes, so every margin in the model falls out of revenue "
    "per unit less cost per unit. Setting a gross or contribution margin directly would be a QC "
    "FAIL on this name. Adjusted EBITDA is additionally a non-IFRS measure and is RECONSTRUCTED "
    "from the statutory lines rather than taken from the release: FY2025 operating profit "
    "1,490,050,629 + depreciation and amortisation 254,182,221 + expected credit losses "
    "111,738,639 + other expenses 43,189,697 + acquisition consulting 330,000 less other income "
    "15,840,137 = EGP 1,883,651,049 against a reported EGP 2,137mn. THE EGP 253mn RESIDUAL IS THE "
    "LTIP-PLUS-PRE-OPERATING ADD-BACK, WHICH IS NOT SEPARATELY DISCLOSED FOR FY2025 — only the "
    "H1-2026 (EGP 202mn) and H1-2025 (EGP 60mn) charges are. The residual must be resolved before "
    "the company's adjusted EBITDA is used in any lens; until it is, the reconstructed figure is "
    "the one the model carries.",
    [f_cogs, f_ga, f_revnote, f_er25, f_er_h1])

R.add_driver(
    "Cleopatra El Tagamoa revenue share (2% / 3% / 4% of its own revenue)",
    DriverMode.BOTTOM_UP,
    "Contractual and stepped, disclosed in the reviewed statements: 2% of total annual revenue in "
    "operating years 1-2, 3% from year 3 to 6, 4% from year 7 to the end of a 27-year term running "
    "from 29 December 2021. Modelled on CTH revenue with the step dates, and the terminal value is "
    "capped at the contract end.",
    [f_cth_contract, f_cth])

R.add_driver(
    "Cleopatra October revenue share (8% / 9% / 10%) and the EGP 250mn advance",
    DriverMode.BOTTOM_UP,
    "Contractual and stepped, disclosed in the reviewed statements: 8% of total revenue of the "
    "Haven Medical Complex in years 1-5, 9% in years 5-6, 10% thereafter, over 25 years from the "
    "operating-licence date, payable in cash only after the EGP 250mn advance is fully consumed. "
    "The advance balance rolls exactly (286,000,000 -> 250,336,106 -> 239,389,674). FLAGGED: "
    "H1-2026 consumption of EGP 10,226,432 implies c.3.9% rather than 8% of estimated Cleopatra "
    "October H1 revenue, so the licence-date trigger must be resolved before the rate is applied.",
    [f_coh_contract, f_irp25])

R.add_driver(
    "Cost of debt (Kd) and the debt amortisation schedule",
    DriverMode.BOTTOM_UP,
    "Not estimated: every facility is contractually priced off the published CBE lending rate plus "
    "a disclosed margin (KFH +0.65%, Nile Badrawy +0.80%, CIB +0.05% then +0.09%), the book is "
    "100% EGP, and the repayment schedule is printed instalment by instalment with the CIB grace "
    "period ending 30 June 2026 and 27 quarterly instalments running from 30 September 2026 to "
    "31 December 2032. Kd glides on the CBE path, not on an assumed spread.",
    [f_loans, f_cbe, f_cov])

R.add_driver(
    "Capitalised interest add-back in the FCFF bridge",
    DriverMode.BOTTOM_UP,
    "The cumulative capitalised-interest balance is disclosed for three consecutive year-ends (EGP "
    "40,645,800 / 386,226,438 / 837,689,037), so the in-year amounts are derivable (c.EGP 345.6mn "
    "2024, c.EGP 451.5mn 2025) and are cross-checked by an implied-rate test on average gross debt. "
    "The build adds capitalised interest to interest paid rather than taking the P&L finance "
    "expense as the cash cost.",
    [f_capint, f_loans])

R.add_driver(
    "Depreciation on projects in progress as they enter service",
    DriverMode.BOTTOM_UP,
    "The fixed-asset note gives projects in progress at EGP 4,738,267,842 (67% of net fixed assets) "
    "and the useful-life policy and asset-class split for everything already in service, so the "
    "step-up as CTH and the Cleopatra October extension transfer is computed from the disclosed "
    "balance rather than assumed. FY2025 depreciation of EGP 217,627,002 is explicitly NOT treated "
    "as a run-rate.",
    [f_fixed, f_cogs])

R.add_driver(
    "Capital expenditure",
    DriverMode.BOTTOM_UP,
    "Guided (49% of sales 2024, 37% 2025, c.10% 2026) AND corroborated by the audited capital-"
    "commitment balance falling from EGP 487,283,142 to 151,017,672 to 13,340,800, plus H1-2026 "
    "actual capex of EGP 813mn. FY2026 is built from H1 actual plus a guided H2 and the resulting "
    "full-year ratio is stated against the 10% guide rather than averaged into it. FY2024 capex is "
    "taken at EGP 2,648,894,145 per the fixed-asset note, not at the EGP 746,376,706 the "
    "non-footing segment row appears to show.",
    [f_commit, f_pipeline, f_footfail, f_fixed])

R.add_driver(
    "Effective tax rate",
    DriverMode.BOTTOM_UP,
    "Built as the 22.5% statutory rate plus an explicit non-deductible add-back keyed to the LTIP "
    "and pre-operating lines, calibrated to the realised effective rate the audited and reviewed "
    "statements produce: 20.7% FY2022, 22.3% FY2023, 24.6% FY2024, 26.6% FY2025, 30.1% H1-2026. "
    "Running the statutory 22.5% would overstate after-tax cash by 5-10% of profit before tax at "
    "the current run-rate.",
    [f_tax, f_fy25, f_q2fs])

R.add_driver(
    "LTIP / employee incentive charge",
    DriverMode.BOTTOM_UP,
    "The mechanic is disclosed (difference between the weighted average price the month before "
    "grant and the month before maturity, times units, divided by the maturity price), the charge "
    "is disclosed (EGP 202mn H1-2026 vs EGP 60mn H1-2025), and the balance-sheet liability is "
    "disclosed at both dates. Modelled as a function of the modelled equity value, held OUTSIDE the "
    "operating cost base so the valuation does not become circular. The company's own EGP "
    "106,661,048 annual estimate is not used and the reason is stated.",
    [f_ltip, f_eip, f_ga])

R.add_driver(
    "Non-controlling interest deduction in the equity bridge",
    DriverMode.BOTTOM_UP,
    "Cairo Specialized Hospital is 42.99% minority-held and carries 96% of the group's EGP "
    "418,028,210 NCI; its standalone revenue (EGP 1,579,063,693), profit (EGP 284,817,902) and "
    "equity (EGP 935,810,254) are all separately disclosed in the audited segment and NCI notes. "
    "The minority is therefore valued on CSH's own earnings at fair value, not deducted at book.",
    [f_nci, f_segnote, f_subs])

R.add_driver(
    "Employee and board profit share (the only 'dividend')",
    DriverMode.BOTTOM_UP,
    "Disclosed in the statement of changes in equity and the cash-flow statement for every period: "
    "EGP 142,179,178 plus 4,166,834 in FY2025 and EGP 144,107,006 plus 9,269,573 in H1-2026, with "
    "cash paid of EGP 143.4mn in H1-2026. Carried as a recurring pre-shareholder cash outflow. NO "
    "ORDINARY DIVIDEND EXISTS, so no dividend-discount lens is available and none is shown.",
    [f_div, f_capital])

R.add_driver(
    "Share count and dilution",
    DriverMode.BOTTOM_UP,
    "1,449,450,084 shares at EGP 0.50 par with nil treasury at FY2025, from the audited share-"
    "capital note, with the FY2025 capital reduction (1,648,577 shares cancelled) and increase "
    "(5,664,458 shares to the employee plan) both dated and reconciled. Annual employee dilution of "
    "c.0.4% is carried forward rather than the count being held flat.",
    [f_capital, f_owners])

R.add_driver(
    "Payer mix and UHIA tariff exposure",
    DriverMode.TOP_DOWN,
    "TOP-DOWN OF NECESSITY AND THE ABSENCE IS EVIDENCED. CLHO discloses no split of revenue by "
    "payer in any document in any period — the negative search covers the audited statements "
    "FY2022-FY2025, both 2026 interims, six earnings releases, three IR presentations and all seven "
    "press releases. UHIA is a tariff-setting payer whose Phase 2 targets 12-13mn more lives and "
    "expects private providers to supply 30-40% of beds, and CLHO operates in Suez, a Phase-1 "
    "governorate. With no mix disclosed, the exposure is carried as a named ARP scenario on the "
    "revenue-per-case drivers rather than modelled, and the study states that it is unquantifiable "
    "from disclosure.",
    [f_neg_payer, f_neg_gahar, f_uhia])

R.add_driver(
    "Bed occupancy percentage and average length of stay",
    DriverMode.TOP_DOWN,
    "TOP-DOWN OF NECESSITY AND THE ABSENCE IS EVIDENCED. No occupancy rate, no average length of "
    "stay and no bed-day count is disclosed in any CLHO document in any period; the only references "
    "are qualitative. Beds and inpatient cases ARE disclosed, so cases per bed is derived and used "
    "as the utilisation proxy, and the missing length-of-stay term — which is what would convert it "
    "into a true occupancy percentage — is flagged as a gap rather than assumed.",
    [f_neg_occ, f_pipeline, f_er25])

R.add_driver(
    "Terminal growth and terminal value structure",
    DriverMode.TOP_DOWN,
    "TOP-DOWN OF NECESSITY. CLHO issues no revenue, EBITDA or earnings guidance at group level — "
    "the negative search covers every 2024-2026 release and presentation — so beyond the named, "
    "contracted capacity (Cleopatra El Tagamoa to 240 beds, Cleopatra October +200 for 2027-28) "
    "there is nothing company-sourced to build on. Terminal growth is norm-built off the CBE's own "
    "medium-term inflation target and is CAPPED by two contract expiries that are disclosed and "
    "dated: the 27-year Cleopatra El Tagamoa right-of-use from December 2021 and the 25-year "
    "Cleopatra October partnership from its licence date, at the end of which both complexes are "
    "handed back with all equipment.",
    [f_neg_guid, f_cth_contract, f_coh_contract, f_cbe, f_ppp])

R.add_driver(
    "Cairo Specialized Hospital 57% -> 90% completion",
    DriverMode.TOP_DOWN,
    "TOP-DOWN OF NECESSITY AND SEARCHED BY NAME, NOT ESTIMATED. The transaction is announced, "
    "regulatory approval is secured and the company states 'a final value has not yet been "
    "determined'; the reviewed statements show 57.01% still held at 30 June 2026. A dated negative "
    "search found no completion, no price and no counterparty, and neither egx.com.eg nor "
    "fra.gov.eg could be reached to inspect the file. It is therefore excluded from the base case "
    "and run as a separate dual-framed scenario with the price labelled an assumption and "
    "sensitised.",
    [f_neg_stake, f_csh, f_subs])

R.add_driver(
    "Strategic-review outcome",
    DriverMode.TOP_DOWN,
    "TOP-DOWN OF NECESSITY. The Board disclosed on 6 September 2026 that a strategic review is "
    "under way to close the gap between intrinsic value and market valuation, with no form, "
    "counterparty, price or timetable. A dated negative search found nothing filed beyond that "
    "paragraph. It is NOT capitalised into any lens; it is carried as a disclosed, dated overhang "
    "in the risk section.",
    [f_neg_stake, f_strategy])

R.add_driver(
    "Competitive intensity in East and West Cairo (the Cleopatra El Tagamoa ramp cap)",
    DriverMode.TOP_DOWN,
    "TOP-DOWN OF NECESSITY. Competitor CAPACITY is well documented and named — Alameda at 1,023 "
    "beds with USD 190mn of new DPI equity and a Houston Methodist partnership at Madinaty in New "
    "Cairo, Andalusia going from 229 to 445 beds, and a 62-project state PPP pipeline — but "
    "competitor PRICING is not observable and the dated negative search records why: none of them "
    "is listed and Egyptian private hospitals do not publish tariffs. The competitive term "
    "therefore enters as a cap on the new-bed utilisation ramp, not as a price-response term.",
    [f_neg_compprice, f_alameda, f_peers, f_ppp])

# ===========================================================================
# OUTPUT
# ===========================================================================
errors, warnings = R.validate()
R.to_json(os.path.join(HERE, 'sweep_register.json'))

print(R.qc_line())
print(f"\nfindings: {len(R.findings)} | drivers: {len(R.drivers)}")
counts = R.counts()
print("by class: " + " | ".join(f"{k} {v}" for k, v in counts.items()))
nbu = sum(1 for d in R.drivers if d.mode is DriverMode.BOTTOM_UP)
print(f"drivers by mode: {nbu} bottom-up / {len(R.drivers) - nbu} top-down")
n_ir = sum(1 for f in R.findings if f.source_type is SourceType.COMPANY_IR)
n_co = sum(1 for f in R.findings if f.source_type is SourceType.COMPANY_OFFICIAL)
print(f"company sources: {n_co} COMPANY_OFFICIAL | {n_ir} COMPANY_IR")
print(f"primary access attempts: {len(R.primary_access)} "
      f"({sum(1 for p in R.primary_access if p.reachable)} reachable / "
      f"{sum(1 for p in R.primary_access if not p.reachable)} blocked)")

print(f"\nVALIDATOR ERRORS ({len(errors)}):")
if errors:
    for e in errors:
        print(f"  ! {e}")
else:
    print("  none")

print(f"\nVALIDATOR WARNINGS ({len(warnings)}):")
if warnings:
    for w in warnings:
        print(f"  - {w}")
else:
    print("  none")

fresh = R.check_freshness(SWEEP_DATE)
print(f"\nfreshness (delivery {SWEEP_DATE}): "
      f"{fresh or 'OK — sweep and intended delivery same day, 0 days elapsed'}")
fresh14 = R.check_freshness("2026-09-23")
print(f"freshness (delivery 2026-09-23): {fresh14 or 'OK — within the 14-day window'}")
print(f"\nregister rows: {len(R.register_rows()) - 1} | driver rows: {len(R.driver_rows()) - 1}")
print(f"JSON written to {os.path.join(HERE, 'sweep_register.json')}")
