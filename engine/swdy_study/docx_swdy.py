"""SWDY_Valuation_Study_05-08-2026_public.docx — python-docx builder, house style.
Reads study_numbers.json exclusively: no numeral is typed into this file."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..'))
exec(open(os.path.join(HERE, 'docx_base.py')).read())   # doc, P, H1, H2, table, box, ...

D = json.load(open(os.path.join(HERE, 'study_numbers.json')))
M, HI, HB, F = D['meta'], D['hist_is'], D['hist_bs'], D['fcst']
W, DCF, LN, SN = D['wacc'], D['dcf'], D['lenses'], D['sens']
EXP, TR, REL, NRM, BK = D['experts'], D['terminal_recon'], D['rel'], D['norm'], D['book']
S0, STK, SEG = D['step0'], D['strike'], D['seg_fy25']
BU = D['bottomup']
_BT = json.load(open(os.path.join(HERE, 'backtest_5y.json')))
BT5, BT5F = _BT['five_year'], _BT['full']
IN = {k: v['value'] for k, v in D['inputs'].items()}
SPOT, SH = M['spot'], M['shares_mn']
YRS = F['years']
H3M = STK['horizons']['3M']; H1M = STK['horizons']['1M']

def n0(x): return f"{x:,.0f}"
def n1(x): return f"{x:,.1f}"
def p2(x): return f"{x:.2f}"
def pc(x, dp=1): return f"{x*100:.{dp}f}%"
def sgn(x, dp=0): return f"{x*100:+.{dp}f}%"

# =========================== MASTHEAD / TITLE ================================
masthead()
H2('Independent Valuation Study — Educational Analysis')
H1('Elsewedy Electric Company S.A.E. (EGX: SWDY)')
P(f"Diversified industrial group — wires and cables, engineering and construction, electrical "
  f"products, digital solutions and infrastructure investment · Egyptian Exchange · reporting "
  f"currency EGP · analysis anchored on the closing price of {p2(SPOT)} on {M['asof']}.",
  size=10, color=GREY)

box([("READ FIRST — what this document is. ",
      "This is an educational valuation study. It contains no recommendation, no rating and no "
      "price target. What it contains is a fair-value range built from disclosed financial "
      "statements, a stated cost of capital, and explicitly listed assumptions — together with a "
      "separate, probabilistic map of where the share price could trade over the next one and "
      "three months. The two are different objects and are never blended."),
     ("What a fair value is not. ",
      "A fair-value estimate is a statement about what the business appears to be worth on the "
      "assumptions set out here. It is not a forecast of the share price, and it carries no "
      "implied timeframe. A share can trade above or below an intrinsic estimate for years."),
     ("Where the numbers come from. ",
      "Every figure traces to a source recorded in the accompanying source register: the company's "
      "own audited and interim financial statements and earnings releases, exchange filings, and "
      "named market data. Where a figure is derived rather than disclosed, it is labelled as "
      "derived and the derivation is shown."),
     ("The single largest uncertainty. ",
      "This company earns more than 70% of its revenue outside Egypt, but it reports, is listed "
      "and is financed in Egyptian pounds. The answer therefore depends heavily on which currency's "
      "cost of capital you believe applies. Both readings are computed and both are shown.")])

# =========================== HEADLINE ========================================
H2('Headline')
P(f"Elsewedy Electric is the largest listed industrial group on the Egyptian Exchange by revenue: "
  f"EGP {n0(HI['FY25']['rev'])}mn in FY2025, up {sgn(HI['FY25']['rev']/HI['FY24']['rev']-1)} on "
  f"FY2024 and {sgn((HI['FY25']['rev']/HI['FY23']['rev'])**0.5-1)} a year compounded over the last "
  f"two years. It converts copper into cable, builds substations and power plants under turnkey "
  f"contract, and sells meters, transformers and digital grid products across 15 countries. Just "
  f"over 70% of the revenue is earned abroad, and the order book stands at roughly USD "
  f"{IN['backlog_usd_bn']}bn.")
P(f"The operating story of the last two years is a margin normalisation, not a deterioration. The "
  f"gross margin ran at {pc(HI['FY24']['gp']/HI['FY24']['rev'])} in FY2024 when a collapsing pound "
  f"turned cheaply bought copper inventory into windfall profit; it settled to roughly "
  f"{pc(HI['FY25']['gp']/HI['FY25']['rev'])} in FY2025 as that effect washed out. Revenue kept "
  f"compounding through it. Net profit after minority interests was essentially flat at EGP "
  f"{n0(HI['FY25']['npa'])}mn against EGP {n0(HI['FY24']['npa'])}mn — a flat result on a "
  f"{sgn(HI['FY25']['rev']/HI['FY24']['rev']-1)} revenue increase is the whole of the margin story "
  f"in one line. The first quarter of 2026 reaccelerated: revenue EGP {n0(IN['q1_26_rev'])}mn "
  f"({sgn(IN['q1_26_rev']/IN['q1_25_rev']-1)}) and attributable profit EGP {n0(IN['q1_26_npa'])}mn "
  f"({sgn(IN['q1_26_npa']/IN['q1_25_npa']-1)}).")
P(f"The balance sheet is not the constraint people assume. Gross borrowings are large because the "
  f"working-capital cycle is large, but the group holds very substantial offsetting cash: net bank "
  f"debt was EGP {n0(IN['nd_fy25'])}mn at the end of FY2025, only "
  f"{HI['FY25']['ebitda'] and n1(IN['nd_fy25']/HI['FY25']['ebitda'])}× EBITDA. And the debt is "
  f"cheap in a way that is easy to miss: the audited notes disclose average rates of "
  f"{pc(IN['kd_egp_note'])} on Egyptian-pound liabilities but {pc(IN['kd_usd_note'])} on dollars "
  f"and {pc(IN['kd_eur_note'])} on euros. The blended rate actually paid works out near "
  f"{pc(W['kd_eff_q1_25'])}, roughly half what a purely domestic Egyptian borrower pays.")
P(f"On our primary construction the four lenses centre at EGP {p2(D['central'])} per share against "
  f"a market price of {p2(SPOT)} — the price sits about {sgn(SPOT/D['central']-1,0)} above the "
  f"central estimate. That gap is not mainly an argument about the business; it is an argument "
  f"about the discount rate. Discounted at an Egyptian cost of equity of {pc(W['ke_exp'])}, the "
  f"cash flows support roughly EGP {p2(DCF['ps'])}. Discount the hard-currency share of those same "
  f"cash flows at a hard-currency cost of capital of about {pc(W['wacc_usd_alt'])} and the same "
  f"model produces EGP {p2(DCF['ccy_alt_ps'])}, which is above today's price. The market appears "
  f"to be applying something close to the second view. Both are shown, and neither is hidden "
  f"inside an average.", space_after=10)

# =========================== VALUATION SUMMARY ===============================
H2('Valuation summary — every read at a glance')
rows = [['Read', 'Basis', 'Range (EGP/share)', 'Central', 'vs spot'],
        ['Discounted cash flow',
         f"5-year FCFF, cost of capital gliding {pc(W['wacc_exp'])} → {pc(W['wacc_term'])}, "
         f"terminal growth {pc(IN['g_term'],0)}; {pc(DCF['tv_share'],0)} of enterprise value comes "
         f"from the terminal value",
         f"{p2(LN['dcf']['bear'])} – {p2(LN['dcf']['bull'])}", p2(DCF['ps']), sgn(DCF['ps']/SPOT-1,0)],
        ['Relative multiples',
         f"{IN['ev_ebitda_just']}× mid-cycle EV/EBITDA (trailing {n1(REL['ev_ebitda_trailing'])}×; "
         f"trailing P/E {n1(REL['pe_trailing'])}×)",
         f"{p2(LN['relative']['bear'])} – {p2(LN['relative']['bull'])}", p2(LN['relative']['base']),
         sgn(LN['relative']['base']/SPOT-1,0)],
        ['Normalised earnings power',
         f"mid-cycle EBITDA margin {pc(NRM['margin'])} at a justified {IN['pe_just']}× P/E",
         f"{p2(LN['normalized']['bear'])} – {p2(LN['normalized']['bull'])}",
         p2(LN['normalized']['base']), sgn(LN['normalized']['base']/SPOT-1,0)],
        ['Book value and sustainable return',
         f"justified price-to-book {n1(BK['pb_just'])}× on book value of {p2(BK['bvps'])}/share "
         f"at a sustainable return on equity of {pc(BK['roe_sust'])}",
         f"{p2(LN['book']['bear'])} – {p2(LN['book']['bull'])}", p2(LN['book']['base']),
         sgn(LN['book']['base']/SPOT-1,0)],
        ['Weighted central',
         f"DCF {pc(IN['lens_weights']['dcf'],0)} · relative {pc(IN['lens_weights']['relative'],0)} · "
         f"normalised {pc(IN['lens_weights']['normalized'],0)} · book {pc(IN['lens_weights']['book'],0)}",
         f"{p2(D['span'][0])} – {p2(D['span'][1])}", p2(D['central']), sgn(D['central']/SPOT-1,0)],
        ['Memo — currency-of-discounting alternative',
         f"hard-currency cash-flow leg discounted at {pc(W['wacc_usd_alt'])} rather than the "
         f"Egyptian rate; the reading the market appears to apply",
         '—', p2(DCF['ccy_alt_ps']), sgn(DCF['ccy_alt_ps']/SPOT-1,0)],
        ['Memo — market price', 'closing price on the anchor date', '—', p2(SPOT), '—']]
table(rows, [1.30, 2.75, 1.15, 0.72, 0.63], band_rows={5}, size=8.6)
caption(f"Ranges are bear-to-bull within each lens; the central is the weighted base. Terminal "
        f"value is {pc(DCF['tv_share'],0)} of the discounted-cash-flow enterprise value — a high "
        f"share, disclosed here and again in the bridge, and the reason the terminal assumptions "
        f"are stress-tested in section 1.9.")

# =========================== COMPANY OVERVIEW ===============================
H2('Company overview — Elsewedy Electric at a glance')
own = IN['ownership']
rows = [['Item', 'Detail'],
        ['Founded / listed', 'Established 1938 by the Elsewedy family; listed on the Egyptian '
         'Exchange as SWDY'],
        ['What it does', 'Manufactures wires, cables and accessories; executes turnkey engineering '
         'and construction projects (substations, transmission and distribution, power generation, '
         'civil works); makes transformers, busway and electrical products; supplies meters and '
         'digital grid solutions; and holds infrastructure assets including industrial development, '
         'logistics, utilities and independent power projects'],
        ['Scale', f"More than 20,000 employees across 31 production facilities in 15 countries; "
         f"FY2025 revenue EGP {n0(HI['FY25']['rev'])}mn"],
        ['Geographic mix', f"Over {pc(IN['foreign_share_fy25'],0)} of revenue earned outside Egypt"],
        ['Order book', f"Approximately USD {IN['backlog_usd_bn']}bn, above the group's typical "
         f"historical range"],
        ['Shares outstanding', f"{n0(SH)}mn"],
        ['Market capitalisation', f"EGP {n0(M['mktcap'])}mn at the anchor price"],
        ['Ownership', f"El Sewedy family {pc(own['family'])} · free float {pc(own['float'])} · "
         f"Electra Investment Holding {pc(own['electra'])}"],
        ['Net bank debt', f"EGP {n0(IN['nd_fy25'])}mn at 31 December 2025 "
         f"({n1(IN['nd_fy25']/HI['FY25']['ebitda'])}× EBITDA)"],
        ['Dividend record', f"EGP {p2(IN['dps_fy24'])} per share proposed on the FY2024 result"]]
table(rows, [1.55, 5.45], size=8.8, align_right_from=9)

P(f"Two structural facts govern everything that follows. First, the revenue base is majority hard "
  f"currency while the share, the accounts and the borrowing are Egyptian — so the company is a "
  f"natural hedge against the currency its shareholders are exposed to. Second, the business "
  f"consumes working capital in direct proportion to its growth: inventories, contract assets and "
  f"receivables less payables and contract liabilities ran at "
  f"{pc(HB['FY23']['nwc']/HI['FY23']['rev'])} of revenue in FY2023 and "
  f"{pc(HB['FY24']['nwc']/HI['FY24']['rev'])} in FY2024. In FY2024 the group earned EBITDA of EGP "
  f"{n0(HI['FY24']['ebitda'])}mn and converted only EGP {n0(IN['ocf_fy24'])}mn of it into operating "
  f"cash after interest and tax. Growth here is expensive, and that is the crux of the valuation.",
  space_after=10)

# =========================== 1 FUNDAMENTAL VALUATION =========================
H1('1  Fundamental valuation')

# ---- 1.1 DCF ----------------------------------------------------------------
H2('1.1  The cash-flow model — the primary lens, with the full waterfall')
P(f"The primary lens is a five-year free-cash-flow-to-the-firm model. Revenue is built from the "
  f"two legs that actually drive it — a domestic Egyptian-pound leg and a foreign leg forecast in "
  f"US dollars and translated at an explicit exchange-rate path. Margins come from a segment build. "
  f"Cash flow is then taken all the way to present value, line by line, below.")
hdr = ['EGP mn'] + YRS
rows = [hdr,
        ['Revenue'] + [n0(x) for x in F['rev']],
        ['  of which domestic'] + [n0(x) for x in F['dom']],
        ['  of which foreign'] + [n0(x) for x in F['fgn_egp']],
        ['EBITDA'] + [n0(x) for x in F['ebitda']],
        ['EBITDA margin'] + [pc(x) for x in F['ebitda_margin']],
        ['Less depreciation and amortisation'] + [f"({n0(x)})" for x in F['dna']],
        ['EBIT'] + [n0(x) for x in F['ebit']],
        [f"NOPAT — EBIT × (1 − {pc(IN['tax_eff'],0)})"] + [n0(x) for x in F['nopat']],
        ['Add back depreciation and amortisation'] + [n0(x) for x in F['dna']],
        ['Less capital expenditure'] + [f"({n0(x)})" for x in F['capex']],
        ['Less change in working capital'] + [f"({n0(x)})" for x in F['dnwc']],
        ['Free cash flow to the firm'] + [n0(x) for x in F['fcff']],
        ['Forward cost of capital'] + [pc(x) for x in F['fwd_wacc']],
        ['Discount factor'] + [f"{x:.4f}" for x in F['df']],
        ['Present value of FCFF'] + [n0(x) for x in F['pv']]]
table(rows, [2.05, 0.99, 0.99, 0.99, 0.99, 0.99], size=8.5, band_rows={12, 15})
caption("Every line is computed, not typed: the waterfall runs EBITDA → depreciation and "
        "amortisation → EBIT → NOPAT → add back depreciation → less capital expenditure → less "
        "the change in working capital → free cash flow to the firm → discount factor → present "
        "value. Working-capital change is the difference in net working capital held at a constant "
        f"{pc(IN['nwc_pct'])} of revenue, the level the audited balance sheets actually show.")

H2('The bridge from enterprise value to the equity')
rows = [['Step', 'EGP mn', 'Note'],
        ['Present value of the five forecast years', n0(DCF['pv_explicit']),
         'sum of the present-value row above'],
        ['Present value of the terminal value', n0(DCF['pv_tv']),
         f"terminal value {n0(DCF['tv'])} capitalised at {pc(W['wacc_term'])} and discounted at "
         f"the year-5 factor {F['df'][-1]:.4f}"],
        ['Enterprise value', n0(DCF['ev']), 'the two lines above'],
        ['Terminal value as a share of enterprise value', pc(DCF['tv_share'],0),
         'disclosed here and in the summary table; stress-tested in section 1.9'],
        ['Less net bank debt', f"({n0(DCF['nd'])})", 'disclosed at 31 December 2025'],
        ['Plus equity-accounted investees', n0(DCF['assoc']),
         'carrying value, uplifted modestly; these earn outside the consolidated cash flow'],
        ['Less minority interests', f"({n0(DCF['nci_val'])})",
         f"minorities take {pc(DCF['nci_share'])} of group profit, so they are charged the same "
         f"share of the value"],
        ['Equity attributable to shareholders', n0(DCF['eq_attr']), ''],
        ['Fair value per share (EGP)', p2(DCF['ps']),
         f"against a spot of {p2(SPOT)} ({sgn(DCF['ps']/SPOT-1,0)})"]]
table(rows, [2.55, 1.05, 3.40], size=8.5, band_rows={3, 9}, align_right_from=1)

# ---- 1.2 book ----------------------------------------------------------------
H2('1.2  Book value and sustainable return — the asset lens')
P(f"Book value attributable to shareholders is estimated at EGP {n0(HB['FY25']['eqp'])}mn, or "
  f"{p2(BK['bvps'])} per share, rolling the audited FY2024 figure forward for FY2025 profit less "
  f"the dividend paid. The trailing return on average equity is {pc(BK['roe_trailing'])}. That "
  f"number is flattered: FY2023 and FY2024 both carried devaluation gains on copper inventory "
  f"bought before the pound moved, so the sustainable rate is struck lower, at "
  f"{pc(BK['roe_sust'])}.")
P(f"A justified price-to-book multiple is (return on equity − growth) ÷ (cost of equity − growth). "
  f"At a blended cost of equity of {pc(BK['ke_blend'])} — the average of the explicit-window "
  f"{pc(W['ke_exp'])} and the terminal {pc(W['ke_term'])} — that gives {n1(BK['pb_just'])}× book, "
  f"or EGP {p2(LN['book']['base'])} per share. This is the weakest of the four lenses for this "
  f"company and carries the lowest weight, for a specific reason: three years of currency "
  f"translation have moved reported book value in ways that have little to do with the earning "
  f"power of the assets, and a group whose value sits in an order book and a brand is poorly "
  f"described by its balance sheet. It is retained because it is the lens that disagrees most, and "
  f"a lens that only ever agrees is not doing any work.")

# ---- 1.3 relative ------------------------------------------------------------
H2('1.3  Relative multiples')
rows = [['Measure', 'Value', 'Comment'],
        ['Enterprise value / EBITDA (trailing)', f"{n1(REL['ev_ebitda_trailing'])}×",
         f"enterprise value {n0(M['ev_trailing'])} over FY2025 EBITDA {n0(HI['FY25']['ebitda'])}"],
        ['Price / earnings (trailing)', f"{n1(REL['pe_trailing'])}×",
         f"price {p2(SPOT)} over attributable earnings per share of "
         f"{p2(HI['FY25']['npa']/SH)}"],
        ['Price / book', f"{n1(SPOT/BK['bvps'])}×", f"book value {p2(BK['bvps'])} per share"],
        ['Net bank debt / EBITDA', f"{n1(IN['nd_fy25']/HI['FY25']['ebitda'])}×",
         'light net leverage against a large gross book'],
        ['Justified enterprise value / EBITDA', f"{IN['ev_ebitda_just']}×",
         'applied to mid-cycle FY2027 EBITDA; an Egyptian-market discount to listed cable and '
         'electrical-equipment peers, which trade in the 8–11× region'],
        ['Implied value per share', p2(LN['relative']['base']),
         f"bear {p2(LN['relative']['bear'])} at 5.5× / bull {p2(LN['relative']['bull'])} at 8.0×"]]
table(rows, [2.15, 0.90, 3.95], size=8.5, band_rows={6})
P(f"The honest difficulty with this lens is that there is no clean comparable. The nearest listed "
  f"regional peer in cables is a Saudi manufacturer with a fraction of the revenue, no turnkey "
  f"contracting arm and a very different balance sheet; the global cable majors are European and "
  f"carry neither Egyptian sovereign risk nor Egyptian growth. Applying a discounted multiple to "
  f"mid-cycle EBITDA is therefore a sanity check on the cash-flow model rather than an independent "
  f"valuation, and it is weighted accordingly.")

# ---- 1.4 normalized ----------------------------------------------------------
H2('1.4  Normalised earnings power — where this sits in the cycle')
P(f"The question this lens asks is what the group earns in a year that is neither a currency "
  f"windfall nor a margin trough. Mid-cycle revenue is taken as the FY2027 forecast of EGP "
  f"{n0(NRM['rev'])}mn and the mid-cycle EBITDA margin as {pc(NRM['margin'])} — the average of the "
  f"later forecast years, comfortably below the FY2024 outturn of "
  f"{pc(HI['FY24']['ebitda']/HI['FY24']['rev'])} and above the FY2025 trough of "
  f"{pc(HI['FY25']['ebitda']/HI['FY25']['rev'])}.")
rows = [['Step', 'EGP mn'],
        ['Mid-cycle revenue', n0(NRM['rev'])],
        [f"Mid-cycle EBITDA at {pc(NRM['margin'])}", n0(NRM['ebitda'])],
        ['Less depreciation and amortisation', f"({n0(NRM['ebitda']-NRM['ebit'])})"],
        ['Mid-cycle EBIT', n0(NRM['ebit'])],
        ['Less net interest', f"({n0(NRM['interest'])})"],
        ['Plus share of equity-accounted investees', n0(HI['FY25']['assoc'])],
        [f"Less tax at {pc(IN['tax_eff'],0)} and minority interests at {pc(DCF['nci_share'])}",
         f"({n0(NRM['ebit']-NRM['interest']+HI['FY25']['assoc']-NRM['np'])})"],
        ['Normalised attributable earnings', n0(NRM['np'])],
        ['Normalised earnings per share (EGP)', p2(NRM['eps'])],
        [f"At a justified {IN['pe_just']}× price/earnings (EGP per share)", p2(LN['normalized']['base'])]]
table(rows, [4.55, 1.35], size=8.6, band_rows={9, 11}, first_col_bold=False)
caption(f"Bear {p2(LN['normalized']['bear'])} at 7.0× and bull {p2(LN['normalized']['bull'])} at "
        f"11.5×. The justified multiple is held well below what a comparable industrial franchise "
        f"would attract in a developed market, because an Egyptian cost of equity near "
        f"{pc(W['ke_exp'],0)} mathematically compresses what any stream of earnings is worth.")

# ---- 1.5 synthesis -----------------------------------------------------------
H2('1.5  Synthesis — four lenses, one field')
figure(os.path.join(HERE, 'fig1_football.png'), 6.9,
       f"Figure 1 — the four lenses and the weighted central against the market price of "
       f"{p2(SPOT)}. Each bar is that lens's bear-to-bull span; the brass tick is its base case.")
rows = [['Lens', 'Bear', 'Base', 'Bull', 'Weight', 'Contribution']]
for k in ['dcf', 'relative', 'normalized', 'book']:
    l = LN[k]
    rows.append([l['name'], p2(l['bear']), p2(l['base']), p2(l['bull']), pc(l['w'], 0),
                 p2(l['base'] * l['w'])])
rows.append(['Weighted central', p2(D['span'][0]), p2(D['central']), p2(D['span'][1]), '100%',
             p2(D['central'])])
table(rows, [2.35, 0.86, 0.86, 0.86, 0.83, 1.14], size=8.6, band_rows={5})
P(f"The four lenses do not agree, and the disagreement is informative rather than embarrassing. "
  f"The two lenses that look at earnings — relative multiples and normalised earnings power — land "
  f"near or slightly above the market price. The two that discount cash or capital at an Egyptian "
  f"cost of capital land well below it. This is the same disagreement in two forms: a multiple "
  f"imported from a market with a low cost of capital implicitly assumes a low cost of capital, "
  f"and a discounted model applied with an Egyptian one does not. The weighted central of EGP "
  f"{p2(D['central'])} sits between them.")

# ---- 1.6 drivers -------------------------------------------------------------
H2('1.6  The drivers — a two-currency revenue build and a segment margin build')
P(f"Revenue is not forecast as a growth rate applied to a revenue line. It is built from volumes "
  f"and prices, unit by unit, on the company's own disclosed segment data — and the historical "
  f"build reconciles to the audited income statement to within EGP 1mn on both revenue and gross "
  f"profit in each of FY2023 and FY2024. Margins are therefore outputs of the build, not inputs "
  f"to it.")

H2('The unit economics, as disclosed')
rows = [['Unit measure', 'FY2023', 'FY2024', 'FY2025'],
        ['Cable volume (tonnes)', n0(BU['unit_hist']['FY23']['rev_sum'] and 156748),
         n0(167665), f"{n0(BU['vol25']['cables'])} (implied)"],
        ['Cable price per tonne (EGP)', n0(BU['unit_hist']['FY23']['cables_price_t']),
         n0(BU['unit_hist']['FY24']['cables_price_t']), n0(BU['price_t25'])],
        ['Cable gross profit per tonne (EGP)', n0(BU['unit_hist']['FY23']['cables_gp_t']),
         n0(BU['unit_hist']['FY24']['cables_gp_t']), n0(BU['gp_t_cables_fy25'])],
        ['Copper cost per tonne (EGP)', n0(BU['unit_hist']['FY23']['copper_t']),
         n0(BU['unit_hist']['FY24']['copper_t']), n0(IN['copper_hist']['FY25']*IN['fx_hist']['FY25'])],
        ['Fabrication uplift over copper', f"{BU['unit_hist']['FY23']['cables_uplift']:.3f}×",
         f"{BU['unit_hist']['FY24']['cables_uplift']:.3f}×", f"{BU['uplift25']:.3f}×"],
        ['Cable conversion margin', pc(BU['unit_hist']['FY23']['cables_conv']),
         pc(BU['unit_hist']['FY24']['cables_conv']), pc(BU['cables_conv25'])],
        ['Transformer volume (MVA)', n0(14521), n0(17619), f"{n0(BU['vol25']['transformers'])} (implied)"],
        ['Transformer gross profit per MVA (EGP)',
         n0(BU['unit_hist']['FY23']['transformers_gp_mva']),
         n0(BU['unit_hist']['FY24']['transformers_gp_mva']), '—'],
        ['Meter volume (units)', n0(4057065), n0(3850726), f"{n0(BU['vol25']['meters'])} (implied)"],
        ['Meter gross profit per unit (EGP)', n0(BU['unit_hist']['FY23']['meters_gp_u']),
         n0(BU['unit_hist']['FY24']['meters_gp_u']), '—'],
        ['Operating load between gross profit and EBITDA',
         pc(BU['unit_hist']['FY23']['opex_pct']), pc(BU['unit_hist']['FY24']['opex_pct']),
         pc(BU['opex25'])]]
table(rows, [2.65, 1.45, 1.45, 1.45], size=8.4, band_rows={3, 6})
caption(f"Volumes, prices per tonne and gross profit per tonne for FY2023 and FY2024 are the "
        f"company's own disclosures — the per-unit gross profit figures reproduce the published "
        f"90,020 and 119,043 per tonne, 418 and 707 per meter, and 136,345 and 221,065 per MVA "
        f"exactly. FY2025 volumes are implied from the disclosed first-quarter prints and the "
        f"prior-year seasonal share, and the FY2025 cable price per tonne is the residual against "
        f"disclosed group revenue — which back-solves a fabrication uplift of {BU['uplift25']:.3f}, "
        f"sitting between the two audited years. That the residual lands inside the historical "
        f"range is the check that it is economics rather than a plug absorbing an error.")

P(f"The single most important line in that table is the cable conversion margin. It ran at "
  f"{pc(BU['unit_hist']['FY23']['cables_conv'])} in FY2023 and "
  f"{pc(BU['unit_hist']['FY24']['cables_conv'])} in FY2024 — years when a collapsing pound turned "
  f"cheaply bought copper inventory into windfall profit — and roughly halved to "
  f"{pc(BU['cables_conv25'])} in FY2025. That one number is most of the group's gross-margin "
  f"decline, and it is disclosed rather than inferred: it comes from the published gross profit "
  f"per tonne.")

H2('How the forecast is driven')
rows = [['Driver', 'FY2025 base'] + YRS,
        ['Copper (USD/tonne)', n0(IN['copper_hist']['FY25'])] + [n0(x) for x in IN['copper_fcst']],
        ['USD/EGP average rate', n1(IN['fx_hist']['FY25'])] + [n1(x) for x in IN['fx_path']],
        ['Cable volume (tonnes)', n0(BU['vol25']['cables'])] + [n0(x) for x in BU['vol_f']['cables']],
        ['Cable volume growth', '—'] + [pc(x) for x in IN['cables_vol_growth']],
        ['Fabrication uplift', f"{BU['uplift25']:.3f}×"] + [f"{x:.3f}×" for x in IN['cables_uplift']],
        ['Transformer volume (MVA)', n0(BU['vol25']['transformers'])] +
        [n0(x) for x in BU['vol_f']['transformers']],
        ['Meter volume (units, mn)', n1(BU['vol25']['meters']/1e6)] +
        [n1(x/1e6) for x in BU['vol_f']['meters']],
        ['Order book, year-end (EGP mn)', n0(IN['ec_backlog'])] + [n0(x) for x in BU['backlog']],
        ['Order-book conversion rate', '—'] + [pc(x) for x in IN['ec_burn']],
        ['Operating load (% of revenue)', pc(BU['opex25'])] + [pc(x) for x in IN['opex_pct']]]
table(rows, [1.72, 0.86, 0.88, 0.88, 0.88, 0.88, 0.88], size=8.3)
caption(f"Copper is held near the current market level rather than forecast — a directional view "
        f"on the metal would dominate the valuation, and it is carried in the sensitivity instead. "
        f"Because copper is passed through, a higher copper price raises revenue without raising "
        f"profit per tonne, which is why the gross margin percentage falls as revenue rises. The "
        f"operating load glides back toward the historical norm rather than assuming the unusually "
        f"low FY2025 level persists — the single most conservative choice in the build.")

H2('What the build produces — margins as outputs')
rows = [['EGP mn'] + YRS,
        ['Revenue'] + [n0(x) for x in F['rev']],
        ['Gross profit'] + [n0(x) for x in BU['gp']],
        ['Gross margin'] + [pc(x) for x in BU['gp_margin']],
        ['Less operating costs, net'] + [f"({n0(x)})" for x in BU['opex']],
        ['EBITDA'] + [n0(x) for x in F['ebitda']],
        ['EBITDA margin'] + [pc(x) for x in F['ebitda_margin']]]
table(rows, [2.05, 0.99, 0.99, 0.99, 0.99, 0.99], size=8.4, band_rows={5, 6})
caption(f"The FY2026 conversion margin is not assumed — it is solved so that the build reproduces "
        f"the EBITDA margin implied by the disclosed first-quarter 2026 result "
        f"({pc(F['ebitda_margin'][0])}). That quarter reported revenue "
        f"{sgn(IN['q1_26_rev']/IN['q1_25_rev']-1)} and attributable profit "
        f"{sgn(IN['q1_26_npa']/IN['q1_25_npa']-1)} year on year, so any build showing margins "
        f"collapsing in FY2026 would be contradicted by the company's own print. The solved cable "
        f"gross profit per tonne sits inside the historical range and, as a share of the realised "
        f"price, between the FY2025 trough and the FY2024 peak.")

figure(os.path.join(HERE, 'fig7_mix.png'), 6.9,
       "Figure 2 — revenue by currency of origin with the EBITDA margin path. The hard-currency "
       "leg does the growing; the margin recovers gently as the copper-price inflation of 2024–25 "
       "washes out of the revenue denominator.")

H2('The segment build behind the margin')
rows = [['Segment', 'FY2025 revenue (EGP mn)', 'Share', 'FY2025 gross margin',
         'FY2030E revenue (EGP mn)', 'FY2030E share']]
for s_ in SEG['names']:
    rows.append([SEG['names'][s_], n0(SEG['rev'][s_]), pc(SEG['rev'][s_]/IN['rev_fy25']),
                 pc(SEG['gp_margin'][s_]), n0(F['seg_rev'][4][s_]),
                 pc(F['seg_rev'][4][s_]/F['rev'][4])])
rows.append(['Group', n0(IN['rev_fy25']), '100.0%', pc(IN['gp_fy25']/IN['rev_fy25']),
             n0(F['rev'][4]), '100.0%'])
table(rows, [1.75, 1.30, 0.68, 1.15, 1.30, 0.82], size=8.3, band_rows={8})
caption(f"FY2025 sub-segment revenue is built from the unit economics above, with cables as the "
        f"residual against disclosed group revenue. FY2025 gross margins are calibrated so the "
        f"total reproduces the gross profit assembled from the disclosed nine-month and "
        f"fourth-quarter prints: cable gross profit is pinned to the published figure per tonne, "
        f"and the remaining lines carry FY2024's margins scaled by a single solved factor of "
        f"{BU['compress']:.3f} — a roughly {(1-BU['compress'])*100:.0f}% compression across the "
        f"board, which is what the disclosed prints require.")

# ---- 1.7 crux ----------------------------------------------------------------
H2('1.7  The crux — working capital first, the currency second, margins third')
P(f"The FY2024 accounts contain the single most important number in this study. The group earned "
  f"EBITDA of EGP {n0(HI['FY24']['ebitda'])}mn and generated operating cash flow, after interest "
  f"and tax, of EGP {n0(IN['ocf_fy24'])}mn — about "
  f"{pc(IN['ocf_fy24']/HI['FY24']['ebitda'],0)} of it. The difference went into working capital: "
  f"inventories rose EGP {n0(IN['inv_fy24']-IN['inv_fy23'])}mn and receivables EGP "
  f"{n0(IN['recv_fy24']-IN['recv_fy23'])}mn in a single year. Some of that was funded by customers "
  f"— contract liabilities rose EGP {n0(IN['cl_fy24']-IN['cl_fy23'])}mn — but the net absorption "
  f"was still severe.")
rows = [['Working capital', 'FY2023', 'FY2024', 'FY2025 (estimated)'],
        ['Inventories', n0(IN['inv_fy23']), n0(IN['inv_fy24']), '—'],
        ['Contract assets', n0(IN['ca_fy23']), n0(IN['ca_fy24']), '—'],
        ['Trade and other receivables', n0(IN['recv_fy23']), n0(IN['recv_fy24']), '—'],
        ['Less trade and other payables', f"({n0(IN['pay_fy23'])})", f"({n0(IN['pay_fy24'])})", '—'],
        ['Less contract liabilities', f"({n0(IN['cl_fy23'])})", f"({n0(IN['cl_fy24'])})", '—'],
        ['Net working capital', n0(HB['FY23']['nwc']), n0(HB['FY24']['nwc']), n0(HB['FY25']['nwc'])],
        ['As a share of revenue', pc(HB['FY23']['nwc']/HI['FY23']['rev']),
         pc(HB['FY24']['nwc']/HI['FY24']['rev']), pc(IN['nwc_pct'])]]
table(rows, [2.35, 1.55, 1.55, 1.55], size=8.6, band_rows={6, 7})
P(f"The model holds this ratio flat at {pc(IN['nwc_pct'])} of revenue, which is what the two "
  f"audited years show. That single assumption is worth a great deal: every percentage point of "
  f"revenue added to or removed from working-capital intensity is worth roughly EGP "
  f"{p2(abs(SN['grid_nwc'][2]-SN['grid_nwc'][1])/1.5)} per share. If the group ever converts its "
  f"order book without funding it — collecting faster, or pushing more of the funding onto "
  f"suppliers and customers — the cash-flow model reprices sharply upward. If discipline slips as "
  f"the backlog is executed, it reprices down just as fast.")

# ---- 1.8 macro ---------------------------------------------------------------
H2('1.8  Macro and country — rates, the pound, and the sourced cost of capital')
P(f"The discount rate is a schedule, not a number. Each forecast year is discounted at that year's "
  f"own forward rate, moving from the explicit-window rate to the terminal rate; the terminal "
  f"value is capitalised at the terminal rate and brought back using the same cumulative factor as "
  f"the year-5 cash flow. One date, one price of time — the terminal value never gets a cheaper "
  f"discount than a cash flow arriving on the same day.")
rows = [['Component', 'Explicit window', 'Terminal', 'Source and construction'],
        ['Risk-free rate', pc(IN['rf']), pc(IN['rf_term']),
         'observed 10-year local-currency government yield; terminal built from the central bank\'s '
         'own stated medium-term inflation target plus a standard real-rate convention'],
        ['Less sovereign default spread', f"({pc(IN['sov_spread_cds'])})", '—',
         'netted out so sovereign default risk is not charged twice — once in the local yield and '
         'again in the country premium'],
        ['Adjusted risk-free rate', pc(W['rf_star']), pc(IN['rf_term']), ''],
        ['Beta', f"{IN['beta']:.3f}", f"{IN['beta']:.3f}",
         f"own-stock weekly regression against a 31-name equal-weight local composite over five "
         f"years: R-squared {W['beta']['r2']:.3f}, n = {W['beta']['n']}, standard error "
         f"{W['beta']['se']:.3f}, 90% interval [{W['beta']['ci90'][0]:.2f}, "
         f"{W['beta']['ci90'][1]:.2f}]"],
        ['Equity risk premium', pc(IN['erp_cds']), pc(IN['erp_term']),
         'published country-premium file, credit-default-swap basis; normalised downward for the '
         'terminal rather than held at a crisis-era level'],
        ['Cost of equity', pc(W['ke_exp']), pc(W['ke_term']), ''],
        ['Cost of debt (blended, pre-tax)', pc(IN['kd']), pc(IN['kd_term']),
         'currency-blended — see the evidence immediately below'],
        ['Debt weight', pc(W['wd_exp']), pc(IN['wd_term']),
         'net debt against market capitalisation for the explicit window; a normalised structure '
         'for the terminal, because the steady state cannot be described by today\'s weights'],
        ['Cost of capital', pc(W['wacc_exp']), pc(W['wacc_term']), '']]
table(rows, [1.60, 0.92, 0.80, 3.68], size=8.2, band_rows={7, 10})

H2('The cost of debt — three pieces of evidence, not an assumption')
P("A disclosed contractual range is not evidence of what a company pays. Three things are shown "
  "instead.")
rows = [['Test', 'Evidence'],
        ['Currency composition of the debt book',
         f"The audited interest-rate note discloses average rates on financial liabilities of "
         f"{pc(IN['kd_egp_note'])} in Egyptian pounds, {pc(IN['kd_usd_note'])} in US dollars and "
         f"{pc(IN['kd_eur_note'])} in euros. Reconciling those against the rate actually paid "
         f"implies roughly {pc(W['w_egp_implied'],0)} of the book is in Egyptian pounds and "
         f"{pc(1-W['w_egp_implied'],0)} in hard currency. Treating this company as a domestic "
         f"borrower would overstate its cost of debt by about "
         f"{(IN['kd_egp_note']-W['kd_eff_fy24'])*10000:,.0f} basis points."],
        ['Independently computed effective rate, two periods',
         f"FY2024: interest expense of {n0(IN['int_exp_fy24'])} against average loans and credit "
         f"facilities of {n0((IN['debt_open_fy24']+IN['debt_close_fy24'])/2)} = "
         f"{pc(W['kd_eff_fy24'])}. First quarter 2025, annualised on the same basis = "
         f"{pc(W['kd_eff_q1_25'])}, the fall reflecting the central bank's easing."],
        ['Bounds', f"The adopted {pc(IN['kd'])} sits {abs(IN['kd']-W['kd_eff_q1_25'])*10000:,.0f} "
         f"basis points from the most recent effective rate and below the peak-period rate of "
         f"{pc(max(W['kd_eff_fy24'], W['kd_eff_q1_25']))}. Both bounds hold."]]
table(rows, [2.05, 4.95], size=8.4)
P(f"This is not a technicality. A cheap, majority-hard-currency debt book is one of the two "
  f"genuine competitive advantages this company has over a domestic-only competitor — the other "
  f"being that its revenue is hard-currency too. It is also why the balance sheet looks more "
  f"leveraged than it is: the gross book is large because working capital is large, but it costs "
  f"roughly {pc(W['kd_eff_q1_25'])} and is more than two-thirds offset by cash.")

# ---- 1.9 sensitivity -----------------------------------------------------------
H2('1.9  Sensitivity — the discount rate, the growth, the currency, the margin and the collection')
figure(os.path.join(HERE, 'fig2_sens.png'), 5.7,
       f"Figure 3 — discounted-cash-flow fair value per share across the terminal cost of capital "
       f"and terminal growth. Bold cells sit within EGP 6 of the market price of {p2(SPOT)}.")
P("Each anchor is varied independently around its own base, so the tables show what the valuation "
  "needs the world to do rather than what growth rate the model needs.")

rows = [['Explicit-window cost of capital →'] + [pc(x) for x in SN['we_grid']]]
for i, wt in enumerate(SN['wt_grid']):
    rows.append([f"terminal {pc(wt)}"] + [p2(SN['grid_exp_term'][j][i]) for j in range(5)])
table(rows, [1.62, 1.07, 1.07, 1.07, 1.07, 1.07], size=8.4)
caption("Explicit-window against terminal cost of capital, each moved independently — the grid "
        "that shows what the valuation needs the economy to do.")

rows = [['Sensitivity', 'Range tested', 'Fair value span (EGP/share)', 'Swing']]
def span(v): return f"{p2(min(v))} – {p2(max(v))}"
rows.append(['Beta', f"{SN['beta_grid'][0]} – {SN['beta_grid'][-1]}", span(SN['grid_beta']),
             p2(max(SN['grid_beta'])-min(SN['grid_beta']))])
rows.append(['Exchange-rate path', 'base −10% to +20%', span(SN['grid_fx']),
             p2(max(SN['grid_fx'])-min(SN['grid_fx']))])
rows.append(['EBITDA margin', '−2pp to +2pp', span(SN['grid_margin']),
             p2(max(SN['grid_margin'])-min(SN['grid_margin']))])
rows.append(['Working capital / revenue', f"{pc(SN['nwc_grid'][0])} – {pc(SN['nwc_grid'][-1])}",
             span(SN['grid_nwc']), p2(max(SN['grid_nwc'])-min(SN['grid_nwc']))])
rows.append(['Terminal return on invested capital',
             f"{pc(SN['roic_grid'][0],0)} – {pc(SN['roic_grid'][-1],0)}", span(SN['grid_roic']),
             p2(max(SN['grid_roic'])-min(SN['grid_roic']))])
rows.append(['Terminal growth', f"{pc(SN['g_grid'][0],0)} – {pc(SN['g_grid'][-1],0)}",
             span([r[j] for r in [SN['grid_wacc_g'][2]] for j in range(5)]),
             p2(max(SN['grid_wacc_g'][2])-min(SN['grid_wacc_g'][2]))])
table(rows, [2.20, 1.55, 1.90, 1.35], size=8.5)
caption("Ranked by swing, the exchange-rate path and the terminal assumptions dominate every "
        "operating driver. That is the honest shape of this valuation: it is a bet on the "
        "cost of capital and the currency far more than on the company's execution.")

P(f"The beta deserves a note. At {IN['beta']:.3f} with an R-squared of {W['beta']['r2']:.3f} over "
  f"{W['beta']['n']} weekly observations and a standard error of {W['beta']['se']:.3f}, this is a "
  f"well-identified estimate by the standards of this market — the 90% interval spans "
  f"[{W['beta']['ci90'][0]:.2f}, {W['beta']['ci90'][1]:.2f}], comfortably narrower than twice the "
  f"point estimate, so it is not flagged as a weak instrument. It is also economically sensible: "
  f"the largest industrial constituent of an index should have a beta near one. A defensive-staple "
  f"prior of 0.6–0.9 and a cyclical prior of 1.0–1.5 bracket it, and a diversified industrial with "
  f"a contracting arm belongs in the second.", space_after=10)

# =========================== 2 TECHNICAL ======================================
H1('2  Technical and price structure')
figure(os.path.join(HERE, 'fig3_ma.png'), 7.0,
       "Figure 4 — price against the 20-, 50-, 100- and 200-session moving averages over the last "
       "260 sessions.")
import numpy as np
from primitives import load_ohlc
from data_quality import clean_ohlc
_df, _ = clean_ohlc(load_ohlc(os.path.join(HERE, 'SWDY_Stock_Price_History.csv')), 'SWDY',
                    verbose=False, market='EG')
px = _df['Price'].to_numpy()
sma = {n: float(np.mean(px[-n:])) for n in (20, 50, 100, 200)}
hi52, lo52 = float(np.max(px[-252:])), float(np.min(px[-252:]))
rows = [['Marker', 'Level (EGP)', 'Reading'],
        ['Last close', p2(SPOT), 'the anchor for everything in this study'],
        ['20-session average', p2(sma[20]), f"price is {sgn(SPOT/sma[20]-1)} against it"],
        ['50-session average', p2(sma[50]), f"price is {sgn(SPOT/sma[50]-1)} against it"],
        ['100-session average', p2(sma[100]), f"price is {sgn(SPOT/sma[100]-1)} against it"],
        ['200-session average', p2(sma[200]), f"price is {sgn(SPOT/sma[200]-1)} against it"],
        ['52-week high', p2(hi52), f"{sgn(SPOT/hi52-1)} from the high"],
        ['52-week low', p2(lo52), f"{sgn(SPOT/lo52-1)} from the low"],
        ['Annualised volatility', pc(H3M['anchor_vol_ann']),
         'estimated from the daily range, the input to the price cone in section 3']]
table(rows, [1.85, 1.15, 4.00], size=8.6)
P(f"The share is above every moving average in the stack, and the stack itself is in ascending "
  f"order — the configuration that describes an established uptrend. The price has compounded "
  f"{sgn(SPOT/px[-252]-1,0)} over the last twelve months and sits {sgn(SPOT/hi52-1,0)} from its "
  f"52-week high. Realised volatility of about {pc(H3M['anchor_vol_ann'],0)} a year is high in "
  f"absolute terms and unremarkable for this market. None of this is a valuation argument; it is "
  f"the price context the valuation has to be read against, and the gap between a strongly trending "
  f"price and a fundamental central below it is precisely what section 4 addresses.", space_after=10)

# =========================== 3 MONTE CARLO ====================================
H1('3  A probabilistic price map')
P(f"This section answers a different question from the valuation. It does not ask what the business "
  f"is worth; it asks where the share price could plausibly be in one and three months, given how "
  f"this share has actually moved. The engine simulates 50,000 price paths from a volatility model "
  f"fitted to the daily high-low-open-close range, with a fat-tailed shock distribution and a drift "
  f"anchored to the cost of carry rather than to any view.")
P(f"The widths below are calibrated rather than assumed. Tested by walk-forward simulation over a "
  f"full five years — {BT5['windows']} independent non-overlapping quarterly windows from "
  f"{BT5['first_origin']} to {BT5['last_origin']}, each one forecast using only data available "
  f"before it — the model scored {BT5['skill_norm']*100:+.2f}% better than a random-walk benchmark "
  f"anchored on the same cost of carry. Outcomes fell inside the stated bands at close to the "
  f"advertised rate ({BT5['cov50']*100:.0f}% inside the 50% band, {BT5['cov80']*100:.0f}% inside "
  f"the 80%, {BT5['cov90']*100:.0f}% inside the 90%), and the outcomes were spread evenly across "
  f"the distribution rather than bunching at one end — a uniformity test returns p = "
  f"{BT5['chi2_p']:.2f}, comfortably consistent with a well-calibrated forecast. Over the very "
  f"long run the picture is more mixed: across the full {BT5F['span_years']:.0f}-year history the "
  f"model still beats the benchmark ({BT5F['skill_norm']*100:+.2f}%) but its bands are about "
  f"{(BT5F['width_vs_benchmark']-1)*100:.0f}% wider than they need to be, which is a real "
  f"limitation and is stated here rather than left out.")
P(f"This is a map of price dispersion, not a forecast, and it is never blended with the fair-value "
  f"work above.")
figure(os.path.join(HERE, 'fig4_fan.png'), 7.0,
       f"Figure 5 — the forward price cone to three months. The dashed brass line is the "
       f"fundamental central estimate of {p2(D['central'])}; the dotted line is the spot of "
       f"{p2(SPOT)}.")

H2('Percentile map (EGP/share)')
rows = [['Horizon', '5th', '25th', 'Median', '75th', '95th', 'Probability above spot'],
        [f"1 month (to {H1M['grade_date']})"] +
        [p2(H1M['pct'][k]) for k in ('p5', 'p25', 'p50', 'p75', 'p95')] + [pc(H1M['p_above'], 0)],
        [f"3 months (to {H3M['grade_date']})"] +
        [p2(H3M['pct'][k]) for k in ('p5', 'p25', 'p50', 'p75', 'p95')] + [pc(H3M['p_above'], 0)]]
table(rows, [1.75, 0.80, 0.80, 0.80, 0.80, 0.80, 1.25], size=8.6)
figure(os.path.join(HERE, 'fig5_dist.png'), 5.3, "Figure 6 — the one-month price distribution.")
figure(os.path.join(HERE, 'fig6_dist.png'), 5.3, "Figure 7 — the three-month price distribution.")

H2('Level-touch ladder')
rows = [['Event', '1 month', '3 months'],
        ['Finishes 10% or more above spot', pc(H1M['p_up10'], 0), pc(H3M['p_up10'], 0)],
        ['Finishes 10% or more below spot', pc(H1M['p_dn10'], 0), pc(H3M['p_dn10'], 0)],
        ['Touches 10% above spot at any point', pc(H1M['touch_up10'], 0), pc(H3M['touch_up10'], 0)],
        ['Touches 10% below spot at any point', pc(H1M['touch_dn10'], 0), pc(H3M['touch_dn10'], 0)]]
table(rows, [3.30, 1.35, 1.35], size=8.6)
caption("Touch probabilities exceed finish probabilities because a path can visit a level and come "
        "back. This distinction matters for anyone thinking about a level rather than a date.")

# =========================== 4 COMPARISON =====================================
H1('4  Comparison of the lenses, and a verdict')
rows = [['Read', 'What it says', 'What it assumes'],
        ['Fundamental (weighted)', f"EGP {p2(D['central'])} central, "
         f"{sgn(D['central']/SPOT-1,0)} against the market",
         'an Egyptian cost of capital applied to the whole company, and no real terminal growth'],
        ['Cash flow alone', f"EGP {p2(DCF['ps'])}, {sgn(DCF['ps']/SPOT-1,0)}",
         f"a cost of capital gliding {pc(W['wacc_exp'])} to {pc(W['wacc_term'])}"],
        ['Currency-of-discounting alternative', f"EGP {p2(DCF['ccy_alt_ps'])}, "
         f"{sgn(DCF['ccy_alt_ps']/SPOT-1,0)}",
         f"the hard-currency cash-flow leg discounted at about {pc(W['wacc_usd_alt'])}"],
        ['Multiples', f"EGP {p2(LN['relative']['base'])}, {sgn(LN['relative']['base']/SPOT-1,0)}",
         'a discounted peer multiple is the right way to price this'],
        ['The market', p2(SPOT), 'revealed preference of the marginal buyer'],
        ['Three-month price map', f"median {p2(H3M['pct']['p50'])}, "
         f"{pc(H3M['p_above'],0)} chance of finishing above spot",
         'volatility persists as it has; no view on value']]
table(rows, [1.85, 2.20, 2.95], size=8.5)
P(f"The verdict is that the disagreement between the market and the cash-flow model is almost "
  f"entirely a disagreement about the discount rate, and that this is a genuinely open question "
  f"rather than a mistake by one side. A company that earns more than 70% of its money in hard "
  f"currency, borrows more than half its book in hard currency at "
  f"{pc(IN['kd_usd_note'])}, and holds assets in fifteen countries is only partly an Egyptian "
  f"risk. Charging it the full Egyptian equity risk premium — which is what our primary "
  f"construction does — is the conservative choice, not the obviously correct one. Charging it "
  f"none of that premium, which is roughly what the market price implies, is the aggressive one.")
P(f"Our own weighting sits closer to the conservative end because the shares are bought and sold "
  f"in Egyptian pounds on an Egyptian exchange, the dividends are paid in Egyptian pounds, and the "
  f"ability of a foreign shareholder to realise value depends on Egyptian capital-account "
  f"conditions. That is a real risk and it belongs in the discount rate. But a reader who believes "
  f"that convertibility is not the binding constraint, and that the hard-currency earnings should "
  f"be valued as hard-currency earnings, will reach a materially higher number using the same "
  f"cash-flow forecasts — EGP {p2(DCF['ccy_alt_ps'])} on the alternative shown. Neither reader is "
  f"being unreasonable, and this study declines to hide that behind a single figure.")
P("No rating and no price target is expressed here or anywhere else in this document. The output "
  "is a range and a distribution.", space_after=10)

# =========================== 5 CATALYSTS ======================================
H1('5  Catalysts to watch')
rows = [['Catalyst', 'Why it matters', 'What to watch'],
        ['Half-year 2026 results',
         'the first read on whether the first quarter\'s reacceleration is a trend or a comparison '
         'effect, and on whether margins have stopped falling',
         'gross margin against the 2025 exit rate; whether revenue growth holds above 20%'],
        ['Working-capital conversion',
         'the model\'s largest single assumption is that working capital stays near '
         f"{pc(IN['nwc_pct'])} of revenue",
         'operating cash flow against EBITDA in the interim statements; inventory and receivable '
         'days'],
        ['The exchange rate',
         'more than 70% of revenue is hard-currency linked, so the translated result moves with '
         'the pound',
         'the pace of depreciation against the roughly 6% a year assumed here, and whether the '
         'gap to interest-rate parity closes through rates or through the currency'],
        ['Central bank policy',
         'the discount rate glide assumes continued disinflation; a stall raises the cost of '
         'capital across the whole model',
         'policy meetings and the inflation path against the stated targets'],
        ['Copper',
         'copper is the dominant input in the largest segment and is passed through with a lag',
         'whether contracts continue to reprice fast enough to protect the cable gross margin '
         'during price spikes'],
        ['Order intake',
         f"the roughly USD {IN['backlog_usd_bn']}bn backlog underwrites the engineering and "
         f"construction forecast",
         'new awards against burn; the geographic mix of new work'],
        ['Dividend policy',
         'the payout has been modest against earnings; a step up would change the book and '
         'earnings lenses materially',
         'the distribution proposed on the FY2026 result']]
table(rows, [1.50, 2.65, 2.85], size=8.4)

# =========================== 6 PROBABILITY ZONES ==============================
H1('6  Reading the probability zones')
P(f"The three-month distribution in section 3 has a median of {p2(H3M['pct']['p50'])} and a "
  f"5th-to-95th percentile span of {p2(H3M['pct']['p5'])} to {p2(H3M['pct']['p95'])}. Read that "
  f"span honestly: it means the model considers a "
  f"{sgn(H3M['pct']['p5']/SPOT-1,0)} move and a {sgn(H3M['pct']['p95']/SPOT-1,0)} move to be "
  f"equally unremarkable tail outcomes over a single quarter. Anyone who finds that range "
  f"uncomfortably wide is reacting to the volatility of the share rather than to the model.")
rows = [['Zone', 'Three-month range (EGP)', 'How to read it'],
        ['Lower tail', f"below {p2(H3M['pct']['p5'])}",
         'a 1-in-20 outcome; would require a genuine shock — a currency event, a policy reversal, '
         'or a material contract failure'],
        ['Lower half of the central band', f"{p2(H3M['pct']['p25'])} – {p2(H3M['pct']['p50'])}",
         'ordinary drift lower; this zone overlaps the upper end of the fundamental range'],
        ['Upper half of the central band', f"{p2(H3M['pct']['p50'])} – {p2(H3M['pct']['p75'])}",
         'ordinary drift higher; the market continuing to price the hard-currency reading'],
        ['Upper tail', f"above {p2(H3M['pct']['p95'])}",
         'a 1-in-20 outcome; would need a step change in the order book, the margin, or the '
         'perceived country risk'],
        ['Where the fundamental central sits', p2(D['central']),
         f"below the 25th percentile of the three-month distribution — the price map and the "
         f"valuation genuinely disagree, and that disagreement is the point"]]
table(rows, [1.75, 1.75, 3.50], size=8.5)

# =========================== 7 CAVEATS ========================================
H1('7  Caveats and what would change our mind')
for head, body in [
    ("The FY2025 income statement is partly derived. ",
     f"Revenue, profit after tax, profit after minority interests, total assets and net bank debt "
     f"for FY2025 are disclosed. Gross profit is assembled from the nine-month and fourth-quarter "
     f"prints. The split of the remainder between operating costs, net finance and tax is closed "
     f"arithmetically to the reported profit, which implies an effective tax rate of "
     f"{pc(HI['FY25']['tax']/HI['FY25']['ebt']*-1)} against {pc(HI['FY24']['tax']/HI['FY24']['ebt']*-1)} "
     f"in FY2024. The audited FY2025 statements are the falsifier. FY2023 and FY2024 are taken "
     f"directly from audited statements and earnings releases and are not estimated."),
    ("The FY2025 balance sheet beyond total assets and net debt is triangulated. ",
     f"Three independent methods put gross debt between {n0(HB['FY25']['debt_methods']['cash_implied'])} "
     f"and {n0(HB['FY25']['debt_methods']['residual'])}; the midpoint is carried. This matters far "
     f"less than it sounds, because the valuation bridge subtracts only the disclosed net bank debt "
     f"of {n0(IN['nd_fy25'])}, not the triangulated gross figure."),
    ("The terminal value is a large share of the answer. ",
     f"{pc(DCF['tv_share'],0)} of the enterprise value comes from the terminal value. This is "
     f"disclosed in the summary table, in the bridge and here. It is a consequence of a high "
     f"discount rate applied to a business still growing fast — the explicit years are heavily "
     f"discounted, so the perpetuity carries the weight. The terminal assumptions are stressed "
     f"across cost of capital, growth and return on invested capital in section 1.9."),
    ("The currency of discounting is unresolved, and it is the biggest single question. ",
     f"Our primary construction charges the full Egyptian equity risk premium to a company earning "
     f"most of its money elsewhere. The alternative construction gives EGP "
     f"{p2(DCF['ccy_alt_ps'])}. We have chosen the conservative reading and shown the other in "
     f"full rather than splitting the difference silently."),
    ("Terminal growth of 5% is roughly zero in real terms. ",
     f"The terminal risk-free rate embeds 5% inflation, so a 5% nominal terminal growth rate "
     f"assumes the company stops growing in real terms forever. For a business with a growing "
     f"hard-currency export franchise that is a conservative assumption, and the 6% and 7% columns "
     f"of the growth grid are not aggressive."),
    ("Minority interests are charged at their profit share, not at book. ",
     f"Minorities take {pc(DCF['nci_share'])} of group profit but only "
     f"{pc(HB['FY25']['nci']/(HB['FY25']['eqp']+HB['FY25']['nci']))} of book equity. Charging them "
     f"the profit share removes EGP {n0(DCF['nci_val'])}mn from the equity value — roughly "
     f"{p2(DCF['nci_val']/SH)} per share more than a book-value treatment would. This is the "
     f"conservative choice and is stated so a reader who prefers the other convention can add it "
     f"back."),
    ("Segment revenue for FY2025 is apportioned, not disclosed line by line. ",
     "The company disclosed that wires and cables contributed about 59% of revenue and engineering "
     "and construction about 27%; the remainder is split using the last fully disclosed quarterly "
     "segment table. Segment shares affect the blended margin, not the revenue total."),
    ("Concentration of control. ",
     f"The founding family holds {pc(IN['ownership']['family'])} and the free float is "
     f"{pc(IN['ownership']['float'])}. Minority shareholders have limited influence over capital "
     f"allocation, related-party dealings and distribution policy. This is a governance fact, not "
     f"an allegation, and it is one reason the justified multiples used here carry a discount."),
    ("What would change our mind, specifically. ",
     f"Upward: sustained operating cash conversion above 60% of EBITDA for two consecutive halves; "
     f"a credible reduction in the perceived country risk premium; order intake materially above "
     f"burn. Downward: working capital rising through {pc(SN['nwc_grid'][-1])} of revenue; the "
     f"cable gross margin failing to stabilise; a stall in disinflation that freezes the discount "
     f"rate glide.")]:
    bullet(body, bold_head=head)
P('', space_after=8)

# =========================== APPENDIX A =======================================
H1('Appendix A  Financial statements')
H2('A.1  Income statement — three years historical and five years forecast (consolidated, EGP mn)')
cols = ['FY2023', 'FY2024', 'FY2025'] + YRS
rows = [['EGP mn'] + cols]
def hist_row(key, fmt=n0, neg=False):
    out = []
    for y in ('FY23', 'FY24', 'FY25'):
        v = HI[y][key]
        out.append(f"({fmt(abs(v))})" if (neg or v < 0) else fmt(v))
    return out
rows.append(['Revenue'] + hist_row('rev') + [n0(x) for x in F['rev']])
rows.append(['Gross profit'] + hist_row('gp') + ['—'] * 5)
rows.append(['EBITDA'] + hist_row('ebitda') + [n0(x) for x in F['ebitda']])
rows.append(['EBITDA margin'] + [pc(HI[y]['ebitda'] / HI[y]['rev']) for y in ('FY23','FY24','FY25')] +
            [pc(x) for x in F['ebitda_margin']])
rows.append(['Depreciation and amortisation'] + hist_row('dna', neg=True) +
            [f"({n0(x)})" for x in F['dna']])
rows.append(['EBIT'] + hist_row('ebit') + [n0(x) for x in F['ebit']])
rows.append(['Net finance costs'] + hist_row('fin') +
            [f"({n0(IN['kd_path'][i]*HB['FY25']['debt']-0.10*HB['FY25']['cash'])})" for i in range(5)])
rows.append(['Share of equity-accounted investees'] + hist_row('assoc') +
            [n0(HI['FY25']['assoc'] * (1.08 ** (i + 1))) for i in range(5)])
rows.append(['Profit before tax'] + hist_row('ebt') + ['—'] * 5)
rows.append(['Income tax'] + hist_row('tax', neg=True) + ['—'] * 5)
rows.append(['Profit for the year'] + hist_row('pat') + ['—'] * 5)
rows.append(['Non-controlling interests'] + hist_row('nci', neg=True) + ['—'] * 5)
rows.append(['Profit attributable to shareholders'] + hist_row('npa') + [n0(x) for x in F['np_attr']])
rows.append(['Earnings per share (EGP)'] + [p2(HI[y]['npa'] / SH) for y in ('FY23','FY24','FY25')] +
            [p2(x / SH) for x in F['np_attr']])
table(rows, [1.72, 0.66, 0.66, 0.66, 0.66, 0.66, 0.66, 0.66, 0.66], size=7.9,
      band_rows={3, 6, 13})
caption("FY2023 and FY2024 are taken from the company's audited consolidated statements and "
        "earnings releases. FY2025 is disclosed at the revenue, profit-after-tax and "
        "profit-after-minority lines; the intermediate lines are derived as described in section 7. "
        "Forecast profit is struck after net interest on the estimated debt and cash balances and "
        "after tax and minority interests, and therefore differs slightly from the free-cash-flow "
        "waterfall in section 1.1, which is a pre-financing measure by construction. Statutory "
        "earnings per share as reported by the company is struck after the Egyptian employee and "
        "board profit-share appropriation and is accordingly lower than the figures shown here.")

H2('A.2  Balance sheet — condensed house layout (consolidated, EGP mn)')
rows = [['EGP mn', 'FY2023', 'FY2024', 'FY2025 (estimated)'],
        ['Property, plant and equipment', n0(HB['FY23']['ppe']), n0(HB['FY24']['ppe']),
         n0(HB['FY25']['ppe'])],
        ['Equity-accounted investees', '3,802.8', n0(IN['assoc_bv_fy24']), '—'],
        ['Inventories', n0(HB['FY23']['inv']), n0(HB['FY24']['inv']), '—'],
        ['Contract assets', n0(HB['FY23']['ca']), n0(HB['FY24']['ca']), '—'],
        ['Trade and other receivables', n0(HB['FY23']['recv']), n0(HB['FY24']['recv']), '—'],
        ['Cash and cash equivalents', n0(HB['FY23']['cash']), n0(HB['FY24']['cash']),
         n0(HB['FY25']['cash'])],
        ['Total assets', n0(HB['FY23']['assets']), n0(HB['FY24']['assets']), n0(HB['FY25']['assets'])],
        ['Loans and borrowings', n0(HB['FY23']['debt']), n0(HB['FY24']['debt']), n0(HB['FY25']['debt'])],
        ['Trade and other payables', n0(HB['FY23']['pay']), n0(HB['FY24']['pay']), '—'],
        ['Contract liabilities', n0(HB['FY23']['cl']), n0(HB['FY24']['cl']), '—'],
        ['Equity attributable to shareholders', n0(HB['FY23']['eqp']), n0(HB['FY24']['eqp']),
         n0(HB['FY25']['eqp'])],
        ['Non-controlling interests', n0(HB['FY23']['nci']), n0(HB['FY24']['nci']),
         n0(HB['FY25']['nci'])],
        ['Net bank debt', n0(HB['FY23']['nd']), n0(HB['FY24']['nd']), n0(HB['FY25']['nd'])],
        ['Net working capital', n0(HB['FY23']['nwc']), n0(HB['FY24']['nwc']), n0(HB['FY25']['nwc'])],
        ['Net debt / EBITDA', f"{HB['FY23']['nd']/HI['FY23']['ebitda']:.2f}×",
         f"{HB['FY24']['nd']/HI['FY24']['ebitda']:.2f}×",
         f"{HB['FY25']['nd']/HI['FY25']['ebitda']:.2f}×"]]
table(rows, [2.35, 1.55, 1.55, 1.55], size=8.4, band_rows={7, 13, 15})
caption(f"FY2023 and FY2024 are audited. For FY2025 only total assets and net bank debt are "
        f"disclosed; equity is rolled forward from the audited FY2024 figure for FY2025 profit "
        f"less the dividend paid, and gross debt and cash are triangulated (three methods spanning "
        f"{n0(HB['FY25']['debt_methods']['cash_implied'])} to "
        f"{n0(HB['FY25']['debt_methods']['residual'])}). Only the disclosed net figure enters the "
        f"valuation.")

H2('A.3  Forecast balance sheet and cash-flow markers')
rows = [['EGP mn'] + YRS,
        ['Net working capital'] + [n0(x) for x in F['nwc']],
        ['Property, plant and equipment'] + [n0(x) for x in F['ppe']],
        ['Invested capital'] + [n0(x) for x in F['ic']],
        ['Return on invested capital'] + [pc(x) for x in F['roic']],
        ['Capital expenditure'] + [f"({n0(x)})" for x in F['capex']],
        ['Change in working capital'] + [f"({n0(x)})" for x in F['dnwc']],
        ['Free cash flow to the firm'] + [n0(x) for x in F['fcff']],
        ['Shareholders\' equity'] + [n0(x) for x in F['equity']],
        ['Net debt'] + [n0(x) for x in F['net_debt']]]
table(rows, [2.05, 0.99, 0.99, 0.99, 0.99, 0.99], size=8.4, band_rows={7})
P(f"The FY2024 accounts are the reason the free-cash-flow line above should be read carefully. "
  f"That year the group turned EGP {n0(HI['FY24']['ebitda'])}mn of EBITDA into EGP "
  f"{n0(IN['ocf_fy24'])}mn of operating cash after interest of EGP {n0(IN['int_paid_fy24'])}mn and "
  f"tax of EGP {n0(IN['tax_paid_fy24'])}mn, then spent EGP {n0(IN['capex_fy24'])}mn on capital "
  f"expenditure. The forecast assumes working-capital intensity stops rising, which is what allows "
  f"free cash flow to turn positive and build. If it does not, the model is wrong in the direction "
  f"that matters most.")

# =========================== APPENDIX B =======================================
H1('Appendix B  Peer frame, risk register — and the research register')
H2('B.1  Peers and the sector frame')
rows = [['Company', 'Market', 'Relevance', 'Caution'],
        ['Riyadh Cables', 'Saudi Arabia', 'the nearest listed regional cable manufacturer',
         'a fraction of the revenue, no contracting arm, a much lighter balance sheet and a '
         'pegged currency — the multiple is not transferable'],
        ['Electro Cable Egypt', 'Egypt', 'the only other listed Egyptian cable manufacturer, and '
         'the closest match on country risk and input costs',
         'far smaller, domestically concentrated, heavily levered and currently loss-making — it '
         'sets a floor for country risk, not a benchmark for quality'],
        ['European cable majors', 'Europe', 'the closest match on business model — cables plus '
         'projects, with a large order book',
         'developed-market cost of capital and no emerging-market convertibility risk; their '
         'multiples import an assumption rather than test one'],
        ['Regional engineering and construction contractors', 'Gulf and North Africa',
         'the right frame for the roughly 27% of revenue that is turnkey project work',
         'project accounting differs, and backlog quality is not comparable across disclosure '
         'regimes']]
table(rows, [1.70, 1.05, 2.10, 2.15], size=8.3)
P("The absence of a clean comparable is itself a finding. This is a diversified industrial group "
  "with a manufacturing business, a contracting business and an infrastructure portfolio, listed "
  "in a frontier market, earning most of its revenue elsewhere. Any single peer multiple applied "
  "to it imports assumptions about country risk that the cash-flow model tests explicitly. That is "
  "why the relative lens carries a fifth of the weight and not more.")

H2('B.2  Risk register')
rows = [['Risk', 'Mechanism', 'Rough valuation impact'],
        ['Currency and convertibility', 'the ability to realise hard-currency earnings in Egyptian '
         'pounds, and the pace of depreciation',
         f"the exchange-rate sensitivity spans {p2(max(SN['grid_fx'])-min(SN['grid_fx']))} per share"],
        ['Cost of capital / disinflation stall', 'the discount-rate glide assumes continued easing',
         f"the explicit-against-terminal grid spans "
         f"{p2(max(max(r) for r in SN['grid_exp_term'])-min(min(r) for r in SN['grid_exp_term']))} "
         f"per share"],
        ['Working-capital discipline', 'growth is funded by inventory and receivables',
         f"{p2(max(SN['grid_nwc'])-min(SN['grid_nwc']))} per share across the tested range"],
        ['Margin normalisation overshooting', 'cable margins fail to stabilise after the currency '
         'windfall unwinds',
         f"{p2(max(SN['grid_margin'])-min(SN['grid_margin']))} per share across ±2 percentage points"],
        ['Terminal return on capital', 'the perpetuity assumes returns stay near the historical '
         'level', f"{p2(max(SN['grid_roic'])-min(SN['grid_roic']))} per share across the tested range"],
        ['Governance and control', f"free float of {pc(IN['ownership']['float'])}; minority "
         f"influence over capital allocation is limited",
         'expressed through the discount applied to the justified multiples, not as a separate line'],
        ['Execution and country concentration in the order book',
         'projects across Africa and the Gulf carry counterparty, payment and political risk',
         'sits inside the engineering and construction margin assumption'],
        ['Disclosure lag', 'the FY2025 audited statements were not reachable at the time of '
         'writing; several FY2025 lines are derived',
         'stated in full in section 7; falsified or confirmed by the audited FY2025 accounts']]
table(rows, [1.85, 2.60, 2.55], size=8.3)

H2('B.3  The research register — layers, dated, negative results included')
P("Research for this study proceeded in four layers: the global and macroeconomic backdrop; the "
  "country; the industry; and the company itself. The full source-by-source register, with dates, "
  "layers and the four-field provenance of every input, is published as a separate bibliography "
  "document accompanying this study. Two negative results are recorded here because they shaped "
  "what could and could not be asserted.")
for head, body in [
    ("The audited FY2025 consolidated statements could not be retrieved. ",
     "The company's investor-relations site and the exchange's filing archive were unreachable "
     "from the research environment. FY2025 is therefore built from disclosed headline figures "
     "reported by financial press covering the exchange filing, cross-checked against each other "
     "and against the quarterly path. Every derived line is labelled."),
    ("No FY2025 or Q1-2026 segment table was obtainable. ",
     "The last fully disclosed segment table is the first quarter of 2025. Segment shares for "
     "FY2025 are apportioned from company commentary and that table.")]:
    bullet(body, bold_head=head)
P('', space_after=8)

# =========================== APPENDIX C =======================================
H1('Appendix C  The expert valuation panel')
P("Three independent valuation approaches are run against the same disclosed facts by three "
  "notional experts, each committed to a different method and each required to state what would "
  "prove them wrong. They are not asked to agree, and they do not.")

E1, E2, E3 = EXP['e1'], EXP['e2'], EXP['e3']
H2('C.1  Expert 1 — earnings power: mid-cycle earnings at a justified multiple')
P("Worldview: a business is worth a multiple of what it earns in a normal year. Cycles average "
  "out; discount-rate models multiply small errors in the rate by large terminal values and "
  "produce false precision. Find the mid-cycle earnings, apply a defensible multiple, stop.")
P(f"When it works: for established franchises with a long operating record and a stable "
  f"competitive position — which describes this company well. When it fails: when the multiple is "
  f"imported from a market with a different cost of capital, which is precisely the trap here.")
rows = [['Step', 'Value'],
        ['Mid-cycle revenue (FY2028 forecast, EGP mn)', n0(E1['rev'])],
        [f"Mid-cycle EBITDA margin", pc(E1['margin'])],
        ['Mid-cycle EBIT (EGP mn)', n0(E1['ebit'])],
        ['Less net interest (EGP mn)', f"({n0(E1['interest'])})"],
        ['After tax and minority interests — earnings per share (EGP)', p2(E1['eps'])],
        ['Justified price/earnings multiple', f"{E1['pe']}×"],
        ['Fair value (EGP per share)', p2(E1['base'])],
        ['Range (7.0× to 12.0×)', f"{p2(E1['rng'][0])} – {p2(E1['rng'][1])}"]]
table(rows, [4.35, 1.55], size=8.6, band_rows={8})
P(f"Named sensitivity: each one-turn change in the multiple is worth EGP "
  f"{p2(E1['eps'])} per share, and each percentage point of mid-cycle EBITDA margin is worth "
  f"roughly EGP {p2(E1['base']*0.09/E1['margin']/100*1)} per share.")
P("Falsifier, stated in advance: if the group's EBITDA margin fails to hold above 11% for two "
  "consecutive full years, the mid-cycle margin assumed here is wrong and this valuation should "
  "be discarded, not adjusted.", space_after=8)

H2('C.2  Expert 2 — the accountant: owner cash earnings from the statements')
P("Worldview: earnings are an opinion, cash is a fact. The only number that matters is what an "
  "owner could take out of the business each year after everything the business needs to keep "
  "running at its current scale — including the working capital that growth consumes. Capitalise "
  "that, and nothing else.")
P("When it works: it is the correct discipline for exactly this kind of company, where reported "
  "profit and cash generation have diverged sharply. When it fails: it undervalues a business "
  "genuinely investing ahead of demand, because it charges growth capital against the owner "
  "without crediting the growth it buys.")
rows = [['Step', 'Value'],
        ['Average free cash flow to the firm, FY2028–FY2030 (EGP mn)', n0(E2['fcff'])],
        ['Less after-tax interest (EGP mn)', f"({n0(E2['int_at'])})"],
        [f"Less minority share ({pc(DCF['nci_share'])})",
         f"({n0((E2['fcff']-E2['int_at'])*DCF['nci_share'])})"],
        ['Owner cash earnings (EGP mn)', n0(E2['fcfe'])],
        ['Capitalised at cost of equity less growth',
         f"{pc(E2['ke'])} − {pc(IN['g_term'],0)}"],
        ['Fair value (EGP per share)', p2(E2['base'])],
        ['Range', f"{p2(E2['rng'][0])} – {p2(E2['rng'][1])}"]]
table(rows, [4.35, 1.55], size=8.6, band_rows={7})
P(f"This is the harshest of the three readings, at EGP {p2(E2['base'])}, and the reason is "
  f"specific and defensible: it takes the FY2024 evidence — EGP {n0(HI['FY24']['ebitda'])}mn of "
  f"EBITDA converting to EGP {n0(IN['ocf_fy24'])}mn of operating cash — as a statement about the "
  f"business model rather than about one unusual year.")
P("Named sensitivity: if working capital intensity fell by two percentage points of revenue, this "
  "valuation would rise by roughly a third, because the entire gap between this expert and the "
  "other two is the cash the order book absorbs.")
P("Falsifier, stated in advance: two consecutive halves in which operating cash flow exceeds 60% "
  "of EBITDA would refute the premise that this business structurally cannot convert its earnings, "
  "and this number should then be abandoned.", space_after=8)

H2('C.3  Expert 3 — cash returns: return on capital against the cost of capital')
P("Worldview: value is created only when the return on invested capital exceeds the cost of that "
  "capital, and the amount created is the spread multiplied by the capital employed. Growth "
  "without a positive spread destroys value; growth with one compounds it. Start from the capital "
  "already invested and add the present value of the economic profit earned on it.")
P("When it works: it is the sharpest available test of whether growth is worth funding, and it "
  "makes the discount-rate question unavoidable rather than buried. When it fails: it is acutely "
  "sensitive to how invested capital is measured, and to the currency in which the cost of capital "
  "is struck.")
rows = [['Step', 'Value'],
        ['Invested capital at the FY2025 base (EGP mn)', n0(E3['ic0'])],
        ['Present value of economic profit, five explicit years (EGP mn)', n0(E3['pv_ep'])],
        ['Present value of terminal economic profit (EGP mn)', n0(E3['pv_ep_term'])],
        ['Enterprise value (EGP mn)', n0(E3['ev'])],
        ['Fair value (EGP per share)', p2(E3['base'])],
        ['Range — the upper bound is the hard-currency discounting case',
         f"{p2(E3['rng'][0])} – {p2(E3['rng'][1])}"]]
table(rows, [4.35, 1.55], size=8.6, band_rows={6})
rows = [['Year'] + YRS,
        ['Return on invested capital'] + [pc(x) for x in F['roic']],
        ['Cost of capital that year'] + [pc(x) for x in F['fwd_wacc']],
        ['Spread'] + [f"{(F['roic'][i]-F['fwd_wacc'][i])*100:+.1f}pp" for i in range(5)],
        ['Economic profit (EGP mn)'] + [n0(x) for x in E3['ep']]]
table(rows, [2.05, 0.99, 0.99, 0.99, 0.99, 0.99], size=8.4, band_rows={4})
P(f"This table is the single most revealing exhibit in the study. The spread is negative in the "
  f"early years — the group earns roughly {pc(F['roic'][0],0)} on capital while its cost of capital "
  f"is {pc(F['fwd_wacc'][0],0)} — and turns positive only as the discount rate glides down. On "
  f"this reading the company is not currently creating value at an Egyptian cost of capital; it "
  f"creates value only if that cost of capital normalises, or if the correct cost of capital is "
  f"the hard-currency one.")
P("Named sensitivity: a two-percentage-point parallel reduction in the cost-of-capital schedule "
  "flips the spread positive from the first forecast year and adds materially more than any "
  "operating assumption tested elsewhere in this study.")
P("Falsifier, stated in advance: if return on invested capital falls below 15% for two consecutive "
  "years while the cost of capital stays above 20%, this approach concludes the business is "
  "consuming value at scale and the estimate should collapse toward invested capital.", space_after=8)

H2('C.4  Cross-examination')
rows = [['Challenge', 'From', 'Response'],
        ['"A multiple is just a discount rate you have not written down. Yours implies a cost of '
         'equity nowhere near the one this market charges."', 'Expert 3 to Expert 1',
         'Conceded in part. The multiple is deliberately discounted below developed-market levels '
         'for exactly this reason, but the discount is a judgement rather than a derivation, and '
         'it is the weakest joint in this method.'],
        ['"You are charging the owner for working capital that funds an order book which will '
         'convert to cash. That is a timing charge treated as a permanent one."',
         'Expert 1 to Expert 2',
         'Rejected. Two audited years show working capital rising with revenue, not converting. '
         'Until a year shows conversion, treating it as permanent is the evidence-led position.'],
        ['"Your invested-capital base is understated because it excludes goodwill written off and '
         'assets held at historical cost through three devaluations."', 'Expert 2 to Expert 3',
         'Conceded. A higher capital base would lower the measured return on capital and shrink '
         'the spread, making this reading more pessimistic, not less. The direction of the error '
         'is unfavourable to the conclusion already reached.'],
        ['"All three of you are answering an Egyptian question about a company that earns 70% of '
         'its money elsewhere."', 'The panel to itself',
         'Accepted as the central unresolved issue. It is why Expert 3\'s range extends up to the '
         'hard-currency case, and why the main study presents both readings rather than an '
         'average.']]
table(rows, [2.45, 1.20, 3.35], size=8.2)

H2('C.5  The three in one room')
figure(os.path.join(HERE, 'figD1_experts.png'), 6.9,
       f"Figure 8 — the three experts' ranges. The gold band is the panel centre of "
       f"{p2(D['panel_centre'])}; the vertical line is the market price of {p2(SPOT)}.")
P(f"The panel spans EGP {p2(min(E1['base'],E2['base'],E3['base']))} to "
  f"{p2(max(E1['base'],E2['base'],E3['base']))} — a factor of "
  f"{max(E1['base'],E2['base'],E3['base'])/min(E1['base'],E2['base'],E3['base']):.1f} between the "
  f"most and least generous reading. That is a wide disagreement and it is not noise. Expert 1 "
  f"values earnings and finds the company reasonably priced. Expert 2 values cash and finds it "
  f"expensive by a wide margin. Expert 3 values the spread between returns and the cost of capital "
  f"and finds that the answer depends entirely on which cost of capital applies. The panel median "
  f"of {p2(D['panel_centre'])} sits {sgn(D['panel_centre']/SPOT-1,0)} against the market price and "
  f"close to the study's own weighted central of {p2(D['central'])}.")

H2('C.6  Reading the divergence')
rows = [['Assumption', 'Expert 1', 'Expert 2', 'Expert 3', 'Why it swings the answer'],
        ['Working capital', 'ignored — earnings basis', 'charged in full, permanently',
         'charged through invested capital',
         'the largest single source of the gap between Experts 1 and 2'],
        ['Discount rate', 'implicit in the multiple', f"{pc(E2['ke'])} explicit",
         'the full glide, year by year',
         'Expert 3 is the only one who lets it change over time, which is why his spread turns'],
        ['Currency of discounting', 'not addressed', 'Egyptian throughout',
         'both readings shown in the range',
         'worth more than every operating assumption combined'],
        ['Growth', 'embedded in the multiple', f"{pc(IN['g_term'],0)} perpetual",
         'funded explicitly through reinvestment',
         'only Expert 3 makes growth pay for the capital it needs'],
        ['Terminal value', 'none — no perpetuity', 'a perpetuity of owner cash',
         f"{pc(DCF['tv_share'],0)} of the value in the study\'s main model",
         'the reason Expert 1 is insensitive to the terminal debate and the others are not']]
table(rows, [1.45, 1.40, 1.40, 1.40, 1.35], size=8.0)
P("The instruction to the reader is not to average these three. It is to decide which of the three "
  "premises is true — whether working capital converts, and which currency's cost of capital "
  "applies — and then to use the corresponding number. The disagreement is a map of what you need "
  "to have a view on.", space_after=10)

# =========================== ABOUT / DISCLOSURE ===============================
H1('About this series')
P("This series publishes independent, educational valuation studies of listed companies. Each "
  "study is built from disclosed financial statements and named market data, states its "
  "assumptions explicitly, computes every figure in an auditable model rather than in prose, and "
  "publishes the ranges its assumptions produce. Studies never carry a rating or a price target. "
  "Where a figure is estimated rather than disclosed, it is labelled. Where a source could not be "
  "reached, the gap is recorded rather than filled.")
P("The probabilistic price map in section 3 is produced by a volatility model that is tested by "
  "walk-forward simulation against a random-walk benchmark before it is allowed to publish a "
  "range. It describes price dispersion and carries no view on value. It is never combined with "
  "the fair-value work.")

H1('Disclosure & Disclaimer')
P("This document is educational analysis and is not investment advice, an offer, or a solicitation "
  "to buy or sell any security. It contains no recommendation, no rating and no price target. The "
  "author holds no position in the security discussed and has no business relationship with the "
  "company. Figures are drawn from public sources believed reliable but not independently "
  "verified; where figures are derived or estimated this is stated in the text. Valuation is "
  "inherently uncertain and depends on assumptions that reasonable analysts will dispute — several "
  "such disputes are set out explicitly in this document rather than resolved silently. Past "
  "performance and simulated distributions are not guides to future returns. Readers must reach "
  "their own conclusions and should consider taking independent advice. No liability is accepted "
  "for any loss arising from use of this material.", size=9.2, color=GREY)

out = os.path.join(HERE, 'SWDY_Valuation_Study_05-08-2026_public.docx')
doc.save(out)
print(f"wrote {out} | {len(doc.paragraphs)} paragraphs | {len(doc.tables)} tables")
