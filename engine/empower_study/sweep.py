"""EMPOWER — four-ring Information Sweep register.

Runs BEFORE any forecast driver is set. Every mandatory category of every ring is
closed by a dated finding or a dated negative search.

SOURCING NOTE: the company's own media archive at empower.ae served every filing
directly (FY2022-FY2025 audited annuals, Q1/Q2-2026 interims, H1-2026 earnings
deck). The IR *HTML pages* return 403 to non-browser agents — the document store
itself does not; both attempts are logged via record_primary_access. FY2025 and
Q1-2026 are scanned PDFs read by OCR with every unreadable cell recorded as null
in the extraction JSONs, never guessed. External-ring findings and their URLs
live in sweep_external.json (35 sources); the register below carries the subset
that sets or bounds a model driver."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from research_sweep import (SweepRegister, AssetClass, Ring, FindingClass,
                            SourceType, DriverMode)

SWEEP_DATE = "2026-08-09"
R = SweepRegister("EMPOWER", AssetClass.STOCK, SWEEP_DATE)
CO, IR_, REG, PMD, PRESS, AGG = (SourceType.COMPANY_OFFICIAL, SourceType.COMPANY_IR,
                                 SourceType.REGULATOR_OFFICIAL,
                                 SourceType.PRIMARY_MARKET_DATA,
                                 SourceType.REPUTABLE_PRESS, SourceType.AGGREGATOR)

# -------------------------------------------------- primary access log
R.record_primary_access("https://www.empower.ae/investor-relations/", False, SWEEP_DATE,
    "IR HTML pages return HTTP 403 to non-browser clients (bot protection)")
R.record_primary_access("https://www.empower.ae/investor-relations/financial/financial-statements/",
    True, SWEEP_DATE,
    "Reachable with a browser user-agent; lists the full filing archive")
R.record_primary_access("https://www.empower.ae/media/lgbpvouk/empower_fs_2025_e_09-02-2026.pdf",
    True, SWEEP_DATE, "FY2025 audited consolidated FS, 85pp (scan; OCR extraction)")
R.record_primary_access("https://www.empower.ae/media/0nspfjmz/empower_fs_2024_e_14-02-2025.pdf",
    True, SWEEP_DATE, "FY2024 audited consolidated FS (text layer)")
R.record_primary_access("https://www.empower.ae/media/vn1fsmte/2023_financial_statements_e.pdf",
    True, SWEEP_DATE, "FY2023 audited consolidated FS (text layer)")
R.record_primary_access("https://www.empower.ae/media/0itbxotb/empower_en_fs_2022.pdf",
    True, SWEEP_DATE, "FY2022 audited consolidated FS (text layer)")
R.record_primary_access("https://www.empower.ae/media/ld0h1d2a/empower_fs_q1_e_06_05_2026.pdf",
    True, SWEEP_DATE, "Q1-2026 condensed interim FS (scan; OCR extraction)")
R.record_primary_access("https://www.empower.ae/media/emibya3p/empower_fs_q2_e_05_08_2026.pdf",
    True, SWEEP_DATE, "Q2/H1-2026 condensed interim FS (text layer)")
R.record_primary_access("https://www.empower.ae/media/z1djkwz3/earnings-presentation-h1-2026.pdf",
    True, SWEEP_DATE, "H1-2026 earnings presentation, 24pp")

R.declare_study_year("2026", ["Q1-2026", "Q2-2026"])

# ---------------------------------------------------------------- RING 1 GLOBAL
f_rate = R.add(Ring.GLOBAL, "rate cycle & USD/FX regime", FindingClass.S,
    "Fed on hold; CBUAE Base Rate held at 3.65% on 29-Jul-2026 (AED hard-pegged, so the "
    "UAE imports the Fed path); FOMC dots carry a hawkish 2026 tilt",
    "CBUAE press release 29-Jul-2026; Fed policy history", REG, "2026-07-29",
    model_impact="Sets the floating leg of the cost of debt (both RCFs price at EIBOR + "
                 "margin; 3M EIBOR ~3.66%) and the near-term discount-rate environment. "
                 "The AED peg removes the FX leg from the valuation entirely.")

f_cmdty = R.add(Ring.GLOBAL, "commodity complex (input/output)", FindingClass.S,
    "District cooling is an electricity-conversion business: purchased electricity & "
    "water are the dominant cash cost (AED 1,467.7m from DEWA in FY2025 = 43% of "
    "revenue). DEWA's fuel surcharge (6 fils/kWh, Jun-2026) floats monthly with fuel",
    "FY2025 audited FS note 12 (related-party purchases); DEWA published tariff",
    CO, "2026-02-09", is_fs_data=True, fiscal_period="FY2025",
    model_impact="Cost-stack escalator class 1: purchased E&W escalates on the DEWA "
                 "tariff + consumption volume, never on a generic CPI index.")

f_gdem = R.add(Ring.GLOBAL, "global sector demand", FindingClass.C,
    "Cooling demand is local by construction (chilled water does not travel); global "
    "read-through is limited to the GCC district-cooling build-out cycle and equipment "
    "supply chains", "GCC district cooling sector coverage", PRESS, "2026-06-01",
    model_impact="")

f_trade = R.add(Ring.GLOBAL, "trade / sanctions / supply chains", FindingClass.S,
    "The Feb-Apr 2026 Iran conflict struck UAE logistics/energy nodes (Dubai airport, "
    "Jebel Ali, Ruwais); ceasefire from 8-Apr-2026, formalised 12/17-Jun, but declared "
    "'over' by the US on 8-Jul with low-intensity fighting since — a fragile truce, "
    "status contested across sources as of the sweep date (both readings recorded)",
    "Wikipedia conflict pages + wire coverage (sweep_external.json, COUNTRY sources)",
    PRESS, "2026-08-09",
    model_impact="The single live macro overhang: sets the bear-case consumption path "
                 "and the catalysts section; also why the market gate's regional "
                 "de-rating context matters when reading the price map.")

# --------------------------------------------------------------- RING 2 COUNTRY
f_macro = R.add(Ring.COUNTRY, "sovereign macro (inflation, policy rate, FX/deval risk)",
    FindingClass.D,
    "CBUAE cut UAE 2026 GDP growth guidance to 1.7% from 5.6% after the strikes; base "
    "rate 3.65%; AED peg intact throughout the conflict; AED sovereign curve: Jan-2031 "
    "T-Bond auctioned at 4.48% YTM on 30-Jul-2026 (spread ~4bp over comparable UST)",
    "CBUAE statements; UAE Ministry of Finance auction result 30-Jul-2026", REG,
    "2026-07-30",
    model_impact="rf = 4.48% (longest AED sovereign print, 4.4y tenor, tenor gap "
                 "flagged); rf* = 4.48% - 0.393% (UAE's own Damodaran rating-basis "
                 "default spread) = 4.09% for the rating-basis Ke build; GDP cut sets "
                 "the near-term consumption driver's ceiling.")

f_reg = R.add(Ring.COUNTRY, "regulatory environment (regulator, caps, tariffs, tax/subsidy)",
    FindingClass.S,
    "Dubai district cooling is tariff-regulated: Executive Council Resolution 6/2021 + "
    "RSB regulation RD10 (tariff approval/adjustment) + Resolution 87/2025 (fees/fines "
    "update). No 2024-26 tariff cut found. UAE CT 9% from 2024 (Empower's FY2025 "
    "effective rate a clean 9.0%); Pillar-Two 15% DMTT applies to >=EUR 750m groups — "
    "whether DEWA-level consolidation sweeps Empower in is CONTESTED and unresolved",
    "Dubai Executive Council resolutions / RSB; FY2025 FS note 28; UAE MoF DMTT "
    "guidance", REG, "2026-08-09",
    model_impact="Pricing power is capped by the regulator: the tariff path is held "
                 "FLAT in nominal AED (no real escalation is assumed anywhere). The "
                 "tax question is the study's DUAL-FRAMED contested judgement: the "
                 "model is computed at 9% AND at 15% and both are published side by "
                 "side — never averaged.")

f_fisc = R.add(Ring.COUNTRY, "fiscal / political events with sector read-through",
    FindingClass.S,
    "Dubai 2040 Urban Master Plan and the post-conflict rebuild keep the connected-"
    "capacity pipeline alive (Empower guides 100-110k RT of new connections for 2026 "
    "even in the conflict year); hospitality occupancy is the transmission channel "
    "from geopolitics to consumption revenue",
    "H1-2026 earnings presentation p13; CBUAE GDP guidance", IR_, "2026-08-05",
    model_impact="Anchors the volume driver: connected-RT additions continue through "
                 "the shock (capacity revenue is contracted), while consumption per "
                 "connected RT carries the macro risk. This split is the model's "
                 "central mechanism.")

# -------------------------------------------------------------- RING 3 INDUSTRY
f_bal = R.add(Ring.INDUSTRY, "demand drivers & capacity/supply balance", FindingClass.D,
    "Empower: 1,707k RT connected / 2,018k RT contracted at 30-Jun-2026 (+51k / +74k "
    "in H1); guidance 100-110k RT of 2026 connections; FY2025 saw 163 new customer "
    "agreements (+171.7k RT contracted). The contracted>connected gap (311k RT) is a "
    "pre-sold growth backlog", "H1-2026 earnings presentation pp3-4,10,13; FY2025 FS "
    "directors' report", IR_, "2026-08-05",
    model_impact="THE volume driver: connected-RT path built from the company's own "
                 "guidance and backlog, not a market growth assumption.")

f_price = R.add(Ring.INDUSTRY, "pricing", FindingClass.D,
    "Consumption revenue disclosed in the auditor's KAM in each audited filing: "
    "FY2022 1,463.0m / FY2023 1,719.6m / FY2024 1,895.3m / FY2025 1,923.9m; revenue "
    "mix H1-2026 per the earnings deck: demand 40% / consumption 49% / others 11%. "
    "Tariffs RSB-approved; DEWA slab tariff 23-38 fils/kWh + 6 fils fuel surcharge",
    "FY2022-FY2025 audited FS auditor KAM sections (mix %: H1-2026 deck p17)", CO,
    "2026-02-09", is_fs_data=True, fiscal_period="FY2025",
    model_impact="Splits revenue into a contracted capacity leg (grows with connected "
                 "RT) and a weather/occupancy consumption leg (RTh x tariff) — the "
                 "two-leg unit build the forecast runs on.")

f_entr = R.add(Ring.INDUSTRY, "new entrants (named-competitor level)", FindingClass.C,
    "Dubai DC is a three-player market with concession-like exclusivity by district: "
    "Empower (~80% Dubai share per its own deck), Tabreed, Emicool (private, Dubai "
    "Investments/Actis JV, USD 1bn 2022 valuation). No new entrant found 2024-26; "
    "Resolution 6/2021 raises the regulatory bar to entry",
    "H1-2026 deck; Dubai Investments/Actis disclosures; sweep_external.json", PRESS,
    "2026-08-09", model_impact="")

f_subst = R.add(Ring.INDUSTRY, "technology substitution", FindingClass.C,
    "No substitution threat inside the horizon: district cooling IS the efficiency "
    "technology displacing standalone chillers (mandated connections under Dubai "
    "policy); the live technology question is efficiency capex (TES tanks, treated "
    "sewage effluent water), a cost line not a demand risk",
    "Sector coverage + company sustainability disclosures", PRESS, "2026-06-01",
    model_impact="")

f_peers = R.add(Ring.INDUSTRY, "competitor capacity / price moves (named)", FindingClass.D,
    "Tabreed (DFM: TABREED): FY2025 revenue AED 2.46bn, EBITDA 1.27bn, NP 465m, net "
    "debt 4.6x EBITDA, ~USD 2.11bn market cap, derived trailing P/E ~16.6x, yield "
    "~4.8%; Q1-2026 NP -32% on finance costs. DEWA (parent, DFM): P/E ~16.8x, yield "
    "~4.4-5.0%. Empower itself at 1.50: trailing P/E 14.2x, EV/EBITDA ~10.8x, yield "
    "5.8%", "Tabreed FY2025/Q1-2026 results via DFM disclosures + market data "
    "(cross-check only, never a build source)", PMD, "2026-08-07",
    model_impact="Peer set for the relative-multiples lens; Tabreed's 4.6x leverage "
                 "vs Empower's 1.8x is why the multiple gap is adjusted at the EV "
                 "line, not read off P/E raw.")

# --------------------------------------------------------------- RING 4 COMPANY
f_fs = R.add(Ring.COMPANY, "official financial statements", FindingClass.D,
    "Five audited years in hand from the company's own archive (FY2021 comparative + "
    "FY2022-FY2025 filings, PwC, unqualified): revenue 2,463.9 / 2,792.5 / 3,035.2 / "
    "3,260.5 / 3,419.3m; EBITDA margin 47.6-50.5% every year; net profit FY2025 "
    "1,003.9m (EPS 0.099); total borrowings 5,503.4m (two AED 2.75bn RCFs, EIBOR + "
    "margin, Sep-27/Feb-28); FY2025 capitalisation rate 4.92% (own disclosed borrowing "
    "cost; 2024: 5.993%)",
    "FY2022-FY2025 audited consolidated FS, empower.ae media archive", CO,
    "2026-02-09", is_fs_data=True, fiscal_period="FY2025",
    model_impact="The audited historical panel every statement roll-forward starts "
                 "from; the 4.92% capitalisation rate anchors the marginal Kd above "
                 "the 4.48% sovereign print.")

f_int = R.add(Ring.COMPANY, "regular disclosures", FindingClass.D,
    "Q1-2026: revenue 630.6m, NP 208.5m. H1-2026: revenue 1,519.4m (+4.5%), NP 467.9m "
    "(+16.2%), EPS 0.0464. The growth is Q1-loaded: Q2 revenue FELL 2.7% y/y (888.8m) "
    "on consumption -42m RTh, effective full-load hours -9.0%, which note 30 ties "
    "partly to conflict impact on hospitality occupancy",
    "Q1-2026 and Q2/H1-2026 condensed interim FS (limited review)", CO, "2026-08-05",
    is_fs_data=True, fiscal_period="Q2-2026",
    model_impact="The study-year actuals the FY2026 forecast must reconcile to: "
                 "capacity revenue growing, consumption revenue shocked. Sets the "
                 "crux (transient vs structural consumption loss).")

f_q1 = R.add(Ring.COMPANY, "regular disclosures", FindingClass.D,
    "Q1-2026 standalone: revenue 630,573k, gross profit (derived H1-Q1 checks exact), "
    "NP 208,485k, EPS 0.0207 — pre-shock quarter, EBITDA margin 56.8% (deck p10)",
    "Q1-2026 condensed interim FS + H1-2026 deck", CO, "2026-05-06",
    is_fs_data=True, fiscal_period="Q1-2026",
    model_impact="Reconciliation anchor for the FY2026E build's first quarter.")

f_ir = R.add(Ring.COMPANY, "IR communications (calls, presentations, releases)",
    FindingClass.D,
    "H1-2026 earnings presentation: connected 1,707k RT (+51.1k in H1), contracted "
    "2,018k RT, FY2026 guidance 100-110k RT of connections, H1 EBITDA 773m (Q1 margin "
    "56.8% / Q2 46.7%), net debt 2,991m = 1.8x LTM EBITDA, revenue mix demand 40% / "
    "consumption 49% / others 11%, dividend AED 875m/yr committed for 2025 AND 2026 "
    "(437.5m paid Apr-2026)",
    "H1-2026 earnings presentation (24pp), empower.ae", IR_, "2026-08-05",
    model_impact="Carries the volume guidance, the leverage anchor and the dividend "
                 "commitment the equity lenses use; the ONLY source for the "
                 "capacity/consumption mix percentages (flagged: not in FS notes).")

f_own = R.add(Ring.COMPANY, "ownership / stake changes (named-transaction rule)",
    FindingClass.B,
    "DEWA raised its stake 56% -> 80% on 10/11-Feb-2026, buying Dubai Holding's 24% "
    "(2.4bn shares) at AED 2.16/share = AED 5.184bn — 44% above the 07-Aug-2026 close "
    "of 1.50. Free float now ~20% (Emirates Power Investment exited; retail/institutional "
    "float remains)",
    "DFM disclosure / DEWA announcement, named transaction", PRESS, "2026-02-11",
    model_impact="BASE CHANGER for the ownership lens: a related-party CONTROL price, "
                 "reported as a disclosed reference point and priced as an expert "
                 "cross-check — never presented as fair value by itself. Also framed "
                 "the float/liquidity risk note.")

f_acq = R.add(Ring.COMPANY, "one-off base-resetting transactions", FindingClass.S,
    "FY2023: acquired 70% of DXB CoolCo (Dubai Airports' district cooling, 35-year "
    "concession) for 892.5m cash + 157.5m NCI recognised; FY2024-25: minor NCI "
    "step-ups (Logstor 3%, Palm Utilities). FY2022: IPO/listing 16-Nov-2022 (10bn "
    "shares, par 0.10)",
    "FY2023/FY2024 audited FS notes 1/32/39", CO, "2025-02-14", is_fs_data=True,
    fiscal_period="FY2023",
    model_impact="Explains the FY2023 borrowings step (4.49bn) and the NCI line; the "
                 "airport concession is inside the connected-RT base, not a separate "
                 "leg (same lens).")

f_fs22 = R.add(Ring.COMPANY, "official financial statements", FindingClass.C,
    "FY2022 audited FS (listing year): revenue 2,792.5m, operating profit 1,051.9m, "
    "net profit 1,000.8m, total assets 9,655.0m, borrowings 4,489.6m — the fourth "
    "complete audited year in the panel, with FY2021 as its comparative column",
    "FY2022 audited consolidated FS, empower.ae media archive", CO, "2023-02-14",
    is_fs_data=True, fiscal_period="FY2022",
    model_impact="Extends the margin/cycle history to five observable years "
                 "(FY2021-FY2025); the FY2021-22 pre-listing comparatives are what "
                 "establish that the ~48-50% EBITDA margin predates the IPO.")

f_guid = R.add(Ring.COMPANY, "strategic plans & guidance", FindingClass.D,
    "FY2026 guidance: 100-110k RT of new connections; 2026E connected potential "
    "1,756-1,766k RT; dividend AED 875m/yr for 2025-26; net-debt discipline stated at "
    "~2x EBITDA; no new-emirate expansion announced",
    "H1-2026 earnings presentation pp12-13", IR_, "2026-08-05",
    model_impact="The explicit-window volume and payout drivers are the company's own "
                 "published numbers, sensitised around, not replaced.")

f_mgmt = R.add(Ring.COMPANY, "management & capital actions", FindingClass.S,
    "2024 refinancing: repaid 3.75bn, drew 4.75bn (net fee); 2025: full 6.75bn "
    "refinance into the two 2.75bn+2.75bn RCFs with a REDUCED interest margin (note "
    "19) and covenant reset assessed as not substantial; interest capitalised 10.7m; "
    "no buyback, no capital increase since IPO",
    "FY2024/FY2025 audited FS note 19", CO, "2026-02-09", is_fs_data=True,
    fiscal_period="FY2024",
    model_impact="Kd evidence chain: own refinance pricing (capitalisation rate 4.92% "
                 "in 2025 vs 5.993% in 2024) tracks EIBOR down — the marginal Kd is "
                 "built from live EIBOR + the implied margin, not a historical rate.")

# ------------------------------------------------------------- negative searches
f_neg_seg = R.add_negative(Ring.COMPANY, "regular disclosures",
    "'Empower capacity charge tariff AED per RT per annum site:empower.ae', FS notes "
    "23/24 all years, IR deck — the AED amount of capacity vs consumption vs connection "
    "revenue is NOT disclosed anywhere except consumption in the auditor KAMs and the "
    "H1-2026 percentage mix; no per-RT tariff schedule is published", SWEEP_DATE)

f_neg_capex = R.add_negative(Ring.COMPANY, "strategic plans & guidance",
    "'Empower capex guidance 2026 AED investment plan' — the deck carries RT guidance "
    "but NO AED capex guidance; no capex budget disclosed in any filing or "
    "presentation", SWEEP_DATE)

f_neg_margin = R.add_negative(Ring.COMPANY, "regular disclosures",
    "'Empower RCF margin basis points EIBOR spread' — the exact margin over EIBOR is "
    "not disclosed in any filing (note 19 says only 'EIBOR + margin', 2025: 'reduction "
    "in interest margin'); the capitalisation rate (4.92%) is the closest disclosed "
    "all-in borrowing cost", SWEEP_DATE)

# ------------------------------------------------------------- DRIVER GATE TABLE
R.add_driver("Connected capacity (RT) path", DriverMode.BOTTOM_UP,
    "Company's own 2026 guidance (100-110k RT) and contracted backlog (311k RT gap) "
    "set additions; connected RT rolls forward from the disclosed 1,707k base.",
    [f_bal, f_guid, f_ir])
R.add_driver("Capacity (demand) revenue", DriverMode.BOTTOM_UP,
    "Connected RT x implied capacity revenue per RT (solved from the disclosed H1-2026 "
    "40% mix and disclosed total revenue — the per-RT rate is NOT published, so the "
    "level is implied and flagged; growth follows connected RT at a flat regulated "
    "tariff).", [f_price, f_bal, f_neg_seg, f_reg])
R.add_driver("Consumption revenue", DriverMode.BOTTOM_UP,
    "Disclosed KAM consumption history (1,463.0 -> 1,923.9m FY22-25) x an EFLH "
    "recovery path: 2026 carries the disclosed -9% EFLH shock; the recovery timing is "
    "the study's crux, computed both ways.", [f_price, f_int, f_fisc])
R.add_driver("Purchased electricity & water cost", DriverMode.BOTTOM_UP,
    "DEWA-sourced E&W (1,467.7m FY2025, disclosed related-party purchase) escalates on "
    "its own driver class — DEWA tariff (flat slabs + floating fuel surcharge) x "
    "consumption volume — never a blended CPI index.", [f_cmdty, f_price])
R.add_driver("Other cost lines (staff, other opex)", DriverMode.BOTTOM_UP,
    "Staff costs and other opex from the disclosed note components, escalated on a UAE "
    "wage/GDP path — a separate escalator class from energy.", [f_fs, f_macro])
R.add_driver("Capex", DriverMode.TOP_DOWN,
    "No AED capex guidance exists (negative search). Capex is modelled as cost-per-new-"
    "RT (derived from disclosed history: cash capex / RT added) x the guided RT path + "
    "maintenance on the installed base — top-down at the finest sourced level, flagged.",
    [f_neg_capex, f_bal]),
R.add_driver("Cost of debt & WACC glide", DriverMode.BOTTOM_UP,
    "Marginal Kd = live 3M EIBOR + the implied margin off the company's own 2025 "
    "refinance (capitalisation rate 4.92%); glide follows the EIBOR forward path; "
    "checked above the AED sovereign 4.48% at every node.", [f_mgmt, f_macro, f_neg_margin])
R.add_driver("Tax rate (9% vs 15% DMTT)", DriverMode.BOTTOM_UP,
    "9% is the disclosed FY2025 effective rate; the Pillar-Two DMTT question via "
    "DEWA-level consolidation is CONTESTED — the model publishes BOTH tax framings "
    "side by side (dual-framing rule applied to the study's central contested "
    "judgement).", [f_reg, f_fs])
R.add_driver("Terminal growth", DriverMode.BOTTOM_UP,
    "Bounded by the regulated flat-tariff regime and Dubai build-out saturation: set "
    "at long-run UAE nominal GDP-consistent 2.5%, cross-checked against the "
    "connected-RT saturation arithmetic; sensitised.", [f_reg, f_fisc, f_bal])

# ------------------------------------------------------------------------ OUTPUT
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
