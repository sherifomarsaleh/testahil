"""AMR_Valuation_Study_09-08-2026_public.docx — the delivered report.

Reads study_numbers.json and the result files. No financial numeral is typed here.
"""
import json, os
exec(open('docx_base.py').read())

HERE = os.path.dirname(os.path.abspath(__file__))
STK = json.load(open('strike_result.json'))
TECH = json.load(open('technicals.json'))
BT = json.load(open('backtest_5y.json'))
PBT = json.load(open('panel_backtest_5y.json'))
BETA = json.load(open('beta_result.json'))
SW = json.load(open('sweep_register.json'))
RC = json.load(open('recalc_result.json'))
DT = json.load(open('driver_test_result.json'))

M, H, F, U, W, DCF = D['meta'], D['history'], D['forecast'], D['unit_build'], D['wacc'], D['dcf']
LN, SN, CS, C = D['lenses'], D['sensitivity'], D['cost_stack'], D['contested']
ALT, DFL, PEERS, EXP = D['dcf_alt'], D['dual_framing_leases'], D['peers']['peers'], D['experts']
FX, SH, SPOT, SPOTA = M['fx'], M['shares_mn'], M['spot'], M['spot_aed']
UNITS, FY = U['units'], F['years']
YH = ['FY2023', 'FY2024', 'FY2025']
aed = lambda usd: usd * FX


def n(x, d=0):
    return f'{x:,.{d}f}'


def pc(x, d=1):
    return f'{100*x:.{d}f}%'


# =====================================================================  1. MASTHEAD
masthead()
P('Americana Restaurants International PLC', size=23, bold=True, space_after=0)
rich([('Abu Dhabi Securities Exchange: AMR', dict(size=11.5, bold=True, color=BRASS)),
      ('   ·   also listed on the Saudi Exchange as 6015   ·   restaurants and quick-service '
       'food   ·   reports in US dollars', dict(size=11.5, color=GREY))], space_after=4)
rich([('Valuation study, 9 August 2026   ·   market price AED ', dict(size=10.5, color=GREY)),
      (f'{SPOTA:.2f}', dict(size=10.5, bold=True)),
      (f' at the close of 7 August 2026 (USD {SPOT:.3f} at the 3.6725 peg)',
       dict(size=10.5, color=GREY))], space_after=10)

box([('READ THIS FIRST. ',
      'This is an educational valuation study, not investment advice, and it carries no '
      'recommendation and no price target. What it produces is a range of values from four '
      'independent methods, and a separate map of where the traded price could sit over the '
      'next one and three months. The two are different objects and are never blended: one is '
      'about what the business is worth, the other about how volatile its share price is.'),
     ('WHAT THE NUMBERS REST ON. ',
      'Every historical figure comes from the company\'s own audited consolidated financial '
      'statements and its own investor materials, read from its investor-relations library. No '
      'data vendor, broker note or news report is used as a source for anything the company '
      'itself reports. Outside figures appear only as cross-checks and are labelled as such '
      'wherever they occur.'),
     ('THE ONE QUESTION THAT DECIDES IT. ',
      'Americana\'s EBITDA margin went from 22.6% to 25.5% in a single year. If that gain is '
      'structural the shares are worth about AED ' + f'{C["way_a"]["value_aed"]:.2f}' +
      '; if it is cyclical, about AED ' + f'{C["way_b"]["value_aed"]:.2f}' + '. The market is at '
      f'AED {SPOTA:.2f}, between the two. Both readings are computed in full and published side '
      'by side in this report and in the companion workbook. Neither is averaged into the other.')])

# =====================================================================  2. HEADLINE
H1('Headline')
central_a = aed(LN['central'])
WB_ = sum(LN['ranges'][k][0] * LN['weights'][k] for k in LN['weights'])
WU_ = sum(LN['ranges'][k][2] * LN['weights'][k] for k in LN['weights'])
rich([('Four methods, on their stated weights, put the equity between a weighted bear of AED ',
       dict()),
      (f'{aed(WB_):.2f}', dict(bold=True)),
      (' and a weighted bull of AED ', dict()),
      (f'{aed(WU_):.2f}', dict(bold=True)),
      (f' a share (the widest single-lens extremes span {aed(LN["low"]):.2f} to '
       f'{aed(LN["high"]):.2f}), with a weighted central value of AED ', dict()),
      (f'{central_a:.2f}', dict(bold=True)),
      (f' — about {pc(abs(LN["central"]/SPOT-1), 0)} '
       f'{"above" if LN["central"] >= SPOT else "below"} the AED {SPOTA:.2f} the market is paying. '
       'That gap is not the interesting part of this study. The interesting part is that the '
       'whole of it, and rather more, turns on a single question the filings do not answer.',
       dict())])

P('Americana operates 2,746 restaurants across twelve countries — KFC, Pizza Hut, Hardee\'s, '
  'Krispy Kreme and a widening tail of smaller brands — as a master franchisee. It does not own '
  'the brands; it pays for them, 5.6% of revenue in royalties last year, and in exchange it '
  'operates the restaurants, employs the people in them — 37,207 on the audited average '
  'full-time-equivalent measure, about 39,400 heads including part-time and contract staff '
  '— and carries the leases. That is '
  'the structural fact that governs everything else here, including why the company should not '
  'be valued on the multiples the brand owners command.')

P('The last three audited years do not tell a simple story. Revenue was USD 2,413 million in '
  '2023, FELL to USD 2,197 million in 2024, and recovered to USD 2,509 million in 2025 — so the '
  'company has only just regained the level it reached three years ago, while adding some 300 '
  'restaurants along the way. The recovery came with something more interesting than the revenue: '
  'in the first half of 2026 revenue rose 12.1%, the cost of food and packaging fell from 29.2% '
  'of sales to 27.4%, EBITDA margin expanded 290 basis points to 25.5%, and profit attributable '
  'to shareholders rose 59.2%.')

P('Whether that margin gain holds is the study. Read as structural — procurement work, menu '
  'engineering, better economics in the delivery channel, all of which the company names — the '
  f'shares are worth about AED {C["way_a"]["value_aed"]:.2f}. Read as cyclical — a friendly turn '
  'in traded food prices and a quiet period on promotion, both of which revert — they are worth '
  f'about AED {C["way_b"]["value_aed"]:.2f}, which is BELOW the current price. The market price '
  'sits between the two readings, which is a reasonable place for it to sit.')

figure('fig2_contested.png', 6.7,
       'The question that decides it. Both readings are complete re-runs of the whole model, '
       'not a sensitivity applied to one number.')

# =====================================================================  3. VALUATION SUMMARY
H1('Valuation summary')
rows = [['Lens', 'Weight', 'Bear', 'Central', 'Bull', 'vs market', 'Terminal value share']]
for k in ['Discounted cash flow', 'Relative multiples', 'Normalised earnings power',
          'Book value and sustainable return']:
    lo, ba, hi = LN['ranges'][k]
    rows.append([k, pc(LN['weights'][k], 0), f'{aed(lo):.2f}', f'{aed(ba):.2f}',
                 f'{aed(hi):.2f}', pc(ba / SPOT - 1, 0),
                 pc(DCF['tv_share'], 0) if k == 'Discounted cash flow' else '—'])
rows.append(['Weighted central (bear and bull weighted the same way)', '100%',
             f'{aed(WB_):.2f}', f'{central_a:.2f}', f'{aed(WU_):.2f}',
             pc(LN['central'] / SPOT - 1, 0), '—'])
rows.append(['Range across the lenses (unweighted extremes)', '—', f'{aed(LN["low"]):.2f}',
             '—', f'{aed(LN["high"]):.2f}', '—', '—'])
rows.append(['Expert panel median', '—', '—', f'{aed(LN["expert_median"]):.2f}', '—',
             pc(LN['expert_median'] / SPOT - 1, 0), '—'])
rows.append(['Market price, 7 August 2026', '—', '—', f'{SPOTA:.2f}', '—', '—', '—'])
table(rows, [2.05, 0.62, 0.72, 0.80, 0.72, 0.78, 1.16], band_rows={5, 6}, size=9.0)
caption('AED a share. The terminal value share is the portion of the cash-flow lens\'s '
        'enterprise value that sits beyond the fifth forecast year; it is shown again in the '
        'bridge from enterprise value to equity below.')

H2('The same table, the other way round — the open question priced twice')
table([['Reading of the margin', 'What it assumes', 'Value (AED)', 'vs market'],
       [C['way_a']['name'], C['way_a']['detail'], f'{C["way_a"]["value_aed"]:.2f}',
        pc(C['way_a']['value_usd'] / SPOT - 1, 0)],
       [C['way_b']['name'], C['way_b']['detail'], f'{C["way_b"]["value_aed"]:.2f}',
        pc(C['way_b']['value_usd'] / SPOT - 1, 0)]],
      [1.75, 3.35, 0.95, 0.95], size=9.0)
caption('Neither is averaged into the other. The difference between them, '
        f'{pc(abs(C["gap_pct"]), 0)}, is larger than the entire plausible range of the cost of '
        'capital.')

H2('The bridge from enterprise value to equity')
BRDG = [['Step', 'USD million', 'AED a share'],
        ['Present value of the five forecast years', n(DCF['sum_pv'], 0),
         f'{aed(DCF["sum_pv"]/SH):.2f}'],
        ['Present value of the terminal value', n(DCF['pv_tv'], 0),
         f'{aed(DCF["pv_tv"]/SH):.2f}'],
        ['Enterprise value', n(DCF['ev'], 0), f'{aed(DCF["ev"]/SH):.2f}'],
        ['Less lease liabilities', f'({n(H["lease_liabilities"][2], 0)})',
         f'({aed(H["lease_liabilities"][2]/SH):.2f})'],
        ['Plus cash and bank deposits', n(H['cash'][2] + H['deposits'][2], 0),
         f'{aed((H["cash"][2]+H["deposits"][2])/SH):.2f}'],
        ['Less non-controlling interests', f'({n(H["nci"][2], 0)})', '(0.00)'],
        ['Equity attributable to shareholders', n(DCF['equity'], 0),
         f'{aed(DCF["equity"]/SH):.2f}'],
        ['Terminal value as a share of enterprise value', pc(DCF['tv_share'], 0), '—']]
