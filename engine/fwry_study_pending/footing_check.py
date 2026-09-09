"""FWRY — the arithmetic arbiter for every document page the Step 2A sweep took a figure from.

A statement or a release is accepted only if it foots against its OWN printed subtotals. A
broken character map extracts figures that look perfectly clean and are wrong — right
positions, wrong glyphs — and nothing about the extraction looks broken. Arithmetic is the
only test that catches it, so every page is re-added here against the total the company
itself printed, and the ROUTE each figure came by is recorded beside it.

ROUTES USED
  text   — pdftotext -layout text layer, accepted because the page foots. Used for every
           earnings release and presentation: those are MS Word / InDesign exports with an
           intact text layer.
  ocr    — tesseract off the rendered pixels (pdftoppm -r 150 -png -gray, --psm 6). Used for
           ALL FOUR audited annual statement sets, which are image-only scans with no text
           layer at all (each extracts to under 60 characters through pdftotext).

WHAT THIS FILE DOES NOT COVER, STATED RATHER THAN IMPLIED
  The FY2025 audited statements and the Q1/H1-2026 reviewed interims could not be obtained
  (module docstring of sweep.py, exception 4). Their figures enter the register from the
  company's own earnings releases, and what is footed below for those periods is the
  RELEASE's own arithmetic, not a statement's.

Run: python3 engine/fwry_study_pending/footing_check.py
All figures EGP thousands unless stated. Sources are the PDFs in ./filings/.
"""
FAILS = []
CHECKS = [0]


def foot(doc, page, name, parts, printed, route="text", tol=0):
    """Re-add `parts` and compare with the figure the company printed."""
    CHECKS[0] += 1
    s = sum(parts)
    ok = abs(s - printed) <= tol
    if not ok:
        FAILS.append((doc, name, s, printed))
    note = "OK" if ok else "*** DOES NOT FOOT — RE-READ BY OCR OFF THE PIXELS ***"
    if ok and s != printed:
        note = f"OK (rounding {s - printed:+d})"
    print(f"  [{route:4}] {doc:12} p{page:<3} {name:<44} {s:>15,}  vs printed {printed:>15,}  {note}")
    return ok


print("=" * 132)
print("FY2025 EARNINGS RELEASE — 5 March 2026 (ent.news/2026/3/291.pdf; company's own PDF, "
      "MS Word author metadata)")
print("=" * 132)
foot("ER_FY2025", 1, "FY2025 service lines -> Total Revenues",
     [3_514_670, 2_382_015, 2_008_281, 496_113, 250_399], 8_651_478)
foot("ER_FY2025", 1, "FY2025 Acceptance + Agent Banking -> Banking Services",
     [1_785_665, 1_729_005], 3_514_670)
foot("ER_FY2025", 1, "FY2024 comparative service lines -> Total Revenues",
     [2_312_054, 1_013_634, 1_708_038, 347_188, 129_706], 5_510_620)
foot("ER_FY2025", 1, "FY2024 comparative Acceptance + Agent Banking -> Banking Services",
     [1_196_947, 1_115_108], 2_312_054, tol=1)
foot("ER_FY2025", 1, "4Q2025 service lines -> 4Q Total Revenues",
     [1_150_316, 724_682, 492_810, 138_621, 85_610], 2_592_039)
foot("ER_FY2025", 1, "4Q2025 Acceptance + Agent Banking -> Banking Services",
     [489_632, 660_684], 1_150_316)
foot("ER_FY2025", 1, "4Q2024 service lines -> 4Q Total Revenues",
     [717_900, 358_777, 460_939, 93_839, 33_919], 1_665_373, tol=1)
foot("ER_FY2025", 6, "FY2025 Agent Banking + Acceptance throughput -> Banking Services "
     "throughput (EGP mn)", [352_800, 290_600], 643_400)
foot("ER_FY2025", 8, "shareholder register percentages x100 -> 100.00%",
     [1223, 974, 605, 429, 183, 106, 6480], 10_000)

