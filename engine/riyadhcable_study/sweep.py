"""Riyadh Cables (Tadawul 4142) — Step 2A four-ring Information Sweep register.
Imports the shared engine register (research_sweep.py) and its enforced invariants
(coverage, provenance, consequence, gate linkage, primary access, FS depth,
study-year quarter coverage, IR coverage). Writes sweep_register.json for the
bibliography document and the research-register appendix. Run before the build;
validated as QC item (m)."""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from research_sweep import (SweepRegister, AssetClass, Ring, FindingClass, SourceType,
                            DriverMode)

reg = SweepRegister("RIYADHCABLE", AssetClass.STOCK, "2026-08-18")

# ---- primary access: the company's own IR site + the escalation that unblocked it ----
reg.record_primary_access(
    "https://riyadh-cables.com/investor-relations/", False, "2026-08-18",
    note="The company IR site sits behind an 'sgcaptcha' bot-protection wall that blocked "
         "automated retrieval (HTTP 202 JS challenge to curl; empty render to the page "
         "fetcher; a headless browser could not complete the challenge). Verified NOT an "
         "egress-proxy fault (the proxy returned 200 for a control host and reached the "
         "company origin, receiving its challenge). Per the primary-source discipline, the "
         "analyst stopped and asked rather than substituting an aggregator; the requester "
         "then supplied the four audited annual statement sets directly — the rule working.")
reg.record_primary_access(
    "https://www.saudiexchange.sa/.../issuer-announcements-details/?anId=97051&cs=4142", True,
    "2026-08-18", note="Tadawul issuer-announcement portal — reachable; the official filed "
    "H1-2026 reviewed interim results announcement read here (revenue, gross profit, "
    "operating profit, net profit vs prior period).")

reg.declare_study_year("2026", ["Q1-2026", "H1-2026"])

# ============================ GLOBAL RING ====================================
gc = reg.add(Ring.GLOBAL, "commodity complex (input/output)", FindingClass.S,
    "Copper and aluminium are the dominant input: materials are 94.9% of cost of revenue "
    "(SAR 8.49bn of 8.94bn) and 79.5% of sales; the group hedges copper, aluminium and lead "
    "via commodity forwards (USD 266mn / SAR 996mn open at 31-Dec-2025). LME copper ~USD "
    "9,500-10,000/t and aluminium ~USD 2,500/t in mid-2026.",
    "LME / company Note 15 & 34 disclosures", SourceType.COMPANY_OFFICIAL, "2026-03-26",
    model_impact="Materials leg escalates on the metal-price path (its own driver), never a "
    "domestic CPI proxy — the cost-stack escalation rule; base holds metals near current, "
    "sensitised +/-15%.", fiscal_period="FY2025")
reg.add(Ring.GLOBAL, "rate cycle & USD/FX regime", FindingClass.C,
    "SAR is hard-pegged to the USD at 3.75, so SAMA tracks the Fed; the 2026 policy path "
    "(SAMA repo 4.25%, easing with the Fed) sets the SAR discount curve directly and removes "
    "any devaluation/translation leg from the valuation.",
    "SAMA / Federal Reserve", SourceType.REGULATOR_OFFICIAL, "2026-08-18",
    model_impact="rf and Kd built off the SAR curve; no FX driver, unlike an EM-currency name.")
reg.add(Ring.GLOBAL, "global sector demand", FindingClass.C,
    "Global wire-and-cable demand is driven by electrification, grid investment, renewables "
    "interconnection and data-centre build-out; the GCC is among the fastest-growing regional "
    "markets on power-infrastructure spend.",
    "Industry context (IEA/BNEF-class electrification themes)", SourceType.REPUTABLE_PRESS,
    "2026-08-18", model_impact="supports the mid-single-digit real volume-growth taper.")
reg.add(Ring.GLOBAL, "trade / sanctions / supply chains", FindingClass.C,
    "Exports are ~27% of revenue, predominantly the UAE (~SAR 2.2bn); no sanctions exposure. "
    "A disclosed MoU with the Syrian Sovereign Fund (May-2026) is early-stage optionality, not "
    "modelled.", "Company disclosures / Tadawul announcements", SourceType.COMPANY_OFFICIAL,
    "2026-05", model_impact="export leg carried at ~4.5% world-nominal terminal growth; MoU not in numbers.")

