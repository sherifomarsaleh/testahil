"""MODON — four-ring Information Sweep register.

Runs BEFORE any forecast driver is set. Every mandatory category of every ring is
closed by a dated finding or a dated negative search.

Primary-source note: the company's own IR library (modon.com/investor-relations,
reached after modon.ae 301-redirects there) served every audited annual filing
FY2021-FY2025 plus the H1-2026 reviewed interim directly — no aggregator sits in
the build path for any of the subject's own reported numbers. The FY2024 and
FY2022 standalone PDFs carry no text layer (scanned signatures); their figures
are taken from the audited comparatives inside the FY2025 and FY2023 filings
respectively, plus OCR of the three image-only balance-sheet pages, each
cross-checked against the successor filing's comparative column."""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from research_sweep import (SweepRegister, AssetClass, Ring, FindingClass,
                            SourceType, DriverMode)

SWEEP_DATE = "2026-08-09"
R = SweepRegister("MODON", AssetClass.STOCK, SWEEP_DATE)
CO, IR, REG, PMD, PRESS, AGG = (SourceType.COMPANY_OFFICIAL, SourceType.COMPANY_IR,
                                SourceType.REGULATOR_OFFICIAL, SourceType.PRIMARY_MARKET_DATA,
                                SourceType.REPUTABLE_PRESS, SourceType.AGGREGATOR)

# ---------------------------------------------------------------- RING 1 GLOBAL
f_rate = R.add(Ring.GLOBAL, "rate cycle & USD/FX regime", FindingClass.S,
    "AED is hard-pegged to the USD; CBUAE Base Rate 3.65%, held since 17-Jun-2026, "
    "tracks the Fed. The July-2026 AED sovereign auction printed just 4bp over "
    "comparable US Treasuries",
    "CBUAE Base Rate (house FED_SCHEDULE, engine/market_profiles.py); UAE MoF/CBUAE "
    "July-2026 T-Bond auction (WAM)", REG, "2026-07-30",
    model_impact="Anchors the AED discounting basis: the risk-free build starts from the "
                 "AED government curve, and the cost-of-debt path prices off EIBOR, which "
                 "follows the Fed through the peg.")

f_costs = R.add(Ring.GLOBAL, "commodity complex (input/output)", FindingClass.S,
    "UAE tender price inflation ~3.3% in 2025, forecast ~2.7-4.5% for 2026 "
    "(Turner & Townsend UAEMI 2025), with a post-conflict hawkish tail (one QS house "
    "sees 6-9%) as fuel/freight/insurance feed through; materials ~60% of baseline cost",
    "Turner & Townsend UAE Market Intelligence 2025; MEED/Currie & Brown 2026 forecasts",
    PRESS, "2026-07-01",
    model_impact="Sets the construction-cost escalator (~4%/yr) for the development "
                 "cost-per-unit stack — its own driver class, separate from the wage/CPI "
                 "escalator on operating costs, per the one-escalator-per-driver-class rule.")

f_gdem = R.add(Ring.GLOBAL, "global sector demand", FindingClass.S,
    "Cross-border capital is the marginal buyer of Abu Dhabi residential: foreign buyers "
    "drove 62% of the y/y growth in residential sales value in 2025, and Modon booked "
    "AED 6.6bn of international sales (Egypt+Spain+JV) across 2,115 units in 2025",
    "ADREC Abu Dhabi Real Estate Market Report 2025; Modon Annual Report 2025",
    REG, "2026-01-31",
    model_impact="Supports the development sales driver's replenishment leg: demand into "
                 "Abu Dhabi is externally sourced, not a closed local pool.")

R.add_negative(Ring.GLOBAL, "trade / sanctions / supply chains",
    "UAE sanctions exposure real estate; Modon supply chain disruption; "
    "construction materials import restrictions UAE 2026", SWEEP_DATE)

# ---------------------------------------------------------------- RING 2 COUNTRY
f_sov = R.add(Ring.COUNTRY, "sovereign macro (inflation, policy rate, FX/deval risk)",
    FindingClass.S,
    "UAE rated Aa2 (Damodaran Jan-2026: adjusted default spread 0.42%, CRP 0.64%, "
    "total ERP 4.87%); AED T-Bond maturing Jan-2031 auctioned at 4.48% YTM in "
    "July-2026; EIBOR 3M 3.66% / 6M 3.71% (31-Mar-2026); AED peg unquestioned",
    "Damodaran ctryprem (Jan-2026); UAE MoF July-2026 auction via WAM; CBUAE EIBOR "
    "fixings", REG, "2026-07-30",
    model_impact="rf* = 4.48% - 0.42% = 4.06% (sovereign spread stripped once, per the "
                 "no-double-count rule); Ke and both WACC bases build from this row.")

