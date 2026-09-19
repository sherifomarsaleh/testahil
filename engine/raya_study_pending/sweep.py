"""RAYA (Raya Holding Company for Financial Investments S.A.E., EGX: RAYA.CA) —
four-ring Step 2A Information Sweep register. FIRST-BUILD study; held under a
`_pending` suffix because it carries no valuation yet and an empty or half-built
`engine/*_study` directory turns roughly ten repository gates red.

Runs BEFORE any forecast driver is set. Every mandatory category of every ring is
closed by a dated finding or a dated negative search.

THIS ISSUER IS A HOLDING COMPANY AND A SINGLE BLENDED MARGIN DESCRIBES NOTHING
=============================================================================
Raya Holding consolidates FORTY subsidiaries running eleven operating businesses
across seven sectors on completely different economics. The FY2025 audited segment
note (note 29) prints gross margins by sector that range from 7.9 per cent (Raya
Electric, appliance OEM/ODM) to 59.5 per cent (Raya Smart Buildings, commercial
leasing) — an eightfold spread inside one issuer. The group's 21.4 per cent FY2025
gross margin is the weighted output of that spread and is not a property of any
business Raya owns. Every driver row below is therefore set at SEGMENT level, and
where the disclosure stops short of volume x price the gap is FLAGGED rather than
filled with an allocation.

WHAT THE SEGMENT NOTE ACTUALLY DISCLOSES, WHICH IS THE QUESTION THAT DECIDED THE
DRIVER MODES
===============================================================================
Note 29 "SEGEMENT REPORTING" (the filing's own spelling) gives SIX lines per
segment, for fourteen named sectors plus an eliminations column and a consolidated
column, for both the year and the comparative:

    Revenues | Cost | Depreciation for the Year | profit for the Year |
    Total Assets | Total Liabilities

That is far more than revenue alone, and it is what makes a segment-level
bottom-up build possible: cost is disclosed per segment, so gross margin is an
OUTPUT of the build rather than an input. What note 29 does NOT carry is
non-controlling interest per segment, headcount per segment, capital expenditure
per segment, units, prices, utilisation, or any geographic split within a segment.
Those absences are closed by dated negative searches (N01-N05) and they are what
forces four driver rows top-down rather than bottom-up.

The operating quantities the statements never carry — seats and utilisation,
branches, production capacity in units, gross transaction value, retail outlets,
gross leasable area, ATM market share — ARE disclosed, but only in the investor-
relations channel (earnings releases, investor presentations, fact sheets). That is
why the COMPANY_IR source type carries four findings here and is not decoration.

OWNERSHIP AND WHERE THE VALUE LEAKS
===================================
Note 1 lists all forty consolidated subsidiaries with an ownership percentage, and
the list is IDENTICAL at 31-Dec-2025 and 30-Jun-2026. Twenty-nine are 100 per cent
owned. Eleven are not, and they are where the minority sits:

    Raya Contact Centre Company              60.13%   (the BPO leg)
    Aman entities (six companies)            76%      (the whole fintech leg)
    Aman Taqa                                39%      (consolidated below 50%)
    Gulf customer experience (Bahrain)       85%
    Raya Restaurants Company                 95.423%
    Ostool for Land Transport Company        90%      (SOLD 1-Jul-2026 — see F34)

The consequence is arithmetic and it is large: non-controlling interest is 30.2 per
cent of total equity at 30-Jun-2026 but took only 16.2 per cent of H1-2026 profit,
and its share of profit has ranged from 11.1 per cent (FY2024) to 21.7 per cent
(FY2023) across the five disclosed periods. ANY BLENDED NCI RATIO MIS-STATES MOST
YEARS. Driver D20 computes it subsidiary by subsidiary at each entity's own named
percentage and flags the mapping gap the segment note leaves.

PRIMARY SOURCE: REACHED IN FULL, AND EVERY FIGURE BELOW COMES FROM IT
=====================================================================
rayacorp.com answered HTTP 200 on the first attempt and every investor-relations
sub-page and PDF downloaded cleanly (one transient CONNECT 502 on /earning-releases/
that succeeded on retry, logged as its own attempt). Four audited consolidated
annual filings (FY2022-FY2025) and both reviewed interim filings of the study year
(Q1-2026, H1-2026) were taken from the company's own site. NO AGGREGATOR SUPPLIED
ANY FIGURE RAYA REPORTS ABOUT ITSELF.

EVERY EGYPTIAN PRIMARY STATEMENT HERE IS IMAGE-ONLY AND WAS READ OFF THE PIXELS
==============================================================================
All six financial-statement PDFs carry ZERO text characters (`pdftotext` returns 0
on 49, 51, 54, 55, 46 and 44 pages respectively). Every statement was rendered and
read visually, then RE-ADDED against the filing's own printed subtotals. The
arithmetic settled four disagreements between routes and each one is recorded on the
finding it belongs to:

  1. FY2024 accounts and notes receivable, read at 110 dpi as EGP 14,600,882,485,
     read at 300 dpi as EGP 14,600,682,485. The current-asset column foots to the
     printed EGP 33,927,432,700 only on the second. An 8 read for a 6. [F21]
  2. H1-2026 FVOCI revaluation reserve, read at 100 dpi as EGP 27,691,078, at 300
     dpi as EGP 27,691,178. Equity before NCI foots to the printed EGP 6,611,896,072
     only on the second. A 1 read for a 0. [F25]
  3. FY2022 intangible assets, read off the ARABIC original (the only FY2022
     consolidated filing published) in Eastern Arabic-Indic numerals as EGP
     19,561,819, read off the English comparative column in the FY2023 filing as
     EGP 19,661,819. Non-current assets foot to the printed EGP 4,005,236,755 only
     on the second. A 5 read for a 6. [F23]
  4. FY2025 segment note, "Information technology" profit for FY2024, printed as
     "1205,,097" with a doubled comma. The column foots to the attributable profit
     of EGP 1,688,543,816 only on 1,205,097. [F26]

Three genuine footing breaks PRINTED IN THE FILINGS THEMSELVES were also found and
are recorded rather than smoothed; they are small in magnitude and large in what
they say about relying on a printed subtotal. See F20, F22 and F26.

BETA WAS DELIBERATELY NOT RESOLVED, PER INSTRUCTION
===================================================
Driver row D25 records the exchange, the listing and the series that exist and
stops there. RAYA is listed on ONE exchange, the EGX, in EGP, ticker RAYA.CA, since
2005; no depositary receipt or second line was found (N06). There is no dual-listing
trap here of the Orascom Construction kind, and the register says so explicitly so a
later build does not go looking for one.
"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from research_sweep import (SweepRegister, AssetClass, Ring, FindingClass,
                            SourceType, DriverMode, RINGS, MANDATORY)

SWEEP_DATE = "2026-09-09"
R = SweepRegister("RAYA", AssetClass.STOCK, SWEEP_DATE)
CO, IR, REG, PMD, PRESS, AGG = (SourceType.COMPANY_OFFICIAL, SourceType.COMPANY_IR,
                                SourceType.REGULATOR_OFFICIAL, SourceType.PRIMARY_MARKET_DATA,
                                SourceType.REPUTABLE_PRESS, SourceType.AGGREGATOR)

# ---------------------------------------------------------- PRIMARY-SOURCE ACCESS
# The company's own website / IR channel was tried FIRST for every Company-ring
# figure, before any aggregator. Every attempt is logged with its REAL result text,
# whether it succeeded or was blocked.
R.record_primary_access("https://rayacorp.com/", True, "2026-09-09",
    "HTTP 200, 100,533 bytes. Company site reachable on the first attempt; full "
    "investor-relations menu present (financial statements, earning releases, "
    "investor presentations, factsheets, annual report, disclosures, stock overview, "
    "dividends overview, corporate governance).")
R.record_primary_access("https://rayacorp.com/financial-statements/", True, "2026-09-09",
    "HTTP 200, 112,779 bytes. 58 statement PDFs listed, FY2019 to H1-2026, "
    "consolidated and standalone. Six consolidated filings taken: FY2022 (Arabic "
    "original), FY2023, FY2024, FY2025, Q1-2026, H1-2026.")
R.record_primary_access("https://rayacorp.com/earning-releases/", False, "2026-09-09",
    "FIRST ATTEMPT FAILED: `curl: (56) CONNECT tunnel failed, response 502`, "
    "http=000, 0 bytes. Logged as its own attempt rather than folded into the retry.")
R.record_primary_access("https://rayacorp.com/earning-releases/", True, "2026-09-09",
    "RETRY SUCCEEDED: HTTP 200, 89,300 bytes. 30 earnings releases listed, 1Q2019 to "
    "1H-2026. Six taken: FY2022, FY2023, FY2024, FY2025, 1Q-2026, 1H-2026.")
R.record_primary_access("https://rayacorp.com/investor-presentations/", True, "2026-09-09",
    "HTTP 200, 85,999 bytes. 25 presentations listed. Two taken: FY2025 (posted "
    "07/2026) and 1Q-2026 (posted 08/2026).")
R.record_primary_access("https://rayacorp.com/factsheets/", True, "2026-09-09",
    "HTTP 200, 74,078 bytes. Ten fact sheets, 1Q2024 to 1H-2026. Three taken.")
R.record_primary_access("https://rayacorp.com/annual-report/", True, "2026-09-09",
    "HTTP 200, 70,942 bytes. Five annual reports (2017, 2018, 2019, AR23, AR24). "
    "AR24 taken (204 pages, text layer present). NO FY2025 ANNUAL REPORT IS PUBLISHED "
    "AS AT THE SWEEP DATE — the FY2025 disclosure set is the audited statements, the "
    "earnings release, the investor presentation and the fact sheet.")
R.record_primary_access("https://rayacorp.com/disclosures/", True, "2026-09-09",
    "HTTP 200, 65,257 bytes, but the page carries NO PDF links and no disclosure "
    "table — the body is rendered client-side and returns empty to a plain fetch. "
    "Same for /stock-overview/ and /dividends-overview/. The EGX filing text behind "
    "them was therefore NOT obtainable from the company site; the substance was taken "
    "from the statement and release PDFs instead, which are static files and did "
    "download.")
R.record_primary_access("https://raya-holding.com/", False, "2026-09-09",
    "`curl: (60) SSL certificate problem: self-signed certificate`. Checked only to "
    "confirm it is not a second company domain; it is not, and nothing was taken "
    "from it.")
R.record_primary_access("https://www.egx.com.eg/en/homepage.aspx", False, "2026-09-09",
    "`curl: (52) Empty reply from server`, http=000. Also on https://egx.com.eg/ . "
    "The exchange's own disclosure portal was NOT reachable from this environment, so "
    "no EGX filing text was read directly. [R-SIGCM-03] fallback applied: the "
    "company's OWN other documents were used instead — the reviewed H1-2026 interim's "
    "note 1 carries the Ostool transaction in full (F34), which is the disclosure the "
    "EGX portal would have carried. No aggregator, broker or press substituted for any "
    "company figure.")
R.record_primary_access("https://www.cbe.org.eg/en/monetary-policy/mpc-decisions", False,
    "2026-09-09",
    "HTTP 200 but a 269-byte WAF page, not content: `Request Rejected — The requested "
    "URL was rejected. Please consult with your administrator. Your support ID is "
    "c785f289-cc6e-4cd7-a95c-b06bdc5804ee`. Same rejection on "
    "/en/monetary-policy/inflation-targets and /en/monetary-policy/inflation. The CBE "
    "root and its 404 page DO serve, so the block is path-specific. The Monetary "
    "Policy Report Q1-2026 PDF was refused the same way (269 bytes of HTML in place of "
    "the PDF). THE FAKE ARTEFACT HAS BEEN REMOVED: "
    "engine/raya_study_pending/filings/CBE_MPR_Q1_2026.pdf held that rejection page, not "
    "the report — 269 bytes of HTML under a .pdf name, support ID "
    "f63899a7-69d2-4c00-a113-f144bad68c25 — and was deleted on 09-09-2026 rather than "
    "left to be read as a filing. The failed access is this record; the file was not "
    "evidence of anything. scripts/check_fetch_authenticity.py now fails on any such "
    "file in the tracked tree. "
    "Egypt's policy rate is therefore carried from Raya's OWN audited note 35 "
    "(F05) and from named press reporting of the 20-Aug-2026 MPC statement (F06), not "
    "from the CBE site.")
R.record_primary_access("https://www.tra.gov.eg/en/", True, "2026-09-09",
    "curl HTTP 200. The NTRA article page for the 21-Jan-2026 handset customs decision "
    "answered curl but timed out in the fetch tool at 60,000 ms, so the decision is "
    "carried at F08 from the regulator's own published announcement as surfaced in "
    "search plus named press, with the route stated.")

# ---------------------------------------------------------------- RING 1  GLOBAL
f_fed = R.add(Ring.GLOBAL, "rate cycle & USD/FX regime", FindingClass.S,
    "US federal funds target range 3.50-3.75%, held 9-3 at the 28-29 July 2026 FOMC; "
    "the 15-16 September 2026 meeting (with a Summary of Economic Projections) had not "
    "sat as at the sweep date",
    "US Federal Reserve, FOMC minutes of 28-29 July 2026 and the published target-range "
    "history", REG, "2026-07-29",
    url="https://www.federalreserve.gov/monetarypolicy/fomcminutes20260729.htm",
    detail="ROUTE: read from the Federal Reserve's own minutes page as surfaced in "
           "search, not fetched page-for-page. The level is corroborated by the FRED "
           "DFEDTARL/DFEDTARU series named in the same results.",
    model_impact="Anchors the FOREIGN leg of the EGP path. The house macro ladder "
                 "derives USD/EGP from Egypt's inflation path against long-run US "
                 "inflation by relative purchasing-power parity; the US policy path is "
                 "the shape input to that, never a free parameter. It also sets the "
                 "discount backdrop for the 27.0% of H1-2026 revenue that Raya earns in "
                 "foreign currency (F28).")

f_mem = R.add(Ring.GLOBAL, "commodity complex (input/output)", FindingClass.B,
    "THE MEMORY-CHIP CRISIS IS RAYA'S INPUT-COST SHOCK. NAND and DRAM contract costs "
    "up over 300% year-on-year on the steepest measure; Gartner's own estimate is a "
    "130% surge in memory prices by end-2026. Smartphone average selling price is "
    "forecast to reach USD 581 in 2026, up 27.6% in a single year",
    "IDC, 'Smartphone Shipments Set for Record 16.7% Drop in 2026, as the Memory Crisis "
    "Hits Full Force'; Gartner press release 26-Feb-2026, 'Surging Memory Costs Will "
    "Reduce Global PC and Smartphone Shipments in 2026'", PRESS, "2026-02-26",
    detail="Raya has no commodity note and hedges nothing disclosed (N05). Its input "
           "exposure is not a metal or a fuel — it is the bill of materials inside the "
           "handsets, PCs, servers and appliances it distributes, integrates and "
           "assembles. Raya Trade (43.7% of H1-2026 revenue) and Raya Information "
           "Technology (20.8%) together are 64.5% of the group and both buy that bill "
           "of materials in dollars.",
    model_impact="BASE CHANGER, and the mechanism behind the whole Q2-2026 result. "
                 "Group gross margin fell to 16.77% in Q2-2026 from 22.26% in Q2-2025 "
                 "and 21.85% in Q1-2026 (F25). The cost-of-revenues driver (D16) is "
                 "built by NATURE off note 25 with 'devices and goods distribution "
                 "cost' — EGP 15,729,838,558 of the group's EGP 27,317,409,179 H1-2026 "
                 "cost base — escalated on this input path rather than on Egyptian CPI. "
                 "Modelled as an explicit dated event and dual-framed with and without "
                 "a 2027 normalisation.")

f_hand = R.add(Ring.GLOBAL, "global sector demand", FindingClass.S,
    "Worldwide smartphone shipments forecast to fall 16.7% in 2026 to just over 1.0bn "
    "units — the steepest annual contraction on record — while market VALUE rises 6.3% "
    "to USD 613bn on price. The sub-USD-100 segment, about 171m devices, becomes "
    "effectively uneconomical. Gartner's separate estimate is -8.4% units",
    "IDC worldwide smartphone tracker commentary, 2026; Gartner, 26-Feb-2026", PRESS,
    "2026-02-26",
    detail="Two houses, two numbers (-16.7% IDC, -13% on an earlier IDC vintage, -8.4% "
           "Gartner). The RANGE is carried into the sensitivity grid; no single number "
           "is treated as the forecast.",
    model_impact="Sets the VOLUME leg of the Raya Trade build (D2) DOWN and the PRICE "
                 "leg UP, which is why the two must be projected separately rather than "
                 "as one revenue growth rate. Raya Trade's mobile distribution and "
                 "retail division was 52.9% of its FY2025 revenue; the entry-level "
                 "squeeze bites hardest exactly there.")

f_trade = R.add(Ring.GLOBAL, "trade / sanctions / supply chains", FindingClass.S,
    "Raya's OWN reviewed H1-2026 interim, note 35, names the escalation in geopolitical "
    "tensions between the United States and Iran as a significant event, warning of "
    "disruptions to global supply chains, higher shipping, insurance and transportation "
    "costs, and pressure on the EGP/USD rate — and states management cannot reliably "
    "determine the financial impact. Suez Canal revenue meanwhile rebounded to USD "
    "4.67bn in FY2025/26 (+23% y/y) with 14,000-15,000 transits against about 26,000 "
    "in 2023",
    "Raya Holding reviewed consolidated interim financial statements for the six months "
    "ended 30 June 2026, note 35 'Significant Events'; Suez Canal Authority figures as "
    "reported 05-Aug-2026", CO, "2026-08-12",
    url="https://rayacorp.com/wp-content/uploads/2026/09/Raya-Holding-Cons.-30-Jun-2026-English.pdf",
    detail="Read off the rendered pixels of printed page 44 of the interim; the filing "
           "carries no text layer. The Suez figures are context and are NOT a Raya "
           "figure — Raya's own logistics leg (Ostool) was sold on 1-Jul-2026 (F34).",
    model_impact="Sets the downside branch of the freight-and-insurance component "
                 "inside cost of revenues (D16) and is the stated reason the EGP path "
                 "carries an alternative scenario. The company itself declines to "
                 "quantify it, so it is carried as a named sensitivity, never as a "
                 "point estimate in the base.")

# --------------------------------------------------------------- RING 2  COUNTRY
f_cbe1 = R.add(Ring.COUNTRY, "sovereign macro (inflation, policy rate, FX/deval risk)",
    FindingClass.D,
    "The Central Bank of Egypt's Monetary Policy Committee cut by 100bp on Thursday 12 "
    "February 2026, taking the overnight deposit rate to 19.00%, the overnight lending "
    "rate to 20.00% and the main operation rate to 19.50%; the discount rate was also "
    "cut 100bp to 19.50%",
    "Raya Holding reviewed consolidated interim financial statements, six months ended "
    "30 June 2026, note 35 'Significant Events'", CO, "2026-08-12",
    url="https://rayacorp.com/wp-content/uploads/2026/09/Raya-Holding-Cons.-30-Jun-2026-English.pdf",
    detail="CARRIED FROM THE COMPANY'S OWN AUDITED-SET DOCUMENT BECAUSE THE CENTRAL "
           "BANK'S SITE REFUSED THE REQUEST. cbe.org.eg returned a 269-byte WAF page "
           "('Request Rejected ... Your support ID is ...') on every monetary-policy "
           "path and on the Q1-2026 Monetary Policy Report PDF. This is [R-SIGCM-03] "
           "working: a named company document, not an aggregator, stands in for the "
           "unreachable primary.",
    model_impact="DRIVER UNLOCK for the cost-of-debt path (D22). Raya's H1-2026 finance "
                 "cost of EGP 1,060,289,247 sits against a gross interest-bearing debt "
                 "stack of about EGP 24.0bn (F30); the corridor level is what the "
                 "implied borrowing rate is tested against rather than an assumed "
                 "spread.")

f_cbe2 = R.add(Ring.COUNTRY, "sovereign macro (inflation, policy rate, FX/deval risk)",
    FindingClass.S,
    "The MPC HELD on 20 August 2026 — a fourth consecutive hold — leaving 19.00% / "
    "20.00% / 19.50%. Annual urban headline inflation was 14.9% in July 2026 against "
    "14.3% in June (core 14.7% against 14.3%; monthly headline and core both 0.0%); "
    "nationwide headline 13.0% against 12.2%. The CBE's own target is 7% (+/-2pp) for "
    "Q4-2026 and it states inflation will remain ABOVE the band in Q4-2026, returning "
    "to it in the second half of 2027",
    "Central Bank of Egypt MPC statement of 20 August 2026 as reported by Bloomberg "
    "('Egypt Holds Rates a Fourth Time With No End to Iran War in Sight') and CAPMAS "
    "July CPI via Daily News Egypt; target and path as already registered in "
    "engine/Cost_of_Capital_Reference.md", PRESS, "2026-08-20",
    detail="Inflation ACCELERATED in July, breaking the cooling trend — the first "
           "increase since March. The CBE Q1-2026 Monetary Policy Report baseline is "
           "16.0% average annual headline in 2026 and 12.0% in 2027, with an "
           "alternative scenario (conflict persisting to end-2026) of 17.0% and 13.0%.",
    model_impact="Sets the explicit-window risk-free rate and the SG&A escalator (D18). "
                 "The terminal risk-free rate (D24) is norm-built from the CBE's OWN "
                 "published 7% target plus the house emerging-market real-rate "
                 "convention, never averaged from history.")

f_fx = R.add(Ring.COUNTRY, "sovereign macro (inflation, policy rate, FX/deval risk)",
    FindingClass.S,
    "USD/EGP about 50.9 in early September 2026, against 50.25 registered on 6 August "
    "2026 and a 52-week range of 46.64-54.86. Raya's own 1Q-2026 investor presentation "
    "states a 31-March-2026 market capitalisation of EGP 21,748mn and USD 398.4mn, an "
    "implied 54.59 — so the pound APPRECIATED about 7% against the dollar between "
    "end-March and the sweep date",
    "Market quote, September 2026; USD/EGP 50.25 of 6 August 2026 as registered in "
    "engine/Cost_of_Capital_Reference.md; implied rate derived from Raya Holding 1Q-2026 "
    "Investor Presentation, stock overview page", PMD, "2026-09-08",
    detail="The implied 54.59 is DERIVED from two figures the company printed side by "
           "side and is used only as a cross-check on the direction, never as a quote.",
    model_impact="Drives the translation leg (D27). Foreign-currency revenue was EGP "
                 "9,129,541,932 in H1-2026, 27.0% of the group; Raya Foods earns 95% of "
                 "its revenue in foreign currency and RCX 68.9% offshore in USD. A "
                 "STRENGTHENING pound is a headwind to those legs and a tailwind to the "
                 "dollar-denominated cost of imported devices — the two must be modelled "
                 "on opposite signs, not netted into one FX assumption.")

f_ntra = R.add(Ring.COUNTRY, "regulatory environment (regulator, caps, tariffs, tax/subsidy)",
    FindingClass.B,
    "Egypt ENDED the customs exemption on mobile phones carried in by passengers at "
    "12:00 noon on Wednesday 21 January 2026. Any device entering with a traveller now "
    "bears a one-time 38.5% customs-and-tax charge (exemption retained for Egyptians "
    "living abroad and for tourists for 90 days). The regulator's stated reason is that "
    "fifteen international handset brands now manufacture in Egypt with about 20m units "
    "a year of capacity — more than local demand — under the 'Egypt Makes Electronics' "
    "programme, creating about 10,000 jobs",
    "National Telecom Regulatory Authority (NTRA/TRA), announcement 'End of exceptional "
    "exemption on imported mobile phones carried by passenger...', effective 21 January "
    "2026; reported by AGBI, The National, Daily News Egypt and EnterpriseAM",
    REG, "2026-01-21",
    url="https://www.tra.gov.eg/en/end-of-exceptional-exemption-on-imported-mobile-phones-carried-by-passenger-following-success-of-local-manufacturing-at-competitive-prices-effective-1200-noon-wednesday-january-21-2026/",
    detail="ROUTE: tra.gov.eg answered curl HTTP 200 but the article page timed out in "
           "the fetch tool at 60,000 ms; the decision is carried from the regulator's "
           "own published announcement as surfaced in search and corroborated by four "
           "named press accounts. THIS IS THE 'WHITELISTING' RAYA'S OWN 1H-2026 RELEASE "
           "REFERS TO when it says the mobile distribution business 'continued to show "
           "improvement following its whitelisting'.",
    model_impact="BASE CHANGER for Raya Trade, and it cuts BOTH ways. It removes the "
                 "grey-import channel that competed with Raya's formal distribution "
                 "(volume and share UP) and simultaneously moves the market toward "
                 "locally assembled devices at lower unit prices, with fifteen brands' "
                 "worth of new domestic supply (price and mix DOWN). Both legs are set "
                 "explicitly in D2 and dual-framed; neither is smoothed into a growth "
                 "rate.")

f_fra = R.add(Ring.COUNTRY, "regulatory environment (regulator, caps, tariffs, tax/subsidy)",
    FindingClass.S,
    "Egypt's Financial Regulatory Authority issued its FIRST comprehensive rulebook for "
    "consumer-finance companies on 5 September 2026 — four days before this sweep — "
    "consolidating licensing, lending, disclosure, capital, risk-management and "
    "cybersecurity requirements. It sits on top of Decision 137/2025, which imposed "
    "Basel-style prudential standards: a minimum 12% capital-adequacy ratio against "
    "risk-weighted assets and qualifying borrowings capped at nine times the capital "
    "base. Cash lending remains capped at EGP 50,000 per loan and 20% of the portfolio "
    "under Decrees 81/2023 and 138/2025",
    "Egyptian Financial Regulatory Authority, comprehensive consumer-finance guide, 5 "
    "September 2026, reported by Daily News Egypt, Amwal Al Ghad, WAYA and The Middle "
    "East Observer; Decision 137/2025 as summarised in Chambers Fintech 2026 Egypt",
    REG, "2026-09-05",
    detail="fra.gov.eg answered HTTP 200 at the sweep date; the rulebook itself is four "
           "days old and its text was not obtainable, so the substance is carried from "
           "named reporting of the regulator's own release and the prior decisions are "
           "carried from a practitioner guide. RE-SOURCE THE RULEBOOK TEXT BEFORE THE "
           "BUILD — it binds 33.6% of the group's H1-2026 gross profit.",
    model_impact="Binds the Aman leg (D5, D6). The 12% CAR floor and the 9x borrowing "
                 "ceiling set the maximum portfolio Aman can carry on a given equity "
                 "base, which caps its growth independently of demand and forces the "
                 "model to SOLVE for the next capital injection rather than assume the "
                 "portfolio compounds. Raya owns 76% of Aman, so 24% of any injection "
                 "is the minority's.")

f_tax = R.add(Ring.COUNTRY, "regulatory environment (regulator, caps, tariffs, tax/subsidy)",
    FindingClass.C,
    "Egyptian corporate income tax 22.5% on net taxable profit. Capital gains on "
    "EGX-listed shares 10%; on unlisted or foreign shares the 22.5% corporate rate. "
    "Dividend withholding 5% for listed companies, 10% for unlisted",
    "PwC Worldwide Tax Summaries, Egypt corporate taxes; corroborated by Andersen Egypt "
    "and Maher Consulting 2026 summaries", REG, "2026-01-01",
    detail="The statutory rate is context, NOT the modelling rate. Raya's own effective "
           "rate was 28.9% (FY2025), 30.1% (FY2024), 39.3% (FY2023), 32.9% (FY2022), "
           "35.9% (Q1-2026) and 29.4% (H1-2026) — the statutory 22.5% would mis-state "
           "every single disclosed period by between 6 and 17 percentage points. See "
           "D21.")

f_imf = R.add(Ring.COUNTRY, "fiscal / political events with sector read-through",
    FindingClass.S,
    "The IMF Executive Board completed Egypt's combined fifth and sixth EFF reviews and "
    "the first RSF review on 26 February 2026, releasing about USD 2.3bn (USD 2.0bn EFF "
    "plus USD 273m RSF) and taking cumulative purchases to about USD 5,207m; the 46-month "
    "EFF was extended to 15 December 2026. Real GDP grew 4.4% in FY2024/25, the current-"
    "account deficit narrowed to 4.2% of GDP, and the Fund states progress on structural "
    "reform — 'particularly progress on the divestment agenda' — has been SLOWER THAN "
    "ENVISAGED",
    "International Monetary Fund, Press Release 26/064 and the accompanying staff report "
    "(Country Report 2026/069), 26 February 2026", REG, "2026-02-26",
    url="https://www.imf.org/en/news/articles/2026/02/26/pr-26064-egypt-imf-completes-5th-and-6th-revs-under-ext-arrange-under-eff-and-1st-rev-under-rsa",
    detail="The divestment sentence matters directly to this issuer: the state-asset "
           "sale programme is the supply of the transactions a listed Egyptian holding "
           "company transacts against, and Raya has just been on the SELL side of one "
           "(F34).",
    model_impact="Sets the macro backdrop for the country risk premium and the sovereign "
                 "spread inputs to the cost of equity, and is the stated reason the "
                 "EGP path carries a conflict-persisting alternative. It changes no "
                 "revenue driver directly and is not allowed to.")

# -------------------------------------------------------------- RING 3  INDUSTRY
f_cfin = R.add(Ring.INDUSTRY, "demand drivers & capacity/supply balance", FindingClass.D,
    "Egyptian consumer financing reached EGP 71.839bn in H1-2026, up 88.5% from EGP "
    "38.110bn in H1-2025, with beneficiaries up 75.7% year-on-year",
    "Egyptian Financial Regulatory Authority H1-2026 non-banking financial services "
    "data, reported by Arab Finance", REG, "2026-08-01",
    detail="Aman's own gross transaction value grew 54% to EGP 67.6bn in H1-2026 from "
           "EGP 43.9bn (F31) — SLOWER than the 88.5% market. That is a share loss and "
           "it is the reason the Aman driver is built off Aman's own disclosed GTV and "
           "portfolio rather than off a market-growth rate applied to a share.",
    model_impact="DRIVER UNLOCK for the Aman revenue build (D5): gives the market "
                 "denominator against which Aman's disclosed GTV and portfolio are "
                 "tested, so the growth rate is bounded by an external series instead "
                 "of extrapolated.")

f_dc = R.add(Ring.INDUSTRY, "demand drivers & capacity/supply balance", FindingClass.D,
    "Egypt's data-centre market is forecast to compound at 18.97% a year from 2025 to "
    "2031. Thirteen colocation facilities operate today, nine of them in Cairo, with "
    "nine more in development. In December 2024 Egypt's Ministry of Communications and "
    "Information Technology and the UAE Ministry of Investment signed an MoU covering 1 "
    "GW of planned data-centre capacity, and a green data-centre project of about 200 MW "
    "of solar and wind is in the official plan. Egypt had about 121m active cellular "
    "connections and 82.7% internet penetration in early 2026",
    "Arizton / Research and Markets, 'Egypt Data Center Market Investment Analysis "
    "2026-2031', published 27 April 2026 — which names RAYA DATA CENTER among the "
    "market's key investors alongside ECC Solutions, e& Egypt, GPX Global Systems, "
    "Orange Business and Telecom Egypt", PRESS, "2026-04-27",
    detail="Raya for Data Centres Company is a 100%-owned subsidiary (F29) and RDC was "
           "4.1% of Raya Information Technology's 1Q-2026 revenue; Raya Network "
           "Services, which sells the data-centre infrastructure, rose from 8% of RIT "
           "revenue in FY2024 to 19% in FY2025 (F32).",
    model_impact="DRIVER UNLOCK for the RIT build (D4): the RNS and RDC lines are set "
                 "against a named external capacity pipeline rather than a growth rate, "
                 "and the 18.97% market CAGR is the ceiling the company-level line is "
                 "tested against.")

f_bpo = R.add(Ring.INDUSTRY, "demand drivers & capacity/supply balance", FindingClass.D,
    "Egypt's BPO sector produced about USD 3.2bn of revenue in 2025 and is projected to "
    "compound at 13.5% to 2030, above the 8.5% global average; Egypt is about 27% of the "
    "MENA BPO market. The Ministry of Communications and Information Technology set a "
    "2026 target of USD 6bn of outsourcing exports, and ITIDA projects the industry at "
    "1.2-1.4% of GDP by 2026",
    "Stealth Agents, 'Egypt BPO Statistics 2026', compiled from ITIDA and MCIT figures; "
    "MCIT export target as reported by Outsource Accelerator", PRESS, "2026-01-01",
    detail="Third-party compilation of official targets rather than a primary ITIDA "
           "release; the ITIDA and MCIT figures inside it are the government's own and "
           "are what the driver leans on.",
    model_impact="DRIVER UNLOCK for the RCX build (D7): sets the demand ceiling against "
                 "which RCX's own 9.2k seat capacity at 81% utilisation is projected, "
                 "and is the reason the seat build carries an export-led offshore leg "
                 "separate from the onshore Egyptian one.")

f_price = R.add(Ring.INDUSTRY, "pricing", FindingClass.S,
    "The 2026 handset market is a PRICE market, not a volume market: units fall 16.7% "
    "while average selling price rises 27.6% to USD 581 and market value rises 6.3%. In "
    "Egypt the 38.5% traveller tariff raises the landed cost of grey-channel devices "
    "while fifteen locally manufacturing brands add lower-priced domestic supply. Raya's "
    "own realised trade margin moved the other way from its revenue: Raya Trade gross "
    "margin fell from 10.4% (FY2024) to 9.6% (FY2025) on 31.1% revenue growth, and group "
    "gross margin collapsed to 16.77% in Q2-2026 from 22.26% in Q2-2025",
    "IDC and Gartner 2026 forecasts (F02, F03); NTRA decision of 21 January 2026 (F08); "
    "Raya Holding FY2025 earnings release and reviewed H1-2026 interim statements",
    PRESS, "2026-08-12",
    model_impact="Sets the PRICE leg of D2 and D3 and is the reason gross margin is an "
                 "OUTPUT of a volume-and-price build rather than an input. A margin "
                 "assumption carried forward from FY2025 would have missed a 5.5-point "
                 "fall inside two quarters.")

f_new = R.add(Ring.INDUSTRY, "new entrants (named-competitor level)", FindingClass.S,
    "Named new entrants into Egypt's data-centre market in 2024: AFRICA DATA CENTRES, "
    "GULF DATA HUB and KHAZNA DATA CENTERS, against incumbents GPX GLOBAL SYSTEMS, EGID, "
    "e& EGYPT (Etisalat Misr), TELECOM EGYPT, ECC SOLUTIONS, ORANGE BUSINESS and RAYA "
    "DATA CENTER. In consumer-electronics retail the named scale competitor is B.TECH — "
    "an omnichannel retailer AND consumer-finance platform with 88+ branches across 25 "
    "governorates and 600+ dealers and distributors — alongside 2B",
    "Arizton Egypt data-centre market report, 27 April 2026; B.TECH company profile",
    PRESS, "2026-04-27",
    detail="B.TECH is the structurally important one: it is the same combination Raya "
           "runs (electronics retail plus captive consumer finance through Aman), which "
           "means the two groups compete on BOTH legs at once rather than on one.",
    model_impact="Caps the RIT data-centre revenue path (D4) and the Raya Trade retail "
                 "share path (D2). Three Gulf-backed entrants arriving inside the "
                 "forecast window is the named mechanism behind the bear case on RDC "
                 "pricing.")

f_ai = R.add(Ring.INDUSTRY, "technology substitution", FindingClass.S,
    "Generative AI is absorbing exactly the work BPO scaled: Gartner projects AI "
    "deployment will cut call-centre labour costs by USD 80bn in 2026, while also "
    "projecting that even by 2027 only about 14% of customer interactions will be FULLY "
    "handled by AI, leaving 86% with a human directly or assisted. Forrester expects 30% "
    "of enterprises to stand up parallel AI service functions by end-2026",
    "Gartner and Forrester 2026 projections as compiled by named industry trade sources",
    PRESS, "2026-01-01",
    detail="The two Gartner numbers point opposite ways and BOTH are carried: an USD 80bn "
           "cost-out is a demand shock to a seat-based revenue model, and a 14% "
           "full-automation ceiling by 2027 is a floor under the human seat base inside "
           "the forecast window. RCX itself reported 29.3% revenue growth in H1-2026 "
           "with margin at 42.5%, so the substitution has not yet shown in the numbers.",
    model_impact="Sets the RCX margin path and its downside branch (D8). The base holds "
                 "the disclosed seat and utilisation trajectory; the bear case prices a "
                 "seat-price deflation consistent with the USD 80bn cost-out, applied to "
                 "the 13.4% of group H1-2026 EBITDA RCX contributes. Modelled as an "
                 "explicit sensitivity, never as a haircut buried in the margin.")

f_comp = R.add(Ring.INDUSTRY, "competitor capacity / price moves (named)", FindingClass.D,
    "Named BPO delivery capacity in Egypt: TELEPERFORMANCE 4,000+ seats across two Cairo "
    "campuses, SUTHERLAND GLOBAL SERVICES 2,500+ seats at Smart Village, CONCENTRIX 1,800 "
    "seats in New Cairo, MAJOREL 1,400 seats in Cairo — about 9,700 seats between the "
    "four. Raya Customer Experience alone reports 9.2k seat capacity at 81% utilisation "
    "with 7,000+ agents in 6 countries and 15 languages. In IT, Raya Information "
    "Technology discloses a 60% share of the Egyptian ATM market",
    "Egypt BPO capacity compilation from named operators' own disclosures; RCX and RIT "
    "figures from Raya Holding's 1Q-2026 and FY2025 investor presentations", PRESS,
    "2026-08-01",
    detail="On these numbers RCX is the single largest seat base in Egypt, roughly equal "
           "to the four named multinationals combined. That is a share statement, and it "
           "is the reason the RCX driver is built on ITS OWN capacity and utilisation "
           "rather than on a share of a market total.",
    model_impact="DRIVER UNLOCK for D7 and D18: gives the competitive capacity "
                 "denominator for the RCX seat build and the named comparators for the "
                 "relative-multiple lens. Also bounds RIT's ATM-linked revenue, since a "
                 "60% share cannot grow much on share and must grow on the installed "
                 "base and the 5-year refresh cycle the company discloses.")

# --------------------------------------------------------------- RING 4  COMPANY
# ---- official financial statements: four audited years + both study-year quarters
f_fs25 = R.add(Ring.COMPANY, "official financial statements", FindingClass.D,
    "FY2025 AUDITED CONSOLIDATED PROFIT OR LOSS (UHY United, Cairo, 5 March 2026, "
    "unqualified 'true and fair view' opinion, Egyptian Accounting Standards). Revenues "
    "EGP 63,829,420,695; cost of revenues (50,138,748,041); GROSS PROFIT 13,690,672,654 "
    "(21.45%); G&A (4,662,443,816); board remuneration (2,987,668); selling and "
    "marketing (2,191,219,120); expected credit losses (404,958,565) with 18,621,665 "
    "reversed; provisions (96,098,879); ECL other debit balances (11,465,244); OPERATING "
    "PROFITS 6,340,121,027; finance cost net (2,369,169,940); FX +6,988,182; associates "
    "132,375,655; dividends 2,555,780; gain on sale of fixed assets 70,507,658; other "
    "income 50,574,323; takaful (97,954,478); goodwill impairment (11,106,449); PBT "
    "4,124,891,758; income taxes (1,190,888,130); NET PROFIT 2,934,003,628, of which "
    "holding company 2,588,357,394 and non-controlling interest 345,646,234",
    "Raya Holding Company for Financial Investments, audited consolidated financial "
    "statements for the year ended 31 December 2025, statement of consolidated profit or "
    "loss, printed page 4", CO, "2026-03-05",
    url="https://rayacorp.com/wp-content/uploads/2026/04/RH-Consolidated-FY-2025-EN_compressed.pdf",
    detail="IMAGE-ONLY FILING: 49 pages, pdftotext returns 0 characters. Read by "
           "rendering at 200 dpi and reading the pixels. EVERY SUBTOTAL RE-ADDED AND "
           "EVERY ONE FOOTS EXACTLY on both the FY2025 and the FY2024 comparative "
           "column: gross profit, operating profits, PBT, net profit and the "
           "holding/NCI split all reproduce to the pound. No route disagreement on this "
           "page.",
    is_fs_data=True, fiscal_period="FY2025",
    model_impact="The revenue and cost base the whole model is built from, and the "
                 "denominator for every margin the study reports.")

f_bs25 = R.add(Ring.COMPANY, "official financial statements", FindingClass.D,
    "FY2025 AUDITED CONSOLIDATED STATEMENT OF FINANCIAL POSITION at 31 December 2025. "
    "Total non-current assets EGP 6,259,354,874; total current assets 44,428,185,936; "
    "TOTAL ASSETS 50,687,540,810. Equity before non-controlling interest 5,858,704,688; "
    "non-controlling interest 2,545,623,485; TOTAL EQUITY 8,404,328,173. Total "
    "non-current liabilities 4,571,309,818; total current liabilities 37,711,902,819; "
    "TOTAL LIABILITIES 42,283,212,637. Issued and paid-up capital 1,070,324,442; "
    "retained earnings 2,060,223,258; periodic distributions (202,908,010); treasury "
    "shares (9,978,744)",
    "Raya Holding audited consolidated financial statements, year ended 31 December "
    "2025, statement of consolidated financial position, printed page 3", CO,
    "2026-03-05",
    url="https://rayacorp.com/wp-content/uploads/2026/04/RH-Consolidated-FY-2025-EN_compressed.pdf",
    detail="ALL EIGHT SUBTOTALS OF THE 2025 COLUMN RE-ADDED AND ALL EIGHT FOOT EXACTLY, "
           "and total equity plus total liabilities equals total assets to the pound. "
           "ONE FOOTING BREAK PRINTED IN THE FILING ITSELF, in the FY2024 COMPARATIVE "
           "column: total assets prints 39,112,323,637 while total equity and "
           "liabilities prints 39,112,323,635, a 2 EGP cross-foot break. It is a break "
           "introduced by the FY2025 filing's restatement of the comparative — the "
           "FY2024 filing as issued cross-foots exactly at 39,112,323,637 on both sides "
           "(F21). Recorded rather than smoothed; immaterial in size, but a printed "
           "subtotal is not evidence on its own.",
    is_fs_data=True, fiscal_period="FY2025",
    model_impact="Fixes the capital structure and the equity bridge. Non-controlling "
                 "interest is 30.29% of total equity here against an 11.78% share of "
                 "FY2025 profit — the single most important number on this page for a "
                 "holding company, and the reason D20 exists.")

f_fs24 = R.add(Ring.COMPANY, "official financial statements", FindingClass.D,
    "FY2024 AUDITED CONSOLIDATED, AS FILED. Revenues EGP 45,119,062,433; cost "
    "(35,699,590,618); gross profit 9,419,471,815 (20.88%); operating profits "
    "3,767,436,110; PBT 2,718,072,788; income taxes (818,860,504); net profit "
    "1,899,212,284, holding company 1,688,543,816, NCI 210,668,468. Total assets "
    "39,112,323,637; total liabilities 34,360,357,571; total equity 4,751,966,064 "
    "(before NCI 3,733,435,791; NCI 1,018,530,273)",
    "Raya Holding audited consolidated financial statements, year ended 31 December "
    "2024, printed pages 3 and 4", CO, "2025-03-01",
    url="https://rayacorp.com/wp-content/uploads/2024/12/RH-Consolidated-FS-31-Dec-2024-ENG.pdf",
    detail="ROUTE DISAGREEMENT RESOLVED BY ARITHMETIC. Accounts and notes receivable "
           "read at 110 dpi as EGP 14,600,882,485; on that figure the current-asset "
           "column sums to 33,927,632,700 against a printed 33,927,432,700 — 200,000 "
           "high. Re-rendered at 300 dpi the same cell reads EGP 14,600,682,485, on "
           "which the column foots EXACTLY, and the FY2024 filing itself prints "
           "14,600,682,485. An 8 read for a 6, in a figure that looked entirely "
           "plausible. SECOND OBSERVATION: this filing prints equity before NCI as "
           "3,733,435,791 while its own components sum to 3,733,435,792 and the FY2025 "
           "filing's comparative prints 3,733,435,792 — a 1 EGP difference in how the "
           "two filings split equity from NCI. Total equity is 4,751,966,064 in both.",
    is_fs_data=True, fiscal_period="FY2024",
    model_impact="Second historical year, and the base against which the FY2025 "
                 "step-change (revenue +41.5%, net profit +54.5%) is measured.")

f_fs23 = R.add(Ring.COMPANY, "official financial statements", FindingClass.D,
    "FY2023 AUDITED CONSOLIDATED, AS FILED. Revenues EGP 31,295,348,778; cost "
    "(24,917,023,895); gross profit 6,378,324,883 (20.38%); operating profit "
    "2,235,401,624; PBT 929,572,455; income taxes (365,690,953); net profit 563,881,502, "
    "holding company 441,356,745, NCI 122,524,757. Total assets 27,148,953,582; total "
    "liabilities 24,225,553,381; total equity 2,923,400,201 (before NCI 2,073,755,759; "
    "NCI 849,644,442)",
    "Raya Holding audited consolidated financial statements, year ended 31 December "
    "2023, printed pages 4 and 5", CO, "2024-03-01",
    url="https://rayacorp.com/wp-content/uploads/2024/09/Consolidated-FS-YE-2023-en.pdf",
    detail="A RESTATEMENT AND TWO PRINTED FOOTING BREAKS, both found by re-adding. "
           "(a) RESTATEMENT: the FY2023 filing shows bank overdraft of EGP 9,128,146,931 "
           "entirely as a CURRENT liability; the FY2024 filing's comparative splits the "
           "same balance into credit facilities 8,430,891,585 current and long-term bank "
           "overdraft 697,255,346 non-current. The difference is EXACTLY 697,255,346. "
           "Total liabilities is 24,225,553,381 in both. A leverage or current-ratio "
           "driver built off the FY2023 filing and rolled against FY2024 would compare "
           "two different definitions. (b) In the FY2024 filing's FY2023 comparative "
           "column the printed non-current-liability subtotal (3,082,119,145) is 4 EGP "
           "ABOVE the sum of its own components (3,082,119,141) and the printed "
           "current-liability subtotal (21,143,434,237) is 3 EGP BELOW its components "
           "(21,143,434,240). Both were re-read at 300 dpi and both reproduce, so these "
           "are print errors in the filing, not read errors. Total liabilities and the "
           "balance-sheet identity hold exactly on the component sums.",
    is_fs_data=True, fiscal_period="FY2023",
    model_impact="Third historical year. Its 21.73% NCI share of profit is the high "
                 "end of the five-period range and is what makes a blended NCI ratio "
                 "indefensible (D20).")

f_fs22 = R.add(Ring.COMPANY, "official financial statements", FindingClass.D,
    "FY2022 AUDITED CONSOLIDATED. Revenues EGP 20,413,178,508; cost (16,340,567,809); "
    "gross profit 4,072,610,699 (19.95%); operating profit 1,247,826,774; PBT "
    "624,320,670; income taxes (205,087,593); net profit 419,233,077, holding company "
    "347,313,087, NCI 71,919,990. Total assets 20,770,171,955; total liabilities "
    "18,512,849,391; total equity 2,257,322,564 (before NCI 1,690,565,139; NCI "
    "566,757,426)",
    "Raya Holding audited consolidated financial statements, year ended 31 December "
    "2022 (Arabic original), and the FY2022 comparative column of the FY2023 audited "
    "consolidated filing (English)", CO, "2023-03-01",
    url="https://rayacorp.com/wp-content/uploads/2024/09/Consolidated-FS-YE-2022.pdf",
    detail="TWO INDEPENDENT ROUTES, AND THE ARITHMETIC ARBITRATED. The only FY2022 "
           "consolidated filing the company publishes is the ARABIC original, whose "
           "figures are set in Eastern Arabic-Indic numerals on a scan with no text "
           "layer. It was transcribed by eye, then checked against the ENGLISH FY2022 "
           "comparative column inside the FY2023 filing. The income statement agrees on "
           "both routes and foots exactly on both. The balance sheet DID NOT: the Arabic "
           "route read intangible assets as EGP 19,561,819, on which non-current assets "
           "sum to 4,005,137,253 against a printed 4,005,236,753 — 99,500 short. The "
           "English comparative reads 19,661,819, on which the column foots EXACTLY to "
           "the printed 4,005,236,755. A 5 read for a 6. The Arabic route also misread "
           "the legal reserve (92,501,015 for 92,010,015), treasury shares (53,585,977 "
           "for 53,685,978) and accumulated translation differences (2,869,605 for "
           "2,849,605); every one of those is settled by the English column, which foots "
           "throughout. NOTE the two filings differ by 2 EGP on total non-current assets "
           "(4,005,236,753 Arabic against 4,005,236,755 English) and by 2 EGP on total "
           "current assets, but agree exactly on total assets, 20,770,171,955.",
    is_fs_data=True, fiscal_period="FY2022",
    model_impact="Fourth historical year — the target depth, not the floor. Gives a "
                 "four-year revenue CAGR of 46.2% and a four-year gross-margin path of "
                 "19.95% / 20.38% / 20.88% / 21.45%, which is the series the Q2-2026 "
                 "collapse to 16.77% has to be judged against.")

f_q1 = R.add(Ring.COMPANY, "official financial statements", FindingClass.D,
    "Q1-2026 REVIEWED CONSOLIDATED INTERIM, three months ended 31 March 2026. Revenues "
    "EGP 15,815,579,610; cost (12,359,605,613); GROSS PROFIT 3,455,973,997 (21.85%); "
    "operating profits 1,214,687,068; finance cost (487,336,084); FX (87,727,587); "
    "associates 54,229,494; PBT 706,592,692; income taxes (253,632,286); net profit "
    "452,960,406, holding company 384,009,190, NCI 68,951,216. Comparative Q1-2025: "
    "revenue 12,881,656,826, gross profit 2,687,859,725 (20.87%), net profit 387,896,239",
    "Raya Holding reviewed consolidated interim financial statements for the three "
    "months ended 31 March 2026, printed page 4", CO, "2026-05-14",
    url="https://rayacorp.com/wp-content/uploads/2026/06/Raya-Holding-Consolidated-31-Mar-2026-English.pdf",
    detail="46 pages, image-only, zero text characters; read off the pixels at 130 dpi. "
           "Every line re-added: gross profit, operating profits, PBT, net profit and "
           "the holding/NCI split all foot exactly on both columns. Q1 plus Q2 revenue "
           "(15,815,579,610 + 17,972,396,843) reproduces the H1 figure to within 1 EGP.",
    is_fs_data=True, fiscal_period="Q1-2026",
    model_impact="First quarter of the study year, swept BEFORE the build. Its 21.85% "
                 "gross margin is close to the FY2025 average and on its own would have "
                 "supported a flat-margin forecast — which Q2 then destroyed. Both "
                 "quarters are in the register for exactly that reason.")

f_q2 = R.add(Ring.COMPANY, "official financial statements", FindingClass.B,
    "H1-2026 AND Q2-2026 REVIEWED CONSOLIDATED INTERIM (limited review report attached; "
    "board authorised 12 August 2026). SIX MONTHS: revenues EGP 33,787,976,454; cost "
    "(27,317,409,179); gross profit 6,470,567,275 (19.15%); operating profits "
    "1,821,284,734; finance cost (1,060,289,247); CAPITAL GAIN FROM SALE OF INVESTMENT "
    "450,508,721; PBT 1,250,300,668; taxes (368,155,056); net profit 882,145,612, "
    "holding company 739,102,032, NCI 143,043,580. THREE MONTHS (Q2 STANDALONE, PRINTED "
    "AS ITS OWN COLUMN): revenues 17,972,396,843; cost (14,957,803,566); gross profit "
    "3,014,593,277 — A 16.77% MARGIN AGAINST 22.26% IN Q2-2025 AND 21.85% IN Q1-2026; "
    "operating profits 606,597,665; finance cost (572,953,164); PBT 543,707,974; net "
    "profit 429,185,203",
    "Raya Holding reviewed consolidated interim financial statements for the six months "
    "ended 30 June 2026, printed pages 3 and 4", CO, "2026-08-12",
    url="https://rayacorp.com/wp-content/uploads/2026/09/Raya-Holding-Cons.-30-Jun-2026-English.pdf",
    detail="44 pages, image-only. Every column re-added and every subtotal foots "
           "exactly, including both three-month columns. ONE ROUTE DISAGREEMENT: the "
           "FVOCI revaluation reserve read at 100 dpi as EGP 27,691,078, on which equity "
           "before NCI sums 100 short of the printed 6,611,896,072; at 300 dpi it reads "
           "27,691,178, on which it foots exactly. A 1 read for a 0. THE NUMBER THAT "
           "MATTERS MOST ON THIS PAGE: of Q2-2026's EGP 543,707,974 pre-tax profit, EGP "
           "450,508,721 is the one-off gain on the Ostool disposal (F34). Strip it and "
           "Q2-2026 pre-tax profit is EGP 93,199,253 — 82.9% of the quarter's pre-tax "
           "profit is a disposal, not trading. Balance sheet at 30 June 2026: total "
           "assets 57,840,084,517; total liabilities 48,364,215,922; total equity "
           "9,475,868,595 of which NCI 2,863,972,523 (30.22%).",
    is_fs_data=True, fiscal_period="Q2-2026",
    model_impact="BASE CHANGER, twice over. (1) The gross-margin base resets from 21.4% "
                 "to 16.8% inside one quarter, so the forecast margin path starts from "
                 "the Q2 exit rate and recovers on a named mechanism (the memory cycle, "
                 "F02) rather than reverting to the FY2025 average. (2) The disposal "
                 "gain is modelled as an explicit dated event and the FY2026 headline is "
                 "dual-framed with and without it — never smoothed into an earnings "
                 "glide.")

# ---- regular disclosures: the segment note, the by-type notes, the subsidiary list
f_seg = R.add(Ring.COMPANY, "regular disclosures", FindingClass.D,
    "THE SEGMENT NOTE, AND IT IS THE JOIN THE WHOLE BUILD RESTS ON. Note 29 'SEGEMENT "
    "REPORTING' (the filing's own spelling) discloses SIX lines per segment — Revenues, "
    "Cost, Depreciation for the Year, profit for the Year, Total Assets, Total "
    "Liabilities — for FOURTEEN named sectors plus eliminations and a consolidated "
    "column, in both the FY2025 audited filing and the H1-2026 reviewed interim. FY2025 "
    "revenue / cost, EGP thousands: Trade and distribution 23,823,293 / (21,524,518); "
    "Information technology 17,666,779 / (14,012,011); Call centers 2,838,963 / "
    "(1,502,762); Finance lease 256,489 / (103,954); International services 743,314 / "
    "(414,377); Land Transportation 2,506,577 / (2,233,730); Restaurants 292,710 / "
    "(136,176); Non-Bank Financial Services 9,550,296 / (5,534,472); Manufacturing and "
    "export 2,264,169 / (1,995,310); canned foods 2,204,311 / (1,484,747); Vehicles "
    "Manufacturing 1,791,411 / (1,378,201); Electrical appliances manufacturing 885,339 "
    "/ (815,721); Securitization 3,000 / nil; Other activities nil; Eliminations "
    "(997,232) / 997,232. IMPLIED SEGMENT GROSS MARGINS RANGE FROM 7.86% (Electrical "
    "appliances) TO 59.47% (Finance lease) — an eightfold spread inside one issuer",
    "Raya Holding audited consolidated financial statements FY2025, note 29, printed "
    "page 43 (landscape); and reviewed interim H1-2026, note 29, printed page 40",
    CO, "2026-03-05",
    url="https://rayacorp.com/wp-content/uploads/2026/04/RH-Consolidated-FY-2025-EN_compressed.pdf",
    detail="RENDERED AT 220-300 dpi, ROTATED, AND EVERY COLUMN RE-ADDED. FOUR THINGS A "
           "LATER BUILD MUST KNOW. (1) THE FY2025 CONSOLIDATED COLUMN IS PHYSICALLY "
           "TRUNCATED AT THE RIGHT PAGE MARGIN in the published PDF — it prints '63,829', "
           "'(50,138,', '2,588', '50,143', '(42,283,' and stops. The consolidated totals "
           "had to be DERIVED by adding the segment columns and the eliminations column, "
           "and then checked against the primary statements. They tie: revenue "
           "63,829,419k against the printed P&L 63,829,421k, cost 50,138,747k against "
           "50,138,748k, total liabilities 42,283,212k against 42,283,213k — all within "
           "rounding at thousands. The H1-2026 interim's own consolidated column is NOT "
           "truncated and prints 33,787,976 / (27,317,409) / (485,475) / 739,102 / "
           "57,840,084 / (48,364,216), every one tying exactly to the interim statements. "
           "(2) THE 'profit for the Year' ROW SUMS TO THE ATTRIBUTABLE PROFIT, NOT TO "
           "NET PROFIT: the fourteen segments plus eliminations give 2,588,357k, which is "
           "the holding company's share, not the group's 2,934,004k. The eliminations "
           "column of (1,449,703k) therefore absorbs intersegment profit AND "
           "non-controlling interest AND holding-level costs, and the note does not "
           "split them (see N01 and D30). (3) SEGMENT TOTAL ASSETS DO NOT TIE TO THE "
           "BALANCE SHEET IN FY2025: the columns foot to 50,143,880k against a balance "
           "sheet of 50,687,541k, a gap of 543,661k which is within 1k of the FY2025 "
           "income-tax liability of 543,660k. Liabilities tie. (4) ROUTE DISAGREEMENT: "
           "the FY2024 comparative profit for Information technology prints as "
           "'1205,,097' with a doubled comma; the column foots to the attributable "
           "1,688,544k only on 1,205,097.",
    is_fs_data=True, fiscal_period="FY2025",
    model_impact="THE DRIVER UNLOCK THAT DECIDES EVERY MODE BELOW. Because COST is "
                 "disclosed per segment, every segment gross margin is an OUTPUT of a "
                 "revenue-and-cost build rather than an input — which is what makes D1 "
                 "through D15 bottom-up. Because NCI, headcount, capex, units and prices "
                 "are NOT disclosed per segment, D18, D19b, D30 and part of D20 stay "
                 "top-down and say so.")

f_seg2 = R.add(Ring.COMPANY, "regular disclosures", FindingClass.D,
    "THE SEGMENT NOTE MAPS ONE-FOR-ONE ONTO THE ELEVEN PORTFOLIO COMPANIES, AND THE "
    "RECONCILIATION IS EXACT. Raya Information Technology as reported in the earnings "
    "release (EGP 18,410mn FY2025 revenue) is the 'Information technology' segment "
    "(17,666,779k) PLUS the 'International services' segment (743,314k) — 18,410,093k, "
    "to the thousand; its gross profit likewise, 3,654,768k + 328,937k = 3,983,705k "
    "against a reported EGP 3,984mn. Aman Holding (EGP 9,553mn) is 'Non-Bank Financial "
    "Services' (9,550,296k) plus 'Securitization' (3,000k) = 9,553,296k. Raya Trade = "
    "Trade and distribution; Raya FMCG = Manufacturing and export; Raya Foods = canned "
    "foods; Raya Auto = Vehicles Manufacturing; Raya Electric = Electrical appliances "
    "manufacturing; Raya Smart Buildings = Finance lease; Ostool = Land Transportation; "
    "Raya Restaurants = Restaurants",
    "Raya Holding FY2025 audited segment note reconciled against the FY2025 earnings "
    "release per-company figures", CO, "2026-03-05",
    detail="ONE RECONCILIATION BREAK, AND IT IS FLAGGED RATHER THAN RESOLVED HERE. The "
           "'Call centers' segment and Raya Customer Experience agree on revenue "
           "(2,838,963k against EGP 2,839mn) but NOT on gross profit: the segment note "
           "implies 1,336,201k (47.07%) while the release reports EGP 1,274mn (44.9%), a "
           "62,201k difference. Every other company reconciles to within a rounding of "
           "the release. The likely cause is a perimeter difference between the segment "
           "and the reported entity — the group runs four separate contact-centre legal "
           "entities (Raya Contact Centre 60.13%, Call Centre Company C3 100%, Raya "
           "Contact Centre Gulf 100%, Raya Contact Centre Europe 100%) plus Raya for "
           "Contact Centre Building Management and Gulf customer experience at 85%. "
           "RESOLVE BEFORE SETTING THE RCX MARGIN; do not average the two.",
    is_fs_data=True, fiscal_period="FY2025",
    model_impact="Makes the eleven-company build auditable against the audited note "
                 "instead of resting on the release alone. It is what allows the "
                 "operating KPIs in the IR channel (seats, branches, capacity, GTV) to "
                 "be attached to audited revenue and cost lines.")

f_type = R.add(Ring.COMPANY, "regular disclosures", FindingClass.D,
    "REVENUE AND COST BY TYPE, BOTH SIDES, BOTH PERIODS. Note 24-A 'Revenues according "
    "to type', H1-2026 (EGP): devices and goods distribution 17,528,836,030; supplies "
    "and installations 6,902,089,606; non-bank financial services 2,222,696,619; call "
    "centre service 1,689,177,196; manufacture and export 1,578,880,603; canned foods "
    "1,044,077,698; vehicles manufacturing 992,054,133; transportation service "
    "984,835,688; electrical appliances 561,549,420; investment property 156,720,343; "
    "restaurant 127,059,118; securitization nil — total 33,787,976,454. Note 24-B by "
    "currency: local 24,658,434,522, foreign 9,129,541,932 (27.0%). NOTE 25 COST OF "
    "REVENUES BY NATURE: devices and goods distribution cost 15,729,838,558; supplies "
    "and installations 6,888,412,846; cost of materials used in production 2,193,696,187; "
    "salaries and wages 1,392,515,437; transportation service cost 862,258,221; "
    "depreciation of fixed assets, intangibles, investment property and right-of-use "
    "211,666,739; finance cost 27,421,281; other direct cost 11,599,910 — total "
    "27,317,409,179",
    "Raya Holding reviewed consolidated interim financial statements, six months ended "
    "30 June 2026, notes 24-A, 24-B, 25 and 26, printed page 38", CO, "2026-08-12",
    url="https://rayacorp.com/wp-content/uploads/2026/09/Raya-Holding-Cons.-30-Jun-2026-English.pdf",
    detail="Read at 250 dpi off the pixels and re-added. Note 24-A foots EXACTLY on both "
           "columns (33,787,976,454 and 27,777,677,893) and reproduces the P&L revenue "
           "line. Note 24-B foots exactly on both. Note 25 foots exactly for H1-2026 and "
           "to within 1 EGP for H1-2025 (components 21,773,459,971 against a printed "
           "21,773,459,972). Note 26 foots exactly on both. ONE PRINT ODDITY: the "
           "H1-2025 electrical-appliances revenue is set as '410.990.935' with full "
           "stops for thousands separators; the column foots only on 410,990,935.",
    is_fs_data=True, fiscal_period="Q2-2026",
    model_impact="DRIVER UNLOCK for the cost build (D16). Cost of revenues is projected "
                 "BY NATURE — eight lines with eight different escalators — instead of "
                 "as one COGS-to-revenue ratio. 'Devices and goods distribution cost', "
                 "57.6% of the H1-2026 cost base, is escalated on the imported-component "
                 "path (F02); 'salaries and wages' on the Egyptian CPI path (F06); "
                 "depreciation from the fixed-asset roll. That is the difference between "
                 "a model that could see the Q2 margin break coming and one that could "
                 "not.")

f_subs = R.add(Ring.COMPANY, "regular disclosures", FindingClass.D,
    "THE SUBSIDIARY LIST WITH OWNERSHIP PERCENTAGES, AND IT IS IDENTICAL AT 31-DEC-2025 "
    "AND 30-JUN-2026. Note 1 lists FORTY consolidated subsidiaries with country and "
    "percentage of ownership, plus SIXTEEN suspended companies. Twenty-nine of the forty "
    "are 100% owned. The eleven that are not: Raya Contact Centre Company 60.13% "
    "(Egypt); Ostool for Land Transport Company 90% (Egypt); Raya Restaurants Company "
    "95.423% (Egypt); Gulf customer experience 85% (Bahrain); AMAN TAQA 39% (Egypt); and "
    "six Aman entities at 76% each — Aman for Electronic Payments, Aman for Financial "
    "Services, Aman for Micro finance, Aman holding company for non-banking financial "
    "services and electronic payments, Aman for Consumer Finance, Aman Securitization. "
    "Foreign subsidiaries: UAE (Raya Gulf, Raya Contact Centre Gulf), Saudi Arabia (Raya "
    "Technology Company Ltd), Nigeria (Best Service Company), Poland (Raya Contact Centre "
    "Europe, Madova), Bahrain (Gulf customer experience)",
    "Raya Holding audited consolidated financial statements FY2025, note 1 'Group "
    "Background', printed page 8; and reviewed interim H1-2026, note 1, printed page 8",
    CO, "2026-03-05",
    url="https://rayacorp.com/wp-content/uploads/2026/04/RH-Consolidated-FY-2025-EN_compressed.pdf",
    detail="Read at 250 dpi to confirm the percentages, because they are load-bearing "
           "and 60.13 / 95.423 / 39 are exactly the kind of figure a low-resolution read "
           "corrupts. TWO THINGS TO FLAG. (a) AMAN TAQA IS CONSOLIDATED AT A 39% "
           "SHAREHOLDING — control below a majority, which the note asserts without "
           "explaining; the consolidation basis for it is not disclosed. (b) THE SAME "
           "FILING CONTRADICTS ITSELF ON OSTOOL: the H1-2026 subsidiary table says 90% "
           "while the transaction narrative on the facing page says Raya was 'the "
           "principal shareholder, holding an 89% stake'. The press and the buyer's own "
           "board disclosure both say 90%. The register records the contradiction rather "
           "than picking a number. (c) OSTOOL IS STILL LISTED AS A 90%-OWNED "
           "CONSOLIDATED SUBSIDIARY AT 30 JUNE 2026 even though the sale agreement was "
           "signed on 3 June 2026 and completed on 1 July 2026 — and yet its Total "
           "Assets and Total Liabilities cells in the H1-2026 segment note are BLANK "
           "while its revenue, cost, depreciation and profit are present. The assets "
           "column then falls 9,771k short of the printed consolidated total; the "
           "liabilities column foots. The correct reading is that Ostool's balance sheet "
           "is out at 30 June and its half-year profit and loss is in.",
    is_fs_data=True, fiscal_period="FY2025",
    model_impact="DRIVER UNLOCK for D20. Non-controlling interest is computed subsidiary "
                 "by subsidiary at these named percentages and NEVER as a blended ratio "
                 "of group profit — NCI took 11.09% of FY2024 profit, 21.73% of FY2023, "
                 "11.78% of FY2025 and 16.22% of H1-2026 while holding 30.2% of equity. "
                 "It also fixes which legs the parent can actually upstream cash from.")

f_debt = R.add(Ring.COMPANY, "regular disclosures", FindingClass.D,
    "DEBT STACK AND OFF-BALANCE-SHEET AT 30 JUNE 2026 (EGP). Current: short-term loans "
    "1,712,420,323; long-term loans and finance lease current portion 1,074,406,189; "
    "finance lease liability current portion 84,079,505; credit facilities 14,441,685,606. "
    "Non-current: long-term loans and finance lease arrangements 4,458,945,749; long-term "
    "bank overdraft 2,231,020,835; long-term finance lease liability 1,507,257,810; long "
    "term notes payable 87,077,233. Cash on hand and at banks 5,621,545,213. CONTINGENT: "
    "letters of guarantee issued by subsidiaries' banks in favour of third parties EGP "
    "8,785,257,276 at 30 June 2026 against 7,763,957,858 at 31 December 2025, of which "
    "8,517,981,983 UNCOVERED (31-Dec-2025: 7,474,636,545) and 267,275,293 covered and "
    "carried inside prepaid expenses and other debit balances",
    "Raya Holding reviewed consolidated interim financial statements H1-2026, statement "
    "of consolidated financial position and note 34 'Contingent Liabilities'",
    CO, "2026-08-12",
    detail="The guarantee split re-adds exactly on both dates (8,517,981,983 + "
           "267,275,293 = 8,785,257,276; 7,474,636,545 + 289,321,313 = 7,763,957,858). "
           "The uncovered letters of guarantee are 90% of total equity and grew 14% in "
           "six months — larger than the group's entire equity before NCI.",
    is_fs_data=True, fiscal_period="Q2-2026",
    model_impact="Fixes the interest-bearing debt for D22 and the enterprise-to-equity "
                 "bridge, and puts the uncovered guarantee balance into the risk section "
                 "as a named, dated exposure rather than a footnote.")

# ---- IR communications: the channel that carries every operating quantity
f_ir_h1 = R.add(Ring.COMPANY, "IR communications (calls, presentations, releases)",
    FindingClass.D,
    "2Q AND 1H-2026 EARNINGS RELEASE, 12 August 2026 — THE NEWEST RELEASE, AND ITS "
    "ANCHORS SUPERSEDE EVERY OLDER ONE IN THE DRIVER SET. Group H1-2026: revenue EGP "
    "33,788mn (+21.6%), gross profit 6,471mn (+7.8%, 19.2% margin), EBITDA 2,900mn "
    "(-9.5%, 8.6% margin), net profit before minority 882mn (-9.2%), after minority 739mn "
    "(-17.1%). Q2-2026: revenue 17,972mn, gross profit 3,015mn (16.8%), EBITDA 1,105mn "
    "(6.2%), net profit before minority 429mn. PER PORTFOLIO COMPANY, H1-2026 revenue and "
    "gross profit (EGP mn): Raya Trade 14,751 (+51.9%) / 1,278 (+23.0%); Raya Information "
    "Technology 7,040 (-12.8% from 8,077); Aman 5,353 (+37.9%) / 2,177 (+37.5%, 40.7%); "
    "Raya Customer Experience 1,704 (+29.3%) / 724 (+19.9%, 42.5%); Raya FMCG 1,579 "
    "(+41.2%) / 163 (+37.0%); Raya Foods 1,044 (-19.4%) / 139 (-66.9% from 419); Ostool "
    "985 (-22.7%) / 123 (-14.0%, 12.4%); Raya Auto 992 (+15.6%); Raya Electric 562 "
    "(+36.6%) / 53 (+180.8%, 9.4%); Raya Smart Buildings 157 (+30.8%) / 88 (+26.7%); Raya "
    "Restaurants 127 (+4.9%) / 69 (+16.2%). Foreign-currency revenue EGP 9,130mn, 27.0% "
    "of group. Aman gross transaction value EGP 67.6bn in H1-2026 against 43.9bn, +54%. "
    "RCX: contact-centre services 57.6% of revenue, offshore 68.9% / onshore 31.1%, Egypt "
    "79.2% / Gulf 19.5% / Europe 1.3%. Five of eleven portfolio companies expanded into "
    "Saudi Arabia during H1-2026. Group headcount over 22,000",
    "Raya Holding for Financial Investments, 2Q & 1H-2026 Earnings Release, Cairo, 12 "
    "August 2026", IR, "2026-08-12",
    url="https://rayacorp.com/wp-content/uploads/2026/09/Raya-Holding-Earning-Release-1H-2026-Final-EN.pdf",
    fiscal_period="Q2-2026",
    detail="Digital PDF with a text layer, so no OCR risk. The release's own Appendix 1 "
           "income statement and Appendix 2 balance sheet reproduce the reviewed interim "
           "statements at EGP million precision, which is an independent check on the "
           "pixel reads at F25. TWO DEFINITIONAL DIFFERENCES A BUILD MUST NOT MIX: the "
           "release's EBITDA is gross profit less G&A, selling and marketing and board "
           "remuneration — i.e. BEFORE all depreciation, expected credit losses, "
           "provisions and goodwill impairment — and its 'Operating Profit' of EGP "
           "1,821mn matches the audited 'OPERATING PROFITS' of 1,821,284,734 for H1 but "
           "did NOT match for FY2025 (release 6,329 against audited 6,340), where the "
           "release deducts goodwill impairment above the line and the filing puts it "
           "below.",
    model_impact="THE PER-COMPANY REVENUE AND GROSS-PROFIT ANCHORS FOR D1-D15, and the "
                 "only source for gross transaction value, geographic mix and the "
                 "offshore/onshore split. Its 2H-2026 statement is the company's own "
                 "guidance and is carried at F39.")

f_ir_kpi = R.add(Ring.COMPANY, "IR communications (calls, presentations, releases)",
    FindingClass.D,
    "THE OPERATING QUANTITIES NO FINANCIAL STATEMENT CARRIES, from the FY2025 earnings "
    "release (5 March 2026), the FY2025 investor presentation (July 2026) and the 1Q-2026 "
    "investor presentation (August 2026). RAYA TRADE: 8,500+ dealers, 65+ retail outlets, "
    "48 service centres, Nigeria since 2007; FY2025 revenue mix mobile distribution and "
    "retail 52.9%, consumer electronics and Mazaya 16.2%, Nigeria 20.8%; 1Q-2026 mix "
    "retail 24.1%, mobile 21.5%, Nigeria 19.4%, consumer electronics 18.8%, Mazaya 6.9%, "
    "EZEE 4.3%. RAYA IT: 60% ATM MARKET SHARE, 95+ services, 1,000+ enterprise customers, "
    "90+ technology partners, 3 operating countries, 5-year average tech refresh, "
    "verticals government 20% / commercial 6% / oil and gas 2%; FY2025 mix Raya "
    "Integration 74%, Raya Network Services 19% (from 8% in FY2024), RIS 4.0%, RDC 3.0%. "
    "AMAN: 250+ branches, 6 fintech licences, 23 governorates, total portfolio EGP 9.7bn, "
    "active issuances 6.7bn, matured 3.0bn; FY2025 GTV EGP 103,859mn (+47.6%); net revenue "
    "mix financial spread 38.8% / digital consumer goods 31.3% / acquisition and "
    "transaction fees 29.9%. RCX: 9.2k SEAT CAPACITY AT 81% UTILISATION, 7,000+ agents, 6 "
    "countries, 15 languages, 100+ clients, 25+ languages served, 16m+ transactions; mix "
    "outsourcing 54.7% / hosting 25.6% / insourcing 19.7%. RAYA FOODS: no.1 exporter of "
    "frozen fruit and vegetables in Egypt, 35k production capacity, 20k sqm plant, 50+ "
    "export countries, strawberry 96.4% of FY2025 sales, 95% of revenue in foreign "
    "currency, USA and Europe 78% / China 11%. RAYA FMCG: 70,000+ points of sale in 14 "
    "governorates, food 66% / non-food 34%. RAYA ELECTRIC: 300k units annual production "
    "capacity TODAY against a 1.5M-unit 2026 pipeline; OEM/ODM for LG, Carrier, "
    "De'Longhi and Elaraby. RAYA SMART BUILDINGS: 70k sqm built-up area, 43k sqm gross "
    "leasable area, 99% OCCUPANCY, plus ~7k sqm of 2026 launches. RAYA RESTAURANTS: 13 "
    "outlets, 500k customers served, Ovio 94.9% / The Lebanese Bakery 3.2%. RAYA AUTO: EV "
    "76% of FY2025 revenue",
    "Raya Holding FY2025 Earnings Release; Raya Holding FY2025 Investor Presentation; "
    "Raya Holding 1Q-2026 Investor Presentation", IR, "2026-08-01",
    url="https://rayacorp.com/wp-content/uploads/2026/07/RH-Investor-Presentation-FY2025.pdf",
    fiscal_period="FY2025",
    detail="THIS IS WHY [INVARIANT 8] EXISTS ON THIS NAME. Not one of these quantities "
           "appears in any of the six financial statements. Seats, utilisation, branches, "
           "production capacity in units, gross leasable area, occupancy, outlets, ATM "
           "share and gross transaction value are all IR-channel only, and they are the "
           "denominators every bottom-up driver below divides by.",
    model_impact="DRIVER UNLOCK for D2, D4, D5, D7, D9, D10, D11, D12, D13 and D14. "
                 "Converts nine of the eleven portfolio companies from a revenue growth "
                 "rate to a capacity-times-utilisation or a volume-times-price build. "
                 "FLAGGED GAP: even here there is no unit PRICE for anything — no revenue "
                 "per seat, per branch, per sqm or per handset is published, so the price "
                 "leg is solved from disclosed revenue divided by the disclosed capacity "
                 "rather than sourced (see N03).")

f_ir_q1 = R.add(Ring.COMPANY, "IR communications (calls, presentations, releases)",
    FindingClass.D,
    "1Q-2026 EARNINGS RELEASE and 1Q-2026 FACT SHEET. Group 1Q-2026: revenue EGP "
    "15,816mn (+22.8% year-on-year), gross profit 3,456mn (+28.6%, 22.0% margin), EBITDA "
    "1,795mn (+28.6%, 11.3% margin), net profit before minority 453mn (2.9% margin), "
    "after minority 384mn. Per company 1Q-2026 revenue / gross profit / EBITDA / net "
    "profit (EGP mn): Raya Trade 3,410 (-1.7%) / 1,201 (+61.6%) / 985 (+75.0%) / 679 "
    "(+76.9%); Raya IT 2,526 (+46.7%) / 991 (+54.6%) / 215 (+328.7%) / 25 (+153.6%); RCX "
    "855 (+34.7%) / 365 (+24.6%) / 189 (-22.8%) / 80 (+22.0%); Raya FMCG 755 (+35.6%) / "
    "75 (+33.6%) / 24 (+26.1%) / 8 (+19.1%); Ostool 492 (-33.9%) / 51 (-23.2%); Raya "
    "Foods 429 (-19.1%) / 67 (-63.2%) / -6 / NET LOSS -177; Raya Electric 218 (+24.8%) / "
    "9 / 1 / -10; Raya Restaurants 51 (flat) / 26 / -4. Revenue mix 1Q-2026: Trade 43.0%, "
    "RIT 21.6%, Aman 16.0%, RCX 5.4%, FMCG 4.9%, Ostool 3.1%, Auto 2.8%. EBITDA mix: RIT "
    "54.9%, Trade 16.6%, Aman 12.0%, RCX 10.5%, RSB 2.2%, Ostool 2.0%",
    "Raya Holding 1Q-2026 Earnings Release (June 2026) and 1Q-2026 Fact Sheet; 1Q-2026 "
    "Investor Presentation", IR, "2026-06-01",
    url="https://rayacorp.com/wp-content/uploads/2026/06/Raya-Holding-Earning-Release-1Q-2026-EN-Final.pdf",
    fiscal_period="Q1-2026",
    detail="Q1 IS WHERE THE DIVERGENCE INSIDE THE GROUP IS VISIBLE AND THE GROUP TOTAL "
           "HIDES IT: in one quarter Raya Trade's gross profit rose 61.6% on revenue that "
           "FELL 1.7%, while Raya Foods' gross profit fell 63.2% and it posted a EGP 177mn "
           "net loss. RIT alone was 54.9% of group EBITDA. A single blended margin on this "
           "issuer describes none of those four businesses.",
    model_impact="Second quarter of the study year swept before the build, and the "
                 "quarterly bridge that lets Q2-2026 be derived per company (H1 less Q1) "
                 "where the company reports only halves.")

# ---- one-off base-resetting transactions, ownership, capital actions, guidance
f_ostool = R.add(Ring.COMPANY, "one-off base-resetting transactions", FindingClass.B,
    "THE OSTOOL DISPOSAL — THE NAMED TRANSACTION, COMPLETED INSIDE THE STUDY YEAR. On 13 "
    "May 2026 Raya Holding's board approved a purchase offer from ASEC COMPANY FOR MINING "
    "(ASCOM, EGX-listed) for Ostool Land Transport Company S.A.E., an Egyptian "
    "joint-stock company. On 3 JUNE 2026 a sale agreement was signed for 77,941,464 "
    "shares at EGP 8.224 per share, a total transaction value of EGP 641,000,000. THE "
    "TRANSFER COMPLETED ON 1 JULY 2026 to an Ascom subsidiary. Raya recognised a net "
    "profit of EGP 441,636,041 in its SEPARATE statements and EGP 450,508,721 in the "
    "CONSOLIDATED statements; the company explains the difference itself — the separate "
    "statements derecognise the investment at cost while the consolidated derecognition "
    "removes the sold minority interest within Ostool's net equity. Ascom's own board "
    "approved a fair-value study by Financial Advice Corporate Transactions (FACT) at EGP "
    "6.253 per share, so the EGP 8.224 paid is a 31.5% premium to the independent "
    "valuation; Raya's board approved a fair-value study by its own adviser Prime Capital "
    "after an FRA no-objection",
    "Raya Holding reviewed consolidated interim financial statements, six months ended 30 "
    "June 2026, note 1 'Group Background (continued)', printed page 9; completion and the "
    "FACT/Prime Capital fair-value studies reported by Arab Finance, EnterpriseAM, Zawya "
    "and Reuters via TradingView", CO, "2026-08-12",
    url="https://rayacorp.com/wp-content/uploads/2026/09/Raya-Holding-Cons.-30-Jun-2026-English.pdf",
    detail="THE SPECIFIC NAMED TRANSACTION WAS SEARCHED, NOT 'ESTIMATED'. Arithmetic "
           "check: 77,941,464 x 8.224 = 640,970,601 against a stated 641,000,000, so the "
           "printed per-share price is a rounding of 641,000,000 / 77,941,464 = 8.2241. "
           "The stake sold is 90% on the buyer's disclosure, the press and Raya's own "
           "subsidiary table, but Raya's narrative on the facing page of the same filing "
           "says 89% and describes the offer as being for 'a 100% stake' — the register "
           "records all three readings rather than choosing (see F29). WHY THIS IS A BASE "
           "CHANGER AND NOT A ONE-LINE FOOTNOTE: Ostool was EGP 2,506,577k of FY2025 "
           "revenue (3.93% of the group) and EGP 985mn of H1-2026 revenue, and it is GONE "
           "from 1 July 2026 — the group is eleven portfolio companies for H1-2026 and TEN "
           "thereafter. A forecast that rolls FY2025 or H1-2026 revenue forward without "
           "removing it overstates FY2027 revenue by about EGP 2bn. Separately, its "
           "disposal gain is 82.9% of Q2-2026 pre-tax profit.",
    model_impact="BASE CHANGER, modelled as an explicit dated event on BOTH legs and "
                 "dual-framed. (1) Land Transportation revenue, cost and profit stop on "
                 "30 June 2026: FY2026 carries six months of Ostool and FY2027 onward "
                 "carries none. (2) The EGP 450,508,721 consolidated gain is a Q2-2026 "
                 "one-off, stripped from the normalised earnings base and shown "
                 "separately in the FY2026 headline. (3) EGP 641m of cash comes in, and "
                 "its use — deleveraging against the EGP 24bn debt stack, or reinvestment "
                 "— is a stated assumption, not a residual.")

f_aman_sale = R.add(Ring.COMPANY, "ownership / stake changes (named-transaction rule)",
    FindingClass.B,
    "THE AMAN PARTIAL DISPOSAL THAT CREATED THE 76% STAKE. The FY2023 audited "
    "consolidated statement of financial position carries an equity line 'Net profit from "
    "selling Aman shares' of EGP 78,461,196 at 31 December 2023 which did not exist at 31 "
    "December 2022. From the FY2024 filing onward the same EGP 78,461,196 balance is "
    "captioned 'Finance Risk Reserve' (note 31), and it grew to EGP 115,325,358 at "
    "31-Dec-2025 and fell to EGP 93,591,140 at 30-Jun-2026. Aman's six operating entities "
    "have stood at 76% Raya ownership at every disclosed date since",
    "Raya Holding audited consolidated financial statements FY2023 (equity section) and "
    "FY2024, FY2025 and H1-2026 (note 31)", CO, "2024-03-01",
    url="https://rayacorp.com/wp-content/uploads/2024/09/Consolidated-FS-YE-2023-en.pdf",
    detail="THE RELABELLING IS RECORDED BECAUSE IT MATTERS: the same balance carries two "
           "different captions in consecutive filings, one describing a share sale and "
           "the other an FRA-mandated financing risk reserve under Egyptian Accounting "
           "Standard 47 and FRA Decision 47. A build that treats the FY2025 'Finance Risk "
           "Reserve' as distributable, or as the Aman sale proceeds, would be wrong on "
           "one of the two readings. THE OPEN QUESTION FOR THE BUILD: who the 24% Aman "
           "minority is, and on what terms, is NOT disclosed anywhere in the filings or "
           "the IR channel. Searched and not found (see N04).",
    model_impact="BASE CHANGER for the ownership chain. It is why the group's "
                 "fastest-growing and highest-margin leg — Aman, 33.6% of H1-2026 gross "
                 "profit at a 40.7% margin — reaches the parent at only 76%, and why "
                 "D20 computes minority interest entity by entity.")

f_own = R.add(Ring.COMPANY, "ownership / stake changes (named-transaction rule)",
    FindingClass.D,
    "SHAREHOLDER STRUCTURE AT 30 JUNE 2026, as published by the company: KHALIL FAMILY "
    "56.6%; NAIF AL-RAJHY 12.1%; ASHRAF KHEIRELDIN 10.6%; TAWEEL FAMILY 6.6%; FREE FLOAT "
    "14.1% (the five sum to exactly 100.0%). By geography: Egypt 80.2%, Saudi Arabia "
    "12.4%, other Arab 6.2%. Listed shares 4,281,297,768; share price EGP 7.68 at 30 June "
    "2026; market capitalisation EGP 32,880,366,858",
    "Raya Holding 2Q & 1H-2026 Earnings Release, shareholder structure and 'RAYA.CA on "
    "the EGX' pages", IR, "2026-08-12",
    url="https://rayacorp.com/wp-content/uploads/2026/09/Raya-Holding-Earning-Release-1H-2026-Final-EN.pdf",
    fiscal_period="Q2-2026",
    detail="TWO ARITHMETIC CHECKS, BOTH EXACT. (1) 4,281,297,768 shares x EGP 0.25 par = "
           "EGP 1,070,324,442, which is the audited issued and paid-up capital at both "
           "31-Dec-2025 and 30-Jun-2026 to the pound — so the share count is confirmed "
           "against the filing, not taken from a market page. (2) 4,281,297,768 x EGP "
           "7.68 = EGP 32,880,366,858, the printed market capitalisation, exactly. THE "
           "FREE FLOAT IS 14.1% AND FOUR HOLDERS OWN 85.9%; the Saudi holding (Naif "
           "Al-Rajhy 12.1%) is the largest single non-family stake. No 2026 change in any "
           "of the four blocks was found (N04).",
    model_impact="Fixes the share count for the per-share bridge and the free float for "
                 "the liquidity and control discussion. The 14.1% float is a stated fact "
                 "about the market in the shares, carried into the risk section; it is "
                 "never used to manufacture a discount.")

f_cap = R.add(Ring.COMPANY, "management & capital actions", FindingClass.D,
    "TREASURY BUYBACKS, ESOP AND DISTRIBUTIONS. Three successive board authorisations: "
    "27 May 2024 up to EGP 10,000,000 (4,933,999 shares bought for EGP 9,876,132 during "
    "2024); 14 April 2025 up to EGP 20,000,000; 5 March 2026 up to EGP 20,000,000, in "
    "each case to fund the company's reward and incentive scheme. Treasury balance: "
    "2,760,000 shares / EGP 4,883,071 at 30 June 2025 after allocating 2,173,000 shares "
    "to share-based compensation for EGP 4,993,061; 3,500,000 shares / EGP 9,978,744 at "
    "31 March 2026; 7,000,000 shares / EGP 28,360,356 at 30 June 2026. Separately the "
    "company executed an EGP 23.9m employee incentive share transfer. Periodic "
    "distributions of EGP 202,908,010 were charged to equity in FY2025 (nil in FY2024); "
    "dividends payable were EGP 71,896,736 at 31-Dec-2025 and EGP 11,572,600 at "
    "30-Jun-2026. Board at 1Q-2026: Medhat Khalil (Chairman), Ahmed Khalil (Executive "
    "Board Member and CEO), Seif Coutry, Amr El Tawil and Hamed Shamma (non-executive), "
    "Ahmed Elguindy (independent); CFO Hossam Hussein",
    "Raya Holding reviewed consolidated interim H1-2026, note 28 'Treasury Shares'; "
    "audited FY2025 statement of financial position; 1Q-2026 Investor Presentation, board "
    "page; Arab Finance report of the employee incentive share transfer", CO, "2026-08-12",
    url="https://rayacorp.com/wp-content/uploads/2026/09/Raya-Holding-Cons.-30-Jun-2026-English.pdf",
    detail="Treasury holdings doubled from 3,500,000 to 7,000,000 shares in a single "
           "quarter and the carrying value nearly TRIPLED (EGP 9,978,744 to EGP "
           "28,360,356) because the shares were bought at a much higher price — the stock "
           "closed EGP 5.08 on 31 March 2026 and EGP 7.68 on 30 June 2026. Even so "
           "treasury is only 0.16% of the 4,281,297,768 shares outstanding, so the "
           "dilution effect is immaterial and is stated as such rather than modelled.",
    is_fs_data=True, fiscal_period="Q2-2026",
    model_impact="Sets the share count and the treasury/ESOP adjustment in the equity "
                 "bridge (D26) and gives the FY2025 distribution of EGP 202,908,010 as "
                 "the only observed payout — which is 7.8% of FY2025 attributable profit "
                 "and EGP 0.047 per share. No payout ratio is extrapolated from one "
                 "observation; see N04 and D31.")

f_guid = R.add(Ring.COMPANY, "strategic plans & guidance", FindingClass.S,
    "MANAGEMENT'S OWN FORWARD STATEMENTS, ALL QUALITATIVE. On margins: 'profitability is "
    "expected to improve in 2H-2026, supported by a gradual recovery in margins, ongoing "
    "operational efficiency initiatives, and seasonally stronger performance across some "
    "of the Group's companies during the second half of the year.' On Raya IT: 'the "
    "company's current strong backlog and project pipeline are expected to contribute "
    "positively to the second half of the year', with the H1 decline attributed to "
    "regional geopolitical developments and a high prior-year base of large seasonal "
    "projects. NAMED EXPANSION COMMITMENTS: five of eleven portfolio companies entered "
    "Saudi Arabia in H1-2026; AMAN KSA received its initial SAMA licence for consumer "
    "lending and Aman was granted FRA approval to establish AMAN SUKUK; Raya Auto formed "
    "a joint venture with Samara Land Transportation Services Co. in Saudi Arabia for "
    "electric golf-cart assembly; Raya Electric holds a 1.5M-unit 2026 production "
    "capacity pipeline against 300k units today; Raya Smart Buildings has 2026 launches "
    "in New Cairo and the New Administrative Capital with Galleria40 occupancy at 99%",
    "Raya Holding 2Q & 1H-2026 Earnings Release, 12 August 2026; FY2025 and 1Q-2026 "
    "Investor Presentations", IR, "2026-08-12",
    url="https://rayacorp.com/wp-content/uploads/2026/09/Raya-Holding-Earning-Release-1H-2026-Final-EN.pdf",
    fiscal_period="Q2-2026",
    detail="THE BACKLOG IS ASSERTED AND NOT QUANTIFIED. Raya IT is described as having a "
           "'strong backlog and project pipeline' and no figure, composition, duration or "
           "conversion rate is given anywhere in the release, the presentations, the fact "
           "sheets or the statements. That is the single most valuable operating anchor "
           "this issuer does not publish, and it is recorded as a gap rather than "
           "estimated (N02).",
    model_impact="Sets the SHAPE of the 2H-2026 margin path — a recovery, on the "
                 "company's own statement, but with no number attached, so the size of "
                 "the recovery is set by the memory-cost path (F02) and sensitised, not "
                 "taken from guidance. The named KSA and capacity commitments set the "
                 "expansion capex assumption in D19b and the Raya Electric volume ramp in "
                 "D10.")

f_mkt = R.add(Ring.COMPANY, "regular disclosures", FindingClass.C,
    "THE LISTING AND THE PRICE SERIES THAT EXIST — RECORDED, WITH NO BETA RESOLVED, PER "
    "INSTRUCTION. Raya Holding trades on ONE exchange: the Egyptian Exchange, ticker "
    "RAYA.CA, in Egyptian pounds, listed since 2005. 4,281,297,768 ordinary shares of EGP "
    "0.25 par. Company-published prices: EGP 5.08 at 31 March 2026 (market cap EGP "
    "21,748mn / USD 398.4mn; 52-week high 5.83, low 2.26) and EGP 7.68 at 30 June 2026 "
    "(market cap EGP 32,880,366,858). The repository holds "
    "engine/raw_ohlc/EG/RAYA.csv — 3,700 rows, 02-Jan-2011 to 23-Aug-2026, last close "
    "EGP 7.07 — and engine/raw_indices/EG/EGX30.csv — 3,869 rows, to 08-Sep-2026, last "
    "56,174.30",
    "Raya Holding 1Q-2026 Investor Presentation and 2Q & 1H-2026 Earnings Release; "
    "repository price and index series", PMD, "2026-08-23",
    detail="THREE THINGS A LATER BUILD MUST NOT GET WRONG. (1) NO DUAL LISTING. Searched "
           "for a depositary receipt, a GDR, a second line or a foreign listing and found "
           "none (N07); every Raya document says 'EGX: RAYA.CA' and nothing else. This is "
           "NOT the Orascom Construction case and the register says so, so a later build "
           "does not go hunting for a second regressor. (2) CURRENCY AND MAGNITUDE AGREE: "
           "the repo series' last close of EGP 7.07 sits between the company's own EGP "
           "5.08 (31-Mar) and EGP 7.68 (30-Jun) marks in the right order of magnitude for "
           "an EGP-denominated EGX line; the series is not a USD or a rebased series. (3) "
           "THE PRICE SERIES IS 17 CALENDAR DAYS STALE against the index. RAYA.csv ends "
           "23-Aug-2026 while EGX30.csv runs to 08-Sep-2026. IT MUST BE REFRESHED BEFORE "
           "ANY REGRESSION RUNS, and the regression must go through "
           "beta_regression.own_stock_beta('RAYA','EG','EGX') against "
           "engine/raw_indices/EG/EGX30.csv — never a constituent composite. NO BETA WAS "
           "RESOLVED IN THIS SWEEP. The 2011 opening prints of EGP 0.09-0.10 are a "
           "split/par-adjusted history and the adjustment basis has NOT been verified "
           "here; verify it before using the pre-2016 window in any regression.")

# ---------------------------------------------- NEGATIVE SEARCHES: silence closes nothing
n_seg = R.add_negative(Ring.COMPANY, "regular disclosures",
    "read every page of the FY2025 audited filing (49pp) and the H1-2026 reviewed interim "
    "(44pp) looking for, per segment: non-controlling interest, headcount or employee "
    "numbers, capital expenditure, units sold, unit prices, utilisation, intersegment "
    "revenue, and revenue by geography. Note 29 carries revenue, cost, depreciation, "
    "profit, total assets and total liabilities AND NOTHING ELSE; there is no capex line "
    "anywhere in the group cash-flow statement's segment disclosure and no employee-cost "
    "line outside the single consolidated 'salaries and wages' figure in note 25. The "
    "eliminations column is a single number per row and is never decomposed",
    SWEEP_DATE)

n_guid = R.add_negative(Ring.COMPANY, "strategic plans & guidance",
    "searched the FY2025 and 1H-2026 earnings releases, the FY2025 and 1Q-2026 investor "
    "presentations, the FY2025/1Q-2026/1H-2026 fact sheets and the 2024 annual report for: "
    "numeric FY2026 or medium-term revenue, EBITDA or margin guidance; a capital-"
    "expenditure plan or budget; a quantified Raya IT backlog, its composition, duration "
    "or conversion; and a target for any of the eleven portfolio companies. NOT ONE "
    "NUMERIC FORWARD FIGURE IS PUBLISHED. The only forward statements are qualitative "
    "(F39) and the only quantified forward item found is Raya Electric's 1.5M-unit 2026 "
    "capacity pipeline, which is a capacity target and not a volume forecast",
    SWEEP_DATE)

n_price = R.add_negative(Ring.INDUSTRY, "pricing",
    "searched every company document for a realised unit price for any Raya business: "
    "average selling price per handset or per device, revenue per seat or per agent-hour "
    "for RCX, revenue per branch or yield on portfolio for Aman, revenue per square metre "
    "for Raya Smart Buildings, price per tonne for Raya Foods, price per unit for Raya "
    "Electric or Raya Auto. NONE IS PUBLISHED. The IR channel gives capacities and mix "
    "percentages but never a price; the statements give revenue by type but never a "
    "quantity. Every price leg in the driver table below is therefore SOLVED from "
    "disclosed revenue divided by a disclosed capacity, and is labelled as derived",
    SWEEP_DATE)

n_own = R.add_negative(Ring.COMPANY, "ownership / stake changes (named-transaction rule)",
    "searched for the identity and terms of the 24% Aman minority and the 39.87% Raya "
    "Contact Centre minority by name; for any 2026 change in the four disclosed blocks "
    "(Khalil Family 56.6%, Naif Al-Rajhy 12.1%, Ashraf KheirEldin 10.6%, Taweel Family "
    "6.6%); for a mandatory tender offer, a block trade or a stake-building disclosure in "
    "RAYA; and for the date and price at which Naif Al-Rajhy acquired his 12.1%. NOTHING "
    "FOUND in the filings, the IR channel or named press. The minorities in the two "
    "largest partially-owned legs are unidentified in the public record, which is a real "
    "gap for a holding company whose minority takes 30% of equity",
    SWEEP_DATE)

n_div = R.add_negative(Ring.COMPANY, "management & capital actions",
    "searched the company's own /dividends-overview/ page (returns HTTP 200 with an "
    "empty client-rendered body), the FY2025 and 1H-2026 releases, the presentations and "
    "the annual report for a stated dividend policy, a payout-ratio target, a dividend "
    "per share, or an ordinary general assembly profit-distribution resolution. NONE "
    "FOUND. The only observable distribution is the EGP 202,908,010 charged to equity in "
    "FY2025 (nil in FY2024, nil in the FY2023 and FY2022 equity statements). ONE "
    "OBSERVATION IS NOT A POLICY and no payout ratio is extrapolated from it",
    SWEEP_DATE)

n_hedge = R.add_negative(Ring.GLOBAL, "commodity complex (input/output)",
    "searched the FY2025 audited filing and the H1-2026 interim for a commodity note, a "
    "hedging policy, a derivative instrument, a forward purchase commitment, or any "
    "quantification of exposure to memory, semiconductor, steel, resin or agricultural "
    "input prices. Note 33 'Financial Risk Management Objectives and Policies' covers "
    "foreign-currency, credit, interest-rate and liquidity risk and NOT commodity risk; "
    "no derivative or hedge is disclosed anywhere. The group's input-price exposure is "
    "therefore unhedged so far as the record shows, and is carried in the model as a "
    "direct pass-through with a lag rather than as a hedged cost",
    SWEEP_DATE)

n_list = R.add_negative(Ring.COMPANY, "regular disclosures",
    "searched for a second listing, a global or American depositary receipt, a London or "
    "Gulf line, or any non-EGX quotation for Raya Holding, and for any statement in the "
    "company's own documents referring to more than one exchange. NONE EXISTS: every "
    "company document says 'EGX: RAYA.CA' and the 1H-2026 release states 'Publicly listed "
    "on the Egyptian Exchange (EGX) since 2005'. Recorded as a dated negative so a later "
    "build does not repeat the search or assume a dual-listing trap that is not there",
    SWEEP_DATE)

R.declare_study_year("2026", ["Q1-2026", "Q2-2026"])

# ============================================================ DRIVER GATE TABLE
# Built at the FINEST SOURCED LEVEL. The segment note discloses cost per segment, so
# every segment margin is an OUTPUT. Where the disclosure stops short of volume x
# price the row says so and names the negative search that proves the absence.
R.add_driver("Group revenue — the SUM of eleven portfolio-company lines, never a group rate",
    DriverMode.BOTTOM_UP,
    "The audited segment note gives revenue for fourteen sectors that map one-for-one "
    "onto the eleven portfolio companies and reconcile to the pound (F26, F27). The "
    "group line is therefore an output of eleven separate builds. A single group growth "
    "rate would have to average a business growing 51.9% (Raya Trade, H1-2026) with one "
    "shrinking 22.7% (Ostool) and one shrinking 19.4% (Raya Foods) in the same half.",
    [f_seg, f_seg2, f_ir_h1, f_fs25])
R.add_driver("Raya Trade revenue — volume and price projected separately by product line",
    DriverMode.BOTTOM_UP,
    "The company discloses the FY2025 and 1Q-2026 revenue mix by product line (mobile "
    "distribution and retail 52.9%, consumer electronics and Mazaya 16.2%, Nigeria 20.8%, "
    "EZEE, other) and the network it sells through (8,500+ dealers, 65+ retail outlets, "
    "48 service centres). Volume is set off the IDC/Gartner unit path (-16.7% to -8.4% "
    "global units in 2026) and price off the +27.6% ASP path, with the 38.5% Egyptian "
    "traveller tariff and fifteen locally manufacturing brands moving the two in opposite "
    "directions. FLAGGED GAP: no unit price or unit volume is published for Raya Trade "
    "itself (N03), so the realised price is SOLVED from disclosed segment revenue and is "
    "labelled derived.",
    [f_ir_kpi, f_seg, f_ntra, f_hand])
R.add_driver("Raya Trade gross margin — OUTPUT of the volume/price/tariff build",
    DriverMode.BOTTOM_UP,
    "MARGIN IS NEVER AN INPUT HERE. The segment note discloses Trade and distribution "
    "cost of EGP 21,524,518k against revenue of 23,823,293k, so the FY2025 margin of "
    "9.65% is computed, not assumed; the release's own 9.6% confirms it. The forecast "
    "margin falls out of the cost build (D16) and is checked against the disclosed path "
    "10.4% (FY2024) to 9.6% (FY2025).",
    [f_seg, f_type, f_mem])
R.add_driver("Raya Information Technology revenue — by value chain, against a named pipeline",
    DriverMode.BOTTOM_UP,
    "RIT = the 'Information technology' segment PLUS the 'International services' segment, "
    "and the two sum to the reported EGP 18,410mn exactly (F27). Built from the disclosed "
    "value-chain mix (Raya Integration 70-74%, Raya Network Services 19% up from 8%, RIS, "
    "RDC, Raya JaFza), the 60% ATM market share, the 5-year tech refresh cycle and the "
    "1,000+ enterprise customer base, against the external data-centre pipeline (18.97% "
    "market CAGR, 1 GW MoU, nine facilities in development). FLAGGED GAP: the backlog "
    "management calls 'strong' is never quantified (N02), so the 2H-2026 recovery is "
    "sized off the disclosed vertical mix and sensitised rather than taken from guidance.",
    [f_seg2, f_ir_kpi, f_dc, f_seg])
R.add_driver("Aman revenue — gross transaction value x take rate, plus portfolio x spread",
    DriverMode.BOTTOM_UP,
    "Aman discloses BOTH quantities: gross transaction value (EGP 103,859mn FY2025, "
    "+47.6%; EGP 67.6bn H1-2026, +54%) and the portfolio (EGP 9.7bn total, 6.7bn active "
    "issuances, 3.0bn matured), together with the net revenue mix (financial spread 38.8%, "
    "digital consumer goods 31.3%, acquisition and transaction fees 29.9%) and 250+ "
    "branches across 23 governorates. Revenue is built as GTV times a take rate solved "
    "from disclosed revenue, plus portfolio times spread, and bounded by the external "
    "market series (Egyptian consumer finance EGP 71.839bn in H1-2026, +88.5%) — against "
    "which Aman is LOSING share, which the build must reproduce rather than assume away.",
    [f_ir_kpi, f_ir_h1, f_cfin, f_seg])
R.add_driver("Aman regulatory capital ceiling — the constraint that caps the portfolio",
    DriverMode.BOTTOM_UP,
    "FRA Decision 137/2025 sets a minimum 12% capital-adequacy ratio against "
    "risk-weighted assets and caps qualifying borrowings at nine times the capital base; "
    "cash lending is capped at EGP 50,000 per loan and 20% of the portfolio. The model "
    "SOLVES for the next capital injection at the modelled portfolio growth rather than "
    "letting the portfolio compound freely, and deducts the 24% minority share of any "
    "injection from the parent's cash.",
    [f_fra, f_subs, f_seg])
R.add_driver("RCX revenue — seats x utilisation x revenue per seat, split offshore/onshore",
    DriverMode.BOTTOM_UP,
    "The company publishes 9.2k seat capacity at 81% utilisation with 7,000+ agents in 6 "
    "countries and 15 languages, and splits revenue offshore 68.9% (predominantly USD) "
    "against onshore 31.1%, and Egypt 79.2% / Gulf 19.5% / Europe 1.3%. Revenue per "
    "occupied seat is solved from disclosed segment revenue and the two legs are grown "
    "separately because one is a dollar export and the other an Egyptian-pound service. "
    "Named competitor capacity (Teleperformance 4,000+, Sutherland 2,500+, Concentrix "
    "1,800, Majorel 1,400) bounds the share.",
    [f_ir_kpi, f_comp, f_seg, f_ir_h1])
R.add_driver("RCX margin and the AI-substitution branch", DriverMode.BOTTOM_UP,
    "The base holds the disclosed gross-margin path (44.9% FY2025 on the release, 42.5% "
    "H1-2026) computed off the segment note's own cost line, with the note-versus-release "
    "62,201k gross-profit break resolved first (F27). The bear branch prices seat-price "
    "deflation consistent with Gartner's USD 80bn 2026 call-centre cost-out, applied to "
    "the 13.4% of H1-2026 group EBITDA RCX contributes, and is bounded above by Gartner's "
    "own 14%-fully-automated-by-2027 ceiling. Modelled as an explicit sensitivity, never "
    "as a haircut hidden inside the margin.",
    [f_seg, f_ai, f_ir_h1])
R.add_driver("Raya Foods revenue — capacity, crop mix and export destination",
    DriverMode.BOTTOM_UP,
    "Built off 35k of disclosed production capacity, a 20k sqm plant, strawberry at "
    "90-96.4% of sales, 95% of revenue in foreign currency and destinations USA and "
    "Europe 78% / China 11%. THIS IS THE GROUP'S WORST LEG AND THE BUILD MUST REPRODUCE "
    "IT: H1-2026 revenue -19.4% and gross profit -66.9% to EGP 139mn from 419mn, with a "
    "EGP 177mn net loss already in Q1-2026. A group-level growth rate would bury that.",
    [f_ir_kpi, f_ir_q1, f_seg])
R.add_driver("Raya Electric revenue — units against a stated capacity ramp",
    DriverMode.BOTTOM_UP,
    "300k units of annual production capacity today against a stated 1.5M-unit 2026 "
    "pipeline, on OEM/ODM contracts with LG, Carrier, De'Longhi and Elaraby. Revenue is "
    "capacity times utilisation times a price solved from FY2025 segment revenue of EGP "
    "885,339k. The margin is the group's thinnest at 7.86% and is an output of the "
    "materials cost line, not an assumption.",
    [f_ir_kpi, f_guid, f_seg])
R.add_driver("Raya Smart Buildings revenue — GLA x occupancy x rent",
    DriverMode.BOTTOM_UP,
    "43k sqm of gross leasable area out of 70k sqm built-up, at 99% occupancy, plus about "
    "7k sqm of named 2026 launches (Sheikh Zayed 2.76k, New Administrative Capital 1.8k, "
    "KOV Mall New Cairo 950, Bank Misr Innovation Hub 1.4k). Rent per sqm is solved from "
    "the disclosed 'Finance lease' segment revenue of EGP 256,489k. At a 59.47% gross "
    "margin this is the group's highest-margin leg and cannot be blended with anything.",
    [f_ir_kpi, f_seg, f_guid])
R.add_driver("Raya FMCG revenue — points of sale x throughput, food and non-food separately",
    DriverMode.BOTTOM_UP,
    "70,000+ points of sale across 14 governorates with a disclosed food 66% / non-food "
    "34% split; revenue per point of sale is solved from the 'Manufacturing and export' "
    "segment revenue of EGP 2,264,169k. The two product legs carry different margins and "
    "are grown separately.",
    [f_ir_kpi, f_seg])
R.add_driver("Raya Auto revenue — electric vehicles and aftermarket, separately",
    DriverMode.BOTTOM_UP,
    "EV was 76% of FY2025 revenue with XPENG unit volumes doubling year-on-year in "
    "H1-2026; commercial vehicles, aftermarket, motorcycles and three-wheelers are the "
    "remainder. Revenue is built on the disclosed EV share against the named model ramp "
    "and the Saudi golf-cart joint venture, with price solved from the 'Vehicles "
    "Manufacturing' segment revenue of EGP 1,791,411k.",
    [f_ir_kpi, f_ir_h1, f_seg])
R.add_driver("Raya Restaurants revenue — outlets x covers", DriverMode.BOTTOM_UP,
    "13 outlets serving 500k customers, Ovio 94.9% and The Lebanese Bakery 3.2%, with two "
    "new Ovio branches opened in FY2025. Revenue per outlet is solved from the "
    "'Restaurants' segment revenue of EGP 292,710k. It is 0.4% of group revenue and is "
    "modelled at that weight, not ignored and not given a page.",
    [f_ir_kpi, f_seg])
R.add_driver("Ostool — REMOVED from 1 July 2026, and the gain framed separately",
    DriverMode.BOTTOM_UP,
    "The Land Transportation segment carries six months of FY2026 and nothing thereafter: "
    "the 90% stake transferred to an ASEC Mining subsidiary on 1 July 2026 for EGP "
    "641,000,000. FY2025 revenue of EGP 2,506,577k and H1-2026 revenue of EGP 985mn drop "
    "out. The EGP 450,508,721 consolidated disposal gain is a dated Q2-2026 one-off, "
    "stripped from normalised earnings and shown separately in the FY2026 headline, with "
    "the use of the EGP 641m proceeds stated as an assumption rather than left as a "
    "residual.",
    [f_ostool, f_q2, f_seg])
R.add_driver("Cost of revenues — projected BY NATURE, eight lines with eight escalators",
    DriverMode.BOTTOM_UP,
    "Note 25 splits the H1-2026 cost of EGP 27,317,409,179 into devices and goods "
    "distribution cost 15,729,838,558 (57.6%), supplies and installations 6,888,412,846, "
    "materials used in production 2,193,696,187, salaries and wages 1,392,515,437, "
    "transportation service cost 862,258,221, depreciation 211,666,739, finance cost "
    "27,421,281 and other direct cost 11,599,910. Each is escalated on its own driver — "
    "imported components on the memory-cost path, wages on the CBE inflation path, "
    "depreciation off the fixed-asset roll — instead of one COGS-to-revenue ratio. This "
    "is the row that lets the model see a margin break coming.",
    [f_type, f_fs25, f_mem])
R.add_driver("Group gross margin — an OUTPUT, checked against the quarterly path",
    DriverMode.BOTTOM_UP,
    "SETTING A GROUP GROSS MARGIN AS AN INPUT WOULD BE A QC FAIL ON THIS NAME, because "
    "the filings disclose cost per segment and cost by nature and therefore permit a "
    "built margin. The output is checked against the disclosed sequence: 19.95% (FY2022), "
    "20.38% (FY2023), 20.88% (FY2024), 21.45% (FY2025), 20.87% (Q1-2025), 22.26% "
    "(Q2-2025), 22.2% (Q4-2025), 21.85% (Q1-2026), 16.77% (Q2-2026). A model that cannot "
    "reproduce the Q2-2026 break from its own cost lines is rejected.",
    [f_q1, f_q2, f_fs25, f_type])
R.add_driver("Depreciation — per segment, from the note that discloses it",
    DriverMode.BOTTOM_UP,
    "Note 29 gives depreciation for the year BY SEGMENT (FY2025 total EGP 957,165k; "
    "H1-2026 total 485,475k, which foots exactly across the fourteen sectors). It is "
    "therefore rolled forward per segment against each segment's own asset base rather "
    "than as a group percentage of revenue or of gross fixed assets.",
    [f_seg, f_fs25])
R.add_driver("Capital expenditure", DriverMode.TOP_DOWN,
    "THE FLOOR OF LAST RESORT, AND THE ABSENCE IS EVIDENCED. The negative search records "
    "that no capital-expenditure figure, plan, budget or guidance is published anywhere — "
    "not per segment in note 29, not in the group cash-flow disclosure, not in any "
    "earnings release, presentation, fact sheet or the annual report. Capex is set as a "
    "percentage of revenue, differentiated between the asset-light legs (Trade, RCX, "
    "Aman) and the asset-heavy ones (Electric, Foods, Smart Buildings), anchored on the "
    "disclosed per-segment depreciation as a proxy for maintenance need, and sensitised. "
    "The named expansion commitments — Raya Electric's 1.5M-unit pipeline, Smart "
    "Buildings' 2026 launches, the Saudi entries — are added on top as explicit items.",
    [n_guid, f_guid, f_seg])
R.add_driver("General and administrative plus selling and marketing expense",
    DriverMode.TOP_DOWN,
    "The negative search records that G&A and selling and marketing are NOT split by "
    "segment, by nature, or into fixed and variable anywhere in the disclosure — only two "
    "consolidated lines (H1-2026: EGP 2,685,310,171 and 1,368,872,899). They are "
    "therefore escalated top-down: G&A on the CBE inflation path, selling and marketing "
    "on modelled revenue with a separate translation effect on the Gulf, Nigerian, Polish "
    "and Bahraini cost bases. THE SHORTFALL IS NAMED RATHER THAN HIDDEN: a 21.6% revenue "
    "increase came with a 22.8% G&A increase and a 26.0% selling-and-marketing increase "
    "in H1-2026, and the model cannot say which of the eleven businesses caused it.",
    [n_seg, f_q2, f_cbe2])
R.add_driver("Non-controlling interest — computed subsidiary by subsidiary, and FLAGGED",
    DriverMode.BOTTOM_UP,
    "NOT A RATIO OF GROUP PROFIT. Each leg's forecast profit is taken to the group share "
    "at its OWN named percentage from note 1: Raya Contact Centre 60.13%, the six Aman "
    "entities 76%, Aman Taqa 39%, Gulf customer experience 85%, Raya Restaurants "
    "95.423%, everything else 100%. THE REASON IS ARITHMETIC: NCI took 17.16% of FY2022 "
    "profit, 21.73% of FY2023, 11.09% of FY2024, 11.78% of FY2025 and 16.22% of H1-2026 "
    "while holding 25.1%, 29.1%, 21.4%, 30.3% and 30.2% of equity — no blended ratio "
    "reproduces two consecutive years. FLAGGED GAP, AND IT IS REAL: the segment note "
    "gives NO NCI per segment (N01), so the map from segment profit to entity profit has "
    "to be built from the subsidiary list and reconciled to the disclosed NCI totals, and "
    "the residual after that reconciliation is stated rather than allocated.",
    [f_subs, f_bs25, f_q2, n_seg])
R.add_driver("Intersegment eliminations and unallocated holding-company cost",
    DriverMode.TOP_DOWN,
    "The eliminations column is large and NEVER decomposed: FY2025 revenue (997,232)k, "
    "profit (1,449,703)k, total assets (19,170,538)k, total liabilities +10,843,089k. The "
    "profit column absorbs intersegment profit AND non-controlling interest AND "
    "holding-level cost in one number, which is why the fourteen segments sum to the "
    "ATTRIBUTABLE profit rather than the group's. The negative search records that no "
    "split is published. It is therefore modelled top-down as a constant proportion of "
    "segment profit, calibrated to FY2022-FY2025 and H1-2026, and it is the single "
    "largest unexplained line in the build — stated as such in the study, not smoothed.",
    [n_seg, f_seg, f_bs25])
R.add_driver("Effective tax rate — computed, never the statutory 22.5%",
    DriverMode.BOTTOM_UP,
    "Raya's own effective rate was 32.85% (FY2022), 39.34% (FY2023), 30.13% (FY2024), "
    "28.87% (FY2025), 35.90% (Q1-2026) and 29.45% (H1-2026). Egypt's 22.5% statutory rate "
    "would mis-state every one of those six periods by between 6.4 and 16.8 percentage "
    "points, because note 32 states the tax is computed for each subsidiary INDIVIDUALLY "
    "and some subsidiaries are exempt under law 8 of 1997. The rate is built off the "
    "disclosed current/deferred split in note 26 and the per-entity structure, and "
    "converges toward statutory only if the mix is argued to.",
    [f_fs25, f_fs24, f_fs23, f_fs22, f_q1, f_q2, f_tax])
R.add_driver("Interest expense and the cost of debt", DriverMode.BOTTOM_UP,
    "Built from the disclosed stack at 30 June 2026 — credit facilities 14,441,685,606, "
    "long-term loans and finance lease 4,458,945,749, long-term bank overdraft "
    "2,231,020,835, short-term loans 1,712,420,323, current portion of long-term "
    "1,074,406,189, lease liabilities 1,591,337,315, notes payable 87,077,233 — against "
    "the CBE corridor of 19.00/20.00/19.50 held on 20 August 2026. The implied borrowing "
    "rate is SOLVED from the disclosed H1-2026 finance cost of EGP 1,060,289,247 on the "
    "average balance and tested against the corridor, rather than assumed as a spread.",
    [f_debt, f_q2, f_cbe1, f_cbe2])
R.add_driver("Working capital — receivables, payables and the credit-loss charge",
    DriverMode.BOTTOM_UP,
    "Accounts and notes receivable EGP 26,048,147,187 and accounts and notes payable "
    "13,555,107,022 at 30 June 2026, against 21,553,121,145 and 11,816,115,113 at 31 "
    "December 2025. THE CREDIT-LOSS CHARGE IS THE ONE TO WATCH: expected credit losses "
    "were EGP 404,958,565 for the whole of FY2025 and EGP 549,676,614 in H1-2026 alone — "
    "already 36% above a full prior year in six months. Modelled off the receivable book "
    "by ageing where disclosed, and the step-up is carried explicitly rather than "
    "averaged.",
    [f_q2, f_bs25, f_fs25])
R.add_driver("Foreign-currency translation and the export legs", DriverMode.BOTTOM_UP,
    "Note 24-B splits revenue into local EGP 24,658,434,522 and foreign 9,129,541,932 "
    "(27.0%) for H1-2026. The legs move on opposite signs: Raya Foods earns 95% of its "
    "revenue in foreign currency and RCX 68.9% offshore in USD, so a strengthening pound "
    "is a headwind there, while the imported-device cost base is a dollar cost and a "
    "tailwind. The EGP path is taken from the house macro ladder, derived from Egypt's "
    "own inflation path against long-run US inflation by relative purchasing-power "
    "parity, never set by hand.",
    [f_type, f_ir_h1, f_fx])
R.add_driver("Terminal risk-free rate", DriverMode.BOTTOM_UP,
    "Norm-built from the Central Bank of Egypt's OWN published medium-term target of 7% "
    "(+/-2pp) plus the house emerging-market real-rate convention, never averaged from "
    "history and never backed out of a price. The explicit window uses the corridor level "
    "held on 20 August 2026.",
    [f_cbe2, f_cbe1])
R.add_driver("Beta regressor and share count — NOT RESOLVED IN THIS SWEEP, per instruction",
    DriverMode.BOTTOM_UP,
    "RECORDED, NOT COMPUTED. Single listing: EGX, RAYA.CA, EGP, since 2005; no depositary "
    "receipt or second line exists (N07), so there is no dual-listing ambiguity of the "
    "Orascom Construction kind. Share count 4,281,297,768, confirmed against the audited "
    "issued and paid-up capital of EGP 1,070,324,442 at EGP 0.25 par, exactly. When the "
    "beta is resolved it must go through beta_regression.own_stock_beta('RAYA','EG','EGX') "
    "against engine/raw_indices/EG/EGX30.csv and NEVER a constituent composite — and "
    "engine/raw_ohlc/EG/RAYA.csv must be refreshed first: it ends 23-Aug-2026 against an "
    "index that runs to 08-Sep-2026. The pre-2016 prints of EGP 0.09-0.10 are "
    "split/par-adjusted on an unverified basis; verify before using that window.",
    [f_mkt, f_own, f_bs25, n_list])
R.add_driver("Share count, treasury and ESOP dilution", DriverMode.BOTTOM_UP,
    "4,281,297,768 shares; treasury 7,000,000 shares carried at EGP 28,360,356 at 30 June "
    "2026, 0.16% of the register and immaterial, stated rather than modelled; three "
    "successive buyback authorisations (EGP 10m May-2024, EGP 20m April-2025, EGP 20m "
    "March-2026) all earmarked for the reward and incentive scheme, plus an EGP 23.9m "
    "employee incentive share transfer.",
    [f_cap, f_own, f_bs25])
R.add_driver("Dividend capacity", DriverMode.TOP_DOWN,
    "The negative search records that NO dividend policy, payout target or per-share "
    "figure is published; the company's own dividends page returns an empty body. The "
    "single observation is EGP 202,908,010 charged to equity in FY2025 — 7.84% of "
    "attributable profit, EGP 0.047 per share — against nil in FY2024, FY2023 and "
    "FY2022. ONE OBSERVATION IS NOT A POLICY. Capacity is therefore built top-down from "
    "what each leg can legally upstream: Aman bounded by the FRA's 12% capital-adequacy "
    "floor and the nine-times borrowing cap, the rest by working capital, with the 24% "
    "and 39.87% minorities taking their share before the parent does.",
    [n_div, f_cap, f_fra])
R.add_driver("Off-balance-sheet guarantees", DriverMode.BOTTOM_UP,
    "Letters of guarantee issued by the subsidiaries' banks in favour of third parties "
    "stood at EGP 8,785,257,276 at 30 June 2026, of which EGP 8,517,981,983 UNCOVERED — "
    "up 13.9% in six months and larger than the group's entire equity before "
    "non-controlling interest. Carried as a named, dated exposure in the risk section and "
    "in the downside branch of the equity bridge; not netted, not ignored.",
    [f_debt, f_q2])
R.add_driver("Group EBITDA — an output, on ONE stated definition", DriverMode.BOTTOM_UP,
    "The company's published EBITDA (gross profit less G&A, selling and marketing and "
    "board remuneration, before all depreciation, expected credit losses, provisions and "
    "goodwill impairment) is NOT the audited 'OPERATING PROFITS' line: they agree for "
    "H1-2026 (EGP 1,821mn) but not for FY2025 (release 6,329 against audited 6,340, the "
    "goodwill impairment sitting on different sides of the line). The study states which "
    "definition it uses and reconciles the other to it; it never mixes the two across "
    "periods.",
    [f_ir_h1, f_fs25, f_ir_kpi])

# ------------------------------------------------------------------------ OUTPUT
errors, warnings = R.validate()
R.to_json(os.path.join(HERE, 'sweep_register.json'))
print(R.qc_line())
print(f"\nfindings: {len(R.findings)} | drivers: {len(R.drivers)}")
c = R.counts()
print(f"  by class: B={c['B']} S={c['S']} D={c['D']} C={c['C']} NEG={c['NEG']}")
nbu = sum(1 for d in R.drivers if d.mode is DriverMode.BOTTOM_UP)
print(f"  driver modes: {nbu} bottom-up / {len(R.drivers) - nbu} top-down")
src = {}
for f in R.findings:
    src[f.source_type.value] = src.get(f.source_type.value, 0) + 1
print("  by source type: " + ", ".join(f"{k}={v}" for k, v in sorted(src.items())))
print(f"  primary access attempts: {len(R.primary_access)} "
      f"({sum(1 for p in R.primary_access if p.reachable)} reachable / "
      f"{sum(1 for p in R.primary_access if not p.reachable)} blocked)")
print(f"  study year {R.study_year}: quarters declared {R.study_quarters_disclosed}")

# ring closure, category by category, so the reader sees the population not a verdict
print("\nRING CLOSURE (mandatory categories, each closed by a dated finding or a dated"
      " negative search):")
for ring in RINGS[AssetClass.STOCK]:
    for cat in MANDATORY[ring]:
        hits = [f for f in R.findings if f.ring is ring and f.category == cat]
        kinds = "+".join(sorted({f.klass.name for f in hits}))
        print(f"  {ring.value:<9} {cat:<58} {len(hits)} finding(s) [{kinds}]")

if errors:
    print(f"\nVALIDATOR ERRORS ({len(errors)}) — disclosed verbatim, not suppressed:")
    for e in errors:
        print(f"  ! {e}")
else:
    print("\nVALIDATOR ERRORS: none")
if warnings:
    print(f"\nVALIDATOR WARNINGS ({len(warnings)}) — verbatim:")
    for w in warnings:
        print(f"  - {w}")
else:
    print("\nVALIDATOR WARNINGS: none")

fr = R.check_freshness(SWEEP_DATE)
print(f"\nfreshness vs intended delivery {SWEEP_DATE}: "
      f"{fr or 'OK — sweep and intended delivery the same day, 0 days elapsed'}")
print("NOTE: the Company ring must be re-run if delivery slips past 2026-09-23 "
      "(14 calendar days), and engine/raw_ohlc/EG/RAYA.csv must be refreshed before "
      "any regression regardless — it ends 23-Aug-2026 against an EGX30 series that "
      "runs to 08-Sep-2026.")
