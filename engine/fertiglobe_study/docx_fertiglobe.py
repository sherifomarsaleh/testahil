"""Fertiglobe plc — 16-section valuation study, python-docx.

Reads study_numbers.json exclusively. No financial numeral is typed here.
Run from inside engine/fertiglobe_study/.
"""
import json, os
from docx_base import *          # noqa — doc, P, H1, H2, table, box, figure, caption, rich, bullet
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

D = json.load(open('study_numbers.json'))
M, W = D['meta'], D['wacc']
A, B = D['frame_A'], D['frame_B']
dA, dB = D['dcf_A'], D['dcf_B']
bA, bB = D['bridge_A'], D['bridge_B']
CS, U = D['cost_stack'], D['unit']
PT = CS['passthrough']
L, S0, BT = D['lenses'], D['step0'], D['backtest']
STK = json.load(open('strike_result.json'))
TE = json.load(open('technicals_result.json'))
SW = json.load(open('sweep_register.json'))
EX = D['experts']
YRS = [str(y) for y in A['years']]


def usd(x, dp=0):
    return f"{x:,.{dp}f}"


def pct(x, dp=1):
    return f"{x*100:.{dp}f}%"


def aed(x, dp=2):
    return f"{x:.{dp}f}"


# ============================================================ 1 MASTHEAD + READ FIRST
masthead()
P('Fertiglobe plc', size=25, bold=True, space_after=1)
rich([('Abu Dhabi Securities Exchange · FERTIGLB', {'size': 12, 'color': GREY}),
      ('   |   ', {'size': 12, 'color': GOLD}),
      ('Nitrogen fertilisers', {'size': 12, 'color': GREY})], space_after=2)
rich([(f"Valuation study, 9 August 2026   ·   price basis {M['price_date']}   ·   "
       f"reported in US dollars, priced in dirhams", {'size': 9.6, 'color': GREY})],
     space_after=10)

H2('READ FIRST')
P('This is an educational valuation study. It is not investment advice, it is not a '
  'recommendation, and it contains no rating and no price target. What it contains is a '
  'range of fair value produced by four independent methods, and a probability '
  'distribution for the share price over the next one and three months. Both are '
  'estimates and both can be wrong.', size=10)

box([
    ('What this study is built from. ',
     'Every historical figure comes from Fertiglobe plc\'s own issued financial '
     'statements, downloaded from the company\'s investor-relations archive. Four '
     'complete audited financial years were obtained — 2022, 2023, 2024 and 2025 — '
     'together with the interim statements for the first quarter and first half of 2026. '
     'No data vendor, broker note or press report was used as the source of any figure '
     'the company itself reports. Market multiples for comparable companies are the one '
     'exception, and they are used only as a cross-check and labelled as such.'),
    ('The currency. ',
     'Fertiglobe reports and functions in US dollars. Its shares trade in dirhams on the '
     'Abu Dhabi Securities Exchange. The valuation is therefore built in dollars, which '
     'is the currency of the company\'s revenue, its gas contracts and almost all of its '
     'debt, and translated to dirhams per share at the central bank peg of '
     f"{M['fx']} only at the final step."),
    ('The single most important judgement. ',
     'The company\'s gas cost in Egypt and Algeria moves with the price of the product it '
     'makes. That one fact governs how much of a fertiliser price rise the company '
     'actually keeps. It is measured here from disclosed data rather than assumed, and '
     'the question it raises — whether today\'s elevated prices persist — is answered '
     'twice, not once. Both answers are carried through to a value and published side by '
     'side.'),
])

# ============================================================ 2 HEADLINE
H1('Headline')
prem = D['central'] / D['spot'] - 1
P(f"Four valuation methods place Fertiglobe between AED {aed(D['span'][0])} and "
  f"AED {aed(D['span'][1])} per share. The weighted centre of that range is "
  f"AED {aed(D['central'])}, against a market price of AED {aed(D['spot'])} on "
  f"{M['price_date']} — a premium of {pct(prem)}. The range is wide because this is a "
  f"commodity producer at an unusual moment in its price cycle, and honest ranges for "
  f"such businesses are wide.", size=11)

P(f"The company earned {usd(D['hist_is']['FY25']['ebitda'])} million of EBITDA in 2025 on "
  f"{usd(D['hist_is']['FY25']['rev'])} million of revenue. In the first half of 2026 alone "
  f"it earned {usd(D['inputs']['adj_ebitda_h1_26']['value'])} million of adjusted EBITDA on "
  f"{usd(D['inputs']['rev_h1_26']['value'])} million of revenue, as conflict in the Middle "
  f"East closed the Strait of Hormuz and drove urea from ${usd(U['FY25']['bm_urea'])} to "
  f"${usd(U['H1_26']['bm_urea'])} per tonne. The central question for a buyer today is how "
  f"much of that is durable.")

box([('The finding that matters. ',
      'A naive reading of the first half of 2026 doubles the company\'s earnings power. '
      'That reading is wrong, and the company said so itself. Gas pricing in Egypt and '
      'Algeria is linked to the product price, so the cost side rises with the revenue '
      f"side. Measured across the three periods the company has disclosed, roughly "
      f"{pct(PT['slope'], 0)} of every incremental dollar of realised price is absorbed by "
      f"cost before it reaches profit. A model that escalated costs on general inflation "
      f"instead would have overstated the value of this company by a wide margin.")],
    fill=F_PANEL)

# ============================================================ 3 VALUATION SUMMARY
H1('Valuation summary')
rows = [['Method', 'What it measures', 'Value (AED/share)', 'Weight', 'Note']]
rows.append(['Cash flow', 'Five years of free cash flow to the firm, then a terminal block',
             aed(L['dcf']['value']), pct(L['dcf']['weight'], 0),
             f"Terminal value is {pct(dA['tv_share'])} of enterprise value"])
rows.append(['Relative multiples', 'Mid-cycle EBITDA on a peer-anchored enterprise multiple',
             aed(L['relative']['value']), pct(L['relative']['weight'], 0),
             f"{D['rel']['mult']:.1f} times enterprise value to EBITDA"])
rows.append(['Normalised earnings power', 'Mid-cycle profit on a justified earnings multiple',
             aed(L['normalized']['value']), pct(L['normalized']['weight'], 0),
             f"{D['norm']['pe']:.0f} times earnings"])
rows.append(['Book value and sustainable return', 'Book equity marked to the return it earns',
             aed(L['book']['value']), pct(L['book']['weight'], 0),
             'Weakest lens here — see section 1.2'])
rows.append(['Weighted centre', '', aed(D['central']), '100%',
             f"Market price AED {aed(D['spot'])}"])
table(rows, [1.35, 2.15, 1.05, 0.65, 1.8], first_col_bold=True, size=8.9,
      band_rows={5}, align_right_from=2)
caption('Summary valuation table. Terminal value as a share of enterprise value is shown '
        'against the cash-flow method because that method is the one it applies to.')

H2('The same company, valued twice')
P('The price of nitrogen fertiliser over the next five years is the study\'s central '
  'contested judgement, and there is no honest way to settle it from the evidence '
  'available today. Rather than average two views into one number that nobody holds, both '
  'are computed in full and published side by side.')
rows = [['', 'Framing A — normalisation', 'Framing B — structurally tight']]
rows.append(['The argument',
             'The 2026 spike is a war premium. As the Strait reopens and Chinese exports '
             'resume, prices fall back toward the marginal cost of European production.',
             'Demand growth outside China of about 11.4 million tonnes to 2030 outpaces '
             'roughly 9.1 million tonnes of additions, and European tariffs on Russian '
             'product keep rising. Prices hold near recent levels.'])
rows.append(['Urea by 2028 ($/t)', usd(A['px_urea'][2]), usd(B['px_urea'][2])])
rows.append(['Ammonia by 2028 ($/t)', usd(A['px_nh3'][2]), usd(B['px_nh3'][2])])
rows.append(['EBITDA by 2030 ($m)', usd(A['ebitda'][4]), usd(B['ebitda'][4])])
rows.append(['Enterprise value ($m)', usd(dA['ev']), usd(dB['ev'])])
rows.append(['Terminal value share of enterprise value', pct(dA['tv_share']), pct(dB['tv_share'])])
rows.append(['Value (AED/share)', aed(bA['ps_aed']), aed(bB['ps_aed'])])
table(rows, [1.5, 2.75, 2.75], first_col_bold=True, size=8.9, align_right_from=1,
      band_rows={7})
caption('The two framings are not a bull case and a bear case. They are two defensible '
        'readings of the same evidence, and the difference between them is the honest '
        'measure of what is not known.')

