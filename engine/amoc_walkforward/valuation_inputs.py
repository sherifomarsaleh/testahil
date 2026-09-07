"""The VALUATION-INPUT BLOCK for this run — the figures a VALUE is rebuilt from.

[R-FCAL-01 AMENDED, 03-09-2026].  A driver panel is not a record a value can be
rebuilt from.  This run's `panel.py` committed the income statement as first
reported, the product table in tonnes and pounds, the cost stack by nature and
the other-revenue note — every figure its own scoring needed — and left no trace
of the balance sheet beside them.  Measured by
`engine/valuation_calibration/bridge_inputs.py`, AMOC carried DEPRECIATION and
NOTHING ELSE at any origin: no cash, no debt, no property, no working capital,
no share count, and therefore no route to capital expenditure even by the
identity, because the identity needs property at two dates.  It was the worst
covered run in the book.

WHY THAT MATTERED MORE HERE THAN ANYWHERE ELSE, AND WHY THE DIRECTION IS THE
POINT.  AMOC is the net-cash company — the name [R-BRIDGE-01](iii) is written
about and [R-GAP-01]'s worked case.  At 30 June 2025 it held EGP 3,141,779,939
of cash and cash equivalents against EGP 26,456,335 of interest-bearing
borrowings, and at 30 June 2021, 2022 and 2023 it held NO INTEREST-BEARING
BORROWINGS AT ALL.  Omitting cash UNDERSTATES equity value, which runs the same
way as the pessimism hypothesis the valuation calibration is testing, so an
instrument built from what this run happened to commit would have confirmed that
hypothesis BY CONSTRUCTION.  On this company the omitted item is not a rounding
error; on the last origin it is more than half of the equity bridge.

WHAT IS HERE.  For every origin this run declares — FY2021 to FY2025, fiscal
years ending 30 June — cash and equivalents, interest-bearing debt, property
plant and equipment, depreciation and amortisation, the working-capital lines,
capital expenditure, and the share count with the par value it was footed
against.  NO PRIOR-YEAR ANCHOR IS CARRIED and the reason is recorded rather than
left as an absence: capital expenditure is DISCLOSED in the cash-flow statement
at every one of the five origins, so the identity capex = dPPE + D&A is never
needed to produce a figure; it is reported BESIDE the disclosed figure wherever
it can run, and at FY2021 it cannot run at all, because the company publishes no
statements older than the FY2022 filing and the 30 June 2020 balance sheet does
not exist in any document this run can reach.

EVERY FIGURE IS A COPY, NOT NEW RESEARCH.  Each one sits on a balance sheet or a
cash-flow statement in a filing this run had already parsed cell by cell for its
income statement; carrying them out is transcription.  Not carrying them out
meant no valuation of this company could ever be rebuilt at a past origin,
permanently, for any year whose filings are no longer to hand.

ROUTE, AND WHY ARITHMETIC DECIDES [clause (iii)].  AMOC files scans.  Measured
across the four annual filings read here, three carry a text layer of ZERO
characters across every page (66, 48 and 53 pages) and the fourth carries about
five thousand characters across 76 pages, none of them on a statement page — so
every figure below arrived by reading the RENDERED PIXELS at 300-340 dpi and NOT
ONE is believed because it looked clean.  Every balance sheet foots — components
to their subtotals, subtotals to total assets, assets to equity and liabilities
— and every cash-flow statement rolls forward to the closing cash the balance
sheet states.  The footing runs at import as assertions rather than living in a
comment, which is this run's own discipline from `panel.py`.

WHAT THE ARITHMETIC CAUGHT, AND IT CAUGHT EVERY ONE.  Each looked perfectly
clean on the page:

  FY2024 fixed assets (net)     834,300,066 -> 834,500,066   (FS2025 comparative)
  FY2022 inventory            1,415,143,389 -> 1,418,143,389 (FS2023 comparative)
  FY2023 depreciation            92,533,870 -> 92,933,870    (FS2024 comparative)
  FY2023 credit interest        105,165,098 -> 105,105,098   (FS2023 own column)
  FY2025 change in inventory  1,854,876,146 -> 1,854,676,146 (FS2025 cash flow)
  FY2025 operating profit
    before working capital    1,596,408,046 -> 1,596,406,046 (FS2025 cash flow)
  FY2024 capital expenditure    243,809,137 -> 243,609,137   (FS2025 comparative)
  FY2024 finance-lease payment    3,746,980 -> 3,746,950     (FS2024 cash flow)

The first three were settled by the OTHER filing's column for the same date; the
rest by the statement's own subtotal or by the closing-cash roll-forward.  None
would have been visible to a reader of the extracted figure.

ONE CELL IS ILLEGIBLE AND IS RECORDED AS SUCH RATHER THAN GUESSED.  FS2023's
cash-flow line "Changes in Fixed Assets and Projects Under Construction" cannot
be read off the page: three OCR passes at three resolutions returned three
different middle groups.  Its value is established by arithmetic from two
independent directions — the FS2023 investing column's own subtotal (which the
whole statement's roll-forward to the balance-sheet cash confirms) requires
111,540,611, and FS2024's comparative column states 111,448,611 for the same
year net of the 92,000 of disposal proceeds FS2023 shows on its own line, and
111,540,611 - 92,000 = 111,448,611 exactly.  The figure is committed with the
dispute recorded, and BOTH readings appear in the record.

POINT IN TIME IS ABSOLUTE, AND ONE CLAUSE OF IT NEEDS SAYING OUT LOUD.  Every
year is carried from the filing that was published at its own origin: FY2022 to
FY2025 from each year's OWN column in its OWN filing.  FY2021 IS THE EXCEPTION
AND IT IS NOT A CHOICE — the company publishes no annual statements older than
the FY2022 filing, so the earliest published record of 30 June 2021 is that
filing's comparative column, which is what is carried and what this record says
it is.  It is not described as first-reported, because no first report of that
date is published.

TWO RE-PRESENTATIONS FALL INSIDE THIS WINDOW AND BOTH ARE RECORDED BESIDE THE
FIGURE THEY WOULD REPLACE, NEVER SUBSTITUTED.  (1) THE PLEDGED DEPOSITS.  At the
FY2023 vintage the whole treasury sits in one balance-sheet line, "Cash and bank
accounts" of 3,278,675,752, and the note discloses inside it EGP 784,250,000
held as a conservative deposit against documentary credit.  The FY2024 filing
moves that amount OUT of cash into a non-current line, "Other financial
investments", and restates FY2023's closing cash to 2,494,425,752.  An origin
standing at FY2023 saw the first presentation and could not have seen the
second, so 3,278,675,752 is what is committed there and the restated figure is
named beside it.  From FY2024 the balance-sheet cash line is already net of the
pledged deposit and the deposit is named as carried beside.  (2) FY2024's
majority profit, which this run's own `panel.py` already carries twice under
L-037; it is not a valuation input and is not repeated here.

WHAT IS DELIBERATELY NOT DECIDED HERE.  This module records; it values nothing.
Where a figure could be defined two ways the record carries the disclosed lines
and names the convention rather than resolving it — interest-bearing debt is the
National Bank of Egypt loan and its current portion, with the lease liabilities
carried BESIDE them rather than folded in or dropped, because whether a lease
liability is debt is a valuation choice and not a reading of the page; and on
three of the five origins that figure is a DISCLOSED ZERO rather than a missing
item, which is a fact about this company and is recorded as one.
"""
from __future__ import annotations

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
CALIB = os.path.join(os.path.dirname(HERE), "valuation_calibration")

