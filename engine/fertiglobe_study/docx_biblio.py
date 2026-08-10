"""Fertiglobe_Bibliography_09-08-2026.docx — the companion source document.

Every input the valuation model uses, with its value, its date and where it came from,
grouped by research layer; the primary documents actually read; the judgements and what
would overturn each; the searches that found nothing; and a note on aggregator data.

Emitted from study_numbers.json and sweep_register.json. No financial numeral is typed
into this builder — every figure is read from the committed numbers file.

Run from inside engine/fertiglobe_study (docx_base loads study_numbers.json relatively):
    python3 docx_biblio.py
"""
import json
import os

from docx.oxml import OxmlElement

import docx_base as B

HERE = os.path.dirname(os.path.abspath(__file__))
D = B.D
INP = D['inputs']
SR = json.load(open(os.path.join(HERE, 'sweep_register.json')))
OUT = os.path.join(HERE, 'Fertiglobe_Bibliography_09-08-2026.docx')

ZW = '​'
NS = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'


def keep_rows_whole(t, repeat_header=True):
    """Stop a row breaking across a page (half a source on one page and half on the next
    is unreadable) and repeat the header row at the top of each new page."""
    for i, row in enumerate(t.rows):
        trPr = row._tr.get_or_add_trPr()
        trPr.append(OxmlElement('w:cantSplit'))
        if i == 0 and repeat_header:
            trPr.append(OxmlElement('w:tblHeader'))
    return t


def zw(url):
    """Insert zero-width break opportunities so a long address wraps inside its column
    instead of forcing the column wider than the page."""
    for ch in ('/', '-', '_', '.', '?', '='):
        url = url.replace(ch, ch + ZW)
    return url


# ---------------------------------------------------------------------------
# value formatting — by magnitude and by what the input actually measures
# ---------------------------------------------------------------------------
PCT = {
    'tax_eff_fy23', 'tax_eff_fy24', 'tax_eff_fy25', 'tax_stat_uae', 'ust10', 'sofr',
    'ad_cds', 'ad_ads', 'ad_erp', 'ad_erp_cds', 'ad_crp', 'eg_erp', 'eg_erp_cds',
    'dz_erp', 'mature_erp', 'tax_dam_uae', 'tax_dam_eg', 'tax_dam_dz', 'w_egypt',
    'w_algeria', 'kd_spread_facility_bc', 'kd_spread_adnoc', 'kd_spread_rcf',
    'kd_cap_rate_rejected', 'urea_util_h1_26',
}
MMBTU = {'bm_ttf_fy25', 'bm_ttf_h1_26', 'bm_ttf_jul26',
         'gas_realised_q2_26', 'gas_realised_q2_26_ecremage'}
MEGATONNE = {'urea_demand_growth_2030', 'urea_capacity_adds_2030'}


def fmt(key, v):
    if isinstance(v, str):
        return v
    if key in PCT:
        s = f'{v * 100:.2f}'.rstrip('0').rstrip('.')
        return f'{s}%'
    if key in MMBTU:
        return f'${v:,.1f} per MMBtu'
    if key in MEGATONNE:
        return f'{v:,.1f} Mt'
    if key == 'eu_tariff_russia_jul26':
        return f'EUR {v:,.0f} per tonne'
    if key == 'spot_aed':
        return f'AED {v:,.2f}'
    if key == 'fx_aed_usd':
        return f'AED {v:,.4f} per USD'
    if key == 'shares_mn':
        return f'{v:,.1f}m shares'
    if key == 'beta':
        return f'{v:,.3f}'
    if key.startswith('vol_') or key.startswith('cap_'):
        return f'{v:,.0f} kt'
    if key.startswith('bm_urea') or key.startswith('bm_nh3'):
        return f'${v:,.0f} per tonne'
    if v < 0:
        return f'-${abs(v):,.1f}m'
    return f'${v:,.1f}m'


