"""The VALUATION-INPUT BLOCK for this run — the figures a VALUE is rebuilt from.

[R-FCAL-01 AMENDED, 03-09-2026].  A driver panel is not a record a value can be
rebuilt from.  This run's `panel.py` committed the income statement, the revenue
and cost notes, the interest-bearing borrowings and the physical volumes — every
figure the walk-forward's own scoring needed — and left no trace of the balance
sheet beside them.  Measured by `engine/valuation_calibration/bridge_inputs.py`,
ARCC carried DEBT and DEPRECIATION and nothing else: no cash, no property, no
working capital, no share count, and therefore no route to capital expenditure
even by the identity, because the identity needs property at two dates.

WHY THAT MATTERED MORE THAN THE COUNT OF WHAT WAS MISSING.  Debt without cash is
the ASYMMETRIC half of a bridge: the debt that is committed is deducted in full
while the cash that would be added back is absent, so a bridge built from what
this run committed is biased DOWNWARD by construction — the same direction as the
hypothesis the calibration is testing, which is the one direction an instrument
must not be biased in.  ARCC held EGP 3,459,391,229 of cash at 31 December 2025
against EGP 1,133,932,616 of borrowings.  On that origin the omitted item is not
a rounding error; it is most of the bridge.

WHAT IS HERE.  For every origin the run declares — FY2018 to FY2025, fiscal years
ending 31 December — cash and equivalents, interest-bearing debt, property plant
and equipment, depreciation and amortisation, the working-capital lines, capital
expenditure, and the share count with the par value it was footed against.  FY2017
is carried too, OUTSIDE the origin list and labelled as what it is: the prior-year
anchor the identity capex = dPPE + D&A needs at the first origin.  It is not an
origin of this run and is not recorded as one.

EVERY FIGURE IS A COPY, NOT NEW RESEARCH.  Each one sits on a balance sheet or a
cash-flow statement in a filing this run had already parsed cell by cell; carrying
them out is transcription.  Not carrying them out meant no valuation of this
company could ever be rebuilt at a past origin, permanently, for any year whose
filings are no longer to hand.

ROUTE, AND WHY ARITHMETIC DECIDES [clause (iii)].  ARCC files every statement as
an image: across the nine annual filings read here, not one page of 437 carried a
text layer worth reading, so every figure arrived by OCR at 300 dpi off the
rendered pixels and NOT ONE is believed because it looked clean.  Every balance
sheet foots — components to their subtotals, subtotals to total assets, assets to
equity and liabilities — and the footing runs at import as assertions rather than
living in a comment, which is this run's own house discipline from `panel.py`.

FIVE FIGURES WERE READ WRONGLY AND ARITHMETIC CAUGHT ALL FIVE.  Each looked
perfectly clean on the page and none would have been visible to a reader of the
extracted figure:

  FY2017 creditors and other credit balances   119 300 630 -> 119 240 630
  FY2018 trade receivables                     illegible   -> 92 994 532
  FY2019 total non-current assets              2 712 684 353 -> 2 712 084 353
  FY2023 depreciation of property and plant    215 976 939 -> 215 376 939
  FY2023 amortisation of right-of-use assets   6 891 239   -> 6 891 333

The first three were settled by the statement's own column, the last two by the
FY2024 filing's comparative column, whose every line foots to the stated subtotal
where the FY2023 page's own reading misses it by 599,906.

POINT IN TIME IS ABSOLUTE.  Every year is carried AS FIRST REPORTED, from its own
filing's own column.  One re-presentation falls inside this window and it is
recorded BESIDE the figure it would replace, never substituted: the FY2023 filing
nets EGP 36,385,385 of debtors against trade and notes payable in its FY2022
comparative, so an origin standing at FY2022 saw debtors of 235,320,162 and could
not have seen the 198,934,777 the next filing showed for the same date.

WHAT IS DELIBERATELY NOT DECIDED HERE.  This module records; it values nothing.
Where a figure could be defined two ways the record carries the disclosed lines
and names the convention rather than resolving it — interest-bearing debt is the
three borrowing lines this run's own `panel.py` forms its rate on, with the lease
liabilities carried BESIDE them rather than folded in or dropped, because whether
a lease liability is debt is a valuation choice and not a reading of the page.
"""
from __future__ import annotations

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
CALIB = os.path.join(os.path.dirname(HERE), "valuation_calibration")