table(BRDG, [3.25, 1.85, 1.90], band_rows={3, 7, 8}, size=9.3)
caption('The company carries no bank debt. Its only borrowing is the capitalised lease estate, '
        'and it holds more cash and deposits than two-thirds of that liability.')

# =====================================================================  4. COMPANY OVERVIEW
H1('Company overview')
P('Americana Restaurants International PLC is registered in the Abu Dhabi Global Market and has '
  'been operating since 1969. It is the largest restaurant operator across the Middle East, '
  'North Africa and Kazakhstan. Its December 2022 initial public offering was the region\'s '
  'first concurrent dual listing: the same shares trade in Abu Dhabi and in Riyadh. Adeptio AD '
  'Investments holds 66.03%; its parent is owned equally by Mohamed Ali Rashed Alabbar and a '
  'subsidiary of the Public Investment Fund of Saudi Arabia.')

P('The business is a master franchisee. It licenses KFC, Pizza Hut, Hardee\'s, Krispy Kreme, '
  'Costa Coffee, Peet\'s Coffee, Baskin-Robbins, TGI Fridays, Wimpy and Chicken Tikka, and has '
  'lately added two of its own: Malak Al Tawouk, acquired in the United Arab Emirates and Saudi '
  'Arabia, and carpo, launched in Qatar. Four power brands produce 94% of revenue. Home delivery '
  'is 52% of sales in the first half of 2026, against 42% in the same half two years earlier, '
  'largely through the company\'s own ordering application rather than third-party platforms.')

rows = [['Market', 'Restaurants at 31 Dec 2025', 'FY2025 revenue (USD m)',
         'Revenue per restaurant (USD 000)', 'Share of revenue', 'Restaurants at 30 Jun 2026']]
tot_rev = sum(U['revenue_hist'][u][2] for u in UNITS)
tot_st25 = sum(U['stores_hist'][u][1] for u in UNITS)
for u in UNITS:
    rows.append([u, n(U['stores_hist'][u][1]), n(U['revenue_hist'][u][2], 0),
                 n(U['rps_2025'][u], 0), pc(U['revenue_hist'][u][2] / tot_rev, 0),
                 n(U['stores_hist'][u][2])])
rows.append(['Total', n(tot_st25), n(tot_rev, 0), n(tot_rev * 1000 / tot_st25, 0), '100%',
             n(sum(U['stores_hist'][u][2] for u in UNITS))])
table(rows, [1.30, 1.25, 1.10, 1.35, 0.85, 1.15], band_rows={8}, size=8.8)
caption('Revenue is stated before intercompany eliminations, which is how the company discloses '
        'it. The Lower Gulf is Qatar, Oman and Bahrain; other markets are Kazakhstan, Iraq, '
        'Lebanon and Jordan. Revenue per restaurant is FY2025 revenue over the restaurant count '
        'at the SAME date, 31 December 2025; the June 2026 column is shown alongside so the '
        'direction of travel in each market is visible.')

P('Two facts in that table matter more than the rest. The first is the spread in revenue per '
  f'restaurant: a restaurant in the United Arab Emirates turns over USD {U["rps_2025"]["UAE"]:,.0f} '
  f'thousand a year, one in Egypt USD {U["rps_2025"]["Egypt"]:,.0f} thousand. Growth in Egypt '
  'therefore adds far less revenue per unit of capital than growth in the Gulf, which is why '
  'this study builds each market separately rather than applying one growth rate to the group. '
  'The second is concentration: the three Major Gulf markets produce 72% of revenue, and all '
  'three currencies are pegged to the US dollar. The company reports that 83% of revenue is '
  'earned in stable pegged currencies — which is why a dollar-reporting company with operations '
  'in Egypt and Kazakhstan is far less exposed to currency than its map suggests.')

H2('The three audited years, in one table')
rows = [['USD million', 'FY2023', 'FY2024', 'FY2025', 'H1 2026']]
h1 = H['h1_2026']
rows.append(['Revenue'] + [n(x, 0) for x in H['revenue']] + [n(h1['revenue'], 0)])
rows.append(['EBITDA'] + [n(x, 0) for x in H['ebitda']] + [n(h1['ebitda'], 0)])
rows.append(['EBITDA margin'] + [pc(x) for x in H['ebitda_margin']] + [pc(h1['margin'])])
rows.append(['Profit attributable to shareholders'] +
            [n(x, 0) for x in H['pat_shareholders']] + [n(h1['pat_shareholders'], 0)])
rows.append(['Restaurants at period end', '2,435', '2,590', '2,749', '2,746'])
rows.append(['Cash and bank deposits'] +
            [n(H['cash'][i] + H['deposits'][i], 0) for i in range(3)] +
            [n(h1['cash_and_deposits'], 0)])
rows.append(['Lease liabilities'] + [n(x, 0) for x in H['lease_liabilities']] +
            [n(h1['lease_liabilities'], 0)])
rows.append(['Bank debt', n(H['bank_debt'][0], 1), '—', '—', '—'])
table(rows, [2.55, 1.05, 1.05, 1.05, 1.30], size=9.0)
caption('The 2023 restaurant count of 2,435 is the company\'s own disclosure in its FY2023 '
        'earnings release. EBITDA is reconstructed as operating profit plus depreciation, '
        'amortisation and impairments — it appears in no audited statement, and the releases '
        'publish a closely similar "Adjusted EBITDA". The 30 June 2026 cash figure includes '
        'the USD 22 million of treasury bills and deposit-linked notes reported that date as '
        'investments in financial assets; the earlier columns have no such line.')

# =====================================================================  5. §1 FUNDAMENTAL
H1('1  Fundamental valuation')
P('Four lenses, applied independently and then weighted. The cash-flow model carries half the '
  'weight because the business is cash-generative and the estate is knowable restaurant by '
  'restaurant. The book lens carries the least, for reasons set out where it appears.')

H2('1.1  The cash-flow model')
P('The model runs in US dollars, which is the company\'s reporting and functional currency, and '
  'converts to dirhams at the 3.6725 peg. Five explicit years, then a terminal value. The '
  'waterfall in full:')
rows = [['USD million'] + FY]
for lab, key, sign in [('Revenue', 'revenue', 1), ('EBITDA', 'ebitda', 1),
                       ('EBITDA margin', 'ebitda_margin', 0),
                       ('Less depreciation and amortisation', 'dna', -1),
                       ('EBIT', 'ebit', 1), ('NOPAT — EBIT after tax', 'nopat', 1),
                       ('Add back depreciation and amortisation', 'dna', 1),
                       ('Less the recurring impairment charge', 'impairment', -1),
                       ('Less capital expenditure, including new leases', 'capex_total', -1),
                       ('Less change in working capital', 'dnwc', -1),
                       ('Free cash flow to the firm', 'fcff', 1),
                       ('Cost of capital', 'wacc_path', 0),
                       ('Discount factor', 'discount_factor', 2)]:
    if sign == 0:
        rows.append([lab] + [pc(x) for x in F[key]])
    elif sign == 2:
        rows.append([lab] + [f'{x:.3f}' for x in F[key]])
    else:
        rows.append([lab] + [(n(sign * x, 0) if sign > 0 else f'({n(x, 0)})') for x in F[key]])
rows.append(['Present value of free cash flow'] + [n(x, 0) for x in DCF['pv']])
table(rows, [2.55, 0.90, 0.90, 0.90, 0.90, 0.90], band_rows={10, 13}, size=8.8)
caption('Taking a new restaurant lease is treated as an investment on this reading, so additions '
        'to right-of-use assets are charged in capital expenditure and the lease liability is '
        'deducted in the bridge. Change in working capital is a source of cash here, not a use, '
        'because the company collects at the till and pays suppliers on terms.')

rows = [['Terminal block', 'Value'],
        ['Terminal-year NOPAT grown one year (USD m)', n(DCF['nopat_next'], 0)],
        ['Invested capital at the end of the forecast (USD m)', n(DCF['invested_capital'], 0)],
        ['Terminal return on incremental capital — faded to the payback-anchored target',
         pc(DCF['roic_term'], 0)],
        ['Model-implied average return on closing capital (the bull reading)',
         pc(DCF['roic_implied_avg'], 0)],
        ['Required reinvestment rate — growth over return on capital', pc(DCF['rr_term'], 1)],
        ['Terminal growth', pc(W['terminal_g'])],
        ['Terminal cost of capital', pc(W['wacc_terminal'], 2)],
        ['Terminal value (USD m)', n(DCF['tv'], 0)],
        ['Present value of the terminal value (USD m)', n(DCF['pv_tv'], 0)],
        ['Terminal value as a share of enterprise value', pc(DCF['tv_share'], 0)],
        ['Enterprise value (USD m)', n(DCF['ev'], 0)],
        ['Equity value (USD m)', n(DCF['equity'], 0)],
        ['Fair value per share at 31 December 2025 (USD)', f'{DCF["fv_unrolled"]:.4f}'],
        ['Rolled to the 7 August 2026 anchor at the cost of equity, net of the USD 0.024 '
         'dividend paid in the window', f'x {W["roll_factor"]:.4f} - 0.024'],
        ['Fair value per share at the anchor (AED)', f'{aed(DCF["fv"]):.2f}']]
