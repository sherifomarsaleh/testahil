#!/usr/bin/env python3
"""PHAR (EIPICO) — the FUNDAMENTAL walk-forward panel [R-FCAL-01].

WHICH WALK-FORWARD THIS IS: the FUNDAMENTAL one — drivers rebuilt at a past
origin and scored against what the company actually reported.  Not the
price-engine walk-forward (band coverage on the Monte Carlo cone,
engine/phar_study/backtest_5y.py) and not the technical walk-forward
(engine/lab/ta_calibration/).

EVERY FIGURE HERE IS THE COMPANY'S OWN.  Source: EIPICO's own investor-relations
archive, eipico.com.eg -> Investor Relations -> Annual Reports, seven annual
reports FY2019..FY2025.  No vendor, no broker, no press (SIGCM clause 1).

POINT-IN-TIME IS ABSOLUTE.  Every year is carried AS FIRST REPORTED, out of that
year's OWN annual report.  Where a later report re-presents a figure the
re-presentation is recorded in `REPRESENTATIONS` beside it and NEVER substituted.

ARITHMETIC IS THE ARBITER, NOT THE EXTRACTOR'S CONFIDENCE.  Every statement is
footed against its own subtotals at import; `assert_all()` raises rather than
warns.  Four printed cells in these filings DO NOT foot and each one is resolved
by the statement's own chain, recorded in `FOOTING_FAILURES`, never smoothed.
"""
from __future__ import annotations
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))

# --------------------------------------------------------------------------
# The filings.  Each is the named annual report, or a page extract of it, held
# in filings/ beside this file.
#
# THAT DIRECTORY IS NOT COMMITTED — `.gitignore` line 51 excludes
# engine/*_walkforward/filings/ across the repository — so a fresh clone does
# NOT carry these PDFs, and saying so here is the point: every record below
# names the ORIGINAL annual report and the EXACT URL it was downloaded from, so
# the extraction is reproducible from EIPICO's own investor-relations page
# rather than from a local copy nobody else has. The FY2021-FY2025 files are
# page extracts because the seven whole reports run to 107MB; the extract's own
# filename carries the page span, the record carries the page, and the source of
# record is the URL.
# --------------------------------------------------------------------------
FILINGS = {
    "AR2019": dict(file="filings/PHAR_AR2019_BoD_Report.pdf",
                   url="https://www.eipico.com.eg/DataImages/HTML/File816.pdf",
                   what="Annual Report 2019 — board of directors' report (this edition carries "
                        "no financial statements; it carries the operating KPI tables)",
                   tier="A", route="text layer (PyMuPDF); every table footed against its own totals"),
    "AR2020": dict(file="filings/PHAR_AR2020_Annual_Report.pdf",
                   url="https://www.eipico.com.eg/DataImages/HTML/File1081.pdf",
                   what="Annual Report 2020 — standalone AND consolidated financial statements, "
                        "auditor's reports, notes; English",
                   tier="A", route="text layer (PyMuPDF); every statement footed against its own subtotals"),
    "AR2021": dict(file="filings/PHAR_AR2021_extract_p64-118.pdf",
                   url="https://www.eipico.com.eg/DataImages/HTML/File1106.pdf",
                   what="Annual Report 2021 — KPI pages and the consolidated statements; Arabic",
                   tier="A", route="text layer (PyMuPDF), Arabic-Indic digits normalised; footed"),
    "AR2022": dict(file="filings/PHAR_AR2022_extract_p59-111.pdf",
                   url="https://www.eipico.com.eg/DataImages/HTML/File1202.pdf",
                   what="Annual Report 2022 — KPI pages and the consolidated statements; Arabic",
                   tier="A", route="text layer (PyMuPDF), Arabic-Indic digits normalised; footed"),
    "AR2023": dict(file="filings/PHAR_AR2023_extract_p55-89.pdf",
                   url="https://www.eipico.com.eg/DataImages/HTML/File1138.pdf",
                   what="Annual Report 2023 — KPI pages and the consolidated statements; Arabic",
                   tier="A", route="text layer (PyMuPDF), Arabic-Indic digits normalised; footed"),
    "AR2024": dict(file="filings/PHAR_AR2024_extract_p59-101.pdf",
                   url="https://www.eipico.com.eg/DataImages/HTML/File1536.pdf",
                   what="Annual Report 2024 — KPI pages, the consolidated statements and notes; Arabic",
                   tier="A", route="text layer (PyMuPDF), Arabic-Indic digits normalised; footed. "
                        "THIS FILING'S ARABIC GLYPH MAP IS PARTLY BROKEN — several header strings "
                        "render as mojibake while the Latin digits extract cleanly, which is exactly "
                        "the condition [R-FCAL-01] warns about, so every figure was footed."),
    "AR2025": dict(file="filings/PHAR_AR2025_extract_p61-103.pdf",
                   url="https://www.eipico.com.eg/DataImages/HTML/File1699.pdf",
                   what="Annual Report 2025 — KPI pages, the consolidated statements and notes; Arabic",
                   tier="A", route="text layer (PyMuPDF), Arabic-Indic digits normalised; footed"),
    "FY2023EN": dict(file="../phar_study/source_FY2023_audited_consolidated.pdf",
                   url="company-supplied English translation of the issued audited statements",
                   what="FY2023 audited consolidated financial statements, auditor's English translation",
                   tier="A", route="text layer for the notes; the statement pages carry no text layer"),
    "FY2024EN": dict(file="../phar_study/source_FY2024_audited_consolidated.pdf",
                   url="company-supplied English translation of the issued audited statements",
                   what="FY2024 audited consolidated financial statements, auditor's English translation",
                   tier="A", route="text layer (pdftotext -layout) for the notes; statement pages imaged"),
}

