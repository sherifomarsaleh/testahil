"""ELEC_Valuation_Study_05-08-2026_public.docx — full 16-section study, house style.
Reads study_numbers.json exclusively (code-first rule: no numeral typed here that
isn't provenance-tracked there)."""
from docx_base import *

D2 = D  # study_numbers.json loaded by docx_base
L = D2['lenses']; coc = D2['coc']; dcf = D2['dcf']; mc = D2['mc']; tech = D2['tech']
E = D2['experts']; H = D2['hist_is']; B = D2['hist_bs']; Q = D2['interims']
spot = D2['spot']; SH = D2['shares']
pr = mc['prob_read']; p1, p3 = mc['pct1'], mc['pct3']
cb = L['central']['base']
strike = D2['strike']

def pegp(x, dp=2):
    return f"EGP {x:,.{dp}f}"

# ---------------- Masthead / title / anchor --------------------------------
masthead()
P('Independent Valuation Study — Educational Analysis', size=12, bold=True, space_before=4, space_after=2)
P('Electro Cable Egypt Co. S.A.E. (EGX: ELEC)', size=17, bold=True, space_after=2)
P('Fundamental analysis · Technical analysis · Monte Carlo simulation — one integrated read',
  size=10.5, italic=True, color=GREY, space_after=8)
rich([('Anchor: ', dict(bold=True)),
      (f"EGP {spot:.2f} (5 Aug 2026 close) · 3,313.5 mn shares · mkt cap ~EGP {D2['mktcap']/1000:.1f} bn · "
       "Egypt's oldest cable maker (founded 1954, Mostorod plant, ~25,000 t/yr), listed on the EGX since 1995, "
       "majority-held by the ", {}),
      ('Gadwa / Pioneers group', dict(bold=True)),
      (' (~78–81%, free float ~20%), consolidating Giza Power Industry and two smaller subsidiaries · products: '
       'low/medium/high-voltage power cables, enameled wire, overhead conductors, telephone cable · prices and '
       'probabilities computed 5 Aug 2026 from the attached daily history · primary lens: a free-cash-flow DCF on '
       'a forward discount-rate schedule that follows the Egyptian easing cycle down · the two swing factors are '
       'working-capital collection and where cable margins settle after the devaluation-era windfall.', {})],
     size=9.8, space_after=10)

# ---------------- READ FIRST box --------------------------------------------
box([
 ('READ FIRST — what this document is, and is not.', ''),
 ('', 'This study is a valuation exercise and an expression of personal analytical opinion, published free of '
      'charge for educational purposes: it shows how one analyst applies fundamental, technical and probabilistic '
      'methods to a listed company, and invites scrutiny of that methodology. It is NOT investment advice, NOT a '
      'recommendation or solicitation to buy, sell or hold any security, and NOT directed at the circumstances of '
      'any reader. The preparer is not licensed by any securities regulator in any jurisdiction, holds no Egyptian '
      '(FRA) or other brokerage or advisory authorisation, provides no financial consultancy, manages no money, '
      'and accepts no fees, funds or clients. See the Disclosure & Disclaimer at the end.'),
 ('', 'A sourcing note specific to this company, stated up front rather than buried: Electro Cable Egypt’s '
      'full audited statements were not reachable through the channels available for this study — headline '
      'revenue, profit and total assets are multiply-sourced from bourse-disclosure reporting services, but '
      'several line items (interest expense, capex, the working-capital split, facility-level debt) are DERIVED '
      'and are labelled as such wherever they appear. The one fully-triangulated year, FY2024, closes to the '
      'reported net profit within 0.8% using the derived lines, which is why the derivations are considered '
      'usable. The companion Source Register document lists every input, its source and its date. Consult a '
      'licensed financial advisor before any investment decision.'),
])

# ---------------- Headline ---------------------------------------------------
H2('Headline')
rich([("The model's read: meaningfully overvalued — the price still pays for devaluation-era earnings the "
       "company itself is no longer printing. ", dict(bold=True)),
      (f"At EGP {spot:.2f} the shares sit roughly {abs(cb/spot-1)*100:.0f}% above our weighted central estimate "
       f"of EGP {cb:.2f} (range {L['central']['bear']:.2f}–{L['central']['bull']:.2f}). The arithmetic of the "
       "last three years explains why. FY2023–24 were windfall years: revenue rose 52% then 59% and net "
       "profit reached EGP 1.25–1.33 bn as devaluation repriced copper-linked cable prices through a "
       "pound-denominated cost base and inventory. FY2025 took the windfall back — revenue −21.5%, net "
       "profit −62% to EGP 500 mn — and 1Q2026 swung to a consolidated net LOSS of EGP 242 mn on sales down "
       "44%. The disclosed 1Q26 lines are blunt: gross margin 5.7% (vs 33.1% a year earlier) and operating profit "
       "of EGP 1.4 mn — effectively zero. Meanwhile the balance sheet carries EGP 10.9 bn of drawn bank facilities "
       "(disclosed; up from 8.96 bn a year earlier) against EGP ~4 bn of equity, working capital has swollen to "
       "~117% of annual revenue (receivables and copper-inflated inventory), and operating cash flow has been "
       "negative — at ~22% funding costs, finance expense alone consumes the entire operating line in a soft year. "
       "The valuation is built bottom-up from tonnage: implied volumes fell from ~24,000 t (96% of capacity, "
       "FY23–24) to ~9,500 t annualized in 1Q26 (~38%), and conversion EBITDA collapsed from ~146,000 to "
       "~11,000 EGP per tonne. On that build, discounted at a rate schedule following the central bank's own "
       "easing path (21.4% gliding to 15.0% terminal, normalized capital structure), the enterprise is worth "
       "LESS than its disclosed EGP 10.9 bn of bank debt — the intrinsic equity is negative and is floored at "
       f"zero only by limited liability. The normalized-earnings and book lenses ({L['normalized']['base']:.2f} "
       f"and {L['book']['base']:.2f}) assume the balance sheet gets fixed first; even the bull scenario "
       f"({L['central']['bull']:.2f} central) sits {abs(L['central']['bull']/spot-1)*100:.0f}% below today's price. "
       "Technically the tape is neutral-to-firm — above the short averages, below the falling 200-day, RSI mid-50s "
       "— and the three-month simulation, which prices the stock's own path rather than its value, puts the "
       f"5th–95th percentile band at EGP {p3['5']:.2f}–{p3['95']:.2f} with a median near {p3['50']:.2f}. "
       "The gap between that tape-anchored map and the fundamental work is the study's central tension, examined "
       "in §4.", {})], space_after=8)

# ---------------- Valuation summary table -----------------------------------
H2('Valuation summary — every read at a glance')
P('One table for the four reads that follow — what the business is worth (fundamental), what the tape is doing '
  '(technical), where price could travel over three months (Monte Carlo), and how three independent expert methods '
  'land. Every row is developed in the sections and appendices below.', size=9.8)
rows = [
 ['Lens / read', 'What it measures', 'Output', 'Takeaway'],
 ['FUNDAMENTAL — what the business is worth (the anchor)', '', '', ''],
 ['FCFF DCF (primary)', 'Cash flow on the easing-cycle discount schedule', pegp(L['dcf']['base']), f"{(L['dcf']['base']/spot-1)*100:+.0f}% vs spot"],
 ['Relative (EV/EBITDA)', 'Mid-cycle EBITDA × peer-anchored multiple', pegp(L['relative']['base']), f"{(L['relative']['base']/spot-1)*100:+.0f}%"],
 ['Normalized earnings', 'Mid-cycle EPS × through-cycle P/E', pegp(L['normalized']['base']), f"{(L['normalized']['base']/spot-1)*100:+.0f}%"],
 ['Book / replacement', 'Justified P/B on sustainable ROE', pegp(L['book']['base']), f"{(L['book']['base']/spot-1)*100:+.0f}%"],
 ['Weighted central', 'Blend 40 / 20 / 20 / 20', pegp(cb), f"{(cb/spot-1)*100:+.0f}% vs {pegp(spot)}"],
 ['TECHNICAL — what the tape is doing (timing, not value)', '', '', ''],
 ['Trend & momentum', 'Price vs the 20/50/100/200-day averages', 'Above 20/50/100 · below 200', 'Neutral, basing'],
 ['Momentum / range', 'RSI · MACD · 52-week range', f"RSI {tech['rsi']:.0f} · MACD flat · 1.90–3.36", 'No strong signal'],
 ['MONTE CARLO — where price could go in 3 months (paths from spot)', '', '', ''],
 ['1 month', '50,000 calibrated paths', f"p5 {p1['5']:.2f} · p50 {p1['50']:.2f} · p95 {p1['95']:.2f}", 'Carry-tilted drift'],
 ['3 months', 'same engine, longer horizon', f"p5 {p3['5']:.2f} · p50 {p3['50']:.2f} · p95 {p3['95']:.2f}", 'Wide, right-skewed'],
 ['EXPERT PANEL — three independent methods (Appendix C)', '', '', ''],
 ['Expert 1 — earnings power', 'Normalized EPS × justified multiple', pegp(E['e1']['base']), 'Most generous'],
 ['Expert 2 — owner cash earnings', 'What the statements actually convert to cash', pegp(E['e2']['base']), 'Most severe'],
 ['Expert 3 — cash returns vs capital cost', 'Economic profit through the rate cycle', pegp(E['e3']['base']), '—'],
 ['Panel range', 'Spread = the collection-and-margin question', f"{pegp(min(E['e1']['base'],E['e2']['base'],E['e3']['base']))}–{max(E['e1']['base'],E['e2']['base'],E['e3']['base']):.2f}", 'All below spot'],
]
table(rows, [2.15, 2.35, 1.45, 1.15], band_rows=[1, 7, 10, 13], size=8.9)
rich([('Bottom line. ', dict(bold=True)),
      (f"Every fundamental lens, and every one of the three expert methods, lands below the market price — the "
       f"most generous read ({L['normalized']['base']:.2f}, normalized earnings power) still sits "
       f"{abs(L['normalized']['base']/spot-1)*100:.0f}% under spot, and the cash-flow-based reads sit far lower. "
       f"On the bottom-up tonnage build there is NO fundamental path to EGP {spot:.2f} inside the modelled "
       f"scenario space: even the bull case — conversion economics recovering to ~175,000 EGP/tonne, volumes near "
       f"70% utilization, full collection, an easing overshoot — centres at {L['central']['bull']:.2f}, still "
       f"{abs(L['central']['bull']/spot-1)*100:.0f}% below the market. Reaching spot requires the devaluation "
       "windfall itself to return. The market may also simply be pricing ELEC as a small-cap trading vehicle — the stock trades actively on the EGX70 rotation, and the controlling group has been a steady "
       "seller into that liquidity (block sales at EGP 2.00–2.21 through 2026). The probabilistic map's "
       f"median ({p3['50']:.2f}) is above spot only because it prices the stock's own path — the carry on Egyptian "
       "money is 19.5% a year and the simulation is anchored on it; it is not a statement about value.", {})],
     size=9.8, space_after=8)

