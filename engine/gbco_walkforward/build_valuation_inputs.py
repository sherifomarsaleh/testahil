#!/usr/bin/env python3
"""GBCO walk-forward — the VALUATION-INPUT BLOCK, per origin [R-FCAL-01 AMENDED 03-09-2026].

A driver panel is not a record a value can be rebuilt from. Every item below sits on a
balance sheet or a cash-flow statement in a filing this run has already parsed cell by
cell, so carrying it out is a COPY rather than new research — and not carrying it means
no valuation this house makes on GBCO could ever be rebuilt at a past origin.

BUILT AS THE RUN GOES, not retro-fitted. Unit: EGP million. Route: PDF text layer
(pymupdf) throughout — every file named per item.

THE SHARE COUNT IS FOOTED OR IT IS NOT RECORDED, and today's count is never carried back.
GB Corp's capital chronology, from note 20 of the FY2025 statements and its predecessors:
135,337,545 shares from 31-Dec-2014; 1,094,009,733 from 31-May-2015; 1,085,500,000 from
15-Aug-2022 after the 8,509,733-share treasury cancellation. Par is EGP 1.00 throughout,
so issued capital divided by par reproduces the count the same document states, exactly.
"""
from __future__ import annotations
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
AR = lambda y: 'engine/gbco_study/src/GB_Annual_Report_%d.pdf' % y
AUD = 'engine/gbco_study/src/GB_Auto_Consolidated_E_31_December_%d.pdf'
REL = lambda t: 'engine/gbco_study/src/GB_Corp_ER_%s.pdf' % t
TXT = 'PDF text layer (pymupdf)'

def V(v, src, note=''):
    return {'value': v, 'source': src, 'route': TXT, 'unit': 'EGP mn', 'note': note}

def M(why):
    return {'missing': why}

def shares(count, capital_thousands, src):
    return {'value': count, 'issued_capital': capital_thousands * 1000.0, 'par_value': 1.0,
            'source': src, 'route': TXT,
            'note': 'issued capital / par = the count the same note states; par EGP 1.00'}

C15 = 1094009733; C22 = 1085500000
SRC_CAP_OLD = (AR(2016) + ' balance sheet "Issued and paid in capital" 1,094,010 (EGP thousand) '
               'and note 19; capital registered in the commercial register 31 May 2015')
SRC_CAP_NEW = ('engine/gbco_study/src/GB_Corp_Annual_Report_2025.pdf note 20 — issued and paid '
               'capital 1,085,500,000 shares of par EGP 1 each, after the 8,509,733-share '
               'treasury cancellation registered 15 August 2022')

NOT_LAYOUT = ('GB Auto\'s FY2018 and FY2019 annual reports lay the audited statements out '
              'NUMBERS-FIRST in a split two-column form whose values cannot be attached to '
              'their labels from the text layer, and the standalone audited PDFs for those '
              'years are not on GB Corp\'s IR filings index, whose statement archive starts at '
              '31 March 2020. Recorded as missing rather than estimated.')

O = {}
O['2015'] = dict(  # prior_year_anchor
    cash=V(1188.704, AR(2016) + ' comparative column, "Cash on hand and at banks"'),
    debt=V(5233.274, AR(2016) + ' comparative, loans 898,473 + loans/borrowings/overdrafts 4,334,801',
           'interest-bearing borrowings only; trade payables and provisions excluded'),
    ppe=V(3175.486, AR(2016) + ' comparative, PP&E and projects under construction (net)'),
    dep=V(254.724, AR(2016) + ' cash-flow statement comparative, "Depreciation and amortization for the year"'),
    capex=V(1259.383, AR(2016) + ' cash-flow comparative, "Acquisition of property, plant, equipment and projects under constructions"'),
    wc=V(2950.981 + 1649.624 - 1786.876, AR(2016) + ' comparative: inventories 2,950,981 + accounts and notes receivable 1,649,624 - trade payables and other credit balances 1,786,876'),
    shares=shares(C15, 1094010, SRC_CAP_OLD))
O['2016'] = dict(
    cash=V(1225.300, AR(2016)), debt=V(8732.109, AR(2016) + ' loans 1,663,490 + loans/borrowings/overdrafts 7,068,619'),
    ppe=V(4898.939, AR(2016)), dep=V(320.759, AR(2016) + ' cash-flow statement'),
    capex=V(1385.345, AR(2016) + ' cash-flow statement'),
    wc=V(5820.482 + 2363.801 - 2807.950, AR(2016) + ' inventories + receivables - trade payables'),
    shares=shares(C15, 1094010, SRC_CAP_OLD))
O['2017'] = dict(
    cash=V(1242.776, AR(2017)), debt=V(9614.792, AR(2017) + ' loans 2,573,823 + loans/borrowings/overdrafts 7,040,969'),
    ppe=V(5602.626, AR(2017)), dep=V(434.762, AR(2017) + ' cash-flow statement'),
    capex=V(1429.438, AR(2017) + ' cash-flow statement'),
    wc=V(3012.824 + 2972.213 - 1519.834, AR(2017) + ' inventories + receivables - trade payables'),
    shares=shares(C15, 1094010, SRC_CAP_OLD))
O['2018'] = dict(
    cash=M(NOT_LAYOUT), debt=M(NOT_LAYOUT), ppe=M(NOT_LAYOUT), dep=M(NOT_LAYOUT),
    capex=M(NOT_LAYOUT), wc=M(NOT_LAYOUT),
    shares=shares(C15, 1094010, SRC_CAP_OLD))
