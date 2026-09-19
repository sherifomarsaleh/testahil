"""GBCO — the Step 2A four-ring Information Sweep register.

WRITTEN 17-09-2026, AFTER THE STUDY RATHER THAN BEFORE IT, AND THAT IS STATED RATHER THAN
DISGUISED. [R-ENF-01 EXTENDED 03-Sep-2026] says the sweep runs through the shared register
or it does not run; GBCO committed no sweep script at all and sits on
engine/build_depth_audit/sweep_outstanding.json for that reason (self-audit S-7). This
file closes that entry. Every finding below is a document this study had ALREADY read and
consumed -- the same defect the ARCC precedent describes: the study held the facts and
wrote them where no checker could point at them.

The register is also what [R-BRIDGE-01] requires of the bridge: a study with neither a
sweep nor an investor-relations register cannot claim to stand on the latest disclosed
balance sheet, and an unestablished answer is not a clean one [R-ENF-04].
"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from research_sweep import (SweepRegister, AssetClass, Ring, FindingClass,
                            SourceType, DriverMode)

SWEEP_DATE = "2026-09-17"
R = SweepRegister("GBCO", AssetClass.STOCK, SWEEP_DATE)
CO, REG, PMD, PRESS, AGG, IR = (SourceType.COMPANY_OFFICIAL, SourceType.REGULATOR_OFFICIAL,
                                SourceType.PRIMARY_MARKET_DATA, SourceType.REPUTABLE_PRESS,
                                SourceType.AGGREGATOR, SourceType.COMPANY_IR)

R.record_primary_access(
    "https://ir.gb-corporation.com/en/filings", True, SWEEP_DATE,
    "HTTP 200. The company's own investor-relations filings page, which its 2Q26 earnings "
    "release names in its own footer ('Historical GB Corp segregated financials can be "
    "downloaded at ir.gb-corporation.com/en/filings'). Every audited statement, reviewed "
    "interim and earnings release this study consumes came from this channel and is held "
    "in engine/gbco_study/src/.")
R.declare_study_year("2026", ["Q1-2026", "Q2-2026"])

# ---------------------------------------------------------------- RING 1 GLOBAL
f_rates = R.add(Ring.GLOBAL, "rate cycle & USD/FX regime", FindingClass.S,
    "Egypt's policy rate is on a declining path from an elevated level -- overnight "
    "deposit 19.00%, held for a fourth consecutive meeting -- which is the shape the "
    "cost-of-capital glide inherits rather than a second assumption",
    "Central Bank of Egypt, Monetary Policy Committee statement of 20 August 2026, as "
    "registered in the house macro path engine/macro_paths/EG.json",
    REG, "2026-08-20",
    model_impact="The glide fractions in the cost-of-capital schedule ARE this path's own "
                 "cumulative progress, so the front-loading of the WACC decline is "
                 "inherited from the easing calendar and is not a free parameter.")

f_ckd = R.add(Ring.GLOBAL, "commodity complex (input/output)", FindingClass.S,
    "This is an assembler and distributor whose cost of sales is overwhelmingly IMPORTED "
    "and dollar-priced: FY2025 volumes split 31,349 CKD kits against 25,199 completely "
    "built-up units, both bought abroad",
    "GB Corp 4Q/FY25 earnings release, Table 2 (Egypt, Jordan and Iraq Passenger Cars "
    "Sales and After-Sales Activity)", CO, "2026-02-26",
    model_impact="It is why the currency path is a first-order driver of the gross margin "
                 "rather than a translation detail, and why note 26's USD borrowing leg "
                 "exists at all -- both are carried in the cost-of-debt build.")

f_gdem = R.add(Ring.GLOBAL, "global sector demand", FindingClass.C,
    "Vehicle demand reaches this company only through three national markets it actually "
    "sells in -- Egypt, Iraq and Jordan -- rather than through a world price; the group "
    "reports no export revenue outside those markets except within CV&CE",
    "GB Corp 4Q/FY25 earnings release, segment commentary", CO, "2026-02-26",
    model_impact="")

f_trade = R.add(Ring.GLOBAL, "trade / sanctions / supply chains", FindingClass.S,
    "GSO certification standards are being implemented in Iraq and Jordan, which the "
    "company expects to improve competitive dynamics against parallel imports; management "
    "expects gradual relief in regional operations from the second half of 2026",
    "GB Corp 4Q/FY25 earnings release, passenger-car commentary", CO, "2026-02-26",
    model_impact="Supports the volume growth ladder in the regional markets WITHOUT being "
                 "taken as a margin improvement: the forecast holds the gross margin at "
                 "the level the latest reviewed half filed [R-ANCHOR-01].")

# --------------------------------------------------------------- RING 2 COUNTRY
f_cbe = R.add(Ring.COUNTRY, "sovereign macro (inflation, policy rate, FX/deval risk)",
    FindingClass.D,
    "Annual headline inflation 14.9% in July 2026 against 14.3% in June; the CBE's own "
    "baseline is 16.0% average for 2026 and 12.0% for 2027, with the 7% target band "
    "regained in the second half of 2027",
    "Central Bank of Egypt, MPC statement of 20 August 2026 and Q1-2026 Monetary Policy "
    "Report, as registered in engine/macro_paths/EG.json", REG, "2026-08-20",
    model_impact="THE STUDY CARRIES NO INFLATION NUMBER OF ITS OWN [R-MACRO-01]: this is "
                 "the ladder the terminal growth, the terminal risk-free rate and the "
                 "derived currency path are all built from.")

f_fx = R.add(Ring.COUNTRY, "regulatory environment (regulator, caps, tariffs, tax/subsidy)",
    FindingClass.D,
    "Egyptian company law's employees' share of profit and the board of directors' bonus "
    "are deducted BEFORE the published basic earnings per share: FY2025 nil and EGP "
    "19,470 thousand, FY2024 EGP 76,549 and 19,016 thousand",
    "GB Corp FY2025 audited consolidated financial statements, note 10 (earnings per "
    "share), as reproduced in the Annual Report 2025", CO, "2026-02-26",
    model_impact="The relative cross-check lens is struck on the company's OWN published "
                 "basic figure on both sides of the multiple, rather than on profit "
                 "attributable to the parent divided by the share count [audit finding 26].",
    is_fs_data=True, fiscal_period="FY2025")

f_region = R.add(Ring.COUNTRY, "fiscal / political events with sector read-through",
    FindingClass.S,
    "Regional geopolitical developments tempered Iraq and Jordan through FY2025 and 1H26; "
    "1H26 profitability 'continued to benefit from strong performance in Egypt, partially "
    "offset by regional losses, restructuring and inventory-liquidation measures, and the "
    "challenging operating environment in Iraq and Jordan'",
    "GB Corp 2Q/1H26 earnings release, GB Auto segment commentary", CO, "2026-08-13",
    model_impact="It is one of the reasons the gross margin is held at the reviewed level "
                 "rather than recovered toward the FY2024 rate: the drag is live and the "
                 "company has not said it has ended.")

# -------------------------------------------------------------- RING 3 INDUSTRY
f_vol = R.add(Ring.INDUSTRY, "demand drivers & capacity/supply balance", FindingClass.D,
    "Egypt, Iraq and Jordan passenger-car volumes rose 34.5% y-o-y in FY2025 to 56,548 "
    "units; GB Auto holds a 21% market share in Egypt; capacity expansion at the Ain "
    "Sokhna facility is underway with an additional production shift under consideration",
    "GB Corp 4Q/FY25 earnings release, Table 2 and passenger-car / CV&CE commentary",
    CO, "2026-02-26",
    model_impact="The volume ladder on every one of the four disclosed business lines is "
                 "built off these units; capacity is not a binding constraint in the "
                 "window, which is what lets volume rather than utilisation be the driver.")

f_price = R.add(Ring.INDUSTRY, "pricing", FindingClass.D,
    "Average selling price is OBSERVABLE on the passenger-car line across three disclosed "
    "years -- 26,994 units on EGP 16,544.3mn, 42,043 on 36,533.4mn and 56,548 on "
    "52,827.3mn -- and on ONE disclosed year for commercial vehicles and light mobility",
    "GB Corp 4Q/FY23, 4Q/FY24 and 4Q/FY25 earnings releases, the volume and revenue tables",
    CO, "2026-02-26",
    model_impact="Passenger cars are built volume x price with a trend the company's own "
                 "three years establish; the other two unit lines have a level and no "
                 "trend, and the price is grown at a STATED rate which the ground-up "
                 "record marks as not measured against anything the company publishes.")

f_entrant = R.add(Ring.INDUSTRY, "new entrants (named-competitor level)", FindingClass.S,
    "Parallel imports of Chinese vehicles in Jordan and Iraq are named by the company as "
    "a live competitive pressure on its own volumes; GB Auto's own response is portfolio "
    "expansion -- Changan's first CKD SUV now among the top five in the Egyptian SUV "
    "segment, Li Auto and Deepal introduced in premium EV/REEV",
    "GB Corp 4Q/FY25 earnings release, passenger-car commentary", CO, "2026-02-26",
    model_impact="Caps the regional volume ladder: the growth rates decline across the "
                 "window rather than compounding at the FY2025 rate.")

f_tech = R.add(Ring.INDUSTRY, "technology substitution", FindingClass.S,
    "Electrification is arriving as a PORTFOLIO question rather than a demand shock: the "
    "group now addresses both mainstream and premium REEV/EV segments through Deepal and "
    "Li Auto, and in light mobility the Qute four-wheeler is gaining traction as an "
    "alternative to the Toktok, supported by government promotion initiatives",
    "GB Corp 4Q/FY25 earnings release, passenger-car and light-mobility commentary",
    CO, "2026-02-26",
    model_impact="Kept in the volume ladder rather than in the margin: the company "
                 "discloses no price or cost separately for these models, so a margin "
                 "claim would have nothing behind it.")

f_neg_comp = R.add(Ring.INDUSTRY, "competitor capacity / price moves (named)",
    FindingClass.NEG,
    "NEGATIVE SEARCH. No named competitor's capacity or price action is disclosed by GB "
    "Corp or retrievable for the Egyptian, Iraqi or Jordanian passenger-car markets at a "
    "company-by-company level: the company names the CATEGORY (parallel Chinese imports) "
    "and its own market share, and no listed Egyptian peer publishes vehicle volumes",
    "Searched: GB Corp's own FY2025 annual report and its four most recent earnings "
    "releases; no peer volume or price disclosure found", CO, SWEEP_DATE,
    model_impact="The relative lens is therefore struck on the company's OWN HISTORY "
                 "rather than on a peer set, which [R-LENS-03] permits and which this "
                 "absence is the reason for.")

# --------------------------------------------------------------- RING 4 COMPANY
f_guide = R.add(Ring.COMPANY, "strategic plans & guidance", FindingClass.S,
    "Management's forward statements in the period: capacity expansion at Ain Sokhna with "
    "an additional shift under consideration; gradual relief expected in regional "
    "operations in the second half of 2026; MNT-Halan's loan book at c.USD 1.95bn with "
    "growth in Turkey and Pakistan",
    "GB Corp 4Q/FY25 and 2Q/1H26 earnings releases", CO, "2026-08-13",
    model_impact="SCORED, NEVER CONSUMED [R-FCAL-01]. It is registered here so that the "
                 "one place this study DOES consume guidance is visible: the capital-"
                 "expenditure ladder rests on the company's investment plans, which that "
                 "rule forbids outright and which is recorded as outstanding with its "
                 "reason in REBUILD_PLAN_17-09-2026.md rather than repaired inside a "
                 "terminal construction that is itself retired.")

f_rel = R.add(Ring.COMPANY, "regular disclosures", FindingClass.D,
    "Three earnings releases carry the segment tables this model is built from: 4Q/FY25 "
    "(26 February 2026), 1Q26 and 2Q/1H26 (13 August 2026). Tables 6, 7, 8, 12 and 13 "
    "give working capital, net debt, the segment income statement, the segmented balance "
    "sheet and the GB Capital income statement",
    "GB Corp earnings releases, ir.gb-corporation.com/en/filings", CO, "2026-08-13",
    model_impact="The working-capital anchor, the net-debt bridge, the cost-of-debt "
                 "denominator, the minority's share and the lender leg's base all come "
                 "from these five tables and from nowhere else.",
    is_fs_data=True, fiscal_period="Q2-2026")

f_ir = R.add(Ring.COMPANY, "IR communications (calls, presentations, releases)",
    FindingClass.S,
    "The company publishes a standalone investor presentation alongside its quarterly "
    "release; the 1Q26 presentation is held in this study's own src/ directory and "
    "carries the segment and portfolio material the statements do not",
    "GB Corp Investor Presentation 1Q26 (GB_IRP_1Q26_-_Final.pdf), obtained from the "
    "company's own investor-relations filings page", IR, "2026-05-01",
    model_impact="Registered distinctly so a reviewer can see how much of the Company "
                 "ring rests on the investor-relations channel specifically, which is "
                 "what the 09-Aug-2026 amendment requires.")

f_round = R.add(Ring.COMPANY, "one-off base-resetting transactions", FindingClass.B,
    "Two of them, in the same period. (i) MNT Investment B.V. completed a strategic "
    "investment transaction with Al Ahly Capital Holding in June 2026. (ii) The "
    "associate's carrying value at 31 December 2025 was RESTATED upward by EGP 2,460,218 "
    "thousand -- 13,272,208 to 15,732,426 across the whole associates block",
    "GB Corp reviewed consolidated interim financial statements for the period ended 30 "
    "June 2026, note 34 (investment in associates), read by OCR off the rendered pixels "
    "because the filing carries no text layer", CO, "2026-08-13",
    model_impact="(i) is the upper branch's entire basis and (ii) is why the GB Capital "
                 "operating base must be struck restated-against-restated: netting the "
                 "restated associate against an unrestated segment equity halved the base "
                 "and doubled every return struck on it [audit finding 8].",
    is_fs_data=True, fiscal_period="Q2-2026")

f_stake = R.add(Ring.COMPANY, "ownership / stake changes (named-transaction rule)",
    FindingClass.B,
    "THE COMPANY DISCLOSES TWO PAIRS OF PERCENTAGES FOR THE SAME NAMED TRANSACTION AND "
    "THIS STUDY REGISTERS BOTH: its 9 June 2026 press release says GB Corp's stake in "
    "MNT-Halan 'will be adjusted to 41.61%, compared to 42.58% prior to the transaction'; "
    "note 34 to the reviewed statements says the stake in MNT BV 'will be decreased to "
    "42.93%, instead of 44.01% before the transaction'. Most likely a difference of LEVEL "
    "-- the Dutch holding vehicle against the operating group",
    "GB Corp press release 'MNT-Halan, a GB Corp Investee Company, Closes Capital Increase "
    "Round Led by Al Ahly Capital Holding' (9 June 2026) and note 34 to the reviewed "
    "30-June-2026 statements", CO, "2026-06-09",
    model_impact="41.61% is adopted because it is the figure the round it is applied to "
                 "was announced with; 42.93% is committed beside it rather than left out, "
                 "because a study registering one of two disclosed figures for one fact "
                 "has decided something silently.")

f_cap = R.add(Ring.COMPANY, "management & capital actions", FindingClass.D,
    "No capital action in the period: issued share capital is unchanged at EGP 1,085.5mn "
    "and the weighted average number of ordinary shares is 1,085,500 thousand in both "
    "FY2024 and FY2025. No employees' share of profit was taken in FY2025 against EGP "
    "76,549 thousand in FY2024, the board bonus running EGP 19,470 and 19,016 thousand",
    "GB Corp FY2025 audited consolidated financial statements, note 10 and the "
    "consolidated statement of financial position", CO, "2026-02-26",
    model_impact="The share count is a FILED figure at every date rather than a carried "
                 "one, and the earnings-per-share deduction is a contested judgement "
                 "carried both ways because the two disclosed years differ by a factor of "
                 "five and the employees' share follows the distribution.",
    is_fs_data=True, fiscal_period="FY2025")

f_fs = R.add(Ring.COMPANY, "official financial statements", FindingClass.D,
    "Audited consolidated financial statements for FY2023, FY2024 and FY2025, and "
    "REVIEWED consolidated interim statements at 31 March 2026 and 30 JUNE 2026. The "
    "30-June-2026 statements are the LATEST DISCLOSED BALANCE SHEET and the bridge stands "
    "on them. KPMG's limited review conclusion on them is QUALIFIED, on the associate: "
    "the reviewers 'were not provided with the consolidated financial statements for one "
    "of the associate companies (MNT - BV)' and were 'unable to verify the accuracy of "
    "the Group's share of profits from this investment', EGP 409,985 thousand",
    "GB Corp audited and reviewed consolidated financial statements, obtained from the "
    "company's own investor-relations filings page", CO, "2026-08-13",
    model_impact="Establishes what LATEST means for [R-BRIDGE-01], and the qualification "
                 "is the strongest single argument the study has for publishing the "
                 "associate on TWO bases rather than one.",
    is_fs_data=True, fiscal_period="FY2025")

f_fs24 = R.add(Ring.COMPANY, "official financial statements", FindingClass.D,
    "FY2024 comparatives as RECLASSIFIED in the FY2025 audited statements: profit "
    "attributable to the parent EGP 2,928,121 thousand, basic earnings per share 2.609, "
    "operating profit 5,820,840 thousand -- the last of which is the figure the delivered "
    "study's Appendix A.2 did not foot to [audit finding 6]",
    "GB Corp FY2025 audited consolidated financial statements, consolidated statement of "
    "profit or loss and note 10", CO, "2026-02-26",
    model_impact="The historical income statement a reader receives, and the denominator "
                 "of the FY2024 rung of the relative lens's own-history multiple.",
    is_fs_data=True, fiscal_period="FY2024")

f_fs23 = R.add(Ring.COMPANY, "official financial statements", FindingClass.D,
    "FY2023 audited: profit attributable to the parent EGP 1,890,727 thousand and basic "
    "earnings per share 1.682",
    "GB Corp FY2023 audited consolidated financial statements, as reproduced in the "
    "Annual Report 2023 (note 9)", CO, "2024-03-01",
    model_impact="The third rung of the relative lens's own-history multiple; three years "
                 "is what makes a median rather than a point.",
    is_fs_data=True, fiscal_period="FY2023")

f_q1 = R.add(Ring.COMPANY, "regular disclosures", FindingClass.D,
    "First-quarter 2026: GB Auto revenue EGP 17,505.7mn, gross profit 2,206.7mn, working "
    "capital 16,655.1mn and net debt 13,090.9mn at 31 March 2026",
    "GB Corp 1Q26 earnings release and the reviewed 31-March-2026 consolidated interim "
    "statements", CO, "2026-05-01",
    model_impact="Swept in BEFORE the build rather than discovered after; superseded as "
                 "the bridge date by the 30-June sheet, and kept as the quarter that "
                 "makes the 1H26 halves readable.",
    is_fs_data=True, fiscal_period="Q1-2026")

f_note26 = R.add(Ring.COMPANY, "official financial statements", FindingClass.D,
    "The debt book is NOT all local currency. Note 26: 'The average interest rate of the "
    "current EGP and USD loans & borrowings is amounted to 21.91% and 8.30% respectively "
    "during the year, the interest rate of EGP and USD 29.19% and 8.40% respectively "
    "during 2024.' Loans, borrowings and overdrafts EGP 37,921,342 thousand at 31 "
    "December 2025. THE BALANCES ARE NOT SPLIT BY CURRENCY ANYWHERE IN THE NOTE",
    "GB Corp FY2025 audited consolidated financial statements, note 26 (loans, borrowings "
    "and overdrafts)", CO, "2026-02-26",
    model_impact="The delivered edition asserted the book was entirely local-currency and "
                 "switched off a whole branch of the cost-of-debt test [audit finding 4]. "
                 "The currency split is now DERIVED by identity from these two rates and "
                 "the segment's own measured effective rate, and labelled derived.",
    is_fs_data=True, fiscal_period="FY2025")

f_neg_capex = R.add(Ring.COMPANY, "strategic plans & guidance", FindingClass.NEG,
    "NEGATIVE SEARCH. GB Corp publishes NO capital-expenditure figure, maintenance-capex "
    "disclosure or numeric investment plan in any earnings release or in the FY2025 "
    "annual report; the Ain Sokhna expansion and the additional shift are described "
    "without a cost. Searched: four earnings releases, the 1Q26 investor presentation and "
    "the FY2025 annual report including the cash-flow statement's investing section",
    "GB Corp earnings releases 4Q24-2Q26, Investor Presentation 1Q26, Annual Report 2025",
    CO, SWEEP_DATE,
    model_impact="This absence is why the capital-expenditure ladder is the study's "
                 "weakest driver and why [R-FCAL-01]'s guidance clause bites on it. It is "
                 "recorded rather than closed.")

f_neg_life = R.add(Ring.COMPANY, "official financial statements", FindingClass.NEG,
    "NEGATIVE SEARCH. No scalar or dominant-class useful life is disclosed. Note 42's "
    "depreciation policy gives RATE RANGES per asset class implying 3 to 50 years, and "
    "note 17 combines LAND -- which is not depreciated -- with buildings in one column, "
    "so the derived identity returns 10.9 to 17.1 years and contradicts the policy note's "
    "own bands. Both admissible routes were run and both failed",
    "GB Corp FY2025 audited consolidated financial statements, notes 17 and 42, as "
    "reproduced in the Annual Report 2025; recorded in full in useful_lives.json",
    CO, "2026-09-07",
    model_impact="engine/terminal_value.py REFUSES this name, so the sanctioned terminal "
                 "cannot be built and the study stays on the [R-TERM-01] ratchet with "
                 "this file named as the reason. STOP AND INFORM, SIGCM clause 8 -- not a "
                 "chosen life.")

# ------------------------------------------------------------ THE DRIVER GATE TABLE
R.add_driver("Passenger-car revenue (volume x price)", DriverMode.BOTTOM_UP,
    "Units and revenue are disclosed for three consecutive years, so both the level and "
    "the trend of the average selling price are observable rather than assumed.",
    [f_price, f_vol, f_rel])
R.add_driver("Commercial vehicles, light mobility and trading revenue", DriverMode.BOTTOM_UP,
    "Units and revenue are disclosed for ONE year on the two unit lines, so the level is "
    "observable and the trend is not; trading discloses revenue only and stops at the "
    "segment. The ground-up record carries the gap on each.",
    [f_price, f_vol])
R.add_driver("Other and inter-segment auto revenue", DriverMode.TOP_DOWN,
    "Neither a unit nor a segment is disclosed for it: EGP 682.8mn is the residual between "
    "GB Auto's external revenue and its four published lines, and EGP 444.8mn is the "
    "disclosed inter-segment line. Held FLAT rather than grown, because the company "
    "publishes no volume, price or growth rate for it.",
    [f_rel, f_neg_comp])
R.add_driver("Gross margin", DriverMode.BOTTOM_UP,
    "Held at the level the latest reviewed half filed, with the regional drag live and "
    "undated by the company. Margins are an OUTPUT of the disclosed cost structure and "
    "the disclosed price, not an input.",
    [f_region, f_rel, f_ckd])
R.add_driver("Working-capital intensity", DriverMode.BOTTOM_UP,
    "Anchored on the 30-June-2026 stock over trailing-twelve-month revenue on the "
    "company's own Table 6 and Table 8 definitions, and HELD FLAT: the stated drift "
    "mechanism has two halves and the conversion cycle measures them in opposite "
    "directions [R-ANCHOR-01].",
    [f_rel, f_q1])
R.add_driver("Cost of debt and the capital structure", DriverMode.BOTTOM_UP,
    "GB Auto's own segment finance cost over a quarter-weighted average of its own "
    "interest-bearing borrowings, on the book the release's own footnote says the charge "
    "is struck on; the currency split derived by identity from note 26's two disclosed "
    "rates because the balances are not split.",
    [f_note26, f_rel])
R.add_driver("Terminal growth and the terminal risk-free rate", DriverMode.BOTTOM_UP,
    "Both DERIVED from the house macro path rather than typed: terminal growth is the "
    "target-band inflation in force plus a stated real rate, and the terminal risk-free "
    "rate is that inflation plus the real-rate convention.",
    [f_cbe, f_rates])
R.add_driver("Capital expenditure", DriverMode.TOP_DOWN,
    "No capital-expenditure guidance, maintenance-capex disclosure or costed investment "
    "plan is published anywhere. The ladder rests on the company's described investment "
    "plans, which [R-FCAL-01] forbids as an INPUT, and that is registered as outstanding "
    "rather than repaired inside a retired terminal construction.",
    [f_neg_capex, f_neg_life])
R.add_driver("The associate (MNT-Halan)", DriverMode.BOTTOM_UP,
    "Published on TWO bases and never averaged: the reviewed carrying value, and the "
    "June-2026 round price. The stake percentages are the company's own, both pairs "
    "registered.",
    [f_round, f_stake, f_fs])
R.add_driver("The lender leg (GB Capital)", DriverMode.BOTTOM_UP,
    "The segment's own shareholders' equity before non-controlling interests LESS the "
    "associates carried inside it, both of them GB Corp's own figures at 30 June 2026, "
    "with the 31-December-2025 comparative struck restated-against-restated.",
    [f_rel, f_round])
R.add_driver("Earnings per share for the relative cross-check", DriverMode.BOTTOM_UP,
    "The company's OWN published basic figure on both sides of the multiple, after the "
    "employees' share of profit and the board bonus that note 10 deducts.",
    [f_fx, f_fs, f_fs24, f_fs23])

# ------------------------------------------------------------------------ OUTPUT
errors, warnings = R.validate()
R.to_json(os.path.join(HERE, 'sweep_register.json'))
print(R.qc_line())
print("\nfindings: %d | drivers: %d" % (len(R.findings), len(R.drivers)))
if errors:
    print("\nVALIDATOR ERRORS (%d) — NAMED, NOT SUPPRESSED:" % len(errors))
    for e in errors:
        print("  ! %s" % e)
if warnings:
    print("\nwarnings (%d):" % len(warnings))
    for w in warnings:
        print("  - %s" % w)
fr = R.check_freshness(SWEEP_DATE)
print("\nfreshness: %s" % (fr or "OK — sweep and delivery same day"))
if errors:
    raise SystemExit(1)
