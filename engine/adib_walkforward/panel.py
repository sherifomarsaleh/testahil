#!/usr/bin/env python3
"""ADIB (Abu Dhabi Islamic Bank - Egypt, EGX: ADIB) — the walk-forward panel.

WHICH ADIB. This is the CAIRO-listed bank, EGX: ADIB, formerly National Bank for
Development S.A.E., renamed after Abu Dhabi Islamic Bank PJSC took control. It is NOT
ADIB Group (ADX: ADIB), which is a separate covered name (ADIBUAE) with its own study.
Every filing below is ADIB-Egypt's own, from adib.eg.

UNITS. EGP thousands throughout. FY2010 and FY2011 are filed in whole EGP and are
divided by 1,000 here; that division is the ONLY arithmetic applied to a filed figure
and it is marked on the row.

PROVENANCE, four fields on every number: value / source document / document date /
tier (A audited-or-company, B exchange-or-regulator, C credible third party). Every
figure in this file is tier A - ADIB-Egypt's own audited consolidated statements,
downloaded from adib.eg. Nothing here is tier B or C.

ROUTE. 'text' means the filing's own text layer carried the figure. 'ocr' means the
figures are a raster and were read from the rendered pixels by two independent passes
(native embedded image upscaled, and a page render), with any disagreement settled by
the statement's OWN arithmetic and, where that was not decisive, by the comparative
column of the following year's filing. Every OCR'd statement below foots exactly.

DERIVED cells carry their formula and are listed in DERIVED_NOTES. Nothing is
estimated, interpolated or inferred to fill a gap.

AS ORIGINALLY REPORTED. IS/BS carry each year as its OWN filing reported it. Where a
later filing restated the year, the restatement is in RESTATEMENTS and is never
substituted - the point-in-time rule is that an origin sees what had been published by
then [R-FCAL-01 §1].
"""

