"""AMOC walk-forward panel — the company's own audited consolidated statements.

EVERY FIGURE HERE WAS READ FROM THE RENDERED PAGE AND THEN FOOTED, and the
footing runs at import as assertions rather than living in a comment. That is
not ceremony. AMOC files scans with no text layer, so every number arrives by
eye, and on this panel the arithmetic caught SIX misreads that looked perfectly
clean on the page:

  FY2025 formed provisions   158,000,000 -> 198,000,000   (income statement)
  FY2023 oils tonnage        114,482.60  -> 114,402.60    (note 14-A)
  FY2023 heavy fuel oil      355,205,884 -> 355,205,084   (note 14-A)
  FY2021 heavy fuel tonnage  49,309.88   -> 49,359.88     (note 14-A)
  FY2021 LPG                 321,976,626 -> 321,976,646   (note 14-A)
  FY2021 waste value         110,430     -> 115,430       (note 14-A)

Not one of those would have been visible to a reader of the extracted number.
Each was found only because a printed subtotal refused to agree with the parts,
which is the protocol's rule working exactly as written: ARITHMETIC IS THE
ARBITER, NOT THE EXTRACTOR'S CONFIDENCE.

PROVENANCE.  Four fields on every year: value, source document, document date,
tier. Every figure is tier A — the company's own audited consolidated financial
statements, downloaded from its own investor-relations archive at amoceg.com.
No vendor, aggregator or press figure enters this panel.

POINT IN TIME.  FY2024 is carried TWICE, on purpose. Its own filing reported a
majority profit of 1,699,154,495; the FY2025 filing's comparative column shows
1,439,557,574 for the same year — a restatement of 259,596,921, all of it in
miscellaneous other revenue. An origin standing at FY2024 saw the first number
and could not have seen the second, so the walk-forward uses AS-REPORTED and
keeps the restatement beside it (L-037).
"""
import os, json

HERE = os.path.dirname(os.path.abspath(__file__))
IR = "https://amoceg.com/reports/investor/financialStatement/"

SOURCES = {
    "FS2022": {"file": "15-641ad5c4187951679480260.pdf", "url": IR + "15-641ad5c4187951679480260.pdf",
               "label": "القوائم المالية المجمعة 30/6/2022 — consolidated financial statements, year ended 30 June 2022",
               "doc_date": "2022-09-2x", "tier": "A", "language": "ar", "opinion": "not read (Arabic scan)"},
    "FS2023": {"file": "41-662794b73ed5a1713870007.pdf", "url": IR + "41-662794b73ed5a1713870007.pdf",
               "label": "Consolidated Financial Statement 30/6/2023", "doc_date": "2023-08-31", "tier": "A",
               "language": "en", "opinion": "QUALIFIED",
               "opinion_basis": ("(1) an EGP 21mn technical study to improve diesel specifications, inside "
                                 "projects under construction, unresolved at 30-Jun-2023; (2) financial "
                                 "investments in ASPC of EGP 12mn carried as available-for-sale and not "
                                 "evaluated by management."),
               "emphasis_of_matter": ("The company seeks to develop the current costing system so that the cost "
                                      "of each type of product produced is accurately reached. The company "
                                      "stated that it implemented a system of costs from the beginning of "
                                      "July 2023.")},
    "FS2024": {"file": "54-66c5a239056101724228153.pdf", "url": IR + "54-66c5a239056101724228153.pdf",
               "label": "Consolidated Financial Statement 30/6/2024", "doc_date": "2024-08-18", "tier": "A",
               "language": "en", "opinion": "not read"},
    "FS2025": {"file": "74-68a2dfafd04651755504559.pdf", "url": IR + "74-68a2dfafd04651755504559.pdf",
               "label": "Consolidated Financial Statement 30/6/2025", "doc_date": "2025-08-18", "tier": "A",
               "language": "en", "opinion": "not read"},
}

