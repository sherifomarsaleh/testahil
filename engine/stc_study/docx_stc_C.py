"""Content part C: Appendices A–D, About, Disclosure, footer."""
from docx_stc_base import *

L = D['lenses']; E = D['experts']; s0 = D['step0']; dcf = D['dcf']; ddm = D['ddm']
spot = D['spot']; hist = D['hist']; fc = D['forecast']

# ================= Appendix A ================================================
H1('Appendix A  Financial statements')
P('Consolidated figures as disclosed by stc — FY2023–FY2025 IR releases on the restated continuing-operations basis '
  '(TAWAL and Digital Infrastructure Co reclassified to discontinued operations), Q1-2026 release and interim FS — all '
  'from stc.com, per the study’s sourcing rule. SAR million. The five-year forecast is the model build (companion Excel, '
  'formula-linked to Assumptions).')
H2('A.1  Income statement — 3-year historical + 5-year forecast (consolidated, SAR mn)')
def f0(x): return f"{x:,.0f}"
IS_fc = {}
for y in ['FY26E','FY27E','FY28E','FY29E','FY30E']:
    r = fc[y]['rev']
    i = ['FY26E','FY27E','FY28E','FY29E','FY30E'].index(y)
    eb = D['drivers']['ebitda_m'][i]*r; dna = D['drivers']['dna_pct'][i]*r
    ebit = eb-dna
    oth = [700, 750, 800, 850, 900][i]
    pbt = ebit + oth
    zk = -pbt*0.097
    npc = pbt+zk
    att = npc*(1-0.025)
    IS_fc[y] = dict(rev=r, eb=eb, dna=dna, ebit=ebit, oth=oth, pbt=pbt, zk=zk, npc=npc, att=att)
rows = [
 ['Line', 'FY23', 'FY24', 'FY25', 'FY26E', 'FY27E', 'FY28E', 'FY29E', 'FY30E'],
 ['Revenue', '71,777', '75,893', '77,819'] + [f0(IS_fc[y]['rev']) for y in IS_fc],
 ['Gross profit', '34,740', '37,326', '37,700'] + [f0(IS_fc[y]['rev']*0.485) for y in IS_fc],
 ['EBITDA', '22,445', '23,951', '24,469'] + [f0(IS_fc[y]['eb']) for y in IS_fc],
 ['D&A & impairment', '(9,284)', '(9,525)', '(10,031)'] + [f"({f0(IS_fc[y]['dna'])})" for y in IS_fc],
 ['Operating profit (EBIT)', '13,161', '14,426', '14,438'] + [f0(IS_fc[y]['ebit']) for y in IS_fc],
 ['Associates, net finance, impairments & other', '826', '(2,292)', '285'] + [f0(IS_fc[y]['oth']) for y in IS_fc],
 ['Profit before zakat & income tax', '13,987', '12,134', '14,723'] + [f0(IS_fc[y]['pbt']) for y in IS_fc],
 ['Zakat & income tax', '(1,327)', '(1,192)', '466'] + [f"({f0(-IS_fc[y]['zk'])})" for y in IS_fc],
 ['Profit from continuing operations', '12,660', '10,942', '15,189'] + [f0(IS_fc[y]['npc']) for y in IS_fc],
 ['Discontinued operations', '759', '13,973', '—', '—', '—', '—', '—', '—'],
 ['Net profit (attributable)', '13,295', '24,689', '14,828'] + [f0(IS_fc[y]['att']) for y in IS_fc],
 ['EPS (SAR)', '2.67', '4.95', '2.97'] + [f"{IS_fc[y]['att']/4989.8:.2f}" for y in IS_fc],
]
table(rows, [2.05, 0.615, 0.615, 0.615, 0.615, 0.615, 0.615, 0.615, 0.615], first_col_bold=True, size=8.2)
caption('FY23–FY25 as disclosed (stc.com IR releases; restated). FY24 discontinued operations include the SAR 12,885 mn '
        'TAWAL/Digital-Infrastructure disposal gain. One-offs: FY23 AlKhobar land gain +1,296, WHT reversal +724; FY24 WHT '
        'reversal +1,500, ERP −2,577, BGSM impairment −764; FY25 zakat credit +466. Forecast columns are the live model '
        'build (rounded); the Excel is the source of truth.')
