#!/usr/bin/env python3
"""SCEM (Sinai Cement Company S.A.E., EGX) — the walk-forward panel.

EVERY FIGURE IS THE COMPANY'S OWN AUDITED STATEMENT, READ OFF THE RENDERED PIXELS.
No vendor, aggregator or press figure enters this panel, and that sentence is the
whole reason this run exists: the first two editions of the SCEM study took revenue,
profit and the balance sheet from Global Cement, cemnet, Daily News Egypt, Arab
Finance and an aggregator's carry of S&P Global Market Intelligence while six audited
PDFs sat one click from sinaicement.com's homepage. SIGCM clause 1 has forbidden that
since July 2026.

ROUTE. All six filings are image-only scans — pdftotext returns 30 to 37 characters
for documents of 30 to 36 pages — so every number here arrives by OCR off the page
image at 150dpi grayscale, and the route is recorded per [R-FCAL-01]. ARITHMETIC IS
THE ARBITER, NOT THE EXTRACTOR'S CONFIDENCE: verify() below runs the footings the
filings themselves print, at import, and a misread digit breaks one of them.

WHAT THE ARITHMETIC ALREADY CAUGHT ON THIS PANEL, both invisible on the page:
  FY2022 short-term loans from affiliated companies   960,000,000 -> 950,000,000
      (the FY2022 filing's own current-liabilities subtotal refuses the first
       reading; the FY2023 filing's comparative column prints 950,000,000)
  FY2021 deferred tax                                  11,761,441 -> 11,751,441
      (the cash-flow statement and the income statement disagree by 10,000 and only
       one of them closes profit before tax to profit after tax)

SPAN AND WHY IT STOPS THERE. Five fiscal years, FY2021 to FY2025, plus the reviewed
quarter to 31 March 2026. The archive stops at FY2021 because the company publishes
exactly six documents and the oldest, SCC-AFS-A-1221, is ARABIC — and its figures are
in Eastern Arabic numerals which the OCR renders as letters, so FY2020's comparative
column cannot be read by any route available here. It is left out and the window is
shortened rather than filled from a vendor: a fabricated cell corrupts the very error
this run scores. The attempt is logged in fetch_attempts.json.

POINT IN TIME. Each year is carried AS FIRST REPORTED, from the filing in which it
was the current year, with the later filing's comparative column used only as a
cross-check. Where the two disagree the disagreement is recorded, never substituted.
"""
import os
import json

HERE = os.path.dirname(os.path.abspath(__file__))
IR = "https://sinaicement.com/wp-content/uploads/"

SOURCES = {
    "AFS2021_AR": {"file": "SCC-AFS-A-1221.pdf", "url": IR + "2025/05/SCC-AFS-A-1221.pdf",
                   "label": "Audited financial statements, year ended 31 December 2021 (ARABIC)",
                   "doc_date": "2022", "tier": "A", "language": "ar",
                   "route": "OCR attempted at 200dpi with the Arabic model; the figures are "
                            "Eastern Arabic numerals and render as letters. NOT USED."},
    "AFS2022": {"file": "SCC-AFS-E-1222.pdf", "url": IR + "2025/05/SCC-AFS-E-1222.pdf",
                "label": "Audited financial statements, year ended 31 December 2022",
                "doc_date": "2023", "tier": "A", "language": "en",
                "route": "OCR off the rendered pixels, 150dpi grayscale (tesseract, eng)"},
    "AFS2023": {"file": "SCC-AFS-E-1223.pdf", "url": IR + "2025/05/SCC-AFS-E-1223.pdf",
                "label": "Audited financial statements, year ended 31 December 2023",
                "doc_date": "2024", "tier": "A", "language": "en",
                "route": "OCR off the rendered pixels, 150dpi grayscale (tesseract, eng)"},
    "AFS2024": {"file": "SCC-AFS-E-1224.pdf", "url": IR + "2025/05/SCC-AFS-E-1224.pdf",
                "label": "Audited financial statements, year ended 31 December 2024",
                "doc_date": "2025-03", "tier": "A", "language": "en",
                "route": "OCR off the rendered pixels"},
    "AFS2025": {"file": "SCC-AFS-E-1225.pdf", "url": IR + "2026/06/SCC-AFS-E-1225.pdf",
                "label": "Audited financial statements, year ended 31 December 2025",
                "doc_date": "2026-03", "tier": "A", "language": "en",
                "route": "OCR off the rendered pixels"},
    "REV2026Q1": {"file": "SCC-AFS-E-0326.pdf", "url": IR + "2026/06/SCC-AFS-E-0326.pdf",
                  "label": "Reviewed interim statements, three months ended 31 March 2026",
                  "doc_date": "2026-05-11", "tier": "A", "language": "en",
                  "route": "OCR off the rendered pixels"},
}

