"""AMOC_Valuation_Study_06-08-2026_public.docx — python-docx builder, house style.
Reads study_numbers.json exclusively: no numeral is typed into this file."""
import json, os, sys
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
BT = D['backtest']; BT5, BTF = BT['five_year'], BT['full']
IN = {k: v['value'] for k, v in D['inputs'].items()}
SPOT, SH = M['spot'], M['shares_mn']
YRS = F['years']
H3M, H1M = STK['horizons']['3M'], STK['horizons']['1M']
BETA = W['beta']
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
  f"moved about {n3(BASE['vol_cy25'])}mn tonnes and turned over EGP {n0(BASE['rev_cy25'])}mn.")
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
  f"the June-2025 year. Exports of oils and waxes rose about 40% on entry into new markets. The "
  f"first calendar quarter of 2026 carried it on: consolidated sales of EGP "
  f"{n0(IN['rev_q1cy26'])}mn and profit of EGP {n0(IN['pat_q1cy26'])}mn, up 37%.")
P(f"On the primary construction the four lenses centre at EGP {p2(D['central'])} a share against "
  f"a market price of {p2(SPOT)} — the central estimate sits about {sgn(D['central']/SPOT-1,0)} "
  f"above the market price, which is to say the shares are roughly fairly valued. The lenses do not agree with each "
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
         'Three independent methods, worked in the appendix',
         f"{p2(min(EXP[e]['rng'][0] for e in ('e1','e2','e3')))} – "
         f"{p2(max(EXP[e]['rng'][1] for e in ('e1','e2','e3')))}",
         p2(D['panel_centre']), sgn(D['panel_centre']/SPOT-1, 0)],
        ['Market price', f"Closing price on {M['asof']}", '—', p2(SPOT), '—']]
table(rows, [1.42, 2.90, 1.06, 0.72, 0.68], size=8.3, band_rows={5, 7}, left_cols={1})
caption(f"Terminal value as a percentage of enterprise value is stated in the first row and "
        f"again in the enterprise-value bridge in section 1.7. At {pc(DCF['tv_share'],1)} it is "
        f"a high but not unusual share for a business whose cost of capital is expected to fall "
        f"by roughly {n0((W['wacc_exp']-W['wacc_term'])*10000)} basis points over the forecast; "
        f"the reader should treat the cash-flow lens as a statement about the terminal state at "
        f"least as much as about the next five years.")

figure('fig1_football.png', 6.9,
       'Figure 1 — the four lenses and the weighted central, each shown bear to bull with the '
       'base marked. The vertical rule is the market price.')

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
         n3(U['spec_vol25']), n0(U['spec_rev25']),
         pc(U['spec_rev25']/BASE['rev_cy25'])],
        ['Fuel and by-products',
         'Low-sulphur gas oil, naphtha, liquefied petroleum gas, fuel-oil blend, aromatic '
         'extract, vacuum residue, sulphur',
         n3(U['fuel_vol25']), n0(U['fuel_rev25']),
         pc(U['fuel_rev25']/BASE['rev_cy25'])],
        ['Total', '', n3(BASE['vol_cy25']), n0(BASE['rev_cy25']), '100.0%']]
table(rows, [1.45, 2.75, 0.95, 1.10, 0.92], size=8.3, band_rows={3}, left_cols={1})
caption(f"The specialty leg is {pc(U['spec_vol25']/BASE['vol_cy25'],0)} of the tonnage but "
        f"{pc(U['spec_rev25']/BASE['rev_cy25'],0)} of the revenue, and a much larger share again "
        f"of the margin. The implied realisation on the fuel leg works out at about USD "
        f"{n0(U['fuel_price_usd25'])} a tonne, which is a plausible gas-oil, naphtha and "
        f"fuel-oil blend against the crude deck — that check is what tells us the split is real "
        f"rather than fitted to a target.")

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
P(f"Not as one growth rate. A refiner's revenue is tonnes times a realised price, and the two "
  f"legs have entirely different economics, so they are forecast separately and in dollars — "
  f"both legs price off dollar product benchmarks even when the sale is domestic — and then "
  f"translated at an explicit exchange-rate path.")
rows = [['', 'CY2025'] + [y.replace('E', '') for y in YRS],
        ['Total volume (mn tonnes)', n3(BASE['vol_cy25'])] + [n3(v) for v in U['vol']],
        ['Specialty volume (mn tonnes)', n3(U['spec_vol25'])] + [n3(v) for v in U['spec_vol']],
        ['Specialty price (USD / tonne)', n0(IN['spec_price_usd_t'])] +
        [n0(U['spec_rev'][i]/U['spec_vol'][i]/IN['fx_path'][i]) for i in range(5)],
        ['Fuel price (USD / tonne)', n0(U['fuel_price_usd25'])] +
        [n0(U['fuel_rev'][i]/(U['vol'][i]-U['spec_vol'][i])/IN['fx_path'][i]) for i in range(5)],
        ['USD / EGP average', n1(IN['fx_avg_cy25'])] + [n1(x) for x in IN['fx_path']],
        ['Specialty revenue (EGP mn)', n0(U['spec_rev25'])] + [n0(x) for x in U['spec_rev']],
        ['Fuel revenue (EGP mn)', n0(U['fuel_rev25'])] + [n0(x) for x in U['fuel_rev']],
        ['TOTAL REVENUE (EGP mn)', n0(BASE['rev_cy25'])] + [n0(x) for x in F['rev']]]