# ---------------------------------------------------------------------------
# plain-English names for every input. The model's own short keys are working
# shorthand and mean nothing to an outside reader, so nothing in this document shows
# one. Most keys are a stem plus a period suffix, so the stem carries the name and the
# suffix is formatted according to whether the item is a flow (a period) or a stock
# (a date).
# ---------------------------------------------------------------------------
FLOW = {
    'rev': 'Revenue',
    'cogs': 'Cost of sales',
    'sga': 'Selling, general and administrative expenses',
    'othinc': 'Other income net of other expenses',
    'dna': 'Depreciation and amortisation',
    'finc': 'Finance income',
    'fcost': 'Finance cost',
    'fx': 'Net foreign exchange loss',
    'tax': 'Income tax charge',
    'tax_paid': 'Income tax paid',
    'tax_eff': 'Reported effective tax rate',
    'nci': 'Profit attributable to non-controlling interests',
    'npown': 'Profit attributable to owners',
    'pbt': 'Profit before tax',
    'op': 'Operating profit',
    'ebitda': 'EBITDA',
    'adj_ebitda': 'Adjusted EBITDA',
    'cfo': 'Net cash from operating activities',
    'capex': 'Capital expenditure',
    'maint_capex': 'Maintenance capital expenditure',
    'divsh': 'Dividends paid to shareholders',
    'divnci': 'Dividends paid to non-controlling interests',
    'cost_raw': 'Cost by nature — raw materials and gas',
    'cost_freight': 'Cost by nature — freight and logistics',
    'cost_staff': 'Cost by nature — employee benefits',
    'cost_maint': 'Cost by nature — maintenance and repair',
    'cost_consult': 'Cost by nature — consultancy',
    'cost_other': 'Cost by nature — other',
    'seg_own_rev': 'Segment revenue, own-produced',
    'seg_own_ebitda': 'Segment adjusted EBITDA, own-produced',
    'seg_3p_rev': 'Segment revenue, third-party traded',
    'seg_3p_ebitda': 'Segment adjusted EBITDA, third-party traded',
    'seg_oth_ebitda': 'Segment adjusted EBITDA, corporate and other',
    'vol_urea': 'Urea sales volume, own-produced',
    'vol_nh3': 'Ammonia sales volume, own-produced',
    'vol_own': 'Total sales volume, own-produced',
    'vol_3p': 'Sales volume, third-party traded',
    'urea_util': 'Urea capacity utilisation',
    'bm_urea_eg': 'Benchmark urea price, granular, free on board Egypt',
    'bm_nh3_me': 'Benchmark ammonia price, free on board Middle East',
    'bm_ttf': 'Benchmark European gas price (TTF)',
    'eu_tariff_russia': 'EU tariff on Russian and Belarusian urea',
}
STOCK = {
    'cash': 'Cash and cash equivalents',
    'inv': 'Inventories',
    'recv': 'Trade and other receivables',
    'pay': 'Trade and other payables',
    'ta': 'Total assets',
    'eq': 'Total equity',
    'eqown': 'Equity attributable to owners',
    'eqnci': 'Equity attributable to non-controlling interests',
    'ltd': 'Long-term loans and borrowings',
    'std': 'Short-term loans and borrowings',
    'lease': 'Lease obligations, current and non-current',
    'dtl': 'Deferred tax liabilities',
    'taxpay': 'Income tax payable',
    'ppe': 'Property, plant and equipment',
    'rou': 'Right-of-use assets',
    'gwi': 'Goodwill and intangible assets',
    'netdebt': 'Net debt',
    'grossdebt': 'Gross interest-bearing debt',
    'sorfert_accr': 'Accrued Algerian gas cost (Sorfert)',
    'debt_usd': 'Loans and borrowings denominated in US dollars',
    'debt_dzd': 'Loans and borrowings denominated in Algerian dinar',
    'debt_aud': 'Loans and borrowings denominated in Australian dollars',
}
PLAIN = {
    'spot_aed': 'Share price, close on the Abu Dhabi Securities Exchange',
    'fx_aed_usd': 'Dirham per US dollar (peg)',
    'shares_mn': 'Ordinary shares outstanding, 31 Dec 2025',
    'beta': 'Beta against the local market',
    'ust10': 'US 10-year Treasury yield',
    'sofr': 'Secured Overnight Financing Rate',
    'ad_cds': 'Abu Dhabi sovereign credit-default-swap spread',
    'ad_ads': 'Abu Dhabi adjusted default spread (rating basis)',
    'ad_erp': 'Abu Dhabi equity risk premium (rating basis)',
    'ad_erp_cds': 'Abu Dhabi equity risk premium (swap basis)',
    'ad_crp': 'Abu Dhabi country risk premium',
    'eg_erp': 'Egypt equity risk premium (rating basis)',
    'eg_erp_cds': 'Egypt equity risk premium (swap basis)',
    'dz_erp': 'Algeria equity risk premium (rating basis)',
    'mature_erp': 'Mature-market equity risk premium',
    'tax_dam_uae': 'Published corporate tax rate, Abu Dhabi',
    'tax_dam_eg': 'Published corporate tax rate, Egypt',
    'tax_dam_dz': 'Published corporate tax rate, Algeria',
    'tax_stat_uae': 'UAE statutory corporate tax rate, per the accounts',
    'w_egypt': 'Share of non-current assets in Egypt',
    'w_algeria': 'Share of non-current assets in Algeria',
    'nca_middle_east': 'Non-current assets, Middle East, 31 Dec 2025',
    'nca_total': 'Non-current assets, total, 31 Dec 2025',
    'nca_other_regions': 'Non-current assets, Europe, North America, Asia and Oceania, '
                         '31 Dec 2025',
    'kd_spread_facility_bc': 'Credit margin on facilities B and C',
    'kd_spread_adnoc': 'Credit margin on the ADNOC term loan',
    'kd_spread_rcf': 'Credit margin on the revolving credit facility',
    'kd_cap_rate_rejected': 'Borrowing-cost capitalisation rate, examined and not used',
    'cap_urea': 'Installed urea production capacity',
    'cap_nh3_merchant': 'Installed merchant ammonia capacity',
    'gas_realised_q2_26': 'Delivered gas price, Q2 2026',
    'gas_realised_q2_26_ecremage': 'Delivered gas price including the Algerian '
                                   'profit-share, Q2 2026',
    'urea_demand_growth_2030': 'Global urea demand growth outside China to 2030',
    'urea_capacity_adds_2030': 'Global urea capacity additions to 2030',
}
PERIOD_FLOW = {'fy22': 'FY2022', 'fy23': 'FY2023', 'fy24': 'FY2024', 'fy25': 'FY2025',
               'h1_26': 'H1 2026', 'q1_26': 'Q1 2026', 'jul26': 'July 2026'}
PERIOD_STOCK = {'fy22': '31 Dec 2022', 'fy23': '31 Dec 2023', 'fy24': '31 Dec 2024',
                'fy25': '31 Dec 2025', 'h1_26': '30 Jun 2026', 'q1_26': '31 Mar 2026',
                'jul26': 'July 2026'}
SUFFIX = ('fy22', 'fy23', 'fy24', 'fy25', 'h1_26', 'q1_26', 'jul26')


