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

import terminal_value as TV          # [R-TERM-01] — verified by import, not by parse
import macro_path as MP              # [R-MACRO-01] — the house path, never a typed rate

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

# ---- [R-MACRO-01]: the house path owns the economy; this study owns no rate of its own
_EG = MP.load('EG')
_HOUSE_CPI = list(_EG.inflation_path[:5])
_US_LT = _EG.raw['us_inflation_lt']['value']
_FX_SPOT = _EG.raw['fx']['spot']['value']
# relative purchasing-power parity, year by year, off the OBSERVED spot. FY2026 is that
# spot: a dated scalar for a year already two-thirds elapsed is a filed fact, not a
# forecast, and [R-MACRO-01 AMENDED] allows a leading-year anchor as a COUNT WITH A
# REASON rather than a blanket. FY2027 onward compound the derived differential.
# THE HOUSE PATH'S OWN DERIVATION, called rather than re-implemented [R-ENF-03]. A
# first draft anchored FY2026 AT the observed spot and compounded from FY2027, on the
# reasoning that a calendar year two-thirds elapsed is closer to a filed fact than to a
# forecast. The house derivation does not admit that and there is no exemption mechanism
# for a currency path, so the study CONFORMS and the tension is registered rather than
# resolved by inventing an anchor: applying a full year of purchasing-power depreciation
# to a quote taken eight months INTO that year puts the FY2026 average at 56.87 while
# the same path's own spot reads 50.25 on 6 August 2026, which would need roughly 70 by
# December. That is a property of the house path's FIRST YEAR and it will reach every
# Egyptian study that commits a currency path; it is recorded in this study's macro note
# for the pass that owns the house path, and it is not this study's to fix.
_HOUSE_FX = [round(x, 4) for x in _EG.fx_path(5)]
# TERMINAL RISK-FREE = terminal inflation + the real-rate convention, derived so it
# cannot disagree with the inflation the rest of the model runs on.
_HOUSE_RF_TERM = round(_EG.terminal_inflation
                       + _EG.raw['real_rate_convention']['value'], 6)

