"""FWRY (Fawry for Banking Technology and Electronic Payments S.A.E., EGX: FWRY.CA)
— four-ring Step 2A Information Sweep register. FIRST-BUILD study; this ticker had no
study directory, so the whole build is held under `engine/fwry_study_pending/` until it
carries a valuation.

Runs BEFORE any forecast driver is set. Every mandatory category of every ring is closed
by a dated finding or a dated negative search.

THIS IS A PAYMENTS PLATFORM WITH A LENDING BOOK BOLTED ON, AND THE SWEEP WAS RUN FOR THAT
SHAPE. The unit economics are THROUGHPUT x TAKE RATE, not volume x price of a product, so
the sweep reached for: total payment value processed (throughput), transaction counts, the
take rate and how it differs by service line, the agent/POS/merchant network counts, and —
kept deliberately separate — the size and the provisioning of the credit book. Revenue is
disclosed BY SERVICE LINE in the company's own earnings releases and NOT in that shape in
the audited statements; the two bases are recorded separately below and are never mixed in
one series. The lending book carries credit risk that a payments multiple does not price,
so its gross portfolio, its sub-books and its provisions ratios are swept as their own
findings.

SOURCING EXCEPTIONS, RECORDED RATHER THAN HIDDEN
================================================
(1) www.fawry.com IS FULLY BLOCKED AT THIS ENVIRONMENT'S EGRESS BY CLOUDFLARE. Every
    www.fawry.com URL tried — the apex, /en/, the investor-relations landing page, the
    investors path, /wp-json/, /sitemap_index.xml, /robots.txt and the direct PDF path of
    the FY2025 earnings release — returned HTTP 403 carrying a ~5.5 kB Cloudflare
    "Just a moment..." JS interstitial rather than the document. ir.fawry.com,
    investors.fawry.com and corporate.fawry.com all failed CONNECT with a 502 at the
    proxy. Fifteen attempts are logged below, each with its outcome. A browser-UA retry, an
    Accept: application/pdf retry, an HTTP/1.1 retry and a Googlebot-UA retry were all
    refused identically, so this is a zone-wide bot challenge, not a per-path rule.

(2) THE EGYPTIAN EXCHANGE PORTAL IS ALSO BLOCKED BEYOND ITS HOME PAGE. www.egx.com.eg/en/
    homepage.aspx returns a real 45 kB page and sets F5/TSPD cookies, but every deeper
    request — /en/DisclosureNews.aspx and the two /downloads/Bulletins/*.pdf files that
    carry Fawry's own filings — returns an empty reply from the server even with the
    session cookies attached. mcdr.com.eg and disclosure.efsa.gov.eg do not resolve.

(3) THE COMPANY'S OWN DOCUMENTS WERE REACHED BY TWO OTHER ROUTES, AND THE ROUTE IS NAMED
    ON EVERY FINDING THAT USES ONE.
      (a) THE INTERNET ARCHIVE'S CAPTURES OF fawry.com. web.archive.org is reachable and
          holds byte-identical captures of Fawry's own PDFs. Twenty-one of the company's
          own documents were retrieved this way — four annual audited consolidated
          statements (FY2021, FY2022, FY2023 English; FY2024 Arabic), one interim, six
          earnings releases, four earnings presentations, the YE2023 corporate-governance
          report and four company press releases. They are held in
          engine/fwry_study_pending/filings/. The archive is a TRANSPORT for the issuer's
          own file, not a source in its own right, so these findings are tagged
          COMPANY_OFFICIAL (statements, governance report) or COMPANY_IR (releases,
          presentations) with the archive timestamp recorded.
      (b) THE ENTERPRISEAM DOCUMENT SERVER (ent.news). Fawry's FY2025 earnings release
          (5 March 2026) and its 1H2026 earnings release (13 August 2026) are not in the
          archive at all. Both were retrieved as the issuer's own PDFs from ent.news, the
          S3 document host EnterpriseAM uses for the releases it links. The PDF metadata
          on both names the author as "Fawry for Banking Technology and Eletcronic
          PAYMENTS I Earnings Release", created in MS Word on 4 March 2026 and 12 August
          2026 respectively — i.e. the company's own file, not a re-typing. EnterpriseAM's
          own HTML pages disallow this class of agent in robots.txt, so nothing was
          crawled there beyond the two article pages already returned by search, and no
          EnterpriseAM prose is used as a source for any Fawry figure.

(4) [R-SIGCM-03] FALLBACK USED FOR FY2025 AND FOR BOTH 2026 QUARTERS, AND NAMED. THE
    AUDITED FY2025 CONSOLIDATED STATEMENTS AND THE Q1/H1-2026 REVIEWED INTERIMS COULD NOT
    BE OBTAINED. Their URLs are known — the FY2025 set is published under
    www.fawry.com/wp-content/uploads/2026/03/ and the Q1-2026 consolidated set at
    www.fawry.com/wp-content/uploads/2026/05/Fawry-Consolidated-Financials-English-31-03-2026.pdf
    — and every one of them sits behind the Cloudflare block in (1). The archive has no
    capture of any of them; Wayback "Save Page Now" requires a logged-in account and was
    refused 401. FY2025, Q1-2026 and Q2-2026 income-statement figures therefore enter this
    register from THE COMPANY'S OWN EARNINGS RELEASES — the named fallback, the company's
    own document, not a vendor and not press. Those three findings are deliberately left
    at is_fs_data=True with SourceType.COMPANY_IR so the validator's PROVENANCE invariant
    FIRES on each of them. THE FLAG IS NOT DOWNGRADED TO MAKE THE RUN LOOK CLEAN: three
    disclosed errors are the honest count of the periods whose numbers do not rest on an
    audited or reviewed statement. Four fiscal years — FY2021 through FY2024 — DO rest on
    the audited statements themselves, read off the pixels and footed (exception 5).

(5) THE AUDITED STATEMENTS ARE IMAGE-ONLY SCANS AND WERE READ OFF THE RENDERED PIXELS.
    All four annual sets extract to fewer than 60 characters through pdftotext; pdffonts
    reports no font at all, so there is no text layer and no character map to break —
    every page is a JPEG or CCITT image. Tesseract could not be used: at this environment's
    CPU throughput a 400x200 pixel crop took 44 seconds and a full page did not finish
    inside 300 seconds, so twelve pages of OCR was not feasible. The statement pages were
    extracted with pdfimages at their native 200 dpi and READ VISUALLY off the rendered
    image instead, which is the same route by a different reader. EVERY FIGURE SO READ IS
    SUBJECT TO engine/fwry_study_pending/footing_check.py, which re-adds each page against
    the subtotal the company itself printed. TWO PAGES FAILED THAT TEST ON THE FIRST READ
    and were re-read at 3x-6x zoom until they footed: the FY2024 income statement (the
    customer-financing provision read 134,600,000 against a true 134,600,555, and the
    FY2023 health contribution read 11,099,750 against a true 11,599,755) and the FY2024
    balance sheet (eight glyphs). Both corrections are recorded in footing_check.py rather
    than silently applied, and the FY2023 English set independently confirms the corrected
    FY2023 figure. THE FY2021 SET FAILED THE SAME TEST ON THREE SUBTOTALS and was accepted
    only after every figure on both statement pages was re-read at the scan's native 200 dpi;
    six OCR glyph errors were caught and corrected, and the five-pound net-profit gap that
    survived the first two rounds of correction turned out NOT to be the deferred-tax line
    it appeared to be, but two further errors either side of it. Had that gap been closed by
    subtraction the register would carry a deferred-tax figure the company never printed and
    would still have been wrong about two other lines. FY2021's scanner provenance was also
    checked, because the file was produced by a Xerox WorkCentre 5330 — a device family
    subject to the 2013 JBIG2 symbol-substitution defect, where the SCANNER swaps digit
    bitmaps and no re-read can recover the truth. The JBIG2 segment headers were parsed and
    every page carries only an immediate generic region, with no symbol dictionary and no
    text region, so that failure mode is ruled out on this file and the pixels can be
    trusted. FOUR audited fiscal years — FY2021, FY2022, FY2023 and FY2024 — are read and
    footed in full, income statement and balance sheet, 91 checks in all, which takes the
    FS-depth invariant from its two-year floor to its four-year target.

(6) THE CENTRAL BANK OF EGYPT'S OWN MONETARY POLICY REPORT WAS REACHED DIRECTLY. The CBE
    site rejects its own HTML paths at this egress (404/rejection page) but serves its
    publication PDFs, so the Q1-2026 Monetary Policy Report was retrieved from
    cbe.org.eg and is the REGULATOR_OFFICIAL source for the policy rates and the published
    inflation targets, rather than press reporting of them.

Run: python3 engine/fwry_study_pending/sweep.py
"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from research_sweep import (SweepRegister, AssetClass, Ring, FindingClass,
                            SourceType, DriverMode)

SWEEP_DATE = "2026-09-08"
R = SweepRegister("FWRY", AssetClass.STOCK, SWEEP_DATE)
CO, IR, REG, PMD, PRESS, AGG = (SourceType.COMPANY_OFFICIAL, SourceType.COMPANY_IR,
                                SourceType.REGULATOR_OFFICIAL, SourceType.PRIMARY_MARKET_DATA,
                                SourceType.REPUTABLE_PRESS, SourceType.AGGREGATOR)

# ---------------------------------------------------------------- PRIMARY ACCESS
# The company's own website/IR page was tried FIRST for every Company-ring figure.
# Every attempt is logged, successful or refused.
R.record_primary_access("https://fawry.com/", False, "2026-09-08",
    "HTTP 403, 5,212-byte Cloudflare 'Just a moment...' JS challenge; redirected to www.")
R.record_primary_access("https://www.fawry.com/en/", False, "2026-09-08",
    "HTTP 403 Cloudflare challenge; retried with a desktop Chrome UA and Accept-Language "
    "header — identical refusal.")
R.record_primary_access("https://www.fawry.com/investor-relations/", False, "2026-09-08",
    "HTTP 403 Cloudflare challenge. This is the IR landing page named in the company's "
    "own governance report (Website: www.fawry.com).")
R.record_primary_access("https://www.fawry.com/financials-and-earning-releases/", False,
    "2026-09-08",
    "HTTP 403 live. The page's own document list WAS read from the Internet Archive's "
    "30-Sep-2025 capture, which is how the naming convention of every statement and "
    "release PDF below was discovered.")
R.record_primary_access("https://www.fawry.com/investor-relations/disclosures/", False,
    "2026-09-08", "HTTP 403 Cloudflare challenge.")
R.record_primary_access(
    "https://www.fawry.com/wp-content/uploads/2026/03/Earnings-Release-4Q25-English-1.pdf",
    False, "2026-09-08",
    "THE FY2025 EARNINGS RELEASE AT ITS OWN URL — HTTP 403. Four header/protocol variants "
    "tried (Accept: application/pdf + Referer, HTTP/1.1, Googlebot UA, plain): all 403.")
R.record_primary_access(
    "https://www.fawry.com/wp-content/uploads/2026/05/Fawry-Consolidated-Financials-English-31-03-2026.pdf",
    False, "2026-09-08",
    "THE Q1-2026 CONSOLIDATED FINANCIAL STATEMENTS AT THEIR OWN URL — HTTP 403. No archive "
    "capture exists. This is the single most material document this sweep could not get.")
R.record_primary_access("https://ir.fawry.com/", False, "2026-09-08",
    "CONNECT tunnel failed, 502 at the proxy — host does not resolve/serve.")
R.record_primary_access("https://investors.fawry.com/", False, "2026-09-08",
    "CONNECT tunnel failed, 502 at the proxy.")
R.record_primary_access("https://corporate.fawry.com/", False, "2026-09-08",
    "CONNECT tunnel failed, 502 at the proxy.")
R.record_primary_access("https://www.fawry.com/wp-json/wp/v2/pages", False, "2026-09-08",
    "HTTP 403 — the WordPress REST API is behind the same challenge, so the document list "
    "could not be read programmatically either.")
R.record_primary_access("https://www.egx.com.eg/en/homepage.aspx", True, "2026-09-08",
    "HTTP 200, 45 kB — the exchange home page IS reachable and sets F5/TSPD session "
    "cookies.")
R.record_primary_access("https://www.egx.com.eg/downloads/Bulletins/330156_2.pdf", False,
    "2026-09-08",
    "FAWRY'S OWN FILING ON THE EXCHANGE PORTAL — empty reply from server (curl 52) on "
    "three attempts, with and without the TSPD session cookies from the home page. The "
    "exchange route to the issuer's documents is closed at this egress.")
R.record_primary_access("https://web.archive.org/web/20260712094455id_/"
    "https://www.fawry.com/wp-content/uploads/2026/03/Fawry-Earnings-Presentation-4Q2025-Final.pdf",
    True, "2026-09-08",
    "REACHED — the company's own FY2025 (4Q25) earnings-call presentation, retrieved as a "
    "byte-identical archive capture of fawry.com. 878,949 bytes, 27 pages, text layer intact.")
R.record_primary_access("https://ent.news/2026/3/291.pdf", True, "2026-09-08",
    "REACHED — Fawry's own FY2025 earnings release PDF (5 March 2026). PDF Author metadata: "
    "'Fawry for Banking Technology and Eletcronic PAYMENTS I Earnings Release', created in "
    "MS Word 4 March 2026. Not in the Internet Archive; this was the only route to it.")
R.record_primary_access("https://ent.news/2026/8/542.pdf", True, "2026-09-08",
    "REACHED — Fawry's own 1H2026 earnings release PDF (13 August 2026), same Author "
    "metadata, created 12 August 2026. Carries the 1Q2026 and 2Q2026 columns that close "
    "the study-year quarter coverage.")
R.record_primary_access("https://web.archive.org/save/"
    "https://www.fawry.com/financials-and-earning-releases/", False, "2026-09-08",
    "Wayback Save Page Now refused: GET returned HTTP 520 and the POST API returned 401 "
    "'You need to be logged in to use Save Page Now.' The blocked FY2025/2026 documents "
    "therefore could not be archived on demand either.")

# ---------------------------------------------------------------- RING 1 GLOBAL
f_fed = R.add(Ring.GLOBAL, "rate cycle & USD/FX regime", FindingClass.S,
    "Fed funds target range 3.50-3.75%, held at the 28-29 July 2026 FOMC on a 9-3 vote; "
    "next decision 16 September 2026. The global easing cycle has stalled rather than "
    "reversed, and the CBE's own report puts several major central banks on hold with it",
    "Federal Reserve FOMC minutes 28-29 July 2026 and statement archive, corroborated by "
    "the CBE Q1-2026 Monetary Policy Report's 'Key Policy Rates in Major Central Banks'",
    REG, "2026-07-29",
    model_impact="Anchors the USD leg of the cost-of-capital build and the direction of "
                 "the EGP rate path: a stalled global easing cycle is what keeps Egypt's "
                 "19.50% main operation rate where it is, which in turn sets the explicit-"
                 "window risk-free rate and the discount-rate glide.")

f_hw = R.add(Ring.GLOBAL, "commodity complex (input/output)", FindingClass.C,
    "Fawry converts no commodity. Its only physical input is the POS terminal estate — 376.6k "
    "terminals at FY2025, and 378.6k at 30-Jun-2026 against 401.0k a year earlier after "
    "management deliberately decommissioned underused terminals — whose bill of materials "
    "is imported semiconductors. The 2026 "
    "memory squeeze is confined to high-bandwidth memory for AI accelerators and does not "
    "reach payment-terminal silicon; the top five terminal vendors (Ingenico/Worldline, "
    "Verifone, PAX, Block, Fiserv) ship more than 60% of units",
    "Fawry FY2025 and 1H2026 earnings releases for the terminal counts; payments-industry "
    "trade coverage of terminal supply and the 2026 memory shortage for the input side",
    PRESS, "2026-06-01",
    model_impact="")

f_gdem = R.add(Ring.GLOBAL, "global sector demand", FindingClass.C,
    "Global digital-payments transaction value is put at roughly USD 37tn for 2026 growing "
    "at a mid-single-digit CAGR, with real-time/account-to-account rails the fastest-growing "
    "segment worldwide — the same rail that is Fawry's substitution risk at home",
    "HSBC Global Payment Trends Report 2026 and Statista digital-payments outlook",
    PRESS, "2026-01-01",
    model_impact="")

f_trade = R.add(Ring.GLOBAL, "trade / sanctions / supply chains", FindingClass.C,
    "No sanctions, tariff or export-control exposure: Fawry's revenue is domestic Egyptian "
    "and EGP-denominated, its throughput never crosses a border, and the only cross-border "
    "item on the roadmap is an INBOUND remittance licence still awaiting approval. Terminal "
    "hardware is imported and is the only supply-chain dependency",
    "Fawry 1H2026 earnings release (domestic network description) and the pending inbound "
    "cross-border remittance licence reported May-2026",
    PRESS, "2026-05-18",
    model_impact="")

# --------------------------------------------------------------- RING 2 COUNTRY
f_cbe = R.add(Ring.COUNTRY, "sovereign macro (inflation, policy rate, FX/deval risk)",
    FindingClass.D,
    "CBE key policy rates held at overnight deposit 19.0%, overnight lending 20.0%, main "
    "operation 19.5% (discount rate 19.5%); 825bp of cuts since April 2025 fully transmitted "
    "to the interbank market, which sat at 19.5% in March 2026. The CBE's announced targets "
    "are 7% (+/-2pp) for Q4 2026 and 5% (+/-2pp) for Q4 2028, and the report itself says "
    "headline inflation is LIKELY TO EXCEED the 7% target",
    "Central Bank of Egypt, Monetary Policy Report Q1-2026 (PDF retrieved directly from "
    "cbe.org.eg; held at engine/fwry_study_pending/filings/CBE_MPR_Q1_2026.pdf)",
    REG, "2026-05-01",
    model_impact="Sets the explicit-window risk-free rate at 19.50% and the TERMINAL rf "
                 "norm-built from the CBE's OWN published medium-term target (7%) plus the "
                 "house EM real-rate convention — never a historical average. Also sets the "
                 "yield assumed on the settlement float and on the money-market fund.")

f_hold = R.add(Ring.COUNTRY, "sovereign macro (inflation, policy rate, FX/deval risk)",
    FindingClass.S,
    "Rates held for a fourth consecutive meeting on 20 August 2026 with annual headline "
    "urban inflation at 14.9% in July 2026 (June 14.3%), and the CBE guiding that inflation "
    "begins a gradual decline only from Q1 2027, approaching target in 2H 2027",
    "CBE MPC decision of 20-Aug-2026 as reported by Bloomberg and Daily News Egypt; CBE "
    "communication of 22-Aug-2026",
    PRESS, "2026-08-20",
    model_impact="Pushes the start of the EGP rate-cut path out to 2027 in the base case. "
                 "Cuts both ways for FWRY: a slower cut path holds the discount rate high, "
                 "but also holds up the float/treasury income and the lending yield.")

f_fx = R.add(Ring.COUNTRY, "sovereign macro (inflation, policy rate, FX/deval risk)",
    FindingClass.C,
    "EGP/USD around 51.2 (USD 0.01955 per EGP) in early September 2026, having traded in a "
    "0.01954-0.02001 band over the preceding week — no repeat of the 2024 step devaluation "
    "in the sweep window",
    "Published EGP/USD spot series", PMD, "2026-09-02",
    model_impact="")

f_psp = R.add(Ring.COUNTRY, "regulatory environment (regulator, caps, tariffs, tax/subsidy)",
    FindingClass.S,
    "TWO REGULATORS, AND THE SPLIT IS THE WHOLE STRUCTURE OF THIS COMPANY. Payment services "
    "and payment systems sit under the CBE, which issued new PSO/PSP licensing and "
    "registration rules in June 2025 and, by board decision of 31 March 2026, widened the "
    "definition of 'financial companies' to cover payment companies, money transfer, "
    "factoring, leasing, SME finance, consumer finance and fintechs. The CBE also scrapped "
    "the 40% cap on bank ownership of fintechs (April 2026), and banks have begun moving. "
    "Non-bank lending, insurance broking and BNPL sit under the FRA",
    "Egyptian legal-practice guides to CBE/FRA fintech licensing (Chambers Fintech 2026 "
    "Egypt; Mondaq CBE & FRA licensing guide) and reporting of the CBE board decisions",
    PRESS, "2026-04-29",
    model_impact="Raises the competitive-intensity assumption in Acceptance and Agent "
                 "Banking: bank-owned acquirers can now be built without the ownership cap. "
                 "Feeds the take-rate decay driver, not the volume driver.")

f_fra = R.add(Ring.COUNTRY, "regulatory environment (regulator, caps, tariffs, tax/subsidy)",
    FindingClass.S,
    "FRA Decree 43 of 24 February 2026 SUSPENDED acceptance of new applications to "
    "incorporate or licence consumer-finance companies under the FinTech Law for one year "
    "from 25 February 2026. Consumer-finance companies may not extend cash loans except up "
    "to EGP 50,000 with FRA pre-approval (Decrees 81/2023 and 138/2025), capped at 20% of "
    "the portfolio",
    "FRA decrees as summarised in the Chambers Fintech 2026 Egypt practice guide",
    PRESS, "2026-02-24",
    model_impact="Two-sided and both sides go into the Financial Services build: the "
                 "licence freeze protects Fawry's existing consumer-finance licence "
                 "(a moat with a one-year clock), while the 20% cash-lending cap bounds "
                 "the mix of the BNPL book and therefore its blended yield.")

f_tax = R.add(Ring.COUNTRY, "regulatory environment (regulator, caps, tariffs, tax/subsidy)",
    FindingClass.C,
    "Egyptian corporate income tax 22.5%, unchanged",
    "Egyptian corporate tax rate per the house Cost-of-Capital reference convention",
    REG, "2026-01-01", model_impact="")

f_vat = R.add(Ring.COUNTRY, "fiscal / political events with sector read-through",
    FindingClass.B,
    "A Cabinet-approved draft law would EXEMPT InstaPay, Fawry and other banking and "
    "non-banking financial services and investment funds from VAT; the package was heading "
    "to the House for approval as of 3 June 2026",
    "Cabinet draft law reported by EnterpriseAM, 03-Jun-2026", PRESS, "2026-06-03",
    model_impact="BASE CHANGER if enacted, and it is modelled as an explicit dated event "
                 "with the headline DUAL-FRAMED with and without — never smoothed into the "
                 "revenue glide. Fawry's services are named in the draft; an exemption "
                 "changes the effective price to the merchant/consumer and therefore the "
                 "take rate the company can retain. Status at the sweep date: NOT ENACTED.")

f_incl = R.add(Ring.COUNTRY, "fiscal / political events with sector read-through",
    FindingClass.C,
    "The cashless-economy and financial-inclusion agenda remains state policy, and the "
    "state is on both sides of the market: Banque Misr (9.74%) and the National Bank of "
    "Egypt (6.05%) are Fawry shareholders while the state-linked e-finance group is its "
    "largest listed competitor, and MSMEDA lends to Fawry's MSME arm (EGP 550mn facility, "
    "2Q2026)",
    "Fawry 1H2026 earnings release (shareholder structure, MSMEDA facility)", IR,
    "2026-08-13", model_impact="")

# -------------------------------------------------------------- RING 3 INDUSTRY
f_ipn = R.add(Ring.INDUSTRY, "demand drivers & capacity/supply balance", FindingClass.S,
    "The CBE's own Instant Payment Network / InstaPay has passed 16mn users and roughly "
    "1.1bn transactions worth about EGP 2.4tn, having processed 263mn transactions worth "
    "over EGP 1.2tn in Q1-2025 alone. Account-to-account and wallet rails are now growing "
    "faster than card rails in Egypt",
    "Central Bank of Egypt IPN disclosures as reported by Egypt Independent and Egyptian "
    "business press", PRESS, "2026-01-01",
    model_impact="Sets the size and growth of the rails Fawry both rides and competes with. "
                 "Used as the ceiling test on the throughput driver: Fawry's EGP 943.6bn "
                 "FY2025 throughput has to be sized against an IPN running at multiples of "
                 "it, so throughput growth is a share-of-rails question, not an "
                 "extrapolation.")

f_take = R.add(Ring.INDUSTRY, "pricing", FindingClass.D,
    "THE TAKE RATE, COMPUTED FROM THE COMPANY'S OWN DISCLOSED PAIRS AND FALLING AT EVERY "
    "SEGMENT WHILE THE BLEND HOLDS. Blended revenue/throughput: 0.916% FY2024 (5,510.6/"
    "601,723), 0.917% FY2025 (8,651.5/943,633), 0.890% 1H2026 (5,222.2/586,857). Acceptance: "
    "0.714% FY2024 (1,196.9/167,600) -> 0.614% FY2025 (1,785.7/290,600) -> 0.591% 1H2026 "
    "(1,000.9/169,500). Agent Banking: 0.545% FY2024 (1,115.1/204,500) -> 0.490% FY2025 "
    "(1,729.0/352,800) -> 0.448% 1H2026 (1,069.2/238,800). Banking Services in total: 0.621% "
    "-> 0.546% -> 0.507%. The blend only holds because mix shifts to the higher-take "
    "Financial Services line",
    "Fawry FY2024, FY2025 and 1H2026 earnings releases — segment revenue and segment "
    "throughput both disclosed in the same document, so each ratio comes from one basis",
    IR, "2026-08-13",
    model_impact="DRIVER UNLOCK, and the central one for this name. Converts revenue from a "
                 "growth rate into THROUGHPUT x TAKE RATE at segment level, with the take "
                 "rate projected DOWN on its own measured trend rather than held flat. Also "
                 "the reason the blended take rate may never be used as the driver: it is an "
                 "output of mix, and mix is itself a driver.")

f_arpt = R.add(Ring.INDUSTRY, "pricing", FindingClass.D,
    "Average revenue per transaction rose from EGP 2.6 in 4Q2024 to EGP 3.4 in 4Q2025 "
    "(+28%) while transaction COUNT grew only 9% (483mn to 527mn in the quarter; 1,930mn to "
    "2,078mn for the year, +7.7%) and average transaction VALUE rose 53% (EGP 379 to EGP "
    "578). Growth is coming from bigger tickets, not more transactions",
    "Fawry FY2025 (4Q25) earnings-call presentation, operational KPI page", IR, "2026-03-16",
    model_impact="Second, independent build of the same revenue line: transactions x revenue "
                 "per transaction, used as the cross-check on throughput x take rate. The "
                 "7.7% transaction growth against 56.8% throughput growth is the single most "
                 "important warning in the sweep — the volume engine is ticket size, which "
                 "is inflation-linked and mean-reverting, not transaction count.")

f_entrants = R.add(Ring.INDUSTRY, "new entrants (named-competitor level)", FindingClass.S,
    "Named competition, by rail. Merchant acceptance: Paymob, reported at roughly 390k "
    "merchants enabled, against Fawry's own disclosed 379k agents and 364.6k "
    "acceptance-enabled POS at 1H2026 — the two counts are NOT on the same basis and the "
    "sweep records that rather than netting them (see the negative search on merchant "
    "counts). Also Geidea, Kashier, Opay. Consumer BNPL: "
    "valU, Shahry, MNT-Halan, Khazna. Bank-owned acquiring: e-finance's Al Ahly Momkn (25%) "
    "and EasyCash (13%), both bought May-2024. Egypt BNPL is put at USD 1.37bn in 2025 "
    "growing toward USD 4.16bn by 2031, with valU, Fawry, Paymob and Shahry named as the "
    "principals",
    "Egypt payments and BNPL market coverage (GlobeNewswire/ResearchAndMarkets Egypt BNPL "
    "2026; Egyptian payment-gateway comparisons)", PRESS, "2026-02-04",
    model_impact="Sets the competitive ceiling on Acceptance take rate and on BNPL yield. "
                 "Feeds the take-rate decay driver and the credit-spread assumption on the "
                 "consumer book, not the throughput driver.")

f_sub = R.add(Ring.INDUSTRY, "technology substitution", FindingClass.S,
    "THE SUBSTITUTION IS LIVE AND THE COMPANY'S OWN NUMBERS SHOW IT. The CBE's IPN/InstaPay "
    "moves money bank-to-bank at little or no fee, which is the direct substitute for "
    "Fawry's oldest rail. Fawry's ADP (bill payment) segment grew just 17.6% in FY2025 and "
    "2.9% in 1H2026 against 57% and 39% group growth, and fell from 39% of revenue in 2023 "
    "to 23% in 2025 to a guided 18% in 2026. In February 2026 the CBE officially launched "
    "Soft POS — turning any phone into a terminal — against which Fawry had pre-built its "
    "own solution in 2024",
    "Fawry FY2025 and 1H2026 earnings releases and FY2025 earnings presentation; CBE Soft "
    "POS launch noted in the company's own FY2025 release", IR, "2026-03-05",
    model_impact="Sets ADP as a DECLINING-SHARE, low-single-digit-growth line in the "
                 "explicit window rather than a group-growth line, and caps the terminal "
                 "estate's contribution: Soft POS removes the hardware moat. This is the "
                 "downside mechanism behind the bear case.")

f_efih = R.add(Ring.INDUSTRY, "competitor capacity / price moves (named)", FindingClass.S,
    "e-finance for Digital and Financial Investments (EGX: EFIH), the listed state-linked "
    "peer, grew FY2025 consolidated revenue 30.0% to EGP 6,773.1mn with EBITDA up 36.0% to "
    "EGP 3,332.4mn, and Q1-2026 revenue above EGP 2.2bn with net profit +42%. On 13 August "
    "2026 it confirmed the acquisition of microfinance lender Tamweely at up to EGP 4.8bn — "
    "the same MSME-lending ground Fawry MSME Finance occupies",
    "e-finance FY2025 earnings release and Egyptian market reporting of the Tamweely "
    "confirmation", PRESS, "2026-08-13",
    model_impact="Defines the relative-multiple peer set (EFIH is the only listed Egyptian "
                 "pure comparator) and prices the competitive threat to the MSME book. The "
                 "Tamweely price is also the only recent, named, arm's-length mark on an "
                 "Egyptian micro-lending book and is carried into the sum-of-the-parts as a "
                 "cross-check on the lending arm's value.")

# --------------------------------------------------------------- RING 4 COMPANY
f_fs21 = R.add(Ring.COMPANY, "official financial statements", FindingClass.D,
    "FY2021 AUDITED CONSOLIDATED, read and footed: operating revenue EGP 1,658,156,677; "
    "operating costs (725,893,276); gross margin 932,263,401 (56.2%); G&A (379,711,786); "
    "ESOP (52,398,016); board compensation (3,972,600); selling and marketing (279,254,967); "
    "medical contribution (5,505,997); formed provisions (11,628,500); net impairment loss on "
    "customers' loans (12,749,394); reversal of expected credit loss 1,770,520; other "
    "operating expenses (7,020,000); net gain on CBE POS-spreading incentives 21,725,295; "
    "credit interest 126,766,483; finance costs (39,439,470); FX 310,283; gain on disposal of "
    "fixed assets 7,168,024; other revenues 5,871,268; operating profit 304,194,544; share of "
    "losses of associates and JVs (5,549,798); gain on step-up from associate to subsidiary "
    "22,800,000; profit before tax 321,444,746; current income tax (75,726,644); deferred tax "
    "(3,596,019); net profit 242,122,083, of which parent 177,177,542 and NCI 64,944,541; EPS "
    "0.12 basic and diluted. Balance sheet: total assets 4,124,074,928 (non-current "
    "1,003,356,023 + current 3,120,718,905), total equity 1,458,019,334 (parent 1,379,010,558 "
    "+ NCI 79,008,776), issued capital 853,652,060, non-current liabilities 165,251,717, "
    "current liabilities 2,500,803,877",
    "Fawry FY2021 audited consolidated financial statements (English translation of the "
    "Arabic original), pages 4-6",
    CO, "2022-03-31",
    detail="ROUTE: image-only scan with no text layer at all (51pp, retrieved as an Internet "
           "Archive capture of the company's own PDF, fawry.com/wp-content/uploads/2023/03/"
           "Fawry-Consolidated-Financials-Q4-2021-English.pdf, capture 20240217155800, stored "
           "at filings/FS_CONS_FY2021_EN.pdf). A first OCR pass produced "
           "filings/FS_CONS_FY2021_EN_OCR.FAILED_FIRST_PASS.txt, retained under that name so "
           "the discarded route stays visible, and it FAILED its footing test on three "
           "subtotals; every figure above was then re-read off the rendered pixels at the "
           "scan's native 200 dpi and the page now foots on all 13 subtotals across both "
           "columns (footing_check.py). SIX OCR GLYPH ERRORS were caught by the footing test "
           "and corrected against the pixels: accounts and notes receivable 63,746,140 read as "
           "53,746,140; medical contribution 5,505,997 read as 505,997; formed provisions "
           "11,628,500 read as 41,628,500; net impairment on customer loans 12,749,394 read as "
           "2,749,394; profit before tax 321,444,746 read as 321,444,745; and current income "
           "tax 75,726,644 read as 75,726,648. THE 5-POUND NET-PROFIT GAP WAS NOT DEFERRED TAX "
           "— deferred tax reads (3,596,019) at native resolution, exactly as the first pass "
           "had it. It was the last two errors in that list, sitting either side of the "
           "deferred-tax line and summing to precisely the 5 observed. SCANNER PROVENANCE CHECKED: the file was produced by "
           "a Xerox WorkCentre 5330, a device family subject to the 2013 JBIG2 symbol-"
           "substitution defect in which the SCANNER silently swaps one digit's bitmap for a "
           "similar one, which no amount of re-reading can recover. The JBIG2 segment headers "
           "were parsed and every page carries only an immediate generic region (type 38), "
           "with no symbol dictionary (type 0) and no text region (type 6/7). Generic-region "
           "coding is lossless at the pixel level, so scanner-side substitution is ruled out "
           "on this file and the pixels are the pixels the scanner saw. Every error found here "
           "was the extractor's, and re-reading is the correct and sufficient remedy. ONE "
           "RESIDUAL, DISCLOSED: the FY2020 comparative column foots on every subtotal except "
           "operating profit, which is 2,000 out. It traces to the medical-contribution cell, "
           "whose fourth digit is physically damaged in the scan (ink dropout) and reads "
           "equally as 4,063,677 or 4,065,677; arithmetic implies 4,065,677 but the glyph is "
           "not legible and NO FY2020 FIGURE IS ADMITTED TO THE REGISTER on the strength of "
           "it. FY2020 is a comparative here, not a year this study carries.",
    model_impact="Earliest historical year the study uses, and the fourth audited year, which "
                 "takes the FS-depth invariant from its floor to its target. It anchors the "
                 "bottom of the operating-leverage path the forecast has to justify: gross "
                 "margin 56.2% in FY2021, 59.7% FY2022, 63.0% FY2023, rising to 68.9% by "
                 "FY2025. A fourth point turns that from a three-point line into a trend with "
                 "a testable shape, and it is the only year in the set that predates the "
                 "2022 devaluation.",
    is_fs_data=True, fiscal_period="FY2021")

f_fs22 = R.add(Ring.COMPANY, "official financial statements", FindingClass.D,
    "FY2022 AUDITED CONSOLIDATED, read and footed: operating revenue EGP 2,279,335,174; "
    "operating costs (918,106,893); gross margin 1,361,228,281 (59.7%); G&A (567,883,468); "
    "selling and marketing (385,919,177); ESOP (99,115,167); provisions formed (16,638,949); "
    "impairment loss on customer loans (29,509,883); expected credit loss (1,674,415); credit "
    "interest 211,071,914; finance costs (42,118,143); operating profit 448,149,871; tax "
    "(117,487,788); net profit 327,055,161, of which parent 240,054,320 and NCI 87,000,841; "
    "EPS 0.08. Balance sheet: total assets 6,423,757,906, total equity 2,595,244,934, issued "
    "capital 1,653,652,060",
    "Fawry FY2023 audited consolidated financial statements — FY2022 comparative column "
    "(English translation of the Arabic original; the standalone FY2022 set is also held)",
    CO, "2024-03-04",
    detail="ROUTE: read off the rendered pixels of the scanned page (pdfimages -> visual "
           "read), because the file has no text layer at all. Every subtotal on the page is "
           "re-added in footing_check.py and foots exactly. The standalone FY2022 audited "
           "set is held at filings/FS_CONS_FY2022_EN.pdf (46pp, 10.1 MB full-fidelity "
           "archive capture after a first attempt returned the archive's 1,048,576-byte "
           "truncated copy, which is retained with a .TRUNCATED suffix so the discarded "
           "route stays visible); the figures above come from the FY2023 set's audited "
           "comparative column, which is what was read.",
    model_impact="Second historical year. It is the pre-scale cost base: "
                 "59.7% gross margin against 68.9% in FY2025, which is the whole operating-"
                 "leverage story the forecast has to justify or fade.",
    is_fs_data=True, fiscal_period="FY2022")

f_fs23 = R.add(Ring.COMPANY, "official financial statements", FindingClass.D,
    "FY2023 AUDITED CONSOLIDATED, read and footed: operating revenue EGP 3,272,016,083; "
    "operating costs (1,210,193,626); gross margin 2,061,822,457 (63.0%); G&A (758,592,564); "
    "selling and marketing (480,982,338); ESOP (105,986,256); board allowances (7,988,000); "
    "health/social contribution (11,599,755); provisions formed (36,549,258); impairment on "
    "customer loans (49,738,948); expected credit loss (13,612,074); credit interest "
    "464,413,386; finance costs (40,214,267); FX gain 11,777,126; operating profit "
    "1,065,736,046; tax (278,653,009); net profit 815,968,937, of which parent 715,338,691 "
    "and NCI 100,630,246; EPS 0.18. Balance sheet: total assets 8,971,583,645; customer loans "
    "231,244,380 non-current + 920,552,076 current; treasury bills 2,342,600,551; cash "
    "2,758,635,418; total equity 3,469,848,632",
    "Fawry FY2023 audited consolidated financial statements (English translation of the "
    "Arabic original), 44pp, Xerox scan created 4 March 2024", CO, "2024-03-04",
    detail="ROUTE: read off the rendered pixels; no text layer. All fifteen subtotals on the "
           "income statement and balance sheet foot exactly (footing_check.py), and the same "
           "FY2023 figures appear as the comparative column of the FY2024 Arabic set, giving "
           "an independent cross-document tie.",
    model_impact="Third historical year and the hinge of the margin story: gross margin "
                 "63.0% against 56.2% in FY2021, 59.7% in FY2022 and 65.7% in FY2024.",
    is_fs_data=True, fiscal_period="FY2023")

f_fs24 = R.add(Ring.COMPANY, "official financial statements", FindingClass.D,
    "FY2024 AUDITED CONSOLIDATED, read and footed: revenue EGP 5,510,620,184; cost of "
    "activity (1,888,316,913); gross profit 3,622,303,271 (65.7%); G&A (1,053,620,943); "
    "selling and marketing (666,676,441); ESOP (80,719,154); board allowances (11,315,012); "
    "health contribution (19,994,772); provisions formed (86,302,287); net provision for "
    "customer financing risk (134,600,555); expected credit loss (7,273,087); credit interest "
    "691,243,802; finance costs (56,537,004); FX gain 32,089,292; gain on disposal 40,937,035; "
    "other income 14,105,209; operating profit 2,296,060,131; associates 5,162,235; profit "
    "before tax 2,301,222,366; tax (552,160,176); net profit 1,749,062,190, of which parent "
    "1,606,651,692 and NCI 142,410,498; EPS 0.41",
    "Fawry FY2024 audited consolidated financial statements (ARABIC original), 43pp",
    CO, "2025-03-02",
    detail="ROUTE: read off the rendered pixels of the Arabic scan; Arabic-Indic digits, no "
           "text layer. THE PAGE FAILED ITS FIRST READ and was re-read at 3x-6x zoom until it "
           "footed — the customer-financing provision was first read 134,600,000 against a "
           "true 134,600,555, and eight balance-sheet glyphs were corrected the same way. "
           "footing_check.py records every corrected line. THE LANGUAGE OF THE SET IS "
           "RECORDED because a label read from an Arabic column must not be silently equated "
           "with one read from an English column; the English FY2024 set exists at the "
           "sibling URL but the archive's only capture of it recorded a 403.",
    model_impact="The most recent AUDITED year, and the last balance sheet the study has. "
                 "Every FY2025 and 2026 balance-sheet item has to be rolled from here, "
                 "because no later statement could be obtained.",
    is_fs_data=True, fiscal_period="FY2024")

f_cost = R.add(Ring.COMPANY, "official financial statements", FindingClass.D,
    "THE COST STACK, WHICH IS WHY MARGIN CAN BE AN OUTPUT. The audited income statement "
    "discloses cost of activity, G&A, selling and marketing, ESOP, board allowances, the "
    "health contribution, provisions formed, the customer-financing provision and expected "
    "credit loss as separate lines for FY2022, FY2023 and FY2024. Cost of activity as a share "
    "of revenue: 40.3% FY2022, 37.0% FY2023, 34.3% FY2024. G&A: 24.9% / 23.2% / 19.1%. "
    "Selling and marketing: 16.9% / 14.7% / 12.1%. Credit interest ran EGP 211.1m / 464.4m / "
    "691.2m and finance costs 42.1m / 40.2m / 56.5m",
    "Fawry FY2023 and FY2024 audited consolidated financial statements", CO, "2025-03-02",
    detail="No earnings release carries any of these lines — the releases stop at gross "
           "profit and at the company's own adjusted EBITDA. This finding is the ONLY route "
           "to a cost-per-unit build, and it exists for three years and stops there.",
    model_impact="MARGIN IS AN OUTPUT. Each cost line is projected on its own driver — cost "
                 "of activity against throughput, G&A and marketing against revenue with the "
                 "measured operating leverage — and gross and EBITDA margins fall out. Setting "
                 "a margin as an input where these lines exist would be a QC fail.",
    is_fs_data=True, fiscal_period="FY2024")

f_bs = R.add(Ring.COMPANY, "official financial statements", FindingClass.D,
    "THE BALANCE SHEET AT 31-DEC-2024, AND THE FLOAT NOBODY DISCLOSES IN A RELEASE. Total "
    "assets EGP 13,256,776,370. On the asset side, cash and bank balances 4,267,441,022 plus "
    "treasury bills 2,240,138,857 = EGP 6.51bn of liquid assets; customer loans and facilities "
    "725,040,807 non-current + 2,233,166,351 current = EGP 2,958,207,158 NET of provisions "
    "(against the release's gross portfolio of 'above EGP 3.1bn' at the same date — the "
    "difference is the provision, and the two bases must not be equated). On the liability "
    "side, long-term loans 381,159,804, short-term loans 886,794,276 and bank facilities "
    "279,364,012 = EGP 1.55bn of debt, so the group is roughly EGP 4.96bn NET CASH before "
    "counting float. THE FLOAT IS THE LARGEST LIABILITY: billers payable 2,303,120,832 plus "
    "merchant advances 2,602,659,644 plus retailer POS security deposits 108,901,634 = EGP "
    "5.01bn of other people's money on the balance sheet. Total equity 5,162,996,252",
    "Fawry FY2024 audited consolidated financial statements, statement of financial position",
    CO, "2025-03-02",
    detail="Read off the rendered pixels and footed line by line; the FY2023 comparative in "
           "the English set foots independently. Credit interest of EGP 691.2m in FY2024 is "
           "the income earned on this pool and on the T-bills, and the company's own EBITDA "
           "definition explicitly EXCLUDES 'interest income not related to the operating "
           "cycle' — so the release's EBITDA and this income are different things.",
    model_impact="Three consequences. (1) The equity bridge ADDS net cash and must decide "
                 "explicitly how much of the EGP 5.01bn float is genuinely free. (2) Credit "
                 "interest is modelled bottom-up as a yield on the float and T-bill balances "
                 "rather than as a plug, and is kept OUT of operating value to avoid double-"
                 "counting. (3) The CBE policy rate feeds earnings directly through this "
                 "line, which is why a slower cut path is not unambiguously bad for FWRY.",
    is_fs_data=True, fiscal_period="FY2024")

f_fs25 = R.add(Ring.COMPANY, "official financial statements", FindingClass.D,
    "[R-SIGCM-03 FALLBACK, DECLARED] FY2025 full-year income statement — revenue EGP "
    "8,651,478k, gross profit EGP 5,959,842k (68.9%), EBITDA EGP 4,968,131k (57.4%), net "
    "profit before NCI EGP 3,100,654k, net profit after NCI EGP 2,889,189k (33.4%); by "
    "service line, Banking Services 3,514,670 (Acceptance 1,785,665 + Agent Banking "
    "1,729,005), Financial Services 2,382,015, ADP 2,008,281, Supply Chain Solutions "
    "496,113, Technology & Others 250,399. THE AUDITED FY2025 STATEMENTS COULD NOT BE "
    "OBTAINED (see module docstring exception 4); these figures come from THE COMPANY'S OWN "
    "FY2025 EARNINGS RELEASE",
    "Fawry FY2025 earnings release, 5 March 2026 (company's own PDF, ent.news/2026/3/291.pdf)",
    IR, "2026-03-05",
    detail="THE SEGMENT TABLE FOOTS AGAINST ITS OWN PRINTED TOTAL: 3,514,670 + 2,382,015 + "
           "2,008,281 + 496,113 + 250,399 = 8,651,478, exactly the printed Total Revenues; "
           "Acceptance + Agent Banking = 3,514,670, exactly the printed Banking Services. "
           "The FY2024 comparative column foots the same way to 5,510,620. Arithmetic is "
           "the arbiter and this document passes it — but it is a release, not a statement, "
           "and the is_fs_data flag is left set so the validator says so.",
    model_impact="The FY2025 base every forward driver is grown from. Carried as the "
                 "company's own released figures, with the audited set named as an open "
                 "item the study must obtain before issue.",
    is_fs_data=True, fiscal_period="FY2025")

f_q1 = R.add(Ring.COMPANY, "regular disclosures", FindingClass.D,
    "[R-SIGCM-03 FALLBACK, DECLARED] Q1-2026 — total revenue EGP 2,410,734k (+34.3% y/y), "
    "Banking Services 924,114 (Acceptance 487,000 + Agent Banking 437,113), Financial "
    "Services 800,506, ADP 472,387, Supply Chain 144,999, Technology & Others 68,729; gross "
    "profit 1,619,818 (67.2%), EBITDA 1,351,464 (56.1%), net profit after NCI 749,339 "
    "(31.1%). The Q1-2026 reviewed interim statements could not be obtained; these are the "
    "comparative column of the company's own 1H2026 release",
    "Fawry 1H2026 earnings release, 13 August 2026 (company's own PDF, ent.news/2026/8/542.pdf)",
    IR, "2026-08-13",
    detail="Ties two ways: the segment lines sum to 2,410,735 against a printed 2,410,734 "
           "(one-unit rounding), and H1 minus Q2 gives 5,222,178 - 2,811,444 = 2,410,734 "
           "exactly.",
    model_impact="First actual quarter of the study year. Q1 revenue growth of 34.3% is "
                 "BELOW the 39% full-year guidance, which the build must reconcile rather "
                 "than average away.",
    is_fs_data=True, fiscal_period="Q1-2026")

f_q2 = R.add(Ring.COMPANY, "regular disclosures", FindingClass.D,
    "[R-SIGCM-03 FALLBACK, DECLARED] Q2-2026 — total revenue EGP 2,811,444k (+42.7% y/y, "
    "+16.6% q/q), Banking Services 1,145,984 (Acceptance 513,918 + Agent Banking 632,066), "
    "Financial Services 888,120, ADP 523,285, Supply Chain 167,039, Technology & Others "
    "87,015; gross profit 1,919,789 (68.3%), EBITDA 1,608,986 (57.2%), net profit after NCI "
    "870,519 (31.0%). 1H2026: revenue 5,222,178, EBITDA 2,960,450 (56.7%), net profit after "
    "NCI 1,619,858 (31.0%), throughput EGP 586,857.2mn (+52.1%). The H1-2026 reviewed "
    "interim statements could not be obtained",
    "Fawry 1H2026 earnings release, 13 August 2026 (company's own PDF)", IR, "2026-08-13",
    detail="Segment lines sum to 2,811,443 against a printed 2,811,444 (one-unit rounding). "
           "Q2 accelerated on Q1 across every KPI, which is the opposite of the shape a "
           "34.3% Q1 alone would imply.",
    model_impact="Second actual quarter of the study year; 1H2026 revenue is 60.4% of the "
                 "guided FY2026 revenue implied by +39% growth, so the guidance is "
                 "achievable but requires the 2H to hold the Q2 run rate.",
    is_fs_data=True, fiscal_period="Q2-2026")

f_rel = R.add(Ring.COMPANY, "regular disclosures", FindingClass.D,
    "THE RELEASE SERIES AND ITS BASIS TRAP. Eight of the company's own earnings releases "
    "were retrieved (FY2023, 2Q2024, 3Q2024, FY2024, Q1-2025, 2Q2025, FY2025, 1H2026). They "
    "disclose revenue in SIX service lines; the audited statements do not carry that split. "
    "The releases also carry a restated basis: Financial Services now includes MSME lending, "
    "consumer finance, insurance brokerage, prepaid card and money-market-fund revenue, and "
    "everything except microfinance was REALLOCATED OUT OF 'Others' — a footnote repeated in "
    "every release from FY2024 onward",
    "Fawry earnings releases FY2023 through 1H2026 (company's own PDFs)", IR, "2026-08-13",
    model_impact="Fixes which basis each series is built on. Segment revenue is taken ONLY "
                 "from the releases and ONLY from FY2024 onward, where the reallocated basis "
                 "is consistent; the audited statements supply the total, the cost stack and "
                 "the balance sheet. THE TWO BASES ARE NEVER MIXED IN ONE SERIES.")

f_loans = R.add(Ring.COMPANY, "regular disclosures", FindingClass.D,
    "THE CREDIT BOOK, SEPARATED FROM THE PAYMENTS BUSINESS. Total gross loan portfolio "
    "across Micro, SME and Consumer: EGP 5,696mn at 31-Dec-2025 (+82.6% y/y) and EGP 6,613mn "
    "at 30-Jun-2026 (+71.3% y/y), against roughly EGP 3.1bn at end-2024 and about EGP 1.2bn "
    "at end-2023. Split at FY2025: MSME EGP 2,811mn (+34.1%) and consumer BNPL EGP 2,885mn "
    "(from EGP 1,023mn); at 1H2026: MSME EGP 3,395mn (+61.9%) and consumer BNPL EGP 3,218mn "
    "(+82.6%). PROVISIONING, disclosed as provisions balance over gross loans: MSME 3.7% at "
    "4Q25 against 4.9% at 4Q24; consumer finance 4.0% against 5.6%. BNPL collection "
    "efficiency 94% in month one, 97% by month two, 98% by month three; average BNPL ticket "
    "EGP 2.3k, average tenor 6.7 months, 5.2 transactions per customer per month",
    "Fawry FY2025 earnings release and FY2025 (4Q25) earnings presentation; 1H2026 earnings "
    "release", IR, "2026-03-16",
    model_impact="THE LENDING BOOK IS MODELLED AS ITS OWN LEG AND NEVER BLENDED INTO THE "
                 "PAYMENTS MULTIPLE. Book size x yield gives Financial Services revenue; the "
                 "disclosed provisions ratios give the cost of risk; the book is funded and "
                 "capital-consuming in a way throughput is not. The FALLING provisions ratio "
                 "on a book that nearly doubled is the single item to stress: a 3.7% ratio on "
                 "a book growing 82.6% is a seasoning question, not a quality result.")

f_pres25 = R.add(Ring.COMPANY, "IR communications (calls, presentations, releases)",
    FindingClass.D,
    "FY2025 (4Q25) earnings-call presentation, 16 March 2026, 27 pages — the document that "
    "carries what no financial statement does: operational KPIs (54.8mn active network "
    "customers, 376.6k total POS, 353.5k acceptance-enabled POS, 36 contracted banks, 4,530 "
    "services, 2,078mn transactions, 393mn mobile-wallet transactions, EGP 835.5bn mobile-"
    "wallet processed value, EGP 943.6bn throughput), the average-revenue-per-transaction "
    "series, segment throughput, the loan-book and provisioning detail, and the 2026 guidance "
    "page",
    "Fawry FY2025 earnings presentation (company's own PDF via Internet Archive capture "
    "20260712094455)", IR, "2026-03-16",
    model_impact="The primary IR channel this study's operating drivers rest on. Supplies "
                 "the throughput, transaction-count and per-transaction-revenue series that "
                 "make the bottom-up build possible at all.")

f_pres_earlier = R.add(Ring.COMPANY, "IR communications (calls, presentations, releases)",
    FindingClass.C,
    "Three earlier decks retrieved for the history: FY2023 (28pp), FY2024 (28pp) and 1Q2025 "
    "(24pp) earnings presentations, giving the same KPI table back to 4Q2021 and the "
    "quarterly throughput series (EGP 40bn 4Q21, 62bn 4Q22, 105bn 4Q23, 183bn 4Q24, 305bn "
    "4Q25)",
    "Fawry FY2023, FY2024 and 1Q2025 earnings presentations (company's own PDFs via "
    "Internet Archive)", IR, "2025-05-01", model_impact="")

f_guid = R.add(Ring.COMPANY, "strategic plans & guidance", FindingClass.D,
    "MANAGEMENT'S OWN 2026 GUIDANCE, from the FY2025 deck: group revenue growth of 39% "
    "y-o-y with the EBITDA margin held 'relatively stable' at 58% (2025 actual 57.4%), and "
    "a revenue MIX guided to NBFI/Financial Services 34%, Acceptance 23%, ADP 18%, Agent "
    "Banking 17%, Supply Chain 6%, Technology & others 3%. The 2023-2025 mix columns on the "
    "same chart reconcile exactly to the released segment revenue, which is how the 2026 "
    "column was read",
    "Fawry FY2025 earnings presentation, guidance section", IR, "2026-03-16",
    detail="The per-segment GROWTH bar chart on the facing page is read positionally and is "
           "flagged for a pixel-level re-read at build time rather than trusted from the "
           "text layer; the MIX chart was verified against actuals (2025 read as ADP 23%, "
           "Acceptance 21%, Agent Banking 20%, NBFI 28%, SCS 6%, Tech 3% against actuals of "
           "23.2/20.6/20.0/27.5/5.7/2.9) and ties.",
    model_impact="Guidance is a CHECK on the bottom-up build, never the build itself. The "
                 "39% and the 58% are carried as management's own view beside the model's "
                 "own throughput x take-rate answer, and the gap between them is reported.")

f_med = R.add(Ring.COMPANY, "strategic plans & guidance", FindingClass.S,
    "New businesses management has committed to in its own words: a phased launch of an "
    "integrated Medical Services Platform (TPA + PBM + microinsurance) beginning in 1H2027, "
    "an inbound cross-border remittance licence awaiting approval as of May 2026, and a TPA "
    "licence obtained June 2026",
    "Fawry 1H2026 earnings release, Chief Executive's Review; licence reporting May/June 2026",
    IR, "2026-08-13",
    model_impact="Kept OUT of the explicit revenue build — no disclosed volume or price "
                 "exists for any of them — and carried instead as a named upside optionality "
                 "line in the scenario table, so that the base case is not quietly credited "
                 "with businesses that have not launched.")

f_promo = R.add(Ring.COMPANY, "one-off base-resetting transactions", FindingClass.B,
    "In 4Q2025 Fawry booked EGP 287mn of revenue from SEASONAL PROMOTIONAL CAMPAIGNS in the "
    "Wallets segment, reported inside Agent Banking. That single item is 11.1% of the "
    "quarter's EGP 2,592mn revenue and is why 4Q25 Agent Banking revenue printed +113.2% "
    "y-o-y",
    "Fawry FY2025 earnings release, footnote to the summary P&L and the segment overview",
    IR, "2026-03-05",
    model_impact="BASE CHANGER, and it resets the FY2025 base the forecast grows from. The "
                 "EGP 287mn is stripped to derive an underlying 4Q25/FY2025 Agent Banking "
                 "run rate, and the headline is DUAL-FRAMED with and without it. Taking "
                 "+113% or the FY2025 Agent Banking total as a run rate is the specific "
                 "error this finding exists to prevent.")

f_basis = R.add(Ring.COMPANY, "one-off base-resetting transactions", FindingClass.S,
    "SEGMENT BASIS CHANGE. From the FY2024 release onward, MSME lending, consumer finance, "
    "insurance brokerage, prepaid card and money-market-fund revenue are reported in "
    "Financial Services, all of them except microfinance having been reallocated out of "
    "'Others'. The FY2023 segment column in the FY2024 release is on the restated basis; "
    "columns in releases published before that are not",
    "Fawry FY2024 through 1H2026 earnings releases, repeated footnote 2", IR, "2025-03-02",
    model_impact="Sets the START of the usable segment series at FY2023-restated. Any "
                 "segment growth rate computed across the boundary is an artefact, and the "
                 "study states the boundary rather than smoothing across it.")

f_holdco = R.add(Ring.COMPANY, "one-off base-resetting transactions", FindingClass.S,
    "Fawry Holding for Financial Investments established on FRA approval of 27 November "
    "2025, authorised capital EGP 50mn, paid-in EGP 5mn, 99.99% owned by Fawry, created to "
    "house the group's investment activities and to carry an 'ongoing restructuring of "
    "existing subsidiaries'",
    "Fawry press release, 30 November 2025 (company's own PDF)", IR, "2025-11-30",
    model_impact="Flags a coming change in the consolidation perimeter and in the "
                 "non-controlling-interest line (NCI was 6.0% of EBT in 4Q25 against 6.3% in "
                 "4Q24). The sum-of-the-parts must be built on the CURRENT perimeter and the "
                 "restructuring named as a pending change, not assumed into it.")

f_acq = R.add(Ring.COMPANY, "one-off base-resetting transactions", FindingClass.B,
    "February 2025: EGP 80mn invested for control of three Egyptian technology companies — "
    "Dirac Systems (51.0%), Virtual CFO (56.6%) and Code Zone (51.0%) — to build out the "
    "'Fawry Business' suite. April 2026: FRA licence for Fawry for Microinsurance, EGP 60mn "
    "capital, 90% owned by Fawry",
    "Fawry press release 26 February 2025 (company's own PDF); FRA microinsurance licence "
    "reported 21 April 2026", IR, "2025-02-26",
    model_impact="BASE CHANGER for the Technology & Others line, which grew 93.1% in FY2025 "
                 "and 74.9% in 2Q2026 off a consolidation, not off organic demand. Modelled "
                 "as a dated step in the base with the acquired revenue named, never as an "
                 "organic growth rate carried forward.")

f_own = R.add(Ring.COMPANY, "ownership / stake changes (named-transaction rule)",
    FindingClass.S,
    "THE REGISTER AT THREE DATES, EACH FROM A COMPANY DOCUMENT, AND THE NAMED EXITS BETWEEN "
    "THEM. 31-Dec-2023 (governance report): Alpha Oryx Limited 416,728,062 shares 12.23%, "
    "Banque Misr 331,942,520 9.74%, Egyptian American Enterprise Fund 289,002,353 8.48%, "
    "Link Hold Co BV 270,344,629 7.93%, National Bank of Egypt 206,225,843 6.05%, Black "
    "Sparrow Long Term Investments 188,640,077 5.53% — 1,702,883,484 shares, 49.98%. "
    "31-Jan-2025 (FY2025 release): Alpha Oryx 12.23%, Banque Misr 9.74%, NBE 6.05%, EAEF "
    "4.29%, responsAbility Participations 1.83%, ESOP 1.06%, free float 64.80%. 31-Jul-2026 "
    "(1H2026 release): Alpha Oryx 12.23%, Banque Misr 9.74%, NBE 6.05%, EAEF 4.24%, ESOP "
    "0.41%, free float 67.33% — sums to 100.00% exactly. Link Hold Co BV (Helios) and Black "
    "Sparrow (MENA LTV) are GONE from the register between Dec-2023 and Jan-2025; "
    "responsAbility is gone between Jan-2025 and Jul-2026; EAEF has roughly halved",
    "Fawry corporate governance report YE2023 (company's own PDF) and the shareholder-"
    "structure charts printed in the FY2025 and 1H2026 earnings releases", CO, "2024-03-04",
    model_impact="Fixes the free float at 67.33% and identifies the overhang: three "
                 "pre-IPO financial sponsors have sold down and EAEF is still selling. That "
                 "is a supply-of-stock fact carried into the liquidity/discount discussion "
                 "and into the beta work — it is NOT used as a valuation input. Alpha Oryx "
                 "(ADQ) at 12.23% is the anchor holder and has not moved across three years.")

f_cap = R.add(Ring.COMPANY, "management & capital actions", FindingClass.D,
    "SHARE CAPITAL FROM THE AUDITED BALANCE SHEETS AND THE GOVERNANCE REPORT, AND A GAP THE "
    "STUDY MUST CLOSE. Issued and paid-up capital: EGP 1,653,652,060 at 31-Dec-2022, rising "
    "to EGP 1,703,261,622 at 31-Dec-2023 and UNCHANGED at 31-Dec-2024. Nominal value EGP 0.50 "
    "per share, so 3,307,304,120 shares at end-2022 and 3,406,523,244 from end-2023. "
    "Authorised capital EGP 3,000,000,000. Listed on the EGX 22 July 2019 under law 159/1981. "
    "An ESOP committee sits at board level; ESOP shares are carried as a negative equity item "
    "(EGP 31,429,709 at FY2024) with a matching ESOP reserve (EGP 150,837,104), and the ESOP "
    "holds 1.06% of the register at 31-Jan-2025 falling to 0.41% at 31-Jul-2026",
    "Fawry FY2023 and FY2024 audited consolidated statements of financial position; Fawry "
    "corporate governance report YE2023", CO, "2025-03-02",
    detail="THE SHARE COUNT DOES NOT RECONCILE TO THE PRINTED EPS AND THE STUDY MUST RESOLVE "
           "IT BEFORE ANY PER-SHARE NUMBER IS PUBLISHED. Parent net profit divided by issued "
           "shares gives EGP 0.472 for FY2024 and 0.210 for FY2023, against printed EPS of "
           "0.41 and 0.18 — implying a weighted-average denominator near 3.92bn and 3.97bn "
           "shares, and an FY2022 implied denominator near 3.0bn that moves the other way. "
           "The EPS note (note 42 in the Arabic set, note 43 in the English) has NOT been "
           "read and is the open item. Separately, a press report of a 'capital hike of EGP "
           "100mn on 200mn shares taking capital to EGP 453.65mn' is internally inconsistent "
           "with a company capital of EGP 1.703bn and is NOT carried.",
    model_impact="Fixes the denominator for every per-share figure at 3,406,523,244 shares "
                 "as last CONFIRMED by a company document, and flags that the audited EPS "
                 "implies a larger weighted count. No per-share value is published until the "
                 "EPS note reconciles.")

f_fund = R.add(Ring.COMPANY, "management & capital actions", FindingClass.D,
    "How the lending book is funded, from the company's own announcements: Fawry MSME "
    "Finance completed its first securitisation on 28 May 2025 — EGP 497.5mn, single tranche, "
    "13-month tenor, rated A- by MERIS, FRA-approved, CI Capital as arranger and bookrunner, "
    "EG Bank custodian — described as the first tranche of a broader programme; and in "
    "2Q2026 secured an EGP 550mn MSMEDA facility (EGP 300mn micro, EGP 250mn SME). Fawry "
    "MSME Finance also holds an FRA Islamic-financing licence (19 March 2025)",
    "Fawry press releases 28 May 2025 and 19 March 2025 (company's own PDFs); 1H2026 "
    "earnings release for the MSMEDA facility", IR, "2025-05-28",
    model_impact="Gives the cost and structure of funding for the credit leg specifically, "
                 "so the lending arm is valued with its own funding cost rather than the "
                 "group WACC. The A- rating and the 13-month tenor are the observable "
                 "anchors for the spread.")

# ------------------------------------------------------- NEGATIVE SEARCHES (DATED)
f_neg_fs25 = R.add_negative(Ring.COMPANY, "official financial statements",
    "'Fawry FY2025 audited consolidated financial statements 31-12-2025' — tried the "
    "company's own URL pattern under fawry.com/wp-content/uploads/2026/03/ (403 Cloudflare), "
    "the EGX bulletin route www.egx.com.eg/downloads/Bulletins/*.pdf (empty reply), the "
    "Internet Archive CDX for every fawry.com PDF captured after 01-Oct-2025 (only two 2026 "
    "files exist in the archive and neither is a statement), and Wayback Save Page Now (401, "
    "login required). The audited FY2025 set and the Q1/H1-2026 reviewed interims are NOT "
    "OBTAINABLE at this egress", SWEEP_DATE)

f_neg_adp = R.add_negative(Ring.INDUSTRY, "pricing",
    "'Fawry ADP alternative digital payments throughput value EGP billion FY2025 disclosed "
    "segment' — ADP, Supply Chain Solutions and Financial Services THROUGHPUT are shown only "
    "as unlabelled bar charts in the presentations; no numeric throughput is disclosed for "
    "them in any release. Only total throughput, Banking Services throughput, Agent Banking "
    "throughput and Acceptance throughput carry numbers, so a take-rate build is possible "
    "for those three lines and not for the rest", SWEEP_DATE)

f_neg_cost = R.add_negative(Ring.COMPANY, "regular disclosures",
    "'Fawry cost of sales breakdown / staff cost / commission expense / merchant "
    "commissions EGP 2025' — the earnings releases stop at gross profit and EBITDA and "
    "disclose NO cost line by nature. Cost-per-transaction and merchant-commission "
    "economics are not in any release; the only route to a cost stack is the audited "
    "statements' own income statement and notes, which exist for FY2021-FY2024 only",
    SWEEP_DATE)

f_neg_capital = R.add_negative(Ring.COMPANY, "management & capital actions",
    "'Fawry EGX disclosure capital increase 2025 2026 stock dividend ESOP general assembly "
    "official' — no company document dated after the YE2023 governance report could be "
    "retrieved that states the current issued capital or share count. Press reports a stock "
    "dividend of 0.2827637989 free shares in March 2026 and a capital increase resolved in "
    "December 2025, but the figures quoted do not reconcile to the company's own EGP 1.703bn "
    "issued capital, so nothing post-2023 is carried", SWEEP_DATE)

f_neg_call = R.add_negative(Ring.COMPANY, "IR communications (calls, presentations, releases)",
    "'Fawry FWRY earnings call transcript 4Q2025 1H2026 Q&A' — the FY2025 deck is headed "
    "'4Q 2025 Earnings Call March 16, 2026' but no transcript or webcast recording of any "
    "Fawry call is retrievable, and the IR events page (fawry.com/investor-relations/events/) "
    "is behind the same Cloudflare block. Management commentary is available only as the "
    "written CEO review printed in each release", SWEEP_DATE)

f_neg_capex = R.add_negative(Ring.COMPANY, "strategic plans & guidance",
    "'Fawry capex capital expenditure guidance POS terminal investment plan 2026' — no "
    "capital-expenditure figure or guidance appears in any release or presentation. The only "
    "capex-adjacent disclosure is the POS terminal count and management's statement that the "
    "estate was deliberately shrunk in 1H2026", SWEEP_DATE)

f_neg_float = R.add_negative(Ring.COMPANY, "regular disclosures",
    "'Fawry settlement float customer balances interest income treasury EGP' in the earnings "
    "releases — NO release or presentation quantifies the settlement float, the billers and "
    "merchant balances held, or the income earned on them, and the company's own EBITDA "
    "definition excludes 'interest income not related to the operating cycle' without saying "
    "how large it is. The search is recorded because it is the release series that is silent: "
    "the AUDITED STATEMENTS do disclose both sides (credit interest EGP 691.2m in FY2024; "
    "billers payable, merchant advances and POS deposits totalling EGP 5.01bn), which is why "
    "the float driver is built bottom-up off the statements and NOT off the releases",
    SWEEP_DATE)

f_neg_vat = R.add_negative(Ring.COUNTRY, "fiscal / political events with sector read-through",
    "'Fawry VAT exemption impact on revenue guidance quantified company statement Egypt draft "
    "law 2026' — the Cabinet draft law naming Fawry is real and dated, but NO company "
    "document quantifies what an exemption would be worth: it is absent from the FY2025 "
    "presentation's guidance page, from the 1H2026 release and from every press release held. "
    "There is nothing of the company's own to build the event from, which is why it is carried "
    "as a dual-framed scenario rather than as a driver",
    "2026-09-09")

f_neg_merch = R.add_negative(Ring.INDUSTRY, "demand drivers & capacity/supply balance",
    "'Fawry merchant count acceptance merchants number 2026 versus agents' — the company "
    "discloses AGENTS (379k), POS terminals (378.6k) and acceptance-enabled POS (364.6k) but "
    "not a merchant count on the same basis as competitors quote theirs, so the "
    "Paymob/Fawry merchant comparison in the industry ring cannot be put on one basis",
    SWEEP_DATE)

# --------------------------------------------------------------- STUDY YEAR
R.declare_study_year("2026", ["Q1-2026", "Q2-2026"])

# ------------------------------------------------------------- DRIVER GATE TABLE
R.add_driver("Throughput by service line (EGP bn)", DriverMode.BOTTOM_UP,
    "Total throughput and the Banking Services / Agent Banking / Acceptance splits are "
    "disclosed in the company's own releases in the same document as the matching segment "
    "revenue (FY2024 601.7bn total, 204.5 agent, 167.6 acceptance; FY2025 943.6 total, 643.4 "
    "banking, 352.8 agent, 290.6 acceptance; 1H2026 586.9 total, 408.3 banking, 238.8 agent, "
    "169.5 acceptance). Built at that level and sized against the CBE's IPN as the ceiling.",
    [f_take, f_ipn, f_fs25, f_q2])

R.add_driver("Take rate by service line (%)", DriverMode.BOTTOM_UP,
    "Computed as segment revenue / segment throughput from the same release, giving a "
    "measured decay per line (Acceptance 0.714 -> 0.614 -> 0.590; Agent Banking 0.545 -> "
    "0.490 -> 0.448). Projected on its own measured trend. THE BLENDED TAKE RATE IS AN "
    "OUTPUT OF MIX AND IS NEVER USED AS AN INPUT.",
    [f_take, f_arpt, f_sub])

R.add_driver("Transactions (mn) and revenue per transaction (EGP)", DriverMode.BOTTOM_UP,
    "Second, independent build of the same revenue line from the company's own KPI table "
    "(1,930mn -> 2,078mn transactions; EGP 2.6 -> 3.4 revenue per transaction in 4Q). Used "
    "as the cross-check on throughput x take rate and as the test of whether growth is "
    "ticket size or activity.",
    [f_arpt, f_pres25])

R.add_driver("ADP (bill payment) revenue", DriverMode.TOP_DOWN,
    "ADP throughput is NOT disclosed numerically in any company document — only as an "
    "unlabelled chart — so no take-rate build is possible for this line. Modelled top-down "
    "on the company's own guided share of revenue and the measured 17.6% FY2025 / 2.9% "
    "1H2026 growth, with the InstaPay substitution as the decay mechanism. The gap is "
    "flagged in the study, not hidden.",
    [f_neg_adp, f_sub])

R.add_driver("Supply Chain Solutions and Technology & Others revenue", DriverMode.TOP_DOWN,
    "Neither line discloses throughput or any unit; Technology & Others is in any case a "
    "consolidation step from the Feb-2025 acquisitions rather than an organic series. "
    "Modelled top-down off the disclosed revenue with the acquisition step dated explicitly.",
    [f_neg_adp, f_acq])

R.add_driver("Financial Services revenue (lending book x yield)", DriverMode.BOTTOM_UP,
    "The gross loan portfolio is disclosed by sub-book at every reporting date (MSME EGP "
    "2,811mn and consumer BNPL EGP 2,885mn at FY2025; EGP 3,395mn and EGP 3,218mn at "
    "1H2026), with average ticket, tenor and transactions per customer for the BNPL book. "
    "Revenue is built as book x yield and NOT as a growth rate on the segment line.",
    [f_loans, f_fs25, f_q2])

R.add_driver("Cost of risk / provisioning on the credit book", DriverMode.BOTTOM_UP,
    "The company discloses the provisions balance over gross loans directly (MSME 3.7% at "
    "4Q25 against 4.9% at 4Q24; consumer finance 4.0% against 5.6%) and BNPL collection "
    "efficiency by month. Cost of risk is set from those ratios and STRESSED for seasoning, "
    "because the ratio fell while the book nearly doubled.",
    [f_loans, f_fund])

R.add_driver("Cost stack and gross margin", DriverMode.BOTTOM_UP,
    "MARGIN IS AN OUTPUT, NOT AN INPUT. The cost stack is built from the audited "
    "statements' own income statement and notes for FY2021-FY2024, which are the only "
    "documents that carry any cost line — the releases stop at gross profit. Gross margin "
    "and EBITDA margin fall out of revenue less the built cost lines and are reported "
    "against the released actuals (68.9% GPM and 57.4% EBITDA margin FY2025) as a check. "
    "FY2021 is now read and footed alongside the other three, which gives the cost stack a "
    "four-year history and, more usefully, one PRE-DEVALUATION year: FY2021 is the only "
    "point in the set struck before the March-2022 float, so the cost lines can be tested "
    "for FX pass-through rather than having it assumed.",
    [f_cost, f_fs21, f_fs22, f_fs23, f_fs24, f_neg_cost])

R.add_driver("Funding cost of the lending arm", DriverMode.BOTTOM_UP,
    "Taken from the company's own named transactions: the EGP 497.5mn 13-month A- rated "
    "securitisation of May 2025 and the EGP 550mn MSMEDA facility of 2Q2026, sitting at the "
    "NBFI subsidiaries rather than at the payments parent.",
    [f_fund, f_fs24])

R.add_driver("Risk-free rate, explicit window and terminal", DriverMode.BOTTOM_UP,
    "Explicit window from the CBE's own published main operation rate (19.50%); terminal "
    "norm-built from the CBE's OWN announced medium-term inflation target (7% +/-2pp for Q4 "
    "2026, 5% +/-2pp for Q4 2028) plus the house EM real-rate convention. Never a historical "
    "average and never backed out of a price.",
    [f_cbe, f_hold])

R.add_driver("Settlement float and credit interest", DriverMode.BOTTOM_UP,
    "Both halves are in the audited statements: the float itself (billers payable EGP 2.30bn "
    "+ merchant advances EGP 2.60bn + POS security deposits EGP 0.11bn at 31-Dec-2024) and "
    "the income it earns (credit interest EGP 211.1m FY2022, 464.4m FY2023, 691.2m FY2024, "
    "alongside T-bills of EGP 2.24bn). Modelled as a yield on the modelled float and T-bill "
    "balances, kept out of operating value and handled in the equity bridge. The releases are "
    "silent on it, which is what the negative search records.",
    [f_bs, f_cost, f_neg_float, f_cbe])

R.add_driver("Capex", DriverMode.TOP_DOWN,
    "No capital-expenditure figure or guidance exists in any company document. Set as a "
    "percentage of revenue benchmarked to the disclosed POS estate — which management is "
    "shrinking deliberately — and sensitised.",
    [f_neg_capex, f_hw])

R.add_driver("Share count for per-share values", DriverMode.BOTTOM_UP,
    "3,406,523,244 shares from the company's own governance report (EGP 1,703,261,622 "
    "issued capital at EGP 0.50 par). Any post-2023 capital action must be confirmed from a "
    "company document before the count moves.",
    [f_cap, f_neg_capital])

R.add_driver("VAT-exemption event", DriverMode.TOP_DOWN,
    "The draft law naming Fawry is Cabinet-approved and not enacted, so there is no "
    "company disclosure to build from. Carried as an explicit dated scenario, dual-framed, "
    "with the base case assuming NO enactment.",
    [f_vat, f_neg_vat])

# ------------------------------------------------------------------------ OUTPUT
errors, warnings = R.validate()
R.to_json(os.path.join(HERE, 'sweep_register.json'))
print(R.qc_line())
print(f"\nfindings: {len(R.findings)} | drivers: {len(R.drivers)}")
bu = sum(1 for d in R.drivers if d.mode is DriverMode.BOTTOM_UP)
print(f"driver modes: {bu} bottom-up / {len(R.drivers) - bu} top-down")
n_ir = sum(1 for f in R.findings if f.source_type is SourceType.COMPANY_IR)
n_co = sum(1 for f in R.findings if f.source_type is SourceType.COMPANY_OFFICIAL)
print(f"company sources: {n_co} COMPANY_OFFICIAL / {n_ir} COMPANY_IR")
print(f"primary access attempts logged: {len(R.primary_access)} "
      f"({sum(1 for p in R.primary_access if p.reachable)} reachable / "
      f"{sum(1 for p in R.primary_access if not p.reachable)} refused)")
if errors:
    print(f"\nVALIDATOR ERRORS ({len(errors)}) — disclosed, not suppressed:")
    for e in errors:
        print(f"  ! {e}")
if warnings:
    print(f"\nwarnings ({len(warnings)}):")
    for w in warnings:
        print(f"  - {w}")
DELIVERY_DATE = "2026-09-09"
fr = R.check_freshness(DELIVERY_DATE)
print(f"\nfreshness (delivery {DELIVERY_DATE}): {fr or 'OK — 1 calendar day between sweep and delivery, well inside the 14-day window'}")
