"""ADNOC Drilling — the standalone bibliography and input register.

Everything the study rests on, in one document: the primary documents actually
read, every single input with its value, date, source and construction, the
judgements and what would overturn each of them, what was looked for and NOT
found, and where a third-party figure disagreed with a primary one.
"""
import json, os
from docx_base import Doc, INK, GREY, BRASS, F_CREAM, F_PANEL2

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, 'study_numbers.json')))
BETA = json.load(open(os.path.join(HERE, 'beta_result.json')))
IN = D['inputs']

LAYER = {
    'Company': 'Company — audited and reviewed financial statements',
    'Company/IR': 'Company — investor communications',
    'Country': 'Country',
    'Global': 'Global',
    'Industry': 'Industry',
    'Market': 'Market',
    'House': 'Analyst judgement',
}
LAYER_ORDER = ['Company', 'Company/IR', 'Industry', 'Country', 'Global', 'Market', 'House']

d = Doc()
P, T = d.P, d.table

d.masthead()
P('ADNOC Drilling Company P.J.S.C.', size=20, bold=True, space_after=2)
P('Bibliography and input register', size=13, bold=True, color=BRASS, space_after=4)
P('Companion to the valuation study of 9 August 2026', size=10.5, color=GREY, space_after=12)

d.box([('Why this document exists. ', 'A valuation is only as good as what it was built from. '
        'This document lists every source that was read, every number that entered the model '
        'with its value and its date, every judgement that was made and what would overturn it, '
        'and — just as important — everything that was looked for and could not be found.'),
       ('The rule that governs it. ', 'Every historical figure about ADNOC Drilling comes from '
        'the company\'s own issued financial statements and disclosures, read from an official '
        'source. No data vendor, broker note, press report or search-result extract is a source '
        'for any figure about the company itself. Third-party data appears in exactly one '
        'place — the peer comparison — and is labelled as such.')])

# ============================== PRIMARY DOCUMENTS ============================
d.H1('1. Primary documents read')
rows = [['Document', 'Period', 'Status', 'Signed / issued', 'Where it was obtained']]
DOCS = [
    ('Reports and consolidated financial statements', 'Year ended 31 December 2023',
     'Audited — KPMG Lower Gulf Limited, unqualified opinion', '12 February 2024',
     'adnocdrilling.ae — investor relations, financial results and presentations'),
    ('Reports and consolidated financial statements', 'Year ended 31 December 2024',
     'Audited — Deloitte & Touche (M.E.), unqualified opinion', '11 February 2025',
     'adnocdrilling.ae — investor relations'),
    ('Reports and consolidated financial statements', 'Year ended 31 December 2025',
     'Audited — Deloitte & Touche (M.E.), unqualified opinion', '11 February 2026',
     'adnocdrilling.ae — investor relations'),
    ('Condensed consolidated interim financial information', 'Three months to 31 March 2026',
     'Reviewed', 'May 2026', 'adnocdrilling.ae — investor relations'),
    ('Condensed consolidated interim financial information', 'Six months to 30 June 2026',
     'Reviewed', '30 July 2026', 'adnocdrilling.ae — investor relations'),
    ('Management discussion and analysis', 'Full year 2023', 'Company-issued',
     'February 2024', 'adnocdrilling.ae — investor relations'),
    ('Management discussion and analysis', 'Full year 2024', 'Company-issued',
     'February 2025', 'adnocdrilling.ae — investor relations'),
    ('Management discussion and analysis', 'Full year 2025', 'Company-issued',
     'February 2026', 'adnocdrilling.ae — investor relations'),
    ('Management discussion and analysis', 'First quarter 2026', 'Company-issued',
     'May 2026', 'adnocdrilling.ae — investor relations'),
    ('Management discussion and analysis', 'First half 2026', 'Company-issued',
     '30 July 2026', 'adnocdrilling.ae — investor relations'),
    ('Earnings presentation', 'Full year 2025', 'Company-issued', 'February 2026',
     'adnocdrilling.ae — investor relations'),
    ('Earnings presentation', 'Second quarter and first half 2026', 'Company-issued',
     '30 July 2026', 'adnocdrilling.ae — investor relations'),
    ('Earnings press release', 'Second quarter and first half 2026', 'Company-issued',
     '30 July 2026', 'adnocdrilling.ae — investor relations'),
    ('Earnings call and webcast transcript', 'Second quarter 2026', 'Company-issued',
     '30 July 2026', 'adnocdrilling.ae — investor relations'),
    ('Corporate presentation', '2026', 'Company-issued', '2026',
     'adnocdrilling.ae — investor relations'),
    ('Daily price history, October 2021 to 7 August 2026', 'Market data',
     '1,215 sessions, screened for corporate actions and non-trading rows before use',
     '7 August 2026', 'Supplied price file'),
]
for r in DOCS:
    rows.append(list(r))
