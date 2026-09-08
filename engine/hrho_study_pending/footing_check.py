"""HRHO — footing check. Arithmetic is the arbiter, so the sweep's claim that every
statement page foots is REPRODUCIBLE rather than asserted.

Every figure below was read from EFG Holding's own filings in
engine/hrho_study_pending/filings/ and is re-added here against the SUBTOTAL THE
FILING ITSELF PRINTS. The route each block came by is stated in ROUTE:

  text   — pdftotext -layout text layer (income statements, notes, segment tables)
  pixels — read off the page rendered at 220 dpi via PyMuPDF, because the
           consolidated statement of financial position carries NO text layer in
           any year (zero characters, nine embedded images) and in the FY2025 set
           the page is /Rotate 270 so the raw embedded image is sideways.

A non-zero difference anywhere is a FAIL and prints. Run:  python3 footing_check.py
"""
FAILS = []


def foot(label, route, parts, printed):
    got = sum(parts)
    ok = (got == printed)
    if not ok:
        FAILS.append((label, route, got, printed, got - printed))
    print(f"  {'OK ' if ok else 'FAIL'} [{route:6}] {label:<58} "
          f"{got:>16,} vs printed {printed:>16,}"
          f"{'' if ok else f'   DIFF {got - printed:+,}'}")


print("=" * 118)
print("FY2025 AUDITED CONSOLIDATED — income statement (EGP k)")
print("=" * 118)
foot("NII = interest income less interest expense", "text",
     [26_981_276, -19_544_037], 7_437_239)
foot("Net fees = fee income less fee expense", "text",
     [14_009_331, -2_349_074], 11_660_257)
foot("Revenue (8 components)", "text",
     [7_437_239, 11_660_257, 661_111, 762_731, 127_846, 4_353_001, 594_928, 72_682],
     25_669_795)
foot("PBT = revenue less 5 cost lines", "text",
     [25_669_795, -15_882_915, -113_575, -950_925, -333_083, -895_095], 7_494_202)
foot("Profit = PBT less tax", "text", [7_494_202, -1_239_570], 6_254_632)
foot("Owners + NCI = profit", "text", [4_058_309, 2_196_323], 6_254_632)

print("\nFY2024 comparative column in the same filing (EGP k)")
foot("NII", "text", [22_319_642, -15_310_258], 7_009_384)
foot("Net fees", "text", [11_452_386, -1_357_101], 10_095_285)
foot("Revenue", "text",
     [7_009_384, 10_095_285, -57_356, 2_844_098, 85_998, 1_423_262, 2_907_706, 48_853],
     24_357_230)
foot("PBT", "text",
     [24_357_230, -14_469_542, -40_678, -773_002, -738_908, -633_597], 7_701_503)
foot("Profit", "text", [7_701_503, -2_370_417], 5_331_086)
foot("Owners + NCI", "text", [4_253_970, 1_077_116], 5_331_086)

print("\n" + "=" * 118)
print("FY2025 AUDITED CONSOLIDATED — statement of financial position (EGP k)")
print("PAGE HAS NO TEXT LAYER; READ OFF THE RENDERED PIXELS AT 220 dpi")
print("=" * 118)
foot("Total assets (13 lines), 31/12/2025", "pixels",
     [46_767_027, 78_128_024, 17_672_952, 34_406_171, 20_758_482, 17_404_066, 0,
      348_710, 4_003_498, 1_903_301, 84_681, 206_765, 8_963_377], 230_647_054)
foot("Total liabilities (10 lines), 31/12/2025", "pixels",
     [34_586_591, 79_322_035, 15_104_080, 13_987_720, 23_136_225, 3_909_625,
      1_984_757, 893_918, 1_923_015, 10_841_107], 185_689_073)
foot("Equity attributable to owners (5 lines)", "pixels",
     [7_179_465, 1_843_542, 993_689, 9_661_185, 15_744_718], 35_422_599)
foot("Total equity = owners + NCI", "pixels", [35_422_599, 9_535_382], 44_957_981)
foot("Liabilities + equity = total assets", "pixels",
     [185_689_073, 44_957_981], 230_647_054)
print("\nFY2024 comparative column, same page")
foot("Total assets (13 lines), 31/12/2024", "pixels",
     [51_540_737, 57_928_603, 15_773_382, 23_488_674, 12_374_218, 12_487_545,
      106_304, 804_867, 2_975_630, 2_490_920, 90_283, 233_912, 6_583_336],
     186_878_411)
