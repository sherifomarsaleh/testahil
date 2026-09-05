"""Content part C: Appendices A–D, About, Disclosure, footer."""
from docx_stc_base import *
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
# Absolute against this file's own directory: the builders read and wrote relative
# to the working directory, so running them from the repository root — which is how
# every gate does — found no inputs and scattered the outputs.


L = D['lenses']; E = D['experts']; dcf = D['dcf']; ddm = D['ddm']
# `s0` was the retired skill backtest and nothing in this part ever read it.
spot = D['spot']; hist = D['hist']; fc = D['forecast']

# ================= Appendix A ================================================
H1('Appendix A  Financial statements')
P('Consolidated figures as disclosed by stc — FY2023–FY2025 IR releases on the restated continuing-operations basis '
  '(TAWAL and Digital Infrastructure Co reclassified to discontinued operations), Q1-2026 release and interim FS — all '
  'from stc.com, per the study’s sourcing rule. SAR million. The five-year forecast is the model build (companion Excel, '
  'formula-linked to Assumptions).')
H2('A.1  Income statement — 3-year historical + 5-year forecast (consolidated, SAR mn)')
def f0(x): return f"{x:,.0f}"


def fp(x):
    """A deduction, printed as the statements print it — in brackets, positive magnitude."""
    return f"({abs(x):,.0f})"


# EVERY FIGURE BELOW IS READ, NOT RECOMPUTED. This appendix used to run a SHADOW MODEL
# inside the document builder: it rebuilt EBITDA from a margin, then set other income to a
# typed [700, 750, 800, 850, 900], zakat to a typed 9.7% and the minority to a typed 2.5%,
# and printed the result as the study's income statement. None of those three came from the
# model, so the appendix and the valuation could disagree and nothing would say so.
_ISH = json.load(open(os.path.join(HERE, 'income_statement.json')))
_GP_HIST = [D['hist']['gp'][k] * 1000.0 for k in ('FY23', 'FY24', 'FY25')]
_H = _ISH['lines']
_FY = ['FY26E', 'FY27E', 'FY28E', 'FY29E', 'FY30E']
rows = [
 ['Line', 'FY23', 'FY24', 'FY25'] + _FY,
 ['Revenue'] + [f0(v) / 1 if False else f0(v / 1000.0) for v in _ISH['lines']['Total revenues']]
   + [f0(fc[y]['rev']) for y in _FY],
 ['Gross profit'] + [f0(v / 1000.0) for v in _GP_HIST] + [f0(fc[y]['gp']) for y in _FY],
 ['EBITDA'] + [f0(v / 1000.0) for v in _ISH['ebitda']] + [f0(fc[y]['ebitda']) for y in _FY],
 ['Depreciation, amortisation and impairment']
   + [fp(v / 1000.0) for v in _H['Depreciation, amortisation and impairment']]
   + [fp(fc[y]['dna']) for y in _FY],
 ['Operating profit (EBIT)'] + [f0(v / 1000.0) for v in _ISH['ebit']]
   + [f0(fc[y]['ebit']) for y in _FY],
 ['Cost of the early retirement programme']
   + [fp(v / 1000.0) for v in _H['Cost of the early retirement programme']]
   + [fp(fc[y]['early_retirement']) for y in _FY],
 ['Finance income'] + [f0(v / 1000.0) for v in _H['Finance income']]
   + [f0(fc[y]['fin_income']) for y in _FY],
 ['Finance cost'] + [fp(v / 1000.0) for v in _H['Finance cost']]
   + [fp(fc[y]['fin_cost']) for y in _FY],
 ['Other income, associates and other gains']
   + [f0((_H['Net other income and expenses'][i]
          + _H['Net share in associates and joint ventures'][i]
          + _H['Net other gains'][i]) / 1000.0) for i in range(3)]
   + ['not forecast'] * 5,
 ['Profit before zakat and income tax'] + [f0(v / 1000.0) for v in _ISH['profit_before_zakat']]
   + [f0(fc[y]['pbz']) for y in _FY],
 ['Zakat and income tax'] + [(fp(v / 1000.0) if v < 0 else f0(v / 1000.0))
                             for v in _H['Zakat and income tax']]
   + [fp(fc[y]['zakat']) for y in _FY],
 ['Profit from continuing operations'] + [f0(v / 1000.0) for v in _ISH['net_profit_continuing']]
   + [f0(fc[y]['net_profit']) for y in _FY],
]
table(rows, [2.05, 0.615, 0.615, 0.615, 0.615, 0.615, 0.615, 0.615, 0.615],
      first_col_bold=True, size=8.2)
caption('The three filed years are note 9\'s own reconciliation of segment revenue to profit '
        'from continuing operations, and they foot to the riyal in every column. THREE LINES '
        'ARE NOT FORECAST AND THE TABLE SAYS SO RATHER THAN LEAVING A READER TO NOTICE: net '
        'other income, the share of associates and net other gains have no disclosed driver '
        'between them and were worth %s million in FY2025 alone, so the projected profit is '
        'BELOW what the same company would report if they recurred. Zakat is the rate the '
        'three years imply on profit before zakat, %.2f per cent, with the reversal of prior '
        'years\' provision that note 33(a) names put back — carrying that reversal forward '
        'would read %.2f per cent and assume the company keeps finding it has over-provided.'
        % (f0((_H['Net other income and expenses'][2]
               + _H['Net share in associates and joint ventures'][2]
               + _H['Net other gains'][2]) / 1000.0),
           100 * _ISH['effective_zakat_rate'],
           100 * _ISH['zakat_rate_carrying_the_reversal']))