# ---------------------------------------------------------------------------
# INCOME STATEMENT, as first reported. Every line POSITIVE as printed; the
# footings below apply the sign the statement's own layout gives it.
# The FY2021-FY2023 layout carries FINANCE EXPENSE INSIDE total expenses, so the
# printed "operating" line is AFTER interest. FY2024-FY2025 keep that layout.
# ---------------------------------------------------------------------------
IS = {
 "FY2021": dict(src="AFS2022", column="comparative", page="pdf p6, income statement",
    sales=1_443_444_954, cogs=1_384_202_744, gross=59_242_210,
    selling=188_188_799, ga=79_645_260, finance=158_114_423, ecl=-7_875,
    provisions=37_297_924, total_expenses=463_238_531, operating=-403_996_321,
    interest_income=38_466_788, capital_gains=-39_871, other_income=258_916,
    fx=8_561_979, below=47_247_812, pbt=-356_748_509,
    deferred_tax=+11_751_441, income_tax=0, pat=-344_997_068, eps=-5.07),
 "FY2022": dict(src="AFS2022", column="own", page="pdf p6, income statement",
    sales=2_343_242_231, cogs=2_194_089_033, gross=149_153_198,
    selling=133_554_330, ga=104_416_786, finance=183_953_231, ecl=-3_367_972,
    provisions=29_247_942, total_expenses=447_804_317, operating=-298_651_119,
    interest_income=13_085_088, capital_gains=187_727, other_income=162_292,
    fx=-43_333_798, below=-29_898_691, pbt=-328_549_810,
    deferred_tax=+8_748_840, income_tax=0, pat=-319_800_970, eps=-2.40),
 "FY2023": dict(src="AFS2023", column="own", page="pdf p6, income statement",
    sales=4_285_470_153, cogs=3_364_587_755, gross=920_882_398,
    selling=556_987_405, ga=162_657_891, finance=275_591_963, ecl=-534_336,
    provisions=5_445_046, total_expenses=1_000_147_969, operating=-79_265_571,
    interest_income=6_973_315, capital_gains=-210, other_income=227_856,
    fx=-38_044_366, below=-30_843_405, pbt=-110_108_976,
    deferred_tax=-7_472_636, income_tax=0, pat=-117_581_612, eps=-0.88),
 # FY2024 and FY2025 are the figures scem_study/filings_extract.py already committed
 # and footed off the same filings; they are repeated here so this panel stands alone,
 # and cross_check_study() asserts the two agree rather than trusting that they do.
 "FY2024": dict(src="AFS2024", column="own", page="pdf p3, income statement",
    sales=6_428_011_851, cogs=3_775_018_888, gross=2_652_992_963,
    selling=765_354_606, ga=355_437_994, finance=194_386_055, ecl=0,
    provisions=37_487_827, total_expenses=1_352_666_482, operating=1_300_326_481,
    interest_income=29_990_318, gain_on_sale_of_investments=1_517_386_642,
    below=1_849_710_004, pbt=3_150_036_485,
    deferred_tax=0, income_tax=77_674_674, pat=3_072_361_811, eps=23.09),
 "FY2025": dict(src="AFS2025", column="own", page="pdf p3, income statement",
    sales=9_089_149_688, cogs=4_632_038_855, gross=4_457_110_833,
    selling=791_121_463, ga=361_535_405, finance=28_517_057, ecl=0,
    provisions=-28_192_283, total_expenses=1_152_981_642, operating=3_304_129_191,
    interest_income=171_609_009, below=54_736_081, pbt=3_358_865_272,
    deferred_tax=0, income_tax=1_074_326_268, pat=2_284_539_004, eps=10.29),
}

