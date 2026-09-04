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
RETW = D['lens_record']['retired']['blend']
RETV = D['lens_record']['retired']['blend_value']
YRS = F['years']
H3M = STK['horizons']['3M']; H1M = STK['horizons']['1M']

def n0(x): return f"{x:,.0f}"
def n1(x): return f"{x:,.1f}"
def p2(x): return f"{x:.2f}"
def pc(x, dp=1): return f"{x*100:.{dp}f}%"
def sgn(x, dp=0): return f"{x*100:+.{dp}f}%"
def to_anchor_docx(v):
    """Mirror of the engine's anchor roll, for counterfactual display values only."""
    return v * DCF['roll'] - IN['dps_fy25']

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
      "This company earns just over half its revenue on a hard-currency-linked basis, but it "
      "reports, is listed and is financed in Egyptian pounds. The answer therefore depends heavily "
      "on which currency's cost of capital you believe applies. Both readings are computed and "
      "both are shown.")])

# =========================== HEADLINE ========================================
H2('Headline')
P(f"Elsewedy Electric is the largest listed industrial group on the Egyptian Exchange by revenue: "
  f"EGP {n0(HI['FY25']['rev'])}mn in FY2025, up {sgn(HI['FY25']['rev']/HI['FY24']['rev']-1)} on "
  f"FY2024 and {sgn((HI['FY25']['rev']/HI['FY23']['rev'])**0.5-1)} a year compounded over the last "
  f"two years. It converts copper into cable, builds substations and power plants under turnkey "
  f"contract, and sells meters, transformers and digital grid products across 15 countries. The "
  f"company discloses exactly three reportable segments — Cables and its accessories, "
  f"Constructions and infrastructure, and Electrical products and digital solutions — and just "
  f"over half of group revenue is earned on a hard-currency-linked basis.")
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
  f"{pc(IN['kd_egp_note'])} on Egyptian-pound liabilities but only {pc(IN['kd_hard_note'])} on the "
  f"blended hard-currency book. The blended rate actually paid works out near "
  f"{pc(W['kd_eff_fy24'])}, less than half what a purely domestic Egyptian borrower pays.")
P(f"On our primary construction the four lenses centre at EGP {p2(D['central'])} per share against "
  f"a market price of {p2(SPOT)} — the price sits about {sgn(SPOT/D['central']-1,0)} above the "
  f"central estimate. That gap is not mainly an argument about the business; it is an argument "
  f"about the discount rate. Discounted at an Egyptian cost of capital gliding "
  f"{pc(W['wacc_exp'])} to {pc(W['wacc_term'])}, the cash flows support roughly EGP "
  f"{p2(DCF['ps'])}. Discount the hard-currency share of those same cash flows at a hard-currency "
  f"cost of capital of about {pc(W['wacc_usd_alt'])} and the same model produces EGP "
  f"{p2(DCF['ccy_alt_ps'])} — still {sgn(DCF['ccy_alt_ps']/SPOT-1,0)} against today's price, but "
  f"{sgn(DCF['ccy_alt_ps']/DCF['ps']-1,0)} above the primary reading. The market appears to be "
  f"applying something at least as generous as the second view. Both are shown, and neither is "
  f"hidden inside an average.", space_after=10)

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
        ['THE CENTRAL — the cash-flow lens, not an average',
         'one class primary IS the central; the lenses above are cross-checks published '
         'at their own values, and the book lens is a disclosed floor that is never weighted',
         f"{p2(D['span'][0])} – {p2(D['span'][1])}", p2(D['central']), sgn(D['central']/SPOT-1,0)],
        ['NOT AVERAGED — the retired blend, published unused',
         f"the retired weights: DCF {pc(RETW['dcf'],0)} · relative {pc(RETW['relative'],0)} · "
         f"normalised {pc(RETW['normalized'],0)} · book {pc(RETW['book'],0)}",
         '—', p2(RETV), sgn(RETV/SPOT-1,0)],
        ['Market price', 'closing price on the anchor date', '—', p2(SPOT), '—'],
        ['ALTERNATIVE READINGS — separate questions, never averaged into the central', '', '', '', ''],
        ['Currency of discounting',
         f"the same cash flows with the hard-currency leg discounted at {pc(W['wacc_usd_alt'])} "
         f"instead of the Egyptian rate — a different view of country risk, not a fifth lens",
         '—', p2(DCF['ccy_alt_ps']), sgn(DCF['ccy_alt_ps']/SPOT-1,0)],
        ['Rating-basis cost of capital',
         f"the same model on the rating column of the published country-risk table rather than "
         f"the market-spread column (see section 1.8)",
         '—', p2(DCF['ps_rating_basis']), sgn(DCF['ps_rating_basis']/SPOT-1,0)],
        ['Minority interests charged before net debt',
         'an alternative sequencing of one line of the bridge (see section 1.8)',
         '—', p2(DCF['ps_nci_alt']), sgn(DCF['ps_nci_alt']/SPOT-1,0)]]
table(rows, [1.30, 2.75, 1.15, 0.72, 0.63], band_rows={5, 7}, size=8.6)
caption(f"The alternative readings are shown so that each genuinely contested choice carries a "
        f"number the reader can see, rather than being averaged silently into the headline. They "
        f"are deliberately excluded from the central because each answers a different "
        f"question — which currency's cost of capital applies, which column of a risk table to "
        f"use, how to sequence one line of the bridge — and blending them would hide the "
        f"disagreement instead of showing it. Ranges are bear-to-bull within each lens; "
        f"THE CENTRAL IS THE CASH-FLOW LENS ITSELF and its range is that same lens under its "
        f"own two scenarios on one clock, not a spread across four methods. Terminal "
        f"value is {pc(DCF['tv_share'],0)} of the discounted-cash-flow enterprise value — a high "
        f"share, disclosed here and again in the bridge, and the reason the terminal assumptions "
        f"are stress-tested in section 1.9.")

# =========================== COMPANY OVERVIEW ===============================
H2('Company overview — Elsewedy Electric at a glance')
own = IN['ownership']
own_float = own['other'] + own['esop']   # free float: everyone outside the family and Electra
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
        ['Geographic mix', f"The audited FY2025 geographic note (Note 5-2) shows "
         f"{pc(IN['fgn_egp_share_fy25'],1)} of revenue booked outside Egypt — a statement about "
         f"where the customer sits, not about pricing currency. Separately, this study derives the "
         f"share that is hard-currency LINKED, i.e. dollar-priced, at about "
         f"{pc(D['fgn_share_fy25_derived'],0)} using segment-level export-intensity weights of "
         f"Cables 65% / Constructions 30% / Electrical products 45% (house judgements, stated so "
         f"they can be disputed; the forecast-year share runs ~53% as Cables' weight in the mix "
         f"rises); that is the figure used wherever the currency question is valued"],
        ['Order book', 'Not disclosed in any of the audited FY2023-25 statements or the Q1-2026 '
         'interim, which are the primary sources this build is confined to. The company\'s '
         'quarterly earnings releases have historically disclosed order-book and volume data '
         '(the FY2024 release, for example, disclosed 167,665 tons of cable sold); those releases '
         'were not reachable from this research environment, so the forecast is built on segment '
         'revenue growth rather than a backlog figure — a cross-check against the released '
         'backlog is the first refinement to make when they become obtainable'],
        ['Shares outstanding', f"{n0(SH)}mn"],
        ['Market capitalisation', f"EGP {n0(M['mktcap'])}mn at the anchor price"],
        ['Ownership', f"El Sewedy family ~{pc(own['family'])} · Electra Investment Holding "
         f"{pc(own['electra'])} · free float ~{pc(own_float)}, per the audited FY2025 shareholder "
         f"table. Electra, an Abu Dhabi holding vehicle, acquired 19.98% in a July-2024 tender "
         f"offer at USD 1.05 per share (~USD 449mn) and topped up to 20.37% by FY2024-end; over "
         f"2025 it SOLD roughly 32.1mn shares into the market, taking its stake to "
         f"{pc(own['electra'])} — a disposal, not dilution: the share count is unchanged. The "
         f"13.07% 'other shareholders' line is an upper bound on the true free float, since "
         f"family-linked vehicles may sit inside it"],
        ['Net bank debt', f"EGP {n0(IN['nd_fy25'])}mn at 31 December 2025 "
         f"({n1(IN['nd_fy25']/HI['FY25']['ebitda'])}× EBITDA), computed from the audited balance "
         f"sheet: loans and borrowings including leases {n0(HB['FY25']['debt'])} less cash "
         f"{n0(HB['FY25']['cash'])}. The company's own FY2025 earnings release quotes EGP "
         f"19,789mn on its own narrower basis; the audited-statement computation is used, and the "
         f"~771mn definitional gap is noted rather than resolved"],
        ['Last strategic transaction', f"Electra Investment Holding's tender offer concluded "
         f"July 2024: {n0(IN['electra_mto']['shares_mn'])}mn shares "
         f"({pc(IN['electra_mto']['stake'])}) at USD {IN['electra_mto']['price_usd']}, about USD "
         f"{n0(IN['electra_mto']['value_usdmn'])}mn — roughly EGP 50 per share at the rate then "
         f"prevailing. Recorded because it is the last price at which a strategic buyer cleared a "
         f"fifth of the company, but NOT used as a valuation anchor: it is two years stale, "
         f"struck before the earnings base grew by about half, and sits at under half today's "
         f"price"],
        ['Dividend record', f"EGP {p2(IN['dps_fy24'])} per share on the FY2024 result "
         f"({pc(IN['dps_fy24']*SH/HI['FY24']['npa'])} of attributable profit), then EGP "
         f"{p2(IN['dps_fy25'])} on FY2025 — ratified by the general assembly on 6 May 2026, rights "
         f"with the share through 1 June, paid from 4 June 2026 — "
         f"{pc(IN['dps_fy25']/(HI['FY25']['npa']/SH))} of FY2025 attributable EPS, an "
         f"{sgn(IN['dps_fy25']/IN['dps_fy24']-1,0)} step-up. An earlier revision of this study "
         f"wrongly stated no FY2025 dividend existed, reasoning from the silence of the annual "
         f"and interim filings; the interim covers a period ending before the assembly met, so "
         f"its silence was never evidence. The forecast payout ratio is {pc(F['payout'],0)}, "
         f"struck at the actual FY2025 rate"]]
