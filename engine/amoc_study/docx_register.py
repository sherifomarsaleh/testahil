"""AMOC_Bibliography_06-08-2026.docx — the companion bibliography document.

Every input in the model: value, source, date and research layer — emitted directly from
study_numbers.json (the compute script's own INPUTS block), plus the document bibliography,
the triangulations, and the negative results.
"""
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
BASE, BETA = D['base'], D['wacc']['beta']
INK = RGBColor(0x1C, 0x3A, 0x36); GREY = RGBColor(0x6E, 0x7B, 0x77)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
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
    if isinstance(v, bool):
        return str(v)
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
H1('Alexandria Mineral Oils Company S.A.E. (EGX: AMOC) — Bibliography and Source Register')
P('Companion document to the valuation study dated 6 August 2026. It records where every number '
  'in that study came from.', size=9.5, color=GREY)

H2('READ FIRST')
P('This document exists so that a reader can check the study rather than trust it. It lists every '
  'input the valuation model uses, together with the value, the source, the date of that source '
  'and the research layer it belongs to. Nothing in the study is computed from a figure that does '
  'not appear here.')
P('Three things are worth knowing before reading the tables. First, inputs marked "House" are '
  'judgements or derivations made by the analyst, not disclosures by the company; each carries '
  'the reasoning that produced it, and a reader is free to disagree and re-run the model. Second, '
  'several figures are TRIANGULATED — derived independently by more than one route and averaged, '
  'with all the routes shown, because the underlying figure was disclosed only through a growth '
  'rate. Third, where a source could not be reached, that is recorded as a negative result at the '
  'end of this document rather than quietly filled in.')

H2('An unusual limitation of this edition, stated up front')
P('Primary filings were NOT reachable from the environment in which this study was built. The '
  'company\'s investor-relations site, the exchange\'s disclosure pages and the commercial '
  'financial-data terminals all refused connections under the network policy in force. Every '
  'company figure in this study therefore comes from published reporting of the company\'s '
  'releases and from financial-data aggregators, not from the audited statements themselves.')
P('The response to that constraint was not to proceed quietly. It was to (a) triangulate every '
  'material figure across independent sources and show the triangulation on the face of the '
  'model, (b) reconstruct the base year from two separately disclosed halves rather than accept '
  'any single reported twelve-month figure, and (c) mark every reconstructed line as '
  'reconstructed wherever it appears. A reader with access to the audited statements should treat '
  'this register as the list of things to check first.')

H2('The research layers')
table([['Layer', 'What it covers'],
       ['Company', 'Alexandria Mineral Oils\' own results releases, general-assembly resolutions '
        'and disclosed operating statistics, as reported by the trade and financial press'],
       ['Country', 'Egyptian macroeconomic and sovereign data: policy rates, government bond '
        'yields, sovereign spreads, the exchange rate, the tax regime, the country equity risk '
        'premium'],
       ['Industry', 'Lubricant base oils, paraffin wax and refined-product markets; the crude '
        'and product price deck'],
       ['Global', 'World interest rates and growth used in the currency-of-discounting '
        'alternative and the terminal ceiling'],
       ['House', 'Analyst judgement — forecast drivers, normalisation choices and cost-of-capital '
        'construction. Each is argued in place rather than asserted']],
      [1.05, 5.95], size=8.6)

