"""Content part A: masthead → §2."""
from docx_base import *

pr = D['mc']['prob_read']; q20, q60 = D['mc']['q20'], D['mc']['q60']
L = D['lenses']; tech = D['tech']; dcf = D['dcf']; sotp = D['sotp']
spot = D['spot']

# ---------------- Masthead / title / anchor --------------------------------
masthead()
P('Independent Valuation Study — Educational Analysis', size=12, bold=True, space_before=4, space_after=2)
P('GB Corp S.A.E. (EGX: GBCO)', size=17, bold=True, space_after=2)
P('Fundamental analysis · Technical analysis · Monte Carlo simulation — one integrated read',
  size=10.5, italic=True, color=GREY, space_after=8)
rich([('Anchor: ', dict(bold=True)),
      ('EGP 31.25 (7 Jul 2026 close) · 1,085.5 mn shares · mkt cap ~EGP 33.9 bn · the continuing listed entity of the former '
       'GB Auto (Ghabbour), renamed GB Corp in 2023, housing ', {}),
      ('GB Auto', dict(bold=True)),
      (' (passenger cars, commercial vehicles & construction equipment, tires & trading, light mobility; Egypt · Iraq · Jordan), ', {}),
      ('GB Capital', dict(bold=True)),
      (' (leasing, factoring, consumer finance, SME lending) and associate stakes led by ', {}),
      ('MNT-Halan', dict(bold=True)),
      (' · prices and probabilities computed 7 Jul 2026 from the attached daily history · primary lens: split-the-legs sum-of-the-parts '
       '(operating company + captive lender, §3.5-F5) · the MNT-Halan stake percentage is now the dominant swing factor, ahead of Auto cash conversion and the Egyptian nominal-rate path.', {})],
     size=9.8, space_after=10)

# ---------------- READ FIRST box --------------------------------------------
box([
 ('READ FIRST — what this document is, and is not.', ''),
 ('', 'This study is a valuation exercise and an expression of personal analytical opinion, published free of charge for '
      'educational purposes: it shows how one analyst applies fundamental, technical and probabilistic methods to a listed '
      'company, and invites scrutiny of that methodology. It is NOT investment advice, NOT a recommendation or solicitation '
      'to buy, sell or hold any security, and NOT directed at the circumstances of any reader. The preparer is not licensed '
      'by any securities regulator in any jurisdiction, holds no Egyptian (FRA) or other brokerage or advisory authorisation, '
      'provides no financial consultancy, manages no money, and accepts no fees, funds or clients. See the Disclosure & '
      'Disclaimer at the end.'),
 ('', 'All values are model outputs presented as ranges and distributions because no single number should be relied on. '
      'Reported financials are the company\u2019s own disclosure (FY23–FY25 earnings releases; 1Q26 release, 14 May 2026); '
      'forward-looking inputs — the marks on GB Capital and the MNT-Halan stake, the complexity discount, the multiples, the '
      'DCF and the Monte-Carlo factor probabilities — are the preparer\u2019s judgments and are flagged throughout. A note on '
      'identity: GB Corp S.A.E. is the renamed GB Auto S.A.E. (Ghabbour Auto); the EGX ticker is GBCO (price history continues '
      'the former AUTO listing). Consult a licensed financial advisor before any investment decision.'),
])

# ---------------- Headline ---------------------------------------------------
H2('Headline')
rich([("The model's read: meaningfully undervalued on a now-confirmed number — and that number raises a real puzzle the "
       "market hasn't obviously resolved. ", dict(bold=True)),
      (f"At EGP 31.25 the shares sit about {abs(L['central']['base']/spot-1)*100:.0f}% below our weighted central estimate of "
       f"EGP {L['central']['base']:.1f}. The four lenses spread wider than usual: the split-the-legs sum-of-the-parts lands at "
       f"{L['sotp']['base']:.1f} after a 10% complexity discount (pre-discount {sotp['prediscount_ps']:.1f}), a conservative "
       f"relative read at {L['relative']['base']:.1f} marks the floor, and a normalized mid-cycle read at "
       f"{L['normalized']['base']:.1f} sits in between. One update belongs up front: GB Corp's own 9-June-2026 press release "
       "on MNT-Halan's Al Ahly Capital-led round states the resulting stake directly — 41.61% (down from 42.58% "
       "pre-transaction) — a current, dated, company-confirmed figure, not an estimate. Applying 41.61% to the round's USD "
       f"1.4bn valuation values the stake alone at \u2248EGP {sotp['mnt_halan_value']/1000:.1f}bn — {sotp['mnt_halan_value']*0.9/(spot*1085.5)*100:.0f}% "
       "of GB Corp's entire spot market cap. That is now a confirmed fact, not a sourcing gap, and it is genuinely strange: "
       "it implies the market prices almost nothing into a real, profitable, EGP 66bn-revenue auto business, which points "
       "to one of two things — either the market applies a far steeper discount to this private mark than this study's 10% "
       "complexity haircut (illiquidity, minority-stake, execution-risk on the second closing), or GB Corp is genuinely "
       "mispriced. This study cannot settle which; §7 returns to it. The stake is now the largest single input in the "
       "model — every 5 percentage points is worth \u2248EGP 3.3/share — ahead of the Auto-leg cash-conversion question that "
       "would otherwise be the crux (FY25 revenue grew 49% but working capital swallowed EGP 8.1bn and Auto net debt rose "
       "to EGP 15.2bn; the DCF still depends on working-capital intensity gliding from 28.5% of revenue back toward its "
       "FY23\u201324 range and on the pace of Egyptian nominal-rate cuts). "
       "Technically the stock is the mirror image of a cheap chart: above all four moving averages, RSI in the low-60s, five "
       "months into a new all-time-high zone. Over three months the Monte Carlo — whose secular drift is the configuration "
       "that passed the Step 0 calibration gate — places the 5th\u201395th percentile band at roughly EGP "
       f"{q60['5']:.0f}\u2013{q60['95']:.0f} with a median near {q60['50']:.0f}; that engine is completely unaffected by the "
       "stake correction, since it prices the stock's own path, not the SOTP.", {})], space_after=8)