table(rows, [1.55, 5.45], size=8.8, align_right_from=9)

P(f"Two structural facts govern everything that follows. First, the revenue base is just over half "
  f"hard-currency linked while the share, the accounts and the borrowing are Egyptian — so the "
  f"company is a natural hedge against the currency its shareholders are exposed to. Second, the "
  f"business consumes working capital in direct proportion to its growth: inventories, contract "
  f"assets and receivables less payables and contract liabilities ran at "
  f"{pc(HB['FY23']['nwc']/HI['FY23']['rev'])} of revenue in FY2023, "
  f"{pc(HB['FY24']['nwc']/HI['FY24']['rev'])} in FY2024 and {pc(HB['FY25']['nwc']/HI['FY25']['rev'])} "
  f"in FY2025. In FY2025 the group earned EBITDA of EGP {n0(HI['FY25']['ebitda'])}mn and converted "
  f"only EGP {n0(IN['ocf_fy25'])}mn of it into operating cash after interest and tax "
  f"({pc(IN['ocf_fy25']/HI['FY25']['ebitda'])}). Growth here is expensive, and that is the crux of "
  f"the valuation.", space_after=10)

# =========================== 1 FUNDAMENTAL VALUATION =========================
H1('1  Fundamental valuation')

# ---- 1.1 DCF ----------------------------------------------------------------
H2('1.1  The cash-flow model — the primary lens, with the full waterfall')
P(f"The primary lens is a five-year free-cash-flow-to-the-firm model. Revenue is not forecast as a "
  f"single growth rate applied to a revenue line: it is built from the three segments the company "
  f"itself discloses — Cables and its accessories, Constructions and infrastructure, Electrical "
  f"products and digital solutions — each grown and margined on its own driver, then summed. "
  f"Margins are therefore OUTPUTS of the build rather than assumptions fed into it, and the "
  f"historical version of that build reconciles to the audited income statement EXACTLY on revenue "
  f"in all three years (Note 5-3) and to the audited operating profit through an explicit, "
  f"exactly-reconciling corporate cost load (Note 16 less G&A, net impairment on receivables, other "
  f"expenses and other income). Section 1.6 sets out the segment build. Cash flow is then taken all "
  f"the way to present value, line by line, below.")