H2('Primary sources relied upon')
table([['Source', 'Publisher', 'Date', 'What was taken from it'],
       ['"AMOC Doubles FY 2025/26 Profit as Revenue Expands 35%"', 'Egypt Oil & Gas',
        'Aug 2026',
        'Revenue and profit after tax for the six months to 30 June 2026, on both a consolidated '
        'and a standalone basis, together with operating cash flow. Carried as corroboration '
        'only; the period it covers was IDENTIFIED by reconciling its two reported growth rates '
        'against the constructed comparative'],
       ['"AMOC Net Profit Rises 37% in Q1 2026"', 'Egypt Oil & Gas', 'Apr–May 2026',
        'Consolidated net sales of EGP 10.51bn and consolidated net profit of EGP 635.12mn for '
        'the quarter to 31 March 2026, with the prior-year comparative. Also the confirmation '
        'that the company now reports on CALENDAR quarters'],
       ['"AMOC Reports Sales of EGP 20 Bn in H2 2025" and the general-assembly report',
        'Egypt Oil & Gas; Egyptian Ministry of Petroleum', 'Mar 2026',
        'The July–December 2025 transition period: 808,000 tonnes sold, sales of about EGP 20bn, '
        'a 14.5% growth rate, exports of about 42,000 tonnes up 40%, the EGP 0.40 per share '
        'dividend approved on 28 March 2026, and the four new storage tanks'],
       ['"AMOC\'s consolidated profits rise 2% YoY in H1 FY 2025/26"', 'Arab Finance',
        'Feb 2026',
        'Consolidated sales of EGP 20.735bn against EGP 18.246bn, and consolidated profit after '
        'tax of EGP 656.428mn, +2%. The prior-year comparative half is what makes the base-year '
        'construction possible'],
       ['"AMOC Reports 27% Sales Growth for Q1 FY2025/26"', 'Egypt Oil & Gas', 'Nov 2025',
        'Standalone and consolidated net sales and profit for the quarter to 30 September 2025'],
       ['"AMOC Reports 17.3% Increase in Standalone Net Profit for FY 2024/25" and the FY2024/25 '
        'results commentary', 'Egypt Oil & Gas; MarketScreener', 'Sep–Oct 2025',
        'Standalone profit of EGP 1.49bn (+17.3%) and consolidated profit of EGP 1.55bn (+3%) '
        'for the year to 30 June 2025; sales of 1.26mn tonnes valued at EGP 36.9bn, +10.8% on '
        '2023/24; output of oils and waxes of 172,000 tonnes at 108% of target'],
       ['"AMOC approves FY2025/26 planning budget"; "AMOC Approves EGP 580mm Capital Budget"',
        'Zawya / Reuters; Egypt Oil & Gas', 'Jun–Jul 2025',
        'The approved capital budget of EGP 580.19mn and the planning-budget net sales of EGP '
        '37.332bn — the anchor for the capital-expenditure driver'],
       ['"AMOC\'s Exceptional Fiscal Year 22/23 Results Gain Approval at the Annual General '
        'Assembly"', 'MoneyController', '2023',
        'Cost of sales of EGP 21,218.64mn and gross profit of EGP 1,297.01mn for the year to 30 '
        'June 2023 — the ONLY period for which both the cost line and the margin line are '
        'separately available, and therefore the anchor for the whole margin discussion'],
       ['Company financial summary pages', 'stockanalysis.com; Investing.com; TradingView',
        'Aug 2026',
        'Shares outstanding, market capitalisation, total assets, total liabilities, cash and '
        'equivalents, total debt, dividend per share and payout ratio'],
       ['Monetary Policy Report Q1 2026 and the August 2026 rate decision',
        'Central Bank of Egypt', '2026',
        'Main operation rate 19.50% (corridor 19.00/20.00), held for a second consecutive '
        'meeting; annual headline inflation of 14.30% in June 2026; the 7% (±2pp) fourth-quarter '
        '2026 and 5% (±2pp) fourth-quarter 2028 inflation targets used to build the terminal '
        'risk-free rate'],
       ['Country default spreads and risk premiums, Egypt row',
        'A. Damodaran, Stern School of Business, New York University', 'January 2026',
        'The credit-default-swap-basis equity risk premium and sovereign default spread used as '
        'primary, and the rating-basis pair disclosed as the computed alternative'],
       ['Egyptian pound closing rates and the 10-year government bond yield',
        'Amwal Al Ghad; house cost-of-capital reference', 'Jul–Aug 2026',
        'USD/EGP at 50.25 (close of 50.30/50.40 on 4 August 2026) and the 10-year local-currency '
        'yield of 22.31%'],
       ['engine/raw_ohlc/EG/AMOC.csv — daily open, high, low, close and volume',
        'Vendor export, screened through the house data-quality gate', '2 Jan 2011 – 6 Aug 2026',
        'The full price history: the closing price the study is anchored on, the beta regression, '
        'the volatility estimate and the simulated price distribution']],
      [1.85, 1.30, 0.80, 3.10], size=7.9)

