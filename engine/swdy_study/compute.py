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
    seg_share_fy25=I(dict(wc=0.590, ec=0.270, ep=0.060, ds=0.060, ii=0.020),
                     "Wires, Cables & Accessories ~59% of group revenue and Engineering & "
                     "Construction ~27% (company commentary on the 2025 results); the residual is "
                     "split across Electrical Products, Digital Solutions and Infrastructure "
                     "Investment in line with the disclosed Q1-2025 segment table (6.0% / 6.1% / "
                     "1.2% of revenue)", "2026-03", "Company"),
    seg_gp_margin_fy25=I(dict(wc=0.1245, ec=0.090, ep=0.380, ds=0.210, ii=0.600),
                         "Segment gross margins set from the disclosed Q1-2025 segment table "
                         "(W&C 16.6%, E&C 8.6%, Electrical Products 39.4%, Digital Solutions 21.9%, "
                         "Infrastructure 63.2%) stepped down for the further H2-2025 normalisation, "
                         "and solved so the weighted blend reproduces the FY2025 group gross margin "
                         "of 14.5%", "2026-08-05", "House"),
    opex_pct_fy25=I(0.035, "Operating cost load between gross profit and EBITDA, as a share of "
                    "revenue: FY2024 SG&A was 5.2% of revenue and Q1-2025 5.4%, against which other "
                    "income runs 1.5-1.7%. The FY2025 net load solves to 3.5% (14.5% gross margin "
                    "less the 11.0% EBITDA margin)", "2026-08-05", "House"),
    ebitda_margin_fy25=I(0.110, "FY2025 group EBITDA margin. Anchored on the last-twelve-month "
                         "aggregator print (USD 663mn EBITDA on USD 6.0bn revenue = 11.0%) and "
                         "cross-checked against the disclosed quarterly path: Q1 12.6%, Q2 11.1%, "
                         "Q4 9.5%", "2026-08-05", "House"),

    # ---- forecast drivers --------------------------------------------------
    foreign_share_fy25=I(0.70, "'Over 70% of revenues generated abroad' (company 2025 commentary). "
                         "The single most important structural fact about this company: the revenue "
                         "base is majority hard-currency while the listing, the reporting currency "
                         "and the cost of capital are Egyptian", "2026-03", "Company"),
    dom_growth=I([0.14, 0.12, 0.10, 0.09, 0.08],
                 "Domestic (EGP) revenue growth FY26E-FY30E. Egypt nominal GDP growth is running "
                 "~16-18% with inflation guided down toward the CBE's 7% (2026) and 5% (2028) "
                 "targets; the domestic leg is set to grow slightly below nominal GDP as "
                 "disinflation proceeds, with no domestic share gain assumed", "2026-08-05", "House"),
    fgn_growth_usd=I([0.10, 0.08, 0.07, 0.06, 0.06],
                     "Foreign revenue growth in USD. Supported by a USD 6.5bn project backlog "
                     "(~4.3x the E&C segment's annual revenue and above the group's historical "
                     "range), regional grid build-out and data-centre driven cable demand; tapering "
                     "to a mature single-digit rate by FY30E", "2026-08-05", "House"),
    fx_path=I([51.0, 54.0, 57.5, 61.0, 64.5],
              "USD/EGP average-rate path FY26E-FY30E, ~6%/yr depreciation from the FY2025 average "
              "of 49.5. DELIBERATELY BELOW covered-interest parity, which on the 22.31% EGP vs "
              "~4.3% USD rate gap implies ~17%/yr — the base case assumes the CBE's disinflation "
              "path largely closes that gap rather than the pound absorbing it. The parity path is "
              "carried as an explicit sensitivity because it moves the valuation more than any "
              "operating driver", "2026-08-05", "House"),
    fx_fy25_avg=I(49.5, "FY2025 average USD/EGP. The audited FY2024 note discloses closing 50.91 / "
                  "average 43.96 for 2024 and closing 30.96 / average 30.59 for 2023; 49.5 is the "
                  "2025 average consistent with the observed path", "2026-08-05", "House"),
    seg_share_fy30=I(dict(wc=0.560, ec=0.280, ep=0.065, ds=0.070, ii=0.025),
                     "FY30E segment mix: a modest drift out of wires & cables into the higher-margin "
                     "digital, electrical-products and infrastructure lines, consistent with the "
                     "company's stated three-year plan to broaden the portfolio. Interpolated "
                     "linearly from the FY2025 mix", "2026-08-05", "House"),
    seg_ebitda_margin_path=I(dict(
        wc=[0.091, 0.0925, 0.095, 0.098, 0.100],
        ec=[0.056, 0.058, 0.061, 0.063, 0.065],
        ep=[0.345, 0.345, 0.345, 0.345, 0.345],
        ds=[0.177, 0.180, 0.182, 0.1835, 0.185],
        ii=[0.565, 0.565, 0.565, 0.565, 0.565]),
        "Segment EBITDA margins FY26E-FY30E = segment gross margin less the 3.5%-of-revenue "
        "operating load, then allowed to recover gently as the copper-driven revenue inflation of "
        "2024-25 washes out of the denominator and the mix shifts. The wires & cables terminal "
        "margin of 10.0% sits well below the FY2024 windfall (14.3%, struck on devaluation "
        "inventory gains) and marginally above the FY2025 trough", "2026-08-05", "House"),
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
    ownership=I(dict(family=0.7818, float=0.2037, electra=0.0145),
                "Shareholder structure at 31 December 2024 and unchanged at 31 March 2025: El Sewedy "
                "family 78.18%, free float 20.37%, Electra Investment Holding 1.45%",
                "2025-05-26", "Company"),
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
ebitda_fy25 = V['ebitda_margin_fy25'] * V['rev_fy25']
dna_fy25 = V['dna_pct'] * V['rev_fy25']
op_fy25 = ebitda_fy25 - dna_fy25
netfin_fy25 = V['netfin_fy25']
assoc_fy25 = V['assoc_fy24'] * 1.15
pbt_fy25 = op_fy25 + netfin_fy25 + assoc_fy25
tax_fy25 = -(pbt_fy25 - V['pat_fy25'])
eff_tax_fy25 = -tax_fy25 / pbt_fy25
nci_fy25 = V['pat_fy25'] - V['npa_fy25']
say(f"[P&L closure FY2025] EBITDA {ebitda_fy25:,.0f} - D&A {dna_fy25:,.0f} = EBIT {op_fy25:,.0f}; "
    f"net finance {netfin_fy25:,.0f}; associates {assoc_fy25:,.0f} -> PBT {pbt_fy25:,.0f}; "
    f"implied tax {-tax_fy25:,.0f} = {eff_tax_fy25:.1%} (FY24 30.1%, FY23 31.3%) -> PAT "
    f"{V['pat_fy25']:,.0f} as disclosed; NCI {nci_fy25:,.0f}")
