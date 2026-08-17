"""AMR_Bibliography_09-08-2026.docx — the standalone sources document.

Every input in the study, with its value, its date, the layer it belongs to and the source and
construction behind it. Nothing is typed here: the register is read from study_numbers.json.
"""
import json, os
exec(open('docx_base.py').read())

SW = json.load(open('sweep_register.json'))
BETA = json.load(open('beta_result.json'))
PEERS = json.load(open('peers.json'))
M, I = D['meta'], D['inputs']
C, DFL = D['contested'], D['dual_framing_leases']

masthead()
P('Americana Restaurants International PLC', size=21, bold=True, space_after=0)
P('Sources and inputs — companion to the valuation study of 9 August 2026', size=12,
  color=BRASS, space_after=10)

box([('WHAT THIS DOCUMENT IS. ',
      'Every number in the valuation study, with where it came from. It exists so a reader can '
      'check any figure without taking the study\'s word for it, and so that the line between '
      'what the company reported and what this study assumed is visible rather than implied.'),
     ('THE RULE THIS STUDY FOLLOWS. ',
      'Everything Americana itself reports — every income-statement, balance-sheet, cash-flow, '
      'segment and note figure — is taken only from the company\'s own audited consolidated '
      'financial statements, its reviewed interim statements and its own investor materials. No '
      'data vendor, broker note or news report is used as a source for any of it. Outside '
      'sources appear for market prices, sovereign risk premiums and peer multiples, and each '
      'is labelled where it is used.')])

# ---------------------------------------------------------------- primary documents
H1('1  Primary documents')
P('All of the following were obtained from the company\'s own investor-relations library at '
  'americanarestaurants.com and read directly. Page and note references appear against '
  'individual inputs in section 3.')
DOCS = [
    ('Audited consolidated financial statements, year ended 31 December 2025',
     'Deloitte & Touche (M.E.) LLP, signed 6 February 2026', 'audited', '2026-02-06'),
    ('Audited consolidated financial statements, year ended 31 December 2024',
     'Deloitte & Touche (M.E.) LLP', 'audited', '2025-02-11'),
    ('Audited consolidated financial statements, year ended 31 December 2023',
     'includes the audited FY2022 comparative column', 'audited', '2024-02-15'),
    ('Reviewed condensed consolidated interim statements, six months ended 30 June 2026',
     'review report by Deloitte & Touche (M.E.) LLP dated 28 July 2026', 'reviewed', '2026-07-28'),
    ('Reviewed condensed consolidated interim statements, three months ended 31 March 2026',
     'the first disclosed quarter of the study year', 'reviewed', '2026-04-28'),
    ('FY 2025 earnings presentation', 'restaurant count by country and brand, cost of inventory '
     'evolution, capital expenditure by brand, dividend declaration', 'investor relations',
     '2026-02-09'),
    ('H1 2026 earnings presentation', 'restaurant count by country and brand, four-wall EBITDA, '
     'net working capital, channel mix, free-cash-flow bridge, capital expenditure and payback '
     'per restaurant', 'investor relations', '2026-07-28'),
    ('H1 2026 earnings press release', 'guidance for 2026, interim dividend, like-for-like growth',
     'investor relations', '2026-07-28'),
    ('FY 2024 earnings presentation', 'restaurant count by country at 31 December 2024, and the '
     'jurisdiction-by-jurisdiction corporate tax table', 'investor relations', '2025-02-13'),
    ('Integrated annual report 2025', 'narrative, strategy and headcount context',
     'annual report', '2026-03-17'),
    ('FY 2023 earnings release', 'the disclosed 2,435 restaurant count at 31 December 2023 and '
     'the 300 gross / 252 net openings of that year', 'investor relations', '2024-02-15'),
]
table([['Document', 'What it carries', 'Status', 'Date']] +
      [[a, b, c, d] for a, b, c, d in DOCS], [2.55, 2.65, 1.00, 0.80], size=8.8)

P('Two further access attempts are recorded for completeness. The Abu Dhabi Securities Exchange '
  'company page returned an automated-access refusal to this environment; it was not needed, '
  'because every document the exchange would carry is published by the company itself. A daily '
  'history for the Abu Dhabi general index was sought from the machine-readable sources '
  'available — the Yahoo index quote returns one observation and no history, and the main '
  'data portals refused automated access — and not obtained; the consequence for the beta, '
  'and its sizing, is in section 1.8 of the study.')