# ---------------------------------------------------------------------------
# BALANCE SHEET, as first reported.
# FY2021 and FY2022 come from the FY2022 filing, which puts the EGP 65,010 of
# other financial investments in CURRENT assets; the FY2023 filing reclassifies
# the identical balance to NON-current. That is a presentation change with no
# effect on any total, and it is in the basis-break register rather than smoothed.
# ---------------------------------------------------------------------------
BS = {
 "FY2021": dict(src="AFS2022", column="comparative", page="pdf p5, balance sheet",
    ppe=1_042_256_485, intangibles=0, cwip=63_225_934, lt_fin_inv=125_561_420,
    other_fin_inv=65_010, other_fin_inv_current=True, total_non_current=1_231_043_839,
    inventories=330_815_427, debtors=117_908_741, due_from_affiliates=2_498_651,
    sundry_debtors=203_176_444, other_debit=140_087_745, cash=93_970_346,
    cash_blocked=650_074_240, total_current=1_538_596_604, total_assets=2_769_640_443,
    capital=680_584_430, legal_reserve=227_163_603, general_reserve=29_359_411,
    under_capital_increase=650_074_240, retained=-1_388_695_718,
    profit_for_year=-344_997_068, equity=-146_511_102,
    deferred_tax_liability=133_761_441, lt_loans=0, lease_lt=0, total_lt=133_761_441,
    bank_facilities=1_646_001_706, provisions=84_300_076,
    st_loans_affiliates=200_000_000, lease_st=0, due_to_affiliates=0,
    suppliers=765_256_383, other_credit=86_831_939,
    total_current_liab=2_782_390_104, total_liabilities=2_916_151_545),
 "FY2022": dict(src="AFS2022", column="own", page="pdf p5, balance sheet",
    ppe=1_011_373_267, intangibles=939_988, cwip=61_374_460, lt_fin_inv=125_561_420,
    other_fin_inv=65_010, other_fin_inv_current=True, total_non_current=1_199_249_135,
    inventories=885_548_344, debtors=269_268_012, due_from_affiliates=6_901_406,
    sundry_debtors=276_562_998, other_debit=135_986_473, cash=124_700_709,
    cash_blocked=0, total_current=1_699_032_952, total_assets=2_898_282_087,
    capital=1_330_658_670, legal_reserve=227_163_603, general_reserve=29_359_411,
    under_capital_increase=0, retained=-1_763_827_282,
    profit_for_year=-319_800_970, equity=-496_446_568,
    deferred_tax_liability=125_012_602, lt_loans=203_619_394, lease_lt=0,
    total_lt=328_631_996,
    bank_facilities=600_309_381, provisions=112_853_076,
    st_loans_affiliates=950_000_000, lease_st=0, due_to_affiliates=0,
    suppliers=1_129_539_373, other_credit=273_394_829,
    total_current_liab=3_066_096_659, total_liabilities=3_394_728_655),
 "FY2023": dict(src="AFS2023", column="own", page="pdf p5, balance sheet",
    ppe=967_198_768, intangibles=920_965, cwip=139_159_795, lt_fin_inv=125_561_420,
    other_fin_inv=65_010, other_fin_inv_current=False, total_non_current=1_232_905_958,
    inventories=883_259_621, debtors=547_056_074, due_from_affiliates=10_821_310,
    sundry_debtors=76_195_147, other_debit=402_643_025, cash=350_019_607,
    cash_blocked=0, total_current=2_269_994_784, total_assets=3_502_900_742,
    capital=1_330_658_670, legal_reserve=227_163_603, general_reserve=29_359_411,
    under_capital_increase=0, retained=-2_083_628_252,
    profit_for_year=-117_581_612, equity=-614_028_180,
    deferred_tax_liability=132_485_238, lt_loans=170_895_515, lease_lt=0,
    total_lt=303_380_753,
    bank_facilities=690_607_915, provisions=105_541_205,
    st_loans_affiliates=1_746_543_178, lease_st=0, due_to_affiliates=0,
    suppliers=993_648_328, other_credit=277_207_543,
    total_current_liab=3_813_548_169, total_liabilities=4_116_928_922),
 "FY2024": dict(src="AFS2025", column="comparative", page="pdf p2, balance sheet",
    ppe=1_026_166_835, intangibles=162_269_152, cwip=344_607_261,
    lt_fin_inv=25_039_500, other_fin_inv=65_010, other_fin_inv_current=False,
    deferred_tax_asset=145_689_339, total_non_current=1_703_837_098,
    inventories=1_049_449_935, debtors=223_320_195, due_from_affiliates=4_170_523,
    sundry_debtors=77_574_168, other_debit=599_285_115, cash=1_890_505_077,
    cash_blocked=147_466_100, total_current=3_991_771_113, total_assets=5_695_608_211,
    capital=1_330_658_670, legal_reserve=227_163_603, general_reserve=29_359_411,
    under_capital_increase=1_277_466_100, retained=-2_201_209_864,
    profit_for_year=3_072_361_812, equity=3_735_799_732,
    deferred_tax_liability=0, lt_loans=0, lease_lt=141_240_526, total_lt=141_240_526,
    bank_facilities=0, provisions=121_722_580, st_loans_affiliates=427_905_191,
    lease_st=8_717_155, due_to_affiliates=0,
    suppliers=599_922_969, other_credit=660_300_058,
    total_current_liab=1_818_567_953, total_liabilities=1_959_808_479),
 "FY2025": dict(src="AFS2025", column="own", page="pdf p2, balance sheet",
    ppe=1_265_871_591, intangibles=138_919_931, cwip=267_673_812,
    lt_fin_inv=25_039_500, other_fin_inv=65_010, other_fin_inv_current=False,
    deferred_tax_asset=0, total_non_current=1_697_569_844,
    inventories=876_191_093, debtors=243_390_012, due_from_affiliates=7_806,
    sundry_debtors=137_574_616, other_debit=577_635_635, cash=4_762_348_666,
    cash_blocked=0, total_current=6_597_147_828, total_assets=8_294_717_672,
    capital=2_608_124_770, legal_reserve=227_163_603, general_reserve=29_359_411,
    under_capital_increase=0, retained=871_151_948,
    profit_for_year=2_284_539_004, equity=6_020_338_736,
    deferred_tax_liability=126_684_552, lt_loans=0, lease_lt=111_742_265,
    total_lt=238_426_817,
    bank_facilities=0, provisions=102_403_549, st_loans_affiliates=0,
    lease_st=25_823_623, due_to_affiliates=20_772_778,
    suppliers=652_572_902, other_credit=1_234_379_267,
    total_current_liab=2_035_952_119, total_liabilities=2_274_378_936),
}