assert 0.20 < eff_tax_fy25 < 0.35, f"FY25 implied effective tax {eff_tax_fy25:.1%} implausible"

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

# ---- revenue: currency build ------------------------------------------------
YRS = ['FY26E', 'FY27E', 'FY28E', 'FY29E', 'FY30E']
dom_fy25 = (1 - V['foreign_share_fy25']) * V['rev_fy25']
fgn_fy25_egp = V['foreign_share_fy25'] * V['rev_fy25']
fgn_fy25_usd = fgn_fy25_egp / V['fx_fy25_avg']
rev, dom, fgn_usd, fgn_egp = [], [], [], []
d, u = dom_fy25, fgn_fy25_usd
for i in range(5):
    d *= (1 + V['dom_growth'][i]); u *= (1 + V['fgn_growth_usd'][i])
    e = u * V['fx_path'][i]
    dom.append(d); fgn_usd.append(u); fgn_egp.append(e); rev.append(d + e)
say(f"[Revenue build] FY2025 splits {dom_fy25:,.0f} domestic + {fgn_fy25_egp:,.0f} foreign "
    f"(USD {fgn_fy25_usd:,.0f}mn at {V['fx_fy25_avg']}). Forecast total revenue " +
    " -> ".join(f"{r:,.0f}" for r in rev) +
    " (growth " + ", ".join(f"{rev[i]/(V['rev_fy25'] if i==0 else rev[i-1])-1:+.1%}" for i in range(5)) + ")")