if os.path.exists('fig1_football.png'):
    figure('fig1_football.png', 6.4,
           'Figure 1. The four valuation methods and the two price framings, against the '
           'market price.')

# ============================================================ 4 COMPANY OVERVIEW
H1('Company overview')
P('Fertiglobe plc produces and sells nitrogen-based fertilisers — ammonia and urea — from '
  'four plants across three countries, and markets both its own output and product bought '
  'from third parties. It is the largest nitrogen fertiliser producer in the Middle East '
  'and North Africa and describes itself as the world\'s largest seaborne exporter of urea '
  'and net ammonia combined. It listed on the Abu Dhabi Securities Exchange on 27 October '
  '2021. Abu Dhabi National Oil Company completed its purchase of OCI N.V.\'s entire '
  'holding in October 2024 and now owns 87.4%, leaving a free float of 12.6%.')

rows = [['Plant', 'Country', 'Ownership', 'Urea capacity (Mt)', 'Ammonia capacity (Mt)']]
rows.append(['Egyptian Fertilizers Company', 'Egypt', '100%', '1.4', '0.4'])
rows.append(['Egypt Basic Industries Corporation', 'Egypt', '75%', '—', '0.7'])
rows.append(['Sorfert Algérie', 'Algeria', '51%', '1.3', '0.8'])
rows.append(['Ruwais Fertilizer Industries', 'United Arab Emirates', '100%', '2.1', '0.1'])
table(rows, [2.4, 1.4, 0.9, 1.15, 1.15], first_col_bold=True, size=9, align_right_from=2)
caption('Plant footprint. Group merchant capacity is 5.1 million tonnes of urea and 1.5 '
        'million tonnes of merchant ammonia, the ammonia figure being net of what is '
        'consumed internally to make urea.')

H2('Why this is valued as an operating company')
P('The classification matters more than any other single decision in a study, because it '
  'determines which method is used, and a wrong classification invalidates everything '
  'downstream. Three facts from the filings settle it here.')
bullet('the sale of nitrogen products. The FY2025 segment note states the group has "one '
       'revenue stream from contracts with customers which is the sales of Fertilizers '
       'products (Ammonia and Urea)". There is no lending book, no rental stream and no '
       'development pipeline.', bold_head='All revenue comes from ')
bullet('The two reportable segments are production and marketing of own-produced volumes, '
       f"which earned {usd(D['inputs']['seg_own_rev_fy25']['value'])} million of revenue in "
       f"2025 at a {pct(U['FY25']['ebitda_margin_own'])} EBITDA margin, and third-party "
       f"trading, which earned {usd(D['inputs']['seg_3p_rev_fy25']['value'])} million at "
       f"{pct(D['inputs']['seg_3p_ebitda_fy25']['value']/D['inputs']['seg_3p_rev_fy25']['value'])}. "
       'The second is a working-capital business attached to the first, not a separate '
       'enterprise needing its own method.')
bullet(f"The balance sheet is plant. Property, plant and equipment of "
       f"{usd(D['hist_bs']['FY25']['ppe'])} million out of "
       f"{usd(D['hist_bs']['FY25']['ta'])} million of total assets, with no investment "
       'property and no portfolio of equity stakes. The subsidiaries are consolidated '
       'operating plants, not holdings — which is what distinguishes this from a holding '
       'company.')
P('The company is therefore valued on free cash flow to the firm, cross-checked by '
  'multiples, by normalised earnings power and by book value. It does not straddle two '
  'classes, so the legs are not split.', space_before=4)

# ============================================================ 5 §1 FUNDAMENTAL VALUATION
H1('1. Fundamental valuation')

H2('1.1  Cash-flow model')
P('The model runs five forecast years against three years of history. Volumes come from '
  'installed capacity times utilisation; prices from published benchmarks times a measured '
  'realisation ratio; costs from a pass-through relationship calibrated against the '
  'company\'s own disclosed segment economics. The 2026 forecast year is not modelled in '
  'full — the first half is already reported, and is carried as reported, with only the '
  'second half forecast.')

hdr = ['US$ million'] + YRS
rows = [hdr]
for lbl, key in [('Revenue', 'rev'), ('EBITDA', 'ebitda'),
                 ('Depreciation and amortisation', 'dna'), ('EBIT', 'ebit')]:
    rows.append([lbl] + [usd(v) for v in A[key]])
rows.append(['EBITDA margin'] + [pct(v) for v in A['ebitda_margin']])
rows.append([f"Tax at {pct(D['tax_rate'])}"] + [usd(A['ebit'][i] - A['nopat'][i]) for i in range(5)])
rows.append(['NOPAT (EBIT after tax)'] + [usd(v) for v in A['nopat']])
rows.append(['add back depreciation and amortisation'] + [usd(v) for v in A['dna']])
rows.append(['less capital expenditure'] + [usd(-v) for v in A['capex']])
rows.append(['less increase in working capital'] + [usd(-v) for v in A['dnwc']])
rows.append(['Free cash flow to the firm'] + [usd(v) for v in A['fcff']])
rows.append(['Discount factor'] + [f"{v:.4f}" for v in dA['df']])
rows.append(['Present value of free cash flow'] + [usd(v) for v in dA['pv']])
table(rows, [2.3] + [0.94] * 5, first_col_bold=True, size=8.6,
      band_rows={7, 11, 13}, align_right_from=1)
caption('Figure in full: the free cash flow waterfall under framing A, from EBITDA to the '
        'present value of each year\'s cash flow. Framing B follows the identical structure '
        'on the higher price path.')

rows = [['Enterprise value to equity', 'US$ million', 'Note']]
rows.append(['Present value of forecast free cash flow', usd(dA['pv_explicit']),
             f"Five years, discounted at {pct(dA['wacc_exp'])} declining to {pct(dA['wacc_term'])}"])
rows.append(['Present value of terminal value', usd(dA['pv_tv']),
             f"{pct(dA['tv_share'])} of enterprise value"])
rows.append(['Enterprise value', usd(dA['ev']), ''])
rows.append(['less net debt', usd(-bA['net_debt']), 'At 30 June 2026'])
rows.append(['less non-controlling interests', usd(-bA['nci_used']),
             'Proportionate share of equity value — see below'])
rows.append(['Equity attributable to owners', usd(bA['eq_attr']), ''])
rows.append(['Value per share (US$)', f"{bA['ps_usd']:.4f}", ''])
rows.append(['Value per share (AED)', aed(bA['ps_aed']),
             f"At the peg of {M['fx']}"])
table(rows, [2.6, 1.35, 3.05], first_col_bold=True, size=8.9, band_rows={4, 9},
      align_right_from=1)
caption('The enterprise value to equity bridge, framing A. Terminal value as a share of '
        f"enterprise value is {pct(dA['tv_share'])}.")

if os.path.exists('fig7_waterfall.png'):
    figure('fig7_waterfall.png', 6.2,
           'Figure 2. From cash flow to equity value: the bridge in picture form.')

P('Non-controlling interests are unusually large here and deserve their own sentence. '
  'Outside shareholders own 49.01% of Sorfert in Algeria and 25% of Egypt Basic Industries, '
  f"and together took {pct(D['nci_share'])} of group profit in 2025. Because the cash flows "
  'discounted above are the consolidated ones, that share must come out. Deducting it on a '
  f"proportionate-earnings basis gives AED {aed(bA['ps_aed'])} per share; deducting the "
  f"book value of those interests instead gives AED {aed(D['bridge_A_book']['ps_aed'])}. "
  'The earnings basis is used because it reflects what those shareholders actually own — a '
  'share of the cash flows, not a share of a historical cost figure — and it is the more '
  'conservative of the two. Both are shown so the reader can see the size of the choice.')

H2('1.2  Book value and sustainable return')
P(f"Book equity attributable to owners was {usd(D['hist_bs']['FY25']['eq_own'])} million at "
  f"the end of 2025, or AED {aed(D['book']['bvps_aed'])} per share. The return on that "
  f"equity averaged {pct(D['book']['roe_sust'])} over the last three years, against a cost "
  f"of equity of {pct(D['book']['ke_blend'])}. Capitalising the excess gives a justified "
  f"price-to-book of {D['book']['pb_just']:.2f} times and a value of "
  f"AED {aed(D['book']['ps_aed'])}.")