H2('A.2  Balance sheet — condensed house layout (consolidated, SAR mn)')
rows = [
 ['Line', 'FY23', 'FY24', 'FY25', 'FY26E', 'FY28E', 'FY30E'],
 ['Net fixed & intangible assets', '78,408', '74,383', '83,529', '86,529', '91,801', '95,232'],
 ['Investments in associates & JVs', '3,800*', '4,200*', '4,641', '5,141', '6,231', '7,441'],
 ['Financial assets (incl. Telefónica)', '22,000*', '23,500*', '24,893', '24,893', '24,893', '24,893'],
 ['Trade receivables, net', '24,500*', '25,800*', '26,727', '27,375', '28,486', '29,222'],
 ['Cash, equivalents & ST murabahas', '28,138', '30,755', '15,080', '21,774', '25,177', '31,116'],
 ['Other assets', '2,800', '2,000', '2,952', '2,952', '2,952', '2,952'],
 ['TOTAL ASSETS', '159,646', '160,638', '157,477', '168,664', '179,540', '190,856'],
 ['Equity attributable', '78,985', '89,417', '83,414', '86,525', '93,364', '101,411'],
 ['Non-controlling interests', '2,530*', '3,069*', '3,482', '3,834', '4,606', '5,455'],
 ['Borrowings & sukuk (excl. leases)', '21,958', '15,132', '15,191', '22,475', '22,475', '22,475'],
 ['Lease liabilities', '6,985*', '4,580*', '2,253', '2,253', '2,253', '2,253'],
 ['Trade payables & financial liabilities', '25,000*', '26,500*', '29,610', '29,610', '29,610', '29,610'],
 ['Zakat, provisions & other liabilities', '24,188', '21,940', '23,527', '23,967', '27,232', '29,652'],
 ['Balance check (assets − L&E)', '0', '0', '0', '0', '0', '0'],
]
table(rows, [2.5, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75], first_col_bold=True, size=8.4)
caption('Disclosed anchors (total assets, cash+murabaha, total debt, attributable equity) exactly as reported; * = grouped '
        'estimate tying to the disclosed totals; FY25 line detail from the Q1-2026 FS 31-Dec-25 comparatives. "Net fixed & '
        'intangible assets" and "Zakat, provisions & other" are the balancing lines, shown as formulas in the Excel so the '
        'check row is exact in every column. FY26E borrowings step up by the completed Jan-2026 $2 bn sukuk. Forecast values '
        'here are indicative reads of the live model.')
H2('A.3  Cash flow, the two FCF framings, and the DPS schedule (device A-2)')
rows = [
 ['Cash flow (SAR mn)', 'FY23', 'FY24', 'FY25', 'FY26E', 'FY28E', 'FY30E'],
 ['Operating cash flow (disclosed / model)', '22,418', '19,885', '18,283', '23,647', '26,155', '28,441'],
 ['Capex (disclosed / model)', '(9,790)', '(11,927)', '(11,795)', '(13,359)', '(14,000)', '(14,006)'],
 ['Free cash flow', '12,628', '7,959', '6,488', '10,287', '12,156', '14,435'],
 ['Dividends paid (attributable)', '(8,000)', '(18,712)', '(10,978)', '(10,978)', '(11,477)', '(12,724)'],
]
table(rows, [2.5, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75], first_col_bold=True, size=8.5)
caption('FY23–FY25 disclosed (stc IR); FY24 dividends-paid include the FY24 quarterly schedule; calendar-2025 cash dividends '
        '≈ SAR 20.9 bn including the SAR 2.00/share special. Model OCF is a NOPAT-based construct and runs richer than the '
        'disclosed series — the conversion gap (receivables, ERP cash, zakat timing) is modelled as an explicit drag and '
        'discussed in §1.1; both framings shown per house rule.')