# The origins this run declares (PRE_REGISTRATION_01-09-2026.md, section 'Origins
# and horizons'). FY2017 is NOT one of them and is carried separately below.
ORIGINS = ["FY%d" % y for y in range(2018, 2026)]

# Which filing carries which year's own column, and the page the figure sits on.
# The file names are the company's own, as published on its investor-relations
# archive and as this run's `panel.py` SOURCES already records them.
FILES = {
    2017: ("FY-2017-Consolidated-Financials-English.pdf", "ARCC_FY2017_Consolidated.pdf"),
    2018: ("ARCC_FY_2018_Consolidated_Financials-English.pdf", "ARCC_FY2018_Consolidated.pdf"),
    2019: ("FY_2019_Consolidated_Financials-English.pdf", "ARCC_FY2019_Consolidated.pdf"),
    2020: ("FY-2020-consolidated-financials-english.pdf", None),
    2021: ("FY_2021_Consolidated_Financials-English.pdf", None),
    2022: ("FY_2022_Consolidated_Financials-English.pdf", None),
    2023: ("4Q2023_ACC_Consolidated_Financials.pdf", None),
    2024: ("FY2024_Consolidated_Financials-English.pdf", None),
    2025: ("FY-2025-Consolidated-Financials-English.pdf", None),
}

ROUTE = ("OCR at 300 dpi off the rendered pixels — the filing carries no text "
         "layer on any page; every figure footed against the statement's own "
         "arithmetic before it was recorded")

