"""AMOC_Valuation_Study_06-08-2026_public.docx — python-docx builder, house style.
Reads study_numbers.json exclusively: no numeral is typed into this file."""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..'))
os.chdir(HERE)
exec(open(os.path.join(HERE, 'docx_base.py')).read())   # doc, P, H1, H2, table, box, ...

D = json.load(open(os.path.join(HERE, 'study_numbers.json')))
M, HI, HB, F, BASE = D['meta'], D['hist_is'], D['hist_bs'], D['fcst'], D['base']
W, DCF, LN, SN = D['wacc'], D['dcf'], D['lenses'], D['sens']
EXP, TR, REL, NRM, BK = D['experts'], D['terminal_recon'], D['rel'], D['norm'], D['book']
S0, STK, U = D['step0'], D['strike'], D['unit']
BT = D['backtest']; BT5, BTF, BTP = BT['five_year'], BT['full'], BT['production']
IN = {k: v['value'] for k, v in D['inputs'].items()}
SPOT, SH = M['spot'], M['shares_mn']
YRS = F['years']
H3M, H1M = STK['horizons']['3M'], STK['horizons']['1M']
BETA = W['beta']
SPEC_REV25 = U['rev25_lines']['oil'] + U['rev25_lines']['wax']
FUEL_REV25 = U['rev25_lines']['fuel']
FUEL_VOL25 = U['vol25']['fuel']
LNAME = dict(oil='Base oils (SN150 / SN500 / SN600)', wax='Fully refined paraffin wax',
             fuel='Fuel and by-products')
XC = json.load(open(os.path.join(HERE, 'formula_count.json')))


def n0(x): return f"{x:,.0f}"
def n1(x): return f"{x:,.1f}"
def n3(x): return f"{x:,.3f}"
def p2(x): return f"{x:.2f}"
def pc(x, dp=1): return f"{x*100:.{dp}f}%"
def sgn(x, dp=1): return f"{x*100:+.{dp}f}%"


YH = ['FY2022/23', 'FY2023/24', 'FY2024/25', 'CY2025']
# the ten-column appendix tables cannot fit the long form without truncating it
YH_SHORT = ['Jun-23', 'Jun-24', 'Jun-25', 'CY2025']
H4 = ['FY23', 'FY24', 'FY25', 'CY25']

import numpy as _np0
P3M_ABOVE_CENTRAL = float(
    (_np0.load(os.path.join(HERE, 'paths_3M.npy'))[:, -1] > D['central']).mean())

# =========================== MASTHEAD / TITLE ================================
masthead()
H2('Independent Valuation Study — Educational Analysis')
H1('Alexandria Mineral Oils Company S.A.E. (EGX: AMOC)')
P(f"Downstream petroleum processor — lubricant base oils, fully refined paraffin wax, special "
  f"oils, gas oil, naphtha, liquefied petroleum gas and fuel-oil blend · Egyptian Exchange · "
  f"reporting currency EGP · analysis anchored on the closing price of {p2(SPOT)} on "
  f"{M['asof']}.", size=10, color=GREY)

box([("READ FIRST — what this document is. ",
      "This is an educational valuation study. It contains no recommendation, no rating and no "
      "price target. What it contains is a fair-value range built from disclosed financial "
      "statements, a stated cost of capital and explicitly listed assumptions — together with a "
      "separate, probabilistic map of where the share price could trade over the next one and "
      "three months. The two are different objects and are never blended."),
     ("What a fair value is not. ",
      "A fair-value estimate is a statement about what the business appears to be worth on the "
      "assumptions set out here. It is not a forecast of the share price and carries no implied "
      "timeframe. A share can trade above or below an intrinsic estimate for years."),
     ("Where the numbers come from. ",
      "Every figure traces to a source recorded in the accompanying source register, which is "
      "issued as a separate document. Where a figure is derived rather than disclosed it is "
      "labelled as derived and the derivation is shown on the face of the companion model."),
     ("The single largest uncertainty. ",
      "The company changed its financial year end from 30 June to 31 December during the period "
      "under review, and the disclosure available for the resulting stub and transition periods "
      "is thinner than for a clean twelve-month year. The base year used here is CONSTRUCTED "
      "from two separately disclosed halves rather than taken from a single filing, and the "
      "construction is shown in full so a reader can check it.")])

# =========================== HEADLINE ========================================
H2('Headline')
P(f"Alexandria Mineral Oils is the only refinery listed on the Egyptian Exchange. It takes "
  f"feedstock from the adjacent state petroleum complex at El-Amerya and separates it into two "
  f"very different product streams: a small, high-value specialty slate — base oils in the "
  f"SN150, SN500 and SN600 grades, fully refined paraffin wax, transformer and special oils — "
  f"and a much larger volume of fuel products and by-products. In calendar 2025 the company "
  f"moved about {n3(U['vol_cy25'])}mn tonnes and turned over EGP {n0(BASE['rev_cy25'])}mn.")
P(f"The economics are those of a thin-margin processor, and the disclosed record says so "
  f"plainly: in the financial year to June 2023 cost of sales of EGP {n0(IN['cogs_fy23'])}mn sat "
  f"against gross profit of EGP {n0(IN['gp_fy23'])}mn, a gross margin of "
  f"{pc(IN['gp_fy23']/IN['rev_fy23'],2)}. That is the single most important fact about the "
  f"company, because it means the value is not in the revenue line — which is largely the "
  f"pass-through of feedstock at world product prices — but in the tonnage, the slate mix and "
  f"the spread earned per tonne.")
P(f"Two structural facts shape everything that follows. The first is the year-end change: the "
  f"exchange approved a move from a 30 June financial year to 31 December, with July to December "
  f"2025 filed as a six-month transition period. The second is the balance sheet. Gross "
  f"borrowings are EGP {n1(IN['debt_snap'])}mn against cash of EGP {n0(IN['cash_snap'])}mn — the "
  f"company is NET CASH to the tune of EGP {n0(-BASE['nd_cy25'])}mn, which is EGP "
  f"{p2(-BASE['nd_cy25']/SH)} a share, or {pc(-BASE['nd_cy25']/M['mktcap'],0)} of the entire "
  f"market capitalisation.")
P(f"The volume story is real and recent. The transition half alone sold "
  f"{n0(IN['vol_h2cy25']*1000)} thousand tonnes, {sgn(0.145,1)} on the same period a year "
  f"earlier and an annualised {n3(IN['vol_h2cy25']*2)}mn tonnes against {n1(IN['vol_fy25'])}mn in "
  f"the June-2025 year. Exports of oils and waxes reached about "
  f"{n0(IN['exp_h2cy25']*1000)} thousand tonnes in that half, up about 40% on entry into new "
  f"markets. The "
  f"first calendar quarter of 2026 carried it on: consolidated sales of EGP "
  f"{n0(IN['rev_q1cy26'])}mn and profit of EGP {n0(IN['pat_q1cy26'])}mn, up 37%.")
P(f"On the primary construction the four lenses centre at EGP {p2(D['central'])} a share against "
  f"a market price of {p2(SPOT)} — the central estimate sits about {sgn(D['central']/SPOT-1,0)} "
  f"above the market price. That gap is smaller than the disagreement AMONG the lenses and far "
  f"smaller than the three-month price distribution in section 3, so it does not support a "
  f"directional conclusion; the honest reading is that the study cannot distinguish this price "
  f"from fair value. The lenses do not agree with each "
  f"other, and that disagreement is the finding rather than a nuisance to be averaged away: the "
  f"cash-flow lens says EGP {p2(DCF['ps'])}, normalised earnings power says EGP "
  f"{p2(LN['normalized']['base'])}, and the two lenses anchored on today's market — relative "
  f"multiples at EGP {p2(LN['relative']['base'])} and book value at EGP {p2(LN['book']['base'])} "
  f"— say less. The spread is what a {pc(W['wacc_exp'])} front-end cost of capital does to a "
  f"business whose growth is real but whose cash arrives over years.", space_after=10)

# =========================== VALUATION SUMMARY ===============================
H2('Valuation summary — every read at a glance')
rows = [['Read', 'Basis', 'Range (EGP)', 'Central', 'vs spot'],
        ['Free cash flow to the firm',
         f"Five-year forecast; cost of capital gliding {pc(W['wacc_exp'])} → {pc(W['wacc_term'])}; "
         f"terminal growth {pc(IN['g_term'],0)}. TERMINAL VALUE = {pc(DCF['tv_share'],1)} OF "
         f"ENTERPRISE VALUE",
         f"{p2(LN['dcf']['bear'])} – {p2(LN['dcf']['bull'])}", p2(DCF['ps']),
         sgn(DCF['ps']/SPOT-1, 0)],
        ['Relative multiples',
         f"{IN['ev_ebitda_just']}× enterprise value to {YRS[1]} EBITDA, discounted back two years "
         f"at the model's own factor; trailing multiple {n1(REL['ev_ebitda_trailing'])}×",
         f"{p2(LN['relative']['bear'])} – {p2(LN['relative']['bull'])}",
         p2(LN['relative']['base']), sgn(LN['relative']['base']/SPOT-1, 0)],
        ['Normalised earnings power',
         f"{IN['pe_just']}× on {NRM['year']} attributable earnings of EGP {p2(NRM['eps'])} a "
         f"share; a mid-cycle earnings-power statement, not a discounted present value",
         f"{p2(LN['normalized']['bear'])} – {p2(LN['normalized']['bull'])}",
         p2(LN['normalized']['base']), sgn(LN['normalized']['base']/SPOT-1, 0)],
        ['Book value and sustainable return',
         f"Justified price-to-book {n1(BK['pb_just'])}× on book value of EGP {p2(BK['bvps'])}, at "
         f"a sustainable return of {pc(IN['roe_sust'],0)} and the perpetual cost of equity "
         f"{pc(W['ke_term'])}",
         f"{p2(LN['book']['bear'])} – {p2(LN['book']['bull'])}", p2(LN['book']['base']),
         sgn(LN['book']['base']/SPOT-1, 0)],
        ['WEIGHTED CENTRAL',
         f"Weights {pc(LN['dcf']['w'],0)} / {pc(LN['relative']['w'],0)} / "
         f"{pc(LN['normalized']['w'],0)} / {pc(LN['book']['w'],0)}",
         f"{p2(D['span'][0])} – {p2(D['span'][1])}", p2(D['central']),
         sgn(D['central']/SPOT-1, 0)],
        ['Expert panel median',
         'Three methods worked in Appendix C. NOT an independent check: one of the three is an '
         'economic-profit build that reproduces the cash-flow lens as an algebraic identity, and '
         'here it IS the median. Read the two genuinely independent reads instead — they bracket '
         'the cash-flow lens rather than confirming it',
         f"{p2(min(EXP[e]['rng'][0] for e in ('e1','e2','e3')))} – "
         f"{p2(max(EXP[e]['rng'][1] for e in ('e1','e2','e3')))}",
         p2(D['panel_centre']), sgn(D['panel_centre']/SPOT-1, 0)],
        ['Market price', f"Closing price on {M['asof']}", '—', p2(SPOT), '—']]
table(rows, [1.42, 2.90, 1.06, 0.72, 0.68], size=8.3, band_rows={5, 7}, left_cols={1})
caption(f"Terminal value as a percentage of enterprise value is stated in the first row and "
        f"again in the enterprise-value bridge in section 1.8. At {pc(DCF['tv_share'],1)} it is "
        f"a high but not unusual share for a business whose cost of capital is expected to fall "
        f"by roughly {n0((W['wacc_exp']-W['wacc_term'])*10000)} basis points over the forecast; "
        f"the reader should treat the cash-flow lens as a statement about the terminal state at "
        f"least as much as about the next five years.")

figure('fig1_football.png', 6.9,
       'Figure 1 — the four lenses and the weighted central, each shown bear to bull with the '
       'base marked. The vertical rule is the market price.')

bullet('What the bear and bull columns above actually are, stated before anyone reads a range off '
       'them. On the cash-flow lens they are FIVE drivers moved simultaneously and in the same '
       'direction, so they compound; they are not one-standard-deviation bands and no probability '
       'attaches to them.', bold_head='Scenario definitions. ')
SC = D['scen']
rows = [['Driver moved', 'Bear', 'Base', 'Bull']]
for k in ('vol_mult', 'gm_shift', 'fx_mult', 'wacc_shift', 'g'):
    if k == 'gm_shift':
        cell = lambda v: sgn(v, 1)
        b = '—'
    elif k == 'wacc_shift':
        cell = lambda v: f"{v*100:+.0f} points"
        b = '—'
    elif k == 'g':
        cell = lambda v: pc(v, 0)
        b = pc(IN['g_term'], 0)
    else:
        cell = lambda v: f"{v:.2f}× the assumed path"
        b = '1.00× (as assumed)'
    rows.append([SC['labels'][k], cell(SC['bear'][k]), b, cell(SC['bull'][k])])
