"""EIPICO_Bibliography_09-08-2026.docx — the standalone bibliography document.

Five things, in order: the primary documents actually read; the FULL input register (every
input with its value, date and construction, grouped by research layer); the judgements, each
with what would overturn it; the negative results; and the places where a secondary source
disagrees with, or reports beyond, the audited filing.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import docx_base as B
from docx.shared import Pt

doc, P, H1, H2, table, box, caption, masthead = (B.doc, B.P, B.H1, B.H2, B.table, B.box,
                                                 B.caption, B.masthead)
GREY = B.GREY

D = json.load(open(os.path.join(HERE, 'study_numbers.json')))
INP = D['inputs']
SW = json.load(open(os.path.join(HERE, 'sweep_register.json')))
M = D['meta']

masthead()
P('Egyptian International Pharmaceutical Industries Company (EIPICO)', size=19, bold=True,
  space_after=1)
P('Bibliography and complete list of inputs — the companion to the valuation study of 9 August 2026',
  size=11, color=GREY, space_after=12)

# ---------------------------------------------------------------- 1. DOCUMENTS
H1('1. Primary documents read')
P('Every historical figure in the study traces to one of these. All were downloaded directly '
  'from the company\'s own website on 9 August 2026.')
rows = [['#', 'Document', 'What was taken from it', 'Address']]
docs = [
    ('P1', 'Annual Report FY2025, including the auditor\'s report, the separate and the '
     'consolidated financial statements with full notes, and the board of directors\' report',
     'The FY2025 and FY2024 consolidated income statement, balance sheet, statement of '
     'changes in equity and cash-flow statement; notes 4 to 36; the revenue-by-channel note '
     '(25); the cost-of-sales note (26); the borrowings note (17) by lender and currency; the '
     'foreign-currency risk note (36) with the average and closing exchange rates; the capital '
     'note (13) with the shareholder table; the associates note (33); the proposed '
     'profit-distribution table; and the board\'s operating statistics — production and sales '
     'by value and by pack, production quantities and available capacity for twenty-one '
     'dosage forms, headcount and the quarterly income summary',
     'eipico.com.eg → Investor Relations → Annual Reports → 2025'),
    ('P2', 'Annual Report FY2024', 'The FY2024 and FY2023 audited consolidated statements '
     'used to cross-confirm the comparative columns of P1, and the FY2024 board operating '
     'statistics', 'eipico.com.eg → Investor Relations → Annual Reports → 2024'),
    ('P3', 'Annual Report FY2023', 'The FY2023 and FY2022 audited consolidated statements and '
     'the FY2023 board report', 'eipico.com.eg → Investor Relations → Annual Reports → 2023'),
    ('P4', 'Annual Report FY2022', 'FY2022 attributable profit, for the traded-multiple '
     'history', 'eipico.com.eg → Investor Relations → Annual Reports → 2022'),
    ('P5', 'Investor presentation', 'Export volume of 60 million packs a year and USD 60 '
     'million of export value; 54 production lines with capacity per shift per year by dosage '
     'form; 414 products across 27 therapeutic groups; products registered across dozens of '
     'countries; the biologicals plant description and product pipeline; the '
     'active-ingredient project description', 'eipico.com.eg → Company Profile → EIPICO Presentation'),
    ('P6', 'Company results release for FY2025', 'Production value of EGP 10.812 billion, '
     'consolidated sales of EGP 9.441 billion, exports of EGP 2.967 billion to 67 countries, '
     'net profit of EGP 1.458 billion — every figure cross-confirmed against the audited '
     'statements in P1', 'eipico.com.eg → News → item 261'),
    ('P7', 'General assembly report, 28 March 2026',
     'The chairman\'s statement of a strategic raw-material stockpile sufficient for at least '
     'eight months — the disclosure that explains the 268-day inventory position',
     'eipico.com.eg → News → item 262'),
    ('P8', 'Company announcement of the biologicals plant licence, 11 December 2025',
     'The Egyptian Drug Authority and Industrial Development Authority licences, and the '
     'launch of the first biosimilar — the disclosure that starts the depreciation clock',
     'eipico.com.eg → News → item 256'),
    ('P9', 'Company announcement of the active-ingredient plant foundation, 15 January 2026',
     'The USD 165 million project in the Suez Canal Economic Zone, and the fact that it is a '
     'separate legal entity', 'eipico.com.eg → News → item 258'),
    ('P10', 'Country default spreads and risk premiums file, last updated 5 January 2026, '
     'read live on 9 August 2026',
     'Egypt row: Moody\'s Caa1; adjusted default spread 6.37%; country risk premium 9.71%; '
     'total equity risk premium 13.94% on the rating basis; corporate tax rate 22.50%; '
     'sovereign credit-default-swap spread 3.41%; equity risk premium on the swap basis 9.41%',
     'pages.stern.nyu.edu → adamodar → datafile → ctryprem'),
    ('P12', 'Reviewed consolidated interim financial statements for the three months ended '
     '31 March 2026, English translation issued by the auditor, review report dated 14 May '
     '2026. THE REVIEW CONCLUSION IS QUALIFIED',
     'The full first-quarter income statement, balance sheet, statement of changes in equity '
     'and cash-flow statement, with the 31 December 2025 comparative column — which ties to '
     'every opening balance in this model, line for line. Supplies the reset FY2026 revenue, '
     'capital-expenditure and finance-cost paths; the confirmation that the construction '
     'balance is transferring and the depreciation charge has doubled; the deconsolidation of '
     'the active-ingredient company; and the three matters on which the auditor qualified',
     'supplied directly for this study'),
    ('P13', 'Audited consolidated financial statements for the year ended 31 December 2024, '
     'English translation issued by the auditor',
     'Used to verify every FY2024 and FY2023 line already taken from the Arabic annual '
     'reports. All tie. Adopted for the presentation of dividend-distribution tax, which this '
     'statement shows on its own line',
     'supplied directly for this study'),
    ('P14', 'Audited consolidated financial statements for the year ended 31 December 2023, '
     'English translation issued by the auditor',
     'Used to verify FY2023 and FY2022. All tie', 'supplied directly for this study'),
    ('P11', 'Daily price history for the listed shares, 2 January 2011 to 6 August 2026',
     'More than three thousand daily open, high, low, close and volume records. Used for the share price, the '
     'beta regression, the technical read and the probability map',
     'supplied for this study'),
]
for r in docs:
    rows.append(list(r))
table(rows, [0.42, 1.55, 3.05, 1.6], size=7.8)
caption('Table B1 — the primary documents. Four consecutive audited financial years were '
        'obtained — FY2022, FY2023, FY2024 and FY2025, each with the auditor\'s report and '
        'full notes — plus the reviewed first quarter of FY2026.')

H2('Primary-source access attempted, and what happened')
rows = [['Source', 'Reachable', 'Outcome']]
for a in SW['primary_access']:
    rows.append([a['url'].replace('https://', '').replace('/', ' / '),
                 'yes' if a['reachable'] else 'NO', a['note']])
table(rows, [2.35, 0.6, 3.65], size=7.6)
caption('Table B2 — every attempt at an official source, logged whether it succeeded or '
        'failed. Three failed and the study says so rather than substituting a weaker source.')

# ------------------------------------------------------- 2. THE INPUT REGISTER
H1('2. Every input, with its source')
P('Every input to the model, with its value, the source it came from, the date of that '
  'source, and the research layer it belongs to. A bare numeral cannot enter this model: the '
  'build asserts that each of these four fields is present and refuses to produce a valuation '
  'if any is missing.')
LAYERS = ['Company', 'Country', 'Market', 'Company/House', 'House']
for layer in LAYERS:
    items = [(k, v) for k, v in INP.items() if v['layer'] == layer]
    if not items:
        continue
    H2(f'Research layer: {layer}   ({len(items)} inputs)')
    rows = [['Input', 'Value', 'Date', 'Source and construction']]
    for k, v in items:
        val = v['value']
        if isinstance(val, dict):
            vs = ', '.join(f'{a} {b:.4f}' for a, b in val.items())
        elif isinstance(val, list):
            vs = ', '.join(f'{x:,.4g}' for x in val)
        elif isinstance(val, bool):
            vs = 'yes' if val else 'no'
        elif isinstance(val, (int, float)):
            vs = f'{val:,.6g}'
        else:
            vs = str(val)
        rows.append([k.replace('_', ' '), vs, v['date'], v['source']])
    table(rows, [1.55, 1.05, 0.66, 3.34], size=7.2)
P(f'Total: {len(INP)} inputs, every one carrying a value, a source, a date and a layer.',
  size=9, italic=True, color=GREY)

# ------------------------------------------------------------- 3. JUDGEMENTS
H1('3. Judgements, and what would overturn each one')
rows = [['Judgement', 'What was decided', 'What would overturn it']]
J = [
    ('The company class and therefore the lens',
     'An operating company — a vertically integrated pharmaceutical manufacturer valued on '
     'free cash flow to the firm, with the equity-accounted associates carried separately in '
     'the bridge. Not a holding company, because the associates are 30% and sub-10% financial '
     'stakes rather than the substance of the business, and not a split-leg valuation, '
     'because there is no captive lender and no separate property leg.',
     'If the associate stake grew to the point where it exceeded the operating business in '
     'value, the company would need a sum-of-the-parts lens instead.'),
    ('The provision charge — THE CONTESTED JUDGEMENT, carried both ways',
     'Frame A treats the credit-loss, inventory and provision charge as a permanent 5.25% of '
     'revenue, the average of the two years either side of the FY2024 spike. Frame B decays '
     'it to 2.5% as the receivable book seasons. Both run to a value per share and both are '
     'published; they are never averaged.',
     'Two more years near 5% of revenue would settle it as Frame A. A charge below 3% in '
     'either FY2026 or FY2027 would settle it as Frame B.'),
    ('No revenue line for the biologicals plant',
     'The plant\'s depreciation and interest are charged because both follow mechanically '
     'from the December 2025 licence. No revenue is credited, because the company has '
     'published none. The required revenue is solved for and published as the crux instead.',
     'Any disclosure of biosimilar volume, price or utilisation.'),
    ('The associate contribution is normalised to EGP 320 million',
     'The disclosed stream is EGP 74.5m, 147.1m and 495.5m across three years and the FY2025 '
     'print is more than three times FY2024. The three-year average is 239.0; 320 sits '
     'between that and the latest year.',
     'A second year near EGP 495 million would make 320 too conservative by roughly EGP 10 a '
     'share.'),
    ('The associates are valued on earnings, not carrying value',
     'They contributed EGP 495.5 million against a carrying value of EGP 675.9 million. '
     'Carrying value is therefore not a usable proxy, and an 11 times multiple is applied to '
     'the normalised stream instead.',
     'Separate accounts for the Saudi associate, which would allow a real valuation rather '
     'than a multiple.'),
    ('The exchange-rate path depreciates about 4% a year, narrowing to 3%',
     'The pound averaged 47.74 in FY2024 and 49.48 in FY2025 while domestic inflation ran far '
     'above the United States\', so the real rate appreciated. The path assumes a partial '
     'reversal.',
     'A step devaluation of the kind seen in March 2024. Note this cuts AGAINST the company, '
     'not for it: imported inputs are 79% of the cash cost stack against a 32% export share.'),
    ('The terminal debt weight is 20%, below today\'s 25%',
     'At a 40% payout the model deleverages through the forecast, so a terminal weight at '
     'today\'s level would contradict the model\'s own trajectory in the direction that '
     'flatters the valuation.',
     'A stated policy of maintaining current leverage.'),
    ('Terminal growth is 5%, which is roughly zero in real terms',
     'It is a pound-nominal rate struck against a terminal risk-free rate that itself embeds '
     'the central bank\'s 5% inflation target. Deliberately conservative for a company with a '
     'third of revenue in hard currency.',
     'Nothing in the near term; the sensitivity table runs 3% to 7% and the value ranges from '
     'EGP 78 to EGP 98.'),
    ('The risk-free rate is normalised by subtracting the sovereign spread',
     'The quoted 22.31% ten-year yield contains Egypt\'s own default risk; subtracting the '
     '3.41% credit-default-swap spread leaves 18.90%, and country risk is then charged once, '
     'inside the equity premium. Both the swap and the rating construction are published and '
     'they agree to 11 basis points.',
     'Nothing — this is a construction rule, and charging the raw yield alongside a '
     'country-loaded premium would double-count. The rate itself is a cached print and is '
     'sensitised.'),
    ('Depreciation is excluded from the escalated unit cost',
     'It enters exactly once, from the property roll-forward. Leaving it in the unit cost as '
     'well would count it twice.',
     'Nothing — this is an arithmetic requirement, and the first cut of the model got it '
     'wrong until the verification caught it.'),
    ('One escalator per physically distinct cost line',
     'Imported ingredients and imported packaging escalate on a hard-currency path through '
     'the exchange rate; labour on wage growth; energy on the regulated tariff schedule; '
     'domestic services on consumer prices.',
     'Nothing — a single blended index across physically distinct lines makes the forecast '
     'margin an artefact of the index rather than of the business.'),
    ('The relative lens uses three multiples, averaged on the sheet',
     'The multiple the model\'s own economics justify (8.1x), the company\'s own four-year '
     'mean (6.7x), and a regional peer median adjusted for the cost-of-equity gap (9.8x). The '
     'unadjusted peer median would give EGP 133 a share; the size of that gap is the '
     'country-risk discount and it is shown rather than hidden.',
     'A peer set facing a comparable cost of equity, which does not currently exist in a '
     'liquid listed form.'),
]
for a, b, c in J:
    rows.append([a, b, c])
table(rows, [1.5, 2.6, 2.5], size=7.6)
caption('Table B3 — twelve judgements, each with the evidence that would overturn it. Stating '
        'the falsifier in advance is what separates a judgement from an assertion.')

# -------------------------------------------------------- 4. NEGATIVE RESULTS
H1('4. Negative results — what was looked for and not found')
rows = [['What was sought', 'Where it was sought', 'Consequence']]
rows += [
    ['[CLOSED] The FY2026 first-quarter interim financial statements',
     'The company\'s own website (annual reports only, no interims published there); the '
     'exchange disclosure portal (every request, scripted and browser-rendered, answered with '
     'a bot-defence challenge page rather than content); the regulator\'s disclosure '
     'sub-domain (refused at the network egress layer)',
     'CLOSED. The filing was supplied directly and is in this edition as primary document P12. '
     'Recorded here because the search history matters: the secondary reporting logged at the '
     'time as an unverified cross-check turned out to be accurate to the pound.'],
    ['Volume, price or utilisation guidance for the biologicals plant',
     'All four annual reports, the investor presentation, and every 2026 press release on the '
     'company\'s own site',
     'The plant is charged but not credited, and the required revenue is solved for and '
     'published as the crux. This is the single largest limitation of the study and it is '
     'deliberate.'],
    ['A counterparty-level or ageing-bucket breakdown of the credit-loss allowance',
     'Notes 10, 20, 31 and 36 of the FY2025 consolidated statements and their FY2024 and '
     'FY2023 equivalents',
     'The charge is disclosed in total and by type but never by counterparty or ageing, so no '
     'bottom-up build is possible. It is carried as a percentage of revenue and, because it '
     'cannot be built up, it is the judgement that is published both ways.'],
    ['Separate accounts for either equity-accounted associate',
     'The investments notes (8/2 and 8/3) of the FY2023, FY2024 and FY2025 filings, and the '
     'company website',
     'Only the carrying value, the ownership percentage and the share of result are '
     'disclosed, so the associate stream is normalised rather than forecast.'],
    ['A live read of the ten-year Egyptian government bond yield',
     'The central bank\'s own fixed-coupon treasury bond auction page',
     'The request was rejected by that site\'s web application firewall. The discount rate '
     'carries a dated house reference print of 21 July 2026 and the rate is sensitised across '
     'a wide range.'],
]
table(rows, [1.5, 2.6, 2.5], size=7.6)
caption('Table B4 — five things that were looked for and not found. A study that reports only '
        'what it found is not reporting its own reliability.')

# ------------------------------------------- 5. SECONDARY-SOURCE DISCREPANCIES
H1('5. Secondary sources, and where they differ from the filings')
P('Nothing in this section is used to build any figure in the study. It is recorded so a '
  'reader who checks the study against a data service and finds a difference knows the '
  'difference was noticed.')
rows = [['Item', 'What the secondary source says', 'What this study does']]
rows += [
    ['FY2026 first-quarter results — NOW VERIFIED',
     'Financial-news reporting of the company\'s exchange filing states consolidated net sales '
     'of about EGP 2.532 billion against EGP 2.299 billion, and attributable net profit of '
     'about EGP 284.0 million against EGP 318.6 million — a fall of roughly 11% on a rise of '
     'roughly 10% in sales',
     f"The filing has since been obtained and both figures are EXACT: net sales "
     f"{INP['q1_rev']['value'] * 1e6:,.0f} against {INP['q1_rev_ly']['value'] * 1e6:,.0f}, "
     f"attributable profit {INP['q1_parent']['value'] * 1e6:,.0f} against "
     f"{INP['q1_parent_ly']['value'] * 1e6:,.0f}, a fall of "
     f"{abs(INP['q1_parent']['value'] / INP['q1_parent_ly']['value'] - 1):.2%}. The study now "
     f"builds on the filing itself, not on the report of it."],
    ['Dividend-distribution tax',
     'The separately issued audited consolidated statements show it on its own line; the '
     'Arabic annual reports fold it into general and administrative expense in FY2023 and into '
     'the associates line in FY2024',
     'This edition adopts the separately issued statements\' presentation for all three '
     'history years. Profit before and after tax is identical either way; the only real effect '
     'is that FY2023 operating profit rises by EGP 4.1 million, 0.34%.'],
    ['FY2023 total assets',
     f"The FY2024 filing prints the FY2023 comparative four pounds below the sum of its own "
     f"subtotals ({INP['assets_fy23']['value'] * 1e6:,.0f})",
     'The subtotal-consistent figure is used. A four-pound difference in the filing itself.'],
    ['FY2024 tablet production volume',
     'The company\'s OWN FY2024 annual report gives one figure for FY2024 tablet production; '
     'the FY2025 report restates the same year about eleven per cent lower',
     'The later filing is used and the restatement is disclosed. It affects a capacity-'
     'utilisation statistic, not a valuation input.'],
    ['Peer valuation multiples',
     'A public-comparables service puts a listed Saudi Arabian generics manufacturer at about '
     '26.7 times trailing earnings and about 25.5 times enterprise value to EBITDA',
     'Used as the third of three legs in the relative lens, explicitly labelled market data, '
     'and adjusted downward for the cost-of-equity gap those peers do not face. Never used '
     'for any EIPICO historical figure.'],
    ['Exports in US dollars',
     'The FY2025 board report gives USD 60 million; the FY2024 report gives USD 54.7 million '
     'for FY2024 while the FY2025 report rounds the same year to USD 55 million',
     'The FY2024 report\'s own 54.7 is used for FY2024 and 60.0 for FY2025, giving 9.7% '
     'hard-currency growth. The difference is rounding and is immaterial.'],
]
table(rows, [1.75, 2.5, 2.35], size=7.6)
caption('Table B5 — where a secondary source says something, and what the study did about it.')

H1('6. How to check this study')
P('The valuation model is a live spreadsheet. Open the Assumptions sheet, change any driver, '
  'and the cost of capital, the discount-rate glide, the discount factors, the cash-flow '
  'waterfall, the terminal block, the three statements, the bridge and every ratio all move. '
  'Three classes of cell are pasted and the READ FIRST sheet names them: audited and '
  'disclosed history, the output of the unit build, and the whole-model re-run grids — the '
  'probability map and the sensitivity tables, which do NOT redraw when a driver changes.')
P('The claim that the workbook calculates was tested on the delivered file rather than '
  'asserted. Every formula cell was independently recalculated and reconciled to the model '
  'that wrote it, and each input was perturbed in place to confirm the answer moves in the '
  'direction the mechanism implies. The evidence is reported in the study\'s quality-control '
  'table.')

OUT = os.path.join(HERE, 'EIPICO_Bibliography_09-08-2026.docx')
doc.save(OUT)
print('wrote', os.path.basename(OUT))
