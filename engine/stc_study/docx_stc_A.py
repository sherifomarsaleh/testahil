"""Content part A: masthead → §2."""
from docx_stc_base import *

pr = D['mc']['prob_read']; q20, q60 = D['mc']['q20'], D['mc']['q60']
L = D['lenses']; tech = D['tech']; dcf = D['dcf']; ddm = D['ddm']
spot = D['spot']; E = D['experts']; cov = D['cover']

# ---------------- Masthead / title / anchor --------------------------------
masthead()
P('Independent Valuation Study — Educational Analysis', size=12, bold=True, space_before=4, space_after=2)
P('Saudi Telecom Company (Tadawul: 7010)', size=17, bold=True, space_after=2)
P('Fundamental analysis · Technical analysis · Monte Carlo simulation — one integrated read',
  size=10.5, italic=True, color=GREY, space_after=8)
rich([('Anchor: ', dict(bold=True)),
      ('SAR 43.58 (7 Jul 2026 close) · 4,989.8 mn shares (5,000 mn issued less treasury) · mkt cap ~SAR 217.5 bn (~US$58 bn) · '
       'the Kingdom’s incumbent operator and the largest MENA telecom by market value: ', {}),
      ('stc KSA', dict(bold=True)),
      (' (consumer, enterprise, wholesale — ~57% mobile share, the national fibre and 5G backbone) plus ', {}),
      ('subsidiaries', dict(bold=True)),
      (' (solutions by stc 79%, stc bank 85%, stc Kuwait 51.8%, stc Bahrain, center3 data centres, sirar, iot squared) and ', {}),
      ('minority stakes', dict(bold=True)),
      (' — 43.06% of the PIF-controlled tower company (TAWAL/Digital Infrastructure) and 9.97% of Telefónica · reporting currency SAR '
       '(pegged to USD at 3.75) · prices and probabilities computed 7 Jul 2026 from the attached daily history · primary lens: '
       'going-concern FCFF DCF, cross-checked by the dividend-policy DDM, relative multiples and normalized earnings · the swing '
       'factors: capex intensity against the locked SAR 2.20 dividend, and the discount-rate (beta) question.', {})],
     size=9.8, space_after=10)

# ---------------- READ FIRST box --------------------------------------------
box([
 ('READ FIRST — what this document is, and is not.', ''),
 ('', 'This study is a valuation exercise and an expression of personal analytical opinion, published free of charge for '
      'educational purposes: it shows how one analyst applies fundamental, technical and probabilistic methods to a listed '
      'company, and invites scrutiny of that methodology. It is NOT investment advice, NOT a recommendation or solicitation '
      'to buy, sell or hold any security, and NOT directed at the circumstances of any reader. The preparer is not licensed '
      'by any securities regulator in any jurisdiction, holds no brokerage or advisory authorisation, provides no financial '
      'consultancy, manages no money, and accepts no fees, funds or clients. See the Disclosure & Disclaimer at the end.'),
 ('', 'All values are model outputs presented as ranges and distributions because no single number should be relied on. '
      'Reported financials are the company’s own disclosure (FY2023–FY2025 IR releases on the restated '
      'continuing-operations basis; Q1-2026 release, 28 Apr 2026; Q1-2026 interim financial statements) — all from '
      'stc.com. Forward-looking inputs — the segment growth and margin paths, capex intensity, the cost of capital, '
      'terminal growth, the multiples and the Monte-Carlo factor probabilities — are the preparer’s judgments and '
      'are flagged throughout. Some balance-sheet detail lines are grouped estimates tying to disclosed totals. Consult a '
      'licensed financial advisor before any investment decision.'),
])

# ---------------- Headline ---------------------------------------------------
H2('Headline')
rich([("The model's read: modestly undervalued, with the answer hinging on whether a zero-net-debt incumbent yielding 5% "
       "can hold its margin story while funding the AI-infrastructure build. ", dict(bold=True)),
      (f"At SAR 43.58 the shares sit about {abs(L['central']['base']/spot-1)*100:.0f}% below our weighted central estimate of "
       f"SAR {L['central']['base']:.0f}. The four lenses cluster unusually tightly: the FCFF DCF lands at {L['dcf']['base']:.0f} "
       f"(80% of it terminal value — disclosed, not buried), the locked dividend policy discounts to {L['ddm']['base']:.0f}, "
       f"a justified EV/EBITDA read gives {L['relative']['base']:.0f}, and a conservative normalized-earnings read marks the floor "
       f"at {L['normalized']['base']:.0f}. In one sentence: on the cash it pays out today stc is roughly fairly valued; on the "
       "cash the business generates once capex normalizes from the current data-centre-and-5G investment phase, it is modestly "
       "cheap. The crux is concrete and observable (§1.7): the SAR 0.55-per-quarter dividend — locked by policy through "
       "the Q3-2027 distribution — costs SAR 11.0 bn a year, and at the guided 15–17.5% capex band our FY26E free cash "
       f"flow covers between 0.86× and 1.04× of it. The balance sheet carries the gap comfortably (net debt ≈ "
       "SAR 7.1 bn, ~0.3× EBITDA, after January’s $2 bn sukuk), but the equity story quietly shifted in 2024–25: "
       "stc sold control of its towers, banked SAR 12.9 bn of gains, paid a SAR 2.00 special, and is now redeploying into AI "
       "data centres (the center3–HUMAIN 1 GW ambition) and adjacencies (stc bank, Telefónica). Technically the tape is "
       "flat — price within ±1% of every major moving average, RSI 48 — a stock waiting for its next catalyst. Over "
       f"three months the Monte Carlo — zero drift, the configuration that passed the Step 0 calibration gate — places "
       f"the 5th–95th percentile band at roughly SAR {q60['5']:.0f}–{q60['95']:.0f} with the median at "
       f"{q60['50']:.1f}, and the honest core — the 50% band — at SAR {q60['25']:.0f}–{q60['75']:.0f}.", {})],
     space_after=8)

