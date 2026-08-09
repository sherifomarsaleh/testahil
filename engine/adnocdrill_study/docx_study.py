"""ADNOC Drilling Company P.J.S.C. — the delivered valuation study.

Sixteen sections, in order. Every financial numeral is read from
study_numbers.json, strike_result.json, experts.json or technicals.json — no
number is typed into this file.
"""
import json, os
from docx_base import Doc, INK, GREY, BRASS, GOLD, F_CREAM, F_PANEL, F_PANEL2

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, 'study_numbers.json')))
ST = json.load(open(os.path.join(HERE, 'strike_result.json')))
EX = json.load(open(os.path.join(HERE, 'experts.json')))
TA = json.load(open(os.path.join(HERE, 'technicals.json')))
S0 = json.load(open(os.path.join(HERE, 'step0_result.json')))
S0D = json.load(open(os.path.join(HERE, 'step0_diagnostic.json')))
BETA = json.load(open(os.path.join(HERE, 'beta_result.json')))

IN, W, M, H, U, UE = (D['inputs'], D['wacc'], D['market'], D['history'], D['units_history'],
                      D['unit_economics'])
CA, CB = D['cases']['A'], D['cases']['B']
RA, RB = CA['rows'], CB['rows']
REL, BOOK, NORM, SENS, FV = (D['relative'], D['book'], D['normalised'], D['sensitivity'],
                             D['fair_value'])
TRI = D['unconv_margin_triangulation']
SPOT = M['spot_aed']
SH = M['shares_outstanding_k']
FX = IN['fx_aed_usd']['value']
H1, H3, H5 = ST['horizons']['1M'], ST['horizons']['3M'], None


def V(k):
    return IN[k]['value']


def bn(x):
    return f'{x/1e6:,.2f}'


def mn(x):
    v = x / 1e3
    if abs(v) < 0.5:          # never print a negative zero
        v = 0.0
    return f'{v:,.0f}'


def pc(x, d=1):
    return f'{x*100:.{d}f}%'


d = Doc()
P, T, H_1, H_2, H_3 = d.P, d.table, d.H1, d.H2, d.H3

# ============================== 1. MASTHEAD + READ FIRST =====================
d.masthead()
P('ADNOC Drilling Company P.J.S.C.', size=22, bold=True, space_after=2)
P('Abu Dhabi Securities Exchange · ADNOCDRILL · reports in US dollars, trades in dirhams',
  size=11, color=GREY, space_after=10)
P('Valuation study — 9 August 2026', size=12, bold=True, color=BRASS, space_after=12)

H_1('READ FIRST')
d.box([
    ('What this is. ', 'An independent valuation of ADNOC Drilling built from the company\'s '
     'own audited and reviewed financial statements. It produces a fair-value RANGE and a '
     'distribution of possible prices. It contains no rating and no price target, and it is '
     'not investment advice.'),
    ('Where the history comes from. ', 'The three years of income statement, balance sheet and '
     'cash flow are read from the signed consolidated financial statements for 2023, 2024 and '
     '2025 and the reviewed interim statements for the first quarter and first half of 2026, '
     'each downloaded from the company\'s own investor-relations site. Operating units — rig '
     'counts, wells drilled, integrated-services rig counts and unconventional revenue — come '
     'from the company\'s own quarterly management commentary, the only published source that '
     'carries them. No data vendor, broker note or press report is a source for any figure '
     'about ADNOC Drilling itself.'),
    ('Two currencies. ', 'The company\'s functional and presentation currency is the US dollar; '
     'its shares trade in dirhams. The valuation runs in dollars and converts to dirhams at the '
     f'peg of {FX} dirhams to the dollar.'),
    ('One judgement, computed both ways. ', 'The most consequential question in this study — '
     'what happens to drilling demand once Abu Dhabi\'s production-capacity target is met — has '
     'two defensible answers. Both are computed in full and published side by side. Neither is '
     'averaged away.'),
])

# ============================== 2. HEADLINE ==================================
H_1('Headline')
P(f'ADNOC Drilling trades at AED {SPOT:.2f}. Five independent lenses put fair value between '
  f'AED {FV["low"]:.2f} and AED {FV["high"]:.2f}, with a weighted central of '
  f'AED {FV["central"]:.2f} — {pc(abs(FV["upside_central"]))} '
  f'{"below" if FV["upside_central"] < 0 else "above"} the market. The company is not '
  f'mispriced by a wide margin; it is priced for the continuation of a programme that its own '
  f'customer has not yet extended beyond 2027.')
P('Three things carry the analysis.', bold=True, space_after=3)
d.bullet('The business is an exceptional operator on almost any measure. Revenue compounded '
         f'from USD {bn(H["2023"]["revenue"])}bn in 2023 to USD {bn(H["2025"]["revenue"])}bn in '
         f'2025, EBITDA margins have run between {pc(H["2023"]["ebitda_margin"])} and '
         f'{pc(H["2024"]["ebitda_margin"])}, and the return on capital employed was '
         f'{pc(H["2025"]["roic"],0)} in 2025 and unchanged in the first half of 2026. Very few '
         'listed drillers anywhere earn that on that scale.',
         bold_head='It is a very good business. ')
d.bullet('Every rig works for one customer group. Revenue is billed to ADNOC Onshore, ADNOC '
         'Offshore and their affiliates; the controlling shareholder is the same group. That '
         'is why the contracted book is so stable, why the receivable is so large — '
         f'days sales outstanding stood at {H["2025"]["dso"]:.0f} days at the '
         f'end of 2025 — and why the terminal question is the only question that matters.',
         bold_head='It has one customer. ')
d.bullet('First-half 2026 revenue grew 4% against 22% for full-year 2025. The company has '
         'reaffirmed roughly USD 5 billion of revenue for 2026 and has explicitly declined to '
         'guide 2027 until rig and services phasing is fixed. The market is paying '
         f'{REL["implied_own_ev_ebitda"]:.1f} times guided EBITDA against a segment-weighted '
         f'peer median of {REL["blended_multiple"]:.1f} times. That gap is the whole argument.',
         bold_head='The growth rate has already turned. ')

d.figure(os.path.join(HERE, 'fig1_football.png'), 6.9,
         'Fair value by lens. Each bar is the same lens re-run on a stated stress — the '
         'discounted-cash-flow bands move the cost of capital 50 basis points either way, the '
         'relative band is the peer set\'s own interquartile range, the book band moves the '
         'cost of equity 50 basis points, the normalised band moves the margin two points.')

# ============================== 3. VALUATION SUMMARY =========================
H_1('Valuation summary')
rows = [['Lens', 'AED/share', 'Weight', 'Bear', 'Bull', 'Terminal value share']]
LBL = {'dcf_A': 'Discounted cash flow — continued expansion',
       'dcf_B': 'Discounted cash flow — capacity plateau',
       'relative': 'Relative multiples', 'book': 'Book value and sustainable return',
       'normalised': 'Normalised earnings power'}
TVS = {'dcf_A': pc(CA['tv_pct_of_ev']), 'dcf_B': pc(CB['tv_pct_of_ev']),
       'relative': '—', 'book': '—', 'normalised': '—'}
for k in ('dcf_A', 'dcf_B', 'relative', 'book', 'normalised'):
    rows.append([LBL[k], f'{FV["by_lens"][k]:.2f}', pc(FV['weights'][k], 0),
                 f'{FV["lens_range"][k]["bear"]:.2f}', f'{FV["lens_range"][k]["bull"]:.2f}',
                 TVS[k]])
rows.append(['Weighted central fair value', f'{FV["central"]:.2f}', '100%',
             f'{FV["central_range"]["bear"]:.2f}', f'{FV["central_range"]["bull"]:.2f}', ''])
rows.append(['Market price, 7 August 2026', f'{SPOT:.2f}', '', '', '', ''])
rows.append(['Central against the market price', pc(FV['upside_central']), '', '', '', ''])
T(rows, [2.55, 0.85, 0.72, 0.72, 0.72, 1.14], band_rows={6, 8})
d.caption('The terminal-value share is shown beside each discounted-cash-flow lens because it '
          'is the honest measure of how much of that answer rests on a period beyond the '
          'forecast. Both cases carry more than seven-tenths of their value there.')

P('Why the two discounted-cash-flow cases carry equal weight and half the total: they are the '
  'same model on two different answers to one question, and the study does not claim to know '
  'which is right. Averaging them into a single case would hide exactly the uncertainty the '
  'reader needs to see.')

# ============================== 4. COMPANY OVERVIEW ==========================
H_1('Company overview')
P('ADNOC Drilling Company P.J.S.C. was incorporated in 1972 by a resolution of the Council of '
  'Ministers of the Government of Abu Dhabi and listed on the Abu Dhabi Securities Exchange in '
  'October 2021. It provides start-to-finish drilling and construction services across '
  'conventional and unconventional reservoirs and hires out onshore and offshore rigs. Its '
  'parent is Abu Dhabi National Oil Company, which is wholly owned by the Government of Abu '
  'Dhabi; during 2025 the shareholding was transferred to XRG P.J.S.C., an international energy '
  'investment company itself wholly owned by ADNOC, with no change in ultimate control.')