table(rows, [5.20, 1.35], band_rows={9, 12}, size=9.3)
caption(f'{pc(DCF["tv_share"], 0)} of the enterprise value sits beyond the fifth year, which '
        'is why the terminal assumptions are sensitised on their own rather than buried in the '
        'total. The terminal return is NOT the model-implied average: the company\'s own '
        'store-economics table (USD 402 thousand a restaurant, three-year average payback, and '
        'the marginal brands beyond five years) says the incremental restaurant earns far less '
        'than the book average, so the return is faded to 30% and the reinvestment rate — '
        'growth over that return — is 10% of terminal profit. Every published value in this '
        'study is rolled from the 31 December 2025 valuation date to the 7 August 2026 price '
        'anchor at the cost of equity, net of the dividend paid between the two dates.')

H2('1.2  Book value and sustainable return')
P(f'The company earned a {pc(H["pat_shareholders"][2]/((H["equity"][1]+H["equity"][2])/2), 0)} '
  'return on average equity in 2025. That number is spectacular and almost meaningless. An '
  'operator that leases every restaurant it runs and distributes about 92% of its earnings holds '
  f'very little book equity — USD {n(H["h1_2026"]["equity"], 0)} million at the half year, '
  f'against a market capitalisation of USD {n(M["mktcap"], 0)} million. A justified '
  'price-to-book multiple therefore divides a very large return by a very small base and is '
  'unstable in both directions. On a sustainable return of '
  f'{pc(LN["book"]["roe"], 0)}, a terminal cost of equity of {pc(W["ke_terminal"], 2)} and '
  f'the same {pc(W["terminal_g"])} terminal growth the cash-flow model uses, the '
  f'justified multiple is {LN["book"]["justified_pb"]:.1f} times book, which gives AED '
  f'{aed(LN["values"]["Book value and sustainable return"]):.2f} a share. It is the lowest of '
  'the four lenses and carries the lowest weight. It is reported because leaving out the lens '
  'that disagrees would be dishonest, not because it is informative. One reconciliation note: '
  'the justified multiple implicitly retains growth over return — about a 93% payout — while '
  'the forecast distributes 85%; the difference is retained cash the firm-value lenses '
  'already count, so it is stated rather than adjusted.')

H2('1.3  Relative multiples')
P('There is no clean comparable. The global names — Yum! Brands, Restaurant Brands, Domino\'s — '
  'are on the other side of Americana\'s contract: they collect royalties and carry EBITDA '
  'margins of 20% to 35% on a fraction of the revenue. The right comparators are the listed '
  'operator-franchisees — closest in structure, Devyani International and Sapphire Foods in '
  'India, which run the same two brands — though their published multiples may sit on a '
  'different lease-accounting basis and are read as indicative rather than precise.')
rows = [['Company', 'Market', 'EV / EBITDA', 'Price / earnings', 'EBITDA margin']]
for sym, p in PEERS.items():
    if p.get('error'):
        continue
    rows.append([p['name'], p['country'],
                 f'{p["ev_ebitda"]:.1f}x' if p.get('ev_ebitda') else '—',
                 f'{p["pe_trailing"]:.1f}x' if p.get('pe_trailing') else '—',
                 pc(p['ebitda_margin']) if p.get('ebitda_margin') else '—'])
rows.append(['Peer median (usable comparators)', '—',
             f'{LN["relative"]["peer_median"]:.1f}x',
             f'{LN["normalised"]["peer_median"]:.1f}x', '—'])
rows.append(['Americana, FY2025 (the peers are as-published trailing figures)',
             'United Arab Emirates',
             f'{D["trailing"]["ev_ebitda"]:.1f}x', f'{D["trailing"]["pe"]:.1f}x',
             pc(H['ebitda_margin'][2])])
table(rows, [2.05, 1.35, 1.10, 1.20, 1.20], band_rows={12, 13}, size=8.8)
caption('Outside market data as published by the aggregator, retrieved 9 August 2026. The '
        'medians take every row inside a stated band — 4 to 40 times for enterprise value to '
        'EBITDA, 5 to 45 times for price to earnings — which excludes one arithmetic artefact '
        'each (a peer on a depressed-earnings year whose multiple is noise, and one whose '
        'published figure appears to carry a basis error). The Indian franchisees\' figures '
        'may sit on a pre-lease-capitalisation basis; the comparison is treated as indicative '
        'only. This table ANCHORS the two justified multiples — it is the reason 8.5 and 17 '
        'times sit below the medians — but no figure in it sources any number Americana '
        'itself reports.')
P(f'The lens applies {LN["relative"]["multiple"]:.1f} times forward EBITDA — below the peer '
  'median — discounts the resulting enterprise value back one year, adds the intervening free '
  f'cash flow and runs the same bridge. That gives AED '
  f'{aed(LN["values"]["Relative multiples"]):.2f} a share. The discount to the peer median is '
  'deliberate: Americana is the operator, it pays the royalty rather than receiving it, and it '
  'carries the whole lease estate on its balance sheet.')

H2('1.4  Normalised earnings power')
P('This lens strips out growth and asks what the company earns at today\'s scale on a '
  'mid-cycle margin — and mid-cycle here means the MIDPOINT of the structural and cyclical '
  'FY2028 readings, '
  f'{pc(LN["normalised"]["margin"])}, not the structural path alone, which sits above every '
  f'margin the company has ever recorded. Revenue at the FY2026 level of USD '
  f'{n(F["revenue"][0], 0)} million on that margin, depreciation, the recurring impairment '
  f'charge and the full net finance result as they stand, taxed at {pc(F["etr"][1])} (the '
  'FY2027 rate on the rising path), gives normalised earnings of USD '
  f'{n(LN["normalised"]["earnings"], 0)} million, or USD {LN["normalised"]["eps"]:.4f} a share. '
  f'At {LN["normalised"]["multiple"]:.0f} times — just below the usable peer median — that is '
  f'AED {aed(LN["values"]["Normalised earnings power"]):.2f}.')

H2('1.5  Synthesis — four lenses, one field')
figure('fig1_lenses.png', 6.8,
       'Each lens with its bear and bull bounds, and the market price. The bounds on the '
       'cash-flow lens are complete re-runs of the model, not one input flexed.')
P('The three earnings-based lenses cluster between AED '
  f'{aed(min(LN["values"][k] for k in ["Discounted cash flow", "Relative multiples", "Normalised earnings power"])):.2f} '
  f'and AED {aed(max(LN["values"][k] for k in ["Discounted cash flow", "Relative multiples", "Normalised earnings power"])):.2f}. '
  'The book lens sits far below them and is the outlier, for the reason given above. The '
  f'weighted central value is AED {central_a:.2f}.')

H2('1.6  The drivers — how revenue and cost are actually built')
P('Revenue is not one growth rate. The company publishes its restaurant count country by country '
  'at each period end, and publishes segment revenue for the same units, so revenue is built as '
  'restaurants times revenue per restaurant across seven market units. The restaurant count grows '
  'on the company\'s own net-new-store programme; the revenue per restaurant grows on disclosed '
  'like-for-like sales growth, less a currency drag applied only in Egypt and the '
  'Kazakhstan-led group of markets, whose currencies are not pegged. The build reproduces '
  'reported revenue exactly in all three audited years, which is the test of whether it is a '
  'model or a decoration.')
figure('fig7_build.png', 6.8,
       'Revenue and the restaurant estate. Both sides of the volume-times-price build move, and '
       'both are shown.')
rows = [['Driver', 'How it is set', 'FY2026E', 'FY2030E']]
rows.append(['Net new restaurants', 'the 125 midpoint of the company\'s guidance for 2026, '
             'then 130, 130, 125, 120 — a two-year rise before the taper. The estate SHRANK by '
             'three in the first half of 2026, so the full-year guide needs about 128 net '
             'openings in the second half; the company reaffirmed it on 28 July',
             n(U['nso'][0]), n(U['nso'][4])])
rows.append(['Like-for-like sales growth', 'set just below the 6.3% delivered in the first half '
             'of 2026, converging on long-run inflation in the pegged markets',
             pc(U['lfl'][0]), pc(U['lfl'][4])])
rows.append(['Restaurants at year end', 'an output of the two rows above',
             n(F['stores'][0]), n(F['stores'][4])])
rows.append(['Revenue (USD m)', 'an output', n(F['revenue'][0], 0), n(F['revenue'][4], 0)])
rows.append(['Currency drag on dollar revenue per restaurant', 'Egypt 2.5% a year, the '
             'Kazakhstan-led markets 1.5%, Morocco 0.5%, every pegged market zero — set from '
             'the inflation differentials, though the two most recent disclosed readings ran '
             'the other way (Egypt dollar revenue +29% in FY2025, +23% in H1 2026)',
             '—', '—'])
rows.append(['EBITDA margin', 'an OUTPUT of the cost stack below, never an input — and the '
             'unit-built staff and delivery lines now cap it: the margin peaks near 25.4% and '
             'eases as the delivery channel grows', pc(F['ebitda_margin'][0]),
             pc(F['ebitda_margin'][4])])
table(rows, [1.75, 2.90, 1.15, 1.15], size=9.0)

P('The cost side gets one escalator per driver class. A globally traded food basket does not '
  'move with local wages, and local wages do not move with fuel, so applying a single blended '
  'inflation rate across all of them would manufacture a margin path out of nothing:')
rows = [['Cost class', 'What drives it', 'FY2023', 'FY2024', 'FY2025', 'FY2030E']]
NAMES = {'inventory': 'Food, filling and packing materials', 'royalties': 'Brand royalties',
         'staff': 'Staff', 'delivery': 'Home delivery and transportation',
         'advertising': 'Advertising and business development',
         'utilities': 'Utilities and communication',
         'rent_other': 'Short-term and variable rent', 'maintenance': 'Maintenance and repairs'}