# ---------------------------------------------------------------------------
# CASH-FLOW LINES the panel and the valuation-input block both need.
# ---------------------------------------------------------------------------
CF = {
 "FY2021": dict(src="AFS2022", column="comparative", page="pdf p9, cash flow",
    depreciation=91_302_015, amortisation=0,
    capex_ppe=17_316_243, capex_cwip=34_872_520, proceeds_disposals=153_461,
    cash_open=17_035_796, cash_close=93_970_346),
 "FY2022": dict(src="AFS2022", column="own", page="pdf p9, cash flow",
    depreciation=90_609_825, amortisation=11_152,
    capex_ppe=62_826_341, capex_cwip=-1_851_474, proceeds_disposals=2_336_322,
    cash_open=93_970_346, cash_close=124_700_709),
 "FY2023": dict(src="AFS2023", column="own", page="pdf p9, cash flow",
    depreciation=87_210_904, amortisation=19_023,
    capex_ppe=43_041_892, capex_cwip=77_785_335, proceeds_disposals=5_277,
    cash_open=124_700_709, cash_close=350_019_607),
 "FY2024": dict(src="AFS2024", column="own", page="pdf p6, cash flow",
    depreciation=88_786_811, amortisation=1_963_206,
    capex_ppe=320_960_258, capex_cwip=205_447_467, proceeds_disposals=None,
    cash_open=350_019_607, cash_close=None),
 "FY2025": dict(src="AFS2025", column="own", page="pdf p6, cash flow",
    depreciation=99_209_674, amortisation=23_349_222,
    capex_ppe=339_330_933, capex_cwip=-76_933_449, proceeds_disposals=None,
    cash_open=None, cash_close=4_762_348_666),
}