# --------------------------------------------------------------------------
# CONSOLIDATED INCOME STATEMENT, as first reported, EGP.
# FY2019 and FY2020 come out of the FY2020 report, which presents the
# consolidated accounts IN THOUSANDS and in condensed form; those two years are
# marked `condensed` and their fine expense split is NOT available on a
# consolidated basis at their own origin.
# --------------------------------------------------------------------------
IS = {
    "FY2019": dict(src="AR2020", unit=1000, condensed=True,
        revenue=3411043000, cogs=2159504000, gross_profit=1251539000,
        expenses_total=590821000, other_block=111930000,
        below_line=67946000, pbt=840594000,
        income_tax=163131000, deferred_tax=-2650000, takaful=8665000,
        net_profit=671448000, parent_profit=611547000, nci=822000),
    "FY2020": dict(src="AR2020", unit=1000, condensed=True,
        revenue=2909774000, cogs=1694094000, gross_profit=1215680000,
        expenses_total=730122000, other_block=77756000,
        below_line=32012000, pbt=595326000,
        income_tax=101679000, deferred_tax=-1532000, takaful=7779000,
        net_profit=487400000, parent_profit=422832000, nci=886000),
    "FY2021": dict(src="AR2021", unit=1, condensed=False,
        revenue=3436975768, cogs=1917127364, gross_profit=1519848404,
        marketing=495821175, rnd=34965136, ga=92345049, board=1881000,
        finance=169098453, provisions=109000000,
        expenses_total=903110813,
        associates=43365383, interest_income=23261717, other_block=66627100,
        capital_gains=2778521, fx=-6254923, other_income=8802261, dividend_tax=0,
        below_line=5325859, pbt=688690550,
        income_tax=136914982, deferred_tax=19984845, takaful=8985341,
        net_profit=522805382, parent_profit=483917960, nci=533302),
    "FY2022": dict(src="AR2022", unit=1, condensed=False,
        revenue=3955156682, cogs=2301968839, gross_profit=1653187843,
        marketing=553837414, rnd=43683190, ga=130892038, board=1859380,
        finance=222096984, provisions=250000000,
        expenses_total=1202369006,
        associates=38016308, interest_income=19752079, other_block=57768387,
        capital_gains=3698493, fx=286404665, other_income=6053659, dividend_tax=0,
        below_line=296156817, pbt=804744041,
        income_tax=162970881, deferred_tax=-12904158, takaful=10917142,
        net_profit=643760176, parent_profit=587040623, nci=777852),
    "FY2023": dict(src="AR2023", unit=1, condensed=False,
        revenue=5231665571, cogs=2896343413, gross_profit=2335322158,
        marketing=648291681, rnd=43227785, ga=151584727, board=2020000,
        finance=407705200, provisions=265000000,
        expenses_total=1517829393,
        associates=74508447, interest_income=26243536, other_block=100751986,
        capital_gains=4689492, fx=139625936, other_income=20695305, dividend_tax=0,
        below_line=165010733, pbt=1083255484,
        income_tax=249772423, deferred_tax=-4147536, takaful=14324267,
        net_profit=823306330, parent_profit=751218307, nci=988615),
    "FY2024": dict(src="AR2024", unit=1, condensed=False,
        revenue=7590545643, cogs=4184382863, gross_profit=3406162780,
        marketing=915021183, rnd=70460824, ga=188492929, board=1580000,
        finance=960131966, provisions=702000000,
        expenses_total=2837686902,
        associates=151580926, interest_income=72048362, other_block=223629288,
        capital_gains=222246, fx=699879896, other_income=42631725, dividend_tax=0,
        dividend_tax_below_line=4468933,
        below_line=738264934, pbt=1530370100,
        income_tax=430792372, deferred_tax=-18964390, takaful=21618514,
        net_profit=1096923604, parent_profit=1008945944, nci=1206525),
    "FY2025": dict(src="AR2025", unit=1, condensed=False,
        revenue=9441379305, cogs=5287140903, gross_profit=4154238402,
        marketing=1000128922, rnd=70935883, ga=221136860, board=1828000,
        finance=1332946559, provisions=494218374,
        expenses_total=3121194598,
        associates=495499218, interest_income=139673783, other_block=635173001,
        capital_gains=1763816, fx=-16168329, other_income=142089566, dividend_tax=0,
        below_line=127685053, pbt=1795901858,
        income_tax=421702076, deferred_tax=-108663088, takaful=24969855,
        net_profit=1457893015, parent_profit=1352284629, nci=16235315),
}

