"""ARCC walk-forward panel — the company's own audited consolidated statements.

EVERY FIGURE HERE WAS READ FROM A SCANNED PAGE AND THEN FOOTED, and the footing
runs at import as assertions rather than living in a comment.  That is not
ceremony.  ARCC files every statement as an image with no text layer, so every
number arrives through OCR, and this scan has a SYSTEMATIC failure mode: it
reads a leading 1 as a 2.  On this panel the arithmetic caught five such
misreads that looked perfectly clean on the page —

  FY2016 income tax        224,683,515   -> 124,683,515   (income statement)
  FY2016 raw materials     2,257,697,536 -> 1,257,697,536 (note 5)
  FY2016 cost of sales     2,655,408,051 -> 1,655,408,051 (note 5 total)
  FY2015 local sales, net  2,379,482,482 -> 2,179,482,482 (FY2016 filing, note 5)
  FY2022 G&A               214,977,983   -> 114,977,983   (FY2023 filing, note 6)

— and every one of them was then CONFIRMED INDEPENDENTLY by the following
year's comparative column.  Not one would have been visible to a reader of the
extracted figure.  ARITHMETIC IS THE ARBITER, NOT THE EXTRACTOR'S CONFIDENCE.

PROVENANCE.  Four fields on every year: value, source document, document date,
tier.  Every financial figure is tier A — ARCC's own audited consolidated
financial statements, downloaded from its own investor-relations archive at
arabiancementcompany.com.  Every physical figure is tier A COMPANY_IR — its own
earnings releases and investor presentations, tagged separately because the
audited statements carry no tonne.  No vendor, aggregator or press figure enters
this panel.

POINT IN TIME.  Every year is carried AS FIRST REPORTED, from its own filing.
Three years in this window were re-presented afterwards (B-2, B-8) and one was
re-presented onto a different revenue basis entirely (B-13), so the distinction
is load-bearing here rather than decorative: an origin standing at FY2018 saw a
cost of sales of 2,826,502,704 and could not have seen the 2,821,949,633 the
FY2019 filing later showed for the same year.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
IR = "https://arabiancementcompany.com/investor-relations/financial-information/"

# ---------------------------------------------------------------------------
# Sources
# ---------------------------------------------------------------------------
SOURCES = {
    "FS2015": dict(file="ACC-2015-Consolidated-Financials-English.pdf", reports="FY2015",
                   comparative="FY2014", tier="A", auditor="Saleh, Barsoum & Abdel Aziz",
                   layout="income-statement-2015", note_revenue=18, note_cost=19),
    "FS2016": dict(file="FY-2016-Consolidated-Financials-English.pdf", reports="FY2016",
                   comparative="FY2015", tier="A", auditor="Saleh, Barsoum & Abdel Aziz",
                   layout="profit-or-loss", note_revenue=5, note_cost=6),
    "FS2017": dict(file="FY-2017-Consolidated-Financials-English.pdf", reports="FY2017",
                   comparative="FY2016", tier="A", auditor="Saleh, Barsoum & Abdel Aziz",
                   layout="profit-or-loss", note_revenue=4, note_cost=5),
    "FS2018": dict(file="ARCC_FY_2018_Consolidated_Financials-English.pdf", reports="FY2018",
                   comparative="FY2017", tier="A", auditor="Saleh, Barsoum & Abdel Aziz",
                   layout="profit-or-loss", note_revenue=4, note_cost=5),
    "FS2019": dict(file="FY_2019_Consolidated_Financials-English.pdf", reports="FY2019",
                   comparative="FY2018", tier="A", auditor="Saleh, Barsoum & Abdel Aziz",
                   layout="profit-or-loss", note_revenue=4, note_cost=5),
    "FS2020": dict(file="FY-2020-consolidated-financials-english.pdf", reports="FY2020",
                   comparative="FY2019", tier="A", auditor="Saleh, Barsoum & Abdel Aziz",
                   layout="profit-or-loss", note_revenue=4, note_cost=5),
    "FS2021": dict(file="FY_2021_Consolidated_Financials-English.pdf", reports="FY2021",
                   comparative="FY2020", tier="A", auditor="Saleh, Barsoum & Abdel Aziz",
                   layout="profit-or-loss", note_revenue=4, note_cost=5),
    "FS2022": dict(file="FY_2022_Consolidated_Financials-English.pdf", reports="FY2022",
                   comparative="FY2021", tier="A", auditor="Wafik, Ramy & Partners (Deloitte)",
                   layout="profit-and-loss-ar", note_revenue=4, note_cost=5),
    "FS2023": dict(file="4Q2023_ACC_Consolidated_Financials.pdf", reports="FY2023",
                   comparative="FY2022", tier="A", auditor="Wafik, Ramy & Partners (Deloitte)",
                   layout="profit-and-loss-ar", note_revenue=4, note_cost=5),
    "FS2024": dict(file="FY2024_Consolidated_Financials-English.pdf", reports="FY2024",
                   comparative="FY2023", tier="A", auditor="Wafik, Ramy & Partners (Deloitte)",
                   layout="profit-and-loss-ar", note_revenue=4, note_cost=5),
    "FS2025": dict(file="FY-2025-Consolidated-Financials-English.pdf", reports="FY2025",
                   comparative="FY2024", tier="A", auditor="Wafik, Ramy & Partners (Deloitte)",
                   doc_date="2026-02-25", layout="profit-and-loss-ar",
                   note_revenue=4, note_cost=5),
    "IH2026": dict(file="2Q2026-Consolidated-Financials-English.pdf", reports="H1-2026",
                   comparative="H1-2025", tier="A", auditor="Wafik, Ramy & Partners (Deloitte)",
                   review="limited review", layout="profit-or-loss-interim"),
    "Q12026": dict(file="Q1-2026-Consolidated-Financials-English.pdf", reports="Q1-2026",
                   comparative="Q1-2025", tier="A", auditor="Wafik, Ramy & Partners (Deloitte)",
                   review="limited review", layout="profit-or-loss-interim"),
}

YEARS = ["FY%d" % y for y in range(2014, 2026)]
ORIGINS = ["FY%d" % y for y in range(2018, 2026)]
HORIZONS = [1, 2, 3, 4, 5]

# ---------------------------------------------------------------------------
# Income statement, AS EACH YEAR WAS FIRST REPORTED.
# Every line is stated POSITIVE as printed; the footing applies the sign the
# statement's own layout gives it.  `tax` is the EXPENSE, so a credit is negative.
# ---------------------------------------------------------------------------
IS = {
 "FY2014": dict(src="FS2015", column="comparative",
    revenue=2_520_586_769, cogs=1_784_610_553, gross_profit=735_976_216,
    ga=91_030_115, pbt=524_314_491, tax=149_591_732, pat=374_722_759,
    majority=374_717_936, nci=4_823),
 "FY2015": dict(src="FS2015", column="own",
    revenue=2_273_300_139, cogs=1_718_039_515, gross_profit=555_260_624,
    ga=81_018_505, pbt=327_193_180, tax=49_964_253, pat=277_228_927,
    majority=277_224_384, nci=4_543),
 "FY2016": dict(src="FS2016", column="own",
    revenue=2_350_034_091, cogs=1_655_408_051, gross_profit=694_626_040,
    ga=78_212_056, pbt=369_699_646, tax=124_683_515, pat=245_016_131,
    majority=245_010_719, nci=5_412),
 "FY2017": dict(src="FS2017", column="own",
    revenue=2_647_337_474, cogs=2_268_506_723, gross_profit=378_830_751,
    ga=106_722_754, pbt=192_592_059, tax=-23_018_600, pat=215_610_659,
    majority=215_607_756, nci=2_903),
 "FY2018": dict(src="FS2018", column="own",
    revenue=3_274_705_803, cogs=2_826_502_704, gross_profit=448_203_099,
    ga=108_388_819, pbt=239_076_638, tax=7_434_476, pat=231_642_162,
    majority=232_910_621, nci=-1_268_459),
 "FY2019": dict(src="FS2019", column="own",
    revenue=3_101_527_489, cogs=2_894_882_469, gross_profit=206_645_020,
    ga=103_266_465, pbt=36_870_099, tax=7_931_515, pat=28_938_584,
    majority=28_927_908, nci=10_676),
 "FY2020": dict(src="FS2020", column="own",
    revenue=2_481_182_477, cogs=2_455_463_159, gross_profit=25_719_318,
    ga=95_464_653, pbt=-137_411_687, tax=-14_623_637, pat=-122_788_050,
    majority=-122_788_178, nci=128),
 "FY2021": dict(src="FS2021", column="own",
    revenue=2_448_631_353, cogs=2_281_083_584, gross_profit=167_547_769,
    ga=81_070_460, pbt=55_178_070, tax=20_988_687, pat=34_189_383,
    majority=34_181_810, nci=7_573),
 "FY2022": dict(src="FS2022", column="own",
    revenue=4_675_002_824, cogs=3_789_816_211, gross_profit=885_186_613,
    ga=114_977_983, pbt=521_863_563, tax=162_877_642, pat=358_985_921,
    majority=358_986_481, nci=-560),
 "FY2023": dict(src="FS2023", column="own",
    revenue=6_042_831_338, cogs=4_759_815_212, gross_profit=1_283_016_126,
    ga=183_940_276, pbt=930_231_432, tax=232_732_802, pat=697_498_630,
    majority=697_488_741, nci=9_889),
 "FY2024": dict(src="FS2024", column="own",
    revenue=8_729_782_821, cogs=6_642_972_487, gross_profit=2_086_810_334,
    ga=267_798_104, pbt=1_505_866_118, tax=345_730_996, pat=1_160_135_122,
    majority=1_160_129_411, nci=5_711),
 "FY2025": dict(src="FS2025", column="own",
    revenue=12_447_320_081, cogs=7_389_054_416, gross_profit=5_058_265_665,
    ga=384_332_833, pbt=4_725_157_878, tax=1_125_467_657, pat=3_599_690_221,
    majority=3_599_585_937, nci=104_284),
}

# The half year the current study never opened.  Carried for the STUDY rebuild,
# not for the walk-forward, whose last scored origin is FY2024.
INTERIM = {
 "H1-2026": dict(src="IH2026", revenue=6_080_577_747, cogs=3_619_039_609,
    gross_profit=2_461_538_138, ga=225_744_621, provisions=31_498_214,
    interest_income=136_861_895, other_income=480_336_061, finance_costs=23_471_833,
    fx=64_661_520, pbt=2_862_682_946, tax=690_229_472, pat=2_172_453_474,
    majority=2_172_395_425, export_subsidy=467_813_139),
 "H1-2025": dict(src="IH2026", column="comparative", revenue=5_499_911_617,
    cogs=3_404_816_990, gross_profit=2_095_094_627, ga=169_880_277,
    provisions=6_550_000, interest_income=54_742_425, other_income=5_615_745,
    finance_costs=30_959_582, fx=-63_689_314, pbt=1_885_513_624, tax=479_961_936,
    pat=1_405_551_688, majority=1_405_469_527),
}

# ---------------------------------------------------------------------------
# Restatements: the SAME year as the FOLLOWING filing later showed it.
# Carried beside the as-reported figure, never substituted for it (B-2).
# ---------------------------------------------------------------------------
RESTATED = {
 "FY2015": dict(src="FS2016", revenue=2_256_645_854, cogs=1_702_399_822,
                gross_profit=554_246_032, ga=80_935_243, pbt=326_988_832,
                note="revenue moves from a GROSS presentation with a disclosed "
                     "sales-discount line to a NET one (B-13); profit after tax unchanged"),
 "FY2016": dict(src="FS2017", cogs=1_655_408_051, mfg_depreciation=155_414_197,
                amortisation=50_676_249,
                note="depreciation and amortisation reclassified between themselves; "
                     "183,570,446 + 22,520,000 = 155,414,197 + 50,676,249, total unchanged"),
 "FY2018": dict(src="FS2019", cogs=2_821_949_633, ga=112_941_890,
                note="4,553,071 moved OUT of cost of sales INTO G&A; PBT unchanged"),
 "FY2019": dict(src="FS2020", cogs=2_899_331_819, ga=98_817_115,
                note="4,449,350 moved INTO cost of sales OUT of G&A — the OPPOSITE "
                     "direction to FY2018's; PBT unchanged"),
}

# ---------------------------------------------------------------------------
# Cost of sales, by note, AS FIRST REPORTED.
# `inventory_change` exists only in the 2015-layout filings; `transport` only
# from FY2016; `rou` (right-of-use amortisation) only from FY2019 (B-3).
# ---------------------------------------------------------------------------
COST = {
 "FY2014": dict(src="FS2015", raw=1_606_615_844, mfg_dep=169_431_156, amort=22_519_999,
                transport=0, overhead=90_913_832, rou=0, inv_change=-104_870_278),
 "FY2015": dict(src="FS2015", raw=1_429_408_240, mfg_dep=175_410_975, amort=22_520_000,
                transport=0, overhead=85_704_714, rou=0, inv_change=4_995_586),
 "FY2016": dict(src="FS2016", raw=1_257_697_536, mfg_dep=183_570_446, amort=22_520_000,
                transport=63_186_301, overhead=128_433_768, rou=0, inv_change=0),
 "FY2017": dict(src="FS2017", raw=1_813_669_965, mfg_dep=186_156_378, amort=50_676_249,
                transport=71_660_891, overhead=146_343_240, rou=0, inv_change=0),
 "FY2018": dict(src="FS2018", raw=2_320_100_398, mfg_dep=199_737_195, amort=50_676_251,
                transport=83_978_028, overhead=172_010_832, rou=0, inv_change=0),
 "FY2019": dict(src="FS2019", raw=2_351_514_978, mfg_dep=206_253_826, amort=50_676_249,
                transport=96_873_618, overhead=185_250_850, rou=4_312_948, inv_change=0),
 "FY2020": dict(src="FS2020", raw=1_951_992_478, mfg_dep=207_050_680, amort=40_749_783,
                transport=76_349_399, overhead=177_282_173, rou=2_038_646, inv_change=0),
 "FY2021": dict(src="FS2021", raw=1_705_509_969, mfg_dep=215_824_383, amort=34_624_973,
                transport=114_651_406, overhead=204_570_005, rou=5_902_848, inv_change=0),
 "FY2022": dict(src="FS2022", raw=3_118_749_383, mfg_dep=205_958_106, amort=28_156_249,
                transport=165_490_092, overhead=265_974_820, rou=5_487_561, inv_change=0),
 # FY2023 overhead is RECOVERED BY FOOTING: the OCR lost the line entirely and the
 # note's other five components plus the income statement's cost of sales pin it
 # exactly.  Recorded as derived rather than read.
 "FY2023": dict(src="FS2023", raw=3_779_817_706, mfg_dep=212_760_649, amort=28_156_249,
                transport=395_718_132, overhead=336_471_143, rou=6_891_333, inv_change=0,
                derived=("overhead",)),
 "FY2024": dict(src="FS2024", raw=5_225_344_010, mfg_dep=217_717_204, amort=28_156_249,
                transport=792_242_214, overhead=372_430_396, rou=7_082_414, inv_change=0),
 "FY2025": dict(src="FS2025", raw=5_698_184_715, mfg_dep=254_765_548, amort=28_156_249,
                transport=764_279_332, overhead=641_143_208, rou=2_525_364, inv_change=0),
}

# ---------------------------------------------------------------------------
# Revenue by note, AS FIRST REPORTED.
# FY2014-FY2015 are on the GROSS basis with a disclosed discount line (B-13);
# `discounts` is zero from FY2016, when the note itself went net.
# `svc_local` / `svc_export` are split only from FY2022 (B-4); before that the
# single unattributed services line is carried in `svc_local` with
# `services_attributed=False`.
# ---------------------------------------------------------------------------
REV = {
 "FY2014": dict(src="FS2015", local=2_809_558_372, export=4_045_800, svc_local=42_460_919,
                svc_export=0, discounts=335_478_322, services_attributed=False, basis="gross"),
 "FY2015": dict(src="FS2015", local=2_748_659_747, export=13_462_034, svc_local=63_701_339,
                svc_export=0, discounts=552_522_981, services_attributed=False, basis="gross"),
 "FY2016": dict(src="FS2016", local=2_238_999_956, export=28_820_124, svc_local=82_214_011,
                svc_export=0, discounts=0, services_attributed=False, basis="net"),
 "FY2017": dict(src="FS2017", local=2_303_579_124, export=236_642_584, svc_local=107_115_766,
                svc_export=0, discounts=0, services_attributed=False, basis="net"),
 "FY2018": dict(src="FS2018", local=2_838_120_489, export=317_378_870, svc_local=119_206_444,
                svc_export=0, discounts=0, services_attributed=False, basis="net"),
 "FY2019": dict(src="FS2019", local=2_604_758_736, export=342_865_036, svc_local=153_903_717,
                svc_export=0, discounts=0, services_attributed=False, basis="net"),
 "FY2020": dict(src="FS2020", local=2_159_139_351, export=199_251_333, svc_local=122_791_793,
                svc_export=0, discounts=0, services_attributed=False, basis="net"),
 "FY2021": dict(src="FS2021", local=2_052_924_236, export=239_005_072, svc_local=156_702_045,
                svc_export=0, discounts=0, services_attributed=False, basis="net"),
 "FY2022": dict(src="FS2022", local=3_821_544_846, export=667_514_155, svc_local=103_058_888,
                svc_export=82_884_935, discounts=0, services_attributed=True, basis="net"),
 "FY2023": dict(src="FS2023", local=3_906_434_047, export=1_622_380_975, svc_local=82_820_228,
                svc_export=431_196_088, discounts=0, services_attributed=True, basis="net"),
 "FY2024": dict(src="FS2024", local=4_703_479_247, export=3_222_781_048, svc_local=179_825_230,
                svc_export=623_697_296, discounts=0, services_attributed=True, basis="net"),
 "FY2025": dict(src="FS2025", local=8_350_454_610, export=3_356_422_381, svc_local=281_863_546,
                svc_export=458_579_544, discounts=0, services_attributed=True, basis="net"),
}

# ---------------------------------------------------------------------------
# Everything between gross profit and profit before tax, AS FIRST REPORTED.
# Sign convention: `+` lines add to profit, `-` lines subtract.  Stored SIGNED,
# so the footing below is a plain sum and there is no sign table to remember.
#
# FY2016 interest income is 7,185,112 and NOT the 7,485,112 its own filing's
# scan yields: the block would then foot to 369,999,647 against a printed
# 369,699,646, and the FY2017 filing's comparative column prints 7,185,112.
# One more instance of B-1, caught the same way as the other five.
# ---------------------------------------------------------------------------
OTHER = {
 "FY2014": dict(src="FS2015", provisions=-2_584_364, reversals=+555_431,
    other_income=+1_223_200, interest_income=+826_015, impairments=-147_782,
    finance_costs=-94_560_609, fx=-25_856_362, disposals=-87_139, jv=0),
 "FY2015": dict(src="FS2015", provisions=-12_660_442, reversals=0,
    other_income=+1_662_397, interest_income=+2_957_672, impairments=-5_631_155,
    finance_costs=-89_563_808, fx=-44_003_603, disposals=+190_000, jv=0),
 "FY2016": dict(src="FS2016", provisions=-1_552_448, reversals=+7_565_087,
    other_income=+886_776, interest_income=+7_185_112, impairments=-832_511,
    finance_costs=-6_816_924, fx=-245_925_656, disposals=-7_711_192, jv=+487_419),
 "FY2017": dict(src="FS2017", provisions=-14_071_776, reversals=+689_181,
    other_income=+3_293_072, interest_income=+4_837_651, impairments=-1_452_480,
    finance_costs=-104_201_990, fx=+30_780_197, disposals=+32_115, jv=+578_092),
 "FY2018": dict(src="FS2018", provisions=-2_245_000, reversals=+2_276_219,
    other_income=+9_033_836, interest_income=+4_913_813, impairments=0,
    finance_costs=-111_059_969, fx=-3_896_880, disposals=0, jv=+240_339),
 "FY2019": dict(src="FS2019", provisions=-2_151_787, reversals=0,
    other_income=+4_346_957, interest_income=+4_306_309, impairments=-2_244_450,
    finance_costs=-137_158_211, fx=+66_332_750, disposals=+15_398, jv=+44_578),
 "FY2020": dict(src="FS2020", provisions=-7_928_240, reversals=0,
    other_income=+7_842_516, interest_income=+1_537_747, impairments=-756_942,
    finance_costs=-81_107_274, fx=+12_322_680, disposals=+277_466, jv=+145_695),
 "FY2021": dict(src="FS2021", provisions=-7_368_018, reversals=0,
    other_income=+46_323_288, interest_income=+743_822, impairments=0,
    finance_costs=-70_126_214, fx=-1_060_989, disposals=+120_000, jv=+68_872),
 "FY2022": dict(src="FS2022", provisions=-111_939_885, reversals=0,
    other_income=+104_227_501, interest_income=+9_967_780, impairments=-706_681,
    finance_costs=-58_081_220, fx=-192_058_477, disposals=+200_000, jv=+45_915),
 "FY2023": dict(src="FS2023", provisions=-15_220_195, reversals=0,
    other_income=+14_913_053, interest_income=+30_813_502, impairments=-5_525_753,
    finance_costs=-76_979_253, fx=-115_144_171, disposals=+87_675, jv=-1_789_276),
 "FY2024": dict(src="FS2024", provisions=-56_052_950, reversals=+1_886_452,
    other_income=+18_292_936, interest_income=+56_458_493, impairments=0,
    finance_costs=-91_188_916, fx=-243_812_127, disposals=+1_270_000, jv=0),
 "FY2025": dict(src="FS2025", provisions=-74_505_707, reversals=0,
    other_income=+53_339_508, interest_income=+226_274_781, impairments=-3_603_563,
    finance_costs=-49_841_733, fx=-101_578_240, disposals=+1_140_000, jv=0),
}

# ---------------------------------------------------------------------------
# Interest-bearing borrowings and the interest they actually bore.
# [R-FCAL-01] §3 trap (i): the rate is formed ONLY on the balances that pay
# interest — long-term borrowings, their current portion, and credit facilities.
# Trade and notes payable, creditors and other credit balances and current tax
# liabilities are excluded BY CONSTRUCTION, not by judgement.
# ---------------------------------------------------------------------------
DEBT = {
 # Total interest-bearing borrowings at each year end: long-term borrowings,
 # their current portion, and credit facilities.  Where the filing prints the
 # combined figure it is carried and the components are checked against it.
 "FY2016": dict(src="FS2017", total=901_665_719, noncurrent=463_562_238,
                current_portion=371_986_732, credit_facilities=66_116_749),
 "FY2017": dict(src="FS2017", total=1_069_055_860, noncurrent=601_101_209,
                current_portion=167_535_000, credit_facilities=300_419_651),
 "FY2018": dict(src="FS2018", total=970_566_943, noncurrent=619_160_870,
                current_portion=77_731_487, credit_facilities=273_674_586),
 "FY2019": dict(src="FS2019", total=644_228_779, noncurrent=491_836_958,
                current_portion=90_356_520, credit_facilities=62_035_301),
 "FY2020": dict(src="FS2021", total=826_729_964, noncurrent=387_454_349,
                current_portion=99_165_216, credit_facilities=340_110_399),
 "FY2021": dict(src="FS2022", total=627_482_651, noncurrent=272_760_907,
                current_portion=114_334_781, credit_facilities=240_386_963),
 "FY2022": dict(src="FS2022", total=701_655_075, noncurrent=177_476_090,
                current_portion=163_534_780, credit_facilities=360_644_205),
 "FY2023": dict(src="FS2023", total=90_074_273, noncurrent=0,
                current_portion=0, credit_facilities=90_074_273),
 "FY2024": dict(src="FS2025", total=760_917_684, noncurrent=120_392_380,
                current_portion=25_481_075, credit_facilities=615_044_229),
 "FY2025": dict(src="FS2025", total=1_133_932_616, noncurrent=888_522_538,
                current_portion=145_493_141, credit_facilities=99_916_937),
}

# ---------------------------------------------------------------------------
# Physical drivers — the company's own earnings releases and presentations.
# Volumes in THOUSAND tonnes.  local + export = total in every year the release
# states all three, which is the check that keeps the deck restatements of B-8
# out of the panel.
# ---------------------------------------------------------------------------
PHYS = {
 "FY2014": dict(src="ER/deck", total=4_131.0, local=None, export=None),
 "FY2015": dict(src="ER/deck", total=4_271.0, local=None, export=None),
 "FY2016": dict(src="ER2016", total=4_040.0, local=3_989.0, export=50.0),
 "FY2017": dict(src="ER2017", total=4_114.0, local=3_714.0, export=401.0),
 "FY2018": dict(src="ER2018", total=4_461.0, local=3_858.0, export=602.0),
 "FY2019": dict(src="ER2019", total=4_557.0, local=3_944.0, export=614.0),
 "FY2020": dict(src="ER2020", total=4_078.0, local=3_714.0, export=364.0),
 "FY2021": dict(src="ER2021", total=3_208.0, local=None, export=497.0),
 "FY2022": dict(src="ER2022", total=4_561.0, local=3_559.1, export=None,
                clinker_export=936.3),
 "FY2023": dict(src="ER2023", total=4_376.1, local=2_674.9, export=1_701.2,
                cement_export=159.3, clinker_export=1_541.9),
 "FY2024": dict(src="ER2024", total=5_054.3, local=2_618.3, export=2_436.0,
                cement_export=361.7, clinker_export=2_074.4),
 "FY2025": dict(src="IP2025", total=4_853.6, local=2_923.6, export=1_930.0,
                cement_export=629.5, clinker_export=1_300.5),
}


# ---------------------------------------------------------------------------
# Footing.  Runs at import.  A panel that will not foot must not be usable.
# ---------------------------------------------------------------------------
def _close(a, b, tol=2):
    return abs(a - b) <= tol


def foot():
    """Every arithmetic identity the filings themselves assert."""
    bad = []
    for fy, r in IS.items():
        if not _close(r["revenue"] - r["cogs"], r["gross_profit"]):
            bad.append("%s revenue-cogs != gross profit" % fy)
        if not _close(r["pbt"] - r["tax"], r["pat"]):
            bad.append("%s pbt-tax != pat" % fy)
        if not _close(r["majority"] + r["nci"], r["pat"]):
            bad.append("%s majority+nci != pat" % fy)
    for fy, c in COST.items():
        tot = (c["raw"] + c["mfg_dep"] + c["amort"] + c["transport"]
               + c["overhead"] + c["rou"] + c["inv_change"])
        if not _close(tot, IS[fy]["cogs"]):
            bad.append("%s cost note %d != income statement %d"
                       % (fy, tot, IS[fy]["cogs"]))
    for fy, r in REV.items():
        tot = (r["local"] + r["export"] + r["svc_local"] + r["svc_export"]
               - r["discounts"])
        if not _close(tot, IS[fy]["revenue"]):
            bad.append("%s revenue note %d != income statement %d"
                       % (fy, tot, IS[fy]["revenue"]))
    for fy, o in OTHER.items():
        below = sum(v for k, v in o.items() if k != "src")
        pbt = IS[fy]["gross_profit"] - IS[fy]["ga"] + below
        if not _close(pbt, IS[fy]["pbt"], tol=3):
            bad.append("%s gross profit - G&A + other items = %d != pbt %d"
                       % (fy, pbt, IS[fy]["pbt"]))
    for fy, p in PHYS.items():
        if p.get("local") is not None and p.get("export") is not None:
            if abs(p["local"] + p["export"] - p["total"]) > 1.5:
                bad.append("%s local+export != total" % fy)
    for fy, p in PHYS.items():
        ce, ke = p.get("cement_export"), p.get("clinker_export")
        if ce is not None and ke is not None and p.get("export") is not None:
            if abs(ce + ke - p["export"]) > 1.5:
                bad.append("%s cement+clinker export != export" % fy)
    for tag, r in INTERIM.items():
        if not _close(r["revenue"] - r["cogs"], r["gross_profit"]):
            bad.append("%s revenue-cogs != gross profit" % tag)
        if not _close(r["pbt"] - r["tax"], r["pat"]):
            bad.append("%s pbt-tax != pat" % tag)
    return bad


# ---------------------------------------------------------------------------
# Derived series the drivers read.  Nothing here is typed; it is all computed
# from the footed panel above.
# ---------------------------------------------------------------------------
def volumes(fy):
    """local, export, total tonnes.  FY2021's local is the release's own
    residual (total less the stated export volume); FY2022's export likewise."""
    p = PHYS[fy]
    tot = p["total"]
    loc, exp = p.get("local"), p.get("export")
    if loc is None and exp is not None:
        loc = tot - exp
    if exp is None and loc is not None:
        exp = tot - loc
    return loc, exp, tot