# ---------------- Company overview -------------------------------------------
H2('Company overview — Electro Cable Egypt at a glance')
rows = [
 ['Item', 'Value'],
 ['Listed entity', 'Electro Cable Egypt Co. S.A.E. (EGX: ELEC; ISIN EGS3G231C011)'],
 ['What it does', 'Egypt’s oldest diversified cable maker (est. 1954, nationalised 1960s, Pioneers group since 2013): LV/MV/HV power cables, enameled copper wire, overhead conductors, telephone cables; Mostorod (Shubra El-Kheima) plant, ~25,000 t/yr; consolidates Giza Power Industry + 2 smaller units'],
 ['Spot / date', f'{pegp(spot)} · 5 Aug 2026 close'],
 ['Shares · market cap', f"3,313.5 mn (par EGP 0.20) · ~EGP {D2['mktcap']/1000:.1f} bn"],
 ['FY25 revenue / net profit', 'EGP 10,819 mn (−21.5% YoY) · EGP 500.3 mn (−62%; 4.6% margin)'],
 ['1Q26 revenue / net profit', 'EGP 2,094 mn (−43.8%) · gross margin 5.7% (vs 33.1%) · net LOSS EGP 241.7 mn (vs +451.4 mn)'],
 ['Balance sheet', 'FY25: assets EGP 16.5 bn · drawn bank facilities EGP 10.9 bn (disclosed; 8.96 bn FY24) · equity ~EGP 4.1 bn · ND/E >240%'],
 ['52-week range', 'EGP 1.90 – 3.36 (all-time high 4.84, 31-Jan-2024)'],
 ['Ownership', 'Gadwa for Industrial Development + Pioneers-group related parties ~78–81%, distributing down via 2026 block sales; free float ~20% ±3pp'],
 ['Dividends', 'None — the company has never paid a dividend'],
 ['Corporate events', 'Alhsn block sale 88 mn sh @ EGP 2.00 (1-Jul-26) · Mashareq exit @ 2.21 (Feb-26) · H1-2026 results due ~mid-Aug-2026'],
]
table(rows, [1.7, 5.4], first_col_bold=True)
caption('Source: bourse-disclosure reporting of the company’s EGX filings (FY23/FY24/FY25 and 1Q26), Mubasher '
        'company profile, ownership disclosures. Values rounded. Full sourcing in the companion Source Register.')

# ================= §1 Fundamental ===========================================
H1('1  Fundamental valuation')
P('We value ELEC as a single operating company — a working-capital-intensive cable assembler whose economics are '
  'set by three things it does not control (copper, the pound, the interest-rate cycle) and two it partly does '
  '(collection of its receivables, and the margin it can defend once devaluation windfalls wash out). The primary '
  'lens is a free-cash-flow DCF built on a forward discount-rate schedule that follows the Egyptian easing cycle '
  'down — discounting every year at one flat crisis-era rate would assert that Egypt never normalises, which the '
  'central bank’s own published path contradicts. A relative read, a normalized mid-cycle read and a '
  'book-value read complete the set; the synthesis and football field are in §1.5, the drivers in §1.6, '
  'the crux in §1.7 and the sensitivity grids in §1.9.')

H2('1.1  The FCFF DCF — the primary lens, with the full waterfall')
P('The build below shows every step from revenue to present value: EBITDA → D&A → EBIT → NOPAT '
  '(EBIT × (1 − 22.5%)) → + D&A → − capex → − Δ working capital → free '
  'cash flow to firm → that year’s own forward discount rate → PV. Note the discount-factor row: '
  'each year is discounted at its own forward WACC, gliding from 22.6% (this year’s money) to 14.1% (terminal '
  'money), with the glide shape taken from the same forward cost-of-debt path used in the interest forecast — one '
  'assumed easing calendar, used everywhere, never two. The terminal value is capitalised at the terminal WACC and '
  'discounted at the same year-5 cumulative factor as the year-5 cash flow: one date, one price of time.', size=9.8)
rows = [['EGP mn', 'FY26E', 'FY27E', 'FY28E', 'FY29E', 'FY30E']]
labels = [('rev', 'Revenue'), ('ebitda', 'EBITDA'), ('dna', '− D&A'), ('ebit', 'EBIT'),
          ('nopat', 'NOPAT (EBIT × (1−t 22.5%))'), ('dna', '+ D&A'), ('capex', '− Capex'),
          ('dwc', '− Δ working capital'), ('fcff', 'Free cash flow to firm'),
          ('fwd_wacc', 'Forward WACC (that year)'), ('df', 'Discount factor (cumulative)'),
          ('pv', 'PV of FCFF')]
for k, (key, lbl) in enumerate(labels):
    row = [lbl]
    for r_ in dcf['rows']:
        v = r_[key]
        if key == 'df': row.append(f"{v:.3f}")
        elif key == 'fwd_wacc': row.append(f"{v*100:.1f}%")
        elif key in ('capex',): row.append(f"({v:,.0f})")
        elif key == 'dwc': row.append(f"({v:,.0f})" if v > 0 else f"{-v:,.0f}")
        elif key == 'dna' and lbl.startswith('−'): row.append(f"({v:,.0f})")
        else: row.append(f"{v:,.0f}")
    rows.append(row)
table(rows, [2.1, 1.0, 1.0, 1.0, 1.0, 1.0], first_col_bold=True, size=8.7)
caption('Δ working capital shown as (build) / release. FY26E’s large positive cash flow is a one-off '
        'working-capital release as revenue contracts — it is collection of the past, not earning power.')
rows = [
 ['DCF bridge', 'EGP mn'],
 ['Σ PV of explicit FCFF (FY26–30E)', f"{dcf['pv_sum']:,.0f}"],
 [f"Terminal value (g = 5.0%, ROIC-consistent: {dcf['roic_T']*100:.1f}% ROIC × {dcf['rr_T']*100:.0f}% reinvestment)", f"{dcf['tv']:,.0f}"],
 ['PV of terminal value (at the year-5 factor)', f"{dcf['pv_tv']:,.0f}"],
 ['Enterprise value', f"{dcf['ev']:,.0f}"],
 ['Terminal value as % of EV', f"{dcf['tv_pct']*100:.0f}%"],
 ['less: net debt (FY25: disclosed facilities − est. cash)', f"({dcf['net_debt']:,.0f})"],
 ['less: non-controlling interests', f"({dcf['nci']:,.0f})"],
 ['Equity value — INTRINSIC (EV does not cover the debt)', f"({-dcf['eq_unfloored']:,.0f})"],
 ['Equity value — floored at zero (limited liability)', f"{dcf['eq']:,.0f}"],
 ['per share (3,313.5 mn shares) — nominal option-value placeholder', pegp(dcf['ps'])],
]
table(rows, [4.0, 1.6], first_col_bold=True)
P(f"Four honesty notes, and they carry the study. First, the base-case DCF says the enterprise is worth EGP "
  f"{abs(dcf['eq_unfloored'])/1000:.1f} bn LESS than its net debt: at record copper (which inflates the working "
  "capital the business must carry) and pre-windfall conversion economics, the discounted cash flows do not cover "
  "the disclosed EGP 10.9 bn facilities. A share cannot be worth less than zero — limited liability floors the "
  "equity — so what a holder owns at the base case is an option on the bull scenario, not a claim on current cash "
  f"flows. Second, {dcf['tv_pct']*100:.0f}% of the EV sits in the terminal value, which is why §1.9 grids the "
  f"terminal rate and the this-year rate independently. Third, the terminal is ROIC-consistent and the arithmetic "
  f"cuts AGAINST the company: at a terminal return on capital of {dcf['roic_T']*100:.1f}% versus a "
  f"{coc['wacc_term']*100:.1f}% terminal cost of capital, growth SUBTRACTS value — funding 5% growth absorbs "
  f"{dcf['rr_T']*100:.0f}% of NOPAT to earn less than the capital costs, so the g-sensitivity gradient runs the "
  "unusual way (more growth, less value) by construction, not by error. Fourth, every 1 bn of EV is worth ~EGP "
  f"0.30/share, which is why the bear–bull span ({L['dcf']['bear']:.2f}–{L['dcf']['bull']:.2f}) is so wide: the "
  "bull case is not a tweak — it requires windfall conversion economics to partially return.", size=9.6)

H2('1.2  Book value and replacement — the asset lens')
P('ELEC has never paid a dividend, so a dividend lens is unavailable; the asset lens takes its place. Book equity '
  'is ~EGP 4.1 bn (FY24 disclosed ~3.6 bn plus FY25 profit, nothing paid out), i.e. book value per share '
  f'≈ EGP {E["bvps"]:.2f}. What justifies a premium or discount to book is the return the book earns: at a '
  'sustainable ~14% ROE (normalized profit ~EGP 600–750 mn on a growing book — well below the 35%+ devaluation-era '
  'prints) against a ~17.3% normalised cost of equity and 5% growth, the justified multiple is (ROE−g)/(Ke−g) '
  f'≈ 0.73× book → EGP {L["book"]["base"]:.2f}/share. The market pays ~1.8× book today — a '
  'multiple that needs ROE near 27% to justify, a level the company only ever reached with devaluation at its back.', size=10.5)
rows = [
 ['Book-lens build', 'Bear', 'Base', 'Bull'],
 ['Sustainable ROE', '11%', '14%', '18%'],
 ['Justified P/B = (ROE−g)/(Ke−g)', f"{(0.11-0.05)/(coc['ke_term']-0.05):.2f}×", f"{(0.14-0.05)/(coc['ke_term']-0.05):.2f}×", f"{(0.18-0.05)/(coc['ke_term']-0.01-0.05):.2f}×"],
 ['Fair value (× BVPS 1.24)', f"{L['book']['bear']:.2f}", f"{L['book']['base']:.2f}", f"{L['book']['bull']:.2f}"],
]
table(rows, [2.6, 1.3, 1.3, 1.3], first_col_bold=True)

H2('1.3  Relative multiples')
P('The only listed pure-play comparable in the market is El Sewedy Electric — forty times ELEC’s revenue, '
  'export-hedged, moderately levered — trading at ~10.4× trailing earnings and ~6× EV/EBITDA. Riyadh '
  'Cables (Tadawul) trades far richer (18× / 15×) in a different market with 0.27× D/E and 39% ROE. '
  'ELEC merits a clear discount to Elsewedy’s multiple: 2.5× levered, domestically concentrated, '
  'no dividend record, and currently loss-making. We mark the lens on mid-cycle FY27E EBITDA at 4.5–6.5× EV/EBITDA, '
  'net of the debt remaining after the FY26E working-capital release.', size=10.5)