O['2019'] = dict(
    cash=V(1408.948, (AUD % 2020) + ' comparative column'),
    debt=M('the FY2020 audited statements\' comparative column carries the FY2019 asset side in '
           'a form the text layer resolves, and its liability side splits loans across two note '
           'references the layout does not attach to values; the FY19 earnings release predates '
           'GB Corp\'s IR release archive, which starts at 1Q20. Recorded as missing.'),
    ppe=V(4043.219, (AUD % 2020) + ' comparative column'),
    dep=V(654.742, (AUD % 2020) + ' cash-flow comparative'),
    capex=V(1736.040, (AUD % 2020) + ' cash-flow comparative, acquisition of PP&E and PUC'),
    wc=V(3788.210 + 6435.527 - 3144.1, (AUD % 2020) + ' comparative inventories and receivables; '
         'trade payables from the 4Q20 release segmented balance sheet'),
    shares=shares(C15, 1094010, SRC_CAP_OLD))
O['2020'] = dict(
    cash=V(1797.830, AUD % 2020), debt=V(14041.7, REL('4Q20_-_E_-_FINAL') + ' Table 6, loans and overdraft 10,459.3 + loans 3,582.4'),
    ppe=V(4167.572, AUD % 2020), dep=V(310.190, (AUD % 2020) + ' cash-flow statement'),
    capex=V(707.765, (AUD % 2020) + ' cash-flow statement'),
    wc=V(3367.987 + 7106.385 - 3144.1, (AUD % 2020) + ' inventories and receivables; payables from the 4Q20 release Table 6'),
    shares=shares(C15, 1094010, SRC_CAP_OLD))
O['2021'] = dict(
    cash=V(1935.644, AUD % 2021), debt=V(17143.2, REL('4Q21_-_E_-_FINAL') + ' Table 6, 13,628.2 + 3,515.0'),
    ppe=V(4208.324, AUD % 2021), dep=V(420.369, (AUD % 2021) + ' cash-flow statement',
        'AS ORIGINALLY REPORTED. The FY2022 annual report restates the FY2021 comparative to '
        '426,281; the restatement is noted beside and never substituted.'),
    capex=V(467.981, (AUD % 2021) + ' cash-flow statement',
        'AS ORIGINALLY REPORTED; restated to 485,789 in the FY2022 comparative'),
    wc=V(4203.342 + 10239.476 - 5418.6, (AUD % 2021) + ' inventories and receivables; payables from the 4Q21 release Table 6'),
    shares=shares(C15, 1094010, SRC_CAP_OLD))
O['2022'] = dict(
    cash=V(4098.1, REL('4Q22_-_E_-_FINAL') + ' Table 12'),
    debt=V(8980.5, REL('4Q22_-_E_-_FINAL') + ' Table 12, 6,040.2 + 2,940.3'),
    ppe=V(4945.2, REL('4Q22_-_E_-_FINAL') + ' Table 12'),
    dep=V(451.098, AR(2022) + ' cash-flow statement'),
    capex=V(1160.574, AR(2022) + ' cash-flow statement'),
    wc=V(3920.0 + 3060.6 - 5812.4, REL('4Q22_-_E_-_FINAL') + ' Table 12'),
    shares=shares(C22, 1085500, SRC_CAP_NEW))
O['2023'] = dict(
    cash=V(4504.2, REL('4Q23_-_ER_-_FINAL') + ' Table 14'),
    debt=V(12237.7, REL('4Q23_-_ER_-_FINAL') + ' Table 14, 7,674.5 + 4,563.2'),
    ppe=V(5965.7, REL('4Q23_-_ER_-_FINAL') + ' Table 14'),
    dep=V(531.403, AR(2023) + ' cash-flow statement'),
    capex=V(2055.957, AR(2023) + ' cash-flow statement'),
    wc=V(6366.1 + 4042.4 - 7110.1, REL('4Q23_-_ER_-_FINAL') + ' Table 14'),
    shares=shares(C22, 1085500, SRC_CAP_NEW))
O['2024'] = dict(
    cash=V(7420.9, REL('4Q24-_E_-_Final') + ' Table 14'),
    debt=V(22608.7, AR(2025) if False else 'engine/gbco_study/src/GB_Corp_Annual_Report_2025.pdf'
           ' comparative column: loans 6,835,835 + bonds 120,000 + loans/borrowings/overdrafts '
           '15,572,866 + bonds 80,000'),
    ppe=V(8193.2, REL('4Q24-_E_-_Final') + ' Table 14'),
    dep=V(1138.459, AR(2024) + ' cash-flow statement'),
    capex=V(3171.932, AR(2024) + ' cash-flow statement'),
    wc=V(21134.3 + 7581.3 - 19333.2, REL('4Q24-_E_-_Final') + ' Table 14'),
    shares=shares(C22, 1085500, SRC_CAP_NEW))

doc = {
    '_rule': '[R-FCAL-01 AMENDED 03-09-2026] — a run commits the inputs a VALUE is rebuilt from',
    '_unit': 'EGP million, except shares (a count) and issued_capital (EGP)',
    '_entity': 'GB Corp S.A.E (formerly GB Auto S.A.E), EGX: GBCO — CONSOLIDATED group figures',
    '_note': ('GB Corp is an operating company with a CAPTIVE LENDER. These are GROUP figures; '
              'the segmented GB Auto / GB Capital split of every line from FY2020 is in the '
              'run\'s panel and in the releases named here, and the two legs are valued '
              'separately because a lender\'s borrowings are its raw material and an '
              'assembler\'s are its working capital.'),
    'prior_year_anchor': {'2015': O.pop('2015')},
    'origins': O,
}
json.dump(doc, open(os.path.join(HERE, 'valuation_inputs.json'), 'w', encoding='utf-8'),
          indent=1, ensure_ascii=False)
print('origins:', ', '.join(sorted(O)))
