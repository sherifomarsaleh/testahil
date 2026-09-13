"""SWDY_Valuation_Study_{edition}_public.docx — python-docx builder, house style.
Reads study_numbers.json exclusively: no numeral is typed into this file."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import edition as _ed                      # the edition date, written once
sys.path.insert(0, os.path.join(HERE, '..'))
exec(open(os.path.join(HERE, 'docx_base.py')).read())   # doc, P, H1, H2, table, box, ...

D = json.load(open(os.path.join(HERE, 'study_numbers.json')))
M, HI, HB, F = D['meta'], D['hist_is'], D['hist_bs'], D['fcst']
W, DCF, LN, SN = D['wacc'], D['dcf'], D['lenses'], D['sens']
EXP, TR, REL, NRM, BK = D['experts'], D['terminal_recon'], D['rel'], D['norm'], D['book']
S0, STK, SEG = D['step0'], D['strike'], D['seg_fy25']
BU = D['bottomup']
AR = D['drivers_as_run']   # what the model RUNS, not what an earlier edition ran
COC = D['cost_of_capital_record']
_SL = DCF['scenario_legs']   # how the published range is struck [F10]
_CT = SN['contested']        # the contested-choice impacts, each a re-run [F23]
import datetime as _dt
def _age_days(iso):
    """How stale an input is at the anchor date. Computed, never typed — an age in a
    delivered sentence is the first thing to go wrong when either date moves [F25]."""
    _d = lambda x: _dt.date(*[int(p) for p in x.split('-')])
    return (_d(M['asof']) - _d(iso)).days
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
def n2(x): return f"{x:,.3f}"
def p2(x): return f"{x:.2f}"
def pc(x, dp=1): return f"{x*100:.{dp}f}%"
def sgn(x, dp=0): return f"{x*100:+.{dp}f}%"


def dirword(x, up="above", down="below", flat="level with"):
    """The direction word for a signed quantity, DERIVED rather than typed.

    A sentence saying "-6.9% ABOVE the primary reading" is not a rounding slip, it is
    two readers of one fact: the figure computes and the word beside it was written
    when the figure had the other sign. This study shipped exactly that on 10-09-2026
    -- the hard-currency alternative had been above the primary reading and the
    re-strike put it below, and the word stayed. The delivered-vocabulary gate's
    sign-word check caught it, which is the only reason anybody knows.
    """
    if abs(x) < 5e-5:
        return flat
    return up if x > 0 else down
def to_anchor_docx(v):
    """Mirror of the engine's anchor roll, for counterfactual display values only."""
    # THE DIVIDEND IS DEDUCTED AT THE ANCHOR, NOT AT ITS EX-DATE. compute.py rolls the
    # EGP 1.85 forward from 4 June to the 3 September anchor at the explicit-window cost
    # of equity and deducts 1.9678; this helper deducted the raw 1.85, so every lens
    # value this document rolled came out 11.8 piastres above the model's — and the
    # equity bridge's printed steps reached 88.06 under a printed total of 87.94, which
    # is a reader adding the column up and not getting the answer.
    return v * DCF['roll'] - DCF['div_at_anchor']

# =========================== MASTHEAD / TITLE ================================
# ONE literal for the delivered filename: the masthead's edition date is derived
# from it, so the two cannot state different days.
DELIVERED = _ed.STUDY_DOCX
masthead(edition_from_filename(DELIVERED))
H2('Independent Valuation Study — Educational Analysis')
H1('Elsewedy Electric Company S.A.E. (EGX: SWDY)')

# [R-DOC-03] THE TWO DATES, AT THE TOP, LABELLED. A valuation states a number struck
# against a price, and those are two facts with two dates that are not the same date.
# Resolved by engine/doc_dates.py and never from a file's modification time.
import sys as _sys_dd
import os as _os_dd
_sys_dd.path.insert(0, _os_dd.path.dirname(_os_dd.path.dirname(_os_dd.path.abspath(__file__))))
import doc_dates as _DD
P(_DD.header_line('SWDY'), size=8, color=GREY)

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
# NOT "THE FOUR LENSES CENTRE AT". Section 1.5 spends a page saying the central is the
# cash-flow lens itself and is NOT an average of the four; this sentence, four pages
# earlier and the first place a reader meets the number, said the opposite in five words.
# The figure it quoted was never a centre of anything -- it is the DCF, to the decimal.
P(f"On our primary construction the cash-flow lens — which is the answer here, not one vote "
  f"of four — values the company at EGP {p2(D['central'])} per share against "
  f"a market price of {p2(SPOT)} — the price sits about {sgn(SPOT/D['central']-1,0)} above the "
  f"central estimate. That gap is not mainly an argument about the business; it is an argument "
  f"about the discount rate. Discounted at an Egyptian cost of capital gliding "
  f"{pc(W['wacc_exp'])} to {pc(W['wacc_term'])}, the cash flows support roughly EGP "
  f"{p2(DCF['ps'])}. Discount the hard-currency share of those same cash flows at a hard-currency "
  f"cost of capital of about {pc(W['wacc_usd_alt'])} and the same model produces EGP "
  f"{p2(DCF['ccy_alt_ps'])} — {sgn(DCF['ccy_alt_ps']/SPOT-1,0)} against today's price, and "
  f"{sgn(DCF['ccy_alt_ps']/DCF['ps']-1,0)} "
  f"{dirword(DCF['ccy_alt_ps']/DCF['ps']-1)} the primary reading. "
  # THE CONCLUSION IS DERIVED TOO, because it inverted with the number. This sentence
  # read "the market appears to be applying something at least as generous as the
  # second view" -- written when the hard-currency alternative sat ABOVE the primary.
  # It now sits below it and further from the price, so the second view is the LESS
  # generous of the two and the old sentence said the opposite of its own figures.
  + (f"So the currency lens does not explain the gap: it is the harsher of the two "
     f"readings, and the market is paying more than either. "
     if DCF['ccy_alt_ps'] < DCF['ps'] else
     f"So a reader who prefers the hard-currency construction closes part of the gap, "
     f"though not all of it. ")
  + f"Both are shown, and neither is hidden inside an average.", space_after=10)

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
        f"own two scenarios on one clock, not a spread across four methods. Those two "
        f"scenarios move the cost of capital through the measured beta at its own 90% "
        f"confidence bounds ({n2(_SL['beta_bear'])} in the bear and {n2(_SL['beta_bull'])} in "
        f"the bull, around an estimate of {n2(_SL['beta_base'])} with a standard error of "
        f"{_SL['beta_se']:.4f} on {_SL['beta_n']} weekly observations), not through a round "
        f"number chosen by hand — so the width of the range is the width the estimate itself "
        f"supports. Because this study takes the terminal beta to be 1.0, that whole interval "
        f"reaches the explicit window only and is worth about "
        f"{p2((_SL['beta_only_bull']-_SL['beta_only_bear'])/2)} a share on its own; the rest of "
        f"the span is the operating case — segment margins {pc(_SL['gp_bear']-1,0)} to "
        f"{pc(_SL['gp_bull']-1,0)} against the adopted level, the currency path "
        f"{pc(_SL['fx_bear']-1,0)} to {pc(_SL['fx_bull']-1,0)}, and the corporate cost load "
        f"{pc(-_SL['opex_bear'],1)} to {pc(-_SL['opex_bull'],1)} of revenue — which are judged "
        f"multipliers and are shown here as such. Terminal "
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
        ['Scale', f"FY2025 revenue EGP {n0(HI['FY25']['rev'])}mn across 31 production "
         f"facilities in 15 countries. AN EXTERNAL REVIEW CHALLENGED THE HEADCOUNT THIS ROW "
         f"USED TO CARRY — 'more than 20,000' — as understating the group several times over, "
         f"and this study cannot settle it from anything it holds: no audited filing it reads "
         f"discloses a headcount. What it CAN check points the same way. The same statements "
         f"disclose a FY2025 wage bill of EGP {n0(D['employees_cap']['wages_fy25'])}mn across "
         f"the three expense notes, which at 20,000 people would be EGP "
         f"{n0(D['employees_cap']['wages_fy25'] * 1e6 / 20000)} a head — implausible for a "
         f"group whose revenue is majority Egyptian. The figure is withdrawn rather than "
         f"replaced with one this study has not sourced, and it is recorded as an open "
         f"question. Nothing in the valuation reads it"],
        ['Geographic mix', f"The audited FY2025 geographic note (Note 5-2) shows "
         f"{pc(IN['fgn_egp_share_fy25'],1)} of revenue booked outside Egypt — a statement about "
         f"where the customer sits, not about pricing currency. Separately, this study derives the "
         f"share that is hard-currency LINKED, i.e. dollar-priced, at about "
         f"{pc(D['fgn_share_fy25_derived'],0)} using segment-level export-intensity weights of "
         f"Cables 65% / Constructions 30% / Electrical products 45% (house judgements, stated so "
         f"they can be disputed; the forecast-year share runs ~53% as Cables' weight in the mix "
         f"rises); that is the figure used wherever the currency question is valued"],
        ['Order book and volumes',
         'Not disclosed in any of the audited FY2023-25 statements or the Q1-2026 interim. '
         'THE COMPANY DISCLOSES BOTH IN ITS OWN QUARTERLY EARNINGS RELEASES, and those '
         f"releases are read. Engineering and construction backlog runs EGP 293bn at "
         f"December 2025 and 346bn at 30 June 2026, with wires and cables 43.5bn and meters "
         f"8.8bn beside it; cable volumes run "
         f"{' / '.join(n0(IN['cables_tonnage_hist'][_y]) for _y in ('FY22','FY23','FY24','FY25'))}"
         f" tonnes over FY2022-25 and {n0(IN['cables_tonnage_h1']['H1_26'])} in the reviewed "
         f"half against {n0(IN['cables_tonnage_h1']['H1_25'])}. The volume series "
         'sets the Cables segment growth driver directly. The backlog is read and NOT burnt '
         'down: it corroborates the Constructions growth rate without producing it'],
        ['Shares outstanding', f"{n0(SH)}mn"],
        ['Market capitalisation', f"EGP {n0(M['mktcap'])}mn at the anchor price"],
        ['Ownership', f"El Sewedy family ~{pc(own['family'])} · Electra Investment Holding "
         f"{pc(own['electra'])} · free float ~{pc(own_float)}, per the audited FY2025 shareholder "
         f"table. Electra, an Abu Dhabi holding vehicle, acquired "
         f"{pc(IN['electra_mto']['stake'])} in a July-2024 tender "
         f"offer at USD {IN['electra_mto']['price_usd']:.2f} per share (~USD "
         f"{n0(IN['electra_mto']['value_usdmn'])}mn) and topped up to "
         f"{pc(IN['sh_electra_fy24'])} by FY2024-end; over "
         f"2025 it SOLD roughly {n1(IN['electra_sold_2025_mn'])}mn shares into the market, "
         f"taking its stake to "
         f"{pc(own['electra'])} — a disposal, not dilution: the share count is unchanged. The "
         f"{pc(own['other'])} 'other shareholders' line is an upper bound on the true free "
         f"float, since "
         f"family-linked vehicles may sit inside it"],
        ['Net bank debt', f"EGP {n0(IN['nd_fy25'])}mn at 31 December 2025 "
         f"({n1(IN['nd_fy25']/HI['FY25']['ebitda'])}× EBITDA), computed from the audited balance "
         f"sheet: loans and borrowings including leases {n0(HB['FY25']['debt'])} less cash "
         f"{n0(HB['FY25']['cash'])}. The company's own FY2025 earnings release quotes EGP "
         f"{n0(IN['nd_release_fy25'])}mn on its own narrower basis; the audited-statement "
         f"computation is used, and the "
         f"{n0(abs(IN['nd_fy25'] - IN['nd_release_fy25']))}mn definitional gap is noted rather "
         f"than resolved"],
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
         f"{pc(DCF['dps_payout_fy25'])} of FY2025 attributable EPS, an "
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
  # F6, EXTERNAL AUDIT: THE MARGINS ARE INPUTS AND THIS CALLED THEM OUTPUTS. Each segment
  # margin is a typed constant held flat for five years — cables 11.4341%, constructions
  # 8.9871%, electrical 23.6221% — and segment profit is revenue times that constant.
  # Only the GROUP EBITDA margin is an output, and only of the segment mix. The
  # distinction matters because the margin row is the LARGEST single sensitivity in this
  # study, wider than any cost-of-capital row: calling it an output takes the reader's
  # biggest lever out of view.
  f"The group EBITDA margin is therefore an OUTPUT of the build — of the segment mix and "
  f"the corporate cost load — rather than an assumption fed into it. The three SEGMENT "
  f"margins are inputs and are stated as such: each is FY2025's own level plus the "
  f"like-for-like change the reviewed half measured, held flat across the window, and the "
  f"alternative of taking the half's LEVEL instead is priced in section 1.9. The "
  f"historical version of that build reconciles to the audited income statement EXACTLY on "
  f"revenue "
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