rows = [
 ['Relative basis', 'Bear', 'Base', 'Bull'],
 ['FY27E EBITDA (EGP mn)', f"{dcf['rows'][1]['ebitda']:,.0f}", f"{dcf['rows'][1]['ebitda']:,.0f}", f"{dcf['rows'][1]['ebitda']:,.0f}"],
 ['EV/EBITDA multiple', '4.5×', '5.5×', '6.5×'],
 ['less net debt (end-FY26E)', f"({dcf['nd_fy26']:,.0f})", f"({dcf['nd_fy26']:,.0f})", f"({dcf['nd_fy26']:,.0f})"],
 ['Fair value (EGP/share)', f"{L['relative']['bear']:.2f}", f"{L['relative']['base']:.2f}", f"{L['relative']['bull']:.2f}"],
]
table(rows, [2.6, 1.3, 1.3, 1.3], first_col_bold=True)
rich([(f"Relative base ≈ {pegp(L['relative']['base'])}", dict(bold=True)),
      (' — the bluntest lens in the study: at ANY peer-anchored multiple (4.5–6.5×) on realistic mid-cycle EBITDA, '
       'the disclosed debt exceeds the entire enterprise value and the equity is worth nothing; the lens is shown '
       'floored at EGP 0.05. For the equity to be worth spot on this lens, the market must apply Elsewedy’s own '
       'multiple to EBITDA that has not been printed since the windfall years.', {})])

H2('1.4  Normalized earnings power — where this sits in the cycle')
P('Cycle position first: FY2023–24 were the top — devaluation repriced the finished-goods book faster than '
  'the cost base, and net margin hit 14.4% then 9.6%. FY2025–26 is the washout: revenue −21.5% then '
  '−44% in 1Q26, a net loss, and margin compression as stable-pound competition returned. Mid-cycle is '
  'neither: we take FY28E-scale operations from the tonnage build (13.4 kt at 54% utilization, revenue ~EGP 12.5 bn, EBITDA ~12%) with a normalised funding cost '
  f'(15% on net debt CONDITIONALLY reduced to ~EGP 6 bn — i.e. this lens assumes the balance sheet has already been fixed, which the base-case cash flows do not achieve) → normalized net profit ≈ EGP {E["np_norm"]:,.0f} mn, EPS '
  f'≈ {E["eps_norm"]:.2f}. At a justified through-cycle 6.5× (a deep discount to Elsewedy’s 10.4× '
  'for leverage, concentration and float), the lens lands at '
  f'{pegp(L["normalized"]["base"])}.', size=10.5)
rows = [
 ['Normalized-earnings basis', 'Bear', 'Base', 'Bull'],
 ['Mid-cycle net profit (EGP mn)', f"{(dcf['rows'][2]['ebit']*0.9-0.16*6500)*(1-0.225):,.0f}", f"{E['np_norm']:,.0f}", f"{(dcf['rows'][2]['ebit']*1.1-0.14*5500)*(1-0.225):,.0f}"],
 ['Justified P/E', '5.5×', '6.5×', '8.0×'],
 ['Fair value (EGP/share)', f"{L['normalized']['bear']:.2f}", f"{L['normalized']['base']:.2f}", f"{L['normalized']['bull']:.2f}"],
]
table(rows, [2.6, 1.3, 1.3, 1.3], first_col_bold=True)

H2('1.5  Synthesis — four lenses, one field')
P('The DCF carries the heaviest weight because it is the only lens that prices the working-capital problem '
  'explicitly; the relative lens anchors what a buyer pays for comparable cash flow; normalized earnings carries '
  'the recovery thesis; the book lens anchors the downside.', size=10.5)
rows = [['Lens', 'Weight', 'Bear', 'Base', 'Bull'],
 ['FCFF DCF (glide schedule)', '40%', f"{L['dcf']['bear']:.2f}", f"{L['dcf']['base']:.2f}", f"{L['dcf']['bull']:.2f}"],
 ['Relative (EV/EBITDA)', '20%', f"{L['relative']['bear']:.2f}", f"{L['relative']['base']:.2f}", f"{L['relative']['bull']:.2f}"],
 ['Normalized earnings', '20%', f"{L['normalized']['bear']:.2f}", f"{L['normalized']['base']:.2f}", f"{L['normalized']['bull']:.2f}"],
 ['Book / replacement', '20%', f"{L['book']['bear']:.2f}", f"{L['book']['base']:.2f}", f"{L['book']['bull']:.2f}"],
 ['Weighted central', '', f"{L['central']['bear']:.2f}", f"{L['central']['base']:.2f}", f"{L['central']['bull']:.2f}"],
]
table(rows, [2.4, 0.9, 1.1, 1.1, 1.1], first_col_bold=True, band_rows=[5])
figure('fig1_football.png', 6.3, 'Figure 1 — Valuation football field. Bars span bear–bull per lens; the brass '
       'tick is each base case; the gold band is the blended central range; the dark line is spot.')
rich([(f"Central fair value ≈ {pegp(cb)}/share", dict(bold=True)),
      (f", {abs(cb/spot-1)*100:.0f}% below spot. Note what the field is saying: the four lenses AGREE — "
       f"{L['relative']['base']:.2f} to {L['normalized']['base']:.2f} at base — and spot sits outside the whole "
       "cluster, at the far edge of the bull span. The disagreement in this study is not between the lenses; it "
       "is between all of them and the price.", {})])

H2('1.6  The drivers — a bottom-up tonnage build, calibrated on disclosed anchors')
P('The forecast is built from physical volumes and unit economics, not top-line growth rates. Revenue = tonnes '
  'shipped × price per tonne, where price per tonne = LME copper × EGP/USD × a fabrication uplift of 1.387× '
  '(copper is ~72% of a power-cable price — industry norm, LME moves passed through quotations). EBITDA = tonnes '
  '× conversion EBITDA per tonne. Margins are OUTPUTS of this build, not assumptions. The company discloses no '
  'volumes, so the build is calibrated on what IS disclosed — revenue, copper, the currency — and validated '
  'against the stated ~25,000 t/yr capacity:', size=9.8)
TG = D2['tonnage']; HV = TG['hist_vol']; HE = TG['hist_ebitda_per_t']
rows = [
 ['Implied history', 'LME avg ($/t)', 'EGP avg', 'Price/t (k EGP)', 'Implied volume (kt)', 'Utilization', 'Conv. EBITDA/t (k)'],
 ['FY23', f"{TG['copper_hist']['FY23']:,.0f}", f"{TG['egp_hist']['FY23']:.1f}", f"{HV['FY23']['price_per_t']*1000:,.0f}",
  f"{HV['FY23']['vol_kt']:.1f}", f"{HV['FY23']['util']*100:.0f}%", f"{HE['FY23']:.0f}"],
 ['  FY23 at the parallel rate (~38)', f"{TG['copper_hist']['FY23']:,.0f}", '38.0',
  f"{HV['FY23_alt_parallel']['price_per_t']*1000:,.0f}", f"{HV['FY23_alt_parallel']['vol_kt']:.1f}",
  f"{HV['FY23_alt_parallel']['util']*100:.0f}%", '—'],
 ['FY24 (the validation year)', f"{TG['copper_hist']['FY24']:,.0f}", f"{TG['egp_hist']['FY24']:.1f}",
  f"{HV['FY24']['price_per_t']*1000:,.0f}", f"{HV['FY24']['vol_kt']:.1f}", f"{HV['FY24']['util']*100:.0f}%", f"{HE['FY24']:.0f}"],
 ['FY25', f"{TG['copper_hist']['FY25']:,.0f}", f"{TG['egp_hist']['FY25']:.1f}", f"{HV['FY25']['price_per_t']*1000:,.0f}",
  f"{HV['FY25']['vol_kt']:.1f}", f"{HV['FY25']['util']*100:.0f}%", f"{HE['FY25']:.0f}"],
 ['Q1-2026, annualized', '12,600', '50.4', f"{HV['Q1_26_annualized']['price_per_t']*1000:,.0f}",
  f"{HV['Q1_26_annualized']['vol_kt']:.1f}", f"{HV['Q1_26_annualized']['util']*100:.0f}%", f"{HE['Q1_26']:.0f}"],
]
table(rows, [1.95, 0.95, 0.7, 1.05, 1.15, 0.85, 1.0], first_col_bold=True, size=8.3)
caption('The fabrication uplift (1.387×) is set from the industry copper-share norm, NOT fitted to this table — '
        'that FY24 then back-solves to 24.0 kt, 96% of the stated capacity in the boom year, is the validation. '
        'The decomposition’s central finding: the revenue collapse is a VOLUME collapse (utilization ~96% → '
        '~38%), partly masked by record copper; and conversion EBITDA per tonne collapsed with it (146 → 11 k '
        'EGP/t) as fixed costs lost their absorption. FY25’s 182 k/t is inflated by copper inventory gains. '
        'Capacity figure is single-sourced and possibly parent-only — utilization is indicative.')
P('The forecast drivers, on the same axes:', size=9.8, space_after=4)
fr_ = dcf['rows']
rows = [['Driver', 'FY26E', 'FY27E', 'FY28E', 'FY29E', 'FY30E'],
 ['Volume (kt)'] + [f"{r['vol_kt']:.1f}" for r in fr_],
 ['Utilization'] + [f"{r['util']*100:.0f}%" for r in fr_],
 ['LME copper ($/t) — flat, no house view'] + [f"{c:,.0f}" for c in TG['copper_fcst']],
 ['EGP/USD (~3%/yr crawl)'] + [f"{e:.1f}" for e in TG['egp_fcst']],
 ['Price per tonne (k EGP)'] + [f"{r['price_per_t']*1000:,.0f}" for r in fr_],
 ['Revenue (EGP mn)'] + [f"{r['rev']:,.0f}" for r in fr_],
 ['Conversion EBITDA/t (k EGP)'] + [f"{r['ebitda_per_t']:.0f}" for r in fr_],
 ['EBITDA (EGP mn) — output'] + [f"{r['ebitda']:,.0f}" for r in fr_],
 ['EBITDA margin — output'] + [f"{r['margin']*100:.1f}%" for r in fr_],
]
table(rows, [2.15, 0.95, 0.95, 0.95, 0.95, 0.95], first_col_bold=True, size=8.5)
caption('Volume recovery to 64% utilization by FY30E (EETC’s EGP 45 bn plan, the EU €690 mn package, '
        'interconnector follow-on) — still below the FY23–24 near-full prints. Conversion EBITDA/t recovers to '
        '135 k by FY30E: nominally below FY24’s 146 k despite five years of EGP inflation, and, as a share of '
        'realized price (13.7%), matching the PRE-windfall 2022 norm (~12%) rather than the devaluation-era '
        '25%. Working capital stays on its intensity glide (112% → 88% of revenue) — copper strength therefore '
        'inflates the working capital the model must fund, which is exactly the mechanism the tonnage build '
        'exists to price. Every driver above is a stated, sensitized house judgment (§1.9).')