# ---------------- Valuation summary table -----------------------------------
H2('Valuation summary — every read at a glance')
P('One table for the four reads that follow — what the business is worth (fundamental), what the tape is doing (technical), '
  'where price could travel over three months (Monte Carlo), and how three independent expert methods land. Every row is '
  'developed in the sections and appendices below.', size=9.8)
E = D['experts']
rows = [
 ['Lens / read', 'What it measures', 'Output', 'Takeaway'],
 ['FUNDAMENTAL — what the business is worth (the anchor)', '', '', ''],
 ['Split-legs SOTP (primary)', 'Auto DCF + lender book + associate marks, less discount', f"EGP {L['sotp']['base']:.1f}", f"{(L['sotp']['base']/spot-1)*100:+.0f}% vs spot"],
 ['Pre-discount NAV', 'The same legs, no complexity discount', f"EGP {sotp['prediscount_ps']:.1f}", f"{(sotp['prediscount_ps']/spot-1)*100:+.0f}%"],
 ['Relative multiples', 'FY26E EPS × justified P/E', f"EGP {L['relative']['base']:.1f}", f"{(L['relative']['base']/spot-1)*100:+.0f}% · the floor"],
 ['Normalized earnings', 'Mid-cycle PAT × through-cycle P/E', f"EGP {L['normalized']['base']:.1f}", f"{(L['normalized']['base']/spot-1)*100:+.0f}%"],
 ['Weighted central', 'Blend 40 / 15 / 20 / 25', f"EGP {L['central']['base']:.1f}", f"{(L['central']['base']/spot-1)*100:+.0f}% vs EGP {spot:.2f}"],
 ['TECHNICAL — what the tape is doing (timing, not value)', '', '', ''],
 ['Trend & momentum', 'Price vs the 20/50/100/200-day averages', 'Above all four', 'Strong uptrend'],
 ['Momentum / range', 'RSI · MACD · 52-week range', f"RSI {tech['rsi']:.0f} · MACD +{tech['macd']['hist']:.2f} · 19.1–33.4", 'Extended, not euphoric'],
 ['MONTE CARLO — where price could go in 3 months (paths from spot)', '', '', ''],
 ['T+20 sessions', '50,000 paths · 16 factors', f"p5 {q20['5']:.0f} · p50 {q20['50']:.1f} · p95 {q20['95']:.0f}", 'Median above spot'],
 ['T+60 sessions', 'same engine, longer horizon', f"p5 {q60['5']:.0f} · p50 {q60['50']:.0f} · p95 {q60['95']:.0f}", 'Wide, right-skewed'],
 ['EXPERT PANEL — three independent methods (Appendix D)', '', '', ''],
 ['Expert 1 — split-legs NAV', 'Marks each leg; fair discount', f"EGP {E['e1']['base']:.1f}", 'The anchor'],
 ['Expert 1 — split-legs NAV', 'Marks each leg; fair discount', f"EGP {E['e1']['base']:.1f}", 'Most bullish'],
 ['Expert 2 — normalized earnings power', 'Mid-cycle PAT × multiple', f"EGP {E['e2']['base']:.1f}", 'Most conservative'],
 ['Expert 3 — cash returns (ROCE vs WACC)', 'Economic profit on capital employed', f"EGP {E['e3']['base']:.1f}", '—'],
 ['Panel range', 'Spread = the MNT-Halan stake question', f"EGP {min(E['e1']['base'],E['e2']['base'],E['e3']['base']):.1f}–{max(E['e1']['base'],E['e2']['base'],E['e3']['base']):.1f}", f"Centres ~EGP {sorted([E['e1']['base'],E['e2']['base'],E['e3']['base']])[1]:.0f}"],
]
table(rows, [2.15, 2.35, 1.45, 1.15], band_rows=[1, 7, 10, 13], first_col_bold=False, size=8.9)
rich([('Bottom line. ', dict(bold=True)),
      (f"The reads spread wider than usual, and every disagreement now traces to the same open question: not what GB "
       f"Corp's MNT-Halan stake is (confirmed: 41.61%, 9-Jun-2026), but what that stake is actually worth and why the "
       f"market doesn't price it at face value. The fundamental central sits near EGP {L['central']['base']:.0f} — "
       f"{abs(L['central']['base']/spot-1)*100:.0f}% below the EGP {spot:.2f} spot — the three experts span "
       f"{min(E['e1']['base'],E['e2']['base'],E['e3']['base']):.0f}\u2013{max(E['e1']['base'],E['e2']['base'],E['e3']['base']):.0f}, "
       "and the tape (unusually) sits closer to spot than the fundamental work — either the market is applying a much "
       "steeper discount to the private MNT-Halan mark than this study's 10%, or it doesn't fully trust the round's "
       "valuation, or GB Corp really is mispriced. The three-month Monte Carlo distribution is unaffected either way: it "
       "prices the stock's own historical path, and its median sits above spot only because the engine's secular drift "
       "survived the calibration gate; Appendix B shows exactly how thin that margin is.", {})], size=9.8, space_after=8)