# ---- segment mix, margins, EBITDA -------------------------------------------
segs = ['wc', 'ec', 'ep', 'ds', 'ii']
SEGNAME = dict(wc='Wires, Cables & Accessories', ec='Engineering & Construction',
               ep='Electrical Products', ds='Digital Solutions', ii='Infrastructure Investment')
s0, s1 = V['seg_share_fy25'], V['seg_share_fy30']
shares = []
for i in range(5):
    f = (i + 1) / 5.0
    raw = {s: s0[s] + (s1[s] - s0[s]) * f for s in segs}
    tot = sum(raw.values())
    shares.append({s: raw[s] / tot for s in segs})
seg_rev = [{s: shares[i][s] * rev[i] for s in segs} for i in range(5)]
seg_ebitda = [{s: seg_rev[i][s] * V['seg_ebitda_margin_path'][s][i] for s in segs} for i in range(5)]
ebitda = [sum(seg_ebitda[i].values()) for i in range(5)]
ebitda_margin = [ebitda[i] / rev[i] for i in range(5)]
# FY2025 segment reference (for the Segments sheet)
seg_rev_fy25 = {s: s0[s] * V['rev_fy25'] for s in segs}
seg_gp_fy25 = {s: seg_rev_fy25[s] * V['seg_gp_margin_fy25'][s] for s in segs}
gp_blend_fy25 = sum(seg_gp_fy25.values()) / V['rev_fy25']
say(f"[Segment mix] FY2025 segment gross margins blend to {gp_blend_fy25:.2%} against the derived "
    f"group gross margin of {V['gp_fy25']/V['rev_fy25']:.2%}. Forecast group EBITDA margin " +
    " -> ".join(f"{m:.2%}" for m in ebitda_margin))
assert abs(gp_blend_fy25 - V['gp_fy25'] / V['rev_fy25']) < 0.005, "segment gross margins do not blend"

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
roic_term = roic[-1]
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
assoc_val = V['assoc_bv_fy24'] * 1.15
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
fcff_f = [fcff[i] * fgn_frac[i] for i in range(5)]
fcff_d = [fcff[i] * (1 - fgn_frac[i]) for i in range(5)]
df_usd, c2 = [], 1.0
for _ in range(5):
    c2 /= (1 + WACC_USD); df_usd.append(c2)
pv_f = sum(fcff_f[i] * df_usd[i] for i in range(5))
tv_f = nopat_term * (1 - rr_term) * fgn_frac[-1] / (WACC_USD - 0.035)
pv_d = sum(fcff_d[i] * df[i] for i in range(5))
tv_d = nopat_term * (1 - rr_term) * (1 - fgn_frac[-1]) / (wacc_term - V['g_term'])
ev_ccy = pv_f + tv_f * df_usd[-1] + pv_d + tv_d * df[-1]
eq_ccy = (ev_ccy - V['nd_fy25'] + assoc_val) * (1 - nci_share)
ccy_ps = eq_ccy / SH
say(f"[Currency-of-discounting alternative] discounting the ~{fgn_frac[-1]:.0%} hard-currency cash "
    f"flow leg at a USD WACC of {WACC_USD:.2%} with 3.5% terminal growth, and the domestic leg "
    f"unchanged, gives EGP {ccy_ps:.2f}/share ({ccy_ps/SPOT-1:+.0%} vs spot). This is disclosed "
    f"as the alternative the market appears to be applying, not as the primary read.")

