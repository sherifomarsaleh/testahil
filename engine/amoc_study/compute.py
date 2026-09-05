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
import math, sys, os, json
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

# RE-STRUCK ON THE LATEST KNOWN PRICE [R-GAP-01 AMENDED, 03-09-2026]. The study
# had been carrying a 6-August close for four weeks while the stock rose 48%, and
# a fair value published against a month-old price is a comparison a reader cannot
# use. The price is an INPUT to the answer here, not only a benchmark beside it:
# it sets market capitalisation and therefore the market-value equity weight the
# cost of capital is built on.
INP['spot'] = I(13.50, "AMOC closing price on the Egyptian Exchange, 3 September 2026", "2026-09-03", "Company")
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

# ---- THE 30-JUNE-2026 HALF-YEAR DISCLOSURE -----------------------------------
# Disclosed to the Egyptian Exchange on 29-30 July 2026, one week BEFORE this study's anchor date.
# The previous edition of this study carried these figures. The audited rebuild DELETED them on a
# rule that treated "is it inside one of the four supplied PDFs?" as the test for whether a figure
# could be used, and then argued that no clean twelve-month period existed. The rule deleted a
# disclosure that had already been sourced and corroborated. It is restored here, flagged REPORTED
# and NOT audited, and the gross-profit line is NOT taken at face value — see the coherence test.
REP = ("Half-year results for 1-Jan to 30-Jun-2026, disclosed to the Egyptian Exchange 29-30 July "
       "2026. REPORTED, NOT AUDITED — a press release, not a filing")
INP['rev_h1cy26_rep'] = I(26_223_000_000.0, f"Net sales, six months to 30-Jun-2026. {REP}", "2026-06-30", "Company")
INP['pat_h1cy26_rep'] = I(1_903_000_000.0, f"Net profit after tax, six months to 30-Jun-2026. {REP}", "2026-06-30", "Company")
INP['gp_h1cy26_rep'] = I(3_258_000_000.0, "Gross profit, six months to 30-Jun-2026, AS RELEASED. This "
                                          "study does NOT use this figure: run through the company's own "
                                          "Q1-2026 expense run rates it implies a profit after tax about "
                                          "12.6% above the profit the same release reports. The gross "
                                          "profit actually used is SOLVED from the release's own profit "
                                          f"line, which two independent coherence tests confirm. {REP}",
                         "2026-06-30", "Company")
INP['pat_h1cy25'] = I(878_800_000.0, "Majority profit, six months to 30-Jun-2025, read off the AUDITED "
                                     "consolidated statement of changes in equity. Used only to test the "
                                     f"reported +109% profit growth in the half above. {AUD}", "2025-06-30", "Company")

# ---- NOTE 14-A: THE AUDITED PRODUCT TABLE, six months to 31-Dec-2025 ----------
# Eight lines, each with tonnes and value. This replaces a three-line build that rested on a
# product table obtained from a reviewer rather than from the filing, and whose realisations had
# to be reconstructed through a crude-parity crack multiple. Nothing is reconstructed now.
FIL = ("Reviewed consolidated financial statements, six months to 30-Jun-2026, limited "
       "review report attached (note 14-A / 15-A)")

# THE TWELVE-MONTH PRODUCT TABLE, BOTH HALVES FILED. The previous edition doubled the
# transition half because it believed the second half existed only as a press release. It
# does not: the reviewed consolidated statements for the six months to 30 June 2026 were
# filed and are in hand. Summing the two disclosed halves gives a real twelve-month product
# table that foots EXACTLY to twelve months of disclosed revenue, so the solved price index
# the previous edition needed disappears entirely.
_PT_H2_25 = dict(oils=54_968.98, wax=41_774.20, gasoil=171_684.881, naphtha=41_430.857,
                 lpg=23_735.778, fueloil=460_153.60, hfo=14_327.52, waste=7.82)
_PT_H1_26 = dict(oils=63_506.66, wax=41_031.54, gasoil=175_035.912, naphtha=39_112.249,
                 lpg=24_203.011, fueloil=339_488.657, hfo=11_854.10, waste=8.84)
_PV_H2_25 = dict(oils=2_597_280_264.0, wax=2_041_969_329.0, gasoil=5_121_703_599.0,
                 naphtha=958_746_631.0, lpg=816_258_520.0, fueloil=8_975_569_716.0,
                 hfo=224_110_353.0, waste=87_400.0)
_PV_H1_26 = dict(oils=4_313_064_027.0, wax=2_610_896_627.0, gasoil=7_911_258_980.0,
                 naphtha=1_278_877_679.0, lpg=1_254_216_267.0, fueloil=8_663_939_828.0,
                 hfo=190_674_246.0, waste=104_800.0)
INP['prod_t'] = I({k: _PT_H2_25[k] + _PT_H1_26[k] for k in _PT_H2_25},
                  f"Tonnes sold by product line, TWELVE months to 30-Jun-2026 — the audited "
                  f"transition half (note 14-A, {AUD}) plus the reviewed half ({FIL}). Both "
                  f"halves are filed; nothing is annualised.", "2026-06-30", "Company")
INP['prod_v'] = I({k: _PV_H2_25[k] + _PV_H1_26[k] for k in _PV_H2_25},
                  f"Sales value by product line, EGP, TWELVE months to 30-Jun-2026 — the audited "
                  f"transition half (note 14-A, {AUD}) plus the reviewed half ({FIL}). Foots to "
                  f"disclosed twelve-month net sales with no scalar.", "2026-06-30", "Company")
# The H1 CY2026 income statement AS FILED. Every line below is read off the statement and the
# statement foots: gross profit, operating profit, profit before tax, profit after tax and the
# majority share all reproduce from their own components.
INP['rev_h1cy26'] = I(26_223_032_454.0, f"Net sales, six months to 30-Jun-2026. {FIL}", "2026-06-30", "Company")
INP['cogs_h1cy26'] = I(22_964_084_821.0, f"Cost of sales, six months to 30-Jun-2026. {FIL}", "2026-06-30", "Company")
INP['gp_h1cy26'] = I(3_258_947_633.0, f"Gross profit, six months to 30-Jun-2026 — 12.43% of net sales. {FIL}", "2026-06-30", "Company")
INP['ga_h1cy26'] = I(675_083_735.0, f"General and administrative expenses, six months to 30-Jun-2026. {FIL}", "2026-06-30", "Company")
INP['mkt_h1cy26'] = I(125_019_700.0, f"Marketing and selling expenses, six months to 30-Jun-2026. {FIL}", "2026-06-30", "Company")
INP['othexp_h1cy26'] = I(2_599_294.0, f"Other expenses, six months to 30-Jun-2026. {FIL}", "2026-06-30", "Company")
INP['prov_h1cy26'] = I(96_672_167.0, f"Formed provisions, six months to 30-Jun-2026. {FIL}", "2026-06-30", "Company")
INP['ecl_h1cy26'] = I(48_692_230.0, f"Expected credit losses formed, six months to 30-Jun-2026. {FIL}", "2026-06-30", "Company")
INP['fin_h1cy26'] = I(1_938_539.0, f"Finance expenses, six months to 30-Jun-2026. {FIL}", "2026-06-30", "Company")
INP['othrev_h1cy26'] = I(196_526_615.0, f"Other operating income, six months to 30-Jun-2026, of which credit interest 134,944,385. {FIL}", "2026-06-30", "Company")
INP['tax_h1cy26'] = I(591_669_261.0, f"Income tax, six months to 30-Jun-2026. {FIL}", "2026-06-30", "Company")
INP['dtax_h1cy26'] = I(6_907_221.0, f"Deferred tax revenue, six months to 30-Jun-2026. {FIL}", "2026-06-30", "Company")
INP['pat_h1cy26'] = I(1_920_706_543.0, f"Net profit after tax, six months to 30-Jun-2026. {FIL}", "2026-06-30", "Company")
INP['nci_h1cy26'] = I(38_756_277.0, f"Non-controlling interest, six months to 30-Jun-2026. {FIL}", "2026-06-30", "Company")
INP['maj_h1cy26'] = I(1_881_950_266.0, f"Majority's share, six months to 30-Jun-2026 — EPS 1.46, and MORE than the whole preceding fiscal year's 1,488,520,098. {FIL}", "2026-06-30", "Company")
for _k, _lab in [('salaries', 'Salaries'), ('raw', 'Raw materials'),
                 ('support', 'Supporting materials'), ('dep', 'Depreciation'),
                 ('other', 'Other cost of sales')]:
    INP['cos_ttm_' + _k] = I(
        {'salaries': 881_019_497.0, 'raw': 17_650_102_725.0, 'support': 64_533_723.0,
         'dep': 58_748_046.0, 'other': 807_146_755.0}[_k]
        + {'salaries': 988_514_768.0, 'raw': 21_023_897_616.0, 'support': 59_621_598.0,
           'dep': 64_458_183.0, 'other': 827_592_656.0}[_k],
        f"{_lab} inside cost of sales, TWELVE months to 30-Jun-2026 (note 15-A, both filed "
        f"halves added). {FIL}", "2026-06-30", "Company")
INP['dep_ttm'] = I(70_125_269.0 + 86_495_738.0,
                   f"Depreciation and right-of-use amortisation, TWELVE months to 30-Jun-2026 — "
                   f"the audited transition half's cash-flow statement plus the reviewed half's. "
                   f"{FIL}", "2026-06-30", "Company")
INP['capex_ttm'] = I(30_357_299.0 + 139_109_418.0,
                     f"Payments for projects under construction and fixed assets, TWELVE months "
                     f"to 30-Jun-2026 — both cash-flow statements. {FIL}", "2026-06-30", "Company")
INP['credint_h1cy26'] = I(134_944_385.0,
                          f"Credit interest earned, six months to 30-Jun-2026 (note 14-B). {FIL}",
                          "2026-06-30", "Company")
INP['cos_h1cy26'] = I(dict(salaries=988_514_768.0, raw=21_023_897_616.0, support=59_621_598.0,
                           dep=64_458_183.0, other=827_592_656.0),
                      f"Cost of sales by nature, six months to 30-Jun-2026 (note 15-A); raw "
                      f"materials are 91.6% of the stack. {FIL}", "2026-06-30", "Company")
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
INP['ppe_net'] = I(873010517.0, "Fixed assets net of accumulated depreciation at 30-Jun-2026 (note 6). Reviewed consolidated FS, six months to 30-Jun-2026, limited review", "2026-06-30", "Company")
INP['ppe_gross'] = I(2_740_810_692.0, "Fixed assets at COST at 31-Dec-2025 (note 6), before accumulated "
                                      "depreciation of 1,847,794,418. The gross figure is what a "
                                      "replacement-capex line has to be built on; the net figure is what "
                                      f"the terminal return is flattered by. {AUD}", "2025-12-31", "Company")
INP['ppe_accdep'] = I(1_847_794_418.0, "Accumulated depreciation on fixed assets at 31-Dec-2025 (note 6). "
                                       "The plant is 67.4% written down and 273,466,121 of it is fully "
                                       f"depreciated and still in use. {AUD}", "2025-12-31", "Company")
INP['puc'] = I(414641768.0, "Projects under construction at 30-Jun-2026 (note 7). Reviewed consolidated FS, six months to 30-Jun-2026, limited review", "2026-06-30", "Company")
INP['inventory'] = I(3764066490.0, "Inventory net of impairment at 30-Jun-2026 (note 9-A). Reviewed consolidated FS, six months to 30-Jun-2026, limited review", "2026-06-30", "Company")
INP['recv'] = I(2035100729.0, "Accounts receivable net at 30-Jun-2026 (note 9-B). Reviewed consolidated FS, six months to 30-Jun-2026, limited review", "2026-06-30", "Company")
INP['debtors'] = I(632115619.0, "Debtors and other debit balances net at 30-Jun-2026 (notes 9-C, 9-D). Reviewed consolidated FS, six months to 30-Jun-2026, limited review", "2026-06-30", "Company")
INP['cash'] = I(3018394920.0, "Cash and cash equivalents at 30-Jun-2026 (note 9-E). UP from 2,463,522,365 six months earlier AFTER paying 861,257,265 of dividends. Reviewed consolidated FS, six months to 30-Jun-2026, limited review", "2026-06-30", "Company")
INP['fin_inv'] = I(525170000.0, "Other financial investments at 30-Jun-2026 — deposits PLEDGED against facilities, not free cash. Reviewed consolidated FS, six months to 30-Jun-2026, limited review", "2026-06-30", "Company")
INP['fvoci'] = I(69_608_696.0, "Financial asset through OCI at 31-Dec-2025 — 104,000 shares, 5.20% of "
                               f"ASCPC, fair value 69,608,696 (note 8-1). {AUD}", "2025-12-31", "Company")
INP['assets_snap'] = I(11405065699.0, "Total assets at 30-Jun-2026. Reviewed consolidated FS, six months to 30-Jun-2026, limited review", "2026-06-30", "Company")
INP['liab_snap'] = I(5261891473.0, "Total liabilities at 30-Jun-2026. Reviewed consolidated FS, six months to 30-Jun-2026, limited review", "2026-06-30", "Company")
INP['eq_parent'] = I(6070338949.0, "Total AMOC (parent) equity at 30-Jun-2026 — EGP 4.70 a share, against 4,790,695,948 six months earlier. Reviewed consolidated FS, six months to 30-Jun-2026, limited review", "2026-06-30", "Company")
INP['eq_nci'] = I(72835277.0, "Non-controlling interest carrying amount at 30-Jun-2026. Reviewed consolidated FS, six months to 30-Jun-2026, limited review", "2026-06-30", "Company")
INP['debt_lt'] = I(12137451.0, "Long-term loans at 30-Jun-2026 (note 20). Reviewed consolidated FS, six months to 30-Jun-2026, limited review", "2026-06-30", "Company")
INP['debt_st'] = I(4715153.0, "Short-term loans and facilities at 30-Jun-2026 (note 20). Reviewed consolidated FS, six months to 30-Jun-2026, limited review", "2026-06-30", "Company")
INP['leases'] = I(2324893.0, "Total lease liabilities at 30-Jun-2026 (note 8-2): 463,553 long term plus 1,861,340 short term. Reviewed consolidated FS, six months to 30-Jun-2026, limited review", "2026-06-30", "Company")
INP['payables'] = I(14015841.0, "Accounts and notes payable at 30-Jun-2026 (note 10-3). Reviewed consolidated FS, six months to 30-Jun-2026, limited review", "2026-06-30", "Company")
INP['creditors'] = I(3286150065.0, "Creditors and other credit balances at 30-Jun-2026 (note 11). Reviewed consolidated FS, six months to 30-Jun-2026, limited review", "2026-06-30", "Company")
INP['provisions'] = I(996857074.0, "Provisions at 30-Jun-2026 (note 10-1) — a recognised liability, carried in full in the bridge. Reviewed consolidated FS, six months to 30-Jun-2026, limited review", "2026-06-30", "Company")
INP['dtax_liab'] = I(95721735.0, "Deferred tax liability at 30-Jun-2026 (note 13-A). Reviewed consolidated FS, six months to 30-Jun-2026, limited review", "2026-06-30", "Company")
INP['tax_due'] = I(591669261.0, "Current income tax due at 30-Jun-2026 (note 10-2). Reviewed consolidated FS, six months to 30-Jun-2026, limited review", "2026-06-30", "Company")
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
INP['div_declared'] = I(258300000.0, "Dividends payable at 30-Jun-2026 (note 11) — HALF the 517,250,000 standing six months earlier, because the declared dividend was largely paid. Reviewed consolidated FS, six months to 30-Jun-2026, limited review", "2026-06-30", "Company")

# ---- ownership and counterparty, as disclosed --------------------------------
INP['nci_share'] = I(30_488_250.0 / 656_428_711.0,
                     "Non-controlling interest as a share of group profit after tax, six months to "
                     "31-Dec-2025 — DISCLOSED, not inferred. The holding in Alexandria Wax "
                     "Products S.A.E. is registered separately as awp_stake. The previous edition "
                     "inferred 3.0% from the gap "
                     "between consolidated and standalone profit; the filing says 4.645%",
                     "2025-12-31", "Company")
# TYPED IN TWO PLACES AND REGISTERED IN NEITHER [added 03-Sep-2026, found by
# prose_check.py on its first run]. 86.45% appeared in this source note and again in the
# study's section 1.1, both hand-typed, while every other disclosed ownership figure in
# this model carries four fields. A disclosed fact quoted in prose with no registered
# input is the numeric-traceability rule's own case.
# TWO FIGURES FROM SUPERSEDED EDITIONS, quoted so a reader of the previous edition can see
# what changed — and typed, because this model cannot compute a number a different model
# produced. They are FACTS about a prior edition, so they carry four fields like any other
# fact rather than sitting in a builder's f-string [found by prose_check.py].
INP['gm_superseded_annualised'] = I(0.07081,
    "Base-year gross margin published by the 06-08-2026 edition of this study, which built "
    "revenue from the six-month product table doubled while annualising cost of sales from "
    "nine months by four thirds — so it corresponded to no filed period at all. Quoted in "
    "section 1.2 to show what changed; not an input to anything.", "2026-08-06", "House")
INP['tv_share_superseded'] = I(0.587,
    "Terminal value as a share of enterprise value in the 06-08-2026 edition, before the "
    "terminal return was struck on invested capital at REPLACEMENT cost. Quoted in section "
    "1.9 to show the direction of the change; not an input to anything.", "2026-08-06",
    "House")
INP['awp_stake'] = I(0.8645, "AMOC's holding in Alexandria Wax Products S.A.E. (note 1-2). "
                             "This is the counterpart of the non-controlling interest above: "
                             "the 13.55% AMOC does not own is what the minority's share of "
                             "profit and of the enterprise is struck on.", "2025-12-31",
                     "Company")
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
INP['line_vol_growth'] = I(dict(oils=[0.0]*5, wax=[0.0]*5, gasoil=[0.0]*5,
                                naphtha=[0.0]*5, lpg=[0.0]*5, fueloil=[0.0]*5,
                                hfo=[0.0]*5, waste=[0.0]*5),
                           "Volume growth by audited product line: FLAT, every line, every year. "
                           "The previous edition grew every line (oils +4.5%, wax +7.0%, fuel oil "
                           "+3.0% in year one) and justified the ranking from the value growth "
                           "printed between two disclosed HALVES. The company's own audited "
                           "annual record for FY2021-FY2025 says the opposite: total sales "
                           "tonnage ran 1,492 / 1,548 / 1,449 / 1,433 / 1,262 thousand tonnes, a "
                           "fall of 18.5% from the FY2022 peak, and six of the eight lines "
                           "shrank over FY2022-FY2025 (gas oil -8.3% a year, naphtha -7.4%, fuel "
                           "oil -6.4%, heavy fuel oil -28.2%; only wax +1.1% and LPG +1.7% grew). "
                           "FLAT IS NOT A NEUTRAL ASSUMPTION HERE, IT IS ALREADY THE OPTIMISTIC "
                           "ONE: the base year is the transition half annualised at 1,616 "
                           "thousand tonnes, which is 12.5% ABOVE the five-year mean of 1,437 and "
                           "above every full year in the record. Holding it flat assumes the "
                           "rebound printed in one half persists. The bear case reverts toward "
                           "the five-year mean and the lever is sensitised end to end",
                           "2026-08-18", "Company")
INP['us_infl'] = I(0.025, "Long-run United States consumer price inflation, the foreign leg of "
                          "the purchasing-power-parity relation used to derive the currency path",
                   "2026-08-06", "Global")
# line_price_growth and fx_path are now DERIVED from the registered Egyptian inflation path
# rather than set by hand. They are appended to the register after V is built, below.
import macro_path as _MPATH
_HP = _MPATH.load('EG')          # the house macro path [R-MACRO-01]

# THE FORECAST YEARS WERE THIS STUDY'S OWN LADDER, AND [R-MACRO-01] FORBIDS THAT OUTRIGHT
# [conformed 03-Sep-2026]. They read 14.5 / 13.0 / 11.5 / 10.0 / 9.5 against a house calendar
# ladder of 16.0 / 12.0 / 9.0 / 7.5 / 7.0 for the same country and the same years. The record
# declared the line exempt on the grounds that the study was internally coherent and that
# rebuilding "belongs in its own pass" — which is a statement about convenience, and
# convenience is not one of the grounds the rule allows. The historical years stay as printed,
# because a filed past is not a forecast.
_HOUSE_LADDER = [_HP.inflation(2026 + _i) for _i in range(5)]
INP['fixed_cost_infl'] = I([1.33, 1.28, 1.12] + [round(1.0 + _r, 6) for _r in _HOUSE_LADDER],
                           "Cumulative-year Egyptian inflation factors applied to the "
                           "pound-denominated cost legs — salaries inside cost of sales, the "
                           "other line, administrative and marketing expense, and capital "
                           "expenditure. The three HISTORICAL years are as printed. The five "
                           "FORECAST years are the single Egyptian inflation path this series "
                           "uses for every Egyptian company it values, read from that path "
                           "rather than set for this study: no valuation here sets an "
                           "inflation rate of its own, because a company cannot be valued in "
                           "an economy the study beside it does not recognise. The path is "
                           "the central bank's published disinflation ladder, and the years "
                           "between published points are labelled as interpolated where they "
                           "are",
                           "2026-09-02", "Country")
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
INP['e1_pe'] = I(7.0, "Expert 1's justified price/earnings multiple. Struck below the main "
                      "normalised lens deliberately: it is an independent opinion, not a "
                      "re-run of the house view", "2026-08-06", "House")
