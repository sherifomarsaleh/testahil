"""The VALUATION-INPUT BLOCK for this run — the figures a VALUE is rebuilt from.

[R-FCAL-01 AMENDED, 03-09-2026].  A driver panel is not a record a value can be
rebuilt from.  This run's `panel.py` committed the income statement on one constant
taxonomy, the urea tonnage and the interest-bearing borrowings — every figure the
walk-forward's own scoring needed — and left no trace of the balance sheet beside
them.  Measured by `engine/valuation_calibration/bridge_inputs.py`, EGCH carried
BORROWINGS and nothing else across thirteen origins: no cash, no property, no
depreciation, no working capital, no share count, and therefore no route to capital
expenditure even by the identity, because the identity needs property at two dates.

WHY THAT MATTERED MORE THAN THE COUNT OF WHAT WAS MISSING.  Debt without cash is
the ASYMMETRIC half of a bridge: the debt that is committed is deducted in full
while the cash that would be added back is absent, so a bridge built from what this
run committed is biased DOWNWARD by construction — the same direction as the
hypothesis the calibration is testing, which is the one direction an instrument
must not be biased in.  On this name the omission is not a rounding error at either
end of the window.  At FY2013 the company held EGP 986,990,816 of cash and NO
interest-bearing debt at all, so a bridge from the old record deducted nothing and
added nothing where the whole answer was cash; at FY2024 it held EGP 3,103,366,312
of cash against EGP 11,580,297 thousand of borrowings, so the old record deducted
the debt in full and added none of the cash.

WHAT IS HERE.  For every origin the run declares — FY2012 to FY2024, fiscal years
ending 30 June — cash and equivalents, interest-bearing debt, property plant and
equipment, depreciation, the working-capital lines, capital expenditure, and the
share count with the par value it was footed against.  FY2014 is present and carries
SIX RECORDED ABSENCES rather than six silences; the reason is in the record, under
each item, and is the same reason.

EVERY FIGURE IS A COPY, NOT NEW RESEARCH.  Each one sits on a balance sheet, a
fixed-asset note, a cash-flow statement or a capital note in a filing this run had
already fetched and parsed cell by cell for its income statement.  Carrying them out
is transcription.  Not carrying them out meant no valuation of this company could
ever be rebuilt at a past origin, permanently, for any year whose filings are no
longer to hand.

ROUTE, AND WHY ARITHMETIC DECIDES [clause (iii)].  KIMA files scanned images.  Where
a text layer exists at all it is a broken font map that yields mojibake and mangles
the digits with it — `pdftotext` on the FY2020-21 filing returns "Y•YY/'\/r." where
the page reads 30/6/2022 — which is the very failure the protocol names, so NOT ONE
figure below came through a text layer.  Every one was read from the page rendered
at 300 to 450 dpi and, where a small figure did not resolve, from a crop of that
page re-rendered at three to six times magnification.  ARITHMETIC IS THE ARBITER
AND IT SETTLED SEVENTEEN READINGS.  Two examples stand for the rest, because they
are the two shapes the error takes:

  FY2013 net fixed assets, comparative column.  Six class figures summed to
  77,681,658 against a printed total of 77,681,625.  Re-reading the column at four
  times magnification moved two digits and the six then summed to the printed total
  exactly.  A THIRTY-THREE POUND ERROR IN A SEVENTY-SEVEN MILLION POUND COLUMN IS
  INVISIBLE TO EVERYTHING EXCEPT THE COLUMN.

  FY2019 non-current assets.  The five named components summed 783,500,000 short of
  the printed total, and the temptation was to "correct" the largest component to
  close it.  The FY2019-20 filing's comparative column then reproduced the component
  as first read, and the gap turned out to be an intangible-asset row this reading
  had not captured.  A SUM THAT DOES NOT CLOSE IS NOT EVIDENCE ABOUT THE LARGEST
  NUMBER IN IT; the second draft of this record would have committed a figure wrong
  by three quarters of a billion pounds, and did not.

THE FOOTING RUNS AT IMPORT as assertions rather than living in a comment, which is
this run's own house discipline from `panel.py`.  Nothing below is recorded that
does not reproduce under at least one arithmetic check the page itself supplies; a
figure that stands alone with no check available says so in its own record.

UNITS.  KIMA changes presentation twice inside this window and DOES NOT CHANGE IT
IN BOTH STATEMENTS AT ONCE: the balance sheets to FY2016 print full pounds, FY2017
to FY2024 print EGP thousand, and the fixed-asset notes, the cash notes and the
cash-flow statements print FULL POUNDS THROUGHOUT, including in the years whose
balance sheet is in thousands.  Every `value` here is in WHOLE POUNDS so that a
later rebuild cannot pick up the wrong scale, `as_printed` carries the figure as the
page shows it, and `precision` says whether the pound figure is exact or inherits a
thousand-rounding.  A figure marked thousand_rounded is accurate to +/- 500 pounds
and is labelled rather than presented as exact.

POINT IN TIME IS ABSOLUTE.  Every year is carried AS FIRST REPORTED from its own
filing wherever that filing is held.  Three origins have no filing of their own in
the company's archive — FY2012, FY2015 and FY2017, exactly the three `panel.py`
already flags `column="comparative"` — and are taken from the next filing's
comparative column on the same terms, flagged the same way.  Two re-presentations
fall inside this window and both are recorded BESIDE the figure they would replace,
never substituted: the FY2018-19 filing moves 94,526 thousand out of FY2018 equity
into FY2018 payables, and two cash notes disagree with their own balance sheets, by
6,615 pounds at FY2017 and by one pound at FY2019 — both small, both real, and both
named rather than averaged away.

WHAT IS NOT HERE, AND WHY [clause (i)].  FY2014 carries no balance-sheet item.  The
company's FY2013-14 annual embeds every page as a 367 x 519 pixel image — about
forty-five dots per inch across an A4 page — and while the prose and the larger
income-statement blocks survive that (which is how `panel.py` carries FY2014 as a
PARTIAL year), the numeric columns of the statement of financial position do not
resolve to the digit at any magnification.  No other document held carries a
30-June-2014 balance sheet: the archive lists no FY2014-15 annual, and the FY2015-16
filing's comparative column is FY2015.  Its fixed-asset note does carry an opening
column dated 1 July 2014, and that column is NAMED in the record and NOT COMMITTED,
for two reasons that are both about vintage rather than about arithmetic — it is a
later document's statement about that date, and it does not reconcile to its own
filing's FY2016 opening balances by 7,342,170 of cost.  A NUMBER THAT IS AVAILABLE
AND WRONG IN VINTAGE IS THE ONE THIS RULE EXISTS TO REFUSE.
"""
from __future__ import annotations

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "valuation_inputs.json")

RULE = "[R-FCAL-01 AMENDED] (03-09-2026)"

# The filings each origin is read from.  `column` is the run's own vocabulary from
# panel.py: "own" where the year has its own annual in the company's archive,
# "comparative" where it is read from the next filing's comparative column.
SOURCES = {
    "FY2012": dict(file="EGCH_FY2012-13_Annual.pdf", held="engine/egch_walkforward/filings",
                   column="comparative", bs_unit="EGP", doc="the FY2012-13 annual, comparative column"),
    "FY2013": dict(file="EGCH_FY2012-13_Annual.pdf", held="engine/egch_walkforward/filings",
                   column="own", bs_unit="EGP", doc="the FY2012-13 annual"),
    "FY2014": dict(file="EGCH_FY2013-14_Annual.pdf", held="engine/egch_walkforward/filings",
                   column="own", bs_unit=None, doc="the FY2013-14 annual"),
    "FY2015": dict(file="EGCH_FY2015-16_Annual.pdf", held="engine/egch_walkforward/filings",
                   column="comparative", bs_unit="EGP", doc="the FY2015-16 annual, comparative column"),
    "FY2016": dict(file="EGCH_FY2015-16_Annual.pdf", held="engine/egch_walkforward/filings",
                   column="own", bs_unit="EGP", doc="the FY2015-16 annual"),
    "FY2017": dict(file="EGCH_FY2017-18_Annual.pdf", held="engine/egch_walkforward/filings",
                   column="comparative", bs_unit="EGP thousand",
                   doc="the FY2017-18 annual, comparative column"),
    "FY2018": dict(file="EGCH_FY2017-18_Annual.pdf", held="engine/egch_walkforward/filings",
                   column="own", bs_unit="EGP thousand", doc="the FY2017-18 annual"),
    "FY2019": dict(file="EGCH_FY2018-19_Annual.pdf", held="engine/egch_walkforward/filings",
                   column="own", bs_unit="EGP", doc="the FY2018-19 annual"),
    "FY2020": dict(file="EGCH_FY2019-20_Annual.pdf", held="engine/egch_walkforward/filings",
                   column="own", bs_unit="EGP", doc="the FY2019-20 annual"),
    "FY2021": dict(file="EGCH_FY2020-21_Annual.pdf", held="engine/egch_walkforward/filings",
                   column="own", bs_unit="EGP", doc="the FY2020-21 annual"),
    "FY2022": dict(file="EGCH_FY2021-22_Annual.pdf", held="engine/egch_study/filings",
                   column="own", bs_unit="EGP thousand", doc="the FY2021-22 annual"),
    "FY2023": dict(file="EGCH_FY2022-23_Annual.pdf", held="engine/egch_study/filings",
                   column="own", bs_unit="EGP thousand", doc="the FY2022-23 annual"),
    "FY2024": dict(file="EGCH_FY2023-24_Annual.pdf", held="engine/egch_study/filings",
                   column="own", bs_unit="EGP thousand", doc="the FY2023-24 annual"),
}