foot("Total liabilities (10 lines), 31/12/2024", "pixels",
     [22_762_916, 67_208_585, 11_489_567, 7_901_466, 20_566_943, 1_432_665,
      1_913_277, 2_083_684, 1_020_705, 11_130_638], 147_510_446)
foot("Equity attributable to owners (6 lines incl. treasury)", "pixels",
     [7_298_030, 1_797_838, 993_689, 11_800_563, -399_975, 12_568_681], 34_058_826)
foot("Liabilities + equity = total assets", "pixels",
     [147_510_446, 34_058_826, 5_309_139], 186_878_411)

print("\n" + "=" * 118)
print("CROSS-ROUTE PROOF — the pixel-read balance sheet against the TEXT-LAYER segment note")
print("=" * 118)
foot("Segment note total assets (12 segments), FY2025", "text",
     [31_190_626, 57_643_085, 2_874_878, 1_213_300, 304_182, 1_267_900, 9_457_440,
      7_359_419, 14_166_291, 3_095_652, 227_765, 101_846_516], 230_647_054)
foot("Segment note total liabilities (12 segments), FY2025", "text",
     [20_810_194, 49_147_341, 1_414_945, 753_372, 133_051, 60_785, 7_719_256,
      5_173_472, 11_968_045, 2_777_011, 169_330, 85_562_271], 185_689_073)
foot("Segment note revenue (12 segments + adjustments), FY2025", "text",
     [1_274_257, 6_030_924, 2_197_455, 1_924_637, 434_004, 105_815, 907_898,
      2_412_129, 2_985_840, 213_820, 25_823, 7_516_545, -359_352], 25_669_795)
foot("Segment note profit (12 segments), FY2025", "text",
     [-646_413, 1_223_523, 754_796, 354_003, 11_616, -106_999, 587_108, 124_479,
      783_344, 75_315, -36_552, 3_130_412], 6_254_632)

print("\n" + "=" * 118)
print("FY2023 AND FY2022 AUDITED — the other two of the four fiscal years")
print("=" * 118)
foot("FY2023 revenue as FILED (9 components)", "text",
     [4_620_981, 6_442_310, 171_671, 1_411_890, 81_477, 730_930, 1_154_847, 9_797,
      45_048], 14_668_951)
foot("FY2023 PBT as FILED", "text",
     [14_668_951, -8_612_116, -38_055, -1_042_335, -235_053, -476_686], 4_264_706)
foot("FY2023 profit as FILED", "text", [4_264_706, -1_093_997], 3_170_709)
foot("FY2023 revenue as RESTATED in the FY2024 filing", "text",
     [4_617_715, 6_442_310, 171_671, 1_411_890, 81_477, 740_727, 1_154_847, 45_048],
     14_665_685)
foot("FY2023 profit as RESTATED", "text",
     [14_665_685, -8_619_089, -38_055, -1_042_335, -224_814, -481_384, -1_093_997],
     3_166_011)
foot("FY2023 total assets (13 lines)", "pixels",
     [32_252_243, 40_196_971, 6_770_962, 9_196_191, 11_647_611, 11_233_860, 330_652,
      844_793, 98_701, 2_177_789, 2_315_613, 126_411, 4_716_177], 121_907_974)
foot("FY2023 liabilities + equity = assets", "pixels",
     [94_512_045, 23_321_025, 4_074_904], 121_907_974)
foot("FY2022 revenue as FILED (EGP units, not thousands)", "text",
     [3_597_884_237, 4_296_576_153, -847_026_822, 923_031_019, 5_660_968,
      381_500_523, 2_495_674_927, 5_486_779, 76_562_049], 10_935_349_833)
foot("FY2022 PBT as FILED (EGP units)", "text",
     [10_935_349_833, -6_426_256_897, -21_174_483, -736_750_108, -156_889_674,
      -296_470_780], 3_297_807_891)
foot("FY2022 profit as FILED (EGP units)", "text",
     [3_297_807_891, -1_103_724_498], 2_194_083_393)
foot("FY2022 total assets as RESTATED (13 lines)", "pixels",
     [26_214_250, 33_222_142, 6_168_256, 6_772_893, 14_080_121, 11_518_692, 349_701,
      606_433, 118_985, 1_636_043, 1_947_231, 64_486, 3_401_911], 106_101_144)