# ---------------------------------------------------------------------------
# THE COST NOTES — the finest level this issuer discloses.
# SINAI CEMENT DISCLOSES NO PHYSICAL VOLUME ANYWHERE: not a tonne of clinker or
# cement, not a capacity, not a utilisation, in any of the six published filings.
# So the ground-up build cannot reach volume x price on a DISCLOSED unit, and
# under SIGCM clause 2 it drops to the finest sourced level and FLAGS the gap:
# the cost-note LINE. That is recorded here rather than worked around, because
# a tonnage taken from a plant register is an industry-ring forecast driver and
# is not the company's own reported figure.
#
# The line names are stable FY2021-FY2023 and again FY2024-FY2025, and they are
# NOT the same set across that boundary: "Operation and Development fees" stops
# after FY2023 and "Clay resource fees" and "Subcontractor" appear from FY2024.
# Those three are in the basis-break register and are scored only inside their
# own definition window. The six lines below carry identical wording in all five
# years and are the ones this run scores.
# ---------------------------------------------------------------------------
COST_NOTES = {
 "FY2021": dict(src="AFS2022", page="pdf p23, notes 23 and 24, comparative column",
    materials_fuel_power_packing=951_333_195, cogs_wages=38_170_121,
    cogs_maintenance=76_025_512, transport_and_loading=167_848_491,
    export_and_quality_mark=1_208_550, industrial_depreciation=87_675_120,
    cogs_note_total=1_402_703_740, change_in_inventory=-18_500_996),
 "FY2022": dict(src="AFS2022", page="pdf p23, notes 23 and 24",
    materials_fuel_power_packing=1_761_956_506, cogs_wages=41_833_792,
    cogs_maintenance=78_877_536, transport_and_loading=120_969_722,
    export_and_quality_mark=786_350, industrial_depreciation=86_777_804,
    cogs_note_total=2_199_574_898, change_in_inventory=-5_485_865),
 "FY2023": dict(src="AFS2023", page="pdf p22, notes 22 and 23",
    materials_fuel_power_packing=3_026_169_346, cogs_wages=46_554_590,
    cogs_maintenance=81_456_188, transport_and_loading=544_400_550,
    export_and_quality_mark=3_884_803, industrial_depreciation=82_564_005,
    cogs_note_total=3_502_831_659, change_in_inventory=-138_243_904),
 "FY2024": dict(src="AFS2025", page="note 24, comparative column",
    materials_fuel_power_packing=3_031_229_986, cogs_wages=69_084_467,
    cogs_maintenance=217_728_745, transport_and_loading=499_269_967,
    export_and_quality_mark=232_605_937, industrial_depreciation=84_045_872,
    cogs_note_total=3_764_687_505, change_in_inventory=+10_331_383),
 "FY2025": dict(src="AFS2025", page="note 24, printed page 23",
    materials_fuel_power_packing=3_592_466_202, cogs_wages=98_744_488,
    cogs_maintenance=306_304_604, transport_and_loading=579_219_496,
    export_and_quality_mark=185_690_219, industrial_depreciation=94_083_975,
    cogs_note_total=4_593_386_885, change_in_inventory=+38_651_970),
}

PAR_VALUE = 10.0          # note 27 and the capital line of every balance sheet

YEARS = ["FY2021", "FY2022", "FY2023", "FY2024", "FY2025"]


