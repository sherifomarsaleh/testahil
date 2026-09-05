"""STC — four-ring Information Sweep register, through the SHARED module.

CLAUDE.md says of engine/research_sweep.py: "import this rather than hand-rolling a
study-local sweep script". This study had no sweep script at all, which is why it sits on
that ratchet; nine studies were in the same state when the gate was written.

WHAT THE SHARED REGISTER FORCES THAT A LOCAL ONE WOULD NOT. Its invariants demand a dated
negative search wherever a mandatory category is closed by absence rather than by a finding,
a company-official source on every financial-statement figure, an investor-relations source
distinct from the audited statements, the company's own site attempted and LOGGED either
way, and every driver tied back to a numbered finding. The point is not that a local script
could not check those — it is that a local script checks the list its author thought of.

EVERY NEGATIVE SEARCH BELOW WAS ACTUALLY RUN over the documents named in src/SOURCES.md,
on the date recorded. Inventing one to clear a coverage check is worse than the gap it
clears, and moving a finding's ring to satisfy a checker is the same offence as renaming
its category.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))

from research_sweep import (SweepRegister, AssetClass, Ring, FindingClass,
                            SourceType, DriverMode)

SWEEP_DATE = "2026-09-05"
R = SweepRegister("STC", AssetClass.STOCK, SWEEP_DATE)
CO, IR, REG, PMD, PRESS = (SourceType.COMPANY_OFFICIAL, SourceType.COMPANY_IR,
                           SourceType.REGULATOR_OFFICIAL, SourceType.PRIMARY_MARKET_DATA,
                           SourceType.REPUTABLE_PRESS)

# --------------------------------------------------------------- PRIMARY ACCESS
# THE COMPANY'S OWN SITE, ATTEMPTED AND LOGGED BOTH WAYS. Four investor-relations URLs
# recorded in this study's earlier register returned the site's own 404 page under an
# HTTP 200 and were written up as evidence the channel was gone; the sitemap listed the
# whole investor section and the presentations page resolved first try [L-343].
R.record_primary_access(
    "https://www.stc.com.sa/content/stcgroupwebsite/sa/en/investors/financial-reports/"
    "presentations-and-report.html", True, SWEEP_DATE,
    note="Reached through www.stc.com.sa/sitemap.xml after four direct URL guesses had "
         "each returned the site's own 404 page under an HTTP 200. Carries every earnings "
         "presentation and call transcript back to 2017. The financial statements come "
         "from the same group site at www.stc.com/content/dam/groupsites/en/pdf/.")

R.declare_study_year("FY2026", ["Q1-2026", "H1-2026"])

# ------------------------------------------------------------------ RING 1 GLOBAL
f_rates = R.add(
    Ring.GLOBAL, "rate cycle & USD/FX regime", FindingClass.S,
    "The riyal is pegged to the dollar at 3.75, so Saudi Arabia imports United States "
    "monetary policy and TODAY IS ALREADY THE TERMINAL for the cost of capital; the house "
    "macro path calls the regime pegged and the schedule is flat by construction",
    # A SOURCE FIELD NAMES AN INSTITUTION, NOT A FILE. This named the house macro path's
    # own file location, and the bibliography quotes the research trail verbatim — so the
    # path reached a document a reader receives, where the shape-matching gate caught it.
    # The file is where this desk keeps the figure; the SOURCE is who published it.
    "The International Monetary Fund's World Economic Outlook database, and the sovereign "
    "quote carried on the house macro path for Saudi Arabia at its own as-of date",
    REG, "2026-07-31",
    model_impact="Sets the cost-of-capital schedule FLAT rather than gliding, and makes "
                 "the currency path flat by construction of the peg. It is also why this "
                 "company's dollar borrowings are carried at their own coupon: under a peg "
                 "the expected depreciation in the local-equivalent cost is zero.")

f_sofr = R.add(
    Ring.GLOBAL, "commodity complex (input/output)", FindingClass.D,
    "This business has no commodity input in the sense the category means: its cost of "
    "revenues is handsets and equipment, interconnection, wages, a regulated levy and "
    "maintenance, and note 35 discloses all seven lines. The nearest thing to a global "
    "price input is imported device and network equipment cost, which is the largest "
    "single line at SAR 14,195,531 thousand, 18.2% of revenue",
    "stc_Annual-2025-en.txt, note 35, cost of revenues by nature", CO, "2026-02-25",
    is_fs_data=True, fiscal_period="FY2025",
    model_impact="The cost-stack rule requires ONE ESCALATOR PER DRIVER CLASS. The device "
                 "and equipment line is dollar-denominated under a pegged riyal, so it "
                 "cannot take the domestic inflation ladder that governs the wage line.")

f_demand = R.add(
    Ring.GLOBAL, "global sector demand", FindingClass.S,
    "Global telecom demand growth is in data volume rather than in revenue per user, and "
    "this company's own record shows the same shape: a subscriber base compounding at "
    "6.00% a year against revenue per subscriber falling 3.86%",
    "EarningsPresentationQ4-2025En.txt and earnings-presentation2024en.txt, subscriber "
    "charts, cross-checked against note 9 segment revenue", IR, "2026-02-25",
    model_impact="It is the reason the stc segment is built as volume times price rather "
                 "than on a net growth rate: the net hides two forces moving opposite ways "
                 "and neither is equally likely to persist.")

n_trade = R.add_negative(
    Ring.GLOBAL, "trade / sanctions / supply chains",
    "Searched the FY2025 audited statements and the FY2025 and H1-2026 earnings "
    "presentations for sanctions, export controls, supply-chain disruption or tariffs. "
    "Two hits in the statements, neither a risk disclosure: one lists 'supply chain and "
    "other related services' among a subsidiary's permitted activities, and one records a "
    "2017 Kuwaiti court ruling on a regulatory tariff decree. No supply-chain or sanctions "
    "exposure is disclosed anywhere in the three documents.",
    SWEEP_DATE)

# ----------------------------------------------------------------- RING 2 COUNTRY
f_macro = R.add(
    Ring.COUNTRY, "sovereign macro (inflation, policy rate, FX/deval risk)", FindingClass.B,
    "Saudi consumer-price inflation ran 2.5% (2023), 1.5% (2024) and 2.0% (2025) and the "
    "published projection ladder is 2.3 / 2.1 / 2.0 / 2.0 / 2.0 to 2030, terminating at "
    "2.0%; the riyal is pegged so devaluation risk is a regime question rather than a rate",
    "International Monetary Fund, World Economic Outlook database, series PCPIPCH, Saudi "
    "Arabia (SAU), read live from the datamapper API", REG, "2026-09-05",
    model_impact="Every nominal growth rate in the model recomputes from a stated REAL "
                 "rate on this ladder, and the three historical prints are what the "
                 "trailing segment growth is deflated by so that history and forecast sit "
                 "on one economy.")

f_reg = R.add(
    Ring.COUNTRY, "regulatory environment (regulator, caps, tariffs, tax/subsidy)",
    FindingClass.B,
    "GOVERNMENT CHARGES ARE A DISCLOSED COST LINE OF SAR 5,417,576 thousand, 7.0% of "
    "revenue, and licences and frequency spectrum are carried at SAR 5,941,321 thousand "
    "net book value with named expiry dates running 2029, 2032, 2033, 2034, 2037 and 2039 "
    "in Saudi Arabia alone. A SAR 1,124,590 thousand 600MHz block expiring 2039 was added "
    "in FY2025",
    "stc_Annual-2025-en.txt, notes 12 and 35", CO, "2026-02-25",
    is_fs_data=True, fiscal_period="FY2025",
    model_impact="The regulated levy is 7% of revenue and moves with a rule rather than "
                 "with inflation, so it cannot sit inside a blended cost escalator. The "
                 "first Saudi spectrum expiry, 2029, falls INSIDE the explicit forecast "
                 "window, and renewal cost is not disclosed — a named gap, not an "
                 "assumption.")

n_fiscal = R.add_negative(
    Ring.COUNTRY, "fiscal / political events with sector read-through",
    "Searched the FY2025 audited statements and both 2026 interim sets for any fiscal or "
    "political event with a stated effect on this company — a change in the zakat or "
    "income-tax basis, a subsidy, a state directive. The tax note records ordinary zakat "
    "and income tax and a FY2025 CREDIT of SAR 466,436 thousand against a FY2024 charge of "
    "1,191,564, a swing of 1.66bn that the statements do not attribute to a policy change. "
    "Nothing else is disclosed.",
    SWEEP_DATE)

# ---------------------------------------------------------------- RING 3 INDUSTRY
f_subs = R.add(
    Ring.INDUSTRY, "demand drivers & capacity/supply balance", FindingClass.D,
    "Saudi mobile subscribers rose 26.47mn to 28.34mn to 30.0mn across the three filed "
    "year ends and fixed 5.57mn to 5.72mn to 6.0mn; the latest disclosed point is 30.3mn "
    "and 6.1mn at H1-2026. Penetration is already far above one mobile line per person, "
    "so the volume line cannot extend at 6% indefinitely",
    "earnings-presentation2024en.txt, EarningsPresentationQ4-2025En.txt and "
    "EarningsPresentationQ2-2026En.txt, subscriber charts", IR, "2026-08-05",
    model_impact="It is the volume half of the stc segment's revenue build, and the reason "
                 "the real rate is faded to zero rather than extended: a penetrated market "
                 "cannot compound its subscriber base for ever.")

f_price = R.add(
    Ring.INDUSTRY, "pricing", FindingClass.D,
    "Revenue per subscriber fell from SAR 1,536.1 a year to 1,457.5 to 1,420.0 across the "
    "three filed years — a decline of 3.86% a year compounding, which with 6.00% volume "
    "growth multiplies back to exactly the +1.91% the audited segment revenue reports",
    "note 9 segment revenue divided by the subscriber counts in the earnings "
    "presentations; units.py checks the identity three ways", IR, "2026-02-25",
    model_impact="The price half of the same build. It is why the segment's +0.16% real "
                 "growth is not a mature business standing still: it is two large forces "
                 "moving against each other, and a forecast on the net could not say which "
                 "one it expected to continue.")

n_entrants = R.add_negative(
    Ring.INDUSTRY, "new entrants (named-competitor level)",
    "Searched the FY2025 audited statements and the FY2025 and H1-2026 earnings "
    "presentations for any named competitor, market-share figure or new entrant. ZERO "
    "hits across all three documents for 'competitor', 'market share', 'Mobily' or 'Zain'. "
    "This company does not disclose its competitive position in any document this study "
    "holds, and no peer multiple or share figure is therefore used anywhere in the model.",
    SWEEP_DATE)

f_tech = R.add(
    Ring.INDUSTRY, "technology substitution", FindingClass.S,
    "Fixed-wireless broadband is disclosed as a separate subscriber category and is flat "
    "at 0.5mn while fixed-wired grows 1.30mn to 1.4mn, so within this company's own "
    "disclosure the substitution runs toward fibre rather than away from it. A direct-to-"
    "mobile satellite partnership with AST SpaceMobile is disclosed as a partnership "
    "rather than as a revenue line",
    "EarningsPresentationQ4-2025En.txt, subscriber categories and the partnership summary",
    IR, "2026-02-25",
    model_impact="It is the reason the fixed lines are not given a decline driver: the "
                 "disclosed mix is moving between fixed categories rather than out of them.")

n_competitor = R.add_negative(
    Ring.INDUSTRY, "competitor capacity / price moves (named)",
    "The same search as the new-entrants category and with the same result: no named "
    "competitor appears in any of the three documents, so no competitor capacity or price "
    "move can be cited. Recorded as an evidenced absence rather than closed by moving a "
    "company-ring finding into this row.",
    SWEEP_DATE)

# ----------------------------------------------------------------- RING 4 COMPANY
f_guide = R.add(
    Ring.COMPANY, "strategic plans & guidance", FindingClass.S,
    "Management publishes a capital-expenditure band of 15.0% to 17.5% of revenue and a "
    "dividend policy of SAR 0.55 a quarter locked to the third quarter of 2027",
    "EarningsPresentationQ4-2025En.txt and the delivered study's own record of the policy",
    IR, "2026-02-25",
    model_impact="SCORED AND NOT CONSUMED [R-FCAL-01]. The delivered study took the capex "
                 "band straight in as its driver; the rebuilt model uses the ratio the "
                 "filings actually show — 1.161 times depreciation — and publishes the "
                 "band beside it as the guidance it is.")

f_fs25 = R.add(
    Ring.COMPANY, "official financial statements", FindingClass.B,
    "FY2025 audited: revenue 77,818,675, gross profit 37,699,689, EBITDA 24,469,435, EBIT "
    "14,438,264, total assets 157,476,669, borrowings 15,191,428, cash and equivalents "
    "13,376,071. Every line foots to its own note",
    "stc_Annual-2025-en.txt, audited by Deloitte and Touche & Co.", CO, "2026-02-25",
    is_fs_data=True, fiscal_period="FY2025",
    model_impact="The base year of the whole build, and the year each segment's gross "
                 "margin is held at.")

f_fs23 = R.add(
    Ring.COMPANY, "regular disclosures", FindingClass.B,
    "FY2023 exists on TWO bases and both are held: as originally reported, revenue "
    "72,336,611 with TAWAL as a segment; as restated on a continuing basis in the FY2024 "
    "filing, 71,777,161 with TAWAL a discontinued operation. The bridge between them foots "
    "to the riyal — less TAWAL's 3,343,350, plus the 3,076,148 of eliminations that went "
    "with it, less note 49's 292,248 reclassification",
    "STC_FY2023_FS_en.txt note 9 and stc_Annual-2024-en.txt notes 9 and 49", CO,
    "2024-02-25", is_fs_data=True, fiscal_period="FY2023",
    model_impact="The forward basis is CONTINUING, because TAWAL was sold and a forecast "
                 "built on revenue the company no longer earns is a forecast of something "
                 "that does not exist. The as-filed column is kept because a point-in-time "
                 "origin must see what was published at the time.")

f_q1 = R.add(
    Ring.COMPANY, "IR communications (calls, presentations, releases)", FindingClass.S,
    "The Q1-2026 reviewed interim and its earnings presentation are published, as are the "
    "H1-2026 set and an H1-2026 earnings call transcript",
    "financial-statementsQ1-2026En.txt and the investor-relations presentations page",
    IR, "2026-05-01", fiscal_period="Q1-2026",
    model_impact="Sweeping every disclosed quarter of the study year BEFORE the build is "
                 "the rule; the Q1 set is registered here and the H1 set is what the "
                 "bridge stands on.")

f_h1 = R.add(
    Ring.COMPANY, "management & capital actions", FindingClass.B,
    "H1-2026 reviewed: total assets 166,996,964, long-term borrowings 22,094,126 and "
    "short-term 1,442,428, lease liabilities 2,258,902, cash 18,940,773, equity "
    "attributable 84,986,806, minority 2,726,349. Share capital is SAR 50,000,000 thousand "
    "in shares of SAR 10, which divides to the 5,000,000 thousand shares note 17 states, "
    "less 6,976 thousand in treasury",
    "financial-statementsQ2-2026En.txt, reviewed, notes 15 and 17", CO, "2026-08-05",
    is_fs_data=True, fiscal_period="H1-2026",
    model_impact="The bridge stands on this sheet and the share count is footed against par "
                 "from it. The balance sheet PRINTS share capital as 60,000,000, which is "
                 "an extraction artefact of that page: note 17 says 50,000,000 at both "
                 "dates and only 50,000,000 makes the equity block foot to the stated "
                 "84,986,806.")

f_sukuk = R.add(
    Ring.COMPANY, "one-off base-resetting transactions", FindingClass.B,
    "TWO ONE-OFFS INSIDE THE COST LINE, each named in its own filing's footnote: SR 1,500 "
    "million of withholding-tax provision reversed into FY2024's network access charges "
    "and SR 724 million of provision reversed into FY2023's government charges. Separately, "
    "international sukuk of SAR 7,500 million was issued in the first half of 2026 in two "
    "tranches at 4.489% and 5.083%, and TAWAL was contributed to DIIC in February 2025 for "
    "43.06% of it",
    "stc_Annual-2025-en.txt note 35, stc_Annual-2024-en.txt note 36, "
    "financial-statementsQ2-2026En.txt note 15 and stc_Annual-2025-en.txt note 8.1.1",
    CO, "2026-08-05", is_fs_data=True, fiscal_period="FY2024",
    model_impact="The two reversals flatter FY2023 and FY2024, so the UNDERLYING gross "
                 "margin rises 47.39 / 47.21 / 48.45 where the reported one dips and "
                 "recovers — and the model holds the highest of the three flat. The sukuk "
                 "is the marginal cost of debt the schedule adopts, and the DIIC "
                 "contribution is why the bridge's associates line more than doubled.")

f_own = R.add(
    Ring.COMPANY, "ownership / stake changes (named-transaction rule)", FindingClass.S,
    "The direct holding in Telefonica rose from 4.97% to 9.97% during 2025 after regulatory "
    "approval, and the forward agreement that had given synthetic exposure to the extra 5% "
    "was terminated. It is irrevocably designated at fair value through other comprehensive "
    "income and carried at SAR 8,513,430 thousand at 30 June 2026",
    "stc_Annual-2025-en.txt note 9.1 and financial-statementsQ2-2026En.txt note 9.1",
    CO, "2026-08-05", is_fs_data=True, fiscal_period="H1-2026",
    model_impact="It is a NAMED transaction rather than an estimate, and the bridge takes "
                 "the company's own disclosed Level 1 fair value rather than a mark this "
                 "desk computed.")

# ------------------------------------------------------------------ DRIVER GATE
R.add_driver(
    "stc segment revenue (two thirds of group)", DriverMode.BOTTOM_UP,
    "Volume times price on disclosed units: subscribers by category from the earnings "
    "presentations, revenue per subscriber derived against the audited segment revenue, "
    "each half faded to zero real and multiplied.",
    [f_subs, f_price, f_fs25])

R.add_driver(
    "the other twelve segments' revenue", DriverMode.BOTTOM_UP,
    "Each grows at its own measured two-year real rate from note 9, deflated by the "
    "published inflation prints, fading to zero real. No unit data is disclosed for any of "
    "them, so this is the finest sourced level available and the gap is flagged rather "
    "than filled.",
    [f_fs25, f_fs23, f_macro])

R.add_driver(
    "cost of revenues", DriverMode.BOTTOM_UP,
    "Note 35 discloses all seven lines by nature for three years and each is a different "
    "driver class. The model currently holds each segment's disclosed gross margin, and "
    "the seven-line build is registered as the next correction rather than claimed here.",
    [f_sofr, f_reg, f_sukuk])

R.add_driver(
    "competitive position and peer multiples", DriverMode.TOP_DOWN,
    "No named competitor, market share or peer figure appears in any document this study "
    "holds, so no relative multiple is taken from peers. The relative lens uses this "
    "company's OWN trailing EV/EBITDA at three year ends instead.",
    [n_entrants, n_competitor, f_fs25])

R.add_driver(
    "spectrum renewal cost inside the explicit window", DriverMode.TOP_DOWN,
    "The first Saudi spectrum expiry falls in 2029, inside the forecast window, and no "
    "renewal cost is disclosed anywhere. Carried inside the capital-expenditure ratio "
    "measured from the filings rather than modelled separately, and named as a gap.",
    [f_reg, n_fiscal, f_fs25])


if __name__ == '__main__':
    errors, warnings = R.validate()
    for e in errors:
        print('ERROR  ', e)
    for w in warnings:
        print('warning', w)
    print()
    print(R.qc_line())
    R.to_json(os.path.join(HERE, 'sweep_register.json'))
    print('wrote sweep_register.json')
    raise SystemExit(1 if errors else 0)
