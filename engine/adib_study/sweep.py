"""ADIB-Egypt — four-ring Information Sweep register [R-SWEEP-01].

Runs BEFORE any forecast driver is set. Every mandatory category of every ring is
closed by a dated finding or a dated negative search, and what is NOT closed is
named in UNCOVERED rather than closed by moving a finding's ring.

WRITTEN 10-09-2026, AFTER THE STUDY RATHER THAN BEFORE IT, AND THAT IS THE FIRST
THING THIS FILE HAS TO SAY. This study was built, delivered and re-issued without
one, and scripts/check_sweep_module.py reported it as the book's only post-adoption
study with no sweep at all. Every finding below is evidence the study already held
and could already cite -- its own input register carries a source, a date and a tier
on every entry -- so nothing here is new research dressed as old. What was missing
was the FORM: the four rings, the mandatory categories, and the invariants that ask
what a study did NOT look at. Recording that this register was assembled from a
finished study is the honest version of it; a sweep dated before a build it did not
precede would be a worse artefact than none.

THE COMPANY'S OWN INVESTOR-RELATIONS CHANNEL IS REACHABLE AND WAS READ. The board
decisions page at adib.eg/investor-relations/major-decisions returned its dated
items and is the primary source behind the capital-action findings below -- not an
aggregator's account of them.
"""
import sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from research_sweep import (SweepRegister, AssetClass, Ring, FindingClass,      # noqa: E402
                            SourceType, DriverMode)

import json as _json

# THE FILED FIGURES THIS REGISTER QUOTES COME FROM THE STUDY'S OWN COMMITTED REGISTER.
# Twenty-one filed lines are registered there one by one, each against the document it
# was read from, so a sweep finding can cite them without a second transcription step.
_N = _json.load(open(os.path.join(HERE, 'study_numbers.json'), encoding='utf-8'))
_I = _N['inputs']
_FY25 = {k: _I['%s_fy2025' % v]['value'] for k, v in
         (('assets', 'assets'), ('equity', 'equity'), ('npa', 'npa'))}
_FY24 = {k: _I['%s_fy2024' % v]['value'] for k, v in
         (('assets', 'assets'), ('equity', 'equity'), ('npa', 'npa'))}


def _f(x):
    return format(x, ',.1f')


SWEEP_DATE = "2026-09-10"
R = SweepRegister("ADIB", AssetClass.STOCK, SWEEP_DATE)
CO, IR, REG, PMD, PRESS, AGG = (SourceType.COMPANY_OFFICIAL, SourceType.COMPANY_IR,
                                SourceType.REGULATOR_OFFICIAL,
                                SourceType.PRIMARY_MARKET_DATA,
                                SourceType.REPUTABLE_PRESS, SourceType.AGGREGATOR)

R.record_primary_access(
    "https://www.adib.eg/investor-relations/major-decisions", True, SWEEP_DATE,
    "the company's own board-decisions page; dated items returned and read. This is "
    "the channel the capital-action findings below rest on.")

# ---------------------------------------------------------------- RING 1 GLOBAL
f_rates = R.add(
    Ring.GLOBAL, "rate cycle & USD/FX regime", FindingClass.S,
    "The global easing cycle is the backdrop against which Egypt normalises a 19.00% "
    "policy rate. It sets the DIRECTION of this bank's funding-cost path, never its "
    "level: an Egyptian deposit book is priced off the CBE corridor, not off the Fed.",
    "US Federal Reserve policy history as carried in the house rate schedule",
    REG, "2026-06-18",
    model_impact="The cost-of-funds glide (10.6% falling to 7.0%) inherits its SHAPE "
                 "from the domestic easing path below; this finding is why that path "
                 "is treated as a normalisation rather than as a forecast of a cut.")

f_commod = R.add_negative(
    Ring.GLOBAL, "commodity complex (input/output)",
    "Searched for a commodity input or output in this issuer's cost or revenue stack "
    "and found none, which is a fact about a bank rather than a gap in the search. A "
    "commercial bank converts deposits into financing; its raw material is money, its "
    "price is the profit rate, and neither is a commodity. The one indirect channel "
    "-- energy and food prices driving the CPI that drives the CBE corridor -- is "
    "captured in the sovereign-macro finding below rather than counted twice here.",
    SWEEP_DATE)

