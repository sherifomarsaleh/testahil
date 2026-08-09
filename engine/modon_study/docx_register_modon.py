# -*- coding: utf-8 -*-
"""MODON_Bibliography_09-08-2026.docx — standalone bibliography: primary documents,
the FULL input register (every input, four fields), judgements with overturn
conditions, negative results, aggregator-discrepancy notes."""
import os, json
HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
exec(open(os.path.join(HERE, 'docx_base.py')).read())

INP = D['inputs']

masthead()
P('Modon Holding PSC — bibliography and input register', size=20, bold=True, space_after=2)
rich([('Companion to the 9 August 2026 valuation study · ADX: MODON', dict(color=GREY, size=10.5))],
     space_after=10)

H1('1 · Primary documents')
pd_rows = [['Document', 'Period', 'Retrieved from', 'Used for'],
 ['Audited consolidated financial statements, Modon Holding PSC (signed 18 Feb 2026)', 'FY2025 + FY2024 comparatives',
  'modon.com investor relations (fy-2025-adx.pdf)', 'all FY2025/FY2024 statement lines, notes 1–36'],
 ['Audited consolidated financial statements, Modon Holding PSC (scanned original)', 'FY2024',
  'modon.com investor relations', 'cross-check only (no text layer; figures from the FY2025 comparatives)'],
 ['Audited consolidated financial statements, Q Holding PSC', 'FY2023 + FY2022 comparatives',
  'modon.com investor relations', 'FY2023/FY2022 statement lines (predecessor perimeter)'],
 ['Interim condensed consolidated financial statements (reviewed)', 'H1-2026',
  'modon.com investor relations', 'study-year actuals; 31-Dec-2025 comparative cross-checks'],
 ['Annual Report 2025', 'FY2025',
  'modon.com investor relations', 'segment KPIs, masterplan disclosures, sales/units, backlog composition'],
 ['FY2025 results announcement (18 Feb 2026)', 'FY2025',
  'modon.com media centre', 'backlog AED 46.0bn, adjusted EBITDA, net-cash definition'],
 ['ADX disclosure portal copies of the above', 'various',
  'apigateway.adx.ae', 'availability confirmed; not needed as the company site served everything'],
 ['UAE MoF/CBUAE dirham treasury auction results (July 2026)', 'Jul-2026',
  'wam.ae (state news agency reporting the official auction)', 'AED sovereign yield 4.48% (Jan-2031 tranche)'],
 ['Damodaran country risk dataset (ctryprem), January 2026 update', 'Jan-2026',
  'pages.stern.nyu.edu', 'UAE Aa2 row: default spread 0.42%, ERP 4.87%; Egypt row for the stress case'],
 ['ADREC Abu Dhabi Real Estate Market Report 2025', '2025',
  'adrec.gov.ae / mediaoffice.abudhabi', 'market size, growth, off-plan share, foreign-buyer share'],
 ['Aldar Q4-FY25 results release · Emaar FY2025 release · Emaar Development FY2025 release', 'FY2025',
  'aldar.com / emaar.com', 'peer fundamentals (cross-check only)'],
 ['Turner & Townsend UAE Market Intelligence 2025; MEED/Currie & Brown 2026 outlooks', '2025-26',
  'public summaries', 'construction-cost escalator (~3-4.5%/yr)'],
 ['CBUAE EIBOR fixings (31 Mar 2026 set)', 'Mar-2026',
  'secondary mirrors (CBUAE page returned HTTP 403 at this session\'s network; logged)', '6M EIBOR 3.71%'],
 ['H1-2026 results announcement (29 Jul 2026)', 'H1-2026',
  'modon.com media centre (verified via official-release syndication)',
  'backlog 65.4bn/95% dev; H1 sales 26bn; net debt 912; unrestricted cash 8.6bn; adj. EBITDA 3.0bn; '
  '3,613 keys/16 hotels — the revision-2 restrike anchors'],
 ['Damodaran emerging-markets industry betas (betaemerg.xls, saved 07-Jan-2026)', 'Jan-2026',
  'pages.stern.nyu.edu', 'industry-beta cross-check (RE Development unlevered 0.45; rejected as '
  'primary, receipt in the study)'],
 ['Uploaded ADX daily price history for MODON (1,577 sessions, Dec-2017 – Aug-2026)', 'to 7 Aug 2026',
  'user-supplied export', 'price anchor, volatility model, technical read, beta regression '
  '(with the 18-name house panel as the proxy composite)']]
table(pd_rows, [2.9, 1.05, 1.6, 1.4], size=8.2)