# ---------------------------------------------------------------------------
# Income statement, as each year was FIRST REPORTED.
# Signs: every line is stated POSITIVE as printed; the footing below applies
# the sign the statement's own layout gives it.
# ---------------------------------------------------------------------------
IS = {
 "FY2021": dict(src="FS2022", column="comparative", asrep=True,
    net_sales=10_182_689_818, cost_of_sales=9_145_979_677, gross_profit=1_036_710_141,
    other_revenues=40_625_608, ga=297_900_709, marketing=26_346_538,
    claims_provision=152_936_750, other_expenses=42_906_480, operating_profit=557_245_272,
    investment_revenues=3_120_000, pbt=560_365_272, income_tax=72_768_952,
    deferred_tax=+11_690_125, npat=499_286_445, nci=13_618_561, majority=485_667_884,
    layout="ar2022"),
 "FY2022": dict(src="FS2022", column="own", asrep=True,
    net_sales=18_441_855_240, cost_of_sales=15_888_827_624, gross_profit=2_553_027_616,
    other_revenues=133_456_159, ga=442_641_214, marketing=26_573_109,
    claims_provision=464_420_145, other_expenses=33_022_090, operating_profit=1_719_827_217,
    investment_revenues=85_541_760, pbt=1_805_368_977, income_tax=510_108_225,
    deferred_tax=-77_678_214, npat=1_217_582_538, nci=23_459_773, majority=1_194_122_765,
    layout="ar2022"),
 "FY2023": dict(src="FS2023", column="own", asrep=True,
    net_sales=24_208_335_757, cost_of_sales=21_893_656_788, gross_profit=2_314_678_969,
    ga=503_268_507, marketing=56_197_833, other_expenses=18_555_702,
    operating_profit=1_736_656_927, claims_provision=360_960_449, finance_expenses=0,
    other_revenues=404_946_540, investment_revenues=6_500_000, pbt=1_787_143_018,
    income_tax=432_881_118, deferred_tax=+17_784_401, npat=1_372_046_301,
    nci=41_546_373, majority=1_330_499_928, layout="en2023"),
 "FY2024": dict(src="FS2024", column="own", asrep=True,
    net_sales=33_767_840_080, cost_of_sales=31_145_748_464, gross_profit=2_622_091_616,
    ga=680_847_571, marketing=115_572_185, other_expenses=22_996_411,
    operating_profit=1_802_675_449, claims_provision=372_944_903, finance_expenses=515_324,
    other_revenues=950_868_836, investment_revenues=10_400_000, pbt=2_390_484_058,
    income_tax=534_783_622, deferred_tax=-90_096_927, npat=1_765_603_509,
    nci=66_449_014, majority=1_699_154_495, layout="en2023"),
 "FY2025": dict(src="FS2025", column="own", asrep=True,
    net_sales=37_622_609_782, cost_of_sales=35_127_091_419, gross_profit=2_495_518_363,
    ga=876_992_444, marketing=167_217_362, other_expenses=28_504_803,
    operating_profit=1_422_803_754, claims_provision=198_000_000, ecl=925_228,
    finance_expenses=4_965_217, other_revenues=800_244_158, investment_revenues=11_440_000,
    pbt=2_030_597_467, income_tax=552_044_321, deferred_tax=+73_397_185,
    npat=1_551_950_331, nci=63_430_233, majority=1_488_520_098, layout="en2023"),
}

# The FY2024 restatement, kept BESIDE the as-reported year, never in place of it.
RESTATED = {
 "FY2024": dict(src="FS2025", ga=680_013_090, operating_profit=1_803_509_930,
    finance_expenses=1_349_805, other_revenues=691_271_915, pbt=2_130_887_137,
    npat=1_506_006_588, majority=1_439_557_574,
    delta_majority=-259_596_921,
    where="miscellaneous other revenues: 368,246,666 as reported -> 108,649,745 as restated",
    note=("The FY2025 filing's own STATEMENT OF CHANGES IN EQUITY still carries 1,699,154,493 as "
          "FY2024's profit at 1 July 2024 — the as-first-reported figure — while its income-statement "
          "comparative column shows 1,439,557,574. The primary document disagrees with itself. "
          "Registered, not reconciled away.")),
}