# ============================ COUNTRY RING ===================================
reg.add(Ring.COUNTRY, "sovereign macro (inflation, policy rate, FX/deval risk)", FindingClass.S,
    "Saudi Arabia: Moody's Aa3, low inflation (~2%), SAMA repo 4.25% held entering 2026, SAR "
    "peg intact. Damodaran (5-Jan-2026): adjusted default spread 0.51%, country risk premium "
    "0.78%, total ERP 5.01% (mature-market base 4.23%).",
    "Damodaran country-risk-premium file; SAMA", SourceType.REGULATOR_OFFICIAL, "2026-01-05",
    model_impact="rf* = SAR 10y 4.85% less 0.51% sovereign spread; ERP 5.01% (rating) / ~5.00% "
    "(CDS); country risk enters once via the CRP.")
reg.add(Ring.COUNTRY, "regulatory environment (regulator, caps, tariffs, tax/subsidy)", FindingClass.S,
    "Zakat (~2.5% of the zakat base) plus income tax (20%) on any non-GCC-owned / foreign-"
    "operation profit share. Audited effective charge rose FY2023 7.0% -> FY2024 7.3% -> FY2025 "
    "9.0% as the foreign profit share grew.",
    "ZATCA regime; company Note 32", SourceType.COMPANY_OFFICIAL, "2026-03-26",
    model_impact="forward blended zakat/tax rate 9.5%, just above the FY2025 print.",
    fiscal_period="FY2025")
reg.add(Ring.COUNTRY, "fiscal / political events with sector read-through", FindingClass.C,
    "Vision-2030 drives grid expansion, giga-projects (NEOM), housing and industrial build-out — "
    "the demand backdrop for domestic cable (73% of revenue). Saudi Electricity Company and NWC "
    "capex are the proximate demand channels.",
    "Government programme disclosures", SourceType.REPUTABLE_PRESS, "2026-08-18",
    model_impact="underpins the domestic volume taper and the 4% nominal terminal growth.")

# ============================ INDUSTRY RING ==================================
reg.add(Ring.INDUSTRY, "demand drivers & capacity/supply balance", FindingClass.S,
    "Saudi/GCC cable demand tracks power-grid capex, construction and renewables; Riyadh Cables "
    "is the largest Saudi producer with plants at MODON industrial cities. H1-2026 revenue +9.5% "
    "was volume-driven ('increase in the volume of quantities sold').",
    "Company H1-2026 results; sector context", SourceType.COMPANY_OFFICIAL, "2026-07-29",
    model_impact="real volume-index growth 8.5% -> 5% taper.", fiscal_period="H1-2026")
reg.add(Ring.INDUSTRY, "pricing", FindingClass.S,
    "Cable pricing is metal-cost pass-through plus a conversion spread; when metal prices rise, "
    "revenue and materials rise together so the % gross margin compresses. H1-2026 shows exactly "
    "this — gross profit flat (-0.06%) on +9.5% revenue, gross margin 15.26% vs FY2025 16.24%.",
    "Company H1-2026 results; Note 34", SourceType.COMPANY_OFFICIAL, "2026-07-29",
    model_impact="gross margin (the conversion spread) is the study's central contested "
    "judgement, anchored on H1-2026 15.26% and computed both ways.", fiscal_period="H1-2026")
reg.add(Ring.INDUSTRY, "new entrants (named-competitor level)", FindingClass.C,
    "Regional peers: Ducab (UAE), Jeddah Cable, Midal Cables (Bahrain, aluminium), and the old "
    "Saudi Cable Company; global majors Nexans and Prysmian bid on high-voltage turnkey work. "
    "High-voltage and export segments face the strongest competition.",
    "Industry knowledge / peer filings", SourceType.REPUTABLE_PRESS, "2026-08-18",
    model_impact="supports a conservative HV-segment growth path and the relative-multiple discount.")
reg.add(Ring.INDUSTRY, "technology substitution", FindingClass.C,
    "No near-term substitution risk to copper/aluminium conductor cable; aluminium-vs-copper "
    "mix shifts on relative price but both are the company's inputs. HVDC and extra-high-voltage "
    "are growth, not substitution.", "Industry knowledge", SourceType.REPUTABLE_PRESS,
    "2026-08-18", model_impact="none — context only.")