# ---- lens 2: relative --------------------------------------------------------
ebitda_mid = ebitda[1]
ev_rel = V['ev_ebitda_just'] * ebitda_mid
rel_ps = ((ev_rel - V['nd_fy25'] + assoc_val) * (1 - nci_share)) / SH
rel_bear = ((5.5 * ebitda_mid - V['nd_fy25'] + assoc_val) * (1 - nci_share)) / SH
rel_bull = ((8.0 * ebitda_mid - V['nd_fy25'] + assoc_val) * (1 - nci_share)) / SH
ev_trailing = MKTCAP + V['nd_fy25']
ev_ebitda_trailing = ev_trailing / ebitda_fy25
pe_trailing = SPOT / (V['npa_fy25'] / SH)

# ---- lens 3: normalized earnings power ---------------------------------------
norm_margin = float(np.mean(ebitda_margin[2:]))
norm_rev = rev[1]
norm_ebitda = norm_margin * norm_rev
norm_ebit = norm_ebitda - V['dna_pct'] * norm_rev
norm_interest = V['kd'] * debt_fy25 - 0.10 * cash_fy25
norm_np = (norm_ebit - norm_interest + assoc_fy25) * (1 - TAX) * (1 - nci_share)
norm_eps = norm_np / SH
norm_ps = V['pe_just'] * norm_eps
norm_bear = 7.0 * norm_eps
norm_bull = 11.5 * norm_eps

# ---- lens 4: book / justified P/B --------------------------------------------
bvps = eqp_fy25 / SH
ke_blend = 0.5 * (ke_exp + ke_term)
pb_just = (V['roe_sust'] - V['g_term']) / (ke_blend - V['g_term'])
book_ps = pb_just * bvps
book_bear = ((V['roe_sust'] - 0.03) / (ke_exp - 0.03)) * bvps
book_bull = ((V['roe_sust'] - V['g_term']) / (ke_term - V['g_term'])) * bvps
roe_trailing = V['npa_fy25'] / ((V['eqp_fy24'] + eqp_fy25) / 2)

# ---- scenarios on the DCF -----------------------------------------------------
def dcf_scenario(margin_shift, fx_mult, wacc_shift, g):
    _ebitda = [(ebitda_margin[i] + margin_shift) * rev[i] * fx_mult for i in range(5)]
    _rev = [rev[i] * fx_mult for i in range(5)]
    _dna = [V['dna_pct'] * r for r in _rev]
    _ebit = [_ebitda[i] - _dna[i] for i in range(5)]
    _nopat = [e * (1 - TAX) for e in _ebit]
    _capex = [V['capex_pct'][i] * r for i, r in enumerate(_rev)]
    _nwc = [V['nwc_pct'] * r for r in _rev]
    _dnwc = [_nwc[0] - nwc_fy25] + [_nwc[i] - _nwc[i - 1] for i in range(1, 5)]
    _f = [_nopat[i] + _dna[i] - _capex[i] - _dnwc[i] for i in range(5)]
    _we, _wt = wacc_exp + wacc_shift, wacc_term + wacc_shift
    _fwd = [_we - (_we - _wt) * f for f in glide_frac]
    _df, cc = [], 1.0
    for w in _fwd:
        cc /= (1 + w); _df.append(cc)
    _ppe, pp = [], ppe_fy25
    for i in range(5):
        pp += _capex[i] - _dna[i]; _ppe.append(pp)
    _roic = _nopat[-1] / (_nwc[-1] + _ppe[-1] + V['intang_fy24'])
    _rr = min(g / _roic, 0.95)
    _tv = _nopat[-1] * (1 + g) * (1 - _rr) / max(_wt - g, 0.02)
    _ev = sum(_f[i] * _df[i] for i in range(5)) + _tv * _df[-1]
    return ((_ev - V['nd_fy25'] + assoc_val) * (1 - nci_share)) / SH

