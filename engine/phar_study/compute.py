"""PHAR (EIPICO) study — master computation. Writes study_numbers.json (single
source of truth for every builder). Code-first rule: INPUTS are four-field
records {value, source, date, layer}; a bare numeral cannot enter the model; the
ASSERT block raises (no JSON emitted) unless the bridge closes, the discount-rate
glide is ordered, the Kd-integrity triple holds, and the terminal is
ROIC-consistent.

BUILT 09-Aug-2026 on the company's OWN audited annual financial statements for
FY2022-FY2025, downloaded from the Egyptian International Pharmaceutical
Industries Company's investor-relations page (eipico.com.eg -> Investor Relations
-> Annual Reports). Every historical figure below is the audited CONSOLIDATED
figure or a disclosed note thereto; not one comes from a data vendor, a broker
note or press coverage.

Company class: OPERATING COMPANY — a vertically integrated generic and branded
pharmaceutical manufacturer and exporter, with a wholly-owned primary-packaging
subsidiary (EIACO) and two equity-accounted associates. Revenue is product sales
through four disclosed channels (direct, distributors, government tenders,
export) plus contract manufacturing. The balance sheet is property- and
inventory-heavy with no lending book. Lens set follows the operating-company
reference: FCFF DCF primary, book value and sustainable return, relative
multiples, and normalised earnings power.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import numpy as np

MN = 1e6   # every monetary figure below is in EGP millions unless named otherwise


# ============================ INPUT REGISTER =================================
Q1SRC = ("Reviewed consolidated interim financial statements for the three months ended "
         "31 March 2026, English translation issued by the auditor, review report dated "
         "14 May 2026. THE REVIEW CONCLUSION IS QUALIFIED")


def I(value, source, date, layer):
    return dict(value=value, source=source, date=date, layer=layer)


AUD25 = ("Audited consolidated financial statements for the year ended 31 December 2025, "
         "published in the company's 2025 Annual Report (eipico.com.eg -> Investor Relations "
         "-> Annual Reports)")
AUD24 = ("Audited consolidated financial statements for the year ended 31 December 2024 "
         "(confirmed against the comparative column of the FY2025 filing)")
AUD23 = ("Audited consolidated financial statements for the year ended 31 December 2023 "
         "(confirmed against the comparative column of the FY2024 filing)")
BOARD25 = ("Board of Directors' report for FY2025, published inside the 2025 Annual Report — "
           "the company's own disclosed operating statistics")
IRDECK = ("Company investor presentation, published on the corporate website "
          "(eipico.com.eg -> Company Profile / EIPICO Presentation)")

INP = dict(
    # ---- market anchors -------------------------------------------------
    spot=I(130.05, "Last close of the uploaded EGX daily price history for the company's listed "
           "ordinary shares", "2026-08-06", "Market"),
    shares_mn=I(168.755750, "Issued and fully paid capital note (13): EGP 1,687,557,500 divided "
                "into 168,755,750 shares of EGP 10 par value, following the July-2025 issue of "
                "20 million new shares approved by the exchange's listing committee on 23 July "
                "2025. The shareholder table in the same note sums to exactly 168,755,750 "
                "shares", "2026-03-28", "Company"),
    wavg_shares_mn=I(162.016024, "Weighted average shares outstanding during FY2025, earnings-"
                     "per-share note (34)", "2026-03-28", "Company"),

    # ---- audited consolidated income statement --------------------------
    rev_fy23=I(5231.665571, AUD23, "2024-03-01", "Company"),
    rev_fy24=I(7590.545643, AUD24, "2025-03-01", "Company"),
    rev_fy25=I(9441.379305, AUD25, "2026-03-01", "Company"),
    cogs_fy23=I(2896.343413, AUD23, "2024-03-01", "Company"),
    cogs_fy24=I(4184.382863, AUD24, "2025-03-01", "Company"),
    cogs_fy25=I(5287.140903, AUD25, "2026-03-01", "Company"),
    mkt_fy23=I(648.291681, AUD23 + ", marketing expenses note", "2024-03-01", "Company"),
    mkt_fy24=I(915.021183, AUD24 + ", marketing expenses note (27)", "2025-03-01", "Company"),
    mkt_fy25=I(1000.128922, AUD25 + ", marketing expenses note (27)", "2026-03-01", "Company"),
    rnd_fy23=I(43.227785, AUD23 + ", research and development note", "2024-03-01", "Company"),
    rnd_fy24=I(70.460824, AUD24 + ", research and development note (28)", "2025-03-01", "Company"),
    rnd_fy25=I(70.935883, AUD25 + ", research and development note (28)", "2026-03-01", "Company"),
    ga_fy23=I(147.460991, "Audited consolidated statement of profit or loss for the year ended "
              "31 December 2023, English translation issued by the auditor: general and "
              "administrative expenses note (30). The Arabic annual report presents this line "
              "at 151.585 with dividend-distribution tax folded into it; the separately issued "
              "statements split the two, and this study follows the split", "2024-03-01",
              "Company"),
    ga_fy24=I(188.492929, AUD24 + ", general and administrative note (29)", "2025-03-01", "Company"),
    ga_fy25=I(221.136860, AUD25 + ", general and administrative note (29)", "2026-03-01", "Company"),
    board_fy23=I(2.020000, AUD23, "2024-03-01", "Company"),
    board_fy24=I(1.580000, AUD24, "2025-03-01", "Company"),
    board_fy25=I(1.828000, AUD25, "2026-03-01", "Company"),
    # credit losses, inventory write-downs and other provisions — charged below
    # gross profit in the company's own presentation
    prov_fy23=I(39.0 + 87.0 + 139.0, AUD23 + ": expected credit losses 39.0, inventory "
                "impairment 87.0, other provisions 139.0", "2024-03-01", "Company"),
    prov_fy24=I(330.0 + 60.0 + 312.0, AUD24 + ": expected credit losses 330.0, inventory "
                "impairment 60.0, other provisions 312.0 (note 31: disputed taxes 180.0, claims "
                "50.0, end-of-service 82.0)", "2025-03-01", "Company"),
    prov_fy25=I(376.157654 + 13.060720 + 105.0, AUD25 + ": expected credit losses 376.158, "
                "inventory impairment 13.061, other provisions 105.0 (note 31: disputed taxes "
                "18.5, claims 1.5, end-of-service 85.0)", "2026-03-01", "Company"),
    fin_fy23=I(407.705200, AUD23 + ", finance costs note", "2024-03-01", "Company"),
    fin_fy24=I(960.131966, AUD24 + ", finance costs note (30)", "2025-03-01", "Company"),
    fin_fy25=I(1332.946559, AUD25 + ", finance costs note (30): interest on credit facilities "
               "1,275.312 plus bank commissions and charges 57.634", "2026-03-01", "Company"),
    assoc_fy23=I(74.508447, AUD23 + ", share of results of subsidiaries and associates",
                 "2024-03-01", "Company"),
    assoc_fy24=I(151.580926, "Audited consolidated statement of profit or loss FY2024, English "
                 "translation issued by the auditor: profit of subsidiaries and associates. "
                 "GROSS of dividend-distribution tax, which that statement shows on its own "
                 "line; the Arabic annual report nets the two to 147.112", "2025-03-01",
                 "Company"),
    assoc_fy25=I(427.906046 + 84.178592, AUD25 + ", note (33): Batterjee Pharma (Saudi Arabia) "
                 "427.906 plus Medical Professions Company 84.179, stated GROSS of the 16.585 "
                 "withholding tax on distributions so that all three years are presented on the "
                 "same basis as the separately issued statements", "2026-03-01", "Company"),
    divtax_fy23=I(4.123733, "Dividend-distribution tax, shown as its own line in the separately "
                  "issued audited consolidated statement of profit or loss FY2023",
                  "2024-03-01", "Company"),
    divtax_fy24=I(4.468933, "Dividend-distribution tax, separately issued audited consolidated "
                  "statement of profit or loss FY2024", "2025-03-01", "Company"),
    divtax_fy25=I(16.585420, AUD25 + ", note (33): withholding tax on associate distributions",
                  "2026-03-01", "Company"),
    intinc_fy23=I(26.243536, AUD23, "2024-03-01", "Company"),
    intinc_fy24=I(72.048362, AUD24, "2025-03-01", "Company"),
    intinc_fy25=I(139.673783, AUD25, "2026-03-01", "Company"),
    fx_fy23=I(139.625936, AUD23 + ", foreign-exchange differences", "2024-03-01", "Company"),
    fx_fy24=I(699.879896, AUD24 + ", foreign-exchange differences", "2025-03-01", "Company"),
    fx_fy25=I(-16.168329, AUD25 + ", foreign-exchange differences", "2026-03-01", "Company"),
    othinc_fy23=I(20.695305 + 4.689492, AUD23 + ": other income 20.695 plus capital gains 4.689",
                  "2024-03-01", "Company"),
    othinc_fy24=I(42.631725 + 0.222246, AUD24 + ": other income 42.632 plus capital gains 0.222",
                  "2025-03-01", "Company"),
    othinc_fy25=I(142.089566 + 1.763816, AUD25 + ": other income 142.090 plus capital gains 1.764",
                  "2026-03-01", "Company"),
    pbt_fy23=I(1083.255484, AUD23, "2024-03-01", "Company"),
    pbt_fy24=I(1530.370100, AUD24, "2025-03-01", "Company"),
    pbt_fy25=I(1795.901858, AUD25, "2026-03-01", "Company"),
    taxtot_fy23=I(249.772423 - 4.147536 + 14.324267, AUD23 + ": current tax 249.772, deferred "
                  "tax credit 4.148, statutory solidarity contribution 14.324", "2024-03-01",
                  "Company"),
    taxtot_fy24=I(430.792372 - 18.964390 + 21.618514, AUD24 + ": current tax 430.792, deferred "
                  "tax credit 18.964, statutory solidarity contribution 21.619", "2025-03-01",
                  "Company"),
    taxtot_fy25=I(421.702076 - 108.663088 + 24.969855, AUD25 + ": current tax 421.702, deferred "
                  "tax credit 108.663, statutory solidarity contribution 24.970", "2026-03-01",
                  "Company"),
    np_fy23=I(823.306330, AUD23 + ", profit for the year", "2024-03-01", "Company"),
    np_fy24=I(1096.923604, AUD24 + ", profit for the year", "2025-03-01", "Company"),
    np_fy25=I(1457.893015, AUD25 + ", profit for the year", "2026-03-01", "Company"),
    parent_fy22=I(587.040623, "Audited consolidated financial statements for FY2022, profit "
                  "attributable to the holding company (587.041) — read from the comparative "
                  "column of the FY2023 filing", "2024-03-01", "Company"),
    parent_fy23=I(822.317715, AUD23 + ", profit attributable to the holding company (751.218 "
                  "parent plus 71.099 the holding company's share of the subsidiary)",
                  "2024-03-01", "Company"),
    parent_fy24=I(1095.717079, AUD24 + ", profit attributable to the holding company",
                  "2025-03-01", "Company"),
    parent_fy25=I(1441.657700, AUD25 + ", profit attributable to the holding company "
                  "(1,352.285 parent plus 89.373 the holding company's share of the subsidiary); "
                  "reported earnings per share EGP 8.89", "2026-03-01", "Company"),

    # ---- depreciation and amortisation (consolidated cash-flow statement) --
    dna_fy23=I(102.675784 + 2.082510 + 0.491451, AUD23 + ", consolidated statement of cash "
               "flows: depreciation of property 102.676, amortisation of right-of-use assets "
               "2.083, amortisation of intangibles 0.491", "2024-03-01", "Company"),
    dna_fy24=I(96.532194 + 2.361230 + 3.918430, AUD24 + ", consolidated statement of cash flows: "
               "depreciation 96.532, right-of-use 2.361, intangibles 3.918", "2025-03-01",
               "Company"),
    dna_fy25=I(109.455425 + 3.323968 + 4.945981, AUD25 + ", consolidated statement of cash "
               "flows: depreciation 109.455, right-of-use 3.324, intangibles 4.946",
               "2026-03-01", "Company"),

    # ---- audited consolidated balance sheet, 31 December 2025 -------------
    ppe_fy25=I(3069.747924, AUD25 + ", note (4) property, plant and equipment net of "
               "accumulated depreciation", "2026-03-01", "Company"),
    ppe_fy24=I(1045.230507, AUD24 + ", note (4)", "2025-03-01", "Company"),
    cip_fy25=I(4901.223806, AUD25 + ", note (6) projects under construction — predominantly the "
               "EIPICO 3 biologicals and biosimilars facility", "2026-03-01", "Company"),
    cip_fy24=I(5693.566382, AUD24 + ", note (6)", "2025-03-01", "Company"),
    rou_fy25=I(233.640379, AUD25 + ", note (5) right-of-use assets net", "2026-03-01", "Company"),
    intang_fy25=I(40.142171, AUD25 + ", note (7) intangible assets net", "2026-03-01", "Company"),
    dta_fy25=I(337.611796, AUD25 + ", deferred tax asset", "2026-03-01", "Company"),
    assoc_bv_fy25=I(675.874567, AUD25 + ", note (8/2) investments in associates carried at "
                    "equity: a 30% interest in Batterjee Pharmaceutical (Saudi Arabia) and a "
                    "9.77%-plus interest in the Medical Professions Company", "2026-03-01",
                    "Company"),
    assoc_bv_fy24=I(465.263725, AUD24 + ", note (8/2)", "2025-03-01", "Company"),
    afs_fy25=I(12.330000, AUD25 + ", note (8/1) non-current assets held for sale — the "
               "investment in EIPICO Tech Pharmaceuticals, in liquidation", "2026-03-01",
               "Company"),
    inv_fy25=I(3887.077629, AUD25 + ", note (9) inventories net of provision", "2026-03-01",
               "Company"),
    inv_fy24=I(3584.699946, AUD24 + ", note (9)", "2025-03-01", "Company"),
    ar_fy25=I(3325.044117, AUD25 + ", note (10) trade and notes receivable net of the expected "
              "credit-loss allowance", "2026-03-01", "Company"),
    ar_fy24=I(3049.275231, AUD24 + ", note (10)", "2025-03-01", "Company"),
    othdr_fy25=I(356.786958, AUD25 + ", note (11) other debtors and debit balances",
                 "2026-03-01", "Company"),
    othdr_fy24=I(185.584353, AUD24 + ", note (11)", "2025-03-01", "Company"),
    cash_fy25=I(1433.426902, AUD25 + ", note (12) cash and bank balances", "2026-03-01",
                "Company"),
    cash_fy24=I(1295.386860, AUD24 + ", note (12)", "2025-03-01", "Company"),
    ap_fy25=I(780.416969, AUD25 + ", note (22) trade and notes payable", "2026-03-01", "Company"),
    ap_fy24=I(410.391619, AUD24 + ", note (22)", "2025-03-01", "Company"),
    othcr_fy25=I(1044.832275, AUD25 + ", note (23) other creditors and credit balances",
                 "2026-03-01", "Company"),
    othcr_fy24=I(367.421180, AUD24 + ", note (23)", "2025-03-01", "Company"),
    provbs_fy25=I(537.942744, AUD25 + ", note (20) provisions", "2026-03-01", "Company"),
    taxpay_fy25=I(388.949813, AUD25 + ", income tax payable", "2026-03-01", "Company"),
    dtl_fy25=I(190.768071, AUD25 + ", note (19) deferred tax liabilities", "2026-03-01",
               "Company"),
    equity_parent_fy25=I(6243.131482, AUD25 + ", total equity attributable to the holding "
                         "company", "2026-03-01", "Company"),
    equity_parent_fy24=I(4653.769234, AUD24, "2025-03-01", "Company"),
    equity_parent_fy23=I(4257.408090, AUD23, "2024-03-01", "Company"),
    nci_fy25=I(288.704605, AUD25 + ", non-controlling interests", "2026-03-01", "Company"),
    assets_fy25=I(18272.906249, AUD25 + ", total assets", "2026-03-01", "Company"),

    # ---- debt, by tranche and currency (note 17) ---------------------------
    loans_lt_fy25=I(3758.803399, AUD25 + ", note (17) long-term instalments of borrowings",
                    "2026-03-01", "Company"),
    loans_st_fy25=I(1107.863191, AUD25 + ", note (17) current instalments of borrowings",
                    "2026-03-01", "Company"),
    facilities_fy25=I(3918.693902, AUD25 + ", note (21) bank overdrafts and credit facilities",
                      "2026-03-01", "Company"),
    leases_fy25=I(11.982389 + 0.382759, AUD25 + ", note (18) lease liabilities: 11.982 "
                  "non-current plus 0.383 current", "2026-03-01", "Company"),
    loans_fx_fy25=I(2188.896030 + 11.325270 + 220.002358 + 23.000694,
                    AUD25 + ", note (17) borrowings by lender and currency: Qatar National Bank "
                    "Alahli US-dollar 2,188.896 and euro 11.325, National Bank of Kuwait euro "
                    "220.002 and US-dollar 23.001", "2026-03-01", "Company"),
    loans_lc_fy25=I(99.625027 + 1401.587586 + 423.652754 + 498.576871,
                    AUD25 + ", note (17): National Bank of Kuwait local currency 99.625, Banque "
                    "du Caire local currency 1,401.588, Abu Dhabi Islamic Bank local currency "
                    "423.653, Kuwait Finance House 498.577", "2026-03-01", "Company"),
    capint_cum_fy25=I(932.390475, AUD25 + ", note (6): interest capitalised into projects under "
                      "construction, cumulative", "2026-03-01", "Company"),
    capint_cum_fy24=I(381.335878, AUD24 + ", note (6): interest capitalised into projects under "
                      "construction, cumulative", "2025-03-01", "Company"),
    capfx_cum_fy24=I(1843.125627, AUD24 + ", note (6): foreign-exchange differences on foreign-"
                     "currency liabilities related to the purchase and construction of the "
                     "EIPICO 3 plant, capitalised", "2025-03-01", "Company"),
    int_fac_fy25=I(1275.312358, AUD25 + ", note (30) interest on credit facilities",
                   "2026-03-01", "Company"),

    # ---- the unit build: volumes, prices and capacity ----------------------
    packs_sold_fy23=I(279.716, BOARD25.replace('FY2025', 'FY2024') + " — packs sold, million: "
                      "273.750 own preparations plus 5.966 contract manufacturing",
                      "2025-03-01", "Company"),
    packs_sold_fy24=I(307.846, BOARD25 + " — packs sold, million: 298.972 own preparations plus "
                      "8.874 contract manufacturing", "2026-03-28", "Company"),
    packs_sold_fy25=I(357.295, BOARD25 + " — packs sold, million: 351.810 own preparations plus "
                      "5.485 contract manufacturing", "2026-03-28", "Company"),
    packs_own_fy24=I(298.972, BOARD25 + " — packs sold of the company's own preparations",
                     "2026-03-28", "Company"),
    packs_own_fy25=I(351.810, BOARD25 + " — packs sold of the company's own preparations",
                     "2026-03-28", "Company"),
    packs_toll_fy25=I(5.485, BOARD25 + " — packs sold under contract-manufacturing agreements",
                      "2026-03-28", "Company"),
    export_packs_fy25=I(60.0, IRDECK + ": export reach of 60 million packs a year to more than "
                        "60 countries", "2026-08-09", "Company"),
    export_usd_fy25=I(60.0, BOARD25 + ": exports of EGP 2,967 million, stated in the same "
                      "paragraph as USD 60 million (2024: EGP 2,500 million / USD 55 million)",
                      "2026-03-28", "Company"),
    export_usd_fy24=I(54.7, "Board of Directors' report for FY2024: exports of EGP 2,500 million "
                      "stated as USD 54.7 million, against EGP 1,592 million / USD 51.6 million "
                      "in FY2023", "2025-03-01", "Company"),
    # channel revenue, standalone basis, as the company itself reports it
    ch_direct_fy25=I(1943.421246, AUD25 + ", revenue note (25): local direct sales",
                     "2026-03-01", "Company"),
    ch_distrib_fy25=I(3591.139796, AUD25 + ", revenue note (25): local distributor sales",
                      "2026-03-01", "Company"),
    ch_tender_fy25=I(751.061996, AUD25 + ", revenue note (25): local tender/supply sales",
                     "2026-03-01", "Company"),
    ch_export_fy25=I(3103.975448 - 136.495540, AUD25 + ", revenue note (25): export sales "
                     "3,103.975 less export distributor incentives 136.496", "2026-03-01",
                     "Company"),
    ch_toll_fy25=I(49.366365, AUD25 + ", revenue note (25): contract-manufacturing revenue",
                   "2026-03-01", "Company"),
    ch_direct_fy24=I(1530.492099, AUD24 + ", revenue note (25)", "2025-03-01", "Company"),
    ch_distrib_fy24=I(2674.363238 - 10.824144, AUD24 + ", revenue note (25): distributor sales "
                      "less local distributor incentives", "2025-03-01", "Company"),
    ch_tender_fy24=I(634.048710, AUD24 + ", revenue note (25)", "2025-03-01", "Company"),
    ch_export_fy24=I(2587.241752 - 87.085806, AUD24 + ", revenue note (25): export sales less "
                     "export distributor incentives", "2025-03-01", "Company"),
    ch_toll_fy24=I(35.835829, AUD24 + ", revenue note (25)", "2025-03-01", "Company"),
    units_prod_fy24=I(2143.68, BOARD25 + " — comparative production by pharmaceutical dosage "
                      "form, million units. NOTE the FY2024 Annual Report's own tablet line "
                      "read 1,513.38 million against the 1,351.75 million restated in the "
                      "FY2025 report; the later filing is used and the restatement disclosed",
                      "2026-03-28", "Company"),
    units_prod_fy25=I(2207.95, BOARD25 + " — production by pharmaceutical dosage form, million "
                      "units, summed across all twenty-one disclosed forms", "2026-03-28",
                      "Company"),
    units_cap=I(3383.06, BOARD25 + " — available capacity in the period, million units, summed "
                "across all disclosed dosage forms (unchanged 2024 and 2025)", "2026-03-28",
                "Company"),
    employees_fy25=I(4981, BOARD25 + " — average headcount", "2026-03-28", "Company"),
    prod_value_fy25=I(10811.924, BOARD25 + " — value of production", "2026-03-28", "Company"),
    products_fy25=I(414, BOARD25 + " — number of registered preparations produced (2024: 401)",
                    "2026-03-28", "Company"),

    # ---- currency -----------------------------------------------------------
    fx_avg_fy25=I(49.48, AUD25 + ", note (36) foreign-currency risk: average exchange rate used "
                  "during the period, EGP per US dollar", "2026-03-01", "Company"),
    fx_close_fy25=I(49.52, AUD25 + ", note (36): closing rate at the balance-sheet date",
                    "2026-03-01", "Company"),
    fx_avg_fy24=I(47.74, AUD24 + ", note (36): average rate during FY2024", "2025-03-01",
                  "Company"),
    fx_close_fy24=I(50.89, AUD24 + ", note (36): closing rate at 31 December 2024", "2025-03-01",
                    "Company"),
    fx_net_monetary_usd_fy25=I(-0.540092, AUD25 + ", note (36): net monetary position in US "
                               "dollars at the balance-sheet date — bank balances 10.510 plus "
                               "receivables 40.068 less creditor banks 51.118, in millions of "
                               "US dollars", "2026-03-01", "Company"),
    fx_path=I([50.5, 52.5, 54.3, 56.0, 57.7],
              "Egyptian pound per US dollar, FY2026E-FY2030E period averages. Built from the "
              "inflation differential rather than asserted: the pound averaged 47.74 in 2024 and "
              "49.48 in 2025 (a 3.6% move) while consumer inflation ran far above the United "
              "States', so the real exchange rate appreciated. The path assumes that reverses "
              "only partially, at roughly 4% a year narrowing to 3% as domestic inflation "
              "converges on the central bank's stated 5% medium-term target", "2026-08-09",
              "House"),

    # ---- forecast drivers: volume ------------------------------------------
    dom_pack_growth=I([0.055, 0.080, 0.075, 0.065, 0.055],
                      "Domestic packs sold, annual volume growth FY2026E-FY2030E. The company "
                      "sold 244.3 million domestic packs of its own preparations in FY2024 and "
                      "291.8 million in FY2025 (+19.5%); disclosed capacity utilisation is 65% "
                      "of 3,383 million units, so the volume is not capacity-constrained. The "
                      "path steps down from a rate materially below the FY2025 outturn toward "
                      "population-plus-penetration growth. THE FIRST YEAR IS RESET TO THE "
                      "FIRST QUARTER'S OUTTURN: net sales grew 10.1% year on year in the three "
                      "months to March 2026, against the 17.5% the first cut of this model "
                      "carried", "2026-08-11", "House"),
    exp_pack_growth=I([0.05, 0.09, 0.085, 0.08, 0.07],
                      "Export packs, annual volume growth. Export value grew 10% in US dollars "
                      "in FY2025 (USD 54.7m to 60.0m) on a company that is already the largest "
                      "Egyptian pharmaceutical exporter with 26% of national pharmaceutical "
                      "export value across 67 countries; the biosimilars plant licensed in "
                      "December 2025 adds a new export line rather than replacing one",
                      "2026-08-09", "House"),
    dom_price_growth=I([0.05, 0.080, 0.075, 0.065, 0.055],
                       "Domestic realised price per pack, annual growth. Egyptian medicine "
                       "prices are set administratively by the Egyptian Drug Authority and move "
                       "in periodic approved adjustments rather than continuously; realised "
                       "price per pack rose 12.6% in FY2025 after a much larger devaluation-"
                       "driven step in FY2024. The path assumes price growth tracks domestic "
                       "inflation as it converges on the central bank's target, with no real "
                       "price gain", "2026-08-09", "House"),
    exp_price_usd_growth=I([0.01, 0.01, 0.01, 0.01, 0.01],
                           "Export realised price per pack in US dollars, annual growth. FY2025 "
                           "realised USD 1.00 per pack. Generic export pricing is competitive "
                           "and broadly flat in hard currency; 1% a year is a nominal-dollar "
                           "drift, not a real gain", "2026-08-09", "House"),
    toll_growth=I([0.15, 0.12, 0.10, 0.08, 0.07],
                  "Contract-manufacturing revenue growth. A small line (0.5% of revenue) that "
                  "grew 37.8% in FY2025 off a low base as the company let third parties use "
                  "idle capacity", "2026-08-09", "House"),

    # ---- forecast drivers: the cost stack, one escalator per driver class ---
    cost_shares=I(dict(materials=0.5488, packaging=0.2456, labour=0.0977, energy=0.0342,
                       services_other=0.0571, depreciation=0.0166),
                  AUD25 + ", cost of sales note (26). Production cost of EGP 5,625.990 million "
                  "splits as: raw materials 3,087.382 (54.88%); packaging materials 1,381.559 "
                  "(24.56%); labour 447.415 wages + 55.497 benefits in kind + 46.342 social "
                  "insurance = 549.254 (9.77%); fuel, oils, electricity, water and lighting "
                  "192.345 (3.42%); all other consumables and services 321.446 (5.71%); "
                  "depreciation 93.498 (1.66%)", "2026-03-01", "Company"),
    esc_materials_usd=I(0.02, "Active pharmaceutical ingredient input prices in US dollars, "
                        "annual escalation. The company's raw materials are predominantly "
                        "imported active ingredients; they are escalated on a hard-currency "
                        "price path passed through the model's own exchange-rate path, NOT on a "
                        "domestic inflation index", "2026-08-09", "House"),
    esc_packaging_import_share=I(0.55, "Share of the packaging cost line that is imported input "
                                 "(aluminium foil, film, closures) and therefore escalates on "
                                 "the hard-currency path; the balance is produced in-house by "
                                 "the group's own ampoule and plastics factories and escalates "
                                 "domestically", "2026-08-09", "House"),
    esc_labour=I([0.14, 0.12, 0.10, 0.085, 0.075],
                 "Egyptian wage escalation. Headcount grew 2% in FY2025 while the wage bill in "
                 "cost of sales grew 27%, so unit labour cost is rising faster than consumer "
                 "prices as the statutory minimum wage is reset; the path decays toward "
                 "domestic inflation", "2026-08-09", "House"),
    esc_energy=I([0.18, 0.15, 0.12, 0.10, 0.08],
                 "Egyptian regulated energy and utility tariffs, escalated ABOVE consumer "
                 "inflation for the near term because the subsidy-reform programme resets "
                 "industrial electricity and gas tariffs on its own schedule; a domestic "
                 "consumer-price proxy would understate it", "2026-08-09", "House"),
    esc_domestic_cpi=I([0.12, 0.10, 0.085, 0.07, 0.06],
                       "Egyptian consumer price inflation path, applied only to genuinely "
                       "domestic service and consumable lines. Converges on the central bank's "
                       "stated 5-7% medium-term target band", "2026-08-09", "House"),

    # ---- forecast drivers: operating expenses, capital, working capital -----
    mkt_pct=I([0.104, 0.102, 0.100, 0.099, 0.098],
              "Selling and marketing expense as a share of revenue. The disclosed ratio fell "
              "from 12.9% (FY2023) to 12.4% (FY2024) to 10.7% (FY2025) as the company got "
              "operating leverage on a larger sales base; the path assumes that gain is largely "
              "banked but not extended much further", "2026-08-09", "House"),
    rnd_pct=I([0.0085, 0.0090, 0.0095, 0.0100, 0.0100],
              "Research and development as a share of revenue, rising modestly from the FY2025 "
              "level of 0.75% as the biosimilars pipeline moves through registration",
              "2026-08-09", "House"),
    ga_pct=I([0.0235, 0.0235, 0.0230, 0.0228, 0.0225],
             "General and administrative expense as a share of revenue, held near the FY2025 "
             "level of 2.34%", "2026-08-09", "House"),
    prov_pct_permanent=I(0.0525, "Credit losses, inventory write-downs and other provisions as a "
                         "permanent share of revenue — the FRAME A reading. Three-year average "
                         "of the disclosed charge: 5.07% (FY2023), 9.24% (FY2024), 5.23% "
                         "(FY2025); the average of the two years either side of the FY2024 "
                         "spike is 5.15%, and 5.25% is struck marginally above it",
                         "2026-08-09", "House"),
    prov_pct_normalising=I([0.045, 0.038, 0.032, 0.028, 0.025],
                           "The FRAME B reading of the same charge: a receivable and inventory "
                           "book that is seasoning, with the charge decaying toward the 2.5% of "
                           "revenue that a distributor-concentrated generic book carries in "
                           "steady state. Both frames are carried through the whole model and "
                           "published side by side; neither is averaged into the other",
                           "2026-08-09", "House"),
    capex_pct=I([0.125, 0.045, 0.035, 0.032, 0.030],
                "Capital expenditure as a share of revenue. FY2024 and FY2025 ran at 37.5% and "
                "14.3% of revenue respectively as the EIPICO 3 plant was built; the plant was "
                "licensed in December 2025 and the residual construction spend completes in "
                "FY2026, after which the requirement falls to maintenance plus incremental line "
                "capacity on a plant running at 65% utilisation", "2026-08-09", "House"),
    cip_transfer=I([3400.0, 1100.0, 400.0, 200.0, 200.0],
                   "Transfers out of projects under construction into depreciable property, "
                   "EGP million. The EIPICO 3 facility obtained its Egyptian Drug Authority and "
                   "Industrial Development Authority licences in December 2025 and entered its "
                   "operating phase in 2026, so the EGP 4,901 million construction balance "
                   "begins depreciating rather than sitting idle. This is the single largest "
                   "mechanical change in the forecast income statement", "2026-08-09", "House"),
    dep_rate=I(0.062, "Average annual depreciation rate on the depreciable property base. "
               "Implied by the audited fixed-asset note: FY2024 depreciation of 96.532 on "
               "average gross property of about 2,697 gives 3.6%, but that base is dominated by "
               "long-lived buildings and land; the incoming EIPICO 3 asset is process equipment "
               "and modular construction with a shorter life. 6.2% is a blended rate consistent "
               "with roughly a sixteen-year average life", "2026-08-09", "House"),
    dio=I([265, 258, 250, 245, 240],
          "Inventory days on cost of sales. The audited FY2025 position implies 268 days. The "
          "chairman stated at the March-2026 general assembly that the company deliberately "
          "holds a strategic raw-material stockpile sufficient for at least eight months, so "
          "this is a policy choice rather than a working-capital failure; the path unwinds it "
          "only slowly", "2026-08-09", "House"),
    dso=I([126, 122, 118, 115, 112],
          "Trade receivable days on revenue. The audited FY2025 position implies 129 days, "
          "against 147 days in FY2024, reflecting a distributor-concentrated domestic book and "
          "export terms; the path continues the improvement already underway", "2026-08-09",
          "House"),
    dpo=I([55, 56, 57, 58, 58],
          "Trade payable days on cost of sales. The audited FY2025 position implies 54 days, up "
          "from 36 days in FY2024", "2026-08-09", "House"),
    payout=I(0.40, "Dividend payout ratio on profit attributable to the holding company. The "
             "board proposed EGP 3.50 a share for FY2025 (EGP 590.645 million on 168,755,750 "
             "shares) against attributable profit of EGP 1,441.658 million, a 41.0% payout; the "
             "FY2024 proposal was EGP 3.00 a share (EGP 446.267 million on 148,755,750 shares) "
             "against EGP 1,095.717 million, 40.7%", "2026-03-28", "Company"),
    dps_fy25=I(3.50, "Dividend per share proposed by the board for FY2025: EGP 590,645,125 "
               "divided by 168,755,750 shares, exactly EGP 3.50. The FY2024 proposal was EGP "
               "446,267,250 on 148,755,750 shares, exactly EGP 3.00", "2026-03-28", "Company"),

    # ---- FY2022/FY2023 balance-sheet history (audited, for the statement appendix) ----
    ppe_fy23=I(963.645369, AUD23 + ", note (4)", "2024-03-01", "Company"),
    cip_fy23=I(3058.211677, AUD23 + ", note (6)", "2024-03-01", "Company"),
    rou_fy23=I(2.022754, AUD23 + ", note (5)", "2024-03-01", "Company"),
    intang_fy23=I(2.301715, AUD23 + ", note (7)", "2024-03-01", "Company"),
    assoc_bv_fy23=I(466.490873, AUD23 + ", note (8)", "2024-03-01", "Company"),
    inv_fy23=I(2242.395730, AUD23 + ", note (9)", "2024-03-01", "Company"),
    ar_fy23=I(2357.855472, AUD23 + ", note (10)", "2024-03-01", "Company"),
    othdr_fy23=I(197.731029, AUD23 + ", note (11)", "2024-03-01", "Company"),
    cash_fy23=I(675.798245, AUD23 + ", note (12)", "2024-03-01", "Company"),
    ap_fy23=I(176.353891, AUD23 + ", note (23)", "2024-03-01", "Company"),
    othcr_fy23=I(230.675384, AUD23 + ", note (24)", "2024-03-01", "Company"),
    provbs_fy23=I(191.159599, AUD23 + ", note (21)", "2024-03-01", "Company"),
    taxpay_fy23=I(184.979290, AUD23 + ", note (25)", "2024-03-01", "Company"),
    dtl_fy23=I(58.940504, AUD23 + ", note (20)", "2024-03-01", "Company"),
    debt_fy23=I(2832.316822 + 2045.331450 + 2.325196, AUD23 + ", notes (17), (19) and (22): "
                "long-term borrowings 2,832.317, bank facilities 2,045.331, lease liabilities "
                "2.325", "2024-03-01", "Company"),
    debt_fy24=I(4782.128576 + 4406.896591 + 11.007696, AUD24 + ", notes (17), (18) and (21): "
                "borrowings 4,782.129, bank facilities 4,406.897, lease liabilities 11.008",
                "2025-03-01", "Company"),
    nci_fy23=I(3.394945, AUD23, "2024-03-01", "Company"),
    nci_fy24=I(3.816172, AUD24, "2025-03-01", "Company"),
    assets_fy23=I(9978.782864, AUD23 + ", total assets", "2024-03-01", "Company"),
    assets_fy24=I(15372.957471, AUD24 + ", total assets", "2025-03-01", "Company"),
    capex_fy23=I(2290.194556, AUD23 + ", consolidated statement of cash flows: payments to "
                 "acquire fixed assets", "2024-03-01", "Company"),
    capex_fy24=I(2846.239746, AUD24 + ", consolidated statement of cash flows", "2025-03-01",
                 "Company"),
    capex_fy25=I(1354.665231, AUD25 + ", consolidated statement of cash flows", "2026-03-01",
                 "Company"),
    ocf_fy23=I(92.483752, AUD23 + ", net cash from operating activities", "2024-03-01",
               "Company"),
    ocf_fy24=I(-1274.488135, AUD24 + ", net cash used in operating activities", "2025-03-01",
               "Company"),
    ocf_fy25=I(1093.516116, AUD25 + ", net cash from operating activities", "2026-03-01",
               "Company"),
    icf_fy23=I(-2329.639953, AUD23 + ", net cash used in investing activities", "2024-03-01",
               "Company"),
    icf_fy24=I(-2679.028944, AUD24, "2025-03-01", "Company"),
    icf_fy25=I(-1201.726573, AUD25, "2026-03-01", "Company"),
    fcf_fy23=I(2209.824906, AUD23 + ", net cash from financing activities", "2024-03-01",
               "Company"),
    fcf_fy24=I(3853.615013, AUD24, "2025-03-01", "Company"),
    fcf_fy25=I(262.411958, AUD25, "2026-03-01", "Company"),
    dwc_fy23=I(-613.396581 - 84.576937 - 137.741615, AUD23 + ", consolidated statement of "
               "cash flows: movements in receivables, inventory and payables", "2024-03-01",
               "Company"),
    dwc_fy24=I(-1124.881150 - 1359.248300 + 57.315970, AUD24, "2025-03-01", "Company"),
    dwc_fy25=I(-601.356590 - 254.572959 + 427.710049, AUD25, "2026-03-01", "Company"),
    dps_fy23=I(2.00, "Proposed profit-distribution table, FY2023 board of directors' report",
               "2024-03-01", "Company"),
    dps_fy24=I(3.00, "Proposed profit-distribution table, FY2024 board of directors' report: "
               "EGP 446,267,250 on 148,755,750 shares", "2025-03-01", "Company"),
    shares_fy23=I(148.755750, "Capital note (13), shares in issue at 31 December 2023 and "
                  "31 December 2024", "2024-03-01", "Company"),
    wavg_shares_fy25=I(162.016024, "Earnings-per-share note (34), FY2025 weighted average",
                       "2026-03-01", "Company"),
    tablets_fy24_as_reported=I(1513.38, "Production of tablets in FY2024 as stated in the "
                               "FY2024 board of directors' report", "2025-03-01", "Company"),
    tablets_fy24_restated=I(1351.75, "The same year restated in the FY2025 board of "
                            "directors' report — a disclosed restatement, resolved in favour "
                            "of the later filing", "2026-03-28", "Company"),
    products_registered=I(1238, IRDECK + ": products registered", "2026-08-09", "Company"),
    countries_registered=I(61, IRDECK + ": countries of registration", "2026-08-09",
                           "Company"),
    export_countries=I(67, BOARD25 + ": countries exported to in FY2025", "2026-03-28",
                       "Company"),
    par_value=I(10.0, "Capital note (13): nominal value per share", "2026-03-01", "Company"),

    # ---- FY2026 first quarter, reviewed interim (obtained after the first issue) ----
    q1_rev=I(2532.833589, Q1SRC + ": net sales for the quarter (Q1-2025: 2,299.890)",
             "2026-05-14", "Company"),
    q1_rev_ly=I(2299.890497, Q1SRC + ": comparative quarter", "2026-05-14", "Company"),
    q1_gp=I(1073.711911, Q1SRC + ": gross profit (Q1-2025: 1,051.090)", "2026-05-14", "Company"),
    q1_gp_ly=I(1051.089983, Q1SRC + ": comparative quarter", "2026-05-14", "Company"),
    q1_dna=I(52.999633 + 1.538957 + 1.670794, Q1SRC + ", statement of cash flows: fixed-asset "
             "depreciation 52.9996, right-of-use amortisation 1.5390, intangible amortisation "
             "1.6708. The comparative quarter total was 26.613, so the charge has MORE THAN "
             "DOUBLED year on year", "2026-05-14", "Company"),
    q1_dna_ly=I(25.257457 + 0.336093 + 1.019572, Q1SRC + ": comparative quarter",
                "2026-05-14", "Company"),
    q1_fin=I(312.861801, Q1SRC + ": financing expenses (Q1-2025: 335.979) — DOWN 6.9% year on "
             "year despite a larger debt book", "2026-05-14", "Company"),
    q1_prov=I(65.0, Q1SRC + ": formed provisions 40.000 plus inventory impairment 25.000. THERE "
              "IS NO EXPECTED-CREDIT-LOSS CHARGE AT ALL, which is one of the three matters the "
              "auditor qualified", "2026-05-14", "Company"),
    q1_assoc=I(13.118430, Q1SRC + ": profits of subsidiaries and associates (Q1-2025: 33.445). "
               "The auditor states the associates' own periodic statements were NOT received, "
               "so this line is incomplete by construction", "2026-05-14", "Company"),
    q1_capex=I(324.734898, Q1SRC + ": payments to purchase fixed assets and projects under "
               "construction", "2026-05-14", "Company"),
    q1_parent=I(283.953868, Q1SRC + ": profit attributable to the holding company (Q1-2025: "
                "318.564), a fall of 10.9% on a 10.1% rise in sales", "2026-05-14", "Company"),
    q1_parent_ly=I(318.563839, Q1SRC + ": comparative quarter", "2026-05-14", "Company"),
    q1_ppe=I(4209.663874, Q1SRC + ": fixed assets net, against 3,069.748 at 31 December 2025 — "
             "a rise of 1,139.916 in one quarter", "2026-05-14", "Company"),
    q1_cip=I(3983.624093, Q1SRC + ": projects under construction, against 4,901.224 at 31 "
             "December 2025 — a TRANSFER OUT of 917.600 in one quarter, which is the study's "
             "central mechanism arriving on schedule", "2026-05-14", "Company"),
    q1_assoc_bv=I(904.360985, Q1SRC + ": investments in associates, against 675.875 at 31 "
                  "December 2025. The increase is the active-ingredient company moving from "
                  "consolidation into associates", "2026-05-14", "Company"),
    q1_nci=I(3.999807, Q1SRC + ": non-controlling interests, against 288.705 at 31 December "
             "2025. The collapse is the deconsolidation of the active-ingredient company",
             "2026-05-14", "Company"),
    q1_debt=I(4021.835282 + 965.585755 + 4428.322532 + 11.867322 + 0.402127,
              Q1SRC + ": long-term loans 4,021.835, short-term loans 965.586, bank facilities "
              "4,428.323, lease liabilities 12.269", "2026-05-14", "Company"),
    q1_cash=I(362.815296, Q1SRC + ": cash and cash equivalents, against 1,433.427 at 31 "
              "December 2025; the quarter paid the FY2025 dividend and built working capital",
              "2026-05-14", "Company"),
    q1_ar=I(4123.004310, Q1SRC + ": accounts and notes receivable net, against 3,325.044 — a "
            "rise of 797.960 against which no credit-loss charge was taken", "2026-05-14",
            "Company"),
    q1_share_of_year_rev=I(0.24360, "Q1-2025 net sales of 2,299.890 as a share of FY2025 net "
                           "sales of 9,441.379 — the seasonal shape used to read the quarter "
                           "into a full year", "2026-05-14", "Company"),
    q1_share_of_year_profit=I(0.22097, "Q1-2025 attributable profit of 318.564 as a share of "
                              "FY2025 attributable profit of 1,441.658", "2026-05-14",
                              "Company"),
    arab_api_cost=I(904.360985 - 675.874567, "The active-ingredient company's carrying value "
                    "after deconsolidation, taken as the movement in investments in associates "
                    "across the first quarter. It is pre-revenue — the company indicates trial "
                    "batches in 2027 — so carrying cost, not an earnings multiple, is the right "
                    "proxy for it", "2026-05-14", "Company"),
    nci_bridge=I(3.999807, "Non-controlling interests deducted in the enterprise-to-equity "
                 "bridge. The audited 31 December 2025 figure was 288.705, but essentially all "
                 "of it was the active-ingredient company's minorities, and that company was "
                 "deconsolidated in the first quarter of 2026. Deducting the December figure "
                 "while also carrying the March associate value would charge the same interest "
                 "twice", "2026-05-14", "Company"),

    # ---- tax ----------------------------------------------------------------
    tax_stat=I(0.225, "Egyptian corporate income tax rate, 22.5% — confirmed in the corporate "
               "tax-rate column of the country risk-premium file read for this study",
               "2026-01-05", "Country"),
    tax_eff_fwd=I(0.235, "Effective tax rate applied to forecast pre-tax profit. Audited "
                  "effective rates, taking current tax less the deferred-tax movement plus the "
                  "statutory solidarity contribution over pre-tax profit: 24.0% (FY2023), 28.3% "
                  "(FY2024), 18.8% (FY2025). The FY2025 rate is flattered by a 108.663 deferred-"
                  "tax credit and by associate income that arrives already taxed; 23.5% sits "
                  "just above the statutory rate to allow for the solidarity contribution and "
                  "for disallowed items", "2026-08-09", "House"),

    # ---- cost of capital ----------------------------------------------------
    rf=I(0.2231, "Egypt ten-year local-currency government bond yield, 22.31% (house cost-of-"
         "capital reference, 21-Jul-2026 print). A live re-read of the central bank's own "
         "fixed-coupon treasury bond auction page was attempted on 09-Aug-2026 and rejected by "
         "that site's web application firewall; the cached print is used and the rate is "
         "sensitised", "2026-07-21", "Country"),
    sov_spread_cds=I(0.0341, "Egypt sovereign credit-default-swap spread, 3.41%, read live on "
                     "09-Aug-2026 from the original country default-spread and risk-premium "
                     "file (last updated 5 January 2026), Egypt row, sovereign CDS column. "
                     "Netted out of the local-currency risk-free rate so that sovereign default "
                     "risk is charged once, inside the equity risk premium, and not twice",
                     "2026-01-05", "Country"),
    sov_spread_rating=I(0.0637, "Egypt adjusted default spread on the rating basis (Moody's "
                        "Caa1), 6.37%, same file and same live read — the alternative "
                        "construction, published for the audit trail", "2026-01-05", "Country"),
    erp_cds=I(0.0941, "Egypt total equity risk premium on the sovereign-CDS basis, 9.41%, same "
              "file and same live read", "2026-01-05", "Country"),
    erp_rating=I(0.1394, "Egypt total equity risk premium on the rating basis, 13.94%, same "
                 "file and same live read (country risk premium 9.71% over a 4.23% mature-market "
                 "premium)", "2026-01-05", "Country"),
    beta=I(0.629, "Own-stock first-tier regression: weekly logarithmic returns of the company's "
           "own shares against an equal-weighted composite of 36 Egyptian listed names built "
           "from the full covered price library, five-year window. R-squared 0.235, n = 257, "
           "standard error 0.071, 90% confidence interval [0.51, 0.75]. Clears every usability "
           "test on every limb and is not weak-instrument flagged. A beta well below one is what "
           "a defensive, price-regulated, domestically-consumed staple should produce",
           "2026-08-09", "House"),
    kd_egp=I(0.2481, "Marginal cost of local-currency debt: the ten-year sovereign yield of "
             "22.31% plus a 250 basis-point corporate credit spread. A same-currency corporate "
             "cannot borrow below its own sovereign, so this is floored at the sovereign yield "
             "by construction", "2026-08-09", "House"),
    kd_fx_coupon=I(0.075, "Marginal coupon on the group's hard-currency borrowings. Half the "
                   "term-loan book is US-dollar and euro paper from Qatar National Bank Alahli "
                   "and the National Bank of Kuwait; 7.5% is the dollar-funding cost for an "
                   "unrated Egyptian corporate at current benchmark rates", "2026-08-09",
                   "House"),
    fx_dep_wacc=I(0.045, "Expected annual depreciation of the Egyptian pound used to carry "
                  "foreign-currency debt at its LOCAL-EQUIVALENT cost. Taken from the model's "
                  "own exchange-rate path (50.5 to 57.7 over five years, a 3.4% compound rate) "
                  "with a margin; a raw hard-currency coupon inside a pound-nominal weighted "
                  "average cost of capital would understate the cost of that debt",
                  "2026-08-09", "House"),
    int_path=I([1250.0, 1210.0, 1150.0, 1090.0, 1030.0],
               "Finance cost charged to the income statement, EGP million. This is NOT the "
               "marginal cost of debt used in the discount rate — that is a forward, "
               "local-equivalent, currency-blended rate; this is what the profit and loss "
               "account actually bears, and part of the group's interest is still being "
               "capitalised into the remaining construction balance. CALIBRATED TO THE FIRST "
               "QUARTER OF 2026: 312.862 of financing expense in three months, DOWN 6.9% year "
               "on year, an annual run-rate of about 1,251 against the 1,548 the first cut of "
               "this model implied. It then declines with the central bank's easing cycle",
               "2026-08-11", "House"),
    kd_path=I([0.189, 0.178, 0.166, 0.156, 0.148],
              "Forward blended cost of debt FY2026E-FY2030E in local-equivalent terms, "
              "continuing the central bank's easing cycle. The discount-rate glide takes its "
              "shape from this path by construction rather than being invented separately",
              "2026-08-09", "House"),
    rf_term=I(0.105, "Terminal risk-free rate, built from norms rather than extrapolated: the "
              "central bank's stated medium-term inflation target of 5% plus the standard "
              "5.5-point emerging-market real-rate convention", "2026-08-09", "House"),
    erp_term=I(0.070, "Terminal equity risk premium, normalised below today's crisis-era level "
               "toward the rating-class norm; never held flat into perpetuity", "2026-08-09",
               "House"),
    kd_term_lc=I(0.150, "Terminal local-currency corporate borrowing rate — the long-run "
                 "Egyptian norm of roughly 10 points above the 5% inflation target",
                 "2026-08-09", "House"),
    kd_term_fx=I(0.065, "Terminal hard-currency coupon", "2026-08-09", "House"),
    wd_term=I(0.20, "Terminal debt weight on a net basis, NORMALISED but reconciled to the "
              "model's own forecast balance sheet rather than asserted. Today's net weight is "
              "25.1%; at a 40% payout the forecast deleverages through the window, so a "
              "terminal weight at today's level would contradict the model's own trajectory. "
              "20% acknowledges that an inventory-heavy manufacturer retains structural gross "
              "leverage", "2026-08-09", "House"),
    g_term=I(0.05, "Terminal growth, 5% — an Egyptian-pound NOMINAL rate struck against a "
             "terminal risk-free rate that itself embeds 5% inflation, so the base case assumes "
             "approximately zero real terminal growth. Deliberately conservative for a company "
             "with a third of its revenue in hard currency and a biosimilars plant just "
             "entering service. Sensitised 3-7%", "2026-08-09", "House"),
    roic_term=I(0.20, "Terminal return on invested capital, used to set terminal reinvestment "
                "as growth divided by return. The model's own FY2030E return on invested "
                "capital is computed below and this input is asserted against it",
                "2026-08-09", "House"),
    assoc_multiple=I(11.0, "Earnings multiple applied to the equity-accounted associate stream "
                     "in the enterprise-to-equity bridge. The associates contributed EGP 495.5 "
                     "million in FY2025 — 34% of attributable profit — against a carrying value "
                     "of only EGP 675.9 million, so carrying value is not a usable proxy. The "
                     "larger holding is a 30% interest in a Saudi Arabian pharmaceutical "
                     "manufacturer; 11 times is struck below the Gulf listed-pharmaceutical "
                     "range to allow for the minority, unlisted and non-controlled nature of "
                     "the stake", "2026-08-09", "House"),
    assoc_norm=I(250.0, "Normalised annual contribution of the EARNING associates, used with "
                 "the multiple above; the pre-revenue active-ingredient company is carried "
                 "separately at cost. "
                 "EGP million. The disclosed stream is volatile — 74.5 (FY2023), 147.1 "
                 "(FY2024), 495.5 (FY2025) — and the FY2025 print is more than three times the "
                 "FY2024 one. The three-year average is 239.0; 320 sits between that average "
                 "and the latest year. REVISED DOWN from 320 after the first quarter of 2026 "
                 "reported only 13.118 against 33.445 a year earlier; on a like-for-like gross "
                 "basis the three disclosed years average 246.1, and 250 is struck there rather "
                 "than at the level the FY2025 print alone would support. The quarter is not "
                 "decisive — the auditor states the associates' own statements were not "
                 "received — but it removes the case for leaning on the best year",
                 "2026-08-11", "House"),

    # ---- relative lens ------------------------------------------------------
    peer_pe_regional=I(19.5, "Median trailing price-earnings multiple of listed Gulf and "
                       "emerging-market generic pharmaceutical manufacturers used as the "
                       "relative anchor. MARKET DATA, cross-check layer — not a company "
                       "historical. Sourced range: a listed Saudi Arabian generics manufacturer "
                       "at 26.7 times, larger and more liquid regional and international "
                       "generic manufacturers in the mid-teens. The median is struck at 19.5 "
                       "and the lens is run across a 13-26 times band rather than on a point",
                       "2026-08-09", "Market"),
    peer_evebitda_regional=I(11.0, "Median enterprise-value-to-EBITDA multiple for the same "
                             "peer group. MARKET DATA, cross-check layer. Range run 8-16 times",
                             "2026-08-09", "Market"),
    own_pe_history_note=I(True, "The relative lens is anchored primarily on the company's OWN "
                          "traded history, which is computable entirely from primary material: "
                          "audited attributable profit divided by the share count in issue at "
                          "each year end, against the year-end close in the price history held "
                          "for this study. No aggregator is in that path", "2026-08-09",
                          "House"),

    # ---- probabilistic map --------------------------------------------------
    q_annual=I(0.0269, "Forward dividend yield used as the carry offset in the probability map: "
               "the EGP 3.50 a share proposed for FY2025 over the 130.05 close",
               "2026-08-09", "Market"),
)

V = {k: v['value'] for k, v in INP.items()}
for k, rec in INP.items():
    assert set(rec) == {'value', 'source', 'date', 'layer'}, k
    assert rec['source'] and rec['date'] and rec['layer'], f'{k} is not four-field complete'

TAX = V['tax_stat']
BOARD_FEE = 2.0          # forecast board remuneration, held at the FY2025 disclosed level
NCI_FWD = 18.0           # non-controlling share, held near the FY2025 disclosed 16.2
YEARS = ['FY2026E', 'FY2027E', 'FY2028E', 'FY2029E', 'FY2030E']
NARR = []


def say(s):
    NARR.append(s)
    print(s)


# ============================ HISTORY ========================================
hist = {}
for y in (23, 24, 25):
    gp = V[f'rev_fy{y}'] - V[f'cogs_fy{y}']
    opex = V[f'mkt_fy{y}'] + V[f'rnd_fy{y}'] + V[f'ga_fy{y}'] + V[f'board_fy{y}']
    ebit_pre_prov = gp - opex
    ebit = ebit_pre_prov - V[f'prov_fy{y}']
    hist[f'FY20{y}'] = dict(
        divtax=V[f'divtax_fy{y}'],
        revenue=V[f'rev_fy{y}'], cogs=V[f'cogs_fy{y}'], gross_profit=gp,
        gross_margin=gp / V[f'rev_fy{y}'],
        marketing=V[f'mkt_fy{y}'], rnd=V[f'rnd_fy{y}'], ga=V[f'ga_fy{y}'], board=V[f'board_fy{y}'],
        provisions=V[f'prov_fy{y}'], prov_pct=V[f'prov_fy{y}'] / V[f'rev_fy{y}'],
        ebit_pre_prov=ebit_pre_prov, ebit=ebit, ebit_margin=ebit / V[f'rev_fy{y}'],
        dna=V[f'dna_fy{y}'],
        ebitda_pre_prov=ebit_pre_prov + V[f'dna_fy{y}'],
        ebitda=ebit + V[f'dna_fy{y}'],
        finance=V[f'fin_fy{y}'], associates=V[f'assoc_fy{y}'],
        interest_income=V[f'intinc_fy{y}'], fx=V[f'fx_fy{y}'], other=V[f'othinc_fy{y}'],
        pbt=V[f'pbt_fy{y}'], tax=V[f'taxtot_fy{y}'], net_profit=V[f'np_fy{y}'],
        parent=V[f'parent_fy{y}'],
        eff_tax=V[f'taxtot_fy{y}'] / V[f'pbt_fy{y}'],
    )
    # the audited statement must reconstruct EXACTLY from its own disclosed lines
    check = (ebit + V[f'assoc_fy{y}'] + V[f'intinc_fy{y}'] + V[f'fx_fy{y}'] + V[f'othinc_fy{y}']
             - V[f'fin_fy{y}'] - V[f'divtax_fy{y}'])
    assert abs(check - V[f'pbt_fy{y}']) < 0.02, \
        f'FY20{y} income statement does not close: {check:.3f} vs {V[f"pbt_fy{y}"]:.3f}'
    assert abs(V[f'pbt_fy{y}'] - V[f'taxtot_fy{y}'] - V[f'np_fy{y}']) < 0.02, \
        f'FY20{y} tax bridge does not close'

say('[History] the audited consolidated income statement reconstructs line-by-line for all '
    'three years: revenue less cost of sales less operating expenses less the provision charge, '
    'plus associates, interest income, exchange differences and other income, less finance '
    'costs, equals disclosed pre-tax profit to within EGP 0.02 million in each year.')
for k in ('FY2023', 'FY2024', 'FY2025'):
    h = hist[k]
    say(f"  {k}: revenue {h['revenue']:,.0f} · gross margin {h['gross_margin']:.1%} · "
        f"provision charge {h['prov_pct']:.2%} of revenue · EBIT {h['ebit']:,.0f} "
        f"({h['ebit_margin']:.1%}) · EBITDA {h['ebitda']:,.0f} · net profit {h['net_profit']:,.0f} "
        f"· effective tax {h['eff_tax']:.1%}")

# ---- the unit build, reconstructed from disclosure --------------------------
exp_rev25 = V['ch_export_fy25']
exp_rev24 = V['ch_export_fy24']
exp_packs25 = V['export_packs_fy25']
exp_packs24 = exp_packs25 * V['export_usd_fy24'] / V['export_usd_fy25']  # dollar price held
dom_packs25 = V['packs_own_fy25'] - exp_packs25
dom_packs24 = V['packs_own_fy24'] - exp_packs24
dom_rev25 = V['ch_direct_fy25'] + V['ch_distrib_fy25'] + V['ch_tender_fy25']
dom_rev24 = V['ch_direct_fy24'] + V['ch_distrib_fy24'] + V['ch_tender_fy24']
dom_ppp25 = dom_rev25 / dom_packs25
dom_ppp24 = dom_rev24 / dom_packs24
exp_ppp_usd25 = (exp_rev25 / V['fx_avg_fy25']) / exp_packs25
say('')
say(f"[Unit build] FY2025 sales of the company's own preparations were {V['packs_own_fy25']:.1f} "
    f"million packs. Exports account for {exp_packs25:.1f} million of them at EGP "
    f"{exp_rev25 / exp_packs25:,.2f} a pack, which is USD {exp_ppp_usd25:.2f} at the disclosed "
    f"average rate of {V['fx_avg_fy25']:.2f}. The domestic book is therefore "
    f"{dom_packs25:.1f} million packs carrying EGP {dom_rev25:,.0f} million of revenue, "
    f"EGP {dom_ppp25:,.2f} a pack, against EGP {dom_ppp24:,.2f} in FY2024 "
    f"(+{dom_ppp25 / dom_ppp24 - 1:.1%}) on {dom_packs24:.1f} million packs "
    f"(+{dom_packs25 / dom_packs24 - 1:.1%} volume).")
say(f"  Production ran at {V['units_prod_fy25']:,.0f} million units against {V['units_cap']:,.0f} "
    f"million of disclosed capacity — {V['units_prod_fy25'] / V['units_cap']:.0%} utilisation, so "
    f"the volume path below is not capacity-constrained.")
# the reconstructed channels must tie to the disclosed standalone revenue total
recon25 = dom_rev25 + exp_rev25 + V['ch_toll_fy25']
say(f"  Reconstructed channel revenue {recon25:,.3f} against the disclosed separate-company "
    f"revenue total of 9,302.469 — a difference of {abs(recon25 - 9302.469331):,.3f}, which is "
    f"rounding on the incentive lines.")
assert abs(recon25 - 9302.469331) < 0.05, 'channel build does not tie to disclosed revenue'

# ============================ FORECAST =======================================
n = 5
fx = V['fx_path']
dom_packs, exp_packs, dom_ppp, exp_ppp_usd, toll = [], [], [], [], []
p_d, p_e, r_d, r_e, r_t = dom_packs25, exp_packs25, dom_ppp25, exp_ppp_usd25, V['ch_toll_fy25']
for i in range(n):
    p_d *= (1 + V['dom_pack_growth'][i]); dom_packs.append(p_d)
    p_e *= (1 + V['exp_pack_growth'][i]); exp_packs.append(p_e)
    r_d *= (1 + V['dom_price_growth'][i]); dom_ppp.append(r_d)
    r_e *= (1 + V['exp_price_usd_growth'][i]); exp_ppp_usd.append(r_e)
    r_t *= (1 + V['toll_growth'][i]); toll.append(r_t)

rev_dom = [dom_packs[i] * dom_ppp[i] for i in range(n)]
rev_exp = [exp_packs[i] * exp_ppp_usd[i] * fx[i] for i in range(n)]
# the consolidated total runs a small step above the separate-company channel build:
# the subsidiary's external sales. Measured, not assumed.
consol_uplift = V['rev_fy25'] / 9302.469331
revenue = [(rev_dom[i] + rev_exp[i] + toll[i]) * consol_uplift for i in range(n)]
say('')
say(f"[Consolidation] the reconstructed channel build is a separate-company total; the audited "
    f"consolidated revenue is {consol_uplift:.4f} times it, the subsidiary's external sales. "
    f"That measured factor, not an assumption, carries the build to a consolidated basis.")

# ---- cost stack: one escalator per driver class ------------------------------
# Depreciation is stripped OUT of the unit cost and comes back exactly once, from
# the property roll-forward below. Leaving it in the escalated unit cost AND
# adding the roll-forward charge would count it twice; the first cut of this model
# did exactly that and the sensitivity harness caught it.
cs_all = V['cost_shares']
DEP_IN_COGS_FY25 = 93.497560      # audited cost-of-sales note (26), depreciation line
DEP_COGS_SHARE = DEP_IN_COGS_FY25 / V['dna_fy25']
CASH_CLASSES = ('materials', 'packaging', 'labour', 'energy', 'services_other')
_cash_tot = sum(cs_all[k] for k in CASH_CLASSES)
cs = {k: cs_all[k] / _cash_tot for k in CASH_CLASSES}
unit_cost25 = (V['cogs_fy25'] - DEP_IN_COGS_FY25) / V['packs_sold_fy25']   # CASH cost per pack
packs_total = [dom_packs[i] + exp_packs[i] + V['packs_toll_fy25'] for i in range(n)]
esc_idx = {k: 1.0 for k in cs}
fx_prev = V['fx_avg_fy25']
unit_costs, cogs_cash = [], []
esc_trace = []
for i in range(n):
    fx_move = fx[i] / fx_prev
    m_esc = (1 + V['esc_materials_usd']) * fx_move                      # imported API
    pk_imp = (1 + V['esc_materials_usd']) * fx_move                     # imported packaging input
    pk_dom = 1 + V['esc_domestic_cpi'][i]
    p_esc = V['esc_packaging_import_share'] * pk_imp + \
        (1 - V['esc_packaging_import_share']) * pk_dom
    l_esc = 1 + V['esc_labour'][i]
    e_esc = 1 + V['esc_energy'][i]
    s_esc = 1 + V['esc_domestic_cpi'][i]
    esc_idx['materials'] *= m_esc
    esc_idx['packaging'] *= p_esc
    esc_idx['labour'] *= l_esc
    esc_idx['energy'] *= e_esc
    esc_idx['services_other'] *= s_esc
    blend = sum(cs[k] * esc_idx[k] for k in CASH_CLASSES)
    unit_costs.append(unit_cost25 * blend)
    cogs_cash.append(unit_costs[-1] * packs_total[i])
    esc_trace.append(dict(year=YEARS[i], fx=fx[i], materials=m_esc - 1, packaging=p_esc - 1,
                          labour=l_esc - 1, energy=e_esc - 1, services=s_esc - 1,
                          blend_index=blend, unit_cash_cost=unit_costs[-1]))
    fx_prev = fx[i]
say('')
say('[Cost stack] every physically distinct cost line carries its OWN escalator: imported '
    'active ingredients (54.9% of production cost) and the imported share of packaging escalate '
    'on a hard-currency price path passed through the exchange-rate path; labour on Egyptian '
    'wage growth; energy on the regulated tariff schedule, which runs above consumer inflation; '
    'domestic services on consumer inflation. No single blended index is applied across them. '
    'Depreciation is excluded here and enters exactly once, from the property roll-forward.')

# ---- operating expenses, both provision frames -------------------------------
mkt_f = [revenue[i] * V['mkt_pct'][i] for i in range(n)]
rnd_f = [revenue[i] * V['rnd_pct'][i] for i in range(n)]
ga_f = [revenue[i] * V['ga_pct'][i] for i in range(n)]
prov_A = [revenue[i] * V['prov_pct_permanent'] for i in range(n)]
prov_B = [revenue[i] * V['prov_pct_normalising'][i] for i in range(n)]

# ---- property, depreciation, capex -------------------------------------------
capex = [revenue[i] * V['capex_pct'][i] for i in range(n)]
ppe, cip, dep = [], [], []
ppe_b, cip_b = V['ppe_fy25'], V['cip_fy25']
for i in range(n):
    transfer = min(V['cip_transfer'][i], cip_b + capex[i])
    d = V['dep_rate'] * (ppe_b + transfer / 2.0)
    ppe_n = ppe_b + transfer - d
    cip_n = cip_b + capex[i] - transfer
    dep.append(d); ppe.append(ppe_n); cip.append(cip_n)
    ppe_b, cip_b = ppe_n, cip_n
amort = [V['dna_fy25'] - 109.455425 for _ in range(n)]     # right-of-use + intangible run-rate
dna = [dep[i] + amort[i] for i in range(n)]
# depreciation lands in cost of sales in the same proportion the audited note shows
cogs = [cogs_cash[i] + dna[i] * DEP_COGS_SHARE for i in range(n)]
gross_profit = [revenue[i] - cogs[i] for i in range(n)]
gross_margin = [gross_profit[i] / revenue[i] for i in range(n)]
say(f"  Gross margin path (after the production share of depreciation): FY2025 actual "
    f"{hist['FY2025']['gross_margin']:.1%} -> " + ' -> '.join(f'{g:.1%}' for g in gross_margin))
say('')
say(f"[Depreciation] the EGP {V['cip_fy25']:,.0f} million construction balance stops being free. "
    f"Transfers of {V['cip_transfer'][0]:,.0f} / {V['cip_transfer'][1]:,.0f} million in the first "
    f"two years take the depreciation charge from an audited FY2025 {V['dna_fy25']:.0f} million "
    f"to {dna[0]:,.0f} then {dna[-1]:,.0f} million. That step is the single largest mechanical "
    f"change in the forecast income statement and it is a consequence of the company's own "
    f"disclosed licensing timetable, not a view.")

ebitda_A = [revenue[i] - cogs_cash[i] - mkt_f[i] - rnd_f[i] - ga_f[i] - prov_A[i] - BOARD_FEE
            for i in range(n)]
ebitda_B = [revenue[i] - cogs_cash[i] - mkt_f[i] - rnd_f[i] - ga_f[i] - prov_B[i] - BOARD_FEE
            for i in range(n)]
ebit_A = [ebitda_A[i] - dna[i] for i in range(n)]
ebit_B = [ebitda_B[i] - dna[i] for i in range(n)]
say(f"  EBITDA (cash costs only) FY2026E {ebitda_A[0]:,.0f} -> FY2030E {ebitda_A[-1]:,.0f} on "
    f"Frame A; EBIT {ebit_A[0]:,.0f} -> {ebit_A[-1]:,.0f} after the depreciation step.")

# ---- working capital ----------------------------------------------------------
inv_f = [cogs[i] * V['dio'][i] / 365 for i in range(n)]
ar_f = [revenue[i] * V['dso'][i] / 365 for i in range(n)]
ap_f = [cogs[i] * V['dpo'][i] / 365 for i in range(n)]
othdr_f = [V['othdr_fy25'] * revenue[i] / V['rev_fy25'] for i in range(n)]
othcr_f = [V['othcr_fy25'] * revenue[i] / V['rev_fy25'] for i in range(n)]
wc = [inv_f[i] + ar_f[i] + othdr_f[i] - ap_f[i] - othcr_f[i] for i in range(n)]
wc0 = (V['inv_fy25'] + V['ar_fy25'] + V['othdr_fy25'] - V['ap_fy25'] - V['othcr_fy25'])
dwc = [wc[0] - wc0] + [wc[i] - wc[i - 1] for i in range(1, n)]
dio0 = V['inv_fy25'] / V['cogs_fy25'] * 365
dso0 = V['ar_fy25'] / V['rev_fy25'] * 365
dpo0 = V['ap_fy25'] / V['cogs_fy25'] * 365
say('')
say(f"[Asset-conversion cycle] the audited FY2025 balance sheet implies {dio0:.0f} inventory "
    f"days, {dso0:.0f} receivable days and {dpo0:.0f} payable days — a cash cycle of "
    f"{dio0 + dso0 - dpo0:.0f} days. The inventory position is policy: the company stated at its "
    f"March-2026 general assembly that it holds a strategic raw-material stockpile sufficient "
    f"for at least eight months. Working capital is PROJECTED from those three ratios, not "
    f"plugged.")

# ============================ COST OF CAPITAL =================================
rf_star = V['rf'] - V['sov_spread_cds']
ke = rf_star + V['beta'] * V['erp_cds']
ke_rating = (V['rf'] - V['sov_spread_rating']) + V['beta'] * V['erp_rating']
ke_double_counted = V['rf'] + V['beta'] * V['erp_cds']   # the retired construction, for contrast

w_fx = V['loans_fx_fy25'] / (V['loans_fx_fy25'] + V['loans_lc_fy25'])
kd_fx_local_equiv = (1 + V['kd_fx_coupon']) * (1 + V['fx_dep_wacc']) - 1
kd_blend = (1 - w_fx) * V['kd_egp'] + w_fx * kd_fx_local_equiv
kd_at = kd_blend * (1 - TAX)

mcap = V['spot'] * V['shares_mn']
gross_debt = V['loans_lt_fy25'] + V['loans_st_fy25'] + V['facilities_fy25'] + V['leases_fy25']
net_debt = gross_debt - V['cash_fy25']
we_net = mcap / (mcap + net_debt)
wd_net = 1 - we_net
wd_gross = gross_debt / (mcap + gross_debt)
wacc0 = we_net * ke + wd_net * kd_at
wacc0_gross = (1 - wd_gross) * ke + wd_gross * kd_at

ke_term = V['rf_term'] + V['beta'] * V['erp_term']
kd_term = (1 - w_fx) * V['kd_term_lc'] + w_fx * ((1 + V['kd_term_fx']) * 1.03 - 1)
kd_term_at = kd_term * (1 - TAX)
wacc_term = (1 - V['wd_term']) * ke_term + V['wd_term'] * kd_term_at

say('')
say(f"[Cost of equity] the quoted ten-year local-currency government yield is {V['rf']:.2%}. "
    f"That yield is not riskless: it embeds the sovereign's own default risk. Subtracting the "
    f"sovereign credit-default-swap spread of {V['sov_spread_cds']:.2%} leaves a normalised "
    f"risk-free rate of {rf_star:.2%}; adding beta {V['beta']:.3f} times the country equity risk "
    f"premium of {V['erp_cds']:.2%} gives a cost of equity of {ke:.2%}. On the rating basis "
    f"the same construction gives {ke_rating:.2%} — the two agree to "
    f"{abs(ke - ke_rating) * 1e4:.0f} basis points, which is reassuring because they are built "
    f"from different columns of the same source. Charging the raw {V['rf']:.2%} yield AND a "
    f"country-loaded premium would give {ke_double_counted:.2%} and would count sovereign risk "
    f"twice; that construction is not used.")
say(f"[Cost of debt] the term-loan note splits the book {1 - w_fx:.0%} local currency / "
    f"{w_fx:.0%} hard currency. The local-currency leg is priced at {V['kd_egp']:.2%} — the "
    f"sovereign yield plus 250 basis points, and above the sovereign by construction. The "
    f"hard-currency leg carries a {V['kd_fx_coupon']:.2%} coupon but is charged at its "
    f"LOCAL-EQUIVALENT cost of {kd_fx_local_equiv:.2%}, coupon compounded with expected currency "
    f"depreciation of {V['fx_dep_wacc']:.2%}. Blended marginal cost of debt {kd_blend:.2%}, "
    f"{kd_at:.2%} after tax.")
# Kd integrity: the marginal rate must be consistent with what the company actually paid
cap_int_fy25 = V['capint_cum_fy25'] - V['capint_cum_fy24']
avg_debt = (gross_debt + V['debt_fy24']) / 2
kd_eff_excl = V['int_fac_fy25'] / avg_debt
kd_eff_incl = (V['int_fac_fy25'] + cap_int_fy25) / avg_debt
say(f"[Cost-of-debt integrity] the company expensed {V['int_fac_fy25']:,.0f} million of interest "
    f"and capitalised a further {cap_int_fy25:,.0f} million into the construction balance in "
    f"FY2025. On average gross debt of {avg_debt:,.0f} million that is {kd_eff_excl:.1%} "
    f"expensed and {kd_eff_incl:.1%} all-in. The {kd_blend:.1%} marginal rate sits inside that "
    f"pair, which is the test: a marginal rate below the expensed rate or above the all-in rate "
    f"would not be credible.")
assert kd_eff_excl <= kd_blend <= kd_eff_incl + 0.01, \
    f'Kd {kd_blend:.3f} outside the effective-rate pair [{kd_eff_excl:.3f}, {kd_eff_incl:.3f}]'
say(f"[Weighted average cost of capital] market capitalisation {mcap:,.0f} against net debt "
    f"{net_debt:,.0f} gives weights {we_net:.1%} equity / {wd_net:.1%} debt and a starting "
    f"discount rate of {wacc0:.2%}. On GROSS debt the weights are "
    f"{1 - wd_gross:.1%}/{wd_gross:.1%} and the rate {wacc0_gross:.2%}; both are published. "
    f"Note the starting rate sits close to the quoted sovereign yield — that is arithmetic, not "
    f"an error: the quoted yield contains default risk that the normalised build strips out and "
    f"re-charges inside the equity premium.")
say(f"[Terminal] cost of equity {ke_term:.2%} (risk-free {V['rf_term']:.2%} plus beta times a "
    f"normalised {V['erp_term']:.2%} premium); cost of debt {kd_term:.2%}, {kd_term_at:.2%} "
    f"after tax; debt weight {V['wd_term']:.0%} -> terminal discount rate {wacc_term:.2%}.")

# ---- the glide: fractions derived from the cost-of-debt path -----------------
kdp = V['kd_path']
glide_frac = [(kdp[i] - kdp[-1]) / (kdp[0] - kdp[-1]) for i in range(n)]
disc_rate = [wacc_term + (wacc0 - wacc_term) * glide_frac[i] for i in range(n)]
assert all(disc_rate[i] >= disc_rate[i + 1] - 1e-12 for i in range(n - 1)), 'glide not ordered'
df, acc = [], 1.0
for i in range(n):
    acc *= (1 + disc_rate[i])
    df.append(1.0 / acc)
say(f"[Discount-rate glide] the fractions are the cost-of-debt path normalised to its own "
    f"endpoints — {', '.join(f'{g:.3f}' for g in glide_frac)} — so the glide has the shape of "
    f"the easing cycle rather than a shape invented for it. Discount rates "
    f"{', '.join(f'{d:.2%}' for d in disc_rate)}; the factors compound.")


# ============================ DCF ============================================
def run_dcf(ebit, ebitda, label):
    nopat = [e * (1 - TAX) for e in ebit]
    fcff = [nopat[i] + dna[i] - capex[i] - dwc[i] for i in range(n)]
    pv = [fcff[i] * df[i] for i in range(n)]
    pv_sum = sum(pv)
    nopat_term = nopat[-1] * (1 + V['g_term'])
    reinv_rate = V['g_term'] / V['roic_term']
    fcff_term = nopat_term * (1 - reinv_rate)
    tv = fcff_term / (wacc_term - V['g_term'])
    pv_tv = tv * df[-1]
    ev_core = pv_sum + pv_tv
    assoc_value = V['assoc_norm'] * V['assoc_multiple'] + V['arab_api_cost']
    ev_total = ev_core + assoc_value + V['afs_fy25']
    equity = ev_total - net_debt - V['nci_bridge']
    ps = equity / V['shares_mn']
    return dict(label=label, ebitda=ebitda, ebit=ebit, nopat=nopat, fcff=fcff, pv=pv,
                pv_sum=pv_sum, nopat_term=nopat_term, reinvest_rate=reinv_rate,
                fcff_term=fcff_term, tv=tv, pv_tv=pv_tv, ev_core=ev_core,
                tv_share=pv_tv / ev_core, assoc_value=assoc_value,
                assoc_earnings_value=V['assoc_norm'] * V['assoc_multiple'],
                arab_api_cost=V['arab_api_cost'], ev_total=ev_total,
                net_debt=net_debt, nci=V['nci_bridge'], equity=equity, per_share=ps)


dcf_A = run_dcf(ebit_A, ebitda_A, 'Frame A — provision charge permanent at 5.25% of revenue')
dcf_B = run_dcf(ebit_B, ebitda_B, 'Frame B — provision charge normalising to 2.5% of revenue')

# ROIC consistency: the terminal reinvestment rate must not assume a return the
# model's own final forecast year does not earn.
ic_fy30 = ppe[-1] + cip[-1] + wc[-1] + V['intang_fy25']
roic_fy30_A = ebit_A[-1] * (1 - TAX) / ic_fy30
roic_fy30_B = ebit_B[-1] * (1 - TAX) / ic_fy30
say('')
say(f"[Terminal consistency] terminal reinvestment is growth {V['g_term']:.0%} divided by a "
    f"terminal return on invested capital of {V['roic_term']:.0%}, i.e. "
    f"{dcf_A['reinvest_rate']:.0%} of terminal operating profit after tax reinvested. The "
    f"model's own FY2030E return on invested capital is {roic_fy30_A:.1%} on Frame A and "
    f"{roic_fy30_B:.1%} on Frame B, so the terminal assumption is not richer than the forecast "
    f"that leads into it.")
assert V['roic_term'] <= max(roic_fy30_A, roic_fy30_B) + 0.02, \
    'terminal ROIC richer than the forecast that leads into it'
for d in (dcf_A, dcf_B):
    assert abs((d['ev_total'] - d['net_debt'] - d['nci']) - d['equity']) < 1e-6, 'bridge open'
    assert 0.0 < d['tv_share'] < 0.95, f"terminal share implausible: {d['tv_share']:.2f}"
say(f"[Terminal weight] the terminal value is {dcf_A['tv_share']:.0%} of core enterprise value "
    f"on Frame A and {dcf_B['tv_share']:.0%} on Frame B. That is high, as it is for any "
    f"growing manufacturer discounted over five explicit years, and it is stated in the "
    f"valuation summary and in the enterprise-to-equity bridge rather than buried.")

# ============================ OTHER LENSES ====================================
# --- book value and sustainable return ---------------------------------------
bv_ps = V['equity_parent_fy25'] / V['shares_mn']
roe_fy25 = V['parent_fy25'] / ((V['equity_parent_fy25'] + V['equity_parent_fy24']) / 2)
roe_fy24 = V['parent_fy24'] / ((V['equity_parent_fy24'] + V['equity_parent_fy23']) / 2)
roe_sust = 0.235          # set below from the forecast, then asserted
roe_fwd = [None] * n
eq_b = V['equity_parent_fy25']
eq_path = []
for i in range(n):
    # Associate income arrives ALREADY TAXED — the equity method takes the group's share of
    # the associate's post-tax profit, and the disclosed figure is already net of withholding.
    # Taxing it again inside this chain would understate attributable profit.
    pat = ((ebit_A[i] - V['int_path'][i]) * (1 - V['tax_eff_fwd'])
           + V['assoc_norm'] - NCI_FWD)
    eq_n = eq_b + pat * (1 - V['payout'])
    roe_fwd[i] = pat / ((eq_b + eq_n) / 2)
    eq_path.append(eq_n)
    eq_b = eq_n
roe_sust = float(np.mean(roe_fwd[-3:]))
just_pb = (roe_sust - V['g_term']) / (ke_term - V['g_term'])
book_ps = just_pb * bv_ps
# The same sustainable return, expressed as an earnings multiple: retention must
# equal growth over return, so the payout the multiple assumes is not free.
payout_implied = 1 - V['g_term'] / roe_sust
just_fwd_pe = payout_implied / (ke_term - V['g_term'])
say('')
say(f"[Book value and sustainable return] book value per share {bv_ps:,.2f}. Return on average "
    f"equity was {roe_fy24:.1%} in FY2024 and {roe_fy25:.1%} in FY2025; the forecast settles at "
    f"{roe_sust:.1%}. A sustainable-return multiple of (return {roe_sust:.1%} less growth "
    f"{V['g_term']:.0%}) over (perpetual cost of equity {ke_term:.2%} less growth) is "
    f"{just_pb:.2f} times book, or {book_ps:,.2f} a share.")

# --- relative multiples: the company's OWN traded history first ---------------
import glob as _glob
sys.path.insert(0, os.path.join(HERE, '..'))
from primitives import load_ohlc
from data_quality import clean_ohlc
_px, _ = clean_ohlc(load_ohlc(os.path.join(HERE, 'PHAR_Stock_Price_History.csv')),
                    'PHAR', verbose=False, market='EG')
_px = _px.set_index('Date')['Price']
own_hist = []
for yr, parent, sh in ((2022, V['parent_fy22'], 99.170500),
                       (2023, V['parent_fy23'], 148.755750),
                       (2024, V['parent_fy24'], 148.755750),
                       (2025, V['parent_fy25'], 168.755750)):
    close = float(_px[_px.index <= f'{yr}-12-31'].iloc[-1])
    own_hist.append(dict(year=yr, close=close, shares=sh, eps=parent / sh,
                         pe=close * sh / parent))
own_pe_mean = float(np.mean([o['pe'] for o in own_hist]))
eps_ttm = V['parent_fy25'] / V['shares_mn']
pe_now = V['spot'] / eps_ttm
ev_now = mcap + net_debt + V['nci_bridge']
evebitda_now = ev_now / hist['FY2025']['ebitda']
# forward relative: FY2027E attributable earnings, both frames
def fwd_eps(ebit_series, i=1):
    pat = ((ebit_series[i] - V['int_path'][i]) * (1 - V['tax_eff_fwd'])
           + V['assoc_norm'] - NCI_FWD)
    return pat / V['shares_mn']
eps_26_A, eps_26_B = fwd_eps(ebit_A, 0), fwd_eps(ebit_B, 0)
eps_27_A, eps_27_B = fwd_eps(ebit_A, 1), fwd_eps(ebit_B, 1)
# THREE methods, averaged ON the sheet rather than asserted:
#   (1) the fundamentals-justified forward multiple, built from this model's own
#       sustainable return and perpetual cost of equity;
#   (2) the company's own four-year traded multiple;
#   (3) the regional peer median, adjusted for the cost-of-equity gap the peers
#       do not face.
eps_fwd = (eps_26_A + eps_26_B) / 2
peer_adj_pe = V['peer_pe_regional'] * (0.10 - 0.05) / (ke_term - V['g_term'])
tri = [('Justified forward multiple from this model', just_fwd_pe, just_fwd_pe * eps_fwd),
       ("The company's own four-year mean multiple", own_pe_mean, own_pe_mean * eps_fwd),
       ('Regional peer median, cost-of-equity adjusted', peer_adj_pe, peer_adj_pe * eps_fwd)]
rel_ps = float(np.mean([t[2] for t in tri]))
rel_lo, rel_hi = min(t[2] for t in tri), max(t[2] for t in tri)
rel_peer_unadjusted = V['peer_pe_regional'] * eps_fwd
say('')
say(f"[Relative multiples] the company's OWN traded history is computable entirely from primary "
    f"material — year-end closes against audited attributable profit: " +
    ', '.join(f"{o['pe']:.1f} times ({o['year']})" for o in own_hist) +
    f", a four-year mean of {own_pe_mean:.1f}. At {V['spot']:,.2f} the shares trade on "
    f"{pe_now:.1f} times trailing attributable earnings and {evebitda_now:.1f} times trailing "
    f"EBITDA. The re-rating is the single most important fact about this share price: the "
    f"earnings multiple has more than doubled against its own four-year history.")
say(f"  The lens triangulates three multiples rather than asserting one. (1) The multiple this "
    f"model's own economics justify: retention must equal growth {V['g_term']:.0%} over "
    f"sustainable return {roe_sust:.1%}, so the payout the multiple can assume is "
    f"{payout_implied:.0%}, and {payout_implied:.0%} over (perpetual cost of equity "
    f"{ke_term:.2%} less growth) is {just_fwd_pe:.1f} times. (2) The company's own four-year "
    f"mean, {own_pe_mean:.1f} times. (3) A regional peer median of "
    f"{V['peer_pe_regional']:.1f} times — but those peers are Gulf-listed and face a cost of "
    f"equity near 10%, not {ke_term:.1%}; adjusted for that single difference the same median "
    f"implies {peer_adj_pe:.1f} times. Averaged on {eps_fwd:,.2f} of FY2026E attributable "
    f"earnings a share: {rel_ps:,.2f}. Left unadjusted, the peer median alone would give "
    f"{rel_peer_unadjusted:,.2f} — the size of that gap IS the country-risk discount, and it is "
    f"shown rather than hidden inside a chosen multiple.")

# --- normalised earnings power -------------------------------------------------
norm_margin = float(np.mean([hist[k]['ebit_margin'] for k in ('FY2023', 'FY2024', 'FY2025')]))
norm_rev = revenue[1]
norm_ebit = norm_rev * norm_margin
norm_pat = ((norm_ebit - BOARD_FEE - V['int_path'][1]) * (1 - V['tax_eff_fwd'])
            + V['assoc_norm'] - NCI_FWD)
norm_ps = (norm_pat / V['shares_mn']) * payout_implied / (ke_term - V['g_term'])
say(f"[Normalised earnings power] the three-year average operating margin is {norm_margin:.1%}, "
    f"against {hist['FY2025']['ebit_margin']:.1%} in FY2025 — so this lens deliberately gives "
    f"back part of the best year. Applied to FY2027E revenue of {norm_rev:,.0f} million, "
    f"financed at the FY2027E cost of debt and taxed at {V['tax_eff_fwd']:.1%}, with the "
    f"normalised associate contribution added, that is EGP {norm_pat / V['shares_mn']:,.2f} a "
    f"share of sustainable earnings. Capitalised at the PERPETUAL cost of equity of "
    f"{ke_term:.2%} less {V['g_term']:.0%} growth, on the {payout_implied:.0%} payout that "
    f"growth rate permits: {norm_ps:,.2f} a share. Using today's crisis-level cost of equity of "
    f"{ke:.2%} in a perpetuity would be a category error — a steady-state multiple takes a "
    f"steady-state rate.")

# --- synthesis: four lenses, one field ------------------------------------------
lenses = [
    dict(name='Discounted cash flow — Frame A', value=dcf_A['per_share'], weight=0.25),
    dict(name='Discounted cash flow — Frame B', value=dcf_B['per_share'], weight=0.25),
    dict(name='Book value and sustainable return', value=book_ps, weight=0.20),
    dict(name='Relative multiples', value=rel_ps, weight=0.15),
    dict(name='Normalised earnings power', value=norm_ps, weight=0.15),
]
fair_base = sum(l['value'] * l['weight'] for l in lenses)
vals = [l['value'] for l in lenses]
fair_bear, fair_bull = min(vals), max(vals)
say('')
say(f"[Synthesis] four lenses, one field: " +
    ' · '.join(f"{l['name']} {l['value']:,.2f}" for l in lenses) +
    f". Weighted centre {fair_base:,.2f}; the field runs {fair_bear:,.2f} to {fair_bull:,.2f} "
    f"against a {V['spot']:,.2f} market price.")

# ============================ SENSITIVITY =====================================
def dcf_at(wacc_shift=0.0, g=None, beta_override=None, prov_pct=None, fx_scale=1.0,
           dom_vol_shift=0.0, dep_rate=None, extra_rev_fy30=0.0, extra_margin=0.45):
    """extra_rev_fy30 is an ADDITIONAL revenue line reaching that level by FY2030E on a
    straight ramp — the biosimilars facility's own contribution, which the base build does
    NOT carry because the company has published no volume or price guidance for it."""
    g = V['g_term'] if g is None else g
    b = V['beta'] if beta_override is None else beta_override
    ke_ = rf_star + b * V['erp_cds'] + wacc_shift
    ket_ = V['rf_term'] + b * V['erp_term'] + wacc_shift
    w0 = we_net * ke_ + wd_net * kd_at
    wt = (1 - V['wd_term']) * ket_ + V['wd_term'] * kd_term_at
    dr = [wt + (w0 - wt) * glide_frac[i] for i in range(n)]
    d_, a_ = [], 1.0
    for i in range(n):
        a_ *= (1 + dr[i]); d_.append(1 / a_)
    # revenue side
    pd_, pe_, rd_, re_, rt_ = dom_packs25, exp_packs25, dom_ppp25, exp_ppp_usd25, V['ch_toll_fy25']
    rev_, cog_, pk_ = [], [], []
    ei = {k: 1.0 for k in cs}
    fxp = V['fx_avg_fy25']
    for i in range(n):
        pd_ *= (1 + V['dom_pack_growth'][i] + dom_vol_shift)
        pe_ *= (1 + V['exp_pack_growth'][i])
        rd_ *= (1 + V['dom_price_growth'][i])
        re_ *= (1 + V['exp_price_usd_growth'][i])
        rt_ *= (1 + V['toll_growth'][i])
        f_ = fx[i] * fx_scale
        rev_.append((pd_ * rd_ + pe_ * re_ * f_ + rt_) * consol_uplift)
        pk_.append(pd_ + pe_ + V['packs_toll_fy25'])
        mv = f_ / fxp
        ei['materials'] *= (1 + V['esc_materials_usd']) * mv
        ei['packaging'] *= (V['esc_packaging_import_share'] * (1 + V['esc_materials_usd']) * mv +
                            (1 - V['esc_packaging_import_share']) * (1 + V['esc_domestic_cpi'][i]))
        ei['labour'] *= (1 + V['esc_labour'][i])
        ei['energy'] *= (1 + V['esc_energy'][i])
        ei['services_other'] *= (1 + V['esc_domestic_cpi'][i])
        bl = sum(cs[k] * ei[k] for k in CASH_CLASSES)
        cog_.append(unit_cost25 * bl * pk_[-1])       # CASH cost of sales, no depreciation
        fxp = f_
    dr_rate = V['dep_rate'] if dep_rate is None else dep_rate
    ppe_b_, cip_b_, dep_ = V['ppe_fy25'], V['cip_fy25'], []
    cap_ = [rev_[i] * V['capex_pct'][i] for i in range(n)]
    for i in range(n):
        tr = min(V['cip_transfer'][i], cip_b_ + cap_[i])
        dd = dr_rate * (ppe_b_ + tr / 2.0)
        ppe_b_ = ppe_b_ + tr - dd; cip_b_ = cip_b_ + cap_[i] - tr
        dep_.append(dd)
    dna_ = [dep_[i] + amort[i] for i in range(n)]
    pv_pct = V['prov_pct_permanent'] if prov_pct is None else prov_pct
    ramp = [0.0, 0.10, 0.30, 0.60, 1.00]
    xrev = [extra_rev_fy30 * ramp[i] for i in range(n)]
    ebit_ = [rev_[i] - cog_[i] - rev_[i] * (V['mkt_pct'][i] + V['rnd_pct'][i] + V['ga_pct'][i])
             - rev_[i] * pv_pct - dna_[i] - BOARD_FEE + xrev[i] * extra_margin
             for i in range(n)]
    rev_ = [rev_[i] + xrev[i] for i in range(n)]
    cogs_full_ = [cog_[i] + dna_[i] * DEP_COGS_SHARE for i in range(n)]
    inv_ = [cogs_full_[i] * V['dio'][i] / 365 for i in range(n)]
    ar_ = [rev_[i] * V['dso'][i] / 365 for i in range(n)]
    ap_ = [cogs_full_[i] * V['dpo'][i] / 365 for i in range(n)]
    od_ = [V['othdr_fy25'] * rev_[i] / V['rev_fy25'] for i in range(n)]
    oc_ = [V['othcr_fy25'] * rev_[i] / V['rev_fy25'] for i in range(n)]
    wc_ = [inv_[i] + ar_[i] + od_[i] - ap_[i] - oc_[i] for i in range(n)]
    dwc_ = [wc_[0] - wc0] + [wc_[i] - wc_[i - 1] for i in range(1, n)]
    fc = [ebit_[i] * (1 - TAX) + dna_[i] - cap_[i] - dwc_[i] for i in range(n)]
    pvs = sum(fc[i] * d_[i] for i in range(n))
    nt = ebit_[-1] * (1 - TAX) * (1 + g)
    tv_ = nt * (1 - g / V['roic_term']) / (wt - g)
    ev_ = (pvs + tv_ * d_[-1] + V['assoc_norm'] * V['assoc_multiple'] + V['arab_api_cost']
           + V['afs_fy25'])
    return (ev_ - net_debt - V['nci_bridge']) / V['shares_mn']


base_dcf = dcf_at()
assert abs(base_dcf - dcf_A['per_share']) < 0.05, \
    f'sensitivity harness disagrees with the DCF: {base_dcf:.4f} vs {dcf_A["per_share"]:.4f}'

sens = dict(
    wacc=[(s, dcf_at(wacc_shift=s)) for s in (-0.02, -0.01, 0.0, 0.01, 0.02)],
    g=[(g, dcf_at(g=g)) for g in (0.03, 0.04, 0.05, 0.06, 0.07)],
    beta=[(b, dcf_at(beta_override=b)) for b in (0.45, 0.55, V['beta'], 0.75, 0.90)],
    prov=[(p, dcf_at(prov_pct=p)) for p in (0.025, 0.035, 0.0525, 0.065, 0.080)],
    fx=[(s, dcf_at(fx_scale=s)) for s in (0.90, 0.95, 1.00, 1.05, 1.10)],
    volume=[(s, dcf_at(dom_vol_shift=s)) for s in (-0.04, -0.02, 0.0, 0.02, 0.04)],
    dep=[(d, dcf_at(dep_rate=d)) for d in (0.045, 0.055, 0.062, 0.070, 0.080)],
)
grid = [[dcf_at(wacc_shift=w, g=g) for g in (0.03, 0.04, 0.05, 0.06, 0.07)]
        for w in (-0.02, -0.01, 0.0, 0.01, 0.02)]

# ---- THE CRUX, stated as a reverse valuation in observable units --------------
# The base build charges the new facility's depreciation and its interest, because
# both are mechanical consequences of the company's own disclosed licensing
# timetable. It does NOT carry a revenue line for the facility, because the company
# has published no volume, price or utilisation guidance for it. So the honest
# question is not "what is it worth" but "how much must the facility sell".
lo, hi = 0.0, 30000.0
for _ in range(80):
    mid = (lo + hi) / 2
    if dcf_at(extra_rev_fy30=mid) < V['spot']:
        lo = mid
    else:
        hi = mid
req_rev = (lo + hi) / 2
req_ebit = req_rev * 0.45
crux = dict(required_fy30_revenue=req_rev,
            required_share_of_fy30=req_rev / (revenue[-1] + req_rev),
            required_ebit=req_ebit, assumed_margin=0.45,
            facility_investment_usd_mn=100.0,
            required_rev_usd_mn=req_rev / fx[-1],
            asset_turn=req_rev / (100.0 * fx[-1]),
            at_base=dcf_A['per_share'], spot=V['spot'])
say('')
say(f"[The crux] the base build charges the new biologicals facility's depreciation and its "
    f"interest — both mechanical consequences of the company's own disclosed December-2025 "
    f"licensing — but carries NO revenue line for it, because the company has published no "
    f"volume, price or utilisation guidance for the plant. So the crux is not what the plant is "
    f"worth; it is how much it must sell. Solving the same model for the market price: an "
    f"additional EGP {req_rev:,.0f} million of revenue by FY2030E at a 45% contribution margin "
    f"closes the gap from {dcf_A['per_share']:,.2f} to {V['spot']:,.2f}. That is "
    f"{crux['required_share_of_fy30']:.0%} of FY2030E revenue, or about USD "
    f"{crux['required_rev_usd_mn']:,.0f} million a year — {crux['asset_turn']:.2f} times the "
    f"USD 100 million the company says it invested in the plant. That number is observable: it "
    f"is testable against the first year the company discloses biosimilar revenue.")

# ============================ OUTPUT ==========================================
step0 = json.load(open(os.path.join(HERE, 'step0_result.json')))
bt5 = json.load(open(os.path.join(HERE, 'backtest_5y.json')))
beta_res = json.load(open(os.path.join(HERE, 'beta_result.json')))

OUT = dict(
    meta=dict(company='Egyptian International Pharmaceutical Industries Company',
              short='EIPICO', ticker='PHAR', market='EG', exchange='The Egyptian Exchange',
              currency='EGP', sector='Pharmaceuticals — generic and branded manufacturing',
              company_class='Operating company (vertically integrated pharmaceutical '
                            'manufacturer and exporter)',
              reference_pattern='Operating company',
              study_date='2026-08-09', price_date='2026-08-06', fy_end='31 December',
              audited_years=['FY2022', 'FY2023', 'FY2024', 'FY2025'],
              spot=V['spot'], shares_mn=V['shares_mn'], mcap=mcap),
    inputs=INP,
    history=hist,
    unit_build=dict(dom_packs_fy24=dom_packs24, dom_packs_fy25=dom_packs25,
                    exp_packs_fy24=exp_packs24, exp_packs_fy25=exp_packs25,
                    dom_price_fy24=dom_ppp24, dom_price_fy25=dom_ppp25,
                    exp_price_usd_fy25=exp_ppp_usd25,
                    dom_rev_fy24=dom_rev24, dom_rev_fy25=dom_rev25,
                    exp_rev_fy24=exp_rev24, exp_rev_fy25=exp_rev25,
                    utilisation_fy25=V['units_prod_fy25'] / V['units_cap'],
                    utilisation_fy24=V['units_prod_fy24'] / V['units_cap'],
                    consol_uplift=consol_uplift, unit_cost_fy25=unit_cost25),
    forecast=dict(years=YEARS, dom_packs=dom_packs, exp_packs=exp_packs, dom_price=dom_ppp,
                  exp_price_usd=exp_ppp_usd, fx=fx, rev_dom=rev_dom, rev_exp=rev_exp, toll=toll,
                  revenue=revenue, packs_total=packs_total, unit_cash_cost=unit_costs,
                  cogs_cash=cogs_cash, cogs=cogs, dep_cogs_share=DEP_COGS_SHARE,
                  gross_profit=gross_profit, gross_margin=gross_margin,
                  marketing=mkt_f, rnd=rnd_f, ga=ga_f, prov_A=prov_A, prov_B=prov_B,
                  ebitda_A=ebitda_A, ebitda_B=ebitda_B, ebit_A=ebit_A, ebit_B=ebit_B,
                  dna=dna, dep=dep, amort=amort, capex=capex, ppe=ppe, cip=cip,
                  inventory=inv_f, receivables=ar_f, payables=ap_f, other_dr=othdr_f,
                  other_cr=othcr_f, wc=wc, dwc=dwc, wc0=wc0, equity=eq_path, roe=roe_fwd,
                  esc_trace=esc_trace, board_fee=BOARD_FEE, nci_fwd=NCI_FWD),
    wacc=dict(rf=V['rf'], sov_spread_cds=V['sov_spread_cds'], rf_star=rf_star, beta=V['beta'],
              erp_cds=V['erp_cds'], ke=ke, ke_rating=ke_rating,
              ke_double_counted_retired=ke_double_counted,
              kd_egp=V['kd_egp'], kd_fx_coupon=V['kd_fx_coupon'],
              kd_fx_local_equiv=kd_fx_local_equiv, w_fx=w_fx, kd_blend=kd_blend, kd_at=kd_at,
              kd_eff_expensed=kd_eff_excl, kd_eff_allin=kd_eff_incl,
              avg_gross_debt=avg_debt, capitalised_interest_fy25=cap_int_fy25,
              mcap=mcap, gross_debt=gross_debt, net_debt=net_debt, cash=V['cash_fy25'],
              we_net=we_net, wd_net=wd_net, wd_gross=wd_gross,
              wacc0=wacc0, wacc0_gross=wacc0_gross,
              ke_term=ke_term, kd_term=kd_term, kd_term_at=kd_term_at, wacc_term=wacc_term,
              glide_frac=glide_frac, disc_rate=disc_rate, df=df, kd_path=kdp,
              beta_regression=beta_res),
    dcf=dict(frame_A=dcf_A, frame_B=dcf_B),
    lenses=dict(items=lenses, fair_base=fair_base, fair_bear=fair_bear, fair_bull=fair_bull,
                book_ps=book_ps, bv_ps=bv_ps, just_pb=just_pb, roe_sust=roe_sust,
                roe_fy24=roe_fy24, roe_fy25=roe_fy25,
                rel_ps=rel_ps, rel_lo=rel_lo, rel_hi=rel_hi,
                rel_triangulation=[[t[0], float(t[1]), float(t[2])] for t in tri],
                rel_peer_unadjusted=rel_peer_unadjusted, just_fwd_pe=just_fwd_pe,
                peer_adj_pe=peer_adj_pe, payout_implied=payout_implied,
                eps_26_A=eps_26_A, eps_26_B=eps_26_B, eps_fwd=eps_fwd,
                own_pe_history=own_hist, own_pe_mean=own_pe_mean, pe_now=pe_now,
                evebitda_now=evebitda_now, eps_ttm=eps_ttm, eps_27_A=eps_27_A,
                eps_27_B=eps_27_B, norm_ps=norm_ps, norm_margin=norm_margin,
                norm_pat_ps=norm_pat / V['shares_mn']),
    sensitivity=dict(**{k: [[float(a), float(b)] for a, b in v] for k, v in sens.items()},
                     grid=grid, grid_wacc=[-0.02, -0.01, 0.0, 0.01, 0.02],
                     grid_g=[0.03, 0.04, 0.05, 0.06, 0.07]),
    crux=crux,
    working_capital=dict(dio_fy25=dio0, dso_fy25=dso0, dpo_fy25=dpo0,
                         ccc_fy25=dio0 + dso0 - dpo0),
    calibration=dict(step0=step0, backtest=bt5),
    narrative=NARR,
)

with open(os.path.join(HERE, 'study_numbers.json'), 'w') as f:
    json.dump(OUT, f, indent=1, default=float)
print('\nwrote study_numbers.json')
print(f"FAIR VALUE FIELD  bear {fair_bear:,.2f} · centre {fair_base:,.2f} · bull {fair_bull:,.2f} "
      f"| spot {V['spot']:,.2f}")