# ---------------- Valuation summary table -----------------------------------
H2('Valuation summary — every read at a glance')
P('One table for the four reads that follow — what the business is worth (fundamental), what the tape is doing (technical), '
  'where price could travel over three months (Monte Carlo), and how three independent expert methods land. Every row is '
  'developed in the sections and appendices below.', size=9.8)
rows = [
 ['Lens / read', 'What it measures', 'Output', 'Takeaway'],
 ['FUNDAMENTAL — what the business is worth (the anchor)', '', '', ''],
 ['FCFF DCF (primary)', 'Core operations + stake marks − net debt − NCI', f"SAR {L['dcf']['base']:.0f}", f"{(L['dcf']['base']/spot-1)*100:+.0f}% vs spot"],
 ['Dividend discount (policy lens)', 'The locked SAR 0.55/quarter, discounted at Ke', f"SAR {L['ddm']['base']:.0f}", f"{(L['ddm']['base']/spot-1)*100:+.0f}%"],
 ['Relative (EV/EBITDA)', 'FY26E EBITDA × justified 9.0×, bridged to equity', f"SAR {L['relative']['base']:.0f}", f"{(L['relative']['base']/spot-1)*100:+.0f}%"],
 ['Normalized earnings', 'Ex-one-off PAT × through-cycle P/E', f"SAR {L['normalized']['base']:.0f}", f"{(L['normalized']['base']/spot-1)*100:+.0f}% · the floor"],
 ['Weighted central', 'Blend 35 / 25 / 20 / 20', f"SAR {L['central']['base']:.0f}", f"{(L['central']['base']/spot-1)*100:+.0f}% vs SAR {spot:.2f}"],
 ['TECHNICAL — what the tape is doing (timing, not value)', '', '', ''],
 ['Trend & momentum', 'Price vs the 20/50/100/200-day averages', 'Flat — within ±1% of all four', 'Range-bound'],
 ['Momentum / range', 'RSI · MACD · 52-week range', f"RSI {tech['rsi']:.0f} · MACD {tech['macd']['hist']:+.2f} · 40.2–45.4", 'Neutral, coiled'],
 ['MONTE CARLO — where price could go in 3 months (paths from spot)', '', '', ''],
 ['T+20 sessions', '50,000 paths · 16 factors', f"p5 {q20['5']:.0f} · p50 {q20['50']:.1f} · p95 {q20['95']:.0f}", 'Median ≈ spot'],
 ['T+60 sessions', 'same engine, longer horizon', f"p5 {q60['5']:.0f} · p50 {q60['50']:.1f} · p95 {q60['95']:.0f}", 'Mild upside skew'],
 ['EXPERT PANEL — three independent methods (Appendix C)', '', '', ''],
 ['Expert 1 — cash returns / economic profit', 'ROIC vs WACC with fading excess returns', f"SAR {E['e1']['base']:.0f}", 'Most conservative'],
 ['Expert 2 — normalized earnings power', 'Mid-cycle EPS × multiple', f"SAR {E['e2']['base']:.0f}", 'The floor-setter'],
 ['Expert 3 — macro-policy scenario tree', 'Rate path & payout scenarios into a DDM', f"SAR {E['e3']['base']:.0f}", 'Closest to spot'],
 ['Panel range', 'Spread = the fade-vs-franchise question', f"SAR {min(E['e1']['base'],E['e2']['base'],E['e3']['base']):.0f}–{max(E['e1']['base'],E['e2']['base'],E['e3']['base']):.0f}", f"Centres ~SAR {sorted([E['e1']['base'],E['e2']['base'],E['e3']['base']])[1]:.0f}"],
]
table(rows, [2.15, 2.35, 1.45, 1.15], band_rows=[1, 7, 10, 13], first_col_bold=False, size=8.9)
rich([('Bottom line. ', dict(bold=True)),
      (f"Every fundamental lens lands between SAR {L['normalized']['base']:.0f} and {L['dcf']['base']:.0f} — a tight cluster "
       f"by house standards — and the weighted central of SAR {L['central']['base']:.0f} sits {(L['central']['base']/spot-1)*100:+.0f}% "
       "above spot. The expert panel is more cautious than the house lenses precisely where it should be: the cash-returns "
       "expert charges the company for the capital the network swallows and lands below spot, while the earnings and policy "
       "experts sit at or just above it. This is not a deep-value situation and it is not an expensive one: it is a "
       "zero-net-debt utility-grade franchise at ~14.7× trailing earnings and a 5.0% locked yield (9.6% counting last year's "
       "special), where the return comes from the dividend plus whatever the market eventually pays for the AI-infrastructure "
       "and fintech options. The three-month distribution centres at spot with a mild upside tilt — the tape has no opinion "
       "yet.", {})], size=9.8, space_after=8)