rows = [
 ['Dividend schedule', 'FY25A', 'FY26E', 'FY27E', 'FY28E', 'FY29E', 'FY30E'],
 ['DPS declared (SAR)', '2.20', '2.20', '2.20', '2.30', '2.40', '2.55'],
 ['Dividend bill (SAR bn)', '11.0', '11.0', '11.0', '11.5', '12.0', '12.7'],
 ['Payout of attributable NP', '74%', '78%', '75%', '75%', '74%', '74%'],
 ['Yield at spot (declared)', '5.0%', '5.0%', '5.0%', '5.3%', '5.5%', '5.9%'],
 ['Stress check', 'At the 17.5% top of the capex band, FY26E cover is 0.86× — the SAR 15.4 bn core cash pile funds the gap for >3 years before leverage exceeds 1× EBITDA; the policy is safe to Q3-2027 barring a margin break.', '', '', '', '', ''],
]
table(rows, [1.9, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85], first_col_bold=True, size=8.6)
caption('Two yield framings (house rule): declared-regular 2.20/sh = 5.0%; cash paid during calendar-2025 incl. the FY24 '
        'special = 4.20/sh = 9.6%. Forecast-vs-actual scorecard (device A-3) and new-vs-old reconciliation (A-4): not '
        'applicable on an initiation; both become standing sections from the first 3-month update.')

# ================= Appendix B ================================================
H1('Appendix B  Peer set, sector structure, and risks')
P('stc is the premium name in a three-player Saudi market inside a GCC cohort where telecom equity is increasingly a '
  'yield-plus-digital-infrastructure asset class.')
rows = [
 ['Name', 'P/E (t)', 'Div yield', 'One-line profile'],
 ['stc (7010)', '~14.7×', '5.0% (9.6% incl. special)', 'Incumbent; ~57% mobile share; net debt ~0; AI-DC and fintech options'],
 ['Mobily (7020)', '~13.5×', '4.5%', 'No.2; e& anchor (~28%); fastest subscriber momentum'],
 ['Zain KSA (7030)', '~12.8×', '4.9%', 'No.3; tower-light; balance-sheet repair done'],
 ['e& (UAE)', '~13.2×', '5.1%', 'UAE incumbent + Vodafone/PPF international portfolio'],
 ['Ooredoo (Qatar)', '~10.7×', '5.7%', 'Multi-market; MENA data-centre pivot'],
 ['du (UAE)', '~17.6×', '5.5%', 'No.2 UAE; hyperscale data-centre momentum — the multiple stc’s DC build aspires to'],
 ['Omantel / Beyon / Telecom Egypt', '11.5× / 11.1× / 8.8×', '3.9% / 7.1% / 1.5%', 'Regional context'],
]
table(rows, [1.55, 1.05, 1.35, 3.05], first_col_bold=True, size=8.7)
caption('Multiples approximate, mixed as-of dates (May–Jul 2026), secondary aggregators — context only, never model inputs.')
P('Sector structure. Saudi mobile is a disciplined three-player market (~57/27/16 stc/Mobily/Zain) under CST regulation, '
  'with spectrum freshly allocated (Nov-2024 auction: stc took 600 MHz + 3.8 GHz), 5G at 63% populated coverage for stc '
  'and FWA adoption among the highest globally — FWA is both an opportunity (4.1 mn of stc’s 6.0 mn fixed lines) and the '
  'competitive vector through which mobile capacity attacks fixed pricing. Fibre stays an stc moat (3.75 mn FTTH, 258k km). '
  'The Kingdom’s AI push (HUMAIN, sovereign compute, the center3 1 GW ambition) is turning telecom capex into a national-'
  'strategy line item. Principal risks: a mobile price war; capex overshoot on the AI build; government-receivables '
  'cycles; subsidiary execution (stc bank credit costs as it scales); the Telefónica mark; regional geopolitics; and the '
  'rate path staying higher for longer.')