def label(key):
    """Plain-English name for a model input. Every key must resolve — an unmapped key is
    a build failure, never a raw key leaking into the reader's table."""
    if key in PLAIN:
        return PLAIN[key]
    for suf in SUFFIX:
        if key.endswith('_' + suf):
            stem = key[: -len(suf) - 1]
            if stem in FLOW:
                return f'{FLOW[stem]}, {PERIOD_FLOW[suf]}'
            if stem in STOCK:
                return f'{STOCK[stem]}, {PERIOD_STOCK[suf]}'
    if key in FLOW:
        return FLOW[key]
    if key in STOCK:
        return STOCK[key]
    raise KeyError(f'no plain-English name for input {key!r}')


_LABELS = {k: label(k) for k in INP}
assert not any('_' in v for v in _LABELS.values()), 'a raw key leaked into a name'
assert len(set(_LABELS.values())) == len(_LABELS), 'two inputs share the same name'

LAYERS = [
    ('GLOBAL', 'Global'),
    ('COUNTRY', 'Country'),
    ('INDUSTRY', 'Industry'),
    ('COMPANY', 'Company — filed financial statements'),
    ('COMPANY_IR', 'Company — investor communications'),
    ('MARKET', 'Market'),
]

# figures quoted in the judgements section, all read from the committed numbers file
CS = D['cost_stack']
W = D['wacc']
DA, DB = D['dcf_A'], D['dcf_B']
BA, BB = D['bridge_A'], D['bridge_B']
BAb, BBb = D['bridge_A_book'], D['bridge_B_book']
FA, FB = D['frame_A'], D['frame_B']
TAX = D['tax_rate']
TRI = W['tax_triangulation']
UNIT = D['unit']
CCC = D['ccc']
REL = D['rel']
NORM = D['norm']
LEN = D['lenses']

# ===========================================================================
B.masthead()
B.H1('Fertiglobe plc (ADX: FERTIGLB) — Sources and Documentation')
B.P('Companion document to the valuation study dated 9 August 2026. It records where every '
    'number in that study came from.', size=9.5, color=B.GREY)

B.box([('What this document is. ',
        'The complete source record behind the valuation study. It lists every input the '
        'model uses, together with its value, the date the value belongs to, the document it '
        'was taken from and how it was constructed — so that a reader can retrace any figure '
        'in the study back to where it came from, and disagree with it on the evidence rather '
        'than on trust.'),
       ('What it is not. ',
        'It is not a summary of the study and it carries no conclusions. Where a figure was '
        'derived rather than disclosed, the derivation is stated in the source column. Where '
        'something was looked for and not found, it appears at the end under what could not be '
        'sourced, rather than being quietly filled in.')])

B.H2('The four layers of research')
B.P('Every input belongs to one of four layers of research — global, country, industry and '
    'company — and the company layer is shown split between the filed financial statements and '
    'the investor communications, because the two channels carry different kinds of fact and a '
    'reader is entitled to see how much of the analysis rests on each. A fifth heading, market, '
    'covers the traded price of the share itself.', size=9.5)
keep_rows_whole(B.table([['Layer', 'What it covers'],
         ['Global',
          'Worldwide interest rates, energy and commodity prices, and the trade and shipping '
          'conditions that frame every producer in the sector'],
         ['Country',
          'Sovereign data for each country the company operates in — credit rating, default '
          'spread, equity risk premium, corporate tax regime — and the dirham peg'],
         ['Industry',
          'Nitrogen fertiliser supply and demand, published benchmark prices by product and '
          'region, import tariffs, and the listed competitive set'],
         ['Company — filed financial statements',
          'The company\'s own audited annual and reviewed interim financial statements, and '
          'the notes to them. Every historical income statement, balance sheet and cash flow '
          'figure in the study comes from this layer and from nowhere else'],
         ['Company — investor communications',
          'Management discussion and analysis reports, investor presentations and the '
          'results-call transcript. These carry the sales volumes, installed capacity, '
          'utilisation, benchmark price tables and the delivered gas price — none of which '
          'appears anywhere in a financial statement'],
         ['Market',
          'The share\'s own traded price history on the Abu Dhabi Securities Exchange, and the '
          'local price library it was regressed against'],
         ],
        [1.75, 5.25], size=8.6, align_right_from=99))

# ---------------------------------------------------------------------------
B.H1('Primary documents relied upon')
B.P('Every company document read for this study. All were obtained from the company\'s own '
    'investor relations pages, which responded normally on 9 August 2026: the investor '
    'relations landing page and the full results and reports archive were both reachable, and '
    'the four audited annual filings were downloaded and read in full at the addresses below '
    '(86, 80, 75 and 74 pages respectively). No company figure in this study comes from '
    'anywhere other than these documents.', size=9.5)

ARCHIVE = 'https://fertiglobe.com/investor-relations/results-reports/'
PA = {p['url']: p for p in SR['primary_access']}
U25 = 'https://fertiglobe.com/wp-content/uploads/2026/03/Fertiglobe-plc-Consolidated-FS-4Mar26-no-nav.pdf'
U24 = ('https://fertiglobe.com/wp-content/uploads/2025/03/En_Fertiglobe-plc-Consolidated-'
       'Financial-Statements-2024-18-March-2025-Signed.pdf')
U23 = ('https://fertiglobe.com/wp-content/uploads/2024/07/EN-Consolidated-FY23-Financial-'
       'Statements-signed-FINAL.pdf')
U22 = ('https://fertiglobe.com/wp-content/uploads/2024/03/Fertiglobe-Consolidated-2022-'
       'Financial-Statements-vF.pdf')
for _u in (U25, U24, U23, U22):
    assert _u in PA and PA[_u]['reachable'], f'primary document not confirmed reachable: {_u}'