# ---------------------------------------------------------------------------
# Consolidated statement of financial position, OWN column, at 31 December.
# Stated positive as printed. Every line below is asserted against the
# statement's own subtotals in `foot()`.
# ---------------------------------------------------------------------------
BS = {
 2017: dict(page=(5, 6),
   ppe=2_371_924_441, auc=249_232_824, intangibles=396_151_869, other_assets=83_653,
   rou=0, jv=2_023_874, tnca=3_019_416_661,
   inventories=257_544_521, trade_receivables=15_512_298, debtors=85_007_648,
   due_from_related=0, cash=133_557_621, tca=491_622_088, total_assets=3_511_038_749,
   capital=757_479_400, treasury=0, legal_reserve=209_713_200, retained=325_021_738,
   parent_equity=1_292_214_338, nci=22_017, total_equity=1_292_236_355,
   borrowings_nc=601_101_209, notes_payable_nc=7_000_000, dtl=337_657_419,
   other_liab_nc=92_968_685, lease_nc=0, tncl=1_038_727_313,
   trade_payables=455_229_498, credit_facilities=300_419_651, tax_payable=110_901,
   borrowings_cp=167_535_000, other_liab_cp=114_462_000, creditors=119_240_630,
   lease_c=0, due_to_related=7_384_177, provisions=15_693_224, dividends_payable=0,
   tcl=1_180_075_081, total_liabilities=2_218_802_394, teal=3_511_038_749),
 2018: dict(page=(5, 6),
   ppe=2_473_177_771, auc=106_904_072, intangibles=345_475_618, other_assets=47_801,
   rou=0, jv=2_264_213, tnca=2_927_869_475,
   inventories=287_985_828, trade_receivables=92_994_532, debtors=107_874_288,
   due_from_related=0, cash=184_590_855, tca=673_445_503, total_assets=3_601_314_978,
   capital=757_479_400, treasury=0, legal_reserve=231_456_593, retained=329_029_161,
   parent_equity=1_317_965_154, nci=2_149_810, total_equity=1_320_114_964,
   borrowings_nc=619_160_870, notes_payable_nc=0, dtl=344_798_687,
   other_liab_nc=12_308_000, lease_nc=0, tncl=976_267_557,
   trade_payables=592_601_887, credit_facilities=273_674_586, tax_payable=293_208,
   borrowings_cp=77_731_487, other_liab_cp=124_681_184, creditors=216_867_519,
   lease_c=0, due_to_related=8_460_876, provisions=10_621_710, dividends_payable=0,
   tcl=1_304_932_457, total_liabilities=2_281_200_014, teal=3_601_314_978),
 2019: dict(page=(5, 6),
   ppe=2_408_100_199, auc=3_777_941, intangibles=294_799_369, other_assets=11_951,
   rou=3_086_102, jv=2_308_791, tnca=2_712_084_353,
   inventories=162_831_419, trade_receivables=27_529_031, debtors=115_574_736,
   due_from_related=0, cash=101_331_254, tca=407_266_440, total_assets=3_119_350_793,
   capital=757_479_400, treasury=0, legal_reserve=254_820_827, retained=151_416_266,
   parent_equity=1_163_716_493, nci=30_980, total_equity=1_163_747_473,
   borrowings_nc=491_836_958, notes_payable_nc=0, dtl=338_826_864,
   other_liab_nc=0, lease_nc=1_538_321, tncl=832_202_143,
   trade_payables=704_046_978, credit_facilities=62_035_301, tax_payable=13_903_338,
   borrowings_cp=90_356_520, other_liab_cp=12_308_000, creditors=216_252_373,
   lease_c=981_360, due_to_related=10_743_810, provisions=12_773_497, dividends_payable=0,
   tcl=1_123_401_177, total_liabilities=1_955_603_320, teal=3_119_350_793),
 2020: dict(page=(5, 6),
   ppe=2_202_003_667, auc=7_800_244, intangibles=254_049_586, other_assets=0,
   rou=1_047_456, jv=2_454_486, tnca=2_467_355_439,
   inventories=176_470_491, trade_receivables=15_938_789, debtors=136_384_081,
   due_from_related=0, cash=67_032_927, tca=395_826_288, total_assets=2_863_181_727,
   capital=757_479_400, treasury=0, legal_reserve=257_830_772, retained=18_551_721,
   parent_equity=1_033_861_893, nci=31_108, total_equity=1_033_893_001,
   borrowings_nc=387_454_349, notes_payable_nc=11_021_813, dtl=323_765_007,
   other_liab_nc=0, lease_nc=0, tncl=722_241_169,
   trade_payables=459_805_964, credit_facilities=340_110_399, tax_payable=438_220,
   borrowings_cp=99_165_216, other_liab_cp=769_250, creditors=180_575_890,
   lease_c=915_298, due_to_related=6_767_033, provisions=18_500_287, dividends_payable=0,
   tcl=1_107_047_557, total_liabilities=1_829_288_726, teal=2_863_181_727),
 2021: dict(page=(5, 6),
   ppe=2_019_945_189, auc=3_261_312, intangibles=219_424_613, other_assets=0,
   rou=17_631_358, jv=2_523_361, tnca=2_262_785_833,
   inventories=369_730_638, trade_receivables=58_876_151, debtors=153_272_743,
   due_from_related=0, cash=128_250_456, tca=710_129_988, total_assets=2_972_915_821,
   capital=757_479_400, treasury=0, legal_reserve=257_830_772, retained=45_625_489,
   parent_equity=1_060_935_661, nci=38_681, total_equity=1_060_974_342,
   borrowings_nc=272_760_907, notes_payable_nc=7_610_691, dtl=301_472_827,
   other_liab_nc=0, lease_nc=6_979_776, tncl=588_824_201,
   trade_payables=693_703_628, credit_facilities=240_386_963, tax_payable=43_280_867,
   borrowings_cp=114_334_781, other_liab_cp=0, creditors=184_254_394,
   lease_c=9_566_342, due_to_related=11_792_907, provisions=25_797_396, dividends_payable=0,
   tcl=1_323_117_278, total_liabilities=1_911_941_479, teal=2_972_915_821),
 2022: dict(page=(5,),
   ppe=1_839_104_558, auc=3_952_133, intangibles=191_268_364, other_assets=0,
   rou=12_992_066, jv=2_569_276, tnca=2_049_886_397,
   inventories=624_486_267, trade_receivables=79_554_875, debtors=235_320_162,
   due_from_related=76_140, cash=818_442_022, tca=1_757_879_466,
   total_assets=3_807_765_863,
   capital=757_479_400, treasury=0, legal_reserve=260_543_120, retained=145_003_980,
   parent_equity=1_163_026_500, nci=38_121, total_equity=1_163_064_621,
   borrowings_nc=177_476_090, notes_payable_nc=4_544_514, dtl=266_201_710,
   other_liab_nc=0, lease_nc=6_724_129, tncl=454_946_443,
   trade_payables=847_567_285, credit_facilities=360_644_205, tax_payable=198_386_556,
   borrowings_cp=163_534_780, other_liab_cp=0, creditors=299_002_000,
   lease_c=6_411_505, due_to_related=369_246, provisions=63_871_019,
   dividends_payable=249_968_203,
   tcl=2_189_754_799, total_liabilities=2_644_701_242, teal=3_807_765_863),
 2023: dict(page=(5,),
   ppe=1_683_607_099, auc=2_426_563, intangibles=163_112_115, other_assets=0,
   rou=12_901_506, jv=0, tnca=1_862_047_283,
   inventories=986_106_029, trade_receivables=228_615_932, debtors=249_566_135,
   due_from_related=95_368, cash=561_096_680, tca=2_025_480_144,
   total_assets=3_887_527_427,
   capital=757_479_400, treasury=0, legal_reserve=294_829_534, retained=701_912_725,
   parent_equity=1_754_221_659, nci=48_010, total_equity=1_754_269_669,
   borrowings_nc=0, notes_payable_nc=1_788_996, dtl=282_218_616,
   other_liab_nc=0, lease_nc=1_739_258, tncl=285_746_870,
   trade_payables=1_067_664_610, credit_facilities=90_074_273, tax_payable=216_715_896,
   borrowings_cp=0, other_liab_cp=0, creditors=309_899_324,
   lease_c=9_481_649, due_to_related=0, provisions=54_445_334,
   dividends_payable=99_229_802,
   tcl=1_847_510_888, total_liabilities=2_133_257_758, teal=3_887_527_427),
 2024: dict(page=(5,),
   ppe=1_669_630_565, auc=706_855_633, intangibles=134_955_866, other_assets=0,
   rou=4_436_332, jv=0, tnca=2_515_878_396,
   inventories=852_490_043, trade_receivables=160_048_158, debtors=632_979_976,
   due_from_related=156_657, cash=1_687_062_873, tca=3_332_737_707,
   total_assets=5_848_616_103,
   capital=757_479_400, treasury=0, legal_reserve=363_627_770, retained=1_182_365_129,
   parent_equity=2_303_472_299, nci=53_721, total_equity=2_303_526_020,
   borrowings_nc=120_392_380, notes_payable_nc=301_142_055, dtl=241_146_994,
   other_liab_nc=0, lease_nc=1_642_532, tncl=664_323_961,
   trade_payables=839_311_693, credit_facilities=615_044_229, tax_payable=374_014_396,
   borrowings_cp=25_481_075, other_liab_cp=0, creditors=345_087_344,
   lease_c=3_625_821, due_to_related=0, provisions=77_899_139,
   dividends_payable=600_302_425,
   tcl=2_880_766_122, total_liabilities=3_545_090_083, teal=5_848_616_103),
 2025: dict(page=(5,),
   ppe=2_522_323_523, auc=391_543_753, intangibles=106_799_617, other_assets=0,
   rou=822_030, jv=0, tnca=3_021_488_923,
   inventories=1_053_646_218, trade_receivables=244_416_417, debtors=1_004_779_062,
   due_from_related=0, cash=3_459_391_229, tca=5_762_232_926,
   total_assets=8_783_721_849,
   capital=757_479_400, treasury=-143_327_985, legal_reserve=379_505_774,
   retained=3_648_917_046,
   parent_equity=4_642_574_235, nci=158_005, total_equity=4_642_732_240,
   borrowings_nc=888_522_538, notes_payable_nc=0, dtl=255_316_160,
   other_liab_nc=103_020_835, lease_nc=0, tncl=1_246_859_533,
   trade_payables=720_176_243, credit_facilities=99_916_937, tax_payable=1_102_259_109,
   borrowings_cp=145_493_141, other_liab_cp=0, creditors=713_424_488,
   lease_c=1_176_042, due_to_related=0, provisions=111_684_116, dividends_payable=0,
   tcl=2_894_130_076, total_liabilities=4_140_989_609, teal=8_783_721_849),
}

