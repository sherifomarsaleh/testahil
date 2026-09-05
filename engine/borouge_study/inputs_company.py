"""BOROUGE — company-ring inputs, every one read off an official Borouge document.

SIGCM clause 1: the historical income statement, balance sheet and cash flow are
constructed ONLY from Borouge plc's own issued financial statements and its own
Management Discussion & Analysis. No aggregator, broker note or press summary is a
source for any figure in this file. The physical unit build (tonnes, utilisation,
benchmark prices, premia, per-tonne costs) comes from the company's own MDA, which
is the only Borouge document that discloses it; the audited statements confirm the
money totals those physicals roll up to, and the reconciliation is asserted in
compute.py rather than asserted in prose.

Every entry carries the four fields the depth bar requires: value, source, date,
research layer.
"""

def I(value, source, date, ring):
    return dict(value=value, source=source, date=date, ring=ring)


# ---- source short-names, spelled out once ----------------------------------
AFS25 = ("Borouge plc audited consolidated financial statements for the year ended "
         "31 December 2025 (statutory), Ernst & Young")
AFS24 = ("Borouge plc audited consolidated financial statements for the year ended "
         "31 December 2024 (statutory), Ernst & Young")
AFS23 = ("Borouge plc audited consolidated financial statements for the year ended "
         "31 December 2023 (statutory), Ernst & Young, signed 31 January 2024")
H126 = ("Borouge plc condensed consolidated interim financial statements for the six "
        "months ended 30 June 2026 (unaudited), reviewed")
MDA25 = "Borouge plc Q4/FY 2025 Management Discussion & Analysis"
MDA24 = "Borouge plc Q4/FY 2024 Management Discussion & Analysis"
MDA23 = "Borouge plc Q4/FY 2023 Management Discussion & Analysis"
MDA26 = "Borouge plc Q2 2026 Management Discussion & Analysis"
AR25 = "Borouge plc Annual Report 2025"

CO = "Company"

