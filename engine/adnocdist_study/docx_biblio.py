"""ADNOCDIST_Bibliography_09-08-2026.docx — the standalone bibliography document that ships
alongside the ADNOC Distribution valuation study.

Six things, in order: what the document is and how the research layers work; the primary
documents actually read and what was taken from each; the FULL input record (every input with
its value, date and construction, grouped by research layer); the judgements, each with what
would overturn it; the negative results — what was looked for and not found, dated; and the
places where the company's own documents disagree with each other or where a secondary source
reports beyond the filing.

NO financial numeral is typed in this file. Every number is a lookup from study_numbers.json,
extracted_financials.json, sweep_research.json, beta_result.json or step0_result.json.
"""
import json, os, re, sys, glob

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import docx_base as B                                                     # noqa: E402

GREY = B.GREY

D = json.load(open(os.path.join(HERE, 'study_numbers.json')))
INP = D['inputs']
M = D['meta']
W = D['wacc']
CRUX = D['crux']
LEN = D['lenses']
EF = json.load(open(os.path.join(HERE, 'extracted_financials.json')))
RES = EF['restatements']
SR = json.load(open(os.path.join(HERE, 'sweep_research.json')))

# The research file is an internal working record and its prose carries internal
# shorthand. The reader of this document is an external party, so every string drawn
# from it is rewritten once, here, at the point of loading — rather than relying on
# each call site to remember.
_SUBS = [
    ('CROSS-CHECK ONLY, NEVER A BUILD SOURCE', 'used only as a cross-check, never as a source for the model'),
    ('CROSS-CHECK ONLY', 'used only as a cross-check'),
    ('CROSS-CHECK', 'cross-check'),
    ('SIGCM clause 1', 'the source-integrity rule'),
    ('SIGCM', 'the source-integrity rule'),
    ('Recorded because the sweep asked for it', 'Recorded because the research plan called for it'),
    ('the sweep asked for it', 'the research plan called for it'),
    ('the sweep', 'the research'),
    ('Sweep', 'Research'),
    ('sweep register', 'source record'),
    ('AGGREGATOR', 'market-data provider'),
    ('COMPANY_OFFICIAL', "the company's own filings"),
    ('COMPANY_IR', "the company's investor materials"),
    ('SECONDARY', 'independent'),
    ('The protocol requires', 'This study requires'),
    ('the protocol requires', 'this study requires'),
    ('protocol', 'standard'),
    ('NOT resolved by this sweep', 'not resolved by this research'),
    ('this sweep', 'this research'),
    ('FLAG-BEFORE-ISSUE item', 'item flagged before issue'),
    ('FLAG-BEFORE-ISSUE', 'flagged before issue'),
    ('FLAG / STOP-AND-INFORM ITEM', 'flagged before issue'),
    ('STOP-AND-INFORM', 'flagged before issue'),
    ('REGULATED PASS-THROUGH', 'regulated pass-through'),
    ('PASS-THROUGH', 'pass-through'),
    ('ORIGINAL ctryprem.html', 'original published country-premium file'),
    ('ctryprem.html', 'the published country-premium file'),
]


def _scrub(o):
    if isinstance(o, str):
        for a, b in _SUBS:
            o = o.replace(a, b)
        return o
    if isinstance(o, list):
        return [_scrub(x) for x in o]
    if isinstance(o, dict):
        return {k: _scrub(v) for k, v in o.items()}
    return o


SR = _scrub(SR)


def _no_filenames(o):
    """The primary documents are named for the reader by title, never by the file they
    happen to be stored in."""
    if isinstance(o, str):
        return re.sub(r'\s*\(review report in source_[A-Za-z0-9_]+\.pdf\)', '', 
                      re.sub(r'source_[A-Za-z0-9_]+\.pdf', 'the filing itself', o))
    if isinstance(o, list):
        return [_no_filenames(x) for x in o]
    if isinstance(o, dict):
        return {k: _no_filenames(v) for k, v in o.items()}
    return o


SR = _no_filenames(SR)
EF = _no_filenames(EF)
BETA = json.load(open(os.path.join(HERE, 'beta_result.json')))
S0 = json.load(open(os.path.join(HERE, 'step0_result.json')))

_reg_path = os.path.join(HERE, 'sweep_register.json')
REG = json.load(open(_reg_path)) if os.path.exists(_reg_path) else None

IR_SITE = 'adnocdistribution.ae  ->  Investors  ->  Reports and presentations'

# ------------------------------------------------------------------ recording wrappers
TEXT = []
TABLES = []
_TN = [0]


def tnum():
    _TN[0] += 1
    return f'Table {_TN[0]}'


def rec(s):
    TEXT.append(str(s))


def P(t='', **k):
    rec(t); return B.P(t, **k)


def H1(t):
    rec(t); return B.H1(t)


def H2(t):
    rec(t); return B.H2(t)


def caption(t):
    rec(t); return B.caption(t)


def box(lines, **k):
    for h, b in lines:
        rec(str(h) + ' ' + str(b))
    return B.box(lines, **k)


def T(rows, widths, label='', **k):
    for r in rows:
        for c in r:
            rec(c)
    TABLES.append((label or f'table {len(TABLES) + 1}', rows, widths))
    return B.table(rows, widths, **k)


# ------------------------------------------------------------------ formatting helpers
def pct(x, dp=2):
    return f'{x * 100:.{dp}f}%'


def money(x):
    return f'{x:,.0f}' if float(x).is_integer() else f'{x:,.3f}'


def unit4(x):
    return f'{x:,.4f}'


def num3(x):
    return f'{x:,.3f}'


RATE_KEYS = {
    'payout', 'tax_statutory', 'tax_effective', 'tax_dmtt', 'rf_observed', 'erp_mature',
    'erp_total', 'crp', 'sov_spread', 'credit_margin', 'credit_margin_usd', 'cb_base_rate',
    'roic_terminal', 'wd_terminal', 'g_terminal',
    'vol_retail_g', 'vol_comm_g', 'gp_retfuel_per_l_g', 'gp_comm_per_l_g', 'rev_nonfuel_g',
    'gm_nonfuel', 'cash_opex_g', 'other_income_g',
}
COEFF_KEYS = {'beta', 'beta_terminal'}
PER_UNIT_KEYS = {'spot', 'dps', 'eps_fy23', 'eps_fy24', 'eps_fy25', 'price_retfuel', 'price_comm'}