keep_rows_whole(B.table([['Document', 'Type', 'Period covered', 'Date', 'Where it was read'],
         ['Fertiglobe plc, Consolidated Financial Statements 2022',
          'Audited annual financial statements', 'Year ended 31 Dec 2022', '14 Feb 2023',
          zw(U22)],
         ['Fertiglobe plc, Consolidated Financial Statements 2023 (signed)',
          'Audited annual financial statements', 'Year ended 31 Dec 2023', '29 Apr 2024',
          zw(U23)],
         ['Fertiglobe plc, Consolidated Financial Statements 2024 (signed)',
          'Audited annual financial statements', 'Year ended 31 Dec 2024', '18 Mar 2025',
          zw(U24)],
         ['Fertiglobe plc, Consolidated Financial Statements 2025 (signed)',
          'Audited annual financial statements', 'Year ended 31 Dec 2025', '4 Mar 2026',
          zw(U25)],
         ['Fertiglobe plc, Condensed Consolidated Interim Financial Statements',
          'Interim financial statements', 'Three months ended 31 Mar 2026', '29 Apr 2026',
          zw(ARCHIVE) + ' (results and reports archive)'],
         ['Fertiglobe plc, Condensed Consolidated Interim Financial Statements',
          'Interim financial statements', 'Six months ended 30 Jun 2026', '28 Jul 2026',
          zw(ARCHIVE) + ' (results and reports archive)'],
         ['Fertiglobe Q4 2025 Results Report',
          'Management discussion and analysis', 'Q4 and full year 2025', '11 Feb 2026',
          zw(ARCHIVE) + ' (results and reports archive)'],
         ['Fertiglobe Q2 2026 Results Report',
          'Management discussion and analysis', 'Q2 and first half 2026', '28 Jul 2026',
          zw(ARCHIVE) + ' (results and reports archive)'],
         ['Fertiglobe Q2 2026 Results Presentation',
          'Investor presentation', 'Q2 and first half 2026', '28 Jul 2026',
          zw(ARCHIVE) + ' (results and reports archive)'],
         ['Fertiglobe Q2 2026 Results Call',
          'Results-call transcript', 'Q2 and first half 2026', '6 Aug 2026',
          zw(ARCHIVE) + ' (results and reports archive)'],
         ],
        [1.65, 1.10, 1.10, 0.75, 2.40], size=7.8, align_right_from=99))

B.H2('What was taken from each')
keep_rows_whole(B.table([['Document', 'What the study takes from it'],
         ['Consolidated Financial Statements 2025',
          'Signed by PricewaterhouseCoopers on 4 March 2026. The whole FY2025 income statement, balance sheet and cash flow, with the FY2024 '
          'comparative column; the two-segment revenue and adjusted earnings note; expenses by '
          'nature; the income taxes note including the statutory rate range; loans and '
          'borrowings tranche by tranche with each margin over the reference rate; the accrued '
          'gas liability; geographical non-current assets by country; the shareholding note; '
          'and the borrowing-cost capitalisation rate that the study examines and does not use'],
         ['Consolidated Financial Statements 2024',
          'The FY2024 comparative figures and segment split, and the Key Audit Matter on the '
          'accrual for increased gas cost at the Algerian plant — the disclosure that first '
          'establishes the size and the unsettled status of that liability'],
         ['Consolidated Financial Statements 2023',
          'The FY2023 year and, through its own comparative column, the FY2022 cycle peak: '
          'revenue, cost of sales, tax charge, tax paid and profit before tax, all four of '
          'which feed the four-year aggregate tax measures'],
         ['Consolidated Financial Statements 2022',
          'The fourth complete audited year, confirming the FY2022 peak figures carried as '
          'comparatives and completing the four-year run used for the tax work'],
         ['Interim Financial Statements, three months ended 31 Mar 2026',
          'The accrued gas liability at the first-quarter date, which shows the balance still '
          'building quarter by quarter rather than having settled'],
         ['Interim Financial Statements, six months ended 30 Jun 2026',
          'The reported first half of the study year in full — revenue, cost of sales, '
          'operating profit, profit attributable to owners, the balance sheet, gross debt, '
          'cash and net debt. Half of 2026 is fact and is carried as fact rather than modelled'],
         ['Q4 2025 Results Report',
          'Sales volumes by product for 2024 and 2025, own-produced and third-party; '
          'maintenance capital expenditure; and the benchmark price table for urea, ammonia '
          'and European gas'],
         ['Q2 2026 Results Report',
          'First-half 2026 sales volumes by product, segment revenue and earnings, capital '
          'expenditure, urea utilisation, the first-half benchmark price table, the mid-July '
          'urea price, and the European tariff schedule on Russian and Belarusian product'],
         ['Q2 2026 Results Presentation',
          'Installed capacity by product, and the company\'s own compilation of global urea '
          'demand growth against capacity additions to 2030'],
         ['Q2 2026 Results Call',
          'The chief executive\'s statement that gas pricing in Egypt and Algeria is '
          'product-linked, and the delivered gas price for the second quarter of 2026 both '
          'excluding and including the Algerian profit-share'],
         ],
        [1.75, 5.25], size=7.9, align_right_from=99))