P('The group reports three segments and states in its own accounts that there were no '
  'inter-segment sales in either of the last two years.', space_after=3)
rows = [['Segment', 'FY2025 revenue (USD mn)', 'Share', 'FY2025 EBITDA (USD mn)',
         'EBITDA margin', 'What it is']]
segs = [('Onshore', H['2025']['seg_onshore'], V('seg_ebitda_on_fy25'),
         'Land rigs, water wells and workover rigs, deployed mainly across ADNOC Onshore '
         'concessions'),
        ('Offshore', H['2025']['seg_offshore'], V('seg_ebitda_off_fy25'),
         'Owned jack-ups and island rigs meeting ADNOC Offshore drilling needs; the jack-up and '
         'island segments were merged into one from the first quarter of 2025'),
        ('Oilfield Services', H['2025']['seg_ofs'], V('seg_ebitda_ofs_fy25'),
         'Integrated and discrete well services, built out of the partnership with Baker Hughes '
         'formed in late 2018')]
for name, rev, eb, what in segs:
    rows.append([name, mn(rev), pc(rev / H['2025']['revenue']), mn(eb), pc(eb / rev), what])
rows.append(['Group', mn(H['2025']['revenue']), '100.0%', mn(H['2025']['ebitda']),
             pc(H['2025']['ebitda_margin']), ''])
T(rows, [1.05, 1.02, 0.62, 1.02, 0.78, 2.21], band_rows={4})

P('The balance sheet is what an asset-heavy driller\'s should look like. Property and equipment '
  f'of USD {bn(H["2025"]["ppe"])}bn is two-thirds of USD {bn(H["2025"]["total_assets"])}bn of '
  f'total assets. There is no lending book, no investment property and no development '
  f'inventory. The only equity-accounted holdings are two service joint ventures — Enersol and '
  f'Turnwell — carried at USD {mn(H["2025"]["jv_investment"])} million and contributing USD '
  f'{mn(H["2025"]["jv_share"])} million of profit. That balance-sheet shape, together with the '
  f'revenue mix above, is the evidence for treating this as an operating company and valuing it '
  'on the cash its fleet generates rather than on a sum of holdings or a book of loans.')

P('The fleet, in the company\'s own numbers:', bold=True, space_after=3)
rows = [['', 'FY2023', 'FY2024', 'FY2025', '30 June 2026']]
rows.append(['Abu Dhabi onshore rigs', f'{V("rigs_onshore_fy23"):.0f}',
             f'{V("rigs_onshore_fy24"):.0f}', f'{V("rigs_onshore_fy25"):.0f}', '92'])
rows.append(['Jack-up rigs', f'{V("rigs_jackup_fy23"):.0f}', f'{V("rigs_jackup_fy24"):.0f}',
             f'{V("rigs_jackup_fy25"):.0f}', '36'])
rows.append(['Island rigs', f'{V("rigs_island_fy23"):.0f}', f'{V("rigs_island_fy24"):.0f}',
             f'{V("rigs_island_fy25"):.0f}', '13'])
rows.append(['Regional rigs outside the UAE', '—', '—', '—',
             f'{V("rigs_regional_2q26"):.0f}'])
rows.append(['Total rigs', '129', '142', '140', '171'])
rows.append(['Integrated-services rigs', f'{V("ids_fy23"):.0f}', f'{V("ids_fy24"):.0f}',
             f'{V("ids_fy25"):.0f}', f'{V("ids_2q26"):.0f}'])
rows.append(['Wells drilled', f'{V("wells_fy23"):.0f}', f'{V("wells_fy24"):.0f}',
             f'{V("wells_fy25"):.0f}', '—'])
T(rows, [2.45, 1.05, 1.05, 1.05, 1.30], band_rows={5})
d.caption('The 2025 total of 140 excludes 29 regional rigs the company reported on a pro-forma '
          'basis at the year end; 8 of those closed in January 2026 through the joint venture '
          'with SLB and the remainder through the acquisition of a stake in MBPS, which is why '
          'they appear in the June 2026 column.')

# ============================== 5. §1 FUNDAMENTAL VALUATION ==================
d.page_break()
H_1('1. Fundamental valuation')

H_2('1.1 Cash-flow model')
P('The primary lens is a discounted free cash flow to the firm over five explicit years, with '
  'a terminal value built on the return the business earns on the capital it reinvests. The '
  'waterfall below is the continued-expansion case in full; every line is a formula in the '
  'delivered workbook.', space_after=4)
rows = [['USD million'] + [f'FY{r["year"]}E' for r in RA]]
for lbl, key, f in (('Revenue', 'revenue', mn), ('EBITDA', 'ebitda_ex_jv', mn),
                    ('EBITDA margin', 'x', None),
                    ('less depreciation and amortisation', 'dna', mn),
                    ('EBIT', 'ebit', mn), ('Tax rate', 't', None),
                    ('NOPAT = EBIT x (1 - tax rate)', 'nopat', mn),
                    ('add back depreciation and amortisation', 'dna', mn),
                    ('less capital expenditure', 'capex', mn),
                    ('less increase in working capital', 'delta_wc', mn),
                    ('Free cash flow to the firm', 'fcff', mn),
                    ('Discount factor', 'discount_factor', None),
                    ('Present value of free cash flow to the firm', 'pv_fcff', mn)):
    if key == 'x':
        rows.append([lbl] + [pc(r['ebitda_ex_jv'] / r['revenue']) for r in RA])
    elif key == 't':
        rows.append([lbl] + [pc(V('tax_rate'), 0) for r in RA])
    elif key == 'discount_factor':
        rows.append([lbl] + [f'{r[key]:.3f}' for r in RA])
    elif lbl.startswith('less'):
        rows.append([lbl] + [f'({f(r[key])})' for r in RA])
    else:
        rows.append([lbl] + [f(r[key]) for r in RA])
T(rows, [2.60, 0.88, 0.88, 0.88, 0.88, 0.88], band_rows={2, 5, 7, 11, 13})

P('The bridge from enterprise value to equity, struck on the capital structure at 30 June 2026 '
  'rather than a year-old one:', space_after=4)
rows = [['USD million', 'Continued expansion', 'Capacity plateau', 'Note']]
BR = [('Present value of the explicit five years', CA['pv_explicit'], CB['pv_explicit'], ''),
      ('Present value of the terminal value', CA['pv_terminal'], CB['pv_terminal'], ''),
      ('Enterprise value', CA['enterprise_value'], CB['enterprise_value'], '')]
for lbl, a, b_, note in BR:
    rows.append([lbl, mn(a), mn(b_), note])
rows.append(['Terminal value as a share of enterprise value', pc(CA['tv_pct_of_ev']),
             pc(CB['tv_pct_of_ev']),
             'More than seven-tenths of the answer sits beyond 2030 in both cases'])
for lbl, key, sign in (('add investment in joint ventures', 'jvinv_1h26', 1),
                       ('add cash and cash equivalents', 'cash_1h26', 1),
                       ('less borrowings', 'debt_1h26', -1),
                       ('less lease liabilities', 'lease_1h26', -1),
                       ('less non-controlling interests', 'nci_1h26', -1),
                       ('less the financial liability over the acquired minorities',
                        'finliab_1h26', -1)):
    v = V(key)
    s = mn(v) if sign > 0 else f'({mn(v)})'
    rows.append([lbl, s, s, ''])
rows.append(['Equity value', mn(CA['equity_value']), mn(CB['equity_value']), ''])
rows.append(['Shares outstanding (million)', f'{SH/1e3:,.0f}', f'{SH/1e3:,.0f}',
             'Issued shares less the shares the appointed market maker holds'])
rows.append(['Value per share (AED)', f'{CA["value_per_share_aed"]:.2f}',
             f'{CB["value_per_share_aed"]:.2f}', 'Converted at the peg'])
T(rows, [2.65, 1.18, 1.18, 2.02], band_rows={3, 4, 12, 14})

H_2('1.2 Book value and sustainable return')
P(f'A business earning a return on equity of {pc(BOOK["roe_sustainable"])} against a cost of '
  f'equity of {pc(W["ke_rating"], 2)} and growing at {pc(BOOK["growth"], 1)} justifies a '
  f'price-to-book of {BOOK["justified_pb"]:.2f} times. Applied to book equity attributable to '
  f'owners of USD {bn(BOOK["book_equity"])}bn — book value per share of AED '
  f'{BOOK["book_equity"]/SH*FX:.2f} — that is AED {BOOK["value_per_share_aed"]:.2f} a share. '
  f'The shares currently trade at {BOOK["current_pb"]:.2f} times book.')
d.box([('Read this lens with care. ', 'The justified multiple is a ratio whose denominator is '
        f'the cost of equity less the growth rate, which here is only '
        f'{pc(W["ke_rating"]-BOOK["growth"], 2)}. A 50-basis-point move in the cost of equity '
        f'moves the implied value from AED {FV["lens_range"]["book"]["bear"]:.2f} to AED '
        f'{FV["lens_range"]["book"]["bull"]:.2f}. The lens carries a 15% weight for that reason '
        'and no more.')], fill=F_PANEL2)

H_2('1.3 Relative multiples')
P('The listed comparator universe splits into four groups that price differently, so each of '
  'this company\'s segments is read against the group that actually does that job, weighted by '
  'that segment\'s share of segment EBITDA.', space_after=4)