# ---------------------------------------------------------------- outside sources
H1('2  Outside sources, and what each is used for')
OUT = [
    ('Aswath Damodaran, NYU Stern — country default spreads and risk premiums, July 2026 '
     'edition (published 15 July 2026)', 'read from the original data file',
     'the equity risk premium for each of the twelve operating countries, on both the ratings '
     'and the credit-default-swap basis', 'cost of capital only'),
    ('US Treasury daily par yield curve', 'close of 7 August 2026, read from the Treasury CSV',
     'the risk-free rate', 'cost of capital only'),
    ('IMF World Economic Outlook, retrieved 9 August 2026',
     'through the IMF DataMapper interface',
     'inflation and real growth for each operating country, which set the currency drag and '
     'anchor terminal growth', 'forecast drivers only'),
    ('Abu Dhabi sovereign US dollar issue, February 2026', 'final re-offer spread of 25 basis '
     'points over Treasuries on the ten-year tranche (price thoughts opened at 55)',
     'a cross-check that the company\'s own borrowing rate sits above its sovereign',
     'cross-check only'),
    ('Peer market data, retrieved 9 August 2026', 'trailing figures as published',
     'the peer multiple table', 'cross-check only — no peer figure enters the valuation'),
    ('FTSE ADX General Index daily history',
     'screened before use; history to ' + str(BETA['index_asof']),
     'the regressor in the beta calculation — the published index of the exchange the shares '
     'trade on, held at ' + BETA['index_file'].replace('/', ' / '),
     'cost of capital only'),
    ('Tadawul All Share Index daily history', 'retrieved 9 August 2026',
     'a disclosed beta cross-check, and the regressor this study\'s first edition used before '
     'the Abu Dhabi index history was available', 'cross-check only'),
]
table([['Source', 'Form', 'What it supplies', 'Scope']] +
      [[a, b, c, d] for a, b, c, d in OUT], [2.25, 1.55, 2.35, 0.85], size=8.6)

P('No outside source supplies any figure Americana itself reports. The distinction matters: a '
  'sovereign risk premium is not something the company can tell us, and a peer\'s multiple is '
  'not something we would take from the company anyway.')

# ---------------------------------------------------------------- the input register
doc.add_page_break()
H1('3  Every input in the study')
P('Grouped by research layer. Company figures are the company\'s own reported numbers; country '
  'and industry figures are external and named; house estimates are this study\'s own judgements '
  'and are marked as such, with the reasoning shown.')

LAYERS = ['Company', 'Company (investor relations)', 'Market', 'Country', 'Industry',
          'House estimate']
LAYER_NOTE = {
    'Company': 'Read from the audited consolidated financial statements or the reviewed interim '
               'statements.',
    'Company (investor relations)': 'Read from the company\'s own earnings presentations and '
                                    'releases — operating data that appears in no financial '
                                    'statement.',
    'Market': 'Traded prices and figures derived from them.',
    'Country': 'External, sourced and dated; used only in the cost of capital and the macro '
               'drivers.',
    'Industry': 'External, used as a cross-check.',
    'House estimate': 'This study\'s own judgement. Each one states its reasoning and what it '
                      'rests on.',
}


def fmt_val(v):
    if isinstance(v, bool):
        return str(v)
    if isinstance(v, (int, float)):
        if abs(v) < 1 and v != 0:
            return f'{v:.5g}'
        return f'{v:,.4g}'
    if isinstance(v, list):
        return ', '.join(fmt_val(x) for x in v[:6])
    if isinstance(v, dict):
        out = '; '.join(f'{k} {fmt_val(x)}' for k, x in list(v.items())[:4])
        return out[:100] + ' …' if len(out) > 100 else out
    return str(v)


total = 0
for layer in LAYERS:
    items = [(k, v) for k, v in I.items() if v['layer'] == layer]
    if not items:
        continue
    H2(f'3.{LAYERS.index(layer)+1}  {layer}  ({len(items)} inputs)')
    P(LAYER_NOTE[layer], size=9.5, italic=True, color=GREY, space_after=4)
    rows = [['Input', 'Value', 'Date', 'Source and construction']]
    for k, v in items:
        rows.append([k.replace('_', ' '), fmt_val(v['value']), v['date'], v['source']])
    table(rows, [1.35, 0.95, 0.72, 3.98], size=7.2)
    total += len(items)
P(f'{total} inputs in total. Every one carries a value, a source, a date and a layer; the build '
  'refuses to run if any of the four is missing.', size=9.5, italic=True, color=GREY)