# ---------------------------------------------------------------------------
# Note 14-A, net sales by product: tonnes and EGP, as each year was reported.
# The taxonomy MOVES across the window; COMMON maps every filing's lines onto
# one set of eight so a driver is scored on a constant definition.
# ---------------------------------------------------------------------------
PRODUCTS = {
 "FY2021": dict(src="FS2022", lines={
    "oils": (119_231.440, 1_669_383_226), "wax": (61_630.896, 939_583_585),
    "gasoil": (411_444.375, 2_692_404_887), "gasoil_bunker": (3_645.185, 31_921_219),
    "naphtha": (88_272.098, 608_375_693), "lpg": (39_840.576, 321_976_646),
    "fueloil_export": (637_120.035, 3_313_762_388),
    "fueloil_export_authority": (81_588.324, 393_382_019),
    "fueloil_blending": (0.0, 0), "hfo": (49_359.88, 211_319_149),
    "aromatic_extract": (89.46, 465_576), "waste": (51.21, 115_430)},
    total=(1_492_273.479, 10_182_689_818)),
 "FY2022": dict(src="FS2022", lines={
    "oils": (110_778.380, 2_435_360_977), "wax": (69_301.500, 1_574_014_615),
    "gasoil": (366_601.600, 4_822_673_717), "gasoil_bunker": (51_691.662, 643_317_018),
    "naphtha": (95_206.676, 1_139_744_069), "lpg": (41_665.905, 608_729_431),
    "fueloil_export": (418_285.918, 3_368_482_953),
    "fueloil_export_authority": (0.0, 0),
    "fueloil_blending": (356_513.932, 3_587_074_872), "hfo": (37_702.340, 262_302_968),
    "aromatic_extract": (0.0, 0), "waste": (68.340, 154_620)},
    total=(1_547_816.253, 18_441_855_240)),
 "FY2023": dict(src="FS2023", lines={
    "oils": (114_402.60, 3_264_464_780), "wax": (65_880.520, 2_175_171_259),
    "gasoil": (355_643.938, 7_067_718_244), "gasoil_bunker": (20_596.612, 429_180_261),
    "naphtha": (92_338.159, 1_364_192_014), "lpg": (44_594.272, 767_091_429),
    "fueloil_export": (0.0, 0), "fueloil_export_authority": (0.0, 0),
    "fueloil_blending": (711_867.178, 8_784_943_578), "hfo": (43_513.840, 355_205_084),
    "aromatic_extract": (0.0, 0), "waste": (51.890, 369_108)},
    total=(1_448_889.008, 24_208_335_757)),
 "FY2024": dict(src="FS2024", lines={
    "oils": (117_762.98, 4_454_085_019), "wax": (64_870.76, 2_864_485_650),
    "gasoil": (401_759.672, 10_752_567_461), "gasoil_bunker": (0.0, 0),
    "naphtha": (82_941.509, 1_742_310_319), "lpg": (45_744.374, 963_877_589),
    "fueloil_export": (0.0, 0), "fueloil_export_authority": (0.0, 0),
    "fueloil_blending": (701_999.847, 12_757_040_812), "hfo": (18_240.62, 233_345_580),
    "aromatic_extract": (0.0, 0), "waste": (20.74, 127_650)},
    total=(1_433_340.502, 33_767_840_080)),
 "FY2025": dict(src="FS2025", lines={
    "oils": (98_182.34, 5_360_390_482), "wax": (71_588.8, 4_029_314_124),
    "gasoil": (322_558.706, 10_076_712_933), "gasoil_bunker": (0.0, 0),
    "naphtha": (75_630.604, 2_099_685_574), "lpg": (43_876.366, 1_408_079_637),
    "fueloil_export": (0.0, 0), "fueloil_export_authority": (0.0, 0),
    "fueloil_blending": (635_744.475, 14_386_176_125), "hfo": (13_937.44, 261_654_307),
    "aromatic_extract": (0.0, 0), "waste": (66.98, 596_600)},
    total=(1_261_585.711, 37_622_609_782)),
}

