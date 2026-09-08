"""ABUK — Abu Qir Fertilizers and Chemical Industries Company (S.A.E.), EGX:ABUK.

Step 2A four-ring Information Sweep register. FIRST-BUILD study: no prior ABUK study
directory existed before this run. Runs BEFORE any forecast driver is set. Every
mandatory category of every ring is closed by a dated finding or a dated negative
search, and every negative search recorded here is a query that was ACTUALLY RUN on
the sweep date.

SOURCING NOTE — the primary-source rule worked, and this is the record of it.
The company's own site was reached at https://abuqir.net (abuqir.com, printed on the
company's own letterhead, is DEAD at this environment's proxy — connection reset by
peer — and is logged as such). Every Company-ring figure below comes from a document
served by abuqir.net: audited/reviewed financial statements, earnings releases, the
EGX "Financial Indicators" filings, the planned-budget filings, general-assembly
resolutions, board reports, shareholder-composition disclosures and material-event
disclosures. NO aggregator, broker or press figure is carried for anything the
company reported about itself. [R-SIGCM-03]'s fallback ladder was NOT needed: no
audited statement had to be substituted.

WRONG-SUBJECT TRAP, CARRIED FORWARD AND WIDENED. A football club shares this name.
abuqirfertilizers.com is the CLUB, not the issuer (fixtures, player categories,
technical staff) — a live host under a plausible name resolving to the wrong subject,
which is worse than a dead one. It was NOT fetched in this sweep. The trap is wider
than the source register recorded: the ISSUER'S OWN DOMAIN carries the club too, at
abuqir.net/abu-qir-club/ (club-bod, club-news, club-teams, club-video-gallery).
Nothing under that path enters this register.

FISCAL-YEAR BREAK — the basis break precedes modelling, and it is not what the
IR page's label says. The year-end moved from 30 June to 31 December. The audited
period ended 31-Dec-2025 is SIX MONTHS (1-Jul-2025 to 31-Dec-2025) while the company's
own IR page files it under "Q4 (Year ended December 31, 2025)". Its own governance
report names it "the Transitional Financial Period Ended December 31, 2025". Booking
its EGP 13,131,643,463 as a full year would overstate the base by roughly a factor of
two. It is tagged fiscal_period="TP-Jul-Dec-2025" here and is DELIBERATELY NOT TAGGED
"FY..." — the FS-depth invariant counts fiscal YEARS, and this is half of one. The
four fiscal years carrying is_fs_data are FY2022, FY2023, FY2024 and FY2025, all
years to 30 June, all from the company's own audited filings.

EXTRACTION ROUTE — arithmetic is the arbiter, not the extractor's confidence.
The source register's "~50 characters across 50 pages" is TRUE OF THE 31-DEC-2025
TRANSITIONAL FILING AND ITS RELEASE, and NOT true of the rest of the shelf: the
FY-Jun-2024, FY-Jun-2025 and H1-2026 statements carry healthy text layers
(1,925 / 2,087 / 2,110 characters per page). The route is therefore recorded per
document, not per company:
  * text layer, arithmetic-confirmed  — FS_FY2024_Jun, FS_FY2025_Jun, FS_H1_2026,
    ER_FY2024_Jun, ER_FY2025_Jun
  * OCR off rendered pixels (pdftoppm -> 8-bit grayscale -> tesseract 5.3.4 eng,
    --psm 6 --oem 1) — FS_TP_Dec2025 (0 chars/50 pages), FS_Q1_2026 (image pages),
    ER_H1_2026, ER_Q1_2026, ER_TP_Dec2025, the KPI/Financial-Indicators filings,
    the planned-budget filings, and every governance / material-event PDF
  * MIXED WITHIN ONE DOCUMENT, which is the trap that matters: page 5 of
    FS_FY2025_Jun (the statement of financial position) is a SCANNED IMAGE carrying
    somebody else's OCR layer inside an otherwise clean PDF — its header extracts as
    "lrant(al/tm nf finonclnl , rolt",n,nt,". It was re-read at 300dpi off the
    rendered pixels and the two routes AGREE figure for figure.
Every statement page used was footed against its own printed subtotals. Where a page
did not foot it was re-read by OCR and BOTH routes recorded (see F21).

THE ONE-EGP BREAKS ARE THE FILING'S OWN, NOT THE EXTRACTION'S. Independent 300dpi
OCR of the 31-Dec-2025 balance sheet reproduces the source register's result exactly:
non-current assets compute to 8,716,933,927 against a printed 8,716,933,928, while
total equity, total liabilities and total equity-and-liabilities all foot to the
pound and agree with each other. Recorded, not repaired.

VALIDATOR STATE: PASS, 0 errors. Warnings are printed verbatim by this module.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))

from research_sweep import (SweepRegister, AssetClass, Ring, FindingClass,   # noqa: E402
                            SourceType, DriverMode)

SWEEP_DATE = "2026-09-08"
DELIVERY_DATE = "2026-09-08"

R = SweepRegister("ABUK", AssetClass.STOCK, SWEEP_DATE)

CO = SourceType.COMPANY_OFFICIAL      # audited/reviewed FS, EGX filings, board reports
IR = SourceType.COMPANY_IR            # earnings releases, financial-indicator filings, budgets
REG = SourceType.REGULATOR_OFFICIAL
PMD = SourceType.PRIMARY_MARKET_DATA
PRESS = SourceType.REPUTABLE_PRESS
AGG = SourceType.AGGREGATOR

SITE = "https://abuqir.net"
UP = SITE + "/wp-content/uploads"

# ---------------------------------------------------------------------------
# PRIMARY ACCESS — the company's own site attempted FIRST, every attempt logged,
# success or failure. [R-SIGCM-01 / L-007]
# ---------------------------------------------------------------------------
R.record_primary_access(
    SITE + "/", reachable=True, attempt_date="2026-09-08",
    note="HTTP 200 in 2.9s. THE ISSUER. Investor-relations section present with a full "
         "document shelf: financial-statements, reports, material-events, planned-budget, "
         "dividends, shareholders, general-assemblies, board-of-directors-resolutions, "
         "shareholders-disclosure-reports. Every Company-ring figure in this register was "
         "taken from a document served by this host.")
R.record_primary_access(
    "https://www.abuqir.net/", reachable=True, attempt_date="2026-09-08",
    note="HTTP 200, 301-redirects to https://abuqir.net/. Same issuer, canonical host.")
R.record_primary_access(
    "https://abuqir.com/", reachable=False, attempt_date="2026-09-08",
    note="curl (35) Recv failure: Connection reset by peer after 12.8s — DEAD at this "
         "environment's proxy. This is the domain the company PRINTS ON ITS OWN LETTERHEAD "
         "('www.abuqir.com', 'afc@abuqir.com') on every earnings release and EGX filing, so "
         "a researcher following the filing's own footer lands on nothing. Logged rather "
         "than silently replaced. The live host is abuqir.net.")
R.record_primary_access(
    SITE + "/investor-relations/financial-statements/", reachable=True,
    attempt_date="2026-09-08",
    note="HTTP 200, 272kb. Source of every statement, earnings release and Financial "
         "Indicators filing cited below. 36 documents enumerated.")
R.record_primary_access(
    SITE + "/investor-relations/material-events/", reachable=True, attempt_date="2026-09-08",
    note="HTTP 200. Twelve material-event disclosures; six of them concern natural-gas "
         "supply interruption or restoration — the operating risk that defines this issuer.")
R.record_primary_access(
    "https://abuqirfertilizers.com", reachable=True, attempt_date="2026-09-08",
    note="NOT FETCHED IN THIS SWEEP, AND DELIBERATELY SO. Recorded reachable on the "
         "authority of engine/abuk_walkforward_pending/SOURCE_REGISTER_08-09-2026.md, which "
         "found it resolves 200 to A FOOTBALL CLUB (fixtures / player-category / "
         "technical-staff), not to the issuer. Logged so that a later reviewer sees the trap "
         "was known and avoided rather than never encountered. No content from this host, or "
         "from abuqir.net/abu-qir-club/, enters this register.")
R.record_primary_access(
    "https://abuqirfert.com | https://abuqir.com.eg", reachable=False,
    attempt_date="2026-09-08",
    note="Do not resolve (000). Recorded from the same source register. A control was run "
         "before these 000s were believed — github.com returns 400 through this container's "
         "proxy, so a 000 here is evidence about the probe, not proof about the host "
         "[R-ENF-04]. Not used to conclude 'the company has no website'.")

# The study year is CALENDAR 2026 after the year-end change. Both disclosed quarters
# are swept in BEFORE the build, not discovered after it [invariant 7 / ARCC].
R.declare_study_year("2026", ["Q1-2026", "Q2-2026"])


# ===========================================================================
# RING 1 — GLOBAL
# ===========================================================================
f_fx_regime = R.add(
    Ring.GLOBAL, "rate cycle & USD/FX regime", FindingClass.S,
    "EGP ~50.95/USD at 07-Sep-2026, broadly flat since the Jun-2026 quarter-end rate the "
    "company itself used (EGP 49.23/USD at 30-Jun-2026, printed in its own currency-risk note)",
    "USD/EGP spot series, cross-checked against the EGP 49.23/USD reporting-date rate "
    "disclosed in ABUK's own H1-2026 currency-risk note",
    PMD, "2026-09-07", url=UP + "/2026/08/Financial-statements-30-6-2026.pdf",
    model_impact="Sets the translation path for the USD 422m NET LONG foreign-currency "
                 "position the company discloses (F38), and the EGP cost of the USD-denominated "
                 "gas price floor (F06). Direction: a weaker EGP is a REVENUE and BALANCE-SHEET "
                 "tailwind and a COST headwind on the same company in the same period — which is "
                 "why the FX driver is built on the disclosed net position, never as a single "
                 "revenue multiplier.")

f_urea = R.add(
    Ring.GLOBAL, "commodity complex (input/output)", FindingClass.B,
    "Granular urea FOB Egypt round-tripped inside the study year: USD ~400-490/t before the "
    "Iran conflict, ~USD 700/t in Mar-2026, USD 694/t on 10-Apr-2026, back to the low USD 400s "
    "by end-Jun-2026 and ~USD 475/t most recently",
    "Urea (Granular) FOB Egypt futures series and contemporaneous market reporting "
    "(CNBC 25-Mar-2026; Investing.com/CBOT UFE1! series)",
    AGG, "2026-06-30",
    model_impact="BASE CHANGER for the realised-price driver, and the reason the H1-2026 "
                 "result is NOT a run-rate. ABUK's record H1-2026 (revenue +85.7%, gross margin "
                 "55.1%) was earned INSIDE the price spike; the spike had already reversed by the "
                 "period end. The price path is set on the post-reversal level with the spike "
                 "modelled as a dated, non-recurring window, never smoothed into a growth glide. "
                 "Market-data provenance only — no company figure rests on this.")

f_gdem = R.add(
    Ring.GLOBAL, "global sector demand", FindingClass.C,
    "Global urea capacity ~240Mt against ~185Mt of annual demand across ~450 producers; "
    "capacity additions ex-China have collapsed from 4.5Mt in 2023 to ~0.3Mt in 2025, and "
    "consumption growth is expected to outpace capacity growth in three of the next five years",
    "SunSirs global urea capacity review; The Western Producer nitrogen market outlook",
    PRESS, "2026-01-01",
    model_impact="")

f_trade = R.add(
    Ring.GLOBAL, "trade / sanctions / supply chains", FindingClass.B,
    "Israel shut in Leviathan and Karish and halted gas exports to Egypt from end-Feb-2026 "
    "amid the Iran conflict; Egypt cut gas supply to state petrochemical and fertilizer plants "
    "by ~50% from 17-May and brought forward LNG/FSRU imports. Resumption since has been "
    "limited to surplus volumes",
    "S&P Global Commodity Insights; MEES; MadaMasr; Al Manassa — Israeli gas export halt and "
    "Egyptian industrial gas rationing",
    PRESS, "2026-02-28",
    model_impact="Sets the UTILISATION BAND on all three ammonia/urea trains. This is the "
                 "single mechanism by which ABUK loses volume, and the company's own filings "
                 "confirm it bites (F36, F37). Volume is banded by gas availability rather than "
                 "run at plate — the same construction the EGCH same-class prior forced after "
                 "flat urea tonnes over-forecast by 9.3% in every unit-window cell.")


# ===========================================================================
# RING 2 — COUNTRY
# ===========================================================================
f_cbe = R.add(
    Ring.COUNTRY, "sovereign macro (inflation, policy rate, FX/deval risk)", FindingClass.D,
    "CBE rate path, taken from the COMPANY'S OWN significant-events note rather than relayed: "
    "25-Dec-2025 overnight deposit/lending cut 100bp to 20%/21%; 12-Feb-2026 cut to 19%/20%; "
    "2-Apr-2026 held unchanged. Urban inflation 14.9% in Jul-2026 (14.3% Jun). CBE's own "
    "targets are 7% (+/-2pp) for Q4-2026 and 5% (+/-2pp) for Q4-2028",
    "ABUK H1-2026 interim financial statements, note 48 'Significant events' item 1; "
    "Central Bank of Egypt policy decisions and CPI release",
    CO, "2026-08-13", url=UP + "/2026/08/Financial-statements-30-6-2026.pdf",
    model_impact="Explicit-window risk-free rate anchors on the 19%/20% corridor. The TERMINAL "
                 "rf is norm-built from the CBE's OWN published Q4-2028 target (5% +/-2pp) plus "
                 "the house EM real-rate convention — never a historical average, and never "
                 "backed out of a price. Country risk is counted once [L-004]: the sovereign "
                 "default spread is netted out of the local yield before any premium is added.")

f_gasprice = R.add(
    Ring.COUNTRY, "regulatory environment (regulator, caps, tariffs, tax/subsidy)", FindingClass.B,
    "PRIME MINISTER DECREE No. 928 of 2026, dated 29-Mar-2026: the selling price of natural gas "
    "supplied to the NITROGEN FERTILIZER industry is set per the applicable pricing formula "
    "WITH A MINIMUM CAP OF USD 8.50 PER MMBTU",
    "ABUK H1-2026 interim financial statements, note 48 'Significant events' item 2 "
    "(the company's own filing, not relayed)",
    CO, "2026-08-13", url=UP + "/2026/08/Financial-statements-30-6-2026.pdf",
    model_impact="BASE CHANGER on the cost side, and the largest single forward variable. "
                 "USD 8.50/mmBtu is far above the USD 5.50 the sector paid from Sep-2025 and "
                 "above the USD 6.50 general-industry floor reported in the press — i.e. the "
                 "press figure is NOT the figure that binds this issuer. Sets the floor under the "
                 "gas-feedstock driver (F30), which is ~90-97% of materials and supplies. Partly "
                 "damped, NOT offset, by the formula link in F30.")

f_duty_on = R.add(
    Ring.COUNTRY, "regulatory environment (regulator, caps, tariffs, tax/subsidy)", FindingClass.B,
    "Export duty imposed and then re-based: Ministerial Decision 190 of 2026 (4-May-2026) levied "
    "USD 90/ton on all nitrogenous fertilizer exports for three months; Decision 258 of 2026 "
    "(23-Jun-2026) replaced it with 10% of FOB value on all fertilizers and repealed 190 and 203",
    "ABUK H1-2026 interim financial statements, note 48 items 3 and 4",
    CO, "2026-08-13", url=UP + "/2026/08/Financial-statements-30-6-2026.pdf",
    model_impact="Prices the export-duty cost inside the study year: a duty was actually in force "
                 "from early May to end-July 2026 on ~81% of sales. It lands in selling and "
                 "marketing expenses, which the H1-2026 release attributes to 'increased export "
                 "duties and packing expenses'. Modelled as a DATED WINDOW, not a permanent rate.")

f_duty_off = R.add(
    Ring.COUNTRY, "regulatory environment (regulator, caps, tariffs, tax/subsidy)", FindingClass.B,
    "AND THEN CANCELLED. Ministerial Decision No. 340 of 2026, dated 25-Jun-2026, CANCELS "
    "Decisions 190/2026, 203/2026 and 258/2026 — every fertilizer export duty — EFFECTIVE "
    "1 AUGUST 2026. The company states it 'is expected to have a positive impact on business "
    "results during subsequent periods'",
    "ABUK H1-2026 interim financial statements, note 48 'Significant events' item 5",
    CO, "2026-08-13", url=UP + "/2026/08/Financial-statements-30-6-2026.pdf",
    model_impact="BASE CHANGER, AND IT REVERSES THE SIGN THE PRESS WOULD HAVE GIVEN THE MODEL. "
                 "The forward export-duty rate is ZERO from 1-Aug-2026, not 10% of FOB. On ~81% "
                 "export revenue that is a first-order difference. Dual-framed in the build: the "
                 "duty is carried as a dated May-July 2026 charge and at zero thereafter, with "
                 "reinstatement priced as an explicit downside scenario rather than assumed away. "
                 "See F09 — no press or aggregator source carried this decree.")

f_neg_duty_press = R.add_negative(
    Ring.COUNTRY, "regulatory environment (regulator, caps, tariffs, tax/subsidy)",
    "searched: 'Egypt Decision 340 of 2026 cancelling export duty fertilizers effective 1 August "
    "2026'; also 'Egypt export duty nitrogen fertilizer urea 2026 imposed'. NINE press and "
    "analyst sources returned across the two queries (hydrocarbonprocessing, MEES, Global Trade "
    "Alert, Arab Finance, BC Insight/CRU, utilities-me, aawsat, Al Manassa, edgeconsultancykw) "
    "and NOT ONE carries Decision 340/2026 or the cancellation. Every one of them stops at the "
    "10% FOB duty under Decision 258/2026 and reports it as in force. THIS NEGATIVE IS THE "
    "EVIDENCE FOR THE PRIMARY-SOURCE RULE: the reversal exists only in the issuer's own filing",
    SWEEP_DATE)

f_gasfloor_press = R.add(
    Ring.COUNTRY, "regulatory environment (regulator, caps, tariffs, tax/subsidy)", FindingClass.S,
    "Sector context around the decree: gas to nitrogen fertilizer plants was raised to USD 5.50/"
    "mmBtu from USD 4.50 in Sep-2025 with an obligation to supply 55% of output locally under a "
    "triple quota; a USD 6.50/mmBtu floor for energy-intensive industry followed in May-2026; "
    "non-nitrogen fertilizer producers were set at USD 7.75",
    "EnterpriseAM Egypt 'The new rules of survival for Egypt's fertilizer industry giants'; "
    "Egypt Oil & Gas; EgyptToday",
    PRESS, "2026-05-31",
    model_impact="Gives the STEP HISTORY the USD 8.50 floor sits on top of, so the cost increase "
                 "is measured from the right base rather than from zero. Context only — the "
                 "binding number is the company's own note 48 (F06). The same source's "
                 "'estimated 15% erosion in returns for every USD 1 increase in gas costs' for "
                 "Abu Qir is an ANALYST estimate and is explicitly NOT used as a driver.")

f_fiscal = R.add(
    Ring.COUNTRY, "fiscal / political events with sector read-through", FindingClass.S,
    "The subsidy arithmetic driving the whole regulatory sequence: an EGP 40bn+ annual fertilizer "
    "subsidy bill, with production cost above EGP 11,000/t against a farmer price of EGP 4,500/t. "
    "ABUK is contractually inside it — its own revenue note states it 'supplies its share agreed "
    "upon with the Ministry of Agriculture in accordance with the decision of the Prime Minister "
    "and at the specified prices'",
    "EnterpriseAM Egypt fertilizer-sector analysis, cross-read against ABUK's own revenue note 31 "
    "(H1-2026) and note 32 (FY-Jun-2025)",
    PRESS, "2026-03-31",
    model_impact="Splits the revenue build into a REGULATED quota leg at administered prices and "
                 "a FREE leg (local free market + export) at market prices. The local/export split "
                 "is disclosed and sourced (F27); the quota-versus-free-market split inside the "
                 "local leg is NOT, and that gap is flagged on the local-price driver.")

f_tax = R.add(
    Ring.COUNTRY, "fiscal / political events with sector read-through", FindingClass.D,
    "Effective tax rate DERIVED FROM THE COMPANY'S OWN PRINTED TAX CHARGE rather than assumed at "
    "the statutory rate: 21.2% FY-Jun-2024 (3,631,829,544/17,108,562,667), 21.6% FY-Jun-2025 "
    "(2,583,771,838/11,936,535,086), 22.4% for the transitional period (1,640,800,617/"
    "7,315,901,110), 20.9% H1-2026 (2,646,377,087/12,657,896,993)",
    "ABUK audited FY-Jun-2024 and FY-Jun-2025 statements; audited transitional-period statements; "
    "reviewed H1-2026 statements — statement of profit or loss, income tax expense line",
    CO, "2026-08-13", is_fs_data=True, fiscal_period="FY2025",
    url=UP + "/2025/11/Financial-statements-for-the-year-ended-June-30-2025.pdf",
    model_impact="Tax is set from the company's own four-period effective rate (20.9-22.4%, a "
                 "tight band around the 22.5% statutory rate) rather than by statutory formula — "
                 "the construction the EGCH same-class prior recorded as its second-largest "
                 "profit error when applied blind.")


# ===========================================================================
# RING 3 — INDUSTRY
# ===========================================================================
f_egyptbal = R.add(
    Ring.INDUSTRY, "demand drivers & capacity/supply balance", FindingClass.S,
    "Egypt's urea capacity is ~7.0-7.3Mt/yr; it exported ~3.2Mt of urea in 2024 for ~USD 1.4bn "
    "and is the second-largest urea exporter in the world after Saudi Arabia. Named domestic "
    "producers: ABUK, MOPCO, EFC, Alexandria Fertilizers (Alexfert), Helwan Fertilizers, KIMA "
    "(EGCH) and NCIC",
    "Arab Fertilizer Association member register; Forbes Middle East Egypt listings; "
    "Egypt Oil & Gas sector coverage",
    PRESS, "2026-01-01",
    model_impact="Frames ABUK's share of a gas-rationed national capacity pool and identifies the "
                 "peer set for the relative lens. Because gas is allocated nationally, competitor "
                 "utilisation and ABUK's own move TOGETHER in a curtailment — so the peer set is "
                 "not an independent cross-check on the volume driver, and is not used as one.")

f_pricevol = R.add(
    Ring.INDUSTRY, "pricing", FindingClass.D,
    "THE VOLUME/PRICE SPLIT, GIVEN BY THE COMPANY ITSELF for H1-2026: sales VOLUMES +12% and "
    "sales VALUE +87% year on year; export VOLUMES +31% and export VALUE +97%. Production "
    "exceeded plan by 23% and rose 17% on the prior period. Realised price per tonne therefore "
    "rose ~67% (1.87/1.12-1) at company level",
    "ABUK 'Unaudited Financial Indicators for the Financial Period Ended June 30, 2026' "
    "(EGX Financial Indicators filing), section SECOND, items 2-5; and the 13-Aug-2026 "
    "earnings release",
    IR, "2026-08-20", fiscal_period="H1-2026", url=UP + "/2026/08/h1-2026.pdf",
    model_impact="DRIVER UNLOCK. Converts revenue from a single growth rate into a VOLUME x "
                 "PRICE build at company level, with both legs projected separately as the "
                 "protocol requires. It also fixes the character of the H1-2026 beat: seven "
                 "eighths of the +87% sales-value rise is PRICE, not volume — so the reversal in "
                 "F02 hits almost all of it. Level gap flagged: this split is company-total, not "
                 "per product (see F45).")

f_mopco = R.add(
    Ring.INDUSTRY, "new entrants (named-competitor level)", FindingClass.S,
    "MOPCO — the largest nitrogen fertilizer plant in Egypt at ~2.0Mt/yr of urea — announced in "
    "Nov-2025 an investment of up to USD 250m to raise capacity ~10% to 2.2Mt/yr, with "
    "USD 200-250m to be spent across 2026/2027 on capacity and export-market expansion",
    "Egypt Oil & Gas, 'MOPCO to Invest up to $250mn in Capacity Expansion, Export Growth'; "
    "Forbes Middle East Egypt's 50 Most Valuable Companies 2026",
    PRESS, "2025-11-01",
    model_impact="The named domestic capacity addition inside the forecast window, and the "
                 "competitor for the same rationed gas. It caps the terminal margin and is the "
                 "mechanism behind the bear case on realised price. ~0.2Mt is ~3% of national "
                 "capacity — material to price, not to ABUK's own volume, and is carried on the "
                 "price leg only.")

f_cbam = R.add(
    Ring.INDUSTRY, "technology substitution", FindingClass.S,
    "CBAM is the live substitution threat, and it is a COST-OF-ACCESS threat rather than a "
    "product one. The EU's definitive phase begins in 2026 on ~15Mt of nitrogen fertilizer "
    "imports. Egypt sends ~46% of its fertilizer exports to the EU and supplies ~one third of EU "
    "nitrogen imports, at a CBAM default embedded-emissions factor of 1.404 tCO2 per tonne of "
    "urea — estimated to raise EU urea prices 10-15%. Blue ammonia is not expected at cost parity "
    "before ~2030 and green ammonia later still, so no physical substitute displaces urea inside "
    "the forecast window",
    "Argus Media 'European urea market braces for CBAM impact in 2026'; Rabobank; Sandbag; "
    "Fertilizers Europe — cross-read against ABUK's own FY2025 release, which names CBAM as the "
    "reason for its hydrogen and emissions programme",
    PRESS, "2026-02-10",
    model_impact="Sets a widening wedge between ABUK's FOB realised price and the EU delivered "
                 "price across the explicit window, and gives the emissions capex (F35) a return. "
                 "Carried on the export realised-price driver as a headwind with an explicit "
                 "start date, not as a demand-destruction assumption — the EU cannot replace the "
                 "import volume.")

f_assoc_peers = R.add(
    Ring.INDUSTRY, "competitor capacity / price moves (named)", FindingClass.D,
    "ABUK's named competitors are partly its own associates, disclosed in its filings: Alexandria "
    "Fertilizers Company 15%, Helwan Fertilizers Company 17%, El Wady for Phosphate Industries "
    "and Fertilizers (WAPHCO), plus Abu Tartour for Phosphoric Acid at 9.5% and Global Company "
    "for Methanol and its Derivatives at 35% (in liquidation). Carrying value of investments at "
    "the equity method EGP 5,250,041,007 at 31-Dec-2025 (EGP 4,716,865,129 restated at "
    "30-Jun-2025); share of associate profit EGP 942,853,070 in H1-2026 against EGP 625,981,291 "
    "in H1-2025",
    "ABUK audited transitional-period statements note 9 and FY-Jun-2025 statements note 9/10; "
    "reviewed H1-2026 statements, statement of profit or loss and note 41",
    CO, "2026-08-13", is_fs_data=True, fiscal_period="FY2025",
    url=UP + "/2026/03/Abu-Qir-FS-as-of-31-12-2025-English-version.pdf",
    model_impact="Makes associate income a SEPARATE, SOURCED EARNINGS LEG rather than a residual: "
                 "it is 7.4% of H1-2026 pre-tax profit and it moves with the same urea price and "
                 "the same gas rationing as the parent. Modelled on the same commodity path as the "
                 "operating legs so the two cannot silently diverge, and excluded from FCFF, "
                 "entering through the equity bridge with the dividends actually received "
                 "(EGP 1,114,082,000 in H1-2026, per the cash-flow statement).")


# ===========================================================================
# RING 4 — COMPANY
# ===========================================================================
# ---- official financial statements: four fiscal years, all to 30 June -----
f_fy2022 = R.add(
    Ring.COMPANY, "official financial statements", FindingClass.D,
    "FY ended 30-Jun-2022, from the IFRS transition/restatement note in the audited FY-Jun-2024 "
    "filing: total assets as previously issued EGP 22,372,473,861, restated EGP 22,019,544,491; "
    "total equity 17,806,394,611 restated to 16,357,091,104; profit for the year EGP 9,054,139,328",
    "ABUK audited financial statements for the year ended 30 June 2024, reclassification and "
    "restatement note (opening balance sheet at 1 July 2022)",
    CO, "2024-08-29", is_fs_data=True, fiscal_period="FY2022",
    url=UP + "/2025/11/Financial-statements-for-the-year-ended-June-30-2024.pdf",
    model_impact="Fourth fiscal year of history, so the normalisation base rests on four years "
                 "rather than the two-year floor. STATED FOR WHAT IT IS: a transition-note "
                 "balance sheet plus the profit line, NOT a full FY2022 income statement — the "
                 "FY-Jun-2023 statements are not published on the company's shelf. Restated "
                 "non-current 6,212,835,484 + current 15,806,709,007 = 22,019,544,491, foots.")

f_fy2023 = R.add(
    Ring.COMPANY, "official financial statements", FindingClass.D,
    "FY ended 30-Jun-2023 (12 months): operating revenue EGP 21,657,256,289, gross profit "
    "12,615,836,725 (58.3%), profit before tax 17,868,068,727, net profit 14,020,468,795. "
    "Balance sheet at 30-Jun-2023: total assets 34,715,086,686, total equity 26,979,902,760",
    "ABUK audited financial statements for the year ended 30 June 2024 (comparative column) and "
    "for the year ended 30 June 2025 (third balance-sheet column)",
    CO, "2024-08-29", is_fs_data=True, fiscal_period="FY2023",
    url=UP + "/2025/11/Financial-statements-for-the-year-ended-June-30-2024.pdf",
    model_impact="The high-margin reference year (58.3% gross). Establishes that the 55.1% gross "
                 "margin printed in H1-2026 is NOT unprecedented for this issuer, which is what "
                 "stops the forecast from mean-reverting it to a mid-40s 'normal' that the "
                 "company's own history does not support.")

f_fy2024 = R.add(
    Ring.COMPANY, "official financial statements", FindingClass.D,
    "FY ended 30-Jun-2024 (12 months): operating revenue EGP 18,527,811,974, cost of goods sold "
    "10,192,200,227, gross profit 8,335,611,747 (45.0%), operating profit 6,435,990,136, net "
    "financing income 9,189,315,539 (of which FX gains 6,748,866,655), profit before tax "
    "17,108,562,667, net profit 13,478,405,404 as filed. Total assets 42,329,153,379, total "
    "equity 33,136,730,289 as filed",
    "ABUK audited financial statements for the year ended 30 June 2024 (KPMG Hazem Hassan)",
    CO, "2024-08-29", is_fs_data=True, fiscal_period="FY2024",
    url=UP + "/2025/11/Financial-statements-for-the-year-ended-June-30-2024.pdf",
    detail="ROUTE: text layer, arithmetic-confirmed. Gross profit and net profit foot exactly; "
           "operating profit and net financing income are out by 1 EGP each and profit before tax "
           "by 2 EGP — the filing's own rounding, since the lines either side of them foot to the "
           "pound. Restated to 13,476,733,123 in the FY-Jun-2025 comparative, a EGP 1,672,281 "
           "difference that is separate from the far larger restatement in F23.",
    model_impact="The base year for the normalisation lens, and the year that shows why net "
                 "profit is the wrong anchor here: EGP 6.75bn of the EGP 13.48bn is a "
                 "non-recurring FX gain. The build is anchored on operating profit and the "
                 "FX result modelled separately off the disclosed net currency position (F38).")

f_fy2025 = R.add(
    Ring.COMPANY, "official financial statements", FindingClass.D,
    "FY ended 30-Jun-2025 (12 months): operating revenue EGP 22,915,657,021, cost of goods sold "
    "12,470,407,550, gross profit 10,445,249,471 (45.6%), operating profit 8,162,886,025, share "
    "dividends 1,091,097,833, net financing income 2,675,995,524, profit before tax "
    "11,936,535,086, net profit 9,352,763,248, EPS EGP 6.32. Total assets 42,219,047,998, "
    "total equity 32,135,051,656 AS FILED",
    "ABUK audited financial statements for the year ended 30 June 2025 (KPMG Hazem Hassan)",
    CO, "2025-08-31", is_fs_data=True, fiscal_period="FY2025",
    url=UP + "/2025/11/Financial-statements-for-the-year-ended-June-30-2025.pdf",
    detail="ROUTE: MIXED, AND THIS IS THE DOCUMENT THAT PROVES THE ROUTE MATTERS. The profit-or-"
           "loss page (p6) and every note used carry a clean text layer and foot exactly. The "
           "STATEMENT OF FINANCIAL POSITION (p5) is a scanned image with an embedded third-party "
           "OCR layer inside the same PDF — its header extracts as 'lrant(al/tm nf finonclnl'. "
           "It was re-rendered at 300dpi and re-read with tesseract; MY OCR AND THE EMBEDDED "
           "LAYER AGREE ON EVERY FIGURE. Non-current assets compute to 15,817,099,619 against a "
           "printed 15,817,099,620 and total equity to 32,135,051,655 against 32,135,051,656, "
           "while total assets and total equity-and-liabilities both foot exactly at "
           "42,219,047,998 and agree with each other — the filing's own rounding, recorded not "
           "repaired.",
    model_impact="Last complete 12-month year on the old basis and the immediate comparator for "
                 "the transitional period. Its BALANCE SHEET IS SUPERSEDED — see F23; its income "
                 "statement is not.")

f_tp = R.add(
    Ring.COMPANY, "one-off base-resetting transactions", FindingClass.B,
    "THE TRANSITIONAL PERIOD IS SIX MONTHS AND THE IR PAGE CALLS IT A YEAR. Audited period "
    "1-Jul-2025 to 31-Dec-2025: operating revenue EGP 13,131,643,463, cost of sales 6,332,226,987, "
    "gross profit 6,799,416,476 (51.8%), operating profit 6,029,350,789, profit before tax "
    "7,315,901,110, net profit 5,675,100,493, EPS EGP 3.69. Comparative 'six months to "
    "31-Dec-2024' revenue EGP 10,249,128,331. Balance sheet at 31-Dec-2025: total assets "
    "32,605,178,370, total liabilities 9,363,338,069, total equity 23,241,840,301",
    "ABUK audited financial statements for the transitional financial period ended 31 December "
    "2025 (KPMG Hazem Hassan opinion, printed page 4)",
    CO, "2026-03-01", is_fs_data=True, fiscal_period="TP-Jul-Dec-2025",
    url=UP + "/2026/03/Abu-Qir-FS-as-of-31-12-2025-English-version.pdf",
    detail="ROUTE: OCR off rendered pixels ONLY — this filing carries 0 characters of text layer "
           "across 50 pages. Read at 300dpi, tesseract 5.3.4, --psm 6 --oem 1. ARITHMETIC PROVES "
           "THE PERIOD LENGTH THREE WAYS ACROSS THREE SEPARATE FILINGS: the FY-Jun-2025 revenue "
           "of 22,915,657,021 less the H1-2026 filing's comparative six months to 30-Jun-2025 of "
           "12,666,528,690 equals 10,249,128,331 — EXACTLY the comparative printed in this "
           "filing. The filing's own words are 'for the six months from July 1 till December 31, "
           "2025'; the IR page files it under 'Q4 (Year ended December 31, 2025)'; the company's "
           "own governance report for the same period calls it 'the Transitional Financial "
           "Period'. Balance sheet: non-current assets compute to 8,716,933,927 against a printed "
           "8,716,933,928 and total assets to 32,605,178,368 against 32,605,178,370, while total "
           "equity, total liabilities and total equity-and-liabilities all foot to the pound.",
    model_impact="BASE CHANGER, and the trap the whole build turns on. Taking the IR label at "
                 "face value books EGP 13.13bn as a full year when it is half of one, overstating "
                 "the base by ~2x and compounding it through every forecast year and the "
                 "terminal. It is carried as a SIX-MONTH stub: no year-on-year rate spans the "
                 "change without being restated to a common length, and the inflation mapping is "
                 "split — fiscal_june governs the years to June, calendar the periods from "
                 "January 2026, and this half belongs to neither [R-MACRO-01 AMENDED]. Anything "
                 "annualised from it is labelled as annualised [R-GAP-01].")

f_restate = R.add(
    Ring.COMPANY, "one-off base-resetting transactions", FindingClass.B,
    "THE INVESTMENT-ACCOUNTING RESTATEMENT, which removes EGP 7.95bn of assets and EGP 5.25bn of "
    "equity. Equity investments moved from fair value through OCI to the EQUITY METHOD. At "
    "30-Jun-2025: total assets restated to EGP 34,264,303,968 from 42,219,047,998 as filed "
    "(-7,954,744,030); total equity to 26,885,346,553 from 32,135,051,656 (-5,249,705,103, "
    "EGP 4.16 per share); revaluation reserve to 3,619,515,858 from 9,188,096,139; deferred tax "
    "liabilities to 235,825,004 from 2,940,863,932. The investments line falls to 4,716,865,129 "
    "from 12,671,609,159 — a delta of EXACTLY -7,954,744,030, equal to the whole change in total "
    "assets. Separately, the Q1-2026 statement of changes in equity books 'Adjustments of "
    "Previous Years' of EGP -8,742,786,175 against 1-Jan-2025 equity, cutting it from "
    "27,607,944,895 to 18,865,158,720",
    "ABUK audited transitional-period statements (restated 30-Jun-2025 and 1-Jul-2024 columns) "
    "and reviewed Q1-2026 interim statement of changes in equity",
    CO, "2026-04-01", is_fs_data=True, fiscal_period="FY2025",
    url=UP + "/2026/04/Abu-Qir-english-Q1-2026.pdf",
    detail="The arithmetic identity between the investments delta and the total-assets delta is "
           "the proof that the restatement is entirely the investment-accounting change and not a "
           "bundle of unrelated adjustments. UNRESOLVED AND FLAGGED RATHER THAN SMOOTHED: the "
           "transitional filing's restated 1-Jul-2024 equity of EGP 28,698,066,473 cannot be "
           "reconciled with the Q1-2026 filing's restated 1-Jan-2025 equity of EGP 18,865,158,720 "
           "across a half-year in which the company earned EGP 5,025,798,914 — the two filings "
           "appear to carry different restatement vintages. This is named as an open item for the "
           "build, not resolved by choosing one.",
    model_impact="BASE CHANGER on every book-value, NAV and equity-anchored lens. Any valuation "
                 "built on the FY-Jun-2025 balance sheet as filed carries EGP 5.25bn (EGP 4.16 a "
                 "share) of equity that the company has since removed. It also re-cuts the income "
                 "statement: 'share dividends' of EGP 1,091,097,833 in FY-Jun-2025 gives way to "
                 "'share of profit of equity accounted investees' of EGP 942,853,070 in H1-2026, "
                 "so the two presentations must never be chained.")

f_q1 = R.add(
    Ring.COMPANY, "regular disclosures", FindingClass.D,
    "Q1-2026 (three months 1-Jan to 31-Mar-2026, reviewed): operating revenue EGP 9,533,426,763, "
    "cost of sales 4,350,675,507, gross profit 5,182,751,256 (54.4%), operating profit "
    "4,423,493,484, FX GAIN +1,751,623,887, share of associates 482,573,229, profit before tax "
    "7,200,896,394, net profit 5,633,180,116, EPS EGP 3.81",
    "ABUK reviewed interim individual financial statements for the period ended 31 March 2026",
    CO, "2026-04-01", is_fs_data=True, fiscal_period="Q1-2026",
    url=UP + "/2026/04/Abu-Qir-english-Q1-2026.pdf",
    detail="ROUTE: mixed — the Q1 filing is largely scanned (0 characters on 47 of 49 pages) but "
           "the profit-or-loss page and the changes-in-equity page carry text layers. CROSS-FOOTS "
           "AGAINST A SECOND FILING: subtracting the H1-2026 filing's standalone three months to "
           "30-Jun-2026 from its six-month column reproduces every Q1 line to within 1 EGP "
           "(revenue 9,533,426,763 exactly; gross profit 5,182,751,257 vs a printed 5,182,751,256).",
    model_impact="First quarter of the study year, swept in before the build. Its 54.4% gross "
                 "margin is 8.8pp above the FY-Jun-2025 full-year 45.6% — the exact shape of the "
                 "ARCC failure, and it is on the record here before any margin path is set.")

f_q2 = R.add(
    Ring.COMPANY, "regular disclosures", FindingClass.D,
    "Q2-2026 (three months 1-Apr to 30-Jun-2026, reviewed, printed as its own column): operating "
    "revenue EGP 13,991,130,366, cost of sales 6,202,317,283, gross profit 7,788,813,083 (55.7%), "
    "operating profit 6,299,852,629, FX LOSS -1,739,552,603, profit before tax 5,457,000,598, "
    "net profit 4,378,339,788, EPS EGP 2.95",
    "ABUK reviewed interim individual financial statements for the period ended 30 June 2026",
    CO, "2026-08-13", is_fs_data=True, fiscal_period="Q2-2026",
    url=UP + "/2026/08/Financial-statements-30-6-2026.pdf",
    model_impact="Second quarter of the study year, swept in before the build. TWO THINGS THE "
                 "HALF-YEAR NUMBER HIDES: the gross margin is still rising quarter on quarter "
                 "(54.4% -> 55.7%) while the urea price was collapsing, and net profit FELL "
                 "quarter on quarter (5.63bn -> 4.38bn) purely on a EGP 3.49bn swing in the FX "
                 "line. The operating and financing legs are therefore forecast separately, never "
                 "on a net-profit growth rate.")

f_h1 = R.add(
    Ring.COMPANY, "regular disclosures", FindingClass.D,
    "H1-2026 (six months to 30-Jun-2026, reviewed): operating revenue EGP 23,524,557,129 (+85.7% "
    "on the restated EGP 12,666,528,690), cost of sales 10,552,992,790, gross profit "
    "12,971,564,340 (55.1% against 48.0%), operating profit 10,723,346,113 (+126.7%), net "
    "financing income 991,697,810, share of associates 942,853,070, profit before tax "
    "12,657,896,993, tax 2,646,377,087, net profit 10,011,519,905 (+119.1%), EPS EGP 6.76",
    "ABUK reviewed interim individual financial statements for the period ended 30 June 2026",
    CO, "2026-08-13", is_fs_data=True, fiscal_period="H1-2026",
    url=UP + "/2026/08/Financial-statements-30-6-2026.pdf",
    detail="ROUTE: text layer, arithmetic-confirmed — every line foots to within 1 EGP and gross "
           "profit, profit before tax and net profit foot exactly.",
    model_impact="SIX MONTHS OF 2026 ALREADY EXCEED THE WHOLE 12-MONTH FY-Jun-2025 REVENUE OF "
                 "EGP 22.92bn. This is the anchor period for the study year and the reason the "
                 "forecast cannot start from a full-year 2025 figure of any kind.")

f_products = R.add(
    Ring.COMPANY, "official financial statements", FindingClass.D,
    "PRODUCT-LEVEL REVENUE, disclosed every period and footing exactly. H1-2026 (EGP m): "
    "granulated urea 9,554, urea 8,779, ammonium nitrate 3,394, ammonia 913, liquid fertilizer "
    "693, sales revenue 23,333. FY-Jun-2025: 9,506 / 7,948 / 4,856 / 279 / 0, sales revenue "
    "22,592. FY-Jun-2024: 7,658 / 6,080 / 4,011 / 576 / 0, sales revenue 18,326. Transitional "
    "6M to Dec-2025: 4,259 / 4,713 / 2,948 / 335 / 694, sales revenue 12,950. Six months to "
    "Dec-2024: 3,630 / 3,433 / 2,768 / 262 / 0, sales revenue 10,095. Local/export split given "
    "for every period",
    "ABUK financial statements, revenue note — note 32 (FY-Jun-2024, FY-Jun-2025, transitional "
    "period) and note 31 (H1-2026)",
    CO, "2026-08-13", is_fs_data=True, fiscal_period="H1-2026",
    url=UP + "/2026/08/Financial-statements-30-6-2026.pdf",
    detail="Every product column foots to its printed sales-revenue subtotal to within 1 EGP "
           "across all five periods, and local+export reconciles to sales revenue exactly in "
           "every one. Two routes: text layer for FY-Jun-2024/25 and H1-2026, 200dpi OCR for the "
           "transitional filing (its note 32 is on printed page 38). ONE PRINTING INCONSISTENCY "
           "RECORDED: 'sale of casual products' is printed as 83,181,553 in H1-2026 note 31 and "
           "83,181,533 in note 32 — 20 EGP apart, immaterial and not repaired.",
    model_impact="DRIVER UNLOCK, and the finest sourced revenue level. Revenue is built per "
                 "product line rather than as one top-line growth rate. It also exposes what a "
                 "blended build would hide: ammonium nitrate revenue FELL 30% from the six months "
                 "to Dec-2025 to H1-2026 while granulated urea rose 124% — opposite directions in "
                 "the same company in the same half.")

f_liquid = R.add(
    Ring.COMPANY, "one-off base-resetting transactions", FindingClass.B,
    "THE LIQUID FERTILIZER (UAN) PLANT RESTARTED AND IS A NEW REVENUE LINE. It contributed "
    "EGP 0 through FY-Jun-2025, then EGP 694,007,097 in the transitional half and "
    "EGP 693,084,000 in H1-2026 — ALL of the latter in the three months to 30-Jun-2026, and "
    "nothing in Q1-2026. Its H1-2026 gross margin is 74.5%, the highest of any segment. The "
    "FY-Jun-2025 audited statements had explicitly stated that 'the non-utilization of the "
    "production capacity of the liquid fertilizer plant during the year is due to demand and "
    "operating conditions'",
    "ABUK audited FY-Jun-2025 statements, fixed-assets note; audited transitional-period "
    "statements note 32; reviewed H1-2026 statements notes 31 and 47",
    CO, "2026-08-13", is_fs_data=True, fiscal_period="H1-2026",
    url=UP + "/2026/08/Financial-statements-30-6-2026.pdf",
    model_impact="BASE CHANGER, modelled as an explicit dated restart and dual-framed, never "
                 "folded into a growth rate on total revenue. Its contribution is LUMPY BY THE "
                 "COMPANY'S OWN NUMBERS — two quarters of roughly EGP 693-694m separated by a "
                 "quarter of zero — so it is carried at a utilisation the disclosure supports "
                 "with the zero-quarter case priced, not annualised from the Q2 print.")

f_segments = R.add(
    Ring.COMPANY, "official financial statements", FindingClass.D,
    "PLANT-LEVEL SEGMENT PROFIT AND LOSS — revenue, cost of sales, gross profit, opex, tax and "
    "net profit for each of Abu Qir Plant (1), Plant (2), Plant (3), Ammonia, Liquid fertilizer "
    "and Plastic Bags. H1-2026 gross margin by plant: Plant 1 61.6%, Plant 2 7.6%, Plant 3 65.7%, "
    "Ammonia 47.9%, Liquid fertilizer 74.5%. FY-Jun-2024 by plant: Plant 1 49.3%, Plant 2 22.3%, "
    "Plant 3 53.7%, Ammonia 41.4%",
    "ABUK audited FY-Jun-2024 statements note 'Operating segments — net profit for the period' "
    "and reviewed H1-2026 statements note 47",
    CO, "2026-08-13", is_fs_data=True, fiscal_period="H1-2026",
    url=UP + "/2026/08/Financial-statements-30-6-2026.pdf",
    detail="Both segment tables foot to the printed consolidated totals: FY-Jun-2024 revenue, "
           "cost of sales and gross profit all reconcile exactly; H1-2026 revenue and cost of "
           "sales foot exactly and gross profit, operating profit and net profit are each out by "
           "1 EGP. Segment-to-product mapping is confirmed by exact equality of the printed "
           "figures: Plant 2 revenue equals ammonium nitrate sales and Plant 3 equals granulated "
           "urea sales in every period.",
    model_impact="THIS IS WHY MARGIN IS AN OUTPUT AND NOT AN INPUT HERE [L-005]. Cost is built "
                 "per plant against revenue per plant and the margin falls out. A single blended "
                 "company gross margin would erase the finding that matters most: Plant 2's "
                 "margin COLLAPSED from 22.3% to 7.6% while the two urea plants expanded to "
                 "61.6% and 65.7% — a mix effect that a company-level margin glide would score as "
                 "an unexplained improvement.")

f_gas = R.add(
    Ring.COMPANY, "official financial statements", FindingClass.D,
    "THE GAS BILL IS SEPARATELY DISCLOSED, AND SO IS ITS PRICE FORMULA. Natural gas purchased "
    "from Egyptian Natural Gas Company (GASCO): EGP 7,576,946,457 in FY-Jun-2024, "
    "EGP 9,768,565,881 in FY-Jun-2025, EGP 9,084,428,000 in the six months to 30-Jun-2026 "
    "(comparative column headed 31-Dec-2025: EGP 5,450,025,058). That is 90.0%, 91.0% and 97.3% "
    "of the 'materials and supplies' cost line. The company states the contract price 'was "
    "determined according to a price formula that takes into consideration the selling prices of "
    "the Ministry of Agriculture and export prices according to the average price of "
    "international bulletins and the average selling price of the USD against EGP at the central "
    "bank of Egypt'",
    "ABUK financial statements, related-party note — significant contracts with related parties "
    "(note 25-4 in H1-2026; equivalent notes in FY-Jun-2024 and FY-Jun-2025)",
    CO, "2026-08-13", is_fs_data=True, fiscal_period="H1-2026",
    url=UP + "/2026/08/Financial-statements-30-6-2026.pdf",
    detail="AMBIGUITY RECORDED RATHER THAN ASSIGNED: in the H1-2026 note the comparative column "
           "is headed 31/12/2025, so the EGP 5,450,025,058 could be either the transitional half "
           "(Jul-Dec 2025) or the comparative half (Jan-Jun 2025). Both readings give a plausible "
           "ratio to the matching cost line, so the figure is carried with its printed heading and "
           "the two clean 12-month observations (FY-Jun-2024 and FY-Jun-2025) carry the trend.",
    model_impact="THE LARGEST DRIVER UNLOCK IN THIS SWEEP. The single biggest cost is a named, "
                 "separately quantified purchase from a named counterparty, so it is built "
                 "bottom-up instead of escalated with a blended index [L-009]. The formula is the "
                 "decisive fact: gas cost is CONTRACTUALLY LINKED to international urea export "
                 "prices and to USD/EGP, so it moves WITH the revenue it funds. A fixed USD/mmBtu "
                 "assumption would misstate both the level and the volatility, and the USD 8.50 "
                 "floor (F06) binds only when the formula output falls below it — which is "
                 "precisely what a post-spike urea price makes likely.")

f_costnature = R.add(
    Ring.COMPANY, "official financial statements", FindingClass.D,
    "COST OF SALES BY NATURE, every period. H1-2026: materials and supplies EGP 9,339,082,380, "
    "salaries and wages 1,046,936,849, depreciation 94,527,659, employee benefits 28,546,633, "
    "other operating cost 127,080,802, less by-products 83,181,533 = 10,552,992,790. FY-Jun-2025: "
    "10,733,542,631 / 1,187,150,630 / 106,569,731 / 37,192,576 / 431,646,819 less 25,694,837 = "
    "12,470,407,550. Materials and supplies fell to 39.7% of revenue in H1-2026 from 45.7% in "
    "H1-2025 and 46.8% in FY-Jun-2025",
    "ABUK financial statements, cost of sales note — note 33 (FY-Jun-2024, FY-Jun-2025) and "
    "note 32 (H1-2026)",
    CO, "2026-08-13", is_fs_data=True, fiscal_period="H1-2026",
    url=UP + "/2026/08/Financial-statements-30-6-2026.pdf",
    detail="Every cost note foots to its printed total EXACTLY in every period tested — unlike "
           "the EGCH same-class prior, where the cost-by-nature notes missed by 247k, 36.3m and "
           "63k EGP and were therefore not usable as a source. These foot, so they are.",
    model_impact="Gives one escalator per cost driver instead of one blended rate across all of "
                 "them [L-009]: gas on the disclosed formula, salaries on wage inflation, "
                 "depreciation off the fixed-asset roll-forward. The fall in materials-to-revenue "
                 "is what generated the H1-2026 margin, and the build must show whether it came "
                 "from price (urea up faster than the gas formula passed through) or from "
                 "efficiency — the two have opposite forward implications.")

f_ir_release = R.add(
    Ring.COMPANY, "IR communications (calls, presentations, releases)", FindingClass.D,
    "H1-2026 earnings release, 13-Aug-2026 — the operating anchors no financial statement "
    "carries. EBITDA EGP 10.84bn at a 46.1% margin (+126% y/y). Sales volumes +12%, sales value "
    "+87%; export volumes +31%, export value +97%. Production beat plan by 23%. Export markets "
    "diversified to 18 COUNTRIES and 73 EXPORT CUSTOMERS, with 40 local free-market customers. "
    "The Ammonia Converter Revamp at Plant (1) and the ammonia transfer-line replacement are "
    "COMPLETE, adding ~200 t/day of ammonia and ~210 t/day of urea capacity while cutting gas "
    "consumption. A long-term strategic plan with McKinsey & Company is nearing completion. New "
    "export markets named: Latin America, Australia, Africa",
    "ABUK Earnings Release for the financial period 01/01/2026 - 30/06/2026",
    IR, "2026-08-13", fiscal_period="H1-2026",
    url=UP + "/2026/08/Earnings-release-30-6-2026.pdf",
    detail="ROUTE: OCR off rendered pixels (0 text layer across 9 pages), 200dpi with the "
           "balance-sheet paragraph re-read at 400dpi. MANDATORY IR SOURCE, tagged distinctly "
           "from COMPANY_OFFICIAL so a reviewer can see how much of the Company ring rests on "
           "the IR channel specifically.",
    model_impact="Supplies EBITDA (never printed in the statements), the volume/price split "
                 "(F14), and the capacity uplift that sets the forward volume ceiling: +200 t/d "
                 "ammonia and +210 t/d urea is a SOURCED, COMPLETED debottleneck, so the volume "
                 "driver rises on disclosure rather than on assumption. Customer counts fix "
                 "concentration risk on the export leg.")

f_ir_kpi = R.add(
    Ring.COMPANY, "IR communications (calls, presentations, releases)", FindingClass.B,
    "H1-2026 'Unaudited Financial Indicators' EGX filing — AND THE COMPANY'S OWN WARNING ABOUT "
    "ITS OWN RESULT. It states the record H1 was delivered 'before the full financial impact of "
    "the recent regulatory policies (the revision of the floor of the natural gas pricing formula "
    "and the imposition of export duties on nitrogen fertilizer exports) was reflected across the "
    "entire reporting period' and that the impact 'is expected to be fully reflected in the "
    "upcoming financial periods'. Also filed: shareholders' equity EGP 29,462,212,810 at "
    "30-Jun-2026 against EGP 23,241,840,301 at 31-Dec-2025; net working capital 18,759,648,883; "
    "retained earnings 16,858,594,774",
    "ABUK Unaudited Financial Indicators for the Financial Period Ended June 30, 2026, "
    "sections FIRST (A)-(C) and SECOND",
    IR, "2026-08-20", fiscal_period="H1-2026", url=UP + "/2026/08/h1-2026.pdf",
    detail="ROUTE: OCR off rendered pixels, 200dpi with the cash-flow block re-read at 400dpi. "
           "TWO DISAGREEMENTS BETWEEN THE COMPANY'S OWN DOCUMENTS, RECORDED NOT RESOLVED. (i) "
           "This filing reports H1-2026 investing cash flow of EGP -4,541,370,372 while the "
           "reviewed cash-flow statement prints EGP -575,805,350, a gap of EGP 3.97bn; the "
           "operating figures differ by exactly the finance-cost-paid line (4,503,078 and "
           "2,719,225) and financing matches to the pound, so the classification differs rather "
           "than the underlying. The -363% change this filing prints is internally consistent "
           "with ITS OWN numbers, so the difference is real and not an OCR artefact. (ii) Its "
           "'paid in capital' row did not resolve at either 200dpi or 400dpi; the audited "
           "statements print EGP 1,892,813,580 in every period and govern.",
    model_impact="BASE CHANGER, stated by the issuer about its own numbers: H1-2026 is explicitly "
                 "NOT a clean run-rate. Both named measures are dated in note 48 (F06, F07, F08) "
                 "and the export duty is CANCELLED from 1-Aug-2026 — so this document's own "
                 "framing is already partly superseded by the statements filed a week earlier, "
                 "and the build follows note 48. The equity figure independently confirms the "
                 "audited EGP 23,241,840,301 and is the third company source to do so.")

f_budget = R.add(
    Ring.COMPANY, "strategic plans & guidance", FindingClass.S,
    "THE COMPANY'S OWN FY2026 PLANNED BUDGET IS ALREADY OBSOLETE. Filed for the financial year "
    "2026: total revenues EGP 26,164m, total expenses EGP 17,329m, profit before taxes "
    "EGP 8,835m. H1-2026 ACTUAL revenue of EGP 23,525m is 89.9% of the full-year budget in six "
    "months, and H1-2026 actual profit before tax of EGP 12,658m is 143% of the FULL-YEAR "
    "budgeted figure",
    "ABUK 'Planned Budget Key Indicators For the Financial Year 2026 — Estimated Results' "
    "(EGX planned-budget filing)",
    IR, "2026-01-31", url=UP + "/2026/01/Budget-KPIs-For-FY-2026.pdf",
    detail="ROUTE: OCR off rendered pixels from the native embedded 200ppi JPEG, band-scanned at "
           "3x upscale. ARITHMETIC IS THE ARBITER AND IT SETTLED A DISPUTED DIGIT: the English "
           "column read 'Profit before 9936' while the Arabic-numeral column read 8835; "
           "26,164 - 17,329 = 8,835 EXACTLY, so 8,835 is the figure and 9,936 is an OCR misread.",
    model_impact="Establishes that management's own published forward number is not usable as a "
                 "driver and must NOT be anchored to — a build that took the budget as guidance "
                 "would forecast a second half of EGP 2.6bn revenue against a first half of "
                 "EGP 23.5bn. It is carried as evidence of forecast dispersion for the scenario "
                 "width, not as a central case.")

f_projects = R.add(
    Ring.COMPANY, "strategic plans & guidance", FindingClass.D,
    "The named investment programme, with stakes and costs. Abu Tartour for Phosphoric Acid — "
    "ABUK stake 9.5%, general contractor agreement signed 29-Jun-2025, project investment cost "
    "USD 643m, shareholders' loan and financing framework agreements signed; El Wadi for "
    "Phosphate Industries and Fertilizers (WAPHCO) to merge into Abu Tartour per its EGM of "
    "13-May-2025. North Abu Qir Agri-Nutrients to merge into a new special free-zone company, "
    "'Khaleej Abu Qir for Agri-Nutrients', authorised capital USD 100m, issued and paid USD 5m. "
    "Global Company for Methanol and its Derivatives (35%) in liquidation per its EGM of "
    "30-Apr-2025. Solar phase one 2.6MW for EGP 88.32m at 85% execution, phase two 2.5-3MW "
    "approved. Hydrogen substitution to lift Plant (1) ammonia capacity from 1,100 to 1,200 "
    "t/day. ABB steam optimisation, USD 500k, cutting boiler gas 2-4%",
    "ABUK Earnings Release for FY ended 30 June 2025, 'Strategy Insights', 'Abu Qir's Internal "
    "Projects' and 'Investment Projects' sections",
    IR, "2025-08-31", url=UP + "/2025/11/Earnings-Release-for-FY-ended-30-06-2025.pdf",
    model_impact="Builds the capex and associate-investment schedule from NAMED, COSTED projects "
                 "rather than as a percentage of revenue, and gives the volume driver its "
                 "disclosed uplift path (Plant 1 ammonia 1,100 -> 1,200 t/day). The USD 643m Abu "
                 "Tartour commitment is carried at ABUK's 9.5% share as a dated cash call, not as "
                 "a full-project number.")

f_gasevents = R.add(
    Ring.COMPANY, "regular disclosures", FindingClass.S,
    "Natural-gas interruption is a RECURRING, DISCLOSED event for this issuer, not a tail risk. "
    "The company's material-event shelf carries: gas supply STOPPED to all plants (disclosed "
    "25-Jun-2024, on an unprecedented heatwave plus cuts to regional supply sources); the "
    "repercussions of the Middle East war on gas supplied (15-Jun-2025); resumption and gradual "
    "start-up (29-Jun-2025); pressure fluctuations in the network; a two-week reduction in gas "
    "supplied; and a further resumption disclosure. Separately, a licence to operate the solar "
    "generation activity under self-consumption was granted by the Egyptian Electric Utility and "
    "Consumer Protection Regulatory Agency (disclosed 23-Dec-2025)",
    "ABUK material-event disclosures to EGX, investor-relations material-events page",
    CO, "2026-01-31", url=SITE + "/investor-relations/material-events/",
    model_impact="Sets the DOWNSIDE BAND on utilisation directly from the issuer's own event "
                 "history — at least three separate curtailment episodes across FY2024-FY2026. "
                 "The volume driver is banded rather than run at plate, and the summer curtailment "
                 "is treated as recurring until a year passes without one, which is exactly the "
                 "overturn condition the EGCH same-class prior recorded.")

f_utilisation = R.add(
    Ring.COMPANY, "regular disclosures", FindingClass.D,
    "The company states the CAUSE of its own under-utilisation in the audited notes: 'The "
    "non-utilization of the production capacity of the liquid fertilizer plant during the year is "
    "due to demand and operating conditions. And for the remaining company plants, due to the "
    "shortage of natural gas supplies provided to the company, the total was accordingly "
    "adjusted.' It also discloses that fully depreciated fixed assets still in operation have a "
    "historical cost of EGP 2.3bn",
    "ABUK audited financial statements for the year ended 30 June 2025, fixed-assets note (4)",
    CO, "2025-08-31", is_fs_data=True, fiscal_period="FY2025",
    url=UP + "/2025/11/Financial-statements-for-the-year-ended-June-30-2025.pdf",
    model_impact="Splits under-utilisation into its two disclosed causes — DEMAND for liquid "
                 "fertilizer and GAS SUPPLY for the ammonia/urea trains — so the volume driver "
                 "carries two independent constraints rather than one blended utilisation rate. "
                 "The EGP 2.3bn of fully depreciated but operating assets flags that reported "
                 "depreciation understates true replacement capex.")

f_fxpos = R.add(
    Ring.COMPANY, "regular disclosures", FindingClass.D,
    "THE FX POSITION IS DISCLOSED, SO THE FX LINE NEED NOT BE ASSUMED. Net foreign-currency "
    "balances of EGP 20,754,874,389 at 30-Jun-2026, equivalent to USD 422 million plus EUR 105 "
    "thousand, at the reporting-date rate of EGP 49.23 per dollar. The company's own stated "
    "sensitivity: a 10% move in foreign currencies changes equity and net profit by approximately "
    "EGP 2,075,487,438. It also states it has NO LOANS at the reporting date",
    "ABUK reviewed H1-2026 interim financial statements, financial-risk note — currency risk (A) "
    "and interest rate risk (B)",
    CO, "2026-08-13", is_fs_data=True, fiscal_period="H1-2026",
    url=UP + "/2026/08/Financial-statements-30-6-2026.pdf",
    detail="Arithmetic check: EGP 20,754,874,389 / USD 422m = EGP 49.18/USD against the disclosed "
           "49.23 reporting rate, consistent to rounding on the stated USD figure.",
    model_impact="Converts the FX result from a top-down assumption into a POSITION x RATE "
                 "calculation, which matters because the FX line swung EGP +1.75bn to -1.74bn "
                 "between Q1 and Q2 of 2026 and drove net profit down while operating profit rose. "
                 "'No loans' fixes the capital structure: the company is DEBT-FREE and net cash, "
                 "so the WACC is effectively all-equity, the cost of debt carries no weight, and "
                 "the enterprise-to-equity bridge ADDS net cash.")

f_shareholders = R.add(
    Ring.COMPANY, "ownership / stake changes (named-transaction rule)", FindingClass.D,
    "Shareholder register at 30-Jun-2026, from the company's own Article 30 disclosure: Alpha "
    "Oryx Limited 271,573,655 shares (21.52%); Saudi Egyptian Investment Company (SEIC) "
    "257,405,245 (20.40%), related party The Saudi Seventh Investment Co.; Egyptian General "
    "Petroleum Corporation (EGPC) 241,153,540 (19.11%); Holding Company for Chemical Industries "
    "92,802,709 (7.35%); Nasser Social Bank 74,477,970 (5.90%); Employees Union 65,000,000 "
    "(5.15%). Holders of 5% and above total 1,002,413,119 shares, 79.44%; free float ~20.56%",
    "ABUK Disclosure report on the composition of the board of directors and shareholders as at "
    "30 June 2026 (Article 30 of the Listing Rules)",
    CO, "2026-07-31", url=UP + "/2026/07/disclosure-report-30-6-2026.pdf",
    detail="SHARE COUNT ESTABLISHED FROM COMPANY DOCUMENTS ONLY, NEVER FROM AN AGGREGATOR, and "
           "confirmed four independent ways: back-solving the disclosed percentages gives "
           "1,261,790,417 (SEIC), 1,261,923,286 (EGPC) and 1,262,135,922 (Employees Union); "
           "issued capital EGP 1,892,813,580 at a EGP 1.50 par gives 1,261,875,720; and the "
           "audited FY-Jun-2025 dividend statement's shareholders' share of EGP 6,309,378,600 at "
           "a printed EGP 5.00 per share gives 1,261,875,720 EXACTLY. That last one is the "
           "authority. ROUTE: 200dpi OCR.",
    model_impact="Fixes the denominator of every per-share figure at 1,261,875,720 and the free "
                 "float at ~20.6%. State and quasi-state ownership approaching 80% — EGPC, the "
                 "Holding Company for Chemical Industries, Nasser Social Bank, SEIC and ADQ's "
                 "Alpha Oryx — is carried as a governance and liquidity constraint on the "
                 "multiple lens, and explains why the gas supplier (GASCO) is a related party of "
                 "the largest single state holder.")

f_alphaoryx = R.add(
    Ring.COMPANY, "ownership / stake changes (named-transaction rule)", FindingClass.C,
    "THE NAMED TRANSACTION BEHIND THE LARGEST HOLDING, searched specifically rather than "
    "estimated: Alpha Oryx Limited, a vehicle of Abu Dhabi's ADQ, acquired the 21.52% stake in "
    "Abu Qir Fertilizers for approximately USD 390m, settled on the EGX on 12-14 April 2022 as "
    "part of a USD ~1.95bn block across five listed Egyptian companies (CIB, Fawry, Alexandria "
    "Container and Cargo Handling, MOPCO and ABUK)",
    "MarketScreener transaction record; Daily News Egypt; Amwal Al Ghad — ADQ/Alpha Oryx "
    "April 2022 acquisitions",
    PRESS, "2022-04-14",
    model_impact="")

f_dividends = R.add(
    Ring.COMPANY, "management & capital actions", FindingClass.D,
    "The distribution history and the waterfall that produces it. FY-Jun-2024: EGP 7.50 per "
    "share. FY-Jun-2025: EGP 5.00 per share, paid EGP 2.00 on 23-Oct-2025 and EGP 3.00 on "
    "25-Dec-2025; shareholders' share EGP 6,309,378,600, employees' share 1,293,145,987, board "
    "remuneration 80,000,000, retained earnings carried forward 6,541,009,784. Transitional "
    "period to 31-Dec-2025: EGP 2.30 per share approved at the OGM of 28-Mar-2026, paid EGP 1.00 "
    "on 22-Apr-2026 and EGP 1.30 on 24-Jun-2026. The board was reconstituted for a new three-year "
    "term at the same OGM; Eng. Hany Sayed Mohamed Dahy is Chairman and CEO",
    "ABUK audited FY-Jun-2025 statements, (Proposed) Dividend Distribution Statement; Resolutions "
    "of the Ordinary General Assembly Meeting held 28 March 2026",
    CO, "2026-03-29", is_fs_data=True, fiscal_period="FY2025",
    url=UP + "/2026/03/ordinary.pdf",
    detail="THE EPS NUMERATOR IS SOLVED, NOT GUESSED. Net profit 9,352,763,248 less employees' "
           "share 1,293,145,987 less board remuneration 80,000,000 = 7,979,617,261; divided by "
           "1,261,875,720 shares = EGP 6.32, EXACTLY the printed EPS. The same ~85% relationship "
           "holds in every period tested (85.3% FY-Jun-2025, 82.0% transitional, 85.3% Q1-2026, "
           "85.2% H1-2026).",
    model_impact="Distributable cash flow is built through the company's OWN appropriation "
                 "waterfall — roughly 13-15% of net profit is diverted to employees and the board "
                 "BEFORE anything reaches shareholders. A dividend model applied to net profit "
                 "would overstate the shareholder claim by that margin in every year. The declining "
                 "per-share sequence (7.50 -> 5.00 -> 2.30 on a half-year) is length-adjusted "
                 "before any payout trend is inferred.")

f_release_typo = R.add(
    Ring.COMPANY, "IR communications (calls, presentations, releases)", FindingClass.S,
    "AN ERROR IN THE COMPANY'S OWN EARNINGS RELEASE, caught by arithmetic. The H1-2026 release "
    "states 'Total equity amounted EGP 29.46 billion on 30/6/2026, compared to EGP 32.24 billion "
    "on 31/12/2025'. The audited transitional-period balance sheet prints total equity of "
    "EGP 23,241,840,301 at 31-Dec-2025 — the release's figure is EGP 9bn too high and looks like "
    "a 23 -> 32 digit transposition",
    "ABUK Earnings Release for the period 01/01/2026 - 30/06/2026, statement of financial "
    "position highlights",
    IR, "2026-08-13", fiscal_period="H1-2026",
    url=UP + "/2026/08/Earnings-release-30-6-2026.pdf",
    detail="ARITHMETIC IS THE ARBITER AND THE RELEASE CONTRADICTS ITSELF. The same paragraph "
           "gives total assets of EGP 32.60bn and total liabilities of EGP 9.36bn at 31-Dec-2025; "
           "32.60 - 9.36 = 23.24, not 32.24. Three company sources agree on 23,241,840,301 — the "
           "audited transitional balance sheet, the Q1-2026 statement of changes in equity "
           "(opening balance at 1-Jan-2026), and the H1-2026 Financial Indicators filing. The "
           "release is the lone outlier. The digits were re-read at 400dpi and '32.24' IS what is "
           "printed, so this is the company's error and not the extraction's.",
    model_impact="Blocks a EGP 9bn error at the top of the equity bridge and fixes the source "
                 "hierarchy for the build: where an earnings release and an audited statement "
                 "disagree, the statement governs and the release is recorded as wrong rather "
                 "than averaged with it. Equity at 31-Dec-2025 is EGP 23,241,840,301.")

f_listing = R.add(
    Ring.COMPANY, "regular disclosures", FindingClass.D,
    "DUAL-LISTING CHECK, run explicitly. ABUK is listed on the Egyptian Exchange ONLY. The "
    "company identifies itself as 'ABUK.CA on the Egyptian Exchange' in its own earnings "
    "releases, files exclusively to EGX, reports solely in EGP, and no second listing appears on "
    "its investor-relations pages. ISIN EGS38191C010. The repository holds engine/raw_ohlc/EG/"
    "ABUK.csv and the registered regressor engine/raw_indices/EG/EGX30.csv",
    "ABUK Earnings Release FY ended 30 June 2025 ('Results in a Nutshell'); ABUK Earnings Release "
    "H1-2026; repository index registry",
    CO, "2026-08-13", url=UP + "/2025/11/Earnings-Release-for-FY-ended-30-06-2025.pdf",
    model_impact="Resolves the dual-listing trap BEFORE the beta is run: a single listing means "
                 "one legitimate regressor and no currency or magnitude ambiguity in the series. "
                 "The beta is taken through beta_regression.own_stock_beta('ABUK','EG','EGX') "
                 "against the published EGX30, never against a constituent composite [R-BETA-01].")

f_route = R.add(
    Ring.COMPANY, "official financial statements", FindingClass.C,
    "Extraction-route record for the whole shelf. Text-layer density per page: FS_FY2024_Jun "
    "1,925; FS_FY2025_Jun 2,087; FS_H1_2026 2,110; ER_FY2024_Jun 2,842; ER_FY2025_Jun 2,128 — "
    "all usable. FS_TP_Dec2025 0 across 50 pages; FS_Q1_2026 170 (image pages with two text "
    "exceptions); ER_H1_2026, ER_Q1_2026 and every KPI, budget, governance and material-event "
    "PDF at 0 — all OCR-only. Within FS_FY2025_Jun the statement of financial position alone is "
    "a scanned image carrying a third-party OCR layer",
    "Route audit over 23 documents retrieved from abuqir.net (pdfinfo / pdftotext character "
    "counts; pdftoppm + tesseract 5.3.4 for the OCR route)",
    CO, "2026-09-08",
    model_impact="")


# ---------------------------------------------------------------------------
# NEGATIVE SEARCHES — every one of these is a query that was ACTUALLY RUN on the
# sweep date, with the result recorded. None was invented to clear a check.
# ---------------------------------------------------------------------------
f_neg_volumes = R.add_negative(
    Ring.COMPANY, "regular disclosures",
    "searched: per-product physical sales and production volumes in tonnes, across the H1-2026, "
    "FY-Jun-2025 and FY-Jun-2024 earnings releases, the Financial Indicators filings and the "
    "audited statements. RESULT: NOT DISCLOSED NUMERICALLY AT PRODUCT LEVEL. Total production "
    "and sales volumes appear ONLY as bar charts captioned 'Product tons (000s)'. The FY-Jun-2024 "
    "release's chart labels are machine-readable (2,180 / 2,022 / 1,953 for production and "
    "2,180 / 2,061 / 1,953 for sales across FY2022/23, FY2023/24 and Plan) but do NOT reconcile "
    "with that release's own narrative of '+9% over plan and -5% versus FY2022/23'; the FY-Jun-"
    "2025 chart yields only 1,983 and 1,853 against a narrative of '+1% from what was planned'; "
    "the H1-2026 chart labels do not resolve at 200dpi or 400dpi beyond 890 and 907. Company-"
    "level volume GROWTH is disclosed in words (+12% sales, +31% export, +17% production) and is "
    "used; absolute per-product tonnage is not obtainable and is NOT guessed at",
    SWEEP_DATE)

f_neg_gasunit = R.add_negative(
    Ring.COMPANY, "official financial statements",
    "searched: ABUK's own gas consumption volume and its realised gas price per unit — grepped "
    "all text-bearing filings for 'mmbtu', 'million british', 'cubic met', 'gas volume', 'gas "
    "quantit', 'per mcf', 'feedstock'. RESULT: exactly ONE hit across three full filings, and it "
    "is the USD 8.50/mmBtu regulatory FLOOR in note 48, not a consumption volume or a realised "
    "price. The company discloses the total EGP paid to GASCO and the pricing FORMULA, but never "
    "its gas volume in mmBtu nor the price it actually paid per unit, so a cost-per-mmBtu build "
    "is not sourceable and the gas driver is built in EGP on the disclosed formula instead",
    SWEEP_DATE)

f_neg_guidance = R.add_negative(
    Ring.COMPANY, "strategic plans & guidance",
    "searched: forward guidance beyond the one-page FY2026 planned-budget filing — grepped the "
    "FY-Jun-2025 and H1-2026 earnings releases for 'guidance', 'outlook for 2026/27/28/29', "
    "'we expect ... to reach', 'target of EGP'. RESULT: ZERO hits. The company publishes a "
    "single-page statutory planned budget (three lines) and no multi-year guidance, no volume "
    "target, no margin target and no capex envelope. The McKinsey strategic plan is described as "
    "'nearing completion' with no numbers attached. Terminal-period assumptions therefore have no "
    "company-stated anchor and are built from the disclosed asset base",
    SWEEP_DATE)

f_neg_quota = R.add_negative(
    Ring.COUNTRY, "fiscal / political events with sector read-through",
    "searched: the split of ABUK's LOCAL revenue between the administered Ministry of Agriculture "
    "quota and the local free market, in the revenue notes of all four filings and in the "
    "earnings releases. RESULT: NOT DISCLOSED. The company confirms it supplies 'its share agreed "
    "upon with the Ministry of Agriculture ... at the specified prices' and separately reports "
    "'expanding customer base in local free market reaching to 40 customers', but never quantifies "
    "either leg. Only the LOCAL versus EXPORT split is given. The sector-wide 55% local-supply "
    "obligation reported in the press is NOT confirmed in any ABUK filing, so it is not applied "
    "as a company constraint",
    SWEEP_DATE)

f_neg_ircall = R.add_negative(
    Ring.COMPANY, "IR communications (calls, presentations, releases)",
    "searched: an earnings-CALL transcript, webcast or slide presentation, across abuqir.net's "
    "investor-relations section (all thirteen sub-pages enumerated: financial-statements, "
    "reports, material-events, planned-budget, statistics, dividends, shareholders, "
    "board-of-directors-resolutions, general-assemblies, stock-insights, company-objective, "
    "shareholders-disclosure-reports, investor-relations-contact). RESULT: NO transcript, "
    "webcast or presentation deck is published. The IR channel is written only — earnings "
    "releases, Financial Indicators filings, planned budgets and board reports — all of which "
    "WERE obtained and are carried above. Recorded so the absence of a call is a fact rather "
    "than a gap",
    SWEEP_DATE)


# ===========================================================================
# DRIVER GATE TABLE — every driver earns its mode.
# Built to the FINEST SOURCED LEVEL; every level-drop is named, not gone quiet about.
# ===========================================================================

# --- revenue: per product, volume AND price ---
for _product, _note in [
        ("Revenue — granulated urea (EGP)", "largest line at 40.9% of H1-2026 sales revenue"),
        ("Revenue — prilled urea (EGP)", "37.6% of H1-2026 sales revenue"),
        ("Revenue — ammonium nitrate (EGP)", "14.5% of H1-2026 sales revenue; the one line in "
                                             "decline, and the one whose margin collapsed"),
        ("Revenue — ammonia (EGP)", "3.9% of H1-2026 sales revenue; recovered from a 52% fall "
                                    "in FY-Jun-2025")]:
    R.add_driver(
        _product, DriverMode.BOTTOM_UP,
        f"Product-level revenue is printed in the revenue note of every filing and foots exactly "
        f"in all five periods ({_note}), and the plant-level segment note carries cost of sales "
        f"and gross profit for the same line. Built per product, not as one top line.",
        [f_products, f_segments, f_fy2025, f_h1])

R.add_driver(
    "Revenue — liquid fertilizer / UAN (EGP)", DriverMode.BOTTOM_UP,
    "New line from a restarted plant, disclosed separately from the transitional period onward "
    "(EGP 694.0m then 693.1m) with its own segment margin of 74.5%. Modelled as an explicit "
    "dated restart and dual-framed, never folded into a growth rate — and carried at a "
    "utilisation the disclosure supports, because the company's own numbers show two "
    "contributing quarters separated by a zero quarter.",
    [f_liquid, f_products, f_segments])

R.add_driver(
    "Sales volume — company total (tonnes, indexed)", DriverMode.BOTTOM_UP,
    "The company states its own volume growth in words: sales volumes +12%, export volumes +31%, "
    "production +17% and 23% above plan in H1-2026. The volume leg is projected on that disclosed "
    "base, banded by gas availability from the issuer's own curtailment history and lifted by the "
    "completed +200 t/day ammonia and +210 t/day urea debottleneck. The EGCH same-class prior "
    "(flat urea tonnes over-forecast by 9.3% in every unit-window cell) is applied: the path "
    "starts below plate, not at it.",
    [f_pricevol, f_ir_release, f_gasevents, f_utilisation, f_trade])

R.add_driver(
    "Realised price per tonne — company level (EGP/t)", DriverMode.BOTTOM_UP,
    "Solved from the company's own disclosed split: sales value +87% against sales volumes +12% "
    "implies realised price +~67% in H1-2026. Projected on the urea reference path, which had "
    "already reversed from ~USD 700/t to the low USD 400s by the period end. Both legs of the "
    "build move — volume and price — as the protocol requires.",
    [f_pricevol, f_urea, f_products])

R.add_driver(
    "Realised price per tonne — BY PRODUCT (EGP/t)", DriverMode.TOP_DOWN,
    "LEVEL DROP, DECLARED. Per-product tonnage is not disclosed anywhere — production and sales "
    "volumes appear only as bar charts whose labels do not reconcile with their own narrative "
    "(F45). Per-product price is therefore carried top-down as the company-level realised-price "
    "path applied to each line's disclosed revenue mix. Never divide one period's revenue by "
    "another period's tonnage [L-010]: no per-product price is computed from the chart labels.",
    [f_neg_volumes, f_pricevol, f_products])

R.add_driver(
    "Local versus export revenue split", DriverMode.BOTTOM_UP,
    "Disclosed and footing in every period: export ran 71.9% / 70.1% / 61.6% / 65.6% / 81.3% of "
    "sales revenue across FY-Jun-2024, FY-Jun-2025, the two halves to December and H1-2026. The "
    "two legs face different prices, different duties and different CBAM exposure, so they are "
    "never blended.",
    [f_products, f_fy2025, f_h1])

R.add_driver(
    "Ministry of Agriculture quota versus local free market", DriverMode.TOP_DOWN,
    "LEVEL DROP, DECLARED. The company confirms it supplies an administered quota at specified "
    "prices and separately reports 40 local free-market customers, but never quantifies either "
    "leg (F48). The regulated share of the local leg is therefore set top-down and sensitised, "
    "and the sector-wide 55% obligation reported in the press is NOT applied as a company "
    "constraint because no ABUK filing confirms it.",
    [f_neg_quota, f_fiscal, f_products])

# --- cost: one escalator per driver, and margin as an OUTPUT ---
R.add_driver(
    "Cost of sales — natural gas feedstock (EGP)", DriverMode.BOTTOM_UP,
    "The single largest cost is separately quantified in the related-party note (EGP 7.58bn "
    "FY-Jun-2024, EGP 9.77bn FY-Jun-2025, EGP 9.08bn in the six months to Jun-2026 — 90-97% of "
    "materials and supplies), and its CONTRACT PRICE FORMULA is disclosed: linked to Ministry of "
    "Agriculture prices, international urea bulletin prices and the CBE USD rate, with the "
    "USD 8.50/mmBtu floor of Decree 928/2026 underneath it. Built as a formula-linked cost that "
    "moves with the revenue it funds, not as a blended escalator [L-009].",
    [f_gas, f_gasprice, f_costnature, f_urea])

R.add_driver(
    "Gas cost per mmBtu", DriverMode.TOP_DOWN,
    "LEVEL DROP, DECLARED. ABUK discloses neither its gas volume nor its realised unit price — "
    "one hit for 'mmBtu' across three full filings and it is the regulatory floor, not a "
    "consumption figure (F46). A cost-per-unit build is therefore not sourceable; the gas driver "
    "runs in EGP on the disclosed formula, and the USD 8.50 floor is applied as a binding "
    "constraint whenever the formula output falls below it.",
    [f_neg_gasunit, f_gas, f_gasprice])

R.add_driver(
    "Cost of sales — salaries, depreciation and other operating cost (EGP)", DriverMode.BOTTOM_UP,
    "Cost of sales is disclosed BY NATURE in every period and foots to the printed total exactly "
    "in every one — salaries and wages, depreciation, employee benefits and other operating cost "
    "are each separately stated. One escalator per line [L-009]: wages on wage inflation, "
    "depreciation off the fixed-asset roll-forward, not a single blended index.",
    [f_costnature, f_fy2025, f_h1])

R.add_driver(
    "Gross margin by plant — AN OUTPUT, NEVER AN INPUT", DriverMode.BOTTOM_UP,
    "NOT SET. Margin falls out of per-product revenue against per-plant cost. The plant-level "
    "segment note discloses revenue, cost of sales and gross profit for each of Plants 1, 2, 3, "
    "Ammonia and Liquid fertilizer, so there is no case for typing a margin in [L-005]. The "
    "reason it matters here is measured: Plant 2's margin collapsed from 22.3% to 7.6% while "
    "Plants 1 and 3 expanded to 61.6% and 65.7% — a blended company margin would score that as an "
    "unexplained improvement instead of a mix shift.",
    [f_segments, f_costnature, f_products, f_gas])

R.add_driver(
    "Selling and marketing expenses, including export duty (EGP)", DriverMode.BOTTOM_UP,
    "Disclosed by nature and attributed by the company itself: the H1-2026 rise is stated to be "
    "'increased export duties and packing expenses'. The duty leg is built from the decrees "
    "directly — USD 90/t from 4-May-2026 under Decision 190, 10% of FOB from 23-Jun-2026 under "
    "Decision 258, and ZERO from 1-Aug-2026 under Decision 340 — applied to the disclosed export "
    "revenue base.",
    [f_costnature, f_duty_on, f_duty_off, f_products])

R.add_driver(
    "Export duty rate, forward", DriverMode.BOTTOM_UP,
    "ZERO from 1-Aug-2026, on the issuer's own filing. Decision 340 of 2026 (25-Jun-2026) cancels "
    "Decisions 190, 203 and 258 effective 1 August 2026 and the company states it expects a "
    "positive impact on subsequent periods. NINE press and analyst sources searched and NOT ONE "
    "carries this decree — every one of them stops at the 10% FOB duty and reports it in force "
    "(F09). Reinstatement is priced as an explicit downside scenario, not assumed away.",
    [f_duty_off, f_duty_on, f_neg_duty_press])

# --- below the operating line ---
R.add_driver(
    "Foreign exchange result (EGP)", DriverMode.BOTTOM_UP,
    "Built as POSITION x RATE, not assumed. The company discloses net foreign-currency balances "
    "of USD 422m plus EUR 105k (EGP 20,754,874,389 at EGP 49.23/USD) and its own +/-10% "
    "sensitivity of EGP 2,075,487,438. This matters because the FX line swung EGP +1.75bn to "
    "-1.74bn between Q1 and Q2 of 2026 and pushed net profit down while operating profit rose.",
    [f_fxpos, f_q1, f_q2, f_fx_regime])

R.add_driver(
    "Finance income on treasury bills and deposits (EGP)", DriverMode.BOTTOM_UP,
    "Built on disclosed balances at disclosed rates: treasury bills at amortised cost of "
    "EGP 2,387,005,439 and other financial assets of EGP 394,692,470 at 31-Dec-2025, cash of "
    "EGP 17.07bn, with interest income from treasury bills (EGP 618,730,025 in H1-2026) and "
    "finance income printed separately in the cash-flow statement. Rates glide with the CBE "
    "corridor. Excluded from FCFF and handled in the equity bridge so the cash is not counted "
    "twice.",
    [f_tp, f_h1, f_cbe, f_fxpos])

R.add_driver(
    "Share of profit of equity-accounted associates (EGP)", DriverMode.BOTTOM_UP,
    "Alexfert 15%, Helwan 17%, WAPHCO and Abu Tartour 9.5% are named with their carrying values "
    "(EGP 5,250,041,007 at 31-Dec-2025) and their contribution printed separately "
    "(EGP 942,853,070 in H1-2026, 7.4% of pre-tax profit). Forecast on the SAME urea price and "
    "gas path as the parent so the two cannot silently diverge, and brought into the bridge at "
    "the dividends actually received (EGP 1,114,082,000 in H1-2026).",
    [f_assoc_peers, f_restate, f_h1])

R.add_driver(
    "Effective tax rate", DriverMode.BOTTOM_UP,
    "Set from the company's own printed charge over four periods — 21.2%, 21.6%, 22.4%, 20.9% — "
    "a tight band around the 22.5% statutory rate, rather than by statutory formula. The EGCH "
    "same-class prior records statutory-formula tax as its second-largest profit error.",
    [f_tax, f_fy2025, f_tp, f_h1])

# --- capital, structure and discounting ---
R.add_driver(
    "Capital expenditure (EGP)", DriverMode.BOTTOM_UP,
    "The cash-flow statement prints 'Payment for acquisition of Fixed assets and assets under "
    "construction' directly — EGP 386,508,202 in H1-2026 against EGP 460,759,681 in H1-2025 — and "
    "the project pipeline is named and costed (Abu Tartour USD 643m at a 9.5% share, solar phase "
    "one EGP 88.32m at 85% complete, phase two 2.5-3MW, ABB steam optimisation USD 500k). Built "
    "from named projects, never as a percentage of revenue. The EGP 2.3bn of fully depreciated "
    "but still-operating assets flags that book depreciation understates replacement need.",
    [f_h1, f_projects, f_utilisation])

R.add_driver(
    "Capital structure and cost of debt", DriverMode.BOTTOM_UP,
    "The company states it has NO LOANS at the reporting date and holds EGP 17.07bn of cash plus "
    "EGP 2.39bn of treasury bills. The WACC is therefore effectively all-equity, the cost of debt "
    "carries no weight, and the enterprise-to-equity bridge ADDS net cash rather than deducting "
    "debt.",
    [f_fxpos, f_tp, f_h1])

R.add_driver(
    "Equity base / book value for the NAV and bridge (EGP)", DriverMode.BOTTOM_UP,
    "EGP 23,241,840,301 at 31-Dec-2025 and EGP 29,462,212,810 at 30-Jun-2026, on THREE agreeing "
    "company sources for the December figure. The FY-Jun-2025 balance sheet as filed is NOT used: "
    "it is superseded by a restatement that removed EGP 7.95bn of assets and EGP 5.25bn of equity "
    "(EGP 4.16 a share). The earnings release's 'EGP 32.24 billion' is recorded as the company's "
    "own error — it fails the release's own arithmetic — and is not averaged in.",
    [f_restate, f_tp, f_release_typo, f_ir_kpi])

R.add_driver(
    "Share count and per-share denominators", DriverMode.BOTTOM_UP,
    "1,261,875,720 shares, established from company documents only and confirmed four ways, the "
    "authority being the audited FY-Jun-2025 dividend statement: shareholders' share of "
    "EGP 6,309,378,600 at a printed EGP 5.00 per share. No aggregator figure is used.",
    [f_shareholders, f_dividends])

R.add_driver(
    "Dividend and distributable cash flow", DriverMode.BOTTOM_UP,
    "Built through the company's OWN appropriation waterfall, which is printed in the audited "
    "dividend distribution statement: net profit less the employees' share less board "
    "remuneration leaves ~85% for shareholders — a relationship that reproduces the printed EPS "
    "to the piastre in every period tested. Applying a payout ratio to net profit would overstate "
    "the shareholder claim by 13-15% every year. The declared sequence (EGP 7.50, 5.00, 2.30) is "
    "length-adjusted for the six-month transitional period before any trend is read.",
    [f_dividends, f_fy2025, f_tp])

R.add_driver(
    "Beta and the cost-of-equity regressor", DriverMode.BOTTOM_UP,
    "Single listing confirmed from the company's own releases (ABUK.CA, EGX only, EGP only, ISIN "
    "EGS38191C010), so there is one legitimate regressor and no currency or magnitude ambiguity. "
    "Run through beta_regression.own_stock_beta('ABUK','EG','EGX') against the registered "
    "published index engine/raw_indices/EG/EGX30.csv — never a constituent composite [R-BETA-01].",
    [f_listing])

R.add_driver(
    "Terminal risk-free rate and inflation", DriverMode.BOTTOM_UP,
    "Norm-built from the CBE's OWN published medium-term targets — 7% (+/-2pp) for Q4-2026 and 5% "
    "(+/-2pp) for Q4-2028 — plus the house EM real-rate convention, with the sovereign default "
    "spread netted out so country risk is charged once [L-004]. Never a historical average and "
    "never backed out of a price. Terminal inflation is set equal to terminal growth [L-055].",
    [f_cbe, f_fx_regime])

R.add_driver(
    "Forecast base period and the fiscal-year break", DriverMode.BOTTOM_UP,
    "The base is the SIX-MONTH transitional period plus the two disclosed 2026 quarters, never a "
    "'FY2025' of twelve months ending in December — no such year exists. Arithmetic across three "
    "separate filings proves the length. The inflation mapping is split at the break "
    "[R-MACRO-01 AMENDED] and anything annualised is labelled as annualised [R-GAP-01].",
    [f_tp, f_q1, f_q2, f_h1, f_fy2025])

R.add_driver(
    "Terminal-period assumptions", DriverMode.TOP_DOWN,
    "LEVEL DROP, DECLARED. The company publishes no multi-year guidance of any kind — a "
    "three-line statutory budget for FY2026 and nothing else, with the McKinsey plan described "
    "only as 'nearing completion' (F47). The terminal is therefore built top-down from the "
    "disclosed asset base and capacity rather than from any company-stated path, and the FY2026 "
    "budget is used ONLY as evidence of forecast dispersion for the scenario width — never as a "
    "central case, since H1 actual pre-tax profit is already 143% of the full-year budgeted figure.",
    [f_neg_guidance, f_budget, f_projects])


# ===========================================================================
# OUTPUT — errors and warnings printed verbatim, never suppressed.
# ===========================================================================
errors, warnings = R.validate()
R.to_json(os.path.join(HERE, 'sweep_register.json'))

print(R.qc_line())
print(f"\nfindings: {len(R.findings)} | drivers: {len(R.drivers)}")

_bu = sum(1 for d in R.drivers if d.mode is DriverMode.BOTTOM_UP)
_td = len(R.drivers) - _bu
_ir = sum(1 for f in R.findings if f.source_type is SourceType.COMPANY_IR)
_co = sum(1 for f in R.findings if f.source_type is SourceType.COMPANY_OFFICIAL)
print(f"drivers by mode: {_bu} bottom-up / {_td} top-down")
print(f"company sources: {_co} COMPANY_OFFICIAL / {_ir} COMPANY_IR")
print(f"primary-access attempts logged: {len(R.primary_access)} "
      f"({sum(1 for p in R.primary_access if p.reachable)} reachable, "
      f"{sum(1 for p in R.primary_access if not p.reachable)} unreachable)")

_fs_years = sorted({f.fiscal_period for f in R.findings
                    if f.is_fs_data and f.fiscal_period.startswith("FY")})
_periods = sorted({f.fiscal_period for f in R.findings if f.fiscal_period})
print(f"fiscal years with is_fs_data: {_fs_years}")
print(f"all periods tagged: {_periods}")

if errors:
    print(f"\nVALIDATOR ERRORS ({len(errors)}) — disclosed, not suppressed:")
    for e in errors:
        print(f"  ! {e}")
else:
    print("\nVALIDATOR ERRORS (0): none.")

if warnings:
    print(f"\nVALIDATOR WARNINGS ({len(warnings)}) — disclosed, not suppressed:")
    for w in warnings:
        print(f"  - {w}")
else:
    print("\nVALIDATOR WARNINGS (0): none.")

_fresh = R.check_freshness(DELIVERY_DATE)
print(f"\nfreshness (delivery {DELIVERY_DATE}): "
      f"{_fresh or 'OK — sweep and intended delivery are the same day, 0 days elapsed'}")
print(f"register rows: {len(R.register_rows()) - 1} | "
      f"driver rows: {len(R.driver_rows()) - 1} | JSON written to "
      f"{os.path.join(HERE, 'sweep_register.json')}")
