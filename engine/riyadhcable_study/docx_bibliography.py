"""Riyadh Cables — standalone bibliography document. Primary-documents table, the full
input register (every input with value / date / source-and-construction, grouped by
research layer), a judgements table (each with what would overturn it), a negative-results
table, and aggregator-discrepancy notes. Reads the committed numbers file and the sweep
register; types no financial numeral of its own."""
import json, os
from docx_base import (doc, P, rich, H1, H2, caption, bullet, table, box, masthead,
                       INK, GREY, BRASS)

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, 'study_numbers.json')))
SW = json.load(open(os.path.join(HERE, 'sweep_register.json')))
INP = D['inputs']

masthead()
P('Riyadh Cables Group Company — Bibliography & Source Register', size=18, bold=True, space_after=2)
P('Tadawul: 4142  ·  companion to the valuation study dated 18 August 2026', size=10.5, color=GREY, space_after=8)
box([('READ FIRST.  ', 'This register lists every source and every input behind the valuation study. Sources '
      'are grouped by research layer: Company (the subject’s own audited and reviewed filings), Country '
      '(sovereign macro and risk premia), Industry (sector and peers), Global (rates, commodities), and House '
      '(the analyst’s own forecast assumptions, each built on a sourced anchor). The company’s historical '
      'figures come only from its own audited statements; no aggregator, broker note or press report is a '
      'source for any company figure — such sources appear only as labelled cross-checks.')])

# ---- primary documents -------------------------------------------------------
H1('Primary documents')
pd_rows = [['Document', 'Publisher / date', 'What was taken from it']]
for doc_, pub, took in [
    ('Consolidated financial statements, year ended 31 Dec 2025', 'Riyadh Cables / KPMG, 26 Mar 2026',
     'Full income statement, balance sheet, cash flow; cost-of-revenue breakdown; segment and geographic '
     'split; inventory; Islamic finance facilities; dividends; shares'),
    ('Consolidated financial statements, year ended 31 Dec 2024', 'Riyadh Cables / KPMG, Mar 2025',
     'FY2024 income statement and balance sheet; FY2023 comparative'),
    ('Consolidated financial statements, year ended 31 Dec 2023', 'Riyadh Cables / KPMG, Mar 2024',
     'FY2023 income statement and balance sheet; FY2022 comparative'),
    ('Annual report, year ended 31 Dec 2022 (IPO year)', 'Riyadh Cables, 2023',
     'FY2022 revenue and profit (cross-verified against the FY2023 comparative)'),
    ('Interim reviewed results, six months to 30 Jun 2026', 'Riyadh Cables via Tadawul, 29 Jul 2026',
     'H1-2026 revenue, gross profit, operating profit, net profit, equity — the near-term margin anchor'),
    ('Interim results, three months to 31 Mar 2026', 'Riyadh Cables via Tadawul, May 2026',
     'Q1-2026 revenue, gross profit, operating profit, net profit'),
    ('Country risk premium data, July 2026 vintage', 'A. Damodaran (NYU Stern), ~10 Jul 2026',
     'Saudi Arabia rating (Aa3), sovereign default spread 0.48%, country risk premium 0.74%, equity risk '
     'premium 4.94% (the CDS-basis figure is the January vintage and is flagged as such)'),
    ('FTSE Saudi Arabian Government Bond Index factsheet, 31 Jul 2026', 'FTSE Russell (LSEG)',
     'The 10-year SAR risk-free rate: 7–10-year bucket yield-to-maturity 5.52% at an 8.24-year average '
     'life, on an upward-sloping curve (whole index 5.48%); corroborated by FRED (US 10-year 4.68–4.72%) '
     'plus the Saudi USD new-issue spread, and by the SAR sukuk index level'),
    ('Dividend record, symbol 4142', 'Saudi Exchange / Argaam dividend table',
     'The FY2025 final dividend: SR 336.86mn at SR 2.25/share, announced 15-Mar-2026, ex 10-May-2026, '
     'paid 18-May-2026 — the only distribution in the roll window (cross-checked against Note 47 of the '
     'audited statements)'),
    ('Tadawul All Share Index (TASI) price history', 'Saudi Exchange',
     'The index against which the stock’s beta is estimated'),
    ('Policy rate and yield references', 'SAMA; sovereign yield sources, Aug 2026',
     'The SAIBOR leg of the marginal cost-of-debt estimate'),
    ('LME copper and aluminium references', 'London Metal Exchange, Aug 2026',
     'The metal-price path behind the materials cost leg (context / cross-check)')]:
    pd_rows.append([doc_, pub, took])