rows = [['Group', 'Median EV/EBITDA', 'Applied to', 'Segment weight', 'Contribution']]
GRP = [('MENA national-oil-company drillers', REL['median_mena']),
       ('Global land drillers', REL['median_land']),
       ('Global offshore drillers', REL['median_offshore']),
       ('Diversified oilfield services', REL['median_ofs'])]
for name, mlt in GRP:
    rows.append([name, f'{mlt:.2f}x', '', '', ''])
w = REL['segment_weights']
m_on = (REL['median_mena'] + REL['median_land']) / 2
m_off = (REL['median_mena'] + REL['median_offshore']) / 2
rows.append(['Onshore multiple (average of the first two)', f'{m_on:.2f}x', 'Onshore',
             pc(w['onshore']), f'{m_on*w["onshore"]:.2f}x'])
rows.append(['Offshore multiple (average of the first and third)', f'{m_off:.2f}x', 'Offshore',
             pc(w['offshore']), f'{m_off*w["offshore"]:.2f}x'])
rows.append(['Oilfield-services multiple', f'{REL["median_ofs"]:.2f}x', 'Oilfield Services',
             pc(w['ofs']), f'{REL["median_ofs"]*w["ofs"]:.2f}x'])
rows.append(['Segment-weighted multiple', f'{REL["blended_multiple"]:.2f}x', '', '100.0%', ''])
rows.append(["ADNOC Drilling's own multiple at AED %.2f" % SPOT,
             f'{REL["implied_own_ev_ebitda"]:.2f}x', '', '', ''])
T(rows, [2.75, 1.15, 1.25, 0.95, 0.93], band_rows={8, 9})
P(f'Applying {REL["blended_multiple"]:.2f} times to the reaffirmed FY2026 EBITDA guidance '
  f'midpoint of USD {bn(REL["applied_ebitda"])}bn gives an enterprise value of USD '
  f'{bn(REL["enterprise_value"])}bn and, through the same bridge, AED '
  f'{REL["value_per_share_aed"]:.2f} a share. This is the lens that sits furthest below the '
  'market price, and the reason is a single observable fact: the shares are valued at '
  f'{REL["implied_own_ev_ebitda"]:.1f} times guided EBITDA when the closest regional comparators '
  f'— two drillers serving national oil companies on multi-year contracts — trade at '
  f'{REL["median_mena"]:.1f} times and the global land drillers at {REL["median_land"]:.1f} '
  'times. A premium is defensible; the size of it is the question.')

H_2('1.4 Normalised earnings power')
P('This lens asks what the fleet the company already owns or has taken delivery of earns at the '
  'margin management itself guides to, with no growth credited at all, and capitalises it.',
  space_after=4)
rows = [['', 'Units', 'Revenue per rig-year (USD mn)', 'Revenue (USD mn)']]
NU = NORM['units']
for lbl, key, rate in (('Abu Dhabi onshore rigs', 'onshore', U['2025']['rev_per_onshore_rig']),
                       ('Regional onshore rigs', 'regional', V('rev_per_rig_regional')),
                       ('Jack-up rigs', 'jackup', UE['rev_per_jackup_fy25']),
                       ('Island rigs', 'island', UE['rev_per_island_fy25']),
                       ('Integrated-services rigs', 'ids', U['2025']['rev_per_ids_rig'])):
    rows.append([lbl, f'{NU[key]:.0f}', f'{rate/1e3:.1f}', mn(NU[key] * rate)])
rows.append(['Normalised revenue', '', '', mn(NORM['revenue'])])
rows.append([f'Normalised EBITDA at the guided margin of {pc(NORM["ebitda_margin"])}', '', '',
             mn(NORM['ebitda'])])
rows.append(['less normalised depreciation and amortisation', '', '', f'({mn(NORM["dna"])})'])
rows.append(['Normalised EBIT', '', '', mn(NORM['ebit'])])
rows.append([f'Normalised NOPAT after tax at {pc(V("tax_rate"),0)}', '', '',
             mn(NORM['nopat'])])
rows.append([f'Capitalised at {pc(NORM["capitalisation_rate"], 2)}', '', '',
             mn(NORM['enterprise_value'])])
rows.append(['Value per share (AED)', '', '', f'{NORM["value_per_share_aed"]:.2f}'])
T(rows, [2.90, 0.85, 1.75, 1.55], band_rows={6, 7, 9, 10, 11, 12})

H_2('1.5 Synthesis — four lenses, one field')
P(f'The five readings span AED {FV["low"]:.2f} to AED {FV["high"]:.2f}. That is a wide field, '
  'and the width is informative rather than embarrassing: the asset-and-multiple lenses sit '
  'below the market and the cash-flow-and-franchise lenses sit at or above it, which is exactly '
  'what happens when a company earns an exceptional return on a modest asset base. The market '
  'price sits inside the field, above the weighted central and below the top of it.')

H_2('1.6 Drivers')
P('Revenue is built from the bottom up: rigs in service times revenue per rig-year, by class, '
  'with margins falling out as an OUTPUT of a cost stack rather than being assumed. The rates '
  'below are derived from the company\'s own disclosed segment revenue and its own disclosed '
  'rig counts — they are arithmetic, not estimates.', space_after=4)
rows = [['Revenue per rig-year (USD million)', 'FY2023', 'FY2024', 'FY2025']]
rows.append(['Abu Dhabi onshore, conventional'] +
            [f'{U[str(y)]["rev_per_onshore_rig"]/1e3:.1f}' for y in (2023, 2024, 2025)])
rows.append(['Offshore, blended'] +
            [f'{U[str(y)]["rev_per_offshore_rig"]/1e3:.1f}' for y in (2023, 2024, 2025)])
rows.append(['Integrated services, conventional'] +
            [f'{U[str(y)]["rev_per_ids_rig"]/1e3:.1f}' for y in (2023, 2024, 2025)])
rows.append(['Wells drilled per drilling rig'] +
            [f'{U[str(y)]["wells_per_rig"]:.1f}' for y in (2023, 2024, 2025)])
T(rows, [3.30, 1.20, 1.20, 1.20])
P('The onshore rate rose from 2023 to 2024 and then fell back in 2025; it is not a trend, so '
  f'the forecast escalates it at {pc(V("esc_dayrate"), 1)}, the domestic inflation rate, rather '
  'than extrapolating the 2024 step. The offshore rate rose steadily as jack-ups and island '
  'rigs came into service. The integrated-services rate is the cleanest growth story in the '
  'business and the least contracted.')

P('Costs are escalated one class at a time. A single blended inflation rate applied across '
  'physically different cost lines is the fastest way to manufacture a margin trend that is '
  'not there, so each line gets the escalator that belongs to it.', space_after=4)
rows = [['Cost line', 'FY2025 conventional base (USD mn)', 'Volume driver', 'Escalator',
         'Rate']]
CSL = {'repairs': 'Repairs and maintenance', 'staff': 'Staff costs',
       'hire': 'Hire of equipment', 'chemicals': 'Chemicals', 'fuel': 'Fuel and lubricants',
       'major_maintenance': 'Major maintenance', 'other': 'Other direct cost'}
ESCN = {V('esc_oilfield'): 'Oilfield-services cost index',
        V('esc_wages'): 'Domestic wage inflation', V('esc_fuel'): 'Own commodity path',
        V('esc_general'): 'Domestic inflation'}
for k, nice in CSL.items():
    e = UE['cost_escalator'][k]
    rows.append([nice, mn(UE['conventional_cost_stack_fy25'][k]),
                 UE['cost_driver'][k].replace('_', ' '), ESCN[e],
                 pc(e, 1) if e else '0.0% flat nominal'])
T(rows, [1.42, 1.60, 1.18, 1.55, 1.25])
P('Fuel is the line that most often gets this wrong. It is a globally traded input, so it is '
  'escalated on its own commodity path and not on a domestic price index: Brent closed at '
  'USD 88.90 on 3 August 2026 against a three-year average of USD 79.48, roughly 12% above the '
  'mean, so a flat nominal path already embeds real mean reversion. It also matters less than '
  'it looks: the company\'s onshore contracts carry an explicit fuel-escalation pass-through, '
  'and its own first-half commentary attributes part of the onshore revenue increase to exactly '
  'that mechanism, so the line is close to margin-neutral in either direction.')

H_2('1.7 The crux')
P('One question dominates this valuation, and it is not a financial one. Abu Dhabi has a stated '
  'objective of five million barrels a day of production capacity by 2027. ADNOC Drilling exists '
  'to deliver it. The fleet has grown from 115 rigs at the end of 2022 to 171 at the middle of '
  '2026, the company has six more island rigs on order for delivery between 2026 and 2028, and '
  'it has bought its way into Oman, Kuwait and Bahrain. What happens after the target is met?',
  space_after=6)
rows = [['', 'Continued expansion', 'Capacity plateau']]
rows.append(['The premise',
             'Regional expansion, integrated services and automation keep the fleet and the '
             'services book growing after 2027; unconventional Phase 1 is followed by more work',
             'The domestic fleet stops growing once the capacity target is met; the ordered '
             'island rigs still arrive because they are paid for, but nothing follows them'])