INP = dict(
    # ---- market anchors -------------------------------------------------
    spot=I(127.30, "Egyptian Exchange close, 3 September 2026 — the latest price available "
           "when this edition was struck. A valuation compared against a month-old quote "
           "is measured against the past rather than the market, so this edition "
           "re-strikes on the current close. The previous edition was struck at EGP "
           "130.05 on 6 August 2026.", "2026-09-03", "Market"),
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
    # ---- PRODUCT-LINE DISCLOSURE: the board report splits the SAME total two ways —
    # by channel (below) and by product line (here). Both are used: the channel split drives
    # the price realised per pack, the product-line split separates the company's OWN
    # preparations from product made under contract for third parties, which carry a
    # completely different economics (a manufacturing fee, not a product price).
    own_prep_value_fy25=I(9160.148, "Board of directors' report for FY2025, published in the company's 2025 Annual Report (eipico.com.eg -> Investor Relations -> Annual Reports), sales-indicators table: value of sales of the company's own preparations, "
                          "EGP thousand converted to million. Together with the "
                          "contract-manufacturing line below it sums to the disclosed "
                          "separate-company total", "2026-03-01", "Company"),
    own_prep_value_fy24=I(7104.160, "Board of directors' report for FY2025, published in the company's 2025 Annual Report (eipico.com.eg -> Investor Relations -> Annual Reports), sales-indicators table, prior-year comparative column", "2026-03-01",
                          "Company"),
    contract_value_fy25=I(142.321, "Board of directors' report for FY2025, published in the company's 2025 Annual Report (eipico.com.eg -> Investor Relations -> Annual Reports), sales-indicators table: value of sales of preparations made under "
                          "contract-manufacturing agreements. NOT the same line as the "
                          "contract-manufacturing REVENUE the company books — that is the "
                          "manufacturing fee only, disclosed separately below", "2026-03-01",
                          "Company"),
    contract_value_fy24=I(259.912, "Board of directors' report for FY2025, published in the company's 2025 Annual Report (eipico.com.eg -> Investor Relations -> Annual Reports), sales-indicators table, prior-year comparative column", "2026-03-01",
                          "Company"),
    packs_toll_fy24=I(8.874, "Board of directors' report for FY2025, published in the company's 2025 Annual Report (eipico.com.eg -> Investor Relations -> Annual Reports), sales-indicators table: packs sold of contract-manufactured preparations, "
                      "million", "2026-03-01", "Company"),
    prod_value_hist=I([1668.045836, 1911.944828, 2463.788810, 2747.157810, 3220.648533,
                       2789.983904, 3364.116402, 3799.457166, 5017.014708, 7364.071677,
                       9302.469311],
                      "Board of directors' report for FY2025, eleven-year revenue history table (total activity revenue, domestic sales, export sales, contract-manufacturing revenue and production value at selling price, by year): total activity revenue FY2015-FY2025, separate company, EGP "
                      "million. Eleven observations, used to test the forecast growth path "
                      "against what the business has actually delivered rather than against an "
                      "assertion", "2026-03-01", "Company"),
    dom_rev_hist=I([1300.974873, 1530.074523, 1772.408657, 2093.136929, 2580.583743,
                    2174.335906, 2611.133966, 2834.802684, 3425.007683, 4863.915731,
                    6334.989403],
                   "Board of directors' report for FY2025, eleven-year revenue history table (total activity revenue, domestic sales, export sales, contract-manufacturing revenue and production value at selling price, by year): domestic sales FY2015-FY2025, separate company, EGP million",
                   "2026-03-01", "Company"),
    exp_rev_hist=I([355.660824, 381.870305, 691.380153, 654.020881, 640.064790, 615.647998,
                    752.982436, 964.654482, 1592.007025, 2500.155946, 2967.479908],
                   "Board of directors' report for FY2025, eleven-year revenue history table (total activity revenue, domestic sales, export sales, contract-manufacturing revenue and production value at selling price, by year): export sales FY2015-FY2025, separate company, EGP million",
                   "2026-03-01", "Company"),
    prod_at_sale_hist=I([1762.036059, 1837.019705, 2592.543185, 2876.887489, 3281.506091,
                         3520.827945, 3464.934156, 4043.785528, 5628.821812, 8475.335057,
                         10811.924284],
                        "Board of directors' report for FY2025, eleven-year revenue history table (total activity revenue, domestic sales, export sales, contract-manufacturing revenue and production value at selling price, by year): value of production at selling price FY2015-FY2025, EGP "
                        "million. Production consistently EXCEEDS sales, which is the "
                        "inventory build the eight-month raw-material and finished-goods "
                        "policy implies", "2026-03-01", "Company"),
    dep_in_cogs_fy25=I(93.497560, AUD25 + ", note (26) cost of sales: the depreciation line "
                       "inside cost of sales. Used to split the forecast depreciation charge "
                       "between production and operating expense in the same proportion the "
                       "audited note shows", "2026-03-01", "Company"),
    dep_only_fy25=I(109.455425, AUD25 + ", note (4) fixed assets: the DEPRECIATION charge "
                    "alone, against the total depreciation-and-amortisation of 117.725 that "
                    "also carries right-of-use and intangible amortisation. The difference is "
                    "the non-property amortisation run-rate the forecast holds flat",
                    "2026-03-01", "Company"),
    ecl_fy23=I(39.0, "Audited consolidated financial statements for the year ended 31 December "
               "2023: the EXPECTED-CREDIT-LOSS component of the formed-provisions line, "
               "separated from inventory impairment and other provisions", "2026-03-01",
               "Company"),
    ecl_fy24=I(330.0, "Audited FY2024 statements: the expected-credit-loss component alone",
               "2026-03-01", "Company"),
    ecl_fy25=I(376.158, AUD25 + ": the expected-credit-loss component alone", "2026-03-01",
               "Company"),
    shares_fy22=I(99.170500, "Shares in issue at 31 December 2022, from the capital and "
                  "shareholders' table in the board report. Used ONLY to compute that year's "
                  "earnings per share and traded multiple", "2026-03-01", "Company"),
    board_fee_fwd=I(2.0, "Board remuneration and attendance allowances carried flat in the "
                    "forecast at the FY2025 disclosed level of 1.828, rounded up. Immaterial "
                    "to value; carried as a line rather than dropped so the forecast income "
                    "statement reconciles to the audited one", "2026-08-09", "House"),
    nci_fwd=I(18.0, "Non-controlling share of forecast profit, held near the FY2025 disclosed "
              "16.235. The subsidiary carrying the minority is the ampoule and vial plant, "
              "which is 98.6% owned", "2026-08-09", "House"),
    plant_cost_usd_mn=I(100.0, "The stated cost of the EIPICO 3 biologicals facility in US "
                        "dollars, as the company describes it in its own announcements and "
                        "investor material. Used only as the denominator of the asset-turn "
                        "figure in the reverse valuation", "2026-08-09", "Company"),
    assoc_saudi_fy25=I(427.906046, AUD25 + ", note (33) associates by entity: the share of "
                       "results attributed to the Saudi Arabian manufacturing associate",
                       "2026-03-01", "Company"),
    assoc_saudi_fy24=I(190.021502, AUD25 + ", note (33), prior-year comparative. NOTE this "
                       "EXCEEDS the group associate line of 151.581 for FY2024, so the other "
                       "holdings were a net drag that year; both figures are published rather "
                       "than one being quoted alone", "2026-03-01", "Company"),
    peer_pe_hi=I(26.7, "Trailing price-earnings multiple of a listed Saudi Arabian generics "
                 "manufacturer. MARKET DATA, cross-check layer", "2026-08-09", "Market"),
    peer_pe_lo=I(16.0, "Trailing price-earnings multiple of larger, more liquid regional and "
                 "international generic manufacturers. MARKET DATA, cross-check layer",
                 "2026-08-09", "Market"),
    w_dcf=I(0.50, "Weight on the discounted-cash-flow reading inside each weighted centre. "
            "Carried IN FULL on one provision frame at a time — never split across both, "
            "because splitting it across both averages the two frames", "2026-08-09", "House"),
    w_book=I(0.20, "Weight on the book-value and sustainable-return reading", "2026-08-09",
             "House"),
    w_rel=I(0.15, "Weight on the relative-multiples reading, held below the intrinsic lenses "
            "because one of its three legs rests on undisclosed peer financials", "2026-08-09",
            "House"),
    w_norm=I(0.15, "Weight on the normalised-earnings-power reading", "2026-08-09", "House"),
    rev_sep_fy25=I(9302.469331, "Board of directors' report for FY2025, published in the company's 2025 Annual Report (eipico.com.eg -> Investor Relations -> Annual Reports), sales-indicators table: total separate-company activity revenue for FY2025. "
                   "The channel build must reconcile to this figure exactly before the "
                   "consolidation factor is applied", "2026-03-01", "Company"),
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
    fx_path=I(_HOUSE_FX,
              "Egyptian pound per US dollar, FY2026E-FY2030E period averages, DERIVED by "
              "relative purchasing-power parity from the house inflation path above "
              "against long-run United States inflation of 2.5% — never hand-set, because "
              "escalating costs at domestic inflation while holding the currency still is "
              "one event counted once and ignored once. The path compounds from the "
              "quote of 50.25 to the dollar on 6 August 2026. The previous edition ended "
              "the window at 57.7 against the 69.7 the "
              "differential produces — it escalated domestic costs at Egyptian inflation "
              "while depreciating the pound at roughly a third of the gap, which is two "
              "views of one economy inside one model.", "2026-09-03", "House"),

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
    esc_domestic_cpi=I(_HOUSE_CPI,
                       "Egyptian consumer price inflation, FY2026E-FY2030E, applied to "
                       "genuinely domestic service and consumable lines. THIS IS THE HOUSE "
                       "PATH AND NOT THIS STUDY'S OWN: 16.0 / 12.0 / 9.0 / 7.5 / 7.0, the "
                       "central bank's own published baseline for 2026 and 2027 and its "
                       "stated glide to the target band thereafter. The previous edition "
                       "carried 12.0 / 10.0 / 8.5 / 7.0 / 6.0 — a path that compounds 7.3% "
                       "lower over the window and terminates a point below the long-run "
                       "rate this same valuation uses in its terminal value. A company "
                       "cannot be valued in an economy the study beside it does not "
                       "recognise, and the divergence was invisible because the number was "
                       "derived rather than typed and nobody asked derived from what.",
                       "2026-09-03", "House"),

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
                         "permanent share of revenue — the FRAME A reading. LABEL CORRECTED: "
                         "this is NOT 'the three-year average', which the earlier edition called "
                         "it. The disclosed charge runs 5.07% (FY2023), 9.24% (FY2024), 5.23% "
                         "(FY2025); the mean of those three ratios is 6.52% and the mean of the "
                         "two years either side of the FY2024 spike is 5.15%. 5.25% IS STRUCK "
                         "MARGINALLY ABOVE THE TWO NON-OUTLIER YEARS, and that is what it "
                         "should be called. Both the 6.52% three-year mean and the 3.03% "
                         "expected-credit-loss-only three-year mean are published beside it and "
                         "the frame is sensitised across them. Context that neither reading "
                         "carries: the first quarter of 2026 booked NO expected credit loss at "
                         "all — one of the three matters the auditor qualified — so 6.52% is "
                         "more than twice a quarter that charged nothing",
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
    rf=I(0.2300, "Egypt ten-year local-currency government bond yield, 23.00%, the observable "
         "print on the SAME date as the equity price used throughout this study (6 August "
         "2026). The earlier edition carried a 22.31% print dated 21 July 2026, which was both "
         "stale against the pricing date and 39 basis points below the observable level on its "
         "own date; the risk-free rate and the share price are now struck on one date. A live "
         "re-read of the central bank's own fixed-coupon treasury bond auction page was "
         "attempted on 09-Aug-2026 and rejected by that site's web application firewall, so the "
         "level is indicated by a market-data series rather than proven from the auction curve "
         "— and it is sensitised", "2026-08-06", "Country"),
    sov_spread_cds=I(0.0342, "Egypt sovereign credit-default-swap spread, 3.42%, from the "
                     "MID-YEAR (July 2026) vintage of the country default-spread and "
                     "risk-premium dataset, Egypt row, 'Sovereign CDS, net of Swiss CDS' "
                     "column, spread measured 30 June 2026. Netted out of the local-currency "
                     "risk-free rate so that sovereign default risk is charged once, inside the "
                     "equity risk premium, and not twice. The January-2026 vintage previously "
                     "used carried 3.41%", "2026-07-02", "Country"),
    sov_spread_rating=I(0.059702, "Egypt adjusted default spread on the rating basis (Moody's "
                        "Caa1), 5.9702%, same mid-year (July 2026) vintage, 'Rating-based "
                        "Default Spread' column — the alternative construction, published for "
                        "the audit trail. The January-2026 vintage carried 6.3725%",
                        "2026-07-02", "Country"),
    erp_cds=I(0.095164, "Egypt TOTAL equity risk premium on the sovereign-CDS basis, 9.5164%, "
              "same mid-year vintage. This is the dataset's TOTAL equity risk premium column, "
              "not its country risk premium column — the total premium is what multiplies beta. "
              "The CDS-basis country risk premium alone is 5.3164%", "2026-07-02", "Country"),
    erp_rating=I(0.134806, "Egypt TOTAL equity risk premium on the rating basis, 13.4806%, same "
                 "mid-year vintage — again the TOTAL equity risk premium column, being the "
                 "9.2806% country risk premium over a 4.20% mature-market premium. The "
                 "January-2026 vintage carried 13.9377% total over a 9.7077% country premium",
                 "2026-07-02", "Country"),
    crp_rating=I(0.092806, "Egypt COUNTRY risk premium on the rating basis, 9.2806%, mid-year "
                 "(July 2026) vintage — carried separately and published beside the total "
                 "premium so that a reader checking the dataset's own 'Country Risk Premium' "
                 "column finds the figure this study calls by that name. It is NOT added to the "
                 "cost of equity; the total premium above already contains it",
                 "2026-07-02", "Country"),
    crp_cds=I(0.053164, "Egypt COUNTRY risk premium on the sovereign-CDS basis, 5.3164%, "
              "mid-year vintage, disclosure only — see the note above", "2026-07-02",
              "Country"),
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
              "CONVERGENCE PATH, FY2026E-FY2030E. This row is NOT the cost of local-currency "
              "debt (24.81%) and NOT the blended marginal cost of debt (18.55%): its first "
              "point, 18.90%, is the NORMALISED RISK-FREE RATE, and the row traces that rate "
              "converging on the terminal norm as the central bank's easing cycle runs. Its "
              "only job is to give the discount-rate glide a shape derived from something in "
              "the model rather than an invented curve; the glide uses the row normalised to "
              "its own endpoints, so the levels cancel and only the SHAPE enters. The earlier "
              "edition described it as a cost-of-debt path, which it is not",
              "2026-08-09", "House"),
    rf_term=I(_HOUSE_RF_TERM, "Terminal risk-free rate, DERIVED and never quoted: the "
              "long-run inflation this valuation carries throughout, 7.0%, plus the "
              "standard 5.5-point emerging-market real-rate convention. The previous "
              "edition used 10.5%, built the same way but on a 5% inflation assumption "
              "that appears nowhere else in the model — the same valuation escalated "
              "costs on one long-run rate and discounted the terminal on another, two "
              "points apart. THE DERIVATION IS WHAT MAKES IT CHECKABLE: the single most "
              "terminal-value-sensitive number in the model cannot be typed, and it "
              "cannot disagree with the inflation the rest of the model uses because it "
              "is computed from it.", "2026-09-03", "House"),
    erp_term=I(0.070, "Terminal equity risk premium, normalised below today's crisis-era level "
               "toward the rating-class norm; never held flat into perpetuity", "2026-08-09",
               "House"),
    kd_term_lc=I(0.150, "Terminal local-currency corporate borrowing rate — the long-run "
                 "Egyptian norm of roughly 10 points above the 5% inflation target",
                 "2026-08-09", "House"),
    kd_term_fx=I(0.065, "Terminal hard-currency coupon", "2026-08-09", "House"),
    wd_term_basis=I('market', "Basis on which the TERMINAL debt weight is set. It is no longer "
                    "an asserted 20%. The earlier edition claimed 20% was 'reconciled to the "
                    "model's own forecast balance sheet'; it was not — that sheet, once it is "
                    "made to balance, carries a book net-debt weight near 39% at FY2030E, and "
                    "today's market-value net-debt weight is near 25%. Neither is 20%, and the "
                    "stated deleveraging never happens once the forecast is funded. This input "
                    "selects which reconcilable reading is used: 'market' takes today's "
                    "market-value net-debt weight (the weighting basis a weighted average cost "
                    "of capital requires), 'book' takes the forecast terminal book weight. Both "
                    "are computed below and both are published", "2026-08-09", "House"),
    g_term_real=I(0.0, "Terminal REAL growth of zero: the business is assumed to hold its "
                  "scale in real terms in perpetuity, with the nominal rate computed from "
                  "the long-run Egyptian inflation this valuation uses throughout. The "
                  "previous edition typed 5% nominal and justified it as 'approximately "
                  "zero real terminal growth' — WHICH IT WAS NOT. Against the 7% long-run "
                  "inflation this valuation carries elsewhere, 5% nominal is a real "
                  "DECLINE of 1.87% a year, for ever, for a company with a third of its "
                  "revenue in hard currency and a biosimilars plant just entering service. "
                  "Nothing in the study argued for a perpetual contraction; the sentence "
                  "asserted the opposite of what the arithmetic did, and a rate quoted "
                  "only in nominal terms is where that hides. Sensitised 3-7% nominal.",
                  "2026-08-09", "House"),
    asset_life_weighted=I(13.80, "Weighted useful life of the depreciable asset base, "
                          "derived from the FY2024 audited consolidated statements' own "
                          "composition: the estimated lives in note 3.1 — buildings and "
                          "structures 50 years, production and service machines 15, means "
                          "of transportation and tools 5, office furniture and equipment "
                          "10, land not depreciated — weighted by the gross cost by class "
                          "in note 4.1 at 31 December 2024. Every life the company "
                          "discloses is a single figure rather than a band, so the "
                          "weighting is unambiguous. The depreciable base of EGP "
                          "2,701,916,171 foots to the note's stated total of "
                          "2,785,102,203 once land of 83,186,032 is excluded. Annual "
                          "depreciation rates add rather than lives, so the weighted life "
                          "is the reciprocal of the weighted rate.", "2024-12-31",
                          "Company"),
    roic_term_source=I('model_fy2030', "Terminal return on invested capital is no longer an "
                       "input. The earlier edition asserted 20% while the model's own FY2030E "
                       "return on invested capital was 16.36% — a 364 basis-point step up, "
                       "taken at exactly the point where three quarters of core enterprise "
                       "value sits. The terminal return is now COMPUTED as the model's own "
                       "final forecast year, so terminal reinvestment (growth divided by "
                       "return) cannot assume a return the forecast does not earn. This input "
                       "records that choice; there is no numeric assumption left to make",
                       "2026-08-09", "House"),
    assoc_multiple=I(11.0, "Earnings multiple applied to the equity-accounted associate stream "
                     "in the enterprise-to-equity bridge. The associates contributed EGP 495.5 "
                     "million in FY2025 — 36% of attributable profit — against a carrying value "
                     "of only EGP 675.9 million, so carrying value is not a usable proxy. The "
                     "larger holding is a 30% interest in a Saudi Arabian pharmaceutical "
                     "manufacturer; 11 times is struck below the Gulf listed-pharmaceutical "
                     "range to allow for the minority, unlisted and non-controlled nature of "
                     "the stake. CROSS-CHECK: the one associate in the group that is itself "
                     "listed trades on roughly 9.3 times trailing earnings, so 11 times is "
                     "above the only observable comparable in the portfolio and the "
                     "enterprise-to-equity bridge is sensitised on it", "2026-08-09", "House"),
    assoc_norm=I(250.0, "Normalised annual contribution of the EARNING associates, used with "
                 "the multiple above; the pre-revenue active-ingredient company is carried "
                 "separately at cost, on its own line. EGP million. BASIS, RECONCILED TO THIS "
                 "STUDY'S OWN INCOME STATEMENT (the earlier edition's basis note quoted 74.5 / "
                 "147.1 / 495.5, two of which did not match it): the disclosed share of "
                 "associates' and subsidiaries' results is 74.508 (FY2023), 151.581 (FY2024) "
                 "and 512.085 (FY2025). Those three average 246.058, and 250 is struck there — "
                 "not at the level the FY2025 print alone would support. REVISED DOWN from 320 "
                 "after the first quarter of 2026 reported only 13.118 against 33.445 a year "
                 "earlier, an annualised 52.5. That quarter is EVIDENCE, NOT A RUN-RATE: the "
                 "auditor states in the review report that the periodic financial statements of "
                 "two of the holdings were not received, so the quarter's associate line is "
                 "incomplete by construction. Both the 250 carried and the 52.5 the quarter "
                 "annualises to are published, and the leg is sensitised across them",
                 "2026-08-11", "House"),

    # ---- relative lens ------------------------------------------------------
    peer_ke=I(0.10, "Cost of equity faced by the struck reference companies — a listed "
              "Saudi Arabian generics manufacturer and larger international generic "
              "manufacturers, all of them in hard-currency or pegged economies. It is the "
              "ONE difference the peer multiple is adjusted for, and it is registered "
              "rather than typed inside the adjustment so a reader can see what the "
              "adjustment is made of.", "2026-08-09", "House"),
    peer_pe_regional=I(21.35, "A STRUCK REFERENCE, not a median of a disclosed peer set — the "
                       "earlier edition called it a 'peer median', which it was not, because "
                       "only two reference points are disclosed. Those two are: a listed Saudi "
                       "Arabian generics manufacturer at 26.7 times, and larger, more liquid "
                       "regional and international generic manufacturers at about 16.0 times. "
                       "21.35 is the midpoint of those two observations — which for a "
                       "two-element set is also their median — rather than a figure struck "
                       "between them by judgement. MARKET DATA, cross-check layer, never a "
                       "source for any company historical. The peers are not named and their "
                       "financials are not published, so this multiple cannot be rebuilt from "
                       "peer filings; that gap is recorded as an open research item and the "
                       "lens is run across a 13-26 times band rather than on a point",
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

# ---- [R-MACRO-01]: the terminal NOMINAL growth is DERIVED, never typed ------------
# The house path owns the inflation; this study owns the REAL rate and nothing else.
# The previous edition typed 5% nominal and described it as "approximately zero real",
# which against the house terminal of 7% is a real DECLINE of 1.87% a year in
# perpetuity — the sentence asserted the opposite of what the number did, and neither
# a reader nor a checker could see it while the rate was quoted in nominal terms.
_EG_PATH = MP.load('EG')
PI_TERM = (_EG_PATH.raw['inflation']['terminal'] or {})['value']
V['g_term'] = (1.0 + PI_TERM) * (1.0 + V['g_term_real']) - 1.0
# --- audit hook: re-run the whole model with one input replaced, for pricing a finding ---
_ovr = os.environ.get('PHAR_OVERRIDE')
if _ovr:
    for _k, _v in json.loads(_ovr).items():
        assert _k in V, f'override targets an unknown input: {_k}'
        V[_k] = _v
        INP[_k] = dict(INP[_k], value=_v, source=INP[_k]['source'] + ' [AUDIT OVERRIDE]')
_QUIET = bool(os.environ.get('PHAR_QUIET'))
for k, rec in INP.items():
    assert set(rec) == {'value', 'source', 'date', 'layer'}, k
    assert rec['source'] and rec['date'] and rec['layer'], f'{k} is not four-field complete'

TAX = V['tax_stat']
BOARD_FEE = V['board_fee_fwd']
NCI_FWD = V['nci_fwd']
YEARS = ['FY2026E', 'FY2027E', 'FY2028E', 'FY2029E', 'FY2030E']
NARR = []


def say(s):
    NARR.append(s)
    if not _QUIET:
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
# THREE PRODUCT LINES, not two. The board report splits the same separate-company total two
# different ways — by CHANNEL and by PRODUCT LINE — and reconciling the two is what separates
# the company's own preparations from product it manufactures under contract for third
# parties. Those are different businesses: the first is priced per pack, the second earns a
# manufacturing fee, and part of the contract-made product is then sold through the company's
# own domestic channels. The earlier cut of this build divided a domestic revenue figure that
# INCLUDED contract-made product by a pack count that EXCLUDED contract packs, which
# overstated the realised price per own pack in both years.
exp_rev25 = V['ch_export_fy25']
exp_rev24 = V['ch_export_fy24']
exp_packs25 = V['export_packs_fy25']
exp_packs24 = exp_packs25 * V['export_usd_fy24'] / V['export_usd_fy25']  # dollar price held
dom_packs25 = V['packs_own_fy25'] - exp_packs25
dom_packs24 = V['packs_own_fy24'] - exp_packs24
# line 1 + 2: the company's OWN preparations, domestic and export
dom_own_rev25 = V['own_prep_value_fy25'] - exp_rev25
dom_own_rev24 = V['own_prep_value_fy24'] - exp_rev24
# line 3: contract manufacturing — a FEE the company books, plus contract-made product that
# reaches the market through its own domestic channels
toll_fee25, toll_fee24 = V['ch_toll_fy25'], V['ch_toll_fy24']
contract_resale25 = V['contract_value_fy25'] - toll_fee25
contract_resale24 = V['contract_value_fy24'] - toll_fee24
toll_packs25, toll_packs24 = V['packs_toll_fy25'], V['packs_toll_fy24']
toll_fee_pp25, toll_fee_pp24 = toll_fee25 / toll_packs25, toll_fee24 / toll_packs24
resale_pp25, resale_pp24 = contract_resale25 / toll_packs25, contract_resale24 / toll_packs24
dom_rev25 = V['ch_direct_fy25'] + V['ch_distrib_fy25'] + V['ch_tender_fy25']
dom_rev24 = V['ch_direct_fy24'] + V['ch_distrib_fy24'] + V['ch_tender_fy24']
dom_ppp25 = dom_own_rev25 / dom_packs25
dom_ppp24 = dom_own_rev24 / dom_packs24
exp_ppp_usd25 = (exp_rev25 / V['fx_avg_fy25']) / exp_packs25
# the two disclosures must close on each other, both years, to the thousand
for _y, _own, _con, _dom, _exp, _tot in (
        (2025, V['own_prep_value_fy25'], V['contract_value_fy25'], dom_rev25, exp_rev25,
         V['rev_sep_fy25']),
        (2024, V['own_prep_value_fy24'], V['contract_value_fy24'], dom_rev24, exp_rev24,
         V['ch_direct_fy24'] + V['ch_distrib_fy24'] + V['ch_tender_fy24'] + exp_rev24
         + V['ch_toll_fy24'])):
    assert abs((_own + _con) - _tot) < 0.03, \
        f'FY{_y} product-line split does not tie to the disclosed total'
    _resale = _con - (V['ch_toll_fy25'] if _y == 2025 else V['ch_toll_fy24'])
    assert abs((_own - _exp) + _resale - _dom) < 0.03, \
        f'FY{_y} channel split and product-line split do not reconcile'
say('')
say(f"[Unit build] The board report splits the same separate-company revenue two ways, and the "
    f"two only reconcile once contract manufacturing is separated out. FY2025 sales of the "
    f"company's OWN preparations were EGP {V['own_prep_value_fy25']:,.3f} million on "
    f"{V['packs_own_fy25']:.3f} million packs; preparations made under CONTRACT for third "
    f"parties were EGP {V['contract_value_fy25']:,.3f} million of product value on "
    f"{toll_packs25:.3f} million packs, of which the company books only the manufacturing fee "
    f"of EGP {toll_fee25:,.3f} million — EGP {toll_fee_pp25:,.2f} a pack — while the remaining "
    f"EGP {contract_resale25:,.3f} million reaches the market through its own domestic "
    f"channels at EGP {resale_pp25:,.2f} a pack. The two splits sum to the same "
    f"EGP {V['rev_sep_fy25']:,.3f} million.")
say(f"  LINE 1, own preparations sold at home: {dom_packs25:.3f} million packs carrying EGP "
    f"{dom_own_rev25:,.3f} million, EGP {dom_ppp25:,.4f} a pack against EGP {dom_ppp24:,.4f} "
    f"in FY2024 — realised price +{dom_ppp25 / dom_ppp24 - 1:.2%} on volume "
    f"+{dom_packs25 / dom_packs24 - 1:.2%}. Dividing the CHANNEL domestic figure of EGP "
    f"{dom_rev25:,.0f} million by these packs instead would read EGP "
    f"{dom_rev25 / dom_packs25:,.4f} a pack, because that figure carries the contract-made "
    f"product as well; the difference is {dom_rev25 / dom_packs25 / dom_ppp25 - 1:.2%} on the "
    f"price and it flows into every forecast year.")
say(f"  LINE 2, own preparations exported: {exp_packs25:.3f} million packs at EGP "
    f"{exp_rev25 / exp_packs25:,.2f} a pack, which is USD {exp_ppp_usd25:.4f} at the disclosed "
    f"average rate of {V['fx_avg_fy25']:.2f} — against USD "
    f"{(exp_rev24 / V['fx_avg_fy24']) / exp_packs24:.4f} in FY2024.")
say(f"  LINE 3, contract manufacturing: packs fell {1 - toll_packs25 / toll_packs24:.1%} to "
    f"{toll_packs25:.3f} million while the fee per pack rose "
    f"{toll_fee_pp25 / toll_fee_pp24 - 1:.1%} to EGP {toll_fee_pp25:,.2f}. This is a small "
    f"line — {(toll_fee25 + contract_resale25) / V['rev_sep_fy25']:.2%} of revenue — but it is "
    f"forecast on its own volume and its own price rather than folded into the domestic book.")
say(f"  Production ran at {V['units_prod_fy25']:,.0f} million units against {V['units_cap']:,.0f} "
    f"million of disclosed capacity — {V['units_prod_fy25'] / V['units_cap']:.0%} utilisation, so "
    f"the volume path below is not capacity-constrained.")
# the reconstructed channels must tie to the disclosed standalone revenue total
recon25 = dom_rev25 + exp_rev25 + V['ch_toll_fy25']
say(f"  Reconstructed channel revenue {recon25:,.3f} against the disclosed separate-company "
    f"revenue total of {V['rev_sep_fy25']:,.3f} — a difference of "
    f"{abs(recon25 - V['rev_sep_fy25']):,.3f}, which is "
    f"rounding on the incentive lines.")
assert abs(recon25 - V['rev_sep_fy25']) < 0.05, 'channel build does not tie to disclosed revenue'

# ============================ FORECAST =======================================
n = 5
fx = V['fx_path']
# EVERY LINE IS A VOLUME TIMES A PRICE. Nothing is grown as a revenue percentage.
dom_packs, exp_packs, dom_ppp, exp_ppp_usd = [], [], [], []
toll_packs, toll_fee_pp, resale_pp = [], [], []
p_d, p_e, r_d, r_e = dom_packs25, exp_packs25, dom_ppp25, exp_ppp_usd25
p_t, f_t, s_t = toll_packs25, toll_fee_pp25, resale_pp25
for i in range(n):
    p_d *= (1 + V['dom_pack_growth'][i]); dom_packs.append(p_d)
    p_e *= (1 + V['exp_pack_growth'][i]); exp_packs.append(p_e)
    r_d *= (1 + V['dom_price_growth'][i]); dom_ppp.append(r_d)
    r_e *= (1 + V['exp_price_usd_growth'][i]); exp_ppp_usd.append(r_e)
    # contract manufacturing: its PACK count grows on its own driver, and both the
    # manufacturing fee and the resale price escalate on the domestic price path — the same
    # administered-price environment the company's own preparations sell into.
    p_t *= (1 + V['toll_growth'][i]); toll_packs.append(p_t)
    f_t *= (1 + V['dom_price_growth'][i]); toll_fee_pp.append(f_t)
    s_t *= (1 + V['dom_price_growth'][i]); resale_pp.append(s_t)

rev_dom = [dom_packs[i] * dom_ppp[i] for i in range(n)]
rev_exp = [exp_packs[i] * exp_ppp_usd[i] * fx[i] for i in range(n)]
toll = [toll_packs[i] * toll_fee_pp[i] for i in range(n)]
rev_resale = [toll_packs[i] * resale_pp[i] for i in range(n)]
# the consolidated total runs a small step above the separate-company channel build:
# the subsidiary's external sales. Measured, not assumed.
consol_uplift = V['rev_fy25'] / V['rev_sep_fy25']
revenue = [(rev_dom[i] + rev_exp[i] + toll[i] + rev_resale[i]) * consol_uplift
           for i in range(n)]
# the build must reproduce the audited FY2025 separate-company total from its own three lines
_base_check = dom_own_rev25 + exp_rev25 + toll_fee25 + contract_resale25
assert abs(_base_check - V['rev_sep_fy25']) < 0.03, \
    f'the three-line unit build does not reproduce FY2025: {_base_check:.3f}'
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
DEP_IN_COGS_FY25 = V['dep_in_cogs_fy25']
DEP_COGS_SHARE = DEP_IN_COGS_FY25 / V['dna_fy25']
CASH_CLASSES = ('materials', 'packaging', 'labour', 'energy', 'services_other')
_cash_tot = sum(cs_all[k] for k in CASH_CLASSES)
cs = {k: cs_all[k] / _cash_tot for k in CASH_CLASSES}
unit_cost25 = (V['cogs_fy25'] - DEP_IN_COGS_FY25) / V['packs_sold_fy25']   # CASH cost per pack
packs_total = [dom_packs[i] + exp_packs[i] + toll_packs[i] for i in range(n)]
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
# Hard-currency exposure of the cost stack, COMPUTED — two legitimate denominators, both
# published. On the CASH cost stack the escalators actually act on, and on the full disclosed
# cost split including the depreciation line. Neither is the 79% the earlier edition's risk
# narrative quoted; that figure counted the WHOLE packaging line as imported, which the same
# study's own cost table denies.
fx_cost_share = cs['materials'] + V['esc_packaging_import_share'] * cs['packaging']
fx_cost_share_all_packaging = cs['materials'] + cs['packaging']
fx_cost_share_full = (cs_all['materials']
                      + V['esc_packaging_import_share'] * cs_all['packaging'])
fx_cost_share_full_all_pack = cs_all['materials'] + cs_all['packaging']
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
amort = [V['dna_fy25'] - V['dep_only_fy25'] for _ in range(n)]   # right-of-use + intangibles
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

# ==================== FORECAST EQUITY, FUNDING AND RETURNS ====================
# This block used to sit below the discounted cash flow. It has been moved ahead of it
# because two things the earlier edition ASSERTED are now DERIVED from it: the terminal
# debt weight and the terminal return on invested capital.
gross_debt_open = (V['loans_lt_fy25'] + V['loans_st_fy25'] + V['facilities_fy25']
                   + V['leases_fy25'])
w_fx = V['loans_fx_fy25'] / (V['loans_fx_fy25'] + V['loans_lc_fy25'])
kd_fx_local_equiv = (1 + V['kd_fx_coupon']) * (1 + V['fx_dep_wacc']) - 1
kd_blend_pre = (1 - w_fx) * V['kd_egp'] + w_fx * kd_fx_local_equiv
roe_fwd, eq_path = [None] * n, []
parent_path, retained_path = [], []
eq_b = V['equity_parent_fy25']
for i in range(n):
    # Associate income arrives ALREADY TAXED — the equity method takes the group's share of
    # the associate's post-tax profit, and the disclosed figure is already net of withholding.
    # Taxing it again inside this chain would understate attributable profit.
    pat = ((ebit_A[i] - V['int_path'][i]) * (1 - V['tax_eff_fwd'])
           + V['assoc_norm'] - NCI_FWD)
    eq_n = eq_b + pat * (1 - V['payout'])
    roe_fwd[i] = pat / ((eq_b + eq_n) / 2)
    eq_path.append(eq_n)
    parent_path.append(pat)
    retained_path.append(pat * (1 - V['payout']))
    eq_b = eq_n
roe_sust = float(np.mean(roe_fwd[-3:]))

# ---- the funding plug: the forecast balance sheet has to balance ---------------
# The earlier edition froze cash AND gross borrowings at their audited 31-Dec-2025 levels
# for five years while retained earnings compounded, so total assets exceeded total
# liabilities and equity by as much as 6.6% and the forecast was quietly unfunded. Cash is
# now held at the audited level as the operating minimum and GROSS BORROWINGS ARE THE PLUG:
# whatever the asset side needs that trade credit, provisions and equity do not supply.
OTH_NC_FWD = (V['assoc_bv_fy25'] + V['intang_fy25'] + V['rou_fy25'] + V['dta_fy25']
              + V['afs_fy25'])
PTX_FWD = V['provbs_fy25'] + V['taxpay_fy25'] + V['dtl_fy25']
cash_f = [V['cash_fy25'] for _ in range(n)]
debt_f, assets_f, bs_gap_old = [], [], []
for i in range(n):
    a = (ppe[i] + cip[i] + OTH_NC_FWD + inv_f[i] + ar_f[i] + othdr_f[i] + cash_f[i])
    other_le = ap_f[i] + othcr_f[i] + PTX_FWD + eq_path[i] + V['nci_bridge']
    assets_f.append(a)
    debt_f.append(a - other_le)
    bs_gap_old.append(a - (other_le + gross_debt_open))
for i in range(n):
    lhs = assets_f[i]
    rhs = (ap_f[i] + othcr_f[i] + PTX_FWD + debt_f[i] + eq_path[i] + V['nci_bridge'])
    assert abs(lhs - rhs) < 1e-6, f'forecast balance sheet does not balance in year {i}'
net_debt_f = [debt_f[i] - cash_f[i] for i in range(n)]
say('')
say(f"[Funding] the forecast balance sheet is FUNDED, not frozen. Cash is held at the audited "
    f"{V['cash_fy25']:,.0f} million operating minimum and gross borrowings carry the "
    f"difference, so total assets equal total liabilities and equity in every forecast year by "
    f"construction. Borrowings run "
    + ' -> '.join(f'{d:,.0f}' for d in debt_f) +
    f" against an audited {gross_debt_open:,.0f}: the working-capital build and the first "
    f"year's capital expenditure are debt-funded while a {V['payout']:.0%} payout continues, "
    f"and the book only returns to its opening level in the final year. The earlier edition "
    f"held both cash and borrowings flat, which left the statement out by up to "
    f"{max(bs_gap_old) / min(assets_f) * 100:.1f}% of total assets.")
say(f"  CONSEQUENCE, STATED RATHER THAN HIDDEN: on this funded book the finance cost charged in "
    f"the income statement implies an average borrowing rate of "
    + ' / '.join(f'{V["int_path"][i] / ((debt_f[i] + (gross_debt_open if i == 0 else debt_f[i - 1])) / 2):.2%}'
                 for i in range(n)) +
    f", against a blended MARGINAL cost of debt of {kd_blend_pre:.2%} used in the discount "
    f"rate. The charged path is calibrated to the first quarter of 2026 and is right for "
    f"FY2026E; the later years assume an easing cycle the debt schedule does not evidence. "
    f"That gap is an open item, it is not resolved in this edition, and the EARNINGS-BASED "
    f"lenses are sensitised across it.")

# ---- terminal return on invested capital: computed, never asserted -------------
ic_fy30 = ppe[-1] + cip[-1] + wc[-1] + V['intang_fy25']
# the FIRST forecast year's invested capital, so the capital behind one unit of REAL
# growth is a MARGINAL quantity — a difference across the window, from which any
# common starting level correctly cancels
ic_fy26 = ppe[0] + cip[0] + wc[0] + V['intang_fy25']

# ============================ COST OF CAPITAL =================================
rf_star = V['rf'] - V['sov_spread_cds']
ke = rf_star + V['beta'] * V['erp_cds']
ke_rating = (V['rf'] - V['sov_spread_rating']) + V['beta'] * V['erp_rating']
ke_double_counted = V['rf'] + V['beta'] * V['erp_cds']   # the retired construction, for contrast

kd_blend = kd_blend_pre
kd_at = kd_blend * (1 - TAX)

mcap = V['spot'] * V['shares_mn']
gross_debt = gross_debt_open
net_debt = gross_debt - V['cash_fy25']
we_net = mcap / (mcap + net_debt)
wd_net = 1 - we_net
wd_gross = gross_debt / (mcap + gross_debt)
wacc0 = we_net * ke + wd_net * kd_at
wacc0_gross = (1 - wd_gross) * ke + wd_gross * kd_at

ke_term = V['rf_term'] + V['beta'] * V['erp_term']
kd_term = (1 - w_fx) * V['kd_term_lc'] + w_fx * ((1 + V['kd_term_fx']) * 1.03 - 1)
kd_term_at = kd_term * (1 - TAX)
# TERMINAL DEBT WEIGHT — DERIVED, both readings computed and published. The earlier edition
# asserted 20% and claimed it was reconciled to the forecast balance sheet; it reconciled to
# neither reading of that sheet.
wd_term_market = wd_net
wd_term_book = net_debt_f[-1] / (net_debt_f[-1] + eq_path[-1])
wd_term = wd_term_market if V['wd_term_basis'] == 'market' else wd_term_book
wacc_term = (1 - wd_term) * ke_term + wd_term * kd_term_at
wacc_term_alt = (1 - wd_term_book) * ke_term + wd_term_book * kd_term_at

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
say(f"  Two FY2025 figures are in play here and they are not the same line: INTEREST ON CREDIT "
    f"FACILITIES of {V['int_fac_fy25']:,.3f} million, which is what an interest RATE must be "
    f"computed on, and the income statement's FINANCE COSTS of {V['fin_fy25']:,.3f} million, "
    f"which is that interest plus {V['fin_fy25'] - V['int_fac_fy25']:,.3f} million of bank "
    f"commissions and charges. Both come from the same note; the bridge between them is stated "
    f"here so that neither reads as a contradiction of the other.")
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
    f"after tax; DERIVED debt weight {wd_term:.1%} on today's market values "
    f"({wd_term_book:.1%} on the funded forecast balance sheet at FY2030E) -> terminal "
    f"discount rate {wacc_term:.2%} ({wacc_term_alt:.2%} on the book weight).")