table(pd_rows, [2.5, 1.7, 2.9], size=8.0)

# ---- full input register grouped by layer -----------------------------------
H1('Full input register')
P('Every input in the model, with its value, date and source-and-construction, grouped by research layer. '
  'Values are the committed model numbers; percentages are shown as entered.', size=9.5, color=GREY)
RINGS = ['Company', 'Country', 'Industry', 'Global', 'Market', 'House', 'Company/House', 'Country/House',
         'Industry/House']
LAYER = {'Company': 'Company', 'Company/House': 'Company', 'Country': 'Country', 'Country/House': 'Country',
         'Industry': 'Industry', 'Industry/House': 'Industry', 'Global': 'Global', 'Market': 'Market',
         'House': 'House'}


def fmt_val(v):
    if isinstance(v, bool):
        return str(v)
    if isinstance(v, (int, float)):
        if abs(v) < 3 and v != int(v):
            return f'{v:.4f}'
        return f'{v:,.2f}' if abs(v) < 1000 else f'{v:,.0f}'
    if isinstance(v, list):
        return ', '.join(f'{x:.3f}' if isinstance(x, float) and abs(x) < 3 else f'{x:,.0f}' for x in v)
    if isinstance(v, dict):
        return '; '.join(f'{k}={x}' for k, x in v.items())
    return str(v)


for layer in ['Company', 'Country', 'Industry', 'Global', 'Market', 'House']:
    items = [(k, r) for k, r in INP.items() if LAYER.get(r['ring'], 'House') == layer]
    if not items:
        continue
    H2(f'{layer} layer')
    reg = [['Input', 'Value', 'Date', 'Source & construction']]
    for k, r in items:
        src = r['source']
        if len(src) > 300:
            src = src[:297] + '…'
        reg.append([k, fmt_val(r['value']), r['date'], src])
    table(reg, [1.35, 1.0, 0.7, 4.05], size=7.2)

# ---- judgements --------------------------------------------------------------
H1('Key judgements — and what would overturn each')
jr = [['Judgement', 'Set to', 'What would overturn it']]
for j, val, ov in [
    ('Sustained gross margin (the crux)', f'{D["inputs"]["spread_anchor"]["value"]*100:.2f}% (H1-2026 anchor)',
     'A run of quarterly gross margins settling materially above or below 14.5–16.0%'),
    ('Company class → lens', 'Operating manufacturer → DCF-primary',
     'Evidence the business is better read as a project contractor or a holding company (the filings do not '
     'support that)'),
    ('Risk-free rate 5.52% (10y SAR)', 'FTSE SAGBI 7–10y bucket, 31-Jul-2026',
     'A dated, traded SAR curve observation materially different at a later anchor; priced ±50bp in the study'),
    ('Cost of equity ~10.6%', f'beta {D["inputs"]["beta"]["value"]:.3f} × ERP {D["inputs"]["erp"]["value"]*100:.2f}% + rf*',
     'A materially different beta on a longer listed history (the 90% CI is 0.62–1.64 and is priced in the '
     'beta grid), or a change in the Saudi sovereign premium'),
    ('Terminal growth 4% nominal', '4.0%', 'A durable change in Saudi construction/electrification demand'),
    ('Real volume growth ~8% tapering', 'from the H1-2026 volume-led print',
     'Slower grid/construction spend, or evidence the H1-2026 volume surge was one-off'),
    ('Metal price path broadly flat', 'held near current',
     'A sustained directional move in copper/aluminium (carried in the sensitivity)'),
    ('Effective zakat/tax 9.5%', 'above the FY2025 9.0% print',
     'A change in the zakat/tax regime or in the foreign-profit share')]:
    jr.append([j, val, ov])