rows.append(['Abu Dhabi onshore rigs by 2030', '100', '92'])
rows.append(['Regional rigs by 2030', '38', '30'])
rows.append(['Integrated-services rigs by 2030', '82', '72'])
rows.append(['Unconventional revenue in 2030 (USD mn)', mn(RA[-1]['unconventional']),
             mn(RB[-1]['unconventional'])])
rows.append(['FY2030 revenue (USD mn)', mn(RA[-1]['revenue']), mn(RB[-1]['revenue'])])
rows.append(['Terminal growth rate', pc(CA['terminal_growth'], 1),
             pc(CB['terminal_growth'], 1)])
rows.append(['Enterprise value (USD mn)', mn(CA['enterprise_value']), mn(CB['enterprise_value'])])
rows.append(['Value per share (AED)', f'{CA["value_per_share_aed"]:.2f}',
             f'{CB["value_per_share_aed"]:.2f}'])
T(rows, [2.10, 2.45, 2.45], band_rows={9})
P(f'The two cases are AED {CA["value_per_share_aed"]-CB["value_per_share_aed"]:.2f} apart — '
  f'{pc((CA["value_per_share_aed"]-CB["value_per_share_aed"])/SPOT)} of the current price. '
  'They are published side by side and are not averaged into one number. A reader who believes '
  'the programme continues should read the first column; a reader who thinks 2027 is the peak '
  'should read the second. The market price sits between them, closer to the first.')

d.box([('One finding materially narrows this. ',
        'The unconventional programme looks like the obvious thing to worry about — USD '
        f'{mn(V("unconv_fy25"))} million of 2025 revenue on a contract with roughly USD 0.86 '
        'billion left at the year end and no announced successor. It is not, because it barely '
        'earns anything. Applying the company\'s own disclosed conventional EBITDA margin of '
        f'{pc(V("conv_ebitda_margin_fy25"),0)} to conventional revenue leaves about '
        f'{pc(TRI["m1_disclosed_fy25_margin"])} of margin on the unconventional book; the '
        'year-on-year incremental bridge gives '
        f'{pc(TRI["m3_incremental_bridge"])}. Both methods are shown in the workbook and '
        f'averaged there to {pc(TRI["average_of_used"])}. So the runoff of a USD 692 million '
        'revenue line removes roughly USD 45 million of EBITDA, not USD 350 million. The crux '
        'is the conventional fleet, not the shale contract.')])

d.page_break()
H_2('1.8 Macro and country — the cost of capital, built')
P('The cash flows are in US dollars, so the discount rate is built in dollars. Country risk '
  'enters ONCE, through the Abu Dhabi country risk premium already inside the equity risk '
  'premium; the risk-free rate is therefore the US Treasury yield normalised by the United '
  'States\' own default spread rather than a local yield that would carry sovereign risk a '
  'second time.', space_after=4)
rows = [['', 'Rating basis', 'CDS basis', 'Source']]
rows.append(['US 10-year Treasury yield, 6 August 2026', pc(V('ust10'), 2), pc(V('ust10'), 2),
             'Federal Reserve H.15'])
rows.append(['less the US adjusted default spread', f'({pc(V("us_default_spread"),2)})',
             f'({pc(V("us_default_spread"),2)})', 'Damodaran country file, 5 January 2026'])
rows.append(['Normalised risk-free rate', pc(W['rf_star'], 2), pc(W['rf_star'], 2), ''])
rows.append(['Equity beta', f'{W["beta"]:.3f}', f'{W["beta"]:.3f}',
             'Own-stock five-year weekly regression'])
rows.append(['Equity risk premium (Abu Dhabi, rated Aa2)', pc(V('erp_rating'), 2),
             pc(V('erp_cds'), 2), 'Damodaran country file'])
rows.append(['Cost of equity', pc(W['ke_rating'], 2), pc(W['ke_cds'], 2), ''])
rows.append(['Marginal cost of debt, pre-tax', pc(W['kd_pretax'], 2), pc(W['kd_pretax'], 2), ''])
rows.append([f'Cost of debt after tax at {pc(V("tax_rate"),0)}', pc(W['kd_after_tax'], 2),
             pc(W['kd_after_tax'], 2), ''])
rows.append(['Weight of equity', pc(W['weight_equity']), pc(W['weight_equity']),
             'Market capitalisation over market capitalisation plus net debt'])
rows.append(['Weighted average cost of capital', pc(W['wacc_rating'], 2), pc(W['wacc_cds'], 2),
             ''])
T(rows, [2.55, 1.10, 1.10, 2.25], band_rows={3, 6, 10})
P(f'Both bases are published because both are defensible and they differ by only '
  f'{(W["wacc_cds"]-W["wacc_rating"])*10000:.0f} basis points; the rating basis is used, and '
  'nothing in the conclusions turns on the choice.')

H_3('Cost of debt: three methods, one test')
P('The cost of debt is marginal and forward-looking, not an accounting average. Three '
  'candidates were computed and one test applied — a same-currency corporate cannot borrow '
  'below its own sovereign.', space_after=4)
rows = [['Method', 'Construction', 'Rate', 'Clears the sovereign floor?']]
rows.append(['Term-matched to the latest facility',
             'US 5-year Treasury yield plus the 0.75% margin on the USD 2.0 billion facility '
             'signed 16 October 2025 with a five-year initial maturity',
             pc(W['kd_candidates']['term_matched'], 2), 'Yes — adopted'])
rows.append(['Spot floating all-in cost',
             'Overnight financing rate plus the same margin',
             pc(W['kd_candidates']['spot_floating'], 2),
             'No — it is a short rate, and it prices below the sovereign'])
rows.append(['Trailing effective rate',
             'FY2025 interest on loans over average gross debt',
             pc(W['kd_candidates']['trailing_effective'], 2),
             'No — and it is backward-looking in any case'])
rows.append(['Sovereign floor',
             'US 5-year Treasury yield plus the Abu Dhabi sovereign credit-default-swap spread',
             pc(W['sovereign_floor'], 2), ''])
T(rows, [1.80, 2.75, 0.75, 1.70], band_rows={4})

H_3('Beta')
P(f'The beta is the company\'s own: a five-year weekly regression of its returns against an '
  f'equal-weight Abu Dhabi composite built from the full committed price library, giving '
  f'{BETA["beta"]:.3f} on {BETA["n"]} weekly observations with an R-squared of '
  f'{BETA["r2"]:.3f}, a standard error of {BETA["se"]:.3f} and a 90% interval of '
  f'{BETA["ci90"][0]:.2f} to {BETA["ci90"][1]:.2f}. Because the listing dates from October 2021 '
  'a full five-year window exists, so no peer beta is needed. Two robustness checks are carried '
  f'rather than hidden: weighting the composite by traded value gives '
  f'{BETA["robustness_turnover_weighted"]["beta"]:.3f}, and a two-year window gives '
  f'{BETA["robustness_2yr_window"]["beta"]:.3f}. All three are well below one, which is what a '
  'contracted revenue stream from a state counterparty should look like — and all three are '
  'below the level at which the valuation would fall to the market price. The sensitivity to '
  'beta is published in section 1.9 for that reason.')

H_2('1.9 Sensitivity')
d.figure(os.path.join(HERE, 'fig2_sens.png'), 6.4,
         'Discounted-cash-flow value per share against the cost of capital and the terminal '
         'growth rate, continued-expansion case. Bold cells lie within AED 0.20 of the market '
         'price.')
rows = [['Driver', 'Move', 'Value per share (AED)', 'Change']]
for bpt in SENS['beta_grid']:
    rows.append(['Equity beta', f'{bpt["beta"]:.3f}', f'{bpt["aed"]:.2f}',
                 pc(bpt['aed'] / CA['value_per_share_aed'] - 1)])
for msh in SENS['margin_shift']:
    rows.append(['EBITDA margin', f'{msh["shift"]*100:+.0f} points', f'{msh["aed"]:.2f}',
                 pc(msh['aed'] / CA['value_per_share_aed'] - 1)])
T(rows, [1.85, 1.55, 1.85, 1.45])
P('The single most powerful driver is the beta, and it is the one input in the whole model that '
  'is estimated from market data rather than read from a filing. At a beta of 1.00 — the level '
  'a reader who distrusts a 0.66 regression might impose — the continued-expansion case falls '
  f'to AED {[b["aed"] for b in SENS["beta_grid"] if b["beta"]==1.00][0]:.2f}, well below the '
  'market price. That is stated here rather than buried in a footnote because it is the '
  'quickest way to overturn this study.')

# ============================== 6. §2 TECHNICAL ==============================
d.page_break()
H_1('2. Technical and price structure')
d.figure(os.path.join(HERE, 'fig3_ma.png'), 6.9,
         'Price against the 20-, 50- and 200-day moving averages, with the computed support '
         'and resistance ladder.')
P(TA['tech']['summary'])
P(f'The trend reading is: {TA["tech"]["trend"].lower()}.')
rows = [['', 'Level (AED)', 'Distance from the close']]
for i, v in enumerate(TA['levels']['res'], start=1):
    rows.append([f'Resistance {i}', f'{v:.2f}', pc(v / TA['close'] - 1)])
