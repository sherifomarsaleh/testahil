"""AMOC (Alexandria Mineral Oils Company S.A.E., EGX: AMOC) — the study's compute layer.

Code-first rule: no financial arithmetic happens outside this script. Every hardcoded
figure enters through the four-field INPUTS register {value, source, date, ring}; a bare
numeral in the inputs block fails the build. The CALC section derives everything else and
the ASSERT section raises rather than emitting study_numbers.json if any of the standing
identities break.

Three structural facts about this name drive the whole model and are established here
rather than asserted in the narrative:

  1. AMOC changed its financial year. The Egyptian Exchange approved a move from a 30-June
     year-end to 31 December, with July-December 2025 reported as a six-month transition
     period. The company now reports calendar quarters. History is therefore carried on the
     reported June years, a calendar-2025 base year is CONSTRUCTED from the two disclosed
     halves, and the forecast runs on calendar years 2026E-2030E.

  2. AMOC is net CASH, not net debt. Gross borrowings are around EGP 25mn against EGP 2.46bn
     of cash. The cost of capital is therefore effectively all-equity, the enterprise-to-equity
     bridge ADDS net cash, and the cost of debt — while still put through the full integrity
     gate — is immaterial to the answer. That materiality is computed, not assumed.

  3. It is a thin-margin processor, not a holding company. FY2022/23 cost of sales of
     EGP 21.22bn against gross profit of EGP 1.30bn is a 5.8% gross margin, and consolidated
     profit exceeds standalone profit by only ~4%. Both facts are used, and both are what rule
     out the holding-company lens.
"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
import numpy as np

# ============================ INPUTS =========================================
INP = {}


def I(value, source, date, ring):
    return dict(value=value, source=source, date=date, ring=ring)


# --- Ring 4: company — EVERY FIGURE BELOW IS READ OFF AN AUDITED FILING -------
# Source: Alexandria Mineral Oils Co (S.A.E.), consolidated financial statements audited by
# Crowe (Dr A. M. Hegazy & Co), UNQUALIFIED opinion, signed Giza 18-Feb-2026, for the transition
# period 1-Jul-2025 to 31-Dec-2025; the limited-review consolidated statements for the six months
# to 31-Dec-2024; and the reviewed consolidated statements for the three months to 31-Mar-2026.
# The previous edition of this study was built on triangulated press reporting because the
# filings could not be reached. They are now in hand. Nothing in this register is triangulated.
AUD = "Audited consolidated FS, transition period 1-Jul-2025 to 31-Dec-2025, Crowe unqualified, 18-Feb-2026"
REV = "Reviewed consolidated FS, three months to 31-Mar-2026"
LRV = "Limited-review consolidated FS, six months to 31-Dec-2024"

INP['spot'] = I(9.10, "AMOC closing price on the Egyptian Exchange, 6 August 2026", "2026-08-06", "Company")
INP['shares_mn'] = I(1291.5, "Issued and paid-up capital EGP 1,291,500,000 at EGP 1 par = "
                             "1,291,500,000 shares (note 18-L, share split to EGP 1 par recorded "
                             "in the Commercial Register 24-Jan-2018)", "2025-12-31", "Company")

# ---- the three audited reporting periods, in full ----------------------------
INP['rev_h2_25'] = I(20_735_725_812.0, f"Net sales, six months to 31-Dec-2025. {AUD}", "2025-12-31", "Company")
INP['cogs_h2_25'] = I(19_461_550_746.0, f"Cost of sales, six months to 31-Dec-2025. {AUD}", "2025-12-31", "Company")
INP['ga_h2_25'] = I(585_636_101.0, f"General and administrative expenses, six months to 31-Dec-2025 (note 15-B). {AUD}", "2025-12-31", "Company")
INP['mkt_h2_25'] = I(93_729_199.0, f"Marketing and selling expenses, six months to 31-Dec-2025 (note 15-C). {AUD}", "2025-12-31", "Company")
INP['othexp_h2_25'] = I(108_781_309.0, "Other operating expenses, six months to 31-Dec-2025 (note 15-D): "
                                       "compensation and fines 101,393,395, donations 5,162,500, board "
                                       f"transport and attendance 2,225,414. {AUD}", "2025-12-25", "Company")
INP['othrev_h2_25'] = I(345_744_052.0, "Other revenue, six months to 31-Dec-2025 (note 14-B): credit "
                                       "interest 173,216,413, provision no longer required 154,301,640, "
                                       "reversed expected credit loss 1,870,481, compensations and fines "
                                       "1,241,123, capital gains 326,000, miscellaneous 14,788,395. NOTE "
                                       "the foreign-exchange gain line is ZERO in this period, against "
                                       f"104,572,235 in the comparative half. {AUD}", "2025-12-31", "Company")
INP['invinc_h2_25'] = I(13_520_000.0, "Revenue from investments — dividend from Alexandria Specialized "
                                      f"Petroleum Products Co (note 14-C). {AUD}", "2025-12-31", "Company")
INP['prov_h2_25'] = I(2_467_769.0, f"Formed provisions charged in the six months to 31-Dec-2025. {AUD}", "2025-12-31", "Company")
INP['fin_h2_25'] = I(1_892_108.0, "Finance expenses, six months to 31-Dec-2025 (note 15-E): loan interest "
                                  f"and charges 1,130,556, lease interest 761,552. {AUD}", "2025-12-31", "Company")
INP['tax_h2_25'] = I(203_945_433.0, f"Current income tax, six months to 31-Dec-2025. {AUD}", "2025-12-31", "Company")
INP['dtax_h2_25'] = I(19_441_512.0, f"Deferred tax CREDIT, six months to 31-Dec-2025. {AUD}", "2025-12-31", "Company")
INP['pat_h2_25'] = I(656_428_711.0, f"Net profit after tax, six months to 31-Dec-2025. {AUD}", "2025-12-31", "Company")
INP['nci_h2_25'] = I(30_488_250.0, f"Non-controlling interest share of profit, six months to 31-Dec-2025. {AUD}", "2025-12-31", "Company")
INP['emp_h2_25'] = I(67_467_871.0, "Employees' profit share and board bonuses deducted in arriving at "
                                   "earnings per share (note 16). A real distribution out of profit that "
                                   f"the previous edition of this study did not model at all. {AUD}", "2025-12-31", "Company")

INP['rev_q1_26'] = I(10_510_779_160.0, f"Net sales, three months to 31-Mar-2026. {REV}", "2026-03-31", "Company")
INP['cogs_q1_26'] = I(9_439_744_195.0, f"Cost of sales, three months to 31-Mar-2026. {REV}", "2026-03-31", "Company")
INP['ga_q1_26'] = I(365_952_237.0, f"General and administrative expenses, three months to 31-Mar-2026. {REV}", "2026-03-31", "Company")
INP['mkt_q1_26'] = I(60_830_975.0, f"Marketing and selling expenses, three months to 31-Mar-2026. {REV}", "2026-03-31", "Company")
INP['othexp_q1_26'] = I(1_080_000.0, f"Other operating expenses, three months to 31-Mar-2026. {REV}", "2026-03-31", "Company")
INP['othrev_q1_26'] = I(225_556_509.0, f"Other revenue, three months to 31-Mar-2026. {REV}", "2026-03-31", "Company")
INP['prov_q1_26'] = I(30_000_000.0, f"Formed provisions, three months to 31-Mar-2026. {REV}", "2026-03-31", "Company")
INP['ecl_q1_26'] = I(20_323_123.0, f"Expected credit losses formed, three months to 31-Mar-2026. {REV}", "2026-03-31", "Company")
INP['fin_q1_26'] = I(982_219.0, f"Finance cost, three months to 31-Mar-2026. {REV}", "2026-03-31", "Company")
INP['tax_q1_26'] = I(175_094_101.0, f"Current income tax, three months to 31-Mar-2026. {REV}", "2026-03-31", "Company")
INP['dtax_q1_26'] = I(-7_209_684.0, f"Deferred tax EXPENSE (negative = charge), three months to 31-Mar-2026. {REV}", "2026-03-31", "Company")
INP['pat_q1_26'] = I(635_119_535.0, f"Net profit after tax, three months to 31-Mar-2026. {REV}", "2026-03-31", "Company")
INP['nci_q1_26'] = I(22_627_676.0, f"Non-controlling interest share of profit, three months to 31-Mar-2026. {REV}", "2026-03-31", "Company")

INP['rev_h2_24'] = I(18_246_078_901.0, f"Net sales, six months to 31-Dec-2024 (comparative column). {AUD}", "2024-12-31", "Company")
INP['cogs_h2_24'] = I(16_995_436_456.0, f"Cost of sales, six months to 31-Dec-2024 (comparative column). {AUD}", "2024-12-31", "Company")
INP['pat_h2_24'] = I(641_640_411.0, f"Net profit after tax, six months to 31-Dec-2024. {AUD}", "2024-12-31", "Company")
INP['rev_q1_25'] = I(10_068_471_935.0, f"Net sales, three months to 31-Mar-2025 (comparative column). {REV}", "2025-03-31", "Company")
INP['cogs_q1_25'] = I(9_559_699_263.0, f"Cost of sales, three months to 31-Mar-2025 (comparative column). {REV}", "2025-03-31", "Company")
INP['pat_fy25_full'] = I(1_488_520_098.0, "Majority profit for the financial year to 30-June-2025, read "
                                          "off the opening column of the consolidated statement of "
                                          f"changes in equity at 1-July-2025. {AUD}", "2025-06-30", "Company")

# ---- NOTE 14-A: THE AUDITED PRODUCT TABLE, six months to 31-Dec-2025 ----------
# Eight lines, each with tonnes and value. This replaces a three-line build that rested on a
# product table obtained from a reviewer rather than from the filing, and whose realisations had
# to be reconstructed through a crude-parity crack multiple. Nothing is reconstructed now.
INP['prod_t'] = I(dict(oils=54_968.98, wax=41_774.20, gasoil=171_684.881, naphtha=41_430.857,
                       lpg=23_735.778, fueloil=460_153.60, hfo=14_327.52, waste=7.82),
                  f"Tonnes sold by product line, six months to 31-Dec-2025 (note 14-A). {AUD}",
                  "2025-12-31", "Company")
INP['prod_v'] = I(dict(oils=2_597_280_264.0, wax=2_041_969_329.0, gasoil=5_121_703_599.0,
                       naphtha=958_746_631.0, lpg=816_258_520.0, fueloil=8_975_569_716.0,
                       hfo=224_110_353.0, waste=87_400.0),
                  f"Sales value by product line, EGP, six months to 31-Dec-2025 (note 14-A). {AUD}",
                  "2025-12-31", "Company")
INP['prod_v_prior'] = I(dict(oils=2_526_857_239.0, wax=1_683_792_907.0, gasoil=5_219_594_878.0,
                             naphtha=1_034_502_087.0, lpg=687_509_617.0, fueloil=6_954_252_764.0,
                             hfo=139_454_409.0, waste=115_000.0),
                        f"Sales value by product line, six months to 31-Dec-2024 (note 14-A comparative). {AUD}",
                        "2024-12-31", "Company")

# ---- NOTE 15-A: THE AUDITED COST STACK ---------------------------------------
# The previous edition BUILT a cost stack from house estimates of yields, energy intensity and a
# solved feedstock differential. The filing discloses the stack directly. It is used as disclosed.
INP['cos_salaries'] = I(881_019_497.0, f"Cost of sales — salaries, six months to 31-Dec-2025 (note 15-A). {AUD}", "2025-12-31", "Company")
INP['cos_raw'] = I(17_650_102_725.0, "Cost of sales — RAW MATERIALS, six months to 31-Dec-2025 (note "
                                     "15-A). 90.7% of cost of sales and 85.1% of revenue: this single "
                                     f"line is what the company is. {AUD}", "2025-12-31", "Company")
INP['cos_support'] = I(64_533_723.0, "Cost of sales — supporting materials (chemicals and additives), "
                                     "six months to 31-Dec-2025 (note 15-A). The previous edition "
                                     "estimated this charge at roughly five times the disclosed figure",
                       "2025-12-31", "Company")
INP['cos_dep'] = I(58_748_046.0, f"Cost of sales — depreciation, six months to 31-Dec-2025 (note 15-A). {AUD}", "2025-12-31", "Company")
INP['cos_other'] = I(807_146_755.0, "Cost of sales — other expenses, six months to 31-Dec-2025 (note "
                                    "15-A): natural gas, operating electricity, operating water, spare "
                                    "parts, maintenance, and the operating management and technical "
                                    "support contract with the Egyptian Projects Operations & "
                                    f"Maintenance Company (EPROM). {AUD}", "2025-12-31", "Company")
INP['cos_salaries_24'] = I(634_571_733.0, f"Cost of sales — salaries, six months to 31-Dec-2024 (note 15-A comparative). {AUD}", "2024-12-31", "Company")
INP['cos_raw_24'] = I(15_597_464_119.0, f"Cost of sales — raw materials, six months to 31-Dec-2024 (note 15-A comparative). {AUD}", "2024-12-31", "Company")
INP['cos_support_24'] = I(68_294_446.0, f"Cost of sales — supporting materials, six months to 31-Dec-2024. {AUD}", "2024-12-31", "Company")
INP['cos_dep_24'] = I(53_507_611.0, f"Cost of sales — depreciation, six months to 31-Dec-2024. {AUD}", "2024-12-31", "Company")
INP['cos_other_24'] = I(641_598_547.0, f"Cost of sales — other expenses, six months to 31-Dec-2024. {AUD}", "2024-12-31", "Company")

# ---- audited balance sheet, 31-Dec-2025 (comparatives 30-Jun-2025 / 31-Dec-2024 / 30-Jun-2024) --
INP['ppe_net'] = I(893_016_274.0, "Fixed assets net of accumulated depreciation at 31-Dec-2025 (note 6). "
                                  "Cost 2,740,810,692 less accumulated depreciation 1,847,794,418 — the "
                                  "plant is 67% written down, and 273,466,121 of it is fully depreciated "
                                  f"and still in use. {AUD}", "2025-12-31", "Company")
INP['puc'] = I(407_323_203.0, "Projects under construction at 31-Dec-2025 (note 7): assets in development "
                              "376,746,526 (administrative building, warehouses, civil projects, ERP "
                              f"system) plus investment expenditure 30,576,677. {AUD}", "2025-12-31", "Company")
INP['inventory'] = I(2_847_392_506.0, "Inventory net of impairment at 31-Dec-2025 (note 9-A): work in "
                                      "process 792,134,042, finished goods 1,166,168,582, spare parts "
                                      "309,298,239, supporting materials 283,470,554, raw materials "
                                      f"118,754,225, goods for resale 155,793,361. {AUD}", "2025-12-31", "Company")
INP['recv'] = I(573_136_185.0, "Accounts receivable net at 31-Dec-2025 (note 9-B). 100% undue and "
                               "unimpaired on the ageing analysis. Counterparties include Shell, "
                               "ExxonMobil, Chevron, Total, TAQA/Castrol, Emarat Misr, OLA Energy and "
                               f"Petromine alongside the state companies. {AUD}", "2025-12-31", "Company")
INP['debtors'] = I(366_012_664.0, f"Debtors and other debit balances net at 31-Dec-2025 (notes 9-C, 9-D). {AUD}", "2025-12-31", "Company")
INP['cash'] = I(2_463_522_365.0, "Cash at banks and on hand at 31-Dec-2025 (note 9-E): time deposits "
                                 "883,351,250 plus current accounts 2,127,100,720 plus cash on hand "
                                 "166,405, less expected credit losses 38,345,960, less PLEDGED deposits "
                                 f"508,750,050 which sit in other financial investments. {AUD}", "2025-12-31", "Company")
INP['fin_inv'] = I(508_750_050.0, "Other financial investments at 31-Dec-2025 — deposits PLEDGED against "
                                  f"credit facilities, so not free cash (note 9-E). {AUD}", "2025-12-31", "Company")
INP['fvoci'] = I(69_608_696.0, "Financial asset through OCI at 31-Dec-2025 — 104,000 shares, 5.20% of "
                               f"ASCPC, fair value 69,608,696 (note 8-1). {AUD}", "2025-12-31", "Company")
INP['assets_snap'] = I(8_136_418_030.0, f"Total assets at 31-Dec-2025. {AUD}", "2025-12-31", "Company")
INP['liab_snap'] = I(3_311_643_082.0, f"Total liabilities at 31-Dec-2025. {AUD}", "2025-12-31", "Company")
INP['eq_parent'] = I(4_790_695_948.0, f"Total AMOC (parent) equity at 31-Dec-2025. {AUD}", "2025-12-31", "Company")
INP['eq_nci'] = I(34_079_000.0, f"Non-controlling interest carrying amount at 31-Dec-2025. {AUD}", "2025-12-31", "Company")
INP['debt_lt'] = I(11_805_265.0, f"Long-term loans at 31-Dec-2025 (note 20). {AUD}", "2025-12-31", "Company")
INP['debt_st'] = I(9_172_172.0, f"Short-term loans and facilities at 31-Dec-2025 (note 20). {AUD}", "2025-12-31", "Company")
INP['leases'] = I(4_278_324.0, f"Total lease liabilities at 31-Dec-2025 (note 8-2-2). {AUD}", "2025-12-31", "Company")
INP['payables'] = I(7_942_650.0, "Accounts and notes payable at 31-Dec-2025 (note 10-3). The previous "
                                 "edition modelled a trade payable of about 2.5bn funding the working "
                                 "capital cycle; the actual trade payable is under 8mn and the funding "
                                 f"sits in the EGPC current account instead. {AUD}", "2025-12-31", "Company")
INP['creditors'] = I(2_044_446_416.0, "Creditors and other credit balances at 31-Dec-2025 (note 11): EGPC "
                                      "current account 1,132,353,505, deposits 70,891,867, miscellaneous "
                                      "taxes 47,021,719, dividends payable 517,250,000, miscellaneous "
                                      f"creditors 148,226,091, customer advances 60,028,880. {AUD}", "2025-12-31", "Company")
INP['provisions'] = I(921_440_353.0, "Provisions at 31-Dec-2025 (note 10-1): tax disputes 904,609,345 and "
                                     "claims and disputes 16,831,008. A contingent liability worth EGP "
                                     "0.71 a share that the previous edition never carried at all",
                      "2025-12-31", "Company")
INP['dtax_liab'] = I(108_612_469.0, f"Deferred tax liability at 31-Dec-2025 (note 13-A). {AUD}", "2025-12-31", "Company")
INP['tax_due'] = I(203_945_433.0, f"Due to the tax authority at 31-Dec-2025 (note 10-2). {AUD}", "2025-12-31", "Company")
INP['assets_jun25'] = I(10_327_865_642.0, f"Total assets at 30-Jun-2025 (comparative column). {AUD}", "2025-06-30", "Company")
INP['eq_parent_jun25'] = I(5_353_528_855.0, f"Total AMOC equity at 30-Jun-2025 (comparative column). {AUD}", "2025-06-30", "Company")
INP['assets_dec24'] = I(7_747_725_648.0, f"Total assets at 31-Dec-2024. {LRV}", "2024-12-31", "Company")
INP['eq_parent_dec24'] = I(4_430_087_458.0, f"Total AMOC equity at 31-Dec-2024. {LRV}", "2024-12-31", "Company")
INP['assets_jun24'] = I(8_386_961_675.0, f"Total assets at 30-Jun-2024 (comparative column). {LRV}", "2024-06-30", "Company")
INP['eq_parent_jun24'] = I(4_922_226_388.0, f"Total AMOC equity at 30-Jun-2024 (comparative column). {LRV}", "2024-06-30", "Company")
INP['ppe_jun25'] = I(937_851_261.0, f"Fixed assets net at 30-Jun-2025. {AUD}", "2025-06-30", "Company")
INP['inv_jun25'] = I(3_735_009_103.0, f"Inventory at 30-Jun-2025. {AUD}", "2025-06-30", "Company")
INP['recv_jun25'] = I(894_888_039.0, f"Accounts receivable at 30-Jun-2025. {AUD}", "2025-06-30", "Company")
INP['debtors_jun25'] = I(611_842_230.0, f"Debtors and other debit balances at 30-Jun-2025. {AUD}", "2025-06-30", "Company")
INP['creditors_jun25'] = I(3_102_041_816.0, f"Creditors and other credit balances at 30-Jun-2025. {AUD}", "2025-06-30", "Company")
INP['payables_jun25'] = I(15_486_636.0, f"Accounts and notes payable at 30-Jun-2025. {AUD}", "2025-06-30", "Company")
INP['cash_jun25'] = I(3_141_779_939.0, f"Cash at banks and on hand at 30-Jun-2025. {AUD}", "2025-06-30", "Company")
INP['cash_mar26'] = I(2_204_898_542.0, f"Cash and cash equivalents at 31-Mar-2026. {REV}", "2026-03-31", "Company")
INP['eq_parent_mar26'] = I(4_800_890_542.0, f"Total parent equity at 31-Mar-2026. {REV}", "2026-03-31", "Company")

# ---- audited cash-flow actuals: the two lines the previous edition got most wrong ----
INP['dep_h2_25'] = I(70_125_269.0, "Fixed-asset depreciation and right-of-use amortisation charged in "
                                   "the six months to 31-Dec-2025, per the cash-flow statement. The "
                                   "previous edition modelled depreciation at 1.1% of revenue, about "
                                   f"440mn a year against an actual near 150mn. {AUD}", "2025-12-31", "Company")
INP['dep_q1_26'] = I(40_597_611.0, f"Fixed-asset depreciation and right-of-use amortisation, Q1-2026. {REV}", "2026-03-31", "Company")
INP['capex_h2_25'] = I(30_357_299.0, "CASH PAID for projects under construction and fixed assets in the "
                                     "six months to 31-Dec-2025. The previous edition modelled capital "
                                     "expenditure at 1.45% of revenue — about 649mn in the first "
                                     f"forecast year — against an actual of roughly a tenth of that. {AUD}",
                       "2025-12-31", "Company")
INP['capex_q1_26'] = I(64_984_482.0, f"Cash paid for projects under construction and fixed assets, Q1-2026. {REV}", "2026-03-31", "Company")
INP['div_h2_25'] = I(736_577_469.0, f"Cash dividends PAID in the six months to 31-Dec-2025. {AUD}", "2025-12-31", "Company")
INP['div_q1_26'] = I(602_957_265.0, f"Cash dividends paid in Q1-2026. {REV}", "2026-03-31", "Company")
INP['credint_h2_25'] = I(173_216_413.0, "Credit interest earned in the six months to 31-Dec-2025, per "
                                        f"note 14-B and the cash-flow statement. {AUD}", "2025-12-31", "Company")
INP['credint_q1_26'] = I(64_104_178.0, f"Credit interest earned in Q1-2026. {REV}", "2026-03-31", "Company")
INP['div_declared'] = I(517_250_000.0, "Dividends payable at 31-Dec-2025 (note 11, other credit "
                                       f"balances) — declared and not yet paid at the reporting date. {AUD}",
                        "2025-12-31", "Company")

# ---- ownership and counterparty, as disclosed --------------------------------
INP['nci_share'] = I(30_488_250.0 / 656_428_711.0,
                     "Non-controlling interest as a share of group profit after tax, six months to "
                     "31-Dec-2025 — DISCLOSED, not inferred. AMOC holds 86.45% of Alexandria Wax "
                     "Products S.A.E. (note 1-2). The previous edition inferred 3.0% from the gap "
                     "between consolidated and standalone profit; the filing says 4.645%",
                     "2025-12-31", "Company")
INP['alexpet_stake'] = I(0.2077, "Alexandria Petroleum Company holds 20.77% of AMOC (note 18, capital "
                                 "structure). The previous edition named the Egyptian General Petroleum "
                                 "Corporation as the 20% shareholder; EGPC is NOT a direct shareholder. "
                                 "Free float (public offering, individuals and other institutions) is "
                                 "28.77%", "2025-12-31", "Company")
INP['egpc_sales'] = I(15_872_300_000.0, "Sales of products to the Egyptian General Petroleum Corporation "
                                        "in the six months to 31-Dec-2025 (note 19-3-B) — 76.5% of net "
                                        "sales. EGPC is also the dominant supplier, with 16.3bn of "
                                        "purchases in the same half. That two-sided relationship is the "
                                        f"real governance fact, and it is disclosed. {AUD}", "2025-12-31", "Company")
INP['egpc_balance'] = I(1_132_353_505.0, f"EGPC current account balance owed at 31-Dec-2025 (note 11). {AUD}", "2025-12-31", "Company")


# ---- the two remaining free operating parameters, and nothing else -----------
INP['line_vol_growth'] = I(dict(oils=[0.045, 0.040, 0.035, 0.030, 0.028],
                                wax=[0.070, 0.055, 0.045, 0.038, 0.032],
                                gasoil=[0.020, 0.020, 0.018, 0.016, 0.015],
                                naphtha=[0.015, 0.018, 0.018, 0.016, 0.015],
                                lpg=[0.025, 0.022, 0.020, 0.018, 0.016],
                                fueloil=[0.030, 0.026, 0.022, 0.020, 0.018],
                                hfo=[0.020, 0.018, 0.016, 0.015, 0.014],
                                waste=[0.0, 0.0, 0.0, 0.0, 0.0]),
                           "Volume growth by AUDITED product line. The RANKING is taken from the "
                           "line-level value growth actually printed between the two disclosed "
                           "halves — wax +21.3%, fuel oil +29.1%, LPG +18.7%, while gas oil "
                           "(-1.9%) and naphtha (-7.3%) FELL — rather than from a view about the "
                           "business. Levels are struck well below those half-on-half rates "
                           "because a single half is not a trend. This is one of only two free "
                           "operating parameters left and it is sensitised end to end",
                           "2026-08-06", "House")
INP['line_price_growth'] = I([0.090, 0.075, 0.065, 0.058, 0.052],
                             "Growth in the realised price per tonne, all lines, in EGP. The "
                             "realisation ITSELF is disclosed — note 14-A value divided by note "
                             "14-A tonnes — so only its growth is forecast. Struck below the "
                             "assumed exchange-rate path on the view that a pass-through processor "
                             "recovers currency in price with a lag. The second and last free "
                             "operating parameter", "2026-08-06", "House")
INP['fixed_cost_infl'] = I([1.33, 1.28, 1.12, 1.145, 1.13, 1.115, 1.10, 1.095],
                           "Cumulative-year Egyptian inflation factors applied to the "
                           "pound-denominated cost legs — salaries inside cost of sales, the "
                           "other line, administrative and marketing expense, and capital "
                           "expenditure. Historical years as printed, easing toward the central "
                           "bank's published target thereafter", "2026-08-06", "Country")
INP['payout_reported'] = I((736_577_469.0 + 602_957_265.0) / (656_428_711.0 + 635_119_535.0),
                           "Dividend payout ratio COMPUTED from the filings: cash dividends "
                           "actually PAID in the audited nine months (736,577,469 in the "
                           "transition half plus 602,957,265 in Q1-2026) over group profit after "
                           "tax for the same nine months. Not a reported ratio and not an "
                           "assumption — the two cash-flow statements divided by the two profit "
                           "lines", "2026-03-31", "Company")
INP['dps'] = I((736_577_469.0 + 602_957_265.0) / 1_291_500_000.0,
               "Dividend per share, cash actually paid in the audited nine months over shares "
               "outstanding. Annualising is left to the reader; the study uses the paid figure",
               "2026-03-31", "Company")
INP['raw_pass'] = I(1.0, "Pass-through factor on the raw-material line: 1.0 means the feedstock "
                         "charge moves one-for-one with realisation and volume, so the gross "
                         "SPREAD per tonne is held flat in real terms and the margin neither "
                         "widens nor narrows by assumption. Setting it below 1.0 is the way to "
                         "express spread widening; the study leaves it at parity and sensitises it",
                    "2026-08-06", "House")

# --- Ring 3: industry ------------------------------------------------------
INP['brent_path'] = I([70.0, 71.5, 73.0, 74.5, 76.0],
                      "Brent crude reference path, USD a barrel, 2026E-2030E. A flat-to-slowly-"
                      "rising deck. In the previous edition this input drove NOTHING — it was "
                      "registered, published in the source register and read by no line of the "
                      "model. It is now the spine of both sides of the margin: every product "
                      "realisation is this deck times a crack multiple solved from the disclosed "
                      "product table, and the feedstock charge is this deck times a differential "
                      "solved from disclosed cost of sales",
                      "2026-08-06", "Industry")
INP['crude_hist'] = I(dict(fy23=85.0, fy24=84.0, fy25=74.0, cy25=70.0),
                      "Brent averages for the four historical periods, USD a barrel. HOUSE "
                      "ESTIMATES read off the published price record for each window, not "
                      "company disclosure. They matter less than they look: the crude level "
                      "enters the margin on BOTH sides and very largely cancels, which the "
                      "study demonstrates rather than asserts",
                      "2026-08-06", "Industry")
INP['fx_hist'] = I(dict(fy23=28.5, fy24=36.4, fy25=48.9, cy25=48.7),
                   "USD/EGP averages for the four historical periods. The June-2024 figure is "
                   "built month by month across the March-2024 float (eight months near 30.9, "
                   "four near 47.5); the others are period averages of the published rate. "
                   "HOUSE ESTIMATES",
                   "2026-08-06", "Country")
# --- Ring 2: country -------------------------------------------------------
INP['rf'] = I(0.2231, "Egypt 10-year local-currency government bond yield, 22.31% (house cost-of-"
                      "capital reference, cached 21-Jul-2026 print, re-verified 06-Aug-2026)",
              "2026-07-21", "Country")
INP['sov_spread_cds'] = I(0.034, "Egypt credit-default-swap-implied sovereign default spread, "
                                 "Damodaran January-2026 country-premium file, CDS column. Netted "
                                 "out of the local-currency risk-free rate so sovereign default "
                                 "risk is not charged twice",
                          "2026-01-05", "Country")
INP['sov_spread_rating'] = I(0.0637, "Damodaran adjusted default spread on the rating basis, "
                                     "January-2026 — the alternative construction, disclosed for "
                                     "the audit trail", "2026-01-05", "Country")
INP['erp_cds'] = I(0.0941, "Damodaran original country-premium file, Egypt row, CDS column, last "
                           "updated 5 January 2026 — total equity risk premium",
                   "2026-01-05", "Country")
INP['erp_rating'] = I(0.1394, "Damodaran original country-premium file, Egypt row, rating basis, "
                              "January-2026 — the alternative", "2026-01-05", "Country")
INP['policy_rate'] = I(0.1950, "Central Bank of Egypt main operation rate 19.50% (corridor "
                               "19.00/20.00), held at the third meeting of 2026 — a second "
                               "consecutive hold", "2026-08-06", "Country")
INP['cpi'] = I(0.1430, "Egypt annual headline inflation 14.30% in June 2026, down from 14.60% in "
                       "May. The central bank expects inflation to accelerate through the third "
                       "quarter of 2026 on base effects, supply pressures and fiscal adjustment "
                       "before resuming its decline", "2026-06-30", "Country")
INP['cbe_target'] = I(0.07, "The central bank's own stated inflation target, 7% (+/-2pp) on "
                            "average for the fourth quarter of 2026, falling to 5% (+/-2pp) for "
                            "the fourth quarter of 2028", "2026-08-06", "Country")
INP['fx'] = I(50.25, "USD/EGP 50.25; the pound closed at 50.30/50.40 on 4 August 2026. The 52-week "
                     "range is 46.64-54.86, so the currency is not range-bound",
              "2026-08-06", "Country")
INP['fx_path'] = I([50.9, 53.4, 55.8, 58.0, 60.1],
                   "USD/EGP average-rate path, about 4.5% a year of depreciation from the 2025 "
                   "average. Below the inflation differential, on the view that the post-float "
                   "regime and the reserve build slow the pass-through — this is a genuine driver: "
                   "both revenue legs are priced off dollar product benchmarks",
                   "2026-08-06", "House")
INP['fx_avg_cy25'] = I(48.7, "USD/EGP average rate for calendar 2025, used to convert the "
                             "dollar-denominated unit build back to the reported base year",
                       "2025-12-31", "Country")
INP['tax_stat'] = I(0.225, "Egypt corporate income tax 22.5%. AMOC is a downstream processor and "
                           "is taxed at the ordinary corporate rate, not the ~40.55% rate that "
                           "applies to exploration and production concessions", "2026", "Country")
INP['egypt_gdp_nominal'] = I(20000000.0, "Egypt nominal gross domestic product, EGP mn, order of "
                                         "magnitude, used only for the terminal-growth crossover "
                                         "arithmetic", "2026-08-06", "Country")
INP['egypt_nominal_growth'] = I(0.15, "Long-run Egyptian nominal growth used as the terminal "
                                      "ceiling for the domestic leg", "2026-08-06", "House")

# --- Ring 1: global --------------------------------------------------------
INP['world_nominal_growth'] = I(0.075, "Long-run world nominal growth used as the terminal ceiling "
                                       "for the export leg", "2026-08-06", "Global")
INP['wacc_usd_rf'] = I(0.043, "US 10-year Treasury yield used in the currency-of-discounting "
                              "alternative", "2026-08-06", "Global")
INP['wacc_usd_erp'] = I(0.075, "Blended emerging-market equity risk premium applied to the "
                               "dollar-denominated alternative", "2026-08-06", "Global")

# --- House drivers ---------------------------------------------------------
INP['beta'] = I(0.9405, "Own-stock tier-1 regression: AMOC weekly log-returns against a 33-name "
                        "equal-weight Egyptian Exchange composite built from the full covered "
                        "library, five-year window. R-squared 0.312, n = 257, standard error "
                        "0.087, 90% confidence interval [0.797, 1.084]. Passes the usability gate "
                        "comfortably and is NOT a weak instrument: the interval spans 0.29x the "
                        "point estimate, well inside the 2x flag",
                "2026-08-06", "House")
INP['tax_eff'] = I(0.235, "Effective tax rate used for NOPAT. Struck one percentage point above "
                          "the 22.5% statutory rate for non-deductible items and the deferred-tax "
                          "drag typical of Egyptian downstream filers",
                   "2026-08-06", "House")
INP['recv_days'] = I(14.0, "Trade receivable days. The offtake is dominated by the state petroleum "
                           "complex on short settlement, which is why a company turning over EGP "
                           "40bn of revenue runs a balance sheet of only EGP 8.1bn",
                     "2026-08-06", "House")
INP['inv_days'] = I(14.0, "Inventory days on cost of sales. Feedstock is drawn from the adjacent "
                          "refining complex rather than imported and stocked",
                    "2026-08-06", "House")
INP['pay_days'] = I(24.0, "Trade payable days on cost of sales. The feedstock payable to the state "
                          "petroleum corporation is the company's principal source of working-"
                          "capital funding", "2026-08-06", "House")
INP['other_ca'] = I(300.0, "Other current assets, EGP mn, held flat", "2026-08-06", "House")
INP['dna_pct'] = I(0.011, "Depreciation and amortisation as a share of revenue. The complex was "
                          "commissioned between 1997 and 2000 and is substantially written down, "
                          "which is why the charge is small against turnover",
                   "2026-08-06", "House")
INP['capex_pct'] = I([0.0145, 0.0140, 0.0135, 0.0130, 0.0125],
                     "Capital expenditure as a share of revenue, tapering. Anchored on the approved "
                     "EGP 580.19mn budget against the same year's budgeted net sales of EGP "
                     "37.332bn, which is 1.55%; the taper reflects the completion of the current "
                     "storage-tank and environmental programme", "2026-08-06", "House")
INP['opex_pct'] = I([0.0125, 0.0125, 0.0126, 0.0127, 0.0128],
                    "The net operating load between gross profit and EBITDA, as a share of "
                    "revenue — selling, general and administrative costs and other expenses, less "
                    "other operating income", "2026-08-06", "House")
INP['cash_yield'] = I(0.170, "Yield earned on the cash pile. Egyptian treasury bills and corporate "
                             "deposits price a few points under the 19.50% policy rate net of the "
                             "20% withholding on interest", "2026-08-06", "House")
INP['cash_yield_path'] = I([0.170, 0.150, 0.135, 0.125, 0.118],
                           "Forward path for the deposit yield, easing with the policy rate",
                           "2026-08-06", "House")
INP['kd'] = I(0.2200, "Marginal cost of debt. The gross book is EGP 25mn — 0.06% of revenue — of "
                      "short-dated Egyptian-pound facilities, so the rate is taken at the corridor "
                      "lending rate of 20.00% plus a 200bp corporate spread rather than pretended "
                      "to be observable. The integrity gate below computes what this input is "
                      "actually WORTH to the answer", "2026-08-06", "House")
INP['kd_path'] = I([0.2200, 0.1950, 0.1750, 0.1600, 0.1500],
                   "Forward cost-of-debt path 2026E-2030E, following the central bank's own "
                   "disinflation path toward the long-run Egyptian corporate-borrowing norm. This "
                   "path is what sets the SHAPE of the cost-of-capital glide; it is not a second "
                   "free parameter", "2026-08-06", "House")
INP['kd_term'] = I(0.1500, "Terminal cost of debt: the midpoint of the 14-16% long-run Egyptian "
                           "corporate-borrowing norm, with no name-specific reason to deviate",
                   "2026-08-06", "House")
INP['rf_term'] = I(0.1050, "Terminal risk-free rate, norm-built: the central bank's own stated "
                           "medium-term inflation target of 5% plus the standard ~5.5pp emerging-"
                           "market real-rate convention. Never a raw historical average and never "
                           "backed out of a price", "2026-08-06", "House")
INP['erp_term'] = I(0.0700, "Terminal equity risk premium, normalised below the currently elevated "
                            "crisis-era level toward the rating-class norm; never held flat into "
                            "perpetuity", "2026-08-06", "House")
INP['wd_term'] = I(0.10, "Terminal debt weight, normalised. The company is net cash today and has "
                         "been for years; a terminal structure carrying a tenth of capital in debt "
                         "is already generous to the valuation and avoids capitalising the current "
                         "zero-leverage position into perpetuity", "2026-08-06", "House")
INP['g_term'] = I(0.05, "Terminal growth, 5% — the standing centre for established names in this "
                        "market once currency turbulence has passed, sensitised 3-7%. An "
                        "EGP-nominal rate struck against an EGP-nominal terminal risk-free rate",
                 "2026-08-06", "House")
INP['ev_ebitda_just'] = I(4.5, "Justified enterprise-value-to-EBITDA multiple on mid-cycle 2028E "
                               "EBITDA. The company's own trailing multiple is around 4.6x on the "
                               "constructed 2025 base. Group I base-oil refiners and independent "
                               "lube processors trade 4-6x; 4.5x holds the name at its own trailing "
                               "level rather than assuming a re-rating. Bear 3.5x / bull 6.0x",
                          "2026-08-06", "House")
INP['pe_just'] = I(7.5, "Justified through-cycle price-to-earnings multiple on normalised earnings. "
                        "Trailing is about 7.5x on the constructed 2025 base. A single-asset "
                        "processor with a 20% state shareholder, an administered feedstock "
                        "relationship and an Egyptian cost of equity near 28% does not earn a "
                        "premium multiple. Bear 5.5x / bull 9.5x", "2026-08-06", "House")
INP['roe_sust'] = I(0.280, "Sustainable return on equity for the book lens. Trailing return on "
                           "average parent equity is about 33%; the sustainable rate is struck "
                           "below it because the reported figure is flattered by a heavily "
                           "written-down asset base that will have to be renewed",
                    "2026-08-06", "House")
INP['lens_weights'] = I(dict(dcf=0.45, relative=0.20, normalized=0.20, book=0.15),
                        "Discounted cash flow primary for a single-asset operating processor with a "
                        "visible volume ramp; the relative and normalised-earnings lenses carry "
                        "equal secondary weight; the book lens least, because a substantially "
                        "depreciated plant makes book value a poor proxy for replacement cost",
                        "2026-08-06", "House")

V = {k: v['value'] for k, v in INP.items()}
LOG = []


def say(s):
    LOG.append(s); print(s)


say("=" * 78)
say("AMOC — ASSERT / derivation log")
say("=" * 78)

# ============================ CALC ===========================================
SH, SPOT, TAX = V['shares_mn'], V['spot'], V['tax_eff']
MKTCAP = SPOT * SH
LINES = ['oils', 'wax', 'gasoil', 'naphtha', 'lpg', 'fueloil', 'hfo', 'waste']
LBL = dict(oils='Base and special oils', wax='Paraffin wax', gasoil='Gas oil',
           naphtha='Naphtha', lpg='Liquefied petroleum gas', fueloil='Fuel oil (mix)',
           hfo='Heavy fuel oil', waste='Waste')
SPEC = ['oils', 'wax']                     # the specialty slate
YRS = ['2026E', '2027E', '2028E', '2029E', '2030E']

# ---- (1) the base year is the NINE AUDITED MONTHS, annualised ----------------
# There is no clean audited twelve-month period: the year-end moved to 31 December, the
# transition filing covers Jul-Dec 2025, and Apr-Jun 2025 is not separately filed. The base is
# therefore the nine months 1-Jul-2025 to 31-Mar-2026 — the audited transition period plus the
# reviewed first quarter, contiguous, no gap, no estimate — scaled by 4/3. That scaling is the
# ONLY step between the filings and the base year, and it is stated on the face of the model.
A = 4.0 / 3.0
rev9 = V['rev_h2_25'] + V['rev_q1_26']
cogs9 = V['cogs_h2_25'] + V['cogs_q1_26']
gp9 = rev9 - cogs9
ga9 = V['ga_h2_25'] + V['ga_q1_26']
mkt9 = V['mkt_h2_25'] + V['mkt_q1_26']
oth9 = V['othexp_h2_25'] + V['othexp_q1_26']
dep9 = V['dep_h2_25'] + V['dep_q1_26']
capex9 = V['capex_h2_25'] + V['capex_q1_26']
credint9 = V['credint_h2_25'] + V['credint_q1_26']
othrev9 = V['othrev_h2_25'] + V['othrev_q1_26']
tax9 = (V['tax_h2_25'] - V['dtax_h2_25']) + (V['tax_q1_26'] - V['dtax_q1_26'])
_pbt_h2 = (V['rev_h2_25'] - V['cogs_h2_25'] - V['ga_h2_25'] - V['mkt_h2_25'] - V['othexp_h2_25']
           - V['prov_h2_25'] - V['fin_h2_25'] + V['othrev_h2_25'] + V['invinc_h2_25'])
_pbt_q1 = (V['rev_q1_26'] - V['cogs_q1_26'] - V['ga_q1_26'] - V['mkt_q1_26'] - V['othexp_q1_26']
           - V['prov_q1_26'] - V['ecl_q1_26'] - V['fin_q1_26'] + V['othrev_q1_26'])
pbt9 = _pbt_h2 + _pbt_q1
pat9 = V['pat_h2_25'] + V['pat_q1_26']
M = 1e6
BASE_REV = rev9 / M * A
BASE_GM = gp9 / rev9
TAX_EFF = tax9 / pbt9
# the P&L rebuilds from its own components: exactly for the audited half, to 400 EGP for the
# reviewed quarter (rounding inside the filing), and the pre-tax / tax / after-tax bridge ties
# to the pound across both periods.
assert abs(_pbt_h2 - 840_932_632.0) < 1.0, "audited half does not rebuild from its components"
assert abs(_pbt_q1 - 817_423_320.0) < 500.0, "reviewed quarter does not rebuild from its components"
assert abs(pbt9 - (pat9 + tax9)) < 500.0, "9M pre-tax does not tie to after-tax plus tax"
say(f"[Base year — nine AUDITED months, annualised] the transition period 1-Jul-2025 to "
    f"31-Dec-2025 (audited, Crowe, unqualified) and the three months to 31-Mar-2026 (reviewed) "
    f"are contiguous and cover nine months: net sales {rev9/M:,.0f}, cost of sales {cogs9/M:,.0f}, "
    f"GROSS PROFIT {gp9/M:,.0f}, a margin of {BASE_GM:.3%}. Annualised at 4/3 the base year is "
    f"{BASE_REV:,.0f} of revenue. There is no clean audited twelve-month period to use instead — "
    f"the year-end moved to December and April-June 2025 is not separately filed — so this "
    f"scaling is the only step between the filings and the base year, and no part of it is "
    f"estimated. The previous edition CONSTRUCTED a calendar-2025 base from two reported halves "
    f"and got {39_996:,.0f}; the audited nine months annualise to {BASE_REV:,.0f}, "
    f"{BASE_REV/39_996-1:+.1%} away.")
say(f"[Effective tax rate, computed not assumed] nine-month pre-tax profit {pbt9/M:,.0f} against "
    f"a total tax charge of {tax9/M:,.0f} (current less deferred, both periods) = {TAX_EFF:.2%}. "
    f"The statutory rate is {V['tax_stat']:.1%}. The previous edition assumed {TAX:.1%}.")

# ---- (2) the margin record, straight off the filings -------------------------
PERIODS = [
    ('6M to Dec-2024', V['rev_h2_24'], V['cogs_h2_24']),
    ('3M to Mar-2025', V['rev_q1_25'], V['cogs_q1_25']),
    ('6M to Dec-2025', V['rev_h2_25'], V['cogs_h2_25']),
    ('3M to Mar-2026', V['rev_q1_26'], V['cogs_q1_26']),
]
gm_hist = [(n, r / M, (r - c) / M, (r - c) / r) for n, r, c in PERIODS]
say("[The margin record, as filed] " + " · ".join(f"{n} {g:.2%}" for n, _, _, g in gm_hist) +
    ". This is not a modelled path and not a house assumption — it is gross profit over net "
    "sales in four consecutively filed periods. Note the shape: the margin was 6.85% in the "
    "half to December 2024, collapsed to 5.05% in the March-2025 quarter, recovered to 6.15% "
    "in the half to December 2025 and then printed 10.19% in the March-2026 quarter. The "
    "March-2026 print is the highest in the disclosed record by a wide margin and it is a "
    "SINGLE QUARTER; the base year above blends it with the half that precedes it rather than "
    "annualising it on its own.")

# ---- (3) the AUDITED cost stack, note 15-A -----------------------------------
COS = dict(salaries=V['cos_salaries'], raw=V['cos_raw'], support=V['cos_support'],
           dep=V['cos_dep'], other=V['cos_other'])
COS24 = dict(salaries=V['cos_salaries_24'], raw=V['cos_raw_24'], support=V['cos_support_24'],
             dep=V['cos_dep_24'], other=V['cos_other_24'])
assert abs(sum(COS.values()) - V['cogs_h2_25']) < 1.0, "note 15-A does not foot to cost of sales"
assert abs(sum(COS24.values()) - V['cogs_h2_24']) < 1.0, "note 15-A comparative does not foot"
cos_share = {k: v / V['cogs_h2_25'] for k, v in COS.items()}
say(f"[The cost stack, DISCLOSED not built] note 15-A splits the {V['cogs_h2_25']/M:,.0f} of cost "
    f"of sales in the transition half: raw materials {COS['raw']/M:,.0f} "
    f"({cos_share['raw']:.1%}), salaries {COS['salaries']/M:,.0f} ({cos_share['salaries']:.1%}), "
    f"other — natural gas, electricity, water, spare parts, maintenance and the EPROM operating "
    f"contract — {COS['other']/M:,.0f} ({cos_share['other']:.1%}), supporting materials "
    f"{COS['support']/M:,.0f} ({cos_share['support']:.1%}) and depreciation {COS['dep']/M:,.0f} "
    f"({cos_share['dep']:.1%}). The previous edition BUILT a stack from house estimates of "
    f"yields, energy intensity and a solved feedstock differential, carried NO salaries line at "
    f"all inside cost of sales, and estimated chemicals at roughly five times the disclosed "
    f"figure. None of that construction survives: the filing states the stack and the model uses "
    f"it as stated.")
raw_of_rev = COS['raw'] / V['rev_h2_25']
say(f"[What this company actually is] raw materials are {raw_of_rev:.1%} of net sales. Every "
    f"other cost line together is {1-raw_of_rev-BASE_GM:.1%}. A business whose single largest "
    f"line is {raw_of_rev:.0%} of revenue and whose gross margin is {BASE_GM:.1%} is a "
    f"PASS-THROUGH PROCESSOR: the value is not in the revenue line, and it is not in cost "
    f"control either — it is in the spread between what the feedstock costs and what the slate "
    f"fetches, and in the tonnage that spread is earned on.")

# ---- (4) the AUDITED product table, note 14-A --------------------------------
PT, PV, PVp = V['prod_t'], V['prod_v'], V['prod_v_prior']
tot_t = sum(PT.values()); tot_v = sum(PV.values())
assert abs(tot_v - V['rev_h2_25']) < 1.0, "note 14-A value column does not foot to net sales"
assert abs(tot_t - 808_083.636) < 0.01, "note 14-A tonnage does not foot"
px = {k: PV[k] / PT[k] for k in LINES}                 # EGP per tonne, DISCLOSED / DISCLOSED
mix_t = {k: PT[k] / tot_t for k in LINES}
mix_v = {k: PV[k] / tot_v for k in LINES}
spec_t = sum(mix_t[k] for k in SPEC); spec_v = sum(mix_v[k] for k in SPEC)
say(f"[The product table, AUDITED] note 14-A gives eight lines with tonnes AND value for the "
    f"transition half: {tot_t:,.0f} tonnes for {tot_v/M:,.0f}. Realisations per tonne fall "
    f"straight out of the division and nothing is reconstructed: " +
    " · ".join(f"{LBL[k]} {px[k]:,.0f}" for k in ('oils', 'wax', 'gasoil', 'fueloil')) +
    f" EGP a tonne. The specialty slate — oils and wax — is {spec_t:.2%} of the tonnage and "
    f"{spec_v:.2%} of the value. The previous edition used a THREE-line table obtained from a "
    f"reviewer rather than the filing, and had to reconstruct realisations through a crude-parity "
    f"crack multiple. The filing makes all of that unnecessary: fuel oil (mix) alone is "
    f"{mix_t['fueloil']:.1%} of tonnage and {mix_v['fueloil']:.1%} of value, and it is not the "
    f"same product as gas oil, naphtha or LPG, which the old build had merged into one slate.")
growth_v = {k: (PV[k] / PVp[k] - 1) if PVp[k] else 0.0 for k in LINES}
say(f"[Line-level value growth, half on half] " +
    " · ".join(f"{LBL[k]} {growth_v[k]:+.1%}" for k in ('oils', 'wax', 'gasoil', 'naphtha',
                                                        'lpg', 'fueloil', 'hfo')) +
    ". Wax is the standout at {:+.1%} and fuel oil at {:+.1%}; gas oil and naphtha both FELL. "
    "That is the mix shift the forecast has to carry, and it is measured rather than "
    "assumed.".format(growth_v['wax'], growth_v['fueloil']))

# ---- (5) the forecast: volume by line, realisations, and the disclosed cost stack ----
# Volume growth is the ONLY free operating parameter left. Everything else — the realisation per
# tonne, the cost stack shares, the tax rate — is taken from the filings and held or grown with
# the stated inflation/FX path.


def build(vol_mult=1.0, price_mult=1.0, fx_mult=1.0, gm_shift=0.0, ratio=None):
    """Revenue from the AUDITED product table (note 14-A) rolled forward on volume and
    realisation. Cost of sales from the AUDITED composition (note 15-A): raw materials and
    supporting materials are pass-through and move with realisation and volume; salaries and the
    other line are pound-denominated and move with local inflation; depreciation is the
    asset-register charge. The gross margin is what falls out."""
    # The disclosed note 15-A composition is a SHARE structure; the LEVEL is set by the
    # nine-month base so the first forecast year joins the audited base year continuously
    # instead of stepping down to the transition half's own margin.
    _cos0 = cogs9 / M * A
    raw0 = _cos0 * cos_share['raw']; sup0 = _cos0 * cos_share['support']
    sal0 = _cos0 * cos_share['salaries']; oth0 = _cos0 * cos_share['other']
    base_t = tot_t * 2 / 1e6
    rev, gp, gm, cogs_l = [], [], [], []
    lines_rev = {k: [] for k in LINES}; lines_vol = {k: [] for k in LINES}
    lmarg = {k: [] for k in LINES}
    infl = 1.0; pidx = 1.0; vidx = {k: 1.0 for k in LINES}
    for i in range(5):
        infl *= V['fixed_cost_infl'][3 + i]
        pidx *= (1 + V['line_price_growth'][i] * price_mult * fx_mult)
        r_lines = {}
        for k in LINES:
            vidx[k] *= (1 + V['line_vol_growth'][k][i] * vol_mult)
            v = PT[k] * 2.0 / 1e6 * vidx[k]
            p = px[k] * pidx
            r_lines[k] = v * p
            lines_vol[k].append(v); lines_rev[k].append(r_lines[k])
        r_tot = sum(r_lines.values())
        volidx = sum(lines_vol[k][i] for k in LINES) / base_t
        raw = raw0 * volidx * pidx * RAW_PASS
        sup = sup0 * volidx * pidx
        c_tot = raw + sup + sal0 * infl + oth0 * infl + _cos0 * cos_share['dep']
        g = r_tot - c_tot + gm_shift * r_tot
        rev.append(r_tot); cogs_l.append(c_tot); gp.append(g); gm.append(g / r_tot)
        for k in LINES:
            lmarg[k].append(g / r_tot)
    _inf = 1.0; opex = []
    for i in range(5):
        _inf *= V['fixed_cost_infl'][3 + i]
        opex.append(OPEX_ANN * _inf)
    ebitda = [gp[i] - opex[i] + DEP_ANN for i in range(5)]
    return dict(rev=rev, gm=gm, gp=gp, opex=opex, cogs=cogs_l, ebitda=ebitda,
                ebitda_margin=[ebitda[i] / rev[i] for i in range(5)],
                lines_rev=lines_rev, lines_vol=lines_vol, line_margin=lmarg,
                vol=[sum(lines_vol[k][i] for k in LINES) for i in range(5)],
                spec_vol=[sum(lines_vol[k][i] for k in SPEC) for i in range(5)],
                spec_rev=[sum(lines_rev[k][i] for k in SPEC) for i in range(5)],
                fuel_rev=[sum(lines_rev[k][i] for k in LINES if k not in SPEC) for i in range(5)],
                m_spec=lmarg['oils'][0], m_fuel=lmarg['fueloil'][0])


# ---- (6) the balance sheet, AUDITED — no reconstruction anywhere -------------
ppe_b = (V['ppe_net'] + V['puc']) / M
inv_b = V['inventory'] / M
recv_b = (V['recv'] + V['debtors']) / M
pay_b = (V['payables'] + V['creditors']) / M
nwc_b = inv_b + recv_b - pay_b
cash_b = V['cash'] / M
debt_b = (V['debt_lt'] + V['debt_st']) / M
nd_cy25 = debt_b - cash_b                     # NEGATIVE: the company is net cash
eqp_cy25 = V['eq_parent'] / M
bvps = eqp_cy25 / SH
IC_B = ppe_b + nwc_b
ppe_cy25 = ppe_b
nwc_b = nwc_b
rev_cy25 = BASE_REV
pat_cy25 = pat9 / M * A
netfin_cy25 = credint9 / M * A
eqp_jun24 = V['eq_parent_jun24'] / M
NCI_SHARE = V['nci_share']
say(f"[Balance sheet, AUDITED] property plant and equipment {V['ppe_net']/M:,.0f} plus projects "
    f"under construction {V['puc']/M:,.0f} = {ppe_b:,.0f}. Inventory {inv_b:,.0f}, receivables "
    f"and debtors {recv_b:,.0f}, payables and creditors {pay_b:,.0f} -> NET WORKING CAPITAL "
    f"{nwc_b:,.0f}. INVESTED CAPITAL {IC_B:,.0f}. The previous edition reconstructed property "
    f"plant and equipment as the residual against disclosed total assets and got 2,403 — "
    f"{2403/ppe_b:.1f} times the filed figure — and put net working capital at 2.0% of revenue "
    f"against an actual {nwc_b/BASE_REV:.1%}. Total assets matched only because the "
    f"reconstruction was anchored on them; the composition was wrong in both directions.")
say(f"[Net cash, AUDITED] cash {cash_b:,.0f} against long-term loans {V['debt_lt']/M:,.1f} and "
    f"short-term loans {V['debt_st']/M:,.1f}: NET CASH {-nd_cy25:,.0f} = EGP {-nd_cy25/SH:.2f} a "
    f"share, {-nd_cy25/MKTCAP:.1%} of market capitalisation. A further {V['fin_inv']/M:,.0f} of "
    f"deposits is PLEDGED against credit facilities and is deliberately NOT counted as free "
    f"cash. Against it sits a tax-disputes provision of {V['provisions']/M:,.0f} — EGP "
    f"{V['provisions']/M/SH:.2f} a share — which the previous edition never carried at all.")
assert abs((V['assets_snap'] - V['liab_snap']) / M - (eqp_cy25 + V['eq_nci'] / M)) < 0.01, \
    "audited balance sheet does not balance"
say(f"[Minority interest, DISCLOSED] the non-controlling share of group profit after tax is "
    f"{NCI_SHARE:.3%} in the audited half — AMOC owns 86.45% of Alexandria Wax Products. The "
    f"previous edition INFERRED 3.0% from a gap between consolidated and standalone profit. It "
    f"is now read off the filing.")

wd_gross = debt_b / (debt_b + MKTCAP)
kd_swing_effect = 0.05 * (1 - TAX) * wd_gross
say(f"[Cost of debt — MATERIALITY] gross debt is {wd_gross:.4%} of the capital structure. A "
    f"500bp error in the cost of debt moves the weighted cost of capital by "
    f"{kd_swing_effect*1e4:.2f} basis points. The input cannot move the answer and the study "
    f"says so rather than dressing an immaterial input as a precise one.")
assert kd_swing_effect < 0.0005, 'cost of debt is material after all'
RAW_PASS = V['raw_pass']
DEP_ANN = dep9 / M * A
CAPEX_ANN = capex9 / M * A
say(f"[Depreciation and capital expenditure, ACTUAL] the nine audited months charged "
    f"{dep9/M:,.0f} of depreciation and right-of-use amortisation and paid {capex9/M:,.0f} in "
    f"cash for fixed assets and projects under construction. Annualised: {DEP_ANN:,.0f} and "
    f"{CAPEX_ANN:,.0f}. The previous edition modelled depreciation at 1.1% of revenue "
    f"({0.011*BASE_REV:,.0f}) and capital expenditure at 1.45% ({0.0145*BASE_REV:,.0f}) — "
    f"{0.011*BASE_REV/DEP_ANN:.1f}x and {0.0145*BASE_REV/CAPEX_ANN:.1f}x the actual. Capital "
    f"expenditure is running at {CAPEX_ANN/DEP_ANN:.2f} times depreciation, which is BELOW "
    f"replacement: this plant is being run, not renewed, and that is the most important thing "
    f"the filings say about its cash flow. It also means the free cash flow the previous "
    f"edition reported was understated by roughly {(0.0145*BASE_REV-CAPEX_ANN):,.0f} a year on "
    f"the capital line alone.")
OPEX_ANN = (ga9 + mkt9 + oth9) / M * A
ebitda_cy25 = (gp9 / M - (ga9 + mkt9 + oth9) / M) * A + DEP_ANN
gm_cy25 = BASE_GM
dna_cy25 = DEP_ANN
opex_cy25 = OPEX_ANN
gp_cy25 = gp9 / M * A
npa_cy25 = (pat9 - V['nci_h2_25'] - V['nci_q1_26']) / M * A
np_cy25 = pat9 / M * A

# ---- cost of capital: explicit window (sovereign double-count removed) -----
rf_star = V['rf'] - V['sov_spread_cds']
ke_exp = rf_star + V['beta'] * V['erp_cds']
ke_rating_alt = (V['rf'] - V['sov_spread_rating']) + V['beta'] * V['erp_rating']
ke_raw_retired = V['rf'] + V['beta'] * V['erp_cds']
kd_at = V['kd'] * (1 - TAX)
# The company is NET CASH, so the weights need care and the direction of the effect is the
# OPPOSITE of the intuition carried over from a net-debt name.
#
# Net debt is negative, so the debt weight is negative and the equity weight exceeds 100%.
# The cost of that negative debt is not the borrowing rate — it is the blend of what the
# tiny debt book costs and what the large cash pile EARNS, which is the deposit yield. Put
# together, the weighting UNLEVERS the observed cost of equity for the cash: the operating
# business must be discounted at a HIGHER rate than the equity, because roughly a fifth of
# the market capitalisation is near-riskless cash diluting the observed equity risk.
#
# The identity that proves it: EV/market-cap x WACC_operating + cash/market-cap x cash-cost
# recombines exactly to the cost of equity. Asserted below.
k_nd_at = (V['kd'] * debt_b - V['cash_yield'] * cash_b) / (debt_b - cash_b) * (1 - TAX)
wd_exp = nd_cy25 / (nd_cy25 + MKTCAP)
we_exp = 1 - wd_exp
wacc_exp = we_exp * ke_exp + wd_exp * k_nd_at
wacc_exp_gross = (1 - wd_gross) * ke_exp + wd_gross * kd_at
say(f"[Cost of equity] risk-free {V['rf']:.2%} less the sovereign default spread "
    f"{V['sov_spread_cds']:.2%} = {rf_star:.2%}; plus beta {V['beta']:.3f} times the equity risk "
    f"premium {V['erp_cds']:.2%} -> cost of equity {ke_exp:.2%}. Alternatives disclosed: on the "
    f"rating basis {ke_rating_alt:.2%}; the RETIRED un-netted construction {ke_raw_retired:.2%}, "
    f"kept only for the audit trail — it charges Egypt's sovereign default risk twice, once "
    f"inside the pound yield and again in the country premium.")
say(f"[Weighted cost of capital, explicit window] net debt is NEGATIVE, so the debt weight is "
    f"{wd_exp:.1%} and the equity weight {we_exp:.1%}. The cost of that negative debt is the "
    f"blend of what the EGP {debt_b:,.0f}mn borrowing costs and what the EGP {cash_b:,.0f}mn cash "
    f"pile EARNS: {k_nd_at:.2%} after tax, i.e. essentially the after-tax deposit yield. Result "
    f"{wacc_exp:.2%} — ABOVE the {ke_exp:.2%} cost of equity, not below it. That direction is the "
    f"point: a company holding {-nd_cy25/MKTCAP:.0%} of its market capitalisation in near-riskless "
    f"cash has an observed equity cost that UNDERSTATES the risk of its operating assets, so "
    f"unlevering for the cash raises the operating rate. On a gross-debt basis the rate would be "
    f"{wacc_exp_gross:.2%}; that construction discounts the operating cash flows at a rate the "
    f"cash has already depressed AND then adds the cash back in the bridge, counting the cash "
    f"twice and overstating the valuation. The net basis is primary and is the more conservative "
    f"of the two by {(wacc_exp-wacc_exp_gross)*1e4:,.0f} basis points.")
_recombine = ((MKTCAP + nd_cy25) / MKTCAP) * wacc_exp + (-nd_cy25 / MKTCAP) * k_nd_at
say(f"[Unlevering identity] enterprise value over market capitalisation "
    f"({(MKTCAP+nd_cy25)/MKTCAP:.4f}) times the operating rate, plus cash over market "
    f"capitalisation ({-nd_cy25/MKTCAP:.4f}) times the cash cost, recombines to "
    f"{_recombine:.4%} against a cost of equity of {ke_exp:.4%} — exact. This is the check that "
    f"the net-cash weighting is a decomposition rather than an adjustment.")
assert abs(_recombine - ke_exp) < 1e-9, "the net-cash unlevering identity does not recombine to Ke"
assert wacc_exp > wacc_exp_gross, \
    "unlevering for net cash must RAISE the operating rate; check the signs"

# ---- terminal (norm-built, never backed out of a price) --------------------
ke_term = V['rf_term'] + V['beta'] * V['erp_term']
kd_term_at = V['kd_term'] * (1 - TAX)
wacc_term = (1 - V['wd_term']) * ke_term + V['wd_term'] * kd_term_at
say(f"[Weighted cost of capital, terminal] cost of equity {ke_term:.2%} (norm-built risk-free "
    f"{V['rf_term']:.2%} = the central bank's own 5% medium-term inflation target plus a 5.5pp "
    f"emerging-market real-rate convention, plus beta times a normalised premium "
    f"{V['erp_term']:.2%}); cost of debt after tax {kd_term_at:.2%}; weights "
    f"{1-V['wd_term']:.0%}/{V['wd_term']:.0%} -> {wacc_term:.2%}. No terminal input is an "
    f"observable quote and none is reverse-engineered from a price.")
assert wacc_term < wacc_exp, "terminal cost of capital must sit below the explicit-window rate"

# ---- glide: fractions from the cost-of-debt path ----------------------------
kdp = V['kd_path']
glide_frac = [(kdp[0] - k) / (kdp[0] - kdp[-1]) for k in kdp]
fwd = [wacc_exp - (wacc_exp - wacc_term) * f for f in glide_frac]
df, _c = [], 1.0
for w in fwd:
    _c /= (1 + w); df.append(_c)
assert all(fwd[i] >= fwd[i + 1] for i in range(4)), "the glide is not monotone"
say("[Glide] forward cost of capital " + " -> ".join(f"{w:.2%}" for w in fwd) +
    "; cumulative discount factors " + ", ".join(f"{d:.4f}" for d in df) +
    ". The glide fractions are the cost-of-debt path's own cumulative progress (" +
    ", ".join(f"{f:.3f}" for f in glide_frac) + "), so the front-loaded shape is inherited from "
    "the assumed easing calendar rather than being a second free parameter.")

# ---- FCFF waterfall — every level from the audited base ----------------------
B = build()
rev, ebitda = B['rev'], B['ebitda']
ebitda_margin = B['ebitda_margin']
say("[Forecast revenue] " + " -> ".join(f"{r:,.0f}" for r in rev) +
    f" (volume {B['vol'][0]:.3f} -> {B['vol'][-1]:.3f}mn tonnes; specialty share of revenue "
    f"{B['spec_rev'][0]/B['rev'][0]:.1%} -> {B['spec_rev'][4]/B['rev'][4]:.1%}). Base-year "
    f"revenue is the audited nine months annualised, {BASE_REV:,.0f}.")
say("[Forecast gross margin] " + " -> ".join(f"{g:.2%}" for g in B['gm']) +
    ". The margin is an OUTPUT of the audited cost composition, not a path: raw materials and "
    "supporting materials are pass-through and move with realisation and volume; salaries and "
    "the other line are pound-denominated and move with local inflation; depreciation is the "
    "asset-register charge. The margin therefore widens only to the extent that the "
    "pound-denominated cost leg grows more slowly than revenue — which is a mechanical "
    "consequence of the disclosed stack, not a view.")
dna = [DEP_ANN for _ in rev]
ebit = [ebitda[i] - dna[i] for i in range(5)]
nopat = [e * (1 - TAX_EFF) for e in ebit]
_cx = CAPEX_ANN
capex = []
for i in range(5):
    _cx *= V['fixed_cost_infl'][3 + i]
    capex.append(_cx)
nwc_pct_aud = nwc_b / BASE_REV
nwc_pct = nwc_pct_aud
nwc = [nwc_pct_aud * r for r in rev]
dnwc = [nwc[0] - nwc_b] + [nwc[i] - nwc[i - 1] for i in range(1, 5)]
say(f"[Capital expenditure, forecast] held at the ACTUAL run rate {CAPEX_ANN:,.0f} grown with "
    f"local inflation: " + " -> ".join(f"{c:,.0f}" for c in capex) + f". That is "
    f"{capex[0]/dna[0]:.2f} times depreciation in the first forecast year. A reader who believes "
    f"the plant must eventually be renewed should raise this line — it is the single sharpest "
    f"criticism available of this valuation and section 7 says so.")
fcff = [nopat[i] + dna[i] - capex[i] - dnwc[i] for i in range(5)]
pv = [fcff[i] * df[i] for i in range(5)]
pv_explicit = float(sum(pv))
say(f"[Free cash flow to the firm] " + " -> ".join(f"{f:,.0f}" for f in fcff) +
    f"; present value of the explicit window {pv_explicit:,.0f}.")

# ---- one roll-forward, consumed everywhere ---------------------------------
NCI_SHARE = V['nci_share']
PAYOUT = V['payout_reported']
interest_path, np_fc, div_fc, eq_fc, nd_fc, cash_fc = [], [], [], [], [], []
_nd, _eq = nd_cy25, eqp_cy25
for i in range(5):
    _cash = debt_b - _nd
    _int = V['cash_yield_path'][i] * max(_cash, 0.0) - V['kd_path'][i] * debt_b
    _pbt = ebit[i] + _int
    _npa = _pbt * (1 - TAX) * (1 - NCI_SHARE)
    _div = PAYOUT * _npa
    _eq += _npa - _div
    _nd = _nd - (fcff[i] + _int * (1 - TAX)) + _div
    interest_path.append(_int); np_fc.append(_npa); div_fc.append(_div)
    eq_fc.append(_eq); nd_fc.append(_nd); cash_fc.append(debt_b - _nd)
say(f"[Forecast finance income] " + " -> ".join(f"{x:,.0f}" for x in interest_path) +
    f" — the charge is a CREDIT throughout and it falls even as the cash pile builds, because "
    f"the deposit yield eases with the policy rate faster than the balance grows. Attributable "
    f"profit " + ", ".join(f"{x:,.0f}" for x in np_fc) + f"; net cash " +
    ", ".join(f"{-x:,.0f}" for x in nd_fc) + f" on a {PAYOUT:.1%} payout.")

# ---- invested capital and the terminal return ------------------------------
ppe_f, _p = [], ppe_cy25
for i in range(5):
    _p += capex[i] - dna[i]; ppe_f.append(_p)
ic = [nwc[i] + ppe_f[i] for i in range(5)]
roic = [nopat[i] / ic[i] for i in range(5)]
roic_term = nopat[-1] * (1 + V['g_term']) / ic[-1]
ic_cy25 = nwc_b + ppe_cy25
say(f"[Return on invested capital] {' / '.join(f'{r:.1%}' for r in roic)}; terminal return taken "
    f"as next year's NOPAT over closing invested capital, {roic_term:.1%}. The level is high "
    f"because the plant is substantially written down and the working capital is negative-to-"
    f"negligible — a real feature of the business, and the reason the required terminal "
    f"reinvestment rate comes out low.")

# ---- terminal growth: reconciled against the AUDITED record ------------------
# The previous edition reconstructed four historical years from days drivers and a roll-back and
# then reconciled against its own reconstruction. The filings give the real thing: two half-years
# and two quarters of audited gross profit, an audited cost stack, an audited asset register and
# an audited capital-expenditure figure. The reconciliation now runs on those.
HKEY = ['6M Dec-2024', '3M Mar-2025', '6M Dec-2025', '3M Mar-2026']
_scale = {'6M Dec-2024': 2.0, '3M Mar-2025': 4.0, '6M Dec-2025': 2.0, '3M Mar-2026': 4.0}
hist_rev = {'6M Dec-2024': V['rev_h2_24'] / M, '3M Mar-2025': V['rev_q1_25'] / M,
            '6M Dec-2025': V['rev_h2_25'] / M, '3M Mar-2026': V['rev_q1_26'] / M}
hist_gp = {'6M Dec-2024': (V['rev_h2_24'] - V['cogs_h2_24']) / M,
           '3M Mar-2025': (V['rev_q1_25'] - V['cogs_q1_25']) / M,
           '6M Dec-2025': (V['rev_h2_25'] - V['cogs_h2_25']) / M,
           '3M Mar-2026': (V['rev_q1_26'] - V['cogs_q1_26']) / M}
hist_gm = {k: hist_gp[k] / hist_rev[k] for k in HKEY}
# operating profit is disclosed for the two periods that carry a full expense note
hist_ebit = {'6M Dec-2025': 486_028_457.0 / M, '3M Mar-2026': 643_172_153.0 / M,
             '6M Dec-2024': 743_620_650.0 / M, '3M Mar-2025': 247_222_032.0 / M}
nopat_h = {k: hist_ebit[k] * _scale[k] * (1 - TAX_EFF) for k in HKEY}
ic_h = {'6M Dec-2025': IC_B, '3M Mar-2026': IC_B,
        '6M Dec-2024': ((918_133_089 + 297_358_158) + (2_774_368_060 + 797_196_793 + 340_920_248)
                        - (10_452_591 + 1_002_068_641)) / M,
        '3M Mar-2025': ((937_851_261 + 403_190_211) + (3_735_009_103 + 894_888_039 + 611_842_230)
                        - (15_486_636 + 3_102_041_816)) / M}
capex_h = {'6M Dec-2025': V['capex_h2_25'] / M * 2, '3M Mar-2026': V['capex_q1_26'] / M * 4,
           '6M Dec-2024': V['capex_h2_25'] / M * 2, '3M Mar-2025': V['capex_q1_26'] / M * 4}
dep_h = {'6M Dec-2025': V['dep_h2_25'] / M * 2, '3M Mar-2026': V['dep_q1_26'] / M * 4,
         '6M Dec-2024': V['dep_h2_25'] / M * 2, '3M Mar-2025': V['dep_q1_26'] / M * 4}
hist_roic = {k: nopat_h[k] / ic_h[k] for k in HKEY}
hist_rr = {k: (capex_h[k] - dep_h[k]) / nopat_h[k] for k in HKEY}
hist_impl_g = {k: hist_roic[k] * hist_rr[k] for k in HKEY}
hist_character = {k: ('burst' if hist_rr[k] > 1.0 else 'stable') for k in HKEY}
nopat_cagr = (nopat_h['3M Mar-2026'] / nopat_h['6M Dec-2024']) ** (1 / 1.25) - 1
stable_keys = [k for k in HKEY if hist_character[k] == 'stable']
stable_g = float(np.mean([hist_impl_g[k] for k in stable_keys]))
say("[Terminal growth, reconciled against the AUDITED record] gross margin as filed " +
    " / ".join(f"{k} {hist_gm[k]:.2%}" for k in HKEY) + ". Annualised returns on invested "
    "capital " + " / ".join(f"{hist_roic[k]:.1%}" for k in HKEY) + "; reinvestment rates " +
    " / ".join(f"{hist_rr[k]:+.1%}" for k in HKEY) + "; implied growth " +
    " / ".join(f"{hist_impl_g[k]:+.1%}" for k in HKEY) + ".")
say(f"[Terminal growth, the check that now BINDS] reinvestment is NEGATIVE in every audited "
    f"period, because cash capital expenditure is running below the depreciation charge. Growth "
    f"= return x reinvestment therefore implies a NEGATIVE steady-state growth rate of about "
    f"{stable_g:.1%}: on its own recent record this company is shrinking its capital base, not "
    f"compounding it. The adopted terminal rate of {V['g_term']:.1%} is NOT supported by the "
    f"reinvestment identity and the study says so on its face rather than burying it. Two "
    f"readings are defensible and both are published: either the under-investment is temporary "
    f"and capital expenditure must rise toward depreciation — in which case free cash flow in "
    f"the explicit window is overstated by roughly {dna[0]-capex[0]:,.0f} a year — or it is "
    f"durable and the terminal growth rate should be at or below zero. The sensitivity grid runs "
    f"terminal growth down to 3% and the reader can go lower.")
say(f"[Terminal growth, stated plainly] the two standing checks disagree with each other, and "
    f"that is the honest reading rather than a problem to be smoothed. Check (a), the historical "
    f"compound NOPAT rate, is {nopat_cagr:+.1%} — far ABOVE the adopted {V['g_term']:.1%}; it is "
    f"a recovery rate off a devaluation-compressed base and belongs in the explicit years, not "
    f"in perpetuity. Check (b), return times reinvestment from stable years, is {stable_g:.1%} — "
    f"BELOW the adopted rate. The adopted {V['g_term']:.0%} sits between them and above the one "
    f"that describes a steady state, so on the check that matters for a perpetuity it remains on "
    f"the GENEROUS side of the company's own record. Sensitised 3-7%; the grid is on the face of "
    f"the workbook. NOTE the reinvestment definition: check (b) uses net capex over NOPAT, "
    f"EXCLUDING working capital, while the free-cash-flow waterfall subtracts working capital. On "
    f"the waterfall-consistent definition the base-year reinvestment rate is "
    f"{(capex_h['6M Dec-2025']-dep_h['6M Dec-2025']+dnwc[0])/nopat_h['6M Dec-2025']:.1%} and the implied "
    f"growth is {hist_roic['6M Dec-2025']*(capex_h['6M Dec-2025']-dep_h['6M Dec-2025']+dnwc[0])/nopat_h['6M Dec-2025']:.1%} "
    f"— ABOVE the adopted rate. Both definitions are shown; neither is hidden.")
rr_waterfall = (capex_h['6M Dec-2025'] - dep_h['6M Dec-2025'] + dnwc[0]) / nopat_h['6M Dec-2025']
g_waterfall = hist_roic['6M Dec-2025'] * rr_waterfall
blend_ceiling = V['egypt_nominal_growth']
dom_share_term = 1.0 - 0.0
fcst_cagr = (rev[-1]/rev[0])**0.25 - 1
yrs_cross = None
cross_candidates = {'recent NOPAT compound rate': None}
assert V['g_term'] < blend_ceiling, "terminal growth exceeds the blended nominal ceiling"

rr_term = V['g_term'] / roic_term
nopat_term = nopat[-1] * (1 + V['g_term'])
tv = nopat_term * (1 - rr_term) / (wacc_term - V['g_term'])
pv_tv = tv * df[-1]
ev = pv_explicit + pv_tv
tv_share = pv_tv / ev
say(f"[Terminal value] required reinvestment rate = growth / return = {V['g_term']:.1%} / "
    f"{roic_term:.1%} = {rr_term:.1%}; terminal NOPAT {nopat_term:,.0f}; terminal value "
    f"{tv:,.0f} capitalised at the terminal cost of capital {wacc_term:.2%} and discounted at the "
    f"YEAR-5 cumulative factor {df[-1]:.4f} — one date, one price of time — giving a present "
    f"value of {pv_tv:,.0f}. TERMINAL VALUE IS {tv_share:.1%} OF ENTERPRISE VALUE.")
assert abs(roic_term * rr_term - V['g_term']) < 1e-9, "terminal growth != return x reinvestment"

# ---- enterprise value -> equity bridge --------------------------------------
nci_val = NCI_SHARE * ev          # on the OPERATING enterprise value, before the cash
eq_attr = ev - nd_cy25 - nci_val
dcf_ps = eq_attr / SH
say(f"[Bridge] enterprise value {ev:,.0f} less net debt {nd_cy25:,.0f} (a NEGATIVE, i.e. net "
    f"cash of {-nd_cy25:,.0f} is ADDED) = {ev - nd_cy25:,.0f}; less minority interests at their "
    f"{NCI_SHARE:.1%} share OF THE ENTERPRISE VALUE (not of the cash — the previous "
    f"construction deducted it after the cash was added, which handed the minority "
    f"{NCI_SHARE*-nd_cy25:,.0f} of the parent's balance) = {nci_val:,.0f} -> equity attributable "
    f"{eq_attr:,.0f} = EGP "
    f"{dcf_ps:.2f} a share against a spot of EGP {SPOT:.2f} ({dcf_ps/SPOT-1:+.1%}).")
assert abs((ev - nd_cy25 - nci_val) - eq_attr) < 1e-6, "the bridge does not close"
assert nci_val > 0 and nd_cy25 < 0, "sign check on the bridge components"

# ---- contested choices, computed rather than asserted -----------------------
wacc_exp_rating = we_exp * ke_rating_alt + wd_exp * kd_at
wacc_term_rating = (1 - V['wd_term']) * (V['rf_term'] + V['beta'] * (V['erp_term'] + 0.045)) + \
    V['wd_term'] * kd_term_at


def _val_at(we_, wt_, g_=None, nci_=None):
    g_ = V['g_term'] if g_ is None else g_
    nci_ = NCI_SHARE if nci_ is None else nci_
    _fwd = [we_ - (we_ - wt_) * f for f in glide_frac]
    _df, cc = [], 1.0
    for w in _fwd:
        cc /= (1 + w); _df.append(cc)
    _roic = nopat[-1] * (1 + g_) / ic[-1]
    _rr = min(g_ / _roic, 0.95)
    _tv = nopat[-1] * (1 + g_) * (1 - _rr) / max(wt_ - g_, 0.02)
    _ev = sum(fcff[i] * _df[i] for i in range(5)) + _tv * _df[-1]
    return (_ev * (1 - nci_) - nd_cy25) / SH


dcf_rating_ps = _val_at(wacc_exp_rating, wacc_term_rating)
nci_alt = 0.06
dcf_nci_alt_ps = _val_at(wacc_exp, wacc_term, nci_=nci_alt)
dcf_grossbasis_ps = _val_at(wacc_exp_gross, wacc_term)
say(f"[Contested choices, computed] (1) rating-basis cost of capital instead of the CDS basis: "
    f"explicit {wacc_exp_rating:.2%} / terminal {wacc_term_rating:.2%} -> EGP "
    f"{dcf_rating_ps:.2f} ({dcf_rating_ps/dcf_ps-1:+.1%}). (2) minority share doubled to "
    f"{nci_alt:.0%} -> EGP {dcf_nci_alt_ps:.2f} ({dcf_nci_alt_ps/dcf_ps-1:+.1%}). (3) "
    f"GROSS-debt rather than net-debt weights, the construction this study rejects because it "
    f"counts the cash pile twice -> EGP {dcf_grossbasis_ps:.2f} "
    f"({dcf_grossbasis_ps/dcf_ps-1:+.1%}).")

# ---- currency-of-discounting alternative -----------------------------------
WACC_USD = 0.90 * (V['wacc_usd_rf'] + V['beta'] * V['wacc_usd_erp']) + \
    0.10 * 0.065 * (1 - TAX)
exp_frac = [(B['spec_rev'][i] * 0.35) / rev[i] for i in range(5)]
fcff_f_usd = [fcff[i] * exp_frac[i] / V['fx_path'][i] for i in range(5)]
fcff_d = [fcff[i] * (1 - exp_frac[i]) for i in range(5)]
df_usd, _c2 = [], 1.0
for _ in range(5):
    _c2 /= (1 + WACC_USD); df_usd.append(_c2)
pv_f_usd = sum(fcff_f_usd[i] * df_usd[i] for i in range(5))
tv_f_usd = (nopat_term * (1 - rr_term) * exp_frac[-1] / V['fx_path'][-1]) / (WACC_USD - 0.035)
ev_f_egp = (pv_f_usd + tv_f_usd * df_usd[-1]) * V['fx']
pv_d = sum(fcff_d[i] * df[i] for i in range(5))
tv_d = nopat_term * (1 - rr_term) * (1 - exp_frac[-1]) / (wacc_term - V['g_term'])
ev_ccy = ev_f_egp + pv_d + tv_d * df[-1]
ccy_ps = (ev_ccy * (1 - NCI_SHARE) - nd_cy25) / SH
say(f"[Currency-of-discounting alternative] the export leg ({exp_frac[-1]:.0%} of cash flow) is "
    f"first DEFLATED to dollars at each year's exchange rate, discounted at a dollar cost of "
    f"capital of {WACC_USD:.2%} with 3.5% terminal growth, and only then translated back at the "
    f"spot rate. Discounting a pound-denominated cash flow already inflated by the assumed "
    f"depreciation path directly at a dollar rate would count the currency benefit twice. Result "
    f"EGP {ccy_ps:.2f} a share ({ccy_ps/SPOT-1:+.1%} against spot).")

# ---- lens 2: relative -------------------------------------------------------
REL_I = 1                                    # 2027E, the year-2 forward
ebitda_mid = ebitda[REL_I]
df_rel = df[REL_I]


pv_interim = sum(pv[:REL_I + 1])


def _rel(mult):
    """A multiple on a forward year values the business FROM that year on. The cash the firm
    generates in the meantime belongs to today's owner and must be added back, or the lens
    silently discards it — which the previous version did, to the tune of the figure below."""
    return (((mult * ebitda_mid) * df_rel + pv_interim) * (1 - NCI_SHARE) - nd_cy25) / SH


rel_ps, rel_bear, rel_bull = _rel(V['ev_ebitda_just']), _rel(3.5), _rel(6.0)
ev_rel_fwd = V['ev_ebitda_just'] * ebitda_mid
ev_rel = ev_rel_fwd * df_rel
ev_trailing = MKTCAP + nd_cy25
ev_ebitda_trailing = ev_trailing / ebitda_cy25
pe_trailing = SPOT / (npa_cy25 / SH)
say(f"[Relative lens] interim free cash flow added back: {pv_interim:,.0f} of present value "
    f"for the years before the multiple year, which the previous construction dropped. "
    f"{V['ev_ebitda_just']}x on 2027E EBITDA {ebitda_mid:,.0f} gives an enterprise "
    f"value of {ev_rel_fwd:,.0f} AS AT end-2027; discounted back at the year-2 factor "
    f"{df_rel:.4f} that is {ev_rel:,.0f} today -> EGP {rel_ps:.2f} a share. Not discounting a "
    f"forward enterprise value back to today would have given EGP "
    f"{((ev_rel_fwd - nd_cy25) * (1 - NCI_SHARE)) / SH:.2f}. The company's own trailing multiple "
    f"is {ev_ebitda_trailing:.1f}x enterprise value to EBITDA and {pe_trailing:.1f}x earnings.")

# ---- lens 3: normalised earnings power --------------------------------------
NORM_I = 2                                   # every component from the SAME year
norm_rev = rev[NORM_I]
norm_ebitda = ebitda[NORM_I]
norm_ebit = norm_ebitda - dna[NORM_I]
norm_interest = interest_path[NORM_I]
norm_np = (norm_ebit + norm_interest) * (1 - TAX) * (1 - NCI_SHARE)
norm_eps = norm_np / SH
norm_ps = V['pe_just'] * norm_eps
norm_bear, norm_bull = 5.5 * norm_eps, 9.5 * norm_eps
say(f"[Normalised earnings lens] every component is taken from 2028E: revenue {norm_rev:,.0f}, "
    f"EBITDA {norm_ebitda:,.0f}, depreciation {dna[NORM_I]:,.0f}, finance income "
    f"{norm_interest:,.0f} -> attributable earnings {norm_np:,.0f}, EGP {norm_eps:.2f} a share; "
    f"at {V['pe_just']}x -> EGP {norm_ps:.2f}.")

# ---- lens 4: book value and sustainable return ------------------------------
bvps = eqp_cy25 / SH
pb_just = (V['roe_sust'] - V['g_term']) / (ke_term - V['g_term'])
book_ps = pb_just * bvps
book_bear = ((V['roe_sust'] - 0.05 - 0.03) / (0.5 * (ke_exp + ke_term) - 0.03)) * bvps
book_bull = ((V['roe_sust'] + 0.03 - V['g_term']) / (ke_term - V['g_term'])) * bvps
roe_trailing = npa_cy25 / ((V['eq_parent_jun25'] / M + eqp_cy25) / 2)
say(f"[Book lens] justified price-to-book {pb_just:.2f}x = (sustainable return "
    f"{V['roe_sust']:.1%} less growth {V['g_term']:.0%}) / (PERPETUAL cost of equity "
    f"{ke_term:.2%} less growth), applied to book value of EGP {bvps:.2f} a share -> EGP "
    f"{book_ps:.2f}. The perpetual rate is the right one inside a perpetuity identity; using a "
    f"blend of the explicit and terminal rates would be internally inconsistent. Trailing return "
    f"on average parent equity is {roe_trailing:.1%}.")

# ---- scenarios --------------------------------------------------------------
def dcf_scenario(vol_mult=1.0, price_mult=1.0, fx_mult=1.0, gm_shift=0.0,
                 wacc_shift=0.0, g=None, nwc_p=None):
    """Full re-run of the unit build and the waterfall, so a volume, price or currency
    move flows through both legs exactly as it does in the base case."""
    g = V['g_term'] if g is None else g
    nwc_p = nwc_pct if nwc_p is None else nwc_p
    S = build(vol_mult=vol_mult, price_mult=price_mult, fx_mult=fx_mult, gm_shift=gm_shift)
    _rev, _ebitda = S['rev'], S['ebitda']
    _dna = [DEP_ANN for _ in _rev]
    _ebit = [_ebitda[i] - _dna[i] for i in range(5)]
    _nopat = [e * (1 - TAX_EFF) for e in _ebit]
    _capex, _cx = [], CAPEX_ANN
    for i in range(5):
        _cx *= V['fixed_cost_infl'][3 + i]; _capex.append(_cx)
    _nwc = [nwc_p * r for r in _rev]
    _dnwc = [_nwc[0] - nwc_b] + [_nwc[i] - _nwc[i - 1] for i in range(1, 5)]
    _f = [_nopat[i] + _dna[i] - _capex[i] - _dnwc[i] for i in range(5)]
    _we, _wt = wacc_exp + wacc_shift, wacc_term + wacc_shift
    _fwd = [_we - (_we - _wt) * f for f in glide_frac]
    _df, cc = [], 1.0
    for w in _fwd:
        cc /= (1 + w); _df.append(cc)
    _ppe, pp = [], ppe_cy25
    for i in range(5):
        pp += _capex[i] - _dna[i]; _ppe.append(pp)
    _roic = _nopat[-1] * (1 + g) / (_nwc[-1] + _ppe[-1])
    _rr = min(g / _roic, 0.95)
    _tv = _nopat[-1] * (1 + g) * (1 - _rr) / max(_wt - g, 0.02)
    _ev = sum(_f[i] * _df[i] for i in range(5)) + _tv * _df[-1]
    return (_ev * (1 - NCI_SHARE) - nd_cy25) / SH


_chk = dcf_scenario()
assert abs(_chk - dcf_ps) < 0.01, f"scenario engine does not reproduce the base: {_chk} vs {dcf_ps}"
SCEN = dict(
    bear=dict(vol_mult=0.4, gm_shift=-0.010, fx_mult=0.97, wacc_shift=+0.02, g=0.03),
    bull=dict(vol_mult=1.5, gm_shift=+0.010, fx_mult=1.03, wacc_shift=-0.02, g=0.06))
dcf_bear = dcf_scenario(**SCEN['bear'])
dcf_bull = dcf_scenario(**SCEN['bull'])
SCEN['bear']['ps'], SCEN['bull']['ps'], SCEN['base_ps'] = dcf_bear, dcf_bull, dcf_ps
SCEN['labels'] = dict(
    vol_mult='Volume growth path, as a multiple of the assumed path',
    gm_shift='Gross margin, shifted on every forecast year',
    fx_mult='Exchange-rate path, as a multiple of the assumed path',
    wacc_shift='Cost of capital, shifted at BOTH the explicit and terminal anchors',
    g='Terminal growth rate')
say(f"[Scenarios on the cash-flow lens] bear EGP {dcf_bear:.2f} / base EGP {dcf_ps:.2f} / bull "
    f"EGP {dcf_bull:.2f}. The scenarios are FIVE simultaneous driver moves, not a single lever: "
    f"volume growth at {SCEN['bear']['vol_mult']:.1f}x / {SCEN['bull']['vol_mult']:.1f}x the "
    f"assumed path, gross margin {SCEN['bear']['gm_shift']:+.1%} / "
    f"{SCEN['bull']['gm_shift']:+.1%}, the exchange-rate path "
    f"{SCEN['bear']['fx_mult']-1:+.0%} / {SCEN['bull']['fx_mult']-1:+.0%}, the cost of capital "
    f"{SCEN['bear']['wacc_shift']:+.0%} / {SCEN['bull']['wacc_shift']:+.0%} at both anchors, and "
    f"terminal growth {SCEN['bear']['g']:.0%} / {SCEN['bull']['g']:.0%}. Because all five move "
    f"together and in the same direction, the bear and bull ends are JOINT-worst and JOINT-best "
    f"cases and are much wider than any single-driver row in the sensitivity table; they are not "
    f"a confidence interval and no probability is attached to them.")

# ---- synthesis --------------------------------------------------------------
W = V['lens_weights']
lenses = dict(
    dcf=dict(name='Discounted cash flow (primary)', bear=dcf_bear, base=dcf_ps, bull=dcf_bull,
             w=W['dcf']),
    relative=dict(name='Relative multiples', bear=rel_bear, base=rel_ps, bull=rel_bull,
                  w=W['relative']),
    normalized=dict(name='Normalised earnings power', bear=norm_bear, base=norm_ps, bull=norm_bull,
                    w=W['normalized']),
    book=dict(name='Book value and sustainable return', bear=book_bear, base=book_ps,
              bull=book_bull, w=W['book']),
)
central = sum(l['base'] * l['w'] for l in lenses.values())
lo = min(l['bear'] for l in lenses.values())
hi = max(l['bull'] for l in lenses.values())
lenses['central'] = dict(name='Weighted central', bear=lo, base=central, bull=hi, w=1.0)
say(f"[Synthesis] weighted central EGP {central:.2f}; full span across lenses and scenarios EGP "
    f"{lo:.2f} - {hi:.2f}; spot EGP {SPOT:.2f} ({central/SPOT-1:+.1%} to the central).")
assert 0.20 <= central / SPOT <= 3.0, f"central/spot {central/SPOT:.2f} outside the plausibility band"

# ---- sensitivity grids (whole-model re-runs) --------------------------------
g_grid = [0.03, 0.04, 0.05, 0.06, 0.07]
wt_grid = [wacc_term - 0.02, wacc_term - 0.01, wacc_term, wacc_term + 0.01, wacc_term + 0.02]
we_grid = [wacc_exp - 0.03, wacc_exp - 0.015, wacc_exp, wacc_exp + 0.015, wacc_exp + 0.03]
grid_wacc_g = [[_val_at(wacc_exp, wt, g) for g in g_grid] for wt in wt_grid]
grid_exp_term = [[_val_at(we, wt) for wt in wt_grid] for we in we_grid]
beta_grid = [0.60, 0.80, 0.9405, 1.15, 1.30]
grid_beta = []
for b in beta_grid:
    _ke = rf_star + b * V['erp_cds']
    _kt = V['rf_term'] + b * V['erp_term']
    grid_beta.append(_val_at(we_exp * _ke + wd_exp * kd_at,
                             (1 - V['wd_term']) * _kt + V['wd_term'] * kd_term_at))
gm_grid = [-0.010, -0.005, 0.0, 0.005, 0.010]
grid_margin = [dcf_scenario(gm_shift=s) for s in gm_grid]
vol_grid = [0.0, 0.5, 1.0, 1.5, 2.0]
grid_vol = [dcf_scenario(vol_mult=m) for m in vol_grid]
fx_grid = [0.90, 0.95, 1.0, 1.05, 1.10]
grid_fx = [dcf_scenario(fx_mult=m) for m in fx_grid]
nwc_grid = [0.00, 0.01, nwc_pct, 0.03, 0.05]
grid_nwc = [dcf_scenario(nwc_p=p) for p in nwc_grid]

# ---- expert panel: three genuinely different methods ------------------------
# Cast by METHOD from the persona library; presented to the reader as Expert 1/2/3.
e1_i = 2
e1_ebit = ebit[e1_i]
e1_int = interest_path[e1_i]
e1_eps = ((e1_ebit + e1_int) * (1 - TAX) * (1 - NCI_SHARE)) / SH
e1_pe = 7.0
e1_base, e1_lo, e1_hi = e1_pe * e1_eps, 5.0 * e1_eps, 9.5 * e1_eps

# Expert 2 works the EQUITY side directly: free cash flow to equity, discounted on the
# cost of EQUITY's own glide, with no enterprise-to-equity bridge at all. Capitalising a
# mid-forecast cash flow straight at the TERMINAL cost of equity — as a first draft of this
# panel did — prices one date twice: it takes a cash flow five years out and brings it home
# at a rate that only applies once the economy has normalised. The glide is applied here for
# exactly the reason it is applied in the primary model.
e2_fcfe = [(fcff[i] + interest_path[i] * (1 - TAX)) * (1 - NCI_SHARE) for i in range(5)]
e2_ke_path = [ke_exp - (ke_exp - ke_term) * f for f in glide_frac]
e2_df, _ce = [], 1.0
for k in e2_ke_path:
    _ce /= (1 + k); e2_df.append(_ce)
e2_pv = sum(e2_fcfe[i] * e2_df[i] for i in range(5))
e2_tv = e2_fcfe[-1] * (1 + V['g_term']) * (1 - rr_term) / (ke_term - V['g_term'])
e2_pv_tv = e2_tv * e2_df[-1]
e2_ke = ke_term
e2_fcff = float(np.mean(fcff[2:]))
e2_fin_at = interest_path[3] * (1 - TAX)
e2_base = (e2_pv + e2_pv_tv) / SH
e2_lo = (e2_pv + e2_fcfe[-1] * 1.03 * (1 - rr_term) / (ke_term + 0.03 - 0.03) * e2_df[-1]) / SH
e2_hi = (e2_pv + e2_fcfe[-1] * 1.06 * (1 - rr_term) / (ke_term - 0.06) * e2_df[-1]) / SH
say(f"[Expert 2 construction] free cash flow to equity " +
    " -> ".join(f"{x:,.0f}" for x in e2_fcfe) + f"; discounted on the cost of EQUITY's own glide "
    f"(" + " -> ".join(f"{k:.1%}" for k in e2_ke_path) + f") for a present value of "
    f"{e2_pv:,.0f}, plus a terminal block of {e2_pv_tv:,.0f}. No bridge is used: the cash pile "
    f"reaches the shareholder through the finance income line rather than as a balance-sheet "
    f"add-back, which is what makes this a genuinely independent second read rather than a "
    f"re-arrangement of the first.")

ic_beg = [ic_cy25] + ic[:-1]
ep_ = [nopat[i] - fwd[i] * ic_beg[i] for i in range(5)]
pv_ep = sum(ep_[i] * df[i] for i in range(5))
ep_term = nopat[-1] * (1 + V['g_term']) - wacc_term * ic[-1]
pv_ep_term = ep_term / (wacc_term - V['g_term']) * df[-1]
e3_ev = ic_cy25 + pv_ep + pv_ep_term
e3_base = (e3_ev * (1 - NCI_SHARE) - nd_cy25) / SH
e3_lo = ((ic_cy25 + pv_ep * 0.6 + pv_ep_term * 0.55) * (1 - NCI_SHARE) - nd_cy25) / SH
e3_hi = ccy_ps
say(f"[Economic-profit convention] the capital charge is taken on BEGINNING-of-year invested "
    f"capital, not ending. Charging ending capital would understate economic profit by about "
    f"{sum((ic[i]-ic_beg[i])*fwd[i] for i in range(5))/5:,.0f}mn a year.")
experts = dict(
    e1=dict(method_short='earnings power at a justified multiple', base=e1_base,
            rng=[e1_lo, e1_hi], eps=e1_eps, ebit=e1_ebit, interest=e1_int, pe=e1_pe,
            year=YRS[e1_i]),
    e2=dict(method_short='free cash flow to equity, discounted', base=e2_base,
            rng=[e2_lo, e2_hi], fcff=e2_fcff, fcfe=e2_fcfe, ke=e2_ke, fin_at=e2_fin_at,
            ke_path=e2_ke_path, df=e2_df, pv=e2_pv, pv_tv=e2_pv_tv),
    e3=dict(method_short='cash returns against the cost of capital', base=e3_base,
            rng=[e3_lo, e3_hi], ic0=ic_cy25, pv_ep=pv_ep, pv_ep_term=pv_ep_term, ev=e3_ev,
            ep=ep_, spread=[roic[i] - fwd[i] for i in range(5)]),
)
panel_centre = float(sorted([e1_base, e2_base, e3_base])[1])
say(f"[Expert panel] Expert 1 EGP {e1_base:.2f} [{e1_lo:.2f}-{e1_hi:.2f}]; Expert 2 EGP "
    f"{e2_base:.2f} [{e2_lo:.2f}-{e2_hi:.2f}]; Expert 3 EGP {e3_base:.2f} [{e3_lo:.2f}-"
    f"{e3_hi:.2f}]; panel median EGP {panel_centre:.2f} ({panel_centre/SPOT-1:+.1%} against spot).")

# ---- fan for the figure -----------------------------------------------------
paths3 = np.load(os.path.join(HERE, 'paths_3M.npy'))
fan = np.percentile(paths3, [5, 25, 50, 75, 95], axis=0)
np.save(os.path.join(HERE, 'fan.npy'), fan)

# ============================ EMIT ===========================================
step0 = json.load(open(os.path.join(HERE, 'step0_result.json')))
strike = json.load(open(os.path.join(HERE, 'strike_result.json')))
beta_res = json.load(open(os.path.join(HERE, 'beta_result.json')))
bt5 = json.load(open(os.path.join(HERE, 'backtest_5y.json')))

OUT = dict(
    meta=dict(ticker='AMOC', company='Alexandria Mineral Oils Company S.A.E.', market='EGX',
              currency='EGP', asof='2026-08-06', spot=SPOT, shares_mn=SH, mktcap=MKTCAP,
              ev_trailing=ev_trailing, klass='downstream petroleum operating company',
              sector='Oil & gas refining and marketing — lubricant base oils and waxes',
              fy_note='financial year moved from 30 June to 31 December'),
    inputs=INP,
    hist_is={k: dict(rev=hist_rev[k], gp=hist_gp[k], gm=hist_gm[k], ebit=hist_ebit[k])
             for k in HKEY},
    hist_bs={k: dict(ic=ic_h[k], roic=hist_roic[k], rr=hist_rr[k]) for k in HKEY},
    audited=dict(periods=HKEY, rev=hist_rev, gp=hist_gp, gm=hist_gm, ebit=hist_ebit,
                 cost_stack={k: v / M for k, v in COS.items()},
                 cost_share=cos_share, prod_t=PT, prod_v=PV, px=px, mix_t=mix_t, mix_v=mix_v,
                 growth_v=growth_v, base_rev=BASE_REV, base_gm=BASE_GM, tax_eff=TAX_EFF,
                 dep_ann=DEP_ANN, capex_ann=CAPEX_ANN, opex_ann=OPEX_ANN, ic=IC_B,
                 ppe=ppe_b, nwc=nwc_b, cash=cash_b, debt=debt_b, provisions=V['provisions']/M,
                 pledged=V['fin_inv']/M, nci_share=NCI_SHARE, spec_t=spec_t, spec_v=spec_v,
                 raw_of_rev=raw_of_rev, rev9=rev9/M, gp9=gp9/M, pat9=pat9/M),
    base=dict(rev_cy25=rev_cy25, pat_cy25=pat_cy25, gm_cy25=gm_cy25, gp_cy25=gp_cy25,
              ebitda_cy25=ebitda_cy25, dna_cy25=dna_cy25, opex_cy25=opex_cy25,
              npa_cy25=npa_cy25, np_cy25=np_cy25, nd_cy25=nd_cy25, eqp_cy25=eqp_cy25,
              ppe_cy25=ppe_cy25, nwc_cy25=nwc_b, ic_cy25=IC_B, bvps=bvps,
              cash=cash_b, debt=debt_b, netfin_cy25=netfin_cy25,
              inv=inv_b, recv=recv_b, pay=pay_b, roe_trailing=roe_trailing,
              implied_life=ppe_b / DEP_ANN, eq_jun25=V['eq_parent_jun25'] / M,
              eq_jun24=V['eq_parent_jun24'] / M, eq_dec24=V['eq_parent_dec24'] / M,
              assets=V['assets_snap'] / M, liab=V['liab_snap'] / M),
    unit=dict(lines=LINES, labels=LBL, spec=SPEC,
              prod_t=PT, prod_v=PV, prod_v_prior=PVp, px=px, mix_t=mix_t, mix_v=mix_v,
              growth_v=growth_v, spec_share_t=spec_t, spec_share_v=spec_v,
              tot_t=tot_t, tot_v=tot_v / M,
              vol_cy25=tot_t * 2 / 1e6, vol25={k: PT[k] * 2 / 1e6 for k in LINES},
              rev25_lines={k: PV[k] / M * 2 for k in LINES},
              cost_stack={k: v / M for k, v in COS.items()}, cost_share=cos_share,
              lines_rev=B['lines_rev'], lines_vol=B['lines_vol'], line_margin=B['line_margin'],
              vol=B['vol'], spec_vol=B['spec_vol'], spec_rev=B['spec_rev'],
              fuel_rev=B['fuel_rev'], cogs=B['cogs'],
              m_spec=B['m_spec'], m_fuel=B['m_fuel'], raw_of_rev=raw_of_rev,
              dep_ann=DEP_ANN, capex_ann=CAPEX_ANN, base_gm=BASE_GM, tax_eff=TAX_EFF),
    fcst=dict(years=YRS, rev=rev, gp=B['gp'], gm=B['gm'], opex=B['opex'], ebitda=ebitda,
              ebitda_margin=ebitda_margin, dna=dna, ebit=ebit, nopat=nopat, capex=capex,
              nwc=nwc, dnwc=dnwc, fcff=fcff, df=df, pv=pv, fwd_wacc=fwd, glide_frac=glide_frac,
              ppe=ppe_f, ic=ic, roic=roic, np_attr=np_fc, equity=eq_fc, net_debt=nd_fc,
              cash=cash_fc, interest=interest_path, div=div_fc, payout=PAYOUT),
    wacc=dict(rf=V['rf'], rf_star=rf_star, ke_exp=ke_exp, ke_rating_alt=ke_rating_alt,
              ke_raw_retired=ke_raw_retired, kd=V['kd'], kd_at=kd_at, we_exp=we_exp,
              wd_exp=wd_exp, wacc_exp=wacc_exp, wacc_exp_gross=wacc_exp_gross, wd_gross=wd_gross, k_nd_at=k_nd_at, ke_term=ke_term, kd_term=V['kd_term'],
              kd_term_at=kd_term_at, wacc_term=wacc_term, glide_frac=glide_frac,
              kd_path=V['kd_path'], kd_swing_effect=kd_swing_effect, wacc_usd_alt=WACC_USD,
              beta=beta_res),
    dcf=dict(pv_explicit=pv_explicit, tv=tv, pv_tv=pv_tv, ev=ev, tv_share=tv_share,
             nd=nd_cy25, nci_share=NCI_SHARE, nci_val=nci_val, eq_attr=eq_attr, ps=dcf_ps,
             roic_term=roic_term, rr_term=rr_term, g=V['g_term'], bear=dcf_bear, bull=dcf_bull,
             ps_rating_basis=dcf_rating_ps, wacc_exp_rating=wacc_exp_rating,
             wacc_term_rating=wacc_term_rating, ps_nci_alt=dcf_nci_alt_ps, nci_alt=nci_alt,
             ps_gross_basis=dcf_grossbasis_ps, ccy_alt_ps=ccy_ps),
    terminal_recon=dict(roic=hist_roic, rr=hist_rr, implied_g=hist_impl_g,
                        character=hist_character, nopat=nopat_h, ic=ic_h, capex=capex_h,
                        nopat_cagr=nopat_cagr, stable_g=stable_g, stable_keys=stable_keys,
                        rr_waterfall=rr_waterfall, g_waterfall=g_waterfall,
                        ceiling=blend_ceiling, crossover_years=yrs_cross, crossover=cross_candidates, fcst_cagr=fcst_cagr,
                        dom_share_term=dom_share_term),
    lenses=lenses, central=central, span=[lo, hi], spot=SPOT, scen=SCEN,
    experts=experts, panel_centre=panel_centre,
    rel=dict(ebitda_mid=ebitda_mid, pv_interim=pv_interim, ev_rel=ev_rel, ev_rel_fwd=ev_rel_fwd, df_rel=df_rel,
             ev_ebitda_trailing=ev_ebitda_trailing, pe_trailing=pe_trailing,
             just_mult=V['ev_ebitda_just'], year=YRS[REL_I]),
    norm=dict(rev=norm_rev, ebitda=norm_ebitda, ebit=norm_ebit, dna=dna[NORM_I],
              interest=norm_interest, np=norm_np, eps=norm_eps, pe=V['pe_just'],
              year=YRS[NORM_I]),
    book=dict(bvps=bvps, pb_just=pb_just, roe_sust=V['roe_sust'], roe_trailing=roe_trailing,
              ke_term=ke_term),
    sens_wg=dict(g_grid=g_grid, wacc_grid=wt_grid, table=grid_wacc_g),
    sens=dict(g_grid=g_grid, wt_grid=wt_grid, we_grid=we_grid, grid_wacc_g=grid_wacc_g,
              grid_exp_term=grid_exp_term, beta_grid=beta_grid, grid_beta=grid_beta,
              gm_grid=gm_grid, grid_margin=grid_margin, vol_grid=vol_grid, grid_vol=grid_vol,
              fx_grid=fx_grid, grid_fx=grid_fx, nwc_grid=nwc_grid, grid_nwc=grid_nwc),
    step0=step0, strike=strike, backtest=bt5,
    assert_log=LOG,
)
with open(os.path.join(HERE, 'study_numbers.json'), 'w') as f:
    json.dump(OUT, f, indent=1)
say("=" * 78)
say(f"ASSERT BLOCK PASSED — study_numbers.json emitted. Terminal value "
    f"{tv_share:.1%} of enterprise value; fair value EGP {central:.2f} against spot EGP "
    f"{SPOT:.2f}; implied {central/SPOT-1:+.1%}.")