# ================= Appendix C ================================================
H1('Appendix C  The expert valuation panel')
P('Every Testahil study closes with a panel of standing expert personas — drawn from the house Expert Persona Library, not '
  'invented for the occasion, so each accumulates a track record across studies and a quarterly update is a re-run, not a '
  're-training. For stc we cast the telecom trio from the library’s coverage map — cash-returns (DCF + returns on capital '
  'against WACC), earnings-power (normalized through-cycle earnings + multiples), and macro-policy (scenario-weighted '
  'policy options) — labelled Expert 1 / 2 / 3. Each runs a genuinely different method, derives its fair value from shown '
  'workings, and states a falsification condition.')

H2('C.1  Expert 1 — cash returns: ROIC against the cost of capital')
P('Worldview and tradition. A business is worth the cash it returns over its life, and it creates value only when each '
  'riyal of capital earns above its cost. He looks past accounting earnings to free cash flow and to the economic-profit '
  'spread — and he is temperamentally suspicious of capex programs described with the word “vision.”', size=9.8)
P('When it works / fails. Best for capital-intensive businesses where returns on capital are the crux — precisely a '
  'telecom. Fails where reinvestment economics are genuinely improving (past ROIC misleads a new-moat story) — his risk '
  'here if the AI-data-centre build earns structurally above telecom returns.', size=9.8)
rows = [
 ['Expert 1’s economic-profit test', 'Value'],
 ['Invested capital (equity 83.4 bn + net debt 7.1 bn)', 'SAR 90.5 bn'],
 ['FY26E NOPAT → ROIC', 'SAR 13.9 bn → 15.3%'],
 ['WACC (accepts the §1.8 build)', '7.59%'],
 ['Economic profit = (ROIC − WACC) × IC', 'SAR ~7.0 bn/yr'],
 ['Fade: excess returns decay 2.5%/yr toward WACC', 'EP multiple ≈ 13.2×'],
 ['Core EV = IC + PV(fading EP)', 'SAR ~183 bn'],
 ['+ stakes − net debt − NCI, / 4,989.8 mn shares', f"→ SAR {E['e1']['base']:.1f}/share"],
]
table(rows, [4.4, 1.7], first_col_bold=True, size=9.0)
P(f"Sensitivity (swing = the fade rate): at a 1%/yr fade (a durable moat) his value rises to ≈SAR {E['e1']['rng'][1]:.0f}; "
  f"at 4%/yr (competition and technology churn eat the spread) it falls to ≈SAR {E['e1']['rng'][0]:.0f}. Cross-examination: "
  "he tells Expert 2 that a 15× multiple on normalized earnings quietly capitalizes today’s ROIC forever without charging "
  "for the capital that sustains it — his fade does explicitly what the multiple hides. He tells Expert 3 that scenario "
  "trees on the policy rate are fine, but the bigger lever is inside the company: each percentage point of capex intensity "
  "is SAR 0.8 bn of cash that either earns the spread or doesn’t.", size=9.8)
rich([('Verdict, falsification, market-implied. ', dict(bold=True)),
      (f"Fair SAR {E['e1']['base']:.1f} (range {E['e1']['rng'][0]:.0f}–{E['e1']['rng'][1]:.0f}) — the panel’s conservative "
       "anchor, below spot: on his arithmetic the market already pays for the excess returns to persist a decade-plus. "
       "Falsified by disclosed data-centre economics showing contracted returns above telecom ROIC (the fade would then be "
       "too harsh), or by ROIC holding ≥15% through FY28 while capex normalizes. What the price implies: at SAR 43.58 the "
       "market discounts a fade of roughly 1.5%/yr — gentler than his 2.5%, i.e. the market believes in the moat slightly "
       "more than he does.", {})])