def fmt_value(key, v):
    """Format by magnitude and by what the input is: a rate as a percentage, a per-share or
    per-litre figure to four decimals, a money figure or a count with thousands separators,
    a list as a comma-separated series in the same convention."""
    if isinstance(v, list):
        return ', '.join(fmt_value(key, x) for x in v)
    if key in RATE_KEYS:
        return pct(v, 2 if abs(v) >= 0.01 else 3)
    if key in COEFF_KEYS:
        return num3(v)
    if key in PER_UNIT_KEYS:
        return unit4(v)
    return money(v)


def nice_date(iso):
    y, m, d = iso.split('-')
    mon = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov',
           'Dec'][int(m) - 1]
    return f'{int(d)} {mon} {y}'


def long_date(iso):
    y, m, d = iso.split('-')
    mon = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
           'September', 'October', 'November', 'December'][int(m) - 1]
    return f'{int(d)} {mon} {y}'


def url_path(u):
    """Render a link as a readable navigation path. Long trailing slugs are cut: an
    unbreakable 100-character token would starve whatever column it lands in, and the
    host plus the first couple of path steps is what actually tells a reader where to
    look."""
    u = re.sub(r'^https?://', '', u).rstrip('/')
    u = u.replace('www.', '')
    parts = [x for x in u.split('/') if x]
    trimmed = []
    for i, seg in enumerate(parts[:3]):
        if len(seg) > 26:
            seg = seg[:24].rstrip('-') + '\u2026'
        trimmed.append(seg)
    if len(parts) > 3:
        trimmed.append('\u2026')
    return '  ->  '.join(trimmed)


def first_sentences(s, n=2, cap=340):
    parts = re.split(r'(?<=[.;]) +', s)
    out = ' '.join(parts[:n]).strip()
    if len(out) > cap:
        out = out[:cap].rsplit(' ', 1)[0] + ' ...'
    return out


USED_AS = {
    'B': 'resets the starting point',
    'S': 'sets or tests a forward driver',
    'D': 'supplies a build-level driver',
    'C': 'context and cross-check only',
}

# ==================================================================== 0. FRONT
B.masthead()
P(M['company'], size=19, bold=True, space_after=1)
P(f"Bibliography and the complete record of inputs — the companion volume to the valuation "
  f"study of {long_date(M['study_date'])}", size=11, color=GREY, space_after=10)

box([
    ('READ FIRST. ',
     'This is not an appendix. It is a separate volume whose only purpose is to let a reader '
     'check the study without taking anything in it on trust. It lists every official document '
     'that was read and what was taken from each; then every single input to the valuation, '
     'with its value, its date and the sentence that says where it came from and how it was '
     'built; then every judgement, each paired with the evidence that would overturn it; then '
     'everything that was searched for and not found; and finally every place where the '
     'documents disagree with each other or where an outside source says something different '
     'from the filing.'),
    ('The five research layers. ',
     'Each input is filed under the layer of the world it comes from. COMPANY is the company\'s '
     'own issued documents — the audited and reviewed financial statements, the management '
     'reports, the results presentations and the integrated report; every historical figure in '
     'the model comes from this layer and from nowhere else. MARKET is what the exchange itself '
     'observes — the share price, and the beta measured from that price history. COUNTRY is the '
     'United Arab Emirates: policy rates, the government bond yield, the tax regime, inflation '
     'and the country risk premium. INDUSTRY is fuel retailing as a business — regulated margin '
     'mechanics, network economics, the electric-vehicle transition and listed peers. GLOBAL is '
     'what is priced outside any one country: crude oil, and the internationally traded product '
     'prices that flow through to the pump.'),
    ('What is not here. ',
     'No data service, no broker and no press report is a source of any figure the company '
     'reports about itself. Where one was consulted at all it was to cross-check, and every '
     'such case is named in the final section. A reader who finds a difference between this '
     'study and a screen should assume the screen and the filing are measuring different '
     'periods, and the last section shows exactly where that happens.'),
])

# ==================================================================== 1. DOCUMENTS
H1('1. The primary documents read')
P(f"Every historical figure in the valuation traces to one of the documents below. All of them "
  f"were obtained from the company's own investor-relations site — {IR_SITE} — and read in "
  f"full. The annual financial statements were audited by "
  f"{EF['meta']['auditors']['FY2023_FY2024_FY2025']}; the half-year statements for "
  f"{nice_date(INP['rev_h126']['date'])} were reviewed by "
  f"{EF['meta']['auditors']['H1_2026_interim_review']}. Amounts are presented in "
  f"{EF['meta']['presentation_currency']} and, in the statements themselves, in thousands: "
  f"“{EF['meta']['unit']}”.")

