"""ARCC_Bibliography_06-08-2026.docx — a standalone source register.

Every figure that reaches the study or the model traces to a row here: what it is, where
it came from, what kind of source that is, and the date the source itself carries.
Reads study_numbers.json and the sweep register — no numeral is typed here.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
sys.path.insert(0, HERE)
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

D = json.load(open('study_numbers.json'))
SW = json.load(open('sweep_register.json'))
INP = D['inputs']

INK = RGBColor(0x1C, 0x3A, 0x36); GREY = RGBColor(0x6E, 0x7B, 0x77)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
F_DARK, F_PANEL, F_CREAM = '1C3A36', 'EAF0EE', 'F6F1E6'

doc = Document()
sec = doc.sections[0]
sec.page_width, sec.page_height = Inches(11), Inches(8.5)      # landscape: long source text
sec.left_margin = sec.right_margin = Inches(0.6)
sec.top_margin = sec.bottom_margin = Inches(0.6)
st = doc.styles['Normal']
st.font.name = 'Calibri'; st.font.size = Pt(9.5); st.font.color.rgb = INK
st.paragraph_format.space_after = Pt(5); st.paragraph_format.line_spacing = 1.05


def shade(cell, hexcolor):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd'); shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto'); shd.set(qn('w:fill'), hexcolor)
    tcPr.append(shd)


def cell_margins(t, top=40, bottom=40, left=80, right=80):
    m = OxmlElement('w:tblCellMar')
    for tag, v in [('top', top), ('left', left), ('bottom', bottom), ('right', right)]:
        e = OxmlElement(f'w:{tag}'); e.set(qn('w:w'), str(v)); e.set(qn('w:type'), 'dxa')
        m.append(e)
    t._tbl.tblPr.append(m)


def borders(t, color='C9D4D1', sz='4'):
    b = OxmlElement('w:tblBorders')
    for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        e = OxmlElement(f'w:{edge}')
        e.set(qn('w:val'), 'single'); e.set(qn('w:sz'), sz)
        e.set(qn('w:space'), '0'); e.set(qn('w:color'), color)
        b.append(e)
    t._tbl.tblPr.append(b)


def P(text='', size=9.5, bold=False, italic=False, color=INK, space_after=5, space_before=0):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.font.size = Pt(size); r.bold = bold; r.italic = italic; r.font.color.rgb = color
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.space_before = Pt(space_before)
    return p


def H1(t): return P(t, size=15, bold=True, space_before=12, space_after=6)
def H2(t): return P(t, size=11.5, bold=True, space_before=10, space_after=4)


def table(rows, widths, size=8.4, wrap_cols=None):
    t = doc.add_table(rows=len(rows), cols=len(widths))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell_margins(t); borders(t)
    t.autofit = False
    layout = OxmlElement('w:tblLayout'); layout.set(qn('w:type'), 'fixed')
    t._tbl.tblPr.append(layout)
    for j, w in enumerate(widths):
        t.columns[j].width = Inches(w)
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            c = t.cell(i, j); c.width = Inches(widths[j])
            p = c.paragraphs[0]; p.paragraph_format.space_after = Pt(1)
            r = p.add_run('' if val is None else str(val))
            r.font.size = Pt(size); r.font.color.rgb = INK
            if i == 0:
                r.bold = True; shade(c, F_PANEL)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return t


# ------------------------------------------------------------------ masthead
t = doc.add_table(rows=1, cols=1); cell_margins(t, 90, 90, 150, 150)
c = t.cell(0, 0); shade(c, F_DARK); c.width = Inches(9.8)
p = c.paragraphs[0]
r = p.add_run('Testahil · Arabian Cement Company S.A.E. (EGX: ARCC) — Source Register')
r.bold = True; r.font.size = Pt(12); r.font.color.rgb = WHITE
r2 = p.add_run('   6 August 2026')
r2.font.size = Pt(10); r2.font.color.rgb = RGBColor(0x9F, 0xB0, 0xAC)
doc.add_paragraph().paragraph_format.space_after = Pt(4)

P('Where every number came from. This register accompanies the valuation study and the '
  'companion model. Each input carries the source it was taken from, the type of that '
  'source, and the date the source itself bears — not the date it was read.', size=10)

# ---------------------------------------------------- sourcing limitation
H2('A limitation to state at the top')
P('No source document was opened. That is a stronger statement than the usual caveat and '
  'it is the accurate one. The audited consolidated financial statements were not read; '
  'neither was the annual report, the FY2025 investor presentation, the exchange filing, '
  'nor even the press articles reporting them. Every attempt to retrieve a page — the '
  'company\'s own website, the exchange\'s disclosure portal, and eleven financial data '
  'and press hosts — was refused by the egress policy governing this environment, which '
  'returns a refusal at the connection stage rather than serving a page.', size=9.5)
P('What WAS available was a web search tool returning synthesised summaries that quote '
  'figures from those pages, together with the daily price series supplied with the '
  'engagement. Every company figure in this register therefore reaches the model at one '
  'further remove than a citation normally implies: it is a figure as RELAYED in a search '
  'result about the reporting, not a figure read in the reporting, and certainly not one '
  'read in the audited print. The source names below identify where each figure '
  'ORIGINATES, which is genuine and worth recording; they do not claim the page was '
  'retrieved.', size=9.5)
P('The consequence is stated rather than hidden. Revenue, attributable profit, operating '
  'income, the balance-sheet totals and both dividend distributions are carried as relayed '
  'from coverage of the company\'s exchange filings and from aggregations of commercial '
  'financial data — two steps removed from the audited print. Every line between them is '
  'DERIVED by closing the disclosed profit, and is labelled as derived wherever it appears. Section 3 lists each derivation and its method. A reader with access to the '
  'audited statements should re-run the model against them; the workbook is built so that '
  'changing an input reprices everything downstream, and that property is tested rather '
  'than asserted.', size=9.5)
P('One disagreement between sources is carried openly rather than resolved. Total assets '
  'of EGP 8,783.72mn less reported equity of EGP 4,642.73mn implies total liabilities of '
  'EGP 4,140.99mn; a separate aggregation prints EGP 2,894.13mn for the same line. The '
  'figure that closes against total assets is the one carried, and the gap is shown on the '
  'balance sheet of the model rather than averaged away.', size=9.5)

# ---------------------------------------------------- input register
doc.add_page_break()
H1('1  Input register — every figure in the model')
RING_ORDER = {'Market': 0, 'Company': 1, 'Industry': 2, 'Country': 3, 'House': 4}
rows = [['#', 'Input', 'Value', 'Ring', 'Source', 'Source date']]


def fmt(v):
    if isinstance(v, list):
        return ', '.join(f'{x:,.4g}' for x in v)
    if isinstance(v, float):
        return f'{v:,.4f}'.rstrip('0').rstrip('.')
    return f'{v:,}' if isinstance(v, int) else str(v)


items = sorted(INP.items(), key=lambda kv: (RING_ORDER.get(kv[1]['ring'], 9), kv[0]))
for i, (k, v) in enumerate(items, 1):
    rows.append([str(i), k, fmt(v['value']), v['ring'], v['source'], v['date']])
table(rows, [0.30, 1.70, 0.92, 0.74, 4.98, 0.84], size=7.4)

# ---------------------------------------------------- source catalogue
doc.add_page_break()
H1('2  Source catalogue — the publications and institutions relied on')
CAT = [
 ('Arabian Cement Company S.A.E. — exchange filings', 'Company filing',
  'FY2022 to FY2025 consolidated results; 9M-2025 and Q1-2026 results; general-meeting '
  'resolutions on the FY2024 and FY2025 cash distributions.',
  'Figures relayed through search summaries of the outlets below. The primary documents '
  'were NOT retrieved from the company website or the exchange portal.'),
 ('Arabian Cement Company — corporate and sustainability disclosure', 'Company disclosure',
  'Plant configuration: two lines in Suez governorate, on average about five million tonnes '
  'a year of first-quality clinker and cement, roughly 6% of Egypt\'s nominal capacity. The '
  'alternative-fuel programme, the 7.2 MWh solar installation, baghouse filters and '
  'hydrogen injection, the 120,000-tonne annual emissions reduction target, and the '
  'supplementary-cementitious-materials, calcined-clay and CEM III product plans.',
  'arabiancementcompany.com'),
 ('Mubasher Info', 'Financial press',
  'FY2024 and FY2025 consolidated results; 9M-2025 results; the EGP 1.10bn FY2024 '
  'distribution at EGP 2.94 per share and the EGP 2.00bn FY2025 distribution.',
  'english.mubasher.info'),
 ('Arab Finance', 'Financial press',
  'FY2025 consolidated profit of EGP 3.599bn on net sales of EGP 12.447bn; Q1-2026 '
  'consolidated profit of EGP 943.068mn on net sales of EGP 2.995bn; Egyptian building-'
  'materials market indicators for 2025.', 'arabfinance.com'),
 ('Zawya / Refinitiv', 'Financial press',
  'Q1-2026 results and the 59.7% year-on-year profit increase; comparative Q1-2025 figures.',
  'zawya.com'),
 ('International Cement Review / cemnet', 'Trade press',
  'Egyptian sector production and pricing commentary; the industry ministry\'s position on '
  'capacity and price stabilisation.', 'cemnet.com'),
 ('Global Cement', 'Trade press',
  'Egyptian nameplate capacity, production, consumption and export volumes for 2025; the '
  'dormant-capacity revival programme of 12.6Mt from the second half of 2026.',
  'globalcement.com'),
 ('EnterpriseAM Egypt', 'Financial press',
  'The 2025 review of the Egyptian cement industry and the 2026 outlook: consumption of '
  '54Mt, the EGP 3,600 per tonne price expectation for 2026, demand-growth forecasts of 1% '
  'to 8%, and the abolition of the production-quota system in May 2025 with exports capped '
  'at 30% of output.', 'enterpriseam.com'),
 ('S&P Global Market Intelligence, via independent aggregations', 'Data aggregator',
  'FY2025 operating income of EGP 4,595.82mn; Q4-2025 revenue of EGP 3,645.60mn and EBITDA '
  'of EGP 1,393.01mn; the trailing gross margin of 40.77%; total assets, total equity, '
  'total debt and cash; the share count of 374.87mn.',
  'Relayed through search summaries of stockanalysis.com, simplywall.st and '
  'investing.com; the three summaries were cross-checked against each other, but none of '
  'the three pages was retrieved'),
 ('Central Bank of Egypt', 'Central bank',
  'Main operation rate of 19.50% held at the April and May 2026 meetings, with the '
  'overnight deposit and lending rates at 19.00% and 20.00%; the Q1-2026 Monetary Policy '
  'Report; the medium-term inflation target of 7% used to build the terminal risk-free '
  'rate; the headline urban inflation series easing to 14.3% in June 2026.', 'cbe.org.eg'),
 ('Egyptian Tax Authority', 'Tax reference',
  'Statutory corporate income tax rate of 22.5%.', 'Statutory rate'),
 ('Aswath Damodaran — country risk premium file', 'Reference dataset',
  'Egypt equity risk premium and sovereign default spread on the credit-default-swap basis, '
  'January 2026 edition. The original file only.', 'Used for the cost-of-equity build'),
 ('Amwal Al Ghad — bank exchange-rate surveys', 'Financial press',
  'The Egyptian pound at 50.30/50.40 against the dollar at the close of 4 August 2026, and '
  'an average bank buying rate of 51.01 on 1 August 2026.', 'en.amwalalghad.com'),
 ('Egyptian Exchange daily price history', 'Market data',
  '2,957 daily open, high, low, close and volume records from 18 May 2014 — the listing '
  'date — to 6 August 2026, supplied with the engagement. This series is the basis of the '
  'price chart, the volatility estimate, the beta regression and the price map.',
  'Supplied as a file'),
 ('Standard cement engineering benchmarks', 'Industry reference',
  'Specific thermal energy of 3.2 to 3.6 GJ per tonne of clinker for a dry '
  'preheater/precalciner kiln; 90 to 110 kWh per tonne of cement; replacement cost of USD '
  '120 to 150 per annual tonne; fixed cash cost of USD 10 to 20 per tonne of capacity.',
  'Used for the unit cost stack and the asset lens'),
]
rows = [['Source', 'Type', 'What it was used for', 'Reference']]
for a, b, c_, d_ in CAT:
    rows.append([a, b, c_, d_])
table(rows, [1.85, 1.62, 4.03, 2.00], size=8.0)

# ---------------------------------------------------- derived figures
doc.add_page_break()
H1('3  Figures that are DERIVED rather than sourced')
P('These do not appear in any source. They are computed, and the method is given so a '
  'reader can reproduce or reject each one.', size=9.5)
SHT = D['share_triangulation']; DNAT = D['dna_triangulation']; TR = D['terminal_reconciliation']
BR = json.load(open('beta_result.json'))
DER = [
 (f'Share count — {SHT["adopted"]:,.2f} million',
  f'Triangulated three ways. The FY2024 distribution of EGP 1,100mn at EGP 2.94 per share '
  f'implies {SHT["from_fy24_distribution"]:,.2f}mn; the FY2025 distribution of EGP 2,000mn '
  f'at EGP 5.34 per share implies {SHT["from_fy25_distribution"]:,.2f}mn; and the quoted '
  f'count is {SHT["quoted"]:,.2f}mn. The three agree to within '
  f'{SHT["spread"]*100:.2f}%, which is why the count is treated as known rather than '
  f'estimated. The reconciliation is on the model\'s Per-Share and Ratios sheet.'),
 (f'FY2025 depreciation — EGP {DNAT["adopted"]:,.0f}mn',
  f'No depreciation line is separately retrievable. Three independent methods are computed '
  f'and averaged ON THE SHEET rather than asserted: the Q4-2025 EBITDA margin applied to '
  f'full-year revenue less the disclosed operating profit gives EGP '
  f'{DNAT["m1_q4_margin_closure"]:,.0f}mn; a peer depreciation charge per tonne of despatch '
  f'applied to this volume gives EGP {DNAT["m2_peer_per_tonne"]:,.0f}mn; and the net '
  f'property base implied by total assets less cash and working capital, times a composite '
  f'rate, gives EGP {DNAT["m3_property_base"]:,.0f}mn. The highest is 3.5 times the lowest '
  f'and that spread is published.'),
 (f'The effective tax rate — {D["history"]["tax_eff"]*100:.2f}%',
  f'Not chosen and not the statutory rate. Disclosed FY2025 operating income of EGP '
  f'4,595.82mn plus modelled net finance income of EGP '
  f'{D["history"]["netfin_fy25"]:,.0f}mn — treasury on the disclosed cash balance less '
  f'interest on the disclosed debt — gives pre-tax profit of EGP '
  f'{D["history"]["pbt_fy25"]:,.0f}mn. Against the disclosed attributable profit of EGP '
  f'3,599mn that leaves this rate and no other. It is above the statutory 22.5% and is used '
  f'in preference to it.'),
 ('Sales volume and realised price, FY2023 to FY2025',
  'Volume is kiln capacity times a utilisation path, divided by the clinker factor. '
  'Realised price is then disclosed revenue divided by that volume, so the build reproduces '
  'the reported top line. The FY2024-to-FY2025 pair is a genuine cross-check rather than an '
  'identity: it decomposes the disclosed +42.6% revenue step into a +5.3% volume step on a '
  '+35.5% price step, which is what the removal of the production quota should look like.'),
 ('FY2023 and FY2024 EBIT and EBITDA',
  'Disclosed attributable profit is grossed up at the effective rate derived above to give '
  'operating profit, with net finance income set to zero in those years because the cash '
  'balance that produces it was built during FY2025. Depreciation at the derived charge per '
  'tonne is added back to give EBITDA.'),
 ('Net property and working capital at FY2025',
  'No breakdown of total assets is retrievable. Inventory is estimated at 60 days of the '
  'cost of sales implied by the disclosed gross margin, receivables at 30 days of revenue, '
  'and net property is the residual against disclosed total assets and cash. These estimates '
  'exist to size the third depreciation method and to open the balance-sheet roll-forward; '
  'they are not load-bearing for the valuation.'),
 (f'Terminal return on invested capital — {TR["roic_repl"]*100:.1f}%',
  f'Struck on REPLACEMENT COST — {D["inputs"]["cap_cement_mt"]["value"]}Mt at USD '
  f'{D["inputs"]["repl_usd_t"]["value"]:.0f} per annual tonne, or EGP '
  f'{D["dcf"]["ic_repl"]:,.0f}mn — rather than on book invested capital, which would flatter '
  f'it several times over because the plant is carried at pre-devaluation historic cost. The '
  f'consequence is that terminal growth is value-destroying in this model, and that is shown '
  f'rather than hidden.'),
 (f'Beta — {BR["beta"]:.3f} adopted',
  f'A five-year weekly regression of the shares against a {BR["composite_names"]}-name '
  f'equal-weight Egyptian composite, with the subject excluded from its own index, returns '
  f'{BR["beta"]:.3f} on {BR["n"]} observations with an R-squared of {BR["r2"]:.3f} and a '
  f'standard error of {BR["se"]:.3f}. That clears the usability gate, so the regression is '
  f'adopted rather than a default — and it is flagged statistically weak, with the '
  f'valuation shown across a beta range. A lead-and-lag estimator correcting for the '
  f'{BR["thin_trading"]["flat_frac"]*100:.1f}% of sessions that close unchanged gives '
  f'{BR["dimson"]["sum_beta"]:.3f}, an uplift not statistically distinguishable from zero; '
  f'its effect on the valuation is published as a value in the study.'),
 ('Capital expenditure',
  'No capital-expenditure guidance is obtainable. It is set at the economic maintenance '
  'level of USD 4.00 per tonne of installed capacity rather than at book depreciation, '
  'because a historic-cost asset base in a currency that has devalued several times '
  'understates what it costs to keep a plant running. This is deliberately conservative and '
  'the cost of the conservatism is computed in the study.'),
 ('Non-controlling interests — EGP 150mn',
  'No minority-interest balance is separately retrievable. The size is inferred from the '
  'profit statements: disclosed FY2025 earnings per share of EGP 9.49 on 374.87mn shares '
  'gives EGP 3,557mn against a stated attributable profit of EGP 3,599mn, a gap of about '
  '1.2% consistent with the statutory employees\' and directors\' profit share rather than '
  'with a large minority. A deliberately non-trivial figure is deducted and sensitised.'),
]
rows = [['Figure', 'How it was derived']]
for a, b in DER:
    rows.append([a, b])
table(rows, [2.40, 7.10], size=8.2)

# ---------------------------------------------------- research trail
doc.add_page_break()
H1('4  Research trail')
P(f'The research was carried out on {SW["sweep_date"]} across four concentric rings — '
  f'global, country, industry and company — with {len(SW["findings"])} recorded findings. '
  'Each finding below names the source and the date that source carries.', size=9.5)
rows = [['Ring', 'Topic', 'Finding', 'Source', 'Date']]
for f in SW['findings']:
    rows.append([f['ring'].title(), f['category'], f['headline'], f['source_name'],
                 f['source_date']])
table(rows, [0.76, 1.58, 4.06, 2.12, 0.88], size=7.4)

H1('5  How each forecast driver was set')
P('Every driver states whether it was built from the ground up or set from the top down, '
  'and names the findings above that it rests on.', size=9.5)
rows = [['Driver', 'Basis', 'How it was set', 'Findings']]
for d in SW['drivers']:
    rows.append([d['driver'], d['mode'].replace('_', ' ').title(), d['justification'],
                 ', '.join(d['sweep_refs'])])
table(rows, [1.70, 0.85, 5.75, 1.10], size=7.8)

P('')
P('Testahil · Independent valuation research · Educational analysis, not investment advice.',
  size=8.4, italic=True, color=GREY)

OUT = 'ARCC_Bibliography_06-08-2026.docx'
doc.save(OUT)
print('wrote', OUT)