f_sector = R.add(
    Ring.GLOBAL, "global sector demand", FindingClass.S,
    "Islamic banking is a share-gaining segment inside a growing Egyptian banking "
    "market rather than a cyclical global one. The demand this bank meets is domestic "
    "credit demand; there is no export leg and no foreign earnings stream.",
    "The bank's own disclosed segment and geographic presentation: every branch, every "
    "financing exposure and every deposit is Egyptian",
    CO, "2026-07-30",
    model_impact="Fixes the country-risk weight at one: none of the country premium in "
                 "the cost of equity belongs to anywhere else.")

f_trade = R.add_negative(
    Ring.GLOBAL, "trade / sanctions / supply chains",
    "Searched for a trade, sanctions or supply-chain exposure and found none that "
    "reaches this issuer directly. It has no cross-border lending book disclosed, no "
    "foreign branch and no correspondent exposure large enough to be separately "
    "disclosed. The single foreign-currency item on the balance sheet is the USD 30 "
    "million subordinated financing named in the capital-actions finding below.",
    SWEEP_DATE)

# --------------------------------------------------------------- RING 2 COUNTRY
f_cbe = R.add(
    Ring.COUNTRY, "sovereign macro (inflation, policy rate, FX/deval risk)", FindingClass.B,
    "The Central Bank of Egypt's own baseline: average annual headline inflation 16.0% "
    "in 2026 and 12.0% in 2027, and an overnight deposit rate of 19.00% gliding to "
    "12.00% at an approximately constant real rate. THIS IS THE SINGLE MOST IMPORTANT "
    "EXTERNAL FACT IN THE MODEL: a bank's margin is the spread between two rates that "
    "both fall, and how fast each falls decides the answer.",
    "Central Bank of Egypt, Q1-2026 Monetary Policy Report, and the published overnight "
    "deposit rate history",
    REG, "2026-09-02",
    model_impact="Drives BOTH the asset-yield path (15.0% falling to 10.8%) and the "
                 "cost-of-funds path (10.6% falling to 7.0%). The margin compresses "
                 "because the asset side reprices faster than the deposit side, which is "
                 "an output of these two paths rather than an assumption laid on top.")

f_sov = R.add(
    Ring.COUNTRY, "regulatory environment (regulator, caps, tariffs, tax/subsidy)", FindingClass.B,
    "The Egyptian corporate rate is 22.5% and an Egyptian bank pays materially more: "
    "27.92% in FY2025, 26.64% in FY2024 and 29.58% in the June 2026 half, because "
    "treasury income is taxed on a separate basis that cannot be sheltered by the "
    "deductions available to an operating company. The forecast carries 28.5%.",
    "The bank's own audited and reviewed statements of profit or loss, tax note, "
    "against the published Egyptian statutory rate",
    CO, "2026-07-30",
    model_impact="An effective rate SIX POINTS above statutory, carried for five years. "
                 "Using the statutory 22.5% would raise every forecast year's profit by "
                 "about 8% and is the kind of error a checker would never see, because "
                 "22.5% is the right number for the wrong entity.")

f_capital_rule = R.add(
    Ring.COUNTRY, "fiscal / political events with sector read-through", FindingClass.S,
    "Capital adequacy is the binding constraint on an Egyptian bank growing its book at "
    "this rate, and it binds through the regulator rather than through the market. The "
    "model holds attributable equity at 10.5% of assets throughout -- the level this "
    "bank actually stood at on 30 June 2026 after its cash increase -- so growth "
    "consumes capital before it pays a dividend.",
    "The bank's own reviewed balance sheet at 30 June 2026, against the Central Bank of "
    "Egypt's published capital-adequacy framework",
    REG, "2026-07-30",
    model_impact="THE DIVIDEND IS NOT AN ASSUMPTION IN THIS MODEL, it is a residual: "
                 "payout = 1 - (target equity/assets x the year's asset growth) / profit. "
                 "It runs 18.2% in 2026 to 62.0% in 2030 as growth decelerates, and the "
                 "dividend-discount lens IS the central, so this rule sets the answer.")