# ---------------- Company overview -------------------------------------------
H2('Company overview — stc at a glance')
rows = [
 ['Item', 'Value'],
 ['Listed entity', 'Saudi Telecom Company (stc Group), Tadawul: 7010'],
 ['What it is', 'The Kingdom’s incumbent telecom operator and MENA’s largest telecom by market value; consumer, enterprise and wholesale connectivity plus a digital-infrastructure and fintech portfolio'],
 ['Spot / date', 'SAR 43.58 · 7 Jul 2026 close'],
 ['Shares · market cap', '4,989.8 mn (5,000 mn issued − ~10.2 mn treasury) · ~SAR 217.5 bn (~US$58 bn)'],
 ['FY2025 revenue / EBITDA / net profit', 'SAR 77,819 mn (+2.5%) · SAR 24,469 mn (31.4% margin) · SAR 14,828 mn (+12.5% adjusted; reported −39.9% vs FY24’s TAWAL-gain year)'],
 ['Q1-2026 revenue / net profit', 'SAR 19,939 mn (+3.8%) · SAR 3,696 mn (+12.0% ex non-recurring; +1.3% reported)'],
 ['Segment split (FY2025)', 'stc KSA SAR 51,119 mn (consumer 32,826 · enterprise 13,514 · wholesale 4,779) · subsidiaries net ~SAR 26,700 mn'],
 ['Balance sheet', 'Net debt SAR 111 mn at FY25 (~0.0× EBITDA); SAR 7.1 bn at Q1-26 after the Jan-2026 $2 bn sukuk (~0.3×); cash framings: FS 21.4 bn incl. stc bank / IR core 15.4 bn'],
 ['Dividend', 'SAR 0.55/quarter locked through Q3-2027 (SAR 2.20/yr ≈ 5.0% yield); FY24 also paid a SAR 2.00 special (cash paid 2025: SAR 4.20/sh ≈ 9.6%)'],
 ['Key stakes', '43.06% Digital Infrastructure Co (TAWAL + Zain towers; PIF 54%) · 9.97% Telefónica (€2.1 bn cost; ≈€1.96 bn market) · solutions by stc 79% (mkt cap ~SAR 26 bn) · stc bank 85% (8 mn customers)'],
 ['52-week range', 'SAR 40.20 (1 Mar 2026) – 45.38 (30 Oct 2025)'],
 ['Ownership', 'PIF 62.0% (after the Nov-2024 SAR 3.86 bn accelerated bookbuild) · free float ~38%'],
 ['Corporate events', '$2 bn dual-tranche sukuk (Jan-2026, 4.489%/5.083%) · 26 mn-share ESIP buyback approved 7 May 2026 · center3–HUMAIN AI-data-centre framework (Dec-2025, toward 1 GW) · SilkLink Syria fibre corridor (SAR 3 bn, Feb-2026) · 2Q26 results due ~late Jul 2026'],
]
table(rows, [1.7, 5.4], first_col_bold=True)
caption('Source: stc FY2023–FY2025 IR releases, Q1-2026 release and interim FS, FY2025 earnings presentation (all stc.com); '
        'Saudi Exchange disclosures; PIF press releases. Values rounded.')

# ================= §1 Fundamental ===========================================
H1('1  Fundamental valuation')
P('We value stc as a going-concern operator and triangulate four lenses. The primary lens is a free-cash-flow-to-firm DCF, '
  'because a mature, capital-intensive network operator is ultimately worth the cash its infrastructure produces after the '
  'capex that keeps it competitive; the tower and Telefónica stakes sit outside the operating engine and are marked '
  'separately on the bridge. A dividend-discount read is the natural cross-check for a company whose board has locked a '
  'SAR 0.55-per-quarter distribution through 2027. A relative EV/EBITDA read and a normalized-earnings read complete the '
  'set. The weights and the football field are in §1.5; the segment engine in §1.6; the crux — dividend cover against the '
  'capex cycle, in real units — in §1.7; the cost-of-capital build (every input sourced, both ERP bases published) in §1.8; '
  'and the sensitivity grids in §1.9. One lens-selection note (§3.5-F5 considered and set aside): stc does own a captive-finance-flavoured arm — stc bank — but at SAR 2.0 bn of revenue (2.5% of group) and an early-stage loan book it does not yet warrant the split-legs operating-co-plus-lender treatment; it is carried inside the subsidiaries line with a justified N/A, to be revisited once SAMA-reported bank financials give it a book worth marking separately. Throughout, the cost of equity is published explicitly as Ke = rf + β × ERP = '
  '5.50% + 0.48 × 5.01% = 7.90% (rating basis; 8.25% on the CDS basis), with the beta a genuine — if short-window — '
  'regression against TASI rather than an assumed round number.')

H2('1.1  The FCFF DCF — the primary lens')
P('The revenue engine is the §1.6 segment build (top-down: stc discloses unit revenue, not subscriber × ARPU detail, so '
  'per the house data-discipline gate we forecast disclosed segment lines rather than manufacture a bottom-up split). '
  'Group revenue compounds ~3.0% — consumer +2.0–3.0%, enterprise recovering to ~4% as mega-project phasing normalizes, '
  'wholesale mid-single-digit on hosting and FWA backhaul, subsidiaries ~5–6% led by solutions, stc bank and center3. The '
  'EBITDA margin glides from 31.4% (FY25) to 32.5% by FY30E — Q1-26 already printed 32.9% — as the subsidiary mix matures. '
  'Capex intensity follows management’s own band: 16.5% of revenue in FY26–27E (the “edge up slightly” guidance for the '
  'mission-critical and data-centre build), fading to 15.0% by FY30E; the long-term guided range is 15–17.5%. A working-'
  'capital/OCF-conversion drag of 0.4–0.8% of revenue reflects the receivables-heavy government business. Zakat and income '
  'tax at the normalized effective ~9.7% (statutory zakat is 2.5% of the zakat base; FY25’s net credit was a one-off).', size=10.5)
