"""COMI (Commercial International Bank - Egypt S.A.E., EGX) — four-ring Step 2A
Information Sweep register. FIRST-BUILD study; this ticker had no study directory.

Runs BEFORE any forecast driver is set. Every mandatory category of every ring is
closed by a dated finding or a dated negative search.

THIS IS A BANK, AND THE LENS SET IS THE BANK ROW OF research_protocol.LENS_REGISTRY:
dividend discount model primary, residual income beside it, relative multiple, book
value as a disclosed floor. THE OPERATING-COMPANY DRIVER SET WAS DELIBERATELY NOT
SWEPT FOR. There is no volume x price, no cost per unit, no utilisation and no
nameplate capacity here, because a bank has none of those things: its revenue is a
spread earned on a balance sheet, its cost of goods is interest paid to depositors,
and its "unit" is a pound of earning assets. The sweep reached the inputs the bank
lens actually needs instead — net interest income decomposed by earning-asset class,
the loan and deposit books by segment and by currency, the stage-1/2/3 expected-credit-
loss disclosure and the cost of risk, regulatory capital against the CBE minimum, the
dividend and payout history, and the Central Bank of Egypt policy-rate exposure. Where
a ring category exists only because the taxonomy is written for operating companies,
it is closed by a finding that says so, not left blank.

SOURCING EXCEPTIONS, RECORDED RATHER THAN HIDDEN
================================================
(1) cibeg.com IS FULLY BLOCKED AT THIS ENVIRONMENT'S EGRESS. Every www.cibeg.com URL
    tried — the IR landing page, the IR library, the financial-statements index, the
    annual-report PDF, three earnings-release PDFs and the yomo newsroom item —
    returned HTTP 200 carrying a 212-byte Imperva/Incapsula challenge interstitial
    rather than the document. ir.cibeg.com failed CONNECT with a 502 at the proxy;
    the bare host cibeg.com failed TLS with "unrecognized name". Eleven attempts are
    logged below, each with its outcome.

(2) THE COMPANY'S OWN FILINGS WERE REACHED BY THE OTHER PRIMARY ROUTE THE ISSUER
    PUBLISHES ON. CIB has a GDR listed in London (CBKD) and files the same documents
    to the LSE's Regulatory News Service; the attachments live at
    rns-pdf.londonstockexchange.com and were retrievable. Seven of CIB's own PDFs
    were downloaded that way and are held in engine/comi_study_pending/filings/. That is an
    exchange filing portal carrying the issuer's own document, so those findings are
    tagged COMPANY_OFFICIAL (statements) or COMPANY_IR (earnings releases) —
    NOT a vendor, NOT press, and NOT an aggregator.

(3) [R-SIGCM-03] FALLBACK USED ONCE, AND NAMED. THE AUDITED CBE-BASIS ANNUAL
    STATEMENTS COULD NOT BE REACHED. CIB publishes TWO annual sets: an IFRS
    consolidated set, and the separate + consolidated statements prepared under the
    Central Bank of Egypt rules of 16-Dec-2008, which are the ones the Ordinary
    General Assembly ratified on 15-Mar-2026 and the ones the quarterly interims and
    the earnings releases sit on. Only the IFRS set was retrievable via RNS. The
    CBE-basis annual figures therefore enter this register through the company's own
    earnings release (F28) and the comparative column of its own interim statements
    (F20/F21) — the company's own documents, the named fallback, not a substitute
    from outside the company. The gap is a live finding (F41), not a footnote.

(4) THE 2Q26 EARNINGS RELEASE HAS NO PDF ATTACHMENT ON RNS. RNS 1122N (21-Jul-2026)
    was published as announcement body text; eight URL variants were tried on
    rns-pdf and none exists, and the issuer's own PDF sits behind the Incapsula block
    in (1). Its release-only anchors — NIM by currency, CASA share, loan-to-deposit,
    NPL and coverage, CET1, ROAE — were read from the RNS announcement body via the
    LSE RNS distribution mirrors (Investegate, ticker.app) and are tagged COMPANY_IR
    with the document named and the route stated in the finding. EVERY FIGURE IN THAT
    RELEASE THAT ALSO APPEARS IN A STATEMENT WAS CROSS-CHECKED AND TIED: net interest
    income EGP 60,826mn, capital adequacy 28.4% and net profit EGP 39,314mn all match
    the interim condensed consolidated statements retrieved as a primary PDF. Nothing
    is carried on the mirror alone that a primary document could settle.

(5) ARITHMETIC IS THE ARBITER, AND EVERY STATEMENT PAGE USED WAS FOOTED. All four
    annual income statements and balance sheets (FY2022, FY2023, FY2024, FY2025), both
    2026 interims, the capital-adequacy note, the stage-1/2/3 tables, the net-interest-
    income note, the deposits note and the retained-earnings note were re-added against
    their own printed subtotals. ALL FOOT TO THE POUND, both current and comparative
    columns; the pdftotext text layer is therefore accepted as sound and no page needed
    OCR re-reading. TWO DOCUMENTS CARRIED NO TEXT LAYER AT ALL and were read by OCR off
    the rendered pixels at 110 dpi: the 15-Mar-2026 OGA resolutions summary (source of
    the EGP 6.00 dividend per share) and the 9-Feb-2026 board resolution summary
    (source of the ESOP capital increase). The route is recorded on each finding.
"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from research_sweep import (SweepRegister, AssetClass, Ring, FindingClass,
                            SourceType, DriverMode)

SWEEP_DATE = "2026-09-08"
R = SweepRegister("COMI", AssetClass.STOCK, SWEEP_DATE)
CO, IR, REG, PMD, PRESS, AGG = (SourceType.COMPANY_OFFICIAL, SourceType.COMPANY_IR,
                                SourceType.REGULATOR_OFFICIAL, SourceType.PRIMARY_MARKET_DATA,
                                SourceType.REPUTABLE_PRESS, SourceType.AGGREGATOR)

# ---------------------------------------------------------------------------
# PRIMARY ACCESS — the company's own site tried FIRST for every Company-ring
# figure, and every attempt logged with its outcome, success or failure.
# ---------------------------------------------------------------------------
BLOCK = ("HTTP 200 carrying a 212-byte Imperva/Incapsula challenge interstitial "
         "(<iframe src=/_Incapsula_Resource...>), not the document. The origin WAF "
         "refuses this environment's egress; the block is silent in the status code, "
         "which is exactly why the byte count is recorded here.")
for u in ("https://www.cibeg.com/en/investor-relations",
          "https://www.cibeg.com/en/investor-relations/financial-information",
          "https://www.cibeg.com/en/investor-relations/ir-library/financial-statements",
          "https://www.cibeg.com/-/media/project/downloads/investor-relations/ir-library/"
          "annual-reports/2025/cib-ar-2025-final.pdf",
          "https://www.cibeg.com/-/media/project/downloads/investor-relations/ir-library/"
          "earning-releases/2025/3q25-press-release.pdf",
          "https://www.cibeg.com/-/media/project/downloads/investor-relations/ir-library/"
          "earning-releases/2026/2q26-press-release.pdf",
          "https://www.cibeg.com/en/newsroom/news/8-20-2026-yomo-announcement"):
    R.record_primary_access(u, False, SWEEP_DATE, BLOCK)
R.record_primary_access("https://ir.cibeg.com", False, SWEEP_DATE,
                        "curl (56) CONNECT tunnel failed, response 502 at the proxy — "
                        "host does not resolve to a served IR site.")
R.record_primary_access("https://cibeg.com", False, SWEEP_DATE,
                        "TLS handshake failed: OpenSSL error 0A000458 'tlsv1 "
                        "unrecognized name' — the bare host serves no certificate for "
                        "itself; only www.cibeg.com does, and that is blocked above.")
R.record_primary_access("https://www.rns-pdf.londonstockexchange.com/rns/", True, SWEEP_DATE,
                        "REACHED. CIB files to the LSE RNS for its GDR (CBKD); the "
                        "attachments are the issuer's own PDFs. Seven downloaded and "
                        "held in engine/comi_study_pending/filings/: FY2022 (5862T), FY2023 "
                        "(7294C), FY2024 (5950X) and FY2025 (3239S) IFRS consolidated "
                        "statements; 1Q26 (9499D) and 2Q26 (1119N) interim condensed "
                        "consolidated statements; FY25 (3242S) and 1Q26 (9517D) earnings "
                        "releases; 15-Mar-2026 OGA resolutions (6754W); 9-Feb-2026 board "
                        "resolutions (3251S); 3-Dec-2025 bonus-share notice (1167K).")
R.record_primary_access("https://www.rns-pdf.londonstockexchange.com/rns/1122N_*", False,
                        SWEEP_DATE,
                        "NO ATTACHMENT EXISTS for the 2Q26 Earnings Release (RNS 1122N, "
                        "21-Jul-2026). Eight URL variants tried across 2026-7-16..23 and "
                        "sequence suffixes _1 and _2; all 404 or 500. The release is an "
                        "RNS body-text announcement. See docstring note (4).")
R.record_primary_access("https://www.egx.com.eg/en/DisclosureAll.aspx", True, SWEEP_DATE,
                        "Exchange reachable (HTTP 200) but the disclosure index is an "
                        "ASP.NET postback shell; no per-issuer COMI disclosure list or "
                        "document URL is retrievable without a browser session.")

R.declare_study_year("2026", ["Q1-2026", "Q2-2026"])

# ============================================================ RING 1 — GLOBAL
f_fed = R.add(Ring.GLOBAL, "rate cycle & USD/FX regime", FindingClass.S,
    "Fed on hold at a 3.50-3.75% target range (29-Jul-2026, 9-3 vote with three "
    "dissents FOR a hike); next FOMC 16-Sep-2026. Egypt's own easing cycle stalled "
    "with it — the CBE has now held four consecutive meetings. EGP ~51.05/USD on "
    "08-Sep-2026; the pound DEPRECIATED EGP 6.9 through Q1-2026 and then APPRECIATED "
    "EGP 5.37 through Q2-2026",
    "US Federal Reserve FOMC statement and minutes 28-29 Jul 2026; EGP/USD spot",
    REG, "2026-07-29",
    model_impact="Sets the external anchor under the FOREIGN-CURRENCY NIM leg, which is "
                 "a separately disclosed driver here (FC NIM 2.17% in H1-2026 against "
                 "LC NIM 12.3%). A US rate on hold holds the FC leg's floor up. The EGP "
                 "path drives the translation of a balance sheet that is 28% foreign "
                 "currency, and the swing from a Q1 depreciation to a Q2 appreciation is "
                 "why 'real growth net of the FX impact' must be modelled separately "
                 "from reported growth.")

f_cmdty = R.add(Ring.GLOBAL, "commodity complex (input/output)", FindingClass.C,
    "A BANK HAS NO INPUT OR OUTPUT COMMODITY, and the category is closed by saying so "
    "rather than by silence. CIB buys no raw material and sells no unit: its cost of "
    "goods is interest paid to depositors (EGP 104.1bn in FY2025) and its revenue is a "
    "spread. The commodity complex reaches it only INDIRECTLY, through Egypt's imported "
    "food and energy bill into CPI and thence into the CBE policy rate. CIB's own 1Q26 "
    "release makes exactly that link: 'an upward flight in global inflation sparked, "
    "bringing all monetary easing plans across the globe to a halt... That inevitably "
    "transmitted to the Egyptian Economy, with the CBE putting-on-hold the anticipated "
    "series of policy-rate cuts'",
    "CIB First-Quarter 2026 News Release, 11 May 2026 (RNS 9517D), management commentary",
    IR, "2026-05-11", model_impact="",
    detail="Recorded so a reviewer can see the operating-company driver set was "
           "considered and ruled out on the class, not overlooked.")

f_gsect = R.add(Ring.GLOBAL, "global sector demand", FindingClass.S,
    "Falling policy rates are compressing bank margins across the emerging-market "
    "complex, and Egypt is inside that pattern rather than outside it: the Egyptian "
    "sector's average NIM is running ~5.2% (Mar-2026) and is expected to ease to ~5.5% "
    "from 5.8% a year earlier on lower treasury yields. CIB sits far above the sector "
    "at 8.61% (H1-2026) — the gap, not the level, is the thing to forecast",
    "Fitch Ratings commentary on Egyptian bank margin compression (reported); Egyptian "
    "banking-sector aggregates for Mar-2026",
    PRESS, "2026-05-02",
    model_impact="Frames the NIM path as a CONVERGENCE question rather than a level "
                 "assumption: the forecast must say why CIB's 3.4pp premium over the "
                 "sector persists or decays, and sensitise it.")

f_trade = R.add(Ring.GLOBAL, "trade / sanctions / supply chains", FindingClass.S,
    "Egypt's external position has rebuilt: international reserves USD 52.8bn "
    "(Mar-2026) and a record banking-sector net foreign asset position of ~USD 30bn, on "
    "recovered tourism, remittances and Suez traffic. That is the supply of the foreign "
    "currency CIB on-lends",
    "S&P Global sovereign review of Egypt (Apr-2026) and Egyptian banking-sector net "
    "foreign asset data, as reported",
    PRESS, "2026-04-14",
    model_impact="Drives the FOREIGN-CURRENCY DEPOSIT growth driver, which is modelled "
                 "in USD and translated, not in EGP. CIB's own FC deposits grew USD "
                 "993mn (+12%) in FY2025 and USD 172mn (+2%) in Q1-2026 — the second "
                 "number is the one that shows the funding tap tightening.")

# =========================================================== RING 2 — COUNTRY
f_cbe = R.add(Ring.COUNTRY, "sovereign macro (inflation, policy rate, FX/deval risk)",
    FindingClass.D,
    "CBE policy corridor read off the regulator's own page on the sweep date: overnight "
    "DEPOSIT rate 19.00%, overnight LENDING rate 20.00%, 'Last Updated 12 Feb 2026, "
    "Effective from 15 Feb 2026'. Main operation and discount rates 19.50%. Held at the "
    "20-Aug-2026 MPC, the fourth consecutive hold since the 100bp cut of Feb-2026. "
    "Cumulative cuts were 725bp through 2025 and 825bp over the year to Q1-2026",
    "Central Bank of Egypt — Overnight Deposit and Lending Rate statistics page, "
    "cbe.org.eg, retrieved 08-Sep-2026",
    REG, "2026-02-12",
    url="https://www.cbe.org.eg/en/economic-research/statistics/overnight-deposit-and-lending-rate",
    model_impact="DRIVER UNLOCK, and the single most consequential external number in "
                 "this study. It sets (a) the explicit-window risk-free rate in Ke, and "
                 "(b) the repricing input to the local-currency NII build — CIB's loan "
                 "book is predominantly variable-rate against a deposit book that is 18% "
                 "non-interest-bearing, so the policy rate moves asset yields faster than "
                 "funding costs in both directions.")

f_cpi = R.add(Ring.COUNTRY, "sovereign macro (inflation, policy rate, FX/deval risk)",
    FindingClass.S,
    "Egyptian annual urban headline inflation re-accelerated to 14.9% in July 2026 from "
    "14.3% in June — the first rise since March — with core CPI at 14.7% and the "
    "all-Egypt headline at 13.0%. Housing, transport and education led",
    "CAPMAS monthly CPI release for July 2026, as reported",
    PRESS, "2026-08-10",
    model_impact="Sets the terminal risk-free rate build and the cost-inflation "
                 "escalator on administrative expenses. A re-accelerating CPI is the "
                 "mechanism that keeps the CBE on hold, which HOLDS THE MARGIN UP in the "
                 "near term and is therefore a bull input to FY2026-27 NII and a bear "
                 "input to the terminal margin — dual-framed, not netted.")

f_reg = R.add(Ring.COUNTRY, "regulatory environment (regulator, caps, tariffs, tax/subsidy)",
    FindingClass.D,
    "The regulatory capital floor, from the bank's own capital-adequacy note: the CBE "
    "requires a MINIMUM CAR OF 12.75% inclusive of the conservation buffer and the D-SIB "
    "surcharge, and a minimum issued and paid-in capital of EGP 5bn (CIB is at EGP "
    "33.8bn). CBE liquidity minima are 20% local currency and 25% foreign currency. "
    "Tier 2 admits stage-1 ECL only up to 1.25% of credit-risk-weighted assets, and "
    "subordinated loans only up to 50% of Tier 1. Data is filed to the CBE monthly",
    "CIB FY2025 IFRS Consolidated Financial Statements, note 34.5 'Capital management', "
    "RNS 3239S filed 09-Feb-2026",
    CO, "2026-02-09", is_fs_data=True, fiscal_period="FY2025",
    model_impact="DRIVER UNLOCK for the dividend lens. The DDM's payout path is bounded "
                 "by the distance between the actual CAR (27.3% at Dec-2025, 28.4% at "
                 "Jun-2026) and this 12.75% floor, given risk-weighted-asset growth. "
                 "Without the floor the payout is an assumption; with it, it is a "
                 "constraint the model must respect explicitly.")

f_ecl_reg = R.add(Ring.COUNTRY, "regulatory environment (regulator, caps, tariffs, tax/subsidy)",
    FindingClass.S,
    "A CBE instruction, not an accounting choice, governs what CIB may pay out of the "
    "FY2025 ECL-model release: the released provision 'is neither recognized in the "
    "Bank's Capital Base and Capital Adequacy Ratio (CAR) nor in its Net Profit "
    "Available for Distribution, as per CBE Instructions'. EGP 13,145,012 thousand was "
    "transferred out of FY2025 net profit into a special reserve",
    "CIB Full-Year 2025 News Release, 9 Feb 2026 (RNS 3242S), management commentary; "
    "CIB FY2025 IFRS Consolidated FS, note 31.8 retained-earnings movement",
    IR, "2026-02-09",
    model_impact="Directly caps the DDM numerator. The FY2025 dividend is 25% of "
                 "REPORTED net profit but 30% of the DISTRIBUTABLE portion, and the "
                 "difference is this reserve. Any payout path built off reported "
                 "earnings without this adjustment over-pays the shareholder.")

f_tax = R.add(Ring.COUNTRY, "fiscal / political events with sector read-through",
    FindingClass.D,
    "Effective tax rate 27.98% in FY2025 and 30.60% in FY2024 against a 22.5% statutory "
    "rate. The reconciliation (note 10.1) shows why: EGP 16,172,168 thousand of "
    "withholding tax in FY2025 (EGP 9,392,763 in FY2024) added on top of EGP 23,580,762 "
    "of tax on accounting profit, against EGP 19,099,995 of exemptions",
    "CIB FY2025 IFRS Consolidated FS, note 10.1 effective-tax-rate reconciliation, "
    "RNS 3239S",
    CO, "2026-02-09", is_fs_data=True, fiscal_period="FY2025",
    model_impact="DRIVER UNLOCK: the tax driver is built from this reconciliation, not "
                 "from the statutory rate. Withholding tax on treasury income is the "
                 "swing item, so the tax rate MOVES WITH THE SOVEREIGN-PAPER SHARE of "
                 "the earning-asset mix rather than sitting flat at 22.5%.")

f_sov = R.add(Ring.COUNTRY, "fiscal / political events with sector read-through",
    FindingClass.S,
    "Egypt rated B/B stable by S&P (affirmed Apr-2026), B stable by Fitch, Caa1 positive "
    "by Moody's; general government debt seen falling to ~89% of GDP by Jun-2026 from a "
    "2023 peak of ~94%. This is not background for this issuer: EGP 619.8bn of CIB's "
    "Jun-2026 balance sheet is government and debt securities, close to its EGP 638.4bn "
    "gross loan book, so the sovereign IS the largest single credit exposure",
    "S&P Global sovereign rating action on Egypt (Apr-2026), as reported; exposure "
    "figures from CIB's own Jun-2026 interim currency and investment tables",
    PRESS, "2026-04-14",
    model_impact="Sets the sovereign-risk premium netted OUT of the local risk-free rate "
                 "in Ke (never charged twice, [L-004]), and is the stated reason the "
                 "residual-income cross-check is run on a stressed sovereign-yield case "
                 "as well as the base.")

# ========================================================== RING 3 — INDUSTRY
f_sector = R.add(Ring.INDUSTRY, "demand drivers & capacity/supply balance", FindingClass.S,
    "Egyptian banking-sector shape as of the sweep: banks operating in Egypt earned a "
    "record EGP 218.4bn of net profit in Q1-2026; sector ROAE 33.9%, ROAA 2.6%, NIM 5.2% "
    "(Mar-2026); NPLs 1.9% of loans with 90.2% provision coverage and sector CAR 19.6% "
    "at end-2025. Deposit shares at Jun-2025: NBE 36.61%, Banque Misr 18.67%, CIB 6.99%, "
    "QNB Alahli 4.71%",
    "Central Bank of Egypt financial soundness indicators and sector aggregates, as "
    "reported; Egyptian banking-sector deposit market-share tables",
    PRESS, "2026-07-05",
    model_impact="Sets the market-growth denominator for CIB's own disclosed share "
                 "drivers (5.26% of loans, 6.81% of deposits at Sep-2025). Share x market "
                 "is the cross-check on the bottom-up loan and deposit build, never its "
                 "source.")

f_price = R.add(Ring.INDUSTRY, "pricing", FindingClass.D,
    "The price in this industry is the SPREAD, and CIB discloses its own to the basis "
    "point and by currency: total NIM 8.95% FY2025 (-53bp YoY), 8.88% Q1-2026 (-24bp "
    "YoY), 8.61% H1-2026 (-35bp YoY), 8.36% in Q2-2026 alone. Split: local currency "
    "13.0% FY2025 -> 12.7% Q1-2026 -> 12.3% H1-2026; foreign currency 2.50% FY2025 -> "
    "2.18% Q1-2026 -> 2.17% H1-2026. Deposit competition is intensifying against "
    "non-bank substitutes (below)",
    "CIB FY25, 1Q26 and 2Q26 Earnings Releases (RNS 3242S, 9517D, 1122N)",
    IR, "2026-07-21",
    model_impact="DRIVER UNLOCK: converts the margin from a single blended assumption "
                 "into TWO priced legs with their own paths and their own drivers — a "
                 "local-currency leg that tracks the CBE corridor and CASA mix, and a "
                 "foreign-currency leg that tracks the Fed and FC funding cost. The "
                 "blended NIM then falls out as an OUTPUT of mix, which is the point: a "
                 "flat blended NIM would have hidden that the FC leg has lost 33bp in "
                 "six months while the LC leg lost 70bp.")

f_entrants = R.add(Ring.INDUSTRY, "new entrants (named-competitor level)", FindingClass.S,
    "Egypt's digital-bank cohort arrived inside the forecast window, named: onebank "
    "(Banque Misr's Misr Digital Innovation) took its FINAL CBE licence in Mar-2026 and "
    "is targeting ~800,000 customers and EGP 40bn of deposits in year one; CIB's own "
    "yomo took PRELIMINARY approval on 19-Aug-2026 for a 4Q-2026 launch; OPay has filed "
    "for a licence and the CBE says more applications are under review. The CBE also "
    "approved fully-online customer onboarding in Aug-2026, which removes the branch "
    "moat",
    "Central Bank of Egypt licensing decisions and digital-bank framework (2023), as "
    "reported; CIB's own yomo announcement of 19-Aug-2026",
    PRESS, "2026-08-25",
    model_impact="Sets the DEPOSIT-COST and CASA-SHARE drivers' downside case. A "
                 "digitally-native competitor bidding for retail current accounts is a "
                 "direct attack on the 63% CASA share that is currently holding CIB's "
                 "local-currency margin up. Modelled as a CASA-erosion sensitivity on "
                 "the LC NIM leg, not as a revenue haircut.")

f_subst = R.add(Ring.INDUSTRY, "technology substitution", FindingClass.S,
    "The substitution threat to this issuer is not to its technology but to its FUNDING: "
    "money-market fund assets in Egypt rose from EGP 316bn at end-2025 to EGP 411bn by "
    "Mar-2026, and the government's Citizen Bond at a net 17.75% has drawn EGP 7.7bn — "
    "both taking flows that used to arrive as bank deposits. CIB's own management names "
    "it: 'new alternative assets such as money market funds redefining the domestic "
    "liquidity, thus resulting in a new operating reality that is expected to bring "
    "about thinner margins across the sector'",
    "CIB First-Quarter 2026 News Release, 11 May 2026 (RNS 9517D), management commentary; "
    "Egyptian mutual-fund and Citizen Bond flow data as reported",
    IR, "2026-05-11",
    model_impact="The single most credible mechanism for terminal-margin decay, and it "
                 "comes from the company's own mouth rather than from a house view. "
                 "Sets the terminal NIM below the current level and is the stated basis "
                 "for the bear case in the sensitivity grid.")

f_peers = R.add(Ring.INDUSTRY, "competitor capacity / price moves (named)", FindingClass.S,
    "Named private-sector peers are growing the same book: QNB Alahli Egypt gross loans "
    "EGP 498.5bn (+7%) and customer deposits EGP 878.8bn (+13%) at Mar-2026; NBE's "
    "corporate and syndicated portfolio ~EGP 5.5tn at Jun-2026 (+14%). Banks are openly "
    "competing for deposits while the CBE holds rates",
    "QNB Alahli and National Bank of Egypt disclosed results for Mar/Jun-2026, as "
    "reported",
    PRESS, "2026-09-05",
    model_impact="Sets the peer set for the relative-multiple cross-check (price-to-book "
                 "against ROE, never a trailing P/E on a year that carries a provision "
                 "release), and evidences that CIB's 18% deposit growth is a market-wide "
                 "rate rather than a share gain — which is what stops the deposit driver "
                 "from being extrapolated as if it were company-specific.")

# =========================================================== RING 4 — COMPANY
# ---- official financial statements: four complete fiscal years, from the filings
f_fs25 = R.add(Ring.COMPANY, "official financial statements", FindingClass.D,
    "FY2025 IFRS consolidated, signed 9-Feb-2026 by the Group CFO and the CEO: interest "
    "income EGP 211,600,177k less interest expense EGP 104,121,746k = net interest "
    "income EGP 107,478,431k; net fee and commission EGP 9,219,043k; net impairment "
    "RELEASED EGP 11,804,786k; profit before tax EGP 104,803,388k; tax EGP 29,323,206k; "
    "net profit EGP 75,480,182k (parent EGP 75,460,219k); basic EPS EGP 22.34. Balance "
    "sheet: total assets EGP 1,445,486,499k, total liabilities EGP 1,221,060,441k, total "
    "equity EGP 224,426,058k",
    "CIB IFRS Consolidated Financial Statements, December 2025 (RNS 3239S, filed "
    "09-Feb-2026), income statement and statement of financial position",
    CO, "2026-02-09", is_fs_data=True, fiscal_period="FY2025",
    detail="FOOTED: every subtotal re-added against its own printed figure — NII, net "
           "fee, the nine-line walk to PBT, PBT to net profit, the parent/NCI split, all "
           "15 asset lines to total assets, all 10 liability lines, the four equity "
           "lines, L+E to total, and the comprehensive-income statement. All differences "
           "zero. Text layer accepted; no OCR needed.",
    model_impact="The anchor year of the historical series and the base the forecast "
                 "rolls forward from. Note the FY2024 comparative column here is "
                 "RESTATED against the FY2024 filing (see F41) — the study uses one "
                 "vintage per line and says which.")

f_fs24 = R.add(Ring.COMPANY, "official financial statements", FindingClass.D,
    "FY2024 IFRS consolidated, signed 18-Feb-2025: interest income EGP 182,735,474k less "
    "EGP 91,751,450k = NII EGP 90,984,024k; net trading income EGP 20,470,230k; "
    "impairment charge EGP 4,523,819k; PBT EGP 71,498,028k; net profit EGP 49,619,082k; "
    "basic EPS EGP 16.34 as printed. Total assets EGP 1,216,838,678k, liabilities EGP "
    "1,069,865,756k, equity EGP 146,972,922k",
    "CIB Annual Financial Report — IFRS Consolidated Financial Statements December 2024 "
    "(RNS 5950X, filed 19-Feb-2025)",
    CO, "2025-02-19", is_fs_data=True, fiscal_period="FY2024",
    detail="FOOTED to the pound on both the FY2024 and FY2023 columns, income statement "
           "and balance sheet. Text layer accepted.",
    model_impact="Second historical year. Carries the devaluation-year distortions that "
                 "make it unusable as a normalisation base without adjustment — see F33.")

f_fs23 = R.add(Ring.COMPANY, "official financial statements", FindingClass.D,
    "FY2023 IFRS consolidated: interest income EGP 104,028,379k less EGP 51,142,688k = "
    "NII EGP 52,885,691k; impairment charge EGP 4,270,081k; PBT EGP 38,560,655k; net "
    "profit EGP 26,576,147k; basic EPS EGP 8.84 as printed. Total assets EGP 836,035,956k, "
    "liabilities EGP 748,497,944k, equity EGP 87,538,012k",
    "CIB Q4.23 Consolidated Financial Statements — IFRS (RNS 7294C, filed 12-Feb-2024)",
    CO, "2024-02-12", is_fs_data=True, fiscal_period="FY2023",
    detail="FOOTED on both columns. Text layer accepted.",
    model_impact="Third historical year — the pre-devaluation reference point for the "
                 "margin and the balance-sheet mix.")

f_fs22 = R.add(Ring.COMPANY, "official financial statements", FindingClass.D,
    "FY2022 IFRS consolidated (comparative column of the FY2023 filing, and separately "
    "filed as RNS 5862T): interest income EGP 55,723,701k less EGP 24,828,159k = NII EGP "
    "30,895,542k; PBT EGP 22,392,634k; net profit EGP 14,619,143k; basic EPS EGP 4.85. "
    "Total assets EGP 642,066,498k, liabilities EGP 575,278,342k, equity EGP 66,788,156k",
    "CIB FY22 IFRS 9 Financial Statements (RNS 5862T, 20-Mar-2023) and the comparative "
    "column of the FY2023 filing (RNS 7294C)",
    CO, "2023-03-20", is_fs_data=True, fiscal_period="FY2022",
    detail="FOOTED on the FY2022 column of the FY2023 filing. Text layer accepted.",
    model_impact="Fourth historical year, taking the series to the protocol's TARGET "
                 "depth of four rather than its floor of two. Fixes the pre-2024 "
                 "normalised ROE the residual-income lens is anchored on.")

f_q1 = R.add(Ring.COMPANY, "official financial statements", FindingClass.D,
    "Q1-2026 interim condensed consolidated (period ended 31-Mar-2026, board-approved): "
    "NII EGP 29,699,580k; PBT EGP 25,563,151k; net profit EGP 17,822,042k; basic EPS EGP "
    "4.65. Total assets EGP 1,568,267,810k; due to customers EGP 1,214,998,089k; equity "
    "incl. NCI EGP 216,173,033k",
    "CIB Consolidated Financial Statements 1Q26 — Interim Condensed, March 2026 "
    "(RNS 9499D, 12-May-2026)",
    CO, "2026-05-12", is_fs_data=True, fiscal_period="Q1-2026",
    detail="FOOTED: 12 asset lines, 9 liability lines, 4 equity lines, L+E, NII and the "
           "nine-line PBT walk — all zero difference. Text layer accepted.",
    model_impact="First quarter of the study year, swept BEFORE the build. Q1's own NIM "
                 "of 8.88% sits ABOVE the H1 average, which means the Q2 figure carried "
                 "the whole decline — a fact that a half-year-only sweep would have "
                 "missed entirely.")

f_q2 = R.add(Ring.COMPANY, "official financial statements", FindingClass.D,
    "Q2/H1-2026 interim condensed consolidated (period ended 30-Jun-2026, board-approved "
    "20-Jul-2026): Q2 alone NII EGP 31,126,568k, PBT EGP 28,595,893k, net profit EGP "
    "21,491,684k, EPS EGP 5.61; H1 NII EGP 60,826,148k, PBT EGP 54,159,044k, net profit "
    "EGP 39,313,726k, EPS EGP 10.23. Total assets EGP 1,690,039,928k; loans and advances "
    "to customers net EGP 597,785,831k; due to customers EGP 1,308,646,344k; equity incl. "
    "NCI EGP 238,416,239k. CAR 28.4%, leverage 11.5%, NSFR 186%, LCR 674%",
    "CIB Condensed Consolidated Financial Statements June 30, 2026 (RNS 1119N, "
    "21-Jul-2026), reviewed, review report attached",
    CO, "2026-07-21", is_fs_data=True, fiscal_period="Q2-2026",
    detail="FOOTED: 12 asset lines, 9 liability lines, equity, L+E, and the Q2, H1-2026 "
           "and H1-2025 income-statement columns — all zero difference. Text layer "
           "accepted.",
    model_impact="The most recent hard number in the study and the roll-forward base. "
                 "Supersedes every earlier balance-sheet anchor.")

# ---- regular disclosures: the notes the bank lens actually runs on
f_nii = R.add(Ring.COMPANY, "regular disclosures", FindingClass.D,
    "NET INTEREST INCOME DECOMPOSED BY EARNING-ASSET CLASS (note 3), which is what makes "
    "a bottom-up NII build possible. FY2025 interest income EGP 211,600,177k = banks "
    "20,066,633 + clients 94,424,365 + treasury bills, bonds and other governmental "
    "notes 89,324,621 + debt instruments at FVOCI and amortised cost 7,784,558. "
    "SOVEREIGN PAPER IS 42% OF INTEREST INCOME, more than customer loans is not, but "
    "close. Interest expense EGP 104,121,746k = banks 9,112,525 + clients 91,747,074 + "
    "repos 14,908 + lease finance 221,200 + other loans 2,835,376 + issued debt 190,663",
    "CIB FY2025 IFRS Consolidated FS, note 3 'Net interest income' (RNS 3239S)",
    CO, "2026-02-09", is_fs_data=True, fiscal_period="FY2025",
    detail="FOOTED: both sub-totals and the grand totals on both the FY2025 and FY2024 "
           "columns.",
    model_impact="DRIVER UNLOCK, and the reason the NII driver is bottom-up rather than "
                 "a margin assumption. Yield per class is solved as interest income by "
                 "class over the period-average balance of that class from the balance "
                 "sheet. THE DISCLOSURE GAP IS FLAGGED: CIB publishes no average-balance "
                 "table, so average balances are opening/closing means, not daily "
                 "averages — the level this drops to and why is stated in the study.")

f_stages = R.add(Ring.COMPANY, "regular disclosures", FindingClass.D,
    "STAGE 1 / 2 / 3 EXPECTED-CREDIT-LOSS DISCLOSURE, by segment, for three dates. "
    "Dec-2025 gross loans to customers EGP 546,260,235k = stage 1 427,519,888 + stage 2 "
    "108,806,857 + stage 3 9,933,490; ECL EGP 34,687,756k = 7,231,807 + 19,797,922 + "
    "7,658,027. Dec-2024: gross 392,383,044 = 265,175,549 + 113,952,542 + 13,254,953; "
    "ECL 45,481,562 = 10,283,121 + 24,751,028 + 10,447,413. Jun-2026: gross 638,366,662 = "
    "523,678,573 + 103,791,178 + 10,896,911; ECL 36,686,288 = 8,934,230 + 19,555,664 + "
    "8,196,394. Split individuals vs corporate and business banking at every date. "
    "Off-balance-sheet facilities and guarantees carried separately (Jun-2026: EGP "
    "331,998,859k exposure, EGP 12,871,313k ECL)",
    "CIB FY2025 IFRS Consolidated FS note 17.1 and the June 2026 interim note 3 "
    "(RNS 3239S, 1119N)",
    CO, "2026-07-21", is_fs_data=True, fiscal_period="Q2-2026",
    detail="FOOTED: every stage row and column at all three dates, plus the gross-to-net "
           "reconciliation (546,260,235 - 34,687,756 - 82,363 - 40,820 - 3,495,530 = "
           "507,953,766 as printed). ALL ZERO. Note that STAGE 3 IS NOT THE NPL RATIO: "
           "stage 3 is 1.82% of gross loans at Dec-2025 while the release's standalone "
           "NPL ratio is 1.67% — different definitions, and the study must not mix them.",
    model_impact="DRIVER UNLOCK for cost of risk. The charge is built as a stage-"
                 "migration model — stage 2 fell from 29.0% of the book at Dec-2024 to "
                 "19.9% at Dec-2025 to 16.3% at Jun-2026, and THAT migration, not a "
                 "flat basis-point assumption, is what produced the FY2025 release.")

f_deps = R.add(Ring.COMPANY, "regular disclosures", FindingClass.D,
    "THE DEPOSIT BOOK, cut four ways in the company's own note. Jun-2026 total EGP "
    "1,308,646,344k: by product — demand 554,043,991 + time 215,014,198 + certificates "
    "of deposit 273,675,783 + saving 257,277,289 + other 8,635,083; by customer — "
    "corporate 565,036,367 / individual 743,609,977; BY RATE TYPE — non-interest-bearing "
    "235,620,875, floating 36,154,372, fixed 1,036,871,097; by tenor — current "
    "1,034,333,353 / non-current 274,312,991. Dec-2025 the same four ways (total EGP "
    "1,110,395,693k, non-interest-bearing 201,838,067). BY CURRENCY at Jun-2026: EGP "
    "852,436,348 / USD 396,082,977 / EUR 48,453,609 / GBP 3,955,277 / other 7,718,133",
    "CIB June 2026 interim note 24 and FY2025 IFRS Consolidated FS note 26 'Due to "
    "customers', plus the foreign-exchange risk table (RNS 1119N, 3239S)",
    CO, "2026-07-21", is_fs_data=True, fiscal_period="Q2-2026",
    detail="FOOTED: all four cuts reconcile to the same printed total at both dates, and "
           "the currency table's rows and columns cross-foot.",
    model_impact="DRIVER UNLOCK for the funding-cost side of the NII build at the finest "
                 "sourced level: cost of funds is built per product and per currency, "
                 "with the 18.0% non-interest-bearing slice (Jun-2026) modelled "
                 "separately because it does not reprice at all when the CBE moves.")

f_curr = R.add(Ring.COMPANY, "regular disclosures", FindingClass.D,
    "THE BALANCE SHEET BY CURRENCY (Jun-2026): financial assets EGP 1,127,560,066k local "
    "/ USD 462,767,694 / EUR 64,125,132 / GBP 4,007,784 / other 7,035,925; financial "
    "liabilities EGP 893,973,456 / USD 433,245,410 / EUR 52,371,142 / GBP 3,959,969 / "
    "other 7,718,133. Net open position EGP 233,586,610 local, USD 29,522,284 equivalent. "
    "Gross loans to customers by currency: EGP 519,840,932 / USD 104,485,279 / EUR "
    "11,275,196",
    "CIB June 2026 interim condensed consolidated FS, foreign-exchange risk table "
    "(RNS 1119N)",
    CO, "2026-07-21", is_fs_data=True, fiscal_period="Q2-2026",
    detail="FOOTED: every currency row sums to its printed EGP-equivalent total, and the "
           "net position reconciles.",
    model_impact="Makes the two-currency NII build possible at balance-sheet level, and "
                 "sizes the translation exposure: ~28% of financial assets are non-EGP, "
                 "so a 10% EGP move is a ~EGP 53bn swing in reported assets before any "
                 "operating effect. The FX translation is modelled explicitly, never "
                 "folded into a growth rate.")

f_subdebt = R.add(Ring.COMPANY, "regular disclosures", FindingClass.D,
    "THE SUBORDINATED AND DEVELOPMENT-FINANCE DEBT SCHEDULE, facility by facility (note "
    "27): British International Investment sub-loan EGP 4,304,350k (10y, floating); EBRD "
    "5y EGP 928,817k; IFC 5y EGP 2,352,914k; EBRD subordinated 10y EGP 7,095,262k; IFC "
    "subordinated 10y EGP 14,181,868k; plus ECO, ARDF and EPAP programme lines. Total EGP "
    "30,471,499k at Dec-2025 (EGP 23,962,389k at Dec-2024), rising to EGP 34,616,250k at "
    "Jun-2026. Of this, EGP 25,581,480k counts as Tier 2 subordinated capital",
    "CIB FY2025 IFRS Consolidated FS notes 27 and 34.5.1 (RNS 3239S); June 2026 interim "
    "balance sheet",
    CO, "2026-02-09", is_fs_data=True, fiscal_period="FY2025",
    detail="FOOTED: the facility list sums to the printed total at both dates, and Tier 2 "
           "(25,581,480 + 9,073,673 stage-1 ECL = 34,655,153) matches its printed total.",
    model_impact="Interest is built from NAMED FACILITIES each at its own rate, which is "
                 "this book's standing convention [L-002/L-003], not from a ratio on "
                 "total liabilities. Also unlocks the Tier 2 leg of the capital forecast: "
                 "sub-debt amortises 20% a year in its last five years, so the Tier 2 "
                 "runway is scheduled rather than assumed.")

f_notabank = R.add(Ring.COMPANY, "regular disclosures", FindingClass.C,
    "STATED SO THE RING IS NOT READ AS THIN: no volume, no realised price, no cost per "
    "unit, no utilisation and no nameplate capacity was sought for this issuer, because "
    "none exists. The operating-company driver set does not apply to a bank and its "
    "absence here is a class decision under LENS_REGISTRY['bank'] = (ddm, "
    "(residual_income, relative_multiple, book_value)), taken before the sweep rather "
    "than discovered during it. The equivalent finest-sourced level for this class — "
    "interest income by earning-asset class, deposits by product and currency, ECL by "
    "stage, capital against the regulatory floor — was swept in full and is recorded at "
    "F22 through F26",
    "CIB FY2025 IFRS Consolidated Financial Statements (RNS 3239S), read end to end for "
    "any volume, unit-price, unit-cost, utilisation or capacity disclosure, of which it "
    "contains none; class ruling from research_protocol.LENS_REGISTRY, bank row",
    CO, "2026-02-09", model_impact="")

# ---- IR communications: MANDATORY, and tagged distinctly from the statements
f_rel25 = R.add(Ring.COMPANY, "IR communications (calls, presentations, releases)",
    FindingClass.D,
    "FY2025 earnings release, 9-Feb-2026 — the operating anchors no statement carries. "
    "NIM 8.95% total / 13.0% local currency / 2.50% foreign currency. CASA share of "
    "deposits up from 56% to 61%. Gross loans EGP 576bn (+44%, EGP 617bn with "
    "securitisation deals); LCY loans +56% or EGP 157bn, FCY loans +24% or USD 562mn. "
    "Deposits EGP 1.11tn (+14%); LCY +21%, FCY +USD 993mn. Gross loan-to-deposit 52% "
    "(56% with securitisation), local-currency LDR at an all-time-high 71%. Loan market "
    "share 5.26%, deposit share 6.81% (Sep-2025 CBE data). NPL 1.67% standalone, coverage "
    "358%, loan-loss provision balance EGP 34.5bn. CAR 27.3%, Tier 1 EGP 186bn = 84% of "
    "total tier capital, CET1 23% after the proposed appropriation. Segment balances: "
    "institutional loans EGP 468bn / deposits EGP 343bn; business banking EGP 16bn / EGP "
    "116bn; retail EGP 92bn / EGP 646bn. 204 branches, 10 units, 1,434 ATMs, 2.5m "
    "customers. CIB-Kenya turned pre-tax positive for the first time since acquisition",
    "CIB Full-Year 2025 News Release, 9 February 2026 (RNS 3242S)",
    IR, "2026-02-09", fiscal_period="FY2025",
    model_impact="DRIVER UNLOCK across the whole bank lens. This one document carries "
                 "the segment loan and deposit split, the CASA share, the NIM currency "
                 "split and the market shares — four drivers that appear in no financial "
                 "statement and could not be built without it. Its consolidated "
                 "highlights table foots (NII 107,700 + non-interest 9,733 = 117,433; "
                 "less 17,562 plus 11,711 = 111,582; less tax 29,895 plus deferred 572 = "
                 "82,259).")

f_rel1q = R.add(Ring.COMPANY, "IR communications (calls, presentations, releases)",
    FindingClass.D,
    "Q1-2026 earnings release, 11-May-2026. NIM 8.88% / LC 12.7% (-56bp YoY) / FC 2.18% "
    "(-64bp YoY). CASA 62% (from 56%). LCY deposits +5% or EGP 33bn from year-end; LCY "
    "loans incl. securitisation +7% or EGP 32bn, taking the LOCAL-CURRENCY LDR TO AN "
    "ALL-TIME-HIGH 72%; FCY deposits +2% or USD 172mn against FCY loans +8% or USD 228mn, "
    "FC LDR 34% from 32%. Institutional loans +8% or EGP 41bn in real terms, of which EGP "
    "27bn is CAPEX lending; SME share of lending 26%. CAR 26.9%, CET1 22.5% (EGP 201bn of "
    "EGP 240bn total tier capital). NPL 1.70%, coverage 344%, total gross loan coverage "
    "5.84%, unsecured coverage 8.26%. Liquidity 51.0% LC / 54.5% FC against CBE 20%/25%; "
    "LCR 341%/579%; NSFR 189%/176%. ROAE 31.9%, ROAA 4.74%, efficiency 16.5%",
    "CIB First-Quarter 2026 News Release, 11 May 2026 (RNS 9517D)",
    IR, "2026-05-11", fiscal_period="Q1-2026",
    model_impact="Q1 of the study year, from the IR channel, tied line-for-line to the "
                 "Q1 interim statements (NII 29,700 / PBT 25,563 / net profit 17,822 all "
                 "match). Its 72% local-currency LDR is the binding constraint on further "
                 "LC loan growth and therefore caps the LC NII driver.")

f_rel2q = R.add(Ring.COMPANY, "IR communications (calls, presentations, releases)",
    FindingClass.D,
    "Q2/H1-2026 earnings release, 21-Jul-2026 — THE NEWEST RELEASE, and its anchors "
    "supersede the FY25 and 1Q26 ones in the driver set. H1-2026 NIM 8.61% total / 12.3% "
    "local currency (-75bp YoY) / 2.17% foreign currency (-53bp YoY); Q2 alone 8.36%. "
    "CASA 63% of deposits; record quarterly local-currency deposit net sales of EGP "
    "141bn, 75% of it into current and savings accounts. Gross loans EGP 680bn (+18%), "
    "deposits EGP 1.30tn (+18%), loan-to-deposit 52.2%. CAR 28.4%, CET1 24.4%. NPL 1.49% "
    "(Q2 1.59%), coverage 358%. ROAE 33.5% (Q2 37.8%), ROAA 5.02%, cost-to-income 15.8%. "
    "EPS EGP 10.2. Local-currency liquidity 46.4% against a 20% CBE minimum; LCR 449% LC",
    "CIB 2Q26 Earnings Release, 21 July 2026 (RNS 1122N)",
    IR, "2026-07-21", fiscal_period="Q2-2026",
    detail="ROUTE RECORDED, per docstring note (4): RNS 1122N carries no PDF attachment "
           "and cibeg.com is Incapsula-blocked, so this release was read from the RNS "
           "announcement BODY via the LSE RNS distribution mirrors. Every figure in it "
           "that a primary document can settle was cross-checked and ties: net interest "
           "income EGP 60,826mn, net profit EGP 39,314mn and CAR 28.4% all match the "
           "interim condensed consolidated statements held as a primary PDF (F21). The "
           "release-only items are the NIM currency split, CASA, LDR, NPL, coverage, "
           "CET1, ROAE, ROAA and cost-to-income.",
    model_impact="SUPERSEDES the FY25 and 1Q26 operating anchors wherever they conflict: "
                 "CASA 63% (was 62%, then 61%), NIM 8.61% (was 8.88%, then 8.95%), CAR "
                 "28.4% (was 26.9%). Gross loans of EGP 680bn here are the "
                 "securitisation-inclusive measure against EGP 638bn on the balance "
                 "sheet — the study states which measure each driver uses.")

f_nocall = R.add_negative(Ring.COMPANY, "IR communications (calls, presentations, releases)",
    "'CIB Commercial International Bank Egypt earnings call transcript webcast 2026 "
    "investor day guidance five-year strategy targets' — CIB DOES hold quarterly calls "
    "(the Q4-2025 call was held 10-Feb-2026 with the CEO and the Head of Investor "
    "Relations named as participants) and does publish a slide deck alongside them, but "
    "NO TRANSCRIPT OR DECK IS OBTAINABLE from the company: cibeg.com is Incapsula-blocked, "
    "no transcript is filed to RNS, and the only copies sit behind third-party paywalls "
    "which are not an acceptable source for the company's own words",
    SWEEP_DATE)

# ---- base-resetting events
f_eclrel = R.add(Ring.COMPANY, "one-off base-resetting transactions", FindingClass.B,
    "THE FY2025 ECL-MODEL RECALIBRATION IS A BASE CHANGER AND MUST BE DUAL-FRAMED. Net "
    "impairment in FY2025 was a RELEASE of EGP 11,804,786k against a CHARGE of EGP "
    "5,401,308k in FY2024 — a EGP 17.2bn swing on a EGP 104.8bn pre-tax profit. Inside "
    "it, a 'PD Recalibration impact' of EGP 8,173,704k on the corporate ECL roll-forward, "
    "footnoted in the company's own statements as 'released ECL to the income statement "
    "and has been transferred to a special reserve'; EGP 13,145,012k was duly transferred "
    "out of net profit to a special reserve in the equity statement. CIB'S OWN NORMALISED "
    "NUMBER: FY2025 net income would be EGP 70.6bn rather than the reported EGP 82.2bn, "
    "and ROAE 41.5% rather than 48.3%",
    "CIB FY2025 IFRS Consolidated FS notes 9 and 31.8 (RNS 3239S); CIB Full-Year 2025 "
    "News Release management commentary (RNS 3242S)",
    CO, "2026-02-09", is_fs_data=True, fiscal_period="FY2025",
    detail="FOOTED: note 9's four components sum to the printed EGP 11,804,786k; the "
           "retained-earnings roll (51,590,097 - 21,744,828 + 2,628 + 111,370 - 8,993,602 "
           "+ 75,460,219 - 26,186 - 13,145,012) closes exactly on the printed "
           "83,254,686.",
    model_impact="BASE CHANGER, modelled as an explicit dated event and never smoothed "
                 "into a cost-of-risk glide. The forecast base for earnings and for the "
                 "residual-income lens is the NORMALISED EGP 70.6bn, with the reported "
                 "EGP 82.2bn shown beside it. It also constrains the DDM directly: the "
                 "CBE excludes the release from both the capital base and distributable "
                 "profit (F8), so it never reaches a dividend.")

f_fx24 = R.add(Ring.COMPANY, "one-off base-resetting transactions", FindingClass.B,
    "FY2024 IS NOT A CLEAN BASE EITHER, for the opposite reason. The March-2024 "
    "devaluation put EGP 20,470,230k of net trading income into FY2024 (of which EGP "
    "20,577,493k was profit on foreign-exchange transactions) against EGP 1,523,649k in "
    "FY2025 — a 93% collapse — while simultaneously putting EGP 15,457,960k of foreign-"
    "exchange LOSSES on non-trading assets and liabilities into other operating expenses. "
    "Both reverse. Reported growth between FY2024 and FY2025 is therefore an artefact of "
    "two offsetting one-offs, not of the operating business",
    "CIB FY2025 IFRS Consolidated FS notes 6 and 8, with FY2024 comparatives (RNS 3239S)",
    CO, "2026-02-09", is_fs_data=True, fiscal_period="FY2024",
    model_impact="BASE CHANGER. FY2024 is excluded as a normalisation base and the "
                 "FX-driven lines are stripped before any trend is fitted. Non-interest "
                 "income is forecast off the FEE AND COMMISSION line (which grew 30% in "
                 "FY2025 and 40% in H1-2026 on real activity), with trading income "
                 "modelled as a separate, explicitly volatile leg.")

# ---- ownership / stake changes: the SPECIFIC NAMED TRANSACTION, never 'estimated'
f_own = R.add(Ring.COMPANY, "ownership / stake changes (named-transaction rule)",
    FindingClass.S,
    "NAMED TRANSACTION: on 8 October 2025 Alpha Oryx Limited — the ADQ (Abu Dhabi) "
    "vehicle that bought into CIB in April 2022 — SOLD 73.50 MILLION CIB SHARES at an "
    "average of EGP 96.50, a consideration of EGP 7.09bn, through EFG Hermes "
    "International Securities Brokerage, cutting its holding from 18.06% to 15.67%. "
    "Disclosed to the EGX as a major-shareholding change. Alpha Oryx remains the largest "
    "shareholder and holds TWO BOARD SEATS: Mr Fadhel Abdul Baqy Abulhasan Algaed AlAli "
    "and Mr Aziz Moolji were both elected 'representing Alpha Oryx Ltd.' at the "
    "15-Mar-2026 Ordinary General Assembly. Fairfax Financial Holdings holds ~6.4%. A "
    "further 18.45 million shares (EGP 2.46bn) crossed through the EGX block-trade "
    "mechanism on ~18-Aug-2026 with neither counterparty disclosed",
    "EGX major-shareholding disclosure of 8-Oct-2025 as reported; CIB's own Ordinary "
    "General Assembly Resolutions Summary, 15 March 2026 (RNS 6754W), board-election item",
    PRESS, "2025-10-13",
    detail="The board-seat half of this finding is from CIB's OWN document, read by OCR "
           "off the rendered pixels of the OGA resolutions PDF (no text layer). The "
           "transaction half is the counterparty's EGX filing as reported; CIB does not "
           "publish its shareholder register and the EGX disclosure index would not open "
           "(see primary-access log). THE EGP 96.50 PRICE IS PRE-BONUS — the 1-for-10 "
           "bonus issue of 17-Dec-2025 puts it at ~EGP 87.7 on today's share count, and "
           "the study must not compare it to a post-bonus price unadjusted.",
    model_impact="Fixes the free float and the overhang. A 15.67% holder that has already "
                 "sold once is a supply risk to the share price, NOT an input to fair "
                 "value — it is reported as an overhang and never as a valuation anchor. "
                 "It also settles governance: two of eleven board seats are the "
                 "shareholder's, which is disclosed rather than inferred.")

# ---- management & capital actions
f_shares = R.add(Ring.COMPANY, "management & capital actions", FindingClass.D,
    "THE SHARE COUNT, which the DDM divides by, moved twice and restated the EPS history "
    "with it. (i) 1-FOR-10 BONUS ISSUE effective 17-Dec-2025, financed from the General "
    "Reserve: issued capital +EGP 3,070,851k to EGP 33,779,361k, shares 3,043,158k -> "
    "3,377,936k. (ii) ESOP 17th tranche approved at the 15-Mar-2026 OGA: +27,203,000 "
    "shares at EGP 10 par, +EGP 272,030,000, taking issued capital to EGP 34,051,391,000 "
    "— which is exactly the figure printed on the 30-Jun-2026 balance sheet. Weighted "
    "average shares for H1-2026 EPS: 3,392,693k basic, 3,434,416k including ESOP "
    "shares. ESOP rights outstanding 78,658k shares across 2026/2027/2028 tranches at an "
    "EGP 10 exercise price. THE RESTATEMENT CHAIN: FY2023 basic EPS printed 8.84, "
    "restated to 8.75 in the FY2024 filing; FY2024 printed 16.34, restated to 14.67 in "
    "the FY2025 filing",
    "CIB FY2025 IFRS Consolidated FS notes 30 and 33 (RNS 3239S); CIB Board of Directors "
    "resolutions summary, 9 February 2026 (RNS 3251S); CIB Ordinary General Assembly "
    "Resolutions Summary, 15 March 2026 (RNS 6754W), items 7 and 5",
    CO, "2026-03-15", is_fs_data=True, fiscal_period="FY2025",
    detail="The two resolution documents carry NO TEXT LAYER and were read by OCR off "
           "the rendered pixels at 110 dpi; the capital figures they give (EGP "
           "33,779,361,000 -> EGP 34,051,391,000 via 27,203,000 shares at EGP 10) "
           "reconcile exactly to the arithmetic and to the printed Jun-2026 balance "
           "sheet, which is the check that validates the OCR route.",
    model_impact="DRIVER UNLOCK: fixes the denominator. A DDM built on an unrestated EPS "
                 "series would carry a 10% break at Dec-2025 that is pure share count. "
                 "The ESOP is dilutive at EGP 10 against a EGP 139 market price and is "
                 "modelled as a scheduled annual issuance, not ignored.")

f_div = R.add(Ring.COMPANY, "management & capital actions", FindingClass.D,
    "THE DIVIDEND, which is the primary lens's entire numerator. FY2025: the Ordinary "
    "General Assembly of 15-Mar-2026 'approved cash dividends payout of EGP 6 per share "
    "to be paid on Thursday, April 9, 2026'. The company frames it as a payout of 25% OF "
    "REPORTED FY2025 NET PROFIT and 30% OF THE DISTRIBUTABLE PORTION. Dividends actually "
    "paid, from the equity statements: FY2022 EGP 3,019,442k, FY2023 EGP 2,016,159k, "
    "FY2024 EGP 2,379,819k, FY2025 EGP 8,993,602k, and H1-2026 EGP 29,037,813k to parent "
    "shareholders (EGP 29,052,828k with NCI) — the last figure being the whole FY2025 "
    "appropriation, cash dividend plus staff profit share plus board bonus, not the cash "
    "dividend alone. No standing payout POLICY is published; the payout is set annually "
    "by the OGA",
    "CIB Ordinary General Assembly Resolutions Summary, 15 March 2026 (RNS 6754W), item 5; "
    "CIB FY2025 News Release (RNS 3242S); equity statements in the FY2022-FY2025 IFRS "
    "filings and the June 2026 interim",
    CO, "2026-03-15", is_fs_data=True, fiscal_period="FY2025",
    detail="The EGP 6.00 per share came by OCR off the rendered pixels of the OGA "
           "resolutions PDF, which carries no text layer. IT IS ARITHMETICALLY "
           "CORROBORATED by the company's own release: 25% of EGP 82.2bn is EGP 20.6bn, "
           "which over 3,377,936k shares is EGP 6.09 — the OCR figure and the "
           "release-derived figure agree to within rounding, which is the check.",
    model_impact="THE PRIMARY LENS'S OWN INPUT. The payout path is built from the "
                 "company's own 25%/30% framing applied to DISTRIBUTABLE profit (F8's "
                 "CBE constraint), tested against the CAR headroom over the 12.75% floor "
                 "(F7). The four-year paid history establishes that payout is a policy "
                 "choice that has just stepped up sharply — 2.4x in FY2025 — which is "
                 "the central uncertainty in the lens and is sensitised, not extrapolated.")

# ---- strategic plans & guidance
f_yomo = R.add(Ring.COMPANY, "strategic plans & guidance", FindingClass.B,
    "yomo: on 19-Aug-2026 CIB announced it had received PRELIMINARY approval from the "
    "Central Bank of Egypt to establish yomo, an independently licensed, digitally-native "
    "bank under Egypt's 2023 digital-bank framework, and that IT IS COMMITTING USD 300 "
    "MILLION to yomo Holding. Launch is targeted for 4Q-2026 and remains contingent on "
    "further regulatory authorisation after technology validation, cybersecurity testing "
    "and operational-resilience work. CIB had already flagged in its FY2025 release that "
    "it 'has already applied for the Digital Bank License'",
    "CIB press release dated 19 August 2026 (RNS 4774R, announced 20-Aug-2026); CIB "
    "Full-Year 2025 News Release (RNS 3242S)",
    IR, "2026-08-19",
    detail="RNS 4774R carries no PDF attachment and the company's own newsroom page "
           "(cibeg.com/en/newsroom/news/8-20-2026-yomo-announcement) is Incapsula-blocked "
           "— see the primary-access log. The announcement body was read via the LSE RNS "
           "distribution mirror and is corroborated by CIB's own PR Newswire wire release "
           "of the same date.",
    model_impact="BASE CHANGER, and the newest one in the file — it post-dates the "
                 "H1-2026 statements, so it appears in NO number the study will otherwise "
                 "use. A USD 300mn equity commitment against EGP 238bn of group equity is "
                 "~6.4% of book at the Jun-2026 rate, deployed into a start-up that will "
                 "lose money before it earns any. Modelled as an explicit dated capital "
                 "outflow plus a loss-making segment, dual-framed with and without, and "
                 "NOT smoothed into the payout ratio.")

f_noguid = R.add_negative(Ring.COMPANY, "strategic plans & guidance",
    "'CIB Egypt dividend policy payout ratio target investor presentation guidance ROE "
    "medium term 2026' and 'CIB Egypt trading income foreign exchange revaluation gains "
    "2026 outlook guidance non-interest income forecast disclosure' — CIB PUBLISHES NO "
    "QUANTIFIED FORWARD GUIDANCE. Management commentary is directional only ('balance "
    "sheet resilience and operating model efficiency as its top priority', 'profitability "
    "likely tamed within normal, rather than previous-exceptional rates'). There is no "
    "NIM target, no ROE target, no loan-growth target, no standing payout policy, no "
    "cost-to-income target beyond a qualitative 'desirable level of 30%', and no forecast "
    "of trading or non-interest income. A five-year strategy is referenced but its "
    "targets are not published",
    SWEEP_DATE)

f_noavg = R.add_negative(Ring.COMPANY, "regular disclosures",
    "'CIB Egypt average interest earning assets disclosure average balance sheet yield on "
    "assets cost of funds quarterly disclosure' — CIB PUBLISHES NO AVERAGE-BALANCE-SHEET "
    "TABLE. It discloses interest income by asset class and interest expense by liability "
    "class (note 3), and period-end balances, but not the average balances those flows "
    "were earned on, and not a yield or cost-of-funds figure per class. The NIM it quotes "
    "is 'based on standalone managerial accounts' by its own footnote and cannot be "
    "reconstructed from the statements",
    SWEEP_DATE)

# ---- market data & listing structure (free-form category: the dual-listing trap)
f_mkt = R.add(Ring.COMPANY, "market data & listing structure", FindingClass.C,
    "DUAL LISTING FLAGGED EXPLICITLY. The ordinary share trades on the EGX as COMI in "
    "EGP; the SAME ISSUER also has a GDR in London under CBKD (Reg S) and OTC lines "
    "CIBEY/CMGGF in USD. Two legitimate regressors exist and only the series tells them "
    "apart. The repo series engine/raw_ohlc/EG/COMI.csv is the EGX line in EGP — 3,772 "
    "rows from 03-Jan-2011, closing EGP 139.00 on 01-Sep-2026 against EGP 103.00 on "
    "31-Dec-2025 (+35% year to date), which is the right currency and the right order of "
    "magnitude for the EGX line and could not be confused with a USD GDR quote. The "
    "regressor for beta is therefore engine/raw_indices/EG/EGX30.csv (56,174.30 on "
    "08-Sep-2026), the published index of the exchange the stock is listed on",
    "engine/raw_ohlc/EG/COMI.csv and engine/raw_indices/EG/EGX30.csv, read on the sweep "
    "date; LSE RNS issuer identity 'Commercial International Bank (Egypt) SAE GDR (Reg S) "
    "- CBKD'",
    PMD, "2026-09-01", model_impact="",
    detail="NOTE FOR THE BUILD: the COMI series is 5 trading days behind the index "
           "(01-Sep vs 08-Sep) and must be refreshed before the beta is struck. Beta is "
           "produced ONLY by engine/beta_regression.own_stock_beta('COMI', 'EG', 'EGX'); "
           "no study-local regression.")

# ---- the reporting-basis finding: which set the historicals sit on
f_basis = R.add(Ring.COMPANY, "official financial statements", FindingClass.S,
    "CIB REPORTS ON TWO BASES AND THEY DO NOT AGREE — the single most important thing to "
    "settle before a driver is set. (a) The ANNUAL set retrieved here is IFRS "
    "consolidated. (b) The QUARTERLY interims state their own basis explicitly: "
    "'prepared in accordance with the Central Bank of Egypt approved by the Board of "
    "Directors on December 16, 2008... condensed financial statements complying with the "
    "Central Bank of Egypt instructions issued on May 3, 2020', with unmentioned "
    "instructions referred to Egyptian Accounting Standards. The earnings releases sit "
    "on the CBE basis too. THE GAP IS MEASURABLE at 31-Dec-2025: total assets EGP "
    "1,445,486,499k on the IFRS set against EGP 1,442,494,120k in the interim's "
    "comparative column (-2,992,379); total liabilities 1,221,060,441 against 1,210,979,902 "
    "(-10,080,539); total equity 224,426,058 against 231,514,218 (+7,088,160). On the "
    "income statement the gap is larger: FY2025 net profit EGP 75,480,182k on IFRS "
    "against EGP 82,259mn in the release, and FY2024 EGP 49,619,082k against EGP 55,257mn",
    "CIB June 2026 interim condensed consolidated FS, note 2.1 'Basis of preparation' "
    "(RNS 1119N); FY2025 IFRS Consolidated FS (RNS 3239S); FY2025 News Release (RNS 3242S)",
    CO, "2026-07-21", is_fs_data=True, fiscal_period="Q2-2026",
    detail="[R-SIGCM-03] EXCEPTION NAMED HERE. The AUDITED CBE-BASIS ANNUAL STATEMENTS — "
           "the separate and consolidated statements the OGA ratified on 15-Mar-2026 — "
           "COULD NOT BE REACHED: they are published on cibeg.com, which is "
           "Incapsula-blocked, and they are not among the documents CIB files to RNS. "
           "Every CBE-basis ANNUAL figure in this register therefore comes from the "
           "company's OWN other documents — the FY2025 earnings release (F28) and the "
           "comparative column of the company's own Q1 and Q2 interim statements (F20, "
           "F21) — which is the named fallback, not a substitute from outside the "
           "company. Both fallback documents foot against their own printed subtotals.",
    model_impact="FORCES A CHOICE THE STUDY MUST STATE. The historical series is built on "
                 "the CBE basis, because that is the basis the interims, the releases, "
                 "the regulatory capital ratios and the distributable-profit calculation "
                 "all sit on — and therefore the basis the dividend is actually paid out "
                 "of. The IFRS set is carried beside it as the reconciliation, never "
                 "spliced into it. Mixing the two would put a EGP 6.8bn step into the "
                 "FY2025 earnings base that is pure accounting basis.")

# ======================================================= DRIVER GATE TABLE
R.add_driver("Net interest income — by earning-asset class x yield, less deposit class "
             "x cost", DriverMode.BOTTOM_UP,
    "THE FINEST SOURCED LEVEL FOR A BANK, and it is disclosed. Note 3 splits interest "
    "income four ways (banks, clients, treasury bills and government notes, debt "
    "instruments) and interest expense six ways; note 26/24 splits deposits by product, "
    "by customer, by rate type and by currency; the FX table splits every asset and "
    "liability class by currency. Yields are solved as flow over period-average balance. "
    "GAP FLAGGED AND DROPPED A LEVEL: CIB publishes no average-balance table (F39), so "
    "averages are opening/closing means rather than daily averages, and the study says so.",
    [f_nii, f_deps, f_curr, f_fs25, f_noavg])

R.add_driver("Net interest margin — total, local currency, foreign currency",
             DriverMode.BOTTOM_UP,
    "MARGINS ARE OUTPUTS, NEVER INPUTS [L-005]. NIM is not typed in; it falls out of the "
    "NII build above and is CHECKED against the company's own disclosed series (8.95% "
    "FY2025, 8.88% Q1-2026, 8.61% H1-2026, with the LC and FC legs each disclosed "
    "separately). A build whose implied NIM misses the disclosed figure is wrong and gets "
    "fixed, rather than being overridden by pasting the disclosed number in.",
    [f_nii, f_price, f_rel2q, f_deps])

R.add_driver("Loan book — by segment (institutional / business banking / retail) and by "
             "currency", DriverMode.BOTTOM_UP,
    "Segment loan balances are disclosed in the releases (institutional EGP 468bn, "
    "business banking EGP 16bn, retail EGP 92bn at Dec-2025) and the statements give the "
    "corporate/individual and currency splits at every date. Growth is projected in BOTH "
    "the balance and its price — the balance per segment, the yield per currency leg — "
    "never as one blended loan-growth rate. The 72% local-currency loan-to-deposit ratio "
    "is the binding cap.",
    [f_stages, f_curr, f_rel25, f_rel1q, f_rel2q])

R.add_driver("Deposit book — by product and currency, and the CASA share",
             DriverMode.BOTTOM_UP,
    "Note 24/26 gives the four-way product cut and the rate-type cut (18.0% "
    "non-interest-bearing at Jun-2026) and the FX table gives the currency cut; the "
    "releases give the CASA share on the company's own definition (56% -> 61% -> 62% -> "
    "63%). Cost of funds is built per product per currency, with the non-interest-bearing "
    "slice modelled separately because it does not reprice with the CBE at all.",
    [f_deps, f_curr, f_rel25, f_rel1q, f_rel2q])

R.add_driver("Cost of risk — ECL by stage, on stage migration", DriverMode.BOTTOM_UP,
    "Stage 1/2/3 balances and ECL are disclosed by segment at Dec-2024, Dec-2025 and "
    "Jun-2026, with the roll-forward showing write-offs, recoveries, the PD-recalibration "
    "release and FX translation separately. The charge is built from stage migration and "
    "stage coverage rates, not from a flat basis-point assumption, and the FY2025 release "
    "is carried as an explicit dated event rather than smoothed into the path.",
    [f_stages, f_eclrel, f_fs25])

R.add_driver("Regulatory capital — CAR, CET1 and the CBE floor", DriverMode.BOTTOM_UP,
    "Note 34.5 gives the full capital stack (Tier 1 EGP 186,435,898k, Tier 2 EGP "
    "34,655,153k, RWA EGP 811,066,999k split into credit, market, operational and "
    "Top-50-overlimit) and the CBE's own 12.75% minimum inclusive of the conservation "
    "buffer and D-SIB surcharge. The Tier 2 leg is scheduled off the named subordinated "
    "facilities and their 20%-a-year amortisation, not assumed.",
    [f_reg, f_subdebt, f_fs25, f_rel2q])

R.add_driver("Dividend per share and the payout path (DDM numerator)", DriverMode.BOTTOM_UP,
    "Built from the company's own approved appropriation — EGP 6.00 per share for FY2025, "
    "framed by CIB as 25% of reported profit and 30% of the DISTRIBUTABLE portion — "
    "applied to distributable rather than reported earnings because the CBE excludes the "
    "ECL release from both the capital base and distributable profit, and tested against "
    "the CAR headroom over the 12.75% floor. Four years of paid dividends give the "
    "history. No standing policy exists (F38), so the ratio is sensitised rather than "
    "extrapolated.",
    [f_div, f_ecl_reg, f_reg, f_eclrel])

R.add_driver("Residual income — book value, ROE and the equity charge",
             DriverMode.BOTTOM_UP,
    "The cross-check lens beside the DDM. Opening book value comes from the equity "
    "statements across four filed years; ROE is the output of the earnings build on the "
    "NORMALISED base (EGP 70.6bn FY2025, CIB's own figure), never the reported one; the "
    "equity charge is Ke. Book value is separately published as a disclosed floor and is "
    "never weighted into the central.",
    [f_fs22, f_fs23, f_fs24, f_fs25, f_eclrel])

R.add_driver("Fee and commission income — by line", DriverMode.BOTTOM_UP,
    "Note 4 splits fee income four ways (credit-related EGP 5,356,905k, custody 680,063, "
    "card 6,287,070, other 3,711,971) and fee expense two ways, so the line is built per "
    "component rather than as a percentage of assets. The releases add the trade-service "
    "fee balance (EGP 358bn outstanding at Q1-2026) behind the credit-related fees.",
    [f_fs25, f_rel25, f_rel1q])

R.add_driver("Administrative expenses", DriverMode.BOTTOM_UP,
    "Note 7 decomposes the whole line — wages EGP 7,134,524k, other benefits 7,595,930, "
    "stock option 1,262,609, social insurance, depreciation 2,264,888, maintenance, "
    "premises, internship, board and other admin — so each component carries its own "
    "escalator rather than one blended inflation rate across all of them [L-009]. The "
    "technology-driven step-up management named in Q1-2026 (+33% YoY) is modelled on the "
    "technology components, not spread across the line.",
    [f_fs25, f_rel1q])

R.add_driver("Effective tax rate", DriverMode.BOTTOM_UP,
    "Built from note 10.1's own reconciliation — statutory 22.5% plus non-deductible "
    "expenses, less exemptions, plus withholding tax — so the rate MOVES with the "
    "sovereign-paper share of the earning-asset mix (27.98% FY2025, 30.60% FY2024) "
    "instead of sitting at the statutory rate.",
    [f_tax, f_fs25, f_nii])

R.add_driver("Cost of equity (Ke): risk-free, beta, equity risk premium",
             DriverMode.BOTTOM_UP,
    "Risk-free from the CBE's own published corridor read on the sweep date, with the "
    "sovereign default spread netted out so country risk is not charged twice [L-004]. "
    "Beta from engine/beta_regression.own_stock_beta('COMI','EG','EGX') against the "
    "published EGX30, never a constituent composite and never a study-local script. The "
    "dual listing is flagged so the EGP EGX line is regressed, not the USD GDR.",
    [f_cbe, f_sov, f_mkt])

R.add_driver("yomo — digital-bank build cost, loss path and capital drag",
             DriverMode.TOP_DOWN,
    "TOP-DOWN BY EVIDENCED ABSENCE, NOT BY CONVENIENCE. CIB has disclosed the commitment "
    "(USD 300mn) and the timing (preliminary approval 19-Aug-2026, launch targeted "
    "4Q-2026) and NOTHING ELSE: the negative search at F38 establishes that no customer "
    "target, no deposit target, no cost path and no break-even year is published for "
    "yomo by CIB. The drag is therefore sized top-down from the disclosed capital "
    "commitment and benchmarked against onebank's published year-one targets, and "
    "dual-framed with and without.",
    [f_noguid, f_yomo, f_entrants])

R.add_driver("Trading income and other non-interest income", DriverMode.TOP_DOWN,
    "TOP-DOWN BY EVIDENCED ABSENCE. The negative search at F38 confirms CIB publishes no "
    "forecast or driver disclosure for trading income, and the line is dominated by FX "
    "revaluation that swung from EGP 20,470,230k (FY2024) to EGP 1,523,649k (FY2025). It "
    "is modelled as a normalised run-rate on the non-FX components with the FX component "
    "set to zero in the base and sensitised in both directions — never trended.",
    [f_noguid, f_fx24, f_fs25])

R.add_driver("Reporting basis for the historical series", DriverMode.BOTTOM_UP,
    "Not a forecast driver but a construction decision that gates every other row, so it "
    "gets a gate row of its own. The series is built on the CBE basis — the basis the "
    "interims, the releases, the regulatory ratios and the distributable-profit "
    "calculation all sit on, and therefore the basis the dividend is paid out of — with "
    "the IFRS set carried beside it as the reconciliation. The EGP 6.8bn FY2025 "
    "difference is disclosed, not spliced away.",
    [f_basis, f_fs25, f_q1, f_q2])

# ================================================================= OUTPUT
errors, warnings = R.validate()
R.to_json(os.path.join(HERE, 'sweep_register.json'))
print(R.qc_line())
print(f"\nfindings: {len(R.findings)} | drivers: {len(R.drivers)}")
by_ring = {}
for f in R.findings:
    by_ring[f.ring.value] = by_ring.get(f.ring.value, 0) + 1
print("by ring:", by_ring)
n_ir = sum(1 for f in R.findings if f.source_type is SourceType.COMPANY_IR)
n_co = sum(1 for f in R.findings if f.source_type is SourceType.COMPANY_OFFICIAL)
print(f"COMPANY_OFFICIAL: {n_co} | COMPANY_IR: {n_ir} | "
      f"primary-access attempts: {len(R.primary_access)} "
      f"({sum(1 for p in R.primary_access if p.reachable)} reachable / "
      f"{sum(1 for p in R.primary_access if not p.reachable)} blocked)")
fs_years = sorted({f.fiscal_period for f in R.findings
                   if f.is_fs_data and f.fiscal_period.startswith("FY")})
fs_qtrs = sorted({f.fiscal_period for f in R.findings
                  if f.fiscal_period.startswith("Q")})
print(f"fiscal years with FS data: {fs_years} | quarters swept: {fs_qtrs}")

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
fr = R.check_freshness(SWEEP_DATE)
print(f"\nfreshness (delivery {SWEEP_DATE}): {fr or 'OK — sweep and intended delivery same day'}")