# ---- the glide: its SHAPE comes from the convergence path, its LEVELS do not --
# The row this normalises is the normalised-risk-free-rate convergence path. Because it is
# rebased to its own endpoints the levels cancel out entirely and only the shape survives.
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
TAX_FCFF = V['tax_eff_fwd']    # the rate the business actually bears, not the statutory rate
# The construction balance still parked at FY2030E has never been charged depreciation, so a
# perpetuity capitalising the final year's operating profit capitalises a profit that
# under-charges the capital standing behind it. The terminal year is normalised for it.
term_dep_catchup = cip[-1] * V['dep_rate']


def run_dcf(ebit, ebitda, label):
    nopat = [e * (1 - TAX_FCFF) for e in ebit]
    fcff = [nopat[i] + dna[i] - capex[i] - dwc[i] for i in range(n)]
    pv = [fcff[i] * df[i] for i in range(n)]
    pv_sum = sum(pv)
    roic_fy30 = nopat[-1] / ic_fy30
    nopat_term = nopat[-1] * (1 + V['g_term']) - term_dep_catchup * (1 - TAX_FCFF)
    # THE RETIRED FORM, kept in one line so the change is legible and priced: the
    # reinvestment identity rr = g/ROIC charges g x IC every year for ever, so the
    # implied replacement cycle is 1/g — a fact about the growth rate rather than about
    # the asset. At the previous edition's 5% that was 20.0 years against a weighted
    # useful life this company's own accounts disclose at 13.80; at the derived 7% it is
    # 14.3. THE DIRECTION IS SET BY THE TYPED GROWTH RATE AND NOT BY THE MARKET: a
    # terminal at zero real growth has 1/g = 1/inflation and runs SHORT in a
    # high-inflation economy, which is what [R-TERM-01 CLAUSE TWO] reasons from; this
    # study typed a rate BELOW inflation and so ran long in exactly the market the
    # clause says should run short.
    reinv_rate = V['g_term'] / roic_fy30
    tv_retired = nopat_term * (1 - reinv_rate) / (wacc_term - V['g_term'])
    _inc_cap = ((ic_fy30 - ic_fy26) / (revenue[-1] - revenue[0])) * revenue[-1]
    _terminal = TV.build(TV.TerminalInputs(
        nopat=nopat_term, wacc=wacc_term, inflation=PI_TERM,
        real_growth=V['g_term_real'],
        dna_book=dna[-1] * (1 + V['g_term']),
        useful_life_years=V['asset_life_weighted'],
        useful_life_source=INP['asset_life_weighted']['source'],
        # The cross-check basis, and the reason is structural rather than convenience:
        # dividing REPLACEMENT-COST invested capital by the disclosed life needs a
        # replacement-cost capital base, and this model commits none — the property note
        # gives GROSS HISTORICAL cost on a base 64% depreciated, and rolling it forward
        # through five years of forecast capital spending at mixed vintages would be a
        # construction of ours rather than a figure the company discloses.
        maintenance_basis='book_dna_escalated',
        working_capital=wc[-1] * (1 + V['g_term']),
        incremental_capital_per_unit_growth=_inc_cap))
    fcff_term = _terminal.fcff
    tv = _terminal.tv
    pv_tv = tv * df[-1]
    ev_core = pv_sum + pv_tv
    assoc_earnings = V['assoc_norm'] * V['assoc_multiple']
    assoc_value = assoc_earnings + V['arab_api_cost']
    ev_total = ev_core + assoc_value + V['afs_fy25']
    equity = ev_total - net_debt - V['nci_bridge']
    ps = equity / V['shares_mn']
    return dict(label=label, ebitda=ebitda, ebit=ebit, nopat=nopat, fcff=fcff, pv=pv,
                pv_sum=pv_sum, nopat_term=nopat_term, reinvest_rate=reinv_rate,
                roic_term=roic_fy30, term_dep_catchup=term_dep_catchup,
                fcff_term=fcff_term, tv=tv, tv_retired=tv_retired,
                terminal_record=dict(inputs=dict(
                    nopat=nopat_term, wacc=wacc_term, inflation=PI_TERM,
                    real_growth=V['g_term_real'], nominal_growth=V['g_term'],
                    dna_book=dna[-1] * (1 + V['g_term']),
                    useful_life_years=V['asset_life_weighted'],
                    useful_life_source=INP['asset_life_weighted']['source'],
                    maintenance_basis='book_dna_escalated',
                    working_capital=wc[-1] * (1 + V['g_term']),
                    incremental_capital_per_unit_growth=_inc_cap),
                    outputs=dict(fcff=_terminal.fcff, tv=_terminal.tv,
                                 floor=_terminal.floor,
                                 maintenance=_terminal.maintenance,
                                 growth_capex=_terminal.growth_capex,
                                 wc_charge=_terminal.wc_charge,
                                 dna_addback=_terminal.dna_addback,
                                 implied_cycle_years=_terminal.implied_cycle_years,
                                 below_floor=_terminal.below_floor),
                    record=_terminal.record,
                    retired_construction=dict(
                        form='NOPAT_term(1 - g/ROIC)/(W-g)', tv=tv_retired,
                        implied_cycle_years=1.0 / V['g_term'])),
                pv_tv=pv_tv, ev_core=ev_core,
                tv_share=pv_tv / ev_core, assoc_value=assoc_value,
                assoc_earnings_value=assoc_earnings,
                arab_api_cost=V['arab_api_cost'], ev_total=ev_total,
                net_debt=net_debt, nci=V['nci_bridge'], equity=equity, per_share=ps,
                tv_share_total=pv_tv / ev_total)