rows = [['SAR mn', 'FY26E', 'FY27E', 'FY28E', 'FY29E', 'FY30E']]
labels = [('rev', 'Group revenue'), ('ebitda', 'EBITDA'), ('dna', 'D&A'), ('ebit', 'EBIT'),
          ('nopat', 'NOPAT = EBIT × (1 − 9.7%)'), ('dna', '+ D&A'), ('capex', '− Capex'),
          ('dwc', '− Δ working capital'), ('fcff', 'FCFF'), ('df', 'Discount factor'), ('pv', 'PV of FCFF')]
for k, lbl in labels:
    row = [lbl]
    for rrow in dcf['rows']:
        v = rrow[k]
        if k == 'df': row.append(f"{v:.3f}")
        elif k in ('capex', 'dwc'): row.append(f"({v:,.0f})")
        elif k == 'dna' and lbl == 'D&A': row.append(f"({v:,.0f})")
        else: row.append(f"{v:,.0f}")
    rows.append(row)
table(rows, [2.1, 1.0, 1.0, 1.0, 1.0, 1.0], first_col_bold=True, size=8.9)
rows = [
 ['DCF bridge', 'SAR mn'],
 ['Σ PV of explicit FCFF (FY26–30E)', f"{dcf['pv_sum']:,.0f}"],
 ['Terminal value (Gordon, g = 2.5%)', f"{dcf['tv']:,.0f}"],
 ['PV of terminal value', f"{dcf['pv_tv']:,.0f}"],
 ['Enterprise value — core operations', f"{dcf['ev']:,.0f}"],
 ['Terminal value as % of EV (device A-7)', f"{dcf['tv_pct']*100:.0f}%"],
 ['+ Associates & JVs (43.06% DIIC/TAWAL, carrying)', f"{dcf['assoc']:,.0f}"],
 ['+ Telefónica 9.97% (market mark)', f"{dcf['telefonica']:,.0f}"],
 ['less: Net debt (IR basis, Q1-26) · NCI', f"({dcf['net_debt']:,.0f}) · ({dcf['nci']:,.0f})"],
 ['Equity value', f"{dcf['eq']:,.0f}"],
 ['DCF fair value per share', f"SAR {dcf['ps']:.2f}"],
]
table(rows, [4.0, 1.6], first_col_bold=True)
P(f"Two honesty notes. First, {dcf['tv_pct']*100:.0f}% of the enterprise value sits in the terminal — at a 5.1-point "
  "WACC−g spread this is a duration bet dressed as a five-year model, which is why §1.9 sensitizes the WACC × g grid and "
  "the beta separately rather than hiding either. Second, the model FCFF (SAR 10.3 bn FY26E) runs ~SAR 2–3 bn richer than "
  "stc's own reported FY25 free cash flow (6.5 bn), because reported OCF absorbs receivables swings, early-retirement cash "
  "and zakat timing that a NOPAT-based FCFF smooths; Q1-26's FCF of 3.9 bn (+494% YoY) suggests the gap is closing, but "
  "Appendix A shows both series so the difference is visible, not blended away (device A-8).")

H2('1.2  Dividend discount — the policy lens, as the cash-flow cross-check')
P('stc is one of the few large emerging-market payers whose dividend is a stated, board-locked policy rather than a ratio: '
  'SAR 0.55 per quarter from the Q4-2024 distribution through the Q3-2027 distribution (announced 25 Aug 2024), with '
  'specials assessed quarterly on top — FY24 shareholders also received SAR 2.00. We discount the locked SAR 2.20 through '
  '2027, step the DPS with earnings thereafter (payout ~75–80%), and grow the terminal dividend at 3.0%.', size=10.5)
rows = [['DDM build', 'FY26E', 'FY27E', 'FY28E', 'FY29E', 'FY30E'],
        ['DPS (SAR)'] + [f"{d:.2f}" for d in ddm['dps']],
        ['PV of DPS @ Ke 7.90%'] + [f"{ddm['dps'][i]/(1+ddm['ke'])**(i+1):.2f}" for i in range(5)]]
table(rows, [2.1, 1.0, 1.0, 1.0, 1.0, 1.0], first_col_bold=True, size=9.0)
rows = [
 ['Σ PV of explicit dividends (FY26–30E)', f"SAR {ddm['pv_div']:.2f}"],
 ['Terminal DPS (FY31E) = FY30E × 1.03', f"SAR {ddm['dps'][-1]*1.03:.2f}"],
 ['Terminal value = TDPS / (Ke − g)', f"SAR {ddm['tv']:.2f}"],
 ['PV of terminal value', f"SAR {ddm['pv_tv']:.2f}"],
 ['DDM fair value per share', f"SAR {ddm['ps']:.2f}"],
 ['Terminal value as % of value (device A-7)', f"{ddm['tv_pct']*100:.0f}%"],
]
table(rows, [4.0, 1.6], first_col_bold=True, header=False)
rich([(f"DDM base ≈ SAR {ddm['ps']:.0f}/share", dict(bold=True)),
      (' — a touch above spot: at a 7.9% cost of equity a locked 5.0% yield growing at ~3% is worth slightly more than the '
       'market pays, and any repeat of a special distribution (the quarterly-assessment clause) is free upside to this lens. '
       'The cross-check earns its place for a subtler reason: it is the one lens that cannot be flattered by the capex '
       'assumptions, because the board has pre-committed the cash.', {})])