# --------------------------------------------------------------------------------
# Source register: one entry per filing actually parsed.
# --------------------------------------------------------------------------------
SOURCES = {
 'FY2010': dict(doc='Consolidated financial statements and the audit report thereon, year ended 31 Dec 2010 (National Bank For Development S.A.E.)',
                url='https://www.adib.eg/media/17601/ADIBEG_Financial_English_Consolidated_Q4_31-12-2010.PDF',
                date='2011', tier='A', route='text', units='EGP (whole)'),
 'FY2011': dict(doc='Consolidated financial statements, year ended 31 Dec 2011',
                url='https://www.adib.eg/media/17601/ADIBEG_Financial_English_Consolidated_Q4_31-12-2011.PDF',
                date='2012', tier='A', route='ocr', units='EGP (whole)'),
 'FY2012': dict(doc='Consolidated financial statements, year ended 31 Dec 2012',
                url='https://www.adib.eg/media/17601/ADIBEG_Financial_English_Consolidated_Q4_31-12-2012.PDF',
                date='2013-03', tier='A', route='text', units="EGP '000"),
 'FY2013': dict(doc='Consolidated financial statements, year ended 31 Dec 2013',
                url='https://www.adib.eg/media/73666/ADIBEG_Financial_English_Consolidated_Q4_31-12-2013.PDF',
                date='2014', tier='A', route='text', units="EGP '000"),
 'FY2014': dict(doc='Consolidated financial statements, year ended 31 Dec 2014 (Restated)',
                url='https://www.adib.eg/media/108766/ADIBEG_Financial_English_Consolidated_Q4_31-12-2014.PDF',
                date='2015', tier='A', route='text', units="EGP '000"),
 'FY2015': dict(doc='Consolidated financial statements, year ended 31 Dec 2015',
                url='https://www.adib.eg/media/157202/ADIBEG_Financial_English_Consolidated_Q4_31-12-2015.PDF',
                date='2016-02-18', tier='A', route='text', units="EGP '000"),
 'FY2016': dict(doc='Consolidated financial statements, year ended 31 Dec 2016',
                url='https://www.adib.eg/media/364987/ADIBEG_Financial_English_Consolidated_Q4_31-12-2016.PDF',
                date='2017-02-16', tier='A', route='text', units="EGP '000"),
 'FY2017': dict(doc='Consolidated financial statements, year ended 31 Dec 2017',
                url='https://www.adib.eg/media/644552/ADIBEG_Financial_English_Consolidated_Q4_31-12-2017.PDF',
                date='2018', tier='A', route='text', units="EGP '000"),
 'FY2018': dict(doc='Consolidated financial statements, year ended 31 Dec 2018',
                url='https://www.adib.eg/media/644552/ADIBEG_Financial_English_Consolidated_Q4_31-12-2018.PDF',
                date='2019', tier='A', route='text', units="EGP '000"),
 'FY2019': dict(doc='Consolidated financial statements, year ended 31 Dec 2019',
                url='https://www.adib.eg/media/644552/ADIBEG_Financial_English_en_Consolidated_Q4_31-12-2019.pdf',
                date='2020', tier='A', route='ocr', units="EGP '000"),
 'FY2020': dict(doc='Consolidated financial statements, year ended 31 Dec 2020',
                url='https://www.adib.eg/media/644552/ADIBEG_Financial_English_Consolidated_Q4_31-12-2020.pdf',
                date='2021-02-18', tier='A', route='ocr', units="EGP '000"),
 'FY2021': dict(doc='FY2021 taken from the COMPARATIVE column of the FY2022 audited consolidated statements. '
                    'The file published under the English FY2021 name on adib.eg is the ARABIC filing '
                    '(102pp, no English statement pages); no English FY2021 consolidated filing was located. '
                    'See fetch_attempts.json.',
                url='https://www.adib.eg/media/644552/ADIB_Consalidated_Condensed_Dec_2022.pdf',
                date='2023-02-09', tier='A', route='text+ocr', units="EGP '000"),
 'FY2022': dict(doc='Consolidated financial statements, year ended 31 Dec 2022',
                url='https://www.adib.eg/media/644552/ADIB_Consalidated_Condensed_Dec_2022.pdf',
                date='2023-02-09', tier='A', route='text(BS)+ocr(IS)', units="EGP '000"),
 'FY2023': dict(doc='Consolidated financial statements, year ended 31 Dec 2023',
                url='https://www.adib.eg/media/644552/ADIBEG_Financial_English_Consalidated_31-12-2023.pdf',
                date='2024', tier='A', route='ocr', units="EGP '000"),
 'FY2024': dict(doc='Consolidated financial statements, year ended 31 Dec 2024',
                url='https://www.adib.eg/media/Consalidated2024EN.pdf',
                date='2025-02-06', tier='A', route='ocr', units="EGP '000"),
 'FY2025': dict(doc='Consolidated financial statements, year ended 31 Dec 2025',
                url='https://www.adib.eg/media/753636/ADIBConsFinancialsDec2025EnglishFull.pdf',
                date='2026-02-05', tier='A', route='ocr', units="EGP '000"),
 'H1_2026': dict(doc='Condensed consolidated interim financial statements, six months ended 30 Jun 2026',
                url='https://www.adib.eg/media/2757582/ADIBConsalidatedQ22026English.pdf',
                date='2026', tier='A', route='ocr', units="EGP '000"),
 'Q1_2026': dict(doc='Condensed consolidated interim financial statements, three months ended 31 Mar 2026',
                url='https://www.adib.eg/media/2757576/consalidatedq1english.pdf',
                date='2026', tier='A', route='ocr', units="EGP '000"),
}