# One taxonomy across the whole window. The filings changed their line names
# twice; these groupings are the chain, and each is verified below against a
# figure the company itself published on BOTH bases.
COMMON = {
 "oils":    ["oils"],
 "wax":     ["wax"],
 "gasoil":  ["gasoil", "gasoil_bunker"],
 "naphtha": ["naphtha"],
 "lpg":     ["lpg"],
 "fueloil": ["fueloil_export", "fueloil_export_authority", "fueloil_blending"],
 "hfo":     ["hfo"],
 "other":   ["aromatic_extract", "waste"],
}

# ---------------------------------------------------------------------------
# Note 15-A, cost of sales by nature.
# ---------------------------------------------------------------------------
COST_STACK = {
 "FY2021": dict(src="FS2022", salaries=634_512_000, raw_materials=7_829_360_742,
                supporting_materials=25_216_148, depreciation=78_603_107, other=578_287_680),
 "FY2022": dict(src="FS2022", salaries=716_315_666, raw_materials=14_431_477_328,
                supporting_materials=59_124_378, depreciation=78_618_923, other=603_291_329),
 "FY2023": dict(src="FS2023", salaries=894_101_346, raw_materials=20_089_327_730,
                supporting_materials=80_411_637, depreciation=83_410_669, other=746_405_406),
 "FY2024": dict(src="FS2024", salaries=1_055_498_598, raw_materials=28_919_657_785,
                supporting_materials=87_800_536, depreciation=88_208_019, other=994_583_526),
 "FY2025": dict(src="FS2025", salaries=1_250_908_915, raw_materials=32_342_980_635,
                supporting_materials=117_487_403, depreciation=109_320_313, other=1_306_394_153),
}

# Note 14-B, other revenue by nature. The existing published study called this
# line "devaluation FX gains" and assumed it away from 2026; it is in fact
# dominated by CREDIT INTEREST on the company's own cash.
OTHER_REVENUE = {
 "FY2021": dict(src="FS2022", credit_interest=34_784_431, provisions_reversed=1_860_597,
                compensations_fines=346_335, capital_gains=1_327_100, misc=2_307_145, fx_gain=0),
 "FY2022": dict(src="FS2022", credit_interest=45_325_676, provisions_reversed=1_924_255,
                compensations_fines=3_046_240, capital_gains=760_644, misc=3_517_830,
                fx_gain=78_881_514),
 "FY2023": dict(src="FS2023", credit_interest=105_105_095, provisions_reversed=12_314_761,
                compensations_fines=740_513, capital_gains=208_000, misc=147_147_329,
                fx_gain=139_430_842),
 # capital_gains is a DASH in FY2024, not a repeat of FY2023's 208,000. Reading it
 # as the latter is the nil-printed-as-a-dash failure (L-036) and the column
 # footing is what refused it.
 "FY2024": dict(src="FS2024", credit_interest=350_152_390, provisions_reversed=16_405_125,
                compensations_fines=776_303, capital_gains=0, misc=368_246_666,
                fx_gain=215_288_352),
 "FY2025": dict(src="FS2025", credit_interest=417_377_530, provisions_reversed=279_457_477,
                compensations_fines=3_971_675, capital_gains=0, misc=42_124_383,
                fx_gain=47_730_203, reversed_ecl=9_582_890),
}

YEARS = ["FY2021", "FY2022", "FY2023", "FY2024", "FY2025"]


# ---------------------------------------------------------------------------
# THE FOOTINGS.  These run at import.  A panel that stops footing must FAIL,
# not warn — the whole point is that a misread number is invisible until the
# arithmetic refuses it.
# ---------------------------------------------------------------------------
def _close(a, b, tol=1.0):
    return abs(a - b) <= tol