# ---------------------------------------------------------------------------
def _foots(name, parts, total, tol=1.0):
    got = sum(parts)
    assert abs(got - total) <= tol, (
        '%s does not foot: the printed rows give %.0f against a printed %.0f — a '
        'misread digit, since the filing foots' % (name, got, total))


def verify():
    """The footings the filings themselves print. A misread digit breaks one."""
    for y, d in IS.items():
        _foots('%s gross' % y, [d['sales'], -d['cogs']], d['gross'])
        parts = [d['selling'], d['ga'], d['finance'], d['ecl'], d['provisions']]
        _foots('%s total expenses' % y, parts, d['total_expenses'])
        _foots('%s operating' % y, [d['gross'], -d['total_expenses']], d['operating'])
        _foots('%s pbt' % y, [d['operating'], d['below']], d['pbt'])
        _foots('%s pat' % y, [d['pbt'], d['deferred_tax'], -d['income_tax']], d['pat'])
    # the below-the-line block foots to its own printed subtotal where the layout prints one
    for y in ("FY2021", "FY2022", "FY2023"):
        d = IS[y]
        _foots('%s non-operating block' % y,
               [d['interest_income'], d['capital_gains'], d['other_income'], d['fx']],
               d['below'])
    for y, d in BS.items():
        nc = [d['ppe'], d['intangibles'], d['cwip'], d['lt_fin_inv'],
              d.get('deferred_tax_asset', 0)]
        if not d['other_fin_inv_current']:
            nc.append(d['other_fin_inv'])
        _foots('%s non-current assets' % y, nc, d['total_non_current'])
        ca = [d['inventories'], d['debtors'], d['due_from_affiliates'],
              d['sundry_debtors'], d['other_debit'], d['cash'], d['cash_blocked']]
        if d['other_fin_inv_current']:
            ca.append(d['other_fin_inv'])
        _foots('%s current assets' % y, ca, d['total_current'])
        _foots('%s total assets' % y, [d['total_non_current'], d['total_current']],
               d['total_assets'])
        _foots('%s equity' % y,
               [d['capital'], d['legal_reserve'], d['general_reserve'],
                d['under_capital_increase'], d['retained'], d['profit_for_year']],
               d['equity'], tol=2.0)
        _foots('%s long-term liabilities' % y,
               [d['deferred_tax_liability'], d['lt_loans'], d['lease_lt']], d['total_lt'])
        _foots('%s current liabilities' % y,
               [d['bank_facilities'], d['provisions'], d['st_loans_affiliates'],
                d['lease_st'], d['due_to_affiliates'], d['suppliers'], d['other_credit']],
               d['total_current_liab'])
        _foots('%s total liabilities' % y, [d['total_lt'], d['total_current_liab']],
               d['total_liabilities'])
        _foots('%s balance sheet' % y, [d['total_liabilities'], d['equity']],
               d['total_assets'], tol=2.0)
    # THE PROFIT ON THE BALANCE SHEET IS THE PROFIT ON THE INCOME STATEMENT
    for y in YEARS:
        assert abs(BS[y]['profit_for_year'] - IS[y]['pat']) <= 2, \
            '%s: the balance sheet and the income statement disagree on the year' % y
    # THE RETAINED-EARNINGS ROLL: last year's retained plus last year's result
    for a, b in zip(YEARS, YEARS[1:]):
        roll = BS[a]['retained'] + BS[a]['profit_for_year']
        gap = BS[b]['retained'] - roll
        BS[b]['retained_roll_residual'] = gap
    # THE SHARE COUNT IS FOOTED OR IT IS NOT RECORDED [R-FCAL-01]. Issued capital over
    # par must reproduce the count, AND that count must reproduce the printed EPS. Both,
    # every year — which is what makes a carried-back count impossible here.
    for y in YEARS:
        n = BS[y]['capital'] / PAR_VALUE
        BS[y]['shares_from_capital'] = n
        if y == "FY2025":
            # the capital increase converted DURING FY2025, so the printed EPS is struck
            # on a weighted-average count and the closing count cannot reproduce it
            continue
        assert abs(IS[y]['pat'] / n - IS[y]['eps']) < 0.02, (
            '%s: the printed EPS does not reproduce from issued capital over par '
            '(%.4f against a printed %.2f)' % (y, IS[y]['pat'] / n, IS[y]['eps']))
    BS["FY2025"]['shares_weighted_average'] = IS["FY2025"]['pat'] / IS["FY2025"]['eps']
    # THE CASH-FLOW STATEMENT'S OWN CASH ROLL
    for y in YEARS:
        c = CF[y]
        if c['cash_close'] is not None:
            assert abs(c['cash_close'] - BS[y]['cash']) <= 2, \
                '%s: the cash-flow close and the balance-sheet cash disagree' % y
        if c['cash_open'] is not None and y != "FY2021":
            prev = YEARS[YEARS.index(y) - 1]
            assert abs(c['cash_open'] - BS[prev]['cash']) <= 2, \
                '%s: the cash-flow open is not last year"s close' % y
    # THE COST NOTE FOOTS TO THE FACE OF THE PROFIT AND LOSS ACCOUNT, every year.
    # This is the strongest control available on the cost stack: note 22/23/24's own
    # total plus its change in inventory IS the cost of sales the income statement
    # prints, and a misread in any component breaks it.
    for y, c in COST_NOTES.items():
        _foots('%s cost note to the face of the P&L' % y,
               [c['cogs_note_total'], c['change_in_inventory']], IS[y]['cogs'])
    return True


