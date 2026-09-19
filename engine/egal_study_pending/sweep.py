"""EGAL — Aluminium Company of Egypt (Egyptalum), EGX:EGAL.CA, ISIN EGS3E181C010.

Step 2A four-ring Information Sweep register. FIRST-BUILD sweep: no prior EGAL study
directory existed. Runs BEFORE any forecast driver is set. Every mandatory category of
every ring is closed by a dated finding or a dated negative search, and every negative
search recorded here is a query that was ACTUALLY RUN on the sweep date.

WRITTEN TO engine/egal_study_pending/ ON PURPOSE. Not engine/egal_study/. A half-built
study directory under the engine/*_study glob turns roughly ten repository gates red;
the _pending suffix sits outside that glob deliberately.

-----------------------------------------------------------------------------------
THE PRIMARY-SOURCE RULE WORKED, AND THIS IS THE RECORD OF IT
-----------------------------------------------------------------------------------
egyptalum.com.eg was reached (HTTP 200) and is the source of every Company-ring figure
below. Its "Investor Relation" page is an iframe onto the company's own IR portal at
mistnews.com/ir/ir.aspx?sk=103905032018, which serves the audited statements, the
disclosure filings, the board/shareholder-structure reports, the dividend and general-
assembly records and the investment-project plans. The company's sustainability report,
its EPD and its plant/capacity pages are served from egyptalum.com.eg itself.

NO aggregator, broker or press figure is carried for anything the company reports about
itself. Press appears only in the Global / Country / Industry rings, as external context.

BLOCKED HOSTS, WITH THE ACTUAL FAILURE TEXT:
  * egyptalum.com  and www.egyptalum.com  -> curl (35) "Recv failure: Connection reset
    by peer". The .com is dead; the live issuer domain is egyptalum.com.eg, which is
    the address printed on the company's own letterhead and in its EGX filings.
  * egyptalum.net  -> curl (56) "CONNECT tunnel failed, response 502".
  * www.egx.com.eg AND egx.com.eg (whole domain, not one path) -> without a browser
    User-Agent: curl (52) "Empty reply from server". With a browser User-Agent:
    HTTP 200, Content-Type text/html, 6,117 bytes containing window["bobcmn"] — an
    Imperva/Incapsula JavaScript bot-challenge page, never the requested PDF. The EGX
    filing portal is therefore unreachable from this environment.

[R-SIGCM-03] FALLBACK, NAMED: every document that the EGX portal would have served was
taken instead from the COMPANY'S OWN IR host (mistnews.com/mistsat/companies/... and
mistnews.com/ir_admintool/reports/...), which is the company's own filing channel, not
a third party. The one document the fallback could NOT reach is named in F44.

-----------------------------------------------------------------------------------
FISCAL YEAR ENDS 30 JUNE. This is not the Egyptian default and it drives everything.
-----------------------------------------------------------------------------------
FY2025 = 1 Jul 2024 to 30 Jun 2025. FY2026 = 1 Jul 2025 to 30 Jun 2026, and FY2026 is
the STUDY YEAR: it was complete on 30 Jun 2026 and its unaudited indicators were
released on 12 Aug 2026, three weeks before this sweep. A build that treats "2026" as
a calendar year will mis-date every quarter and every tariff step.

-----------------------------------------------------------------------------------
EXTRACTION ROUTE — EVERY EGAL FILING IS A PURE IMAGE SCAN
-----------------------------------------------------------------------------------
All eleven statement PDFs on the IR shelf carry ZERO text characters across every page
(pdftotext returns 0 chars on 39, 40, 38, 15, 8 and 81-page documents alike). There is
no text layer to trust or distrust; the only route is the rendered pixels. Tesseract in
this environment took >5 minutes per page and was abandoned; pages were read off
pdftoppm renders at 100-600 dpi and EVERY column was re-added against the filing's own
printed subtotals.

THREE GLYPH ERRORS WERE CAUGHT THIS WAY, AND BOTH ROUTES ARE RECORDED:
  1. FY2025 annual, page 1, FY2024 comparative "equipments": the 200 dpi render is
     ambiguous between 2,586,061,477 and 2,586,081,477. Only 2,586,061,477 makes the
     printed total fixed assets of 2,870,263,580 foot. Arithmetic settled it.
  2. FY2024 annual, page 7, FY2023 comparative: at 100 dpi the cost lines read
     14,866,774,151 and 136,967,172, which sum to 15,003,741,323 against a printed
     total cost of 15,002,731,323 — a 1,010,000 break. Re-read at 400 dpi they are
     14,865,774,151 and 136,957,172, which foot to the pound. Two glyph errors on one
     page, both settled by the column re-add.
  3. FY2025 annual, note 20, the sales-quantity disclosure: at 100 dpi it reads
     "290 thousand tons"; at 260 dpi and again at 600 dpi it reads "295 thousand tons".
     No subtotal exists to arbitrate, so the highest-resolution read governs and both
     are recorded here. The 295 kt figure is the single most load-bearing number in
     the whole sweep — it is the denominator of realised price per tonne — and the
     100 dpi read would have put realised price 1.7% too high.

WHAT FOOTS: the FY2025 balance sheet, income statement and cash-flow statement all
foot exactly, line by line, in both the current and the comparative column; total
assets equal total liabilities and equity to the pound in FY2025, FY2024, Q1-FY2026
and 9M-FY2026; the FY2025 gross-receivable client list (5,475,986,269.98) equals net
trade receivable plus its provision (4,877,357,549 + 598,628,721) exactly.

WHAT DOES NOT FOOT, RECORDED RATHER THAN REPAIRED: the company's own Sustainability
Report 2022-2023 prints Total Emissions 3,955,246.20 tCO2e, Total Production 286,412.00
t Al and GHG Intensity 13.182 tCO2e/tAl. 3,955,246.20 / 286,412.00 = 13.810, not
13.182. Both the text layer and a 200 dpi pixel read agree on all three digits, so this
is the document's own internal inconsistency, not an extraction error. 13.182 implies a
denominator of 300,049 t. See F30.

-----------------------------------------------------------------------------------
BETA — DELIBERATELY NOT RESOLVED, PER INSTRUCTION
-----------------------------------------------------------------------------------
No beta is computed here and none should be inferred from this register. What is
recorded (F49) is the listing and the series that exist: a SINGLE listing on the
Egyptian Exchange, ticker EGAL.CA, ISIN EGS3E181C010, listed 29 July 1997, quoted and
reported in EGP. There is NO dual listing — the Orascom Construction ADX/EGX trap does
not apply here, and that was checked rather than assumed. The repo already holds
engine/raw_ohlc/EG/EGAL.csv (3,537 daily rows, 02-Jan-2011 to 23-Aug-2026, last close
EGP 330.00) and engine/raw_indices/EG/EGX30.csv (to 08-Sep-2026, 56,174.30). THE PRICE
SERIES IS STALE BY SEVENTEEN CALENDAR DAYS relative to this sweep and the stock has
moved a long way inside that gap: the company's own IR feed showed a last/close of
EGP 374.99 on the sweep date, 13.6% above the last row in the repo file. Any beta run
must refresh the panel first. Resolving the beta itself is out of scope for this sweep
and is left to a run of engine/beta_regression.py own_stock_beta().

-----------------------------------------------------------------------------------
WHAT A LATER BUILD WOULD GET WRONG IF IT DID NOT READ THIS REGISTER
-----------------------------------------------------------------------------------
  * It would smooth an administered power tariff that stepped +26.1% then +18.1%.
  * It would carry FY2025's 34.6% gross margin forward and miss Q1-FY2026's 30.0%.
  * It would treat the state's 92.04% holding as float and mis-size liquidity.
  * It would model Trafigura's +300 kt as growth rather than as a dual-framed event.
  * It would put FY2022 in the history table from a source that does not exist.

VALIDATOR STATE: printed verbatim by this module at the bottom. Nothing suppressed.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))

from research_sweep import (SweepRegister, AssetClass, Ring, FindingClass,
                            SourceType, DriverMode)

SWEEP_DATE = "2026-09-09"
R = SweepRegister("EGAL", AssetClass.STOCK, SWEEP_DATE)

CO = SourceType.COMPANY_OFFICIAL
IR = SourceType.COMPANY_IR
REG = SourceType.REGULATOR_OFFICIAL
PMD = SourceType.PRIMARY_MARKET_DATA
PRESS = SourceType.REPUTABLE_PRESS

# =====================================================================
# PRIMARY ACCESS — the company's own channel, logged success and failure
# =====================================================================
R.record_primary_access(
    "https://egyptalum.com.eg/", True, "2026-09-09",
    note="HTTP 200. The live issuer domain, and the address printed on the company's "
         "own EGX cover letters and disclosure filings. Source of the plant/capacity "
         "pages, the sustainability shelf and the IR entry point.")
R.record_primary_access(
    "https://egyptalum.com/", False, "2026-09-09",
    note="curl (35) 'Recv failure: Connection reset by peer'. The .com is dead. "
         "www.egyptalum.com fails identically. Recorded so a later reader does not "
         "repeat the attempt or mistake the dead host for the issuer.")
R.record_primary_access(
    "https://egyptalum.net/", False, "2026-09-09",
    note="curl (56) 'CONNECT tunnel failed, response 502' at this environment's proxy.")
R.record_primary_access(
    "https://egyptalum.com.eg/Ir.aspx?LId=7", True, "2026-09-09",
    note="HTTP 200 after one transient ws_closed_mid_exchange retry. The page body is "
         "EMPTY apart from an iframe onto the company's own IR portal — a reader who "
         "stops at this page would wrongly conclude EGAL publishes no IR material.")
R.record_primary_access(
    "https://www.mistnews.com/ir/ir.aspx?sk=103905032018", True, "2026-09-09",
    note="HTTP 200. The company's own IR portal behind that iframe. Its sub-pages "
         "(financial.aspx, news.aspx, Economic_Agenda.aspx, getData.aspx) return "
         "'Not authorized or you need to enable cookies' unless the full m= company "
         "key is passed on the query string; with it they serve normally. Recorded "
         "because the naive fetch looks like a permission wall and is not one.")
R.record_primary_access(
    "https://www.mistnews.com/mistsat/companies/mezanyat/en/334089_1_0_2025.pdf",
    True, "2026-09-09",
    note="HTTP 200, 6,081,727 bytes. FY2025 audited statements, direct from the "
         "company's own IR host. Eleven statement PDFs retrieved from this path.")
R.record_primary_access(
    "https://www.egx.com.eg/downloads/Bulletins/342467_1.pdf", False, "2026-09-09",
    note="BLOCKED. Without a browser User-Agent: curl (52) 'Empty reply from server'. "
         "With a Chrome User-Agent: HTTP 200, Content-Type text/html, 6,117 bytes of "
         "Imperva/Incapsula JavaScript bot-challenge (window[\"bobcmn\"]), not a PDF. "
         "www.egx.com.eg/en/homepage.aspx returns the same challenge, so the block is "
         "the whole domain and not this path. This is the attachment carrying the "
         "FY2026 full-year UNAUDITED financial indicators from the 11-Aug-2026 board "
         "meeting. USER ACTION REQUESTED — see F44.")
R.record_primary_access(
    "https://egx.com.eg/downloads/Bulletins/342467_1.pdf", False, "2026-09-09",
    note="Same Imperva challenge without the www host. Recorded so the no-www variant "
         "is not tried again as if it were a route round the block.")
R.record_primary_access(
    "https://egyptalum.com.eg/Files/Sustainability/"
    "Sustainability__Report__for_Egyptalum_2022-2023_-_REV01_(4)_Final_version.pdf",
    True, "2026-09-09",
    note="HTTP 200, 11,514,456 bytes, 80 pages WITH a text layer. The only company "
         "document that discloses site electricity consumption and production tonnes.")
R.record_primary_access(
    "https://www.mistnews.com/ir_admintool/reports/"
    "Investment%20Projects%20Plan%20Year%202024-2025.pdf", True, "2026-09-09",
    note="HTTP 200. Line-item capital budget for FY2024/25, from the IR portal's "
         "Summary of Operations page. The FY2025-2026 equivalent returns HTTP 404.")

# =====================================================================
# STUDY YEAR — FY2026 (1 Jul 2025 to 30 Jun 2026)
# =====================================================================
R.declare_study_year("2026", ["Q1-2026", "H1-2026", "9M-2026", "FY2026"])

# =====================================================================
# RING 1 — GLOBAL
# =====================================================================
f_rates = R.add(
    Ring.GLOBAL, "rate cycle & USD/FX regime", FindingClass.S,
    "EGP at USD/EGP 50.9786 buy / 51.0786 sell on 08-Sep-2026 on the CBE's own board; "
    "the currency has been broadly stable since the March-2024 float, so the FX shock "
    "that dominated FY2024 has become an FX TAILWIND",
    "Central Bank of Egypt, official daily exchange rates, 08-Sep-2026",
    REG, "2026-09-08",
    url="https://www.cbe.org.eg/en/economic-research/statistics/exchange-rates",
    model_impact="Sets the translation rate for the ~60% of revenue that is exported "
                 "and USD-linked, and for alumina/coke imports. The FX line flipped "
                 "from a loss of EGP 811.5m in FY2024 to a gain of EGP 260.8m in FY2025 "
                 "and EGP 682m in 9M-FY2026 — modelled explicitly, NOT smoothed into "
                 "an operating margin.")

f_lme = R.add(
    Ring.GLOBAL, "commodity complex (input/output)", FindingClass.D,
    "LME three-month aluminium ~USD 3,250/t in early Sep-2026, having crossed USD 3,000 "
    "at the start of 2026, peaked at USD 3,325 on 29-Jan-2026 and printed a cash bid of "
    "USD 3,738 on 04-Jun-2026. Alumina, the main input, is in the OPPOSITE state: a "
    "0.8-1.1 Mt surplus with 2026 averaging around USD 290/t after easing to USD 304/t "
    "in March",
    "LME price reporting aggregated across Fastmarkets, ING Think and International "
    "Aluminium Journal coverage of the 2026 market",
    PRESS, "2026-09-01",
    detail="EGAL itself points investors at the LME: its own website carries a 'London "
           "Metal Exchange — Primary Aluminium Prices, Daily Prices (www.lme.co.uk)' "
           "page under the Smelter menu, so the LME is the company's own stated price "
           "reference rather than an analyst's imposition.",
    model_impact="DRIVER UNLOCK for the price leg. Realised EGP price per tonne is "
                 "built as LME plus/minus a solved realisation spread rather than as a "
                 "growth rate, and the widening LME-versus-alumina spread is the "
                 "mechanism behind any gross-margin recovery in the forecast window.")

f_gdem = R.add(
    Ring.GLOBAL, "global sector demand", FindingClass.S,
    "Primary aluminium stays in deficit through 2026 — roughly 140 kt on the tightest "
    "published estimate, following a wider 2025 shortfall — because China is pressed "
    "against its self-imposed 45 Mt capacity cap while power constraints limit supply "
    "growth elsewhere",
    "ING Think, 'Aluminium deficit will support prices in 2026'; Wood Mackenzie short-"
    "term outlook; alcircle market tightness coverage",
    PRESS, "2026-06-01",
    model_impact="Supports holding the realised-price path near current LME rather "
                 "than mean-reverting it down, and is the reason the bear case is "
                 "driven by EGAL's own cost line rather than by a metal-price collapse.")

f_trade = R.add(
    Ring.GLOBAL, "trade / sanctions / supply chains", FindingClass.B,
    "Two trade walls closed on aluminium inside the study year. The US Section 232 "
    "tariff on aluminium stands at 50%, and from 06-Apr-2026 it applies to the FULL "
    "customs value of derivative products. The EU's CBAM left its reporting phase and "
    "became financially binding in January 2026, with certificates benchmarked at just "
    "over EUR 75 per tonne of embedded CO2",
    "US Section 232 proclamations as summarised by White & Case and Congressional "
    "Research Service; European Commission CBAM definitive-period rules",
    PRESS, "2026-06-02",
    detail="EGAL's exposure is specific and measurable rather than generic: it exported "
           "EGP 22,102m in 9M-FY2026 (60.1% of sales, F26) and its own disclosed GHG "
           "intensity is 13.182 tCO2e per tonne of aluminium (F30) against the 5.2 "
           "tCO2e/t threshold its own sustainability report plots itself against. A "
           "grid-powered Egyptian smelter is on the wrong side of CBAM arithmetic.",
    model_impact="BASE CHANGER, dual-framed. Model the export leg with and without a "
                 "CBAM certificate charge on embedded carbon above the benchmark, and "
                 "show the US 50% tariff as a discrete constraint on the addressable "
                 "export market — never as a haircut folded into a growth rate. This is "
                 "also the commercial logic behind the Scatec solar PPAs (F23).")

# =====================================================================
# RING 2 — COUNTRY
# =====================================================================
f_cbe = R.add(
    Ring.COUNTRY, "sovereign macro (inflation, policy rate, FX/deval risk)",
    FindingClass.D,
    "CBE held for a fourth consecutive meeting on 20-Aug-2026: overnight deposit 19.00%, "
    "overnight lending 20.00%, main operation 19.50%. Headline inflation rose to 14.9% "
    "in July from 14.3% in June and core to 14.7% from 14.3%, though monthly headline "
    "and core both printed 0.0%. The CBE expects inflation to accelerate through Q3-2026 "
    "before declining toward target",
    "Central Bank of Egypt MPC statement 20-Aug-2026 and Monetary Policy Report Q1-2026",
    REG, "2026-08-20",
    url="https://www.cbe.org.eg/-/media/project/cbe/listing/publication/"
        "monetary-policy-report/2026/monetary-policy-report---mpr-q1-2026.pdf",
    model_impact="DRIVER UNLOCK for the cost of capital. Explicit-window risk-free rate "
                 "anchors on the 19.50% main operation rate; the terminal is norm-built "
                 "off the CBE's OWN published medium-term inflation target plus a "
                 "standard EM real-rate convention, never averaged out of history. Also "
                 "sets the yield on EGAL's very large cash pile (F16).")

f_tariff = R.add(
    Ring.COUNTRY, "regulatory environment (regulator, caps, tariffs, tax/subsidy)",
    FindingClass.B,
    "THE ADMINISTERED POWER TARIFF, WHICH IS THIS COMPANY'S REAL P&L. EgyptERA's "
    "published schedule for Extra High Voltage (220-132 kV), 'OTHER USERS': 126.9 "
    "Pt/kWh average energy price for 1-Jan-2024 to 31-Jul-2024 (off-peak 117.1, on-peak "
    "175.7, demand charge EGP 40/kW/month); 160.0 Pt/kWh flat from 01-Sep-2024; 189.0 "
    "Pt/kWh flat from April 2026. That is +26.1% then +18.1%, and +48.9% cumulative",
    "Egyptian Electric Utility and Consumer Protection Regulatory Agency (EgyptERA), "
    "published tariff schedules Tarrif2024N, TarrifAug2024 and TarrifApril2026",
    REG, "2026-04-01",
    url="https://egyptera.org/en/TarrifApril2026.aspx",
    detail="High Voltage (66-33 kV) OTHER USERS moved 174.0 -> 205.0 Pt/kWh on the same "
           "dates. KIMA, the other electro-intensive Upper Egypt plant, is named as its "
           "own tariff line at 160.0 then 189.0; EGAL is NOT separately named and no "
           "EGAL-specific rate is published. EgyptERA has no 2025 tariff page, which "
           "implies the Sep-2024 rate held for nineteen months to April 2026 — stated "
           "as an inference from the absence of a page, not as a disclosure.",
    model_impact="BASE CHANGER, and the single most important number in the model. Map "
                 "the steps onto the JUNE fiscal year, which is where the damage is: "
                 "FY2025 ran two months at 126.9 and ten at 160.0; FY2026 ran nine "
                 "months at 160.0 and three at 189.0, a weighted ~167.3; FY2027 carries "
                 "a FULL year at 189.0, so roughly a further +13% on the average power "
                 "price arrives mechanically with NO new tariff decision. Model each "
                 "step as an explicit dated event and dual-frame the next one. Never "
                 "smooth an administered tariff into a cost-inflation glide.")

f_tax = R.add(
    Ring.COUNTRY, "regulatory environment (regulator, caps, tariffs, tax/subsidy)",
    FindingClass.C,
    "Egypt corporate income tax 22.5%. EGAL's own audited effective rate is higher: "
    "25.50% in FY2025 (income tax EGP 3,470,440,485 plus deferred EGP 15,726,039 on "
    "profit before tax of EGP 13,671,756,576) against 22.46% in FY2024",
    "Aluminium Company of Egypt, audited financial statements FY2025 (income statement, "
    "printed page 8) and FY2024",
    CO, "2025-08-13",
    model_impact="")

f_state = R.add(
    Ring.COUNTRY, "fiscal / political events with sector read-through", FindingClass.S,
    "EGAL is a state industrial asset and is being run as one. It is 89.837%-owned by "
    "Metallurgical Industries Company, under the Ministry of the Public Business Sector. "
    "The Holding Company for Metallurgical Industries resolved in its final committee "
    "meeting of December 2023 to rehabilitate the plant to raise molten-aluminium and "
    "semi-product output, committing about USD 300,000,000 over the following three "
    "years explicitly to cut energy-consumption cost and CO2. The Prime Minister "
    "personally inspected the new wire line, with the Minister of the Public Business "
    "Sector, Eng. Mohamed Shimi, in attendance",
    "Egyptalum Sustainability Report 2022-2023, section 6-2 Energy; Egyptalum company "
    "news item on the Prime Minister's inspection",
    CO, "2024-06-30",
    detail="The reciprocal of state ownership is state pricing: the same government "
           "that funds the rehabilitation sets the power tariff in F03. Both legs must "
           "be modelled, not just the friendly one.",
    model_impact="Supports a capex path well above maintenance levels through the "
                 "explicit window and gives the rehabilitation an owner with the means "
                 "to fund it. It does NOT license assuming a preferential tariff — no "
                 "such tariff is published or disclosed (F45).")

# =====================================================================
# RING 3 — INDUSTRY
# =====================================================================
f_bal = R.add(
    Ring.INDUSTRY, "demand drivers & capacity/supply balance", FindingClass.S,
    "The global market is structurally tight into 2026 on China's 45 Mt cap and on "
    "power constraints outside China, with a projected 100-180 kt deficit underpinning "
    "a USD 3,000-3,200/t price range. Egypt sits inside that tightness as a net "
    "beneficiary on price and a net victim on the input that causes it — power",
    "alcircle, 'Emerging structural tightness in aluminium supply'; ING Think 2026 "
    "aluminium outlook",
    PRESS, "2026-06-01",
    model_impact="Frames the volume driver as capacity-constrained rather than "
                 "demand-constrained: EGAL's forecast volume is set by its own cells "
                 "and its own power, not by whether it can sell the metal.")

f_price = R.add(
    Ring.INDUSTRY, "pricing", FindingClass.D,
    "Aluminium is a world-priced commodity and EGAL is a price taker with roughly 0.45% "
    "of global supply. Consensus 2026 averages clustered at USD 2,700-2,918/t before "
    "the year began (Fastmarkets base USD 2,918, high USD 3,238, low USD 2,550) and "
    "actual 2026 prices have run well above the top of that range",
    "Fastmarkets 2026 aluminium forecast as reported by International Aluminium "
    "Journal; LME price reporting",
    PRESS, "2026-09-01",
    model_impact="DRIVER UNLOCK: converts revenue from a growth rate into a genuine "
                 "volume x price build, and supplies the price scenario spread for the "
                 "sensitivity grid (low 2,550 / base 2,918 / high 3,238 USD/t) instead "
                 "of an invented plus-or-minus band.")

f_entrant = R.add(
    Ring.INDUSTRY, "new entrants (named-competitor level)", FindingClass.S,
    "Two named entrants are targeting Egyptian aluminium at once. Henan Zhongfu "
    "Industrial (China) plans a USD 2bn aluminium production complex in the Suez Canal "
    "Economic Zone at East Port Said, over 1 million square metres and about 3,000 "
    "direct jobs, aimed at premium alloys for food packaging, batteries, electronics, "
    "aviation and rail. Separately Trafigura, with EGAL and Metallurgical Industries "
    "Holding, is in exclusive negotiations on a USD 750-900m complex comprising a "
    "300,000 tpa smelter and a 150,000 tpa anode plant",
    "aluminiumtoday and EgyptToday reporting of the Henan Zhongfu Suez proposal; Energy "
    "Capital & Power reporting of the Trafigura exclusive negotiations",
    PRESS, "2026-08-21",
    detail="Henan Zhongfu targets downstream alloys rather than primary metal, so the "
           "nearer-term competitive overlap is for POWER ALLOCATION and for skilled "
           "labour, not for EGAL's ingot customers. That distinction matters and should "
           "not be collapsed into 'new competition'.",
    model_impact="Caps the terminal margin: a second Egyptian aluminium complex "
                 "competing for the same administered grid capacity weakens any "
                 "assumption that EGAL's power terms improve. Handled as a terminal-"
                 "margin constraint, not as a volume loss inside the explicit window.")

f_tech = R.add(
    Ring.INDUSTRY, "technology substitution", FindingClass.S,
    "ELYSIS started up a 450 kA inert-anode cell at Rio Tinto's Alma smelter in "
    "November 2025 — the first commercial-SIZE implementation — and has issued its "
    "first smelter technology licence, for a 100 kA ten-pot demonstration at Arvida. "
    "The technology removes direct process CO2 and yields oxygen instead",
    "ELYSIS and Rio Tinto releases, Nov-2025; Light Metal Age smelting coverage",
    PRESS, "2025-11-01",
    detail="This is NOT substitution of aluminium demand — nothing displaces aluminium "
           "in the forecast window. It is substitution of the SMELTING PROCESS, and it "
           "matters to EGAL through the carbon channel: EGAL's prebake cells consume "
           "carbon anodes and it runs its own 172,000 tpa anode plant and 140,000 tpa "
           "calciner (F19). An inert-anode world eventually strands that integration. "
           "First commercial cells are years out; the effect lands beyond the explicit "
           "window and belongs in the terminal, not in the glide.",
    model_impact="Terminal-value qualifier only. Do not put an inert-anode capex or "
                 "saving in the explicit window; state in the terminal discussion that "
                 "EGAL's anode/calciner integration is a carbon liability under CBAM "
                 "and a stranding risk under inert anodes.")

f_peers = R.add(
    Ring.INDUSTRY, "competitor capacity / price moves (named)", FindingClass.C,
    "EGAL is a small regional player and the named comparators are an order of "
    "magnitude larger. Emirates Global Aluminium runs over 2.5 Mt/yr and its Al "
    "Taweelah recycling plant — the UAE's largest — was 72% complete with first hot "
    "metal expected in Q1-2026; in April 2026 EGA agreed to buy 80% of Italian "
    "recycler Eco Green. Aluminium Bahrain (Alba) runs more than 1.62 Mt/yr at the "
    "world's largest single-site smelter and acquired Aluminium Dunkerque, the EU's "
    "largest smelter, for about USD 2.2bn",
    "Light Metal Age and Alba/EGA corporate announcements as compiled by alcircle, "
    "'Gulf aluminium producers accelerate overseas acquisitions'",
    PRESS, "2026-04-01",
    detail="At a 320,000 tpa nameplate EGAL is about one fifth of Alba and one eighth "
           "of EGA. The Gulf peers are moving into RECYCLING and into EU-located "
           "capacity, i.e. buying their way inside the CBAM border. EGAL's answer is "
           "solar PPAs (F23) rather than relocation, which is a materially different "
           "and less complete hedge.",
    model_impact="")

# =====================================================================
# RING 4 — COMPANY
# Every figure below comes from a document served by the company's own channel.
# =====================================================================

# ---- official financial statements ----------------------------------
f_fs25 = R.add(
    Ring.COMPANY, "official financial statements", FindingClass.D,
    "FY2025 audited (1-Jul-2024 to 30-Jun-2025): net sales EGP 43,182,999,188 plus "
    "other operating revenue 97,925 = total income from operations 43,183,097,113; cost "
    "of goods sold 27,873,523,941 and distribution/selling 350,470,794 = total cost "
    "28,223,994,735; GROSS PROFIT 14,959,102,378 (34.64%); profit before tax "
    "13,671,756,576; NET PROFIT 10,185,590,052; EPS EGP 24.69 on 412,500,000 shares",
    "Aluminium Company of Egypt, audited financial statements for the year ended "
    "30-Jun-2025, signed by ACC/ Alaa Abd Ellatif Ahmed, ACC/ Nasser Thabet Abd Elaal "
    "and CEO Dr.Eng/ Mahmoud Agour, prepared 13-Aug-2025",
    CO, "2025-08-13",
    url="https://www.mistnews.com/mistsat/companies/mezanyat/en/334089_1_0_2025.pdf",
    detail="Read off 200-400 dpi renders; zero text layer. Every column re-added: the "
           "income statement chain from gross profit through other revenues "
           "(1,058,290,771), administrative expenses (161,546,996), burdens and losses "
           "(133,010,182), net provisions (2,007,136,407), other expenses (28,639,714) "
           "and financial expenses (15,303,274) reproduces the printed profit before "
           "tax of 13,671,756,576 EXACTLY.",
    is_fs_data=True, fiscal_period="FY2025",
    model_impact="The base year. Anchors revenue, the cost stack and the margin the "
                 "forecast starts from.")

f_bs25 = R.add(
    Ring.COMPANY, "official financial statements", FindingClass.D,
    "FY2025 audited balance sheet at 30-Jun-2025: total assets EGP 29,337,064,428 "
    "(non-current 4,861,700,926 + current 24,475,363,502); total equity 22,373,758,710; "
    "non-current liabilities 181,197,914 (all deferred tax); current liabilities "
    "6,782,107,804. Issued and paid-in capital EGP 1,650,000,000. TOTAL GROSS DEBT IS "
    "EGP 37,688,150 — an overdraft of 7,927,970 and credit facilities of 29,760,180 — "
    "against cash and current accounts of EGP 5,515,544,207",
    "Aluminium Company of Egypt, audited statement of financial position at 30-Jun-2025, "
    "printed pages 1-4",
    CO, "2025-08-13",
    detail="Balances to the pound in both columns: 22,373,758,710 + 181,197,914 + "
           "6,782,107,804 = 29,337,064,428 = 4,861,700,926 + 24,475,363,502. FY2024 "
           "comparative closes identically at 20,492,508,818.",
    is_fs_data=True, fiscal_period="FY2025",
    model_impact="Fixes the capital structure as NET CASH by a wide margin: gross debt "
                 "is 0.17% of equity. WACC is effectively all-equity, the EV-to-equity "
                 "bridge ADDS net cash, and treasury income is excluded from FCFF to "
                 "avoid counting the cash twice.")

f_cf25 = R.add(
    Ring.COMPANY, "official financial statements", FindingClass.D,
    "FY2025 audited cash flow: operating EGP 4,661,412,352; investing +1,658,492,690 "
    "(credit interest 601,244,062 and treasury-bill redemptions 2,329,950,096 less "
    "CAPEX OF EGP 1,272,701,468); financing -3,345,045,835, all dividends; FX effect "
    "+220,815,782; closing cash 5,477,856,051. FY2024 capex was EGP 427,827,676, so "
    "capex nearly TRIPLED",
    "Aluminium Company of Egypt, audited statement of cash flows for the year ended "
    "30-Jun-2025, printed page 10",
    CO, "2025-08-13",
    detail="Every subtotal re-added and exact. Closing cash 5,477,856,051 differs from "
           "balance-sheet cash 5,515,544,207 by precisely 37,688,150, the overdraft "
           "plus credit facilities — the cash-flow statement is on a net-of-overdraft "
           "basis and is internally consistent.",
    is_fs_data=True, fiscal_period="FY2025",
    model_impact="Gives the actual capex base and the dividend outflow, and shows "
                 "operating cash at only 46% of net profit in FY2025 — a working-"
                 "capital drag that must be modelled rather than assumed away.")

f_fs24 = R.add(
    Ring.COMPANY, "official financial statements", FindingClass.D,
    "FY2024 audited (1-Jul-2023 to 30-Jun-2024): total income from operations EGP "
    "32,815,674,548; total cost 20,180,760,065; GROSS PROFIT 12,634,914,483 (38.50%); "
    "profit before tax 12,024,550,165; NET PROFIT 9,324,234,387. Total assets "
    "20,492,508,818, equity 15,566,403,860, gross debt EGP 5,759,164",
    "Aluminium Company of Egypt, audited financial statements for the year ended "
    "30-Jun-2024, marked 'after modification', dated 13-Sep-2024 and filed 30-Sep-2024",
    CO, "2024-09-13",
    url="https://www.mistnews.com/mistsat/companies/mezanyat/en/334089_1_0_2024.pdf",
    detail="The filing is stamped 'after modification' on every page — it is a revised "
           "issue, and a build should say so rather than present it as the original.",
    is_fs_data=True, fiscal_period="FY2024",
    model_impact="The peak-margin year, and the comparative base for FY2025. FY2024's "
                 "38.5% gross margin is the high-water mark the forecast must NOT "
                 "assume returns.")

f_fs23 = R.add(
    Ring.COMPANY, "official financial statements", FindingClass.D,
    "FY2023 (1-Jul-2022 to 30-Jun-2023), from the audited comparative column of the "
    "FY2024 filing: net sales EGP 22,045,631,557 plus 295,065 = total income from "
    "operations 22,045,926,622; cost of goods sold 14,865,774,151 and distribution/"
    "selling 136,957,172 = total cost 15,002,731,323; GROSS PROFIT 7,043,195,299 "
    "(31.95%); profit before tax 12,024,550,165 in FY2024 versus NET PROFIT of EGP "
    "3,691,336,550 in FY2023",
    "Aluminium Company of Egypt, audited financial statements for the year ended "
    "30-Jun-2024, comparative column at 30-Jun-2023",
    CO, "2024-09-13",
    detail="THIS IS THE PAGE THAT CAUGHT TWO GLYPH ERRORS. At 100 dpi the two cost "
           "lines read 14,866,774,151 and 136,967,172 and failed to foot by 1,010,000 "
           "against the printed total. Re-read at 400 dpi they are 14,865,774,151 and "
           "136,957,172 and foot exactly, and the printed gross profit of 7,043,195,299 "
           "confirms it independently. Arithmetic was the arbiter, not the render.",
    is_fs_data=True, fiscal_period="FY2023",
    model_impact="The third historical year and the pre-devaluation margin reference: "
                 "31.95% in FY2023 versus 38.50% in FY2024 shows how much of the FY2024 "
                 "margin came from the EGP float rather than from operations.")

f_vol = R.add(
    Ring.COMPANY, "official financial statements", FindingClass.D,
    "THE PHYSICAL DENOMINATOR. Note 20 of the FY2025 audited statements, on revenue "
    "recognition: 'For the period from 1/07/2024 till 30/06/2025, sales quantity "
    "reached (295 thousand tons amounting to EGP 43184 million).' That implies a "
    "realised price of EGP 146,386 PER TONNE for FY2025",
    "Aluminium Company of Egypt, audited financial statements FY2025, note (20) "
    "Recognition of Revenues, printed note page 17",
    CO, "2025-08-13",
    detail="EXTRACTION ROUTE RECORDED BECAUSE THE TWO ROUTES DISAGREED. The 100 dpi "
           "contact-sheet render reads '290 thousand tons'; independent re-renders at "
           "260 dpi and 600 dpi both read '295 thousand tons'. No printed subtotal can "
           "arbitrate a figure written in words, so the highest-resolution read governs "
           "and the low-resolution read is recorded beside it. The EGP 43,184 million "
           "in the same sentence ties to the printed net sales of 43,182,999,188, which "
           "confirms the sentence is about the same period and basis.",
    is_fs_data=True, fiscal_period="FY2025",
    model_impact="DRIVER UNLOCK, and the one that makes a smelter model possible at "
                 "all. Revenue becomes tonnes x EGP/tonne. Volume is projected against "
                 "the 320,000 tpa nameplate and the idle-cell count; price is projected "
                 "against LME. Growth is projected in BOTH legs separately, never as a "
                 "single revenue rate.")

f_cells = R.add(
    Ring.COMPANY, "official financial statements", FindingClass.D,
    "IDLE CAPACITY, DISCLOSED. The FY2025 audited note on temporarily-stopped fixed "
    "assets states 'The number of cells stopped 14 cells', and separately that "
    "'Electricity Plant: All parts of the generation plant were abandoned in the "
    "abandonment session held on 17/3/2022. Only building remained'",
    "Aluminium Company of Egypt, audited financial statements FY2025, 'Book Value of "
    "the Temporarily-stopped Fixed Assets', printed note page 2",
    CO, "2025-08-13",
    detail="Read at 300 dpi. The same note names a 'Line 7 Project' and its consultant "
           "'Pictel Company' — the seventh potline, i.e. the expansion referred to in "
           "F21, appears in the audited statements and not only in the press release.",
    is_fs_data=True, fiscal_period="FY2025",
    model_impact="Two hard consequences. First, 14 idle cells set the top of the "
                 "utilisation-recovery leg without any new capital. Second, and much "
                 "larger: with its own generation plant abandoned in 2022, EGAL buys "
                 "100% of its electricity from the grid at the administered tariff "
                 "(F03) with NO self-generation hedge whatsoever. The tariff is a pure "
                 "pass-through into cost and must be modelled as one.")

f_prov = R.add(
    Ring.COMPANY, "official financial statements", FindingClass.S,
    "Provisions are large, volatile and back-loaded. FY2025 charged EGP 2,018,015,677 "
    "net of 10,879,270 released, against EGP 305,130,514 in FY2024 — a 6.6x jump. The "
    "trade-receivable bad-debt provision alone was fed EGP 500,631,517, taking it from "
    "97,997,204 to 598,628,721. A 'production stoppage reserve' of EGP 3,803,487,434 "
    "sits inside other reserves at 30-Jun-2025 and had risen to EGP 6,349,884,947 by "
    "31-Mar-2026",
    "Aluminium Company of Egypt, audited FY2025 provisions note and 'Analysis acc/ "
    "Other reserves'; 9M-FY2026 filing, same schedules",
    CO, "2025-08-13",
    detail="The provisions note foots against the income statement exactly: the "
           "movement schedule's feed of 2,022,173,310 less the 4,157,633 shown as 'use' "
           "gives the 2,018,015,677 charged. Almost all of the FY2025 charge fell in "
           "Q4: 9M-FY2025 net provisions were only EGP 35m against EGP 2,007m for the "
           "full year, which is why Q4-FY2025 net profit was roughly EGP 292m on "
           "revenue of about EGP 11.1bn.",
    is_fs_data=True, fiscal_period="FY2025",
    model_impact="Forces a NORMALISED earnings lens rather than a trailing one, and "
                 "warns against annualising any single EGAL quarter. The receivable "
                 "provision build is also a working-capital quality signal that belongs "
                 "in the cash-conversion driver.")

f_q1 = R.add(
    Ring.COMPANY, "official financial statements", FindingClass.B,
    "THE QUARTER THAT CONTRADICTS THE MARGIN PATH. Q1-FY2026 (1-Jul-2025 to "
    "30-Sep-2025): net sales EGP 11,326,397,162, essentially FLAT on Q1-FY2025's "
    "11,334,384,628 (-0.07%), while cost of goods sold rose 28.9% from 6,104,521,131 to "
    "7,865,843,513. Gross profit FELL 34.1% to 3,398,262,119. GROSS MARGIN 30.00% "
    "AGAINST 45.48% A YEAR EARLIER. Net profit for the quarter EGP 2,415,725,215",
    "Aluminium Company of Egypt, reviewed financial statements for the period "
    "1-Jul-2025 to 30-Sep-2025, filed to EGX 08-Dec-2025 under cover of a letter signed "
    "by the Investor Relations Officer, Acc. Esmat Safwat Mohammad",
    CO, "2025-12-08",
    url="https://www.mistnews.com/mistsat/companies/mezanyat/en/334089_4_0_2026.pdf",
    detail="Both cost columns re-added and exact: 7,865,843,513 + 62,291,530 = "
           "7,928,135,043 and 11,326,397,162 - 7,928,135,043 = 3,398,262,119. The "
           "mechanism is legible in the tariff table: Q1-FY2025 ran two of its three "
           "months at 126.9 Pt/kWh and one at 160.0, while Q1-FY2026 ran all three at "
           "160.0 — roughly a 21% year-on-year rise in the power price on flat volume. "
           "The FX line also flipped, from a gain of 60,010,156 to a loss of "
           "274,775,392.",
    is_fs_data=True, fiscal_period="Q1-2026",
    model_impact="BASE CHANGER for the margin path, and the reason this sweep exists. A "
                 "forecast built off FY2025's 34.64% gross margin without reading this "
                 "quarter would be starting 4.6 points too high. Margin must be an "
                 "OUTPUT of the tonnes x price less power-cost build, and the build must "
                 "reproduce 30.00% for Q1-FY2026 before it is allowed to forecast "
                 "anything. Dual-frame the recovery: Q2+Q3 FY2026 recovered to 34.96% "
                 "(derived: 9M less Q1), so Q1 was a trough, not a new level.")

f_9m = R.add(
    Ring.COMPANY, "official financial statements", FindingClass.D,
    "9M-FY2026 (1-Jul-2025 to 31-Mar-2026): total income from operations EGP "
    "36,731,184,608 (net sales 36,731,173,811 plus 10,797); total cost 24,452,389,078 "
    "(COGS 24,132,815,358, distribution/selling 319,573,720); GROSS PROFIT "
    "12,278,795,530, a margin of 33.43% against 37.78% in 9M-FY2025; net profit "
    "10,447,306,397. Balance sheet at 31-Mar-2026: total assets EGP 36,939m, equity "
    "28,849m, non-current liabilities 154m, current liabilities 7,936m",
    "Aluminium Company of Egypt, reviewed financial statements and Board of Directors' "
    "Report for the period 1-Jul-2025 to 31-Mar-2026",
    CO, "2026-06-21",
    url="https://www.mistnews.com/mistsat/companies/mezanyat/en/334089_9_0_2026.pdf",
    detail="Re-added exactly: 24,132,815,358 + 319,573,720 = 24,452,389,078 and "
           "36,731,184,608 - 24,452,389,078 = 12,278,795,530. The balance sheet closes: "
           "28,849 + 154 + 7,936 = 36,939, and the 30-Jun-2025 comparative of 29,337 "
           "ties to the audited FY2025 total of 29,337,064,428.",
    is_fs_data=True, fiscal_period="9M-2026",
    model_impact="The most recent full income statement available. Sets the FY2026 "
                 "run-rate the forecast starts from, and shows the margin STABILISING "
                 "around 33-35% rather than continuing to fall after Q1.")

# ---- IR communications (COMPANY_IR) ---------------------------------
f_bod9m = R.add(
    Ring.COMPANY, "IR communications (calls, presentations, releases)", FindingClass.D,
    "THE RESULTS RELEASE, WITH THE ANCHORS THE STATEMENTS DO NOT CARRY. The Board of "
    "Directors' Report for 9M-FY2026 gives budget-versus-actual and, for the first "
    "time, the GEOGRAPHIC SPLIT: total sales EGP 36,753m against a budget of 36,577m "
    "(100.5%); LOCAL SALES 14,651m against a budget of 12,215m (120%); EXPORTS 22,102m "
    "against a budget of 24,362m (90.7%). Profit before tax 13,232m against a budget of "
    "13,267m (99.7%); profit after tax 10,447m against 10,287m (101.5%)",
    "Aluminium Company of Egypt, Board of Directors' Report on the Company's Business "
    "for the period July 2025 to March 2026, section 'Fifth: Other Indicators', signed "
    "by Executive Managing Director Dr. Engineer/ Mahmoud Abdel Aleem Ajour",
    IR, "2026-06-21",
    detail="Read at 300 dpi and re-added: 14,651 + 22,102 = 36,753, and each "
           "achievement ratio reproduces (14,651/12,215 = 119.9%, 22,102/24,362 = "
           "90.7%, 36,753/36,577 = 100.5%). Note the EGP 22m gap between the 'total "
           "sales' indicator of 36,753 and the income statement's 36,731 — two "
           "different company definitions, both carried, neither reconciled away. The "
           "same report states the company's own explanation of the result: gross "
           "profit rose 'attributed to higher sales volumes and an increase in average "
           "selling prices', and net income rose 5.6% 'attributed to higher sales and "
           "foreign exchange gains'.",
    fiscal_period="9M-2026",
    model_impact="DRIVER UNLOCK for the revenue split. Exports are 60.1% of sales and "
                 "local 39.9%, so the FX and CBAM exposures are sized off a disclosed "
                 "number rather than an assumption. It also supplies the company's OWN "
                 "attribution — volume up AND price up — which the volume x price build "
                 "must reproduce. A NEWER release supersedes this one: the FY2026 "
                 "full-year indicators of 12-Aug-2026 (F44) are not obtainable, so this "
                 "9M release remains the governing operating anchor and the study must "
                 "say so.")

f_energy = R.add(
    Ring.COMPANY, "IR communications (calls, presentations, releases)", FindingClass.D,
    "THE ELECTRICITY BILL, IN KILOWATT-HOURS. The company's own Sustainability Report "
    "discloses Average Energy Use for 2022-2023: ELECTRICITY 4,703,545,513 kWh per year "
    "across industrial processes, the farm, the workers' city, administrative offices "
    "and Safaga port; natural gas 32,228,550 units for industrial processes; petrol "
    "84,199 L for vehicles. It states plainly that 'the largest energy consumption in "
    "the value chain is accounted for by the production of primary aluminium'",
    "Egyptalum Sustainability Report 2022-2023, section 6-2 Energy, page 42",
    IR, "2024-06-30",
    url="https://egyptalum.com.eg/Files/Sustainability/"
        "Sustainability__Report__for_Egyptalum_2022-2023_-_REV01_(4)_Final_version.pdf",
    detail="Confirmed by BOTH routes: the PDF text layer and an independent 200 dpi "
           "pixel read agree digit for digit on 4,703,545,513. Against the 286,412 t of "
           "production disclosed on page 46 that is 16,422 kWh per tonne SITE-WIDE — "
           "which includes the rolling mill, the extrusion plant, the anode plant, the "
           "calciner, the farm, the workers' city and the port, so the smelter-only "
           "figure is lower and is NOT disclosed. Note also the vintage mismatch: the "
           "electricity figure is a 2022-2023 average while the production figure is "
           "the 2022 base year.",
    model_impact="DRIVER UNLOCK for the cost side, and the reason this company can be "
                 "modelled bottom-up at all. Power cost = kWh/t x EgyptERA tariff x "
                 "tonnes. At 16,422 kWh/t and the April-2026 tariff of 189.0 Pt/kWh "
                 "that is about EGP 31,000 of power per tonne against a FY2025 realised "
                 "price of EGP 146,386 — roughly a fifth of revenue from one "
                 "administered input. FLAG THE GAP explicitly in the study: the split "
                 "between smelter and downstream kWh is not disclosed, so the build is "
                 "at SITE level and says so.")

f_kanak = R.add(
    Ring.COMPANY, "IR communications (calls, presentations, releases)", FindingClass.D,
    "A DISCLOSED ENERGY-INTENSITY DELTA. Egyptalum has partnered with the Swiss company "
    "Kanak on an energy-saving project for aluminium reduction cells aiming to cut "
    "consumption by 500 kWh PER TONNE of aluminium, using copper inserts in collector "
    "bars plus insulation and lining improvements. Seven trial pots show promising "
    "results; final evaluation is still under way before roll-out across all cells. A "
    "waste-heat-recovery project on the reduction cells is 'still under negotiation and "
    "study'",
    "Egyptalum Sustainability Report 2022-2023, section 6-2-1 Energy Saving Projects",
    IR, "2024-06-30",
    model_impact="DRIVER UNLOCK for the efficiency leg. 500 kWh/t is about 3% of the "
                 "16,422 kWh/t site figure, worth roughly EGP 945/t at the April-2026 "
                 "tariff. Model it as a SCENARIO, not the base: seven trial pots is not "
                 "a commissioned project, and the company says so. Waste-heat recovery "
                 "is excluded entirely — 'under negotiation and study' is not a plan.")

f_ghg = R.add(
    Ring.COMPANY, "IR communications (calls, presentations, releases)", FindingClass.S,
    "CARBON INTENSITY, AND AN ARITHMETIC BREAK IN THE COMPANY'S OWN TABLE. Base year "
    "2022: Scope 1 586,611.00 tCO2e, Scope 2 2,328,257.25, Scope 3 1,040,377.95, Total "
    "Emissions 3,955,246.20, TOTAL PRODUCTION 286,412.00 t Al, GHG Intensity 13.182 "
    "tCO2e/tAl. The company plots itself against a 5.2 tCO2e/t sectoral threshold",
    "Egyptalum Sustainability Report 2022-2023, section 6-2-3, page 46",
    IR, "2024-06-30",
    detail="THE PAGE DOES NOT FOOT AND IS RECORDED, NOT REPAIRED. 3,955,246.20 / "
           "286,412.00 = 13.810, not the printed 13.182; the printed intensity implies "
           "a denominator of 300,049 t. The scope lines themselves DO foot (586,611.00 "
           "+ 2,328,257.25 + 1,040,377.95 = 3,955,246.20) and page 44 of the same "
           "report prints the total as 3,955,246.29, nine hundredths different again. "
           "Both extraction routes — text layer and 200 dpi pixels — agree on every "
           "digit, so this is the document's own inconsistency. The 286,412 t "
           "production figure is the more primitive datum and is twice confirmed; the "
           "13.182 intensity is not reproducible from it.",
    model_impact="Sizes the CBAM exposure in F04 against the disclosed export share in "
                 "F26. Carry the production figure; quote the intensity only with the "
                 "break disclosed beside it. Do not use 13.182 to derive tonnes.")

f_epd = R.add(
    Ring.COMPANY, "IR communications (calls, presentations, releases)", FindingClass.C,
    "Egyptalum publishes an Environmental Product Declaration for one kilogram of "
    "aluminium ingot, verified against PCR 2022:08 on 2022 production data using "
    "SimaPro 9.4 and ecoinvent 3.8. Core (A2-A3) primary energy is 132 MJ/kg "
    "non-renewable plus 5.48 MJ/kg renewable; upstream (A1) adds 92.7 and 11.4",
    "Egyptalum, Environmental Product Declaration for Aluminium Ingot",
    IR, "2024-06-30",
    url="https://egyptalum.com.eg/Files/Sustainability/EPD%20for%20EGYPTALUM_"
        "Aluminum%20Ingot(1).pdf",
    detail="Primary energy is not metered electricity — converting it to kWh at the "
           "gate requires a grid-efficiency assumption the EPD does not state. Recorded "
           "as a cross-check on the order of magnitude of F28, NOT as a second "
           "independent kWh/t figure.",
    model_impact="")

# ---- strategic plans & guidance -------------------------------------
f_traf = R.add(
    Ring.COMPANY, "strategic plans & guidance", FindingClass.B,
    "TRAFIGURA. On 6 May 2026 a strategic partnership agreement was signed with "
    "Trafigura setting out 'a study for a project to increase global production "
    "capacity between Egypt Aluminum Company and Trafigura, to prepare the existing "
    "plant in Naga Hammadi for an additional production capacity of 300,000 TONS of "
    "aluminum metal annually. The estimated initial investment is $900 million.' The "
    "company's own website describes the counterparty as Trafigura Limited and the "
    "purpose as 'new expansions at the aluminum complex in Naga Hammadi, with an "
    "investment cost of up to $900 million'",
    "Egypt Aluminum (EGAL.CA) statement to the Egyptian Exchange, 06-May-2026, as "
    "served on the company's own IR portal; Egyptalum company news item 1069",
    CO, "2026-05-06",
    detail="NAME MISMATCH RECORDED RATHER THAN RESOLVED: the EGX statement says "
           "'Trafigura International' and the company's own website says 'Trafigura "
           "Limited'. The 21-Jun-2026 release on 'the latest updates of foil production "
           "project' is a SECOND, separate project. A further release followed on "
           "21-May-2026 and AGM minutes were notarised on 10-May-2026.",
    fiscal_period="FY2026",
    model_impact="BASE CHANGER, and it must be DUAL-FRAMED, never glided. +300,000 tpa "
                 "would roughly DOUBLE a 320,000 tpa plant. But the signed document is "
                 "'a study for a project' — pre-FID, with no announced financing close, "
                 "no start date and no completion date. Model the base case WITHOUT it "
                 "and show the expansion as a separate, explicitly dated scenario with "
                 "its own USD 900m capital cost and its own power requirement, which at "
                 "16,422 kWh/t would be roughly 4.9 TWh a year of ADDITIONAL "
                 "administered-tariff electricity that nobody has yet contracted.")

f_wire = R.add(
    Ring.COMPANY, "strategic plans & guidance", FindingClass.B,
    "A COMMISSIONED CAPACITY ADDITION, AS OPPOSED TO A STUDY. The Prime Minister "
    "inspected a NEW WIRE PRODUCTION LINE at Egypt Aluminium 'with an annual capacity "
    "of 60,000 tons' which 'has recently begun operations'. The Minister of the Public "
    "Business Sector, Eng. Mohamed Shimi, stated that the new line DOUBLES the "
    "company's aluminium wire production to 120,000 tonnes per year",
    "Egyptalum company news item 1068, 'The Prime Minister inspects the new production "
    "line for wire at Egypt Aluminum Company'",
    CO, "2026-01-01",
    detail="60,000 tpa new on a 60,000 tpa existing base gives the 120,000 tpa the "
           "Minister quotes — the two company statements are internally consistent. "
           "Unlike Trafigura this line is BUILT and RUNNING, so it belongs in the base "
           "case, not in a scenario.",
    fiscal_period="FY2026",
    model_impact="BASE CHANGER in the base case, and a MIX effect rather than a primary-"
                 "metal volume effect: wire rod is a higher-value cast-house product, so "
                 "it raises realised EGP per tonne without adding smelter tonnes. Model "
                 "it in the price leg as a mix uplift and say so, rather than adding "
                 "60 kt to primary volume.")

f_solar = R.add(
    Ring.COMPANY, "strategic plans & guidance", FindingClass.S,
    "THE POWER HEDGE. Egyptalum has signed an agreement with the Norwegian company "
    "Scatec to build a 1 GIGAWATT solar power station supplying the Nag Hammadi "
    "industrial complex, in two 500 MW phases, the first expected within 18 months of "
    "signing and the second within 24 months, with Scatec handling development, "
    "financing, equipment and studies",
    "Egyptalum Sustainability Report 2022-2023, section 3-1 On-site Solar panels",
    CO, "2024-06-30",
    detail="The report also claims 'the use of solar energy in aluminum production at "
           "Aluminum Company of Egypt represents 33% of the energy used', which sits "
           "oddly beside the future tense of the Scatec agreement in the very next "
           "paragraph; the claim is recorded but NOT used. External reporting places "
           "the Scatec deal at 1.1 GW signed March 2025 with a 100 MW/200 MWh battery, "
           "and the African Development Bank approving up to USD 66m for a 500 MW first "
           "phase (Dandara) plus 100 MWh of storage — that external detail is context, "
           "not a company figure, and is not carried as one.",
    fiscal_period="FY2026",
    model_impact="The only structural answer to F03 that EGAL controls. A 1 GW solar "
                 "plant at, say, a 25% capacity factor generates roughly 2.2 TWh a year "
                 "against site consumption of 4.7 TWh — so it could displace on the "
                 "order of half the grid bill IF the PPA price is below the tariff. THE "
                 "PPA PRICE IS NOT DISCLOSED (F45), so this is modelled as a SCENARIO "
                 "on the power-cost driver with the PPA tariff as the swing variable, "
                 "never as a base-case saving.")

f_plan = R.add(
    Ring.COMPANY, "strategic plans & guidance", FindingClass.D,
    "A LINE-ITEM CAPITAL BUDGET, WHICH IS RARE AND USABLE. The company's Investment "
    "Projects Plan for FY2024-2025, published on the IR portal, totals EGP 2,061,018 "
    "thousand after amendment: production cells (major overhauls of 144 CELLS) and gas "
    "purification filters 1,158,040; a 50,000-tonne alumina storage silo at Nag Hammadi "
    "389,616; rectifier development, replacing the Russian rectification transformers "
    "and exchangers 152,660; transport and Safaga port 166,841; utilities including the "
    "industrial-gas plant and air compressor no. 3 138,750; workshops 14,513; rod plant "
    "19,525; extrusion plant 7,723; foundry 3,350; auxiliary services 10,000",
    "Egyptalum, Investment Projects Plan for the Fiscal Year 2024-2025, from the IR "
    "portal's Summary of Operations page",
    CO, "2024-07-01",
    url="https://www.mistnews.com/ir_admintool/reports/"
        "Investment%20Projects%20Plan%20Year%202024-2025.pdf",
    detail="Re-added and exact: the ten line items sum to 2,061,018. THREE COMPANY-"
           "OFFICIAL NUMBERS EXIST FOR THE SAME YEAR'S CAPEX AND THEY DO NOT AGREE — "
           "this plan says EGP 2,061m after amendment; note (23) of the FY2025 audited "
           "statements says 'The investment budget for FY 2024/2025 amounts to EGP 1051 "
           "million' (verified at 400 dpi, it does read 1051); and the audited cash-flow "
           "statement shows EGP 1,272,701,468 actually paid. All three are recorded. "
           "The FY2023-2024 plan is also published; the FY2025-2026 plan returns HTTP "
           "404 and does not exist on the portal.",
    fiscal_period="FY2025",
    model_impact="DRIVER UNLOCK for capex at the finest level any Egyptian issuer in "
                 "this book has offered: cell overhauls, a silo, rectifier transformers. "
                 "Capex is built BOTTOM-UP off this cycle — the 144-cell overhaul "
                 "programme against a ~6-year pot life sets a recurring maintenance "
                 "rhythm — and is NOT set as a percentage of revenue. The budget-versus-"
                 "actual gap is carried as the execution-slippage factor, sized off the "
                 "disclosed numbers rather than assumed.")

# ---- regular disclosures --------------------------------------------
f_cap = R.add(
    Ring.COMPANY, "regular disclosures", FindingClass.D,
    "INSTALLED CAPACITY, FROM THE COMPANY'S OWN PLANT PAGES. Primary smelter 300,000 to "
    "320,000 tpa on prebake technology; 'In April 2010, all production lines were "
    "rehabilitated and upgraded to pre-baked cells to reach 320,000 tons annually'; six "
    "potlines (first two October 1975, five by July 1983, prebake line 6 October 1997). "
    "Cast houses 320,000 t/yr of slabs, billets, foundry ingots, 99.7/99.8 ingots, "
    "T-bars and 9/9.5 mm wire rod. Rolling mill up to 108,000 tpa hot and 30,000 tpa "
    "cold. Extrusion 12,000 t/yr on two presses. Prebaked anode plant 172,000 tpa "
    "(design). Calcined coke plant 140,000 tpa (design)",
    "Egyptalum website, Smelter / Company Profile / Cast Houses / Rolling Mill / "
    "Extrusion Capacity / Anode Blocks / Calcined Coke pages",
    CO, "2026-09-09",
    url="https://egyptalum.com.eg/staticPages.aspx?LId=40&PID=25",
    detail="The 50th-anniversary company news item independently repeats 'an annual "
           "production capacity exceeding 320,000 tonnes'. The company also states its "
           "siting logic in its own words: Nag Hammadi was chosen for 'the nearness of "
           "the site to the High Dam Power Transformers Station (500 kv)' and its first "
           "stated corporate objective is 'Exploitation of part of the hydroelectric "
           "power produced by the High Dam on a regular and economical basis'. The "
           "company was built as a power-conversion asset and describes itself that way.",
    model_impact="DRIVER UNLOCK for the volume ceiling. 320,000 tpa nameplate against "
                 "295,000 t of FY2025 sales is ~92% utilisation, and against 286,412 t "
                 "of CY2022 production ~90%. The volume leg is therefore a UTILISATION "
                 "path bounded at 320 kt, not a growth rate — there is very little room "
                 "to grow tonnes without the Line 7 / Trafigura capital in F21.")

f_disc = R.add(
    Ring.COMPANY, "regular disclosures", FindingClass.C,
    "The filing rhythm is complete and regular. The IR portal's Financial Statements "
    "shelf carries Annual FY2024 and FY2025, Quarter and 9-Months for 2024, 2025 and "
    "2026, and Semi-annual 2025. Its Disclosure Reports shelf carries the board-and-"
    "shareholder-structure report for every quarter end from 31-Mar-2019 to 30-Jun-2026 "
    "without a gap. Its Audit Reports shelf runs from 31-Mar-2013 to 30-Sep-2024",
    "Egyptalum investor-relations portal, financial.aspx id=1 / id=2 / id=3",
    CO, "2026-09-09",
    model_impact="")

f_emp = R.add(
    Ring.COMPANY, "regular disclosures", FindingClass.D,
    "OPERATING SCALE AND FOOTPRINT AT 31-MAR-2026: 4,802 employees, of whom 4,794 are "
    "permanent and 8 on contract. Donations over 9M-FY2026 EGP 3,122,613. Land held: "
    "book value about EGP 4.5m over roughly 3,000 acres. Cash-flow narrative: operating "
    "surplus about EGP 8,517m against EGP 4,906m in the prior-year period; investing "
    "formation EGP 2,151m; financing outflow EGP 2,735m; FX gain EGP 682m against EGP "
    "217m",
    "Aluminium Company of Egypt, Board of Directors' Report for July 2025 to March "
    "2026, sections 'Third: Cash Flow Statements' and 'Fourth: Other Information'",
    CO, "2026-06-21",
    detail="Read at 260 dpi. FY2025 cash wages in the administrative-expense note were "
           "EGP 74,156 thousand of a total EGP 160,719 thousand of administrative cost, "
           "and the note foots exactly (12,385 + 95,935 + 52,399 = 160,719), which ties "
           "to the printed 'other administrative expenses' of 160,720,351.",
    fiscal_period="9M-2026",
    model_impact="DRIVER UNLOCK for the labour cost leg: 4,802 heads is a hard "
                 "denominator for a cost-per-employee build, and it also sizes the "
                 "social/political cost of any capacity rationalisation at a state-owned "
                 "Upper Egypt employer — which is why the 14 idle cells in F14 should "
                 "not be assumed to be restarted or scrapped on economics alone.")

# ---- ownership / stake changes --------------------------------------
f_own = R.add(
    Ring.COMPANY, "ownership / stake changes (named-transaction rule)", FindingClass.D,
    "THE FLOAT, FROM THE COMPANY'S OWN FILING, NAMED TRANSACTION BY NAMED TRANSACTION. "
    "At 30-Jun-2026: Metallurgical Industries Company S.A.E. holds 370,578,435 shares = "
    "89.83720%; El Nasr Mining Company, a related group of Metallurgical Industries, "
    "holds 9,075,000 = 2.200%; together 379,653,435 = 92.03720%. The National Social "
    "Insurance Authority holds a further 20,722,544 = 5.023647% across five funds. The "
    "company's own free-float line reads: total shares held for retention purposes "
    "379,655,012 = 92.03758% (7 holders), TOTAL FREELY TRADED SHARES 32,844,988 = "
    "7.96242% across 20,719 holders",
    "Aluminium Company of Egypt, Disclosure Report on the Board of Directors and "
    "Shareholder Structure pursuant to Article 30 of the Listing Rules, for the period "
    "ended 30-Jun-2026",
    CO, "2026-07-22",
    url="https://www.mistnews.com/mistsat/companies/announcement/"
        "%D9%85%D8%B5%D8%B1%20%D9%84%D9%84%D8%A7%D9%84%D9%88%D9%85%D9%86%D9%8A%D9%88"
        "%D9%85%203062026.pdf",
    detail="Every percentage re-derived against 412,500,000 shares and exact to six "
           "decimals: 370,578,435/412,500,000 = 89.8372%, 379,653,435 = 92.0372%, "
           "20,722,544 = 5.023647%, 412,500,000 - 379,655,012 = 32,844,988 = 7.96242%. "
           "NO STAKE CHANGE HAS OCCURRED: the same 370,578,435 and 9,075,000 appear in "
           "the 30-Jun-2022 disclosure. What HAS changed is the number of holders — "
           "2,750 at 30-Jun-2022, 14,497 at 31-Mar-2026, 20,726 at 30-Jun-2026, a 43% "
           "rise in one quarter.",
    fiscal_period="FY2026",
    model_impact="Two consequences the build must carry. First, the free float is "
                 "7.96% of a EGP 155bn market capitalisation, roughly EGP 12.3bn, and "
                 "if the state insurance funds are also treated as non-trading it falls "
                 "to 2.94%. That is a liquidity and control discount that must be "
                 "stated, and it makes the observed price a thin-float price. Second, "
                 "any minority-protection or privatisation scenario is a discrete event "
                 "with a named counterparty, never an assumed re-rating.")

# ---- management & capital actions -----------------------------------
f_div = R.add(
    Ring.COMPANY, "management & capital actions", FindingClass.D,
    "THE DIVIDEND RECORD, FROM THE COMPANY'S OWN IR REGISTER. Coupon 23: EGP 8.00 per "
    "share, maturity 13-Oct-2025, paid 16-Oct-2025 through MCDR (out of FY2025). Coupon "
    "22: EGP 7.000, 21-Nov-2024 (FY2024). Coupon 21: EGP 6.500, 23-Nov-2023 (FY2023). "
    "Coupon 20: EGP 4.4999878787, 21-Nov-2022 (FY2022). Earlier: 0.75 (2019), 3.000 "
    "(2018), 7.000 (May-2018), 3.000 (2017), 1.100 (2016), 1.400 (2015), 1.00 (2012)",
    "Egyptalum investor-relations portal, Economic Agenda / Dividends register",
    CO, "2025-10-16",
    detail="EGP 8.00 on 412,500,000 shares is EGP 3,300m, against total dividends "
           "payable of EGP 3,367,817,150 on the 30-Sep-2025 balance sheet and EGP "
           "3,345,045,835 actually paid in FY2025 — the gap is the employees' and "
           "board's statutory share. The FY2025 audited statutes note sets those out: "
           "at least 20% of net profit to legal reserve until it equals half of capital; "
           "personnel entitled to 10-12% of distributable profit; board remuneration "
           "capped at 10% of annual distributable profit less 5% of paid-up capital.",
    fiscal_period="FY2025",
    model_impact="DRIVER UNLOCK for the payout and for the equity bridge. Payout is "
                 "built off the disclosed statutory waterfall and the actual coupon "
                 "history, not off a target ratio. DPS has compounded 4.50 -> 6.50 -> "
                 "7.00 -> 8.00 across FY2022-FY2025, a 21% CAGR while EPS grew far "
                 "faster, so the payout RATIO has been falling and cash has been piling "
                 "up on the balance sheet — that accumulation is the equity bridge.")

f_gov = R.add(
    Ring.COMPANY, "management & capital actions", FindingClass.C,
    "Share capital unchanged: issued and paid-in EGP 1,650,000,000 at EGP 4.00 par = "
    "412,500,000 shares, authorised EGP 5,000,000,000, listed on EGX since 29-Jul-1997. "
    "The FY2025 audited statements confirm 412.5 million shares. Chief Executive "
    "Officer and Executive Managing Director: Dr. Eng. Mahmoud Abdel Aleem Agour. "
    "Investor Relations Officer: Acc. Esmat Safwat Mohammad, investrel@egyptalum.com.eg. "
    "Ordinary General Meetings were held on 18-Sep-2025 and 27-Apr-2026, the latter "
    "with minutes notarised 10-May-2026",
    "Egyptalum IR portal company data and General Assembly register; Disclosure Report "
    "at 30-Jun-2026; FY2025 audited statements note (16)",
    CO, "2026-09-09",
    detail="EGAL was established 2 July 1976 under Minister of Industry Decision 597 of "
           "1976, now governed by Law 203 of 1991 as amended by Law 185 of 2020. Its "
           "corporate term runs 5-Dec-2018 to 4-Dec-2043 per the EGM of 8-Oct-2018. No "
           "capital increase, buy-back, bonus issue or split appears anywhere in the "
           "record for FY2022 to FY2026.",
    model_impact="")

# ---- one-off base-resetting transactions ----------------------------
f_stop = R.add(
    Ring.COMPANY, "one-off base-resetting transactions", FindingClass.B,
    "THE PRODUCTION STOPPAGE RESERVE, WHICH IS NOT AN ORDINARY RESERVE. A 'production "
    "suspension risk reserve' of EGP 1,622 million was created in 2015/2016 by "
    "Extraordinary General Assembly resolution 'to cover the losses incurred as a "
    "result of a power cut'. It stood at EGP 1,473,415,047 at 30-Jun-2024, "
    "3,803,487,434 at 30-Jun-2025 and 6,349,884,947 at 31-Mar-2026 — it has more than "
    "quadrupled in under two years",
    "Aluminium Company of Egypt, audited financial statements FY2024 and FY2025, "
    "'Analysis acc/ Other reserves' and the owner's-equity notes; 9M-FY2026 filing",
    CO, "2025-08-13",
    detail="Each year's other-reserves schedule foots exactly: FY2025's 192,558,315 + "
           "22,516,186 + 3,803,487,434 = 4,018,561,935 and 9M-FY2026's 192,558,315 + "
           "22,516,186 + 6,349,884,947 = 6,564,959,448. This is the company itself "
           "putting a number on the risk that its power supply is interrupted — the "
           "single clearest statement in the whole filing of what the real hazard is.",
    is_fs_data=True, fiscal_period="FY2025",
    model_impact="BASE CHANGER for the equity bridge and for the risk case, and it must "
                 "be DUAL-FRAMED. It is an appropriation of retained earnings, not a "
                 "liability, so it does NOT reduce distributable value on its face — but "
                 "it is ring-fenced from distribution and its growth rate is a direct "
                 "drag on the dividend. Frame the equity value both with the reserve "
                 "treated as distributable and with it treated as permanently "
                 "restricted, and state the difference in EGP per share.")

f_prot = R.add(
    Ring.COMPANY, "one-off base-resetting transactions", FindingClass.S,
    "TRADE PROTECTION, IMPOSED AND THEN REVOKED. On 13-Apr-2021 the Ministry of Trade "
    "and Industry imposed final safeguard measures on imported aluminium moulds, "
    "cylinders and wires for three years: 16.5% of CIF with a minimum of USD 333 per "
    "tonne in year one, then 10.5% with minima of USD 271 and USD 211. On 14-Nov-2022 "
    "the Ministry passed a resolution to REVOKE AND CANCEL that measure. Separately, a "
    "US anti-dumping case against aluminium from eighteen countries including Egypt "
    "ended in March 2021 with the rate cut from 31.5% to 12.3%; EGAL's exports into it "
    "were 4,866 t in FY2018, 21,152 t in FY2019 and 1,060 t in FY2020",
    "Aluminium Company of Egypt, audited financial statements FY2025, notes (13) "
    "Protection File and (14) Dumping File",
    CO, "2025-08-13",
    is_fs_data=True, fiscal_period="FY2025",
    model_impact="Sets the domestic-price ceiling. With the safeguard cancelled since "
                 "November 2022, EGAL's LOCAL selling price is disciplined by import "
                 "parity rather than protected — which is why the local-versus-export "
                 "split in F26 has to be modelled at two different realised prices "
                 "rather than one blended number. The old export tonnages are also the "
                 "only multi-year physical volume series the company has ever printed.")

f_anode = R.add(
    Ring.COMPANY, "one-off base-resetting transactions", FindingClass.C,
    "Two carbon-integration commitments sit outside the operating accounts. A provision "
    "for contribution to the carbon blocks company stood at EGP 817,662,886 at "
    "30-Jun-2024, 865,230,181 at 30-Jun-2025 and 914,027,800 at 31-Mar-2026. EGAL's "
    "stake in Egypt Anode Block Company is USD 5.8m, about EGP 33.85m, a 20% holding "
    "with a joint guarantee of a loan, and EGAL lent it EGP 7,507,500 at 13% over four "
    "years. There is also a non-banking guarantee of EGP 95m due from Egyptian Copper "
    "Works since FY2007/2008 on which EGP 98.5m of interest has accrued and against "
    "which a full provision has been made",
    "Aluminium Company of Egypt, audited financial statements FY2025, notes (3), (4) "
    "and (16)",
    CO, "2025-08-13",
    is_fs_data=True, fiscal_period="FY2025",
    model_impact="")

# =====================================================================
# NEGATIVE SEARCHES — dated, with the query that was actually run
# =====================================================================
f_neg_fy22 = R.add_negative(
    Ring.COMPANY, "official financial statements",
    "Probed the company's own IR statement shelf exhaustively for FY2022 and FY2023 "
    "annual statements: https://www.mistnews.com/mistsat/companies/mezanyat/{en,ar}/"
    "334089_{1,2,3,4,5,9}_0_{2020,2021,2022,2023}.{pdf,PDF} — 96 URL variants, EVERY "
    "ONE non-200. The IR portal's own Financial Statements index lists only "
    "9M-2026, Quarter-2026, Annual-2025, 9M-2025, Semi-annual-2025, Quarter-2025, "
    "Annual-2024, 9M-2024, Quarter-2024, 9M-2019 and Semi-annual-2019: there is NO "
    "FY2022 or FY2023 annual filing on the company's channel. Also checked the "
    "Disclosure Reports for 30-Jun-2022 and 30-Jun-2023, which carry board and "
    "shareholder structure ONLY and no financial statements. The EGX portal, which "
    "would hold the archive, is Imperva-blocked (see primary access). FY2023 is "
    "therefore carried from the audited COMPARATIVE column of the FY2024 filing (F09), "
    "which is a company-official audited document; FY2022 IS NOT AVAILABLE FROM ANY "
    "PRIMARY COMPANY SOURCE and is NOT substituted from an aggregator.",
    SWEEP_DATE)

f_neg_fy26 = R.add(
    Ring.COMPANY, "official financial statements", FindingClass.NEG,
    "Negative search — the FY2026 full-year unaudited indicators EXIST and could not be "
    "retrieved (searched: EGX bulletin 342467_1.pdf and 342467_2.pdf; mistnews "
    "announcement directory filename guesses; the IR Financial Statements shelf, which "
    "stops at 9M-2026)",
    "negative search", SourceType.SEARCH, SWEEP_DATE,
    detail="THE STOP-AND-INFORM ITEM. The company's own IR news feed records, dated "
           "12-Aug-2026: 'Egypt Aluminum (EGAL.CA) - Decisions of the BoD's Meeting ... "
           "Decisions of the Board of Directors' meeting held on 11/08/2026 and the "
           "company's unaudited financial indicators for the year ending on 30/06/2026', "
           "with two attachments — 'Decisions of the BoD Meeting in Arabic & English "
           "(1,657 KB)' and 'Audit Committee Report in Arabic & English (370 KB)'. Both "
           "resolve to https://www.egx.com.eg/downloads/Bulletins/342467_1.pdf and "
           "342467_2.pdf, and the whole egx.com.eg domain returns an Imperva/Incapsula "
           "JavaScript challenge instead of content. [R-SIGCM-03]'s fallback ladder was "
           "exhausted: the company's own IR host serves the statements shelf (which "
           "stops at 9M-2026), the disclosure shelf (board and shareholder structure "
           "only, no financials) and the investment plans (which stop at FY2024-2025). "
           "No company-official route to the FY2026 full-year figures exists from here. "
           "USER ACTION REQUESTED: please attach 342467_1.pdf. NO aggregator, broker or "
           "press number has been substituted for it.",
    fiscal_period="FY2026")

f_neg_h1 = R.add(
    Ring.COMPANY, "regular disclosures", FindingClass.NEG,
    "Negative search — no H1-FY2026 (six months to 31-Dec-2025) financial statements on "
    "the company's channel (searched: 334089_2_0_2026.pdf in both en and ar on the IR "
    "statement shelf, and the shelf's own index)",
    "negative search", SourceType.SEARCH, SWEEP_DATE,
    detail="The shelf carries Semi-annual 2025 but NOT Semi-annual 2026, and the "
           "334089_2_0_2026.pdf path is non-200 in both languages. The period is "
           "nonetheless covered by a company-official disclosure — the board-and-"
           "shareholder-structure report for the period ended 31/12/2025, retrieved and "
           "tagged H1-2026 — and cumulatively by the 9M-FY2026 statements. A build "
           "should derive Q2 and Q3 of FY2026 as 9M less Q1 and LABEL them derived, "
           "rather than presenting a half-year it does not have.",
    fiscal_period="H1-2026")

f_neg_cogs = R.add_negative(
    Ring.COMPANY, "regular disclosures",
    "'Egyptalum cost of sales breakdown by nature electricity power alumina anode "
    "carbon coke energy cost EGP' across all four audited filings and the sustainability "
    "report. The audited statements DO carry an expense-by-nature analysis, but ONLY "
    "for administrative expenses (fuel-oils 1,131 / spare parts and packing 8,665 / "
    "ELECTRICITY AND WATER 1,223 / stationery 1,366 / wages 95,935 / purchased services "
    "42,544 / depreciation 962 / rents 589 / indirect taxes 8,304, in EGP thousands, "
    "footing exactly to 160,719). There is NO equivalent analysis of the EGP "
    "27,873,523,941 cost of goods sold: no electricity cost line, no alumina cost, no "
    "anode cost, no consumption quantity for any input. Note (17), captioned 'Income "
    "Statement (Classification of Expense by Nature)', in fact prints only the tax "
    "reconciliation.",
    SWEEP_DATE)

f_neg_tariff = R.add_negative(
    Ring.COMPANY, "regular disclosures",
    "'Egyptalum electricity tariff contract EETC power purchase agreement price per kWh "
    "EGP piastres' across the audited statements, the sustainability report, the EPD, "
    "the investment plans, the board reports and the company website. THE COMPANY "
    "DISCLOSES ITS ELECTRICITY CONSUMPTION IN KWH BUT NEVER THE PRICE IT PAYS FOR IT. "
    "No contracted tariff, no supply agreement, no EETC contract term, and no price for "
    "the Scatec solar PPA appears anywhere in any company document. EgyptERA's "
    "published schedule (F03) names KIMA as its own extra-high-voltage tariff line but "
    "does NOT name EGAL, so it is not possible to confirm from any primary source "
    "whether EGAL pays the published 'OTHER USERS' rate or a negotiated one.",
    SWEEP_DATE)

f_neg_kwh = R.add_negative(
    Ring.COMPANY, "IR communications (calls, presentations, releases)",
    "'Egyptalum kWh per tonne smelter specific energy consumption DC current efficiency "
    "amperage pot line' in the sustainability report, the EPD, the ASI audit report "
    "listing and the plant pages. The SITE-WIDE electricity total is disclosed (F28) "
    "and an energy-saving delta of 500 kWh/t is disclosed (F29), but the SMELTER-ONLY "
    "specific energy consumption, the cell amperage and the current efficiency are not. "
    "There is also no earnings-call transcript, no results presentation deck and no "
    "webcast anywhere on the company's channel — EGAL's investor communication is "
    "filings and board reports only, with no analyst call.",
    SWEEP_DATE)

f_neg_guid = R.add_negative(
    Ring.COMPANY, "strategic plans & guidance",
    "'Egyptalum guidance outlook forecast target production tonnes FY2027 volume "
    "capacity utilisation' across the board reports, the AGM materials and the company "
    "news feed. EGAL publishes a BUDGET and reports achievement against it after the "
    "fact (F26), but issues NO forward guidance of any kind — no volume target, no "
    "price assumption, no margin target, no capex guidance beyond the year already "
    "begun. The FY2025-2026 Investment Projects Plan is a 404 on the portal, so even "
    "the current year's capital budget is not published.",
    SWEEP_DATE)

f_neg_stake = R.add_negative(
    Ring.COMPANY, "ownership / stake changes (named-transaction rule)",
    "'Egyptalum Metallurgical Industries stake sale privatisation IPO offering "
    "programme mandatory tender offer' plus a direct comparison of the company's own "
    "shareholder-structure disclosures at 30-Jun-2022 and 30-Jun-2026. NO STAKE "
    "TRANSACTION HAS OCCURRED: Metallurgical Industries Company holds exactly "
    "370,578,435 shares on both dates and El Nasr Mining exactly 9,075,000. No tender "
    "offer, no secondary offering, no state-divestment programme entry and no strategic "
    "stake sale appears in any company filing. Searched the specific named transaction "
    "rather than accepting an 'estimated' float.",
    SWEEP_DATE)

f_neg_bod = R.add_negative(
    Ring.COMPANY, "management & capital actions",
    "'Egyptalum capital increase bonus shares stock split buyback treasury shares "
    "employee share scheme' across the IR portal's Bonus Share and Insider Action "
    "registers, the General Assembly register and the audited statements. Both the "
    "Bonus Share and the Insider Action registers are EMPTY. Issued capital has been "
    "EGP 1,650,000,000 on 412,500,000 shares at EGP 4.00 par throughout FY2022-FY2026, "
    "and the 30-Jun-2022 disclosure records treasury shares as 'لا يوجد' — none.",
    SWEEP_DATE)

f_neg_fx = R.add_negative(
    Ring.COUNTRY, "fiscal / political events with sector read-through",
    "'Egyptalum EGP USD exchange rate assumption hedging policy forward contracts "
    "currency risk' in the audited statements' financial-instruments and foreign-"
    "currency notes. The company states its translation POLICY (CBE rate at the "
    "beginning of each month and at each balance-sheet date) and reports the resulting "
    "gain or loss, but discloses NO hedging programme, NO forward book and NO forward "
    "FX assumption. The FX path in the model is therefore external to the company.",
    SWEEP_DATE)

f_neg_lease = R.add_negative(
    Ring.GLOBAL, "trade / sanctions / supply chains",
    "'Egyptalum CBAM certificate cost exposure EU export carbon border adjustment "
    "quantified' in the company's own documents. EGAL's sustainability report NAMES "
    "CBAM as a transition challenge in its 17-Nov-2025 EGX/Chapter Zero panel item and "
    "plots itself against the 5.2 tCO2e/t threshold, but has NEVER quantified a CBAM "
    "cost, disclosed the EU share of its exports, or stated an embedded-emissions "
    "figure per shipment. The exposure must therefore be SIZED by the study from F04, "
    "F26 and F30 and labelled as an estimate, not quoted as a disclosure.",
    SWEEP_DATE)

f_series = R.add(
    Ring.COMPANY, "regular disclosures", FindingClass.C,
    "THE LISTING AND THE PRICE SERIES, RECORDED — NO BETA RESOLVED. Single listing on "
    "the Egyptian Exchange, ticker EGAL.CA, ISIN EGS3E181C010, sector Basic Resources, "
    "listed 29-Jul-1997, quoted and reported in EGP. NO DUAL LISTING EXISTS — checked, "
    "not assumed. On the sweep date the company's own IR feed showed open 370, high "
    "376, low 364, last and close 374.99, change +4.99 (+1.35%), volume 210,362, market "
    "capitalisation EGP 152,625,000,000 and a trailing P/E of 14.98 on FY2025 EPS of "
    "24.69",
    "Egyptalum investor-relations portal, share-price block; engine/raw_ohlc/EG/EGAL.csv "
    "and engine/raw_indices/EG/EGX30.csv",
    PMD, "2026-09-09",
    detail="The repo already holds engine/raw_ohlc/EG/EGAL.csv, 3,537 daily rows from "
           "02-Jan-2011 to 23-Aug-2026, last close EGP 330.00, and "
           "engine/raw_indices/EG/EGX30.csv to 08-Sep-2026 at 56,174.30. THE STOCK FILE "
           "IS STALE BY SEVENTEEN CALENDAR DAYS AND THE STOCK HAS MOVED 13.6% INSIDE "
           "THAT GAP (330.00 on 23-Aug against the IR feed's 374.99 on 09-Sep). "
           "Currency and magnitude were verified against the exchange the stock is "
           "filed under: EGP 330 x 412.5m shares is EGP 136bn, consistent with the IR "
           "feed's EGP 152.6bn at 370, so the series is the EGX EGP line. Refresh the "
           "panel through Step 0.0 BEFORE any regression. Per instruction, no beta is "
           "resolved in this sweep; the regressor for a later run is EGX30, the "
           "published index of the exchange EGAL is listed on, via "
           "engine/beta_regression.py own_stock_beta(). Do not hand-roll one.",
    model_impact="")

# =====================================================================
# DRIVER GATE TABLE
# Bottom-up is the default; every top-down row names the absence that forced it.
# =====================================================================
R.add_driver(
    "Sales volume (tonnes of aluminium)", DriverMode.BOTTOM_UP,
    "Built as a UTILISATION PATH against a disclosed 320,000 tpa nameplate, not as a "
    "growth rate. Anchors: 295,000 t sold in FY2025 from the audited revenue-recognition "
    "note; 286,412 t produced in CY2022 from the sustainability report; 14 reduction "
    "cells idle at 30-Jun-2025 from the audited stopped-assets note. Ceiling is physical "
    "and the headroom is small (~92% utilised), so tonnes cannot carry the forecast.",
    [f_vol, f_cap, f_cells, f_fs25])

R.add_driver(
    "Realised price (EGP per tonne)", DriverMode.BOTTOM_UP,
    "Solved from the audited disclosure — EGP 43,184m over 295 kt = EGP 146,386/t for "
    "FY2025 — then projected against the LME path in USD and the CBE EGP rate, with the "
    "realisation spread to LME held or flexed rather than invented. Growth is projected "
    "in the PRICE leg separately from the volume leg, per the protocol.",
    [f_vol, f_lme, f_rates, f_fs25])

R.add_driver(
    "Local versus export revenue split", DriverMode.BOTTOM_UP,
    "Disclosed by the company for 9M-FY2026: local EGP 14,651m (39.9%) and exports EGP "
    "22,102m (60.1%), each against its own budget. Two realised prices are modelled, not "
    "one blended price, because the local price is disciplined by import parity since "
    "the safeguard was revoked in November 2022.",
    [f_bod9m, f_prot])

R.add_driver(
    "Electricity consumption per tonne (kWh/t)", DriverMode.BOTTOM_UP,
    "Company-disclosed site electricity of 4,703,545,513 kWh/yr over disclosed "
    "production of 286,412 t gives 16,422 kWh/t SITE-WIDE. FLAGGED GAP, stated openly: "
    "the smelter-only figure is not disclosed, so the build is at SITE level and the "
    "study says so rather than implying a pot-line number it does not have. The Kanak "
    "500 kWh/t saving is carried as a scenario, not in the base.",
    [f_energy, f_kanak, f_neg_kwh])

R.add_driver(
    "Power tariff (EGP per kWh)", DriverMode.BOTTOM_UP,
    "EgyptERA's published extra-high-voltage schedule, mapped onto the JUNE fiscal year: "
    "126.9 Pt/kWh to Jul-2024, 160.0 from Sep-2024, 189.0 from Apr-2026. Each step is an "
    "explicit dated event and the next one is dual-framed. FY2027 carries a full year at "
    "189.0 with no new decision needed. The company has no self-generation — its own "
    "plant was abandoned in March 2022 — so the tariff passes straight through.",
    [f_tariff, f_cells, f_energy])

R.add_driver(
    "Power cost per tonne (EGP/t) — the dominant cost line", DriverMode.BOTTOM_UP,
    "kWh/t x tariff x tonnes, every term of which is sourced above. At 16,422 kWh/t and "
    "189.0 Pt/kWh this is roughly EGP 31,000/t against a FY2025 realised price of EGP "
    "146,386/t. Built as a cost PER UNIT, which is what the protocol requires wherever "
    "the filings disclose enough to do it.",
    [f_energy, f_tariff, f_vol])

R.add_driver(
    "Gross margin", DriverMode.BOTTOM_UP,
    "AN OUTPUT, NEVER AN INPUT. Computed as realised price less the built cost stack, "
    "and the build must REPRODUCE the four disclosed margins before it forecasts "
    "anything: 31.95% FY2023, 38.50% FY2024, 34.64% FY2025, 30.00% Q1-FY2026 and 33.43% "
    "9M-FY2026. Setting a margin here would be a QC fail, because the filings disclose "
    "enough to build cost per unit instead.",
    [f_fs23, f_fs24, f_fs25, f_q1, f_9m])

R.add_driver(
    "Non-power cash cost per tonne (alumina, anodes, coke, consumables)",
    DriverMode.TOP_DOWN,
    "FORCED TOP-DOWN AND FLAGGED. The company publishes an expense-by-nature analysis "
    "for administrative expenses only; the EGP 27.9bn cost of goods sold has no "
    "breakdown, no electricity line, no alumina cost and no input quantities. Modelled "
    "as a residual per tonne after the bottom-up power cost, indexed to the alumina "
    "price and to Egyptian inflation, and sensitised. This is the coarsest level in the "
    "model and the study must say so out loud rather than going quiet about it.",
    [f_neg_cogs, f_fs25, f_lme])

R.add_driver(
    "Labour cost", DriverMode.BOTTOM_UP,
    "4,802 employees at 31-Mar-2026 (4,794 permanent) is a hard denominator; cost per "
    "head is built from the audited wages and insurance lines and grown with Egyptian "
    "wage inflation. The state-owned Upper Egypt context means headcount is modelled as "
    "sticky, not as a lever.",
    [f_emp, f_fs25, f_cf25])

R.add_driver(
    "Capex", DriverMode.BOTTOM_UP,
    "Built off the company's own line-item Investment Projects Plan — 144-cell overhauls, "
    "a 50 kt alumina silo, Russian rectifier transformers, gas filters — against actual "
    "capex paid of EGP 1,272,701,468 in FY2025 and EGP 427,827,676 in FY2024. The three "
    "conflicting company figures for FY2024/25 capex (plan 2,061m, note 1,051m, actual "
    "1,273m) are all disclosed and the execution gap is carried as a slippage factor. "
    "Not a percentage of revenue.",
    [f_plan, f_cf25, f_cells])

R.add_driver(
    "Expansion capacity (Line 7 / Trafigura +300 kt; new 60 kt wire line)",
    DriverMode.BOTTOM_UP,
    "Two different things, deliberately separated. The 60,000 tpa wire line is BUILT and "
    "running and enters the BASE CASE as a product-mix uplift to realised price. The "
    "Trafigura +300,000 tpa at USD 900m is a signed STUDY agreement, pre-FID, with no "
    "financing close and no dates — it is excluded from the base case and shown as an "
    "explicit dual-framed scenario carrying its own capital cost and its own ~4.9 TWh of "
    "uncontracted administered-tariff power.",
    [f_traf, f_wire, f_cells, f_cap])

R.add_driver(
    "Solar PPA displacement of grid power", DriverMode.TOP_DOWN,
    "Scatec's 1 GW in two 500 MW phases is company-disclosed, but THE PPA PRICE IS NOT, "
    "and neither is the contracted volume or the start date. Modelled top-down as a "
    "scenario on the power-cost driver with the PPA tariff as the swing variable and "
    "zero displacement in the base case. Top-down here is the evidenced floor, not "
    "convenience.",
    [f_neg_tariff, f_solar])

R.add_driver(
    "FX (EGP/USD) path", DriverMode.TOP_DOWN,
    "The company discloses its translation policy and the resulting gain or loss but no "
    "hedging programme, no forward book and no FX assumption, so the path cannot be "
    "built from company disclosure. Set from the CBE spot of 50.98/51.08 and the CBE's "
    "own published inflation path, and sensitised — with the explicit and separate FX "
    "line modelled rather than folded into margin.",
    [f_neg_fx, f_rates, f_cbe])

R.add_driver(
    "Working capital and cash conversion", DriverMode.BOTTOM_UP,
    "Built from the audited balance-sheet detail — inventories of EGP 13.23bn including "
    "EGP 3.40bn of letters of credit, gross receivables of EGP 5.48bn against a EGP "
    "598.6m provision that was fed EGP 500.6m in FY2025 alone — against operating cash "
    "of EGP 4.66bn on net profit of EGP 10.19bn. The 46% conversion is a modelled "
    "output, not an assumption.",
    [f_bs25, f_cf25, f_prov])

R.add_driver(
    "Cost of capital: risk-free rate and Ke", DriverMode.BOTTOM_UP,
    "Explicit-window risk-free anchored on the CBE main operation rate of 19.50% held "
    "20-Aug-2026; terminal norm-built from the CBE's OWN published medium-term inflation "
    "target plus a standard EM real-rate convention, never averaged from history. Kd "
    "carries almost no weight: gross debt is EGP 37.7m against EGP 22.4bn of equity.",
    [f_cbe, f_bs25])

R.add_driver(
    "Tax rate", DriverMode.BOTTOM_UP,
    "Built from the audited effective rate — 25.50% in FY2025 and 22.46% in FY2024 — "
    "against the 22.5% statutory rate, with the gap carried explicitly rather than "
    "assumed away.",
    [f_tax, f_fs25])

R.add_driver(
    "Dividend and the equity bridge", DriverMode.BOTTOM_UP,
    "Built off the disclosed statutory waterfall (20% to legal reserve, 10-12% to "
    "personnel, board capped) and the actual coupon history 4.50 / 6.50 / 7.00 / 8.00 "
    "for FY2022-FY2025. The production stoppage reserve, which has more than quadrupled "
    "to EGP 6.35bn, is dual-framed as distributable and as permanently restricted, with "
    "the difference stated in EGP per share.",
    [f_div, f_stop, f_bs25])

R.add_driver(
    "CBAM and US Section 232 export exposure", DriverMode.TOP_DOWN,
    "Sized by the study from three disclosed numbers — 60.1% export share, 13.182 "
    "tCO2e/t disclosed intensity, EUR 75/t certificate benchmark — because the company "
    "has never quantified a CBAM cost, disclosed its EU export share or published an "
    "embedded-emissions figure. Labelled an estimate throughout, never quoted as a "
    "disclosure.",
    [f_neg_lease, f_trade, f_bod9m, f_ghg])

# =====================================================================
# OUTPUT — errors and warnings printed verbatim, nothing suppressed
# =====================================================================
errors, warnings = R.validate()
R.to_json(os.path.join(HERE, 'sweep_register.json'))

print(R.qc_line())
print(f"\nfindings: {len(R.findings)} | drivers: {len(R.drivers)}")
c = R.counts()
print(f"classes: B={c['B']} S={c['S']} D={c['D']} C={c['C']} NEG={c['NEG']}")
nbu = sum(1 for d in R.drivers if d.mode is DriverMode.BOTTOM_UP)
print(f"driver modes: {nbu} bottom-up / {len(R.drivers) - nbu} top-down")
n_ir = sum(1 for f in R.findings if f.source_type is SourceType.COMPANY_IR)
n_co = sum(1 for f in R.findings if f.source_type is SourceType.COMPANY_OFFICIAL)
print(f"company sources: {n_co} COMPANY_OFFICIAL, {n_ir} COMPANY_IR")
fs_years = sorted({f.fiscal_period for f in R.findings
                   if f.is_fs_data and f.fiscal_period.startswith("FY")})
print(f"FS fiscal years carrying is_fs_data: {fs_years}")
print(f"study year {R.study_year} quarters declared: {R.study_quarters_disclosed}")
print(f"primary access attempts logged: {len(R.primary_access)} "
      f"({sum(1 for p in R.primary_access if p.reachable)} reachable, "
      f"{sum(1 for p in R.primary_access if not p.reachable)} blocked)")

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
    print("\nVALIDATOR WARNINGS: none")

fresh = R.check_freshness(SWEEP_DATE)
print(f"\nfreshness (delivery {SWEEP_DATE}): "
      f"{fresh or 'OK — sweep and intended delivery the same day, 0 days elapsed'}")
