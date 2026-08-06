"""SWDY_Bibliography_05-08-2026.docx — the companion bibliography document.
Every input in the model: value, source, date and research layer — emitted from
study_numbers.json (the compute script's own INPUTS block), plus the document
bibliography and the negative results."""
import json, os
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, 'study_numbers.json')))
INP = D['inputs']
INK = RGBColor(0x1C, 0x3A, 0x36); GREY = RGBColor(0x6E, 0x7B, 0x77); WHITE = RGBColor(0xFF, 0xFF, 0xFF)
F_DARK, F_PANEL, F_CREAM = '1C3A36', 'EAF0EE', 'F6F1E6'

doc = Document()
sec = doc.sections[0]
sec.page_width, sec.page_height = Inches(8.5), Inches(11)
sec.left_margin = sec.right_margin = Inches(0.7)
sec.top_margin = sec.bottom_margin = Inches(0.6)
st = doc.styles['Normal']
st.font.name = 'Calibri'; st.font.size = Pt(10); st.font.color.rgb = INK
st.paragraph_format.space_after = Pt(5)

def shade(cell, hexcolor):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd'); shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto'); shd.set(qn('w:fill'), hexcolor)
    tcPr.append(shd)

def cell_margins(table, top=36, bottom=36, left=80, right=80):
    m = OxmlElement('w:tblCellMar')
    for tag, v in [('top', top), ('left', left), ('bottom', bottom), ('right', right)]:
        e = OxmlElement(f'w:{tag}'); e.set(qn('w:w'), str(v)); e.set(qn('w:type'), 'dxa')
        m.append(e)
    table._tbl.tblPr.append(m)

def borders(table, color='C9D4D1', sz='4'):
    b = OxmlElement('w:tblBorders')
    for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        e = OxmlElement(f'w:{edge}')
        e.set(qn('w:val'), 'single'); e.set(qn('w:sz'), sz)
        e.set(qn('w:space'), '0'); e.set(qn('w:color'), color)
        b.append(e)
    table._tbl.tblPr.append(b)

def P(text='', size=10, bold=False, italic=False, color=INK, space_after=5, space_before=0):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.font.size = Pt(size); r.bold = bold; r.italic = italic; r.font.color.rgb = color
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.space_before = Pt(space_before)
    return p

def H1(t): return P(t, size=13, bold=True, space_before=12, space_after=4)
def H2(t): return P(t, size=11, bold=True, space_before=8, space_after=3)

def table(rows, widths, size=8.2, header=True):
    t = doc.add_table(rows=len(rows), cols=len(widths))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell_margins(t); borders(t); t.autofit = False
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
            if i == 0 and header:
                r.bold = True; shade(c, F_PANEL)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return t

def masthead():
    t = doc.add_table(rows=1, cols=1)
    cell_margins(t, 80, 80, 150, 150)
    c = t.cell(0, 0); shade(c, F_DARK); c.width = Inches(7.1)
    p = c.paragraphs[0]
    r = p.add_run('Testahil · Independent Valuation Study — Educational Analysis')
    r.bold = True; r.font.size = Pt(11); r.font.color.rgb = WHITE
    r2 = p.add_run('   Not investment advice')
    r2.font.size = Pt(9.5); r2.font.color.rgb = RGBColor(0x9F, 0xB0, 0xAC)
    doc.add_paragraph().paragraph_format.space_after = Pt(0)

def fmt(v):
    if isinstance(v, float):
        return f"{v:,.4f}".rstrip('0').rstrip('.') if abs(v) < 100 else f"{v:,.1f}"
    if isinstance(v, int):
        return f"{v:,}"
    if isinstance(v, dict):
        return "; ".join(f"{k}: {fmt(x)}" for k, x in v.items())
    if isinstance(v, (list, tuple)):
        return ", ".join(fmt(x) for x in v)
    return str(v)

# ============================================================================
masthead()
H1('Elsewedy Electric Company S.A.E. (EGX: SWDY) — Bibliography and Source Register')
P('Companion document to the valuation study dated 5 August 2026. It records where every number '
  'in that study came from.', size=9.5, color=GREY)

H2('READ FIRST')
P('This document exists so that a reader can check the study rather than trust it. It lists every '
  'input the valuation model uses, together with the value, the source, the date of that source, '
  'and the research layer it belongs to. Nothing in the study is computed from a figure that does '
  'not appear here.')
P('Two things are worth knowing before reading the tables. First, inputs marked "House" are '
  'judgements or derivations made by the analyst, not disclosures by the company — each carries '
  'the reasoning that produced it, and the reader is free to disagree with it and re-run the '
  'model. Second, where a company disclosure could not be reached, that is recorded as a negative '
  'result at the end of this document rather than quietly filled in.')