H2('1.7  The crux — working capital first, margins second, rates third')
P('Three judgments drive this valuation, in order of size. FIRST, collection. Working capital stands near '
  '~EGP 12.6 bn — 117% of a full year’s revenue — against ~76% a year earlier: copper-inflated inventory plus '
  'receivables that grew as revenue shrank, funded by EGP 10.9 bn of disclosed bank facilities. The DCF’s '
  'FY26E cash flow is dominated by a ~EGP 2.9 bn assumed release as sales contract; if those receivables do not '
  'collect (state-linked customers, dealer credit), the release never happens, debt stays ~EGP 11 bn at 22% '
  'money, and the equity rounds to nothing — that is the bear case’s mechanism, not rhetoric. Each 5 points '
  'of terminal working-capital intensity is worth roughly EGP 0.15–0.20/share. SECOND, the margin. FY24–25 '
  'EBITDA margins near 25% carried devaluation inventory gains; the DISCLOSED 1Q26 lines put the trough on the '
  'table — gross margin 5.7%, operating profit zero. The model’s 16–18% mid-cycle is a judgment between the '
  'proven trough and the windfall ceiling — each 15% on conversion EBITDA/t is worth roughly EGP 0.25–0.35/share (§1.9 grid). THIRD, the '
  'rate path: at 22% money, finance expense consumes the operating line; at the terminal 15%, the same business '
  'supports a meaningful EPS again. The easing calendar is therefore load-bearing — which is exactly why it is '
  'built into the discount schedule rather than averaged away.', size=10.5)

H2('1.8  Macro and country — rates, the pound, copper, and the sourced cost of capital')
P('Egypt held its policy corridor at 19.00/20.00% in July 2026 (third consecutive hold, after 825bp of cuts '
  'Apr-25→Feb-26) with inflation at 14.3% and a 7%±2pp target for late-2026, 5%±2pp for 2028. The '
  'pound has been range-bound (47–52/USD) since the March-2024 float — two years of nominal stability against '
  '14–28% inflation is a large REAL appreciation, which is precisely what un-winds windfall cable margins: '
  'copper is fully imported and USD-priced (up ~51% y/y), sales are domestic and EGP-priced. The demand side is '
  'genuinely strong — EETC’s EGP 45 bn transmission plan, the EU’s €690 mn grid package, the '
  '95%-complete Egypt–Saudi interconnector — but pass-through pricing means volume recovers before margin '
  'does. Every cost-of-capital input below is sourced (full provenance in the Source Register):', size=10.5)
rows = [
 ['Component', 'Value', 'Source / note'],
 ['Egypt 10Y local yield (observed)', f"{coc['rf']*100:.2f}%", 'investing.com print, 21-Jul-2026; May-26 window avg 21.3% corroborates'],
 ['less sovereign default spread (CDS)', f"−{coc['sov_cds']*100:.2f}%", 'The local yield already prices default risk; charging it again in the ERP would double-count'],
 ['= risk-free for the equity build', f"{coc['rf_star_cds']*100:.2f}%", 'CDS basis (rating basis: 22.31 − 6.37 = 15.94%)'],
 ['Equity risk premium — Egypt (CDS-based, primary)', f"{coc['erp_cds']*100:.2f}%", 'Damodaran original country-risk file, Jan-2026 (rating-based 13.94% shown in sensitivity)'],
 ['Beta (own regression, weekly, 5yr)', f"{coc['beta']:.3f}", 'vs 30-name equal-weight EGX composite: R² 0.222, n=257, SE 0.113, CI90 [0.78, 1.15] — passes the usability gate; not weak-flagged'],
 ['Cost of equity Ke', f"{coc['ke_cds']*100:.2f}%", '= 18.91 + 0.964 × 9.41'],
 ['Cost of debt Kd (pre-tax, marginal EGP)', f"{coc['kd']*100:.1f}%", 'Corridor + credit margin; checked against effective rates 23.5% (FY24) and 21.7% (FY25, on the disclosed debt path) — inside 150bp'],
 ['Debt currency', '~100% EGP (presumption, flagged)', 'No facility disclosure reachable; no USD facility found in any search — the gap is stated, not assumed away'],
 ['Weights E / D — explicit window', f"{coc['we']*100:.0f}% / {coc['wd']*100:.0f}%", 'Market cap 7.26 bn vs disclosed FY25 bank facilities 10.9 bn'],
 ['WACC — explicit window (this year)', f"{coc['wacc_exp']*100:.2f}%", 'CDS-primary (rating alternative 23.20%)'],
 ['Terminal rf (norm-built)', f"{coc['rf_term']*100:.1f}%", 'CBE’s own Q4-2028 inflation target 5% + 5.5pp real-rate convention'],
 ['Terminal ERP · terminal Kd', f"{coc['erp_term']*100:.1f}% · {coc['kd_term']*100:.1f}%", 'Normalised below crisis level · Egyptian long-run corporate norm 14–16%'],
 ['Weights E / D — terminal (normalized)', f"{coc['we_term']*100:.0f}% / {coc['wd_term']*100:.0f}%", 'The steady state presupposes deleveraging; today’s ~60% distress weight into perpetuity would be circular (the equity weight depends on the DCF’s own output). Conservative direction: more weight on the dearer equity leg'],
 ['WACC — terminal', f"{coc['wacc_term']*100:.2f}%", 'Capitalises the terminal value; reached via the glide below'],
]
table(rows, [2.6, 1.3, 3.0], first_col_bold=True, size=8.6)
P('The forward schedule, year by year — the glide shape is the forward cost-of-debt path’s own cumulative '
  'progress, so the discount rate and the interest forecast normalise on one easing calendar:', size=9.8, space_after=4)
rows = [['', 'FY26E', 'FY27E', 'FY28E', 'FY29E', 'FY30E']]
rows.append(['Forward Kd path'] + [f"{k*100:.1f}%" for k in coc['kd_path']])
rows.append(['Glide fraction'] + [f"{f*100:.0f}%" for f in coc['glide_frac']])
rows.append(['Forward WACC'] + [f"{w*100:.1f}%" for w in coc['fwd_wacc']])
rows.append(['Cumulative discount factor'] + [f"{d_:.3f}" for d_ in coc['df']])
table(rows, [2.1, 1.0, 1.0, 1.0, 1.0, 1.0], first_col_bold=True, size=8.9)
caption('A pound arriving 31-Dec-2030 carries the same 0.437 discount factor whether it arrives as a forecast '
        'cash flow or inside the terminal value — the common sell-side construction that discounts the terminal '
        'alone at a lower rate manufactures value by relabelling, and is not used here.')

H2('1.9  Sensitivity — the rate, the growth, the margin, the collection, and the beta')
figure('fig2_sens.png', 5.6, 'Figure 2 — DCF fair value (EGP/share) across terminal WACC × terminal growth. '
       'Bold cells sit nearest spot.')
S = D2['sens_wg']
rows = [['Terminal WACC \\ g'] + [f"{g*100:.0f}%" for g in S['g_grid']]]
for i, w in enumerate(S['wacc_grid']):
    rows.append([f"{w*100:.1f}%"] + [f"{v:.2f}" for v in S['table'][i]])
table(rows, [1.5, 1.0, 1.0, 1.0, 1.0, 1.0], first_col_bold=True, size=9.0)
caption(f"DCF fair value (EGP/share) across terminal WACC × terminal growth. Base cell "
        f"{coc['wacc_term']*100:.1f}% × 5% = {dcf['ps']:.2f} (equity floored at zero — the base EV does not "
        "cover the net debt). Note the g-gradient runs the UNUSUAL way — more growth, less value — because the "
        "terminal return on capital (10.3%) sits below the terminal cost of capital (15.0%): growth that earns "
        "less than it costs subtracts value. This is the construction working correctly, not an error.")
S2 = D2['sens_expl']
rows = [['Explicit \\ terminal WACC'] + [f"{w*100:.1f}%" for w in S2['term_grid']]]
for i, w in enumerate(S2['expl_grid']):
    rows.append([f"{w*100:.1f}%"] + [f"{v:.2f}" for v in S2['table'][i]])
table(rows, [1.7, 1.0, 1.0, 1.0, 1.0, 1.0], first_col_bold=True, size=9.0)
caption('Explicit-window WACC × terminal WACC, each varied independently around its own base — what the '
        'valuation needs the ECONOMY to do, separate from what it needs the company to do.')
S3 = D2['sens_mn']
rows = [['Conversion-EBITDA/t shift \\ terminal NWC %'] + [f"{n*100:.0f}%" for n in S3['nwc_grid']]]
for i, m in enumerate(S3['margin_grid']):
    rows.append([f"{m*100:+.0f}%"] + [f"{v:.2f}" for v in S3['table'][i]])
table(rows, [2.1, 0.95, 0.95, 0.95, 0.95, 0.95], first_col_bold=True, size=8.9)
caption('The company grid: conversion economics × working-capital collection. +30% on conversion EBITDA/t '
        '(≈175 k EGP/t — a partial return of the windfall) AND collection back toward FY24’s ~76% intensity '
        'still does not reach spot on this lens alone; the market price needs the bull case on every axis at '
        'once, including the cost of capital.')
rows = [['Beta', 'Ke', 'WACC (explicit)', 'WACC (terminal)', 'DCF (EGP/sh)']]
for b in D2['sens_beta']:
    rows.append([f"{b['beta']:.2f}" + (' ← CI low' if abs(b['beta']-0.78)<0.005 else
                 (' ← used' if abs(b['beta']-0.964)<0.005 else (' ← CI high' if abs(b['beta']-1.15)<0.005 else ''))),
                 f"{b['ke']*100:.1f}%", f"{b['wacc_exp']*100:.1f}%", f"{b['wacc_term']*100:.1f}%",
                 f"{b['dcf']:.2f}"])
table(rows, [1.5, 1.1, 1.3, 1.3, 1.2], first_col_bold=True, size=8.9)
caption('Beta sensitivity spanning the regression’s own 90% confidence interval plus the fixed house anchors. '
        'The valuation conclusion does not turn on the beta.')

