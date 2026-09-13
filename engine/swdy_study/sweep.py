"""SWDY — four-ring Step 2A Information Sweep register.

THIS STUDY HAD NO SWEEP REGISTER. It had the sweep: 220 four-field inputs, each with a
named source and a date, a bibliography of primary documents, a set of dated negative
searches and an explicit account of which drivers are built bottom-up and which are not.
What it did not have was that record in the form research_sweep.py enforces — so the
invariants nobody had checked were: that every mandatory category of every ring is closed
by a finding OR a dated negative search; that a financial-statement line is sourced from
the company itself; that every driver cites the finding that unlocked it or the negative
search that forced it top-down; that the company's own IR channel was attempted and
logged either way; that the study year's already-disclosed quarters are swept in BEFORE
the build rather than discovered after.

RECONSTRUCTED FROM THE STUDY'S OWN COMMITTED RECORD, NOT FROM RECOLLECTION. Every finding
below carries the source name and date the input register already holds for it; the
negative searches are the ones the delivered bibliography already publishes. Where the
record does not answer an invariant, the entry says so and the validator is left to fire.

Sweep dates run 05-Aug-2026 (the first pass) to 10-Sep-2026 (the last research pass);
each finding carries its own source date rather than the sweep's.
"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from research_sweep import (SweepRegister, AssetClass, Ring, FindingClass,
                            SourceType, DriverMode)

SWEEP_DATE = "2026-09-10"
R = SweepRegister("SWDY", AssetClass.STOCK, SWEEP_DATE)
CO, IR, REG, PMD, PRESS, AGG = (SourceType.COMPANY_OFFICIAL, SourceType.COMPANY_IR,
                                SourceType.REGULATOR_OFFICIAL, SourceType.PRIMARY_MARKET_DATA,
                                SourceType.REPUTABLE_PRESS, SourceType.AGGREGATOR)

FY25 = "Audited FY2025 consolidated financial statements (issued 15 March 2026)"
FY24 = "Audited FY2024 consolidated financial statements (issued 13 March 2025)"
FY23 = "Audited FY2023 consolidated financial statements (issued 13 March 2024)"
Q126 = "Q1-2026 condensed consolidated interim financial statements (reviewed, 13 May 2026)"
H126 = "H1-2026 condensed consolidated interim financial statements (reviewed, 11 August 2026)"

# ---------------------------------------------------------------- RING 1 GLOBAL
f_rates = R.add(Ring.GLOBAL, "rate cycle & USD/FX regime", FindingClass.S,
    "Global easing is under way and the US dollar risk-free rate is the reference the "
    "hard-currency alternative construction discounts at. The study carries a USD "
    "risk-free rate as a registered input and builds the whole currency-of-discounting "
    "alternative on it",
    "House cost-of-capital reference, USD risk-free reading", REG, "2026-08-05",
    model_impact="Sets the hard-currency alternative cost of capital, the study's second "
                 "published construction of the discount rate and its largest single "
                 "unresolved judgement.")

f_copper = R.add(Ring.GLOBAL, "commodity complex (input/output)", FindingClass.S,
    "Copper is the dominant input of the largest segment. The forecast holds it near the "
    "current market level rather than taking a directional view, and carries the view in "
    "the sensitivity instead: a plus or minus 15% move is worth EGP 8.73 a share",
    "London Metal Exchange copper price history and forward curve", PMD, "2026-08-05",
    model_impact="Drives Cables revenue through the measured pass-through, and drives "
                 "working capital with it. Carried in the one-way sensitivity, not "
                 "forecast directionally.")

f_gdem = R.add(Ring.GLOBAL, "global sector demand", FindingClass.C,
    "Cable and turnkey engineering demand reaches this issuer through Gulf, African and "
    "European project markets rather than a world price: the company's own Q2-2026 "
    "release puts 79% of group sales outside Egypt or from exports, 84% in wires and "
    "cables and 67% in engineering and construction, each up nine points on the quarter",
    "Company Q2-2026 earnings release and results presentation", IR, "2026-08-12",
    model_impact="Establishes the DIRECTION and a ceiling for the hard-currency share of "
                 "revenue. It does NOT set the weights, because the published measure "
                 "counts exports out of Egypt as well as sales booked abroad while the "
                 "weights are about currency of invoicing; the study's 65% and 30% are on "
                 "the conservative side of it and are not raised on this finding.")

f_neg_trade = R.add_negative(Ring.GLOBAL, "trade / sanctions / supply chains",
    "Tariff, sanctions, anti-dumping or export-licence exposure naming this issuer or "
    "Egyptian cable exports specifically — searched across the four audited filings, the "
    "interim statements and the company's own releases. Nothing disclosed and nothing "
    "found; no such exposure is modelled and none is assumed away", SWEEP_DATE)

# --------------------------------------------------------------- RING 2 COUNTRY
# A PUBLISHED CENTRAL-BANK TARGET AND A PUBLISHED BOND YIELD ARE DISCLOSURES, not
# situations. Classed D, because the gate rule is right to ask what a bottom-up driver
# was unlocked BY, and "the macro environment" is not an answer.
f_macro = R.add(Ring.COUNTRY, "sovereign macro (inflation, policy rate, FX/deval risk)",
    FindingClass.D,
    "Egypt's disinflation path and the pound are the two quantities this valuation is "
    "most exposed to. The study takes its terminal inflation and real-rate convention "
    "from the house macro path rather than typing a nominal rate, so the terminal growth "
    "and the terminal discount rate are built on the SAME inflation",
    "House macro profile for Egypt (terminal inflation, real-rate convention) and the "
    "Egypt 10-year local-currency government bond yield",
    REG, "2026-07-21",
    detail="Readings of the 10-year yield on the anchor date span roughly 22.3% to 23.0% "
           "across sources and disagree with each other; the adopted point sits at the "
           "low end and the rate is carried in the sensitivity grid because of it.",
    model_impact="Sets rf, rf_term, the terminal growth rate and the whole cost-of-capital "
                 "glide. The largest single lever in the study.")

f_ccy = R.add(Ring.COUNTRY, "sovereign macro (inflation, policy rate, FX/deval risk)",
    FindingClass.S,
    "The pound path: about 6% a year of depreciation, far below what the interest-rate "
    "differential implies, on the assumption that the disinflation path closes most of "
    "the gap rather than the currency absorbing it",
    "House EGP/USD path; the exchange rate on the anchor date", PMD, "2026-08-05",
    model_impact="Translates the hard-currency share of revenue and of the debt book. "
                 "Section 1.9's currency row swings EGP 23.27 a share across ±15%.")

f_tax = R.add(Ring.COUNTRY, "regulatory environment (regulator, caps, tariffs, tax/subsidy)",
    FindingClass.D,
    "Egypt's statutory corporate income tax rate is 22.5%. The company's audited effective "
    "rates ran 31.3% (FY2023), 30.1% (FY2024) and 22.6% (FY2025), and 25.75% on the "
    "Q1-2026 print; no statutory-to-effective reconciliation is disclosed in any filing",
    "PwC Worldwide Tax Summaries — Egypt, and the audited statements' own tax notes",
    REG, "2026-05-13",
    model_impact="Sets the forecast effective tax rate and the after-tax cost of debt. The "
                 "absence of a reconciliation is why the rate is carried in the "
                 "sensitivity rather than assumed to converge on the statutory rate.")

f_emp = R.add(Ring.COUNTRY, "regulatory environment (regulator, caps, tariffs, tax/subsidy)",
    FindingClass.D,
    "Egyptian company law gives employees a statutory share of distributable profits, "
    "capped at total annual wages. It is disclosed only in the earnings-per-share note, "
    "below the attributable line, and appears in no line of the income statement",
    FY25 + ", note 39 and the wage-bill notes", CO, "2026-03-15", is_fs_data=True,
    fiscal_period="FY2025",
    model_impact="Charged in the equity bridge at the mean of FY2024, FY2025 and H1-2026. "
                 "The cap does not bind: wages of EGP 18,906mn against a share of EGP "
                 "2,073mn is 9.1x of headroom, computed from three notes of the same "
                 "statements, so the charge is the measured one and not an upper bound.")

f_fiscal = R.add(Ring.COUNTRY, "fiscal / political events with sector read-through",
    FindingClass.S,
    "Egypt's country risk is charged as a premium beside beta rather than through it: the "
    "hard-currency CDS spread is netted out of the local risk-free rate and re-enters, "
    "volatility-scaled, inside the equity risk premium. The net country charge through "
    "the equity channel is about +1.9pp",
    "Published country-premium file, Egypt row, January-2026 vintage, CDS and rating bases",
    REG, "2026-01-05",
    model_impact="Sets the explicit-window cost of equity. The un-netted construction is "
                 "retired and retained in the audit trail; the rating-basis column is "
                 "published as the disclosed alternative.")

f_neg_taxrec = R.add_negative(Ring.COUNTRY,
    "regulatory environment (regulator, caps, tariffs, tax/subsidy)",
    "A statutory-to-effective tax reconciliation in any of the four audited filings or "
    "the two interims — the note that would show which of deferred tax, non-deductible "
    "items, withholding on foreign operations or associate income drives the 31.3% / "
    "30.1% / 22.6% effective-rate path. Not disclosed in any of them. This is why the "
    "effective rate is set top-down between the statutory rate and the audited history "
    "and carried in the sensitivity, rather than built from its components", SWEEP_DATE)

# -------------------------------------------------------------- RING 3 INDUSTRY
f_demand = R.add(Ring.INDUSTRY, "demand drivers & capacity/supply balance", FindingClass.S,
    "Engineering and construction backlog: EGP 196bn at Dec-2024, 293bn at Dec-2025 and "
    "346bn at 30 June 2026 — THE THREE POINTS THIS STUDY CAN DATE. Four intermediate "
    "readings (261, 276, 307) were carried in an earlier edition of this entry inside the "
    "same comma-separated run as the dated ones, which reads as a quarterly series and is "
    "not one: they are undated here and cannot be placed against a quarter from anything "
    "this study holds, and an external review read the run as mis-sequenced, correctly. "
    "They are withdrawn from the series rather than given dates they do not have. Wires "
    "and cables 43.5bn and meters 8.8bn are disclosed beside the total. The dated "
    "endpoints give +18% over the reviewed half against the +27.4% revenue growth the "
    "Constructions driver is anchored on, which is the comparison the entry exists for "
    "and which the withdrawn points do not affect",
    "Company Q2-2026 earnings release, backlog disclosure", IR, "2026-08-12",
    model_impact="CORROBORATES the Constructions taper without being burnt down to produce "
                 "it — the releases disclose no burn profile, so the taper stays a taper on "
                 "the segment's own revenue record rather than becoming a burn rate.")

f_price = R.add(Ring.INDUSTRY, "pricing", FindingClass.D,
    "The pass-through this business actually achieved, measured rather than assumed: "
    "cables revenue per tonne tracked copper times the pound almost exactly in FY2024 and "
    "then failed to in FY2025, a measured pass-through shortfall computed from audited "
    "segment revenue against the company's own disclosed tonnage",
    FY25 + " segment note 5-3, against the company's disclosed tonnage series",
    CO, "2026-03-15", is_fs_data=True, fiscal_period="FY2025",
    model_impact="Sets cables_passthrough — the measured shortfall applied in the middle "
                 "forecast years, nil in the first and last. It is the reason the study "
                 "does not assume the FY2023-24 margins return.")

f_tonnage = R.add(Ring.INDUSTRY, "demand drivers & capacity/supply balance", FindingClass.D,
    "Cable tonnage: 144,997 / 156,748 / 167,665 / 185,449 tonnes over FY2022-25 and 99,239 "
    "in the reviewed half against 89,636 — an 8.5% three-year compound rate",
    "Company quarterly earnings releases (the issuer's own; NOT audited)", IR, "2026-02-15",
    model_impact="THE Cables volume driver. The unit the largest segment is built on, and "
                 "the reason 55.4% of forecast revenue is at unit level rather than on a "
                 "growth rate.")

f_neg_entrants = R.add_negative(Ring.INDUSTRY, "new entrants (named-competitor level)",
    "A named new entrant in Egyptian cable manufacture or turnkey power engineering, and "
    "any announced capacity addition by one — searched across the filings, the releases "
    "and trade press. Nothing found that is nameable and dated; no entrant effect is "
    "modelled and the absence is not treated as evidence of none", SWEEP_DATE)

f_neg_tech = R.add_negative(Ring.INDUSTRY, "technology substitution",
    "Substitution risk to copper conductor (aluminium conductor, HVDC, superconducting "
    "cable) at a scale and date that would reach this issuer's order book inside the "
    "forecast window. Nothing disclosed in the filings and nothing dated found; no "
    "substitution effect is modelled", SWEEP_DATE)

f_neg_comp = R.add_negative(Ring.INDUSTRY, "competitor capacity / price moves (named)",
    "A named competitor's capacity or price move usable as a comparable. The nearest "
    "regional peer in cables is a Saudi manufacturer with a fraction of the revenue and "
    "no turnkey engineering arm, and no listed comparable exists for this business mix on "
    "this exchange. THIS IS THE NEGATIVE SEARCH BEHIND THE RELATIVE LENS: no peer "
    "multiple is computed anywhere in this study, and an earlier draft's unsupported "
    "'peers trade at 8-11x' range was withdrawn rather than sourced", SWEEP_DATE)

# --------------------------------------------------------------- RING 4 COMPANY
f_fs25 = R.add(Ring.COMPANY, "official financial statements", FindingClass.D,
    "FY2025 audited consolidated statements: revenue EGP 281,049mn, gross profit 40,762mn, "
    "and the segment note disclosing revenue and profit for all three segments. Segment "
    "revenue ties EXACTLY to consolidated revenue in every year",
    FY25, CO, "2026-03-15", is_fs_data=True, fiscal_period="FY2025",
    model_impact="The forecast base year. Every historical line in Appendix A is this "
                 "statement or its two predecessors, not a derivation.")

f_fs24 = R.add(Ring.COMPANY, "official financial statements", FindingClass.D,
    "FY2024 audited consolidated statements, including the three-way EGP/USD/EUR split of "
    "the borrowings note that FY2025 replaced with a two-way split",
    FY24, CO, "2025-03-13", is_fs_data=True, fiscal_period="FY2024",
    model_impact="Historical income statement and balance sheet; the FY2024 currency split "
                 "is the cross-check on the inferred FY2025 pound share of the debt book.")

f_fs23 = R.add(Ring.COMPANY, "official financial statements", FindingClass.D,
    "FY2023 audited consolidated statements: the third historical year, and the one whose "
    "margins the market's case requires to return",
    FY23, CO, "2024-03-13", is_fs_data=True, fiscal_period="FY2023",
    model_impact="Historical income statement and balance sheet; the FY2023-24 margin "
                 "level is the [R-STAR-01] case's single largest lever.")

f_q126 = R.add(Ring.COMPANY, "regular disclosures", FindingClass.D,
    "Q1-2026 reviewed interim: revenue, gross profit, the effective tax rate of 25.75%, "
    "and the borrowings note giving 20.32% on Egyptian-pound and 5.28% on hard-currency "
    "liabilities",
    Q126, CO, "2026-05-13", is_fs_data=True, fiscal_period="Q1-2026",
    model_impact="The FY2026E segment build is cross-checked — not calibrated — against "
                 "this print: 370,194 against a 356,323 grossed-up implied full year.")

f_h126 = R.add(Ring.COMPANY, "regular disclosures", FindingClass.D,
    "H1-2026 reviewed interim: segment revenue and segment profit for all three segments, "
    "the minority share of profit and of equity, and the employees' statutory share",
    H126, CO, "2026-08-11", is_fs_data=True, fiscal_period="H1-2026",
    model_impact="[R-ANCHOR-01] the three segment margin paths are RE-ANCHORED on this "
                 "half, and the FY2026 segment growth rates with them.")

f_debt = R.add(Ring.COMPANY, "management & capital actions", FindingClass.D,
    "The borrowings note discloses 21.30% on Egyptian-pound financial liabilities and "
    "5.29% blended on 'US dollars and foreign currencies' — average rates by currency "
    "bucket, but not the size of each bucket",
    FY25 + ", note 32", CO, "2026-03-15", is_fs_data=True, fiscal_period="FY2025",
    model_impact="The pound share of the debt book is BACK-SOLVED from the independently "
                 "computed effective rate at roughly 28%, and is labelled inferred "
                 "wherever it appears.")

f_own = R.add(Ring.COMPANY, "ownership / stake changes (named-transaction rule)", FindingClass.B,
    "Electra Investment Holding, an Abu Dhabi vehicle, acquired 19.98% in a July-2024 "
    "mandatory tender offer at USD 1.05 a share (~USD 449mn) and topped up to 20.37% by "
    "FY2024-end; over 2025 it SOLD roughly 32.1mn shares into the market. The founding "
    "family holds 68.0% and the free float is 13.1%",
    FY25 + " shareholder table, and the tender-offer record", CO, "2026-03-15",
    entity="Elsewedy Electric Company S.A.E.", entity_is_issuer=True,
    model_impact="A DISPOSAL, NOT DILUTION — the share count is unchanged, and the study "
                 "divides by the issued count throughout. Modelled explicitly as a "
                 "governance fact in the caveats, never smoothed into anything.")

f_assoc = R.add(Ring.COMPANY, "one-off base-resetting transactions", FindingClass.D,
    "Equity-accounted associates and non-controlling interests: minorities take 9.7% of "
    "group profit but only 7.1% of book equity",
    FY25 + " and " + H126, CO, "2026-08-11", is_fs_data=True, fiscal_period="H1-2026",
    model_impact="Minorities are charged at their PROFIT share, not at book — EGP "
                 "19,832mn, or 9.26 a share, off the equity value. Charging book instead "
                 "would add back EGP 6.87 a share, and the choice is disclosed.")

f_ir = R.add(Ring.COMPANY, "IR communications (calls, presentations, releases)", FindingClass.D,
    "The company's own quarterly earnings releases and results presentations, which carry "
    "what the audited statements do not: cable tonnage, engineering backlog, and the "
    "export and outside-Egypt sales shares",
    "Company quarterly earnings releases and Q2-2026 results presentation", IR,
    "2026-08-14",
    detail="AN EARLIER EDITION OF THIS STUDY RECORDED THESE AS 'not reachable from this "
           "research environment'. That was wrong — they were held here throughout — and "
           "the claim is withdrawn in the delivered document. What remains true is that "
           "they are the issuer's own publications and are NOT audited, which is why they "
           "drive a volume and never a financial-statement line.",
    model_impact="Unlocks the Cables unit build. Without this channel the largest segment "
                 "would be a growth rate.")

f_guid = R.add(Ring.COMPANY, "strategic plans & guidance", FindingClass.C,
    "The company publishes no numeric forward guidance — no revenue, margin, capex or "
    "backlog-conversion target — in any filing or release read for this study. Its "
    "strategy commentary is directional: export growth, the hard-currency share of sales, "
    "and the engineering backlog",
    "Company Q2-2026 results presentation and the audited statements' board report",
    IR, "2026-08-12",
    model_impact="No guidance is embedded anywhere. Every forecast driver is either a unit "
                 "series, a measured pass-through, a taper on the segment's own audited "
                 "revenue record, or a house macro path.")

# THIS CATEGORY WAS CLOSED BY A NEGATIVE SEARCH SAYING NOTHING WAS FOUND, and the study
# it records carries four dated announcements and reasons about all of them at length.
# The negative result was written before those passes and never replaced. A sweep
# register whose own study knows more than it does is worse than an empty one: it
# certifies that the looking was done and came back empty.
#
# WHAT IS TRUE IS NARROWER AND SURVIVES BELOW: none of them adds a revenue line, and the
# reason is that the spend is already inside the capex path and the output is already
# inside segment growth rates anchored on the company's own reviewed half. "Nothing is
# modelled" and "nothing was found" are different findings that read identically in a
# register, and only one of them is this study's.
f_plants = R.add(Ring.COMPANY,
    "announced projects, ventures and capacity (entity verified as the listed issuer)",
    FindingClass.B,
    "Three plants announced 24 June 2026, all opening in Q1-2028: a copper-recycling "
    "complex (US$80mn, 20,000 t/yr of scrap into cathode), a copper-tube plant (US$65mn, "
    "15,000 t/yr) and an aluminium-rod line (US$55mn, 50,000 t/yr, output targeted "
    "entirely at export) — about US$200mn, roughly EGP 11bn at the forecast rate",
    "Company announcement, 24 June 2026", IR, "2026-06-24",
    entity="Elsewedy Electric Company S.A.E.", entity_is_issuer=True,
    model_impact="MODELLED BY NOT BEING ADDED, which is a decision and is recorded as one. "
                 "The spend sits inside the capital-expenditure path, and the output sits "
                 "inside segment growth rates anchored on the company's own reviewed half, "
                 "so adding a revenue line for these plants would count the same growth "
                 "twice. Nothing is added, and that is a finding rather than an omission.")

f_datagrid = R.add(Ring.COMPANY,
    "announced projects, ventures and capacity (entity verified as the listed issuer)",
    FindingClass.D,
    "August 2026: a pre-purchase agreement to manufacture four high-voltage transformers "
    "of up to 360 MVA for a New Zealand data-centre grid connection, commissioning late "
    "2027. AN EXTERNAL REVIEW DISPUTES HOW THIS ENTRY NAMED THE COUNTERPARTIES — an "
    "earlier edition attributed the order to a specific end-customer and a specific "
    "network operator — and this study cannot settle the attribution from a primary "
    "source it has read. The entity that matters to the register IS verified and is "
    "unchanged: the announcing party is the listed issuer. The counterparty names are "
    "withdrawn rather than defended, because the entry\'s job is to name a mechanism and "
    "it does that without them",
    "Company announcement, August 2026", IR, "2026-08-01",
    entity="Elsewedy Electric Company S.A.E.", entity_is_issuer=True,
    model_impact="NAMES THE MECHANISM behind the Electrical products growth level rather "
                 "than adding to it: the global grid-equipment cycle driving that order is "
                 "the same one running through the segment's own disclosed numbers, and "
                 "the path HALVES the growth rate over four years rather than "
                 "extrapolating. The order is not modelled as a revenue line.")

f_neg_proj = R.add_negative(Ring.COMPANY,
    "announced projects, ventures and capacity (entity verified as the listed issuer)",
    "A capacity addition attributable to the listed issuer that is NOT already inside the "
    "capital-expenditure path or the segment growth anchored on the reviewed half — the "
    "named-transaction rule applied to what would change the model rather than to what "
    "was announced. None found: the four announcements above all fall inside one or the "
    "other, so no capacity line is added and capex runs as a percentage of revenue and is "
    "sensitised. Also searched and NOT found: an 8-12% export cash rebate naming this "
    "company as a beneficiary — the programme is real and dated, neither research pass "
    "could name this issuer under it or quantify a rate, and the two disagreed on the "
    "budget itself, so nothing enters", SWEEP_DATE)

f_neg_ob = R.add_negative(Ring.COMPANY, "official financial statements",
    "An order book, backlog or unit-volume (tonnage, MVA, meter-count) disclosure for any "
    "segment IN THE AUDITED FILINGS, including the Q1-2026 and H1-2026 interims. Not "
    "disclosed: the company reports segment revenue (note 5-3) and segment profit (note "
    "16) and nothing beneath them. The issuer's own releases do disclose tonnage and "
    "backlog and are recorded separately above, unaudited", SWEEP_DATE)

f_neg_split = R.add_negative(Ring.COMPANY, "management & capital actions",
    "A facility-by-facility or currency-by-currency breakdown of the debt book finer than "
    "the two-way EGP / hard-currency split disclosed in the FY2025 and Q1-2026 borrowings "
    "notes. Not disclosed at finer granularity; the pound share is back-solved and "
    "labelled inferred", SWEEP_DATE)

f_beta = R.add(Ring.COMPANY, "regular disclosures", FindingClass.D,
    "Own-stock beta, MEASURED: a weekly regression of this share against the published "
    "EGX30 index of the exchange it is listed on, matched to the exchange's own trading "
    "week and Dimson-corrected for thin trading. Beta 1.2249, R-squared 0.368, n = 256, "
    "standard error 0.1699, 90% interval [0.945, 1.504]",
    "engine/raw_ohlc/EG/SWDY.csv against engine/raw_indices/EG/EGX30.csv, through "
    "beta_regression.own_stock_beta()", PMD, "2026-09-08",
    detail="WITHDRAWN AND KEPT FOR COMPARISON: the previous edition regressed against a "
           "31-name equal-weight composite of the covered library and got 1.0087 at an "
           "R-squared of 0.291 — 21.4% below the conforming figure, explaining less of "
           "the stock. A constituent composite is a coverage artefact rather than a "
           "market, and SIGCM clause 6 calls it a hard fail rather than a tier.",
    model_impact="The beta leg of the explicit-window cost of equity. It applies to the "
                 "MATURE-MARKET premium only; the country premium is charged flat beside "
                 "it [R-COC-03]. Terminal beta is carried to 1.0 under the named "
                 "construction beta_to_one_split.")

# ------------------------------------------------------------- PRIMARY ACCESS
R.record_primary_access(
    "https://www.elsewedyelectric.com — investor relations, financial reports and "
    "quarterly earnings releases",
    reachable=True, attempt_date="2026-08-14",
    note="The issuer's own IR channel was reached and read. The quarterly earnings "
         "releases and the Q2-2026 results presentation come from it, and they carry the "
         "tonnage and backlog series the audited statements do not. An earlier edition of "
         "this study asserted the opposite — that the releases 'were not reachable from "
         "this research environment' — and that assertion is withdrawn in the delivered "
         "document and here.")

# --------------------------------------------------------------- STUDY YEAR
R.declare_study_year("FY2026", ["Q1-2026", "H1-2026"])

# ------------------------------------------------------------- DRIVER GATE TABLE
R.add_driver("Cables revenue — tonnage", DriverMode.BOTTOM_UP,
    "Built on the issuer's own disclosed tonnage series (144,997 to 185,449 tonnes over "
    "FY2022-25, 99,239 in the reviewed half), tapering from 10.7% to 5.5%. The unit is "
    "disclosed, so the segment is a unit model and not a growth rate.",
    [f_tonnage, f_ir, f_fs25])
R.add_driver("Cables revenue — copper and currency pass-through", DriverMode.BOTTOM_UP,
    "The pass-through is MEASURED out of the segment's own audited revenue per tonne "
    "against copper times the pound, not assumed. It is nil in the first and last "
    "forecast years and carries the measured shortfall in the middle three.",
    [f_price, f_copper, f_ccy, f_fs25])
R.add_driver("Constructions and infrastructure revenue", DriverMode.TOP_DOWN,
    "No unit exists that this business can be built on and no filing supplies one: "
    "turnkey engineering revenue is recognised on progress against contracts of differing "
    "size, and no filing discloses contract count, megawatts or kilometres. The segment "
    "tapers on its own FY2023-25 revenue CAGR; the disclosed backlog corroborates the "
    "level without setting it, because the releases disclose no burn profile.",
    [f_neg_ob, f_demand, f_fs25])
R.add_driver("Electrical products revenue", DriverMode.TOP_DOWN,
    "The segment aggregates transformers, meters and electrical accessories on one "
    "disclosed line and no filing splits it, so there is no unit to build on. It tapers "
    "on its own FY2023-25 revenue CAGR.",
    [f_neg_ob, f_fs25])
R.add_driver("Segment margins (all three)", DriverMode.BOTTOM_UP,
    "Re-anchored on the H1-2026 reviewed half [R-ANCHOR-01] rather than glided toward the "
    "FY2023-24 level. The FY2023-24 margins were earned on inventory bought before a "
    "devaluation, and the most recent full year measures that pricing power leaving.",
    [f_h126, f_price, f_fs25])
R.add_driver("Corporate cost load", DriverMode.BOTTOM_UP,
    "Stated on the same segment-profit-to-EBIT basis as the audited history and glided UP "
    "from FY2025's unusually low level toward the FY2023-24 average — the single most "
    "conservative choice in the build.",
    [f_fs25, f_fs24, f_fs23])
R.add_driver("Effective tax rate", DriverMode.TOP_DOWN,
    "No statutory-to-effective reconciliation is disclosed in any filing, so the rate "
    "cannot be built from its components. It is set between the statutory 22.5% and the "
    "audited effective history and carried in the sensitivity.",
    [f_neg_taxrec, f_tax, f_q126])
R.add_driver("Cost of debt and the Kd glide", DriverMode.BOTTOM_UP,
    "Currency-blended from the disclosed rates by bucket. The bucket SIZES are not "
    "disclosed, so the pound weight is back-solved from the independently computed "
    "effective rate and labelled inferred; the adopted 9.5% is struck just below both the "
    "FY2025 and Q1-2026 blended points.",
    [f_debt, f_q126, f_neg_split])
R.add_driver("Cost of equity and the country premium", DriverMode.BOTTOM_UP,
    "Beta applies to the mature-market premium only; the country premium is charged flat "
    "beside it [R-COC-03]. Beta is an own-stock weekly regression against the published "
    "EGX30 index of the exchange this share is listed on.",
    [f_beta, f_fiscal, f_macro])
R.add_driver("Terminal risk-free rate and terminal growth", DriverMode.BOTTOM_UP,
    "Both are DERIVED from the same house macro path — terminal inflation plus a real "
    "convention for the rate, terminal inflation plus zero real for the growth — so they "
    "cannot disagree about inflation. Never backed out of a price.",
    [f_macro])
R.add_driver("Capital expenditure", DriverMode.TOP_DOWN,
    "No capex guidance, maintenance-capex disclosure or investment programme is published "
    "by the issuer. Three plants ARE announced with dated dollar costs — about US$200mn, "
    "roughly EGP 11bn — and they are checked against the path rather than added to it: "
    "the sum sits inside a capex path running EGP 8.2bn to 14.7bn a year, so the path "
    "already carries them. Capex therefore runs as a percentage of revenue on the "
    "disclosed historical rate, and is sensitised.",
    [f_plants, f_neg_proj, f_guid])
R.add_driver("Minority interests", DriverMode.BOTTOM_UP,
    "Charged at the disclosed profit share rather than at book, from the interim's own "
    "split of profit and of equity.",
    [f_assoc, f_h126])

# ------------------------------------------------------------------------ OUTPUT
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
fr = R.check_freshness(SWEEP_DATE)
print("\nfreshness: %s" % (fr or "OK"))
if errors:
    raise SystemExit(1)