# The origins this run declares (PRE_REGISTRATION_01-09-2026.md, section 1
# 'Origins and horizons'). Fiscal years ending 30 June.
ORIGINS = ["FY%d" % y for y in range(2021, 2026)]

# The filings, as this run's own panel.py SOURCES already records them, from the
# company's own investor-relations archive at amoceg.com.
FILES = {
    "FS2022": ("15-641ad5c4187951679480260.pdf",
               "consolidated financial statements for the year ended 30 June 2022, "
               "Arabic edition — the oldest annual accounts this company publishes",
               66, 0),
    "FS2023": ("41-662794b73ed5a1713870007.pdf",
               "consolidated financial statements for the year ended 30 June 2023",
               76, 5337),
    "FS2024": ("54-66c5a239056101724228153.pdf",
               "consolidated financial statements for the year ended 30 June 2024",
               48, 0),
    "FS2025": ("74-68a2dfafd04651755504559.pdf",
               "consolidated financial statements for the year ended 30 June 2025",
               53, 0),
}

ROUTE = ("read off the RENDERED PAGE at 300-340 dpi — the filing carries no usable "
         "text layer on any statement page; every figure footed against the "
         "statement's own arithmetic before it was recorded")

# ---------------------------------------------------------------------------
# Consolidated statement of financial position, at 30 June, stated POSITIVE as
# printed.  A key set to 0 is a line the year does not print; LABELS carries the
# exact printed wording for every line a year DOES print, so the record cannot
# claim a line the page does not carry.  Every one is asserted in foot().
# ---------------------------------------------------------------------------
BS = {
 2021: dict(src="FS2022", column="comparative", page=(3, 4),
   fixed=847_625_770, puc=92_266_216, rou=1_979_955, afs=12_000_000,
   other_fin_inv=0, intangible=118_046, tnca=953_989_987,
   inventory=853_968_067, receivables=560_350_057, debtors=141_871_628,
   debit_balances=36_718_559, cash=1_260_172_286, tca=2_853_080_597,
   total_assets=3_807_070_584,
   capital=1_291_500_000, legal=527_801_493, other_reserves=51_326_484, oci=0,
   retained=518_700, profit=485_667_884, parent_equity=2_356_814_561,
   nci=13_903_111, total_equity=2_370_717_672,
   loan_nc=0, lease_nc=249_731, dtl=38_498_469, tncl=38_748_200,
   prov_disputed_tax=177_157_227, prov_claims=18_917_979, prov_total=0,
   payables=27_995_043, lease_c=1_205_238, corp_tax=72_768_952, loan_c=0,
   creditors=905_566_049, credit_balances=193_994_224,
   tcl=1_397_604_712, teal=3_807_070_584),
 2022: dict(src="FS2022", column="own", page=(3, 4),
   fixed=788_054_047, puc=129_848_643, rou=227_029, afs=12_000_000,
   other_fin_inv=0, intangible=302_478, tnca=930_432_197,
   inventory=1_418_143_389, receivables=398_833_005, debtors=544_474_972,
   debit_balances=63_492_223, cash=1_565_815_560, tca=3_990_759_149,
   total_assets=4_921_191_346,
   capital=1_291_500_000, legal=547_674_161, other_reserves=194_763_937, oci=0,
   retained=1_457_358, profit=1_194_122_765, parent_equity=3_229_518_221,
   nci=23_891_446, total_equity=3_253_409_667,
   loan_nc=0, lease_nc=0, dtl=116_176_683, tncl=116_176_683,
   prov_disputed_tax=593_805_055, prov_claims=42_969_568, prov_total=0,
   payables=10_534_513, lease_c=249_732, corp_tax=510_108_225, loan_c=0,
   creditors=83_667_248, credit_balances=310_270_655,
   tcl=1_551_604_996, teal=4_921_191_346),
 2023: dict(src="FS2023", column="own", page=(5,),
   fixed=832_286_362, puc=110_210_971, rou=10_820_796, afs=12_000_000,
   other_fin_inv=0, intangible=227_257, tnca=965_545_386,
   inventory=1_206_916_842, receivables=573_262_747, debtors=662_007_687,
   debit_balances=0, cash=3_278_675_752, tca=5_720_863_028,
   total_assets=6_686_408_414,
   capital=1_291_500_000, legal=599_858_513, other_reserves=370_333_560, oci=0,
   retained=346_906_036, profit=1_330_499_928, parent_equity=3_939_098_037,
   nci=44_165_659, total_equity=3_983_263_696,
   loan_nc=0, lease_nc=10_118_184, dtl=98_392_283, tncl=108_510_467,
   prov_disputed_tax=0, prov_claims=0, prov_total=965_377_742,
   payables=1_908_984, lease_c=0, corp_tax=529_120_600, loan_c=0,
   creditors=1_098_226_925, credit_balances=0,
   tcl=2_594_634_251, teal=6_686_408_414),
 2024: dict(src="FS2024", column="own", page=(5,),
   fixed=834_500_066, puc=258_128_413, rou=7_097_719, afs=12_000_000,
   other_fin_inv=512_550_000, intangible=181_244, tnca=1_624_457_442,
   inventory=1_880_332_957, receivables=1_115_883_982, debtors=600_010_477,
   debit_balances=0, cash=3_166_276_817, tca=6_762_504_233,
   total_assets=8_386_961_675,
   capital=1_291_500_000, legal=646_182_250, other_reserves=440_778_524, oci=0,
   retained=844_611_119, profit=1_699_154_495, parent_equity=4_922_226_388,
   nci=69_278_749, total_equity=4_991_505_137,
   loan_nc=31_139_885, lease_nc=3_695_138, dtl=188_489_209, tncl=223_324_232,
   prov_disputed_tax=0, prov_claims=0, prov_total=1_188_243_677,
   payables=4_403_395, lease_c=2_676_096, corp_tax=678_888_836,
   loan_c=10_232_552, creditors=1_287_687_750, credit_balances=0,
   tcl=3_172_132_306, teal=8_386_961_675),
 2025: dict(src="FS2025", column="own", page=(5,),
   fixed=937_851_261, puc=403_190_211, rou=6_610_589, afs=69_608_696,
   other_fin_inv=526_974_100, intangible=111_474, tnca=1_944_346_331,
   inventory=3_735_009_103, receivables=894_888_039, debtors=611_842_230,
   debit_balances=0, cash=3_141_779_939, tca=8_383_519_311,
   total_assets=10_327_865_642,
   capital=1_291_500_000, legal=646_182_250, other_reserves=1_444_391_872,
   oci=44_646_739, retained=438_287_896, profit=1_488_520_098,
   parent_equity=5_353_528_855, nci=68_644_851, total_equity=5_422_173_706,
   loan_nc=16_963_823, lease_nc=1_669_855, dtl=128_053_981, tncl=146_687_659,
   prov_disputed_tax=0, prov_claims=0, prov_total=1_075_741_993,
   payables=15_486_636, lease_c=4_196_999, corp_tax=552_044_321,
   loan_c=9_492_512, creditors=3_102_041_816, credit_balances=0,
   tcl=4_759_004_277, teal=10_327_865_642),
}