# --------------------------------------------------------------------------
# CONSOLIDATED BALANCE SHEET, as first reported, EGP.
# --------------------------------------------------------------------------
BS = {
    "FY2019": dict(src="AR2020", ppe=798131000, cip=164043000, intangibles=0,
        associates_bv=259398000, rou=0, nca=1221572000,
        inventory=1437990000, ar=1088642000, other_rec=77757000, hfs=0,
        cash=588988000, ca=3193377000, total_assets=4414949000,
        capital=991705000, treasury=0, reserves=1247046000, retained=40467000,
        eiaco_div=0, year_profit=670626000, parent_equity=2949844000,
        nci_equity=2540000, total_equity=2952384000,
        lt_loans=0, lt_facilities=0, lease_lt=0, dtl=53391000, ncl=53391000,
        provisions=154915000, bank_credit=989578000, ap=91450000,
        div_payable=0, other_cl=169259000, tax_payable=3972000, lease_st=0,
        cl=1409174000),
    "FY2020": dict(src="AR2020", ppe=840152000, cip=185690000, intangibles=0,
        associates_bv=339166000, rou=0, nca=1365008000,
        inventory=1797394000, ar=876424000, other_rec=261033000, hfs=0,
        cash=732754000, ca=3667605000, total_assets=5032613000,
        capital=991705000, treasury=-89863000, reserves=1451466000, retained=4114000,
        eiaco_div=0, year_profit=486514000, parent_equity=2843936000,
        nci_equity=2884000, total_equity=2846820000,
        lt_loans=0, lt_facilities=0, lease_lt=0, dtl=51860000, ncl=51860000,
        provisions=58284000, bank_credit=1779446000, ap=77339000,
        div_payable=0, other_cl=148636000, tax_payable=70228000, lease_st=0,
        cl=2133933000),
    "FY2021": dict(src="AR2021", ppe=922138625, cip=449841684, intangibles=0,
        associates_bv=339165845, rou=0, nca=1711146154,
        inventory=1817785529, ar=1199627287, other_rec=232942176, hfs=0,
        cash=311587051, ca=3561942043, total_assets=5273088197,
        capital=991705000, treasury=0, reserves=1451126674, retained=5544976,
        eiaco_div=0, year_profit=522272080, parent_equity=2970648730,
        nci_equity=2820166, total_equity=2973468896,
        lt_loans=279638056, lt_facilities=249427444, lease_lt=0, dtl=71844662,
        ncl=600910162,
        provisions=73785303, bank_credit=1219165622, ap=75445425,
        div_payable=0, other_cl=219695420, tax_payable=110617369, lease_st=0,
        cl=1698709139),
    "FY2022": dict(src="AR2022", ppe=969914107, cip=866160786, intangibles=1567040,
        associates_bv=352342033, rou=1835170, nca=2191819136,
        inventory=2161799424, ar=1794422644, other_rec=130569216, hfs=12330000,
        cash=482969378, ca=4582090662, total_assets=6773909798,
        capital=991705000, treasury=0, reserves=1502885332, retained=74145367,
        eiaco_div=27616000, year_profit=642982324, parent_equity=3239334023,
        nci_equity=3052935, total_equity=3242386958,
        lt_loans=735619163, lt_facilities=76512181, lease_lt=794054, dtl=58940504,
        ncl=871865902,
        provisions=115393367, bank_credit=2032647352, ap=200245865,
        div_payable=0, other_cl=203162053, tax_payable=106817993, lease_st=1390308,
        cl=2659656938),
    "FY2023": dict(src="AR2023", ppe=963645365, cip=3058211677, intangibles=2301715,
        associates_bv=466490873, rou=2022754, nca=4492672384,
        inventory=2242395730, ar=2357855472, other_rec=197731029, hfs=12330000,
        cash=675798245, ca=5486110476, total_assets=9978782860,
        capital=1487557500, treasury=0, reserves=1835139939, retained=77872936,
        eiaco_div=34520000, year_profit=822317715, parent_equity=4257408090,
        nci_equity=3394945, total_equity=4260803035,
        lt_loans=2832316822, lt_facilities=0, lease_lt=134716, dtl=54792968,
        ncl=2887244506,
        provisions=191159599, bank_credit=2045331450, ap=176353891,
        div_payable=45225, other_cl=230675384, tax_payable=184979290, lease_st=2190480,
        cl=2830735319),
    "FY2024": dict(src="AR2024", ppe=1045230507, cip=5693566382, intangibles=32053960,
        associates_bv=465263725, rou=9566507, nca=7245681081,
        inventory=3584699946, ar=3049275231, other_rec=185584353, hfs=12330000,
        cash=1295386860, ca=8127276390, total_assets=15372957471,
        capital=1487557500, treasury=0, reserves=1919226893, retained=113295762,
        eiaco_div=37972000, year_profit=1095717079, parent_equity=4653769234,
        nci_equity=3816172, total_equity=4657585406,
        lt_loans=4782128576, lt_facilities=0, lease_lt=10706509, dtl=35828578,
        ncl=4828663663,
        provisions=356698370, bank_credit=4406896591, ap=410391619,
        div_payable=152488, other_cl=367421180, tax_payable=344846967, lease_st=301187,
        cl=5886708402),
    "FY2025": dict(src="AR2025", ppe=3069747924, cip=4901223806, intangibles=40142171,
        associates_bv=675874567, rou=233640379, dta=337611796, nca=9258240643,
        inventory=3887077629, ar=3325044117, other_rec=356786958, hfs=12330000,
        cash=1433426902, ca=9014665606, total_assets=18272906249,
        capital=1687557500, treasury=0, reserves=2722047479, retained=391868803,
        eiaco_div=0, year_profit=1441657700, parent_equity=6243131482,
        nci_equity=288704605, total_equity=6531836087,
        lt_loans=3758803399, lt_facilities=0, lease_lt=11982389, dtl=190768071,
        ncl=3961553859,
        provisions=537942744, bank_credit=3918693902, ap=780416969,
        div_payable=434651, other_cl=1044832275, tax_payable=388949813,
        lease_st=382759, st_loans=1107863191,
        cl=7779516303),
}
# FY2025 carries a separate short-term loans line the earlier years fold into
# bank credit; FY2021 folds the related-party creditor balance of 38,199,893
# into other_cl so the current-liability subtotal foots as printed.