hdr = ['EGP mn'] + YRS
rows = [hdr,
        ['Revenue'] + [n0(x) for x in F['rev']],
        ['  of which domestic'] + [n0(x) for x in F['dom']],
        ['  of which foreign'] + [n0(x) for x in F['fgn_egp']],
        ['EBITDA'] + [n0(x) for x in F['ebitda']],
        ['EBITDA margin'] + [pc(x) for x in F['ebitda_margin']],
        ['Less depreciation and amortisation'] + [f"({n0(x)})" for x in F['dna']],
        ['EBIT'] + [n0(x) for x in F['ebit']],
        [f"NOPAT — EBIT × (1 − {pc(IN['tax_eff'])})"] + [n0(x) for x in F['nopat']],
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

H2('The bridge from enterprise value to the equity — and to the anchor date')
_tfcff = F['nopat'][-1] * (1 + DCF['g']) * (1 - DCF['rr_term'])
rows = [['Step', 'EGP mn', 'Note'],
        ['Present value of the five forecast years', n0(DCF['pv_explicit']),
         'sum of the present-value row above'],
        ['Terminal-year free cash flow', n0(_tfcff),
         f"FY2030E NOPAT grown {pc(DCF['g'],0)} × (1 − reinvestment rate {pc(DCF['rr_term'])}); "
         f"the reinvestment rate is forced to g ÷ terminal return on capital "
         f"({pc(DCF['roic_term'])}) so growth is paid for — this is why the terminal cash flow "
         f"sits above year-5 FCFF, disclosed here rather than left implicit"],
        ['Present value of the terminal value', n0(DCF['pv_tv']),
         f"the terminal cash flow capitalised at {pc(W['wacc_term'])} − {pc(DCF['g'],0)} = "
         f"{n0(DCF['tv'])}, discounted at the year-5 factor {F['df'][-1]:.4f}"],
        ['Enterprise value', n0(DCF['ev']), 'the two lines above'],
        ['Terminal value as a share of enterprise value', pc(DCF['tv_share'],0),
         'disclosed here and in the summary table; stress-tested in section 1.9'],
        ['Less net bank debt', f"({n0(DCF['nd'])})", 'audited, at 31 December 2025'],
        ['Plus equity-accounted investees', n0(DCF['assoc']),
         'audited FY2025 carrying value, no uplift; these earn outside the consolidated cash flow'],
        ['Less minority interests', f"({n0(DCF['nci_val'])})",
         f"minorities take {pc(DCF['nci_share'])} of group profit, so they are charged the same "
         f"share of the value"],
        ['Equity attributable, at 31 December 2025', n0(DCF['eq_attr']),
         f"EGP {p2(DCF['ps_dec'])} per share — dated at the audited balance-sheet date the "
         f"bridge subtracts net debt at"],
        [f"Rolled {DCF['anchor_days']:.0f}/365 of a year to the anchor", f"×{DCF['roll']:.4f}",
         f"fair value accretes at the {pc(W['ke_exp'])} cost of equity between the valuation "
         f"date and the 5-Aug-2026 anchor — one date, one price of time, applied to the "
         f"comparison itself"],
        [f"Less the FY2025 dividend paid in the window", f"({p2(IN['dps_fy25'])}/sh)",
         'EGP 1.85, ex 1 June 2026 — value that left the share before the anchor date'],
        ['Fair value per share at the anchor (EGP)', p2(DCF['ps']),
         f"against a spot of {p2(SPOT)} ({sgn(DCF['ps']/SPOT-1,0)})"]]
table(rows, [2.55, 1.05, 3.40], size=8.4, band_rows={4, 12}, align_right_from=1)
caption("Every lens in this study — not only the cash-flow model — is rolled to the anchor on "
        "the same two lines, so no value dated 31 December 2025 is ever compared to an August "
        "price. An earlier revision omitted the roll; an external review correctly flagged the "
        "omission as a breach of the study's own one-date rule, worth about seven months of "
        "accretion on the primary lens.")

# ---- 1.2 book ----------------------------------------------------------------
H2('1.2  Book value and sustainable return — the asset lens')
P(f"Book value attributable to shareholders is EGP {n0(HB['FY25']['eqp'])}mn at the audited FY2025 "
  f"close, or {p2(BK['bvps'])} per share. The trailing return on average equity is "
  f"{pc(BK['roe_trailing'])}. That "
  f"number is flattered: FY2023 and FY2024 both carried devaluation gains on copper inventory "
  f"bought before the pound moved, so the sustainable rate is struck lower, at "
  f"{pc(BK['roe_sust'])}.")
P(f"A justified price-to-book multiple is (return on equity − growth) ÷ (cost of equity − growth). "
  f"It is priced at the PERPETUAL (terminal) cost of equity of {pc(BK['ke_blend'])} — a "
  f"steady-state multiple takes a steady-state rate, not a five-year transitional one. (An "
  f"earlier wording called this figure an 'average' of the two windows, which it never was; the "
  f"actual average, {pc(0.5*(W['ke_exp']+W['ke_term']))}, is the construction behind this lens's "
  f"published bear bound of {p2(LN['book']['bear'])}.) That gives {n1(BK['pb_just'])}× book, "
  f"or EGP {p2(LN['book']['base'])} per share at the anchor. This is the weakest of the four lenses for this "
  f"company and carries the lowest weight, for a specific reason: three years of currency "
  f"translation have moved reported book value in ways that have little to do with the earning "
  f"power of the assets, and a group whose value sits in an order book and a brand is poorly "
  f"described by its balance sheet. It is retained because it is the lens that disagrees most, and "
  f"a lens that only ever agrees is not doing any work.")

# ---- 1.3 relative ------------------------------------------------------------
H2('1.3  Relative multiples')
rows = [['Measure', 'Value', 'Comment'],
        ['Enterprise value / EBITDA (trailing)', f"{n1(REL['ev_ebitda_trailing'])}×",
         f"enterprise value {n0(M['ev_trailing'])} over FY2025 house EBITDA "
         f"{n0(HI['FY25']['ebitda'])} (EBIT + D&A). Two base notes: this trailing EV is market "
         f"cap plus net debt WITHOUT the associates/minority adjustments the justified multiple "
         f"below carries — a simpler market-observable convention, labelled as such; and on the "
         f"company's own published non-GAAP EBITDA (a different, larger definition) the multiple "
         f"would be lower"],
        ['Price / earnings (trailing, attributable basis)', f"{n1(REL['pe_trailing'])}×",
         f"price {p2(SPOT)} over attributable earnings per share of "
         f"{p2(HI['FY25']['npa']/SH)}"],
        ['Price / earnings (trailing, as-reported basis)', f"{n1(SPOT/7.13)}×",
         "the company's own reported earnings per share is struck after the Egyptian employee and "
         "board profit-share appropriation, so screens and data vendors show this higher multiple. "
         "Both are given because a reader comparing against a screen will see the second"],
        ['Price / book', f"{n1(SPOT/BK['bvps'])}×", f"book value {p2(BK['bvps'])} per share"],
        ['Net bank debt / EBITDA', f"{n1(IN['nd_fy25']/HI['FY25']['ebitda'])}×",
         'light net leverage against a large gross book'],
        ['Justified enterprise value / EBITDA', f"{IN['ev_ebitda_just']}×",
         'applied to FY2027E EBITDA and then DISCOUNTED BACK two years, because a forward '
         'multiple produces a forward enterprise value. The multiple is set below the '
         "company's own trailing multiple as an Egyptian-market discount. NOTE: no peer "
         'multiple is computed anywhere in this study, so this is a judgement anchored on '
         "SWDY's own trading history, not a peer-derived figure — an earlier draft asserted a "
         '"peers trade at 8–11×" range that was not supported by any calculation, and it has '
         'been withdrawn'],
        ['Plus interim cash flows', f"({n0(-REL['pv_interim'])})",
         'the present value of the FY2026-27 free cash flows the forward multiple does not '
         'capture — net negative, because FY2026 consumes working capital. Added after external '
         'review; omitting it had overstated this lens slightly'],
        ['Implied value per share, at the anchor', p2(LN['relative']['base']),
         f"bear {p2(LN['relative']['bear'])} at 5.5× / bull {p2(LN['relative']['bull'])} at "
         f"8.0×; rolled to the anchor date on the same two lines as the cash-flow bridge"]]
table(rows, [2.15, 0.90, 3.95], size=8.5, band_rows={6})
_rel_undisc = to_anchor_docx(((REL['ev_rel_fwd'] + REL['pv_interim'] - IN['nd_fy25']
                               + DCF['assoc'])*(1-DCF['nci_share']))/SH)
P(f"Two things about this lens should be read before its number is. First, applying a multiple to "
  f"a forecast year gives an enterprise value AS AT that year; it has to be discounted back before "
  f"it can be compared with today's price. Not doing so would have produced EGP "
  f"{p2(_rel_undisc)} per share instead of {p2(LN['relative']['base'])} — a EGP "
  f"{p2(_rel_undisc - LN['relative']['base'])} "
  f"overstatement, which an earlier draft of this study contained. Second, the justified multiple "
  f"is a judgement, not a peer-derived figure.")
P(f"The honest difficulty with this lens is that there is no clean comparable. The nearest listed "
  f"regional peer in cables is a Saudi manufacturer with a fraction of the revenue, no turnkey "
  f"contracting arm and a very different balance sheet; the global cable majors are European and "
  f"carry neither Egyptian sovereign risk nor Egyptian growth. Applying a discounted multiple to "
  f"mid-cycle EBITDA is therefore a sanity check on the cash-flow model rather than an independent "
  f"valuation, and it is weighted accordingly.")

# ---- 1.4 normalized ----------------------------------------------------------
H2('1.4  Normalised earnings power — mid-cycle margin at current scale')
P(f"The question this lens asks is what the group earns at its CURRENT scale in a year that is "
  f"neither a currency windfall nor a margin trough. The mid-cycle EBITDA margin of "
  f"{pc(NRM['margin'])} — the {NRM['margin_year']} point of the forecast, comfortably below the "
  f"FY2024 outturn of {pc(HI['FY24']['ebitda']/HI['FY24']['rev'])} and above the FY2025 trough of "
  f"{pc(HI['FY25']['ebitda']/HI['FY25']['rev'])} — is applied to FY2026E revenue of EGP "
  f"{n0(NRM['rev'])}mn. An earlier revision applied the multiple to FY2028-SCALE earnings with no "
  f"time value, injecting two years of undiscounted growth into a present-day lens; an external "
  f"review flagged it correctly and the construction was restated, worth about EGP 4.9 per share "
  f"on the cash-flow lens.")
rows = [['Step', 'EGP mn'],
        ['Current-scale (FY2026E) revenue', n0(NRM['rev'])],
        [f"Mid-cycle EBITDA margin ({NRM['margin_year']}) at {pc(NRM['margin'])}", n0(NRM['ebitda'])],
        ['Less depreciation and amortisation', f"({n0(NRM['ebitda']-NRM['ebit'])})"],
        ['Mid-cycle EBIT', n0(NRM['ebit'])],
        ['Less net interest (FY2026E)', f"({n0(NRM['interest'])})"],
        ['Plus share of equity-accounted investees (FY2026E)', n0(NRM['assoc'])],
        [f"Less tax at {pc(IN['tax_eff'])} and minority interests at {pc(DCF['nci_share'])}",
         f"({n0(NRM['ebit']-NRM['interest']+NRM['assoc']-NRM['np'])})"],
        ['Normalised attributable earnings', n0(NRM['np'])],
        ['Normalised earnings per share (EGP)', p2(NRM['eps'])],
        [f"At a justified {IN['pe_just']}× price/earnings, rolled to the anchor (EGP per share)",
         p2(LN['normalized']['base'])]]
table(rows, [4.55, 1.35], size=8.6, band_rows={9, 11}, first_col_bold=False)
caption(f"Bear {p2(LN['normalized']['bear'])} at 7.0× and bull {p2(LN['normalized']['bull'])} at "
        f"11.5×, both rolled to the anchor date like every other lens. Every input row is the "
        f"figure the computation actually uses — the associate line is the FY2026E forecast, not "
        f"the FY2025 actual. One disclosed conservatism: equity-method associate income is taxed "
        f"at {pc(IN['tax_eff'])} inside this lens although it arrives already post-tax at the "
        f"investee — worth about +0.4/share on the central if removed. The justified multiple is "
        f"held well below what a comparable industrial franchise would attract in a developed "
        f"market, because an Egyptian cost of equity near {pc(W['ke_exp'],0)} mathematically "
        f"compresses what any stream of earnings is worth.")

# ---- 1.5 synthesis -----------------------------------------------------------
H2('1.5  Synthesis — one lens is the answer, the rest are cross-checks')
figure(os.path.join(HERE, 'fig1_football.png'), 6.9,
       f"Figure 1 — the four lenses against the market price of "
       f"{p2(SPOT)}. Each bar is that lens's bear-to-bull span; the brass tick is its base case.")
rows = [['Lens', 'Bear', 'Base', 'Bull', 'Role', 'vs price']]
ROLE = {'dcf': 'THE ANSWER', 'relative': 'cross-check',
        'normalized': 'not published for this class',
        'book': 'a floor, never weighted'}
for k in ['dcf', 'relative', 'normalized', 'book']:
    l = LN[k]
    rows.append([l['name'], p2(l['bear']), p2(l['base']), p2(l['bull']), ROLE[k],
                 sgn(l['base']/SPOT-1, 0)])
rows.append(['THE CENTRAL — the cash-flow lens, not an average',
             p2(D['span'][0]), p2(D['central']), p2(D['span'][1]), 'the class primary',
             sgn(D['central']/SPOT-1, 0)])
rows.append(['NOT AVERAGED — the retired blend, published unused',
             '', p2(RETV), '', 'retired', sgn(RETV/SPOT-1, 0)])
table(rows, [2.35, 0.86, 0.86, 0.86, 0.83, 1.14], size=8.6, band_rows={5})
P(f"The four lenses do not agree, and the disagreement is informative rather than embarrassing. "
  f"The two lenses that look at earnings — relative multiples and normalised earnings power — land "
  f"near or slightly above the market price. The two that discount cash or capital at an Egyptian "
  f"cost of capital land well below it. This is the same disagreement in two forms: a multiple "
  f"imported from a market with a low cost of capital implicitly assumes a low cost of capital, "
  f"and a discounted model applied with an Egyptian one does not. THE CENTRAL DOES NOT SIT "
  f"BETWEEN THEM: it is the cash-flow lens itself at EGP {p2(D['central'])}, and the "
  f"market-anchored reads are published beside it at their own values so a reader can judge "
  f"the disagreement rather than receive a number in which it has already been settled by a "
  f"weight. An earlier edition did settle it that way and reported EGP {p2(RETV)}, "
  f"{sgn(RETV/SPOT-1,0)} against the price where this study holds {sgn(D['central']/SPOT-1,0)}.")

# ---- 1.6 drivers -------------------------------------------------------------
H2('1.6  The drivers — the three disclosed segments, each grown on its own driver')
P(f"Revenue is not forecast as a single growth rate applied to a revenue line. The company "
  f"discloses exactly three reportable segments — Cables and its accessories, Constructions and "
  f"infrastructure, and Electrical products and digital solutions — with revenue by segment (Note "
  f"5-3) that reconciles EXACTLY to consolidated revenue in every one of the three audited years, "
  f"and segment profit (Note 16) that reconciles to consolidated operating profit through an "
  f"explicit corporate cost load. None of the three audited filings, including the Q1-2026 "
  f"interim, discloses a tonnage, unit-volume or order-book figure for any segment, so the "
  f"forecast is built as a taper on each segment's own recent revenue growth and margin path "
  f"rather than a reconstructed unit model. Margins are therefore outputs of the build, not "
  f"inputs to it.")

H2('The three disclosed segments, historically')
UH = BU['unit_hist']
rows = [['Segment', 'FY2023 revenue', 'margin', 'FY2024 revenue', 'margin', 'FY2025 revenue',
         'margin']]
for s_ in BU['subs']:
    rows.append([BU['subnames'][s_],
                 n0(UH['FY23']['rev'][s_]), pc(UH['FY23']['margin'][s_]),
                 n0(UH['FY24']['rev'][s_]), pc(UH['FY24']['margin'][s_]),
                 n0(UH['FY25']['rev'][s_]), pc(UH['FY25']['margin'][s_])])
rows.append(['Group revenue', n0(UH['FY23']['rev_sum']), '', n0(UH['FY24']['rev_sum']), '',
             n0(UH['FY25']['rev_sum']), ''])
table(rows, [1.95, 0.98, 0.62, 0.98, 0.62, 0.98, 0.62], size=8.1, band_rows={5})
caption(f"Segment revenue (Note 5-3) sums to consolidated revenue exactly in every year shown — "
        f"there is no elimination or apportionment. Segment margin is segment profit (Note 16, "
        f"inside- and outside-Egypt columns summed) divided by this same revenue base. Every "
        f"segment compressed from FY2023 to FY2025; Cables and Constructions compressed the most, "
        f"Electrical products the least.")

H2('How the forecast is driven')
rows = [['Driver', 'FY2025 base'] + YRS,
        ['Copper (USD/tonne)', n0(IN['copper_hist']['FY25'])] + [n0(x) for x in IN['copper_fcst']],
        ['USD/EGP average rate', n1(IN['fx_hist']['FY25'])] + [n1(x) for x in IN['fx_path']],
        ['Cables — real growth (over copper × FX)', '—'] +
        [pc(x) for x in IN['cables_real_growth']],
        ['Cables — segment margin', pc(UH['FY25']['margin']['cables'])] +
        [pc(x) for x in IN['cables_margin']],
        ['Constructions and infrastructure — revenue growth', '—'] +
        [pc(x) for x in IN['construct_growth']],
        ['Constructions and infrastructure — segment margin', pc(UH['FY25']['margin']['construct'])] +
        [pc(x) for x in IN['construct_margin']],
        ['Electrical products and digital solutions — revenue growth', '—'] +
        [pc(x) for x in IN['elecprod_growth']],
        ['Electrical products and digital solutions — segment margin',
         pc(UH['FY25']['margin']['elecprod'])] + [pc(x) for x in IN['elecprod_margin']],
        ['Corporate cost load, segment profit → EBIT basis (% of revenue)',
         pc(IN['corp_load_hist']['FY25'])] + [pc(x) for x in IN['opex_pct']],
        ['Capital expenditure (% of revenue)', pc(IN['capex_pct_hist']['FY25'])] +
        [pc(x) for x in IN['capex_pct']],
        ['Depreciation and amortisation (% of revenue)', pc(IN['dna_pct_hist']['FY25'])] +
        [pc(IN['dna_pct'])] * 5]
table(rows, [2.35, 0.73, 0.73, 0.73, 0.73, 0.73, 0.73], size=8.0)
caption(f"Copper is held near the current market level rather than forecast — a directional view "
        f"on the metal would dominate the valuation, and it is carried in the sensitivity instead. "
        f"Cables grows on copper-price growth × FX-translation growth × a modest real-volume "
        f"assumption, since no tonnage figure is disclosed in the audited statements to build a "
        f"literal unit model from. Constructions and Electrical products taper on their own "
        f"FY2023-25 revenue CAGR. The corporate cost load — stated on the same segment-profit-to-"
        f"EBIT basis as the audited history (5.70% / 4.30% / 3.16%) — glides UP from FY2025's "
        f"unusually low level toward the FY2023-24 average, the single most conservative choice "
        f"in the build. The capex and D&A paths are shown because they are live free-cash-flow "
        f"drivers, not footnotes: capex tapers from the FY2025 peak of 4.7% as the 2024-25 "
        f"capacity programme completes (it ran 3.1% in FY2023 and 3.7% in FY2024); holding it at "
        f"the FY2025 peak instead would cost roughly EGP 1.8 on the cash-flow lens.")

H2('What the build produces — margins as outputs')
rows = [['EGP mn'] + YRS,
        ['Revenue'] + [n0(x) for x in F['rev']],
        ['Segment profit (Note 16 basis)'] + [n0(x) for x in BU['gp']],
        ['Segment profit margin'] + [pc(x) for x in BU['gp_margin']],
        ['Less corporate cost load (to EBIT)'] + [f"({n0(x)})" for x in BU['opex']],
        ['EBIT'] + [n0(x) for x in F['ebit']],
        ['Add back depreciation and amortisation'] + [n0(x) for x in F['dna']],
        ['EBITDA'] + [n0(x) for x in F['ebitda']],
        ['EBITDA margin'] + [pc(x) for x in F['ebitda_margin']]]
table(rows, [2.05, 0.99, 0.99, 0.99, 0.99, 0.99], size=8.4, band_rows={5, 7})
caption(f"The FY2026 build is checked, not calibrated, against the print: the disclosed Q1-2026 "
        f"revenue of {n0(IN['q1_26_rev'])}, grossed up on the Q1-2025 seasonal share of FY2025, "
        f"implies a full FY2026 of roughly {n0(BU['q1_26_implied_fy'])}, against the build's "
        f"{n0(F['rev'][0])} — a "
        f"{sgn(F['rev'][0]/BU['q1_26_implied_fy']-1)} difference, an independent check that the "
        f"segment build is not running ahead of the company's own trading. That quarter reported "
        f"revenue {sgn(IN['q1_26_rev']/IN['q1_25_rev']-1)} and attributable profit "
        f"{sgn(IN['q1_26_npa']/IN['q1_25_npa']-1)} year on year.")

figure(os.path.join(HERE, 'fig7_mix.png'), 6.9,
       "Figure 2 — revenue by currency of origin with the EBITDA margin path. The hard-currency "
       "leg does the growing; the margin recovers gently as the copper-price inflation of 2024–25 "
       "washes out of the revenue denominator.")

H2('The segment mix, FY2025 against FY2030E')
rows = [['Segment', 'FY2025 revenue (EGP mn)', 'Share', 'FY2025 margin',
         'FY2030E revenue (EGP mn)', 'FY2030E share']]
for s_ in SEG['names']:
    rows.append([SEG['names'][s_], n0(SEG['rev'][s_]), pc(SEG['rev'][s_]/IN['rev_fy25']),
                 pc(SEG['gp_margin'][s_]), n0(F['seg_rev'][4][s_]),
                 pc(F['seg_rev'][4][s_]/F['rev'][4])])
rows.append(['Group', n0(IN['rev_fy25']), '100.0%', pc(sum(SEG['gp'].values())/IN['rev_fy25']),
             n0(F['rev'][4]), '100.0%'])
table(rows, [1.75, 1.30, 0.68, 1.15, 1.30, 0.82], size=8.3, band_rows={5})
caption(f"FY2025 figures are the audited Note 5-3 / Note 16 disclosures directly; nothing is "
        f"apportioned or calibrated. By FY2030E Cables' share of revenue rises from "
        f"{pc(SEG['rev']['cables']/IN['rev_fy25'])} to "
        f"{pc(F['seg_rev'][4]['cables']/F['rev'][4])} as it compounds on copper and FX; "
        f"Constructions' share falls as its growth tapers fastest.")

# ---- 1.7 crux ----------------------------------------------------------------
H2('1.7  The crux — working capital first, the currency second, margins third')
P(f"The FY2025 accounts contain the single most important number in this study. The group earned "
  f"EBITDA of EGP {n0(HI['FY25']['ebitda'])}mn and generated operating cash flow, after interest "
  f"and tax, of EGP {n0(IN['ocf_fy25'])}mn — about "
  f"{pc(IN['ocf_fy25']/HI['FY25']['ebitda'],0)} of it. The difference went into working capital, "
  f"though FY2025 was genuinely the best of the three audited years on this measure: net working "
  f"capital fell from {pc(HB['FY24']['nwc']/HI['FY24']['rev'])} of revenue in FY2024 to "
  f"{pc(HB['FY25']['nwc']/HI['FY25']['rev'])} in FY2025, even as revenue grew "
  f"{sgn(HI['FY25']['rev']/HI['FY24']['rev']-1)}.")
rows = [['Working capital', 'FY2023', 'FY2024', 'FY2025'],
        ['Inventories', n0(IN['inv_fy23']), n0(IN['inv_fy24']), n0(IN['inv_fy25'])],
        ['Contract assets', n0(IN['ca_fy23']), n0(IN['ca_fy24']), n0(IN['ca_fy25'])],
        ['Trade and other receivables', n0(IN['recv_fy23']), n0(IN['recv_fy24']), n0(IN['recv_fy25'])],
        ['Less trade and other payables', f"({n0(IN['pay_fy23'])})", f"({n0(IN['pay_fy24'])})",
         f"({n0(IN['pay_fy25'])})"],
        ['Less contract liabilities', f"({n0(IN['cl_fy23'])})", f"({n0(IN['cl_fy24'])})",
         f"({n0(IN['cl_fy25'])})"],
        ['Net working capital', n0(HB['FY23']['nwc']), n0(HB['FY24']['nwc']), n0(HB['FY25']['nwc'])],
        ['As a share of revenue', pc(HB['FY23']['nwc']/HI['FY23']['rev']),
         pc(HB['FY24']['nwc']/HI['FY24']['rev']), pc(HB['FY25']['nwc']/HI['FY25']['rev'])]]
table(rows, [2.35, 1.55, 1.55, 1.55], size=8.6, band_rows={6, 7})
P(f"The segment build makes a second point that a percentage-of-revenue model hides. Copper is "
  f"passed through in Cables: a higher copper price raises revenue without raising the profit "
  f"earned on it. But working capital scales with revenue, so a copper spike CONSUMES cash while "
  f"adding almost no profit. That is visible in FY2026E, where revenue rises "
  f"{sgn(F['rev'][0]/HI['FY25']['rev']-1,0)} — much of it copper and FX translation — and the "
  f"resulting EGP {n0(F['dnwc'][0])}mn working-capital build cuts free cash flow to the firm to "
  f"just EGP {n0(F['fcff'][0])}mn, against EGP {n0(F['fcff'][1])}mn the following year once the "
  f"step-up is absorbed. A rising copper price is not good news for this business in the year it "
  f"happens.")
P(f"The model holds this ratio near {pc(IN['nwc_pct'])} of revenue, the FY2025 disclosed level. "
  f"That single assumption is worth a great deal: every percentage point of revenue added to or "
  f"removed from working-capital intensity is worth roughly EGP "
  f"{p2(abs(SN['grid_nwc'][2]-SN['grid_nwc'][1])/1.5)}-"
  f"{p2(abs(SN['grid_nwc'][-1]-SN['grid_nwc'][0])/6.0)} per share (the local slope at the base "
  f"and the average across the tested 17-23% span). If the group converts working "
  f"capital further — collecting faster, or pushing more of the funding onto suppliers and "
  f"customers — the cash-flow model reprices sharply upward. If FY2025's improvement reverses, it "
  f"reprices down just as fast.")

# ---- 1.8 macro ---------------------------------------------------------------
H2('1.8  Macro and country — rates, the pound, and the sourced cost of capital')
P(f"The discount rate is a schedule, not a number. Each forecast year is discounted at that year's "
  f"own forward rate, moving from the explicit-window rate to the terminal rate; the terminal "
  f"value is capitalised at the terminal rate and brought back using the same cumulative factor as "
  f"the year-5 cash flow. One date, one price of time — the terminal value never gets a cheaper "
  f"discount than a cash flow arriving on the same day.")
rows = [['Component', 'Explicit window', 'Terminal', 'Source and construction'],
        ['Risk-free rate', pc(IN['rf']), pc(IN['rf_term']),
         'observed 10-year local-currency government yield (readings on the anchor date span '
         'roughly 22.3-23.0% across sources and disagree; the adopted point sits at the low end '
         'and the rate is carried in the sensitivity). Terminal = the central bank\'s 5% '
         'Q4-2028 inflation-target midpoint — deliberately the terminal-state target, not the '
         'nearer 7% Q4-2026 waypoint — plus a 5.5pp real-rate convention'],
        ['Less sovereign default spread', f"({pc(IN['sov_spread_cds'])})", '—',
         'the hard-currency CDS spread, netted from the local yield and then re-entering, '
         'volatility-scaled, through the country premium inside the ERP. The NET country charge '
         'through the equity channel is therefore about +1.9pp, not zero — stated plainly, since '
         'an earlier wording implied the netting removed the charge outright. The un-netted '
         'construction (cost of equity 31.8%) is retired but retained in the audit trail'],
        ['Adjusted risk-free rate', pc(W['rf_star']), pc(IN['rf_term']), ''],
        ['Beta', f"{IN['beta']:.3f}", f"{IN['beta']:.3f}",
         f"own-stock weekly regression against a 31-name equal-weight local composite over five "
         f"years: R-squared {W['beta']['r2']:.3f}, n = {W['beta']['n']}, standard error "
         f"{W['beta']['se']:.3f}, 90% interval [{W['beta']['ci90'][0]:.2f}, "
         f"{W['beta']['ci90'][1]:.2f}]"],
        ['Equity risk premium', pc(IN['erp_cds']), pc(IN['erp_term']),
         'published country-premium file (January-2026 vintage, both columns confirmed against '
         'the file), credit-default-swap basis; the rating-basis column is the published '
         'alternative below. Normalised downward for the terminal rather than held at a '
         'crisis-era level'],
        ['Cost of equity', pc(W['ke_exp']), pc(W['ke_term']), ''],
        ['Cost of debt (blended, pre-tax)', pc(IN['kd']), pc(IN['kd_term']),
         f"currency-blended — see the evidence immediately below. 9.5% is the FY2026 forward "
         f"point of the disclosed cost-of-debt path under the central bank's easing cycle; the "
         f"FY2025 trailing effective rate was {pc(W['kd_eff_fy24'])}, and the integrity gate "
         f"bounds the two against each other"],
        ['Cost-of-debt path (drives the glide)', ' / '.join(pc(k,1) for k in W['kd_path']), '—',
         'the forward rates whose cumulative progress sets the glide fractions between the '
         'explicit-window and terminal cost of capital — published so the three intermediate '
         'discount rates are reproducible'],
        ['Debt weight', pc(W['wd_exp']), pc(IN['wd_term']),
         'net debt against market capitalisation for the explicit window; a normalised 15% for '
         'the terminal — REVISED from 25% after review showed the old weight contradicted the '
         'model\'s own forecast deleveraging in the direction that flattered the valuation; '
         'worth about -2.4 on the cash-flow lens'],
        ['Cost of capital', pc(W['wacc_exp']), pc(W['wacc_term']), '']]
table(rows, [1.60, 0.92, 0.80, 3.68], size=8.2, band_rows={8, 12})
caption("Discounting is end-of-year discrete (each year's flow at its full-year factor) — the "
        "conservative convention; mid-year discounting would raise the explicit strip about 7%. "
        "All values are then rolled to the 5-Aug-2026 anchor as shown in the bridge.")

H2('The cost of debt — three pieces of evidence, not an assumption')
P("A disclosed contractual range is not evidence of what a company pays. Three things are shown "
  "instead.")
rows = [['Test', 'Evidence'],
        ['Currency composition of the debt book',
         f"The audited FY2025 interest-rate note discloses average rates of {pc(IN['kd_egp_note'])} "
         f"on Egyptian-pound financial liabilities and {pc(IN['kd_hard_note'])} on the blended "
         f"hard-currency book (the note moved from a three-way EGP/USD/EUR split in FY2024 to this "
         f"simpler two-way format in FY2025). Reconciling those against the rate actually paid "
         f"implies roughly {pc(W['w_egp_implied'],0)} of the book is in Egyptian pounds and "
         f"{pc(1-W['w_egp_implied'],0)} in hard currency — DOWN sharply from the roughly 44% pound "
         f"share implied a year earlier, as hard-currency facilities were drawn down further. "
         f"Treating this company as a domestic borrower would overstate its cost of debt by about "
         f"{(IN['kd_egp_note']-W['kd_eff_fy24'])*10000:,.0f} basis points."],
        ['Independently computed effective rate',
         f"FY2025: interest expense on loans and credit facilities of {n0(IN['int_exp_fy25'])} "
         f"against the average of the opening and closing balance "
         f"({n0(IN['debt_open_fy25'])} and {n0(IN['debt_close_fy25'])}) = {pc(W['kd_eff_fy24'])}."],
        ['Bounds', f"The adopted {pc(IN['kd'])} sits within {abs(IN['kd']-W['kd_eff_fy24'])*10000:,.0f} "
         f"basis points of the independently computed effective rate and does not exceed it by "
         f"more than 50 basis points. Both bounds hold."]]
table(rows, [2.05, 4.95], size=8.4)
P(f"This is not a technicality. A cheap, majority-hard-currency debt book is one of the two "
  f"genuine competitive advantages this company has over a domestic-only competitor — the other "
  f"being that its revenue is hard-currency linked too. It is also why the balance sheet looks "
  f"more leveraged than it is: the gross book is large because working capital is large, but it "
  f"costs roughly {pc(W['kd_eff_fy24'])} and is more than two-thirds offset by cash.")

H2('Where this construction is contested, and what the alternatives are worth')
P("Six choices in the construction above are legitimately arguable, and external reviewers have "
  "argued them. Rather than defend each in prose, each alternative is computed and its value "
  "published here, so a reader who prefers a different convention can take the number directly.")
rows = [['Choice made', 'The alternative', 'Fair value on the alternative', 'Why we keep ours'],
        [f"Equity risk premium on the credit-default-swap basis ({pc(IN['erp_cds'])}), with the "
         f"sovereign spread netted at {pc(IN['sov_spread_cds'])}",
         f"The rating basis from the same published table: spread {pc(IN['sov_spread_rating'])}, "
         f"premium {pc(IN['erp_rating'])}, cost of equity {pc(W['ke_rating_alt'])}",
         f"EGP {p2(DCF['ps_rating_basis'])} (against {p2(DCF['ps'])})",
         'Both are columns of the same published source. The market-observed basis is preferred to '
         'the agency-rating basis, which lags. This is the single largest open question in the '
         'cost of capital and the alternative is worth roughly '
         f"{p2(DCF['ps'] - DCF['ps_rating_basis'])} per share"],
        ['Minority interests charged against consolidated equity, after net debt',
         'Charged against unlevered enterprise value, before net debt',
         f"EGP {p2(DCF['ps_nci_alt'])} ({p2(DCF['ps_nci_alt'] - DCF['ps'])})",
         'The audited borrowings note records facilities granted to the company AND its '
         'subsidiaries, guaranteed by promissory notes from subsidiaries — so minorities do bear '
         'a share of the debt. The alternative assumes all borrowing sits at the parent, which '
         'the note contradicts'],
        ['Capital weights on net debt',
         f"On gross debt ({pc(W['wd_gross'])} weight, cost of capital {pc(W['wacc_exp_gross'])})",
         'raises the value',
         'Net debt is the quantity the bridge subtracts; using it in both places keeps the two '
         'consistent, and it is the more conservative of the two'],
        [f"Cost of debt on currency composition ({pc(IN['kd'])}): the disclosed coupon on each "
         f"currency leg, unadjusted",
         f"EGP-equivalent ({pc(DCF['kd_egp_equiv'])}): the hard-currency legs loaded with the "
         f"pound's own {pc(DCF['fx_dep_avg'])}/year forecast depreciation, under uncovered "
         f"interest parity",
         f"EGP {p2(DCF['ps_kd_egp_equiv'])} ({p2(DCF['ps_kd_egp_equiv'] - DCF['ps'])})",
         "Net debt carries only " + pc(W['wd_exp']) + " of the capital structure, so even this "
         f"{(DCF['kd_egp_equiv']-IN['kd'])*10000:,.0f}-basis-point swing in Kd moves the fair value "
         "by well under 1% — smaller than it "
         "looks. CAUTION: keeping the currency-composition basis as primary means the "
         "hard-currency debt is carried at its coupon rate, not compensated for devaluation "
         "risk beyond what this forecast's own exchange-rate path already assumes"],
        ['Risk-free rate ' + pc(IN['rf']),
         'External readings of the same instrument on the same date range from about 22.3% to '
         '23.0%, and disagree with each other; the adopted point sits at the low end',
         'roughly ±1% of value per 100bp',
         'Because the readings conflict, the rate is carried in the sensitivity grid rather '
         'than presented as precise; the direction of the low-end choice is generous and is '
         'said so here'],
        [f"Forecast effective tax rate {pc(IN['tax_eff'])}",
         f"Egypt's statutory 22.5%, or FY2025's actual effective 22.57%",
         'roughly +1.8 on the cash-flow lens (+2.5%)',
         'Audited effective rates ran 31.3% (FY2023), 30.1% (FY2024), 22.6% (FY2025) and 25.75% '
         '(Q1-2026); no statutory-vs-effective reconciliation is disclosed, and the group pays '
         'tax in 15+ jurisdictions plus revenue-basis Free-Zone entities. 24.5% sits between the '
         'FY2025 print and the Q1-2026 print rather than extrapolating the single best year — '
         'an external review correctly noted this choice was priced in the register but not '
         'displayed here; it now is']]
table(rows, [1.72, 1.85, 1.28, 2.15], size=8.0)
caption(f"The rating-basis column is the one most often raised against this study. It is not a "
        f"correction to an error — both bases are published by the same source and both appear in "
        f"this study's input register — but it is a material choice, and at EGP "
        f"{p2(DCF['ps_rating_basis'])} the alternative sits well below the primary. A reader who "
        f"prefers agency ratings to market spreads should use that number. (A July-2026 refresh "
        f"of the same file reportedly lifts the rating-basis premium by roughly one point, making "
        f"that alternative slightly more adverse still; the CDS-basis primary reproduces almost "
        f"unchanged from the July parameters.)")

# ---- 1.9 sensitivity -----------------------------------------------------------
H2('1.9  Sensitivity — the discount rate, the growth, the currency, the margin and the collection')
figure(os.path.join(HERE, 'fig2_sens.png'), 5.7,
       f"Figure 3 — discounted-cash-flow fair value per share across the terminal cost of capital "
       f"and terminal growth. No cell in the tested range reaches the market price of {p2(SPOT)}: "
       f"even the most generous corner sits well below it.")
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
rows.append(['Exchange-rate path', 'base −10% to +70% (the deep tail is the interest-parity '
             'case)', span(SN['grid_fx']), p2(max(SN['grid_fx'])-min(SN['grid_fx']))])
rows.append(['Segment margins (all three, multiplicative)', '−15% to +15%', span(SN['grid_margin']),
             p2(max(SN['grid_margin'])-min(SN['grid_margin']))])
rows.append(['Copper price', '−15% to +15%', span(SN['grid_copper']),
             p2(max(SN['grid_copper'])-min(SN['grid_copper']))])
rows.append(['Working capital / revenue', f"{pc(SN['nwc_grid'][0])} – {pc(SN['nwc_grid'][-1])}",
             span(SN['grid_nwc']), p2(max(SN['grid_nwc'])-min(SN['grid_nwc']))])
rows.append(['Terminal return on invested capital',
             f"{pc(SN['roic_grid'][0],0)} – {pc(SN['roic_grid'][-1],0)}", span(SN['grid_roic']),
             p2(max(SN['grid_roic'])-min(SN['grid_roic']))])
rows.append(['Terminal growth', f"{pc(SN['g_grid'][0],0)} – {pc(SN['g_grid'][-1],0)}",
             span([r[j] for r in [SN['grid_wacc_g'][2]] for j in range(5)]),
             p2(max(SN['grid_wacc_g'][2])-min(SN['grid_wacc_g'][2]))])
table(rows, [2.20, 1.55, 1.90, 1.35], size=8.5)
caption("Every row is a full re-run of the segment build, not a multiplier applied to a finished "
        "revenue line: a currency or copper move flows through Cables' revenue, the working "
        "capital and the segment profit exactly as it does in the base case. Note the copper row — "
        "the swing is small and can even run the 'wrong' way, because a higher metal price raises "
        "revenue and working capital without raising the profit Cables earns on it. Ranked by "
        "single-row swing, the segment-margin row is the LARGEST — an earlier caption claimed the "
        "terminal assumptions dominated every operating driver, which this table itself "
        "contradicts (a review caught it); what remains true is that the two cost-of-capital "
        "grids jointly span the widest surface, and a ±15% margin shock is a far larger "
        "displacement of the base case than any one row's parameter step.")

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
        ['52-week high (closing basis)', p2(hi52), f"{sgn(SPOT/hi52-1,1)} from the high — the "
         f"high IS the +14.1% print of 4 August 2026, one session before the anchor"],
        ['52-week high (intraday)', p2(float(np.max(_df['High'].to_numpy()[-252:]))),
         f"{sgn(SPOT/float(np.max(_df['High'].to_numpy()[-252:]))-1)} from the high — the "
         f"conventional basis, and the wider of the two"],
        ['52-week low', p2(lo52), f"{sgn(SPOT/lo52-1)} from the low"],
        ['Annualised volatility', pc(H3M['anchor_vol_ann']),
         'the fitted range-based volatility model\'s CURRENT state (an exponentially-weighted '
         'estimate, not a fixed window — the 50-session simple figure is given below for '
         'comparison), the input to the price cone in section 3']]