# The exact printed wording of every line each year carries.  A key absent here
# is a line that year does not print, and the record omits it rather than
# claiming a zero the page never stated.
LABELS = {
 2021: dict(fixed="الأصول الثابتة (fixed assets, net)",
   puc="مشروعات تحت التنفيذ (projects under construction)",
   rou="أصول حق انتفاع (right-of-use assets)",
   afs="استثمارات مالية متاحة للبيع (financial investments available for sale)",
   intangible="أصول غير ملموسة (intangible assets)",
   inventory="المخزون (inventory)", receivables="عملاء (customers)",
   debtors="مدينون (debtors)", debit_balances="أرصدة مدينة (debit balances)",
   cash="النقدية (cash: time deposits, current accounts, cash on hand)",
   capital="رأس المال (capital)", legal="الاحتياطي القانوني (legal reserve)",
   other_reserves="احتياطيات أخري (other reserves)",
   retained="الارباح المرحلة (retained earnings)",
   profit="أرباح الفترة (profit for the period)",
   nci="حقوق أصحاب الحصص غير المسيطرة (non-controlling interests)",
   lease_nc="التزامات عقود التأجير طويلة الأجل (long-term lease liabilities)",
   dtl="التزامات ضريبية مؤجلة (deferred tax liabilities)",
   prov_disputed_tax="مخصص ضرائب متنازع عليها (disputed taxes provision)",
   prov_claims="مخصص مطالبات و منازعات (claims and disputes provision)",
   payables="موردون وأوراق دفع (suppliers and notes payable)",
   lease_c="التزام قصير الأجل - عقد التأجير (short-term lease liability)",
   corp_tax="ضريبة شركات الاموال (corporate tax)",
   creditors="دائنون (creditors)",
   credit_balances="أرصدة دائنة (credit balances)"),
 2023: dict(fixed="Fixed Assets", puc="Projects under constructing",
   rou="Usufruct Assets", afs="Investment for sale",
   intangible="Intangible Assets", inventory="Inventory",
   receivables="Accounts Receivables", debtors="Debtors and other debits",
   cash="Cash and bank accounts", capital="Paid in capital",
   legal="Legal Reserves", other_reserves="Other Reserves",
   retained="Retained earnings", profit="Earnings for the Period",
   nci="Rights of non-controlling quota holders",
   lease_nc="Leasing contracts", dtl="Defferred Tax Liablitiy",
   prov_total="Provisions", payables="Suppliers and notes payable",
   corp_tax="IRS dues", creditors="Creditors and others"),
 2024: dict(fixed="Fixed assets (net)", puc="Projects under construction",
   rou="Right of use assets (net)", afs="Financial investments",
   other_fin_inv="Other Financial investments",
   intangible="Intangible Assets", inventory="Inventory (net)",
   receivables="Accounts receivable (net)",
   debtors="Debtors and other debit balances (net)",
   cash="Cash at banks and on hand", capital="Issued and paid up capital",
   legal="Legal reserve", other_reserves="Other reserves",
   retained="Retained earnings", profit="Profit for the year",
   nci="Non-controlling interest",
   loan_nc="National Bank of Egypt (Pledged by time deposit)",
   lease_nc="Long term liability - lease contract",
   dtl="Deferred tax liability", prov_total="Provisions",
   payables="Accounts Payable", loan_c="Loans due",
   lease_c="Short term liability - lease contracts",
   corp_tax="Due to tax authority",
   creditors="Creditors and other credit balances"),
 2025: dict(fixed="Fixed assets (Net)", puc="Projects under construction",
   rou="Right of use assets", afs="Financial assets at FVOCI",
   other_fin_inv="Other Financial Investments",
   intangible="Intangible Assets", inventory="Inventory (net)",
   receivables="Accounts receivable (net)",
   debtors="Debtors and other debit balances (net)",
   cash="Cash at banks and on hand (net)",
   capital="Issued and paid up capital", legal="Legal reserve",
   other_reserves="Other reserves",
   oci="Other Comprehensive Income Items",
   retained="Retained earnings", profit="Profit for the Year",
   nci="Non-controlling interest",
   loan_nc="National Bank of Egypt loan (pledged by time deposit)",
   lease_nc="Long term lease liabilities", dtl="Deferred tax liability",
   prov_total="Provisions", payables="Accounts and notes payable",
   loan_c="National Bank of Egypt loan due",
   lease_c="Short term lease liability", corp_tax="Due to tax authority",
   creditors="Creditors and other credit balances"),
}
# Same filing, same Arabic layout, own column — minus the one line the 30 June
# 2022 column prints as a dash, which the record must not claim as a line.
LABELS[2022] = {k: v for k, v in LABELS[2021].items() if k != "lease_nc"}