# ---------------- Company overview -------------------------------------------
H2('Company overview — GB Corp at a glance')
rows = [
 ['Item', 'Value'],
 ['Listed entity', 'GB Corp S.A.E. (EGX: GBCO; formerly GB Auto / Ghabbour Auto, AUTO)'],
 ['What it owns', 'GB Auto (PC assembly & distribution, CV&CE, tires & trading, light mobility) · GB Capital (Drive Finance, GB Lease & Factoring, rentals, Kredit) · associates: MNT-Halan, Bedaya, Kaf'],
 ['Spot / date', 'EGP 31.25 · 7 Jul 2026 close'],
 ['Shares · market cap', '1,085.5 mn · ~EGP 33.9 bn'],
 ['FY25 revenue / net profit', 'EGP 80,229.8 mn (+48.7% YoY) · EGP 2,880.0 mn (3.6% margin)'],
 ['1Q26 revenue / net profit', 'EGP 21,570.8 mn (+28.7%) · EGP 435.8 mn (−30.4%, regional drag + finance cost)'],
 ['Segment split (FY25, pre-elim.)', 'GB Auto EGP 66.4 bn (83%) · GB Capital EGP 14.7 bn (17%); Capital = ~47% of segment net profit'],
 ['Auto net debt / group equity', 'EGP 15.2 bn (2.39× Auto EBITDA; 2.14× at 1Q26) · attributable equity EGP 28.8 bn (BVPS 26.5)'],
 ['52-week range', 'EGP 19.10 – 33.40 (all-time high 3 Feb 2026)'],
 ['Ownership · leadership', 'Ghabbour family ~63.4% · free float ~36.6% · Group CEO Nader Ghabbour'],
 ['Corporate events', 'MNT-Halan first-close capital increase at USD 1.4 bn valuation (Jun 2026) · Sadat CKD facility inaugurated Jun 2026 · 2Q26 results due 11 Aug 2026'],
]
table(rows, [1.7, 5.4], first_col_bold=True)
caption('Source: company 4Q23/4Q24/4Q25 and 1Q26 earnings releases, EGX data, MNT-Halan transaction press release (Jun 2026). Values rounded.')

# ================= §1 Fundamental ===========================================
H1('1  Fundamental valuation')
P('We value GB Corp as an operating company with a captive finance arm and split the legs (§3.5-F5): blending an auto '
  'assembler-distributor, a leveraged lender and an unlisted fintech associate into one multiple would blur three different '
  'economics. The primary lens is therefore a split-legs sum-of-the-parts: the Auto operating leg on a free-cash-flow DCF; '
  'GB Capital on its adjusted operating book times a return-justified multiple; the MNT-Halan-led associate stakes at '
  'GB Corp\u2019s own last-confirmed disclosed ownership, cross-checked against the June-2026 funding round. A '
  'relative-multiple read and a normalized mid-cycle read complete the set. The weights and the football field are in §1.5; '
  'the dominant swing factor is now the MNT-Halan stake itself (box below §1.1), ahead of Auto cash conversion — dissected '
  'in §1.7 — and the sensitivity grids in §1.9.')

H2('1.1  Split-the-legs sum-of-the-parts — the primary lens')
P('Each leg is marked on the basis that fits it. The Auto leg takes the §1.2 DCF value; GB Capital is marked on the '
  'company\u2019s own adjusted-ROAE equity base (the disclosure that strips the MNT-Halan revaluation out of the equity '
  'denominator: NP EGP 1,366 mn / 15.1% adjusted ROAE \u21d2 ~EGP 9.5 bn of operating book) at 1.0\u00d7 \u2014 the return-justified '
  'multiple for a mid-teens-ROE lender whose margin is a beneficiary of the easing cycle; and the associates are marked by '
  'applying GB Corp\u2019s own current, confirmed stake to the June-2026 funding round (USD 1.4 bn \u00d7 41.61% \u00d7 EGP/USD '
  '\u2248 47.5 \u21d2 \u2248EGP 27.7 bn). UPDATE (09-07-2026): an earlier draft of this study used an unsourced ~20% stake '
  'estimate, later corrected to 42.58% (GB Corp\u2019s last-disclosed figure at the time, from a 28-Jul-2024 press release). '
  'GB Corp has since confirmed the current figure directly: its 9-June-2026 press release on MNT-Halan\u2019s Al Ahly '
  'Capital-led capital increase states "GB Corp\u2019s ownership stake in MNT-Halan will be adjusted to 41.61%, compared to '
  '42.58% prior to the transaction" \u2014 a dated, current, company-confirmed number, now used as the base case without a '
  'staleness caveat. Within the associates line, MNT-Halan is the overwhelming majority of the value (\u224899%), with '
  'Bedaya and Kaf the \u2248EGP 0.4 bn residual. From the sum we deduct a 10% complexity discount for the wrapper: an auto '
  'operator, an NBFI and an unlisted fintech in one listing will not trade at the clean sum of its parts.')