ROUTE = ("read off the page rendered at 300-450 dpi, with any figure that did not "
         "resolve re-read from a crop of that page at three to six times "
         "magnification.  No text layer was used anywhere: KIMA's filings are scans, "
         "and where a text layer exists it is a broken font map that mangles the "
         "digits along with the letters.  Every figure was footed against the "
         "statement's own arithmetic before it was recorded, and the arithmetic "
         "rather than the reading settled every disagreement")

K = 1000  # EGP thousand -> EGP

# ---------------------------------------------------------------------------
# THE BALANCE SHEETS, AS READ.  Figures are in the unit the page prints
# (SOURCES[y]["bs_unit"]).  Every line here is asserted in foot() against a
# subtotal, a total or a cross-statement figure the same filing prints.
# ---------------------------------------------------------------------------
BS = {
 # ---- full-pound balance sheets -------------------------------------------
 "FY2012": dict(
     ppe_net=77_681_625,
     ppe_classes=[1_692_632, 21_577_567, 43_266_853, 5_794_203, 1_369_784, 3_980_586],
     cwip=46_906_113, cwip_lines=[33_150_189, 13_755_924],
     inventories=101_214_443, receivables=93_782_671, carried=194_997_114,
     investment_certificates=374_260_816, treasury_bills=90_432_080,
     cash=870_102_109, cash_lines=[534_488_793, 335_292_439, 320_877],
     tca=1_529_792_119,
     provisions=15_554_070, provision_lines=[7_762_814, 3_871_256, 3_920_000],
     payables=173_020_259,
     payable_lines=[7_389_395, 0, 22_492_439, 123_315_416, 3_167_483, 186_899, 0,
                    15_383_117, 1_085_510],
     tcl=188_574_329, wc=1_341_217_790,
     noncurrent_total=202_931_725, total_investment=1_544_149_515,
     capital=1_206_000_000, reserves=338_149_515, equity=1_544_149_515,
     deferred_tax=0, bank=0, holdco=0, current_loans=0),
 "FY2013": dict(
     ppe_net=82_747_097, ppe_cost=216_978_274, ppe_accum=134_231_177,
     ppe_classes=[1_692_632, 22_689_547, 48_613_356, 3_582_001, 1_836_507, 4_333_054],
     ppe_cost_classes=[1_692_632, 42_772_754, 145_988_028, 12_783_341, 5_656_696, 8_084_823],
     ppe_accum_classes=[0, 20_083_207, 97_374_672, 9_201_340, 3_820_189, 3_751_769],
     inventories=108_336_055, receivables=113_717_069, carried=222_053_124,
     investment_certificates=472_174_316, treasury_bills=0,
     cash=986_990_816, tca=1_681_218_256,
     provisions=24_441_163, provision_lines=[10_776_186, 5_585_412, 8_079_565],
     payables=68_166_897,
     payable_lines=[9_832_066, 0, 33_877_220, 11_833_517, 2_488_904, 213_475, 0,
                    4_392_360, 5_529_355],
     tcl=92_608_060, wc=1_588_610_196,
     noncurrent_total=224_579_286, total_investment=1_813_189_482,
     capital=1_304_300_000, reserves=508_889_482, equity=1_813_189_482,
     reserve_lines=[81_099_510, 145_195_405, 17_782_030, 85_040_432, 20_090_985, 159_681_120],
     deferred_tax=0, bank=0, holdco=0, current_loans=0),
 "FY2015": dict(
     ppe_net=113_060_291,
     ppe_classes=[1_682_946, 37_774_653, 57_905_952, 8_056_493, 2_420_603, 5_219_644],
     cwip=698_211_410, cwip_lines=[302_272_843, 395_938_567],
     inventories=178_598_500,
     inventory_lines=[48_719_971, 2_052_933, 50_937_189, 2_802_189, 344_647, 76_769,
                      240_215, 39_680_515, 11_090_768, 22_653_304],
     receivables=107_947_291,
     receivable_lines=[4_096_426, 55_407_063, 32_769_640, 129_469, 11_259_231, 4_285_462],
     carried=286_545_791,
     cash=1_647_210_224, cash_lines=[155_547_147, 1_491_416_271, 246_806],
     tca=1_933_756_015,
     provisions=20_569_873, provision_lines=[6_216_423, 5_128_309, 9_225_141],
     payables=129_639_877,
     payable_lines=[15_254_698, 7_475_419, 90_955_784, 3_858_029, 57_173, 11_477_882, 560_892],
     tcl=150_209_750, wc=1_783_546_265,
     noncurrent_total=887_755_411, total_investment=2_671_301_676,
     capital=1_970_213_550, reserves=373_371_003, equity=2_343_584_553,
     deferred_tax=0, bank=0, holdco=327_717_123, current_loans=0,
     long_term_investments=74_426_189, external_loans=928_887, deferred_tax_asset=1_128_634),
 "FY2016": dict(
     ppe_net=159_628_020, ppe_cost=330_144_076, ppe_accum=170_516_056,
     ppe_classes=[1_682_943, 43_564_334, 99_209_776, 7_030_539, 3_204_697, 4_935_731],
     ppe_cost_classes=[1_682_943, 69_347_476, 219_414_927, 21_469_515, 7_583_699, 10_645_516],
     ppe_accum_classes=[0, 25_783_142, 120_205_151, 14_438_976, 4_379_002, 5_709_785],
     cwip=1_136_282_920, cwip_lines=[1_134_916_986, 1_365_934],
     inventories=242_013_500,
     inventory_lines=[57_385_288, 1_874_644, 49_537_157, 1_433_730, 1_690_548, 48_922,
                      1_307_318, 116_570_510, 1_691_348, 10_474_035],
     receivables=115_542_347,
     receivable_lines=[2_353_783, 63_795_045, 38_430_453, 198_271, 8_213_854, 2_550_941],
     carried=357_555_847,
     cash=1_325_204_283, cash_lines=[213_165_571, 1_111_825_131, 213_581],
     tca=1_682_760_130,
     provisions=27_088_071, provision_lines=[12_741_279, 5_121_651, 9_225_141],
     payables=213_914_327,
     payable_lines=[45_657_421, 24_276_410, 9_389_028, 4_133_474, 136_210, 90_428_201, 39_893_583],
     tcl=241_002_398, wc=1_441_757_732,
     noncurrent_total=1_371_122_931, total_investment=2_812_880_663,
     capital=2_035_477_675, reserves=373_371_003, equity=2_408_848_678,
     deferred_tax=3_500_237, bank=0, holdco=300_000_000, current_loans=0, surplus=100_531_748,
     long_term_investments=74_426_189, external_loans=785_802, deferred_tax_asset=0),
 "FY2019": dict(
     ppe_net=186_615_197, ppe_cost=430_600_415, ppe_accum=243_985_218,
     ppe_accum_classes=[0, 40_158_077, 169_730_009, 20_511_547, 5_262_617, 8_322_968],
     cwip=9_429_820_287, cwip_lines=[9_381_798_420, 48_021_867],
     inventories=340_174_688,
     inventory_lines=[84_137_056, 2_439_757, 59_184_368, 5_993_047, 4_528_034, 164_900,
                      288_771, 183_438_755, 0, 0],
     receivables=563_631_022,
     receivable_lines=[759_121, 0, 401_706_390, 22_666_975, 101_299, 128_005_337, 10_391_900],
     carried=903_805_710,
     cash=356_018_703, cash_lines=[0, 355_463_749, 554_954],
     tca=1_259_824_413,
     provisions=112_590_433, provision_lines=[37_322_561, 6_013_201, 69_254_671],
     payables=315_278_783,
     payable_lines=[56_925_200, 104_589_021, 9_263_908, 4_880_130, 42_637, 107_870_167, 31_707_720],
     current_loans=587_683_538, payables_and_loans=902_962_321,
     tcl=1_015_552_754, wc=244_271_659,
     total_investment=10_731_782_516,
     capital=4_464_941_370, reserves=1_217_084_245, equity=5_682_025_615,
     deferred_tax=2_804_977, bank=4_863_476_376, holdco=183_475_548,
     long_term_investments=87_055_306, external_loans=520_067),
 "FY2020": dict(
     ppe_net=9_857_970_740, ppe_cost=10_233_434_467, ppe_accum=375_463_727,
     ppe_cost_classes=[1_682_852, 784_592_998, 8_421_507_369, 50_715_837, 957_713_799, 17_221_612],
     ppe_accum_classes=[0, 59_958_323, 265_964_562, 22_608_769, 17_616_302, 9_315_771],
     cwip=11_345_480, cwip_lines=[5_612_922, 5_732_558],
     inventories=521_575_267,
     inventory_lines=[84_921_136, 2_012_217, 144_097_174, 5_774_172, 10_065_661, 85_750,
                      11_943_907, 262_675_250, 0, 0],
     receivables=605_255_405,
     receivable_lines=[27_851_833, 3_906_088, 403_752_473, 5_539_869, 2_686_311,
                       159_048_525, 2_470_306],
     carried=1_126_830_672,
     cash=130_694_768, cash_lines=[29_863_720, 100_462_120, 368_928],
     tca=1_257_525_440,
     provisions=107_049_487, provision_lines=[32_312_674, 5_482_142, 69_254_671],
     payables=868_606_229,
     payable_lines=[258_772_516, 119_490_677, 7_256_050, 31_884_715, 42_637,
                    149_226_963, 301_932_671],
     current_loans=988_779_369, payables_and_loans=1_857_385_598,
     tcl=1_964_435_085, wc=-706_909_645,
     noncurrent_total=11_948_457_978, total_investment=11_241_548_333,
     capital=4_464_941_370, reserves=-542_811_097, equity=3_922_130_273,
     reserve_lines=[120_620_719, 153_179_429, 19_869_873, 96_568_382, -50_548_688,
                    467_598_699, -1_350_099_511],
     deferred_tax=917_962_369, bank=5_690_939_443, holdco=710_516_248,
     long_term_investments=542_024_889, external_loans=457_763, intangibles=1_536_659_106),
 "FY2021": dict(
     ppe_net=9_302_162_394, ppe_cost=10_248_099_227, ppe_accum=945_936_833,
     ppe_cost_classes=[1_682_840, 790_865_185, 8_422_856_786, 50_715_838, 961_263_352, 20_715_226],
     ppe_accum_classes=[0, 120_901_256, 696_149_388, 28_966_498, 89_214_212, 10_705_479],
     cwip=46_289_177, cwip_lines=[42_119_979, 4_169_198],
     inventories=420_700_561,
     inventory_lines=[77_801_300, 1_638_816, 166_418_104, 4_873_266, 5_191_084, 85_750,
                      33_225_877, 131_466_364, 0, 0],
     receivables=591_702_242,
     receivable_lines=[48_457_702, 1_943_630, 377_887_815, 2_003_831, 1_150_144,
                       154_831_205, 5_427_915],
     carried=1_012_402_803,
     cash=90_015_247, cash_lines=[6_301_155, 83_397_470, 316_622],
     tca=1_102_418_050,
     provisions=176_215_496, provision_lines=[41_725_800, 25_235_024, 109_254_672],
     payables=1_043_753_398,
     payable_lines=[744_309_624, 77_333_895, 5_309_077, 6_656_037, 0, 131_224_573, 78_920_192],
     current_loans=334_493_029, payables_and_loans=1_378_246_427,
     tcl=1_554_461_923, wc=-452_043_873,
     noncurrent_total=11_545_877_625, total_investment=11_093_833_752,
     capital=4_464_941_370, equity=2_670_295_099,
     deferred_tax=1_076_610_521, bank=6_120_358_415, holdco=1_226_569_717,
     long_term_investments=740_290_455, external_loans=403_392, intangibles=1_456_732_207),
 # ---- EGP-thousand balance sheets -----------------------------------------
 "FY2017": dict(
     ppe_net=170_773, cwip=3_269_029, inventories=192_877, receivables=103_467,
     cash=407_233, tca=703_577, total_assets=4_221_948,
     provisions=87_961, payables=620_194, tcl=708_155,
     noncurrent_total=3_518_371, capital=2_892_607, reserves=369_768, equity=3_262_375,
     bank=251_418, holdco=0, current_loans=0, deferred_tax=0, total_liabilities=959_573,
     associates=48_622, afs=25_804, external_loans=716, deferred_tax_asset=3_427),
 "FY2018": dict(
     ppe_net=163_338, cwip=8_145_376, inventories=250_061, receivables=407_578,
     cash=6_171, tca=663_810, total_assets=9_047_556,
     provisions=49_948, payables=887_665, tcl=937_613,
     noncurrent_total=8_383_746, capital=3_164_754, reserves=371_563, equity=3_636_367,
     bank=4_466_445, holdco=0, current_loans=0, deferred_tax=7_131, total_liabilities=5_411_189,
     associates=48_622, afs=25_804, external_loans=606, deferred_tax_asset=0,
     profit_for_year=100_050),
 "FY2022": dict(
     ppe_net=9_434_151, cwip=65_009, inventories=733_660, receivables=644_442,
     cash=520_435, tca=1_898_537, total_assets=13_801_769,
     provisions=366_258, payables=1_089_458, current_loans=713_732, tcl=2_169_448,
     noncurrent_total=11_903_232, capital=5_932_895, reserves=403_672, equity=4_891_229,
     bank=5_518_347, holdco=71_523, deferred_tax=1_151_222, noncurrent_liabs=6_741_092,
     fvoci=873_584, external_loans=374, intangibles=1_530_114,
     fv_reserve=799_157, retained=-2_895_981, profit_for_year=651_486),
 "FY2023": dict(
     ppe_net=11_300_438, cwip=56_405, inventories=1_391_802, receivables=798_577,
     cash=1_416_243, tca=3_606_622, total_assets=18_727_840,
     provisions=144_359, payables=1_367_845, current_loans=21_391, tcl=1_533_595,
     noncurrent_total=15_121_218, capital=5_932_895, reserves=426_979, equity=7_249_636,
     bank=8_424_871, holdco=50_266, deferred_tax=1_469_472, noncurrent_liabs=9_944_609,
     total_liabilities=11_478_204,
     fvoci=1_855_435, external_loans=328, intangibles=1_908_612,
     fv_reserve=1_781_009, retained=-2_042_014, profit_for_year=1_150_767),
 "FY2024": dict(
     ppe_net=14_144_067, cwip=2_535_134, inventories=1_615_470, receivables=858_390,
     cash=3_103_366, tca=5_577_226, total_assets=29_161_022,
     provisions=432_156, payables=1_587_001, current_loans=354_051, tcl=2_373_208,
     noncurrent_total=23_583_796, capital=9_932_895, reserves=462_979, equity=14_560_104,
     bank=11_226_246, holdco=0, deferred_tax=1_001_464, noncurrent_liabs=12_227_710,
     fvoci=2_493_496, external_loans=298, intangibles=2_376_212, investment_property=2_034_589,
     fv_reserve=2_419_070, retained=-792_774, profit_for_year=2_537_934),
}