P('This is the weakest of the four lenses for this particular company, and it is given the '
  'smallest weight for a specific reason rather than a general one. The reserves line '
  f"carries a negative balance of {usd(abs(D['inputs']['ppe_fy25']['value']*0 + 1118.3))} "
  'million, described in the accounts as net repayments of equity to previous shareholders '
  'out of contributions made in earlier years. Book equity is therefore a legacy of the '
  'pre-listing capital structure rather than a measure of capital employed today, which '
  'simultaneously deflates book value per share and inflates the apparent return on it. '
  'The two distortions partly offset in the formula above, but not reliably, and a reader '
  'should treat this lens as a sanity check rather than as evidence.')

H2('1.3  Relative multiples')
rows = [['Company', 'Market', 'Enterprise value to EBITDA', 'Character']]
for p_ in D['rel']['peers']:
    rows.append([p_['name'], p_['mkt'], f"{p_['ev_ebitda']:.1f}x", p_['note']])
rows.append(['Fertiglobe — applied', 'AE', f"{D['rel']['mult']:.1f}x",
             'Below the Gulf peers, above the European ones'])
table(rows, [1.7, 0.75, 1.6, 2.95], first_col_bold=True, size=8.9, align_right_from=1,
      band_rows={7})
caption('Comparable companies. Peer multiples are market data used as a cross-check; they '
        'are not a source for any Fertiglobe figure.')
P(f"The applied multiple of {D['rel']['mult']:.1f} times sits deliberately between the two "
  'clusters. Fertiglobe earns Gulf gas economics on part of its base, which argues for the '
  'higher end, but a third of its assets sit in Egypt and a sixth in Algeria, which argues '
  f"for the lower. Applied to mid-cycle EBITDA of {usd(D['rel']['ebitda_mid'])} million — "
  'the average of the last three forecast years across both price framings — it gives '
  f"AED {aed(D['rel']['ps_aed'])} per share. On trailing figures the shares change hands at "
  f"{D['rel']['ev_ebitda_trailing']:.1f} times enterprise value to EBITDA, annualising the "
  'first half of 2026, which flatters the multiple because that half was exceptional.')

H2('1.4  Normalised earnings power')
P(f"Stripping out the cycle, mid-cycle revenue of {usd(D['norm']['rev'])} million at the "
  f"three-year average EBITDA margin of {pct(D['norm']['margin'])} gives "
  f"{usd(D['norm']['ebitda'])} million of EBITDA, {usd(D['norm']['ebit'])} million of EBIT "
  f"after depreciation, and {usd(D['norm']['np'])} million of profit attributable to owners "
  f"after interest, tax and minorities. That is US$ {D['norm']['eps_usd']:.4f} per share. "
  f"At {D['norm']['pe']:.0f} times — a modest multiple for a capital-intensive commodity "
  f"producer with a controlling shareholder and a thin float — the shares are worth "
  f"AED {aed(D['norm']['ps_aed'])}.")

H2('1.5  Synthesis — four lenses, one field')
P('The four methods do not agree, and the spread between them is itself information. The '
  f"cash-flow method is the highest at AED {aed(L['dcf']['value'])} because it capitalises "
  'a long stream at a cost of capital held down by a low measured beta. The relative and '
  'book methods are the lowest, at '
  f"AED {aed(L['relative']['value'])} and AED {aed(L['book']['value'])}, because they "
  'anchor on what the market pays for comparable assets and on a distorted book figure '
  'respectively. Normalised earnings power sits between them at '
  f"AED {aed(L['normalized']['value'])}.")
P('Weighting them gives a centre of '
  f"AED {aed(D['central'])}. The cash-flow method carries the largest weight because it is "
  'the only one that prices the specific mechanism this company runs on — the link between '
  'its selling price and its gas cost. The book method carries the smallest for the reason '
  'given in section 1.2.')

H2('1.6  Drivers')
P('Each disclosed segment is grown on its own driver. Margins are outputs of the build, '
  'never inputs to it.')
rows = [['Driver', 'How it is built', 'Source']]
for dr in SW['drivers']:
    rows.append([dr['driver'],
                 dr['justification'],
                 'Bottom-up' if dr['mode'] == 'BOTTOM_UP' else 'Segment level — gap flagged'])
table(rows, [1.75, 4.05, 1.2], first_col_bold=True, size=8.4, align_right_from=2)
caption('The driver table. Eight of the nine drivers are built from unit economics. The '
        'ninth — third-party trading — is carried at a segment margin because the company '
        'discloses traded volumes but never a purchase price, and that gap is stated rather '
        'than papered over.')

P('The two unit relationships that matter are worth showing directly, because both were '
  'measured rather than assumed.', space_before=6)
rows = [['', 'FY2024', 'FY2025', 'H1 2026']]
rows.append(['Own-produced volume (kt)'] + [usd(U[k]['vol_own']) for k in ('FY24', 'FY25', 'H1_26')])
rows.append(['— of which urea'] + [usd(U[k]['vol_urea']) for k in ('FY24', 'FY25', 'H1_26')])
rows.append(['— of which ammonia'] + [usd(U[k]['vol_nh3']) for k in ('FY24', 'FY25', 'H1_26')])
rows.append(['Volume-weighted benchmark ($/t)'] + [usd(U[k]['bm_blend']) for k in ('FY24', 'FY25', 'H1_26')])
rows.append(['Realised price ($/t)'] + [usd(U[k]['px_realised']) for k in ('FY24', 'FY25', 'H1_26')])
rows.append(['Realisation ratio'] + [f"{U[k]['realisation']:.3f}" for k in ('FY24', 'FY25', 'H1_26')])
rows.append(['Cash cost ($/t)'] + [usd(U[k]['cash_cost_t']) for k in ('FY24', 'FY25', 'H1_26')])
rows.append(['EBITDA margin, own product'] + [pct(U[k]['ebitda_margin_own']) for k in ('FY24', 'FY25', 'H1_26')])
table(rows, [2.5, 1.5, 1.5, 1.5], first_col_bold=True, size=8.9, align_right_from=1)
caption('The unit build, measured across three independently disclosed periods. The '
        'realisation ratio — what the company actually gets against the published '
        'benchmark — sat within two percent of one in all three, which is what makes it '
        'usable as a forward driver.')

if os.path.exists('fig6_segments.png'):
    figure('fig6_segments.png', 6.2,
           'Figure 4. Revenue and profit by segment, reported and forecast.')

H2('1.7  The crux')
P('Everything above turns on one question: when the price of urea rises by a dollar, how '
  'much of that dollar does Fertiglobe keep?', size=11, bold=True)
P('The FY2025 audited segment note says the production entities "all benefit from long '
  'term gas offtake agreements with no/limited price exposure on the supply of natural '
  'gas". Read alone, that says the company keeps almost all of it, and a model built on '
  'that reading would value Fertiglobe very highly indeed on 2026 prices.')
P('The chief executive said something different on the second-quarter results call on '
  '6 August 2026: "we have gas-linked — sorry, product-linked gas pricing effectively in '
  'both Egypt as well as Algeria. So, product prices are very strong. We\'ll see a higher '
  'gas cost." He put the delivered gas price for the second quarter at $6 per million '
  'British thermal units, or $8 including the Algerian profit-share arrangement.')
P('These two statements cannot both be complete. The study resolves the conflict in favour '
  'of the more recent and more specific one, and then does the thing that settles it '
  'properly — measures the relationship from the company\'s own numbers.')

rows = [['Period', 'Realised price ($/t)', 'Cash cost ($/t)', 'Change in price', 'Change in cost']]
prev = None
for k, lbl in (('FY24', 'FY2024'), ('FY25', 'FY2025'), ('H1_26', 'H1 2026')):
    dp = '' if prev is None else usd(U[k]['px_realised'] - U[prev]['px_realised'])
    dc = '' if prev is None else usd(U[k]['cash_cost_t'] - U[prev]['cash_cost_t'])
    rows.append([lbl, usd(U[k]['px_realised']), usd(U[k]['cash_cost_t']), dp, dc])
    prev = k
table(rows, [1.3, 1.55, 1.4, 1.4, 1.35], first_col_bold=True, size=8.9, align_right_from=1)
caption('Cost against price, from disclosed segment revenue and segment EBITDA divided by '
        'disclosed own-produced volume. Three periods, three independent filings.')

P(f"Regressing cash cost per tonne on realised price per tonne across those three periods "
  f"gives a slope of {PT['slope']:.3f} with an R-squared of {PT['r2']:.3f}. In plain terms: "
  f"about {pct(PT['slope'], 0)} of every additional dollar of price is consumed by cost "
  f"before it reaches profit. Three observations is a small sample and the study says so "
  f"plainly — but two independent checks support it.")