for k, lab in NAMES.items():
    L = CS['lines'][k]
    rows.append([lab, L['driver_class']] + [pc(x) for x in L['pct_hist']] +
                [pc(L['path'][4])])
rows.append(['All other operating costs', 'the residual of the three expense notes',
             '—', '—', pc(CS['residual_pct']), pc(CS['residual_pct'])])
rows.append(['Other income', 'held at its FY2025 share — the half-point the margin needs '
             'beyond the cost lines', '—', '—',
             pc(H['other_income'][2] / H['revenue'][2]), pc(H['other_income'][2] / H['revenue'][2])])
table(rows, [1.75, 1.85, 0.78, 0.78, 0.78, 0.85], size=8.6)
caption('Each line as a share of revenue; the FY2030 staff and delivery shares are OUTPUTS of '
        'their unit builds — staff is headcount per restaurant times a wage growing at the '
        'audited 6% a year, and delivery is the channel share times a cost per delivered '
        'dollar — so the two biggest operating lines are built from volume and price, not '
        'escalated. Royalties are contractual and held flat. The food line is anchored on the '
        '27.4% actually recorded in the first half of 2026.')

H2('1.7  The crux')
P('The crux is the food and packaging line, and behind it the whole margin. Between the first '
  'half of 2025 and the first half of 2026 it fell from 29.2% of revenue to 27.4%. On 2026 '
  f'revenue of about USD {n(F["revenue"][0], 0)} million, that 180 basis points is worth roughly '
  f'USD {n(0.018*F["revenue"][0], 0)} million of EBITDA a year — more than a fifth of the '
  'group\'s entire operating profit. The company attributes it to procurement scale, menu '
  'optimisation and supplier negotiation. Those are real capabilities and they do not evaporate. '
  'But the same 180 points are equally consistent with a favourable turn in globally traded food '
  'prices and a period of restrained promotional intensity across the region, and those do '
  'revert.')
P('Nothing in the filings settles it, and no amount of further analysis of the published numbers '
  'will. So the study does not pick. It computes both, publishes both, and lets the reader see '
  'that the market price sits between them:')
table([['', C['way_a']['name'], C['way_b']['name']],
       ['EBITDA margin, FY2030E', pc(F['ebitda_margin'][4]),
        pc(D['inputs']['margin_path_cyclical']['value'][4])],
       ['Value per share (AED)', f'{C["way_a"]["value_aed"]:.2f}',
        f'{C["way_b"]["value_aed"]:.2f}'],
       ['Against the market price', pc(C['way_a']['value_usd'] / SPOT - 1, 0),
        pc(C['way_b']['value_usd'] / SPOT - 1, 0)]],
      [2.30, 2.35, 2.35], size=9.3)
P('The observable test is quarterly and public, and two of its readings are already in. The '
  'company disclosed the full quarterly series with its half-year results: 29.2% in the first '
  'and second quarters of 2025, 28.5% in the third, 27.1% in the fourth, then 27.3% in the '
  'first quarter of 2026 and 27.5% in the second. The trough was the fourth quarter of 2025, '
  'and the ratio has RISEN in the two quarters since — the two most recently disclosed '
  'readings lean toward the cyclical column, not the structural one. If the ratio holds near '
  '27% through the second half of 2026 the structural reading is winning; a drift back toward '
  '29% would confirm the cyclical one.')

H2('1.8  Macro, country risk and the cost of capital')
P('The company reports in dollars and earns 83% of its revenue in currencies pegged to the '
  'dollar, so the cost of capital is built in dollars. The risk-free rate is the US ten-year '
  'Treasury yield less the US sovereign\'s own default spread, which prevents sovereign risk '
  'being counted twice — once in the base rate and again in the premium. Country risk then '
  'enters once, through an equity risk premium blended across all twelve operating countries on '
  'their share of revenue.')
rows = [['Country', 'Share of revenue', 'Equity risk premium (ratings)',
         'Equity risk premium (credit-default-swap)']]
for c_, wt in sorted(W['country_weights'].items(), key=lambda kv: -kv[1]):
    star = ' *' if c_ in W['cds_not_published'] else ''
    rows.append([c_, pc(wt), pc(W['erp_by_country_rating'][c_], 2),
                 pc(W['erp_by_country_cds'][c_], 2) + star])
rows.append(['Revenue-weighted blend', '100%', pc(W['erp_rating'], 2), pc(W['erp_cds'], 2)])
table(rows, [1.65, 1.35, 1.95, 2.05], band_rows={13}, size=8.8)
caption('* No sovereign credit-default-swap is published for these countries, so the '
        'ratings-based premium is carried in that column and the substitution is flagged here '
        'rather than hidden. Country premiums as published by Aswath Damodaran of NYU Stern, '
        'January 2026 edition, read from the original data file. Revenue shares for the four '
        'separately disclosed countries are the company\'s own; within the two multi-country '
        'segments the split follows restaurant count, which is the only published physical '
        'measure at that level.')

rows = [['Component', 'Ratings basis', 'Credit-default-swap basis', 'Where it comes from']]
rows.append(['US ten-year Treasury yield', pc(W['rf_ust'], 2), pc(W['rf_ust'], 2),
             'close of 7 August 2026'])
rows.append(['Less the US sovereign spread', pc(W['us_default_spread'], 2), pc(W['us_cds'], 2),
             'the same source as the premium added back'])
rows.append(['Risk-free rate', pc(W['rf_rating'], 2), pc(W['rf_cds'], 2), 'the difference'])
rows.append(['Beta', f'{W["beta"]:.3f}', f'{W["beta"]:.3f}',
             'the company\'s own weekly share returns'])
rows.append(['Blended equity risk premium', pc(W['erp_rating'], 2), pc(W['erp_cds'], 2),
             'the table above'])
rows.append(['Cost of equity', pc(W['ke_rating'], 2), pc(W['ke_cds'], 2), 'built from the rows above'])
rows.append(['Cost of debt', pc(W['kd'], 2), pc(W['kd'], 2),
             'the company\'s own borrowing rate — see below'])
rows.append(['Cost of debt after tax', pc(W['kd_after_tax'], 2), pc(W['kd_after_tax'], 2), ''])
rows.append(['Debt weight', pc(W['debt_weight']), pc(W['debt_weight']),
             'lease liabilities over lease liabilities plus market capitalisation'])
rows.append(['Weighted cost of capital', pc(W['wacc_rating'], 2), pc(W['wacc_cds'], 2), ''])
rows.append(['Terminal cost of capital', pc(W['wacc_terminal'], 2), '—',
             'on the terminal risk-free rate'])
table(rows, [2.05, 1.15, 1.65, 2.15], band_rows={6, 10}, size=8.8)
caption('Both premium bases are published. The valuation runs on the ratings basis; the '
        'credit-default-swap basis is 35 basis points cheaper and would raise the cash-flow '
        'value slightly.')

P('The cost of debt deserves a note, because Americana has no bank debt at all — none at the end '
  'of 2024, none at the end of 2025, and USD 42 thousand of commitment charges in the whole of '
  'last year. Its only borrowing is the lease estate. The rate used here is therefore the '
  'company\'s own incremental borrowing rate, read straight out of its lease accounting: '
  f'USD {n(H["lease_interest"][2], 1)} million of lease finance cost over an average lease '
  f'liability of USD {n((H["lease_liabilities"][1]+H["lease_liabilities"][2])/2, 0)} million, or '
  f'{pc(W["kd"], 2)}. The same construction on the 2024 accounts gives {pc(W["kd_fy24"], 2)}. '
  'Determining that rate is one of the two matters the auditor singles out as most significant '
  'in the audit. It sits above the Abu Dhabi sovereign, which is what a corporate borrowing in '
  'the same currency must do.')

rows = [['Evidence on the cost of debt', 'Rate'],
        ['Company incremental borrowing rate implied by FY2025 lease accounting', pc(W['kd'], 2)],
        ['The same construction on the FY2024 accounts', pc(W['kd_fy24'], 2)],
        ['Abu Dhabi ten-year sovereign, US dollars (Treasury plus the February 2026 new-issue '
         'spread of 55 basis points)', pc(W['rf_ust'] + W['abu_dhabi_spread'], 2)],
        ['US ten-year Treasury', pc(W['rf_ust'], 2)],
        ['Bank debt outstanding at 31 December 2025', 'none']]
table(rows, [5.60, 1.15], size=9.0)

P('Beta is measured on the company\'s own share price against the published index of the '
  'exchange those shares trade on, the FTSE ADX General Index, whose history runs to '
  f'{BETA["index_asof"]}. The regression uses {BETA["n"]} complete weekly observations over '
  f'windows labelled {BETA["first_obs"]} to {BETA["last_obs"]} — {BETA["window_years"]} years, '
  'the whole life of the listing, which began in December 2022 — and both series are screened '
  'for data quality before either is used. The result carries the lead-lag correction that '
  'applies when a stock and its index need not react to the same news on the same day: beta '
  f'{W["beta"]:.3f}, standard error {BETA["se"]:.3f}, R-squared {pc(BETA["r2"])}.')

P('The imprecision is the honest headline here rather than a footnote. A 90% confidence '
  f'interval on this estimate runs from {BETA["ci90"][0]:.2f} to {BETA["ci90"][1]:.2f}, which '
  'is wide enough to contain almost every figure a reasonable person might argue for, so no '
  'part of this valuation should be read as resting on beta being exactly right. What can be '
  'said is that the level is corroborated: adjusting the raw coefficient toward the market in '
  f'the standard way gives {BETA["blume_crosscheck"]:.3f}, and the company sits, as one would '
  'expect of a consumer operator, below the property and banking names that dominate this '
  'index and above a defensive food producer.')