# --------------------------------------------------------------------------------
# Income statement, EGP '000, AS ORIGINALLY REPORTED in each year's own filing.
#   fin_income   income from Murabaha, Musharaka, Mudaraba and similar income
#   cost_funds   cost of deposits and similar costs (negative)
#   net_funds    = fin_income + cost_funds  (the bank's net financing income)
#   fee_inc / fee_exp / net_fees
#   admin        administrative expenses (negative)
#   other_op     other operating income/(expenses), SIGNED as filed
#   ecl          impairment / expected credit losses (negative = charge)
#   other_nii    DERIVED residual: dividends + trading + associates + investment and
#                disposal gains. Formula in DERIVED_NOTES.
#   pbt / tax / np / np_parent / nci
# --------------------------------------------------------------------------------
IS = {
 # FY2010-FY2011 carry a consolidated NON-BANK subsidiary: the income statement has
 # 'Sales revenue' and 'Cost of sale' lines inside the funds and fee blocks. See
 # BASIS_BREAKS. Filed in whole EGP; /1000 applied.
 'FY2010': dict(fin_income=562217.078, cost_funds=-465400.176, sales_revenue=111848.323,
                net_funds=208665.225, fee_inc=66005.579, fee_exp=-1263.781,
                cost_of_sale=-69456.795, net_fees=-4714.997,
                div=5134.275, trading=21433.882, admin=-294516.998, other_op=-135835.269,
                ecl=-493272.001, assoc=-489.948, inv_gain=15978.059,
                pbt=-677617.772, tax=187900.142, np=-489717.630,
                np_parent=-491439.621, nci=1721.991, eps=-2.62),
 'FY2011': dict(fin_income=710967.0, cost_funds=-556991.0, net_funds=153976.0,
                fee_inc=59887.0, fee_exp=-1960.0, net_fees=57927.0,
                div=4158.0, trading=9761.0, admin=-373763.0, other_op=-102169.0,
                ecl=-371055.0, assoc=-607.0, inv_gain=1105.0,
                pbt=-620667.0, tax=20642.0, np=-600025.0,
                np_parent=-601314.0, nci=1289.0, eps=-3.01),
 'FY2012': dict(fin_income=996950.0, cost_funds=-704335.0, net_funds=292615.0,
                fee_inc=61181.0, fee_exp=-941.0, net_fees=60240.0,
                div=3872.0, trading=18356.0, admin=-425972.0, other_op=-102063.0,
                ecl=-978291.0, assoc=51.0, inv_gain=-20227.0,
                pbt=-1151419.0, tax=274472.0, np=-876947.0,
                np_parent=-872434.0, nci=-4513.0, eps=-4.36),
 'FY2013': dict(fin_income=1197626.0, cost_funds=-821717.0, net_funds=375909.0,
                fee_inc=117571.0, fee_exp=-5626.0, net_fees=111945.0,
                div=4686.0, trading=60025.0, admin=-532146.0, other_op=-163489.0,
                ecl=69144.0, assoc=2999.0, inv_gain=-1136.0,
                pbt=-72063.0, tax=147786.0, np=75723.0,
                np_parent=71129.0, nci=4594.0, eps=0.36),
 'FY2014': dict(fin_income=1449913.0, cost_funds=-823702.0, net_funds=626211.0,
                fee_inc=250053.0, fee_exp=-11193.0, net_fees=238860.0,
                div=7805.0, trading=105854.0, admin=-626601.0, other_op=-1945.0,
                ecl=65290.0, assoc=5742.0, inv_gain=1912.0,
                pbt=423128.0, tax=-160792.0, np=262336.0,
                np_parent=258061.0, nci=4275.0, eps=1.29),
 'FY2015': dict(fin_income=1910977.0, cost_funds=-944300.0, net_funds=966677.0,
                fee_inc=241716.0, fee_exp=-8743.0, net_fees=232973.0,
                div=6135.0, trading=107909.0, admin=-762073.0, other_op=113073.0,
                ecl=-51557.0, assoc=6729.0, inv_gain=14095.0,
                pbt=633961.0, tax=-414722.0, np=219239.0,
                np_parent=212289.0, nci=6950.0, eps=1.06),
 'FY2016': dict(fin_income=2702704.0, cost_funds=-1263787.0, net_funds=1438917.0,
                fee_inc=359223.0, fee_exp=-10058.0, net_fees=349165.0,
                div=2768.0, trading=214928.0, admin=-958576.0, other_op=51593.0,
                ecl=-267105.0, assoc=7952.0, inv_gain=5652.0,
                pbt=845294.0, tax=-448256.0, np=397038.0,
                np_parent=414096.0, nci=-17058.0, eps=2.07),
 'FY2017': dict(fin_income=4125576.0, cost_funds=-2102180.0, net_funds=2023396.0,
                fee_inc=473525.0, fee_exp=-9727.0, net_fees=463798.0,
                div=2209.0, trading=143482.0, admin=-1172144.0, other_op=-47981.0,
                ecl=-132766.0, assoc=6502.0, inv_gain=46128.0,
                pbt=1332624.0, tax=-701026.0, np=631598.0,
                np_parent=633092.0, nci=-1494.0, eps=3.17),
 'FY2018': dict(fin_income=5713202.0, cost_funds=-3217211.0, net_funds=2495991.0,
                fee_inc=503112.0, fee_exp=-75568.0, net_fees=427544.0,
                div=3206.0, trading=156223.0, admin=-1235822.0, other_op=-308630.0,
                ecl=-235483.0, assoc=18452.0, inv_gain=3940.0,
                pbt=1325421.0, tax=-475182.0, np=850239.0,
                np_parent=854933.0, nci=-4694.0, eps=4.27),
 'FY2019': dict(fin_income=6853732.0, cost_funds=-3775799.0, net_funds=3077933.0,
                fee_inc=522546.0, fee_exp=-119518.0, net_fees=403028.0,
                div=4950.0, trading=220445.0, admin=-1375085.0, other_op=-248585.0,
                ecl=-406587.0, assoc=24896.0, inv_gain=6941.0,
                pbt=1707936.0, tax=-479697.0, np=1228239.0,
                np_parent=1229438.0, nci=-1199.0, eps=6.15),
 'FY2020': dict(fin_income=7147760.0, cost_funds=-4041183.0, net_funds=3106577.0,
                fee_inc=597641.0, fee_exp=-145473.0, net_fees=452168.0,
                div=2632.0, trading=181860.0, admin=-1343162.0, other_op=-246218.0,
                ecl=-444706.0, assoc=29030.0, inv_gain=13971.0,
                pbt=1752152.0, tax=-556283.0, np=1195869.0,
                np_parent=1192389.0, nci=3480.0, eps=5.11),
 'FY2021': dict(fin_income=8197874.0, cost_funds=-4697626.0, net_funds=3500248.0,
                fee_inc=789985.0, fee_exp=-175852.0, net_fees=614133.0,
                div=4824.0, trading=83974.0, admin=-1443471.0, other_op=-427481.0,
                ecl=-175667.0, assoc=36145.0, inv_gain=235.0, subsid_gain=87920.0,
                discontinued=-22859.0,
                pbt=2280860.0, tax=-807478.0, np=1450523.0,
                np_parent=1453132.0, nci=-2609.0, eps=6.10),
 'FY2022': dict(fin_income=11036472.0, cost_funds=-6214102.0, net_funds=4822370.0,
                fee_inc=1277972.0, fee_exp=-238075.0, net_fees=1039897.0,
                div=2689.0, trading=163452.0, admin=-1529482.0, other_op=-420557.0,
                ecl=-832461.0, assoc=32929.0, inv_gain=27276.0, subsid_gain=168.0,
                discontinued=-5806.0,
                pbt=3306281.0, tax=-1110728.0, np=2189747.0,
                np_parent=2196374.0, nci=-6627.0, eps=7.43),
 'FY2023': dict(fin_income=19533749.0, cost_funds=-10609499.0, net_funds=8924250.0,
                fee_inc=1946618.0, fee_exp=-388129.0, net_fees=1558489.0,
                div=5202.0, trading=291150.0, admin=-1921925.0, other_op=-772507.0,
                ecl=-1633830.0, assoc_and_inv=84525.0,
                pbt=6535354.0, tax=-1861514.0, np=4673840.0,
                np_parent=4670654.0, nci=3186.0, eps=8.67),
 'FY2024': dict(fin_income=36944486.0, cost_funds=-21691838.0, net_funds=15252648.0,
                fee_inc=2590419.0, fee_exp=-695288.0, net_fees=1895131.0,
                div=5415.0, trading=708711.0, admin=-2614518.0, other_op=-927002.0,
                ecl=-2170571.0, assoc=140338.0, inv_gain=0.0,
                pbt=12290152.0, tax=-3274213.0, np=9015939.0,
                np_parent=9008926.0, nci=7013.0, eps=14.02),
 'FY2025': dict(fin_income=49262455.0, cost_funds=-29110120.0, net_funds=20152335.0,
                fee_inc=3566871.0, fee_exp=-837021.0, net_fees=2729850.0,
                div=6307.0, trading=546571.0, admin=-3431217.0, other_op=-1176050.0,
                ecl=-1514062.0, assoc=161253.0, inv_gain=7155.0,
                pbt=17482142.0, tax=-4881186.0, np=12600956.0,
                np_parent=12588572.0, nci=12384.0, eps=11.25),
}