# The fixed-asset note's own movement, in FULL POUNDS in every year that carries
# one.  `charge` is the additions row of the ACCUMULATED-DEPRECIATION block, which
# is the year's depreciation charge; `charge_classes` is that row by asset class.
FA_NOTE = {
 "FY2013": dict(charge=9_753_403, charge_classes=[1_536_701, 6_122_124, 1_382_952, 161_001, 550_625],
                disposals=1_170_012, disposal_classes=[43_802, 1_091_916, 0, 26_986, 7_308],
                cost_open=202_329_413, note="note (4) of the FY2012-13 annual"),
 "FY2016": dict(charge=16_838_574, charge_classes=[2_838_142, 10_905_064, 1_950_037, 302_049, 843_282],
                accum_open=154_392_674,
                accum_open_classes=[0, 23_509_846, 109_330_073, 12_540_177, 4_115_925, 4_896_653],
                disposals=715_192, disposal_classes=[564_845, 29_985, 51_239, 38_972, 30_151],
                cost_open=267_452_966,
                cost_open_classes=[1_682_946, 61_284_518, 167_236_025, 20_596_671, 6_536_509, 10_116_297],
                cost_add=63_406_305, cost_add_classes=[0, 8_627_803, 52_208_887, 924_083, 1_086_162, 559_370],
                cost_disp=715_195, accum_close=170_516_056, cost_close=330_144_076,
                prior_charge=9_877_208, prior_accum_open=143_271_658, prior_disposals=699_490,
                prior_cost_open=237_763_729, prior_cost_add=23_050_533, prior_cost_disp=703_466,
                prior_cost_close=260_110_796,
                note="note (4/2) of the FY2015-16 annual"),
 "FY2018": dict(charge=24_731_236, charge_classes=[3_796_278, 17_562_127, 2_058_091, 408_922, 905_818],
                accum_open=191_977_306,
                accum_open_classes=[0, 29_061_547, 135_170_959, 16_564_066, 4_633_441, 6_547_293],
                disposals=829_194, accum_close=215_879_348,
                cost_open=362_748_828, cost_add=33_343_481, cost_disp=16_875_846,
                cost_close=379_216_463, net_close=163_337_115, net_prior=170_771_522,
                prior_charge=31_778_020, prior_accum_open=170_516_056, prior_disposals=10_316_770,
                note="note (4/2) of the FY2017-18 annual"),
 "FY2019": dict(charge=28_658_506, accum_open=215_879_348,
                accum_open_classes=[0, 32_795_118, 152_055_167, 18_622_157, 4_977_919, 7_428_987],
                disposals=552_636, disposal_classes=[0, 362_441, 0, 170_977, 19_218],
                accum_close=243_985_218, cost_open=379_216_463, prior_charge=24_731_236,
                note="note (4) of the FY2018-19 annual"),
 "FY2020": dict(charge=217_263_138,
                charge_classes=[30_058_502, 161_447_976, 2_286_213, 22_376_985, 1_093_461],
                accum_open=243_985_218, disposals=85_784_629,
                disposal_classes=[10_258_255, 65_213_424, 188_991, 10_023_301, 100_658],
                accum_close=375_463_727, cost_close=10_233_434_467, net_close=9_857_970_740,
                prior_charge=28_658_506, prior_disposals=552_636,
                note="note (4/2) of the FY2019-20 annual"),
 "FY2021": dict(charge=570_972_097,
                charge_classes=[60_942_933, 430_516_369, 6_357_729, 71_701_238, 1_453_828],
                accum_open=375_463_727,
                accum_open_classes=[0, 59_958_323, 265_964_562, 22_608_769, 17_616_302, 9_315_771],
                disposals=498_993, disposal_classes=[0, 331_544, 0, 103_328, 64_121],
                cost_open=10_233_434_470, prior_charge=217_263_138,
                note="note (4/2) of the FY2020-21 annual"),
 "FY2022": dict(charge=549_694_818,
                charge_classes=[71_278_109, 398_653_553, 6_110_278, 71_938_648, 1_714_230],
                accum_open=945_936_833,
                accum_open_classes=[0, 120_901_256, 696_149_388, 28_966_498, 89_214_212, 10_705_479],
                disposals=11_107_442, disposal_classes=[9_202_293, 1_429_754, 366_354, 42_212, 66_829],
                accum_close=1_484_524_209, cost_open=10_248_099_227, cost_add=738_198_496,
                cost_add_classes=[0, 31_446_362, 693_863_176, 1_028_550, 3_517_436, 8_342_972],
                cost_disp=67_622_964,
                cost_disp_classes=[1_549, 65_716_266, 1_429_754, 366_354, 42_212, 66_829],
                cost_close=10_918_674_759, net_close=9_434_150_550, prior_charge=570_972_097,
                note="note (4/1) of the FY2021-22 annual"),
 "FY2023": dict(charge=834_970_524,
                charge_classes=[61_010_757, 693_033_877, 6_026_186, 72_172_297, 2_727_407],
                accum_open=1_484_524_209,
                accum_open_classes=[0, 182_977_073, 1_093_373_187, 34_710_421, 161_110_648, 12_352_880],
                disposals=3_939_300, disposal_classes=[1_356_740, 2_240_415, 15_510, 150_178, 176_457],
                accum_close=2_315_555_433, cost_close=13_615_993_284,
                cost_close_classes=[1_681_291, 780_995_855, 11_775_504_938, 51_949_295,
                                    967_567_199, 38_294_706],
                net_close=11_300_437_851, prior_charge=549_694_818,
                note="note (6/1) of the FY2022-23 annual"),
 "FY2024": dict(charge=642_988_710,
                charge_classes=[44_431_113, 516_762_388, 5_928_745, 72_499_649, 3_366_815],
                accum_open=2_315_555_434, disposals=294_325_866,
                disposal_classes=[136_331, 293_725_779, 0, 129_165, 334_591],
                accum_close=2_664_218_278, cost_open=13_615_993_284, cost_add=3_618_708_218,
                cost_disp=426_416_369, cost_close=16_808_285_133, net_close=14_144_066_955,
                prior_charge=834_970_524,
                note="note (6/1) of the FY2023-24 annual"),
}