# ---------------------------------------------------------------------------
# Consolidated statement of cash flows, OWN column, for the year.
# Capital expenditure is DISCLOSED on every one of these statements — payments
# for property, plant and equipment and payments for assets under construction,
# each its own line — so it is committed as a figure and NOT derived. The
# identity is still reported beside it in `build()`, because two independent
# routes to one number is a check and the disagreement between them is the
# accrual/cash difference a reader should see rather than a defect.
# ---------------------------------------------------------------------------
CF = {
 2017: dict(page=(10, 11), dep_ppe=186_297_452, amort_intangibles=50_676_249,
            amort_other=59_752, amort_rou=0,
            capex_ppe=17_594_103, capex_auc=242_103_780, capex_other=143_404,
            cash_end=133_557_621),
 2018: dict(page=(10, 11), dep_ppe=199_833_161, amort_intangibles=50_676_251,
            amort_other=35_852, amort_rou=0,
            capex_ppe=27_405_852, capex_auc=96_669_881, capex_other=0,
            cash_end=184_590_855),
 2019: dict(page=(10, 11), dep_ppe=210_637_159, amort_intangibles=50_676_249,
            amort_other=35_850, amort_rou=4_312_948,
            capex_ppe=38_380_668, capex_auc=3_436_791, capex_other=0,
            cash_end=101_331_254),
 2020: dict(page=(10, 11), dep_ppe=210_297_525, amort_intangibles=40_749_783,
            amort_other=11_951, amort_rou=2_038_646,
            capex_ppe=4_250_127, capex_auc=1_236_682, capex_other=0,
            cash_end=67_032_927),
 2021: dict(page=(10, 11), dep_ppe=217_929_493, amort_intangibles=34_624_973,
            amort_other=0, amort_rou=5_902_848,
            capex_ppe=19_208_760, capex_auc=0, capex_other=0,
            cash_end=128_250_456,
            note="the statement discloses a non-cash transaction beside it — the "
                 "unpaid portion of the purchase cost of fixed assets, EGP 13 235 203 "
                 "— so cash capital expenditure understates the year's additions by "
                 "that amount"),
 2022: dict(page=(9,), dep_ppe=208_215_007, amort_intangibles=28_156_249,
            amort_other=0, amort_rou=5_568_129,
            capex_ppe=27_374_376, capex_auc=690_821, capex_other=0,
            cash_end=818_442_022),
 2023: dict(page=(9,), dep_ppe=215_376_939, amort_intangibles=28_156_249,
            amort_other=0, amort_rou=6_891_333,
            capex_ppe=56_808_221, capex_auc=1_735_742, capex_other=0,
            cash_end=561_096_680,
            note="the FY2023 page's own reading gave 215 976 939 and 6 891 239; "
                 "neither foots the adjustments subtotal the same page states and "
                 "the FY2024 filing's comparative column foots it exactly, so the "
                 "comparative is what is carried and the difference is an OCR "
                 "misread rather than a re-presentation"),
 2024: dict(page=(9,), dep_ppe=221_562_864, amort_intangibles=28_156_249,
            amort_other=0, amort_rou=7_082_414,
            capex_ppe=206_542_630, capex_auc=705_472_770, capex_other=0,
            cash_end=1_687_062_873),
 2025: dict(page=(9,), dep_ppe=259_089_682, amort_intangibles=28_156_249,
            amort_other=0, amort_rou=2_525_364,
            capex_ppe=329_893_202, capex_auc=466_577_558, capex_other=0,
            cash_end=3_459_391_229),
}