rows = [
 ['Leg (base case)', 'Basis', 'Value (EGP mn)'],
 ['GB Auto operating leg', f"FCFF DCF (\u00a71.2): EV {dcf['ev']:,.0f} \u2212 net debt 15,210 \u2212 NCI 800", f"{sotp['auto_eq']:,.0f}"],
 ['GB Capital lending leg', 'Adjusted operating book 9,500 \u00d7 1.0\u00d7', f"{sotp['cap_val']:,.0f}"],
 ['Associate \u2014 MNT-Halan (41.61%, confirmed 9-Jun-2026)', 'USD 1.4 bn Jun-26 round \u00d7 41.61% stake \u00d7 47.5 EGP/USD', f"{sotp['mnt_halan_value']:,.0f}"],
 ['Other associates (Bedaya, Kaf)', 'Residual carrying value', f"{sotp['other_assoc']:,.0f}"],
 ['\u03a3 Equity value (pre-discount)', f"= EGP {sotp['prediscount_ps']:.1f} / share", f"{sotp['total']:,.0f}"],
 ['less: complexity / conglomerate discount', '10%', f"({sotp['total']*sotp['disc']:,.0f})"],
 ['SOTP equity value', f"= EGP {sotp['ps']:.1f} / share", f"{sotp['eq']:,.0f}"],
]
table(rows, [2.5, 3.1, 1.5], first_col_bold=True)
rich([(f"SOTP base \u2248 EGP {sotp['ps']:.1f}/share", dict(bold=True)),
      (f", with a wide bear\u2013bull span of {sotp['bear']:.0f}\u2013{sotp['bull']:.0f} \u2014 driven mainly by the discount applied to "
       f"the MNT-Halan mark and the Auto margin/working-capital path (\u00a71.9). The market-implied read is now a confirmed "
       f"puzzle rather than a sourcing question: market cap less the lender and the associates at the confirmed 41.61% "
       "stake implies a deeply negative value for the Auto leg \u2014 impossible for a profitable, EGP 66bn-revenue business. "
       "Since the stake itself is no longer in question, the honest reads are that the market applies a much steeper "
       "discount to this private mark than this study\u2019s 10%, doesn\u2019t fully trust the USD 1.4bn valuation\u2019s "
       "read-through to GB Corp\u2019s economic interest, or GB Corp is genuinely mispriced. \u00a77 discusses which is most "
       "plausible.", {})])

H2('What the MNT-Halan stake is worth inside this valuation \u2014 now a confirmed number, and a real puzzle')
P('Because this single line dominates the whole valuation, here is its exact footprint, using GB Corp\u2019s own '
  '9-June-2026 confirmed figure:', size=9.8, space_after=4)
rows = [
 ['MNT-Halan in the GBCO valuation', 'Value'],
 ['Confirmed value at the June-2026 round (41.61% stake)', f"USD 1.4 bn \u00d7 41.61% \u00d7 47.5 = EGP {sotp['mnt_halan_value']:,.0f} mn"],
 ['Per share, pre-discount', f"EGP {sotp['mnt_halan_value']/1085.5:.2f} \u2014 {sotp['mnt_halan_value']/sotp['total']*100:.0f}% of the EGP {sotp['prediscount_ps']:.1f} pre-discount NAV"],
 ['Per share, after the 10% discount', f"EGP {sotp['mnt_halan_value']*0.9/1085.5:.2f} \u2014 same {sotp['mnt_halan_value']/sotp['total']*100:.0f}% share of the EGP {sotp['ps']:.1f} SOTP"],
 ['As a share of the market price (EGP 31.25)', f"\u2248{sotp['mnt_halan_value']*0.9/(31.25*1085.5)*100:.0f}% \u2014 confirmed, and the puzzle (see below)"],
 ['Every 5 percentage points of stake (for context)', "\u2248EGP 3.3/share of SOTP fair value \u2014 no longer the open question it was"],
]
table(rows, [2.7, 4.4], first_col_bold=True, size=9.0)
H2('The market-cap puzzle \u2014 what a confirmed 41.61% stake actually implies')
P('With the stake now confirmed rather than estimated, the residual uncertainty shifts entirely to the mark and the '
  'discount, not the ownership percentage. The table below shows how sensitive the SOTP would have been to the stake '
  'question that is now closed, followed by what actually needs explaining:', size=9.8)
rows = [['GB stake in MNT-Halan', 'MNT-Halan value (EGP mn)', 'SOTP fair value/sh', 'Note']]
stakes_notes = [
 (0.20, 'prior placeholder \u2014 wrong, superseded'),
 (0.25, ''),
 (0.30, ''),
 (0.3545, ''),
 (0.40, ''),
 (0.4258, 'the interim correction \u2014 pre-transaction figure, now superseded'),
 (0.4161, 'CONFIRMED current (GB Corp PR, 9-Jun-2026) \u2014 base case'),
]
for st, note in stakes_notes:
    val = st * 1400.0 * 47.5
    ps = (val + sotp['auto_eq'] + sotp['cap_val'] + sotp['other_assoc']) * 0.9 / 1085.5
    rows.append([f"{st*100:.2f}%", f"{val:,.0f}", f"{ps:.1f}", note])
table(rows, [1.5, 1.7, 1.3, 2.6], first_col_bold=True, size=8.8)
rich([('In plain terms: ', dict(bold=True)),
      ("the stake question this study originally flagged as its biggest uncertainty is now closed \u2014 GB Corp confirmed "
       "41.61% in writing on 9 June 2026. What remains open is not \u201cwhat does GB Corp own\u201d but \u201cwhat is that "
       "ownership worth, and why doesn\u2019t the market price it at face value.\u201d A confirmed 41.61% stake in a company "
       f"marked at USD 1.4bn is worth more than {sotp['mnt_halan_value']*0.9/(31.25*1085.5)*100:.0f}% of GB Corp\u2019s entire "
       "market cap \u2014 either the market is applying a steep private-mark discount this study\u2019s 10% doesn\u2019t capture, "
       "or GB Corp is genuinely mispriced. The bear case in this study\u2019s football field (\u00a71.5) reflects the former via "
       "a much heavier discount on the stake; the base case takes the confirmed number at the round\u2019s valuation. \u00a77 "
       "returns to this as the study\u2019s central open question.", {})], size=9.8)