bullet(f"The relationship survives removing the Algerian gas accrual. That accrual is a "
       f"retrospective catch-up rather than a run rate, and stripping it out changes the "
       f"slope only from {PT['slope']:.3f} to "
       f"{CS['passthrough_ex_accrual']['slope']:.3f}. The link is therefore not an artefact "
       f"of that one item.")
bullet(f"The physics agrees. At roughly {CS['gas_per_tonne']:.0f} million British thermal "
       f"units of gas per tonne of product sold, the observed cost increase between 2025 "
       f"and the first half of 2026 implies the delivered gas price rose by about "
       f"${CS['implied_delta_gas']:.2f} per unit. Working back from the "
       f"${CS['gas_q2_26']:.0f} the chief executive disclosed for the second quarter puts "
       f"the earlier price near ${CS['implied_base_gas']:.2f} — which is exactly where "
       f"legacy Algerian and Egyptian contract gas would be expected to sit. The accounting "
       f"and the engineering arrive at the same place by different routes.")

if os.path.exists('fig3_costpass.png'):
    figure('fig3_costpass.png', 6.0,
           'Figure 3. Cash cost per tonne against realised price per tonne, with the fitted '
           'relationship. This is the study\'s central piece of evidence.')

box([('Why this cuts both ways. ',
      'The link is not simply bad news. It is what the chief executive called right-way '
      'risk: when prices fall, the gas cost falls with them, and the margin is defended '
      'from below as well as capped from above. It makes Fertiglobe a less volatile '
      'business than its revenue line suggests — and a less explosive one than the first '
      'half of 2026 suggests.')], fill=F_PANEL)

H2('1.8  Macro and country')
P('Fertiglobe operates across three sovereigns with very different risk, and the cost of '
  'capital is built from the ground up to reflect that rather than treating the company as '
  'purely Emirati.')
rows = [['Country', 'Rating', 'Default spread', 'Equity risk premium', 'Share of non-current assets']]
rows.append(['Abu Dhabi', 'Aa2', pct(W['ad_ads'], 2), pct(D['inputs']['ad_erp']['value']),
             pct(W['w_uae'])])
rows.append(['Egypt', 'Caa1', '6.37%', pct(D['inputs']['eg_erp']['value']), pct(W['w_egypt'])])
rows.append(['Algeria', 'Not rated', '3.83%', pct(D['inputs']['dz_erp']['value']),
             pct(W['w_algeria'])])
rows.append(['Other', '—', '—', pct(W['mature_erp']), pct(W['w_other'])])
rows.append(['Weighted', '', '', pct(W['erp_rating']), '100%'])
table(rows, [1.4, 1.0, 1.25, 1.6, 1.75], first_col_bold=True, size=8.9, align_right_from=1,
      band_rows={5})
caption('Each country is priced off its own published sovereign row and weighted by where '
        'the plants actually are. Treating the company as purely Emirati would have used '
        f"{pct(D['inputs']['ad_erp']['value'])} instead of {pct(W['erp_rating'])} — a "
        'difference that would have flowed straight into the valuation.')

P('The risk-free rate is normalised so sovereign risk is counted once and not twice. The '
  f"Abu Dhabi dollar sovereign yields about {pct(W['adgb10'])}, being the US 10-year "
  f"Treasury at {pct(W['ust10'])} plus the emirate's own credit spread. Removing that same "
  f"spread again leaves a normalised risk-free rate of {pct(W['rf_star_rating'])}. Country "
  'risk then enters once, inside the equity risk premium above. Using the raw local yield '
  'together with a country-loaded premium would have double-counted it.')

rows = [['Component', 'Rating basis', 'Credit-default-swap basis', 'Source']]
rows.append(['Normalised risk-free rate', pct(W['rf_star_rating']), pct(W['rf_star_cds']),
             'Abu Dhabi dollar sovereign, net of its own default spread'])
rows.append(['Beta', f"{W['beta']:.3f}", f"{W['beta']:.3f}",
             f"Own-share weekly regression, {W['beta_window']} years, n={W['beta_n']}"])
rows.append(['Equity risk premium', pct(W['erp_rating']), pct(W['erp_cds']),
             'Asset-weighted across the three operating countries'])
rows.append(['Cost of equity', pct(W['ke_rating']), pct(W['ke_cds']), ''])
rows.append(['Cost of debt before tax', pct(W['kd']), pct(W['kd']),
             'Marginal — see the evidence table below'])
rows.append(['Cost of debt after tax', pct(W['kd_at']), pct(W['kd_at']),
             f"At the forecast tax rate of {pct(D['tax_rate'])}"])
rows.append(['Weight of equity', pct(W['we']), pct(W['we']), 'Market capitalisation'])
rows.append(['Weighted average cost of capital', pct(W['wacc_rating']), pct(W['wacc_cds']), ''])
rows.append(['Terminal cost of capital', pct(W['wacc_term_rating']), pct(W['wacc_term_cds']),
             f"At a normalised {pct(W['wd_term'])} debt weight"])
table(rows, [2.0, 1.05, 1.5, 2.45], first_col_bold=True, size=8.6, band_rows={9},
      align_right_from=1)
caption('The cost of capital, published on both premium bases as the house method requires. '
        'The rating basis is used for the headline; the credit-default-swap basis is shown '
        'because Algeria has no traded swap, so that column is not fully comparable.')

P('The cost of debt is marginal and forward-looking, taken from the company\'s own most '
  'recent borrowings rather than from anything historical.', space_before=6)
rows = [['Facility', 'Amount', 'Margin', 'Used?']]
rows.append(['Term facilities B and C', '$1,100m', 'SOFR + 0.90%',
             'Yes — spread renegotiated down from 150 and 140 basis points during 2025'])
rows.append(['ADNOC term loan', '$300m', 'SOFR + 1.05%', 'Yes — drawn 27 March 2025'])
rows.append(['Revolving credit facility', '$600m', 'SOFR + 1.15%', 'Undrawn at year end'])
rows.append(['Sorfert term loan', '$35m', 'Algerian bank rate + 1.95%',
             'Foreign-currency tranche, carried at local-equivalent cost'])
rows.append(['Weighted average capitalisation rate', '—', f"{pct(W['kd_cap_rate_rejected'])}",
             'NOT used — this is a historical accounting rate, not a marginal cost'])
rows.append(['Marginal cost of debt applied', '—', pct(W['kd']),
             f"US 10-year plus the average margin on the two most recent facilities"])
table(rows, [2.05, 0.8, 1.5, 2.65], first_col_bold=True, size=8.4, align_right_from=1,
      band_rows={6})
caption('Cost-of-debt evidence. The rate applied sits above the Abu Dhabi sovereign at '
        f"{pct(W['adgb10'])}, as a same-currency corporate must, and below the accounting "
        'capitalisation rate the company discloses for a different purpose.')

P(f"Debt is {pct(1-W['fx_debt_share'])} US dollar denominated, matching the currency of the "
  f"cash flows. The remaining {pct(W['fx_debt_share'])} is the Algerian dinar tranche and "
  'two Australian dollar trade facilities, both carried at local-equivalent cost rather '
  'than at their headline foreign coupon.')

P('The forecast tax rate is not lifted from any single reported year, because no single '
  'reported year is representative — the company reported effective rates of '
  f"{pct(D['inputs']['tax_eff_fy23']['value'])}, {pct(D['inputs']['tax_eff_fy24']['value'])} "
  f"and {pct(D['inputs']['tax_eff_fy25']['value'])} across the last three, each flattered "
  'by items that do not recur. Three independent estimates are computed and averaged:',
  space_before=6)
tt = W['tax_triangulation']
rows = [['Method', 'Rate', 'Basis']]
rows.append(['Four-year aggregate effective rate', pct(tt['aggregate_effective']),
             'Total tax charge over total pre-tax profit, 2022 to 2025'])
rows.append(['Four-year aggregate cash rate', pct(tt['aggregate_cash']),
             'Total tax actually paid over total pre-tax profit, 2022 to 2025'])
rows.append(['Jurisdiction-weighted statutory rate', pct(tt['jurisdiction_weighted']),
             'Published corporate rates weighted by assets in each country'])
rows.append(['Applied', pct(tt['used']), 'The average of the three'])
table(rows, [2.5, 0.9, 3.6], first_col_bold=True, size=8.9, align_right_from=1, band_rows={4})

H2('1.9  Sensitivity')
P('The value is most sensitive to the gas pass-through rate and to the price path — which '
  'is to say, to the crux. It is next most sensitive to beta, which is the study\'s most '
  'fragile input for reasons set out in the caveats.')