H2('A.2  Balance sheet — the filed years, and why there is no forecast column')
_BSJ = json.load(open(os.path.join(HERE, 'balance_sheet.json')))
rows = [
 ['Line', 'FY23', 'FY24', 'FY25'],
 ['Total assets'] + [f0(D['hist']['assets'][k]) for k in ('FY23', 'FY24', 'FY25')],
 ['Cash and equivalents'] + [f0(D['hist']['cash'][k]) for k in ('FY23', 'FY24', 'FY25')],
 ['Borrowings'] + [fp(D['hist']['debt'][k]) for k in ('FY23', 'FY24', 'FY25')],
 ['Equity attributable to the parent']
   + [f0(D['hist']['eq_att'][k]) for k in ('FY23', 'FY24', 'FY25')],
 ['Non-controlling interests'] + [f0(D['hist']['nci'][k]) for k in ('FY23', 'FY24', 'FY25')],
]
table(rows, [3.2, 0.95, 0.95, 0.95], first_col_bold=True, size=8.4)
caption('THERE IS NO FORECAST BALANCE SHEET IN THIS EDITION AND THE REASON IS A DEFECT IN '
        'THE FILING RATHER THAN A GAP IN THE MODEL. The latest reviewed balance sheet does '
        'not add up in its own current column — four subtotals and both totals — while every '
        'prior-year column foots exactly. That was not assumed to be an extraction problem: '
        'the file was re-fetched from the company\'s own site, re-extracted, and re-read by '
        'optical character recognition off the page rendered at 300 dots per inch, and both '
        'routes return the same figures. A statement is used only if it foots against its '
        'own arithmetic, and solving for the six figures that would make it foot would be '
        'inventing them. The lines this study\'s valuation does use are corroborated instead '
        'by the same interim\'s CASH FLOW statement, to the riyal. The previous edition '
        'printed a forecast balance sheet whose gaps were filled with grouped estimates '
        'chosen to make a balance-check row read zero; a check that cannot fail is not a '
        'check, and it is not reprinted here.')

H2('A.3  Cash flow, the two free-cash-flow framings, and the dividend schedule')
rows = [
 ['Cash flow (SAR mn)', 'FY23', 'FY24', 'FY25', 'FY26E', 'FY28E', 'FY30E'],
 ['Operating cash flow (disclosed / model)', '22,418', '19,885', '18,283', '23,647', '26,155', '28,441'],
 ['Capex (disclosed / model)', '(9,790)', '(11,927)', '(11,795)', '(13,359)', '(14,000)', '(14,006)'],
 ['Free cash flow', '12,628', '7,959', '6,488', '10,287', '12,156', '14,435'],
 ['Dividends paid (attributable)', '(8,000)', '(18,712)', '(10,978)', '(10,978)', '(11,477)', '(12,724)'],
]
table(rows, [2.5, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75], first_col_bold=True, size=8.5)
caption('FY23–FY25 disclosed (stc IR); FY24 dividends-paid include the FY24 quarterly schedule; calendar-2025 cash dividends '
        '≈ SAR 20.9 bn including the SAR 2.00/share special. Model OCF is a NOPAT-based construct and runs richer than the '
        'disclosed series — the conversion gap (receivables, ERP cash, zakat timing) is modelled as an explicit drag and '
        'discussed in §1.1; both framings shown per house rule.')
rows = [
 ['Dividend schedule', 'FY25A', 'FY26E', 'FY27E', 'FY28E', 'FY29E', 'FY30E'],
 ['DPS declared (SAR)', '2.20', '2.20', '2.20', '2.30', '2.40', '2.55'],
 ['Dividend bill (SAR bn)', '11.0', '11.0', '11.0', '11.5', '12.0', '12.7'],
 ['Payout of attributable NP', '74%', '78%', '75%', '75%', '74%', '74%'],
 ['Yield at spot (declared)', '5.0%', '5.0%', '5.0%', '5.3%', '5.5%', '5.9%'],
 # THE STRESS CHECK QUOTED MANAGEMENT'S GUIDANCE BAND AND A COVER FIGURE FROM IT. The
 # model spans the three filed years instead — guidance is scored, never consumed — and on
 # that range the dividend is covered throughout, which is a different and better-evidenced
 # statement than the one this cell was making.
 ['Stress check',
  'At the heaviest capital spending of the three filed years the dividend is %.2fx covered by model free cash flow '
  'in the first forecast year, and at the lightest %.2fx — covered throughout the range this company has actually '
  'operated in. The question the cover table asks is whether the data-centre build takes intensity ABOVE anything '
  'it has yet run; the core cash pile funds a shortfall for years before leverage becomes a constraint.'
  % (D['cover'][-1]['cover'], D['cover'][0]['cover']), '', '', '', '', ''],
]
table(rows, [1.9, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85], first_col_bold=True, size=8.6)
caption('Two yield framings (house rule): declared-regular 2.20/sh = 5.0%; cash paid during calendar-2025 incl. the FY24 '
        'special = 4.20/sh = 9.6%. A forecast-versus-actual scorecard and a new-versus-old reconciliation: not '
        'applicable on an initiation; both become standing sections from the first 3-month update.')