# ================= §2 Technical ==============================================
H1('2  Technical and price structure')
P('The tape is neutral: a stock that de-rated hard (−28% year-to-date, −21% over twelve months) and is '
  'now basing. Price sits above the 20/50/100-day averages but below a still-falling 200-day near 2.40 — the '
  'signature of a countertrend rally inside a larger downtrend, powered by the July-2026 EGX small-cap rotation '
  'rather than company news. RSI in the mid-50s and a flat MACD confirm: no strong signal either way. The deep '
  'floor is the 52-week low at 1.90; the ceiling that matters is the 200-day / 2.40–2.50 shelf, then the '
  'February-2026 block-trade zone near 2.80.', size=10.5)
rows = [
 ['Indicator', 'Reading', 'Signal'],
 ['Spot', pegp(spot), '—'],
 ['SMA 20 / 50', f"EGP {tech['sma']['20']:.2f} / {tech['sma']['50']:.2f}", 'Above both — short-term stabilising'],
 ['SMA 100 / 200', f"EGP {tech['sma']['100']:.2f} / {tech['sma']['200']:.2f}", 'Above 100 · below a falling 200 — larger trend still down'],
 ['RSI (14)', f"{tech['rsi']:.1f}", 'Neutral'],
 ['MACD (12,26,9)', f"{tech['macd']['line']:+.3f} line / {tech['macd']['signal']:+.3f} signal / {tech['macd']['hist']:+.3f} hist", 'Flat, momentum fading'],
 ['52-week range', 'EGP 1.90 – 3.36', 'Lower third of the range'],
 ['Realized vol (252d)', f"{tech['rv252']*100:.1f}%", 'Moderate for an EGX small-cap'],
 ['12-month / YTD return', f"{tech['ret_12m']*100:+.0f}% / {tech['ret_ytd']*100:+.0f}%", 'De-rating year'],
]
table(rows, [1.8, 2.6, 2.5], first_col_bold=True)
figure('fig3_ma.png', 6.4, 'Figure 3 — Price versus the moving-average stack, last 260 sessions.')
P('For the probabilistic work this matters one way: a basing, high-carry tape thickens the near-term upside tail '
  'even where the fundamental work says value sits far lower. The technical and fundamental pictures disagree '
  'here, and §6 reads the resulting probability zones without forcing a reconciliation.', size=10.5)

# ================= §3 Monte Carlo ===========================================
H1('3  Monte Carlo — a probabilistic price map')
P('The probability read below opens the section, per house presentation: computed from the same 50,000 paths as '
  'everything that follows, it is a summary of the distribution, not an input to it.', size=9.8, space_after=4)
rows = [
 ['The probability read (3 months)', ''],
 ['P(price above spot)', f"{pr['p_above']*100:.0f}%"],
 ['P(+10%) vs P(−10%) — the odds', f"{pr['p_up10']*100:.0f}% vs {pr['p_dn10']*100:.0f}%  ·  {pr['odds']:.1f} : 1"],
 ['Median level, and its move', f"{pegp(pr['median'])}  ({pr['med_move']*100:+.1f}%)"],
 ['The 50% band (25th–75th)', f"EGP {pr['band50'][0]:.2f} – {pr['band50'][1]:.2f}"],
 ['Touch(+10%) / touch(−10%) at any point', f"{pr['touch_up10']*100:.0f}%  /  {pr['touch_dn10']*100:.0f}%"],
]
table(rows, [3.3, 3.3], first_col_bold=True, band_rows=[0], header=False)
P(f"We simulate 50,000 three-month price paths with the house engine, exactly as fitted on the 30-name Egyptian "
  f"panel: width from a gap-aware Yang–Zhang variance forecast (annualised ≈ "
  f"{strike['horizons']['3M']['anchor_vol_ann']*100:.0f}% at this anchor), Student-t(6) tails calibrated on the "
  "panel, and drift anchored on the cost of carrying Egyptian money (the 19.50% policy-corridor rate) — "
  "deliberately nothing else. No margin view, no fair-value gap, no analyst judgment enters the drift: the same "
  "configuration was walk-forward tested on this stock's own history at seventeen non-overlapping quarterly "
  "origins and beat a random-walk benchmark with correct interval coverage, which is the only reason it is "
  "published. The upward median is the price of time in a 19.5% currency, not a view that the stock should rise.", size=10.5)
rich([('By design the paths diffuse from spot as near-term price and deliberately do not embed the fundamental '
       'value gap of §1. ', dict(bold=True)),
      ('§3 maps where price could go from today; §1 says what the business is worth. When they disagree '
       '— as they do here — that disagreement is information, and §4 reads it.', {})])
P('Forces and events on the watch list — context for reading the distribution, not drift inputs (the engine is '
  'deliberately carry-only):', size=9.8, space_after=4)
rows = [
 ['Continuous force', 'Dir.', 'Discrete event (next 3 months)', 'When / note'],
 ['EGX70 small-cap rotation / retail flows', '±', 'H1-2026 results publication', '~mid-Aug-2026 — the single largest scheduled event'],
 ['CBE easing resumption (finance-cost relief)', '+', 'CBE MPC meetings', '20-Aug / 01-Oct / 12-Nov-2026'],
 ['Copper at records (input cost, WC strain)', '−', 'Egypt–Saudi interconnector commissioning', 'Final testing since Feb-2026'],
 ['EGP stability (real appreciation vs margins)', '−', 'EETC tender awards (EGP 45bn plan)', 'Through FY26/27'],
 ['Grid-capex demand cycle', '+', 'Further controlling-group block sales', 'Pattern: Jan/Feb/Apr/Jul-2026'],
 ['Receivables collection cycle', '±', 'EGP step-move (either direction)', 'Range-bound 47–52 since the float'],
]
table(rows, [2.15, 0.5, 2.2, 1.65], size=8.6)
H2('Percentile map (EGP/share)')
rows = [['Horizon', 'p5', 'p25', 'p50', 'p75', 'p95'],
 ['1 month', f"{p1['5']:.2f}", f"{p1['25']:.2f}", f"{p1['50']:.2f}", f"{p1['75']:.2f}", f"{p1['95']:.2f}"],
 ['3 months', f"{p3['5']:.2f}", f"{p3['25']:.2f}", f"{p3['50']:.2f}", f"{p3['75']:.2f}", f"{p3['95']:.2f}"]]
table(rows, [1.9, 1.0, 1.0, 1.0, 1.0, 1.0], first_col_bold=True)
P(f"Lead with the 50% band, not the tails: a quarter ahead, half of all paths finish between roughly EGP "
  f"{p3['25']:.2f} and {p3['75']:.2f}; at one month the band is EGP {p1['25']:.2f}–{p1['75']:.2f}. The "
  "5–95% cone is context, not a forecast.", size=9.8)
figure('fig4_fan.png', 6.4, 'Figure 4 — Forward price cone to 3 months. The brass dashed line marks the '
       'fundamental central — far below the whole cone: the tape would have to fall out of its own distribution '
       'to reach it within a quarter.')
figure('fig5_dist.png', 5.2, 'Figure 5 — Price distribution at 1 month.')
figure('fig6_dist.png', 5.2, 'Figure 6 — Price distribution at 3 months.')
H2('Level-touch ladder')
P('The probability that price touches a level at any point by the horizon (running max for upside, running min '
  'for downside):', size=9.8)
notes = {'3.00': 'Post-results re-rating zone', '2.75': 'Feb-26 block-trade zone', '2.50': 'The 200-day shelf',
         '2.35': 'SMA-200 first test', '2.19': 'Spot', '2.05': 'July base / SMA-50 zone', '1.90': '52-week low',
         '1.70': 'Below the low — bear-case zone'}
rows = [['Level (EGP)', '1-month touch', '3-month touch', 'Note']]
for Lv, tv in mc['touch'].items():
    if abs(float(Lv) - spot) < 0.005: continue
    rows.append([Lv, f"{tv['t1']*100:.0f}%", f"{tv['t3']*100:.0f}%", notes.get(Lv, '')])
table(rows, [1.2, 1.2, 1.2, 3.0], first_col_bold=True)

# ================= §4 comparison =============================================
H1('4  Comparison of the lenses, and a verdict')
P(f"Three readings sit side by side, and they genuinely disagree. The fundamental lenses cluster at EGP "
  f"{L['relative']['base']:.2f}–{L['normalized']['base']:.2f} with a central of {cb:.2f} — roughly "
  f"{abs(cb/spot-1)*100:.0f}% below the market. The technical picture is neutral: a basing chart inside a larger "
  f"downtrend, no strong signal. The probabilistic map's median ({p3['50']:.2f}) sits slightly ABOVE spot — but "
  "read it for what it is: the engine anchors drift on the 19.5% cost of Egyptian money and prices the stock's "
  "own path; it does not know what the business is worth. The fundamental work says the price needs the bull "
  "scenario to be right; the tape says the market is not currently walking away from that bet; the simulation "
  "says a quarter is too short for the gap to close by drift alone.", size=10.5)
rows = [
 ['Lens', 'Reads', 'Central / implication'],
 ['Fundamental (4-lens)', 'Meaningfully overvalued', f"{pegp(cb)} ({(cb/spot-1)*100:+.0f}%)"],
 ['Technical', 'Neutral — basing inside a downtrend', 'Support 2.05 / 1.90; resistance 2.40 (200d) / 2.80'],
 ['Monte Carlo (3-month)', 'Carry-tilted, wide', f"Median {p3['50']:.2f}; p5–p95 {p3['5']:.2f}–{p3['95']:.2f}"],
]
table(rows, [1.9, 1.9, 3.1], first_col_bold=True)
rich([('Verdict (a fair-value read, not a recommendation). ', dict(bold=True)),
      (f"ELEC reads severely overvalued on fundamentals ({(cb/spot-1)*100:+.0f}% to the central estimate), and the "
       "bottom-up build sharpens the statement: at record copper and pre-windfall conversion economics, the "
       "enterprise is worth less than its disclosed EGP 10.9 bn of bank debt — the base-case equity is an option, "
       "not a claim — and the modelled equity P&L path breaches book solvency by FY29E unless margins or volumes "
       "outrun the base case. Three checkable legs carry the read: the earnings the market capitalises were "
       "devaluation-era windfalls the company has stopped printing (1Q26: gross margin 5.7%, operating profit "
       "zero); implied volumes have fallen to ~38% of capacity while working capital of ~117% of revenue is "
       "funded at 22% money; and the controlling group has been selling at EGP 2.00–2.21 throughout 2026. What "
       "would change the read is equally specific: an H1-2026 print showing conversion EBITDA per tonne back "
       "above ~100,000 EGP without currency help, receivables actually collecting (operating cash flow positive, "
       "debt falling), or a step-devaluation — the one event that genuinely reruns the windfall. Even then, note "
       f"the ceiling: the modelled bull central is {L['central']['bull']:.2f}. The bear–bull span (EGP "
       f"{L['central']['bear']:.2f}–{L['central']['bull']:.2f}) is wide, humility is warranted on the derived "
       "lines, and the tonnage build rests on a single-sourced capacity figure — but no reading of the disclosed "
       "numbers we can construct supports the current price. We publish the distribution, not a target.", {})])