# --------------------------------------------------------------------------------
# Balance sheet, EGP '000, as originally reported in each year's own filing.
# --------------------------------------------------------------------------------
BS = {
 'FY2010': dict(total_assets=11897868.048, cust_deposits=10832874.006,
                total_liab=11507711.158, equity=390156.890, capital=1173321.0),
 'FY2011': dict(total_assets=13655409.377, cust_deposits=12040430.769,
                total_liab=13076124.689, equity=579284.688,
                fin_customers=2750247.645 + 1539146.114, capital=1999503.0),
 'FY2012': dict(total_assets=14429038.0, cust_deposits=12963029.0, due_to_banks=337733.0,
                subordinated=180777.0, total_liab=13955783.0, equity=473255.0,
                equity_parent=454366.0, nci=18889.0,
                fin_customers=391381.0 + 4703185.0, capital=1999503.0),
 'FY2013': dict(total_assets=16238406.0, cust_deposits=14588317.0, due_to_banks=1099.0,
                subordinated=209023.0, total_liab=15482132.0, equity=756274.0,
                fin_customers=294736.0 + 6037440.0, capital=1999503.0),
 'FY2014': dict(total_assets=19556172.0, cust_deposits=16579761.0, due_to_banks=793126.0,
                subordinated=203209.0, total_liab=18544552.0, equity=1011620.0,
                fin_customers=227952.0 + 8199861.0, capital=1999503.0),
 'FY2015': dict(total_assets=23588365.0, cust_deposits=20343021.0, due_to_banks=662301.0,
                subordinated=258205.0, total_liab=22439457.0, equity=1148908.0,
                equity_parent=1126582.0, nci=22326.0,
                fin_customers=229760.0 + 10046525.0, capital=1999503.0),
 'FY2016': dict(total_assets=33228215.0, cust_deposits=25513513.0, due_to_banks=2239144.0,
                subordinated=770025.0, total_liab=31638287.0, equity=1589928.0,
                equity_parent=1588433.0, nci=1495.0,
                fin_customers=215565.0 + 15016128.0, capital=2000000.0),
 'FY2017': dict(total_assets=37415243.0, cust_deposits=29832871.0, due_to_banks=905082.0,
                subordinated=777582.0, total_liab=35122458.0, equity=2292785.0,
                equity_parent=2247454.0, nci=45331.0,
                fin_customers=222023.0 + 16060969.0, capital=2000000.0),
 'FY2018': dict(total_assets=49406296.0, cust_deposits=39888883.0, due_to_banks=2464132.0,
                subordinated=828952.0, total_liab=46241876.0, equity=3164420.0,
                equity_parent=3141107.0, nci=23313.0,
                fin_customers=223089.0 + 23797412.0, capital=2000000.0),
 'FY2019': dict(total_assets=60324735.0, cust_deposits=51161108.0, due_to_banks=282893.0,
                subordinated=1263220.0, total_liab=55979364.0, equity=4345371.0,
                equity_parent=4327142.0, nci=18229.0,
                fin_customers=8000.0 + 30726378.0, capital=2000000.0),
 'FY2020': dict(total_assets=73885054.0, cust_deposits=62673279.0, due_to_banks=656738.0,
                subordinated=1613794.0, total_liab=68336747.0, equity=5548307.0,
                equity_parent=5529676.0, nci=18631.0,
                fin_customers=10434.0 + 40063467.0, capital=2000000.0),
 'FY2021': dict(total_assets=90554612.0, cust_deposits=75679539.0, due_to_banks=2352263.0,
                subordinated=1980165.0, total_liab=83675004.0, equity=6879608.0,
                equity_parent=6896970.0, nci=-17362.0,
                fin_customers=12172.0 + 45158029.0, capital=2000000.0),
 'FY2022': dict(total_assets=116827151.0, cust_deposits=97614326.0, due_to_banks=74840.0,
                subordinated=3085265.0, total_liab=107923352.0, equity=8903799.0,
                equity_parent=8890241.0, nci=13558.0,
                fin_customers=14659.0 + 56558054.0, capital=4000000.0),
 'FY2023': dict(total_assets=162254679.0, cust_deposits=127031908.0, due_to_banks=6478842.0,
                subordinated=4753202.0, total_liab=147890231.0, equity=14364448.0,
                equity_parent=14344817.0, nci=19631.0,
                fin_customers=16305.0 + 63083489.0, capital=5000000.0),
 'FY2024': dict(total_assets=260467106.0, cust_deposits=199982599.0, due_to_banks=14837337.0,
                subordinated=10401271.0, total_liab=237480399.0, equity=22986707.0,
                equity_parent=22958669.0, nci=28038.0,
                fin_customers=95691071.0, capital=6000000.0),
 'FY2025': dict(total_assets=346711205.0, cust_deposits=277564370.0, due_to_banks=5921757.0,
                subordinated=10232006.0, total_liab=312076349.0, equity=34634856.0,
                equity_parent=34596280.0, nci=38576.0,
                fin_customers=147226062.0, capital=12000000.0),
}