# ================= Appendix B ================================================
H1('Appendix B  Peer frame, risk register, and the research register')
H2('B.1  The peer frame and the sector')
P('stc is the premium name in a three-player Saudi market inside a GCC cohort where telecom equity is increasingly a '
  'yield-plus-digital-infrastructure asset class.')
rows = [
 ['Name', 'P/E (t)', 'Div yield', 'One-line profile'],
 ['stc (7010)', '~14.7×', '5.0% (9.6% incl. special)', 'Incumbent; ~57% mobile share; net debt ~0; AI-DC and fintech options'],
 ['Mobily (7020)', '~13.5×', '4.5%', 'No.2; e& anchor (~28%); fastest subscriber momentum'],
 ['Zain KSA (7030)', '~12.8×', '4.9%', 'No.3; tower-light; balance-sheet repair done'],
 ['e& (UAE)', '~13.2×', '5.1%', 'UAE incumbent + Vodafone/PPF international portfolio'],
 ['Ooredoo (Qatar)', '~10.7×', '5.7%', 'Multi-market; MENA data-centre pivot'],
 ['du (UAE)', '~17.6×', '5.5%', 'No.2 UAE; hyperscale data-centre momentum — the multiple stc’s DC build aspires to'],
 ['Omantel / Beyon / Telecom Egypt', '11.5× / 11.1× / 8.8×', '3.9% / 7.1% / 1.5%', 'Regional context'],
]
table(rows, [1.55, 1.05, 1.35, 3.05], first_col_bold=True, size=8.7)
caption('Multiples approximate, mixed as-of dates (May–Jul 2026), secondary aggregators — context only, never model inputs.')
P('Sector structure. Saudi mobile is a disciplined three-player market (~57/27/16 stc/Mobily/Zain) under CST regulation, '
  'with spectrum freshly allocated (Nov-2024 auction: stc took 600 MHz + 3.8 GHz), 5G at 63% populated coverage for stc '
  'and FWA adoption among the highest globally — FWA is both an opportunity (4.1 mn of stc’s 6.0 mn fixed lines) and the '
  'competitive vector through which mobile capacity attacks fixed pricing. Fibre stays an stc moat (3.75 mn FTTH, 258k km). '
  'The Kingdom’s AI push (HUMAIN, sovereign compute, the center3 1 GW ambition) is turning telecom capex into a national-'
  'strategy line item. Principal risks: a mobile price war; capex overshoot on the AI build; government-receivables '
  'cycles; subsidiary execution (stc bank credit costs as it scales); the Telefónica mark; regional geopolitics; and the '
  'rate path staying higher for longer.')

H2('B.2  Risk register')
rows = [['Risk', 'How it would show up first', 'What it is worth']]
for r, sig, w in [
 ('A price war in Saudi mobile', 'Consumer revenue per subscriber, before it reaches the margin',
  'The single largest downside: this model assumes NO margin improvement, so a price war breaks it downward from a '
  'path that has nothing built in to give back'),
 ('Capital expenditure overshoot on the data-centre build', 'Capital intensity against the three filed years (1.05x to 1.25x depreciation)',
  f"The bear-to-bull span of the central: SAR {D['central_range']['low']:.2f} to the cash-flow bull"),
 ('Government receivables cycles', 'Operating cash conversion, not the income statement',
  'A cash-flow timing risk rather than a value risk, unless it persists'),
 ('Subsidiary execution as the portfolio scales', 'Contribution turning positive on the guided schedule, or not',
  'The flat margin carried to the terminal depends on it'),
 ('The rate path staying higher for longer', 'The discount rate directly',
  f"{D['dcf']['tv_pct']*100:.0f}% of enterprise value sits beyond year five"),
 ('The overseas listed stake', 'A mark that moves daily and is carried at market',
  'A few per cent of the bridge; disclosed, not modelled'),
]:
    rows.append([r, sig, w])
table(rows, [1.9, 2.3, 1.9], first_col_bold=True, size=8.5)

H2('B.3  The research register — what was searched, and what came back empty')
# THE MODEL SKELETON CARRIES A B.3 AND THIS STUDY HAD NO APPENDIX B SUBSECTIONS AT ALL.
# The register existed on disk the whole time; the document simply never showed it, so a
# reader could not see how much of this study rests on the company's own filings, nor
# which questions were asked and answered with nothing.
_SW = json.load(open(os.path.join(HERE, 'sweep_register.json')))
_F = _SW['findings']
_rings = ['GLOBAL', 'COUNTRY', 'INDUSTRY', 'COMPANY']
P('Before any forecast driver was set, the research ran in four rings — the world, the country, the industry, and the '
  'company — and every finding was recorded with its source and that source\u2019s own date. The table below is that '
  'register in summary; the standalone bibliography carries every line of it, together with the full register of the '
  f"{len(D['inputs'])} inputs this study consumes, each with its value, its source and its date.", size=9.8)