H2('The research layers')
table([['Layer', 'What it covers'],
       ['Market', 'Prices, volumes and market-observable data for the security itself'],
       ['Country', 'Egyptian macroeconomic and sovereign data: policy rates, government bond '
        'yields, sovereign spreads, the exchange rate, the tax regime, the country equity risk '
        'premium'],
       ['Industry', 'The wires and cables sector, engineering and construction, input costs and '
        'the competitive frame'],
       ['Company', 'Elsewedy Electric\'s own audited and interim financial statements, earnings '
        'releases, exchange filings and disclosures'],
       ['House', 'Analyst judgement — forecast drivers, normalisation choices and cost-of-capital '
        'construction. Each is argued in place rather than asserted']],
      [1.05, 5.95], size=8.6)

H2('Primary documents relied upon')
table([['Document', 'Publisher', 'Date', 'What was taken from it'],
       ['Consolidated financial statements for the year ended 31 December 2024 (audited, '
        'translated from Arabic)', 'Elsewedy Electric Company', '12 March 2025',
        'Full consolidated statement of cash flows; loans and borrowings note including the '
        'financing-liability reconciliation; interest-rate risk note with average rates by '
        'currency; currency risk note; goodwill impairment note'],
       ['Q4 2024 earnings release (FY 2024 results)', 'Elsewedy Electric Company', '13 March 2025',
        'Consolidated income statement FY2024 with FY2023 comparatives; consolidated balance sheet '
        'at 31 December 2024 and 2023; segment revenue and gross profit table; net debt; share '
        'count; shareholder structure; proposed dividend'],
       ['Q2 2024 earnings release (H1 2024 results)', 'Elsewedy Electric Company', '15 August 2024',
        'Segment operating detail including cable sales volumes and gross profit per tonne; '
        'turnkey backlog and awards by sector and region; balance sheet at 31 December 2023'],
       ['Q1 2025 earnings release', 'Elsewedy Electric Company', '26 May 2025',
        'Q1-2025 income statement, EBITDA and net bank debt; the restated five-segment reporting '
        'structure; shareholder structure at 31 March 2025'],
       ['Condensed consolidated interim financial statements, three months ended 31 March 2025',
        'Elsewedy Electric Company', '26 May 2025',
        'Q1-2025 statement of profit or loss; interim statement of cash flows including '
        'depreciation, capital expenditure, interest paid and net movement in borrowings'],
       ['Segment analysis workbooks, Q4 2024 and Q1 2025', 'Elsewedy Electric Company',
        '13 March 2025 / 26 May 2025',
        'Segment revenue, gross profit, selling expense and depreciation by segment on both the '
        'old and the restated segment taxonomy'],
       ['Q4 2025 earnings release (FY 2025 results) — reported figures',
        'Elsewedy Electric Company, via financial press covering the exchange filing',
        'March 2026',
        'FY2025 revenue, profit after tax, profit after minority interests, total assets, net bank '
        'debt, fourth-quarter gross profit and EBITDA. The release itself was not directly '
        'reachable — see the negative results below'],
       ['Q1 2026 exchange filing — reported figures',
        'Elsewedy Electric Company, via financial press covering the exchange filing',
        '13 May 2026', 'Q1-2026 revenue and profit attributable to the parent'],
       ['Country risk premium and default spread file', 'Damodaran, NYU Stern',
        '5 January 2026', 'Egypt equity risk premium and sovereign default spread, credit-default-'
        'swap basis and rating basis'],
       ['Egypt 10-year local-currency government bond yield', 'Market data, house cost-of-capital '
        'reference', '21 July 2026, re-verified 5 August 2026', 'The risk-free rate anchor'],
       ['Worldwide Tax Summaries — Egypt', 'PwC', '2026', 'Corporate income tax rate'],
       ['Daily price history for SWDY on the Egyptian Exchange', 'Supplied price series',
        'to 5 August 2026',
        'The anchor price, the volatility estimate, the moving-average structure, the beta '
        'regression and the price distributions'],
       ['Daily price history for the covered Egyptian equity library', 'House data library',
        'to August 2026', 'The 31-name equal-weight composite used as the market proxy in the '
        'beta regression']],
      [1.55, 1.25, 0.95, 3.25], size=8.0)

# ---- the four-field input register ------------------------------------------
H1('The full input register')
P('Every input to the valuation model, in the order the model declares them. The "Layer" column '
  'is the research layer defined above. Values are shown as the model holds them: EGP millions '
  'for financial-statement lines, decimals for rates and shares.', size=9.5, color=GREY)

for ring in ['Market', 'Company', 'Country', 'House']:
    items = [(k, v) for k, v in INP.items() if v['ring'] == ring]
    if not items:
        continue
    H2(f'{ring} layer — {len(items)} inputs')
    rows = [['Input', 'Value', 'Date', 'Source and construction']]
    for k, v in items:
        rows.append([k.replace('_', ' '), fmt(v['value']), v['date'], v['source']])
    table(rows, [1.15, 0.95, 0.72, 4.18], size=7.6)

# ---- judgements ---------------------------------------------------------------
H1('The judgements, stated separately')
P('These are the places where the analyst chose rather than observed. They are collected here so '
  'a reader can find them without reading the whole study.')