T(rows, [1.95, 1.45, 1.85, 1.05, 1.70], size=8.4)
P('The 2023 and 2024 statements were each cross-confirmed against the following year\'s '
  'comparative column and tie to the dollar. Every statement page parsed cleanly except the '
  'signed balance-sheet page in each annual report, which is an image; those three pages were '
  'read by optical character recognition and then verified by checking that the totals foot and '
  'that each year\'s figures match the following year\'s comparative column.', size=9.5)

# ============================== THE INPUT REGISTER ===========================
d.page_break()
d.H1('2. The input register')
P('Every input to the model, grouped by the layer of research it came from. An input with no '
  'source is not permitted to enter the model — the build fails rather than proceeding.',
  space_after=6)
by_layer = {}
for key, rec in IN.items():
    by_layer.setdefault(rec['ring'], []).append((key, rec))


def fmtval(v):
    if isinstance(v, str):
        return v
    if abs(v) >= 1000:
        return f'{v:,.1f}'
    if abs(v) < 1:
        return f'{v:.4f}'
    return f'{v:,.3f}'


for layer in LAYER_ORDER:
    items = by_layer.get(layer)
    if not items:
        continue
    d.H2(LAYER[layer])
    rows = [['Input', 'Value', 'Date', 'Source and construction']]
    for key, rec in sorted(items):
        rows.append([key.replace('_', ' '), fmtval(rec['value']), rec['date'], rec['source']])
    T(rows, [1.45, 0.90, 0.85, 3.80], size=8.0, align_right_from=1)

# ============================== JUDGEMENTS ===================================
d.page_break()
d.H1('3. Judgements, and what would overturn each one')
rows = [['Judgement', 'What was decided', 'Why', 'What would overturn it']]
JUD = [
    ('The company is an operating company, not a holding company',
     'Valued on the cash its own fleet generates, primarily by discounted cash flow',
     'Three operating segments with no inter-segment sales, property and equipment two-thirds '
     'of total assets, no lending book, no investment property, and only two small '
     'equity-accounted service joint ventures',
     'A restructuring that turned the company into a holder of stakes rather than an operator'),
    ('The valuation runs in US dollars',
     'The model is built in dollars and converted to dirhams at the peg',
     'The company states in its accounts that the dollar is its functional and presentation '
     'currency; re-expressing three audited years into dirhams would add translation noise the '
     'source data does not contain',
     'A change of functional currency, or the end of the dirham peg'),
    ('The terminal question is computed both ways rather than resolved',
     'Two full discounted-cash-flow cases, weighted equally, published side by side',
     'The company has explicitly declined to guide beyond 2026 until phasing is fixed, so there '
     'is no evidential basis on which to prefer one',
     'Published 2027 and medium-term guidance'),
    ('The beta is the company\'s own regression',
     f'{BETA["beta"]:.3f}, from a five-year weekly regression against a local composite',
     f'The listing dates from October 2021, so a full five-year window exists and clears the '
     f'usability standard: {BETA["n"]} observations, R-squared {BETA["r2"]:.3f}, standard error '
     f'{BETA["se"]:.3f}',
     'A materially different beta from a longer record, or a stress episode that breaks the '
     'historical correlation. The valuation is more sensitive to this than to any other input'),
    ('The cost of debt is term-matched, not spot',
     f'{D["wacc"]["kd_pretax"]*100:.2f}%, the five-year Treasury yield plus the company\'s own '
     f'0.75% facility margin',
     'A five-year facility should be priced off a five-year rate. The spot floating cost and '
     'the trailing accounting rate were both computed and both fail the test that a '
     'same-currency corporate cannot borrow below its own sovereign',
     'A new facility priced differently, or a change in the sovereign spread'),
    ('The unconventional programme earns almost no margin',
     f'{IN["unconv_ebitda_margin"]["value"]*100:.1f}% EBITDA margin, triangulated two ways in '
     f'the workbook and averaged there',
     'The company discloses a conventional EBITDA margin separately from the group margin; the '
     'difference between them, applied to the disclosed unconventional revenue, is what is left',
     'A disclosed segment margin for the unconventional business, or a materially different '
     'group margin once the programme runs off'),
    ('Revenue per regional rig is roughly 40% of the Abu Dhabi rate',
     f'USD {IN["rev_per_rig_regional"]["value"]/1e3:.1f} million per rig-year',
     'Derived by subtracting the Abu Dhabi fleet at its disclosed realised rate from the '
     'reported first-half onshore revenue, leaving what the regional rigs earned',
     'A full year of reported regional data, which does not yet exist'),
    ('Terminal return on invested capital fades to 18%',
     'From a demonstrated 23% return on capital employed',
     'Holding 23% in perpetuity capitalises an incumbency that faces renegotiation at every '
     'contract roll; fading to the cost of capital would contradict a record sustained through '
     'a full commodity cycle',
     'A contract renewal at materially different terms'),
    ('Costs escalate one class at a time',
     'A wage index on labour, an oilfield-services index on maintenance and equipment hire, and '
     'the commodity\'s own path on fuel',
     'A single blended index across physically different cost lines manufactures a margin trend '
     'that is an artifact of the assumption rather than of the business',
     'Disclosure of the actual contractual escalation mechanics, which are not published'),
    ('Debt is held flat and only the guided dividend floor is paid',
     'Cash accumulates and net debt turns negative by 2030',
     'The company guides to leverage below 2.0 times and runs at 1.0 times, and the dividend '
     'floor is the only distribution it has committed to',
     'Any capital-allocation announcement. This affects the forecast balance sheet, not the '
     'enterprise value'),
]
for j in JUD:
    rows.append(list(j))