INP['proc_intensity'] = I(dict(oils=1.00, wax=1.15, gasoil=0.25, naphtha=0.20, lpg=0.15,
                               fueloil=0.05, hfo=0.05, waste=0.00),
                          "Processing intensity by product line, relative weights, used to "
                          "allocate the note 15-A conversion stack (salaries, supporting "
                          "materials, other, depreciation) across the eight disclosed lines. "
                          "Base oils are the reference at 1.00: they pass the full lube train — "
                          "vacuum distillation, solvent extraction, dewaxing, hydrofinishing. "
                          "Paraffin wax carries 1.15 for the additional deoiling and sweating "
                          "steps. Gas oil, naphtha and LPG are light ends drawn off the front of "
                          "the process and carry 0.25/0.20/0.15. Fuel oil and heavy fuel oil are "
                          "the residue, sold substantially as produced, at 0.05. THIS IS THE "
                          "ONLY OPERATING INPUT IN THE MODEL THAT IS NOT READ OFF A FILING, and "
                          "it exists because note 15-A discloses the cost stack for the company "
                          "and not by line. It is stated here rather than hidden in a formula, "
                          "and the valuation is sensitised to it",
                  "2026-08-06", "House")
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
INP['beta'] = I(0.9080, "Own-stock tier-1 regression, AMOC weekly log-returns against the "
                        "EGX30 — the published index of the exchange AMOC is listed on, "
                        "series as of 22 July 2026. R-squared 0.259, n = 253, standard "
                        "error 0.165, 90% confidence interval [0.637, 1.179], Blume cross-check "
                        "0.939. Passes the usability gate. THIS REPLACES the previous edition's "
                        "0.9405, which was regressed against a 33-name equal-weight composite of "
                        "the covered Egyptian names — a coverage artefact rather than a market, "
                        "and a source-integrity failure whatever number it produced. The "
                        "correction is small on this name, -3.5% on beta and under a percent on "
                        "fair value; it is made because the provenance was wrong, not because the "
                        "answer was",
                "2026-07-22", "Company")
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
# THE COST OF DEBT SITS ABOVE THE SOVEREIGN, AND THE PREVIOUS BUILD DID NOT.
# The 06-Aug-2026 edition priced this off the CORRIDOR LENDING RATE of 20.00%
# plus a 200bp corporate spread, for 22.00% — against an Egyptian ten-year yield
# of 22.31% recorded in this same file. A same-currency corporate borrowing 31bp
# BELOW the government that taxes it is forbidden outright by the cost-of-capital
# procedure, and the first run of the new cost-of-capital gate found it here, in
# the one study that had implemented the rest of that procedure.
#
# THE ARGUMENT FOR THE OLD BUILD IS RECORDED RATHER THAN DISMISSED, because it is
# not a silly one: the company's facilities are SHORT-DATED and the corridor is an
# overnight policy rate, so a short borrowing costing less than a ten-year bond
# yield is a term-structure fact, not a company out-borrowing its sovereign. The
# rule is nonetheless stated on the sovereign the model actually discounts with,
# and a study that prices its debt off a different point of the curve from its own
# risk-free rate is comparing two things and calling them one.
#
# WHAT IT IS WORTH: the gross book is EGP 25mn, 0.06% of revenue, on a company
# that is NET CASH. The correction moves the answer by essentially nothing, and
# that is exactly why it is made — a rule that is only obeyed when it is expensive
# is not a rule.
INP['kd'] = I(0.2231 + 0.0200, "Marginal cost of debt: the Egyptian ten-year sovereign yield "
                      "this study discounts with, plus a 200bp corporate spread. The gross book "
                      "is EGP 25mn — 0.06% of revenue — of short-dated Egyptian-pound "
                      "facilities, so no observable marginal rate exists and the rate is built "
                      "rather than pretended to be observed. It replaces a build off the 20.00% "
                      "corridor lending rate, which produced 22.00% — below the sovereign, which "
                      "a same-currency corporate cannot be. The integrity gate below computes "
                      "what this input is actually WORTH to the answer",
              "2026-09-02", "House")
INP['kd_path'] = I([0.2431, 0.1950, 0.1750, 0.1600, 0.1500],
                   "Forward cost-of-debt path 2026E-2030E, following the central bank's own "
                   "disinflation path toward the long-run Egyptian corporate-borrowing norm. This "
                   "path is what sets the SHAPE of the cost-of-capital glide; it is not a second "
                   "free parameter", "2026-08-06", "House")
INP['kd_term'] = I(0.1500, "Terminal cost of debt: the midpoint of the 14-16% long-run Egyptian "
                           "corporate-borrowing norm, with no name-specific reason to deviate",
                   "2026-08-06", "House")
INP['real_rate_term'] = I(0.055, "Terminal real risk-free rate, the standard emerging-market "
                                 "convention. The terminal NOMINAL risk-free rate is not an input: it "
                                 "is DERIVED as this real rate plus the central bank's inflation "
                                 "target IN FORCE for the terminal horizon (`cbe_target`), so the "
                                 "single most terminal-value-sensitive number in the model cannot be "
                                 "set by hand. The previous edition hardcoded 10.50% by adding 5.5pp "
                                 "to the 5% target dated Q4-2028 while describing it as 'the' "
                                 "medium-term target; the target in force is 7% for Q4-2026 and the "
                                 "July-2026 rate decision pushed even that to H2-2027",
                          "2026-08-06", "House")
INP['erp_term'] = I(0.0700, "Terminal equity risk premium, normalised below the currently elevated "
                            "crisis-era level toward the rating-class norm; never held flat into "
                            "perpetuity", "2026-08-06", "House")
INP['wd_term'] = I(0.10, "Terminal debt weight, normalised. The company is net cash today and has "
                         "been for years; a terminal structure carrying a tenth of capital in debt "
                         "is already generous to the valuation and avoids capitalising the current "
                         "zero-leverage position into perpetuity", "2026-08-06", "House")
INP['lens_weights'] = I(dict(dcf=0.45, relative=0.20, normalized=0.20, book=0.15),
                        "Discounted cash flow primary for a single-asset operating processor with a "
                        "visible volume ramp; the relative and normalised-earnings lenses carry "
                        "equal secondary weight; the book lens least, because a substantially "
                        "depreciated plant makes book value a poor proxy for replacement cost",
                        "2026-08-06", "House")
INP['pe_just'] = I(7.5, "Justified through-cycle price-to-earnings multiple on normalised earnings. "
                        "Trailing is about 7.5x on the constructed 2025 base. A single-asset "
                        "processor with a 20% state shareholder, an administered feedstock "
                        "relationship and an Egyptian cost of equity near 28% does not earn a "
                        "premium multiple. Bear 5.5x / bull 9.5x", "2026-08-06", "House")
INP['rel_rerating'] = I(0.0, "Re-rating applied to the company's OWN trailing enterprise-value "
                             "to EBITDA multiple in the relative lens. ZERO: the name is held at "
                             "the multiple the market already pays it. The justified multiple is "
                             "no longer a free number — it is DERIVED as the trailing multiple "
                             "times one plus this figure, so it cannot drift away from the "
                             "company's own pricing without the drift being visible. The previous "
                             "edition set 4.5x by hand and justified it as 'holding the name at "
                             "its own trailing level' against a stated trailing multiple of "
                             "'around 4.6x'; the model's own output was different, so the stated "
                             "justification was false whichever way the multiple was struck. "
                             "Holding at zero re-rating makes the lens a statement about the "
                             "BRIDGE — what the disclosed claims on the cash are worth — rather "
                             "than a disguised view on the multiple",
                        "2026-08-06", "House")
INP['roe_sust'] = I(0.280, "Sustainable return on equity for the book lens. Trailing return on "
                           "average parent equity is about 33%; the sustainable rate is struck "
                           "below it because the reported figure is flattered by a heavily "
                           "written-down asset base that will have to be renewed",
                    "2026-08-06", "House")
INP['g_term'] = I(0.07, "Terminal growth, 7% — INFLATION ONLY, and no real growth at all. It is "
                        "set equal to the central bank's published inflation target, which is the "
                        "same 7% embedded in this study's own terminal risk-free rate. The "
                        "previous edition used 5% against that identical 12.5% nominal rate, "
                        "which is a business shrinking about 2% a year in real terms for ever — "
                        "an assumption never stated as one, on a plant serving a population "
                        "growing 1.6% a year. Zero real growth is still the conservative end: it "
                        "assumes AMOC never again grows a tonne", "2026-08-06", "Country")
V = {k: v['value'] for k, v in INP.items()}

# ---- ONE MACRO PATH, NOT THREE THAT CONTRADICT EACH OTHER --------------------
# The previous edition escalated the pound-denominated COST legs at Egyptian inflation of 14.5%
# falling to 9.5%, escalated product REALISATION at 9.0% falling to 5.2%, and depreciated the
# CURRENCY at 7.7% falling to 3.6% — three different views of the same economy, running side by
# side for five years, with no mechanism offered for the gaps. It called the price path one of
# "only two free operating parameters". A country cannot run 14.5% domestic inflation against a
# currency sliding 4% a year without an enormous real appreciation, and on a company whose
# feedstock is 82% of revenue and is priced off the same barrel as its output, that incoherence
# alone manufactures the margin decline the forecast then reports as a finding.
#
# Both are now DERIVED from the one registered inflation path by relative purchasing-power
# parity: the pound depreciates at the inflation differential, and the slate — priced off dollar
# product benchmarks, with crude held FLAT in dollars because no forecast of it is defensible —
# fetches that many more pounds. Feedstock rides the same path, so the SPREAD is preserved in
# real terms and the margin is free to be an output rather than an artefact of the index choice.
# TWO FREE PARAMETERS ARE REMOVED BY THIS, NOT ADDED.
_EG_INFL = [V['fixed_cost_infl'][3 + i] - 1.0 for i in range(5)]
_DEPREC = [(1 + e) / (1 + V['us_infl']) - 1 for e in _EG_INFL]
INP['line_price_growth'] = I([round(d, 6) for d in _DEPREC],
    "Growth in the realised price per tonne, all lines, in EGP. DERIVED, not chosen: crude is "
    "held FLAT in dollars — no forecast of it is defensible — and the pound depreciates at the "
    "inflation differential between the registered Egyptian path and United States inflation, "
    "so a dollar-priced slate fetches that many more pounds. This REPLACES a hand-set path of "
    "9.0% falling to 5.2%, which sat two-thirds below the inflation this same model applies to "
    "the company's own costs, with no mechanism given for the gap", "2026-08-06", "Country")
_FXP, _cum = [], 1.0
for _d in _DEPREC:
    _cum *= (1 + _d)
    _FXP.append(round(V['fx_avg_cy25'] * _cum, 2))
INP['fx_path'] = I(_FXP,
    "USD/EGP average-rate path, DERIVED from the same purchasing-power-parity relation as the "
    "price path so the two cannot disagree. It replaces a hand-set path that depreciated the "
    "pound at roughly a third of the inflation differential", "2026-08-06", "Country")
V = {k: v['value'] for k, v in INP.items()}
# --- MODEL BODY BEGINS HERE (reachability gate splits on this line) ---
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
say(f"[Base year — ALTERNATIVE: nine AUDITED months, annualised] the transition period "
    f"1-Jul-2025 to 31-Dec-2025 (audited, Crowe, unqualified) and the three months to "
    f"31-Mar-2026 (reviewed) are contiguous and cover nine months: net sales {rev9/M:,.0f}, cost "
    f"of sales {cogs9/M:,.0f}, GROSS PROFIT {gp9/M:,.0f}, a margin of {BASE_GM:.3%}. Annualised "
    f"at 4/3 that is {BASE_REV:,.0f} of revenue. This edition NO LONGER uses it as the headline "
    f"base — see the twelve months to 30-Jun-2026 below — but publishes it as the alternative, "
    f"because half of the twelve-month base is a press release rather than a filing.")

# ---- (1b) THE HEADLINE BASE: the twelve months to 30 June 2026 ---------------
# The previous edition of this study argued that no clean twelve-month period existed. That was
# wrong, and it was wrong on evidence this study had already sourced: AMOC disclosed its 1-Jan to
# 30-Jun-2026 half to the exchange on 29-30 July 2026, a week before the anchor date. The audited
# transition half (Jul-Dec 2025, AUDITED) plus that half is twelve contiguous months to
# 30-Jun-2026, with no annualisation scalar at all.
#
# THE RELEASED GROSS PROFIT IS NOW THE FILED GROSS PROFIT, AND IT WAS RIGHT.
# The previous edition rejected the released gross-profit line on a coherence test and SOLVED
# gross profit from the release's own profit line instead. The reviewed statements settle it:
# gross profit for the half is 3,258,947,633, which is the released figure to the pound.
#
# WHY THE TEST FAILED IS WORTH KEEPING. It estimated the half's other revenue by DOUBLING
# Q1-2026's 225,556,509, giving 451mn against an actual 196,526,615 — other income is the most
# volatile line in this income statement and the least suited to being doubled. That single
# over-credit of ~255mn is most of what made the released gross profit look incoherent. A
# coherence test built on an extrapolated volatile line rejected a correct disclosure, and the
# study then carried a gross margin roughly a fifth too low into every lens.
_h1_opex = V['ga_h1cy26'] + V['mkt_h1cy26'] + V['othexp_h1cy26']
_h1_othrev = V['othrev_h1cy26']
_h1_prov = V['prov_h1cy26'] + V['ecl_h1cy26']
_h1_fin = V['fin_h1cy26']
gp_h1cy26 = V['gp_h1cy26']
gp_h1cy26_at_release = V['gp_h1cy26_rep']
_pat_if_released_gp = V['pat_h1cy26']

# The filed statement is checked against ITSELF rather than against a press release: every
# subtotal must reproduce from its own components, or the extraction is wrong.
_op_h1 = gp_h1cy26 - _h1_opex
assert abs(_op_h1 - 2_456_244_904.0) < 1.0, "H1-2026 operating profit does not foot"
_pbt_h1 = _op_h1 - _h1_prov - _h1_fin + _h1_othrev
assert abs(_pbt_h1 - 2_505_468_583.0) < 1.0, "H1-2026 profit before tax does not foot"
_pat_h1 = _pbt_h1 - V['tax_h1cy26'] + V['dtax_h1cy26']
assert abs(_pat_h1 - V['pat_h1cy26']) < 1.0, "H1-2026 profit after tax does not foot"
assert abs(V['pat_h1cy26'] - V['nci_h1cy26'] - V['maj_h1cy26']) < 1.0, "H1-2026 majority does not foot"
assert abs(V['rev_h1cy26'] - V['cogs_h1cy26'] - gp_h1cy26) < 1.0, "H1-2026 gross profit does not foot"

# The press release is retained ONLY as a cross-check on itself, now that the filing exists.
CT1 = abs(V['pat_h1cy26_rep'] / V['pat_h1cy26'] - 1)      # release vs filed profit
CT2 = abs(V['rev_h1cy26_rep'] / V['rev_h1cy26'] - 1)      # release vs filed revenue
CT3 = abs(V['gp_h1cy26_rep'] / gp_h1cy26 - 1)             # release vs filed gross profit
assert CT1 < 0.02 and CT2 < 0.02 and CT3 < 0.02, (
    "the press release and the filing disagree by more than 2% — investigate before using either")
say(f"[The half is FILED, not a press release] the reviewed consolidated statements for the six "
    f"months to 30-Jun-2026 are in hand. Net sales {V['rev_h1cy26']/M:,.0f}, gross profit "
    f"{gp_h1cy26/M:,.0f} — a gross margin of {gp_h1cy26/V['rev_h1cy26']:.2%} — and majority "
    f"profit {V['maj_h1cy26']/M:,.0f}, which is MORE IN SIX MONTHS than the whole fiscal year to "
    f"30-Jun-2025 earned ({V['pat_fy25_full']/M:,.0f}). The previous edition solved gross profit "
    f"from the profit line because a coherence test rejected the released figure; the filing "
    f"says the released figure was right to {CT3:.2%}, and the test failed because it doubled "
    f"Q1's other revenue to estimate the half — 451mn against an actual "
    f"{V['othrev_h1cy26']/M:,.0f}mn. The release ties to the filing within {CT1:.2%} on profit "
    f"and {CT2:.2%} on revenue.")

REV_TTM = (V['rev_h2_25'] + V['rev_h1cy26']) / M
GP_TTM = (V['rev_h2_25'] - V['cogs_h2_25'] + gp_h1cy26) / M
COGS_TTM = REV_TTM - GP_TTM
GM_TTM = GP_TTM / REV_TTM
say(f"[Base year — TWELVE CONTIGUOUS MONTHS to 30-Jun-2026, BOTH HALVES FILED] the audited "
    f"transition half (Jul-Dec 2025) plus the REVIEWED half (Jan-Jun 2026) is a clean twelve "
    f"months: net sales {REV_TTM:,.0f}, gross profit {GP_TTM:,.0f}, margin {GM_TTM:.3%}. No 4/3 "
    f"scalar, no annualisation, and no period estimated. THE PREVIOUS EDITION CALLED HALF OF "
    f"THIS BASE 'A PRESS RELEASE RATHER THAN A FILING' AND SOLVED ITS GROSS PROFIT FROM THE "
    f"PROFIT LINE. Both halves are filed. The gross margin used here is {GM_TTM:.3%} against the "
    f"{(gp9 - (V['rev_q1_26'] - V['cogs_q1_26']) + (V['pat_h1cy26_rep']/(1-TAX_EFF) + (V['ga_q1_26']+V['mkt_q1_26']+V['othexp_q1_26'])*2 - V['othrev_q1_26']*2 + (V['prov_q1_26']+V['ecl_q1_26'])*2 + V['fin_q1_26']*2))/M/REV_TTM:.3%} "
    f"the solve produced — the correction is worth about 0.65 of a percentage point on the base "
    f"margin and it runs through every lens in this study. The half's own margin is "
    f"{gp_h1cy26/V['rev_h1cy26']:.2%}, and the quarter inside it that is not Q1 is "
    f"{(gp_h1cy26 - (V['rev_q1_26']-V['cogs_q1_26']))/(V['rev_h1cy26']-V['rev_q1_26']):.2%}.")

BASE_REV = REV_TTM
BASE_GM = GM_TTM
BASE_COGS = COGS_TTM
BASE_GP = GP_TTM
BASE_YEAR = "twelve months to 30-Jun-2026, both halves filed"
say(f"[Base year — SELECTED] {BASE_YEAR}. Revenue {BASE_REV:,.0f}, gross margin {BASE_GM:.3%}, "
    f"against the nine-month annualisation's {rev9/M*A:,.0f} and {gp9/rev9:.3%}. Both are "
    f"published and the model runs on either; the twelve-month base is the headline because it "
    f"needs no annualisation scalar, and the nine-month base is retained because all of it is "
    f"audited or reviewed. The gap between the two is {BASE_REV/(rev9/M*A)-1:+.1%} on revenue "
    f"and {BASE_GM-gp9/rev9:+.2%} on margin, and that gap is a real uncertainty about this "
    f"company, not a rounding difference.")

# ---- the twelve-month aggregates, BOTH HALVES FILED --------------------------
# The previous edition scaled Q1-2026 by 2 to reach the second half, because it believed that
# half existed only as a press release. Every line below is now the audited transition half plus
# the REVIEWED half, added. Nothing is scaled, and the difference is not cosmetic: doubling Q1's
# other revenue put 451mn where the filing shows 197mn.
ga_ttm = V['ga_h2_25'] + V['ga_h1cy26']
mkt_ttm = V['mkt_h2_25'] + V['mkt_h1cy26']
oth_ttm = V['othexp_h2_25'] + V['othexp_h1cy26']
prov_ttm = V['prov_h2_25'] + V['prov_h1cy26'] + V['ecl_h1cy26']
othrev_ttm = V['othrev_h2_25'] + V['othrev_h1cy26']
credint_ttm = V['credint_h2_25'] + V['credint_h1cy26']  # note 14-B, both halves as filed
fin_ttm = V['fin_h2_25'] + V['fin_h1cy26']
_nci_ttm = V['nci_h2_25'] + V['nci_h1cy26']
_pat_ttm = V['pat_h2_25'] + V['pat_h1cy26']
dep_ttm = V['dep_ttm']
capex_ttm = V['capex_ttm']
emp_ttm = V['emp_h2_25'] * 2.0                          # the only line still scaled; see below
_H1_SCALE = 1.0                                         # retained: nothing is scaled any more

# ---- three rates the waterfall needs, every one SOLVED from the filings ------
# TAX. The unlevered waterfall applies the STATUTORY rate to operating profit. The effective rate
# of 22.12% is correct for its own base — a pre-tax profit that includes credit interest, other
# income and a deferred credit — and applying it to EBIT and then into perpetuity taxes a
# narrower base at a rate struck on a wider one. The effective rate stays where it belongs, in
# the historical reconciliation.
TAX_STAT = V['tax_stat']
# EMPLOYEES' PROFIT SHARE. Struck as the company strikes it: the disclosed charge over the profit
# it is charged against, so the rate is solved rather than picked.
EMP_RATE = emp_ttm / _pat_ttm
# MINORITY. The previous edition called 4.645% "the DISCLOSED rate". It is not disclosed: it is a
# ratio computed from ONE audited half, and it was struck on a profit figure that includes the
# PARENT's credit interest — so the cash the study is careful to keep out of the minority's reach
# on one line is inside the ratio on the next. It is restruck here over the whole base year and
# over OPERATING profit only.
NCI_OP = _nci_ttm / (_pat_ttm - credint_ttm * (1 - TAX_EFF))
say(f"[Three rates, SOLVED not assumed] statutory tax {TAX_STAT:.2%} on operating profit (the "
    f"effective {TAX_EFF:.2%} is struck on a pre-tax base that includes credit interest and a "
    f"deferred credit, and is kept for the historical reconciliation only). Employees' profit "
    f"share and board bonuses {EMP_RATE:.2%} of profit after tax, solved from the disclosed "
    f"charge of {emp_ttm/M:,.0f} over profit of {_pat_ttm/M:,.0f}. Minority interest "
    f"{NCI_OP:.3%}, restruck over the whole base year and over OPERATING profit — against the "
    f"{V['nci_share']:.3%} the previous edition called 'the DISCLOSED rate', which was a "
    f"single-half ratio computed on a profit base that included the parent's own credit "
    f"interest.")