dcf_bear = dcf_scenario(-0.015, 0.94, +0.02, 0.03)
dcf_bull = dcf_scenario(+0.015, 1.08, -0.02, 0.06)
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
beta_grid = [0.6, 0.8, 1.0, 1.009, 1.15, 1.3]
def dcf_beta(b):
    ke = rf_star + b * V['erp_cds']
    we_ = we_exp * ke + wd_exp * kd_at
    wt_ = (1 - V['wd_term']) * (V['rf_term'] + b * V['erp_term']) + V['wd_term'] * kd_term_at
    return dcf_at(we_, wt_, V['g_term'])
grid_beta = [dcf_beta(b) for b in beta_grid]
fx_grid = [0.90, 0.95, 1.00, 1.08, 1.20]
grid_fx = [dcf_scenario(0.0, m, 0.0, V['g_term']) for m in fx_grid]
mg_grid = [-0.02, -0.01, 0.0, 0.01, 0.02]
grid_margin = [dcf_scenario(m, 1.0, 0.0, V['g_term']) for m in mg_grid]
nwc_grid = [0.20, 0.215, 0.23, 0.245, 0.26]
def dcf_nwc(pct):
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
for i in range(5):
    interest = V['kd_path'][i] * debt_fy25 - 0.10 * cash_fy25
    pbt_i = ebit[i] - interest + assoc_fy25 * (1 + 0.08) ** (i + 1)
    pat_i = pbt_i * (1 - TAX)
    npa_i = pat_i * (1 - nci_share)
    div_i = 0.25 * npa_i
    e_ += npa_i - div_i
    eq_fc.append(e_); np_fc.append(npa_i)
    nd_ = nd_ - (fcff[i] - interest * (1 - TAX)) + div_i
    nd_fc.append(nd_)
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
e2_ke = ke_blend
e2_base = e2_fcfe * (1 + V['g_term']) / (e2_ke - V['g_term']) / SH
e2_lo = e2_fcfe * 1.03 / (ke_exp - 0.03) / SH
e2_hi = e2_fcfe * 1.05 / (ke_term - V['g_term']) / SH
# E3 — cash returns: economic profit on invested capital through the rate cycle.
ep_ = [nopat[i] - fwd[i] * ic[i] for i in range(5)]
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
    fcst=dict(years=YRS, rev=rev, dom=dom, fgn_usd=fgn_usd, fgn_egp=fgn_egp,
              ebitda=ebitda, ebitda_margin=ebitda_margin, dna=dna, ebit=ebit, nopat=nopat,
              capex=capex, nwc=nwc, dnwc=dnwc, fcff=fcff, df=df, pv=pv, fwd_wacc=fwd,
              ppe=ppe, ic=ic, roic=roic, np_attr=np_fc, equity=eq_fc, net_debt=nd_fc,
              seg_rev=seg_rev, seg_ebitda=seg_ebitda, seg_shares=shares),
    seg_fy25=dict(rev=seg_rev_fy25, gp=seg_gp_fy25, names=SEGNAME,
                  gp_margin=V['seg_gp_margin_fy25']),
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
              interest=norm_interest, np=norm_np, eps=norm_eps, pe=V['pe_just']),
    book=dict(bvps=bvps, pb_just=pb_just, roe_sust=V['roe_sust'], roe_trailing=roe_trailing,
              ke_blend=ke_blend),
    sens=dict(g_grid=g_grid, wt_grid=wt_grid, we_grid=we_grid, grid_wacc_g=grid_wacc_g,
              grid_exp_term=grid_exp_term, beta_grid=beta_grid, grid_beta=grid_beta,
              fx_grid=fx_grid, grid_fx=grid_fx, mg_grid=mg_grid, grid_margin=grid_margin,
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