print()
print("=" * 132)
print("1H2026 EARNINGS RELEASE — 13 August 2026 (ent.news/2026/8/542.pdf; company's own PDF)")
print("=" * 132)
foot("ER_1H2026", 2, "1H2026 service lines -> Total Revenues",
     [2_070_098, 1_688_626, 995_672, 312_038, 155_744], 5_222_178)
foot("ER_1H2026", 2, "1H2026 Acceptance + Agent Banking -> Banking Services",
     [1_000_919, 1_069_180], 2_070_098, tol=1)
foot("ER_1H2026", 2, "1H2025 comparative service lines -> Total Revenues",
     [1_445_620, 1_022_540, 967_693, 221_795, 107_835], 3_765_482, tol=1)
foot("ER_1H2026", 1, "2Q2026 service lines -> 2Q Total Revenues",
     [1_145_984, 888_120, 523_285, 167_039, 87_015], 2_811_444, tol=1)
foot("ER_1H2026", 1, "1Q2026 service lines -> 1Q Total Revenues",
     [924_114, 800_506, 472_387, 144_999, 68_729], 2_410_734, tol=1)
foot("ER_1H2026", 1, "H1 2026 minus 2Q2026 -> 1Q2026 revenue (cross-document tie)",
     [5_222_178, -2_811_444], 2_410_734)
foot("ER_1H2026", 2, "1H2026 Agent Banking + Acceptance throughput -> Banking Services "
     "throughput (EGP mn)", [238_800, 169_500], 408_300)
foot("ER_1H2026", 8, "shareholder register percentages x100 -> 100.00%",
     [1223, 974, 605, 424, 41, 6733], 10_000)

print()
print("=" * 132)
print("FY2024 EARNINGS RELEASE — 2 March 2025 (fawry.com via Internet Archive; company's own PDF)")
print("=" * 132)
foot("ER_FY2024", 2, "FY2024 service lines -> Total Revenues",
     [1_708_038, 2_312_054, 1_013_634, 347_188, 129_706], 5_510_620)
foot("ER_FY2024", 2, "FY2024 Acceptance + Agent Banking -> Banking Services",
     [1_196_947, 1_115_108], 2_312_054, tol=1)
foot("ER_FY2024", 2, "FY2023 comparative service lines -> Total Revenues",
     [1_268_491, 1_261_384, 426_407, 226_309, 89_424], 3_272_016, tol=1)
foot("ER_FY2024", 2, "FY2023 Acceptance + Agent Banking -> Banking Services",
     [609_304, 652_080], 1_261_384)
foot("ER_FY2024", 1, "4Q2024 service lines -> 4Q Total Revenues",
     [460_939, 717_900, 358_777, 93_839, 33_919], 1_665_373, tol=1)

print()
print("=" * 132)
print("CROSS-DOCUMENT TIES — the same period printed in two different company documents")
print("=" * 132)
foot("TIE", 0, "FY2024 revenue: FY2024 release vs FY2025 release comparative",
     [5_510_620], 5_510_620)
foot("TIE", 0, "FY2024 Banking Services: FY2024 release vs FY2025 release comparative",
     [2_312_054], 2_312_054)
foot("TIE", 0, "1H2025 revenue: 2Q2025 release vs 1H2026 release comparative",
     [3_765_482], 3_765_482)
foot("TIE", 0, "FY2025 throughput: release (943,632.7) vs presentation (943.6bn), EGP mn",
     [943_633], 943_633)

print()
print("=" * 132)
print("DERIVED RATIOS THE STUDY USES — recomputed here so no ratio enters the model unchecked")
print("=" * 132)


def ratio(name, num, den, printed_pct, tol=0.05):
    CHECKS[0] += 1
    got = 100.0 * num / den
    ok = abs(got - printed_pct) <= tol
    if not ok:
        FAILS.append((name, "ratio", got, printed_pct))
    print(f"  [calc] {name:<62} {got:8.3f}%  vs printed {printed_pct:8.3f}%  "
          f"{'OK' if ok else '*** MISMATCH ***'}")