# --------------------------------------------------------------------------
# CASH-FLOW AND FIXED-ASSET ITEMS, consolidated, as first reported.
# --------------------------------------------------------------------------
CF = {
    "FY2019": dict(src="AR2020", dep=None, rou_amort=None, intang_amort=None, capex=None,
        missing="the FY2020 report presents the consolidated cash-flow statement in CONDENSED "
                "form — one 'adjustments to reconcile' line and one 'investing activities' line "
                "— so neither the consolidated depreciation charge nor consolidated capex is "
                "disclosed for FY2019 anywhere in a filing published by the FY2019 or FY2020 "
                "year end. Not estimated; the cell is left out."),
    "FY2020": dict(src="AR2020", dep=None, rou_amort=None, intang_amort=None, capex=None,
        missing="same condensed consolidated cash-flow presentation as FY2019. The consolidated "
                "charge of 139,570,904 and capex of 203,563,553 were FIRST disclosed in the "
                "FY2021 report's comparative column, AFTER this origin, and are recorded in "
                "LATER_DISCLOSURE rather than substituted here. The origin's own filing does "
                "disclose a STANDALONE depreciation charge of 133,553,000 (note 4) and standalone "
                "fixed-asset cost additions of 180,714,000 — a different basis, recorded beside."),
    "FY2021": dict(src="AR2021", dep=90881011, rou_amort=0, intang_amort=0, capex=437086549,
        dividends_paid=383572856),
    "FY2022": dict(src="AR2022", dep=97229977, rou_amort=1868782, intang_amort=161220, capex=562954417,
        dividends_paid=393139776),
    "FY2023": dict(src="AR2023", dep=102675784, rou_amort=2082510, intang_amort=491451, capex=2290194556,
        dividends_paid=309756566),
    "FY2024": dict(src="AR2024", dep=96532194, rou_amort=2361230, intang_amort=3918430, capex=2846239746,
        dividends_paid=434005242),
    "FY2025": dict(src="AR2025", dep=109455425, rou_amort=3323968, intang_amort=4945981, capex=1354665231,
        dividends_paid=611365823),
}

LATER_DISCLOSURE = {
    "FY2020": dict(dep_consolidated=139570904, capex_consolidated=203563553,
                   first_disclosed_in="AR2021",
                   dep_standalone_own_filing=133553000,
                   ppe_cost_additions_standalone_own_filing=180714000,
                   dividends_paid_consolidated=503099471),
}