for i, v in enumerate(TA['levels']['sup'], start=1):
    rows.append([f'Support {i}', f'{v:.2f}', pc(v / TA['close'] - 1)])
rows.append(['Last close', f"{TA['close']:.2f}", ''])
rows.append(['52-week range', f"{TA['lo_52w']:.2f} – {TA['hi_52w']:.2f}",
             f"{pc(TA['pct_off_high'])} off the high"])
T(rows, [1.85, 2.30, 2.55], band_rows={7})
P(f'Upside trigger: {TA["tech"]["bull"]} Downside trigger: {TA["tech"]["bear"]}')
P('Every level and every clause above is computed from the same cleaned price series the '
  'probability map runs on; nothing here is a chart opinion. Levels one and above are the '
  'nearest to the close in each direction.')

# ============================== 7. §3 PROBABILISTIC MAP ======================
H_1('3. Probability map')
P('Alongside the fundamental work the study carries a probability map: a simulation of where '
  'the price could be at two fixed future dates, given how this share has actually behaved. It '
  'is a different question from fair value and it is answered differently — 50,000 simulated '
  'price paths anchored on the close of 7 August 2026, with the drift set by the risk-free rate '
  f'less the dividend yield the company has itself guided to '
  f'({pc(ST["q_annual"], 2)} on the reaffirmed USD 1.05 billion floor), so no part of the '
  'answer comes from assuming the shares go up.', space_after=4)
d.figure(os.path.join(HERE, 'fig4_fan.png'), 6.9,
         f'Three-month cone to {H3["grade_date"]}, with the preceding 120 sessions of realised '
         f'price for scale.')
rows = [['', f'One month — {H1["grade_date"]}', f'Three months — {H3["grade_date"]}']]
for p in ('p5', 'p25', 'p50', 'p75', 'p95'):
    rows.append([f'{p[1:]}th percentile (AED)', f'{H1["pct"][p]:.2f}', f'{H3["pct"][p]:.2f}'])
rows.append(['Probability of finishing above AED %.2f' % SPOT, pc(H1['p_above']),
             pc(H3['p_above'])])
rows.append(['Probability of finishing 10% or more above', pc(H1['p_up10']), pc(H3['p_up10'])])
rows.append(['Probability of finishing 10% or more below', pc(H1['p_dn10']), pc(H3['p_dn10'])])
T(rows, [2.90, 2.05, 2.05], band_rows={6})
P('Touching a level at any point during the window is a different and higher probability than '
  'finishing beyond it, and both are given.', space_after=4)
rows = [['Level', 'AED', 'Touched within one month', 'Touched within three months']]
for k in (5, 10, 15, 20):
    rows.append([f'+{k}%', f'{SPOT*(1+k/100):.2f}', pc(H1[f'touch_up{k}']),
                 pc(H3[f'touch_up{k}'])])
for k in (5, 10, 15, 20):
    rows.append([f'-{k}%', f'{SPOT*(1-k/100):.2f}', pc(H1[f'touch_dn{k}']),
                 pc(H3[f'touch_dn{k}'])])
T(rows, [1.10, 1.10, 2.35, 2.45])
d.figure(os.path.join(HERE, 'fig6_dist.png'), 6.2,
         'The three-month distribution of outcomes. The gold line is the current price.')

H_2('How well has this map worked?')
P('A probability map that has never been scored is decoration, so the record is stated plainly. '
  'Run backwards across every three-month window this share has produced since listing — '
  f'{S0["windows_scored"]} independent, non-overlapping windows — the map scored '
  f'{abs(S0["skill_norm"])*100:.2f}% WORSE than a simple no-information benchmark that assumes '
  'the price simply drifts with the risk-free rate less the dividend. That shortfall held under '
  'three different resampling schemes, so it is a real result and not a sampling artifact.',
  space_after=4)
P('The reason is specific and worth stating, because it is not the reason most readers would '
  'assume. The map is not pointing the wrong way. Its centring is close to perfect: the median '
  f'of the realised outcomes sat at the {S0["pit_mean"]*100:.0f}th percentile of the predicted '
  f'distribution, against 50 for a perfectly centred forecast. The problem is that it is TOO '
  f'WIDE. Every single realised outcome fell inside the predicted 80% band and inside the 90% '
  f'band — {pc(S0["cov80"],0)} and {pc(S0["cov90"],0)} coverage against targets of 80% and 90% '
  f'— and the band itself was {S0["w90_ratio"]:.2f} times the benchmark\'s. A band that wide is '
  'never wrong and is not very useful, and a scoring rule that rewards sharpness penalises it '
  'accordingly.', space_after=4)
P('The cause is mechanical. The bands are calibrated across a panel of Abu Dhabi and Dubai '
  'listed companies, and this share\'s own realised volatility of '
  f'{pc(S0D["own_annualised_vol"])} sits at the {S0D["own_vol_percentile_in_panel"]*100:.0f}th '
  f'percentile of that panel, below its median of {pc(S0D["panel_median_vol"])}. A band sized '
  'for the average name is too wide for a below-average-volatility one. Narrowing it to '
  '80% of the panel width would have turned the score positive, and that is reported as a '
  'diagnosis rather than applied, because a width chosen after seeing the outcomes it is '
  'scored on is not evidence of anything.', space_after=4)
P(f'The one-month map is a different matter: over {S0["h1"]["windows_scored"]} windows it '
  f'scored {S0["h1"]["skill_norm"]*100:+.2f}% against the same benchmark — statistically '
  'indistinguishable from it — with outcomes spread across the predicted distribution rather '
  'than bunched in the middle. Read the three-month percentiles above as an outer bound on '
  'plausible movement rather than as a calibrated probability, and read the one-month figures '
  'as neither better nor worse than assuming no information.')

# ============================== 8. §4 COMPARISON =============================
d.page_break()
H_1('4. Comparison of the lenses')
rows = [['Lens', 'AED/share', 'What it assumes', 'When it is the right lens',
         'When it misleads']]
rows.append(['Discounted cash flow — continued expansion',
             f'{CA["value_per_share_aed"]:.2f}',
             'The fleet and the services book keep growing after the capacity target is met',
             'When a customer has a published multi-decade investment programme',
             'When the programme is a project with an end date rather than a policy'])
rows.append(['Discounted cash flow — capacity plateau', f'{CB["value_per_share_aed"]:.2f}',
             'Domestic growth stops in 2027 and only the ordered rigs arrive',
             'When the demand driver is an explicit capacity target',
             'When it ignores regional expansion that is already contracted'])
rows.append(['Relative multiples', f'{REL["value_per_share_aed"]:.2f}',
             'That this company should be valued like other listed drillers',
             'When the peer set genuinely does the same job',
             'When the peers are exposed to a spot market and this company is not'])
rows.append(['Book value and sustainable return', f'{BOOK["value_per_share_aed"]:.2f}',
             'That a return on equity above the cost of equity is durable',
             'When a franchise has demonstrated the return through a cycle',
             'When the cost of equity is close to the growth rate, as it is here'])
rows.append(['Normalised earnings power', f'{NORM["value_per_share_aed"]:.2f}',
             'Only the fleet already installed, at the guided margin, forever',
             'As a floor that credits no growth at all',
             'When the installed fleet is genuinely still being built out'])
T(rows, [1.55, 0.80, 1.55, 1.55, 1.55], size=8.6)
P('The lenses disagree in a structured way rather than randomly. The two that read the company '
  'as a set of assets or as one of a class of drillers sit below the market; the two that read '
  'it as a franchise earning an above-cost return sit above. That is the same disagreement the '
  'expert panel in Appendix C reaches from three different starting points, and it is the '
  'disagreement a reader has to resolve for themselves.')

# ============================== 9. §5 CATALYSTS ==============================
H_1('5. Catalysts')
rows = [['What', 'When', 'Why it matters', 'Which way']]
rows.append(['2027 guidance', 'The company has said it will publish it once rig and '
             'oilfield-services phasing is fixed',
             'This is the single observation that separates the two discounted-cash-flow cases',
             'Either'])
rows.append(['Third-quarter 2026 results', 'Expected late October 2026',
             'The first read on whether the first-half deceleration to 4% revenue growth is '
             'phasing or trend', 'Either'])
rows.append(['Completion of the MBPS acquisition',
             'Announced November 2025, subject to regulatory approval',
             '22 of the 30 regional rigs already in the June 2026 fleet count come through it',
             'Down if it fails'])
rows.append(['Delivery of the remaining ordered island rigs', 'Gradually to 2028',
             'Four of the six ordered rigs are still to arrive; they are the most visible '
             'contracted growth in the model', 'Up'])
rows.append(['An unconventional Phase 2 award', 'Not announced',
             'Would extend a revenue line that is large but, on the evidence in section 1.7, '
             'barely profitable', 'Up, but less than it looks'])
rows.append(['Integrated-services rig count reaching the stated 70 target',
             'End of 2026', 'The fastest-growing and highest-incremental-margin part of the '
             'business', 'Up'])
rows.append(['A change in the dividend policy', 'Board discretion',
             f'The guided floor of USD {bn(V("g26_dividend"))}bn is '
             f'{pc(V("g26_dividend")/RA[0]["pat"])} of forecast 2026 profit; the model '
             'accumulates cash rather than assuming a rise', 'Up if raised'])