# ---------------------------------------------------------------------------
# The capital note, read off each year's OWN filing. THE COUNT IS FOOTED OR IT
# IS NOT RECORDED [clause (ii)]: issued capital divided by par must reproduce
# the count the same document states. Today's count is never carried back —
# each year's entry is that year's own note, with its own page.
# ---------------------------------------------------------------------------
CAPITAL = {}

# Disclosures that ride beside a figure and change how it should be read.
NOTES = {}


def _close(a, b, tol=1):
    return abs(a - b) <= tol


def foot():
    """Every balance sheet against its own subtotals. Returns the failures."""
    bad = []
    for y, b in sorted(BS.items()):
        nca = sum(b[k] for k in ("ppe", "auc", "intangibles", "other_assets", "rou", "jv"))
        ca = sum(b[k] for k in ("inventories", "trade_receivables", "debtors",
                                "due_from_related", "cash"))
        ncl = sum(b[k] for k in ("borrowings_nc", "notes_payable_nc", "dtl",
                                 "other_liab_nc", "lease_nc"))
        cl = sum(b[k] for k in ("trade_payables", "credit_facilities", "tax_payable",
                                "borrowings_cp", "other_liab_cp", "creditors", "lease_c",
                                "due_to_related", "provisions", "dividends_payable"))
        eq = b["capital"] + b["treasury"] + b["legal_reserve"] + b["retained"]
        for what, got, want in (
                ("non-current assets", nca, b["tnca"]),
                ("current assets", ca, b["tca"]),
                ("total assets", nca + ca, b["total_assets"]),
                ("non-current liabilities", ncl, b["tncl"]),
                ("current liabilities", cl, b["tcl"]),
                ("total liabilities", ncl + cl, b["total_liabilities"]),
                ("equity attributable to owners", eq, b["parent_equity"]),
                ("total equity", b["parent_equity"] + b["nci"], b["total_equity"]),
                ("equity and liabilities", b["total_equity"] + b["total_liabilities"],
                 b["teal"])):
            if not _close(got, want):
                bad.append("%d %s: %d against a stated %d" % (y, what, got, want))
    for y, c in sorted(CF.items()):
        if y in BS and not _close(c["cash_end"], BS[y]["cash"]):
            bad.append("%d cash at the end of the cash-flow statement %d against a "
                       "balance sheet %d" % (y, c["cash_end"], BS[y]["cash"]))
    for y, k in sorted(CAPITAL.items()):
        implied = k["issued_capital"] / k["par_value"]
        if abs(implied - k["shares"]) > max(1.0, 1e-6 * k["shares"]):
            bad.append("%d capital %.0f / par %.4g = %.0f against a stated %.0f — the "
                       "document does not foot against itself" % (
                           y, k["issued_capital"], k["par_value"], implied, k["shares"]))
    return bad