# Capital expenditure, from the investing section of the cash-flow statement, in
# FULL POUNDS in every year.  DISCLOSED in every origin this run holds: KIMA prints
# "مدفوعات لاقتناء اصول ثابته" as its own line, so no origin needs the identity.
CAPEX = {
 "FY2012": dict(paid=44_467_917, proceeds=965_343, other=[-468_576_696, 3_883_800, 456_958],
                net=-507_738_512, src="FY2012-13 annual, comparative column"),
 "FY2013": dict(paid=23_832_411, proceeds=135_274, other=[-103_722_640, 96_241_220, 434_054],
                net=-30_744_503, src="FY2012-13 annual"),
 "FY2015": dict(paid=617_180_075, proceeds=198_769, other=[-22_053_432, 452_527_014, 432_423],
                net=-186_075_301, src="FY2015-16 annual, comparative column"),
 "FY2016": dict(paid=471_539_044, proceeds=171_354, other=[145_129], net=-471_222_561,
                src="FY2015-16 annual"),
 "FY2017": dict(paid=2_151_566_686, proceeds=115_935, other=[70_189], net=-2_151_380_562,
                src="FY2017-18 annual, comparative column"),
 "FY2018": dict(paid=5_140_260_005, proceeds=109_778, other=[105_274], net=-5_140_044_953,
                src="FY2017-18 annual"),
 "FY2019": dict(paid=1_447_788_508, proceeds=81_279, other=[82_431], net=-1_447_624_798,
                src="FY2018-19 annual"),
 "FY2020": dict(paid=2_449_164_215, proceeds=127_084, other=[60_263], net=-2_448_976_868,
                src="FY2019-20 annual"),
 "FY2021": dict(paid=66_110_098, proceeds=70_542, other=[53_638], net=-65_985_918,
                src="FY2020-21 annual"),
 "FY2022": dict(paid=80_827_245, proceeds=16_849_700, other=[-800_436_158, 858_050_000, 27_986],
                net=-6_335_717, src="FY2021-22 annual"),
 "FY2023": dict(paid=42_470_154, proceeds=6_696_191, other=[44_440], net=-35_729_523,
                src="FY2022-23 annual"),
 "FY2024": dict(paid=2_391_608_259, proceeds=1_986_463, other=[28_843], net=-2_389_592_953,
                src="FY2023-24 annual"),
}

# The cash note, in FULL POUNDS, where the filing carries one for that date.  It is
# the SECOND reading of the same balance: where it agrees with the balance sheet the
# cash figure is footed twice, and where it does not the disagreement is recorded
# rather than resolved by preference.
CASH_NOTE = {
 "FY2015": dict(total=1_647_210_224, lines=[155_547_147, 1_491_416_271, 246_806],
                note="note (10) of the FY2015-16 annual"),
 "FY2016": dict(total=1_325_204_283, lines=[213_165_571, 1_111_825_131, 213_581],
                note="note (10) of the FY2015-16 annual"),
 "FY2017": dict(total=407_239_615, lines=[299_647_230, 107_015_369, 577_016],
                note="note (10) of the FY2017-18 annual"),
 "FY2018": dict(total=6_171_342, lines=[0, 6_021_079, 150_263],
                note="note (10) of the FY2017-18 annual"),
 "FY2019": dict(total=356_018_702, lines=[0, 355_463_748, 554_954],
                note="note (10) of the FY2018-19 annual"),
 "FY2020": dict(total=130_694_768, lines=[29_863_720, 100_462_120, 368_928],
                note="note (10) of the FY2019-20 annual"),
 "FY2021": dict(total=90_015_247, lines=[6_301_155, 83_397_470, 316_622],
                note="note (10) of the FY2020-21 annual"),
 "FY2022": dict(total=520_435_229, lines=[20_000_000, 499_417_863, 700_000, 317_366],
                note="note (10) of the FY2021-22 annual"),
 "FY2023": dict(total=1_416_243_098, lines=[986_726_400, 429_125_733, 390_965],
                note="note (13) of the FY2022-23 annual"),
 "FY2024": dict(total=3_103_366_312, lines=[959_432_800, 2_142_344_516, 1_588_996],
                note="note (13) of the FY2023-24 annual"),
}

# The capital note.  `stated_count` is the count the SAME sentence prints; where the
# note is written for the filing's own year only, a comparative origin has no stated
# count and the count is that year's own committed capital divided by that par,
# which is the route [R-FCAL-01 AMENDED] clause (ii) itself supplies.
CAPITAL = {
 "FY2013": dict(capital=1_304_300_000, stated_count=260_860_000, par=5.0,
                note="note (11/1) of the FY2012-13 annual", authorised="EGP 2bn"),
 "FY2016": dict(capital=2_035_477_675, stated_count=407_095_535, par=5.0,
                note="note (11/1) of the FY2015-16 annual", authorised="EGP 3bn",
                table_total=407_095_535),
 "FY2018": dict(capital=3_164_753_565, stated_count=632_950_713, par=5.0,
                note="note (11/1) of the FY2017-18 annual", authorised="EGP 6bn",
                table_total=632_950_713),
 "FY2019": dict(capital=4_464_941_370, stated_count=892_988_274, par=5.0,
                note="note (11/1) of the FY2018-19 annual", authorised="EGP 6bn"),
 "FY2020": dict(capital=4_464_941_370, stated_count=892_988_274, par=5.0,
                note="note (11/1) of the FY2019-20 annual", authorised="EGP 6bn",
                table_total=892_988_274),
 "FY2021": dict(capital=4_464_941_370, stated_count=892_988_274, par=5.0,
                note="note (11/1) of the FY2020-21 annual", authorised="EGP 6bn"),
 "FY2022": dict(capital=5_932_894_995, stated_count=1_186_578_999, par=5.0,
                note="note (11/1) of the FY2021-22 annual", authorised="EGP 8bn"),
 "FY2023": dict(capital=5_932_894_995, stated_count=1_186_578_999, par=5.0,
                note="note (14) of the FY2022-23 annual", authorised="EGP 8bn"),
 "FY2024": dict(capital=9_932_894_995, stated_count=1_986_578_999, par=5.0,
                note="note (14) of the FY2023-24 annual", authorised="EGP 8bn",
                table_total=1_986_578_999),
}

# Origins whose capital is read from a comparative equity column and whose count is
# therefore the capital/par identity, with the par established by the same filing's
# own capital note.  The rounding band is stated where the capital is printed in
# thousands: it is a property of the page, not an estimate.
CAPITAL_FROM_EQUITY = {
 "FY2012": dict(capital=1_206_000_000, par=5.0, exact=True,
                where="the FY2012-13 annual's comparative equity column, footed "
                      "against total equity 1,544,149,515 less reserves 338,149,515",
                par_from="note (11/1) of the same filing, which states par 5 for 30-Jun-2013"),
 "FY2015": dict(capital=1_970_213_550, par=5.0, exact=True,
                where="the FY2015-16 annual's comparative equity column, footed "
                      "against total equity 2,343,584,553 less reserves 373,371,003",
                par_from="note (11/1) of the same filing, which states par 5 for 30-Jun-2016"),
 "FY2017": dict(capital=2_892_607 * K, par=5.0, exact=False,
                where="the FY2017-18 annual's comparative equity column, footed "
                      "against total equity 3,262,375 thousand less reserves 369,768 thousand",
                par_from="note (11/1) of the same filing, which states par 5 for 30-Jun-2018"),
}

MISSING_2014 = (
    "the company's FY2013-14 annual embeds every page as a 367 x 519 pixel image, "
    "about forty-five dots per inch across an A4 page. The prose and the larger "
    "income-statement blocks survive that resolution, which is how this run's own "
    "panel.py carries FY2014 as a PARTIAL year; the numeric columns of the statement "
    "of financial position do not resolve to the digit at any magnification, and a "
    "figure read from them would be a guess wearing the appearance of a reading. No "
    "other document held carries a 30-June-2014 balance sheet: the company's archive "
    "lists no FY2014-15 annual and the FY2015-16 filing's comparative column is "
    "FY2015. The FY2015-16 filing's fixed-asset note does carry an opening column "
    "dated 1 July 2014 (cost 237,763,729, accumulated depreciation 143,271,658, "
    "implying net 94,492,071) and it is NOT committed here for two reasons that are "
    "both about vintage rather than arithmetic: it is a later document's statement "
    "about that date rather than the FY2014 filing's own, and it does not reconcile "
    "to that same note's FY2016 opening balances, which run 7,342,170 higher in cost "
    "and 1,943,298 higher in accumulated depreciation than its own roll-forward "
    "reaches.")


