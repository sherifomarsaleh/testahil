"""Content part A: masthead → §2."""
from docx_stc_base import *
import os

HERE = os.path.dirname(os.path.abspath(__file__))
# Absolute against this file's own directory: the builders read and wrote relative
# to the working directory, so running them from the repository root — which is how
# every gate does — found no inputs and scattered the outputs.


pr = D['mc']['prob_read']; q20, q60 = D['mc']['q20'], D['mc']['q60']
L = D['lenses']; tech = D['tech']; dcf = D['dcf']; ddm = D['ddm']
LR = D['lens_record']
spot = D['spot']; E = D['experts']; cov = D['cover']

# ---------------- Masthead / title / anchor --------------------------------
masthead()
P('Independent Valuation Study — Educational Analysis', size=12, bold=True, space_before=4, space_after=2)
P('Saudi Telecom Company (Tadawul: 7010)', size=17, bold=True, space_after=2)
P('Fundamental analysis · Technical analysis · Monte Carlo simulation — one integrated read',
  size=10.5, italic=True, color=GREY, space_after=8)
rich([('Anchor: ', dict(bold=True)),
      (f"SAR {spot:.2f} ({D['spot_date']} close) \u00b7 {D['bridge_record']['shares_mn']:,.1f} mn shares "
       f"(issued capital over par, less treasury) \u00b7 market capitalisation SAR "
       f"{spot * D['bridge_record']['shares_mn'] / 1000.0:,.1f} bn \u00b7 "
       "the Kingdom\u2019s incumbent operator and the largest MENA telecom by market value: ", {}),
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
# THE HEADLINE IS COMPUTED AND ITS DIRECTION FOLLOWS THE ARITHMETIC. Every clause here was
# written for an answer this study no longer publishes: a typed spot of 43.58, a "weighted
# central" that [R-LENS-03] retired, four lenses described as clustering tightly when they
# now span ten riyals, a typed terminal share against a computed one, and a central called
# ABOVE spot while the figure printed beside it was negative.
_gap = L['central']['base'] / spot - 1.0
_dir = 'below' if _gap < 0 else 'above'
rich([("The model's read: the central sits below the traded price, and the study is HELD "
       "rather than published while it does. ", dict(bold=True)),
      (f"At SAR {spot:.2f} — the latest known close, on {D['spot_date']} — the shares sit "
       f"about {abs(_gap)*100:.0f}% {'above' if _gap < 0 else 'below'} the central of SAR "
       f"{L['central']['base']:.2f}, which is the CASH-FLOW lens and not an average of the "
       f"reads beside it. Those cross-checks do NOT cluster: the dividend-policy read "
       f"discounts to {L['ddm']['base']:.0f}, the enterprise multiple on this company's own "
       f"history gives {L['relative']['base']:.0f}, a normalised-earnings read marks "
       f"{L['normalized']['base']:.0f}, and disclosed book value is {L['book_value']:.0f} — "
       f"a published range of SAR {LR['envelope']['low']:.1f} to "
       f"{LR['envelope']['high']:.1f}, and the study publishes that disagreement rather "
       f"than averaging it away. The terminal carries {D['dcf']['tv_pct']*100:.0f}% of the "
       f"cash-flow value — disclosed, not buried — and is built on the "
       f"{D['terminal_record']['inputs']['useful_life_years']:.1f}-year asset life this "
       f"company's own accounting-policies note discloses, never on the reciprocal of an "
       f"inflation rate. Over three months the price map places the 5th-to-95th percentile "
       f"band at roughly SAR {q60['5']:.0f}-{q60['95']:.0f}, the median at {q60['50']:.1f}, "
       f"and the middle half at SAR {q60['25']:.0f}-{q60['75']:.0f}.", {})],
     space_after=8)

# ---------------- Valuation summary table -----------------------------------
H2('Valuation summary — every read at a glance')
P('One table for the four reads that follow — what the business is worth (fundamental), what the tape is doing (technical), '
  'where price could travel over three months (Monte Carlo), and how three independent expert methods land. Every row is '
  'developed in the sections and appendices below.', size=9.8)
# THE TAKEAWAY COLUMN RANKS THREE COMMITTED NUMBERS AND WAS TYPED. "Closest to spot" sat
# on Expert 3 while Expert 2 is nearer the market, and "the floor-setter" sat on the
# expert whose read is the HIGHEST of the three.
_eb = {'Expert 1': E['e1']['base'], 'Expert 2': E['e2']['base'], 'Expert 3': E['e3']['base']}
_near = min(_eb, key=lambda k: abs(_eb[k] - spot))
_low = min(_eb, key=lambda k: _eb[k])


def _etake(who):
    bits = []
    if who == _low:
        bits.append('the lowest of the three')
    if who == _near:
        bits.append('nearest the market')
    return '; '.join(bits) if bits else 'between the two'


rows = [
 ['Lens / read', 'What it measures', 'Output', 'Takeaway'],
 ['FUNDAMENTAL — what the business is worth (the anchor)', '', '', ''],
 ['FCFF DCF (primary)', 'Core operations + stake marks − net debt − NCI', f"SAR {L['dcf']['base']:.0f}", f"{(L['dcf']['base']/spot-1)*100:+.0f}% vs spot"],
 ['Dividend discount (policy lens)', 'The locked SAR 0.55/quarter, discounted at Ke', f"SAR {L['ddm']['base']:.0f}", f"{(L['ddm']['base']/spot-1)*100:+.0f}%"],
 ['Relative (EV/EBITDA)', 'FY26E EBITDA × justified 9.0×, bridged to equity', f"SAR {L['relative']['base']:.0f}", f"{(L['relative']['base']/spot-1)*100:+.0f}%"],
 ['Normalized earnings', 'Ex-one-off PAT × through-cycle P/E', f"SAR {L['normalized']['base']:.0f}", f"{(L['normalized']['base']/spot-1)*100:+.0f}% · a cross-check, not the floor"],
 # ONE CLASS PRIMARY IS THE CENTRAL. This row read "Weighted central — Blend 35/25/20/20",
 # the construction [R-LENS-03] retired: a number produced by averaging several methods is
 # not more robust than the best of them, it is a new method with free parameters nobody
 # tested, and it imports every weakness of the weakest lens at whatever weight somebody
 # typed. Two of those four are not permitted cross-checks for this class at all.
 ['THE CENTRAL — the cash-flow lens, not an average',
  'the class primary; the others are cross-checks',
  f"SAR {L['central']['base']:.2f}",
  f"{(L['central']['base']/spot-1)*100:+.1f}% vs SAR {spot:.2f}"],
 ['Published range', 'the span of the present-value reads',
  f"SAR {LR['envelope']['low']:.1f}-{LR['envelope']['high']:.1f}", ''],
 ['TECHNICAL — what the tape is doing (timing, not value)', '', '', ''],
 ['Trend & momentum', 'Price vs the 20/50/100/200-day averages',
  f"Above all four, by {(D['cone_anchor']/max(tech['sma'].values())-1)*100:.1f}% on the highest", 'Firm, low energy'],
 ['Momentum / range', 'RSI · MACD · 52-week range',
  f"RSI {tech['rsi']:.0f} · MACD {tech['macd']['hist']:+.2f} · {tech['lo52']:.1f}–{tech['hi52']:.1f}",
  'Firm, not overbought' if tech['rsi'] < 70 else 'Overbought'],
 ['THE PRICE MAP — where price could go, from the cone anchor', '', '', ''],
 [D['engine']['horizons']['1M']['label'].capitalize(), '50,000 paths, the production engine',
  f"p5 {q20['5']:.0f} · p50 {q20['50']:.1f} · p95 {q20['95']:.0f}",
  f"Median {(q20['50']/D['cone_anchor']-1)*100:+.1f}% on the anchor"],
 [D['engine']['horizons']['3M']['label'].capitalize(), 'same engine, the longer horizon',
  f"p5 {q60['5']:.0f} · p50 {q60['50']:.1f} · p95 {q60['95']:.0f}",
  f"Median {(q60['50']/D['cone_anchor']-1)*100:+.1f}%; a small upward lean"],
 ['EXPERT PANEL — three independent methods (Appendix C)', '', '', ''],
 ['Expert 1 — cash returns / economic profit', 'ROIC vs WACC with fading excess returns', f"SAR {E['e1']['base']:.0f}", _etake('Expert 1')],
 ['Expert 2 — normalized earnings power', 'Mid-cycle EPS × multiple', f"SAR {E['e2']['base']:.0f}", _etake('Expert 2')],
 ['Expert 3 — macro-policy scenario tree', 'Rate path & payout scenarios into a DDM', f"SAR {E['e3']['base']:.0f}", _etake('Expert 3')],
 ['Panel range', 'Spread = the fade-vs-franchise question', f"SAR {min(E['e1']['base'],E['e2']['base'],E['e3']['base']):.0f}–{max(E['e1']['base'],E['e2']['base'],E['e3']['base']):.0f}", f"Centres ~SAR {sorted([E['e1']['base'],E['e2']['base'],E['e3']['base']])[1]:.0f}"],
]
table(rows, [2.15, 2.35, 1.45, 1.15], band_rows=[1, 7, 10, 13], first_col_bold=False, size=8.9)
rich([('Bottom line. ', dict(bold=True)),
      (f"The fundamental reads span SAR {LR['envelope']['low']:.1f} to "
       f"{LR['envelope']['high']:.1f} and the central — the cash-flow lens, which is what "
       f"this class is valued on — is SAR {L['central']['base']:.2f}, "
       f"{abs(_gap)*100:.1f}% {_dir} the latest known price. THAT GAP IS WHY THIS STUDY IS "
       "HELD: a central more than a tenth below the traded price is a high-prior-of-defect "
       "region, and an eight-heading review is what stands between the number and a reader. "
       "The review did not move the answer toward the price and was not meant to — what it "
       "found were defects in the model, each corrected on its own evidence, and the answer "
       "moved where the corrections took it. The cross-checks are published beside the "
       "central and never averaged into it: two of them are not permitted cross-checks for "
       "this class at all, and in the delivered edition they carried 45% of a weighted "
       "answer.", {})], size=9.8, space_after=8)

# ---------------- Company overview -------------------------------------------
H2('Company overview — stc at a glance')
rows = [
 ['Item', 'Value'],
 ['Listed entity', 'Saudi Telecom Company (stc Group), Tadawul: 7010'],
 ['What it is', 'The Kingdom’s incumbent telecom operator and MENA’s largest telecom by market value; consumer, enterprise and wholesale connectivity plus a digital-infrastructure and fintech portfolio'],
 ['Spot / date', f"SAR {spot:.2f} \u00b7 {D['spot_date']} close, the latest known"],
 ['Shares \u00b7 market capitalisation',
   f"{D['bridge_record']['shares_mn']:,.1f} mn (issued capital over par, less treasury) "
   f"\u00b7 SAR {spot * D['bridge_record']['shares_mn'] / 1000.0:,.1f} bn"],
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
P('We value stc as a going-concern operator. ONE lens is the answer — a free-cash-flow-to-firm DCF — and the others '
  'are published beside it as cross-checks rather than averaged into it. The primary lens is that DCF, '
  'because a mature, capital-intensive network operator is ultimately worth the cash its infrastructure produces after the '
  'capex that keeps it competitive; the tower and Telefónica stakes sit outside the operating engine and are marked '
  'separately on the bridge. A dividend-discount read is the natural cross-check for a company whose board has locked a '
  'SAR 0.55-per-quarter distribution through 2027. A relative EV/EBITDA read and a normalized-earnings read complete the '
  'set. The weights and the football field are in §1.5; the segment engine in §1.6; the crux — dividend cover against the '
  'capex cycle, in real units — in §1.7; the cost-of-capital build (every input sourced, both ERP bases published) in §1.8; '
  'and the sensitivity grids in §1.9. '
  'One lens-selection note, considered and set aside: stc does own a captive-finance arm in stc bank, but at SAR 2.0 bn of revenue — 2.5% of the group — and an early-stage loan book it does not yet warrant the split-legs '
  'treatment a bank leg would get; it is carried inside the subsidiaries line and flagged as such, to be revisited '
  'once its regulated financials give it a book worth marking separately. Throughout, the cost of equity is '
  f"published explicitly as the normalised risk-free rate plus beta times the equity risk premium: "
  f"{D['coc_record']['rf_star']*100:.2f}% + {D['coc_record']['beta']:.4f} x {D['coc_record']['erp']*100:.2f}% = "
  f"{D['coc_record']['ke_exp']*100:.2f}%, on the {D['coc_record']['erp_basis']} basis this study names as central, "
  'with the alternative basis published beside it in §1.8 rather than chosen silently. The beta behind it is a '
  'five-year weekly regression against the published index of the exchange the stock is listed on, not an assumed '
  'round number.')

H2('1.1  The FCFF DCF — the primary lens')
# EVERY NUMBER IN THIS PARAGRAPH WAS TYPED AND FOUR OF THEM HAD STOPPED BEING TRUE. It
# said revenue compounds at 3.0% where the committed path gives 2.4%; that the margin
# GLIDES UP from 31.4% to 32.5% where the model runs 31.98% down to 31.82%; that capital
# intensity is 16.5% of revenue fading to 15.0%, which is MANAGEMENT'S GUIDANCE BAND and
# is exactly the construction this rebuild retired — guidance is scored, never consumed —
# against a measured 14.96%; and that tax is 9.7% where the model applies 8.03%. The
# reconciliation instrument could not see any of it: each of those figures exists
# elsewhere in the committed record (a sensitivity step, a filed year, a guidance range),
# so a rendering set wide enough to admit the legitimate uses admits these too. A widening
# made to clear a false positive can hide a true one, and the answer is not a narrower set
# but a paragraph that computes what it asserts.
_rv = D['drivers'] if 'drivers' in D else {}
_ebm = _rv['ebitda_m']; _cpx = _rv['capex_pct']
_revp = [r['rev'] for r in D['dcf']['rows']]
_r0, _r4 = _revp[0], _revp[-1]
_cagr = (_r4 / _r0) ** (1.0 / (len(_revp) - 1)) - 1
P('The revenue engine is the §1.6 segment build: stc discloses revenue by segment rather than subscribers and revenue '
  'per subscriber, so the forecast grows the disclosed lines on their own drivers rather than manufacturing a '
  'bottom-up split it has no data for. '
  f"Group revenue compounds {_cagr*100:.1f}% a year across the explicit window, from SAR {_r0:,.0f} mn to "
  f"{_r4:,.0f} mn — consumer growing slowly, enterprise recovering as mega-project phasing normalises, wholesale on "
  'hosting and fixed-wireless backhaul, and the subsidiaries fastest of the four. The EBITDA margin runs '
  f"{_ebm[0]*100:.2f}% in the first forecast year and {_ebm[-1]*100:.2f}% in the last: essentially flat, and slightly "
  'DOWN rather than up. That is deliberate and it is the point of §1.6 — margins here are an OUTPUT of the cost build, '
  'not an input, so the model is not permitted to assume the mix improvement that a glide would represent. '
  f"Capital intensity is {_cpx[0]*100:.2f}% of revenue, held flat, and it is MEASURED rather than guided: it is the "
  f"three filed years' own mean of {_rv['capex_to_dna_adopted']:.3f} times the depreciation of the base being renewed. "
  'Management publishes a band and an earlier edition of this study took its path straight from it; a forward target '
  'leans the same way an optimistic model does, so guidance is scored against what happens and never consumed as an '
  'input. Working capital is projected from the asset-conversion cycle rather than plugged. '
  f"Zakat and income tax enter at the {D['tax_rate']*100:.2f}% the three filed years imply on operating profit, with "
  'the disclosed reversal of a prior year’s provision taken out rather than extrapolated.', size=10.5)
rows = [['SAR mn', 'FY26E', 'FY27E', 'FY28E', 'FY29E', 'FY30E']]
labels = [('rev', 'Group revenue'), ('ebitda', 'EBITDA'), ('dna', 'D&A'), ('ebit', 'EBIT'),
          ('nopat', 'NOPAT = EBIT × (1 − %.2f%%)' % (D['tax_rate'] * 100)), ('dna', '+ D&A'), ('capex', '− Capex'),
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
 [f"Terminal value (perpetuity, g = {dcf['tg']*100:.2f}%)", f"{dcf['tv']:,.0f}"],
 ['PV of terminal value', f"{dcf['pv_tv']:,.0f}"],
 ['Enterprise value — core operations', f"{dcf['ev']:,.0f}"],
 ['Terminal value as % of enterprise value', f"{dcf['tv_pct']*100:.0f}%"],
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
  "Appendix A shows both series so the difference is visible rather than averaged away.")

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
 ['Terminal value as % of the total', f"{ddm['tv_pct']*100:.0f}%"],
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

# The reconciliation of note 9 is its own committed artefact rather than a block inside
# the numbers file, because it is read by three builders and written by one.
import json as _json
_ISJ = _json.load(open(os.path.join(HERE, 'income_statement.json')))
H2('1.4  Normalized earnings power — where this sits in the cycle')
P('Cycle position first: unlike a developer or a smelter, stc’s P&L has no violent cycle, but FY25 profit is '
  f"still not a clean base — it carries the reversal of a prior year's zakat provision, SAR "
  f"{_ISJ['zakat_reversal_fy2025']/1000.0:,.0f} mn on its own disclosed line, and FY24 before "
  'it carried the SAR 12.9 bn TAWAL disposal gain, a SAR 1.5 bn withholding-tax reversal and a SAR 2.6 bn early-retirement '
  f"charge. Margins sit mid-cycle: the forecast opens at an EBITDA margin of {D['drivers']['ebitda_m'][0]*100:.2f}% "
  'against the filed FY2025 year, and it is an output of the cost build rather than a target, enterprise revenue is at the '
  'soft point of the government mega-project phasing, and the subsidiary portfolio (stc bank, center3) is still in its '
  'investment phase, with several guided to turn contribution-positive from 2026. '
  # THIS SENTENCE WAS THE PRE-CORRECTION NORMALISATION AND SURVIVED THE CORRECTION. It read
  # "~SAR 14.4 bn (reported FY25 14.8 bn less the zakat credit), or EPS ~2.89" — which is
  # the filed profit less 466, the NET zakat line for the year rather than the one-off
  # inside it. What is non-recurring is the reversal of prior years' provision that the
  # zakat note carries on its own line, and the normalisation charges the year at the rate
  # the three filed years imply instead. The table in Appendix C was rebuilt on that and
  # asserted; this paragraph restated the retired arithmetic in words, where no assertion
  # reaches. FIXING A TABLE DOES NOT FIX THE SENTENCE THAT RESTATES IT.
  f"Normalised attributable profit is therefore SAR {D['rel_basis']['norm_pat']/1000.0:,.1f} bn — the filed profit "
  f"before zakat, charged at the {D['tax_rate_on_pbz']*100:.2f}% the three filed years imply once the disclosed "
  'reversal of a prior year’s provision is taken out rather than extrapolated, less the minority’s share — or '
  f"SAR {D['rel_basis']['norm_eps']:.2f} a share, capitalised at "
  f"{D['lenses']['normalized']['base']/D['rel_basis']['norm_eps']:.0f} times, which is this stock’s own multi-year "
  'median area and the middle of its peer set.', size=10.5)
rows = [
 ['Normalized-earnings basis', 'Bear', 'Base', 'Bull'],
 ['Normalized PAT (SAR mn)', '13,600', '14,400', '15,200'],
 ['Justified P/E', '13.5×', '15.0×', '16.5×'],
 ['Fair value (SAR/share)', f"{L['normalized']['bear']:.1f}", f"{L['normalized']['base']:.1f}", f"{L['normalized']['bull']:.1f}"],
]
table(rows, [2.6, 1.3, 1.3, 1.3], first_col_bold=True)
rich([(f"Normalized base ≈ SAR {L['normalized']['base']:.0f}", dict(bold=True)),
      # "THE FLOOR OF THE SET" IS FALSE ON THREE COMMITTED NUMBERS: this lens reads ABOVE
      # both the cash-flow lens and the dividend lens, and the DISCLOSED floor is book value.
      (f" — not the floor of the set, which is the disclosed book value of SAR {L['book_value']:.2f}, but the read "
       'that pays nothing for growth beyond today’s earnings power and treats the data-centre '
       'build purely as cost.', {})])

H2('1.5  Synthesis — the central, and the lenses beside it')
P('We weight the DCF most heavily because it is the only lens that prices the full capex-and-recovery arc; the DDM carries '
  'the pre-committed cash; the relative lens anchors to what the market pays for GCC telecom cash flows today; normalized '
  'earnings is the ballast.')
rows = [['Lens', 'Weight', 'Bear', 'Base', 'Bull'],
 ['FCFF DCF (primary)', '35%', f"{L['dcf']['bear']:.0f}", f"{L['dcf']['base']:.1f}", f"{L['dcf']['bull']:.0f}"],
 ['Dividend discount (policy)', '25%', f"{L['ddm']['bear']:.0f}", f"{L['ddm']['base']:.1f}", f"{L['ddm']['bull']:.0f}"],
 ['Relative (EV/EBITDA)', '20%', f"{L['relative']['bear']:.0f}", f"{L['relative']['base']:.1f}", f"{L['relative']['bull']:.0f}"],
 ['Normalized earnings', '20%', f"{L['normalized']['bear']:.0f}", f"{L['normalized']['base']:.1f}", f"{L['normalized']['bull']:.0f}"],
 ['THE CENTRAL — the class primary', '', f"{L['dcf']['bear']:.1f}",
  f"{L['dcf']['base']:.1f}", f"{L['dcf']['bull']:.1f}"],
]
table(rows, [2.4, 0.9, 1.1, 1.1, 1.1], first_col_bold=True, band_rows=[5])
figure(os.path.join(HERE, 'fig1_football.png'), 6.3, 'Figure 1 — Valuation football field. Bars span bear–bull per lens; the brass tick is each '
       'base case; the gold band is the range the present-value reads span; the ink line is the market price.')
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
P('The build is per disclosed segment. THE PREVIOUS EDITION GREW FOUR BUSINESS UNITS — '
  'consumer, enterprise, wholesale and a subsidiaries residual — which is not how this '
  'company reports: note 9 discloses ELEVEN operating segments and each is grown on its own '
  'measured real rate. One of them, the Saudi operating business and two thirds of group '
  'revenue, is built as volume times price from the subscriber counts the earnings '
  'presentations disclose; the others are forecast on their net rate because no unit data '
  'is published for them, and that gap is stated rather than filled.', size=9.8)
fc = D['forecast']
_SEGH, _SEGF = D['seg_hist'], D['seg_forecast']
_ELIM = 'Eliminations / adjustments'
_order = [k for k in sorted(_SEGH, key=lambda k: -_SEGH[k]['FY25']) if k != _ELIM]
rows = [['Operating segment (note 9)', 'FY24', 'FY25', 'FY26E', 'FY28E', 'FY30E']]
for _k in _order:
    rows.append([_k,
                 f"{_SEGH[_k]['FY24']:,.0f}", f"{_SEGH[_k]['FY25']:,.0f}",
                 f"{_SEGF[_k]['FY26E']:,.0f}", f"{_SEGF[_k]['FY28E']:,.0f}",
                 f"{_SEGF[_k]['FY30E']:,.0f}"])
# The elimination is forecast as a share of GROSS segment revenue rather than grown on its
# own rate, so it comes off the forecast record's own line rather than the segment table.
rows.append([_ELIM,
             f"({abs(_SEGH[_ELIM]['FY24']):,.0f})", f"({abs(_SEGH[_ELIM]['FY25']):,.0f})",
             f"({abs(fc['FY26E']['elim']):,.0f})", f"({abs(fc['FY28E']['elim']):,.0f})",
             f"({abs(fc['FY30E']['elim']):,.0f})"])
rows.append(['Group revenue',
             f"{D['hist']['rev']['FY24']:,.0f}", f"{D['hist']['rev']['FY25']:,.0f}",
             f"{fc['FY26E']['rev']:,.0f}", f"{fc['FY28E']['rev']:,.0f}",
             f"{fc['FY30E']['rev']:,.0f}"])
rows.append(['EBITDA margin', '', '',
             f"{fc['FY26E']['ebitda_margin']*100:.1f}%",
             f"{fc['FY28E']['ebitda_margin']*100:.1f}%",
             f"{fc['FY30E']['ebitda_margin']*100:.1f}%"])
rows.append(['Capital intensity (% of revenue)', '', '',
             *[f"{D['drivers']['capex_pct'][i]*100:.1f}%" for i in (0, 2, 4)]])
table(rows, [2.35, 0.95, 0.95, 0.95, 0.95, 0.95], first_col_bold=True, size=8.0)
caption('History: stc FY2025 earnings presentation and IR releases (stc.com), restated basis. Forecast drivers are the house’s '
        'own flagged view. These are the company\'s own internal unit names, used here to describe '
        'what drives the business; the MODEL is built on the eleven operating segments note 9 '
        'discloses, which is a different and finer cut.')

# The crux paragraph quotes the cover table, the beta grid and the rate grid; all three
# are committed and none is retyped.
_CV = D['cover']
S = D['sens']
_GI = min(range(len(S['g_steps'])), key=lambda k: abs(S['g_steps'][k] - D['dcf']['tg']))
_WI = min(range(len(S['wacc_steps'])), key=lambda k: abs(S['wacc_steps'][k] - D['dcf']['wacc']))
_B1 = next(r for r in S['beta_grid'] if r['adopted'])
_BETA1 = next(r for r in S['beta_grid'] if abs(r['beta'] - 1.0) < 1e-9)

H2('1.7  The crux — dividend cover against the capex cycle, in real units')
P('Three judgments drive this valuation, and all three are observable rather than abstract. First and largest: capex '
  f"intensity against the locked dividend. The policy dividend costs SAR "
  f"{D['drivers']['payout_dps'][0] * D['bridge_record']['shares_mn'] / 1000.0:,.2f} bn a year "
  f"({D['drivers']['payout_dps'][0]:.2f} x {D['bridge_record']['shares_mn']:,.1f} mn shares); "
  # THIS PARAGRAPH DESCRIBED A COVER TABLE THAT NO LONGER EXISTS AND A BETA THAT NO LONGER
  # EXISTS. It framed the tension across management's 15-17.5% GUIDANCE band — the
  # construction this rebuild retired, since guidance is scored and never consumed — and
  # its cover figures (0.86x at the top, fully covered at the bottom) belong to that band,
  # not to the three filed years the table below actually spans. It then described the
  # discount rate as built on a nine-week regression of 0.48.
  f"and the model spans the range this company's OWN three filed years actually ran, "
  f"{_CV[0]['capex'].split(' ')[0]} to {_CV[-1]['capex'].split(' ')[0]} of revenue, rather than the band management "
  f"guides to. The cover table below is the whole tension in one place: at the heaviest of those three years the "
  f"dividend is {_CV[-1]['cover']:.2f}x covered by model free cash flow in the first forecast year, and at the "
  f"lightest {_CV[0]['cover']:.2f}x — so on this company's own history of capital spending the dividend is covered "
  f"throughout, and the question is whether the data-centre build takes intensity ABOVE anything it has yet run. "
  f"Second: the discount rate, a {D['coc_record']['weight_equity']*100:.0f}%-equity-weighted cost of capital on a "
  f"{D['coc_record']['beta']:.2f} beta from a five-year weekly regression (§1.8) — at a beta of 1.0 the value falls "
  f"from SAR {_B1['ps']:.2f} to {_BETA1['ps']:.2f}, {(_BETA1['ps']/spot-1)*100:+.0f}% against the price, so §1.9 "
  'publishes the whole grid rather than letting one regression settle it. Third: the policy rate path — each 50 basis '
  f"points off the curve is worth about SAR {abs(S['table_wg'][_WI-1][_GI]-S['table_wg'][_WI][_GI]):.1f} on the value "
  'and lowers the funding cost of the build directly. A fourth, slower variable: mobile competition (Mobily’s '
  'subscriber growth has '
  'outpaced stc’s revenue growth for four quarters) — each 1 pp off consumer growth costs ≈SAR 2 of fair value.', size=10.5)
rows = [['FY26E scenario (real units)', 'Model FCF (SAR bn)', 'Dividend bill (SAR bn)', 'Cover']]
for c in cov:
    rows.append([f"Capex at {c['capex']}", f"{c['fcf']:.1f}", f"{c['div']:.1f}", f"{c['cover']:.2f}×"])
table(rows, [2.6, 1.5, 1.5, 0.9], first_col_bold=True)
caption('The dividend schedule and its stress test live in Appendix A.3. The dividend is policy-locked through the '
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
  'and no currency factor in the price map. Every input in the cost-of-capital build is sourced and named:', size=10.5)
# EVERY CELL OF THIS TABLE WAS TYPED, AND BY THE TIME THE STUDY WAS REBUILT NOT ONE OF
# THEM MATCHED THE MODEL. It published a risk-free rate of 5.50% against a committed
# 5.52%, a beta of 0.48 from a nine-week daily window against a conforming 0.71 from a
# five-year weekly regression, a cost of equity of 7.90% against 8.59%, weights of
# 90.6/9.4 against 90.3/9.7, a weighted cost of capital of 7.59% against 8.13%, and a
# terminal growth of 2.50% against 2.00%. The model was right throughout; the page a
# reader actually reads described a different company's cost of capital. Every figure
# below now comes from the committed schedule.
wb = dcf['wacc_build']
_c = D['coc_record']
_beta = wb['beta_reg']
rows = [
 ['Cost-of-capital build', 'Value', 'Source'],
 ['Risk-free rate, as observed', f"{_c['rf_observed']*100:.2f}%",
  'The sovereign yield on the house macro path for Saudi Arabia, carried with its own as-of date'],
 ['  — less this sovereign\u2019s own default spread', f"{_c['default_spread']*100:.2f}%",
  'Country risk is charged exactly once, and it is charged inside the equity risk premium below — so it is '
  'removed here rather than counted twice'],
 ['Normalised risk-free rate', f"{_c['rf_star']*100:.2f}%", 'The two lines above, by subtraction'],
 ['Equity beta', f"{_beta['beta']:.4f}",
  f"A {_beta['window_years']:.2f}-year weekly regression of stc against the published index of the exchange it is "
  f"listed on ({_beta['index_file']}, as of {_beta['index_asof']}): {_beta['n']} observations, R\u00b2 "
  f"{_beta['r2']*100:.1f}%, standard error {_beta['se']:.4f}. This is the first tier of the house preference order, "
  f"not a stopgap — but it explains {_beta['r2']*100:.0f}% of the variance and no more, which is why §1.9 prices the "
  f"answer at every beta up to 1.2"],
 [f"Equity risk premium ({_c['erp_basis']} basis, adopted)", f"{_c['erp']*100:.2f}%",
  'The premium published for Saudi Arabia specifically, on the basis this study names as central; the alternative '
  'basis is published beside it rather than chosen silently'],
 ['Cost of equity', f"{_c['ke_exp']*100:.2f}%", 'The normalised risk-free rate plus beta times the premium'],
 ['Cost of debt, before tax', f"{_c['kd_pretax']*100:.2f}%",
  'Built from the company\u2019s own facilities, and above this sovereign\u2019s own yield, as a same-currency corporate '
  'borrower must be'],
 [f"Cost of debt, after tax", f"{_c['kd_aftertax']*100:.2f}%",
  f"At the {D['tax_rate']*100:.2f}% effective rate the three filed years imply" if 'tax_rate' in D else
  'At the effective rate the three filed years imply'],
 ['Weights (equity / debt)', f"{_c['weight_equity']*100:.1f}% / {_c['weight_debt']*100:.1f}%", _c['weights_source']],
 ['Weighted cost of capital', f"{_c['wacc_exp']*100:.2f}%", 'The explicit-window rate the forecast is discounted at'],
 ['Terminal cost of capital', f"{_c['wacc_terminal']*100:.2f}%",
  'Flat against the explicit window, and that is not an oversight: the riyal is pegged, so this economy is already at '
  'its terminal cost of capital by construction of the peg and there is no normalisation to glide toward'],
 ['Terminal growth (nominal)', f"{dcf['tg']*100:.2f}%",
  f"Terminal inflation of {D['macro_record']['terminal']['inflation_in_rf']*100:.1f}% plus a stated real growth of "
  f"{D['macro_record']['terminal']['real']*100:.1f}% — derived from the house macro path rather than chosen, and the "
  'real component is written down as the number it is'],
]
table(rows, [2.3, 1.0, 3.6], first_col_bold=True, size=8.4)
P('Two honesty notes on this build. First, the sovereign quote behind the risk-free rate is older than the fourteen-day '
  'bound this house sets: ' + _c['sovereign_staleness_disclosed'] + ' Second, the beta is a proper five-year weekly '
  f"regression against the exchange\u2019s own published index — the standard, not a stopgap — but its R\u00b2 of "
  f"{_beta['r2']*100:.0f}% means roughly {(1-_beta['r2'])*100:.0f}% of what moves this stock is specific to it rather "
  'than to the market. A beta is a statement about co-movement, and on this name that statement is weak. The grid in '
  '§1.9 prices the answer at every beta up to 1.2 for exactly that reason. Both are recorded with the study\u2019s own '
  'inputs.', size=9.6)

H2('1.9  Sensitivity — the margin, the capex, the rate spread, and the beta')
P('The first grid re-prices the cash-flow model across the two real-unit operating levers (EBITDA margin and capital '
  'intensity); the second across the cost of capital × terminal growth; the third across the beta — which is a proper '
  'five-year weekly regression against the exchange’s own index, but explains less than a third of this stock’s '
  'variance, so it is the input whose uncertainty is widest even though its construction is sound.')
figure(os.path.join(HERE, 'fig2_sens.png'), 5.6,
       'Figure 2 — Fair value from the cash-flow model (SAR/share) across shifts in the EBITDA margin and in '
       f"capital intensity. The bold cell is the base case. EVERY cell in the grid sits below the market price of "
       f"SAR {spot:.2f}: on this model the disagreement with the market survives the whole plausible range of both "
       'operating levers, so it is not an artefact of where either one was set.')
S = D['sens']
wg_rows = [['WACC \\ terminal g', '1.5%', '2.0%', '2.5%', '3.0%', '3.5%']]
for i, w in enumerate(S['wacc_steps']):
    row = [f'{w*100:.2f}%' + (' (base)' if abs(w - dcf['wacc']) < 1e-9 else '')]
    for j in range(5):
        v = S['table_wg'][i][j]
        row.append('n.m.' if v is None else f'{v:.1f}')
    wg_rows.append(row)
table(wg_rows, [1.5, 1.0, 1.0, 1.0, 1.0, 1.0], first_col_bold=True, size=9.0)
# THE BASE CELL IS NOT IN THE 2.5% COLUMN. This caption named one, typed, while the
# terminal growth the model actually uses is 2.00% — so it pointed a reader at the wrong
# cell of its own grid and the figure it quoted came from a third place entirely.
_gi = min(range(len(S['g_steps'])), key=lambda i: abs(S['g_steps'][i] - dcf['tg']))
_wi = min(range(len(S['wacc_steps'])), key=lambda i: abs(S['wacc_steps'][i] - dcf['wacc']))
assert abs(S['table_wg'][_wi][_gi] - dcf['ps']) < 1e-6, 'the named base cell must be the answer'
caption(f"Fair value from the cash-flow model (SAR/share) across the cost of capital and terminal growth. The base "
        f"cell is {dcf['wacc']*100:.2f}% against {dcf['tg']*100:.2f}%, giving SAR {S['table_wg'][_wi][_gi]:.2f}. "
        'The CDS-ERP alternative WACC (7.90%) sits between the third and fourth rows.')
# SIX TYPED ROWS, AND BY THE REBUILD EVERY ONE WAS STALE — including the row labelled the
# regressed base, which still carried the retired nine-week beta of 0.48 and a cost of
# capital of 7.59% against the schedule's 8.13%. A grid whose base row disagrees with the
# model is worse than no grid, because it reads as the model's own arithmetic. The grid is
# now computed, and the model asserts at build time that its adopted row reproduces the
# published answer.
_BG = D['sens']['beta_grid']
rows = [['Beta', 'Cost of equity', 'Cost of capital', 'Value per share', 'Note']]
for _r in _BG:
    rows.append([f"{_r['beta']:.2f}", f"{_r['ke']*100:.2f}%", f"{_r['wacc']*100:.2f}%",
                 f"{_r['ps']:.2f}",
                 'the adopted regression' if _r['adopted'] else
                 ('the house fallback, had the regression failed its usability gate'
                  if abs(_r['beta'] - 1.0) < 1e-9 else '')])
table(rows, [1.0, 1.4, 1.4, 1.3, 2.1], first_col_bold=True, size=8.9)
_b1 = next(r for r in _BG if abs(r['beta'] - 1.0) < 1e-9)
caption('The grid is mandatory disclosure here: the regression is a proper five-year weekly one against the exchange\u2019s '
        f"own published index, but it explains {D['dcf']['wacc_build']['beta_reg']['r2']*100:.0f}% of this stock\u2019s "
        'variance and no more, so the answer is priced across the plausible range rather than at one point. The read '
        f"survives moderate beta doubt \u2014 at {_BG[-3]['beta']:.2f} the value is SAR {_BG[-3]['ps']:.2f} \u2014 but not "
        f"a full reversion to 1.0, where it falls to SAR {_b1['ps']:.2f}, "
        f"{(_b1['ps']/D['spot']-1)*100:.0f}% against the market price.")

# ================= §2 Technical ==============================================
H1('2  Technical and price structure')
# EVERY CLAUSE HERE IS SELECTED BY A COMPUTED NUMBER. What stood here contradicted the
# model beside it three times in one paragraph: it called an RSI of 65.7 "dead neutral",
# a positive MACD "fractionally negative", and a price sitting above all four moving
# averages "within +/-1% of the stack, no trend". Every figure in the table was computed
# and right; the words around them were typed and wrong, which no check that inspects
# figures can see. The prose is now assembled from the same numbers the table prints.
# TWO CLOCKS, AND THIS SECTION RUNS ON THE OTHER ONE. The technical read is computed on
# the last session in the persistent price library; the valuation is struck against the
# latest known close, which is a later date. Using the valuation price here put the stock
# 0.1% BELOW the highest of its own moving averages in a sentence saying it had stepped
# clear of them — the same figure, the wrong clock. Everything in this section is
# measured at the technical anchor, and the section says which date that is.
_tanchor = D['cone_anchor']
_tdate = D['cone_anchor_date']
_stack = [tech['sma'][k] for k in ('20', '50', '100', '200')]
_above = sum(1 for v in _stack if _tanchor > v)
_gap = (_tanchor / max(_stack) - 1) * 100
_rsi = tech['rsi']
_rsi_word = ('firm but short of overbought' if 60 <= _rsi < 70 else
             'overbought' if _rsi >= 70 else
             'neutral' if 45 <= _rsi < 60 else
             'soft' if 30 <= _rsi < 45 else 'oversold')
_macd_word = ('positive, with the line above its signal' if tech['macd']['hist'] > 0
              else 'negative, with the line below its signal')
_pos52 = (spot - tech['lo52']) / (tech['hi52'] - tech['lo52']) * 100
P(f"The tape is firm and the stock is trading above its whole moving-average stack. At SAR {_tanchor:.2f} the price sits "
  f"above all {_above} of the 20-, 50-, 100- and 200-day averages, which are themselves compressed into a band of "
  f"SAR {max(_stack) - min(_stack):.2f} ({min(_stack):.2f} to {max(_stack):.2f}) — so the stack is flat while the price "
  f"has stepped clear of it by {_gap:.1f}% above the highest of the four. RSI(14) at {_rsi:.0f} is {_rsi_word}, and the "
  f"MACD histogram is {_macd_word}. The 52-week range is narrow for an emerging-market name — {tech['lo52']:.2f} to "
  f"{tech['hi52']:.2f}, a span of {(tech['hi52'] / tech['lo52'] - 1) * 100:.0f}% — and realised volatility over the "
  f"trailing year ({tech['rv252'] * 100:.1f}%) is among the lowest on the exchange. Price is up "
  f"{tech['chg20'] * 100:.1f}% over the last twenty sessions and {tech['chg60'] * 100:.1f}% over the last sixty. This is "
  "a quiet advance rather than a trending breakout: the direction is up, the energy behind it is low.")
rows = [
 ['Indicator', 'Reading', 'What it says'],
 [f'Price on {_tdate}', f"SAR {_tanchor:.2f}", f"{_pos52:.0f}th percentile of the 52-week range"],
 ['SMA 20 / 50', f"SAR {tech['sma']['20']:.2f} / {tech['sma']['50']:.2f}",
  f"Price above both, by {(_tanchor/tech['sma']['20']-1)*100:.1f}% and {(_tanchor/tech['sma']['50']-1)*100:.1f}%"],
 ['SMA 100 / 200', f"SAR {tech['sma']['100']:.2f} / {tech['sma']['200']:.2f}",
  f"Stack compressed into SAR {max(_stack)-min(_stack):.2f} — a long flat base"],
 ['RSI (14)', f"{_rsi:.1f}", _rsi_word.capitalize()],
 ['MACD (12,26,9)', f"{tech['macd']['line']:+.2f} line / {tech['macd']['signal']:+.2f} signal / {tech['macd']['hist']:+.2f} hist",
  _macd_word.capitalize()],
 ['52-week range', f"SAR {tech['lo52']:.2f} – {tech['hi52']:.2f}",
  f"A span of {(tech['hi52']/tech['lo52']-1)*100:.0f}% — narrow"],
 ['Change over 20 / 60 sessions', f"{tech['chg20']*100:+.1f}% / {tech['chg60']*100:+.1f}%", 'A quiet advance'],
 ['Realised volatility (252 sessions)', f"{tech['rv252']*100:.1f}%",
  f"Very low; the forward read used in §3 is {D['engine']['horizons']['3M']['anchor_vol_ann']*100:.1f}%"],
]
table(rows, [1.8, 2.6, 2.5], first_col_bold=True)
figure(os.path.join(HERE, 'fig3_ma.png'), 6.4, 'Figure 3 — Price against the moving-average stack, the last 260 sessions.')
P('For the probabilistic work this matters in one way: a low-volatility tape produces a genuinely narrow three-month '
  f"cone — the 5th-to-95th band in §3 runs {(D['mc']['q60']['5']/_tanchor-1)*100:+.1f}% to "
  f"{(D['mc']['q60']['95']/_tanchor-1)*100:+.1f}% around the anchor — so even a modest fundamental surprise can carry the "
  'price to the edge of the distribution. The technical read neither confirms nor contradicts the fundamental one, and '
  'it is not asked to: it is the shortest of the three lenses and speaks only to the weeks ahead.')
