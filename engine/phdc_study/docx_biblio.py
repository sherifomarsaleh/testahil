"""PHDC_Bibliography_19-08-2026.docx — the standalone bibliography: primary documents,
the full four-field input register, judgements with what would overturn them, negative
results, and aggregator discrepancies. Every value is read from study_numbers.json."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
os.chdir(HERE)
exec(open(os.path.join(HERE, '..', 'du_study', 'docx_base.py')).read())

D = json.load(open('study_numbers.json'))
SW = json.load(open('sweep_register.json'))
INP, M, H, W, L, SYN = D['inputs'], D['meta'], D['hist'], D['wacc'], D['lenses'], D['synthesis']

_T = [0]
def T():
    _T[0] += 1
    return 'Table %d' % _T[0]

def lalign(t, cols):
    for row in t.rows:
        for j in cols:
            for p in row.cells[j].paragraphs:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    return t

def fmt(v):
    if isinstance(v, bool):
        return 'yes' if v else 'no'
    if isinstance(v, (int,)):
        return format(v, ',')
    if isinstance(v, float):
        if abs(v) >= 1000:
            return format(round(v, 3), ',')
        if abs(v) < 1 and v != 0:
            return '%.6g' % v
        return '%.4g' % v
    if isinstance(v, list):
        return ', '.join(fmt(x) for x in v[:8]) + ('' if len(v) <= 8 else ' …')
    if isinstance(v, dict):
        return '; '.join('%s %s' % (k, fmt(x)) for k, x in list(v.items())[:6])
    return str(v)

masthead()
P('Palm Hills Developments (EGX:PHDC)', size=19, bold=True, space_after=2)
P('Bibliography, input register and research record — fundamental refresh, 19 August 2026',
  size=11.5, color=BRASS, space_after=10)
P('This document accompanies the valuation study of the same date. It exists so that every '
  'number in that study can be traced to a document, a date and a layer of research, and so that '
  'a reader can see which judgements are load-bearing and what would overturn each of them.',
  size=10)

# ============================================================ PRIMARY DOCUMENTS
H1('1  Primary documents')
rows = [['Document', 'Issuer and date', 'What it supplies']]
rows += [
    ['Interim consolidated financial statements as of 30 June 2026',
     'Palm Hills Developments Company S.A.E; limited review report by Forvis Mazars Mostafa '
     'Shawki (Khaled Said El Rabat, Financial Regulatory Authority registration 258); board '
     'authorisation and review report both dated 17 August 2026',
     'The whole of the historical base: the income statement for the half and its comparative, '
     'the balance sheet at 30 June 2026 and 31 December 2025, the cash-flow statement, the '
     'statement of changes in equity, and notes 34, 41-72 and 76'],
    ['Audited consolidated financial statements for the year ended 31 December 2024, with 2023 '
     'comparatives',
     'Palm Hills Developments Company S.A.E; retrieved from the company investor-relations asset '
     'library',
     'Two audited fiscal years from the filing itself: revenue, cost of revenues, gross profit, '
     'administrative cost, finance costs, profit before and after tax, depreciation, capital '
     'expenditure, operating cash flow and the movement in the Residents\' Association balance'],
    ['1Q2026 earnings release', 'Palm Hills Developments, 20 May 2026',
     'New sales, backlog, the company\'s own net-debt figure, construction spending, units due '
     'for handover, land bank, and the company\'s own revenue, EBITDA and profit history for '
     '2022 to 2025'],
    ['9M2025 earnings release', 'Palm Hills Developments, 13 November 2025',
     'Nine-month revenue, gross profit, EBITDA, new sales, construction spending, backlog and net '
     'debt — which, with the full-year totals, pins the fourth quarter of 2025'],
    ['1H2025 earnings release', 'Palm Hills Developments, 13 August 2025',
     'The comparable half-year operating anchors: construction spending, cash collection, backlog'],
    ['Treasury bond and bill auction results',
     'Central Bank of Egypt; bond auction 17 August 2026, bill auctions 13 and 16 August 2026',
     'The observed risk-free rate and the shape of the local curve'],
    ['Country default spreads and risk premiums, ctrypremJuly26',
     'A. Damodaran, Stern School of Business; credit-default-swap spreads as at 30 June 2026',
     'The Egypt row: rating, adjusted default spread, country risk premium, total equity risk '
     'premium on both bases, corporate tax rate'],
    ['Daily price series for the shares and for the exchange index',
     'The house price library for Palm Hills and for the thirty-share Egyptian Exchange index, '
     'both as of 22 July 2026',
     'The beta regression'],
]
lalign(table(rows, [1.75, 2.2, 3.05], first_col_bold=True, size=8.0), {1, 2})
caption('%s. Every document that supplies a number to the study. Nothing describing what Palm '
        'Hills reported comes from anywhere else.' % T())

P('Documents sought and NOT obtained. Two, and both matter. The results release for the first '
  'half of 2026 is not published on the company\'s investor-relations site, on the content '
  'interface behind it, or on the wire service that carried earlier Palm Hills releases; all '
  'three were checked on 19 August 2026 and the newest financial result on any of them is the '
  'first-quarter release of 20 May. The 2025 annual audited statements are not published either, '
  'and neither is a 2025 results release. The consequence of the first is that the company\'s own '
  'backlog figure, its own net-debt definition, first-half contracted sales and first-half '
  'construction spending are carried as unverified press reporting and no model driver reads '
  'them. The consequence of the second is that 2025 gross profit, cost of revenues and finance '
  'costs are shown blank in the study\'s three-year history rather than estimated.', size=9.6)

# ============================================================= INPUT REGISTER
H1('2  Input register — every input, four fields')
P('Every input carries a value, a source, a date and the layer of research it belongs to. The '
  'model refuses to emit a number if any of the %d entries is missing any of the four.'
  % len(INP), size=9.8)
LAYERS = ['Company', 'Country', 'Industry', 'Market', 'Prior study']
for layer in LAYERS:
    items = sorted([(k, v) for k, v in INP.items() if v['ring'] == layer])
    if not items:
        continue
    H2('2.%d  %s layer — %d inputs' % (LAYERS.index(layer) + 1, layer, len(items)))
    rows = [['Input', 'Value', 'Date', 'Source and construction']]
    for k, v in items:
        rows.append([k, fmt(v['value']), v['date'], v['source']])
    lalign(table(rows, [1.25, 0.95, 0.72, 4.08], first_col_bold=True, size=6.4), {3})
    caption('%s. The %s layer in full.' % (T(), layer.lower()))

# ================================================================= JUDGEMENTS
H1('3  Judgements, and what would overturn each')
rows = [['Judgement', 'What the study does', 'What would overturn it']]
rows += [
    ["The Residents' Association float is permanent operating funding",
     'Adopted as the base framing. The balance has risen in every disclosed period, no '
     'association has been constituted, and the invested proceeds earn for the company. The other '
     'framing is computed in full and published beside it, never averaged into it.',
     'Any association taking legal personality and its assets with it under Building Law 119. '
     'That single event moves the study from EGP %s to EGP %s a share.'
     % (p2v := ('%.2f' % SYN['framing_A']['base']), '%.2f' % SYN['framing_B']['base'])],
    ['The cost of capital normalises with the disinflation path',
     'The discount rate glides from %.2f%% today to %.2f%% by the end of the explicit horizon, on '
     'a terminal risk-free rate built from the central bank\'s own 5 per cent target for the '
     'fourth quarter of 2028. The spot-anchored constant rate is carried as the other end of '
     'every range.' % (W['wacc_cds'] * 100, W['wacc_term'] * 100),
     'An inflation path that stops falling. July\'s urban print of %.1f%% was the first '
     'acceleration in four months. Holding the spot rate throughout takes the cash-flow lens from '
     'EGP %.2f to EGP %.2f.' % (INP['cpi_urban']['value'] * 100, L['dcf']['A'], L['dcf']['A_spot'])],
    ['The price-to-build-cost ratio holds at its measured level',
     'Held at the measured %.3fx and escalated only by the difference between the selling-price '
     'path and the build-cost path. Not extrapolated downward from the year-on-year fall.'
     % H['P_h126'],
     'A first-half 2027 ratio below %.2fx. The two most recent quarters argue against further '
     'compression — the margin recovered from %.1f%% to %.1f%% — but they are two quarters.'
     % (D['sens']['crux_P'][0], H['ebitda_margin_q425'] * 100, H['ebitda_margin_q226'] * 100)],
    ['Real construction volume grows and then decelerates',
     'Work carried out annualises %+.1f%% above 2025; the path carries %.0f%% real growth in 2027 '
     'falling to %.0f%% by 2031.'
     % ((INP['work_h126']['value'] * 2 / INP['work_fy25']['value'] - 1) * 100,
        INP['vol_growth']['value'][0] * 100, INP['vol_growth']['value'][-1] * 100),
     'A land bank or a launch programme that will not carry the volume. The exposure is real but '
     'one-sided: at no real growth at all the cash-flow lens falls from EGP %.2f to EGP %.2f, and '
     'at half again the base path it rises to EGP %.2f. It runs that way because %.0f%% of the '
     'capital funding the work is customer money — net of it the return on capital is %.1f%%, '
     'against %.1f%% on the gross base.'
     % (D['sens']['vol_vps'][2], D['sens']['vol_vps'][0], D['sens']['vol_vps'][3],
        (1 - D['gdv']['ic_end_ex_float'] / D['gdv']['ic_end']) * 100,
        D['gdv']['roic_ex_float'] * 100, D['gdv']['roic_A'] * 100)],
    ['The construction cost stack splits 25/20/25/30 across steel, cement, finishing and labour',
     'Estimated. No filing discloses a cost-by-nature split of construction. Each class still '
     'carries its own escalator; only the weights are judgement.',
     'A cost-by-nature disclosure. Two hundred basis points of error in the blended escalator is '
     'worth EGP %.2f a share.'
     % abs(max(D['sens']['cost_vps']) - min(D['sens']['cost_vps']))],
    ['Land cost and the partners\' share of revenue cannot be separated',
     'Demonstrated rather than asserted: the disclosed data give one equation in two unknowns, '
     'and the study publishes the bound it can put on the margin move instead of inventing a '
     'split.',
     'Any disclosure splitting the cost of real estate development. Until then the block moves '
     'with revenue at its measured %.2f%% rather than with cost inflation.' % (H['c2'] * 100)],
    ['Net debt is EGP %s mn' % format(round(H['netdebt_company']), ','),
     "The company's own definition — interest-bearing obligations from note 34 less cash and "
     'treasury bills. The broader definition carrying notes payable and land liabilities gives '
     'EGP %s mn, and the restricted definition used in framing B gives EGP %s mn. All three are '
     'published.' % (format(round(H['netdebt_broad']), ','),
                     format(round(H['netdebt_restricted']), ',')),
     'Nothing factual — this is a definitional choice, which is why all three are shown rather '
     'than one being presented as the answer.'],
]
lalign(table(rows, [1.55, 2.6, 2.85], first_col_bold=True, size=7.6), {1, 2})
caption('%s. The seven judgements this study rests on, each with its falsifier stated in advance.'
        % T())

# ============================================================ NEGATIVE RESULTS
H1('4  Negative results')
P('A search that returns nothing is evidence, and it is only evidence if it is dated and '
  'recorded. Five were logged in this refresh.', size=9.8)
rows = [['Layer and topic', 'What was searched', 'Date']]
import re as _re
for f in SW.get('findings', []):
    if f.get('klass') != 'NEGATIVE_SEARCH':
        continue
    _h = f.get('headline', '')
    _m = _re.search(r'\((.*)\)\s*$', _h, _re.S)
    rows.append([('%s — %s' % (f.get('ring', '').title(), f.get('category', ''))),
                 _m.group(1) if _m else _h, f.get('source_date', '')])
if len(rows) == 1:
    rows.append(['—', 'see the research record in the study', ''])
lalign(table(rows, [1.7, 4.5, 0.8], first_col_bold=True, size=7.6), {1})
caption('%s. Dated negative searches. The top-down treatment of the land-and-partners block is '
        'justified by the fourth of these and by nothing else.' % T())

P('Two further negatives are recorded as failed attempts to reach a primary document rather than '
  'as failed searches: the first-half 2026 results release and the 2025 annual statements, both '
  'described in section 1.', size=9.6)

# ==================================================== AGGREGATOR DISCREPANCIES
H1('5  Aggregator and source discrepancies')
rows = [['Item', 'The two figures', 'How the study resolves it']]
rows += [
    ['2025 attributable profit',
     'The company\'s own history chart in the first-quarter release shows EGP %s mn; the audited '
     'statement of changes in equity inside the 30 June filing shows EGP %s mn'
     % (format(round(INP['np_fy25_ir']['value']), ','), format(round(INP['np_fy25']['value']), ',')),
     'The statement governs. The chart figure is recorded here and used nowhere.'],
    ['2025 revenue and EBITDA',
     'Available only from the company\'s own history charts, at EGP %s mn and EGP %s mn'
     % (format(round(INP['rev_fy25_ir']['value']), ','),
        format(round(INP['ebitda_fy25_ir']['value']), ',')),
     'Used, because they are company-issued and no statement is available, and flagged as chart '
     'figures wherever they appear.'],
    ['Backlog',
     'Note 72 gives EGP %.1fbn of contractual value for undelivered-unit contracts concluded '
     'since the start of 2023; the company\'s own wider definition stood at EGP %.0fbn at the '
     'first quarter and press reporting attributes EGP %.0fbn to the first half'
     % (INP['bk_contract']['value'] / 1000, INP['backlog_1q26']['value'] / 1000,
        INP['backlog_h126_press']['value'] / 1000),
     'The study anchors on note 72 because it is the only one that appears in a reviewed '
     'statement, and states the other two beside it.'],
    ['North Coast and Alexandria first-quarter sales',
     'The company\'s own release states EGP 5.4bn in its prose and EGP 5.9bn in the chart on the '
     'same page',
     'Neither is used as a driver. Recorded because a reader comparing the two would otherwise '
     'assume a transcription error here.'],
    ['Emaar Misr first-quarter 2026 figures',
     'One aggregator reports net income of EGP 7.77bn on revenue of EGP 6.76bn',
     'Not used. Net income above revenue is not possible for an operating quarter; the peer set '
     'carries only the price-to-earnings and enterprise-value multiples, not the underlying '
     'aggregator financials.'],
    ['Peer multiples generally',
     'Sourced from market-data aggregators, quotes dated 11 August 2026 for the Egyptian names '
     'and June to August 2026 for the Gulf names',
     'Used to price OTHER companies only. No aggregator figure enters any Palm Hills historical, '
     'any driver or any statement line.'],
]
lalign(table(rows, [1.4, 2.7, 2.9], first_col_bold=True, size=7.6), {1, 2})
caption('%s. Where two sources disagree, both are stated and the study says which it follows.' % T())

# ================================================================ THE ARITHMETIC
H1('6  Assertions the model runs before it will emit a number')
P('The model raises rather than warning. If any of the following fails, no numbers file is '
  'written and no document can be built. %d assertions ran clean on this build.'
  % len(D['assert_log']), size=9.8)
rows = [['#', 'Assertion']]
for i, a in enumerate(D['assert_log'], 1):
    rows.append([str(i), a.replace('OK  ', '')])
lalign(table(rows, [0.4, 6.6], size=7.0), {1})
caption('%s. The full assertion log for this build.' % T())

OUT = 'PHDC_Bibliography_19-08-2026.docx'
doc.save(OUT)
print('wrote %s — %d tables, %d register entries, %d assertions'
      % (OUT, _T[0], len(INP), len(D['assert_log'])))