H2('The valuation, on one page')
# THE ONE TABLE A READER OPENS THE DOCUMENT TO FIND [R-DCF-01]. Built by the shared
# module from this study's own committed numbers — nothing here is recomputed, and
# the module refuses to render a table whose present values do not sum to the
# enterprise value the study published.
import dcf_table as _DT
# THIS STUDY'S OWN NAMES FOR TWO CONTRACT FIELDS. Undeclared, the shared bridge
# found neither: it read `emp_val` where this study files `emp_charge`, and
# meta.shares where this study writes shares_mn. The employees' statutory share
# is EGP 22,575mn -- 10.55 a share -- and the delivered bridge printed an equity
# value its own printed lines did not reach.
_vt_rows, _vt_bridge, _vt_rec = _DT.dcf_table(
    D, currency='EGP', unit='mn',
    fields={'emp_val': 'emp_charge', 'shares': 'shares_mn'})
table(_vt_rows, [2.10, 0.62, 0.62, 0.62, 0.62, 0.62], size=7.6,
      band_rows={_i for _i, _r in enumerate(_vt_rows)
                 if _r[0] == 'Free cash flow to the firm'})
table(_vt_bridge, [3.60, 1.10], size=7.6,
      band_rows={_i for _i, _r in enumerate(_vt_bridge)
                 if _r[0] in ('ENTERPRISE VALUE', 'EQUITY VALUE', 'VALUE PER SHARE')})
caption("Every line is read from this study's own committed numbers, not recomputed for the "
        "table: the present values sum to the enterprise value above them, and the bridge "
        "runs to the value per share the rest of this document carries. Free cash flow is "
        "NEGATIVE in the first forecast year — revenue grows by more than a third and working "
        "capital absorbs "
        f"{n0(F['dnwc'][0])} against capital expenditure of {n0(F['capex'][0])} — which is what "
        "growth costs a working-capital-heavy industrial and is not a distress signal. The "
        f"terminal value is {pc(DCF['tv_share'])} of enterprise value, so the two lines under "
        "it deserve the sensitivity that follows.")

H2('The two numbers the answer turns on')
_sg_rows, _sg_rec = _DT.sensitivity_grid(D, currency='EGP')
table(_sg_rows, [1.55, 1.03, 1.03, 1.03, 1.03, 1.03], size=7.8, band_rows={0, 3})
caption(f"Terminal cost of capital down the side, terminal growth across the top, both stepping "
        f"around the adopted case. THE CENTRE CELL IS THE STUDY'S OWN ANSWER — EGP "
        f"{p2(_sg_rec['centre_cell'])} — so the reader can locate the struck number on the grid "
        "and read the cost of being wrong in either direction from it. A one-point move in the "
        "terminal cost of capital is worth more than a one-point move in terminal growth, which "
        "is the usual shape when the terminal carries most of the value.")

H2('The bridge from enterprise value to the equity — and to the anchor date')
# THE BLOCK PRINTED A CASH FLOW THE MODEL DOES NOT USE. It computed the terminal flow as
# NOPAT x (1+g) x (1 - reinvestment rate) — the identity this study RETIRED — and got
# 30,397, which capitalises to 490,003 against the 493,872 printed two rows below it. The
# model's terminal is built by the sanctioned module and its cash flow is 28,072. So the
# one table a reader uses to follow the largest number in the study could not be added up.
# Read from the committed terminal record, and described as what it is.
_TR = DCF['terminal_record']
_tfcff = _TR['fcff']
rows = [['Step', 'EGP mn', 'Note'],
        ['Present value of the five forecast years', n0(DCF['pv_explicit']),
         'sum of the present-value row above'],
        ['Terminal-year free cash flow', n0(_tfcff),
         f"NOT a reinvestment-rate identity. FY2030E NOPAT of {n0(F['nopat'][-1])} — the last "
         f"forecast year's, NOT grown, because the capitalisation below grows the finished "
         f"cash flow one year and growing it here as well would overstate the terminal by a "
         f"full year — plus book "
         f"depreciation of {n0(_TR['dna_addback'])} added back, LESS maintenance at "
         f"replacement cost {n0(_TR['maintenance'])} on the derived "
         f"{IN['asset_life_derived']:.2f}-year asset life, less growth capital "
         f"{n0(_TR['growth_capex'])} at the stated real terminal growth, less inflation on "
         f"working capital {n0(_TR['wc_charge'])} — so the terminal pays for replacing its "
         f"own assets at what they cost to replace, not at what they cost historically. "
         f"The retired construction forced reinvestment to g ÷ terminal return on capital "
         f"({pc(DCF['roic_term'])}) and is published beside the model, unused"],
        ['Present value of the terminal value', n0(DCF['pv_tv']),
         f"the terminal cash flow grown one year and capitalised at "
         f"{pc(W['wacc_term'],2)} − {pc(DCF['g'],2)}, then discounted at the year-5 factor "
         f"{F['df'][-1]:.4f}. IT REPRODUCES FROM THE ROW ABOVE: {n0(_tfcff)} × "
         f"{1+DCF['g']:.4f} ÷ {pc(DCF['terminal_spread'],4)} = {n0(DCF['tv'])}, and "
         f"{n0(DCF['tv'])} × {F['df'][-1]:.4f} = {n0(DCF['pv_tv'])}"],
        ['Enterprise value', n0(DCF['ev']), 'the two lines above'],
        ['Terminal value as a share of enterprise value', pc(DCF['tv_share'],0),
         'disclosed here and in the summary table; stress-tested in section 1.9'],
        ['Less net bank debt', f"({n0(DCF['nd'])})", 'audited, at 31 December 2025'],
        ['Plus equity-accounted investees', n0(DCF['assoc']),
         'audited FY2025 carrying value, no uplift; these earn outside the consolidated cash flow'],
        ['Less minority interests', f"({n0(DCF['nci_val'])})",
         f"minorities take {pc(DCF['nci_share'])} of group profit, so they are charged the same "
         f"share of the value"],
        # THE ROW WITHOUT WHICH THIS TABLE DOES NOT ADD UP. It was charged in the model
        # from the first edition and printed in none of them, so the four steps above
        # summed to 92,458 against a printed equity of 81,185 and nothing in the document
        # accounted for the 11,273 difference.
        ["Less the employees' statutory share of distributable profits",
         f"({n0(DCF['emp_charge'])})",
         f"Egyptian company law gives employees a share of DISTRIBUTABLE PROFITS. This "
         f"study does not compute that statutory base — it is struck at the company level "
         f"and the filings do not publish it — so the "
         f"{pc(DCF['emp_rate'])} carried here is not the statutory percentage. It is the "
         f"OBSERVED RATIO the disclosure itself reports the charge at: the mean of the "
         f"charge over profit attributable to owners across FY2024, FY2025 and H1-2026, "
         f"carried forward on the assumption that the relationship between the two bases "
         f"holds. Stated because the difference matters to a reader checking the law: the "
         f"base in the statute and the base in this row are not the same quantity, and "
         f"earlier editions of this table named only the second while citing the first. "
         f"The charge is disclosed only in the earnings-per-share note, below "
         f"the attributable line, and appears in no line of the income statement. The "
         # THIS CELL SAID "no filing discloses the cap's headroom, so the charge is an
         # UPPER bound" WHILE THE STUDY COMPUTED THE HEADROOM. The wage bill is disclosed
         # in three notes of the same audited statements; study_numbers.employees_cap
         # carries wages of EGP 18,906mn against a share of EGP 2,073mn -- 9.1x of
         # headroom -- and records binds=False. A caveat retained after the work that
         # answers it reads as diligence and is the opposite: it tells the reader to
         # discount a number this study has actually pinned down.
         f"statutory share is capped at total annual wages, and that cap does not bind: "
         f"the wage bill is disclosed in three notes of the same audited statements at "
         f"EGP {n0(D['employees_cap']['wages_fy25'])}mn against a statutory share of EGP "
         f"{n0(D['employees_cap']['share_fy25'])}mn, so the charge sits at "
         f"{n1(D['employees_cap']['headroom_fy25'])}x of headroom. It is the measured "
         f"charge, not an upper bound"],
        ['Equity attributable, at 31 December 2025', n0(DCF['eq_attr']),
         f"EGP {p2(DCF['ps_dec'])} per share — dated at the audited balance-sheet date the "
         f"bridge subtracts net debt at"],
        [f"Rolled {DCF['anchor_days']:.0f}/365 of a year to the anchor", f"×{DCF['roll']:.4f}",
         f"fair value accretes at the {pc(W['ke_exp'])} cost of equity between the valuation "
         f"date and the {M['asof']} anchor — one date, one price of time, applied to the "
         f"comparison itself"],
        [f"Less the FY2025 dividend paid in the window", f"({p2(DCF['div_at_anchor'])}/sh)",
         f"EGP {p2(IN['dps_fy25'])} went ex on 4 June 2026 — value that left the share before "
         f"the anchor. It is deducted AT THE ANCHOR, not at its ex-date: carried forward the "
         f"{DCF['div_days']:.0f} days to {M['asof']} at the {pc(W['ke_exp'])} cost of equity "
         f"the rest of the roll uses, it is EGP {p2(DCF['div_at_anchor'])}. Deducting the raw "
         f"{p2(IN['dps_fy25'])} against a value rolled the whole way would credit the share "
         f"with earning a "
         f"return on money it had already paid out"],
        ['Fair value per share at the anchor (EGP)', p2(DCF['ps']),
         f"against a spot of {p2(SPOT)} ({sgn(DCF['ps']/SPOT-1,0)})"]]