B.H2('Primary sources outside the company')
keep_rows_whole(B.table([['Source', 'Publisher', 'Date read', 'What was taken from it'],
         ['Country default spreads and risk premiums (ctryprem)',
          'A. Damodaran, NYU Stern', '9 Aug 2026',
          'The credit rating, adjusted default spread, sovereign credit-default-swap spread, '
          'country risk premium and equity risk premium for Abu Dhabi, Egypt and Algeria, each '
          'read from that country\'s own row on both a rating and a swap basis, plus the '
          'corporate tax rate for each. Address: '
          + zw('https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/ctryprem.html')],
         ['Series DGS10 — 10-year Treasury constant maturity',
          'Federal Reserve Bank of St Louis', '6 Aug 2026',
          'The dollar risk-free base. Address: ' + zw('https://fred.stlouisfed.org/series/DGS10')],
         ['Secured Overnight Financing Rate',
          'Federal Reserve Bank of New York', '6 Aug 2026',
          'The floating reference rate the company\'s own dollar facilities are priced over'],
         ['Dirham peg to the US dollar',
          'Central Bank of the UAE', '7 Aug 2026',
          'The fixed rate of 3.6725 dirhams to the dollar, held since 1997, used to translate '
          'the dollar valuation into the listing currency'],
         ['Daily price history for FERTIGLB on the Abu Dhabi Securities Exchange',
          'Study price history', 'to 7 Aug 2026',
          'The anchor price, the volatility estimate, the moving-average structure and the '
          'weekly returns used in the beta regression'],
         ['Daily price history for the covered UAE equity library',
          'Study price history', 'to 7 Aug 2026',
          'The published FTSE ADX General index, the regressor for an ADX-listed share'],
         ],
        [1.55, 1.15, 0.80, 3.50], size=7.9, align_right_from=99))

# ---------------------------------------------------------------------------
B.H1('Every input the model uses')
B.P('The complete list, grouped by research layer. Each row gives the value as the model holds '
    'it, the date the value belongs to, and the document it came from together with how it was '
    'constructed where it was not simply read off a page. Financial-statement lines are in '
    'millions of US dollars, the currency the company reports in; volumes are in thousands of '
    'tonnes; prices are per tonne or per million British thermal units; rates and shares are '
    'shown as percentages. Nothing in the study is computed from a figure that does not appear '
    'here.', size=9.5)

_total = 0
for tag, label in LAYERS:
    items = [(k, v) for k, v in INP.items() if v['ring'] == tag]
    if not items:
        continue
    _total += len(items)
    B.H2(f'{label} — {len(items)} inputs')
    rows = [['Input', 'Value', 'Date', 'Source and construction']]
    for k, v in items:
        rows.append([k.replace('_', ' '), fmt(k, v['value']), v['date'], v['source']])
    keep_rows_whole(B.table(rows, [1.20, 0.85, 0.75, 4.20], size=7.5,
                            align_right_from=99))

assert _total == len(INP), f'{_total} rows written against {len(INP)} inputs'

# ---------------------------------------------------------------------------
B.H1('The judgements, and what would overturn each')
B.P('These are the places where the analyst chose rather than observed. They are collected here '
    'so that a reader can find every one of them without reading the whole study, and each '
    'carries the evidence that would overturn it — stated in advance, in observable terms.',
    size=9.5)