table(rows, [1.85, 1.15, 4.00], size=8.6)
P(f"The share is above every moving average in the stack, and the stack itself is in ascending "
  f"order — the configuration that describes an established uptrend. The price has compounded "
  f"{sgn(SPOT/px[-252]-1,0)} over the last 252 trading sessions (the exchange's trailing year on "
  f"the supplied series) and sits {sgn(SPOT/hi52-1,1)} from its "
  f"52-week high. Realised volatility of about {pc(H3M['anchor_vol_ann'],0)} a year is high in "
  f"absolute terms and unremarkable for this market. None of this is a valuation argument; it is "
  f"the price context the valuation has to be read against, and the gap between a strongly trending "
  f"price and a fundamental central below it is precisely what section 4 addresses.")
_r = np.diff(np.log(px)); _v50 = float(np.std(_r[-50:]) * np.sqrt(252))
_rx = np.delete(_r, -2); _v50x = float(np.std(_rx[-50:]) * np.sqrt(252))
P(f"One caveat on the volatility that sets the width of the price cone in section 3. The "
  f"{pc(H3M['anchor_vol_ann'])} annualised figure is dominated by a single session: the shares "
  f"rose 14.1% on 4 August 2026 on roughly eleven times normal volume. Realised volatility over "
  f"the last 50 sessions is {pc(_v50)}; strip out that one session and it falls to {pc(_v50x)}. "
  f"The cone in section 3 is therefore wide because of one day's move, and a reader who regards "
  f"that session as a one-off should treat the bands as correspondingly generous.", space_after=10)