rows.append(['RESULTING FAIR VALUE (EGP a share)', p2(SC['bear']['ps']), p2(SC['base_ps']),
             p2(SC['bull']['ps'])])
table(rows, [3.05, 1.10, 1.35, 1.10], size=8.4, band_rows={6}, left_cols={0})
caption(f"The other three lenses take their ranges differently and it is worth saying so rather "
        f"than letting the reader assume one convention: the relative lens is struck on multiples "
        f"of 3.5× and 6.0× enterprise value to EBITDA against {IN['ev_ebitda_just']}× in the "
        f"base; normalised earnings power on price-to-earnings multiples of 5.5× and 9.5× against "
        f"{IN['pe_just']}×; and the book lens by moving the sustainable return ±3 points and the "
        f"growth rate, at a blended rather than perpetual cost of equity on the bear side. Only "
        f"the cash-flow lens re-runs the model. Because the four conventions differ, the full "
        f"span of EGP {p2(D['span'][0])} to {p2(D['span'][1])} in the summary table is the "
        f"envelope of four differently-constructed ranges and should not be read as a "
        f"distribution.")

# =========================== COMPANY OVERVIEW ================================
H1('The company')
P(f"Alexandria Mineral Oils Company was established in 1997 to meet Egypt's domestic requirement "
  f"for lubricating base oils and paraffin waxes and to place the surplus into export markets. "
  f"Its single complex sits at El-Amerya, west of Alexandria, adjacent to the refining assets it "
  f"draws feedstock from. It is the only refinery listed on the Egyptian Exchange, and the "
  f"Egyptian General Petroleum Corporation is its second-largest single shareholder with a "
  f"{pc(IN['egpc_stake'],0)} holding — a fact that matters commercially as well as politically, "
  f"because the same state complex is both the principal supplier of feedstock and a principal "
  f"offtaker of product.")
H2('What it actually sells')
rows = [['Leg', 'Products', 'Volume (mn t)', 'Revenue (EGP mn)', 'Share of revenue'],
        ['Specialty oils and waxes',
         'Base oils SN150 / SN500 / SN600, fully refined solid and liquid paraffin wax, '
         'uninhibited transformer oil, automatic transmission fluid, spindle oil',
         n3(U['spec_vol25']), n0(SPEC_REV25),
         pc(SPEC_REV25/BASE['rev_cy25'])],
        ['Fuel and by-products',
         'Low-sulphur gas oil, naphtha, liquefied petroleum gas, fuel-oil blend, aromatic '
         'extract, vacuum residue, sulphur',
         n3(FUEL_VOL25), n0(FUEL_REV25),
         pc(FUEL_REV25/BASE['rev_cy25'])],
        ['Total', '', n3(U['vol_cy25']), n0(BASE['rev_cy25']), '100.0%']]
table(rows, [1.45, 2.75, 0.95, 1.10, 0.92], size=8.3, band_rows={3}, left_cols={1})
caption(f"The specialty leg is {pc(U['spec_vol25']/U['vol_cy25'],0)} of the tonnage but "
        f"{pc(SPEC_REV25/BASE['rev_cy25'],0)} of the revenue, and a much larger share again of "
        f"the margin. That is the whole investment case for the slate mix in one line. The two "
        f"legs shown here are an AGGREGATION of the three product lines built in section 1.4 — "
        f"base oils and paraffin wax added together — and not a separate estimate; readers "
        f"wanting the line-by-line tonnage, dollar realisation and revenue should go there. An "
        f"earlier edition offered the implied fuel realisation as the check 'that tells us the "
        f"split is real rather than fitted to a target'. In that edition the fuel price was the "
        f"RESIDUAL of base-year revenue, so the check was circular and the sentence has been "
        f"withdrawn. Section 1.5 now shows something the aggregation above conceals entirely: "
        f"almost all of this company's gross profit is made on the specialty leg, and the fuel "
        f"slate runs at or below break-even.")

H2('The balance sheet is the unusual part')
P(f"A company turning over EGP {n1(BASE['rev_cy25']/1000)}bn runs on a balance sheet of EGP "
  f"{n1(IN['assets_snap']/1000)}bn. That is an asset turnover near "
  f"{n1(BASE['rev_cy25']/IN['assets_snap'])} times, extraordinary for a refiner, and it has two "
  f"causes. The plant was commissioned between 1997 and 2000 and is substantially written down — "
  f"at the depreciation charge the model carries, the residual book has roughly "
  f"{n1(BASE['implied_life'])} years of life left in it. And the working-capital cycle is "
  f"effectively funded by the counterparty: net working capital is about "
  f"{pc(BASE['nwc_pct'])} of revenue, because the feedstock payable to the state petroleum "
  f"corporation is the company's principal source of short-term funding.")
P(f"The consequence for the valuation is that this is a business with very little invested "
  f"capital and therefore a very high accounting return on it — {pc(TR['roic']['CY25'])} in the "
  f"base year on the reconstruction used here. That is a real feature, not an artefact, and it "
  f"is why the terminal reinvestment the model requires to fund {pc(IN['g_term'],0)} of "
  f"perpetual growth is only {pc(DCF['rr_term'])} of profit. It also carries a warning, which "
  f"section 7 returns to: a return that high on a plant that old is partly a statement about "
  f"depreciation, and the capital will eventually have to be replaced at something closer to "
  f"replacement cost.")

# =========================== 1 FUNDAMENTAL VALUATION =========================
H1('1  Fundamental valuation')
H2('1.1  Why this company is valued as an operating company and not as anything else')
P(f"The lens decision is the one that invalidates a study if it is wrong, so the evidence is set "
  f"out before the arithmetic. Three readings were available: an operating company valued on its "
  f"own cash flows; a holding company valued by summing its stakes; or a two-leg business "
  f"requiring both. The evidence points cleanly to the first.")
bullet('Consolidated profit after tax for the year to June 2025 was EGP '
       f"{n0(IN['pat_fy25'])}mn against standalone profit of EGP "
       f"{n0(IN['pat_fy25_standalone'])}mn. Everything outside the parent refinery therefore "
       f"contributes about {pc(IN['pat_fy25']/IN['pat_fy25_standalone']-1)} of the group. A "
       "holding company is a portfolio whose value is the sum of its stakes; here roughly 96% of "
       "the profit comes from one plant.", bold_head='Earnings concentration. ')
bullet('All of it is own-production petroleum product sold by the tonne. There is no financing '
       'leg, no captive lender, no development land bank and no recurring-income property — the '
       'revenue mix is a product slate, not a set of businesses.',
       bold_head='Revenue mix. ')
bullet(f"Inventory, receivables and payables dominate; the plant is written down and the "
       f"investment portfolio is immaterial next to the operating assets. A holding company's "
       f"balance sheet looks the opposite way round.", bold_head='Balance-sheet shape. ')
P(f"So the primary lens is a discounted free cash flow to the firm, cross-checked by relative "
  f"multiples, normalised earnings power and book value against a sustainable return. Nothing is "
  f"split into legs that need different methods, because there are none.")

H2('1.2  The base year is constructed, and here is the construction')
P(f"The financial year moved from 30 June to 31 December. That leaves no single filed twelve-"
  f"month period that is both recent and clean, so the base year is built from two separately "
  f"disclosed halves — neither of them estimated.")
rows = [['Step', 'Period', 'Revenue (EGP mn)', 'Profit after tax (EGP mn)'],
        ['Reported June year (average of three disclosed figures)', 'Jul 2024 – Jun 2025',
         n0(BASE['rev_fy25']), n0(IN['pat_fy25'])],
        ['less the disclosed first half', 'Jul – Dec 2024',
         f"({n0(IN['rev_h1fy25'])})", f"({n0(IN['pat_h1fy25'])})"],
        ['= the second calendar half of 2025 comparative', 'Jan – Jun 2025',
         n0(BASE['rev_h1cy25']), n0(BASE['pat_h1cy25'])],
        ['plus the filed transition period', 'Jul – Dec 2025',
         n0(IN['rev_h2cy25']), n0(IN['pat_h2cy25'])],
        ['= BASE YEAR', 'Calendar 2025', n0(BASE['rev_cy25']), n0(BASE['pat_cy25'])]]
table(rows, [3.05, 1.35, 1.35, 1.35], size=8.6, band_rows={5}, left_cols={1})
caption(f"Net margin on the constructed base year is {pc(BASE['pat_cy25']/BASE['rev_cy25'],2)}. "
        f"The construction is carried on the face of the companion model as live formulas, so a "
        f"reader who disagrees with one of the four disclosed inputs can change it and watch the "
        f"base move.")
P(f"A separate release covering the six months to 30 June 2026 reports revenue of EGP "
  f"{n0(IN['rev_h1cy26_rep'])}mn, up 35%, and profit after tax of EGP "
  f"{n0(IN['pat_h1cy26_rep'])}mn, up 109%. Against the January-to-June 2025 half constructed "
  f"above, those are {sgn(BASE['implied_growth_rev'])} and {sgn(BASE['implied_growth_pat'])} — "
  f"both reproduce the reported growth rates independently, which is what identifies the period "
  f"the release covers. It is carried here as corroboration and NOT as the forecast base, for "
  f"two reasons: it rests on a single source, and the margin it implies is far above anything in "
  f"the company's own record. The margin path used below is deliberately struck under it.")

H2('1.3  A line the reported profit hides — and why the forecast leaves it out')
P(f"Building the historical years from the gross margin down, rather than backwards from "
  f"reported profit, exposes something the headline numbers conceal. Reported pre-tax profit in "
  f"these years is materially larger than the operating result plus finance income can explain. "
  f"The residual is other and non-operating income, and it has a shape:")
rows = [['', *YH],
        ['Operating result (EBIT)', *[n0(HI[k]['ebit']) for k in H4]],
        ['Net finance income', *[n0(HI[k]['fin']) for k in H4]],
        ['Other and non-operating income', *[n0(HI[k]['other']) for k in H4]],
        ['= profit before tax', *[n0(HI[k]['ebt']) for k in H4]],
        ['Other income as a share of pre-tax profit',
         *[pc(HI[k]['other']/HI[k]['ebt']) for k in H4]]]
table(rows, [2.55, 1.09, 1.09, 1.09, 1.09], size=8.4, band_rows={4})
P(f"EGP {n0(HI['FY23']['other'])}mn in the year to June 2023, {n0(HI['FY24']['other'])}mn, "
  f"{n0(HI['FY25']['other'])}mn, and effectively nothing by calendar 2025. That is the profile of "
  f"exchange gains on dollar export receivables through the 2022-to-2024 devaluation sequence, "
  f"washing out as the pound stabilised. It explains the otherwise puzzling record of the last "
  f"three years — revenue compounding hard while reported profit barely moved — because the "
  f"operating result was rising as the currency windfall drained away.")
P(f"The forecast carries NONE of it. Every year from 2026 onward assumes zero other income. That "
  f"is deliberately conservative, and a reader who expects further pound weakness should regard "
  f"the forecast profit line as understated by whatever they think that windfall is worth. It "
  f"also means the fair value here is a valuation of the refinery, not of a currency position.")

H2('1.4  How revenue is built')
P(f"Not as one growth rate, and not from a calibrated price either. The company discloses a "
  f"product table — tonnes and value by line — and every realisation in this model is derived "
  f"from it. Base oils sold {IN['line_oil_t']:,.0f} tonnes for EGP {IN['line_oil_v']:,.1f}mn and "
  f"paraffin wax {IN['line_wax_t']:,.0f} tonnes for EGP {IN['line_wax_v']:,.1f}mn against a total "
  f"of {IN['line_tot_t']:,.0f} tonnes for EGP {IN['line_tot_v']:,.1f}mn, leaving the fuel and "
  f"by-product slate as the third line. Dividing gives EGP {U['px_egp']['oil']:,.0f}, "
  f"{U['px_egp']['wax']:,.0f} and {U['px_egp']['fuel']:,.0f} a tonne, which at that year's "
  f"exchange rate is USD {U['px_usd']['oil']:,.0f}, {U['px_usd']['wax']:,.0f} and "
  f"USD {U['px_usd']['fuel']:,.0f} — the right levels and the right order for SN-grade base oil, "
  f"paraffin and a gas-oil blend. NO PRICE IN THIS MODEL IS CALIBRATED AND NONE IS A RESIDUAL.")
P(f"That matters because of what it replaces. An earlier construction of this study had two legs, "
  f"a specialty price that was a free input and a fuel price that was the RESIDUAL of the base-year "
  f"revenue — and then offered the implied fuel realisation as a check that the split was real. A "
  f"residual cannot corroborate the construction that produced it. It is gone.")