_inc_cap_base = ((ic_fy30 - ic_fy26) / (revenue[-1] - revenue[0])) * revenue[-1]

dcf_A = run_dcf(ebit_A, ebitda_A, 'Frame A — provision charge permanent at 5.25% of revenue')
dcf_B = run_dcf(ebit_B, ebitda_B, 'Frame B — provision charge normalising to 2.5% of revenue')

# ROIC consistency: the terminal reinvestment rate is now SET BY the model's own final
# forecast year rather than checked against it.
roic_fy30_A, roic_fy30_B = dcf_A['roic_term'], dcf_B['roic_term']
say('')
say(f"[Terminal consistency] terminal reinvestment is growth {V['g_term']:.0%} divided by the "
    f"model's OWN FY2030E return on invested capital — {roic_fy30_A:.2%} on Frame A and "
    f"{roic_fy30_B:.2%} on Frame B — so {dcf_A['reinvest_rate']:.1%} of terminal operating "
    f"profit after tax is reinvested on Frame A. There is no terminal return assumption left "
    f"to make. The earlier edition asserted 20% here, a {(0.20 - roic_fy30_A) * 1e4:.0f} "
    f"basis-point step above the last forecast year, taken at exactly the point where three "
    f"quarters of core enterprise value sits.")
say(f"  The terminal year is also charged the depreciation the forecast never charged: "
    f"{cip[-1]:,.0f} million of construction is still parked at FY2030E and has never entered "
    f"the depreciable base, so at the model's own {V['dep_rate']:.1%} rate a further "
    f"{term_dep_catchup:,.0f} million a year is deducted before the perpetuity is struck. A "
    f"steady state cannot capitalise profit on capital it never charges.")