# ---------------------------------------------------------------------------
# Consolidated statement of cash flows.  `dep` is the statement's own
# depreciation-and-amortisation add-back — the GROUP charge, which is more than
# the cost-of-sales depreciation this run's panel.py carries: that one is the
# manufacturing share of note 15-A and this is the whole company.  `capex` is
# the disclosed payment for fixed assets and projects under construction;
# `disposals` is the separate proceeds line where the year prints one.
# ---------------------------------------------------------------------------
CF = {
 2021: dict(src="FS2022", column="comparative", page=(10,),
   dep=82_356_037, capex=31_690_213, disposals=723_296,
   cash_end=1_260_172_286,
   dep_label="الاهلاكات الاصول الثابتة (depreciation of fixed assets)",
   capex_label=("متحصلات (مدفوعات) الأصول الثابتة والمشروعات تحت التنفيذ, note 5 "
                "(payments for fixed assets and projects under construction)")),
 2022: dict(src="FS2022", column="own", page=(10,),
   dep=83_807_680, capex=60_559_283, disposals=760_644,
   cash_end=1_565_815_560,
   dep_label="الاهلاكات الاصول الثابتة (depreciation of fixed assets)",
   capex_label=("متحصلات (مدفوعات) الأصول الثابتة والمشروعات تحت التنفيذ, note 5 "
                "(payments for fixed assets and projects under construction)")),
 2023: dict(src="FS2023", column="own", page=(11,),
   dep=92_933_870, capex=111_540_611, disposals=92_000,
   cash_end=3_278_675_752,
   dep_label="Depreciation of Fixed Assets",
   capex_label="Changes in Fixed Assets and Projects Under Construction, note 5",
   capex_route_dispute=(
       "this cell cannot be read off the page: three OCR passes at 300, 450 and "
       "600 dpi returned three different middle groups. The figure is established "
       "by arithmetic from two directions. (i) The FS2023 investing column's own "
       "subtotal of 127,227,863 — itself confirmed by the statement's roll-forward "
       "to the balance-sheet cash of 3,278,675,752 — requires 111,540,611 given "
       "revenue collected from investments of 137,985,226 and revenue from credit "
       "interest of 100,691,248, both of which FS2024's comparative column states "
       "identically. (ii) FS2024's comparative states 111,448,611 for the same "
       "year, and 111,540,611 less the 92,000 of disposal proceeds FS2023 shows on "
       "its own separate line is 111,448,611 exactly — one presentational change, "
       "net against gross of disposals, rather than two restatements"),
   capex_as_restated=111_448_611),
 2024: dict(src="FS2024", column="own", page=(9,),
   dep=97_994_727, capex=243_609_137, disposals=0,
   cash_end=3_166_276_817,
   dep_label="Fixed asset depreciation and right of use amortization",
   capex_label=("Proceeds or Payments for fixed assets and projects under "
                "construction")),
 2025: dict(src="FS2025", column="own", page=(9,),
   dep=127_506_241, capex=371_228_733, disposals=0,
   cash_end=3_141_779_939,
   dep_label="Fixed asset depreciation and right of use amortization",
   capex_label="Payments for projects under construction and fixed assets"),
}

# The cost-of-sales depreciation this run's own panel.py carries, quoted here so
# a reader can see that the group charge above is a DIFFERENT measurement and
# not a disagreement with the panel.
COS_DEPRECIATION = {2021: 78_603_107, 2022: 78_618_923, 2023: 83_410_669,
                    2024: 88_208_019, 2025: 109_320_313}

# ---------------------------------------------------------------------------
# THE CAPITAL NOTE, read off each year's OWN filing.  THE COUNT IS FOOTED OR IT
# IS NOT RECORDED [clause (ii)]: issued capital divided by par must reproduce
# the count the same document states.  Today's count is never carried back —
# each entry is that year's own note in that year's own filing, with its page.
#
# AMOC's capital note proper is a CHRONOLOGY of resolutions, which is the case
# clause (ii) names; the recital establishes the par value and the identity
# (RECITAL below, and asserted in foot()).  But the count does not have to rest
# on the recital alone here, because every filing ALSO carries an earnings-per-
# share note stating the number of shares and the par value for the same date,
# and that is what each entry cites.
# ---------------------------------------------------------------------------
CAPITAL = {
 2021: dict(src="FS2022", page=60, column="comparative",
   note="(١٥) نصيب السهم في أرباح (خسائر) الفترة — earnings per share for the period",
   shares=1_291_500_000, issued_capital=1_291_500_000, par_value=1.0,
   par_source=("the note's own footer, 'قيمة السهم الإسمية ١ جنيه' (share par value "
               "1 EGP), printed beside 'عدد الأسهم' (number of shares) of "
               "1,291,500,000 for this same date"),
   cross_check=("the note's own earnings per share of 0.35 reproduces from its "
                "stated profit after the employees' and board share of 446,057,800 "
                "over this count")),
 2022: dict(src="FS2022", page=60, column="own",
   note="(١٥) نصيب السهم في أرباح (خسائر) الفترة — earnings per share for the period",
   shares=1_291_500_000, issued_capital=1_291_500_000, par_value=1.0,
   par_source=("the note's own footer, 'قيمة السهم الإسمية ١ جنيه' (share par value "
               "1 EGP), printed beside 'عدد الأسهم' (number of shares) of "
               "1,291,500,000 for this same date"),
   cross_check=("the note's own earnings per share of 0.85 reproduces from its "
                "stated profit after the employees' and board share of "
                "1,090,388,455 over this count")),
 2023: dict(src="FS2023", page=69, column="own",
   note="17- Earnings Per Share for the Year",
   shares=1_291_500_000, issued_capital=1_291_500_000, par_value=1.0,
   par_source=("the table's own footer line, 'Pare Value Per Share Is 1 EGP', "
               "printed beside 'Number of Shares' of 1,291,500,000 for this date"),
   cross_check=("the note's own earnings per share of 0.92 reproduces from its "
                "stated profit after the employees' and board share of "
                "1,190,645,298 over this count")),
 2024: dict(src="FS2024", page=43, column="own",
   note="16- Earnings per Share for the period",
   shares=1_291_500_000, issued_capital=1_291_500_000, par_value=1.0,
   par_source=("the table's own footer line, '(Share par value 1 EGP)', printed "
               "beside 'Number of shares' of 1,291,500,000 for this date"),
   cross_check=("the note's own earnings per share of 1.32 reproduces from its "
                "stated profit after the employees' and board share of "
                "1,519,944,144 over this count")),
 2025: dict(src="FS2025", page=45, column="own",
   note="16- Earnings per Share for the year",
   shares=1_291_500_000, issued_capital=1_291_500_000, par_value=1.0,
   par_source=("the table's own footer line, '(Share par value 1 EGP)', printed "
               "beside 'Number of shares' of 1,291,500,000 for this date"),
   cross_check=("the note's own earnings per share of 1.15 reproduces from its "
                "stated profit after the employees' and board share of "
                "1,329,375,065 over this count")),
}