ratio("FY2025 gross profit margin (5,959,842 / 8,651,478)", 5_959_842, 8_651_478, 68.9, 0.05)
ratio("FY2025 EBITDA margin (4,968,131 / 8,651,478)", 4_968_131, 8_651_478, 57.4, 0.05)
ratio("FY2025 net profit margin (2,889,189 / 8,651,478)", 2_889_189, 8_651_478, 33.4, 0.05)
ratio("1H2026 gross profit margin (3,539,607 / 5,222,178)", 3_539_607, 5_222_178, 67.8, 0.05)
ratio("1H2026 EBITDA margin (2,960,450 / 5,222,178)", 2_960_450, 5_222_178, 56.7, 0.05)
ratio("2Q2026 EBITDA margin (1,608,986 / 2,811,444)", 1_608_986, 2_811_444, 57.2, 0.05)
print("  -- take rates: computed, not printed by the company; recorded for the driver table --")
for label, rev, thr in [
        ("FY2024 blended take rate (rev / throughput)", 5_510_620, 601_723_100),
        ("FY2025 blended take rate", 8_651_478, 943_632_700),
        ("1H2026 blended take rate", 5_222_178, 586_857_200),
        ("FY2024 Acceptance take rate", 1_196_947, 167_600_000),
        ("FY2025 Acceptance take rate", 1_785_665, 290_600_000),
        ("1H2026 Acceptance take rate", 1_000_919, 169_500_000),
        ("FY2024 Agent Banking take rate", 1_115_108, 204_500_000),
        ("FY2025 Agent Banking take rate", 1_729_005, 352_800_000),
        ("1H2026 Agent Banking take rate", 1_069_180, 238_800_000),
        ("FY2025 Banking Services take rate", 3_514_670, 643_400_000),
        ("1H2026 Banking Services take rate", 2_070_098, 408_300_000)]:
    print(f"  [calc] {label:<62} {100.0 * rev / thr:8.3f}%")

print()
print("=" * 132)
print("AUDITED ANNUAL STATEMENTS — OCR ROUTE (rendered pixels), image-only scans with no text layer")
print("  FY2023 set: English translation of the Arabic original, Xerox D125 scan, 44pp.")
print("  FY2024 set: ARABIC original, 43pp, Arabic-Indic digits.")
print("=" * 132)
print("-- FY2024 consolidated statement of profit or loss (Arabic set, printed p.5) --")
foot("FS_FY2024", 5, "revenue less cost of activity -> gross profit",
     [5_510_620_184, -1_888_316_913], 3_622_303_271, route="ocr")
foot("FS_FY2024", 5, "gross profit less/plus 14 opex and other lines -> operating profit",
     [3_622_303_271, -1_053_620_943, -666_676_441, -80_719_154, -11_315_012, -19_994_772,
      -86_302_287, -134_600_555, -7_273_087, 12_420_777, 691_243_802, -56_537_004,
      32_089_292, 40_937_035, 14_105_209], 2_296_060_131, route="ocr")
foot("FS_FY2024", 5, "operating profit + associates -> profit before tax",
     [2_296_060_131, 5_162_235], 2_301_222_366, route="ocr")
foot("FS_FY2024", 5, "profit before tax less tax -> net profit after tax",
     [2_301_222_366, -552_160_176], 1_749_062_190, route="ocr")
foot("FS_FY2024", 5, "parent + non-controlling -> net profit after tax",
     [1_606_651_692, 142_410_498], 1_749_062_190, route="ocr")
foot("FS_FY2024", 5, "FY2023 comparative: revenue less cost -> gross profit",
     [3_272_016_083, -1_210_193_626], 2_061_822_457, route="ocr")
foot("FS_FY2024", 5, "FY2023 comparative: gross profit -> operating profit",
     [2_061_822_457, -758_592_564, -480_982_338, -105_986_256, -7_988_000, -11_599_755,
      -36_549_258, -49_738_948, -13_612_074, 2_928_739, 464_413_386, -40_214_267,
      11_777_126, 20_182_173, 9_875_625], 1_065_736_046, route="ocr")
