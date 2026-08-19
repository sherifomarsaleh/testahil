"""PHDC — four-ring Information Sweep register, fundamental refresh of 19-Aug-2026.

Runs before any forecast driver is set. Every mandatory category of every ring is
closed by a dated finding or a dated negative search.

Primary-source note. The Company ring rests on documents the company itself issued.
The 30-Jun-2026 reviewed interim statements were supplied by the user; the FY2024
audited statements and every earnings release were pulled from the company's own
investor-relations asset library. The 1H2026 EARNINGS RELEASE IS NOT OBTAINABLE:
the IR site, its content API and the wire that carried earlier Palm Hills releases
were all checked on 19-Aug-2026 and the newest financial result published on any of
them is the 1Q2026 release of 20-May-2026. Its operating anchors — the company's own
backlog figure, its own net-debt definition, H1 new sales, H1 construction spending —
are therefore recorded as SECONDARY-UNVERIFIED from press reporting, and NO MODEL
DRIVER READS THEM. The study asks the user to attach that release, exactly as the
stop-and-inform rule requires, rather than substituting a weaker source silently.
"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from research_sweep import (SweepRegister, AssetClass, Ring, FindingClass,
                            SourceType, DriverMode)

SWEEP_DATE = "2026-08-19"
R = SweepRegister("PHDC", AssetClass.STOCK, SWEEP_DATE)
CO, IR, REG, PMD, PRESS, AGG = (SourceType.COMPANY_OFFICIAL, SourceType.COMPANY_IR,
                                SourceType.REGULATOR_OFFICIAL, SourceType.PRIMARY_MARKET_DATA,
                                SourceType.REPUTABLE_PRESS, SourceType.AGGREGATOR)

FS26 = "Interim consolidated financial statements as of 30 June 2026, limited review by Forvis Mazars Mostafa Shawki, 17-Aug-2026"
FS24 = "Audited consolidated financial statements for the year ended 31 December 2024, with 2023 comparatives"

# ================================================================ RING 1 GLOBAL
f_rate = R.add(Ring.GLOBAL, "rate cycle & USD/FX regime", FindingClass.S,
    "The pound is managed, not pegged: USD/EGP traded 49.65-51.36 over the thirty days "
    "to 19-Aug-2026 and stood at 50.52. Egypt's own curve is inverted — the 364-day bill "
    "cleared at 24.95% while the three-year bond cleared at 23.27% — so the currency and "
    "the local rate cycle are one driver, not two",
    "Central Bank of Egypt auction results (13, 16 and 17 August 2026); mid-market USD/EGP",
    PMD, "2026-08-19",
    model_impact="Sets the observed risk-free rate for the cost of capital and the "
                 "imported share of the construction cost stack. RE-RUN this refresh: the "
                 "prior study discounted at a flat 18% against a sovereign now clearing at 23.27%.")

f_comm = R.add(Ring.GLOBAL, "commodity complex (input/output)", FindingClass.S,
    "Egyptian producers left August 2026 rebar sales prices unchanged against July after "
    "earlier declines: Ezz 39,850, Beshay 39,200, Suez 38,950, Egyptian Steel 37,350 EGP "
    "per tonne, with smaller mills at 33,800-36,500. Against that, the company's own "
    "note 76 flags rising hydrocarbon and gas prices feeding the cost of works",
    "Egyptian producer August-2026 rebar price announcements; note 76, 30-Jun-2026 interim",
    PRESS, "2026-08-19",
    model_impact="RE-RUN. Steel carries its own escalator, set to zero for FY2026 on the "
                 "measured August print and 6% thereafter — never blended with cement, "
                 "finishing or labour.")

f_gdem = R.add(Ring.GLOBAL, "global sector demand", FindingClass.S,
    "Gulf capital remains the marginal cross-border buyer of Egyptian coastal product, "
    "and the company has taken the trade the other way: a 1.9 million square metre "
    "development adjacent to Saadiyat Island in Abu Dhabi, its first overseas project",
    "1Q2026 earnings release, company profile section", IR, "2026-05-20",
    model_impact="CARRIED FORWARD from the prior edition. Treated as pipeline optionality "
                 "outside the base construction-volume driver.")

R.add_negative(Ring.GLOBAL, "trade / sanctions / supply chains",
    "Egypt construction materials import restrictions 2026; sanctions exposure Egyptian "
    "real estate developers; cement and steel export bans — nothing found bearing on the "
    "subject. CARRIED FORWARD: no driver in this study depends on it", SWEEP_DATE)

# =============================================================== RING 2 COUNTRY
f_sov = R.add(Ring.COUNTRY, "sovereign macro (inflation, policy rate, FX/deval risk)",
    FindingClass.S,
    "Egypt is Caa1 at Moody's, B at S&P and Fitch. Damodaran's July-2026 file gives a "
    "rating-based adjusted default spread of 5.97% and a total equity risk premium of "
    "13.48%; on the CDS basis the sovereign trades at 3.42% net of Swiss and the total "
    "premium is 9.52%. Urban inflation rose to 14.9% in July from 14.3% in June — the "
    "first acceleration in four months — and the Monetary Policy Committee held the "
    "overnight deposit rate at 19.00% on 9 July after 825bp of cuts",
    "Damodaran ctrypremJuly26.xlsx, Egypt row; CAPMAS July-2026 release; CBE MPC statement",
    PMD, "2026-08-10",
    model_impact="RE-RUN in full. rf* = 23.269% less the sovereign's own default spread on "
                 "each basis, so country risk enters once. Both equity-risk-premium bases "
                 "are published. The inflation path drives three of the four cost escalators.")

f_tax = R.add(Ring.COUNTRY, "regulatory environment (regulator, caps, tariffs, tax/subsidy)",
    FindingClass.S,
    "Corporate tax 22.5%, confirmed on the face of the company's own tax note and matching "
    "Damodaran's Egypt row. Residents' associations are governed by Building Law 119 of "
    "2008: on constitution an association takes its own legal personality and the assets "
    "and liabilities held for it are separated in its favour",
    "Note 70 and note 63, 30-Jun-2026 interim statements", CO, "2026-08-17",
    is_fs_data=True, fiscal_period="H1-2026",
    model_impact="RE-RUN. Law 119 is the whole of the contested judgement: it is what makes "
                 "the EGP 34,337mn Residents' Association balance arguably third-party money.")

f_fiscal = R.add(Ring.COUNTRY, "fiscal / political events with sector read-through",
    FindingClass.S,
    "The company's own subsequent-events note ties the currency and hydrocarbon moves to "
    "regional conflict and warns it may raise the cost of works and affect total profit",
    "Note 76, significant events, 30-Jun-2026 interim statements", CO, "2026-08-17",
    fiscal_period="H1-2026",
    model_impact="RE-RUN. Specifies the geopolitical lever on the ticker page as a shock to "
                 "the selling-price path and the cost path, not to the volume path.")

# ============================================================== RING 3 INDUSTRY
f_mkt = R.add(Ring.INDUSTRY, "demand drivers & capacity/supply balance", FindingClass.S,
    "The ten largest Egyptian developers sold EGP 670bn in H1-2026 against EGP 651bn a "
    "year earlier, up 2.9%, on about 39,000 units, down 5%. Value is being carried by "
    "price while volume contracts",
    "Daily News Egypt survey of the ten largest developers", PRESS, "2026-08-18",
    model_impact="RE-RUN. The implied average-ticket rise of 8.3% is the dated near-term "
                 "anchor for the selling-price escalator; the volume contraction is why the "
                 "construction-volume path decelerates.")

f_price = R.add(Ring.INDUSTRY, "pricing", FindingClass.S,
    "Same survey: rising prices are supporting developers' sales while underlying demand "
    "is under pressure and buyers face reduced purchasing power. Palm Hills ranked second "
    "on H1-2026 sales",
    "Daily News Egypt survey of the ten largest developers", PRESS, "2026-08-18",
    model_impact="RE-RUN. Price escalates at 8.3% in the anchor year then converges on the "
                 "disinflation path; it is the numerator of the crux ratio.")

f_peer = R.add(Ring.INDUSTRY, "competitor capacity / price moves (named)", FindingClass.S,
    "Talaat Moustafa led H1-2026 with about EGP 219bn of sales; Mountain View 63.7bn, "
    "Emaar Misr 60.9bn, Hyde Park 52.9bn, Tatweer Misr 50.5bn, Madaar Ras El Hekma 44bn, "
    "G Developments 30bn, Madinet Masr 28.4bn, La Vista 26.5bn. On the market: Talaat "
    "Moustafa trades at 10.2x earnings on a market value of EGP 156.6bn, Emaar Misr and "
    "SODIC at about 6.1x forward, Heliopolis Housing at 7.5x; outside Egypt, Emaar "
    "Properties at 6.5x and 3.6x EBITDA, Aldar at 7.7x and 6.6x EBITDA",
    "Daily News Egypt survey; market-data aggregators (Simply Wall St, TradingView, "
    "stockanalysis.com), quotes dated 11-Aug-2026 and June/August 2026", AGG, "2026-08-11",
    model_impact="RE-RUN. Feeds the relative-multiples lens only, in and outside the country. "
                 "No aggregator figure touches the subject's own reported historicals.")

R.add_negative(Ring.INDUSTRY, "new entrants (named-competitor level)",
    "New entrants to Egyptian residential development 2026; foreign developers entering "
    "Egypt; Ras El Hekma consortium new masterplan developers. The named set is unchanged "
    "from the prior edition apart from Madaar Ras El Hekma appearing in the top ten. "
    "CARRIED FORWARD", SWEEP_DATE)

R.add_negative(Ring.INDUSTRY, "technology substitution",
    "Modular and prefabricated construction disruption of Egyptian developer margins; "
    "proptech disintermediation of Egyptian brokerage. Nothing found that changes a driver. "
    "CARRIED FORWARD", SWEEP_DATE)

# =============================================================== RING 4 COMPANY
f_fs26 = R.add(Ring.COMPANY, "official financial statements", FindingClass.S,
    "Interim consolidated statements as of 30 June 2026, limited review by Forvis Mazars "
    "Mostafa Shawki, board authorisation and review report both dated 17-Aug-2026. Revenue "
    "EGP 19,528mn (+25.4%), gross operating profit 6,926mn (35.47%), attributable profit "
    "2,265mn (-7.3%), total assets 194,767mn, controlling equity 18,911mn",
    FS26, CO, "2026-08-17", is_fs_data=True, fiscal_period="H1-2026",
    model_impact="NEW. Every historical line in the model comes from this filing or from "
                 "the FY2024 audited statements. It replaces the prior edition's entirely "
                 "assumption-driven project build.")

f_fs24 = R.add(Ring.COMPANY, "official financial statements", FindingClass.C,
    "FY2024 audited consolidated statements with FY2023 comparatives: revenue EGP "
    "27,167mn and 17,462mn, gross profit 9,330mn and 5,508mn, attributable profit 3,255mn "
    "and 1,582mn — two audited fiscal years read from the filing itself",
    FS24, CO, "2025-03-01", is_fs_data=True, fiscal_period="FY2024",
    model_impact="NEW. Supplies the three-year history and, decisively, shows that the "
                 "H1-2026 gross margin of 35.5% sits ABOVE FY2023 and marginally above "
                 "FY2024 — the 2025 margin was the outlier, not 2026.")

f_fs23 = R.add(Ring.COMPANY, "official financial statements", FindingClass.C,
    "FY2023 audited figures taken from the comparative column of the FY2024 filing: "
    "revenue EGP 17,462mn, gross profit 5,508mn, profit before tax 2,301mn, attributable "
    "profit 1,582mn",
    FS24, CO, "2025-03-01", is_fs_data=True, fiscal_period="FY2023")

f_note72 = R.add(Ring.COMPANY, "regular disclosures", FindingClass.S,
    "Note 72 is the only backlog figure that appears in a reviewed or audited statement: "
    "contracts for undelivered units concluded between 1-Jan-2023 and 30-Jun-2026 carry a "
    "contractual value of EGP 149,118mn, notes receivable of EGP 116,540mn nominal held "
    "off balance sheet, and a present value of EGP 59,398mn, with a full maturity ladder "
    "to 2030 and beyond",
    FS26 + " — note 72", CO, "2026-08-17", is_fs_data=True, fiscal_period="H1-2026",
    model_impact="NEW. Anchors the contracted-book expert lens and the volume path. It is "
                 "also the second dual-framing: the company's own wider backlog definition "
                 "stood at EGP 263bn at 1Q2026, and the study says which is which.")

f_ra = R.add(Ring.COMPANY, "one-off base-resetting transactions", FindingClass.B,
    "The Residents' Association balance reached EGP 34,337mn at 30-Jun-2026, up EGP "
    "5,215mn in six months. It is deferred customer money invested for the associations' "
    "benefit until each takes legal personality under Building Law 119. Strip its movement "
    "out and reported operating cash flow is negative in every disclosed period: EGP "
    "-3,716mn in H1-2026, -5,592mn in H1-2025, -6,963mn in FY2024 and -3,024mn in FY2023",
    FS26 + " — note 63 and the cash-flow statement; " + FS24, CO, "2026-08-17",
    is_fs_data=True, fiscal_period="H1-2026",
    model_impact="NEW, and it is THE contested judgement. Computed both ways: framing A "
                 "treats the float as permanent operating funding, framing B as restricted "
                 "third-party money. Both are published in full; they are never averaged.")

f_debt = R.add(Ring.COMPANY, "management & capital actions", FindingClass.S,
    "Note 34 gives the company's own schedule of interest-bearing obligations: EGP "
    "26,480mn, of which about EGP 21.4bn floats (a 2% rate move is worth EGP 428mn). Every "
    "facility in note 51 is denominated in Egyptian pounds, and the net foreign-currency "
    "position is an ASSET of EGP 2,448mn. The company also bought 23.51 million treasury "
    "shares in H1-2026 at an average EGP 9.61 and paid EGP 686mn of dividends",
    FS26 + " — notes 34, 48-52, 62", CO, "2026-08-17", is_fs_data=True,
    fiscal_period="H1-2026",
    model_impact="NEW. Fixes the local-currency/foreign-currency debt split at effectively "
                 "100% local, corrects the share count to the ex-treasury 2,824.5mn, and "
                 "corrects the prior edition's claim that the company pays no dividend.")

f_ir1q = R.add(Ring.COMPANY, "IR communications (calls, presentations, releases)",
    FindingClass.S,
    "1Q2026 earnings release, 20-May-2026: new sales EGP 52bn, backlog EGP 263bn, net debt "
    "EGP 3.3bn on the company's own definition, construction spending EGP 4.6bn up 60% "
    "year on year, 1,200 contractual units ready for handover in FY2026, land bank 46 "
    "million square metres, an EGP 2.015bn securitisation closed under a EGP 30bn "
    "programme, and the company's own revenue, EBITDA and profit history for 2022-2025",
    "Palm Hills Developments 1Q2026 earnings release, company IR asset library", IR,
    "2026-05-20", fiscal_period="Q1-2026",
    model_impact="RE-RUN. The construction-spending and units-for-handover figures are the "
                 "physical cross-check on the work-carried-out driver; the history charts "
                 "supply FY2025 revenue and EBITDA, which no obtained statement carries.")

f_ir9m = R.add(Ring.COMPANY, "IR communications (calls, presentations, releases)",
    FindingClass.C,
    "9M2025 release, 13-Nov-2025: revenue EGP 25,549mn, gross profit 10,423mn at a 41% "
    "margin, EBITDA 6,690mn at 26%, new sales EGP 182bn, construction spending EGP 10.5bn "
    "up 71%, backlog EGP 225bn, net debt EGP 4.2bn. With the FY2025 totals this pins "
    "Q4-2025 at a 17.5% EBITDA margin",
    "Palm Hills Developments 9M2025 earnings release", IR, "2025-11-13", fiscal_period="FY2025",
    model_impact="NEW. Establishes that the margin compression began in Q4-2025 and has "
                 "since stabilised, which is why the crux holds the measured rate flat "
                 "rather than extrapolating further decline.")

f_launch = R.add(Ring.COMPANY, "strategic plans & guidance", FindingClass.B,
    "SECONDARY-UNVERIFIED. Press reporting of the 1H2026 results states that Hacienda Ras "
    "El Hekma booked EGP 75bn of sales in the first two weeks of launch to the close of "
    "17-Aug-2026, to be recognised as new sales in Q3-2026, and puts the backlog at a "
    "record EGP 284bn. Neither figure appears in any company document this study could "
    "obtain",
    "Arab Finance and related press reporting of the 1H2026 results release", PRESS,
    "2026-08-18",
    model_impact="NO DRIVER READS IT. It raises the launch lever's default probability on "
                 "the ticker page from 55 to 85 and appears in the catalyst calendar, and "
                 "it is flagged as unverified in both places.")

f_neg_split = R.add_negative(Ring.COMPANY, "regular disclosures",
    "Land cost of contracted units and the joint-arrangement partners' share of revenue, "
    "searched for as a separable disclosure across every obtained document: note 43 (which "
    "states plainly that work in progress is struck AFTER excluding the cost of the "
    "contracted lands), note 65 (which stops at one line, cost of real estate development), "
    "note 58 (which gives the partners' balance by project but not the charge to the income "
    "statement), the FY2024 audited notes and every earnings release 2023-2026. NOT "
    "DISCLOSED ANYWHERE. Solving across period pairs leaves one equation in two unknowns "
    "because the cumulative charge to the income statement is given at only two dates",
    SWEEP_DATE)

R.add_negative(Ring.COMPANY, "ownership / stake changes (named-transaction rule)",
    "Palm Hills Developments shareholding changes 2026; Mansour Group stake sale; new "
    "strategic investor. Nothing found. The only capital action in the period is the "
    "treasury buyback disclosed in note 62, which is recorded above", SWEEP_DATE)

# ---- primary access log: attempts and outcomes, successes and failures --------
R.record_primary_access("https://www.palmhillsdevelopments.com/investor-relations", True,
    SWEEP_DATE, "served, but as a client-rendered application; the asset library behind it "
                "was read through its content delivery interface")
R.record_primary_access("https://ir.palmhillsdevelopments.com/en-us/financial", True,
    SWEEP_DATE, "reached; the newest published financial result is the 1Q2026 release")
R.record_primary_access("company IR asset library (financial results collection)", True,
    SWEEP_DATE, "FY2024 audited statements, Q1-2026 and Q2-2025 interims, and every "
                "earnings release from 2015 to 1Q2026 retrieved directly")
R.record_primary_access("1H2026 earnings release — company IR channel", False, SWEEP_DATE,
    "NOT PUBLISHED as of 19-Aug-2026 on the IR site, its content API or the wire that "
    "carried earlier Palm Hills releases. Its operating anchors are therefore carried as "
    "secondary and unverified, no driver reads them, and the study asks for the document")
R.record_primary_access("FY2025 annual financial statements — company IR channel", False,
    SWEEP_DATE, "NOT PUBLISHED. FY2025 revenue and EBITDA are taken from the company's own "
                "history charts in the 1Q2026 release; FY2025 attributable profit comes "
                "from the audited statement of changes in equity inside the 30-Jun-2026 "
                "filing; FY2025 gross profit and finance costs are shown blank, not estimated")
R.record_primary_access("https://www.cbe.org.eg/en/auctions/egp-t-bonds-fixed-coupon", True,
    SWEEP_DATE, "17-Aug-2026 bond auction results read directly from the central bank")
R.record_primary_access("https://pages.stern.nyu.edu/~adamodar/pc/datasets/ctrypremJuly26.xlsx",
    True, SWEEP_DATE, "July-2026 original country-premium file; the Egypt row is read from it")

# ---- study-year declaration: PHDC reports quarterly ---------------------------
R.declare_study_year("2026", ["Q1-2026", "H1-2026"])

# ---- driver gate table --------------------------------------------------------
R.add_driver("Construction volume executed (the physical driver)", DriverMode.BOTTOM_UP,
             "Note 43 discloses work carried out in the period and cumulatively, split "
             "into land and construction, with capitalised interest separately stated. "
             "The 1Q2026 release gives cash construction spending and the units due for "
             "handover as an independent cross-check",
             [f_fs26, f_ir1q, f_mkt])
R.add_driver("Selling price per unit of work (the crux ratio)", DriverMode.BOTTOM_UP,
             "Note 64 gives real-estate revenue and note 43 gives the construction cost "
             "relieved to the income statement, so the ratio is measured, not assumed; the "
             "industry survey supplies the dated escalation anchor",
             [f_fs26, f_mkt, f_price])
R.add_driver("Construction cost per unit, one escalator per physical class",
             DriverMode.BOTTOM_UP,
             "Steel on the measured August-2026 producer prices, cement on the disclosed "
             "Egyptian price path, finishing on the published inflation path, site labour "
             "on that path plus a margin. The class WEIGHTS are estimated and flagged: no "
             "filing discloses a cost-by-nature split of construction",
             [f_comm, f_sov, f_fs26])
R.add_driver("Land cost and partners' share of revenue", DriverMode.TOP_DOWN,
             "NEGATIVE SEARCH JUSTIFIES TOP-DOWN. The two blocks cannot be separated from "
             "the disclosed data: note 43 pins the construction half of the cost of real "
             "estate development and the remainder is land plus the joint-arrangement "
             "partners' share together. One equation, two unknowns, and no period pair "
             "resolves it. The study demonstrates the split unidentified, publishes the "
             "range it can bound, and carries the combined block at its measured rate",
             [f_fs26, f_note72, f_neg_split])
R.add_driver("Working capital and the cash conversion cycle", DriverMode.BOTTOM_UP,
             "Receivables, work in progress, supplier advances, customer advances, "
             "contractor payables and the joint-arrangement balance are each disclosed on "
             "the face of the balance sheet and rolled on their own measured ratio",
             [f_fs26])
R.add_driver("Residents' Association float", DriverMode.BOTTOM_UP,
             "Solved from the company's own disclosed movements across FY2023, FY2024 and "
             "H1-2026 rather than assumed; carried as a bounded stock ratio and computed "
             "BOTH WAYS as the study's contested judgement",
             [f_ra, f_tax])
R.add_driver("Cost of capital", DriverMode.BOTTOM_UP,
             "Risk-free from the central bank's own auction, sovereign spread and equity "
             "risk premium from the July-2026 original country file, beta from the "
             "sanctioned own-stock regression against the exchange's published index, "
             "marginal cost of debt from the company's own realised interest cost against "
             "its own treasury-bill book",
             [f_sov, f_rate, f_debt])

# ---- validate -----------------------------------------------------------------
errors, warnings = R.validate()
print("errors:", errors)
print("warnings:", warnings)
print(R.qc_line())
print("freshness:", R.check_freshness(SWEEP_DATE) or "OK — sweep and delivery same day")
assert not errors, errors
R.to_json(os.path.join(HERE, "sweep_register.json"))
print("wrote sweep_register.json —", R.counts())