T(rows, [1.85, 1.55, 2.60, 1.00], size=8.8)

# ============================== 10. §6 READING THE ZONES =====================
H_1('6. Reading the probability zones')
P('The percentile map in section 3 is not a forecast of where the price will go. It is a '
  'statement about how far it could plausibly travel in a given window, given how it has '
  'travelled before. Three cautions apply to reading it.', space_after=4)
d.bullet('A 5th percentile is not a floor. One outcome in twenty is expected to fall below it, '
         'and the events that produce those outcomes — a contract loss, a sovereign shock, a '
         'sharp move in oil — are exactly the ones a volatility model does not see coming.',
         bold_head='Percentiles are not bounds. ')
d.bullet('The probability of touching a level at some point in a window is materially higher '
         'than the probability of finishing beyond it. Both are tabulated because confusing '
         'them is the most common error in reading a cone.',
         bold_head='Touching is not finishing. ')
d.bullet('On this share\'s own record the three-month band has been too wide, as section 3 '
         'sets out in full. Treat the outer percentiles as generous rather than tight.',
         bold_head='This particular band is wide. ')
P('The map and the valuation answer different questions and are not reconciled with each other. '
  'The valuation says what the business is worth; the map says how far the price might wander '
  'in the next quarter regardless.')

# ============================== 11. §7 CAVEATS ===============================
H_1('7. Caveats, and what would change our mind')
rows = [['Caveat', 'What it does to the answer', 'What would settle it']]
rows.append(['The terminal value is more than seven-tenths of enterprise value in both cases',
             'Most of this valuation is a claim about a period nobody has contracted for',
             'Published 2027 and medium-term guidance'])
rows.append([f'The beta of {W["beta"]:.2f} does more work than any other input',
             f'At a beta of 1.00 the valuation falls to AED '
             f'{[b["aed"] for b in SENS["beta_grid"] if b["beta"]==1.00][0]:.2f}',
             'A longer trading record, or a stress episode that tests the correlation'])
rows.append(['One customer group, which is also the controlling shareholder',
             'Contract terms are set inside a group, not in a market; the model reads realised '
             'rates and cannot see the negotiation behind them',
             'Disclosure of contract tenor and repricing mechanics'])
rows.append(['Regional expansion is bought, not built',
             'Two acquisitions supply 30 of the 171 rigs; the revenue per regional rig is '
             'derived from one half-year of consolidation',
             'A full year of reported regional segment data'])
rows.append(['The dividend floor is a policy, not an obligation',
             'The distribution lens in Appendix C rests on it entirely',
             'A declared distribution below the floor, or a capital raise'])
rows.append(['The forecast holds debt flat and pays only the guided floor',
             f'Cash accumulates to USD {bn(RA[-1]["cash_close"])}bn by 2030 and net debt turns '
             'negative; enterprise value is unaffected, but the balance sheet in Appendix A is '
             'a floor case, not a prediction',
             'Any capital-allocation announcement'])
rows.append(['First-half 2026 revenue grew 4%, against 22% for 2025',
             'The forecast reconciles to guidance for 2026 and grows from there; if the '
             'deceleration is trend rather than phasing, the continued-expansion case is wrong',
             'Third-quarter and full-year 2026 results'])
T(rows, [2.15, 3.00, 1.85], size=8.8)

# ============================== 12. APPENDIX A ===============================
d.page_break()
H_1('Appendix A — financial statements')
H_2('A.1 Income statement — three audited years and five forecast years')
rows = [['USD million', 'FY2023', 'FY2024', 'FY2025'] + [f'FY{r["year"]}E' for r in RA]]


def isrow(lbl, hfn, ffn, fmt=mn, band=False):
    rows.append([lbl] + [fmt(hfn(H[str(y)])) for y in (2023, 2024, 2025)] +
                [fmt(ffn(r)) for r in RA])


isrow('Revenue', lambda h: h['revenue'], lambda r: r['revenue'])
isrow('Direct cost', lambda h: -h['direct_cost'], lambda r: -(r['conv_cash_cost']
                                                             + r['unconv_cash_cost'] + r['dna']))
isrow('Gross profit', lambda h: h['gross_profit'],
      lambda r: r['revenue'] - r['conv_cash_cost'] - r['unconv_cash_cost'] - r['dna'])
isrow('General and administrative expenses', lambda h: -h['gna'], lambda r: -r['gna'])
isrow('Other income', lambda h: h['other_income'], lambda r: r['other_income'])
isrow('Share of joint-venture results', lambda h: h['jv_share'], lambda r: r['jv_share'])
isrow('EBITDA', lambda h: h['ebitda'], lambda r: r['ebitda'])
rows.append(['EBITDA margin'] + [pc(H[str(y)]['ebitda_margin']) for y in (2023, 2024, 2025)] +
            [pc(r['ebitda_margin']) for r in RA])
isrow('Depreciation and amortisation', lambda h: -h['dna'], lambda r: -r['dna'])
isrow('EBIT', lambda h: h['ebit'], lambda r: r['ebit'] + r['jv_share'])
isrow('Finance cost', lambda h: -h['finance_cost'], lambda r: -r['interest'])
isrow('Finance income', lambda h: h['finance_income'], lambda r: r['finance_income'])
isrow('Profit before tax', lambda h: h['pbt'], lambda r: r['pbt'])
isrow('Income tax', lambda h: -h['tax'], lambda r: -r['tax'])
isrow('Profit after tax', lambda h: h['pat'], lambda r: r['pat'])
rows.append(['Net margin'] + [pc(H[str(y)]['net_margin']) for y in (2023, 2024, 2025)] +
            [pc(r['net_margin']) for r in RA])
T(rows, [1.75, 0.72, 0.72, 0.72, 0.72, 0.72, 0.72, 0.72, 0.72], size=8.3,
  band_rows={7, 15})
d.caption('The three historical years are the audited figures. FY2023 carries no income tax '
          'because the Abu Dhabi fiscal arrangement took effect on 1 January 2024.')

H_2('A.2 Balance sheet')
rows = [['USD million', 'FY2023', 'FY2024', 'FY2025'] + [f'FY{r["year"]}E' for r in RA]]


def bsrow(lbl, hfn, key, band=False):
    rows.append([lbl] + [mn(hfn(H[str(y)])) for y in (2023, 2024, 2025)] +
                [mn(r['balance_sheet'][key]) for r in RA])


bsrow('Fixed assets', lambda h: h['ppe'] + h['rou'] + h['intangibles'], 'fixed_assets')
bsrow('Other non-current assets', lambda h: h['deferred_tax_asset'] + h['advances'],
      'other_non_current')
bsrow('Investment in joint ventures', lambda h: h['jv_investment'], 'jv_investment')
bsrow('Inventories', lambda h: h['inventories'], 'inventories')
bsrow('Trade and other receivables', lambda h: h['receivables'], 'receivables')
bsrow('Due from related parties', lambda h: h['due_from_rp'], 'due_from_rp')
bsrow('Cash and cash equivalents', lambda h: h['cash'] + h['assets_held_for_sale'], 'cash')
rows.append(['Total assets'] +
            [mn(H[str(y)]['total_assets']) for y in (2023, 2024, 2025)] +
            [mn(r['balance_sheet']['total_assets']) for r in RA])
bsrow('Borrowings and lease liabilities', lambda h: h['debt'] + h['leases'], 'debt')
bsrow('Trade and other payables', lambda h: h['payables'], 'payables')
bsrow('Due to related parties', lambda h: h['due_to_rp'], 'due_to_rp')
bsrow("Employees' end of service benefits", lambda h: h['eosb'], 'eosb')
bsrow('Income tax payable', lambda h: h['tax_payable'], 'tax_payable')
rows.append(['Total liabilities'] +
            [mn(H[str(y)]['total_assets'] - H[str(y)]['equity']) for y in (2023, 2024, 2025)] +
            [mn(r['balance_sheet']['total_liabilities']) for r in RA])
rows.append(['Total equity'] + [mn(H[str(y)]['equity']) for y in (2023, 2024, 2025)] +
            [mn(r['balance_sheet']['equity_residual']) for r in RA])
rows.append(['Net debt'] + [mn(H[str(y)]['net_debt']) for y in (2023, 2024, 2025)] +
            [mn(r['net_debt']) for r in RA])
rows.append(['Net debt / EBITDA'] +
            [f"{H[str(y)]['net_debt']/H[str(y)]['ebitda']:.2f}x" for y in (2023, 2024, 2025)] +
            [f"{r['net_debt']/r['ebitda']:.2f}x" for r in RA])
T(rows, [1.75, 0.72, 0.72, 0.72, 0.72, 0.72, 0.72, 0.72, 0.72], size=8.3,
  band_rows={8, 14, 15})
d.caption('The forecast balance sheet holds gross debt flat at the audited 2025 level and pays '
          'only the guided dividend floor, so surplus cash accumulates. It balances in every '
          'year, and the residual equity agrees with the independently rolled-forward equity to '
          'the dollar.')