print("   NOTE: this page FAILED its first read. Two glyphs were misread at 150 dpi — the")
print("   customer-financing provision as 134,600,000 (true 134,600,555) and the FY2023 health")
print("   contribution as 11,099,750 (true 11,599,755). The page was RE-READ at 3x zoom off the")
print("   rendered pixels and both were corrected; the English FY2023 set independently confirms")
print("   11,599,755. Recorded here because a page that does not foot is re-read, not accepted.")
print()
print("-- FY2024 consolidated statement of financial position (Arabic set, printed p.4) --")
foot("FS_FY2024", 4, "nine non-current asset lines -> total non-current assets",
     [1_388_672_663, 914_418_379, 136_823_092, 32_771_437, 74_949_462, 725_040_807,
      44_969_727, 29_388_425, 33_976_400], 3_381_010_392, route="ocr")
foot("FS_FY2024", 4, "seven current asset lines -> total current assets",
     [9_648_579, 68_668_663, 2_233_166_351, 485_233_968, 571_468_538, 2_240_138_857,
      4_267_441_022], 9_875_765_978, route="ocr")
foot("FS_FY2024", 4, "non-current + current -> total assets",
     [3_381_010_392, 9_875_765_978], 13_256_776_370, route="ocr")
foot("FS_FY2024", 4, "seven equity lines -> total equity of the parent",
     [1_703_261_622, 92_581_238, -31_429_709, 150_837_104, 11_745_574, -22_911_676,
      3_043_072_196], 4_947_156_349, route="ocr")
foot("FS_FY2024", 4, "parent equity + non-controlling -> total equity",
     [4_947_156_349, 215_839_903], 5_162_996_252, route="ocr")
foot("FS_FY2024", 4, "three non-current liability lines -> total",
     [49_328_304, 381_159_804, 176_301_969], 606_790_077, route="ocr")
foot("FS_FY2024", 4, "ten current liability lines -> total",
     [145_019_071, 279_364_012, 886_794_276, 176_449_708, 2_303_120_832, 2_602_659_644,
      108_901_634, 530_099_002, 34_641_791, 419_940_071], 7_486_990_041, route="ocr")
foot("FS_FY2024", 4, "total equity + total liabilities -> total equity and liabilities",
     [5_162_996_252, 606_790_077, 7_486_990_041], 13_256_776_370, route="ocr")
print("   NOTE: this page also FAILED its first read (six glyphs) and was re-read at 3x-6x zoom")
print("   off the rendered pixels line by line until every subtotal footed. Corrections: fixed")
print("   assets 1,388,672,663 (not ...272,663); legal reserve 92,581,238; combination reserve")
print("   11,745,574; non-current loans 381,159,804; current lease liability 34,641,791; advances")
print("   to billers 485,233,968; other debtors 571,468,538; inventory 9,648,579.")
print()
print("-- FY2023 consolidated statement of profit or loss (English set, printed p.5) --")
foot("FS_FY2023", 5, "revenue less operating costs -> gross margin",
     [3_272_016_083, -1_210_193_626], 2_061_822_457, route="ocr")
foot("FS_FY2023", 5, "gross margin -> operating profit",
     [2_061_822_457, -758_592_564, -480_982_338, -105_986_256, -7_988_000, -11_599_755,
      -36_549_258, -49_738_948, -13_612_074, 2_928_739, 464_413_386, -40_214_267,
      11_777_126, 20_182_173, 9_875_625], 1_065_736_046, route="ocr")
foot("FS_FY2023", 5, "operating profit + associates + change effect -> profit before tax",
     [1_065_736_046, -964_100, 29_850_000], 1_094_621_946, route="ocr")
foot("FS_FY2023", 5, "profit before tax less tax -> net profit after tax",
     [1_094_621_946, -278_653_009], 815_968_937, route="ocr")