H2('1.3  Relative multiples')
P('On trailing numbers stc trades at ~14.7× earnings, ~9.5× EV/EBITDA and 2.5× book — the premium name in a GCC cohort '
  'spanning 10.7× (Ooredoo) to 17.6× (du) on earnings. The premium tracks the franchise: ~57% mobile share, the only '
  'national fixed/fibre footprint, net debt ≈ zero against regional peers at 1–2× EBITDA, and the highest absolute yield '
  'commitment. The disciplined relative read is a justified EV/EBITDA on the FY26E build, bridged to equity with the same '
  'stake marks as the DCF.', size=10.5)
rows = [
 ['Relative basis', 'Bear', 'Base', 'Bull'],
 ['FY26E EBITDA (SAR mn)', '25,746', '25,746', '25,746'],
 ['Justified EV/EBITDA', '8.0×', '9.0×', '10.0×'],
 ['Fair value (SAR/share)', f"{L['relative']['bear']:.1f}", f"{L['relative']['base']:.1f}", f"{L['relative']['bull']:.1f}"],
 ['P/E cross-check at base (on FY26E EPS 2.82)', '', f"{L['relative']['base']/2.82:.1f}×', ''".replace(chr(39)+', '+chr(39)+chr(39), ''), ''],
]
rows[4] = ['P/E cross-check at base (on FY26E EPS 2.82)', '', f"{L['relative']['base']/2.82:.1f}×", '']
table(rows, [2.6, 1.3, 1.3, 1.3], first_col_bold=True)
rich([(f"Relative base ≈ SAR {L['relative']['base']:.0f}", dict(bold=True)),
      (' — in line with the DCF, which is itself informative: the market’s multiple for this franchise already embeds '
       'roughly the same view of its cash engine as our explicit model.', {})])

H2('1.4  Normalized earnings power — where this sits in the cycle')
P('Cycle position first (device A-6): unlike a developer or a smelter, stc’s P&L has no violent cycle, but FY25 profit is '
  'still not a clean base — it carries a one-off SAR 466 mn zakat credit (prior-year provision reversals), and FY24 before '
  'it carried the SAR 12.9 bn TAWAL disposal gain, a SAR 1.5 bn withholding-tax reversal and a SAR 2.6 bn early-retirement '
  'charge. Margins sit mid-cycle: EBITDA margin 31.4% is on the guided path (Q1-26: 32.9%), enterprise revenue is at the '
  'soft point of the government mega-project phasing, and the subsidiary portfolio (stc bank, center3) is still in its '
  'investment phase — 2–3 subsidiaries are guided to turn contribution-positive from 2026. Normalized attributable profit '
  'is therefore ~SAR 14.4 bn (reported FY25 14.8 bn less the zakat credit), or EPS ≈ 2.89, capitalized at a through-cycle '
  '15× — the stock’s own multi-year median area and the peer-set mid.', size=10.5)
rows = [
 ['Normalized-earnings basis', 'Bear', 'Base', 'Bull'],
 ['Normalized PAT (SAR mn)', '13,600', '14,400', '15,200'],
 ['Justified P/E', '13.5×', '15.0×', '16.5×'],
 ['Fair value (SAR/share)', f"{L['normalized']['bear']:.1f}", f"{L['normalized']['base']:.1f}", f"{L['normalized']['bull']:.1f}"],
]
table(rows, [2.6, 1.3, 1.3, 1.3], first_col_bold=True)
rich([(f"Normalized base ≈ SAR {L['normalized']['base']:.0f}", dict(bold=True)),
      (' — the floor of the set: it pays nothing for growth beyond today’s earnings power and treats the AI-infrastructure '
       'build purely as cost.', {})])

H2('1.5  Synthesis — four lenses')
P('We weight the DCF most heavily because it is the only lens that prices the full capex-and-recovery arc; the DDM carries '
  'the pre-committed cash; the relative lens anchors to what the market pays for GCC telecom cash flows today; normalized '
  'earnings is the ballast.')
rows = [['Lens', 'Weight', 'Bear', 'Base', 'Bull'],
 ['FCFF DCF (primary)', '35%', f"{L['dcf']['bear']:.0f}", f"{L['dcf']['base']:.1f}", f"{L['dcf']['bull']:.0f}"],
 ['Dividend discount (policy)', '25%', f"{L['ddm']['bear']:.0f}", f"{L['ddm']['base']:.1f}", f"{L['ddm']['bull']:.0f}"],
 ['Relative (EV/EBITDA)', '20%', f"{L['relative']['bear']:.0f}", f"{L['relative']['base']:.1f}", f"{L['relative']['bull']:.0f}"],
 ['Normalized earnings', '20%', f"{L['normalized']['bear']:.0f}", f"{L['normalized']['base']:.1f}", f"{L['normalized']['bull']:.0f}"],
 ['Weighted central', '', f"{L['central']['bear']:.1f}", f"{L['central']['base']:.1f}", f"{L['central']['bull']:.1f}"],
]
table(rows, [2.4, 0.9, 1.1, 1.1, 1.1], first_col_bold=True, band_rows=[5])
figure('fig1_football.png', 6.3, 'Figure 1 — Valuation football field. Bars span bear–bull per lens; the brass tick is each '
       'base case; the gold band is the blended central range; the ink line is spot.')
