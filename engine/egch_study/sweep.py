"""EGCH (Egyptian Chemical Industries — KIMA) — four-ring Information Sweep register.

Runs BEFORE any forecast driver is set. Every mandatory category of every ring is
closed by a dated finding or a dated negative search.

SOURCING NOTE, recorded rather than hidden: this session's original egress policy
refused CONNECT to kimaegypt.com, egx.com.eg, fra.gov.eg and every aggregator. The
user then created an unrestricted network environment (Testahil-open) and the primary
documents were fetched THROUGH the company's own IR channel by a network-enabled
helper session: seven filings (four audited annuals FY2021/22-FY2024/25, three
FY2025/26 limited-review interims), each logged in filings/SOURCES.md with its exact
URL, size, page count and on-page period confirmation. All financial-statement
figures in this register carry COMPANY_OFFICIAL provenance from those filings, read
page-by-page (the PDFs are scanned images; extraction was a visual read of the
Arabic statements, crossfooted against every subtotal).
"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from research_sweep import (SweepRegister, AssetClass, Ring, FindingClass,
                            SourceType, DriverMode)

SWEEP_DATE = "2026-09-01"
R = SweepRegister("EGCH", AssetClass.STOCK, SWEEP_DATE)
CO, IR, REG, PMD, PRESS, AGG = (SourceType.COMPANY_OFFICIAL, SourceType.COMPANY_IR,
                                SourceType.REGULATOR_OFFICIAL, SourceType.PRIMARY_MARKET_DATA,
                                SourceType.REPUTABLE_PRESS, SourceType.AGGREGATOR)

# ---- primary access log (success AND failure both recorded) -----------------
R.record_primary_access("https://www.kimaegypt.com/InvestorsRelations.aspx", True, SWEEP_DATE,
    "Company's own IR page. This session's original proxy refused CONNECT (403); the user "
    "opened an unrestricted environment and a network-enabled helper session retrieved the "
    "page and every filing. The page embeds the IR portal from mistnews.com (the company's "
    "IR-portal provider); the PDFs are the company's own issued filings.")
R.record_primary_access("https://www.mistnews.com/ir/ir.aspx?sk=1034241017", True, SWEEP_DATE,
    "KIMA's IR portal (Financial Statements / Disclosure Reports / Audit Reports / Share "
    "Price / News). Source of all seven filing PDFs; full index in filings/SOURCES.md.")
R.record_primary_access("https://www.egx.com.eg/en/CompanyProfile.aspx?ISIN=EGS38201C017", False, SWEEP_DATE,
    "Exchange disclosure portal behind an F5/TSPD JS bot-challenge: WebFetch 503, curl got "
    "the challenge HTML, headless Chromium reset — even from the unrestricted helper. "
    "Exchange-stated share count therefore NOT obtained from EGX; the share count is taken "
    "from note 14 of the audited FY2024/25 statements instead (1,986,578,999 x EGP 5).")
R.record_primary_access("https://www.cbe.org.eg/en/auctions/egp-t-bills", False, SWEEP_DATE,
    "CBE auction pages WAF-blocked ('requested URL was rejected') from the helper too; "
    "T-bill yields carried from secondary quotes (investing.com), labelled as such.")

# ---- 1 September 2026 edition: the primary channel re-tried, and the archive read back to 2009
R.record_primary_access("https://www.kimaegypt.com/InvestorsRelations.aspx", True, "2026-09-01",
    "Reachable directly (HTTP 200) on 1 September 2026; the embedded Mist portal listing page "
    "timed out once and returned a 709-byte stub on retry, so the 8 August index was used.")
R.record_primary_access("https://www.mistnews.com/mistsat/companies/mezanyat/", True, "2026-09-01",
    "Ten older annual statements (years to June 2009, 2010, 2011, 2013, 2014, 2016, 2018, 2019, "
    "2020, 2021) retrieved as real PDFs from the company's own portal for the calibration of the "
    "method on the company's history. The portal lists no annual for 2012, 2015 or 2017 and "
    "nothing older than 2009; no FY2025/26 annual had been published.")
R.record_primary_access("https://kima.com.eg/", False, "2026-09-01",
    "Refused at the egress proxy; not the company's domain (kimaegypt.com is).")

# ---- study year: FY2025/26 (ends 30-Jun-2026); all three disclosed interims swept
R.declare_study_year("FY2025/26", ["Q1-2025/26", "H1-2025/26", "9M-2025/26"])

# ================================ RING 1 — GLOBAL ============================
f_rate = R.add(Ring.GLOBAL, "rate cycle & USD/FX regime", FindingClass.S,
    "Global easing cycle under way; Fed funds midpoint 3.63% (Jun-2026) — the backdrop "
    "against which Egypt's 19.00/19.50% policy corridor normalises",
    "US Federal Reserve policy history (house FED_SCHEDULE, engine/market_profiles.py)",
    REG, "2026-06-18",
    model_impact="Anchors the direction of the Kd glide and the terminal risk-free build: "
                 "the EGP cost-of-debt path falls only if the global path allows it.")

f_urea = R.add(Ring.GLOBAL, "commodity complex (input/output)", FindingClass.S,
    "Urea is the output commodity and it is in a war-supply squeeze: Middle-East conflict "
    "(Hormuz risk, Israeli-gas force majeure) drove global urea above $700/t FOB in "
    "H1-2026; CME Urea (Granular) FOB EGYPT front month settled ~$545/t on 7-Aug-2026. "
    "Natural gas is the input; Egyptian fertilizer producers pay a formula price of "
    "$5.75/mmBtu (raised from $4.50 effective from Nov-2021 pricing decision)",
    "CME/TradingView UFE front month (helper snapshot, live_data.json); Profercy/CRU "
    "coverage; gas formula price per note 28 of the audited FY2024/25 statements",
    PMD, "2026-08-07",
    model_impact="Sets the export-price driver's anchor ($545/t FOB Egypt today, mean-"
                 "reverting glide) and the gas-cost driver's USD price leg ($5.75/mmBtu "
                 "through USD/EGP — its own escalator, never a CPI proxy).")

f_gdem = R.add(Ring.GLOBAL, "global sector demand", FindingClass.C,
    "Nitrogen demand is annually recurring and price-inelastic (crop nutrient); the Middle "
    "East 'big three' (Qatar, Saudi, Egypt) carry ~35% of seaborne ammonia/urea trade, so "
    "regional disruption transmits straight into the FOB Egypt price",
    "CRU Group, 'Middle East Conflict: Urea supply disruptions could be catastrophic'",
    PRESS, "2026-03-01")

f_trade = R.add(Ring.GLOBAL, "trade / sanctions / supply chains", FindingClass.S,
    "Two trade-policy overlays: (1) Israel's war-driven gas-export force majeure removes "
    "~one LNG cargo per four days from Egypt's balance, forcing industrial gas rationing; "
    "(2) the EU CBAM reaches Egyptian nitrogen exports — KIMA has contracted an MRV "
    "emissions-reporting system (EGP 4.46m, Feb-2025) and its auditor warns delays "
    "threaten EU-bound exports from 2026",
    "S&P Global/Argus gas-curtailment coverage; CBAM/MRV per the auditor's report on the "
    "audited FY2024/25 statements", PRESS, "2026-03-04",
    model_impact="Downside scenario driver: gas-availability haircut on volumes; CBAM "
                 "compliance treated as a cost line risk, not a separate leg.")

# ================================ RING 2 — COUNTRY ===========================
f_cbe = R.add(Ring.COUNTRY, "sovereign macro (inflation, policy rate, FX/deval risk)", FindingClass.S,
    "CBE held the corridor at 19.00/20.00% (main operation 19.50%) in July-2026 after "
    "825bp of cuts from Apr-2025; headline CPI 14.3% y/y (Jun-2026, third month easing); "
    "USD/EGP 49.79 (7-Aug-2026); 10Y EGP sovereign 23.0% (6-Aug-2026). Devaluation "
    "remains a way of life: the EGP swung ~47 (Dec-2025) to ~50.4 (Mar-2026) and that "
    "single move produced a 1.46bn EGP Q3 FX loss on KIMA's USD debt",
    "CBE July-2026 MPC (FocusEconomics report); TradingEconomics CPI; investing.com "
    "10Y/FX (helper snapshot live_data.json); FX-loss mechanics per the 9M-2025/26 "
    "interim statements", PMD, "2026-08-07",
    model_impact="Sets rf* build (23.0% less the sovereign's own default spread), the "
                 "USD/EGP path applied to the gas price, the USD debt service, and the "
                 "FX-translation line that dominates quarterly earnings volatility.")

f_quota = R.add(Ring.COUNTRY, "regulatory environment (regulator, caps, tariffs, tax/subsidy)", FindingClass.S,
    "The nitrogen-fertilizer regime is administered: cabinet decision 170 (24-Nov-2021) "
    "required 55% of production to the subsidized system + 10% local free market with "
    "max 35% exports; trade-ministry decree 241/2021 set an EGP 2,500/t export levy on "
    "quota shortfalls (KIMA was charged EGP 437.5m on a 175kt shortfall in FY2024/25). "
    "Cabinet decision of 8-Sep-2025 then CUT the subsidized obligation (KIMA's required "
    "cooperative deliveries reset to ~16kt at a changed supply price, ~2.5kt/month) — "
    "the export share rose to ~53% sector-wide — and 2026 policy switched the export "
    "levy toward a 10% ad-valorem duty tied to global prices. Subsidized urea "
    "~EGP 6,000/t vs open-market ~EGP 28-32k/t",
    "Cabinet/ministry decisions as cited in the auditor's reports on the audited "
    "FY2024/25 statements and the Q1-2025/26 limited review; Mada Masr and Edge "
    "Consultancy reporting on the Sep-2025 redistribution and 2026 duty change",
    CO, "2025-09-08", fiscal_period="Q1-2025/26",
    model_impact="THE mix driver: share of output at subsidized vs free-local vs export "
                 "price, plus the export-duty wedge on the realized export price. The "
                 "Sep-2025 cut is why the FY2025/26 export mix and margin jumped.")

f_gasav = R.add(Ring.COUNTRY, "fiscal / political events with sector read-through", FindingClass.S,
    "Egypt's gas deficit forces summer industrial rationing (households and power first): "
    "producers were curtailed up to ~50% in the 2025 and 2026 summers; KIMA expensed "
    "factory-stoppage costs of EGP 152.7m (FY2023/24) and 164.5m (FY2024/25) and booked "
    "abnormal gas losses of ~EGP 781m cumulative FY2022/23-FY2024/25 (~249m in FY2024/25 "
    "alone); its Q1-2025/26 gas loss was 31.3m m3 (~EGP 251m) with August-2025 usage at "
    "8,492 m3/t against a 1,200 m3/t standard because plants burned gas idling/restarting",
    "Auditor's reports on the audited FY2024/25 statements and Q1-2025/26 limited "
    "review; S&P Global gas-cut coverage", CO, "2025-11-13", fiscal_period="Q1-2025/26",
    model_impact="Volume driver's availability haircut (utilisation capped below design "
                 "by summer gas cuts) and a standing abnormal-gas-cost line in the "
                 "cost stack.")

# ================================ RING 3 — INDUSTRY ==========================
f_cap = R.add(Ring.INDUSTRY, "demand drivers & capacity/supply balance", FindingClass.S,
    "Egypt operates ~7.2-7.3 Mt/y of urea capacity (Abu Qir, MOPCO, AlexFert, Helwan, "
    "KIMA, NCIC); domestic subsidized demand takes the administered share and the "
    "balance exports through Mediterranean ports. KIMA is the smallest gas-based "
    "producer (~0.57 Mt/y design) and the only one located 1,000km inland at Aswan",
    "Discovery Alert Egypt-nitrogen supply analysis; capacity plates per Tecnimont "
    "project record and note 28 benchmarks (1,200 t/d ammonia / 1,575 t/d urea)",
    PRESS, "2026-03-25",
    model_impact="Caps the volume driver at design capacity; the Aswan location makes "
                 "freight-to-port its own explicit cost line (EGP 610m in FY2024/25).")

f_price = R.add(Ring.INDUSTRY, "pricing", FindingClass.S,
    "Three-tier realized pricing: subsidized ~EGP 6,000/t; local free-market urea "
    "reached EGP 14,600/t by Jun-2024 (auditor) and sacks of EGP 1,400-1,600/50kg "
    "(~EGP 28-32k/t) by mid-2026 as the EGP price caught the world price; export FOB "
    "Egypt $545/t front month (Aug-2026) after $710-720/t placements in Mar-2026. "
    "KIMA's Q1-2025/26 export prices rose 43% y/y (auditor)",
    "Auditor's reports (FY2023/24, Q1-2025/26); CME FOB Egypt quote; Al Manassa / "
    "Mada Masr local-market reporting", CO, "2026-08-07", fiscal_period="Q1-2025/26",
    model_impact="Sets the three price legs of the revenue build separately — never one "
                 "blended realized price.")

f_entrant = R.add_negative(Ring.INDUSTRY, "new entrants (named-competitor level)",
    "new Egyptian nitrogen/urea plant announcements 2025-2026 beyond existing producers' "
    "debottlenecks (searched: Egypt new urea plant 2026, NCIC expansion, green ammonia "
    "greenfield urea)", SWEEP_DATE)

f_tech = R.add(Ring.INDUSTRY, "technology substitution", FindingClass.C,
    "Green-ammonia projects (Scatec/Egypt Green at Ain Sokhna and successors) target "
    "export bunkering/hydrogen niches, not the domestic subsidized urea system; no "
    "commercial displacement of gas-based urea inside the forecast window",
    "Egypt green-hydrogen program coverage", PRESS, "2026-01-15")

f_peers = R.add(Ring.INDUSTRY, "competitor capacity / price moves (named)", FindingClass.S,
    "Named peers: Abu Qir Fertilizers (ABUK, ~2 Mt/y, EGX-listed — KIMA holds a 2.7% "
    "stake it began selling down in H1-2025/26) and MOPCO (Damietta) were curtailed by "
    "up to ~50% in the 2026 gas squeeze; both sit on the coast with structurally lower "
    "freight than Aswan. ABUK also acts as KIMA's ammonia export marketer (12% of the "
    "export price per the disputed FY2024/25 contract)",
    "S&P Global curtailment coverage; ABUK relationship per the auditor's report on the "
    "audited FY2024/25 statements", CO, "2026-03-04",
    model_impact="Peer KPI/multiple cross-checks (ABUK margins, EV/t); the ammonia-"
                 "marketing fee stays in the selling-cost stack.")

# ================================ RING 4 — COMPANY ===========================
f_fs22 = R.add(Ring.COMPANY, "official financial statements", FindingClass.D,
    "Audited FY2021/22 (comparatives in the FY2022/23 filing): revenue 4,440.7m, gross "
    "2,117.7m (47.7%), net 651.5m; equity 4,891.2m; KIMA-2 USD loan 6,232.1m incl. "
    "current portion",
    "Audited financial statements FY2022/23 (Central Auditing Organization + PKF), "
    "kimaegypt.com IR portal", CO, "2023-10-08", is_fs_data=True, fiscal_period="FY2021/22",
    model_impact="First year of the four-year statement history the model chains from.")

f_fs23 = R.add(Ring.COMPANY, "official financial statements", FindingClass.D,
    "Audited FY2022/23: revenue 6,612.2m (gas year: urea +2% over design at ~586kt), "
    "gross 3,037.7m (46.0%), net 1,150.8m; capex a mere 42.5m — KIMA-2 complete, "
    "pre-ANNA; dual-audited (state CAO + PKF Rashed Badr & Co)",
    "Audited financial statements FY2022/23, kimaegypt.com IR portal",
    CO, "2023-10-08", is_fs_data=True, fiscal_period="FY2022/23",
    model_impact="Peak-utilisation reference year for the volume driver's upper leg.")

f_fs24 = R.add(Ring.COMPANY, "official financial statements", FindingClass.D,
    "Audited FY2023/24: revenue 6,532.1m, net 2,537.9m — but 2,034.6m of that is a "
    "ONE-OFF investment-property revaluation gain; underlying ~503m. Ammonia/urea "
    "output fell ~29%/~11% on gas cuts; EGP tranche of the KIMA-2 loan fully repaid "
    "June-2024; EGP 4bn capital increase (3,066.7m cash + 933.3m holdco debt-to-equity)",
    "Audited financial statements FY2023/24, kimaegypt.com IR portal",
    CO, "2024-10-23", is_fs_data=True, fiscal_period="FY2023/24",
    model_impact="Base-cleaning: the revaluation gain is stripped from every margin and "
                 "ROE read; the trough-utilisation reference for the volume driver.")

f_fs25 = R.add(Ring.COMPANY, "official financial statements", FindingClass.D,
    "Audited FY2024/25: revenue 8,602.6m split EXPORT 6,608.8m / LOCAL 1,993.8m (note "
    "20), gross 3,302.3m (38.4%), net 987.0m; production urea 513,385t @ EGP 7,509/t, "
    "ammonia 318,242t @ 9,114/t, AN 26,058t, nitric acid 35,590t (auditor cost table); "
    "COGS: materials 4,398.6m / wages 212.9m / depreciation 776.5m; selling includes "
    "freight-to-port 610.2m; finance cost 1,460.9m of which USD-loan interest 1,338.0m; "
    "debt 12.18bn (USD tranche ~$233m + holdco 596.9m); cash 3,057.0m; zero dividends",
    "Audited financial statements FY2024/25 (Central Auditing Organization, report "
    "23-Sep-2025), kimaegypt.com IR portal", CO, "2025-09-24", is_fs_data=True,
    fiscal_period="FY2024/25",
    model_impact="The anchor year: every forecast driver chains off this base.")

f_q1 = R.add(Ring.COMPANY, "regular disclosures", FindingClass.D,
    "Q1-2025/26 (limited review, state auditor + Nasr Abou El Abbas/Morison Global): "
    "revenue 1,184.8m (+23.6% y/y), gross 389.8m; auditor: urea export volumes +34%, "
    "export prices +43% y/y; net 482.7m incl. +357.2m FX gain",
    "Q1-2025/26 interim statements (16-Nov-2025 filing), kimaegypt.com IR portal",
    CO, "2025-11-16", is_fs_data=True, fiscal_period="Q1-2025/26",
    model_impact="Study-year actuals: sets the FY2025/26 volume/price/mix starting run.")

f_h1 = R.add(Ring.COMPANY, "regular disclosures", FindingClass.D,
    "H1-2025/26: revenue 4,156.4m, gross 1,672.6m (40.2%), net 1,190.0m incl. +383.9m "
    "FX gain; holdco loan repaid down to 45.96m; part of the ABUK stake SOLD "
    "(~559.8m proceeds in the 9M cash flow)",
    "H1-2025/26 interim statements (15-Feb-2026 filing), kimaegypt.com IR portal",
    CO, "2026-02-15", is_fs_data=True, fiscal_period="H1-2025/26",
    model_impact="Confirms the mix-shift margin; updates the non-operating asset stack "
                 "for the EV-to-equity bridge.")

f_9m = R.add(Ring.COMPANY, "regular disclosures", FindingClass.D,
    "9M-2025/26: revenue 7,314.9m (+14.5% y/y), gross 3,135.0m (42.9%), net 531.3m "
    "AFTER a 1,072.0m FX loss (Q3 alone -1,455.9m as USD/EGP went ~47 to ~50.4 on "
    "~$260-290m USD debt); operationally Q3 was the best quarter on record (revenue "
    "3,158.6m, gross 46.3%). Company budget column: 9M budget net 1,021.9m. ANNA CWIP "
    "5,653.5m; ANNA loan draws 1,585.8m in 9M",
    "9M-2025/26 interim statements (21-May-2026 filing), kimaegypt.com IR portal",
    CO, "2026-05-21", is_fs_data=True, fiscal_period="9M-2025/26",
    model_impact="TTM base for the strike; quantifies the FX-translation channel that "
                 "the fair-value range must carry as a sensitivity; the budget column "
                 "is the sourced near-term cost anchor the cost stack must cite.")

f_anna = R.add(Ring.COMPANY, "strategic plans & guidance", FindingClass.S,
    "ANNA project (nitric acid + ammonium nitrate, Tecnimont/Orascom consortium): "
    "final bank-approved cost EGP 6,422.4m + US$278.4m (agreement 25-Jun-2025), "
    "financed US$82.9m + EGP 5,930.7m amortizing to 2035/2036; contract $245.0m + "
    "EGP 1,611m signed 12-Oct-2023; execution 8.3% vs 21.7% plan (30-Jun-2025), "
    "12.9% vs 37% (30-Sep-2025); a holding-company committee (9-Apr-2025) found "
    "'severe deficiencies' in the award process. Purpose: convert surplus ammonia "
    "capacity (design 438kt vs urea's ~297kt need) into AN products",
    "Note 18-3 and auditor's reports, audited FY2024/25 + Q1-2025/26 filings",
    CO, "2025-09-24", fiscal_period="FY2024/25",
    model_impact="Capex driver (bottom-up from the approved cost and draw schedule) and "
                 "debt build; ANNA revenue is carried as an explicit SCENARIO leg, not "
                 "in the base FCFF, given 2-year delay track and governance findings.")

f_ir = R.add(Ring.COMPANY, "IR communications (calls, presentations, releases)", FindingClass.C,
    "KIMA's IR channel is the Mist-hosted portal: quarterly board & shareholder-"
    "structure disclosure reports (latest 30-Jun-2026), news feed, share-price page. "
    "No investor presentations or earnings calls exist — volumes/prices/utilisation "
    "reach the record only through the statutory auditor's tables, which this sweep "
    "therefore mines as the de-facto IR disclosure",
    "KIMA IR portal index (Disclosure Reports section, item dated 30-Jun-2026), "
    "mistnews.com via kimaegypt.com", IR, "2026-06-30")

f_neg_ir = R.add_negative(Ring.COMPANY, "IR communications (calls, presentations, releases)",
    "KIMA investor presentation, earnings call transcript, guidance deck (searched IR "
    "portal index + web: 'KIMA investor presentation', 'كيما مؤتمر المحللين')", SWEEP_DATE)

f_reval = R.add(Ring.COMPANY, "one-off base-resetting transactions", FindingClass.B,
    "Three base-resetting events: (1) FY2023/24 investment-property revaluation gain "
    "EGP 2,034.6m (one-off, in net profit); (2) Mar-2024 capital increase EGP 4bn to "
    "9,932.9m paid-in (1,986,578,999 shares x EGP 5); (3) H1-2025/26 partial sale of "
    "the ABUK stake (~559.8m proceeds; FVOCI assets 2,163.3m -> 1,382.9m by Mar-2026). "
    "Also: ferrosilicon furnace (idle since 2019) leased to a Saudi tenant from "
    "May-2025 — ferrosilicon is now rental income, not production",
    "Audited FY2023/24 and FY2024/25 statements; H1/9M-2025/26 interims",
    CO, "2026-05-21", is_fs_data=True, fiscal_period="FY2024/25",
    model_impact="Dual-framing on FY2023/24 profit (with/without the gain); share count "
                 "and equity base reset; the non-operating bridge marks the REMAINING "
                 "stakes at market and the ferrosilicon leg becomes a rental line.")

f_own = R.add(Ring.COMPANY, "ownership / stake changes (named-transaction rule)", FindingClass.C,
    "Register (note 14, 30-Jun-2025): Chemical Industries Holding 69.825%, public-"
    "sector workers' insurance fund 19.27%, Banque Misr 3.78%, business-sector "
    "insurance fund 0.94%, individuals 6.184% — free float ~6.2%, consistent with the "
    "thin-trading diagnostics in the beta build. Offtake: Ameropa AG agreement "
    "1-Nov-2024, ~30kt/month (~67% of production), one year renewable to Oct-2025, "
    "signed at the funding banks' request",
    "Note 14 + auditor's report, audited FY2024/25 statements", CO, "2025-09-24",
    fiscal_period="FY2024/25")

f_mgmt = R.add(Ring.COMPANY, "management & capital actions", FindingClass.S,
    "Zero dividends in FY2023/24 and FY2024/25 (appropriation statements: all retained "
    "after legal reserve) — q=0 is SOURCED, not assumed; the 500m holdco loan drawn "
    "FY2024/25 at ~19.4% was repaid to 45.96m by Dec-2025; gas arrears are being "
    "rescheduled with Petrotrade (25.98m rescheduling interest in FY2024/25, 35m "
    "late-fine provision); KIMA-1 fire (21-Mar-2025, 12m cost) repaired, plant "
    "restarted 29-Jul-2025",
    "Appropriation statements and notes 16/26, audited FY2024/25 statements",
    CO, "2025-09-24", fiscal_period="FY2024/25",
    model_impact="q_annual=0 in the cone strike; working-capital driver carries the "
                 "gas-arrears financing behavior; no buyback/dividend leg in the bridge.")

# ---------------- negative searches closing remaining coverage ---------------
f_neg_capex = R.add_negative(Ring.COMPANY, "strategic plans & guidance",
    "maintenance-capex guidance or an investment plan beyond ANNA (searched filings' "
    "board reports + news: 'كيما خطة استثمارية', 'KIMA capex plan')", SWEEP_DATE)

# ============================ DRIVER GATE TABLE ==============================
R.add_driver("Urea volumes (tonnes)", DriverMode.BOTTOM_UP,
    "Design capacity 574,875 t/y (1,575 t/d, note 28 benchmark) with actuals 586kt "
    "(FY2022/23) / 522kt (FY2023/24) / 513kt (FY2024/25) from the auditor's own "
    "production tables; forecast utilisation banded by the gas-availability pattern "
    "(summer cuts) and the Q1-2025/26 +34% export-volume print.",
    [f_fs25, f_q1, f_gasav, f_cap])
R.add_driver("Realized price mix (subsidized / local free / export)", DriverMode.BOTTOM_UP,
    "Note 20 gives the FY2024/25 export/local revenue split (6,608.8m/1,993.8m); the "
    "quota decrees set the administered shares and their Sep-2025 reset; FOB Egypt "
    "$545/t and the EGP 2,500/t-to-10% duty wedge price the export leg; EGP 6,000/t "
    "prices the subsidized leg.",
    [f_fs25, f_quota, f_price, f_urea])
R.add_driver("Natural-gas cost (feedstock + fuel)", DriverMode.BOTTOM_UP,
    "Priced as USD formula price ($5.75/mmBtu, note 28) x usage (1,025-1,771 m3/t "
    "urea, auditor) x USD/EGP path — a commodity input escalating on its own USD path "
    "through FX, never a domestic-CPI proxy (cost-stack escalation rule); the abnormal-"
    "loss history (781m cumulative) carries as a standing inefficiency line.",
    [f_fs25, f_urea, f_gasav])
R.add_driver("Non-gas cost stack (wages, services, electricity, freight)", DriverMode.BOTTOM_UP,
    "Two escalator classes: the domestic lines (wages 212.9m, services, other materials, "
    "freight-to-port 610.2m per export tonne, other selling and administration, all FY2024/25) "
    "share the domestic inflation path, while gas, the export price and the subsidised price "
    "each carry their own; every unit rate is anchored on the FY2024/25 auditor's product-cost "
    "table and the reviewed FY2025/26 quarters. The company's own budget column in the 9M "
    "interim is registered and scored against the outturn; no driver consumes it.",
    [f_fs25, f_9m])
R.add_driver("Depreciation & amortization", DriverMode.BOTTOM_UP,
    "Note 6 register: KIMA-2 machinery at 3.95%/yr, intangible usufruct at 4.75%/yr; "
    "FY2024/25 charge 771.2m + 119.4m amortization; ANNA assets phase in on "
    "commissioning at the same class rates.",
    [f_fs25, f_anna])
R.add_driver("Capex", DriverMode.BOTTOM_UP,
    "ANNA from its bank-approved cost (EGP 6,422.4m + $278.4m) and observed draw pace "
    "(CWIP 3,790.2m -> 5,653.5m in nine months); maintenance capex from the pre-ANNA "
    "observed run (42.5-81m/yr FY2022-23) uplifted for age — the one leg without "
    "guidance, so it is sensitized.",
    [f_anna, f_9m, f_neg_capex])
R.add_driver("Cost of debt / WACC glide", DriverMode.BOTTOM_UP,
    "The USD consortium loan's actual interest (1,338.0m FY2024/25 on ~$233m = ~11.5% "
    "USD, carried at local-equivalent cost), the holdco loan's 19.4% EGP print, and "
    "the ANNA loan schedule to 2035/36 give a fully-sourced Kd; rf* from the live 10Y "
    "less the sovereign's own default spread.",
    [f_fs25, f_anna, f_cbe])
R.add_driver("ANNA revenue leg", DriverMode.BOTTOM_UP,
    "Carried as an explicit scenario (not base FCFF): bank-approved cost, capacity "
    "purpose (converting the 438kt ammonia design surplus into AN), and the delay/"
    "governance record are all disclosed; the scenario prices completion in 2029-2030 "
    "against the sunk-capex base case.",
    [f_anna, f_fs25])
R.add_driver("Dividend / distribution policy (q)", DriverMode.BOTTOM_UP,
    "q=0 sourced from two consecutive appropriation statements (zero proposed both "
    "years); flagged to revisit when leverage normalises.",
    [f_mgmt, f_fs25])

f_hist = R.add(Ring.COMPANY, "long-run reported history (calibration of the method)", FindingClass.S,
    "Eighteen fiscal years of the company's own audited statements, FY2008-FY2025, read from the "
    "rendered pages and footed subtotal by subtotal (17 of 18 years foot on every line; the 2014 "
    "annual is a 367x519-pixel scan carried only for the blocks that foot). The old Aswan plant "
    "was shut in FY2019 and the gas-fed complex commissioned through FY2020-FY2021 with two loss "
    "years between; revenue FY2018 571m, FY2021 1,399m, FY2022 4,441m, FY2025 8,603m EGP",
    "Audited annual statements for the years to 30 June 2009-2021 from the company's IR portal "
    "(engine/egch_walkforward/panel.py carries every figure with its footing)", CO, "2026-09-01",
    model_impact="Tests the forecasting method on the company's own past before it is trusted on "
                 "its future: years three to five of the forecast are published as ranges from "
                 "the measured error distribution, and the terminal inflation is reconciled to "
                 "terminal growth.", is_fs_data=True)

# ------------------------------------------------------------------ OUTPUT
errors, warnings = R.validate()
R.to_json(os.path.join(HERE, 'sweep_register.json'))
print(R.qc_line())
print(f"\nfindings: {len(R.findings)} | drivers: {len(R.drivers)}")
if errors:
    print(f"\nVALIDATOR ERRORS ({len(errors)}):")
    for e in errors:
        print(f"  ! {e}")
if warnings:
    print(f"\nwarnings ({len(warnings)}):")
    for w in warnings:
        print(f"  - {w}")
fr = R.check_freshness(SWEEP_DATE)
print(f"\nfreshness: {fr or 'OK — sweep and delivery same day'}")