for d in (dcf_A, dcf_B):
    assert abs((d['ev_total'] - d['net_debt'] - d['nci']) - d['equity']) < 1e-6, 'bridge open'
    assert 0.0 < d['tv_share'] < 0.95, f"terminal share implausible: {d['tv_share']:.2f}"
    assert abs(d['reinvest_rate'] - V['g_term'] / d['roic_term']) < 1e-12, 'reinvestment open'
say(f"[Terminal weight] the terminal value is {dcf_A['tv_share']:.0%} of CORE enterprise value "
    f"on Frame A and {dcf_B['tv_share']:.0%} on Frame B — {dcf_A['tv_share_total']:.0%} and "
    f"{dcf_B['tv_share_total']:.0%} of TOTAL enterprise value, which carries the associates and "
    f"the assets held for sale as well. Both readings are published; the earlier edition "
    f"dropped the word 'core' outside the workbook, which made the concentration look higher "
    f"than the whole bridge supports. It is high either way, as it is for any growing "
    f"manufacturer discounted over five explicit years, and the terminal grid in the "
    f"sensitivity section runs the whole range rather than quoting a comfortable part of it.")
say(f"  The terminal DEBT WEIGHT is derived, not asserted. Today's market-value net-debt weight "
    f"is {wd_term_market:.1%}; the forecast balance sheet, once funded, carries a book net-debt "
    f"weight of {wd_term_book:.1%} at FY2030E. The valuation uses the market-value reading, "
    f"{wd_term:.1%}, because a weighted average cost of capital weights market values; the book "
    f"reading gives a terminal rate of {wacc_term_alt:.2%} against {wacc_term:.2%} and is "
    f"published beside it. The earlier edition used 20%, which is neither reading, and said it "
    f"was reconciled to a balance sheet that did not balance.")

# ============================ OTHER LENSES ====================================
# --- book value and sustainable return ---------------------------------------
bv_ps = V['equity_parent_fy25'] / V['shares_mn']
roe_fy25 = V['parent_fy25'] / ((V['equity_parent_fy25'] + V['equity_parent_fy24']) / 2)
roe_fy24 = V['parent_fy24'] / ((V['equity_parent_fy24'] + V['equity_parent_fy23']) / 2)
just_pb = (roe_sust - V['g_term']) / (ke_term - V['g_term'])
book_ps = just_pb * bv_ps
# The same sustainable return, expressed as an earnings multiple: retention must
# equal growth over return, so the payout the multiple assumes is not free.
payout_implied = 1 - V['g_term'] / roe_sust
just_fwd_pe = payout_implied / (ke_term - V['g_term'])
say('')
say(f"[Book value and sustainable return] book value per share {bv_ps:,.2f}. Return on average "
    f"equity was {roe_fy24:.1%} in FY2024 and {roe_fy25:.1%} in FY2025. The forecast path is "
    + ' / '.join(f'{r:.1%}' for r in roe_fwd) +
    f" — it RISES THROUGH the window rather than settling, so the sustainable return used here "
    f"is the MEAN OF ITS LAST THREE YEARS, {roe_sust:.2%}, computed from that path and not "
    f"asserted. (The earlier edition described the same number as the level the forecast "
    f"'settles at', which the path does not do.) A sustainable-return multiple of (return "
    f"{roe_sust:.1%} less growth {V['g_term']:.0%}) over (perpetual cost of equity "
    f"{ke_term:.2%} less growth) is {just_pb:.3f} times book, or {book_ps:,.2f} a share. Every "
    f"term in that multiple is live: change beta, the terminal risk-free rate, the terminal "
    f"premium or growth and the lens moves.")

# --- relative multiples: the company's OWN traded history first ---------------
import glob as _glob
sys.path.insert(0, os.path.join(HERE, '..'))
from primitives import load_ohlc
from data_quality import clean_ohlc
_px, _ = clean_ohlc(load_ohlc(os.path.join(HERE, 'PHAR_Stock_Price_History.csv')),
                    'PHAR', verbose=False, market='EG')
_px = _px.set_index('Date')['Price']
own_hist = []
for yr, parent, sh in ((2022, V['parent_fy22'], V['shares_fy22']),
                       (2023, V['parent_fy23'], V['shares_fy23']),
                       (2024, V['parent_fy24'], V['shares_fy23']),
                       (2025, V['parent_fy25'], V['wavg_shares_fy25'])):
    close = float(_px[_px.index <= f'{yr}-12-31'].iloc[-1])
    own_hist.append(dict(year=yr, close=close, shares=sh, eps=parent / sh,
                         pe=close * sh / parent))
own_pe_mean = float(np.mean([o['pe'] for o in own_hist]))
# TWO SHARE COUNTS, BOTH PUBLISHED. The capital increase from 148.755750 to 168.755750 million
# shares completed during FY2025, so the audited weighted-average count for that year is
# 162.016024 million while the count in issue at the year end — and today — is 168.755750
# million. The earlier edition carried the closing count in one sheet and the weighted average
# in another without saying so. Per-period consistency: a multiple struck on a FULL YEAR of
# earnings uses that year's WEIGHTED-AVERAGE count; a multiple struck on today's price uses
# the count in issue today.
eps_ttm = V['parent_fy25'] / V['shares_mn']                 # count in issue today
eps_ttm_wavg = V['parent_fy25'] / V['wavg_shares_fy25']     # audited weighted average
pe_now = V['spot'] / eps_ttm
pe_now_wavg = V['spot'] / eps_ttm_wavg
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
# The struck reference is DERIVED: the midpoint of the only two disclosed observations.
peer_pe_struck = (V['peer_pe_hi'] + V['peer_pe_lo']) / 2
assert abs(peer_pe_struck - V['peer_pe_regional']) < 1e-9, \
    'the struck peer reference does not equal the midpoint of its two observations'
# THE GROWTH IN THE NUMERATOR IS THE SAME GROWTH AS IN THE DENOMINATOR, and it was a
# TYPED 0.05 — the terminal growth of a previous edition, left behind when that rate
# became derived. The adjustment re-prices a peer multiple at THIS company's cost of
# equity and nothing else, so a different growth on the two sides would be re-pricing
# the growth as well and calling it a cost-of-equity adjustment. The workbook had it
# right and the model had it stale, which is the direction that normally runs the other
# way and is why the recalculation gate is worth having in both directions.
peer_adj_pe = (peer_pe_struck * (V['peer_ke'] - V['g_term'])
               / (ke_term - V['g_term']))
# PERIOD-MATCHED. A TRAILING multiple multiplies TRAILING earnings; a FORWARD multiple
# multiplies FORWARD earnings. The earlier edition applied all three legs to FY2026E earnings,
# including the two built from trailing multiples — and because FY2026E earnings are BELOW
# trailing on the depreciation and interest step, that mismatch understated the lens.
tri = [('Justified forward multiple from this model, on FY2026E earnings',
        just_fwd_pe, just_fwd_pe * eps_fwd),
       ("The company's own four-year mean multiple, on trailing earnings",
        own_pe_mean, own_pe_mean * eps_ttm),
       ('Struck peer reference, cost-of-equity adjusted, on trailing earnings',
        peer_adj_pe, peer_adj_pe * eps_ttm)]
rel_ps = float(np.mean([t[2] for t in tri]))
rel_lo, rel_hi = min(t[2] for t in tri), max(t[2] for t in tri)
rel_peer_unadjusted = V['peer_pe_regional'] * eps_ttm
say('')
say(f"[Relative multiples] the company's OWN traded history is computable entirely from primary "
    f"material — year-end closes against audited attributable profit: " +
    ', '.join(f"{o['pe']:.1f} times ({o['year']})" for o in own_hist) +
    f", a four-year mean of {own_pe_mean:.1f}. Each year divides that year's audited "
    f"attributable profit by that year's WEIGHTED-AVERAGE share count, so the FY2025 reading "
    f"uses {V['wavg_shares_fy25']:.3f} million shares rather than the "
    f"{V['shares_mn']:.3f} million now in issue — the capital increase completed during that "
    f"year. At {V['spot']:,.2f} the shares trade on {pe_now:.1f} times trailing attributable "
    f"earnings measured on the count in issue today, or {pe_now_wavg:.1f} times on the audited "
    f"weighted average; both readings are legitimate and both are published. The shares also "
    f"trade on {evebitda_now:.1f} times trailing EBITDA. The re-rating is the single most "
    f"important fact about this share price: the earnings multiple has more than doubled "
    f"against its own four-year history.")
say(f"  The lens triangulates three multiples rather than asserting one, and EACH IS APPLIED TO "
    f"THE EARNINGS OF ITS OWN PERIOD. (1) The forward multiple this model's own economics "
    f"justify: retention must equal growth {V['g_term']:.0%} over sustainable return "
    f"{roe_sust:.1%}, so the payout the multiple can assume is {payout_implied:.0%}, and "
    f"{payout_implied:.0%} over (perpetual cost of equity {ke_term:.2%} less growth) is "
    f"{just_fwd_pe:.2f} times — applied to {eps_fwd:,.2f} of FY2026E earnings a share. (2) The "
    f"company's own four-year mean, {own_pe_mean:.2f} times, a TRAILING multiple applied to "
    f"{eps_ttm:,.2f} of trailing earnings. (3) A struck reference of "
    f"{V['peer_pe_regional']:.2f} times — the midpoint of the only two comparable observations "
    f"available, 26.7 times for a listed Saudi Arabian generics manufacturer and about 16 "
    f"times for larger international generic manufacturers, and NOT a median of a disclosed "
    f"peer set — but those companies are Gulf-listed and face a cost of equity near 10%, not "
    f"{ke_term:.1%}; adjusted for that single difference the same reference implies "
    f"{peer_adj_pe:.2f} times, also on trailing earnings. The three give "
    + ' / '.join(f'{t[2]:,.2f}' for t in tri) +
    f", averaging {rel_ps:,.2f}. Left unadjusted, the struck reference alone would give "
    f"{rel_peer_unadjusted:,.2f} — the size of that gap IS the country-risk discount, and it is "
    f"shown rather than hidden inside a chosen multiple. The peers are not named and their "
    f"financials are not published, so this third leg cannot be rebuilt from peer filings; that "
    f"is a stated limitation of the leg, not a hidden one.")

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