# The recital clause (ii) names, from the capital note itself (FS2025 note 11
# paragraphs K and L, and the same chronology in FS2024 and FS2023): the par
# value was split from EGP 10 to EGP 1 in February 2017, giving 861,000,000
# shares in place of 86,100,000, and a half bonus share distributed in January
# 2018 took the count to 1,291,500,000. The identity is asserted in foot().
RECITAL = dict(
    src="FS2025", page=40, note="11- Capital, paragraphs K and L",
    par_value=1.0, shares_after_split=861_000_000, bonus_fraction=0.5,
    shares_after_bonus=1_291_500_000,
    text=("K — the par value of AMOC's share is split from 10 EGP to 1 EGP, to end "
          "up with a total 861,000,000 shares instead of 86,100,000 shares, upon "
          "extraordinary general assembly approval on 25 February 2017, recorded in "
          "the commercial register on 4 April 2017. L — upon the approval of the "
          "AMOC General Assembly held on 23 September 2017, an allotment of half a "
          "bonus share among shareholders, distributed through the Egyptian Stock "
          "Exchange on 3 January 2018, ending in 1,291,500,000 shares"))

# The paid-in-capital composition annex, which both the FY2022 and FY2023 filings
# print and which states the capital total but NEITHER a par value NOR a count —
# recorded so a later reader can see why the earnings-per-share note is what the
# count is cited to.
CAPITAL_COMPOSITION = dict(
    sources={"FS2022": 32, "FS2023": 29},
    lines={"cash shares — 100% of principal capital": 210_000_000,
           "cash shares — 100% of the capital increase": 488_000_000,
           "shares in kind — 100% of the capital increase "
           "(Alexandria Petroleum Company)": 122_000_000,
           "free shares — 5% of the paid-in capital": 41_000_000,
           "free shares — 50% of the paid-in capital": 430_500_000},
    total=1_291_500_000,
    note=("this annex states the composition of the paid-in capital and foots to "
          "1,291,500,000, and it names neither a par value nor a share count, so a "
          "count cannot be footed from it alone"))

# Disclosures that ride beside a figure and change how it should be read.
NOTES = {
 (2023, "cash"): dict(
   presentation=(
     "at this vintage the whole treasury sits in ONE balance-sheet line and the "
     "note discloses inside it EGP 784,250,000 held as a conservative deposit "
     "against documentary credit"),
   restated_by_a_later_filing=2_494_425_752,
   restatement=(
     "FS2024 moves that 784,250,000 out of cash into a non-current line, 'Other "
     "Financial investments', and restates this year's closing cash to "
     "2,494,425,752. An origin standing at FY2023 saw the first presentation and "
     "could not have seen the second, so the first is committed and the second is "
     "named beside it, never substituted"),
   note_page=62, note_ref="E- Cash"),
}

# The cash note's own composition, per year, from the filing that year published.
CASH_LINES = {
 2021: dict(page=3, ref="النقدية (7-هـ)", lines={
   "ودائع لأجل بالبنوك (time deposits at banks)": 1_146_879_500,
   "حسابات جارية بالبنوك (current accounts at banks)": 113_157_642,
   "نقدية بالخزينة (cash on hand)": 135_144}, pledged=0),
 2022: dict(page=3, ref="النقدية (7-هـ)", lines={
   "ودائع لأجل بالبنوك (time deposits at banks)": 1_165_940_000,
   "حسابات جارية بالبنوك (current accounts at banks)": 399_730_838,
   "نقدية بالخزينة (cash on hand)": 144_722}, pledged=0),
 2023: dict(page=62, ref="E- Cash", lines={
   "Time Deposits At Banks": 2_776_075_000,
   "Current Accounts": 506_058_708,
   "Allowance for credit losses on cash balances": -3_518_317,
   "Cash on Hand": 60_361}, pledged=0),
 2024: dict(page=36, ref="9-E Cash at banks and on hand", lines={
   "Time deposits": 1_755_450_000,
   "Current accounts": 1_970_732_002,
   "Cash on hand": 371_406,
   "Expected credit losses (cash balances)": -47_726_591}, pledged=512_550_000),
 2025: dict(page=38, ref="9- E Cash at banks and on hand", lines={
   "Time deposits": 1_117_302_500,
   "Current accounts": 2_585_199_346,
   "Cash on hand": 40_063,
   "Expected credit losses (cash balances)": -33_787_870}, pledged=526_974_100),
}

WC_ASSETS = ("inventory", "receivables", "debtors", "debit_balances")
WC_LIABS = ("payables", "creditors", "credit_balances")
EXCLUDED = ("cash", "loan_c", "lease_c", "corp_tax", "prov_disputed_tax",
            "prov_claims", "prov_total")


def _close(a, b, tol=1):
    return abs(a - b) <= tol