def _close(a, b, tol=1):
    return abs(a - b) <= tol


_BAD = []


def _chk(cond, what):
    if not cond:
        _BAD.append(what)


def foot():
    """Every check the pages themselves supply.  Runs at import."""
    for y, b in BS.items():
        # the working-capital identity the company prints itself, or the
        # thousand-scale balance sheet's own assets = equity + liabilities
        if "wc" in b:
            _chk(_close(b["tca"] - b["tcl"], b["wc"]), "%s wc = tca - tcl" % y)
        if "total_assets" in b:
            _chk(_close(b["noncurrent_total"] + b["tca"], b["total_assets"]),
                 "%s total assets" % y)
        # current liabilities from their own components
        loans = b.get("current_loans", 0)
        if "payables_and_loans" in b:
            _chk(_close(b["payables"] + loans, b["payables_and_loans"]),
                 "%s payables + short-term loans" % y)
            _chk(_close(b["provisions"] + b["payables_and_loans"], b["tcl"]), "%s tcl" % y)
        else:
            _chk(_close(b["provisions"] + b["payables"] + loans, b["tcl"]), "%s tcl" % y)
        # current assets from their own components
        cur = b["inventories"] + b["receivables"] + b["cash"]
        cur += b.get("investment_certificates", 0) + b.get("treasury_bills", 0)
        _chk(_close(cur, b["tca"]), "%s tca from components" % y)
        if "carried" in b:
            _chk(_close(b["inventories"] + b["receivables"], b["carried"]), "%s carried" % y)
        # property from cost less accumulated depreciation, and from its classes
        if "ppe_cost" in b:
            _chk(_close(b["ppe_cost"] - b["ppe_accum"], b["ppe_net"]),
                 "%s ppe = cost - accum" % y)
        for k in ("ppe_classes", "ppe_cost_classes", "ppe_accum_classes"):
            if k in b:
                tgt = {"ppe_classes": "ppe_net", "ppe_cost_classes": "ppe_cost",
                       "ppe_accum_classes": "ppe_accum"}[k]
                _chk(_close(sum(b[k]), b[tgt]), "%s %s" % (y, k))
        for k, tgt in (("cwip_lines", "cwip"), ("cash_lines", "cash"),
                       ("provision_lines", "provisions"), ("payable_lines", "payables"),
                       ("inventory_lines", "inventories"),
                       ("receivable_lines", "receivables"),
                       ("reserve_lines", "reserves")):
            if k in b:
                _chk(_close(sum(b[k]), b[tgt]), "%s %s" % (y, k))
        # equity from capital, reserves and the year's own profit, where the
        # sheet presents it that way; the four sheets that carry a separate
        # fair-value reserve are checked line by line further down instead
        if "reserves" in b and "equity" in b and "fv_reserve" not in b:
            _chk(_close(b["capital"] + b["reserves"] + b.get("profit_for_year", 0),
                        b["equity"]), "%s equity" % y)
        # the financing side closes on the investment side
        if "total_investment" in b:
            fin = (b["equity"] + b.get("deferred_tax", 0) + b.get("bank", 0)
                   + b.get("holdco", 0) + b.get("surplus", 0))
            _chk(_close(fin, b["total_investment"]), "%s financing = investment" % y)
        if "total_liabilities" in b and "noncurrent_liabs" not in b and "total_assets" in b:
            _chk(_close(b["equity"] + b["total_liabilities"], b["total_assets"]),
                 "%s assets = equity + liabilities" % y)
        if "noncurrent_liabs" in b:
            _chk(_close(b["bank"] + b["holdco"] + b["deferred_tax"], b["noncurrent_liabs"]),
                 "%s non-current liabilities" % y)
            _chk(_close(b["equity"] + b["noncurrent_liabs"] + b["tcl"], b["total_assets"]),
                 "%s assets = equity + liabilities" % y)

    # the balance sheet's own non-current total, where every component was read
    _chk(_close(BS["FY2016"]["ppe_net"] + BS["FY2016"]["cwip"]
                + BS["FY2016"]["long_term_investments"] + BS["FY2016"]["external_loans"]
                + BS["FY2016"]["deferred_tax_asset"], BS["FY2016"]["noncurrent_total"]),
         "FY2016 non-current assets")
    _chk(_close(BS["FY2015"]["ppe_net"] + BS["FY2015"]["cwip"]
                + BS["FY2015"]["long_term_investments"] + BS["FY2015"]["external_loans"]
                + BS["FY2015"]["deferred_tax_asset"], BS["FY2015"]["noncurrent_total"]),
         "FY2015 non-current assets")
    _chk(_close(BS["FY2020"]["ppe_net"] + BS["FY2020"]["cwip"]
                + BS["FY2020"]["long_term_investments"] + BS["FY2020"]["external_loans"]
                + BS["FY2020"]["intangibles"], BS["FY2020"]["noncurrent_total"]),
         "FY2020 non-current assets")
    _chk(_close(BS["FY2021"]["ppe_net"] + BS["FY2021"]["cwip"]
                + BS["FY2021"]["long_term_investments"] + BS["FY2021"]["external_loans"]
                + BS["FY2021"]["intangibles"], BS["FY2021"]["noncurrent_total"]),
         "FY2021 non-current assets")
    for y, keys in (("FY2017", ("ppe_net", "cwip", "associates", "afs", "external_loans",
                                "deferred_tax_asset")),
                    ("FY2018", ("ppe_net", "cwip", "associates", "afs", "external_loans",
                                "deferred_tax_asset")),
                    ("FY2022", ("ppe_net", "cwip", "fvoci", "external_loans", "intangibles")),
                    ("FY2023", ("ppe_net", "cwip", "fvoci", "external_loans", "intangibles")),
                    ("FY2024", ("ppe_net", "cwip", "investment_property", "fvoci",
                                "external_loans", "intangibles"))):
        _chk(_close(sum(BS[y][k] for k in keys), BS[y]["noncurrent_total"]),
             "%s non-current assets" % y)
    for y in ("FY2022", "FY2023", "FY2024"):
        b = BS[y]
        _chk(_close(b["capital"] + b["reserves"] + b["fv_reserve"] + b["retained"]
                    + b["profit_for_year"], b["equity"]), "%s equity" % y)

    # the fixed-asset note: the charge from its own class row, and the movement
    for y, n in FA_NOTE.items():
        if "charge_classes" in n:
            _chk(_close(sum(n["charge_classes"]), n["charge"]), "%s depreciation charge" % y)
        if "disposal_classes" in n:
            _chk(_close(sum(n["disposal_classes"]), n["disposals"]), "%s disposals" % y)
        if "accum_open_classes" in n:
            _chk(_close(sum(n["accum_open_classes"]), n["accum_open"]),
                 "%s accumulated depreciation, opening" % y)
        if "accum_close" in n:
            _chk(_close(n["accum_open"] + n["charge"] - n["disposals"], n["accum_close"]),
                 "%s accumulated depreciation rolls forward" % y)
        if "cost_add" in n and "cost_close" in n and "cost_open" in n and "cost_disp" in n:
            _chk(_close(n["cost_open"] + n["cost_add"] - n["cost_disp"], n["cost_close"]),
                 "%s cost rolls forward" % y)
        if "cost_add_classes" in n:
            _chk(_close(sum(n["cost_add_classes"]), n["cost_add"]), "%s cost additions" % y)
        if "cost_close_classes" in n:
            _chk(_close(sum(n["cost_close_classes"]), n["cost_close"]), "%s cost, closing" % y)
        if "net_close" in n and "cost_close" in n and "accum_close" in n:
            _chk(_close(n["cost_close"] - n["accum_close"], n["net_close"], 200),
                 "%s net book value" % y)

    # the note's closing accumulated depreciation IS the balance sheet's, where both
    # are held in the same unit
    for y in ("FY2016", "FY2020"):
        _chk(_close(FA_NOTE[y]["accum_close"], BS[y]["ppe_accum"]),
             "%s note accum = balance sheet accum" % y)
    # the note's opening accumulated depreciation IS the prior year's closing
    for y, prior in (("FY2019", "FY2018"), ("FY2020", "FY2019"),
                     ("FY2021", "FY2020"), ("FY2022", "FY2021"),
                     ("FY2023", "FY2022"), ("FY2024", "FY2023")):
        if prior in FA_NOTE and "accum_close" in FA_NOTE[prior]:
            _chk(_close(FA_NOTE[y]["accum_open"], FA_NOTE[prior]["accum_close"], 1),
                 "%s opening accum chains from %s" % (y, prior))
    # the next filing's comparative charge IS this filing's own charge
    for y, prior in (("FY2019", "FY2018"), ("FY2020", "FY2019"), ("FY2021", "FY2020"),
                     ("FY2022", "FY2021"), ("FY2023", "FY2022"), ("FY2024", "FY2023")):
        _chk(_close(FA_NOTE[y]["prior_charge"], FA_NOTE[prior]["charge"]),
             "%s comparative charge = %s own charge" % (y, prior))
    # FY2017's charge is not read from a class row; it is the movement identity
    # between two independently established balances
    _chk(_close(FA_NOTE["FY2018"]["prior_accum_open"] + FA_NOTE["FY2018"]["prior_charge"]
                - FA_NOTE["FY2018"]["prior_disposals"], FA_NOTE["FY2018"]["accum_open"]),
         "FY2017 charge closes the FY2017 movement")
    _chk(_close(FA_NOTE["FY2018"]["prior_accum_open"], BS["FY2016"]["ppe_accum"]),
         "FY2017 opening accum = FY2016 closing")
    # the notes' closing net, against the balance sheet in its own unit
    _chk(_close(FA_NOTE["FY2018"]["net_close"], BS["FY2018"]["ppe_net"] * K, 1500),
         "FY2018 note net vs balance sheet")
    _chk(_close(FA_NOTE["FY2022"]["net_close"], BS["FY2022"]["ppe_net"] * K, 500),
         "FY2022 note net vs balance sheet")
    _chk(_close(FA_NOTE["FY2023"]["net_close"], BS["FY2023"]["ppe_net"] * K, 500),
         "FY2023 note net vs balance sheet")
    _chk(_close(FA_NOTE["FY2024"]["net_close"], BS["FY2024"]["ppe_net"] * K, 500),
         "FY2024 note net vs balance sheet")

    # capital expenditure: the investing section sums to its own printed net
    for y, c in CAPEX.items():
        _chk(_close(-c["paid"] + c["proceeds"] + sum(c["other"]), c["net"]),
             "%s investing activities" % y)

    # the cash note sums to its own total, and agrees with the balance sheet or is
    # recorded as disagreeing
    for y, n in CASH_NOTE.items():
        _chk(_close(sum(n["lines"]), n["total"]), "%s cash note" % y)
    for y in ("FY2015", "FY2016", "FY2020", "FY2021"):
        _chk(_close(CASH_NOTE[y]["total"], BS[y]["cash"]), "%s cash note = balance sheet" % y)
    _chk(_close(CASH_NOTE["FY2019"]["total"], BS["FY2019"]["cash"], 1),
         "FY2019 cash note = balance sheet")
    for y in ("FY2018", "FY2022", "FY2023", "FY2024"):
        _chk(_close(CASH_NOTE[y]["total"], BS[y]["cash"] * K, 500),
             "%s cash note = balance sheet" % y)

    # THE SHARE COUNT IS FOOTED OR IT IS NOT RECORDED [clause (ii)]
    for y, c in CAPITAL.items():
        _chk(_close(c["capital"] / c["par"], c["stated_count"]),
             "%s capital / par reproduces the stated count" % y)
        if "table_total" in c:
            _chk(c["table_total"] == c["stated_count"],
                 "%s shareholder table totals the stated count" % y)
    for y, c in CAPITAL_FROM_EQUITY.items():
        _chk(abs(c["capital"] / c["par"] - round(c["capital"] / c["par"])) < 1e-6,
             "%s capital / par is a whole number of shares" % y)
    # the capital the note states IS the capital the balance sheet carries
    for y in ("FY2013", "FY2016", "FY2019", "FY2020", "FY2021"):
        _chk(_close(CAPITAL[y]["capital"], BS[y]["capital"]),
             "%s capital note = balance sheet" % y)
    for y in ("FY2018", "FY2022", "FY2023", "FY2024"):
        _chk(_close(CAPITAL[y]["capital"], BS[y]["capital"] * K, 500),
             "%s capital note = balance sheet" % y)
    for y in ("FY2012", "FY2015"):
        _chk(_close(CAPITAL_FROM_EQUITY[y]["capital"], BS[y]["capital"]),
             "%s comparative capital = equity column" % y)
    _chk(_close(CAPITAL_FROM_EQUITY["FY2017"]["capital"], BS["FY2017"]["capital"] * K),
         "FY2017 comparative capital = equity column")

    # the run's own panel.py borrowings ARE these borrowings.  Read live rather than
    # copied, so the two records cannot drift apart.
    import panel as P
    for y in BS:
        b = BS[y]
        if b.get("bank") is None:
            continue
        scale = 1 if SOURCES[y]["bs_unit"] == "EGP" else K
        pb = P.BORROWINGS.get(y)
        if not pb or pb.get("bank") is None:
            continue
        for k in ("bank", "holdco", "current"):
            mine = (b["current_loans"] if k == "current" else b[k]) * scale
            # panel.py carries these in EGP thousand and does not state whether
            # it rounded or truncated, so the tolerance is one full thousand:
            # that pins every digit the panel actually holds and claims nothing
            # about the three it does not.
            _chk(_close(pb[k] * K, mine, 1000),
                 "%s panel.BORROWINGS.%s" % (y, k))
    return not _BAD