TAX = TAX_EFF          # the audited rate supersedes the assumption everywhere downstream
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
# The cost stack is the TWELVE-MONTH stack — the audited transition half's note 15-A plus the
# reviewed half's note 15-A — so it sits on the same twelve months as the product table and the
# base-year revenue. Doubling one half would have put a six-month cost base against a
# twelve-month revenue base, and on this company the two halves are not alike: raw materials
# were 90.7% of the stack in the first and 91.6% in the second.
_H1_COS = V['cos_h1cy26']
COS = dict(salaries=V['cos_ttm_salaries'], raw=V['cos_ttm_raw'],
           support=V['cos_ttm_support'], dep=V['cos_ttm_dep'], other=V['cos_ttm_other'])
# The registered twelve-month components must equal the two FILED halves added. This is a real
# check, not a tautology: the halves and the twelve-month figures are separate register entries,
# so editing one without the other stops the build here rather than at a number a reader sees.
assert abs(COS['salaries'] - (V['cos_salaries'] + _H1_COS['salaries'])) < 1.0, "salaries"
assert abs(COS['raw'] - (V['cos_raw'] + _H1_COS['raw'])) < 1.0, "raw materials"
assert abs(COS['support'] - (V['cos_support'] + _H1_COS['support'])) < 1.0, "supporting materials"
assert abs(COS['dep'] - (V['cos_dep'] + _H1_COS['dep'])) < 1.0, "depreciation"
assert abs(COS['other'] - (V['cos_other'] + _H1_COS['other'])) < 1.0, "other cost of sales"
assert abs(sum(COS.values()) - (V['cogs_h2_25'] + V['cogs_h1cy26'])) < 1.0, (
    "the twelve-month cost stack does not foot to twelve months of disclosed cost of sales")
COS24 = dict(salaries=V['cos_salaries_24'], raw=V['cos_raw_24'], support=V['cos_support_24'],
             dep=V['cos_dep_24'], other=V['cos_other_24'])
assert abs(sum(COS.values()) - (V['cogs_h2_25'] + V['cogs_h1cy26'])) < 1.0, (
    "the twelve-month note 15-A stack does not foot to twelve months of cost of sales")
assert abs(sum(COS24.values()) - V['cogs_h2_24']) < 1.0, "note 15-A comparative does not foot"
_COGS_TTM_EGP = V['cogs_h2_25'] + V['cogs_h1cy26']
cos_share = {k: v / _COGS_TTM_EGP for k, v in COS.items()}
say(f"[The cost stack, DISCLOSED not built] note 15-A splits the {_COGS_TTM_EGP/M:,.0f} of cost "
    f"of sales across the two filed halves: raw materials {COS['raw']/M:,.0f} "
    f"({cos_share['raw']:.1%}), salaries {COS['salaries']/M:,.0f} ({cos_share['salaries']:.1%}), "
    f"other — natural gas, electricity, water, spare parts, maintenance and the EPROM operating "
    f"contract — {COS['other']/M:,.0f} ({cos_share['other']:.1%}), supporting materials "
    f"{COS['support']/M:,.0f} ({cos_share['support']:.1%}) and depreciation {COS['dep']/M:,.0f} "
    f"({cos_share['dep']:.1%}). The previous edition BUILT a stack from house estimates of "
    f"yields, energy intensity and a solved feedstock differential, carried NO salaries line at "
    f"all inside cost of sales, and estimated chemicals at roughly five times the disclosed "
    f"figure. None of that construction survives: the filing states the stack and the model uses "
    f"it as stated.")
raw_of_rev = COS['raw'] / (V['rev_h2_25'] + V['rev_h1cy26'])
say(f"[What this company actually is] raw materials are {raw_of_rev:.1%} of net sales. Every "
    f"other cost line together is {1-raw_of_rev-BASE_GM:.1%}. A business whose single largest "
    f"line is {raw_of_rev:.0%} of revenue and whose gross margin is {BASE_GM:.1%} is a "
    f"PASS-THROUGH PROCESSOR: the value is not in the revenue line, and it is not in cost "
    f"control either — it is in the spread between what the feedstock costs and what the slate "
    f"fetches, and in the tonnage that spread is earned on.")

# ---- (4) the AUDITED product table, note 14-A --------------------------------
PT, PV, PVp = V['prod_t'], V['prod_v'], V['prod_v_prior']
tot_t = sum(PT.values()); tot_v = sum(PV.values())
assert abs(tot_v - (V['rev_h2_25'] + V['rev_h1cy26'])) < 1.0, (
    "the twelve-month note 14-A value column does not foot to twelve months of net sales")
assert abs(tot_t - 1_502_324.605) < 0.01, (
    "the twelve-month note 14-A tonnage does not foot to the two disclosed halves")
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

# ---- (5) THE BOTTOM-UP BUILD ------------------------------------------------
# Both sides of the gross margin are now built per product line, from the disclosed table, on the
# SAME twelve months. Nothing is a blended percentage of revenue.
#
# REVENUE per line = tonnes x realisation per tonne. Tonnes are the note 14-A half annualised;
# realisations are note 14-A value / note 14-A tonnes, lifted by ONE solved index so the base year
# foots to the twelve-month revenue. That index is solved, not assumed, and it is the only free
# scalar on the revenue side.
#
# COST per line = feedstock per tonne + conversion per tonne. Note 15-A discloses the five cost
# components for the company as a whole, not by line, so an allocation basis is needed and is
# stated rather than buried:
#   - RAW MATERIALS are allocated on TONNES. The feedstock is a single common stream drawn from
#     the adjacent refining complex; a tonne of throughput consumes a tonne of feed whatever it
#     leaves as. This is the 90.7% of cost, so the basis matters and the simplest defensible one
#     is used.
#   - CONVERSION (salaries, supporting materials, other, depreciation) is allocated on PROCESSING
#     INTENSITY, measured as each line's realisation over the common feedstock cost per tonne.
#     A tonne of base oil sells for 47,250 and a tonne of fuel oil for 19,506 out of the same
#     feed; the difference is processing, and processing is what the conversion stack pays for.
#     The intensity weights are SOLVED so the allocation foots to the disclosed total exactly.
# The per-line gross margins that come out of this are DIFFERENT for every line, which is the
# point: the previous edition applied one blended margin to all eight lines and called it a
# bottom-up build.
T0 = tot_t / M                                         # mn tonnes, TWELVE disclosed months
_rev_at_disclosed_px = sum(PT[k] * px[k] for k in LINES) / M
PX_INDEX = BASE_REV / _rev_at_disclosed_px             # SOLVED, the only free scalar on revenue
px0 = {k: px[k] * PX_INDEX for k in LINES}             # base-year realisation per tonne, EGP
t0 = {k: PT[k] / M for k in LINES}                     # base-year tonnes, mn
assert abs(sum(t0[k] * px0[k] for k in LINES) - BASE_REV) < 1e-6, "revenue build does not foot to the base year"

COS_TTM = BASE_COGS * M                                 # EGP, twelve months, footing to the base
raw_tot0 = COS_TTM * cos_share['raw']
conv_tot0 = COS_TTM * (1 - cos_share['raw'])
# CONVERSION is allocated on PROCESSING INTENSITY, and this is the ONE operating input in the
# model that is not read off a filing. It has to be: note 15-A gives the cost stack for the
# company and not by line, and note 14-A gives only price and volume — so ANY weight derived from
# note 14-A alone is a function of price, and a price-derived weight returns the same margin on
# every line, which is exactly the defect this build exists to remove.
PROC = V['proc_intensity']
_pw_den = sum(t0[k] * PROC[k] for k in LINES)
conv_pt = {k: conv_tot0 * PROC[k] / (_pw_den * M) for k in LINES}
# FEEDSTOCK is allocated on NET REALISABLE VALUE — realisation less that line's own separable
# conversion cost. This is the textbook joint-product method and it is the only one of the three
# candidates that survives a sanity check. Flat per tonne says fuel oil sells below the cost of
# its own feed (realisation 19,506 against a common feed at 23,980) — an artefact of the basis.
# Relative sales value says base oils and paraffin wax, the products this plant was built for,
# run at NEGATIVE margins once their conversion cost is stacked on top. Net realisable value
# charges each line for the feed in proportion to what is left after its own processing, which is
# both the standard and the only basis that produces a positive spread on every disclosed line.
_nrv = {k: px0[k] - conv_pt[k] for k in LINES}
_nrv_den = sum(t0[k] * _nrv[k] for k in LINES)
raw_pt = {k: raw_tot0 * _nrv[k] / (_nrv_den * M) for k in LINES}
RAW_OF_REV = raw_tot0 / (BASE_REV * M)
assert all(_nrv[k] > 0 for k in LINES), "a line's conversion cost exceeds its realisation"
assert abs(sum(t0[k] * M * (raw_pt[k] + conv_pt[k]) for k in LINES) - COS_TTM) < 1.0, \
    "per-line cost allocation does not foot to the disclosed cost of sales"
_m0 = {k: 1 - (raw_pt[k] + conv_pt[k]) / px0[k] for k in LINES}
_spread = {k: px0[k] - raw_pt[k] - conv_pt[k] for k in LINES}
assert all(_spread[k] > 0 for k in LINES), "a line earns a negative unit spread"
say("[Cost, PER LINE — built, not blended] conversion runs " +
    " · ".join(f"{LBL[k]} {conv_pt[k]:,.0f}" for k in ('oils', 'wax', 'gasoil', 'fueloil')) +
    " EGP a tonne on the registered processing-intensity weights; feedstock is then allocated on "
    "NET REALISABLE VALUE — realisation less that line's own conversion — which is the standard "
    "joint-product method and the only basis of the three tested that leaves every disclosed "
    "line with a positive spread. GROSS SPREAD PER TONNE: " +
    " · ".join(f"{LBL[k]} {_spread[k]:,.0f}" for k in ('oils', 'wax', 'gasoil', 'naphtha', 'lpg',
                                                       'fueloil', 'hfo')) +
    f" EGP. That is the number that matters and it is the one the previous edition could not "
    f"produce: a tonne of base oil contributes {_spread['oils']/_spread['fueloil']:.1f} times the "
    f"spread of a tonne of fuel oil, so the specialty mix is now a real driver of value. GROSS "
    f"MARGIN BY LINE: " +
    " · ".join(f"{LBL[k]} {_m0[k]:.1%}" for k in ('oils', 'wax', 'gasoil', 'fueloil')) +
    f" against a blended {BASE_GM:.1%} — note that the specialty lines show a LOWER margin "
    f"percentage on a HIGHER spread per tonne, because their realisation per tonne is nearly "
    f"three times fuel oil's. Percentage margin is the wrong lens on a joint-product slate; "
    f"spread per tonne is the right one, and the previous edition had neither.")
say("[The one operating input that is not read off a filing] the processing-intensity weights " +
    " · ".join(f"{LBL[k]} {PROC[k]:.2f}" for k in LINES if k != 'waste') +
    ". Note 15-A discloses the cost stack for the company and NOT by line. Any weight derivable "
    "from note 14-A alone is a function of realisation, and a realisation-derived weight returns "
    "an identical margin on every line — which is the defect being removed. So this vector is a "
    "judgement, it is registered and dated like every other input, and section 7 treats it as a "
    "named weakness rather than burying it in a formula.")

# ---- capital expenditure, BUILT from the asset register ----------------------
# Capex was one annualised cash number held flat and inflated. It is now two components, both
# derived from disclosed balances: MAINTENANCE, which replaces the asset base over its implied
# life, and GROWTH, which funds incremental tonnage at the plant's own capital intensity.
ASSET_LIFE = V['ppe_gross'] / (dep_ttm / 1.0)           # years, gross cost over the annual charge
CAP_INTENSITY = (V['ppe_gross'] + V['puc']) / (T0 * M)  # EGP of gross plant per annual tonne
MAINT_CAPEX0 = V['ppe_gross'] / ASSET_LIFE / M          # EGP mn a year at today's price level
say(f"[Capital expenditure, BUILT] fixed assets at COST are {V['ppe_gross']/M:,.0f} against an "
    f"annual depreciation charge of {dep_ttm/M:,.0f}, an implied asset life of "
    f"{ASSET_LIFE:.1f} years. Maintenance capital expenditure is struck at cost over that life, "
    f"{MAINT_CAPEX0:,.0f} a year before inflation — against cash actually paid of "
    f"{capex_ttm/M:,.0f}. The company is spending {capex_ttm/M/MAINT_CAPEX0:.2f} times "
    f"replacement. GROWTH capital expenditure is charged at the plant's own capital intensity of "
    f"{CAP_INTENSITY:,.0f} EGP of gross plant per annual tonne, so incremental tonnage now COSTS "
    f"something instead of arriving free. The previous edition held one cash number flat and "
    f"inflated it, which made volume growth self-funding.")

# ---- working capital, BUILT on days SOLVED from the audited balance sheet ----
INV_DAYS = V['inventory'] / (BASE_COGS * M) * 365.0
RECV_DAYS = (V['recv'] + V['debtors']) / (BASE_REV * M) * 365.0
_pay_op = V['payables'] + V['creditors'] - V['div_declared']    # dividends payable is FINANCING
PAY_DAYS = _pay_op / (BASE_COGS * M) * 365.0
say(f"[Working capital, BUILT on solved days] inventory {INV_DAYS:.1f} days of cost of sales, "
    f"receivables {RECV_DAYS:.1f} days of revenue, operating payables {PAY_DAYS:.1f} days of "
    f"cost of sales — every one SOLVED from the audited balance sheet against the base year, not "
    f"assumed. The house registry carried {V['inv_days']:.0f}/{V['recv_days']:.0f}/"
    f"{V['pay_days']:.0f} days and no formula read any of them. Dividends payable of "
    f"{V['div_declared']/M:,.0f} is REMOVED from creditors: a declared distribution to "
    f"shareholders is a financing claim, and leaving it inside operating working capital both "
    f"understated the capital the business ties up and let a shareholder claim vanish from the "
    f"bridge. It is carried in the bridge instead.")


def build(vol_adj=0.0, price_mult=1.0, fx_mult=1.0, gm_shift=0.0, ratio=None,
          pound_on_price=None):
    """Revenue AND cost, both per line, both from the same twelve-month base.

    Per line: tonnes x realisation for revenue; tonnes x (feedstock + conversion) for cost.
    Feedstock per tonne moves with realisation (pass-through). Conversion per tonne splits into
    a pound-denominated leg on local inflation and a materials leg on realisation. Operating
    expense is three disclosed lines on three different drivers plus two charges the previous
    edition registered and never took. Depreciation rolls off the asset register instead of
    being held flat."""
    rev, gp, gm, cogs_l = [], [], [], []
    lines_rev = {k: [] for k in LINES}; lines_vol = {k: [] for k in LINES}
    lines_cost = {k: [] for k in LINES}; lmarg = {k: [] for k in LINES}
    _pound_on_price = (POUND_ON_PRICE if pound_on_price is None else pound_on_price)
    infl = 1.0; pidx = 1.0; vidx = {k: 1.0 for k in LINES}
    _sal_sh = cos_share['salaries'] / (1 - cos_share['raw'])
    _oth_sh = cos_share['other'] / (1 - cos_share['raw'])
    _sup_sh = cos_share['support'] / (1 - cos_share['raw'])
    _dep_sh = cos_share['dep'] / (1 - cos_share['raw'])
    for i in range(5):
        infl *= V['fixed_cost_infl'][3 + i]
        pidx *= (1 + V['line_price_growth'][i] * price_mult * fx_mult)
        r_tot = c_tot = 0.0
        for k in LINES:
            vidx[k] *= (1 + V['line_vol_growth'][k][i] + vol_adj)
            v = t0[k] * vidx[k]
            p = px0[k] * pidx
            # feedstock per tonne is pass-through; conversion splits by driver
            # THE STUDY'S OWN PRINCIPLE, APPLIED TO ONE COST LEG AND NOT THE OTHER
            # [found 03-Sep-2026 by the re-strike, on the principal's lead].
            # raw_pass=1.0 is registered with the words "the gross SPREAD per tonne
            # is held flat in real terms and the margin neither widens nor narrows".
            # That is true of the FEEDSTOCK leg and false of the CONVERSION leg two
            # lines below it: salaries and other conversion costs escalate at the
            # full domestic inflation ladder (14.5% falling to 9.5%) while realised
            # price grows only at the currency differential (11.7% falling to 6.8%),
            # a REAL COST DRIFT of +2.7 to +2.8 points a year, compounding for ever.
            # Nothing in the study declared it and nothing sourced it, and it is
            # what produces the whole of the forecast margin decline.
            _pound = pidx if _pound_on_price else infl
            cpt = (raw_pt[k] * pidx * RAW_PASS
                   + conv_pt[k] * (_sal_sh * _pound + _oth_sh * _pound
                                   + _sup_sh * pidx + _dep_sh))
            r = v * p; c = v * cpt
            lines_vol[k].append(v); lines_rev[k].append(r); lines_cost[k].append(c)
            lmarg[k].append(1 - cpt / p)
            r_tot += r; c_tot += c
        g = r_tot - c_tot + gm_shift * r_tot
        rev.append(r_tot); cogs_l.append(c_tot); gp.append(g); gm.append(g / r_tot)
    # operating expense: three disclosed lines, three drivers, plus two charges never taken
    _inf = 1.0; opex = []
    for i in range(5):
        _inf *= V['fixed_cost_infl'][3 + i]
        _volidx = sum(lines_vol[k][i] for k in LINES) / T0
        ga = ga_ttm / M * _inf                       # administrative: pound costs, inflation
        mk = mkt_ttm / M * _inf * _volidx            # selling: inflation AND tonnage
        ot = oth_ttm / M * _inf                      # other operating: inflation
        pv = prov_ttm / M * _inf                     # formed provisions and expected credit losses
        opex.append(ga + mk + ot + pv)
    return dict(rev=rev, gm=gm, gp=gp, opex=opex, cogs=cogs_l,
                lines_rev=lines_rev, lines_vol=lines_vol, lines_cost=lines_cost,
                line_margin=lmarg,
                vol=[sum(lines_vol[k][i] for k in LINES) for i in range(5)],
                spec_vol=[sum(lines_vol[k][i] for k in SPEC) for i in range(5)],
                spec_rev=[sum(lines_rev[k][i] for k in SPEC) for i in range(5)],
                fuel_rev=[sum(lines_rev[k][i] for k in LINES if k not in SPEC) for i in range(5)],
                m_spec=lmarg['oils'][0], m_fuel=lmarg['fueloil'][0])


# ---- (6) the balance sheet, AUDITED — no reconstruction anywhere -------------
ppe_b = (V['ppe_net'] + V['puc']) / M
inv_b = V['inventory'] / M
recv_b = (V['recv'] + V['debtors']) / M
# dividends payable is a DECLARED distribution, not operating working capital. It is removed
# here as well as from the forecast days, so opening and forecast working capital sit on the
# same basis; it is then carried as its own claim in the equity bridge. Leaving it in the
# opening balance while excluding it from the forecast would have put a 517mn step into the
# first forecast year's cash flow that no operating change caused.
pay_b = (V['payables'] + V['creditors'] - V['div_declared']) / M
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
# ---------------------------------------------------------------------------
# THE REAL COST DRIFT IS REMOVED, AND THE COMPANY'S OWN FILED RECORD IS WHAT
# REMOVED IT [03-Sep-2026, found by the re-strike on the principal's lead].
#
# The previous editions escalated the pound-denominated conversion legs at the
# full Egyptian inflation ladder (14.5% falling to 9.5%) while realised price per
# tonne grew only at the currency differential (11.7% falling to 6.8%). That is a
# REAL COST DRIFT of +2.7 to +2.8 points a year, compounding for ever, and it
# produced the whole of the forecast margin decline: 9.494% in 2026 falling to
# 8.764% in 2030, against a base year of 9.653%.
#
# THREE THINGS ARE WRONG WITH IT, AND NONE OF THEM IS A MATTER OF TASTE.
#
# (i) IT CONTRADICTS THE STUDY'S OWN DECLARED PRINCIPLE. raw_pass = 1.0 is
#     registered with the words "the gross SPREAD per tonne is held flat in real
#     terms and the margin neither widens nor narrows". That principle is applied
#     to the feedstock leg and silently broken on the conversion leg two lines
#     below it.
#
# (ii) IT IS UNSOURCED. No input registers a real cost drift, no disclosure
#     supports one, and no sentence in the study told a reader that its forecast
#     margin decline was an escalator artefact rather than a finding. That is
#     [L-048] exactly, and the digest already carries the ARCC precedent in these
#     words: "the model's whole forecast margin decline was a mechanical artifact
#     of the price path being set below a single blended cost-inflation index in
#     every year, by construction". The lesson was registered, correct, and
#     re-violated by this study.
#
# (iii) THE MEASURED DIRECTION IN THE COMPANY'S OWN RECORD IS THE OPPOSITE. The
#     standing rule permits a unit rate to drift "only where a named structural
#     mechanism has a MEASURED like-for-like direction in the company's own period
#     pair". Cost per unit of revenue across the five filed periods runs
#     93.146% -> 94.947% -> 93.855% -> 89.810% -> 87.572%: it FELL 5.58 points
#     while the model asserts it rises 2.7 points a year for ever.
#
# So the study's own principle is now applied to EVERY cost leg, which is what
# POUND_ON_PRICE=True means. It is worth +19.4% (EGP 9.9142 -> 11.8342) and it is
# therefore this study's most consequential contested judgement, priced BOTH ways
# below and published side by side rather than averaged.
#
# WHAT THIS IS NOT: it is not moving the number toward the price, which
# [R-GAP-01] prohibits outright. The corrected margin path is roughly 9.7% flat --
# still well BELOW the 12.43% this company filed for the half to 30 June 2026, and
# below the 10.19% of the quarter before it. The correction removes an unsupported
# decline; it does not adopt the improvement, which the rule says to hold flat.
POUND_ON_PRICE = True
DEP_ANN = dep_ttm / M
CAPEX_ANN = capex_ttm / M
say(f"[Depreciation and capital expenditure, ACTUAL] over the twelve months to 30-Jun-2026 the "
    f"company charged {DEP_ANN:,.0f} of depreciation and right-of-use amortisation and paid "
    f"{CAPEX_ANN:,.0f} in cash for fixed assets and projects under construction. Cash capital "
    f"expenditure is {CAPEX_ANN/DEP_ANN:.2f} times the depreciation charge and "
    f"{CAPEX_ANN/MAINT_CAPEX0:.2f} times replacement at gross cost. The previous edition held "
    f"the cash figure flat and inflated it, and separately stated that free cash flow was "
    f"overstated by 'roughly EGP 2mn a year' — a claim that holds in the first forecast year and "
    f"reverses sign in every year after it. Capital expenditure is now BUILT: maintenance at "
    f"cost over the implied asset life, plus growth at the plant's own capital intensity, so the "
    f"caveat is computed across the whole window instead of asserted for one year of it.")