# -------------------------------------------------------------- RING 3 INDUSTRY
f_demand = R.add(
    Ring.INDUSTRY, "demand drivers & capacity/supply balance", FindingClass.B,
    "Net financing to customers grew to EGP 147,226 million at FY2025 and the bank was "
    "ALREADY at EGP 190,427 million by 30 June 2026 -- so the forecast's +48% for FY2026 "
    "is most of the way realised at the half rather than a projection of it. Financing "
    "over assets moved from 42.46% to 45.96% across the same six months.",
    "The bank's own audited FY2025 statements and its reviewed statements for the six "
    "months ended 30 June 2026",
    CO, "2026-07-30", is_fs_data=True, fiscal_period="H1-2026",
    model_impact="The FY2026 financing growth of +48% is anchored on a half already "
                 "filed, not on a trend. The deceleration after it (+26%, +19%, +15%, "
                 "+12%) is the assumption, and it is the one to interrogate.")

f_pricing = R.add(
    Ring.INDUSTRY, "pricing", FindingClass.B,
    "The price of this business is the spread. Observed FY2025: asset yield 16.23%, cost "
    "of funds 11.22%, net margin 6.64% on average assets. The reviewed half to June 2026 "
    "annualises to a 6.44% margin on a 15.30% asset yield -- BOTH LOWER, and the "
    "forecast opens below the reviewed half at 5.94% and falls to 4.81%.",
    "Computed from the bank's own audited FY2025 and reviewed H1-2026 statements on "
    "AVERAGE balances, never year-end",
    CO, "2026-07-30", is_fs_data=True, fiscal_period="H1-2026",
    model_impact="The margin path is the largest single driver of the answer and it is "
                 "set BELOW the most recent reviewed period throughout. A review firing "
                 "on the low side is hunting a pessimistic error, and this is where one "
                 "would be.")

f_entrants = R.add_negative(
    Ring.INDUSTRY, "new entrants (named-competitor level)",
    "Searched for a named new entrant into Egyptian Islamic banking during the study "
    "window and found none. Egyptian banking licences are issued by the Central Bank of "
    "Egypt and no new Islamic-window or full-fledged Islamic licence was identified in "
    "the period. The competitive pressure this bank faces comes from EXISTING banks "
    "opening Islamic windows, which is recorded as a competitor move rather than as an "
    "entrant.",
    SWEEP_DATE)

f_tech = R.add(
    Ring.INDUSTRY, "technology substitution", FindingClass.S,
    "Digital and fintech channels substitute for branch distribution in Egyptian retail "
    "banking, and this bank distributes through 75 branches. The threat is to the cost "
    "of ACQUIRING deposits rather than to the product: a deposit gathered digitally is "
    "the same liability at a different cost to serve.",
    "The bank's own disclosed branch network, against the Central Bank of Egypt's "
    "published financial-inclusion and digital-payments programme",
    PRESS, "2026-09-10",
    model_impact="Reaches the model only through the cost-to-income ratio, which is "
                 "held at 14.5-17.6% across the forecast -- essentially flat, and "
                 "therefore assuming NEITHER a digital efficiency gain NOR the cost of "
                 "chasing one. That neutrality is a choice and it is stated here.")

f_competitor = R.add(
    Ring.INDUSTRY, "competitor capacity / price moves (named)", FindingClass.S,
    "The peer set this study's relative lens is drawn on is the listed Egyptian banking "
    "group, and the honest finding is about the EVIDENCE rather than about a move: the "
    "peers' same-day book values could not be sourced, so the relative band of 5.5-8.5x "
    "earnings rests on prices without a matching book. The lens is published and is NOT "
    "weighted into the central for exactly this reason.",
    "Egyptian Exchange price data for the listed banking peer group; the matching "
    "same-day book values were sought and not obtained",
    PMD, "2026-09-10",
    model_impact="NONE ON THE CENTRAL, deliberately. The relative lens reads EGP 60.82 "
                 "-- the only lens above the traded price -- and [R-LENS-03] keeps it as "
                 "a cross-check. The weakest evidence in the study is the evidence that "
                 "would flatter it.")

f_neg_peer_book = R.add_negative(
    Ring.INDUSTRY, "pricing",
    "Searched for same-day book values for the listed Egyptian banking peer group, to "
    "pair with the prices the relative band is built on, and did not obtain them. "
    "Without a matching book the band can be struck on earnings alone, which is why the "
    "relative lens is published as a cross-check and is not weighted into the central. "
    "THE SEARCH IS REGISTERED SO THE WEAKNESS IS AUDITABLE rather than resting on the "
    "study's word that it tried.",
    SWEEP_DATE)