reg.add(Ring.INDUSTRY, "competitor capacity / price moves (named)", FindingClass.C,
    "Peer multiples anchor the relative lens: Nexans/Prysmian ~7-9x forward EV/EBITDA; Indian "
    "peers Polycab/KEI trade at a large growth premium (~20-30x). Riyadh Cables trades ~11-12x "
    "trailing EV/EBITDA.",
    "Peer market data", SourceType.AGGREGATOR, "2026-08-18",
    model_impact="justified EV/EBITDA 9.0x set mid-range with a single-country discount.")

# ============================ COMPANY RING ===================================
# official financial statements — FOUR audited years (target met)
reg.add(Ring.COMPANY, "official financial statements", FindingClass.D,
    "FY2025 audited consolidated statements (KPMG, unmodified, signed 26-Mar-2026): full IS, "
    "BS, CF and notes, including Note 34 cost-of-revenue breakdown, Note 40 segments/geography, "
    "Note 15 inventory, Note 24 Islamic finance.",
    "Riyadh Cables FY2025 audited FS (KPMG)", SourceType.COMPANY_OFFICIAL, "2026-03-26",
    model_impact="anchors the FY2025 base year and the ground-up cost stack.",
    is_fs_data=True, fiscal_period="FY2025")
reg.add(Ring.COMPANY, "official financial statements", FindingClass.D,
    "FY2024 audited consolidated statements: full IS/BS + 2023 comparative.",
    "Riyadh Cables FY2024 audited FS", SourceType.COMPANY_OFFICIAL, "2025-03",
    model_impact="FY2024 historical year and the FY2023 comparative.", is_fs_data=True,
    fiscal_period="FY2024")
reg.add(Ring.COMPANY, "official financial statements", FindingClass.D,
    "FY2023 audited consolidated statements: full IS/BS + 2022 comparative.",
    "Riyadh Cables FY2023 audited FS", SourceType.COMPANY_OFFICIAL, "2024-03",
    model_impact="FY2023 historical year.", is_fs_data=True, fiscal_period="FY2023")
reg.add(Ring.COMPANY, "official financial statements", FindingClass.C,
    "FY2022 audited annual report (IPO year): revenue SAR 6.85bn, net profit SAR 352mn — the "
    "growth base three years back; cross-verified against the FY2023 comparative column.",
    "Riyadh Cables FY2022 annual report", SourceType.COMPANY_OFFICIAL, "2023-03",
    model_impact="FY2022 context/growth base.", is_fs_data=True, fiscal_period="FY2022")
# regular disclosures — the 2026 interims (study-year quarters)
reg.add(Ring.COMPANY, "regular disclosures", FindingClass.B,
    "H1-2026 reviewed interim results (Tadawul-filed 29-Jul-2026): revenue SAR 5,697.6mn (+9.5%), "
    "gross profit SAR 869.8mn (FLAT), operating profit SAR 669.7mn, net profit SAR 588.8mn, "
    "equity SAR 3,471mn. The most recent reviewed actual — the near-term margin anchor.",
    "Tadawul H1-2026 announcement (anId 97051)", SourceType.COMPANY_OFFICIAL, "2026-07-29",
    model_impact="resets the FY2026 base: gross margin anchored on H1-2026 15.26%, not FY2025 "
    "16.24%.", fiscal_period="H1-2026")
reg.add(Ring.COMPANY, "regular disclosures", FindingClass.S,
    "Q1-2026 results (Tadawul-filed): revenue SAR 2,767.7mn (+11.2%), gross profit SAR 430.5mn, "
    "operating profit SAR 327.3mn, net profit SAR 282.0mn, EPS 1.88.",
    "Tadawul Q1-2026 announcement", SourceType.COMPANY_OFFICIAL, "2026-05-05",
    model_impact="corroborates the volume-led growth and margin normalisation.", fiscal_period="Q1-2026")
# IR communications — mandatory COMPANY_IR
reg.add(Ring.COMPANY, "IR communications (calls, presentations, releases)", FindingClass.C,
    "H1-2026 earnings conference call (hosted 4-Aug-2026) and results release: management "
    "attributes growth to volume ('increase in the volume of quantities sold') and favourable "
    "product-mix changes — the qualitative basis for the volume-led, margin-normalising forecast.",
    "Riyadh Cables H1-2026 earnings call / results release", SourceType.COMPANY_IR, "2026-08-04",
    model_impact="qualitative support for volume-driver split vs price/metal.")