rich([(f"Central fair value ≈ SAR {L['central']['base']:.0f}/share", dict(bold=True)),
      (f", {(L['central']['base']/spot-1)*100:+.0f}% versus spot. The bear–bull span ({L['central']['bear']:.0f}–"
       f"{L['central']['bull']:.0f}) is driven almost entirely by the DCF’s terminal arithmetic — the bear case is "
       "WACC +100 bp with margins 50 bp lighter and capex 100 bp heavier; the bull is the mirror image. Note what the "
       "spread is NOT about: revenue. A ±1 pp change to every growth rate moves the central by only ~SAR 2 — this is a "
       "margin, capex and discount-rate story, which is exactly what §1.7 and §1.9 sensitize.", {})])

H2('1.6  The segments — a deeper look, and the driver table')
rows = [
 ['Segment / leg', 'FY25 revenue', 'Trend', 'Margin role', 'Swing role'],
 ['KSA Consumer (CBU)', 'SAR 32.8 bn (+3.4%)', 'Mobility +2.8%, fixed +6.6%; 30.6 mn subs (+5.3% Q1-26)', 'The cash cow', 'Competition watch'],
 ['KSA Enterprise (EBU)', 'SAR 13.5 bn (+0.4%)', 'Government phasing; private sector +6%; flat ex-mega-projects', 'High-margin', 'Recovery lever'],
 ['KSA Wholesale & Carrier', 'SAR 4.8 bn (+10.8%)', 'Hosting, FWA backhaul, national roaming (+32.6% national)', 'Structural', 'Steady'],
 ['Subsidiaries (net)', '~SAR 26.7 bn', 'solutions 12.7 bn · channels ~14.1 bn gross · stc bank 2.0 bn (+11%) · SCCC +62% · sirar +13% · center3', 'Dilutive today, guided to turn', 'The option book'],
 ['Associates & stakes', 'off-P&L', '43.06% towers (DIIC) · 9.97% Telefónica · iot squared 50%', 'Equity-method / marks', 'Bridge items'],
]
table(rows, [1.55, 1.35, 2.35, 1.15, 0.95], first_col_bold=True, size=8.6)
P('The top-down driver build (§3.5-C — the gate is deliberately NOT cleared for a bottom-up subscriber × ARPU model: stc '
  'discloses unit revenue and subscriber counts but not ARPU by tier, so a manufactured split would be false precision — '
  'the ETEL precedent in the house protocol). The sourced segment history comes first; the forward path is the house view:', size=9.8)
fc = D['forecast']
rows = [['Driver (disclosed history)', 'FY24', 'FY25', 'FY26E', 'FY28E', 'FY30E'],
 ['KSA Consumer (SAR mn)', '31,741', '32,826', f"{fc['FY26E']['cbu']:,.0f}", f"{fc['FY28E']['cbu']:,.0f}", f"{fc['FY30E']['cbu']:,.0f}"],
 ['KSA Enterprise', '13,466', '13,514', f"{fc['FY26E']['ebu']:,.0f}", f"{fc['FY28E']['ebu']:,.0f}", f"{fc['FY30E']['ebu']:,.0f}"],
 ['KSA Wholesale & Carrier', '4,313', '4,779', f"{fc['FY26E']['wc']:,.0f}", f"{fc['FY28E']['wc']:,.0f}", f"{fc['FY30E']['wc']:,.0f}"],
 ['Subsidiaries, net', '26,249', '26,700', f"{fc['FY26E']['sub']:,.0f}", f"{fc['FY28E']['sub']:,.0f}", f"{fc['FY30E']['sub']:,.0f}"],
 ['Group revenue', '75,893', '77,819', f"{fc['FY26E']['rev']:,.0f}", f"{fc['FY28E']['rev']:,.0f}", f"{fc['FY30E']['rev']:,.0f}"],
 ['EBITDA margin', '31.5%', '31.4%', '31.8%', '32.2%', '32.5%'],
 ['Capex intensity', '15.7%', '15.2%', '16.5%', '16.0%', '15.0%'],
]
table(rows, [2.2, 0.95, 0.95, 1.0, 1.0, 1.0], first_col_bold=True, size=8.9)
caption('History: stc FY2025 earnings presentation and IR releases (stc.com), restated basis. Forecast drivers are the house’s '
        'own flagged view (Fundamental Driver Ledger rows logged). Q1-26 actuals: CBU +5.2%, EBU −3.6%, W&C +6.2%.')