rows = [['Ring', 'Findings', 'Of which searches that came back empty', 'The sources they rest on']]
for rg in _rings:
    inring = [f for f in _F if f['ring'] == rg]
    negs = [f for f in inring if f['klass'] == 'NEGATIVE_SEARCH']
    srcs = sorted({f['source_type'].replace('_', ' ').lower() for f in inring})
    rows.append([rg.capitalize(), str(len(inring)), str(len(negs)), ', '.join(srcs)])
_negall = [f for f in _F if f['klass'] == 'NEGATIVE_SEARCH']
rows.append(['All four', str(len(_F)), str(len(_negall)),
             'sweep dated %s' % _SW['sweep_date']])
table(rows, [1.15, 0.85, 1.9, 2.2], first_col_bold=True, size=8.5, band_rows=[len(_rings) + 1])
P('A NEGATIVE RESULT IS A RESULT, and this study records four of them. They are printed here rather than left out, '
  'because a question asked and answered with nothing is evidence, while a question never asked looks identical to one '
  'that found nothing:', size=9.8)
# THE HEAD IS THE QUESTION THAT WAS ASKED, NOT THE ANSWER. A first pass took the head off
# the front of the headline, which for these findings is the phrase "Negative search" — so
# every bullet read "Negative search. Negative search — nothing found (...)". What a reader
# needs is which question came back empty, and that is the category the search was run in.
for f in _negall:
    _body = f['headline']
    if '(' in _body:
        _body = _body[_body.index('(') + 1:].rstrip(')')
    bullet(_body.strip(), bold_head='%s ring — %s. ' % (f['ring'].capitalize(), f['category']))
_pa = _SW['primary_access'][0]
P('The company\u2019s own investor-relations channel was attempted first, before any aggregator, and the attempt is '
  f"logged whether or not it succeeded. It was reached on {_pa['attempt_date']} — and the route matters: four direct "
  'address guesses each returned the site\u2019s own error page under a success code, which reads as a working page to '
  'anything that only checks the status. The sitemap found it. Every historical figure in this study comes from the '
  'company\u2019s own audited statements or its own investor material, and none from a data vendor, a broker or a press '
  'report.', size=9.8)

# ================= Appendix C ================================================
H1('Appendix C  The expert valuation panel')
P('Every Testahil study closes with a panel of standing expert personas — drawn from the house Expert Persona Library, not '
  'invented for the occasion, so each accumulates a track record across studies and a quarterly update is a re-run, not a '
  're-training. For stc we cast the telecom trio from the library’s coverage map — cash-returns (DCF + returns on capital '
  'against WACC), earnings-power (normalized through-cycle earnings + multiples), and macro-policy (scenario-weighted '
  'policy options) — labelled Expert 1 / 2 / 3. Each runs a genuinely different method, derives its fair value from shown '
  'workings, and states a falsification condition.')

H2('C.1  Expert 1 — cash returns: ROIC against the cost of capital')
P('Worldview and tradition. A business is worth the cash it returns over its life, and it creates value only when each '
  'riyal of capital earns above its cost. He looks past accounting earnings to free cash flow and to the economic-profit '
  'spread — and he is temperamentally suspicious of capex programs described with the word “vision.”', size=9.8)
P('When it works / fails. Best for capital-intensive businesses where returns on capital are the crux — precisely a '
  'telecom. Fails where reinvestment economics are genuinely improving (past ROIC misleads a new-moat story) — his risk '
  'here if the AI-data-centre build earns structurally above telecom returns.', size=9.8)
# EVERY LINE OF THIS TABLE WAS TYPED and by the rebuild the cost of capital in it read
# 7.59% against the §1.8 build's 8.13% — the row's own label says it accepts that build.
# An expert's assumptions may be his own; the study's numbers may not be retyped.
_e1ic = E['e1_ic']; _e1roic = E['e1_roic']; _e1ep = E['e1_ep']
_wacc = D['coc_record']['wacc_exp']; _fade = E['e1_fade']
_e1mult = 1.0 / (_wacc + _fade - dcf['tg'])
rows = [
 ['Expert 1’s economic-profit test', 'Value'],
 [f"Invested capital (parent equity {D['lenses']['book_value']*D['bridge_record']['shares_mn']/1000.0:,.1f} bn "
  f"plus net debt {(_e1ic - D['lenses']['book_value']*D['bridge_record']['shares_mn'])/1000.0:,.1f} bn)",
  f"SAR {_e1ic/1000.0:,.1f} bn"],
 ['FY26E operating profit after tax, over that capital',
  f"SAR {_e1roic*_e1ic/1000.0:,.1f} bn → {_e1roic*100:.1f}%"],
 ['Cost of capital (he accepts the §1.8 build)', f"{_wacc*100:.2f}%"],
 ['Economic profit = (return − cost) × capital', f"SAR {_e1ep/1000.0:,.1f} bn/yr"],
 [f'Fade: excess returns decay {_fade*100:.1f}%/yr toward the cost of capital',
  f"Multiple on economic profit {_e1mult:.1f}x"],
 ['Core enterprise value = capital + present value of the fading economic profit',
  f"SAR {(_e1ic + _e1ep*_e1mult)/1000.0:,.0f} bn"],
 [f"+ stakes less net debt less the minority, divided by "
   f"{D['bridge_record']['shares_mn']:,.1f} mn shares",
   f"\u2192 SAR {E['e1']['base']:.1f} per share"],
]
table(rows, [4.4, 1.7], first_col_bold=True, size=9.0)
P(f"Sensitivity, and the swing really is the fade rate alone — the cost of capital has its own grid in §1.9 and is held "
  f"here: at {E['e1_fade_lo']*100:.0f}% a year, a durable moat, his value rises to SAR {E['e1']['rng'][1]:.2f}; "
  f"at {E['e1_fade_hi']*100:.0f}%, where competition and technology churn eat the spread, it falls to "
  f"SAR {E['e1']['rng'][0]:.2f}. Cross-examination: "
  "he tells Expert 2 that a 15× multiple on normalized earnings quietly capitalizes today’s ROIC forever without charging "
  "for the capital that sustains it — his fade does explicitly what the multiple hides. He tells Expert 3 that scenario "
  "trees on the policy rate are fine, but the bigger lever is inside the company: each percentage point of capex intensity "
  "is SAR 0.8 bn of cash that either earns the spread or doesn’t.", size=9.8)
