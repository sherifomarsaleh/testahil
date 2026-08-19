"""SAVOLA — Step 2A Information Sweep register (engine/research_sweep.py scaffold).

Every finding is dated and sourced; financial-statement lines are COMPANY_OFFICIAL only
(audited/reviewed statements or the company's own announcements/releases); IR presentations
are tagged COMPANY_IR distinctly. Aggregators appear only as market-data cross-checks.
Run: validates the register and writes sweep_register.json; a validation error is a build FAIL.
"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from research_sweep import (SweepRegister, AssetClass, Ring, FindingClass, SourceType,
                            DriverMode)

reg = SweepRegister("SAVOLA", AssetClass.STOCK, "2026-08-18")

# ---- primary access log ------------------------------------------------------
reg.record_primary_access("https://www.savola.com/en/investors/financial-statements", True,
                          "2026-08-18", "company IR portal reachable; FY2023-25 audited FS, "
                          "Q1-2026 reviewed FS, all interim FS 2004-2025 listed and downloadable")
reg.record_primary_access("https://www.savola.com/en/investors/earnings-presentations", True,
                          "2026-08-18", "Q2-2026 and FY2025 investor presentations downloaded")
reg.record_primary_access("https://www.savola.com/en/news-media", True, "2026-08-18",
                          "company's own H1-2026 earnings release PDF (06-Aug-2026) downloaded")
reg.record_primary_access("https://www.saudiexchange.sa/.../?anId=94980&cs=2050", True,
                          "2026-08-18", "official Saudi Exchange announcement pages for Q1-2026 "
                          "results (anId 94980), FY2025 results (93502), FY2025 dividend (93503) read")
reg.record_primary_access("https://www.savola.com/en/investors/financial-statements (Q2-2026 "
                          "reviewed interim FS)", True, "2026-08-19",
                          "Q2-2026 reviewed interim FS RETRIEVED from the company site "
                          "(second edition — the first edition wrongly recorded them "
                          "unavailable and missed the Mehbaj consideration in note 19, the "
                          "30-Jun balance sheet and the ex-treasury EPS divisor; corrected "
                          "under the critique response). H1-2026 P&L anchors also sit in the "
                          "company's own earnings release + investor presentation; the reviewed "
                          "FS is a registered follow-up, not silently substituted.")

# ---- COMPANY ring ------------------------------------------------------------
fFS25 = reg.add(Ring.COMPANY, "official financial statements", FindingClass.D,
    "FY2025 audited consolidated FS (Deloitte, unmodified, authorized 05-Mar-2026): revenue "
    "26,081.1mn (+13.2%), gross profit 5,088.9 (19.5%), operating result 1,137.2, profit "
    "attributable 874.5, EPS 2.93; five reportable segments with full P&L/asset detail",
    "Savola FY2025 audited FS", SourceType.COMPANY_OFFICIAL, "2026-03-05",
    model_impact="base year for the whole model: segment revenues/COGS, cost-nature detail "
    "(notes 35-38), D&A 1,190.0, borrowings 1,893.9, leases 3,952.2, BS/CF anchors",
    is_fs_data=True, fiscal_period="FY2025",
    url="https://savola.blob.core.windows.net/website/docs/default-source/financial-reports/25-savola-en-signed-fs.pdf")
fFS24 = reg.add(Ring.COMPANY, "official financial statements", FindingClass.D,
    "FY2024 audited consolidated FS (KPMG): revenue 23,986.7 (incl. Türkiye basis), the SAR 6.0bn "
    "rights issue + SAR 8.3bn capital reduction (833.98mn shares cancelled) + Almarai in-kind "
    "distribution (fair value 12.75bn, gain 11,554.7mn) all completed in 2024",
    "Savola FY2024 audited FS", SourceType.COMPANY_OFFICIAL, "2025-03-10",
    model_impact="FY2024 comparative + FY2023 comparative statements; capital-structure reset "
    "(300mn shares) that defines today's per-share base",
    is_fs_data=True, fiscal_period="FY2024")
fFS23 = reg.add(Ring.COMPANY, "official financial statements", FindingClass.D,
    "FY2023 audited consolidated FS: revenue 26,818.3 (original basis incl. Iran/Sudan/Türkiye), "
    "profit attributable 899.2, EPS 1.69; FY2022 comparatives (revenue 28,054.7, EPS 1.39)",
    "Savola FY2023 audited FS", SourceType.COMPANY_OFFICIAL, "2024-03-14",
    model_impact="third+fourth audited years; DSO/DIO/DPO history for the asset-conversion cycle",
    is_fs_data=True, fiscal_period="FY2023")
reg.add(Ring.COMPANY, "official financial statements", FindingClass.C,
    "FY2022 full statements (comparatives in FY2023 audited FS): revenue 28,054.7, gross profit "
    "4,874.1, profit attributable 742.8 — pre-restructuring perimeter incl. Iran/Sudan/Türkiye",
    "Savola FY2023 audited FS (FY2022 comparatives)", SourceType.COMPANY_OFFICIAL, "2024-03-14",
    is_fs_data=True, fiscal_period="FY2022")
fQ1 = reg.add(Ring.COMPANY, "regular disclosures", FindingClass.D,
    "Q1-2026 reviewed interim FS: revenue 7,292.2 (+0.2%), gross profit 1,402.1 (19.2%), "
    "operating result 421.7 (+16.7%), profit attributable 284.5 (incl. +41.7 Sudan disposal gain "
    "in discontinued), continuing EPS 0.82; BS at 31-Mar-2026: loans 1,785.9, cash 932.1, "
    "equity attributable 5,708.4",
    "Savola Q1-2026 reviewed interim FS", SourceType.COMPANY_OFFICIAL, "2026-05-06",
    model_impact="study-year Q1 actuals anchor FY2026E; working-capital seasonality",
    is_fs_data=True, fiscal_period="Q1-2026")
fH1rel = reg.add(Ring.COMPANY, "regular disclosures", FindingClass.B,
    "H1-2026 earnings release (company's own, 06-Aug-2026): H1 revenue 13,588 (+3.9%), EBITDA "
    "1,316 (9.7%, +70bp), net profit attributable 401 (+36%), recurring 372 (+40%); Q2 revenue "
    "6,295 (+8.6%); net debt 851 at 30-Jun-2026; capex 385; dividends paid 524 incl. NCI; Sudan "
    "exit completed (consideration 52.5, gain 43, Savola share 41); opex down to 14.5% of revenue",
    "Savola H1-2026 earnings release", SourceType.COMPANY_OFFICIAL, "2026-08-06",
    model_impact="FY2026E base: H1 actuals lock the first half; Sudan gain excluded from "
    "recurring base; net-debt/capex/dividend anchors for the cash walk",
    is_fs_data=True, fiscal_period="Q2-2026",
    url="https://savola.blob.core.windows.net/website/docs/default-source/custom-azure-uploads/savola-group---h1-2026-earnings-release--en---fv.pdf")
fQ2pres = reg.add(Ring.COMPANY, "IR communications (calls, presentations, releases)", FindingClass.D,
    "Q2-2026 investor presentation (Aug-2026): category unit data — oil volume 749k MT (+16.1%), "
    "sugar 1,038k MT (+7.2%), pasta 139k MT (+3.1%); GP/ton oil 762 (H1-25: 814), sugar 218, "
    "pasta 527; volume/price split of FP revenue (+757 volume / -275 price); Panda 231 stores "
    "(+4 net H1), NSA 583k m2, 149 CXR stores done, e-commerce ~2.5x YoY; segment net debt split "
    "(Foods 1.3bn, Panda 39mn, Herfy net cash 28mn, Kabeer 58mn); leases by segment (Panda 2.9bn "
    "of 3.7bn); unallocated costs H1 114 (64 cash + 50 non-cash)",
    "Savola Q2-2026 investor presentation", SourceType.COMPANY_IR, "2026-08-06",
    model_impact="UNLOCKS the bottom-up Food-Processing build (category volume x GP/ton) and the "
    "Panda store x sales-per-store build; segment debt/lease split feeds the bridge",
    fiscal_period="Q2-2026")
fFYpres = reg.add(Ring.COMPANY, "IR communications (calls, presentations, releases)", FindingClass.D,
    "FY2025 investor presentation: FY category units — oil 1,322k MT / rev 7,098 / GP 958 / "
    "EBITDA 563; sugar 2,162k MT (USCE-adjusted comparatives) / rev 4,868 / GP 413 / EBITDA 335; "
    "pasta rev 545, EBITDA margin 13.5%; recurring group revenue 26,081 vs 24,939 (+4.6%, "
    "comparative includes USCE pro-forma 1,563), recurring EBITDA 2,291 (8.8%) vs 2,346 (9.4%); "
    "recurring net profit 539.1 vs 295.5 with the full reported-to-recurring bridge (zakat/accrual "
    "reversals -300, Türkiye gain -32.3, put-option gain -40.2); net debt 411 (Dec-25) vs 594 "
    "(Dec-24); capex 858 (Panda 567, Foods 231); Panda opened 20 stores, closed 2, CXR 132 "
    "cumulative; 2026 target: 20+ new stores and 20+ CXR conversions",
    "Savola FY2025 investor presentation", SourceType.COMPANY_IR, "2026-03-09",
    model_impact="FY-level unit bases for every Food-Processing category; the recurring-EBITDA "
    "bridge that separates perimeter (USCE) from organic growth; Panda expansion guidance "
    "(20 stores/yr) as the store-path driver",
    fiscal_period="FY2025")
fDiv = reg.add(Ring.COMPANY, "management & capital actions", FindingClass.S,
    "FY2025 dividend: board recommended SAR 1.70/share (SAR 510mn, 17% of par) on 05-Mar-2026 "
    "under the stated policy of distributing ~50-60% of net profit annually; ex-date 07-May-2026; "
    "paid during H1-2026 (524 incl. NCI per the H1 release). FY2024: no dividend (12-Mar-2025 "
    "announcement) — the restructuring year",
    "Saudi Exchange announcement anId 93503 + AR2025 g-6 + H1-2026 release",
    SourceType.COMPANY_OFFICIAL, "2026-03-08",
    model_impact="payout driver 50-60% of net profit for the forecast BS/CF walk; q=0 for the "
    "1M/3M price cones (next expected ex-date ~May-2027, outside both windows) — flagged, not "
    "assumed silently")
fSudan = reg.add(Ring.COMPANY, "one-off base-resetting transactions", FindingClass.B,
    "Portfolio rationalisation COMPLETE: Iran exited FY2024 (loss 1,121.6), Sudan exited H1-2026 "
    "(consideration 52.5, gain 43), Türkiye (KUGU) disposed 2025 via share-swap into a 15% stake "
    "in Tiryaki (agreed equity valuation SAR 274.6mn; Tiryaki shares received post-YE, FVOCI)",
    "FY2025 audited FS note 22 + H1-2026 release", SourceType.COMPANY_OFFICIAL, "2026-08-06",
    model_impact="continuing perimeter is now Arabia+Egypt+Algeria+UAE food/retail; discontinued "
    "losses do not recur in the base; Tiryaki 15% enters the bridge as a non-operating asset "
    "at its FVOCI carrying value")
fMehbaj = reg.add(Ring.COMPANY, "ownership / stake changes (named-transaction rule)", FindingClass.S,
    "Al Mehbaj Al Shamiya for Trading LLC acquired 100% in July 2026 (subsequent to H1) — Saudi "
    "premium nuts/coffee/spices/pulses processor, to scale the Nuts-Spices-Pulses platform with "
    "the planned new Jeddah facility; total consideration SR 11.4mn (5.4 paid + 6.0 deferred), "
    "DISCLOSED in the Q2-2026 reviewed interims note 19, subject to GA ratification (the first "
    "edition recorded it undisclosed — corrected). Related-party dimension: Al Mehbaj is an Abdulkadir "
    "Al-Muhaidib & Sons company (AR2025 governance disclosures) — Al-Muhaidib is a major Savola "
    "shareholder",
    "Savola Q2-2026 reviewed interim FS note 19 + H1-2026 release + AR2025", SourceType.COMPANY_OFFICIAL,
    "2026-08-05",
    model_impact="Nuts/Spices KSA leg gets an inorganic scale step from H2-2026; consideration "
    "undisclosed so modelled as a modest revenue bolt-on inside the FP nuts category with the "
    "gap FLAGGED — no invented purchase price enters the bridge")
fStrat = reg.add(Ring.COMPANY, "strategic plans & guidance", FindingClass.S,
    "AR2025 + Q2-2026 presentation guidance: Panda to add 20+ stores and 20+ CXR conversions in "
    "2026; e-commerce scaling on the Ocado platform (~2.5x YoY); Foods investing in local "
    "manufacturing (new Jeddah processing facility, refinery upgrades); replacement-cost pressure "
    "expected through Q3/Q4-2026 but 'manageable within pricing and procurement measures'",
    "Savola AR2025 + Q2-2026 presentation", SourceType.COMPANY_IR, "2026-08-06",
    model_impact="store-path driver 20/yr; capex path anchored on FY2025 858 + H1-2026 385 "
    "run-rate; H2-2026 gross-margin held below H1 in the oil category (replacement cost)")
fESOP = reg.add(Ring.COMPANY, "management & capital actions", FindingClass.C,
    "Treasury/ESOP: 300.0mn shares issued; weighted-average outstanding 298.589mn FY2025 "
    "(1.41mn treasury under the employee plan; 70.0mn SAR of shares purchased in 2025); diluted "
    "299.257mn", "FY2025 audited FS notes 19/31", SourceType.COMPANY_OFFICIAL, "2026-03-05",
    is_fs_data=True, fiscal_period="FY2025")
fZak = reg.add(Ring.COMPANY, "regular disclosures", FindingClass.S,
    "Zakat: FY2025 carries a net REVERSAL of 217.4 (ZATCA final assessment of 2024 released "
    "247.3 of prior-year accruals, net); ZATCA assessments now FINAL through 2024; underlying "
    "continuing foreign income-tax charge 142.5; pending subsidiary zakat appeals total 32.3",
    "FY2025 audited FS note 29", SourceType.COMPANY_OFFICIAL, "2026-03-05",
    model_impact="normalized combined zakat+tax rate for the forecast (~19.5% of PBT) instead of "
    "the reversal-distorted FY2025 effective rate; recurring-earnings base strips the 247.3",
    is_fs_data=True, fiscal_period="FY2025")

# ---- INDUSTRY ring -----------------------------------------------------------
fFAO = reg.add(Ring.INDUSTRY, "pricing", FindingClass.S,
    "FAO Food Price Index Jul-2026 (released 07-Aug-2026): Vegetable Oils index 195.7 — HIGHEST "
    "since Jun-2022, palm and soy rising (+2.0% m/m); Sugar index 95.0 (-8.0% y/y, weak); "
    "Cereals 113.8 (+6.9% y/y, wheat +5.8% m/m on Black Sea risk)",
    "FAO Food Price Index", SourceType.REGULATOR_OFFICIAL, "2026-08-07",
    model_impact="cost side of the oil category: replacement-cost pressure is REAL and rising — "
    "H2-2026E oil GP/ton held BELOW the H1 actual; sugar price path held soft (revenue headwind, "
    "margin neutral-to-positive for a refiner); pasta input (wheat) watch",
    url="https://www.fao.org/worldfoodsituation/foodpricesindex/en/")
reg.add(Ring.INDUSTRY, "demand drivers & capacity/supply balance", FindingClass.C,
    "Saudi grocery retail: value-focused market with discounter influx and intense competition "
    "(company's own words, H1-2026 release: 'highly competitive, value-focused Saudi grocery "
    "market'); Panda claims market-share gains in hypermarkets + e-commerce",
    "Savola H1-2026 release + Q2-2026 presentation", SourceType.COMPANY_IR, "2026-08-06")
fPeers = reg.add(Ring.INDUSTRY, "competitor capacity / price moves (named)", FindingClass.C,
    "Named Saudi peers (market data 18-Aug-2026): Almarai (2280) P/E 19.7 TTM / mcap 48.2bn; "
    "Al Othaim Markets (4001) P/E 19.4 / mcap 4.4bn, FY2025 earnings -51%; BinDawood (4161) "
    "P/E 19.8 / mcap 5.2bn; NADEC (6010) P/E 13.0 / mcap 4.0bn; Herfy (6002) LOSS-making, "
    "mcap 1.00bn at 15.50/share; international analogue Wilmar (SGX F34) P/E 12.4",
    "stockanalysis.com quotes (market data)", SourceType.AGGREGATOR, "2026-08-18",
    model_impact="")
reg.add(Ring.INDUSTRY, "new entrants (named-competitor level)", FindingClass.C,
    "Retail competitive set: Al Othaim expanding, BinDawood (incl. Qatar), Lulu KSA, plus "
    "discounter formats pressuring sales densities — visible in Panda's flat sales/store and "
    "Othaim's -51% FY2025 earnings; QSR pressure visible in Herfy's revenue -6.8% and losses",
    "company disclosures + peer market data", SourceType.REPUTABLE_PRESS, "2026-08-18")
reg.add(Ring.INDUSTRY, "technology substitution", FindingClass.C,
    "Grocery e-commerce substitution: Panda's own online revenue ~2.5x YoY on the Ocado platform "
    "integration, aggregator platforms expanding — channel shift is the load-bearing retail-tech "
    "fact; no manufacturing-tech substitution event found for oils/sugar/pasta (searched "
    "18-Aug-2026)", "Savola Q2-2026 presentation", SourceType.COMPANY_IR, "2026-08-06")

# ---- COUNTRY ring ------------------------------------------------------------
fCPI = reg.add(Ring.COUNTRY, "sovereign macro (inflation, policy rate, FX/deval risk)", FindingClass.S,
    "Saudi CPI +1.8% y/y in Jul-2026 (GASTAT; food & beverages +1.5%); SAMA policy tracking the "
    "Fed post-peg (repo 4.00% after the Jun-2026 Fed cut); NDMC 1Y retail savings sukuk (Sah) "
    "fixed return 4.70% for the Aug-2026 subscription (up from 4.60% in July); Egypt (21% of "
    "revenue): CBE policy rate 19.50% (held since Apr-2026), EGP a serial-devaluation currency — "
    "Savola's net EGP balance-sheet exposure is a LIABILITY of EGP 7.41bn (a partial natural "
    "hedge: devaluation produces translation gains on the net liability)",
    "GASTAT via Arab News 14-Aug-2026 + NDMC announcement + FY2025 FS note 42",
    SourceType.REGULATOR_OFFICIAL, "2026-08-14",
    model_impact="Saudi revenue deflator ~2%; Egypt translation drag priced into segment "
    "revenue growth; rf construction uses the observed 1Y SAR sovereign 4.70%")
reg.add(Ring.COUNTRY, "regulatory environment (regulator, caps, tariffs, tax/subsidy)", FindingClass.C,
    "No new Saudi food-price caps, VAT change, or retail licensing shock found in 2026 (searched "
    "18-Aug-2026); sugar/edible-oil import regimes stable; Egypt operates under import/FX "
    "prioritisation for staples (supports USCE/AICE volumes)", "negative search + company filings",
    SourceType.SEARCH, "2026-08-18")
reg.add(Ring.COUNTRY, "fiscal / political events with sector read-through", FindingClass.C,
    "Regional geopolitical/logistics disruption raised freight, insurance and energy-linked "
    "logistics costs and hit Al Kabeer's Saudi trading conditions (company's own H1-2026 "
    "disclosure); Red Sea routing costs persist through 2026",
    "Savola H1-2026 release", SourceType.COMPANY_OFFICIAL, "2026-08-06")

# ---- GLOBAL ring -------------------------------------------------------------
fRates = reg.add(Ring.GLOBAL, "rate cycle & USD/FX regime", FindingClass.S,
    "UST 10Y 4.68% (FRED DGS10, 14-Aug-2026); UST 1Y 3.98% (DGS1) — Fed at 3.50-3.75% since "
    "Jun-2026, long end steep; Saudi sovereign USD 10Y priced Jan-2026 at UST+85bp (11.5bn "
    "4-tranche jumbo, Emirates NBD note 06-Jan-2026); Damodaran Jan-2026 Saudi row: Aa3, "
    "default spread 0.51%, ERP 5.01% (CDS 0.98% / ERP 5.72%); SAIBOR-3M 4.74% (Jun-2026); "
    "SAR pegged at 3.75",
    "FTSE SAGBI factsheet 31-Jul-2026 + iBoxx SAR sukuk publications + FRED + Damodaran "
    "ctryprem (July-2026 rating legs; Jan-2026 CDS legs, flagged)", SourceType.PRIMARY_MARKET_DATA,
    "2026-07-31",
    model_impact="rf OBSERVED on the published SAR sovereign curve: FTSE SAGBI 7-10y 5.52% "
    "(iBoxx 5.44% @6.07y corroborates; the first edition's UST+spread proxy landed at 5.53% "
    "and is retired); July-2026 Damodaran rating legs (0.48%/4.94%); both ERP bases carried "
    "through the WACC")
reg.add(Ring.GLOBAL, "commodity complex (input/output)", FindingClass.S,
    "Input complex: palm/soy (oil COGS) at 4-year highs and rising; raw sugar soft (-8% y/y) — "
    "compresses refined realizations but helps refiner spreads; wheat (pasta input) +5.8% m/m on "
    "Black Sea supply risk; Savola's own sugar book carries committed purchases of 214.9k t raw "
    "(212mn) against committed refined sales of 544.3k t (1,044mn) at Dec-2025",
    "FAO Jul-2026 + FY2025 FS note 30", SourceType.REGULATOR_OFFICIAL, "2026-08-07",
    model_impact="oil GP/ton path: H2-2026 held below H1 (replacement cost), FY2027+ mild "
    "normalisation; sugar committed-book prices anchor the near-term sugar revenue/ton")
reg.add(Ring.GLOBAL, "global sector demand", FindingClass.C,
    "Staple-food demand across MENA resilient; Savola's H1 volume growth (+11.7% FP) is "
    "company-specific evidence of demand strength in its markets despite pricing pressure",
    "Savola H1-2026 release", SourceType.COMPANY_OFFICIAL, "2026-08-06")
reg.add(Ring.GLOBAL, "trade / sanctions / supply chains", FindingClass.C,
    "Supply-chain: company cites higher freight/insurance/energy-linked logistics costs and "
    "'timely sourcing and commercial actions' keeping availability; Sudan/Iran exits remove "
    "sanction-adjacent exposure; no new trade restriction on Saudi food imports found "
    "(searched 18-Aug-2026)", "Savola H1-2026 release + negative search", SourceType.SEARCH,
    "2026-08-18")

# ---- negative searches to close remaining mandatory categories ---------------
nGuid = reg.add_negative(Ring.COMPANY, "strategic plans & guidance",
    "numeric FY2026 revenue/EBITDA guidance (none published — only store-count and CXR targets)",
    "2026-08-18")
reg.add_negative(Ring.INDUSTRY, "demand drivers & capacity/supply balance",
    "independent Saudi grocery market-size series for 2026 (GASTAT retail index not "
    "product-specific; no official grocery-market volume series found)", "2026-08-18")
nMehbaj = reg.add_negative(Ring.COMPANY, "ownership / stake changes (named-transaction rule)",
    "Al Mehbaj business-combination detail beyond the note-19 consideration (asset breakdown, "
    "earn-outs) — awaits the FY2026 statements' business-combination note", "2026-08-19")
reg.add_negative(Ring.COMPANY, "regular disclosures",
    "Panda store count at 30-Jun-2025 — not disclosed in any deck, release or interim; the "
    "sales-per-store change is published as a range (-7.1%/-6.0%) over the 213-assumption and "
    "interpolated-218 bases", "2026-08-19")
nSplit = reg.add_negative(Ring.COMPANY, "regular disclosures",
    "Panda sales-per-store or like-for-like growth series (not disclosed; only total revenue, "
    "store count and NSA are published)", "2026-08-18")

# ---- study year --------------------------------------------------------------
reg.declare_study_year("2026", ["Q1-2026", "Q2-2026"])

# ---- driver gate table -------------------------------------------------------
reg.add_driver("Oil volume (k MT) x revenue/ton x GP/ton", DriverMode.BOTTOM_UP,
    "category volumes and GP/ton disclosed FY2025 + H1-2026 (1,322k MT FY25; 749k MT H1-26 "
    "+16.1%); H2 held to a moderated path; GP/ton anchored on H1-2026 reviewed actual 762 with "
    "the FAO veg-oil rise capping H2", [fQ2pres, fFYpres, fFAO])
reg.add_driver("Sugar volume (k MT) x revenue/ton x GP/ton", DriverMode.BOTTOM_UP,
    "volumes disclosed (2,162k MT FY25 USCE-adjusted; 1,038k MT H1-26 +7.2%); refined price soft "
    "per FAO and the company's own committed-sales book; GP/ton anchored on H1-2026 actual 218",
    [fQ2pres, fFYpres, fFAO])
reg.add_driver("Pasta volume (k MT) x revenue/ton x GP/ton", DriverMode.BOTTOM_UP,
    "volumes disclosed (139k MT H1-26 +3.1%); GP/ton 527 H1-2026 actual anchored",
    [fQ2pres, fFYpres])
reg.add_driver("Nuts/Spices (Bayara + Mehbaj) revenue + margin", DriverMode.BOTTOM_UP,
    "UAE/KSA split disclosed to EBITDA level H1-2026; Mehbaj bolt-on from H2-2026 with "
    "consideration UNDISCLOSED — revenue effect modelled small and flagged",
    [fQ2pres, fMehbaj, nMehbaj])
reg.add_driver("Panda: store count x sales-per-store; EBITDA margin as output", DriverMode.BOTTOM_UP,
    "store path from company guidance (20+/yr) and disclosed H1-2026 network (231); "
    "sales/store DERIVED from disclosed revenue and store count (no LFL series published — "
    "negative search cited); margin an output of gross margin less operating ratios",
    [fQ2pres, fFYpres, fStrat, nSplit])
reg.add_driver("Herfy (Food Services) revenue path", DriverMode.TOP_DOWN,
    "no unit disclosure (restaurant count not in Savola's filings); revenue glide anchored on "
    "H1-2026 actual (-6.8%) recovering to flat/+2%; margin from disclosed H1-2026 EBITDA 18.7%",
    [nGuid, fH1rel])
reg.add_driver("Frozen Food (Al Kabeer) revenue path", DriverMode.TOP_DOWN,
    "no volume disclosure; revenue glide from H1-2026 actual (-1.4%) to +3-4%; GM 35.8% and "
    "EBITDA 13.7% anchored on H1-2026 actuals", [nGuid, fH1rel])
reg.add_driver("Working capital from DSO/DIO/DPO", DriverMode.BOTTOM_UP,
    "component days computed from FY2023-25 audited statements and held at the FY2025 level "
    "with the sugar committed book as the near-term anchor", [fFS25, fFS24])
reg.add_driver("Capex path", DriverMode.BOTTOM_UP,
    "FY2025 858 by segment (Panda 567) + H1-2026 385 actual + 20-store/yr guidance + FY2025 "
    "capital commitments 425 disclosed", [fFYpres, fH1rel, fStrat])
reg.add_driver("Combined zakat + income tax rate", DriverMode.BOTTOM_UP,
    "normalized from the disclosed components (foreign tax 142.5 continuing FY2025; zakat "
    "ex-reversal; FY2023 17.6%, Q1-2026 20.5%) -> 19.5% flat, sensitized",
    [fZak, fFS25, fQ1])

errors, warnings = reg.validate()
print("errors:", errors)
print("warnings:", warnings)
assert not errors, f"SWEEP REGISTER FAIL: {errors}"
print(reg.qc_line())
fresh = reg.check_freshness("2026-08-18")
print("freshness:", fresh or "OK (same-day)")
reg.to_json(os.path.join(HERE, 'sweep_register.json'))
print("wrote sweep_register.json |", len(reg.findings), "findings |", len(reg.drivers), "drivers")