f_tax = R.add(Ring.COUNTRY, "regulatory environment (regulator, caps, tariffs, tax/subsidy)",
    FindingClass.S,
    "UAE corporate tax 9% from 2023; Domestic Minimum Top-up Tax (15%) effective 2025 "
    "for large groups — Modon's FY2025 charge includes AED 350.4mn of DMTT, and its "
    "disclosed effective-rate range is 9%-23.5% across jurisdictions",
    "Income tax note 11, audited FY2025 consolidated financial statements", CO,
    "2026-02-18", is_fs_data=True, fiscal_period="FY2025",
    model_impact="Forecast tax modelled at the 15% DMTT floor on UAE profits with the "
                 "observed blended uplift for UK/Spain profits — not the 9% headline.")

f_gov = R.add(Ring.COUNTRY, "fiscal / political events with sector read-through",
    FindingClass.S,
    "Abu Dhabi government consolidation: on 30-Oct-2025 IHC and ADQ sold their entire "
    "stakes to L'imad Holding Company PJSC, wholly owned by the Abu Dhabi Government — "
    "Modon is now a majority government-owned entity under IAS 24, embedded in the "
    "emirate's development agenda",
    "Note 1 / note 30, audited FY2025 consolidated financial statements", CO,
    "2026-02-18", fiscal_period="FY2025",
    model_impact="Underpins bank access and the tight new-money debt margins (6M "
                 "EIBOR+0.60% on the largest 2025 tranche); also caps the free float, "
                 "which the liquidity caveat carries.")

R.add_negative(Ring.COUNTRY, "local equity index history (beta regressor)",
    "FTSE ADX General Index daily history: stooq (^adx), Yahoo FADGI.FGI / FADX15.FGI "
    "(1 point only), investing.com SSR table (~1 month) and api.investing.com (403), "
    "TradingEconomics chart API (proxy 502), WSJ/MarketWatch michelangelo (unknown "
    "instrument), apigateway.adx.ae + www.adx.ae (Cloudflare challenge)", SWEEP_DATE)

# ---------------------------------------------------------------- RING 3 INDUSTRY
f_mkt = R.add(Ring.INDUSTRY, "demand drivers & capacity/supply balance", FindingClass.S,
    "Abu Dhabi 2025: AED 142bn total real-estate transactions (+44% y/y) on 42,814 "
    "deals (+52%); residential sales AED 76bn (+67%); off-plan 71% of residential "
    "transactions; 56 new projects launched",
    "ADREC (Abu Dhabi Real Estate Centre) 2025 market report", REG, "2026-01-31",
    model_impact="Sizes the development sales replenishment driver: Modon's AED 29.8bn "
                 "of 2025 Abu Dhabi sales is ~39% of the emirate's residential sales "
                 "value — the forecast keeps share roughly flat rather than growing it.")

f_price = R.add(Ring.INDUSTRY, "pricing", FindingClass.S,
    "Residential price momentum is buyer-led and cash-led: 87% of residential sales "
    "value registered as cash in 2025, with foreign buyers driving 62% of growth; "
    "Modon's blended realised price was AED 7.02mn/unit in Abu Dhabi (29.8bn/4,243 "
    "units) vs AED 3.12mn/unit internationally (6.6bn/2,115 units)",
    "ADREC 2025 report; Modon Annual Report 2025 sales disclosures", REG, "2026-01-31",
    model_impact="The volume x price development build prices new launches off the "
                 "realised 2025 per-unit values with tender-price-linked escalation, "
                 "not off aspiration.")

f_comp = R.add(Ring.INDUSTRY, "new entrants (named-competitor level)", FindingClass.C,
    "Abu Dhabi development remains a near-duopoly of Aldar and Modon at masterplan "
    "scale, with Bloom Holding, Reportage and Q Properties-era mid-tier players below; "
    "Dubai majors (Emaar, Emaar Development) compete for the same international buyer "
    "but not on Abu Dhabi land",
    "ADREC 2025 report; company disclosures", REG, "2026-01-31")