H1('2 · Negative results — searched, not found')
neg = [['What was sought', 'Where', 'Outcome'],
 ['FTSE ADX General Index daily history (beta regressor)',
  'stooq (^adx); Yahoo Finance FADGI.FGI / FADX15.FGI / ^ADI; investing.com page + API; '
  'TradingEconomics chart API; WSJ/MarketWatch charting API; adx.ae + apigateway.adx.ae',
  'No downloadable series from any of seven sources. At revision 2 beta comes from a weekly '
  'regression of MODON against an equal-weight composite of the 18 house-library UAE names '
  '(3y beta 1.025, R² 0.37, n 155, gate PASS) — adopted 1.03, flagged as a proxy-index '
  'regression; the Damodaran industry route (0.45 unlevered) rejected as primary with receipt.'],
 ['UAE sovereign CDS spread (for a CDS-basis equity premium)',
  'Damodaran ctryprem, January 2026', 'Published as NA for the UAE — no CDS-basis cost of '
  'capital can be built; the rating basis stands alone.'],
 ['Quantified remaining-performance-obligation (backlog) table inside the audited statements',
  'FY2025 financial statements', 'Not disclosed at that level in the notes; the AED 46.0bn '
  'backlog and its 93% development share come from the results announcement and annual report.'],
 ['Per-project volumes and prices', 'annual report, results releases',
  'Disclosed only as totals (units and value by geography); the revenue build therefore stops '
  'at segment level with unit-level anchors, and says so.'],
 ['A dividend policy', 'FY2025 results release, annual report, statements',
  'None paid to owners in FY2024–25, none proposed — the zero in the model is sourced.'],
 ['Real-estate/events technology substitution risk', 'sector press 2025-26',
  'Nothing material found.'],
 ['Sanctions or supply-chain exposure relevant to the model', 'sector press 2025-26',
  'Nothing material found.']]
table(neg, [1.9, 2.35, 2.7], size=8.2)

H1('3 · Judgements — and what would overturn each')
jd = [['Judgement', 'Basis', 'What would overturn it'],
 ['Base sales path: post-H1 new sales AED 12bn (H2-26), then 30bn fading to 21bn/yr — '
  'every year below the 52bn annualised H1 pace',
  'H1-2026 ACTUAL sales of 26bn; ADREC structural demand; Modon share of Abu Dhabi residential',
  'two consecutive halves of new sales below AED 8bn, or an Abu Dhabi residential downturn'],
 ['Development margin glide 41% → 38%',
  'FY2025 43.7% and H1-2026 41.3% actuals; construction escalator vs price escalation',
  'arms-length land sales clearing below 20% gross margin; tender inflation >6%/yr sustained'],
 ['Working capital: component build absorbs through FY2028, releases only late',
  'receivable days 440 at both audited anchors; advances cover 1.86x and declining; '
  'land-bank draw vs new-WIP add — calibrated at 31-Dec-25 and 30-Jun-26',
  'FY2026 statements showing receivable days rising above ~470, or advances cover '
  'falling faster than assumed'],
 ['Tax at 15.5% (DMTT floor + foreign uplift)',
  'note 11 (DMTT charged from 2025); H1-2026 effective 15.4%',
  'a DMTT carve-out, or foreign profits growing beyond ~1/4 of the mix'],
 ['Beta 1.03 (own-stock regression vs the equal-weight 18-name panel proxy)',
  '3y weekly beta 1.025 (R² 0.37, n 155, usability gate PASS); 2y 1.055; 5y 1.071; '
  'industry route rejected as primary (receipt in the study)',
  'the official index becoming downloadable and its regression disagreeing materially '
  'with the proxy'],
 ['Terminal ROIC 8.5% — between the FY2025 clean 6.1% and the model\'s own forward path (~15%)',
  'at-cost land bank converting to recognised profit; deliberate mean-reversion below the path',
  'land monetisation stalling: at the clean achieved return the terminal value falls ~16% '
  'and the DCF ~11% (computed, not estimated)'],
 ['No conflict premium in the cost of equity (mid-2026 regional practice was +1pt)',
  'July-2026 AED sovereign auction at ~4bp over US Treasuries',
  'regional escalation reflected in the sovereign curve — re-add the point (strip shown)'],
 ['Lens weights 40/20/20/20',
  'contracted backlog justifies a DCF anchor; tight float keeps market lenses honest',
  'a float event or dividend policy would raise the market lenses\' weight']]
table(jd, [2.0, 2.45, 2.5], size=8.2)

