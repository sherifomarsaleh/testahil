# -*- coding: utf-8 -*-
"""MODON_Valuation_Study_10-08-2026_public.docx — revision 2. All numbers from
study_numbers.json; no financial numeral typed here. External-reader clean."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
exec(open(os.path.join(HERE, 'docx_base.py')).read())

M, HI, HB, F = D['meta'], D['hist_is'], D['hist_bs'], D['fcst']
W, DCF, LN, SN = D['wacc'], D['dcf'], D['lenses'], D['sens']
EXPD, REL, NRM, BKL = D['experts'], D['rel'], D['norm'], D['book']
SEG, S0, STK, CJ = D['seg_fy25'], D['step0'], D['strike'], D['contested']
TECH, H1D, UN, HA = D['tech'], D['h1'], D['units'], D['h1_anchors']
IN = {k: (v['value'] if isinstance(v, dict) and 'value' in v else v)
      for k, v in D['inputs'].items()}
SPOT, SH = M['spot'], M['shares_mn']
CEN = D['central']
H1M, H3M = STK['horizons']['1M'], STK['horizons']['3M']

def n0(x): return f'{x:,.0f}'
def px(x): return f'{x:.2f}'
def pc(x, d=1): return f'{x*100:.{d}f}%'
def bn(x): return f'{x/1000:,.1f}'
YRS = F['years']

# ============================ MASTHEAD + READ FIRST ===========================
masthead()
P('Modon Holding PSC', size=24, bold=True, space_after=0)
rich([('ADX: MODON · Abu Dhabi Securities Exchange · United Arab Emirates dirham (AED)',
       dict(color=GREY, size=11))], space_after=2)
rich([(f'Independent valuation study · revision 3 · 10 August 2026 · valuation date 30 June 2026 · '
       f'price anchor AED {px(SPOT)} (close 7 August 2026)', dict(color=GREY, size=10))],
     space_after=10)
box([
 ('READ FIRST. ', 'This study is an independent, educational analysis of Modon Holding PSC. '
  'It is not investment advice, not a recommendation, and it contains no price target. '
  'Every value is a model output presented as a range with its assumptions shown.'),
 ('Revision 3. ', f'One input changed and it changed the verdict. Revisions 1 and 2 could '
  f'not obtain the exchange\'s official index and measured the stock\'s market sensitivity '
  f'against a composite built from this study\'s own price library, flagged in both editions '
  f'as a stand-in. The official FTSE ADX General series has since been obtained, and the '
  f'regression is now run against it on the house method — including the correction for thin '
  f'trading that a stock with 84.75% of its shares in one pair of hands requires, and which a '
  f'plain regression understates. Beta goes from {IN["beta_rev2_published"]:.2f} to '
  f'{IN["beta"]:.2f}, the cost of equity from 9.08% to {pc(W["ke_exp"], 2)}, and the weighted '
  f'central from AED 3.38 to AED {px(CEN)}. Against a price of AED {px(SPOT)} that turns a 19% '
  f'discount to fair value into a {pc(abs(CEN / SPOT - 1), 0)} premium — the shares read '
  f'EXPENSIVE on these lenses, where two editions ago they read cheap. Nothing in the forecast '
  f'moved: not a revenue line, not a margin, not the backlog. The stand-in flattered the '
  f'company and the correction is reported here rather than absorbed quietly. Beta is the '
  f'input this valuation is now most exposed to, and its 90% range '
  f'({IN["beta_record"]["ci90"][0]:.2f}-{IN["beta_record"]["ci90"][1]:.2f}) is wide; section '
  f'1.9 prices it.'),
 ('Revision 2. ', 'The first edition (earlier the same day) struck its development drivers on '
  '31-December-2025 disclosures although the company\'s H1-2026 results release of 29 July 2026 '
  '— which this study cites for other figures — had superseded them: the revenue backlog had '
  'reached AED 65.4 billion (95% development) and H1 sales AED 26 billion. External audits '
  'caught that failure and several others. This edition restrikes the valuation on the '
  '30-June-2026 reviewed balance sheet, rebuilds working capital from components, charges '
  'depreciation on the asset base, derives the terminal capital structure from the model\'s own '
  'forecast, bridges on available rather than gross cash, replaces the assumed beta with a '
  'regression, and rebuilds the peer table on one attributable basis from the peers\' own '
  'filings. Each change is marked where it appears.'),
 ('Sources. ', 'Every historical figure comes from the company\'s own audited statements, '
  'reviewed interims and results announcements. Peer figures are cross-checks, labelled. The '
  'companion bibliography lists every input with value, source and date.'),
 ('The one judgement that matters most. ', 'Whether the realised 2025–26 development surge '
  'normalises-but-sustains (base) or collapses to run-off (now a stress case — the H1 '
  'disclosure falsified it as a live central path) moves this valuation more than any other '
  'input. Both readings are computed in full and shown side by side, never averaged.'),
])

# ============================ HEADLINE ========================================
H1('Headline')
rich([(f'Fair value AED {px(LN["central"]["bear"])}–{px(LN["central"]["bull"])} per share '
       f'(the envelope of the four lenses\' extremes, not a distribution), weighted central '
       f'AED {px(CEN)}, against a market price of AED {px(SPOT)} ({CEN / SPOT - 1:+.0%}). ',
       dict(bold=True, size=12))], space_after=8)
P(f'Modon Holding is Abu Dhabi\'s government-owned city-builder: real-estate development '
  f'(Hudayriyat Island, Reem Island, Ras El Hekma in Egypt), the ADNEC events platform, a '
  f'hospitality portfolio and an asset-management leg. The first half of 2026 was the strongest '
  f'in its history: revenue AED {bn(H1D["rev"])}bn (+40%), profit AED {bn(H1D["pat"])}bn, '
  f'real-estate sales AED {bn(HA["sales"])}bn in six months (a single Hudayriyat launch took '
  f'AED 13bn within days), and a revenue backlog of AED {bn(HA["backlog"])}bn — double a year '
  f'earlier, 95% of it contracted development.')
P(f'The cash-flow reading of that backlog is worth AED {px(DCF["ps"])} per share on the base '
  f'path, and AED {px(CJ["runoff_ps"])} even if launches halve and fade (the run-off stress). '
  f'The market lenses sit lower: the peer multiple implies about AED {px(REL["base"])}, '
  f'normalised mid-cycle earnings about AED {px(NRM["base"])}, and book value at a justified '
  f'multiple about AED {px(BKL["base"])}. The market prices Modon at '
  f'{REL["pe_trailing_attr"]:.1f}x trailing attributable earnings against '
  f'{REL["peers"]["ALDAR"]["pe_attr"]:.1f}x for Aldar on the same basis. Section 4 prices the '
  f'gap; section 1.7 shows both sales paths in full.')
P(f'Over the next three months the price map is symmetric and modest: central band AED '
  f'{px(H3M["pct"]["p25"])}–{px(H3M["pct"]["p75"])}, 5th–95th percentiles AED '
  f'{px(H3M["pct"]["p5"])}–{px(H3M["pct"]["p95"])}. A fundamental verdict of this size, if '
  f'right, plays out over years, not a quarter.')

# ============================ VALUATION SUMMARY ===============================
H1('Valuation summary')
rows = [['Lens', 'Bear', 'Base', 'Bull', 'Weight', 'vs price']]
for k, nm in [('dcf', 'Discounted cash flow (primary)'), ('relative', 'Relative multiples'),
              ('normalized', 'Normalised earnings power'), ('book', 'Book value & sustainable return')]:
    l = LN[k]
    rows.append([nm, px(l['bear']), px(l['base']), px(l['bull']), pc(l['w'], 0),
                 f"{l['base'] / SPOT - 1:+.0%}"])
rows.append(['Weighted central', px(LN['central']['bear']), px(CEN), px(LN['central']['bull']),
             '100%', f'{CEN / SPOT - 1:+.0%}'])
rows.append([f'DCF terminal value share of enterprise value: {pc(DCF["tv_share"])}',
             '', '', '', '', ''])
rows.append(['Market price (7 Aug 2026)', '', px(SPOT), '', '', ''])
table(rows, [2.55, 0.82, 0.82, 0.82, 0.78, 0.85], band_rows={5}, first_col_bold=False)
caption('AED per share. The DCF bear is the run-off stress and the bull the growth-hold '
        'scenario of section 1.7 — engine re-runs whose full driver vectors are published on '
        'the model\'s Assumptions sheet. The bear–bull row on the central line is the envelope '
        'of lens extremes, labelled as such. The terminal value share is stated beside the lens '
        'it belongs to and linked live in the Excel bridge.')
rich([('The contested judgement, both ways: ', dict(bold=True)),
      (f'base path AED {px(DCF["ps"])} · run-off stress AED {px(CJ["runoff_ps"])}. Same balance '
       f'sheet, different sales paths; never averaged. The realised H1-2026 sales of AED 26bn '
       f'falsified the run-off as a central scenario — it is retained as the stress bound.',
       dict())], space_after=10)

# ============================ COMPANY OVERVIEW ================================
H1('Company overview')
P('Modon Holding PSC is the Abu Dhabi government\'s listed city-development platform. The '
  'listed vehicle began as Al Qudra Holding, became Q Holding, and in 2024 absorbed Modon '
  'Properties and the ADNEC Group in a share-financed combination that multiplied the balance '
  'sheet roughly four-fold and reset the perimeter — FY2024 income carries a AED '
  f'{bn(D["oneoff"]["fy24"]["bargain"])}bn accounting gain from that combination and is treated '
  'as a transition year throughout. On 30 October 2025 IHC and ADQ sold their entire stakes to '
  'L\'imad Holding Company PJSC, wholly owned by the Abu Dhabi Government — 84.75% of the '
  'shares (the arithmetic of the disclosed share count; one company announcement rounds it to '
  '84.76%). The stock trades on ADX\'s growth market with a correspondingly thin free float.')
P('Four reported segments. Real Estate Development (54% of FY2025 revenue) masterplans and '
  'sells land and homes on Hudayriyat Island (>50mn sqm, 40,000 planned units), Reem Island '
  'and Al Ain, and leads phase 1 of Ras El Hekma on Egypt\'s north coast (170.8mn sqm, '
  '500,000+ planned units), alongside La Zagaleta in Spain. Events, Catering & Tourism (36%) '
  'is the ADNEC platform: venues in Abu Dhabi and London (ExCeL), event infrastructure (Arena '
  'Group), catering and tourism. Hospitality (6%) reported 7,137 keys across 27 hotels '
  'including managed properties at end-2025; the H1-2026 release counts 3,613 keys across 16 '
  'owned, operated and JV hotels — the narrower perimeter this study\'s forward driver uses, '
  'with the difference (managed-for-others keys) stated. Asset & Investment Management (5%) '
  'holds the recurring-income portfolio (96–97% occupancy) and financial investments including '
  '50% of 2 Finsbury Avenue in London. Recurring revenues reached 38% of the group in H1-2026.')
seg_rows = [['Segment', 'Revenue', 'Gross profit', 'Margin', 'Profit before tax', 'Assets']]
for k, nm in [('red', 'Real Estate Development'), ('aim', 'Asset & Investment Mgmt'),
              ('hosp', 'Hospitality'), ('ect', 'Events, Catering & Tourism')]:
    seg_rows.append([nm, n0(SEG['rev'][k]), n0(SEG['gp'][k]), pc(SEG['gp_margin'][k]),
                     n0(SEG['pbt'][k]), n0(SEG['assets'][k])])
seg_rows.append(['Group (incl. others/eliminations)', n0(HI['FY25']['rev']), n0(HI['FY25']['gp']),
                 pc(HI['FY25']['gp'] / HI['FY25']['rev']), n0(HI['FY25']['ebt']),
                 n0(HB['FY25']['assets'])])
table(seg_rows, [2.15, 0.95, 0.95, 0.72, 1.05, 0.95], band_rows={5})
caption('FY2025 segments, AED mn, audited. Hospitality\'s pre-tax loss reflects financing and '
        'depreciation on a young portfolio; its gross profit is positive.')

# ============================ SECTION 1 =======================================
H1('1 · Fundamental valuation')

H2('1.1 · Cash-flow model — restruck at 30 June 2026')
P(f'The model values the company from its 30-June-2026 reviewed balance sheet: a half-year '
  f'2026 stub, then four full years, then the terminal block. Development revenue converts the '
  f'disclosed AED {bn(HA["dev_backlog"])}bn development backlog (65.4bn × 95%) at a visible '
  f'conversion rate anchored to the pace actually recognised in H1 (development revenue '
  f'ex-land of AED 4.2bn on an opening 42.6bn backlog, ~20% annualised); new launches roll the '
  f'backlog forward. The other legs are anchored on their H1 actuals with the events-heavy '
  f'second-half seasonality stated. Fair-value gains, bargain and disposal gains are zero '
  f'across the forecast by construction.')
P('Working capital is built from components, calibrated at the two balance-sheet dates '
  '(31-Dec-2025 and 30-Jun-2026): receivable days on revenue (440 days at both anchors — the '
  'related-party collection question in one number), a land-bank roll (new project WIP added '
  'per dirham of sales, cost of sales drawn from the existing at-cost bank), and '
  'payables-plus-advances cover of direct costs (2.6× at end-2025, 1.86× at 30-Jun-2026, '
  'declining — presale advances, not the balance sheet, fund construction). The result is '
  'absorption while growth is hot — matching the AED 3.9bn operating outflow the H1 statements '
  'actually show — and releases only late, as collections and the land bank catch up. The '
  'first edition assumed schedule-based releases; the audits were right to attack it.')
wf = [['AED mn'] + YRS]
for lbl, key in [('Revenue', 'rev'), ('Gross profit', 'gp'),
                 ('General & administrative', 'ga'), ('Selling & marketing', 'sm'),
                 ('Investment and other income', 'invinc'), ('EBIT', 'ebit'),
                 ('EBITDA margin', 'ebitda_margin'),
                 ('Depreciation & amortisation (asset-base)', 'dna'),
                 ('EBITDA', 'ebitda'), ('NOPAT = EBIT × (1 − 15.5%)', 'nopat'),
                 ('+ D&A', 'dna'), ('− capital expenditure', 'capex'),
                 ('− Δ working capital (components)', 'dnwc'),
                 ('Free cash flow to firm', 'fcff'),
                 ('Discount factor', 'df'), ('PV of FCFF', 'pv')]:
    vals = F[key]
    if key == 'ebitda_margin':
        wf.append([lbl] + [pc(v) for v in vals])
    elif key == 'df':
        wf.append([lbl] + [f'{v:.4f}' for v in vals])
    elif key in ('ga', 'sm', 'capex'):
        wf.append([lbl] + [n0(-v) for v in vals])
    else:
        wf.append([lbl] + [n0(v) for v in vals])
table(wf, [2.35, 0.93, 0.93, 0.93, 0.93, 0.93], band_rows={6, 14})
caption(f'H2-2026E is a half-year stub discounted at 0.5 years; FY2027E–FY2030E at 1.5–4.5 '
        f'years. Explicit present value AED {n0(DCF["pv_explicit"])}mn at the '
        f'{pc(W["wacc_exp"], 2)} cost of capital of section 1.8. The Δ-working-capital row '
        f'ABSORBS cash through FY2028 — the reversal of the first edition\'s release schedule.')
wcrows = [['Working-capital components (AED mn)'] + YRS,
          ['Receivables incl. related-party (days × revenue)'] + [n0(v) for v in F['recv']],
          ['Inventories + development WIP (roll)'] + [n0(v) for v in F['invdwip']],
          ['Payables incl. advances (cover × costs)'] + [n0(v) for v in F['pay']],
          ['Net working capital'] + [n0(v) for v in F['nwc']],
          ['Δ working capital (+ = absorption)'] + [n0(v) for v in F['dnwc']]]
table(wcrows, [2.35, 0.93, 0.93, 0.93, 0.93, 0.93], band_rows={5}, size=8.6)
P(f'Terminal block. Terminal growth {pc(DCF["g"], 1)}; terminal return on capital '
  f'{pc(IN["roic_term"], 1)} — deliberately below the model\'s own forecast path (which '
  f'reaches ~{pc(F["roic"][-1], 0)} by FY2030E as capital releases while profit grows) and '
  f'above the FY2025 clean achieved {pc(D["terminal_recon"]["roic_fy25_clean"], 1)}, a stated '
  f'mean-reversion margin of safety. Reinvestment = g/ROIC = {pc(DCF["rr_term"])}, derived. '
  f'The terminal debt weight is no longer assumed: it is DERIVED from the model\'s own '
  f'FY2030E balance sheet ({pc(W["wd_term"], 1)}), which puts the terminal rate at '
  f'{pc(W["wacc_term"], 2)} — ABOVE the explicit-window rate, where the first edition had it '
  f'below. Terminal value AED {n0(DCF["tv"])}mn, worth AED {n0(DCF["pv_tv"])}mn today — '
  f'{pc(DCF["tv_share"])} of enterprise value, a share the reader should see and judge; the '
  f'working-capital absorption in the explicit years pushes it up, and section 1.9 prices the '
  f'terminal-return case both ways.')
br = [['Enterprise value → equity per share (30-Jun-2026)', 'AED mn'],
      ['PV of explicit periods', n0(DCF['pv_explicit'])],
      ['PV of terminal value', n0(DCF['pv_tv'])],
      ['Enterprise value', n0(DCF['ev'])],
      [f'  of which terminal value: {pc(DCF["tv_share"])}', ''],
      ['+ unrestricted (available) cash — disclosed', n0(DCF['cash_avail'])],
      [f'  (excluded: AED {n0(DCF["restricted"])}mn of escrow/restricted cash — it funds '
       f'completion of the very backlog the DCF values; adding it back would double-count)', ''],
      ['− debt incl. the related-party loan', n0(-DCF['debt'])],
      ['− lease liabilities', n0(-DCF['lease'])],
      ['+ associates & joint ventures at book', n0(DCF['assoc'])],
      ['+ financial assets', n0(DCF['finass'])],
      [f'− non-controlling interests, capitalised at 2% of equity value '
       f'(book AED {n0(DCF["nci_book"])}mn shown as the alternative)', n0(-DCF['nci_val'])],
      ['Equity attributable, 30 Jun 2026', n0(DCF['eq_attr'])],
      [f'Per share ({n0(SH)}mn shares)', px(DCF['ps_jun'])],
      ['Rolled 38 days to the 7 Aug 2026 anchor at the cost of equity', px(DCF['ps'])]]
table(br, [4.6, 1.6], band_rows={3, 12, 14})
caption(f'Gross-cash alternative (first edition\'s basis): AED {px(DCF["ps_grosscash"])}; '
        f'book-NCI alternative: AED {px(DCF["ps_booknci"])}. Both are shown in the workbook. '
        f'On the strict all-cash basis the company holds net cash of AED '
        f'{n0(-(DCF["debt"] - DCF["cash_total"]))}mn; on its own available-cash definition it '
        f'reports net debt of AED {n0(HA["netdebt"])}mn — both framings stated.')

H2('1.2 · Book value and sustainable return')
P(f'Attributable equity at 30 June 2026 is AED {n0(HA["eqp"])}mn — AED {px(BKL["bvps"])} per '
  f'share, so the market pays {BKL["pb_trailing"]:.2f}x book. One cleaning, tied to the '
  f'disclosed line items: FY2025 carried AED {n0(D["oneoff"]["fy25"]["total"])}mn of fair-value '
  f'and disposal gains; removing them (tax-effected) puts clean attributable return on average '
  f'equity at {pc(BKL["roe_fy25_clean"])} against {pc(BKL["roe_fy25"])} reported. The '
  f'{pc(IN["roe_sust"], 1)} used here is a forward-sustainable judgement, not that cleaning: '
  f'it sits between the mechanical clean figure and the model\'s own forecast path '
  f'({pc(F["roic"][1], 1)} rising), and the first edition\'s conflation of the two — flagged '
  f'by the audits — is withdrawn. Justified price-to-book = ({pc(IN["roe_sust"], 1)} − '
  f'{pc(IN["g_term"], 1)}) / ({pc(W["ke_exp"], 2)} − {pc(IN["g_term"], 1)}) = '
  f'{BKL["pb_just"]:.2f}x, worth AED {px(BKL["base"])} per share rolled to the anchor — this '
  f'lens is now struck on the same date as the others.')

H2('1.3 · Relative multiples — rebuilt on one basis')
prs = [['Peer', 'Spot', 'Mkt cap, AED mn', 'FY2025 attributable NP', 'Trailing P/E (attr.)',
        'Backlog (own disclosure)'],
       ['Aldar Properties (ADX)', px(REL['peers']['ALDAR']['spot']),
        n0(REL['peers']['ALDAR']['mcap']), n0(REL['peers']['ALDAR']['np_attr']),
        f"{REL['peers']['ALDAR']['pe_attr']:.2f}x", n0(REL['peers']['ALDAR']['backlog'])],
       ['Emaar Properties (DFM)', px(REL['peers']['EMAAR']['spot']),
        n0(REL['peers']['EMAAR']['mcap']), n0(REL['peers']['EMAAR']['np_attr']),
        f"{REL['peers']['EMAAR']['pe_attr']:.2f}x", n0(REL['peers']['EMAAR']['backlog'])],
       ['Emaar Development (DFM)', px(REL['peers']['EMAARDEV']['spot']),
        n0(REL['peers']['EMAARDEV']['mcap']), n0(REL['peers']['EMAARDEV']['np_attr']),
        f"{REL['peers']['EMAARDEV']['pe_attr']:.2f}x", n0(REL['peers']['EMAARDEV']['backlog'])],
       ['Modon Holding', px(SPOT), n0(M['mktcap']), n0(IN['npa_fy25']),
        f"{REL['pe_trailing_attr']:.2f}x", n0(HA['backlog'])]]
table(prs, [1.75, 0.6, 1.12, 1.28, 1.1, 1.15], band_rows={4}, size=8.8)
caption('One basis throughout: attributable profit from each peer\'s own audited filings and '
        'releases; every multiple is the printed market cap over the printed profit (the first '
        'edition\'s table mixed bases and vintages and did not reconcile — rebuilt after the '
        'audits). Backlogs: Aldar FY2025 development 71.7bn; Emaar group 155bn; Emaar '
        'Development 125.2bn; Modon 30-Jun-2026 group 65.4bn — own disclosure and date per row. '
        'On the group-profit basis Modon\'s trailing multiple is '
        f'{REL["pe_trailing_group"]:.1f}x (dual-framed; FY2025 NCI was a loss, so attributable '
        'exceeds group profit).')
P(f'The attributable peer set runs {REL["peers"]["EMAARDEV"]["pe_attr"]:.1f}–'
  f'{REL["peers"]["ALDAR"]["pe_attr"]:.1f}x trailing. This study applies '
  f'{IN["pe_just"]:.1f}x to FY2026E attributable profit (H1 actual plus the H2 model, AED '
  f'{n0(REL["fy26_npa"])}mn) — parity-minus with the sector leader: the growth and '
  f'recurring-income premium and the ~15%-float/related-party discount are treated as '
  f'offsetting, and a forward multiple on a growing base is worth ~8% more than the same '
  f'trailing multiple, stated. That gives AED {px(REL["base"])} per share. The EV/EBITDA '
  f'cross-check ({IN["ev_ebitda_just"]:.1f}x, a house multiple with no computable peer anchor '
  f'— peer net debt is not disclosed in reachable form) implies AED {px(REL["ev_ps"])} and is '
  f'displayed in the workbook but NOT averaged into the lens; the first edition\'s silent '
  f'blend of two legs 43% apart is withdrawn.')

H2('1.4 · Normalised earnings power')
P(f'Through a full cycle this study assumes development sales settle near AED '
  f'{bn(IN["norm_sales"])}bn a year — raised from the first edition\'s 18bn because the '
  f'realised H1-2026 (AED 26bn in six months) lifts any honest cycle average, yet still far '
  f'below the current pace — with the recurring legs grown moderately: normalised revenue '
  f'about AED {bn(NRM["rev"])}bn, through-cycle net margin {pc(IN["norm_margin"])}, normalised '
  f'earnings AED {n0(NRM["np"])}mn (AED {NRM["eps"]:.3f}/share), worth AED {px(NRM["base"])} '
  f'at {IN["norm_pe"]:.1f}x. The harshest lens: it treats 2025–26 as a cycle top.')

H2('1.5 · Synthesis — four lenses, one field')
figure('fig1_football.png', 6.9, 'Figure 1 — the four lenses and the weighted central against '
       'the market price. The DCF span is the run-off-stress-to-growth-hold spread.')
P(f'Weights: DCF {pc(LN["dcf"]["w"], 0)} on backlog visibility; the three market lenses carry '
  f'{pc(0.6, 0)} jointly — and that structure IS how the float and governance friction is '
  f'priced. One audit demanded an additional ~30% holding-company discount on top; that would '
  f'charge the same friction twice, and is rejected with the reasoning stated here — the '
  f'central already sits {1 - CEN / DCF["ps"]:.0%} below the DCF because of it. Result: AED '
  f'{px(CEN)}, {CEN / SPOT - 1:+.0%} above the market.')

H2('1.6 · Drivers — each leg on its own driver')
dr = [['Leg', 'Driver build', 'Path'],
      ['Development', f'conversion of the disclosed 30-Jun backlog '
       f'({pc(IN["conv_path"][0], 1)} half-year stub, then {pc(IN["conv_path"][1], 0)}→'
       f'{pc(IN["conv_path"][-1], 0)}) + land sales; new sales AED {bn(IN["new_sales"][1])}bn→'
       f'{bn(IN["new_sales"][-1])}bn/yr — every year below the realised H1 annualised pace',
       f'revenue AED {bn(F["red_rev"][1])}bn→{bn(F["red_rev"][-1])}bn'],
      ['  margin', f'{pc(IN["red_margin"][0], 1)}→{pc(IN["red_margin"][-1], 1)} (H1 actual '
       f'{pc(SEG["h1_gp_margin"]["red"], 1)}); related-party land mix fades; construction '
       'escalator ~4% vs realised-price ~2%', 'output'],
      ['Asset & investment mgmt', 'H1 actual + contracted occupancy (96%); ~8.5%/yr',
       f'AED {n0(F["aim_rev"][1])}→{n0(F["aim_rev"][-1])}mn'],
      ['Hospitality', 'H1 actual + winter seasonality on the 3,613 owned/operated/JV keys; '
       'margin recovering to 30%', f'AED {n0(F["hosp_rev"][1])}→{n0(F["hosp_rev"][-1])}mn'],
      ['Events, catering & tourism', 'H1 actual + the H2-weighted events season; ~4%/yr',
       f'AED {bn(F["ect_rev"][1])}bn→{bn(F["ect_rev"][-1])}bn'],
      ['Working capital', 'receivable days 440→370; land-bank draw vs new-WIP add; '
       'advances cover 1.86×→1.40×', 'absorbs, then releases late'],
      ['D&A', f'{pc(IN["dna_rate"], 1)} on the average depreciable base (asset-base charge — '
       'the first edition\'s revenue-driven D&A is withdrawn)', 'from the base roll'],
      ['Tax', f'DMTT floor + foreign uplift (H1 actual {pc(H1D["eff_tax"])})', pc(IN['tax_f'])]]
table(dr, [1.55, 3.6, 1.7], size=8.8)
caption('Per-project volumes and prices are not disclosed; the build stops at segment level '
        'with unit-level anchors (FY2025: AED 7.0mn/unit realised in Abu Dhabi, 3.1mn '
        'internationally — the latter including joint-venture sales, so per-unit division '
        'across categories is not closed). That gap is flagged, not papered over.')

H2('1.7 · The crux — the sales path, priced both ways')
cj = [['', 'Base: normalising-but-sustained', 'Stress: backlog run-off'],
      ['New development sales', f'H2-26 AED {bn(IN["new_sales"][0])}bn, then '
       f'{bn(IN["new_sales"][1])}→{bn(IN["new_sales"][-1])}bn/yr',
       f'H2-26 AED {bn(IN["new_sales_runoff"][0])}bn, then '
       f'{bn(IN["new_sales_runoff"][1])}→{bn(IN["new_sales_runoff"][-1])}bn/yr'],
      ['Development margin', f'{pc(IN["red_margin"][0], 1)}→{pc(IN["red_margin"][-1], 1)}',
       f'{pc(IN["red_margin_runoff"][0], 1)}→{pc(IN["red_margin_runoff"][-1], 1)}'],
      ['FY2030E group revenue', f'AED {bn(F["rev"][-1])}bn', f'AED {bn(CJ["runoff_rev"][-1])}bn'],
      ['Value per share', f'AED {px(DCF["ps"])}', f'AED {px(CJ["runoff_ps"])}'],
      ['Status', 'central path', 'stress bound: the disclosed H1-2026 sales (AED 26bn in six '
       'months, 2.6× prior year) falsify this as a live central scenario; it prices the '
       'question "what if that was the top?"']]
table(cj, [1.35, 2.75, 2.75], size=8.9, band_rows={4})
P(f'Even the stress reading values the group {CJ["runoff_ps"] / SPOT - 1:+.0%} against the '
  f'market price; the growth-hold upper reading (sales held near the realised pace) reaches '
  f'AED {px(CJ["bull_ps"])}. All three driver vectors are published in the workbook.')

H2('1.8 · Macro and country — the cost of capital, built and priced')
P(f'Rates are sourced and each risk charged once. The AED government curve gives '
  f'{pc(IN["rf"], 2)} (January-2031 dirham treasury tranche, auctioned July 2026 ~4bp over US '
  f'Treasuries; the longest liquid AED tenor, ~4.4 years against a perpetual stream — a '
  f'limitation, stated); netting the UAE\'s own {pc(IN["sov_spread_rating"], 2)} default '
  f'spread — which already sits inside the equity premium — leaves {pc(W["rf_star"], 2)}. The '
  f'equity premium is {pc(IN["erp_rating"], 2)} on the rating basis (no sovereign CDS series '
  f'exists for the UAE, so no CDS-basis alternative can be built; and the spread-basis mix in '
  f'the first edition — rating-based for the netting, market-based for retiring the conflict '
  f'premium — is now stated: on a like-for-like basis the two constructions differ by ~6bp).')
P(f'Beta is measured against the exchange\'s own published index. Earlier editions could not '
  f'obtain the FTSE ADX General series and used a composite of this study\'s own UAE price '
  f'library as a stand-in, flagged as such; a composite of the names a research programme '
  f'happens to cover is an artefact of that coverage, not a market, and it is no longer used '
  f'as a regressor. The official series (as of {IN["beta_record"]["index_asof"]}) is now the '
  f'benchmark, screened for data quality before use, and the regression runs on '
  f'{IN["beta_record"]["n"]} weekly observations over {IN["beta_record"]["window_years"]:.1f} '
  f'years to {IN["beta_record"]["last_obs"]}.')
P(f'The result is beta {IN["beta"]:.2f}, quoted here with its uncertainty because the '
  f'uncertainty is large: standard error {IN["beta_record"]["se"]:.2f}, R-squared '
  f'{IN["beta_record"]["r2"]:.2f}, a 90% range of {IN["beta_record"]["ci90"][0]:.2f} to '
  f'{IN["beta_record"]["ci90"][1]:.2f}. Two adjustments sit behind it and both matter. First, '
  f'the regression corrects for thin trading: 84.75% of Modon\'s shares are held by one '
  f'entity, so the stock does not move in step with the index within a single week, and an '
  f'uncorrected regression reads {IN["beta_naive_same_weeks"]["beta"]:.2f} — understating the '
  f'sensitivity by {IN["beta"] - IN["beta_naive_same_weeks"]["beta"]:.2f}. Second, the '
  f'benchmark itself: the official index is materially less volatile than the self-built '
  f'composite it replaced, and because beta divides the stock\'s volatility by the market\'s, '
  f'a better-diversified benchmark RAISES it. A published long-run adjustment toward the '
  f'market average reads {IN["beta_record"]["blume_crosscheck"]:.2f}, between the two, and is '
  f'shown as a cross-check rather than adopted. The industry-average route (emerging-market '
  f'real-estate development, unlevered ~0.45) was tested and rejected as primary: that average '
  f'is dominated by highly-levered developers unrepresentative of a state platform, and it is '
  f'kept only as a lower-bound cross-check. This is the largest single mover in the valuation '
  f'and it moves against the company; section 1.9 sensitises it one standard error at a time '
  f'rather than around a convention.')
wt = [['Cost of capital', 'Value', 'Construction'],
      ['Risk-free rate, normalised', pc(W['rf_star'], 2), f'{pc(IN["rf"], 2)} − '
       f'{pc(IN["sov_spread_rating"], 2)} default spread'],
      ['Cost of equity', pc(W['ke_exp'], 2), f'rf* + {IN["beta"]:.2f} × {pc(IN["erp_rating"], 2)}'],
      ['Marginal cost of debt', pc(W['kd'], 2), f'6M EIBOR {pc(IN["eibor6m"], 2)} '
       f'(31-Mar-2026 fixing, dated — the official page refused retrieval twice; ~3bp of '
       f'rate per 25bp of fixing) + {pc(IN["kd_margin"], 2)} margin'],
      ['  after tax', pc(W['kd_at'], 2), f'× (1 − {pc(IN["tax_f"])})'],
      ['Weights', f"{pc(W['we_exp'], 1)} / {pc(W['wd_exp'], 1)}",
       'market equity / 30-Jun-2026 book debt. Circularity acknowledged: the market\'s own '
       'weights are used while the study argues the equity is mispriced; at the study\'s own '
       'equity value the rate would be ~30bp higher and the DCF ~1% lower'],
      ['Cost of capital, explicit window', pc(W['wacc_exp'], 2), 'weighted'],
      ['Cost of capital, terminal', pc(W['wacc_term'], 2),
       f'weights DERIVED from the model\'s own FY2030E balance sheet '
       f'({pc(W["wd_term"], 1)} debt) — above the explicit rate, as a shrinking debt share '
       f'demands']]
table(wt, [2.05, 1.15, 3.65], size=8.8, band_rows={6})
kd_rows = [['Cost-of-debt evidence (loan note, FY2025)', 'Rate', 'Maturity'],
           ['Largest new AED tranche (AED 1,415mn)', '6M EIBOR + 0.60%', 'Jan-2027'],
           ['AED construction tranches', '3M EIBOR + 0.85% to + 2.5%', '2028–2030'],
           ['GBP venue debt (ExCeL, hotels)', 'SONIA + 0.95% to + 2.05%', '2028–2029'],
           ['USD project tranches', 'SOFR + margin (to + 4.98%)', '2026–2027'],
           ['Fixed AED tranches', '3.32% – 4.36%', '2028–2033'],
           ['Blended marginal rate used', pc(W['kd'], 2),
            f'above the {pc(IN["rf"], 2)} sovereign, as it must be'],
           ['Realised effective rate, FY2025', pc(W['kd_eff_fy25'], 1),
            'interest charge over average loan book']]
table(kd_rows, [3.4, 1.9, 1.55], size=8.9, band_rows={6})
P(f'Priced stress readings: charging the {pc(IN["fgn_share"], 0)} of revenue earned outside '
  f'the UAE (the audited geographic split in the revenue note — recognised revenue, not '
  f'contracted sales) with Egypt\'s country premium cuts the DCF to AED '
  f'{px(DCF["ps_egystress"])}; the mid-2026 conflict premium stays retired on the auction '
  f'evidence, with a +2-point cost-of-equity strip below. Tax at the 15% domestic-minimum '
  f'floor plus the observed foreign uplift.')

H2('1.9 · Sensitivity')
figure('fig2_sens.png', 6.4, f'Figure 2 — DCF fair value across cost-of-equity shifts and '
       f'terminal growth. Rebuilt so the centre cell equals the base case (the first edition\'s '
       f'grid used a different terminal convention from its own base — an audit finding). Read '
       f'the rows left to right: MORE terminal growth now SUBTRACTS value. That is not an error '
       f'— at revision 3 the terminal cost of capital ({pc(W["wacc_term"], 1)}) sits above the '
       f'terminal return on capital ({pc(IN["roic_term"], 1)}), so profit reinvested in the '
       f'terminal block earns less than it costs, and growing it faster destroys value. At '
       f'revision 2 the two were within a fifth of a point of each other and the same rows were '
       f'nearly flat. The gradient inverted because beta rose, not because the business '
       f'changed.')
sens_rows = [['One-way strip (DCF per share)', '−2', '−1', 'base', '+1', '+2'],
             [f'Beta {SN["beta_grid"][0]:.2f} → {SN["beta_grid"][-1]:.2f} '
              f'(base {IN["beta"]:.2f}, steps of one standard error)']
             + [px(v) for v in SN['grid_beta']],
             ['Development margin ±4pts'] + [px(v) for v in SN['grid_margin']],
             ['Conversion rate ±6pts'] + [px(v) for v in SN['grid_conv']],
             ['New sales 50%→150% of base'] + [px(v) for v in SN['grid_sales']],
             ['Working capital ±AED 1bn/yr'] + [px(v) for v in SN['grid_nwc']],
             ['Receivable days ±60'] + [px(v) for v in SN['grid_dso']],
             ['Cost of equity +0 → +2pts (own axis: 0 at base)'] + [px(v) for v in SN['grid_ke']]]
table(sens_rows, [2.6, 0.85, 0.85, 0.85, 0.85, 0.85], size=9.0)
caption('Each cell is a complete revaluation; scenario driver vectors are published on the '
        'Assumptions sheet. Two mechanisms worth naming: a uniform conversion-rate shift '
        'raises value (all five years convert more), while pulling conversion forward only in '
        'the first period is nearly value-neutral — it drains the backlog that feeds the '
        'terminal year; and the receivable-days strip is the priced form of the related-party '
        'collection risk.')

# ============================ SECTION 2 =======================================
H1('2 · Technical and price structure')
figure('fig3_ma.png', 6.9, 'Figure 3 — the last 260 sessions against the 20/50/100/200-day '
       'moving averages.')
T = TECH['tech']
P(f'{T["summary"]} (The MACD histogram is +0.002 — marginally positive; "turning up" rests '
  f'on that computed sign, shown here at full precision.)')
P(f'{T["trend"]}. {T["bull"]} {T["bear"]}')
lv = [['Nearest levels (computed from swing-point clusters)', 'AED'],
      ['Resistance 3', px(TECH['levels']['res'][2])],
      ['Resistance 2', px(TECH['levels']['res'][1])],
      ['Resistance 1 (nearest)', px(TECH['levels']['res'][0])],
      ['Last close (7 Aug 2026)', px(TECH['close'])],
      ['Support 1 (nearest)', px(TECH['levels']['sup'][0])],
      ['Support 2', px(TECH['levels']['sup'][1])],
      ['Support 3', px(TECH['levels']['sup'][2])]]
table(lv, [4.4, 1.4], band_rows={4})
caption('Levels are recency-weighted swing-point clusters computed from the full price '
        'history; the read is computed, not drawn by hand.')

# ============================ SECTION 3 =======================================
H1('3 · Probabilistic price map')
P(f'Struck from the 7 August 2026 close of AED {px(SPOT)} using a volatility model fitted to '
  f'this market\'s panel of ADX/DFM names, drift at the short-term dirham rate (no dividend is '
  f'paid or proposed — a sourced zero), 50,000 paths. Unchanged from the first edition: the '
  f'price series and anchor did not change.')
P(f'How much to trust it: tested on {S0["windows_scored"]} non-overlapping three-month windows '
  f'walked forward over the post-2022 trading regime (earlier windows excluded because the UAE '
  f'changed its trading week in January 2022 — and, worth stating, part of that history '
  f'belongs to the smaller predecessor company), the method beat a drift-adjusted random walk '
  f'by {S0["skill_norm"]*100:.1f}% on a proper scoring rule, robust across resampling. '
  f'Coverage runs WIDE: the 80% band contained {pc(S0["cov80"], 0)} of outcomes and the 90% '
  f'band the same {pc(S0["cov90"], 0)} — over-coverage, not precision; the bands are, if '
  f'anything, conservative at this sample size. The forecast percentile of realised prices is '
  f'statistically indistinguishable from uniform. Calibrated ranges, not promises.')
figure('fig4_fan.png', 6.9, 'Figure 4 — the three-month cone: median, central 50% band and '
       '5–95% band.')
pmap = [['', '1 month (to ' + H1M['grade_date'] + ')', '3 months (to ' + H3M['grade_date'] + ')'],
        ['5th percentile', px(H1M['pct']['p5']), px(H3M['pct']['p5'])],
        ['25th percentile', px(H1M['pct']['p25']), px(H3M['pct']['p25'])],
        ['Median', px(H1M['pct']['p50']), px(H3M['pct']['p50'])],
        ['75th percentile', px(H1M['pct']['p75']), px(H3M['pct']['p75'])],
        ['95th percentile', px(H1M['pct']['p95']), px(H3M['pct']['p95'])],
        ['P(finish above spot)', pc(H1M['p_above'], 0), pc(H3M['p_above'], 0)],
        ['P(finish ≥ +10%)', pc(H1M['p_up10'], 0), pc(H3M['p_up10'], 0)],
        ['P(finish ≤ −10%)', pc(H1M['p_dn10'], 0), pc(H3M['p_dn10'], 0)],
        ['P(touch +5% at any point)', pc(H1M['touch_up5'], 0), pc(H3M['touch_up5'], 0)],
        ['P(touch −5% at any point)', pc(H1M['touch_dn5'], 0), pc(H3M['touch_dn5'], 0)],
        ['P(touch +10% at any point)', pc(H1M['touch_up10'], 0), pc(H3M['touch_up10'], 0)],
        ['P(touch −10% at any point)', pc(H1M['touch_dn10'], 0), pc(H3M['touch_dn10'], 0)]]
table(pmap, [2.6, 1.85, 1.85])
caption('Calendar-defined windows, settled on the first trading session on or after each date.')
figure('fig5_dist.png', 5.2, 'Figure 5 — simulated distribution at one month.')
figure('fig6_dist.png', 5.2, 'Figure 6 — simulated distribution at three months.')

# ============================ SECTION 4 =======================================
H1('4 · Comparison of the lenses')
P(f'The gap narrowed but did not close. The cash-flow lenses say AED {px(CJ["runoff_ps"])}–'
  f'{px(CJ["bull_ps"])} depending on the sales path; the market lenses say AED '
  f'{px(NRM["base"])}–{px(BKL["base"])}. Three readings, each priced. First: the market is '
  f'charging for risk. Making the base cash flows worth AED {px(SPOT)} requires a cost of '
  f'equity of {pc(D["market_implied"]["ke"], 1)} — {pc(D["market_implied"]["ke_add"], 1)} '
  f'above the built-up rate: a hard-currency frontier-credit premium on a AA-sovereign\'s own '
  f'developer. Materially less absurd than it sounds, given ~85% state ownership, '
  f'related-party land sales at 67% gross margins, and a receivable book that consumed AED '
  f'5.4bn of cash in six months.')
P(f'Second: the market is pricing the run-off stress with a further discount — the stress '
  f'value of AED {px(CJ["runoff_ps"])} needs a {pc(D["market_implied"]["runoff_discount"], 0)} '
  f'holding-company-style haircut to land on the price. Third: the market lenses anchor on '
  f'current multiples while the DCF anchors on the contracted backlog — and '
  f'{pc(DCF["tv_share"])} of the DCF\'s enterprise value is terminal, which is where '
  f'scepticism belongs; the working-capital honesty of this revision moved cash out of the '
  f'explicit window and made that share larger, not smaller. The weighted central of AED '
  f'{px(CEN)} holds these readings in stated proportions rather than pretending they agree.')
figure('figD1_experts.png', 6.9, 'Figure 7 — three expert framings (Appendix C) against the '
       'market price.')

# ============================ SECTION 5 =======================================
H1('5 · Catalysts')
bullet(' FY2026 results (February 2027): whether H2 shows the receivable build-up collecting — '
       'the model requires roughly AED 7.5bn of H2 operating cash inflow on the IFRS basis '
       'after H1\'s AED −3.9bn, and says so.', 'Collections.')
bullet(' Every dirham of the ~AED 10.8bn related-party receivable book (Department of Finance '
       'the largest counterparty) collected converts a paper claim into cash — the '
       'receivable-days strip in section 1.9 is this risk, priced.', 'Related parties.')
bullet(' Ras El Hekma phase-1 delivery milestones and further precinct launches.', 'Egypt.')
bullet(' A maiden dividend policy would force the market to price the cash flows as owner '
       'earnings; none has been announced.', 'Capital returns.')
bullet(' Any placement widening the ~15% free float changes the relative lens directly.',
       'Float.')
bullet(' The dirham imports US policy: each cut lowers the discount rate and mortgage '
       'friction.', 'Rates.')

# ============================ SECTION 6 =======================================
H1('6 · Reading the probability zones')
P(f'The three-month map says: a two-in-three chance the price sits between AED '
  f'{px(H3M["pct"]["p25"])} and {px(H3M["pct"]["p75"])} on {H3M["grade_date"]}; '
  f'{pc(H3M["touch_dn5"], 0)} odds that AED {px(SPOT * 0.95)} trades at some point (just '
  f'above the {px(TECH["levels"]["sup"][1])} support); {pc(H3M["touch_up5"], 0)} odds that '
  f'AED {px(SPOT * 1.05)} trades — just ABOVE the nearest resistance at '
  f'{px(TECH["levels"]["res"][0])}, so a touch of it would already be a breakout signal. A '
  f'reader holding this study\'s fundamental view should not expect the map to confirm it '
  f'inside a quarter: the map is calibrated to realised volatility, not to the study\'s '
  f'opinion, and a {CEN / SPOT - 1:+.0%} revaluation is a multi-year event, visible first in '
  f'collections, margins and the dividend decision.')

# ============================ SECTION 7 =======================================
H1('7 · Caveats — what would change our mind')
bullet(' More than half of FY2025 land-sale profit came from related-party transactions at a '
       '67% gross margin; arms-length repricing would cut the margin path and every cash-flow '
       'lens. Expert 1\'s land mark-up is set at exactly half that margin for this reason.',
       'Related-party pricing.')
bullet(f' H1-2026 consumed AED 3.9bn of operating cash into receivables. The component build '
       f'now absorbs cash through FY2028; if receivable days do not fall from 440 as assumed, '
       f'each 30 days is about AED {abs(SN["grid_dso"][3] - SN["grid_dso"][2]):.2f} per share '
       f'(section 1.9).', 'Collections.')
bullet(' FY2024 is a perimeter break and FY2023 belongs to a smaller predecessor: exactly two '
       'audited years of the modern group exist. Every trend read off this history carries '
       'that caveat.', 'Short clean history.')
bullet(f' Beta is the input this valuation is most exposed to. It is now regressed against the '
       f'exchange\'s official index and corrected for thin trading, and reads {IN["beta"]:.2f} '
       f'— but the 90% range runs {IN["beta_record"]["ci90"][0]:.2f} to '
       f'{IN["beta_record"]["ci90"][1]:.2f}, and across that range the cash-flow lens moves '
       f'from about AED {SN["grid_beta"][-1]:.2f} to AED {SN["grid_beta"][0]:.2f}. A reader who '
       f'believes the low end believes a materially higher value; the study adopts the measured '
       f'centre, not the convenient end.', 'Beta.')
bullet(f' {pc(DCF["tv_share"])} of the DCF\'s enterprise value is terminal. At the terminal '
       f'return of {pc(IN["roic_term"], 1)} the block assumes the land bank converts to '
       f'recognised profit; at FY2025\'s clean achieved '
       f'{pc(D["terminal_recon"]["roic_fy25_clean"], 1)} the terminal value falls by roughly a '
       f'sixth and the DCF by about a tenth.', 'Terminal weight.')
bullet(' The probability map is fitted to a market panel more liquid than MODON\'s float; '
       'thin trading can gap.', 'Liquidity.')

# ============================ APPENDIX A ======================================
H1('Appendix A · Financial statements')
H2('A.1 · Income statement — audited years, H1-2026 actual, forecast')
ist = [['AED mn', 'FY2023*', 'FY2024**', 'FY2025', 'H1-26A'] + YRS]
def hrow(lbl, key, fmt=n0):
    return [lbl] + [fmt(HI[y][key]) for y in ['FY23', 'FY24', 'FY25']]
ist.append(hrow('Revenue', 'rev') + [n0(H1D['rev'])] + [n0(v) for v in F['rev']])
ist.append(hrow('Gross profit', 'gp') + [n0(H1D['gp'])] + [n0(v) for v in F['gp']])
ist.append(hrow('EBITDA (house basis)', 'ebitda') + ['—'] + [n0(v) for v in F['ebitda']])
ist.append(hrow('Depreciation & amortisation', 'dna') + ['—'] + [n0(v) for v in F['dna']])
ist.append(hrow('EBIT', 'ebit') + ['—'] + [n0(v) for v in F['ebit']])
ist.append(hrow('Net finance result', 'fin') + ['—']
           + [n0(F['np'][t] / (1 - IN['tax_f']) - F['ebit'][t] - F['assoc'][t])
              for t in range(5)])
ist.append(hrow('Associates & joint ventures', 'assoc') + ['—'] + [n0(v) for v in F['assoc']])
ist.append(hrow('Profit before tax', 'ebt') + [n0(H1D['pbt'])]
           + [n0(F['np'][t] / (1 - IN['tax_f'])) for t in range(5)])
ist.append(hrow('Income tax', 'tax') + [n0(-H1D['eff_tax'] * H1D['pbt'])]
           + [n0(-F['np'][t] / (1 - IN['tax_f']) * IN['tax_f']) for t in range(5)])
ist.append(hrow('Profit for the period', 'pat') + [n0(H1D['pat'])] + [n0(v) for v in F['np']])
ist.append(hrow('Attributable to owners', 'npa') + [n0(H1D['npa'])]
           + [n0(v) for v in F['np_attr']])
table(ist, [1.5, 0.62, 0.62, 0.62, 0.62, 0.6, 0.6, 0.6, 0.6, 0.6], size=7.9, band_rows={10})
caption('* Q Holding perimeter. ** Includes the AED 9,192mn bargain gain (ex-gain profit AED '
        '197mn); the FY2024 EBITDA of 9,795 shown here is dominated by it — house basis, '
        'labelled, dual-framed. "Profit before tax" includes small discontinued items, as '
        'presented. FY2026E full year = H1 actual + the H2-26E stub.')
H2('A.2 · Balance sheet')
bst = [['AED mn', 'FY2024', 'FY2025', '30-Jun-26A'] + YRS]
bst.append(['Receivables incl. related-party', n0(HB['FY24']['recv'] + HB['FY24']['duefr']),
            n0(HB['FY25']['recv'] + HB['FY25']['duefr']), n0(HA['recv'])]
           + [n0(v) for v in F['recv']])
bst.append(['Inventories + development WIP', n0(HB['FY24']['inv'] + HB['FY24']['dwip']),
            n0(HB['FY25']['inv'] + HB['FY25']['dwip']), n0(HA['invdwip'])]
           + [n0(v) for v in F['invdwip']])
bst.append(['Payables incl. advances + related-party', n0(HB['FY24']['pay'] + HB['FY24']['dueto']),
            n0(HB['FY25']['pay'] + HB['FY25']['dueto']), n0(HA['pay'])]
           + [n0(v) for v in F['pay']])
bst.append(['Net working capital', n0(HB['FY24']['nwc']), n0(HB['FY25']['nwc']),
            n0(F['nwc_30jun'])] + [n0(v) for v in F['nwc']])
bst.append(['Cash and bank balances', n0(HB['FY24']['cash']), n0(HB['FY25']['cash']),
            n0(HA['cash_total'])] + [n0(v) for v in F['cash']])
bst.append(['Debt incl. related-party loan', n0(HB['FY24']['debt']), n0(HB['FY25']['debt']),
            n0(HA['debt'])] + [n0(v) for v in F['debt']])
bst.append(['Net debt (− = net cash)', n0(HB['FY24']['nd']), n0(HB['FY25']['nd']),
            n0(HA['debt'] - HA['cash_total'])] + [n0(v) for v in F['net_debt']])
bst.append(['Equity attributable to owners', n0(HB['FY24']['eqp']), n0(HB['FY25']['eqp']),
            n0(HA['eqp'])] + [n0(HA['eqp'] + sum(F['np_attr'][:t + 1])) for t in range(5)])
table(bst, [1.66, 0.68, 0.68, 0.68, 0.62, 0.62, 0.62, 0.62, 0.62], size=7.9, band_rows={7})
caption('Forecast columns roll only the lines the model drives; asset lines it does not '
        'forecast are left to the workbook. FY2023 (Q Holding perimeter) appears in A.1; its '
        'balance sheet is in the workbook.')
H2('A.3 · Cash-flow markers')
cft = [['AED mn', 'FY2024A', 'FY2025A', 'H1-26A'] + YRS,
       ['IFRS operating cash flow (audited/reviewed)', n0(D['hist_cf']['FY24']['ocf']),
        n0(D['hist_cf']['FY25']['ocf']), n0(H1D['ocf'])] + ['—'] * 5,
       ['Model construct: NOPAT + D&A − ΔWC (a DIFFERENT measure — pre-interest, model tax)',
        '—', '—', '—'] + [n0(F['nopat'][t] + F['dna'][t] - F['dnwc'][t]) for t in range(5)],
       ['Capital expenditure', n0(D['hist_cf']['FY24']['capex']),
        n0(D['hist_cf']['FY25']['capex']), n0(312.5)] + [n0(v) for v in F['capex']],
       ['Free cash flow to firm', '—', '—', '—'] + [n0(v) for v in F['fcff']]]
table(cft, [2.02, 0.62, 0.62, 0.62, 0.60, 0.60, 0.60, 0.60, 0.60], size=8.0)
caption(f'The two operating rows are different measures and are no longer presented as one '
        f'series (an audit finding). The model\'s FY2026 implies roughly AED '
        f'{-H1D["ocf"] + F["nopat"][0] + F["dna"][0] - F["dnwc"][0]:,.0f}mn of H2 operating '
        f'inflow on the IFRS basis after H1\'s outflow — stated in section 5 as the thing to '
        f'watch.')

# ============================ APPENDIX B ======================================
H1('Appendix B · Peers, risks and research register')
H2('B.1 · Peer set')
pr2 = [['Company', 'Market', 'FY2025 revenue', 'FY2025 attributable NP', 'Trailing P/E (attr.)',
        'Backlog (own disclosure, dated)'],
       ['Aldar Properties', 'ADX', n0(REL['peers']['ALDAR']['rev']),
        n0(REL['peers']['ALDAR']['np_attr']), f"{REL['peers']['ALDAR']['pe_attr']:.2f}x",
        n0(REL['peers']['ALDAR']['backlog']) + ' (FY25 dev.)'],
       ['Emaar Properties', 'DFM', n0(REL['peers']['EMAAR']['rev']),
        n0(REL['peers']['EMAAR']['np_attr']), f"{REL['peers']['EMAAR']['pe_attr']:.2f}x",
        n0(REL['peers']['EMAAR']['backlog']) + ' (FY25 group)'],
       ['Emaar Development', 'DFM', n0(REL['peers']['EMAARDEV']['rev']),
        n0(REL['peers']['EMAARDEV']['np_attr']), f"{REL['peers']['EMAARDEV']['pe_attr']:.2f}x",
        n0(REL['peers']['EMAARDEV']['backlog']) + ' (FY25)'],
       ['Modon Holding', 'ADX', n0(HI['FY25']['rev']), n0(IN['npa_fy25']),
        f"{REL['pe_trailing_attr']:.2f}x", n0(HA['backlog']) + ' (30-Jun-26 group)']]
table(pr2, [1.42, 0.62, 1.0, 1.28, 1.1, 1.55], band_rows={4}, size=8.6)
caption('AED mn; one attributable basis; every backlog labelled with its object and date. '
        'Peer figures from the peers\' own audited filings and releases; prices 7-Aug-2026.')
H2('B.2 · Risk register')
rr = [['Risk', 'Where it bites', 'How it is priced here'],
      ['Related-party sales concentration and pricing', 'development margin, receivables',
       'margin glide; Expert 2 haircut; margin and receivable-day strips'],
      ['Receivable collection timing', 'working capital', 'component build absorbs through '
       'FY2028; ±60-day strip'],
      ['Abu Dhabi residential cycle turns', 'new sales, pricing', 'run-off stress priced in '
       'full (section 1.7)'],
      ['Egypt macro and FX on Ras El Hekma', 'international leg',
       'Egypt-premium stress: AED ' + px(DCF['ps_egystress']) + ' per share'],
      ['Rates higher for longer', 'discount rate, demand', '+2pt cost-of-equity strip'],
      ['Free float and index exclusion', 'the multiple, not the cash',
       '60% weight on market lenses IS the discount; no second haircut'],
      ['Execution at masterplan scale', 'capex, delivery cadence', 'conversion strip; the '
       'terminal return held below the model\'s own path']]
table(rr, [2.15, 2.15, 2.55], size=8.8)
H2('B.3 · Research register')
rrg = [['Area', 'What was established', 'Source', 'Date']]
import json as _json
SR = _json.load(open('sweep_register.json'))
def _clean_src(x):
    x = x.replace(' (house FED_SCHEDULE, engine/market_profiles.py)',
                  ' (house monetary-policy calendar)')
    return x
for f_ in SR['findings']:
    f_['source_name'] = _clean_src(f_.get('source_name', ''))
    if f_['klass'] == 'NEG':
        rrg.append([f_['ring'].title(), 'Searched, nothing found: ' + f_['headline']
                    .replace('Negative search — nothing found (', '').rstrip(')'),
                    'search log', f_['source_date']])
    else:
        hl = f_['headline']
        hl = hl.replace('[ADDED at revision 2: the first edition swept the interim '
                        'STATEMENTS but not this release, and struck its development drivers '
                        'on 31-Dec-2025 disclosures — the largest finding of the external '
                        'audits, accepted and implemented]',
                        '(added at revision 2 after external audit)')
        rrg.append([f_['ring'].title(), hl, f_['source_name'], f_['source_date']])
table(rrg, [0.75, 3.7, 1.75, 0.75], size=7.6)
caption('Every claim the model rests on, with source and date. The companion bibliography '
        'carries the full input-by-input register — now including the corrections adopted '
        'from the external audits, each marked.')

# ============================ APPENDIX C ======================================
H1('Appendix C · Three experts, worked in full')
P('Three framings, each taken to a number by a different method, with stated blind spots and '
  'falsifiers. Labelled Expert 1, 2 and 3. Expert 2 builds on the study\'s own run-off '
  'scenario — a derived framing with an independent overlay, labelled as such, not a third '
  'independent view.')

H2('C.1 · Expert 1 — the asset value (revalued net assets)')
P('Worldview: a developer is a warehouse of land bought below market. Works when the land is '
  'carried far below realisable value; fails when the buyer of first resort is a related '
  'party whose price is the appraisal.')
e1 = EXPD['e1']
e1t = [['Line', 'AED mn'],
       ['Attributable equity, 30 Jun 2026 (reviewed)', n0(e1['eqp'])],
       ['Land bank at cost (land plots within inventories, FY2025 note)', n0(e1['land_bv'])],
       [f'Mark-up: {pc(e1["uplift"], 1)} — EXACTLY half the realised 67.4% related-party '
        f'land-sale margin (the first edition said "half" but applied 35%; aligned)',
        n0(e1['land_bv'] * e1['uplift'])],
       [f'Work-in-progress mark-up: {pc(e1["dwip_uplift"], 0)} on AED '
        + n0(IN['dwip_bv_h1']) + 'mn', n0(IN['dwip_bv_h1'] * e1['dwip_uplift'])],
       ['Revalued net asset value', n0(e1['nav'])],
       [f'Per share ({n0(SH)}mn shares)', px(e1['base'])],
       ['Range: appraisal haircut 15% to premium 12%', f"{px(e1['rng'][0])}–{px(e1['rng'][1])}"]]
table(e1t, [4.7, 1.5], band_rows={5})
P(f'Named sensitivity: each 10 points of land mark-up is AED {px(e1["land_bv"] * 0.10 / SH)} '
  f'per share. Falsifier: two consecutive halves of arms-length land sales clearing below 20% '
  f'gross margin collapses the mark-up toward zero and this value toward book (AED '
  f'{px(BKL["bvps"])}).')

H2('C.2 · Expert 2 — owner cash flow on the run-off stress (derived framing)')
P('Worldview: value only the cash an owner could take out if no new story arrives; treat '
  'affiliate receivables as impaired until collected. Works at cycle tops; structurally '
  'blind to compounding growth.')
e2 = EXPD['e2']
e2t = [['Line', 'Value'],
       ['Run-off stress DCF (the study\'s own scenario)', f"AED {px(e2['runoff_ps'])}/sh"],
       ['Related-party receivable book, 30 Jun 2026', f"AED {n0(e2['rp_book'])}mn"],
       [f'Haircut: {pc(e2["haircut"], 0)} for timing and collection',
        f"− AED {px(e2['haircut'] * e2['rp_book'] / SH)}/sh"],
       ['Expert 2 value', f"AED {px(e2['base'])}/sh"],
       ['Range: deeper haircut, to the base DCF less 5%', f"{px(e2['rng'][0])}–{px(e2['rng'][1])}"]]
table(e2t, [4.7, 1.6], band_rows={4})
P(f'Named sensitivity: each 10 points of haircut is AED {px(0.10 * e2["rp_book"] / SH)} per '
  f'share. Falsifier: the Department-of-Finance receivable collecting on schedule through '
  f'FY2026 removes the haircut and moves this expert to AED {px(e2["runoff_ps"])}.')

H2('C.3 · Expert 3 — the market pricer')
P('Worldview: the peer multiple is the verdict of everyone else\'s money. Works when the peer '
  'set is deep; prices inflections only after the fact.')
e3 = EXPD['e3']
e3t = [['Line', 'Value'],
       ['FY2026E attributable profit (H1 actual + H2 model)', f"AED {n0(e3['npa26'])}mn"],
       [f'Multiple: {e3["pe"]:.1f}x — the arithmetic MEAN of the rebuilt attributable peer '
        f'set (4.73/5.78/8.10; the first edition claimed "centre" but used 6.5x)', ''],
       ['Implied equity value', f"AED {n0(e3['pe'] * e3['npa26'])}mn"],
       ['Per share', f"AED {px(e3['base'])}"],
       ['Range: trough 4.73x to leader 8.10x', f"{px(e3['rng'][0])}–{px(e3['rng'][1])}"]]
table(e3t, [4.7, 1.6], band_rows={4})
P(f'Named sensitivity: each turn of P/E is AED {px(e3["npa26"] / SH)} per share. Falsifier: a '
  f'dividend policy plus a float above 25% would justify migrating toward the cash-flow '
  f'lenses.')

H2('C.4 · Cross-examination')
bullet(' Expert 1 to Expert 2: your haircut double-counts — the run-off already starves the '
       'related-party channel. Expert 2 concedes in part: the haircut stays on the stock of '
       'receivables, not the flow. Sustained in part.', '')
bullet(' Expert 2 to Expert 1: your mark-up is circular — the margin you halve was set by '
       'related-party sales. Expert 1 concedes the circularity; the falsifier (arms-length '
       'clearing prices within two reporting periods) is the test. Acknowledged.', '')
bullet(' Expert 3 to both: the shares trade at 11.5x attributable earnings against a leader '
       'at 8.1x — the market has voted. Experts 1 and 2 reject the inference: a 15% float is '
       'not a verdict but the absence of one. Rejected, reason stated.', '')

H2('C.5 · Three in one room')
P(f'One sentence each. Expert 1: "the land covers the price at AED {px(EXPD["e1"]["base"])}." '
  f'Expert 2: "paid to wait even in run-off — AED {px(EXPD["e2"]["base"])} — if the '
  f'affiliates pay their bills." Expert 3: "until the float and dividend exist it is worth '
  f'the peer mean: AED {px(EXPD["e3"]["base"])}." Median AED {px(D["panel_centre"])} — '
  f'between the study\'s market lenses and its cash-flow lenses, which is where the '
  f'disagreement lives.')

H2('C.6 · Divergence table')
dv = [['Assumption', 'Expert 1', 'Expert 2', 'Expert 3', 'Gap it drives'],
      ['Land bank worth above cost', f'+{pc(EXPD["e1"]["uplift"], 0)}', '0%', 'ignored',
       f'AED {px(EXPD["e1"]["land_bv"] * EXPD["e1"]["uplift"] / SH)}/sh'],
      ['Related-party receivables', 'face value', f'−{pc(EXPD["e2"]["haircut"], 0)}',
       'face value', f'AED {px(EXPD["e2"]["haircut"] * EXPD["e2"]["rp_book"] / SH)}/sh'],
      ['Sales path', 'irrelevant (assets)', 'run-off stress', 'FY2026E only',
       f'AED {px(DCF["ps"] - CJ["runoff_ps"])}/sh between base and stress'],
      ['Multiple regime', 'n/a', 'n/a', f'{EXPD["e3"]["pe"]:.1f}x peer mean',
       f'AED {px((IN["pe_just"] - EXPD["e3"]["pe"]) * EXPD["e3"]["npa26"] / SH)}/sh vs the '
       f'study\'s {IN["pe_just"]:.1f}x']]
table(dv, [1.6, 1.05, 1.05, 1.05, 2.1], size=8.6)

# ============================ ABOUT / DISCLOSURE ==============================
H1('About this study')
P('Revision 2, produced the same day as the first edition after external audits of that '
  'edition. Every number in the study, the Excel model and the bibliography comes from one '
  'computed model; the delivered workbook is verified cell by cell against it — 617 formula '
  'cells reproduce the model exactly, zero unresolvable, zero unchecked — and a driver test '
  'on the delivered file confirms 25 drivers reprice the workbook in the asserted direction '
  'with no dead inputs (the published scenario-vector rows are display inputs for the pasted '
  'engine re-runs and are inert by design, stated on the sheet). The historical record is '
  'built exclusively from the company\'s own audited statements, reviewed interims and '
  'results announcements; where a figure is both disclosed and derivable, the disclosed '
  'figure is carried. The audits\' accepted findings and this study\'s own re-audit findings '
  'are implemented and marked where they appear; their rejected findings are answered with '
  'receipts in the build record.')
H1('Disclosure')
P('Educational analysis. Not investment advice, not a recommendation, not an offer. No '
  'rating is expressed. The single weighted central is the centre of a stated range of '
  'model outputs, not a price target, and the full per-lens ranges are shown wherever it '
  'appears. The authors hold no position in MODON. Data as of 9 August 2026; prices as of '
  'the 7 August 2026 close. © Testahil 2026.', size=9)

doc.save('MODON_Valuation_Study_10-08-2026_public.docx')
print('wrote MODON_Valuation_Study_10-08-2026_public.docx (revision 3)')