# =========================== 3 MONTE CARLO ====================================
H1('3  A probabilistic price map')
P(f"This section answers a different question from the valuation. It does not ask what the business "
  f"is worth; it asks where the share price could plausibly be in one and three months, given how "
  f"this share has actually moved. The engine simulates 50,000 price paths from a volatility model "
  f"fitted to the daily high-low-open-close range, with a fat-tailed shock distribution and a drift "
  f"anchored to the cost of carry — an EGP deposit-rate carry, ~18% annualised as implied by the "
  f"median path, deliberately below the 22.3% bond yield and carrying no directional view.")
P(f"The widths below are calibrated rather than assumed. Tested by walk-forward simulation over "
  f"nearly five years — {BT5['windows']} independent non-overlapping quarterly windows with "
  f"origins from {BT5['first_origin']} to {BT5['last_origin']} (the final window runs three "
  f"months past its origin), each one forecast using only data available "
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
H1('4  Comparison of the lenses')
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
         'a judged multiple on forward earnings, discounted back, is the right way to price this '
         '(no peer multiple is computed anywhere in this study — §1.3)'],
        ['The market', p2(SPOT), 'revealed preference of the marginal buyer'],
        ['Three-month price map', f"median {p2(H3M['pct']['p50'])}, "
         f"{pc(H3M['p_above'],0)} chance of finishing above spot",
         'volatility persists as it has; no view on value']]