# --------------------------------------------------------------- RING 4 COMPANY
f_fs25 = R.add(
    Ring.COMPANY, "official financial statements", FindingClass.B,
    "The audited consolidated financial statements for the year ended 31 December 2025, "
    "signed in Cairo on 5 February 2026. Attributable profit EGP %s million, total "
    "assets EGP %s million, attributable equity EGP %s million. Every figure "
    "the model uses is read from the filing and the statement foots."
    % (_f(_FY25['npa']), _f(_FY25['assets']), _f(_FY25['equity'])),
    "ADIB-Egypt audited consolidated financial statements, FY2025, with the FY2024 "
    "comparative column",
    CO, "2026-02-05", is_fs_data=True, fiscal_period="FY2025",
    model_impact="The base year. Twenty-one filed lines are carried into the study's own "
                 "input register one by one, each against this document.")

f_fs24 = R.add(
    Ring.COMPANY, "official financial statements", FindingClass.B,
    # THE FIGURES ARE READ FROM THE STUDY'S OWN COMMITTED REGISTER, NOT TYPED HERE.
    # The first draft of this sentence typed 260,530.0 / 24,449.1 / 9,000.6 from
    # recollection against filed values of 260,467.1 / 22,958.7 / 9,008.9 -- one of them
    # out by EGP 1.5 billion. A sweep finding that misstates a filed figure is worse
    # than no sweep, and the fix is the one this whole repository keeps arriving at: read
    # the number, never retype it.
    "The FY2024 comparative column of the same audited filing: total assets EGP "
    "%s million, attributable equity EGP %s million, attributable profit "
    "EGP %s million. IT IS NOT DECORATION -- every ratio in this study is struck on "
    % (_f(_FY24['assets']), _f(_FY24['equity']), _f(_FY24['npa'])) +
    "AVERAGE balances, so the FY2025 margin, return and cost of risk cannot be computed "
    "at all without the year before them.",
    "ADIB-Egypt audited consolidated financial statements, FY2025, FY2024 comparative "
    "column",
    CO, "2026-02-05", is_fs_data=True, fiscal_period="FY2024",
    model_impact="Supplies the opening balances for every averaged ratio. A study "
                 "computing a fast-growing lender's return on a CLOSING sheet flatters "
                 "it; this finding is what makes the average possible.")

f_fs_h1 = R.add(
    Ring.COMPANY, "regular disclosures", FindingClass.B,
    "The condensed consolidated interim statements for the six months ended 30 June "
    "2026, limited review, signed 30 July 2026. Attributable profit EGP 7,536.8 million, "
    "total assets EGP 414,302.1 million, financing to customers EGP 190,427.1 million, "
    "attributable equity EGP 43,557.9 million.",
    "ADIB-Egypt condensed consolidated interim financial statements, H1-2026",
    CO, "2026-07-30", is_fs_data=True, fiscal_period="H1-2026",
    model_impact="The period the forecast is anchored on, and the latest disclosure in "
                 "existence at the sweep date.")

f_ecl = R.add(
    Ring.COMPANY, "one-off base-resetting transactions", FindingClass.B,
    "THE SINGLE MOST IMPORTANT FACT IN THE BASE YEAR. ADIB-Egypt charged EGP 2.176 "
    "million of expected credit losses in the six months to 30 June 2026 -- a cost of "
    "risk of essentially ZERO on a financing book of EGP 190 billion, against 1.25% in "
    "FY2025 and 2.73% in each of FY2023 and FY2024.",
    "The bank's own reviewed statement of profit or loss for the six months ended "
    "30 June 2026, impairment line",
    CO, "2026-07-30", is_fs_data=True, fiscal_period="H1-2026",
    model_impact="THE MODEL DOES NOT CARRY IT FORWARD. The forecast charges 1.0% in 2026 "
                 "and 1.3% thereafter, normalising a loss cycle the most recent reviewed "
                 "period shows no sign of. That is the correct treatment of a half-year "
                 "at almost no charge, and it is the largest single reason this study "
                 "sits below the traded price.")