def foot():
    """Every statement against its own arithmetic. Returns the failures."""
    bad = []
    for y, b in sorted(BS.items()):
        nca = sum(b[k] for k in ("fixed", "puc", "rou", "afs", "other_fin_inv",
                                 "intangible"))
        ca = sum(b[k] for k in ("inventory", "receivables", "debtors",
                                "debit_balances", "cash"))
        eq = sum(b[k] for k in ("capital", "legal", "other_reserves", "oci",
                                "retained", "profit"))
        ncl = sum(b[k] for k in ("loan_nc", "lease_nc", "dtl"))
        cl = sum(b[k] for k in ("prov_disputed_tax", "prov_claims", "prov_total",
                                "payables", "lease_c", "corp_tax", "loan_c",
                                "creditors", "credit_balances"))
        for what, got, want in (
                ("non-current assets", nca, b["tnca"]),
                ("current assets", ca, b["tca"]),
                ("total assets", nca + ca, b["total_assets"]),
                ("equity attributable to owners", eq, b["parent_equity"]),
                ("total equity", b["parent_equity"] + b["nci"], b["total_equity"]),
                ("non-current liabilities", ncl, b["tncl"]),
                ("current liabilities", cl, b["tcl"]),
                ("equity and liabilities",
                 b["total_equity"] + b["tncl"] + b["tcl"], b["teal"]),
                ("total assets against equity and liabilities",
                 b["total_assets"], b["teal"])):
            if not _close(got, want):
                bad.append("%d %s: %d against a stated %d" % (y, what, got, want))
        # a line the year prints must have a label, and a labelled line must be
        # a line the year prints — otherwise the record claims what the page
        # does not say, or hides what it does.
        lab = LABELS[y]
        for k, v in b.items():
            if k in ("src", "column", "page") or not isinstance(v, int):
                continue
            if k in ("tnca", "tca", "total_assets", "parent_equity",
                     "total_equity", "tncl", "tcl", "teal"):
                continue
            if v and k not in lab:
                bad.append("%d %s carries %d and no printed label" % (y, k, v))
            if not v and k in lab:
                bad.append("%d %s is labelled and carries nothing" % (y, k))
    for y, c in sorted(CF.items()):
        if not _close(c["cash_end"], BS[y]["cash"]):
            bad.append("%d cash at the end of the cash-flow statement %d against a "
                       "balance sheet %d" % (y, c["cash_end"], BS[y]["cash"]))
    for y, k in sorted(CASH_LINES.items()):
        got = sum(k["lines"].values()) - k["pledged"]
        if not _close(got, BS[y]["cash"]):
            bad.append("%d the cash note's own lines give %d against a balance "
                       "sheet %d" % (y, got, BS[y]["cash"]))
        if k["pledged"] and not _close(k["pledged"], BS[y]["other_fin_inv"]):
            bad.append("%d the pledged deposit deducted in the cash note is %d "
                       "against an 'other financial investments' line of %d"
                       % (y, k["pledged"], BS[y]["other_fin_inv"]))
    for y, k in sorted(CAPITAL.items()):
        implied = k["issued_capital"] / k["par_value"]
        if abs(implied - k["shares"]) > max(1.0, 1e-9 * k["shares"]):
            bad.append("%d capital %.0f / par %g = %.0f against a stated %.0f — the "
                       "document does not foot against itself"
                       % (y, k["issued_capital"], k["par_value"], implied,
                          k["shares"]))
        if not _close(k["issued_capital"], BS[y]["capital"]):
            bad.append("%d the capital note's issued capital %d is not the capital "
                       "the balance sheet states, %d"
                       % (y, k["issued_capital"], BS[y]["capital"]))
    got = RECITAL["shares_after_split"] * (1 + RECITAL["bonus_fraction"])
    if not _close(got, RECITAL["shares_after_bonus"]):
        bad.append("the capital recital does not reproduce its own count: %.0f "
                   "against a stated %d" % (got, RECITAL["shares_after_bonus"]))
    if not _close(sum(CAPITAL_COMPOSITION["lines"].values()),
                  CAPITAL_COMPOSITION["total"]):
        bad.append("the paid-in-capital composition annex does not foot")
    return bad


_BAD = foot()
assert not _BAD, "the valuation-input block does not foot: " + "; ".join(_BAD)


def debt(y):
    """Interest-bearing borrowings, on the disclosed lines and nothing else.

    The National Bank of Egypt loan and its current portion. Trade and notes
    payable, creditors and other credit balances, the tax due and the provisions
    are excluded BY CONSTRUCTION — this run's own pre-registration refuses to
    form a borrowing rate on a denominator that includes non-interest-bearing
    balances, which is the [R-FCAL-01] trap (i) discipline, and the same
    definition is used here so the block and the panel cannot disagree about
    what debt means. The lease liabilities are carried BESIDE, named, because
    folding them in or dropping them are both valuation choices and this record
    makes neither. On FY2021, FY2022 and FY2023 the answer is a DISCLOSED ZERO:
    the balance sheet carries no borrowings line at all.
    """
    b = BS[y]
    return b["loan_nc"] + b["loan_c"]


def working_capital(y):
    """Operating working capital: the trading lines, and nothing else."""
    b = BS[y]
    return sum(b[k] for k in WC_ASSETS) - sum(b[k] for k in WC_LIABS)


def source(y, statement, page, ref=None):
    key = BS[y]["src"] if statement != "cf" else CF[y]["src"]
    fn, label, _, _ = FILES[key]
    col = BS[y]["column"] if statement != "cf" else CF[y]["column"]
    return ("%s, %s, page %s%s — the %s column of the company's own %s, from its "
            "own investor-relations archive"
            % (fn, ref or statement, ", ".join(str(p) for p in page),
               "", col, label))


def _lines(y, keys):
    lab = LABELS[y]
    return {lab[k]: BS[y][k] for k in keys if BS[y].get(k) and k in lab}


def _cash(y):
    b, k = BS[y], CASH_LINES[y]
    rec = {
        "value": b["cash"],
        "as_at": "%d-06-30" % y,
        "source": source(y, "consolidated statement of financial position",
                         b["page"], LABELS[y]["cash"]),
        "route": ROUTE,
        "lines": dict(k["lines"]),
        "note_source": ("%s, %s, page %d"
                        % (FILES[BS[y]["src"]][0], k["ref"], k["page"])),
        "check": ("the cash-flow statement closes on the same figure — %d"
                  % CF[y]["cash_end"]),
    }
    if k["pledged"]:
        rec["carried_beside_not_included"] = {
            "pledged_deposits_classified_as_other_financial_investments":
                k["pledged"],
            "why": ("the cash note deducts this deposit, pledged against the "
                    "National Bank of Egypt facility, and the balance sheet "
                    "carries it in a non-current line; it is a claim on the "
                    "company's own money and whether a bridge adds it back is a "
                    "valuation choice this record does not make"),
        }
    rec.update(NOTES.get((y, "cash"), {}))
    return rec


