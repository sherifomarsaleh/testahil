"""AIRARABIA — four-ring Information Sweep register.

Runs BEFORE any forecast driver is set. Every mandatory category of every ring is
closed by a dated finding or a dated negative search. The Company ring is
primary-source-first: airarabia.com's investor-relations page was reachable and
served the audited FY2022-FY2025 statements, the Q1-2026 reviewed interim, and
the results presentations directly — no aggregator sits anywhere in the FS build
path. The FY2022-2024 statement PDFs are image scans and were OCR'd locally;
every OCR'd figure used in the model was cross-checked against the following
year's typed comparative column wherever one exists.
"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from research_sweep import (SweepRegister, AssetClass, Ring, FindingClass,
                            SourceType, DriverMode)

SWEEP_DATE = "2026-08-09"
R = SweepRegister("AIRARABIA", AssetClass.STOCK, SWEEP_DATE)
CO, IR, REG, PMD, PRESS, AGG = (SourceType.COMPANY_OFFICIAL, SourceType.COMPANY_IR,
                                SourceType.REGULATOR_OFFICIAL, SourceType.PRIMARY_MARKET_DATA,
                                SourceType.REPUTABLE_PRESS, SourceType.AGGREGATOR)

# ---- primary access log (success IS still logged) ---------------------------
R.record_primary_access("https://www.airarabia.com/en/about-us/investor-relations",
                        True, SWEEP_DATE,
                        "Reachable. Served audited FS FY2022-FY2025, Q1-2026 reviewed "
                        "interim, annual report 2025 and results presentations directly. "
                        "FY2022-24 FS PDFs are image scans — OCR'd locally, figures "
                        "cross-checked against later filings' typed comparatives.")
R.record_primary_access("https://www.dfm.ae/the-exchange/market-information/company/AIRARABIA",
                        True, SWEEP_DATE,
                        "DFM disclosure page reachable (HTTP 200) — used as the exchange "
                        "cross-check for the listing venue and disclosures; documents "
                        "themselves taken from the company's own IR page.")
R.declare_study_year("2026", ["Q1-2026"])

# ---------------------------------------------------------------- RING 1 GLOBAL
f_rate = R.add(Ring.GLOBAL, "rate cycle & USD/FX regime", FindingClass.S,
    "CBUAE base rate 3.65%, maintained 29-Jul-2026 mirroring the Fed hold; latest dot "
    "plot tilts hawkish (nine policymakers back higher 2026 rates). AED hard-pegged",
    "CBUAE press release; Gulf News Fed coverage", REG, "2026-07-29",
    url="https://www.centralbank.ae/en/news-and-publications/news-and-insights/press-release/cbuae-maintains-the-base-rate-at-3-65-1/",
    model_impact="Deposit-yield path on the AED 5.2bn cash pile (4.41% disclosed avg "
                 "rolls to ~3.7%) and the Kd glide; the MC carry anchor stays the Fed "
                 "path per the pegged-currency rule.")

f_fuel = R.add(Ring.GLOBAL, "commodity complex (input/output)", FindingClass.S,
    "Jet fuel USD 158.77/bbl (IATA monitor, early Aug-2026) after the H1 conflict "
    "spike; IATA's June-2026 full-year assumption jet USD 152/Brent 95 vs EIA July "
    "STEO Brent 81.91 (2026) -> 64.76 (2027) — the 2026-27 fuel path is genuinely "
    "contested between the two official-sector sources",
    "IATA Jet Fuel Price Monitor; IATA 07-Jun-2026 outlook; EIA July-2026 STEO",
    REG, "2026-08-09",
    url="https://www.iata.org/en/publications/economics/fuel-monitor/",
    model_impact="Fuel cost per pax is the study's CENTRAL CONTESTED JUDGEMENT, priced "
                 "both ways: base = EIA relief path (195 -> 165 AED/pax), alternative = "
                 "IATA high-fuel persistence (210 -> 205). Fuel is 37% of direct costs.")

f_gdem = R.add(Ring.GLOBAL, "global sector demand", FindingClass.S,
    "IATA June-2026 mid-year update: 2026 global RPK growth cut to +2.1% (from +4.9% "
    "in Dec-2025), net margin 2.0%, MIDDLE EAST RPK -11.4% on the Feb-Mar airspace "
    "closures with phased restoration to ~1-Jun-2026",
    "IATA press release 07-Jun-2026", REG, "2026-06-07",
    url="https://www.iata.org/en/pressroom/2026-releases/06-07-middle-east-disruptions-high-fuel-prices-halve-airline-industry-profitability/",
    model_impact="FY2026 pax path set at -1.6% (Q1 actual -11%, H2 recovery) — the "
                 "regional average is dominated by the big hub carriers; Air Arabia's "
                 "own Q1 print (-5% group pax, record 86.4% load factor) shows milder "
                 "impact and anchors the recovery slope.")

f_supply = R.add(Ring.GLOBAL, "trade / sanctions / supply chains", FindingClass.S,
    "Airbus A320-family rate-75 target pushed to end-2027; GTF powder-metal "
    "inspections still constrain engines; Jan-Feb 2026 deliveries ~20% below 2025 "
    "pace; Airbus filed a damages claim against Pratt & Whitney (Mar-2026). Air "
    "Arabia's neos are CFM LEAP-powered — exposure is via market tightness, not its "
    "own engines. Narrowbody lease rates easing from record highs (new A320neo "
    ">= ~USD 400k/mo, IBA)",
    "Aerospace Global News; Simple Flying; IBA public articles", PRESS, "2026-03-31",
    model_impact="Caps the feasible delivery ramp (~10/yr vs the order's nominal pace) "
                 "and supports the wet-lease unwind assumption inside other-costs/pax.")

# --------------------------------------------------------------- RING 2 COUNTRY
f_uae = R.add(Ring.COUNTRY, "sovereign macro (inflation, policy rate, FX/deval risk)",
    FindingClass.S,
    "UAE GDP +5.6% (2025 est.) with ~5.6% projected for 2026 (CBUAE QER Mar-2026; IMF "
    "+4.8%/+5.0%); inflation projected 1.8% (2026), 2.0% (2027). AED T-Bond auction "
    "Jul-2026: Jan-2031 tranche YTM 4.48%, 4bp over UST; May-2026: 4.30%",
    "CBUAE Quarterly Economic Review Mar-2026; UAE Ministry of Finance auction results",
    REG, "2026-07-30",
    url="https://mof.gov.ae/en/news/uae-successfully-concludes-may-2026-treasury-bond-auction/",
    model_impact="rf = 4.48% AED sovereign less the UAE's own 0.42% Aa2 default spread "
                 "= 4.06% rf*; cost-class escalators for landing/handling at UAE CPI "
                 "~2%; terminal rf norm-built at 4.0%.")

f_reg = R.add(Ring.COUNTRY, "regulatory environment (regulator, caps, tariffs, tax/subsidy)",
    FindingClass.S,
    "UAE Domestic Minimum Top-up Tax (DMTT) 15% effective 1-Jan-2025 for Pillar-Two "
    "groups — Air Arabia is in scope and provides at 15% (Note 27, FY2025 filing); "
    "FY2024 was the 9% CT year, FY2023 untaxed",
    "FY2025 audited financial statements Note 27; UAE MoF Pillar Two announcement",
    CO, "2026-02-13",
    model_impact="Forecast tax rate held at the statutory 15% (audited effective "
                 "prints: 8.79% FY2024, 11.60% FY2025 — exempt income keeps realised "
                 "below statutory; holding 15% is the conservative anchor).")

f_pol = R.add(Ring.COUNTRY, "fiscal / political events with sector read-through",
    FindingClass.S,
    "Feb-Mar 2026 regional conflict closed or restricted 7+ countries' airspace "
    "(Iran, Iraq, Israel, Kuwait, Bahrain, Lebanon, parts of Jordan) with phased "
    "restoration through ~1-Jun-2026; Sharjah's own hub kept operating",
    "Simple Flying disruption round-up; Air Arabia Q1-2026 press release", PRESS,
    "2026-06-01",
    model_impact="Explains the Q1-2026 prints (pax -11% consolidated, net profit -22%) "
                 "and sets FY2026 as a dip-then-recover year rather than a trend break; "
                 "recurrence carried in the bear scenario.")

f_idx = R.add(Ring.COUNTRY, "market benchmark for the cost-of-equity regression",
    FindingClass.S,
    "The ordinary shares are listed on the Dubai Financial Market — stated identically in "
    "Note 1 of the FY2025 audited statements, the FY2025 annual report, and the Q1-2026 "
    "interim (Note 1); the annual report's own share-price performance chart benchmarks the "
    "stock against the DFM general index. The company's INVESTMENT portfolio holds both "
    "DFM-listed (AED 5,631mn) and Abu Dhabi-listed (AED 4,730mn) securities (Note 11), which "
    "is why the listing venue was read off the filing rather than inferred. The FTSE ADX "
    "General Index 2011-2026 is the series the exchange-keyed beta rule resolves for DFM "
    "names under a registered interim substitution (no DFM General series is registered)",
    "FY2025 audited financial statements Note 1 and Note 11; FY2025 annual report; Q1-2026 "
    "interim Note 1; FTSE ADX General Index history (aggregator, index only)",
    CO, "2026-08-17",
    model_impact="Beta ADOPTED from the own-stock 5-year weekly regression against the FTSE "
                 "ADX General index (0.812, R2 0.135), the regressor the rule resolves for a "
                 "DFM-listed name. The DFM General series held in the repo gives 1.086 at R2 "
                 "0.402 — 3x the explanatory power and worth -0.83/share — and is published as "
                 "a priced cross-check; registering it is a pending rule amendment, not a "
                 "study-level choice.")

# --------------------------------------------------------------- RING 3 INDUSTRY
f_dem = R.add(Ring.INDUSTRY, "demand drivers & capacity/supply balance", FindingClass.S,
    "Sharjah Airport 2025: 19.48mn passengers +13.9% (2024: 17.1mn, 2023: 15.36mn); "
    "Dubai tourism record 19.59mn visitors 2025; UAE tourism ~13% of GDP",
    "Sharjah Airport Authority press release Jan-2026; Khaleej Times", REG, "2026-01-31",
    url="https://www.sharjahairport.ae/en/",
    model_impact="Supports the +8-9%/yr pax path FY2027-30 at the home hub — the "
                 "airport itself is growing double-digit and Air Arabia is its anchor "
                 "carrier.")

f_price = R.add(Ring.INDUSTRY, "pricing", FindingClass.S,
    "Q1-2026: Air Arabia revenue +1% on -11% consolidated pax with a RECORD 86.4% "
    "load factor — constrained regional capacity lifted yields materially; IATA "
    "expects yield normalisation as capacity restores",
    "Air Arabia Q1-2026 results presentation", IR, "2026-05-13",
    fiscal_period="Q1-2026",
    model_impact="Fare path: +1.9% FY2026 then -1.6% FY2027 (give-back) then +1%/yr — "
                 "yield discipline without extrapolating a conflict-scarcity price.")

f_entrants = R.add(Ring.INDUSTRY, "new entrants (named-competitor level)", FindingClass.S,
    "Wizz Air Abu Dhabi permanently ceased operations 01-Sep-2025 (engine degradation "
    "in hot/harsh conditions, geopolitics, market access) — the only true ULCC "
    "challenger in the UAE exited; Air Arabia Abu Dhabi is expanding ~40% capacity "
    "into the vacuum",
    "Wizz Air strategic realignment statement; Khaleej Times 14-Jul-2025", PRESS,
    "2025-09-01",
    model_impact="Supports the JV-network growth path (assoc profit +18%/yr mid-window) "
                 "and the ancillary/yield assumptions at the Abu Dhabi hub.")

f_tech = R.add(Ring.INDUSTRY, "technology substitution", FindingClass.C,
    "No modal substitution threat at Air Arabia's stage lengths (2-5hr international "
    "short-haul across GCC/South Asia/Levant — no rail alternative crosses these "
    "borders); the relevant technology shift is the A320neo's ~20% lower fuel burn, "
    "which the company itself cites",
    "Q4-2025 results presentation; company press release on first neo", IR, "2026-02-13")

f_comp = R.add(Ring.INDUSTRY, "competitor capacity / price moves (named)", FindingClass.S,
    "flydubai: 12 MAX deliveries due 2026, ordered up to 150 A321neo (first Airbus "
    "order, Nov-2025) + 75 firm MAX; Etihad record 22.4mn pax 2025, summer-2026 "
    "capacity +10%; Emirates summer-2026 frequencies ~-12% y/y post-conflict; Jazeera "
    "Airways FY2025 net profit KWD 21.8mn (+114%) on 5mn+ pax",
    "FlightGlobal; VisaHQ/Etihad; Zawya Jazeera FY2025 coverage", PRESS, "2026-02-28",
    model_impact="Competitive capacity re-expands into 2027 — one driver of the "
                 "FY2027 fare give-back; Jazeera's multiple anchors the relative lens.")

# --------------------------------------------------------------- RING 4 COMPANY
f_strat = R.add(Ring.COMPANY, "strategic plans & guidance", FindingClass.S,
    "120-aircraft A320/A321neo-family order (73 A320neo + 27 A321neo + 20 A321XLR, "
    "2019, ~USD 14bn list): first neo delivered 29-Sep-2025 (CFM LEAP, 174 seats), "
    "nine A320-family added in FY2025 to a 90-aircraft operating fleet; pre-delivery "
    "payments 2,028.3 on the balance sheet",
    "Company press release (first neo); Q4-2025 results presentation; FY2025 FS Note 7",
    CO, "2026-02-13",
    model_impact="Fleet-led pax path 90 -> ~115 aircraft by FY2030; capex path "
                 "~AED 1.9-2.0bn/yr incl. the PDP ladder; D&A path fleet-driven.")

f_disc = R.add(Ring.COMPANY, "regular disclosures", FindingClass.D,
    "Audited FY2025 consolidated statements (KPMG Lower Gulf, unqualified, "
    "13-Feb-2026): revenue 7,787.6 (+15%), net profit 1,628.7, EPS 0.35; Note 43 "
    "restates FY2024 comparatives (lease-rental revenue reclass, maintenance "
    "provisions, lease/borrowing classification). FY2024, FY2023, FY2022 audited "
    "statements all retrieved from the same IR page",
    "airarabia.com investor relations — audited FS FY2022-FY2025", CO, "2026-02-13",
    is_fs_data=True, fiscal_period="FY2025",
    model_impact="Unlocks the full bottom-up build: revenue disaggregation (Note 28a), "
                 "the 11-line direct-cost stack (Note 29), unit economics per pax, and "
                 "the restated balance-sheet history.")

f_fs24 = R.add(Ring.COMPANY, "official financial statements", FindingClass.D,
    "FY2024 audited statements (revenue 6,639.1 as reported / 6,765.9 restated; net "
    "profit 1,467.6); FY2023 audited (5,999.8 / 1,547.7); FY2022 audited (5,241.8 / "
    "1,222.3) — four complete audited fiscal years in hand, each cross-checked "
    "against the following filing's comparative column",
    "airarabia.com investor relations — audited FS FY2022-FY2024", CO, "2025-02-13",
    is_fs_data=True, fiscal_period="FY2024",
    model_impact="Three-year historical IS/BS/CF in the study (FY2023-25) with FY2022 "
                 "as the fourth-year context column; DSO/DPO/deferred-income cycle "
                 "measured from the statements.")
R.add(Ring.COMPANY, "official financial statements", FindingClass.D,
      "FY2023 audited statements: revenue 5,999.750, PBT 1,547.696, D&A 647.327, "
      "no income tax (pre-CT era)",
      "airarabia.com IR — FY2023 audited FS (OCR'd scan, figures confirmed against the "
      "FY2024 filing's typed comparatives)", CO, "2024-02-13",
      is_fs_data=True, fiscal_period="FY2023",
      model_impact="FY2023 column of the historical statements and the cost-stack "
                   "history (fuel 1,690.6, staff 774.8, maintenance 438.9).")
R.add(Ring.COMPANY, "official financial statements", FindingClass.C,
      "FY2022 audited statements: revenue 5,241.830, profit 1,222.306, EPS 0.26",
      "airarabia.com IR — FY2022 audited FS (OCR'd scan, confirmed against FY2023 "
      "comparatives)", CO, "2023-02-13",
      is_fs_data=True, fiscal_period="FY2022")

f_q1 = R.add(Ring.COMPANY, "IR communications (calls, presentations, releases)",
    FindingClass.S,
    "Q1-2026 reviewed interim + results presentation: revenue 1,800.4 (+1%), net "
    "profit 278.1 (-22%), consolidated pax 2.68mn (-11%), group pax 4.70mn (-5%), "
    "record 86.4% load factor — the study year's only disclosed quarter, swept in "
    "BEFORE the build. Q4-2025 presentation: FY2025 pax 13.06mn, LF 85.3%, fleet 90 "
    "+5 short-term leases, 219 destinations, cash AED 5.3bn",
    "Air Arabia Q1-2026 and Q4-2025 results presentations", IR, "2026-05-13",
    fiscal_period="Q1-2026",
    model_impact="FY2026 revenue cross-check (Q1 seasonal gross-up = 7,880 vs build "
                 "7,869); pax/LF/fleet unit history that no financial statement "
                 "carries.")

f_oneoff = R.add(Ring.COMPANY, "one-off base-resetting transactions", FindingClass.S,
    "During FY2025 the Group raised Air Arabia Egypt from 40% to 49% and entered "
    "'Air Arabia DMM LLC' — a new 49% Saudi JV with Saudi investors to establish a "
    "Dammam-based airline (Note 1h); Fly Arna (Armenia) and Air Arabia Jordan are in "
    "liquidation",
    "FY2025 audited FS Note 1", CO, "2026-02-13",
    model_impact="JV-network share-of-profit path (+18%/yr mid-window with FY2026 "
                 "held flat for DMM start-up costs); the JV network is the study's "
                 "dual-framed bridge item (book 363.4 vs capitalised 2,850).")

f_own = R.add(Ring.COMPANY, "ownership / stake changes (named-transaction rule)",
    FindingClass.C,
    "Share capital unchanged at 4,666.7mn shares since FY2022; the FY2025 auditor's "
    "report notes the Group PURCHASED SHARES during 2025 (legal-requirement "
    "disclosure item v) — no cancellation disclosed, capital unchanged; no "
    "named-stake change in the free float found",
    "FY2025 audited FS — auditor's report and Note 18", CO, "2026-02-13")

f_mgmt = R.add(Ring.COMPANY, "management & capital actions", FindingClass.S,
    "FY2025 dividend 30 fils/share (AED 1.4bn, ~USD 381mn) APPROVED at the AGM of "
    "12-Mar-2026; board elected for three years. DPS ladder: 0.15 (FY22) / 0.20 "
    "(FY23) / 0.25 (FY24) / 0.30 (FY25)",
    "Air Arabia press release — AGM 12-Mar-2026", CO, "2026-03-12",
    url="https://press.airarabia.com/air-arabia-shareholders-approve-30-dividend-distribution-at-annual-general-meeting/",
    model_impact="q_annual for the price cone = 0.30/5.24 = 5.73%; payout path 100% "
                 "-> ~85%; the anchor roll nets the 0.30 paid inside the window.")

# ---- negative searches ------------------------------------------------------
f_neg_seats = R.add_negative(Ring.COMPANY, "regular disclosures",
    "ASK/seat-capacity, stage-length or per-route disclosure in FS, annual report or "
    "IR decks (searched all retrieved documents)", SWEEP_DATE)
f_neg_hedge = R.add_negative(Ring.COMPANY, "regular disclosures",
    "fuel hedge RATIO/volume disclosure (Note 24 discloses instruments and fair "
    "values 2026-2028 but no hedged share)", SWEEP_DATE)
f_neg_split = R.add_negative(Ring.COMPANY, "strategic plans & guidance",
    "owned-vs-leased split of forward aircraft deliveries (searched FS notes, AR, "
    "presentations)", SWEEP_DATE)

# ---- driver gate table ------------------------------------------------------
R.add_driver("Passengers x load factor (pax path)", DriverMode.BOTTOM_UP,
             "Disclosed pax and LF per presentation KEY PERFORMANCE tables FY2022-Q1-2026; "
             "fleet path from the disclosed order/deliveries", [f_q1, f_strat, f_dem])
R.add_driver("Fare + baggage per pax", DriverMode.BOTTOM_UP,
             "Note 28a passenger+baggage revenue over disclosed pax", [f_disc, f_price])
R.add_driver("Ancillary per pax", DriverMode.BOTTOM_UP,
             "Note 28a 'other airline related services' over disclosed pax", [f_disc])
R.add_driver("Fuel cost per pax (dual-framed)", DriverMode.BOTTOM_UP,
             "Note 29 fuel line over disclosed pax; forward path on the EIA/IATA "
             "commodity escalator — its own driver class, never a CPI proxy",
             [f_disc, f_fuel]),
R.add_driver("Staff / maintenance / landing / handling per pax", DriverMode.BOTTOM_UP,
             "Note 29 lines over disclosed pax, one escalator per driver class "
             "(wage, MRO, tariff-CPI)", [f_disc, f_uae])
R.add_driver("Fleet capex incl. pre-delivery payments", DriverMode.TOP_DOWN,
             "Owned-vs-leased forward delivery split is NOT disclosed (dated negative "
             "search) — capex path is a top-down construction on the FY2025 actual and "
             "the order ladder, flagged and heavily sensitised", [f_neg_split, f_strat])
R.add_driver("JV/associate profit share", DriverMode.BOTTOM_UP,
             "Note 12 per-investee 100%-basis P&Ls and shares", [f_oneoff, f_disc])
R.add_driver("Working capital ratio", DriverMode.BOTTOM_UP,
             "Deferred income / payables / maintenance provisions from the audited "
             "balance sheets, three-year centre", [f_disc, f_fs24])

# ---- validate + emit --------------------------------------------------------
errors, warnings = R.validate()
for w in warnings:
    print("WARN:", w)
for e in errors:
    print("ERROR:", e)
assert not errors, f"{len(errors)} sweep validation errors"
fresh = R.check_freshness("2026-08-09")
if fresh:
    print("FRESHNESS:", fresh)
R.to_json(os.path.join(HERE, 'sweep_register.json'))
print(R.qc_line())
print(f"findings={len(R.findings)} drivers={len(R.drivers)} "
      f"primary_access={len(R.primary_access)} study_year={R.study_year} "
      f"quarters={R.study_quarters_disclosed}")