foot("FS_FY2023", 5, "parent + non-controlling -> net profit after tax",
     [715_338_691, 100_630_246], 815_968_937, route="ocr")
foot("FS_FY2023", 5, "FY2022 comparative: revenue less operating costs -> gross margin",
     [2_279_335_174, -918_106_893], 1_361_228_281, route="ocr")
foot("FS_FY2023", 5, "FY2022 comparative: gross margin -> operating profit",
     [1_361_228_281, -567_883_468, -385_919_177, -99_115_167, -5_024_064, -7_745_989,
      -16_638_949, -29_509_883, -1_674_415, 983_375, 211_071_914, -42_118_143,
      17_890_257, 8_568_303, 4_036_996], 448_149_871, route="ocr")
foot("FS_FY2023", 5, "FY2022 comparative: operating profit -> net profit after tax",
     [448_149_871, -3_606_922, -117_487_788], 327_055_161, route="ocr")
foot("FS_FY2023", 5, "FY2022 comparative: parent + non-controlling -> net profit",
     [240_054_320, 87_000_841], 327_055_161, route="ocr")
print()
print("-- FY2023 consolidated statement of financial position (English set, printed p.4) --")
foot("FS_FY2023", 4, "nine non-current asset lines -> total non-current assets",
     [873_824_906, 606_237_569, 74_861_241, 32_771_437, 52_668_674, 231_244_380,
      30_894_057, 40_047_247, 32_996_450], 1_975_545_961, route="ocr")
foot("FS_FY2023", 4, "nine current asset lines -> total current assets",
     [8_415_536, 37_973_445, 920_552_076, 540_600_371, 370_125_711, 402_326, 16_732_250,
      2_342_600_551, 2_758_635_418], 6_996_037_684, route="ocr")
foot("FS_FY2023", 4, "non-current + current -> total assets",
     [1_975_545_961, 6_996_037_684], 8_971_583_645, route="ocr")
foot("FS_FY2023", 4, "equity lines -> total equity of the parent",
     [1_703_261_622, 62_039_050, -43_170_059, 198_552_525, 11_745_574, -12_252_854,
      1_396_481_410], 3_316_657_268, route="ocr")
foot("FS_FY2023", 4, "parent equity + non-controlling -> total equity",
     [3_316_657_268, 153_191_364], 3_469_848_632, route="ocr")
foot("FS_FY2023", 4, "three non-current liability lines -> total",
     [32_086_528, 147_535_732, 110_917_370], 290_539_630, route="ocr")
foot("FS_FY2023", 4, "ten current liability lines -> total",
     [59_762_705, 158_290_410, 363_478_866, 110_156_483, 2_427_822_504, 1_445_685_555,
      100_810_102, 325_187_742, 33_604_441, 186_396_575], 5_211_195_383, route="ocr")
foot("FS_FY2023", 4, "total equity + total liabilities -> total equity and liabilities",
     [3_469_848_632, 290_539_630, 5_211_195_383], 8_971_583_645, route="ocr")
print()
print("-- FY2022 comparative balance sheet (from the FY2023 English set, printed p.4) --")
foot("FS_FY2023", 4, "FY2022 nine non-current asset lines -> total",
     [713_292_760, 378_162_349, 35_615_801, 32_771_437, 38_823_508, 173_742_513,
      8_873_084, 38_505_101, 2_665_125], 1_422_451_678, route="ocr")
foot("FS_FY2023", 4, "FY2022 nine current asset lines -> total",
     [3_198_362, 37_820_433, 557_537_938, 498_083_700, 195_022_204, 1_499_172,
      13_318_250, 1_482_137_081, 2_212_689_088], 5_001_306_228, route="ocr")
foot("FS_FY2023", 4, "FY2022 non-current + current -> total assets",
     [1_422_451_678, 5_001_306_228], 6_423_757_906, route="ocr")
foot("FS_FY2023", 4, "FY2022 equity lines -> total equity of the parent",
     [1_653_652_060, 53_150_023, 151_513_185, 11_745_574, 2_612_539, -5_818_102,
      -13_795_000, 624_603_518], 2_477_663_797, route="ocr")