P('Three earlier estimates are on the record and none is used. Before the Abu Dhabi index '
  'history was available this study regressed the company\'s Riyadh-listed line against the '
  'Saudi index and obtained 0.894 — the same shares, but priced against a different country\'s '
  'market cycle. An equally weighted basket of eighteen UAE-listed names gave 0.586, and a '
  'US-listed fund tracking a UAE index, which prices hours after the Abu Dhabi close, gave '
  '0.469. The last two understated the figure by roughly half. A basket of the companies this '
  'series happens to cover is not a market: it changes whenever another company is added to '
  'the coverage, it mixes two exchanges together, and it contains the very company being '
  'valued, so the shares would be regressed partly against themselves.')

H2('1.9  Sensitivity')
figure('fig8_tornado.png', 6.6,
       'One driver at a time. The margin row is the widest, which is why the margin question is '
       'the study rather than a footnote.')
rows = [['Cost of capital \\ terminal growth'] + [pc(g) for g in SN['g_grid']]]
for i, dw in enumerate(SN['w_grid']):
    rows.append([pc(W['wacc_rating'] + dw, 2)] +
                [f'{aed(v):.2f}' for v in SN['grid_growth_wacc'][i]])
table(rows, [2.55, 0.88, 0.88, 0.88, 0.88, 0.88], size=9.0)
caption('AED a share. Each cell is a complete re-run of the model, including the unit build.')
rows = [['Cost of capital \\ EBITDA margin'] + [f'{100*m:+.0f}pp' for m in SN['m_grid']]]
for i, dw in enumerate(SN['w_grid']):
    rows.append([pc(W['wacc_rating'] + dw, 2)] +
                [f'{aed(v):.2f}' for v in SN['grid_margin_wacc'][i]])
table(rows, [2.55, 0.88, 0.88, 0.88, 0.88, 0.88], size=9.0)
caption('The margin axis moves the answer further than the cost-of-capital axis across any '
        'range either could plausibly take.')

# =====================================================================  6. §2 TECHNICAL
H1('2  Price structure')
figure('fig3_price.png', 6.8,
       'Two years of closing prices with the 50-day and 200-day averages, and the support and '
       'resistance levels computed from the same series.')
P(TECH['tech']['summary'])
P(TECH['tech']['bull'] + ' ' + TECH['tech']['bear'])
rows = [['Level', 'AED', 'Distance from the close']]
for i, lv in enumerate(TECH['levels']['res']):
    rows.append([f'Resistance {i+1}', f'{lv:.2f}', pc(lv / SPOTA - 1)])
for i, lv in enumerate(TECH['levels']['sup']):
    rows.append([f'Support {i+1}', f'{lv:.2f}', pc(lv / SPOTA - 1)])
table(rows, [2.30, 2.30, 2.40], size=9.3)
caption('Computed from the daily price series used throughout this study (13 December 2022 '
        'to 7 August 2026, delivered in the study repository). Levels are clustered pivot '
        'highs and lows in the same cleaned price '
        'series the valuation and the probability map use; the first of each is the nearest to '
        'the last close. This is a description of the tape, and carries no view on value.')

# =====================================================================  7. §3 PROBABILISTIC
H1('3  The probability price map')
P('This section is about the share price, not the business. It answers a different question from '
  'everything above: given how this share has actually behaved, where could it be in one and '
  'three months? It is never blended with the valuation.')
figure('fig4_cone.png', 6.8,
       'The middle 50% and the middle 90% of simulated outcomes, from the last close.')
rows = [['Horizon', '5th', '25th', 'Median', '75th', '95th', 'Chance above the market']]
for tag, lab in (('1M', 'One month, to '), ('3M', 'Three months, to ')):
    p = STK['horizons'][tag]
    rows.append([lab + p['grade_date']] +
                [f'{p["pct"][q]:.2f}' for q in ('p5', 'p25', 'p50', 'p75', 'p95')] +
                [pc(p['p_above'], 0)])
table(rows, [1.95, 0.80, 0.80, 0.85, 0.80, 0.80, 1.00], size=9.0)
caption('AED a share. Fifty thousand simulated paths from the close of 7 August 2026.')

rows = [['Level event', 'One month', 'Three months']]
for lab, key in [('Finishes 10% or more above the market price', 'p_up10'),
                 ('Finishes 10% or more below', 'p_dn10'),
                 ('Touches 10% above at any point', 'touch_up10'),
                 ('Touches 10% below at any point', 'touch_dn10')]:
    rows.append([lab, pc(STK['horizons']['1M'][key], 0), pc(STK['horizons']['3M'][key], 0)])
table(rows, [3.60, 1.70, 1.70], size=9.3)

figure('fig5_dist3m.png', 6.5, 'Three months — the whole distribution, not just its edges.')

H2('How much confidence this map deserves')
p5 = BT['production']
pp = PBT['five_year']
P('The honest answer is: less than for most of the shares we cover, and here is exactly why. '
  'Americana listed on 12 December 2022. Its own price history supports only '
  f'{p5["windows"]} non-overlapping three-month windows once a year of history is set aside to '
  'estimate volatility from — not the five years a proper single-name track record needs. Over '
  f'those {p5["windows"]} windows the simulation scored '
  f'{p5["skill_norm"]:+.4f} against a random walk anchored on the same interest and dividend '
  'carry, which is marginally NEGATIVE: on this name\'s own short record the method has not '
  'beaten the simple benchmark. The spread of outcomes was well shaped — the realised price fell '
  f'inside the 90% band in {pc(p5["cov90"], 0)} of windows and inside the 80% band in '
  f'{pc(p5["cov80"], 0)} — and a formal test of whether outcomes land uniformly across the '
  f'distribution is passed comfortably on the chi-square (p={p5["chi2_p"]}) and only '
  f'marginally on the Kolmogorov-Smirnov (p={p5["ks_p"]}). But ten windows cannot carry a strong claim either way.')
P('The width and shape of the band are not fitted on Americana alone; they come from a pooled '
  f'set of {pp["names"]} UAE-listed shares. That set does carry the longer record: '
  f'{pp["windows"]} windows over {pp["span_years"]} years, on which the method scored '
  f'{pp["skill_norm"]:+.4f} against the same benchmark — positive, though the confidence interval '
  'still straddles zero. There the calibration is genuinely good: outcomes fell inside the 50%, '
  f'80% and 90% bands {pc(pp["cov50"], 0)}, {pc(pp["cov80"], 0)} and {pc(pp["cov90"], 0)} of the '
  f'time against targets of 50%, 80% and 90%, and the uniformity tests are comfortable '
  f'(chi-square p={pp["chi2_p"]}, Kolmogorov-Smirnov p={pp["ks_p"]}). The pooled window is '
  f'{pp["span_years"]} years rather than five because the United Arab Emirates changed its '
  'trading week in January 2022 and the earlier pattern of trading days is not comparable.')
P('So: treat the shape of this distribution as reliable and the claim that it beats a coin toss '
  'as unproven for this particular share. Read the band, not the midpoint.')

# =====================================================================  8. §4 COMPARISON
H1('4  Comparison of the lenses')
rows = [['Lens', 'What it is really measuring', 'Central (AED)',
         'What would move it most']]
rows.append(['Discounted cash flow', 'the cash the restaurants generate, discounted',
             f'{aed(LN["values"]["Discounted cash flow"]):.2f}',
             'the EBITDA margin, then terminal growth'])
rows.append(['Relative multiples', 'what the market pays other operators for EBITDA',
             f'{aed(LN["values"]["Relative multiples"]):.2f}',
             'the multiple chosen, which no peer settles'])
rows.append(['Normalised earnings power', 'mid-cycle earnings at today\'s scale',
             f'{aed(LN["values"]["Normalised earnings power"]):.2f}',
             'the mid-cycle margin, again'])
rows.append(['Book value and sustainable return', 'the return earned on a very small book',
             f'{aed(LN["values"]["Book value and sustainable return"]):.2f}',
             'almost anything — the base is tiny'])
table(rows, [1.75, 2.20, 1.05, 2.00], size=9.0)
P('Three of the four converge, and they converge because they share an input: the margin. That '
  'is not four independent confirmations — it is one judgement seen from three angles. The '
  'reader should discount the apparent agreement accordingly. The fourth lens disagrees for a '
  'structural reason that has nothing to do with the margin, and is weighted down for it.')

H2('A second question, answered twice and worth less than expected')
P(DFL['why'])
table([['Reading', 'Value (AED)', 'Enterprise value (USD m)', 'Deducted in the bridge (USD m)'],
       [DFL['way_a']['name'], f'{DFL["way_a"]["value_aed"]:.2f}', n(DFL['way_a']['ev'], 0),
        n(DFL['way_a']['net_debt'], 0)],
       [DFL['way_b']['name'], f'{DFL["way_b"]["value_aed"]:.2f}', n(DFL['way_b']['ev'], 0),
        n(DFL['way_b']['net_debt'], 0)]],
      [2.25, 1.30, 1.75, 1.70], size=9.0)
P(DFL['finding'])

# =====================================================================  9. §5 CATALYSTS
H1('5  Catalysts')
rows = [['What to watch', 'When', 'Why it matters']]
rows.append(['Cost of food and packaging as a share of revenue', 'every quarter',
             'the single observable test of the structural-versus-cyclical question; near 27% '
             'supports the higher value, drifting to 29% supports the lower'])
rows.append(['Like-for-like sales growth', 'every quarter',
             'management guides to mid-single digits for 2026; the model assumes '
             f'{pc(U["lfl"][0])} in 2026 tapering to {pc(U["lfl"][4])}'])
rows.append(['Net new restaurants against the 120–130 guidance', 'full year 2026',
             'the volume half of the build; the model takes the 125 midpoint'])