# ---------------------------------------------------------------- judgements
doc.add_page_break()
H1('4  Judgements, and what would overturn each one')
P('These are the places where this study exercised judgement rather than read a number. Each is '
  'stated with the evidence behind it and the observation that would prove it wrong.')
J = [
    ('The margin gain is structural (the base case), and the cyclical reading is published '
     'beside it',
     'The company names procurement scale, menu optimisation and improving delivery economics, '
     'and the cost of food and packaging has fallen for four consecutive quarters. The same '
     'evidence is consistent with a favourable turn in traded food prices.',
     'Food and packaging cost back above 29% of revenue for two consecutive quarters. The '
     'study does not resolve this — it computes both readings, '
     f'AED {C["way_a"]["value_aed"]:.2f} against AED {C["way_b"]["value_aed"]:.2f}.'),
    ('Leases are treated as debt, with right-of-use additions charged as investment',
     'It is how the accounts present them, and it is internally consistent as long as taking a '
     'lease is charged as investment rather than only depreciated.',
     f'Nothing much — this was computed both ways and the answer moves by '
     f'{abs(DFL["gap_pct"])*100:.1f}%. The judgement turns out not to matter, which is itself '
     'worth knowing.'),
    ('Beta of ' + f'{D["wacc"]["beta"]:.3f}' + ', from the company\'s own shares against the '
     'FTSE ADX General Index',
     f'{BETA["n"]} weekly observations over {BETA["window_years"]} years — the whole life of '
     f'the listing — standard error {BETA["se"]:.3f}, R-squared {100*BETA["r2"]:.1f}%, '
     'lead-lag corrected, both series screened for data quality first. The regressor is the '
     f'published index of the exchange the shares trade on ({BETA["index_file"]}, history to '
     f'{BETA["index_asof"]}), in the same currency and struck at the same closing auction.',
     'Almost anything, and that is the point: the 90% confidence interval runs from '
     f'{BETA["ci90"][0]:.2f} to {BETA["ci90"][1]:.2f}. Three earlier estimates are on the '
     'record and none is used — the Riyadh line against the Saudi index 0.894 (a different '
     'country\'s market cycle, and this study\'s first published input, before the Abu Dhabi '
     'index was available), a basket of eighteen covered UAE names 0.586, and a US-listed UAE '
     'index fund pricing hours after the Abu Dhabi close 0.469.'),
    ('Cost of debt of ' + f'{100*D["wacc"]["kd"]:.2f}%, the company\'s own lease borrowing rate',
     'The company has no bank debt. Its lease finance cost over its average lease liability is '
     'the only borrowing rate it actually pays, and determining that rate is a key audit matter '
     'in the filing.',
     'A bond or bank facility priced away from this level. The 2024 accounts give '
     f'{100*D["wacc"]["kd_fy24"]:.2f}% on the same construction, so the figure is stable.'),
    ('Terminal growth of ' + f'{100*D["wacc"]["terminal_g"]:.1f}% in US dollars',
     'The IMF projects about 2% long-run inflation in the pegged Gulf markets that produce most '
     'of the revenue; a mature estate can add roughly a point of real volume. The figure is set '
     'well below the risk-free rate, which is the ceiling any perpetual growth rate must respect.',
     'Nothing observable in the short run. It is sensitised from 2.0% to 4.0% in the study, a '
     'range worth about ' +
     f'{abs(D["sensitivity"]["single"]["Terminal growth (2.0% / 2.5% / 3.0% / 3.5% / 4.0%)"][4] - D["sensitivity"]["single"]["Terminal growth (2.0% / 2.5% / 3.0% / 3.5% / 4.0%)"][0]) * M["fx"]:.2f}'
     ' dirhams a share.'),
    ('Effective tax rate rising from 14.5% to 16.0%',
     'The rate went 4% to 11% to 14% over three years as the United Arab Emirates introduced '
     'corporate tax and the first domestic minimum top-up taxes landed; the first half of 2026 '
     'ran at 14.1%. The company publishes the jurisdiction-by-jurisdiction position.',
     'The remaining jurisdictions not adopting the minimum, or the group securing reliefs. Worth '
     'about 1.8% of value per two points of tax.'),
    ('Net new restaurants of 125 in 2026, then a taper to 120',
     'The 2026 figure is the midpoint of the company\'s own published guidance of 120 to 130. '
     'The taper reflects a maturing estate.',
     'Openings running materially above or below guidance. A 20% change in the programme is '
     'worth about 2.2% of value.'),
    ('The allocation of new restaurants across markets',
     'The company guides the total but does not publish the split. The allocation follows where '
     'the estate has grown over the last eighteen months.',
     'A published country split that differs. This is the one estimate inside the revenue build, '
     'and the group result is insensitive to it because growth rates differ across markets by '
     'more than revenue per restaurant does.'),
    ('Lens weights of 50 / 20 / 20 / 10',
     'The cash-flow lens carries most because the estate is knowable restaurant by restaurant '
     'and the company publishes the store-level economics. The book lens carries least because '
     'an operator that leases its estate holds almost no book equity.',
     'Nothing observable. The weights are stated so a reader who disagrees can re-weight: every '
     'lens value is published separately.'),
]
rows = [['The judgement', 'What it rests on', 'What would overturn it']]
for a, b, c_ in J:
    rows.append([a, b, c_])