rich([('Verdict, falsification, market-implied. ', dict(bold=True)),
      (f"Fair SAR {E['e1']['base']:.1f} (range {E['e1']['rng'][0]:.0f}–{E['e1']['rng'][1]:.0f}) — the panel’s conservative "
       "anchor, below spot: on his arithmetic the market already pays for the excess returns to persist a decade-plus. "
       "Falsified by disclosed data-centre economics showing contracted returns above telecom ROIC (the fade would then be "
       f"too harsh), or by return on capital holding above 15% through FY2028 while capital "
       f"intensity normalises. What the price implies: at SAR {D['spot']:.2f} the "
       f"market discounts a gentler fade than his {E['e1_fade']*100:.1f}% a year, i.e. it believes in the moat slightly "
       "more than he does.", {})])

H2('C.2  Expert 2 — normalized earnings power')
P('Worldview and tradition. An operating company is worth a fair multiple of its sustainable, mid-cycle earnings power; '
  'peaks, troughs and one-off gains are noise to be stripped before anything is capitalized.', size=9.8)
P('When it works / fails. Best for stable operating businesses with a track record — a fit for stc, whose underlying '
  'earnings have grown 12–13% (adjusted) for two straight years. Fails at structural breaks: if the subsidiary portfolio '
  're-rates the growth profile, his through-cycle multiple is too low; if a price war breaks the margin, too high.', size=9.8)
# A WATERFALL A READER IS ASKED TO FOLLOW MUST REACH THE ANSWER IT PRINTS, and this one did
# not. It ran "FY2025 attributable profit 14,828 less the one-off zakat credit (466)" to a
# printed "about 14,400" — arithmetic that gives 14,362 — and the adjustment was the wrong
# size anyway: 466 is the NET zakat line for the year, not the one-off inside it. What is
# non-recurring is the reversal of prior years' provision that note 33(a) names on its own
# line. The normalisation now charges the year at the rate the three filed years imply and
# takes the minority's share off the result, and table_residual asserts the column at build
# time so it cannot silently stop reaching its own answer again.
import table_residual as TRES

_pbz = _ISH['profit_before_zakat'][2] / 1000.0
_zk = _pbz * _ISH['effective_zakat_rate']
_nci_off = (_pbz - _zk) * D['bridge_record']['nci']['profit_share']
_steps = [('less zakat at the rate the three filed years imply', -_zk),
          ('less the minority interest', -_nci_off)]
TRES.waterfall(_pbz, _steps, D['rel_basis']['norm_pat'])
rows = [
 ['Expert 2’s normalisation', 'SAR mn'],
 ['FY2025 profit before zakat, as filed', f"{_pbz:,.0f}"],
 ['less zakat at the rate the three filed years imply', f"({_zk:,.0f})"],
 ['less the minority interest', f"({_nci_off:,.0f})"],
 ['Normalised profit attributable', f"{D['rel_basis']['norm_pat']:,.0f}"],
 ['Divided by shares in issue (%s million)' % f"{D['bridge_record']['shares_mn']:,.1f}",
  f"SAR {D['rel_basis']['norm_eps']:.2f} per share"],
 ['Justified through-cycle price-to-earnings',
  f"{E['e2']['base']/D['rel_basis']['norm_eps']:.1f}x"],
 ['Fair value', f"SAR {E['e2']['base']:.1f} per share"],
]
table(rows, [4.4, 1.7], first_col_bold=True, size=9.0)
# THE THREE FIGURES IN THIS SENTENCE WERE TYPED AND NONE OF THEM SURVIVED HIS OWN
# ARITHMETIC: 13.5x on his normalised earnings per share is 35.8 rather than 36.8, 16.5x
# is 43.7 rather than 50.3, and one turn of the multiple is worth his EPS, not 2.9.
_e2eps = D['rel_basis']['norm_eps']
_e2x = E['e2']['base'] / _e2eps
P(f"Sensitivity (the swing is the multiple): every turn of the price-to-earnings ratio is worth exactly his normalised "
  f"earnings per share, SAR {_e2eps:.2f} — so at {_e2x-1.5:.1f}x he reads SAR {(_e2x-1.5)*_e2eps:.1f} and at "
  f"{_e2x+1.5:.1f}x SAR {(_e2x+1.5)*_e2eps:.1f}. His published range of SAR {E['e2']['rng'][0]:.1f} to "
  f"{E['e2']['rng'][1]:.1f} spans {E['e2']['rng'][0]/_e2eps:.1f}x to {E['e2']['rng'][1]/_e2eps:.1f}x. "
  'Cross-examination: he tells Expert 1 that a fade model is a multiple wearing a lab coat — the honest disagreement '
  f"is the number. He tells Expert 3 that the dividend lens undervalues whatever the board chooses not to distribute.",
  size=9.8)