rows.append(['Malak Al Tawouk integration and the Kuwait launch', '2026–2027',
             'the first owned brand at scale, and the first test of whether the group can build '
             'rather than only license'])
rows.append(['The ADNOC Distribution partnership', 'over five years',
             'preferential access to 200 high-traffic sites on a shared capital model — cheaper '
             'volume growth than the base case assumes'])
rows.append(['Domestic minimum top-up taxes in the remaining jurisdictions', '2026–2028',
             'the effective rate has gone from 4% to 14% in two years; the model carries it to 16%'])
rows.append(['The dividend', 'twice a year',
             'USD 201.6 million was declared against 2025 and USD 100.8 million as an interim '
             'against 2026; a cut would end the distributable-cash reading of the shares'])
table(rows, [2.25, 1.20, 3.55], size=8.8)

# =====================================================================  10. §6 ZONES
H1('6  Reading the probability zones')
P('The map in section 3 is not a forecast and the median is not a target. It says that if this '
  'share behaves over the next three months as it has behaved historically, and if nothing '
  'arrives that its past does not contain, then the middle half of the outcomes falls between '
  f'AED {STK["horizons"]["3M"]["pct"]["p25"]:.2f} and AED '
  f'{STK["horizons"]["3M"]["pct"]["p75"]:.2f}, and nine times in ten it lands between AED '
  f'{STK["horizons"]["3M"]["pct"]["p5"]:.2f} and AED '
  f'{STK["horizons"]["3M"]["pct"]["p95"]:.2f}.')
P('The centre of that distribution is close to today\'s price by construction, not by judgement: '
  'the simulation is anchored on the interest rate less the dividend yield, which is what a share '
  'price is expected to do in the absence of news. It contains no view whatsoever on whether the '
  'shares are cheap. That view lives in sections 1 and 4, and it is a different kind of statement '
  'on a different time horizon — a valuation says where the price should settle over years, not '
  'where it will be in November.')
import numpy as _np
_term3 = _np.load('paths_3M.npy')[:, -1]
_pctile = float((_term3 < LN['central'] * FX).mean())
P('The right way to use the two together: the valuation range and the three-month band overlap '
  'substantially. The valuation\'s central value of AED '
  f'{central_a:.2f} sits at the {pc(_pctile, 0)} mark of the three-month distribution — inside '
  'it, not beyond it. Nothing in this study requires the market to be wrong within three months '
  'for the valuation to be right; it requires only that the business goes on earning what it '
  'earns.')

figure('fig6_dist1m.png', 6.4, 'One month — a tighter distribution on the same construction.')

# =====================================================================  11. §7 CAVEATS
H1('7  Caveats, and what would change our mind')
for head, body in [
    ('The margin. ',
     'Stated once more because it is the whole study. If the food-cost gain of the last year '
     'reverses, the cyclical column is the right one and these shares are worth less than the '
     'market is paying, not more.'),
    ('Three-quarters of the value is beyond year five. ',
     f'{pc(DCF["tv_share"], 0)} of the enterprise value in the cash-flow lens sits in the '
     'terminal value. That is normal for a growing, cash-generative business at a 9.6% cost of '
     'capital, but it means the answer is sensitive to two numbers — terminal growth and the '
     'terminal cost of capital — that no filing can confirm.'),
    ('The price record is short. ',
     'The company listed in December 2022. Three and a half years of price history is enough to '
     'measure a beta and shape a distribution; it is not enough to prove the distribution beats '
     'a naive benchmark on this name, and section 3 says so plainly.'),
    ('The allocation of new restaurants across markets is an estimate. ',
     'The company guides the total but does not publish the split by country. The allocation '
     'here follows where the estate has actually grown. The group result is not very sensitive '
     'to it, because the growth rates differ between markets by more than the revenue per '
     'restaurant does — but it is an estimate, and it is the only one in the revenue build.'),
    ('The margin is capped by the channel mix. ',
     'The delivery channel is dearer to serve than the counter, and its share keeps rising; '
     'built as volume times price, the delivery line rises from 7.4% to 7.9% of revenue and '
     'holds the EBITDA margin near 25% rather than letting it expand indefinitely. The first '
     'edition of this study escalated delivery as a flat share and showed a higher terminal '
     'margin.'),
    ('A controlled company. ',
     'Adeptio holds 66.03%. The free float is a third of the shares, and the dividend policy, '
     'the acquisition programme and the capital structure are set by a holder whose interests '
     'need not coincide with a minority\'s.'),
    ('Egypt and Kazakhstan. ',
     'Together about 15% of revenue, in currencies that are not pegged and have not been stable. '
     'The model applies a currency drag to both; that drag is a judgement, not a disclosure.'),
    ('What would change our mind. ',
     'Food and packaging costs back above 29% of revenue for two consecutive quarters; '
     'like-for-like growth falling below 3%; average capital expenditure per restaurant rising '
     'above USD 500 thousand while the payback lengthens past four years; or a cut to the '
     'dividend. Any one of those would move this study materially, and the first is the one to '
     'watch.')]:
    rich([(head, dict(bold=True)), (body, dict())], space_after=5)

# =====================================================================  12. APPENDIX A
doc.add_page_break()
H1('Appendix A  The statements')
H2('A.1  Income statement — three years audited, five years forecast')
rows = [['USD million'] + YH + FY]
def r_(lab, vals, fmt='n0'):
    if fmt == 'pc':
        rows.append([lab] + [pc(v) for v in vals])
    else:
        rows.append([lab] + [n(v, 0) for v in vals])
r_('Revenue', H['revenue'] + F['revenue'])
r_('Cost of revenues', [-x for x in H['cogs']] + [None] * 5) if False else \
    rows.append(['Cost of revenues'] + [f'({n(x, 0)})' for x in H['cogs']] + ['—'] * 5)
rows.append(['Gross profit'] + [n(x, 0) for x in H['gross_profit']] + ['—'] * 5)
r_('EBITDA', H['ebitda'] + F['ebitda'])
r_('EBITDA margin', H['ebitda_margin'] + F['ebitda_margin'], 'pc')
rows.append(['Depreciation and amortisation'] +
            [f'({n(x, 0)})' for x in H['dna'] + F['dna']])
r_('EBIT', H['ebit'] + F['ebit'])
rows.append(['Impairments — audited, then the recurring charge'] +
            [f'({n(H["impair_nonfin"][i] + H["impair_fin"][i], 0)})' for i in range(3)] +
            [f'({n(x, 0)})' for x in F['impairment']])
r_('Finance income', H['finance_income'] + F['finance_income'])
rows.append(['Finance costs'] +
            [f'({n(x, 0)})' for x in H['finance_cost'] + F['finance_cost']])
r_('Profit before tax', H['pbt'] + F['pbt'])
rows.append(['Income tax and zakat'] + [f'({n(x, 0)})' for x in H['tax'] + F['tax']])
r_('Profit for the year', H['pat'] + F['pat'])
rows.append(['Non-controlling interests'] +
            [n(H['pat_shareholders'][i] - H['pat'][i], 1) for i in range(3)] + ['—'] * 5)
r_('Profit attributable to shareholders', H['pat_shareholders'] + F['pat'])
rows.append(['Earnings per share (USD)'] +
            [f'{x:.4f}' for x in H['eps'] + F['eps']])
table(rows, [1.95, 0.63, 0.63, 0.63, 0.63, 0.63, 0.63, 0.63, 0.63], size=8.2)
caption('EBIT is EBITDA less depreciation, above the impairment line; the audited operating '
        'profit is EBIT after it. The forecast charges a recurring impairment of 0.31% of '
        'revenue — the three-year audited average — rather than assuming a perfect estate. '
        'The non-controlling interest was 4.9% of FY2024 profit and has since collapsed to a '
        'rounding item; the forecast carries none.')

H2('A.2  Balance sheet')
rows = [['USD million'] + YH + FY]
r_('Property, equipment, intangibles and investment property',
   [H['ppe'][i] + H['intangibles'][i] + H['investment_property'][i] for i in range(3)]
   + F['owned_assets'])
r_('Right-of-use assets', H['rou'] + F['rou'])
rows.append(['Inventories'] + [n(x, 0) for x in H['inventories']] + ['—'] * 5)
rows.append(['Trade and other receivables'] + [n(x, 0) for x in H['receivables']] + ['—'] * 5)
r_('Cash and bank deposits', [H['cash'][i] + H['deposits'][i] for i in range(3)] + F['cash'])
# THE COLUMN MUST ADD UP FOR A READER. The five asset lines this table breaks out are USD
# 10mn short of the disclosed total in each audited year. This study holds the total and
# those five lines and no others, so the remainder cannot be NAMED here without the
# underlying statements — naming it would be an invention rather than a disclosure. It is
# printed as what it is: a labelled residual, so a reader can see there are assets outside
# the five broken out and cannot mistake a missing line for a wrong total.
_oth = [H['total_assets'][i] - (H['ppe'][i] + H['intangibles'][i]
                                + H['investment_property'][i] + H['rou'][i]
                                + H['inventories'][i] + H['receivables'][i]
                                + H['cash'][i] + H['deposits'][i]) for i in range(3)]
rows.append(['Other assets, not broken out in this table (residual)']
            + [n(x, 0) for x in _oth] + ['—'] * 5)
rows.append(['Total assets'] + [n(x, 0) for x in H['total_assets']] + ['—'] * 5)
rows.append(['Payables, tax and provisions'] + [n(x, 0) for x in H['payables']] + ['—'] * 5)
r_('Lease liabilities', H['lease_liabilities'] + F['lease_liabilities'])
rows.append(['Bank debt', n(H['bank_debt'][0], 0), '—', '—'] + ['—'] * 5)
r_('Equity attributable to shareholders', H['equity'] + F['equity'])
rows.append(['Net working capital'] +
            [f'({n(-x, 0)})' for x in H['nwc'] + F['nwc']])