H1('3b · Corrections adopted at revision 2 (external audits + re-audit)')
corr = [['Item', 'First edition', 'Revision 2', 'Why'],
 ['Development backlog driver', '42,600 (31-Dec-25)', '62,130 (30-Jun-26, 65.4bn × 95%)',
  'H1-2026 release superseded the anchor 11 days before publication'],
 ['FY2026 new development sales', '26,000 assumed for the full year',
  'AED 26bn H1 ACTUAL + 12bn H2 assumption', 'the assumption was already achieved in six months'],
 ['Bridge cash', 'gross 12,642 incl. ~4.0bn escrow', 'available 8,600 (disclosed)',
  'escrow funds completion of the backlog being valued — double-count'],
 ['Bridge date', '31-Dec-2025 rolled 219 days', '30-Jun-2026 rolled 38 days',
  'the balance sheet moved against the roll across that window'],
 ['Terminal debt weight', 'assumed 15%', 'derived from the model\'s own FY2030E (~8%)',
  'internal coherence'],
 ['Working capital', 'assumed release schedule', 'component build (days/cover/land-bank), '
  'absorbing through FY2028', 'H1 actuals show absorption while growth runs'],
 ['D&A driver', '4.2% of revenue', '3.4% on the average asset base', 'asset-base charge'],
 ['Beta', '1.0 assumed (tier-3)', '1.03 regressed vs panel proxy', 'evidence obtained'],
 ['Peer table', 'mixed bases/vintages; multiples irreconcilable',
  'one attributable basis, every multiple = printed numerator/denominator',
  'Aldar backlog was the 9M-2025 vintage; Emaar Dev backlog was the parent\'s figure; '
  'Emaar NP was disclosed, not n/d'],
 ['Relative lens', 'silent average of two legs 43% apart', 'P/E leg only; EV/EBITDA a '
  'labelled unanchored cross-check', 'method disagreement was hidden'],
 ['NCI in the bridge', 'book 847', 'capitalised max(book, 2% of equity value)',
  'consolidated premium implies NCI premium'],
 ['Expert 3 multiple', '6.5x called the "centre"', '6.2x = the stated mean',
  'the statistic now matches its label'],
 ['Expert 1 land mark-up', '35% called "half of 67%"', '33.7% = exactly half',
  'wording-number mismatch (self-found)'],
 ['Sensitivity grid', 'centre cell ≠ base case', 'rebuilt; centre = base', 'convention '
  'mismatch between grid and base'],
 ['Prose corrections', '"worth about AED 1/sh" (WC); "roughly halves" (terminal); '
  '"just below the resistance"; MACD at 2dp; conversion-direction caption',
  'each restated with the computed number', 'audit findings, all verified']]
table(corr, [1.35, 1.75, 1.95, 2.0], size=7.6)

H1('4 · Aggregator-discrepancy notes')
ag = [['Item', 'Primary figure', 'Aggregator figure', 'Resolution'],
 ['MODON trailing P/E', 'computed 11.78x (46,262/3,926, group profit basis)',
  'stockanalysis.com shows 11.33x (attributable basis)',
  'both stated; the study quotes its own computed basis and labels it'],
 ['FY2024 net profit', 'AED 9,389mn as reported (incl. AED 9,192mn bargain gain)',
  'some feeds show ~AED 197mn ("adjusted")',
  'both framings carried throughout (dual-framed)'],
 ['Shares outstanding', '16,347,080 thousand (note 23)', '16.35bn (rounded)',
  'note 23 figure used everywhere'],
 ['EIBOR', 'CBUAE official page unreachable (403) this session',
  'mirrors quote 3M 3.66% / 6M 3.71% (31-Mar-2026 set)',
  'mirror figures used, dated, and flagged as secondary']]
table(ag, [1.3, 2.15, 1.95, 1.55], size=8.2)

H1('5 · The full input register')
P(f'Every input the model consumes — {len(INP)} entries — with value, source and date, grouped by '
  'research layer. Values are AED million unless the label says otherwise.', size=9.5)

def fmt_val(v):
    if isinstance(v, (int, float)):
        if abs(v) < 3 and v != int(v):
            return f'{v:,.4f}'.rstrip('0').rstrip('.')
        return f'{v:,.3f}'.rstrip('0').rstrip('.')
    if isinstance(v, list):
        return ' · '.join(fmt_val(x) for x in v[:6])
    if isinstance(v, dict):
        return '; '.join(f'{k}: {fmt_val(x)}' for k, x in list(v.items())[:6])
    return str(v)

RINGS = ['Market', 'Company', 'Company/House', 'Country', 'Country/House', 'Industry', 'House']
by_ring = {r: [] for r in RINGS}
for k, v in INP.items():
    ring = v.get('ring', 'House')
    by_ring.setdefault(ring, []).append((k, v))
for ring in RINGS:
    entries = by_ring.get(ring, [])
    if not entries:
        continue
    H2(f'{ring} layer — {len(entries)} inputs')
    rows = [['Input', 'Value', 'Source', 'Date']]
    for k, v in entries:
        rows.append([k, fmt_val(v['value']), v['source'], v['date']])
    table(rows, [1.25, 1.15, 3.9, 0.75], size=7.2)

H1('Disclosure')
P('Companion to the Modon Holding valuation study of 9 August 2026. Educational analysis; not '
  'investment advice. © Testahil 2026.', size=9)

doc.save('MODON_Bibliography_09-08-2026.docx')
print('wrote MODON_Bibliography_09-08-2026.docx —', len(INP), 'inputs')