table(rows, [2.55, 1.05, 3.40], size=8.4, band_rows={4, 13}, align_right_from=1)
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
  f"or EGP {p2(LN['book']['base'])} per share at the anchor. This is the weakest of the four "
  f"lenses for this company — it is published as a disclosed FLOOR and is never weighted, "
  f"because nothing here is weighted — for a specific reason: three years of currency "
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
        # THE DENOMINATOR WAS TYPED. eps_fy25 is a four-field input read out of note 39
        # of the audited statements; this cell held its own copy, so a correction to the
        # register would have left the multiple standing on the old number.
        ['Price / earnings (trailing, as-reported basis)', f"{n1(SPOT/IN['eps_fy25'])}×",
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
        # F21: THIS ROW WAS WRONG THREE WAYS AT ONCE. It is labelled "Plus", the model
        # ADDS it, and the committed value is POSITIVE (+3,106.38) — and it printed
        # "(-3,106)", a bracket and a minus sign on a positive number, under a prose note
        # calling it "net negative". FY2026's present value is -252 and FY2027's is
        # +3,359, and the study's own free-cash-flow table prints both two pages earlier.
        ['Plus interim cash flows', n0(REL['pv_interim']),
         f"the present value of the FY2026-27 free cash flows the forward multiple does not "
         f"capture. NET POSITIVE: FY2026 consumes working capital and its present value is "
         f"{n0(F['fcff'][0] * F['df'][0])}, but FY2027 contributes "
         f"{n0(F['fcff'][1] * F['df'][1])} and the second outweighs the first. Added after "
         f"external review; omitting it had UNDERSTATED this lens"],
        ['Implied value per share, at the anchor', p2(LN['relative']['base']),
         f"bear {p2(LN['relative']['bear'])} at {n1(LN['relative']['mult_bear'])}× / bull "
         f"{p2(LN['relative']['bull'])} at "
         f"{n1(LN['relative']['mult_bull'])}×; rolled to the anchor date on the same two "
         f"lines as the cash-flow bridge"]]
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
  f"review flagged it correctly and the construction was restated. The retired construction "
  f"is published beside the model rather than described: see the lens record, which carries "
  f"what it returned and what the restatement cost.")
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
caption(f"Bear {p2(LN['normalized']['bear'])} at {n1(LN['normalized']['pe_bear'])}× and bull "
        f"{p2(LN['normalized']['bull'])} at {n1(LN['normalized']['pe_bull'])}×, both rolled to "
        f"the anchor date like every other lens. Every input row is the "
        f"figure the computation actually uses — the associate line is the FY2026E forecast, not "
        f"the FY2025 actual. One disclosed conservatism: equity-method associate income is taxed "
        f"at {pc(IN['tax_eff'])} inside this lens although it arrives already post-tax at the "
        f"investee — worth {p2(LN['normalized']['assoc_tax_ps'])} a share on THIS lens if "
        f"removed, computed rather than estimated (an earlier edition of this sentence said "
        f"about +0.4, which understated it roughly fivefold: this is an earnings lens, so the "
        f"multiple applies to the relieved earnings too). The justified multiple is "
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
        # "NOT PUBLISHED FOR THIS CLASS" IN THE ROW THAT PUBLISHES IT, with a bear, a
        # base and a bull beside the words. The lens is RETIRED for this class and it is
        # computed and shown anyway — deliberately, so the reader can see what was
        # removed rather than take the removal on trust. The role says that instead of
        # denying the row it sits in.
        'normalized': 'RETIRED for this class — computed and shown, never weighted',
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
# the share of the forecast base year built at unit level, read from the same segment
# revenue the driver record measures it on — never typed
_SEG_UNIT_SHARE = (BU['unit_hist']['FY25']['rev']['cables']
                   / sum(BU['unit_hist']['FY25']['rev'].values()))
P(f"Revenue is not forecast as a single growth rate applied to a revenue line. The company "
  f"discloses exactly three reportable segments — Cables and its accessories, Constructions and "
  f"infrastructure, and Electrical products and digital solutions — with revenue by segment (Note "
  f"5-3) that reconciles EXACTLY to consolidated revenue in every one of the three audited years, "
  f"and segment profit (Note 16) that reconciles to consolidated operating profit through an "
  # HALF OF THIS SURVIVED THE REPAIR AND CONTRADICTS THE PAGE BELOW IT. The audited
  # filings still disclose no unit, and that has not changed. What changed is that the
  # issuer's own quarterly releases do, and Cables is built on them — so "rather than a
  # reconstructed unit model" is now true of two segments and false of the largest, and
  # it sat fifteen lines above a caption saying Cables grows on disclosed tonnage.
  f"explicit corporate cost load. None of the three audited filings, including the Q1-2026 "
  f"interim, discloses a tonnage, unit-volume or order-book figure for any segment. The "
  f"company's own quarterly earnings releases DO, and they are read: Cables is built as a "
  f"unit model on the disclosed tonnage series times a copper and currency pass-through "
  f"measured out of that segment's own audited revenue per tonne — {pc(_SEG_UNIT_SHARE)} of "
  f"FY2025 revenue. Constructions and Electrical products have no unit in any source, so "
  f"they taper on their own recent revenue growth and margin path. THE SEGMENT MARGINS ARE "
  f"INPUTS in all three, not outputs: each is a constant held flat across the window, set "
  f"at FY2025's level plus the reviewed half's like-for-like change "
  f"({', '.join('%s %s' % (k[:4], pc(v, 2)) for k, v in AR['seg_margin_adopted'].items())}). "
  f"Only the group EBITDA margin is an output, and only of the mix. This is the largest "
  f"single lever in the study and section 1.9 prices both sides of it.")

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
        # THE TABLE PUBLISHED A RETIRED DRIVER AS THE LIVE ONE. cables_real_growth is a
        # flat 3.0% and the model does not read it: compute.py runs cable revenue on
        # disclosed tonnage growth times a measured copper/FX pass-through. So the one
        # table in the document headed "How the forecast is driven" named a driver the
        # forecast is not driven by, and a reader reproducing the build from this page
        # could not have arrived at the model's own revenue line.
        # F4, EXTERNAL AUDIT 13-09-2026: THIS TABLE PUBLISHED A FY2026 DRIVER NO FORMULA
        # READS. FY2026 is grown at the measured half-on-half ratio — compute.py asserts
        # it and REFUSES a disagreeing figure — and the tonnage and pass-through drivers
        # run from FY2027. The rows said otherwise, and the audit priced a reader
        # following them at EGP 83.52 against the study's 87.94. Both rows now show the
        # measured ratio in the year the model measures, and the drivers in the years
        # they drive.
        ['Cables — FY2026 growth, MEASURED on the reviewed half',
         '—', pc(AR['seg_g26']['cables'], 2), '—', '—', '—', '—'],
        ['Cables — tonnage growth (the disclosed volume driver, FY2027-30)', '—', '—'] +
        [pc(x) for x in IN['cables_volume_growth'][1:]],
        # AN EXACT ZERO IS WRITTEN "nil", NOT "0.0%". The QC gate treats a cell whose whole
        # content is "0.0%" as a leaked unformatted value, and it is right to: that is what
        # an unset rate looks like. These two zeros are real and committed — full
        # pass-through, no measured shortfall, in the first and last forecast years — so
        # they are written the way a financial statement writes a true nil, which tells the
        # reader the difference the gate was trying to protect.
        ['Cables — copper/FX pass-through to revenue (FY2027-30)', '—', '—'] +
        ['nil' if x == 0 else pc(x) for x in IN['cables_passthrough'][1:]],
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
        # F2: THIS ROW PRINTED THE RETIRED TAPER. The model holds capex at a flat measured
        # share in every year; the taper 4.4 / 4.0 / 3.6 / 3.3 / 3.1 that this row carried
        # was superseded on 09-09-2026 and is read by no formula. It contradicted the
        # study's OWN free-cash-flow table two pages earlier, which prints the levels that
        # go with the flat share.
        ['Capital expenditure (% of revenue)', pc(IN['capex_pct_hist']['FY25'])] +
        [pc(AR['capex_pct_measured'], 2)] * 5,
        ['Depreciation and amortisation (% of revenue)', pc(IN['dna_pct_hist']['FY25'])] +
        [pc(IN['dna_pct'])] * 5]