DOCS = {
    'source_FY2023_audited_consolidated.pdf': (
        'Audited consolidated financial statements for the year ended 31 December 2023, with '
        'the independent auditor\'s report and the full notes',
        'The company, for the year ended 31 December 2023',
        'The FY2023 income statement, balance sheet, statement of changes in equity and '
        'cash-flow statement, and the notes behind them: revenue and direct costs, the '
        'distribution and administrative expenses note with its depreciation and amortisation '
        'split, the borrowings note, the lease and right-of-use notes, the trade receivables '
        'and payables notes and the capital-risk table. Supplies the FY2022 comparative revenue '
        'and net profit, and the two separately presented FY2023 impairment lines.'),
    'source_FY2024_audited_consolidated.pdf': (
        'Audited consolidated financial statements for the year ended 31 December 2024, with '
        'the independent auditor\'s report and the full notes',
        'The company, for the year ended 31 December 2024',
        'The complete FY2024 statements and notes on the same basis; the restated opening '
        'equity at 1 January 2024 and the accounting-change note behind it; the '
        're-presentation of the FY2023 impairment comparative as a single line; and the '
        'FY2023 comparative column used to confirm every prior-year figure line for line.'),
    'source_FY2025_audited_consolidated.pdf': (
        'Audited consolidated financial statements for the year ended 31 December 2025, with '
        'the independent auditor\'s report and the full notes',
        'The company, for the year ended 31 December 2025',
        'The complete FY2025 statements and notes: revenue by segment and by category, direct '
        'costs, the expense note and its depreciation split, the income-tax note and its rate '
        'reconciliation, the borrowings note with the per-currency interest basis, leases, '
        'working-capital balances, provisions, the dividend note and the capital-risk table. '
        'This is the anchor filing for the whole model.'),
    'source_Q1_2026_reviewed_interim.pdf': (
        'Reviewed interim condensed consolidated financial statements for the three months '
        'ended 31 March 2026',
        'The company, for the quarter ended 31 March 2026',
        'The first-quarter revenue, profit and balance-sheet position, and the confirmation '
        'that the 31 December 2025 audited closing balances carry forward unchanged into 2026.'),
    'source_Q2_2026_reviewed_interim.pdf': (
        'Reviewed interim condensed consolidated financial statements for the six months ended '
        '30 June 2026',
        'The company, for the half-year ended 30 June 2026',
        'The whole first half of 2026 — revenue, direct costs, gross profit, expenses, '
        'depreciation, finance costs, tax and net profit, with the balance sheet and cash-flow '
        'statement — which is the base the forecast is struck from. Also the events-after-the-'
        'reporting-date note describing the proposed South African acquisition, and the '
        'associate dividend disclosure.'),
    'source_Q2_2025_reviewed.pdf': (
        'Reviewed interim condensed consolidated financial statements for the six months ended '
        '30 June 2025',
        'The company, for the half-year ended 30 June 2025',
        'The prior-year half-year comparatives — revenue, volumes by segment, gross profit by '
        'segment and inventory movements — without which the first half of 2026 could not be '
        'read as a growth rate rather than a level.'),
    'source_FY2025_mda.pdf': (
        'Management discussion and analysis for the year ended 31 December 2025',
        'The company, published with the FY2025 results',
        'The operating figures no financial statement carries: fuel volumes by segment, the '
        'station count, convenience-store and electric-vehicle-point counts, transaction '
        'counts, gross profit split between retail fuel, non-fuel and commercial, the '
        'inventory-movement disclosure for FY2025 and FY2024, and the underlying EBITDA '
        'summary table.'),
    'source_Q2_2026_mda.pdf': (
        'Management discussion and analysis for the second quarter and first half of 2026',
        'The company, published with the H1-2026 results',
        'The same operating set for the first half of 2026 and its 2025 comparative, including '
        'the inventory movement for the half and its split between fuel retail and commercial; '
        'the reaffirmed 2026 capital-expenditure, network and dividend targets; the '
        'medium-term network and non-fuel targets; and the description of the proposed South '
        'African acquisition and its stated accretion.'),
    'source_FY2025_presentation.pdf': (
        'Results presentation for the year ended 31 December 2025',
        'The company, published with the FY2025 results',
        'The segment bridges and per-litre margin build behind the FY2025 management report, '
        'used to confirm the gross-profit-per-litre construction.'),
    'source_Q1_2026_presentation.pdf': (
        'Results presentation for the first quarter of 2026',
        'The company, published with the Q1-2026 results',
        'The 2026 targets as first stated — network additions, electric-vehicle points, '
        'capital expenditure and the dividend floor — and the first-quarter operating detail.'),
    'source_Q2_2026_presentation.pdf': (
        'Results presentation for the second quarter and first half of 2026',
        'The company, published with the H1-2026 results',
        'The reaffirmed 2026 targets, the per-segment operating detail for the half, and the '
        'transaction description and stated accretion for the proposed South African '
        'acquisition.'),
    'source_2025_integrated_report.pdf': (
        'Integrated annual report 2025',
        'The company, for the year ended 31 December 2025',
        'Strategy, network and transition detail: the medium-term network target, the '
        'electric-vehicle build-out, the convenience-store conversion series, the efficiency '
        'programme, and the environmental and workforce series. Also the second published '
        'version of underlying EBITDA, which differs from the management report and is '
        'reported in the final section.'),
}

present = sorted(os.path.basename(p) for p in glob.glob(os.path.join(HERE, 'source_*.pdf')))
missing = [f for f in present if f not in DOCS]
assert not missing, f'undescribed primary documents: {missing}'

order = [
    'source_FY2023_audited_consolidated.pdf', 'source_FY2024_audited_consolidated.pdf',
    'source_FY2025_audited_consolidated.pdf', 'source_Q1_2026_reviewed_interim.pdf',
    'source_Q2_2026_reviewed_interim.pdf', 'source_Q2_2025_reviewed.pdf',
    'source_FY2025_mda.pdf', 'source_Q2_2026_mda.pdf', 'source_FY2025_presentation.pdf',
    'source_Q1_2026_presentation.pdf', 'source_Q2_2026_presentation.pdf',
    'source_2025_integrated_report.pdf',
]
order = [f for f in order if f in present]
assert len(order) == len(present)

rows = [['Ref', 'Document', 'Publisher and period', 'What was taken from it']]
for i, f in enumerate(order, start=1):
    d = DOCS[f]
    rows.append([f'D{i}', d[0], d[1], d[2]])
T(rows, [0.38, 1.62, 1.15, 3.85], size=7.8, label='primary documents')
caption(f'{tnum()} — the official documents read, all of them obtained from the company\'s own '
        f'investor-relations site. Three consecutive audited financial years were obtained, '
        f'each with the auditor\'s report and the full notes, together with three reviewed '
        f'interim filings, two management reports, three results presentations and the '
        f'integrated annual report.')

if REG and REG.get('primary_access'):
    H2('Attempts at an official source, and what happened')
    rows = [['Source attempted', 'Reached', 'Outcome']]
    for a in REG['primary_access']:
        rows.append([url_path(a['url']), 'yes' if a.get('reachable') else 'NO',
                     a.get('note', '')])
    T(rows, [2.45, 0.55, 4.0], size=7.6, label='access attempts')
    caption(f'{tnum()} — every attempt at an official source, logged whether it succeeded or '
            f'failed. A failure is reported here rather than quietly replaced by a weaker '
            f'source.')

H2('Other sources consulted, none of them a source of the company\'s own reported figures')
P(f"The company's own documents cannot supply a crude price, a government bond yield, a tax "
  f"rate or a peer multiple. Those come from outside, and every outside source consulted is "
  f"listed below with the date it was read and what it was used for. The share-price history "
  f"itself is a separate input: {S0['clean_rows']:,} daily records for the listing, spanning "
  f"{S0['span_years']:.1f} years to the close of {long_date(M['price_date'])}, screened for "
  f"the exchange's own daily price limit so that any move larger than one session can "
  f"physically produce is treated as a corporate action or a data error rather than a return. "
  f"That series carries the share price, the beta regression, the technical read and the "
  f"probability map.")