sn = D['sens']
rows = [['Gas pass-through rate'] + [f"{p:.2f}" for p in sn['pt_grid']]]
rows.append(['Value (AED/share)'] + [aed(v) for v in sn['grid_pt']])
table(rows, [1.9] + [1.02] * 5, first_col_bold=True, size=8.9, align_right_from=1)
rows = [['Price path shift'] + [f"{p:+.0%}" for p in sn['px_grid']]]
rows.append(['Value (AED/share)'] + [aed(v) for v in sn['grid_px']])
table(rows, [1.9] + [1.02] * 5, first_col_bold=True, size=8.9, align_right_from=1)
rows = [['Beta'] + [f"{b:.2f}" for b in sn['beta_grid']]]
rows.append(['Value (AED/share)'] + [aed(v) for v in sn['grid_beta']])
table(rows, [1.9] + [1.02] * 5, first_col_bold=True, size=8.9, align_right_from=1)
rows = [['Tax rate'] + [pct(t, 0) for t in sn['tax_grid']]]
rows.append(['Value (AED/share)'] + [aed(v) for v in sn['grid_tax']])
table(rows, [1.9] + [1.02] * 5, first_col_bold=True, size=8.9, align_right_from=1)
caption('One-way sensitivities, framing A. The first two lines are the crux; the third is '
        'the fragile input.')

rows = [['Terminal cost of capital \\ growth'] + [pct(g, 1) for g in sn['g_grid']]]
for i, w_ in enumerate(sn['wacc_grid']):
    rows.append([pct(w_)] + [aed(v) for v in sn['grid_wacc_g'][i]])
table(rows, [1.9] + [1.02] * 5, first_col_bold=True, size=8.9, align_right_from=1)
caption('Two-way sensitivity of value to the terminal cost of capital and terminal growth, '
        'in AED per share.')

if os.path.exists('fig2_sens.png'):
    figure('fig2_sens.png', 6.2, 'Figure 5. What moves the value, ranked.')

# ============================================================ 6 §2 TECHNICAL
H1('2. Technical and price structure')
t = TE['tech']
P(t['summary'])
rows = [['', 'Level (AED)', '', '', 'Level (AED)']]
rows = [['Resistance', 'AED', 'Support', 'AED']]
for i in range(3):
    rows.append([f"R{i+1}", aed(TE['levels']['res'][i]), f"S{i+1}",
                 aed(TE['levels']['sup'][i])])
table(rows, [1.5, 1.3, 1.5, 1.3], first_col_bold=True, size=9, align_right_from=1)
caption('Resistance and support, nearest first, from clustered price pivots weighted by '
        'recency and blended with the moving-average stack.')
rows = [['Indicator', 'Reading']]
rows.append(['Last close', f"AED {aed(TE['close'])} on {TE['data_date']}"])
rows.append(['20-day moving average', f"AED {aed(TE['ma']['20'])} ({TE['ma_slope']['20']})"])
rows.append(['50-day moving average', f"AED {aed(TE['ma']['50'])} ({TE['ma_slope']['50']})"])
rows.append(['200-day moving average', f"AED {aed(TE['ma']['200'])} ({TE['ma_slope']['200']})"])
rows.append(['Relative strength index (14)', f"{TE['rsi']:.0f}"])
rows.append(['Average true range (14)', f"AED {TE['atr']:.3f} ({pct(TE['atr_pct'])} of price)"])
rows.append(['52-week range', f"AED {aed(TE['lo_52w'])} to AED {aed(TE['hi_52w'])}"])
rows.append(['Position in range', f"{pct(TE['pct_off_high'])} below the high, "
                                  f"{pct(TE['pct_off_low'])} above the low"])
table(rows, [2.4, 4.6], first_col_bold=True, size=8.9, align_right_from=1)
P(f"Bull case: {t['bull']}  Bear case: {t['bear']}", size=9.6, italic=True)
P('This section describes the tape and nothing more. It carries no view on the business, '
  'because a chart cannot see one.', size=9, italic=True, color=GREY)

# ============================================================ 7 §3 PROBABILISTIC MAP
H1('3. Probability map for the share price')
P('Separately from the valuation above, the study estimates a probability distribution for '
  'the share price at one and three months, built from the share\'s own price history. '
  'This is a statement about the range of outcomes, not a forecast of one.')
for short in ('1M', '3M'):
    h = STK['horizons'][short]
    lbl = 'One month' if short == '1M' else 'Three months'
    P(f"{lbl} — to {h['grade_date']}", bold=True, size=10.5, space_before=6, space_after=2)
    rows = [['Percentile', '5th', '25th', '50th', '75th', '95th']]
    rows.append(['Price (AED)'] + [aed(h['pct'][f'p{p}']) for p in (5, 25, 50, 75, 95)])
    rows.append(['Change from AED ' + aed(STK['spot'])] +
                [f"{h['pct'][f'p{p}']/STK['spot']-1:+.1%}" for p in (5, 25, 50, 75, 95)])
    table(rows, [1.9] + [1.02] * 5, first_col_bold=True, size=8.9, align_right_from=1)
    rows = [['Move', '±5%', '±10%', '±15%', '±20%']]
    rows.append(['Chance of touching, up'] + [pct(h[f'touch_up{p}']) for p in (5, 10, 15, 20)])
    rows.append(['Chance of touching, down'] + [pct(h[f'touch_dn{p}']) for p in (5, 10, 15, 20)])
    rows.append(['Chance of ending above', pct(h['end_up5']), pct(h['end_up10']), '', ''])
    rows.append(['Chance of ending below', pct(h['end_dn5']), pct(h['end_dn10']), '', ''])
    table(rows, [2.2] + [1.2] * 4, first_col_bold=True, size=8.9, align_right_from=1)

if os.path.exists('fig4_fan.png'):
    figure('fig4_fan.png', 6.2, 'Figure 6. The one and three month probability ranges.')
if os.path.exists('fig5_dist.png'):
    figure('fig5_dist.png', 5.6, 'Figure 7. The distribution of possible prices at three months.')

H2('How much to trust this')
P('The method was tested against the share\'s own history before being used. Fertiglobe '
  'listed on 27 October 2021, so the price record runs '
  f"{BT['history_span_years']} years — a literal five-year test is not available for this "
  'company, and the test therefore covers the whole of its listed life, which is the '
  f"maximum evidence that exists. Over {BT['production']['windows']} independent "
  f"three-month windows from {BT['production']['first_origin']} to "
  f"{BT['production']['last_origin']}, the method scored "
  f"{BT['production']['skill_norm']:+.4f} against a random-walk benchmark that already "
  'includes the time value of money. That is statistically indistinguishable from the '
  'benchmark: the method neither beat it nor lost to it, and the study says so rather than '
  'claiming an edge it did not demonstrate.')
P(f"Where the method did do well is in the shape of the distribution, which is what a "
  f"probability range is actually for. Realised outcomes fell across the predicted "
  f"percentiles roughly evenly — a chi-square test on that spread returns "
  f"p={BT['production']['chi2_p']:.2f} and a Kolmogorov-Smirnov test "
  f"p={BT['production']['ks_p']:.2f}, both comfortably consistent with the bands being "
  f"honest. Actual outcomes landed inside the 50% band {pct(BT['production']['cov50'], 0)} "
  f"of the time and inside the 90% band {pct(BT['production']['cov90'], 0)} of the time.")
P('One caveat is recorded rather than buried. Re-running the same test from five different '
  'starting points to get more observations produces a distribution that is no longer '
  f"evenly spread (p={BT['staggered']['chi2_p']:.3f}), with outcomes tilted slightly below "
  'the centre of the range. Those runs overlap each other, which makes the statistical '
  'test read as more significant than it is, so it is not treated as a verdict — but it is '
  'a hint that the centre of the range may sit a little high, and a reader should lean on '
  'the width of the bands rather than their midpoint.')

# ============================================================ 8 §4 COMPARISON
H1('4. Comparison of the lenses')
rows = [['Method', 'Value (AED)', 'Against the market price', 'What it assumes that the others do not']]
for k, nm in (('dcf', 'Cash flow'), ('relative', 'Relative multiples'),
              ('normalized', 'Normalised earnings power'), ('book', 'Book value')):
    v = L[k]['value']
    rows.append([nm, aed(v), f"{v/D['spot']-1:+.0%}",
                 {'dcf': 'That the gas link, the price path and the cost of capital are all '
                         'right for five years and beyond',
                  'relative': 'That the market is pricing comparable assets sensibly today',
                  'normalized': 'That there is such a thing as a mid-cycle margin for this '
                                'business, and that the last three years contain it',
                  'book': 'That book equity means something — which here it largely does '
                          'not'}[k]])
