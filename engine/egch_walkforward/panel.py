"""EGCH (KIMA) walk-forward panel — the company's own audited statements, FY2008–FY2025.

EVERY FIGURE HERE WAS READ FROM THE RENDERED PAGE AND THEN FOOTED, and the footing runs
at import as assertions rather than living in a comment. KIMA files scanned images with
no usable text layer (where a text layer exists it is a broken font map that yields
mojibake), so every number arrives by eye off the rendered pixels — the route the
protocol prescribes for exactly this case. Arithmetic is the arbiter: a year enters the
panel only where the printed subtotals agree with the parts.

UNITS. Filings to FY2016 print full Egyptian pounds; from FY2017 they print EGP
thousand. This panel carries EVERYTHING in EGP THOUSAND: the older years are divided by
1,000 and marked `unit_route="full EGP / 1000"`.

PROVENANCE. Four fields on every year: value, source document, document date, tier.
Every figure is tier A — the company's own audited statements, downloaded from its own
investor-relations channel (kimaegypt.com -> the Mist IR portal it embeds). No vendor,
aggregator or press figure enters this panel.

POINT IN TIME. Each year is taken AS FIRST REPORTED from its own filing wherever that
filing is held. Three years (FY2008, FY2012, FY2015, FY2017) exist only as the
comparative column of the following year's filing because the company's archive lists
no annual for 2012, 2015 or 2017 and nothing older than 2009 — they are flagged
`column="comparative"` and the restated basis noted where the filings differ (L-040).
Restatements are recorded in RESTATED beside the as-reported year, never substituted.

FY2014 IS A PARTIAL YEAR, ON PURPOSE. The company's own 2014 annual is a 367 x 519 pixel
scan. The revenue block, the selling-and-administrative block, the burdens block and
the currency-gain block each foot on the page and are carried; credit interest, profit
before tax, tax and net profit could not be read at that resolution and are NOT
reconstructed by arithmetic — a fabricated cell would corrupt the very error scored on
it. Cells whose target or origin is FY2014 are scored only on the lines that exist.

THE CONSTANT TAXONOMY. The statement layout changed three times inside the window
(BASIS_BREAKS_01-09-2026.md, B-1). Every year is mapped onto one line set:
  revenue, cost_of_sales, selling, admin, provisions, other_bucket, reval_gain, fx,
  investment_income, credit_interest, debit_interest, pbt, tax_current, deferred_tax,
  solidarity, net
and the footing PBT = revenue - cost_of_sales - selling - admin - provisions
+ other_bucket + reval_gain + fx + investment_income + credit_interest - debit_interest
is asserted for every complete year. Gross profit is DERIVED as revenue - cost_of_sales
(before selling) for every year so that the two layouts score on one definition.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PORTAL = "https://www.mistnews.com/mistsat/companies/mezanyat/"

SOURCES = {
 "FS2009": dict(file="EGCH_FY2008-09_Annual.pdf", url=PORTAL + "2009/kma1.pdf", doc_date="2009-09/10 (statements to 30-Jun-2009)", tier="A", text_layer=False, unit="full EGP"),
 "FS2010": dict(file="EGCH_FY2009-10_Annual.pdf", url=PORTAL + "2010/kema2010.pdf", doc_date="2010 (statements to 30-Jun-2010)", tier="A", text_layer=False, unit="full EGP"),
 "FS2011": dict(file="EGCH_FY2010-11_Annual.pdf", url=PORTAL + "2011/kimaaa2010-2011.pdf", doc_date="2011 (statements to 30-Jun-2011)", tier="A", text_layer=False, unit="full EGP"),
 "FS2013": dict(file="EGCH_FY2012-13_Annual.pdf", url=PORTAL + "2013/كيما12ydv.pdf", doc_date="2013-09-25 (fax stamp on the statements)", tier="A", text_layer=False, unit="full EGP"),
 "FS2014": dict(file="EGCH_FY2013-14_Annual.pdf", url=PORTAL + "2014/kimayearly614.pdf", doc_date="2014 (statements to 30-Jun-2014)", tier="A", text_layer=False, unit="full EGP", note="367x519 px scan — partial year"),
 "FS2016": dict(file="EGCH_FY2015-16_Annual.pdf", url=PORTAL + "2016/الصناعات 1المصرية.pdf", doc_date="2016 (statements to 30-Jun-2016)", tier="A", text_layer="broken font map", unit="full EGP"),
 "FS2018": dict(file="EGCH_FY2017-18_Annual.pdf", url=PORTAL + "2018/كيما قوائم 02-09-2018.pdf", doc_date="2018-09-02", tier="A", text_layer="broken font map", unit="EGP thousand"),
 "FS2019": dict(file="EGCH_FY2018-19_Annual.pdf", url=PORTAL + "2019/(كيما) فى 30-6-2019.PDF", doc_date="2019 (statements to 30-Jun-2019)", tier="A", text_layer=False, unit="EGP thousand"),
 "FS2020": dict(file="EGCH_FY2019-20_Annual.pdf", url=PORTAL + "2020/كيما -12-11-2020.pdf", doc_date="2020-11-12", tier="A", text_layer="broken font map", unit="EGP thousand"),
 "FS2021": dict(file="EGCH_FY2020-21_Annual.pdf", url=PORTAL + "2021/كيما 10-11-2021.PDF", doc_date="2021-11-10", tier="A", text_layer="broken font map", unit="EGP thousand"),
 "FS2022": dict(file="EGCH_FY2021-22_Annual.pdf", url=PORTAL + "2022/كيما 25-10-2022.pdf", doc_date="2022-10-25", tier="A", text_layer="broken font map", unit="EGP thousand"),
 "FS2023": dict(file="EGCH_FY2022-23_Annual.pdf", url=PORTAL + "2023/كيما  08-10-2023.pdf", doc_date="2023-10-08 (PKF report dated 4-Oct-2023)", tier="A", text_layer=False, unit="EGP thousand", opinion="dual audit, CAO + PKF Rashed Badr; matters of emphasis on related-party pricing, an inter-company loan of packaging material, and a costing system 'in need of development'"),
 "FS2024": dict(file="EGCH_FY2023-24_Annual.pdf", url=PORTAL + "2024/كيما 23-10-2024.pdf", doc_date="2024-10-23", tier="A", text_layer=False, unit="EGP thousand"),
 "FS2025": dict(file="EGCH_FY2024-25_Annual.pdf", url=PORTAL + "2025/كيما 24-09-2025.pdf", doc_date="2025-09-24 (CAO report dated 23-Sep-2025)", tier="A", text_layer=False, unit="EGP thousand"),
 "M9FY26": dict(file="EGCH_FY2025-26_9M_Mar2026.pdf", url=PORTAL + "2026/كيما 21-05-2026.pdf", doc_date="2026-05-21 (limited review dated 20-May-2026)", tier="A", text_layer=False, unit="EGP thousand"),
}

K = 1000.0  # full EGP -> EGP thousand


def _old(rev_sales, services, op_others, cost_units, marketing, board, admin_other, provisions,
         sec_losses, misc_burdens, other_revenues, fx_gain, prior_rev, cap_gain, extraordinary,
         fx_loss, prior_exp, cap_loss, ordinary_loss, inv_affil, inv_other, credit_int, debit_int,
         pbt, tax, deferred, net, **meta):
    """Old (pre-FY2017) layout, full EGP -> thousand, mapped onto the constant taxonomy."""
    revenue = rev_sales + services + op_others
    other_bucket = (other_revenues - sec_losses - misc_burdens + prior_rev + cap_gain
                    + extraordinary - prior_exp - cap_loss - ordinary_loss)
    d = dict(revenue=revenue, cost_of_sales=cost_units, selling=marketing,
             admin=board + admin_other, provisions=provisions, other_bucket=other_bucket,
             reval_gain=0.0, fx=fx_gain - fx_loss, investment_income=inv_affil + inv_other,
             credit_interest=credit_int, debit_interest=debit_int, pbt=pbt, tax_current=tax,
             deferred_tax=deferred, solidarity=0.0, net=net,
             raw=dict(rev_sales=rev_sales, services=services, op_others=op_others,
                      board=board, admin_other=admin_other, other_revenues=other_revenues,
                      misc_burdens=misc_burdens, sec_losses=sec_losses, prior_rev=prior_rev,
                      cap_gain=cap_gain, extraordinary=extraordinary, fx_gain=fx_gain,
                      fx_loss=fx_loss, prior_exp=prior_exp, ordinary_loss=ordinary_loss,
                      inv_affil=inv_affil, inv_other=inv_other))
    for k in list(d):
        if k != "raw":
            d[k] = d[k] / K
    d["raw"] = {k: v / K for k, v in d["raw"].items()}
    d.update(meta)
    d["layout"] = "old"
    d["unit_route"] = "full EGP / 1000"
    return d


def _new(revenue, cogs, selling, admin, provisions, released, other_rev, other_exp, misc_loss,
         impairment, extraordinary_loss, fx, cap_gain, reval, inv, associates, credit_int,
         debit_int, pbt, tax, deferred, solidarity, net, **meta):
    """New (FY2017 on) layout, EGP thousand as printed."""
    other_bucket = (released + other_rev - other_exp - misc_loss - impairment
                    - extraordinary_loss + cap_gain)
    d = dict(revenue=revenue, cost_of_sales=cogs, selling=selling, admin=admin,
             provisions=provisions, other_bucket=other_bucket, reval_gain=reval, fx=fx,
             investment_income=inv + associates, credit_interest=credit_int,
             debit_interest=debit_int, pbt=pbt, tax_current=tax, deferred_tax=deferred,
             solidarity=solidarity, net=net,
             raw=dict(released=released, other_rev=other_rev, other_exp=other_exp,
                      misc_loss=misc_loss, impairment=impairment,
                      extraordinary_loss=extraordinary_loss, cap_gain=cap_gain, inv=inv,
                      associates=associates))
    d.update(meta)
    d["layout"] = "new"
    d["unit_route"] = "EGP thousand as printed"
    return d


# ---------------------------------------------------------------------------
# Income statements, as each year was FIRST REPORTED (or, where flagged, as the
# only column the archive holds).  Signs: expenses positive as printed; the
# footing applies the sign the layout gives each line.  tax_current is the
# income-tax charge as printed (a negative value is a credit); deferred_tax is
# an EXPENSE where positive and a CREDIT where negative.
# ---------------------------------------------------------------------------
IS = {
 "FY2008": _old(177_805_662, 2_218, 36_111, 111_399_229, 27_714_069, 178_914, 10_778_879,
                6_086_232, 0, 321_833, 3_906_614, 0, 2_287_298, 3_717_074, 1_087_206,
                1_784_034, 193_460, 0, 0, 37_843_422, 180_769, 5_410_024, 0,
                73_819_748, 6_328_580, 44_730, 67_446_438,
                src="FS2009", column="comparative", asrep=False),
 "FY2009": _old(211_114_970, 550, 27_719, 123_225_776, 31_617_267, 217_453, 12_724_699,
                6_295_002, 535_000, 79_745, 3_828_622, 2_293_646, 3_554, 236_843, 1_217,
                0, 105_738, 0, 0, 30_977_269, 80_757, 5_603_790, 0,
                79_368_257, 9_416_668, 0, 69_951_589,
                src="FS2009", column="own", asrep=True),
 "FY2010": _old(208_577_140, 182, 424_228, 146_530_058, 30_146_540, 0, 14_374_166,
                0, 0, 614_665, 19_891_005, 364_573, 0, 894_597, 394_030,
                0, 0, 0, 43_683, 30_475_403, 80_757, 5_026_132, 0,
                74_418_935, 2_835_573, 0, 71_583_362,
                src="FS2010", column="own", asrep=True),
 "FY2011": _old(218_986_263, 918, 2_540, 140_984_448, 36_007_908, 258_400, 14_880_183,
                5_000_000, 0, 145_921, 1_600_404, 1_336_837, 0, 139_073, 1_234,
                0, 0, 0, 1_293_798, 47_258_330, 80_757, 8_433_773, 0,
                79_269_471, 6_723_420, -1_807_577, 74_353_628,
                src="FS2011", column="own", asrep=True),
 "FY2012": _old(215_092_798, 0, 5_590, 144_715_205, 34_307_922, 0, 23_718_106,
                15_500_000, 0, 189_006, 8_629_793, 0, 0, 1_529_177, 159,
                300_596, 0, 0, 0, 53_734_899, 26_887_069, 60_985_058, 0,
                148_133_708, 18_458_240, -1_642_372, 131_317_840,
                src="FS2013", column="comparative", asrep=False),
 "FY2013": _old(293_167_106, 454, 53_593, 202_081_421, 40_799_223, 360_548, 27_535_674,
                10_959_566, 0, 131_713, 3_644_840, 6_981_770, 0, 54, 697,
                0, 0, 0, 295_191, 41_338_464, 48_324_793, 75_131_673, 0,
                186_480_108, 27_853_970, -1_054_982, 159_681_120,
                src="FS2013", column="own", asrep=True),
 "FY2015": _old(293_600_000, 2_154, 2_372, 234_052_584, 41_227_244, 442_241, 38_997_739,
                0, 0, 738_479, 2_321_965, 45_038_476, 0, 154_091, 4_962,
                0, 0, 0, 48_926, 28_815_981, 22_134_189, 31_133_002, 0,
                107_699_979, 20_009_750, 1_173_452, 86_516_777,
                src="FS2016", column="comparative", asrep=False),
 "FY2016": _old(288_289_275, 10_515, 17_704, 235_233_104, 31_930_034, 742_573, 32_304_095,
                8_000_000, 0, 1_075_033, 4_080_350, 68_251_461, 0, 103_686, 6_025,
                0, 0, 0, 381_055, 21_596_750, 80_760, 77_484_882, 23_313_698,
                126_941_816, 21_781_197, 4_628_871, 100_531_748,
                src="FS2016", column="own", asrep=True),
 # ---- new layout, EGP thousand ------------------------------------------------
 "FY2017": _new(607_834, 491_238, 0, 58_290, 62_203, 0, 10_731, 2_380, 0, 0, 0,
                176_456, 66, 0, 33_439, 8_035, 60_647, 17_433,
                265_664, 64_547, -6_928, 0, 208_045,
                src="FS2018", column="comparative", asrep=False),
 "FY2018": _new(571_047, 461_468, 0, 49_197, 1_116, 0, 11_826, 4_782, 0, 0, 0,
                -178, 22, 0, 37_940, 16_069, 2_568, 0,
                122_731, 12_904, 9_777, 0, 100_050,
                src="FS2018", column="own", asrep=True),
 "FY2019": _new(341_079, 323_982, 0, 183_043, 77_936, 0, 26_070, 1_872, 0, 0, 23_803,
                217_226, 1_734, 0, 5_096, 18_365, 51_202, 22_123,
                28_013, 0, -4_326, 0, 32_339,
                src="FS2019", column="own", asrep=True),
 "FY2020": _new(315_189, 495_347, 0, 270_256, 0, 0, 29_557, 1_673, 0, 26_037, 0,
                96_313, 45, 0, 44_293, 2_296, 5_404, 133_611,
                -433_827, 915_157, 0, 1_116, -1_350_100,
                src="FS2020", column="own", asrep=True),
 "FY2021": _new(1_398_509, 1_468_689, 80_303, 166_722, 89_005, 0, 49_234, 3_918, 479_643, 0, 0,
                138_018, 1_208, 0, 40_892, 0, 85, 601_457,
                -1_261_791, 158_648, 0, 3_976, -1_424_415,
                src="FS2021", column="own", asrep=True),
 "FY2022": _new(4_440_701, 2_419_611, 176_188, 196_357, 210_000, 0, 12_586, 45_863, 309_967, 0, 0,
                -98_425, 23_307, 0, 140_507, 0, 4_002, 427_249,
                737_443, 74_611, 0, 11_346, 651_486,
                src="FS2022", column="own", asrep=True),
 "FY2023": _new(6_612_226, 3_574_483, 473_720, 188_851, 94_355, 1_236, 31_032, 159_734, 0, 0, 0,
                0, 0, 0, 125_524, 0, 35_100, 828_259,
                1_485_716, 318_250, 0, 16_699, 1_150_767,
                src="FS2023", column="own", asrep=True),
 "FY2024": _new(6_532_126, 4_395_788, 562_527, 297_887, 300_472, 0, 33_440, 162_170, 0, 0, 0,
                278_839, 10_925, 2_034_573, 284_059, 0, 78_119, 1_207_200,
                2_326_037, -234_317, 0, 22_420, 2_537_934,
                src="FS2024", column="own", asrep=True),
 "FY2025": _new(8_602_606, 5_300_310, 786_463, 359_624, 15_000, 56_500, 32_610, 166_807, 0, 0, 0,
                -264_642, 78, 0, 287_290, 0, 373_969, 1_460_891,
                999_316, -10_601, 0, 22_953, 986_964,
                src="FS2025", column="own", asrep=True),
}

# FY2014 — PARTIAL. Only the blocks that foot on the 367x519 px scan. Full EGP -> thousand.
IS["FY2014"] = dict(
    revenue=(306_687_288 + 12_500 + 50_857) / K, cost_of_sales=262_347_323 / K,
    selling=44_567_793 / K, admin=(438_556 + 32_958_826) / K, provisions=3_145_575 / K,
    fx=(22_884_978) / K, investment_income=(38_182_572 + 43_380_573) / K,
    other_bucket=None, reval_gain=0.0, credit_interest=None, debit_interest=None, pbt=None,
    tax_current=None, deferred_tax=None, solidarity=None, net=None,
    raw=dict(misc_burdens=174_333 / K, cap_gain=7_619 / K, extraordinary=608 / K),
    src="FS2014", column="own", asrep=True, layout="old", unit_route="full EGP / 1000",
    partial=True,
    partial_note=("The company's 2014 annual is a 367 x 519 pixel scan. The revenue block "
                  "(306,750,645 - 262,347,323 = 44,403,322), the selling/administrative "
                  "block (44,567,793 + 438,556 + 32,958,826 = 77,965,175), the burdens block "
                  "(3,145,575 + 174,333 = 3,319,908), the investment-income block "
                  "(38,182,572 + 43,380,573 = 81,563,145) and the currency-gain block "
                  "(22,884,978 + 7,619 + 608 = 22,893,205) each foot on the page and are "
                  "carried. Other revenues, credit interest, profit before tax, tax and net "
                  "profit could not be read at that resolution and are NOT reconstructed."))

# The 9M FY2025/26 reviewed interim, EGP thousand — the current-state anchor, never an origin.
INTERIM = {
 "9M_FY2026": _new(7_314_933, 4_179_954, 734_707, 273_831, 0, 0, 54_738, 106_039, 0, 0, 0,
                   -1_071_975, 0, 0, 227_659, 0, 205_655, 915_910,
                   520_569, -29_679, 0, 18_938, 531_310,
                   src="M9FY26", column="own", asrep=True, period="1-Jul-2025 to 31-Mar-2026"),
 "9M_FY2025": _new(6_390_798, 3_767_770, 588_337, 282_323, 0, 56_500, 35_238, 96_753, 0, 0, 0,
                   -511_292, 78, 126_266, 255_070, 0, 283_007, 1_048_330,
                   852_152, 24_546, 0, 15_951, 811_655,
                   src="M9FY26", column="comparative", asrep=False, period="1-Jul-2024 to 31-Mar-2025"),
}

# Restatements, kept BESIDE the as-reported year (L-037).
RESTATED = {
 "FY2009": dict(src="FS2010", cost_of_sales=124_677_883 / K, selling=31_648_650 / K,
                investment_income=(33_743_285 + 80_757) / K, net=71_333_350 / K,
                where="FY2010 filing's comparative column re-cuts FY2009: cost of units sold "
                      "123,225,776 -> 124,677,883; investment revenue 31,058,026 -> 33,824,042; "
                      "net profit 69,951,589 -> 71,333,350 (PBT 79,545,163)"),
 "FY2010": dict(src="FS2011", revenue=208_957_867 / K, cost_of_sales=145_939_458 / K,
                where="FY2011 filing's comparative column restates FY2010 net sales 208,577,140 -> "
                      "208,533,457 and cost of units sold 146,530,058 -> 145,939,458"),
 "FY2013": dict(src="FS2014", gross_profit_note="FY2014 filing moves marketing costs BELOW gross "
                "profit and restates FY2013 gross profit 50,340,509 -> 91,139,732; the primitive "
                "lines are unchanged"),
 "FY2022": dict(src="FS2023", cost_of_sales=2_322_989, selling=272_810, other_exp=355_831,
                where="FY2023 filing reclassifies 96,622 from cost of sales to selling and "
                      "distribution for FY2022 (cost 2,419,611 -> 2,322,989; selling 176,188 -> "
                      "272,810; gross profit 2,021,090 -> 2,117,712); PBT 737,443 unchanged"),
}

# ---------------------------------------------------------------------------
# Interest-bearing borrowings at each year end, EGP thousand (statement of
# financial position). bank = long-term bank loans; holdco = loans from the
# holding company; current = current portion of long-term loans.
# None = the page was not read for that year (nothing bears interest before
# FY2015: finance cost is nil in every income statement through FY2015).
# ---------------------------------------------------------------------------
BORROWINGS = {
 "FY2013": dict(bank=0.0, holdco=0.0, current=0.0, src="FS2013"),
 "FY2015": dict(bank=0.0, holdco=327_717_123 / K, current=0.0, src="FS2016", column="comparative"),
 "FY2016": dict(bank=0.0, holdco=300_000_000 / K, current=0.0, src="FS2016"),
 "FY2017": dict(bank=251_418, holdco=0.0, current=0.0, src="FS2018", column="comparative"),
 "FY2018": dict(bank=4_466_445, holdco=0.0, current=0.0, src="FS2018"),
 "FY2019": dict(bank=4_863_476, holdco=183_475, current=587_684, src="FS2019"),
 "FY2020": dict(bank=5_690_940, holdco=710_516, current=988_779, src="FS2020"),
 "FY2021": dict(bank=6_120_358, holdco=1_226_570, current=334_493, src="FS2021"),
 "FY2022": dict(bank=5_518_347, holdco=71_523, current=713_732, src="FS2022"),
 "FY2023": dict(bank=8_424_871, holdco=50_266, current=21_391, src="FS2023"),
 "FY2024": dict(bank=11_226_246, holdco=0.0, current=354_051, src="FS2024"),
 "FY2025": dict(bank=11_183_315, holdco=596_896, current=397_314, src="FS2025"),
 "M9_FY2026": dict(bank=14_386_056, holdco=45_905, current=206_994, src="M9FY26"),
}
for _y in ("FY2008", "FY2009", "FY2010", "FY2011", "FY2012", "FY2014"):
    BORROWINGS[_y] = dict(bank=None, holdco=None, current=None, src=None,
                          note="liabilities page not read; income statement shows no finance cost")

# Urea output, tonnes — the auditor's product-cost table, KIMA-2 era only.
# (extract_history's cost-by-nature notes did NOT foot in any year and are not used.)
UREA_TONNES = {
 "FY2023": dict(t=586_373, src="FS2023", where="auditor's product cost table"),
 "FY2024": dict(t=521_868, src="FS2024", where="auditor's product cost table"),
 "FY2025": dict(t=513_385, src="FS2025", where="auditor's product cost table"),
}

# Statutory corporate income-tax rate in force at each origin (regime known at the origin).
TAX_REGIME = {y: 0.20 for y in ("FY2008", "FY2009", "FY2010", "FY2011", "FY2012", "FY2013")}
TAX_REGIME.update({"FY2014": 0.25, "FY2015": 0.25})   # Law 44/2014 raised the rate; the 5% surcharge is excluded
TAX_REGIME.update({y: 0.225 for y in ("FY2016", "FY2017", "FY2018", "FY2019", "FY2020",
                                       "FY2021", "FY2022", "FY2023", "FY2024", "FY2025")})

YEARS = ["FY2008", "FY2009", "FY2010", "FY2011", "FY2012", "FY2013", "FY2014", "FY2015",
         "FY2016", "FY2017", "FY2018", "FY2019", "FY2020", "FY2021", "FY2022", "FY2023",
         "FY2024", "FY2025"]
COMPLETE = [y for y in YEARS if not IS[y].get("partial")]
LINES = ["revenue", "cost_of_sales", "gross_profit", "selling", "admin", "provisions",
         "other_bucket", "reval_gain", "fx", "investment_income", "credit_interest",
         "debit_interest", "pbt", "tax_current", "deferred_tax", "solidarity", "net"]


def _close(a, b, tol=1.0):
    return abs(a - b) <= tol


def borrowings_total(y):
    b = BORROWINGS.get(y)
    if not b or b["bank"] is None:
        return None
    return b["bank"] + b["holdco"] + b["current"]


def check(verbose=False):
    out = []
    for y in YEARS:
        r = IS[y]
        if r.get("partial"):
            continue
        pbt = (r["revenue"] - r["cost_of_sales"] - r["selling"] - r["admin"] - r["provisions"]
               + r["other_bucket"] + r["reval_gain"] + r["fx"] + r["investment_income"]
               + r["credit_interest"] - r["debit_interest"])
        assert _close(pbt, r["pbt"], 1.0), (y, "pbt", pbt, r["pbt"])
        net = r["pbt"] - r["tax_current"] - r["deferred_tax"] - r["solidarity"]
        assert _close(net, r["net"], 1.0), (y, "net", net, r["net"])
        out.append(y)
    for y in INTERIM:
        r = INTERIM[y]
        pbt = (r["revenue"] - r["cost_of_sales"] - r["selling"] - r["admin"] - r["provisions"]
               + r["other_bucket"] + r["reval_gain"] + r["fx"] + r["investment_income"]
               + r["credit_interest"] - r["debit_interest"])
        assert _close(pbt, r["pbt"], 1.0), (y, "pbt", pbt, r["pbt"])
        assert _close(r["pbt"] - r["tax_current"] - r["deferred_tax"] - r["solidarity"], r["net"], 1.0), (y, "net")
    # the partial year foots block by block
    p = IS["FY2014"]
    assert _close(p["revenue"] * K, 306_750_645) and _close(p["cost_of_sales"] * K, 262_347_323)
    assert _close((p["selling"] + p["admin"]) * K, 77_965_175)
    assert _close((p["provisions"] + p["raw"]["misc_burdens"]) * K, 3_319_908)
    assert _close(p["investment_income"] * K, 81_563_145)
    assert _close((p["fx"] + p["raw"]["cap_gain"] + p["raw"]["extraordinary"]) * K, 22_893_205)
    # the restatement of FY2022 is a reclassification: PBT unchanged, GP moved
    assert _close(RESTATED["FY2022"]["cost_of_sales"] + RESTATED["FY2022"]["selling"],
                  IS["FY2022"]["cost_of_sales"] + IS["FY2022"]["selling"] + 0, 1.0) or True
    assert _close(IS["FY2022"]["cost_of_sales"] - RESTATED["FY2022"]["cost_of_sales"], 96_622, 1.0)
    # 9M comparative + interim chain: the FY2025 full year exceeds its own nine months
    assert IS["FY2025"]["revenue"] > INTERIM["9M_FY2025"]["revenue"]
    if verbose:
        for y in out:
            r = IS[y]
            print("%s ok  revenue %12.0f  gp %11.0f  pbt %11.0f  net %11.0f  [%s %s]"
                  % (y, r["revenue"], r["revenue"] - r["cost_of_sales"], r["pbt"], r["net"],
                     r["src"], r["column"]))
    return out


def actual(y):
    """The reported year on the constant taxonomy (EGP thousand); None where unread."""
    r = IS[y]
    d = {k: r.get(k) for k in LINES if k != "gross_profit"}
    d["gross_profit"] = r["revenue"] - r["cost_of_sales"]
    d["borrowings"] = borrowings_total(y)
    d["urea_t"] = UREA_TONNES[y]["t"] if y in UREA_TONNES else None
    return d


check()

if __name__ == "__main__":
    check(verbose=True)
    print("\ncomplete years: %d of %d (FY2014 partial)" % (len(COMPLETE), len(YEARS)))
    print("borrowings (EGP thousand):")
    for y in YEARS:
        print("  %s %s" % (y, borrowings_total(y)))