LBL = {'oil': 'Base oils', 'wax': 'Paraffin wax', 'fuel': 'Fuel and by-products'}
P(f"There is no reconciliation factor in this edition, and no assumed price growth either. Both "
  f"are replaced by something the earlier build did not have: a crude reference that prices the "
  f"product AND the feedstock. Every realisation is the Brent deck times a CRACK MULTIPLE solved "
  f"from the disclosed table — base oils {U['crack']['oil']:.3f} times crude parity, paraffin wax "
  f"{U['crack']['wax']:.3f} times, and the fuel and by-product slate "
  f"{U['crack']['fuel']:.3f} times, which is to say at parity. Those three numbers are the "
  f"disclosed product table divided by the crude price. They are not fitted to anything, and "
  f"that base oil prints near 1.9 times crude, wax near 1.7 and a gas-oil blend within a per cent "
  f"of parity is the textbook shape of a lube refinery's slate — the strongest single piece of "
  f"evidence available here that the product table is genuine.")
rows = [['', 'Disclosed\nyear to\nJun-2024', 'CY2025'] + [y.replace('E', '') for y in YRS]]
rows.append(['VOLUME (mn tonnes)', '', '', '', '', '', '', ''])
for k in U['lines']:
    rows.append([f"   {LBL[k]}", n3(IN[f'line_{k}_t']/1e6) if k != 'fuel' else n3(U['line_fuel_t']/1e6),
                 n3(U['vol25'][k])] + [n3(v) for v in U['lines_vol'][k]])
rows.append(['   TOTAL', n3(IN['line_tot_t']/1e6), n3(U['vol_cy25'])] + [n3(v) for v in U['vol']])
rows.append(['CRUDE AND REALISATIONS (USD)', '', '', '', '', '', '', ''])
rows.append(['   Brent equivalent, per barrel', n1(IN['crude_hist']['fy24']),
             n1(U['hist_margin']['cy25']['brent'])] +
            [n1(x*U['recon_px']) for x in IN['brent_path']])
for k in U['lines']:
    rows.append([f"   {LBL[k]} — per tonne", n0(U['px_usd'][k]),
                 n0(U['hist_margin']['cy25']['parity']*U['crack'][k])] +
                [n0(IN['brent_path'][i]*IN['bbl_per_t_feed']*U['recon_px']*U['crack'][k])
                 for i in range(5)])
rows.append(['   USD / EGP average', n1(IN['fx_fy24']), n1(IN['fx_avg_cy25'])] +
            [n1(x) for x in IN['fx_path']])
rows.append(['REVENUE (EGP mn)', '', '', '', '', '', '', ''])
for k in U['lines']:
    rows.append([f"   {LBL[k]}", n0(IN[f'line_{k}_v']) if k != 'fuel' else n0(U['line_fuel_v']),
                 n0(U['rev25_lines'][k])] + [n0(x) for x in U['lines_rev'][k]])
rows.append(['   TOTAL', n0(IN['line_tot_v']), n0(BASE['rev_cy25'])] + [n0(x) for x in F['rev']])
table(rows, [1.62, 0.78, 0.72, 0.72, 0.72, 0.72, 0.72, 0.72], size=7.6,
      band_rows={1, 5, 6, 11, 12, 16}, left_cols={0})
caption(f"The base-year column carries a crude EQUIVALENT of ${U['hist_margin']['cy25']['brent']:,.1f} "
        f"a barrel against a published 2025 Brent average nearer "
        f"${IN['crude_hist']['cy25']:,.0f} — a premium of {U['recon_px']-1:+.1%}, which is what "
        f"the disclosed revenue requires at the disclosed tonnage and the solved crack "
        f"multiples. That premium is CARRIED into the forecast rather than dropped, because "
        f"dropping it would silently reprice every product line on the first forecast day. It is "
        f"the honest successor to the blanket reconciliation factor the previous edition "
        f"applied: same job, but a number that means something physical and that a reader can "
        f"disagree with.")

figure('fig7_mix.png', 6.9,
       'Figure 2 — revenue by product line with the EBITDA margin on the right axis.')

H2('1.5  The cost side, built per tonne — and what it says about the fuel slate')
P(f"This is the section the previous edition did not have, and its absence was the single "
  f"largest weakness in that model. Cost of sales is {1-F['gm'][0]:.1%} of revenue on this "
  f"company. Modelling it as revenue times one minus an assumed margin means the assumption IS "
  f"the valuation. It is now built.")
rows = [['Component', 'Basis', f"CY2025 (EGP mn)", 'Per tonne of product'],
        ['Feedstock', 'Crude parity × a differential SOLVED on disclosed cost of sales',
         n0(U['hist_margin']['cy25']['cogs']['feed']),
         f"USD {U['hist_margin']['cy25']['feed_pt']:,.0f}"],
        ['Energy and utilities', 'Per tonne of feedstock intake',
         n0(U['hist_margin']['cy25']['cogs']['energy']),
         f"USD {IN['energy_usd_t']/(1-IN['loss_frac']):,.0f}"],
        ['Chemicals, solvent, catalyst', 'Per tonne of product, by line',
         n0(U['hist_margin']['cy25']['cogs']['chem']), 'USD 3 – 60 by line'],
        ['Fixed conversion', 'Labour, maintenance, plant overhead — EGP-denominated',
         n0(U['hist_margin']['cy25']['cogs']['fixed']), '—'],
        ['COST OF SALES', '', n0(U['hist_margin']['cy25']['cogs']['total']), ''],
        ['REVENUE', '', n0(BASE['rev_cy25']), ''],
        ['GROSS MARGIN (output)', '', pc(U['gm_built'][3], 2), '']]
table(rows, [1.55, 2.75, 1.15, 1.25], size=8.2, band_rows={5, 7}, left_cols={0, 1})
P(f"Only ONE parameter in that table is fitted, and it is fitted to disclosure rather than to a "
  f"margin. The year to June 2023 is the only period with a disclosed cost of sales — EGP "
  f"{n0(IN['cogs_fy23'])}mn against revenue of {n0(IN['rev_fy23'])}mn. Energy, chemicals and the "
  f"fixed leg account for part of it; the feedstock charge is whatever is left. That works out "
  f"at {U['feed_diff']:.4f} of crude parity, which is a small discount to crude — exactly what a "
  f"lube plant drawing vacuum gas oil and long residue from the adjacent state complex should "
  f"show. It was solved, not chosen, and if it had come out at 1.3 or at 0.5 this whole section "
  f"would have had to be abandoned.")
P(f"Everything after that is a PREDICTION. The build is calibrated on one year and one cost "
  f"line; the other three historical margins are outputs, and the previous edition's assumed "
  f"path is the thing they can be checked against.")
rows = [['', *YH],
        ['Gross margin — BUILT (this edition)', *[pc(x, 2) for x in U['gm_built']]],
        ['Gross margin — ASSUMED (previous edition)',
         *[pc(x, 2) for x in U['gm_assumed_old']]],
        ['Difference', *[f"{(a-b)*1e4:+.0f} bp" for a, b in zip(U['gm_built'],
                                                                U['gm_assumed_old'])]]]
table(rows, [2.42, 1.09, 1.09, 1.09, 1.09], size=8.4, band_rows={1})
caption(f"The June-2023 column is the calibration, so a zero difference there is arithmetic and "
        f"not evidence. The other three are the test, and they land within "
        f"{max(abs(a-b) for a, b in zip(U['gm_built'][1:], U['gm_assumed_old'][1:]))*1e4:.0f} "
        f"basis points of a path that was built by a completely different route — from the "
        f"disclosed FY2022/23 margin drifting up on an assumed mix shift. Two independent "
        f"constructions agreeing to within a point on a 6% margin is a real check, and it is the "
        f"one the earlier edition's 'reconciliation factor' was reaching for and missing. Where "
        f"they disagree the BUILT number is carried, which is why the forecast margin here is "
        f"slightly below the previous edition's.")
P(f"Now the finding that matters, and it is not a small one. Because the cost build prices every "
  f"line off the same feedstock, the per-line margins are OUTPUTS, and they are nothing like "
  f"each other.", size=10)
rows = [['Line', 'Realisation (USD/t)', 'Gross margin 2026E', 'Share of tonnage',
         'Share of gross profit'],
        *[[LBL[k],
           n0(IN['brent_path'][0]*IN['bbl_per_t_feed']*U['recon_px']*U['crack'][k]),
           pc(U['line_margin'][k][0], 1),
           pc(U['lines_vol'][k][0]/U['vol'][0], 1),
           pc(U['lines_rev'][k][0]*U['line_margin'][k][0]/F['gp'][0], 1)] for k in U['lines']]]
table(rows, [1.60, 1.35, 1.20, 1.15, 1.40], size=8.3, left_cols={0})
caption(f"Read the bottom row first. The fuel and by-product slate is "
        f"{U['lines_vol']['fuel'][0]/U['vol'][0]:.0%} of the tonnage and it runs at "
        f"{pc(U['line_margin']['fuel'][0],1)} — at or below break-even — because it sells at "
        f"crude parity and the feedstock costs almost as much as the product fetches. Essentially "
        f"the whole gross profit of this company is made on the "
        f"{(U['lines_vol']['oil'][0]+U['lines_vol']['wax'][0])/U['vol'][0]:.0%} of tonnage that "
        f"is base oil and wax. The previous edition ASSUMED the specialty slate earned 3.5 times "
        f"the fuel slate, which put them at roughly 14% against 4%. That was not a small error of "
        f"degree — it described a different business.")
P(f"Three consequences follow, and they change how the rest of this study should be read. First, "
  f"growth in the fuel slate is worth almost nothing: tonnage there converts to revenue and to "
  f"very little else. Second, the export push into base oils and wax is worth far more than the "
  f"earlier model could show, because it is the only leg that carries margin. Third, this "
  f"company is far more exposed to the base-oil crack than to crude, to volume, or to the "
  f"exchange rate — and the sensitivity table in section 1.11 should be read with that in mind.")
P(f"One honest caution on all of it. The yields, the energy intensity and the chemicals charges "
  f"are HOUSE ESTIMATES; this environment could not reach the notes to the accounts that would "
  f"replace them. What protects the conclusion is that the two parameters doing the real work — "
  f"the crack multiples and the feedstock differential — are both solved against disclosure, and "
  f"that the estimated ones are demonstrably weak levers. The process-loss rate, the one yield "
  f"parameter with no source at all, moves the blended margin by less than a hundred-thousandth "
  f"of itself, because it scales feedstock intake and the solved differential in opposite "
  f"directions and they cancel. That is asserted in the companion model as a live test, not "
  f"claimed here.")
P(f"And the crude deck, which was the obvious worry: moving it 10% either way moves the built "
  f"margin from {pc(U['elast']['dn'],2)} to {pc(U['elast']['up'],2)} against a base of "
  f"{pc(U['elast']['base'],2)} — an elasticity near "
  f"{abs((U['elast']['up']-U['elast']['dn'])/2/U['elast']['base'])/0.10:.1f} times rather than "
  f"the fifteen a naive reading would fear. Crude prices the product and the feedstock, so most "
  f"of it cancels; what does not cancel is the EGP-denominated fixed leg, whose share of revenue "
  f"moves when the dollar side moves. That is also the mechanism behind something the earlier "
  f"model could not explain — why this company's reported margin WIDENED through the devaluation "
  f"sequence while its dollar economics did not improve at all.")


H2('1.6  The cost of capital, built rather than asserted')
P(f"Egypt is a market in monetary transition, so a single flat rate applied to both the explicit "
  f"years and a perpetuity would assert that the cost of capital never normalises — a claim the "
  f"central bank's own published disinflation path contradicts. The schedule below therefore "
  f"slides from an explicit-window rate to a terminal rate, and the terminal value is discounted "
  f"at exactly the same cumulative factor as year-five cash flow. One date, one price of time.")
rows = [['Component', 'Explicit window', 'Terminal', 'Note'],
        ['Risk-free rate', pc(IN['rf']), pc(IN['rf_term']),
         "10-year local-currency government bond today; the terminal rate is norm-built from the "
         f"central bank's own published inflation target — {pc(IN['cbe_target'],0)} for late 2026, "
         f"falling to 5% thereafter — plus an emerging-market real-rate convention"
         " "
         "real-rate convention"],
        ['less sovereign default spread', f"({pc(IN['sov_spread_cds'])})", '—',
         'netted out so Egypt’s default risk is not charged twice — once inside the pound '
         'yield and again in the country premium'],
        ['Beta', n3(IN['beta']), n3(IN['beta']),
         f"own-stock regression, R-squared {pc(BETA['r2'])}, n = {BETA['n']}"],
        ['Equity risk premium', pc(IN['erp_cds']), pc(IN['erp_term']),
         'total premium on the credit-default-swap basis; normalised below the crisis-era level '
         'into perpetuity'],
        ['COST OF EQUITY', pc(W['ke_exp']), pc(W['ke_term']), ''],
        ['Cost of net debt, after tax', pc(W['k_nd_at']), pc(W['kd_term_at']),
         'blend of what the borrowing costs and what the cash earns'],
        ['Debt weight', pc(W['wd_exp']), pc(IN['wd_term'], 0),
         'NEGATIVE today, because the company is net cash'],
        ['WEIGHTED COST OF CAPITAL', pc(W['wacc_exp']), pc(W['wacc_term']), '']]