rows = [['Ref', 'Subject', 'Source, and when it was read', 'How it was used']]
for e in SR['entries']:
    rows.append([
        e['id'], e['topic'],
        f"{e['source_name']}\n{url_path(e['source_url'])}\nread "
        f"{nice_date(e['access_date'])}"
        + (f"; as at {nice_date(e['as_of_date'])}" if e.get('as_of_date') else ''),
        f"{USED_AS[e['classification']].capitalize()}. {first_sentences(e['consequence'])}"])
T(rows, [0.42, 1.5, 2.13, 2.95], size=7.2, label='outside sources')
caption(f'{tnum()} — the {len(SR["entries"])} sources consulted outside the company\'s own '
        f'documents, grouped by the layer they belong to: '
        f'{SR["meta"]["entry_count_by_ring"]["GLOBAL"]} global, '
        f'{SR["meta"]["entry_count_by_ring"]["COUNTRY"]} country, '
        f'{SR["meta"]["entry_count_by_ring"]["INDUSTRY"]} industry and '
        f'{SR["meta"]["entry_count_by_ring"]["COMPANY"]} about the company itself — the last of '
        f'which are context and cross-check only and are never a source of a reported figure.')

# ==================================================================== 2. INPUT RECORD
H1('2. The full input record')
P(f"Every input the valuation uses, with its value, the date that value belongs to, and the "
  f"sentence that says where it came from and how it was built. There are {len(INP)} of them "
  f"and all {len(INP)} are printed here. A bare numeral cannot enter the model: the build "
  f"refuses to produce a valuation unless each input carries all four fields — a value, a "
  f"source, a date and a layer.")
P('Conventions in the value column: money figures are in dirhams, in millions, with thousands '
  'separators, unless the input name says otherwise; rates and growth figures are shown as '
  'percentages; per-share and per-litre figures are shown to four decimals; volumes are in '
  'millions of litres and station, store and transaction figures are counts. Where an input is '
  'a path rather than a single figure, the five forecast years are shown in order as a '
  'comma-separated series.', size=9.6, color=GREY)

LAYER_NOTE = {
    'Market': 'What the exchange itself observes — the share price and what is measured from '
              'its history.',
    'Company': 'The company\'s own issued documents. Every historical figure in the model sits '
               'in this layer.',
    'Country': 'The United Arab Emirates — policy rates, the government bond curve, the tax '
               'regime, inflation and country risk.',
    'Industry': 'Fuel retailing as a business — regulated margin mechanics, network economics '
                'and the transition away from liquid fuel.',
    'Global': 'What is priced outside any one country — crude oil and the internationally '
              'traded product prices that reach the pump.',
}
LAYER_ORDER = ['Market', 'Company', 'Country', 'Industry', 'Global']
seen = 0
counts = {}
for layer in LAYER_ORDER:
    items = sorted(((k, v) for k, v in INP.items() if v['layer'] == layer), key=lambda x: x[0])
    counts[layer] = len(items)
    if not items:
        continue
    H2(f'{layer} layer — {len(items)} inputs')
    P(LAYER_NOTE[layer], size=9.4, italic=True, color=GREY, space_after=4)
    rows = [['Input', 'Value', 'Date', 'Source, and how the figure was built']]
    for k, v in items:
        rows.append([k.replace('_', ' '), fmt_value(k, v['value']), nice_date(v['date']),
                     v['source']])
        seen += 1
    T(rows, [1.15, 1.0, 0.65, 4.2], size=7.2, align_right_from=99,
      label=f'input record — {layer}')
    caption(f'{tnum()} — every {layer.lower()}-layer input, in alphabetical order.')

assert seen == len(INP), f'input record published {seen} of {len(INP)}'
P(f'Total: {seen} inputs published — {", ".join(f"{c} {l.lower()}" for l, c in counts.items())} '
  f'— every one of them carrying a value, a source, a date and a layer.',
  size=9.4, italic=True, color=GREY)

# ==================================================================== 3. JUDGEMENTS
H1('3. The judgements, and what would overturn each one')
P('A judgement is a decision that the documents do not make for you. Each one below is stated '
  'with the evidence that would show it to be wrong. Stating the falsifier in advance is what '
  'separates a judgement from an assertion.')