H2('1.2  The Auto-leg DCF — the cash-flow engine of the SOTP')
P('The Auto leg is built bottom-up on disclosed units × ASP per line of business (the data-discipline gate is cleared: '
  'volumes and revenue are published per LoB, so ASP is arithmetic, not guesswork — the driver table is in §1.6 and Appendix '
  'A). Gross margin glides from 13.8% (FY26E, absorbing the regional drag visible in 1Q26\u2019s 12.4%) back to 14.5% — '
  'below FY24\u2019s FX-windfall 19.2% by design; GS&A holds ~7%; capex follows the EGP 3 bn 2026 guidance then normalizes; '
  'and the crux — net working capital — glides from 28.5% of revenue (FY25) to 21.5% by FY30E as the payables re-extension '
  'completes and the Sadat stock-build unwinds. WACC is built bottom-up from sourced inputs, not house defaults (§1.8 '
  'table): Ke = 22.55% rf + 1.0 β × 9.41% ERP = 31.96%, blended with after-tax debt to 22.94%; terminal growth 11.5% '
  'nominal EGP.')
rows = [['EGP mn', 'FY26E', 'FY27E', 'FY28E', 'FY29E', 'FY30E']]
labels = [('rev', 'Auto revenue'), ('ebitda', 'EBITDA'), ('dna', 'D&A'), ('ebit', 'EBIT'),
          ('nopat', 'NOPAT = EBIT × (1 − 28%)'), ('dna', '+ D&A'), ('capex', '− Capex'),
          ('dwc', '− Δ working capital'), ('fcff', 'FCFF'), ('df', 'Discount factor'), ('pv', 'PV of FCFF')]
for key, lbl in labels:
    row = [lbl]
    for rrow in dcf['rows']:
        v = rrow[key]
        if key == 'df': row.append(f"{v:.3f}")
        elif key in ('capex', 'dwc'): row.append(f"({v:,.0f})")
        elif key == 'dna' and lbl.startswith('D&A'): row.append(f"({v:,.0f})")
        else: row.append(f"{v:,.0f}")
    rows.append(row)
table(rows, [2.1, 1.0, 1.0, 1.0, 1.0, 1.0], first_col_bold=True, size=8.9)
rows = [
 ['DCF bridge', 'EGP mn'],
 ['Σ PV of explicit FCFF (FY26–30E)', f"{dcf['pv_sum']:,.0f}"],
 ['Terminal value (Gordon, g = 11.5%)', f"{dcf['tv']:,.0f}"],
 ['PV of terminal value', f"{dcf['pv_tv']:,.0f}"],
 ['Enterprise value — Auto leg', f"{dcf['ev']:,.0f}"],
 ['Terminal value as % of EV (device A-7)', f"{dcf['tv_pct']*100:.0f}%"],
 ['less: Auto net debt · Auto NCI', '(15,210) · (800)'],
 ['Auto equity value', f"{dcf['auto_eq']:,.0f}"],
]
table(rows, [4.0, 1.6], first_col_bold=True)
P(f"Two honesty notes. First, {dcf['tv_pct']*100:.0f}% of the EV sits in the terminal value — this is a growth-and-rates bet "
  "dressed as a five-year model, which is why §1.9 sensitizes the WACC × terminal-g grid rather than hiding it. Second, the "
  "explicit-period FCFF is thin (EGP 0.2 bn in FY26E) precisely because growth consumes working capital; the value is in the "
  "steady state, not the ramp. Both are disclosed rather than blended away (device A-8).")

H2('1.3  Relative multiples')
P('On FY25 earnings GB Corp trades at ~11.8× P/E and ~1.18× book. On the FY26E build (~EGP 3.3 bn attributable, EPS ~3.04) '
  'the forward P/E is ~10.3×. A justified multiple for the blend — an EM auto distributor (typically 8–12×) plus a mid-teens-'
  'ROE NBFI (6–10×) with an unlisted fintech kicker — sits around 8–11×. We mark the lens on the FY26E EPS.')
rows = [
 ['Relative basis', 'Bear', 'Base', 'Bull'],
 ['FY26E net profit (EGP mn)', '3,300', '3,300', '3,300'],
 ['Justified P/E', '8.0×', '9.5×', '11.0×'],
 ['Fair value (EGP/share)', f"{L['relative']['bear']:.1f}", f"{L['relative']['base']:.1f}", f"{L['relative']['bull']:.1f}"],
]
table(rows, [2.6, 1.3, 1.3, 1.3], first_col_bold=True)
rich([(f"Relative base ≈ EGP {L['relative']['base']:.1f}", dict(bold=True)),
      (' — the most conservative lens and probably where a sceptic anchors: it pays for this year\u2019s earnings and gives '
       'nothing for the working-capital release or the associate optionality.', {})])

H2('1.4  Normalized earnings power — where this sits in the cycle')
P('Cycle position first (device A-6): GB\u2019s FY25 passenger-car volume of 56.5k units is roughly double the 2023 trough '
  '(27.0k) but still well short of the company\u2019s mid-2010s run-rate, and the Egyptian market\u2019s 210k registrations '
  'in 2025 — +40% y/y — remain below the pre-2016-devaluation peak; the recovery is mid-cycle, not late-cycle. Margins are '
  'past their peak, though: FY24\u2019s 19.2% Auto gross margin carried an FX-scarcity windfall that is normalizing (14.8% '
  'FY25, 12.4% in 1Q26). Mid-cycle earnings power therefore blends recovering volumes with normalized margins: ~EGP 4.2 bn '
  'of group PAT (Auto ~2.2 bn at 14.5% GPM on FY27-scale revenue + Capital ~1.7 bn + associates), against FY25\u2019s '
  'reported 2.9 bn.')