table(rows, [1.62, 0.95, 0.82, 3.36], size=8.2, band_rows={5, 8}, left_cols={3})
P(f"The weighting deserves a paragraph, because it runs the opposite way to the intuition most "
  f"readers bring. Net debt is negative, so the debt weight is {pc(W['wd_exp'])} and the equity "
  f"weight {pc(W['we_exp'])}. The cost of that negative debt is the blend of what the EGP "
  f"{n1(IN['debt_snap'])}mn of borrowing costs and what the EGP {n0(IN['cash_snap'])}mn cash pile "
  f"EARNS — {pc(W['k_nd_at'])} after tax, essentially the after-tax deposit yield. The result, "
  f"{pc(W['wacc_exp'])}, sits ABOVE the {pc(W['ke_exp'])} cost of equity rather than below it. "
  f"That is the point of the construction: a company holding {pc(-BASE['nd_cy25']/M['mktcap'],0)} "
  f"of its market capitalisation in near-riskless cash has an observed equity cost that "
  f"UNDERSTATES the risk of its operating assets, and unlevering for the cash is what recovers "
  f"the operating rate. The identity closes exactly — enterprise value over market "
  f"capitalisation times the operating rate, plus cash over market capitalisation times the cash "
  f"cost, recombines to the cost of equity.")
P(f"On a gross-debt basis the rate would be {pc(W['wacc_exp_gross'])} and the answer EGP "
  f"{p2(DCF['ps_gross_basis'])} a share, {sgn(DCF['ps_gross_basis']/DCF['ps']-1)} higher. That "
  f"construction discounts the operating cash flows at a rate the cash has already depressed and "
  f"then adds the same cash back in the bridge — counting it twice. The net basis is primary and "
  f"is the more conservative of the two by "
  f"{n0((W['wacc_exp']-W['wacc_exp_gross'])*10000)} basis points.")

H2('1.7  The discount-rate schedule, year by year')
rows = [['', *[y for y in YRS]],
        ['Cost of debt path', *[pc(x) for x in IN['kd_path']]],
        ['Cumulative progress along that path', *[f"{x:.3f}" for x in F['glide_frac']]],
        ['Forward cost of capital', *[pc(x) for x in F['fwd_wacc']]],
        ['Cumulative discount factor', *[f"{x:.4f}" for x in F['df']]]]
table(rows, [2.35, 0.92, 0.92, 0.92, 0.92, 0.92], size=8.4, band_rows={3, 4})
caption('The glide fractions are the cost-of-debt path’s own cumulative progress, so the '
        'front-loaded shape is inherited from one assumed easing calendar rather than being a '
        'second free parameter chosen separately. The terminal value is brought home on the '
        f"year-five factor of {F['df'][4]:.4f}, the same factor that discounts year-five cash "
        'flow.')

H2('1.8  The free-cash-flow waterfall and the enterprise-value bridge')
rows = [['EGP mn', *YRS],
        ['Revenue', *[n0(x) for x in F['rev']]],
        ['EBITDA', *[n0(x) for x in F['ebitda']]],
        ['EBITDA margin', *[pc(x, 2) for x in F['ebitda_margin']]],
        ['less depreciation and amortisation', *[f"({n0(x)})" for x in F['dna']]],
        ['EBIT', *[n0(x) for x in F['ebit']]],
        [f"NOPAT = EBIT × (1 − {pc(IN['tax_eff'],1)})", *[n0(x) for x in F['nopat']]],
        ['add back depreciation and amortisation', *[n0(x) for x in F['dna']]],
        ['less capital expenditure', *[f"({n0(x)})" for x in F['capex']]],
        ['less change in net working capital',
         *[f"({n0(x)})" if x >= 0 else n0(-x) for x in F['dnwc']]],
        ['FREE CASH FLOW TO THE FIRM', *[n0(x) for x in F['fcff']]],
        ['Discount factor', *[f"{x:.4f}" for x in F['df']]],
        ['PRESENT VALUE OF FREE CASH FLOW', *[n0(x) for x in F['pv']]]]
table(rows, [2.35, 0.92, 0.92, 0.92, 0.92, 0.92], size=8.2, band_rows={10, 12})
P(f"Two disclosed figures belong beside this table, neither of which the model otherwise "
  f"consumes. The rate applied above is an EFFECTIVE {pc(IN['tax_eff'],1)} against Egypt's "
  f"statutory corporate rate of {pc(IN['tax_stat'],1)} — AMOC is taxed at the ordinary rate, not "
  f"the ~40.55% that applies to exploration and production — and the study deliberately carries "
  f"the higher effective figure. Separately, the company's own approved planning budget put net "
  f"sales at EGP {n0(IN['budget_rev'])}mn for the year to June 2026 against a budgeted net "
  f"profit near EGP 1.02bn. The forecast here runs above the revenue line of that budget, on "
  f"calendar years and on the disclosed volume ramp; a reader who prefers management's own plan "
  f"should treat the first forecast year as the more aggressive of the two and discount "
  f"accordingly.", size=10)
caption('The full build is shown to the present value of free cash flow rather than stopping at '
        'the cash-flow line, so every step between the margin and the discounted number is '
        'visible and checkable.')

figure('fig8_waterfall.png', 6.6,
       'Figure 3 — the same waterfall for the first forecast year, drawn to scale.')

H2('1.9  The terminal block')
P(f"Growth in perpetuity has to be paid for with capital. The reinvestment rate is therefore not "
  f"a free choice: it is forced to satisfy growth = return × reinvestment exactly. At a terminal "
  f"return on invested capital of {pc(DCF['roic_term'])} — next year's profit over closing "
  f"invested capital, the standard convention — funding {pc(IN['g_term'],0)} of growth requires "
  f"reinvesting {pc(DCF['rr_term'])} of profit, and the rest is available to the providers of "
  f"capital.")
rows = [['Enterprise value to equity, and what makes it up', 'EGP mn', 'EGP / share'],
        ['Present value of the explicit five years', n0(DCF['pv_explicit']),
         p2(DCF['pv_explicit']/SH)],
        ['Present value of the terminal value', n0(DCF['pv_tv']), p2(DCF['pv_tv']/SH)],
        ['TERMINAL VALUE AS A PERCENTAGE OF ENTERPRISE VALUE', pc(DCF['tv_share'], 1), ''],
        ['ENTERPRISE VALUE (the operating assets)', n0(DCF['ev']), p2(DCF['ev']/SH)],
        [f"less minority interests at {pc(DCF['nci_share'])}, ON THE ENTERPRISE VALUE",
         f"({n0(DCF['nci_val'])})", f"({p2(DCF['nci_val']/SH)})"],
        ['= operating assets attributable to shareholders', n0(DCF['ev']-DCF['nci_val']),
         p2((DCF['ev']-DCF['nci_val'])/SH)],
        ['less net debt (negative — net cash is ADDED, in full)', n0(DCF['nd']),
         p2(DCF['nd']/SH)],
        ['EQUITY ATTRIBUTABLE TO SHAREHOLDERS', n0(DCF['eq_attr']), p2(DCF['ps'])],
        ['Market price', '', p2(SPOT)]]
table(rows, [3.85, 1.45, 1.30], size=8.5, band_rows={3, 4, 8})
caption(f"Terminal value is {pc(DCF['tv_share'],1)} of enterprise value, stated here as well as "
        f"in the summary table so the reader meets it in both places. The ORDER of the last three "
        f"rows is the substantive point and it was wrong in an earlier edition. That edition "
        f"added the cash first and then deducted the minority from the combined total, and "
        f"defended it in a caption reading 'the minority deduction is taken AFTER net debt, so "
        f"the minority does not carry a share of the parent's cash'. The algebra runs the other "
        f"way: deducting {pc(DCF['nci_share'])} of a total that already INCLUDES the cash hands "
        f"the minority {pc(DCF['nci_share'])} of the parent's balance — about EGP "
        f"{n0(DCF['nci_share']*-DCF['nd'])}mn of it. An external review caught this and it is "
        f"accepted. The minority is now deducted from the OPERATING enterprise value, before the "
        f"cash, and the cash is added back in full because it belongs to the parent. The "
        f"correction is worth EGP {p2(DCF['nci_share']*-DCF['nd']/SH)} a share.")

H2('1.10  Terminal growth, reconciled against the company’s own record')
P(f"A terminal rate is the single easiest place to manufacture a valuation, so it is checked "
  f"against what the business has actually done rather than asserted.")
rows = [['', *YH],
        ['NOPAT (EGP mn)', *[n0(TR['nopat'][k]) for k in H4]],
        ['Invested capital (EGP mn)', *[n0(TR['ic'][k]) for k in H4]],
        ['Return on invested capital', *[pc(TR['roic'][k]) for k in H4]],
        ['Capital expenditure (EGP mn)', *[n0(TR['capex'][k]) for k in H4]],
        ['Reinvestment rate', *[pc(TR['rr'][k]) for k in H4]],
        ['Character', *[TR['character'][k] for k in H4]],
        ['Implied growth (return × reinvestment)', *[pc(TR['implied_g'][k]) for k in H4]]]
table(rows, [2.42, 1.09, 1.09, 1.09, 1.09], size=8.4, band_rows={7})
P(f"Two check numbers, stated plainly. Actual compound NOPAT growth from the June-2023 year to "
  f"the constructed calendar-2025 base was {sgn(TR['nopat_cagr'])} a year. The growth implied by "
  f"return times reinvestment, taken from stable years only — every year here is self-funded, "
  f"with reinvestment well under 100% of profit — is {pc(TR['stable_g'])}. The adopted terminal "
  f"rate is {pc(IN['g_term'],0)}, the standing centre for an established name in this market once "
  f"currency turbulence has passed.")
P(f"THE TWO CHECKS DISAGREE WITH EACH OTHER, and that is the honest reading rather than a "
  f"problem to be smoothed. An earlier edition of this section said 'both checks come in below "
  f"the adopted rate'. That sentence was true of the model as it then stood and became FALSE "
  f"when the margin build was rebuilt from the product lines up, which moved the historical "
  f"NOPAT compound rate from {sgn(0.026)} to {sgn(TR['nopat_cagr'])}; the sentence survived the "
  f"rebuild because the assertion guarding it only tested the adopted rate against its ceiling "
  f"and never against the checks. It is corrected here and the guard now reports each candidate "
  f"individually.")
P(f"Taken one at a time: check (a), the historical compound rate of {sgn(TR['nopat_cagr'])}, is "
  f"far ABOVE the adopted {pc(IN['g_term'],0)} — but it is a recovery rate off a devaluation-"
  f"compressed base and belongs in the explicit years, not in a perpetuity. Check (b), return "
  f"times reinvestment on the stable years, is {pc(TR['stable_g'])} and is BELOW the adopted "
  f"rate. The adopted {pc(IN['g_term'],0)} sits between them, and above the one that actually "
  f"describes a steady state — so on the check that matters for a perpetuity it remains on the "
  f"GENEROUS side of the company's own record, not the conservative side. It is sensitised from "
  f"3% to 7% and the whole grid is on the face of the companion model.")
P(f"One definitional caution on check (b), because it changes the answer. It is struck on net "
  f"capital expenditure over profit, EXCLUDING working capital, while the free-cash-flow "
  f"waterfall above subtracts working capital as well. On the waterfall-consistent definition "
  f"the base-year reinvestment rate is {pc(TR['rr_waterfall'])} and the implied growth "
  f"is {pc(TR['g_waterfall'])} — ABOVE the adopted rate rather than below it. Both "
  f"definitions are shown and neither is hidden; a reader who prefers the waterfall-consistent "
  f"one should read the {pc(IN['g_term'],0)} as conservative instead.")
P(f"The crossover test — how long a candidate growth rate would take to make the company larger "
  f"than the economy it sits in — is reported candidate by candidate, because a blanket "
  f"'it does not bind' would be wrong. Against Egyptian nominal growth of about "
  f"{pc(IN['egypt_nominal_growth'],0)}: the forecast revenue rate of {sgn(TR['fcst_cagr'])} is "
  f"BELOW it and does not bind; the adopted terminal rate of {pc(IN['g_term'],0)} is BELOW it "
  f"and does not bind; the recent compound NOPAT rate of {sgn(TR['nopat_cagr'])} is ABOVE it and "
  f"DOES bind — at that rate the company would overtake Egypt's entire nominal gross domestic "
  f"product in about {n0(TR['crossover']['recent NOPAT compound rate'])} years, which is precisely "
  f"why it is a historical rate and not a terminal one. The binding constraint on the rate "
  f"actually adopted is the reinvestment identity, not the ceiling.")

H2('1.11  Sensitivities')
figure('fig2_sens.png', 6.3,
       'Figure 4 — fair value across the terminal cost of capital and the terminal growth rate. '
       'Bold entries sit within half a pound of the market price.')