H2('C.2  Expert 2 — normalized earnings power')
P('Worldview and tradition. An operating company is worth a fair multiple of its sustainable, mid-cycle earnings power; '
  'peaks, troughs and one-off gains are noise to be stripped before anything is capitalized.', size=9.8)
P('When it works / fails. Best for stable operating businesses with a track record — a fit for stc, whose underlying '
  'earnings have grown 12–13% (adjusted) for two straight years. Fails at structural breaks: if the subsidiary portfolio '
  're-rates the growth profile, his through-cycle multiple is too low; if a price war breaks the margin, too high.', size=9.8)
rows = [
 ['Expert 2’s normalization', 'Value'],
 ['FY25 attributable profit, reported', 'SAR 14,828 mn'],
 ['less: one-off zakat credit', '(466)'],
 ['Normalized PAT → EPS', 'SAR ~14,400 mn → SAR 2.89'],
 ['Justified through-cycle P/E', '15.0×'],
 ['Fair value', f"→ SAR {E['e2']['base']:.1f}/share"],
]
table(rows, [4.4, 1.7], first_col_bold=True, size=9.0)
P('Sensitivity (swing = the multiple): at 13.5× SAR 36.8; at 16.5× SAR 50.3; each 1× of P/E ≈ SAR 2.9. Cross-examination: '
  'he tells Expert 1 that a fade model is just a multiple wearing a lab coat — the honest disagreement is the number, and '
  '15× for a zero-net-debt incumbent yielding 5% is not heroic when du trades at 17.6×. He tells Expert 3 that the '
  'dividend lens undervalues whatever the board chooses not to distribute — the same retained cash the specials keep '
  'proving exists.', size=9.8)
rich([('Verdict, falsification, market-implied. ', dict(bold=True)),
      (f"Fair SAR {E['e2']['base']:.1f} (range {E['e2']['rng'][0]:.0f}–{E['e2']['rng'][1]:.0f}) — a whisker below spot: on "
       "clean current earnings the stock is fully priced, and everything above 15× is paying for growth not yet printed. "
       "Falsified by two consecutive years of double-digit adjusted EPS growth (his base would be stale), or by the margin "
       "glide reversing. The market pays 15.1× his normalized EPS — it agrees with him almost exactly.", {})])

H2('C.3  Expert 3 — macro-policy: the scenario tree')
P('Worldview and tradition. In a policy-driven market, policy outranks fundamentals: the Fed/SAMA rate path, the oil-'
  'funded fiscal impulse, and sovereign strategic priorities (Vision 2030, the AI build, PIF’s portfolio choices) move '
  'this stock more than management execution does. He prices the equity as a probability-weighted set of policy worlds, '
  'expressed through the dividend stream — the one cash flow a policy-anchored shareholder actually receives.', size=9.8)
P('When it works / fails. Best where binary policy catalysts dominate — rate cuts, sovereign flows, national-champion '
  'capex mandates. Fails through false precision: the probabilities are judgments, and the tree can miss the branch that '
  'grows (his own flag: a KSA price war appears in nobody’s policy scenario, yet would dominate all of them).', size=9.8)