# ---- the triangulations -----------------------------------------------------
H1('Triangulated figures — every route shown')
P('Where a figure was disclosed only through a growth rate, it is derived by more than one '
  'independent route and the AVERAGE is carried. The routes are on the face of the companion '
  'model as live formulas, not asserted here.')
table([['Figure', 'Route', 'Value (EGP mn)', 'Adopted'],
       ['FY2023/24 revenue', 'A: prior-year comparative in the FY2024/25 summary',
        f"{INP['rev_fy24_a']['value']:,.0f}", f"{BASE['rev_fy24']:,.0f}"],
       ['', 'B: back-solved from the company\'s own "+10.8% on 2023/24" statement',
        f"{INP['rev_fy24_b']['value']:,.0f}", ''],
       ['FY2024/25 revenue', 'A: company release — 1.26mn tonnes valued at EGP 36.9bn',
        f"{INP['rev_fy25_a']['value']:,.0f}", f"{BASE['rev_fy25']:,.0f}"],
       ['', 'B: aggregator fiscal-2025 revenue line',
        f"{INP['rev_fy25_b']['value']:,.0f}", ''],
       ['', 'C: the same release\'s separate "revenues" figure',
        f"{INP['rev_fy25_c']['value']:,.0f}", ''],
       ['Shares outstanding (mn)', 'A: reported shares outstanding', '1,291.56', '1,291.56'],
       ['', 'B: FY2024/25 standalone profit over this count gives EGP 1.154 a share, and the '
        'declared EGP 0.80 dividend over that is a 69.3% payout against a 69.4% reported ratio',
        'confirms', ''],
       ['', 'C: reported market capitalisation of EGP 11.51bn implies EGP 8.91 a share against '
        'a 6 August close of EGP 9.10', 'confirms', '']],
      [1.35, 3.45, 1.00, 0.95], size=8.0)

H2('The period-identification check')
P('One reported figure required its PERIOD to be established before it could be used. A release '
  'labelled "FY 2025/26" reports revenue of EGP 26.2bn (+35%) and profit after tax of EGP 1.90bn '
  '(+109%). Those cannot describe a twelve-month period, because the July–December 2025 half '
  'alone was EGP 20.735bn. Against the January–June 2025 half constructed from disclosed figures '
  f"— revenue EGP {BASE['rev_h1cy25']:,.0f}mn and profit EGP {BASE['pat_h1cy25']:,.0f}mn — the "
  f"same two figures are {BASE['implied_growth_rev']*100:+.1f}% and "
  f"{BASE['implied_growth_pat']*100:+.1f}%, reproducing BOTH reported growth rates "
  'independently. Two independent exact matches identify the period as the six months to 30 June '
  '2026. It is carried as corroboration and not as the forecast base.')

# ---- the full input register ------------------------------------------------
H1('The full input register')
P('Every hardcoded figure the compute script consumes, in the order it is declared. A bare '
  'numeral anywhere in the inputs block fails the build, so this table is complete by '
  'construction.')
by_ring = {}
for k, v in INP.items():
    by_ring.setdefault(v['ring'], []).append((k, v))
for ring in ('Company', 'Industry', 'Country', 'Global', 'House'):
    if ring not in by_ring:
        continue
    H2(f'{ring} layer — {len(by_ring[ring])} inputs')
    rows = [['Input', 'Value', 'Date', 'Source and reasoning']]
    for k, v in by_ring[ring]:
        rows.append([k, fmt(v['value']), v['date'], v['source']])
    table(rows, [1.30, 1.00, 0.72, 4.05], size=7.5)

# ---- negative results -------------------------------------------------------
H1('Negative results — what could not be sourced')
P('Recorded rather than filled in. Each of these is a place where a reader with better access '
  'can improve the study.')