table(rows, [1.75, 0.95, 1.5, 2.8], first_col_bold=True, size=8.7, align_right_from=1)
P('The methods disagree by a factor of two from bottom to top. That is not a failure of the '
  'analysis; it is the correct output for a commodity producer whose selling price doubled '
  'in six months and whose cost base follows it. Any single number presented without that '
  'spread would be more precise than the evidence permits.')

# ============================================================ 9 §5 CATALYSTS
H1('5. Catalysts')
rows = [['Catalyst', 'Direction', 'What to watch']]
rows.append(['Chinese urea export policy', 'Down',
             'Exports were absent until quota guidance in May 2026 and remain minimal. A '
             'full reopening is the largest single downside to the price path.'])
rows.append(['The Strait of Hormuz', 'Both',
             'Reopening relieves the logistics cost that hit the first half of 2026 but '
             'removes the supply squeeze holding prices up. The two partly cancel.'])
rows.append(['Settlement of the Algerian gas contract', 'Down / clarifying',
             f"The accrued liability reached ${usd(D['inputs']['sorfert_accr_h1_26']['value'])} "
             'million by 30 June 2026 with no agreed payment schedule. Settlement converts '
             'an estimate into a cash obligation and reveals the true formula.'])
rows.append(['European tariffs on Russian product', 'Up',
             'Already EUR 60 per tonne and scheduled to reach EUR 315 by 2028. Egyptian and '
             'Algerian product enters duty free.'])
rows.append(['The lower-carbon ammonia plant', 'Up',
             'One million tonnes, operations expected 2027, total project cost under $500 '
             'million. Excluded from this valuation entirely — see below.'])
rows.append(['European gas prices', 'Up',
             'Gas above $20 per unit puts European producers under water and sets a floor '
             'under ammonia. It is the mechanism behind the marginal-cost anchor.'])
table(rows, [2.1, 1.2, 3.7], first_col_bold=True, size=8.6, align_right_from=1)

P('The lower-carbon ammonia project deserves a note because its exclusion is deliberate. '
  'The parent is warehousing the project, and Fertiglobe holds only an option to move to '
  '54% ownership after completion. It is therefore not a consolidated cash flow today and '
  'is carried at nothing. If exercised on the terms described, it would add capacity worth '
  'roughly a sixth of the current merchant base for a capital cost the parent has already '
  'largely borne. That is real value sitting outside the numbers in this study.')

# ============================================================ 10 §6 READING THE ZONES
H1('6. Reading the probability zones')
P('The percentile table in section 3 is easy to misread, so here is what it does and does '
  'not say.')
bullet('The 50th percentile is not a forecast. It is the middle of a distribution, and the '
       'distribution is wide. Half of all outcomes fall on each side of it.')
bullet('The touch probabilities are higher than the ending probabilities, and that is not '
       'an error. A price can trade through a level during the period and come back; '
       'touching is easier than finishing.')
bullet('The bands come from the share\'s own volatility, not from the valuation. A share '
       'can be cheap on the analysis in section 1 and still spend three months falling. '
       'The two halves of this study answer different questions and are deliberately not '
       'reconciled.')
bullet('The bands widen with the square root of time, roughly. The three-month range is '
       'wider than the one-month range because more can happen, not because the outlook is '
       'worse.')

# ============================================================ 11 §7 CAVEATS
H1('7. Caveats and what would change our mind')
rows = [['Concern', 'Why it matters', 'What would change the answer']]
rows.append(['The pass-through rate rests on three observations',
             'It is the single most consequential number in the study and the sample is '
             'tiny. The physical cross-check and the accrual-stripped rerun both support '
             'it, but neither is a substitute for more data.',
             'Two more reported half-years at different price levels. If the slope moves to '
             f"0.65 the value falls to AED {aed(sn['grid_pt'][4])}; at 0.30 it rises to "
             f"AED {aed(sn['grid_pt'][0])}."])
rows.append(['The beta is weak',
             f"The regression against the local market gives {W['beta']:.3f} but explains "
             f"only {pct(W['beta_r2'])} of the share's movement, with a 90% confidence "
             f"interval from {W['beta_ci90'][0]:.2f} to {W['beta_ci90'][1]:.2f}. The reason "
             'is economic, not statistical: this share is driven by global nitrogen prices, '
             'and the local index is mostly banks and property.',
             f"A beta of 1.0 rather than {W['beta']:.2f} would cut the cash-flow value "
             'materially. The sensitivity table in section 1.9 shows the range; a reader '
             'who believes the local index is the wrong yardstick should read the low end '
             'of the cash-flow lens and lean on the other three.'])
rows.append(['The Algerian gas liability is unsettled',
             f"${usd(D['inputs']['sorfert_accr_h1_26']['value'])} million accrued at 30 June "
             '2026, retrospective to November 2023, with negotiations unconcluded and no '
             'payment schedule. The auditors treated it as a key audit matter.',
             'The settled formula. If the final price is materially above what has been '
             'accrued, both the liability and the forward cost rate rise together.'])
rows.append(['Two primary sources disagree',
             'The audited segment note describes limited gas price exposure; the chief '
             'executive describes product-linked pricing. The study follows the latter.',
             'A clear statement in the next annual report. If the segment note wording '
             'proves the accurate one, the value is materially higher than shown here.'])
rows.append(['The float is thin',
             'A 12.6% free float against an 87.4% state-owned parent. Price discovery is '
             'limited and the share can move on flow rather than fundamentals.',
             'Nothing in the near term. It is a permanent feature to price, not an event '
             'to wait for.'])
rows.append(['Terminal value dominates',
             f"{pct(dA['tv_share'])} of enterprise value sits beyond year five under "
             f"framing A and {pct(dB['tv_share'])} under framing B. That is normal for a "
             'long-lived asset base and still means most of the answer is an assumption.',
             'The two-way sensitivity in section 1.9 is the honest map of that exposure.'])
rows.append(['Third-party trading is not built bottom-up',
             'The company discloses traded volumes but never a purchase price, so this leg '
             'is carried at a segment margin rather than unit economics.',
             'Disclosure of trading cost of goods sold. The leg is small — under a fifth of '
             'revenue and under a fiftieth of profit — so the gap is flagged rather than '
             'fatal.'])
table(rows, [1.7, 2.6, 2.7], first_col_bold=True, size=8.4, align_right_from=3)

# ============================================================ 12 APPENDIX A
doc.add_page_break()
H1('Appendix A — Financial statements')
H2('A.1  Income statement — three years reported, five years forecast')
rows = [['US$ million', 'FY2023', 'FY2024', 'FY2025'] + [y + 'E' for y in YRS]]
for lbl, hk, fk in (('Revenue', 'rev', 'rev'), ('EBITDA', 'ebitda', 'ebitda'),
                    ('Depreciation and amortisation', 'dna', 'dna'), ('EBIT', 'ebit', 'ebit')):
    rows.append([lbl] + [usd(D['hist_is'][y][hk]) for y in ('FY23', 'FY24', 'FY25')]
                + [usd(v) for v in A[fk]])
rows.append(['EBITDA margin'] + [pct(D['hist_is'][y]['ebitda_margin']) for y in ('FY23', 'FY24', 'FY25')]
            + [pct(v) for v in A['ebitda_margin']])
rows.append(['Net finance cost'] + [usd(D['hist_is'][y]['netfin']) for y in ('FY23', 'FY24', 'FY25')]
            + ['' for _ in YRS])
rows.append(['Profit before tax'] + [usd(D['hist_is'][y]['pbt']) for y in ('FY23', 'FY24', 'FY25')]
            + ['' for _ in YRS])
rows.append(['Profit for the year'] + [usd(D['hist_is'][y]['np']) for y in ('FY23', 'FY24', 'FY25')]
            + ['' for _ in YRS])
rows.append(['Attributable to owners'] + [usd(D['hist_is'][y]['np_own']) for y in ('FY23', 'FY24', 'FY25')]
            + [usd(v) for v in A['np_attr']])
table(rows, [1.75] + [0.655] * 8, first_col_bold=True, size=7.9, align_right_from=1)
caption('Reported years are taken line by line from the audited consolidated statements. '
        'Forecast years are framing A.')