H2('1.7  The crux — dividend cover against the capex cycle, in real units')
P('Three judgments drive this valuation, and all three are observable rather than abstract. First and largest: capex '
  'intensity against the locked dividend. The policy dividend costs SAR 10.98 bn a year (2.20 × 4,989.8 mn shares); '
  'management guides capex to 15–17.5% of revenue with 2026–27 “edging up.” The cover table below is the whole tension in '
  'one place — at the top of the guided band the dividend is only 0.86× covered by model FY26E free cash flow and the '
  'balance sheet funds the rest; at the bottom it is fully covered. Each percentage point of capex intensity is worth '
  '≈SAR 0.8 bn of annual FCF and ≈SAR 1.6 of DCF fair value per share. Second: the discount rate. This is a 90%-equity-'
  'weighted WACC built on a 0.48 regressed beta from a nine-week window (§1.8) — at β = 1.0 the DCF falls from ~50 to ~34, '
  'below spot, so §1.9 publishes the full beta grid rather than letting one regression settle it. Third: the SAMA/Fed '
  'path — the rf is 5.5% today; each 50 bp off the Saudi curve adds ≈SAR 4–5 to the DCF and directly lowers the funding '
  'cost of the AI-infrastructure build. A fourth, slower variable: KSA mobile competition (Mobily’s subscriber growth has '
  'outpaced stc’s revenue growth for four quarters) — each 1 pp off consumer growth costs ≈SAR 2 of fair value.', size=10.5)
rows = [['FY26E scenario (real units)', 'Model FCF (SAR bn)', 'Dividend bill (SAR bn)', 'Cover']]
for c in cov:
    rows.append([f"Capex at {c['capex']}", f"{c['fcf']:.1f}", f"{c['div']:.1f}", f"{c['cover']:.2f}×"])
table(rows, [2.6, 1.5, 1.5, 0.9], first_col_bold=True)
caption('Device A-2: the DPS schedule and its stress test live in Appendix A.3. The dividend is policy-locked through the '
        'Q3-2027 distribution; the test is whether FCF or the balance sheet pays for it — at Q1-26 run-rate (FCF 3.9 bn vs '
        'a 2.74 bn quarterly dividend) it was FCF, for the first quarter in a year.')

H2('1.8  Macro and country — SAMA, oil, Vision 2030, and the sourced cost of capital')
P('stc is a defensive claim on the Saudi macro, in three channels. Rates: SAMA shadows the Fed to defend the riyal peg '
  '(repo 4.25% / reverse repo 3.75% since 10 Dec 2025; the Fed held 3.50–3.75% on 17 Jun 2026), so the discount rate and '
  'the sukuk funding cost are set in Washington as much as Riyadh. Oil and the fiscal impulse: government ICT and '
  'giga-project spend (SAR ~32 bn of digital-government spend in 2025) drives the enterprise book — the FY25 softness was '
  'phasing, not demand. Vision 2030: the structural bid — data centres (the center3–HUMAIN 1 GW ambition inside a national '
  'AI push), 5G/fibre densification, and digital-services adjacencies — is what turns a utility growth profile into a '
  'utility-plus-options profile. Because the riyal is pegged, there is no currency-translation channel in the valuation '
  'and no FX factor in the Monte Carlo. Every input in the cost-of-capital build is sourced and named (house rule §3.5-G):', size=10.5)
wb = dcf['wacc_build']
rows = [
 ['Cost-of-capital build', 'Value', 'Source'],
 ['Risk-free rate (rf)', '5.50%', 'Derived SAR 10Y: KSA govt-guaranteed USD 10Y priced UST+95bp on 8-Jul-2026 (SRC $1.5bn sukuk; UST 4.45%) = 5.40%, plus the SAR-over-USD pickup per the Saudi Exchange sovereign-debt primer (21-May-2026); FAB’s 5.5% as cross-check. Flagged: derived — no free live SAR 10Y screen exists'],
 ['Equity beta (β)', '0.48', 'Genuine daily stc-vs-TASI regression, n=40 sessions (5-May→7-Jul-2026): β 0.475, R² 14.3%, SE 0.19 — passes the house usability gate; flagged short-window, beta grid in §1.9'],
 ['Equity risk premium (rating-based, primary)', '5.01%', 'Damodaran ORIGINAL file (ctryprem.html), Saudi Arabia row, “Last updated: January 5, 2026”: Aa3, CRP 0.78% + mature 4.23%'],
 ['  — ERP, CDS-based (the “more current” alternative)', '5.72%', 'Same file, CDS column (sovereign CDS 0.98%) — for Saudi the CDS basis is the HIGHER one'],
 ['Cost of equity Ke = rf + β × ERP', '7.90%', '(rating basis; 8.25% on the CDS basis)'],
 ['Pre-tax cost of debt', '5.00%', 'stc’s own instruments: Jan-26 $2bn sukuk 4.489%/5.083% (T+75/T+90); 2019 sukuk 3.89%; SAR murabaha ≈ SAIBOR 4.79% + 60–100bp'],
 ['After-tax cost of debt (9.7% effective zakat/tax)', '4.51%', 'Debt mix: USD-linked ≈55–60% (named sukuk/ECA), SAR remainder — peg makes USD legs quasi-SAR'],
 ['Weights (E / D)', '90.6% / 9.4%', 'Market cap (43.58 × 4,989.8 mn) vs Q1-26 disclosed total debt SAR 22,475 mn'],
 ['WACC', '7.59%', '(7.90% on the CDS-based ERP — both published per protocol)'],
 ['Terminal growth (nominal SAR)', '2.50%', 'House view ≈ long-run nominal GDP-lite for a mature operator; sensitized in §1.9'],
]
table(rows, [2.3, 1.0, 3.6], first_col_bold=True, size=8.4)
P('Two honesty notes on this build. First, the risk-free rate is a derived figure: Saudi Arabia has no freely quoted '
  'live SAR 10-year screen, so we triangulated from a government-guaranteed USD sukuk priced the day before the study '
  '(UST + 95 bp) plus the officially documented SAR-over-USD sovereign pickup — the number is checkable end-to-end, but '
  'it is an estimate of a quote, not a quote. Second, the beta is regressed on only nine weeks of daily data, because '
  'every programmatic source of longer TASI history is access-blocked; 0.48 is consistent with a defensive, '
  'PIF-anchored mega-cap (aggregators print ~0.2 on longer windows), but the honest treatment is the grid in §1.9, where '
  'the reader can see the valuation at any beta up to 1.2. Both flags are logged in the study’s driver ledger.', size=9.6)