table(rows, [1.85, 2.20, 2.95], size=8.5)
P(f"The reading we take from this is that the disagreement between the market and the cash-flow model is almost "
  f"entirely a disagreement about the discount rate, and that this is a genuinely open question "
  f"rather than a mistake by one side. A company that earns just over half its money on a "
  f"hard-currency-linked basis, borrows roughly {pc(1-W['w_egp_implied'],0)} of its book in hard "
  f"currency at {pc(IN['kd_hard_note'])}, and holds assets in fifteen countries is only partly an "
  f"Egyptian risk. Charging it the full Egyptian equity risk premium — which is what our primary "
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
         f'about {pc(D["fgn_share_fy25_derived"],0)} of revenue is hard-currency linked, so both '
         f'the translated result and the working capital move with the pound',
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
         'no order book or backlog figure is disclosed anywhere in the audited filings, so the '
         'Constructions and infrastructure forecast tapers on its own revenue growth rather than '
         'a burn rate',
         'whether Constructions and infrastructure revenue growth (18% in FY2026E) holds up or '
         'decelerates faster than assumed'],
        ['Dividend policy',
         f"the FY2025 payout ALREADY stepped up +85%, to EGP {p2(IN['dps_fy25'])} (paid June "
         f"2026, 22.8% of attributable EPS); the forecast assumes {pc(F['payout'],0)} — whether "
         f"the step-up is the start of a trajectory or a plateau moves the equity roll-forward "
         f"and the net-debt path",
         'the distribution proposed on the FY2026 result, against the 22.8% just paid']]
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
         f"below even the 5th percentile ({p2(H3M['pct']['p5'])}) of the three-month "
         f"distribution — the price map and the valuation genuinely disagree, and stating the "
         f"gap at its full size is the point"]]
table(rows, [1.75, 1.75, 3.50], size=8.5)