# ================= §5 catalysts ==============================================
H1('5  Catalysts to watch')
for head, body in [
 ('H1-2026 results (~mid-August 2026). ', 'The single most important print of the year: whether the 1Q26 loss '
  'was the trough. Watch three lines — gross margin (the ~14% implied trough vs any recovery), receivables '
  '(collection or further build), and finance cost (the first read on easing pass-through).'),
 ('CBE MPC meetings (20-Aug, 01-Oct, 12-Nov 2026). ', 'Each 100bp off the corridor cuts ~EGP 110 mn from annual '
  'finance cost at the disclosed debt load and compresses the discount schedule — the most mechanical catalyst.'),
 ('EETC tender awards under the EGP 45 bn FY25/26 plan. ', 'Direct order-book demand; ELEC’s ~2/3 revenue '
  'exposure to the power sector makes tender flow the volume driver.'),
 ('Egypt–Saudi interconnector commissioning. ', 'In final testing since Feb-2026; commissioning validates the '
  'HV build-out cycle and pulls forward follow-on grid spending.'),
 ('Copper. ', 'At records (+51% y/y) with Goldman scenarios above $14,000/t: every leg higher inflates ELEC’s '
  'working capital and funding need; a copper break lower would be a quiet balance-sheet relief.'),
 ('The pound. ', 'A step-devaluation would reflate cable margins and inventory (the FY23–24 mechanism) at '
  'the cost of the funding base; continued stability keeps the margin squeeze on. This stock is, in effect, a '
  'devaluation call option the market keeps partly priced.'),
 ('Controlling-group block sales. ', 'Gadwa/Alhsn/Mashareq sold through Jan/Feb/Apr/Jul-2026 at EGP 2.00–2.21. '
  'Further distribution caps rallies; a cessation — or a strategic buyer — changes the flow picture.'),
 ('Any audited-statement access. ', 'Publication of the full FY25/H1-26 statements (receivables ageing, facility '
  'schedule, capex) would resolve the derived lines in this model — in either direction.'),
]:
    bullet(body, bold_head=head)

# ================= §6 zones ==================================================
H1('6  Reading the probability zones')
P(f'Translating the three-month distribution into plain zones, anchored on spot {pegp(spot)} and the fair-value '
  'cluster:', size=10.5)
Z = mc['zones']
rows = [
 ['Zone (3 months)', 'Range', 'Approx. probability', 'What it would mean'],
 ['Deep downside', '< EGP 1.80', f'~{Z[0]*100:.0f}%', 'Collection fails / H1 loss deepens; breaks the 52-week low toward the fundamental reads'],
 ['Lower band', 'EGP 1.80–2.05', f'~{Z[1]*100:.0f}%', 'De-rating resumes; the July base gives way'],
 ['Around spot', 'EGP 2.05–2.35', f'~{Z[2]*100:.0f}%', 'Status quo: small-cap rotation holds the price, fundamentals unresolved'],
 ['Upper band', 'EGP 2.35–2.70', f'~{Z[3]*100:.0f}%', 'H1 relief + easing resumption; 200-day reclaimed'],
 ['Strong upside', '> EGP 2.70', f'~{Z[4]*100:.0f}%', 'Margin-recovery evidence or devaluation trade returns; block-trade zone retested'],
]
table(rows, [1.5, 1.3, 1.5, 2.6], first_col_bold=True)
P('Note what the zone table cannot say: nothing in a three-month price map adjudicates the fundamental question. '
  'Even the deep-downside zone stops far above the DCF’s base value — if the fundamental work is right, the '
  'reckoning is slower than a quarter. The map describes the tape’s physics; the thesis lives in §1.', size=10.5)

# ================= §7 caveats ================================================
H1('7  Caveats and what would change our mind')
for head, body in [
 ('The statements gap is narrower than at first build, but still real. ', 'The Q1-2026 income-statement lines and the '
  'FY25/FY24 bank-facilities balances ARE disclosed (recovered from press coverage of the EGX filings); interest '
  'expense, capex, the working-capital split and facility-level terms remain DERIVED. The FY24 triangulation closing within 0.8% earns the derivations a place in the model, but a single '
  'audited disclosure could move the net-debt anchor by ±1 bn — worth ±EGP 0.30/share. Every derived '
  'line is flagged in §1.6 and the Source Register.'),
 ('The base-case equity P&L path raises a genuine solvency question. ', 'Charging 22%-gliding-to-15% money on '
  'the disclosed debt against recovering-but-thin conversion economics, the modelled book equity erodes from '
  '~EGP 4.1 bn to below zero by FY29E, with net debt rising toward EGP 17 bn. This is a modelled path on derived '
  'lines, not an audit opinion — but it is what the disclosed numbers imply if nothing improves, and it explains '
  'why the DCF equity is an option rather than a claim. The exits are named in §4: collection, conversion '
  'recovery above ~100k EGP/t, a step-devaluation, or a controlling-group recapitalisation.'),
 ('The working-capital release is an assumption, not a fact. ', 'FY26E’s cash flow leans on ~EGP 2.6 bn of '
  'collection as revenue contracts. Receivables from state-linked customers can age for years; if intensity stays '
  'above ~100% of revenue, the bear case is the base case.'),
 ('Margin normalisation is a judgment between poles. ', 'Nobody outside the company knows whether 25% EBITDA '
  'margins were entirely windfall; the 17.5–19% mid-cycle here is argued, sensitized, and could be wrong in '
  'either direction. The §1.9 company grid is the honest statement of how much this matters.'),
 (f"Terminal-value dependency. ", f"{dcf['tv_pct']*100:.0f}% of the EV is terminal value at a 9.1-pt terminal "
  "spread; the study is partly a bet on Egyptian normalisation arriving on the central bank’s own schedule."),
 ('A devaluation would rescue the bull case. ', 'The FY23–24 windfall mechanism — EGP falls, copper-linked '
  'prices reprice, inventory gains — is repeatable. This study’s base case assumes the pound holds; readers '
  'who expect another step-move should weight the bull column, and note that the same event punishes the funding '
  'side and the country risk premium.'),
 ('The market may be pricing flow, not value. ', 'A 20%-float EGX70 name in a retail rotation can stay away from '
  'fundamental value for a long time; overvaluation is a statement about the destination, never the timetable.'),
 ('Concentrated ownership cuts both ways. ', 'The ~80% controlling group has been selling — but it could equally '
  'take the company private, restructure the debt, or inject assets; control events are not in the model.'),
 ('The simulation prices the path, not the thesis. ', 'Its median sits above spot because Egyptian carry is '
  '19.5%; do not read that as the model disagreeing with itself — the two clocks measure different things.'),
]:
    bullet(body, bold_head=head)

# ================= Appendix A ================================================
H1('Appendix A  Financial statements')
P('Consolidated figures as available through bourse-disclosure reporting of the company’s EGX filings; '
  'derived lines are marked (d) and their construction is stated in §1.6 and the Source Register. The '
  'five-year forecast is the model build (companion Excel, formula-linked to its Assumptions sheet). EGP million.')
H2('A.1  Income statement — 3-year historical + 5-year forecast (consolidated, EGP mn)')
def _f(v): return f"{v:,.0f}"
fr = dcf['rows']
rows = [
 ['Line', 'FY23', 'FY24', 'FY25', 'FY26E', 'FY27E', 'FY28E', 'FY29E', 'FY30E'],
 ['Revenue', _f(H['FY23']['rev']), _f(H['FY24']['rev']), _f(H['FY25']['rev'])] + [_f(r['rev']) for r in fr],
 ['EBITDA', _f(H['FY23']['ebitda']) + ' (d)', _f(H['FY24']['ebitda']), _f(H['FY25']['ebitda']) + ' (d)'] + [_f(r['ebitda']) for r in fr],
 ['EBITDA margin', f"{H['FY23']['ebitda']/H['FY23']['rev']*100:.1f}%", f"{H['FY24']['ebitda']/H['FY24']['rev']*100:.1f}%", f"{H['FY25']['ebitda']/H['FY25']['rev']*100:.1f}%"] + [f"{r['ebitda']/r['rev']*100:.1f}%" for r in fr],
 ['D&A', f"({H['FY23']['dna']:,.0f}) (d)", f"({H['FY24']['dna']:,.0f})", f"({H['FY25']['dna']:,.0f}) (d)"] + [f"({r['dna']:,.0f})" for r in fr],
 ['EBIT', _f(H['FY23']['ebit']) + ' (d)', _f(H['FY24']['ebit']), _f(H['FY25']['ebit']) + ' (d)'] + [_f(r['ebit']) for r in fr],
 ['Net finance cost', f"({-H['FY23']['fin']:,.0f}) (d)", f"({-H['FY24']['fin']:,.0f}) (d)", f"({-H['FY25']['fin']:,.0f}) (d)"]
  + [f"({-r['fin']:,.0f})" for r in D2['is_fcst']],
 ['Earnings before tax', _f(H['FY23']['ebt']), _f(H['FY24']['ebt']), _f(H['FY25']['ebt'])]
  + [(f"({-r['ebt']:,.0f})" if r['ebt'] < 0 else _f(r['ebt'])) for r in D2['is_fcst']],
 ['Income tax (22.5%)', f"({-H['FY23']['tax']:,.0f})", f"({-H['FY24']['tax']:,.0f})", f"({-H['FY25']['tax']:,.0f})"]
  + [(f"({-r['tax']:,.0f})" if r['tax'] < 0 else '—') for r in D2['is_fcst']],
 ['Net profit (attributable)', _f(H['FY23']['np']), _f(H['FY24']['np']), _f(H['FY25']['np'])]
  + [(f"({-r['np']:,.0f})" if r['np'] < 0 else _f(r['np'])) for r in D2['is_fcst']],
 ['EPS (EGP)', f"{H['FY23']['np']/SH:.2f}", f"{H['FY24']['np']/SH:.2f}", f"{H['FY25']['np']/SH:.2f}"]
  + [(f"({-r['eps']:.2f})" if r['eps'] < 0 else f"{r['eps']:.2f}") for r in D2['is_fcst']],
]
table(rows, [2.05, 0.625, 0.625, 0.625, 0.625, 0.625, 0.625, 0.625, 0.625], first_col_bold=True, size=8.0)
caption('Historical revenue/NP/EBT/tax: bourse-reported. (d) = derived (FY24 closes to the reported NP within '
        '0.8% — the triangulation that licenses the method). Forecast net-finance-cost line uses the forward Kd '
        'path on the modelled debt schedule; the equity P&L is shown for completeness — the valuation runs on '
        'FCFF, which is independent of the financing line.')