table(rows, [1.85, 2.60, 2.55], size=8.2)

# ---------------------------------------------------------------- negative results
H1('5  What was looked for and not found')
P('A source list that only records what was located is misleading. These categories were '
  'searched and returned nothing that would change a number.')
rows = [['Category', 'What was searched', 'Date']]
for f in SW['findings']:
    if f['klass'] == 'NEG':
        rows.append([f['category'], f['headline'].replace('Negative search — nothing found (', '')
                    .rstrip(')'), f['source_date']])
table(rows, [1.55, 4.75, 0.70], size=8.4)

H1('6  Discrepancies between sources, and how they were resolved')
DISC = [
    ('Restaurant count at 31 December 2025: 2,749 in the presentation appendix against 2,709 in '
     'the portfolio-evolution chart on the same page',
     'The two are both correct and measure different things: 2,709 is the organic estate and '
     '2,749 includes the 40 net restaurants that arrived with the Pizza Hut Oman acquisition. '
     'The study uses 2,749, which is the estate that generates revenue, and builds the forecast '
     'on the organic guidance so the acquisition is not double-counted.'),
    ('Net working capital: the company reports USD (248) million; a narrow definition of trade '
     'payables alone gives USD (180) million',
     'The company\'s own aggregate — inventories plus receivables less payables, tax payable and '
     'provisions — is the one used, because it reconciles exactly to the published figure and to '
     'the published ratio of revenue. The narrower definition is not wrong, it is a different '
     'measure.'),
    ('Gross capital expenditure: USD 125.2 million in the presentation against USD 108.8 million '
     'in the cash-flow statement',
     'The presentation figure includes the consideration paid for the Pizza Hut Oman subsidiary '
     'and initial franchisor fees. The study uses the cash-flow statement figure for the '
     'historical record and builds the forecast from restaurant economics, so the acquisition is '
     'handled separately rather than embedded in a capital-expenditure ratio.'),
    ('EBITDA: the company publishes USD 595.6 million for FY2025 and does not define it in the '
     'financial statements',
     'The definition was reconstructed from the company\'s own reconciliation — operating profit '
     'plus depreciation and amortisation plus impairments on non-financial and financial assets '
     '— and it reproduces the published figure to the nearest thousand dollars in FY2025 and in '
     'both halves of 2026. That reconstruction, not the published headline, is what the model '
     'uses, so the same definition applies to every forecast year.'),
    ('Peer multiples: one regional comparator screens at over 100 times EBITDA',
     'That name is running a 2.6% EBITDA margin on a depressed year, so its multiple is '
     'arithmetic rather than information. It is shown in the peer table for completeness and '
     'excluded from the median, along with any comparator outside a 4-to-40-times band. The '
     'exclusion rule is stated rather than applied silently.'),
]
rows = [['The discrepancy', 'How it was resolved']]
for a, b in DISC:
    rows.append([a, b])
table(rows, [2.60, 4.40], size=8.4)

H1('7  A note on what this study could not obtain')
P('Two things were wanted and not obtained, and both are recorded in the study itself rather '
  'than left to be discovered.')
P('First, a daily history for the Abu Dhabi general index. It was sought from several '
  'machine-readable sources and none served a timeseries. The consequence is that the beta '
  'regression runs against the index of the company\'s other home market rather than its primary '
  'one. Both currencies are pegged to the dollar and both markets list the same shares, and two '
  'independent cross-checks come out lower than the adopted figure, so the effect is to make the '
  'cost of equity slightly more conservative rather than less.')
P('Second, a country-level split of the company\'s restaurant-opening guidance. It is not '
  'published at that level. The study allocates the guided total across markets on where the '
  'estate has actually been growing, and flags that allocation as an estimate.')

OUT = 'AMR_Bibliography_09-08-2026.docx'
doc.save(OUT)
print('wrote', OUT)