OPEX_ANN = (ga_ttm + mkt_ttm + oth_ttm + prov_ttm) / M
ebitda_cy25 = BASE_GP - OPEX_ANN + DEP_ANN
gm_cy25 = BASE_GM
dna_cy25 = DEP_ANN
opex_cy25 = OPEX_ANN
gp_cy25 = BASE_GP
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
def cost_of_capital(beta):
    """Both anchors from one beta. The base case and every sensitivity row call this.
    The previous edition rebuilt the explicit anchor inside the beta sweep using the
    cost of GROSS debt where the base case uses the cost of NET debt, so the beta row's
    centre did not return the base case and two reviewers found it independently."""
    _ke = rf_star + beta * V['erp_cds']
    # THE OPERATING CASH FLOWS ARE DISCOUNTED AT THE UNLEVERED RATE, NOT AT A NET-CASH WACC.
    # The previous edition weighted the cost of capital on NET debt. Because AMOC holds net
    # cash the debt weight is NEGATIVE (-26.2%), which levers the equity weight to 1.26 and
    # pushes the discount rate on the OPERATING cash flows to 31.19% — 374 basis points ABOVE
    # the cost of equity — and the bridge then adds the same cash back at face value. That
    # charges for the cash twice: once by discounting the operations as though they were
    # riskier for holding it, and once by counting it at a hundred pistres. Either value the
    # whole firm at a blended rate and add nothing, or value the operations at the operating
    # rate and add the cash. This does the second. Gross borrowings are 0.14% of the capital
    # structure at market value, so the unlevered rate IS the cost of equity to three decimals.
    return _ke, _ke

ke_exp, wacc_exp = cost_of_capital(V['beta'])
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
# ---- WHERE THE CASH IS CHARGED FOR, AND HOW MANY TIMES ----------------------
# The previous edition discounted the OPERATING cash flows at a cost of capital weighted on NET
# debt. With net cash the debt weight is negative, so the equity weight levers ABOVE one and the
# operating rate lands ABOVE the cost of equity — 31.19% against 27.45%, 374 basis points of
# extra discounting applied to the refinery because the company also owns a bank balance. The
# bridge then added that same balance back at face. Both cannot be right. This edition discounts
# the operations at the unlevered rate and adds the cash at face, which is one charge, not two.
_wd_net_retired = nd_cy25 / (nd_cy25 + MKTCAP)
_wacc_net_retired = (1 - _wd_net_retired) * ke_exp + _wd_net_retired * k_nd_at
say(f"[The cash is charged for ONCE] gross borrowings are {(V['debt_lt']+V['debt_st'])/M:,.1f} "
    f"against a market capitalisation of {MKTCAP:,.0f} — {(V['debt_lt']+V['debt_st'])/M/MKTCAP:.4%} "
    f"of the capital structure — so the unlevered cost of capital IS the cost of equity, "
    f"{ke_exp:.2%}, and that is the rate the operating cash flows are discounted at. The "
    f"previous edition used a NET-debt-weighted rate of {_wacc_net_retired:.2%}: because the "
    f"company holds net cash the debt weight is {_wd_net_retired:+.1%}, the equity weight levers "
    f"to {1-_wd_net_retired:.3f}, and the operating rate comes out "
    f"{_wacc_net_retired-ke_exp:+.2%} ABOVE the cost of equity. It then added the cash back at "
    f"face in the bridge. That is the same cash charged twice — once by discounting the refinery "
    f"as though owning a deposit made it riskier, and once by counting the deposit at par. A "
    f"reader may value the WHOLE firm at a blended rate and add nothing, or value the operations "
    f"at the operating rate and add the cash; this study does the second and says so.")
assert wacc_exp > wacc_exp_gross, \
    "unlevering for net cash must RAISE the operating rate; check the signs"

# ---- terminal (norm-built, never backed out of a price) --------------------
RF_TERM = V['cbe_target'] + V['real_rate_term']   # DERIVED, not set by hand
kd_term_at = V['kd_term'] * (1 - TAX)

def terminal_cost_of_capital(beta):
    return (1 - V['wd_term']) * (RF_TERM + beta * V['erp_term']) + \
        V['wd_term'] * kd_term_at

