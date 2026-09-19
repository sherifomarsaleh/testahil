"""ISPH (Ibnsina Pharma, EGX: ISPH.CA) — Step 2A four-ring Information Sweep register.

FIRST-BUILD study. Held under `_pending` until it carries a valuation.
Runs BEFORE any forecast driver is set. Every mandatory category of every ring is
closed by a dated finding or a dated negative search.

WHAT THIS COMPANY IS, because it decides the driver set. Ibn Sina Pharma is a
pharmaceutical DISTRIBUTOR, not a manufacturer. It buys finished packs at an
administered price and resells them at an administered price; the spread between
the two is set by decree, not by the company. Its economics are therefore volume
through a network at a thin regulated spread, financed on short-term bank credit.
FY2025 gross margin was 8.42% and net margin 1.24%; the company's own FY2025 cash
flow statement shows operating cash flow of NEGATIVE EGP 71.1mn after EGP 2,271mn
of finance cost paid, on EGP 952mn of net profit. The cash conversion cycle is the
business, and the interest on it is the second-largest cost line after the goods.

PRIMARY-SOURCE ACCESS, RECORDED RATHER THAN HIDDEN.
  * The corporate site https://ibnsina-pharma.com/ is behind Cloudflare and
    returns HTTP 403 "Sorry, you have been blocked" to this environment, both by
    scripted request and by the rendering fetch tool. It was tried FIRST and the
    refusal is logged.
  * The dedicated investor-relations sub-domain https://ir.ibnsina-pharma.com/ IS
    reachable and is the build source for every historical figure in this register:
    the Results Center carries audited consolidated statements for FY2015-FY2025
    and reviewed interims through 2Q2026, and the Presentations page carries the
    earnings-call decks. Nothing in the Company ring rests on an aggregator.
  * The Central Bank of Egypt's home page is reachable and was read live on the
    sweep date; its CPI statistics sub-page resets the connection. The Egyptian
    Drug Authority's site is reachable and its track-and-trace notice was read
    from the regulator itself.
  * One press source used in the Country ring (MadaMasr, 21-Sep-2025, on the
    Unified Procurement Authority's arrears) returned HTTP 403 to the fetch tool;
    that finding rests on the search engine's extract of the article and SAYS SO
    in its own detail field rather than pretending to a full read.

ARITHMETIC IS THE ARBITER, AND HERE IT HAD TO BE. Every primary statement page in
this issuer's filings — statement of financial position, profit or loss, changes in
equity, cash flow — is a SCANNED IMAGE with no text layer; only the notes carry
extractable text. Every one of those pages was therefore rendered to pixels at
150-170 dpi and read off the rendered image, and every column was then re-added
against its own printed subtotals. The route each figure came by is recorded in
finding F26, together with the seven places where the arithmetic did NOT close and
what the arithmetic settled. Nothing here was taken on an extractor's confidence.

NO DUAL LISTING. ISPH trades on EGX only, as ISPH.CA, in EGP, ISIN EGS512O1C012,
1,008,000,000 shares at EGP 0.25 par. The repo's own price series
engine/raw_ohlc/EG/ISPH.csv closes at 13.220 on 23-Aug-2026 against the IR site's
live EGP 13.18 on the sweep date — same currency, same magnitude, same exchange.
Checked and closed by F44 rather than assumed.
"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from research_sweep import (SweepRegister, AssetClass, Ring, FindingClass,
                            SourceType, DriverMode)

SWEEP_DATE = "2026-09-08"
R = SweepRegister("ISPH", AssetClass.STOCK, SWEEP_DATE)
CO, IR, REG, PMD, PRESS, AGG = (SourceType.COMPANY_OFFICIAL, SourceType.COMPANY_IR,
                                SourceType.REGULATOR_OFFICIAL, SourceType.PRIMARY_MARKET_DATA,
                                SourceType.REPUTABLE_PRESS, SourceType.AGGREGATOR)

# document URLs, all on the company's own investor-relations host
SITE = "https://ibnsina-pharma.com/"
IRSITE = "https://ir.ibnsina-pharma.com/"
DOCS = "https://irfiles.technologyverse.com/isph"
FS25 = f"{DOCS}/IbnSina-Pharma-Q4-Dec-25-Consolidated-En-FSs-Issued.pdf"
FS24 = f"{DOCS}/IbnSina-Pharma-31DEC24-Cons-FSs-EN-Issued.pdf"
FS23 = f"{DOCS}/IbnSina-Pharma-FY-23-Consolidated-En-.pdf"
FS22 = f"{DOCS}/%D8%A7%D9%84%D9%82%D9%88%D8%A7%D8%A6%D9%85-%D8%A7%D9%84%D9%85%D8%A7%D9%84%D9%8A%D9%87-%D8%A7%D9%84%D9%85%D8%AC%D9%85%D8%B9%D9%87.pdf"
FSQ126 = f"{DOCS}/IbnSina-Pharma-Q1-Mar-26-Consolidated-En-FSs-Issued.pdf"
FSQ226 = f"{DOCS}/IbnSina-Pharma-Q2-Jun-26-Consolidated-En-FSs-Issued.pdf"
ER25 = f"{DOCS}/ISP-ER-FY-2025-Final.pdf"
ERQ126 = f"{DOCS}/ISP-ER-Q1-2026-Final.pdf"
ERQ226 = f"{DOCS}/ISP-ER-Q2-2026-final.pdf"
DECK25 = f"{DOCS}/1.-Investors-Presentation-Q4-2025.pdf"
BOD25 = f"{DOCS}/board-eng-25.pdf"

# ---------------------------------------------------------------------------
# PRIMARY-SOURCE ACCESS — the company's own site tried FIRST, logged either way
# ---------------------------------------------------------------------------
R.record_primary_access(SITE, False, SWEEP_DATE,
    "CORPORATE SITE BLOCKED. HTTP 403 with a Cloudflare interstitial reading 'Sorry, "
    "you have been blocked / You are unable to access ibnsina-pharma.com'. Tried first, "
    "by scripted request with a browser user-agent and again through the rendering fetch "
    "tool. This is origin-side bot defence, not this environment's egress proxy: the "
    "proxy's own failure log carries no entry for this host.")
R.record_primary_access("https://ibnsina-pharma.com/investor-relations/", False, SWEEP_DATE,
    "Same Cloudflare 403 on the corporate site's investor-relations path.")
R.record_primary_access(IRSITE, True, SWEEP_DATE,
    "DEDICATED IR SUB-DOMAIN REACHABLE (HTTP 200) and it is the build source for the "
    "whole Company ring. Sections read: Results Center, Presentations and Publications, "
    "Board and Shareholders Actions, News and Disclosures, Share & Corporate Information, "
    "Dividends, Insider Transactions, Analyst Coverage, Listing Information, Company "
    "Profile, IR Calendar.")
R.record_primary_access(f"{IRSITE}en/results-center", True, SWEEP_DATE,
    "Results Center lists audited consolidated statements FY2015-FY2025 and reviewed "
    "interims to 2Q2026, plus an earnings release for every period from FY2017. Six "
    "statement PDFs downloaded for this sweep: FY2022 (Arabic), FY2023, FY2024, FY2025, "
    "1Q2026, 2Q2026 — and five earnings releases.")
R.record_primary_access(f"{IRSITE}en/presentations-and-publications", True, SWEEP_DATE,
    "Earnings-call decks FY2017 through FY2025 downloaded; FY2025 deck (3 March 2026) "
    "carries the 2026 guidance page, the cash-conversion-cycle series by quarter and the "
    "FY22-FY25 free-cash-flow bridge. NOTE THE GAP: the most recent deck is FY2025. No "
    "1Q2026 or 1H2026 investor presentation has been published, so the study-year "
    "quarters are covered by their releases and statements only — see F43.")
R.record_primary_access(DECK25, True, SWEEP_DATE,
    "FY2025 investor presentation / earnings-call deck downloaded and read page by page "
    "off rendered pixels where the chart text does not extract cleanly.")
R.record_primary_access("https://www.cbe.org.eg/en", True, SWEEP_DATE,
    "Central Bank of Egypt home page read live: overnight deposit 19.00%, overnight "
    "lending 20.00%, main operation 19.50%, CONIA 19.488%, core inflation 14.700%, "
    "headline inflation 14.900%, USD buy 50.9786 / sell 51.0786.")
R.record_primary_access("https://www.cbe.org.eg/en/economic-research/statistics/cpi", False,
    SWEEP_DATE, "CBE CPI statistics sub-page resets the connection (curl error 35, "
    "'Recv failure: Connection reset by peer'). The inflation prints in F05 are taken "
    "from the CBE home page's own key-statistics panel instead, same issuer.")
R.record_primary_access("https://edaegypt.gov.eg/en/", True, SWEEP_DATE,
    "Egyptian Drug Authority site reachable; the Track & Trace notice-to-applicant "
    "(EDREX:NP.CIP.009, version 2/0, issue date 19/04/2026) downloaded and read.")

R.declare_study_year("2026", ["Q1-2026", "Q2-2026"])

# ---------------------------------------------------------------------------
# RING 1 — GLOBAL
# ---------------------------------------------------------------------------
f_fed = R.add(Ring.GLOBAL, "rate cycle & USD/FX regime", FindingClass.S,
    "Fed funds target range held at 3.50-3.75% for a fifth consecutive meeting on 29 July "
    "2026, with three dissents preferring a 25bp rise. Egypt's own easing has stopped in "
    "the same place: the CBE held on 20 August 2026 for a fourth consecutive meeting",
    "Federal Reserve FOMC statement, 29 July 2026, and the FOMC minutes of 28-29 July 2026",
    REG, "2026-07-29",
    url="https://www.federalreserve.gov/newsevents/pressreleases/monetary20260729a.htm",
    model_impact="Sets the SHAPE of the Kd path, which on this name is the second-largest "
                 "cost driver after the goods themselves. A stalled global easing cycle is "
                 "the condition under which the CBE's own pause persists, so the FY2026 "
                 "guidance assumption of a 4pp rate fall (F31) is modelled as a SCENARIO "
                 "and not as the base; the base holds the policy rate at the live 19.00/"
                 "20.00% (F05) and glides it only on evidence.")

f_fuel = R.add(Ring.GLOBAL, "commodity complex (input/output)", FindingClass.S,
    "Egypt raised petroleum product prices by EGP 3 per litre on 10 March 2026, a 14-17% "
    "rise, with diesel to EGP 20.50/litre, 92-octane to EGP 22.25 and vehicle CNG up 30% "
    "to EGP 13/m3 — the increase attributed to the Iran war and crude at multi-year highs",
    "Egyptian Ministry of Petroleum and Mineral Resources pricing decision of 10 March "
    "2026, reported by the State Information Service, Ahram Online and The National",
    PRESS, "2026-03-10",
    detail="Route recorded honestly: the ministry's own release was not fetched directly; "
           "this is press reporting of a government pricing decision, cross-read across "
           "three outlets carrying identical figures.",
    model_impact="Feeds the DISTRIBUTION COST STACK, not the cost of goods. ISPH runs 1,154 "
                 "delivery vehicles (F27) and books logistics inside cost of sales (EGP "
                 "111.9mn FY2025, note 24) and transport inside selling salaries/travel/"
                 "transport (EGP 1,153.7mn FY2025, note 25). Fuel escalates on this path, "
                 "NOT on headline CPI — one escalator per cost driver.")

f_gdem = R.add(Ring.GLOBAL, "global sector demand", FindingClass.C,
    "IQVIA Institute's 2026 global forecast has the world medicine market compounding at "
    "5-8% a year to about USD 2.6 trillion by 2030, with pharmerging markets adding USD "
    "121bn over the period",
    "IQVIA Institute, Global Medicine Use Trends 2026 / 2026 forecast commentary",
    PRESS, "2026-03-01",
    url="https://www.iqvia.com/insights/the-iqvia-institute/reports-and-publications/reports/global-medicine-use-trends-2026")

f_supply = R.add(Ring.GLOBAL, "trade / sanctions / supply chains", FindingClass.S,
    "Management reports NO shortages in the Egyptian market through 1H2026 despite the "
    "regional conflict, because manufacturers hold roughly four to six months of raw "
    "material; ISPH nevertheless raised its own inventory deliberately as a mitigation, "
    "taking inventory days from 38.3 (1H25) to 42.9 (1H26) and inventory on the balance "
    "sheet from EGP 8,246mn to EGP 11,437mn in six months",
    "Ibnsina Pharma 1H2026 earnings release, Cairo 12 August 2026, 'Working Capital' and "
    "co-CEO commentary", IR, "2026-08-12", url=ERQ226, fiscal_period="Q2-2026",
    model_impact="Raises the INVENTORY DAYS driver above its own trailing mean and keeps it "
                 "there while the conflict persists — a stated policy choice, not a control "
                 "failure, so the forecast unwinds it slowly rather than reverting to the "
                 "34.7-day FY2025 exit. Each extra inventory day costs roughly EGP 190mn of "
                 "funding at the FY2026 revenue run-rate, charged at the credit-facility rate.")

# ---------------------------------------------------------------------------
# RING 2 — COUNTRY
# ---------------------------------------------------------------------------
f_cbe = R.add(Ring.COUNTRY, "sovereign macro (inflation, policy rate, FX/deval risk)",
    FindingClass.D,
    "Read live from the CBE's own site on the sweep date: overnight deposit rate 19.00%, "
    "overnight lending rate 20.00%, main operation 19.50%, discount rate 19.50%, all "
    "effective from 15 February 2026; CONIA 19.488%; core inflation 14.700%; headline "
    "inflation 14.900%; USD buy 50.9786 / sell 51.0786, EUR buy 59.1810 / sell 59.4350",
    "Central Bank of Egypt, official website key-statistics panel and MPC Decisions page, "
    "read 8 September 2026", REG, "2026-09-08", url="https://www.cbe.org.eg/en",
    model_impact="DRIVER UNLOCK for the interest leg. The lending rate is the reference the "
                 "credit-facility cost is built off, and the company's own filing (note 35) "
                 "prints the full MPC path it borrowed through — 25.00/26.00% in Apr-2025 "
                 "down to 19.00/20.00% in Feb-2026 — so the historical interest charge can "
                 "be tied to a dated rate rather than a plug. Positive real rate of ~4.1pp "
                 "on headline is what keeps the pause credible.")

f_hold = R.add(Ring.COUNTRY, "sovereign macro (inflation, policy rate, FX/deval risk)",
    FindingClass.S,
    "The CBE held rates on 20 August 2026 for a fourth consecutive meeting, all six "
    "economists surveyed expecting it; July 2026 core inflation rose to 14.7% from 14.3% "
    "in June and headline to 14.9% from 14.3% — inflation turning back UP, not down",
    "Bloomberg, 'Egypt Holds Rates a Fourth Time With No End to Iran War in Sight', "
    "20 August 2026; Daily News Egypt MPC preview of 19 August 2026", PRESS, "2026-08-20",
    model_impact="Kills the assumption embedded in the company's own FY2026 guidance that "
                 "rates fall 4pp this year (F31). The base case holds the policy rate flat "
                 "through FY2026 and glides it only from FY2027; the guidance path is carried "
                 "as the upside scenario. Interest expense is ~2.4% of sales against a 1.2% "
                 "net margin, so this single assumption is worth more than the whole margin.")

f_decree = R.add(Ring.COUNTRY, "regulatory environment (regulator, caps, tariffs, tax/subsidy)",
    FindingClass.D,
    "Egyptian drug prices are ADMINISTERED end to end. Minister of Health Decree 499/2012 "
    "imposes MANDATORY profit margins at each level of the supply chain — distributor and "
    "pharmacist — which must be reflected in the final sale price; the EDA's Pricing "
    "Committee sets the price itself by external reference pricing, innovators at the lowest "
    "reference-country price and generics at a decreed discount to it. Prices may be reviewed "
    "when the currency moves more than 15% a year, or on company request capped at 5% a year",
    "Mondaq / Pharmaceutical & Medical Devices Comparative Guide — Egypt (2025), citing "
    "Minister of Health Decree 499/2012 and the EDA Pricing Decree", PRESS, "2025-06-01",
    url="https://www.mondaq.com/healthcare/1586796/pharmaceutical-medical-devices-comparative-guide",
    model_impact="THE FINDING THAT DECIDES THE WHOLE DRIVER SET. The distributor's spread is "
                 "a decreed percentage of an administered price, so gross profit is "
                 "(regulated spread x administered price x volume) and NOT a margin to be "
                 "typed in. The revenue build is market units x average selling price x ISPH "
                 "share; the cost build is purchase cost per pack from note 24. Margin falls "
                 "out. See also F39: the decree's own margin SCHEDULE could not be obtained, "
                 "which is why the spread is inferred from the filed cost stack rather than "
                 "read off the decree.")

f_reprice26 = R.add(Ring.COUNTRY, "regulatory environment (regulator, caps, tariffs, tax/subsidy)",
    FindingClass.B,
    "THE PRICING REGIME IS BEING REPLACED, ANNOUNCED THE DAY OF THIS SWEEP. The EDA is "
    "launching a new framework 'in the coming days': no price move while the USD stays "
    "inside a 10% band, with sustained swings of up to six months triggering a review on "
    "actual product costs; the reference basket cut from 35 countries to 15 with regional "
    "markets such as the UAE added; foreign products at the lowest suitable reference price "
    "minus a further 10%; locally made products priced at 50-60% of the imported equivalent. "
    "Industry officials quoted expect drug prices DOWN 30-40%. Prices last moved in October 2024",
    "EnterpriseAM Egypt, 'The gov't overhauls drugs pricing with FX band, smaller reference "
    "basket, and local production advantage', 8 September 2026", PRESS, "2026-09-08",
    url="https://enterpriseam.com/egypt/2026/09/08/the-govt-overhauls-drugs-pricing-with-fx-band-smaller-reference-basket-and-local-production-advantage/",
    model_impact="BASE CHANGER, and it must be modelled as an explicit dated event and "
                 "DUAL-FRAMED, never smoothed into a price glide. It hits the PRICE leg of "
                 "the volume x price build directly, in the opposite direction to every "
                 "recent year: FY2023-FY2025 revenue growth was almost entirely price "
                 "(market ASP EGP 58 -> 86 -> 110 per box on units that FELL 4%, then rose "
                 "10%). A 30-40% price cut with a fixed percentage spread cuts gross profit "
                 "per pack by the same proportion unless volume replaces it. Frame A: regime "
                 "unchanged, company guidance of 11% ASP growth. Frame B: the new formula "
                 "lands inside the window and prices fall. Report both.")

f_margins25 = R.add(Ring.COUNTRY, "regulatory environment (regulator, caps, tariffs, tax/subsidy)",
    FindingClass.S,
    "The margin schedule itself was restructured in the 2025 round: the EDA agreed with the "
    "pharmacists' syndicate to drop the extra EGP 1-per-pack margin in exchange for raising "
    "the pharmacy discount on essential domestic drugs from 20% to 23% and on non-essential "
    "domestic drugs from 25% to 27%, with imported-drug discounts restructured to 15-20%; "
    "oncology and high-priced packs excluded and given a FIXED margin instead (EGP 4,000 on "
    "packs above EGP 100,000; EGP 3,000 on EGP 50,000-100,000; EGP 2,000 on EGP 20,000 up). "
    "The new repricing trigger is a weighted index — USD 60%, inflation 30%, interest rates "
    "10% — opening applications at a +/-10% cumulative move",
    "Al Manassa, 'Egypt to link drug prices to exchange rate and inflation', reporting the "
    "EDA's community dialogue with the pharmacists' syndicates, the Chamber of Pharmaceutical "
    "Industry and the distribution companies", PRESS, "2026-02-01",
    url="https://manassa.news/en/news/33099",
    model_impact="The distributor's spread is the residual between the manufacturer's ex-"
                 "factory price and the pharmacy's discount. Raising the PHARMACY discount by "
                 "3pp on essential domestic drugs compresses what is left for the distributor "
                 "on the same pack unless the ex-factory price moves too. Sets the direction "
                 "of the FY2027+ spread assumption to DOWN from the FY2025 peak, and gives "
                 "the mix rule: the fixed-EGP margin on high-price packs means an oncology "
                 "and specialty mix shift RAISES revenue per pack while LOWERING margin "
                 "percentage — exactly the mix effect the company names in F27.")

f_tax = R.add(Ring.COUNTRY, "regulatory environment (regulator, caps, tariffs, tax/subsidy)",
    FindingClass.D,
    "Egyptian corporate income tax 22.50%, confirmed from the company's own deferred-tax "
    "table where every temporary difference is measured at 22.50%; the parent's corporate "
    "tax records are examined and settled through 2023, salary/stamp/VAT through 2022 and "
    "withholding tax through 2024, and the subsidiary AIM Healthcare has never been examined "
    "since inception",
    "Ibn Sina Pharma FY2025 audited consolidated financial statements, notes 29 and 31",
    CO, "2026-03-01", url=FS25, is_fs_data=True, fiscal_period="FY2025",
    model_impact="Fixes the statutory tax rate for the forecast at 22.50% rather than an "
                 "effective rate: the FY2025 effective charge of 11.6% is the product of a "
                 "one-off EGP 131.6mn deferred-tax credit and cannot be projected. Tax is "
                 "built as 22.50% of taxable profit with the deferred balance rolled on the "
                 "lease and ECL differences the note itemises. The unexamined subsidiary is "
                 "an unquantified contingent tax exposure and is disclosed, not provided for.")

f_upa = R.add(Ring.COUNTRY, "fiscal / political events with sector read-through", FindingClass.S,
    "THE STATE IS A SLOW PAYER AND ITS ARREARS ARE THE HOSPITAL CHANNEL'S RECEIVABLE. A "
    "presidential decision cut back the powers of the Unified Procurement Authority after "
    "its debts to pharmaceutical suppliers piled up and medicines went missing; the UPA told "
    "firms implementation was unlikely before July 2026, when the new fiscal year begins and "
    "after existing debts are fully settled. Proposals under discussion include bank loans "
    "and credit facilities to clear the dues, and selling land held by the Egyptian "
    "Pharmaceutical Trading Company, merged into the UPA in 2020. Major distributors "
    "including United Pharma are named as facing mounting pressure from the debts",
    "MadaMasr, 'Piled-up debts, missing medicines: Sisi cuts back powers of Unified "
    "Procurement Authority', 21 September 2025", PRESS, "2025-09-21",
    detail="ROUTE RECORDED: the article itself returned HTTP 403 to this environment's fetch "
           "tool. This finding rests on the search engine's extract of that article, which is "
           "weaker than a full read, and is flagged as such rather than presented as a direct "
           "read. It is corroborated independently by the company's own disclosure that "
           "'UPA Collection' is one of the four named drivers of its cash conversion cycle "
           "(F29) and that hospital purchases with 'longer credit facilities' were CAPPED in "
           "2Q25 in proportion to hospital collection performance and resumed from 3Q25 (F29).",
    model_impact="Sets the DSO driver for the tenders and private-hospitals channel, 18.4% of "
                 "1H2026 gross revenue and the fastest-growing channel at +29.5%. Group DSO "
                 "has risen 85 -> 90 -> 94.5 days across FY2024/FY2025/1H2026 while the "
                 "hospital mix rose; the forecast holds hospital-channel DSO ABOVE the group "
                 "average and sensitises a UPA settlement as an upside, not a base.")

# ---------------------------------------------------------------------------
# RING 3 — INDUSTRY
# ---------------------------------------------------------------------------
f_mkt = R.add(Ring.INDUSTRY, "demand drivers & capacity/supply balance", FindingClass.D,
    "IQVIA's Egypt market, decomposed into units and price by the company itself: FY2023 "
    "EGP 206bn (+29%) on 3.5bn units (-4%) at an average selling price of EGP 58 (+34%); "
    "FY2024 EGP 292bn (+41%) on 3.4bn units (-4%) at EGP 86 (+48%); FY2025 EGP 410bn (+41%) "
    "on 3.72bn units (+10%) at EGP 110 (+28%). 1H2026 EGP 214bn (+14.4%) on 1,700mn units "
    "(-3.6%) at an ASP of EGP 126 (+18.7%)",
    "Ibnsina Pharma FY2025 investor presentation / earnings call, 3 March 2026, 'Market & "
    "Company Growth'; and the FY2025 and 1H2026 earnings releases, both citing IQVIA",
    IR, "2026-03-03", url=DECK25, fiscal_period="FY2025",
    model_impact="DRIVER UNLOCK. Converts the top line from a growth rate into market units x "
                 "market ASP x ISPH share, each leg forecast separately. It also carries the "
                 "warning the growth rate hides: VOLUME HAS FALLEN IN THREE OF THE LAST FOUR "
                 "PERIODS. Every year of headline growth since FY2023 is price. A price regime "
                 "change (F08) therefore removes the entire growth engine, which is why the "
                 "volume and price legs must be projected separately and never blended.")

f_price = R.add(Ring.INDUSTRY, "pricing", FindingClass.D,
    "The company's own realised price per box: EGP 65 at the end of 2023 rising to EGP 114 in "
    "2025, +77% in two years, disclosed in the FY2025 release's own explanation of why its "
    "debt rose ('new purchases of pharma products done with higher prices while selling the "
    "old inventory in old prices'). FY2026 guidance decomposes 15% market growth into 11% ASP "
    "and 4% units",
    "Ibnsina Pharma FY2025 earnings release, 2 March 2026, 'Leverage Ratios'; FY2025 "
    "investor presentation, 2026 Guidance page", IR, "2026-03-02", url=ER25,
    fiscal_period="FY2025",
    model_impact="Gives the PRICE leg its own level and its own history, and names the "
                 "mechanism by which repricing moves the balance sheet before it moves the "
                 "income statement: inventory is bought at the new price and sold out of the "
                 "old, so a repricing event is a WORKING-CAPITAL shock first and a margin "
                 "event second. The model must carry that lag explicitly rather than "
                 "revaluing inventory and revenue in the same period.")

f_ezaby = R.add(Ring.INDUSTRY, "new entrants (named-competitor level)", FindingClass.S,
    "A NAMED CUSTOMER HAS BECOME A NAMED COMPETITOR. IQVIA has begun classifying the Ezaby "
    "Group as a DISTRIBUTOR when it purchases from ISP to supply its own branches, and ISP's "
    "reported market share is now restated upward to include Ezaby's share so it aligns with "
    "the historical series. ISP's 1H2026 share of 29.1% is quoted on that adjusted basis",
    "Ibnsina Pharma 1H2026 earnings release, 12 August 2026, Market Overview footnote",
    IR, "2026-08-12", url=ERQ226, fiscal_period="Q2-2026",
    model_impact="The disintermediation risk for a distributor, named and dated. A large "
                 "pharmacy chain buying to supply its own branches is one step from buying "
                 "direct from manufacturers. Caps the market-share driver: the FY2026 guidance "
                 "of 32.0% is NOT adopted; share is held at the 1H2026 actual of 29.1% in the "
                 "base and the 32.0% path is run as the upside. It also means the reported "
                 "share series is not on a constant definition and must be footnoted wherever "
                 "it is quoted.")

f_tt = R.add(Ring.INDUSTRY, "technology substitution", FindingClass.S,
    "Egypt's national pharmaceutical Track & Trace system (EPTTS) is live: Phase 1 applies to "
    "all shipments shipped on or after 1 FEBRUARY 2026 plus the stock packed with them; every "
    "saleable pack must carry a GS1 DataMatrix with GTIN, serial, expiry and batch; and "
    "DISTRIBUTION CENTRES ARE NOT PERMITTED TO SERIALIZE OR REPRINT BARCODES — printing inside "
    "Egypt is allowed only at EDA-licensed facilities after batch approval. No API exists in "
    "Phase 1; reporting is by CSV, capped at 50,000 serials per file, with atomic rejection",
    "Egyptian Drug Authority, Notice to Applicant — Egyptian Track & Trace for Pharmaceutical "
    "(EPTTS) Technical FAQ Phase 1, code EDREX:NP.CIP.009, version 2/0, issued 19 April 2026",
    REG, "2026-04-19",
    url="https://edaegypt.gov.eg/media/paif1cpf/egyptian-track-trace-for-pharmaceutical-eptts-technical-faq-phase-1-_2026.pdf",
    model_impact="Two-sided and both sides are modelled. AGAINST: the serialize/reprint ban "
                 "constrains the 3PL service line the company sells — its own profile lists "
                 "overprinting, relabelling and repackaging — so the 3PL revenue driver (EGP "
                 "336.6mn in 1H2026, +89.4%) is capped below its recent growth rate pending "
                 "evidence of an EDA licence. FOR: mandatory serialisation raises the fixed "
                 "compliance cost of distributing at all, which is a barrier to the sub-scale "
                 "entrant and supports the share driver. Technology capex is already running "
                 "at EGP 97.7mn (FY2025) and EGP 58.5mn (1H2026).")

f_share = R.add(Ring.INDUSTRY, "competitor capacity / price moves (named)", FindingClass.S,
    "ISP's IQVIA share peaked and has turned: 24.2% FY2023, 30.8% FY2024, 31.1% 1H2025, 30.2% "
    "FY2025, 28.7% 1Q2026, 29.1% 1H2026 — 2.0pp below the 1H2025 peak and 2.9pp below the "
    "company's own 32.0% FY2026 assumption. Within that, ISP leads pharmacy and wholesale "
    "with ~35% of a segment that is 69% of the drug market, and is the largest private "
    "distributor to hospitals with 22.3% of a segment that is ~31%. Among named private "
    "competitors, United Pharma is reported to be under mounting debt pressure from the UPA "
    "arrears",
    "Ibnsina Pharma FY2025, 1Q2026 and 1H2026 earnings releases citing IQVIA; Arab Finance / "
    "Zawya reporting of the H1-2025 IQVIA ranking; MadaMasr, 21 September 2025 on United Pharma",
    IR, "2026-08-12", url=ERQ226, fiscal_period="Q2-2026",
    model_impact="Sets the MARKET-SHARE driver at the 1H2026 actual of 29.1% held flat, not at "
                 "guidance. A rival's funding distress is an upside to share and a downside to "
                 "sector receivable quality at the same time, so it is NOT taken as a "
                 "one-directional share tailwind.")

# ---------------------------------------------------------------------------
# RING 4 — COMPANY — official financial statements
# ---------------------------------------------------------------------------
f_fs25 = R.add(Ring.COMPANY, "official financial statements", FindingClass.D,
    "FY2025 AUDITED CONSOLIDATED, unqualified opinion by Ghorab & Co (Nexia International), "
    "Cairo 1 March 2026, signed by CFO Mo'men Gomaa, CEO Omar Abdul Gawad and Chairman Abd El "
    "Aziz Ali Abd El Aziz. Net sales EGP 76,597,057,544; cost of sales EGP 70,147,680,642; "
    "gross profit EGP 6,449,376,902 (8.42%); operating profit after other income, selling, "
    "admin and ECL EGP 3,613,452,963; net financing cost EGP 2,536,109,720; profit before tax "
    "EGP 1,077,343,243; net profit EGP 951,983,367; EPS EGP 0.76. Total assets EGP "
    "36,213,703,819; total equity EGP 2,784,020,299; total liabilities EGP 33,429,683,520. "
    "Operating cash flow NEGATIVE EGP 71,055,245 after EGP 2,271,077,430 of finance cost paid",
    "Ibn Sina Pharma FY2025 audited consolidated financial statements, statement of financial "
    "position (printed p.3), profit or loss (p.4), changes in equity (p.6) and cash flow (p.7)",
    CO, "2026-03-01", url=FS25, is_fs_data=True, fiscal_period="FY2025",
    detail="Read off rendered pixels; every column re-added against its own printed subtotals "
           "and every one closed to the pound. See F26 for the full footing record.",
    model_impact="The base year. Establishes that the whole business converts a 8.42% gross "
                 "margin into a 1.24% net margin, and that the gap is 3.3pp of interest — so "
                 "the interest driver, not the margin driver, is where the value is.")

f_fs24 = R.add(Ring.COMPANY, "official financial statements", FindingClass.D,
    "FY2024 AUDITED CONSOLIDATED. Net sales EGP 55,842,453,860; cost of sales EGP "
    "51,445,884,310; gross profit EGP 4,396,569,550 (7.87%); net financing cost EGP "
    "1,549,514,268; profit before tax EGP 703,280,660; net profit EGP 614,562,345; EPS EGP "
    "0.49. Total assets EGP 28,641,557,747; total equity EGP 2,031,218,546. Operating cash "
    "flow NEGATIVE EGP 926,576,018",
    "Ibn Sina Pharma FY2024 audited consolidated financial statements (own filing), "
    "cross-tied to the FY2025 filing's comparative column", CO, "2025-02-25", url=FS24,
    is_fs_data=True, fiscal_period="FY2024",
    model_impact="Second historical year. The FY2024/FY2025 pair is what shows the margin "
                 "RISING 7.87% -> 8.42% on the repricing round, which is the level the "
                 "forecast must decide whether to keep.")

f_fs23 = R.add(Ring.COMPANY, "official financial statements", FindingClass.D,
    "FY2023 AUDITED CONSOLIDATED, unqualified opinion by Khaled Elghannam & Eissa Refaei & Co "
    "(Nexia International) — a DIFFERENT audit firm from FY2025. Net sales EGP 33,949,328,681; "
    "cost of sales EGP 31,434,239,757; gross profit EGP 2,515,088,924 (7.41%); net financing "
    "cost EGP 878,788,400; net profit EGP 213,272,470; EPS EGP 0.17. Total assets EGP "
    "18,549,810,926; total equity EGP 1,449,119,799",
    "Ibn Sina Pharma FY2023 audited consolidated financial statements", CO, "2024-03-03",
    url=FS23, is_fs_data=True, fiscal_period="FY2023",
    detail="The FY2023 filing has NO text layer at all — 45 scanned pages. Every figure here "
           "was read off rendered pixels and footed. Cross-filing tie confirmed: this "
           "statement's closing equity of EGP 1,449,119,799 is the opening balance of the "
           "FY2025 statement of changes in equity, to the pound.",
    model_impact="Third historical year and the pre-repricing margin floor: 7.41% gross margin "
                 "on a market whose ASP was EGP 58 a box. Anchors the bear case for the spread.")

f_fs22 = R.add(Ring.COMPANY, "official financial statements", FindingClass.D,
    "FY2022 AUDITED CONSOLIDATED (Arabic original, unqualified opinion signed Cairo 28 "
    "February 2023). Net sales EGP 22,264,495,100; cost of sales EGP 20,647,700,037; gross "
    "profit EGP 1,616,795,063 (7.26%); net financing cost EGP 305,421,241; net profit EGP "
    "170,874,350; EPS EGP 0.13. Its own FY2021 comparative: net sales EGP 21,732,832,791, "
    "gross profit EGP 1,629,518,921 (7.50%), net profit EGP 314,396,880, EPS EGP 0.26",
    "Ibn Sina Pharma FY2022 audited consolidated financial statements, Arabic original",
    CO, "2023-02-28", url=FS22, is_fs_data=True, fiscal_period="FY2022",
    detail="Arabic-Indic numerals read off rendered pixels. Every FY2022 figure agrees to the "
           "pound with the comparative column of the FY2023 English filing, which is an "
           "independent cross-check of both readings. NOTE THE FY2021 SHAPE: net profit FELL "
           "from EGP 314mn to EGP 171mn while revenue rose 2.4% — the finance cost went from "
           "EGP 199mn to EGP 305mn. The pattern of interest eating growth is not new.",
    model_impact="Fourth historical year, hitting the protocol's target depth. Gives the "
                 "pre-devaluation spread of 7.26-7.50% and the interest-cost sensitivity that "
                 "predates the 2024 float.")

f_wc = R.add(Ring.COMPANY, "official financial statements", FindingClass.D,
    "THE WORKING-CAPITAL BALANCE SHEET, FY2025, from the notes. Inventory EGP 8,246,348,097 "
    "(goods for sale 6,725.8mn, goods in transit 813.2mn, returns 664.1mn, spares 43.2mn). "
    "Receivables gross EGP 22,162,598,258 (accounts 17,428.8mn + notes 4,733.8mn) less ECL "
    "628,094,686 = 21,534,503,572, of which 21,520,398,466 falls due inside 12 months. "
    "Suppliers and notes payable EGP 25,475,648,743 (suppliers 6,016.4mn + NOTES PAYABLE "
    "19,459.3mn). Credit facilities EGP 5,169,637,310, stated to finance purchases and "
    "operating expenses. Loans EGP 994,523,138 across five NAMED facilities: EBRD 800,000,000 "
    "drawn against an 800,000,000 limit to 1 Dec 2030; First Abu Dhabi Misr 93,149,322 of "
    "190,000,000 to 2030; Faisal Islamic Bank 74,908,778 to Aug 2028; National Bank of Egypt "
    "18,131,705 of 200,000,000 to Jun 2026; Credit Agricole 8,333,333 of 50,000,000 to Jun "
    "2026. Lease liabilities EGP 1,048,772,858 with EGP 284,416,983 of finance charge in the "
    "year. Contingent liabilities EGP 4,460,203,265 — letters of credit 2,203,390,019 and "
    "letters of guarantee 2,256,813,246",
    "Ibn Sina Pharma FY2025 audited consolidated financial statements, notes 7, 8, 12, 16, 17, "
    "18, 19, 33", CO, "2026-03-01", url=FS25, is_fs_data=True, fiscal_period="FY2025",
    model_impact="DRIVER UNLOCK for the entire cash-conversion-cycle build AND for the interest "
                 "leg. Debt is built facility by facility with its own limit and maturity, per "
                 "the same-class prior in engine/Fundamental_Driver_Ledger.md (GBCO, "
                 "07-09-2026): finance cost must be built on the borrowings that actually bear "
                 "interest, never as a ratio to revenue. Notes payable at 76% of trade payables "
                 "means the payable is a BILL with a date, so DPO is a contractual driver not "
                 "a behavioural one. The EGP 2.2bn of letters of credit is how imported "
                 "inventory is financed and belongs in the funding cost, not off-sheet.")

# ---------------------------------------------------------------------------
# RING 4 — COMPANY — regular disclosures (study-year quarters)
# ---------------------------------------------------------------------------
f_q126 = R.add(Ring.COMPANY, "regular disclosures", FindingClass.D,
    "Q1-2026 REVIEWED CONSOLIDATED, period ended 31 March 2026. Net sales EGP 20,500,933,842 "
    "(+20.3% on Q1-2025's 17,044,961,201); cost of sales EGP 18,861,369,933; gross profit EGP "
    "1,639,563,909 — a gross margin of 8.00% against 8.38% in Q1-2025. Financing expenses fell "
    "to EGP 468,493,074 from EGP 611,216,963. Net profit EGP 255,936,016 (+40.7%); EPS EGP 0.21",
    "Ibn Sina Pharma 1Q2026 reviewed consolidated financial statements, statement of profit or "
    "loss (printed p.4)", CO, "2026-05-17", url=FSQ126, is_fs_data=True, fiscal_period="Q1-2026",
    detail="THIS PAGE DID NOT FOOT AS PRINTED AND ARITHMETIC SETTLED IT. The operating subtotal "
           "is printed in brackets as (691,218,660) for Q1-2026 and (785,000,347) for Q1-2025, "
           "i.e. as negatives; every line below uses them as POSITIVES, and only then does the "
           "page reach its own printed profit before tax of 276,836,865 and 186,342,077. The "
           "1H2026 filing prints the same subtotal without brackets. Bracketing error in the "
           "1Q filing; the magnitudes are right and are used.",
    model_impact="First actual of the study year. The margin is already BELOW the FY2025 "
                 "full-year 8.42% and below the company's own 8.2% FY2026 guidance.")

f_q226 = R.add(Ring.COMPANY, "regular disclosures", FindingClass.B,
    "Q2/1H-2026 REVIEWED CONSOLIDATED, period ended 30 June 2026, AND IT CONTRADICTS A FLAT "
    "MARGIN PATH. 1H net sales EGP 41,492,005,562 (+18.4%); gross profit EGP 3,332,749,479 at "
    "a GROSS MARGIN OF 8.03% against 8.70% in 1H2025 and against the FY2025 full year of "
    "8.42%. Q2 alone: net sales EGP 20,991,071,720, gross profit EGP 1,693,185,570, margin "
    "8.07% against 9.01% in Q2-2025. 1H financing expenses EGP 1,008,333,103, DOWN 22.6%. Net "
    "profit EGP 511,299,061 (+31.5%). Balance sheet at 30 June 2026: inventory EGP "
    "11,436,516,818 (up 38.7% in six months), receivables EGP 22,005,784,958, payables EGP "
    "26,321,185,238, credit facilities EGP 7,532,189,291 (up 45.7% in six months), total "
    "assets EGP 40,180,625,208, equity EGP 3,137,279,411",
    "Ibn Sina Pharma 2Q2026 reviewed consolidated financial statements, financial position "
    "(printed p.3), profit or loss (p.4), comprehensive income (p.5)",
    CO, "2026-08-12", url=FSQ226, is_fs_data=True, fiscal_period="Q2-2026",
    detail="All four columns of the profit-or-loss page re-added and all four closed exactly; "
           "the balance sheet closes on both dates. Read off rendered pixels.",
    model_impact="BASE CHANGER for the margin path, and it is modelled as a dated event rather "
                 "than smoothed. TWO HALVES OF THE YEAR MOVE IN OPPOSITE DIRECTIONS: the gross "
                 "margin is 39bp below the FY2025 average while the interest cost is 23% lower, "
                 "so net profit rises 31.5% on a FALLING spread. Any forecast that holds the "
                 "FY2025 margin flat is already contradicted by the company's own half-year. "
                 "The margin driver starts from 8.03%, not 8.42%. Separately, inventory and "
                 "credit facilities both grew far faster than sales in the half, so the "
                 "working-capital driver must be set off the 1H exit balances, not the FY2025 "
                 "close.")

f_costs = R.add(Ring.COMPANY, "regular disclosures", FindingClass.D,
    "THE COST STACK, ITEMISED, WHICH IS WHAT MAKES MARGIN AN OUTPUT. FY2025 cost of sales "
    "(note 24) EGP 70,147,680,642: pharmaceuticals and cosmetics 69,869,668,630 — 99.60% of "
    "the total — plus logistics 111,851,760, rentals and storage 32,219,196, salaries "
    "47,325,379, utilities 22,734,888, insurance 8,281,312, right-of-use depreciation "
    "8,323,286, amortisation 1,804,458, other 45,472,199, less discount 466. Selling and "
    "marketing (note 25) EGP 1,669,119,042: salaries/travel/transport 1,153,657,636, "
    "maintenance/services/utilities 298,524,433, rent/insurance/security/cleaning 142,321,061, "
    "other 74,615,912. General and administrative (note 26) EGP 1,011,851,126 including "
    "depreciation 171,772,249, right-of-use depreciation 139,677,882, amortisation 27,628,779 "
    "and bank expenses 72,153,298. Revenue by line (note 23): pharmaceuticals and cosmetics "
    "76,194,743,873, warehousing and transportation services 326,078,079, other marketing "
    "services 72,383,699, database programming 3,851,893",
    "Ibn Sina Pharma FY2025 audited consolidated financial statements, notes 23, 24, 25 and 26",
    CO, "2026-03-01", url=FS25, is_fs_data=True, fiscal_period="FY2025",
    model_impact="DRIVER UNLOCK, and the reason no margin is ever an input on this name. Cost "
                 "of goods is 99.60% of cost of sales, so purchase cost per pack is derivable "
                 "from note 24 divided by the volume leg, and the gross spread FALLS OUT of "
                 "(selling price per pack - purchase cost per pack) x packs. Everything else "
                 "in the stack is a distribution cost with its own physical driver: logistics "
                 "and transport on the vehicle count and the fuel path, rent and storage on "
                 "pallet positions, salaries on headcount.")

f_grossnet = R.add(Ring.COMPANY, "regular disclosures", FindingClass.D,
    "THE GROSS-TO-NET BRIDGE — the negotiated half of the spread, which the decree does not "
    "set. Gross revenue against net revenue: FY2024 EGP 57,909,529,493 vs 55,842,453,860, a "
    "discount of 2,067,075,633 or 3.57% of gross; FY2025 EGP 80,092,086,952 vs 76,597,057,544, "
    "a discount of 3,495,029,408 or 4.36%; 1H2026 EGP 43,195,734,805 vs 41,492,005,562, a "
    "discount of 1,703,729,243 or 3.94%. Management explains the FY2025 widening directly: "
    "'targeting cash segments implies more cash discounts, however it allows liquidity in a "
    "high interest rate environment'",
    "Ibnsina Pharma FY2025 and 1H2026 earnings releases, Income Statement tables and Gross "
    "Profit commentary", IR, "2026-08-12", url=ERQ226, fiscal_period="Q2-2026",
    model_impact="Separates the CONTRACTUAL spread (the decreed margin, F07) from the "
                 "NEGOTIATED spread (the cash discount the company chooses to give), and makes "
                 "the second one a driver in its own right with an explicit trade-off against "
                 "DSO and interest. A discount given to pull cash forward is priced against "
                 "the credit-facility rate; that is the single decision this business makes "
                 "most often and it must be modelled, not averaged away.")

f_foot = R.add(Ring.COMPANY, "regular disclosures", FindingClass.C,
    "FOOTING RECORD. Every primary statement page in FY2022, FY2023, FY2024, FY2025, 1Q2026 "
    "and 2Q2026 is a scanned image with no text layer, so each was rendered to pixels and read "
    "off the image, then re-added against its own printed subtotals. All closed except seven "
    "places, each resolved by arithmetic: (a) FY2025 note 26 totals EGP 1,011,690,002 against "
    "the face's 1,011,851,126, a gap of 161,124 — the FACE is right because only 1,011,851,126 "
    "reaches the printed operating subtotal of 3,613,452,963; (b) FY2025 note 27 totals "
    "82,538,284 against the face's 82,436,233, a gap of 102,051, same test, face right; (c) the "
    "FY2025 statement of changes in equity shows FY2024 net profit 614,562,239 with NCI (112) "
    "against the profit-and-loss account's 614,562,345 with NCI (6), a gap of EGP 106 in "
    "non-controlling interests; (d) the FY2023 filing's FY2022 equity column adds to "
    "1,259,876,658 against a printed 1,259,876,659, one pound; (e) the 1Q2026 operating "
    "subtotal is printed in brackets and used as a positive (see F26); (f) FY2025 note 16 "
    "labels the EGP 891,226,704 tranche 'short term' and the EGP 103,296,434 tranche 'long "
    "term', the exact reverse of the balance sheet, and the EBRD facility's 2030 maturity "
    "settles that the FACE is right; (g) FY2025 note 8 swaps the labels 'formation' and 'used' "
    "on the ECL movement against the cash-flow statement, though the roll-forward foots either "
    "way. Nothing material; every one disclosed",
    "Ibn Sina Pharma FY2022, FY2023, FY2024, FY2025, 1Q2026 and 2Q2026 filings, read by "
    "rendering each statement page at 150-170 dpi", CO, "2026-09-08", url=FS25)

# ---------------------------------------------------------------------------
# RING 4 — COMPANY — IR communications
# ---------------------------------------------------------------------------
f_er226 = R.add(Ring.COMPANY, "IR communications (calls, presentations, releases)",
    FindingClass.D,
    "1H2026 EARNINGS RELEASE, Cairo 12 August 2026 — the operating anchors the statements do "
    "not carry. Clients served 52,736, split 47,788 retail pharmacies, 3,982 hospital clients "
    "and 966 wholesale clients; by geography 31.8% Cairo and Canal, 28.9% Delta, 25.0% Upper "
    "Egypt, 14.3% Alexandria. 72 sites, revenue per site EGP 576.3mn (+18.4%). Fleet 1,154 "
    "vehicles against 1,024, revenue per vehicle EGP 36mn (+5.1%). Headcount 10,081 against "
    "9,528, +823 in the year, revenue per employee EGP 4.1mn (+8.7%). CHANNEL SPLIT of EGP "
    "43.2bn gross: pharmacies 53.0% = EGP 22.9bn (+25.1%); wholesale 27.9% = EGP 12bn (+0.7%); "
    "tenders and private hospitals 18.4% = EGP 7.9bn (+29.5%); 3PL and other 0.8% = EGP 336.6mn "
    "(+89.4%). WAREHOUSING: scaling from 88k pallet positions in 2025 to 157k by year-end 2026. "
    "Capex EGP 579mn — distribution centres 430mn, vehicles 57.6mn, technology 58.5mn, upgrades "
    "23.5mn. Interest expense to sales 2.4% from 3.7%; debt ratio 22.8% from 26.2%; TTM net "
    "debt/EBITDA 2.15x from 2.21x; net debt to equity 2.62x from 3.0x",
    "Ibnsina Pharma 1H2026 Earnings Release, 12 August 2026", IR, "2026-08-12", url=ERQ226,
    fiscal_period="Q2-2026",
    model_impact="DRIVER UNLOCK for the entire physical build, and the release is arithmetic-"
                 "consistent with the filing: its EBITDA of 1,737,883,491 is exactly gross "
                 "profit less SG&A-ex-D&A less ECL from the audited profit-and-loss account. "
                 "Revenue is built by CHANNEL, each with its own price and volume path and its "
                 "own receivable term. Wholesale at +0.7% against pharmacies at +25.1% is the "
                 "mix shift that explains the margin fall, so the channel split is not colour, "
                 "it is the margin bridge.")

f_er126 = R.add(Ring.COMPANY, "IR communications (calls, presentations, releases)",
    FindingClass.D,
    "1Q2026 EARNINGS RELEASE, Cairo 17 May 2026. Cash conversion cycle 7.8 days against 9.9 in "
    "1Q2025 — inventory 40.7 days (38.2), receivables 94.6 days (90.7), payables 127.4 days "
    "(119.0). Clients 52,541 of which 48,297 retail pharmacies. Market share 28.7%. Debt ratio "
    "16.6% from 24%. Interest expense to sales 2.3% from 3.6%. Operating cash flow POSITIVE "
    "EGP 477mn against negative EGP 1,512mn in 1Q2025. Non-pharma distribution EGP 1.5bn, +68%",
    "Ibnsina Pharma 1Q2026 Earnings Release, 17 May 2026", IR, "2026-05-17", url=ERQ126,
    fiscal_period="Q1-2026",
    model_impact="Gives the study year's first cash-conversion-cycle reading and shows how "
                 "violently it swings within a year — 7.8 days at 1Q, 15.2 days at 1H. The CCC "
                 "is therefore modelled QUARTERLY from its three legs, not annually from a "
                 "ratio, because the annual average hides a funding need that peaks mid-year.")

f_er25 = R.add(Ring.COMPANY, "IR communications (calls, presentations, releases)",
    FindingClass.D,
    "FY2025 EARNINGS RELEASE (2 March 2026) AND EARNINGS-CALL DECK (3 March 2026). FY2025: "
    "52,938 clients (48,514 retail pharmacies, 3,441 hospital, 983 wholesale), 72 sites at EGP "
    "1bn revenue each, 1,091 vehicles from 946, 9,731 employees from 8,970. Channel split of "
    "EGP 80bn gross: pharmacies 49.7% = 39.8bn (+36.3%), wholesale 31.0% = 24.8bn (+33.8%), "
    "tenders and hospitals 18.8% = 15bn (+52.2%), 3PL 0.5% (+59.0%). THE FULL CASH-CONVERSION-"
    "CYCLE SERIES BY QUARTER, DSO/DIO/DPO: 1Q24 88/32/118 = 2.0 days; 1H24 87/29/115 = 1.3; "
    "9M24 85/33/119 = 0.0; FY24 85/31/113 = 2.9; 1Q25 91/38/119 = 9.9; 1H25 90/38/115 = 13.5; "
    "9M25 90/37/116 = 10.7; FY25 90/35/118 = 6.7 — with the four named drivers of the cycle: "
    "UPA collection, importation inventory, the repricing effect on inventory, and a decrease "
    "in supplier credit terms. THE FY22-FY25 CASH BRIDGE: operating cash flow 843 / 1,056 / "
    "449 / 2,200; financial interest (482) / (930) / (1,375) / (2,271); net CFO 362 / 126 / "
    "(927) / (71); net capex (1,376) / (280) / (260) / (648); FCFF (641) / 567 / (120) / 1,041; "
    "net borrowings 1,412 / 766 / 917 / 1,005; FCFE 398 / 612 / (269) / 285 (EGP mn). Net debt "
    "EGP 5.5bn at end-2025 from a 1H25 peak of EGP 7.3bn; EGP 1.2bn of assets monetised. Capex "
    "EGP 684mn: distribution centres 460.6mn including Ramp's new warehouse (+40k pallet "
    "positions) and the Hassan Allam mega-warehouse (+29k, about 33% of total capacity), "
    "technology 97.7mn, vehicles 68.9mn, upgrades 55.3mn",
    "Ibnsina Pharma FY2025 Earnings Release, 2 March 2026, and FY2025 Investor Presentation / "
    "Business Review earnings call, 3 March 2026", IR, "2026-03-03", url=DECK25,
    fiscal_period="FY2025",
    model_impact="DRIVER UNLOCK for the cash conversion cycle as a DRIVER rather than a ratio: "
                 "ten dated observations of each of DSO, DIO and DPO, so each leg has its own "
                 "history, its own named causes and its own forecastable path. The FY22-FY25 "
                 "bridge is the reconciliation the DCF must reproduce: FCFF turned positive in "
                 "FY2025 for the first time since FY2023, and only because the cycle "
                 "contracted, not because margin improved.")

f_bod = R.add(Ring.COMPANY, "IR communications (calls, presentations, releases)", FindingClass.C,
    "The FY2025 Board of Directors' Report (2 March 2026) states management's top priority for "
    "the year was strengthening the financial position; that debt ratios peaked in 2Q2025 on "
    "the repricing and were reversed in the second half, aided by liquidating assets worth EGP "
    "1.2bn, the return of working-capital cycles to normal rates, disciplined inventory "
    "management and strong collection; and that the high interest-rate environment 'hinders the "
    "full translation of this growth into higher profitability levels'. Published alongside "
    "TCFD and ESG reports for 2025",
    "Ibnsina Pharma FY25 Board of Directors' Report", CO, "2026-03-02", url=BOD25)

# ---------------------------------------------------------------------------
# RING 4 — COMPANY — guidance, transactions, ownership, capital
# ---------------------------------------------------------------------------
f_guid = R.add(Ring.COMPANY, "strategic plans & guidance", FindingClass.D,
    "FY2026 GUIDANCE, from the company's own earnings-call deck. Gross revenue EGP 100,000mn "
    "against FY2025's 80,092mn, +25%; gross profit EGP 7,980mn at an 8.2% margin, +24%; EBITDA "
    "EGP 4,428mn at 4.5%, +14%; net profit EGP 1,500mn at 1.5%, +58%; SG&A EGP 3,252mn at 3.3% "
    "of sales, +877mn. STATED ASSUMPTIONS: market growth 15% split 11% ASP and 4% units; "
    "interest rates DOWN 4pp in FY2026; +EGP 300mn of non-core business profit; market share "
    "32.0%, up 1.8pp. Investment EGP 931mn (FY25 830mn, FY24 474mn). Capacity from 132 to 214 "
    "thousand cubic metres, +62%",
    "Ibnsina Pharma FY2025 Investor Presentation, '2026's Guidance' page, earnings call "
    "3 March 2026", IR, "2026-03-03", url=DECK25, fiscal_period="FY2025",
    model_impact="Guidance is an INPUT TO BE TESTED, never adopted. Each of its four "
                 "assumptions becomes an explicit driver with its own evidence: the rate cut is "
                 "contradicted by F05/F06 (four consecutive holds); the share is contradicted "
                 "by F16 (29.1% actual); the margin is contradicted by F23 (8.03% actual). The "
                 "study builds its own path and reports the distance to guidance rather than "
                 "inheriting it.")

f_gap = R.add(Ring.COMPANY, "strategic plans & guidance", FindingClass.S,
    "THE HALF-YEAR IS ALREADY BEHIND THE GUIDANCE ON EVERY LINE THAT MATTERS. Guidance / "
    "1H2026 actual: gross revenue EGP 100.0bn full year against EGP 43.2bn at the half, a "
    "run-rate of 86.4bn; gross margin 8.2% against 8.03%; EBITDA margin 4.5% against 4.2%; "
    "market share 32.0% against 29.1%. EBITDA itself FELL 3.1% year on year in the half. "
    "Management's own words: the 1H mix 'aligns with the 2026 gross margin guidance of 8.2%, "
    "which management expects to materialize in the coming quarters', and the 32% OPEX rise is "
    "'a one-time hike that is not expected to recur next year'",
    "Ibnsina Pharma 1H2026 Earnings Release, 12 August 2026, compared line by line against the "
    "FY2025 Investor Presentation's 2026 guidance page", IR, "2026-08-12", url=ERQ226,
    fiscal_period="Q2-2026",
    model_impact="Sets the base case BELOW guidance on all four legs and makes guidance the "
                 "upside frame. Specifically: revenue at the 1H run-rate plus normal seasonality "
                 "rather than +25%; gross margin starting at 8.03%; share at 29.1%; and the "
                 "OPEX step treated as PERMANENT unless the company's minimum-wage and social-"
                 "insurance compliance costs are shown to reverse, because a statutory wage "
                 "floor does not un-rise.")

f_mon = R.add(Ring.COMPANY, "one-off base-resetting transactions", FindingClass.B,
    "EGP 1.2bn OF ASSET MONETISATION IN 2025, AND IT IS IN FY2025 EARNINGS. The board (meetings "
    "153 and 154) approved and the company disclosed to EGX the sale of El Shorouk hospital "
    "(valuation disclosed 25 May 2025) and the El Haram building (valuations disclosed 29 June "
    "and 1 July 2025). The FY2025 accounts carry a gain from sale of fixed assets of EGP "
    "50,688,937 and a gain from sale of assets held for sale of EGP 20,821,694 — together 86.7% "
    "of the EGP 82,538,284 of other income — with EGP 127,000,000 and EGP 52,200,710 of "
    "proceeds in investing cash flow, and right-of-use disposals of EGP 666,205,981 against "
    "lease-liability disposals of EGP 613,921,396",
    "Ibnsina Pharma EGX disclosures of 25 May 2025, 29 June 2025 and 1 July 2025 via the IR "
    "News and Disclosures page; FY2025 audited consolidated financial statements notes 13, 17 "
    "and 27 and the cash flow statement", CO, "2026-03-01", url=FS25, is_fs_data=True,
    fiscal_period="FY2025",
    model_impact="BASE CHANGER, modelled as an explicit dated event and DUAL-FRAMED. It "
                 "flatters FY2025 three ways at once — other income, investing cash inflow, and "
                 "the deleveraging that produced the 18% debt ratio and 1.4x net debt/EBITDA "
                 "the equity story rests on. Underlying FY2025 net profit ex-disposal gains is "
                 "roughly EGP 881mn against the reported 952mn, and the FY2026 base is struck "
                 "on the underlying figure. Assets held for sale are down to EGP 105.5mn at "
                 "30 June 2026, so the monetisation lever is nearly spent.")

f_origin = R.add(Ring.COMPANY, "ownership / stake changes (named-transaction rule)",
    FindingClass.D,
    "A NAMED STAKE PURCHASE, SEARCHED AS THE SPECIFIC TRANSACTION. Ibnsina Pharma is acquiring "
    "28% of ORIGIN VENTURES (S.A.E.) for EGP 136,000,000. At 31 December 2025 EGP 40,000,000 "
    "had been paid on account and sat in current assets as 'financial investments advance "
    "payment' (note 9); by 30 June 2026 the balance is the full EGP 136,000,000. Separately the "
    "group holds four consolidated subsidiaries: AIM Healthcare Investments and Consultancy "
    "99.99%, Ramp Company for Logistic Services 99.99%, Digi 360 Software 90.50% and Ibn Sina "
    "Trade for Export 99.99%",
    "Ibn Sina Pharma FY2025 audited consolidated financial statements, note 1 and note 9, and "
    "the 2Q2026 statement of financial position", CO, "2026-03-01", url=FS25, is_fs_data=True,
    fiscal_period="FY2025",
    model_impact="A dated, named EGP 136mn cash outflow across FY2025-1H2026 that is an "
                 "INVESTMENT, not capex, and must not be absorbed into the maintenance-capex "
                 "rate. The 28% holding is below control and will be equity-accounted or held "
                 "at fair value, so it belongs in the equity bridge as a non-operating asset, "
                 "not in enterprise cash flow.")

f_own = R.add(Ring.COMPANY, "ownership / stake changes (named-transaction rule)", FindingClass.S,
    "SHAREHOLDER STRUCTURE, from the company's own disclosure: Abdel Gawad family 15.6%, Faisal "
    "Islamic Bank 14.0%, Mahgoub family 10.1%, C3 Capital Consortium 4.5%, free float 55.8% "
    "(sums to 100.0). The Disclosure Form on the board and shareholder structure was filed 6 "
    "October 2025 for the period ended 30 September 2025. THE INSIDER REGISTER SHOWS SUSTAINED "
    "SELLING IN 2026: related-party sells of 342,155 (12 Jan), 236,626 (13 Jan), 400,000 (14 "
    "Jan), 221,219 (15 Jan), 50,000 (18 Feb), 1,100,336 (12 Mar) and 400,000 + 300,000 + 50,000 "
    "(2 Apr), plus insider sells of 500,000 and 85,000 (5 Feb), 35,000 and 32,000 (8 Feb) and "
    "70,000 (20 May) against insider buys of only 18,360, 10,600, 20,000, 10,000 and 10,000",
    "Ibnsina Pharma IR Share & Corporate Information page and Insider Transactions register, "
    "read 8 September 2026; Disclosure Form of 6 October 2025", CO, "2026-09-08",
    url=f"{IRSITE}en/share-corporate-information-overview",
    detail="GAP STATED RATHER THAN PAPERED OVER: the insider register discloses type, volume "
           "and date but NOT the transacting party's name, so these lines cannot be attributed "
           "to a named holder and are not treated as a change in any disclosed stake. Faisal "
           "Islamic Bank appears on BOTH sides of the register — a 14.0% shareholder and a "
           "lender of EGP 74,908,778 under note 16 — which is a related-party exposure the "
           "study must disclose.",
    model_impact="Fixes the free float at 55.8% for the liquidity and control discussion, and "
                 "flags concentrated related-party selling through 2026 as a governance "
                 "observation that belongs in the risk section, not in the cash flows. No "
                 "driver is set from an unnamed insider line.")

f_cap = R.add(Ring.COMPANY, "management & capital actions", FindingClass.D,
    "SHARE COUNT AND THE PROFIT-SHARE DEDUCTION. 1,008,000,000 shares listed at EGP 0.25 par "
    "against issued and paid-up capital of EGP 252,000,000 — confirmed independently by the IR "
    "share page and by note 30, which uses a weighted average of 1,008,000,000. NOTE 30 ALSO "
    "SHOWS WHAT EPS IS STRUCK ON: employees' and board of directors' share of profit "
    "(estimated) of EGP 180,876,840 in FY2025 and EGP 116,766,846 in FY2024 is deducted before "
    "EPS — EXACTLY 19.0% of net profit in BOTH years. Dividends: EGP 0.16/share on FY2024 "
    "profit (ex 12 October 2025, paid 15 October 2025) and EGP 0.13/share on FY2025 profit (ex "
    "26 April 2026, paid 29 April 2026), with EGP 158mn of proposed distribution to board, "
    "employees and shareholders; cash dividends paid were EGP 201,038,137 in FY2025 and EGP "
    "25,620,772 in FY2024",
    "Ibn Sina Pharma FY2025 audited consolidated financial statements note 30 and the statement "
    "of changes in equity; IR Share & Corporate Information and Dividends pages",
    CO, "2026-03-01", url=FS25, is_fs_data=True, fiscal_period="FY2025",
    model_impact="Two things the equity bridge would otherwise miss. First, per-share values "
                 "divide by 1,008,000,000, not by the EGP 252mn capital figure an aggregator "
                 "would report. Second, 19.0% of net profit is contractually distributed to "
                 "employees and the board BEFORE anything reaches shareholders — a leakage that "
                 "held at exactly 19.0% in two consecutive years, so it is modelled as a rule "
                 "at 19% of net profit rather than ignored or averaged.")

f_aud = R.add(Ring.COMPANY, "management & capital actions", FindingClass.C,
    "AUDITOR CHANGED AND THE COMPANY'S OWN SITE HAS NOT CAUGHT UP. FY2022 and FY2023 were "
    "signed by Khaled Elghannam & Eissa Refaei & Co (register no. 6116, FRA register 192); "
    "FY2025 is signed by Ghorab & Co, Essam Ghorab (register no. 4393, FRA register 134). Both "
    "are Nexia International members. The IR Corporate Information page still names 'Khaled El "
    "Ghannam, Eissa Refai & Co.' as auditor when read on 8 September 2026, and the same page's "
    "quote panel still labels its earnings per share 'based on first quarter 2024'. Board and "
    "signatories are unchanged throughout: CFO Mo'men Gomaa, CEO Omar Abdul Gawad, Chairman "
    "Abd El Aziz Ali Abd El Aziz",
    "Ibn Sina Pharma FY2022, FY2023 and FY2025 auditors' reports; IR Company Profile page read "
    "8 September 2026", CO, "2026-09-08", url=FS23)

f_subs = R.add(Ring.COMPANY, "strategic plans & guidance", FindingClass.D,
    "THE DIVERSIFICATION LEG IS DISCLOSED AT SEGMENT LEVEL AND THE GAP IS FLAGGED. Revenue and "
    "NET PROFIT are given for three business units but no cost stack: Non-pharma FMCG "
    "Distribution (started 2021) revenue EGP 1,266mn FY23, 2,926mn FY24, 4,679mn FY25, net "
    "profit 59mn (2.0%) FY24 and 114mn (2.4%) FY25; Ibnsina Pharma's Scientific Office (2023) "
    "revenue 54 / 145 / 194mn, net profit 58mn (39.6%) FY24 and 71mn (36.3%) FY25; Ramp "
    "Logistics (2021) revenue 140 / 223 / 375mn, net profit 4mn (2.0%) FY24 and 35mn (9.2%) "
    "FY25. Together EGP 220mn, or 23.1% of FY2025 group net profit — which matches the "
    "company's own claim of '23% of net profit from non-core activities'. The board has since "
    "approved establishing two further subsidiaries, one for non-pharmaceutical distribution "
    "and trade and one for medical promotion, consulting, marketing, market studies and "
    "advertising",
    "Ibnsina Pharma FY2025 Investor Presentation, 'Subsidiaries & BUs' page; FY2025 and 1H2026 "
    "earnings releases", IR, "2026-03-03", url=DECK25, fiscal_period="FY2025",
    model_impact="Builds the diversification leg at SEGMENT level — revenue and net margin per "
                 "unit, projected separately — and FLAGS the gap explicitly: no cost of sales, "
                 "no opex and no capital employed is disclosed per unit, so the segment margins "
                 "are taken as given and cannot be built from cost per unit the way the core "
                 "distribution business can. The Scientific Office's 36-40% net margin on EGP "
                 "194mn is the highest-margin line in the group and the smallest; it is "
                 "modelled but never extrapolated.")

# ---------------------------------------------------------------------------
# NEGATIVE SEARCHES — every one actually run, on the dates shown
# ---------------------------------------------------------------------------
n_margin = R.add_negative(Ring.COUNTRY,
    "regulatory environment (regulator, caps, tariffs, tax/subsidy)",
    "searched: 'Egyptian Drug Authority drug pricing decree 2025 repricing distributor margin "
    "pharmacy margin percentage' and 'Egypt pharmaceutical distributor margin regulated 8.5% "
    "wholesale margin decree Ministry of Health' — the EXISTENCE of mandatory distributor and "
    "pharmacist margins under Minister of Health Decree 499/2012 is confirmed by two "
    "independent legal sources, but THE DECREE'S OWN SCHEDULE OF DISTRIBUTOR MARGIN "
    "PERCENTAGES COULD NOT BE OBTAINED in English or Arabic. The pharmacy-side discounts "
    "(20->23%, 25->27%, imported 15-20%) are reported; the distributor's own percentage is not. "
    "Consequence: the spread is inferred from the filed cost stack (F24) rather than read off "
    "the decree, and that is stated wherever the spread is quoted",
    SWEEP_DATE)

n_epharm = R.add_negative(Ring.INDUSTRY, "technology substitution",
    "searched: 'Egypt drug track and trace system EDA 2026 e-pharmacy online pharmacy "
    "regulation direct-to-pharmacy distribution disintermediation' — returned the EDA "
    "serialisation programme and nothing else. NO licensed e-pharmacy channel, no "
    "manufacturer direct-to-pharmacy scheme and no third-party marketplace that bypasses the "
    "distributor surfaced for Egypt. The live substitution threat is a customer integrating "
    "backwards (F14, Ezaby), not a technology replacing the channel",
    SWEEP_DATE)

n_peers = R.add_negative(Ring.INDUSTRY, "competitor capacity / price moves (named)",
    "searched: 'Egypt largest pharmaceutical distributors named Pharma Overseas Ibnsina Pharma "
    "Multipharma UCP wholesale drug distribution companies Egypt 2026' and 'Pharma Overseas "
    "Egypt distributor market share 2025 revenue second largest competitor Ibnsina' — NO "
    "published financial statements, revenue, margin or capacity figures exist for any named "
    "private Egyptian pharmaceutical distributor. None is listed. IQVIA share data reaches the "
    "public record only through ISPH's own releases, i.e. only for ISPH itself. Consequence: "
    "there is no peer set for a relative-multiple lens on distribution economics and no "
    "competitor cost curve; the competitive read rests on ISPH's own share series (F16)",
    SWEEP_DATE)

n_drop = R.add_negative(Ring.COMPANY, "regular disclosures",
    "searched the IR Results Center, the FY2025 earnings-call deck, all earnings releases from "
    "FY2023 to 1H2026, the FY25 board report and the sustainability/ESG reports for: deliveries "
    "per day, orders per client, drop frequency, delivery frequency, order lines, drop size, "
    "and ISPH's OWN unit/box volumes. NONE IS DISCLOSED. Client counts, site counts, vehicle "
    "counts, headcount and revenue-per-unit ratios are given; the transaction counts behind "
    "them are not, and neither is ISPH's own pack volume — only the MARKET's units from IQVIA. "
    "Consequence: drop frequency cannot be a driver, and the volume leg is built as market "
    "units x ISPH share rather than from the company's own pack count",
    SWEEP_DATE)

n_deck = R.add_negative(Ring.COMPANY, "IR communications (calls, presentations, releases)",
    "searched the IR Presentations and Publications page and the IR Calendar on 8 September "
    "2026 for a 1Q2026 or 1H2026 investor presentation, earnings-call deck or call transcript. "
    "NONE EXISTS — the most recent deck is FY2025 (3 March 2026), and the IR Calendar reads "
    "'There are currently no events'. No transcript of any call is published in any period. "
    "Consequence: the study year's quarters are covered by their statements and releases only, "
    "and no 2026 management commentary beyond the releases is available",
    SWEEP_DATE)

n_dual = R.add_negative(Ring.COMPANY, "management & capital actions",
    "searched the IR Listing Information and Share & Corporate Information pages for a second "
    "listing, GDR, ADR or depositary programme. NONE. ISPH is listed on the Egyptian Exchange "
    "ONLY, ticker ISPH.CA, ISIN EGS512O1C012, quoted in EGP, listed 8 November 2017, "
    "1,008,000,000 shares at EGP 0.25 par. Verified against the repo's own series "
    "engine/raw_ohlc/EG/ISPH.csv, which closes at EGP 13.220 on 23 August 2026 against the IR "
    "page's live EGP 13.18 on 8 September 2026 — same currency, same magnitude, one exchange. "
    "The dual-listing trap does not apply here and the regressor is unambiguous: EGX30 via "
    "engine/raw_indices/EG/EGX30.csv, through own_stock_beta() and never a composite",
    SWEEP_DATE)

n_fuel = R.add_negative(Ring.GLOBAL, "commodity complex (input/output)",
    "searched the FY2022-FY2025 audited statements and the 1Q/2Q2026 interims for a disclosed "
    "fuel, diesel or energy cost line. NONE IS BROKEN OUT. The nearest disclosures are "
    "'logistics' inside cost of sales (EGP 111,851,760 in FY2025, note 24) and "
    "'salaries, travel and transportation expenses' inside selling and marketing (EGP "
    "1,153,657,636, note 25), neither of which separates fuel from wages. Consequence: the "
    "fuel escalator is applied to a DERIVED transport cost base, and the derivation is "
    "flagged rather than presented as a disclosed figure",
    SWEEP_DATE)

# ---------------------------------------------------------------------------
# DRIVER GATE TABLE — every driver, mode earned, finest sourced level
# ---------------------------------------------------------------------------
R.add_driver("Gross revenue by channel (retail pharmacies / wholesale / tenders & private "
             "hospitals / 3PL & other)", DriverMode.BOTTOM_UP,
    "Four channels, each with its own disclosed revenue, growth rate and share of the top "
    "line for FY2024, FY2025, 1Q2026 and 1H2026, tied back to the audited revenue note. Each "
    "channel carries its own price path, its own receivable term and its own margin, because "
    "hospitals and non-pharma 'are not eligible for the fixed retail margin' in the company's "
    "own words. This is the finest level the disclosure reaches on the revenue side.",
    [f_er226, f_er25, f_costs, f_fs25])

R.add_driver("Volume — packs sold (market units x ISPH share)", DriverMode.BOTTOM_UP,
    "Market units are disclosed by year and half (3.5bn FY23, 3.4bn FY24, 3.72bn FY25, 1,700mn "
    "1H26) alongside ISPH's IQVIA share, so the volume leg is built rather than assumed. GAP "
    "FLAGGED EXPLICITLY: ISPH does not disclose its OWN pack count anywhere (negative search "
    "F42), so the build is market units x share and the residual error sits in the share leg, "
    "which is stated wherever a volume number is quoted.",
    [f_mkt, f_share, n_drop])

R.add_driver("Price — average selling price per pack", DriverMode.BOTTOM_UP,
    "The company discloses its own realised price per box (EGP 65 end-2023 to EGP 114 in 2025) "
    "and the market's ASP series (58 / 86 / 110 / 126), and decomposes its own FY2026 growth "
    "assumption into 11% price and 4% volume. Price and volume are therefore projected "
    "SEPARATELY, which is what makes the September 2026 pricing overhaul modellable at all.",
    [f_price, f_mkt, f_reprice26])

R.add_driver("Cost of goods per pack — and therefore the gross spread as an OUTPUT",
    DriverMode.BOTTOM_UP,
    "Note 24 gives purchase cost of pharmaceuticals and cosmetics at EGP 69,869,668,630, 99.60% "
    "of cost of sales, against note 23's revenue by line. Cost per pack divides straight out, "
    "and gross profit is (price per pack - cost per pack) x packs. NO MARGIN IS AN INPUT "
    "ANYWHERE IN THIS MODEL. The regulated spread constrains the answer; it does not supply it.",
    [f_costs, f_fs25, f_decree])

R.add_driver("Distribution cost stack — warehousing, fleet, salaries, technology",
    DriverMode.BOTTOM_UP,
    "Every line of notes 24, 25 and 26 is disclosed and each is attached to its own physical "
    "driver: rent and storage to pallet positions (88k to 157k by end-2026), transport to the "
    "vehicle count (946 / 1,091 / 1,154), salaries to headcount (8,970 / 9,731 / 10,081), "
    "technology to the disclosed technology capex. One escalator per driver, never a blended "
    "inflation rate; the fuel leg escalates on the March 2026 pricing decision.",
    [f_costs, f_er226, f_er25, f_fuel, n_fuel])

R.add_driver("Days sales outstanding (DSO)", DriverMode.BOTTOM_UP,
    "Ten dated disclosed observations (88 / 87 / 85 / 85 / 91 / 90 / 90 / 90 by quarter through "
    "FY2025, then 94.6 at 1Q26 and 94.5 at 1H26) against the audited receivables note, split by "
    "channel because the hospital and tender channel is on state payment terms and the UPA's "
    "arrears are a named, dated cause.",
    [f_er25, f_er126, f_er226, f_wc, f_upa])

R.add_driver("Inventory days (DIO)", DriverMode.BOTTOM_UP,
    "Disclosed series 32 / 29 / 33 / 31 / 38 / 38 / 37 / 35, then 40.7 at 1Q26 and 42.9 at "
    "1H26, against note 7's composition (goods for sale, goods in transit, returns, spares). "
    "The rise is a stated policy response to regional supply risk, so it unwinds slowly and on "
    "evidence rather than reverting to the mean.",
    [f_er25, f_er226, f_wc, f_supply])

R.add_driver("Days payable outstanding (DPO)", DriverMode.BOTTOM_UP,
    "Disclosed series 118 / 115 / 119 / 113 / 119 / 115 / 116 / 118, then 127.4 at 1Q26 and "
    "122.2 at 1H26, against note 19's split of suppliers EGP 6,016mn versus NOTES PAYABLE EGP "
    "19,459mn. Three quarters of the payable is a dated bill, so DPO is contractual and its "
    "movement is explained by supplier mix (longer-facility hospital suppliers versus shorter-"
    "facility suppliers) rather than by stretching.",
    [f_er25, f_er126, f_wc])

R.add_driver("Cash conversion cycle (days) — modelled as a driver, not reported as a ratio",
    DriverMode.BOTTOM_UP,
    "DIO + DSO - DPO built quarterly from the three legs above, each with its own history and "
    "its own named causes (UPA collection, importation inventory, the repricing effect on "
    "inventory, supplier credit terms). The disclosed CCC series is 2.0 / 1.3 / 0.0 / 2.9 / 9.9 "
    "/ 13.5 / 10.7 / 6.7 / 7.8 / 15.2 days — a range that swings by 15 days inside eighteen "
    "months, which is exactly why an annual average would hide the funding peak.",
    [f_er25, f_er126, f_er226, f_wc])

R.add_driver("Interest cost of financing the cycle", DriverMode.BOTTOM_UP,
    "Built facility by facility from note 16's five NAMED loans with their limits and "
    "maturities (EBRD EGP 800mn to Dec 2030, First Abu Dhabi Misr, Faisal Islamic, NBE, Credit "
    "Agricole), plus note 18's credit facilities (EGP 5,169.6mn at FY25 to 7,532.2mn at 1H26) "
    "priced off the CBE lending rate the company's own note 35 tracks, plus note 17's lease "
    "finance charge of EGP 284.4mn. SAME-CLASS PRIOR APPLIED: engine/Fundamental_Driver_Ledger."
    "md's GBCO entry of 07-09-2026 records that a finance cost built as a ratio to revenue "
    "carries a funding shock forward for years and loses to a freeze at four of five horizons; "
    "the correct denominator is the borrowings that actually bear interest. That is what is "
    "built here.",
    [f_wc, f_cbe, f_fs25, f_q226])

R.add_driver("Discounts — the gross-to-net bridge", DriverMode.BOTTOM_UP,
    "Disclosed for three periods: 3.57% of gross in FY2024, 4.36% in FY2025, 3.94% in 1H2026, "
    "with the company naming the trade-off ('targeting cash segments implies more cash "
    "discounts, however it allows liquidity in a high interest rate environment'). Modelled "
    "against the DSO and interest drivers as one decision, not as an independent percentage.",
    [f_grossnet, f_er226, f_fs25])

R.add_driver("Employees' and board of directors' profit share", DriverMode.BOTTOM_UP,
    "Note 30 discloses EGP 180,876,840 for FY2025 and EGP 116,766,846 for FY2024 — exactly "
    "19.0% of net profit in both years. Modelled as a 19% rule on net profit and deducted "
    "before anything reaches shareholders, because that is how the company's own EPS is struck.",
    [f_cap, f_fs25])

R.add_driver("Capex and warehouse capacity", DriverMode.BOTTOM_UP,
    "Disclosed by category for two years: FY2025 EGP 684mn (distribution centres 460.6, "
    "technology 97.7, vehicles 68.9, upgrades 55.3) and 1H2026 EGP 579mn (74 / 10 / 10 / 4 per "
    "cent), against a capacity path of 88k to 157k pallet positions and 132 to 214 thousand "
    "cubic metres and an FY2026 investment plan of EGP 931mn. Capex is built off the capacity "
    "the company says it is adding, not off a percentage of revenue.",
    [f_er226, f_er25, f_guid])

R.add_driver("Fleet size and cost per vehicle", DriverMode.BOTTOM_UP,
    "946 vehicles at FY2024, 1,091 at FY2025, 1,154 at 1H2026, with revenue per vehicle "
    "disclosed alongside; vehicle capex disclosed separately (EGP 68.9mn FY25, EGP 57.6mn "
    "1H26); running cost escalated on the March 2026 fuel decision rather than on CPI.",
    [f_er226, f_er25, f_fuel])

R.add_driver("Tax", DriverMode.BOTTOM_UP,
    "22.50% statutory rate, confirmed inside the company's own deferred-tax table where every "
    "temporary difference is measured at 22.50%, with the deferred balance rolled on the lease "
    "and ECL differences note 29 itemises. The FY2025 effective rate of 11.6% is a deferred "
    "credit and is NOT projected.",
    [f_tax, f_fs25])

R.add_driver("Non-core segments — non-pharma FMCG, Scientific Office, Ramp Logistics",
    DriverMode.BOTTOM_UP,
    "Built at SEGMENT level: revenue and net profit are disclosed per unit for FY2023-FY2025. "
    "GAP FLAGGED: no cost of sales, no opex and no capital employed is disclosed per unit, so "
    "these three margins are taken as disclosed and cannot be built from cost per unit the way "
    "the core business is. That is a coarser level than the rest of the model and it is said "
    "so here rather than left to be discovered.",
    [f_subs, f_er25])

R.add_driver("Market share", DriverMode.TOP_DOWN,
    "There is no bottom-up route to share. No named Egyptian distributor publishes financials, "
    "capacity or pricing, none is listed, and IQVIA's data reaches the public record only "
    "through ISPH's own releases — so no competitor volume can be built and share cannot be "
    "derived as one-minus-the-others. The negative search F41 is what forces this driver "
    "top-down. Set at the 1H2026 actual of 29.1% held flat, with the company's 32.0% guidance "
    "as the upside frame and the Ezaby reclassification footnoted wherever share is quoted.",
    [n_peers, f_share, f_ezaby])

R.add_driver("Drop frequency / deliveries per client", DriverMode.TOP_DOWN,
    "Cannot be built at all. The negative search F42 records that no delivery-frequency, order-"
    "count or drop-size figure exists in any company document. Revenue per client (EGP 43.2bn "
    "gross over 52,736 clients in 1H2026) is the only observable, so service intensity is "
    "carried as a top-down ratio and its absence is disclosed rather than filled with an "
    "estimate.",
    [n_drop, f_er226])

# ---------------------------------------------------------------------------
# OUTPUT
# ---------------------------------------------------------------------------
errors, warnings = R.validate()
R.to_json(os.path.join(HERE, 'sweep_register.json'))
print(R.qc_line())
print(f"\nfindings: {len(R.findings)} | drivers: {len(R.drivers)}")
print(f"rings closed: {len(set(f.ring for f in R.findings))}/4 | "
      f"primary-access attempts: {len(R.primary_access)} "
      f"({sum(1 for p in R.primary_access if p.reachable)} reachable, "
      f"{sum(1 for p in R.primary_access if not p.reachable)} blocked)")
if errors:
    print(f"\nVALIDATOR ERRORS ({len(errors)}) — disclosed, not suppressed:")
    for e in errors:
        print(f"  ! {e}")
else:
    print("\nVALIDATOR ERRORS: none")
if warnings:
    print(f"\nwarnings ({len(warnings)}):")
    for w in warnings:
        print(f"  - {w}")
else:
    print("warnings: none")
fresh = R.check_freshness(SWEEP_DATE)
print(f"\nfreshness (delivery {SWEEP_DATE}): {fresh or 'OK — sweep and delivery same day'}")