# --- synthesis: TWO centres, one for each reading of the contested judgement ------
# The contested judgement is the provision charge, and this study's standing rule is that its
# two readings are never averaged into one number. The earlier edition broke that rule with
# its own headline: weighting Frame A and Frame B at 0.25 each IS a straight average of them,
# and it supplied a majority of the single centre published. There is no single centre now.
# Each frame carries the DCF weight in full, alongside the three lenses that do not depend on
# which reading is right, and the answer is published as a pair.
shared_lenses = [
    dict(name='Book value and sustainable return', value=book_ps, weight=V['w_book']),
    dict(name='Relative multiples', value=rel_ps, weight=V['w_rel']),
    dict(name='Normalised earnings power', value=norm_ps, weight=V['w_norm']),
]
W_DCF = V['w_dcf']


def weighted_centre(dcf_ps):
    """THE RETIRED BLEND, kept in one function so the change is legible and priced."""
    return W_DCF * dcf_ps + sum(l['value'] * l['weight'] for l in shared_lenses)


# [R-LENS-03]: ONE CLASS PRIMARY IS THE CENTRAL, AND THIS STUDY HAS TWO OF THEM because
# it publishes two frames rather than averaging them. Each frame's centre is now its OWN
# cash-flow read, and the three other lenses are cross-checks published beside both.
# The typed 50/20/15/15 weights had never cleared an out-of-sample test — chosen, written
# down, inherited — and they pulled BOTH frames toward the same three shared numbers,
# which is the opposite of what a two-sided answer is for: the whole point is that the
# contested judgement moves the answer, and blending it against three readings that do
# not depend on it damps exactly the disagreement the reader is being shown.
blend_A = weighted_centre(dcf_A['per_share'])
blend_B = weighted_centre(dcf_B['per_share'])
centre_A = dcf_A['per_share']
centre_B = dcf_B['per_share']
lenses_A = [dict(name='Discounted cash flow — Frame A (THE CENTRE)',
                 value=dcf_A['per_share'], weight=1.0, role='primary')] + \
    [dict(l, weight=0.0, role='cross_check') for l in shared_lenses]
lenses_B = [dict(name='Discounted cash flow — Frame B (THE CENTRE)',
                 value=dcf_B['per_share'], weight=1.0, role='primary')] + \
    [dict(l, weight=0.0, role='cross_check') for l in shared_lenses]
vals = [dcf_A['per_share'], dcf_B['per_share'], book_ps, rel_ps, norm_ps]
fair_bear, fair_bull = min(vals), max(vals)
say('')
say(f"[Synthesis — one lens per frame, not a blend] the centre of each frame IS its own "
    f"cash-flow read: Frame A {centre_A:,.2f}, Frame B {centre_B:,.2f}, against a "
    f"{V['spot']:,.2f} market price ({centre_A/V['spot']-1:+.1%} and "
    f"{centre_B/V['spot']-1:+.1%}). The three lenses that do not turn on the contested "
    f"judgement are published beside both and averaged into neither: " +
    ' · '.join(f"{l['name']} {l['value']:,.2f}" for l in shared_lenses) +
    f". The retired 50/20/15/15 blend read {blend_A:,.2f} and {blend_B:,.2f} — it pulled "
    f"BOTH frames toward the same three shared numbers, which damps precisely the "
    f"disagreement a two-sided answer exists to show, and its weights had never cleared "
    f"an out-of-sample test. NORMALISED EARNINGS POWER, at {norm_ps:,.2f}, is computed "
    f"and published and is NOT one of the lenses: the registry does not permit it for "
    f"this class. The field across all five readings runs {fair_bear:,.2f} to "
    f"{fair_bull:,.2f}.")

# ============================ SENSITIVITY =====================================
# The ramp the reverse valuation puts the incremental revenue on. PUBLISHED, because the
# answer it produces is meaningless without it: a hurdle placed entirely in the terminal year
# is a different — and easier — hurdle than the same total reached along a path.
CRUX_RAMP = [0.0, 0.10, 0.30, 0.60, 1.00]

# The provision charge, read every way the disclosed statements allow. Computed here so no
# reading of it is quoted from prose.
_prov_hist = [(V['prov_fy23'], V['rev_fy23']), (V['prov_fy24'], V['rev_fy24']),
              (V['prov_fy25'], V['rev_fy25'])]
_ecl_hist = [(V['ecl_fy23'], V['rev_fy23']), (V['ecl_fy24'], V['rev_fy24']),
             (V['ecl_fy25'], V['rev_fy25'])]
PROV_3YR_MEAN = float(np.mean([p / r for p, r in _prov_hist]))
PROV_ECL_3YR_MEAN = float(np.mean([p / r for p, r in _ecl_hist]))
PROV_2YR_MEAN = float(np.mean([_prov_hist[0][0] / _prov_hist[0][1],
                               _prov_hist[2][0] / _prov_hist[2][1]]))


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
    wt = (1 - wd_term) * ket_ + wd_term * kd_term_at
    dr = [wt + (w0 - wt) * glide_frac[i] for i in range(n)]
    d_, a_ = [], 1.0
    for i in range(n):
        a_ *= (1 + dr[i]); d_.append(1 / a_)
    # revenue side
    pd_, pe_, rd_, re_ = dom_packs25, exp_packs25, dom_ppp25, exp_ppp_usd25
    pt_, ft_, st_ = toll_packs25, toll_fee_pp25, resale_pp25
    rev_, cog_, pk_ = [], [], []
    ei = {k: 1.0 for k in cs}
    fxp = V['fx_avg_fy25']
    for i in range(n):
        pd_ *= (1 + V['dom_pack_growth'][i] + dom_vol_shift)
        pe_ *= (1 + V['exp_pack_growth'][i])
        rd_ *= (1 + V['dom_price_growth'][i])
        re_ *= (1 + V['exp_price_usd_growth'][i])
        pt_ *= (1 + V['toll_growth'][i])
        ft_ *= (1 + V['dom_price_growth'][i])
        st_ *= (1 + V['dom_price_growth'][i])
        f_ = fx[i] * fx_scale
        rev_.append((pd_ * rd_ + pe_ * re_ * f_ + pt_ * ft_ + pt_ * st_) * consol_uplift)
        pk_.append(pd_ + pe_ + pt_)
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
    cip_close_ = cip_b_
    dna_ = [dep_[i] + amort[i] for i in range(n)]
    pv_pct = V['prov_pct_permanent'] if prov_pct is None else prov_pct
    xrev = [extra_rev_fy30 * r for r in CRUX_RAMP]
    ebit_ = [rev_[i] - cog_[i] - rev_[i] * (V['mkt_pct'][i] + V['rnd_pct'][i] + V['ga_pct'][i])
             - rev_[i] * pv_pct - dna_[i] - BOARD_FEE + xrev[i] * extra_margin
             for i in range(n)]
    rev_ = [rev_[i] + xrev[i] for i in range(n)]
    # ANY INCREMENTAL REVENUE IS CHARGED THE SAME REINVESTMENT IDENTITY AS THE EXISTING
    # BUSINESS: capital expenditure at the same share of revenue, and working capital on the
    # same day ratios applied to its own revenue and its own cost of sales. The earlier
    # edition let the incremental revenue arrive free of both, which made the hurdle the
    # market's price implies look easier than the model's own discipline requires.
    cap_ = [cap_[i] + xrev[i] * V['capex_pct'][i] for i in range(n)]
    cog_ = [cog_[i] + xrev[i] * (1 - extra_margin) for i in range(n)]
    cogs_full_ = [cog_[i] + dna_[i] * DEP_COGS_SHARE for i in range(n)]
    inv_ = [cogs_full_[i] * V['dio'][i] / 365 for i in range(n)]
    ar_ = [rev_[i] * V['dso'][i] / 365 for i in range(n)]
    ap_ = [cogs_full_[i] * V['dpo'][i] / 365 for i in range(n)]
    od_ = [V['othdr_fy25'] * rev_[i] / V['rev_fy25'] for i in range(n)]
    oc_ = [V['othcr_fy25'] * rev_[i] / V['rev_fy25'] for i in range(n)]
    wc_ = [inv_[i] + ar_[i] + od_[i] - ap_[i] - oc_[i] for i in range(n)]
    dwc_ = [wc_[0] - wc0] + [wc_[i] - wc_[i - 1] for i in range(1, n)]
    fc = [ebit_[i] * (1 - TAX_FCFF) + dna_[i] - cap_[i] - dwc_[i] for i in range(n)]
    pvs = sum(fc[i] * d_[i] for i in range(n))
    ic_ = ppe_b_ + cip_b_ + wc_[-1] + V['intang_fy25']
    roic_ = ebit_[-1] * (1 - TAX_FCFF) / ic_
    nt = (ebit_[-1] * (1 - TAX_FCFF) * (1 + g)
          - cip_close_ * dr_rate * (1 - TAX_FCFF))
    # The terminal is built through the sanctioned module here too. A sensitivity grid
    # that keeps the retired construction grades a model the study no longer publishes,
    # and this study's own base assert is what caught it. A scenario states its growth
    # as a NOMINAL rate because that is what a reader varies; it is converted to the
    # REAL rate against the same house inflation, so the module derives back exactly the
    # nominal that was asked for and no rate is typed twice.
    try:
        tv_ = TV.build(TV.TerminalInputs(
            nopat=nt, wacc=max(wt, g + 0.02), inflation=PI_TERM,
            real_growth=(1.0 + g) / (1.0 + PI_TERM) - 1.0,
            dna_book=dna_[-1] * (1 + g),
            useful_life_years=V['asset_life_weighted'],
            useful_life_source=INP['asset_life_weighted']['source'],
            maintenance_basis='book_dna_escalated',
            working_capital=wc_[-1] * (1 + g),
            incremental_capital_per_unit_growth=_inc_cap_base)).tv
    except TV.TerminalRefused:
        return float('nan')
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
# The three readings of the provision charge that anyone auditing this study will ask for,
# published together rather than argued about: the level carried, the mean of the three
# disclosed years, and the expected-credit-loss component alone.
PROV_READINGS = [
    ('Carried — struck above the two non-outlier years', V['prov_pct_permanent']),
    ('Mean of the three disclosed years, including the FY2024 spike', PROV_3YR_MEAN),
    ('Expected-credit-loss component alone, three-year mean', PROV_ECL_3YR_MEAN),
    ('The two non-outlier years, FY2023 and FY2025', PROV_2YR_MEAN),
]
prov_readings = [(name, p, dcf_at(prov_pct=p)) for name, p in PROV_READINGS]
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
            facility_investment_usd_mn=V['plant_cost_usd_mn'],
            required_rev_usd_mn=req_rev / fx[-1],
            asset_turn=req_rev / (V['plant_cost_usd_mn'] * fx[-1]),
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
say(f"  Two things that must be published for that hurdle to be auditable, and were not before. "
    f"THE RAMP: the incremental revenue is not dropped into the final year, it is phased "
    + ' / '.join(f'{r:.0%}' for r in CRUX_RAMP) +
    f" across FY2026E-FY2030E, and the same total placed entirely in FY2030E would be a lower "
    f"and easier hurdle. THE REINVESTMENT: the incremental revenue is charged capital "
    f"expenditure at the same share of revenue as the existing business and working capital on "
    f"the same day ratios, so it faces the identical reinvestment discipline. The earlier "
    f"edition let it arrive free of both and published a hurdle of about USD 115 million; "
    f"charged properly it is USD {crux['required_rev_usd_mn']:,.0f} million.")


# ======================= FORECAST ANCHOR ======================================
# [R-ANCHOR-01] THE FORECAST IS ANCHORED ON THE LATEST REVIEWED PERIOD, AND A
# DECLINE AWAY FROM IT NAMES ITS MECHANISM. The record is printed for every study
# whether or not it fires. THIS ONE FIRES ON BOTH CLAUSES, and the record says so
# rather than the study carrying the decline in silence.
#
# THE ANCHOR IS THE REVIEWED QUARTER, NOT THE AUDITED YEAR: a near-term reviewed
# actual outranks a stale full-year rate, and the most recent period this model
# consumes is the three months to 31 March 2026. Its gross margin is read straight
# off the reviewed income statement -- gross profit over net sales -- and the same
# statement carries the comparative quarter, which is where the like-for-like
# measurement comes from. Nothing here is estimated: every figure below is a
# committed input or a committed model series.
_FA_Q1_GM      = V['q1_gp'] / V['q1_rev']
_FA_Q1_GM_LY   = V['q1_gp_ly'] / V['q1_rev_ly']
_FA_Q1_COST    = (V['q1_rev'] - V['q1_gp']) / V['q1_rev']
_FA_Q1_COST_LY = (V['q1_rev_ly'] - V['q1_gp_ly']) / V['q1_rev_ly']
_FA_Q1_DNA_R    = V['q1_dna'] / V['q1_rev']
_FA_Q1_DNA_R_LY = V['q1_dna_ly'] / V['q1_rev_ly']
# per-pack rates, filed against filed on both sides: packs from the Board of
# Directors' report, revenue and cost of sales from the audited statements; the
# forecast year uses the identical construction on the model's own series
_FA_RPP24, _FA_RPP25 = (hist['FY2024']['revenue'] / V['packs_sold_fy24'],
                        hist['FY2025']['revenue'] / V['packs_sold_fy25'])
