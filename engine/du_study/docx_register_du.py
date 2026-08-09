"""DU_Bibliography_09-08-2026.docx — the companion bibliography document.
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
H1('Emirates Integrated Telecommunications Company PJSC (DFM: DU) — Bibliography and '
   'Source Register')
P('Companion document to the valuation study dated 9 August 2026. It records where every '
  'number in that study came from.', size=9.5, color=GREY)

H2('READ FIRST')
P('This document exists so that a reader can check the study rather than trust it. It lists '
  'every input the valuation model uses, together with the value, the source, the date of '
  'that source, and the research layer it belongs to. Nothing in the study is computed from '
  'a figure that does not appear here.')
P('Two things are worth knowing before reading the tables. First, inputs marked "House" are '
  'judgements or derivations made by the analyst, not disclosures by the company — each '
  'carries the reasoning that produced it, and the reader is free to disagree with it and '
  're-run the model. Second, where a disclosure could not be reached, that is recorded as a '
  'negative result at the end of this document rather than quietly filled in.')

H2('The research layers')
table([['Layer', 'What it covers'],
       ['Company', 'the company\'s own audited/reviewed statements, filings, releases and '
        'investor presentations — the only permitted source for its reported historicals'],
       ['Industry', 'peers, the regulator, sector pricing and multiples'],
       ['Country', 'UAE macro, rates, the sovereign, the fiscal regime'],
       ['Market', 'exchange data: prices, the index, the beta regression'],
       ['House', 'analyst judgements and constructions, each with its reasoning']],
      [1.10, 5.95])

H2('Primary documents relied upon')
table([['Document', 'What it provided', 'Date', 'Where read'],
       ['Integrated Annual Report 2025 (audited consolidated FS; KPMG Lower Gulf, '
        'unmodified opinion)', 'FY2025 and re-presented FY2024: every income-statement, '
        'balance-sheet, cash-flow and segment line; notes 4-39 incl. borrowings (none), '
        'leases, tax/royalty, segments', '09-Feb-2026', 'investors.du.ae'],
       ['Annual Report 2024 (audited; PwC, unqualified)', 'FY2024 original presentation and '
        'FY2023 comparatives; the FY2023 royalty-accrual disclosure that makes the '
        'working-capital series like-for-like', '10-Feb-2025', 'investors.du.ae'],
       ['Annual Report 2023 (audited; PwC, unqualified)', 'FY2023 and complete FY2022 '
        'comparatives; the pre-2024 royalty construction (Note 27) that defines Framing B',
        '13-Feb-2024', 'investors.du.ae'],
       ['H1-2026 condensed consolidated interim FS (KPMG ISRE 2410 review)', 'H1/Q2-2026 '
        'actuals; the 30-Jun-2026 balance sheet; the licence-term note; the royalty-regime '
        'note; dividend record', '22-Jul-2026', 'investors.du.ae'],
       ['Q1-2026 condensed consolidated interim FS (KPMG review)', 'Q1-2026 actuals',
        '22-Apr-2026', 'investors.du.ae'],
       ['Q2-2026 earnings release + analyst presentation', 'subscribers, ARPU, capex '
        'intensity, revised FY2026 guidance, interim dividend', '23-Jul-2026',
        'investors.du.ae'],
       ['Q4/FY2025 results presentation', 'FY2025 KPIs, subscriber base, original FY2026 '
        'guidance, dividend and payout record', '10-Feb-2026', 'investors.du.ae'],
       ['UAE MoF T-bond auction results; Emirates Islamic AED yield sheet', 'the AED '
        'risk-free anchor and curve context', 'Jul/Aug-2026', 'public market data'],
       ['Damodaran country risk dataset (ctryprem)', 'UAE rating-based default spread and '
        'equity risk premium; the live implied US premium', '05-Jan-2026 / 01-Aug-2026',
        'pages.stern.nyu.edu/~adamodar'],
       ['DFM official index API + cross-validated Yahoo history', 'the DFM General Index '
        'series behind the beta regression (identical closes on all 307 overlapping '
        'sessions)', '2021-2026', 'api2.dfm.ae / finance.yahoo.com'],
       ['stc USD sukuk curve quotes', 'the GCC telecom credit spread behind the marginal '
        'cost of debt', '06-Aug-2026', 'public market data'],
       ['IMF World Economic Outlook (Apr-2026) and July-2026 Update', 'UAE and regional '
        'growth/inflation; the war\'s macro baseline', 'Apr/Jul-2026', 'imf.org']],
      [2.30, 2.95, 0.85, 0.90])

H1('The full input register')
import collections
groups = collections.OrderedDict()
for k, rec in INP.items():
    ring = rec['ring'].split('/')[0]
    groups.setdefault(ring, []).append((k, rec))
for ring, items in groups.items():
    H2(f'{ring} layer — {len(items)} inputs')
    rows = [['Input', 'Value', 'Source and construction', 'Date']]
    for k, rec in items:
        rows.append([k, fmt(rec['value']), rec['source'], rec['date']])
    table(rows, [1.05, 1.15, 4.10, 0.75], size=7.4)

H1('The judgements, stated separately')
P('Every forecast rests on judgements. Each is stated here with what would overturn it.')
table([['Judgement', 'Basis', 'What would overturn it'],
       ['The fiscal regime persists at the current 43.6% combined take (Framing A is the '
        'base)', 'the legislated 2024-2026 regime; a ministry notification extending the '
        'structure to 2027-2029 disclosed by the peer operator', 'du\'s own disclosure of '
        'different post-2026 terms — Framing B is priced throughout in case'],
       ['Mobile recovers to 9,450k subscribers by end-2026, then adds ~210-310k/yr',
        'the company\'s own Q2 commentary (recovery underway, gross adds below pre-war), '
        'Dubai population re-acceleration', 'a re-opened conflict, or two quarters of '
        'negative total net adds'],
       ['Blended ARPU essentially flat', 'four quarters printed within 63.3-63.4; postpaid '
        'mix offsetting prepaid dilution; no price war in the record', 'ARPU below AED 60 '
        'without a disclosed mix explanation'],
       ['Contribution margins hold at audited FY2025 rates (ICT lifts on scale)',
        'two consistent disclosed years within ~1pp per segment', 'a disclosed margin '
        'reset — e.g. wholesale repricing or ICT mix collapse'],
       ['Capex peaks at 15.5% of revenue then glides to 13%', 'commitments up ~14% in six '
        'months; the disclosed data-centre programme; no numeric company guidance '
        '(flagged)', 'company capex guidance above the path, or the programme extending '
        'past FY2028'],
       ['Payout stays at 98%', 'FY2024 actual 98%, FY2025 ~100%, interim raised through the '
        'war quarter', 'any declared cut'],
       ['Beta 0.472 from the own-index regression', 'five years weekly, R² 0.20, gate '
        'passed, composite cross-check 0.394', 'a structural re-rating of DFM correlations; '
        'the 0.57-0.80 alternatives are priced'],
       ['Terminal growth 2.5%', 'below long-run UAE nominal GDP (~4%+); duopoly at '
        'population-plus-inflation minus price erosion', 'sustained sub-2% revenue growth '
        'after the recovery completes'],
       ['Lease replacement charged at right-of-use depreciation', 'conservative: actual '
        'FY2025 lease additions ran at a quarter of depreciation', 'a disclosed structural '
        'shift to leased infrastructure']],
      [1.85, 2.60, 2.60], size=7.8)

H1('Negative results — what could not be sourced')
table([['What was sought', 'Where', 'Outcome'],
       ['UAE sovereign 5-year credit-default-swap quote', 'cbonds (403), '
        'worldgovernmentbonds (script-only), Damodaran (prints NA for UAE)',
        'NOT SOURCED — the market-spread premium basis uses the traded Abu Dhabi USD '
        'curve (+25bp) instead, disclosed in section 1.8'],
       ['Peer EV/EBITDA multiples, clean', 'public aggregators', 'net-debt figures missing '
        'or stale — the relative lens runs on P/E and dividend yield only, stated in 1.3'],
       ['Concluded TDRA licence-renewal terms', 'TDRA site, du IR disclosure list, DFM '
        'announcements, press', 'NOT FOUND at the sweep date — the licence note in the '
        'H1-2026 interims is the latest primary word; treated as catalyst 2'],
       ['du\'s own disclosure of the post-2026 royalty regime', 'du filings and DFM '
        'disclosures', 'NOT FOUND — the H1-2026 notes still say "effective from 2024 to '
        '2026"; the extension notification is disclosed by e&, not yet by du; both '
        'framings priced'],
       ['Wholesale and ICT unit KPIs (minutes, racks, MW, backlog)', 'AR2023-AR2025, all '
        'interims, all decks', 'never disclosed — both segments built top-down, flagged'],
       ['Numeric FY2026 capex guidance', 'Feb/Apr/Jul-2026 releases and decks',
        'not guided — house path anchored on disclosed commitments, flagged'],
       ['Analyst consensus on du', 'public sources', 'not cleanly retrievable (searches '
        'polluted by the exchange\'s own ticker); noted, not used']],
      [2.20, 2.30, 2.55], size=7.8)

H1('A note on source discrepancies')
P('Three discrepancies a checking reader will find, all explained rather than smoothed: '
  '(1) FY2024 EBITDA is 6,469.8 in this study (the IFRS 18 re-presented comparative on the '
  'face of the FY2025 statements) but derives as 6,472.2 from the original FY2024 '
  'presentation — the re-presented basis is used so FY2024 and FY2025 sit on one '
  'presentation. (2) FY2024 federal royalty is 1,571.6 on the re-presented face but 1,675.9 '
  'in the original FY2024 statements (which included prior-period adjustments); the '
  're-presented figure is carried, and the FY2024 effective-rate note (44.7%) belongs to '
  'the original basis. (3) The company\'s IR capex (cost-additions basis, 2,274 for FY2025) '
  'differs from the cash-flow-statement capex (2,353.2) used in the model; the audited cash '
  'basis is used and the IR basis is quoted only where the IR intensity ratios are cited.')

H1('Disclosure')
P('This bibliography is part of an educational analysis and is not investment advice. '
  'Sources are quoted for verification; all errors of transcription are the authors\' own. '
  '© Testahil, 2026.', size=9.3)

doc.save(os.path.join(HERE, 'DU_Bibliography_09-08-2026.docx'))
print('wrote DU_Bibliography_09-08-2026.docx')