table([['Judgement', 'What was chosen', 'Why', 'What would overturn it'],
       ['Currency of discounting',
        'The full Egyptian cost of capital is charged to the whole company as the primary reading; '
        'the hard-currency alternative is computed and shown but not averaged in',
        'The shares trade, and dividends are paid, in Egyptian pounds on an Egyptian exchange, and '
        'realising value depends on Egyptian capital-account conditions',
        'Evidence that convertibility is not a binding constraint for this issuer would shift the '
        'primary reading materially higher'],
       ['Exchange-rate path',
        'About 6% a year of depreciation, far below what the interest-rate differential implies',
        'The base case assumes the central bank\'s disinflation path closes most of the gap rather '
        'than the currency absorbing it',
        'A disorderly move in the pound; the sensitivity table carries the parity case'],
       ['Working capital held flat at the historical share of revenue',
        'Net working capital stays near the level the two audited years show',
        'Two audited years show it rising with revenue rather than converting',
        'Two consecutive halves of operating cash flow above 60% of EBITDA'],
       ['Terminal growth of 5%',
        'The standing centre for established names in this market, sensitised 3–7%',
        'It is below the blended long-run nominal growth ceiling of the economies the company '
        'operates in, and is reconciled to the return on capital and reinvestment rate',
        'A demonstrated structural change in the export franchise\'s long-run growth'],
       ['Cost of debt at the blended rather than the domestic rate',
        'A currency-blended rate near the independently computed effective rate',
        'The audited notes disclose materially cheaper hard-currency borrowing, and most of the '
        'book is hard currency',
        'A shift of the debt book back into Egyptian pounds'],
       ['Minority interests charged at their share of group profit',
        'Rather than at book value',
        'Minorities take a larger share of profit than of book equity, so the profit share is the '
        'conservative charge',
        'A reader preferring the book convention can add the difference back; the amount is stated '
        'in the study'],
       ['Effective tax rate of 25% for NOPAT',
        'Above the Egyptian statutory rate',
        'Reported effective rates ran above statutory in every historical year because foreign '
        'profits are taxed elsewhere',
        'The audited FY2025 tax note'],
       ['FY2025 income statement closed to reported profit',
        'EBITDA set at the disclosed margin; the tax rate closes the account',
        'Only the top and bottom lines were disclosed for FY2025',
        'The audited FY2025 consolidated statements']],
      [1.35, 1.75, 2.05, 1.85], size=7.8)

# ---- negative results ---------------------------------------------------------
H1('Negative results — what could not be sourced')
P('Recorded because an unsourced gap that is not disclosed becomes an invisible assumption.')
table([['What was sought', 'Outcome', 'How the study handled it'],
       ['Audited consolidated financial statements for FY2025',
        'Not reachable. The company\'s investor-relations site and the exchange\'s filing archive '
        'were both unreachable from the research environment; the company\'s document repository '
        'was reachable but its contents stop at the first quarter of 2025',
        'FY2025 was built from the disclosed headline figures reported by financial press covering '
        'the exchange filing, cross-checked against each other and against the quarterly path. '
        'Every derived line is labelled in the study and in the register above'],
       ['The Q4 2025 and Q1 2026 earnings releases in full',
        'Located but not retrievable; the hosting domains were unreachable',
        'Headline figures were taken from press coverage of the filings. Segment detail for FY2025 '
        'and Q1 2026 does not exist in the study as a result — segment shares are apportioned from '
        'company commentary and the last fully disclosed segment table'],
       ['FY2025 balance sheet beyond total assets and net bank debt',
        'Not disclosed in any reachable source',
        'Triangulated by three independent methods; the spread is shown in the study and only the '
        'disclosed net debt enters the valuation bridge'],
       ['A facility-by-facility currency split of the debt book',
        'Not disclosed at that granularity',
        'The split was inferred from the disclosed average rates by currency and the independently '
        'computed blended effective rate, and is labelled as inferred'],
       ['An explanation for the sharp single-session price move on 4 August 2026',
        'No corresponding company disclosure or news item was found',
        'Not used. The study\'s anchor is the closing price on 5 August 2026 and no narrative is '
        'attached to the move']],
      [1.55, 2.35, 3.10], size=7.8)

H1('A note on aggregator data')
P('Aggregator and data-vendor figures were used only where a company source was unavailable, and '
  'they were checked against the company\'s own disclosures wherever both existed. One material '
  'discrepancy was found and is recorded here: a widely syndicated "FY2025" balance sheet — total '
  'assets, total equity, total debt and cash — reproduces the company\'s audited 31 December 2024 '
  'figures exactly, one year stale. It was discarded. The FY2025 balance-sheet figures used in '
  'this study are the disclosed total assets and net bank debt, plus the triangulation described '
  'above.')

H1('Disclosure')
P('This document accompanies an educational valuation study. It is not investment advice and '
  'contains no recommendation, rating or price target. Sources are listed so that readers can '
  'verify the analysis independently. Where a figure is derived or estimated rather than '
  'disclosed, that is stated.', size=9.2, color=GREY)

out = os.path.join(HERE, 'SWDY_Bibliography_05-08-2026.docx')
doc.save(out)
print(f'wrote {out} | {len(doc.paragraphs)} paragraphs | {len(doc.tables)} tables | '
      f'{len(INP)} inputs registered')