# ---------------------------------------------------------------------------
def derived():
    """What the filings imply. Computed, never typed."""
    out = {}
    for y in YEARS:
        d, b, c = IS[y], BS[y], CF[y]
        dna = c['depreciation'] + c['amortisation']
        # INTEREST COMES FROM THE BORROWINGS THAT ACTUALLY BEAR IT [R-FCAL-01 trap (i)].
        # Suppliers, other credit accounts, provisions and the deferred tax liability
        # pay no interest and are excluded. Sinai's interest-bearing book is bank
        # facilities, long-term bank loans, loans from affiliated companies and, from
        # FY2024, lease liabilities under EAS 49.
        ibd = (b['bank_facilities'] + b['lt_loans'] + b['st_loans_affiliates']
               + b['lease_lt'] + b['lease_st'])
        wc = (b['inventories'] + b['debtors'] + b['due_from_affiliates']
              + b['sundry_debtors'] + b['other_debit']
              - b['suppliers'] - b['other_credit'])
        out[y] = dict(
            revenue=d['sales'] / 1e6,
            cogs=d['cogs'] / 1e6,
            gross_margin=d['gross'] / d['sales'],
            selling=d['selling'] / 1e6,
            ga=d['ga'] / 1e6,
            finance_expense=d['finance'] / 1e6,
            interest_income=d['interest_income'] / 1e6,
            dna=dna / 1e6,
            # EBIT adds back the finance charge this layout buries in operating expenses
            ebit=(d['operating'] + d['finance']) / 1e6,
            ebitda=(d['operating'] + d['finance'] + dna) / 1e6,
            ebitda_margin=(d['operating'] + d['finance'] + dna) / d['sales'],
            pat=d['pat'] / 1e6,
            capex=(c['capex_ppe'] + c['capex_cwip']) / 1e6,
            capex_disclosed=True,
            ppe=b['ppe'] / 1e6,
            cash=(b['cash'] + b['cash_blocked']) / 1e6,
            interest_bearing_debt=ibd / 1e6,
            working_capital=wc / 1e6,
            wc_pct_revenue=wc / d['sales'],
            equity=b['equity'] / 1e6,
            shares_mn=b['shares_from_capital'] / 1e6,
            materials=COST_NOTES[y]['materials_fuel_power_packing'] / 1e6,
            cogs_wages=COST_NOTES[y]['cogs_wages'] / 1e6,
            cogs_maintenance=COST_NOTES[y]['cogs_maintenance'] / 1e6,
            transport=COST_NOTES[y]['transport_and_loading'] / 1e6,
            export_expense=COST_NOTES[y]['export_and_quality_mark'] / 1e6,
            materials_pct_revenue=(COST_NOTES[y]['materials_fuel_power_packing']
                                   / d['sales']),
        )
    # the borrowing RATE on the borrowings that actually bear it, and the number the
    # broad-denominator mistake would have produced instead
    for a, b_ in zip(YEARS, YEARS[1:]):
        avg_ibd = (out[a]['interest_bearing_debt'] + out[b_]['interest_bearing_debt']) / 2
        out[b_]['kd_on_borrowings'] = out[b_]['finance_expense'] / avg_ibd if avg_ibd else None
        broad = (BS[a]['total_liabilities'] + BS[b_]['total_liabilities']) / 2 / 1e6
        out[b_]['kd_on_total_liabilities'] = out[b_]['finance_expense'] / broad
    # the deposit rate the cash pile actually earned
    for a, b_ in zip(YEARS, YEARS[1:]):
        avg_cash = (out[a]['cash'] + out[b_]['cash']) / 2
        out[b_]['deposit_rate'] = out[b_]['interest_income'] / avg_cash if avg_cash else None
    # capex by the identity, as a cross-check on the disclosed figure [R-FCAL-01]
    for a, b_ in zip(YEARS, YEARS[1:]):
        out[b_]['capex_identity'] = (out[b_]['ppe'] - out[a]['ppe']) + out[b_]['dna']
    return out