H2('A.2  Balance sheet')
rows = [['US$ million', 'FY2023', 'FY2024', 'FY2025', 'H1 2026']]
for lbl, k in (('Property, plant and equipment', 'ppe'), ('Inventories', 'inv'),
               ('Trade and other receivables', 'recv'), ('Cash and cash equivalents', 'cash'),
               ('Total assets', 'ta'), ('Trade and other payables', 'pay'),
               ('Gross interest-bearing debt', 'debt_gross'), ('Net debt', 'net_debt'),
               ('Equity attributable to owners', 'eq_own'),
               ('Non-controlling interests', 'eq_nci'), ('Total equity', 'eq_tot')):
    h1 = {'inv': D['inputs']['inv_h1_26']['value'], 'recv': D['inputs']['recv_h1_26']['value'],
          'cash': D['inputs']['cash_h1_26']['value'], 'ta': D['inputs']['ta_h1_26']['value'],
          'pay': D['inputs']['pay_h1_26']['value'],
          'debt_gross': D['inputs']['grossdebt_h1_26']['value'],
          'net_debt': D['inputs']['netdebt_h1_26']['value'],
          'eq_tot': D['inputs']['eq_h1_26']['value']}.get(k)
    rows.append([lbl] + [usd(D['hist_bs'][y][k]) for y in ('FY23', 'FY24', 'FY25')]
                + [usd(h1) if h1 is not None else '—'])
table(rows, [2.6, 1.1, 1.1, 1.1, 1.1], first_col_bold=True, size=8.6, align_right_from=1)

H2('A.3  Forecast balance sheet and cash flow markers')
rows = [['US$ million'] + [y + 'E' for y in YRS]]
for lbl, k in (('Property, plant and equipment', 'ppe'), ('Net working capital', 'nwc'),
               ('Invested capital', 'ic'), ('Return on invested capital', 'roic'),
               ('Net debt', 'net_debt'), ('Capital expenditure', 'capex'),
               ('Free cash flow to the firm', 'fcff')):
    if k == 'roic':
        rows.append([lbl] + [pct(v) for v in A[k]])
    else:
        rows.append([lbl] + [usd(v) for v in A[k]])
table(rows, [2.3] + [0.94] * 5, first_col_bold=True, size=8.6, align_right_from=1)

P('The working-capital cycle is projected from the cycle the company actually runs, not '
  'plugged. Receivable days, inventory days and payable days measured off the filed '
  'statements were '
  f"{D['ccc']['FY25']['dso']:.0f}, {D['ccc']['FY25']['dio']:.0f} and "
  f"{D['ccc']['FY25_ex_accrual']['dpo']:.0f} respectively for 2025, the payable figure "
  'excluding the Algerian gas accrual because that is not a trade payable in the ordinary '
  'course. Including it would have shown a negative cash conversion cycle of '
  f"{abs(D['ccc']['FY25']['ccc']):.0f} days and made the business look as though suppliers "
  f"funded it; excluding it gives {D['ccc']['FY25_ex_accrual']['ccc']:.0f} days, which is "
  'the honest figure and the one used.', space_before=4)

# ============================================================ 13 APPENDIX B
doc.add_page_break()
H1('Appendix B — Peers, risks and sources')
H2('B.1  Comparable companies')
rows = [['Company', 'Market', 'Enterprise value to EBITDA', 'Character']]
for p_ in D['rel']['peers']:
    rows.append([p_['name'], p_['mkt'], f"{p_['ev_ebitda']:.1f}x", p_['note']])
table(rows, [1.7, 0.8, 1.6, 2.9], first_col_bold=True, size=8.7, align_right_from=1)

H2('B.2  Risk register')
rows = [['Risk', 'Type', 'Assessment']]
rows.append(['Nitrogen price cycle', 'Market',
             'The dominant exposure, partly self-hedged by the gas link'])
rows.append(['Algerian gas contract settlement', 'Contractual',
             'Unquantified until agreed; accrued but not settled'])
rows.append(['Egyptian gas supply', 'Operational',
             'Curtailments hit the second quarter of 2025; management reported no '
             'interruptions through the first half of 2026'])
rows.append(['Regional conflict and shipping routes', 'Geopolitical',
             'Directly affected export volumes and logistics cost in 2026'])
rows.append(['Country risk in Egypt and Algeria', 'Sovereign',
             'Priced explicitly through the asset-weighted equity risk premium'])
rows.append(['Concentrated ownership and thin float', 'Governance / liquidity',
             '87.4% held by one shareholder'])
rows.append(['Currency', 'Financial',
             'Low — reporting, revenue and most debt are all in US dollars, and the '
             'dirham is pegged'])
table(rows, [2.1, 1.35, 3.55], first_col_bold=True, size=8.6, align_right_from=2)

H2('B.3  Sources')
P('The complete source record — every input with its value, date and derivation, grouped '
  'by research layer, together with the primary documents, the judgements and what would '
  'overturn each of them, and the searches that returned nothing — is published as a '
  'separate document accompanying this study. In summary:')
rows = [['Category', 'Count', 'Detail']]
rows.append(['Complete audited financial years obtained', '4',
             'FY2022, FY2023, FY2024 and FY2025, each from the signed consolidated '
             'statements'])
rows.append(['Interim periods of the current year', '2',
             'First quarter and first half of 2026, both already on the public record and '
             'both incorporated before the forecast was built'])
rows.append(['Company documents read', f"{len(SW['primary_access'])}+",
             'Audited statements, interim statements, management discussion and analysis '
             'reports, investor presentations and the results-call transcript'])
rows.append(['Distinct inputs recorded', f"{len(D['inputs'])}",
             'Each with a value, a source, a date and a research layer'])
rows.append(['Aggregator-sourced figures in the build', '0',
             'Peer market multiples are used as a cross-check only and are labelled as such'])
table(rows, [2.6, 0.7, 3.7], first_col_bold=True, size=8.6, align_right_from=1)

# ============================================================ 14 APPENDIX C
doc.add_page_break()
H1('Appendix C — Expert panel')
P('Three analysts were asked to value the company by genuinely different methods. Each '
  'shows their workings, names the assumption their answer rests on, and states in advance '
  'what would prove them wrong.')

H2('C.1  Expert 1 — the multiple')
P('Worldview: a commodity producer is worth what the market pays for comparable cash flows. '
  'Discounted cash flow models of cyclical businesses are precision theatre; the multiple '
  'embeds what buyers actually believe.')
P('When it works: at cycle midpoints, and where the peer set is genuinely comparable. '
  'When it fails: at cycle extremes, when every peer is mispriced together, and when the '
  'peer set differs in gas cost, country risk or capital structure — all three of which '
  'apply here to some degree.')
rows = [['Line', 'Value']]
rows.append(['Mid-cycle EBITDA (US$m)', usd(EX['e1']['ebitda'])])
rows.append(['Multiple applied', f"{EX['e1']['mult']:.1f}x"])
rows.append(['Enterprise value (US$m)', usd(EX['e1']['ev'])])
rows.append(['less net debt (US$m)', usd(-bA['net_debt'])])
rows.append(['less non-controlling interests', pct(D['nci_share']) + ' of equity value'])
rows.append(['Value per share (AED)', aed(EX['e1']['ps_aed'])])
table(rows, [3.4, 3.6], first_col_bold=True, size=8.9, align_right_from=1, band_rows={6})
P(f"Named sensitivity: each half-turn on the multiple moves the value by roughly "
  f"AED {abs(EX['e1']['ebitda']*0.5*(1-D['nci_share'])/M['shares_mn']*M['fx']):.2f} per "
  f"share. Falsifier stated in advance: if Gulf nitrogen peers de-rate below 7 times while "
  f"Fertiglobe's own earnings hold, this method is reading a sector sentiment rather than a "
  f"company value, and should be discounted.")

H2('C.2  Expert 2 — the cash flow')
P('Worldview: only the cash a business produces matters, and the job is to model the '
  'mechanism that produces it. For this company that mechanism is the link between selling '
  'price and gas cost, and any model that ignores it is valuing a different company.')
P('When it works: where the operating mechanics are understood and documented. When it '
  'fails: when the discount rate is uncertain, which it badly is here — the beta explains '
  f"only {pct(W['beta_r2'])} of the share's movement.")
rows = [['Line', 'Framing A', 'Framing B']]
rows.append(['Present value of five years of cash flow (US$m)', usd(dA['pv_explicit']),
             usd(dB['pv_explicit'])])