T(rows, [1.45, 1.70, 2.60, 2.25], size=8.0)

# ============================== NEGATIVE RESULTS =============================
d.page_break()
d.H1('4. Negative results — what was looked for and not found')
P('A register of sources is only honest if it records the searches that failed. Each row below '
  'is something this study would have used and could not obtain, together with what was done '
  'instead.', space_after=6)
rows = [['What was sought', 'Where', 'Outcome', 'What was done instead']]
NEG = [
    ('Contract tenor, day-rate mechanics and repricing terms',
     'All annual and interim filings, all management commentary, the corporate presentation and '
     'the second-quarter 2026 earnings call transcript',
     'Not disclosed anywhere. The company describes its revenue base as "highly contracted" and '
     'as supporting visibility "through at least 2030", but publishes no tenor, no rate and no '
     'escalation mechanism',
     'Realised revenue per rig-year is derived from disclosed segment revenue and disclosed rig '
     'counts, and escalated at domestic inflation rather than at an assumed contractual rate. '
     'The gap is flagged in the study caveats'),
    ('Backlog on the basis other listed drillers report it',
     'All filings',
     'Not published. The accounts disclose USD 19.4 million of unsatisfied performance '
     'obligations, which is a revenue-recognition measure covering work already promised and '
     'not a contract backlog',
     'The contracted-cash-flow expert treats the five forecast years as the contracted book '
     'rather than relying on a published backlog figure, and says so'),
    ('Guidance for 2027 and beyond',
     'The full-year 2025 results, the first-quarter 2026 results and the first-half 2026 results',
     'Withheld. The company states guidance will be provided "as the phasing for additional '
     'rigs and additional OFS volumes is finalized"',
     'The study carries two full cases instead of one, weighted equally, and does not average '
     'them'),
    ('A separately disclosed margin for the unconventional business',
     'All filings and management commentary',
     'Not disclosed. Only a conventional margin and a group margin are published',
     'The unconventional margin is inferred from the difference between the two, by two '
     'independent methods that are shown and averaged in the workbook'),
    ('Segment-level results for the acquired regional businesses',
     'First-quarter and first-half 2026 filings',
     'Not disclosed separately. The regional rigs are consolidated into the Onshore segment',
     'Revenue per regional rig is derived by subtraction and flagged as the least well-supported '
     'unit rate in the model'),
    ('The exchange disclosure portal',
     'adx.ae',
     'Returned an access error from this environment on 9 August 2026',
     'Not required. Every filing was obtained directly from the company, which is the primary '
     'source in any case'),
    ('A dirham-denominated government bond curve',
     'The central bank of the United Arab Emirates and general market data sources',
     'The central bank site returned an access error and the market data source refused the '
     'connection',
     'Not required for the valuation, which is built in US dollars because the cash flows are. '
     'A dirham-basis cross-check would need this curve and is therefore not published rather '
     'than being estimated'),
    ('Peer rig counts, to compute enterprise value per rig',
     'Peer disclosures',
     'Not gathered. Collecting rig counts on a consistent definition across thirteen peers was '
     'beyond what the peer cross-check needed',
     'The relative lens uses enterprise value to EBITDA, which is computable consistently from '
     'each peer\'s own reported figures'),
]
for n in NEG:
    rows.append(list(n))