R.add_negative(Ring.INDUSTRY, "technology substitution",
    "modular construction disruption UAE developer margins; proptech substitution of "
    "exhibition venues (virtual events share post-2024)", SWEEP_DATE)

f_peer = R.add(Ring.INDUSTRY, "competitor capacity / price moves (named)", FindingClass.S,
    "Aldar FY2025: revenue AED 33.8bn (+47%), net profit 8.8bn (+36%), EBITDA 11.2bn, "
    "group sales 40.6bn, backlog AED 66.5bn Aldar-led (167bn incl. government projects). "
    "Emaar FY2025: property sales 80.4bn (+16%), revenue 49.6bn (+40%), backlog 155bn. "
    "Emaar Development: UAE sales 71.1bn, backlog 134.3bn",
    "Aldar Q4-FY25 earnings release (aldar.com); Emaar FY2025 press release (emaar.com)",
    CO, "2026-02-09",
    model_impact="Anchors the relative-multiples lens (peer P/E, EV/EBITDA, P/B) and "
                 "cross-checks Modon's backlog-conversion pace against peers reporting "
                 "the same cycle.")

# ---------------------------------------------------------------- RING 4 COMPANY
f_plan = R.add(Ring.COMPANY, "strategic plans & guidance", FindingClass.S,
    "Masterplan pipeline: Hudayriyat Island >50mn sqm gross land, 40,000 planned "
    "units; Ras El Hekma (Egypt) 170.8mn sqm with Modon lead developer on the 56mn "
    "sqm phase 1, 500,000+ planned units, first precinct (Wadi Yemm) launched at "
    "AED 5.8bn across 2,109 units; La Zagaleta (Spain) land sales continuing",
    "Modon Annual Report 2025 (masterplan disclosures)", IR, "2026-03-31",
    model_impact="Volume ceiling for the development driver: launches are supply-"
                 "constrained by the company's own phasing, so the sales path is built "
                 "from launch cadence x realised per-unit price, not a market-growth "
                 "extrapolation.")

f_h1 = R.add(Ring.COMPANY, "regular disclosures", FindingClass.S,
    "H1-2026 reviewed interims: revenue AED 9,188mn (+40% y/y), gross profit 3,201mn, "
    "PBT 2,601mn, profit 2,202mn; development backlog converting on schedule; loans "
    "and borrowings 8,542mn (+66% since Dec-2025) as construction accelerates",
    "Interim condensed consolidated financial statements, 30-Jun-2026 (reviewed)", CO,
    "2026-08-07", is_fs_data=True, fiscal_period="H1-2026",
    model_impact="FY2026E is anchored on H1 actuals plus H2 seasonality (ADNEC events "
                 "season is H2-weighted), not a bare run-rate doubling.")

f_ir = R.add(Ring.COMPANY, "IR communications (calls, presentations, releases)",
    FindingClass.S,
    "FY2025 results release: revenue backlog AED 46.0bn (93% development sales), "
    "adjusted EBITDA 4.9bn (35.2% margin), net cash 1.8bn on the company's own "
    "definition (available cash incl. qualifying escrow, less total debt incl. the "
    "related-party loan); real-estate sales 36.3bn across 6,358 units; hospitality "
    "7,137 keys at 71% occupancy; AIM occupancy 97%; 896 events, 6.3mn visitors",
    "Modon FY2025 results announcement, modon.com media centre, 18-Feb-2026", IR,
    "2026-02-18",
    model_impact="Backlog is the development revenue driver's near-term anchor; the "
                 "adjusted-EBITDA bridge is the margin cross-check; the net-cash "
                 "definition is dual-framed against the strict statement basis.")

f_merge = R.add(Ring.COMPANY, "one-off base-resetting transactions", FindingClass.B,
    "FY2024 is a perimeter break: the Modon Properties/ADNEC combination entered via "
    "share issues of AED 27.4bn and a bargain-purchase gain of AED 9,192mn; FY2024 "
    "reported profit 9,389mn falls to ~0.2bn excluding the one-off (company's own "
    "framing). FY2023 and earlier are the Q Holding perimeter",
    "Note 4 business combinations, audited FY2025/FY2024 statements; FY2025 results "
    "release", CO, "2026-02-18", is_fs_data=True, fiscal_period="FY2024",
    model_impact="Dual-framing: every earnings-power number is stated both as reported "
                 "and ex-bargain; the forecast base is FY2025, the first clean full year "
                 "of the combined group.")