_BAD = foot()
assert not _BAD, "the valuation-input block does not foot: " + "; ".join(_BAD)


def debt(y):
    """Interest-bearing borrowings, on this run's own definition.

    `panel.py` forms the effective rate on long-term borrowings, their current
    portion and credit facilities, and excludes trade and notes payable,
    creditors and other credit balances and current tax BY CONSTRUCTION — the
    [R-FCAL-01] trap (i) discipline. The same three lines are what is committed
    here, so the block and the panel cannot disagree about what debt means. The
    lease liabilities are carried BESIDE them, named, because folding them in or
    dropping them are both valuation choices and this record makes neither.
    """
    b = BS[y]
    return b["borrowings_nc"] + b["borrowings_cp"] + b["credit_facilities"]


def working_capital(y):
    """Operating working capital: the trading lines, and nothing else.

    Cash, borrowings, credit facilities, current tax, the dividend declared but
    unpaid, provisions and lease liabilities are all EXCLUDED and all named in
    the record, because a reader cannot tell an excluded line from an unread one.
    """
    b = BS[y]
    assets = (b["inventories"] + b["trade_receivables"] + b["debtors"]
              + b["due_from_related"])
    liabs = b["trade_payables"] + b["creditors"] + b["due_to_related"]
    return assets - liabs


def source(y, statement, page):
    f = FILES[y][0]
    return ("%s, %s, page %s (the company's own audited consolidated financial "
            "statements for the year ended 31 December %d, from its own "
            "investor-relations archive)"
            % (f, statement, ", ".join(str(p) for p in page), y))


def _cash(y):
    b, r = BS[y], dict(NOTES.get((y, "cash"), {}))
    rec = {
        "value": b["cash"],
        "as_at": "%d-12-31" % y,
        "source": source(y, "consolidated statement of financial position, "
                            "'Cash and bank balances'", BS[y]["page"]),
        "route": ROUTE,
        "lines": {"cash_and_bank_balances": b["cash"]},
        "check": ("the cash-flow statement closes on the same figure — "
                  "%d" % CF[y]["cash_end"]),
    }
    rec.update(r)
    return rec


def _debt(y):
    b = BS[y]
    return {
        "value": debt(y),
        "as_at": "%d-12-31" % y,
        "source": source(y, "consolidated statement of financial position, "
                            "borrowings (non-current), current portion of long-term "
                            "borrowings and credit facilities", BS[y]["page"]),
        "route": ROUTE,
        "definition": ("long-term borrowings, their current portion and credit "
                       "facilities — the three lines this run's own panel.py forms "
                       "its effective rate on, so the block and the panel cannot "
                       "disagree about what debt means"),
        "lines": {
            "borrowings_non_current": b["borrowings_nc"],
            "current_portion_of_long_term_borrowings": b["borrowings_cp"],
            "credit_facilities": b["credit_facilities"],
        },
        "carried_beside_not_folded_in": {
            "lease_liabilities_non_current": b["lease_nc"],
            "lease_liabilities_current": b["lease_c"],
            "notes_payable_non_current": b["notes_payable_nc"],
            "why": ("whether a lease liability or a long-dated supplier balance is "
                    "debt is a valuation choice; this record reads the page and "
                    "makes neither choice, so both are named rather than folded in "
                    "or dropped"),
        },
        "check": ("reproduces this run's own committed panel.DEBT total for the "
                  "same year"),
    }