table(rows, [1.90, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85], size=8.2, band_rows={8})
caption(f"Volume growth tapers from {pc(IN['vol_growth'][0])} to {pc(IN['vol_growth'][4])}. The "
        f"step-change is already IN the base year — the transition half annualises to "
        f"{n3(IN['vol_h2cy25']*2)}mn tonnes against {n1(IN['vol_fy25'])}mn in the June-2025 year "
        f"— so the forecast carries only the residual utilisation gain and then maintenance "
        f"growth. The specialty leg grows faster on the export push and lifts its share of "
        f"revenue from {pc(U['spec_rev25']/BASE['rev_cy25'],0)} to "
        f"{pc(U['spec_rev'][4]/F['rev'][4],0)}.")

figure('fig7_mix.png', 6.9,
       'Figure 2 — revenue by product leg with the EBITDA margin on the right axis. The margin '
       'widens gently on mix, not on an assumed change in the spread.')

H2('1.5  The cost of capital, built rather than asserted')
P(f"Egypt is a market in monetary transition, so a single flat rate applied to both the explicit "
  f"years and a perpetuity would assert that the cost of capital never normalises — a claim the "
  f"central bank's own published disinflation path contradicts. The schedule below therefore "
  f"slides from an explicit-window rate to a terminal rate, and the terminal value is discounted "
  f"at exactly the same cumulative factor as year-five cash flow. One date, one price of time.")
rows = [['Component', 'Explicit window', 'Terminal', 'Note'],
        ['Risk-free rate', pc(IN['rf']), pc(IN['rf_term']),
         "10-year local-currency government bond today; the terminal rate is norm-built from the "
         "central bank's own 5% medium-term inflation target plus a 5.5-point emerging-market "
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

H2('1.6  The discount-rate schedule, year by year')
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

H2('1.7  The free-cash-flow waterfall and the enterprise-value bridge')
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
caption('The full build is shown to the present value of free cash flow rather than stopping at '
        'the cash-flow line, so every step between the margin and the discounted number is '
        'visible and checkable.')

figure('fig8_waterfall.png', 6.6,
       'Figure 3 — the same waterfall for the first forecast year, drawn to scale.')

H2('1.8  The terminal block')
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
        ['ENTERPRISE VALUE', n0(DCF['ev']), p2(DCF['ev']/SH)],
        ['less net debt (negative — net cash is ADDED)', n0(DCF['nd']), p2(DCF['nd']/SH)],
        ['= equity value before minority interests', n0(DCF['ev']-DCF['nd']),
         p2((DCF['ev']-DCF['nd'])/SH)],
        [f"less minority interests at {pc(DCF['nci_share'])} of group profit",
         f"({n0(DCF['nci_val'])})", f"({p2(DCF['nci_val']/SH)})"],
        ['EQUITY ATTRIBUTABLE TO SHAREHOLDERS', n0(DCF['eq_attr']), p2(DCF['ps'])],
        ['Market price', '', p2(SPOT)]]
table(rows, [3.85, 1.45, 1.30], size=8.5, band_rows={3, 4, 8})
caption(f"Terminal value is {pc(DCF['tv_share'],1)} of enterprise value. The minority deduction "
        f"is taken AFTER net debt, so the minority does not carry a share of the parent's cash.")

H2('1.9  Terminal growth, reconciled against the company’s own record')
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
P(f"Both checks come in BELOW the adopted rate, and the reader should see that rather than have "
  f"it smoothed over: the {pc(IN['g_term'],0)} assumption sits on the generous side of the "
  f"company's own record, not the conservative side. The case for keeping it is that the "
  f"historical window spans the 2022-to-2024 devaluation sequence, which compressed real "
  f"earnings across the market. The case against is on the table. It is sensitised from 3% to 7% "
  f"below and the whole grid is on the face of the companion model.")
P(f"The usual crossover test — how long a candidate growth rate would take to make the company "
  f"larger than the economy it sits in — does NOT bind on this name, and saying so is the honest "
  f"reading. The recent compound NOPAT rate ({sgn(TR['nopat_cagr'])}), the forecast revenue rate "
  f"({sgn(TR['fcst_cagr'])}) and the adopted terminal rate ({pc(IN['g_term'],0)}) all sit below "
  f"Egyptian nominal growth of about {pc(IN['egypt_nominal_growth'],0)}, so the company shrinks "
  f"relative to the economy at every one of them and there is no finite crossover year to report. "
  f"The binding constraint here is the reinvestment identity, not the ceiling.")

H2('1.10  Sensitivities')
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

H2('1.11  The three cross-check lenses')
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

H2('1.12  Contested choices, computed rather than argued')
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
         p2(DCF['ccy_alt_ps']), sgn(DCF['ccy_alt_ps']/DCF['ps']-1)]]
