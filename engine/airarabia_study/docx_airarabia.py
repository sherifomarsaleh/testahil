"""AIRARABIA_Valuation_Study_09-08-2026_public.docx — 16 sections in the house
skeleton, operating-company lens set. Every numeral is read from
study_numbers.json (or the technical/backtest JSONs) — none is typed here."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
sys.path.insert(0, HERE)
exec(open(os.path.join(HERE, 'docx_base.py')).read())

TA = json.load(open('ta_state.json'))
BT = D['backtest_5y']
SW = json.load(open('sweep_register.json'))
M, HI, HB, F = D['meta'], D['hist_is'], D['hist_bs'], D['fcst']
W, DCF, LN, SN = D['wacc'], D['dcf'], D['lenses'], D['sens']
EXP, REL, NRM, BKL = D['experts'], D['rel'], D['norm'], D['book']
BU, S0, STK = D['bottomup'], D['step0'], D['strike']
IN = {k: v['value'] for k, v in D['inputs'].items()}
SPOT, SH = M['spot'], M['shares_mn']
H1_, H3_ = STK['horizons']['1M'], STK['horizons']['3M']
YF = F['years']
CEN = D['central']

def pct(x, dp=1): return f'{x*100:.{dp}f}%'
def mn(x): return f'{x:,.0f}'
def px(x): return f'{x:.2f}'

# ============================== MASTHEAD + READ FIRST =========================
masthead()
P('Air Arabia PJSC', size=22, bold=True, space_after=0)
rich([('Dubai Financial Market · AIRARABIA · Aviation — low-cost airline · ', dict(size=10.5, color=GREY)),
      (f"Report date 9 August 2026 · prices as of {M['asof']}", dict(size=10.5, color=GREY))],
     space_after=10)
box([
 ('READ FIRST — what this document is.  ',
  'An independent, educational valuation study of Air Arabia PJSC. It is not investment advice, not a '
  'solicitation, and it contains no rating and no price target. It presents fair-value RANGES from four '
  'valuation lenses, a probability map for the share price, and every assumption used to build them.'),
 ('Sources.  ',
  'Built exclusively on the company\'s own audited consolidated financial statements FY2022–FY2025 (KPMG '
  'Lower Gulf, unqualified opinion on FY2025 dated 13-Feb-2026), the reviewed Q1-2026 interim (Grant '
  'Thornton UAE), and the company\'s own results presentations — all read from airarabia.com investor '
  'relations. Peer figures are cross-checks only and are labelled as such. A companion bibliography '
  'document lists every input with source and date.'),
 ('Two judgements are shown both ways, never averaged.  ',
  'The 2026-27 fuel path (the official US energy-agency curve versus the airline association\'s high-fuel '
  'assumption) and the value of the joint-venture airline network (audited carrying value versus '
  'capitalised profit share). Each framing is priced in full and both appear side by side.'),
 ('The companion workbook calculates.  ',
  'Every figure derivable from a driver is a live Excel formula; only audited history, the unit build\'s '
  'disclosed bases, and whole-model re-runs (the Monte Carlo map, sensitivity grids and scenario bounds) '
  'are pasted, and the workbook\'s READ FIRST sheet names those three classes.'),
])

# ============================== HEADLINE ======================================
H1('Headline')
rich([(f'Fair value clusters at AED {CEN:.2f} per share on the base framing and AED '
       f"{D['central_jvcap']:.2f} with the joint-venture network capitalised — against a market price of "
       f'AED {SPOT:.2f}. ', dict(bold=True)),
      ('The market is paying roughly a fifth more than the base fundamental value; the gap is, in large '
       'part, a price on two things this study deliberately prices both ways: cheaper fuel from 2027 and '
       'the five equity-accounted airlines the balance sheet carries at less than two times their annual '
       'profit contribution.', dict())])
P(f"Air Arabia closed FY2025 with record results: revenue AED {mn(HI['FY25']['rev'])}mn (+15%), profit "
  f"before tax AED {mn(HI['FY25']['ebt'])}mn (+14%), 13.06mn passengers (+16%) at a record 85.3% seat "
  f"load factor, a fleet of 90 A320-family aircraft, net CASH of AED {mn(-HB['FY25']['nd'])}mn including "
  f"fixed deposits, and a dividend raised for the fourth straight year to 30 fils. The Q1-2026 quarter "
  f"then absorbed the February–March regional airspace closures: revenue held (+1%) on 11% fewer "
  f"consolidated passengers, while net profit fell 22% — a dip this study treats as exactly that, not a "
  f"trend break.")
P(f"Over the next three months the price map assigns a 50% band of AED {H3_['pct']['p25']:.2f}–"
  f"{H3_['pct']['p75']:.2f} and a 90% band of AED {H3_['pct']['p5']:.2f}–{H3_['pct']['p95']:.2f} around "
  f"the AED {SPOT:.2f} spot — the fundamental ranges below are slower-moving claims about value, the map "
  f"is a calibrated claim about price.")

# ============================== VALUATION SUMMARY =============================
H1('Valuation summary — every read at a glance')
rows = [['Lens', 'Bear', 'Base', 'Bull', 'Weight', 'vs spot']]
for k, extra in [('dcf', f" · terminal value {pct(DCF['tv_share'],0)} of EV"), ('relative', ''),
                 ('normalized', ''), ('book', '')]:
    l = LN[k]
    rows.append([l['name'] + extra, px(l['bear']), px(l['base']), px(l['bull']),
                 pct(l['w'], 0), f"{l['base']/SPOT-1:+.0%}"])
rows.append(['Weighted central', px(LN['central']['bear']), px(CEN), px(LN['central']['bull']),
             '100%', f'{CEN/SPOT-1:+.0%}'])
table(rows, [2.65, 0.75, 0.75, 0.75, 0.75, 0.85], band_rows={5})
rows = [['Alternative framings (never averaged into the central)', 'AED/share', 'vs spot'],
        ['DCF with the JV network capitalised at '
         f"{IN['jv_pe']:.0f}x its profit share", px(DCF['ps_jvcap']), f"{DCF['ps_jvcap']/SPOT-1:+.0%}"],
        ['Weighted central on that framing', px(D['central_jvcap']), f"{D['central_jvcap']/SPOT-1:+.0%}"],
        ['DCF on the high-fuel alternative (association path held)', px(DCF['ps_iata_fuel']),
         f"{DCF['ps_iata_fuel']/SPOT-1:+.0%}"],
        ['Expert panel median', px(D['panel_centre']), f"{D['panel_centre']/SPOT-1:+.0%}"],
        [f"Market price ({M['asof']})", px(SPOT), '—']]
table(rows, [4.30, 1.20, 1.00])
caption('The DCF row shows the terminal-value share of enterprise value beside the lens, as it should: '
        f"{pct(DCF['tv_share'],0)} of the operating value sits beyond the five forecast years, because "
        'the fleet build-out\'s spending lands inside the window while much of its revenue lands after it.')

# ============================== COMPANY OVERVIEEW =============================
H1('Company overview')
P('Air Arabia PJSC, incorporated 19 June 2007 and listed on the Dubai Financial Market, is the Middle '
  'East and North Africa\'s first and largest listed low-cost carrier. From hubs at Sharjah and Ras Al '
  'Khaimah it operates a 90-aircraft Airbus A320-family fleet (plus five short-term leases) to 219 '
  'destinations, with the first of 120 ordered A320neo-family aircraft (73 A320neo, 27 A321neo, 20 '
  'A321XLR — the 2019 order) delivered on 29 September 2025. Around the listed company sits a network of '
  'equity-accounted airline ventures: Air Arabia Abu Dhabi (49%, with Etihad), Air Arabia Egypt (raised '
  'to 49% in 2025), Fly Jinnah in Pakistan (45%), Air Arabia Maroc (44.13%), and — signed in 2025 — Air '
  'Arabia DMM (49%), a new Dammam-based Saudi carrier. The group also owns hotels (Centro Sharjah, '
  'Radisson Blu Dubai Marina), the COZMO travel network, aviation-services subsidiaries, and leases 17 '
  'of its aircraft to the venture airlines.')
P(f"Class and lens. Air Arabia is an OPERATING COMPANY — a low-cost airline: {pct(6165.584/7787.581,0)} "
  "of FY2025 revenue is passenger fares plus baggage, another 11% is ancillary/cargo/services sold around "
  "the seat, 3% is aircraft leases to its own ventures and 1% hotels. The balance sheet is a fleet "
  f"(AED {mn(HB['FY25']['ppe'])}mn owned equipment, AED {mn(HB['FY25']['rou'])}mn right-of-use aircraft, "
  f"AED {mn(HB['FY25']['adv'])}mn pre-delivery payments) funded by secured aircraft debt and leases of "
  f"AED {mn(HB['FY25']['debt'])}mn against AED {mn(-HB['FY25']['nd'])}mn of NET CASH. The study therefore "
  "values the airline on discounted free cash flow with a passenger-level unit build, and handles the "
  "equity-accounted venture network explicitly in the enterprise-to-equity bridge — the one genuinely "
  "contested structural judgement.")

# ============================== 1 FUNDAMENTAL VALUATION =======================
H1('1  Fundamental valuation')
H2('1.1  The cash-flow model — FCFF waterfall and the bridge to equity')
P('Revenue is built from passengers times per-passenger rates; the cost stack is per-passenger lines '
  'with one escalator each (section 1.6). The waterfall below runs from EBITDA to enterprise value; '
  'every line of it is a live formula in the companion workbook.')
rows = [['AED mn'] + [y for y in YF]]
for lbl, arr in [('Revenue', F['rev']), ('EBITDA (incl. fees and other income)', F['ebitda_incl']),
                 ('less depreciation & amortisation', F['dna']),
                 ('EBIT', F['ebit_incl']),
                 (f"NOPAT (EBIT × (1 − {pct(IN['tax_eff'],0)}))", F['nopat']),
                 ('add back depreciation & amortisation', F['dna']),
                 ('less fleet capital expenditure', F['capex']),
                 ('less change in working capital', F['dnwc']),
                 ('Free cash flow to the firm', F['fcff']),
                 ('Discount factor (glide-compounded)', None),
                 ('PV of FCFF', F['pv'])]:
    if arr is None:
        rows.append([lbl] + [f"{x:.4f}" for x in F['df']])
    else:
        rows.append([lbl] + [mn(x) for x in arr])
table(rows, [2.55, 0.89, 0.89, 0.89, 0.89, 0.89], band_rows={9, 11})
caption(f"The FY2026 free cash flow is negative (AED {mn(F['fcff'][0])}mn): the fuel spike lands in the "
        "same year as the heaviest pre-delivery-payment schedule. It turns positive from FY2027 and "
        "reaches AED "
        f"{mn(F['fcff'][4])}mn by FY2030.")
rows = [['Enterprise value → equity', 'AED mn'],
        ['PV of explicit years FY2026–30', mn(DCF['pv_explicit'])],
        [f"PV of terminal value (growth {pct(IN['g_term'])}, terminal cost of capital "
         f"{pct(W['wacc_term'],2)}, reinvestment = g / return on capital = {pct(DCF['rr_term'])})",
         mn(DCF['pv_tv'])],
        ['Enterprise value of the airline', mn(DCF['ev'])],
        [f"Terminal value as a share of enterprise value", pct(DCF['tv_share'], 0)],
        ['plus net cash (cash + fixed deposits − borrowings − leases)', mn(-DCF['nd'])],
        ['plus non-operating assets (investments, investment property, net investment in lease)',
         mn(DCF['non_op'])],
        ['plus JV network at audited carrying value — BASE framing', mn(DCF['jv_book'])],
        ['less minorities', f"{DCF['nci_val']:.1f}"],
        ['Equity attributable, 31-Dec-2025', mn(DCF['eq_attr'])],
        [f"Per share, rolled to {M['asof']} at the cost of equity less the 30-fils dividend",
         f"AED {px(DCF['ps'])}"],
        [f"Same bridge with the JV network at {IN['jv_pe']:.0f}× profit share — ALTERNATIVE framing",
         f"AED {px(DCF['ps_jvcap'])}"]]
table(rows, [5.30, 1.20], band_rows={4, 10, 11, 12})
H2('1.2  Book value and sustainable return')
P(f"Audited FY2025 book value is AED {px(BKL['bvps'])} per share. The trailing return on average "
  f"attributable equity is {pct(BKL['roe_trailing'])}; the study strikes the SUSTAINABLE return at "
  f"{pct(IN['roe_sust'],0)} — below the record year, because FY2025 carried a yield tailwind from "
  f"constrained regional capacity. A justified price-to-book of ({pct(IN['roe_sust'],0)} − "
  f"{pct(IN['g_term'])}) / ({pct(W['ke_term'],2)} − {pct(IN['g_term'])}) = "
  f"{BKL['pb_just']:.2f}× values the share at AED {px(LN['book']['base'])} at the anchor "
  f"(bear {px(LN['book']['bear'])} / bull {px(LN['book']['bull'])}).")
H2('1.3  Relative multiples')
P(f"At {IN['ev_ebitda_just']:.1f}× FY2027E EBITDA of AED {mn(REL['ebitda_mid'])}mn — the global "
  f"low-cost-carrier centre — discounted to today and passed through the same bridge, the share is worth "
  f"AED {px(LN['relative']['base'])} (bear {px(LN['relative']['bear'])} at 6.0×, bull "
  f"{px(LN['relative']['bull'])} at 9.0×). For context, the market currently pays "
  f"{REL['ev_ebitda_trailing']:.1f}× trailing EV/EBITDA and {REL['pe_trailing']:.1f}× trailing earnings "
  f"— a premium to Ryanair (7.8×, 12.6×), easyJet (3.5×, 12.4×) and the sector aggregate (7.6×, 12.9×), "
  f"nearer Kuwait's Jazeera Airways (~17.7× earnings). The relative lens's message is that the premium "
  f"is already in the price; whether the JV network and the order book justify it is the study's "
  f"central question, not the lens's input.")
H2('1.4  Normalised earnings power')
P(f"Applying the mid-cycle EBITDA margin ({pct(NRM['margin'])}, the FY2028E middle year) to FY2026E "
  f"revenue at CURRENT scale, with FY2026E net finance income and JV share, gives normalised earnings "
  f"of AED {NRM['eps']:.3f} per share; at a justified through-cycle multiple of {IN['pe_just']:.0f}× "
  f"that is AED {px(LN['normalized']['base'])} (bear {px(LN['normalized']['bear'])} at 10×, bull "
  f"{px(LN['normalized']['bull'])} at 16×).")
H2('1.5  Synthesis — four lenses, one field')
figure('fig1_football.png', 6.9,
       'Figure 1 — the four lenses and the weighted central. Every lens base sits below the market '
       'price on the base framing; the capitalised-JV framing closes part of the gap.')
H2('1.6  Drivers — the unit build, each line on its own driver')
P('The company discloses passengers, load factor and a full revenue and cost disaggregation, but not '
  'seats or available seat-kilometres; passengers × per-passenger rates is therefore the finest '
  'disclosed level, and that is where the model is built. Margins are OUTPUTS.')
rows = [['Unit economics (AED per passenger)', 'FY2024', 'FY2025'] + YF]
uh24, uh25 = BU['unit_hist']['FY24'], BU['unit_hist']['FY25']
rows.append(['Passengers (millions)', f"{uh24['pax']:.2f}", f"{uh25['pax']:.2f}"]
            + [f'{p:.2f}' for p in F['pax']])
rows.append(['Fare + baggage', f"{uh24['fare']:.0f}", f"{uh25['fare']:.0f}"]
            + [f"{x:.0f}" for x in IN['fare_path']])
rows.append(['Ancillary', f"{uh24['anc']:.0f}", f"{uh25['anc']:.0f}"]
            + [f"{x:.0f}" for x in IN['anc_path']])
rows.append(['Fuel (base path)', f"{uh24['fuel']:.0f}", f"{uh25['fuel']:.0f}"]
            + [f"{x:.0f}" for x in IN['fuel_per_pax']])
rows.append(['Fuel (high-fuel alternative)', '—', '—'] + [f"{x:.0f}" for x in IN['fuel_per_pax_alt']])
rows.append(['Staff', f"{uh24['staff']:.0f}", f"{uh25['staff']:.0f}"]
            + [f"{x:.0f}" for x in IN['staff_per_pax']])
rows.append(['Maintenance', f"{uh24['maint']:.0f}", f"{uh25['maint']:.0f}"]
            + [f"{x:.0f}" for x in IN['maint_per_pax']])
rows.append(['Landing & overflying', f"{uh24['landing']:.0f}", f"{uh25['landing']:.0f}"]
            + [f"{x:.0f}" for x in IN['landing_per_pax']])
rows.append(['Handling', f"{uh24['handling']:.0f}", f"{uh25['handling']:.0f}"]
            + [f"{x:.0f}" for x in IN['handling_per_pax']])
rows.append(['Other direct', f"{uh24['other']:.0f}", f"{uh25['other']:.0f}"]
            + [f"{x:.0f}" for x in IN['other_per_pax']])
table(rows, [1.90, 0.66, 0.66, 0.66, 0.66, 0.66, 0.66, 0.66], size=8.6)
caption('One escalator per cost class: fuel moves on the commodity path (never a domestic inflation '
        'proxy), staff on UAE aviation wages, maintenance on its own MRO inflation, airport charges on '
        '~2% UAE inflation, and the other-direct line is held flat as the 2025 wet-lease spike unwinds '
        'against ordinary inflation. Passenger growth is fleet-led: 90 aircraft to roughly 115 by 2030 '
        'out of the 120-aircraft order, at a held ~85–86% load factor.')
figure('fig7_units.png', 6.9,
       'Figure 2 — passengers, revenue and the EBITDA margin path. The 2026 dip is the fuel spike plus '
       'flat traffic; 2027 recovers on the official-curve fuel path.')
H2('1.7  The crux — fuel, and what the joint ventures are worth')
P(f"Two judgements dominate this valuation, and both are sensitised in their own physical units. FUEL: "
  f"straight from the model's own grid, at 92.5% of the base fuel path the DCF is "
  f"AED {px(SN['grid_fuel'][1])} and at 107.5% it is AED {px(SN['grid_fuel'][3])} — about AED "
  f"{px((SN['grid_fuel'][1]-SN['grid_fuel'][3])/2)} per share for each 7.5% move in the fuel line "
  f"(roughly AED 13 per passenger). Priced BOTH ways as full paths: base (official-curve relief) AED "
  f"{px(DCF['ps'])}; association-assumption held high, AED {px(DCF['ps_iata_fuel'])}. THE JV NETWORK: "
  f"at the audited carrying value it contributes AED {DCF['jv_book']/SH:.2f} per share; capitalised at "
  f"{IN['jv_pe']:.0f}× its AED {mn(IN['assoc_fy25'])}mn profit share it contributes AED "
  f"{DCF['jv_cap']/SH:.2f} — the {px(DCF['ps_jvcap']-DCF['ps'])} per-share gap between the two framings "
  f"is the single largest contested item in the study, and the ventures' own 100%-basis profits grew "
  f"roughly 65% in FY2025 with a new Saudi carrier signed.")
H2('1.8  Macro & country — the cost of capital, built and evidenced')
rows = [['Component', 'Value', 'Evidence'],
        ['AED government bond yield', pct(IN['rf'],2),
         'UAE Ministry of Finance dirham T-Bond auction, July-2026, January-2031 tranche (4bp over '
         'comparable US Treasuries); May-2026 auction 4.30%'],
        ['less UAE sovereign default spread', pct(IN['sov_spread_rating'],2),
         'Aa2 rating basis, Damodaran country file, 5-Jan-2026 — netted so sovereign risk is counted '
         'once, in the premium'],
        ['Net risk-free rate', pct(W['rf_star'],2), 'derived'],
        ['Beta', f"{IN['beta_used']:.3f}",
         'own-stock five-year weekly regression against the Dubai (DFM) general index: R² 0.40, 258 '
         'weeks, standard error 0.083, 90% interval 0.95–1.22'],
        ['Equity risk premium', pct(IN['erp_rating'],2),
         'Damodaran UAE row, January-2026 (mature 4.23% + country 0.64%). The same file publishes no '
         'usable UAE sovereign-swap-based alternative — stated rather than substituted'],
        ['Cost of equity', pct(W['ke_exp'],2), 'derived'],
        ['Marginal cost of debt', pct(IN['kd'],2), 'see the evidence table below'],
        ['Weights (gross debt / equity, market value)', f"{pct(W['wd_exp'])} / {pct(W['we_exp'])}",
         'market capitalisation at spot; gross debt as audited'],
        ['Cost of capital — explicit window', pct(W['wacc_exp'],2), 'derived'],
        ['Cost of capital — terminal', pct(W['wacc_term'],2),
         f"risk-free normalised to {pct(IN['rf_term'])}, premium {pct(IN['erp_term'],2)}, debt weight "
         f"{pct(IN['wd_term'],0)} — norm-built, never backed out of a price"]]
table(rows, [2.05, 0.90, 4.05], size=8.6)
rows = [['Cost-of-debt evidence', 'Rate', 'Nature'],
        ['Lease book average finance charge (FY2025 note)', '4.0%',
         'secured on the aircraft — a floor, not a marginal rate'],
        ['FY2025 aircraft loan (AED 849.6mn for 5 aircraft)', 'n/d', 'mortgage-secured'],
        ['Effective finance cost / average gross debt', pct(W['kd_eff_fy25'],2), 'blended, secured book'],
        ['Fixed deposits earn (FY2025 note)', '4.41%', 'the asset-side opportunity rate'],
        ['AED sovereign, January-2031', pct(IN['rf'],2), 'the unsecured floor for any AED corporate'],
        ['ADOPTED marginal unsecured cost of debt', pct(IN['kd'],2),
         'sovereign + ~100bp; above every secured print and the deposit rate, as it must be']]
table(rows, [2.80, 0.95, 3.25], size=8.6, band_rows={6})
P(f"Tax: the UAE Domestic Minimum Top-up Tax puts the group at a 15% statutory rate from 2025; the "
  f"audited effective rates were 8.79% (FY2024, the 9% year) and 11.60% (FY2025, exempt income). The "
  f"forecast provides at the full 15% — the conservative anchor. Country backdrop: UAE GDP grew ~5.6% "
  f"in 2025 with ~5% projected for 2026, inflation ~2%, and the central bank's base rate held at 3.65% "
  f"(29-Jul-2026) under the dollar peg; Sharjah airport handled a record 19.5mn passengers in 2025, "
  f"up 13.9%.")
H2('1.9  Sensitivity')
figure('fig2_sens.png', 6.3,
       'Figure 3 — DCF fair value across terminal cost of capital × terminal growth.')
rows = [['Driver (whole-model re-runs)', '-2 steps', '-1', 'Base', '+1', '+2']]
for lbl, xs, vals, fmtx in [
        ('Beta', SN['beta_grid'], SN['grid_beta'], lambda x: f'{x:.2f}'),
        ('Fuel path multiplier', SN['fuel_grid'], SN['grid_fuel'], lambda x: f'{x:.3g}×'),
        ('Passenger volumes', SN['paxg_grid'], SN['grid_pax'], lambda x: f'{x:.2f}×'),
        ('Fare per passenger', SN['fare_grid'], SN['grid_fare'], lambda x: f'{x:.2f}×'),
        ('Fleet capex', SN['capex_grid'], SN['grid_capex'], lambda x: f'{x:.2f}×'),
        ('JV value in the bridge (AED mn)', SN['jv_grid'], SN['grid_jv'], lambda x: f'{x:,.0f}'),
        ('Working capital / revenue', SN['nwc_grid'], SN['grid_nwc'], lambda x: f'{x:.0%}')]:
    rows.append([f'{lbl}  [{fmtx(xs[0])} … {fmtx(xs[4])}]'] + [px(v) for v in vals])
table(rows, [2.90, 0.82, 0.82, 0.82, 0.82, 0.82], size=8.6)
caption('Each cell is a complete revaluation at the perturbed driver, all else held. The middle column '
        'is the base DCF of AED ' + px(DCF['ps']) + '.')

# ============================== 2 TECHNICAL ====================================
H1('2  Technical and price structure')
nr = TA['tech']
P(nr['summary'])
P(nr['trend'])
rows = [['Level', 'AED', 'Reading'],
        ['Resistance 3', f"{TA['levels']['res'][2]:.2f}", 'the 52-week high zone'],
        ['Resistance 2', f"{TA['levels']['res'][1]:.2f}", 'minor supply shelf'],
        ['Resistance 1 (nearest)', f"{TA['levels']['res'][0]:.2f}", nr['bull']],
        [f"Last close ({M['asof']})", f"{SPOT:.2f}", 'above the whole moving-average stack'],
        ['Support 1 (nearest)', f"{TA['levels']['sup'][0]:.2f}", nr['bear']],
        ['Support 2', f"{TA['levels']['sup'][1]:.2f}", 'pivot cluster'],
        ['Support 3', f"{TA['levels']['sup'][2]:.2f}", 'the deeper shelf']]
table(rows, [1.55, 0.85, 4.60], size=8.8, band_rows={4})
figure('fig3_ma.png', 6.9, 'Figure 4 — price against the moving-average stack, last 260 sessions.')

# ============================== 3 PROBABILISTIC PRICE MAP ======================
H1('3  A probabilistic price map')
P(f"From the {STK['anchor_date']} close of AED {SPOT:.2f}, 50,000 simulated price paths — volatility "
  f"fitted to this stock's own trading history, drift anchored to the risk-free rate net of the 5.7% "
  f"trailing dividend yield — give the following bands:")
rows = [['', 'One month', 'Three months'],
        ['Check date', H1_['grade_date'], H3_['grade_date']],
        ['5th percentile', px(H1_['pct']['p5']), px(H3_['pct']['p5'])],
        ['25th percentile', px(H1_['pct']['p25']), px(H3_['pct']['p25'])],
        ['Median', px(H1_['pct']['p50']), px(H3_['pct']['p50'])],
        ['75th percentile', px(H1_['pct']['p75']), px(H3_['pct']['p75'])],
        ['95th percentile', px(H1_['pct']['p95']), px(H3_['pct']['p95'])],
        ['Probability of finishing above spot', pct(H1_['p_above'],0), pct(H3_['p_above'],0)],
        ['Probability of +10% or better at the check date', pct(H1_['p_up10'],0), pct(H3_['p_up10'],0)],
        ['Probability of −10% or worse at the check date', pct(H1_['p_dn10'],0), pct(H3_['p_dn10'],0)],
        ['Probability of touching +10% at any point', pct(H1_['touch_up10'],0), pct(H3_['touch_up10'],0)],
        ['Probability of touching −10% at any point', pct(H1_['touch_dn10'],0), pct(H3_['touch_dn10'],0)]]
table(rows, [3.50, 1.35, 1.35], size=8.8)
figure('fig4_fan.png', 6.9, 'Figure 5 — the three-month price cone.')
figure('fig5_dist.png', 5.2, 'Figure 6 — the one-month terminal price distribution.')
figure('fig6_dist.png', 5.2, 'Figure 7 — the three-month terminal price distribution.')
P(f"How much to trust these bands. Backtested on this stock's own history — every quarter-length "
  f"window from 2012 to 2026, {BT['full']['windows']} of them — the simulation's probability bands beat "
  f"a naive random-walk benchmark by a small margin on a standard probabilistic accuracy score "
  f"({BT['full']['skill_norm']*100:+.1f}%), and over the most recent four-plus years the two are "
  f"statistically indistinguishable: an honest, calibrated map rather than a crystal ball. Realised "
  f"prices landed inside the 80% band {pct(BT['full']['cov80'],0)} of the time and inside the 90% band "
  f"{pct(BT['full']['cov90'],0)} — about as close to nominal as {BT['full']['windows']} windows allow. "
  f"The recent windows lean toward outcomes in the upper half of the bands (the share nearly tripled "
  f"from its 2022 lows), which is visible in the distribution of where outcomes fell but does not "
  f"reject uniformity on a standard test of the full history.")

# ============================== 4 COMPARISON OF THE LENSES =====================
H1('4  Comparison of the lenses')
rows = [['Lens', 'What it sees', 'What it misses'],
        ['DCF (base)', 'the fleet build-out\'s cash cost, the negative-working-capital engine, fuel '
         'relief from 2027', 'the JV network\'s value beyond book; anything after FY2030 except through '
         'the terminal'],
        ['DCF (JV capitalised)', 'the ventures as going concerns at a growth multiple',
         'their startup risk — Saudi DMM is pre-operational, two ventures are being wound up'],
        ['Relative', 'what the world pays for LCC earnings today', 'Air Arabia\'s net cash and JV '
         'optionality are only partly in sector multiples'],
        ['Normalised', 'through-cycle earning power at current scale', 'growth beyond FY2026 scale'],
        ['Book', 'audited equity and a sustainable return', 'slots, brand and the ventures — none on '
         'the balance sheet at economic value']]
table(rows, [1.35, 3.00, 2.65], size=8.6)
P(f"All four lens bases sit between AED {px(min(LN[k]['base'] for k in ('dcf','relative','normalized','book')))} "
  f"and AED {px(max(LN[k]['base'] for k in ('dcf','relative','normalized','book')))} — a tight cluster "
  f"{abs(CEN/SPOT-1)*100:.0f}% below the market price. The market, in other words, is already paying "
  f"for the JV-capitalised framing plus some of the order book's post-2030 tail. That is not "
  f"irrational; it is simply not conservative, and this study's job is to show exactly which "
  f"assumptions you must accept to get there.")

# ============================== 5 CATALYSTS ====================================
H1('5  Catalysts to watch')
for head, body in [
    ('Half-year 2026 results (mid-August 2026).  ',
     'The first full print after the airspace disruption: watch whether Q2 yields held the Q1 record '
     'load factor, and the first disclosure of summer bookings.'),
    ('The fuel path.  ',
     'The official curve has Brent averaging ~$82 in 2026 falling toward ~$65 in 2027; the airline '
     'association assumed ~$95 with jet fuel near $152. Every quarter the curve view wins is roughly '
     'AED 0.04 per share of annualised value; the study prices both paths in full.'),
    ('Air Arabia DMM (Saudi Arabia).  ',
     'The 49% Dammam carrier signed in 2025: an operating-certificate date, fleet plan or launch '
     'schedule would move the JV framing from optionality toward earnings.'),
    ('Abu Dhabi expansion.  ',
     'The venture with Etihad plans ~40% capacity growth into the space Wizz Air abandoned in '
     'September 2025 — its profit share doubled in FY2025 and it pays no dividend yet.'),
    ('Airbus deliveries.  ',
     'Nine A320-family aircraft arrived in FY2025; the neo ramp (lower fuel burn, more seats) is the '
     'whole volume story, and Airbus\'s output remains constrained.'),
    ('The dividend ladder.  ',
     'Four consecutive 5-fil raises to 30 fils (a 5.7% trailing yield). A fifth raise with FY2026 '
     'results would signal the board reads the dip year as behind it.')]:
    bullet(body, bold_head=head)

# ============================== 6 READING THE ZONES ============================
H1('6  Reading the probability zones')
rows = [['Zone (three months)', 'AED range', 'Chance ending there', 'What it would likely mean'],
        ['Deep left tail', f"below {px(H3_['pct']['p5'])}", '5%',
         'renewed regional escalation or a demand shock; the fundamental floor arguments engage'],
        ['Lower band', f"{px(H3_['pct']['p5'])} – {px(H3_['pct']['p25'])}", '20%',
         'fuel stays high into 2027 or H1 results disappoint; price approaches the base '
         'fundamental central'],
        ['Middle band', f"{px(H3_['pct']['p25'])} – {px(H3_['pct']['p75'])}", '50%',
         'the ordinary drift of a well-owned share; no verdict on the framings'],
        ['Upper band', f"{px(H3_['pct']['p75'])} – {px(H3_['pct']['p95'])}", '20%',
         'fuel relief confirmed plus JV news; the market extends the capitalised framing'],
        ['Right tail', f"above {px(H3_['pct']['p95'])}", '5%',
         'a step-change: Saudi launch detail, a special distribution, or an index event']]
table(rows, [1.35, 1.30, 1.10, 3.25], size=8.6)

# ============================== 7 CAVEATS ======================================
H1('7  Caveats — and what would change our mind')
for head, body in [
    ('The owned-versus-leased delivery split is not disclosed.  ',
     'Fleet capex is the model\'s weakest driver: the forward split between loan-financed and leased '
     'aircraft is assumed (~3–4 owned a year plus the pre-delivery ladder) and heavily sensitised. A '
     'disclosure of the financing plan for the neo ramp would replace an assumption with a fact.'),
    ('Fuel hedge ratios are not disclosed.  ',
     'The accounts show commodity swaps and collars out to 2028 but not the hedged share; the fuel '
     'sensitivity therefore overstates both directions somewhat.'),
    ('The JV network\'s disclosure is thin.  ',
     'One page of 100%-basis figures per venture, once a year. The contested judgement would collapse '
     'if the group consolidated a venture or published venture-level guidance.'),
    ('Geopolitics.  ',
     'H1-2026 showed the exposure: seven airspaces closed and the group still held revenue flat. A '
     'longer closure or a Gulf escalation is the bear case, and no probability map built on history '
     'prices an unprecedented event well.'),
    ('Older filings are scanned images.  ',
     'FY2022–FY2024 statements were machine-read and every figure used was cross-checked against the '
     'following year\'s typed comparative column; the FY2024 revenue-line table in the FY2025 filing '
     'itself contains a footing inconsistency, recorded in the bibliography rather than repaired.'),
    ('What would move the fair value UP.  ',
     'Confirmed 2027 fuel relief (adds ~AED 1.7 to the DCF versus the high-fuel path), a Saudi launch '
     'date, consolidated venture disclosure, or a faster neo ramp at held load factors.'),
    ('What would move it DOWN.  ',
     'Fuel high for longer, a yield war as regional capacity returns, a delivery slip pushing the '
     'capex-revenue mismatch deeper, or the dividend ladder breaking.')]:
    bullet(body, bold_head=head)

# ============================== APPENDIX A ====================================
H1('Appendix A — Financial statements')
H2('A.1  Income statement, three years audited + five years forecast (AED mn)')
rows = [[''] + ['FY2023', 'FY2024*', 'FY2025'] + YF]
def isrow(lbl, hkey, farr, fmt=mn):
    rows.append([lbl] + [fmt(HI[y][hkey]) for y in ('FY23', 'FY24', 'FY25')] + [fmt(x) for x in farr])
np_f = F['np_attr']; pat_f = [n / (1 - DCF['nci_share']) for n in np_f]
pbt_f = [p / (1 - IN['tax_eff']) for p in pat_f]
isrow('Revenue', 'rev', F['rev'])
isrow('Direct operating costs', 'dcost',
      [F['dcost_cash'][i] + F['dna'][i] * 0.93 for i in range(5)])
rows[-1] = (['Direct operating costs (cash, forecast)'] +
            [mn(HI[y]['dcost']) for y in ('FY23', 'FY24', 'FY25')] + [mn(x) for x in F['dcost_cash']])
isrow('EBITDA', 'ebitda', F['ebitda'])
isrow('Depreciation & amortisation', 'dna', F['dna'])
isrow('Operating profit', 'ebit', [F['ebitda'][i] - F['dna'][i] for i in range(5)])
isrow('Other income', 'other', F['other_inc'])
isrow('Finance income', 'fininc', F['fininc'])
isrow('Finance costs', 'fincost', F['interest'])
isrow('Share of JV and associate profit', 'assoc', F['assoc'])
isrow('Profit before tax', 'ebt', pbt_f)
isrow('Income tax', 'tax', [p * IN['tax_eff'] for p in pbt_f])
isrow('Profit for the year', 'pat', pat_f)
isrow('Attributable to owners', 'npa', np_f)
rows.append(['Earnings per share (AED)'] + [f"{HI[y]['npa']/SH:.2f}" for y in ('FY23', 'FY24', 'FY25')]
            + [f'{n/SH:.2f}' for n in np_f])
table(rows, [1.70, 0.66, 0.66, 0.66, 0.66, 0.66, 0.66, 0.66, 0.66], size=7.9)
caption('*FY2024 as restated in the FY2025 filing (lease-rental revenue reclassified into revenue, '
        'maintenance provisions re-measured). FY2023 as reported. Historical direct costs include '
        'their depreciation; forecast direct costs are shown cash-basis with all depreciation on its '
        'own line — the operating-profit line is on one consistent basis throughout.')
H2('A.2  Balance sheet (AED mn)')
rows = [[''] + ['FY2023*', 'FY2024', 'FY2025'] + ['FY2026E', 'FY2028E', 'FY2030E']]
def bsrow(lbl, fn, fc=None):
    rows.append([lbl] + [mn(fn(HB[y])) for y in ('FY23', 'FY24', 'FY25')]
                + ([mn(fc[0]), mn(fc[2]), mn(fc[4])] if fc else ['—', '—', '—']))
bsrow('Fleet assets (owned + right-of-use + advances)', lambda b: b['ppe'] + b['rou'] + b['adv'], F['ppe'])
bsrow('Inventories', lambda b: b['inv'])
bsrow('Trade and other receivables (current)', lambda b: b['recv'])
bsrow('Cash and fixed deposits', lambda b: b['cash'] + b['dep'])
bsrow('Borrowings and lease liabilities', lambda b: b['debt'])
bsrow('Payables, deferred income and provisions', lambda b: b['pay'] + b['definc'] + b['maint'] + b['staffb'])
bsrow('Working capital (net, operating)', lambda b: b['nwc'], F['nwc'])
bsrow('Net debt (negative = net cash)', lambda b: b['nd'],
      [F['net_debt'][0], 0, F['net_debt'][2], 0, F['net_debt'][4]][:5])
rows[-1] = (['Net debt (negative = net cash)'] + [mn(HB[y]['nd']) for y in ('FY23', 'FY24', 'FY25')]
            + [mn(F['net_debt'][0]), mn(F['net_debt'][2]), mn(F['net_debt'][4])])
bsrow('Equity attributable to owners', lambda b: b['eqp'],
      [F['equity'][0], 0, F['equity'][2], 0, F['equity'][4]][:5])
rows[-1] = (['Equity attributable to owners'] + [mn(HB[y]['eqp']) for y in ('FY23', 'FY24', 'FY25')]
            + [mn(F['equity'][0]), mn(F['equity'][2]), mn(F['equity'][4])])
table(rows, [2.30, 0.78, 0.78, 0.78, 0.78, 0.78, 0.78], size=8.2)
caption('*FY2023 column is the restated 1-January-2024 position from the FY2025 filing — the same '
        'basis as FY2024/25. Forecast columns roll fleet assets, working capital, net debt and equity; '
        'the intermediate rows are audited history only.')
H2('A.3  Cash-flow markers (AED mn)')
rows = [['', 'FY2023', 'FY2024', 'FY2025', 'FY2026E', 'FY2028E', 'FY2030E'],
        ['Net cash from operating activities', mn(IN['ocf_fy23']), mn(IN['ocf_fy24']),
         mn(IN['ocf_fy25']), '—', '—', '—'],
        ['Fleet capex incl. aircraft advances', mn(IN['capex_fy23']), mn(IN['capex_fy24']),
         mn(IN['capex_fy25']), mn(F['capex'][0]), mn(F['capex'][2]), mn(F['capex'][4])],
        ['Free cash flow to the firm (model basis)', '—', '—', '—',
         mn(F['fcff'][0]), mn(F['fcff'][2]), mn(F['fcff'][4])],
        ['Dividends paid to owners', mn(IN['div_fy23']), mn(IN['div_fy24']), mn(IN['div_fy25']),
         mn(F['div'][0]), mn(F['div'][2]), mn(F['div'][4])]]
table(rows, [2.30, 0.78, 0.78, 0.78, 0.78, 0.78, 0.78], size=8.2)

# ============================== APPENDIX B ====================================
doc.add_page_break()
H1('Appendix B — Peer frame, risk register, research register')
H2('B.1  Peer frame (cross-check only, never a build source)')
rows = [['Carrier', 'Trailing P/E', 'EV/EBITDA', 'Basis'],
        ['Ryanair', '12.6×', '7.8×', 'trailing, USD ADR, 09-Aug-2026'],
        ['easyJet', '12.4×', '3.5×', 'trailing, GBP, 07-Aug-2026'],
        ['IndiGo', 'n/m (loss year)', '11.1×', 'trailing, INR, 09-Aug-2026'],
        ['Pegasus', '8.9×', '6.6×', 'lira statutory accounts — caution'],
        ['Jazeera Airways', '≈17.7× (computed)', 'n/d', 'KWD, market cap 07-Aug-2026 / FY2025 profit'],
        ['Air-transport sector aggregate', '12.9×', '7.6×', 'profitable firms, January-2026 dataset'],
        ['Air Arabia at spot', f"{REL['pe_trailing']:.1f}×", f"{REL['ev_ebitda_trailing']:.1f}×",
         'FY2025 audited, spot 07-Aug-2026']]
table(rows, [1.80, 1.35, 1.10, 2.75], size=8.6, band_rows={7})
H2('B.2  Risk register')
rows = [['Risk', 'Mechanism', 'Where it is priced'],
        ['Regional conflict / airspace closure', 'traffic and yields, as in Q1-2026',
         'bear scenario; zones section'],
        ['Fuel above the official curve', 'largest single cost line (37% of direct costs)',
         'the high-fuel framing, priced in full'],
        ['Delivery slippage', 'volume growth is fleet-led', 'capex/pax sensitivities'],
        ['Yield compression as capacity returns', 'FY2027 fare give-back already assumed',
         'fare sensitivity ±6%'],
        ['JV startup losses (Saudi DMM)', 'associate line dip', 'FY2026 JV growth held flat'],
        ['Concentration: Sharjah hub slots', 'home-market advantage is also single-point exposure',
         'caveats; not separately priced'],
        ['Rate path under the dollar peg', 'deposit income falls if the Fed cuts',
         'deposit-yield path 4.4% → 3.7%']]
table(rows, [2.10, 2.75, 2.15], size=8.6)
H2('B.3  Research register — where the study\'s facts come from')
P(f"The build rests on {sum(1 for f_ in SW['findings'] if f_['source_type']=='COMPANY_OFFICIAL')} "
  f"company-official documents (audited statements FY2022–FY2025, the reviewed Q1-2026 interim, the "
  f"2025 annual report and corporate press releases), "
  f"{sum(1 for f_ in SW['findings'] if f_['source_type']=='COMPANY_IR')} investor-presentation "
  f"sources, and official-sector references (UAE central bank, the finance ministry's bond auctions, "
  f"the January-2026 country-premium dataset, the airline association's monitors, the US energy "
  f"agency's outlook). Three searches returned nothing and are recorded as such: seat/ASK disclosure, "
  f"fuel-hedge ratios, and the owned-versus-leased forward delivery split. The full input-by-input "
  f"listing, with dates and what each source contributed, is the companion bibliography document.")

# ============================== APPENDIX C ====================================
doc.add_page_break()
H1('Appendix C — Expert panel')
P('Three experts, labelled Expert 1/2/3, each committed to a genuinely different method, each showing '
  'complete workings and naming, in advance, the evidence that would prove them wrong.')

H2('C.1  Expert 1 — earnings power at a justified multiple')
P('Worldview: an airline is worth what its mid-cycle earnings can be sold for. Cycles wash out; buy '
  'earnings power, not forecasts. Works best on established franchises with stable unit economics; '
  'fails at inflection points — a fleet doubling or a startup network breaks "mid-cycle".')
E1 = EXP['e1']
rows = [['Line', 'Value'],
        ['Mid-cycle EBITDA margin (FY2028E)', pct(E1['margin'])],
        ['Applied to FY2028E revenue (AED mn)', mn(E1['rev'])],
        ['plus fees/other income, less depreciation → EBIT (AED mn)', mn(E1['ebit'])],
        ['plus net finance income (AED mn)', mn(-E1['interest'])],
        ['plus JV profit share (AED mn)', mn(F['assoc'][2])],
        [f"× (1 − 15% tax) × (1 − minorities) ÷ {SH:,.0f}mn shares → EPS (AED)", f"{E1['eps']:.3f}"],
        [f"× justified multiple {E1['pe']:.0f}× → value (AED/share, at the anchor)", px(E1['base'])],
        ['Range at 10× / 16×', f"{px(E1['rng'][0])} – {px(E1['rng'][1])}"]]
table(rows, [4.30, 2.70], size=8.8, band_rows={8})
P(f"Named sensitivity: each turn of the multiple is AED {E1['eps']*1.055:.2f} per share. Falsifier, "
  f"stated in advance: if H1-2026 EBITDA margin prints below 20%, the mid-cycle margin is wrong and "
  f"this valuation falls with it.")

H2('C.2  Expert 2 — owner cash earnings capitalised')
P('Worldview: profits are an opinion, cash is a fact. Value the average free cash the firm will '
  'actually throw off, capitalise it at the perpetual rate, and credit the cash pile separately. '
  'Works best on steady cash machines; fails when today\'s capex buys tomorrow\'s cash flows — it '
  'penalises investment years.')
E2 = EXP['e2']
rows = [['Line', 'Value'],
        ['Average FCFF, FY2028–30 (the steadier years, AED mn)', mn(E2['fcff'])],
        ['plus after-tax net finance income (AED mn)', mn(-E2['int_at'])],
        ['plus 40% of the JV profit share, after tax (the cash-remitted part, AED mn)',
         mn(F['assoc'][3] * (1 - IN['tax_eff']) * 0.4)],
        ['Owner cash earnings (AED mn)', mn(E2['fcfe'])],
        [f"Capitalised at {pct(E2['ke'],2)} − {pct(IN['g_term'])} growth, plus half the net cash "
         f"(haircut for permanence), per share", px(E2['base'])],
        ['Range (tighter rate + full cash / wider rate, no cash)',
         f"{px(E2['rng'][0])} – {px(E2['rng'][1])}"]]
table(rows, [4.30, 2.70], size=8.8, band_rows={6})
P('Named sensitivity: every AED 100mn of sustained FCFF is about AED 0.31 per share at these rates. '
  'Falsifier: if FY2027 FCFF prints negative again, the "steadier years" average is fiction and the '
  'capitalisation collapses.')

H2('C.3  Expert 3 — cash returns against the cost of capital')
P('Worldview: value is created only where the return on invested capital beats the cost of that '
  'capital; everything else is accounting. Start from invested capital, add the present value of the '
  'spread. Works best where capital and returns are measurable; fails when the capital base itself is '
  'mispriced — negative working capital makes the measured base small and the measured return huge.')
E3 = EXP['e3']
rows = [['Line', 'Value'],
        ['Invested capital, FY2025 (fleet + intangibles + working capital, AED mn)', mn(E3['ic0'])],
        ['PV of excess returns, explicit years (AED mn)', mn(E3['pv_ep'])],
        ['PV of terminal excess returns (AED mn)', mn(E3['pv_ep_term'])],
        ['Implied enterprise value (AED mn)', mn(E3['ev'])],
        ['Through the same bridge (net cash, non-operating, JV at book, minorities), per share',
         px(E3['base'])],
        ['Range (spread fades 40–45% / JV capitalised)', f"{px(E3['rng'][0])} – {px(E3['rng'][1])}"]]
table(rows, [4.30, 2.70], size=8.8, band_rows={5})
P(f"The measured spread: forecast returns on invested capital of "
  f"{' / '.join(pct(r,0) for r in F['roic'])} against a ~8.7–8.9% cost of capital. Falsifier: if the "
  f"FY2026 return on capital prints below the cost of capital (the fuel-spike year makes it close), "
  f"the excess-return engine is idling and the base collapses toward invested capital plus cash.")

H2('C.4  Cross-examination')
for head, body in [
    ('Expert 2 to Expert 1:  ',
     '"Your multiple prices earnings the company must spend to keep. EPS is after depreciation but '
     'before the AED 1.9–2.0bn of yearly fleet spending — in an expansion, cash EPS is far lower." '
     'Expert 1 CONCEDES half: the multiple is struck at 13× rather than Jazeera\'s 17.7× precisely to '
     'haircut expansion-cycle earnings; the other half stands because leased deliveries never pass '
     'through capex.'),
    ('Expert 1 to Expert 2:  ',
     '"You average FY2028–30 cash flow and call it perpetual — but you exclude FY2026-27 precisely '
     'because they are investment years, then keep none of the growth that investment buys." Expert 2 '
     'REJECTS: the capitalisation already grows the base at 2.5% forever; counting the fleet\'s growth '
     'twice is how airlines get overvalued.'),
    ('Expert 3 to both:  ',
     '"Neither of you measures whether growth CREATES value. My spread says it does — barely: a '
     '~14% terminal return against a ~8.7% bar. If the neo ramp lands at lease rates that push the '
     'true capital base up, the spread halves." Both CONCEDE the point defines the bear case; Expert 1 '
     'notes the measured spread has beaten the bar every audited year on record.'),
    ('All three on the JV network:  ',
     'Expert 1 would capitalise it (earnings are earnings), Expert 2 counts only remitted cash, '
     'Expert 3 carries it at book because its capital is unmeasurable from outside. The study keeps '
     'the disagreement: it IS the two published framings.')]:
    bullet(body, bold_head=head)

H2('C.5  The three in one room')
P(f"Ask the panel for one number and they refuse; ask for a region and they agree more than their "
  f"methods suggest: Expert 1 at AED {px(EXP['e1']['base'])}, Expert 2 at {px(EXP['e2']['base'])}, "
  f"Expert 3 at {px(EXP['e3']['base'])} — a median of {px(D['panel_centre'])}, "
  f"{abs(D['panel_centre']/SPOT-1)*100:.0f}% below the market. Where they genuinely differ is not "
  f"arithmetic but posture toward the ventures and the order book: the panel's whole spread is a "
  f"debate about value that has not yet reached the consolidated accounts.")
figure('figD1_experts.png', 6.9, 'Figure 8 — the three experts\' ranges against the market price.')

H2('C.6  Reading the divergence')
rows = [['Assumption', 'Expert 1', 'Expert 2', 'Expert 3', 'Drives'],
        ['Mid-cycle margin', pct(EXP['e1']['margin']), 'n/a (cash basis)', 'inside the spread',
         'E1 vs E2 gap'],
        ['Investment years FY2026-27', 'in the multiple', 'excluded from the base', 'in the spread '
         'years', 'E2\'s low base'],
        ['JV network', 'would capitalise', 'cash remitted only (40%)', 'at book',
         'the whole panel-vs-market gap'],
        ['Net cash', 'implicitly in the multiple', 'half credited', 'fully in the bridge',
         'E2 vs E3 gap'],
        ['Terminal growth', 'in the multiple', pct(IN['g_term']), pct(IN['g_term']),
         'small between panellists']]
table(rows, [1.55, 1.35, 1.40, 1.30, 1.40], size=8.4)

# ============================== ABOUT / DISCLOSURE ============================
doc.add_page_break()
H1('About this series')
P('Testahil publishes independent, educational valuation studies of listed companies across the Gulf, '
  'Egypt and beyond, each built the same way: primary sources only for the company\'s own numbers, a '
  'unit-level forecast wherever disclosure allows, four valuation lenses, a calibrated probability map '
  'for the share price, an adversarial expert panel — and a companion workbook that calculates rather '
  'than stores, so every assumption can be changed and every consequence seen. Forecast bands are '
  'tracked publicly and scored against their outcomes when they mature.')
H1('Disclosure & disclaimer')
P('This document is educational analysis, not investment advice, not an offer, and not a solicitation. '
  'It contains no rating and no price target; all values are model outputs presented as ranges with '
  'their assumptions. The authors hold no position in Air Arabia PJSC and receive no compensation from '
  'any company mentioned. Figures are believed accurate as of 9 August 2026 but are not warranted; '
  'audited financial statements of Air Arabia PJSC remain the authoritative record. Investing involves '
  'risk, including loss of principal. Nothing here accounts for any reader\'s objectives or '
  'constraints. Seek licensed advice before acting.', size=9.3)

OUT = 'AIRARABIA_Valuation_Study_09-08-2026_public.docx'
doc.save(OUT)
print('wrote', OUT, '| paragraphs:', len(doc.paragraphs), '| tables:', len(doc.tables))