# --------------------------------------------------------------------------------
# Current-year disclosed periods. NOT scored - the walk-forward's last actual is
# FY2025. These anchor the study's base year and its forecast anchor [R-ANCHOR-01].
# --------------------------------------------------------------------------------
INTERIM = {
 'H1_2026': dict(fin_income=29117908.0, cost_funds=-16863967.0, net_funds=12253941.0,
                 fee_inc=2024636.0, fee_exp=-508077.0, net_fees=1516559.0,
                 div=5139.0, trading=560181.0, admin=-2239003.0, other_op=-1515642.0,
                 pbt=10721790.0, tax=-3170957.0, np=7550833.0,
                 np_parent=7536797.0, nci=14036.0, eps=4.98,
                 total_assets=414302106.0, total_liab=370689472.0,
                 equity=43612634.0, equity_parent=43557932.0,
                 fin_customers=190427051.0),
 'H1_2025': dict(fin_income=23361569.0, cost_funds=-13800156.0, net_funds=9561413.0,
                 fee_inc=1694809.0, fee_exp=-331341.0, net_fees=1363468.0,
                 div=2280.0, trading=455342.0, admin=-1561610.0, other_op=-741715.0,
                 pbt=8428137.0, tax=-2194198.0, np=6233939.0, nci=8315.0, eps=7.43),
}