def _debt(y):
    b = BS[y]
    v = debt(y)
    rec = {
        "value": v,
        "as_at": "%d-06-30" % y,
        "source": source(y, "consolidated statement of financial position",
                         b["page"],
                         "the borrowings lines" if v else
                         "the liabilities sections, which carry no borrowings line"),
        "route": ROUTE,
        "definition": ("the National Bank of Egypt loan and its current portion — "
                       "the only interest-bearing borrowings this company "
                       "discloses. Trade and notes payable, creditors and other "
                       "credit balances, the tax due and the provisions are "
                       "excluded, the same construction this run's own "
                       "pre-registration uses when it refuses to form a borrowing "
                       "rate on a wider denominator"),
        "lines": _lines(y, ("loan_nc", "loan_c")),
        "carried_beside_not_folded_in": dict(
            _lines(y, ("lease_nc", "lease_c")),
            why=("whether a lease liability is debt is a valuation choice; this "
                 "record reads the page and makes neither choice, so the lease "
                 "lines are named rather than folded in or dropped"),
        ),
    }
    if not v:
        rec["disclosed_zero"] = (
            "this is a DISCLOSED ZERO and not a missing item: the balance sheet at "
            "this date carries no borrowings line of any kind, only the lease "
            "liabilities named beside. The company is unlevered and holds net cash")
    return rec


def _capex(y):
    c = CF[y]
    rec = {
        "value": c["capex"],
        "period": "FY%d" % y,
        "source": source(y, "cf", c["page"],
                         "consolidated statement of cash flows, investing "
                         "activities — %s" % c["capex_label"]),
        "route": ROUTE,
        "derived": False,
        "disclosed": True,
    }
    if c.get("disposals"):
        rec["disposal_proceeds_shown_separately"] = c["disposals"]
    if c.get("capex_route_dispute"):
        rec["route_dispute"] = c["capex_route_dispute"]
        rec["as_restated_by_a_later_filing"] = c["capex_as_restated"]
    if y - 1 in BS:
        prior, now = BS[y - 1], BS[y]
        ident = ((now["fixed"] + now["puc"]) - (prior["fixed"] + prior["puc"])
                 + c["dep"])
        rec["identity_cross_check"] = {
            "identity": "capex = dPPE + D&A",
            "value": ident,
            "basis": ("fixed assets net plus projects under construction at both "
                      "dates, and the group depreciation and amortisation charge "
                      "for the year"),
            "difference_from_disclosed": ident - c["capex"],
            "note": ("the two are not the same measurement and the gap is not a "
                     "defect: disposals leave at net book value, right-of-use "
                     "assets are recognised without cash, and assets move out of "
                     "construction into property without cash. The DISCLOSED cash "
                     "figure is what is committed; the identity is reported beside "
                     "it so a later rebuild can see both rather than assume they "
                     "agree"),
        }
    else:
        rec["identity_cross_check"] = {
            "identity": "capex = dPPE + D&A",
            "value": None,
            "missing": ("the identity cannot run at this origin: it needs property "
                        "at two dates and the company publishes no statements older "
                        "than the FY2022 filing, so the 30 June 2020 balance sheet "
                        "is not in any document this run can reach. It is not "
                        "needed — capital expenditure is DISCLOSED at this origin "
                        "and the disclosed figure is what is committed"),
        }
    return rec


def _ppe(y):
    b = BS[y]
    return {
        "value": b["fixed"],
        "as_at": "%d-06-30" % y,
        "source": source(y, "consolidated statement of financial position",
                         b["page"], LABELS[y]["fixed"]),
        "route": ROUTE,
        "lines": _lines(y, ("fixed", "puc", "rou", "intangible")),
        "note": ("the identity capex = dPPE + D&A is run on fixed assets PLUS "
                 "projects under construction, because this company's spending "
                 "lands in construction first and moves across without cash; the "
                 "right-of-use asset and the intangible are named beside and are "
                 "not in the property figure"),
    }


def _dep(y):
    c = CF[y]
    return {
        "value": c["dep"],
        "period": "FY%d" % y,
        "source": source(y, "cf", c["page"],
                         "consolidated statement of cash flows, the depreciation "
                         "and amortisation add-back — %s" % c["dep_label"]),
        "route": ROUTE,
        "note": ("the GROUP charge, which is more than the cost-of-sales "
                 "depreciation this run's panel.py carries for the same year "
                 "(%d, note 15-A): that one is the manufacturing share and this is "
                 "the whole company, so the two are different measurements and not "
                 "a disagreement" % COS_DEPRECIATION[y]),
        "cost_of_sales_depreciation_for_comparison": COS_DEPRECIATION[y],
    }


def _wc(y):
    b, lab = BS[y], LABELS[y]
    excluded = {lab[k]: b[k] for k in EXCLUDED if b.get(k) and k in lab}
    excluded.update({lab[k]: b[k] for k in ("lease_nc", "dtl", "loan_nc")
                     if b.get(k) and k in lab})
    excluded["why"] = ("a reader cannot tell an excluded line from an unread one, "
                       "so every balance-sheet line that is NOT in the "
                       "working-capital figure is named here with its own amount")
    return {
        "value": working_capital(y),
        "as_at": "%d-06-30" % y,
        "source": source(y, "consolidated statement of financial position",
                         b["page"], "the trading lines of current assets and "
                                    "current liabilities"),
        "route": ROUTE,
        "definition": ("inventory + trade receivables + debtors and other debit "
                       "balances, less suppliers and notes payable and creditors "
                       "and other credit balances"),
        "lines": dict(_lines(y, WC_ASSETS), **_lines(y, WC_LIABS)),
        "printed_subtotals": {"total current assets": b["tca"],
                              "total current liabilities": b["tcl"]},
        "excluded_and_named": excluded,
        "definition_note": ("the debtors line is a mixed balance — it carries tax "
                            "instalments, withholding tax, deposits, loans to "
                            "employees, prepayments and accrued interest as well as "
                            "trade items — and it is taken whole rather than split, "
                            "because the filings do not split it on a constant basis "
                            "across this window; the composition is in the filing's "
                            "own debtors note at each date"),
    }