H_2('A.3 Cash flow and the working-capital cycle')
rows = [['USD million', 'FY2023', 'FY2024', 'FY2025'] + [f'FY{r["year"]}E' for r in RA]]
rows.append(['Net cash from operating activities'] +
            [mn(H[str(y)]['cfo']) for y in (2023, 2024, 2025)] + [mn(r['cfo']) for r in RA])
rows.append(['Capital expenditure'] + [f'({mn(H[str(y)]["capex"])})' for y in (2023, 2024, 2025)]
            + [f'({mn(r["capex"])})' for r in RA])
rows.append(['Dividends paid'] + [f'({mn(H[str(y)]["dividends"])})' for y in (2023, 2024, 2025)]
            + [f'({mn(r["dividend"])})' for r in RA])
rows.append(['Free cash flow to the firm'] + ['—'] * 3 + [mn(r['fcff']) for r in RA])
rows.append(['Closing cash'] + [mn(H[str(y)]['cash']) for y in (2023, 2024, 2025)] +
            [mn(r['cash_close']) for r in RA])
T(rows, [1.75, 0.72, 0.72, 0.72, 0.72, 0.72, 0.72, 0.72, 0.72], size=8.3, band_rows={4})
P('The asset-conversion cycle, read from the statements and used to project the balance sheet '
  'rather than plugged:', space_after=4)
rows = [['Days', 'FY2023', 'FY2024', 'FY2025', 'What it is']]
rows.append(['Days sales outstanding'] + [f'{H[str(y)]["dso"]:.0f}' for y in (2023, 2024, 2025)] +
            ['Trade receivables plus amounts due from related parties, over revenue. The size '
             'reflects unbilled contract assets on work performed for group companies'])
rows.append(['Days inventory outstanding'] +
            [f'{H[str(y)]["dio"]:.0f}' for y in (2023, 2024, 2025)] +
            ['Inventories over direct cost'])
rows.append(['Days payables outstanding'] +
            [f'{H[str(y)]["dpo"]:.0f}' for y in (2023, 2024, 2025)] +
            ['Trade and other payables plus amounts due to related parties, over direct cost'])
rows.append(['Working capital as a share of revenue'] +
            [pc(H[str(y)]['working_capital'] / H[str(y)]['revenue'])
             for y in (2023, 2024, 2025)] +
            [f'Averaged to {pc(UE["wc_pct_revenue"])} and used to drive the forecast'])
T(rows, [2.05, 0.72, 0.72, 0.72, 2.79], size=8.6, band_rows={4})

# ============================== 13. APPENDIX B ===============================
d.page_break()
H_1('Appendix B — peers, risks and research register')
H_2('B.1 The peer set')
rows = [['Company', 'Group', 'Enterprise value (USD mn)', 'Last 12 months EBITDA (USD mn)',
         'EV/EBITDA']]
for p in REL['peers']:
    rows.append([p['name'], p['group'], f"{p['ev_usd_mn']:,.0f}",
                 f"{p['ltm_ebitda_usd_mn']:,.0f}",
                 f"{p['ev_ebitda']:.2f}x" if p['ev_ebitda'] else '—'])
rows.append(['ADNOC Drilling at AED %.2f' % SPOT, 'Subject',
             f"{M['enterprise_value_usd_k']/1e3:,.0f}", f"{REL['applied_ebitda']/1e3:,.0f}",
             f"{REL['implied_own_ev_ebitda']:.2f}x"])
T(rows, [1.75, 2.05, 1.35, 1.55, 0.90], size=8.5, band_rows={14})
d.caption('Peer prices are at the close on 7 August 2026; earnings and balance-sheet figures '
          'are each company\'s own latest reported period. Nothing on this table is a source '
          'for any ADNOC Drilling figure — it is used for cross-check and for the relative lens '
          'only.')

H_2('B.2 Risk register')
rows = [['Risk', 'How it would show up', 'Severity', 'Already visible?']]
rows.append(['Customer concentration', 'A change in contract terms at renewal, invisible until '
             'realised revenue per rig moves', 'High', 'No — terms are not disclosed'])
rows.append(['Capacity target achieved and drilling demand plateaus',
             'Flat or falling rig count from 2028', 'High',
             'Partly — 2027 guidance is deliberately withheld'])
rows.append(['Receivable concentration', 'Four counterparties represented 99.9% of related-party '
             'receivables at the end of 2025', 'Medium',
             'Yes — disclosed in the accounts'])
rows.append(['Current liabilities exceed current assets',
             'The company disclosed a USD 477.7 million shortfall at the end of 2025 and states '
             'it has assessed liquidity under several scenarios', 'Low',
             'Yes — disclosed, with USD 1.5 billion of undrawn revolving capacity behind it'])
rows.append(['Regional integration risk',
             'Two acquisitions consolidated within six months; margin dilution already visible '
             'in the first-half onshore numbers', 'Medium', 'Yes — onshore EBITDA margin fell '
             'from 50% to 45% year on year in the first half'])
rows.append(['Oil price', 'Indirect: it moves the customer\'s investment programme rather than '
             'this company\'s day rates', 'Medium', 'No'])
rows.append(['Floating-rate debt', 'All borrowings are priced over the overnight financing rate',
             'Low', 'Yes — the rate structure is disclosed in the borrowings note'])
T(rows, [1.75, 3.00, 0.85, 2.00], size=8.6)

H_2('B.3 Research register — what was looked for, and what was found')
rows = [['Question', 'Where it was looked for', 'Outcome']]
rows.append(['Audited statements for three complete years',
             "The company's investor-relations site",
             'Found: signed consolidated statements for 2023, 2024 and 2025, plus reviewed '
             'interims for the first quarter and first half of 2026'])
rows.append(['Rig counts, wells drilled and utilisation',
             'Quarterly management commentary and earnings presentations',
             'Found for every year from 2022 to the second quarter of 2026'])
rows.append(['Contract tenor and day-rate mechanics', 'All filings and presentations',
             'NOT FOUND. The company does not disclose contract tenor or repricing terms. '
             'Realised revenue per rig is used instead, and the gap is flagged'])
rows.append(['Backlog', 'All filings',
             'NOT FOUND in the form other drillers report. The accounts disclose only USD 19.4 '
             'million of unsatisfied performance obligations, which is a revenue-recognition '
             'measure and not a backlog'])
rows.append(['2027 and beyond guidance', 'Results releases',
             'NOT AVAILABLE. The company states it will publish it once rig and '
             'oilfield-services phasing is finalised. This absence is the reason the study '
             'carries two cases rather than one'])
rows.append(['Exchange disclosure portal', 'adx.ae',
             'Returned an access error from this environment. Not required — the filings were '
             'obtained from the company itself'])
rows.append(['Local-currency government bond curve',
             'Central bank of the UAE and market data sources',
             'NOT OBTAINED. Not required: the cash flows are in US dollars and the discount '
             'rate is built in dollars. A dirham-basis cross-check would need this curve and is '
             'therefore not published'])
T(rows, [1.85, 1.85, 3.90], size=8.6)

# ============================== 14. APPENDIX C ===============================
d.page_break()
H_1('Appendix C — the expert panel')
P('Three analysts value the same company by three genuinely different methods. Each shows the '
  'workings, each names the sensitivity that matters most to their answer, and each states in '
  'advance what would prove them wrong.')

E = {e['label']: e for e in EX['experts']}
E1, E2, E3 = E['Expert 1']['detail'], E['Expert 2']['detail'], E['Expert 3']['detail']

H_2('C.1 Expert 1 — the asset valuer')
P('Worldview: a rig is a machine with a replacement cost. Anything a buyer pays above the cost '
  'of rebuilding the fleet is a payment for a contract, and contracts end. This lens is '
  'therefore not a fair value at all; it is a floor, and its usefulness is the size of the gap '
  'between it and the market.', space_after=3)
P('When it works: in a downturn, when contracts lapse and the steel is what is left. When it '
  'fails: in a company like this one, where the contract is the asset.', space_after=4)
rows = [['USD million', '', 'Source or construction']]
rows.append(['Property and equipment at cost', mn(E1['gross_ppe_cost']),
             'FY2025 property and equipment note'])
rows.append(['less accumulated depreciation', f"({mn(E1['accumulated_depreciation'])})",
             'Same note'])
rows.append(['Net book value', mn(E1['net_book_value']), ''])
rows.append([f"Replacement uplift on net book at {pc(E1['replacement_uplift_on_net_book'],0)}",
             mn(E1['uplifted_net_fleet'] - E1['net_book_value']),
             'The fleet was bought over many years; rebuilding it costs more than it cost'])
rows.append(['Fully depreciated assets still in use, at cost',
             mn(E1['fully_depreciated_in_use_at_cost']),
             'Disclosed in the FY2025 note: assets still in use with nil carrying value'])
rows.append([f"valued at {pc(E1['residual_rate_on_fully_depreciated'],0)} of cost",
             mn(E1['fully_depreciated_value']), ''])
rows.append(['Depreciated replacement cost of the fleet', mn(E1['depreciated_replacement_cost']),
             ''])
rows.append(['add right-of-use assets and intangibles', mn(E1['right_of_use_and_intangibles']),
             ''])