# --------------------------------------------------------------------------
# OPERATING KPIs, from the company's own annual-report KPI tables (COMPANY_IR
# tier, tagged distinctly from the audited-statement tier).  Sales, exports and
# production value are STANDALONE — the KPI table is the parent's.
# --------------------------------------------------------------------------
KPI = {
    "FY2018": dict(src="AR2019", packs_th=299040, sales_th=2747574, exports_th=654040,
                   production_value_th=2876887, products=347, export_usd_mn=36.704),
    "FY2019": dict(src="AR2019", packs_th=323267, sales_th=3220649, exports_th=640065,
                   production_value_th=3281506, products=353, export_usd_mn=38.149),
    "FY2020": dict(src="AR2020", packs_th=None, sales_th=2814500, exports_th=635400,
                   production_value_th=3520900, products=371, export_usd_mn=None,
                   missing="the FY2020 annual report is a condensed edition that carries no "
                           "packs-produced figure; 327,850 thousand was first disclosed in the "
                           "FY2021 report and is NOT carried back into this origin."),
    "FY2021": dict(src="AR2021", packs_th=316844, sales_th=3364116, exports_th=752982,
                   production_value_th=3464934, products=381, export_usd_mn=None),
    "FY2022": dict(src="AR2022", packs_th=339906, sales_th=3799457, exports_th=964654,
                   production_value_th=4043786, products=401, export_usd_mn=None),
    "FY2023": dict(src="AR2023", packs_th=330562, sales_th=5017015, exports_th=1592007,
                   production_value_th=5628822, products=401, export_usd_mn=None),
    "FY2024": dict(src="AR2024", packs_th=306133, sales_th=7364072, exports_th=2500156,
                   production_value_th=8475335, products=412, export_usd_mn=None),
    "FY2025": dict(src="AR2025", packs_th=326682, sales_th=9302469, exports_th=2967480,
                   production_value_th=10811924, products=414, export_usd_mn=None),
}

SHARES = {
    "FY2019": dict(issued_capital=991705000, par=10.0, count=99170500, src="AR2020"),
    "FY2020": dict(issued_capital=991705000, par=10.0, count=99170500, src="AR2020",
                   note="treasury shares of EGP 89,863,280 at par = 8,986,328 shares were held at "
                        "31-12-2020 and are disclosed as a deduction from paid capital"),
    "FY2021": dict(issued_capital=991705000, par=10.0, count=99170500, src="AR2021"),
    "FY2022": dict(issued_capital=991705000, par=10.0, count=99170500, src="AR2022"),
    "FY2023": dict(issued_capital=1487557500, par=10.0, count=148755750, src="AR2023"),
    "FY2024": dict(issued_capital=1487557500, par=10.0, count=148755750, src="AR2024"),
    "FY2025": dict(issued_capital=1687557500, par=10.0, count=168755750, src="AR2025"),
}

# --------------------------------------------------------------------------
# THE FOUR PRINTED CELLS THAT DO NOT FOOT.  Each is resolved by the statement's
# own arithmetic and by a later filing's comparative; the defective cell is
# named, the correction is not smoothed, and nothing here is an estimate.
# --------------------------------------------------------------------------
FOOTING_FAILURES = [
    dict(id="F-1", filing="AR2022", statement="consolidated income statement, FY2022",
         printed="gross profit 1,635,187,843",
         correct=1653187843,
         how="revenue 3,955,156,682 less cost of sales 2,301,968,839 is 1,653,187,843, and only "
             "that figure carries the statement's own chain to its printed profit before tax: "
             "1,653,187,843 - 1,202,369,006 + 57,768,387 + 296,156,817 = 804,744,041 exactly. "
             "The printed 1,635,187,843 leaves the chain 18,000,000 short. A 53/35 transposition "
             "in the gross-profit cell; revenue and cost of sales are both confirmed by the "
             "FY2023 report's comparative column.",
         note="THE SAME DEFECTIVE FIGURE IS CARRIED FORWARD into the FY2023 report's FY2022 "
              "comparative, so a reader checking one filing against the next sees agreement and "
              "still has the wrong number. Only the arithmetic separates them."),
    dict(id="F-2", filing="AR2023", statement="consolidated statement of financial position, FY2023",
         printed="fixed assets (net) 963,645,369 and, with it, total non-current assets "
                 "4,492,672,388 and total assets 9,978,782,864",
         correct=963645365,
         how="the sheet does not balance as printed: equity 4,260,803,035 plus total liabilities "
             "5,717,979,825 is 9,978,782,860, four pounds below the printed total assets. The "
             "FY2024 report's comparative column carries 963,645,365 and balances exactly."),
    dict(id="F-3", filing="AR2024", statement="consolidated statement of financial position, FY2024",
         printed="income taxes payable 344,864,967",
         correct=344846967,
         how="the printed current-liability subtotal of 5,886,708,402 is reproduced only by "
             "344,846,967; the printed cell overshoots it by 18,000. The FY2025 report's "
             "comparative column carries 344,846,967. An 846/864 transposition."),
    dict(id="F-4", filing="AR2024", statement="consolidated statement of financial position, FY2024",
         printed="long-term lease liabilities 10,705,609",
         correct=10706509,
         how="the printed non-current-liability subtotal of 4,828,663,663 is reproduced only by "
             "10,706,509; the printed cell falls 900 short. The FY2025 comparative carries "
             "10,706,509. An 05/06 transposition."),
    dict(id="F-5", filing="AR2024", statement="consolidated statement of financial position, FY2024",
         printed="total liabilities 10,715,372,056",
         correct=10715372065,
         how="its own two components, 4,828,663,663 and 5,886,708,402, sum to 10,715,372,065, "
             "and that is also what the FY2025 comparative carries. A 65/56 transposition in a "
             "subtotal, so nothing downstream of it is affected."),
    dict(id="F-6", filing="AR2023", statement="consolidated income statement, FY2023",
         printed="the sub-total of associates and interest income, 100,751,986",
         correct=100751986,
         how="its two printed components, 74,508,447 and 26,243,536, sum to 100,751,983 — three "
             "pounds below the printed sub-total. THE SUB-TOTAL IS THE FIGURE THE STATEMENT USES: "
             "it is what carries the chain to the printed profit before tax of 1,083,255,484. The "
             "three pounds sit inside one of the two components and no later filing separates "
             "them, so the sub-total is carried and the discrepancy is recorded rather than "
             "allocated. It is 0.0000003 of revenue and moves nothing."),
]