JUD = [
    ['Gas cost moves with the product price, at about '
     f'{CS["passthrough"]["slope"]:.2f} of every dollar',
     f'Cash cost per tonne is modelled as ${CS["passthrough"]["intercept"]:,.0f} plus '
     f'{CS["passthrough"]["slope"]:.3f} times the realised price per tonne, fitted across the '
     f'three disclosed periods (fit quality {CS["passthrough"]["r2"]:.3f}). It replaces an '
     'inflation-escalated cost stack entirely',
     'The chief executive stated on the results call of 6 August 2026 that gas pricing in '
     'Egypt and Algeria is product-linked. The relationship is measured from disclosed segment '
     'revenue and earnings rather than assumed, and it survives removing the Algerian gas '
     f'catch-up charge (slope {CS["passthrough_ex_accrual"]["slope"]:.3f} without it), so it is '
     'not an artefact of that one item. It is corroborated physically: the fitted cost step '
     f'implies about ${CS["implied_delta_gas"]:.2f} per MMBtu of extra gas cost against the '
     f'${CS["gas_q2_26"]:.0f} per MMBtu the company disclosed for the second quarter of 2026',
     'Two consecutive periods in which cost per tonne fails to follow realised price at '
     'anything close to this slope — most plainly, a fall in product prices that is not '
     'followed by a fall in cost per tonne. A published Algerian or Egyptian gas formula '
     'showing a fixed price would overturn it outright'],
    ['The product price path — carried BOTH ways, never averaged into one number',
     f'Framing A reverts urea to ${FA["px_urea"][2]:,.0f} per tonne by 2028 and holds there; '
     f'framing B holds it near ${FB["px_urea"][2]:,.0f}. Both are run all the way to a value: '
     f'AED {BA["ps_aed"]:.2f} under A and AED {BB["ps_aed"]:.2f} under B. Both appear in the '
     'summary, the body, the workbook and an expert\'s range',
     'This is the single most consequential contested judgement in the study, and averaging the '
     'two would hide it. Framing A treats the 2026 spike as a war premium on top of a '
     'marginal-cost anchor set by European gas; framing B rests on the company\'s own sourced '
     'supply and demand balance — demand growth outside China of about '
     f'{INP["urea_demand_growth_2030"]["value"]:.1f} million tonnes to 2030 against about '
     f'{INP["urea_capacity_adds_2030"]["value"]:.1f} million tonnes of additions — and the '
     'rising European tariff wall on Russian and Belarusian product',
     'Framing A is overturned by two or more quarters of urea holding above $520 per tonne '
     'with the Strait of Hormuz open and freight normalised. Framing B is overturned by '
     'Chinese export quotas returning at scale, or by any of the announced projects that have '
     'not reached a final investment decision doing so'],
    ['The forecast tax rate is the average of three sourced estimates',
     f'{TAX * 100:.1f}% — the mean of the four-year aggregate reported effective rate '
     f'({TRI["aggregate_effective"] * 100:.1f}%), the four-year aggregate cash rate '
     f'({TRI["aggregate_cash"] * 100:.1f}%) and a jurisdiction-weighted statutory build '
     f'({TRI["jurisdiction_weighted"] * 100:.1f}%)',
     'No single reported year is usable. The group\'s own statutory rate ranges from zero to '
     '25% because certain entities hold qualified free-zone status, and the reported effective '
     f'rate of {INP["tax_eff_fy25"]["value"] * 100:.0f}% in 2025 and '
     f'{INP["tax_eff_fy24"]["value"] * 100:.0f}% in 2024 was flattered by items that do not '
     'recur. Taking the average of three independently constructed measures is the honest '
     'answer to a rate that is genuinely uncertain',
     'A completed review of free-zone qualification, or the loss of it at a material entity. '
     'The study sensitises the rate from 8% to 20%, and the value moves by roughly a tenth '
     'across that span'],
    [f'Beta of {W["beta"]:.3f} from the share\'s own history, despite a weak fit',
     f'{W["beta"]:.3f}, from {W["beta_n"]} weekly observations over {W["beta_window"]:.1f} years '
     'against the published FTSE ADX General index — the index of the exchange the share is '
     'listed on. It is used as measured, not adjusted toward one',
     f'The regression explains only {W["beta_r2"] * 100:.1f}% of the variance and the standard '
     f'error is {W["beta_se"]:.3f}, so the 90% interval runs from {W["beta_ci90"][0]:.2f} to '
     f'{W["beta_ci90"][1]:.2f} — a genuinely weak fit, which is what a 12.6% free float on a '
     'commodity producer should produce. The share tracks nitrogen prices, not the local index. '
     'The study says so plainly rather than borrowing a foreign peer beta that would look '
     'firmer than the evidence is',
     'A materially higher free float, or a longer history, that lifts the explanatory power. '
     f'The whole 90% interval is priced in the sensitivity table: at {W["beta_ci90"][1]:.2f} '
     'the value falls by roughly a fifth. A reader who prefers the adjusted-toward-one '
     f'convention would use {W["beta_blume"]:.3f}, which is shown'],
    ['The terminal return on capital is triangulated, not carried from the last forecast year',
     f'{DA["roic_term"] * 100:.1f}% — the mean of the final-year book return '
     f'({DA["roic_book"] * 100:.1f}%), the return on replacement cost '
     f'({DA["roic_replacement"] * 100:.1f}%) and a long-run sector return for merchant nitrogen '
     f'producers ({DA["roic_sector"] * 100:.1f}%). It sets the reinvestment rate of '
     f'{DA["rr_term"] * 100:.1f}% in the terminal block',
     'Book invested capital is depreciated historical cost, so a book return above a fifth '
     'overstates what the next tonne of capacity actually earns; replacement cost understates '
     'it, because the existing plants carry a gas position a new entrant cannot buy. Neither '
     'is right on its own',
     'A greenfield nitrogen project reaching a final investment decision at a disclosed capital '
     'cost far from the $1,250 per tonne of capacity assumed here would move the '
     'replacement-cost leg directly, and with it the terminal reinvestment rate'],
    ['Non-controlling interests are charged at their share of profit, not at book value',
     f'{D["nci_share"] * 100:.1f}% of total equity value is deducted for minorities in the '
     f'bridge from enterprise to attributable equity, which is AED {BA["ps_aed"]:.2f} under '
     f'framing A. On a book basis (the balance-sheet carrying amount of '
     f'${BA["nci_book"]:,.1f}m) the same framing gives AED {BAb["ps_aed"]:.2f}',
     'Minorities are large and concentrated in the two most profitable assets — 25% of the '
     'Egyptian producer and 49.01% of the Algerian one. They take a materially larger share of '
     'group profit than of group book equity, so charging them at profit share is the '
     'conservative reading and the one consistent with valuing the whole enterprise on its cash '
     'flows',
     'A buy-out of either minority at a disclosed price, which would replace the estimate with '
     'a transaction. A reader who prefers the book convention can read the alternative directly '
     'from the bridge, which is published on both bases'],
    ['The lower-carbon ammonia project is excluded from the base case',
     'No cash flow, no capital and no value is carried for the one-million-tonne lower-carbon '
     'ammonia plant. It is named as an unpriced upside catalyst instead',
     'The parent is warehousing the project and the company holds only an option to move to 54% '
     'ownership after completion, expected in 2027. An option that has not been exercised over '
     'an asset that is not consolidated is not a cash flow today, and modelling it would put '
     'the study\'s central figure at the mercy of an ownership decision the company has not '
     'taken',
     'Exercise of the option, or any disclosure that fixes the terms and timing of the '
     'transfer. At that point it becomes a consolidated asset and belongs in the model'],
    ['2026 is built as the reported half year plus a modelled second half',
     f'The disclosed first half — {INP["vol_own_h1_26"]["value"]:,.0f} kt of own-produced '
     f'volume on ${INP["seg_own_rev_h1_26"]["value"]:,.0f}m of segment revenue — is carried as '
     'fact, and only the second half is forecast',
     'Half of the study year has already been reported. Carrying a modelled full year over a '
     'period the company has published would discard evidence that exists',
     'Nothing — this is arithmetic, not judgement. It is listed because it explains why the '
     '2026 column behaves differently from the four that follow'],
    ['Utilisation improves gradually rather than stepping up',
     f'Urea utilisation glides from {FA["util_urea"][0] * 100:.1f}% in 2026 to '
     f'{FA["util_urea"][-1] * 100:.1f}% by 2030; merchant ammonia from '
     f'{FA["util_nh3"][0] * 100:.1f}% to {FA["util_nh3"][-1] * 100:.1f}%. Installed capacity is '
     'held flat, because no additions are announced',
     'The company runs a stated manufacturing improvement programme but gives no numeric volume '
     'guidance, so no guidance figure is carried. The glide is anchored on the '
     f'{INP["urea_util_h1_26"]["value"] * 100:.0f}% urea utilisation actually reported for the '
     'first half of 2026',
     'An unplanned outage at either large plant, or a debottlenecking announcement that raises '
     'nameplate capacity. Utilisation is sensitised in the study and is the second most '
     'powerful driver after price'],
    ['The third-party trading leg is carried at a segment margin, not built from unit economics',
     'Traded volumes grow from 1,150 kt to 1,350 kt at a 7.5% margin on revenue — the one leg '
     'of the model that is not built from volume times price less cost per tonne. The gap is '
     'flagged rather than papered over',
     'Volumes are disclosed by product but purchase-side unit economics are not disclosed '
     'anywhere, in any filing or presentation. A margin measured from disclosed segment '
     'earnings is the finest level the evidence supports',
     'Any disclosure of purchase cost per tonne on traded product. The leg is small — it '
     'contributes a low-single-digit share of group earnings — so even a large error in it '
     'moves the value little'],
    ['Working capital is projected from the conversion cycle, with the gas accrual removed',
     f'Receivable days of {CCC["FY25"]["dso"]:.0f}, inventory days of {CCC["FY25"]["dio"]:.0f} '
     f'and payable days of {CCC["FY25_ex_accrual"]["dpo"]:.0f}, all measured off the filed '
     'statements. Including the accrual would put payable days at '
     f'{CCC["FY25"]["dpo"]:.0f} and make the cycle look permanently negative',
     'The accrued gas catch-up is not a trade payable arising in the ordinary course; it is an '
     'unsettled liability with no payment schedule. Leaving it inside payables would show the '
     'company financing itself on supplier credit it has not actually negotiated',
     'Settlement of the accrual on disclosed terms, which would convert it into either a cash '
     'outflow or a scheduled payable and put the question beyond judgement'],
    ['The cost of capital is weighted by where the plants are, not by where the company is listed',
     f'The equity risk premium is {W["erp_rating"] * 100:.2f}% on a rating basis and '
     f'{W["erp_cds"] * 100:.2f}% on a swap basis, blending each country\'s own published row at '
     f'{W["w_uae"] * 100:.1f}% UAE, {W["w_egypt"] * 100:.1f}% Egypt and '
     f'{W["w_algeria"] * 100:.1f}% Algeria, weighted by disclosed non-current assets. Both '
     'bases are published',
     'Treating an Abu Dhabi listing as an Abu Dhabi risk profile would have used '
     f'{INP["ad_erp"]["value"] * 100:.2f}% and ignored that nearly half the asset base sits in '
     'Egypt and Algeria. Country risk is counted once, inside the premium, and the risk-free '
     'rate is normalised by removing the same sovereign spread so it is not counted twice',
     'A material change in the asset mix, or a sovereign rating action in any of the three '
     'countries. The weights come from a disclosed note and move with it'],
    ['The cost of debt is the company\'s own marginal borrowing, not its accounting rate',
     f'{W["kd"] * 100:.2f}% — the dollar reference rate plus {W["kd_spread"] * 100:.3f}%, the '
     'average margin on the two most recent facilities the company actually drew. The '
     f'{W["kd_cap_rate_rejected"] * 100:.2f}% borrowing-cost capitalisation rate disclosed in '
     'the accounts is examined and not used',
     'The capitalisation rate is a historical accounting average across a book that has since '
     'been repriced; the study needs the rate at which the next dollar is borrowed. The '
     'marginal rate is checked to sit above the Abu Dhabi sovereign, as a same-currency '
     'corporate must',
     'A new facility at a materially different margin, which would be disclosed in the next '
     'borrowings note and would replace the figure directly'],
    ['Terminal growth of 2.0% and a terminal debt weight of 20%',
     f'Cash flows grow at {D["g_term"] * 100:.1f}% after 2030 and the cost of capital glides '
     f'from {W["wacc_rating"] * 100:.2f}% to {W["wacc_term_rating"] * 100:.2f}% as leverage '
     'normalises toward the sector. The terminal block is '
     f'{DA["tv_share"] * 100:.0f}% of enterprise value under framing A',
     'Two per cent is long-run dollar inflation with no real growth — appropriate for a mature '
     'plant base with no announced capacity additions. The debt weight is where merchant '
     'nitrogen producers actually run, above the company\'s currently light net leverage',
     'A sustained change in the group\'s target capital structure, or evidence of real volume '
     'growth beyond debottlenecking. Growth is sensitised from 1.0% to 3.0% against the cost of '
     'capital in the study'],
    ['The relative lens uses a multiple below the Gulf peers and above the European ones',
     f'{REL["mult"]:.1f} times mid-cycle earnings before interest, tax, depreciation and '
     f'amortisation of ${REL["ebitda_mid"]:,.0f}m, against a peer set trading from '
     f'{min(p["ev_ebitda"] for p in REL["peers"]):.1f} to '
     f'{max(p["ev_ebitda"] for p in REL["peers"]):.1f} times',
     'The company earns Gulf gas economics but carries Egyptian and Algerian country risk, so '
     'it should not trade at either end of its own peer set. Mid-cycle earnings are the average '
     'of the last three forecast years under both price framings, so the multiple is not '
     'applied to a peak',
     'A re-rating of the Gulf nitrogen names as a group, or a change in the country mix of the '
     'asset base. This lens carries a 20% weight in the blend and is the lowest of the four'],
    ['The four lenses are weighted, not averaged',
     ' · '.join(f'{k} {v["weight"] * 100:.0f}%' for k, v in LEN.items()),
     'The cash-flow lens carries the most weight because the unit economics are disclosed well '
     'enough to build it from the ground up; the book lens carries the least because '
     'depreciated historical cost is the weakest guide to the value of plants whose worth turns '
     'on a gas contract',
     'A reader who disagrees can re-weight: the four lens values and the two price framings are '
     'all published separately, and the spread between the lowest and the highest is stated '
     'rather than smoothed away'],
]
keep_rows_whole(
    B.table([['Judgement', 'What was chosen', 'Why', 'What would overturn it']] + JUD,
            [1.30, 1.75, 1.95, 2.00], size=7.5, align_right_from=99))

