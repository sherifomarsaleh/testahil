"""ETEL — Telecom Egypt Company S.A.E. (EGX: ETEL; LSE GDR: TEEG) — Step 2A four-ring
Information Sweep register, through the SHARED module engine/research_sweep.py.

FIRST BUILD. No prior study directory existed for this name; a published edition dated
03-07-2026 exists in assets/editions.json with no engine-side working directory behind it,
so nothing here inherits from a predecessor.

RUN BEFORE ANY FORECAST DRIVER IS SET. Every mandatory category of every ring is closed by
a dated finding or by a dated negative search that was ACTUALLY RUN on the date recorded.

-----------------------------------------------------------------------------------------
PRIMARY SOURCE: the company's own channel was tried first and it worked.
-----------------------------------------------------------------------------------------
te.eg (the retail site) refused the root document with a connection reset at this
environment's proxy relay and its sitemap carries no investor section at all. The investor
site ir.te.eg answered on the second attempt after one transient 502 at the CONNECT, and it
is complete: audited and interim statements back to 2006, earnings releases, results
presentations, conference-call transcripts and a quarterly Fact Book workbook. EVERY
Company-ring figure below comes from that channel. No aggregator, broker or press source
carries any figure Telecom Egypt reported about itself in this register.

-----------------------------------------------------------------------------------------
ARITHMETIC IS THE ARBITER — the route each figure came by, recorded.
-----------------------------------------------------------------------------------------
Three extraction routes were used and each is named on the finding that rests on it:

  TEXT  — the PDF's own text layer (pdftotext -layout). Only FS_Q4-2025 (the FY2025 audited
          consolidated set) carries one, and even there PDF pages 3-5 are images with no
          text at all, so the auditor's report and the balance sheet had to be OCR'd.
  OCR   — rendered pixels re-read by tesseract, used for every FY2022/FY2023/FY2024 page,
          both 2026 interims, and the H1-2026 earnings release, all of which are pure scans.
  XLSX  — the IR Fact Book workbook, read with openpyxl. IR channel, never a statement.

Every statement page accepted below was footed against its own printed subtotals before it
was used. Three things the footing caught, all recorded as findings rather than silently
corrected:

  (a) The FY2025 CONSOLIDATED STATEMENT OF CHANGES IN EQUITY DOES NOT FOOT. Its printed
      "Total transactions with shareholders" for FY2025 is (2 249 264) while the rows above
      it sum to (4 809 871), and its closing retained earnings of 41 050 147 exceeds the
      balance sheet's 38 489 540 by exactly the omitted 2 560 607 dividend. BOTH extraction
      routes (text layer and OCR off the rendered pixels) return the same figures, so this
      is a defect in the filed document, not in the extraction. The balance sheet, the
      segment note, the H1-2026 interim's own FY2025 comparative and the Fact Book all
      agree at 38 489 540. F43 records it. Equity is taken from the balance sheet.
  (b) The Q1-2026 interim OCR returned a net finance cost of 7 737 973 that did not foot;
      the printed pre-tax subtotal only reconciles at 7 757 973, which the Fact Book
      independently confirms. A 2-in-1000 glyph error, invisible to the eye, caught by
      addition. F21 records the route.
  (c) The FY2025 balance-sheet OCR returned "104 14_ 296", "43 064 514", "2 468 557",
      "8 10€ 567" and "2 97& 482". Every one of them broke a column that otherwise foots to
      the pound, and every one is recoverable from the total. No figure was accepted on the
      extractor's confidence.

-----------------------------------------------------------------------------------------
WHAT THE STUDY MUST NOT DO, discovered here rather than after the build.
-----------------------------------------------------------------------------------------
  * ARPU x SUBSCRIBERS DOES NOT REPRODUCE REVENUE. The company publishes both, and they do
    not multiply together: the H&C fixed-voice ARPU printed for Q2-2026 is EGP 40.07 while
    disclosed H&C voice revenue over disclosed H&C voice subscribers gives EGP 50.88 — the
    printed rate is 21% low. F33 carries the numbers. The published ARPU is a growth
    indicator on the company's own definition, not a build input.
  * MOBILE REVENUE IS NOT DISCLOSED ANYWHERE. WE's 15.2m mobile subscribers sit inside the
    "Home & Consumer" retail segment and its revenue is reported only as a growth rate. F49
    is the negative search. The mobile leg cannot be built bottom-up and the gate row says so.
  * THE FY2025 BALANCE SHEET EXISTS ON TWO BASES. The audited statement nets deferred tax
    (total assets 225 882 527); the H1-2026 interim reclassifies it gross (231 058 652) and
    the Fact Book, the FY2025 release and the Q1/H1-2026 releases all use the gross basis.
    Both foot. F42 records it; the study must state which basis it carries.
  * DUAL LISTING. Ordinary shares trade on the EGX as ETEL.CA in EGP; GDRs trade on the LSE
    as TEEG.LN, each GDR being five ordinary shares. F55 flags it. The repo's own series
    engine/raw_ohlc/EG/ETEL.csv closes at EGP 118.49 on 23-Aug-2026, which is the EGX line
    and not the GDR, so the regressor is EGX30 under wacc_builder.market_index_path('EG').
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))

from research_sweep import (SweepRegister, AssetClass, Ring, FindingClass,
                            SourceType, DriverMode)

SWEEP_DATE = "2026-09-08"
R = SweepRegister("ETEL", AssetClass.STOCK, SWEEP_DATE)

CO, IR, REG = (SourceType.COMPANY_OFFICIAL, SourceType.COMPANY_IR,
               SourceType.REGULATOR_OFFICIAL)
PMD, PRESS, AGG = (SourceType.PRIMARY_MARKET_DATA, SourceType.REPUTABLE_PRESS,
                   SourceType.AGGREGATOR)

# ==========================================================================================
# PRIMARY ACCESS — the company's own site, attempted FIRST and logged either way
# ==========================================================================================
R.record_primary_access(
    "https://te.eg/", False, SWEEP_DATE,
    note="Corporate/retail site. The root document was refused with 'Recv failure: "
         "Connection reset by peer' and the agent proxy's own status endpoint logged "
         "connect_rejected and two ws_closed_mid_exchange events for te.eg:443 at the same "
         "minute. https://www.te.eg/en did answer 200 but is a JavaScript shell with no "
         "links in the served HTML, and te.eg/sitemap.xml (190 sub-sitemaps, 700 URLs "
         "crawled) contains NO investor-relations path at any depth. Tried before any "
         "other source; recorded because it failed, not despite it.")

R.record_primary_access(
    "https://ir.te.eg/en", True, SWEEP_DATE,
    note="THE PRIMARY CHANNEL, and it is complete. First CONNECT returned a proxy 502; the "
         "retry answered 200 and every subsequent request succeeded. Sections reached: "
         "/FinancialInformation/FinancialStatements, /QuarterlyResults, "
         "/CorporatePresentation, /AnnualReports, /CorporateNews/PressReleases, "
         "/ShareInformation. Year filtering is served by "
         "/en/FinancialInformation/{section}_Partial/{year}, which was walked for 2022-2026 "
         "to enumerate documents rather than guessing URLs.")

R.record_primary_access(
    "https://ir.te.eg/en/FinancialInformation/FinancialStatements", True, SWEEP_DATE,
    note="Audited EAS consolidated and standalone statements plus IFRS consolidated, by "
         "quarter, 2006-2026. Downloaded and used here: FY2022, FY2023, FY2024 and FY2025 "
         "audited EAS consolidated (Q4 filings), and the Q1-2026 and H1-2026 condensed "
         "interims. FY2026 lists Q1 and Q2 only, which is what fixes the disclosed-quarter "
         "declaration below.")

R.record_primary_access(
    "https://ir.te.eg/en/FinancialInformation/QuarterlyResults", True, SWEEP_DATE,
    note="Earnings release, conference-call transcript, results presentation and Fact Book "
         "(.xlsx) for every quarter. The Fact Book is the operating-anchor document: "
         "subscribers and ARPU by segment, revenue to sub-line, quarterly in-service capex, "
         "the USD/EGP rate the company itself used, and Vodafone Egypt's own KPIs. "
         "Downloaded: FB Q4-2025, Q1-2026, Q2-2026; releases and presentations for the same "
         "three periods; transcripts for the same three.")

R.record_primary_access(
    "https://www.cbe.org.eg/en/economic-research/statistics/cbe-rates", False, SWEEP_DATE,
    note="NOT a company source — logged here so the block is visible rather than implied. "
         "The Central Bank of Egypt's rates page and its Q1-2026 Monetary Policy Report PDF "
         "both returned the site's WAF rejection ('The requested URL was rejected') through "
         "this environment's proxy. The CBE's own decision figures in F06 are therefore "
         "carried at one remove, from reporting that quotes the MPC statement directly, and "
         "the finding says so on its face.")

# ==========================================================================================
# STUDY YEAR — every quarter of FY2026 already on the public record at the sweep date
# ==========================================================================================
R.declare_study_year("2026", ["Q1-2026", "Q2-2026"])

# ==========================================================================================
# RING 1 — GLOBAL
# ==========================================================================================
f_fed = R.add(
    Ring.GLOBAL, "rate cycle & USD/FX regime", FindingClass.S,
    "The US federal funds target range is 3.50-3.75%, held since December 2025 and most "
    "recently on 29 July 2026; the next FOMC is 15-16 September 2026. This is the external "
    "anchor against which Egypt's 19.50% main operation rate has to normalise, and it is "
    "the rate on the 45.4% of Telecom Egypt's debt that is denominated in US dollars",
    "Federal Open Market Committee policy statements and minutes, Board of Governors of the "
    "Federal Reserve System",
    REG, "2026-07-29",
    model_impact="Sets the direction of the USD leg of the cost of debt. Telecom Egypt's "
                 "USD facilities are all variable-rate (note 27), so the dollar policy path "
                 "feeds the interest driver directly rather than through a spread "
                 "assumption; it is also the floor under the terminal risk-free build.")

f_fx = R.add(
    Ring.GLOBAL, "rate cycle & USD/FX regime", FindingClass.D,
    "The company publishes the exact USD/EGP rates it used: average 30.2435 (FY2023), "
    "44.3946 (FY2024), 49.23 (FY2025), 49.2275 (Q1-2026) and 50.1971 (H1-2026); closing "
    "30.80, 50.83, 47.65, 54.55 and 49.23. The pound STRENGTHENED through the FY2025 close "
    "and again through Q2-2026, which is why Q2-2026 carries a net finance GAIN of EGP "
    "908 021 thousand where Q1-2026 carried a EGP 7 757 973 thousand net finance cost",
    "Telecom Egypt Fact Book Q2-2026, sheet 'KPIs Highlight' (XLSX route)", IR, "2026-08-13",
    fiscal_period="Q2-2026",
    model_impact="DRIVER UNLOCK. Fixes the FX path used for the USD-linked wholesale revenue "
                 "leg and for the revaluation of the net foreign-currency liability, on the "
                 "company's own rates rather than a market series. It also proves the FX "
                 "line is TWO-SIDED and must not be modelled as a one-way loss.")

f_inputs = R.add(
    Ring.GLOBAL, "commodity complex (input/output)", FindingClass.D,
    "There is no single commodity input, and the audited statements name every cost line by "
    "nature. FY2025 operating costs of EGP 61 833 836 thousand break into 20 disclosed "
    "lines, of which the globally-priced ones are: cost of merchandise available for sale "
    "(handsets) 1 855 834, right of use (IRU) outside Egypt - leased circuits 2 261 860, "
    "fuel 1 897 522, spare parts 997 846, maintenance 1 497 803 and electricity and water "
    "172 793. Call cost at 16 082 021 and salaries and wages at 6 620 037 are the two "
    "largest lines and are domestic",
    "Telecom Egypt FY2025 audited consolidated financial statements, note 6 'Operating "
    "costs' (KPMG Hazem Hassan, Cairo, 26 February 2026) — TEXT route, note foots to "
    "61 833 836 exactly across all 20 lines for FY2025 and to 51 185 050 for FY2024",
    CO, "2026-02-26",
    url="https://ir.te.eg/IRMedia/Financial_Information/EAS_Consolidated_Statement/2026/EAS_Consolidated_Statement38a2837b-8610-4c24-aa82-ac57ea993e7e.pdf", is_fs_data=True, fiscal_period="FY2025",
    model_impact="DRIVER UNLOCK, and the reason margins can be an OUTPUT on this name. Each "
                 "line takes its own escalator: the imported and USD-linked lines follow the "
                 "FX path, fuel and electricity follow Egyptian energy-price reform, the "
                 "regulated NTRA charge follows its own base, and wages follow domestic "
                 "inflation. One blended index across all 20 would invent a margin trend.")

f_gdemand = R.add(
    Ring.GLOBAL, "global sector demand", FindingClass.S,
    "The demand this company sells into is international transit, not a world price. Egypt "
    "anchors, on the company's own statement, over 90% of the data traffic moving between "
    "Europe, Asia and Africa; Telecom Egypt has 16 subsea cable systems in service with 6 "
    "or more planned, 11 landing points in service with 3 or more planned, and 12 diverse "
    "terrestrial crossing routes. Systems land from FEA (1997) through 2Africa (2023) and "
    "Coral Bridge (2025), with Africa-1, IEX, Medusa, SEA-ME-WE-6 and MRSC dated 2027 and "
    "EAGLE 2028",
    "Telecom Egypt Corporate Presentation 2026, 'Our International Connectivity Network', "
    "and Q1 2026 Earnings Release (21 May 2026)", IR, "2026-05-21",
    model_impact="Sets the volume driver for the International Customers & Networks leg and "
                 "dates the capacity that arrives inside the forecast window. The 2027-28 "
                 "landings are the reason cable-project revenue must be modelled as a lumpy "
                 "dated schedule, never as a growth rate off a cyclical base.")

f_redsea = R.add(
    Ring.GLOBAL, "trade / sanctions / supply chains", FindingClass.S,
    "The Red Sea corridor these cables run through has been repeatedly severed. AAE-1 was "
    "cut in December 2024 and not repaired until 7 April 2025, an outage of nearly four "
    "months; PEACE was cut 1 450km from Zafarana on 4 March 2025 and repaired 26 March "
    "2025; SMW4 and IMEWE were both cut on 6 September 2025, slowing traffic across India, "
    "Pakistan and the Gulf. Telecom Egypt is a landing party or consortium member on AAE-1, "
    "IMEWE, PEACE and the SEA-ME-WE family",
    "Submarine Networks / Data Center Dynamics / ThousandEyes reporting of the Red Sea "
    "cable incidents, cross-read against the company's own system list",
    PRESS, "2025-09-06",
    model_impact="A two-sided structural driver. Cuts remove capacity revenue and raise "
                 "restoration cost in the period they happen, and simultaneously raise "
                 "demand for the diversified terrestrial crossing routes the company sells. "
                 "Modelled as a downside scenario on the IC&N leg with an offsetting "
                 "terrestrial uplift, not as a single-signed haircut.")

# ==========================================================================================
# RING 2 — COUNTRY
# ==========================================================================================
f_cbe = R.add(
    Ring.COUNTRY, "sovereign macro (inflation, policy rate, FX/deval risk)", FindingClass.D,
    "The Central Bank of Egypt has held the overnight deposit rate at 19.00%, the overnight "
    "lending rate at 20.00% and the main operation and discount rate at 19.50% since the "
    "12 February 2026 cut of 100bp, through the May and July 2026 meetings. The CBE's own "
    "target is 7% plus or minus 2pp; it expects headline inflation to accelerate through Q3 "
    "2026 and stay above target through Q4 2026 before declining from Q1 2027 and "
    "approaching target in H2 2027",
    "Central Bank of Egypt Monetary Policy Committee statements, quoted directly in Daily "
    "News Egypt's reports of the 21 May 2026 and July 2026 meetings",
    REG, "2026-05-21",
    detail="THE CBE'S OWN SITE WAS BLOCKED at this environment's proxy (logged under primary "
           "access) — both cbe.org.eg/en/economic-research/statistics/cbe-rates and the Q1 "
           "2026 Monetary Policy Report PDF returned the site's WAF rejection. The figures "
           "are the MPC's own, at one remove. Re-source from the CBE directly before the "
           "cost-of-capital block is struck.",
    model_impact="Explicit-window Egyptian risk-free rate and the EGP leg of the cost of "
                 "debt. The terminal rate is norm-built from the CBE's OWN published target "
                 "of 7% plus the house EM real-rate convention, never from a historical "
                 "average. The stated 2027 disinflation path is what allows a glide rather "
                 "than a flat ladder.")

f_cpi = R.add(
    Ring.COUNTRY, "sovereign macro (inflation, policy rate, FX/deval risk)", FindingClass.S,
    "Annual urban headline inflation was 14.9% in July 2026 against 14.3% in June, driven "
    "by housing, water, electricity, gas and fuel at +31.1% year on year, transport and "
    "communications at +21.1% and education at +20%. Headline inflation for the country as "
    "a whole was 13.0% in July against 12.2% in June",
    "Central Agency for Public Mobilisation and Statistics (CAPMAS) monthly CPI release of "
    "10 August 2026",
    REG, "2026-08-10",
    model_impact="The escalator on the domestic cost lines — wages, transport, organisations "
                 "services. The transport-and-communications sub-index at +21.1% is also the "
                 "measured pass-through of the NTRA tariff rise into the consumer basket, "
                 "which caps how far a second round can be pushed inside the window.")

f_ntra = R.add(
    Ring.COUNTRY, "regulatory environment (regulator, caps, tariffs, tax/subsidy)",
    FindingClass.B,
    "On 6 May 2026 the NTRA approved a telecom price adjustment of 9% to 15% on home and "
    "mobile internet packages, steeper on high-consumption plans, while holding fixed and "
    "mobile VOICE minutes, prepaid recharge cards and e-wallet charges unchanged, and "
    "simultaneously mandating an EGP 150 home-internet tier, an EGP 5 mobile tier and free "
    "access to government and educational sites after data exhaustion. The regulator "
    "attributed the rise to the dollar, electricity and the diesel that powers mobile towers",
    "National Telecom Regulatory Authority decision of 6 May 2026, reported by Al Manassa "
    "and Ahram Online; the company's own applied percentages are in F13",
    REG, "2026-05-06",
    model_impact="BASE CHANGER, and it is dated inside the study year. It resets the retail "
                 "price base from Q2-2026 and is DUAL-FRAMED: the rise applies only to DATA "
                 "packages, so the voice ARPU line must not be escalated with it, and the "
                 "mandated EGP 150 and EGP 5 tiers are a mix drag that partly offsets the "
                 "headline percentage. Modelled as an explicit dated step, never smoothed.")

f_spectrum = R.add(
    Ring.COUNTRY, "regulatory environment (regulator, caps, tariffs, tax/subsidy)",
    FindingClass.S,
    "Telecom Egypt signed an agreement on 7 February 2026 to acquire new frequency bands "
    "and renew the rights of use for existing bands. It holds Egypt's first 5G network "
    "licence, granted January 2024 for USD 150m; Vodafone Egypt, Orange Egypt and e& Egypt "
    "received theirs in October 2024 for USD 675m between them, and commercial 5G launched "
    "nationwide in June 2025. The NTRA's 2026-2030 National Spectrum Strategy releases "
    "roughly 410-420MHz of new spectrum in phases",
    "Telecom Egypt FY2025 audited consolidated financial statements, note 44 'Subsequent "
    "events' (TEXT route), read with the Corporate Presentation 2026 and NTRA/MCIT reporting "
    "of the licence awards",
    CO, "2026-02-26",
    url="https://ir.te.eg/IRMedia/Financial_Information/EAS_Consolidated_Statement/2026/EAS_Consolidated_Statement38a2837b-8610-4c24-aa82-ac57ea993e7e.pdf", fiscal_period="FY2025",
    model_impact="Licence capex is a dated cash item inside the window and it is separable: "
                 "the company itself reports FCFF both including and excluding mobile "
                 "licence capex. The intangible roll in note 17 shows EGP 4 953 550 thousand "
                 "transferred out of projects-under-construction into mobile licences in "
                 "FY2025, which sets the amortisation base going forward.")

f_govt = R.add(
    Ring.COUNTRY, "fiscal / political events with sector read-through", FindingClass.S,
    "The Egyptian Government owns 70% of the issued capital, held through the Ministry of "
    "Finance, after a 20% public offering in December 2005 and a further 10% placed during "
    "2023; 30% is the free float. Note 37-2 discloses that this produces mutual services "
    "between the company and government entities across revenues, costs, taxes, social "
    "insurance and customs. The company quotes the CBE's FY2025/2026 real GDP growth "
    "projection of 5.1% as its own planning backdrop",
    "Telecom Egypt FY2025 audited consolidated financial statements, note 31 'Capital' and "
    "note 37-2 'Transactions with the Egyptian government' (TEXT route), and the FY2025 "
    "Earnings Release of 26 February 2026",
    CO, "2026-02-26",
    url="https://ir.te.eg/IRMedia/Financial_Information/EAS_Consolidated_Statement/2026/EAS_Consolidated_Statement38a2837b-8610-4c24-aa82-ac57ea993e7e.pdf", is_fs_data=True, fiscal_period="FY2025",
    model_impact="Three consequences, all modelled. The state is simultaneously owner, "
                 "regulator and a large customer, so the NTRA tariff decision is not an "
                 "arm's-length price. The 30% float caps index weight and is the mechanism "
                 "behind any placement overhang. And a government receivable book is a "
                 "working-capital driver in its own right, not a residual plug.")

# ==========================================================================================
# RING 3 — INDUSTRY
# ==========================================================================================
f_mkt = R.add(
    Ring.INDUSTRY, "demand drivers & capacity/supply balance", FindingClass.D,
    "Egypt's fixed-broadband market was 13 231 thousand subscribers at 9M-2025, of which "
    "Telecom Egypt held 10 861 thousand and all others 2 370 thousand — an 82.1% share of "
    "the national fixed-broadband base. Household penetration ran 51.6% for fixed voice and "
    "49.4% for broadband at 9M-2025, from 43.3% and 39.3% at FY2021. Mobile voice "
    "penetration reached 133% of population and mobile data 88%, with the mobile data "
    "market at 91 560 thousand subscribers from 63 440 thousand at FY2021",
    "Telecom Egypt Corporate Presentation 2026, 'Fixed Services' and 'Mobile Market' slides, "
    "sourced on their face to MCIT and operators' disclosures",
    IR, "2026-02-05",
    url="https://ir.te.eg/IRMedia/Financial_Information/2026/Financial_Information173467e6-c593-4286-9fb7-ee16490de8b8.pdf",
    model_impact="DRIVER UNLOCK for the fixed legs. Subscriber growth is bounded by "
                 "household penetration heading toward saturation, so the fixed-line volume "
                 "driver decays toward household formation while the mobile leg still has "
                 "headroom on data penetration. This is what stops a straight-line "
                 "extrapolation of the 7-9% subscriber growth of the last two years.")

f_fibre = R.add(
    Ring.INDUSTRY, "demand drivers & capacity/supply balance", FindingClass.C,
    "Fibre access network capacity reached 34 353 thousand homes at 9M-2025, from 30 800 "
    "thousand at FY2020, 32 230 at FY2022 and 33 875 at FY2024. The company states 100% of "
    "households have had copper replaced with fibre to the cabinet, with FTTH rollout "
    "accelerating as legacy copper is phased out, greenfield FTTH across the New "
    "Administrative Capital, 4G fixed wireless access where FTTH does not reach, and "
    "fibre-to-the-building for 31 thousand government buildings in three phases",
    "Telecom Egypt Corporate Presentation 2026, 'Digitizing Egypt' slide", IR, "2026-02-05",
    model_impact="")

f_price = R.add(
    Ring.INDUSTRY, "pricing", FindingClass.D,
    "Telecom Egypt states the percentages it actually applied under the NTRA decision: "
    "fixed broadband prices up 13.5% and mobile prices up 15%. The effect is visible in the "
    "Q2-2026 numbers — retail data revenue rose 30% year on year in the quarter and "
    "contributed 65% of total revenue growth (Home and Consumer data revenue on the "
    "company's own quarterly series is +30.1%). Two earlier price adjustments were taken "
    "in FY2024, which is why FY2025 Home and Consumer ARPU rose 36% year on year",
    "Telecom Egypt H1 2026 Earnings Release, 13 August 2026 (OCR route, pages 3-4), read "
    "with the FY2025 Earnings Release of 26 February 2026",
    IR, "2026-08-13",
    url="https://ir.te.eg/IRMedia/Financial_Information/Earnings_Release/2026/Earnings_Release6e0e975f-190e-438d-926e-1ac077443e9c.pdf", fiscal_period="Q2-2026",
    model_impact="DRIVER UNLOCK. Converts the retail price leg from a growth rate to a dated "
                 "step of a stated size, applied to the DATA base only. Also the evidence "
                 "that a price round lands with roughly one quarter of lag, which sets where "
                 "in the year the next one can be assumed to bite.")

f_5g = R.add(
    Ring.INDUSTRY, "competitor capacity / price moves (named)", FindingClass.D,
    "All four Egyptian mobile operators are named and all four now hold 5G spectrum. By "
    "market share of mobile subscribers: Vodafone Egypt roughly 42%, Orange Egypt roughly "
    "26%, e& Egypt (Etisalat Misr) roughly 22%, with Telecom Egypt's WE the remainder on "
    "15 475 thousand subscribers at FY2025. Telecom Egypt is the only one of the four whose "
    "economics the study sees twice — once as WE and once through the 44.95% holding in "
    "Vodafone Egypt",
    "Egypt telecom market share reporting (Mordor Intelligence / Analysys Mason country "
    "reports) cross-read against the company's own subscriber disclosure",
    AGG, "2026-01-01",
    model_impact="Sets the competitive ceiling on WE's subscriber share and, more "
                 "importantly, makes the Vodafone Egypt stake a partial HEDGE on WE's own "
                 "share loss: subscribers WE loses to the market leader come back at 44.95%. "
                 "The two legs are modelled together, never independently.")

f_sub = R.add_negative(
    Ring.INDUSTRY, "technology substitution",
    "Searched the FY2025 audited statements, the Corporate Presentation 2026, the FY2025 "
    "and Q1/H1-2026 earnings releases and results presentations, and open sources, for a "
    "disclosed or quantified substitution threat to fixed broadband or fixed voice — "
    "satellite direct-to-consumer (Starlink), over-the-top voice displacement, or fixed-"
    "wireless cannibalisation of FTTH. Nothing quantified exists in any company document. "
    "The only substitution the company itself describes is INTERNAL and planned: 4G fixed "
    "wireless access deployed by Telecom Egypt where FTTH does not reach, and copper phased "
    "out in favour of fibre. No licensed satellite consumer-broadband competitor is "
    "disclosed. Category closed by absence, and the top-down treatment of the terminal "
    "fixed-line decay rate rests on this.",
    SWEEP_DATE)

f_entrants = R.add_negative(
    Ring.INDUSTRY, "new entrants (named-competitor level)",
    "Searched NTRA licence reporting, MCIT statements and the company's own risk and "
    "competition language for a FIFTH licensed Egyptian fixed or mobile operator, or a new "
    "entrant into international transit or subsea landing rights, over 2025-2026. None "
    "exists: the market remains the four named operators, and the 2026-2030 National "
    "Spectrum Strategy allocates the new 410-420MHz among those same four rather than "
    "opening a licence round. The one adjacent entrant found is a partner rather than a "
    "competitor — Helios Investment Partners' proposed stake in a Telecom Egypt data-centre "
    "subsidiary, which the company terminated on 16 July 2026 (see F41).",
    SWEEP_DATE)

# ==========================================================================================
# RING 4 — COMPANY: audited financial statements, four fiscal years, from the filings
# ==========================================================================================
f_fy25 = R.add(
    Ring.COMPANY, "official financial statements", FindingClass.D,
    "FY2025 audited consolidated: operating revenues EGP 106 672 946 thousand, operating "
    "costs (61 833 836), gross profit 44 839 110, operating profit 28 042 356, net finance "
    "cost (11 959 482), share of profit of equity accounted investees 14 828 173, income "
    "tax (8 569 486), net profit from continued operations 22 341 561, discontinued 236 502, "
    "net profit 22 578 063, attributable to shareholders 22 554 632, EPS EGP 11.93",
    "Telecom Egypt FY2025 audited consolidated financial statements, Consolidated Statement "
    "of Profit or Loss, page 2 — auditor KPMG Hazem Hassan, unqualified with an emphasis of "
    "matter on the Ramses Central fire, Cairo 26 February 2026. TEXT route; every subtotal "
    "on the page re-added and foots exactly, both the FY2025 and the FY2024 column",
    CO, "2026-02-26",
    url="https://ir.te.eg/IRMedia/Financial_Information/EAS_Consolidated_Statement/2026/EAS_Consolidated_Statement38a2837b-8610-4c24-aa82-ac57ea993e7e.pdf", is_fs_data=True, fiscal_period="FY2025",
    model_impact="The primary historical year. Every forecast line ties back to these "
                 "printed figures; nothing between revenue and net profit is derived when "
                 "the statement prints it.")

f_fy24 = R.add(
    Ring.COMPANY, "official financial statements", FindingClass.D,
    "FY2024 as filed in its own audited statement: operating revenues EGP 82 036 929 "
    "thousand, operating costs (51 241 962), gross profit 30 794 967, operating profit "
    "17 657 834, income tax (451 127), net profit 10 111 328, EPS EGP 4.79. THE FY2025 "
    "STATEMENT RE-PRESENTS THE SAME YEAR at revenue 81 677 812 and operating profit "
    "17 356 527 — the difference of 359 117 in revenue is exactly the discontinued-"
    "operations revenue the FY2025 segment note carries on its own line, and the net profit "
    "of 10 111 328 is identical on both presentations",
    "Telecom Egypt FY2024 audited consolidated financial statements, Consolidated Statement "
    "of Income, page 2 (OCR route off the rendered pixels — the file carries no text layer "
    "at all; both the FY2024 and the FY2023 column were re-added and foot exactly)",
    CO, "2025-02-01",
    url="https://ir.te.eg/IRMedia/Financial_Information/EAS_Consolidated_Statement/2025/EAS_Consolidated_Statement7a64a1df-6064-45ee-9b5c-544641710870.pdf", is_fs_data=True, fiscal_period="FY2024",
    model_impact="Second historical year, and the reason a naive FY2024-to-FY2025 revenue "
                 "growth rate is wrong by 0.44pp unless the discontinued-operations "
                 "re-presentation is applied to both ends. The reconciliation is carried "
                 "explicitly in the historical table rather than smoothed.")

f_fy23 = R.add(
    Ring.COMPANY, "official financial statements", FindingClass.D,
    "FY2023 as filed: operating revenues EGP 56 679 153 thousand, operating costs "
    "(34 289 981), gross profit 22 389 172, operating profit 12 266 386, share of profit of "
    "equity accounted investees 5 032 657, net profit 11 472 963, EPS EGP 5.70. THE FY2024 "
    "STATEMENT RESTATES the same year's associate income to 5 280 319 and net profit to "
    "11 720 625 with EPS 5.85 — a restatement of EGP 247 662 thousand that runs straight "
    "through to the bottom line. Balance sheet as filed: total assets 150 640 094, equity "
    "50 884 932",
    "Telecom Egypt FY2023 audited consolidated financial statements, Consolidated Statement "
    "of Income page 2 and Consolidated Statement of Financial Position page 1 (OCR route; "
    "both columns re-added and foot, including the FY2022 comparative)",
    CO, "2024-02-01",
    url="https://ir.te.eg/IRMedia/Financial_Information/EAS_Consolidated_Statement/2024/EAS_Consolidated_Statement7d145cd3-847d-454a-b361-bd492cf5ed51.pdf", is_fs_data=True, fiscal_period="FY2023",
    model_impact="Third historical year. The restatement is why the Fact Book's FY2023 net "
                 "profit of 11 720.6 does not match the FY2023 filing's 11 473.0 — the "
                 "workbook carries the restated comparative, and the study must pick one "
                 "vintage and say which, rather than mixing them across a growth series.")

f_fy22 = R.add(
    Ring.COMPANY, "official financial statements", FindingClass.D,
    "FY2022 comparative, audited: operating revenues EGP 44 273 344 thousand, operating "
    "costs (26 485 370), gross profit 17 787 974, operating profit 9 590 237, net finance "
    "cost (1 630 455), share of profit of equity accounted investees 2 695 038, net profit "
    "9 187 456, EPS EGP 4.61. Balance sheet: total assets 119 239 737, total equity "
    "46 267 850, of which fixed assets and projects under construction 59 818 733",
    "Telecom Egypt FY2023 audited consolidated financial statements, prior-year "
    "(reclassified) column of the Statement of Income and Statement of Financial Position "
    "(OCR route; foots — the OCR read '$272' for the non-controlling interest of 5 272 and "
    "the addition recovered it)",
    CO, "2024-02-01",
    url="https://ir.te.eg/IRMedia/Financial_Information/EAS_Consolidated_Statement/2024/EAS_Consolidated_Statement7d145cd3-847d-454a-b361-bd492cf5ed51.pdf", is_fs_data=True, fiscal_period="FY2022",
    model_impact="Fourth historical year, which takes the depth to the protocol's target of "
                 "four rather than its floor of two. It is also the pre-devaluation base "
                 "year: revenue has grown 2.41x from FY2022 to FY2025 against a USD/EGP move "
                 "on the company's own closing rates from 24.69 to 47.65, which is what "
                 "separates the price/volume "
                 "component of growth from the currency component.")

f_q1 = R.add(
    Ring.COMPANY, "official financial statements", FindingClass.D,
    "Q1-2026 interim: operating revenues EGP 28 210 642 thousand, operating costs "
    "(16 015 081), gross profit 12 195 561, operating profit 8 618 239, net finance cost "
    "(7 757 973), share of associates 3 730 952, net profit 3 575 914, EPS EGP 2.09. Net "
    "profit FELL 23% year on year on a 14% revenue rise, entirely because of a non-cash FX "
    "loss the company sizes at EGP 5.3bn",
    "Telecom Egypt Q1-2026 condensed consolidated interim financial statements, Statement "
    "of Profit or Loss page 2, limited review by KPMG Hazem Hassan (OCR route). The OCR "
    "returned a net finance cost of 7 737 973 which does NOT foot against the printed "
    "pre-tax subtotal of 4 591 218; the figure that foots is 7 757 973, independently "
    "confirmed by the Fact Book. Arithmetic decided it, not the extractor",
    CO, "2026-05-21",
    url="https://ir.te.eg/IRMedia/Financial_Information/EAS_Consolidated_Statement/2026/EAS_Consolidated_Statement33dc1e9f-a5b4-4ac0-a9c6-08be870f5ee7.pdf", is_fs_data=True, fiscal_period="Q1-2026",
    model_impact="First quarter of the study year, swept BEFORE the build. It sets the "
                 "starting margin (43.2% gross, 30.6% operating) and it is the standing "
                 "warning that this company's reported net profit is dominated by an FX "
                 "revaluation the operating model does not produce.")

f_q2 = R.add(
    Ring.COMPANY, "official financial statements", FindingClass.D,
    "H1-2026 interim, with the Q2 quarter shown separately: H1 operating revenues EGP "
    "59 215 908 thousand, operating costs (33 730 381), gross profit 25 485 527, operating "
    "profit 17 582 442, share of associates 9 105 076, net profit 15 409 984, EPS EGP 9.02. "
    "Q2 alone: revenue 31 005 266, gross profit 13 289 966, operating profit 8 964 203, a "
    "net finance GAIN of 908 021, and net profit 11 834 070 — up 102% year on year. Balance "
    "sheet at 30 June 2026: total assets 236 024 417, total equity 73 666 236, long-term "
    "loans 29 044 630 and short-term 42 463 030",
    "Telecom Egypt H1-2026 condensed consolidated interim financial statements, Statement of "
    "Profit or Loss page 2 and Statement of Financial Position page 1, LIMITED REVIEW "
    "conclusion by KPMG Hazem Hassan, Cairo 13 August 2026 (OCR route; every subtotal on "
    "both pages re-added and foots exactly, including the FY2025 comparative column)",
    CO, "2026-08-13",
    url="https://ir.te.eg/IRMedia/Financial_Information/EAS_Consolidated_Statement/2026/EAS_Consolidated_Statementc4505d23-5a0e-4824-ba97-b5951592597e.pdf", is_fs_data=True, fiscal_period="Q2-2026",
    model_impact="Second quarter of the study year, swept BEFORE the build, and it is the "
                 "one that matters: it carries the first period of NTRA-approved pricing and "
                 "an FX movement in the opposite direction to Q1. H1 gross margin of 43.0% "
                 "and a 45% EBITDA margin are the live starting point for the margin path, "
                 "not the FY2025 full-year average.")

f_review = R.add(
    Ring.COMPANY, "official financial statements", FindingClass.S,
    "The 2026 interims are REVIEWED, not audited. KPMG's Q2-2026 conclusion is the limited-"
    "review negative-assurance form under Egyptian Accounting Standard 30, while both "
    "earnings releases describe the same numbers as 'audited financial results'. The FY2025 "
    "annual set is a full audit with an unqualified opinion and an emphasis of matter",
    "Telecom Egypt H1-2026 condensed consolidated interim financial statements, limited "
    "review report page 4 (OCR route), read against the H1-2026 Earnings Release of "
    "13 August 2026",
    CO, "2026-08-13",
    url="https://ir.te.eg/IRMedia/Financial_Information/EAS_Consolidated_Statement/2026/EAS_Consolidated_Statementc4505d23-5a0e-4824-ba97-b5951592597e.pdf", fiscal_period="Q2-2026",
    model_impact="Assurance level is stated in the study's own source table rather than "
                 "inherited from the release's wording. It does not change a number; it "
                 "changes what the reader is told the number rests on.")

# ---- Company: regular disclosures (the notes the build actually consumes) ----------------
f_seg = R.add(
    Ring.COMPANY, "regular disclosures", FindingClass.D,
    "Revenue is disclosed on TWO different cuts, and both foot. By business unit (note 5): "
    "FY2025 Home and personal communications EGP 52 086 310 thousand, Enterprise 9 788 235, "
    "Domestic wholesale 10 293 543, International carriers 18 202 241, International cables "
    "and networks 16 302 617. By operating segment (note 41), with costs attached: "
    "Communications, marine cables and infrastructure revenue 58 977 725 against costs "
    "(38 514 405) for a 34.7% gross margin, Internet 42 808 010 against (20 121 214) for "
    "53.0%, Outsourcing 4 057 050 against (2 536 673) for 37.5%, All other 830 161 against "
    "(661 544)",
    "Telecom Egypt FY2025 audited consolidated financial statements, note 5 'Operating "
    "revenues' and note 41 'Segment reporting' (TEXT route; both notes re-added and foot to "
    "106 672 946 and to 61 833 836 for FY2025 and to the FY2024 equivalents)",
    CO, "2026-02-26",
    url="https://ir.te.eg/IRMedia/Financial_Information/EAS_Consolidated_Statement/2026/EAS_Consolidated_Statement38a2837b-8610-4c24-aa82-ac57ea993e7e.pdf", is_fs_data=True, fiscal_period="FY2025",
    model_impact="DRIVER UNLOCK for the cost side. Note 41 is the only disclosure that "
                 "attaches COST to a revenue grouping, so it is what makes a gross margin an "
                 "output at segment level rather than an input. The two cuts do not map onto "
                 "each other and the study reconciles them explicitly instead of assuming.")

f_costs_detail = R.add(
    Ring.COMPANY, "regular disclosures", FindingClass.D,
    "Below gross profit the statements name every line again. FY2025 selling and "
    "distribution of EGP 6 078 657 thousand breaks into 10 disclosed lines led by salaries "
    "and wages 2 975 311, advertising and marketing 1 341 992 and agents' commissions and "
    "collection contracts 1 088 573. General and administrative of 8 641 814 is led by "
    "salaries and wages 4 968 233, with end-of-service compensation 166 149 and a loyalty "
    "and belonging fund contribution of 250 000. Depreciation of EGP 14 781 067 is allocated "
    "across operating costs 14 612 060, selling 27 808, G&A 126 551 and discontinued 14 648",
    "Telecom Egypt FY2025 audited consolidated financial statements, notes 8, 9 and 16 "
    "(TEXT route; note 8 re-added and foots to 6 078 657 for FY2025 and 5 415 716 for FY2024)",
    CO, "2026-02-26",
    url="https://ir.te.eg/IRMedia/Financial_Information/EAS_Consolidated_Statement/2026/EAS_Consolidated_Statement38a2837b-8610-4c24-aa82-ac57ea993e7e.pdf", is_fs_data=True, fiscal_period="FY2025",
    model_impact="Extends the cost stack below gross profit so operating margin is an output "
                 "too, not only gross margin. Total employee cost across all three captions "
                 "is EGP 16.07bn, the second-largest cost in the business after call cost — "
                 "which is exactly why the missing headcount (F50) matters.")

f_debt = R.add(
    Ring.COMPANY, "regular disclosures", FindingClass.D,
    "Debt is disclosed facility by facility with its currency, maturity and rate basis. At "
    "31 December 2025 total loans and credit facilities were EGP 73 758 796 thousand: USD "
    "foreign loans 30 426 074 (USD 368 533 thousand) maturing in quarterly instalments to "
    "08/11/2029, EUR foreign loans 850 132 to 30/06/2036, EGP local loans 18 045 800 to "
    "06/11/2031, EGP bank facilities 21 353 382, USD bank facilities 3 078 986 ending "
    "31/12/2026 and EUR supplier facilities 4 422. ALL SIX ARE VARIABLE RATE. Currency mix: "
    "45.4% USD, 1.2% EUR, 53.4% EGP against 59.3% / 1.1% / 39.6% a year earlier",
    "Telecom Egypt FY2025 audited consolidated financial statements, note 27 'Loans and "
    "credit facilities' (TEXT route; the short-term column foots to 38 433 287, the "
    "long-term to 35 325 509 and the two agree with the balance sheet, both years)",
    CO, "2026-02-26",
    url="https://ir.te.eg/IRMedia/Financial_Information/EAS_Consolidated_Statement/2026/EAS_Consolidated_Statement38a2837b-8610-4c24-aa82-ac57ea993e7e.pdf", is_fs_data=True, fiscal_period="FY2025",
    model_impact="DRIVER UNLOCK for interest and for FX. Interest is built facility by "
                 "facility against its own currency's policy path rather than as one blended "
                 "rate on average debt. The 13.8pp swing OUT of foreign-currency debt in a "
                 "single year is itself a driver: it cuts the revaluation exposure that "
                 "produced the Q1-2026 loss. Note 27 states no coupon, only 'variable', so "
                 "the spread is solved against the disclosed finance cost and flagged.")

f_fxexp = R.add(
    Ring.COMPANY, "regular disclosures", FindingClass.D,
    "The net foreign-currency position is disclosed in full. At 31 December 2025 assets in "
    "foreign currency were EGP 22 432 505 thousand against liabilities of EGP 69 628 968, a "
    "NET DEFICIT of EGP 47 196 463 (FY2024: 44 179 862), short USD 594 794 thousand, EUR "
    "225 659 thousand and Chinese Yuan 1 054 237 thousand. The company's own sensitivity "
    "states that a 10% strengthening of foreign currencies costs EGP 4 719 646 thousand — "
    "which is precisely 10% of the disclosed net deficit and confirms the linearity",
    "Telecom Egypt FY2025 audited consolidated financial statements, notes 40-3 'Currency "
    "risk exposure' and 40-4 'Sensitivity analysis' (TEXT route; the disclosed sensitivity "
    "reproduces exactly from the disclosed net position, both years)",
    CO, "2026-02-26",
    url="https://ir.te.eg/IRMedia/Financial_Information/EAS_Consolidated_Statement/2026/EAS_Consolidated_Statement38a2837b-8610-4c24-aa82-ac57ea993e7e.pdf", is_fs_data=True, fiscal_period="FY2025",
    model_impact="DRIVER UNLOCK. The FX line becomes a computed output of a disclosed net "
                 "monetary position times a modelled rate path, not a plug. The CNY leg is "
                 "vendor financing from network-equipment suppliers and moves on a different "
                 "rate from the USD leg, so it is escalated separately.")

f_vfe = R.add(
    Ring.COMPANY, "regular disclosures", FindingClass.D,
    "The Vodafone Egypt holding is disclosed at 44.95% — 107 869 799 shares — NOT the 45% "
    "the company's own press boilerplate rounds it to. Carrying value EGP 30 662 412 "
    "thousand at 31/12/2025 from 18 654 705, rolled forward by share of profit 14 760 634 "
    "less accrued dividends 2 477 474 and employee dividends 275 453. Vodafone Egypt's own "
    "accounts are given: revenues EGP 109 601 000 thousand, profit before tax 42 570 000, "
    "net profit 32 841 000, equity 57 720 856. Vodafone Egypt's year ends 31 March, so the "
    "group's share is stitched from three stub periods, which is why 44.95% of 32 841 000 "
    "gives 14 762 030 against the 14 760 634 recognised",
    "Telecom Egypt FY2025 audited consolidated financial statements, note 20 'Equity "
    "accounted investees' and note 20-1 (TEXT route; the holding total foots to 30 738 330 "
    "and agrees with the balance sheet, and Vodafone Egypt's own balance sheet foots to "
    "57 720 856)",
    CO, "2026-02-26",
    url="https://ir.te.eg/IRMedia/Financial_Information/EAS_Consolidated_Statement/2026/EAS_Consolidated_Statement38a2837b-8610-4c24-aa82-ac57ea993e7e.pdf", is_fs_data=True, fiscal_period="FY2025",
    model_impact="DRIVER UNLOCK, and it is a third of the earnings. The stake is modelled as "
                 "its own bottom-up leg on Vodafone Egypt's disclosed accounts at 44.95%, "
                 "never as a percentage of Telecom Egypt's own profit. The March year-end "
                 "stitch is carried explicitly as a one-quarter lag rather than ignored.")

f_vferp = R.add(
    Ring.COMPANY, "regular disclosures", FindingClass.S,
    "Telecom Egypt and Vodafone Egypt trade with each other at scale and the flows run both "
    "ways: FY2025 charges TO Telecom Egypt for outgoing calls and voice services EGP "
    "7 227 398 thousand, and charges BY Telecom Egypt for incoming and international calls, "
    "transmission claims and the lease of premises and towers EGP 5 712 999 thousand, "
    "leaving a net credit balance due to the associate of EGP 4 543 996 thousand at "
    "31/12/2025 against 2 468 657 a year earlier",
    "Telecom Egypt FY2025 audited consolidated financial statements, note 37-1 'Credit "
    "balances due to associates' (TEXT route)",
    CO, "2026-02-26",
    url="https://ir.te.eg/IRMedia/Financial_Information/EAS_Consolidated_Statement/2026/EAS_Consolidated_Statement38a2837b-8610-4c24-aa82-ac57ea993e7e.pdf", is_fs_data=True, fiscal_period="FY2025",
    model_impact="Roughly EGP 5.7bn of Telecom Egypt's own revenue is billed to the "
                 "associate it owns 44.95% of, and EGP 7.2bn of its cost is billed by it. "
                 "The two legs cannot be forecast independently without double-counting the "
                 "same traffic, and the working-capital driver has to carry the balance that "
                 "swings between them.")

f_cap = R.add(
    Ring.COMPANY, "regular disclosures", FindingClass.D,
    "Issued and fully paid capital is EGP 17 070 716 thousand in 1 707 071 600 shares at "
    "EGP 10 par. Earnings per share is struck on net profit AFTER deducting the employees' "
    "share of 2 120 728 thousand and the board's share of 63 089 thousand, giving profit "
    "available for distribution of 20 370 815 and EPS of EGP 11.93 — so 9.7% of FY2025 "
    "profit never reaches shareholders",
    "Telecom Egypt FY2025 audited consolidated financial statements, note 15 'Basic and "
    "diluted earnings per share' and note 31 'Capital' (TEXT route; EPS reproduces from the "
    "disclosed numerator and share count)",
    CO, "2026-02-26",
    url="https://ir.te.eg/IRMedia/Financial_Information/EAS_Consolidated_Statement/2026/EAS_Consolidated_Statement38a2837b-8610-4c24-aa82-ac57ea993e7e.pdf", is_fs_data=True, fiscal_period="FY2025",
    model_impact="Fixes the share count with no aggregator involved and, more consequential, "
                 "fixes the EQUITY BRIDGE: the statutory employee and board profit share is "
                 "a real, recurring, roughly 9-10% leakage between group net profit and "
                 "distributable earnings. A per-share value built off group profit without "
                 "it is overstated by that margin.")

f_intang = R.add(
    Ring.COMPANY, "regular disclosures", FindingClass.D,
    "The asset base is dated and its lives are disclosed. Fixed assets and projects under "
    "construction stood at EGP 119 828 621 thousand at 31/12/2025 (H1-2026: 122 873 752), "
    "on straight-line lives of 5-50 years for buildings and infrastructure, 3-15 for "
    "technical equipment and information technology, 7-15 for vehicles, 5-10 for furniture "
    "and 2-8 for tools. Mobile licences and frequencies carry at 18 057 470 net of "
    "7 760 938 accumulated amortisation, after EGP 4 953 550 was transferred in from "
    "projects under construction during FY2025 and FY2025 amortisation of 1 776 112",
    "Telecom Egypt FY2025 audited consolidated financial statements, accounting policy 4-3 "
    "(C), note 16 and note 17 (TEXT route; the intangible roll re-added and foots to a net "
    "18 066 436 which agrees with the balance sheet)",
    CO, "2026-02-26",
    url="https://ir.te.eg/IRMedia/Financial_Information/EAS_Consolidated_Statement/2026/EAS_Consolidated_Statement38a2837b-8610-4c24-aa82-ac57ea993e7e.pdf", is_fs_data=True, fiscal_period="FY2025",
    model_impact="DRIVER UNLOCK for depreciation and amortisation and the input to the "
                 "[R-ASSET-01] asset-base vintage test. Depreciation is built off the "
                 "disclosed gross base and its own lives rather than held at a ratio to "
                 "revenue, and licence amortisation runs off the disclosed licence carrying "
                 "value over its stated term.")

# ---- Company: IR communications ----------------------------------------------------------
f_kpi = R.add(
    Ring.COMPANY, "IR communications (calls, presentations, releases)", FindingClass.D,
    "The Fact Book workbook carries the unit economics no financial statement holds, "
    "quarterly from Q1-2023 to Q2-2026 on seven sheets. Subscribers at Q2-2026 (thousands): "
    "Home and Consumer fixed voice 13 136.1 and fixed data 11 124.7; Enterprise fixed voice "
    "1 203.3 and fixed data 346.2; mobile 15 214. Published ARPU at Q2-2026 (EGP/month): "
    "H&C fixed voice 40.07 and ADSL 373.75; Enterprise fixed voice 146.41 and ADSL 431.40. "
    "Revenue is broken to 20 sub-lines including cable projects, cables operations and "
    "maintenance, capacity sales, data centre and international customer support, and "
    "in-service capex is given by quarter (Q2-2026 EGP 3 578.6mn)",
    "Telecom Egypt Fact Book Q2-2026 (.xlsx), sheets 'Operational KPIs', 'Revenue "
    "breakdown', 'KPIs Highlight' — XLSX route. The subscriber totals reconcile exactly to "
    "the H1-2026 Earnings Release: 13 136.1 + 1 203.3 = 14 339 voice and 11 124.7 + 346.2 = "
    "11 471 data, both as printed in the release",
    IR, "2026-08-13",
    url="https://ir.te.eg/IRMedia/Financial_Information/Fact_Book/2026/Fact_Book92ac7121-bc3f-4f4f-b5a3-b2ebb564abbb.xlsx", fiscal_period="Q2-2026",
    model_impact="DRIVER UNLOCK, and the reason the retail legs can be built as volume times "
                 "price at all. Subscribers by segment are the volume driver directly. The "
                 "published ARPU is NOT the price driver — see F33.")

f_arpu = R.add(
    Ring.COMPANY, "IR communications (calls, presentations, releases)", FindingClass.S,
    "THE PUBLISHED ARPU AND THE PUBLISHED REVENUE DO NOT MULTIPLY TOGETHER. For Q2-2026 the "
    "company prints a Home and Consumer fixed-voice ARPU of EGP 40.07 a month; its own "
    "disclosed H&C voice revenue of EGP 2 000 861 thousand over its own disclosed average "
    "H&C voice subscribers of 13 107 thousand gives EGP 50.88 — the printed rate is 21.2% "
    "below the derived one. For H&C data the printed ADSL ARPU of EGP 373.75 against a "
    "derived EGP 434.05 is 13.9% below, and there the derived rate is contaminated in the "
    "other direction because retail MOBILE data revenue also sits inside the H&C 'Data' "
    "line. The company's ARPU is computed on its own base, which it does not define",
    "Telecom Egypt Fact Book Q2-2026, sheets 'Operational KPIs' and 'Revenue breakdown', "
    "reconciled arithmetically at this desk (XLSX route)",
    IR, "2026-08-13",
    url="https://ir.te.eg/IRMedia/Financial_Information/Fact_Book/2026/Fact_Book92ac7121-bc3f-4f4f-b5a3-b2ebb564abbb.xlsx", fiscal_period="Q2-2026",
    model_impact="Decides the SHAPE of the price driver, and it is the single most "
                 "consequential finding in the Company ring. The published ARPU is used as a "
                 "GROWTH INDICATOR only; the LEVEL is back-solved against disclosed segment "
                 "revenue, so the price leg is a DERIVED rate, not a disclosed one. The "
                 "study states that the unit build is half-disclosed — volumes yes, prices "
                 "no — rather than letting a reader infer both were sourced.")

f_rel = R.add(
    Ring.COMPANY, "IR communications (calls, presentations, releases)", FindingClass.B,
    "The H1-2026 results announcement of 13 August 2026 is the NEWEST release and its "
    "anchors supersede the FY2025 set. Revenue EGP 59.2bn (+17%), EBITDA EGP 26.4bn at a "
    "45% margin, net profit EGP 15.4bn (+47%) at a 26% margin against 21% in H1-2025. "
    "In-service capex EGP 4.9bn or 8% of sales, cash capex including licence EGP 18.6bn. "
    "Net debt to annualised EBITDA 1.2x from 1.6x. FCFF EGP 10.0bn, 38% of EBITDA. Segment "
    "revenue for H1: Home and Consumer 30 731, Enterprise 5 456, Domestic Wholesale 6 050, "
    "International Carriers 11 729, International Customers and Networks 5 249",
    "Telecom Egypt H1 2026 Earnings Release, 13 August 2026 (OCR route off the rendered "
    "pixels; the document carries no text layer)",
    IR, "2026-08-13",
    url="https://ir.te.eg/IRMedia/Financial_Information/Earnings_Release/2026/Earnings_Release6e0e975f-190e-438d-926e-1ac077443e9c.pdf", fiscal_period="Q2-2026",
    model_impact="BASE CHANGER for the driver set. Every operating anchor the study starts "
                 "from is taken from this release rather than from FY2025: the 45% EBITDA "
                 "margin, the 1.2x leverage, the 8%-of-sales in-service capex run-rate and "
                 "the segment mix. Where an older figure is kept, the study says why.")

f_ebit = R.add(
    Ring.COMPANY, "IR communications (calls, presentations, releases)", FindingClass.S,
    "The earnings releases print an 'EBIT' line that EXCEEDS their own EBITDA line — H1-2026 "
    "EBIT of EGP 26 714mn against EBITDA of EGP 26 436mn, and Q2-2026 EBIT of 14 359 against "
    "EBITDA of 13 815. That cannot be true of EBITDA less depreciation and amortisation. The "
    "gap is associate income: the audited operating profit for H1-2026 is EGP 17 582 442 "
    "thousand, and the release's EBIT only approaches its printed value once the EGP 9 105 "
    "076 thousand share of Vodafone Egypt's profit is added back in",
    "Telecom Egypt H1 2026 Earnings Release, Income Statement Summary (OCR route), "
    "reconciled against the H1-2026 interim Statement of Profit or Loss",
    IR, "2026-08-13",
    url="https://ir.te.eg/IRMedia/Financial_Information/Earnings_Release/2026/Earnings_Release6e0e975f-190e-438d-926e-1ac077443e9c.pdf", fiscal_period="Q2-2026",
    model_impact="The release's EBIT is NOT an operating-profit measure and is not used as "
                 "one anywhere in the model. Operating profit comes from the statements. Any "
                 "multiple struck on EV must use the audited operating profit or an EBITDA "
                 "that excludes associate income, or it double-counts the stake that the "
                 "sum-of-parts already values separately.")

f_call = R.add(
    Ring.COMPANY, "IR communications (calls, presentations, releases)", FindingClass.C,
    "Conference-call transcripts are published for every quarter alongside the release and "
    "the presentation; Q4-2025, Q1-2026 and Q2-2026 were downloaded from the investor site. "
    "The results presentation adds the series the release does not: total debt and net debt "
    "by year FY2021-FY2025 (net debt 13 401 / 24 297 / 38 786 / 73 197 / 62 862 EGP mn), "
    "foreign-currency debt in dollars (USD 955 / 1 076 / 1 070 / 968 / 721mn) and net "
    "debt/EBITDA including vendor financing (1.4x / 1.8x / 2.3x / 2.9x / 1.8x)",
    "Telecom Egypt FY2025 Results Presentation, 'Balance Sheet Highlights' slide, and the "
    "conference-call transcript library at ir.te.eg/en/FinancialInformation/QuarterlyResults",
    IR, "2026-02-26",
    url="https://ir.te.eg/IRMedia/Financial_Information/Results_Presentation/2026/Results_Presentationa4a1acb0-d65f-4d34-aa15-552b56bf9e3a.pdf", fiscal_period="FY2025",
    model_impact="")

f_netdebt = R.add(
    Ring.COMPANY, "IR communications (calls, presentations, releases)", FindingClass.D,
    "The company's own net-debt definition is derivable and it reproduces exactly. FY2025 "
    "net debt of EGP 62 862mn equals total debt 73 759 less cash and cash equivalents 8 312 "
    "less financial assets at amortised cost - treasury bills 2 585. On EBITDA of 47 495 "
    "that gives 1.32x, which is the 1.3x the company reports; FY2024 gives 73 197 / 32 623 "
    "= 2.24x against the reported 2.2x. It excludes vendor-financing obligations, which the "
    "company reports on a SEPARATE and higher ladder reaching 2.9x in FY2024",
    "Telecom Egypt FY2025 Results Presentation and FY2025 Earnings Release (26 February "
    "2026), reconciled against the audited balance sheet",
    IR, "2026-02-26",
    url="https://ir.te.eg/IRMedia/Financial_Information/Results_Presentation/2026/Results_Presentationa4a1acb0-d65f-4d34-aa15-552b56bf9e3a.pdf", fiscal_period="FY2025",
    model_impact="DRIVER UNLOCK for the enterprise-to-equity bridge. The bridge uses the "
                 "company's own definition so the leverage the study quotes is the leverage "
                 "the company quotes, and the vendor-financing ladder is reported ALONGSIDE "
                 "it rather than blended into it — the two differ by half a turn.")

# ---- Company: strategy and guidance -------------------------------------------------------
f_guid = R.add(
    Ring.COMPANY, "strategic plans & guidance", FindingClass.D,
    "The Board approved the FY2026 budget on 11 December 2025 and published four KPI "
    "guidance ranges: revenue growth in the high single digits, EBITDA margin in the low "
    "forties, in-service capex-to-sales in the low twenties and a positive FCFF-to-EBITDA "
    "ratio in the mid-thirties. FY2025 actual against FY2025 guidance was a beat on every "
    "one: 31% growth against low twenties, a 45% EBITDA margin against high thirties, "
    "in-service capex 19% and cash capex 28% of sales against low twenties, and FCFF/EBITDA "
    "44% against early forties",
    "Telecom Egypt 2026 Guidance announcement of 11 December 2025, carried in the FY2025 "
    "Results Presentation, 'Our Performance in Context' slide",
    IR, "2025-12-11",
    url="https://ir.te.eg/IRMedia/Financial_Information/Results_Presentation/2026/Results_Presentationa4a1acb0-d65f-4d34-aa15-552b56bf9e3a.pdf",
    model_impact="DRIVER UNLOCK, and it is scored rather than consumed. The guidance bands "
                 "are the management prior; the model is built from the sourced unit "
                 "economics and the two are then compared, with the one-year beat record on "
                 "all four metrics reported as evidence about the prior's conservatism.")

f_beat = R.add(
    Ring.COMPANY, "strategic plans & guidance", FindingClass.S,
    "On 21 May 2026 the company said it expects to EXCEED its FY2026 guidance of "
    "high-single-digit revenue growth on the back of the NTRA tariff adjustment, while "
    "maintaining the EBITDA margin in the low forties, in-service capex-to-sales in the low "
    "twenties and FCFF-to-EBITDA in the mid-thirties, subject to macroeconomic and FX "
    "stability. H1-2026 revenue growth of 17% is running at roughly twice the guided rate",
    "Telecom Egypt Q1 2026 Earnings Release, 21 May 2026, chief executive's statement (TEXT "
    "route), read against the H1 2026 Earnings Release of 13 August 2026",
    IR, "2026-05-21",
    url="https://ir.te.eg/IRMedia/Financial_Information/Earnings_Release/2026/Earnings_Release3da58290-416c-4151-92f9-68f3a4e7461f.pdf", fiscal_period="Q1-2026",
    model_impact="Raises the explicit-window revenue driver above the published guidance "
                 "band and dates the reason. The condition management attaches — FX "
                 "stability — is carried into the model as the sensitivity axis rather than "
                 "dropped.")

# ---- Company: one-off base-resetting transactions ------------------------------------------
f_fire = R.add(
    Ring.COMPANY, "one-off base-resetting transactions", FindingClass.B,
    "On 7 July 2025 a fire broke out in an equipment room of the Ramses Central building, "
    "one of the main hubs of Egypt's telecommunications infrastructure. The cost of the "
    "disposed assets was EGP 2 343 107 thousand and the capital loss recognised EGP "
    "1 483 568 thousand, against which EGP 200 million was received from insurers as an "
    "interim payment; the remaining claim is open pending the completion of official "
    "investigations. The auditor placed an emphasis of matter on it in the FY2025 opinion "
    "and repeated it in the H1-2026 review conclusion",
    "Telecom Egypt FY2025 audited consolidated financial statements, note 43-1 and the "
    "auditor's report (TEXT route for the note, OCR route for the auditor's report page, "
    "which carries no text layer)",
    CO, "2026-02-26",
    url="https://ir.te.eg/IRMedia/Financial_Information/EAS_Consolidated_Statement/2026/EAS_Consolidated_Statement38a2837b-8610-4c24-aa82-ac57ea993e7e.pdf", is_fs_data=True, fiscal_period="FY2025",
    model_impact="BASE CHANGER, dual-framed. The EGP 1.48bn capital loss sits in FY2025 "
                 "'Other expenses' — which is why that line jumped from 556 146 to 2 314 623 "
                 "— and it is NOT recurring, so the normalised FY2025 base adds it back. The "
                 "outstanding insurance claim is a contingent ASSET modelled at zero in the "
                 "base and shown in the upside, never accrued.")

f_rdh = R.add(
    Ring.COMPANY, "one-off base-resetting transactions", FindingClass.B,
    "The Regional Data Hub monetisation is DEAD, and the two ends of it are in two different "
    "documents. The FY2025 statements record that on 3 September 2025 the Board granted "
    "preliminary approval to a binding offer for a 75%-80% stake in a subsidiary that would "
    "own the Regional Data Hub, with terms and conditions signed. The H1-2026 release then "
    "records, dated 16 July 2026, that Telecom Egypt will NOT proceed with the proposed RDH "
    "transaction with Helios Investments, and describes the data-centre business as a "
    "'wholly owned' subsidiary",
    "Telecom Egypt FY2025 audited consolidated financial statements, note 43-2 (TEXT route), "
    "superseded by the H1 2026 Earnings Release of 13 August 2026, main events (OCR route)",
    CO, "2026-08-13",
    url="https://ir.te.eg/IRMedia/Financial_Information/Earnings_Release/2026/Earnings_Release6e0e975f-190e-438d-926e-1ac077443e9c.pdf", fiscal_period="Q2-2026",
    model_impact="BASE CHANGER, and it removes a cash inflow a study written off the FY2025 "
                 "statements alone would have carried. There is no disposal proceed and no "
                 "deconsolidation; the data-centre revenue line — EGP 418 184 thousand in "
                 "Q4-2025 rising to 451 179 in Q2-2026 — stays fully in the forecast at 100% "
                 "ownership. Dual-framed against the counterfactual in which it had closed.")

f_dtax = R.add(
    Ring.COMPANY, "one-off base-resetting transactions", FindingClass.S,
    "THE FY2025 BALANCE SHEET EXISTS ON TWO BASES AND BOTH FOOT. The audited statement nets "
    "deferred tax, showing no deferred tax asset, a deferred tax liability of EGP 1 869 989 "
    "thousand and total assets of 225 882 527. The H1-2026 interim re-presents the same date "
    "GROSS and labels it 'Reclassified' — deferred tax asset 5 176 125, liability 7 046 114, "
    "total assets 231 058 652, a difference of exactly 5 176 125. The Fact Book, the Q1-2026 "
    "release and the H1-2026 release all use the gross basis; only the FY2025 audited "
    "statement and the FY2025 release use the net one",
    "Telecom Egypt FY2025 audited Consolidated Statement of Financial Position (OCR route) "
    "against the H1-2026 interim Statement of Financial Position, FY2025 comparative column "
    "(OCR route) — both re-added and both foot to their own totals",
    CO, "2026-08-13",
    url="https://ir.te.eg/IRMedia/Financial_Information/EAS_Consolidated_Statement/2026/EAS_Consolidated_Statementc4505d23-5a0e-4824-ba97-b5951592597e.pdf", is_fs_data=True, fiscal_period="Q2-2026",
    model_impact="Not a valuation driver, but it decides whether the historical total-asset "
                 "and returns series has a 2.3% step in it that is pure presentation. The "
                 "study carries ONE basis across all four years and states which. It also "
                 "means any FY2025 balance-sheet figure quoted from a Telecom Egypt document "
                 "has to be checked for which basis it came off.")

f_socie = R.add(
    Ring.COMPANY, "one-off base-resetting transactions", FindingClass.S,
    "THE FY2025 CONSOLIDATED STATEMENT OF CHANGES IN EQUITY DOES NOT FOOT. Its printed FY2025 "
    "'Total transactions with shareholders' is (2 249 264) while the rows printed above it "
    "sum to (4 809 871): the EGP 2 560 607 thousand dividend for 2024 is listed but not "
    "carried into the subtotal, and the same happens to the EGP 5 613 thousand "
    "non-controlling dividend. Its closing retained earnings of 41 050 147 and total equity "
    "of 66 254 046 therefore exceed the balance sheet's 38 489 540 and 63 687 826 by exactly "
    "those amounts. The FY2024 rows on the same page foot correctly",
    "Telecom Egypt FY2025 audited consolidated financial statements, Consolidated Statement "
    "of Changes in Equity, page 4. READ BY BOTH ROUTES — the text layer and a 200dpi OCR of "
    "the rendered pixels return identical figures, so this is a defect in the filed document "
    "and not in the extraction. The balance sheet, note 41, the H1-2026 interim's FY2025 "
    "comparative and the Fact Book all agree at 38 489 540",
    CO, "2026-02-26",
    url="https://ir.te.eg/IRMedia/Financial_Information/EAS_Consolidated_Statement/2026/EAS_Consolidated_Statement38a2837b-8610-4c24-aa82-ac57ea993e7e.pdf", is_fs_data=True, fiscal_period="FY2025",
    model_impact="Closing equity, retained earnings and the dividend history are taken from "
                 "the BALANCE SHEET and the cash-flow statement, never from this page. A "
                 "book-value or return-on-equity lens built off the changes-in-equity "
                 "statement would overstate equity by EGP 2.57bn, 4.0%. Disclosed here so a "
                 "later reader who opens that page and gets a different number knows why.")

# ---- Company: ownership / stake changes (named-transaction rule) ---------------------------
f_own = R.add(
    Ring.COMPANY, "ownership / stake changes (named-transaction rule)", FindingClass.D,
    "Named and dated, not estimated. The Egyptian Government holds 70% of 1 707 071 600 "
    "shares through the Ministry of Finance; 20% was sold in the December 2005 public "
    "offering and a further 10% was placed during 2023, giving the current 30% free float. "
    "Telecom Egypt entered FTSE Russell's Emerging Markets index following a mid-cap upgrade",
    "Telecom Egypt FY2025 audited consolidated financial statements, note 31 'Capital' "
    "(TEXT route), and the company's own press release 'Telecom Egypt Enters FTSE Russell "
    "Emerging Markets Index Following Mid-Cap Upgrade' at ir.te.eg/en/CorporateNews",
    CO, "2026-02-26",
    url="https://ir.te.eg/IRMedia/Financial_Information/EAS_Consolidated_Statement/2026/EAS_Consolidated_Statement38a2837b-8610-4c24-aa82-ac57ea993e7e.pdf", is_fs_data=True, fiscal_period="FY2025",
    model_impact="Fixes the float at 30% and 512.1m shares. A further state placement is the "
                 "named overhang scenario, dated to nothing and therefore modelled as a "
                 "discount-rate/liquidity sensitivity rather than a cash-flow event.")

f_vfestake = R.add(
    Ring.COMPANY, "ownership / stake changes (named-transaction rule)", FindingClass.D,
    "The Vodafone Egypt stake is a NAMED and dated transaction, acquired between 2003 and "
    "2006 and held since at 44.95% — 107 869 799 shares of Vodafone Egypt Telecommunications "
    "Company. Two smaller associates are also disclosed: Egypt Trust at 35.71% (carrying "
    "value EGP 62 440 thousand) and New Matrix for Technology at 25.50% (13 478). The "
    "ownership percentage has not moved between FY2024 and FY2025",
    "Telecom Egypt FY2025 audited consolidated financial statements, note 20 (TEXT route), "
    "and the Corporate Presentation 2026 'Company Snapshot' for the acquisition dates",
    CO, "2026-02-26",
    url="https://ir.te.eg/IRMedia/Financial_Information/EAS_Consolidated_Statement/2026/EAS_Consolidated_Statement38a2837b-8610-4c24-aa82-ac57ea993e7e.pdf", is_fs_data=True, fiscal_period="FY2025",
    model_impact="The sum-of-the-parts stake leg is struck at the FILED 44.95%, not the 45% "
                 "the company's own boilerplate and the prior published edition both round "
                 "to. On an FY2025 associate contribution of EGP 14.83bn the rounding is "
                 "worth roughly EGP 16mn a year — small, and there is no reason to carry a "
                 "rounded figure when the exact one is filed.")

# ---- Company: management & capital actions -------------------------------------------------
f_div = R.add(
    Ring.COMPANY, "management & capital actions", FindingClass.D,
    "The Board proposed a dividend of EGP 1.50 per share for FY2025 on 26 February 2026, "
    "subject to General Assembly approval, and it was distributed on 30 April 2026. On "
    "1 707 071 600 shares that is EGP 2 560 607 thousand, which is the figure the FY2025 "
    "cash-flow statement shows paid for FY2024 and the identical amount paid the year "
    "before — the ordinary dividend has been held flat in nominal pounds for three years "
    "while earnings per share went from 4.79 to 11.93",
    "Telecom Egypt FY2025 Earnings Release of 26 February 2026 and Q1 2026 Earnings Release "
    "of 21 May 2026 for the payment date, reconciled to the FY2025 audited Consolidated "
    "Statement of Cash Flows (TEXT route), which foots from opening cash 7 565 330 to "
    "closing 7 684 542",
    CO, "2026-02-26",
    url="https://ir.te.eg/IRMedia/Financial_Information/Earnings_Release/2026/Earnings_Releasedf2a8cae-5863-43e4-ba1d-b9e575f4deaa.pdf", is_fs_data=True, fiscal_period="FY2025",
    model_impact="Sets the payout driver, and it is a LEVEL not a ratio: EGP 2.56bn flat "
                 "regardless of earnings, an 11.3% payout of FY2025 attributable profit "
                 "against 25.4% of FY2024's. A percentage-of-earnings payout assumption "
                 "would be contradicted by three years of the company's own behaviour.")

f_mgmt = R.add(
    Ring.COMPANY, "management & capital actions", FindingClass.S,
    "The management team turned over through 2025 and the structure was rebuilt. Board and "
    "executive leadership changes were announced on 25 March 2025 and again on 30 September "
    "2025, and on 31 December 2025 the Board approved an organisational transformation "
    "'designed to enhance strategic focus and operational agility'. The team is now Tamer El "
    "Mahdi as Managing Director and CEO with Wael Hanafy as CFO; the Q1-2026 release "
    "describes a reorganised retail structure sharpening focus on Enterprise, SME and SOHO "
    "and on fixed-mobile convergence",
    "Telecom Egypt FY2025 Results Presentation main-events pages and Corporate Presentation "
    "2026 leadership slide, with the officers' names as signed on the H1-2026 interim "
    "statements",
    IR, "2026-02-26",
    url="https://ir.te.eg/IRMedia/Financial_Information/Results_Presentation/2026/Results_Presentationa4a1acb0-d65f-4d34-aa15-552b56bf9e3a.pdf",
    model_impact="Two consequences. The Enterprise segment gets a re-based growth driver "
                 "rather than an extrapolation of its 16-18% history, because the "
                 "reorganisation is explicitly aimed at it. And the guidance record (F38) is "
                 "only one year old under this team, which is why the guidance is scored "
                 "rather than consumed.")

f_capex = R.add(
    Ring.COMPANY, "management & capital actions", FindingClass.D,
    "Capital expenditure is disclosed on two bases and by category. In-service capex by "
    "quarter runs EGP 1 292mn in Q1-2026 and 3 578.6mn in Q2-2026 against 20 396mn for the "
    "whole of FY2025 and 19 813mn for FY2024; the FY2024 split by category was access "
    "network 60%, transmission 17%, customer care 9%, international cable 8% and other 6%. "
    "Cash capex including licences was EGP 29.6bn in FY2025 (28% of sales) against EGP 35bn "
    "in FY2024, and EGP 18.6bn in H1-2026 alone. The most recent bar on the company's vendor-financing "
    "obligations chart reads EGP 21 352mn, and the chart's year labels did not survive "
    "extraction, so the year is not asserted here",
    "Telecom Egypt Fact Book Q2-2026 sheet 'KPIs Highlight' (XLSX route), FY2025 Results "
    "Presentation 'CapEx Analysis' and Corporate Presentation 2026; cross-checked against "
    "the audited cash-flow statement's payments for fixed assets of EGP 27 778 906 thousand "
    "and intangibles of 1 837 862 in FY2025",
    IR, "2026-08-13",
    url="https://ir.te.eg/IRMedia/Financial_Information/Fact_Book/2026/Fact_Book92ac7121-bc3f-4f4f-b5a3-b2ebb564abbb.xlsx", fiscal_period="Q2-2026",
    model_impact="DRIVER UNLOCK for capex, and the two bases have to be kept apart: "
                 "in-service capex is what enters the asset base and drives depreciation, "
                 "cash capex is what leaves the bank and drives free cash flow, and vendor "
                 "financing is the EGP 21.4bn bridge between them. A model using one number "
                 "for both misstates either the depreciation or the cash.")

# ==========================================================================================
# NEGATIVE SEARCHES — dated, and every one of them was actually run
# ==========================================================================================
f_neg_mobrev = R.add_negative(
    Ring.COMPANY, "regular disclosures",
    "Searched for a separately disclosed MOBILE REVENUE line across: the FY2022, FY2023, "
    "FY2024 and FY2025 audited consolidated statements (notes 5 and 41 in each), the Fact "
    "Book Q2-2026 'Revenue breakdown' sheet at its full 20-line depth, the FY2025 and "
    "H1-2026 results presentations, the Corporate Presentation 2026 and the FY2025, Q1-2026 "
    "and H1-2026 earnings releases. NO SUCH LINE EXISTS ANYWHERE. WE's mobile business is "
    "reported inside the 'Home & Consumer' retail unit and inside its 'Voice' and 'Data' "
    "sub-lines, which are not split between fixed and mobile. All that is disclosed is a "
    "subscriber count (15 214 thousand at Q2-2026) and a growth rate quoted in prose "
    "('Retail Mobile recorded 38% YoY growth' FY2025; 'Mobile revenue increased 28% YoY' "
    "H1-2026). Query strings run over the extracted text: 'mobile revenue', 'retail mobile', "
    "'WE mobile', 'Mobile' across the Fact Book sheets.",
    SWEEP_DATE)

f_neg_head = R.add_negative(
    Ring.COMPANY, "regular disclosures",
    "Searched for HEADCOUNT — 'number of employees', 'headcount', 'workforce', 'employees "
    "numbered', 'average number of' — across the FY2025 audited consolidated statements in "
    "full (all 60 pages of extracted text), the Corporate Presentation 2026, the FY2025 "
    "Results Presentation and the FY2025 earnings release. NOT DISCLOSED. The only "
    "'average number of' in the FY2025 statements is the weighted average share count. "
    "Employee cost IS disclosed and is the second-largest cost in the business at roughly "
    "EGP 16.07bn across operating costs, selling and G&A in FY2025, so the largest "
    "unbuildable line is a big one. This closes the wage driver as top-down.",
    SWEEP_DATE)

f_neg_ccy = R.add_negative(
    Ring.COMPANY, "regular disclosures",
    "Searched for a disclosed CURRENCY SPLIT OF REVENUE — what share of turnover is billed "
    "in or linked to US dollars. Query terms 'USD', 'dollar', 'currency', 'natural hedge', "
    "'hedge', 'foreign currency revenue' across the FY2025 audited statements, the Corporate "
    "Presentation 2026, the FY2025 Results Presentation and all three 2026 earnings "
    "releases. NOT DISCLOSED as a figure. The company describes its 'USD-linked "
    "international wholesale revenues' as a 'natural hedge' in prose but never quantifies "
    "the share. Note 40-3 gives the currency split of ASSETS AND LIABILITIES only. The "
    "closest sourced proxy is the two international business units' share of revenue: "
    "International Carriers plus International Cables and Networks was EGP 34 504 858 "
    "thousand of FY2025's 106 672 946, or 32.3% (FY2024: 34.3%) — and even that is an upper "
    "bound, because incoming international call revenue is settled in dollars while some "
    "domestic-facing lines inside those units are not.",
    SWEEP_DATE)

f_neg_wacc = R.add_negative(
    Ring.COMPANY, "strategic plans & guidance",
    "Searched the FY2025 audited statements, the Corporate Presentation 2026, the FY2025 "
    "Results Presentation and the three 2026 earnings releases for any company-stated "
    "DISCOUNT RATE, cost of capital, hurdle rate, target capital structure or impairment "
    "discount rate. NONE IS DISCLOSED. The statements record no goodwill impairment test "
    "requiring one — the only goodwill on the books, EGP 15 839 thousand, was disposed of "
    "during FY2025. There is therefore no company-sourced anchor for the cost of capital and "
    "it must be built from market inputs under wacc_builder.",
    SWEEP_DATE)

f_neg_q3 = R.add_negative(
    Ring.COMPANY, "official financial statements",
    "Checked ir.te.eg/en/FinancialInformation/FinancialStatements_Partial/2026 and "
    "/QuarterlyResults_Partial/2026 on the sweep date for a Q3-2026 filing. The 2026 year "
    "carries Q1 and Q2 ONLY — EAS consolidated and standalone statements, earnings release, "
    "transcript, results presentation and Fact Book for each. No Q3-2026 document of any "
    "kind exists yet, and no IFRS consolidated statement has been posted for either 2026 "
    "quarter (the IFRS set has consistently lagged the EAS set by about a year). The study "
    "year is therefore complete at two quarters and the declaration above says so.",
    SWEEP_DATE)

f_neg_fibre26 = R.add_negative(
    Ring.INDUSTRY, "pricing",
    "Searched for a SECOND NTRA tariff round, or any published tariff schedule beyond the "
    "6 May 2026 decision, across NTRA and MCIT reporting and the company's own H1-2026 "
    "release and transcript. None exists. The company's forward pricing language stops at "
    "'we expect this to support revenue in the coming quarters'. There is no dated basis for "
    "assuming a further regulated price rise inside the explicit window, so any second round "
    "is an upside scenario and is labelled as one.",
    SWEEP_DATE)

# ---- the dual-listing trap, flagged explicitly ---------------------------------------------
f_dual = R.add(
    Ring.COMPANY, "management & capital actions", FindingClass.S,
    "DUAL LISTING. The same issuer trades in two places under two tickers: ordinary shares "
    "on the Egyptian Exchange as ETEL.CA in Egyptian pounds, and Global Depositary Receipts "
    "on the London Stock Exchange as TEEG.LN, each GDR representing FIVE ordinary shares. "
    "The company states both on every release. The repo's own series "
    "engine/raw_ohlc/EG/ETEL.csv closes at EGP 118.49 on 23 August 2026 across 3 766 rows "
    "back to 2011, which is the EGX line in pounds — a GDR series would print roughly a "
    "fifth of that number of units at five times the price in dollars",
    "Telecom Egypt FY2025 audited consolidated financial statements, note 1-1 'Legal Entity' "
    "(OCR/TEXT route), and the ticker line carried on every earnings release; series "
    "verified against engine/raw_ohlc/EG/ETEL.csv",
    CO, "2026-02-26",
    url="https://ir.te.eg/IRMedia/Financial_Information/EAS_Consolidated_Statement/2026/EAS_Consolidated_Statement38a2837b-8610-4c24-aa82-ac57ea993e7e.pdf", is_fs_data=True, fiscal_period="FY2025",
    model_impact="Fixes the regressor. The beta is run through beta_regression.own_stock_beta "
                 "against the published index of the exchange the priced line is listed on — "
                 "EG/EGX30 under wacc_builder.market_index_path('EG') — and NOT against a "
                 "sterling or dollar GDR series or any constituent composite. The currency "
                 "and magnitude of the series were checked against the exchange before the "
                 "regressor was chosen, which is the whole point of the check.")

# ==========================================================================================
# DRIVER GATE TABLE — every driver, the mode earned, and what earned it
# ==========================================================================================
R.add_driver(
    "Fixed voice subscribers (Home & Consumer, and Enterprise, separately)",
    DriverMode.BOTTOM_UP,
    "The company publishes the two subscriber bases separately and quarterly back to "
    "Q1-2023 (Q2-2026: 13 136.1k and 1 203.3k), and they reconcile exactly to the total "
    "printed in the earnings release. Growth is projected against the disclosed household "
    "penetration ceiling of 51.6%, not extrapolated.",
    [f_kpi, f_mkt, f_rel])

R.add_driver(
    "Fixed broadband subscribers (Home & Consumer, and Enterprise, separately)",
    DriverMode.BOTTOM_UP,
    "Same source and same quarterly depth (Q2-2026: 11 124.7k and 346.2k). The national "
    "market size and Telecom Egypt's 82.1% share of it are disclosed, so the driver is "
    "bounded by market growth times share rather than by its own trend.",
    [f_kpi, f_mkt])

R.add_driver(
    "Mobile subscribers (WE)", DriverMode.BOTTOM_UP,
    "Disclosed quarterly (15 214k at Q2-2026, and note the base FELL from 15 287k in "
    "Q1-2026 and 15 475k at FY2025 — the first sequential declines in the series). The "
    "four-operator market shares are named, so share is projected against a named field.",
    [f_kpi, f_5g, f_rel])

R.add_driver(
    "Retail price per subscriber — fixed voice and fixed data (DERIVED, not disclosed)",
    DriverMode.BOTTOM_UP,
    "Built as disclosed segment revenue divided by disclosed subscribers, NOT as the "
    "company's published ARPU, because the two differ by 21% on fixed voice and 14% on data "
    "and the company does not define its base. The rate is therefore a DERIVED unit price "
    "and the study says so; the published ARPU is used only as a cross-check on direction. "
    "The dated NTRA step of +13.5% fixed broadband and +15% mobile is applied to the data "
    "leg alone.",
    [f_arpu, f_kpi, f_price, f_ntra])

R.add_driver(
    "Retail mobile revenue", DriverMode.TOP_DOWN,
    "NOT BUILDABLE. There is no disclosed mobile revenue line anywhere in four years of "
    "audited statements, the Fact Book at full depth, three presentations or three earnings "
    "releases — only a subscriber count and a prose growth rate. Mobile is grown on the "
    "disclosed subscriber base times the company's own stated mobile revenue growth rate, "
    "inside the Home & Consumer segment total, and the gap is flagged in the study.",
    [f_neg_mobrev, f_kpi])

R.add_driver(
    "Enterprise revenue (voice, data, other)", DriverMode.BOTTOM_UP,
    "Disclosed to three sub-lines quarterly in the Fact Book revenue breakdown and to a "
    "segment total in note 5 of the audited statements, with subscriber counts and the "
    "company's own ARPU for both Enterprise legs.",
    [f_kpi, f_seg])

R.add_driver(
    "Domestic wholesale revenue (infrastructure-transmission, and voice)",
    DriverMode.BOTTOM_UP,
    "Disclosed to two sub-lines quarterly, with the H1-2026 release giving the driver in "
    "words as well as pounds: infrastructure revenue up 21% to EGP 6.0bn. The underlying "
    "contracts are 3-10 year agreements with the named mobile network operators.",
    [f_kpi, f_seg, f_rel])

R.add_driver(
    "International carriers revenue (transit, incoming calls, outgoing calls)",
    DriverMode.BOTTOM_UP,
    "Disclosed to three sub-lines quarterly, and this is the one leg where a VOLUME is "
    "published alongside the value: international incoming call traffic is given as a growth "
    "rate (+26% FY2025, +18% H1-2026) against the disclosed revenue, so price per minute is "
    "solved rather than assumed. The leg is USD-settled and takes the FX path.",
    [f_kpi, f_seg, f_rel, f_fx])

R.add_driver(
    "International cables & networks revenue (cable projects, O&M, capacity sales, data "
    "centre, customer support)", DriverMode.BOTTOM_UP,
    "Disclosed to five sub-lines quarterly. Cable projects are LUMPY by construction — EGP "
    "3 143 504 thousand in Q4-2025 against zero in Q1-2026 and Q2-2026 — so they are "
    "modelled as a dated delivery schedule against the company's own 2027-28 landing list, "
    "never as a growth rate. The data-centre line stays at 100% ownership after the RDH "
    "transaction was abandoned.",
    [f_kpi, f_seg, f_gdemand, f_rdh])

R.add_driver(
    "Operating cost stack — 20 lines by nature; MARGIN IS THE OUTPUT",
    DriverMode.BOTTOM_UP,
    "Note 6 names all 20 lines and foots exactly for both FY2025 and FY2024, and notes 8 "
    "and 9 do the same below gross profit. Each line takes its own escalator against its own "
    "base: call cost against traffic, the NTRA frequency and licence charge against its own "
    "regulated base, fuel and electricity against energy reform, imported handsets and IRU "
    "against the FX path, wages against domestic CPI. No contribution or gross margin is "
    "ever an input on this name.",
    [f_inputs, f_costs_detail, f_seg, f_cpi])

R.add_driver(
    "Employee cost", DriverMode.TOP_DOWN,
    "The cost is disclosed across three captions but HEADCOUNT IS NOT DISCLOSED ANYWHERE, so "
    "it cannot be built as heads times cost per head. Held at its own three-year share of "
    "revenue escalated on the CAPMAS domestic index, and flagged as the largest unbuildable "
    "line in the stack at roughly EGP 16.07bn.",
    [f_neg_head, f_costs_detail])

R.add_driver(
    "In-service capex and cash capex, kept separate", DriverMode.BOTTOM_UP,
    "Both bases are disclosed quarterly, the FY2024 category split is published, the FY2026 "
    "guidance band is stated, and the audited cash-flow statement gives the cash figure "
    "independently. In-service capex feeds the asset base and depreciation; cash capex feeds "
    "free cash flow; the charted EGP 21.4bn of vendor financing is the bridge and is "
    "modelled explicitly.",
    [f_capex, f_guid, f_fy25])

R.add_driver(
    "Depreciation and amortisation", DriverMode.BOTTOM_UP,
    "Built off the disclosed gross asset base and the disclosed straight-line lives (5-50 "
    "years buildings and infrastructure, 3-15 technical equipment), with licence "
    "amortisation run off the disclosed licence carrying value of EGP 18 057 470 thousand "
    "over its stated term. Never held at a ratio to revenue.",
    [f_intang, f_fy25])

R.add_driver(
    "Vodafone Egypt associate income (44.95%)", DriverMode.BOTTOM_UP,
    "Vodafone Egypt's own revenue, profit before tax, net profit, equity and balance sheet "
    "are disclosed in note 20-1, and the Fact Book adds its subscribers (53 841k at "
    "Q2-2026), postpaid mix, blended and split ARPU, service revenue, operating profit and "
    "capex quarterly. The leg is built on Vodafone Egypt's own unit economics at the filed "
    "44.95%, with the March year-end stitch carried as an explicit lag.",
    [f_vfe, f_kpi, f_vfestake])

R.add_driver(
    "Vodafone Egypt dividends received (the cash leg of the stake)", DriverMode.BOTTOM_UP,
    "The accrued-dividend line inside the note 20-1 roll-forward (EGP 2 477 474 thousand in "
    "FY2025) and the 'dividends collected from investments' line in the audited cash-flow "
    "statement (EGP 2 231 549 thousand) give the cash conversion of the stake directly, "
    "which is what the equity bridge needs rather than the equity-accounted profit.",
    [f_vfe, f_fy25])

R.add_driver(
    "Interest expense — facility by facility", DriverMode.BOTTOM_UP,
    "Note 27 names six facilities with their currency, principal, maturity and repayment "
    "schedule. Each takes its own currency's policy path — the USD legs off the federal "
    "funds path, the EGP legs off the CBE path — rather than one blended rate on average "
    "debt. Note 27 states only 'variable interest rate' and no coupon, so the spread over "
    "each policy rate is SOLVED against the disclosed FY2025 finance cost of EGP 13 753 377 "
    "thousand and the solved spread is disclosed as a derived input.",
    [f_debt, f_cbe, f_fed, f_fy25])

R.add_driver(
    "FX gain/loss on the net foreign-currency monetary position", DriverMode.BOTTOM_UP,
    "Note 40-3 discloses the net position by currency and note 40-4 confirms the "
    "sensitivity is linear in it. The line is therefore computed as the disclosed net "
    "deficit times the modelled rate path, TWO-SIDED — Q1-2026 produced a EGP 7.76bn net "
    "finance cost and Q2-2026 a EGP 0.91bn net finance gain from the same balance sheet.",
    [f_fxexp, f_fx, f_q1, f_q2])

R.add_driver(
    "Foreign-currency share of revenue", DriverMode.TOP_DOWN,
    "The company describes its international wholesale revenue as a USD-linked natural "
    "hedge but never quantifies the share, and the currency note covers the balance sheet "
    "only. Proxied at the disclosed international business units' 32.3% of FY2025 revenue "
    "and treated as an upper bound, sensitised, and flagged as unsourced at the line level.",
    [f_neg_ccy, f_seg])

R.add_driver(
    "Income tax", DriverMode.BOTTOM_UP,
    "Current and deferred tax are disclosed separately in note 33 and quarterly in the Fact "
    "Book, and the effective rate on the FY2025 pre-tax profit of EGP 30 911 047 thousand is "
    "computable from the filings. Deferred tax is modelled on its disclosed movement, not "
    "netted into one effective rate.",
    [f_fy25, f_dtax])

R.add_driver(
    "Employee and board statutory profit share (the equity bridge leakage)",
    DriverMode.BOTTOM_UP,
    "Note 15 discloses it as a line: EGP 2 120 728 thousand of employees' share and 63 089 "
    "of board share deducted from FY2025 profit before EPS is struck, 9.7% of attributable "
    "profit. Carried explicitly in the bridge rather than absorbed into the payout ratio.",
    [f_cap, f_fy25])

R.add_driver(
    "Ordinary dividend", DriverMode.BOTTOM_UP,
    "Set as a LEVEL, not a ratio: EGP 1.50 per share, EGP 2 560 607 thousand in total, "
    "unchanged in nominal pounds across FY2023, FY2024 and FY2025 while EPS went from 4.79 "
    "to 11.93. The company's own three-year behaviour, not an assumed payout percentage.",
    [f_div, f_fy25])

R.add_driver(
    "Net debt and the enterprise-to-equity bridge", DriverMode.BOTTOM_UP,
    "Uses the company's own definition, which reproduces exactly from the audited balance "
    "sheet: total debt less cash and cash equivalents less treasury bills at amortised cost. "
    "Vendor-financing obligations of EGP 21.4bn are reported on their own separate ladder "
    "alongside it, as the company reports them, rather than blended in.",
    [f_netdebt, f_debt, f_capex])

R.add_driver(
    "Equity, book value and the dividend history", DriverMode.BOTTOM_UP,
    "Taken from the audited BALANCE SHEET and cash-flow statement, NOT from the Consolidated "
    "Statement of Changes in Equity, whose FY2025 rows do not foot and overstate closing "
    "equity by EGP 2.57bn. Both extraction routes were run on that page and both return the "
    "same non-footing figures, so the defect is in the filing.",
    [f_socie, f_fy25, f_dtax])

R.add_driver(
    "Beta and the regressor", DriverMode.BOTTOM_UP,
    "The priced line is the EGX ordinary share in Egyptian pounds, verified against the "
    "repo's own series at EGP 118.49 on 23 August 2026, so the regressor is EG/EGX30 through "
    "beta_regression.own_stock_beta. The London GDR at five ordinary shares each is a second "
    "legitimate series for the same issuer and is explicitly NOT used.",
    [f_dual, f_own])

R.add_driver(
    "Cost of capital — risk-free, ERP and the terminal ladder", DriverMode.TOP_DOWN,
    "The company discloses no discount rate, hurdle rate or target structure of any kind, "
    "and carries no goodwill requiring an impairment test that would reveal one. The build "
    "is therefore entirely external: the explicit-window risk-free from the CBE's held "
    "19.50% main operation rate, the terminal norm-built off the CBE's OWN published 7% "
    "target plus the house EM real-rate convention, with the sovereign default spread netted "
    "out so country risk is not charged twice.",
    [f_neg_wacc, f_cbe])

R.add_driver(
    "FY2026 revenue growth", DriverMode.BOTTOM_UP,
    "Built from the sourced unit economics — subscribers by segment times a derived unit "
    "price, plus the dated NTRA step — and then compared with the Board's published "
    "high-single-digit guidance and management's May 2026 statement that it expects to "
    "exceed it. H1-2026 actual growth of 17% is the live evidence. Guidance is scored, "
    "never consumed as the driver.",
    [f_guid, f_beat, f_rel, f_price])

# ==========================================================================================
# OUTPUT
# ==========================================================================================
errors, warnings = R.validate()
R.to_json(os.path.join(HERE, 'sweep_register.json'))

print(R.qc_line())
print()
print(f"findings: {len(R.findings)} | drivers: {len(R.drivers)}")
counts = R.counts()
print(f"by class: " + " · ".join(f"{k} {v}" for k, v in counts.items()))
n_ir = sum(1 for f in R.findings if f.source_type is SourceType.COMPANY_IR)
n_co = sum(1 for f in R.findings if f.source_type is SourceType.COMPANY_OFFICIAL)
print(f"COMPANY_OFFICIAL findings: {n_co} | COMPANY_IR findings: {n_ir}")
fs_years = sorted({f.fiscal_period for f in R.findings
                   if f.is_fs_data and f.fiscal_period.startswith("FY")})
quarters = sorted({f.fiscal_period for f in R.findings
                   if f.fiscal_period.startswith("Q")})
print(f"fiscal years carrying FS data: {fs_years}")
print(f"study-year quarters swept: {quarters}")
print(f"primary access attempts: {len(R.primary_access)} "
      f"({sum(1 for p in R.primary_access if p.reachable)} reachable, "
      f"{sum(1 for p in R.primary_access if not p.reachable)} blocked)")

if errors:
    print(f"\nVALIDATOR ERRORS ({len(errors)}) — reported verbatim, not suppressed:")
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
print(f"\nfreshness (delivery {SWEEP_DATE}): {fr or 'OK — sweep and delivery same day'}")