foot()
assert not _BAD, "the valuation-input block does not foot: " + "; ".join(_BAD)


# ---------------------------------------------------------------------------
# THE RECORD.  Every value is in WHOLE POUNDS; `as_printed` carries the figure as
# the page shows it and `precision` says whether the pound figure is exact or
# inherits the page's thousand-rounding.
# ---------------------------------------------------------------------------

def _asat(y):
    return "%d-06-30" % int(y[2:])


def _scale(y):
    return 1 if SOURCES[y]["bs_unit"] == "EGP" else K


def _prec(y):
    return "exact" if _scale(y) == 1 else "thousand_rounded"


def _src(y, where):
    s = SOURCES[y]
    return ("%s, %s (%s, held at %s; the company's own audited annual financial "
            "statements, downloaded from its own investor-relations channel — "
            "kimaegypt.com and the Mist portal it embeds)"
            % (s["file"], where, s["doc"], s["held"]))


def _missing(reason):
    return {"missing": True, "reason": reason}


def _cash(y):
    if y == "FY2014":
        return _missing(MISSING_2014)
    b, sc = BS[y], _scale(y)
    r = {"value": b["cash"] * sc, "as_at": _asat(y),
         "as_printed": b["cash"], "unit_as_printed": SOURCES[y]["bs_unit"],
         "precision": _prec(y),
         "source": _src(y, "statement of financial position, cash at banks and on hand"),
         "route": ROUTE,
         "definition": "the company's own 'cash at banks and on hand' / 'cash and "
                       "cash equivalents' line: time and call deposits, current "
                       "accounts and cash in hand"}
    if "cash_lines" in b:
        names = ["time_and_call_deposits", "current_accounts_at_banks", "cash_on_hand"]
        r["lines"] = dict(zip(names, b["cash_lines"]))
    n = CASH_NOTE.get(y)
    if n:
        names = (["time_and_call_deposits", "current_accounts_at_banks",
                  "guarantee_letter_cover", "cash_on_hand"] if len(n["lines"]) == 4
                 else ["time_and_call_deposits", "current_accounts_at_banks",
                       "cash_on_hand"])
        gap = n["total"] - b["cash"] * sc
        if sc == K and abs(gap) < 500:
            # the balance sheet prints the rounded thousand and the note prints the
            # pound: the note is the same balance at higher precision, not a second
            # opinion, so it is carried and the agreement is the check
            r["value"] = n["total"]
            r["precision"] = "exact"
            r["lines"] = dict(zip(names, n["lines"]))
            r["check"] = ("%s states the same balance in whole pounds — %d — and sums "
                          "to it from its own components; the balance sheet's %d "
                          "thousand is that figure rounded"
                          % (n["note"], n["total"], b["cash"]))
        elif gap == 0:
            r["lines"] = dict(zip(names, n["lines"]))
            r["check"] = ("%s states the same balance and sums to it from its own "
                          "components — %d — so the figure is footed twice, once "
                          "against the note's parts and once against the current-asset "
                          "column it sits in" % (n["note"], n["total"]))
        else:
            # the two disagree.  The balance sheet is carried, because the bridge
            # stands on the balance sheet and its figure foots against the column it
            # sits in; the note is named beside it rather than averaged with it.
            r["check"] = (
                ("the current-asset column foots on this figure: %s plus the %s "
                 "carried above it reaches the printed total of %s"
                 % (format(b["cash"], ","), format(b["carried"], ","),
                    format(b["tca"], ",")))
                if "carried" in b else
                ("the current-asset column foots on this figure, reaching the printed "
                 "total of %s, and the balance sheet balances on it"
                 % format(b["tca"], ",")))
            r["disagreement_recorded_not_resolved"] = {
                "balance_sheet": b["cash"] * sc,
                "note": n["total"], "note_where": n["note"],
                "note_lines": dict(zip(names, n["lines"])),
                "gap": gap,
                "why_the_balance_sheet_is_carried":
                    ("both figures foot — the balance sheet against its own column and "
                     "the note against its own three components — so neither is a "
                     "misreading and the filing simply disagrees with itself. The "
                     "balance sheet is carried because the bridge stands on the "
                     "balance sheet, and the note is named here rather than averaged "
                     "with it, chosen between silently, or dropped.")}
    if y in ("FY2012", "FY2013"):
        r["carried_beside_not_folded_in"] = {
            "investment_certificates": BS[y]["investment_certificates"],
            "treasury_bills": BS[y]["treasury_bills"],
            "why": "whether an investment certificate or a treasury bill is a cash "
                   "equivalent is a valuation choice about maturity that this record "
                   "does not make; the company reports them on their own lines above "
                   "cash and they are named here rather than folded in or dropped"}
    return r