INP = dict(

    # ======================= MARKET ANCHORS =================================
    # RE-STRUCK ON THE LATEST KNOWN PRICE [R-GAP-01 AMENDED]. The study stood on the
    # 7-August close for a month. A fair value published against a month-old price is a
    # comparison a reader cannot use, whatever the fair value is worth — and this rebuild
    # moves the answer far enough that the price it is measured against decides whether the
    # study may publish at all.
    # WRITTEN FOR A READER. A first version of this source field named the repository file
    # the closes are committed in, which is internal plumbing and has no business in a
    # delivered bibliography; the vocabulary gate caught it the same minute.
    spot_aed=I(2.35, "Closing price 03-Sep-2026 on the Abu Dhabi Securities Exchange. It "
               "supersedes the 07-Aug-2026 close of 2.40 the previous edition was struck "
               "at",
               "2026-09-03", "Market"),
    aed_per_usd=I(3.6725, "AED/USD central parity. The dirham has been pegged to the US "
                  "dollar at this rate since November 1997 and the Central Bank of the "
                  "UAE has maintained it without interruption since",
                  "2026-08-07", "Country"),

    shares_issued=I(30_057_691_583, AFS25 + ", note 14 (share capital) and note 29: "
                    "30,057,691,583 ordinary shares of USD 0.16 each in issue",
                    "2025-12-31", CO),
    shares_wavg_fy25=I(29_937_557_774, AFS25 + ", note 29: weighted average number of "
                       "shares in issue for the year, after the weighted effect of "
                       "treasury shares acquired during 2025", "2025-12-31", CO),
    shares_wavg_fy24=I(30_057_691_583, AFS25 + ", note 29, comparative column",
                       "2024-12-31", CO),
    treasury_cost_h126=I(216_703, H126 + ", statement of changes in equity: cumulative "
                         "cost of own shares acquired, USD'000", "2026-06-30", CO),
    treasury_cost_fy25=I(158_223, AFS25 + ", note 31 (treasury shares), USD'000",
                         "2025-12-31", CO),

    # ======================= INCOME STATEMENT, USD'000 ======================
    # Three complete audited years, each read from the filing that reports it.
    rev_fy23=I(5_791_345, AFS23 + " — consolidated statement of profit or loss, revenue",
               "2023-12-31", CO),
    rev_fy24=I(6_026_123, AFS24 + " — consolidated statement of profit or loss, revenue",
               "2024-12-31", CO),
    rev_fy25=I(5_847_773, AFS25 + " — consolidated statement of profit or loss, revenue "
               "(note 19)", "2025-12-31", CO),
    cogs_fy23=I(3_627_383, AFS23 + " — cost of sales", "2023-12-31", CO),
    cogs_fy24=I(3_490_989, AFS24 + " — cost of sales", "2024-12-31", CO),
    cogs_fy25=I(3_565_985, AFS25 + " — cost of sales (note 20)", "2025-12-31", CO),
    othinc_fy23=I(17_350, AFS23 + " — other income", "2023-12-31", CO),
    othinc_fy24=I(53_951, AFS24 + " — other income", "2024-12-31", CO),
    othinc_fy25=I(26_321, AFS25 + " — other income (note 22)", "2025-12-31", CO),
    ga_fy23=I(182_915, AFS23 + " — general and administrative expenses",
              "2023-12-31", CO),
    ga_fy24=I(193_121, AFS24 + " — general and administrative expenses",
              "2024-12-31", CO),
    ga_fy25=I(196_577, AFS25 + " — general and administrative expenses (note 23)",
              "2025-12-31", CO),
    sd_fy23=I(399_495, AFS23 + " — selling and distribution expenses", "2023-12-31", CO),
    sd_fy24=I(471_963, AFS24 + " — selling and distribution expenses", "2024-12-31", CO),
    sd_fy25=I(416_028, AFS25 + " — selling and distribution expenses (note 24)",
              "2025-12-31", CO),
    imp_fy23=I(1_731, AFS23 + " — impairment loss on property, plant and equipment and "
               "intangible assets", "2023-12-31", CO),
    imp_fy24=I(3_082, AFS24 + " — impairment loss on property, plant and equipment and "
               "intangible assets", "2024-12-31", CO),
    imp_fy25=I(1_441, AFS25 + " — impairment loss on property, plant and equipment and "
               "intangible assets (note 6)", "2025-12-31", CO),
    ebit_fy23=I(1_597_171, AFS23 + " — operating profit", "2023-12-31", CO),
    ebit_fy24=I(1_920_919, AFS24 + " — operating profit", "2024-12-31", CO),
    ebit_fy25=I(1_694_063, AFS25 + " — operating profit", "2025-12-31", CO),
    fininc_fy23=I(26_815, AFS23 + " — finance income", "2023-12-31", CO),
    fininc_fy24=I(28_554, AFS24 + " — finance income", "2024-12-31", CO),
    fininc_fy25=I(23_718, AFS25 + " — finance income", "2025-12-31", CO),
    fincost_fy23=I(220_909, AFS23 + " — finance costs", "2023-12-31", CO),
    fincost_fy24=I(202_025, AFS24 + " — finance costs", "2024-12-31", CO),
    fincost_fy25=I(175_924, AFS25 + " — finance costs (note 17.1: interest on loans "
                   "164,476, interest on lease liabilities 6,193, others 5,255)",
                   "2025-12-31", CO),
    fx_fy23=I(-2_074, AFS23 + " — foreign exchange loss", "2023-12-31", CO),
    fx_fy24=I(-2_139, AFS24 + " — foreign exchange loss", "2024-12-31", CO),
    fx_fy25=I(-2_013, AFS25 + " — foreign exchange loss", "2025-12-31", CO),
    pbt_fy23=I(1_401_003, AFS23 + " — profit before tax", "2023-12-31", CO),
    pbt_fy24=I(1_745_309, AFS24 + " — profit before tax", "2024-12-31", CO),
    pbt_fy25=I(1_539_844, AFS25 + " — profit before tax", "2025-12-31", CO),
    tax_fy23=I(400_333, AFS23 + " — income tax expense (note 12a)", "2023-12-31", CO),
    tax_fy24=I(506_361, AFS24 + " — income tax expense (note 12a)", "2024-12-31", CO),
    tax_fy25=I(440_714, AFS25 + " — income tax expense (note 13a): current UAE 385,236, "
               "current foreign 11,360, deferred 44,118", "2025-12-31", CO),
    pat_fy23=I(1_000_670, AFS23 + " — profit for the year", "2023-12-31", CO),
    pat_fy24=I(1_238_948, AFS24 + " — profit for the year", "2024-12-31", CO),
    pat_fy25=I(1_099_130, AFS25 + " — profit for the year", "2025-12-31", CO),
    pat_owners_fy23=I(991_125, AFS23 + " — profit attributable to owners of the Company",
                      "2023-12-31", CO),
    pat_owners_fy24=I(1_225_273, AFS24 + " — profit attributable to owners",
                      "2024-12-31", CO),
    pat_owners_fy25=I(1_089_178, AFS25 + " — profit attributable to shareholders of the "
                      "Parent", "2025-12-31", CO),
    nci_fy25=I(9_952, AFS25 + " — profit attributable to non-controlling interests",
               "2025-12-31", CO),
    tax_applicable_rate_fy25=I(0.3824, AFS25 + ", note 13(b) reconciliation of effective "
                               "tax rate: the applicable rate on accounting profit, which "
                               "the Group states as 38.24% for 2025 against 29.66% for "
                               "2024", "2025-12-31", CO),

    # ======================= BALANCE SHEET, USD'000 =========================
    ppe_fy23=I(6_677_355, AFS24 + " — property, plant and equipment, comparative column",
               "2023-12-31", CO),
    ppe_fy24=I(6_292_502, AFS24 + " — property, plant and equipment", "2024-12-31", CO),
    ppe_fy25=I(6_082_232, AFS25 + " — property, plant and equipment (note 6)",
               "2025-12-31", CO),
    intang_fy23=I(60_126, AFS24 + " — intangible assets, comparative", "2023-12-31", CO),
    intang_fy24=I(60_643, AFS24 + " — intangible assets", "2024-12-31", CO),
    intang_fy25=I(104_573, AFS25 + " — intangible assets (note 7)", "2025-12-31", CO),
    rou_fy24=I(24_797, AFS24 + " — right-of-use assets", "2024-12-31", CO),
    rou_fy25=I(23_327, AFS25 + " — right-of-use assets (note 8a)", "2025-12-31", CO),
    sublease_nc_fy25=I(135_697, AFS25 + " — investment in sublease, non-current",
                       "2025-12-31", CO),
    sublease_c_fy25=I(5_952, AFS25 + " — investments in sublease, current",
                      "2025-12-31", CO),
    loans_emp_nc_fy25=I(21_905, AFS25 + " — loans to employees, non-current",
                        "2025-12-31", CO),
    loans_emp_c_fy25=I(13_245, AFS25 + " — loans to employees, current", "2025-12-31", CO),
    dta_fy25=I(1_992, AFS25 + " — deferred tax assets (note 13c)", "2025-12-31", CO),
    inv_fy23=I(645_184, AFS24 + " — inventories, comparative", "2023-12-31", CO),
    inv_fy24=I(640_505, AFS24 + " — inventories", "2024-12-31", CO),
    inv_fy25=I(523_702, AFS25 + " — inventories (note 9)", "2025-12-31", CO),
    ar_fy23=I(796_682, AFS24 + " — trade receivables, comparative", "2023-12-31", CO),
    ar_fy24=I(858_768, AFS24 + " — trade receivables", "2024-12-31", CO),
    ar_fy25=I(808_237, AFS25 + " — trade receivables (note 10a)", "2025-12-31", CO),
    duefrom_fy23=I(181_549, AFS24 + " — amounts due from related parties, comparative",
                   "2023-12-31", CO),
    duefrom_fy24=I(209_937, AFS24 + " — amounts due from related parties",
                   "2024-12-31", CO),
    duefrom_fy25=I(293_251, AFS25 + " — amounts due from related parties (note 12d)",
                   "2025-12-31", CO),
    prepaid_fy25=I(48_090, AFS25 + " — prepayments and other receivables (note 10b)",
                   "2025-12-31", CO),
    cash_fy23=I(353_921, AFS24 + " — cash and cash equivalents, comparative",
                "2023-12-31", CO),
    cash_fy24=I(418_506, AFS24 + " — cash and cash equivalents", "2024-12-31", CO),
    cash_fy25=I(426_901, AFS25 + " — cash and cash equivalents (note 11)",
                "2025-12-31", CO),
    ta_fy23=I(8_943_896, AFS24 + " — total assets, comparative", "2023-12-31", CO),
    ta_fy24=I(8_707_465, AFS24 + " — total assets", "2024-12-31", CO),
    ta_fy25=I(8_489_104, AFS25 + " — total assets", "2025-12-31", CO),
    eq_owners_fy23=I(4_532_482, AFS24 + " — equity attributable to owners, comparative",
                     "2023-12-31", CO),
    eq_owners_fy24=I(4_462_726, AFS24 + " — equity attributable to owners of the Company",
                     "2024-12-31", CO),
    eq_owners_fy25=I(4_088_850, AFS25 + " — equity attributable to the owners of the "
                     "Company", "2025-12-31", CO),
    nci_bs_fy25=I(26_832, AFS25 + " — non-controlling interests", "2025-12-31", CO),
    eq_total_fy25=I(4_115_682, AFS25 + " — total equity", "2025-12-31", CO),
    ap_fy23=I(308_333, AFS24 + " — trade and other payables, comparative",
              "2023-12-31", CO),
    ap_fy24=I(356_660, AFS24 + " — trade and other payables", "2024-12-31", CO),
    ap_fy25=I(378_200, AFS25 + " — trade and other payables (note 18): trade accounts "
              "payable 79,430, accrued expenses 248,325, contract liabilities 20,568, "
              "other payables 29,877", "2025-12-31", CO),
    ap_trade_only_fy25=I(79_430, AFS25 + " — note 18, trade accounts payable component "
                         "only", "2025-12-31", CO),
    dueto_fy23=I(567_034, AFS24 + " — amounts due to related parties, comparative: "
                 "current 532,645 plus non-current 34,389", "2023-12-31", CO),
    dueto_fy24=I(520_260, AFS24 + " — amounts due to related parties, current",
                 "2024-12-31", CO),
    dueto_fy25=I(576_502, AFS25 + " — amounts due to related parties (note 12c)",
                 "2025-12-31", CO),
    debt_fy23=I(3_140_725, AFS24 + " — bank loans, non-current, comparative",
                "2023-12-31", CO),
    debt_fy24=I(2_944_100, AFS24 + " — bank loans, non-current", "2024-12-31", CO),
    debt_fy25=I(2_957_730, AFS25 + " — bank loans (note 17), reclassified to current "
                "liabilities because the 5-year facility dated 19 December 2021 matures "
                "within twelve months of the reporting date", "2025-12-31", CO),
    debt_gross_fy25=I(2_960_680, AFS25 + " — note 17 before unamortised transaction costs "
                      "of 2,950: commercial term facility 2,600,000, Islamic facility "
                      "350,000, receivables discounting 10,680", "2025-12-31", CO),
    lease_nc_fy25=I(156_652, AFS25 + " — lease liabilities, non-current (note 8c)",
                    "2025-12-31", CO),
    lease_c_fy25=I(9_528, AFS25 + " — lease liabilities, current (note 8c)",
                   "2025-12-31", CO),
    dtl_fy25=I(128_972, AFS25 + " — deferred tax liability (note 13c)", "2025-12-31", CO),
    eosb_nc_fy25=I(93_044, AFS25 + " — provision for employees' end of service benefits, "
                   "non-current (note 16)", "2025-12-31", CO),
    eosb_c_fy25=I(12_293, AFS25 + " — provision for employees' end of service benefits, "
                  "current (note 16)", "2025-12-31", CO),
    taxpay_fy25=I(54_499, AFS25 + " — income tax payable", "2025-12-31", CO),
    tl_fy25=I(4_373_422, AFS25 + " — total liabilities", "2025-12-31", CO),

    # ======================= CASH FLOW, USD'000 =============================
    dep_ppe_fy23=I(539_612, AFS24 + " — depreciation on property, plant and equipment, "
                   "cash flow statement comparative", "2023-12-31", CO),
    dep_ppe_fy24=I(524_116, AFS24 + " — depreciation on property, plant and equipment",
                   "2024-12-31", CO),
    dep_ppe_fy25=I(449_384, AFS25 + " — depreciation on property, plant and equipment "
                   "(note 6)", "2025-12-31", CO),
    dep_rou_fy23=I(4_376, AFS24 + " — depreciation on right-of-use assets, comparative",
                   "2023-12-31", CO),
    dep_rou_fy24=I(4_786, AFS24 + " — depreciation on right-of-use assets",
                   "2024-12-31", CO),
    dep_rou_fy25=I(3_609, AFS25 + " — depreciation on right-of-use assets (note 8a)",
                   "2025-12-31", CO),
    amort_fy23=I(28_181, AFS24 + " — amortisation of intangible assets, comparative",
                 "2023-12-31", CO),
    amort_fy24=I(23_748, AFS24 + " — amortisation of intangible assets", "2024-12-31", CO),
    amort_fy25=I(23_321, AFS25 + " — amortisation of intangible assets (note 7)",
                 "2025-12-31", CO),
    cfo_fy23=I(1_768_720, AFS24 + " — net cash generated from operating activities, "
               "comparative", "2023-12-31", CO),
    cfo_fy24=I(1_913_152, AFS24 + " — net cash generated from operating activities",
               "2024-12-31", CO),
    cfo_fy25=I(1_920_976, AFS25 + " — net cash generated from operating activities",
               "2025-12-31", CO),
    capex_ppe_fy23=I(191_504, AFS24 + " — payments for purchase of property, plant and "
                     "equipment, comparative", "2023-12-31", CO),
    capex_ppe_fy24=I(160_124, AFS24 + " — payments for purchase of property, plant and "
                     "equipment", "2024-12-31", CO),
    capex_ppe_fy25=I(275_687, AFS25 + " — payments for purchase of property, plant and "
                     "equipment (note 6)", "2025-12-31", CO),
    capex_intang_fy25=I(32_546, AFS25 + " — payments for purchase of intangible assets",
                        "2025-12-31", CO),
    capex_intang_fy24=I(7_259, AFS24 + " — payments for purchase of intangible assets",
                        "2024-12-31", CO),
    capex_intang_fy23=I(7_276, AFS24 + " — payments for purchase of intangible assets, "
                        "comparative", "2023-12-31", CO),
    div_paid_fy23=I(1_317_242, AFS24 + " — payment of dividends, comparative",
                    "2023-12-31", CO),
    div_paid_fy24=I(1_307_024, AFS24 + " — payment of dividends", "2024-12-31", CO),
    div_paid_fy25=I(1_312_080, AFS25 + " — payment of dividends (note 12b)",
                    "2025-12-31", CO),
    taxpaid_fy25=I(389_595, AFS25 + " — tax paid", "2025-12-31", CO),
    intpaid_fy25=I(161_769, AFS25 + " — payment of interest on bank loan",
                   "2025-12-31", CO),

    # ======================= H1 2026 INTERIM, USD'000 =======================
    rev_h126=I(2_581_161, H126 + " — revenue for the six-month period", "2026-06-30", CO),
    rev_q126=I(1_175_190, MDA26 + " — Q1 2026 revenue of USD 1,175 million; the interim "
               "statements report the six-month figure and the three-month figure, and "
               "Q1 is the difference (2,581,161 less 1,405,971)", "2026-03-31", CO),
    rev_q226=I(1_405_971, H126 + " — revenue for the three-month period ended 30 June "
               "2026", "2026-06-30", CO),
    cogs_h126=I(1_631_518, H126 + " — cost of sales, six months", "2026-06-30", CO),
    ga_h126=I(96_053, H126 + " — general and administrative expenses, six months",
              "2026-06-30", CO),
    sd_h126=I(346_738, H126 + " — selling and distribution expenses, six months",
              "2026-06-30", CO),
    othinc_h126=I(37_190, H126 + " — other income, six months, including approximately "
                  "USD 25 million pre-tax of insurance claim proceeds relating to the "
                  "regional geopolitical disruption", "2026-06-30", CO),
    imp_h126=I(6_436, H126 + " — impairment loss on property, plant and equipment, in "
               "respect of assets damaged in the 5 April 2026 incident", "2026-06-30", CO),
    ebit_h126=I(537_606, H126 + " — operating profit, six months", "2026-06-30", CO),
    pbt_h126=I(462_680, H126 + " — profit before tax, six months", "2026-06-30", CO),
    tax_h126=I(116_119, H126 + " — income tax expense, six months (note 15)",
               "2026-06-30", CO),
    pat_h126=I(346_561, H126 + " — profit for the six-month period", "2026-06-30", CO),
    ta_h126=I(8_595_755, H126 + " — total assets", "2026-06-30", CO),
    eq_total_h126=I(3_748_031, H126 + " — total equity", "2026-06-30", CO),
    eq_owners_h126=I(3_725_997, H126 + " — equity attributable to owners of the Company",
                     "2026-06-30", CO),
    debt_rp_nc_h126=I(2_800_000, H126 + ", note 11(iv) — related party loans and "
                      "borrowings, non-current: Term Facility 1 of USD 1,500 million and "
                      "Term Facility 2 of USD 1,300 million, both with Borouge Group "
                      "International AG", "2026-06-30", CO),
    debt_rp_c_h126=I(50_000, H126 + ", note 11(iv)(b) — revolving credit facility with "
                     "Borouge Group International AG, drawn", "2026-06-30", CO),
    debt_ext_h126=I(399_998, H126 + ", note 10(ii) — limited recourse receivables "
                    "discounting agreement with an external commercial bank, of a USD 400 "
                    "million facility", "2026-06-30", CO),
    netdebt_h126=I(3_275_000, MDA26 + " — net debt of USD 3,275 million as at 30 June "
                   "2026, against USD 2,694 million at 30 June 2025", "2026-06-30", CO),
    netdebt_fy25=I(2_696_000, MDA25 + " — net debt of USD 2,696 million", "2025-12-31", CO),
    lease_add_xlpe2=I(56_500, H126 + " — right-of-use asset and corresponding lease "
                      "liability of approximately USD 56.5 million recognised on the "
                      "commencement of commercial operations at the XLPE 2 plant",
                      "2026-06-30", CO),

    # ======================= PHYSICAL UNIT BUILD ============================
    # Nameplate capacity. Fixed: Borouge 4 is NOT owned by Borouge plc.
    cap_pe_fy25=I(2_750, MDA25 + " — polyethylene production capacity, FY2025, kt",
                  "2025-12-31", CO),
    cap_pp_fy25=I(2_230, MDA25 + " — polypropylene production capacity, FY2025, kt",
                  "2025-12-31", CO),
    cap_nameplate=I(5_000, MDA26 + " — footnote to the management guidance table: "
                    "'Ruwais plant nameplate capacity: 5 mtpa'", "2026-06-30", CO),

    # Sales volumes, kt
    vol_pe_fy23=I(2_715, MDA24 + " — polyethylene sales volumes, FY2023 comparative, kt",
                  "2023-12-31", CO),
    vol_pp_fy23=I(2_285, MDA24 + " — polypropylene sales volumes, FY2023 comparative, kt",
                  "2023-12-31", CO),
    vol_oth_fy23=I(116, MDA24 + " — ethylene and others sales volumes, FY2023, kt",
                   "2023-12-31", CO),
    vol_pe_fy24=I(3_072, MDA25 + " — polyethylene sales volumes, FY2024 comparative, kt",
                  "2024-12-31", CO),
    vol_pp_fy24=I(2_253, MDA25 + " — polypropylene sales volumes, FY2024 comparative, kt",
                  "2024-12-31", CO),
    vol_oth_fy24=I(10, MDA25 + " — ethylene and others sales volumes, FY2024, kt",
                   "2024-12-31", CO),
    vol_pe_fy25=I(3_053, MDA25 + " — polyethylene sales volumes, FY2025, kt",
                  "2025-12-31", CO),
    vol_pp_fy25=I(2_322, MDA25 + " — polypropylene sales volumes, FY2025, kt",
                  "2025-12-31", CO),
    vol_oth_fy25=I(13, MDA25 + " — ethylene and others sales volumes, FY2025, kt",
                   "2025-12-31", CO),
    vol_pe_h126=I(1_048, MDA26 + " — polyethylene sales volumes, H1 2026, kt",
                  "2026-06-30", CO),
    vol_pp_h126=I(910, MDA26 + " — polypropylene sales volumes, H1 2026, kt",
                  "2026-06-30", CO),

    # Production volumes and utilisation
    prod_pe_fy25=I(2_817, MDA25 + " — polyethylene production volume, FY2025, kt",
                   "2025-12-31", CO),
    prod_pp_fy25=I(2_225, MDA25 + " — polypropylene production volume, FY2025, kt",
                   "2025-12-31", CO),
    util_pe_fy25=I(1.02, MDA25 + " — polyethylene utilisation rate, FY2025, stated as "
                   "102% including the impact of the Borouge 3 turnaround in Q2 2025",
                   "2025-12-31", CO),
    util_pp_fy25=I(1.00, MDA25 + " — polypropylene utilisation rate, FY2025, 100%",
                   "2025-12-31", CO),
    util_pe_fy24=I(1.10, MDA25 + " — polyethylene utilisation rate, FY2024, 110%",
                   "2024-12-31", CO),
    util_pp_fy24=I(0.98, MDA25 + " — polypropylene utilisation rate, FY2024, 98%",
                   "2024-12-31", CO),
    util_pe_h126=I(0.73, MDA26 + " — polyethylene utilisation rate, H1 2026, 73%, after "
                   "the 5 April incident and the Strait of Hormuz closure",
                   "2026-06-30", CO),
    util_pp_h126=I(0.84, MDA26 + " — polypropylene utilisation rate, H1 2026, 84%",
                   "2026-06-30", CO),
    prod_h126=I(1_929, MDA26 + " — total production, H1 2026, kt, against 2,201 kt in "
                "H1 2025", "2026-06-30", CO),

    # Realised prices, benchmarks and premia, USD/t.
    # Benchmark = HDPE Blow Molding NEA CFR for PE, Raffia NEA CFR for PP, per CMA,
    # as the company itself defines them in every MDA footnote.
    bench_pe_fy23=I(914, MDA24 + " — polyethylene average benchmark, FY2023, USD/t",
                    "2023-12-31", CO),
    bench_pp_fy23=I(891, MDA24 + " — polypropylene average benchmark, FY2023, USD/t",
                    "2023-12-31", CO),
    bench_pe_fy24=I(898, MDA25 + " — polyethylene average benchmark, FY2024, USD/t",
                    "2024-12-31", CO),
    bench_pp_fy24=I(897, MDA25 + " — polypropylene average benchmark, FY2024, USD/t",
                    "2024-12-31", CO),
    bench_pe_fy25=I(822, MDA25 + " — polyethylene average benchmark, FY2025, USD/t",
                    "2025-12-31", CO),
    bench_pp_fy25=I(851, MDA25 + " — polypropylene average benchmark, FY2025, USD/t",
                    "2025-12-31", CO),
    bench_pe_h126=I(970, MDA26 + " — polyethylene average benchmark, H1 2026, USD/t",
                    "2026-06-30", CO),
    bench_pp_h126=I(1_018, MDA26 + " — polypropylene average benchmark, H1 2026, USD/t",
                    "2026-06-30", CO),
    bench_pe_q226=I(1_144, MDA26 + " — polyethylene average benchmark, Q2 2026, USD/t, "
                    "up 38% year on year during the Strait of Hormuz closure",
                    "2026-06-30", CO),
    bench_pp_q226=I(1_202, MDA26 + " — polypropylene average benchmark, Q2 2026, USD/t",
                    "2026-06-30", CO),
    prem_pe_fy23=I(215, MDA24 + " — polyethylene premia, FY2023, USD/t", "2023-12-31", CO),
    prem_pp_fy23=I(125, MDA24 + " — polypropylene premia, FY2023, USD/t", "2023-12-31", CO),
    prem_pe_fy24=I(197, MDA25 + " — polyethylene premia, FY2024, USD/t", "2024-12-31", CO),
    prem_pp_fy24=I(150, MDA25 + " — polypropylene premia, FY2024, USD/t", "2024-12-31", CO),
    prem_pe_fy25=I(224, MDA25 + " — polyethylene premia, FY2025, USD/t", "2025-12-31", CO),
    prem_pp_fy25=I(134, MDA25 + " — polypropylene premia, FY2025, USD/t", "2025-12-31", CO),
    prem_pe_h126=I(300, MDA26 + " — polyethylene premia, H1 2026, USD/t", "2026-06-30", CO),
    prem_pp_h126=I(187, MDA26 + " — polypropylene premia, H1 2026, USD/t", "2026-06-30", CO),
    prem_pe_ttc=I(200, MDA26 + " — management through-the-cycle premia guidance for "
                  "polyethylene, reiterated at Q2 2026, c. USD 200/t", "2026-06-30", CO),
    prem_pp_ttc=I(140, MDA26 + " — management through-the-cycle premia guidance for "
                  "polypropylene, reiterated at Q2 2026, c. USD 140/t", "2026-06-30", CO),
    asp_pe_fy25=I(1_046, MDA25 + " — polyethylene average sales price, FY2025, USD/t",
                  "2025-12-31", CO),
    asp_pp_fy25=I(985, MDA25 + " — polypropylene average sales price, FY2025, USD/t",
                  "2025-12-31", CO),
    rev_pe_fy25=I(3_436, MDA25 + " — polyethylene revenue, FY2025, USD million",
                  "2025-12-31", CO),
    rev_pp_fy25=I(2_368, MDA25 + " — polypropylene revenue, FY2025, USD million",
                  "2025-12-31", CO),
    rev_oth_fy25=I(44, MDA25 + " — ethylene and others revenue, FY2025, USD million",
                   "2025-12-31", CO),

    # ======================= COST STACK, USD million ========================
    # One line per physical driver class. The escalation rule attaches a different
    # escalator to each of these, never one blended index across all of them.
    feed_fy23=I(1_357, MDA23 + " — feedstock costs, FY2023, USD million",
                "2023-12-31", CO),
    feed_fy24=I(1_288, MDA25 + " — feedstock costs, FY2024 comparative, USD million",
                "2024-12-31", CO),
    feed_fy25=I(1_295, MDA25 + " — feedstock costs, FY2025, USD million",
                "2025-12-31", CO),
    feed_h126=I(761, MDA26 + " — feedstock costs, H1 2026, USD million, up 33% year on "
                "year on higher purchased propylene prices after the Olefins Conversion "
                "Unit was idled", "2026-06-30", CO),
    othprod_fy23=I(1_704, MDA23 + " — other variable and fixed production costs, FY2023, "
                   "USD million", "2023-12-31", CO),
    othprod_fy24=I(1_659, MDA25 + " — other variable and fixed production costs, FY2024 "
                   "comparative, USD million", "2024-12-31", CO),
    othprod_fy25=I(1_804, MDA25 + " — other variable and fixed production costs, FY2025, "
                   "USD million", "2025-12-31", CO),
    othprod_h126=I(676, MDA26 + " — other variable and fixed production costs, H1 2026, "
                   "USD million", "2026-06-30", CO),
    cos_exda_fy23=I(3_062, MDA23 + " — cost of sales excluding depreciation and "
                    "amortisation, FY2023, USD million", "2023-12-31", CO),
    cos_exda_fy24=I(2_947, MDA25 + " — cost of sales excluding D&A, FY2024 comparative, "
                    "USD million", "2024-12-31", CO),
    cos_exda_fy25=I(3_099, MDA25 + " — cost of sales excluding D&A, FY2025, USD million",
                    "2025-12-31", CO),
    ga_exda_fy25=I(188, MDA25 + " — general and administrative expenses excluding D&A, "
                   "FY2025, USD million", "2025-12-31", CO),
    sd_exda_h126=I(347, MDA26 + " — selling and distribution expenses, H1 2026, USD "
                   "million, up 81% year on year on higher freight and logistics costs "
                   "while alternative routes are in use", "2026-06-30", CO),
    ebitda_adj_fy23=I(2_171, MDA24 + " — adjusted EBITDA, FY2023, USD million",
                      "2023-12-31", CO),
    ebitda_adj_fy24=I(2_477, MDA25 + " — adjusted EBITDA, FY2024, USD million",
                      "2024-12-31", CO),
    ebitda_adj_fy25=I(2_172, MDA25 + " — adjusted EBITDA, FY2025, USD million",
                      "2025-12-31", CO),
    ebitda_adj_h126=I(744, MDA26 + " — adjusted EBITDA, H1 2026, USD million, down 26% "
                      "year on year", "2026-06-30", CO),
    capex_h126=I(163, MDA26 + " — capital expenditure, H1 2026, USD million",
                 "2026-06-30", CO),
    dep_reassessment_benefit=I(163, MDA25 + " — the Q3 2025 reassessment of the useful "
                               "life of certain fixed assets, which extended asset life "
                               "by up to an additional 10 years and is expected to "
                               "result in a recurring annual benefit of USD 163 million "
                               "in lower depreciation charges over the next 5 financial "
                               "years compared with 2024 levels", "2025-12-31", CO),

    # ======================= GUIDANCE AND STRUCTURE =========================
    div_fils_guided=I(0.162, MDA26 + " — 'For FY 2026, management intends to pay "
                      "dividends amounting to 16.2 fils per share, in line with the "
                      "Company's commitment to maintain a minimum dividend of 16.2 fils "
                      "per share per annum until at least 2030'; 16.2 fils is AED 0.162",
                      "2026-06-30", CO),
    capex_guide_2026=I(300, MDA26 + " — 'The repairs are expected to have only a limited "
                       "impact on 2026 maintenance capex, which is guided to be below "
                       "USD 300 million'", "2026-06-30", CO),
    util_guide_2026=I(1.05, MDA25 + " — 'management expects to achieve average "
                      "utilisation of around 105% for FY 2026', guidance given before "
                      "the 5 April 2026 incident and the Strait of Hormuz closure and "
                      "superseded by the Q2 2026 statement that management is targeting "
                      "higher utilisation in H2 2026 subject to feedstock and logistics "
                      "availability and freedom of navigation", "2025-12-31", CO),
    b4_ownership=I(0.0, H126 + " and " + MDA26 + " — 'Under the Asset Usage Agreement "
                   "signed in March 2026, Borouge operates the Borouge 4 assets on "
                   "behalf of the project's owners, ADNOC and OMV, and will market all "
                   "Borouge 4 production volumes in return for an at-cost asset "
                   "utilisation fee.' Borouge plc therefore owns none of the Borouge 4 "
                   "capacity and earns no production margin on it", "2026-06-30", CO),
    kd_margin_t1=I(0.00725, H126 + ", note 11(iv)(a) — Term Facility 1, USD 1,500 "
                   "million, 3 years from inception, reference agreement signed 9 April "
                   "2026, interest at SOFR + 0.725% plus an annualised participation fee "
                   "of 0.08% of loan value", "2026-04-09", CO),
    kd_margin_t2=I(0.00875, H126 + ", note 11(iv)(a) — Term Facility 2, USD 1,300 "
                   "million, 5 years from inception, agreement signed 9 April 2026, "
                   "interest at SOFR + 0.875% plus an annualised participation fee of "
                   "0.078%", "2026-04-09", CO),
    kd_fee_t1=I(0.0008, H126 + ", note 11(iv)(a) — annualised participation fee on Term "
                "Facility 1", "2026-04-09", CO),
    kd_fee_t2=I(0.00078, H126 + ", note 11(iv)(a) — annualised participation fee on Term "
                "Facility 2", "2026-04-09", CO),
    kd_margin_old=I(0.0090, AFS25 + ", note 17 — the superseded external commercial term "
                    "facility carried SOFR + 0.90%; it was arranged with a consortium of "
                    "banks on 19 December 2021 and was repaid in full on 9 April 2026, "
                    "so it is the last ARM'S-LENGTH price Borouge paid for term debt",
                    "2021-12-19", CO),
    debt_currency=I("USD", AFS25 + " note 17 and " + H126 + " notes 10 and 11(iv) — every "
                    "borrowing in the book, before and after the April 2026 refinancing, "
                    "is denominated in US dollars, which is also the Group's presentation "
                    "and functional currency. There is no foreign-currency tranche to "
                    "carry at a local-equivalent cost", "2026-06-30", CO),
)