def _capex(y):
    c = CF[y]
    disclosed = c["capex_ppe"] + c["capex_auc"] + c["capex_other"]
    rec = {
        "value": disclosed,
        "period": "FY%d" % y,
        "source": source(y, "consolidated statement of cash flows, investing "
                            "activities — payments for property, plant and equipment "
                            "and payments for assets under construction", c["page"]),
        "route": ROUTE,
        "derived": False,
        "disclosed": True,
        "lines": {
            "payments_for_property_plant_and_equipment": c["capex_ppe"],
            "payments_for_assets_under_construction": c["capex_auc"],
            "payments_for_other_assets": c["capex_other"],
        },
    }
    if y - 1 in BS:
        prior, now = BS[y - 1], BS[y]
        ident = ((now["ppe"] + now["auc"]) - (prior["ppe"] + prior["auc"])
                 + c["dep_ppe"])
        rec["identity_cross_check"] = {
            "identity": "capex = dPPE + D&A",
            "value": ident,
            "basis": ("property, plant and equipment plus assets under construction "
                      "at both dates, and the depreciation of property, plant and "
                      "equipment for the year"),
            "difference_from_disclosed": ident - disclosed,
            "note": ("the two are not the same measurement and the gap is not a "
                     "defect: disposals leave at net book value, additions can be "
                     "unpaid at the year end, and assets move out of construction "
                     "into property without cash. The DISCLOSED cash figure is what "
                     "is committed; the identity is reported beside it so a later "
                     "rebuild can see both rather than assume they agree"),
        }
    if c.get("note"):
        rec["note"] = c["note"]
    return rec


def _ppe(y):
    b = BS[y]
    return {
        "value": b["ppe"],
        "as_at": "%d-12-31" % y,
        "source": source(y, "consolidated statement of financial position, "
                            "'Property, plant and equipment (net)'", BS[y]["page"]),
        "route": ROUTE,
        "lines": {
            "property_plant_and_equipment_net": b["ppe"],
            "assets_under_construction": b["auc"],
            "right_of_use_assets_net": b["rou"],
            "intangible_assets_net": b["intangibles"],
        },
        "note": ("the identity capex = dPPE + D&A is run on property PLUS assets "
                 "under construction, because this company's spending lands in "
                 "construction first and moves across without cash; the intangible "
                 "is the operating licence and amortises on its own line"),
    }


def _dep(y):
    c = CF[y]
    total = (c["dep_ppe"] + c["amort_intangibles"] + c["amort_other"]
             + c["amort_rou"])
    rec = {
        "value": total,
        "period": "FY%d" % y,
        "source": source(y, "consolidated statement of cash flows, the "
                            "depreciation and amortisation add-backs", c["page"]),
        "route": ROUTE,
        "lines": {
            "depreciation_of_property_plant_and_equipment": c["dep_ppe"],
            "amortisation_of_intangible_assets": c["amort_intangibles"],
            "amortisation_of_other_assets": c["amort_other"],
            "amortisation_of_right_of_use_assets": c["amort_rou"],
        },
        "note": ("the whole charge, which is more than the cost-of-sales "
                 "depreciation this run's panel.py carries: that one is the "
                 "manufacturing share and this is the group total"),
    }
    if c.get("note"):
        rec["route_dispute"] = c["note"]
    return rec


def _wc(y):
    b = BS[y]
    rec = {
        "value": working_capital(y),
        "as_at": "%d-12-31" % y,
        "source": source(y, "consolidated statement of financial position, the "
                            "trading lines of current assets and current "
                            "liabilities", BS[y]["page"]),
        "route": ROUTE,
        "definition": ("inventories + trade receivables + debtors and other debit "
                       "balances + due from related parties, less trade and notes "
                       "payable, creditors and other credit balances and due to "
                       "related parties"),
        "lines": {
            "inventories": b["inventories"],
            "trade_receivables_net": b["trade_receivables"],
            "debtors_and_other_debit_balances_net": b["debtors"],
            "due_from_related_parties": b["due_from_related"],
            "trade_and_notes_payable": b["trade_payables"],
            "creditors_and_other_credit_balances": b["creditors"],
            "due_to_related_parties": b["due_to_related"],
            "total_current_assets": b["tca"],
            "total_current_liabilities": b["tcl"],
        },
        "excluded_and_named": {
            "cash_and_bank_balances": b["cash"],
            "credit_facilities": b["credit_facilities"],
            "current_portion_of_long_term_borrowings": b["borrowings_cp"],
            "current_income_tax_liability": b["tax_payable"],
            "dividends_payable": b["dividends_payable"],
            "provisions": b["provisions"],
            "lease_liabilities_current": b["lease_c"],
            "current_portion_of_long_term_other_liabilities": b["other_liab_cp"],
            "why": ("a reader cannot tell an excluded line from an unread one, so "
                    "every current line that is NOT in the working-capital figure "
                    "is named here with its own amount"),
        },
    }
    if (y, "wc") in NOTES:
        rec.update(NOTES[(y, "wc")])
    return rec