# --------------------------------------------------------------------------
# RE-PRESENTATIONS.  Recorded beside the figure, never substituted [R-FCAL-01].
# --------------------------------------------------------------------------
REPRESENTATIONS = [
    dict(id="R-1", year="FY2020", what="revenue and cost of sales",
         as_first_reported=dict(revenue=2909774000, cogs=1694094000),
         as_re_presented=dict(revenue=2885627759, cogs=1674501938, source="AR2021"),
         effect="revenue 24,146,241 lower and cost of sales 19,592,062 lower; net profit "
                "unchanged at 487,400,000 (the FY2021 report's FY2020 column reaches the "
                "identical figure). A gross-up/net-down reclassification, not a restatement."),
    dict(id="R-2", year="FY2021", what="revenue and marketing expenses",
         as_first_reported=dict(revenue=3436975768, marketing=495821175),
         as_re_presented=dict(revenue=3408804513, marketing=467649920, source="AR2022"),
         effect="both 28,171,255 lower; profit before tax unchanged. The same "
                "gross-up/net-down reclassification as R-1, one year later."),
    dict(id="R-3", year="FY2021", what="net profit for the year",
         as_first_reported=dict(net_profit=522805382),
         as_re_presented=dict(net_profit=488285382, source="AR2022"),
         effect="34,520,000 lower, being the EIACO distributed profit that the FY2022 "
                "presentation shows as a separate equity line rather than inside the year's "
                "profit. A PRESENTATION change in a line the model scores, so FY2021 is scored "
                "on its own filing and the FY2022 view is recorded here."),
    dict(id="R-4", year="FY2021", what="trade receivables and current liabilities",
         as_first_reported=dict(ar=1199627287, cl=1698709139),
         as_re_presented=dict(ar=1161427394, cl=1660509246, source="AR2022"),
         effect="the related-party balance of 38,199,893 is netted against receivables rather "
                "than shown as a creditor. Working capital unchanged in substance."),
    dict(id="R-5", year="FY2023", what="general and administrative expenses",
         as_first_reported=dict(ga=151584727),
         as_re_presented=dict(ga=147460994, dividend_tax=4123733, source="AR2024"),
         effect="the tax on dividends received is taken out of administrative expenses and shown "
                "on its own line. FY2023 is scored on its own filing; the delivered study uses "
                "the FY2024 presentation, which is why the two differ by exactly that amount."),
    dict(id="R-6", year="FY2024", what="borrowings",
         as_first_reported=dict(lt_loans=4782128576),
         as_re_presented=dict(lt_loans=3425026502, st_loans=1357102074, source="AR2025"),
         effect="the current portion is split out. TOTAL INTEREST-BEARING DEBT IS UNCHANGED — "
                "3,425,026,502 + 1,357,102,074 = 4,782,128,576 exactly — which is why the debt "
                "driver is built on the total and not on the long-term line."),
    dict(id="R-7", year="FY2024", what="packs produced",
         as_first_reported=dict(packs_th=306133),
         as_re_presented=dict(packs_th=299608, source="AR2025"),
         effect="6,525 thousand packs lower, 2.1%. A KPI redefinition inside the company's own "
                "indicator table with no reconciliation given, so the unit driver is scored only "
                "against the figure each origin's own report published."),
    dict(id="R-8", year="FY2024", what="profit before tax in the cash-flow statement",
         as_first_reported=dict(pbt_income_statement=1530370100),
         as_re_presented=dict(pbt_cash_flow_statement=1532370100, source="AR2025"),
         effect="the FY2025 report's comparative cash-flow column opens on 1,532,370,100 against "
                "the 1,530,370,100 both income statements print. Two million, 0.13% of the line. "
                "The income statement figure is the one carried, and the discrepancy is recorded."),
]