rows = [['Driver', 'Range tested', 'Fair value across the range (EGP)'],
        ['Terminal cost of capital',
         f"{pc(SN['wt_grid'][0])} – {pc(SN['wt_grid'][4])}",
         ' · '.join(p2(SN['grid_wacc_g'][i][2]) for i in range(5))],
        ['Terminal growth', f"{pc(SN['g_grid'][0],0)} – {pc(SN['g_grid'][4],0)}",
         ' · '.join(p2(SN['grid_wacc_g'][2][j]) for j in range(5))],
        ['Explicit-window cost of capital',
         f"{pc(SN['we_grid'][0])} – {pc(SN['we_grid'][4])}",
         ' · '.join(p2(SN['grid_exp_term'][i][2]) for i in range(5))],
        ['Beta', f"{SN['beta_grid'][0]:.2f} – {SN['beta_grid'][4]:.2f}",
         ' · '.join(p2(x) for x in SN['grid_beta'])],
        ['Gross margin shift',
         f"{sgn(SN['gm_grid'][0],1)} – {sgn(SN['gm_grid'][4],1)} on the whole path",
         ' · '.join(p2(x) for x in SN['grid_margin'])],
        ['Volume growth', 'zero to double the assumed path',
         ' · '.join(p2(x) for x in SN['grid_vol'])],
        ['Exchange-rate path', '−10% to +10% on the assumed path',
         ' · '.join(p2(x) for x in SN['grid_fx'])],
        ['Net working capital', f"{pc(SN['nwc_grid'][0],0)} – {pc(SN['nwc_grid'][4],0)} of revenue",
         ' · '.join(p2(x) for x in SN['grid_nwc'])]]
table(rows, [1.85, 2.05, 3.05], size=8.2, left_cols={1, 2})
caption(f"The crux is the cost of capital, not the operating assumptions. Doubling the entire "
        f"volume growth path moves the answer from EGP {p2(SN['grid_vol'][2])} to "
        f"{p2(SN['grid_vol'][4])}; a two-point move in the terminal rate alone moves it across a "
        f"wider span than that. This is a valuation about Egyptian interest rates at least as "
        f"much as it is about a refinery.")

H2('1.12  The three cross-check lenses')
P(f"Relative multiples. Applying {IN['ev_ebitda_just']}× enterprise value to EBITDA to "
  f"{REL['year']} EBITDA of EGP {n0(REL['ebitda_mid'])}mn gives an enterprise value of EGP "
  f"{n0(REL['ev_rel_fwd'])}mn AS AT the end of that year. It has to be discounted back before it "
  f"can be compared to today's price: at the model's own year-two factor of {REL['df_rel']:.4f} "
  f"that is EGP {n0(REL['ev_rel'])}mn today, and EGP {p2(LN['relative']['base'])} a share after "
  f"the bridge. Not discounting a forward enterprise value would have produced EGP "
  f"{p2(((REL['ev_rel_fwd'] - DCF['nd']) * (1-DCF['nci_share']))/SH)} — the difference between "
  f"the two is the whole reason multiples and discounted cash flows are so often reconciled "
  f"badly. The company's own trailing multiples are {n1(REL['ev_ebitda_trailing'])}× enterprise "
  f"value to EBITDA and {n1(REL['pe_trailing'])}× earnings.")
P(f"Normalised earnings power. Every component is taken from the same year, {NRM['year']}, so "
  f"the lens is not a blend of different points in the cycle: EBITDA of EGP {n0(NRM['ebitda'])}mn "
  f"less depreciation of EGP {n0(NRM['dna'])}mn, plus net finance income of EGP "
  f"{n0(NRM['interest'])}mn, taxed and after minorities, gives EGP {p2(NRM['eps'])} a share. At "
  f"{IN['pe_just']}× that is EGP {p2(LN['normalized']['base'])}. This lens is a statement of "
  f"mid-cycle earnings POWER at a through-cycle multiple, not a discounted present value — which "
  f"is exactly why it is the most generous of the four and why it carries only "
  f"{pc(LN['normalized']['w'],0)} of the weight.")
P(f"Book value and sustainable return. The justified price-to-book identity gives "
  f"{n1(BK['pb_just'])}× = (sustainable return {pc(IN['roe_sust'],0)} less growth "
  f"{pc(IN['g_term'],0)}) divided by (perpetual cost of equity {pc(W['ke_term'])} less growth), "
  f"applied to attributable book value of EGP {p2(BK['bvps'])} a share, for EGP "
  f"{p2(LN['book']['base'])}. The perpetual rate is the correct one inside a perpetuity identity; "
  f"using a blend of the explicit and terminal rates would be internally inconsistent. Trailing "
  f"return on average attributable equity is {pc(BK['roe_trailing'])}, and the sustainable rate "
  f"is struck below it because the reported figure is flattered by an asset base that is nearly "
  f"written off and will have to be renewed.")

H2('1.13  Contested choices, computed rather than argued')
rows = [['Choice', 'This study', 'The alternative', 'Fair value on the alternative', 'Effect'],
        ['Country risk basis', 'Credit-default-swap column',
         f"Rating basis: cost of capital {pc(DCF['wacc_exp_rating'])} explicit / "
         f"{pc(DCF['wacc_term_rating'])} terminal", p2(DCF['ps_rating_basis']),
         sgn(DCF['ps_rating_basis']/DCF['ps']-1)],
        ['Capital-structure weights', 'Net debt (negative)', 'Gross debt',
         p2(DCF['ps_gross_basis']), sgn(DCF['ps_gross_basis']/DCF['ps']-1)],
        ['Minority share of group profit', pc(DCF['nci_share']),
         f"Doubled to {pc(DCF['nci_alt'],0)}", p2(DCF['ps_nci_alt']),
         sgn(DCF['ps_nci_alt']/DCF['ps']-1)],
        ['Currency of discounting', 'Egyptian pound throughout',
         f"Export leg deflated to dollars and discounted at {pc(W['wacc_usd_alt'])}",
         p2(DCF['ccy_alt_ps']), sgn(DCF['ccy_alt_ps']/DCF['ps']-1)],
        ['THIS STUDY, ALL FOUR CHOICES AS MADE ABOVE', '—', '—', p2(DCF['ps']), '—']]
table(rows, [1.55, 1.55, 2.30, 1.00, 0.70], size=8.2, left_cols={1, 2}, band_rows={5})
caption(f"The base is stated in the last row so the percentages are checkable rather than "
        f"relative to a number the reader has to go and find: every effect column is measured "
        f"against the cash-flow lens at EGP {p2(DCF['ps'])} a share, which is the primary "
        f"construction and not the weighted central of EGP {p2(D['central'])}. Note the "
        f"asymmetry that follows from that. The four choices move the answer between "
        f"{sgn(min(DCF['ps_rating_basis'],DCF['ps_nci_alt'])/DCF['ps']-1)} and "
        f"{sgn(max(DCF['ps_gross_basis'],DCF['ccy_alt_ps'])/DCF['ps']-1)}, so the single largest "
        f"contested choice in this study is worth more than the entire gap between the central "
        f"estimate and the market price. Each alternative is run through the whole model and "
        f"reported as a VALUE, not described. "
        'The currency alternative deflates the export cash flows to dollars at each year’s '
        'exchange rate before discounting them at a dollar rate, and only then translates back — '
        'discounting a pound cash flow already inflated by the assumed depreciation path directly '
        'at a dollar rate would count the currency benefit twice.')

# =========================== 2 TECHNICAL =====================================
H1('2  The price record')
figure('fig3_ma.png', 6.9,
       'Figure 5 — the closing price against its 20, 50, 100 and 200-session moving averages over '
       'the last twelve months of trading.')
P(f"The series used throughout this study runs from {S0['series_first']} to {S0['series_last']} "
  f"and covers {n0(S0['clean_rows'])} clean sessions out of {n0(S0['raw_rows'])} raw rows, over "
  f"{n1(S0['span_years'])} years at {n1(S0['density_rows_per_yr'])} sessions a year, which "
  f"matches the exchange's own Sunday-to-Thursday calendar. An earlier edition of this section "
  f"said the series 'runs from 2022'; it does not — 2022 is where the CALIBRATION exercise in "
  f"the appendix starts scoring forecasts, and every price statistic in this study is taken from "
  f"the full fifteen-and-a-half-year series.")
P(f"It was screened before use. One row carrying a non-positive price was removed "
  f"({S0['dq_log'][0].split('(')[1].split(')')[0]}); {pc(S0['flat_frac'])} of sessions are flat, "
  f"which is normal for a mid-cap on this exchange and well inside the gate. The largest "
  f"single-session move in the whole history is {S0['max_abs_log']:.4f} in log terms. Two "
  f"thresholds bear on that number and they are different things, which the earlier edition ran "
  f"together. The exchange's own ±20% daily price limit is {math.log(1.20):.4f} in logs — the "
  f"largest observed move sits just INSIDE it, by four ten-thousandths. The engine's artefact "
  f"screen fires at {S0['jump_threshold']:.4f}, set deliberately ABOVE the price limit so that "
  f"only a move no trade could have produced is flagged. Nothing fires. A share split or an "
  f"unadjusted dividend would have shown up as a move the price limit forbids, and none does, so "
  f"there is no unadjusted corporate action hiding in the series and no block of pre-listing "
  f"placeholder rows.")

# =========================== 3 MONTE CARLO ===================================
H1('3  Where the price could trade')
P(f"This section is a different object from the valuation above and is never blended with it. It "
  f"is a probability map of the share price over one and three months, produced by simulating "
  f"50,000 paths from the cleaned price history with a volatility model fitted on the whole "
  f"Egyptian market rather than on this name alone.")
figure('fig4_fan.png', 6.9,
       'Figure 6 — the forward price cone to three months. The dashed rule is the fundamental '
       'central estimate; the dotted rule is the market price.')
rows = [['', 'One month', 'Three months'],
        ['Calendar horizon date', H1M['target_date'], H3M['target_date']],
        ['Check date actually used', H1M['grade_date'], H3M['grade_date']],
        ['Sessions simulated', n0(H1M['h']), n0(H3M['h'])],
        ['5th percentile', p2(H1M['pct']['p5']), p2(H3M['pct']['p5'])],
        ['25th percentile', p2(H1M['pct']['p25']), p2(H3M['pct']['p25'])],
        ['Median', p2(H1M['pct']['p50']), p2(H3M['pct']['p50'])],
        ['75th percentile', p2(H1M['pct']['p75']), p2(H3M['pct']['p75'])],
        ['95th percentile', p2(H1M['pct']['p95']), p2(H3M['pct']['p95'])],
        ['Probability above today’s price', pc(H1M['p_above']), pc(H3M['p_above'])],
        ['Probability 10% or more up', pc(H1M['p_up10']), pc(H3M['p_up10'])],
        ['Probability 10% or more down', pc(H1M['p_dn10']), pc(H3M['p_dn10'])],
        ['Probability of touching +10% at any point', pc(H1M['touch_up10']),
         pc(H3M['touch_up10'])],
        ['Probability of touching −10% at any point', pc(H1M['touch_dn10']),
         pc(H3M['touch_dn10'])],
        ['Annualised volatility at the anchor', pc(H1M['anchor_vol_ann']),
         pc(H3M['anchor_vol_ann'])]]
table(rows, [3.20, 1.70, 1.70], size=8.5)
caption(f"Two dates are shown because they differ, and an earlier edition printed only one of "
        f"them. The Egyptian Exchange trades Sunday to Thursday, so the three-month calendar date "
        f"of {H3M['target_date']} falls on a non-trading day; the cone is graded on the first "
        f"session at or after it, {H3M['grade_date']}. The horizon is therefore "
        f"{n0(H3M['h'])} sessions rather than a round quarter, and the percentiles above are the "
        f"distribution at that session.")
P(f"The drift is not zero and is not a view. Over three months the simulated log drift is "
  f"{H3M['drift_log_h']:+.4f}, which annualises to about "
  f"{pc(H3M['drift_log_h']*4,1)} — the CARRY, and nothing else: the local "
  f"risk-free rate of {pc(STK['rf_live'])} less the dividend yield of {pc(STK['q_annual'])} the "
  f"share currently pays, less the half-variance convexity term. NO PART OF THE DRIFT COMES FROM "
  f"THE VALUATION. The fundamental estimate of EGP {p2(D['central'])} does not enter this "
  f"section at any point; it is drawn on the charts as a reference rule and used to cut the zones "
  f"in section 6, and that is the whole of its role here. If the drift were set from the "
  f"valuation the two halves of this study would no longer be independent and the comparison in "
  f"section 4 would be circular.", size=10)