_inv = INP['invmove_A']['value']
J = [
    ('Inventory movements are a timing effect and net to zero — THE CONTESTED JUDGEMENT, '
     'carried both ways',
     f"The company earned inventory gains of AED {money(INP['invgain_fy24']['value'])} million "
     f"in FY2024, AED {money(INP['invgain_fy25']['value'])} million in FY2025 and AED "
     f"{money(INP['invgain_h126']['value'])} million in the first half of 2026 alone. The "
     f"normalised frame carries the realised first half of 2026 and nothing after it, on the "
     f"view that a timing difference between the cost of stock bought and the price at which "
     f"it is sold nets to zero across a full crude cycle. The through-cycle frame instead "
     f"carries the FY2024-FY2025 average of AED {money(CRUX['avg_24_25'])} million every year. "
     f"Both frames run all the way to a value per share — AED "
     f"{num3(CRUX['normalised_value'])} against AED {num3(CRUX['throughcycle_value'])} — and "
     f"both are published. They are never averaged.",
     'Several consecutive years of positive movements through a full crude price cycle, '
     'including a year in which the crude price falls. One falling-price year that still '
     'produced a gain would settle it; a falling-price year that produced a loss of similar '
     'size would settle it the other way.'),
    ('Terminal growth is set below domestic inflation',
     f"Growth beyond the forecast horizon is {fmt_value('g_terminal', INP['g_terminal']['value'])}, "
     f"below the domestic inflation rate, because the volume base — litres of liquid fuel sold "
     f"through a station network — faces substitution by electric vehicles that the non-fuel "
     f"business, a fifth of gross profit, cannot offset. {INP['g_terminal']['source']}.",
     'The share of electric vehicles in new car sales in the United Arab Emirates staying in '
     'the low single digits through 2030, or fuel volumes per station rising rather than '
     'holding flat. Either would say the drag being priced is not there.'),
    ('The beta is measured against the local exchange, with the company taken out of the index',
     f"A beta of {fmt_value('beta', INP['beta']['value'])}, from "
     f"{BETA['primary_ex_subject']['n']} weekly observations against an equal-weight composite "
     f"of the exchange's own listed names, with the company itself removed from that composite "
     f"so it is not being regressed partly against itself. The regression has an R-squared of "
     f"{BETA['primary_ex_subject']['r2']:.3f} and a standard error of "
     f"{BETA['primary_ex_subject']['se']:.3f}. Left in the index the coefficient would be "
     f"{BETA['primary']['beta']:.3f}; the more conservative construction is the one carried.",
     'The regression losing significance — a standard error that stops being comfortably '
     'smaller than the coefficient — or the share\'s own volatility converging on the exchange '
     'median, which would pull the coefficient toward one.'),
    ('The base case excludes the proposed South African acquisition',
     f"{EF['proposed_acquisition_shell_downstream_south_africa']['status']} The target is "
     f"{EF['proposed_acquisition_shell_downstream_south_africa']['target']}, at "
     f"{EF['proposed_acquisition_shell_downstream_south_africa']['implied_enterprise_value']}. "
     f"It is described in the study and priced at zero in the base case, because a signed "
     f"agreement that has not closed is not yet an earnings stream.",
     f"Completion, which the company expects in "
     f"{EF['proposed_acquisition_shell_downstream_south_africa']['expected_completion'].split(',')[0]}. "
     f"The company's own stated accretion is "
     f"{EF['proposed_acquisition_shell_downstream_south_africa']['stated_accretion_MDA']['eps_accretion']} "
     f"to earnings per share in the first full year after completion."),
    ('The minimum top-up tax is not applied in the base case',
     f"The forecast is taxed at the effective rate the audited accounts actually produced — "
     f"{fmt_value('tax_effective', INP['tax_effective']['value'])} in FY2025, above the "
     f"{fmt_value('tax_statutory', INP['tax_statutory']['value'])} federal rate because the "
     f"Egyptian subsidiary is taxed higher. The "
     f"{fmt_value('tax_dmtt', INP['tax_dmtt']['value'])} minimum top-up tax exists in law for "
     f"groups of this size, but the FY2025 audited tax reconciliation does not apply it: that "
     f"note reconciles at the federal rate. The base case follows the filing and the top-up "
     f"case is priced separately.",
     'A future filing showing a top-up charge, or a tax reconciliation that starts from the '
     'higher rate. That is a disclosure, not an inference, and it would arrive in an audited '
     'note.'),
    ('The realised fuel price is escalated on its own crude-linked path, not on a domestic '
     'inflation index',
     f"The realised retail price per litre follows AED "
     f"{fmt_value('price_retfuel', INP['price_retfuel']['value'])} across the forecast years. "
     f"{INP['price_retfuel']['source']}.",
     'A crude path materially different from the one used — the study\'s own price sensitivity '
     'shows what that does. A domestic price cap that broke the link between the pump price and '
     'the crude price would overturn the construction itself rather than the level.'),
    ('The commercial margin per litre holds its 2026 step-up',
     f"Commercial gross profit per litre is escalated by "
     f"{fmt_value('gp_comm_per_l_g', INP['gp_comm_per_l_g']['value'][0])} in FY2026 and by the "
     f"domestic inflation rate thereafter. {INP['gp_comm_per_l_g']['source']}.",
     'A second half of 2026, or a 2027, in which commercial gross profit per litre falls back '
     'toward its 2025 level. That would say the step was a one-period contract effect rather '
     'than a repricing that holds.'),
    ('The regulated retail margin is a domestic line and takes a domestic escalator',
     f"Retail fuel gross profit per litre escalates at "
     f"{fmt_value('gp_retfuel_per_l_g', INP['gp_retfuel_per_l_g']['value'][0])} a year. "
     f"{INP['gp_retfuel_per_l_g']['source']}.",
     'The margin formula itself changing, or a period in which the realised retail margin per '
     'litre moves with crude rather than independently of it.'),
    ('The risk-free rate is normalised by taking out the sovereign\'s own default spread',
     f"The observed local-currency government yield is "
     f"{fmt_value('rf_observed', INP['rf_observed']['value'])}; the sovereign's own adjusted "
     f"default spread of {fmt_value('sov_spread', INP['sov_spread']['value'])} is subtracted, "
     f"leaving {pct(W['rf_star'])}. Country risk is then charged exactly once, inside the "
     f"equity risk premium of {pct(W['erp'])}. Charging the raw yield alongside a "
     f"country-loaded premium would count the same risk twice.",
     'Nothing — this is a construction rule rather than a view. What is open to challenge is '
     'the level of the yield itself, and that is shown across a range in the study\'s '
     'sensitivity.'),
    ('The cost of debt is built from the sovereign yield plus the company\'s own disclosed '
     'credit margin',
     f"The pre-tax marginal cost of debt is {pct(W['kd_pretax'])} — the local-currency "
     f"sovereign yield plus the dirham margin of "
     f"{fmt_value('credit_margin', INP['credit_margin']['value'])} the company discloses on "
     f"its own term loan. It therefore sits above the sovereign, as a same-currency corporate "
     f"borrower must. The dollar tranche carries a margin of "
     f"{fmt_value('credit_margin_usd', INP['credit_margin_usd']['value'])} and is shown "
     f"separately at {pct(W['kd_pretax_usd_basis'])}.",
     'A new borrowing at a materially different spread. The company\'s next refinancing is the '
     'observation that would settle it.'),
    ('The cost of capital is glided rather than held flat',
     f"The discount rate moves from {pct(W['wacc'])} today to {pct(W['wacc_terminal'])} at the "
     f"end of the forecast, as the beta drifts from "
     f"{fmt_value('beta', INP['beta']['value'])} to "
     f"{fmt_value('beta_terminal', INP['beta_terminal']['value'])} and the debt weight from "
     f"{pct(W['wd'])} to {fmt_value('wd_terminal', INP['wd_terminal']['value'])}. "
     f"{INP['beta_terminal']['source']}.",
     'A stated policy of holding leverage where it is, or evidence that the transition risk in '
     'the business is not rising — either would argue for the flat construction instead.'),
    ('The terminal return on capital fades from what the company earns today',
     f"Terminal return on invested capital is set at "
     f"{fmt_value('roic_terminal', INP['roic_terminal']['value'])}. "
     f"{INP['roic_terminal']['source']}.",
     'The network continuing to earn its current return on capital while still growing — which '
     'would mean the reinvestment rate implied by the terminal block is too high and the '
     'terminal value too low.'),
    ('Impairment and other operating charges are normalised rather than carried at their '
     'realised level',
     f"FY2026 carries the realised first half annualised, at AED "
     f"{money(INP['impair_norm']['value'][0])} million, falling to AED "
     f"{money(INP['impair_norm']['value'][1])} million and then escalating with inflation. "
     f"{INP['impair_norm']['source']}.",
     'A third consecutive year at the elevated level, which would make it a run rate rather '
     'than a provisioning cycle.'),
    ('Cash operating costs take a domestic escalator, net of the company\'s own efficiency '
     'programme',
     f"Cash operating costs grow at "
     f"{fmt_value('cash_opex_g', INP['cash_opex_g']['value'][0])} a year. "
     f"{INP['cash_opex_g']['source']}.",
     'The efficiency programme being abandoned or missed, or a network expansion that adds '
     'cost faster than the stated rate.'),
    ('The dividend is carried at close to the whole of earnings',
     f"The payout used in the equity roll-forward is "
     f"{fmt_value('payout', INP['payout']['value'])}. {INP['payout']['source']}.",
     'A change to the stated policy, or a year in which the fixed dirham dividend is cut. '
     'Because the policy sets a fixed amount per share with a floor of a stated share of '
     'profit, rising profits reduce the payout ratio mechanically without any decision at all.'),
]
rows = [['The judgement', 'What was decided, and on what evidence', 'What would overturn it']]
for a, b, c in J:
    rows.append([a, b, c])