rows = [
 ['Scenario (through 2027)', 'Prob.', 'World', 'DDM value'],
 ['Easing + special dividends', '30%', 'Fed/SAMA cut 75–100 bp; cover proven; a special repeats', f"SAR {L['ddm']['bull']*1.02:.0f}"],
 ['Base: policy held, dividend locked', '45%', 'Gradual cuts; capex mid-band; SAR 2.20 through 2027 then +3%', f"SAR {ddm['ps']:.0f}"],
 ['Higher-for-longer + capex overrun', '25%', 'No cuts to mid-2027; capex at 17.5%; no specials', f"SAR {L['ddm']['bear']*0.96:.0f}"],
 ['Probability-weighted fair value', '', '', f"SAR {E['e3']['base']:.1f}"],
]
table(rows, [2.2, 0.7, 2.7, 1.1], first_col_bold=True, size=8.9, band_rows=[4])
P(f"Sensitivity (swing = the scenario weights): shifting 10 points from base to bear moves him ≈SAR 1.5; his answer is "
  "more stable than either colleague’s because the dividend floor does most of the work in every branch. "
  "Cross-examination: he tells Expert 1 that a fade rate is unknowable to the decimal while the policy calendar is "
  "published — model what is scheduled. He tells Expert 2 that a through-cycle multiple assumes a cycle; Saudi rates are "
  "pegged to a foreign central bank, so the local 'cycle' is imported and can stay dislocated from local fundamentals for "
  "years.", size=9.8)
rich([('Verdict, falsification, market-implied. ', dict(bold=True)),
      (f"Fair SAR {E['e3']['base']:.1f} — essentially the DDM with eyes open, and the panel value closest to spot. "
       "Falsified by the board breaking the policy (either direction: a cut dividend or a step-change up), or by a Fed "
       "path outside his tree (no cuts through 2027, or emergency easing). What the price implies: the market is pricing "
       "roughly his base case with a small weight on the bear — i.e. the locked dividend at a ~5% yield, and near-zero "
       "credit for specials or the AI build.", {})])

H2('C.5  The three in one room')
P('Put the three in a room and the argument is about one thing: what happens to stc’s return on capital as the Kingdom’s '
  'AI-infrastructure build runs through its income statement.', size=9.8)
P('Expert 1: “Fifteen percent returns on ninety billion of capital, fading as every telecom’s returns have always faded. '
  'The data centres are capex with a press release until someone shows me contracted economics. I pay SAR 37.”', size=9.8)
P('Expert 3: “Your fade rate is a guess dressed as physics. What is not a guess: the board has signed a cheque for SAR 2.20 '
  'a year through 2027, SAMA’s next moves are the Fed’s, and the sovereign has made this company its digital-infrastructure '
  'champion. Price the policy, not the physics — SAR 46.”', size=9.8)
P('Expert 2: “You are both reaching. Clean earnings are SAR 2.89 a share, growing high single digits; the market pays 15× '
  'for that across the Gulf. Everything else — fades, scenario trees, gigawatts — is a story about the sixteenth multiple '
  'point. SAR 43, and the market agrees with me to the decimal.”', size=9.8)

H2('C.6  Reading the divergence')
figure('figD1_experts.png', 6.0, 'Figure C-1 — The three experts’ fair-value ranges. Brass ticks are base cases; the gold '
       'band is the panel centre; the ink line is spot. The spread is the return-fade question.')
rows = [
 ['Expert', 'Method', 'Single swing assumption', 'Base fair value'],
 ['Expert 1', 'Cash returns / economic profit', 'The fade rate on excess returns (2.5%/yr)', f"SAR {E['e1']['base']:.1f}"],
 ['Expert 2', 'Normalized earnings power', 'The through-cycle multiple (15×)', f"SAR {E['e2']['base']:.1f}"],
 ['Expert 3', 'Macro-policy scenario tree', 'The scenario weights on the rate/payout path', f"SAR {E['e3']['base']:.1f}"],
]
table(rows, [1.0, 2.2, 2.5, 1.3], first_col_bold=True, size=9.0)
P(f"The spread — SAR {min(E['e1']['base'],E['e2']['base'],E['e3']['base']):.0f} to "
  f"{max(E['e1']['base'],E['e2']['base'],E['e3']['base']):.0f}, about 23% of the low — is narrow by this series’ standards, "
  "and it measures one thing cleanly: how much of stc’s current 15% return on capital survives the next decade of "
  "competition, technology churn and nation-scale capex. Expert 1 charges for the erosion explicitly and lands below spot; "
  "Expert 2 freezes today’s clean earnings at a market multiple and lands at spot; Expert 3 prices the policy floor and "
  "lands above it. The house lenses (§1.5) sit above the panel because the DCF credits the margin glide and capex fade the "
  "experts decline to pre-pay for — that gap, ~SAR 4, is the price of believing management’s own guidance. An investor’s "
  "position on this stock reduces to a position on that one axis: if the AI-infrastructure build earns telecom-plus "
  "returns, the house DCF is right and the stock is cheap; if it earns telecom-minus, Expert 1 is right and today’s price "
  "already flatters it.")