T(rows, [1.55, 1.55, 2.35, 2.55], size=8.0)

# ============================== THIRD-PARTY DATA =============================
d.H1('5. Third-party data, and where it disagrees')
P('Third-party data appears in exactly one place in this study: the peer comparison. Peer '
  'prices are market observations at the close on 7 August 2026; peer revenue, EBITDA, debt, '
  'cash and share counts are each company\'s own reported figures as redistributed by a market '
  'data service. That is a cross-check use — the relative lens applies a peer MULTIPLE to ADNOC '
  'Drilling\'s OWN audited and guided EBITDA, so no peer figure enters this company\'s income '
  'statement, balance sheet or cash flow.', space_after=6)
rows = [['Where third-party data is used', 'What it is', 'What it is not used for']]
rows.append(['Peer enterprise values and EBITDA', 'Thirteen listed drillers and oilfield-service '
             'companies, at their own latest reported periods',
             'Any ADNOC Drilling figure'])
rows.append(['Market interest rates', 'US Treasury yields and the overnight financing rate, '
             'from the Federal Reserve H.15 release',
             'Anything company-specific'])
rows.append(['Equity risk premium and sovereign spreads',
             'Damodaran country default spreads and risk premiums, file dated 5 January 2026, '
             'Abu Dhabi row', 'Anything company-specific'])
rows.append(['Commodity and price indices',
             'Brent, US producer price index for drilling oil and gas wells, and United Arab '
             'Emirates consumer price inflation, all via the Federal Reserve Bank of St. Louis',
             'Any company revenue or cost figure directly — they set escalation rates only'])
T(rows, [2.10, 3.10, 1.80], size=8.6)

d.H2('Discrepancies noted')
rows = [['Figure', 'Primary source', 'Elsewhere', 'Resolution']]
rows.append(['Current trade and other payables at 31 December 2025', 'USD 1,039.4 million on '
             'the face of the balance sheet',
             'USD 1,030.8 million in the financial-instruments maturity table',
             'Both are correct and neither is an error: the maturity table covers financial '
             'liabilities only and excludes non-financial items such as contract liabilities. '
             'The balance-sheet figure is used'])
rows.append(['Total rig count at the end of 2025', '140 rigs on the reported basis',
             '169 rigs on the pro-forma basis in the same document',
             'The pro-forma count includes 29 regional rigs from two transactions that had not '
             'closed. The reported 140 is used for 2025 and the regional rigs enter from 2026, '
             'when they were actually consolidated'])
rows.append(['Capital expenditure for 2025',
             'USD 805.2 million of cash purchases of property and equipment in the cash-flow '
             'statement',
             'USD 772 million described as capital expenditure in the management commentary',
             'The two are defined differently — the commentary figure includes prepaid delivery '
             'payments and excludes accruals. The cash-flow statement figure is used, plus '
             'intangibles, because it is the audited one'])
T(rows, [1.55, 2.10, 2.05, 3.30], size=8.0)

d.H1('6. Software and method')
P('The model, the figures and both delivered documents are generated from one committed numbers '
  'file, so no figure can differ between the study, the workbook and this bibliography. The '
  'delivered workbook is verified by an independent recalculation that evaluates every formula '
  'and requires each one to reproduce the model, and by a driver test that perturbs every input '
  'in place and requires the headline to move in the direction asserted before the test was '
  'run. The results of both are reported in the study\'s quality-control table.')

OUT = os.path.join(HERE, 'ADNOCDRILL_Bibliography_09-08-2026.docx')
d.save(OUT)
print(f'wrote {OUT}')
print(f'  {len(d.doc.paragraphs)} paragraphs, {len(d.tables)} tables, '
      f'{len(IN)} inputs registered')