table([['What was sought', 'Why it matters', 'Outcome'],
       ['The audited consolidated financial statements for the year to 30 June 2025 and the '
        'transition period to 31 December 2025',
        'Would replace the entire reconstructed balance sheet and the closed income statement '
        'with disclosed lines',
        'NOT REACHED. The company\'s investor-relations site and its published statement PDFs '
        'refused connection under the network policy in force'],
       ['The exchange\'s own disclosure pages for the company',
        'Would confirm the transition-period filing and the year-end change directly rather than '
        'through reporting of them',
        'NOT REACHED. Same cause'],
       ['An AUDITED segmental or product-line revenue note',
        'The three-line build used here rests on a reported product table — tonnes and value for '
        'base oils, paraffin wax and the total — rather than on an audited segment note',
        'PARTIALLY REACHED. The product table was obtained in reported form, not from the filing '
        'itself, and is flagged as such at its input. It was validated three ways before '
        'adoption: the two disclosed shares are internally coherent '
        f"({D['unit']['spec_share_t']*100:.2f}% of tonnes against "
        f"{D['unit']['spec_share_v']*100:.2f}% of value); the implied dollar realisations of "
        f"USD {D['unit']['px_usd']['oil']:,.0f}, {D['unit']['px_usd']['wax']:,.0f} and "
        f"{D['unit']['px_usd']['fuel']:,.0f} a tonne are the right levels and the right ORDER "
        'for SN-grade base oil, fully refined paraffin and a gas-oil blend; and rolling the '
        'three lines forward reproduces the independently built calendar-2025 revenue to within '
        f"{abs(D['unit']['recon']-1)*100:.1f}%. No price in the model is calibrated and none is "
        'a residual'],
       ['A disclosed non-controlling-interest balance or profit share',
        'The minority deduction in the bridge is inferred from the gap between consolidated and '
        'standalone profit',
        f"NOT FOUND. Held at {D['dcf']['nci_share']*100:.1f}% and sensitised to "
        f"{D['dcf']['nci_alt']*100:.0f}%, which moves the answer by "
        f"{(D['dcf']['ps_nci_alt']/D['dcf']['ps']-1)*100:+.1f}%"],
       ['A disclosed depreciation charge, capital-expenditure actual, or property, plant and '
        'equipment balance',
        'All three are drivers of the free-cash-flow waterfall',
        'NOT FOUND as disclosed lines. The capital budget of EGP 580.19mn is disclosed and is '
        'used as the anchor; depreciation is set as a share of revenue and property, plant and '
        'equipment is the residual against disclosed total assets'],
       ['A traded credit-default-swap quote for Egypt as at August 2026',
        'The sovereign spread netted out of the risk-free rate',
        'NOT REACHED live. The January-2026 published country-premium file is used, and the '
        'rating-basis alternative is computed and published as a value'],
       ['Listed peer multiples for Egyptian or regional lubricant base-oil processors',
        'The relative lens',
        'NO DIRECT LISTED COMPARATOR EXISTS — the company is the only listed refinery on the '
        'exchange. The multiple range used is taken from the international Group I base-oil and '
        'independent-processor band and is disclosed as such rather than presented as a peer set']],
      [1.95, 2.10, 2.90], size=7.9)

H1('Method note')
P('All financial arithmetic in the study originates in an executed, asserting compute script. '
  'Every hardcoded figure enters through the four-field register reproduced above; the script '
  'refuses to emit its results unless the enterprise-to-equity bridge closes exactly, terminal '
  'value as a percentage of enterprise value is computed and printed, the implied fair value '
  'sits inside a stated plausibility band, and net debt and minority interests carry the correct '
  'signs into the bridge.')
P('The companion workbook was verified on the DELIVERED file rather than on the script that '
  'wrote it: every formula cell was independently re-evaluated and required to reproduce the '
  'model\'s own value with none unresolvable and none unchecked, and every input was perturbed '
  'in place with the whole workbook re-evaluated to confirm it moves the headline in the '
  'asserted direction.')

doc.save(os.path.join(HERE, 'AMOC_Bibliography_06-08-2026.docx'))
print('wrote AMOC_Bibliography_06-08-2026.docx')