rich([('Verdict, falsification, market-implied. ', dict(bold=True)),
      (f"Fair SAR {E['e2']['base']:.1f} (range {E['e2']['rng'][0]:.0f}–{E['e2']['rng'][1]:.0f}), "
       f"{(E['e2']['base']/D['spot']-1)*100:+.0f}% against the market. On clean current earnings the stock is priced "
       f"above his read: the market pays {D['spot']/_e2eps:.1f}x his normalised earnings against the {_e2x:.1f}x he "
       "will justify, and the difference is growth not yet printed. Falsified by two consecutive years of double-digit "
       "adjusted earnings growth, which would make his base stale, or by the flat margin path turning down.", {})])

H2('C.3  Expert 3 — macro-policy: the scenario tree')
P('Worldview and tradition. In a policy-driven market, policy outranks fundamentals: the Fed/SAMA rate path, the oil-'
  'funded fiscal impulse, and sovereign strategic priorities (Vision 2030, the AI build, PIF’s portfolio choices) move '
  'this stock more than management execution does. He prices the equity as a probability-weighted set of policy worlds, '
  'expressed through the dividend stream — the one cash flow a policy-anchored shareholder actually receives.', size=9.8)
P('When it works / fails. Best where binary policy catalysts dominate — rate cuts, sovereign flows, national-champion '
  'capex mandates. Fails through false precision: the probabilities are judgments, and the tree can miss the branch that '
  'grows (his own flag: a KSA price war appears in nobody’s policy scenario, yet would dominate all of them).', size=9.8)
rows = [
 ['Scenario (through 2027)', 'Prob.', 'World', 'DDM value'],
 ['Easing + special dividends', '30%', 'Fed/SAMA cut 75–100 bp; cover proven; a special repeats', f"SAR {L['ddm']['bull']*1.02:.0f}"],
 ['Base: policy held, dividend locked', '45%', 'Gradual cuts; capex mid-band; SAR 2.20 through 2027 then +3%', f"SAR {ddm['ps']:.0f}"],
 ['Higher-for-longer + capex overrun', '25%', 'No cuts to mid-2027; capex at 17.5%; no specials', f"SAR {L['ddm']['bear']*0.96:.0f}"],
 ['Probability-weighted fair value', '', '', f"SAR {E['e3']['base']:.1f}"],
]
table(rows, [2.2, 0.7, 2.7, 1.1], first_col_bold=True, size=8.9, band_rows=[4])
P(f"Sensitivity (swing = the scenario weights): shifting 10 points from base to bear moves him ≈SAR 1.5; his answer is "
  "more stable than either colleague’s because the dividend floor does most of the work in every branch. "
  "Cross-examination: he tells Expert 1 that a fade rate is unknowable to the decimal while the policy calendar is "
  "published — model what is scheduled. He tells Expert 2 that a through-cycle multiple assumes a cycle; Saudi rates are "
  "pegged to a foreign central bank, so the local 'cycle' is imported and can stay dislocated from local fundamentals for "
  "years.", size=9.8)
rich([('Verdict, falsification, market-implied. ', dict(bold=True)),
      # "THE PANEL VALUE CLOSEST TO SPOT" WAS TYPED AND IS NO LONGER TRUE: on the rebuilt
      # numbers Expert 2 sits nearer the market than Expert 3 does. Which expert is
      # closest is arithmetic about three committed numbers, so it is computed.
      (f"Fair SAR {E['e3']['base']:.1f} — the dividend model with its eyes open, and "
       f"{'the panel value closest to the market' if abs(E['e3']['base']-D['spot']) <= min(abs(E['e1']['base']-D['spot']), abs(E['e2']['base']-D['spot'])) else 'between his two colleagues, with Expert 2 the nearer to the market'}. "
       "Falsified by the board breaking the policy (either direction: a cut dividend or a step-change up), or by a Fed "
       "path outside his tree (no cuts through 2027, or emergency easing). What the price implies: the market is pricing "
       "roughly his base case with a small weight on the bear — i.e. the locked dividend at a ~5% yield, and near-zero "
       "credit for specials or the AI build.", {})])

H2('C.4  Cross-examination — each challenge conceded or rejected')
# THE MODEL SKELETON CARRIES A C.4 AND THIS STUDY SKIPPED STRAIGHT FROM C.3 TO C.5. The
# challenges existed — each expert put one to each colleague inside their own paragraph —
# but nothing said which of them survived, which is the whole point of the section: a
# challenge that is never answered is a debating point rather than a finding.
P('Each expert puts a challenge to each colleague above. A challenge is worth nothing until somebody says whether it '
  'lands, so each is answered here, and two of the four are conceded.', size=9.8)