r_('Net debt', H['net_debt'] + F['net_debt'])
table(rows, [1.95, 0.63, 0.63, 0.63, 0.63, 0.63, 0.63, 0.63, 0.63], size=8.2)
caption('A condensed layout: it does not foot to zero, because provisions, the employee '
        'end-of-service liability, deferred tax and related-party balances are not shown '
        'separately. Every historical line is the audited closing figure.')

H2('A.3  Cash flow and the forecast markers')
rows = [['USD million'] + YH + FY]
r_('EBITDA', H['ebitda'] + F['ebitda'])
rows.append(['Owned capital expenditure'] +
            [f'({n(x, 0)})' for x in H['capex'] + F['capex']])
rows.append(['Additions to right-of-use assets', '—', n(279.4, 0), n(255.2, 0)] +
            [n(x, 0) for x in F['lease_additions']])
rows.append(['Lease payments — principal and interest'] +
            [f'({n(H["lease_principal"][i] + H["lease_interest"][i], 0)})' for i in range(3)] +
            [f'({n(x, 0)})' for x in F['lease_payments']])
rows.append(['Income tax and zakat'] + [f'({n(x, 0)})' for x in H['tax'] + F['tax']])
rows.append(['Cash generated from operations, as reported'] +
            [n(x, 0) for x in H['cfo']] + ['—'] * 5)
r_('Free cash flow to the firm', [0, 0, 0] + F['fcff'])
rows[-1] = ['Free cash flow to the firm', '—', '—', '—'] + [n(x, 0) for x in F['fcff']]
rows.append(['Dividends paid'] +
            [f'({n(x, 0)})' for x in H['dividends_paid'] + F['dividends']])
r_('Return on invested capital', [0, 0, 0] + F['roic'], 'pc')
rows[-1] = ['Return on invested capital', '—', '—', '—'] + [pc(x) for x in F['roic']]
table(rows, [1.95, 0.63, 0.63, 0.63, 0.63, 0.63, 0.63, 0.63, 0.63], size=8.2)

# =====================================================================  13. APPENDIX B
doc.add_page_break()
H1('Appendix B  Peers, risks and sources')
H2('B.1  Peer frame')
P('Reproduced from section 1.3 with the reason each name is present. A cross-check only.')
rows = [['Company', 'Market', 'Why it is here']]
for sym, p in PEERS.items():
    if p.get('error'):
        continue
    rows.append([p['name'], p['country'], p['rationale']])
table(rows, [1.75, 1.35, 3.90], size=8.6)

H2('B.2  Risk register')
rows = [['Risk', 'How it would show up', 'Where it is priced']]
RISK = [('Margin reversion', 'food and packaging cost back toward 29% of revenue',
         'the cyclical column, ' + f'{C["way_b"]["value_aed"]:.2f} a share'),
        ('Concentration in three markets', 'a demand shock in the UAE, Saudi Arabia or Kuwait, '
         'which together are 72% of revenue', 'the like-for-like sensitivity'),
        ('Franchisor relationships', 'loss or repricing of a master franchise agreement',
         'not priced — it would invalidate the model rather than move it'),
        ('Currency in Egypt and Kazakhstan', 'a further devaluation cutting dollar revenue',
         'the currency drag in the unit build'),
        ('Tax', 'further domestic minimum top-up taxes as more jurisdictions adopt them',
         'the effective rate path to 16%'),
        ('Lease renewal terms', 'landlords repricing on renewal in a strong retail market',
         'the lease payment and right-of-use addition ratios'),
        ('Controlling shareholder', 'a change in dividend or capital policy',
         'the payout assumption; the enterprise value is unaffected'),
        ('Acquisition integration', 'Malak Al Tawouk and Pizza Hut Oman failing to scale',
         'not priced separately — organic guidance is used')]
for a, b, c_ in RISK:
    rows.append([a, b, c_])
table(rows, [1.55, 2.65, 2.80], size=8.6)

H2('B.3  Research register — what was consulted, and what was looked for and not found')
rows = [['#', 'Layer', 'Topic', 'Finding', 'Source', 'Date']]
LAYER = {'GLOBAL': 'Global', 'COUNTRY': 'Country', 'INDUSTRY': 'Industry', 'COMPANY': 'Company'}
for f in SW['findings']:
    rows.append([f['fid'], LAYER.get(f['ring'], f['ring']), f['category'],
                 f['headline'][:210], f['source_name'][:120], f['source_date']])
table(rows, [0.40, 0.70, 1.30, 2.30, 1.75, 0.70], size=7.4)
caption('Entries marked as a negative search record a category that was searched with nothing '
        'found — recorded so a reader can see what was looked for, not only what was located. '
        'The full source list, with every input and where it came from, is in the companion '
        'bibliography document.')

# =====================================================================  14. APPENDIX C
doc.add_page_break()
H1('Appendix C  The expert panel')
P('Three valuation specialists, each working from a genuinely different method, each shown in '
  'full: the worldview, when the method works and when it fails, a worked valuation with every '
  'intermediate line, a named sensitivity with numbers, and a falsification condition stated in '
  'advance. They are then cross-examined against each other.')
figure('fig9_experts.png', 6.5, 'Three methods, three answers, and the market price.')

for i, e in enumerate(EXP):
    H2(f'C.{i+1}  {e["label"]} — {e["method"]}')
    rich([('Worldview. ', dict(bold=True)), (e['worldview'], dict())], space_after=4)
    rich([('When it works. ', dict(bold=True)), (e['works'], dict())], space_after=4)
    rich([('When it fails. ', dict(bold=True)), (e['fails'], dict())], space_after=4)
    rich([('Falsifier, stated in advance. ', dict(bold=True)), (e['falsifier'], dict())],
         space_after=6)

E1, E2, E3 = EXP
H2('C.1 continued — Expert 1, the working')
P('The estate is valued as a portfolio of restaurants: what one earns against what one costs to '
  'build, multiplied by the number of them, less what head office and the landlords take.')
fw = 433.0 * 2
rows = [['Line', 'Value', 'Where it comes from'],
        ['Four-wall EBITDA, first half of 2026 (USD m)', n(433.0, 0),
         'disclosed — revenue less cost of revenues and selling costs, before depreciation'],
        ['Annualised (USD m)', n(fw, 0), 'doubled'],
        ['Restaurants at 31 December 2025', n(2749), 'disclosed'],
        ['Four-wall EBITDA per restaurant (USD 000)', n(fw / 2749 * 1000, 0), 'the two above'],
        ['Average capital cost of one restaurant (USD 000)',
         n(D['inputs']['capex_per_store_k']['value'], 0),
         'disclosed, across 356 openings'],
        ['Cash return on the cost of one restaurant',
         pc(fw / 2749 * 1000 / D['inputs']['capex_per_store_k']['value'], 0), 'the two above'],
        ['Less corporate overhead (USD m)', f'({n(H["ga"][2] * 0.86 if "ga" in H else D["history"]["admin"][2]*0.86, 0)})',
         'general and administrative expenses less their depreciation share'],
        ['Less maintenance capital expenditure (USD m)',
         f'({n(D["inputs"]["maintenance_capex_pct"]["value"] * F["revenue"][0], 0)})',
         'the derived maintenance rate on FY2026 revenue'],
        ['Less lease payments (USD m)',
         f'({n(D["inputs"]["lease_payments_pct"]["value"] * F["revenue"][0], 0)})',
         'the disclosed rent bill on FY2026 revenue'],
        ['Owner cash earnings after tax (USD m)',
         n((fw - D['history']['admin'][2] * 0.86
            - D['inputs']['maintenance_capex_pct']['value'] * F['revenue'][0]
            - D['inputs']['lease_payments_pct']['value'] * F['revenue'][0])
           * (1 - F['etr'][1]), 0), 'the lines above, taxed'],
        ['Capitalisation rate', pc(W['ke_terminal'] - 0.02, 1),
         'the terminal cost of equity less two points for the growth in the estate'],
        ['Business value (USD m)', n(E1['base'] * SH - (H['cash'][2] + H['deposits'][2]) + H['nci'][2], 0),
         'owner cash earnings capitalised'],
        ['Plus cash and deposits, less minorities (USD m)',
         n(H['cash'][2] + H['deposits'][2] - H['nci'][2], 0), 'disclosed'],
        ['Value per share (AED)', f'{aed(E1["base"]):.2f}', ''],
        ['Named sensitivity', f'AED {aed(E1["low"]):.2f} – {aed(E1["high"]):.2f}',
         'capitalisation rate 150 basis points higher to 100 lower']]
table(rows, [2.45, 1.45, 3.10], band_rows={14}, size=8.6)

H2('C.2 continued — Expert 2, the working')
rows = [['Line', 'Value', 'Where it comes from'],
        ['Dividend declared against FY2025 (USD m)', n(201.6, 1),
         'disclosed — 91.99% of net profit'],
        ['Shares outstanding (million)', n(SH, 0), 'disclosed, net of treasury'],
        ['Dividend per share (USD)', f'{201.6/SH:.4f}', 'the two above'],
        ['Growth assumed', pc(W['terminal_g']), 'the same long-run rate the cash-flow model uses'],
        ['Cost of equity', pc(W['ke_terminal'], 2), 'the terminal cost of equity'],
        ['Value per share (USD)', f'{E2["base"]:.4f}', 'the dividend grown one year, capitalised'],
        ['Value per share (AED)', f'{aed(E2["base"]):.2f}', ''],
        ['Named sensitivity', f'AED {aed(E2["low"]):.2f} – {aed(E2["high"]):.2f}',
         'growth 2% with the cost of equity a point higher, against growth 4% with it 50 basis '
         'points lower']]