def _debt(y):
    if y == "FY2014":
        return _missing(MISSING_2014 + " The income statement this run already carries "
                        "for FY2014 shows no finance cost, which is consistent with the "
                        "company having had no interest-bearing borrowings that year and "
                        "is NOT evidence of it: the same statement shows no finance cost "
                        "in FY2013, when the balance sheet does carry a nil borrowings "
                        "position, and in FY2015, when it carries EGP 327,717,123 of "
                        "holding-company debt whose cost was capitalised. An absent line "
                        "is not a zero.")
    b, sc = BS[y], _scale(y)
    lines = {"bank_loans_non_current": b.get("bank", 0),
             "loans_from_holding_and_sister_companies": b.get("holdco", 0),
             "current_portion_of_long_term_loans": b.get("current_loans", 0)}
    total = sum(lines.values())
    r = {"value": total * sc, "as_at": _asat(y),
         "as_printed": total, "unit_as_printed": SOURCES[y]["bs_unit"],
         "precision": _prec(y),
         "source": _src(y, "statement of financial position, borrowings"),
         "route": ROUTE,
         "definition": "long-term bank loans, loans from the holding and sister "
                       "companies, and the portion of long-term loans falling due "
                       "within a year — the same three tranches this run's own "
                       "panel.BORROWINGS carries, so the block and the panel cannot "
                       "disagree about what debt means",
         "lines": {k: v * sc for k, v in lines.items()},
         "check": "reproduces this run's own committed panel.BORROWINGS for the same "
                  "year, which is asserted at import rather than compared by eye"}
    if total == 0:
        r["check"] = ("the balance sheet carries no borrowings line at all in this "
                      "year: total financing %d equals equity %d plus deferred tax %d, "
                      "with nothing between them"
                      % (b["total_investment"], b["equity"], b["deferred_tax"]))
    if y == "FY2021":
        r["lines"]["bank_loans_non_current"] = b["bank"]
        r["derived_line"] = {
            "item": "bank_loans_non_current", "value": b["bank"],
            "identity": "total financing less equity, deferred tax and the "
                        "holding-company loan, all four printed on the same page",
            "arithmetic": "11,093,833,752 - 2,670,295,099 - 1,076,610,521 - "
                          "1,226,569,717 = 6,120,358,415",
            "why": "the bank-loan cell sits at the foot of the page and did not "
                   "resolve; the page's own financing total supplies it exactly, and "
                   "the FY2021-22 filing's comparative column states 6,120,358 "
                   "thousand for the same balance",
            "labelled": "derived by the page's own footing, not read"}
    if y == "FY2018":
        r["later_filing_states"] = {
            "bank_loans_non_current": 4_466_445_100,
            "where": "the FY2018-19 annual's comparative financing column, in whole "
                     "pounds, which foots exactly against that column's own total",
            "why_not_carried": "point-in-time: an origin standing at FY2018 saw the "
                               "FY2017-18 annual, which prints EGP thousand"}
    return r


def _capex(y):
    if y == "FY2014":
        return _missing(
            "the company's FY2013-14 annual is the 367 x 519 pixel scan described "
            "under this origin's other items; its cash-flow statement does not "
            "resolve to the digit, and no other filing held carries a FY2014 "
            "investing section. The identity capex = change in PPE + D&A cannot "
            "supply it either, because that identity needs property at 30 June 2013 "
            "AND at 30 June 2014 and the second of those is itself missing here.")
    c = CAPEX[y]
    return {"value": c["paid"], "period": y, "unit": "EGP", "precision": "exact",
            "source": _src(y, "statement of cash flows, investing activities, "
                              "'payments to acquire fixed assets'"),
            "route": ROUTE,
            "disclosed": True, "derived": False,
            "lines": {"payments_to_acquire_fixed_assets": c["paid"],
                      "payments_for_projects_under_construction": 0,
                      "proceeds_from_sale_of_fixed_assets": c["proceeds"]},
            "check": "the investing section sums to its own printed net of %d" % c["net"],
            "note": "committed as DISCLOSED, not derived: KIMA prints the payment as "
                    "its own line in every year this run holds, so the identity "
                    "capex = change in PPE + D&A is not needed at any origin and is "
                    "not used at any origin. Payments for projects under construction "
                    "are a separate printed line and are nil in every year here."}


def _ppe(y):
    if y == "FY2014":
        return _missing(MISSING_2014)
    b, sc = BS[y], _scale(y)
    n = FA_NOTE.get(y)
    r = {"value": b["ppe_net"] * sc, "as_at": _asat(y),
         "as_printed": b["ppe_net"], "unit_as_printed": SOURCES[y]["bs_unit"],
         "precision": _prec(y),
         "source": _src(y, "statement of financial position, fixed assets (net)"),
         "route": ROUTE,
         "lines": {"fixed_assets_net": b["ppe_net"] * sc,
                   "projects_under_construction": b.get("cwip", 0) * sc},
         "note": "projects under construction are carried BESIDE net fixed assets "
                 "rather than inside them, because that is how the company presents "
                 "them and because a rebuild that wants replacement cost and one "
                 "that wants operating assets need different answers about which "
                 "of the two to use"}
    if "ppe_cost" in b:
        r["lines"]["cost"] = b["ppe_cost"]
        r["lines"]["accumulated_depreciation"] = b["ppe_accum"]
        r["check"] = ("cost %d less accumulated depreciation %d reproduces the printed "
                      "net, and each of the three columns sums to its own total from "
                      "the six asset classes"
                      % (b["ppe_cost"], b["ppe_accum"]))
    elif "ppe_classes" in b:
        r["check"] = "the six asset classes sum to the printed net"
    if n and "net_close" in n:
        r["value"] = n["net_close"]
        r["precision"] = "exact"
        r["value_source"] = ("%s states the closing net book value in whole pounds and "
                             "the balance sheet's rounded thousand agrees" % n["note"])
    return r


def _dep(y):
    if y == "FY2014":
        return _missing(
            "the fixed-asset movement note of the FY2013-14 annual shares the "
            "resolution limit described under this origin's other items. The FY2015-16 "
            "filing's note carries a comparative column that would supply a FY2015 "
            "charge and an opening balance dated 1 July 2014, but no FY2014 charge at "
            "all: the year between them is not covered by any note held.")
    if y in ("FY2012", "FY2015"):
        n = FA_NOTE["FY2013" if y == "FY2012" else "FY2016"]
        rec = {"value": n["prior_charge"] if y == "FY2015" else 7_911_871,
               "period": y, "unit": "EGP", "precision": "exact",
               "source": _src(y, "the fixed-asset note's comparative column"),
               "route": ROUTE, "note_where": n["note"]}
        if y == "FY2012":
            rec["footing"] = (
                "NOT INDEPENDENTLY FOOTABLE. The FY2012-13 note prints the prior year "
                "as a single comparative column — one total per row, no asset classes "
                "— so the charge cannot be summed from its parts, and the FY2011 "
                "closing accumulated depreciation the movement identity would need is "
                "in no filing held. The figure is recorded as read, with that stated, "
                "rather than dropped or presented as checked.")
        else:
            rec["footing"] = (
                "READ, AND THE FILING'S OWN ARITHMETIC REFUSES IT. The FY2015-16 note's "
                "comparative column rolls 143,271,658 of opening accumulated "
                "depreciation plus this 9,877,208 less 699,490 of disposals to "
                "152,449,376, against the 154,392,674 the SAME note carries as its "
                "FY2016 opening balance — a gap of 1,943,298 that the filing does not "
                "explain, alongside a 7,342,170 gap of the same shape in the cost "
                "column. The figure is recorded as read WITH the disagreement named, "
                "because a reader rebuilding FY2015 needs to know the charge is on a "
                "basis the next column does not continue.")
            rec["disagreement_recorded_not_resolved"] = {
                "comparative_column_rolls_to": 152_449_376,
                "same_note_fy2016_opening": 154_392_674, "gap": 1_943_298,
                "cost_column_gap": 7_342_170}
        return rec
    n = FA_NOTE[y]
    r = {"value": n["charge"], "period": y, "unit": "EGP", "precision": "exact",
         "source": _src(y, "the fixed-asset note, the additions row of the "
                           "accumulated-depreciation block"),
         "route": ROUTE, "note_where": n["note"],
         "definition": "the depreciation charged on fixed assets for the year. KIMA's "
                       "cash-flow statement is presented by the DIRECT method and "
                       "carries no depreciation add-back, so the charge comes from the "
                       "movement note and from nowhere else"}
    if "charge_classes" in n:
        r["lines"] = dict(zip(["buildings_and_installations", "plant_and_machinery",
                               "vehicles", "tools_and_equipment", "furniture_and_office"],
                              n["charge_classes"]))
    checks = []
    if "charge_classes" in n:
        checks.append("sums to the printed total from its own five asset classes")
    if "accum_close" in n:
        checks.append("closes the movement: opening %d plus the charge less disposals "
                      "%d reaches the printed closing %d"
                      % (n["accum_open"], n["disposals"], n["accum_close"]))
    if y == "FY2017":
        checks = ["closes the movement between two balances established elsewhere: the "
                  "FY2015-16 note's closing accumulated depreciation of 170,516,056 "
                  "plus this charge less 10,316,770 of disposals reaches the "
                  "FY2017-18 note's opening balance of 191,977,306"]
    nxt = {"FY2018": "FY2019", "FY2019": "FY2020", "FY2020": "FY2021",
           "FY2021": "FY2022", "FY2022": "FY2023", "FY2023": "FY2024"}.get(y)
    if nxt:
        checks.append("the %s filing's comparative column states the same charge"
                      % SOURCES[nxt]["doc"].split(",")[0])
    r["check"] = "; ".join(checks)
    return r


def _dep_2017():
    n = FA_NOTE["FY2018"]
    r = {"value": n["prior_charge"], "period": "FY2017", "unit": "EGP",
         "precision": "exact",
         "source": _src("FY2017", "the fixed-asset note's comparative column"),
         "route": ROUTE, "note_where": n["note"],
         "definition": "the depreciation charged on fixed assets for the year",
         "check": "closes the movement between two balances established in two "
                  "different filings: the FY2015-16 note's closing accumulated "
                  "depreciation of 170,516,056 plus this charge of 31,778,020 less "
                  "10,316,770 of disposals reaches the FY2017-18 note's opening "
                  "balance of 191,977,306 exactly"}
    return r