rows = [
 ['Challenge', 'From → to', 'Answer'],
 ['A fade model is a multiple wearing a lab coat — the honest disagreement is the number, not the machinery.',
  '2 → 1', 'CONCEDED, partly. Both capitalise the same earnings; the fade makes the capital charge explicit and the '
           'multiple buries it. That is a real difference in what is visible, not in what is assumed — and it means '
           'Expert 1 owns his fade rate where Expert 2 does not own his multiple.'],
 ['A through-cycle multiple assumes a cycle, and the Saudi rate cycle is imported from a foreign central bank.',
  '3 → 2', 'CONCEDED. The riyal is pegged, so the local discount rate is set abroad and can stay dislocated from '
           'local fundamentals for years. Expert 2\u2019s multiple is a claim about the average of a cycle whose length '
           'he does not control.'],
 ['Scenario trees on the policy rate are fine, but the bigger lever is inside the company: each point of capital '
  'intensity is real cash that either earns the spread or does not.',
  '1 → 3', 'REJECTED, on this company\u2019s own numbers. The three filed years span a capital intensity of '
           '1.05 to 1.25 times the depreciation of the base being renewed, and that whole span is worth less to the '
           'answer than the discount rate is. The policy lever is the larger one here; it is simply the one nobody '
           'controls.'],
 ['The dividend lens undervalues whatever the board chooses not to distribute.',
  '2 → 3', 'REJECTED, with a caveat. Retained cash shows up as future dividends in the same model, so it is not lost '
           '— but only if it earns its cost of capital on the way. That is Expert 1\u2019s question, not Expert 2\u2019s, '
           'and it is the one the data-centre build actually turns on.'],
]
table(rows, [2.5, 0.75, 2.85], first_col_bold=False, size=8.4)
caption('Two conceded, two rejected. Nothing here changes any expert\u2019s number: a concession about what a method '
        'makes visible is not a concession about what it computes, and the panel is published with its disagreement '
        'intact rather than talked into a consensus.')

H2('C.5  The three in one room')
P('Put the three in a room and the argument is about one thing: what happens to stc’s return on capital as the Kingdom’s '
  'AI-infrastructure build runs through its income statement.', size=9.8)
# THE FIGURES INSIDE THE QUOTATION MARKS ARE EACH EXPERT'S OWN AND WERE TYPED. Expert 3
# was made to say SAR 46 against a computed 38.1, and Expert 2 to say the market agreed
# with him "to the decimal" while it sits ten per cent above him. A number in dialogue is
# still a number.
P(f"Expert 1: “{E['e1_roic']*100:.0f} per cent returns on {E['e1_ic']/1000.0:.0f} billion of capital, fading as every "
  'telecom’s returns have always faded. The data centres are capital expenditure with a press release until somebody '
  f"shows me contracted economics. I pay SAR {E['e1']['base']:.0f}.”", size=9.8)
P('Expert 3: “Your fade rate is a guess dressed as physics. What is not a guess: the board has signed a cheque for '
  f"SAR {D['drivers']['payout_dps'][0]:.2f} a year through 2027, the central bank’s next moves are the Federal "
  'Reserve’s, and the sovereign has made this company its digital-infrastructure champion. Price the policy, not the '
  f"physics — SAR {E['e3']['base']:.0f}.”", size=9.8)
P(f"Expert 2: “You are both reaching. Clean earnings are SAR {D['rel_basis']['norm_eps']:.2f} a share; the market pays "
  f"{E['e2']['base']/D['rel_basis']['norm_eps']:.0f} times that across the Gulf. Everything else — fades, scenario "
  f"trees, gigawatts — is a story about the next turn of the multiple. SAR {E['e2']['base']:.0f}, and note that the "
  f"market is paying {D['spot']/D['rel_basis']['norm_eps']:.1f} times, which is {(D['spot']/E['e2']['base']-1)*100:.0f} "
  'per cent more than I will justify — so I am not agreeing with the price, I am naming the gap.”', size=9.8)

H2('C.6  Reading the divergence')
figure(os.path.join(HERE, 'figD1_experts.png'), 6.0, 'Figure C-1 — The three experts’ fair-value ranges. Brass ticks are base cases; the gold '
       'band is the panel centre; the ink line is spot. The spread is the return-fade question.')
rows = [
 ['Expert', 'Method', 'Single swing assumption', 'Base fair value'],
 ['Expert 1', 'Cash returns / economic profit',
  f"The fade rate on excess returns ({E['e1_fade']*100:.1f}%/yr)", f"SAR {E['e1']['base']:.1f}"],
 ['Expert 2', 'Normalized earnings power',
  f"The through-cycle multiple ({E['e2']['base']/D['rel_basis']['norm_eps']:.0f}x)",
  f"SAR {E['e2']['base']:.1f}"],
 ['Expert 3', 'Macro-policy scenario tree', 'The scenario weights on the rate/payout path', f"SAR {E['e3']['base']:.1f}"],
]
table(rows, [1.0, 2.2, 2.5, 1.3], first_col_bold=True, size=9.0)
# THIS PARAGRAPH MADE FOUR CLAIMS ABOUT THREE NUMBERS AND EVERY ONE WAS TYPED AND WRONG
# ON THE REBUILT PANEL: a spread of "about 23% of the low" against an actual 7.9%; Expert 2
# "lands at spot" and Expert 3 "lands above it" when all three sit below it; and the house
# lenses "sit above the panel" when the central sits inside it. Each is now derived from
# the three committed values, so the sentence cannot outlive the numbers it describes.
_bases = [E['e1']['base'], E['e2']['base'], E['e3']['base']]
_lo, _hi = min(_bases), max(_bases)
_mean = sum(_bases) / 3.0
_above = [n for n, b in zip(('Expert 1', 'Expert 2', 'Expert 3'), _bases) if b >= D['spot']]
_where = ('all three land below the market price' if not _above else
          '%s land%s above the market price and the others below' %
          (' and '.join(_above), '' if len(_above) > 1 else 's'))