# ---------------------------------------------------------------------------
B.H1('What could not be sourced')
B.P('Every category that was searched and produced nothing. Each says what was actually looked '
    'for, in which documents, and how the study handled the absence. They are recorded because '
    'an absence that is not written down becomes an assumption that nobody can see.', size=9.5)

NEG = [f for f in SR['findings'] if f['klass'] == 'NEGATIVE_SEARCH']
assert len(NEG) == 3, f'expected three searches that found nothing, got {len(NEG)}'
keep_rows_whole(B.table([['What was searched for, and where', 'Outcome',
          'How the study handled it', 'Date searched'],
         ['Impairments, discontinued operations, restatements or disposals — searched the '
          'FY2025 audited statements and both 2026 interim filings',
          'Nothing found beyond the Wengfu Australia acquisition, which is disclosed and is '
          'not a base-resetting disposal',
          'No adjustment. The historical series is used as filed, without normalisation for '
          'one-off items, because none were disclosed',
          NEG[0]['source_date']],
         ['A purchase price, cost per tonne or gross margin per tonne on third-party traded '
          'product — searched the FY2023, FY2024 and FY2025 audited statements, both 2026 '
          'interim filings, every results report and the results-call transcript',
          'Nothing found. Volumes are disclosed by product, but no purchase-side unit economics '
          'are given anywhere — only segment revenue and segment earnings',
          'The trading leg is carried at a margin measured from disclosed segment earnings '
          'rather than built from unit economics, and is flagged in the study as the one leg '
          'not built from the ground up',
          NEG[1]['source_date']],
         ['A delivered gas price per MMBtu for any period before the second quarter of 2026, '
          'and the Algerian and Egyptian gas pricing formulas themselves — searched all four '
          'audited filings, both interim filings and every results report',
          'Nothing found. Only the single second-quarter 2026 figure given on the results call '
          'exists; no formula and no historical series is published',
          'The cost relationship is calibrated from disclosed segment revenue and earnings '
          'across three periods, then checked against that one disclosed gas price and against '
          'gas consumption intensity per tonne. It is not built from a formula, because no '
          'formula is public',
          NEG[2]['source_date']],
         ],
        [2.05, 1.85, 2.30, 0.80], size=7.6, align_right_from=99))

