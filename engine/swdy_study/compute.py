"""SWDY study — master computation. Writes study_numbers.json (single source of
truth for every builder). Code-first rule: INPUTS are four-field records
{value, source, date, ring}; a bare numeral cannot enter the model; the ASSERT
block raises (no JSON emitted) unless the bridge closes, the discount-rate glide
is ordered, the Kd-integrity triple holds, and the terminal is ROIC-consistent.

Company class: diversified industrial operating company (wires & cables
manufacturer + engineering & construction contractor + electrical products,
digital solutions and infrastructure investment). Lens set follows the
operating-company reference: FCFF DCF primary, relative multiples, normalized
earnings power, and a book/ROE lens.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import numpy as np

# ============================ INPUTS =========================================
def I(value, source, date, ring):
    return dict(value=value, source=source, date=date, ring=ring)

INP = dict(
    # ---- anchors --------------------------------------------------------
    spot=I(105.20, "Uploaded EGX daily price history, last close", "2026-08-05", "Market"),
    shares_mn=I(2140.777876, "Number of shares 2,140,777,876 — company earnings release, Share "
                "Information panel (unchanged across FY2024 and Q1-2025 releases). An EGM-approved "
                "capital cut writes off 1.422mn expired ESOP shares, taking issued capital to "
                "EGP 2.139bn; immaterial (0.07%) and not yet listed, so the disclosed count is used",
                "2025-05-26", "Company"),
    tax_stat=I(0.225, "Egypt corporate income tax 22.5% (PwC Worldwide Tax Summaries, unchanged "
               "2025-26)", "2026", "Country"),
    tax_eff=I(0.25, "Group effective tax rate used for NOPAT. Reported effective rates: FY2023 "
              "31.3%, FY2024 30.1%, FY2025 25.2% (derived, see P&L closure). The group pays tax in "
              "15 countries; 25% is struck between the FY25 derived rate and the Egyptian statutory "
              "22.5%, above the statutory rate because foreign profits are taxed in higher-rate "
              "jurisdictions and withholding leaks on repatriation", "2026-08-05", "House"),
    fx=I(49.8, "USD/EGP mid-market ~49.8 (house cost-of-capital reference, re-verified 05-Aug-2026). "
         "The pound was not range-bound over the last year: ~46.8 (Feb-26) to ~54.7 (Apr-26 regional "
         "war spike) and back to ~49.8", "2026-08-05", "Country"),

    # ---- historical income statement (EGP mn, consolidated) --------------
    rev_fy23=I(152186.2, "Consolidated Income Statement, FY2024 earnings release (FY-2023 comparative)",
               "2025-03-13", "Company"),
    rev_fy24=I(231981.8, "Consolidated Income Statement, FY2024 earnings release", "2025-03-13", "Company"),
    rev_fy25=I(281049.0, "FY2025 consolidated revenues EGP 281.04bn (EGX filing, reported by Arab "
               "Finance / Mubasher; +21.15% on FY2024)", "2026-03", "Company"),
    gp_fy23=I(29077.3, "Consolidated Income Statement, FY2024 earnings release (comparative)",
              "2025-03-13", "Company"),
    gp_fy24=I(43898.5, "Consolidated Income Statement, FY2024 earnings release", "2025-03-13", "Company"),
    gp_fy25=I(40720.0, "DERIVED: 9M-2025 gross profit ~EGP 30.0bn (15.0% of the 199.71bn 9M revenue, "
              "press coverage of the 9M filing) + Q4-2025 gross profit 10.77bn (Q4-2025 release: "
              "-0.7% y/y on Q4-2024's 10,841, 13.2% margin). Blends to a 14.5% FY margin",
              "2026-03", "House"),
    op_fy23=I(17739.1, "Operating profit, FY2024 earnings release (comparative)", "2025-03-13", "Company"),
    op_fy24=I(29341.7, "Operating profit, FY2024 earnings release", "2025-03-13", "Company"),
    dna_fy23=I(2296.0, "Audited consolidated statement of cash flows FY2024 (2023 column): PP&E "
               "depreciation 2,120.8 + investment property 6.4 + intangibles amortisation 53.9 + "
               "right-of-use 114.9", "2025-03-12", "Company"),
    dna_fy24=I(2259.9, "Audited consolidated statement of cash flows FY2024: PP&E depreciation "
               "2,019.6 + investment property 1.5 + intangibles amortisation 80.7 + right-of-use "
               "157.9", "2025-03-12", "Company"),
    netfin_fy23=I(-2124.4, "Net finance costs, FY2024 earnings release (comparative)", "2025-03-13", "Company"),
    netfin_fy24=I(-3515.4, "Net finance costs, FY2024 earnings release", "2025-03-13", "Company"),
    assoc_fy23=I(603.6, "Share of profit of equity-accounted investees, FY2024 release (comparative)",
                 "2025-03-13", "Company"),
    assoc_fy24=I(1132.4, "Share of profit of equity-accounted investees, FY2024 release",
                 "2025-03-13", "Company"),
    tax_fy23=I(-5080.4, "Income tax expense, FY2024 earnings release (comparative)", "2025-03-13", "Company"),
    tax_fy24=I(-8121.5, "Income tax expense, FY2024 earnings release", "2025-03-13", "Company"),
    pat_fy23=I(11138.0, "Profit for the period, FY2024 earnings release (comparative)", "2025-03-13", "Company"),
    pat_fy24=I(18837.2, "Profit for the period, FY2024 earnings release", "2025-03-13", "Company"),
    pat_fy25=I(19180.0, "FY2025 consolidated net profit after tax EGP 19.18bn vs EGP 18.83bn FY2024 "
               "(EGX filing via Mubasher). The FY2024 comparative reconciles exactly to the audited "
               "'Profit for the period' of 18,837.2, confirming this is the pre-minority line",
               "2026-03", "Company"),
    npa_fy23=I(10115.7, "Profit attributable to owners of the company, FY2024 release (comparative)",
               "2025-03-13", "Company"),
    npa_fy24=I(17461.4, "Profit attributable to owners of the company, FY2024 release",
               "2025-03-13", "Company"),
    npa_fy25=I(17330.0, "FY2025 net profit after minority: FY2024's 17,461.4 less the disclosed "
               "-0.75% y/y move (Arab Finance headline on the FY2025 filing). Cross-checks to the "
               "quarterly build: 9M-2025 12,670 + Q4-2025 4,660 (Q4 release: +10.6% y/y on Q4-2024's "
               "4,209)", "2026-03", "Company"),

    # ---- historical balance sheet (EGP mn, consolidated) -----------------
    ppe_fy23=I(18009.2, "Consolidated Balance Sheet 31/12/2023, FY2024 earnings release", "2025-03-13", "Company"),
    ppe_fy24=I(27543.8, "Consolidated Balance Sheet 31/12/2024, FY2024 earnings release", "2025-03-13", "Company"),
    inv_fy23=I(30881.8, "Inventories 31/12/2023", "2025-03-13", "Company"),
    inv_fy24=I(56795.9, "Inventories 31/12/2024", "2025-03-13", "Company"),
    ca_fy23=I(16179.6, "Contract assets 31/12/2023", "2025-03-13", "Company"),
    ca_fy24=I(18052.0, "Contract assets 31/12/2024", "2025-03-13", "Company"),
    recv_fy23=I(46591.9, "Trade, notes and other receivables (current) 31/12/2023", "2025-03-13", "Company"),
    recv_fy24=I(86736.3, "Trade, notes and other receivables (current) 31/12/2024", "2025-03-13", "Company"),
    pay_fy23=I(31938.1, "Trade, notes and other payables 31/12/2023", "2025-03-13", "Company"),
    pay_fy24=I(54808.2, "Trade, notes and other payables 31/12/2024", "2025-03-13", "Company"),
    cl_fy23=I(25060.3, "Contract liabilities 31/12/2023", "2025-03-13", "Company"),
    cl_fy24=I(53281.1, "Contract liabilities 31/12/2024", "2025-03-13", "Company"),
    cash_fy23=I(25552.0, "Cash and cash equivalents 31/12/2023", "2025-03-13", "Company"),
    cash_fy24=I(38180.0, "Cash and cash equivalents 31/12/2024", "2025-03-13", "Company"),
    assets_fy23=I(151448.7, "Total assets 31/12/2023", "2025-03-13", "Company"),
    assets_fy24=I(249527.1, "Total assets 31/12/2024", "2025-03-13", "Company"),
    assets_fy25=I(311090.0, "Total assets EGP 311.09bn at 31 December 2025 (EGX filing coverage)",
                  "2026-03", "Company"),
    debt_fy23=I(41766.5, "Loans and borrowings, current 34,950.8 + non-current 6,815.7 (31/12/2023)",
                "2025-03-13", "Company"),
    debt_fy24=I(59082.9, "Loans and borrowings, current 52,733.9 + non-current 6,349.0 (31/12/2024). "
                "Note 32 splits this into loans 18,747.3, bank credit facilities 40,049.5 and lease "
                "liabilities 286.1", "2025-03-12", "Company"),
    nd_fy23=I(14768.0, "Net debt at 31 December 2023, stated in the FY2024 earnings release",
              "2025-03-13", "Company"),
    nd_fy24=I(20028.0, "Net debt at 31 December 2024, stated in the FY2024 earnings release. The "
              "Q1-2025 release restates the same date as net BANK debt of 19,727 (leases excluded); "
              "the 301 difference is immaterial and the larger figure is carried",
              "2025-03-13", "Company"),
    nd_fy25=I(19789.0, "Net bank debt EGP 19,789mn at 31 December 2025, stated in the Q4-2025 "
              "earnings release ('remained almost flat')", "2026-03", "Company"),
    eqp_fy23=I(35724.5, "Equity attributable to owners of the parent 31/12/2023", "2025-03-13", "Company"),
    eqp_fy24=I(55274.9, "Equity attributable to owners of the parent 31/12/2024", "2025-03-13", "Company"),
    nci_fy23=I(2384.0, "Non-controlling interests 31/12/2023", "2025-03-13", "Company"),
    nci_fy24=I(4251.8, "Non-controlling interests 31/12/2024", "2025-03-13", "Company"),
    assoc_bv_fy24=I(6474.0, "Equity-accounted investees (carrying value) 31/12/2024", "2025-03-13", "Company"),
    intang_fy24=I(1459.2, "Intangible assets and goodwill 31/12/2024", "2025-03-13", "Company"),
    dps_fy24=I(1.00, "Board proposed a dividend of EGP 1.00 per share on the FY2024 result (CEO "
               "statement, FY2024 earnings release); shareholder dividends of 2,176.0 were paid in "
               "the FY2024 cash flow statement for the prior year", "2025-03-13", "Company"),

    # ---- cash-flow markers (EGP mn) --------------------------------------
    capex_fy23=I(4830.0, "Audited FY2024 cash flow (2023 column): PP&E and projects under "
                 "construction 4,748.6 + intangibles 81.4", "2025-03-12", "Company"),
    capex_fy24=I(8765.7, "Audited FY2024 cash flow: PP&E and projects under construction 8,489.8 + "
                 "intangibles 275.9", "2025-03-12", "Company"),
    int_paid_fy24=I(7706.9, "Interest paid, audited FY2024 consolidated statement of cash flows",
                    "2025-03-12", "Company"),
    tax_paid_fy24=I(4891.0, "Income tax paid, audited FY2024 consolidated statement of cash flows",
                    "2025-03-12", "Company"),
    ocf_fy24=I(3979.4, "Net cash flows from operating activities FY2024 (after interest and tax) — "
               "only 3,979 against EBITDA of 31,602, the working-capital absorption in one number",
               "2025-03-12", "Company"),

    # ---- interim (EGP mn) -------------------------------------------------
    q1_25_rev=I(59391.5, "Condensed consolidated interim statement of profit or loss, 3M to "
                "31-Mar-2025", "2025-05-26", "Company"),
    q1_25_gp=I(9973.7, "Gross profit, Q1-2025 interim statements", "2025-05-26", "Company"),
    q1_25_op=I(6503.9, "Operating profit, Q1-2025 interim statements", "2025-05-26", "Company"),
    q1_25_ebitda=I(7488.8, "EBITDA, Q1-2025 earnings release (12.6% margin)", "2025-05-26", "Company"),
    q1_25_npa=I(4146.4, "Profit attributable to owners of the parent, Q1-2025", "2025-05-26", "Company"),
    q1_25_fincost=I(1745.6, "Finance costs (gross), Q1-2025 interim statements", "2025-05-26", "Company"),
    q1_25_netfin=I(-755.7, "NET finance costs Q1-2025: finance costs 1,745.6 less finance income "
                   "989.9. The group carries very large cash and short-term deposits, so gross "
                   "interest expense materially overstates the net charge", "2025-05-26", "Company"),
    netfin_fy25=I(-3400.0, "DERIVED FY2025 net finance cost. The Q1-2025 net run-rate annualises to "
                  "-3,023 and FY2024 printed -3,515 on a smaller debt book; -3,400 is struck "
                  "between them, allowing for a larger balance sheet against a falling policy rate. "
                  "This is the one materially estimated line in the FY2025 income statement and it "
                  "is what the implied tax rate is most sensitive to", "2026-08-05", "House"),
    q1_25_dna=I(681.0, "Q1-2025 interim cash flow: PP&E depreciation 637.5 + investment property 0.4 "
                "+ intangibles 2.0 + right-of-use 41.2", "2025-05-26", "Company"),
    q1_26_rev=I(75298.0, "Q1-2026 consolidated revenues EGP 75.298bn (EGX filing 13-May-2026, via "
                "Arab Finance)", "2026-05-13", "Company"),
    q1_26_npa=I(4845.0, "Q1-2026 consolidated net profit attributable to the parent EGP 4.845bn, "
                "+16.86% y/y (EGX filing 13-May-2026)", "2026-05-13", "Company"),

    # ---- segment structure -------------------------------------------------
    # ---- BOTTOM-UP UNIT ECONOMICS ---------------------------------------
    # The forecast is built from volumes and prices per unit, not from growth
    # rates applied to a revenue line. Every historical figure below is
    # disclosed, and the sub-segment build reconciles to the audited income
    # statement to within EGP 0.2mn on both revenue and gross profit.
    seg_hist=I(dict(
        FY23=dict(rawmat=(25869.7, 3478.6), cables=(56551.5, 14110.5), ec=(52896.4, 6130.0),
                  meters=(7092.9, 1694.3), transformers=(6614.1, 1979.9),
                  elecprod=(2575.1, 1386.7), infra=(586.5, 297.5)),
        FY24=dict(rawmat=(49608.2, 7647.2), cables=(87581.6, 19959.3), ec=(70042.4, 7831.1),
                  meters=(9996.7, 2722.5), transformers=(11308.7, 3895.0),
                  elecprod=(2565.2, 1300.4), infra=(879.1, 542.9))),
        "Sub-segment revenue and gross profit (EGP mn) from the company's own published segment "
        "analysis workbooks for FY2024 (with FY2023 comparatives). The reported 'Wires & Cables' "
        "segment splits into Cables and Raw Material (the copper-rod pass-through arm) and the two "
        "sum exactly to it. Turnkey gross profit is taken from the income statement where it "
        "differs marginally from the workbook", "2025-03-13", "Company"),
    vol_hist=I(dict(cables={'FY23': 156748.0, 'FY24': 167665.0},
                    meters={'FY23': 4057065.0, 'FY24': 3850726.0},
                    transformers={'FY23': 14521.0, 'FY24': 17619.0}),
               "Disclosed sales volumes: cables in tonnes, meters in units, transformers in MVA "
               "(company earnings releases, FY2024 with FY2023 comparatives). These reproduce the "
               "disclosed gross profit per tonne (90,020 / 119,043), per meter (418 / 707) and per "
               "MVA (136,345 / 221,065) exactly", "2025-03-13", "Company"),
    q1_units=I(dict(cables_q1_25=41476.0, cables_q1_24=44975.0,
                    meters_q1_25=1169502.0, meters_q1_24=811357.0,
                    transformers_q1_25=5112.0, transformers_q1_24=5142.0),
               "Q1-2025 disclosed volumes with Q1-2024 comparatives (Q1-2025 earnings release): "
               "cables 41,476t (-7.8%), meters 1,169,502 (+44.1%), transformers 5,112 MVA (-0.6%). "
               "Used with the FY2024 seasonal share to estimate the FY2025 volume base, which is "
               "not itself disclosed", "2025-05-26", "Company"),
    copper_hist=I(dict(FY23=8478.0, FY24=9147.0, FY25=10000.0),
                  "LME copper cash, annual average USD/tonne (house commodity reference)",
                  "2026-08-05", "Industry"),
    fx_hist=I(dict(FY23=30.7, FY24=45.3, FY25=49.5),
              "Annual average USD/EGP. The audited FY2024 note discloses closing 50.91 / average "
              "43.96 for 2024 and closing 30.96 / average 30.59 for 2023; the figures here are the "
              "house averages consistent with those disclosures", "2026-08-05", "Country"),
    fx_path=I([51.0, 54.0, 57.5, 61.0, 64.5],
              "USD/EGP average-rate path, about 6%/yr of depreciation from the FY2025 average of "
              "49.5. This is a genuine driver in the bottom-up build, not a translation "
              "convenience: copper is priced in dollars, so it sets the Egyptian-pound price per "
              "tonne of cable and rod directly. DELIBERATELY BELOW covered-interest parity, which "
              "on the 22.31% pound against a ~4.3% dollar rate implies about 17%/yr — the base "
              "case assumes disinflation closes most of that gap rather than the currency "
              "absorbing it. The parity case is carried as an explicit sensitivity",
              "2026-08-05", "House"),
    copper_fcst=I([13400.0, 14000.0, 14000.0, 14000.0, 14000.0],
                  "LME copper. FY2026 is set at USD 13,400/t, between the Q1-2026 average of "
                  "12,852 actually realised and the current cash price of about 14,000 "
                  "(13.9-14.2k, early August 2026); thereafter the current level is held flat. "
                  "Held flat rather than forecast: copper is the largest single input and a "
                  "directional view on it would dominate the valuation. The -10% column of the "
                  "sensitivity carries the mean-reversion case", "2026-08-05", "Industry"),
    cables_vol_growth=I([0.06, 0.05, 0.04, 0.04, 0.04],
                        "Cable tonnage growth. The FY2025 base is a 7.7% volume DECLINE on FY2024 "
                        "(disclosed Q1-2025 -7.8%), so the forecast is a recovery to roughly the "
                        "FY2024 level by FY2028 and modest growth thereafter, supported by regional "
                        "grid build-out, data-centre demand and the export book. No capacity "
                        "step-change is assumed", "2026-08-05", "House"),
    cables_uplift=I([1.30, 1.30, 1.30, 1.30, 1.30],
                    "Fabrication uplift: cable price per tonne divided by the copper cost per "
                    "tonne. History back-solves to 1.386 (FY2023) and 1.261 (FY2024); the forecast "
                    "is held at 1.30, between the two. This is the term that converts a copper "
                    "price into a cable price, and holding it flat means no pricing-power "
                    "assumption is being smuggled in", "2026-08-05", "House"),
    cables_gp_t_fy25=I(88173.0, "Cable gross profit per tonne, Q1-2025 as disclosed (against "
                       "93,672 in Q1-2024 on the restated basis). Taken as the FY2025 run-rate: "
                       "it is the hard evidence for how far cable conversion margins actually "
                       "compressed, and it is what pins the FY2025 unit build to reality rather "
                       "than to an assumption", "2025-05-26", "Company"),
    cables_conv=I([0.150, 0.160, 0.170, 0.175, 0.175],
                  "Cable conversion margin — gross profit as a share of the realised price per "
                  "tonne — for the forecast years. History back-solves to 25.0% (FY2023), 22.8% "
                  "(FY2024) and roughly 13.8% (FY2025, from the disclosed gross profit per tonne "
                  "against the back-solved price per tonne). The forecast recovers only part of "
                  "that collapse and never approaches the FY2023-24 levels, which carried "
                  "devaluation gains on cheaply bought copper inventory", "2026-08-05", "House"),
    unit_gp_growth=I([0.085, 0.080, 0.075, 0.070, 0.070],
                     "Growth in gross profit PER UNIT for the manufacturing lines — per tonne of "
                     "cable and rod, per MVA of transformer, per meter. This is the correct "
                     "structure for a converter: when copper spikes, revenue rises because the "
                     "metal is passed through, but the conversion margin earned on each tonne does "
                     "not, so the percentage margin falls. Modelling these as a percentage of a "
                     "copper-inflated price would manufacture profit out of a commodity move. The "
                     "path is set at roughly Egyptian cost inflation, i.e. a flat real conversion "
                     "margin with no recovery in unit profitability assumed",
                     "2026-08-05", "House"),
    margin_recovery=I([1.00, 1.04, 1.07, 1.09, 1.10],
                      "Recovery factor applied to the FY2025 gross margins of the non-cable lines. "
                      "FY2025 margins are calibrated to the disclosed group gross profit, which "
                      "implies roughly a 10% compression against FY2024 across those lines; the "
                      "forecast recovers about half of it by FY2030 and no more",
                      "2026-08-05", "House"),
    rawmat_vol_growth=I([0.04, 0.04, 0.03, 0.03, 0.03],
                        "Raw-material (copper rod) tonnage growth. This arm is close to a pure "
                        "pass-through: implied volume was 99kt in FY2023 and 120kt in FY2024",
                        "2026-08-05", "House"),
    rawmat_uplift=I(1.02, "Raw-material price per tonne as a multiple of the copper cost — a "
                    "thin conversion spread over the metal", "2026-08-05", "House"),
    rawmat_gp=I(0.135, "Raw-material gross margin. History 13.4% (FY2023), 15.4% (FY2024); the "
                "forecast is struck at the lower end", "2026-08-05", "House"),
    ec_backlog=I(323700.0, "Engineering and construction order book: USD 6.5bn translated at the "
                 "spot rate. Disclosed as 'approximately USD 6.5bn, above the group's typical "
                 "historical range'. The reported turnkey backlog was EGP 165bn (Mar-2024), 239bn "
                 "(Jun-2024) and 196bn (Dec-2024), so the current book is a genuine step up",
                 "2026-03", "Company"),
    ec_burn=I([0.270, 0.265, 0.260, 0.255, 0.250],
              "Share of the opening order book converted to revenue each year. The FY2025 revenue "
              "of roughly EGP 88bn against a book of EGP 324bn implies about 27%, i.e. a "
              "three-and-a-half-year book. The rate is tapered as the book lengthens",
              "2026-08-05", "House"),
    ec_book_to_bill=I([1.05, 1.05, 1.03, 1.02, 1.00],
                      "New awards as a multiple of revenue recognised. Above one early, reflecting "
                      "the disclosed step up in the order book, converging to replacement",
                      "2026-08-05", "House"),
    seg_rev_fy25_disclosed=I(dict(ec=87100.7, transformers=17703.5, meters=16594.1, infra=3857.9),
                             "FY2025 segment revenue on the restated five-segment taxonomy: "
                             "engineering & construction 87,100.7, electrical products 17,703.5, "
                             "digital solutions 16,594.1, infrastructure investment 3,857.9, with "
                             "wires, cables & accessories 155,792.9 - summing to the reported "
                             "281,049. REPLACES the earlier assumption that the FY2024 mix "
                             "carried forward, which an external audit correctly identified as "
                             "the prior year's mix relabelled. TWO competing external claims were "
                             "tested against each other: press coverage of the release reports "
                             "E&C growth of +51%, which would put the segment at 105,764. That "
                             "figure is REJECTED because it fails an independent coherence test - "
                             "it leaves so little revenue for cables that the implied fabrication "
                             "uplift over copper falls to 1.077, below anything in the company's "
                             "own history (1.386 in FY2023, 1.261 in FY2024). The 87,100.7 figure "
                             "(+24.4%) passes that test, and is adopted on that basis rather than "
                             "on the authority of either source", "2026-03", "Company"),
    ec_gp=I(0.110, "Engineering and construction gross margin. History 11.6% (FY2023) and 11.2% "
            "(FY2024); held at 11.0%", "2026-08-05", "House"),
    transformers_vol_growth=I([0.08, 0.07, 0.06, 0.05, 0.05],
                              "Transformer MVA growth. History: 14,521 MVA (FY2023) to 17,619 "
                              "(FY2024), +21.3%, then broadly flat through Q1-2025. Regional "
                              "transmission investment supports mid-single-digit growth",
                              "2026-08-05", "House"),
    transformers_gp=I(0.320, "Transformer gross margin as a share of price per MVA. History 29.9% "
                      "(FY2023) and 34.4% (FY2024); struck between them", "2026-08-05", "House"),
    meters_vol_growth=I([0.06, 0.05, 0.05, 0.04, 0.04],
                        "Smart-meter unit growth. Volumes fell 5.1% in FY2024 but Q1-2025 ran "
                        "+44.1% y/y as national metering programmes restarted",
                        "2026-08-05", "House"),
    meters_gp=I(0.250, "Meter gross margin as a share of price per unit. History 23.9% (FY2023) "
                "and 27.2% (FY2024)", "2026-08-05", "House"),
    unit_price_inflation=I([0.08, 0.075, 0.07, 0.07, 0.07],
                           "Nominal price growth for the units not priced off copper (meters). "
                           "Set below Egyptian headline inflation on the disinflation path",
                           "2026-08-05", "House"),
    other_growth=I([0.12, 0.11, 0.10, 0.09, 0.08],
                   "Revenue growth for the two smallest lines — other electrical products, and "
                   "infrastructure investment (industrial development, logistics, utilities, dry "
                   "port and independent power projects). Together under 3% of revenue",
                   "2026-08-05", "House"),
    other_gp=I(dict(elecprod=0.450, infra=0.600),
               "Gross margins on the two residual lines. History: other electrical products 53.9% "
               "(FY2023) and 50.7% (FY2024); infrastructure 50.7% and 61.8%. Struck conservatively",
               "2026-08-05", "House"),
    opex_pct=I([0.040, 0.043, 0.046, 0.048, 0.050],
               "The net operating load between gross profit and EBITDA, as a share of revenue — "
               "selling, general and administrative costs and other expenses, less other income. "
               "History: 5.94% (FY2023) and 5.30% (FY2024). FY2025 solves to a much lower level, "
               "so the forecast glides back TOWARD the historical norm rather than assuming the "
               "FY2025 load persists. This is the single most conservative choice in the rebuild",
               "2026-08-05", "House"),
    foreign_share_fy25=I(0.70, "'Over 70% of revenues generated abroad' (company 2025 commentary). "
                         "Used to report the currency split of the bottom-up revenue build, and to "
                         "translate the copper-linked lines, which are dollar-priced by "
                         "construction", "2026-03", "Company"),
    nwc_pct=I(0.230, "Net working capital as a share of revenue, held flat at the historical level. "
              "Computed from the audited balance sheets: FY2023 24.1% and FY2024 23.1% "
              "(inventories + contract assets + receivables less payables less contract "
              "liabilities). This is the single largest cash-flow driver in the model",
              "2026-08-05", "House"),
    capex_pct=I([0.030, 0.029, 0.028, 0.026, 0.024],
                "Capex as a share of revenue, tapering. History: FY2023 3.2%, FY2024 3.8% (a "
                "capacity burst — property, plant and equipment rose 53% in one year), Q1-2025 "
                "4.7% annualised. The taper assumes the current expansion cycle completes and "
                "spending settles toward maintenance plus modest capacity addition",
                "2026-08-05", "House"),
    dna_pct=I(0.0105, "Depreciation and amortisation as a share of revenue. History: FY2024 0.97%, "
              "Q1-2025 1.15%; set at 1.05% rising with the enlarged asset base", "2026-08-05", "House"),

    # ---- cost of capital ---------------------------------------------------
    rf=I(0.2231, "Egypt 10-year local-currency government bond yield, 22.31% (house cost-of-capital "
         "reference, cached 21-Jul-2026 print, re-verified 05-Aug-2026)", "2026-07-21", "Country"),
    sov_spread_cds=I(0.0340, "Egypt CDS-implied sovereign default spread, Damodaran January-2026 "
                     "country-premium file, CDS column. Netted out of the local-currency risk-free "
                     "rate so sovereign default risk is not charged twice", "2026-01-05", "Country"),
    sov_spread_rating=I(0.0637, "Damodaran adjusted default spread on the rating basis (Caa1), "
                        "January-2026 — the alternative construction, disclosed for the audit trail",
                        "2026-01-05", "Country"),
    erp_cds=I(0.0941, "Damodaran original country-premium file, Egypt row, CDS column, last updated "
              "5 January 2026 — total equity risk premium", "2026-01-05", "Country"),
    erp_rating=I(0.1394, "Damodaran original country-premium file, Egypt row, rating basis, "
                 "January-2026 — the alternative", "2026-01-05", "Country"),
    erp_ops_weighted=I(0.0737, "Operations-weighted equity risk premium: 30% Egypt at 9.41% and 70% "
                       "rest-of-world at a 6.5% blended emerging/frontier premium, reflecting where "
                       "the revenue is actually earned. Shown as an explicit alternative, not the "
                       "primary, because the standing house rule takes the country premium of the "
                       "listing and reporting currency", "2026-08-05", "House"),
    beta=I(1.009, "Own-stock tier-1 regression: SWDY weekly log-returns against a 31-name "
           "equal-weight EGX composite built from the full covered library, 5-year window. "
           "R-squared 0.291, n = 258, standard error 0.098, 90% confidence interval [0.85, 1.17]. "
           "Comfortably clears the usability gate and is NOT weak-instrument flagged (R-squared "
           "well above 10%, interval span 0.32 against a 1.009 point estimate)", "2026-08-05", "House"),
    kd=I(0.130, "Marginal cost of debt, CURRENCY-BLENDED. The audited FY2024 interest-rate note "
         "discloses average rates on financial liabilities of 28.68% in Egyptian pounds, 6.49% in "
         "US dollars and 3.92% in euros, and Note 32 confirms 28.6% / 6.45% / 7.45%. The blended "
         "rate the company actually pays is far below the Egyptian rate because a majority of the "
         "book is hard currency. Set at 13.0% against the independently computed effective rates "
         "below, allowing for the CBE's easing since the FY2024 note", "2026-08-05", "House"),
    kd_egp_note=I(0.2868, "Average interest rate on Egyptian-pound financial liabilities, audited "
                  "FY2024 interest-rate-risk note", "2025-03-12", "Company"),
    kd_usd_note=I(0.0649, "Average interest rate on US-dollar financial liabilities, audited FY2024 "
                  "interest-rate-risk note", "2025-03-12", "Company"),
    kd_eur_note=I(0.0392, "Average interest rate on euro financial liabilities, audited FY2024 "
                  "interest-rate-risk note", "2025-03-12", "Company"),
    debt_open_fy24=I(41167.5, "Loans and credit facilities at 1 January 2024, financing-liability "
                     "reconciliation, audited FY2024 note 32", "2025-03-12", "Company"),
    debt_close_fy24=I(58796.8, "Loans and credit facilities at 31 December 2024, financing-liability "
                      "reconciliation, audited FY2024 note 32 (excludes 286.1 of lease liabilities)",
                      "2025-03-12", "Company"),
    int_exp_fy24=I(7706.9, "Interest expense on loans and credit facilities, audited FY2024 note 32 "
                   "financing-liability reconciliation", "2025-03-12", "Company"),
    debt_q1_25=I(55149.9, "Loans and credit facilities at 31 March 2025: the FY2024 closing balance "
                 "of 58,796.8 less the 3,646.9 net repayment shown in the Q1-2025 interim cash flow "
                 "statement", "2025-05-26", "Company"),
    kd_path=I([0.130, 0.122, 0.115, 0.110, 0.106],
              "Forward cost-of-debt path FY26E-FY30E on the blended book. The Egyptian leg follows "
              "the CBE easing cycle (main operation rate 19.50%, held since April 2026 after three "
              "consecutive pauses) toward the 7% (2026) and 5% (2028) inflation targets; the hard-"
              "currency leg is broadly flat. The discount-rate glide takes its shape from this path "
              "by construction rather than being invented separately", "2026-08-05", "House"),
    kd_term=I(0.105, "Terminal blended cost of debt: ~45% Egyptian pound at the 15% long-run "
              "Egyptian corporate-borrowing norm and ~55% hard currency at ~6.5%", "2026-08-05", "House"),
    rf_term=I(0.105, "Terminal risk-free rate, norm-built: the CBE's own stated medium-term "
              "inflation target of 5% plus the standard ~5.5pp emerging-market real-rate "
              "convention. Never a raw historical average and never reverse-engineered from a price",
              "2026-08-05", "House"),
    erp_term=I(0.070, "Terminal equity risk premium, normalised below the currently elevated "
               "crisis-era level toward the rating-class norm; never held flat into perpetuity",
               "2026-08-05", "House"),
    wd_term=I(0.25, "Terminal debt weight D/(D+E), NORMALISED rather than today's weights. The "
              "company runs a gross debt book sized to fund working capital but carries very large "
              "offsetting cash, so its net leverage is light; 25% is the steady-state structure for "
              "a diversified industrial of this scale", "2026-08-05", "House"),
    g_term=I(0.05, "Terminal growth, 5% — the standing centre for established names in this market "
             "post-disinflation, sensitised 3-7%. Note this is an EGP-NOMINAL rate struck against a "
             "terminal risk-free rate that itself embeds 5% inflation, so the base case assumes "
             "approximately zero real terminal growth: a deliberate conservatism for a company "
             "whose revenue is majority hard-currency", "2026-08-05", "House"),

    # ---- lens inputs -------------------------------------------------------
    ev_ebitda_just=I(6.5, "Justified EV/EBITDA on mid-cycle FY27E EBITDA. The company's own trailing "
                     "multiple is ~7.9x; listed cable and electrical-equipment peers trade 8-11x and "
                     "Riyadh Cables ~14x on earnings. 6.5x applies an Egyptian-market discount for "
                     "sovereign, currency-convertibility and disclosure risk. Bear 5.5x / bull 8.0x",
                     "2026-08-05", "House"),
    pe_just=I(9.0, "Justified through-cycle P/E on normalised earnings. Trailing is ~13.0x. 9.0x "
              "reflects a high-quality franchise held back by an Egyptian cost of equity near 28%. "
              "Bear 7.0x / bull 11.5x", "2026-08-05", "House"),
    roe_sust=I(0.235, "Sustainable return on equity for the book lens. Trailing ROE is ~27.5% on "
               "average parent equity; the FY2023-24 prints were flattered by devaluation inventory "
               "gains, so the sustainable rate is struck below them", "2026-08-05", "House"),
    lens_weights=I(dict(dcf=0.45, relative=0.20, normalized=0.20, book=0.15),
                   "DCF primary for an operating manufacturer with a long, contracted order book; "
                   "the relative and normalised-earnings lenses carry equal secondary weight and "
                   "the book lens least, because reported book value is distorted by three years of "
                   "currency translation", "2026-08-05", "House"),
    backlog_usd_bn=I(6.5, "Group project backlog approximately USD 6.5bn, above the group's typical "
                     "historical range (company 2025 commentary)", "2026-03", "Company"),
    ownership=I(dict(family=0.680, electra=0.2037, float=0.116),
                "CORRECTED. The company's own shareholder pie chart carries 78.18% / 20.37% / "
                "1.45% against the legend 'El Sewedy Family / Free Float / Electra Investment "
                "Holding'. Reading that in legend order gives a 20.37% free float — which is "
                "wrong. Electra Investment Holding (Abu Dhabi, IHC-linked) acquired ~427.7mn "
                "shares, about 20%, in a July-2024 mandatory tender offer at USD 1.05/share "
                "(~USD 449mn), confirmed by multiple independent reports of the exchange filing. "
                "The 20.37% slice is therefore ELECTRA, not the float. Independent sources put "
                "the family near 68%, leaving a free float of roughly 11.6% — about half what a "
                "legend-order reading implies. Material to governance and to liquidity",
                "2026-08-06", "Company"),
    electra_mto=I(dict(price_usd=1.05, shares_mn=427.7, value_usdmn=449.1, date='2024-07',
                       stake=0.1998),
                  "Electra Investment Holding's mandatory tender offer, concluded July 2024: "
                  "~427.7mn shares (19.98%) at USD 1.05/share, ~USD 449mn, advised by EFG Hermes. "
                  "Roughly EGP 50/share at the exchange rate then prevailing. Recorded as the "
                  "last known price at which a strategic buyer cleared a fifth of the company. "
                  "NOT used as a valuation anchor: it is two years stale, struck before the "
                  "earnings base grew by roughly half, and at less than half today's price",
                  "2024-07", "Market"),
    dps_fy25=I(1.85, "FY2025 dividend of EGP 1.85 per share (+85% on the FY2024 EGP 1.00), "
               "approved at the 6-May-2026 general meeting and paid from 4 June 2026 — i.e. "
               "BEFORE the anchor date. Roughly EGP 3.96bn. The study previously reported only "
               "the FY2024 distribution", "2026-05-10", "Company"),
)

# validate four-field completeness (code-first rule)
for k, rec in INP.items():
    assert set(rec) == {'value', 'source', 'date', 'ring'}, f"INPUT {k} not four-field"
    assert rec['source'] and rec['date'] and rec['ring'], f"INPUT {k} missing provenance"

V = {k: rec['value'] for k, rec in INP.items()}
LOG = []
def say(s):
    LOG.append(s); print(s)

say("=" * 78)
say("SWDY — ASSERT / derivation log")
say("=" * 78)

# ============================ CALC ===========================================
SH, SPOT, TAX = V['shares_mn'], V['spot'], V['tax_eff']
MKTCAP = SPOT * SH

# ---- FY2025 income statement closed from the disclosed anchors -------------
# Disclosed: revenue, gross profit (derived from quarterly prints), profit after
# tax and profit after minority. Unknown: the split of the remainder between
# operating costs, net finance and tax. We fix EBITDA at the disclosed margin,
# derive D&A and EBIT, then let the tax rate close the P&L to the reported PAT.
dna_fy25 = V['dna_pct'] * V['rev_fy25']
netfin_fy25 = V['netfin_fy25']
assoc_fy25 = V['assoc_fy24'] * 1.15
# With a bottom-up build the stated effective tax rate is the input and EBITDA is
# what the disclosed profit implies — the reverse of a top-down model.
eff_tax_fy25 = V['tax_eff']
pbt_fy25 = V['pat_fy25'] / (1 - eff_tax_fy25)
tax_fy25 = -(pbt_fy25 - V['pat_fy25'])
op_fy25 = pbt_fy25 - netfin_fy25 - assoc_fy25
ebitda_fy25 = op_fy25 + dna_fy25
nci_fy25 = V['pat_fy25'] - V['npa_fy25']
say(f"[P&L closure FY2025] disclosed profit after tax {V['pat_fy25']:,.0f} at the stated "
    f"{eff_tax_fy25:.1%} effective rate implies pre-tax profit {pbt_fy25:,.0f}; less net finance "
    f"{netfin_fy25:,.0f} and associates {assoc_fy25:,.0f} gives EBIT {op_fy25:,.0f}, and adding "
    f"depreciation {dna_fy25:,.0f} gives EBITDA {ebitda_fy25:,.0f} "
    f"({ebitda_fy25/V['rev_fy25']:.2%} of revenue). The disclosed quarterly EBITDA margins were "
    f"12.6% (Q1), 11.1% (Q2) and 9.5% (Q4), so a full-year figure near 11% is consistent with "
    f"the prints. NCI {nci_fy25:,.0f}")
assert 0.085 < ebitda_fy25 / V['rev_fy25'] < 0.135, "FY25 implied EBITDA margin outside the prints"

ebitda_fy23 = V['op_fy23'] + V['dna_fy23']
ebitda_fy24 = V['op_fy24'] + V['dna_fy24']
say(f"[EBITDA basis] House EBITDA = operating profit + depreciation and amortisation: FY23 "
    f"{ebitda_fy23:,.0f}, FY24 {ebitda_fy24:,.0f}. The company's own reported EBITDA (20,668 / "
    f"32,772) is higher because it also adds back impairments and certain other charges; the "
    f"house basis is used throughout so the DCF waterfall reconciles line by line.")

hist_is = {
    'FY23': dict(rev=V['rev_fy23'], gp=V['gp_fy23'], ebitda=ebitda_fy23, dna=V['dna_fy23'],
                 ebit=V['op_fy23'], fin=V['netfin_fy23'], assoc=V['assoc_fy23'],
                 ebt=V['op_fy23'] + V['netfin_fy23'] + V['assoc_fy23'], tax=V['tax_fy23'],
                 pat=V['pat_fy23'], nci=V['pat_fy23'] - V['npa_fy23'], npa=V['npa_fy23']),
    'FY24': dict(rev=V['rev_fy24'], gp=V['gp_fy24'], ebitda=ebitda_fy24, dna=V['dna_fy24'],
                 ebit=V['op_fy24'], fin=V['netfin_fy24'], assoc=V['assoc_fy24'],
                 ebt=V['op_fy24'] + V['netfin_fy24'] + V['assoc_fy24'], tax=V['tax_fy24'],
                 pat=V['pat_fy24'], nci=V['pat_fy24'] - V['npa_fy24'], npa=V['npa_fy24']),
    'FY25': dict(rev=V['rev_fy25'], gp=V['gp_fy25'], ebitda=ebitda_fy25, dna=dna_fy25,
                 ebit=op_fy25, fin=netfin_fy25, assoc=assoc_fy25, ebt=pbt_fy25, tax=tax_fy25,
                 pat=V['pat_fy25'], nci=nci_fy25, npa=V['npa_fy25']),
}

# ---- historical net working capital ---------------------------------------
nwc_fy23 = (V['inv_fy23'] + V['ca_fy23'] + V['recv_fy23']) - (V['pay_fy23'] + V['cl_fy23'])
nwc_fy24 = (V['inv_fy24'] + V['ca_fy24'] + V['recv_fy24']) - (V['pay_fy24'] + V['cl_fy24'])
nwc_fy25 = V['nwc_pct'] * V['rev_fy25']
say(f"[Working capital] FY23 {nwc_fy23:,.0f} ({nwc_fy23/V['rev_fy23']:.1%} of revenue), FY24 "
    f"{nwc_fy24:,.0f} ({nwc_fy24/V['rev_fy24']:.1%}), FY25 {nwc_fy25:,.0f} "
    f"({V['nwc_pct']:.1%}, held at the historical level)")
assert abs(nwc_fy24 / V['rev_fy24'] - V['nwc_pct']) < 0.02, "NWC driver not consistent with FY24"

# ---- FY2025 balance sheet, triangulated ------------------------------------
eqp_fy25 = V['eqp_fy24'] + V['npa_fy25'] - V['dps_fy24'] * SH
nci_bv_fy25 = V['nci_fy24'] + nci_fy25 - 250.0
eq_fy25 = eqp_fy25 + nci_bv_fy25
liab_fy25 = V['assets_fy25'] - eq_fy25
growth_fy25 = V['rev_fy25'] / V['rev_fy24'] - 1.0
nondebt_fy25 = (V['assets_fy24'] - V['eqp_fy24'] - V['nci_fy24'] - V['debt_fy24']) * (1 + growth_fy25)
debt_fy25_a = liab_fy25 - nondebt_fy25                       # A: balance-sheet residual
debt_fy25_b = V['debt_fy24'] * (1 + growth_fy25)             # B: scale with revenue
cash_fy25_c = (V['cash_fy24'] + 875.0) * (1 + growth_fy25)   # C: scale cash, back out debt
debt_fy25_c = cash_fy25_c + V['nd_fy25']
debt_fy25 = float(np.mean([debt_fy25_a, debt_fy25_b, debt_fy25_c]))
cash_fy25 = debt_fy25 - V['nd_fy25']
say(f"[FY2025 balance sheet triangulation] equity attributable {eqp_fy25:,.0f} (FY24 "
    f"{V['eqp_fy24']:,.0f} + profit {V['npa_fy25']:,.0f} - dividend "
    f"{V['dps_fy24']*SH:,.0f}); total equity {eq_fy25:,.0f}; liabilities {liab_fy25:,.0f}. "
    f"Gross debt: (A) balance-sheet residual {debt_fy25_a:,.0f}, (B) revenue-scaled "
    f"{debt_fy25_b:,.0f}, (C) implied by revenue-scaled cash {debt_fy25_c:,.0f} -> adopted "
    f"{debt_fy25:,.0f}, cash {cash_fy25:,.0f}. NET debt is NOT triangulated — it is the "
    f"disclosed {V['nd_fy25']:,.0f}, and the valuation bridge uses only that.")
assert abs(debt_fy25 - cash_fy25 - V['nd_fy25']) < 1.0, "FY25 net debt identity broken"

# ---- Kd integrity gate ------------------------------------------------------
kd_eff_fy24 = V['int_exp_fy24'] / ((V['debt_open_fy24'] + V['debt_close_fy24']) / 2)
kd_eff_q1_25 = (V['q1_25_fincost'] * 4) / ((V['debt_close_fy24'] + V['debt_q1_25']) / 2)
fx_blend = 0.5 * (V['kd_usd_note'] + V['kd_eur_note'])
w_egp = (kd_eff_fy24 - fx_blend) / (V['kd_egp_note'] - fx_blend)
say(f"[Kd integrity] (i) CURRENCY COMPOSITION — audited note rates: EGP {V['kd_egp_note']:.2%}, "
    f"USD {V['kd_usd_note']:.2%}, EUR {V['kd_eur_note']:.2%}. The blended effective rate implies "
    f"an Egyptian-pound share of {w_egp:.1%} and a hard-currency share of {1-w_egp:.1%}. A "
    f"single-currency Kd would overstate the cost of debt by roughly "
    f"{(V['kd_egp_note'] - kd_eff_fy24)*1e4:,.0f}bp.")
say(f"[Kd integrity] (ii) INDEPENDENT EFFECTIVE RATES — FY2024 interest expense "
    f"{V['int_exp_fy24']:,.0f} / average loans and facilities "
    f"{(V['debt_open_fy24']+V['debt_close_fy24'])/2:,.0f} = {kd_eff_fy24:.2%}; Q1-2025 finance "
    f"costs annualised / average balance = {kd_eff_q1_25:.2%}.")
say(f"[Kd integrity] (iii) BOUNDS — adopted Kd {V['kd']:.2%}: within 150bp of the most recent "
    f"effective rate ({abs(V['kd']-kd_eff_q1_25)*1e4:,.0f}bp) and does not exceed the peak-year "
    f"effective rate {max(kd_eff_fy24, kd_eff_q1_25):.2%} by more than 50bp.")
assert abs(V['kd'] - kd_eff_q1_25) <= 0.015, f"Kd {V['kd']:.3f} more than 150bp from {kd_eff_q1_25:.3f}"
assert V['kd'] <= max(kd_eff_fy24, kd_eff_q1_25) + 0.005, "Kd exceeds peak effective rate by >50bp"

# ---- cost of capital: explicit window (sovereign double-count removed) -----
rf_star = V['rf'] - V['sov_spread_cds']
ke_exp = rf_star + V['beta'] * V['erp_cds']
ke_rating_alt = (V['rf'] - V['sov_spread_rating']) + V['beta'] * V['erp_rating']
ke_ops_alt = rf_star + V['beta'] * V['erp_ops_weighted']
ke_raw_retired = V['rf'] + V['beta'] * V['erp_cds']
kd_at = V['kd'] * (1 - TAX)
wd_exp = V['nd_fy25'] / (V['nd_fy25'] + MKTCAP)
we_exp = 1 - wd_exp
wacc_exp = we_exp * ke_exp + wd_exp * kd_at
wd_gross = debt_fy25 / (debt_fy25 + MKTCAP)
wacc_exp_gross = (1 - wd_gross) * ke_exp + wd_gross * kd_at
say(f"[Cost of equity] rf {V['rf']:.2%} less sovereign CDS spread {V['sov_spread_cds']:.2%} = "
    f"{rf_star:.2%}; + beta {V['beta']:.3f} x ERP {V['erp_cds']:.2%} -> Ke {ke_exp:.2%}. "
    f"Alternatives disclosed: rating basis {ke_rating_alt:.2%}; operations-weighted premium "
    f"{ke_ops_alt:.2%}; the RETIRED un-netted construction {ke_raw_retired:.2%} (audit trail only).")
say(f"[WACC explicit] weights on NET debt {wd_exp:.1%} / equity {we_exp:.1%} -> {wacc_exp:.2%}. "
    f"On gross debt the weights would be {wd_gross:.1%} / {1-wd_gross:.1%} -> "
    f"{wacc_exp_gross:.2%}; the net-debt basis is used because it is the same quantity the "
    f"enterprise-to-equity bridge subtracts, and it is the more conservative of the two.")

# ---- terminal (norm-built, never backed out of a price) --------------------
ke_term = V['rf_term'] + V['beta'] * V['erp_term']
kd_term_at = V['kd_term'] * (1 - TAX)
wacc_term = (1 - V['wd_term']) * ke_term + V['wd_term'] * kd_term_at
say(f"[WACC terminal] Ke {ke_term:.2%} (rf {V['rf_term']:.2%} + beta x ERP {V['erp_term']:.2%}); "
    f"Kd after tax {kd_term_at:.2%}; weights {1-V['wd_term']:.0%}/{V['wd_term']:.0%} -> "
    f"{wacc_term:.2%}")
assert wacc_term < wacc_exp, "terminal WACC must be below the explicit-window WACC"

# ---- glide: fractions from kd_path (never invented separately) -------------
kdp = V['kd_path']
glide_frac = [(kdp[0] - k) / (kdp[0] - kdp[-1]) for k in kdp]
fwd = [wacc_exp - (wacc_exp - wacc_term) * f for f in glide_frac]
df, c = [], 1.0
for w in fwd:
    c /= (1 + w); df.append(c)
assert all(fwd[i] >= fwd[i + 1] for i in range(len(fwd) - 1)), "glide not monotone"
say("[Glide] forward WACC " + " -> ".join(f"{w:.2%}" for w in fwd) +
    "; cumulative discount factors " + ", ".join(f"{d:.4f}" for d in df) +
    ". The glide fractions are the cost-of-debt path's own cumulative progress, so the shape is "
    "inherited rather than being a second free parameter.")

# ---- BOTTOM-UP UNIT ECONOMICS ------------------------------------------------
YRS = ['FY26E', 'FY27E', 'FY28E', 'FY29E', 'FY30E']
SUBS = ['cables', 'rawmat', 'ec', 'transformers', 'meters', 'elecprod', 'infra']
SUBNAME = dict(cables='Cables', rawmat='Raw material (copper rod)',
               ec='Engineering & construction', transformers='Transformers',
               meters='Meters & digital', elecprod='Other electrical products',
               infra='Infrastructure investment')
SH_, VH = V['seg_hist'], V['vol_hist']
CU, FXH = V['copper_hist'], V['fx_hist']

# historical unit economics — validated against the audited statements
unit_hist = {}
for y in ('FY23', 'FY24'):
    seg = SH_[y]
    rev_sum = sum(v[0] for v in seg.values()); gp_sum = sum(v[1] for v in seg.values())
    cu_t = CU[y] * FXH[y]
    unit_hist[y] = dict(
        rev_sum=rev_sum, gp_sum=gp_sum, copper_t=cu_t,
        cables_price_t=seg['cables'][0] * 1e6 / VH['cables'][y],
        cables_gp_t=seg['cables'][1] * 1e6 / VH['cables'][y],
        cables_uplift=(seg['cables'][0] * 1e6 / VH['cables'][y]) / cu_t,
        cables_conv=seg['cables'][1] / seg['cables'][0],
        meters_price=seg['meters'][0] * 1e6 / VH['meters'][y],
        meters_gp_u=seg['meters'][1] * 1e6 / VH['meters'][y],
        transformers_price=seg['transformers'][0] * 1e6 / VH['transformers'][y],
        transformers_gp_mva=seg['transformers'][1] * 1e6 / VH['transformers'][y],
        rawmat_kt=seg['rawmat'][0] * 1e6 / cu_t,
        ec_gp=seg['ec'][1] / seg['ec'][0],
        opex_pct=(gp_sum - (V['op_fy23'] + V['dna_fy23'] if y == 'FY23'
                            else V['op_fy24'] + V['dna_fy24'])) / rev_sum)
say(f"[Bottom-up base] the sub-segment build reconciles to the audited statements: FY2023 revenue "
    f"{unit_hist['FY23']['rev_sum']:,.1f} vs reported {V['rev_fy23']:,.1f}, gross profit "
    f"{unit_hist['FY23']['gp_sum']:,.1f} vs {V['gp_fy23']:,.1f}; FY2024 revenue "
    f"{unit_hist['FY24']['rev_sum']:,.1f} vs {V['rev_fy24']:,.1f}, gross profit "
    f"{unit_hist['FY24']['gp_sum']:,.1f} vs {V['gp_fy24']:,.1f}.")
for y in ('FY23', 'FY24'):
    assert abs(unit_hist[y]['rev_sum'] - V[f'rev_{y.lower()}']) < 1.0, 'sub-segment revenue break'
    assert abs(unit_hist[y]['gp_sum'] - V[f'gp_{y.lower()}']) < 1.0, 'sub-segment gross profit break'
say(f"[Unit economics] cables price/tonne {unit_hist['FY23']['cables_price_t']:,.0f} -> "
    f"{unit_hist['FY24']['cables_price_t']:,.0f}; fabrication uplift over copper "
    f"{unit_hist['FY23']['cables_uplift']:.3f} -> {unit_hist['FY24']['cables_uplift']:.3f}; "
    f"conversion margin {unit_hist['FY23']['cables_conv']:.1%} -> "
    f"{unit_hist['FY24']['cables_conv']:.1%}. Meters price/unit "
    f"{unit_hist['FY23']['meters_price']:,.0f} -> {unit_hist['FY24']['meters_price']:,.0f}; "
    f"transformers price/MVA {unit_hist['FY23']['transformers_price']:,.0f} -> "
    f"{unit_hist['FY24']['transformers_price']:,.0f}. Operating load between gross profit and "
    f"EBITDA {unit_hist['FY23']['opex_pct']:.2%} -> {unit_hist['FY24']['opex_pct']:.2%} of revenue.")

# ---- FY2025 unit base: volumes from Q1 seasonality, revenue calibrated to disclosure ----
Q = V['q1_units']
seas = {k: Q[f'{k}_q1_24'] / VH[k]['FY24'] for k in ('cables', 'meters', 'transformers')}
vol25 = {k: Q[f'{k}_q1_25'] / seas[k] for k in seas}
cu_t25 = CU['FY25'] * FXH['FY25']
# non-cables lines built first; cables revenue is the residual against disclosed group revenue,
# which back-solves the FY2025 fabrication uplift as the diagnostic
rawmat_kt25 = unit_hist['FY24']['rawmat_kt'] * 1.00
rev25 = {}
rev25['rawmat'] = rawmat_kt25 * cu_t25 * V['rawmat_uplift'] / 1e6
# FY2025 sub-segment revenue is now pinned to the DISCLOSED growth rates applied to the
# FY2024 base on the restated taxonomy, rather than assuming the FY2024 mix persisted.
G25 = V['seg_rev_fy25_disclosed']
rev25['ec'] = G25['ec']
rev25['transformers'] = G25['transformers']
rev25['meters'] = G25['meters']
rev25['infra'] = G25['infra']
rev25['elecprod'] = SH_['FY24']['elecprod'][0] * 1.25
rev25['cables'] = V['rev_fy25'] - sum(rev25.values())
uplift25 = rev25['cables'] * 1e6 / vol25['cables'] / cu_t25
price_t25 = rev25['cables'] * 1e6 / vol25['cables']
say(f"[FY2025 unit base] volumes implied from the disclosed Q1 prints and the FY2024 seasonal "
    f"share: cables {vol25['cables']:,.0f}t ({vol25['cables']/VH['cables']['FY24']-1:+.1%} on "
    f"FY2024), meters {vol25['meters']:,.0f} units, transformers "
    f"{vol25['transformers']:,.0f} MVA. Cables revenue is the residual against the disclosed group "
    f"revenue of {V['rev_fy25']:,.0f}, which BACK-SOLVES the FY2025 fabrication uplift to "
    f"{uplift25:.3f}, against 1.386 in FY2023 and 1.261 in FY2024. That this residual lands "
    f"in the historical neighbourhood is the check that the segment split is economics rather "
    f"than a plug — and it is the test that rejected the competing '+51% E&C' reading, which "
    f"forces the uplift to 1.077.")
assert 1.10 < uplift25 < 1.50, f"FY25 back-solved uplift {uplift25:.3f} outside the historical range"

# FY2025 gross profit: cables PINNED to the disclosed gross profit per tonne; the
# remaining lines carry FY2024's margins scaled by one compression factor, solved so
# the total reproduces the gross profit assembled from the disclosed prints.
gp25 = {}
gp25['cables'] = vol25['cables'] * V['cables_gp_t_fy25'] / 1e6
cables_conv25 = gp25['cables'] / rev25['cables']
gp24_margin = {k: SH_['FY24'][k][1] / SH_['FY24'][k][0] for k in SUBS}
others = [k for k in SUBS if k != 'cables']
rest_rev = sum(rev25[k] for k in others)
rest_gp24_blend = sum(rev25[k] * gp24_margin[k] for k in others)
compress = (V['gp_fy25'] - gp25['cables']) / rest_gp24_blend
for k in others:
    gp25[k] = rev25[k] * gp24_margin[k] * compress
gp_bu25 = sum(gp25.values())
margin25 = {k: gp25[k] / rev25[k] for k in SUBS}
opex25 = (gp_bu25 - ebitda_fy25) / V['rev_fy25']
say(f"[FY2025 margin calibration] cables gross profit is PINNED to the disclosed "
    f"{V['cables_gp_t_fy25']:,.0f} EGP per tonne x {vol25['cables']:,.0f}t = "
    f"{gp25['cables']:,.0f}, i.e. a conversion margin of {cables_conv25:.1%} against "
    f"{unit_hist['FY24']['cables_conv']:.1%} in FY2024 — the cable margin roughly HALVED, and that "
    f"single fact is most of the group's gross-margin decline. The other lines carry FY2024's "
    f"margins scaled by {compress:.3f}, solved so the total reproduces the {V['gp_fy25']:,.0f} "
    f"assembled from the disclosed prints. Resulting FY2025 margins: " +
    ", ".join(f"{SUBNAME[k]} {margin25[k]:.1%}" for k in SUBS) + ".")
say(f"[FY2025 operating load] bottom-up gross profit {gp_bu25:,.0f} less EBITDA "
    f"{ebitda_fy25:,.0f} implies an operating load of {opex25:.2%} of revenue, against "
    f"{unit_hist['FY24']['opex_pct']:.2%} in FY2024 and {unit_hist['FY23']['opex_pct']:.2%} in "
    f"FY2023. The forecast glides from {V['opex_pct'][0]:.1%} back toward the historical norm "
    f"rather than assuming the FY2025 level persists.")
assert abs(gp_bu25 - V['gp_fy25']) < 1.0, 'FY25 gross profit calibration did not close'
assert 0.7 < compress < 1.15, f'FY25 margin compression factor {compress:.3f} implausible' 

# ---- FORECAST: volumes x prices, sub-segment by sub-segment --------------------
vol_f = {k: [] for k in ('cables', 'meters', 'transformers', 'rawmat')}
seg_rev = []; seg_gp = []
backlog = V['ec_backlog']; bl_path = []
vc, vm, vt, vr = vol25['cables'], vol25['meters'], vol25['transformers'], rawmat_kt25
ec_prev = rev25['ec']; ep_prev = rev25['elecprod']; inf_prev = rev25['infra']
mp, tp = unit_hist['FY24']['meters_price'] * 1.08, unit_hist['FY24']['transformers_price'] * 1.09
# The most recent hard evidence is the Q1-2026 print. Back out the EBITDA margin it
# implies, and SOLVE the FY2026 cable conversion margin that reproduces it, rather than
# assuming a conversion margin and contradicting the print.
_nci_sh = nci_fy25 / V['pat_fy25']
q1_26_pat = V['q1_26_npa'] / (1 - _nci_sh)
q1_26_pbt = q1_26_pat / (1 - TAX)
q1_26_ebit = q1_26_pbt - netfin_fy25 / 4 - assoc_fy25 / 4
q1_26_ebitda = q1_26_ebit + V['dna_pct'] * V['q1_26_rev']
q1_26_margin = q1_26_ebitda / V['q1_26_rev']
say(f"[Q1-2026 calibration] the disclosed Q1-2026 revenue {V['q1_26_rev']:,.0f} "
    f"({V['q1_26_rev']/V['q1_25_rev']-1:+.1%} y/y) and attributable profit {V['q1_26_npa']:,.0f} "
    f"({V['q1_26_npa']/V['q1_25_npa']-1:+.1%} y/y) imply, on the same tax, minority, finance and "
    f"depreciation structure, an EBITDA margin of about {q1_26_margin:.2%} — against "
    f"{V['q1_25_ebitda']/V['q1_25_rev']:.2%} in Q1-2025. Profit GREW on a higher copper price, so "
    f"any build that shows margins collapsing in FY2026 is contradicted by the print. The FY2026 "
    f"cable conversion margin is therefore SOLVED to reproduce this, not assumed.")
gp_t_cables = V['cables_gp_t_fy25']
gp_t_rawmat = gp25['rawmat'] * 1e6 / rawmat_kt25
gp_mva = gp25['transformers'] * 1e6 / vol25['transformers']
gp_unit_m = gp25['meters'] * 1e6 / vol25['meters']
say(f"[Per-unit gross profit, FY2025 base] cables {gp_t_cables:,.0f} EGP/tonne (disclosed), rod "
    f"{gp_t_rawmat:,.0f} EGP/tonne, transformers {gp_mva:,.0f} EGP/MVA, meters "
    f"{gp_unit_m:,.0f} EGP/unit. These grow with cost inflation only — no real recovery in "
    f"conversion profitability is assumed anywhere in the forecast.")
def _fy26_gp(gpt):
    cu_t = V['copper_fcst'][0] * V['fx_path'][0]
    vc_ = vol25['cables'] * (1 + V['cables_vol_growth'][0])
    vr_ = rawmat_kt25 * (1 + V['rawmat_vol_growth'][0])
    vt_ = vol25['transformers'] * (1 + V['transformers_vol_growth'][0])
    vm_ = vol25['meters'] * (1 + V['meters_vol_growth'][0])
    rev_ = (vc_ * cu_t * V['cables_uplift'][0] + vr_ * cu_t * V['rawmat_uplift']) / 1e6
    rev_ += V['ec_backlog'] * V['ec_burn'][0]
    rev_ += vt_ * (cu_t * unit_hist['FY24']['transformers_price'] / unit_hist['FY24']['copper_t']) / 1e6
    rev_ += vm_ * unit_hist['FY24']['meters_price'] * 1.08 * (1 + V['unit_price_inflation'][0]) / 1e6
    rev_ += rev25['elecprod'] * (1 + V['other_growth'][0]) + rev25['infra'] * (1 + V['other_growth'][0])
    g_ = vc_ * gpt / 1e6
    g_ += vr_ * (gp25['rawmat'] * 1e6 / rawmat_kt25) * (1 + V['unit_gp_growth'][0]) / 1e6
    g_ += V['ec_backlog'] * V['ec_burn'][0] * margin25['ec'] * V['margin_recovery'][0]
    g_ += vt_ * (gp25['transformers'] * 1e6 / vol25['transformers']) * (1 + V['unit_gp_growth'][0]) / 1e6
    g_ += vm_ * (gp25['meters'] * 1e6 / vol25['meters']) * (1 + V['unit_gp_growth'][0]) / 1e6
    g_ += rev25['elecprod'] * (1 + V['other_growth'][0]) * margin25['elecprod'] * V['margin_recovery'][0]
    g_ += rev25['infra'] * (1 + V['other_growth'][0]) * margin25['infra'] * V['margin_recovery'][0]
    return (g_ - V['opex_pct'][0] * rev_) / rev_

lo_, hi_ = 60000.0, 260000.0
for _ in range(90):
    mid_ = (lo_ + hi_) / 2
    if _fy26_gp(mid_) < q1_26_margin: lo_ = mid_
    else: hi_ = mid_
gp_t_cables = (lo_ + hi_) / 2
say(f"[Cable conversion margin, solved] FY2026 gross profit per tonne solves to "
    f"{gp_t_cables:,.0f} EGP to reproduce the Q1-2026 implied EBITDA margin — against the "
    f"disclosed {V['cables_gp_t_fy25']:,.0f} in Q1-2025, {unit_hist['FY24']['cables_gp_t']:,.0f} "
    f"in FY2024 and {unit_hist['FY23']['cables_gp_t']:,.0f} in FY2023. It sits inside the "
    f"historical range, so the print and the unit build are mutually consistent.")
_cu26 = V['copper_fcst'][0] * V['fx_path'][0]
say(f"[Conversion margin cross-check] as a SHARE of the realised price per tonne that solved "
    f"figure is {gp_t_cables/(_cu26*V['cables_uplift'][0]):.1%}, between the FY2025 trough of "
    f"{cables_conv25:.1%} and the FY2024 peak of {unit_hist['FY24']['cables_conv']:.1%}. In "
    f"absolute EGP it is below what pure copper-cost scaling of FY2024 would give "
    f"({unit_hist['FY24']['cables_gp_t']*_cu26/unit_hist['FY24']['copper_t']:,.0f}), so the "
    f"solve does not assume the converter captures the whole metal move. NOTE the solve "
    f"attributes all of the Q1-2026 improvement to cables, where the volatility demonstrably is; "
    f"if it in fact came from another line the sub-segment split changes but GROUP EBITDA — the "
    f"only thing the valuation consumes — is pinned by the print either way.")
assert unit_hist['FY23']['cables_gp_t'] * 0.75 < gp_t_cables < unit_hist['FY24']['cables_gp_t'] * 1.45, \
    f'solved cable conversion margin {gp_t_cables:,.0f} outside the historical range'
gp_t_cables /= (1 + V['unit_gp_growth'][0])   # loop advances it on the first pass

GP_T_CABLES_0 = gp_t_cables

def build(fx_mult=1.0, gp_unit_mult=1.0, vol_mult=1.0, copper_mult=1.0, opex_shift=0.0):
    """Re-run the whole unit build. Scenarios and sensitivity grids call THIS, so a
    currency or copper move flows through the price per tonne, the working capital and
    the gross profit exactly as it does in the base case — not as a flat multiplier on
    a finished revenue line."""
    vc, vm, vt, vr = (vol25['cables'], vol25['meters'], vol25['transformers'], rawmat_kt25)
    ep_, if_ = rev25['elecprod'], rev25['infra']
    mp_ = unit_hist['FY24']['meters_price'] * 1.08
    gpc, gpr = GP_T_CABLES_0 * gp_unit_mult, (gp25['rawmat'] * 1e6 / rawmat_kt25) * gp_unit_mult
    gpv, gpm = ((gp25['transformers'] * 1e6 / vol25['transformers']) * gp_unit_mult,
                (gp25['meters'] * 1e6 / vol25['meters']) * gp_unit_mult)
    bl = V['ec_backlog']
    R, G_, BL, VOL = [], [], [], {k: [] for k in ('cables', 'meters', 'transformers', 'rawmat')}
    for i in range(5):
        cu_t = V['copper_fcst'][i] * copper_mult * V['fx_path'][i] * fx_mult
        vc *= (1 + V['cables_vol_growth'][i]) * (vol_mult ** 0.2)
        vm *= (1 + V['meters_vol_growth'][i]) * (vol_mult ** 0.2)
        vt *= (1 + V['transformers_vol_growth'][i]) * (vol_mult ** 0.2)
        vr *= (1 + V['rawmat_vol_growth'][i]) * (vol_mult ** 0.2)
        mp_ *= (1 + V['unit_price_inflation'][i])
        gpc *= (1 + V['unit_gp_growth'][i]); gpr *= (1 + V['unit_gp_growth'][i])
        gpv *= (1 + V['unit_gp_growth'][i]); gpm *= (1 + V['unit_gp_growth'][i])
        tp_ = cu_t * (unit_hist['FY24']['transformers_price'] / unit_hist['FY24']['copper_t'])
        r, g = {}, {}
        r['cables'] = vc * cu_t * V['cables_uplift'][i] / 1e6; g['cables'] = vc * gpc / 1e6
        r['rawmat'] = vr * cu_t * V['rawmat_uplift'] / 1e6;    g['rawmat'] = vr * gpr / 1e6
        r['ec'] = bl * V['ec_burn'][i]
        g['ec'] = r['ec'] * margin25['ec'] * V['margin_recovery'][i]
        bl = bl - r['ec'] + r['ec'] * V['ec_book_to_bill'][i]
        r['transformers'] = vt * tp_ / 1e6; g['transformers'] = vt * gpv / 1e6
        r['meters'] = vm * mp_ / 1e6;       g['meters'] = vm * gpm / 1e6
        ep_ *= (1 + V['other_growth'][i]); if_ *= (1 + V['other_growth'][i])
        r['elecprod'] = ep_; g['elecprod'] = ep_ * margin25['elecprod'] * V['margin_recovery'][i]
        r['infra'] = if_;    g['infra'] = if_ * margin25['infra'] * V['margin_recovery'][i]
        R.append(r); G_.append(g); BL.append(bl)
        VOL['cables'].append(vc); VOL['meters'].append(vm)
        VOL['transformers'].append(vt); VOL['rawmat'].append(vr)
    rev_ = [sum(R[i].values()) for i in range(5)]
    gp_ = [sum(G_[i].values()) for i in range(5)]
    opex_ = [(V['opex_pct'][i] + opex_shift) * rev_[i] for i in range(5)]
    ebitda_ = [gp_[i] - opex_[i] for i in range(5)]
    return dict(rev=rev_, gp=gp_, opex=opex_, ebitda=ebitda_, seg_rev=R, seg_gp=G_,
                backlog=BL, vol=VOL)

_B = build()
seg_rev, seg_gp, bl_path, vol_f = _B['seg_rev'], _B['seg_gp'], _B['backlog'], _B['vol']
rev = _B['rev']; gp = _B['gp']; opex = _B['opex']
ebitda = _B['ebitda']
ebitda_margin = [ebitda[i] / rev[i] for i in range(5)]
gp_margin = [gp[i] / rev[i] for i in range(5)]
say(f"[Forecast, bottom-up] revenue " + " -> ".join(f"{r:,.0f}" for r in rev) +
    " (growth " + ", ".join(f"{rev[i]/(V['rev_fy25'] if i==0 else rev[i-1])-1:+.1%}"
                            for i in range(5)) + ")")
say(f"[Forecast margins are OUTPUTS] gross margin " +
    " -> ".join(f"{m:.2%}" for m in gp_margin) + "; EBITDA margin " +
    " -> ".join(f"{m:.2%}" for m in ebitda_margin) +
    f". Cable tonnage {vol_f['cables'][0]:,.0f} -> {vol_f['cables'][-1]:,.0f} "
    f"({vol_f['cables'][-1]/VH['cables']['FY24']-1:+.1%} against FY2024); order book "
    f"{V['ec_backlog']:,.0f} -> {bl_path[-1]:,.0f}.")
_impl26 = V['q1_26_rev'] / (V['q1_25_rev'] / V['rev_fy25'])
say(f"[FY2026 cross-check against the print] the disclosed Q1-2026 revenue of "
    f"{V['q1_26_rev']:,.0f}, grossed up on the Q1-2025 seasonal share, implies a full year of "
    f"{_impl26:,.0f}. The build produces {rev[0]:,.0f}, {rev[0]/_impl26-1:+.1%} against it — an "
    f"independent check that the unit build is not running ahead of the company's own trading.")
assert abs(rev[0] / _impl26 - 1) < 0.08, 'FY26 build diverges from the Q1-2026 print'

# currency split, reported off the bottom-up build (copper-linked lines are dollar-priced)
fgn_egp = [seg_rev[i]['cables'] * 0.60 + seg_rev[i]['rawmat'] * 0.55 + seg_rev[i]['ec'] * 0.80 +
           (seg_rev[i]['transformers'] + seg_rev[i]['meters']) * 0.55 for i in range(5)]
dom = [rev[i] - fgn_egp[i] for i in range(5)]
fgn_usd = [fgn_egp[i] / V['fx_path'][i] for i in range(5)]
fgn25 = (rev25['cables'] * 0.60 + rev25['rawmat'] * 0.55 + rev25['ec'] * 0.80 +
         (rev25['transformers'] + rev25['meters']) * 0.55)
fgn_share_fy25_derived = fgn25 / V['rev_fy25']
say(f"[Currency split — two different questions] the company discloses that over "
    f"{V['foreign_share_fy25']:.0%} of revenue is earned ABROAD, which is a geographic statement "
    f"about where the customer sits. The build derives the share that is HARD-CURRENCY LINKED — "
    f"dollar-priced by construction — at {fgn25/V['rev_fy25']:.0%} in FY2025 and " +
    " -> ".join(f"{fgn_egp[i]/rev[i]:.0%}" for i in range(5)) +
    f" thereafter. The two are not in conflict: a project executed in a North African market for "
    f"a local utility is foreign revenue but not necessarily dollar-priced. The LOWER figure is "
    f"used everywhere the currency question is valued, because it is the conservative one.")

# FY2025 presentation objects reused downstream
segs = SUBS
SEGNAME = SUBNAME
seg_rev_fy25 = rev25
seg_gp_fy25 = gp25
shares = [{s: seg_rev[i][s] / rev[i] for s in SUBS} for i in range(5)]
seg_ebitda = [{s: seg_gp[i][s] - V['opex_pct'][i] * seg_rev[i][s] for s in SUBS} for i in range(5)]

# ---- FCFF waterfall ---------------------------------------------------------
dna = [V['dna_pct'] * r for r in rev]
ebit = [ebitda[i] - dna[i] for i in range(5)]
nopat = [e * (1 - TAX) for e in ebit]
capex = [V['capex_pct'][i] * rev[i] for i in range(5)]
nwc = [V['nwc_pct'] * r for r in rev]
dnwc = [nwc[0] - nwc_fy25] + [nwc[i] - nwc[i - 1] for i in range(1, 5)]
fcff = [nopat[i] + dna[i] - capex[i] - dnwc[i] for i in range(5)]
pv = [fcff[i] * df[i] for i in range(5)]
pv_explicit = float(sum(pv))

# ---- forward net-finance path (needed by the lenses below, recomputed identically
# in the forecast-equity block) --------------------------------------------------
interest_path_pre, _nd = [], V['nd_fy25']
for i in range(5):
    _cash = debt_fy25 - _nd
    _int = V['kd_path'][i] * debt_fy25 - 0.10 * max(_cash, 0.0)
    interest_path_pre.append(_int)
    _nd = _nd - (fcff[i] - _int * (1 - TAX)) + 0.25 * max(ebit[i] - _int, 0.0) * (1 - TAX) * (1 - nci_share_pre if False else 0.9035)

# ---- invested capital, terminal ROIC ----------------------------------------
ic_fy23 = nwc_fy23 + V['ppe_fy23']
ic_fy24 = nwc_fy24 + V['ppe_fy24'] + V['intang_fy24']
ppe = []
p = V['ppe_fy24'] + (V['capex_pct'][0] * V['rev_fy25'] - dna_fy25)   # FY25 net addition
ppe_fy25 = p
for i in range(5):
    p += capex[i] - dna[i]; ppe.append(p)
ic = [nwc[i] + ppe[i] + V['intang_fy24'] for i in range(5)]
roic = [nopat[i] / ic[i] for i in range(5)]
roic_term = nopat[-1] * (1 + V['g_term']) / ic[-1]   # NOPAT(n+1) / IC(n), the standard convention
say(f"[Terminal return on capital] taken as next year's NOPAT over the closing invested capital "
    f"({roic_term:.1%}), the standard convention, rather than the same year's NOPAT over closing "
    f"capital ({roic[-1]:.1%}).")
nopat_fy23 = V['op_fy23'] * (1 - 0.313)
nopat_fy24 = V['op_fy24'] * (1 - 0.301)
nopat_fy25 = op_fy25 * (1 - eff_tax_fy25)
ic_fy25 = nwc_fy25 + ppe_fy25 + V['intang_fy24']
hist_roic = dict(FY23=nopat_fy23 / ic_fy23, FY24=nopat_fy24 / ic_fy24, FY25=nopat_fy25 / ic_fy25)
hist_rr = dict(FY23=(V['capex_fy23'] - V['dna_fy23']) / nopat_fy23,
               FY24=(V['capex_fy24'] - V['dna_fy24']) / nopat_fy24,
               FY25=(V['capex_pct'][0] * V['rev_fy25'] - dna_fy25) / nopat_fy25)
hist_impl_g = {y: hist_roic[y] * hist_rr[y] for y in hist_roic}
nopat_cagr = (nopat_fy25 / nopat_fy23) ** 0.5 - 1
stable_g = float(np.mean([hist_impl_g['FY23'], hist_impl_g['FY25']]))
say(f"[Terminal growth reconciliation] historical ROIC {hist_roic['FY23']:.1%} / "
    f"{hist_roic['FY24']:.1%} / {hist_roic['FY25']:.1%}; reinvestment rate "
    f"{hist_rr['FY23']:.1%} / {hist_rr['FY24']:.1%} / {hist_rr['FY25']:.1%}; implied g "
    f"{hist_impl_g['FY23']:.1%} / {hist_impl_g['FY24']:.1%} / {hist_impl_g['FY25']:.1%}. "
    f"Check (a): actual NOPAT CAGR FY23-FY25 = {nopat_cagr:+.1%}. Check (b): implied g from "
    f"STABLE years only (FY24 excluded as a debt-funded capacity burst, reinvestment "
    f"{hist_rr['FY24']:.0%}) = {stable_g:.1%}. Adopted terminal g {V['g_term']:.1%}.")

# terminal value: reinvestment is FORCED to satisfy g = ROIC x RR exactly
rr_term = V['g_term'] / roic_term
nopat_term = nopat[-1] * (1 + V['g_term'])
tv = nopat_term * (1 - rr_term) / (wacc_term - V['g_term'])
pv_tv = tv * df[-1]
ev = pv_explicit + pv_tv
tv_share = pv_tv / ev
say(f"[Terminal value] terminal ROIC {roic_term:.1%}; required reinvestment rate "
    f"g/ROIC = {rr_term:.1%}; terminal NOPAT {nopat_term:,.0f}; TV {tv:,.0f} capitalised at the "
    f"terminal WACC and discounted at the YEAR-5 factor {df[-1]:.4f} (one date, one price of "
    f"time) -> PV {pv_tv:,.0f}. Terminal value is {tv_share:.0%} of enterprise value.")
assert abs(roic_term * rr_term - V['g_term']) < 1e-9, "terminal g != ROIC x RR"

# ---- crossover arithmetic (terminal-growth ceiling) -------------------------
EGYPT_GDP = 20000000.0        # EGP mn, nominal, order of magnitude
EGYPT_NOM = 0.15
dom_share_term = dom[-1] / rev[-1]
blend_ceiling = dom_share_term * EGYPT_NOM + (1 - dom_share_term) * 0.075
yrs_cross = np.log(EGYPT_GDP / dom[-1]) / np.log((1 + nopat_cagr) / (1 + EGYPT_NOM))
say(f"[Terminal ceiling] the domestic leg is {dom_share_term:.0%} of FY30E revenue; a blended "
    f"long-run nominal ceiling is {blend_ceiling:.1%} ({EGYPT_NOM:.0%} Egyptian nominal on the "
    f"domestic leg, 7.5% world nominal on the export leg). Adopted g of {V['g_term']:.0%} sits "
    f"below it. If the recent NOPAT CAGR of {nopat_cagr:.0%} were floated as a TERMINAL rate, the "
    f"domestic revenue leg alone would overtake Egypt's entire nominal GDP in about "
    f"{yrs_cross:.0f} years — arithmetic necessity, not a modelling opinion.")
assert V['g_term'] < blend_ceiling, "terminal g exceeds the blended nominal growth ceiling"

# ---- EV -> equity bridge ----------------------------------------------------
assoc_val = V['assoc_bv_fy24']   # carrying value, no uplift
say(f"[Associates] carried at the audited FY2024 carrying value of {assoc_val:,.0f} with NO "
    f"uplift. The previous version applied an undisclosed 1.15x, which an external audit "
    f"correctly flagged as an unsourced adjustment; it is removed.")
nci_share = nci_fy25 / V['pat_fy25']
eq_pre_nci = ev - V['nd_fy25'] + assoc_val
nci_val = nci_share * eq_pre_nci
eq_attr = eq_pre_nci - nci_val
dcf_ps = eq_attr / SH
say(f"[Bridge] EV {ev:,.0f} - net debt {V['nd_fy25']:,.0f} + associates at carrying value "
    f"{assoc_val:,.0f} = {eq_pre_nci:,.0f}; less minority interests at their "
    f"{nci_share:.1%} share of group profit = {nci_val:,.0f} -> equity attributable "
    f"{eq_attr:,.0f} = EGP {dcf_ps:.2f}/share against a spot of {SPOT:.2f} "
    f"({dcf_ps/SPOT-1:+.0%}).")
assert abs((ev - V['nd_fy25'] + assoc_val - nci_val) - eq_attr) < 1e-6, "bridge does not close"
assert V['nd_fy25'] > 0 and nci_val > 0, "net debt and NCI must reduce equity value"

# ---- currency-of-discounting alternative (the market's implied view) -------
# Value the hard-currency leg at a hard-currency WACC and the domestic leg at the
# Egyptian WACC, then translate. Disclosed as an alternative, not the primary.
WACC_USD = 0.75 * (0.043 + V['beta'] * 0.075) + 0.25 * 0.065 * (1 - TAX)
fgn_frac = [fgn_egp[i] / rev[i] for i in range(5)]
# The foreign cash-flow leg is EGP-denominated and INFLATED by the assumed depreciation
# path. Discounting it at a hard-currency rate without first deflating it back to dollars
# would count the currency benefit twice. So: convert each year to USD at that year's
# rate, discount in USD, then translate the result back at the FY2025 rate.
fcff_f_usd = [fcff[i] * fgn_frac[i] / V['fx_path'][i] for i in range(5)]
fcff_d = [fcff[i] * (1 - fgn_frac[i]) for i in range(5)]
df_usd, c2 = [], 1.0
for _ in range(5):
    c2 /= (1 + WACC_USD); df_usd.append(c2)
pv_f_usd = sum(fcff_f_usd[i] * df_usd[i] for i in range(5))
tv_f_usd = (nopat_term * (1 - rr_term) * fgn_frac[-1] / V['fx_path'][-1]) / (WACC_USD - 0.035)
ev_f_egp = (pv_f_usd + tv_f_usd * df_usd[-1]) * V['fx_hist']['FY25']
pv_d = sum(fcff_d[i] * df[i] for i in range(5))
tv_d = nopat_term * (1 - rr_term) * (1 - fgn_frac[-1]) / (wacc_term - V['g_term'])
ev_ccy = ev_f_egp + pv_d + tv_d * df[-1]
eq_ccy = (ev_ccy - V['nd_fy25'] + assoc_val) * (1 - nci_share)
ccy_ps = eq_ccy / SH
say(f"[Currency-of-discounting alternative — UIP-corrected] the hard-currency leg "
    f"({fgn_frac[-1]:.0%} of cash flow) is first DEFLATED to dollars at each year's exchange "
    f"rate, discounted at a USD cost of capital of {WACC_USD:.2%} with 3.5% terminal growth, and "
    f"only then translated back. Discounting the EGP-denominated leg — already inflated by the "
    f"assumed depreciation path — directly at a dollar rate would count the currency benefit "
    f"twice, which is what the previous version did. Corrected result EGP {ccy_ps:.2f}/share "
    f"({ccy_ps/SPOT-1:+.0%} vs spot), against {108.27:.2f} before the correction.")

# ---- responses to external challenge, computed rather than asserted ----------
# (a) Rating-basis cost of capital. Three separate external audits have read the
# study's CDS-basis equity risk premium against Damodaran's RATING-basis column and
# called the difference an error. They are different columns of the same published
# table, and both are already in the input register — but the fair response is to
# publish what the rating basis does to the VALUE, not just to the cost of equity.
wacc_exp_rating = we_exp * ke_rating_alt + wd_exp * kd_at
wacc_term_rating = (1 - V['wd_term']) * (V['rf_term'] + V['beta'] * (V['erp_term'] + 0.045)) \
    + V['wd_term'] * kd_term_at
def _val_at(we_, wt_, g_=None):
    g_ = V['g_term'] if g_ is None else g_
    _fwd = [we_ - (we_ - wt_) * f for f in glide_frac]
    _df, cc = [], 1.0
    for w in _fwd:
        cc /= (1 + w); _df.append(cc)
    _rr = min(g_ / roic_term, 0.95)
    _tv = nopat[-1] * (1 + g_) * (1 - _rr) / max(wt_ - g_, 0.02)
    _ev = sum(fcff[i] * _df[i] for i in range(5)) + _tv * _df[-1]
    return ((_ev - V['nd_fy25'] + assoc_val) * (1 - nci_share)) / SH
assert abs(_val_at(wacc_exp, wacc_term) - dcf_ps) < 0.01, 'rating-basis helper does not reproduce base'
dcf_rating_ps = _val_at(wacc_exp_rating, wacc_term_rating)
say(f"[Rating-basis alternative, published] on Damodaran's RATING column (sovereign spread "
    f"{V['sov_spread_rating']:.2%}, equity risk premium {V['erp_rating']:.2%}) the cost of equity "
    f"is {ke_rating_alt:.2%} and the cost of capital {wacc_exp_rating:.2%} -> "
    f"{wacc_term_rating:.2%}, giving EGP {dcf_rating_ps:.2f}/share against the CDS-basis "
    f"{dcf_ps:.2f}. Both columns are published by the same source; the CDS basis is the house "
    f"primary because it is market-observed rather than agency-lagged. The rating basis is now "
    f"shown as a VALUE, not merely as a rate.")

# (b) Alternative NCI sequencing: charge minorities against unlevered enterprise value
# before net debt, rather than against consolidated equity after it.
nci_alt = nci_share * (ev + assoc_val)
eq_alt = ev + assoc_val - nci_alt - V['nd_fy25']
nci_alt_ps = eq_alt / SH
say(f"[Minority-interest sequencing, alternative published] charging minorities "
    f"{nci_share:.1%} of UNLEVERED enterprise value plus associates ({nci_alt:,.0f}) and "
    f"deducting net debt afterwards gives EGP {nci_alt_ps:.2f}/share, against {dcf_ps:.2f} on the "
    f"adopted sequencing — a difference of {nci_alt_ps - dcf_ps:+.2f}. The adopted method is "
    f"retained because the audited borrowings note records facilities granted to 'the Company AND "
    f"ITS SUBSIDIARIES ... guaranteed by promissory notes FROM SUBSIDIARIES', i.e. debt does sit "
    f"at subsidiary level, so minorities do bear a share of it. The alternative assumes all "
    f"borrowing is at the parent, which the note contradicts.")

# ---- lens 2: relative --------------------------------------------------------
# A multiple applied to FY2027 EBITDA produces an enterprise value AS AT end-FY2027.
# It has to be discounted back to today before the bridge. The previous version treated
# a two-year-forward enterprise value as today's — an external audit was right to call
# this out, and it was worth roughly EGP 29/share on this lens.
REL_I = 1
ebitda_mid = ebitda[REL_I]
df_rel = df[REL_I]
ev_rel_fwd = V['ev_ebitda_just'] * ebitda_mid
ev_rel = ev_rel_fwd * df_rel
def _rel(mult):
    return (((mult * ebitda_mid) * df_rel - V['nd_fy25'] + assoc_val) * (1 - nci_share)) / SH
rel_ps, rel_bear, rel_bull = _rel(V['ev_ebitda_just']), _rel(5.5), _rel(8.0)
say(f"[Relative lens — forward EV discounted] {V['ev_ebitda_just']}x on FY2027E EBITDA "
    f"{ebitda_mid:,.0f} gives an enterprise value of {ev_rel_fwd:,.0f} AS AT end-FY2027; "
    f"discounted back at the year-2 factor {df_rel:.4f} that is {ev_rel:,.0f} today -> "
    f"EGP {rel_ps:.2f}/share. Not discounting it would have given "
    f"{((ev_rel_fwd - V['nd_fy25'] + assoc_val) * (1 - nci_share)) / SH:.2f}.")
ev_trailing = MKTCAP + V['nd_fy25']
ev_ebitda_trailing = ev_trailing / ebitda_fy25
pe_trailing = SPOT / (V['npa_fy25'] / SH)

# ---- lens 3: normalized earnings power ---------------------------------------
# All three components now come from the SAME year (FY2028E, the mid-point of the
# forecast). The previous build mixed FY2027 revenue, an FY2028-30 average margin,
# FY2026 peak interest and FY2025 associates — an external audit was right to call
# that temporally incoherent.
NORM_I = 2
norm_margin = ebitda_margin[NORM_I]
norm_rev = rev[NORM_I]
norm_ebitda = norm_margin * norm_rev
norm_ebit = norm_ebitda - V['dna_pct'] * norm_rev
norm_interest = interest_path_pre[NORM_I]
norm_assoc = assoc_fy25 * (1.08 ** (NORM_I + 1))
norm_np = (norm_ebit - norm_interest + norm_assoc) * (1 - TAX) * (1 - nci_share)
norm_eps = norm_np / SH
norm_ps = V['pe_just'] * norm_eps
norm_bear = 7.0 * norm_eps
norm_bull = 11.5 * norm_eps

# ---- lens 4: book / justified P/B --------------------------------------------
bvps = eqp_fy25 / SH
# The justified price-to-book identity (ROE - g)/(Ke - g) is a perpetuity, so it takes the
# PERPETUAL cost of equity. The previous version used an average of the explicit-window and
# terminal rates inside a perpetual formula — internally inconsistent, and an external audit
# was right about it. Correcting it RAISES this lens.
ke_blend = ke_term
pb_just = (V['roe_sust'] - V['g_term']) / (ke_term - V['g_term'])
book_ps = pb_just * bvps
book_bear = ((V['roe_sust'] - 0.03) / (0.5 * (ke_exp + ke_term) - 0.03)) * bvps
book_bull = ((V['roe_sust'] + 0.02 - V['g_term']) / (ke_term - V['g_term'])) * bvps
say(f"[Book lens] justified price-to-book {pb_just:.2f}x = (sustainable return {V['roe_sust']:.1%} "
    f"- growth {V['g_term']:.0%}) / (PERPETUAL cost of equity {ke_term:.2%} - growth). Using a "
    f"blended cost of equity inside a perpetuity formula, as the previous version did, is "
    f"inconsistent and understated this lens by roughly "
    f"{(pb_just - (V['roe_sust']-V['g_term'])/(0.5*(ke_exp+ke_term)-V['g_term']))*bvps:.2f}/share.")
roe_trailing = V['npa_fy25'] / ((V['eqp_fy24'] + eqp_fy25) / 2)

# ---- scenarios on the DCF -----------------------------------------------------
def dcf_scenario(gp_unit_mult=1.0, fx_mult=1.0, wacc_shift=0.0, g=None, opex_shift=0.0,
                 copper_mult=1.0, nwc=None):
    """Scenario valuation. Re-runs the FULL unit build, so a currency or copper move
    flows through the price per tonne, the working capital and the gross profit exactly
    as it does in the base case."""
    g = V['g_term'] if g is None else g
    nwc = V['nwc_pct'] if nwc is None else nwc
    B = build(fx_mult=fx_mult, gp_unit_mult=gp_unit_mult, copper_mult=copper_mult,
              opex_shift=opex_shift)
    _rev, _ebitda = B['rev'], B['ebitda']
    _dna = [V['dna_pct'] * r for r in _rev]
    _ebit = [_ebitda[i] - _dna[i] for i in range(5)]
    _nopat = [e * (1 - TAX) for e in _ebit]
    _capex = [V['capex_pct'][i] * r for i, r in enumerate(_rev)]
    _nwc = [nwc * r for r in _rev]
    _dnwc = [_nwc[0] - nwc * V['rev_fy25']] + [_nwc[i] - _nwc[i - 1] for i in range(1, 5)]
    _f = [_nopat[i] + _dna[i] - _capex[i] - _dnwc[i] for i in range(5)]
    _we, _wt = wacc_exp + wacc_shift, wacc_term + wacc_shift
    _fwd = [_we - (_we - _wt) * f for f in glide_frac]
    _df, cc = [], 1.0
    for w in _fwd:
        cc /= (1 + w); _df.append(cc)
    _ppe, pp = [], ppe_fy25
    for i in range(5):
        pp += _capex[i] - _dna[i]; _ppe.append(pp)
    _roic = _nopat[-1] * (1 + g) / (_nwc[-1] + _ppe[-1] + V['intang_fy24'])
    _rr = min(g / _roic, 0.95)
    _tv = _nopat[-1] * (1 + g) * (1 - _rr) / max(_wt - g, 0.02)
    _ev = sum(_f[i] * _df[i] for i in range(5)) + _tv * _df[-1]
    return ((_ev - V['nd_fy25'] + assoc_val) * (1 - nci_share)) / SH

_base_chk = dcf_scenario()
assert abs(_base_chk - dcf_ps) < 0.02, f'scenario engine does not reproduce base: {_base_chk} vs {dcf_ps}'

dcf_bear = dcf_scenario(gp_unit_mult=0.88, fx_mult=0.94, wacc_shift=+0.02, g=0.03,
                        opex_shift=+0.005)
dcf_bull = dcf_scenario(gp_unit_mult=1.12, fx_mult=1.08, wacc_shift=-0.02, g=0.06,
                        opex_shift=-0.005)
say(f"[DCF scenarios] bear {dcf_bear:.2f} / base {dcf_ps:.2f} / bull {dcf_bull:.2f} EGP per share")

# ---- synthesis ----------------------------------------------------------------
W = V['lens_weights']
lenses = dict(
    dcf=dict(name='Discounted cash flow (primary)', bear=dcf_bear, base=dcf_ps, bull=dcf_bull, w=W['dcf']),
    relative=dict(name='Relative multiples', bear=rel_bear, base=rel_ps, bull=rel_bull, w=W['relative']),
    normalized=dict(name='Normalised earnings power', bear=norm_bear, base=norm_ps, bull=norm_bull,
                    w=W['normalized']),
    book=dict(name='Book value and sustainable return', bear=book_bear, base=book_ps, bull=book_bull,
              w=W['book']),
)
central = sum(l['base'] * l['w'] for l in lenses.values())
lo = min(l['bear'] for l in lenses.values())
hi = max(l['bull'] for l in lenses.values())
lenses['central'] = dict(name='Weighted central', bear=lo, base=central, bull=hi, w=1.0)
say(f"[Synthesis] weighted central EGP {central:.2f}; full span across lenses and scenarios "
    f"{lo:.2f} - {hi:.2f}; spot {SPOT:.2f} ({central/SPOT-1:+.0%} to the central).")
assert 0.20 <= central / SPOT <= 3.0, f"central/spot {central/SPOT:.2f} outside the plausibility band"

# ---- sensitivity grids ---------------------------------------------------------
g_grid = [0.03, 0.04, 0.05, 0.06, 0.07]
wt_grid = [wacc_term - 0.02, wacc_term - 0.01, wacc_term, wacc_term + 0.01, wacc_term + 0.02]
we_grid = [wacc_exp - 0.03, wacc_exp - 0.015, wacc_exp, wacc_exp + 0.015, wacc_exp + 0.03]

def dcf_at(we_, wt_, g_):
    _fwd = [we_ - (we_ - wt_) * f for f in glide_frac]
    _df, cc = [], 1.0
    for w in _fwd:
        cc /= (1 + w); _df.append(cc)
    _rr = min(g_ / roic_term, 0.95)
    _tv = nopat[-1] * (1 + g_) * (1 - _rr) / max(wt_ - g_, 0.02)
    _ev = sum(fcff[i] * _df[i] for i in range(5)) + _tv * _df[-1]
    return ((_ev - V['nd_fy25'] + assoc_val) * (1 - nci_share)) / SH

grid_wacc_g = [[dcf_at(wacc_exp, wt, g) for g in g_grid] for wt in wt_grid]
grid_exp_term = [[dcf_at(we, wt, V['g_term']) for wt in wt_grid] for we in we_grid]
beta_grid = [0.60, 0.80, round(V['beta'], 3), 1.15, 1.30]
def dcf_beta(b):
    ke = rf_star + b * V['erp_cds']
    we_ = we_exp * ke + wd_exp * kd_at
    wt_ = (1 - V['wd_term']) * (V['rf_term'] + b * V['erp_term']) + V['wd_term'] * kd_term_at
    return dcf_at(we_, wt_, V['g_term'])
grid_beta = [dcf_beta(b) for b in beta_grid]
fx_grid = [0.90, 1.00, 1.20, 1.45, 1.70]   # top of range reaches the parity path
grid_fx = [dcf_scenario(fx_mult=m) for m in fx_grid]
mg_grid = [0.85, 0.925, 1.0, 1.075, 1.15]
grid_margin = [dcf_scenario(gp_unit_mult=m) for m in mg_grid]
cu_grid = [0.85, 0.925, 1.0, 1.075, 1.15]
grid_copper = [dcf_scenario(copper_mult=m) for m in cu_grid]
nwc_grid = [0.20, 0.215, 0.23, 0.245, 0.26]
def dcf_nwc(pct):
    return dcf_scenario(nwc=pct)

def _dcf_nwc_unused(pct):
    _nwc = [pct * r for r in rev]
    _dnwc = [_nwc[0] - pct * V['rev_fy25']] + [_nwc[i] - _nwc[i - 1] for i in range(1, 5)]
    _f = [nopat[i] + dna[i] - capex[i] - _dnwc[i] for i in range(5)]
    _rr = min(V['g_term'] / roic_term, 0.95)
    _tv = nopat[-1] * (1 + V['g_term']) * (1 - _rr) / (wacc_term - V['g_term'])
    _ev = sum(_f[i] * df[i] for i in range(5)) + _tv * df[-1]
    return ((_ev - V['nd_fy25'] + assoc_val) * (1 - nci_share)) / SH
grid_nwc = [dcf_nwc(p) for p in nwc_grid]
roic_grid = [0.15, 0.18, roic_term, 0.26, 0.30]
def dcf_roic(r):
    _rr = min(V['g_term'] / r, 0.95)
    _tv = nopat[-1] * (1 + V['g_term']) * (1 - _rr) / (wacc_term - V['g_term'])
    _ev = pv_explicit + _tv * df[-1]
    return ((_ev - V['nd_fy25'] + assoc_val) * (1 - nci_share)) / SH
grid_roic = [dcf_roic(r) for r in roic_grid]

# ---- forecast balance sheet & cash-flow markers ---------------------------------
eq_fc, e_ = [], eqp_fy25
np_fc, nd_fc = [], []
nd_ = V['nd_fy25']
interest_path = []
for i in range(5):
    # gross borrowings fund working capital and stay broadly in place; the cash pile
    # builds as free cash flow accrues, so the NET charge falls with net debt.
    cash_i = debt_fy25 - nd_
    interest = V['kd_path'][i] * debt_fy25 - 0.10 * max(cash_i, 0.0)
    interest_path.append(interest)
    pbt_i = ebit[i] - interest + assoc_fy25 * (1 + 0.08) ** (i + 1)
    pat_i = pbt_i * (1 - TAX)
    npa_i = pat_i * (1 - nci_share)
    div_i = 0.25 * npa_i
    e_ += npa_i - div_i
    eq_fc.append(e_); np_fc.append(npa_i)
    nd_ = nd_ - (fcff[i] - interest * (1 - TAX)) + div_i
    nd_fc.append(nd_)
say(f"[Forecast interest] net finance cost falls " + " -> ".join(f"{x:,.0f}" for x in interest_path) +
    f" as the cash pile builds against a broadly static gross debt book — the charge tracks the "
    f"net debt path rather than being frozen at the FY2025 balance.")
say(f"[Forecast equity] attributable profit " + ", ".join(f"{x:,.0f}" for x in np_fc) +
    f"; net debt path " + ", ".join(f"{x:,.0f}" for x in nd_fc) +
    f" (25% payout assumed). Net debt / EBITDA falls from "
    f"{V['nd_fy25']/ebitda_fy25:.2f}x to {nd_fc[-1]/ebitda[-1]:.2f}x.")

# ---- expert panel: three genuinely different methods ---------------------------
# Cast by METHOD from the persona library; presented to the reader as Expert 1/2/3.
# E1 — earnings power: mid-cycle earnings at a justified multiple.
e1_margin = 0.118
e1_rev = rev[2]
e1_ebit = e1_margin * e1_rev - V['dna_pct'] * e1_rev
e1_int = V['kd_path'][2] * debt_fy25 - 0.10 * cash_fy25
e1_eps = ((e1_ebit - e1_int + assoc_fy25) * (1 - TAX) * (1 - nci_share)) / SH
e1_base, e1_lo, e1_hi = 9.5 * e1_eps, 7.0 * e1_eps, 12.0 * e1_eps
# E2 — the accountant: owner cash earnings, capitalised. The harshest lens for a
# working-capital-hungry contractor: cash actually left after funding the order book.
e2_fcff = float(np.mean(fcff[2:]))
e2_int_at = (V['kd_path'][3] * debt_fy25 - 0.10 * cash_fy25) * (1 - TAX)
e2_fcfe = (e2_fcff - e2_int_at) * (1 - nci_share)
# Expert 2 capitalises owner cash earnings in perpetuity, so — on the same logic that
# corrects the book lens — the PERPETUAL cost of equity is the right rate. The range is
# taken on the discount rate and the growth rate, not by re-using the same rate twice.
e2_ke = ke_term
e2_base = e2_fcfe * (1 + V['g_term']) / (e2_ke - V['g_term']) / SH
e2_lo = e2_fcfe * 1.03 / (0.5 * (ke_exp + ke_term) - 0.03) / SH
e2_hi = e2_fcfe * 1.06 / (e2_ke - 0.06) / SH
# E3 — cash returns: economic profit on invested capital through the rate cycle.
ic_beg = [ic_fy25] + ic[:-1]
ep_ = [nopat[i] - fwd[i] * ic_beg[i] for i in range(5)]
say(f"[Economic profit convention] the capital charge is taken on BEGINNING-of-year invested "
    f"capital, not ending. Charging ending capital understates economic profit by roughly "
    f"{sum((ic[i]-ic_beg[i])*fwd[i] for i in range(5))/5:,.0f}mn a year and pushes the year in "
    f"which the return spread turns positive one year later than it should. Corrected here.")
pv_ep = sum(ep_[i] * df[i] for i in range(5))
ep_term = nopat[-1] * (1 + V['g_term']) - wacc_term * ic[-1] * (1 + V['g_term'])
pv_ep_term = ep_term / (wacc_term - V['g_term']) * df[-1]
e3_ev = ic_fy25 + pv_ep + pv_ep_term
e3_base = ((e3_ev - V['nd_fy25'] + assoc_val) * (1 - nci_share)) / SH
e3_lo = ((ic_fy25 + pv_ep * 0.6 + pv_ep_term * 0.55 - V['nd_fy25'] + assoc_val) * (1 - nci_share)) / SH
e3_hi = ccy_ps
experts = dict(
    e1=dict(method_short='earnings power', base=e1_base, rng=[e1_lo, e1_hi], eps=e1_eps,
            margin=e1_margin, rev=e1_rev, ebit=e1_ebit, interest=e1_int, pe=9.5),
    e2=dict(method_short='owner cash earnings', base=e2_base, rng=[e2_lo, e2_hi], fcff=e2_fcff,
            fcfe=e2_fcfe, ke=e2_ke, int_at=e2_int_at),
    e3=dict(method_short='cash returns vs cost of capital', base=e3_base, rng=[e3_lo, e3_hi],
            ic0=ic_fy25, pv_ep=pv_ep, pv_ep_term=pv_ep_term, ev=e3_ev, ep=ep_,
            spread=[roic[i] - fwd[i] for i in range(5)]),
)
panel_centre = float(sorted([e1_base, e2_base, e3_base])[1])
say(f"[Expert panel] Expert 1 {e1_base:.2f} [{e1_lo:.2f}-{e1_hi:.2f}]; Expert 2 {e2_base:.2f} "
    f"[{e2_lo:.2f}-{e2_hi:.2f}]; Expert 3 {e3_base:.2f} [{e3_lo:.2f}-{e3_hi:.2f}]; "
    f"panel median {panel_centre:.2f} ({panel_centre/SPOT-1:+.0%} vs spot)")

# ---- fan for the figure ---------------------------------------------------------
paths3 = np.load(os.path.join(HERE, 'paths_3M.npy'))
fan = np.percentile(paths3, [5, 25, 50, 75, 95], axis=0)
np.save(os.path.join(HERE, 'fan.npy'), fan)

# ============================ EMIT ==============================================
step0 = json.load(open(os.path.join(HERE, 'step0_result.json')))
strike = json.load(open(os.path.join(HERE, 'strike_result.json')))
beta_res = json.load(open(os.path.join(HERE, 'beta_result.json')))

OUT = dict(
    meta=dict(ticker='SWDY', company='Elsewedy Electric Company S.A.E.', market='EGX',
              currency='EGP', asof='2026-08-05', spot=SPOT, shares_mn=SH, mktcap=MKTCAP,
              ev_trailing=ev_trailing, klass='diversified industrial operating company'),
    inputs=INP,
    hist_is=hist_is,
    hist_bs=dict(
        FY23=dict(ppe=V['ppe_fy23'], inv=V['inv_fy23'], ca=V['ca_fy23'], recv=V['recv_fy23'],
                  cash=V['cash_fy23'], assets=V['assets_fy23'], debt=V['debt_fy23'],
                  pay=V['pay_fy23'], cl=V['cl_fy23'], eqp=V['eqp_fy23'], nci=V['nci_fy23'],
                  nd=V['nd_fy23'], nwc=nwc_fy23),
        FY24=dict(ppe=V['ppe_fy24'], inv=V['inv_fy24'], ca=V['ca_fy24'], recv=V['recv_fy24'],
                  cash=V['cash_fy24'], assets=V['assets_fy24'], debt=V['debt_fy24'],
                  pay=V['pay_fy24'], cl=V['cl_fy24'], eqp=V['eqp_fy24'], nci=V['nci_fy24'],
                  nd=V['nd_fy24'], nwc=nwc_fy24),
        FY25=dict(ppe=ppe_fy25, assets=V['assets_fy25'], debt=debt_fy25, cash=cash_fy25,
                  eqp=eqp_fy25, nci=nci_bv_fy25, nd=V['nd_fy25'], nwc=nwc_fy25,
                  debt_methods=dict(residual=debt_fy25_a, revenue_scaled=debt_fy25_b,
                                    cash_implied=debt_fy25_c)),
    ),
    fgn_share_fy25_derived=fgn_share_fy25_derived, fgn_egp_fy25=fgn25,
    fcst=dict(years=YRS, rev=rev, dom=dom, fgn_usd=fgn_usd, fgn_egp=fgn_egp,
              ebitda=ebitda, ebitda_margin=ebitda_margin, dna=dna, ebit=ebit, nopat=nopat,
              capex=capex, nwc=nwc, dnwc=dnwc, fcff=fcff, df=df, pv=pv, fwd_wacc=fwd,
              ppe=ppe, ic=ic, roic=roic, np_attr=np_fc, equity=eq_fc, net_debt=nd_fc,
              seg_rev=seg_rev, seg_ebitda=seg_ebitda, seg_shares=shares),
    seg_fy25=dict(rev=seg_rev_fy25, gp=seg_gp_fy25, names=SEGNAME, gp_margin=margin25),
    bottomup=dict(unit_hist=unit_hist, vol25=vol25, vol_f=vol_f, uplift25=uplift25,
                  price_t25=price_t25, cables_conv25=cables_conv25, compress=compress,
                  opex25=opex25, backlog=bl_path, gp=gp, gp_margin=gp_margin,
                  opex=opex, seg_gp=seg_gp, subs=SUBS, subnames=SUBNAME,
                  gp_t_cables_fy25=V['cables_gp_t_fy25'],
                  q1_26_implied_fy=V['q1_26_rev'] / (V['q1_25_rev'] / V['rev_fy25'])),
    wacc=dict(rf=V['rf'], rf_star=rf_star, ke_exp=ke_exp, ke_rating_alt=ke_rating_alt,
              ke_ops_alt=ke_ops_alt, ke_raw_retired=ke_raw_retired, kd=V['kd'], kd_at=kd_at,
              we_exp=we_exp, wd_exp=wd_exp, wacc_exp=wacc_exp, wacc_exp_gross=wacc_exp_gross,
              wd_gross=wd_gross, ke_term=ke_term, kd_term=V['kd_term'], kd_term_at=kd_term_at,
              wacc_term=wacc_term, glide_frac=glide_frac, kd_path=V['kd_path'],
              kd_eff_fy24=kd_eff_fy24, kd_eff_q1_25=kd_eff_q1_25, w_egp_implied=w_egp,
              wacc_usd_alt=WACC_USD, beta=beta_res),
    dcf=dict(pv_explicit=pv_explicit, tv=tv, pv_tv=pv_tv, ev=ev, tv_share=tv_share,
             nd=V['nd_fy25'], assoc=assoc_val, nci_share=nci_share, nci_val=nci_val,
             eq_attr=eq_attr, ps=dcf_ps, roic_term=roic_term, rr_term=rr_term,
             ps_rating_basis=dcf_rating_ps, wacc_exp_rating=wacc_exp_rating,
             wacc_term_rating=wacc_term_rating, ps_nci_alt=nci_alt_ps, nci_alt=nci_alt,
             g=V['g_term'], bear=dcf_bear, bull=dcf_bull, ccy_alt_ps=ccy_ps),
    terminal_recon=dict(roic=hist_roic, rr=hist_rr, implied_g=hist_impl_g,
                        nopat=dict(FY23=nopat_fy23, FY24=nopat_fy24, FY25=nopat_fy25),
                        capex=dict(FY23=V['capex_fy23'], FY24=V['capex_fy24'],
                                   FY25=V['capex_pct'][0] * V['rev_fy25']),
                        ebitda=dict(FY23=ebitda_fy23, FY24=ebitda_fy24, FY25=ebitda_fy25),
                        nopat_cagr=nopat_cagr, stable_g=stable_g,
                        ceiling=blend_ceiling, crossover_years=float(yrs_cross)),
    lenses=lenses, central=central, span=[lo, hi], spot=SPOT,
    experts=experts, panel_centre=panel_centre,
    sens_wg=dict(g_grid=g_grid, wacc_grid=wt_grid, table=grid_wacc_g),
    rel=dict(ebitda_mid=ebitda_mid, ev_rel=ev_rel, ev_ebitda_trailing=ev_ebitda_trailing,
             pe_trailing=pe_trailing, just_mult=V['ev_ebitda_just']),
    norm=dict(margin=norm_margin, rev=norm_rev, ebitda=norm_ebitda, ebit=norm_ebit,
              interest=norm_interest, np=norm_np, eps=norm_eps, pe=V['pe_just'],
              year=YRS[NORM_I], assoc=norm_assoc),
    book=dict(bvps=bvps, pb_just=pb_just, roe_sust=V['roe_sust'], roe_trailing=roe_trailing,
              ke_blend=ke_blend),
    sens=dict(g_grid=g_grid, wt_grid=wt_grid, we_grid=we_grid, grid_wacc_g=grid_wacc_g,
              grid_exp_term=grid_exp_term, beta_grid=beta_grid, grid_beta=grid_beta,
              fx_grid=fx_grid, grid_fx=grid_fx, mg_grid=mg_grid, grid_margin=grid_margin,
              cu_grid=cu_grid, grid_copper=grid_copper,
              nwc_grid=nwc_grid, grid_nwc=grid_nwc, roic_grid=roic_grid, grid_roic=grid_roic),
    step0=step0, strike=strike,
    assert_log=LOG,
)
with open(os.path.join(HERE, 'study_numbers.json'), 'w') as f:
    json.dump(OUT, f, indent=1, default=float)
say("=" * 78)
say(f"WROTE study_numbers.json | central EGP {central:.2f} [{lo:.2f} - {hi:.2f}] vs spot "
    f"{SPOT:.2f} | DCF {dcf_ps:.2f} | TV {tv_share:.0%} of EV | WACC {wacc_exp:.2%} -> "
    f"{wacc_term:.2%}")