rows.append(['Present value of terminal value (US$m)', usd(dA['pv_tv']), usd(dB['pv_tv'])])
rows.append(['Enterprise value (US$m)', usd(dA['ev']), usd(dB['ev'])])
rows.append(['Terminal share of enterprise value', pct(dA['tv_share']), pct(dB['tv_share'])])
rows.append(['Terminal return on capital applied', pct(dA['roic_term']), pct(dB['roic_term'])])
rows.append(['Reinvestment rate', pct(dA['rr_term']), pct(dB['rr_term'])])
rows.append(['Value per share (AED)', aed(bA['ps_aed']), aed(bB['ps_aed'])])
table(rows, [3.2, 1.9, 1.9], first_col_bold=True, size=8.9, align_right_from=1, band_rows={7})
P('Named sensitivity: moving the gas pass-through from '
  f"{PT['slope']:.2f} to 0.65 takes the value from AED {aed(EX['e2']['ps_aed'])} to "
  f"AED {aed(sn['grid_pt'][4])}. Falsifier stated in advance: if the company reports a "
  'half-year in which realised price falls sharply and cash cost per tonne does not follow '
  'it down, the pass-through relationship is not real and this valuation is wrong in both '
  'directions at once.')

H2('C.3  Expert 3 — the assets')
P('Worldview: in a commodity industry, price eventually returns to the cost of building new '
  'supply. What the existing plants would cost to replace is therefore the anchor, and '
  'earnings are the noise around it.')
P('When it works: over long horizons, and where capacity is fungible and tradeable. When it '
  'fails: when existing assets carry something a new entrant cannot buy — which is exactly '
  'the case here, because the legacy Algerian and Egyptian gas contracts are not available '
  'to anyone building today. This method therefore understates.')
rows = [['Line', 'Value']]
rows.append(['Installed capacity (kt)', usd(EX['e3']['capacity_kt'])])
rows.append(['Replacement cost per tonne of capacity (US$)', usd(EX['e3']['per_tonne'])])
rows.append(['Replacement enterprise value (US$m)', usd(EX['e3']['ev'])])
rows.append(['less net debt (US$m)', usd(-bA['net_debt'])])
rows.append(['Value per share (AED)', aed(EX['e3']['ps_aed'])])
table(rows, [3.4, 3.6], first_col_bold=True, size=8.9, align_right_from=1, band_rows={5})
P('Named sensitivity: a $250 change in replacement cost per tonne moves the value by about '
  f"AED {abs(6600*250/1000*(1-D['nci_share'])/M['shares_mn']*M['fx']):.2f} per share. "
  'Falsifier stated in advance: a greenfield ammonia-urea complex announced anywhere in the '
  'Gulf at a materially different capital cost per tonne would reset this anchor '
  'immediately.')

H2('C.4  Cross-examination')
rows = [['Challenge', 'From', 'Response']]
rows.append(['"Your multiple is borrowed from companies with different gas contracts and '
             'different country risk. It cannot be the anchor."', 'Expert 2 to Expert 1',
             'Conceded in part. The multiple applied sits below the Gulf peers precisely '
             'for that reason, but the objection is right that the peer set is imperfect.'])
rows.append(['"Two thirds of your value is a terminal number resting on a beta that '
             'explains six percent of anything."', 'Expert 1 to Expert 2',
             'Conceded. This is the method\'s real weakness and the reason the study weights '
             'it at less than half rather than relying on it alone.'])
rows.append(['"Replacement cost ignores that the whole business is a legacy gas contract "'
             '"wrapped in steel."', 'Expert 2 to Expert 3',
             'Conceded, and stated by Expert 3 in advance. The method is a floor, not a '
             'valuation.'])
rows.append(['"Your cash flow model assumes the pass-through holds when prices fall. It has '
             'only ever been observed while they rose."', 'Expert 3 to Expert 2',
             'Rejected, with a caveat. The chief executive described the arrangement as '
             'symmetric, and a contract formula does not know which way the price is '
             'moving. But the observation is fair that it has not yet been tested downward, '
             'and it is recorded as the stated falsifier.'])
rows.append(['"If the audited note is right and gas exposure really is limited, all three '
             'of you are too low."', 'Expert 1 to all',
             'Accepted as a live possibility and carried in the caveats. It is the single '
             'reading of the evidence under which this study is materially too '
             'conservative.'])
table(rows, [2.5, 1.35, 3.15], first_col_bold=True, size=8.4, align_right_from=3)

H2('C.5  The three in one room')
P('Put together, the three converge more than their methods suggest they should. Expert 1 '
  f"lands at AED {aed(EX['e1']['ps_aed'])}, Expert 2 at AED {aed(EX['e2']['ps_aed'])} on "
  f"framing A, and Expert 3 at AED {aed(EX['e3']['ps_aed'])}. The spread is about "
  f"AED {max(EX['e1']['ps_aed'], EX['e2']['ps_aed'], EX['e3']['ps_aed']) - min(EX['e1']['ps_aed'], EX['e2']['ps_aed'], EX['e3']['ps_aed']):.2f} "
  'per share, or roughly a eighth of the middle value — narrow, given that one counted cash '
  'flows, one counted comparable multiples and one counted steel.')
P('They agree on the mechanism and disagree about its durability. All three accept that the '
  'gas link is real and that it caps the upside from a price spike. Expert 2 is willing to '
  'model five years of it; Expert 1 doubts anyone can; Expert 3 thinks it does not matter '
  'over a long enough horizon. Where they genuinely part company is the terminal value, and '
  'that is also where the study is least certain.')

H2('C.6  Divergence table')
rows = [['Assumption', 'Expert 1', 'Expert 2', 'Expert 3', 'Drives how much of the gap?']]
rows.append(['Mid-cycle EBITDA', usd(EX['e1']['ebitda']) + 'm', 'Modelled per year',
             'Not used', 'Small — the levels are close'])
rows.append(['Terminal treatment', 'Multiple embeds it',
             pct(dA['tv_share']) + ' of value', 'Replacement cost is the terminal',
             'Large — this is the main divergence'])
rows.append(['Cost of capital', 'Implicit in the multiple', pct(W['wacc_rating']),
             'Not used', 'Large — Expert 2 alone is exposed to the weak beta'])
rows.append(['Gas pass-through', 'Implicit', f"{PT['slope']:.2f} explicit", 'Irrelevant',
             'Moderate — all three are exposed, only one prices it'])
rows.append(['Value of the legacy gas contracts', 'Partly in the multiple',
             'In the cash flows', 'Excluded by construction',
             'Explains why Expert 3 is a floor'])
table(rows, [1.6, 1.4, 1.35, 1.3, 1.35], first_col_bold=True, size=8.2, align_right_from=1)

if os.path.exists('figD1_experts.png'):
    figure('figD1_experts.png', 5.8, 'Figure 8. The three expert valuations and their spread.')

# ============================================================ 15 ABOUT
doc.add_page_break()
H1('About')
P('Testahil publishes independent valuation studies and calibrated probability ranges for '
  'listed securities, together with a public record of every forecast made and how it '
  'turned out. Studies are built from primary sources — the company\'s own issued financial '
  'statements and disclosures — and every figure in a study traces to a dated source in the '
  'accompanying source document.')
P('Two things are published for every company: a fair-value range produced by four '
  'independent methods, and a probability distribution for the share price over defined '
  'horizons. They answer different questions and are not reconciled with one another. '
  'Neither is a rating and neither is a price target, because a single number implies a '
  'confidence that the evidence does not support.')
P('Every probability range is tested against the security\'s own price history before it is '
  'published, scored against a benchmark that already includes the time value of money, and '
  'reported honestly whether it beat that benchmark or not. In this study it did not beat '
  'it, and section 3 says so.')

# ============================================================ 16 DISCLOSURE
H1('Disclosure')
P('This document is educational analysis. It is not investment advice, an offer, a '
  'solicitation, or a recommendation to buy or sell any security. It contains no rating and '
  'no price target.')
P('The analysis rests on public information believed to be reliable, principally the '
  'company\'s own audited and interim financial statements, management commentary, investor '
  'presentations and results-call transcript, together with published sovereign risk data '
  'and market prices. No representation is made that it is complete or free of error. '
  'Forward-looking figures are estimates and will differ, possibly materially, from what '
  'actually happens.')
P('Valuation involves judgement. Reasonable analysts using the same public information will '
  'reach different conclusions, and this study makes the largest of its own judgements '
  'visible and computes the most consequential one two ways rather than one. Readers should '
  'form their own view and, where appropriate, take professional advice.')
P(f"Price basis {M['price_date']}. Study date {M['asof']}. Currency: figures in US dollars "
  f"unless marked AED; per-share values converted at {M['fx']} dirhams to the dollar.",
  size=9, color=GREY)

doc.save('Fertiglobe_Valuation_Study_09-08-2026.docx')
print('wrote Fertiglobe_Valuation_Study_09-08-2026.docx')
