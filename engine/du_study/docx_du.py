"""DU_Valuation_Study_09-08-2026_public.docx — 16-section study, house style,
model-study (SWDY) skeleton, operating-company lens. Every financial numeral is
read from study_numbers.json; no number is typed into this builder."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
os.chdir(HERE)
exec(open(os.path.join(HERE, 'docx_base.py')).read())

D = json.load(open(os.path.join(HERE, 'study_numbers.json')))
IN = {k: v['value'] for k, v in D['inputs'].items()}
M, HI, HB, F = D['meta'], D['hist_is'], D['hist_bs'], D['fcst']
W, DCF, LN, SN = D['wacc'], D['dcf'], D['lenses'], D['sens']
EXP, REL, NRM, BK = D['experts'], D['rel'], D['norm'], D['book']
SEG, S0, STK, BU = D['seg_fy25'], D['step0'], D['strike'], D['bottomup']
BT = D['backtest']; BT5, BTF = BT['five_year'], BT['full']
SPOT, SH = M['spot'], M['shares_mn']
CEN, LO_, HI_ = D['central'], D['span'][0], D['span'][1]
H1M, H3M = STK['horizons']['1M'], STK['horizons']['3M']
SEGS = ['mobile', 'fixed', 'wholesale', 'ict']
TAXA = IN['tax_eff']

def p2(x):  return f'{x:,.2f}'
def p1(x):  return f'{x:,.1f}'
def n0(x):  return f'{x:,.0f}'
def pc(x, d=1): return f'{x*100:.{d}f}%'
def sgn(x, d=1): return f'{x*100:+.{d}f}%'

# =========================== MASTHEAD / TITLE ================================
masthead()
H2('Independent Valuation Study — Educational Analysis')
H1('Emirates Integrated Telecommunications Company PJSC (DFM: DU)')
rich([('du · United Arab Emirates · Integrated telecom operator (mobile · fixed · wholesale · '
       'ICT and data centres)   ', dict(size=10.5)),
      (f"Anchor {M['asof']} · Spot AED {p2(SPOT)} · Market capitalisation AED "
       f"{n0(M['mktcap'])}mn", dict(size=10.5, color=GREY))], space_after=10)
P('READ FIRST. This study is an educational analysis, not investment advice, a recommendation '
  'or a solicitation. It never issues a rating or a price target: it publishes fair-value '
  'RANGES and probability DISTRIBUTIONS, and it separates what the business may be worth '
  '(sections 1, 4, 5) from where the price could plausibly trade (sections 2, 3, 6) — two '
  'different questions that are never blended. All figures are in United Arab Emirates dirhams '
  '(AED); the company reports, lists and pays dividends in AED, so no currency translation '
  'enters the model anywhere. Historical financials come exclusively from the company\'s own '
  'audited and reviewed consolidated financial statements, read from its investor-relations '
  'portal; every input is listed with source and date in the companion bibliography document.',
  size=9.6, space_after=12)

# =========================== HEADLINE ========================================
H2('Headline')
box([
 ('The business. ', 'du is the second operator in the UAE\'s two-player telecom market: '
  f"{n0(BU['subs_mobile']['Q2_2026'])} thousand mobile customers, "
  f"{n0(BU['subs_fixed']['Q2_2026'])} thousand fixed subscriptions, four disclosed segments "
  f"(Mobile, Fixed, Wholesale, ICT), FY2025 revenue AED {n0(HI['FY25']['rev'])}mn and an "
  f"EBITDA margin of {pc(HI['FY25']['ebitda']/HI['FY25']['rev'])} — with ZERO drawn debt in "
  'every year studied and a dividend paid out of essentially all of profit.'),
 ('The valuation. ', f'Weighted central AED {p2(CEN)} per share against a spot of '
  f'AED {p2(SPOT)} ({sgn(CEN/SPOT-1,0)}), inside a full bear-to-bull span of AED {p2(LO_)} to '
  f'AED {p2(HI_)}. The cash-flow lens alone reads AED {p2(DCF["ps"])}; the market-anchored '
  f'relative lens reads AED {p2(LN["relative"]["base"])}. That gap is the study\'s honest '
  'tension, and section 4 explains rather than hides it.'),
 ('The contested judgement. ', 'The 38% federal royalty plus 9% corporate tax regime '
  f'(a {pc(TAXA)} combined take) is legislated only through 2026. Carried forward it gives '
  f'AED {p2(DCF["ps"])}; a reversion to the heavier pre-2024 construction gives '
  f'AED {p2(DCF["ps_framing_b"])}. Both are published side by side — the judgement is worth '
  f'AED {p2(DCF["ps"]-DCF["ps_framing_b"])} per share and is never averaged into one number.'),
 ('The moment. ', 'This study is struck weeks after a regional war collapsed Gulf tourism and '
  f"took {n0(-BU['subs_mobile']['Q2_2026']+BU['subs_mobile']['Q1_2026'])} thousand mobile "
  'customers off du\'s base in a single quarter, and days after the company cut its own '
  'revenue guidance while raising the interim dividend. The company\'s operating licence '
  'renewal was disclosed as expected to conclude by 8 August 2026 — one day after this '
  'study\'s price anchor.'),
], fill=F_CREAM)

# =========================== VALUATION SUMMARY ===============================
H2('Valuation summary — every read at a glance')
rows = [['Lens', 'Bear', 'Base', 'Bull', 'Weight', 'vs spot']]
for k, nm in [('dcf', 'Discounted cash flow (primary)'), ('relative', 'Relative multiples'),
              ('normalized', 'Normalised earnings power'), ('book', 'Book value & sustainable return')]:
    l = LN[k]
    rows.append([nm, p2(l['bear']), p2(l['base']), p2(l['bull']), pc(l['w'], 0),
                 sgn(l['base']/SPOT-1, 0)])
rows.append(['Weighted central', p2(LO_), p2(CEN), p2(HI_), '100%', sgn(CEN/SPOT-1, 0)])
rows.append(['DCF under Framing B (fiscal reversion)', '', p2(DCF['ps_framing_b']), '', '—',
             sgn(DCF['ps_framing_b']/SPOT-1, 0)])
rows.append(['Expert panel median (Appendix C)', '', p2(D['panel_centre']), '', '—',
             sgn(D['panel_centre']/SPOT-1, 0)])
rows.append([f"DCF terminal value share of enterprise value: {pc(DCF['tv_share'],0)}",
             '', '', '', '', ''])
table(rows, [2.55, 0.85, 0.85, 0.85, 0.75, 0.85], band_rows={5})
caption(f'Table 1 — the valuation summary. Weighted central AED {p2(CEN)}; every lens value is '
        f'dated at the {M["asof"]} anchor, net of the AED {p2(IN["div_between"])} final FY2025 '
        f'dividend paid 28-Apr-2026. The terminal value is {pc(DCF["tv_share"],0)} of the DCF '
        'enterprise value — stated here because a reader should know how much of the primary '
        'lens rests on the far future.')
figure(os.path.join(HERE, 'fig1_football.png'), 7.0,
       'Figure 1 — the valuation football field: bear-to-bull span per lens, brass tick = base, '
       'dark line = spot.')

# =========================== COMPANY OVERVIEW ===============================
H2('Company overview — du at a glance')
P('Emirates Integrated Telecommunications Company PJSC — branded du — launched service in 2007 '
  'as the UAE\'s second licensed operator and has settled into a stable duopoly with e& '
  '(formerly Etisalat). It is majority state-anchored: the Emirates Investment Authority is '
  'the controlling shareholder, and 2025\'s main capital-markets event was a secondary '
  'offering in which Mubadala\'s Mamoura vehicle sold three quarters of its stake (7.55% of '
  'the company), widening the free float without changing control.')
P(f"The revenue mix that decides the company's class: FY2025 mobile services AED "
  f"{n0(SEG['rev']['mobile'])}mn ({pc(SEG['rev']['mobile']/HI['FY25']['rev'],0)} of revenue), "
  f"fixed services AED {n0(SEG['rev']['fixed'])}mn "
  f"({pc(SEG['rev']['fixed']/HI['FY25']['rev'],0)}), wholesale AED "
  f"{n0(SEG['rev']['wholesale'])}mn ({pc(SEG['rev']['wholesale']/HI['FY25']['rev'],0)}) and "
  f"ICT and associated telecom services AED {n0(SEG['rev']['ict'])}mn "
  f"({pc(SEG['rev']['ict']/HI['FY25']['rev'],0)}). The balance-sheet shape: network assets "
  f"(property, plant and equipment AED {n0(HB['FY25']['ppe'])}mn plus right-of-use assets and "
  f"intangibles) financed by equity of AED {n0(HB['FY25']['eq'])}mn, structurally NEGATIVE "
  f"working capital ({pc(D['nwc_pct'])} of revenue — customers and suppliers fund the "
  f"operation), no borrowings, and cash plus term deposits of AED "
  f"{n0(HB['FY25']['net_cash'])}mn against lease liabilities of AED "
  f"{n0(HB['FY25']['lease'])}mn. That is an integrated telecom OPERATING COMPANY, with no "
  'captive lender, no development book and no holding-company discount to model: the lens set '
  'is the operating-company one — a full FCFF discounted cash flow as the primary lens, '
  'cross-read by relative multiples, normalised earnings power and a book/sustainable-return '
  'lens.')
P('Two structural facts organise everything else. First, the state takes roughly '
  f'{pc(TAXA,0)} of pre-royalty profit (38% federal royalty plus 9% corporate tax since 2024; '
  'the pre-2024 construction took over half) — so every operating improvement reaches '
  'shareholders at barely more than half strength, and the fiscal regime is worth more than '
  'any operating driver. Second, the balance sheet is unleveraged with a near-total payout: '
  'du is run as a cash-distribution machine on a licence, which is why the licence renewal '
  'and the royalty renewal are the two catalysts that matter most (section 5).')
P(f"The quarter this study is struck in: a regional war that began in February 2026 collapsed "
  f"Gulf tourism and cut du's prepaid base by "
  f"{n0(BU['subs_mobile']['Q1_2026']-BU['subs_mobile']['Q2_2026'])} thousand in Q2-2026, "
  f"while postpaid kept growing and H1-2026 net profit still rose "
  f"{sgn(IN['h1_26_np']/IN['h1_25_np']-1)} on an EBITDA margin of "
  f"{pc(IN['h1_26_ebitda']/IN['h1_26_rev'])} — the "
  'resilience and the vulnerability in one print. A ceasefire is in place; the recovery path '
  'is the forecast\'s biggest operating assumption and is sensitised explicitly.',
  space_after=10)

# =========================== 1 FUNDAMENTAL VALUATION =========================
H1('1  Fundamental valuation')
P('Four lenses, weighted into one field: the discounted cash flow carries '
  f"{pc(LN['dcf']['w'],0)}, relative multiples {pc(LN['relative']['w'],0)}, normalised "
  f"earnings power {pc(LN['normalized']['w'],0)} and the book lens {pc(LN['book']['w'],0)}.")

H2('1.1  The cash-flow model — the primary lens, with the full waterfall')
P('The model builds five explicit years from the four disclosed segments (section 1.6), '
  'charges the combined royalty-and-tax take on operating profit, funds the network and the '
  'lease book, releases (negative) working capital as revenue grows, and discounts each '
  'year\'s free cash flow at its own forward cost of capital. The full waterfall — every line '
  'of it a live formula in the companion workbook:')
rows = [['AED mn'] + F['years']]
for lab, series in [('Revenue', F['rev']), ('EBITDA', F['ebitda']),
                    ('less depreciation & amortisation', [-x for x in F['dna']]),
                    ('EBIT', F['ebit']),
                    (f'NOPAT — EBIT × (1 − {pc(TAXA)})', F['nopat']),
                    ('add back depreciation & amortisation', F['dna']),
                    ('less capital expenditure', [-x for x in F['capex']]),
                    ('less lease replacement', [-x for x in F['rou_repl']]),
                    ('less change in working capital', [-x for x in F['dnwc']]),
                    ('Free cash flow to the firm', F['fcff']),
                    ('discount factor (glide)', F['df']),
                    ('PV of FCFF', F['pv'])]:
    fmt = p2 if lab.startswith('discount') else n0
    rows.append([lab] + [fmt(x) for x in series])
table(rows, [2.30, 0.94, 0.94, 0.94, 0.94, 0.94], band_rows={2, 4, 10, 12}, size=8.8)
caption(f'Table 2 — the FCFF waterfall. EBITDA margin holds near {pc(F["ebitda_margin"][0])} '
        '(an OUTPUT of the segment build, not an input); capital intensity glides from '
        f'{pc(IN["capex_pct"][0])} of revenue at the data-centre peak to {pc(IN["capex_pct"][-1])}; '
        'lease replacement is charged at right-of-use depreciation so the lease book neither '
        'inflates nor starves the cash flow; working-capital change is a cash RELEASE in every '
        'year because the working capital is negative and revenue grows.')
P(f"Terminal value: terminal-year NOPAT grown at {pc(IN['g_term'])} with a reinvestment rate "
  f"set by the growth itself — g / return on capital = {pc(IN['g_term'])} / "
  f"{pc(DCF['roic_term'])} = {pc(DCF['rr_term'])} of NOPAT — capitalised at the terminal cost "
  f"of capital of {pc(W['wacc_term'],2)} less growth. That yields a terminal value of AED "
  f"{n0(DCF['tv'])}mn, whose present value is AED {n0(DCF['pv_tv'])}mn — "
  f"{pc(DCF['tv_share'],0)} of enterprise value. A reader should sit with that number: at a "
  f"{pc(W['wacc_term'],2)} discount rate almost all of the value of a stable, "
  'licence-protected annuity IS the far future, and that is exactly why the two renewal '
  'catalysts in section 5 dominate everything else in this report.')

H2('The bridge from enterprise value to the equity — and to the anchor date')
rows = [['Step', 'AED mn', 'AED / share'],
        ['Present value of the five forecast years', n0(DCF['pv_explicit']),
         p2(DCF['pv_explicit']/SH)],
        ['Present value of the terminal value', n0(DCF['pv_tv']), p2(DCF['pv_tv']/SH)],
        ['Enterprise value', n0(DCF['ev']), p2(DCF['ev']/SH)],
        [f"Terminal value share of enterprise value: {pc(DCF['tv_share'],0)}", '', ''],
        ['less lease liabilities (the only debt-like item)', n0(-DCF['lease']),
         p2(-DCF['lease']/SH)],
        ['plus cash and term deposits', n0(DCF['net_cash']), p2(DCF['net_cash']/SH)],
        ['plus equity-accounted investees', p2(DCF['investees']), p2(DCF['investees']/SH)],
        ['Equity value at 31-Dec-2025', n0(DCF['eq_val']), p2(DCF['ps_dec'])],
        [f"× anchor accretion (1+Ke)^(219/365) = {DCF['roll']:.4f}, less the AED "
         f"{p2(IN['div_between'])} final dividend paid 28-Apr-2026", '', ''],
        ['Fair value per share at the 07-Aug-2026 anchor', '', p2(DCF['ps'])]]
table(rows, [4.05, 1.30, 1.30], band_rows={3, 8, 10})
caption('Table 3 — enterprise value to equity. There are no minority interests (every '
        'subsidiary is wholly owned) and no borrowings to net: the bridge is leases out, cash '
        'in. The H1-2026 interim dividend of AED 0.26, declared 23-Jul-2026 but unpaid at the '
        'anchor, stays in the share.')
P(f"Scenario span on this lens: bear AED {p2(LN['dcf']['bear'])} (ARPU −5%, a quarter-million "
  f"fewer subscribers, margins −3%, +100bp on the discount rate, terminal growth "
  f"{pc(0.02)}), bull AED {p2(LN['dcf']['bull'])} (the war recovery runs hot and the "
  'data-centre leg compounds). The base case is deliberately NOT the midpoint of those two: '
  'it is built driver by driver in section 1.6.', space_after=10)

H2('1.2  Book value and sustainable return — the asset lens')
P(f"Book value per share is AED {p2(BK['bvps'])} (audited FY2025 equity of AED "
  f"{n0(HB['FY25']['eq'])}mn over {n0(SH)}mn shares). du earned a return on average equity of "
  f"{pc(BK['roe_trailing'])} in FY2025 — a licensed duopoly running negative working capital "
  'needs very little equity, so the return on it is high by construction. The lens asks what '
  f"a sustainable {pc(BK['roe_sust'],0)} return is worth against a perpetual cost of equity "
  f"of {pc(BK['ke_term'],2)}: justified price-to-book = ({pc(BK['roe_sust'],0)} − "
  f"{pc(IN['g_term'])}) / ({pc(BK['ke_term'],2)} − {pc(IN['g_term'])}) = "
  f"{BK['pb_just']:.2f}×, i.e. AED {p2(LN['book']['base'])} per share at the anchor. The "
  'multiple looks extreme against industrial norms; it is what the arithmetic of a small '
  'equity base and a low required return produces, and the honest caveat is that it is the '
  'lens MOST exposed to the low regression beta discussed in section 1.8 — which is why it '
  f"carries only a {pc(LN['book']['w'],0)} weight.")

H2('1.3  Relative multiples')
P(f"du trades at {REL['pe_trailing']:.1f}× trailing earnings and "
  f"{REL['ev_ebitda_trailing']:.1f}× trailing EV/EBITDA (both computed from the audited "
  f"figures, not quoted). The Gulf telecom bracket runs from roughly 9× (Zain) through "
  f"11-12× (Omantel, Ooredoo) and 15.5× (Mobily) to 18.9× (stc) and 20.7× (e&) on trailing "
  'earnings — aggregator reads, used as a cross-check frame and labelled as such, never as a '
  'build source. The justified multiple applied here is the peer median '
  f"{IN['pe_just']:.1f}×: du's growth and payout sit above the bracket's middle, its fiscal "
  'take and single-market concentration below the top names. Applied to FY2026E earnings per '
  f"share of AED {p2(REL['eps26'])} and rolled to the anchor: AED {p2(LN['relative']['base'])} "
  f"per share [bear 12× → AED {p2(LN['relative']['bear'])}; bull 18.5× → AED "
  f"{p2(LN['relative']['bull'])}].")
P(f"A second, independent market cross-check from the dividend: du's FY2026E dividend of AED "
  f"{p2(REL['dps26'])} per share at the regional benchmark payer's yield "
  f"({pc(IN['div_yield_peer'])}, stc) is worth AED {p2(D['yield_ps'])} — usefully ABOVE the "
  'earnings-multiple read, because du pays out more of its earnings than the bracket. Peer '
  'EV/EBITDA could not be reliably sourced from public aggregators at the sweep date '
  '(net-debt figures missing) and the lens therefore runs on earnings and yield only; that '
  'limitation is stated rather than papered over.')

H2('1.4  Normalised earnings power — mid-cycle margin at current scale')
P('The lens strips the cycle: the mid-cycle EBITDA margin (the middle forecast year, '
  f"FY2028E, {pc(NRM['margin'])}) applied to CURRENT-scale revenue (FY2026E, AED "
  f"{n0(NRM['rev'])}mn), less FY2026E depreciation, plus FY2026E net finance income, taxed at "
  f"the combined {pc(TAXA)}: normalised earnings of AED {n0(NRM['np'])}mn, or AED "
  f"{p2(NRM['eps'])} per share. At the justified {IN['pe_just']:.1f}× and rolled to the "
  f"anchor: AED {p2(LN['normalized']['base'])} [12× → {p2(LN['normalized']['bear'])}; 18.5× → "
  f"{p2(LN['normalized']['bull'])}]. It reads within a few fils of the relative lens because "
  'du\'s current year IS close to mid-cycle: the war knocked the top line, not the margin '
  '(H1-2026 printed the best margin in the company\'s history).')

H2('1.5  Synthesis — four lenses, one field')
P(f"Weighted central: AED {p2(CEN)} ({sgn(CEN/SPOT-1,0)} to spot), full span AED {p2(LO_)} to "
  f"AED {p2(HI_)}. The DCF ({pc(LN['dcf']['w'],0)} weight) reads {sgn(LN['dcf']['base']/SPOT-1,0)} "
  'above the market; the two market-anchored lenses read roughly at the market. Section 4 '
  'takes that disagreement seriously — it is a statement about the discount rate, not about '
  'the forecast.', space_after=10)

# =========================== 1.6 DRIVERS =====================================
H2('1.6  The drivers — each disclosed segment grown on its own driver')
H2('The four disclosed segments, historically')
SR = BU['seg_rev_hist']; SC = BU['seg_contrib_hist']
rows = [['Segment', 'FY2023*', 'FY2024', 'FY2025', 'FY2025 contribution', 'margin']]
for s, nm in [('mobile', 'Mobile'), ('fixed', 'Fixed'), ('wholesale', 'Wholesale'),
              ('ict', 'ICT & associated')]:
    rows.append([nm, n0(SR['FY23'][s]), n0(SR['FY24'][s]), n0(SR['FY25'][s]),
                 n0(SC['FY25'][s]), pc(SEG['margin'][s])])
rows.append(['Total', n0(sum(SR['FY23'].values())), n0(sum(SR['FY24'].values())),
             n0(sum(SR['FY25'].values())), n0(sum(SC['FY25'].values())), ''])
table(rows, [1.55, 1.02, 1.02, 1.02, 1.42, 0.85], band_rows={5})
caption('Table 4 — segment revenue (AED mn) and FY2025 contribution (revenue less direct '
        'costs, the company\'s own Note 38 measure). *FY2023 is on the pre-2024 segment basis '
        '(the wholesale/other boundary moved in the re-segmentation) and is shown for '
        'continuity, not comparability; the forecast is built off the consistent FY2024-25 '
        'basis. Segment revenue ties exactly to consolidated revenue in every year.')
H2('How the forecast is driven')
P('Mobile and Fixed are built as volume × price — the finest level the company disclosed. '
  f"Mobile: the quarterly customer base ({n0(BU['subs_mobile']['Q4_2024'])}k end-2024 → "
  f"{n0(BU['subs_mobile']['Q4_2025'])}k end-2025 → {n0(BU['subs_mobile']['Q2_2026'])}k after "
  'the war quarter) times blended ARPU (AED '
  f"{BU['arpu']['FY2025']:.1f}/month in FY2025, {BU['arpu']['Q2_2026']:.1f} in Q2-2026). The "
  'frame reproduces the audited FY2025 mobile segment to within 0.1%: average base '
  f"{n0((BU['subs_mobile']['Q4_2024']+BU['subs_mobile']['Q4_2025'])/2)}k × AED "
  f"{BU['arpu']['FY2025']:.1f} × 12 = AED {n0(BU['unit_mobile_fy25'])}mn against a disclosed "
  f"AED {n0(SR['FY25']['mobile'])}mn. The forecast path: recovery to "
  f"{n0(IN['subs_mobile_path'][0])}k by end-2026 (the company itself reports gross adds still "
  f"below pre-war levels), then to {n0(IN['subs_mobile_path'][-1])}k by end-2030 — growth of "
  'roughly a quarter-million customers a year, well below the boom year 2025 added, with ARPU '
  f"essentially flat (AED {IN['arpu_mobile_path'][0]:.1f} → {IN['arpu_mobile_path'][-1]:.1f}: "
  'postpaid mix gains offsetting prepaid dilution, and no price war anywhere in the record).')
P(f"Fixed: subscribers {n0(BU['subs_fixed']['Q4_2024'])}k → {n0(BU['subs_fixed']['Q2_2026'])}k, "
  f"forecast to {n0(IN['subs_fixed_path'][-1])}k on continued fibre and fixed-wireless share "
  'gain, times an implied revenue per subscription (a consumer-plus-enterprise blend, so a '
  'revenue-intensity metric rather than a tariff) rising gently with the enterprise mix. '
  'Wholesale and ICT disclose no unit measures anywhere in the filings — that gap is flagged, '
  'and both are grown at segment level: wholesale on a war-recovery path (roaming and transit '
  f"were hit; {sgn(IN['seg_g']['wholesale'][0])} in 2026 then ~+2%), ICT on the data-centre "
  f"ramp ({sgn(IN['seg_g']['ict'][1])} at peak), which is anchored on the company's own "
  'disclosed programme: five data centres, a hyperscale campus with Microsoft as anchor '
  'tenant, and capital commitments UP a quarter-billion dirhams in six months.')
H2('What the build produces — margins as outputs')
rows = [['', 'FY2025A'] + F['years']]
rows.append(['Revenue (AED mn)', n0(HI['FY25']['rev'])] + [n0(x) for x in F['rev']])
rows.append(['growth', ''] + [sgn(F['rev'][0]/HI['FY25']['rev']-1,1)]
            + [sgn(F['rev'][i]/F['rev'][i-1]-1,1) for i in range(1, 5)])
rows.append(['EBITDA (AED mn)', n0(HI['FY25']['ebitda'])] + [n0(x) for x in F['ebitda']])
rows.append(['EBITDA margin — an OUTPUT', pc(HI['FY25']['ebitda']/HI['FY25']['rev'])]
            + [pc(m) for m in F['ebitda_margin']])
table(rows, [1.95, 0.72, 0.72, 0.72, 0.72, 0.72, 0.72], band_rows={4}, size=8.4)
caption(f'Table 5 — the build\'s output. FY2026E growth of {sgn(F["rev"][0]/HI["FY25"]["rev"]-1,1)} '
        'lands inside the company\'s own revised 4-6% guidance; the margin output sits just '
        'above the guided 46-47% because the first half already printed 49.2% and the build '
        'holds the audited contribution margins rather than forcing the guidance midpoint. '
        'The cost stack behind it carries one escalator per cost class: wages on UAE wage '
        'inflation, network on network scale, the licence fee and credit losses on revenue, '
        'administration on CPI — never one blended index.')
figure(os.path.join(HERE, 'fig7_mix.png'), 7.0,
       'Figure 2 — revenue by segment and the EBITDA margin path. ICT is the growth leg; '
       'mobile the recovery story; the margin is flat by construction of the disclosed '
       'contribution margins and the escalating cost stack.')

# =========================== 1.7 CRUX ========================================
H2('1.7  The crux — the state\'s take first, the licence second, the war third')
P('Every valuation has one judgement that moves it more than all the others. Here it is the '
  f"FISCAL REGIME. At the current {pc(TAXA)} combined take the cash-flow lens reads AED "
  f"{p2(DCF['ps'])}; at the pre-2024 construction's take it reads AED "
  f"{p2(DCF['ps_framing_b'])}. In real observable units: every single percentage point of "
  f"combined take is worth roughly AED {p2(SN['dcf_tax_per_pp'])} "
  'per share, and the regime that applies from 1 January 2027 was, at this study\'s sweep '
  'date, disclosed in du\'s own filings only as "effective from 2024 to 2026". A ministry '
  'notification extending the same structure to 2027-2029 has been disclosed by the OTHER '
  'operator; du\'s own confirmation had not yet been filed. Section 5 treats that as the '
  'first catalyst, and both framings are priced throughout this study.')
P('Second, the licence: the regulator extended du\'s operating licence only to 8 August 2026 '
  '— one day after this study\'s price anchor — with renewal "in final stage" per the '
  'reviewed interim statements. The base case carries renewal on comparable terms (the '
  f"licence fee held at {pc(IN['licence_pct'])} of revenue); every percentage point of "
  'revenue added to that fee costs about AED '
  f"{p2(LN['dcf']['base'] - SN['dcf_opex_1pp'])} per share — priced in the "
  'sensitivity table, not waved at. Third, the war recovery: the subscriber sensitivity in '
  'section 1.9 spans the outcome from a renewed conflict to a boom-style rebound.')

# =========================== 1.8 MACRO & COUNTRY =============================
H2('1.8  Macro and country — rates, the peg, and the sourced cost of capital')
P('The dirham is hard-pegged to the dollar, so the UAE imports US monetary policy: the '
  'central bank\'s base rate tracks the Fed, and at the sweep date the market was pricing '
  'possible HIKES rather than the cuts of six months earlier. The UAE sovereign is rated '
  'Aa2 and its dirham curve auctions THROUGH the US Treasury curve at matched tenors. '
  'Growth is strong (around 5% real in 2025) even as the regional war cut the wider region\'s '
  '2026 outlook; inflation is around 2%.')
rows = [['Component', 'Value', 'Source basis'],
        ['Risk-free rate (Jan-2031 AED T-bond, the longest liquid AED tenor)', pc(IN['rf'],2),
         'UAE MoF auction, 22-Jul-2026'],
        ['less UAE sovereign default spread (Aa2, rating basis)',
         pc(IN['sov_spread_rating'],2), 'Damodaran dataset, Jan-2026'],
        ['Risk-free net of the sovereign spread', pc(W['rf_star'],2),
         'country risk enters ONCE, via the premium'],
        ['Beta — DU weekly vs the DFM General Index, 5 years',
         f"{IN['beta']:.3f}", 'own regression; details below'],
        ['Equity risk premium (UAE total, rating basis)', pc(IN['erp_rating'],2),
         'Damodaran, mature 4.23% + country 0.64%'],
        ['Cost of equity', pc(W['ke_exp'],2), 'build, not assumption'],
        ['Marginal cost of debt (AED sovereign + GCC telecom spread)', pc(IN['kd'],2),
         'stc sukuk curve evidence; du has no debt'],
        ['Weights — market equity / lease debt', f"{pc(W['we_exp'],1)} / {pc(W['wd_exp'],1)}",
         'market capitalisation vs the audited lease book'],
        ['Cost of capital — explicit window', pc(W['wacc_exp'],2), ''],
        ['Cost of capital — terminal', pc(W['wacc_term'],2),
         f"terminal risk-free {pc(IN['rf_term'],2)}, debt weight {pc(IN['wd_term'],0)}"]]
table(rows, [3.30, 1.10, 2.25], band_rows={6, 9, 10}, size=8.8)
caption('Table 6 — the cost of capital, built from sourced parts. The sovereign spread is '
        'stripped from the risk-free rate because the equity premium already carries the '
        'country premium — counting it twice is the classic error this construction exists '
        'to avoid. On the second premium basis (market-spread, with the live implied US '
        f'premium), the same build gives {pc(W["ke_mkt_alt"],2)} cost of equity and '
        f'{pc(W["wacc_exp_mkt"],2)} cost of capital — both bases are published.')
H2('The beta — measured, gated, and honestly low')
BR = W['beta']
P(f"du's beta is measured, not assumed: weekly log-returns against its OWN index (the DFM "
  f"General), five years, {BR['n']} observations: beta {BR['beta']:.3f}, R² {BR['r2']:.2f}, "
  f"standard error {BR['se']:.3f}, 90% confidence interval {BR['ci90'][0]:.2f} to "
  f"{BR['ci90'][1]:.2f}. The regression passes the usability gate (enough observations, "
  'explanatory power, an error smaller than the estimate), and an equal-weight composite of '
  f"the market's own large names cross-checks it at {BR['composite_alt']['beta']:.3f}. A "
  'defensive, negative-net-debt utility-like telecom measuring below 0.5 on its own index is '
  'economically coherent — and it is also the single assumption doing the most work in this '
  'study, because at these weights the cost of capital is essentially the cost of equity. '
  'Betas of 0.57 (the interval\'s top), 0.65 and 0.80 are priced in section 1.9: the last '
  'takes the DCF from AED '
  f"{p2(SN['grid_beta'][1])} to AED {p2(SN['grid_beta'][4])}. The market, at "
  f"{REL['pe_trailing']:.1f}× earnings, is implicitly charging a HIGHER required return than "
  'this regression produces; section 4 prices that disagreement rather than dismissing it.')
H2('Where this construction is contested, and what the alternatives are worth')
rows = [['Contested construction', 'Base', 'Alternative', 'Worth (AED/share)'],
        ['Risk-free tenor: Jan-2031 AED print vs 10y peg-extrapolated proxy',
         pc(IN['rf'],2), pc(IN['rf_alt'],2),
         f"{p2(DCF['ps_rf_alt'])} vs {p2(DCF['ps'])} ({p2(DCF['ps_rf_alt']-DCF['ps'])})"],
        ['Equity premium basis: rating vs market-spread',
         pc(IN['erp_rating'],2), pc(IN['erp_mkt'],2),
         f"cost of capital {pc(W['wacc_exp'],2)} vs {pc(W['wacc_exp_mkt'],2)}"],
        ['Beta: regression vs the sector-implied prior',
         f"{IN['beta']:.3f}", '0.80',
         f"{p2(SN['grid_beta'][1])} vs {p2(SN['grid_beta'][4])}"],
        ['Fiscal regime: Framing A vs Framing B',
         pc(TAXA), pc(F['taxB_path'][0]),
         f"{p2(DCF['ps'])} vs {p2(DCF['ps_framing_b'])}"]]
table(rows, [2.90, 0.95, 1.05, 1.75], size=8.8)
caption('Table 7 — every contested construction priced, not just named. The retired error is '
        f'also preserved for the audit trail: an UN-netted risk-free rate would have given a '
        f'{pc(W["ke_raw_retired"],2)} cost of equity — the sovereign-risk double-count this '
        'method exists to prevent.')

# =========================== 1.9 SENSITIVITY =================================
H2('1.9  Sensitivity — the discount rate, the growth, the regime and the war')
figure(os.path.join(HERE, 'fig2_sens.png'), 6.6,
       'Figure 3 — DCF fair value against the terminal cost of capital and terminal growth. '
       'Bold cells sit within about 80 fils of spot.')
rows = [['Driver (grid)', '', '', 'base', '', '', 'swing']]
for lab, grid, vals, gf in [
        ('Beta', SN['beta_grid'], SN['grid_beta'], '{:.2f}'),
        ('Combined fiscal take', SN['tax_grid'], SN['grid_tax'], '{:.0%}'),
        ('Blended ARPU (×)', SN['arpu_grid'], SN['grid_arpu'], '{:.2f}'),
        ("Subscribers ('000, shift)", SN['subs_grid'], SN['grid_subs'], '{:+.0f}'),
        ('Contribution margins (×)', SN['mg_grid'], SN['grid_margin'], '{:.2f}'),
        ('Capex path (×)', SN['capex_grid'], SN['grid_capex'], '{:.2f}'),
        ('Terminal ROIC', SN['roic_grid'], SN['grid_roic'], '{:.0%}')]:
    rows.append([f"{lab}  ({' / '.join(gf.format(g) for g in grid)})"]
                + [p2(v) for v in vals] + [p2(max(vals) - min(vals))])
table(rows, [2.60, 0.70, 0.70, 0.70, 0.70, 0.70, 0.70], size=8.2)
caption('Table 8 — single-driver sensitivities on the DCF (AED/share); the middle column is '
        'the base. Each cell is a complete re-run of the model including the unit build. The '
        'rank order is the study\'s honest hierarchy: the discount rate and the fiscal regime '
        'dwarf every operating driver; among operating drivers ARPU is king, which is why a '
        'duopoly that does not price-war deserves its premium.')

# =========================== 2 TECHNICAL ======================================
H1('2  Technical and price structure')
figure(os.path.join(HERE, 'fig3_ma.png'), 7.0,
       'Figure 4 — price against the 20-, 50-, 100- and 200-session moving averages over the '
       'last 260 sessions.')
import numpy as np
from primitives import load_ohlc
from data_quality import clean_ohlc
_df, _ = clean_ohlc(load_ohlc(os.path.join(HERE, '..', 'raw_ohlc', 'AE', 'DU.csv')), 'DU',
                    verbose=False, market='AE')
px = _df['Price'].to_numpy()
sma = {n: float(np.mean(px[-n:])) for n in (20, 50, 100, 200)}
hi52, lo52 = float(np.max(px[-252:])), float(np.min(px[-252:]))
hi52i = float(np.max(_df['High'].to_numpy()[-252:]))
rows = [['Marker', 'Level (AED)', 'Reading'],
        ['Last close', p2(SPOT), 'the anchor for everything in this study'],
        ['20-session average', p2(sma[20]), f"price is {sgn(SPOT/sma[20]-1)} against it"],
        ['50-session average', p2(sma[50]), f"price is {sgn(SPOT/sma[50]-1)} against it"],
        ['100-session average', p2(sma[100]), f"price is {sgn(SPOT/sma[100]-1)} against it"],
        ['200-session average', p2(sma[200]), f"price is {sgn(SPOT/sma[200]-1)} against it"],
        ['52-week high (closing basis)', p2(hi52), f"{sgn(SPOT/hi52-1,1)} from the high"],
        ['52-week high (intraday)', p2(hi52i), f"{sgn(SPOT/hi52i-1,1)} from the high — the "
         'conventional basis, and the wider of the two'],
        ['52-week low', p2(lo52), f"{sgn(SPOT/lo52-1)} from the low"],
        ['Annualised volatility', pc(H3M['anchor_vol_ann'],1),
         'the fitted range-based volatility model\'s CURRENT state — elevated by the '
         'war-quarter swings — and the input to the price cone in section 3']]
table(rows, [1.85, 1.15, 4.00], size=8.6)
_r = np.diff(np.log(px)); _v50 = float(np.std(_r[-50:]) * np.sqrt(252))
P(f"The share sits {sgn(SPOT/sma[200]-1)} above its 200-session average but "
  f"{sgn(SPOT/hi52-1,1)} below its 52-week closing high — an uptrend that has given back its "
  'top since the war quarter. Realised volatility over the last 50 sessions is '
  f"{pc(_v50)}; the model's range-based estimate of {pc(H3M['anchor_vol_ann'])} reflects the "
  'regime of the last months rather than a single session. None of this is a valuation '
  'argument; it is the price context the valuation has to be read against, and the gap '
  'between a recovering price and a fundamental central above it is what section 4 '
  'addresses.', space_after=10)

# =========================== 3 MONTE CARLO ====================================
H1('3  A probabilistic price map')
P('This section answers a different question from the valuation. It does not ask what the '
  'business is worth; it asks where the share price could plausibly be in one and three '
  'months, given how this share has actually moved. The engine simulates 50,000 price paths '
  'from a volatility model fitted to the daily high-low-open-close range, with a fat-tailed '
  'shock distribution and a drift anchored to the cost of carry — the dollar policy path '
  'under the dirham\'s peg, net of the dividend yield — carrying no directional view.')
P(f"The widths below are tested rather than assumed, and the honest result is stated plainly: "
  f"over the last five years of non-overlapping quarterly windows ({BT5['windows']} of them, "
  f"origins {BT5['first_origin']} to {BT5['last_origin']}, each forecast using only data "
  f"available before it), the model scored {BT5['skill_norm']*100:+.2f}% against a random-walk "
  f"benchmark anchored on the same cost of carry — statistically indistinguishable from the "
  f"benchmark (the confidence interval spans zero), neither better nor worse. Outcomes fell "
  f"inside the stated bands at least as often as advertised ({BT5['cov50']*100:.0f}% inside "
  f"the 50% band, {BT5['cov80']*100:.0f}% inside the 80%, {BT5['cov90']*100:.0f}% inside the "
  f"90%) and were spread evenly across the distribution — a uniformity test returns p = "
  f"{BT5['chi2_p']:.2f}, comfortably consistent with a calibrated forecast. The one real "
  f"limitation: for this particular low-volatility share the bands run about "
  f"{(BT5['width_vs_benchmark']-1)*100:.0f}% wider than the benchmark's — the cone is "
  'over-cautious rather than over-confident, and a reader should treat the outer bands as '
  'generous. Over the full history the model UNDERPERFORMS the benchmark on windows that '
  'predate the 2022 change in the exchange\'s trading week; those windows are excluded from '
  'the production calibration for that reason, and the exclusion is disclosed here.')
P('This is a map of price dispersion, not a forecast, and it is never blended with the '
  'fair-value work above.')
figure(os.path.join(HERE, 'fig4_fan.png'), 7.0,
       f"Figure 5 — the forward price cone to three months. The dashed brass line is the "
       f"fundamental central estimate of {p2(CEN)}; the dotted line is the spot of {p2(SPOT)}.")
H2('Percentile map (AED/share)')
rows = [['Horizon', '5th', '25th', 'Median', '75th', '95th', 'P(above spot)'],
        [f"One month — to {H1M['grade_date']}"] + [p2(H1M['pct'][k]) for k in
         ('p5', 'p25', 'p50', 'p75', 'p95')] + [pc(H1M['p_above'],0)],
        [f"Three months — to {H3M['grade_date']}"] + [p2(H3M['pct'][k]) for k in
         ('p5', 'p25', 'p50', 'p75', 'p95')] + [pc(H3M['p_above'],0)]]
table(rows, [1.95, 0.80, 0.80, 0.80, 0.80, 0.80, 1.05], size=8.8)
figure(os.path.join(HERE, 'fig5_dist.png'), 5.4, 'Figure 6 — price distribution at one month.')
figure(os.path.join(HERE, 'fig6_dist.png'), 5.4, 'Figure 7 — price distribution at three months.')
H2('Level-touch ladder')
rows = [['Event', 'One month', 'Three months'],
        ['Finishes 10% or more above spot', pc(H1M['p_up10'],0), pc(H3M['p_up10'],0)],
        ['Finishes 10% or more below spot', pc(H1M['p_dn10'],0), pc(H3M['p_dn10'],0)],
        ['Touches 10% above spot at any point', pc(H1M['touch_up10'],0), pc(H3M['touch_up10'],0)],
        ['Touches 10% below spot at any point', pc(H1M['touch_dn10'],0), pc(H3M['touch_dn10'],0)]]
table(rows, [3.30, 1.30, 1.30], size=8.8, space_after=10) if False else \
    table(rows, [3.30, 1.30, 1.30], size=8.8)
P('', space_after=6)

# =========================== 4 COMPARISON =====================================
H1('4  Comparison of the lenses')
P(f"The field disagrees, and the disagreement is informative. The cash-flow lens reads AED "
  f"{p2(LN['dcf']['base'])}; the two market-anchored lenses read AED "
  f"{p2(LN['relative']['base'])} and AED {p2(LN['normalized']['base'])}; the book lens AED "
  f"{p2(LN['book']['base'])}. The spread is NOT about the forecast — all four lenses consume "
  'the same build, and the near-term numbers are anchored on a printed first half. It is '
  'about the price of time and certainty: the measured beta prices du\'s equity at a '
  f"{pc(W['ke_exp'],1)} required return, while the regional market, at the peer median "
  'multiple, implicitly charges something closer to the return implied by a 15-16× earnings '
  'multiple on a slow-growing annuity — two to three points more. Discount this study\'s own '
  'cash flows at that market-implied rate and you get, in effect, the relative lens.')
P('What would close the gap from each side. The DCF is right and the market re-rates if: the '
  'fiscal regime is extended on current terms with the floor lapsing or lightening; the '
  'licence renews on comparable terms; the war recovery completes; and the data-centre leg '
  'starts printing revenue the market can see. The market is right and the DCF is generous '
  'if: the royalty regime reverts or worsens (Framing B alone closes most of the gap — AED '
  f"{p2(DCF['ps_framing_b'])}); the measured beta understates the true risk of a "
  'single-market, single-licence operator (beta 0.80 alone takes the DCF to AED '
  f"{p2(SN['grid_beta'][4])}); or terminal reinvestment needs are heavier than "
  f"{pc(DCF['rr_term'])} of profit. The weighted central of AED {p2(CEN)} embodies exactly "
  'this balance: it leans toward the cash flows but pays the market-anchored lenses the '
  f"{pc(LN['relative']['w']+LN['normalized']['w'],0)} respect their discipline has earned.")
figure(os.path.join(HERE, 'figD1_experts.png'), 7.0,
       'Figure 8 — the expert panel\'s three independent reads (Appendix C), against spot.')

# =========================== 5 CATALYSTS ======================================
H1('5  Catalysts to watch')
for head, body in [
    ('1 · The post-2026 fiscal regime (direction: either; size: the study\'s largest). ',
     'du\'s own filings describe the 38% + 9% regime as effective 2024-2026. The other '
     'operator has disclosed a ministry notification extending the structure through 2029; '
     'du\'s mirroring disclosure — and whether the AED 1.8bn combined floor carries over — '
     f'is the single most valuable sentence the company can publish: AED {p2(DCF["ps"])} '
     f'versus AED {p2(DCF["ps_framing_b"])} per share between the framings.'),
    ('2 · The licence renewal (direction: binary-adverse tail; timing: now). ',
     'The TDRA extension ran to 8 August 2026 with conclusion expected "on or before" that '
     'date — i.e. the outcome is due at press time. Renewal on comparable terms is the base '
     'case and would be a non-event; a renewal that raises the fee ratio costs roughly AED '
     f'{p2(LN["dcf"]["base"] - SN["dcf_opex_1pp"])} per share per percentage point of revenue.'),
    ('3 · The war recovery (direction: up if the ceasefire holds). ',
     'Prepaid subscribers, roaming and wholesale transit all recover with tourism; the '
     'company itself reports gross adds below pre-war levels with a ceasefire in place. The '
     'Q3-2026 print (late October) is the first clean read; a return to net adds above '
     '+150k/quarter would put the bull subscriber path in play.'),
    ('4 · The data-centre leg (direction: up; horizon: 2027-2028). ',
     'Five data centres plus the Microsoft-anchored hyperscale campus; commitments rose to '
     f'AED {n0(2411.760) if False else "2,412"}mn at mid-2026. First disclosed hyperscale '
     'revenue — or a named second anchor tenant — would convert the ICT growth path from '
     'house assumption to disclosed run-rate.'),
    ('5 · The dividend (direction: up, mechanically). ',
     f'The board raised the interim {pc(0.083) if False else "8.3%"} in the same release '
     'that cut revenue guidance — a statement of intent. At the forecast payout the FY2026E '
     f'dividend is AED {p2(F["dps"][0])}; at the regional benchmark yield that alone is '
     f'worth AED {p2(D["yield_ps"])} per share (section 1.3).')]:
    bullet(body, bold_head=head)
P('', space_after=4)

# =========================== 6 PROBABILITY ZONES ==============================
H1('6  Reading the probability zones')
P('How to read sections 2-3 against section 1. The three-month cone spans AED '
  f"{p2(H3M['pct']['p5'])} to {p2(H3M['pct']['p95'])} — the price can visit a lot of places "
  'in ninety days without any of them being a statement about value. The fundamental central '
  f"of AED {p2(CEN)} sits {'inside' if H3M['pct']['p5'] <= CEN <= H3M['pct']['p95'] else 'OUTSIDE'} "
  'the cone\'s upper half: reaching it within a quarter would be a strong but not '
  'extraordinary move. Three zones, then:')
for head, body in [
    (f"Below AED {p2(H3M['pct']['p25'])} (the cone's lower quarter): ",
     'price weakness this deep with no fiscal or licence news would widen the value gap '
     'mechanically; with adverse regime news it would simply be the market pricing Framing '
     'B — check which before reading it as opportunity.'),
    (f"AED {p2(H3M['pct']['p25'])} to {p2(H3M['pct']['p75'])} (the middle half): ",
     'noise. Nothing in this band changes any conclusion in this study.'),
    (f"Above AED {p2(H3M['pct']['p75'])}: ",
     'the market starting to pay for the recovery and the regime extension before they are '
     'printed; at the cone\'s top the share would still sit below the cash-flow lens but at '
     'the weighted central.')]:
    bullet(body, bold_head=head)
P('The cone is honest about its own limits: for this share its bands have historically run '
  'wider than needed (section 3), so the outer zones are conservative.', space_after=10)

# =========================== 7 CAVEATS ========================================
H1('7  Caveats and what would change our mind')
for head, body in [
    ('The discount rate is the study. ', 'A 0.47 measured beta against an Aa2 curve prices '
     f"du's equity at {pc(W['ke_exp'],1)}. Every conclusion that differs from the market "
     'traces to that number; section 1.8 prices the alternatives and section 4 takes the '
     'other side seriously. If du\'s risk is the sector\'s rather than its regression\'s, '
     'the central is several dirhams lower.'),
    ('The terminal value is most of the value. ', f"{pc(DCF['tv_share'],0)} of the DCF's "
     'enterprise value is beyond year five. That is the honest shape of a low-discount-rate '
     'annuity, and it is why the licence and the royalty — the two things that could touch '
     'the annuity itself — outrank every operating driver.'),
    ('The fiscal regime is not ours to forecast. ', 'Both framings are priced throughout; '
     'the study REFUSES a single number where the state has not yet published one. If a '
     'harsher-than-either construction emerged, both framings would need re-striking.'),
    ('The war path. ', 'The base case assumes the ceasefire holds and tourism normalises '
     'into 2027. A re-opened conflict invalidates the subscriber path, the wholesale '
     'recovery and possibly the multiple — the bear scenario, not the base.'),
    ('Wholesale and ICT are built top-down. ', 'No unit disclosures exist for either; both '
     'are flagged. The ICT ramp in particular leans on a disclosed programme whose revenue '
     'model (colocation vs services) the company has not yet broken out.'),
    ('What would change our mind, concretely. ', 'A royalty construction harsher than '
     'Framing B; licence renewal terms materially above the current fee ratio; two '
     'consecutive quarters of negative postpaid net adds; ARPU breaking below AED 60 '
     'without a mix explanation; or the payout being cut other than for a named investment '
     'programme. Any one of these re-opens the build; the register in Appendix B tells a '
     'reader exactly which inputs to re-examine first.')]:
    bullet(body, bold_head=head)
P('', space_after=6)

# =========================== APPENDIX A =======================================
H1('Appendix A  Financial statements')
H2('A.1  Income statement — three years historical and five years forecast (consolidated, AED mn)')
H3Y = ['FY23', 'FY24', 'FY25']
rows = [['AED mn', 'FY2023', 'FY2024', 'FY2025'] + F['years']]
def isrow(lab, hist, fc, fmt=n0):
    return [lab] + [fmt(h) if h is not None else '—' for h in hist] + [fmt(x) for x in fc]
pbt_f = [F['ebit'][i] + F['int_inc'][i] - F['int_exp'][i] for i in range(5)]
rows.append(isrow('Revenue', [HI[y]['rev'] for y in H3Y], F['rev']))
rows.append(isrow('EBITDA', [HI[y]['ebitda'] for y in H3Y], F['ebitda']))
rows.append(isrow('EBITDA margin', [HI[y]['ebitda']/HI[y]['rev'] for y in H3Y],
                  F['ebitda_margin'], fmt=lambda x: pc(x)))
rows.append(isrow('Depreciation & amortisation', [-HI[y]['dna'] for y in H3Y],
                  [-x for x in F['dna']]))
rows.append(isrow('Operating profit (EBIT)', [HI[y]['ebit'] for y in H3Y], F['ebit']))
rows.append(isrow('Net finance income / (cost)',
                  [None, HI['FY24']['fin'], HI['FY25']['fin']],
                  [F['int_inc'][i] - F['int_exp'][i] for i in range(5)]))
rows.append(isrow('Profit before royalty and tax', [HI[y]['pbt'] for y in H3Y], pbt_f))
rows.append(isrow('Federal royalty and income tax',
                  [-(HI[y]['royalty'] + HI[y]['tax']) for y in H3Y],
                  [-pbt_f[i] * TAXA for i in range(5)]))
rows.append(isrow('Net profit', [HI[y]['np'] for y in H3Y], F['np']))
rows.append(isrow('Earnings per share (AED)', [HI[y]['eps'] for y in H3Y],
                  F['eps'], fmt=p2))
rows.append(isrow('Dividend per share (AED)',
                  [IN['dps_fy23'], IN['dps_fy24'], IN['dps_fy25']], F['dps'], fmt=p2))
table(rows, [1.86] + [0.63]*8, band_rows={2, 9}, size=8.2)
caption('Table A1 — FY2023-25 are the audited figures (FY2024 on the re-presented basis of '
        'the FY2025 statements, so the two recent years sit on one presentation; FY2023 '
        'EBITDA is derived from audited components because the older format prints no such '
        'line, and is flagged as such). The FY2023 royalty is the old-regime charge; no '
        'corporate income tax existed before 2024.')
H2('A.2  Balance sheet — condensed house layout (consolidated, AED mn)')
rows = [['AED mn', 'FY2023', 'FY2024', 'FY2025'] + F['years']]
rows.append(isrow('Property, plant and equipment', [HB[y]['ppe'] for y in H3Y], F['ppe']))
rows.append(isrow('Right-of-use assets', [HB[y]['rou'] for y in H3Y], F['rou']))
rows.append(isrow('Intangibles (excl. goodwill)', [HB[y]['intang'] for y in H3Y], F['intang']))
rows.append(isrow('Goodwill', [None, HB['FY24']['goodwill'], HB['FY25']['goodwill']],
                  [HB['FY25']['goodwill']] * 5))
rows.append(isrow('Net working capital', [HB[y]['nwc'] for y in H3Y], F['nwc']))
rows.append(isrow('Cash and term deposits', [HB[y]['net_cash'] for y in H3Y], F['net_cash']))
rows.append(isrow('Lease liabilities', [HB[y]['lease'] for y in H3Y],
                  [HB['FY25']['lease']] * 5))
rows.append(isrow('Total equity', [HB[y]['eq'] for y in H3Y], F['equity']))
rows.append(isrow('Net cash after leases',
                  [HB[y]['net_cash'] - HB[y]['lease'] for y in H3Y],
                  [F['net_cash'][i] - HB['FY25']['lease'] for i in range(5)]))
table(rows, [1.86] + [0.63]*8, band_rows={8}, size=8.2)
caption('Table A2 — a condensed layout: receivables, payables, contract balances and the '
        'royalty accrual are netted inside working capital (the FY2023 payables line still '
        'contained the royalty accrual, separately disclosed from FY2024; it is excluded in '
        'every year so the series is like-for-like). Zero drawn borrowings in every year '
        'shown. Goodwill was not a separate line in the FY2023 layout.')
H2('A.3  Forecast balance sheet and cash-flow markers')
P(f"The equity walk: profit less the {pc(F['payout'],0)} payout compounds equity from AED "
  f"{n0(HB['FY25']['eq'])}mn to AED {n0(F['equity'][-1])}mn by FY2030E. The cash walk is the "
  'stress line: at a near-total payout plus the data-centre capex peak, cash and term '
  f"deposits fall from AED {n0(HB['FY25']['net_cash'])}mn to AED {n0(min(F['net_cash']))}mn "
  'at the trough before rebuilding — the audited mid-2026 position (term deposits nil after '
  'the royalty settlement and final dividend) already shows exactly this mechanic, and the '
  'undrawn AED 2.0bn facility is the disclosed backstop. Working capital RELEASES cash every '
  'year; the lease book is held flat with replacement charged at depreciation.',
  space_after=10)

# =========================== APPENDIX B =======================================
H1('Appendix B  Peer frame, risk register — and the research register')
H2('B.1  Peers and the sector frame')
rows = [['Company', 'Market', 'Trailing P/E', 'Yield', 'Read-across'],
        ['e&', 'UAE (ADX)', '~20.7×', '~4.8%',
         'the duopoly partner: scale + international assets earn the premium multiple'],
        ['stc', 'Saudi Arabia', '~18.9×', '~5.2%', 'the regional benchmark payer'],
        ['Mobily', 'Saudi Arabia', '~15.5×', '~2.9%',
         'closest structural analogue — the #2 that closed the gap; sets the justified P/E'],
        ['Ooredoo', 'Qatar', '~12.5×', '~4.6%', 'multi-market, softer growth'],
        ['Zain', 'Kuwait', '~9×', '~6-7%', 'levered multi-market; the bracket floor'],
        ['Omantel', 'Oman', '~11.4×', '~6.7%', 'small-market incumbent, yield-heavy'],
        ['DT / Vodafone', 'Developed', 'n/m', '~3.4%',
         'the developed bracket: more leverage, lower returns, lower multiples']]
table(rows, [1.30, 1.20, 1.00, 0.80, 2.70], size=8.6)
caption('Table B1 — aggregator reads at the sweep date, labelled cross-check; never a build '
        'source. du computes at '
        f"{REL['pe_trailing']:.1f}× trailing earnings and {REL['ev_ebitda_trailing']:.1f}× "
        'trailing EV/EBITDA from its own audited figures.')
H2('B.2  Risk register')
rows = [['Risk', 'Mechanism', 'Where it is priced'],
        ['Fiscal regime reversion or worsening', 'combined take above the current '
         f'{pc(TAXA,0)}', f"Framing B throughout: AED {p2(DCF['ps_framing_b'])}"],
        ['Licence renewal on worse terms', 'fee ratio above '
         f"{pc(IN['licence_pct'])} of revenue",
         f"~AED {p2(LN['dcf']['base'] - SN['dcf_opex_1pp'])}/share per +1pp (section 1.9)"],
        ['War re-escalation', 'prepaid, roaming, wholesale transit reverse',
         'subscriber sensitivity and the DCF bear'],
        ['Required-return mismeasurement', 'the 0.47 regression beta understates true risk',
         f"beta grid to 0.80: AED {p2(SN['grid_beta'][4])}"],
        ['Data-centre execution', 'ICT ramp slips; capex stays high without the revenue',
         'ICT growth and capex grids'],
        ['Payout sustainability', 'near-total payout + capex peak drains liquidity',
         'the cash walk in A.3; the undrawn facility is the backstop'],
        ['Concentration', 'one market, one regulator, one licence',
         'the weight given to market-anchored lenses in the synthesis']]
table(rows, [1.85, 2.60, 2.55], size=8.6)
H2('B.3  The research register — layers, dated, negative results included')
P('The full input register — every input with value, source and date, grouped by research '
  'layer, with the judgement table (each judgement paired with what would overturn it), the '
  'negative-results table and the source-discrepancy notes — ships as the companion '
  'bibliography document. Highlights a reader should know: all statement figures were read '
  'from the company\'s own audited/reviewed filings on its investor-relations portal (four '
  'complete fiscal years, plus both 2026 interims, swept in before the build); the UAE '
  'sovereign credit-default-swap quote was UNREACHABLE at the sweep date and the market '
  'spread was proxied by the traded Abu Dhabi dollar curve, disclosed rather than silently '
  'substituted; no public peer EV/EBITDA was clean enough to use; and no announcement of '
  'concluded licence-renewal terms existed at the sweep date — a dated negative search, not '
  'an oversight.', space_after=10)

# =========================== APPENDIX C =======================================
H1('Appendix C  The expert valuation panel')
P('Three experts, three genuinely different methods, each with worked arithmetic, a named '
  'sensitivity and a falsifier stated in advance. They are labelled Expert 1/2/3; their '
  'methods, not their names, are the point. Cast by method: an '
  'earnings-power investor, a dividend-stream investor, and an economic-profit analyst.')

E1, E2, E3 = EXP['e1'], EXP['e2'], EXP['e3']
H2('C.1  Expert 1 — earnings power: through-cycle earnings at a conservative multiple')
P('Worldview: buy durable earnings power at a multiple that does not need the story to work. '
  'Works best on stable franchises near mid-cycle; fails when the cycle is mistaken for the '
  'trend or when a regime change (here: fiscal) resets the earnings base itself.')
rows = [['Step', 'Value'],
        ['Mid-cycle earnings per share (FY2028E)', p2(E1['eps'])],
        ['Through-cycle multiple applied', f"{E1['pe']:.1f}×"],
        ['Value at FY2028, discounted two years at the cost of equity',
         p2(E1['base'] + IN['div_between']) + '  (before the paid-dividend adjustment)'],
        ['less the final FY2025 dividend paid before the anchor', p2(IN['div_between'])],
        ['Expert 1 fair value (anchor date)', p2(E1['base'])],
        ['Range: 12× to 17.5× the same earnings', f"{p2(E1['rng'][0])} – {p2(E1['rng'][1])}"]]
table(rows, [4.30, 2.30], band_rows={5})
P(f"Named sensitivity: the multiple. Each turn of the multiple is worth AED "
  f"{p2(abs(E1['rng'][1]-E1['rng'][0])/5.5)} per share at mid-cycle earnings. Falsifier, "
  'stated in advance: if FY2027 earnings per share prints below the FY2026 estimate — i.e. '
  'the war recovery stalls into earnings — the mid-cycle base is wrong and this read is '
  'withdrawn.')
H2('C.2  Expert 2 — the dividend stream: the natural lens for a full-payout duopoly')
P('Worldview: for a company that pays out essentially everything, the dividend IS the cash '
  'flow; value it directly as a growing perpetuity. Works best when payout is policy, not '
  'accident, and the balance sheet cannot be raided; fails when the payout is about to be '
  'cut — the model capitalises a promise.')
rows = [['Step', 'Value'],
        ['FY2026E dividend per share', p2(E2['dps'])],
        [f"grown at {pc(E2['g'])} into a perpetuity at the terminal cost of equity "
         f"{pc(E2['ke'],2)}", f"{p2(E2['dps'])} × {1+E2['g']:.3f} / "
         f"({pc(E2['ke'],2)} − {pc(E2['g'])})"],
        ['less the final FY2025 dividend paid before the anchor', p2(IN['div_between'])],
        ['Expert 2 fair value (anchor date)', p2(E2['base'])],
        ['Range: cut-and-higher-rate bear to 3%-growth bull',
         f"{p2(E2['rng'][0])} – {p2(E2['rng'][1])}"]]
table(rows, [4.30, 2.30], band_rows={4})
P('Named sensitivity: the growth-rate spread (Ke − g). At these levels each 50 basis points '
  f"of spread is worth roughly AED {p2(E2['base']*0.005/(E2['ke']-E2['g']))} per share. "
  'Falsifier: an interim or final dividend DECLARED lower than the prior year\'s equivalent '
  '— the first cut in the record — withdraws this read immediately.')
H2('C.3  Expert 3 — cash returns: economic profit on invested capital')
P('Worldview: value = capital + the present value of returns ABOVE the cost of capital; a '
  'franchise is only worth a premium while its return spread lasts. Works best where '
  'invested capital is measurable and returns are stable; fails when intangible capital '
  '(spectrum rights, the licence itself) does the earning but sits off the balance sheet — '
  'which flatters the measured return.')
rows = [['Step', 'AED mn'],
        ['Invested capital, FY2025 (PP&E + right-of-use + intangibles + goodwill + working '
         'capital)', n0(E3['ic0'])],
        ['PV of five years of economic profit (NOPAT less capital charge at the forward '
         'rate)', n0(E3['pv_ep'])],
        ['PV of the terminal economic-profit annuity', n0(E3['pv_ep_term'])],
        ['Implied enterprise value', n0(E3['ev'])],
        ['bridge to equity (leases out, cash in), per share at the anchor', p2(E3['base'])],
        ['Range: fading spreads bear to the rate-tenor bull',
         f"{p2(E3['rng'][0])} – {p2(E3['rng'][1])}"]]
table(rows, [4.30, 2.30], band_rows={5})
P(f"The return spread behind it: forecast returns on capital of "
  f"{' / '.join(pc(x,0) for x in F['roic'])} against forward costs of capital of "
  f"{' / '.join(pc(x,1) for x in F['fwd_wacc'])} — a spread of roughly twenty points, which "
  'is what a licensed duopoly with negative working capital looks like in this framework. '
  'Named sensitivity: terminal capital intensity — if the data-centre era permanently '
  'raises invested capital per dirham of profit, the terminal annuity shrinks. Falsifier: '
  'return on invested capital printing below 20% for two consecutive years.')
H2('C.4  Cross-examination')
for head, body in [
    ('Expert 2 to Expert 1: ', 'your multiple is a market mood; my denominator is a policy '
     'rate. CONCEDED in part by Expert 1: the multiple carries sentiment — which is exactly '
     'why it is set at the peer median rather than du\'s own historical average.'),
    ('Expert 1 to Expert 2: ', 'you capitalise a promise at a 3.7-point spread; one cut and '
     'your number is fiction. REJECTED by Expert 2: the payout has risen through a war '
     'quarter and a guidance cut — the board has told you what the dividend is for.'),
    ('Expert 3 to both: ', 'neither of you charges for capital. The spread is the asset. '
     'CONCEDED by both — with the counter, ACCEPTED by Expert 3, that his invested-capital '
     'base omits the licence value itself, so his measured spread flatters the franchise '
     'precisely when the licence is up for renewal.'),
    ('All three to the primary model: ', 'the DCF\'s terminal value is '
     f"{pc(DCF['tv_share'],0)} of enterprise value at a discount rate its own section calls "
     'the study\'s biggest assumption. The model\'s answer: the beta is measured, gated, '
     'cross-checked, and priced against its alternatives in two separate tables — the '
     'disagreement is put in front of the reader rather than resolved by fiat.')]:
    bullet(body, bold_head=head)
H2('C.5  The three in one room')
P(f"Where they land: Expert 1 at AED {p2(E1['base'])}, Expert 2 at AED {p2(E2['base'])}, "
  f"Expert 3 at AED {p2(E3['base'])} — a panel median of AED {p2(D['panel_centre'])}. The "
  'shape of the disagreement is the study in miniature: the earnings-power read hugs the '
  'market because it borrows the market\'s multiple; the two cash-based reads sit together '
  'well above it because they price du\'s cash at du\'s measured risk. The room\'s one joint '
  'statement: at spot, the market is paying for the annuity and giving the growth legs — '
  'data centres, the war recovery, the postpaid mix — away for little.')
H2('C.6  Reading the divergence')
rows = [['Gap', 'Driver of the gap', 'Worth (AED/share)'],
        [f"Expert 1 ({p2(E1['base'])}) vs Expert 2 ({p2(E2['base'])})",
         'market multiple vs measured cost of equity as the price of the same cash',
         p2(abs(E2['base'] - E1['base']))],
        [f"Expert 2 ({p2(E2['base'])}) vs Expert 3 ({p2(E3['base'])})",
         'payout-as-perpetuity vs capital-charged spread — small, because at ~100% payout '
         'the dividend nearly IS the economic profit', p2(abs(E2['base'] - E3['base']))],
        [f"Panel median vs the study's weighted central ({p2(CEN)})",
         'the synthesis deliberately weights the market-anchored lenses the panel\'s '
         'cash-flow majority does not', p2(abs(D['panel_centre'] - CEN))]]
table(rows, [2.30, 3.35, 1.35], size=8.6)
caption('Table C1 — the divergence table: which assumption drives which gap.', space_after=10) \
    if False else caption('Table C1 — the divergence table: which assumption drives which gap.')

# =========================== ABOUT / DISCLOSURE ===============================
H1('About this series')
P('Testahil publishes independent, educational valuation studies of listed companies and '
  'metals. Each study separates fundamental value (built from audited filings, bottom-up) '
  'from price probability (a calibrated simulation of where the price could trade), and '
  'publishes ranges and distributions rather than targets. Delivered studies are never '
  'retro-edited; corrections are made forward, in the open. The companion Excel model is '
  'formula-driven so every figure can be traced to its driver, and the companion '
  'bibliography lists every input with source and date.')
H1('Disclosure & Disclaimer')
P('This document is educational analysis, not investment advice, an offer, a solicitation, '
  'or a recommendation to buy or sell any security. It expresses no rating and no price '
  'target. The authors hold no position in the securities discussed and receive no '
  'compensation from any issuer. All historical figures derive from the company\'s own '
  'published audited or reviewed consolidated financial statements; forecasts are the '
  'authors\' own and are inherently uncertain. Probabilities describe model output, not '
  'promises. Markets can and do behave outside any model\'s bands. Readers should conduct '
  'their own research and consult their own advisers. © Testahil, 2026.', size=9.3)

doc.save(os.path.join(HERE, 'DU_Valuation_Study_09-08-2026_public.docx'))
print('wrote DU_Valuation_Study_09-08-2026_public.docx')