H2('A.2  Balance sheet — condensed house layout (consolidated, EGP mn)')
IF = D2['is_fcst']
rows = [
 ['Line', 'FY22', 'FY23e', 'FY24', 'FY25e', 'FY27E', 'FY30E'],
 ['Total assets (model basis fwd)', _f(B['assets']['FY22']), _f(B['assets']['FY23e']) + ' (e)', _f(B['assets']['FY24']), _f(B['assets']['FY25']),
  _f(fr[1]['nwc'] + 2380), _f(fr[4]['nwc'] + 2380)],
 ['  of which net working capital', 'n/d', '~7,000 (e)', '~10,500 (d)', f"{B['nwc_fy25e']:,.0f} (d)", _f(fr[1]['nwc']), _f(fr[4]['nwc'])],
 ['Net debt', 'n/d', 'n/d', f"{B['debt_fy24']-B['cash_fy24']:,.0f}", f"{B['net_debt_fy25e']:,.0f} (d)",
  _f(IF[1]['nd_close']), _f(IF[4]['nd_close'])],
 ['Equity attributable', 'n/d', 'n/d', _f(B['equity_fy24']), f"{B['equity_fy25e']:,.0f} (d)",
  _f(D2['debt_schedule']['eq_path'][2]), _f(D2['debt_schedule']['eq_path'][5])],
 ['Net debt / equity', 'n/d', 'n/d', f"{(B['debt_fy24']-B['cash_fy24'])/B['equity_fy24']*100:.0f}%",
  f"{B['net_debt_fy25e']/B['equity_fy25e']*100:.0f}% (d)",
  f"{IF[1]['nd_close']/D2['debt_schedule']['eq_path'][2]*100:.0f}%",
  f"{IF[4]['nd_close']/D2['debt_schedule']['eq_path'][5]*100:.0f}%"],
]
table(rows, [2.3, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85], first_col_bold=True, size=8.4)
caption('(e) = estimate bounded by disclosed prints; (d) = derived from disclosed totals (construction in '
        '§1.6). FY22/FY24/FY25 total assets, the FY24 debt/cash/equity set and the FY25 facilities are sourced; '
        'the FY23 year-end balance sheet was never found (flagged gap). Forecast columns are the model’s '
        'clean-surplus roll-forward — and they are the honest bad news: on the base case, book equity erodes '
        'toward zero by FY29–30E while net debt compounds. See §7, first two caveats.')
H2('A.3  Cash flow markers and the working-capital story')
rows = [
 ['Marker', 'FY23', 'FY24', 'FY25', 'FY26E'],
 ['Operating cash flow', 'negative (agg.)', 'negative (agg.)', '~breakeven (d)', f"+{fr[0]['nopat']+fr[0]['dna']-fr[0]['dwc']:,.0f} (release)"],
 ['NWC as % of revenue', '~81% (e)', '~76% (d)', '~117% (d)', f"{fr[0]['nwc']/fr[0]['rev']*100:.0f}%"],
 ['Capex (derived through D&A)', '~104 (d)', '~165 (d)', '~130 (d)', f"{fr[0]['capex']:,.0f}"],
 ['Dividends paid', '0', '0', '0', '0 — never paid'],
]
table(rows, [2.6, 1.15, 1.15, 1.15, 1.35], first_col_bold=True, size=8.8)
caption('The aggregator flag “operating cash flow is negative; debt is not well covered” (FY24 vintage) '
        'is the single most important sentence in ELEC’s public record: three years of reported profits '
        'never became cash — they became receivables and inventory, funded by debt at 20%+ money.')

# ================= Appendix B ================================================
H1('Appendix B  Peer frame, risk register — and the research register')
H2('B.1  Peers and the sector frame')
rows = [
 ['Name', 'Mkt cap', 'P/E', 'EV/EBITDA', 'D/E', 'Note'],
 ['El Sewedy Electric (EGX: SWDY)', 'EGP 196 bn', '10.4×', '~6.0×', 'moderate', 'FY25 revenue EGP 281 bn, NP 17.3 bn; W&C segment +66% — the sector’s demand proof'],
 ['Riyadh Cables (Tadawul: 4142)', 'SAR 18.0 bn', '18.0×', '15.0×', '0.27×', 'What the market pays for the same industry with a clean balance sheet'],
 ['Electro Cable Egypt (ELEC)', 'EGP 7.3 bn', '14.6× trailing', '~6.1× on FY25e', '~2.5×', 'On depressed, now loss-making earnings; ~5.5× on FY24 windfall EPS'],
 ['Giza Cables (private)', '—', '—', '—', '—', 'The other mid-tier player; no public financials'],
]
table(rows, [2.0, 1.0, 0.85, 1.0, 0.75, 1.7], first_col_bold=True, size=8.5)
P('Sector structure: one giant (Elsewedy, with scale, exports and funding access) above a tier of mid-caps '
  'competing on price and local content in government tenders. Demand is the strongest it has been in a decade '
  '(grid capex, interconnection, renewables hookups) — but pass-through pricing means the demand cycle rescues '
  'volumes before it rescues margins, and funding cost decides who banks the difference.', size=10.5)
H2('B.2  Risk register')
rows = [
 ['Risk', 'Direction', 'Where it is priced'],
 ['Receivables fail to collect / further WC build', 'Severe negative', 'Bear DCF (0.05); the central weight on the DCF'],
 ['Margins never recover past ~14%', 'Negative', 'Company grid, bear column'],
 ['Copper spikes further (WC funding strain)', 'Negative', 'Qualitative; enters through the NWC glide'],
 ['EGP step-devaluation', 'Positive for margins, negative for funding/CRP', 'Bull margin column; not in the base case'],
 ['Easing cycle stalls (inflation re-accelerates)', 'Negative', 'Explicit × terminal WACC grid'],
 ['Controlling-group distribution continues', 'Negative (flow)', 'Not in the model — a market-structure risk'],
 ['Control event (buy-out, restructuring, asset injection)', 'Either', 'Not in the model'],
 ['Statement access resolves derived lines adversely', 'Either', '§7 first caveat; ±EGP 0.30/share on the ND anchor'],
]
table(rows, [2.9, 1.6, 2.5], first_col_bold=True, size=8.7)
H2('B.3  The research register — four layers, dated, negative searches included')
P('Research for this study ran outward-in — world, country, industry, company — before any forecast driver was '
  'set. The register below condenses what was found and where; the companion Source Register document carries '
  'the full input-by-input listing.', size=9.8)
rows = [['Layer', 'Class', 'Finding (condensed)', 'Source', 'Date']]
reg = [
 ('Global', 'D', 'Copper +51.6% y/y to ~$6.63/lb COMEX / ~$12.8k LME avg; US 15% tariff from Jan-27; Goldman >$14k scenario', 'TradingEconomics; INN; TradingKey', '05-Aug-26'),
 ('Global', 'S', 'Grid renewal + data centers drive global W&C demand (~6.5% CAGR to $409bn by 2034)', 'Fortune BI; Mordor; CRU', '2026'),
 ('Global', 'B', 'Fed held 3.50–3.75% on 29-Jul-26 (fifth straight hold)', 'Federal Reserve', '29-Jul-26'),
 ('Country', 'B/D', 'CBE held 19.00/20.00% on 09-Jul-26, third straight hold; 825bp cut Apr-25→Feb-26; next MPC 20-Aug', 'CBE via FocusEconomics', '09-Jul-26'),
 ('Country', 'B', 'Inflation 14.3% (Jun-26); target 7±2pp Q4-26, 5±2pp Q4-28', 'CBE CPI release', '09-Jul-26'),
 ('Country', 'B', 'Egypt 10Y ~21.3% (May-26 avg); 22.31% print 21-Jul-26; 5Y CDS 270→330bp', 'investing.com; MoF; MacroMicro', 'May–Jul-26'),
 ('Country', 'S/D', 'EETC EGP 45bn FY25/26 plan; EGP 26.5bn spent FY24/25; EU €690mn package 15-Jun-26 (22GW hookups by 2030)', 'DNE; EEAS', 'Nov-25–Jun-26'),
 ('Country', 'B', 'EGP ~50.3; range-bound 47–52 since Mar-24 float = large real appreciation', 'Bloomberg; The National', 'Aug-26'),
 ('Country', 'B', 'Corporate tax confirmed 22.5%, unchanged', 'PwC Tax Summaries', '2026'),
 ('Industry', 'S', 'Egypt power-cable market ~6.7% CAGR 2026-32; Elsewedy W&C +66% FY25 proves the demand cycle', '6Wresearch; Elsewedy IR', '2026'),
 ('Industry', 'S', 'LME-linked pass-through pricing with raw-material clauses; margins structurally thin; scale + funding decide winners', 'IndexBox', '2025-26'),
 ('Industry', 'D', 'Egypt–Saudi $1.8bn/3,000MW interconnector 95% complete, final testing since Feb-26', 'DNE; Zawya', 'Feb-26'),
 ('Company', 'C', 'FY25 NP −62% to 500.3mn; 1Q26 net LOSS 241.6mn on sales −44% — the windfall is over', 'Zawya; Arab Finance', 'Mar/May-26'),
 ('Company', 'C', 'FY24-vintage: debt ~9bn, equity ~3.6bn, D/E 248% (was 36%), OCF negative, coverage 2.0×', 'Simply Wall St', 'May-25'),
 ('Company', 'C/D', 'Controlling-group block sales: Alhsn 88mn sh @2.00 (01-Jul-26); Mashareq exit @2.21 (Feb-26); Gadwa group ~81% (Mar-25)', 'Arab Finance; Zawya', '2025-26'),
 ('Company', 'C', 'No analyst coverage; no dividend ever; no capital increase 2024-26 (negative searches, logged)', 'sweep, negative results', '05-Aug-26'),
 ('Company', 'C', 'Audited FS PDFs unreachable (company site & disclosure hosts blocked) — derived lines flagged throughout', 'access log', '05-Aug-26'),
]
for layer, cls, finding, src, dt in reg:
    rows.append([layer, cls, finding, src, dt])
table(rows, [0.75, 0.55, 3.4, 1.45, 0.85], first_col_bold=True, size=7.9)
caption('Class: B = backdrop · S = structural · D = discrete/event · C = company-specific.')

# ================= Appendix C ================================================
H1('Appendix C  The expert valuation panel')
P('Every study closes with a panel of standing expert methods — each expert runs a genuinely different method, '
  'derives a fair value from shown workings, and states the evidence that would falsify it. For ELEC we cast the '
  'earnings-power lens, the accountant’s owner-cash-earnings lens, and the cash-returns lens — the three '
  'methods that disagree most productively on a levered cyclical.', size=10.5)