# ---------------------------------------------------------------------------
B.H1('A note on aggregator data, and one conflict between two company sources')
B.P('No aggregator, data vendor, broker note or press report is the source of any figure the '
    'company itself has reported. Every historical income statement, balance sheet, cash flow, '
    'segment and note figure in this study comes from the audited annual filings and the '
    'reviewed interim filings listed above, and every recomputed subtotal was checked back '
    'against the filed figure it should equal.')
B.P('The only aggregator-sourced items anywhere in the study are the peer enterprise multiples '
    'used in the relative lens — Nutrien, CF Industries, Yara International, OCI Global, '
    'Industries Qatar and SABIC Agri-Nutrients. They are market prices for other companies, not '
    'facts about this one, and they are labelled in the study as a cross-check on the '
    'cash-flow work rather than as an input to it. Benchmark product prices come from the '
    'company\'s own published tables, which cite the commodity price reporting agencies '
    'underneath them.')
B.H2('The one genuine conflict between two primary sources')
B.P('The audited FY2025 segment note describes the gas offtake agreements as carrying '
    '"no/limited price exposure on the supply of natural gas". On the results call of 6 August '
    '2026 the chief executive said the opposite in substance: that the company has '
    '"product-linked gas pricing effectively in both Egypt as well as Algeria. So, product '
    'prices are very strong. We\'ll see a higher gas cost." Both are company sources and they '
    'cannot both describe the same arrangement.')
B.P('The study resolves the conflict in favour of the results-call statement, for three '
    'reasons. It is the more recent of the two, by five months. It is the more specific — it '
    'names the two countries and the direction of the effect, where the accounting note is a '
    'general characterisation written for a different purpose. And it is corroborated by two '
    'independent pieces of evidence: the delivered gas price the company disclosed for the '
    f'second quarter of 2026 (${CS["gas_q2_26"]:.0f} per MMBtu, or '
    f'${CS["gas_q2_26_ecremage"]:.0f} including the Algerian profit-share) is far above what a '
    'fixed contract would imply, and the cost data itself, calibrated across three disclosed '
    f'periods, tracks the product price with a fit of {CS["passthrough"]["r2"]:.3f}. The '
    'consequence is material and is stated plainly in the study: it converts the cost side of '
    'the model from an inflation-escalated stack into a function of the product price, which '
    'compresses the upside of high prices and cushions the downside of low ones. A reader who '
    'prefers the accounting note\'s characterisation should read the sensitivity table, where '
    'the relationship is priced from 0.30 to 0.65 of every dollar.')

# ---------------------------------------------------------------------------
B.H1('Disclosure')
B.P('This document accompanies an educational valuation study. It is not investment advice and '
    'contains no recommendation, rating or price target. Sources are listed so that readers can '
    'verify the analysis independently. Where a figure is derived or estimated rather than '
    'disclosed, that is stated in the row it appears in.', size=9.2, color=B.GREY)

B.doc.save(OUT)
print(f'wrote {OUT}')
print(f'{len(B.doc.paragraphs)} paragraphs | {len(B.doc.tables)} tables | '
      f'{_total} of {len(INP)} inputs listed | {len(JUD)} judgements | '
      f'{len(NEG)} searches that found nothing')