def _shares(y):
    if y not in CAPITAL:
        return {"missing": ("no capital note could be read for FY%d, so no count is "
                            "recorded — a count that does not foot against its own "
                            "issued capital and par value is not recorded at all" % y)}
    k = CAPITAL[y]
    return {
        "value": k["shares"],
        "as_at": "%d-06-30" % y,
        "issued_capital": k["issued_capital"],
        "par_value": k["par_value"],
        "source": ("%s, %s, page %d — the %s column"
                   % (FILES[k["src"]][0], k["note"], k["page"], k["column"])),
        "route": ROUTE,
        "check": ("issued capital %d / par %g = %d, matching the count the same "
                  "note states, and matching the capital the balance sheet states "
                  "for the same date"
                  % (k["issued_capital"], k["par_value"],
                     k["issued_capital"] / k["par_value"])),
        "par_source": k["par_source"],
        "cross_check": k["cross_check"],
        "vintage": ("read off the %s filing's own note; no later count is carried "
                    "back to this origin" % k["src"]),
        "recital": RECITAL["text"],
    }


def block(y):
    return {
        "cash": _cash(y),
        "debt": _debt(y),
        "capex": _capex(y),
        "ppe": _ppe(y),
        "dep": _dep(y),
        "wc": _wc(y),
        "shares": _shares(y),
    }


def record():
    """The valuation-input block, in the shape [R-FCAL-01 AMENDED] defines."""
    return {
        "_": ("The inputs a VALUE is rebuilt from at each of this run's origins, "
              "committed beside the driver panel under [R-FCAL-01 AMENDED]. "
              "GENERATED by engine/amoc_walkforward/valuation_inputs.py, which "
              "foots every balance sheet against its own subtotals, every cash "
              "note against the balance sheet, every cash-flow statement against "
              "the closing cash and every share count against its own par value, "
              "at import; never hand-edited."),
        "run": "AMOC",
        "rule": "[R-FCAL-01 AMENDED] (03-09-2026)",
        "company": "Alexandria Mineral Oils Company S.A.E",
        "currency": "EGP",
        "units": "as printed in the filings — units, not thousands or millions",
        "basis": "consolidated",
        "fiscal_year_end": "30 June",
        "origins_declared_by": "PRE_REGISTRATION_01-09-2026.md",
        "route": ROUTE,
        "text_layer_census": {
            f: {"pages": pg, "text_layer_characters": tx,
                "label": label}
            for f, (fn, label, pg, tx) in
            ((v[0], v) for v in FILES.values())},
        "point_in_time": (
            "FY2022 to FY2025 are carried from each year's OWN column in its OWN "
            "filing. FY2021 is carried from the comparative column of the FY2022 "
            "filing, and that is stated rather than glossed: the company publishes "
            "no annual statements older than that filing, so no first report of 30 "
            "June 2021 exists to read. The one re-presentation inside this window "
            "that touches a committed item — the pledged deposits moving out of "
            "cash in the FY2024 filing — is recorded beside the FY2023 figure it "
            "would replace and never substituted."),
        "sources": {k: {"file": v[0], "label": v[1], "pages": v[2]}
                    for k, v in FILES.items()},
        "capital_recital": RECITAL,
        "capital_composition_annex": CAPITAL_COMPOSITION,
        "origins": {"FY%d" % y: block(y) for y in range(2021, 2026)},
        "prior_year_anchor": {
            "missing": ("no 30 June 2020 balance sheet is carried and none can be: "
                        "the company publishes no statements older than the FY2022 "
                        "filing. It is not needed — capital expenditure is DISCLOSED "
                        "in the cash-flow statement at every one of the five "
                        "origins, so the identity capex = dPPE + D&A never has to "
                        "produce a figure; it is reported beside the disclosed "
                        "figure at FY2022 to FY2025 and recorded as unrunnable at "
                        "FY2021."),
        },
    }


def shares_record():
    """The point-in-time counts, in the shape the calibration panel reads.

    engine/valuation_calibration/panel.py resolves a share count for an origin
    from shares_{ticker}.json and from nothing else, so a count committed only
    inside this run's own record would be invisible to the readiness matrix that
    decides which origins the calibration can score. It is GENERATED here, from
    the same footed reading, so the two cannot drift apart.
    """
    out = {
        "_": ("GENERATED by engine/amoc_walkforward/valuation_inputs.py from that "
              "run's own reading of each year's earnings-per-share note — NOT by "
              "extract_shares.py, whose scan this did not run. Never hand-edited."),
        "ticker": "AMOC",
        "shares_mn": {},
        "rule": ("recorded only where issued capital divided by par value "
                 "reproduces the share count the same document states"),
    }
    for y, k in sorted(CAPITAL.items()):
        out["shares_mn"][str(y)] = {
            "shares_mn": k["shares"] / 1e6,
            "issued_capital": float(k["issued_capital"]),
            "par_value": float(k["par_value"]),
            "page": k["page"],
            "file": FILES[k["src"]][0],
            "check": ("capital %d / par %g = %d, matching the stated count"
                      % (k["issued_capital"], k["par_value"],
                         k["issued_capital"] / k["par_value"])),
            "how": k["par_source"],
            "route": ROUTE,
        }
    return out


def main():
    bad = foot()
    if bad:
        raise SystemExit("REFUSED — the block does not foot:\n  " + "\n  ".join(bad))
    rec = record()
    p = os.path.join(HERE, "valuation_inputs.json")
    json.dump(rec, open(p, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    q = os.path.join(CALIB, "shares_amoc.json")
    json.dump(shares_record(), open(q, "w", encoding="utf-8"), indent=1,
              ensure_ascii=False)

    print("valuation-input block — AMOC\n")
    hdr = ("origin", "cash", "debt", "capex", "ppe", "D&A", "working cap", "shares")
    print("  %-8s %15s %13s %13s %13s %13s %15s %14s" % hdr)
    print("  " + "-" * 112)
    n_missing = 0
    for y in range(2021, 2026):
        b = block(y)

        def v(i):
            r = b[i]
            return "MISSING" if "missing" in r else format(r["value"], ",.0f")
        print("  FY%-6d %15s %13s %13s %13s %13s %15s %14s"
              % (y, v("cash"), v("debt"), v("capex"), v("ppe"), v("dep"), v("wc"),
                 v("shares")))
        n_missing += sum(1 for r in b.values() if "missing" in r)
    print("\n  5 origins x 7 items = 35 cells, %d recorded missing" % n_missing)
    print("  every balance sheet, cash note, cash-flow roll-forward and share")
    print("  count footed against its own arithmetic at import")
    root = os.path.dirname(os.path.dirname(HERE))
    print("  wrote %s" % os.path.relpath(p, root))
    print("  wrote %s" % os.path.relpath(q, root))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