T(rows, [1.45, 3.05, 2.5], size=7.6, label='judgements')
caption(f'{tnum()} — the {len(J)} judgements the valuation rests on, each with the evidence '
        f'that would overturn it. The first of them is the study\'s most consequential '
        f'contested judgement and is carried both ways all the way to a value per share, '
        f'never averaged into one number.')

# ==================================================================== 4. NEGATIVE RESULTS
H1('4. What was looked for and not found')
P(f"A study that reports only what it found is not reporting its own reliability. Everything "
  f"below was searched for on or before {long_date(SR['meta']['access_date'])} and not "
  f"obtained, together with what the valuation does instead.")

NEG = [
    ('The central bank\'s own published interbank rate',
     'The Central Bank of the United Arab Emirates interbank rate page',
     f"The page refused automated access on {long_date(SR['meta']['access_date'])}. The "
     f"study's own network route was checked at the same moment and was healthy, so this was "
     f"the site's own protection against automated readers rather than a connection failure. "
     f"The marginal cost of debt was built instead from the local-currency sovereign yield of "
     f"{fmt_value('rf_observed', INP['rf_observed']['value'])} plus the company's own "
     f"disclosed credit margin of "
     f"{fmt_value('credit_margin', INP['credit_margin']['value'])}, both of which are primary "
     f"figures. The central bank's base rate of "
     f"{fmt_value('cb_base_rate', INP['cb_base_rate']['value'])} was obtained from the bank's "
     f"own rate announcement and is shown as a floating-rate cross-check."),
    ('An inventory-movement figure for FY2023 or FY2022',
     'All three audited filings, both management reports, all three results presentations and '
     'the integrated report',
     f"{EF['inventory_movements']['coverage_gap']} The through-cycle frame therefore averages "
     f"over FY2024, FY2025 and the first half of 2026 only, and the study says so where the "
     f"average is used. It is also the reason this judgement is published both ways rather "
     f"than settled."),
    ('The outstanding dirham-versus-dollar split of the term loan',
     'The borrowings note in each of the three audited filings and both interim filings',
     f"{EF['meta']['not_found'][2]} The debt is therefore split for the cost-of-capital build "
     f"using the disclosed per-currency margins and the original drawdown proportions, and "
     f"both the dirham-basis and dollar-basis costs of debt are published side by side rather "
     f"than blended into one."),
    ('A ten-year dirham-denominated federal government bond',
     'The Ministry of Finance auction results for the federal Treasury bond programme',
     f"No such tenor has been issued. The longest sourced local-currency point is the January "
     f"2031 tranche at {fmt_value('rf_observed', INP['rf_observed']['value'])}, about four and "
     f"a half years. That observed yield is used rather than a constructed ten-year point, and "
     f"the alternative — extrapolating the curve off the sovereign's dollar issuance — is "
     f"shown as a sensitivity rather than presented as an observation."),
    ('A credit-default-swap-based row for the United Arab Emirates in the country-risk file',
     'The country default spreads and risk premiums file, in the original published version',
     f"The file carries no swap-based row for this sovereign, so only the rating-based "
     f"construction can be published: an adjusted default spread of "
     f"{fmt_value('sov_spread', INP['sov_spread']['value'])} and a total equity risk premium "
     f"of {fmt_value('erp_total', INP['erp_total']['value'])}, being the mature-market premium "
     f"of {fmt_value('erp_mature', INP['erp_mature']['value'])} plus a country risk premium of "
     f"{fmt_value('crp', INP['crp']['value'])}. Where two bases exist a study of this house "
     f"publishes both; here only one exists and that is stated rather than hidden."),
    ('A more recent version of the same country-risk file',
     'The original publication of the country default spreads and risk premiums file',
     'A mid-2026 update exists, but its row for this country could not be verified in the '
     'original published file, and a third-party restatement of that row contradicts the '
     'original and was therefore not used. The January 2026 vintage is used and its vintage is '
     'disclosed wherever the premium appears.'),
    ('Quantitative guidance for 2026 earnings or volumes',
     'Both management reports and all three results presentations',
     f"{EF['guidance_and_targets']['FY2026_targets_reaffirmed']['ebitda_guidance']} "
     f"{EF['guidance_and_targets']['FY2026_targets_reaffirmed']['volume_guidance']} The "
     f"company does give network, capital-expenditure and dividend targets, and those are used; "
     f"the volume and margin paths are built from the disclosed first half rather than from "
     f"any company forecast."),
    ('FY2023 operating statistics — volumes, station counts, store and charging-point counts',
     'All three audited filings, the FY2025 management report and the integrated report',
     f"{EF['meta']['not_found'][0]} The unit build therefore starts from FY2024, which is the "
     f"first year for which volumes and network counts are disclosed alongside the accounts, "
     f"and FY2023 is carried at the statement level only."),
    ('An EBITDA figure for FY2023 or FY2022',
     'The audited filings and the obtained management reports',
     f"{EF['meta']['not_found'][1]} The earnings history in this study is therefore presented "
     f"on audited operating profit, which exists for every year, with EBITDA shown only where "
     f"the company itself published it."),
    ('The stated maturity date of the term loan',
     'The borrowings note in the FY2025 audited filing',
     f"{EF['meta']['not_found'][3]} The refinancing date and term are used to place the "
     f"maturity, and the study does not present a precise repayment schedule it cannot source."),
    ('The management report for the first quarter of 2026',
     'The company\'s investor-relations site',
     f"{EF['meta']['not_found'][5]} The reviewed interim statements and the first-quarter "
     f"results presentation were both obtained, so the quarter is covered; the commentary "
     f"volume for that quarter is not."),
    ('A complete monthly retail fuel price series for 2025',
     'The monthly announcements of the national fuel price committee, and compilations of them',
     'Only part of the year was located directly, together with the published annual range. '
     'The realised price per litre used in the model is not taken from these announcements at '
     'all — it is computed from the company\'s own disclosed revenue and volumes — so the '
     'series serves only as a cross-check on the direction of travel.'),
    ('Current competitor station counts, and a current figure for the electric-vehicle share '
     'of new car sales',
     'Competitor disclosure, national statistics and industry sources',
     'The most recent competitor network figures found are more than a year old and the '
     'available electric-vehicle share is older still. Neither is load-bearing: the market-share '
     'context is presented with its vintage stated, and the transition drag is expressed as a '
     'taper in the company\'s own volume growth rather than derived from a national adoption '
     'figure.'),
    ('The published national energy outlook tables behind the crude forecast',
     'The statistical agency\'s own outlook document',
     'The document could not be read in the form published. The crude path is therefore built '
     'from reporting of that same outlook, and the study says so; the price path is also shown '
     'across a range wide enough to contain the disagreement.'),
    ('A current national economic review for 2026',
     'The published country consultation reports',
     'Only the 2025 vintage was located, which predates the 2026 oil shock entirely. Its '
     'growth forecasts are cited with the vintage attached and are used for context, never as '
     'a driver of the forecast.'),
    ('Traded multiples for two named unlisted competitors',
     'Public market data for the two businesses',
     'Neither has publicly traded equity — one is an unlisted joint venture and the other is '
     'privately controlled — so neither can carry a multiple. The peer table is built from the '
     'listed operators that do, and the omission is recorded rather than filled with an '
     'estimate.'),
]
rows = [['What was sought', 'Where it was sought', 'What was done instead']]
for a, b, c in NEG:
    rows.append([a, b, c])