rows = [
 ['Normalized-earnings basis', 'Bear', 'Base', 'Bull'],
 ['Mid-cycle PAT (EGP mn)', '3,600', '4,200', '4,800'],
 ['Justified P/E', '7.5×', '8.5×', '9.5×'],
 ['Fair value (EGP/share)', f"{L['normalized']['bear']:.1f}", f"{L['normalized']['base']:.1f}", f"{L['normalized']['bull']:.1f}"],
]
table(rows, [2.6, 1.3, 1.3, 1.3], first_col_bold=True)
rich([(f"Normalized base ≈ EGP {L['normalized']['base']:.1f}", dict(bold=True)),
      (' — the ceiling of the central case: in effect the bet that the volume recovery completes while margins hold the '
       'post-windfall floor.', {})])

H2('1.5  Synthesis — four lenses')
P('We weight the SOTP most heavily because it respects the differing economics of the legs; the pre-discount NAV carries the '
  'discount-narrowing case; the relative lens anchors the floor; normalized earnings carries the recovery thesis.')
rows = [['Lens', 'Weight', 'Bear', 'Base', 'Bull'],
 ['Split-legs SOTP', '40%', f"{L['sotp']['bear']:.0f}", f"{L['sotp']['base']:.1f}", f"{L['sotp']['bull']:.0f}"],
 ['Pre-discount NAV', '15%', f"{L['prediscount']['bear']:.0f}", f"{L['prediscount']['base']:.1f}", f"{L['prediscount']['bull']:.0f}"],
 ['Relative multiples', '20%', f"{L['relative']['bear']:.0f}", f"{L['relative']['base']:.1f}", f"{L['relative']['bull']:.0f}"],
 ['Normalized earnings', '25%', f"{L['normalized']['bear']:.0f}", f"{L['normalized']['base']:.1f}", f"{L['normalized']['bull']:.0f}"],
 ['Weighted central', '', f"{L['central']['bear']:.1f}", f"{L['central']['base']:.1f}", f"{L['central']['bull']:.1f}"],
]
table(rows, [2.4, 0.9, 1.1, 1.1, 1.1], first_col_bold=True, band_rows=[5])
figure('fig1_football.png', 6.3, 'Figure 1 — Valuation football field. Bars span bear–bull per lens; the brass tick is each '
       'base case; the gold band is the blended central range; the light line is spot.')
rich([(f"Central fair value ≈ EGP {L['central']['base']:.1f}/share", dict(bold=True)),
      (f", {abs(L['central']['base']/spot-1)*100:.0f}% below spot. Unlike a typical Testahil football field, the width here "
       f"is not really four independent views converging — the SOTP and pre-discount NAV lenses ({L['sotp']['base']:.1f} and "
       f"{sotp['prediscount_ps']:.1f}) both carry the same MNT-Halan stake assumption, so they move together with it, while "
       f"the relative ({L['relative']['base']:.1f}) and normalized ({L['normalized']['base']:.1f}) lenses don\u2019t touch "
       "the stake at all and sit much closer to spot. That split is itself informative: strip out the MNT-Halan question "
       "and this is a fairly-priced operator; include it at the last disclosed stake and it looks meaningfully cheap. Which "
       "is right depends entirely on a number this study cannot currently confirm to the decimal (§1.1 box).", {})])

H2('1.6  The legs — a deeper look, and the units × ASP driver table')
rows = [
 ['Leg', 'Cyclicality', 'Margin / return trend', 'Capital intensity', 'Swing role'],
 ['GB Auto — PC (80% of Auto rev)', 'High (rates, FX, imports)', 'GPM normalizing 14.8% → ~14%', 'Very high (working capital)', 'Dominant'],
 ['GB Auto — CV&CE, trading, mobility', 'Moderate', 'Bus exports scaling', 'Moderate', 'Diversifier'],
 ['GB Capital', 'Credit-cycle', 'Adj. ROAE 15.1%; NIM 5.0%; NPL 2.1–2.5%', 'Leverage 0.86× D/E', 'Compounder'],
 ['Associates (MNT-Halan et al.)', 'Venture-like', 'Revenue +50% (1Q26); loan book > USD 1.7 bn', 'Off balance sheet', 'Optionality'],
]
table(rows, [1.9, 1.2, 1.9, 1.35, 0.85], first_col_bold=True, size=8.7)
P('The bottom-up build (§3.5-B/C — gate cleared: every driver below is disclosed or arithmetic on disclosed figures):', size=9.8)
fc = D['forecast']
rows = [['Driver (disclosed)', 'FY23', 'FY24', 'FY25', 'FY26E', 'FY30E'],
 ['PC volume (units)', '26,994', '42,043', '56,548', f"{fc['FY26E']['pc_vol']:,.0f}", f"{fc['FY30E']['pc_vol']:,.0f}"],
 ['PC ASP (EGP mn/unit)', '0.61', '0.87', '0.93', f"{fc['FY26E']['pc_asp']:.2f}", f"{fc['FY30E']['pc_asp']:.2f}"],
 ['PC revenue (EGP mn)', '16,544', '36,533', '52,827', f"{fc['FY26E']['pc_rev']:,.0f}", f"{fc['FY30E']['pc_rev']:,.0f}"],
 ['CV&CE revenue', '2,323', '3,985', '5,957', f"{fc['FY26E']['cv_rev']:,.0f}", f"{fc['FY30E']['cv_rev']:,.0f}"],
 ['Light-Mobility revenue', '854', '1,378', '2,204', f"{fc['FY26E']['lm_rev']:,.0f}", f"{fc['FY30E']['lm_rev']:,.0f}"],
 ['Trading (tires + parts)', '2,507', '3,816', '4,243', f"{fc['FY26E']['tr_rev']:,.0f}", f"{fc['FY30E']['tr_rev']:,.0f}"],
 ['GB Auto total revenue', '23,854', '47,065', '66,358', f"{fc['FY26E']['auto_rev']:,.0f}", f"{fc['FY30E']['auto_rev']:,.0f}"],
]
table(rows, [2.2, 0.95, 0.95, 0.95, 1.0, 1.0], first_col_bold=True, size=8.9)
caption('FY25 PC mix: 31,349 CKD / 25,199 CBU; Egypt 80.5% of PC revenue, Iraq/Jordan 19.5%. Sources: 4Q23/4Q24/4Q25 releases, '
        'Tables 2–7. Forecast drivers are the house\u2019s own flagged view.')