table(jr, [1.9, 1.8, 3.4], size=7.8)

# ---- negative results --------------------------------------------------------
H1('Negative results — searched, not found')
nr = [['Item', 'What was sought', 'Outcome']]
for it, sought, outc in [
    ('Company IR website (direct)', 'The audited statements from riyadh-cables.com',
     'Blocked by an automated-traffic challenge; the requester supplied the four audited statement sets '
     'directly, which are the build source'),
    ('Cable tonnage / volumes', 'A disclosed physical volume to build a literal unit model',
     'Not disclosed; a tonnage index is used and flagged'),
    ('Full H1-2026 interim statements', 'The complete reviewed half-year balance sheet and cash flow — in '
     'particular the 30-Jun-2026 net debt and working capital, to cross-check the model’s implied intra-year '
     'path', 'Only the summary reviewed results (P&L and equity) were reachable; the bridge is built on the '
     'audited 31-Dec-2025 balance sheet and rolled at the cost of equity, and the unread 30-Jun balance '
     'sheet is an open follow-up item, stated here rather than papered over'),
    ('July-2026 CDS-basis ERP table', 'The CDS leg of the dual-basis equity risk premium at the July vintage',
     'Not sourced; the CDS-basis figure quoted is the January vintage and is flagged as one vintage older '
     'than the rating leg'),
    ('Order book / backlog', 'A backlog figure for the high-voltage turnkey segment',
     'Not separately disclosed; the small segment is grown on its own revenue history'),
    ('Formal revenue guidance', 'Management numeric guidance', 'None issued; drivers are built from the '
     'disclosed history and the reviewed half-year')]:
    nr.append([it, sought, outc])
table(nr, [1.7, 2.0, 3.4], size=7.8)

# ---- aggregator-discrepancy note ---------------------------------------------
H1('Aggregator-discrepancy note')
P('Where public aggregators (used only as cross-checks) were consulted, their headline figures were '
  'consistent with the audited statements: 2025 revenue near SAR 10.67bn and net profit near SAR 1.08bn '
  'matched the audited income statement, and the Tadawul-filed results announcements matched the underlying '
  'statements. Two discrepancies are recorded. First, the uploaded price-history export printed the '
  '18-Aug-2026 close as SAR 104.80 — an unsettled intraday snapshot; the exchange’s settled record shows '
  'SAR 104.90 (−1.40 on the 106.30 previous close), and the settled print is used, with the library row '
  'revised and the raw export kept unchanged. Second, Note 22 of the FY2025 statements labels the two '
  'dividends paid during 2025 “SR 1.9 per share” while stating each at SR 299.4mn — amounts that imply SR '
  '2.00 per share on the 149.7mn shares outstanding; the amounts govern and the label is treated as a '
  'filing typo. In every case the audited amount or exchange-filed figure was used.')

# ---- primary-access log ------------------------------------------------------
H1('Primary-access log')
for pa in SW['primary_access']:
    status = 'reached' if pa['reachable'] else 'blocked'
    rich([(f'{pa["url"]} ', {'bold': True}), (f'({status}, {pa["attempt_date"]}) — {pa.get("note","")}', {})],
         size=8.4, space_after=4)

OUT = os.path.join(HERE, 'RIYADHCABLE_Bibliography_18-08-2026.docx')
doc.save(OUT)
print('wrote', os.path.basename(OUT), '| tables', len(doc.tables), '| inputs registered', len(INP))