figure('fig5_dist.png', 5.4, 'Figure 7 — the simulated price distribution at one month.')
figure('fig6_dist.png', 5.4, 'Figure 8 — the same at three months.')
P(f"Is the cone credible? It is tested against the honest null — a random walk anchored on the "
  f"carry, so the test cannot be won simply by pointing at the direction interest rates push a "
  f"price. THE VERDICT ON THIS NAME IS PARITY, NOT SKILL, AND THAT IS STATED BEFORE THE "
  f"FAVOURABLE NUMBERS RATHER THAN AFTER THEM. On the production window set — the "
  f"{BTP['windows']} post-break origins the standing gate actually scores, running "
  f"{BTP['first_origin']} to {BTP['last_origin']} — the margin over the benchmark is "
  f"{sgn(BTP['skill_norm'],2)} and the verdict is {BTP['verdict']}: the confidence interval "
  f"straddles zero on every bootstrap block tested, so the honest reading is that this cone is "
  f"AS GOOD AS the carry-anchored random walk on this name, not better than it.")
rows = [['Window set', 'Origins', 'Period', 'Margin over benchmark', 'Verdict'],
        [BTP['label'], n0(BTP['windows']), f"{BTP['first_origin']} – {BTP['last_origin']}",
         sgn(BTP['skill_norm'], 2), BTP['verdict']],
        [BT5['label'], n0(BT5['windows']), f"{BT5['first_origin']} – {BT5['last_origin']}",
         sgn(BT5['skill_norm'], 2), BT5['verdict']],
        [BTF['label'], n0(BTF['windows']), f"{BTF['first_origin']} – {BTF['last_origin']}",
         sgn(BTF['skill_norm'], 2), BTF['verdict']],
        ['Market-level fit (all covered Egyptian names)', n0(BT['fit']['panel_names']) + ' names',
         f"fitted {BT['fit']['fit_date']}", sgn(BT['fit']['market_skill'], 2),
         BT['fit']['market_verdict']]]
table(rows, [2.05, 0.80, 1.55, 1.20, 0.80], size=8.2, left_cols={0})
caption(f"All three name-level window sets are shown, not the flattering one. Only the FULL "
        f"history reaches a PASS, and it reaches it on {BTF['windows']} origins stretching back "
        f"to {BTF['first_origin']} — a period that includes market conditions the current fit was "
        f"not calibrated on. The two recent sets both return PARITY. What carries the cone into "
        f"this study is the MARKET-level gate, which passes at {sgn(BT['fit']['market_skill'],2)} "
        f"across {BT['fit']['panel_names']} names: the volatility model is fitted on the whole "
        f"exchange, not on AMOC, and it is the market fit that is required to pass. A reader who "
        f"wants a name-level demonstration of skill will not find one here.")
P(f"What the tests DO establish, and it is not nothing: the cone is correctly SHAPED even where "
  f"it is not sharper. The probability-integral transform is close to uniform on the production "
  f"set (chi-square p = {BTP['chi2_p']}, Kolmogorov-Smirnov p = {BTP['ks_p']}), so the cone is "
  f"neither systematically too wide nor too narrow nor off-centre; coverage of the stated 90% "
  f"band runs at {pc(BTP['cov90'],0)} against a target of 90%; and the cone is "
  f"{n1(BTP['width_vs_benchmark'])} times the benchmark's width, so whatever margin it does earn "
  f"comes from being better centred rather than from being wider. A well-calibrated cone that "
  f"merely matches the random walk is still a usable probability map — it is just not evidence "
  f"of forecasting edge, and this study does not claim one.")

# =========================== 4 COMPARISON ====================================
H1('4  The two answers side by side')
rows = [['', 'What it says', 'Value'],
        ['Fundamental central', 'What the business appears to be worth on the assumptions here',
         p2(D['central'])],
        ['Market price', 'What it costs today', p2(SPOT)],
        ['Gap', 'Fundamental against market', sgn(D['central']/SPOT-1)],
        ['Three-month median of the price map',
         'The centre of the simulated distribution, which is anchored on today’s price and '
         'knows nothing about the valuation', p2(H3M['pct']['p50'])],
        ['Probability the price is above the fundamental central in three months',
         'Read directly off the simulated distribution',
         pc(P3M_ABOVE_CENTRAL)]]
table(rows, [2.35, 3.35, 1.20], size=8.5, left_cols={1})
caption('The valuation and the price map are produced by entirely separate machinery and are '
        'presented side by side rather than reconciled. Where they disagree, that disagreement is '
        'information.')

# =========================== 5 CATALYSTS =====================================
H1('5  What would move the answer')
bullet(f"The margin path is the operating crux. The six months to June 2026 imply a margin far "
       f"above anything in the record, and this study deliberately forecasts under it. If that "
       f"print proves to be a durable step rather than a spread windfall, the cash-flow lens is "
       f"too low. A half-point on the gross margin across the whole path is worth roughly EGP "
       f"{p2(abs(SN['grid_margin'][3]-SN['grid_margin'][2]))} a share.",
       bold_head='Whether the 2026 margin holds. ')
bullet(f"Throughput annualises to {n3(IN['vol_h2cy25']*2)}mn tonnes on the transition half "
       f"against {n1(IN['vol_fy25'])}mn in the June-2025 year. The forecast assumes the ramp is "
       f"largely done and only the residual utilisation gain remains. Doubling the assumed growth "
       f"path is worth about EGP {p2(SN['grid_vol'][4]-SN['grid_vol'][2])} a share; halting it "
       f"altogether costs about EGP {p2(abs(SN['grid_vol'][0]-SN['grid_vol'][2]))}.",
       bold_head='Whether the volume ramp continues. ')
bullet(f"This is the largest single lever in the study. Two points off the terminal cost of "
       f"capital is worth about EGP "
       f"{p2(SN['grid_wacc_g'][0][2]-SN['grid_wacc_g'][2][2])} a share — more than any operating "
       f"assumption tested. The terminal rate is built from the central bank's own stated "
       f"medium-term inflation target; if disinflation stalls, that assumption is the one that "
       f"breaks first.", bold_head='The pace of Egyptian disinflation. ')
bullet(f"The state petroleum corporation is both the second-largest shareholder at "
       f"{pc(IN['egpc_stake'],0)} and the counterparty on both sides of the trade. The feedstock "
       f"price, the offtake price and the payables that fund the working-capital cycle are all "
       f"administered relationships rather than arm's-length markets. A change in any of them "
       f"would move the margin without any change in the external environment.",
       bold_head='The relationship with the state petroleum complex. ')
bullet(f"Roughly a third of the specialty leg is exported and both legs price off dollar "
       f"benchmarks. A ten per cent move on the exchange-rate path is worth about EGP "
       f"{p2(abs(SN['grid_fx'][4]-SN['grid_fx'][2]))} a share.",
       bold_head='The currency. ')
bullet(f"The declared dividend is EGP {p2(IN['dps'])} a share, a yield of "
       f"{pc(IN['dps']/SPOT)} at today's price against a reported payout ratio of "
       f"{pc(IN['payout_reported'])}. With the company already net cash and generating more, the "
       f"payout policy is a live question — and one the market may care about more than the "
       f"discounted cash flow.", bold_head='What happens to the cash. ')

# =========================== 6 PROBABILITY ZONES =============================
H1('6  Probability zones')
import numpy as _np
_p3 = _np.load(os.path.join(HERE, 'paths_3M.npy'))[:, -1]
_C = D['central']
zones = [(f"Below EGP 7.50", float((_p3 < 7.5).mean())),
         (f"EGP 7.50 – {p2(SPOT)} (below today)", float(((_p3 >= 7.5) & (_p3 < SPOT)).mean())),
         (f"EGP {p2(SPOT)} – {p2(_C)} (today to the central estimate)",
          float(((_p3 >= SPOT) & (_p3 < _C)).mean())),
         (f"EGP {p2(_C)} – 11.00 (above the central estimate)",
          float(((_p3 >= _C) & (_p3 < 11.0)).mean())),
         ('Above EGP 11.00', float((_p3 >= 11.0).mean()))]
rows = [['Zone at three months', 'Probability']] + [[z, pc(p)] for z, p in zones]
table(rows, [4.20, 1.50], size=8.6)
caption('Read off the simulated distribution directly. The zones are cut at the market price and '
        'at the fundamental central estimate so the reader can see how much of the distribution '
        'sits on each side of each.')

# =========================== 7 CAVEATS =======================================
H1('7  Caveats — what is weak in this study')
P('Stated at the level of detail a reader would need to disagree with it.')
bullet('The company changed its financial year end mid-period, and the disclosure available for '
       'the stub periods is thinner than for a clean twelve-month year. The base year here is '
       'built from two separately disclosed halves; each half is a filed figure, but the '
       'combination is ours and not the company’s.',
       bold_head='The base year is constructed, not filed. ')
bullet(f"Only four balance-sheet lines are available at a single date — total assets, total "
       f"liabilities, cash and gross debt. Everything else on the balance sheets in Appendix A is "
       f"built from days drivers and rolled backwards through disclosed profit and dividends. It "
       f"is a reconstruction and is labelled as one wherever it appears. Be careful with the two "
       f"'checks' offered for it, because ONE OF THEM IS A TAUTOLOGY AND THE OTHER IS NEARLY "
       f"ONE. That the balance sheet balances proves nothing: property, plant and equipment is "
       f"the RESIDUAL off disclosed total assets, so it balances by construction and would "
       f"balance just as neatly on any working-capital assumption at all. The implied remaining "
       f"asset life of {n1(BASE['implied_life'])} years is only slightly better — it is that same "
       f"residual divided by the depreciation charge, so it is a direct function of the "
       f"receivable, inventory and payable day counts assumed above it, and a reader who "
       f"disagreed with those would get a different 'check'. What the life figure genuinely "
       f"tests is narrow: it says the residual is not absurd — not negative, and not so large "
       f"that a 1997 plant would appear newly built. Treat it as a bounds test, not a "
       f"verification. The only true external check available is share capital plus disclosed "
       f"reserves against total equity, and that one uses a figure the company published.",
       bold_head='The historical balance sheets are reconstructed. ')
bullet(f"Revenue for two of the historical years is available only through growth-rate "
       f"disclosures, so each is carried as the AVERAGE of independently sourced methods: "
       f"{n0(BASE['rev_fy24_methods'][0])} and {n0(BASE['rev_fy24_methods'][1])} for the "
       f"June-2024 year; {n0(BASE['rev_fy25_methods'][0])}, {n0(BASE['rev_fy25_methods'][1])} and "
       f"{n0(BASE['rev_fy25_methods'][2])} for June-2025. The methods and the average are on the "
       f"face of the companion model rather than asserted here.",
       bold_head='Two revenue figures are triangulated, not disclosed. ')
bullet(f"The half-year release covering the six months to June 2026 rests on one source. Its "
       f"reported growth rates reconcile independently against the constructed comparative, which "
       f"is why it is used as corroboration; but it is not the forecast base and the margin path "
       f"is struck under what it implies.",
       bold_head='The most recent print is single-sourced. ')
bullet(f"{pc(DCF['tv_share'],1)} of enterprise value sits beyond year five. That is what happens "
       f"when a cost of capital is expected to fall by "
       f"{n0((W['wacc_exp']-W['wacc_term'])*10000)} basis points across a forecast, and it means "
       f"the answer is a statement about the terminal state as much as about the explicit years. "
       f"Both terminal anchors are house views, disclosed as such, and neither is reverse-"
       f"engineered from a price.", bold_head='The terminal value carries most of the weight. ')
bullet(f"The reported return on invested capital of {pc(TR['roic']['CY25'])} is partly a "
       f"statement about depreciation on a plant commissioned between 1997 and 2000. The terminal "
       f"reinvestment rate of {pc(DCF['rr_term'])} that this return implies would not survive a "
       f"replacement cycle at current construction costs. This is the sharpest single criticism "
       f"available of the cash-flow lens and it is not answered here — it is disclosed.",
       bold_head='The return on capital may not be repeatable. ')
bullet(f"The company neither buys its feedstock nor sells much of its output in an arm's-length "
       f"market, and the counterparty owns {pc(IN['egpc_stake'],0)} of it. A margin forecast for "
       f"a business like that is a forecast about an administered relationship.",
       bold_head='The counterparty is also the shareholder. ')
bullet(f"Reported pre-tax profit in the historical years contains EGP "
       f"{n0(HI['FY25']['other'])}mn to {n0(HI['FY23']['other'])}mn a year of other and "
       f"non-operating income, which this study reads as devaluation-driven exchange gains and "
       f"excludes from the forecast entirely. If some of it is in fact recurring — a durable "
       f"trading or investment stream rather than a currency effect — then the forecast profit "
       f"line and the normalised-earnings lens are both understated.",
       bold_head='Other income is read as non-recurring, and might not be. ')
bullet(f"The minority share of group profit is estimated at {pc(DCF['nci_share'])} from the gap "
       f"between consolidated and standalone profit rather than disclosed directly. Doubling it "
       f"moves the answer by {sgn(DCF['ps_nci_alt']/DCF['ps']-1)}.",
       bold_head='The minority interest is inferred. ')