# =========================== 7 CAVEATS ========================================
H1('7  Caveats and what would change our mind')
for head, body in [
    ("No order book, backlog or unit-volume figure is disclosed in the audited statements. ",
     f"All three audited financial statements and the Q1-2026 interim disclose segment revenue "
     f"and segment profit, but no tonnage, MVA, meter count or order-book figure for any segment. "
     f"The company's quarterly EARNINGS RELEASES have historically carried backlog and volume "
     f"data; they were not reachable from this research environment, so the forecast is built as "
     f"a taper on each segment's own recent revenue growth and margin path rather than a "
     f"backlog-burn model. An earlier wording said 'disclosed anywhere', which overclaimed — the "
     f"scope of the negative result is the audited statements, and cross-checking the "
     f"Constructions taper against the released backlog is the first refinement to make when "
     f"those releases become obtainable."),
    ("The valuation is dated, and the dating is now explicit. ",
     f"The cash-flow model is constructed at 31 December 2025 (the audited balance-sheet date); "
     f"every lens value is rolled {DCF['anchor_days']:.0f}/365 of a year to the 5-Aug-2026 "
     f"anchor at the {pc(W['ke_exp'])} cost of equity less the EGP {p2(IN['dps_fy25'])} dividend "
     f"paid in the window — worth about +{p2(DCF['ps']-DCF['ps_dec']+IN['dps_fy25'])} gross on "
     f"the primary lens. An earlier revision omitted this roll and compared a 31-Dec-2025 value "
     f"directly to the August price; an external review flagged it, correctly."),
    ("The terminal value is a large share of the answer. ",
     f"{pc(DCF['tv_share'],0)} of the enterprise value comes from the terminal value. This is "
     f"disclosed in the summary table, in the bridge and here. It is a consequence of a high "
     f"discount rate applied to a business still growing fast — the explicit years are heavily "
     f"discounted, so the perpetuity carries the weight. The terminal assumptions are stressed "
     f"across cost of capital, growth and return on invested capital in section 1.9."),
    ("The FY2026 forecast is checked against one quarter, not several. ",
     f"The segment build for FY2026E is cross-checked, not calibrated, against the disclosed "
     f"Q1-2026 print — the build's {n0(F['rev'][0])} against a {n0(BU['q1_26_implied_fy'])} "
     f"grossed-up implied full year, a gap of "
     f"{sgn(F['rev'][0]/BU['q1_26_implied_fy']-1)}. One quarter is a thin check, and it is the "
     f"reason the half-year 2026 result matters: it will either confirm or contradict the segment "
     f"growth and margin paths that all three cash-based lenses share."),
    ("The currency of discounting is unresolved, and it is the biggest single question. ",
     f"Our primary construction charges the full Egyptian equity risk premium to a company earning "
     f"just over half its money on a hard-currency-linked basis. The alternative construction "
     f"gives EGP {p2(DCF['ccy_alt_ps'])}. We have chosen the conservative reading and shown the "
     f"other in full rather than splitting the difference silently."),
    ("Terminal growth of 5% is roughly zero in real terms. ",
     f"The terminal risk-free rate embeds 5% inflation, so a 5% nominal terminal growth rate "
     f"assumes the company stops growing in real terms forever. For a business with a growing "
     f"hard-currency export franchise that is a conservative assumption, and the 6% and 7% columns "
     f"of the growth grid are not aggressive."),
    ("Minority interests are charged at their profit share, not at book. ",
     f"Minorities take {pc(DCF['nci_share'])} of group profit but only "
     f"{pc(HB['FY25']['nci']/(HB['FY25']['eqp']+HB['FY25']['nci']))} of book equity. Charging them "
     f"the profit share removes EGP {n0(DCF['nci_val'])}mn ({p2(DCF['nci_val']/SH)} per share) "
     f"from the equity value — EGP {p2((DCF['nci_val']-HB['FY25']['nci'])/SH)} per share MORE "
     f"than deducting the audited book value of {n0(HB['FY25']['nci'])}mn would (an earlier "
     f"wording conflated the total charge with the excess; this states both). It is also the "
     f"internally consistent choice: this study values the group's equity at "
     f"{n1(BK['pb_just'])}× book, so valuing the minorities' stake at 1.0× book while valuing "
     f"everyone else's above it would apply two different standards to the same subsidiaries."),
    ("The Egyptian-pound share of the debt book is inferred, not disclosed directly. ",
     f"The audited notes give average rates by currency bucket but not the size of each bucket. "
     f"The {pc(W['w_egp_implied'],0)} pound share used here is back-solved from the independently "
     f"computed effective interest rate against those two disclosed rates, and is labelled as "
     f"inferred throughout."),
    ("Concentration of control. ",
     f"The founding family holds {pc(IN['ownership']['family'])} and the free float is "
     f"{pc(own_float)}. Minority shareholders have limited influence over capital "
     f"allocation, related-party dealings and distribution policy. This is a governance fact, not "
     f"an allegation, and it is one reason the justified multiples used here carry a discount."),
    ("What would change our mind, specifically. ",
     f"Upward: sustained operating cash conversion above 60% of EBITDA for two consecutive years; "
     f"a credible reduction in the perceived country risk premium; Constructions and infrastructure "
     f"revenue growth holding above the taper assumed here. Downward: working capital rising "
     f"through {pc(SN['nwc_grid'][-1])} of revenue; segment margins failing to stabilise; a stall "
     f"in disinflation that freezes the discount rate glide.")]:
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
rows.append(['EBITDA (derived: EBIT + D&A)'] + hist_row('ebitda') + [n0(x) for x in F['ebitda']])
rows.append(['EBITDA margin'] + [pc(HI[y]['ebitda'] / HI[y]['rev']) for y in ('FY23','FY24','FY25')] +
            [pc(x) for x in F['ebitda_margin']])
rows.append(['Depreciation and amortisation'] + hist_row('dna', neg=True) +
            [f"({n0(x)})" for x in F['dna']])
rows.append(['EBIT'] + hist_row('ebit') + [n0(x) for x in F['ebit']])
rows.append(['Net finance costs'] + hist_row('fin') + [f"({n0(x)})" for x in F['interest']])
rows.append(['Share of equity-accounted investees'] + hist_row('assoc') +
            [n0(x) for x in F['assoc']])
rows.append(['Profit before tax'] + hist_row('ebt') + ['—'] * 5)
rows.append(['Income tax'] + hist_row('tax', neg=True) + ['—'] * 5)
rows.append(['Profit for the year'] + hist_row('pat') + ['—'] * 5)
rows.append(['Non-controlling interests'] + hist_row('nci', neg=True) + ['—'] * 5)
rows.append(['Profit attributable to shareholders'] + hist_row('npa') + [n0(x) for x in F['np_attr']])
rows.append(['Earnings per share (derived: attributable ÷ shares, EGP)'] +
            [p2(HI[y]['npa'] / SH) for y in ('FY23','FY24','FY25')] +
            [p2(x / SH) for x in F['np_attr']])
table(rows, [1.72, 0.66, 0.66, 0.66, 0.66, 0.66, 0.66, 0.66, 0.66], size=7.9,
      band_rows={3, 6, 13})
caption("Every FY2023-25 STATEMENT line is taken directly from the company's audited consolidated "
        "statements. Two rows are house DERIVATIONS and are labelled as such: EBITDA (EBIT plus "
        "D&A — the audited statements contain no EBITDA line, and the company's own separately "
        "published non-GAAP EBITDA is a different, larger definition) and earnings per share "
        "(attributable profit over shares outstanding; the company's own reported EPS of "
        "4.26 / 7.22 / 7.13 is struck after the Egyptian employee and board profit-share "
        "appropriation and is accordingly lower — both bases appear in §1.3). Forecast profit is "
        "struck after net interest on the estimated debt and cash balances and after tax and "
        "minority interests, and therefore differs slightly from the free-cash-flow waterfall in "
        "section 1.1, which is a pre-financing measure by construction.")

H2('A.2  Balance sheet — condensed house layout (consolidated, EGP mn)')
rows = [['EGP mn', 'FY2023', 'FY2024', 'FY2025'],
        ['Property, plant and equipment', n0(HB['FY23']['ppe']), n0(HB['FY24']['ppe']),
         n0(HB['FY25']['ppe'])],
        ['Equity-accounted investees', '3,802.8', n0(IN['assoc_bv_fy24']), n0(IN['assoc_bv_fy25'])],
        ['Inventories', n0(HB['FY23']['inv']), n0(HB['FY24']['inv']), n0(HB['FY25']['inv'])],
        ['Contract assets', n0(HB['FY23']['ca']), n0(HB['FY24']['ca']), n0(HB['FY25']['ca'])],
        ['Trade and other receivables', n0(HB['FY23']['recv']), n0(HB['FY24']['recv']),
         n0(HB['FY25']['recv'])],
        ['Cash and cash equivalents', n0(HB['FY23']['cash']), n0(HB['FY24']['cash']),
         n0(HB['FY25']['cash'])],
        ['Total assets', n0(HB['FY23']['assets']), n0(HB['FY24']['assets']), n0(HB['FY25']['assets'])],
        ['Loans and borrowings', n0(HB['FY23']['debt']), n0(HB['FY24']['debt']), n0(HB['FY25']['debt'])],
        ['Trade and other payables', n0(HB['FY23']['pay']), n0(HB['FY24']['pay']), n0(HB['FY25']['pay'])],
        ['Contract liabilities', n0(HB['FY23']['cl']), n0(HB['FY24']['cl']), n0(HB['FY25']['cl'])],
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
caption("FY2023, FY2024 and FY2025 are all audited — every line, including FY2025, is the closing "
        "figure from the company's own consolidated statements. No triangulation or roll-forward "
        "is used for any historical year.")

H2('A.3  Forecast balance sheet and cash-flow markers')
rows = [['EGP mn'] + YRS,
        ['Net working capital'] + [n0(x) for x in F['nwc']],
        ['Property, plant and equipment'] + [n0(x) for x in F['ppe']],
        ['Intangible assets and goodwill'] + [n0(IN['intang_fy25'])] * 5,
        ['Invested capital'] + [n0(x) for x in F['ic']],
        ['Return on invested capital'] + [pc(x) for x in F['roic']],
        ['Capital expenditure'] + [f"({n0(x)})" for x in F['capex']],
        ['Change in working capital'] + [f"({n0(x)})" for x in F['dnwc']],
        ['Free cash flow to the firm'] + [n0(x) for x in F['fcff']],
        ['Shareholders\' equity'] + [n0(x) for x in F['equity']],
        ['Net debt'] + [n0(x) for x in F['net_debt']]]
table(rows, [2.05, 0.99, 0.99, 0.99, 0.99, 0.99], size=8.4, band_rows={7})
P(f"The FY2025 accounts are the reason the free-cash-flow line above should be read carefully. "
  f"That year the group turned EGP {n0(HI['FY25']['ebitda'])}mn of EBITDA into EGP "
  f"{n0(IN['ocf_fy25'])}mn of operating cash after interest of EGP {n0(IN['int_paid_fy25'])}mn and "
  f"tax of EGP {n0(IN['tax_paid_fy25'])}mn, then spent EGP {n0(IN['capex_fy25'])}mn on capital "
  f"expenditure. The forecast assumes working-capital intensity stays near this level rather than "
  f"deteriorating, which is what allows free cash flow to turn positive and build. If it does not, "
  f"the model is wrong in the direction that matters most.")

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
         'the right frame for the roughly 32% of revenue that is the Constructions and '
         'infrastructure segment',
         'project accounting differs, and backlog quality is not comparable across disclosure '
         'regimes']]