H2('1.9  Sensitivity — the margin, the capex, the rate spread, and the beta')
P('The first grid re-prices the DCF across the two real-unit operating levers (EBITDA margin and capex intensity); the '
  'second across WACC × terminal growth; the third across the beta — the single input most likely to move the answer, '
  'given the short regression window.')
figure('fig2_sens.png', 5.6, 'Figure 2 — DCF fair value (SAR/share) across EBITDA-margin and capex-intensity shifts. '
       'Bold cells sit nearest spot (SAR 43.58).')
S = D['sens']
wg_rows = [['WACC \\ terminal g', '1.5%', '2.0%', '2.5%', '3.0%', '3.5%']]
for i, w in enumerate(S['wacc_steps']):
    row = [f'{w*100:.2f}%' + (' (base)' if abs(w - dcf['wacc']) < 1e-9 else '')]
    for j in range(5):
        v = S['table_wg'][i][j]
        row.append('n.m.' if v is None else f'{v:.1f}')
    wg_rows.append(row)
table(wg_rows, [1.5, 1.0, 1.0, 1.0, 1.0, 1.0], first_col_bold=True, size=9.0)
caption(f"DCF fair value (SAR/share) across WACC × terminal growth. Base cell {dcf['wacc']*100:.2f}% × 2.5% = {dcf['ps']:.1f}. "
        'The CDS-ERP alternative WACC (7.90%) sits between the third and fourth rows.')
rows = [['Beta', 'Ke (rating ERP)', 'WACC', 'DCF value/sh', 'Note'],
 ['0.30', '7.00%', '7.05%', '59.8', ''],
 ['0.48', '7.90%', '7.59%', f"{dcf['ps']:.1f}", 'regressed base (n=40, R² 14%)'],
 ['0.70', '9.01%', '8.59%', '41.8', ''],
 ['0.85', '9.76%', '9.27%', '37.6', ''],
 ['1.00', '10.51%', '9.95%', '34.2', 'house fallback had the regression failed'],
 ['1.20', '11.51%', '10.86%', '30.4', ''],
]
table(rows, [1.0, 1.4, 1.1, 1.3, 2.4], first_col_bold=True, size=8.9)
caption('The beta grid is mandatory disclosure here (house rule): a nine-week regression passes the usability gate but is '
        'not a settled estimate. Even at β = 0.70 the DCF only converges to spot — the undervaluation read survives '
        'moderate beta doubt but not a full reversion to 1.0.')

# ================= §2 Technical ==============================================
H1('2  Technical and price structure')
P('The tape is flat in every sense that matters. stc trades within ±1% of all four major moving averages (the stack itself '
  'is compressed into a SAR 0.7 band — 43.25 to 43.93), RSI sits at 48, and the MACD histogram is fractionally negative '
  'with both lines hugging zero. The 52-week range is narrow for an emerging-market name — 40.20 (1 Mar 2026) to 45.38 '
  '(30 Oct 2025), barely ±6% around spot — and realized volatility (13% over the trailing year) is among the lowest on '
  'Tadawul. Price action over the last quarter: +4%, in a series of small steps around the Q1 print and the May dividend. '
  'This is a coiled, catalyst-waiting chart, not a trending one.')
rows = [
 ['Indicator', 'Reading', 'Signal'],
 ['Spot', 'SAR 43.58', '—'],
 ['SMA 20 / 50', f"SAR {tech['sma']['20']:.2f} / {tech['sma']['50']:.2f}", 'Spot within ±1% of both — no trend'],
 ['SMA 100 / 200', f"SAR {tech['sma']['100']:.2f} / {tech['sma']['200']:.2f}", 'Stack compressed — long base'],
 ['RSI (14)', f"{tech['rsi']:.1f}", 'Dead neutral'],
 ['MACD (12,26,9)', f"{tech['macd']['line']:+.2f} line / {tech['macd']['signal']:+.2f} signal / {tech['macd']['hist']:+.2f} hist", 'Flat, fractionally negative'],
 ['52-week range', 'SAR 40.20 – 45.38', 'Spot at the 63rd percentile'],
 ['20-day / 60-day change', f"{tech['chg20']*100:+.1f}% / {tech['chg60']*100:+.1f}%", 'Quiet accumulation'],
 ['Realized vol (252d)', f"{tech['rv252']*100:.1f}%", 'Very low; HAR forward read 15.1%'],
]
table(rows, [1.8, 2.6, 2.5], first_col_bold=True)
figure('fig3_ma.png', 6.4, 'Figure 3 — Price versus the moving-average stack, last 260 sessions.')
P('For the probabilistic work this matters in one way: a compressed, low-volatility tape produces a genuinely narrow '
  'three-month cone — the 5–95% band in §3 spans only ±12% — so even modest fundamental catalysts (a covered dividend, a '
  'capex surprise, a special) can move price to the edge of the distribution. The technical picture neither confirms nor '
  'contradicts the fundamental read; it simply has not voted yet.')