reg.add(Ring.COMPANY, "strategic plans & guidance", FindingClass.C,
    "Capacity expansion largely completed (FY2025 assets-under-construction 108mn of 189mn "
    "capex); export push into the UAE and wider MENA; no explicit numeric revenue guidance issued.",
    "Company disclosures / IR", SourceType.COMPANY_IR, "2026-07-29",
    model_impact="capex taper to ~1.6-1.9% of revenue; no guidance to anchor, so drivers are "
    "built from the disclosed history.")
reg.add(Ring.COMPANY, "one-off base-resetting transactions", FindingClass.S,
    "FY2025 acquisition of a subsidiary with non-controlling interests (NCI rose from -0.5mn to "
    "62.7mn; goodwill/intangibles rose to 137.9mn from 57.2mn; SAR 108.9mn cash paid). No other "
    "base-resetting one-offs.", "FY2025 audited FS (Notes 10, 46)", SourceType.COMPANY_OFFICIAL,
    "2026-03-26", model_impact="NCI deducted at carrying value in the bridge; goodwill excluded "
    "from invested capital.", is_fs_data=True, fiscal_period="FY2025")
reg.add(Ring.COMPANY, "ownership / stake changes (named-transaction rule)", FindingClass.C,
    "May-2026 disclosed transfer of 9 million shares among major shareholders; the company "
    "IPO'd 30% in December 2022. Founding-family control with a substantial free float.",
    "Tadawul announcement, 20-May-2026", SourceType.COMPANY_OFFICIAL, "2026-05-20",
    model_impact="none on cash flows; noted for float/governance context.")
reg.add(Ring.COMPANY, "management & capital actions", FindingClass.C,
    "Semi-annual dividend policy: FY2025 paid SAR 3.8/share (SAR 1.9 final FY2024 + SAR 1.9 "
    "interim), 52.6% of EPS; 150mn shares, SAR 1.5bn capital, 282,500 treasury shares.",
    "FY2025 audited FS (Notes 20, 22, 41)", SourceType.COMPANY_OFFICIAL, "2026-03-26",
    model_impact="forward payout 55%; share count 149.72mn for per-share values.",
    is_fs_data=True, fiscal_period="FY2025")

# ---- per-driver gate table --------------------------------------------------
# Finding ids are assigned in add() order; F13 = FY2025 audited FS (D, COMPANY_OFFICIAL),
# F17 = H1-2026 reviewed results (B, COMPANY_OFFICIAL). Both satisfy the bottom-up gate.
reg.add_driver("Cable volume index (real growth)", DriverMode.BOTTOM_UP,
    "Grown off the disclosed segment revenue and the H1-2026 volume-led growth statement; "
    "tonnage is not disclosed so an index is used, flagged.", ["F08", "F09", "F13"])
reg.add_driver("Metal content per unit (materials leg)", DriverMode.BOTTOM_UP,
    "Note 34 discloses materials as a distinct cost line (94.9% of COGS); escalated on the LME "
    "copper/aluminium path, its own driver.", ["F01", "F13"])
reg.add_driver("Conversion cost per unit", DriverMode.BOTTOM_UP,
    "Note 34 discloses the non-metal cost stack (salaries, depreciation, repairs, utilities); "
    "escalated on Saudi domestic inflation, a separate escalator.", ["F13"])
reg.add_driver("Sustained gross margin (conversion spread)", DriverMode.BOTTOM_UP,
    "The study's central judgement, anchored on the H1-2026 reviewed gross margin (15.26%) and "
    "computed both ways against the FY2025 peak.", ["F09", "F17"])
reg.add_driver("Working-capital intensity", DriverMode.BOTTOM_UP,
    "Inventory + receivables less payables from the audited balance sheets, held at the FY2025 "
    "27.9% of revenue.", ["F13", "F21"])

errors, warnings = reg.validate()
reg.to_json(os.path.join(HERE, 'sweep_register.json'))
print(reg.qc_line())
if errors:
    print("\nERRORS:")
    for e in errors:
        print("  -", e)
if warnings:
    print("\nWARNINGS:")
    for w in warnings:
        print("  -", w)
print(f"\nprimary-access attempts: {len(reg.primary_access)}; findings: {len(reg.findings)}; "
      f"drivers: {len(reg.drivers)}")