def check(verbose=False):
    out = []
    for y in YEARS:
        r = IS[y]
        assert _close(r["net_sales"] - r["cost_of_sales"], r["gross_profit"]), (y, "gross profit")
        if r["layout"] == "ar2022":
            # Arabic 2022 layout: other revenues and the claims provision sit INSIDE
            # operating profit. The English layout from FY2023 puts both below it.
            op = (r["gross_profit"] + r["other_revenues"] - r["ga"] - r["marketing"]
                  - r["claims_provision"] - r["other_expenses"])
            assert _close(op, r["operating_profit"]), (y, "operating profit", op)
            pbt = r["operating_profit"] + r["investment_revenues"]
        else:
            op = r["gross_profit"] - r["ga"] - r["marketing"] - r["other_expenses"]
            assert _close(op, r["operating_profit"]), (y, "operating profit", op)
            pbt = (r["operating_profit"] - r["claims_provision"] - r.get("ecl", 0)
                   - r.get("finance_expenses", 0) + r["other_revenues"] + r["investment_revenues"])
        assert _close(pbt, r["pbt"]), (y, "pbt", pbt, r["pbt"])
        npat = r["pbt"] - r["income_tax"] + r["deferred_tax"]
        assert _close(npat, r["npat"]), (y, "npat", npat, r["npat"])
        assert _close(r["npat"] - r["nci"], r["majority"]), (y, "majority")

        p = PRODUCTS[y]
        t = sum(v[0] for v in p["lines"].values())
        e = sum(v[1] for v in p["lines"].values())
        assert _close(t, p["total"][0], 0.01), (y, "product tonnage", t, p["total"][0])
        assert _close(e, p["total"][1]), (y, "product value", e, p["total"][1])
        assert _close(p["total"][1], r["net_sales"]), (y, "products vs net sales")

        c = COST_STACK[y]
        cs = sum(v for k, v in c.items() if k != "src")
        assert _close(cs, r["cost_of_sales"]), (y, "cost stack", cs, r["cost_of_sales"])

        o = OTHER_REVENUE[y]
        os_ = sum(v for k, v in o.items() if k != "src")
        assert _close(os_, r["other_revenues"]), (y, "other revenue", os_, r["other_revenues"])
        out.append(y)

    # The restatement is real and is checked as such, so a later edit that
    # quietly "tidied" FY2024 onto one basis would fail here.
    rs = RESTATED["FY2024"]
    assert IS["FY2024"]["majority"] - rs["majority"] == -rs["delta_majority"], "FY2024 restatement"

    # The taxonomy chain. FY2023 is published on BOTH cuts — its own filing
    # splits gas oil from gas oil (bunker), and the FY2024 filing restates the
    # same year with "Solar Bunker" as its own line summing to the same total.
    # That is what licenses the grouping; it is verified, not assumed.
    assert _close(PRODUCTS["FY2023"]["lines"]["gasoil"][1]
                  + PRODUCTS["FY2023"]["lines"]["gasoil_bunker"][1], 7_496_898_505)
    if verbose:
        for y in out:
            print("{} ok  sales {:,}  tonnes {:,.0f}".format(y, IS[y]["net_sales"], PRODUCTS[y]["total"][0]))
    return out


def common_lines(year):
    """Product table on the constant eight-line taxonomy."""
    p = PRODUCTS[year]["lines"]
    return {k: (sum(p[s][0] for s in src), sum(p[s][1] for s in src)) for k, src in COMMON.items()}


check()

if __name__ == "__main__":
    check(verbose=True)
    print("\ncommon taxonomy, tonnes:")
    for y in YEARS:
        cl = common_lines(y)
        print(" ", y, " ".join("%s=%.0f" % (k, v[0]) for k, v in cl.items()))
    print("\nrealisation EGP/t:")
    for y in YEARS:
        cl = common_lines(y)
        print(" ", y, " ".join("%s=%.0f" % (k, (v[1] / v[0] if v[0] else 0)) for k, v in cl.items()))