T(rows, [1.72, 1.62, 3.66], size=7.6, label='negative results')
caption(f'{tnum()} — {len(NEG)} searches that came back empty, each dated and each with the '
        f'consequence for the valuation stated. Three of them change what the study can claim; '
        f'the rest are disclosed limitations.')

# ==================================================================== 5. DISCREPANCIES
H1('5. Where the documents disagree, and what was done about it')
P('Three kinds of thing are recorded here: places where the company restated or re-presented '
  'its own prior-year figures, places where two of the company\'s own documents print '
  'different numbers for the same thing, and places where an outside data service reports '
  'something different from the filing. In every case both readings are recorded and the one '
  'used is named.')

H2('5.1 Restatements and internal differences in the company\'s own documents')
rows = [['Item', 'What the documents show', 'What this study does']]
for r in RES:
    right = ' '.join(x for x in [r.get('effect', ''), r.get('which_taken', '')] if x).strip()
    rows.append([r['item'], r['description'], right])
T(rows, [1.5, 3.1, 2.4], size=7.4, label='restatements')
caption(f'{tnum()} — every restatement, re-presentation and internal inconsistency found '
        f'across the twelve documents. The first is the only one that changes a balance: '
        f'because the prior year was not restated, closing equity for FY2023 does not equal '
        f'the adjusted opening equity for FY2024, and the equity roll-forward in this study '
        f'carries that break rather than smoothing it away.')

H2('5.2 Outside data services, and where they differ from the filings')
P('Nothing in this table is used to build any figure in the study. It is recorded so that a '
  'reader who checks the study against a screen and finds a difference knows the difference '
  'was noticed, and knows what it is.')

_co01 = next(e for e in SR['entries'] if e['id'] == 'CO-01')
_co08 = next(e for e in SR['entries'] if e['id'] == 'CO-08')
_c13 = next(e for e in SR['entries'] if e['id'] == 'C-13')
_c16 = next(e for e in SR['entries'] if e['id'] == 'C-16')
_co11 = next(e for e in SR['entries'] if e['id'] == 'CO-11')
_i15 = next(e for e in SR['entries'] if e['id'] == 'I-15')