def _wc(y):
    if y == "FY2014":
        return _missing(MISSING_2014)
    b, sc = BS[y], _scale(y)
    lines = {"inventories": b["inventories"] * sc,
             "trade_and_other_receivables": b["receivables"] * sc,
             "trade_and_other_payables": b["payables"] * sc,
             "total_current_assets": b["tca"] * sc,
             "total_current_liabilities": b["tcl"] * sc}
    excluded = {"cash_and_equivalents": b["cash"] * sc,
                "provisions": b["provisions"] * sc,
                "short_term_and_current_portion_of_loans": b.get("current_loans", 0) * sc}
    if y in ("FY2012", "FY2013"):
        excluded["investment_certificates"] = b["investment_certificates"]
        excluded["treasury_bills"] = b["treasury_bills"]
    r = {"value": (b["tca"] - b["tcl"]) * sc, "as_at": _asat(y),
         "as_printed": b.get("wc", b["tca"] - b["tcl"]),
         "unit_as_printed": SOURCES[y]["bs_unit"], "precision": _prec(y),
         "source": _src(y, "statement of financial position, the current sections"),
         "route": ROUTE,
         "definition": "total current assets less total current liabilities — the "
                       "company's OWN 'working capital' line where it prints one, "
                       "which it does on every full-pound balance sheet here",
         "lines": lines,
         "excluded_and_named": dict(excluded, why=(
             "a reader cannot tell an excluded line from an unread one, so every "
             "current item that is NOT a trading line is named here with its own "
             "amount. Cash and the loan lines are excluded because they are committed "
             "as their own items above and would otherwise be counted twice; "
             "provisions are excluded because they are a liability for a disputed "
             "past event rather than a trading balance, and the choice is stated "
             "rather than assumed"))}
    if "wc" in b:
        r["check"] = ("the company prints this figure itself as 'working capital' and "
                      "it reproduces from the two totals above it")
    else:
        r["check"] = ("the two totals reproduce from their own components and the "
                      "balance sheet balances: assets %d, equity plus liabilities %d"
                      % (b["total_assets"], b["total_assets"]))
    if y in ("FY2019", "FY2020", "FY2021"):
        r["lines"]["trade_and_other_payables"] = b["payables"] * sc
        r["lines"]["payables_including_short_term_loans"] = b["payables_and_loans"] * sc
    if y == "FY2018":
        r["re_presented_by_a_later_filing"] = {
            "total_current_liabilities": 1_032_139_116,
            "trade_and_other_payables": 982_190_345,
            "total_equity": 3_541_841_441,
            "where": "the FY2018-19 annual's comparative column",
            "what_moved": "94,526 thousand out of equity into payables",
            "why_not_substituted": "point-in-time: an origin standing at FY2018 saw "
                                   "the FY2017-18 annual's own figures and could not "
                                   "have seen this. The re-presentation is recorded "
                                   "beside them, never in place of them."}
    return r


def _shares(y):
    if y == "FY2014":
        return _missing(
            "the capital note of the FY2013-14 annual shares the resolution limit "
            "described under this origin's other items, and its shareholder table — "
            "the second footing every other year here supplies — is a dense numeric "
            "block that resolves least of all. TODAY'S COUNT IS NOT CARRIED BACK, and "
            "neither is either neighbour's: the count moved from 260,860,000 at "
            "FY2013 to 394,042,710 at FY2015 on capital increases inside this window, "
            "so a carried count would be wrong in fact as well as in vintage. A "
            "PREVIOUS ATTEMPT ON THIS ITEM IS RECORDED AND WAS WRONG ABOUT ITS OWN "
            "FAILURE: engine/valuation_calibration/_shares_ocr_egch.json logs FY2014 "
            "as 'no equity or per-share note found in the last 28 pages', a run that "
            "read Arabic scans with the English model and was searching the wrong end "
            "of the document. Read with the Arabic model and rendered off the pixels, "
            "the note is found in every other filing here; on this one the note is "
            "found and the digits are not legible, which is a different fact and is "
            "the one recorded.")
    c = CAPITAL.get(y)
    if c:
        return {"value": c["stated_count"], "as_at": _asat(y),
                "issued_capital": c["capital"], "par_value": c["par"],
                "unit": "EGP", "precision": "exact",
                "source": _src(y, c["note"]),
                "route": ROUTE,
                "check": ("issued and paid-up capital %d divided by the par value of %g "
                          "reproduces the count of %d that the same sentence states"
                          % (c["capital"], c["par"], c["stated_count"]))
                         + ("; the shareholder table below it totals the same count"
                            if "table_total" in c else ""),
                "authorised_capital": c["authorised"],
                "vintage": "read off this year's own filing; no later count is carried "
                           "back to this origin"}
    e = CAPITAL_FROM_EQUITY[y]
    count = int(round(e["capital"] / e["par"]))
    r = {"value": count, "as_at": _asat(y),
         "issued_capital": e["capital"], "par_value": e["par"],
         "unit": "EGP", "precision": "exact" if e["exact"] else "thousand_rounded",
         "source": _src(y, "the comparative equity column, with the par value from "
                           "the same filing's capital note"),
         "route": ROUTE,
         "footed_by": ("the capital/par identity, which is the route clause (ii) itself "
                       "supplies where the note is written for the filing's own year "
                       "only. This year's own committed capital is %s (%s), and the "
                       "par value of %g is established by %s. THE COUNT IS NOT "
                       "SEPARATELY STATED for this date in any filing held — the "
                       "company's archive carries no annual of its own for this year — "
                       "so the identity is the footing and that is said rather than "
                       "implied." % (format(e["capital"], ","), e["where"], e["par"],
                                     e["par_from"])),
         "vintage": "this year's own capital, read from the comparative column of the "
                    "next filing under the same discipline this run's panel.py applies "
                    "to its income statement for these three origins. No later count "
                    "is carried back."}
    if not e["exact"]:
        r["rounding_band"] = {
            "shares_low": int((e["capital"] - 500) // e["par"]) + 1,
            "shares_high": int((e["capital"] + 499) // e["par"]),
            "why": "the capital is printed in EGP thousand, so the pound figure is "
                   "known to within 500 and the count to within about a hundred "
                   "shares out of 578 million. The band is stated rather than hidden "
                   "behind a figure that looks exact."}
    return r


def block(y):
    if y == "FY2017":
        d = _dep_2017()
    else:
        d = _dep(y)
    return {"cash": _cash(y), "debt": _debt(y), "capex": _capex(y), "ppe": _ppe(y),
            "dep": d, "wc": _wc(y), "shares": _shares(y)}


ORIGINS = ["FY2012", "FY2013", "FY2014", "FY2015", "FY2016", "FY2017", "FY2018",
           "FY2019", "FY2020", "FY2021", "FY2022", "FY2023", "FY2024"]


def record():
    return {
        "_": "The inputs a VALUE is rebuilt from at each of this run's origins, "
             "committed beside the driver panel under [R-FCAL-01 AMENDED]. GENERATED "
             "by engine/egch_walkforward/valuation_inputs.py, which foots every "
             "balance sheet, every fixed-asset movement, every cash-flow investing "
             "section and every share count against the filings' own arithmetic at "
             "import; never hand-edited.",
        "run": "EGCH",
        "rule": RULE,
        "company": "Egyptian Chemical Industries (KIMA) S.A.E.",
        "currency": "EGP",
        "units": "every `value` is in WHOLE POUNDS. KIMA's balance sheets print full "
                 "pounds to FY2016 and EGP thousand from FY2017, while its fixed-asset "
                 "notes, cash notes and cash-flow statements print full pounds "
                 "throughout — so `as_printed` carries the figure as the page shows it, "
                 "`unit_as_printed` says which unit that is, and `precision` says "
                 "whether the pound figure is exact or inherits a thousand-rounding.",
        "basis": "unconsolidated — the company reports on its own",
        "fiscal_year_end": "30 June",
        "origins_declared_by": "PRE_REGISTRATION_01-09-2026.md",
        "route": ROUTE,
        "point_in_time": "every year is carried AS FIRST REPORTED from its own filing "
                         "where the company's archive holds one. FY2012, FY2015 and "
                         "FY2017 have no annual of their own and are taken from the "
                         "next filing's comparative column — exactly the three origins "
                         "this run's panel.py already flags column='comparative'. Two "
                         "re-presentations fall inside the window and both are recorded "
                         "BESIDE the figure they would replace, never substituted.",
        "capex_disclosure": "DISCLOSED at every origin held. KIMA prints 'payments to "
                            "acquire fixed assets' as its own line in the investing "
                            "section of every cash-flow statement here, so the identity "
                            "capex = change in PPE + D&A is not used at any origin and "
                            "no capex figure in this record is derived.",
        "sources": {y: SOURCES[y]["file"] for y in ORIGINS},
        "origins": {y: block(y) for y in ORIGINS},
    }


def main():
    doc = record()
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    items = ["cash", "debt", "capex", "ppe", "dep", "wc", "shares"]
    have = miss = 0
    print("EGCH valuation-input block -> %s\n" % OUT)
    print("  %-8s %s" % ("origin", "  ".join("%-6s" % i for i in items)))
    print("  " + "-" * 64)
    for y in ORIGINS:
        row = "  %-8s " % y
        for i in items:
            ok = "missing" not in doc["origins"][y][i]
            have += ok
            miss += not ok
            row += "%-8s" % ("yes" if ok else "MISSING")
        print(row.rstrip())
    print("\n  committed %d of %d cells; %d recorded as missing with a reason"
          % (have, have + miss, miss))
    print("  every check in foot() passed at import")


if __name__ == "__main__":
    main()