caption('Each expert’s point fair value (and bull/base/bear where applicable) is logged with the study date (9 Jul 2026) and '
        'spot (SAR 43.58) as an internal per-expert track record, kept separate from the core Calibration Ledger.')

# ================= About / Disclaimer / footer ================================
H1('About this series')
P('Testahil publishes independent, educational valuation studies. Each is an attempt to reason transparently about what a '
  'security is worth, with every assumption shown and a companion model so readers can disagree productively. The house '
  'style is distributions, not tips: we describe ranges and probabilities, not targets, and we do not tell anyone what to '
  'do. Studies are framed as educational analysis, the preparer is not licensed by any securities regulator, and holdings '
  'are disclosed.')
H1('Disclosure & Disclaimer')
for head, body in [
 ('Not investment advice. ', 'This document is educational and informational only. It is not, and must not be relied upon '
  'as, investment, financial, legal, accounting or tax advice, nor an offer, solicitation or recommendation to buy, sell or '
  'hold any security. It contains no price target and no rating.'),
 ('No licence; no advisory relationship. ', 'The preparer is not registered or licensed with any securities or financial '
  'regulator in any jurisdiction — including the Saudi Capital Market Authority (CMA) — holds no brokerage or investment-'
  'advisory authorisation, and is not acting as your adviser or fiduciary. Nothing here is personalised to your '
  'circumstances.'),
 ('Holdings disclosure. ', 'The preparer may hold, and may in the future take or dispose of, a position in the security '
  'discussed in this report, and may transact at any time without notice. This is a potential conflict of interest you '
  'should weigh.'),
 ('Sources & accuracy. ', 'Reported financial and operating figures are drawn from the company’s public disclosure '
  '(stc.com IR releases and interim financial statements) and other public sources believed reliable but not independently '
  'verified; they may contain errors or be superseded. Forward-looking inputs — the segment growth and margin paths, capex '
  'intensity, the derived risk-free rate and regressed beta, terminal growth, the multiples, the stake marks and the '
  'Monte-Carlo factor probabilities — are the preparer’s own judgments and are inherently uncertain. Some balance-sheet '
  'detail lines are grouped estimates tying to disclosed totals.'),
 ('Forward-looking statements. ', 'Any statements about the future are estimates subject to risks and uncertainties; actual '
  'results may differ materially. The Monte Carlo models price, not value, and encodes subjective probabilities for events '
  'that have not occurred.'),
 ('No reliance; your responsibility. ', 'Do your own research and consult a licensed professional before making any '
  'decision. You are solely responsible for your investment decisions and their outcomes. To the maximum extent permitted '
  'by law, the preparer accepts no liability for any loss arising from use of this document.'),
 ('Currency & figures. ', 'Figures are in Saudi riyals (SAR), millions unless stated; bn denotes billion. The riyal is '
  'pegged to the US dollar at 3.75. Rounding may cause totals to differ slightly. Spot price and market data are as of '
  '7 July 2026 and change continuously.'),
]:
    rich([(head, dict(bold=True, italic=True)), (body, {})], size=9.6, space_after=5)
P('TESTAHIL · Independent Valuation Study · Educational Analysis · Saudi Telecom Company (Tadawul: 7010) · '
  'edition 09-07-2026 · reporting currency SAR', size=8.8, color=GREY, align='center', space_before=10)

doc.save('STC_Valuation_Study_09-07-2026_public.docx')
print('docx saved')