def prices(fy):
    """Realised price per tonne by channel, DERIVED from the audited revenue
    note over the released tonnage — never from a deck's rev/ton, which is
    struck on a revenue figure the accounts do not print.

    Returns None where the year is on the gross revenue basis (B-13): a price
    per tonne struck on gross revenue and one struck on net revenue are two
    different objects, and this window's discounts ran to 19.6% of gross."""
    if REV[fy]["basis"] != "net":
        return None, None
    loc, exp, _ = volumes(fy)
    r = REV[fy]
    return (r["local"] / (loc * 1000.0) if loc else None,
            r["export"] / (exp * 1000.0) if exp else None)


def unit_costs(fy):
    """Raw materials, transport and overhead per tonne SOLD."""
    _, _, tot = volumes(fy)
    c = COST[fy]
    return (c["raw"] / (tot * 1000.0), c["transport"] / (tot * 1000.0),
            c["overhead"] / (tot * 1000.0))


def interest_bearing(fy):
    d = DEBT.get(fy)
    if not d:
        return None
    parts = [d["noncurrent"], d["current_portion"], d["credit_facilities"]]
    tot = sum(parts)
    assert abs(tot - d["total"]) <= 2, "%s borrowings components %d != total %d" % (fy, tot, d["total"])
    return d["total"]