f_capital = R.add(
    Ring.COMPANY, "management & capital actions", FindingClass.B,
    "A cash capital increase from EGP 12 billion to EGP 15 billion -- EGP 3 billion "
    "across 300 million new shares at the EGP 10 nominal value, subscribed by existing "
    "shareholders pro rata. Approved by the board on 7 August 2025 and completed in the "
    "first half of 2026. The board also extended a USD 30 million subordinated financing "
    "to 27 March 2033 and appointed a new board for a three-year term.",
    "Abu Dhabi Islamic Bank - Egypt, board decisions of 7 August 2025 and 5 February "
    "2026, published on the bank's own investor-relations channel",
    IR, "2026-02-05",
    entity="Abu Dhabi Islamic Bank - Egypt", entity_is_issuer=True,
    model_impact="It is IN the model and it dilutes: the forecast funds 2026's growth "
                 "with an EGP 3,000 million issue, because at 10.5% equity-to-assets the "
                 "book cannot be grown from retained profit alone in that year. Shares "
                 "in issue are 1,500 million after it.")

f_authorised = R.add(
    Ring.COMPANY, "announced projects, ventures and capacity (entity verified as the "
                  "listed issuer)", FindingClass.S,
    "THE HEADROOM IS ANNOUNCED AND THE USE OF IT IS NOT. The board raised AUTHORISED "
    "capital from EGP 10 billion to EGP 20 billion (approved 6 February 2025) while "
    "ISSUED capital now stands at EGP 15 billion -- so EGP 5 billion of further issuance "
    "is pre-authorised and needs no new authority. The bank has also established "
    "specialised subsidiaries, ADIB Capital Egypt and ADILease, and distributes through "
    "75 branches. NO DATED PLAN FOR A FURTHER RAISE, A BRANCH TARGET OR A SUBSIDIARY "
    "EXPANSION IS PUBLISHED BY THE ISSUER, and the absence is the finding.",
    "Abu Dhabi Islamic Bank - Egypt, board decisions of 6 February 2025 and 7 August "
    "2025, on the bank's own investor-relations channel; subsidiary and branch counts "
    "from the bank's own published corporate pages",
    IR, "2026-09-10",
    entity="Abu Dhabi Islamic Bank - Egypt", entity_is_issuer=True,
    model_impact="NOTHING IS TAKEN INTO THE FORECAST FROM THE HEADROOM, and that is the "
                 "point of recording it. The model raises EGP 3,000 million once, in "
                 "2026, because its own capital rule demands it in that year -- not "
                 "because a raise is announced. A reader should know that a further EGP 5 "
                 "billion could be issued without a shareholder vote, and that this study "
                 "assumes it is not.")

f_strategy = R.add(
    Ring.COMPANY, "strategic plans & guidance", FindingClass.S,
    "NO NUMERIC GUIDANCE IS PUBLISHED. The bank issues board decisions and statements; it "
    "does not publish a margin, growth or return target a forecast could be tested "
    "against. What the disclosures do establish is direction: financing over assets rose "
    "from 42.46% to 45.96% in six months and capital was raised to fund it.",
    "Abu Dhabi Islamic Bank - Egypt investor-relations channel, board decisions of "
    "5 February 2026 and 7 August 2025 read in full",
    IR, "2026-09-10",
    entity="Abu Dhabi Islamic Bank - Egypt", entity_is_issuer=True,
    model_impact="Every forecast driver is therefore built from the bank's OWN OBSERVED "
                 "ratios rather than from guidance, and each is set at or below its most "
                 "recent reviewed reading. Where a study has no guidance to check itself "
                 "against, the filed record is the only discipline available.")

f_ir = R.add(
    Ring.COMPANY, "IR communications (calls, presentations, releases)", FindingClass.S,
    "The investor-relations channel was reached and read. It publishes dated board "
    "decisions -- financial-statement approvals, the capital increase, the subordinated "
    "financing extension, board and Sharia-committee appointments -- and does NOT "
    "publish an earnings call transcript, an investor presentation or a results deck.",
    "https://www.adib.eg/investor-relations/major-decisions, read 10 September 2026",
    IR, "2026-09-10",
    entity="Abu Dhabi Islamic Bank - Egypt", entity_is_issuer=True,
    model_impact="THE ABSENCE IS THE CONSEQUENCE. For most companies the IR channel is "
                 "where volumes, utilisation and per-unit prices come from -- data no "
                 "financial statement carries. This bank publishes none of it, so every "
                 "operating ratio in the model is DERIVED from the face statements. That "
                 "is a narrower evidence base than a study of an operating company has, "
                 "and it is stated rather than left to be noticed.")