def cross_check_study():
    """This panel and scem_study/filings_extract.py read the same filings. Assert they
    agree rather than assume it — two readings of one scan is the cheapest available
    control on the route."""
    p = os.path.join(os.path.dirname(HERE), 'scem_study', 'filings_extract.json')
    if not os.path.exists(p):
        return 'filings_extract.json absent — RECORDED AS MISSING, not skipped'
    s = json.load(open(p))
    n = 0
    for y in ("FY2024", "FY2025"):
        for k in ('sales', 'cogs', 'gross', 'operating', 'pbt', 'pat'):
            assert s['income_statement'][y][k] == IS[y][k], \
                'the two readings of %s %s disagree' % (y, k)
            n += 1
        for k in ('total_assets', 'equity', 'total_liabilities', 'cash'):
            key = 'ppe' if k == 'ppe' else k
            assert s['balance_sheet'][y][key] == BS[y][key], \
                'the two readings of %s %s disagree' % (y, k)
            n += 1
    return '%d figures agree between this panel and the study extract' % n


if __name__ == '__main__':
    verify()
    d = derived()
    print('every footing the filings perform: PASSED')
    print(cross_check_study())
    json.dump({'sources': SOURCES, 'income_statement': IS, 'balance_sheet': BS,
               'cash_flow': CF, 'cost_notes': COST_NOTES, 'par_value': PAR_VALUE, 'years': YEARS,
               'derived': d},
              open(os.path.join(HERE, 'panel_export.json'), 'w'), indent=1)
    print()
    hdr = ('%-8s %9s %9s %8s %7s %8s %8s %9s %8s'
           % ('year', 'revenue', 'EBITDA', 'mgn', 'D&A', 'capex', 'PAT', 'debt', 'shares'))
    print(hdr)
    for y in YEARS:
        r = d[y]
        print('%-8s %9.1f %9.1f %7.1f%% %7.1f %8.1f %8.1f %9.1f %8.1f'
              % (y, r['revenue'], r['ebitda'], r['ebitda_margin'] * 100, r['dna'],
                 r['capex'], r['pat'], r['interest_bearing_debt'], r['shares_mn']))
    print()
    print('%-8s %22s %24s %14s' % ('year', 'Kd on the borrowings',
                                   'Kd on total liabilities', 'deposit rate'))
    for y in YEARS[1:]:
        r = d[y]
        print('%-8s %21.2f%% %23.2f%% %13.2f%%'
              % (y, r['kd_on_borrowings'] * 100, r['kd_on_total_liabilities'] * 100,
                 r['deposit_rate'] * 100))