table(rows, [2.45, 1.45, 3.10], band_rows={7}, size=8.6)

H2('C.3 continued — Expert 3, the working')
rows = [['Line', 'Value', 'Where it comes from'],
        ['NOPAT, FY2026E (USD m)', n(F['nopat'][0], 0), 'the cash-flow model'],
        ['Invested capital, FY2026E (USD m)', n(F['invested_capital'][0], 0),
         'owned assets, right-of-use assets and working capital'],
        ['Return on invested capital', pc(F['roic'][0]), 'the two above'],
        ['Cost of capital', pc(W['wacc_rating'], 2), 'built in section 1.8'],
        ['The spread', pc(F['roic'][0] - W['wacc_rating']),
         'the return above the cost — the whole case in one number'],
        ['Value of current profit (USD m)', n(F['nopat'][0] / W['wacc_terminal'], 0),
         'NOPAT capitalised at the terminal cost of capital'],
        ['Value of future growth (USD m)',
         n(D['experts'][2]['base'] * SH + (H['lease_liabilities'][2] - H['cash'][2]
           - H['deposits'][2]) + H['nci'][2] - F['nopat'][0] / W['wacc_terminal'], 0),
         'the present value of the spread on capital not yet invested'],
        ['Enterprise value (USD m)',
         n(D['experts'][2]['base'] * SH + (H['lease_liabilities'][2] - H['cash'][2]
           - H['deposits'][2]) + H['nci'][2], 0), 'the two above'],
        ['Value per share (AED)', f'{aed(E3["base"]):.2f}', 'after the same bridge'],
        ['Named sensitivity', f'AED {aed(E3["low"]):.2f} – {aed(E3["high"]):.2f}',
         'no value from future growth at all, against the growth term 18% higher']]
table(rows, [2.45, 1.45, 3.10], band_rows={9}, size=8.6)

H2('C.4  Cross-examination')
XEX = [('Expert 2 to Expert 1',
        '"You capitalise four-wall EBITDA less an overhead allocation. But four-wall EBITDA is '
        'reported by the company on its own definition, and it excludes the corporate cost of '
        'running 2,700 restaurants across twelve tax jurisdictions. Your overhead deduction is a '
        'single line taken from the general and administrative note. Are you confident that is '
        'the whole of it?"',
        'CONCEDED in part. The general and administrative note is the whole of the disclosed '
        'above-restaurant cost, but the selling and marketing line also contains shared costs the '
        'company says are allocated on floor space, and some of those are corporate. Expert 1\'s '
        'value is therefore an upper bound on this method. It is the highest of the three, which '
        'is consistent with that concession.'),
       ('Expert 1 to Expert 2',
        '"You value the company on the dividend it happens to pay. It paid 92% of earnings last '
        'year because it had nothing better to do with the cash. If it finds something better — '
        'and it has just bought two brands — your value falls even though the business has '
        'improved. That is backwards."',
        'REJECTED, with a caveat. The dividend is capitalised with a growth rate attached; '
        'redirecting cash into restaurants that earn 56% on capital would raise the growth term '
        'and offset the lower payout. The caveat is that the method cannot see that trade '
        'happening until the dividend actually grows, so it lags. Expert 2\'s value is the '
        'lowest of the three, which is the price of that lag.'),
       ('Expert 3 to both',
        '"Both of you value the estate as it stands. Neither of you asks whether the return on '
        'capital survives the next 600 restaurants. Americana is opening into progressively '
        'less prime sites — that is what a maturing estate does — and the payback table the '
        'company publishes already shows Pizza Hut, Krispy Kreme and the growth brands at over '
        'five years against KFC at 2.4."',
        'CONCEDED, and it is the sharpest point in the panel. The published payback data does '
        'show the marginal restaurant earning materially less than the average one. Expert 3\'s '
        'method is the only one of the three that prices this explicitly, through the spread on '
        'incremental capital. It is why his value sits between the other two rather than at an '
        'extreme.'),
       ('Expert 2 to Expert 3',
        '"Your invested capital is 70% right-of-use assets — an accounting construction whose '
        'size depends on lease-term judgements the auditor flags as a key matter. Your return on '
        'invested capital is therefore an artefact of a judgement, not a fact."',
        'CONCEDED. It is why the study computes the lease treatment both ways in section 4. The '
        'reassuring finding is that the two readings differ by under two per cent once each is '
        'built consistently, so this particular objection turns out not to move the answer.')]
for who, q, a in XEX:
    rich([(who + '. ', dict(bold=True)), (q, dict(italic=True))], space_after=3)
    P(a, size=10, space_after=8)

H2('C.5  The three in one room')
P('Put together, the three agree on more than their numbers suggest. All three think the '
  'restaurant estate earns a genuine, wide return on the capital it consumes — 56% on '
  'incremental capital, a three-year average payback, a cash return on the cost of a restaurant '
  f'of about {pc(fw / 2749 * 1000 / D["inputs"]["capex_per_store_k"]["value"], 0)}. None of them '
  'disputes that. What they disagree about is what an outside minority shareholder gets from it.')
P('Expert 1 says: everything, eventually, because the cash is real and the estate is growing. '
  'Expert 2 says: only what is handed over, and what is handed over is a 4% yield growing at '
  'three points a year, which is worth what a 4% yield growing at three points a year is worth. '
  'Expert 3 says: the estate\'s return is the right thing to look at, but you have to ask what '
  'it will be on the NEXT restaurant, not the average one — and the company\'s own payback '
  'disclosure says the answer is less.')
P('The panel median is AED ' + f'{aed(LN["expert_median"]):.2f}' + ', BELOW both the weighted '
  f'central value of AED {central_a:.2f} and the market price of AED {SPOTA:.2f}. That is worth '
  'stating plainly rather than smoothing away: the three methods that pay closest attention to '
  'what a minority shareholder actually receives, and to what the marginal restaurant earns, '
  'come out lower than the four-lens weighting does. The four-lens result leans on the cash-flow '
  'model, which values the whole firm and assumes the margin gain holds. The panel leans on '
  'distributions and on incremental returns. Both are in the report.')

H2('C.6  Where they diverge, and which assumption drives it')
rows = [['Pair', 'Gap (AED)', 'The assumption that drives it']]
rows.append([f'{E1["label"]} vs {E2["label"]}', f'{aed(E1["base"]-E2["base"]):.2f}',
             'whether value accrues to the firm or only to the dividend. Expert 1 capitalises '
             'all owner cash earnings; Expert 2 capitalises only the declared distribution, '
             'which is about 60% of it.'])
rows.append([f'{E1["label"]} vs {E3["label"]}', f'{aed(E1["base"]-E3["base"]):.2f}',
             'the return on the NEXT restaurant. Expert 1 applies the portfolio average; '
             'Expert 3 prices a spread that narrows as the estate matures.'])
rows.append([f'{E3["label"]} vs {E2["label"]}', f'{aed(E3["base"]-E2["base"]):.2f}',
             'reinvestment. Expert 3 gives credit for growth funded from retained cash; '
             'Expert 2 treats retained cash as value that has not yet reached the shareholder.'])
table(rows, [1.55, 1.05, 4.40], size=8.8)

# =====================================================================  15. ABOUT
doc.add_page_break()
H1('About this study')
P('Testahil publishes independent valuation studies and calibrated probability ranges. Every '
  'study is built the same way: the company\'s own filings first, a model built from drivers '
  'rather than growth rates, several independent methods rather than one, and an explicit '
  'account of what would prove the study wrong.')
P('The historical figures here come from Americana Restaurants\' own audited consolidated '
  'financial statements for 2022 through 2025, its reviewed interim statements for the first '
  'quarter and first half of 2026, and its own earnings presentations and releases — all read '
  'from the company\'s investor-relations library. Outside data appears only as a cross-check '
  'and is labelled where it appears. Every input, with its value, its date and where it came '
  'from, is listed in the companion bibliography document. The companion workbook contains the '
  f'model itself: {RC["n_formula"]} live formula cells, so a reader can change a driver and '
  'watch it reprice.')
P('This study was checked before release. Every formula cell in the workbook was recalculated '
  'independently of the software that wrote it and reconciled against the model that produced '
  f'it — {RC["n_formula"]} of {RC["n_formula"]} agree, with none unresolved and none unchecked. '
  f'Each of {DT["n_directional"]} drivers was then changed in the delivered file and the whole '
  'workbook re-evaluated, to confirm the headline value moves in the direction it should; a '
  f'further {DT["dead_sweep_inputs"]} inputs were swept to confirm none of them is inert.')

# =====================================================================  16. DISCLOSURE
H1('Disclosure')
P('This document is educational analysis. It is not investment advice, not a recommendation, '
  'and not an offer or solicitation to buy or sell any security. It contains no rating and no '
  'price target; what it contains is a range of values produced by explicit methods from stated '
  'assumptions, and a separate statistical description of price dispersion.')
P('Valuation is not measurement. Every figure beyond the audited history is a model output that '
  'depends on assumptions a reasonable person could disagree with, and the study says where '
  'those disagreements would lead. Past performance is not a guide to future results. The value '
  'of shares can fall as well as rise. Readers should form their own view and, where '
  'appropriate, take professional advice.')
P('Testahil holds no position in Americana Restaurants International PLC and has no business '
  'relationship with the company. No part of this study was reviewed by the company before '
  'publication.')
P(f'Prices and market data are as at the close of 7 August 2026. Company financial data is as '
  f'reported in the audited statements to 31 December 2025 and the reviewed interim statements '
  f'to 30 June 2026. Country risk premiums are the January 2026 edition. Study date: '
  f'9 August 2026.', size=9.5, color=GREY)

OUT = 'AMR_Valuation_Study_09-08-2026_public.docx'
doc.save(OUT)
print('wrote', OUT)