H2('1.7  The crux: the MNT-Halan mark and discount, then cash conversion and the rate path')
P('Three judgments drive the valuation, in order of size. First and now by far the largest: not what GB Corp\u2019s '
  'MNT-Halan stake is — that is confirmed (41.61%, 9-Jun-2026 press release, §1.1 box) — but what a private mark this '
  'large should be discounted by, given that taking it at face value implies the stake alone is worth roughly three '
  'quarters of GB Corp\u2019s entire market cap. This study applies a 10% complexity discount uniformly across all three '
  'legs; a reader who believes the market is applying a much steeper illiquidity/minority discount specifically to the '
  'MNT-Halan mark should treat the SOTP bear case, not the base case, as the more realistic anchor. Second, where Auto '
  'working-capital intensity settles (the observable, disclosed unit: net Auto working capital as % of Auto revenue — '
  'device A-1). It ran '
  '18.7% in FY23, 22.9% in FY24 and 28.5% in FY25 as import-restriction payables normalized and inventory was pre-built for '
  'Sadat; we glide it to 21.5% by FY30E. Each percentage point of steady-state intensity is worth roughly EGP 4–5/share of '
  'SOTP value. Third, the Egyptian nominal-rate path: the 22.94% WACC against 11.5% terminal growth is an 11.4-pt real '
  'spread struck off a 22.55% sourced risk-free rate; every 100 bp the CBE easing cycle takes out of that spread adds '
  '~EGP 3/share (§1.9 '
  'grid). A fourth, binary-style exposure (§3.5-E device 6, applied cross-class): roughly a fifth of PC revenue is '
  'Iraq/Jordan, where the regional conflict cut 1Q26 volumes — a full-year regional freeze would take ~EGP 1.5–2 bn off '
  'Auto gross profit, worth ~EGP 2–3/share.')

H2('1.8  Macro and country — rates, the pound, imports and the region')
P('GB Corp is a leveraged play on Egyptian nominal normalization. The CBE has cut 825 bp since April 2025 and held its '
  'deposit rate at 19.00% through the April and May 2026 meetings with inflation ~14.6%; every cut lowers GB Capital\u2019s '
  'funding cost on a fixed-rate-lending book, lowers the Auto customer\u2019s instalment, and compresses the discount rate '
  'this study applies. The EGP (~47–48/USD, firmer y/y) sets CKD input costs and the EGP value of the MNT-Halan mark — a '
  'step-devaluation is the single nastiest macro scenario for both margin and multiple. Import policy and Chinese entrants '
  '(BYD\u2019s Egypt entry; grey imports into Iraq) set the competitive ceiling on ASPs; localization (Sadat, 46%+ local '
  'content on core CKD lines) is the structural answer. Every input in the cost-of-capital build below is sourced from a '
  'named, checkable source — not a house default (house rule §3.5-G, rebuilt 09-07-2026):', size=10.5)
rows = [
 ['Cost-of-capital build', 'Value', 'Source'],
 ['Risk-free rate (rf)', '22.55%', 'Egypt 10Y local govt bond yield, investing.com, 3-Jul-2026'],
 ['Equity beta (β)', '1.00', 'GBCO-vs-EGX30 regression attempted (n=5 annual: β=−0.15, R²=0.01, unusable); house default per protocol when no reliable regression obtainable'],
 ['Equity risk premium (ERP, CDS-based, primary)', '9.41%', "Damodaran's original country-risk file, Egypt row (ctryprem.html)"],
 ['  — ERP, rating-based (alternative, \u201cstandard practice\u201d)', '13.94%', 'Same source, rating-based column'],
 ['Cost of equity Ke = rf + β × ERP', '31.96%', '(CDS-based, primary; 36.49% on the rating-based alternative)'],
 ['Pre-tax cost of debt', '20.70%', 'CBE weighted-average EGP bank lending rate, <12mo tenor, Feb-2026'],
 ['After-tax cost of debt (28% tax)', '14.90%', 'Debt is ~100% EGP-denominated — 5 disclosed facilities checked, all EGP, no USD facility found'],
 ['Weights (E / D)', '47.1% / 52.9%', 'Market cap (spot × shares) vs. FY25 disclosed group borrowings'],
 ['WACC', '22.94%', '(25.08% on the rating-based ERP alternative — see §1.9)'],
 ['Terminal growth (nominal EGP)', '11.5%', 'House view, sensitized in the grid below'],
]
table(rows, [2.6, 1.3, 3.0], first_col_bold=True, size=8.7)
P('Two honesty notes on this build. First, GBCO\u2019s own beta could not be reliably estimated: five annual observations '
  'against the EGX30 produced a negative, statistically meaningless slope (R² ≈ 1%), so beta is set to 1.0 rather than '
  'borrowed from cross-country auto-sector peers, which would import Auto & Truck operating risk from markets with '
  'entirely different capital structures and macro regimes. Second, the equity risk premium was initially mis-sourced in '
  'an earlier draft (a secondary source\u2019s claimed 14.87% did not match Damodaran\u2019s own published 13.94%/9.41%) — '
  'corrected here after checking his original file directly, and logged in the house Fundamental Driver Ledger so the '
  'same mistake cannot recur silently on a future study.', size=9.6)