DERIVED_NOTES = {
 'IS.other_nii': 'other_nii = pbt - net_funds - net_fees - admin - other_op - ecl. The '
                 'statement identity; it collects dividends, net trading, share of '
                 'associates and gains on financial investments/disposals into one '
                 'block. Used as the driver because the components are individually '
                 'immaterial (<1.5% of PBT each after FY2014) and are not separately '
                 'forecastable from any disclosed volume.',
 'IS.FY2025.inv_gain': '7,155 = pbt - (every other filed line on the page). The gain on '
                       'financial investments is the one line the two OCR passes never '
                       'agreed on; the footing identity settles it and it is 0.04% of PBT.',
 'IS.FY2025.nci_check': 'np_parent 12,588,572 + nci 12,384 = np 12,600,956 (filed). Foots.',
 'IS.FY2018.np_parent': '854,933 = np 850,239 - nci (-4,694). The FY2018 filing prints '
                        'the split in its FY2019 comparative; the FY2018 page itself was '
                        'read for np and nci.',
 'BS.FY2010': 'FY2010 is filed in whole EGP; /1000 applied. equity = total_assets - '
              'total_liab (the FY2010 page prints the equity block by component).',
 'BS.FY2011.equity': '579,284.688 = total_assets 13,655,409.377 - total_liab '
                     '13,076,124.689, both filed. The FY2012 filing RESTATES FY2011 to '
                     'total_assets 13,653,070 / equity 567,509 - see RESTATEMENTS.',
 'BS.FY2013.equity': '756,274 = total_assets 16,238,406 - total_liab 15,482,132, both '
                     'filed in the FY2014 comparative column.',
 'BS.FY2014.equity': '1,011,620 = 19,556,172 - 18,544,552, both filed.',
 'BS.FY2025.nci': '38,576 = total_equity 34,634,856 - equity_parent 34,596,280. '
                  'equity_parent itself foots on its own components '
                  '(12,000,000 + 1,613,793 + 19,323 + 20,963,164).',
 'BS.fin_customers': 'conventional + Islamic financing to customers, both net of '
                     'impairment, as the filing splits them. From FY2024 the filing '
                     'prints one line.',
}