def average_borrowings(fy):
    """The AVERAGE of the opening and closing interest-bearing balance.

    Not a refinement for its own sake.  ARCC repaid essentially its whole debt
    book during FY2023 — 701,655,075 at the start of the year and 90,074,273 at
    the end — so a rate struck on the CLOSING balance would read 85% for a
    company that borrows at around twenty, and one struck on the OPENING balance
    would read eleven.  Neither is the rate it paid.  The average is the only
    denominator that means the same thing in a year when the balance moved and
    in a year when it did not, and it is applied to every year alike.
    """
    prev = "FY%d" % (int(fy[2:]) - 1)
    a, b = interest_bearing(prev), interest_bearing(fy)
    if b is None:
        return None
    return b if a is None else (a + b) / 2.0


def borrowing_rate(fy):
    """Finance charge over the borrowings that ACTUALLY BEAR IT — never over a
    broader liabilities total.  Returns None where the panel cannot form it
    rather than widening the denominator until the answer looks sensible; that
    widening is the trap [R-FCAL-01] §3 names first and it manufactures a bias
    that is arithmetic, not evidence ([L-002])."""
    d = DEBT.get(fy)
    ib = average_borrowings(fy)
    if not d or not ib:
        return None
    # The charge is the INCOME STATEMENT's finance cost line — the same line the
    # projection reproduces — over the borrowings that actually bear it.  Using
    # the disclosed components instead would change definition between filings:
    # the pre-FY2022 layout does not split credit-facility interest out at all,
    # so a component-based rate would silently mean something different before
    # and after FY2022.  One definition, applied to every year.
    charge = -OTHER[fy]["finance_costs"]
    return charge / ib