BASIS_BREAKS = [
    dict(id="B-1", year="FY2021", what="consolidated presentation",
         detail="the FY2019 and FY2020 consolidated accounts are presented CONDENSED and IN "
                "THOUSANDS — revenue, cost of sales, one 'expenses' line, one 'revenues' line — "
                "while FY2021 onward carry the full expense split in units of one pound. "
                "TREATMENT: revenue, cost of sales, gross profit, total expenses, profit before "
                "tax and net profit are scored across all seven years; marketing, R&D, "
                "administrative, finance cost and provisions are scored ONLY inside their own "
                "definition window, FY2021-FY2025."),
    dict(id="B-2", year="FY2022", what="right-of-use assets and lease liabilities",
         detail="EAS 49 leases first appear in the consolidated balance sheet at FY2022 (1,835,170 "
                "of right-of-use assets, 794,054 long-term and 1,390,308 short-term liabilities). "
                "TREATMENT: immaterial at under 0.03% of assets; carried in the balance-sheet "
                "block from FY2022 and absent, correctly, before it."),
    dict(id="B-3", year="FY2023", what="issued capital",
         detail="capital increased from 991,705,000 to 1,487,557,500 on 6 August 2023, being "
                "49,585,250 new shares of EGP 10 par. TREATMENT: the share count is read from each "
                "year's own capital note and NEVER carried back; per-share figures are not a "
                "driver of this run."),
    dict(id="B-4", year="FY2025", what="issued capital, again",
         detail="capital increased to 1,687,557,500 in July 2025, being 20,000,000 new shares of "
                "EGP 10 par. Same treatment."),
    dict(id="B-5", year="FY2023", what="the capital programme",
         detail="projects under construction go 866,160,786 (FY2022) -> 3,058,211,677 (FY2023) -> "
                "5,693,566,382 (FY2024) and then FALL to 4,901,223,806 (FY2025) as EIPICO 3 is "
                "transferred into fixed assets (2,086,458,897 transferred in FY2025 alone). "
                "TREATMENT: this is the single largest structural fact in the window and is NOT a "
                "basis break in the accounting sense — it is a real capital programme. It is "
                "listed here because a mechanical capex driver estimated on FY2019-FY2022 cannot "
                "see it, and the run's own capex error is the measurement of that."),
    dict(id="B-6", year="FY2022", what="the currency",
         detail="the Egyptian pound was devalued in March 2022, October 2022, January 2023 and "
                "March 2024. TREATMENT: the currency is macro and enters the macro/company split "
                "of every error; export revenue is dollar-linked and the active-ingredient import "
                "bill is dollar-linked, which is [L-302] and is why the split is run both ways."),
]

# --------------------------------------------------------------------------
# Footings.  Raise, never warn.
# --------------------------------------------------------------------------
def assert_all():
    bad = []
    for y, r in IS.items():
        if abs(r["revenue"] - r["cogs"] - r["gross_profit"]) > 1:
            bad.append("%s: revenue - cogs does not reproduce gross profit" % y)
        chain = r["gross_profit"] - r["expenses_total"] + r["other_block"] + r["below_line"]
        if abs(chain - r["pbt"]) > 1:
            bad.append("%s: the income-statement chain reaches %d against a stated pbt of %d"
                       % (y, chain, r["pbt"]))
        tax = r["income_tax"] + r["deferred_tax"] + r["takaful"]
        if abs(r["pbt"] - tax - r["net_profit"]) > 1:
            bad.append("%s: pbt less tax does not reproduce net profit" % y)
        if not r["condensed"]:
            exp = (r["marketing"] + r["rnd"] + r["ga"] + r["board"] + r["finance"]
                   + r["provisions"] + r["dividend_tax"])
            if abs(exp - r["expenses_total"]) > 1:
                bad.append("%s: the expense lines sum to %d against a stated total of %d"
                           % (y, exp, r["expenses_total"]))
            ob = r["associates"] + r["interest_income"]
            if abs(ob - r["other_block"]) > 3:
                bad.append("%s: associates plus interest income does not reproduce its subtotal" % y)
    for y, b in BS.items():
        nca = (b["ppe"] + b["cip"] + b["intangibles"] + b["associates_bv"] + b["rou"]
               + b.get("dta", 0))
        if abs(nca - b["nca"]) > 1:
            bad.append("%s: non-current assets sum to %d against a stated %d" % (y, nca, b["nca"]))
        ca = b["inventory"] + b["ar"] + b["other_rec"] + b["hfs"] + b["cash"]
        if abs(ca - b["ca"]) > 1:
            bad.append("%s: current assets sum to %d against a stated %d" % (y, ca, b["ca"]))
        if abs(b["nca"] + b["ca"] - b["total_assets"]) > 1:
            bad.append("%s: total assets do not foot" % y)
        eq = (b["capital"] + b["treasury"] + b["reserves"] + b["retained"]
              + b["eiaco_div"] + b["year_profit"])
        if abs(eq - b["parent_equity"]) > 1:
            bad.append("%s: parent equity does not foot" % y)
        if abs(b["parent_equity"] + b["nci_equity"] - b["total_equity"]) > 1:
            bad.append("%s: total equity does not foot" % y)
        ncl = b["lt_loans"] + b["lt_facilities"] + b["lease_lt"] + b["dtl"]
        if abs(ncl - b["ncl"]) > 1:
            bad.append("%s: non-current liabilities sum to %d against a stated %d" % (y, ncl, b["ncl"]))
        cl = (b["provisions"] + b["bank_credit"] + b["ap"] + b["div_payable"]
              + b["other_cl"] + b["tax_payable"] + b["lease_st"] + b.get("st_loans", 0))
        if abs(cl - b["cl"]) > 1:
            bad.append("%s: current liabilities sum to %d against a stated %d" % (y, cl, b["cl"]))
        if abs(b["total_equity"] + b["ncl"] + b["cl"] - b["total_assets"]) > 1:
            bad.append("%s: THE BALANCE SHEET DOES NOT BALANCE" % y)
    for y, s in SHARES.items():
        if abs(s["issued_capital"] / s["par"] - s["count"]) > 1:
            bad.append("%s: the share count does not foot against capital over par" % y)
    for y, k in KPI.items():
        if k.get("sales_th") and k.get("exports_th") and k["exports_th"] > k["sales_th"]:
            bad.append("%s: exports exceed total sales" % y)
    if bad:
        raise AssertionError("PHAR panel does not foot:\n  " + "\n  ".join(bad))
    return True