# Later filings that restated an earlier year. NEVER substituted into IS/BS above.
RESTATEMENTS = {
 'FY2011': 'FY2012 filing: total_assets 13,653,070 (vs 13,655,409 filed), equity 567,509 '
           '(vs 579,285), net_fees 57,927 (vs -16,340 filed - the non-bank subsidiary '
           "'sales revenue'/'cost of sale' pair was reclassified out of the fee block).",
 'FY2014': 'FY2015 filing: cost_funds -824,768, net_funds 625,145, trading 73,438, '
           'other_op +30,297, pbt 421,888, np 261,096, np_parent 256,821, '
           'total_assets 19,539,215.',
 'FY2015': 'FY2016 filing: total_assets 23,574,992, total_liab 22,444,763, '
           'admin -762,074, pbt 633,960, np 219,238.',
 'FY2016': 'FY2017 filing: admin -957,762, other_op +50,779, cust_deposits 25,516,880, '
           'total_liab 31,603,451, equity 1,624,764.',
 'FY2017': 'FY2018 filing: net_fees 409,241 (fee_exp -64,284), admin -1,015,388, '
           'other_op -150,180, total_assets 37,413,309, total_liab 35,122,986.',
 'FY2018': 'FY2019 filing: net_fees 407,361 (fee_inc 504,980 / fee_exp -97,619), '
           'admin -1,202,563, other_op -321,129, total_assets 49,400,805, '
           'total_liab 46,236,385.',
}


def other_nii(y):
    """The non-interest, non-fee income block. DERIVED - see DERIVED_NOTES."""
    r = IS[y]
    return (r['pbt'] - r['net_funds'] - r['net_fees'] - r['admin']
            - r['other_op'] - r['ecl'])


def avg(field, y, source=BS):
    """Average of opening and closing. Returns None where the opening year is absent."""
    p = 'FY%d' % (int(y[2:]) - 1)
    if p not in source or y not in source:
        return None
    a, b = source[p].get(field), source[y].get(field)
    if a is None or b is None:
        return None
    return (a + b) / 2.0


def foots(y, tol=1.0):
    """Does the filed income statement add up? Returns (ok, residual)."""
    r = IS[y]
    s = (r['net_funds'] + r['net_fees'] + r['admin'] + r['other_op'] + r['ecl']
         + other_nii(y))
    return abs(s - r['pbt']) <= tol, s - r['pbt']


YEARS = sorted(IS)

if __name__ == '__main__':
    print('%-8s %14s %14s %12s %12s %12s' % ('year', 'fin_income', 'net_funds',
                                             'other_nii', 'pbt', 'np_parent'))
    for y in YEARS:
        print('%-8s %14.0f %14.0f %12.0f %12.0f %12.0f'
              % (y, IS[y]['fin_income'], IS[y]['net_funds'], other_nii(y),
                 IS[y]['pbt'], IS[y]['np_parent']))
    print()
    bad = [(y, foots(y)[1]) for y in YEARS if not foots(y)[0]]
    print('income statements that do not foot: %s' % (bad or 'none'))
    for y in YEARS:
        b = BS[y]
        r = b['total_assets'] - b['total_liab'] - b['equity']
        if abs(r) > 1.0:
            print('BS %s does not foot by %.1f' % (y, r))