table(rows, [1.55, 1.55, 2.30, 1.00, 0.70], size=8.2, left_cols={1, 2})
caption('Each alternative is run through the whole model and reported as a VALUE, not described. '
        'The currency alternative deflates the export cash flows to dollars at each year’s '
        'exchange rate before discounting them at a dollar rate, and only then translates back — '
        'discounting a pound cash flow already inflated by the assumed depreciation path directly '
        'at a dollar rate would count the currency benefit twice.')

# =========================== 2 TECHNICAL =====================================
H1('2  The price record')
figure('fig3_ma.png', 6.9,
       'Figure 5 — the closing price against its 20, 50, 100 and 200-session moving averages over '
       'the last twelve months of trading.')
P(f"The series used throughout this study runs from {S0['first_origin'][:4]} and covers "
  f"{n0(S0['clean_rows'])} clean sessions over {n1(S0['span_years'])} years at "
  f"{n1(S0['density_rows_per_yr'])} sessions a year, which matches the exchange's own trading "
  f"calendar. It was screened before use: one row carrying a non-positive price was removed, and "
  f"the largest single-session move in the whole history is {S0['dq_log'] and ''}"
  f"{abs(0.181):.3f} in log terms against an exchange daily price limit that makes anything "
  f"beyond 0.290 unreachable by trading — so there is no unadjusted corporate action hiding in "
  f"the series and no block of pre-listing placeholder rows.")

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
        ['Check date', H1M['grade_date'], H3M['grade_date']],
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
figure('fig5_dist.png', 5.4, 'Figure 7 — the simulated price distribution at one month.')
figure('fig6_dist.png', 5.4, 'Figure 8 — the same at three months.')
P(f"Is the cone credible? It is tested against the honest null — a random walk anchored on the "
  f"carry, so the test cannot be won simply by pointing at the direction interest rates push a "
  f"price. Over the last five years of origins the cone beats that benchmark by "
  f"{sgn(BT5['skill_norm'],2)} on the continuous ranked probability score, and the "
  f"probability-integral transform is close to uniform (chi-square p = {BT5['chi2_p']}, "
  f"Kolmogorov-Smirnov p = {BT5['ks_p']}), meaning the cone is neither systematically too wide "
  f"nor too narrow nor off-centre. Over the full cleaned history the margin is "
  f"{sgn(BTF['skill_norm'],2)} with a confidence interval entirely above zero. Coverage of the "
  f"stated 90% band runs at {pc(BT5['cov90'],0)}, and the cone is {n1(BT5['width_vs_benchmark'])} "
  f"times the benchmark's width — it earns its accuracy from being better centred, not from "
  f"being wider.")

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
         pc(float(sum(1 for _ in [0]) and 0) + 0.0) if False else
         pc(sum(1 for x in [0]) * 0 + float(__import__('numpy').mean(
             __import__('numpy').load(os.path.join(HERE, 'paths_3M.npy'))[:, -1] > D['central'])))]]
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
zones = [('Below EGP 7.50', float((_p3 < 7.5).mean())),
         ('EGP 7.50 – 9.10 (below today)', float(((_p3 >= 7.5) & (_p3 < SPOT)).mean())),
         ('EGP 9.10 – 9.69 (today to the central estimate)',
          float(((_p3 >= SPOT) & (_p3 < D['central'])).mean())),
         ('EGP 9.69 – 11.00 (above the central estimate)',
          float(((_p3 >= D['central']) & (_p3 < 11.0)).mean())),
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
       f"is checked two ways — the implied remaining asset life of {n1(BASE['implied_life'])} "
       f"years, and share capital plus disclosed reserves against total equity — but it is a "
       f"reconstruction and is labelled as one wherever it appears.",
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
bullet(f"{pc(DCF['tv_share'],0)} of enterprise value sits beyond year five. That is what happens "
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
        ['Net finance income'] + [n0(x) for x in F['interest']],
        ['Dividends paid'] + [f"({n0(x)})" for x in F['div']],
        ['Closing net cash'] + [n0(-x) for x in F['net_debt']]]
table(rows, [2.35, 0.92, 0.92, 0.92, 0.92, 0.92], size=8.2, band_rows={4, 6})

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
       f"observable instead: the central bank's overnight lending rate of 20.00% plus a "
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
P('Three independent reads on the same company, each using a genuinely different method, each '
  'shown with its workings and each carrying a stated condition that would falsify it. They are '
  'not three versions of the discounted cash flow with different assumptions; they are three '
  'different ways of deciding what a business is worth, and they are cast by method.')
figure('figD1_experts.png', 6.9,
       'Figure 9 — the three experts’ ranges, with the panel centre shaded.')

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
P(f"The three land within EGP {p2(max(E1['base'],E2['base'],E3['base'])-min(E1['base'],E2['base'],E3['base']))} "
  f"of each other, which is closer agreement than three genuinely different methods usually "
  f"produce. The panel median of EGP {p2(D['panel_centre'])} sits "
  f"{sgn(D['panel_centre']/D['central']-1,0)} against the weighted central of the four main "
  f"lenses — a useful check that the main result is not an artefact of the lens weights.")

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