_BAD = foot()
assert not _BAD, "ARCC panel does not foot:\n  " + "\n  ".join(_BAD)


if __name__ == "__main__":
    print("ARCC panel — %d fiscal years, FY2014..FY2025, all tier A" % len(IS))
    n = (len(IS) * 3 + len(COST) + len(REV) + len(OTHER) + len(INTERIM) * 2
         + sum(1 for p in PHYS.values() if p.get("local") is not None
               and p.get("export") is not None)
         + sum(1 for p in PHYS.values() if p.get("cement_export") is not None
               and p.get("clinker_export") is not None and p.get("export") is not None)
         + len(DEBT))
    print("footing: OK (%d identities checked)" % n)
    print()
    print("%-8s %14s %14s %8s %9s %9s %9s %9s" %
          ("year", "revenue", "cost of sales", "vol kt", "loc EGP/t", "exp EGP/t",
           "raw/t", "rate"))
    for fy in YEARS:
        loc, exp, tot = volumes(fy)
        pl, pe = prices(fy)
        rm, tr, ov = unit_costs(fy)
        rate = borrowing_rate(fy)
        print("%-8s %14d %14d %8.1f %9s %9s %9.0f %9s" %
              (fy, IS[fy]["revenue"], IS[fy]["cogs"], tot,
               "%.0f" % pl if pl else "-", "%.0f" % pe if pe else "-", rm,
               "%.2f%%" % (100 * rate) if rate else "-"))