rows = [['Item', 'What the outside source says', 'What this study does']]
rows += [
    ['Headline financials on a market-data service',
     _co01['finding'],
     f"Only the share price, the share count and the market value were taken from it. The "
     f"revenue, earnings and cash-flow figures there are trailing-twelve-month and unaudited, "
     f"and they do not agree with the audited year because they are not measuring the same "
     f"period: the audited FY2025 revenue is AED {money(INP['rev_fy25']['value'])} million and "
     f"net profit AED {money(INP['np_fy25']['value'])} million, while the trailing figures "
     f"include the first half of 2026, in which the realised price per litre rose sharply with "
     f"crude. The trailing multiple quoted there likewise differs from this study's own, which "
     f"is computed as the share price over audited FY2025 earnings per share of AED "
     f"{unit4(INP['eps_fy25']['value'])}, giving {LEN['pe_now']:.1f} times."],
    ['The guaranteed minimum margin under the supply agreement',
     first_sentences(_co08['finding'], 3, 520),
     'This is the single most consequential structural feature of the business and it was '
     'found first in commentary rather than in the agreement disclosure itself. It is not used '
     'as an input. The margin actually earned is computed from the company\'s own disclosed '
     'gross profit and volumes, so the model rests on the realised outcome rather than on the '
     'reported floor beneath it; the floor is described in the study as protection, not as a '
     'number in the build.'],
    ['A later version of the country-risk premium file',
     first_sentences(_c13['finding'], 3, 520),
     f"The originally published file, of the vintage stated in the input record, is the one "
     f"used: a total equity risk premium of "
     f"{fmt_value('erp_total', INP['erp_total']['value'])}. The later third-party restatement "
     f"contradicts the original and could not be verified in the publisher's own file, so it "
     f"is not used; the difference is small enough to sit inside the study's own sensitivity "
     f"on the discount rate."],
    ['The company\'s own tax position, as reported in the press',
     first_sentences(_c16['finding'], 2, 460),
     f"Not used. The tax rate in the model is computed from the audited filings themselves — "
     f"the income tax charge over profit before tax, an effective "
     f"{fmt_value('tax_effective', INP['tax_effective']['value'])} in FY2025 — and the "
     f"reconciliation in that same note is what establishes which regime the company is "
     f"actually paying under."],
    ['Peer trading multiples',
     'Multiples for seven listed fuel retailers and convenience operators, taken from a public '
     'comparables service.',
     'Used only in the relative lens, and only as a cross-check on the multiple the company\'s '
     'own economics justify. Every peer figure is labelled as market data. No peer figure is '
     'used anywhere in the construction of this company\'s own reported history.'],
    ['Two competitors with no traded equity',
     first_sentences(_i15['finding'], 2, 400),
     'Recorded as a negative result and excluded from the peer table rather than estimated. '
     'The peer set is built only from operators with a real traded price.'],
    ['Sell-side estimates and consensus',
     first_sentences(_co11['finding'], 2, 420),
     'Read, and never used. No consensus figure enters any lens, any driver or any historical '
     'line. It is recorded here only so that a reader can see it was looked at.'],
]
T(rows, [1.5, 3.05, 2.45], size=7.4, label='outside-source differences')
caption(f'{tnum()} — where an outside source says something, and what the study did about it. '
        f'In every case the answer is the same in substance: the company\'s own issued '
        f'documents are the only source of anything the company reports about itself.')

P('To state it once more, plainly, because it is the rule the whole study rests on: every '
  'historical figure in the model — every line of the income statement, the balance sheet and '
  'the cash-flow statement, every volume, every station count and every per-litre margin — '
  'comes from the company\'s own issued and audited or reviewed documents. Market data, peer '
  'multiples and press reporting appear only as cross-checks, are labelled as such wherever '
  'they appear, and were never a build source.', bold=False)

# ==================================================================== CHECKS
BANNED = [
    r'\bsweep\b', r'\bregisters?\b', r'\bprotocols?\b', r'\bpanels?\b', r'\bgates?\b',
    r'\bmodel study\b', r'\bCRPS\b', r'\bPIT\b', r'\bwalk-?forward\b', r'\bPARITY\b',
    r'\bverdicts?\b', r'\bSIGCM\b', r'\bSTOP-AND-INFORM\b', r'\bStep \d', r'\bstep 0',
    r'\bring\b', r'\bmc_v3\b', r'\bdata_quality\b', r'\bresearch_sweep\b', r'\badaptive_width\b',
    r'\bwacc_builder\b', r'\bapply_technicals\b', r'\bta_chart\b', r'\bdocx_base\b',
    r'\bstudy_numbers\b', r'\bcompute\.py\b', r'source_[A-Za-z0-9_]+\.pdf',
]
# These are internal taxonomy tokens, which are UPPERCASE wherever they occur in code.
# Matched case-sensitively so that ordinary English ('a pass-through cost', 'secondary
# reporting') is not flagged: the defect is the token leaking through, not the word.
BANNED_TOKENS = [r'\bPASS\b', r'\bFAIL\b', r'\bAGGREGATOR\b', r'\bCROSS-CHECK ONLY\b',
                 r'\bSECONDARY\b', r'\bPARITY\b', r'\bBOUNDARY\b', r'\bCOMPANY_IR\b',
                 r'\bCOMPANY_OFFICIAL\b']
hits = []
for t in TEXT:
    for pat in BANNED:
        for m in re.finditer(pat, t, re.I):
            hits.append((pat, t[max(0, m.start() - 60):m.start() + 60].replace('\n', ' ')))
    for pat in BANNED_TOKENS:
        for m in re.finditer(pat, t):          # case-SENSITIVE
            hits.append((pat, t[max(0, m.start() - 60):m.start() + 60].replace('\n', ' ')))

CPI = 15.5          # characters per inch at the table font sizes used here
width_fails = []
for label, rows_, widths in TABLES:
    if round(sum(widths), 6) > 7.0:
        width_fails.append((label, 'total width', sum(widths)))
    for j, w in enumerate(widths):
        cells = [str(r[j]) for r in rows_]
        longest = max((max((len(x) for x in c.split()), default=0) for c in cells), default=0)
        if longest > w * CPI:
            width_fails.append((label, f'col {j} unbreakable word {longest}ch', w * CPI))
        body = [str(r[j]) for r in rows_[1:]] or ['']
        fill = (sum(len(c) for c in body) / len(body)) / (w * CPI)
        if w > 1.2 and fill < 0.30:
            width_fails.append((label, f'col {j} only {fill:.0%} filled', w))

print(f'tables: {len(TABLES)}  numbered captions: {_TN[0]}')
for label, rows_, widths in TABLES:
    print(f'  {label:34s} rows={len(rows_):4d} widths={widths} sum={sum(widths):.2f}')
print('inputs published by layer:', counts, '=> total', seen, 'of', len(INP))
if hits:
    print('VOCABULARY HITS:')
    for p_, ctx in hits:
        print('   ', p_, '::', ctx)
if width_fails:
    print('WIDTH FAILURES:')
    for f_ in width_fails:
        print('   ', f_)
assert not hits, 'external-reader vocabulary found'
assert not width_fails, 'table geometry check failed'

OUT = os.path.join(HERE, 'ADNOCDIST_Bibliography_09-08-2026.docx')
B.doc.save(OUT)
print('wrote', os.path.basename(OUT))