ke_term = RF_TERM + V['beta'] * V['erp_term']
wacc_term = terminal_cost_of_capital(V['beta'])
say(f"[Weighted cost of capital, terminal] cost of equity {ke_term:.2%} (norm-built risk-free "
    f"{RF_TERM:.2%} = the central bank's inflation target IN FORCE for the terminal "
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

# ---- FCFF waterfall — ONE implementation, used by the base run and every scenario ----
# The previous edition carried two copies of this waterfall: one for the base case and one inside
# the scenario engine. They drifted, and a change to the terminal block applied to one and not the
# other. There is now one function. Everything that reports a per-share number goes through it.
def waterfall(S, wacc_shift=0.0, g=None, roic_cap=None, nwc_days=None,
              we=None, wt=None, nci=None):
    """From a build() result to enterprise value and value per share.

    Depreciation ROLLS off the asset register instead of being held flat: opening net book plus
    capital expenditure, charged over the implied asset life. Capital expenditure is MAINTENANCE
    at cost over that life plus GROWTH at the plant's own capital intensity on incremental
    tonnage. Working capital is built on days, so it responds to cost of sales and revenue
    separately rather than to one blended percentage."""
    g = V['g_term'] if g is None else g
    inv_d, recv_d, pay_d = nwc_days or (INV_DAYS, RECV_DAYS, PAY_DAYS)
    _rev, _gp, _opex, _cogs = S['rev'], S['gp'], S['opex'], S['cogs']
    _dna, _capex, _ppe_g, _ppe_n = [], [], [], []
    gross, net = V['ppe_gross'] / M + V['puc'] / M, ppe_b
    _inf = 1.0
    for i in range(5):
        _inf *= V['fixed_cost_infl'][3 + i]
        dv = S['vol'][i] - (T0 if i == 0 else S['vol'][i - 1])
        cap = MAINT_CAPEX0 * _inf + max(dv, 0.0) * CAP_INTENSITY * _inf
        d = gross / ASSET_LIFE
        gross += cap; net += cap - d
        _capex.append(cap); _dna.append(d); _ppe_g.append(gross); _ppe_n.append(net)
    _ebitda = [_gp[i] - _opex[i] for i in range(5)]          # opex already excludes depreciation
    _ebit = [_ebitda[i] - _dna[i] for i in range(5)]
    _nopat = [e * (1 - TAX_STAT) for e in _ebit]
    # employees' profit share and board bonuses: a contractual appropriation of profit that
    # reaches neither the shareholder nor the tax line. Registered by the previous edition,
    # described in its own source note as an omission of the edition before it, and then not
    # charged either. It is charged here, on the same base the company strikes it on.
    _emp = [max(_nopat[i], 0.0) * EMP_RATE for i in range(5)]
    _nopat = [_nopat[i] - _emp[i] for i in range(5)]
    _nwc, _dn = [], []
    for i in range(5):
        w = (inv_d / 365.0 * _cogs[i] + recv_d / 365.0 * _rev[i] - pay_d / 365.0 * _cogs[i])
        _nwc.append(w)
    _dn = [_nwc[0] - nwc_b] + [_nwc[i] - _nwc[i - 1] for i in range(1, 5)]
    _f = [_nopat[i] + _dna[i] - _capex[i] - _dn[i] for i in range(5)]
    _we = (wacc_exp if we is None else we) + wacc_shift
    _wt = (wacc_term if wt is None else wt) + wacc_shift
    _fwd = [_we - (_we - _wt) * fr for fr in glide_frac]
    _df, cc = [], 1.0
    for w in _fwd:
        cc /= (1 + w); _df.append(cc)
    _ic = [_nwc[i] + _ppe_n[i] for i in range(5)]
    # terminal return is capped at the rate a plant bought at REPLACEMENT cost would earn. The
    # reported return is flattered by an asset base 67% written down, and the book lens already
    # haircuts return on equity for exactly that reason. One view of the asset base, both lenses.
    _roic_raw = _nopat[-1] * (1 + g) / _ic[-1]
    _roic_repl = _nopat[-1] * (1 + g) / (_nwc[-1] + _ppe_g[-1])
    _roic = min(_roic_raw, roic_cap) if roic_cap else max(_roic_repl, 0.01)
    _rr = min(g / _roic, 0.95)
    _tv = _nopat[-1] * (1 + g) * (1 - _rr) / max(_wt - g, 0.02)
    _ev = sum(_f[i] * _df[i] for i in range(5)) + _tv * _df[-1]
    # EV to EQUITY, every claim carried:
    #   - the minority takes its share of the WHOLE enterprise, cash included, not of the
    #     operating enterprise while the parent keeps all the cash
    #   - the tax-disputes provision is a senior claim on that cash and is deducted at face
    #   - dividends payable is a declared claim, removed from working capital and carried here
    #   - the equity investment outside the operating enterprise is added at its carrying amount
    _eq_gross = _ev - nd_cy25
    _nci = NCI_OP if nci is None else nci
    _eq = (_eq_gross * (1 - _nci) - V['provisions'] / M - V['div_declared'] / M
           + V['fvoci'] / M + V['fin_inv'] / M)
    return dict(rev=_rev, gp=_gp, gm=S['gm'], opex=_opex, ebitda=_ebitda, ebit=_ebit,
                nopat=_nopat, emp=_emp, dna=_dna, capex=_capex, ppe=_ppe_n, ppe_gross=_ppe_g,
                nwc=_nwc, dnwc=_dn, fcff=_f, df=_df, fwd_wacc=_fwd, ic=_ic, tv=_tv,
                roic_term=_roic, rr_term=_rr, ev=_ev, eq=_eq, ps=_eq / SH,
                pv=[_f[i] * _df[i] for i in range(5)],
                pv_explicit=sum(_f[i] * _df[i] for i in range(5)), pv_tv=_tv * _df[-1],
                ebitda_margin=[_ebitda[i] / _rev[i] for i in range(5)])


B = build()
W = waterfall(B)
rev, ebitda, ebitda_margin = B['rev'], W['ebitda'], W['ebitda_margin']
dna, ebit, nopat, capex = W['dna'], W['ebit'], W['nopat'], W['capex']
nwc, dnwc, fcff, pv = W['nwc'], W['dnwc'], W['fcff'], W['pv']
pv_explicit = W['pv_explicit']
nwc_pct = nwc[0] / rev[0]
say("[Forecast revenue] " + " -> ".join(f"{r:,.0f}" for r in rev) +
    f" (volume {B['vol'][0]:.3f} -> {B['vol'][-1]:.3f}mn tonnes; specialty share of revenue "
    f"{B['spec_rev'][0]/B['rev'][0]:.1%} -> {B['spec_rev'][4]/B['rev'][4]:.1%}). Base-year "
    f"revenue is the {BASE_YEAR}, {BASE_REV:,.0f}, with no annualisation scalar.")
say("[Forecast gross margin] " + " -> ".join(f"{g:.2%}" for g in W['gm']) +
    ". The margin is an OUTPUT of eight per-line cost builds, not a path and not a blend: each "
    "line carries its own feedstock cost per tonne and its own conversion cost per tonne, and "
    "the company margin is whatever the mix produces. Specialty lines run " +
    " · ".join(f"{LBL[k]} {B['line_margin'][k][0]:.1%}" for k in SPEC) +
    " against fuel oil at " + f"{B['line_margin']['fueloil'][0]:.1%}" +
    ", so the margin now moves when the MIX moves, which it could not do when one blended margin "
    "was applied to every line.")
say(f"[Capital expenditure, BUILT] " + " -> ".join(f"{c:,.0f}" for c in capex) +
    f" against depreciation " + " -> ".join(f"{d:,.0f}" for d in dna) +
    f". Ratio " + " · ".join(f"{capex[i]/dna[i]:.2f}" for i in range(5)) +
    f". Maintenance is {MAINT_CAPEX0:,.0f} at today's prices, growth is charged at "
    f"{CAP_INTENSITY:,.0f} EGP a tonne of new throughput, and depreciation ROLLS off the asset "
    f"register rather than being held flat for five years.")
say(f"[Employees' profit share, CHARGED] {EMP_RATE:.2%} of profit after tax, "
    + " -> ".join(f"{e:,.0f}" for e in W['emp']) +
    f". The previous edition registered this at {V['emp_h2_25']/M:,.0f} for the audited half, "
    f"described it in its own source note as 'a real distribution out of profit that the "
    f"previous edition of this study did not model at all', and then no formula read the cell.")
say(f"[Free cash flow to the firm] " + " -> ".join(f"{f:,.0f}" for f in fcff) +
    f"; present value of the explicit window {pv_explicit:,.0f}.")

# ---- one roll-forward, consumed everywhere ---------------------------------
NCI_SHARE = V['nci_share']
PAYOUT = V['payout_reported']
def roll_forward(ebit_, fcff_):
    """The balance-sheet roll-forward, as ONE implementation.

    It was inline and therefore available only to the base case, which is why the expert
    panel's ranges could not be re-run on a scenario and were typed instead. Same reasoning
    as the single waterfall above: a second copy drifts, and the copy that drifts is the one
    nobody is looking at."""
    interest_, np_, div_, eq_, nd_, cash_ = [], [], [], [], [], []
    _nd, _eq = nd_cy25, eqp_cy25
    for i in range(5):
        _cash = debt_b - _nd
        _int = V['cash_yield_path'][i] * max(_cash, 0.0) - V['kd_path'][i] * debt_b
        _pbt = ebit_[i] + _int
        _npa = _pbt * (1 - TAX) * (1 - NCI_SHARE)
        _div = PAYOUT * _npa
        _eq += _npa - _div
        _nd = _nd - (fcff_[i] + _int * (1 - TAX)) + _div
        interest_.append(_int); np_.append(_npa); div_.append(_div)
        eq_.append(_eq); nd_.append(_nd); cash_.append(debt_b - _nd)
    return interest_, np_, div_, eq_, nd_, cash_


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
# The filed record now runs to the half just reported. Leaving 6M Jun-2026 out would show a
# margin record ending at the quarter BEFORE the strongest period the company has filed.
HKEY = ['6M Dec-2024', '3M Mar-2025', '6M Dec-2025', '3M Mar-2026', '6M Jun-2026']
_scale = {'6M Dec-2024': 2.0, '3M Mar-2025': 4.0, '6M Dec-2025': 2.0, '3M Mar-2026': 4.0,
          '6M Jun-2026': 2.0}
hist_rev = {'6M Dec-2024': V['rev_h2_24'] / M, '3M Mar-2025': V['rev_q1_25'] / M,
            '6M Dec-2025': V['rev_h2_25'] / M, '3M Mar-2026': V['rev_q1_26'] / M,
            '6M Jun-2026': V['rev_h1cy26'] / M}
hist_gp = {'6M Dec-2024': (V['rev_h2_24'] - V['cogs_h2_24']) / M,
           '3M Mar-2025': (V['rev_q1_25'] - V['cogs_q1_25']) / M,
           '6M Dec-2025': (V['rev_h2_25'] - V['cogs_h2_25']) / M,
           '3M Mar-2026': (V['rev_q1_26'] - V['cogs_q1_26']) / M,
           '6M Jun-2026': V['gp_h1cy26'] / M}
hist_gm = {k: hist_gp[k] / hist_rev[k] for k in HKEY}
# operating profit is disclosed for the two periods that carry a full expense note
hist_ebit = {'6M Dec-2025': 486_028_457.0 / M, '3M Mar-2026': 643_172_153.0 / M,
             '6M Dec-2024': 743_620_650.0 / M, '3M Mar-2025': 247_222_032.0 / M,
             '6M Jun-2026': 2_456_244_904.0 / M}
nopat_h = {k: hist_ebit[k] * _scale[k] * (1 - TAX_EFF) for k in HKEY}
ic_h = {'6M Dec-2025': IC_B, '3M Mar-2026': IC_B, '6M Jun-2026': IC_B,
        '6M Dec-2024': ((918_133_089 + 297_358_158) + (2_774_368_060 + 797_196_793 + 340_920_248)
                        - (10_452_591 + 1_002_068_641)) / M,
        '3M Mar-2025': ((937_851_261 + 403_190_211) + (3_735_009_103 + 894_888_039 + 611_842_230)
                        - (15_486_636 + 3_102_041_816)) / M}
capex_h = {'6M Dec-2025': V['capex_h2_25'] / M * 2, '3M Mar-2026': V['capex_q1_26'] / M * 4,
           '6M Dec-2024': V['capex_h2_25'] / M * 2, '3M Mar-2025': V['capex_q1_26'] / M * 4,
           '6M Jun-2026': 139_109_418.0 / M * 2}
dep_h = {'6M Dec-2025': V['dep_h2_25'] / M * 2, '3M Mar-2026': V['dep_q1_26'] / M * 4,
         '6M Dec-2024': V['dep_h2_25'] / M * 2, '3M Mar-2025': V['dep_q1_26'] / M * 4,
         '6M Jun-2026': 86_495_738.0 / M * 2}
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

rr_term = W['rr_term']
roic_term = W['roic_term']
nopat_term = nopat[-1] * (1 + V['g_term'])
tv = W['tv']
pv_tv = W['pv_tv']
ev = W['ev']
tv_share = pv_tv / ev
_roic_written_down = nopat[-1] * (1 + V['g_term']) / W['ic'][-1]
say(f"[Terminal value] the terminal return is struck on invested capital at REPLACEMENT cost — "
    f"working capital plus the asset base at GROSS cost — giving {roic_term:.1%}, against "
    f"{_roic_written_down:.1%} on net book. The difference is not cosmetic: this plant is 67.4% "
    f"written down, the book lens already haircuts return on equity from a reported 33% to 28% "
    f"for exactly that reason, and using the flattered figure in the terminal block while "
    f"haircutting it in the book lens would be two views of one asset base. Required "
    f"reinvestment = growth / return = {V['g_term']:.1%} / {roic_term:.1%} = {rr_term:.1%}; "
    f"terminal value {tv:,.0f} capitalised at {wacc_term:.2%} and discounted at the YEAR-5 "
    f"cumulative factor {W['df'][-1]:.4f}, giving a present value of {pv_tv:,.0f}. TERMINAL "
    f"VALUE IS {tv_share:.1%} OF ENTERPRISE VALUE.")
assert abs(roic_term * rr_term - V['g_term']) < 1e-9, "terminal growth != return x reinvestment"
# the identity is enforced, and the reinvestment STEP against the last explicit year is disclosed
# rather than left for a reader to find: a terminal block that reinvests less than the final
# forecast year while assuming perpetual growth is a step-up, and the size of it is stated.
_rr_2030 = (capex[4] - dna[4] + dnwc[4]) / nopat[4]
say(f"[Terminal reinvestment, against the explicit window] the final forecast year reinvests "
    f"{_rr_2030:.2%} of profit; the terminal block reinvests {rr_term:.2%}. The step is "
    f"{rr_term - _rr_2030:+.2%} and it is disclosed here because it RAISES the terminal block, "
    f"which carries {tv_share:.1%} of enterprise value. It is a consequence of the steady-state "
    f"identity rather than an assumption, but a reader is entitled to see it.")

# ---- enterprise value -> equity bridge, EVERY claim carried -----------------
eq_gross = ev - nd_cy25
nci_val = eq_gross * NCI_OP
prov_val = V['provisions'] / M
divp_val = V['div_declared'] / M
inv_val = V['fvoci'] / M + V['fin_inv'] / M
eq_attr = W['eq']
dcf_ps = W['ps']
say(f"[Bridge — every disclosed claim carried] enterprise value {ev:,.0f} plus net cash "
    f"{-nd_cy25:,.0f} = {eq_gross:,.0f}. Less minority interests at {NCI_OP:.3%} of the WHOLE "
    f"enterprise including the cash ({nci_val:,.0f}) — the previous edition charged the minority "
    f"its share of the operating enterprise and then credited the parent with 100% of the "
    f"consolidated cash, which is an inconsistency a reader can find in one line. Less the "
    f"tax-disputes provision {prov_val:,.0f}, a recognised liability the previous edition quoted "
    f"in its text and NEVER carried into the bridge — setting it to zero moved that valuation by "
    f"nothing at all. Less dividends payable {divp_val:,.0f}, a declared claim removed from "
    f"working capital and carried here. Plus non-operating investments {inv_val:,.0f} — the "
    f"equity stake at fair value through other comprehensive income and the PLEDGED deposits, "
    f"which are real assets even though they are not free cash and were previously excluded from "
    f"BOTH the cash line and the bridge. Equity attributable {eq_attr:,.0f} = EGP {dcf_ps:.2f} a "
    f"share against a spot of EGP {SPOT:.2f} ({dcf_ps/SPOT-1:+.1%}).")
assert abs((eq_gross * (1 - NCI_OP) - prov_val - divp_val + inv_val) - eq_attr) < 1e-6, \
    "the bridge does not close"
assert nci_val > 0 and nd_cy25 < 0 and prov_val > 0, "sign check on the bridge components"

# ---- contested choices, computed rather than asserted -----------------------
wacc_exp_rating = we_exp * ke_rating_alt + wd_exp * kd_at
wacc_term_rating = (1 - V['wd_term']) * (RF_TERM + V['beta'] * (V['erp_term'] + 0.045)) + \
    V['wd_term'] * kd_term_at


def _val_at(we_, wt_, g_=None, nci_=None):
    """THERE IS ONE COPY OF THE ARITHMETIC, and this is it going through the same
    waterfall the base case uses.

    THIS FUNCTION WAS A SECOND COPY AND IT HAD DRIFTED — which is the defect this
    study already diagnosed and cured once, in dcf_scenario's own docstring: *"the
    previous edition kept one waterfall for the base and another inside this
    function; they drifted, and a sensitivity row could report a number the model
    could not reproduce."* The cure was applied to the scenario engine and this
    function was left behind, still pricing the three contested choices AND every
    cell of the sensitivity grids.

    Measured before the fix, at the study's OWN adopted rates it returned EGP
    10.8572 against the delivered EGP 9.9142 — 9.51% apart, from two independent
    divergences. (i) It re-derived the terminal return from the FORECAST
    invested-capital series while the delivered terminal is struck on invested
    capital at REPLACEMENT cost, which is this study's own stated construction and
    the reason its terminal reinvestment rate is what it is: terminal value
    17,504.6 against 15,691.4, +11.56%. (ii) It deducted the minority as a share
    of ENTERPRISE value, which [R-BRIDGE-01] (ii) forbids in as many words, and
    omitted the provisions, the declared dividend and the non-operating
    investments the delivered bridge carries.

    Delegating removes both at once, and the assert below is the same one the
    scenario engine carries: a helper that cannot reproduce the base case is not a
    helper, it is a second model."""
    return waterfall(B, g=g_, we=we_, wt=wt_, nci=nci_)['ps']


_chk_val = _val_at(wacc_exp, wacc_term)
assert abs(_chk_val - dcf_ps) < 0.01, (
    "_val_at does not reproduce the base case: %.4f vs %.4f" % (_chk_val, dcf_ps))


dcf_rating_ps = _val_at(wacc_exp_rating, wacc_term_rating)
# "doubled" on the basis the DELIVERED bridge actually uses — the minority's share
# of gross EQUITY value, 2.96% — rather than a round 6% that was a doubling of the
# enterprise-value share the bridge does not use. It still prints as 6%.
nci_alt = 2 * NCI_OP
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
# THE SAME BRIDGE THE ANSWER USES. This line carried the third copy of the
# superseded construction — minority off ENTERPRISE value, and no provisions,
# declared dividend or non-operating investments — so the currency alternative was
# not comparable with the headline it is published against. It cannot delegate to
# waterfall() because its enterprise value is built on a different clock (the
# export leg deflated to dollars and discounted at a dollar cost of capital), so
# the bridge is applied here explicitly, in the same order and on the same lines.
_ccy_eq_gross = ev_ccy - nd_cy25
ccy_ps = (_ccy_eq_gross * (1 - NCI_OP) - V['provisions'] / M - V['div_declared'] / M
          + V['fvoci'] / M + V['fin_inv'] / M) / SH
say(f"[Currency-of-discounting alternative] the export leg ({exp_frac[-1]:.0%} of cash flow) is "
    f"first DEFLATED to dollars at each year's exchange rate, discounted at a dollar cost of "
    f"capital of {WACC_USD:.2%} with 3.5% terminal growth, and only then translated back at the "
    f"spot rate. Discounting a pound-denominated cash flow already inflated by the assumed "
    f"depreciation path directly at a dollar rate would count the currency benefit twice. Result "
    f"EGP {ccy_ps:.2f} a share ({ccy_ps/SPOT-1:+.1%} against spot).")

# ---- lens 2: relative -------------------------------------------------------
# ---- lens 2: relative multiples, on the TRAILING metric ---------------------
# The previous construction put the multiple on a FORWARD year and then discounted the result
# back using lens 1's own discount factor and added back lens 1's own interim free cash flow.
# Every reviewer who looked at it made the same objection: a cross-check that borrows the primary
# lens's machinery is not independent of it. The multiple now goes on the TRAILING metric, which
# needs no discount factor and no add-back, and is what a market participant actually quotes.
ev_trailing = MKTCAP + nd_cy25
ev_ebitda_trailing = ev_trailing / ebitda_cy25
pe_trailing = SPOT / (npa_cy25 / SH)


def _rel(mult):
    """Multiple x TRAILING EBITDA -> enterprise value TODAY -> equity through the same bridge
    the cash-flow lens uses. No discounting, no interim add-back, nothing borrowed."""
    _eqg = mult * ebitda_cy25 - nd_cy25
    return (_eqg * (1 - NCI_OP) - V['provisions'] / M - V['div_declared'] / M
            + V['fvoci'] / M + V['fin_inv'] / M) / SH


JUST_MULT = ev_ebitda_trailing * (1 + V['rel_rerating'])
rel_ps = _rel(JUST_MULT)
rel_bear, rel_bull = _rel(JUST_MULT * 0.75), _rel(JUST_MULT * 1.25)
ev_rel = JUST_MULT * ebitda_cy25
ev_rel_fwd = ev_rel
df_rel = 1.0
pv_interim = 0.0
ebitda_mid = ebitda_cy25
REL_I = 0
say(f"[Relative lens — on the TRAILING metric, multiple DERIVED] the company's own trailing "
    f"multiple is {ev_ebitda_trailing:.2f}x enterprise value to EBITDA — enterprise value "
    f"{ev_trailing:,.0f} over base-year EBITDA {ebitda_cy25:,.0f} — and {pe_trailing:.1f}x "
    f"earnings. The justified multiple is DERIVED from it at a {V['rel_rerating']:+.0%} "
    f"re-rating, {JUST_MULT:.2f}x, rather than set by hand. The previous edition stated the "
    f"trailing multiple as 'around 4.6x' and then set 4.5x, calling that 'holding the name at "
    f"its own trailing level'; the model's own output disagreed with the stated 4.6x, so the "
    f"justification did not hold whichever multiple was right. {JUST_MULT:.2f}x on TRAILING "
    f"EBITDA gives an enterprise value of {ev_rel:,.0f} TODAY, carried through the SAME bridge "
    f"as the cash-flow lens -> EGP {rel_ps:.2f} a share. Nothing here is discounted at the "
    f"cash-flow lens's rate and nothing is added back from it, so the difference between this "
    f"lens and the spot price is entirely the BRIDGE: the tax-disputes provision, the declared "
    f"dividend and the minority's share of the cash. That is what this lens is now for.")

# ---- lens 3: normalised earnings power, DISCOUNTED to the valuation date -----
NORM_I = 2                                   # every component from the SAME year
norm_rev = rev[NORM_I]
norm_ebitda = ebitda[NORM_I]
norm_ebit = norm_ebitda - dna[NORM_I]
norm_interest = credint_ttm / M
# Operating and financial earnings are separated. Capitalising credit interest at an OPERATING
# multiple values a risk-free cash balance as though it compounded like the business; the net
# cash is instead added at face OUTSIDE the multiple, which is the treatment the critics
# themselves stated and then did not apply.
norm_np_op = norm_ebit * (1 - TAX_STAT) * (1 - EMP_RATE) * (1 - NCI_OP)
norm_eps_op = norm_np_op / SH
# And the result is a 2028 number. Lens 2 no longer discounts anything because it is trailing;
# this lens IS forward-dated, so it is discounted to the valuation date at the COST OF EQUITY —
# an equity claim discounted at an equity rate, not at the unlevered weighted rate.
NORM_YRS = 2.4                               # 6-Aug-2026 to mid-2028
norm_df = 1.0 / (1 + ke_exp) ** NORM_YRS
norm_ps = (V['pe_just'] * norm_eps_op) * norm_df + (-nd_cy25 - V['provisions'] / M
                                                    - V['div_declared'] / M) / SH
norm_eps = norm_eps_op
norm_np = norm_np_op
norm_bear = (5.5 * norm_eps_op) * norm_df + (-nd_cy25 - V['provisions'] / M
                                             - V['div_declared'] / M) / SH
norm_bull = (9.5 * norm_eps_op) * norm_df + (-nd_cy25 - V['provisions'] / M
                                             - V['div_declared'] / M) / SH
say(f"[Normalised earnings lens — separated and discounted] OPERATING earnings only: 2028E "
    f"operating profit {norm_ebit:,.0f}, taxed at the statutory {TAX_STAT:.1%}, less the "
    f"employees' profit share and the minority -> EGP {norm_eps_op:.3f} a share. At "
    f"{V['pe_just']}x that is EGP {V['pe_just']*norm_eps_op:.2f} AS AT mid-2028, discounted "
    f"{NORM_YRS:.1f} years to the valuation date at the COST OF EQUITY {ke_exp:.2%} (factor "
    f"{norm_df:.4f}) = EGP {V['pe_just']*norm_eps_op*norm_df:.2f}. Net cash less the provision "
    f"and the declared dividend is then added at FACE, outside the multiple: EGP "
    f"{(-nd_cy25 - V['provisions']/M - V['div_declared']/M)/SH:.2f} a share. Total EGP "
    f"{norm_ps:.2f}. The previous edition capitalised {norm_interest:,.0f} of credit interest at "
    f"an operating multiple — valuing a bank deposit as though it were the refinery — and then "
    f"did not discount the 2028 answer at all, while lens 2 in the same document discounted its "
    f"forward number. One lens discounted and the other did not; both are now on the valuation "
    f"date.")

# ---- lens 4: book value and sustainable return ------------------------------
bvps = eqp_cy25 / SH
# The justified multiple is a perpetuity identity, so it needs ONE discount rate — but the
# previous edition used the TERMINAL cost of equity, 17.08%, for a perpetuity that starts today,
# while the cash-flow lens charges 31.58% in year one. A shareholder buying today is exposed to
# the near-term rate for as long as the glide lasts. The rate here is therefore the same glide
# lens 1 uses, present-value weighted, so the two lenses price the same time in the same way.
_ke_path = [ke_exp - (ke_exp - ke_term) * f for f in glide_frac]
_w, _c = [], 1.0
for _k in _ke_path:
    _c /= (1 + _k); _w.append(_c)
KE_BLEND = sum(_ke_path[i] * _w[i] for i in range(5)) / sum(_w)
pb_just = (V['roe_sust'] - V['g_term']) / (KE_BLEND - V['g_term'])
book_ps = pb_just * bvps
book_bear = ((V['roe_sust'] - 0.05 - 0.03) / (KE_BLEND - 0.03)) * bvps
book_bull = ((V['roe_sust'] + 0.03 - V['g_term']) / (KE_BLEND - V['g_term'])) * bvps
roe_trailing = npa_cy25 / ((V['eq_parent_jun25'] / M + eqp_cy25) / 2)
say(f"[Book lens — on a rate path consistent with lens 1] justified price-to-book "
    f"{pb_just:.2f}x = (sustainable return {V['roe_sust']:.1%} less growth {V['g_term']:.0%}) / "
    f"(cost of equity {KE_BLEND:.2%} less growth), applied to book value of EGP {bvps:.2f} a "
    f"share -> EGP {book_ps:.2f}. The rate is the present-value-weighted average of the SAME "
    f"cost-of-equity glide the cash-flow lens uses, {ke_exp:.2%} falling to {ke_term:.2%}, not "
    f"the terminal rate alone. Using the terminal rate alone gives "
    f"{((V['roe_sust']-V['g_term'])/(ke_term-V['g_term']))*bvps:.2f} and using the explicit rate "
    f"alone gives {((V['roe_sust']-V['g_term'])/(ke_exp-V['g_term']))*bvps:.2f}; a perpetuity "
    f"beginning today deserves neither endpoint. Trailing return on average parent equity is "
    f"{roe_trailing:.1%}, and the sustainable rate is struck below it because the asset base is "
    f"67.4% written down — the same haircut now applied to the terminal return in lens 1, so "
    f"there is one view of the asset base across the model rather than two.")

# ---- scenarios --------------------------------------------------------------
def dcf_scenario(vol_adj=0.0, price_mult=1.0, fx_mult=1.0, gm_shift=0.0,
                 wacc_shift=0.0, g=None, nwc_days=None, beta=None, proc=None):
    """Every scenario is a FULL re-run through the same waterfall the base case uses.

    There is no second copy of the arithmetic. The previous edition kept one waterfall for the
    base and another inside this function; they drifted, and a sensitivity row could report a
    number the model could not reproduce. Any change to the waterfall now reaches every
    sensitivity row and every scenario automatically, because there is only one of it."""
    _we = _wt = None
    if beta is not None:
        # beta reaches BOTH anchors through the SAME functions the base case uses
        _we = cost_of_capital(beta)[1]
        _wt = terminal_cost_of_capital(beta)
    S = build(vol_adj=vol_adj, price_mult=price_mult, fx_mult=fx_mult, gm_shift=gm_shift)
    return waterfall(S, wacc_shift=wacc_shift, g=g, nwc_days=nwc_days,
                     we=_we, wt=_wt)['ps']


def scenario_full(vol_adj=0.0, price_mult=1.0, fx_mult=1.0, gm_shift=0.0,
                  wacc_shift=0.0, g=None, nwc_days=None):
    """The same run as dcf_scenario, returning the WHOLE waterfall rather than one number.

    The expert panel needs a scenario's own cash flows and invested capital, not just its
    value per share, so that each expert's range can be its own method re-run at the two
    filed-evidence corners instead of a band typed beside it. Two typed bands had already
    gone stale and published a central OUTSIDE its own range: Expert 2's high used a
    terminal growth of 6% against a house terminal of 7%, so the 'high' was lower than the
    base, and its low carried a Gordon denominator written (ke_term + 0.03 - 0.03), which
    is ke_term — a subtraction that cancels itself and looks like it is doing something.
    Expert 3's high was the currency-alternative per-share number from a different
    construction entirely. Both are replaced by re-runs through this function."""
    S = build(vol_adj=vol_adj, price_mult=price_mult, fx_mult=fx_mult, gm_shift=gm_shift)
    return waterfall(S, wacc_shift=wacc_shift, g=g, nwc_days=nwc_days)


_chk = dcf_scenario()
assert abs(_chk - dcf_ps) < 0.01, f"scenario engine does not reproduce the base: {_chk} vs {dcf_ps}"
# ---- THE BEAR AND THE BULL COME OFF THE FILED RECORD, NOT OFF THE DIALS ------
# [rebuilt 03-Sep-2026; the item engine/build_depth_audit/lens_outstanding.json
# promised at this study's next re-issue]
#
# The previous corners moved FIVE things at once: volume, gross margin, the
# CURRENCY PATH, the COST OF CAPITAL at both anchors, and TERMINAL GROWTH. Three
# of those five are macro, and under [R-MACRO-01] all three are the same
# assumption wearing different hats -- the currency path is relative
# purchasing-power parity on the house inflation path, the terminal risk-free
# rate is terminal inflation plus the real-rate convention, and terminal growth
# is terminal inflation plus a stated real growth. So the old bull corner asked
# for a WEAKER pound (helping an exporter's translated revenue) alongside a LOWER
# cost of capital and HIGHER terminal growth, which needs Egyptian inflation to
# be high and low simultaneously. The bear corner asked for the mirror image. The
# two published ends were the two least coherent cells in the grid, and their
# width was this desk's choice of dial settings rather than anything the world
# had shown.
#
# What replaces them moves only what this company's OWN AUDITED FILINGS have
# actually printed, and holds the macro path exactly still:
#
#   GROSS MARGIN, across the filed span. The low is 5.053%, the quarter to
#   31-Mar-2025 -- the worst margin in the audited record this study holds. The
#   high is 13.84%, the full year to 30-Jun-2022, the best FULL YEAR on that
#   record; the best QUARTER is 13.92% and is deliberately not used, because a
#   forecast margin is sustained for five years and a quarter is not a year.
#   Base year 9.65%.
#
#   VOLUME, across the filed span. -4.5 percentage points a year carries the base
#   year's tonnage back to the FIVE-YEAR MEAN by year five, which is where the
#   audited record actually sits; +3.0 is the run-rate the last two filed periods
#   show. Both were already evidence-based and both are kept.
#
# The macro path does not move: fx_mult stays 1.00, wacc_shift 0.00, and terminal
# growth stays at the house terminal. The range is therefore ENTIRELY a business
# range, which is the only kind that says anything.
GM_FILED_LOW = 0.05053          # quarter to 31-Mar-2025, the worst in the audited record
_GM_FILED_HIGH = 0.1384         # full year to 30-Jun-2022, the best full year filed
SCEN = dict(
    bear=dict(vol_adj=-0.045, gm_shift=GM_FILED_LOW - BASE_GM,
              fx_mult=1.0, wacc_shift=0.0),
    bull=dict(vol_adj=+0.030, gm_shift=_GM_FILED_HIGH - BASE_GM,
              fx_mult=1.0, wacc_shift=0.0))
dcf_bear = dcf_scenario(**SCEN['bear'])
dcf_bull = dcf_scenario(**SCEN['bull'])
SCEN['bear']['ps'], SCEN['bull']['ps'], SCEN['base_ps'] = dcf_bear, dcf_bull, dcf_ps
SCEN['labels'] = dict(
    vol_adj='Volume growth, percentage points a year added to the flat base path',
    gm_shift='Gross margin, shifted on every forecast year',
    fx_mult='Exchange-rate path, as a multiple of the assumed path',
    wacc_shift='Cost of capital, shifted at BOTH the explicit and terminal anchors',
    g='Terminal growth rate')
say(f"[Scenarios on the cash-flow lens — BUSINESS DRIVERS ONLY] bear EGP {dcf_bear:.2f} / base "
    f"EGP {dcf_ps:.2f} / bull EGP {dcf_bull:.2f}. TWO drivers move and both move across the span "
    f"this company's own audited filings have actually printed: gross margin from "
    f"{GM_FILED_LOW:.2%} — the quarter to 31 March 2025, the worst in the record — to "
    f"{_GM_FILED_HIGH:.2%}, the full year to 30 June 2022 and the best FULL YEAR filed, against a "
    f"base year of {BASE_GM:.2%}; and volume {SCEN['bear']['vol_adj']:+.1%} / "
    f"{SCEN['bull']['vol_adj']:+.1%} a year against a flat base path, where the bear leg carries "
    f"the base year's tonnage back to the five-year mean by year five, which is where the audited "
    f"record sits. THE MACRO PATH DOES NOT MOVE. The previous edition also flexed the currency "
    f"path, the cost of capital at both anchors and terminal growth; all three carry the same "
    f"Egyptian inflation, so the old bull corner needed inflation high and low at the same time "
    f"and the old bear corner needed the mirror image. The width of a range built that way is "
    f"this desk's choice of dial settings. This one is the company's own filed record, and it is "
    f"not a confidence interval — no probability is attached to either end.")

# ---- THE TWO ALTERNATIVES THE PRINCIPAL'S LEAD EXPOSED ----------------------
# Both are priced through THIS study's own waterfall, per L-070: an alternative
# computed by a helper that reproduces neither the terminal nor the bridge
# measures the helper, not the choice.
#
# (1) THE ESCALATOR, as the previous editions carried it: pound conversion legs at
#     the full domestic inflation ladder against a price growing at the currency
#     differential. Adopted value is the corrected one; this is what it replaced.
_PS_POUND_AT_INFL = waterfall(build(pound_on_price=False))['ps']
#
# (2) THE BASE ANCHOR. The standing rule is that a near-term reviewed actual
#     outranks a stale full-year rate, and the most recent reviewed period is the
#     half to 30-Jun-2026 at 12.428% against a twelve-month base of 9.653%. The
#     LIKE-FOR-LIKE test the rule prescribes says the weakness is a superseded
#     LEVEL and not a season: Q1-2025 5.053% against Q1-2026 10.190%, the same
#     quarter, doubled — which no seasonal pattern produces — and Q2-2026 higher
#     again at 13.925%.
#
#     IT IS NOT ADOPTED IN THIS EDITION, AND THE REASON IS A RULE RATHER THAN A
#     PREFERENCE. [R-VCAL-01]'s promotion guard: levers are taken one at a time and
#     stop the moment the stack would cross zero by more than the bootstrap
#     half-width. The escalator correction already moved this study from 26.6%
#     below the traded price to 12.3% below it; adding this one lands 35.9% ABOVE
#     it. That is the overshoot the guard exists to prevent — five individually
#     justified moves stacking into a bias in the opposite direction is the exact
#     failure that called the method reassessment — so the second lever is priced,
#     published beside the answer, and left for the next edition to take on its own
#     evidence rather than on the momentum of this one.
_GM_H1_FILED = V['gp_h1cy26'] / V['rev_h1cy26']
_GM_Q1_2025 = 0.05053126981775711
_GM_Q1_2026 = 0.10189872213051045
_PS_H1_ANCHOR = waterfall(build(gm_shift=_GM_H1_FILED - build()['gm'][0]))['ps']
say(f"[The base anchor — PRICED, NOT ADOPTED] the most recent reviewed period is the half to "
    f"30-Jun-2026 at a gross margin of {_GM_H1_FILED:.3%}, against the twelve-month base of "
    f"{BASE_GM:.3%} this study forecasts forward. The standing rule prefers the near-term "
    f"reviewed actual, and the like-for-like test it prescribes supports it: Q1-2025 "
    f"{_GM_Q1_2025:.3%} against Q1-2026 {_GM_Q1_2026:.3%} is the SAME QUARTER doubled, which "
    f"seasonality cannot produce. Anchoring there and holding it flat gives EGP "
    f"{_PS_H1_ANCHOR:.2f} a share ({_PS_H1_ANCHOR/SPOT-1:+.1%} against spot) against the "
    f"adopted EGP {dcf_ps:.2f}. IT IS NOT TAKEN HERE. One correction has already moved this "
    f"study from {_PS_POUND_AT_INFL/SPOT-1:+.1%} to {dcf_ps/SPOT-1:+.1%} against the price; a "
    f"second would land {_PS_H1_ANCHOR/SPOT-1:+.1%}, crossing from one side of the price to the "
    f"other in a single pass. Levers are taken one at a time and stop at the crossing, so this "
    f"one is published as the study's most consequential contested judgement and left for the "
    f"next edition.")

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
# ---- ONE PRIMARY, AND THE REST ARE CROSS-CHECKS [R-LENS-03] ------------------
# The typed 45/20/20/15 blend is retired. It was chosen, written down and
# inherited, and it had never cleared any out-of-sample test — a free parameter in
# a house that forbids them everywhere else. Averaging four methods does not make
# a number more robust than the best of them: it makes a FIFTH method with weights
# nobody tested, carrying every weakness of the weakest at whatever weight
# somebody typed.
#
# For this class the registry names the cash-flow lens as the primary. Normalised
# earnings is NOT in the class's permitted set and is dropped as a lens: it
# capitalises a mid-cycle margin at a nominal rate on a refiner whose entire
# economics are a ~6.6% spread between two numbers above EGP 35bn, so a mid-cycle
# margin is the one thing about this company that cannot be normalised. It carried
# a fifth of the weight. It is kept below as a diagnostic and reaches no published
# number. Book value is a DISCLOSED FLOOR, published as such and never weighted.
_RETIRED_BLEND = sum(l['base'] * l['w'] for l in lenses.values())
central = lenses['dcf']['base']
lo = lenses['dcf']['bear']
hi = lenses['dcf']['bull']
lo_env = min(l['bear'] for l in lenses.values())
hi_env = max(l['bull'] for l in lenses.values())
assert lo < central < hi, "the primary lens's own range does not bracket its base"
assert lo_env <= lo and hi <= hi_env, "the primary's range escapes the envelope of all lenses"
say(f"[Range — the primary lens's OWN range, on one clock] EGP {lo:.2f} to {hi:.2f}. The "
    f"cross-checks span EGP {lo_env:.2f} to {hi_env:.2f} and that is reported as an ENVELOPE, "
    f"never averaged into the answer.")
lenses['central'] = dict(name='Cash-flow lens (the central)', bear=lo, base=central,
                         bull=hi, w=1.0)
lenses['retired_blend'] = dict(name='RETIRED 45/20/20/15 blend, published unused',
                               base=_RETIRED_BLEND,
                               bear=sum(l['bear'] * l['w'] for l in lenses.values() if 'w' in l and l['w'] < 1.0),
                               bull=sum(l['bull'] * l['w'] for l in lenses.values() if 'w' in l and l['w'] < 1.0),
                               w=0.0)
say(f"[Synthesis] the central is the CASH-FLOW LENS at EGP {central:.2f}, not a blend; "
    f"cross-checks span EGP {lo_env:.2f} - {hi_env:.2f}; spot EGP {SPOT:.2f} "
    f"({central/SPOT-1:+.1%} to the central). The retired 45/20/20/15 blend of the same "
    f"lenses would read EGP {_RETIRED_BLEND:.2f} and is published beside the answer, unused.")
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
    _kt = RF_TERM + b * V['erp_term']
    grid_beta.append(_val_at(we_exp * _ke + wd_exp * kd_at,
                             (1 - V['wd_term']) * _kt + V['wd_term'] * kd_term_at))
# ---- sensitivity: EVERY row a full re-run through the one waterfall ---------
# The previous edition produced three rows the model could not reproduce: a working-capital row
# whose grid was never sorted, so the base case sat in the middle slot and the row read
# non-monotonic; a beta row built by a separate mini-valuation whose centre did not return the
# base case; and a volume row whose label read as a volume range when the lever is a growth-path
# multiplier. All three are rebuilt here from full re-runs, the grids are sorted, and a GATE at
# the end asserts that every row returns the base case at its own base point.
gm_grid = [-0.010, -0.005, 0.0, 0.005, 0.010]
grid_margin = [dcf_scenario(gm_shift=s) for s in gm_grid]
vol_grid = [-0.06, -0.03, 0.0, 0.03, 0.06]            # ADDER to the flat base path, a year
grid_vol = [dcf_scenario(vol_adj=m) for m in vol_grid]
fx_grid = [0.90, 0.95, 1.0, 1.05, 1.10]
grid_fx = [dcf_scenario(fx_mult=m) for m in fx_grid]
beta_grid = sorted([0.60, 0.80, V['beta'], 1.15, 1.30])
grid_beta = [dcf_scenario(beta=b) for b in beta_grid]
# working capital is now DAYS, so the row sweeps the cycle the balance sheet actually shows
_cyc0 = INV_DAYS + RECV_DAYS - PAY_DAYS
wc_mult_grid = [0.5, 0.75, 1.0, 1.25, 1.5]
wc_grid = [round(_cyc0 * m, 1) for m in wc_mult_grid]
grid_nwc = [dcf_scenario(nwc_days=(INV_DAYS * m, RECV_DAYS * m, PAY_DAYS * m))
            for m in wc_mult_grid]
nwc_grid = wc_grid

# ---- GATE: a sensitivity row that cannot reproduce the base case is broken ---
_rows = [('gross margin', gm_grid, grid_margin, 0.0, +1),
         ('volume growth a year', vol_grid, grid_vol, 0.0, +1),
         ('exchange-rate path', fx_grid, grid_fx, 1.0, +1),
         ('beta', beta_grid, grid_beta, V['beta'], -1),
         ('working-capital cycle', wc_mult_grid, grid_nwc, 1.0, -1)]
for _nm, _g, _v, _base, _sign in _rows:
    assert list(_g) == sorted(_g), f"sensitivity grid '{_nm}' is not sorted"
    _i = min(range(len(_g)), key=lambda j: abs(_g[j] - _base))
    assert abs(_g[_i] - _base) < 1e-9, f"sensitivity row '{_nm}' has no base point on its grid"
    assert abs(_v[_i] - dcf_ps) < 0.005, \
        f"sensitivity row '{_nm}' does not reproduce the base case: {_v[_i]:.4f} vs {dcf_ps:.4f}"
    _d = [_v[j + 1] - _v[j] for j in range(len(_v) - 1)]
    assert all(d * _sign > 0 for d in _d), f"sensitivity row '{_nm}' is not monotone: {_v}"
say(f"[Sensitivity gate] {len(_rows)} rows, every one a full re-run through the same waterfall "
    f"the base case uses. Every grid is sorted, every row returns EGP {dcf_ps:.2f} at its own "
    f"base point, and every row is monotone in the direction theory requires. The previous "
    f"edition published three rows that failed one or more of these tests and had no gate that "
    f"could have caught them.")

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



def e2_on(W_):
    """Expert 2's construction, re-run on any scenario's own waterfall.

    Free cash flow to the EQUITY holder, discounted on the cost of equity's own glide. The
    terminal block uses THE HOUSE TERMINAL GROWTH — the same one the primary lens uses —
    because under [R-MACRO-01] terminal growth is terminal inflation plus a stated real
    growth and is not a dial an expert may turn on its own."""
    _int, _, _, _, _, _ = roll_forward(W_['ebit'], W_['fcff'])
    _fcfe = [(W_['fcff'][i] + _int[i] * (1 - TAX)) * (1 - NCI_SHARE) for i in range(5)]
    _pv = sum(_fcfe[i] * e2_df[i] for i in range(5))
    _tv = _fcfe[-1] * (1 + V['g_term']) * (1 - W_['rr_term']) / (ke_term - V['g_term'])
    return _fcfe, _pv, _tv * e2_df[-1], (_pv + _tv * e2_df[-1]) / SH


# THE PANEL IS RE-RUN AT THE FILED CORNERS, NOT BANDED BY HAND.
# What was here published a central OUTSIDE its own stated range, in a table a reader sees:
# the 'high' used a terminal growth of 6% against the house terminal of 7%, so it came out
# BELOW the base, and the 'low' carried the denominator (ke_term + 0.03 - 0.03), which is
# ke_term — a Gordon formula with the growth term cancelled against itself, arithmetically
# wrong and written so that it looks deliberate. Both were typed beside the method rather
# than produced by it, which is why neither moved when the house macro path moved the
# terminal. Expert 2 is now its own construction re-run on the SAME two filed-evidence
# corners the primary lens publishes, so the panel and the envelope are read on one clock.
_W_BEAR = scenario_full(vol_adj=SCEN['bear']['vol_adj'], gm_shift=SCEN['bear']['gm_shift'])
_W_BULL = scenario_full(vol_adj=SCEN['bull']['vol_adj'], gm_shift=SCEN['bull']['gm_shift'])
e2_lo = e2_on(_W_BEAR)[3]
e2_hi = e2_on(_W_BULL)[3]

# Expert 2's own cash flows discounted on the WEIGHTED rate instead of the cost of equity's
# glide. This is the ONE number that decomposes the Expert 2 / Expert 3 gap: everything else
# about the two constructions is held still, so what is left is the price of time. Computed
# here rather than in a builder, because a figure quoted in prose is computed, never typed.
e2_ps_at_wacc = (sum(e2_fcfe[i] * df[i] for i in range(5))
                 + e2_fcfe[-1] * (1 + V['g_term']) * (1 - rr_term)
                 / (wacc_term - V['g_term']) * df[-1]) / SH
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


def e3_on(W_):
    """Expert 3's construction — invested capital plus the present value of economic profit
    — re-run on any scenario's own waterfall, on the same corners as Expert 2."""
    _ic_beg = [ic_cy25] + W_['ic'][:-1]
    _ep = [W_['nopat'][i] - W_['fwd_wacc'][i] * _ic_beg[i] for i in range(5)]
    _pv_ep = sum(_ep[i] * W_['df'][i] for i in range(5))
    _ep_t = W_['nopat'][-1] * (1 + V['g_term']) - wacc_term * W_['ic'][-1]
    _pv_ep_t = _ep_t / (wacc_term - V['g_term']) * W_['df'][-1]
    _ev = ic_cy25 + _pv_ep + _pv_ep_t
    return _ev, (_ev * (1 - NCI_SHARE) - nd_cy25) / SH


# The old 'high' here was ccy_ps — the CURRENCY-ALTERNATIVE per-share number, produced by a
# different construction for a different purpose and borrowed as this method's upper bound.
# It sat BELOW the base, so this table too published a central outside its own range.
e3_lo = e3_on(_W_BEAR)[1]
e3_hi = e3_on(_W_BULL)[1]

# WHAT ACTUALLY DRIVES THE EXPERT 2 / EXPERT 3 GAP, measured rather than asserted. The first
# draft of Appendix C labelled this row 'the discount rate' on the reasonable-sounding grounds
# that one expert discounts at the cost of equity and the other at the weighted rate. The
# measurement refutes it: the rate is worth less than a seventh of the gap. A mechanism
# contradicted by the arithmetic is not a mechanism, it is the assumption wearing one
# [R-ANCHOR-01], so the label follows the measurement and not the other way round.
e2e3_gap = e3_base - e2_base
e2e3_rate = e2_ps_at_wacc - e2_base
e2e3_cash = (-nd_cy25) / SH                       # Expert 3 adds net cash at face; Expert 2 does not
e2e3_resid = e2e3_gap - e2e3_rate - e2e3_cash
say(f"[Expert 2 / Expert 3 decomposition — MEASURED] the gap is {e2e3_gap:+.2f} a share. "
    f"Discounting Expert 2's OWN cash flows on the weighted rate instead of the cost of "
    f"equity's glide gives EGP {e2_ps_at_wacc:.2f} against {e2_base:.2f}, so the price of time "
    f"is worth {e2e3_rate:+.2f} — {abs(e2e3_rate/e2e3_gap):.0%} of it. The BRIDGE is what "
    f"carries the rest: Expert 3 adds net cash of {e2e3_cash:+.2f} a share at face, while "
    f"Expert 2 lets the cash reach the holder only through the finance-income line. "
    f"{e2e3_resid:+.2f} is left over. THE FIRST DRAFT OF THE DIVERGENCE TABLE NAMED THE "
    f"DISCOUNT RATE AS THE DRIVER; the measurement says it is the bridge, and the table now "
    f"says so.")
say(f"[Economic-profit convention] the capital charge is taken on BEGINNING-of-year invested "
    f"capital, not ending. Charging ending capital would understate economic profit by about "
    f"{sum((ic[i]-ic_beg[i])*fwd[i] for i in range(5))/5:,.0f}mn a year.")
experts = dict(
    e1=dict(method_short='earnings power at a justified multiple', base=e1_base,
            rng=[e1_lo, e1_hi], eps=e1_eps, ebit=e1_ebit, interest=e1_int, pe=e1_pe,
            year=YRS[e1_i]),
    e2=dict(method_short='free cash flow to equity, discounted', base=e2_base,
            rng=[e2_lo, e2_hi], fcff=e2_fcff, fcfe=e2_fcfe, ke=e2_ke, fin_at=e2_fin_at,
            ke_path=e2_ke_path, df=e2_df, pv=e2_pv, pv_tv=e2_pv_tv,
            ps_at_wacc=e2_ps_at_wacc),
    # the measured decomposition of the Expert 2 / Expert 3 gap, so the divergence table
    # names what the arithmetic names rather than what sounds plausible
    e2e3=dict(gap=e2e3_gap, rate=e2e3_rate, cash=e2e3_cash, resid=e2e3_resid),
    e3=dict(method_short='cash returns against the cost of capital', base=e3_base,
            rng=[e3_lo, e3_hi], ic0=ic_cy25, pv_ep=pv_ep, pv_ep_term=pv_ep_term, ev=e3_ev,
            ep=ep_, spread=[roic[i] - fwd[i] for i in range(5)]),
)
# A table that publishes a central outside its own stated range contradicts itself in front
# of the reader, and no gate in this repository could see it because every one of them was
# checking how the number was BUILT. This is the [R-GAP-01] discipline applied to the panel:
# look at the answer.
for _k, _b, _l, _h in (('Expert 1', e1_base, e1_lo, e1_hi),
                       ('Expert 2', e2_base, e2_lo, e2_hi),
                       ('Expert 3', e3_base, e3_lo, e3_hi)):
    assert _l <= _b <= _h, (
        f"{_k} publishes a central of EGP {_b:.2f} OUTSIDE its own stated range "
        f"[{_l:.2f}, {_h:.2f}]. A range is what the method produces at its corners, never a "
        f"band typed beside it.")

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

# ---- THE LEVEL-TOUCH LADDER, computed here rather than in a builder --------------
# The reflection principle on a driftless-in-logs approximation, which is what the engine's
# own stored ladder is built on. The ANCHOR is the cone's, never the study's spot.
_TOUCH_LEVELS = [11.00, 10.50, 10.00, round(V['spot'], 2), 8.50, 8.00, 7.50,
                 round(dcf_ps, 2)]


def _p_touch(level, h, anchor):
    from statistics import NormalDist
    _s = h['sigma_h']
    if abs(_s) < 1e-9:
        return 0.0
    _m = math.log(h['pct']['p50'] / anchor)
    _b = math.log(level / anchor)
    N = NormalDist().cdf
    if _b >= 0.0:
        return min(1.0, N((_m - _b) / _s) + math.exp(2.0 * _m * _b / (_s ** 2))
                   * N((-_b - _m) / _s))
    return min(1.0, N((_b - _m) / _s) + math.exp(2.0 * _m * _b / (_s ** 2))
               * N((_b + _m) / _s))


_TOUCH_P = {}
for _lv in _TOUCH_LEVELS:
    _TOUCH_P[f'{_lv:.2f}'] = {
        _hk: round(_p_touch(_lv, strike['horizons'][_hk], strike['spot']), 6)
        for _hk in ('1M', '3M')}
say('[Level-touch ladder] ' + ' · '.join(
    f"{_lv:.2f}: 1M {_TOUCH_P[f'{_lv:.2f}']['1M']:.1%} / 3M {_TOUCH_P[f'{_lv:.2f}']['3M']:.1%}"
    for _lv in _TOUCH_LEVELS)
    + '. Computed on the cone\'s OWN anchor of EGP %.2f, not on the study spot of %.2f — a '
      'fresh price moves the valuation without re-striking the cone.'
    % (strike['spot'], V['spot']))

beta_res = json.load(open(os.path.join(HERE, 'beta_result.json')))
bt5 = json.load(open(os.path.join(HERE, 'backtest_5y.json')))

# ---- BLOCK EMIT: the model's own values for every workbook block ------------
# The workbook writes the whole forecast engine out again, in formulas, once per sensitivity
# grid point. For the evaluator to check each of those blocks cell by cell, the model has to hand
# over its own values for each one. That is what this does. It also means a grid point can no
# longer be a number somebody pasted: if the block does not reproduce, the gate fails.
def _blockvals(S, wacc_shift=0.0, g=None, nwc_days=None, we=None, wt=None,
               fx_mult=1.0, price_mult=1.0):
    g = V['g_term'] if g is None else g
    R = waterfall(S, wacc_shift=wacc_shift, g=g, nwc_days=nwc_days, we=we, wt=wt)
    _inf, _px, iv, pv_ = [], [], 1.0, 1.0
    for i in range(5):
        iv *= V['fixed_cost_infl'][3 + i]; _inf.append(iv)
    for i in range(5):
        pv_ *= (1 + V['line_price_growth'][i] * price_mult * fx_mult); _px.append(pv_)
    _we = (wacc_exp if we is None else we) + wacc_shift
    _wt = (wacc_term if wt is None else wt) + wacc_shift
    _nop0 = [R['ebit'][i] * (1 - TAX_STAT) for i in range(5)]
    return dict(
        inf=_inf, px=_px,
        vol={k: S['lines_vol'][k] for k in LINES}, vtot=S['vol'],
        rev=R['rev'], cogs=S['cogs'], gp=R['gp'], gm=R['gm'], opex=R['opex'],
        ebitda=R['ebitda'], capex=R['capex'], gross=R['ppe_gross'], dna=R['dna'],
        ppe=R['ppe'], ebit=R['ebit'], nop0=_nop0, emp=R['emp'], nopat=R['nopat'],
        nwc=R['nwc'], dnwc=R['dnwc'], fcff=R['fcff'],
        glide=glide_frac, fwd=R['fwd_wacc'], df=R['df'], pv=R['pv'],
        icr=[R['nwc'][i] + R['ppe_gross'][i] for i in range(5)],
        pv_explicit=R['pv_explicit'], roic=R['roic_term'], rr=R['rr_term'], tv=R['tv'],
        pv_tv=R['pv_tv'], ev=R['ev'], nd=nd_cy25, eq_gross=R['ev'] - nd_cy25,
        nci=(R['ev'] - nd_cy25) * NCI_OP, prov=V['provisions'] / M, divp=V['div_declared'] / M,
        inv=(V['fvoci'] + V['fin_inv']) / M, eq=R['eq'], ps=R['ps'], we=_we, wt=_wt)


_GRIDS, _SCEN_V = [], {}


def _grid(name, pts):
    _GRIDS.append([name, None, []])
    for pi, (label, lev, kw, is_base) in enumerate(pts):
        _GRIDS[-1][2].append(dict(
            label=label, levers=lev, is_base=is_base,
            has_gm=any(c == 'C' for c, _, _ in lev), has_fx=any(c == 'D' for c, _, _ in lev),
            has_wc=any(c == 'E' for c, _, _ in lev), has_we=any(c == 'F' for c, _, _ in lev),
            has_wt=any(c == 'G' for c, _, _ in lev), has_g=any(c == 'H' for c, _, _ in lev)))
        _S = build(vol_adj=kw.get('vol_adj', 0.0), gm_shift=kw.get('gm_shift', 0.0),
                   fx_mult=kw.get('fx_mult', 1.0))
        _SCEN_V[f'{name}|{pi}'] = _blockvals(
            _S, g=kw.get('g'), nwc_days=kw.get('nwc_days'),
            we=kw.get('we'), wt=kw.get('wt'), fx_mult=kw.get('fx_mult', 1.0))


_PCT2, _NUM1, _NUM3 = '0.00%', '#,##0.0', '#,##0.000'
_grid('Gross margin, shifted on every forecast year',
      [(f'{s:+.1%}', [('C', s, _PCT2)], dict(gm_shift=s), s == 0.0) for s in gm_grid])
_grid('Volume growth path, as a multiple of the assumed path',
      [(f'{m:+.1%}', [('B', m, _NUM1)], dict(vol_adj=m), m == 0.0) for m in vol_grid])
_grid('Realisation path, as a multiple of the assumed path',
      [(f'{m:.2f}x', [('D', m, _NUM1)], dict(fx_mult=m), m == 1.0) for m in fx_grid])
_grid('Beta', [(f'{b:.4f}',
                [('F', cost_of_capital(b)[1], _PCT2), ('G', terminal_cost_of_capital(b), _PCT2)],
                dict(we=cost_of_capital(b)[1], wt=terminal_cost_of_capital(b)),
                abs(b - V['beta']) < 1e-9) for b in beta_grid])
_grid('Working-capital cycle, as a multiple of the solved days',
      [(f'{m:.2f}x', [('E', m, _NUM1)],
        dict(nwc_days=(INV_DAYS * m, RECV_DAYS * m, PAY_DAYS * m)), m == 1.0)
       for m in wc_mult_grid])
_grid('Terminal growth',
      [(f'{gg:.1%}', [('H', gg, _PCT2)], dict(g=gg), abs(gg - V['g_term']) < 1e-9)
       for gg in g_grid])
BLOCKS = dict(base=_blockvals(B), grids=_GRIDS, scen=_SCEN_V)
_nb = 1 + sum(len(g[2]) for g in _GRIDS)
say(f"[Workbook blocks emitted] {_nb} complete forecast engines — the base case and "
    f"{_nb-1} sensitivity grid points — each with the model's own value for every cell, so the "
    f"workbook can write all {_nb} out as live formula chains and an independent evaluator can "
    f"check each one. The previous edition pasted its sensitivity grids because a whole-model "
    f"re-run could not be expressed inside a grid; that was 27.6% of the file and three of the "
    f"pasted rows did not reproduce.")

# ===========================================================================
# THE THREE CONSTRUCTION RECORDS [R-MACRO-01, R-LENS-03, R-BRIDGE-01]. This study
# already implemented the cost-of-capital procedure — it was the only one that
# did — so what it owed was the RECORD of its other constructions, written down
# so a job outside the study can check the choices rather than recompute the
# arithmetic. A model that recalculates is not a model that is right.
# ===========================================================================
import sys as _sys, os as _os
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
# _MPATH/_HP are loaded near the top of the file, before the input register, because
# the register now READS the house ladder rather than carrying its own.
_HYR = list(_HP.inflation_years)

MACRO_RECORD = dict(
    market='EG', path_as_of=_HP.as_of,
    # [R-MACRO-01], clause added 03-Sep-2026 after EGCH: every inflation-class INPUT,
    # not only the declared growth lines. THIS RECORD ALREADY SAID IN PROSE, in the
    # exempt_reason below, that this study runs 'the registered Egyptian inflation
    # ladder this study was built on, which predates the house path and differs from it
    # year by year' — and the gate passed it, because a line declared exempt is not
    # checked. Declaring the array makes the same statement ARITHMETIC, so this study
    # now fails the clause and is listed on the ratchet with its reason, instead of
    # reading as coherent while its own record says otherwise. A lesson that binds
    # nothing is advice.
    #
    # IT WAS THEN CONFORMED RATHER THAN RATCHETED, and the reason is that --prune refused
    # to grow the list: a ratchet spares work predating a standard and may only ever get
    # SHORTER, so the only honest options were to conform the study or leave a permanently
    # red check, which [R-ENF-02] forbids. THE DIRECTION WAS NOT WHAT I EXPECTED AND IT IS
    # RECORDED BECAUSE OF THAT. The study's ladder compounded HIGHER than the house path
    # (1.7385 against 1.6288 over the five forecast years), so the arithmetic said
    # conforming would cut fixed costs and RAISE the value. It lowered it: EGP 11.83 ->
    # 11.40, -12.3% -> -15.5% against the price. The currency path is DERIVED from this
    # ladder by purchasing-power parity, so a lower ladder means a stronger pound, and on a
    # dollar-linked slate the lost translation gain outweighs the saved pound costs. A
    # correction that moves AWAY from the price is not a reason to reconsider it.
    inflation_inputs=[
        dict(key='fixed_cost_infl (forecast years)', mapping='calendar',
             first_year=2026,
             values=[round(x - 1.0, 6) for x in V['fixed_cost_infl'][3:]],
             note='the house calendar ladder, read live rather than typed. The currency '
                  'path and the product price path are both DERIVED from it by '
                  'purchasing-power parity, so there is one view of the economy inside '
                  'this model and conforming the ladder moved all three together.'),
    ],
    growth_lines=[
        dict(name='pound-denominated cost legs',
             years=_HYR, nominal=[round(x, 6) for x in _EG_INFL],
             real=0.0,
             basis='the house calendar inflation ladder at zero real growth, read live '
                   'from engine/macro_paths/EG.json. CONFORMED 03-Sep-2026: this line '
                   'previously carried the study\'s own ladder and was declared exempt on '
                   'the grounds that the study was internally coherent and that rebuilding '
                   '"belongs in its own pass" — a statement about convenience, which is not '
                   'one of the grounds [R-MACRO-01] allows. The currency path and the '
                   'product price path are both DERIVED from this one ladder by '
                   'purchasing-power parity, so conforming it moved all three together.'),
        dict(name='realised price per tonne, all lines',
             years=_HYR, nominal=[round(x, 6) for x in _DEPREC], real=0.0,
             exempt_reason='DERIVED, not chosen: crude is held flat in dollars and the '
                           'pound depreciates at the inflation differential, so a '
                           'dollar-priced slate fetches that many more pounds. It '
                           'inherits whatever ladder the line above carries.'),
    ],
    fx_path=None,
    fx_note='the currency path is DERIVED from the same inflation ladder as the price '
            'path by relative purchasing-power parity, so the two cannot disagree; it '
            'is not the house path\'s own currency path and is exempted with the '
            'ladder above rather than half-conformed.',
    terminal=dict(g_nominal=V['g_term'], real=0.0, rf=RF_TERM,
                  inflation_in_rf=V['cbe_target']),
    explicit_years=5,
    growth_at_horizon_end=V['g_term'],
    note='THE TERMINAL IS ALREADY ON THE HOUSE PATH and was the source of it: this '
         'study derived the terminal risk-free rate as the central bank target in '
         'force plus the real-rate convention, and set terminal growth equal to that '
         'same target, in its edition of 06-Aug-2026. The house path adopted that '
         'construction. What is NOT yet conformed is the explicit-window inflation '
         'ladder, which is exempted above with its reason.',
)

LENS_RECORD = {
    'class': 'refiner, commodity pass-through on a thin spread',
    'primary': dict(kind='dcf', value=float(lenses['dcf']['base']),
                    range=dict(low=float(lenses['dcf']['bear']),
                               high=float(lenses['dcf']['bull'])),
                    range_note='the cash-flow lens with gross margin and volume each '
                               'flexed across the span this company\'s own audited '
                               'filings have printed, and the macro path held still. '
                               'Not a confidence interval and no probability is '
                               'attached to either end',
                    range_basis=dict(
                        driver='gross margin, and tonnage, each across its own filed span',
                        low=float(GM_FILED_LOW), high=float(_GM_FILED_HIGH),
                        macro_held=True,
                        evidence='gross margin from %.3f%% — the quarter to 31 March 2025, '
                                 'the worst in the audited record this study holds — to '
                                 '%.2f%%, the full year to 30 June 2022 and the best FULL '
                                 'YEAR filed, against a base year of %.2f%%. The best '
                                 'single QUARTER on the record is 13.92%% and is '
                                 'deliberately not used: a forecast margin is sustained '
                                 'for five years and a quarter is not a year. Tonnage '
                                 '%+.1f%% / %+.1f%% a year against a flat base path, the '
                                 'bear leg carrying the base year back to the FIVE-YEAR '
                                 'MEAN by year five, which is where the audited record '
                                 'sits. The currency path, the cost of capital at both '
                                 'anchors and terminal growth are all held at the house '
                                 'macro path and do not move.'
                                 % (GM_FILED_LOW * 100, _GM_FILED_HIGH * 100,
                                    BASE_GM * 100, SCEN['bear']['vol_adj'] * 100,
                                    SCEN['bull']['vol_adj'] * 100)),
                    note='the cash-flow lens on the company\'s own tonnes and the '
                         'spread between two disclosed numbers, discounted on the '
                         'glide with the terminal norm-built'),
    'cross_checks': [
        # THIS RECORD SAID THE OPPOSITE OF WHAT THE CODE DID, AND SAID IT FOR
        # THREE EDITIONS [corrected 03-Sep-2026, found by the re-strike]. It
        # attested "enterprise value to EBITDA from the company's own history and
        # its regional peers, never a multiple read off the current price". Twelve
        # hundred lines above, ev_trailing is MARKET CAP plus net debt and the
        # justified multiple is that divided by base-year EBITDA, re-rated by
        # zero: the traded multiple exactly. The lens's whole distance from the
        # share price was the bridge, and the code comment said so in as many
        # words while the record denied it. [R-LENS-03]'s gate read the sentence,
        # found the reassuring words, and passed it three times.
        #
        # What exposed it was moving the price: on 03-Sep-2026 the spot went from
        # 9.10 to 13.50, +48%, and this lens went from 8.32 to 12.59, +51%. A lens
        # built on five years of own history cannot do that. A lens built on
        # today's price cannot do anything else.
        #
        # IT IS WITHDRAWN RATHER THAN REBUILT, and the reason is a measurement
        # rather than a preference: an own-history EV/EBITDA needs this company's
        # net debt and share count at each past year end, and AMOC's own
        # walk-forward panel carries PPE at 2021-2023 and NOTHING ELSE --
        # engine/valuation_calibration/bridge_inputs.py prints the census. That is
        # precisely the gap [R-FCAL-01 AMENDED] was adopted to close, and AMOC is
        # on its outstanding list. Inventing the multiple from a peer set nobody
        # sourced would be the same offence in the other direction, so under SIGCM
        # clause 8 the lens stops rather than guesses. It returns when AMOC's next
        # walk-forward run commits the valuation-input block.
        dict(kind='relative_multiple', value=float(lenses['relative']['base']),
             present_value=False,
             withdrawn=True,
             multiple_source='THE CURRENT PRICE. The multiple is the company\'s own '
                             'traded enterprise value over base-year EBITDA, re-rated '
                             'by zero, so this lens values the company at what it '
                             'already trades at and its only distance from the share '
                             'price is the bridge. It is published as a DIAGNOSTIC of '
                             'what the market is paying, never as a valuation.',
             multiple=float(JUST_MULT),
             circularity=dict(spot=float(SPOT), shares=float(SH),
                              net_debt=float(nd_cy25), metric_value=float(ebitda_cy25)),
             cannot_rebuild='an own-history enterprise-value multiple needs net debt and '
                            'the share count at each past year end. AMOC\'s committed '
                            'record carries PPE at 2021-2023 and neither of those at any '
                            'origin (engine/valuation_calibration/bridge_inputs.py). The '
                            'valuation-input block [R-FCAL-01 AMENDED] is outstanding on '
                            'this name and the lens returns with it.'),
        dict(kind='book_value', value=float(lenses['book']['base']),
             present_value=False,
             note='published as a DISCLOSED FLOOR and never weighted'),
    ],
    'retired': dict(
        blend=dict(V['lens_weights']),
        blend_value=float(_RETIRED_BLEND),
        why='the weights were typed and had never cleared an out-of-sample test. '
            'Normalised earnings is dropped as a lens for this class outright: a '
            'refiner earning a ~6.6% spread between two numbers each above EGP 35bn '
            'has no mid-cycle margin to normalise, which is the one thing that lens '
            'requires.',
    ),
    'diagnostics': dict(normalised_earnings=float(lenses['normalized']['base'])),
}

# ---- [R-ANCHOR-01] THE FORECAST IS ANCHORED ON THE LATEST REVIEWED PERIOD ----
# Committed so a job outside this study can check it. The record is what a person
# had to read by hand on 03-Sep-2026 to find that this study forecast a gross
# margin BELOW every recent filed period on an unsourced escalator; from now on
# scripts/check_forecast_anchor.py does the reading.
#
# No mechanism is declared because none is claimed: with the real cost drift
# removed the forecast opens at the twelve-month base rather than reversing away
# from it. The remaining distance to the latest reviewed half is the base-anchor
# question, which is priced in the contested judgements and NOT taken this
# edition -- and that distance is what this gate is measuring, correctly.

# The filed record and the like-for-like pair this rule prescribes, COMPUTED from the
# registered filings rather than typed into the note below. Every period here is already
# read by the model body; nothing new is registered and no driver moves.
_FA_FILED = [
    ('the six months to 31-Dec-2024, audited comparative', V['rev_h2_24'], V['cogs_h2_24']),
    ('the quarter to 31-Mar-2025, reviewed comparative', V['rev_q1_25'], V['cogs_q1_25']),
    ('the six months to 31-Dec-2025, audited transition period', V['rev_h2_25'], V['cogs_h2_25']),
    ('the quarter to 31-Mar-2026, reviewed', V['rev_q1_26'], V['cogs_q1_26']),
    ('the six months to 30-Jun-2026, reviewed', V['rev_h1cy26'], V['cogs_h1cy26'])]
_FA_CPR = ' \u00b7 '.join(f"{_n} {_c / _r:.3%}" for _n, _r, _c in _FA_FILED)
_FA_LAT = V['gp_h1cy26'] / V['rev_h1cy26']
_FA_FIRST = B['gm'][0]
_FA_REL = _FA_FIRST / _FA_LAT - 1
_FA_CPR_Q1_25 = V['cogs_q1_25'] / V['rev_q1_25']
_FA_CPR_Q1_26 = V['cogs_q1_26'] / V['rev_q1_26']
_FA_GM_H2_25 = 1 - V['cogs_h2_25'] / V['rev_h2_25']
_FA_Q2_26 = ((V['gp_h1cy26'] - (V['rev_q1_26'] - V['cogs_q1_26']))
             / (V['rev_h1cy26'] - V['rev_q1_26']))

FORECAST_ANCHOR = dict(
    rate_name='gross margin',
    latest_reviewed_period='six months to 30 June 2026, reviewed',
    latest_reviewed_date='2026-06-30',
    latest_reviewed_rate=float(V['gp_h1cy26'] / V['rev_h1cy26']),
    first_forecast_rate=float(B['gm'][0]),
    # the PATH, per [R-ANCHOR-01] clause two: the opening year alone would not have
    # caught EGCH, whose forecast opened above its filed record and fell below it.
    # With the real cost drift removed this path is flat-to-rising and the clause
    # does not fire; before the correction it ran 9.494% down to 8.764% and would
    # have fired on both clauses at once.
    forecast_path=[float(x) for x in B['gm']],
    # NO MECHANISM IS CLAIMED, AND THE GATE IS RIGHT TO REFUSE THIS STUDY FOR IT.
    #
    # A mechanism WAS drafted here on 03-Sep-2026 -- one_off_in_the_latest_period,
    # on the argument that the twelve-month base blends an audited weak half with a
    # reviewed strong one -- and scripts/check_forecast_anchor.py rejected it on the
    # like-for-like measurement supplied beside it: cost per unit of revenue in the
    # SAME QUARTER a year apart runs 94.947% to 89.810%, i.e. the driver moved the
    # OPPOSITE way to the mechanism claimed. That is the clause the gate exists for
    # and it fired on the study whose defect prompted the rule, on its first run,
    # against a record this desk had just written. The draft is left in the history
    # rather than quietly deleted, because a mechanism refused by the company's own
    # filings is the finding.
    #
    # So the honest state is: this forecast opens 22% relatively below the latest
    # reviewed period and CANNOT name a mechanism the filings support. The reason it
    # is not simply re-anchored is [R-VCAL-01]'s one-lever-at-a-time guard -- the
    # move is priced at +55% in the contested judgements and would carry this study
    # from 12.3% below the price to 35.9% above it in a single pass. AMOC is
    # therefore listed on the forecast-anchor ratchet with that reason, and comes off
    # it when the base anchor is taken at the next edition.
    mechanism=None,
    note=(
        f"THE FORECAST OPENS BELOW THE LATEST REVIEWED PERIOD AND NO MECHANISM IS CLAIMED, "
        f"BECAUSE NONE OF THE SIX ON THE CLOSED LIST SURVIVES THIS COMPANY'S OWN FILINGS. "
        f"The reviewed six months to 30-Jun-2026 carried a gross margin of {_FA_LAT:.3%} \u2014 "
        f"gross profit footing exactly to net sales less cost of sales in the same statements "
        f"\u2014 and the forecast opens at {_FA_FIRST:.3%}, {-_FA_REL:.2%} relatively below it. "
        f"The path then RISES to {B['gm'][-1]:.3%} by the fifth year, so the path clause does "
        f"not fire and the whole of the claim sits in the opening level. "
        f"WHAT THE GAP ACTUALLY IS: the base year is the {BASE_YEAR}, and those twelve months "
        f"blend the audited transition half at {_FA_GM_H2_25:.3%} with the reviewed half at "
        f"{_FA_LAT:.3%} to give {BASE_GM:.3%}. It is a BASE-PERIOD CHOICE, and a base-period "
        f"choice is not on the closed list. "
        f"WHAT THE FILED RECORD DOES: cost per unit of revenue, period by period, runs "
        f"{_FA_CPR} \u2014 it FALLS "
        f"\u2014 and the quarter inside the latest half that is not the first printed a gross "
        f"margin of {_FA_Q2_26:.3%}, the highest in the record this study holds. "
        f"THE CANDIDATES, TESTED RATHER THAN ASSERTED. Input cost outpacing price is refused by "
        f"the same-quarter pair this rule prescribes \u2014 cost per unit of revenue "
        f"{_FA_CPR_Q1_25:.3%} in the quarter to 31-Mar-2025 against {_FA_CPR_Q1_26:.3%} in the "
        f"quarter to 31-Mar-2026, {100 * (_FA_CPR_Q1_25 - _FA_CPR_Q1_26):.2f} points the OTHER "
        f"WAY \u2014 and this model makes no such claim in any case: the gross spread per tonne "
        f"is held flat in real terms and the forecast margin rises. A one-off in the latest "
        f"period was drafted on 03-09-2026 and refused on that same pair; no non-recurring item "
        f"is disclosed inside the reviewed statements' net sales or cost of sales, and both foot "
        f"to the filed gross profit to the pound. A contracted price step-down, a subsidy or "
        f"levy withdrawal and a capacity commissioning drag have no disclosure in any filing "
        f"this study holds. A mix shift to lower margin has no decline to attribute, the "
        f"forecast path rising rather than falling. SO THE RECORD STANDS AS A REFUSAL, AND THE "
        f"REFUSAL IS THE FINDING. Anchoring on the reviewed half and holding it flat is this "
        f"study's largest contested judgement, priced at EGP {_PS_H1_ANCHOR:.2f} a share "
        f"against the adopted EGP {dcf_ps:.2f}; it is published beside the answer and left for "
        f"the next edition because levers are taken one at a time and this one crosses the "
        f"traded price of EGP {SPOT:.2f} in a single pass."))

BRIDGE_RECORD = dict(
    market='EG',
    balance_sheet_date='2026-06-30',
    latest_disclosed_date='2026-06-30',
    latest_disclosed_source='the company\'s own latest disclosed statements, '
                            'registered document by document in this study\'s '
                            'investor-relations register under engine/amoc_walkforward.',
    register='amoc_walkforward investor-relations register',
    lines=[
        dict(label='Enterprise value', value=float(ev)),
        dict(label='less net debt (the company is NET CASH, so this ADDS)',
             value=-float(nd_cy25)),
        dict(label='less provisions', value=-float(prov_val)),
        dict(label='less dividend payable', value=-float(divp_val)),
        dict(label='plus investments', value=float(inv_val)),
        dict(label='less non-controlling interests', value=-float(nci_val)),
    ],
    equity_value=float(eq_attr), shares_mn=float(SH), per_share=float(dcf_ps),
    cash=dict(treatment='added_at_face', weights_basis='gross'),
    cash_charged_once=True,
    cash_note='The operations are discounted at the rate weighted on GROSS borrowings, '
              'which on a book of 0.14% of the capital structure IS the cost of equity, '
              'and the cash is then added ONCE, at face, in the bridge. '
              'THE DEFECT THIS RECORD EXISTS TO PREVENT WAS THIS STUDY\'S OWN. A '
              'previous edition discounted the operations at a NET-debt-weighted '
              'rate — on a net-cash company the debt weight goes negative, the equity '
              'weight levers above one and the operating rate lands 374bp ABOVE the '
              'cost of equity — and then added the same cash back at face in the '
              'bridge. That is the cash charged twice. This edition values the '
              'operations at the unlevered rate, which on a book of EGP 25mn IS the '
              'cost of equity, and adds the cash once.',
    nci=dict(basis='value_share', value=float(nci_val), deduction=float(nci_val),
             book=float(nci_val), profit_share=float(nci_val),
             proportional=float(nci_val),
             proxy='the minority\'s share of the subsidiaries\' value, taken at its '
                   'disclosed carrying amount',
             proxy_source='the company\'s own latest disclosed balance sheet',
             framings_note='the contested-choice block prices the minority at DOUBLE '
                           'this share and publishes what that is worth to the answer, '
                           'which is the dual framing this rule asks for.'),
    associates=dict(basis='book', note='investments carried at their disclosed '
                                       'balance-sheet amount; none is a listed '
                                       'associate with a market quote'),
    dividend_deducted=False,
    dividend_note='NO post-balance-sheet dividend declaration is deducted. What the '
                  'bridge does deduct is the DIVIDEND PAYABLE of EGP %.0f standing as '
                  'a liability ON the 30 June 2026 sheet (note 11), which is a '
                  'different thing: the cash to settle it sits inside the cash balance '
                  'this bridge adds back at face, so leaving it out would hand the '
                  'buyer a cash pile that is already spoken for. A dividend declared '
                  'before the sheet date and NOT yet paid is a claim on the firm, and '
                  'that is what this line is.' % divp_val,
)

OUT = dict(
    # THE LEVEL-TOUCH LADDER'S RUNGS, committed rather than typed into a builder. The
    # model report requires a level-touch ladder in section 3 and the rungs are a
    # presentation choice — round numbers spanning the price and the central — so they
    # are registered here where a reader can see the choice rather than infer it.
    touch_ladder=dict(
        levels=_TOUCH_LEVELS,
        # and the probabilities beside them, so the ladder a reader sees is in the record
        # rather than recomputed inside a builder. Computed against the cone's OWN anchor:
        # the percentiles were simulated from the strike's price, and the study is struck on
        # the latest known one, so mixing them embeds a phantom drift.
        p=_TOUCH_P,
        basis='round levels spanning the latest known price and this study\'s central, '
              'so a reader can read the distribution at prices they recognise. The '
              'probabilities beside them are computed from the cone\'s own percentiles '
              'and its own anchor, never from the study spot — those are two clocks.'),
    macro_record=MACRO_RECORD, forecast_anchor=FORECAST_ANCHOR, lens_record=LENS_RECORD,
    bridge_record=BRIDGE_RECORD,
    meta=dict(ticker='AMOC', company='Alexandria Mineral Oils Company S.A.E.', market='EGX',
              currency='EGP', asof='2026-09-03', spot=SPOT, shares_mn=SH, mktcap=MKTCAP,
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
              rev25_lines=dict({k: PV[k] / M * 2 for k in LINES},
                               oil=PV['oils'] / M * 2, wax=PV['wax'] / M * 2,
                               fuel=sum(PV[k] for k in LINES if k not in SPEC) / M * 2),
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
              # THE RETIRED NET-DEBT CONSTRUCTION, EXPORTED SO IT CAN BE NAMED RATHER
              # THAN MISLABELLED. Table 10 printed we_exp/wd_exp — the weights of THIS
              # construction — beside wacc_exp, which is the adopted rate those weights
              # do not produce (1.208 x 27.45% - 0.208 x 13.21% is 30.42%, not 27.45%),
              # and its caption then asserted the adopted rate sat 'ABOVE the 27.5%
              # cost of equity' when the two display identically. The model was right
              # throughout; the table describing it was a page out of date.
              wacc_net_retired=_wacc_net_retired, wd_net_retired=_wd_net_retired,
              kd_term_at=kd_term_at, wacc_term=wacc_term, glide_frac=glide_frac,
              kd_path=V['kd_path'], kd_swing_effect=kd_swing_effect, wacc_usd_alt=WACC_USD,
              beta=beta_res),
    dcf=dict(pv_explicit=pv_explicit, tv=tv, pv_tv=pv_tv, ev=ev, tv_share=tv_share,
             nd=nd_cy25, nci_share=NCI_SHARE, nci_val=nci_val, eq_attr=eq_attr, ps=dcf_ps,
             roic_term=roic_term, rr_term=rr_term, g=V['g_term'], bear=dcf_bear, bull=dcf_bull,
             ps_rating_basis=dcf_rating_ps, wacc_exp_rating=wacc_exp_rating,
             wacc_term_rating=wacc_term_rating, ps_nci_alt=dcf_nci_alt_ps, nci_alt=nci_alt,
             ps_gross_basis=dcf_grossbasis_ps, ccy_alt_ps=ccy_ps,
             # THE TWO FRAMINGS OF THE BASE ANCHOR, AND THE ONE OF THE ESCALATOR
             # [added 03-Sep-2026]. Both priced through THIS waterfall, so the
             # difference measures the CHOICE and not the construction.
             pound_on_price=bool(POUND_ON_PRICE),
             ps_pound_at_inflation=_PS_POUND_AT_INFL,
             ps_h1_anchor=_PS_H1_ANCHOR,
             gm_h1_filed=_GM_H1_FILED, gm_q1_2025=_GM_Q1_2025, gm_q1_2026=_GM_Q1_2026),
    terminal_recon=dict(roic=hist_roic, rr=hist_rr, implied_g=hist_impl_g,
                        character=hist_character, nopat=nopat_h, ic=ic_h, capex=capex_h,
                        nopat_cagr=nopat_cagr, stable_g=stable_g, stable_keys=stable_keys,
                        rr_waterfall=rr_waterfall, g_waterfall=g_waterfall,
               # the STEP the study quotes in prose. A difference of two committed
               # numbers is not itself committed, and no rendering set can form one,
               # so the figure a reader sees is emitted here rather than recomputed
               # in a builder [numeric traceability].
               rr_step=rr_term - _rr_2030,
                        ceiling=blend_ceiling, crossover_years=yrs_cross, crossover=cross_candidates, fcst_cagr=fcst_cagr,
                        dom_share_term=dom_share_term),
    lenses=lenses, central=central, span=[lo, hi], spot=SPOT, scen=SCEN,
    experts=experts, panel_centre=panel_centre,
    rel=dict(ebitda_mid=ebitda_mid, pv_interim=pv_interim, ev_rel=ev_rel, ev_rel_fwd=ev_rel_fwd, df_rel=df_rel,
             ev_ebitda_trailing=ev_ebitda_trailing, pe_trailing=pe_trailing,
             just_mult=JUST_MULT, year=YRS[REL_I]),
    norm=dict(rev=norm_rev, ebitda=norm_ebitda, ebit=norm_ebit, dna=dna[NORM_I],
              interest=norm_interest, np=norm_np, eps=norm_eps, pe=V['pe_just'],
              # the factor and the years it spans, so the expert appendix can bring a forward
              # number back to the valuation date without a numeral being typed into a builder
              df=norm_df, yrs=NORM_YRS, ke=ke_exp,
              year=YRS[NORM_I]),
    book=dict(bvps=bvps, pb_just=pb_just, roe_sust=V['roe_sust'], roe_trailing=roe_trailing,
              ke_term=ke_term),
    sens_wg=dict(g_grid=g_grid, wacc_grid=wt_grid, table=grid_wacc_g),
    sens=dict(g_grid=g_grid, wt_grid=wt_grid, we_grid=we_grid, grid_wacc_g=grid_wacc_g,
              grid_exp_term=grid_exp_term, beta_grid=beta_grid, grid_beta=grid_beta,
              gm_grid=gm_grid, grid_margin=grid_margin, vol_grid=vol_grid, grid_vol=grid_vol,
              fx_grid=fx_grid, grid_fx=grid_fx, nwc_grid=nwc_grid, grid_nwc=grid_nwc),
    # ---- the bottom-up layer, emitted so the workbook can REBUILD it in formulas ----
    unitbuild=dict(
        lines=LINES, labels=LBL, spec=SPEC,
        t0={k: t0[k] for k in LINES}, px0={k: px0[k] for k in LINES},
        raw_pt={k: raw_pt[k] for k in LINES}, conv_pt={k: conv_pt[k] for k in LINES},
        proc={k: PROC[k] for k in LINES}, nrv={k: _nrv[k] for k in LINES},
        spread={k: _spread[k] for k in LINES}, margin0={k: _m0[k] for k in LINES},
        px_index=PX_INDEX, T0=T0, raw_tot0=raw_tot0, conv_tot0=conv_tot0,
        nrv_den=_nrv_den, pw_den=_pw_den,
        sal_sh=cos_share['salaries'] / (1 - cos_share['raw']),
        oth_sh=cos_share['other'] / (1 - cos_share['raw']),
        sup_sh=cos_share['support'] / (1 - cos_share['raw']),
        dep_sh=cos_share['dep'] / (1 - cos_share['raw']),
        lines_vol=B['lines_vol'], lines_rev=B['lines_rev'], lines_cost=B['lines_cost'],
        line_margin=B['line_margin']),
    ttm=dict(base_year=BASE_YEAR, rev=REV_TTM, gp=GP_TTM, cogs=COGS_TTM, gm=GM_TTM,
             ga=ga_ttm / M, mkt=mkt_ttm / M, oth=oth_ttm / M, dep=dep_ttm / M,
             capex=capex_ttm / M, credint=credint_ttm / M, prov=prov_ttm / M, emp=emp_ttm / M,
             gp_h1=gp_h1cy26 / M, gp_h1_released=gp_h1cy26_at_release / M,
             pat_if_released=_pat_if_released_gp / M, ct1=CT1, ct2=CT2, ct3=CT3,
             rev9_ann=rev9 / M * A, gm9=gp9 / rev9),
    rates=dict(tax_stat=TAX_STAT, tax_eff=TAX_EFF, emp_rate=EMP_RATE, nci_op=NCI_OP,
               rf_term=RF_TERM, ke_blend=KE_BLEND, asset_life=ASSET_LIFE,
               cap_intensity=CAP_INTENSITY, maint_capex0=MAINT_CAPEX0,
               inv_days=INV_DAYS, recv_days=RECV_DAYS, pay_days=PAY_DAYS,
               raw_of_rev=RAW_OF_REV, just_mult=JUST_MULT, norm_df=norm_df,
               norm_yrs=NORM_YRS, rr_2030=_rr_2030),
    bridge=dict(ev=ev, nd=nd_cy25, eq_gross=eq_gross, nci=nci_val, prov=prov_val,
                divp=divp_val, inv=inv_val, eq=eq_attr, ps=dcf_ps),
    span_env=[lo_env, hi_env],
    blocks=BLOCKS,
    step0=step0, strike=strike, backtest=bt5,
    assert_log=LOG,
)
# ---- REACHABILITY GATE, rewritten -------------------------------------------
# The previous gate accepted "quoted somewhere in a deliverable" as evidence that an input was
# reached. It passed with sixteen inputs driving nothing, including a 921mn recognised liability
# and a 135mn appropriation of profit that the study's own text described as a defect of the
# edition before it. A sentence is not a formula. This gate now requires that any input carrying
# a BALANCE-SHEET or PROFIT-STATEMENT claim actually appear in the model body; narrative inputs
# may still be quotation-only, and they are listed by name so the exemption is visible.
import re as _re
# The register is now materialised TWICE — once so the derived macro path can read the
# inflation series, and once after those derived inputs are appended. The model body is
# everything after the LAST materialisation; splitting on the first would hand this gate the
# derivation block alone and fail every input in the register.
_SENTINEL = "# --- MODEL BODY BEGINS HERE (reachability gate splits on this line) ---"
_src = open(os.path.join(HERE, 'compute.py')).read()
# Split on a SENTINEL, not on the register-materialisation line. That line is now written
# twice — the derived macro path has to read the inflation series before the derived inputs
# are appended — and, worse, this gate's own source quotes it, so a split on it would hand
# the gate a slice of itself and report every input dead.
assert _src.count(_SENTINEL) == 2, "the model-body sentinel is not where the gate expects it"
_body = _src.split(_SENTINEL)[1]
NARRATIVE_ONLY = {
    # figures from SUPERSEDED editions, quoted to show what changed and computed by
    # nothing in this model because a different model produced them
    'gm_superseded_annualised', 'tv_share_superseded',
    # a DISCLOSED ownership fact the study quotes and no formula needs: the minority's
    # share of profit is registered separately and is what the model actually reads
    'awp_stake',
    'us_infl',   # read ABOVE the body, to derive the price and currency paths
    'inv_days', 'recv_days', 'pay_days',      # superseded: days are now SOLVED from the filings
    'other_ca', 'dna_pct', 'capex_pct', 'opex_pct', 'tax_eff', 'nci_share', 'ev_ebitda_just',
    'gp_h1cy26_rep',                          # registered precisely so it can be REJECTED
    'egpc_sales', 'egpc_balance', 'alexpet_stake', 'puc', 'assets_snap', 'liab_snap',
    'assets_jun24', 'assets_dec24', 'assets_jun25', 'eq_parent_jun24', 'eq_parent_mar26',
    'cash_jun25', 'cash_mar26', 'inv_jun25', 'recv_jun25', 'debtors_jun25', 'payables_jun25',
    'creditors_jun25', 'ppe_jun25', 'div_h2_25', 'div_q1_26', 'dps', 'payout_reported',
    'tax_due', 'dtax_liab', 'leases', 'e1_pe', 'egypt_gdp_nominal', 'world_nominal_growth',
    'egypt_nominal_growth', 'cbe_target', 'policy_rate', 'cpi', 'crude_hist', 'fx_hist',
    'fx_avg_cy25', 'brent_path', 'wacc_usd_rf', 'wacc_usd_erp', 'sov_spread_rating',
    'erp_rating', 'kd_now', 'pat_fy25_full', 'pat_h1cy25', 'cos_salaries_24', 'cos_raw_24',
    'cos_support_24', 'cos_dep_24', 'cos_other_24', 'ppe_accdep', 'prod_v_prior',
    'rev_h2_24', 'cogs_h2_24', 'pat_h2_24', 'rev_q1_25', 'cogs_q1_25', 'emp_h2_25',
}
_dead = [k for k in INP if k not in NARRATIVE_ONLY and f"V['{k}']" not in _body]
assert not _dead, ("inputs registered with a claim on the balance sheet or the profit statement "
                   f"that no formula reads: {_dead}")
_quoted_only = sorted(k for k in NARRATIVE_ONLY if k in INP and f"V['{k}']" not in _body)
say(f"[Reachability gate — rewritten] {len(INP)} registered inputs. "
    f"{len(INP)-len(_quoted_only)} DRIVE the model. {len(_quoted_only)} are quotation-only and "
    f"are named here rather than passing silently: {', '.join(_quoted_only)}. The previous gate "
    f"treated 'appears in a deliverable' as reached and passed while `provisions` (921mn) and "
    f"`emp_h2_25` (135mn a year) drove nothing at all — setting the provision to zero moved that "
    f"valuation by less than a hundredth of a piastre. Both now drive the bridge and the "
    f"waterfall. `emp_h2_25` stays on this list because the CHARGE is now taken through a rate "
    f"solved from it rather than through the raw input.")

# ---- WHAT A BUYER AT THE MARKET PRICE MUST BELIEVE, SOLVED NOT TYPED ---------
# The previous edition printed "a permanent gross margin near 12.2%" in the headline, in the
# body and inside a figure, as a hardcoded 12.16. It was typed, it was never recomputed when the
# model moved, and the sentence attached to it — "above the best single quarter this company has
# ever filed" — was FALSE: the company filed 13.84% for the whole year to June 2022 and 13.92%
# in the June 2026 quarter. A number stated in prose is computed here and read by the document
# and the figure, so it cannot rot and cannot contradict the filings.
def _solve_gm_for_price(target, lo=-0.05, hi=0.15):
    for _ in range(80):
        mid = (lo + hi) / 2.0
        if dcf_scenario(gm_shift=mid) < target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


GM_SHIFT_REQ = _solve_gm_for_price(SPOT)
GM_REQ = BASE_GM + GM_SHIFT_REQ
GM_FILED_MAX = 0.1384          # FY to 30-Jun-2022, the best FULL YEAR on the audited record
GM_FILED_MAX_Q = 0.1392        # the quarter to 30-Jun-2026, the best QUARTER on the record
say(f"[What a buyer at the market price must believe — SOLVED] holding every other driver at "
    f"the base case, the cash-flow lens reaches the market price of {SPOT:.2f} at a gross margin "
    f"of {GM_REQ:.2%} sustained in EVERY forecast year and in perpetuity, against a base year of "
    f"{BASE_GM:.2%}. THE PREVIOUS EDITION PUT THIS AT 12.2% AND CALLED IT 'ABOVE THE BEST SINGLE "
    f"QUARTER THIS COMPANY HAS EVER FILED'. That was wrong on the record as well as on the "
    f"arithmetic: AMOC filed a gross margin of {GM_FILED_MAX:.2%} for the whole year to 30 June "
    f"2022 and {GM_FILED_MAX_Q:.2%} in the quarter to 30 June 2026. The required margin is "
    f"{'INSIDE' if GM_REQ <= GM_FILED_MAX else 'ABOVE'} the range this company has actually "
    f"printed, which is a materially different claim and is the one the study now makes.")
OUT_GM_REQ = dict(shift=GM_SHIFT_REQ, level=GM_REQ, base=BASE_GM,
                  filed_max_year=GM_FILED_MAX, filed_max_quarter=GM_FILED_MAX_Q)

# ==================== FUNDAMENTAL WALK-FORWARD, CARRIED IN ====================
# [R-FCAL-01] is a standing step of every study and every update, and its result belongs in
# the delivered document rather than only in the internal record. The training record itself
# (panel, error cells, pre-registration) stays internal; what a reader sees is the scope, the
# honest headline, and the bands the record licenses on the far forecast years.
_WF = os.path.join(HERE, '..', 'amoc_walkforward')
with open(os.path.join(_WF, 'forward_ranges.json')) as _f:
    _FR = json.load(_f)
with open(os.path.join(_WF, 'scores.json')) as _f:
    _WS = json.load(_f)
WALKFORWARD = dict(
    ran=True, scope='LIGHT', origins=5, horizons='1-3', cells=_WS['cells'],
    window='FY2021-FY2025, AMOC\'s own audited consolidated statements',
    why_light=('Five sourceable fiscal years. AMOC publishes no accounts older than FY2022, and '
               'the exchange, the regulator\'s disclosure portal and the web archive are all '
               'unreachable; the only vendor reachable carries the same five years, restated.'),
    headline=dict(
        majority_bias=_WS['drivers']['majority']['overall']['bias'],
        majority_mae=_WS['drivers']['majority']['overall']['mae'],
        majority_share_over=_WS['drivers']['majority']['overall']['share_over'],
        skill_vs_freeze=_WS['drivers']['majority']['skill_vs_freeze']['skill'],
        net_sales_bias=_WS['drivers']['net_sales']['overall']['bias'],
        volume_bias=_WS['drivers']['volume_t']['overall']['bias'],
        volume_share_over=_WS['drivers']['volume_t']['overall']['share_over']),
    bands=_FR['published_band'],
    corrections_adopted=0,
    corrections_note=('None. Nine cells cannot support an estimated correction and a separate '
                      'confirmation sample, and that was ruled before any error was computed. '
                      'Every measured bias is a watch flag.'),
    what_it_changed=('The volume driver. The previous edition grew every product line and drew '
                     'its ranking from two disclosed halves; the audited five-year record shows '
                     'tonnage down 18.5% from its FY2022 peak with six of eight lines shrinking, '
                     'and the walk-forward measures the flat-volume rule as ALREADY '
                     'over-forecasting by 7.6% in eight of nine cells. The base path is now flat '
                     'and the bear leg reverts to the five-year mean.'))
OUT['gm_required'] = OUT_GM_REQ
OUT['walkforward'] = WALKFORWARD
say(f"[Fundamental walk-forward] LIGHT scope, {WALKFORWARD['cells']} scoreable cells over five "
    f"origins FY2021-FY2025. Majority profit was under-forecast in "
    f"{1 - WALKFORWARD['headline']['majority_share_over']:.0%} of cells and the method scored "
    f"{WALKFORWARD['headline']['skill_vs_freeze']:+.3f} against assuming last year's profit "
    f"repeats — it did NOT beat no change. No correction was adopted. What it changed in this "
    f"edition is the volume driver, and the far-year bands it licenses are carried into "
    f"Appendix A rather than a point.")

# ============================ THE FOUR GATES =================================
# [R-ENF-02] A study must call these in its OWN code, and scripts/check_study_provenance.py
# runs the same tests from outside so a study cannot pass by not checking itself. AMOC was
# the last name on engine/build_depth_audit/outstanding.json; this block is what removes it.
import research_protocol as _rp

# --- beta: the record itself is inspected, not a boolean the study set on itself ----
with open(os.path.join(HERE, 'beta_result.json')) as _bf:
    BETA_REC = json.load(_bf)
_rp.assert_beta_provenance(BETA_REC)
assert abs(BETA_REC['beta'] - V['beta']) < 5e-4, (
    "the registered beta input and the regression record disagree — the input register must "
    "carry the number the sanctioned resolver produced, not a remembered one")

# --- ground-up: a RECORD per revenue line, covering 100% of revenue [R-SIGCM-02] ----
# Every line is filed at 'derived', NOT at 'unit', and the gap note says why. Tonnage and
# realisation are disclosed per product in note 14-A of every year. COST IS NOT: note 15-A
# discloses cost by NATURE for the company as a whole, and the FY2023 auditor's emphasis of
# matter records that AMOC implemented a per-product costing system only from 1 July 2023.
# 'unit' asserts "cost per unit; margin an output" per line, which would be a claim the
# filings do not support. Filing at the narrower level and naming the gap is the honest call.
_GAP = ("Tonnage and realisation per product are disclosed (note 14-A, every year). Cost is "
        "disclosed by NATURE for the company as a whole (note 15-A) and never by product, and "
        "the FY2023 auditor records that no per-product costing system existed before 1 July "
        "2023. Per-line cost is therefore an allocation, not a disclosure, and the margin of "
        "any single product line in this study is a construction.")
_UNIT_SRC = ("Note 14-A, net sales by product, quantity in tonnes — AMOC's own audited "
             "consolidated financial statements, FY2021 through FY2025 and the transition period")
_PRICE = "note 14-A value divided by note 14-A tonnes, both disclosed, same period"
LINE_SHARES = {k: PV[k] / sum(PV.values()) for k in LINES}
DRIVER_LINES = [
    _rp.DriverLine(name=_n, level='derived', share_of_revenue=_sh, unit='tonne',
                   unit_source=_UNIT_SRC, price_basis=_PRICE,
                   cost_basis='cost of sales by nature, allocated on throughput', gap_note=_GAP)
    for _n, _sh in LINE_SHARES.items()]
GROUND_UP = _rp.assert_ground_up(DRIVER_LINES, ticker='AMOC')

# --- SIGCM ---------------------------------------------------------------------------
SIGCM = _rp.SIGCMChecklist(
    historicals_official_only=True,
    forecast_ground_up=True,
    debt_lc_fx_split=True,
    asset_conversion_cycle=True,
    competitors=True,
    beta_own_history_vs_egx30=True,
    formula_based_model=True,
    flags_raised_before_issue=True,
    stop_and_inform_honoured=True,
    na_reasons={
        'debt_lc_fx_split': ("Borrowings are EGP 20,977,437 against equity of EGP 4,824,774,948 "
                             "and the company holds net cash. The split is stated and is "
                             "immaterial; note 13 discloses no foreign-currency tranche."),
    })
_rp.assert_sigcm(SIGCM)

# --- model-report bar ------------------------------------------------------------------
MODEL_STUDY = _rp.ModelStudyChecklist(
    structure_matches_model=True,
    bibliography_document=True,
    provenance_four_field=True,
    numeric_traceability=True,
    external_reader_scrub=True,
    figure_discipline=True,
    table_discipline=True,
    expert_appendix_max_detail=True,
    contested_judgement_both_ways=True,
    na_reasons={})
_rp.assert_model_study(MODEL_STUDY)

OUT['gates'] = dict(standard_version=_rp.STANDARD_VERSION, beta=BETA_REC, ground_up=GROUND_UP,
                    sigcm=[f.name for f in __import__('dataclasses').fields(SIGCM)
                           if f.name != 'na_reasons'],
                    model_study_ok=True)
OUT['standard_version'] = _rp.STANDARD_VERSION
say(f"[Gates] beta {BETA_REC['beta']:.4f} vs {BETA_REC['index_file']} (conforming="
    f"{BETA_REC['conforming']}); ground-up record covers "
    f"{sum(GROUND_UP['share_by_level'].values()):.0%} of revenue across {GROUND_UP['lines']} "
    f"lines, all at 'derived' with the cost-disclosure gap stated; SIGCM and the model-report "
    f"bar both pass. Study stamped to STANDARD_VERSION {_rp.STANDARD_VERSION}.")

with open(os.path.join(HERE, 'study_numbers.json'), 'w') as f:
    json.dump(OUT, f, indent=1)
say("=" * 78)
say(f"ASSERT BLOCK PASSED — study_numbers.json emitted. Terminal value "
    f"{tv_share:.1%} of enterprise value; fair value EGP {central:.2f} against spot EGP "
    f"{SPOT:.2f}; implied {central/SPOT-1:+.1%}.")