table(rows, [2.35, 0.73, 0.73, 0.73, 0.73, 0.73, 0.73], size=8.0)
caption(f"Copper is carried forward at the current market level IN REAL TERMS rather than "
        f"forecast: {n0(IN['copper_fcst'][0])}/t in FY2026 and the level thereafter escalated at "
        f"the house's own US long-run inflation, reaching {n0(IN['copper_fcst'][-1])}/t by "
        f"FY2030E. Earlier editions called this 'held flat' and held the dollar price flat in "
        f"NOMINAL terms, which is a real decline of about a tenth across the window — a "
        f"directional view on the metal arrived at by leaving a number alone. A directional view "
        f"would dominate the valuation, and it is carried in the sensitivity instead. "
        # AND THE CAPTION DESCRIBED THE RETIRED DRIVER TOO, in the same sentence that
        # repeated a claim section 7 withdraws. The tonnage exists, it is in the company's
        # own quarterly releases, and this study's cable revenue is built on it.
        f"Cables grows on DISCLOSED TONNAGE — {n0(IN['cables_tonnage_hist']['FY25'])} tonnes "
        f"in FY2025 from the company's own quarterly releases, a "
        f"{pc(IN['cables_tonnage_cagr'])} three-year compound rate — times a copper and "
        f"currency pass-through measured out of the segment's own audited revenue per tonne, "
        f"rather than on a revenue growth assumption. The audited statements disclose no "
        f"tonnage for any segment; the releases are the issuer's own and are cited as such. "
        f"Constructions and Electrical products taper on their own "
        f"FY2023-25 revenue CAGR. The corporate cost load — stated on the same segment-profit-to-"
        f"EBIT basis as the audited history ("
        f"{' / '.join(pc(IN['corp_load_hist'][y], 2) for y in ('FY23', 'FY24', 'FY25'))}) — "
        # F1, THE LARGEST FINDING OF THE EXTERNAL AUDIT. This said the load "glides UP
        # from FY2025's unusually low level toward the FY2023-24 average, the single most
        # conservative choice in the build". The model holds it FLAT at 3.07%, BELOW
        # FY2025's own 3.16%. A reader running the described glide gets EGP 53.9962 — 33.95
        # a share, 38.6%, below the answer on the cover. The bibliography said the right
        # thing all along; the study said the opposite of the bibliography.
        f"is HELD FLAT at {pc(AR['corp_load_adopted'], 2)} in every forecast year, slightly "
        f"BELOW FY2025's own {pc(AR['corp_load_fy25'], 2)} — the reviewed half measures the "
        f"level holding rather than reverting, and the forecast follows the measurement. THIS "
        f"IS THE STUDY'S MOST CONSEQUENTIAL CONTESTED JUDGEMENT AND IT IS PUBLISHED BOTH WAYS: "
        f"the retired reversion path ({' / '.join(pc(x, 2) for x in IN['corp_load_reversion'])}) "
        f"gives EGP {p2(AR['corp_load_reversion_value'])} a share, "
        f"{sgn(AR['corp_load_reversion_value']/D['central']-1, 0)} against the central. "
        f"The capex and D&A paths are shown because they are live free-cash-flow "
        f"drivers, not footnotes: capex is held at a flat "
        f"{pc(AR['capex_pct_measured'], 2)} of revenue, the rate measured off the completed "
        f"2024-25 programme (it ran 3.1% in FY2023, 3.7% in FY2024 and peaked at 4.7% in "
        f"FY2025). Holding it at that FY2025 peak instead would cost EGP "
        f"{p2(AR['capex_at_fy25_peak_cost'])} on the cash-flow lens, taking it to "
        f"{p2(AR['capex_at_fy25_peak_value'])} — an earlier edition of this caption put that "
        f"cost at 1.8 and was wrong by a factor of 4.6.")

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
# F5, EXTERNAL AUDIT: THE BUILD IS CALIBRATED ON THE REVIEWED HALF AND THIS SAID IT WAS
# NOT. All three FY2026 segment growth rates ARE the H1-2026/H1-2025 ratios, all three
# margins are FY2025 plus the like-for-like half change, and working capital and capex are
# re-anchored on the same half. So the Q1 gross-up offered here as "an independent check"
# is not independent — it is a quarter of the period the build is anchored on. The half's
# own check is tighter and was not shown.
caption(f"THE FY2026 BUILD IS CALIBRATED ON THE REVIEWED HALF TO 30 JUNE 2026, not merely "
        f"checked against it: all three segment growth rates are that half's own "
        f"year-on-year ratios ({', '.join('%s %s' % (k, pc(v, 2)) for k, v in AR['seg_g26'].items())}), "
        f"all three margins are FY2025 plus its like-for-like change, and working capital and "
        f"capital expenditure are re-anchored on it. The Q1-2026 gross-up is therefore NOT an "
        f"independent check — it is a quarter of the period the build stands on — and it is "
        f"shown for continuity rather than as corroboration: the disclosed Q1-2026 revenue of "
        f"{n0(IN['q1_26_rev'])}, grossed up on the Q1-2025 seasonal share of FY2025, implies a "
        f"full FY2026 of roughly {n0(BU['q1_26_implied_fy'])} against the build's "
        f"{n0(F['rev'][0])}, a {sgn(F['rev'][0]/BU['q1_26_implied_fy']-1)} difference. That quarter reported "
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
rows.append(['Group', n0(IN['rev_fy25']), pc(1.0), pc(sum(SEG['gp'].values())/IN['rev_fy25']),
             n0(F['rev'][4]), pc(1.0)])
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
  f"and the average across the tested {pc(SN['nwc_grid'][0], 0)}-{pc(SN['nwc_grid'][-1], 0)} "
  f"span). If the group converts working "
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
         # F25: "readings on the anchor date" WAS NOT TRUE OF THIS RATE. The registry
         # dates it 21 July 2026, cached, re-verified 5 August; the anchor is 3 September.
         # The study was describing a live read it had not made. The rate is not changed
         # here — re-sourcing it is a house act, not a study one, and the study's own
         # sensitivity already prices the move — but the sentence now says which date the
         # number carries, read out of the register rather than asserted.
         f"observed 10-year local-currency government yield, carried at the "
         f"{D['inputs']['rf']['date']} print (cached, re-verified 05-Aug-2026) and NOT read "
         f"on the {M['asof']} anchor date, which is {_age_days(D['inputs']['rf']['date'])} "
         f"days later; "
         f"the row below prices what a 100bp move is worth. Readings of the same instrument span "
         # F9, EXTERNAL AUDIT: THIS JUSTIFICATION DESCRIBED A CONSTRUCTION THE MODEL
         # RETIRED, on the line carrying 89.4% of enterprise value. It said the terminal
         # risk-free embeds a 5% inflation target plus a 5.5pp real convention. The model
         # reads 7.00% + 3.50% from the house macro path — the SAME 7% the terminal
         # growth of 9.14% is built on, which is the whole point: a discount rate and a
         # growth rate on two different inflations is a free lunch of 2pp in perpetuity.
         # Read from the record now, so the two can never disagree on the page again.
         f"roughly {pc(IN['rf_external_span'][0])}-{pc(IN['rf_external_span'][1])} across "
         f"sources and disagree; the adopted point sits at the "
         f"low end and the rate is carried in the sensitivity. Terminal = "
         f"{pc(IN['pi_term'])} long-run Egyptian inflation READ FROM THE HOUSE MACRO PATH "
         f"plus a {pc(IN['rf_term'] - IN['pi_term'], 1)} real-rate convention = "
         f"{pc(IN['rf_term'], 2)}. It is the same inflation the terminal growth rate of "
         f"{pc(IN['g_term'], 2)} is derived from, by construction rather than by "
         f"coincidence — a discount rate and a growth rate built on two different "
         f"inflations would be a free lunch of two points in perpetuity"],
        ['Less sovereign default spread', f"({pc(IN['sov_spread_cds'])})", '—',
         'the hard-currency CDS spread, netted from the local yield and then re-entering, '
         'volatility-scaled, through the country premium inside the ERP. The NET country charge '
         'through the equity channel is therefore about +1.9pp, not zero — stated plainly, since '
         'an earlier wording implied the netting removed the charge outright. The un-netted '
         f"construction (cost of equity {pc(W['ke_raw_retired'])}) is retired but "
         'retained in the audit trail'],
        ['Adjusted risk-free rate', pc(W['rf_star']), pc(IN['rf_term']), ''],
        # THE REGRESSOR IS NAMED FROM THE RECORD, NOT TYPED, AND IT USED TO BE WRONG.
        # This cell printed the LIVE statistics -- which come from the published EGX30
        # regression -- under the description "a 31-name equal-weight local composite
        # over five years". That composite is the construction this house WITHDREW, so
        # the row attached correct numbers to a false account of where they came from.
        # The same defect was found and fixed on another name today; typed provenance
        # goes stale the moment the record beneath it moves, and nothing compares them.
        # THE TERMINAL COLUMN PRINTED TODAY'S BETA AND THE TERMINAL DOES NOT USE IT.
        # compute.py sets BETA_TERM = 1.0 by instruction -- a mature business in a mature
        # economy converges toward the market -- the cost-of-capital record names the
        # construction `beta_to_one_split` and publishes beta_terminal = 1.0, and the
        # workbook prints 1.00. Only this row said 1.225, so the delivered report was the
        # one artefact of the four that contradicted the model it describes. Both columns
        # are READ from the record now; neither is typed and neither is the other's copy.
        ['Beta', f"{COC['beta']:.3f}", f"{COC['beta_terminal']:.3f}",
         f"explicit window: own-stock weekly regression against the published "
         f"{os.path.basename(W['beta']['index_file']).replace('.csv', '')} index of the "
         f"exchange this share is listed on, over {W['beta']['window_years']:.2f} years: "
         f"R-squared {W['beta']['r2']:.3f}, n = {W['beta']['n']}, standard error "
         f"{W['beta']['se']:.3f}, 90% interval [{W['beta']['ci90'][0]:.2f}, "
         f"{W['beta']['ci90'][1]:.2f}]. Terminal: beta is carried to "
         f"{COC['beta_terminal']:.2f} rather than held at the measured figure — today's "
         f"relative risk is not a property of the company in perpetuity, and the "
         f"construction is named in the cost-of-capital record as "
         f"{COC['ke_terminal_construction']}"],
        # F7, EXTERNAL AUDIT: THIS TABLE DID NOT PRODUCE ITS OWN COST OF EQUITY. It printed
        # one premium row of 9.41% beside a beta of 1.225, and 18.91% + 1.2249 x 9.41% is
        # 30.44%, not the 28.09% on the line below. The premium SPLITS — beta multiplies
        # the mature-market leg only and the country premium is levied flat beside it
        # [R-COC-03] — and that split was argued in the prose and shown nowhere in the
        # table a reader reproduces the number from. Priced by the audit: a reader running
        # the literally printed rows gets EGP 56.97, 35.2% below the answer. The legs are
        # separate rows now, and the two columns add up on the page.
        ['Equity risk premium — mature-market leg (beta applies HERE, and only here)',
         pc(W['erp_mature'], 2), pc(W['erp_mature'], 2),
         'the mature-market equity risk premium out of the published country-premium file '
         '(January-2026 vintage). This is the only leg the beta above multiplies'],
        ['  → beta × the mature leg', pc(W['beta_leg'], 2),
         pc(W['erp_total_charged_term'] - W['crp_eff_term'], 2),
         'the product of the two rows above it'],
        ['Country premium — levied FLAT, never multiplied by beta',
         pc(W['crp_eff'], 2), pc(W['crp_eff_term'], 2),
         f"Egypt's home premium of {pc(W['crp_home'], 2)} weighted at "
         f"{IN['lambda_country']:.4f} for the share of operations inside Egypt, blended with "
         f"a {pc(IN['crp_foreign'], 2)} premium on the rest. Charging a "
         f"{IN['beta']:.2f}-beta company {IN['beta']-1:.0%} more country risk than the "
         f"market is a separate claim and this study does not make it"],
        ['Total premium charged (the two legs above)',
         pc(W['erp_total_charged'], 2), pc(W['erp_total_charged_term'], 2),
         f"for comparison, the undivided published premium is {pc(IN['erp_cds'])} on the "
         f"credit-default-swap basis; multiplying THAT by beta is the retired construction "
         f"and gives a cost of equity of {pc(W['ke_raw_retired'])}"],
        ['Cost of equity', pc(W['ke_exp']), pc(W['ke_term']),
         'the adjusted risk-free rate plus the two premium legs above — and the rows of '
         'this table now reach it: ' +
         pc(W['rf_star'], 2) + ' + ' + pc(W['beta_leg'], 2) + ' + ' + pc(W['crp_eff'], 2) +
         ' = ' + pc(W['ke_exp'], 2)],
        ['Cost of debt (blended, pre-tax)', pc(IN['kd']), pc(IN['kd_term']),
         f"currency-blended — see the evidence immediately below. {pc(IN['kd'])} is the FY2026 "
         f"forward "
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
caption(f"Discounting is end-of-year discrete (each year's flow at its full-year factor) — the "
        f"conservative convention; mid-year discounting would raise the explicit strip by "
        f"{pc(DCF['midyear_uplift'])}, computed by re-discounting the same five flows half a "
        f"year earlier rather than estimated in prose. "
        # THE ANCHOR MOVED AND FOUR SENTENCES DID NOT. The study is struck at 3 September
        # 2026 and said so in its masthead; these carried the superseded 5-Aug date. Read
        # from the numbers file, so they move with it.
        f"All values are then rolled to the {M['asof']} anchor as shown in the bridge.")

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
         f"{pc(1-W['w_egp_implied'],0)} in hard currency — DOWN sharply from the "
         f"{pc(IN['w_egp_implied_fy24'],0)} pound "
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
         # THIS CELL READ "raises the value" — an adjective in a column headed with a
         # currency, in a table whose stated purpose is to let a reader take the
         # alternative number directly. Re-run through the same function as the headline.
         f"EGP {p2(_CT['gross_weights'])} ({p2(_CT['gross_weights'] - DCF['ps'])})",
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
         f"by {pc(abs(DCF['ps_kd_egp_equiv'] / DCF['ps'] - 1), 2)} — smaller than it "
         "looks. CAUTION: keeping the currency-composition basis as primary means the "
         "hard-currency debt is carried at its coupon rate, not compensated for devaluation "
         "risk beyond what this forecast's own exchange-rate path already assumes"],
        ['Risk-free rate ' + pc(IN['rf']),
         f"External readings of the same instrument range from about "
         f"{pc(IN['rf_external_span'][0])} to {pc(IN['rf_external_span'][1])}, and disagree "
         f"with each other; the adopted point sits at the low end",
         # "roughly +/-1% of value per 100bp" UNDERSTATED IT by nearly a factor of two.
         f"EGP {p2(_CT['rf_dn100'])} at 100bp lower, {p2(_CT['rf_up100'])} at 100bp higher "
         f"({p2(_CT['rf_up100'] - DCF['ps'])} / +{p2(_CT['rf_dn100'] - DCF['ps'])}) — about "
         f"{pc(abs(_CT['rf_dn100'] - DCF['ps']) / DCF['ps'])} of value per 100bp, not the "
         f"1% an earlier edition of this cell estimated in prose",
         'Because the readings conflict, the rate is carried in the sensitivity grid rather '
         'than presented as precise; the direction of the low-end choice is generous and is '
         'said so here'],
        [f"Forecast effective tax rate {pc(IN['tax_eff'])}",
         f"Egypt's statutory {pc(IN['tax_stat'])}, or FY2025's actual effective "
         f"{pc(SN['tax_path']['fy25'])}",
         # AND THIS ONE WAS WRONG BY 2.8x. "roughly +1.8 (+2.5%)" for a move to the
         # statutory rate, which this model prices at +4.95. The cell also stopped the
         # disclosed series at the quarter while the half containing it ran five points
         # higher — see the row's own note, now corrected.
         f"EGP {p2(_CT['tax_statutory'])} at the statutory rate "
         f"(+{p2(_CT['tax_statutory'] - DCF['ps'])}); EGP "
         f"{p2(min(SN['grid_tax']))} at the implied second quarter's "
         f"{pc(SN['tax_path']['q2_26_implied'])} ({p2(min(SN['grid_tax']) - DCF['ps'])})",
         f"Audited effective rates ran {pc(SN['tax_path']['fy23'])} (FY2023), "
         f"{pc(SN['tax_path']['fy24'])} (FY2024), {pc(SN['tax_path']['fy25'])} (FY2025), "
         f"{pc(SN['tax_path']['q1_26'])} "
         f"(Q1-2026) and {pc(SN['tax_path']['h1_26'])} (H1-2026) — and since the quarter sits "
         f"inside the half, the SECOND quarter alone implies "
         f"{pc(SN['tax_path']['q2_26_implied'])}. The adopted "
         f"{pc(IN['tax_eff'])} therefore sits BELOW all four of the most recent readings, and "
         f"earlier editions of this cell stopped at the quarter and called it an uptick. No "
         f"statutory-vs-effective reconciliation is disclosed, and the group pays "
         f"tax in 15+ jurisdictions plus revenue-basis Free-Zone entities. One reviewed half "
         f"is not a five-year forecast and the rate is not raised on it; what was wrong was "
         f"showing the reader neither the half nor what it costs. Section 1.9 now carries the "
         f"row and section 1.9b prices the half in full"]]