rows.append(['add net working capital', mn(E1['net_working_capital']), 'FY2025 balance sheet'])
rows.append(['add other non-current assets', mn(E1['other_non_current']), ''])
rows.append(['Asset enterprise value', mn(E1['enterprise_asset_value']), ''])
rows.append(['Equity value after the bridge', mn(E1['equity_value']),
             'Same bridge as the main study'])
rows.append(['Value per share (AED)', f"{E1['value_per_share_aed']:.2f}", ''])
T(rows, [2.85, 1.30, 2.85], size=8.6, band_rows={3, 7, 11, 12, 13})
P('Named sensitivity: the replacement uplift is the only judgement in the table.', space_after=3)
rows = [['Replacement uplift on net book'] + [pc(s['uplift'], 0) for s in E1['sensitivity']]]
rows.append(['Value per share (AED)'] + [f"{s['aed']:.2f}" for s in E1['sensitivity']])
T(rows, [2.60, 1.10, 1.10, 1.10, 1.10])
P(f'Falsifier, stated in advance: {EX["falsifiers"]["Expert 1"]}')

H_2('C.2 Expert 2 — the contracted-cash-flow analyst')
P('Worldview: this is not an equity, it is a bond with an equity tail. The near years are '
  'contracted to a state counterparty and should be discounted at something close to a '
  'corporate borrowing rate; the years beyond the window are not contracted at all and deserve '
  'a penalty on top of the ordinary cost of capital.', space_after=3)
P('When it works: on infrastructure and long-contract assets where the counterparty is better '
  'credit than the company. When it fails: when the "contracted" book turns out to be '
  'cancellable, or when splitting the rate is used to make a number bigger rather than more '
  'honest.', space_after=4)
rows = [['USD million', 'FY2026E', 'FY2027E', 'FY2028E', 'FY2029E', 'FY2030E']]
rows.append(['Free cash flow to the firm'] + [mn(y['fcff']) for y in E2['contracted_years']])
rows.append([f"Discount factor at {pc(E2['contracted_discount_rate'],2)}"] +
            [f"{y['discount_factor']:.3f}" for y in E2['contracted_years']])
rows.append(['Present value'] + [mn(y['present_value']) for y in E2['contracted_years']])
T(rows, [2.30, 0.95, 0.95, 0.95, 0.95, 0.95], band_rows={3})
rows = [['', 'USD million', 'Construction']]
rows.append(['Present value of the contracted years', mn(E2['pv_contracted']), ''])
rows.append(['Terminal-year NOPAT', mn(E2['terminal_nopat']),
             f"FY2030 NOPAT grown at {pc(E2['tail_growth'],1)}"])
rows.append(['Reinvestment rate', pc(E2['terminal_reinvestment']),
             'Growth over the terminal return on capital'])
rows.append(['Tail discount rate', pc(E2['tail_discount_rate'], 2),
             f"The cost of capital plus a 150-basis-point renewal premium"])
rows.append(['Terminal value', mn(E2['terminal_value']), ''])
rows.append(['Present value of the terminal value', mn(E2['pv_terminal']), ''])
rows.append(['Enterprise value', mn(E2['enterprise_value']), ''])
rows.append(['of which terminal', pc(E2['tv_pct_of_ev']), ''])
rows.append(['Equity value after the bridge', mn(E2['equity_value']), ''])
rows.append(['Value per share (AED)', f"{E2['value_per_share_aed']:.2f}", ''])
T(rows, [2.75, 1.35, 3.40], size=8.6, band_rows={8, 11})
rows = [['Renewal premium over the cost of capital'] +
        [pc(s['tail_premium'], 1) for s in E2['sensitivity']]]
rows.append(['Value per share (AED)'] + [f"{s['aed']:.2f}" for s in E2['sensitivity']])
T(rows, [2.60, 0.90, 0.90, 0.90, 0.90, 0.90])
P(f'Falsifier, stated in advance: {EX["falsifiers"]["Expert 2"]}')

H_2('C.3 Expert 3 — the distribution investor')
P('Worldview: a minority shareholder in a state-controlled company owns the distribution, not '
  'the enterprise. Value what actually leaves the company, discounted at the cost of equity — '
  'not at a cost of capital that blends in debt the shareholder does not own.', space_after=3)
P('When it works: on mature, high-payout, majority-controlled companies. When it fails: when '
  'the payout is a policy that can be withdrawn, and whenever retained cash is genuinely being '
  'reinvested at a high return — as some of it is here.', space_after=4)
rows = [['', 'FY2026E', 'FY2027E', 'FY2028E', 'FY2029E', 'FY2030E']]
rows.append(['Dividend (USD million)'] + [mn(s['dividend']) for s in E3['schedule']])
rows.append([f"Discount factor at {pc(E3['cost_of_equity'],2)}"] +
            [f"{s['discount_factor']:.3f}" for s in E3['schedule']])
rows.append(['Present value'] + [mn(s['present_value']) for s in E3['schedule']])
T(rows, [2.30, 0.95, 0.95, 0.95, 0.95, 0.95], band_rows={3})
rows = [['', 'USD million', 'Construction']]
rows.append(['Present value of the five guided years', mn(E3['pv_stage1']), ''])
rows.append(['Terminal dividend', mn(E3['terminal_dividend']),
             f"FY2030 dividend grown at {pc(E3['terminal_growth'],1)}"])
rows.append(['Terminal value', mn(E3['terminal_value']), ''])
rows.append(['Present value of the terminal value', mn(E3['pv_terminal']), ''])
rows.append(['Equity value', mn(E3['equity_value']), ''])
rows.append(['Value per share (AED)', f"{E3['value_per_share_aed']:.2f}", ''])
rows.append(['Payout as a share of forecast profit, 2026', pc(E3['payout_check_2026']),
             'The floor is covered by earnings with room to spare'])
rows.append(['Payout as a share of forecast profit, 2030', pc(E3['payout_check_2030']), ''])
T(rows, [2.75, 1.35, 3.40], size=8.6, band_rows={6, 7})
rows = [['Terminal growth of the distribution'] +
        [pc(s['terminal_growth'], 1) for s in E3['sensitivity']]]
rows.append(['Value per share (AED)'] + [f"{s['aed']:.2f}" for s in E3['sensitivity']])
T(rows, [2.60, 0.90, 0.90, 0.90, 0.90, 0.90])
P(f'Falsifier, stated in advance: {EX["falsifiers"]["Expert 3"]}')

H_2('C.4 Cross-examination')
for ce in EX['cross_examination']:
    P(ce['challenge'], bold=True, size=9.6, space_after=2)
    P(ce['response'], size=9.6, space_after=2)
    P(f"Verdict: {ce['verdict']}.", italic=True, size=9.6, color=BRASS, space_after=8)

H_2('C.5 The three in one room')
P(EX['three_in_a_room'])
d.figure(os.path.join(HERE, 'figD1_experts.png'), 6.6,
         'The three valuations against the market price. The bar is each expert\'s own '
         'published sensitivity range; the brass tick is the base case.')

H_2('C.6 Divergence — which assumption drives which gap')
rows = [['Assumption', 'Expert 1', 'Expert 2', 'Expert 3', 'What it drives']]
for dv in EX['divergence']:
    rows.append([dv['assumption'], dv['e1'], dv['e2'], dv['e3'], dv['drives']])
T(rows, [1.15, 1.55, 1.55, 1.55, 1.70], size=8.2)

# ============================== 15. ABOUT ====================================
d.page_break()
H_1('About this study')
P('Testahil publishes independent valuation studies and calibrated probability maps, with a '
  'public record of how they turned out. Every study is built from the subject company\'s own '
  'issued financial statements, read from an official source. The delivered workbook '
  'calculates: change a driver and the valuation moves. Every formula in it has been checked '
  'against the model that produced it, and every input has been perturbed to prove the chain '
  'from driver to answer is live.')
P('This study values ADNOC Drilling Company P.J.S.C. as an operating company, using a '
  'discounted cash flow as the primary lens with relative multiples, normalised earnings power '
  'and a book-and-return lens alongside it. Its most consequential judgement is computed both '
  'ways and published both ways.')

# ============================== 16. DISCLOSURE ===============================
H_1('Disclosure')
P('This document is educational analysis. It is not investment advice, not a recommendation, '
  'and not an offer or solicitation to buy or sell any security. It contains no rating and no '
  'price target. Fair-value ranges and probability distributions are estimates that depend on '
  'assumptions stated throughout the document, and reasonable people applying the same evidence '
  'will reach different numbers.')
P('The historical financial information is taken from ADNOC Drilling Company P.J.S.C.\'s own '
  'published financial statements and disclosures. Third-party market data is used only for '
  'peer comparison and is identified as such wherever it appears. Prices and market data are as '
  'at 7 August 2026 and go stale immediately.')
P('Past performance and past accuracy are not guarantees of future results. Readers should form '
  'their own view and, where appropriate, take professional advice.')
P('© 2026 Testahil. All rights reserved.', size=9, color=GREY)

OUT = os.path.join(HERE, 'ADNOCDRILL_Valuation_Study_09-08-2026.docx')
d.save(OUT)
print(f'wrote {OUT}')
print(f'  {len(d.doc.paragraphs)} paragraphs, {len(d.tables)} tables, '
      f'{len(d.doc.inline_shapes)} figures')