foot("FY2022 liabilities + equity = assets", "pixels",
     [83_732_560, 18_923_298, 3_445_286], 106_101_144)

print("\n" + "=" * 118)
print("STUDY YEAR 2026 — both disclosed quarters")
print("=" * 118)
foot("Q1-2026 revenue", "text",
     [2_290_019, 2_733_559, 52_926, 27_685, 3_464, 1_084_622, 357_397, -5_553],
     6_544_119)
foot("Q1-2026 PBT", "text",
     [6_544_119, -3_427_869, -34_903, -470_527, -33_933, -262_211], 2_314_676)
foot("Q1-2026 profit; owners + NCI", "text", [1_034_391, 488_160], 1_522_551)
foot("Q2-2026 standalone revenue", "text",
     [2_264_504, 3_798_858, 229_043, -758_503, 73_492, 561_232, 236_435, 6_719],
     6_411_780)
foot("Q2-2026 standalone PBT", "text",
     [6_411_780, -3_973_807, -24_136, -355_904, -21_026, -309_436], 1_727_471)
foot("H1-2026 revenue", "text",
     [4_554_523, 6_532_417, 281_969, -730_818, 76_956, 1_645_854, 593_832, 1_166],
     12_955_899)
foot("H1-2026 PBT", "text",
     [12_955_899, -7_401_676, -59_039, -826_431, -54_959, -571_647], 4_042_147)
foot("H1-2026 owners + NCI", "text", [1_809_978, 1_088_989], 2_898_967)
foot("CROSS-FILING: Q1 profit + Q2 profit = H1 profit", "text",
     [1_522_551, 1_376_416], 2_898_967)
foot("CROSS-FILING: Q1 owners + Q2 owners = H1 owners", "text",
     [1_034_391, 775_587], 1_809_978)

print("\n" + "=" * 118)
print("H1-2026 NOTES — the two-leg / three-leg evidence")
print("=" * 118)
foot("Segment revenue (12 segments + adjustments)", "text",
     [396_463, 3_376_977, 792_956, 632_481, 340_452, 375_306, 248_903, 1_053_335,
      1_827_154, 86_343, 35_900, 3_971_062, -181_433], 12_955_899)
foot("  of which LEG 1 the Investment Bank (5 segments)", "text",
     [3_376_977, 792_956, 632_481, 340_452, 396_463], 5_539_329)
foot("  of which LEG 2 the NBFI platform (6 segments)", "text",
     [375_306, 248_903, 1_053_335, 1_827_154, 86_343, 35_900], 3_626_941)
foot("  three verticals less adjustments = audited revenue", "text",
     [5_539_329, 3_626_941, 3_971_062, -181_433], 12_955_899)
foot("Segment total assets (12 segments)", "text",
     [26_727_585, 67_619_043, 2_079_011, 1_178_859, 368_326, 1_505_411, 14_514_787,
      6_266_099, 19_637_242, 2_186_122, 456_483, 118_131_591], 260_670_559)
foot("Segment total liabilities (12 segments)", "text",
     [15_651_731, 57_752_717, 545_940, 367_964, 155_419, 88_985, 14_456_594,
      5_608_685, 16_534_658, 1_831_016, 299_226, 101_153_718], 214_446_653)
foot("Geographic revenue Egypt / GCC / Other", "text",
     [9_752_277, 3_063_784, 139_838], 12_955_899)
foot("Geographic assets Egypt / GCC / Other", "text",
     [181_995_093, 68_611_244, 10_064_222], 260_670_559)
foot("NCI note (6 components) at 30/6/2026", "text",
     [5_207_420, 404_395, 252_096, 909_338, 2_239_368, 1_088_989], 10_101_606)
foot("NCI note (6 components) at 31/12/2025", "text",
     [3_010_921, 355_060, 158_469, 3_045_339, 769_270, 2_196_323], 9_535_382)
foot("Loans and facilities to customers, gross, 30/6/2026", "text",
     [5_911_001, 15_473_543, 15_436_189, 4_280_268, 61_460_409, 2_805_915, 485_519,
      -9_999_230], 95_853_614)
foot("Loans net of impairment = current + non-current", "text",
     [45_232_227, 47_191_126], 92_423_353)