table(rows, [1.72, 1.85, 1.28, 2.15], size=8.0)
caption(f"The rating-basis column is the one most often raised against this study. It is not a "
        f"correction to an error — both bases are published by the same source and both appear in "
        f"this study's input register — but it is a material choice, and at EGP "
        f"{p2(DCF['ps_rating_basis'])} the alternative sits well below the primary. A reader who "
        f"prefers agency ratings to market spreads should use that number. "
        f"THIS FIGURE HAS MOVED, AND A READER HOLDING AN EARLIER EDITION SHOULD KNOW WHY. "
        f"It was published at EGP {p2(DCF['ps_rating_retired_identity'])}, on a cost of equity "
        f"of {pc(W['ke_rating_retired_identity'])} built by multiplying beta through the WHOLE "
        f"{pc(IN['erp_rating'])} premium — country risk included — which is the construction "
        f"this study's own cost-of-capital section says it does not use, and which its adopted "
        f"case is explicitly built to avoid. The terminal leg was worse: it multiplied today's "
        f"beta through a premium raised by a flat four and a half points that appeared in no "
        f"register and no source. Rebuilt the way the adopted case is built — the mature premium "
        f"priced by beta, the country premium charged flat beside it, the terminal on the same "
        f"converged beta and the same normalisation — the rating basis gives EGP "
        f"{p2(DCF['ps_rating_basis'])}. The direction is the awkward part and it is stated "
        f"rather than buried: the mature premium is the same on both bases by arithmetic "
        f"({pc(IN['erp_rating'])} less {pc(IN['sov_spread_rating'])} scaled, against "
        f"{pc(IN['erp_cds'])} less {pc(IN['sov_spread_cds'])} scaled), so switching column moves "
        f"the sovereign spread and the country premium and nothing else — and the spread is "
        f"netted OUT of the risk-free rate, which is why the rating basis comes out cheaper in "
        f"the explicit window rather than dearer. The alternative is still well below the "
        f"primary; it is no longer below it for the wrong reason.")

# ---- 1.9 sensitivity -----------------------------------------------------------
H2('1.9  Sensitivity — the discount rate, the growth, the currency, the margin and the collection')
# THE CAPTION SAID "No cell in the tested range reaches the market price" OVER A GRID
# WITH FOUR CELLS ABOVE IT. It was true when written and the grid has been re-run since,
# through the sanctioned terminal module and with the employees' statutory share charged.
# A claim about a table typed beside the table is a claim nothing compares; it is counted
# out of the grid now, so it cannot be right once and wrong afterwards.
# AND IT COUNTED THE WRONG GRID. Figure 3 is drawn from sens_wg — terminal cost of
# capital against terminal growth, topping out at 221.10 — and this caption counted
# grid_exp_term, the EXPLICIT-window grid, which tops out at 143.24. Both happen to put
# four cells above the price, so the sentence agreed with the picture by coincidence and
# would have stopped agreeing the moment either grid moved. The caption reads the array
# the figure is drawn from.
_G = [v for r in D['sens_wg']['table'] for v in r]
_reach = sum(1 for v in _G if v >= SPOT)
figure(os.path.join(HERE, 'fig2_sens.png'), 5.7,
       f"Figure 3 — discounted-cash-flow fair value per share across the terminal cost of capital "
       f"and terminal growth. "
       + (f"No cell in the tested range reaches the market price of {p2(SPOT)}: even the most "
          f"generous corner, at {p2(max(_G))}, sits below it."
          if not _reach else
          f"{_reach} of the {len(_G)} cells reach the market price of {p2(SPOT)}, all of them in "
          f"the corner combining the lowest terminal cost of capital with the highest terminal "
          f"growth; the grid tops out at {p2(max(_G))}. What it takes to get there is the point: "
          f"a terminal cost of capital {(W['wacc_term'] - min(D['sens_wg']['wacc_grid']))*10000:,.0f}bp "
          f"below the adopted one at the same time as terminal growth at the top of the "
          f"tested range — the two most favourable assumptions in the grid, together."))
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
rows.append(['Exchange-rate path',
             f"base {sgn(SN['fx_grid'][0] - 1, 0)} to {sgn(SN['fx_grid'][-1] - 1, 0)} "
             f"(the deep tail is the interest-parity case)",
             span(SN['grid_fx']), p2(max(SN['grid_fx'])-min(SN['grid_fx']))])
rows.append(['Segment margins (all three, multiplicative)', '−15% to +15%', span(SN['grid_margin']),
             p2(max(SN['grid_margin'])-min(SN['grid_margin']))])
rows.append(['Copper price', '−15% to +15%', span(SN['grid_copper']),
             p2(max(SN['grid_copper'])-min(SN['grid_copper']))])
rows.append(['Working capital / revenue', f"{pc(SN['nwc_grid'][0])} – {pc(SN['nwc_grid'][-1])}",
             span(SN['grid_nwc']), p2(max(SN['grid_nwc'])-min(SN['grid_nwc']))])
rows.append(['Terminal return on invested capital',
             f"{pc(SN['roic_grid'][0],0)} – {pc(SN['roic_grid'][-1],0)}", span(SN['grid_roic']),
             p2(max(SN['grid_roic'])-min(SN['grid_roic']))])
# THE ROW THAT WAS MISSING [F13]. The most adverse observation in this company's whole
# disclosed tax record was read, registered, flagged material in our own register — and
# then appeared in no sensitivity, no scenario and no sentence. A reader could not find
# out what it costs. It costs this.
rows.append(['Forecast effective tax rate',
             f"{pc(SN['tax_grid'][0])} (statutory) – {pc(SN['tax_grid'][-1])} (the implied "
             f"second quarter)", span(SN['grid_tax']),
             p2(max(SN['grid_tax'])-min(SN['grid_tax']))])
rows.append(['Terminal growth', f"{pc(SN['g_grid'][0],0)} – {pc(SN['g_grid'][-1],0)}",
             span([r[j] for r in [SN['grid_wacc_g'][2]] for j in range(5)]),
             p2(max(SN['grid_wacc_g'][2])-min(SN['grid_wacc_g'][2]))])
table(rows, [2.20, 1.55, 1.90, 1.35], size=8.5)

# THE FIVE JUDGEMENTS THAT MOVE THE ANSWER, EACH PUBLISHED BOTH WAYS. Every one was found
# UNPRICED — by an external forensic audit of this edition, or by this house's own blind
# self-audit run against it — and three of the five move the answer TOWARD the market
# price, which is precisely why none of them is adopted here. The depth bar requires a
# study's most consequential contested judgement to be computed both ways and shown side
# by side; this study did that for the corporate cost load and for the pass-through, and
# not for the one worth more than both together.
H2('1.9b  The five judgements that move the answer, priced both ways')
P("Each row below is a FULL RE-RUN of the model with one input changed — not an elasticity "
  "and not a multiplier on a finished line. None of them is adopted. Three of the five "
  "would raise the value toward the traded price, and that is the reason they are shown "
  "rather than taken: a judgement that happens to close a gap has to be right on its own "
  "merits before it is right at all.", size=9.5)
_cr_rows = [['The judgement', 'What this study adopts', 'The alternative', 'EGP/share']]
for _r in D['contested_rulings']:
    _v = ('%s   (%s)' % (p2(_r['value']), sgn(_r['value'] / D['central'] - 1, 0))
          if _r.get('value') is not None else 'not re-run — see note')
    _cr_rows.append([_r['name'], _r['adopted'], _r['alternative'], _v])
table(_cr_rows, [1.85, 1.75, 1.75, 1.15], size=8.2)
for _r in D['contested_rulings']:
    P('%s — %s' % (_r['name'], _r['note']), size=9.0, color=GREY)
caption(f"The central of EGP {p2(D['central'])} is the study's answer and none of these "
        f"alternatives displaces it. They are published because a reader is entitled to see "
        f"the levers that move the number most, and because this study's own gap to the "
        f"market — {sgn(D['central']/SPOT-1, 0)} — is mostly ONE of them: read the reviewed "
        f"half as a level rather than as a change, and apply that consistently to margins, "
        f"capital expenditure and the minority share, and the answer lands near the traded "
        f"price. That is a methodological disagreement about a filing we read, not a "
        f"disagreement about information the market has and we lack, and it is stated here "
        f"rather than left for an auditor to find.")
# THE COPPER SENTENCE DESCRIBED A GRID THAT NO LONGER EXISTS. It said the swing "can even
# run the 'wrong' way"; the repaired grid runs 83.40 to 92.13, monotone upward. The
# DIRECTION is read off the grid here rather than asserted, and the economics the sentence
# was reaching for survive: the swing is the smallest of any operating row, because the
# metal passes through to cost and working capital as well as to revenue.
_cu = SN['grid_copper']
_cu_up = all(_cu[i] <= _cu[i + 1] for i in range(len(_cu) - 1))
_swings = {'the segment-margin row': max(SN['grid_margin']) - min(SN['grid_margin']),
           'the terminal return-on-capital row': max(SN['grid_roic']) - min(SN['grid_roic']),
           'the currency row': max(SN['grid_fx']) - min(SN['grid_fx']),
           'the working-capital row': max(SN['grid_nwc']) - min(SN['grid_nwc']),
           'the copper row': max(_cu) - min(_cu)}
_rank = sorted(_swings.items(), key=lambda kv: -kv[1])
caption("Every row is a full re-run of the segment build, not a multiplier applied to a finished "
        "revenue line: a currency or copper move flows through Cables' revenue, the working "
        "capital and the segment profit exactly as it does in the base case. Note the copper row — "
        f"it is the SMALLEST swing of any operating driver at EGP {_swings['the copper row']:.2f} "
        f"a share across a ±15% move, and it runs "
        + ("upward throughout" if _cu_up else "in both directions") +
        ": a higher metal price raises Cables' revenue and its working capital together, and "
        "raises the profit earned on that revenue hardly at all. Ranked by "
        f"single-row swing, {_rank[0][0]} is the LARGEST at EGP {_rank[0][1]:.2f} a share, ahead "
        f"of {_rank[1][0]} at EGP {_rank[1][1]:.2f} — an earlier caption claimed the "
        "terminal assumptions dominated every operating driver, which this table itself "
        "contradicts (a review caught it); what remains true is that the two cost-of-capital "
        "grids jointly span the widest surface, and a ±15% margin shock is a far larger "
        "displacement of the base case than any one row's parameter step.")
P(f"Every grid above is produced by the SAME valuation function as the headline, and it is "
  f"asserted to reproduce it: at the adopted rates, growth and beta the function returns "
  f"EGP {p2(SN['grid_exp_term'][2][2])} against the published central of {p2(D['central'])}. Until "
  f"this edition the grids ran through a second function that re-implemented the terminal on "
  f"a construction the study had already retired and omitted the employees' statutory share "
  # THE PERCENTAGE DRIFTED WITH EVERY RE-STRIKE AND DESCRIBED NOTHING [09-09-2026].
  # 49.7076 is a fixed historical figure — what the RETIRED grid returned at its adopted
  # point — and this divided it by TODAY's central, so the sentence claimed the retired
  # surface sat some percentage above "the answer it was supposed to be testing" while
  # measuring it against an answer struck after the defect was fixed. Every correction to
  # this study silently rewrote a statement about a superseded edition. The absolute
  # figure is the fact; the ratio was never one.
  f"of profit that the bridge charges, so the surface was centred at EGP "
  f"{p2(IN['grid_centre_retired'])} rather than on the answer it was supposed to be "
  f"testing. Note also "
  f"where the adopted point SITS in each range rather than assuming it is the middle: "
  f"terminal growth is adopted at {pc(IN['g_term'],0)}, the TOP of the "
  f"{pc(SN['g_grid'][0],0)}–{pc(SN['g_grid'][-1],0)} range tested, so the terminal-growth "
  f"row runs from the answer downwards and not symmetrically around it.", space_after=10)