def _shares(y):
    if y not in CAPITAL:
        return {"missing": ("the capital note of the FY%d filing could not be read, "
                            "so no count is recorded — a count that does not foot "
                            "against its own issued capital and par value is not "
                            "recorded at all" % y)}
    k = CAPITAL[y]
    rec = {
        "value": k["shares"],
        "as_at": "%d-12-31" % y,
        "issued_capital": k["issued_capital"],
        "par_value": k["par_value"],
        "source": source(y, "note %s, the capital note" % k["note"], (k["page"],)),
        "route": ROUTE,
        "check": ("issued capital %d / par %g = %d, matching the count the same "
                  "note states" % (k["issued_capital"], k["par_value"],
                                   k["issued_capital"] / k["par_value"])),
        "par_source": k["par_source"],
        "vintage": ("read off the FY%d filing's own note; no later count is carried "
                    "back to this origin" % y),
    }
    if k.get("treasury_cost"):
        rec["treasury_shares_at_cost"] = k["treasury_cost"]
        rec["note"] = k.get("treasury_note", "")
    return rec


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
              "GENERATED by engine/arcc_walkforward/valuation_inputs.py, which "
              "foots every balance sheet against its own subtotals at import; "
              "never hand-edited."),
        "run": "ARCC",
        "rule": "[R-FCAL-01 AMENDED] (03-09-2026)",
        "company": "Arabian Cement Company S.A.E.",
        "currency": "EGP",
        "units": "as printed in the filings — units, not thousands or millions",
        "basis": "consolidated",
        "fiscal_year_end": "31 December",
        "origins_declared_by": "PRE_REGISTRATION_01-09-2026.md",
        "route": ROUTE,
        "point_in_time": (
            "every year is carried AS FIRST REPORTED, from its own filing's own "
            "column. The one re-presentation inside this window is recorded beside "
            "the figure it would replace and never substituted."),
        "sources": {str(y): FILES[y][0] for y in sorted(FILES)},
        "origins": {"FY%d" % y: block(y) for y in range(2018, 2026)},
        "prior_year_anchor": {
            "_": ("FY2017 is NOT an origin of this run. It is carried because the "
                  "identity capex = dPPE + D&A needs property at two dates and "
                  "FY2018 is the first origin; recording it inside `origins` would "
                  "misstate what this run tested."),
            "FY2017": block(2017),
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
        "_": ("GENERATED by engine/arcc_walkforward/valuation_inputs.py from that "
              "run's own reading of each year's capital note — NOT by "
              "extract_shares.py, whose scan this did not run. Never hand-edited."),
        "ticker": "ARCC",
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
            "file": FILES[y][0],
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
        raise SystemExit("REFUSED — the block does not foot:\n  "
                         + "\n  ".join(bad))
    rec = record()
    p = os.path.join(HERE, "valuation_inputs.json")
    json.dump(rec, open(p, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    q = os.path.join(CALIB, "shares_arcc.json")
    json.dump(shares_record(), open(q, "w", encoding="utf-8"), indent=1,
              ensure_ascii=False)

    print("valuation-input block — ARCC\n")
    print("  %-8s %14s %14s %14s %12s %14s %14s %12s"
          % ("origin", "cash", "debt", "capex", "ppe", "D&A", "working cap", "shares"))
    print("  " + "-" * 108)
    for y in range(2018, 2026):
        b = block(y)
        def v(i):
            r = b[i]
            return "MISSING" if "missing" in r else "%,.0f".replace(",", "") % 0 \
                if r.get("value") is None else format(r["value"], ",.0f")
        print("  FY%-6d %14s %14s %14s %14s %14s %14s %12s"
              % (y, v("cash"), v("debt"), v("capex"), v("ppe"), v("dep"), v("wc"),
                 v("shares")))
    n_missing = sum(1 for y in range(2018, 2026) for i, r in block(y).items()
                    if "missing" in r)
    print("\n  %d origins x 7 items = %d cells, %d recorded missing"
          % (8, 8 * 7, n_missing))
    print("  wrote %s" % os.path.relpath(p, os.path.dirname(os.path.dirname(HERE))))
    print("  wrote %s" % os.path.relpath(q, os.path.dirname(os.path.dirname(HERE))))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