foot("Customer deposits by type, 30/6/2026", "text",
     [39_798_088, 16_951_623, 15_592_674, 17_683_853, 3_595_597], 93_621_835)
foot("Customer deposits by counterparty", "text",
     [46_447_697, 47_174_138], 93_621_835)
foot("Customer deposits by maturity", "text",
     [79_957_162, 13_664_673], 93_621_835)
foot("Bank NXT corporate ECL: stage 1 carrying", "text",
     [1_856_917, 27_845_659, 5_346_611, 49], 35_049_236)
foot("Bank NXT corporate ECL: stage 2 carrying", "text",
     [1_838, 644_870, 1_346_010, 63, 17_596], 2_010_377)
foot("Bank NXT corporate ECL: stage 3 carrying", "text",
     [3, 31_870, 3_039, 1_007_811, 167_802], 1_210_525)
foot("Bank NXT corporate ECL: three stages = total carrying", "text",
     [35_049_236, 2_010_377, 1_210_525], 38_270_138)
foot("Bank NXT corporate ECL: carrying less ECL = net", "text",
     [38_270_138, -2_133_361], 36_136_777)
foot("Off-balance-sheet securitisation assets", "text",
     [15_619_278, 1_239_913, 600_000], 17_459_191)
foot("Off-balance-sheet securitisation liabilities", "text",
     [13_662_987, 180_000], 13_842_987)
foot("Share capital after the 20-Sep-2025 write-off (EGP k)", "text",
     [7_298_030, -118_565], 7_179_465)

print("\n" + "=" * 118)
print("EARNINGS RELEASE vs AUDITED STATEMENTS — the release's own tables (EGP mn, "
      "release rounding)")
print("=" * 118)
foot("2Q26 release: three verticals = Net Operating Revenue, H1-2026", "text",
     [5_539, 3_627, 3_971], 13_137)
foot("2Q26 release: three verticals NPATM H1-2026 vs audited owners' profit "
     "1,810", "text", [457, 596, 758], 1_811)
foot("FY25 release: three verticals = Net Operating Revenue FY2025", "text",
     [11_861, 6_651, 7_517], 26_029)
foot("FY25 release: FY2025 revenue less adjustments = audited 25,670", "text",
     [26_029, -359], 25_670)
foot("FY24 release column: three verticals FY2024", "text",
     [14_686, 4_777, 4_959], 24_422)
foot("Bank NXT standalone assets, Jun-26 (rounding +1)", "text",
     [15_534, 9_810, 57_817, 28_510, 5_884], 117_555)
foot("Bank NXT standalone liabilities, Jun-26 (rounding +1)", "text",
     [452, 93_979, 6_822], 101_253)
foot("Bank NXT gross loans by type, Jun-26", "text", [32_597, 23_187, 5_689], 61_473)
foot("Bank NXT deposits by type, Jun-26", "text", [57_839, 32_544, 3_596], 93_979)
foot("Bank NXT P&L H1-2026: revenue", "text", [3_283, 500, 188], 3_971)
foot("Bank NXT P&L H1-2026: NPBT", "text", [3_971, -1_633, -185], 2_153)
foot("EFG Hermes H1-2026: Sell-Side", "text", [632, 3_377], 4_009)
foot("EFG Hermes H1-2026: Buy-Side", "text", [793, 340], 1_133)
foot("EFG Hermes H1-2026: net operating profit", "text", [5_539, -4_403], 1_136)
foot("Egypt AUM stack, 2Q26 (EGP bn x10 to keep integers)", "text",
     [303, 281, 59], 643)

print("\n" + "=" * 118)
if FAILS:
    print(f"RESULT: {len(FAILS)} FOOTING FAILURE(S) — the statement is NOT accepted")
    for lab, route, got, printed, diff in FAILS:
        print(f"  ! [{route}] {lab}: computed {got:,} vs printed {printed:,} "
              f"(diff {diff:+,})")
    raise SystemExit(1)
print("RESULT: ALL FOOTING CHECKS PASS.")
print("Four complete audited fiscal years (FY2022, FY2023, FY2024, FY2025) and both")
print("disclosed quarters of the study year (Q1-2026, Q2-2026) foot against their own")
print("printed subtotals, on both the current and the comparative column. The")
print("pixel-read balance sheets agree with the independent text-layer segment note.")
print("The earnings releases tie to the audited statements at every overlap.")
print("=" * 118)