_FA_CPP24, _FA_CPP25 = (hist['FY2024']['cogs'] / V['packs_sold_fy24'],
                        hist['FY2025']['cogs'] / V['packs_sold_fy25'])
_FA_RPP26, _FA_CPP26 = revenue[0] / packs_total[0], cogs[0] / packs_total[0]
# where the fall against the audited base year sits: the cash stack against the
# production share of depreciation, both as a share of revenue. The audited note
# gives the FY2025 split; the forecast year is the model's own.
_FA_CASH25 = (hist['FY2025']['cogs'] - V['dep_in_cogs_fy25']) / hist['FY2025']['revenue']
_FA_DEP25  = V['dep_in_cogs_fy25'] / hist['FY2025']['revenue']
_FA_CASH26 = cogs_cash[0] / revenue[0]
_FA_DEP26  = dna[0] * DEP_COGS_SHARE / revenue[0]
# the domestic price leg against the house ladder it is escalated beside
_FA_REAL_DOM = [(1 + V['dom_price_growth'][i]) / (1 + V['esc_domestic_cpi'][i]) - 1
                for i in range(n)]
_FA_REAL_CUM = 1.0
for _r in _FA_REAL_DOM:
    _FA_REAL_CUM *= (1 + _r)

FORECAST_ANCHOR = dict(
    rate_name='gross margin',
    latest_reviewed_period='Q1-2026, reviewed interim',
    latest_reviewed_date='2026-03-31',
    latest_reviewed_rate=float(_FA_Q1_GM),
    first_forecast_rate=float(gross_margin[0]),
    forecast_path=[float(g) for g in gross_margin],
    mechanism=dict(
        name='input_cost_outpacing_price',
        disclosure=(
            'the audited FY2025 cost-of-sales note splits production cost by nature: raw '
            'materials %.2f%%, packaging materials %.2f%%, labour %.2f%%, fuel, oils, '
            'electricity, water and lighting %.2f%%, other consumables and services %.2f%%, '
            'depreciation %.2f%%. The raw-material leg is imported active pharmaceutical '
            'ingredient and part of the packaging leg is imported film, foil and closures, '
            'so on the study\'s registered import share of packaging %.1f%% of the CASH cost '
            'stack -- those same lines excluding the depreciation shown above -- is priced '
            'abroad and reaches the income statement through the exchange '
            'rate, which the FY2025 foreign-currency note states at EGP %.2f to the dollar on '
            'average during the period. The output price is not on the same clock: the '
            'domestic leg is administratively priced and moves in approved steps, and the '
            'export leg is set in dollars. The two legs separate visibly in the '
            'company\'s own filings twice over. In the reviewed first quarter of 2026 net '
            'sales rose %.1f%% on the comparative quarter while cost of sales rose %.1f%%. '
            'In the audited pair FY2024 to FY2025, on the pack counts the Board of '
            'Directors\' report discloses, revenue per pack rose %.2f%% against cost of '
            'sales per pack %.2f%%, and the audited gross margin fell from %.2f%% to %.2f%%.'
            % (100 * cs_all['materials'], 100 * cs_all['packaging'], 100 * cs_all['labour'],
               100 * cs_all['energy'], 100 * cs_all['services_other'],
               100 * cs_all['depreciation'], 100 * fx_cost_share, V['fx_avg_fy25'],
               100 * (V['q1_rev'] / V['q1_rev_ly'] - 1),
               100 * ((V['q1_rev'] - V['q1_gp']) / (V['q1_rev_ly'] - V['q1_gp_ly']) - 1),
               100 * (_FA_RPP25 / _FA_RPP24 - 1), 100 * (_FA_CPP25 / _FA_CPP24 - 1),
               100 * hist['FY2024']['gross_margin'], 100 * hist['FY2025']['gross_margin'])),
        like_for_like=dict(
            measures='cost of sales per unit of revenue, the reviewed first quarter of 2026 '
                     'against the comparative quarter presented in the same filing',
            period_a='Q1-2025, the comparative quarter (three months ended 31 March 2025)',
            value_a=float(_FA_Q1_COST_LY),
            period_b='Q1-2026, reviewed (three months ended 31 March 2026)',
            value_b=float(_FA_Q1_COST),
            higher_is_worse=True)),
    note=(
        'BOTH CLAUSES FIRE AND THE RECORD SAYS SO. The forecast opens at %.2f%% against a '
        'latest reviewed %.2f%%, %.2f points and %.1f%% relatively below it, and then falls '
        'a further %.1f%% relative from its own opening year to %.2f%% in the final explicit '
        'year. The audited record is FY2023 %.2f%%, FY2024 %.2f%%, FY2025 %.2f%%; the '
        'reviewed first quarter of 2026 is %.2f%% against a comparative quarter of %.2f%%, '
        'so the company was already running below its audited years before the forecast '
        'starts. WHERE THE FALL SITS, against the audited base year: the cash cost stack '
        'goes from %.2f%% of revenue to %.2f%% and the production share of depreciation '
        'from %.2f%% to %.2f%%, so roughly three quarters of the %.2f-point fall is the '
        'cost stack and the rest is the new facility beginning to depreciate. THE '
        'COMMISSIONING STEP IS ALREADY PARTLY INSIDE THE ANCHOR and that is why it is not '
        'the mechanism named: the reviewed quarter carries depreciation and amortisation of '
        '%.2f%% of revenue against %.2f%% in the comparative quarter, the transfer out of '
        'construction arriving on the company\'s own schedule. WHAT THE FILINGS DO NOT '
        'ESTABLISH IS THE MAGNITUDE, and this record does not pretend otherwise. The '
        'direction agrees with the company\'s own accounts on both measured pairs, but the '
        'model opens a far wider wedge than the filings have ever shown: revenue per pack '
        '%+.2f%% against cost of sales per pack %+.2f%% in the first forecast year, against '
        'a filed FY2024-to-FY2025 pair of %+.2f%% and %+.2f%%. The domestic realised price '
        'is escalated at %.1f%% in the first year against a house consumer-inflation ladder '
        'of %.1f%%, and %.1f%% cumulatively in real terms across the explicit window, while '
        'the domestic cost legs escalate on that same ladder and the labour and energy legs '
        'above it. The company\'s own filed domestic realised price per pack rose %.2f%% in '
        'FY2025. A real price cut compounding for five years is a claim about the world; the '
        'filings give it a direction and they do not give it that size, and the input '
        'register\'s own justification for the path says price growth tracks domestic '
        'inflation with no real price gain, which these numbers are not. That is registered '
        'here rather than corrected, because this record is a measurement of what the model '
        'does and the correction is a rebuild.'
        % (100 * gross_margin[0], 100 * _FA_Q1_GM,
           100 * (_FA_Q1_GM - gross_margin[0]),
           100 * (_FA_Q1_GM - gross_margin[0]) / _FA_Q1_GM,
           100 * (gross_margin[0] - min(gross_margin)) / gross_margin[0],
           100 * min(gross_margin),
           100 * hist['FY2023']['gross_margin'], 100 * hist['FY2024']['gross_margin'],
           100 * hist['FY2025']['gross_margin'], 100 * _FA_Q1_GM, 100 * _FA_Q1_GM_LY,
           100 * _FA_CASH25, 100 * _FA_CASH26, 100 * _FA_DEP25, 100 * _FA_DEP26,
           100 * (hist['FY2025']['gross_margin'] - gross_margin[0]),
           100 * _FA_Q1_DNA_R, 100 * _FA_Q1_DNA_R_LY,
           100 * (_FA_RPP26 / _FA_RPP25 - 1), 100 * (_FA_CPP26 / _FA_CPP25 - 1),
           100 * (_FA_RPP25 / _FA_RPP24 - 1), 100 * (_FA_CPP25 / _FA_CPP24 - 1),
           100 * V['dom_price_growth'][0], 100 * V['esc_domestic_cpi'][0],
           100 * (_FA_REAL_CUM - 1),
           100 * (dom_ppp25 / dom_ppp24 - 1))))