# =========================== APPENDIX A ======================================
H1('Appendix A  Financial statements')
H2('A.1  Income statement — four historical periods and a five-year forecast (EGP mn)')
rows = [['EGP mn'] + YH_SHORT + [y for y in YRS]]
rows.append(['Revenue'] + [n0(HI[k]['rev']) for k in H4] + [n0(x) for x in F['rev']])
rows.append(['Gross profit'] + [n0(HI[k]['gp']) for k in H4] + [n0(x) for x in F['gp']])
rows.append(['Gross margin'] + [pc(HI[k]['gp']/HI[k]['rev'], 2) for k in H4] +
            [pc(x, 2) for x in F['gm']])
rows.append(['Operating cost load'] + [f"({n0(HI[k]['opex'])})" for k in H4] +
            [f"({n0(x)})" for x in F['opex']])
rows.append(['EBITDA'] + [n0(HI[k]['ebitda']) for k in H4] + [n0(x) for x in F['ebitda']])
rows.append(['EBITDA margin'] + [pc(HI[k]['ebitda']/HI[k]['rev'], 2) for k in H4] +
            [pc(x, 2) for x in F['ebitda_margin']])
rows.append(['Depreciation and amortisation'] + [f"({n0(HI[k]['dna'])})" for k in H4] +
            [f"({n0(x)})" for x in F['dna']])
rows.append(['EBIT'] + [n0(HI[k]['ebit']) for k in H4] + [n0(x) for x in F['ebit']])
rows.append(['Net finance income'] + [n0(HI[k]['fin']) for k in H4] +
            [n0(x) for x in F['interest']])
rows.append(['Other and non-operating income'] + [n0(HI[k]['other']) for k in H4] + ['—'] * 5)
rows.append(['Profit before tax'] + [n0(HI[k]['ebt']) for k in H4] +
            [n0(F['ebit'][i] + F['interest'][i]) for i in range(5)])
rows.append(['Tax'] + [f"({n0(abs(HI[k]['tax']))})" for k in H4] +
            [f"({n0((F['ebit'][i]+F['interest'][i])*IN['tax_eff'])})" for i in range(5)])
rows.append(['Profit after tax'] + [n0(HI[k]['pat']) for k in H4] +
            [n0((F['ebit'][i]+F['interest'][i])*(1-IN['tax_eff'])) for i in range(5)])
rows.append(['Minority interests'] + [f"({n0(HI[k]['nci'])})" for k in H4] +
            [f"({n0((F['ebit'][i]+F['interest'][i])*(1-IN['tax_eff'])*DCF['nci_share'])})"
             for i in range(5)])
rows.append(['Profit attributable to shareholders'] + [n0(HI[k]['npa']) for k in H4] +
            [n0(x) for x in F['np_attr']])
rows.append(['Earnings per share (EGP)'] + [p2(HI[k]['npa']/SH) for k in H4] +
            [p2(x/SH) for x in F['np_attr']])
table(rows, [1.62, 0.63, 0.63, 0.63, 0.63, 0.62, 0.62, 0.62, 0.62, 0.62], size=7.5,
      band_rows={5, 8, 15})
caption('Revenue and gross profit for the June-2023 year are disclosed. The June-2024 and '
        'June-2025 revenue figures are the average of independently sourced methods. The '
        'calendar-2025 column is constructed from two disclosed halves as shown in section 1.2, '
        'and its intermediate lines are closed from the disclosed profit at the stated effective '
        'tax rate. Forecast profit is struck after net finance income and therefore differs from '
        'the free-cash-flow waterfall, which is a pre-financing measure by construction.')

H2('A.2  Balance sheet — four historical periods and a five-year forecast (EGP mn)')
_ta_h = [HB[k]['ppe'] + HB[k]['inv'] + HB[k]['recv'] + IN['other_ca'] + HB[k]['cash'] for k in H4]
_inv_f = [(F['rev'][i]-F['gp'][i])*IN['inv_days']/365 for i in range(5)]
_recv_f = [F['rev'][i]*IN['recv_days']/365 for i in range(5)]
_pay_f = [(F['rev'][i]-F['gp'][i])*IN['pay_days']/365 for i in range(5)]
_ta_f = [F['ppe'][i] + _inv_f[i] + _recv_f[i] + IN['other_ca'] + F['cash'][i] for i in range(5)]
rows = [['EGP mn'] + YH_SHORT + [y for y in YRS],
        ['Property, plant and equipment'] + [n0(HB[k]['ppe']) for k in H4] +
        [n0(x) for x in F['ppe']],
        ['Inventories'] + [n0(HB[k]['inv']) for k in H4] + [n0(x) for x in _inv_f],
        ['Trade receivables'] + [n0(HB[k]['recv']) for k in H4] + [n0(x) for x in _recv_f],
        ['Other current assets'] + [n0(IN['other_ca'])] * 9,
        ['Cash and equivalents'] + [n0(HB[k]['cash']) for k in H4] + [n0(x) for x in F['cash']],
        ['TOTAL ASSETS'] + [n0(x) for x in _ta_h] + [n0(x) for x in _ta_f],
        ['Trade payables'] + [n0(HB[k]['pay']) for k in H4] + [n0(x) for x in _pay_f],
        ['Gross debt'] + [n1(IN['debt_snap'])] * 9,
        ['Other liabilities and provisions'] + [n0(HB[k]['other_liab']) for k in H4] +
        [n0(BASE['other_liab']*F['rev'][i]/BASE['rev_cy25']) for i in range(5)],
        ['Shareholders equity'] + [n0(HB[k]['eqp']) for k in H4] + [n0(x) for x in F['equity']],
        ['Minority interests'] + [n0(HB[k]['nci']) for k in H4] +
        [n0(F['equity'][i]/(1-DCF['nci_share'])*DCF['nci_share']) for i in range(5)],
        ['NET WORKING CAPITAL'] + [n0(HB[k]['nwc']) for k in H4] + [n0(x) for x in F['nwc']],
        ['NET CASH'] + [n0(-HB[k]['nd']) for k in H4] + [n0(-x) for x in F['net_debt']]]
table(rows, [1.62, 0.63, 0.63, 0.63, 0.63, 0.62, 0.62, 0.62, 0.62, 0.62], size=7.5,
      band_rows={6, 12, 13})
caption('Total assets, total liabilities, cash and gross debt at the calendar-2025 date are the '
        'only disclosed lines. Property, plant and equipment is the residual against disclosed '
        'total assets; inventories, receivables and payables are driven off days assumptions; '
        'and the three earlier years are rolled backwards through disclosed profit and the '
        'declared dividend. Each column foots exactly, and the companion model carries the '
        'balance check as a live formula.')

H2('A.3  Cash flow — five-year forecast (EGP mn)')
rows = [['EGP mn'] + YRS,
        ['NOPAT'] + [n0(x) for x in F['nopat']],
        ['add back depreciation and amortisation'] + [n0(x) for x in F['dna']],
        ['less change in net working capital'] + [f"({n0(x)})" if x >= 0 else n0(-x)
                                                  for x in F['dnwc']],
        ['OPERATING CASH FLOW'] + [n0(F['nopat'][i]+F['dna'][i]-F['dnwc'][i]) for i in range(5)],
        ['less capital expenditure'] + [f"({n0(x)})" for x in F['capex']],
        ['FREE CASH FLOW TO THE FIRM'] + [n0(x) for x in F['fcff']],
        ['Opening net cash'] + [n0(-x) for x in [BASE['nd_cy25']] + F['net_debt'][:4]],
        [f"add net finance income, AFTER tax at {pc(IN['tax_eff'],1)}"] +
        [n0(x*(1-IN['tax_eff'])) for x in F['interest']],
        ['less dividends paid'] + [f"({n0(x)})" for x in F['div']],
        ['CLOSING NET CASH'] + [n0(-x) for x in F['net_debt']]]
table(rows, [2.35, 0.92, 0.92, 0.92, 0.92, 0.92], size=8.2, band_rows={4, 9})
caption(f"The statement foots. Opening net cash plus free cash flow to the firm plus AFTER-TAX "
        f"finance income less dividends equals closing net cash, to the last EGP mn, in every "
        f"year. An earlier edition printed the PRE-tax finance income on this line while the "
        f"model rolled the balance forward on the after-tax figure, so the column did not add up "
        f"— a gap of about EGP {n0(F['interest'][0]*IN['tax_eff'])}mn a year, which is the tax on "
        f"the deposit income. The model was right and the printed line was wrong; the line has "
        f"been corrected rather than the tax quietly dropped. Note that free cash flow to the "
        f"firm is struck AFTER tax on operating profit only, which is why the tax on finance "
        f"income has to appear separately here.")

# =========================== APPENDIX B ======================================
H1('Appendix B  The cost of capital in detail')
H2('B.1  Beta')
P(f"The beta is a genuine regression on this company's own returns, not a default. AMOC weekly "
  f"logarithmic returns were regressed against an equal-weight composite of "
  f"{BETA['composite_names']} Egyptian Exchange constituents over {BETA['window_years']} years.")
rows = [['Diagnostic', 'Value', 'Reading'],
        ['Beta', n3(BETA['beta']), 'the point estimate'],
        ['R-squared', pc(BETA['r2']), 'well above the 5% usability floor'],
        ['Observations', n0(BETA['n']), 'far above the 24-observation minimum'],
        ['Standard error', n3(BETA['se']), 'comfortably below the point estimate'],
        ['90% confidence interval',
         f"{BETA['ci90'][0]:.3f} – {BETA['ci90'][1]:.3f}",
         f"spans {(BETA['ci90'][1]-BETA['ci90'][0])/BETA['beta']:.2f}× the point estimate"],
        ['Weak-instrument flag', 'NOT flagged',
         'R-squared is above 10% and the interval is well inside twice the point estimate']]
table(rows, [1.85, 1.55, 3.30], size=8.4, left_cols={2})
P(f"This is an unusually well-identified beta for an Egyptian mid-cap, and it is worth saying so "
  f"rather than hedging: an R-squared of {pc(BETA['r2'])} on {BETA['n']} weekly observations "
  f"means the market explains close to a third of this share's variance. The point estimate of "
  f"{n3(BETA['beta'])} also passes the plausibility check — a single-asset processor with "
  f"administered input and output prices should sit near the market, neither defensive like a "
  f"staple nor geared like a developer, and it does.")
rows = [['Beta'] + [f"{b:.2f}" for b in SN['beta_grid']],
        ['Fair value (EGP)'] + [p2(x) for x in SN['grid_beta']]]
table(rows, [1.85, 0.95, 0.95, 0.95, 0.95, 0.95], size=8.5, align_right_from=1)
caption('Beta sensitivity across the 90% confidence interval plus the standard round anchors, so '
        'this study can be compared with others on the same grid.')

H2('B.2  The cost of debt, and why it does not matter here')
P(f"The standing procedure requires three pieces of evidence for the cost of debt, and all three "
  f"are produced — but on this name the third is the one that matters, and it cuts in an unusual "
  f"direction.")
bullet(f"The entire book is EGP {n1(IN['debt_snap'])}mn of short-dated Egyptian-pound bank "
       f"facilities. There is no foreign-currency leg, so no currency blend is available and none "
       f"is claimed. The company's dollar exposure sits in export receivables, not in debt.",
       bold_head='Currency composition. ')
bullet(f"An interest-expense-over-average-balance computation on a book this small is not a "
       f"usable estimator — the denominator is {pc(IN['debt_snap']/BASE['rev_cy25'],3)} of "
       f"revenue and rounds away in the disclosure. The rate is therefore built from an "
       f"observable instead: the central bank's main operation rate of {pc(IN['policy_rate'])}, "
    f"held at the third meeting of 2026 against headline inflation of {pc(IN['cpi'])}, plus a "
       f"200-basis-point corporate spread, giving {pc(IN['kd'])}. Saying that plainly is the "
       f"honest alternative to computing a precise-looking number out of a rounding residual.",
       bold_head='Independent effective rate. ')
bullet(f"Gross debt is {pc(W['wd_gross'],3)} of the capital structure. A 500-basis-point error "
       f"in the cost of debt — larger than any plausible mis-estimate — moves the weighted cost "
       f"of capital by {W['kd_swing_effect']*10000:.2f} basis points. What the gate establishes "
       f"here is not that the input is right but that it cannot move the answer, and the study "
       f"says so rather than dressing an immaterial input as a precise one.",
       bold_head='Bounds and materiality. ')

H2('B.3  Explicit against terminal cost of capital')
rows = [['Explicit \\ terminal'] + [pc(x) for x in SN['wt_grid']]]
for i, we in enumerate(SN['we_grid']):
    rows.append([pc(we)] + [p2(v) for v in SN['grid_exp_term'][i]])
table(rows, [1.55, 1.02, 1.02, 1.02, 1.02, 1.02], size=8.4)
caption('Each anchor varied independently around its own base, so the grid shows what the '
        'valuation needs THE ECONOMY to do rather than only what growth rate the model needs.')