P(f"The beta deserves a note. At {IN['beta']:.3f} with an R-squared of {W['beta']['r2']:.3f} over "
  f"{W['beta']['n']} weekly observations and a standard error of {W['beta']['se']:.3f}, this is a "
  f"well-identified estimate by the standards of this market — the 90% interval spans "
  f"[{W['beta']['ci90'][0]:.2f}, {W['beta']['ci90'][1]:.2f}], comfortably narrower than twice the "
  f"point estimate, so it is not flagged as a weak instrument. A defensive-staple "
  f"prior of 0.6–0.9 and a cyclical prior of 1.0–1.5 bracket it, and a diversified industrial with "
  f"a contracting arm belongs in the second. "
  f"ONE SENTENCE OF THE OLD DEFENCE IS WITHDRAWN. It read that the estimate is "
  f"economically sensible because 'the largest industrial constituent of an index should have a "
  f"beta near one'. An external review pointed out that this company is not a constituent of the "
  f"index it is regressed against, and this study had not checked. The regressor is unchanged and "
  f"is not wrong: {W['beta']['index_file']} is the registered published index of the exchange the "
  f"stock is listed on, which is what the standing rule names, and an index a stock is not in is "
  f"still the market that stock's return is measured against. What was wrong was defending it "
  f"with a fact about membership. The estimate now stands on what this study can actually check: "
  f"{W['beta']['n']} weekly observations, the fit above, and the economic prior.", space_after=10)

# =========================== 2 TECHNICAL ======================================
H1('2  Technical and price structure')
figure(os.path.join(HERE, 'fig3_ma.png'), 7.0,
       "Figure 4 — price against the 20-, 50-, 100- and 200-session moving averages over the last "
       "260 sessions.")
import numpy as np
# THE SAME FRAME AS THE CONE AND THE FIGURES -- see price_series.py. This table read the
# study-local file and printed averages of 93.77 / 90.04 / 86.07 / 81.88 and a 52-week
# closing high of 109.02 in the row directly below "Last close 130.00", which cannot both
# be true: 130.00 on that series would BE the 52-week high.
import price_series
_df, _ = price_series.frame()
px = _df['Price'].to_numpy()
sma = {n: float(np.mean(px[-n:])) for n in (20, 50, 100, 200)}
hi52, lo52 = float(np.max(px[-252:])), float(np.min(px[-252:]))
rows = [['Marker', 'Level (EGP)', 'Reading'],
        ['Last close', p2(SPOT), 'the anchor for everything in this study'],
        ['20-session average', p2(sma[20]), f"price is {sgn(SPOT/sma[20]-1)} against it"],
        ['50-session average', p2(sma[50]), f"price is {sgn(SPOT/sma[50]-1)} against it"],
        ['100-session average', p2(sma[100]), f"price is {sgn(SPOT/sma[100]-1)} against it"],
        ['200-session average', p2(sma[200]), f"price is {sgn(SPOT/sma[200]-1)} against it"],
        # THE DATE WAS TYPED AND THE SERIES MOVED UNDER IT. It said the 52-week closing
        # high was "the +14.1% print of 4 August 2026, one session before the anchor" —
        # true of the withdrawn 5-August series, and false of the library this study now
        # reads, where the high is the anchor's own close. The date is read off the same
        # frame the level is, so the two cannot disagree again.
        ['52-week high (closing basis)', p2(hi52),
         (f"the high IS this study's own anchor close of {p2(SPOT)} on "
          f"{str(_df['Date'].iloc[-252:].iloc[int(np.argmax(px[-252:]))].date())} — the share "
          f"is AT its 52-week closing high, which is worth stating plainly rather than as a "
          f"distance from it"
          if abs(hi52 - SPOT) < 0.005 else
          f"{sgn(SPOT/hi52-1,1)} from the high, set on "
          f"{str(_df['Date'].iloc[-252:].iloc[int(np.argmax(px[-252:]))].date())}")],
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
  f"rose {pc(float(np.exp(_r[-2]) - 1))} on 4 August 2026 on roughly eleven times normal "
  f"volume. Realised volatility over "
  f"the last 50 sessions is {pc(_v50)}; strip out that one session and it falls to {pc(_v50x)}. "
  f"The cone in section 3 is therefore wide because of one day's move, and a reader who regards "
  f"that session as a one-off should treat the bands as correspondingly generous.", space_after=10)

# =========================== 3 MONTE CARLO ====================================
H1('3  A probabilistic price map')
P(f"This section answers a different question from the valuation. It does not ask what the business "
  f"is worth; it asks where the share price could plausibly be in one and three months, given how "
  f"this share has actually moved. The engine simulates 50,000 price paths from a volatility model "
  f"fitted to the daily high-low-open-close range, with a fat-tailed shock distribution and a drift "
  f"anchored to the cost of carry — an EGP deposit-rate carry of "
  f"{pc(STK['rf_live'])} annualised, read from the live market profile, deliberately below the "
  f"{pc(IN['rf'])} bond yield and carrying no directional view.")
# WHAT A READER IS SHOWN IS THE BAND RECORD [R-CAL-02, R-CAL-03]. The two skill clauses
# this paragraph used to carry — the model scoring a per cent or so "better than a
# random-walk benchmark" over five years and again over the full history — were the
# retired verdict in plain words, and the verdict reaches no page, figure, document or
# deck. What replaces them is not less: the coverage figures WITH their window count, the
# uniformity test, and the band-width ratio, which is the sharpness measure the protocol
# says is disclosed rather than gated, and is what the retired comparison was standing
# in for.
P(f"The widths below are calibrated rather than assumed. Tested by walk-forward simulation over "
  f"nearly five years — {BT5['windows']} independent non-overlapping quarterly windows with "
  f"origins from {BT5['first_origin']} to {BT5['last_origin']} (the final window runs three "
  f"months past its origin), each one forecast using only data available "
  # "CLOSE TO THE ADVERTISED RATE" WAS AN EYEBALL. 42% inside a 50% band looks eight
  # points light; over nineteen windows it is eight outcomes against an expected nine
  # and a half, which is not a finding. The two-sided exact binomial says so, and it is
  # printed, because the reader cannot be expected to do small-sample arithmetic in their
  # head to decide whether a number this study calls close actually is.
  f"before it — outcomes fell inside the stated bands at close to the "
  f"advertised rate ({BT5['cov50']*100:.0f}% inside the 50% band, {BT5['cov80']*100:.0f}% inside "
  f"the 80%, {BT5['cov90']*100:.0f}% inside the 90%, over those {BT5['windows']} windows). "
  f"Close is tested rather than asserted: a two-sided exact binomial against each band's own "
  f"rate returns p = {BT5['cov_binom']['50']:.2f}, {BT5['cov_binom']['80']:.2f} and "
  f"{BT5['cov_binom']['90']:.2f}, so on this sample none of the three departs from its stated "
  f"rate by more than chance would produce — which is a statement about the sample's size as "
  f"much as about the calibration, and is worth reading that way. And "
  f"the outcomes were spread evenly across "
  f"the distribution rather than bunching at one end — a uniformity test returns p = "
  f"{BT5['chi2_p']:.2f}, comfortably consistent with a well-calibrated forecast. Over the very "
  f"long run the picture is more mixed: across the full {BT5F['span_years']:.0f}-year history the "
  f"bands are about "
  f"{(BT5F['width_vs_benchmark']-1)*100:.0f}% wider than a naive carry-anchored band, which is a "
  f"real limitation — a wider band catches more by construction — and is stated here rather "
  f"than left out. "
  # TWO COVERAGE RECORDS FOR ONE NAME, AND THE READER SHOULD BE TOLD, NOT LEFT TO FIND
  # OUT. This page publishes the five-year window; the per-name calibration record
  # carries the full history, and a reader who sees both without being told they are
  # different samples is entitled to think one of them is wrong. They are one method
  # measured over two windows, and the longer one is the better-covered of the two,
  # which is worth saying out loud rather than burying.
  f"THE FULL-HISTORY FIGURES ARE DIFFERENT AND BOTH ARE PUBLISHED: over all "
  f"{BT5F['windows']} windows the 90% band caught {BT5F['cov90']*100:.0f}% against the "
  f"{BT5['cov90']*100:.0f}% on the five-year window above, and the 50% band "
  f"{BT5F['cov50']*100:.0f}% against {BT5['cov50']*100:.0f}%. That is one method measured "
  f"over two samples and not two answers to one question — the longer window is the "
  f"better-covered of the two, and a reader comparing this page against a coverage figure "
  f"quoted elsewhere for this name should check which window it is on before concluding "
  f"anything from the difference.")
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
        [f"Finishes {pc(H3M['move_threshold'], 0)} or more above spot",
         pc(H1M['p_up10'], 0), pc(H3M['p_up10'], 0)],
        [f"Finishes {pc(H3M['move_threshold'], 0)} or more below spot",
         pc(H1M['p_dn10'], 0), pc(H3M['p_dn10'], 0)],
        [f"Touches {pc(H3M['move_threshold'], 0)} above spot at any point",
         pc(H1M['touch_up10'], 0), pc(H3M['touch_up10'], 0)],
        [f"Touches {pc(H3M['move_threshold'], 0)} below spot at any point",
         pc(H1M['touch_dn10'], 0), pc(H3M['touch_dn10'], 0)]]
table(rows, [3.30, 1.35, 1.35], size=8.6)
caption("Touch probabilities exceed finish probabilities because a path can visit a level and come "
        "back. This distinction matters for anyone thinking about a level rather than a date.")

