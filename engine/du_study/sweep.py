"""DU — four-ring Information Sweep register (Step 2A). Runs BEFORE any
forecast driver is set. Every mandatory category of every ring is closed by a
dated finding or a dated negative search.

Primary access succeeded end-to-end this build: investors.du.ae served the
audited FY2023/FY2024/FY2025 annual reports and both 2026 reviewed interims
directly, so every Company-ring financial figure is COMPANY_OFFICIAL from the
filings themselves. The one primary-source failure worth recording is UAE
sovereign CDS (cbonds 403; Damodaran prints NA) — logged, proxied by the traded
Abu Dhabi USD spread, never silently substituted.
"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from research_sweep import (SweepRegister, AssetClass, Ring, FindingClass,
                            SourceType, DriverMode)

SWEEP_DATE = "2026-08-09"
R = SweepRegister("DU", AssetClass.STOCK, SWEEP_DATE)
CO, IR, REG, PMD, PRESS, AGG = (SourceType.COMPANY_OFFICIAL, SourceType.COMPANY_IR,
                                SourceType.REGULATOR_OFFICIAL, SourceType.PRIMARY_MARKET_DATA,
                                SourceType.REPUTABLE_PRESS, SourceType.AGGREGATOR)

R.record_primary_access("https://investors.du.ae/", True, SWEEP_DATE,
                        "IR portal reachable; served AR2023/AR2024/AR2025 PDFs, Q1-2026 and "
                        "H1-2026 reviewed FS, earnings releases and analyst decks directly")
R.record_primary_access("https://www.du.ae/about-us/investor-relations", True, SWEEP_DATE,
                        "301 -> investors.du.ae")
R.record_primary_access("https://pages.stern.nyu.edu/~adamodar/ (ctryprem)", True, SWEEP_DATE,
                        "UAE row read fresh from the original dataset, 05-Jan-2026 update")
R.record_primary_access("https://api2.dfm.ae/web/widgets/v1/data (DFM index API)", True,
                        SWEEP_DATE, "official DFMGI closes 2025-2026; spliced with "
                        "cross-validated Yahoo history for 2021-2024 (identical on all 307 "
                        "overlapping sessions)")
R.record_primary_access("FTSE ADX General index history (user-supplied investing.com export, 2011..24-Jul-2026)", True, "2026-08-10",
                        "adopted per user instruction as the UAE base market index for the beta regression; DFM General retained as the published alternative")
R.record_primary_access("cbonds/worldgovernmentbonds UAE 5y CDS", False, SWEEP_DATE,
                        "403 / JS-only; UAE CDS also NA in Damodaran — market-spread basis "
                        "built from the traded Abu Dhabi USD 10y (+25bp) instead, and both "
                        "ERP bases are published")

R.declare_study_year("2026", ["Q1-2026", "Q2-2026"])

# ---------------------------------------------------------------- RING 1 GLOBAL
f_rate = R.add(Ring.GLOBAL, "rate cycle & USD/FX regime", FindingClass.S,
    "Fed at 3.50-3.75% with ZERO 2026 cuts delivered and markets pricing possible hikes "
    "(~4% year-end); US 10Y 4.68% (08-Aug-2026). The AED is hard-pegged, so this is the UAE "
    "rate anchor: AED T-bond Jan-2031 auctioned at 4.48% (22-Jul-2026), through UST at +4bp",
    "US Treasury market / UAE MoF T-bond auction results / house FED_SCHEDULE", PMD,
    "2026-08-08",
    model_impact="Sets rf 4.48% (AED, longest liquid tenor) and keeps the WACC glide SHALLOW "
                 "(terminal rf 4.30%) — a hiking tail risk argues against assuming cheap "
                 "terminal money.")
f_oil = R.add(Ring.GLOBAL, "commodity complex (input/output)", FindingClass.C,
    "Oil averaging ~$89/bbl in 2026 (IMF July-2026 assumption) — a fiscal TAILWIND for the "
    "UAE state (du's controlling shareholder base and its enterprise/government demand), not "
    "a cost line: du's cost stack is interconnect, staff, network and licence fees, none "
    "oil-indexed",
    "IMF WEO Update, July 2026", REG, "2026-07-29",
    model_impact="No per-unit energy escalator needed in the cost stack (unlike an "
                 "energy-conversion business); UAE fiscal strength supports the "
                 "government/enterprise ICT demand line.")
f_gdem = R.add(Ring.GLOBAL, "global sector demand", FindingClass.S,
    "Global telecom 2026: low-single-digit service-revenue growth, 5G monetisation via FWA "
    "and B2B, and an AI/data-centre capex supercycle pulling telcos into hyperscaler "
    "partnerships — the exact leg du is building (Microsoft hyperscale anchor tenancy)",
    "Sector coverage (press synthesis, labelled)", PRESS, "2026-06-30",
    model_impact="Supports the ICT segment's +8-11% growth path and the elevated 15.5% "
                 "near-term capex intensity.")
f_trade = R.add(Ring.GLOBAL, "trade / sanctions / supply chains", FindingClass.S,
    "US/Israel-Iran war from 28-Feb-2026: Hormuz disruption, Gulf security fears, regional "
    "tourism collapse. Ceasefire in place; IMF baseline has Hormuz reopening from mid-July "
    "2026 and prewar conditions by March 2027, with re-escalation the named top downside",
    "IMF WEO Update July 2026 + regional coverage", REG, "2026-07-29",
    model_impact="THE swing factor for prepaid subscribers, roaming and wholesale transit: "
                 "the base case assumes recovery through H2-2026/2027 (mobile base "
                 "9.28m -> 9.45m by end-2026); the bear scenario re-opens the conflict.")

# ---------------------------------------------------------------- RING 2 COUNTRY
f_macro = R.add(Ring.COUNTRY, "sovereign macro (inflation, policy rate, FX/deval risk)",
    FindingClass.S,
    "UAE real GDP ~5.6% (2025), ~3-5.6% forecast 2026 (IMF Apr-2026 WEO 3.1%; CBUAE ~5%); "
    "CPI ~1.8-2.5%; CBUAE base rate 3.65% tracking the Fed under the hard peg; Aa2/stable; "
    "MENA regional growth slashed to 0.7% for 2026 by the July WEO Update on the war, "
    "rebounding 6.5% in 2027",
    "IMF WEO Apr-2026 + July-2026 Update; CBUAE", REG, "2026-07-29",
    model_impact="Terminal nominal growth 2.5% sits well inside long-run nominal GDP ~4%+; "
                 "no FX/deval leg in an AED model (hard peg, Aa2).")
f_reg = R.add(Ring.COUNTRY, "regulatory environment (regulator, caps, tariffs, tax/subsidy)",
    FindingClass.B,
    "TDRA licence: the FY2025/H1-2026 notes disclose the licence term extended only to "
    "08-Aug-2026 with renewal 'in final stage, expected to conclude on or before August 8, "
    "2026' — i.e. the licence horizon expires within days of this study's anchor. Licence "
    "fees run 2.7% of revenue. No public announcement of concluded terms was found by the "
    "sweep date (negative search logged below)",
    "du H1-2026 reviewed FS Note 5 (licence) + AR2025", CO, "2026-07-22",
    model_impact="Base case carries renewal on comparable terms (fees held at 2.70% of "
                 "revenue); a renewal on materially worse terms is priced in the crux "
                 "sensitivity (each +1pp of revenue in licence fees is ~AED -1.0/share).")
f_fiscal = R.add(Ring.COUNTRY, "fiscal / political events with sector read-through",
    FindingClass.B,
    "THE CONTESTED JUDGEMENT'S EVIDENCE BASE: the 38% federal royalty + 9% CT regime "
    "(combined floor AED 1.8bn/yr) is legislated 2024-2026 (Cabinet 8/38 of 2023). du's own "
    "H1-2026 notes (22-Jul-2026) still describe 2024-2026 only. e&'s market disclosure of an "
    "MoF notification dated 17-Jul-2026 reports a THREE-YEAR EXTENSION (2027-2029) on the "
    "same structure — peer-operator disclosure, not yet mirrored in du's own filings",
    "du H1-2026 FS Note 14 (COMPANY_OFFICIAL) + e& disclosure of MoF notification (17-Jul-2026)",
    REG, "2026-07-17",
    model_impact="Framing A (base): 43.6% combined take persists. Framing B: reversion to the "
                 "pre-2024 construction (15% regulated revenue + 30% regulated profit = 51-53% "
                 "take). BOTH computed: AED 19.14 vs 16.29 per share on the DCF.")

# ---------------------------------------------------------------- RING 3 INDUSTRY
f_dem = R.add(Ring.INDUSTRY, "demand drivers & capacity/supply balance", FindingClass.S,
    "UAE telecom demand = population + tourism + enterprise digitalisation. Dubai population "
    "growth slowed to 1.55% in Q1-2026 on the war then RE-ACCELERATED to 1.86% in Q2 (4.74m "
    "end-Q2); tourism collapsed (hotel occupancy projections ~80% -> ~10%, March airport "
    "traffic -66%) and is now recovering under the ceasefire",
    "Dubai Statistics Center / press coverage of the tourism shock", PRESS, "2026-07-15",
    model_impact="Drives the subscriber paths: prepaid recovery +170k in H2-2026, then "
                 "+210-310k/yr — below the 2025 boom (+788k), above the conflict trough.")
f_price = R.add(Ring.INDUSTRY, "pricing", FindingClass.S,
    "UAE mobile pricing is rational-duopoly: du's blended mobile ARPU printed 63.3-63.4 "
    "AED/month across FY2025-Q2-2026 (company KPI) with postpaid +9% y/y mix gain offsetting "
    "prepaid dilution — no price war anywhere in the disclosure record",
    "du quarterly presentations (ARPU series)", IR, "2026-07-23",
    model_impact="ARPU path held essentially flat (+0.3%/yr); the ±8% ARPU sensitivity spans "
                 "AED 15.9-22.4 on the DCF.")
R.add_negative(Ring.INDUSTRY, "new entrants (named-competitor level)",
    "UAE third mobile licence / new MVNO 2025-2026 (TDRA announcements, press)", SWEEP_DATE)
f_tech = R.add(Ring.INDUSTRY, "technology substitution", FindingClass.S,
    "5G-Advanced/FWA substitutes fixed broadband (du deployed world-first L-Band + U6GHz "
    "next-gen 5G, Q2-2026); satellite D2D remains complementary at UAE price points; "
    "data-centre/AI services substitute legacy ICT resale — du is building five DCs plus a "
    "$544.5m hyperscale campus with Microsoft as anchor tenant",
    "du Q2-2026 presentation + Microsoft/du announcement (Apr-2025)", IR, "2026-07-23",
    model_impact="Underwrites the fixed segment's +4.5-7.5% growth (FWA share gain) and the "
                 "ICT ramp; also the 15.5% capex peak.")
f_comp = R.add(Ring.INDUSTRY, "competitor capacity / price moves (named)", FindingClass.S,
    "e& (EAND, the incumbent, ~2/3 mobile share historically): FY2025 DPS raised to 90 fils "
    "with 95 fils guided for FY2026 — the duopoly is in harvest-and-distribute mode, not "
    "land-grab; Mobily (KSA #2, the closest structural analogue) trades ~15.5x trailing P/E",
    "e& IR dividend policy + aggregator multiple reads (labelled cross-check)", PRESS,
    "2026-08-08",
    model_impact="Peer P/E median 15.5x anchors the relative lens; duopoly rationality "
                 "supports flat-ARPU and stable contribution margins.")

# ---------------------------------------------------------------- RING 4 COMPANY
f_guide = R.add(Ring.COMPANY, "strategic plans & guidance", FindingClass.S,
    "FY2026 guidance CUT at the Q2 print (23-Jul-2026): revenue growth 4-6% (from 5-7% set "
    "Feb-2026 and explicitly maintained 22-Apr-2026); EBITDA margin confirmed 46-47%. The "
    "interim dividend was RAISED 8.3% to 26 fils in the same release",
    "du Q2-2026 earnings release", IR, "2026-07-23", fiscal_period="Q2-2026",
    model_impact="FY2026E revenue build lands +4.3%, inside the revised band; the margin "
                 "OUTPUT (47.1%) sits just above guidance because H1 already printed 49.2%.")
f_fs25 = R.add(Ring.COMPANY, "official financial statements", FindingClass.B,
    "FY2025 audited consolidated FS (KPMG, unmodified, 09-Feb-2026): revenue 15,905.421mn "
    "(+8.7%), EBITDA 7,338.388mn (46.1%), net profit 2,905.085mn, EPS 0.64, zero borrowings, "
    "net cash 2,249.7mn before leases 1,938.8mn; DPS 0.64 (~100% payout)",
    "Integrated Annual Report 2025, investors.du.ae", CO, "2026-02-09",
    is_fs_data=True, fiscal_period="FY2025",
    model_impact="The roll-forward base for every statement line in the model.")
f_fs24 = R.add(Ring.COMPANY, "official financial statements", FindingClass.C,
    "FY2024 audited FS (PwC, unqualified, 10-Feb-2025): revenue 14,635.917mn, net profit "
    "2,487.547mn; first year of the 38%+9% regime (combined 44.7%/42.2% takes on the two "
    "presentation bases)",
    "Annual Report 2024, investors.du.ae", CO, "2025-02-10", is_fs_data=True,
    fiscal_period="FY2024",
    model_impact="Second audited year; carries the FY2023 royalty-accrual disclosure that "
                 "makes the working-capital series like-for-like.")
f_fs23 = R.add(Ring.COMPANY, "official financial statements", FindingClass.C,
    "FY2023 audited FS (PwC, unqualified, 13-Feb-2024): revenue 13,636.340mn, net profit "
    "1,667.851mn under the OLD royalty regime (53.1% take) — the evidence base for Framing B",
    "Annual Report 2023, investors.du.ae", CO, "2024-02-13", is_fs_data=True,
    fiscal_period="FY2023",
    model_impact="Third audited year (target met); prices the contested judgement's "
                 "reversion leg.")
f_fs22 = R.add(Ring.COMPANY, "official financial statements", FindingClass.C,
    "FY2022 complete comparatives (full IS/BS/CF columns in the audited FY2023 statements): "
    "revenue 12,754.492mn, net profit 1,219.561mn, EPS 0.27, total equity 8,770.152mn, zero "
    "borrowings (last term loan repaid during FY2022), old-regime royalty take",
    "Annual Report 2023 (FY2022 comparative columns), investors.du.ae", CO, "2024-02-13",
    is_fs_data=True, fiscal_period="FY2022",
    model_impact="Fourth complete fiscal year (target met): extends the margin, payout and "
                 "working-capital history behind the forecast ratios.")
f_q1 = R.add(Ring.COMPANY, "regular disclosures", FindingClass.C,
    "Q1-2026 reviewed FS (KPMG ISRE 2410): revenue 4,114.108mn (+6.9%), EBITDA margin 49.5%, "
    "net profit 834.177mn; balance sheet carried the AED 0.40 final dividend as payable",
    "Q1-2026 condensed consolidated interim FS, investors.du.ae", CO, "2026-04-22",
    is_fs_data=True, fiscal_period="Q1-2026",
    model_impact="First study-year quarter, swept in BEFORE the build.")
f_q2 = R.add(Ring.COMPANY, "regular disclosures", FindingClass.B,
    "H1-2026 reviewed FS (KPMG, 22-Jul-2026): H1 revenue 8,197.573mn (+5.8%), EBITDA "
    "4,031.922mn (49.2%), net profit 1,631.971mn (+12.6%); 30-Jun balance sheet: cash "
    "307.2mn, term deposits NIL (Q2 absorbed ~4.1bn of royalty + final dividend), leases "
    "1,735.1mn, AED 2.0bn RCF undrawn; Q2 mobile net adds -412k (prepaid -442k, war)",
    "H1-2026 condensed consolidated interim FS, investors.du.ae", CO, "2026-07-22",
    is_fs_data=True, fiscal_period="Q2-2026",
    model_impact="FY2026E = H1 ACTUAL + unit-built H2; the war's subscriber damage is in the "
                 "base, not assumed away.")
f_ir = R.add(Ring.COMPANY, "IR communications (calls, presentations, releases)",
    FindingClass.D,
    "Quarterly KPI series from the analyst decks: mobile subscribers 8,916k (Q4-24) -> "
    "9,704k (Q4-25) -> 9,280k (Q2-26); prepaid/postpaid split; fixed 682k -> 744k; blended "
    "mobile ARPU 63.3-65.8 AED/mo; capex intensity by quarter; opFCF = EBITDA - capex. None "
    "of this appears in any financial statement — this is the disclosure that CONVERTS the "
    "mobile and fixed forecasts from top-down to bottom-up (subscribers x ARPU)",
    "du quarterly analyst presentations + earnings releases (Q4-2025 through Q2-2026)", IR,
    "2026-07-23", fiscal_period="Q2-2026",
    model_impact="DRIVER UNLOCK: mobile revenue = avg base x ARPU x 12 reproduces the "
                 "audited FY2025 segment to -0.04%; both unit paths are forecast drivers.")
f_spo = R.add(Ring.COMPANY, "ownership / stake changes (named-transaction rule)",
    FindingClass.C,
    "NAMED TRANSACTION: Secondary Public Offering of 342,084,084 du shares (7.55% of capital) "
    "by Mamoura Diversified Global Holding PJSC (Mubadala subsidiary) — 75% of its du stake — "
    "completed 2025, widening free float; Emirates Investment Authority remains the "
    "controlling shareholder. Also: Associated Group's holding amended to DH 8 LLC",
    "Integrated Annual Report 2025 (governance section), investors.du.ae", CO, "2026-02-09",
    model_impact="No control change; better float/liquidity supports the tier-1 own-index "
                 "beta regression's representativeness.")
f_cap = R.add(Ring.COMPANY, "management & capital actions", FindingClass.S,
    "Capital actions 2026: AED 2.0bn 7-year unsecured RCF signed 06-Apr-2026 (undrawn); "
    "final FY2025 DPS 0.40 paid 28-Apr-2026; interim 0.26 declared 23-Jul-2026 (+8.3%); "
    "du Ventures $50m VC fund launched Q2-2026 (Shorooq partnership); two Cayman SPVs "
    "incorporated H1-2026 (Investment Company 1/2)",
    "H1-2026 FS notes + Q2-2026 release", CO, "2026-07-23", fiscal_period="Q2-2026",
    model_impact="98% payout carried forward; liquidity backstop lets the balance sheet run "
                 "to near-zero term deposits through the capex peak without new equity.")
f_dc = R.add(Ring.COMPANY, "one-off base-resetting transactions", FindingClass.S,
    "The hyperscale data-centre programme: $544.5m (~AED 2.0bn) build with Microsoft as "
    "anchor tenant (announced Apr-2025), five DCs in operation/ramp, GPU-as-a-service and "
    "sovereign-cloud services launching from the Q4-2025 deck onwards; Q2-2026 capex +19.8% "
    "y/y on the DC/cloud/AI acceleration",
    "du announcements + Q4-2025/Q2-2026 decks", IR, "2026-07-23",
    model_impact="Resets the ICT growth base (+8-11%/yr) AND the capex path (15.5% of "
                 "revenue at peak, gliding to 13.0%) — both flagged as house paths on "
                 "sourced commitment evidence (commitments 2,411.8mn at 30-Jun-2026).")
R.add_negative(Ring.COMPANY, "one-off base-resetting transactions",
    "du M&A / acquisitions / disposals 2025-2026 beyond the DC programme and SPO "
    "(press, DFM disclosures)", SWEEP_DATE)
R.add_negative(Ring.COUNTRY, "regulatory environment (regulator, caps, tariffs, tax/subsidy)",
    "TDRA or du announcement of CONCLUDED licence-renewal terms (TDRA site, du IR "
    "disclosure list, DFM announcements, press)", SWEEP_DATE)
neg_whl = R.add_negative(Ring.COMPANY, "regular disclosures",
    "wholesale unit KPIs (transit minutes, IRU capacity, roaming volumes) anywhere in "
    "AR2023-AR2025, interim FS, or any analyst deck", SWEEP_DATE)
neg_ict = R.add_negative(Ring.COMPANY, "regular disclosures",
    "ICT/data-centre unit KPIs (racks, MW, utilisation, contract backlog) in any du "
    "disclosure; only programme-level capex and partner names are public", SWEEP_DATE)
neg_capex = R.add_negative(Ring.COMPANY, "strategic plans & guidance",
    "numeric FY2026 capex guidance in the Feb/Apr/Jul-2026 releases and decks "
    "(revenue growth and EBITDA margin are guided; capex is not)", SWEEP_DATE)
neg_regime = R.add_negative(Ring.COUNTRY, "fiscal / political events with sector read-through",
    "post-2026 royalty/CT regime in du's OWN filings and DFM disclosures (H1-2026 notes "
    "still say 'effective from 2024 to 2026'; the 17-Jul-2026 MoF extension notification "
    "is disclosed by e&, not yet by du)", SWEEP_DATE)

# ---------------------------------------------------------------- DRIVER GATE
R.add_driver("Mobile revenue (subscribers x ARPU)", DriverMode.BOTTOM_UP,
             "Company-disclosed quarterly subscriber base (prepaid/postpaid) and blended "
             "ARPU reproduce the audited segment to -0.04% in FY2025; both are forecast "
             "at unit level", [f_ir, f_fs25, f_dem])
R.add_driver("Fixed revenue (subscribers x implied revenue-per-sub)", DriverMode.BOTTOM_UP,
             "Subscriber base disclosed quarterly; revenue-per-sub is implied (consumer + "
             "enterprise blend) — unit build with the intensity metric flagged as implied",
             [f_ir, f_tech])
R.add_driver("Wholesale revenue", DriverMode.TOP_DOWN,
             "No unit KPIs (minutes/transit) disclosed anywhere in the record — FLAGGED: "
             "segment-level growth on the war-recovery path is the finest sourced level",
             [f_q2, f_trade, neg_whl])
R.add_driver("ICT & associated telecom revenue", DriverMode.TOP_DOWN,
             "No unit KPIs (racks/MW/contract book) disclosed — FLAGGED: segment-level "
             "growth on the sourced data-centre programme evidence",
             [f_dc, f_gdem, neg_ict])
R.add_driver("Segment contribution margins", DriverMode.BOTTOM_UP,
             "Disclosed per segment in Note 38 (two consistent years); held at audited "
             "FY2025 rates, ICT lifted on scale", [f_fs25])
R.add_driver("Opex stack (staff/network/marketing/licence/admin/ECL)", DriverMode.BOTTOM_UP,
             "Disclosed by nature on the face of the income statement; one escalator per "
             "driver class (wages, network scale, revenue-linked regulatory fee, CPI)",
             [f_fs25, f_q2]),
R.add_driver("Capex path (15.5% -> 13.0% of revenue)", DriverMode.TOP_DOWN,
             "No numeric FY2026 capex guidance published — FLAGGED as a house path anchored "
             "on disclosed commitments (2,411.8mn) and the disclosed DC programme",
             [f_dc, f_q2, neg_capex])
R.add_driver("Post-2026 fiscal regime (the contested judgement)", DriverMode.TOP_DOWN,
             "Not legislated in du's own filings beyond 2026; BOTH framings computed and "
             "published side by side", [f_fiscal, f_fs23, neg_regime])

errors, warnings = R.validate()
print(R.qc_line())
for w in warnings:
    print("WARN:", w)
fresh = R.check_freshness("2026-08-09")
if fresh:
    print("WARN:", fresh)
assert not errors, errors
R.to_json(os.path.join(HERE, 'sweep_register.json'))
print("wrote sweep_register.json |", R.counts())