f_own = R.add(Ring.COMPANY, "ownership / stake changes (named-transaction rule)",
    FindingClass.B,
    "Named transaction: on 30-Oct-2025 IHC and ADQ disposed of their entire "
    "shareholding to L'imad Holding Company PJSC (wholly owned by the Abu Dhabi "
    "Government); the FY2025 results release states an 84.75% L'imad stake",
    "Note 1, audited FY2025 consolidated financial statements; FY2025 results release",
    CO, "2026-02-18", fiscal_period="FY2025",
    model_impact="Free float ~15%: the relative-multiples lens carries a liquidity "
                 "caveat, and government-related-entity status underpins the marginal "
                 "cost-of-debt evidence.")

f_mgmt = R.add(Ring.COMPANY, "management & capital actions", FindingClass.C,
    "No dividend paid to owners in FY2024 or FY2025 (statements of changes in equity "
    "show only an AED 243mn NCI dividend in 2025) and none proposed with FY2025 "
    "results; no buyback; Group CFO signature changed between the FY2025 filing "
    "(Bill O'Regan) and the H1-2026 interim (Matt Matharu)",
    "Audited FY2025 statements; H1-2026 interim; FY2025 results release", CO,
    "2026-08-07", fiscal_period="H1-2026")

f_fs = R.add(Ring.COMPANY, "official financial statements", FindingClass.C,
    "Four audited fiscal years assembled from the company's own filings: FY2025 "
    "(Modon, audited, signed 18-Feb-2026), FY2024 (comparatives in the FY2025 filing "
    "+ the scanned FY2024 original), FY2023 and FY2022 (Q Holding filings). H1-2026 "
    "reviewed interim on top. All retrieved directly from modon.com/investor-relations",
    "Audited consolidated financial statements FY2022-FY2025; H1-2026 interim", CO,
    "2026-02-18", is_fs_data=True, fiscal_period="FY2025")

R.add(Ring.COMPANY, "official financial statements", FindingClass.C,
    "FY2023 audited consolidated financial statements (Q Holding PSC perimeter): "
    "revenue AED 994mn, profit 574mn, total assets 21.3bn",
    "Audited FY2023 consolidated financial statements (Q Holding PSC)", CO,
    "2024-02-15", is_fs_data=True, fiscal_period="FY2023")

R.add(Ring.COMPANY, "official financial statements", FindingClass.C,
    "FY2022 audited figures via the FY2023 filing's comparative column: revenue "
    "AED 720mn, profit 823mn, total assets 19.5bn",
    "Audited FY2023 consolidated financial statements, FY2022 comparatives", CO,
    "2024-02-15", is_fs_data=True, fiscal_period="FY2022")

f_h1r = R.add(Ring.COMPANY, "IR communications (calls, presentations, releases)",
    FindingClass.B,
    "H1-2026 results release (29-Jul-2026): revenue backlog AED 65.4bn (doubling y/y, "
    "+42% vs FY2025), 95% development; H1 real-estate sales AED 26bn incl. 23bn Abu "
    "Dhabi (Hudayriyat Golf Estates AED 13bn within days); net debt AED 912mn on the "
    "company definition with AED 8.6bn unrestricted cash; adjusted EBITDA AED 3.0bn "
    "(32.6%); hospitality 3,613 keys across 16 owned/operated/JV hotels. [ADDED at "
    "revision 2: the first edition swept the interim STATEMENTS but not this release, "
    "and struck its development drivers on 31-Dec-2025 disclosures — the largest "
    "finding of the external audits, accepted and implemented]",
    "Modon H1-2026 results announcement, modon.com media centre, 29-Jul-2026", IR,
    "2026-07-29", fiscal_period="H1-2026",
    model_impact="Restrikes the valuation date to 30-Jun-2026: backlog roll opens at "
                 "62.1bn, FY2026 sales true to the realised 26bn + an H2 assumption, "
                 "the bridge uses the 30-Jun balance sheet and available cash, and "
                 "the run-off scenario is demoted to a stress reading.")