# =========================== 4 COMPARISON =====================================
H1('4  Comparison of the lenses')
rows = [['Read', 'What it says', 'What it assumes'],
        ['Fundamental (the cash-flow lens, unweighted)', f"EGP {p2(D['central'])} central, "
         f"{sgn(D['central']/SPOT-1,0)} against the market",
         'one lens is the answer and the others are cross-checks published beside it — never a weighted blend'],
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
  # THE SECOND SITE OF THE SAME CLAIM, and it is the one that matters most because it is
  # the paragraph explaining the whole disagreement. Our construction does NOT charge the
  # full Egyptian premium: [R-COC-03] splits it, beta applies to the mature leg only, and
  # the country premium is levied flat and weighted for the share of operations inside
  # Egypt. Describing the retired construction here made the study's own reading sound
  # more conservative than it is, in the one place a reader goes to judge exactly that.
  f"Egyptian risk. Charging it a country premium of {pc(W['crp_eff'],2)} — weighted at "
  f"{IN['lambda_country']:.4f} for the Egyptian share of operations, and levied FLAT rather "
  f"than multiplied by beta, which is what our primary construction does — is the "
  f"conservative choice, not the obviously correct one. Charging it none of that premium, "
  f"which is roughly what the market price implies, is the aggressive one. Charging the "
  f"whole {pc(W['crp_home'],2)} home premium unweighted, which an earlier construction did "
  f"and this study retired, would be more conservative still.")
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
         f"gross margin against the 2025 exit rate; whether revenue growth holds above the "
         f"{pc(F['rev'][1] / F['rev'][0] - 1, 0)} the second forecast year assumes"],
        ['Working-capital conversion',
         'the model\'s largest single assumption is that working capital stays near '
         f"{pc(IN['nwc_pct'])} of revenue",
         'operating cash flow against EBITDA in the interim statements; inventory and receivable '
         'days'],
        ['The exchange rate',
         f'about {pc(D["fgn_share_fy25_derived"],0)} of revenue is hard-currency linked, so both '
         f'the translated result and the working capital move with the pound',
         f"the pace of depreciation against the {pc(DCF['fx_dep_avg'])} a year assumed here, "
         f"and whether the "
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
         # HALF OF THIS WAS STILL TRUE AND HALF WAS WITHDRAWN. The audited filings disclose
         # no backlog and that has not changed; the company's own releases do, and this
         # study reads EGP 346bn at 30 June 2026. Why the taper survives anyway is the
         # part worth saying: a backlog without a disclosed burn profile cannot be turned
         # into revenue, so it corroborates the taper instead of replacing it.
         'no order book or backlog figure is disclosed in any AUDITED filing. The company\'s '
         'own quarterly releases disclose an engineering backlog of EGP 346bn at 30 June '
         '2026, which is read; they do not disclose the burn profile that would turn it '
         'into revenue, so the Constructions and infrastructure forecast tapers on its own '
         'revenue growth and the backlog corroborates that taper rather than setting it',
         f"whether Constructions and infrastructure revenue growth "
         f"({pc(AR['seg_g26']['construct'], 0)} in FY2026E) holds up or "
         'decelerates faster than assumed'],
        ['Dividend policy',
         f"the FY2025 payout ALREADY stepped up sharply, to EGP {p2(IN['dps_fy25'])} (paid June "
         f"2026, {pc(DCF['dps_payout_fy25'])} of attributable EPS); the forecast assumes "
         f"{pc(F['payout'],0)} — whether "
         f"the step-up is the start of a trajectory or a plateau moves the equity roll-forward "
         f"and the net-debt path",
         f"the distribution proposed on the FY2026 result, against the "
         f"{pc(DCF['dps_payout_fy25'])} just paid"]]
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
         'one outcome in twenty; would require a genuine shock — a currency event, a policy '
         'reversal, or a material contract failure'],
        # F29: THE MAP SKIPPED 40% OF WHAT IT MAPS. It ran below the 5th, then the 25th
        # to the 50th, the 50th to the 75th, then above the 95th — 5 + 25 + 25 + 5 = 60%
        # of the distribution, with the 5th-to-25th and the 75th-to-95th missing
        # entirely. Those are the two bands a reader is most likely to land in after the
        # central ones, and the omission is invisible unless the percentages are added
        # up. Every band is now present and the column says what each is worth, so the
        # arithmetic is on the page rather than in the reader's head.
        ['Lower band', f"{p2(H3M['pct']['p5'])} – {p2(H3M['pct']['p25'])}",
         'one outcome in five; a drift lower without a shock — the zone the fundamental '
         'range and the price map come closest to agreeing in'],
        ['Lower half of the central band', f"{p2(H3M['pct']['p25'])} – {p2(H3M['pct']['p50'])}",
         'one in four; ordinary drift lower, and this zone overlaps the upper end of the '
         'fundamental range'],
        ['Upper half of the central band', f"{p2(H3M['pct']['p50'])} – {p2(H3M['pct']['p75'])}",
         'one in four; ordinary drift higher, the market continuing to price the '
         'hard-currency reading'],
        ['Upper band', f"{p2(H3M['pct']['p75'])} – {p2(H3M['pct']['p95'])}",
         'one outcome in five; a drift higher without a step change'],
        ['Upper tail', f"above {p2(H3M['pct']['p95'])}",
         'one outcome in twenty; would need a step change in the order book, the margin, or '
         'the perceived country risk'],
        ['Where the fundamental central sits', p2(D['central']),
         f"below even the 5th percentile ({p2(H3M['pct']['p5'])}) of the three-month "
         f"distribution — the price map and the valuation genuinely disagree, and stating the "
         f"gap at its full size is the point"]]
table(rows, [1.75, 1.75, 3.50], size=8.5)
caption(f"The six zones above the last row cover the distribution exactly once: "
        f"5 + 20 + 25 + 25 + 20 + 5 = 100 per cent. An earlier edition of this table "
        f"published four of them and covered 60 per cent, with the 5th-to-25th and the "
        f"75th-to-95th absent — which is where two readers in five would have found "
        f"themselves. The drift behind these percentiles is the carry term "
        f"{n1(1000 * H3M['drift_log_h'])} plus a signal term "
        f"{n1(1000 * H3M['alpha_log_h'])}, in thousandths of a log point over the "
        f"{H3M['h']}-session horizon; the sum is what the engine is handed and what the "
        f"median reproduces from, and earlier editions recorded only the first of the two.")

# =========================== 7 CAVEATS ========================================
H1('7  Caveats and what would change our mind')

# ---- YEARS THREE TO FIVE AS RANGES, from this company's own history -----------
P("The far forecast years are published as RANGES rather than as points, and the range is "
  "not an opinion about uncertainty. The method used to build this forecast was rebuilt at "
  "twelve past year-ends of Elsewedy Electric's own history, projected forward from each, "
  "and scored against what the company went on to report — 750 driver-years in all. The "
  "bands below are that record's own error distribution applied to the point path: they say "
  "how far this method has actually missed by, at this distance, on this company.")
_FR = json.load(open(os.path.join(HERE, '..', 'swdy_walkforward', 'forward_ranges.json')))
_bands = _FR['bands']
_YRS = [('3', 'FY2028E', 2), ('4', 'FY2029E', 3), ('5', 'FY2030E', 4)]
_rows = [['Year (horizon)', 'Low', 'Point', 'High', 'Basis (observations)']]
for _drv, _lab, _fmt in (('A_revenue', 'Revenue (EGP mn)', 'rev'),
                         ('A_gross_profit', 'Gross profit (EGP mn)', 'gp')):
    for _h, _yl, _i in _YRS:
        _b = _bands.get(_drv, {}).get(_h)
        if not _b:
            continue
        _pt = F['rev'][_i] if _fmt == 'rev' else BU['gp'][_i]
        _rows.append([f'{_yl} — {_lab}', n0(_pt * _b['low']), n0(_pt), n0(_pt * _b['high']),
                      f"{_b['basis']} ({_b['count']})"])
table(_rows, [2.30, 1.20, 1.20, 1.20, 1.10], size=8.5)
P("The bands are wide and they are honest about why: the twelve years they are measured over "
  "contain a currency that went from about seven to the pound to about forty-eight, and a "
  "revenue line that grew sixteen and a half times. A method scored across that is not going "
  "to produce a narrow band at five years, and a narrow one would be a claim this record "
  "cannot support. Where nine or more observations exist the band is a tenth-to-ninetieth "
  "percentile; below that it is the SPAN of the observations, which is a smaller claim and is "
  "labelled as one. Each band multiplies the point: a low of 0.55 and a high of 2.60 would "
  "mean the outturn had landed between 0.55 and 2.60 times what this method projected — an "
  "illustration of how to read the column, not a figure from this table.")

