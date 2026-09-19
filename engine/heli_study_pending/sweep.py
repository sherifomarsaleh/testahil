"""HELI — Heliopolis Company for Housing and Development S.A.E. (EGX: HELI, Egypt)
Step 2A four-ring Information Sweep.

Runs BEFORE any forecast driver is set. Every mandatory category of every ring is closed
by a dated finding or a dated negative search. This module imports engine/research_sweep.py
and hand-rolls nothing. It builds no valuation, no driver model and no document.

WRITE LOCATION. This module and its JSON live in `engine/heli_study_pending/`, which sits
deliberately OUTSIDE the `engine/*_study` glob every repository gate walks, so a half-built
study directory cannot turn those gates red. There is no `engine/heli_study/` and none
should be created until a study is actually built.

-------------------------------------------------------------------------------
THE HEADLINE, STATED FIRST BECAUSE A LATER BUILD MUST NOT MISS IT
-------------------------------------------------------------------------------
NO AUDITED OR REVIEWED FINANCIAL STATEMENT OF THIS COMPANY COULD BE OBTAINED — not one
period, not one page. FY2022, FY2023, FY2024, FY2025 audited and the Q1-2026 and H1-2026
reviewed interims all exist and are all filed; every route to them from this environment
is blocked, and each block is logged below with its real failure text. Consequently:

  * ZERO findings in this register carry `is_fs_data=True`. The FS-DEPTH invariant fires
    with 0 fiscal years. That error is LEFT TO FIRE and reported verbatim. It is not
    closed by relabelling press-relayed figures as company data — the exact failure the
    SCEM register recorded and that later proved to have been wrong by 12-28 per cent on
    the balance-sheet triple.
  * The study year 2026 is declared with both disclosed quarters (Q1-2026 filed ~May-2026,
    H1-2026 announced 09-Aug-2026). Neither is tagged to a finding, because neither
    filing could be read. QUARTER COVERAGE fires. That error is also LEFT TO FIRE: tagging
    a negative search with the quarter would silence the invariant while the actuals stay
    unswept, which is the failure the invariant exists to catch.

A STUDY CANNOT BE BUILT ON THIS REGISTER AS IT STANDS. What is needed is named at the
bottom of this docstring under "WHAT TO ATTACH".

-------------------------------------------------------------------------------
PRIMARY-SOURCE ACCESS — every attempt logged, success or failure, with the real text
-------------------------------------------------------------------------------
THE COMPANY'S OWN SITE IS misr-algadida.com, NOT the domain every aggregator prints.
  * http://misr-algadida.com/  -> HTTP 200. This is the live corporate site of Misr Al
    Gadida (Heliopolis Company for Housing and Development). Reached over PLAIN HTTP.
  * https://misr-algadida.com/ -> "curl: (60) SSL certificate problem: certificate has
    expired". The company's own TLS certificate is expired, so its own site is only
    readable over http. Recorded rather than smoothed over: a later run that tries https
    first and stops will conclude the company has no website.
  * https://www.heliopoliscompany.com/ -> HTTP 200, 114 bytes, a JavaScript redirect to
    /lander which 302s to forsale.godaddy.com. The domain that Investing.com, Simply
    Wall St and several brokers still publish as this issuer's website is EXPIRED AND
    PARKED FOR SALE. It is not the company. Logged because "the aggregator's link
    resolved" is not the same fact as "the company was reached".
  * Dead-end candidates, all "gateway answered 502 to CONNECT (policy denial or upstream
    failure)" at this environment's proxy: www.misrelgedida.com, www.heliopolishousing.com,
    www.heliopolis-housing.com, www.heliopoliscompany.com.eg, heliopolisco.com,
    www.hhd.com.eg, www.heliopolis.com.eg, www.misralgadida.com.eg, www.hccd.com.eg
    (the state parent), mpbs.gov.eg (the ministry), www.mcdr.com.eg.

THE COMPANY'S IR DOCUMENT LIBRARY IS AN EMBEDDED EGID WIDGET, AND ITS DATA PORT IS SHUT.
  * http://misr-algadida.com/investor-relations -> HTTP 200. The page carries twelve tabs
    (Stock Overview, Financial Statements, Disclosures, Announcements, News, Corporate
    Actions, Insider Transactions, Governance, Board of Directors, Company Profile, IR
    Contacts, Calculator) and every one of them is an iframe onto
    https://ir.egidegypt.com/{en|ar}/{tab}/l2CcUsLEX0X_jNgUyU870fBLV0SPpysHh_i22D-IFog!
  * https://ir.egidegypt.com/en/financialstatement/<appKey> -> HTTP 200, but 22,613 bytes
    of Angular shell with no data in it.
  * https://ir.egidegypt.com/assets/config.json -> HTTP 200 and it names the reason:
    {"frontUrl":"https://ir.egidegypt.com","baseUrl":"https://ir.egidegypt.com:8080", ...}
    The document API is on PORT 8080.
  * https://ir.egidegypt.com:8080/api/identity/Settings/getCompanySettings/<appKey>
      -> "curl: (35) Recv failure: Connection reset by peer"   (https, four attempts)
      -> "curl: (28) Connection timed out after 30002 milliseconds"  (http)
      -> proxy log: kind "ws_closed_mid_exchange", detail "tunnel closed (code 1006,
         Connection ended) after 6s; 517 B sent, 39 B received, client reading".
    So the company's own filing library is one hop away and unreadable.
  * https://data.egidegypt.com/ -> HTTP 403; /api/Feed/GetCompanyProfile?SYMBOL_CODE=HELI
    -> HTTP 404. The attachment host answers, but attachment paths are only issued by the
    port-8080 API, so nothing can be fetched from it without that API.

THE EXCHANGE PORTAL ANSWERS WITH A CAPTCHA, NOT WITH FILINGS.
  * https://www.egx.com.eg/... with a default curl user agent -> "curl: (52) Empty reply
    from server". THIS IS NOT THE WHOLE STORY, and earlier registers in this repository
    stopped there. With a browser user agent the same URLs return HTTP 200 — carrying an
    F5/TSPD bot-defence interstitial whose visible text is:
      "Please enable JavaScript to view the page content. Your support ID is:
       6431284897889349852 ... This question is for testing whether you are a human
       visitor and to prevent automated spam submission ... What code is in the image?"
    A 200 that is an image CAPTCHA, on /en/DisclosureAll.aspx, /en/homepage.aspx and on
    static files: https://www.egx.com.eg/downloads/Bulletins/302003_2.pdf returns
    content_type text/html, 6,139 bytes, the same challenge. No CAPTCHA was solved and
    none should be.
  * https://web.archive.org/save/https://www.egx.com.eg/en/DisclosureAll.aspx -> HTTP 520,
    body "Sorry Job failed". The Internet Archive cannot fetch it either.
  * Wayback CDX (which IS reachable) holds HELI documents on egx.com.eg only from
    2011-2013, and zero egx.com.eg PDFs archived since 2024-01-01.
  * https://www.mubasher.info/markets/EGX/stocks/HELI/financial-statements -> HTTP 403,
    Cloudflare "Attention Required!". Logged for completeness only: an aggregator is not
    a permitted source for this company's own reported numbers in any case.

[R-SIGCM-03] NAMED FALLBACK, AND ITS LIMIT. Because the statements themselves cannot be
reached, the company's OWN other documents are used where they carry the figure: the
corporate site's project, partnership, history and governance pages; its media-centre
releases (including its own 9M-2025 results release); its Ordinary General Assembly
invitation for the 2 May 2026 meeting; and its seven downloadable governance policies.
Those are tagged COMPANY_OFFICIAL / COMPANY_IR and are the only company-sourced figures
here. NOTHING ELSE IS PROMOTED. Where only a data vendor, a broker or the press carries a
number the company reported about itself, the finding says so in its own text and the
number is quarantined — it is context for a later build to VERIFY, never an input.

-------------------------------------------------------------------------------
SCANNED AND IMAGE-ONLY DOCUMENTS
-------------------------------------------------------------------------------
Egyptian primary statements are routinely image-only, and the two company PDFs that are
image-only here confirm the house tooling is ready for them: the CSR Policy (4 pages) and
the Code of Conduct and Ethics (2 pages) return 0 extractable characters on every page
(PyMuPDF 1.28.2). Neither carries a financial figure, so no OCR read was needed and none
was performed. tesseract is present at /usr/bin/tesseract and pdftoppm at /usr/bin/pdftoppm,
so the render-and-re-add route is available the moment a statement arrives. NO FOOTING
CHECK APPEARS IN THIS REGISTER BECAUSE NO STATEMENT WAS OBTAINED TO FOOT. The arithmetic
that WAS done is on the relayed figures, and it caught two defects — see F45 and F46.
One further defect is in the company's own page: its OGM item is headlined "May 2, 2025"
and its body convenes the meeting for "Saturday, May 2, 2026" over the accounts for the
year ended 31 December 2025. The body and the agenda agree; the headline is wrong.

-------------------------------------------------------------------------------
THE LAND BANK IS THE ASSET BASE, AND THE VINTAGE IS THE WHOLE QUESTION [R-ASSET-01]
-------------------------------------------------------------------------------
The newest land-bank statement found is DATED 02-AUG-2026 and is the CEO's own numbers in
a company statement: about 1,450 feddans of developable land left, of which about 700
feddans inside New Heliopolis, after roughly 2,500 feddans were contracted out to partner
developers over the preceding three years, with the portfolio split about 70 per cent
partnership / 30 per cent self-development (F30). That figure reaches this register through
the press, which is a provenance problem, not a vintage problem.

THE ORDERING, STATED EXPLICITLY BECAUSE THE INSTRUCTION REQUIRES IT AND BECAUSE IT IS THE
FINDING RATHER THAN A FOOTNOTE:
  * newest land-bank figure sourced .............. 02-Aug-2026  (~1,450 feddans, CEO
                                                    statement relayed by masrawy)
  * newest COMPANY-OWN land statement sourced .... 09-Sep-2026 retrieval of an UNDATED
                                                    corporate page reading "1400 + Acres
                                                    of land for development" (F28)
  * newest filing sourced ........................ NONE. No financial statement of any
                                                    period was obtainable.
So the asset base is NOT older than the information set — it is newer than every company
document in this register. The ordering test is passed in form and is EMPTY in substance,
because the information set has no statement in it at all. A later build must re-run the
land-bank question against the FY2025 balance sheet and the H1-2026 interim once they are
in hand, and must not carry 1,450 feddans into an RNAV beside a balance sheet it has never
read.

LAND HAS BEEN ADDED AND RESTATED REPEATEDLY, WHICH IS PRECISELY THE DEFECT [R-ASSET-01]
WAS ADOPTED ON. Within the last 24 months: ~766 feddans acquired at Hadayek El Asema
(Capital Gardens) during 2025; ~52,000 sqm acquired in East Mansoura; and about 710,000
sqm of previously disputed "excess area" in New Heliopolis regularised with the New Urban
Communities Authority on 22-Jan-2026 after a dispute that had run since 1995. A study that
takes a 2024 land figure and glides it is wrong before it starts.

TWO TRAPS INSIDE THE LAND NUMBER ITSELF:
  1. UNIT. The company's own English pages say "acres" where its own Arabic text says
     "فدان" (feddan) for the same plots — New Heliopolis is "5,400 acres" on the
     partnerships page and 5,406 feddans on the New Heliopolis page; Ajad is 77.19
     "acres" in one place and 77.91 feddans in another. A feddan is 4,200.833 sqm and an
     acre is 4,046.856 sqm, a 3.8 per cent difference. At 1,450 units the gap is
     6.09m sqm versus 5.87m sqm — 221,000 sqm, which is not a rounding error in an RNAV.
     Every land figure in this register is recorded in the unit the source printed and is
     NOT converted.
  2. WHAT "OWNS" MEANS. Roughly 2,500 feddans are already committed under revenue-share
     partnership contracts. Those hectares are not a second, separate asset to value
     beside the contracted revenue streams. Counting both is double counting.

-------------------------------------------------------------------------------
STATE OWNERSHIP AND LITIGATION — MATERIAL AND LONG-RUNNING, AS INSTRUCTED
-------------------------------------------------------------------------------
The state, through the Holding Company for Construction and Development, is the
controlling shareholder. The company's own history page states that Misr Al Gadida was
established as an HCCD subsidiary in 1991 and that 10 per cent of its shares were offered
to the public on 27 September 1995; a serving HCCD Managing Director sits on its board
(F35). The commonly quoted 72.3 per cent is NOT from a company document and is quarantined
as such (F36); no company-official shareholder disclosure could be reached and no named
state-stake transaction was found (F37 negative search).

The auditor is the CENTRAL AUDITING ORGANIZATION, the state audit authority — the company's
own OGM agenda lists its report as a separate item from the external auditor's report
(F26). Its report on the FY2025 statements carries qualifications that go to the land base
itself: EGP 13bn of Hadayek El Asema land classified under projects-under-construction
rather than land inventory although no project or partnership had been established on it
at the reporting date; land inventory held for sale not measured at the lower of cost and
net realisable value; and encroachments by individuals and entities on company land and
buildings of about 2,074 feddans, over 8 million sqm (F42, F43). The company's reply is
that the classification does not affect equity, that land is valued by CBE-accredited
valuers at each partnership, that land value has roughly quadrupled in three years, and
that disputes with Zahraa El Maadi, Maadi for Construction and the National Company for
Asset Management have been settled, with the Nadi El Shams land compensated by alternative
land in New Obour (F44). BOTH the qualification and the reply reach this register through
the press. Neither is verified against a primary document, and both are flagged.

-------------------------------------------------------------------------------
NO BETA IS RESOLVED HERE, BY INSTRUCTION
-------------------------------------------------------------------------------
Recorded instead (F47): the listing is the Egyptian Exchange, EGX, ticker HELI (HELI.CA),
listed since 1995, quoted in EGP; no second listing, GDR or depositary line was found, so
the dual-listing trap that ORAS carries is not live on this name — but that is a negative
search, not a company confirmation. The price series that exists in this repository is
engine/raw_ohlc/EG/HELI.csv: 3,763 daily rows, 02-Jan-2011 to 23-Aug-2026, last close EGP
7.75, single-digit EGP throughout, which matches an EGX-quoted local line rather than any
foreign line. The exchange index for EG/EGX in this repository is
engine/raw_indices/EG/EGX30.csv, which runs to 08-Sep-2026 — SIXTEEN CALENDAR DAYS LONGER
than the stock file. The regressor ruling and the beta are not this sweep's to take.
AND A WARNING FOR WHOEVER DOES TAKE IT: two bonus issues sit inside this window (a bonus
share with the FY2024 distribution in May-2025, and two bonus shares per share with the
FY2025 distribution in May-2026, which took issued capital from EGP 333.8m to EGP 1,001.4m
at EGP 0.25 par, i.e. from ~1.335bn to ~4.006bn shares). Step 0.0 must establish whether
the stored price series is adjusted for them before any return, beta or per-share figure
is computed off it.

-------------------------------------------------------------------------------
WHAT TO ATTACH — the sweep stops here and asks rather than substituting
-------------------------------------------------------------------------------
  1. Audited annual financial statements (standalone and consolidated if issued) for the
     years ended 31-Dec-2022, 31-Dec-2023, 31-Dec-2024 and 31-Dec-2025, with the auditor's
     report and the Central Auditing Organization's report.
  2. Reviewed interim statements for the three months ended 31-Mar-2026 and the six months
     ended 30-Jun-2026.
  3. The board's report and the results announcements filed with EGX for FY2025, Q1-2026
     and H1-2026 (the operating anchors — land, partnership backlog, collections — are in
     the release, not in the statements).
  4. The FY2025 corporate governance report and the shareholder structure page from the
     company's own IR portal (the tab exists at
     https://ir.egidegypt.com/en/governance/l2CcUsLEX0X_jNgUyU870fBLV0SPpysHh_i22D-IFog!
     and cannot be read because its data port is shut).
Routes tried for each are logged above and in `primary_access`.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))

from research_sweep import (SweepRegister, AssetClass, Ring, FindingClass,   # noqa: E402
                            SourceType, DriverMode)

SWEEP_DATE = "2026-09-09"
R = SweepRegister("HELI", AssetClass.STOCK, SWEEP_DATE)

CO = SourceType.COMPANY_OFFICIAL
IR = SourceType.COMPANY_IR
REG = SourceType.REGULATOR_OFFICIAL
PMD = SourceType.PRIMARY_MARKET_DATA
PRESS = SourceType.REPUTABLE_PRESS
AGG = SourceType.AGGREGATOR

SITE = "http://misr-algadida.com"
APPKEY = "l2CcUsLEX0X_jNgUyU870fBLV0SPpysHh_i22D-IFog!"

# ---------------------------------------------------------------------------
# PRIMARY ACCESS LOG — logged whether it succeeded or was blocked, with the
# actual failure text. Never a remembered one.
# ---------------------------------------------------------------------------
R.record_primary_access(
    f"{SITE}/", True, SWEEP_DATE,
    "HTTP 200 over PLAIN HTTP. This is the company's live corporate site (Misr Al Gadida "
    "= Heliopolis Company for Housing and Development). Apache/2.4.63 (Ubuntu).")
R.record_primary_access(
    "https://misr-algadida.com/", False, SWEEP_DATE,
    "curl: (60) SSL certificate problem: certificate has expired. The company's own TLS "
    "certificate is expired; the site is only readable over http. A run that tries https "
    "and stops will wrongly conclude the company has no website.")
R.record_primary_access(
    f"{SITE}/investor-relations", True, SWEEP_DATE,
    "HTTP 200. Twelve IR tabs, every one an iframe onto ir.egidegypt.com with appKey "
    f"{APPKEY} — the page itself hosts no document.")
R.record_primary_access(
    f"https://ir.egidegypt.com/en/financialstatement/{APPKEY}", False, SWEEP_DATE,
    "HTTP 200 but 22,613 bytes of Angular shell with no data. The financial-statement "
    "library is rendered client-side from an API this environment cannot reach.")
R.record_primary_access(
    "https://ir.egidegypt.com/assets/config.json", True, SWEEP_DATE,
    'HTTP 200. Names the reason the library cannot be read: {"frontUrl":'
    '"https://ir.egidegypt.com","baseUrl":"https://ir.egidegypt.com:8080",'
    '"authUrl":"/api/identity/Auth/token"} — the document API is on port 8080.')
R.record_primary_access(
    f"https://ir.egidegypt.com:8080/api/identity/Settings/getCompanySettings/{APPKEY}",
    False, SWEEP_DATE,
    "https -> 'curl: (35) Recv failure: Connection reset by peer' (4 attempts); "
    "http -> 'curl: (28) Connection timed out after 30002 milliseconds'. Proxy log: "
    "kind 'ws_closed_mid_exchange', detail 'tunnel closed (code 1006, Connection ended) "
    "after 6s; 517 B sent, 39 B received, client reading'. Port 8080 does not pass.")
R.record_primary_access(
    "https://data.egidegypt.com/", False, SWEEP_DATE,
    "HTTP 403 on root; /api/Feed/GetCompanyProfile?SYMBOL_CODE=HELI -> HTTP 404 (IIS). "
    "This is the EGID attachment host and it answers, but attachment paths are only "
    "issued by the port-8080 API, so no document can be addressed on it.")
R.record_primary_access(
    "https://www.heliopoliscompany.com/", False, SWEEP_DATE,
    "HTTP 200, 114 bytes: a JavaScript redirect to /lander which 302s to "
    "forsale.godaddy.com. The domain aggregators and brokers still publish as this "
    "issuer's website is EXPIRED AND PARKED FOR SALE. It is not the company.")
R.record_primary_access(
    "https://www.egx.com.eg/en/DisclosureAll.aspx", False, SWEEP_DATE,
    "Default curl UA -> 'curl: (52) Empty reply from server'. WITH A BROWSER UA -> HTTP "
    "200 carrying an F5/TSPD bot-defence CAPTCHA: 'Please enable JavaScript to view the "
    "page content. Your support ID is: 6431284897889349852 ... What code is in the "
    "image?' A 200 that is not a page. No CAPTCHA was solved.")
R.record_primary_access(
    "https://www.egx.com.eg/downloads/Bulletins/302003_2.pdf", False, SWEEP_DATE,
    "HTTP 200 with a browser UA but content_type text/html, 6,139 bytes — the same F5 "
    "challenge. Static files behind the portal are gated too, so even a known filing "
    "path would not fetch.")
R.record_primary_access(
    "https://web.archive.org/save/https://www.egx.com.eg/en/DisclosureAll.aspx",
    False, SWEEP_DATE,
    "HTTP 520, body 'Sorry Job failed'. The Internet Archive cannot fetch the EGX "
    "disclosure index either. CDX search itself works and shows HELI documents on "
    "egx.com.eg only for 2011-2013 and zero egx.com.eg PDFs archived since 2024-01-01.")
R.record_primary_access(
    "https://www.mubasher.info/markets/EGX/stocks/HELI/financial-statements", False,
    SWEEP_DATE,
    "HTTP 403, Cloudflare 'Attention Required!'. Logged for completeness only — an "
    "aggregator is not a permitted source for this company's own reported figures.")
R.record_primary_access(
    "https://www.hccd.com.eg/ (state parent) and https://mpbs.gov.eg/ (ministry)",
    False, SWEEP_DATE,
    "Both: 'gateway answered 502 to CONNECT (policy denial or upstream failure)'. The "
    "controlling shareholder's own site and the supervising ministry's site are both "
    "unreachable, so neither could corroborate the shareholding.")
R.record_primary_access(
    "https://fra.gov.eg/", True, SWEEP_DATE,
    "HTTP 200. Reached and searched: the Financial Regulatory Authority publishes its "
    "own decisions and registers but no listed-company financial-statement library, so "
    "it is not a route to the filings.")
R.record_primary_access(
    "https://www.cbe.org.eg/en/economic-research/statistics/"
    "overnight-deposit-and-lending-rate", True, SWEEP_DATE,
    "HTTP 200 WITH A BROWSER USER AGENT. Recorded because earlier registers in this "
    "repository logged cbe.org.eg as a WAF interstitial: the block is user-agent gated, "
    "not absolute. The rate and FX pages read cleanly once a browser UA is sent.")

R.declare_study_year("2026", ["Q1-2026", "Q2-2026"])

# ===========================================================================
# RING 1 — GLOBAL
# ===========================================================================
f_fx = R.add(
    Ring.GLOBAL, "rate cycle & USD/FX regime", FindingClass.D,
    "EGP/USD 50.9786 buy / 51.0786 sell at the CBE's own published average market rate, "
    "08-Sep-2026 — a pound that has been broadly stable through 2026 rather than sliding",
    "Central Bank of Egypt — Exchange Rates (Average Market Rate in EGP), page dated "
    "08 Sep 2026", REG, "2026-09-08",
    url="https://www.cbe.org.eg/en/economic-research/statistics/exchange-rates",
    detail="Read direct from the CBE with a browser user agent. Euro 59.1810/59.4350, "
           "Saudi riyal 13.5747/13.6017, UAE dirham 13.8793/13.9080 on the same table.",
    model_impact="DRIVER UNLOCK for the currency frame: a stable EGP is what allows the "
                 "Gulf-partner and USD-referenced land-value commentary to be compared "
                 "with EGP contract minimums without an implicit devaluation assumption. "
                 "Sets the FX line of any USD cross-check and the sensitivity axis.")

f_gcost = R.add(
    Ring.GLOBAL, "commodity complex (input/output)", FindingClass.S,
    "Egyptian construction costs kept rising through H1-2026 on imported inputs, reduced "
    "energy subsidies and restrictive financing; FX, domestic liquidity and GDP are the "
    "strongest drivers of local material prices, not the CPI",
    "Gleeds Egypt Construction Market Report Q1/Q2 2026; Emerald/SASBE vector-"
    "autoregression study of Egyptian construction material prices (steel, cement, "
    "bricks, gypsum board, ceramic tiles)", PRESS, "2026-06-30",
    model_impact="Sets the direction of the self-development cost line: build cost per "
                 "sqm rises with FX and energy reform and does not deflate with headline "
                 "inflation. On the partnership model this pressure sits with the PARTNER "
                 "developer, which is the mechanism that makes HELI's disclosed gross "
                 "margin structurally higher than a self-building peer's.")

f_gulf = R.add(
    Ring.GLOBAL, "global sector demand", FindingClass.S,
    "Gulf capital is rotating from outright acquisitions into revenue-share partnerships "
    "with Egyptian landowners — an estimated USD 35-40bn of Gulf-linked projects live in "
    "2026, Qatari Diar launching phase one of a USD 30bn Egyptian development and "
    "transferring USD 3.5bn to the state in late 2025",
    "Ahram Online, 'Egypt's real estate market shifts from Gulf acquisitions to strategic "
    "partnerships'; AGBI, 'Qatari Diar launches phase one of $30bn Egypt development'; "
    "Arabian Business on 2026 Gulf inflows", PRESS, "2026-08-31",
    model_impact="This is the demand side of HELI's entire business model. The company "
                 "monetises land by contracting it to developers for a revenue share, so "
                 "partner appetite IS the driver of new contract signings. Sets the "
                 "probability and pace of further partnership announcements in the "
                 "explicit window, and the bear case if that appetite cools.")

f_trade = R.add(
    Ring.GLOBAL, "trade / sanctions / supply chains", FindingClass.C,
    "Regional geopolitics and Red Sea shipping disruption continued to lengthen and price "
    "up imported construction inputs into Egypt in H1-2026; Suez activity remains a drag "
    "on the national accounts even as non-oil manufacturing and tourism offset it",
    "Gleeds Egypt Construction Market Report Q1/Q2 2026; IMF commentary relayed by Ahram "
    "Online and Amwal Al Ghad on the 2026 growth upgrade", PRESS, "2026-07-31",
    model_impact="")

# ===========================================================================
# RING 2 — COUNTRY
# ===========================================================================
f_cbe = R.add(
    Ring.COUNTRY, "sovereign macro (inflation, policy rate, FX/deval risk)",
    FindingClass.D,
    "CBE overnight deposit rate 19.00% and overnight lending rate 20.00%, effective from "
    "15 Feb 2026, page last updated 12 Feb 2026 — no change published since",
    "Central Bank of Egypt — Overnight Deposit and Lending Rate", REG, "2026-02-12",
    url="https://www.cbe.org.eg/en/economic-research/statistics/"
        "overnight-deposit-and-lending-rate",
    detail="Read direct from the CBE with a browser user agent; the page prints both its "
           "'Last Updated' and 'Effective from' dates, which is why both are carried.",
    model_impact="DRIVER UNLOCK: fixes the explicit-window local-currency risk-free "
                 "anchor at the CBE's published corridor rather than at a vendor's "
                 "number, and dates it. Any Ke or Kd build in a later study starts here.")

f_cbetgt = R.add(
    Ring.COUNTRY, "sovereign macro (inflation, policy rate, FX/deval risk)", FindingClass.S,
    "The CBE's own inflation target for Q4-2026 is 7% (+/- 2pp); the Bank paused its "
    "easing cycle in 2026 after inflation fell to 11.9% in January 2026, and the IMF "
    "lifted Egypt's 2026 growth forecast to 4.6% in its July-2026 WEO update",
    "Central Bank of Egypt — Inflation page (last updated 10 Aug 2026) for the framework "
    "and target; IMF July-2026 WEO update relayed by Amwal Al Ghad and Arab Finance for "
    "growth", REG, "2026-08-10",
    url="https://www.cbe.org.eg/en/monetary-policy/inflation",
    model_impact="Sets the TERMINAL risk-free build: the norm is constructed off the "
                 "CBE's own published medium-term target plus an EM real-rate "
                 "convention, never off a historical average and never off a spot yield. "
                 "Also sets the direction of the discount-rate glide.")

f_fra = R.add(
    Ring.COUNTRY, "regulatory environment (regulator, caps, tariffs, tax/subsidy)",
    FindingClass.S,
    "The FRA amended Decision 179/2025 to ease developer-to-REIT conversion: a single "
    "test of net equity of at least EGP 500m per the latest approved statements replaces "
    "the old twin test, with borrowing capped at 60% of fund NAV; separately the housing "
    "ministry is drafting a real-estate development governance law and an Egyptian "
    "Federation of Developers that would license and grade developers, and broker "
    "registration was made compulsory by Ministerial Decision 578/2025 (published in "
    "Al-Waqa'i Al-Masriya on 17-Jan-2026)",
    "Ahram Online on the FRA board amendment; Daily News Egypt, 'Egypt drafts new real "
    "estate governance law, plans unified body for developers' (24-May-2026); Shalakany "
    "Law Office and Property Finder on Ministerial Decision 578/2025", PRESS, "2026-05-24",
    model_impact="Two live channels. (1) A REIT-conversion route is a real alternative "
                 "monetisation of a land bank and belongs in the optionality discussion "
                 "rather than the base case. (2) Developer licensing and grading raises "
                 "the barrier for the small partners HELI contracts with, which "
                 "concentrates future partnership tenders on the large names it has "
                 "already signed — supports contract continuity, narrows partner choice.")

f_state = R.add(
    Ring.COUNTRY, "fiscal / political events with sector read-through", FindingClass.S,
    "The Ministry of Public Business Sector reported EGP 126bn of revenue across its "
    "companies, up about 20%, and roughly EGP 24bn of net profit in FY2024-25, and "
    "presents asset monetisation as policy; separately the housing ministry is offering "
    "10,000 feddans of serviced land to individuals under the 'Maskan' programme in 2026",
    "Ministry of Public Business Sector year review, republished by the company itself in "
    "its own media centre; Al Arabiya on the 10,000-feddan land offering", CO,
    "2026-01-31", url=f"{SITE}/media/33",
    detail="Carried as company-official because the company republished the ministry "
           "review on its own site; the underlying claims are the ministry's.",
    model_impact="Sets the policy backdrop for the controlling shareholder's intentions: "
                 "asset monetisation is the stated objective of HELI's owner, which is "
                 "the political mechanism behind the partnership programme. The state's "
                 "own serviced-land offerings are simultaneously the competing supply "
                 "into the same buyer pool — carried as a cap on land-price escalation.")

# ===========================================================================
# RING 3 — INDUSTRY
# ===========================================================================
f_dem = R.add(
    Ring.INDUSTRY, "demand drivers & capacity/supply balance", FindingClass.S,
    "Around 221,000 residential units across 139 projects are on the market in Cairo, "
    "apartments 66% of supply and 51% of stock sold unfinished; the Egyptian residential "
    "market is put at USD 9.81bn in 2025 rising to USD 10.71bn in 2026, a 9.09% CAGR to "
    "2031",
    "Mordor Intelligence — Residential Real Estate Market in Egypt; corroborated on the "
    "supply count by Sands of Wealth's 2026 market analysis", PRESS, "2026-06-30",
    model_impact="Sets the absorption assumption behind HELI's partner developers' "
                 "revenue, which is what the guaranteed-minimum contracts are struck "
                 "against. A supply glut is the mechanism by which a partner falls back "
                 "on the minimum rather than the share — the single most important "
                 "sensitivity on the partnership revenue driver.")

f_price = R.add(
    Ring.INDUSTRY, "pricing", FindingClass.S,
    "Egyptian residential prices are expected up roughly 10-18% in nominal EGP over the "
    "next twelve months, with Mostakbal City 15-22%, New Zayed 14-20% and Ras El Hekma "
    "16-25% at the top of the range — i.e. nominal escalation broadly at or a little "
    "below inflation, not the 2023-24 step-change",
    "Sands of Wealth, 'Property Price Forecasts Egypt (2026)'; Buildex market report on "
    "New Cairo / NAC / Zayed pricing", PRESS, "2026-07-31",
    model_impact="Sets the price leg of any volume x price build for self-developed "
                 "units and the escalation applied to partner revenue above the "
                 "guaranteed minimum. Nominal escalation below the discount rate is what "
                 "makes the guaranteed minimums, not the share, the binding case in the "
                 "bear scenario.")

f_entrant = R.add(
    Ring.INDUSTRY, "new entrants (named-competitor level)", FindingClass.S,
    "Named new capacity entering HELI's own catchment: Qatari Diar at Alam El-Roum, VIE "
    "Communities (Egyptian-Emirati) with over EGP 150bn of mixed-use in New Cairo and the "
    "North Coast, and PARAGON with Saudi Arabia's ADEER on 'Sumou Boulevard' in Mostakbal "
    "City at about EGP 70bn",
    "Arabian Business and Ahram Online on 2026 Gulf-linked project pipeline; AGBI on "
    "Qatari Diar", PRESS, "2026-08-31",
    model_impact="These are the alternatives HELI's future partners can take their "
                 "capital to. Sets the competitive tension in the terms of the NEXT "
                 "partnership contract — the revenue-share percentage and the guaranteed "
                 "minimum — rather than the ones already signed.")

f_tech = R.add_negative(
    Ring.INDUSTRY, "technology substitution",
    "searched: 'Egypt real estate technology substitution modular construction prefab "
    "proptech disrupting developers 2026', 'بدائل تكنولوجية التطوير العقاري مصر 2026', "
    "and the construction-materials and residential-market reports above for any "
    "substitution threat to conventional developed-plot housing. Nothing found. The land-"
    "monetisation model HELI runs is a legal and planning construct, not a technology; "
    "the live technology questions in the reports are BIM, digital sales channels and the "
    "e& Business smart-city agreement HELI itself signed, all of which are cost or "
    "service items rather than demand substitution", SWEEP_DATE)

f_peer = R.add(
    Ring.INDUSTRY, "competitor capacity / price moves (named)", FindingClass.S,
    "Named EGX peers posted the same 2026 step-change and are simultaneously HELI's "
    "counterparties: Madinet Masr is both a listed competitor and HELI's 491-feddan "
    "partner and was buying 411,200 treasury shares on 30-Aug-2026 while reporting H1-2026 "
    "infrastructure spend of EGP 3.5bn; Cairo Housing multiplied H1-2026 profit 13.5x "
    "(+1,249%); SODIC has been HELI's partner on 655 feddans since 2016",
    "Al Borsa News (30-Aug-2026 treasury purchase; 09-Aug-2026 infrastructure spend; "
    "20-Aug-2026 Cairo Housing H1-2026); the company's own partnerships page for the "
    "SODIC and Madinet Masr relationships", PRESS, "2026-08-30",
    model_impact="Fixes the relative-multiple peer set AND flags that the peer set is "
                 "contaminated: two of the closest comparables are counterparties whose "
                 "own results embed the other side of HELI's contracts. Any multiple "
                 "lens must be applied to normalised earnings and must say which peers "
                 "are counterparties.")

# ===========================================================================
# RING 4 — COMPANY
# ===========================================================================
# ---- strategic plans & guidance -------------------------------------------
f_guid = R.add(
    Ring.COMPANY, "strategic plans & guidance", FindingClass.S,
    "CEO statement 02-Aug-2026: the company targets ~30% ANNUAL PROFIT GROWTH across 2026 "
    "and 2027, has contracted about 2,500 feddans in New Heliopolis to partner developers "
    "over the last three years, still owns about 700 feddans inside the city, and holds a "
    "developable land portfolio of about 1,450 feddans, roughly 70% of which is monetised "
    "through partnerships and 30% self-developed",
    "Company statement by Managing Director & CEO Dr Sameh El Sayed, relayed by Masrawy, "
    "'مصر الجديدة للإسكان تستهدف نمو الأرباح 30% سنويًا خلال 2026 و2027'", PRESS,
    "2026-08-02",
    url="https://www.masrawy.com/news/news_economy/details/2026/8/2/3026796/",
    detail="PROVENANCE FLAG: this is the company's own statement reaching the register "
           "through the press because the company's own IR channel could not serve it. "
           "The 30% growth target and every land figure in it must be re-sourced from "
           "the company's filing or release before any of it is modelled. "
           "ARITHMETIC CHECK PERFORMED: ~700 feddans retained in New Heliopolis plus the "
           "~766 feddans acquired at Hadayek El Asema equals ~1,466, which reconciles to "
           "the stated ~1,450 developable feddans within rounding. The two independent "
           "statements are therefore consistent with each other.",
    model_impact="THE ASSET BASE ITSELF and the growth frame. Sets (a) the land quantity "
                 "any RNAV or land-monetisation lens starts from, dated 02-Aug-2026; "
                 "(b) the 70/30 split that decides how much of forward revenue is "
                 "contracted share versus self-developed volume x price; (c) a "
                 "management growth target that is REPORTED and never adopted as a "
                 "forecast input.")

f_selfdev = R.add(
    Ring.COMPANY, "strategic plans & guidance", FindingClass.D,
    "Self-development pipeline, from the company's own project pages: Jadinah, a 300-"
    "feddan fully integrated community delivered in three phases, phase one launched "
    "September 2025 and the first Egyptian compound to win the Green Pyramid (GPRS) Gold "
    "rating; plus named New Heliopolis schemes with unit counts — Bronze Villas (24 "
    "villas, 297 sqm built-up each, Block 52F), Jewels (10 buildings, third phase of a "
    "28-building block), Medallion (85 residential units and 29 commercial shops across "
    "six buildings), Scarlet",
    "Company website — Our Projects and media releases", CO, SWEEP_DATE,
    url=f"{SITE}/our-projects",
    detail="Pages are undated on the company's site; source_date is the retrieval date "
           "and is labelled as such rather than invented.",
    model_impact="DRIVER UNLOCK: gives a unit-level base for the self-developed 30% of "
                 "the portfolio — countable units and built-up areas by scheme rather "
                 "than a blended revenue growth rate. This is the finest sourced level "
                 "available for the self-development leg.")

f_pricepoint = R.add(
    Ring.COMPANY, "IR communications (calls, presentations, releases)", FindingClass.D,
    "The company's own New Heliopolis page publishes the retail terms it sells on: "
    "starting price EGP 6,100,000, 10% down payment, 10 years to pay, across villa, "
    "chalet, townhouse and apartment product; the city is stated at 5,406 feddans, "
    "established by presidential decree, planned for up to 250,000 residents",
    "Company website — New Heliopolis (IR/marketing product page)", IR, SWEEP_DATE,
    url=f"{SITE}/new-heliopolis",
    detail="Undated page; retrieval date carried. This is the price-per-unit and payment-"
           "terms data no financial statement carries, which is exactly why the IR "
           "channel is a mandatory source and not an optional one.",
    model_impact="DRIVER UNLOCK for the price leg of the self-development build and for "
                 "the collections profile: a 10% down payment over a 10-year plan sets "
                 "the cash-conversion lag between a recognised sale and cash, which is "
                 "the single largest difference between HELI's profit and its cash flow.")

# ---- IR communications ------------------------------------------------------
f_irch = R.add(
    Ring.COMPANY, "IR communications (calls, presentations, releases)", FindingClass.S,
    "The company's IR channel exists and publishes twelve categories — Stock Performance, "
    "Financial Statements, Latest Announcements, Stock News, Corporate Actions, Insider "
    "Transactions, Disclosure, Governance Report, Board of Directors, Company Data, IR "
    "Contacts and a Calculator — all served through EGID's hosted widget, and NONE of "
    "them can be read from this environment because the widget's data API is on port 8080",
    "Company website — Investor Relations, and ir.egidegypt.com config.json", IR,
    SWEEP_DATE, url=f"{SITE}/investor-relations",
    detail="The tab list is itself the finding: it tells a later run exactly which "
           "documents exist and where, so the ask to the principal can name them.",
    model_impact="Gate consequence, not a number: every driver that would need a filing "
                 "is forced TOP_DOWN or blocked outright by this one access failure. It "
                 "is the reason this register carries no is_fs_data finding.")

f_9m25 = R.add(
    Ring.COMPANY, "IR communications (calls, presentations, releases)", FindingClass.D,
    "The company's own 9M-2025 results release: total revenue EGP 1.274bn for the period "
    "ended 30 September 2025, up 42% year on year, with Q3-2025 alone at EGP 1.156bn "
    "against EGP 722m a year earlier (+60.18%); the company attributes the fall in net "
    "profit to moving away from parking liquidity in treasury bills and into expanding "
    "its land portfolio and self-financing projects; Jadinah phase one (300 feddans) "
    "launched in September 2025",
    "Company media centre — 'Misr Al Gadida achieves revenues exceeding EGP 1.27 billion, "
    "marking 42% growth during the first nine months of 2025'", IR, "2025-11-15",
    url=f"{SITE}/media/32", fiscal_period="9M-2025",
    detail="THE ONLY RESULTS COMMUNICATION OF ANY PERIOD OBTAINED FROM A COMPANY CHANNEL. "
           "The page is undated; 2025-11-15 is a conservative placement inside the "
           "Egyptian 9M filing window and is flagged as inferred, not printed. No "
           "statement backs it, so it is NOT tagged is_fs_data.",
    model_impact="DRIVER UNLOCK, with a caveat: gives the only company-sourced revenue "
                 "shape in the register — quarterly revenue is violently lumpy (Q3-2025 "
                 "alone was 91% of the first nine months), which rules out any smoothed "
                 "quarterly glide and forces a contract-event revenue model. Also names "
                 "the treasury-income leg that a later P&L reconstruction must separate "
                 "from operating profit.")

# ---- regular disclosures ----------------------------------------------------
f_ogm = R.add(
    Ring.COMPANY, "regular disclosures", FindingClass.D,
    "The company's own Ordinary General Assembly invitation convenes the meeting for "
    "Saturday 2 May 2026 over the financial year ENDED 31 DECEMBER 2025, with a ten-item "
    "agenda: board report, EXTERNAL AUDITOR's report, a SEPARATE report of the state "
    "accountability authority (the Central Auditing Organization), approval of the "
    "financial statements, the corporate governance report with an independent assurance "
    "report and ESG and TCFD sustainability reports, board discharge, a cash dividend out "
    "of FY2025 profits with payment dates to be set with MCDR and EGX, board remuneration "
    "for FY2026, donations, and reappointment of the external auditor for FY2026",
    "Company media centre — OGM invitation (E-Magles registration at "
    "https://emagles.com/voterinformation/HELI)", CO, "2026-04-01",
    url=f"{SITE}/media/38",
    detail="THE FISCAL-YEAR QUESTION IS SETTLED HERE, FROM THE COMPANY'S OWN DOCUMENT: "
           "HELI reports on a 31 DECEMBER year end, not the 30 June year end that Law 203 "
           "public-sector companies often carry. A study must not assume a June year. "
           "DEFECT IN THE COMPANY'S OWN PAGE, RECORDED RATHER THAN CORRECTED: the item is "
           "headlined 'Saturday, May 2, 2025' while its body convenes 'Saturday, May 2, "
           "2026' and its agenda covers FY2025 — body and agenda agree, the headline is "
           "wrong. source_date 2026-04-01 is an inferred publication date inside the "
           "statutory notice period, not a printed one.",
    model_impact="DRIVER UNLOCK: fixes the reporting calendar (Q1/H1/9M/FY on calendar "
                 "quarters), confirms the dividend is a live annual event decided at the "
                 "OGM, and names the CAO as a second statutory auditor whose separate "
                 "report is part of the disclosure set a build must read.")

f_series = R.add(
    Ring.COMPANY, "regular disclosures", FindingClass.C,
    "Price series held in this repository: engine/raw_ohlc/EG/HELI.csv, 3,763 daily rows, "
    "02-Jan-2011 to 23-Aug-2026, last close EGP 7.75 (open 7.78, high 7.90, low 7.74, "
    "volume 9.25m); the EG/EGX index file engine/raw_indices/EG/EGX30.csv runs to "
    "08-Sep-2026, sixteen calendar days longer than the stock file",
    "engine/raw_ohlc/EG/HELI.csv and engine/raw_indices/EG/EGX30.csv (vendor market data, "
    "permitted for market data only)", AGG, "2026-08-23",
    detail="Recorded so a later build starts from the real state of the data rather than "
           "assuming it. The stock file is STALE relative to the index file, which "
           "matters for any weekly grid.",
    model_impact="")

# ---- one-off base-resetting transactions ------------------------------------
f_nuca = R.add(
    Ring.COMPANY, "one-off base-resetting transactions", FindingClass.B,
    "BASE CHANGER — LAND ADDED. The company reached a final settlement with the New Urban "
    "Communities Authority over the EXCESS AREA at New Heliopolis: about 710,000 sqm held "
    "on an undivided basis, a dispute running since 1995, closed by payment of the "
    "remaining EGP 96m claim on 22-Jan-2026 and announced 27-Jan-2026",
    "Al Borsa News, '\"مصر الجديدة\" تُنهي نزاعًا تاريخيًا على 710 آلاف متر بـ \"هليوبوليس "
    "الجديدة\"', quoting CEO Sameh El Sayed", PRESS, "2026-01-27",
    url="https://www.alborsaanews.com/2026/01/27/1945686",
    detail="PROVENANCE FLAG: company statement relayed by press; not verified against a "
           "filing. THIRTY-ONE YEARS OF DISPUTE CLOSED INSIDE THE STUDY WINDOW.",
    model_impact="BASE CHANGER, modelled explicitly and dual-framed: 710,000 sqm moves "
                 "from contingent to owned-and-developable, against a known EGP 96m "
                 "closing payment. The land base must be stated with and without it, and "
                 "the FY2025 balance sheet (pre-settlement) will NOT contain it while the "
                 "H1-2026 interim (post-settlement) should — which is exactly the "
                 "ordering [R-ASSET-01] exists to police.")

f_mm = R.add(
    Ring.COMPANY, "one-off base-resetting transactions", FindingClass.B,
    "BASE CHANGER — the Madinet Masr partnership on two New Heliopolis plots totalling "
    "491 feddans (Plot 1 245.1 fd, Plot 2 246.31 fd): total project revenue expected at "
    "EGP 194.4bn over 12 years, of which HELI's share is EGP 70.9bn with a GUARANTEED "
    "MINIMUM of EGP 53.18bn payable over 9 years; HELI's participation is 36.5% of semi-"
    "finished units plus 20% of finishing cost on fully finished units",
    "Company media centre — 'Misr Al Gadida and Madinet Masr Sign Partnership Agreement "
    "for 491 Feddans in New Heliopolis'", CO, "2026-02-15", url=f"{SITE}/media/22",
    detail="Undated page; date inferred from the release's own reference to four "
           "partnerships secured 'since November 2023' and from the partnerships page "
           "dating the Talala scheme to 2024 — flagged as inferred. The partnerships page "
           "gives the plot as 491.49 'acres' where this release says 491 feddans: the "
           "unit ambiguity is live in the company's own English text.",
    model_impact="BASE CHANGER and the single largest contracted revenue line. Gives a "
                 "contract-level bottom-up build: a floor (EGP 53.18bn over 9 years) and "
                 "an expected case (EGP 70.9bn over 12 years) for one named counterparty. "
                 "Dual-framed against the floor, never straight-lined.")

f_gdev = R.add(
    Ring.COMPANY, "one-off base-resetting transactions", FindingClass.B,
    "BASE CHANGER — two contracts with Middle East for Development & Real Estate "
    "Investment (marketed as G Developments, project 'New Kairo'): the SOUTHERN 865 "
    "feddans signed Sunday 21-Jan-2024 at 28% of semi-finished unit revenue plus 3% of "
    "finishing value, guaranteed minimum EGP 23bn and expected return EGP 39.7bn over a "
    "10-year build and 14-year sales period; and a later addendum over the NORTHERN 894 "
    "feddans with a guaranteed minimum of EGP 23.806bn, an advance payment of EGP 155.25m "
    "and a bank guarantee of EGP 134.55m",
    "Company media centre — '...Signs 865-Feddan Development Partnership...' and "
    "'...Approves Contract Addendum for 894 Feddans Development in New Heliopolis' (the "
    "latter citing the company's own statement to the Egyptian Exchange)", CO,
    "2024-01-21", url=f"{SITE}/media/30",
    detail="Two releases, both on the company's own site; the addendum release is "
           "undated on the page and post-dates the January-2024 signing.",
    model_impact="BASE CHANGER: EGP 46.8bn of combined guaranteed minimums on 1,759 "
                 "feddans, with a named advance and a named bank guarantee that fix the "
                 "early cash profile. Builds the second and third contracted revenue "
                 "streams bottom-up and dates the start of each.")

f_ajad = R.add(
    Ring.COMPANY, "one-off base-resetting transactions", FindingClass.D,
    "The fourth partnership: Ajad Developments on 77.91 feddans (the partnerships page "
    "says 77.19 acres) for the Elaia compound, Ajad's first Egyptian project, signed 2023; "
    "and the company's own aggregate — four partnerships with three developers since "
    "November 2023 carrying total GUARANTEED MINIMUM revenue of EGP 106bn, total projected "
    "revenue of EGP 166bn, expected to reach EGP 200bn over 15 years",
    "Company media centre and partnerships page", CO, "2026-02-15",
    url=f"{SITE}/partnerships",
    detail="The EGP 106bn aggregate minimum is the company's own arithmetic across its "
           "four contracts and is the cleanest single anchor in the register. NOTE the "
           "unit inconsistency inside the company's own text (77.91 feddans vs 77.19 "
           "acres) — recorded, not reconciled.",
    model_impact="DRIVER UNLOCK: converts partnership revenue from a growth rate into a "
                 "contracted schedule with a company-stated floor of EGP 106bn. The "
                 "floor, its 9-15 year spreads and its counterparty concentration are the "
                 "backbone of any revenue build.")

f_capgar = R.add(
    Ring.COMPANY, "one-off base-resetting transactions", FindingClass.B,
    "BASE CHANGER — LAND ADDED: about 766 feddans acquired at Hadayek El Asema (Capital "
    "Gardens) during 2025, the company's first major land purchase outside New Heliopolis, "
    "with master-plan design and the ministerial decree under way; and a further ~52,000 "
    "sqm plot in the East District of Mansoura contracted to a Al-Safi / Jebal consortium "
    "for mixed-use development with partnership revenue estimated at about EGP 10bn",
    "Daily News Egypt, 'Heliopolis Company for Housing to develop 766 Feddans in Hadayek "
    "Al-Asima' (01-Jun-2025), and the company's own media release on the Mansoura "
    "contracting", PRESS, "2025-06-01",
    url="https://www.dailynewsegypt.com/2025/06/01/"
        "heliopolis-company-for-housing-to-develop-766-feddans-in-hadayek-al-asima/",
    detail="The Mansoura half of this finding is company-official (media centre, "
           f"{SITE}/media/34); the Capital Gardens half is press. The consideration is "
           "reported at USD 241m in one relay and appears in the CAO report at EGP 13bn "
           "(about USD 255m at 51 EGP/USD) — the two are consistent, and neither is "
           "primary.",
    model_impact="BASE CHANGER for the asset base: the land bank GREW by roughly half its "
                 "developable area in 2025-26, which is the exact defect [R-ASSET-01] was "
                 "adopted on. It also changes the geography of the story from a single-"
                 "city land holder to a two-city one. Dual-framed with and without "
                 "Capital Gardens until the balance-sheet classification is read.")

f_park = R.add(
    Ring.COMPANY, "one-off base-resetting transactions", FindingClass.S,
    "Prior-cycle monetisation, unverified: the sale of a 7.12m sqm Heliopark plot to the "
    "National Organization for Social Insurance for a reported EGP 15bn, approved in "
    "October 2023 — a single transaction larger than any partnership minimum and the "
    "likely explanation of the FY2023-24 revenue and cash shape",
    "HC Securities note 'Heliopolis Housing, Accelerated monetization underway' "
    "(broker research; recorded as a lead, never as a figure)", PRESS, "2023-10-31",
    detail="QUARANTINED. A broker note is not a permitted source for a company-reported "
           "figure under SIGCM clause 1. It is logged so a later build knows to look for "
           "this transaction in the FY2023 and FY2024 statements, not so the number can "
           "be used.",
    model_impact="If confirmed, this resets the FY2023/FY2024 revenue base and makes any "
                 "growth rate computed off those years meaningless. Flagged as the first "
                 "thing to check when the audited statements arrive.")

# ---- ownership / stake changes ---------------------------------------------
f_hccd = R.add(
    Ring.COMPANY, "ownership / stake changes (named-transaction rule)", FindingClass.S,
    "The company's own history page states that Misr Al Gadida was established as a "
    "subsidiary of the state-owned HOLDING COMPANY FOR CONSTRUCTION AND DEVELOPMENT in "
    "1991 and that on 27 September 1995 10% of its shares were offered for public trading; "
    "its own board page lists Essam Abdel Fattah Mohamed, Managing Director for Financial "
    "and Administrative Affairs AT HCCD, as a board member, and Dr Gihan Saleh, Economic "
    "Advisor to the Prime Minister, as a non-executive member",
    "Company website — About Us (History & Company Timeline; Board of Directors)", CO,
    SWEEP_DATE, url=f"{SITE}/about",
    detail="This is the strongest COMPANY-OFFICIAL evidence of control obtainable. It "
           "establishes the controlling relationship and board representation; it does "
           "NOT state a percentage.",
    model_impact="Sets the governance frame that every other company driver sits inside: "
                 "a state-controlled issuer whose land is allocated by, and disputed "
                 "with, other arms of the same state. Feeds the discount for minority "
                 "position and the governance discussion, not a cash-flow line.")

f_float = R.add(
    Ring.COMPANY, "ownership / stake changes (named-transaction rule)", FindingClass.C,
    "The state's holding is widely reported at 72.3% through HCCD, sourced to Q1-2026 "
    "data, implying a free float of about 27.7%",
    "African Markets / Simply Wall St / press repetition of the same figure", AGG,
    "2026-03-31",
    detail="QUARANTINED — NOT A COMPANY SOURCE. No company-official shareholder structure "
           "could be read: the IR portal's Company Data tab is behind the port-8080 API "
           "and the EGX profile is behind the CAPTCHA. A build must confirm the "
           "percentage and the share count from the FY2025 governance report or the "
           "filing before using either.",
    model_impact="")

f_nostake = R.add_negative(
    Ring.COMPANY, "ownership / stake changes (named-transaction rule)",
    "searched, per the named-transaction rule and never as an estimate: 'مصر الجديدة "
    "للإسكان طرح حصة حكومية برنامج الطروحات بيع حصة الشركة القابضة للتشييد والتعمير 2025 "
    "2026 نسبة ملكية', 'Heliopolis Housing HELI state stake sale privatisation programme "
    "offering', and the company's own media centre and IR announcement tabs. NO named "
    "transaction exists: no stake sale, no secondary offering, no strategic-investor "
    "agreement and no announced intention to sell HCCD's holding was found on any date. "
    "The 72.3% figure above therefore stands unconfirmed and unchanged rather than "
    "being modelled as in play", SWEEP_DATE)

# ---- management & capital actions -------------------------------------------
f_div = R.add(
    Ring.COMPANY, "management & capital actions", FindingClass.S,
    "The 2 May 2026 OGM approved a FY2025 cash distribution of about EGP 1.78bn paid in "
    "two equal instalments of EGP 0.223 per share (first within a month of the meeting, "
    "second in December 2026) AND a capital increase from EGP 333.8m to EGP 1,001.4m "
    "(+EGP 667.6m) by issuing 2.67bn bonus shares at EGP 0.25 par — two bonus shares for "
    "every share held; the prior year's OGM (15-May-2025) had approved EGP 1.34 per share "
    "plus one bonus share",
    "Amwal Al Ghad, 'مصر الجديدة للإسكان تقر توزيعات نقدية بـ1.78 مليار جنيه عن عام 2025' "
    "(03-May-2026); Al Borsa News, 'عمومية مصر الجديدة تُقر توزيع 1.34 جنيه وسهم مجاني' "
    "(15-May-2025)", PRESS, "2026-05-03",
    detail="QUARANTINED — the OGM minutes themselves could not be reached. ARITHMETIC "
           "CHECK PERFORMED AND IT TIES: EGP 333.8m at EGP 0.25 par = 1,335.2m shares; "
           "two bonus shares each gives 4,005.6m shares = EGP 1,001.4m of capital; and "
           "EGP 1.78bn / (2 x EGP 0.223) = 3.99bn shares, which reproduces the post-bonus "
           "count. The three reported figures are mutually consistent, which raises "
           "confidence in the relay without making it primary.",
    model_impact="Sets the share count for EVERY per-share figure and the dividend path. "
                 "ALSO A DATA-QUALITY TRAP: at EGP 7.75 the post-bonus count implies a "
                 "market capitalisation near EGP 31bn, and any per-share history computed "
                 "off an unadjusted price series will be wrong by a factor of three at the "
                 "2026 bonus and six across both. Step 0.0 must settle the adjustment "
                 "before a beta or a multiple is computed.")

f_mgmt = R.add(
    Ring.COMPANY, "management & capital actions", FindingClass.C,
    "Management and governance: Dr Sameh El Sayed is Managing Director and CEO; the "
    "company issued a full ISO 37000:2021 governance policy set on 1 July 2025 — Related "
    "Party Transactions (HHD-GOV-POL-002), Insider Trading (003), Conflict of Interest "
    "(004), Disclosure (006) and Succession Planning (007), each downloadable and each "
    "carrying an issue number and issue date; the CSR policy and the Code of Conduct are "
    "image-only scans and the 'all policies' download link is broken (HTTP 404)",
    "Company website — Corporate Governance Compliance Policies (seven PDFs retrieved "
    "into engine/heli_study_pending/src/)", CO, "2025-07-01",
    url=f"{SITE}/corporate-governance-compliance-policies",
    model_impact="")

f_negcap = R.add_negative(
    Ring.COMPANY, "management & capital actions",
    "searched for a COMPANY-OFFICIAL record of the capital increase and the dividend: the "
    "IR portal's Corporate Actions and Disclosure tabs (port-8080 API, unreachable), the "
    "EGX disclosure portal (F5 CAPTCHA), the company's own media centre (30 items, none "
    "of them the OGM minutes or the corporate-action notice), and the E-Magles voter "
    "portal referenced in the OGM invitation. Nothing company-official found. The "
    "dividend, the bonus issue and the resulting share count are therefore press-relayed "
    "only and are quarantined in F(div)", SWEEP_DATE)

# ---- official financial statements ------------------------------------------
f_negfs = R.add_negative(
    Ring.COMPANY, "official financial statements",
    "THE CENTRAL FAILURE OF THIS SWEEP, searched exhaustively and closed negative. Tried, "
    "in this order: (1) the company's own site misr-algadida.com — reached over http, "
    "carries no financial statement, no annual report and no earnings release beyond the "
    "9M-2025 item; (2) its IR page's twelve EGID tabs including Financial Statements — "
    "Angular shells whose data API is https://ir.egidegypt.com:8080, which returns 'curl: "
    "(35) Recv failure: Connection reset by peer' over https and 'curl: (28) Connection "
    "timed out after 30002 milliseconds' over http; (3) the EGID attachment host "
    "data.egidegypt.com — HTTP 403 root, HTTP 404 on every guessed path, and paths are "
    "only issued by that same API; (4) the EGX disclosure portal — 'curl: (52) Empty "
    "reply from server' with a default UA and, with a browser UA, HTTP 200 carrying an "
    "F5/TSPD CAPTCHA ('...Your support ID is: 6431284897889349852 ... What code is in the "
    "image?'), including on static /downloads/ PDFs; (5) web.archive.org save-page-now on "
    "the EGX index — HTTP 520 'Sorry Job failed'; (6) Wayback CDX — HELI documents on "
    "egx.com.eg only 2011-2013, zero egx.com.eg PDFs archived since 2024; (7) the expired "
    "corporate domain heliopoliscompany.com in the archive — PDFs only 2007-2014; (8) FRA "
    "(reachable, no listed-company statement library); (9) the state parent hccd.com.eg "
    "and the ministry mpbs.gov.eg — both 502 at the proxy; (10) searches in Arabic and "
    "English for the filings as PDFs ('مصر الجديدة للإسكان القوائم المالية المستقلة "
    "المدققة 31 ديسمبر 2025 pdf', 'قائمة المركز المالي', 'Heliopolis Housing audited "
    "financial statements FY2025 pdf') — every hit was a vendor page, a broker page or a "
    "login wall. NO AUDITED OR REVIEWED STATEMENT OF ANY PERIOD WAS OBTAINED. Nothing in "
    "this register is tagged is_fs_data and the FS-DEPTH invariant is left to fire",
    SWEEP_DATE)

f_negcao = R.add_negative(
    Ring.COMPANY, "regular disclosures",
    "searched for the primary text of the Central Auditing Organization's report on the "
    "FY2025 statements and for the company's own reply to it: asa.gov.eg (reachable, "
    "publishes no company-level audit reports), the EGX disclosure portal (CAPTCHA), the "
    "company's media centre (not published there) and the IR Disclosure tab (port-8080). "
    "Only press relays of both documents were obtainable, and they are recorded as press "
    "in F(cao) and F(caoreply) rather than promoted", SWEEP_DATE)

# ---- the audit qualifications and the encroachment problem ------------------
f_cao = R.add(
    Ring.COMPANY, "regular disclosures", FindingClass.S,
    "The Central Auditing Organization's report on the FY2025 financial statements raises "
    "three findings that go to the asset base itself: (1) land carried under PROJECTS "
    "UNDER CONSTRUCTION rather than land inventory although no project had been built and "
    "no partnership struck on it at the reporting date — EGP 13bn for the Hadayek El "
    "Asema land, EGP 96.33m for a 4,945 sqm Obour plot bought from Maadi for Construction "
    "and EGP 821k for a 60-feddan Obour barter plot; (2) land inventory held for sale not "
    "measured at the lower of cost and net realisable value; (3) ENCROACHMENTS by "
    "individuals and entities on company land and buildings covering, so far as could be "
    "counted, about 2,074 FEDDANS — over 8 million sqm — limiting the company's ability to "
    "use them. It also flags EGP 46.283m of returned customer cheques, some dating to "
    "2019, with no legal action taken on part of them",
    "Osoul Misr Magazine and Al Dostor, both reporting the CAO report on the FY2025 "
    "statements and the company's reply", PRESS, "2026-04-27",
    url="https://www.osoulmisrmagazine.com/436444",
    detail="QUARANTINED: press relay of a state-audit document that could not be read "
           "directly (see the negative search above). The encroachment area alone is "
           "larger than the entire ~1,450-feddan developable portfolio the CEO cites, so "
           "the two numbers cannot both be describing the same land — reconciling them is "
           "a first-order task for the build, not a footnote.",
    model_impact="STRUCTURAL, and it points straight at the land driver. It (a) puts a "
                 "question over which land sits in inventory at what carrying value, "
                 "which is the input to any RNAV; (b) puts ~2,074 feddans of the estate "
                 "in dispute or occupation, which must be deducted or provisioned before "
                 "any land quantity is valued; (c) means the EGP 13bn Capital Gardens "
                 "land is NOT in land inventory in the FY2025 balance sheet, so a naive "
                 "read of that line will understate the land base.")

f_caoreply = R.add(
    Ring.COMPANY, "regular disclosures", FindingClass.S,
    "The company's reply: the classification of the Hadayek El Asema land as work in "
    "progress follows the start of master-plan design and the ministerial decree and does "
    "not affect shareholders' equity in any way; land is valued at CURRENT value by "
    "CBE-accredited valuers at each partnership and the guaranteed minimum is calculated "
    "from that valuation; land value has roughly QUADRUPLED over the last three years as "
    "more developers entered the city; disputes with Zahraa El Maadi, Maadi for "
    "Construction and the National Company for Asset Management have been settled and the "
    "Nadi El Shams land was compensated with alternative land in New Obour; legal "
    "proceedings are taken on returned cheques after the permitted period",
    "Al Dostor, 'مصر الجديدة للإسكان ترد على ملاحظات الجهاز المركزي للمحاسبات' "
    "(26-Apr-2026); Osoul Misr Magazine (27-Apr-2026)", PRESS, "2026-04-26",
    url="https://www.dostor.org/5526408",
    detail="QUARANTINED as press. Note what the reply concedes: the balance-sheet land "
           "value is a HISTORIC cost figure and the economic value used in contracts is a "
           "separate, four-times-higher, valuer-set number.",
    model_impact="STRUCTURAL and it decides the valuation lens: if contract minimums are "
                 "struck off independent current valuations, then the guaranteed-minimum "
                 "schedule is a better read on land value than the balance sheet is, and "
                 "an RNAV built on book land cost would be badly low. The '4x in three "
                 "years' claim is REPORTED, never adopted as an escalation input.")

# ---- the asset base, stated as an ordering ----------------------------------
f_landsite = R.add(
    Ring.COMPANY, "strategic plans & guidance", FindingClass.D,
    "The company's own corporate page states '1400 + Acres of land for development', "
    "'120 + Years of Urban Development', '3rd Oldest Real Estate Company in the world' "
    "and '+15 BEGP Market Value of assets'; its partnerships page states New Heliopolis "
    "at 5,400 acres and its New Heliopolis page at 5,406 feddans",
    "Company website — About Us and Partnerships", CO, SWEEP_DATE,
    url=f"{SITE}/about",
    detail="UNDATED ON THE SITE — this is the vintage problem in its purest form. The "
           "figure agrees with the CEO's dated ~1,450 feddans (02-Aug-2026), which is "
           "what allows it to be used at all; on its own it carries no as-at date and "
           "must never be quoted as current without one. The company's own English text "
           "uses 'acres' where its Arabic uses 'feddan' for the same plots, a 3.8% "
           "difference that is 221,000 sqm at this size.",
    model_impact="DRIVER UNLOCK, conditional: this is the only COMPANY-OFFICIAL statement "
                 "of total developable land in the register and it is the anchor for the "
                 "land-quantity driver. It must be dated from the filing before it is "
                 "used, and the unit must be resolved from the Arabic filing, not from "
                 "the English marketing page.")

f_assetbase = R.add(
    Ring.COMPANY, "strategic plans & guidance", FindingClass.S,
    "[R-ASSET-01] ORDERING, STATED EXPLICITLY: newest land-bank figure sourced is dated "
    "02-Aug-2026 (~1,450 developable feddans, CEO statement via press); newest COMPANY-OWN "
    "land statement is an UNDATED corporate page retrieved 09-Sep-2026; newest FILING "
    "sourced is NONE. The asset base is therefore not older than the information set — it "
    "is newer than every company document here — but the test passes on an information "
    "set that contains no financial statement at all",
    "This register's own retrieval log", CO, SWEEP_DATE,
    detail="Land ADDED inside the window and therefore not in older figures: ~766 feddans "
           "at Hadayek El Asema (2025), ~52,000 sqm at Mansoura (2026), ~710,000 sqm of "
           "excess area regularised with NUCA (22-Jan-2026). Land COMMITTED and therefore "
           "not separately valuable: ~2,500 feddans under partnership contracts. Land "
           "CONTESTED: ~2,074 feddans of encroachment per the CAO.",
    model_impact="Governs the asset-base record any later study must commit under "
                 "[R-ASSET-01]: quantity ~1,450 feddans, unit FEDDAN (to be confirmed "
                 "against the Arabic filing), as_at 2026-08-02, disclosure 'CEO statement "
                 "relayed by press — NOT a filing'. That last field is the reason this "
                 "study cannot yet be built: the asset base has no primary disclosure "
                 "behind it.")

f_isin = R.add(
    Ring.COMPANY, "regular disclosures", FindingClass.C,
    "Listing: the Egyptian Exchange (EGX), ticker HELI, Reuters HELI.CA, quoted in EGP, "
    "listed since 1995 with the first 10% offered on 27-Sep-1995 per the company's own "
    "history page; ISIN reported as EGS65591C017. NO SECOND LISTING, GDR OR DEPOSITARY "
    "LINE WAS FOUND, so the dual-listing trap is not live on this name",
    "Company history page (listing and 1995 offering) for the company facts; MarketScreener "
    "and Arab Finance for the ISIN string", AGG, SWEEP_DATE,
    detail="The ISIN is NOT confirmed from a company document and is flagged: the EGID "
           "widget bundle embedded on the company's own IR page carries the string "
           "EGS30031C016 in a TradingView URL, which is the widget's default symbol and "
           "not this issuer's — a trap for anyone reading the page source. The absence of "
           "a second listing is a negative search result, not a company confirmation.",
    model_impact="")

# ===========================================================================
# ARITHMETIC — what could be re-added without the statements, and what it caught
# ===========================================================================
f_arith1 = R.add(
    Ring.COMPANY, "regular disclosures", FindingClass.S,
    "ARITHMETIC CHECK ON THE RELAYED FY2025 FIGURES, AND IT CAUGHT A DEFECT. Press relays "
    "give FY2025 revenue of EGP 3.137bn against EGP 1.055bn in FY2024. One outlet prints "
    "that as '+97%' and others as '+197%'; 3.137 / 1.055 = 2.973, so the increase is "
    "197.3% and the '97%' is wrong. The same relays print gross profit of EGP 2.867bn "
    "(gross margin 91.4% against 72% in FY2024) and net profit after tax of EGP 2.705bn "
    "in one outlet and EGP 2.711bn in another against EGP 2.559bn in FY2024",
    "Osoul Misr Magazine, Al Mezan, Amwal Al Ghad, Zawya and Arab Finance relays of the "
    "company's FY2025 filing", PRESS, "2026-03-01",
    detail="QUARANTINED AND NOT USED. Recorded for two reasons: it is evidence that the "
           "relays disagree with each other at the pound level on the single most "
           "important line, and it demonstrates why a relayed figure is not a substitute "
           "for a filing. A 91% gross margin on a land-monetisation model is plausible "
           "and is exactly the kind of figure that must be verified rather than believed.",
    model_impact="Gate consequence: the margin CANNOT be set as an input on this "
                 "evidence, and a build that did so would be a QC fail. Margin is an "
                 "output of a cost-per-unit build once the statements are in hand.")

f_arith2 = R.add(
    Ring.COMPANY, "regular disclosures", FindingClass.S,
    "SECOND ARITHMETIC CHECK, ON THE SHAPE OF THE YEAR. The company's own 9M-2025 release "
    "gives revenue of EGP 1.274bn to 30-Sep-2025; the relayed FY2025 revenue is EGP "
    "3.137bn; so Q4-2025 alone carried about EGP 1.863bn, roughly 59% of the year, on top "
    "of a Q3 that was itself 91% of the first nine months. H1-2026 is separately relayed "
    "at EGP 2.24bn of revenue and EGP 1.35bn of net profit against EGP 732.79m and EGP "
    "640.29m a year earlier, announced 09-Aug-2026",
    "Company 9M-2025 release (company-official) combined with press relays of the FY2025 "
    "and H1-2026 filings — Hapi Journal, Masrawy and Amwal Al Ghad, 09-Aug-2026", PRESS,
    "2026-08-09",
    detail="QUARANTINED for the relayed halves. The arithmetic itself is this register's "
           "and is what a later build must not skip: two consecutive periods in which one "
           "quarter carries most of the year's revenue means revenue recognition here is "
           "EVENT-DRIVEN — contract signings, plot handovers and milestone recognitions — "
           "not a smooth delivery flow.",
    model_impact="Forbids a quarterly or annual growth-rate model outright. Revenue must "
                 "be built as dated contract events with their own recognition triggers, "
                 "and any cone or scenario must widen for the lumpiness rather than "
                 "assume a glide.")

# ---- awards / colour --------------------------------------------------------
f_forbes = R.add(
    Ring.COMPANY, "IR communications (calls, presentations, releases)", FindingClass.C,
    "Company-published context: ranked among Forbes Middle East's 50 most valuable "
    "companies in Egypt for a third consecutive year and sixth by value among the top ten "
    "real-estate names; a 120th-anniversary event attended by the Prime Minister; a "
    "strategic agreement with e& Business for a smart-city digital layer at New "
    "Heliopolis; an asset-management contract with Al Qalaa for the Ghurnata heritage "
    "venue at 30% of revenue with an EGP 1.8m annual minimum rising 40% from year two",
    "Company media centre", CO, SWEEP_DATE, url=f"{SITE}/media",
    model_impact="")

f_azure = R.add(
    Ring.COMPANY, "regular disclosures", FindingClass.D,
    "Unit-level sales datapoint from the company's own release: 90 residential units of "
    "varying sizes sold at the Azure compound in New Heliopolis for total sales of about "
    "EGP 428m, of which about EGP 60m collected as advances — five times the EGP 91m sold "
    "in Q1-2024 — with 200 further units planned for launch at end-October 2024",
    "Company media centre — 'Misr Al Gadida Sells 90 Residential Units in Azure Compound'",
    CO, "2024-10-01", url=f"{SITE}/media/19",
    detail="Undated page; placed at October 2024 from its own forward reference to an "
           "end-October 2024 launch. EGP 428m over 90 units implies about EGP 4.76m per "
           "unit, which sits below the EGP 6.1m starting price now published — consistent "
           "with two years of price escalation.",
    model_impact="DRIVER UNLOCK: the only units-times-price datapoint in the register, "
                 "and it also gives the cash-conversion ratio at the point of sale "
                 "(EGP 60m collected on EGP 428m sold, about 14%). Sets the self-"
                 "development volume x price build and its collections lag.")

# ===========================================================================
# DRIVER GATE TABLE — the mode each driver can be built at on TODAY's evidence.
# This is the gate, not a model. No beta row exists, by instruction.
# ===========================================================================
R.add_driver(
    "Land bank — developable area and its as-at date", DriverMode.BOTTOM_UP,
    "A company-official statement of total developable land exists ('1400 + Acres', "
    "F(landsite)) and is corroborated by a dated CEO statement of ~1,450 feddans and by "
    "the plot-level partnership contracts, which sum consistently. BOTTOM-UP AT PLOT "
    "LEVEL IS AVAILABLE. THE GAP IS FLAGGED RATHER THAN HIDDEN: the anchor page is "
    "undated, the unit (feddan vs acre) is inconsistent in the company's own English "
    "text, and ~2,074 feddans are reported encroached — so the quantity must be re-struck "
    "against the filing before it is valued.",
    [f_landsite, f_guid, f_mm, f_gdev, f_ajad, f_capgar, f_nuca, f_assetbase, f_cao])

R.add_driver(
    "Partnership revenue — per contract, guaranteed minimum and revenue share",
    DriverMode.BOTTOM_UP,
    "Four named contracts with named counterparties, each with its own area, revenue-share "
    "percentage, guaranteed minimum, expected case and tenor, all from the company's own "
    "releases: Madinet Masr 491 fd (36.5% + 20% of finishing, min EGP 53.18bn/9yr, "
    "expected EGP 70.9bn/12yr); G Developments 865 fd (28% + 3%, min EGP 23bn, expected "
    "EGP 39.7bn) and 894 fd (min EGP 23.806bn, advance EGP 155.25m, bank guarantee "
    "EGP 134.55m); Ajad 77.91 fd. Company-stated aggregate minimum EGP 106bn. This is the "
    "finest sourced level and it is contract level.",
    [f_mm, f_gdev, f_ajad, f_9m25])

R.add_driver(
    "Self-development revenue — units x price, and the collections lag",
    DriverMode.BOTTOM_UP,
    "Unit counts and built-up areas are published per scheme (Bronze Villas 24 villas at "
    "297 sqm, Jewels 10 buildings, Medallion 85 units + 29 shops, Jadinah 300 feddans in "
    "three phases), the retail terms are published (from EGP 6.1m, 10% down, 10 years), "
    "and one realised sale is disclosed (90 Azure units for EGP 428m with EGP 60m "
    "collected). Volume AND price are both projectable from company sources.",
    [f_selfdev, f_pricepoint, f_azure, f_9m25])

R.add_driver(
    "Revenue recognition timing — event-driven, not a glide", DriverMode.BOTTOM_UP,
    "The company's own 9M-2025 release plus arithmetic against the relayed full year "
    "shows one quarter carrying most of the year twice over. The recognition pattern is "
    "therefore built from dated contract events, which the company's own releases date.",
    [f_9m25, f_arith2, f_mm, f_gdev])

R.add_driver(
    "Cost of sales and cost per unit", DriverMode.TOP_DOWN,
    "FORCED TOP-DOWN BY AN ACCESS FAILURE, not by choice. No statement of any period could "
    "be obtained, so no cost line exists to build from. Until the filings arrive this "
    "driver cannot be built at all, and a top-down benchmark would be an invention rather "
    "than a floor — it is recorded here as BLOCKED so the build cannot proceed past it.",
    [f_negfs])

R.add_driver(
    "Gross and operating margin — OUTPUT, never an input", DriverMode.TOP_DOWN,
    "The only margin evidence is a press-relayed 91.4% FY2025 gross margin whose own "
    "source disagrees with itself on the revenue growth rate beside it. Setting a margin "
    "as an input on this evidence would be a QC fail; margin must fall out of a cost-per-"
    "unit build once the statements are in hand. Recorded as blocked pending the filings.",
    [f_negfs, f_arith1])

R.add_driver(
    "Balance sheet, net cash/debt and the EV-to-equity bridge", DriverMode.TOP_DOWN,
    "No balance sheet of any date could be obtained, so the bridge cannot stand on the "
    "latest disclosed balance sheet as [R-BRIDGE-01] requires. Blocked.",
    [f_negfs])

R.add_driver(
    "Land carrying value and the RNAV base", DriverMode.TOP_DOWN,
    "The CAO reports that the largest land parcel sits in projects-under-construction "
    "rather than land inventory and that inventory is not held at the lower of cost and "
    "NRV, and the company replies that economic value is set by independent valuers at "
    "each partnership and has quadrupled in three years. Neither document could be read "
    "directly. The carrying value cannot be sourced, so the RNAV base is blocked pending "
    "the filings.",
    [f_negfs, f_negcao])

R.add_driver(
    "Encroachment and dispute provision (~2,074 feddans)", DriverMode.TOP_DOWN,
    "The area is reported by the state auditor through the press and exceeds the entire "
    "stated developable portfolio, so it cannot be netted off the land quantity without "
    "the primary text. Blocked pending the CAO report and the FY2025 statements.",
    [f_negcao, f_cao])

R.add_driver(
    "Share count, per-share metrics and the dividend path", DriverMode.TOP_DOWN,
    "Two bonus issues (one share in 2025, two shares per share in 2026) and a capital "
    "increase from EGP 333.8m to EGP 1,001.4m are press-relayed only; the three relayed "
    "figures reconcile arithmetically but no company document could be read. Every "
    "per-share figure is blocked until the count is confirmed, and the stored price "
    "series must be tested for bonus adjustment first.",
    [f_negcap, f_div, f_series])

R.add_driver(
    "State shareholding and free float", DriverMode.TOP_DOWN,
    "Control is company-confirmed (HCCD parentage and an HCCD executive on the board) but "
    "the percentage is not; no named stake transaction exists on any date, so the holding "
    "is carried as unchanged rather than as in play.",
    [f_nostake, f_hccd, f_float])

R.add_driver(
    "Risk-free rate and the discount-rate glide", DriverMode.BOTTOM_UP,
    "Built from the CBE's own published corridor (19.00% deposit / 20.00% lending, "
    "effective 15-Feb-2026) for the explicit window and normed to the CBE's own published "
    "Q4-2026 target of 7% (+/-2pp) for the terminal, with the EGP frame set by the CBE's "
    "own 08-Sep-2026 exchange-rate table. Never averaged from history, never backed out "
    "of a price.",
    [f_cbe, f_cbetgt, f_fx])

R.add_driver(
    "Partner-demand and absorption sensitivity on the guaranteed minimums",
    DriverMode.BOTTOM_UP,
    "The contracts give an explicit floor and an expected case, and the market evidence "
    "gives the absorption and pricing conditions under which a partner falls back on the "
    "floor. The sensitivity is therefore built between two sourced numbers rather than "
    "assumed as a percentage haircut.",
    [f_mm, f_gdev, f_dem, f_price, f_gulf])

# ===========================================================================
# OUTPUT
# ===========================================================================
errors, warnings = R.validate()
R.to_json(os.path.join(HERE, 'sweep_register.json'))
print(R.qc_line())
print(f"\nfindings: {len(R.findings)} | drivers: {len(R.drivers)} | "
      f"primary-access attempts: {len(R.primary_access)}")
bu = sum(1 for d in R.drivers if d.mode is DriverMode.BOTTOM_UP)
print(f"driver modes: {bu} bottom-up / {len(R.drivers) - bu} top-down")
ir_n = sum(1 for f in R.findings if f.source_type is SourceType.COMPANY_IR)
co_n = sum(1 for f in R.findings if f.source_type is SourceType.COMPANY_OFFICIAL)
print(f"company-sourced findings: {co_n} COMPANY_OFFICIAL + {ir_n} COMPANY_IR")

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
print(f"\nfreshness (delivery {SWEEP_DATE}): {fr or 'OK — sweep and delivery same day'}")
fr2 = R.check_freshness("2026-09-23")
print(f"freshness (delivery 2026-09-23): {fr2 or 'OK'}")
print("\nSTOP AND INFORM: no audited or reviewed statement of any period was obtained. "
      "See the module docstring, WHAT TO ATTACH.")