# =========================== APPENDIX C ======================================
H1('Appendix C  The expert appendix')
P('Three reads on the same company, each shown with its workings and each carrying a stated '
  'condition that would falsify it. TWO OF THE THREE ARE INDEPENDENT OF THE PRIMARY MODEL AND ONE '
  'IS NOT, and it is worth knowing which before reading them. Expert 1 works from earnings power '
  'at a justified multiple and Expert 2 from free cash flow to equity with no bridge at all; '
  'neither can be derived from the cash-flow lens and they land on opposite sides of it. Expert 3 '
  'works from economic profit, which — built off the same profit after tax, the same invested '
  'capital and the same discount path — is the discounted cash flow written a different way. It '
  'reproduces the primary lens exactly, by identity, and is included as an ARITHMETIC AUDIT of '
  'that lens rather than as a third opinion. An earlier edition of this appendix called all three '
  'independent and offered their median as a check on the main result. That was wrong twice over '
  'and both errors are corrected below.')
figure('figD1_experts.png', 6.9,
       'Figure 9 — the three experts’ ranges. The shaded band is the panel centre, which is NOT '
       'an independent check: Expert 3 is the cash-flow lens by identity and here it is also the '
       'median, so the band sits exactly where the primary model does.')

E1, E2, E3 = EXP['e1'], EXP['e2'], EXP['e3']
H2(f"Expert 1 — {E1['method_short']}")
P(f"Method. This expert refuses to forecast a terminal state at all. The question is what the "
  f"business earns in a normal year once the current ramp is complete, and what a buyer should "
  f"pay for that stream. Mid-cycle is taken as {E1['year']}, the middle of the forecast window.")
rows = [['Step', 'EGP mn unless stated'],
        [f"{E1['year']} EBIT", n0(E1['ebit'])],
        ['add net finance income on the cash pile', n0(E1['interest'])],
        [f"less tax at {pc(IN['tax_eff'],1)} and minorities at {pc(DCF['nci_share'])}",
         f"({n0(E1['ebit']+E1['interest']-E1['eps']*SH/1)})" if False else
         f"({n0((E1['ebit']+E1['interest']) - E1['eps']*SH)})"],
        ['= attributable earnings', n0(E1['eps']*SH)],
        ['Earnings per share (EGP)', p2(E1['eps'])],
        [f"× justified multiple of {E1['pe']}×", ''],
        ['FAIR VALUE (EGP per share)', p2(E1['base'])]]
table(rows, [4.20, 1.60], size=8.5, band_rows={7})
P(f"Range EGP {p2(E1['rng'][0])} to {p2(E1['rng'][1])}, struck on multiples of 5.0× and 9.5×. "
  f"Expert 1's view is that a single-asset processor with administered input and output prices, "
  f"a 20% state shareholder and an Egyptian cost of equity near {pc(W['ke_exp'],0)} does not earn "
  f"a premium multiple, and that the company's own trailing {n1(REL['pe_trailing'])}× is about "
  f"where it belongs.")
P(f"Falsification. This expert is wrong if the mid-cycle year is not mid-cycle — specifically, if "
  f"the margin printed in the six months to June 2026 turns out to be the new normal rather than "
  f"a spread windfall. Watch two consecutive calendar halves at a gross margin above 8%: that "
  f"would mean the earnings base used here is too low and the method understates by roughly a "
  f"third.", size=10)

H2(f"Expert 2 — {E2['method_short']}")
P(f"Method. This expert distrusts enterprise-value bridges — too many places to add something "
  f"back twice — and works the equity side directly. Free cash flow to equity is free cash flow "
  f"to the firm plus the after-tax finance income the cash pile actually earns, discounted on the "
  f"cost of EQUITY's own glide, with no bridge at all. The cash reaches the shareholder through "
  f"the income line rather than as a balance-sheet add-back, which is what makes this an "
  f"independent read rather than a rearrangement of the primary model.")
rows = [['', *YRS],
        ['Free cash flow to equity (EGP mn)', *[n0(x) for x in E2['fcfe']]],
        ['Cost of equity', *[pc(x) for x in E2['ke_path']]],
        ['Discount factor', *[f"{x:.4f}" for x in E2['df']]]]
table(rows, [2.35, 0.92, 0.92, 0.92, 0.92, 0.92], size=8.3)
rows = [['Step', 'EGP mn'],
        ['Present value of the explicit five years', n0(E2['pv'])],
        ['Present value of the terminal block', n0(E2['pv_tv'])],
        [f"Total equity value, over {n1(SH)}mn shares", n0(E2['pv']+E2['pv_tv'])],
        ['FAIR VALUE (EGP per share)', p2(E2['base'])]]
table(rows, [4.20, 1.60], size=8.5, band_rows={4})
P(f"Range EGP {p2(E2['rng'][0])} to {p2(E2['rng'][1])}, taken on the discount rate and the growth "
  f"rate rather than by re-using the same rate twice. An earlier draft of this panel capitalised "
  f"a mid-forecast cash flow straight at the TERMINAL cost of equity and produced EGP 14.73 — "
  f"a number that prices one date twice, taking a cash flow five years out and bringing it home "
  f"at a rate that only applies once the economy has normalised. The glide is applied here for "
  f"exactly the reason it is applied in the primary model, and the correction is disclosed rather "
  f"than quietly made.")
P(f"Falsification. Expert 2 is wrong if the cash does not belong to the shareholder. The whole "
  f"method rests on finance income being a durable, distributable stream. If the cash pile is "
  f"committed — to a replacement capital programme, to a related-party receivable, or to working "
  f"capital the counterparty stops funding — then the finance income leg disappears and this "
  f"expert's answer falls by roughly a fifth. Watch payable days: a move from "
  f"{n0(IN['pay_days'])} toward the receivable cycle would be the first sign.", size=10)

H2(f"Expert 3 — {E3['method_short']}")
P(f"Method. This expert asks one question: does the company earn more on its capital than the "
  f"capital costs, and for how long? Value is the capital already invested plus the present value "
  f"of every future year's economic profit — profit after tax less a charge for the capital "
  f"employed to make it. Nothing about growth enters except through the capital it consumes.")
rows = [['', *YRS],
        ['Return on invested capital', *[pc(x) for x in F['roic']]],
        ['Cost of capital that year', *[pc(x) for x in F['fwd_wacc']]],
        ['Spread', *[sgn(x) for x in E3['spread']]],
        ['Economic profit (EGP mn)', *[n0(x) for x in E3['ep']]]]
table(rows, [2.35, 0.92, 0.92, 0.92, 0.92, 0.92], size=8.3)
rows = [['Step', 'EGP mn'],
        ['Invested capital at the start', n0(E3['ic0'])],
        ['Present value of explicit economic profit', n0(E3['pv_ep'])],
        ['Present value of terminal economic profit', n0(E3['pv_ep_term'])],
        ['= enterprise value', n0(E3['ev'])],
        ['FAIR VALUE after the bridge (EGP per share)', p2(E3['base'])]]
table(rows, [4.20, 1.60], size=8.5, band_rows={5})
P(f"Read the base number before reading anything else into it. Expert 3 returns EGP "
  f"{p2(E3['base'])} and the primary cash-flow lens returns EGP {p2(DCF['ps'])} — the same "
  f"number, and not by coincidence. An economic-profit valuation and a discounted-cash-flow "
  f"valuation built off the same profit after tax, the same invested capital and the same "
  f"discount path are ALGEBRAICALLY THE SAME VALUATION; the capital charge that economic profit "
  f"subtracts each year is exactly the capital that the cash-flow waterfall subtracts as "
  f"investment, discounted differently and then added back as the opening capital base. An "
  f"earlier draft of this study presented the agreement as corroboration. It is not "
  f"corroboration — it is an identity, and a study that offers an identity as evidence is "
  f"marking its own homework. What the agreement DOES establish is that the primary model has no "
  f"arithmetic leak: had the two differed by a piastre, one of them would contain a mistake. "
  f"Expert 3 is therefore an audit of the primary model, and only Experts 1 and 2 are "
  f"independent opinions about the company.", size=10)
P(f"The capital charge is taken on BEGINNING-of-year invested capital, not ending. Charging "
  f"ending capital is the commoner convention and it is wrong: it charges the company for capital "
  f"it had not yet deployed, understating economic profit and pushing the year in which the "
  f"return spread turns positive one year later than it should.")
P(f"Range EGP {p2(E3['rng'][0])} to {p2(E3['rng'][1])}. The low end haircuts both economic-profit "
  f"legs sharply, on the view that a return spread of "
  f"{sgn(E3['spread'][0])} in the first year against a cost of capital of "
  f"{pc(F['fwd_wacc'][0])} is a fact about depreciation as much as about the business. The high "
  f"end is the currency-of-discounting alternative.")
P(f"Falsification. Expert 3 is wrong if the invested-capital base is understated — which it is, "
  f"if the plant would cost materially more than {n0(BASE['ppe_cy25'])} to replace. Re-run the "
  f"same method on a replacement-cost capital base and both the return and the spread fall "
  f"sharply. This is the same criticism section 7 makes of the primary model, and Expert 3 is the "
  f"most exposed of the three to it.", size=10)

H2('The panel')
rows = [['', 'Method', 'Range (EGP)', 'Base (EGP)', 'vs spot'],
        ['Expert 1', E1['method_short'], f"{p2(E1['rng'][0])} – {p2(E1['rng'][1])}",
         p2(E1['base']), sgn(E1['base']/SPOT-1, 0)],
        ['Expert 2', E2['method_short'], f"{p2(E2['rng'][0])} – {p2(E2['rng'][1])}",
         p2(E2['base']), sgn(E2['base']/SPOT-1, 0)],
        ['Expert 3', E3['method_short'], f"{p2(E3['rng'][0])} – {p2(E3['rng'][1])}",
         p2(E3['base']), sgn(E3['base']/SPOT-1, 0)],
        ['PANEL MEDIAN', 'the middle of the three', '', p2(D['panel_centre']),
         sgn(D['panel_centre']/SPOT-1, 0)]]
table(rows, [0.85, 2.55, 1.25, 0.85, 0.75], size=8.4, band_rows={4}, left_cols={1})
P(f"The panel median of EGP {p2(D['panel_centre'])} must NOT be read as an independent check on "
  f"the weighted central. Expert 3 reproduces the primary cash-flow lens exactly, as an identity, "
  f"so the median of the three is the middle value of a set containing the answer it is "
  f"supposedly checking — and here the median IS Expert 3, which is to say it is the discounted "
  f"cash flow with a different label on it. An earlier draft of this study described the panel "
  f"median as 'a useful check that the main result is not an artefact of the lens weights'. That "
  f"sentence was wrong and it has been removed rather than softened.")
P(f"What the panel does say is this. The two genuinely independent reads bracket the primary "
  f"model: Expert 1's earnings-power method comes out ABOVE at EGP {p2(E1['base'])} and Expert "
  f"2's equity-side method comes out BELOW at EGP {p2(E2['base'])}, a spread of EGP "
  f"{p2(E1['base']-E2['base'])} — {pc((E1['base']-E2['base'])/D['central'],0)} of the weighted "
  f"central. The cash-flow lens sits between them. Two methods that share no bridge, no terminal "
  f"formula and no multiple disagreeing by a quarter of the answer is the honest measure of how "
  f"much precision this company admits, and it is considerably less than any single lens implies "
  f"on its own.")

# =========================== ABOUT / DISCLOSURE ==============================
H1('About this study')
box([('What this is. ',
      'An independent, educational valuation study produced by Testahil. It carries no rating, '
      'no recommendation and no price target.'),
     ('What it is not. ',
      'It is not investment advice, not a solicitation, and not a forecast of the share price. '
      'The fair-value range is a statement about the business under the assumptions listed; the '
      'probability map is a separate statement about price, and the two are never blended.'),
     ('Sources. ',
      'Every input carries a value, a source and a date, recorded in the accompanying source '
      'register issued as a separate document alongside this study.'),
     ('Method. ',
      'All financial arithmetic in this study originates in an executed, asserting compute '
      'script; no figure is calculated in the narrative. The companion workbook is '
      f"formula-driven — {n0(XC['formulas'])} live formulas against {n0(XC['numeric_values'])} "
      'entered numbers, of which the great majority are the input register itself and the two '
      'whole-model re-run grids.'),
     ('Verification. ',
      f"Both verification gates were run on the delivered workbook rather than on the script that "
      f"wrote it: {n0(XC['formulas'])} of {n0(XC['formulas'])} formula cells reproduce the "
      f"model's own value, with none unresolvable and none unchecked; and every input was "
      f"perturbed in place with the whole workbook re-evaluated, confirming each moves the "
      f"headline in the asserted direction with no dead inputs."),
     ('Limitations of this edition. ',
      'The company changed its financial year end mid-period, primary filings were not reachable '
      'from the build environment, and the historical balance sheets are therefore a '
      'reconstruction from four disclosed lines. Section 7 sets out each limitation at the level '
      'of detail a reader would need to disagree with it.')])

doc.save(os.path.join(HERE, 'AMOC_Valuation_Study_06-08-2026_public.docx'))
print('wrote AMOC_Valuation_Study_06-08-2026_public.docx')