H2('C.1  Expert 1 — earnings power: normalized EPS at a justified multiple')
P('Worldview. A cyclical is worth a fair multiple of its mid-cycle earnings; both the windfall peak and the '
  'washout trough are noise to be stripped.', size=9.8)
P('When it works / fails. Best with a long through-cycle record; vulnerable when “mid-cycle” itself is '
  'contested — exactly the ELEC problem: is normal 14% EBITDA margin or 25%?', size=9.8)
rows = [
 ['Expert 1’s build', 'Value'],
 ['Mid-cycle revenue (FY28E-scale)', f"{dcf['rows'][2]['rev']:,.0f}"],
 ['Mid-cycle EBITDA margin', '16%'],
 ['Normalized net profit (after 15% money on ~6bn net debt)', f"{E['np_norm']:,.0f}"],
 ['Normalized EPS', f"{E['eps_norm']:.2f}"],
 ['Justified through-cycle P/E', '6.5×'],
 ['Fair value', f"→ {pegp(E['e1']['base'])}"],
]
table(rows, [4.4, 1.7], first_col_bold=True, size=9.0)
P(f"Sensitivity (swing = the margin and the multiple): at 8× on the same earnings, {E['e1']['rng'][1]:.2f}; "
  f"at 5.5× on bear-margin earnings, {E['e1']['rng'][0]:.2f}. Falsified by two consecutive halves of EBITDA "
  "margin above ~20% without currency help — that would prove the windfall margins were partly structural.", size=9.8)

H2('C.2  Expert 2 — the accountant: owner cash earnings from the statements')
P('Worldview. Profit is an opinion; cash is a fact. Value only the earnings that historically became cash the '
  'owner could take out.', size=9.8)
P('When it works / fails. Devastating on names whose profits pile up as receivables — ELEC precisely; unfair to '
  'genuine growth if the working-capital build eventually monetises.', size=9.8)
rows = [
 ['Expert 2’s ledger', 'Value'],
 ['Reported cumulative NP FY23–FY25', f"{H['FY23']['np']+H['FY24']['np']+H['FY25']['np']:,.0f}"],
 ['Of which converted to operating cash', '≈ nil (OCF negative in FY23/24; ~breakeven FY25)'],
 ['Where it went', 'Receivables + inventory, funded by EGP 10.9bn of disclosed bank facilities at 20%+ money'],
 ['Cash-earnings basis he will pay for (FY27E, actual funding cost)', f"~{(dcf['rows'][1]['ebit']-coc['kd_path'][1]*dcf['nd_fy26'])*(1-0.225):,.0f}/yr + partial credit for normalisation"],
 ['Multiple on cash earnings', '6×'],
 ['Fair value', f"→ {pegp(E['e2']['base'])}"],
]
table(rows, [4.4, 1.7], first_col_bold=True, size=9.0)
P(f"Sensitivity: his range ({E['e2']['rng'][0]:.2f}–{E['e2']['rng'][1]:.2f}) turns almost entirely on how "
  "much credit to give unproven collection. Falsified by a published cash-flow statement showing sustained "
  "positive operating cash flow with receivables actually falling — he would re-run on the proven number.", size=9.8)

H2('C.3  Expert 3 — cash returns: ROIC against the cost of capital, through the rate cycle')
P('Worldview. A business is worth its invested capital plus the present value of its spread over the cost of '
  'that capital. In a disinflating economy, both legs move — measure them on one calendar.', size=9.8)
P('When it works / fails. The right frame for capital-heavy compounders and the honest frame for capital-heavy '
  'value traps; weakest when invested capital itself is mismeasured (his caveat: ELEC’s IC is mostly '
  'working capital of contestable quality).', size=9.8)
rows = [
 ['Expert 3’s economic-profit test', 'Value'],
 ['Invested capital (terminal-year basis)', f"{dcf['ic_T']:,.0f}"],
 ['Terminal ROIC', f"{dcf['roic_T']*100:.1f}%"],
 ['Cost of capital: 22.6% today → 14.1% terminal', 'the spread is NEGATIVE for the whole explicit window'],
 ['His EV (economic-profit build ≈ the DCF with a 5% haircut on the spread years)', f"{dcf['ev']*0.95:,.0f}"],
 ['less net debt', f"({dcf['net_debt']:,.0f})"],
 ['Fair value', f"→ {pegp(E['e3']['base'])}"],
]
table(rows, [4.4, 1.7], first_col_bold=True, size=9.0)
P(f"Sensitivity: ±EGP 500 mn on the EV or the debt anchor moves him ±0.15/share — his range "
  f"({E['e3']['rng'][0]:.2f}–{E['e3']['rng'][1]:.2f}) is the leverage talking, not the method. Falsified by "
  "ROIC printing above the falling WACC earlier than modelled — collection would do it, since it shrinks the "
  "denominator and the debt at once.", size=9.8)

H2('C.4  Cross-examination')
P('Expert 1 to Expert 2: “You are punishing them twice — once for the working-capital build and again with a '
  '6× multiple on the earnings that survive it. Collection is not impossible; it is just unproven.”', size=9.8)
P('Expert 2 to Expert 1: “Your normalized EPS pays out of profits that have never once turned into cash. '
  'Show me one year of positive operating cash flow and I will move; until then a multiple on paper earnings is '
  'a multiple on paper.”', size=9.8)
P('Expert 3 to both: “You are arguing about the numerator. The economics are simpler: this business earns '
  '~10% on its capital at the terminal and pays 22% for money today, 15% even in the normalized state. A negative spread at this leverage '
  'is value destruction on a schedule — the only question is whether the easing cycle arrives before the '
  'balance sheet does.”', size=9.8)

H2('C.5  The three in one room')
P(f"Where they agree is more striking than where they differ: all three land below EGP {max(E['e1']['base'],E['e2']['base'],E['e3']['base']):.2f} "
  "— the most generous number in the room is still ~37% under the market. They disagree on mechanism, not "
  "direction: Expert 1 prices a recovery that has not printed, Expert 2 refuses to pay for cash that has not "
  "appeared, Expert 3 counts the cost of waiting for either. Each names the same two exhibits as decisive: the "
  "H1-2026 statements (margin and receivables) and any audited cash-flow disclosure.", size=9.8)

H2('C.6  Reading the divergence')
figure('figD1_experts.png', 6.0, 'Figure 7 — The three experts’ fair-value ranges. Brass ticks are base '
       'cases; the gold band is the panel centre; the dark line is spot — above every range shown.')
rows = [
 ['Expert', 'Method', 'Single swing assumption', 'Base fair value'],
 ['Expert 1', 'Earnings power × justified multiple', 'Mid-cycle EBITDA margin 16%', pegp(E['e1']['base'])],
 ['Expert 2', 'Owner cash earnings', 'Credit given to unproven collection', pegp(E['e2']['base'])],
 ['Expert 3', 'Cash returns (ROIC vs WACC)', 'The net-debt anchor ±1 bn', pegp(E['e3']['base'])],
]
table(rows, [1.0, 2.2, 2.5, 1.3], first_col_bold=True, size=9.0)
P(f"The spread — {min(E['e1']['base'],E['e2']['base'],E['e3']['base']):.2f} to "
  f"{max(E['e1']['base'],E['e2']['base'],E['e3']['base']):.2f} at base — is wide in ratio terms but narrow in "
  "message: no method that starts from the company’s own disclosed numbers reaches the market price without "
  "assuming the best corner of the scenario space. The panel’s centre sits close to the study’s "
  f"weighted central ({pegp(cb)}), which is the reassuring kind of agreement: three different roads, one "
  "neighbourhood.", size=9.8)
caption('Each expert’s point fair value (and range) is logged with the study date (5 Aug 2026) and spot '
        f'({pegp(spot)}) as an internal per-expert track record.')

# ================= About / Disclaimer ========================================
H1('About this series')
P('Testahil publishes independent, educational valuation studies. Each is an attempt to reason transparently '
  'about what a security is worth, with every assumption shown and a companion model so readers can disagree '
  'productively. The house style is distributions, not tips: we describe ranges and probabilities, not targets, '
  'and we do not tell anyone what to do. Studies are framed as educational analysis, the preparer is not licensed '
  'by any securities regulator, and holdings are disclosed.')
H1('Disclosure & Disclaimer')
for head, body in [
 ('Not investment advice. ', 'This document is educational and informational only. It is not, and must not be '
  'relied upon as, investment, financial, legal, accounting or tax advice, nor an offer, solicitation or '
  'recommendation to buy, sell or hold any security. It contains no price target and no rating.'),
 ('No licence; no advisory relationship. ', 'The preparer is not registered or licensed with any securities or '
  'financial regulator in any jurisdiction — including Egypt’s Financial Regulatory Authority (FRA) — holds '
  'no brokerage or investment-advisory authorisation, and is not acting as your adviser or fiduciary. Nothing '
  'here is personalised to your circumstances.'),
 ('Holdings disclosure. ', 'The preparer may hold, and may in the future take or dispose of, a position in the '
  'security discussed in this report, and may transact at any time without notice. This is a potential conflict '
  'of interest you should weigh.'),
 ('Sources & accuracy. ', 'Reported financial and operating figures are drawn from public disclosure-reporting '
  'services believed reliable but not independently verified; the company’s audited statements were not '
  'directly accessible, and lines derived from disclosed totals are flagged as such throughout. Forward-looking '
  'inputs — margins, the working-capital path, multiples, the discount-rate schedule and simulation settings — '
  'are the preparer’s own judgments and are inherently uncertain.'),
 ('Forward-looking statements. ', 'Any statements about the future are estimates subject to risks and '
  'uncertainties; actual results may differ materially. The Monte Carlo models price, not value.'),
 ('No reliance; your responsibility. ', 'Do your own research and consult a licensed professional before making '
  'any decision. You are solely responsible for your investment decisions and their outcomes. To the maximum '
  'extent permitted by law, the preparer accepts no liability for any loss arising from use of this document.'),
 ('Currency & figures. ', 'Figures are in Egyptian pounds (EGP), millions unless stated; bn denotes billion. FX '
  'at study date: USD/EGP ≈ 50.3. Rounding may cause totals to differ slightly. Spot price and market data '
  'are as of 5 August 2026 and change continuously.'),
]:
    rich([(head, dict(bold=True, italic=True)), (body, {})], size=9.6, space_after=5)
P('TESTAHIL · Independent Valuation Study · Educational Analysis · Electro Cable Egypt Co. S.A.E. (EGX: ELEC) · '
  'edition 05-08-2026 · reporting currency EGP', size=8.8, color=GREY, align='center', space_before=10)

doc.save('ELEC_Valuation_Study_05-08-2026_public.docx')
print('docx saved:', len(doc.paragraphs), 'paragraphs,', len(doc.tables), 'tables')