say('')
say('[Forecast anchor] gross margin: latest reviewed period Q1-2026 at '
    f'{_FA_Q1_GM:.2%}, first forecast year {gross_margin[0]:.2%}, '
    f'{100 * (gross_margin[0] - _FA_Q1_GM):+.2f} points and '
    f'{100 * (gross_margin[0] - _FA_Q1_GM) / _FA_Q1_GM:+.1f}% relative. Path low '
    f'{min(gross_margin):.2%}. Mechanism named: input cost outpacing price; measured '
    f'cost per unit of revenue {_FA_Q1_COST_LY:.4f} -> {_FA_Q1_COST:.4f} in the '
    f'company\'s own quarter pair.')

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
                    dom_own_rev_fy25=dom_own_rev25, dom_own_rev_fy24=dom_own_rev24,
                    contract_resale_fy25=contract_resale25,
                    contract_resale_fy24=contract_resale24,
                    toll_packs_fy25=toll_packs25, toll_packs_fy24=toll_packs24,
                    toll_fee_pp_fy25=toll_fee_pp25, toll_fee_pp_fy24=toll_fee_pp24,
                    resale_pp_fy25=resale_pp25, resale_pp_fy24=resale_pp24,
                    utilisation_fy25=V['units_prod_fy25'] / V['units_cap'],
                    utilisation_fy24=V['units_prod_fy24'] / V['units_cap'],
                    consol_uplift=consol_uplift, unit_cost_fy25=unit_cost25),
    forecast=dict(years=YEARS, dom_packs=dom_packs, exp_packs=exp_packs, dom_price=dom_ppp,
                  exp_price_usd=exp_ppp_usd, fx=fx, rev_dom=rev_dom, rev_exp=rev_exp, toll=toll,
                  toll_packs=toll_packs, toll_fee_pp=toll_fee_pp, resale_pp=resale_pp,
                  rev_resale=rev_resale,
                  revenue=revenue, packs_total=packs_total, unit_cash_cost=unit_costs,
                  cogs_cash=cogs_cash, cogs=cogs, dep_cogs_share=DEP_COGS_SHARE,
                  gross_profit=gross_profit, gross_margin=gross_margin,
                  marketing=mkt_f, rnd=rnd_f, ga=ga_f, prov_A=prov_A, prov_B=prov_B,
                  ebitda_A=ebitda_A, ebitda_B=ebitda_B, ebit_A=ebit_A, ebit_B=ebit_B,
                  dna=dna, dep=dep, amort=amort, capex=capex, ppe=ppe, cip=cip,
                  inventory=inv_f, receivables=ar_f, payables=ap_f, other_dr=othdr_f,
                  other_cr=othcr_f, wc=wc, dwc=dwc, wc0=wc0, equity=eq_path, roe=roe_fwd,
                  esc_trace=esc_trace, board_fee=BOARD_FEE, nci_fwd=NCI_FWD,
                  parent=parent_path, retained=retained_path,
                  eps=[p / V['shares_mn'] for p in parent_path],
                  cash=cash_f, debt=debt_f, net_debt=net_debt_f, assets=assets_f,
                  oth_nc=OTH_NC_FWD, ptx=PTX_FWD, bs_gap_frozen=bs_gap_old,
                  int_rate_implied=[V['int_path'][i]
                                    / ((debt_f[i] + (gross_debt_open if i == 0 else debt_f[i-1])) / 2)
                                    for i in range(n)]),
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
              wd_term=wd_term, wd_term_market=wd_term_market, wd_term_book=wd_term_book,
              wacc_term_book_basis=wacc_term_alt, tax_fcff=TAX_FCFF, tax_stat=TAX,
              crp_rating=V['crp_rating'], crp_cds=V['crp_cds'],
              beta_regression=beta_res),
    dcf=dict(frame_A=dcf_A, frame_B=dcf_B),
    # A TWO-SIDED ANSWER IN THE SHAPE EVERY GATE READS. This study publishes two named
    # branches and no average — which is right, and was INVISIBLE: the gap gate, the
    # publish block and the blend census all resolve a study's answer through a top-level
    # central, found none, and reported PHAR unreadable rather than breaching. An
    # unreadable study is held either way, so nothing shipped wrongly; what was lost is
    # that the number nobody could read was 34% below the market, which is exactly the
    # region [R-GAP-01] exists to audit.
    # [R-MACRO-01 AMENDED]: every INFLATION-CLASS input, named with the mapping that
    # derives it from the house ladder, declared even when empty. The rule's own lesson
    # is that a check reading what a study DECLARES is not checking what it USES — and
    # this study is the case in point: its declared growth lines were fine while an
    # input named nowhere in the record, the domestic consumer-price path, drove the
    # cost stack AND the purchasing-power wedge and therefore the whole currency path.
    # DERIVED QUANTITIES, committed where a builder can read them. They are NOT inputs
    # and do not belong in the four-field register — a register is for figures with a
    # source and a date, and a derived rate's provenance is the derivation. Builders
    # read them from here so no document re-derives one differently.
    derived=dict(
        g_term=V['g_term'], g_term_real=V['g_term_real'], pi_term=PI_TERM,
        rf_term=V['rf_term'],
        note='the terminal nominal growth and the terminal risk-free rate are both '
             'computed from the house long-run inflation of %.1f%% — the growth as '
             '(1+inflation)(1+real)-1 at %.2f%% real, the risk-free as inflation plus '
             'the %.1f-point real-rate convention. Neither can be typed, so neither can '
             'disagree with the inflation the rest of the model uses.'
             % (100 * PI_TERM, 100 * V['g_term_real'],
                100 * _EG.raw['real_rate_convention']['value'])),
    macro_record=dict(
        market='EG', path_as_of=_EG.as_of, explicit_years=[2026, 2027, 2028, 2029, 2030],
        inflation_inputs=[
            dict(key='esc_domestic_cpi', mapping='calendar', first_year=2026,
                 exempt_head=0, values=list(V['esc_domestic_cpi']),
                 note='the house calendar ladder exactly, at zero real: this study '
                      'carries no inflation rate of its own'),
        ],
        # the gate compares this list against its own derived purchasing-power path, so
        # it is the LIST and the metadata sits beside it rather than wrapping it
        # NO fx_base: the house path's own default base is the 2025 period average it
        # registers, and passing the August spot instead makes the check derive from
        # a different anchor than the study built on — the two must be the same
        # object or the comparison is between two constructions rather than one.
        fx_path=list(V['fx_path']),
        fx_path_note=dict(
            mapping='calendar', first_year=2026,
            exempt_head=0,
            registered_tension='The derivation compounds a full year of purchasing-power '
                               'depreciation onto a quote taken EIGHT MONTHS INTO that '
                               'year, so the FY2026 average comes out at 56.87 while the '
                               'same house path reads 50.25 on 6 August 2026 — which '
                               'would need roughly 70 by December. The study CONFORMS '
                               'rather than inventing an anchor, and this is registered '
                               'as a property of the house path\'s first year that will '
                               'reach every Egyptian study committing a currency path.',
            derivation='relative purchasing-power parity on the house inflation ladder '
                       'against long-run United States inflation of %.1f%%, compounded '
                       'year by year from that anchor' % (100 * _US_LT)),
        terminal=dict(g_nominal=V['g_term'], real=V['g_term_real'], rf=V['rf_term'],
                      inflation_in_rf=PI_TERM, inflation=PI_TERM,
                      real_growth=V['g_term_real'], nominal_growth=V['g_term'],
                      note='zero real growth: the business holds its scale in real terms '
                           'in perpetuity, and the nominal rate is DERIVED from the house '
                           'terminal inflation rather than typed. The previous edition '
                           'typed 5% nominal and described it as "approximately zero real "'
                           'terminal growth", which against a 7% long-run rate is a real '
                           'DECLINE of 1.87% a year, in perpetuity, that nothing in the '
                           'study argued for'),
        growth_lines=[
            dict(name='domestic service and consumable cost escalation',
                 years=[2026, 2027, 2028, 2029, 2030],
                 nominal=list(V['esc_domestic_cpi']), real=0.0,
                 basis='the house ladder at zero real growth'),
        ],
        note=('The active-ingredient escalation of %.1f%% and the export price growth of '
              '%.1f%% are quoted in US DOLLARS and are not inflation-class inputs on this '
              'path: they escalate a hard-currency price and reach the pound only through '
              'the derived currency path above, which is where this ladder governs them.'
              % (100 * V['esc_materials_usd'], 100 * V['exp_price_usd_growth'][0])),
    ),
    central_two_sided=dict(
        why="the provision charge is the study's single most consequential contested "
            "judgement and the two readings of it are published side by side, never "
            "averaged: averaging them would state a number neither branch supports.",
        branches=[
            dict(label='Frame A — provision charge permanent at 5.25% of revenue',
                 value=centre_A,
                 condition="the elevated receivable-provision charge of the last two "
                           "years is the new normal"),
            dict(label='Frame B — provision charge normalising to 2.5% of revenue',
                 value=centre_B,
                 condition="the charge reverts toward the level the company ran before "
                           "the currency devaluation"),
        ]),
    spot=V['spot'], spot_date=INP['spot']['date'],
    # [R-ANCHOR-01]: the forecast rate against the latest reviewed period, printed
    # for every study whether or not it fires. This one fires on both clauses.
    forecast_anchor=FORECAST_ANCHOR,
    lens_record=dict(**{'class': 'pharmaceutical manufacturer, generic and branded'},
        primary=dict(kind='dcf', two_sided=True, value=None,
                     range=dict(low=min(centre_A, centre_B),
                                high=max(centre_A, centre_B)),
                     range_note="the two published frames of the contested provision "
                                "judgement, each its own present-value read on one "
                                "clock — not a spread across methods and not a spread "
                                "invented around a point",
                     range_basis=dict(
                         driver="the receivable-provision charge as a share of revenue, "
                                "5.25% against 2.5%",
                         low=min(centre_A, centre_B), high=max(centre_A, centre_B),
                         units="EGP per share, the present-value read under each frame",
                         macro_held=True,
                         evidence="both frames re-run the same unit build with only the "
                                  "provision charge changed; the cost of capital, the "
                                  "inflation path, the derived terminal growth and the "
                                  "terminal construction are identical in both, so the "
                                  "spread is the judgement and nothing else")),
        cross_checks=[
            dict(kind='relative_multiple', value=rel_ps, present_value=False,
                 # THE ADOPTED MULTIPLE IS THE MEAN OF THE THREE LEGS, and it is
                 # committed rather than described: a source named in prose is an
                 # attestation, and the multiple is the thing that can be checked.
                 multiple=sum(m for _, m, _ in tri) / len(tri),
                 multiple_legs=[dict(basis=b, multiple=float(m), value=float(v))
                                for b, m, v in tri],
                 # The circularity check: what multiple the TRADED price implies on the
                 # same metric, so a reader can see the lens is not the price wearing a
                 # different label. Trailing attributable profit on the count in issue.
                 circularity=dict(spot=V['spot'], shares=V['shares_mn'],
                                  net_debt=net_debt,
                                  metric_value=V['np_fy25']),
                 multiple_source="three multiples applied to the earnings of their own "
                                 "periods — one justified by this model's own economics, "
                                 "one the company's own four-year mean of year-end close "
                                 "over audited attributable profit, and one struck "
                                 "reference adjusted for the cost-of-equity difference; "
                                 "never a multiple read off the current price",
                 note="the peers behind the third leg are not named and their financials "
                      "are not published, so that leg cannot be rebuilt from peer "
                      "filings — a stated limitation of the leg"),
            dict(kind='book_value', value=book_ps, present_value=False, floor=True,
                 note="a disclosed FLOOR on a justified price-to-book, published as such "
                      "and never weighted")],
        cross_checks_not_built=[
            dict(kind='ev_ebitda_own_history',
                 why="this class permits an enterprise multiple on the company's own "
                     "history and this study publishes an EARNINGS multiple on its own "
                     "history instead. The enterprise version needs a series of past "
                     "enterprise values, which needs past net debt at each year end on a "
                     "consistent definition across a period spanning two devaluations. "
                     "Named rather than quietly absent.")],
        lenses_excluded=[
            dict(kind='normalized_earnings', value=norm_ps,
                 why="not a permitted lens for any class in the registry. It is computed "
                     "and published as an observation; it does not enter either centre.")],
        envelope=dict(low=min(centre_A, centre_B), high=max(centre_A, centre_B)),
        central=None,
        retired_blend=dict(
            weights=dict(dcf=W_DCF, book=V['w_book'], relative=V['w_rel'],
                         normalized=V['w_norm']),
            value_frame_A=blend_A, value_frame_B=blend_B,
            why_retired="typed weights that had never cleared an out-of-sample test, one "
                        "of the four lenses is not permitted for any class, and blending "
                        "each frame against three readings that do NOT depend on the "
                        "contested judgement damps precisely the disagreement a two-sided "
                        "answer exists to show")),
    lenses=dict(items_A=lenses_A, items_B=lenses_B, shared=shared_lenses, w_dcf=W_DCF,
                centre_A=centre_A, centre_B=centre_B,
                blend_A=blend_A, blend_B=blend_B,
                fair_bear=fair_bear, fair_bull=fair_bull,
                book_ps=book_ps, bv_ps=bv_ps, just_pb=just_pb, roe_sust=roe_sust,
                roe_fy24=roe_fy24, roe_fy25=roe_fy25,
                rel_ps=rel_ps, rel_lo=rel_lo, rel_hi=rel_hi,
                rel_triangulation=[[t[0], float(t[1]), float(t[2])] for t in tri],
                rel_peer_unadjusted=rel_peer_unadjusted, just_fwd_pe=just_fwd_pe,
                peer_adj_pe=peer_adj_pe, payout_implied=payout_implied,
                eps_26_A=eps_26_A, eps_26_B=eps_26_B, eps_fwd=eps_fwd,
                own_pe_history=own_hist, own_pe_mean=own_pe_mean, pe_now=pe_now,
                pe_now_wavg=pe_now_wavg, eps_ttm_wavg=eps_ttm_wavg,
                evebitda_now=evebitda_now, eps_ttm=eps_ttm, eps_27_A=eps_27_A,
                eps_27_B=eps_27_B, norm_ps=norm_ps, norm_margin=norm_margin,
                norm_pat_ps=norm_pat / V['shares_mn']),
    sensitivity=dict(**{k: [[float(a), float(b)] for a, b in v] for k, v in sens.items()},
                     grid=grid, grid_wacc=[-0.02, -0.01, 0.0, 0.01, 0.02],
                     grid_g=[0.03, 0.04, 0.05, 0.06, 0.07],
                     grid_lo=float(min(min(r) for r in grid)),
                     grid_hi=float(max(max(r) for r in grid)),
                     prov_readings=[[a, float(b), float(c)] for a, b, c in prov_readings],
                     prov_3yr_mean=PROV_3YR_MEAN, prov_ecl_3yr_mean=PROV_ECL_3YR_MEAN,
                     prov_2yr_mean=PROV_2YR_MEAN),
    crux=crux,
    crux_ramp=CRUX_RAMP,
    cost_exposure=dict(fx_cost_share=fx_cost_share,
                       fx_cost_share_if_all_packaging_imported=fx_cost_share_all_packaging,
                       fx_cost_share_full_stack=fx_cost_share_full,
                       fx_cost_share_full_stack_if_all_packaging=fx_cost_share_full_all_pack,
                       materials_share=cs['materials'], packaging_share=cs['packaging'],
                       packaging_import_share=V['esc_packaging_import_share']),
    working_capital=dict(dio_fy25=dio0, dso_fy25=dso0, dpo_fy25=dpo0,
                         ccc_fy25=dio0 + dso0 - dpo0),
    calibration=dict(step0=step0, backtest=bt5),
    narrative=NARR,
)

_out_path = os.environ.get('PHAR_OUT', os.path.join(HERE, 'study_numbers.json'))
with open(_out_path, 'w') as f:
    json.dump(OUT, f, indent=1, default=float)
print('\nwrote study_numbers.json')
print(f"FAIR VALUE FIELD  bear {fair_bear:,.2f} · centre A {centre_A:,.2f} · centre B "
      f"{centre_B:,.2f} · bull {fair_bull:,.2f} | spot {V['spot']:,.2f}")