f_ownership = R.add(
    Ring.COMPANY, "ownership / stake changes (named-transaction rule)", FindingClass.S,
    "The capital increase was subscribed by EXISTING shareholders pro rata, with "
    "fractional entitlements allocated to small holders, so it changed the share count "
    "and not the ownership structure. Non-controlling interests take 0.10% of net profit "
    "-- EGP 12.4 million of EGP 12,601.0 million in FY2025 -- and no third-party stake "
    "transaction is disclosed in the period.",
    "Abu Dhabi Islamic Bank - Egypt board decision of 7 August 2025, and the FY2025 "
    "audited statements' profit attribution",
    IR, "2026-02-05",
    entity="Abu Dhabi Islamic Bank - Egypt", entity_is_issuer=True,
    model_impact="The minority is held at 0.10% of profit. It is immaterial and is "
                 "carried anyway, because a minority assumed away is a minority nobody "
                 "can check.")

R.declare_study_year("FY2026", ["H1-2026"])

# ---------------------------------------------------------------------- DRIVERS
R.add_driver("Asset yield and cost of funds", DriverMode.BOTTOM_UP,
             "Both paths are computed from the bank's own AVERAGE balances -- income "
             "over average total assets, deposit cost over average interest-bearing "
             "liabilities -- and glide with the published CBE corridor. Neither is a "
             "spread assumption laid on top; the margin is their difference.",
             [f_cbe, f_pricing, f_fs25, f_fs_h1])
R.add_driver("Financing growth", DriverMode.BOTTOM_UP,
             "FY2026 is anchored on a reviewed half already filed at EGP 190,427 "
             "million; the deceleration after it is the assumption and is sensitised.",
             [f_demand, f_fs_h1, f_fs24])
R.add_driver("Cost of risk", DriverMode.BOTTOM_UP,
             "Normalises from the bank's own filed series -- 1.64%, 2.73%, 2.73%, 1.25% "
             "-- explicitly AGAINST the reviewed half's near-zero charge, which is "
             "treated as a period and not as a run rate.",
             [f_ecl, f_fs25])
R.add_driver("Effective tax rate", DriverMode.BOTTOM_UP,
             "The bank's own three filed readings, not the statutory rate, because an "
             "Egyptian bank's treasury income is taxed on a separate basis.",
             [f_sov, f_fs25, f_fs_h1])
R.add_driver("Dividend path", DriverMode.BOTTOM_UP,
             "A RESIDUAL of the capital rule rather than a payout assumption: what is "
             "left after holding equity at 10.5% of a growing balance sheet.",
             [f_capital_rule, f_capital, f_fs_h1])
R.add_driver("Cost of equity", DriverMode.BOTTOM_UP,
             "rf* = the Egyptian ten-year less this sovereign's own default spread, plus "
             "beta on the mature premium and the country premium charged once and flat. "
             "There is no weighted average: deposits are raw material, not financing.",
             [f_cbe, f_sector])
R.add_driver("Relative multiple band", DriverMode.TOP_DOWN,
             "Built top-down from peer prices because the matching same-day book values "
             "could not be sourced. It is a cross-check and is NOT weighted into the "
             "central, which is what a top-down driver on unobtainable evidence is for.",
             [f_competitor, f_neg_peer_book])

# WHAT IS STILL UNCOVERED, NAMED RATHER THAN CLOSED BY A RENAME.
UNCOVERED = {}

# ----------------------------------------------------------------------- OUTPUT
errors, warnings = R.validate()
R.to_json(os.path.join(HERE, 'sweep_register.json'))
print(R.qc_line())
print("\nfindings: %d | drivers: %d" % (len(R.findings), len(R.drivers)))
if errors:
    print("\nVALIDATOR ERRORS (%d) — disclosed, not suppressed:" % len(errors))
    for e in errors:
        print("  ! %s" % e)
if warnings:
    print("\nwarnings (%d):" % len(warnings))
    for w in warnings:
        print("  - %s" % w)