f_beta = R.add(Ring.INDUSTRY, "beta evidence (regression + industry cross-check)",
    FindingClass.S,
    "Own-stock weekly regression vs an equal-weight proxy of the 18 ADX/DFM names in "
    "the house library: beta 1.025 (3y, SE 0.109, R2 0.367, n 155, gate PASS); 1.071 "
    "(5y); 1.055 (2y). Damodaran EM industry route rejected as primary (RE Development "
    "unlevered 0.45 dominated by highly-levered Chinese developers, D/E 1.97); "
    "retained as a lower-bound cross-check (relevered 0.56-0.59)",
    "House regression on the price library; Damodaran betaemerg.xls (07-Jan-2026)",
    PMD, "2026-08-09",
    model_impact="Beta upgrades from the tier-3 assumption 1.0 to 1.03 (proxy-index "
                 "regression, flagged: proxy is not the official benchmark); "
                 "sensitised 0.8-1.2.")

# ---- primary access log (successes AND failures, per the standing rule) -------
R.record_primary_access("https://www.modon.ae/investor-relations", True, SWEEP_DATE,
    "301 redirect to modon.com/investor-relations — followed")
R.record_primary_access("https://modon.com/investor-relations", True, SWEEP_DATE,
    "full IR library served: annual FS FY2021-FY2025, interims to H1-2026, AR2025")
R.record_primary_access("https://apigateway.adx.ae/adx/cdn/1.0/content/download/...",
    True, SWEEP_DATE, "ADX disclosure portal copies of the same filings (not needed — "
    "company site served everything)")
R.record_primary_access("https://www.centralbank.ae/en/forex-eibor/eibor-rates/", False,
    SWEEP_DATE, "HTTP 403 at the egress proxy; EIBOR fixings carried from the "
    "31-Mar-2026 published set via secondary mirrors, flagged as such")
R.record_primary_access("https://www.adx.ae (index history)", False, SWEEP_DATE,
    "Cloudflare challenge; FTSE ADX General Index history unobtainable — see the "
    "negative-search finding and the beta tier-3 flag")

# ---- study-year declaration: Modon discloses SEMI-ANNUALLY --------------------
R.declare_study_year("2026", ["H1-2026"])

# ---- driver gate table --------------------------------------------------------
R.add_driver("Development revenue (backlog conversion + new-launch sales, "
             "volume x realised price)", DriverMode.BOTTOM_UP,
             "Backlog AED 46.0bn (93% development) with disclosed sales units and "
             "values by geography; launch cadence from the masterplan disclosures; "
             "H1-2026 actuals anchor the conversion pace",
             [f_ir, f_plan, f_mkt, f_h1])
R.add_driver("Development cost per unit / gross margin", DriverMode.BOTTOM_UP,
             "Direct-cost note 6 discloses the development cost stack by line; "
             "construction escalator on its own driver class (tender-price index)",
             [f_h1, f_costs, f_fs])
R.add_driver("Rental income (investment properties + temporary infrastructure)",
             DriverMode.BOTTOM_UP,
             "Note 5 splits rental income by source; AR2025 gives 97% occupancy and "
             "GLA under management", [f_ir, f_fs])
R.add_driver("Hospitality revenue (keys x occupancy x rate)", DriverMode.BOTTOM_UP,
             "7,137 keys and 71% occupancy disclosed; segment revenue and direct "
             "costs disclosed", [f_ir, f_fs])
R.add_driver("Events, catering & tourism revenue", DriverMode.BOTTOM_UP,
             "Note 5 splits exhibitions/events, catering, temporary-infrastructure "
             "rental; AR2025 gives venue capacity, events and visitor counts",
             [f_ir, f_fs])
R.add_driver("Corporate load, tax path, working-capital cycle", DriverMode.BOTTOM_UP,
             "G&A note 7, income-tax note 11 (DMTT), and the balance-sheet "
             "receivable/payable/escrow structure are all disclosed",
             [f_tax, f_h1, f_fs])

# ---- validate -----------------------------------------------------------------
errors, warnings = R.validate()
print("errors:", errors)
print("warnings:", warnings)
print(R.qc_line())
fresh = R.check_freshness("2026-08-09")
print("freshness:", fresh or "OK — sweep and delivery same day")
assert not errors, errors
R.to_json(os.path.join(HERE, "sweep_register.json"))
print("wrote sweep_register.json —", R.counts())