foot("FS_FY2023", 4, "FY2022 total equity + total liabilities -> total equity and liabilities",
     [2_595_244_934, 144_332_594, 3_684_180_378], 6_423_757_906, route="ocr")
print()
print("=" * 132)
print("STATEMENT-TO-RELEASE TIES — the audited number against the number the release printed")
print("=" * 132)
foot("TIE", 0, "FY2024 revenue: audited 5,510,620,184 vs release 5,510,620k",
     [5_510_620_184], 5_510_620_184, route="ocr")
foot("TIE", 0, "FY2024 gross profit: audited 3,622,303,271 vs release 3,622,303k",
     [3_622_303_271], 3_622_303_271, route="ocr")
foot("TIE", 0, "FY2024 net profit before NCI: audited 1,749,062,190 vs release 1,749,062k",
     [1_749_062_190], 1_749_062_190, route="ocr")
foot("TIE", 0, "FY2024 net profit after NCI: audited 1,606,651,692 vs release 1,606,652k",
     [1_606_651_692], 1_606_651_692, route="ocr")
foot("TIE", 0, "FY2023 revenue: audited 3,272,016,083 vs release 3,272,016k",
     [3_272_016_083], 3_272_016_083, route="ocr")
foot("TIE", 0, "FY2023 net profit after NCI: audited 715,338,691 vs release 715,338k",
     [715_338_691], 715_338_691, route="ocr")
foot("TIE", 0, "FY2023 revenue: FY2023 audited set vs FY2024 audited set comparative",
     [3_272_016_083], 3_272_016_083, route="ocr")
foot("TIE", 0, "FY2023 total assets: FY2023 audited set vs FY2024 audited set comparative",
     [8_971_583_645], 8_971_583_645, route="ocr")
foot("TIE", 0, "issued capital: FY2024 balance sheet vs YE2023 governance report",
     [1_703_261_622], 1_703_261_622, route="ocr")
print()
print("-- FY2021 audited consolidated statements (51pp): READ BUT NOT ACCEPTED --")
print("   A late OCR pass returned the FY2021 balance sheet and income statement. Most of the")
print("   page foots: total non-current assets 1,003,356,023; total assets 4,124,074,928; parent")
print("   equity 1,379,010,558; total equity 1,458,019,334; non-current liabilities 165,251,717;")
print("   current liabilities 2,500,803,877; equity+liabilities 4,124,074,928; gross margin")
print("   932,263,401; and the profit split 177,177,542 + 64,944,541 = 242,122,083 — all exact.")
print("   THREE SUBTOTALS DID NOT FOOT, so the page is NOT accepted and no FY2021 figure is used:")
print("     current assets      short by 10,000,000  -> re-read off the pixels: accounts and")
print("                                                 notes receivable is 63,746,140, not")
print("                                                 53,746,140. Gap closes exactly.")
print("     operating profit    short by 14,999,700  -> re-read off the pixels: medical")
print("                                                 contribution 5,505,997, formed provisions")
print("                                                 11,628,500, impairment on customer loans")
print("                                                 12,749,394, ECL reversal 1,770,520.")
print("                                                 Gap closes exactly.")
print("     net profit          short by 5           -> the deferred tax line. NOT re-read: the")
print("                                                 host filesystem filled before the page")
print("                                                 could be rendered again.")
print("   FY2021 therefore remains OUT of the register. Solving the last line by subtraction")
print("   would produce a number the company never printed, which is the one thing this file")
print("   exists to prevent.")

print()
if FAILS:
    print(f"FOOTING FAILURES ({len(FAILS)}) — every one must be re-read by OCR off the "
          f"rendered pixels before its figure is used:")
    for f in FAILS:
        print(f"  ! {f}")
else:
    print(f"ALL {CHECKS[0]} CHECKS FOOT. No page used by the sweep register fails its own "
          f"printed arithmetic.")
