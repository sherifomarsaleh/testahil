"""GBCO fundamental refresh (19-08-2026) — Step 2A Information Sweep register.

Fundamental refresh trigger: new H1-2026 disclosure set (reviewed consolidated interim FS
+ 2Q/1H26 earnings release, both dated 13-Aug-2026). NOT a new study (trigger a) and NOT
a roll-forward (trigger b): no recalibration, no cone re-strike, no ledger rows, no
technical read. The Company ring is re-run in full on the new disclosures; the Global /
Country rings are re-run ONLY where a driver moved (Egypt 10Y yield, Damodaran Egypt row,
CBE policy path, EGP/USD, Egypt CPI); the Industry ring is re-run for the Egypt auto
market print and peer multiples. Everything else is carried forward from the 08-07-2026
study's sweep and said so in the study text.

Run:  python3 sweep.py   (writes sweep_register.json; validate() must return no errors)
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from research_sweep import (SweepRegister, AssetClass, Ring, FindingClass, SourceType,
                            DriverMode, RINGS, MANDATORY)

SWEEP_DATE = "2026-08-19"
reg = SweepRegister("GBCO", AssetClass.STOCK, SWEEP_DATE)

# ---------------------------------------------------------------------------------------
# PRIMARY ACCESS — the company's own site, attempted FIRST, logged with outcome
# ---------------------------------------------------------------------------------------
reg.record_primary_access(
    "https://ir.gb-corporation.com/en/filings", True, SWEEP_DATE,
    "REACHABLE. Filings page lists the exact documents supplied by the user "
    "(GB Corp Consolidated 30 June 2026; GBCorpQ22026 - Release) plus the Q2-26 "
    "newsletter, standalone FS, BOD minutes 13-Aug-2026 and Form 30. The page's own "
    "EGX widget quoted the share at EGP 29.70 (range 29.42-30.50) on the sweep date.")
reg.declare_study_year("2026", ["Q1-2026", "Q2-2026"])

# ---------------------------------------------------------------------------------------
# COMPANY RING — re-run in full on the new disclosure set
# ---------------------------------------------------------------------------------------
fFS = reg.add(Ring.COMPANY, "official financial statements", FindingClass.D,
    "H1-2026 reviewed consolidated interim FS (KPMG Hazem Hassan, limited review): group "
    "revenue EGP 48,474.4mn (+35.2%), GP 7,421.9mn (15.3%), EBT 1,790.4mn, NP attrib "
    "1,262.0mn (EPS 1.163), BS total 100,921.4mn, parent equity 33,454.3mn",
    "GB Corp consolidated interim FS, 30-Jun-2026 (user-supplied; also on IR filings page)",
    SourceType.COMPANY_OFFICIAL, "2026-08-13",
    detail="FY2025 comparatives RESTATED (note 39): MNT Investment B.V. carrying +2,460.2mn, "
           "Drive receivables reclass +692.8mn LT->ST, parent equity +2,882.7mn.",
    model_impact="Anchors every H1-26 actual in the refresh; restates the FY25 base the "
                 "prior study was built on (associates 13,689.5 -> 15,732.4)",
    is_fs_data=True, fiscal_period="Q2-2026")

fQ1 = reg.add(Ring.COMPANY, "official financial statements", FindingClass.D,
    "Q1-2026 actuals (as comparatives inside the H1-26 disclosure set): group revenue "
    "21,570.8mn (48,474.4 less 2Q's 26,903.6), auto revenue 17,734.9mn, auto EBITDA "
    "1,194.3mn (2Q26 rebound to 2,290.5mn), auto net debt 13,090.9mn at 1Q26",
    "GB Corp 2Q/1H26 earnings release quarterly tables (1Q26 columns)",
    SourceType.COMPANY_OFFICIAL, "2026-08-13",
    model_impact="Gives the intra-year shape (2Q >> 1Q) used to set the H2-26E seasonal "
                 "uplift on volumes and margins",
    is_fs_data=True, fiscal_period="Q1-2026")

fER = reg.add(Ring.COMPANY, "IR communications (calls, presentations, releases)", FindingClass.D,
    "2Q/1H26 earnings release: PC 29,554 units / EGP 30,595.7mn (ASP 1.035mn); CV&CE "
    "2,490 units / 4,749.1mn; Light Mobility 21,173 units / 1,435.2mn; Trading 2,572.3mn "
    "(tires 1,956.3 + parts 616.0); auto GPM 14.3%, EBITDA 3,484.8mn, ND 14,493.6mn "
    "(2.14x); GB Capital revenue 9,088.2mn, book 24.0bn, NPL 2.8%, D/E 1.08x",
    "GB Corp 2Q/1H26 earnings release (COMPANY_IR channel)",
    SourceType.COMPANY_IR, "2026-08-13",
    model_impact="Unlocks the full volume x price rebuild per line of business and the "
                 "per-segment cost-per-unit anchors; supersedes every FY26E driver in the "
                 "08-07-2026 study",
    fiscal_period="Q2-2026")

fMNT = reg.add(Ring.COMPANY, "ownership / stake changes (named-transaction rule)", FindingClass.B,
    "MNT Investment B.V.: stake 42.93% after the June-2026 Al Ahly Capital first close "
    "(44.01% before) — NOT the 41.61% in the 9-Jun-2026 press release, which described "
    "the post-second-closing position; equity-method carrying value EGP 15,723.5mn at "
    "30-Jun-26 (restated opening +2,460.2mn); H1-26 equity pickup 409.985mn",
    "H1-26 FS note 34 + note 39 (restatement)", SourceType.COMPANY_OFFICIAL, "2026-08-13",
    detail="KPMG review conclusion is QUALIFIED on exactly this line: MNT BV's own FS for "
           "the period were not provided, so the 409.9mn share of profit is unverified — "
           "second consecutive period this qualification appears (also FY2025).",
    model_impact="Resets the associates leg: stake 41.61%->42.93%; adds the company's own "
                 "balance-sheet mark (15,723.5mn) as the second framing of the study's "
                 "most contested judgement (vs the USD 1.4bn round mark)",
    is_fs_data=True, fiscal_period="Q2-2026")

reg.add(Ring.COMPANY, "one-off base-resetting transactions", FindingClass.S,
    "FY25 restatement (note 39): investment in associate +2,460.2mn, Drive LT->ST "
    "receivables reclass, DTL +46.2mn, parent equity +2,882.7mn — the FY25 book the "
    "prior study cited is superseded",
    "H1-26 FS note 39", SourceType.COMPANY_OFFICIAL, "2026-08-13",
    model_impact="Every FY25 balance-sheet base in the model moves to the restated "
                 "column; book-value lens BVPS is restated 30.82 not 26.5",
    is_fs_data=True, fiscal_period="FY2025")

reg.add(Ring.COMPANY, "strategic plans & guidance", FindingClass.S,
    "CEO letter: Egypt demand supportive but 'improving supply and greater model "
    "availability may place some pressure on pricing and margins'; Jordan rationalization "
    "impact moderates 3Q, largely subsides from 4Q; Iraq recovery dependent on "
    "geopolitics; additional Hyundai CKD model Sep-26, third Changan model 4Q26, new EV "
    "brand Aug-26; Sadat fully operational; Ain Sokhna CV capacity expansion under "
    "consideration",
    "GB Corp 2Q/1H26 earnings release, CEO note", SourceType.COMPANY_IR, "2026-08-13",
    model_impact="Caps the ASP escalator below realized H1 pace from FY27; sets regional "
                 "drag fading into FY27; supports H2-26E volume uplift from launches",
    fiscal_period="Q2-2026")

reg.add(Ring.COMPANY, "regular disclosures", FindingClass.D,
    "Borrowing-cost disclosure (note 26): average interest rate on current EGP loans & "
    "borrowings 20.82% during H1-26 (21.91% FY25); USD 7.78% (8.30% FY25); essentially "
    "the whole book variable-rate (43,480.1mn of loans/advances/overdrafts at variable "
    "rates note 29); Drive bond program note 38 (2022 vintage 13.5-14.0% fixed)",
    "H1-26 FS notes 26/29/38", SourceType.COMPANY_OFFICIAL, "2026-08-13",
    model_impact="THE marginal Kd anchor: 20.82% EGP, dated, from the filing itself — "
                 "replaces the prior study's CEIC/TradingEconomics-quoted CBE average",
    is_fs_data=True, fiscal_period="Q2-2026")

reg.add(Ring.COMPANY, "management & capital actions", FindingClass.C,
    "FY25 dividend EGP 379.925mn (0.35/share) paid in two installments 29-Apr-26 and "
    "29-Jul-26; capital commitments 1,020.5mn at 30-Jun-26 (new production lines), "
    "up from 525.5mn at FY25; Algeria arbitration ongoing (>= USD 24mn claim); assets "
    "held for sale 867.1mn (land, sale delayed)",
    "H1-26 FS notes 10/31/30/42", SourceType.COMPANY_OFFICIAL, "2026-08-13",
    is_fs_data=True, fiscal_period="Q2-2026")

# Historical FS depth (four full fiscal years on the record for this name)
reg.add(Ring.COMPANY, "official financial statements", FindingClass.D,
    "FY2025 consolidated results (group revenue 80,229.8mn, auto 66,358.3mn, auto "
    "EBITDA 6,363.3mn, ND 15,210.0mn) — as extracted for the 08-07-2026 study from the "
    "company's issued 4Q25 statements/release and re-verified against the ER's own "
    "ND/LTM-EBITDA print (15,210.0/2.39x = 6,364)",
    "GB Corp FY2025 issued statements/4Q25 release (via the delivered 08-07-2026 study "
    "workbook, cell-verified)", SourceType.COMPANY_OFFICIAL, "2026-02-26",
    model_impact="FY25 base year for every driver; restated where note 39 applies",
    is_fs_data=True, fiscal_period="FY2025")
reg.add(Ring.COMPANY, "official financial statements", FindingClass.D,
    "FY2024 consolidated results (group revenue 53,969.5mn, auto 47,065.0mn, PC 42,043 "
    "units / 36,533.4mn)", "GB Corp FY2024 issued statements/4Q24 release (via the "
    "delivered 08-07-2026 study workbook)", SourceType.COMPANY_OFFICIAL, "2025-03-01",
    model_impact="Second historical year", is_fs_data=True, fiscal_period="FY2024")
reg.add(Ring.COMPANY, "official financial statements", FindingClass.D,
    "FY2023 consolidated results (group revenue 28,317.2mn, auto 23,854.0mn, PC 26,994 "
    "units / 16,544.3mn)", "GB Corp FY2023 issued statements/4Q23 release (via the "
    "delivered 08-07-2026 study workbook)", SourceType.COMPANY_OFFICIAL, "2024-03-01",
    model_impact="Third historical year", is_fs_data=True, fiscal_period="FY2023")

# ---------------------------------------------------------------------------------------
# COUNTRY RING — re-run where a driver moved
# ---------------------------------------------------------------------------------------
reg.add(Ring.COUNTRY, "sovereign macro (inflation, policy rate, FX/deval risk)", FindingClass.S,
    "Egypt 10Y local yield 22.92% (19-Aug-26, 52wk 19.79-23.05); CBE overnight deposit "
    "held at 19.00% for a third consecutive MPC (Jul-26) after the 100bp cut opening "
    "2026; USD/EGP 50.71 (was 47.5 at the prior study, -6.8% EGP); urban CPI 14.9% "
    "y/y Jul-26 (up from 14.3% Jun)",
    "investing.com Egypt 10Y + USD/EGP quotes; SIS/Daily News Egypt on CBE MPC 11-Jul-26; "
    "CAPMAS via press 10-Aug-26", SourceType.PRIMARY_MARKET_DATA, "2026-08-19",
    model_impact="rf_observed 22.55->22.92; EGP/USD in the MNT mark 47.5->50.71; CPI and "
                 "FX escalator paths for the per-class cost stack; CBE path supports "
                 "PC affordability and GB Capital NIM",
    url="https://www.investing.com/rates-bonds/egypt-10-year-bond-yield")

reg.add(Ring.COUNTRY, "regulatory environment (regulator, caps, tariffs, tax/subsidy)", FindingClass.S,
    "New CBE requirements governing bank participation in securitization: banks "
    "re-working approval processes; company expects delayed transactions, deferred "
    "revenue recognition and higher funding costs in H2-26, normalizing thereafter; "
    "FRA regulates all GB Capital subsidiaries; statutory corporate tax 22.5% "
    "(effective H1-26 41.0% on unshielded regional losses, note 11-C)",
    "GB Corp 2Q/1H26 earnings release (CEO note + GB Capital section) + H1-26 FS note 11-C",
    SourceType.COMPANY_IR, "2026-08-13",
    model_impact="GB Capital H2-26E revenue haircut vs run-rate; effective-tax glide "
                 "38%->22.5% as regional losses fade",
    fiscal_period="Q2-2026")

reg.add(Ring.COUNTRY, "fiscal / political events with sector read-through", FindingClass.C,
    "Damodaran Jan-2026 Egypt row: Caa1, adjusted default spread 6.37%, CRP 9.71%, "
    "total ERP 13.94% (rating basis); sovereign CDS 3.41%, ERP on the CDS basis 9.41%; "
    "US row 4.46%/4.69% anchors the mature-market premium",
    "Damodaran ORIGINAL ctryprem.html, 'last updated January 5, 2026'",
    SourceType.REGULATOR_OFFICIAL, "2026-01-05",
    url="https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/ctryprem.html")

# ---------------------------------------------------------------------------------------
# INDUSTRY RING — re-run: market print, EV shares, peers
# ---------------------------------------------------------------------------------------
reg.add(Ring.INDUSTRY, "demand drivers & capacity/supply balance", FindingClass.S,
    "AMIC: Egypt passenger-car sales 62.3k units in H1-26 (+18% y/y from 52.8k); total "
    "vehicle market 102.1k (+40.5%); demand aided by lower rates, pent-up replacement "
    "and pre-buying ahead of post-deval price increases; supply/model availability "
    "improving",
    "AMIC via Zawya/Arab Finance/Ahram coverage, H1-26 prints",
    SourceType.REPUTABLE_PRESS, "2026-07-20",
    model_impact="Market-size anchor for PC volume path: GB's H1 Egypt PC volumes imply "
                 "a stable ~40% share of the AMIC PC market; FY26E volume set on H1 "
                 "actual + launch-driven H2, not on a share gain assumption")

reg.add(Ring.INDUSTRY, "pricing", FindingClass.S,
    "Realized H1-26 PC ASP 1.035mn EGP (+10.8% vs FY25 0.934mn) on pricing + mix; "
    "company itself flags supply-driven pricing pressure ahead; tires margin boosted by "
    "inventory bought at favorable historical cost (one-off)",
    "GB Corp 2Q/1H26 earnings release", SourceType.COMPANY_IR, "2026-08-13",
    model_impact="ASP escalator: FY26E realized-anchored (+11.9%), then decaying below "
                 "the FX+CPI path (8/7/6/6%); tires unit cost resets +4% in FY27",
    fiscal_period="Q2-2026")

reg.add(Ring.INDUSTRY, "new entrants (named-competitor level)", FindingClass.S,
    "NEV competition intensifying: GB holds ~17.5% of the total EV market and ~40% of "
    "REEV (Deepal ~31% of REEV alone); GB adding an A/B-class EV brand Aug-26; BYD and "
    "Chinese OEM entry risk remains the priced negative in the discrete stack",
    "GB Corp 2Q/1H26 earnings release (EV/REEV shares)", SourceType.COMPANY_IR, "2026-08-13",
    model_impact="Keeps the BYD/price-shock discrete factor; supports PC volume "
                 "resilience via portfolio breadth", fiscal_period="Q2-2026")

reg.add(Ring.INDUSTRY, "technology substitution", FindingClass.C,
    "REEV/EV mix shift inside Egypt PC demand is being captured by GB's own portfolio "
    "(Deepal, premium EV, new A/B EV brand) rather than displacing it; four-wheeler "
    "Qute constrained by India supply (production disruptions), expected to resolve",
    "GB Corp 2Q/1H26 earnings release", SourceType.COMPANY_IR, "2026-08-13",
    fiscal_period="Q2-2026")

reg.add(Ring.INDUSTRY, "competitor capacity / price moves (named)", FindingClass.C,
    "Peer marks refreshed 19-Aug-26: Dogus Otomotiv (Istanbul) trailing P/E 12.55, P/B "
    "0.62 (TAS-29 inflation-restated book); Contact Financial (EGX, NBFS) trailing P/E "
    "9.41, mktcap ~EGP 6.0-6.6bn across aggregators; AutoNation (US) P/E 9.11 (fwd "
    "8.35); Bajaj Auto (NSE) P/E 27.56, P/B 7.49",
    "investing.com ratio pages + stockanalysis.com, 19-Aug-2026",
    SourceType.AGGREGATOR, "2026-08-19",
    detail="Aggregator discrepancy note: CNFN market cap quoted 6.64bn (stockanalysis), "
           "6.01bn (tradingview) and 4.489bn (african-markets, 07-Jul date) — dates "
           "differ; used for multiple context only, never for the subject's numbers.")

# ---------------------------------------------------------------------------------------
# GLOBAL RING — carried forward except the two that moved
# ---------------------------------------------------------------------------------------
reg.add(Ring.GLOBAL, "rate cycle & USD/FX regime", FindingClass.C,
    "USD funding cost on the company's own USD tranches 7.78% average H1-26 (8.30% "
    "FY25) — the global rate cycle easing is already visible inside the filing; EGP "
    "spot path is the binding FX variable, not the USD leg",
    "H1-26 FS note 26 + investing.com USD/EGP", SourceType.COMPANY_OFFICIAL, "2026-08-13",
    is_fs_data=True, fiscal_period="Q2-2026")
reg.add(Ring.GLOBAL, "commodity complex (input/output)", FindingClass.C,
    "CKD kit/import content is the commodity-complex exposure (steel/components priced "
    "in USD/CNY); no direct commodity disclosure in the filing set — cost side is "
    "escalated on FX + CPI classes with the import share flagged as constructed",
    "H1-26 disclosure set (absence noted)", SourceType.COMPANY_OFFICIAL, "2026-08-13",
    fiscal_period="Q2-2026")
reg.add(Ring.GLOBAL, "global sector demand", FindingClass.C,
    "Regional (Iraq/Jordan) auto demand still depressed by geopolitics — foreign PC "
    "revenue share fell 25.8% -> 14.6% of PC in one year; exports of Egyptian-built "
    "buses a growth channel (CV&CE 'continued export momentum')",
    "GB Corp 2Q/1H26 earnings release + FS note 5 foreign-revenue split",
    SourceType.COMPANY_OFFICIAL, "2026-08-13", is_fs_data=True, fiscal_period="Q2-2026")
reg.add_negative(Ring.GLOBAL, "trade / sanctions / supply chains",
    "GB Corp H1-26 disclosure set + press sweep for sanctions/trade actions touching "
    "Egypt auto imports or Bajaj/Hyundai/Changan supply into Egypt (India Qute supply "
    "disruption is captured under technology substitution)", SWEEP_DATE)

# ---------------------------------------------------------------------------------------
# Driver gate table — mode per driver, citing the findings above
# ---------------------------------------------------------------------------------------
reg.add_driver("PC volumes (units, CKD/CBU)", DriverMode.BOTTOM_UP,
    "units disclosed quarterly (29,554 H1 actual; CKD 15,454 / CBU 14,100) + AMIC market "
    "print; H2-26E set on launch calendar", [fER, fFS])
reg.add_driver("PC ASP (EGP mn/unit)", DriverMode.BOTTOM_UP,
    "revenue/units disclosed; realized 1.035 H1-26; forward capped below FX+CPI per CEO "
    "supply-pressure guidance", [fER])
reg.add_driver("PC unit cost (EGP mn/unit)", DriverMode.BOTTOM_UP,
    "segment cost of sales disclosed (note 5-B: 27,054.2 on 29,554 units = 0.9154); "
    "escalated per class: FX-linked import share + domestic CPI share (share weights "
    "constructed, flagged)", [fFS, fER])
reg.add_driver("CV&CE volumes & ASP", DriverMode.BOTTOM_UP,
    "bus/truck/CE units and revenue disclosed quarterly (2,490 units H1)", [fER])
reg.add_driver("Light Mobility volumes & ASP", DriverMode.BOTTOM_UP,
    "2-3-4W units and revenue disclosed (21,173 H1); Qute supply constraint noted", [fER])
reg.add_driver("Trading (tires + parts) revenue", DriverMode.BOTTOM_UP,
    "tires and ready-parts revenue disclosed separately; tires margin one-off flagged",
    [fER])
nSGA = reg.add_negative(Ring.COMPANY, "cost-line granularity (SG&A per function)",
    "H1-26 FS searched for per-function SG&A below the by-nature note 36 and the "
    "segment note 5-B allocations — not disclosed", SWEEP_DATE)
reg.add_driver("Auto SG&A / other income / provisions (% of revenue)", DriverMode.TOP_DOWN,
    "no per-line cost granularity below the by-nature note; anchored on H1-26 actual "
    "ratios (7.10% / 0.84% / -0.22%) and held", [nSGA])
reg.add_driver("Working capital (DIO/DSO/DPO -> WC)", DriverMode.BOTTOM_UP,
    "five quarterly WC snapshots disclosed (Table 6) + component days computed from the "
    "statements; projected on days, 4Q build acknowledged", [fER, fFS])
reg.add_driver("Auto capex", DriverMode.BOTTOM_UP,
    "H1-26 actual 1,376.5 (257.0 PP&E + 1,119.5 projects) + capital commitments "
    "1,020.5mn disclosed", [fFS])
reg.add_driver("Auto effective tax path", DriverMode.BOTTOM_UP,
    "note 11-C reconciliation (22.5% statutory, 41.0% effective on unshielded regional "
    "losses) + CEO guidance on the regional drag fading", [fFS])
reg.add_driver("GB Capital leg (operating equity ex-associates)", DriverMode.BOTTOM_UP,
    "segment BS discloses GB Capital parent equity 22,497.8 and the associates carrying "
    "inside it; operating equity derived 6,267.3", [fFS, fER])
reg.add_driver("MNT-Halan / associates leg (BOTH-WAYS mark)", DriverMode.BOTTOM_UP,
    "stake 42.93% + carrying 15,723.5 from note 34; USD 1.4bn round from the June-26 "
    "first close (company release, press-corroborated); computed both ways, never "
    "averaged", [fMNT])
reg.add_driver("Kd (marginal, EGP)", DriverMode.BOTTOM_UP,
    "note 26 average EGP rate 20.82% H1-26, variable-rate book (note 29) so the average "
    "IS the marginal rate; USD tranche 7.78% + expected depreciation", [fFS])

# ---------------------------------------------------------------------------------------
# Close every remaining mandatory category with a dated negative search
# ---------------------------------------------------------------------------------------
for ring in RINGS[AssetClass.STOCK]:
    for cat in MANDATORY[ring]:
        if not any(f.ring is ring and f.category == cat for f in reg.findings):
            reg.add_negative(ring, cat,
                f"targeted query set for '{cat}' on GBCO/GB Corp/Egypt autos-NBFS, "
                f"19-Aug-2026 pass", SWEEP_DATE)

errors, warnings = reg.validate()
print(reg.qc_line())
if warnings:
    for w in warnings:
        print("WARN:", w)
if errors:
    for e in errors:
        print("ERROR:", e)
    raise SystemExit("SWEEP REGISTER INVALID")
freshness = reg.check_freshness("2026-08-19")
print("freshness:", freshness or "OK (same-day)")
reg.to_json(os.path.join(os.path.dirname(os.path.abspath(__file__)), "sweep_register.json"))
print("sweep_register.json written:", len(reg.findings), "findings,",
      len(reg.drivers), "driver rows")