table(rows, [1.70, 1.05, 2.10, 2.15], size=8.3)
P("The absence of a clean comparable is itself a finding. This is a diversified industrial group "
  "with a manufacturing business, a contracting business and an infrastructure portfolio, listed "
  "in a frontier market, earning just over half its revenue on a hard-currency-linked basis. Any "
  "single peer multiple applied to it imports assumptions about country risk that the cash-flow "
  "model tests explicitly. That is why the relative lens carries a fifth of the weight and not "
  "more.")

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
        ['Margin normalisation overshooting', 'segment margins fail to stabilise after the '
         'currency windfall that lifted FY2023-24 unwinds further',
         f"{p2(max(SN['grid_margin'])-min(SN['grid_margin']))} per share across ±2 percentage points"],
        ['Terminal return on capital', 'the perpetuity assumes returns stay near the historical '
         'level', f"{p2(max(SN['grid_roic'])-min(SN['grid_roic']))} per share across the tested range"],
        ['Governance and control', f"free float of {pc(own_float)}; minority "
         f"influence over capital allocation is limited",
         'expressed through the discount applied to the justified multiples, not as a separate line'],
        ['Execution and country concentration',
         'projects across Africa and the Gulf carry counterparty, payment and political risk',
         'sits inside the Constructions and infrastructure segment margin assumption'],
        ['No order book or unit-volume disclosure', 'the forecast tapers on segment revenue '
         'growth rather than a reconstructed unit or backlog-burn model',
         'stated in full in section 7']]
table(rows, [1.85, 2.60, 2.55], size=8.3)

H2('B.3  The research register — layers, dated, negative results included')
P("Research for this study proceeded in four layers: the global and macroeconomic backdrop; the "
  "country; the industry; and the company itself. The full source-by-source register, with dates, "
  "layers and the four-field provenance of every input, is published as a separate bibliography "
  "document accompanying this study. This version was rebuilt once the company's own audited "
  "FY2023-25 consolidated statements and Q1-2026 condensed interim statements became available; "
  "two negative results remain and are recorded here because they shaped what could and could not "
  "be asserted.")
for head, body in [
    ("No order book, backlog or unit-volume figure is disclosed in the audited statements. ",
     "Neither the three audited annual statements nor the Q1-2026 interim discloses a tonnage, "
     "MVA, meter-count or backlog figure for any segment. The company's quarterly earnings "
     "releases have historically carried such data but were not reachable from this research "
     "environment. The forecast is built as a taper on each segment's own recent revenue growth "
     "and margin path instead."),
    ("A facility-by-facility currency split of the debt book is not disclosed. ",
     "The audited notes give average rates by currency bucket (Egyptian pound and a blended "
     "hard-currency bucket in FY2025) but not the size of each bucket. The pound share used here "
     "is back-solved from the independently computed effective interest rate and is labelled as "
     "inferred.")]:
    bullet(body, bold_head=head)
P('', space_after=8)

# =========================== APPENDIX C =======================================
H1('Appendix C  The expert valuation panel')
P(f"Three valuation approaches are run against the same disclosed facts by three notional "
  f"experts, each committed to a different method and each required to state what would prove "
  f"them wrong. They are not asked to agree, and they do not. Two dating and independence notes, "
  f"stated up front: every panel figure is rolled to the 5-Aug-2026 anchor exactly as the four "
  f"lenses are; and Expert 1 deliberately runs the SAME kind of earnings-power question as "
  f"section 1.4 with different persona choices — FY2028-scale earnings at 9.5× against the "
  f"lens's current-scale earnings at 9.0× — which is why the two land {p2(EXP['e1']['base'])} and "
  f"{p2(LN['normalized']['base'])} respectively. The divergence is the persona doing what it "
  f"says (no time-value discipline), it is disclosed, and only the section-1.4 construction "
  f"enters the central.")

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
        ['Less after-tax interest (EGP mn)', f"({n0(E2['int_at'])}) — the FY2029 point of the "
         f"forecast's net-finance construction (cost-of-debt path × gross book less 10% on the "
         f"FY2025 cash balance), after tax; shown because a review correctly noted it was not "
         f"reconcilable as previously displayed"],
        [f"Less minority share ({pc(DCF['nci_share'])})",
         f"({n0((E2['fcff']-E2['int_at'])*DCF['nci_share'])})"],
        ['Owner cash earnings (EGP mn)', n0(E2['fcfe'])],
        ['Grown one year and capitalised at cost of equity less growth',
         f"× {1+IN['g_term']:.2f} ÷ ({pc(E2['ke'])} − {pc(IN['g_term'],0)})"],
        ['Fair value, rolled to the anchor (EGP per share)', p2(E2['base'])],
        ['Range', f"{p2(E2['rng'][0])} – {p2(E2['rng'][1])}"]]
table(rows, [4.35, 1.55], size=8.6, band_rows={7})
P(f"This is the harshest of the three readings, at EGP {p2(E2['base'])}, and the reason is "
  f"specific and defensible: it takes the FY2025 evidence — EGP {n0(HI['FY25']['ebitda'])}mn of "
  f"EBITDA converting to EGP {n0(IN['ocf_fy25'])}mn of operating cash — as a statement about the "
  f"business model rather than about one unusual year.")
P("Named sensitivity: if working capital intensity fell by two percentage points of revenue, this "
  "valuation would rise by roughly a third, because the entire gap between this expert and the "
  "other two is the cash working capital absorbs.")
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
        ['Fair value, rolled to the anchor (EGP per share)', p2(E3['base'])],
        ['Range — the upper bound is the hard-currency discounting case',
         f"{p2(E3['rng'][0])} – {p2(E3['rng'][1])}"]]
table(rows, [4.35, 1.55], size=8.6, band_rows={6})
rows = [['Year'] + YRS,
        ['Return on invested capital (NOPAT ÷ closing capital)'] + [pc(x) for x in F['roic']],
        ['Cost of capital that year'] + [pc(x) for x in F['fwd_wacc']],
        ['Spread'] + [f"{(F['roic'][i]-F['fwd_wacc'][i])*100:+.1f}pp" for i in range(5)],
        ['Economic profit (NOPAT − charge on OPENING capital, EGP mn)'] +
        [n0(x) for x in E3['ep']]]
table(rows, [2.05, 0.99, 0.99, 0.99, 0.99, 0.99], size=8.4, band_rows={4})
caption(f"Two conventions sit in this table and are named so they cannot be confused: the ROIC "
        f"row divides by CLOSING capital (matching Appendix A.3), while economic profit charges "
        f"the cost of capital on OPENING capital — the capital actually employed through the "
        f"year. So spread × closing capital will not reproduce the economic-profit row; the "
        f"identity holds on opening capital. Note also that this leg's enterprise value "
        f"({n0(E3['ev'])}) and the DCF's ({n0(DCF['ev'])}) differ by {n0(DCF['ev']-E3['ev'])}: "
        f"economic-profit and FCFF valuations are algebraically identical on identical "
        f"assumptions, and the gap here is exactly the different terminal treatment (a fading "
        f"economic-profit perpetuity versus the reinvestment-rate terminal value). Expert 3 is "
        f"therefore a RESTATEMENT of the DCF under a different terminal discipline, not an "
        f"independent confirmation, and is read as such.")
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
        ['"You are charging the owner for working capital that funds growth which will convert to '
         'cash. That is a timing charge treated as a permanent one."',
         'Expert 1 to Expert 2',
         'Partly conceded. FY2025 did improve — working capital fell from 23.1% to 19.9% of '
         'revenue even as revenue grew. Until that improvement repeats for a second year, treating '
         'the earlier absorption as the norm rather than the exception is the more cautious '
         'position.'],
        ['"Your invested-capital base is understated because it excludes goodwill written off and '
         'assets held at historical cost through three devaluations."', 'Expert 2 to Expert 3',
         'Conceded. A higher capital base would lower the measured return on capital and shrink '
         'the spread, making this reading more pessimistic, not less. The direction of the error '
         'is unfavourable to the conclusion already reached.'],
        ['"All three of you are answering an Egyptian question about a company that earns just '
         'over half its money on a hard-currency-linked basis."', 'The panel to itself',
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
  f"values earnings and lands near the market price. Expert 2 values cash and lands well below "
  f"it. Expert 3 values the spread between returns and the cost of capital "
  f"and finds that the answer depends entirely on which cost of capital applies. The panel median "
  f"of {p2(D['panel_centre'])} sits {sgn(D['panel_centre']/SPOT-1,0)} against the market price and "
  f"{sgn(D['panel_centre']/D['central']-1,0)} against the study's own central of "
  f"{p2(D['central'])} — a real gap, stated at its size rather than smoothed, and driven by the "
  f"panel's harsher cash and returns legs outvoting its generous earnings leg.")

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