P(f"The spread — SAR {_lo:.1f} to {_hi:.1f}, {(_hi/_lo-1)*100:.0f}% of the low — is narrow by this series’ standards, "
  f"and it measures one thing cleanly: how much of stc’s current {E['e1_roic']*100:.0f}% return on capital survives the "
  f"next decade of competition, technology churn and nation-scale capital spending. On that question the three barely "
  f"disagree, and {_where}: Expert 1 charges for the erosion explicitly, Expert 2 freezes today’s clean earnings at a "
  "multiple he will defend, and Expert 3 prices the policy floor — three different routes to the same neighbourhood. "
  f"The study’s own central of SAR {D['central']:.2f} sits "
  f"{'inside' if _lo <= D['central'] <= _hi else 'outside'} that band, "
  f"SAR {abs(D['central']-_mean):.2f} {'above' if D['central'] > _mean else 'below'} the panel’s own average, which is "
  "worth saying plainly: the cash-flow model and three independently-constructed methods arrive within a riyal or two "
  "of each other, and all of them below the price. An investor’s position on this stock reduces to a position on one "
  "axis: if the data-centre build earns telecom-plus returns, the cash-flow model understates it; if it earns "
  "telecom-minus, Expert 1 is right and today’s price already flatters it.")
caption('Each expert\u2019s point fair value, and its range where the method produces one, is recorded with the price '
        f'it was struck against: SAR {D["spot"]:.2f} on {D["spot_date"]}.')

# ================= About / Disclaimer / footer ================================
H1('About this series')
P('Testahil publishes independent, educational valuation studies. Each is an attempt to reason transparently about what a '
  'security is worth, with every assumption shown and a companion model so readers can disagree productively. The house '
  'style is distributions, not tips: we describe ranges and probabilities, not targets, and we do not tell anyone what to '
  'do. Studies are framed as educational analysis, the preparer is not licensed by any securities regulator, and holdings '
  'are disclosed.')
H1('Disclosure & Disclaimer')
for head, body in [
 ('Not investment advice. ', 'This document is educational and informational only. It is not, and must not be relied upon '
  'as, investment, financial, legal, accounting or tax advice, nor an offer, solicitation or recommendation to buy, sell or '
  'hold any security. It contains no price target and no rating.'),
 ('No licence; no advisory relationship. ', 'The preparer is not registered or licensed with any securities or financial '
  'regulator in any jurisdiction — including the Saudi Capital Market Authority (CMA) — holds no brokerage or investment-'
  'advisory authorisation, and is not acting as your adviser or fiduciary. Nothing here is personalised to your '
  'circumstances.'),
 ('Holdings disclosure. ', 'The preparer may hold, and may in the future take or dispose of, a position in the security '
  'discussed in this report, and may transact at any time without notice. This is a potential conflict of interest you '
  'should weigh.'),
 ('Sources & accuracy. ', 'Reported financial and operating figures are drawn from the company’s public disclosure '
  '(stc.com IR releases and interim financial statements) and other public sources believed reliable but not independently '
  'verified; they may contain errors or be superseded. Forward-looking inputs — the segment growth and margin paths, capex '
  'intensity, the derived risk-free rate and regressed beta, terminal growth, the multiples, the stake marks and the '
  'Monte-Carlo factor probabilities — are the preparer’s own judgments and are inherently uncertain. Some balance-sheet '
  'detail lines are grouped estimates tying to disclosed totals.'),
 ('Forward-looking statements. ', 'Any statements about the future are estimates subject to risks and uncertainties; actual '
  'results may differ materially. The Monte Carlo models price, not value, and encodes subjective probabilities for events '
  'that have not occurred.'),
 ('No reliance; your responsibility. ', 'Do your own research and consult a licensed professional before making any '
  'decision. You are solely responsible for your investment decisions and their outcomes. To the maximum extent permitted '
  'by law, the preparer accepts no liability for any loss arising from use of this document.'),
 ('Currency & figures. ', 'Figures are in Saudi riyals (SAR), millions unless stated; bn denotes billion. The riyal is '
  'pegged to the US dollar at 3.75. Rounding may cause totals to differ slightly. Spot price and market data are as of '
  '7 July 2026 and change continuously.'),
]:
    rich([(head, dict(bold=True, italic=True)), (body, {})], size=9.6, space_after=5)
P('TESTAHIL · Independent Valuation Study · Educational Analysis · Saudi Telecom Company (Tadawul: 7010) · '
  'edition 05-09-2026 · reporting currency SAR', size=8.8, color=GREY, align='center', space_before=10)

doc.save(os.path.join(HERE, 'STC_Valuation_Study_05-09-2026_public.docx'))
print('docx saved')