def interest_bearing_debt(y):
    """[R-FCAL-01] trap (i): interest comes from the borrowings that ACTUALLY bear it.

    Loans, credit facilities and bank credit lines only. Trade payables, other
    creditors, provisions, tax payable, dividends payable and lease liabilities
    are EXCLUDED — dividing the finance charge by a broader liabilities total
    understates the rate by a multiple and manufactures a bias that looks
    exactly like evidence.
    """
    b = BS[y]
    return (b["lt_loans"] + b["lt_facilities"] + b["bank_credit"] + b.get("st_loans", 0))


def dna(y):
    c = CF[y]
    if c["dep"] is None:
        return None
    return c["dep"] + (c["rou_amort"] or 0) + (c["intang_amort"] or 0)


def export_share(y):
    k = KPI[y]
    return k["exports_th"] / k["sales_th"]


def consolidation_ratio(y):
    """Consolidated revenue over the parent's own disclosed sales value.

    The company's KPI table is the PARENT's; the statements this run scores are
    CONSOLIDATED.  The ratio is a driver in its own right rather than a fudge:
    it is the EIACO ampoules subsidiary, and it is stable.
    """
    return IS[y]["revenue"] / (KPI[y]["sales_th"] * 1000.0)


def export():
    assert_all()
    years = sorted(IS)
    out = dict(
        _="PHAR (EIPICO) fundamental walk-forward panel. GENERATED by panel.py, which foots "
          "every statement against its own subtotals at import; never hand-edited.",
        run="PHAR", company="Egyptian International Pharmaceutical Industries Company (EIPICO)",
        exchange="EGX", market="EG", currency="EGP", basis="consolidated",
        fiscal_year_end="31 December",
        span="FY2019-FY2025, seven sourceable fiscal years",
        filings=FILINGS, income_statement=IS, balance_sheet=BS, cash_flow=CF,
        kpi=KPI, shares=SHARES, later_disclosure=LATER_DISCLOSURE,
        footing_failures=FOOTING_FAILURES, representations=REPRESENTATIONS,
        basis_breaks=BASIS_BREAKS,
        derived=dict(
            interest_bearing_debt={y: interest_bearing_debt(y) for y in years},
            dna={y: dna(y) for y in years},
            export_share={y: round(export_share(y), 6) for y in years},
            consolidation_ratio={y: round(consolidation_ratio(y), 6) for y in years},
            effective_borrowing_rate={
                y: round(IS[y].get("finance") / ((interest_bearing_debt(y)
                                                  + interest_bearing_debt(p)) / 2.0), 6)
                for p, y in zip(years, years[1:]) if IS[y].get("finance")},
        ),
    )
    with open(os.path.join(HERE, "panel_export.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
    return out


if __name__ == "__main__":
    d = export()
    print("PHAR panel — %d fiscal years, every statement footed" % len(d["income_statement"]))
    for y in sorted(IS):
        print("  %s  rev %14d  gp %13d  np %12d  debt %13d  packs %s"
              % (y, IS[y]["revenue"], IS[y]["gross_profit"], IS[y]["net_profit"],
                 interest_bearing_debt(y),
                 KPI[y]["packs_th"] if KPI[y]["packs_th"] else "  n/d"))
    print("\neffective borrowing rate, finance cost over average INTEREST-BEARING debt:")
    for y, r in d["derived"]["effective_borrowing_rate"].items():
        print("  %s  %.2f%%" % (y, 100 * r))