H2('1.9  Sensitivity — the margin, the discount, and the rate spread')
P('Holding the lender and associate marks (and the MNT-Halan stake, at the confirmed 41.61%) fixed, the first grid '
  're-prices the SOTP across the Auto gross-margin path and the complexity discount; the second across the WACC × '
  'terminal-growth spread — now built bottom-up rather than assumed (§1.8), so this grid is the honest range around a '
  'sourced base case, not around a house guess. The stake is no longer the open question — what matters now is the '
  'discount applied to its mark, sensitized in the §1.1 box, since it dominates both of these grids combined.')
figure('fig2_sens.png', 5.6, 'Figure 2 — SOTP fair value (EGP/share) across the Auto GPM shift and the complexity discount. '
       'Bold cells sit nearest spot (EGP 31.25).')
import numpy as np
fcffs = [r['fcff'] for r in dcf['rows']]
base_wacc = dcf['wacc']
wg_rows = [['WACC \\ terminal g', '9.5%', '10.5%', '11.5%', '12.5%', '13.5%']]
wacc_steps = [base_wacc-0.02, base_wacc-0.01, base_wacc, base_wacc+0.01, base_wacc+0.02]
for w in wacc_steps:
    row = [f'{w*100:.1f}%']
    for g in [0.095, 0.105, 0.115, 0.125, 0.135]:
        if w - g < 0.045: row.append('n.m.'); continue
        pv = sum(f/(1+w)**(i+1) for i, f in enumerate(fcffs))
        tv = fcffs[-1]*(1+g)/(w-g)/(1+w)**5
        ps = ((pv+tv-15210-800.4+9500+sotp['assoc'])*0.9)/1085.5
        row.append(f'{ps:.1f}')
    wg_rows.append(row)
table(wg_rows, [1.5, 1.0, 1.0, 1.0, 1.0, 1.0], first_col_bold=True, size=9.0)
caption(f"SOTP fair value (EGP/share, post-discount) across WACC × terminal growth. Base cell {base_wacc*100:.1f}% × 11.5% = {sotp['ps']:.1f}. "
        'The WACC axis is centred on the sourced bottom-up build (§1.8: rf 22.55% + β 1.0 × ERP 9.41%, blended with '
        'after-tax Kd 14.9%), not a round-number guess. This grid holds the confirmed 41.61% MNT-Halan stake fixed; '
        'it is not the dominant sensitivity in this study (see §1.1).')

# ================= §2 Technical ==============================================
H1('2  Technical and price structure')
P('The tape is strong and extended. GBCO trades above all four major moving averages, the MACD histogram has just re-crossed '
  'positive, and RSI sits in the low-60s — firm, not yet euphoric. The structure is a stair-step advance: a February spike to '
  'the EGP 33.40 all-time high, a two-month consolidation into the April low near 24, and a renewed leg that has carried '
  'price back within ~6% of the high. The 52-week low at 19.10 is the deep floor; the 20-day average near 30 is the trend\u2019s '
  'first support.')
rows = [
 ['Indicator', 'Reading', 'Signal'],
 ['Spot', 'EGP 31.25', '—'],
 ['SMA 20 / 50', f"EGP {tech['sma']['20']:.1f} / {tech['sma']['50']:.1f}", 'Above both — short-term up'],
 ['SMA 100 / 200', f"EGP {tech['sma']['100']:.1f} / {tech['sma']['200']:.1f}", 'Above both — trend up'],
 ['RSI (14)', f"{tech['rsi']:.1f}", 'Firm; below overbought'],
 ['MACD (12,26,9)', f"+{tech['macd']['line']:.2f} line / +{tech['macd']['signal']:.2f} signal / +{tech['macd']['hist']:.2f} hist", 'Bullish, momentum re-building'],
 ['52-week range', 'EGP 19.10 – 33.40', 'Upper tenth of range'],
 ['Realized vol (252d)', f"{tech['rv252']*100:.1f}%", 'Elevated but off crisis highs'],
]
table(rows, [1.8, 2.6, 2.5], first_col_bold=True)
figure('fig3_ma.png', 6.4, 'Figure 3 — Price versus the moving-average stack, last 260 sessions.')
P('For the probabilistic work this matters in one way: an above-trend, momentum-positive tape thickens the near-term upside '
  'tail even where the fundamental work says value has been reached. The technical and fundamental pictures genuinely '
  'disagree here — unusually, with the tape the more bullish — and §6 reads the resulting probability zones without forcing '
  'a reconciliation.')