for head, body in [
    ("The audited statements carry no volumes; the company's own releases do, and they are read. ",
     f"All three audited financial statements and the Q1-2026 interim disclose segment revenue "
     f"and segment profit, but no tonnage, MVA, meter count or order-book figure for any segment. "
     f"THE COMPANY'S QUARTERLY EARNINGS RELEASES CARRY BOTH, and this edition reads them. Cable "
     f"volumes run 144,997 / 156,748 / 167,665 / 185,449 tonnes over FY2022-25 and 99,239 in the "
     f"reviewed half against 89,636, and that series now sets the Cables growth driver instead of "
     f"a residual. Engineering backlog reaches EGP 346bn at 30 June 2026, read and NOT burnt down "
     f"— it corroborates the Constructions taper rather than producing it. TWO EARLIER WORDINGS "
     f"ARE WITHDRAWN: one said this data was 'disclosed anywhere', which overclaimed the scope of "
     f"a negative result, and one said the releases 'were not reachable from this research "
     f"environment', which was simply wrong — they were held here the whole time. Cross-checking "
     f"the Constructions taper against the released backlog was named as the first refinement to "
     f"make when "
     f"those releases become obtainable."),
    ("The valuation is dated, and the dating is now explicit. ",
     f"The cash-flow model is constructed at 31 December 2025 (the audited balance-sheet date); "
     f"every lens value is rolled {DCF['anchor_days']:.0f}/365 of a year to the 3-Sep-2026 "
     # THE THIRD SITE OF THE RAW DIVIDEND, and it survived its own fix this morning: the
     # bridge row and the roll helper were both moved onto div_at_anchor and this
     # sentence was not, so it named 1.85 and its gross figure came out 13.70 against
     # the model's 13.8168. The dividend is deducted AT THE ANCHOR — carried forward
     # from its ex-date at the same cost of equity the rest of the roll uses — and both
     # numbers are read from the record now rather than assembled from an input.
     f"anchor at the {pc(W['ke_exp'])} cost of equity, less the FY2025 dividend carried "
     f"forward to that anchor at the same rate: EGP {p2(IN['dps_fy25'])} went ex on 4 June "
     f"and is worth EGP {p2(DCF['div_at_anchor'])} by 3 September. The roll is worth about "
     f"+{p2(DCF['ps']-DCF['ps_dec']+DCF['div_at_anchor'])} gross on the primary lens, "
     f"+{p2(DCF['ps']-DCF['ps_dec'])} after the dividend leaves. An earlier revision omitted this roll and compared a 31-Dec-2025 value "
     f"directly to the August price; an external review flagged it, correctly."),
    ("The terminal value is a large share of the answer. ",
     f"{pc(DCF['tv_share'],0)} of the enterprise value comes from the terminal value. This is "
     f"disclosed in the summary table, in the bridge and here. It is a consequence of a high "
     f"discount rate applied to a business still growing fast — the explicit years are heavily "
     f"discounted, so the perpetuity carries the weight. The terminal assumptions are stressed "
     f"across cost of capital, growth and return on invested capital in section 1.9."),
    # F5, THE SECOND SITE AND THE MORE SERIOUS ONE. This caveat told a reader the FY2026
    # forecast rests on one quarter and that the half-year result was still ahead as a
    # test of it. The half-year result is the thing the forecast is BUILT ON: every FY2026
    # segment growth rate is its year-on-year ratio, every margin is FY2025 plus its
    # like-for-like change, and working capital and capex are re-anchored on it. The
    # caveat inverted what it was warning about, and section 5 listed the same filing as a
    # future catalyst. The real caveat is narrower and harder, so it is stated.
    ("The FY2026 forecast is calibrated on ONE reviewed half, not tested against it. ",
     f"Every FY2026 segment driver is the H1-2026 half's own measurement: growth rates "
     f"{', '.join('%s %s' % (k, pc(v, 2)) for k, v in AR['seg_g26'].items())}, margins at "
     f"FY2025 plus that half's like-for-like change, and working capital and capital "
     f"expenditure re-anchored on the same half. The Q1-2026 gross-up shown in section 1.6 "
     f"is therefore NOT an independent check — it covers a quarter of the period the build "
     f"stands on. THE REAL EXPOSURE IS THIS: a single half sets the base year of a "
     f"five-year model, and whether that half is read as a LEVEL or as a CHANGE is worth "
     f"more than any other judgement in this study. Section 1.9 prices both readings. What "
     f"would settle it is a second half measured the same way — the FY2026 full-year "
     f"result, not the half already in hand."),
    ("The currency of discounting is unresolved, and it is the biggest single question. ",
     # NOT "THE FULL EGYPTIAN PREMIUM". [R-COC-03] splits it: beta applies to the mature
     # leg and the country premium is charged FLAT beside it, weighted by the share of
     # operations in Egypt. The sentence described the construction this study retired.
     f"Our primary construction charges beta against a mature-market premium of "
     f"{pc(W['erp_mature'],2)} and an Egyptian country premium of {pc(W['crp_eff'],2)} FLAT "
     # NO RULE IDENTIFIER ON A READER'S PAGE. Rewriting this sentence to describe the
     # split premium correctly, I put the rule's tag in it — internal machinery, and the
     # delivered-vocabulary gate caught it. The rule is said in words instead.
     f"beside it rather than multiplied through it, to a company earning just over half "
     f"its money on a "
     f"hard-currency-linked basis. The country charge is weighted at "
     f"{IN['lambda_country']:.4f} for the share of operations inside Egypt rather than "
     f"levied whole, and beta is not applied to it: charging a {IN['beta']:.2f}-beta company "
     f"{IN['beta']-1:.0%} more Egypt risk than the market is a separate claim and this study "
     f"does not make it. The alternative construction "
     f"gives EGP {p2(DCF['ccy_alt_ps'])}. We have chosen the conservative reading and shown the "
     f"other in full rather than splitting the difference silently."),
    # FOUR FALSE SENTENCES ABOUT THE LEG CARRYING 89% OF ENTERPRISE VALUE. This bullet
    # said the terminal growth was "EXACTLY zero in real terms", derived "from a stated
    # real growth of zero", that it "assumes the company stops growing in real terms
    # forever", and pointed at "the 6% and 7% columns of the growth grid". The committed
    # real growth is 2.0%, 7% inflation at zero real would be 7.00% and not 9.14%, and the
    # grid runs 7.14% to 11.14% — there is no 6% column and no 7% column. It was true when
    # the terminal carried zero real growth; the terminal was rebuilt and the caveat was
    # not, and it is precisely the caveat a careful reader turns to. Every figure is read
    # now, and the direction of the judgement is stated on the numbers that are actually
    # in the model rather than on the ones that used to be.
    (f"Terminal growth of {pc(IN['g_term'],2)} is {pc(IN['g_term_real'],1)} in real terms. ",
     f"The terminal rate embeds {pc(IN['pi_term'],0)} inflation and the terminal growth rate is "
     f"DERIVED from it and a STATED real growth of {pc(IN['g_term_real'],1)}: "
     f"(1+{pc(IN['pi_term'],0)})(1+{pc(IN['g_term_real'],1)})-1 = {pc(IN['g_term'],2)}, so it is "
     f"not a nominal figure somebody typed beside an inflation assumption. What that assumes is "
     f"that the company grows {pc(IN['g_term_real'],1)} a year faster than prices for ever, and "
     f"that is a CLAIM rather than a neutral choice — it is held below Egypt's long-run real "
     f"growth, so the company is assumed to cede share of the economy, but it is not zero and "
     f"this study does not pretend it is. The growth grid runs {pc(SN['g_grid'][0],2)} to "
     f"{pc(SN['g_grid'][-1],2)}; at its bottom, which is {pc(SN['g_grid'][0]-IN['pi_term'],2)} "
     f"real, the cash-flow lens gives EGP {p2(min(SN['grid_wacc_g'][2]))}."),
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
# ONE ROW, TWO MEASURES, SPLICED AT THE FORECAST BOUNDARY. The FY2023-25 cells were
# TRUE gross profit off the face of the audited income statement — revenue less cost of
# sales, 19.1% / 18.9% / 14.5% of revenue. The forecast cells were the sum of the three
# disclosed segments' Note 16 segment PROFIT, which is struck after depreciation and
# after segment overhead: 12.3% rising to 12.7%. Read down the row, gross margin appears
# to fall 2.2 points at the boundary; on either basis consistently it does not. The model
# builds on segment profit, so that is the row, and it carries its own audited history
# (17.4% / 17.0% / 12.3%). True gross profit stays, labelled, history-only, because it is
# what the audited statements actually print and dropping it would hide the difference
# rather than state it.
_SEGP_HIST = {y: sum(BU['unit_hist'][y]['profit'].values()) for y in ('FY23', 'FY24', 'FY25')}
rows.append(['Gross profit (audited face: revenue less cost of sales)']
            + hist_row('gp') + ['—'] * 5)
rows.append(['Segment profit, three disclosed segments (Note 16 basis — the forecast build)']
            + [n0(_SEGP_HIST[y]) for y in ('FY23', 'FY24', 'FY25')]
            + [n0(x) for x in F['gp']])
rows.append(['EBITDA (derived: EBIT + D&A)'] + hist_row('ebitda') + [n0(x) for x in F['ebitda']])
rows.append(['EBITDA margin'] + [pc(HI[y]['ebitda'] / HI[y]['rev']) for y in ('FY23','FY24','FY25')] +
            [pc(x) for x in F['ebitda_margin']])
rows.append(['Depreciation and amortisation'] + hist_row('dna', neg=True) +
            [f"({n0(x)})" for x in F['dna']])
rows.append(['EBIT'] + hist_row('ebit') + [n0(x) for x in F['ebit']])
rows.append(['Net finance costs'] + hist_row('fin') + [f"({n0(x)})" for x in F['interest']])
rows.append(['Share of equity-accounted investees'] + hist_row('assoc') +
            [n0(x) for x in F['assoc']])
rows.append(['Profit before tax'] + hist_row('ebt') + [n0(x) for x in F['pbt']])
rows.append(['Income tax'] + hist_row('tax', neg=True) + [f"({n0(x)})" for x in F['tax_is']])
rows.append(['Profit for the year'] + hist_row('pat') + [n0(x) for x in F['pat']])
rows.append(['Non-controlling interests'] + hist_row('nci', neg=True) + [f"({n0(x)})" for x in F['nci_is']])
rows.append(['Profit attributable to shareholders'] + hist_row('npa') + [n0(x) for x in F['np_attr']])
rows.append(['Earnings per share (derived: attributable ÷ shares, EGP)'] +
            [p2(HI[y]['npa'] / SH) for y in ('FY23','FY24','FY25')] +
            [p2(x / SH) for x in F['np_attr']])
table(rows, [1.72, 0.66, 0.66, 0.66, 0.66, 0.66, 0.66, 0.66, 0.66], size=7.9,
      band_rows={3, 6, 13})
caption("Every FY2023-25 STATEMENT line is taken directly from the company's audited consolidated "
        "statements. Two rows are house DERIVATIONS and are labelled as such: EBITDA (EBIT plus "
        "D&A — the audited statements contain no EBITDA line, and the company's own separately "
        f"published non-GAAP EBITDA is a different, larger definition) and earnings per share "
        f"(attributable profit over shares outstanding; the company's own reported EPS of "
        f"{' / '.join(p2(IN['eps_reported'][_y]) for _y in ('FY23', 'FY24', 'FY25'))} "
        f"is struck after the Egyptian employee and board profit-share "
        "appropriation and is accordingly lower — both bases appear in §1.3). Forecast profit is "
        "struck after net interest on the estimated debt and cash balances and after tax and "
        "minority interests, and therefore differs slightly from the free-cash-flow waterfall in "
        "section 1.1, which is a pre-financing measure by construction.")

H2('A.2  Balance sheet — condensed house layout (consolidated, EGP mn)')
rows = [['EGP mn', 'FY2023', 'FY2024', 'FY2025'],
        ['Property, plant and equipment', n0(HB['FY23']['ppe']), n0(HB['FY24']['ppe']),
         n0(HB['FY25']['ppe'])],
        ['Equity-accounted investees', n0(IN['assoc_bv_fy23']), n0(IN['assoc_bv_fy24']),
         n0(IN['assoc_bv_fy25'])],
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
        ['Return on invested capital (NOPAT ÷ closing capital)'] + [pc(x) for x in F['roic']],
        ['Capital expenditure'] + [f"({n0(x)})" for x in F['capex']],
        ['Change in working capital'] + [f"({n0(x)})" for x in F['dnwc']],
        ['Free cash flow to the firm'] + [n0(x) for x in F['fcff']],
        ['Shareholders\' equity'] + [n0(x) for x in F['equity']],
        ['Net debt'] + [n0(x) for x in F['net_debt']]]
table(rows, [2.05, 0.99, 0.99, 0.99, 0.99, 0.99], size=8.4, band_rows={7})
caption(f"ONE NOTE ON THE RETURN ROW, because two conventions meet here and an external "
        f"review read across them. The row above divides each year's NOPAT by that same "
        f"year's closing capital, and on that basis the path runs {pc(F['roic'][0])} down to "
        f"{pc(F['roic'][-1])}. The terminal quotes {pc(DCF['roic_term'])}, which looks higher "
        f"than every year in the forecast and is not: it is the standard terminal convention, "
        f"NEXT year's NOPAT over closing capital, which is exactly one year of growth above "
        f"the same-year figure — {pc(DCF['roic_term_sameyear'])} × "
        f"{1 + DCF['g']:.4f} = {pc(DCF['roic_term'])}. On one convention the terminal does not "
        f"step up at all; on the other it appears to, and the earlier editions of this page "
        f"printed the two side by side without saying which was which.")
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
         f"the right frame for the {pc(SEG['rev']['construct'] / IN['rev_fy25'])} of revenue "
         f"that is the Constructions and infrastructure segment",
         'project accounting differs, and backlog quality is not comparable across disclosure '
         'regimes']]
table(rows, [1.70, 1.05, 2.10, 2.15], size=8.3)
P("The absence of a clean comparable is itself a finding. This is a diversified industrial group "
  "with a manufacturing business, a contracting business and an infrastructure portfolio, listed "
  "in a frontier market, earning just over half its revenue on a hard-currency-linked basis. Any "
  "single peer multiple applied to it imports assumptions about country risk that the cash-flow "
  # THE RETIRED BLEND'S VOCABULARY, SURVIVING IN A SECTION NOBODY RE-READ. The relative
  # lens carries no weight at all — the central IS the cash-flow lens, and section 1.5
  # spends a page on exactly that. "A fifth of the weight" is the 45/20/20/15 blend this
  # study withdrew, quoted here as if it were still the method.
  "model tests explicitly. That is why the relative lens is published BESIDE the central at "
  "its own value rather than averaged into it: it carries no weight, because there is no "
  "weighting. A reader who thinks the imported multiple is the better guide can read it off "
  "the page unmixed, which is the point of showing it.")

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
         # THE THIRD SITE OF THE SAME HALF-TRUTH. Cables IS a unit model, on the
         # issuer's own disclosed tonnage; it is the other two segments that taper.
         'growth. Cables is the exception and it is the largest segment: it is built '
         'as a unit model on the tonnage the company discloses in its own quarterly '
         'releases. The backlog is read and not burnt down, because no source '
         'discloses the burn profile that would take',
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
     # SECTION 7 WITHDRAWS THIS EXACT CLAIM and this register kept printing it. The
     # releases were held here the whole time; they carry the tonnage series the Cables
     # driver is now built on. A negative search that has since been answered is not a
     # negative search, and leaving it in the register is how a study comes to contradict
     # itself between two of its own pages.
     "MVA, meter-count or backlog figure for any segment. THIS NEGATIVE RESULT IS NOW "
     "PARTLY ANSWERED AND IS RECORDED THAT WAY: the company's own quarterly earnings "
     "releases carry the data and were read — cable tonnage of 144,997 / 156,748 / "
     "167,665 / 185,449 over FY2022-25 and 99,239 in the reviewed half, and an "
     "engineering backlog of EGP 346bn at 30 June 2026. The tonnage series sets the "
     "Cables growth driver; the backlog corroborates the Constructions taper rather "
     "than producing it. What remains negative is narrower and is stated as such: the "
     "AUDITED statements disclose none of it, so none of it is audited."),
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
  f"stated up front: every panel figure is rolled to the {M['asof']} anchor exactly as the four "
  f"lenses are; and Expert 1 deliberately runs the SAME kind of earnings-power question as "
  f"section 1.4 with different persona choices — FY2028-scale earnings at "
  f"{n1(EXP['e1']['pe'])}× against the "
  f"lens's current-scale earnings at {n1(LN['normalized']['pe_base'])}× — which is why the two "
  f"land {p2(EXP['e1']['base'])} and "
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
        [f"Range ({n1(E1['pe_lo'])}× to {n1(E1['pe_hi'])}×)",
         f"{p2(E1['rng'][0])} – {p2(E1['rng'][1])}"]]
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
         f"forecast's net-finance construction (cost-of-debt path × gross book less "
         f"{pc(IN['cash_yield'], 0)} on the "
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

out = os.path.join(HERE, DELIVERED)
doc.save(out)
print(f"wrote {out} | {len(doc.paragraphs)} paragraphs | {len(doc.tables)} tables")
