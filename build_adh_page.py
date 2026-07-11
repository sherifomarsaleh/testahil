#!/usr/bin/env python3
# Build alphadhabi.html from extra.html (post-bugfix) with exact-string replacements.
import re, sys
s = open('extra.html').read()
orig = s
R = []
def rep(a, b, n=None):
    global s
    c = s.count(a)
    if c == 0:
        print('MISS:', a[:90]); sys.exit(1)
    if n and c != n:
        print(f'COUNT {c}!={n}:', a[:80]); sys.exit(1)
    s = s.replace(a, b)

# ---- head/meta/canonical -----------------------------------------------------
rep('<title>eXtra / United Electronics (4003) — is the stock worth it? | testahil?</title>',
    '<title>Alpha Dhabi Holding (ALPHADHABI) — is the stock worth it? | testahil?</title>')
rep('<meta name="description" content="Where could eXtra / United Electronics (TADAWUL:4003) be in 1–3 months? A plain-language read of the odds, a weighted fair value, plus the full valuation study and open Excel model.">',
    '<meta name="description" content="Where could Alpha Dhabi Holding (ADX:ALPHADHABI) be in 1–3 months? A plain-language read of the odds, a weighted fair value, plus the full valuation study and open Excel model.">')
rep('<meta property="og:title" content="eXtra (4003) — is it worth it? | testahil?">',
    '<meta property="og:title" content="Alpha Dhabi (ALPHADHABI) — is it worth it? | testahil?">')
rep('<meta property="og:description" content="Where could eXtra go in 1–3 months? Plain-language odds, a fair-value read, and the open model.">',
    '<meta property="og:description" content="Where could Alpha Dhabi go in 1–3 months? Plain-language odds, a fair-value read, and the open model.">')
rep('<meta name="twitter:title" content="eXtra (4003) — is it worth it? | testahil?">',
    '<meta name="twitter:title" content="Alpha Dhabi (ALPHADHABI) — is it worth it? | testahil?">')
rep('<meta name="twitter:description" content="Where could eXtra go in 1–3 months? Plain-language odds, a fair-value read, and the open model.">',
    '<meta name="twitter:description" content="Where could Alpha Dhabi go in 1–3 months? Plain-language odds, a fair-value read, and the open model.">')
for a, b in [('https://testahil.com/extra.html', 'https://testahil.com/alphadhabi.html'),
             ('https://testahil.com/ar/extra.html', 'https://testahil.com/ar/alphadhabi.html')]:
    s = s.replace(a, b)

# ---- JSON-LD ------------------------------------------------------------------
rep('"headline": "eXtra / United Electronics (4003) — Independent Valuation Study"',
    '"headline": "Alpha Dhabi Holding (ALPHADHABI) — Independent Valuation Study"')
rep('"description": "Where could eXtra / United Electronics (4003) trade in 1–3 months? A probability distribution, a weighted fair value, and the open model. Educational analysis, not investment advice."',
    '"description": "Where could Alpha Dhabi Holding (ALPHADHABI) trade in 1–3 months? A probability distribution, a weighted fair value, and the open model. Educational analysis, not investment advice."')
rep('"datePublished": "2026-07-09"', '"datePublished": "2026-07-10"')
rep('"dateModified": "2026-07-09"', '"dateModified": "2026-07-10"')
rep('"name": "United Electronics Company (eXtra)",\n        "tickerSymbol": "TADAWUL:4003"',
    '"name": "Alpha Dhabi Holding PJSC",\n        "tickerSymbol": "ADX:ALPHADHABI"')
rep('"name": "eXtra / United Electronics (4003)",', '"name": "Alpha Dhabi Holding (ALPHADHABI)",')
rep('"name": "What is the fair-value range for eXtra / United Electronics (4003)?"',
    '"name": "What is the fair-value range for Alpha Dhabi Holding (ALPHADHABI)?"')
rep('"text": "testahil publishes a probability distribution of where eXtra could trade over the next 1–3 months',
    '"text": "testahil publishes a probability distribution of where Alpha Dhabi could trade over the next 1–3 months')
rep('"name": "How is the eXtra valuation calculated?"', '"name": "How is the Alpha Dhabi valuation calculated?"')
# the FAQ method answer will have been fixed in extra.html's bugfix to a split-legs text; replace whatever is there now:
faq_pat = re.compile(r'("name": "How is the Alpha Dhabi valuation calculated\?",\s*"acceptedAnswer": \{\s*"@type": "Answer",\s*"text": ")[^"]*(")', re.S)
FAQ_ANS = ('The study values Alpha Dhabi as a holding company: the primary lens is a mark-to-market '
    'sum-of-the-parts NAV \u2014 the four listed stakes (Aldar, NMDC Group, PureHealth, NCTH) at exchange prices, '
    'Trojan Construction at its arm\u2019s-length ADQ transaction mark, and the rest of the parent\u2019s audited book '
    'at carrying value, less a 0\u201325% holdco discount \u2014 cross-checked by a consolidated FCFF DCF, a '
    'look-through P/E, and the stated AED 2 bn dividend policy, then expressed as a 50,000-path Monte Carlo '
    'probability distribution. Every assumption is visible and editable in the free Excel model.')
s = faq_pat.sub(lambda m: m.group(1)+FAQ_ANS+m.group(2), s, count=1)
rep('"name": "Does testahil recommend buying or selling eXtra?"',
    '"name": "Does testahil recommend buying or selling Alpha Dhabi?"')
rep('"name": "Is the eXtra model free to download?"', '"name": "Is the Alpha Dhabi model free to download?"')
rep('"text": "Yes. The full eXtra valuation study (Word/PDF) and the open Excel model are free to download, with every assumption editable."',
    '"text": "Yes. The full Alpha Dhabi valuation study (Word/PDF) and the open Excel model are free to download, with every assumption editable."')

# ---- nav / hero ----------------------------------------------------------------
rep('<a href="ar/extra.html" class="lang-ar"', '<a href="ar/alphadhabi.html" class="lang-ar"')
rep('<span class="chip num">TADAWUL:4003</span>', '<span class="chip num">ADX:ALPHADHABI</span>')
rep('<h1 style="font-size:var(--fs-h1);margin-top:.4em">eXtra <span style="font-weight:400;font-size:.6em;opacity:.7">United Electronics</span></h1>',
    '<h1 style="font-size:var(--fs-h1);margin-top:.4em">Alpha Dhabi <span style="font-weight:400;font-size:.6em;opacity:.7">Alpha Dhabi Holding PJSC</span></h1>')
rep('Latest <b class="num" id="spot"></b> SAR (<span id="spotdate"></span>) · our weighted fair value <b class="num">81</b> · scenarios <span class="num">66</span> (cautious) to <span class="num">92</span> (all goes right).',
    'Latest <b class="num" id="spot"></b> AED (<span id="spotdate"></span>) · our weighted fair value <b class="num">7.30</b> · scenarios <span class="num">6.08</span> (cautious) to <span class="num">8.82</span> (all goes right).')

# ---- fundamental lens sub + plain terms ----------------------------------------
rep('<p class="lens-sub">Built up split-legs — a retail cash-flow (DCF) valuation plus the captive consumer-finance book — and cross-checked against relative multiples — <em>what is it worth?</em></p>',
    '<p class="lens-sub">Built as a mark-to-market sum-of-the-parts NAV — the listed stakes at exchange prices plus Trojan at its transaction mark — cross-checked against a consolidated DCF, look-through multiples and the stated dividend policy — <em>what is it worth?</em></p>')
plain_old = s[s.find('<b>In plain terms:</b>'):]
plain_old = plain_old[:plain_old.find('</p>')]
plain_new = ('<b>In plain terms:</b> Alpha Dhabi is a holding company, so we price what it owns. Four of its five biggest '
    'assets trade on the ADX every day — 31.6% of Aldar (worth AED 20.5 bn at market), 76.7% of NMDC Group (14.4 bn), '
    '35.1% of PureHealth (8.6 bn) and 73.7% of NCTH (2.4 bn) — and the fifth, 51% of Trojan Construction, was priced by a '
    'real transaction when ADQ bought the other 49%. Add the rest of the audited book at carrying value and the whole '
    'holding is worth about AED 7.44 a share before any holdco discount, or ~6.32 at a standard 15% discount. The market '
    'pays AED 8.22 — a premium of roughly 10% over the undiscounted parts, which is the entire debate: it is a bet that '
    'the IHC deal pipeline and the fair-value-gain engine keep compounding book value faster than you could yourself. A '
    'consolidated cash-flow model says ~11.7 is possible once the working-capital build normalizes (we weight that lightly '
    '— it is a ceiling, not an anchor), look-through earnings say ~8.1, and the stated AED 2 bn dividend policy discounts '
    'to just ~4.6. The weighted central is ~7.30, about 11% below spot, after a year in which the shares already fell 33% '
    'and touched 6.84 during the spring Gulf war — which remains the live tail under every number on this page.')
s = s.replace(plain_old, plain_new)

# ---- mc-lab: legend / verdict / zones / constants ------------------------------
rep('technical support 65.0</span>', 'technical support 7.40</span>')
rep('technical resistance 73.4</span>', 'technical resistance 8.84</span>')
rep('below technical support (65.0)', 'below technical support (7.40)')
rep('at or above technical resistance (73.4)', 'at or above technical resistance (8.84)')
rep('<span class="mc-big" id="mc-vMed">SAR 67.60</span>', '<span class="mc-big" id="mc-vMed">AED 8.30</span>')
rep('<span class="mc-big" id="mc-vRange">53 – 86</span>', '<span class="mc-big" id="mc-vRange">6.3 – 10.9</span>')
rep('</i> below 65.0</span>', '</i> below 7.40</span>')
rep('</i> 65.0 – 68.1</span>', '</i> 7.40 – 8.22</span>')
rep('</i> 68.1 – 73.4</span>', '</i> 8.22 – 8.84</span>')
rep('</i> ≥ 73.4</span>', '</i> ≥ 8.84</span>')
rep('var H=60, BETA=0.5826, FLOOR=65.00, R2=68.10, TARGET=73.40;',
    'var H=60, BETA=0.5826, FLOOR=7.40, R2=8.22, TARGET=8.84;')
rep('var LADDER_UP=[71.51,74.91,78.32], LADDER_DN=[64.70,61.29,57.89];',
    'var LADDER_UP=[8.63,9.04,9.45], LADDER_DN=[7.81,7.40,6.99];')
rep('try{ if(typeof TICKERS!=="undefined" && TICKERS && TICKERS.EXTRA){ T=TICKERS.EXTRA; } }catch(e){}',
    'try{ if(typeof TICKERS!=="undefined" && TICKERS && TICKERS.ALPHADHABI){ T=TICKERS.ALPHADHABI; } }catch(e){}')
rep('var S0=(T&&typeof T.spot==="number")?T.spot:24.00;', 'var S0=(T&&typeof T.spot==="number")?T.spot:8.22;')
rep('var fmt=function(v){return "SAR "+(Math.round(v*100)/100).toFixed(2);};',
    'var fmt=function(v){return "AED "+(Math.round(v*100)/100).toFixed(2);};')
rep('<div class="mc-card-h"><h4>Percentiles (SAR/share)</h4></div>', '<div class="mc-card-h"><h4>Percentiles (AED/share)</h4></div>')

# calibration constants → ADH (baseline mu3=+0.00915, var3=0.02772 at H=60; matches sig60 0.1665 / carry 0.92% published)
rep('var CONT_FIXED=[["Deposits",-0.002,0.015],["TASI",0.0045,0.027],["Liquidity",-0.002,0.015],["CoR",-0.0005,0.012]];',
    'var CONT_FIXED=[["NMDC",-0.004,0.038],["Tax",-0.001,0.010],["OilFiscal",0.008,0.034],["Flows",0.0025,0.025]];')
rep('var IDIO=0.0174, EGP_VOL=0.042, AICAP_VOL=0.023, INR_VOL=0.023;',
    'var IDIO=0.127, EGP_VOL=0.040, AICAP_VOL=0.030, INR_VOL=0.028;')
rep('var EV_FIXED=[["earn",0.5,0.0118,0.031],["fed",0.3,-0.006,0.031],["cor",0.25,-0.02,0.031],["oil",0.25,-0.028,0.038],["projfin",0.3,0.014,0.031],["index",0.3,0.014,0.023],["capital",0.2,0.008,0.023]];',
    'var EV_FIXED=[["earn",0.5,0.012,0.045],["split",0.5,0.006,0.028],["fed",0.3,-0.006,0.030],["rpt",0.25,0.014,0.050],["nmdcprov",0.3,-0.014,0.040]];')
rep('var GEO_MEAN=-0.07, GEO_SD=0.038, LNCH_MEAN=0.01, LNCH_SD=0.018;',
    'var GEO_MEAN=-0.085, GEO_SD=0.045, LNCH_MEAN=0.018, LNCH_SD=0.02;')

# ---- the five levers -----------------------------------------------------------
rep('<label for="mc-egp"><span class="mc-name">SAMA / Fed policy-rate path (demand + Tasheel spread)</span><span class="mc-val" id="mc-egpVal">+0.1% / quarter</span></label>',
    '<label for="mc-egp"><span class="mc-name">Fed / CBUAE policy-rate path (the peg imports it)</span><span class="mc-val" id="mc-egpVal">+0.1% / quarter</span></label>')
rep('<p class="mc-chan">The dominant driver. eXtra is doubly geared to the SAMA policy rate (which shadows the Fed to defend the riyal peg): rate cuts lift financed big-ticket demand at the tills and widen Tasheel\'s lending spread at the same time, while a higher-for-longer path softens demand and compresses the spread together.</p>',
    '<p class="mc-chan">The dirham peg imports every Fed move through the CBUAE base rate: cuts lower the carry anchor, the group\u2019s funding cost and the discount rate on every marked stake at once; a higher-for-longer path does the reverse. The 3M EIBOR (3.93%) is the drift anchor of the published engine.</p>')
rep('<label for="mc-geo"><span class="mc-name">Consumer / regional demand shock — probability</span><span class="mc-val" id="mc-geoVal">15% · −7% if it hits</span></label>',
    '<label for="mc-geo"><span class="mc-name">Gulf-war stress — probability</span><span class="mc-val" id="mc-geoVal">25% · −8.5% if it hits</span></label>')
rep('<input type="range" id="mc-geo" min="-60" max="-5" step="1" value="-15">',
    '<input type="range" id="mc-geo" min="-60" max="-5" step="1" value="-25">')
rep('<p class="mc-chan">A one-off downside shock — a sharp consumer pullback, a regional escalation, or a spike in Tasheel\'s provisioning — that de-rates the stock. The main near-term downside for a net-cash retailer already at a 52-week low.</p>',
    '<p class="mc-chan">The dominant tail. A renewed Iran-war escalation hits all four ADX stake marks, Gulf logistics (NMDC\u2019s marine works, Trojan\u2019s sites) and the oil-fiscal pulse behind Abu Dhabi\u2019s pipeline simultaneously — the March trough (AED 6.84) shows the mechanism. The 7–8 Jul ceasefire collapse post-dates the price data; this slider is where you price it.</p>')
rep('<label for="mc-lnch"><span class="mc-name">Dividend declaration surprise — probability</span><span class="mc-val" id="mc-lnchVal">30% · +1.0% if it lands</span></label>',
    '<label for="mc-lnch"><span class="mc-name">Buyback / distribution support — probability</span><span class="mc-val" id="mc-lnchVal">35% · +1.8% if it lands</span></label>')
rep('<input type="range" id="mc-lnch" min="0" max="90" step="1" value="30">',
    '<input type="range" id="mc-lnch" min="0" max="90" step="1" value="35">')
rep('<p class="mc-chan">eXtra pays a well-covered ~7% yield (payout ~76%). A maintained or raised dividend confirms the yield floor that supports the price at these lows; a cut would remove it.</p>',
    '<p class="mc-chan">A running buyback in a thin float (IHC holds ~87%) is a mechanical support, and the GA-approved policy (AED 2 bn +5%/yr) is a floor signal. Visible repurchase pace or an early-declared FY26 distribution lands as a positive event; a policy breach would remove the floor.</p>')
rep('<label for="mc-aicap"><span class="mc-name">Non-oil GDP &amp; Vision-2030 consumption</span><span class="mc-val" id="mc-aicapVal">+0.3% / quarter</span></label>',
    '<label for="mc-aicap"><span class="mc-name">Abu Dhabi property &amp; Aldar momentum</span><span class="mc-val" id="mc-aicapVal">+0.7% / quarter</span></label>')
rep('<input type="range" id="mc-aicap" min="-5" max="8" step="0.5" value="0.3">',
    '<input type="range" id="mc-aicap" min="-5" max="8" step="0.1" value="0.7">')
rep('<p class="mc-chan">The structural tailwind: rising household income, e-commerce penetration and Vision-2030 spending lift big-ticket electronics demand — and push informal consumer credit into regulated finance, which feeds Tasheel.</p>',
    '<p class="mc-chan">Aldar is 28% of marked NAV and the group\u2019s biggest profit engine (record FY25, AED 71.7 bn backlog; Abu Dhabi deals +43% in 9M-25). Its tape is the single largest continuous force on Alpha Dhabi\u2019s — this lever tilts it.</p>')
rep('<label for="mc-krw"><span class="mc-name">Consumer-finance regulation &amp; provisioning</span><span class="mc-val" id="mc-krwVal">+0.1% / quarter</span></label>',
    '<label for="mc-krw"><span class="mc-name">IHC deal flow &amp; the FV-gain engine</span><span class="mc-val" id="mc-krwVal">+0.4% / quarter</span></label>')
rep('<input type="range" id="mc-krw" min="-6" max="8" step="0.5" value="0.1">',
    '<input type="range" id="mc-krw" min="-6" max="8" step="0.1" value="0.4">')
rep('<p class="mc-chan">SAMA finance-company rules and the provisioning cycle drive the Tasheel leg — the recent ~20% dip in consumer-finance profit was provisioning, not demand. Tighter rules compress the finance spread; a benign regime lets it earn its ~19% ROE.</p>',
    '<p class="mc-chan">The premium\u2019s engine: ecosystem transactions (the NMDC buy-up, the NCTH injection) and fair-value gains (+AED 3.2 bn in FY25) are what compound the book above the marks. Deals landing at fair prices push this up; a related-party injection at rich marks, or a quiet quarter, pulls it down.</p>')
rep("el(\"mc-reset\").addEventListener(\"click\",function(){egp.value=\"0.1\"; aicap.value=\"0.3\"; krw.value=\"0.1\"; geo.value=\"-15\"; lnch.value=\"30\"; setHz(60); render();});",
    "el(\"mc-reset\").addEventListener(\"click\",function(){egp.value=\"0.1\"; aicap.value=\"0.7\"; krw.value=\"0.4\"; geo.value=\"-25\"; lnch.value=\"35\"; setHz(60); render();});")

# ---- lenses table + chart levels + drives-the-odds -----------------------------
rep('''        <tr><td>Split-legs sum-of-the-parts — primary</td><td class="num">90</td><td class="num">50%</td></tr>
        <tr><td>&nbsp;&nbsp;· Retail operating-co DCF (net-cash)</td><td class="num">65</td><td class="num">—</td></tr>
        <tr><td>&nbsp;&nbsp;· Tasheel — captive finance (68.75%)</td><td class="num">25</td><td class="num">—</td></tr>
        <tr><td>Relative multiples (P/E 12×)</td><td class="num">75</td><td class="num">25%</td></tr>
        <tr><td>Monte-Carlo — T+60 median</td><td class="num">68</td><td class="num">25%</td></tr>
        <tr style="font-weight:700"><td>Weighted central fair value</td><td class="num">81</td><td class="num">+19% vs spot</td></tr>''',
    '''        <tr><td>Sum-of-the-parts NAV — primary (15% holdco discount)</td><td class="num">6.32</td><td class="num">45%</td></tr>
        <tr><td>&nbsp;&nbsp;· Marked NAV at par (0% discount)</td><td class="num">7.44</td><td class="num">—</td></tr>
        <tr><td>Consolidated FCFF DCF (the ceiling)</td><td class="num">11.72</td><td class="num">15%</td></tr>
        <tr><td>Look-through relative (P/E 9.5×)</td><td class="num">8.07</td><td class="num">25%</td></tr>
        <tr><td>Dividend policy, discounted (DDM)</td><td class="num">4.55</td><td class="num">15%</td></tr>
        <tr style="font-weight:700"><td>Weighted central fair value</td><td class="num">7.30</td><td class="num">−11% vs spot</td></tr>''')
rep('<th class="num">Per share (SAR)</th>', '<th class="num">Per share (AED)</th>')
rep('<p class="muted" style="margin-top:8px">The lenses span SAR 66 (weighted cautious) to SAR 92 (weighted bull). The sum-of-the-parts is the primary read — a net-cash retail DCF plus the captive consumer-finance book taken at eXtra\'s 68.75% — and the whole gap to spot turns on the retail discount rate (a short-window beta of 0.55 vs a conservative 0.80) and the multiple placed on Tasheel. Full detail is in the study and the open model.</p>',
    '<p class="muted" style="margin-top:8px">The lenses span AED 6.08 (weighted cautious) to 8.82 (weighted bull). The sum-of-the-parts is the primary read — the four listed stakes at exchange prices, Trojan at the AED 4,997 mn ADQ actually paid for 49%, and the residual audited book at carrying value — and the whole debate is the premium: spot sits ~10% above even the undiscounted NAV of 7.44. The DCF\u2019s 11.72 is a multi-year ceiling (80% terminal value, working-capital absorption still heavy) weighted at just 15%. Full detail is in the study and the open model.</p>')
rep('<td class="num">73.4 · 76.7 · 79.7</td>', '<td class="num">8.50 · 8.84 · 9.50</td>')
rep('<td class="num">68.1 · 65.0 · 62.0</td>', '<td class="num">7.80 · 7.40 · 6.84</td>')
rep('<td class="num">~2.0%</td>', '<td class="num">~2.1%</td>')
rep('<td class="num">~66 (weighted bear)</td>', '<td class="num">~6.08 (weighted bear)</td>')
rep('<p class="muted">50,000 paths, carry-anchored: the drift is the SAMA/Fed rate path against eXtra\'s ~7% dividend yield (the two are close, so the median is an explained flat), with the spread set by the Saudi-panel-fitted regime width. The forces the study reasons through are the rate path (financed demand + Tasheel\'s funding spread), non-oil GDP &amp; Vision-2030 consumption, consumer-finance provisioning &amp; regulation, e-commerce competition, the dividend signal, foreign flows and a momentum/mean-reversion tilt — plus event forces: a quarterly earnings surprise, a SAMA policy surprise, a dividend declaration, a provisioning/regulatory change and a regional event. Details in the <a href="method.html">methodology</a>.</p>',
    '<p class="muted">50,000 paths, carry-anchored: the drift is the 3M EIBOR (3.93%) with no ex-dividend date inside the window (the FY25 distribution was paid in Q1; the next lands ~Q1-27), so the median drifts gently up; the spread is the share\u2019s own gap-aware volatility (annualized ~34%) after a provisional single-name UAE calibration — honestly flagged as provisional until a multi-name ADX panel exists. The forces the study reasons through are the Fed/CBUAE rate path, Abu Dhabi property &amp; Aldar\u2019s tape, IHC deal flow and the fair-value-gain engine, NMDC\u2019s normalization, the DMTT tax glide, oil and the fiscal pulse, float/index mechanics — plus event forces: the Q2 results and the missing attributable split, a related-party transaction, a Fed surprise, buyback/distribution news, and the war regime itself. One honest caveat, stated in the study twice: the width was fitted through 3 Jul — a pre-re-escalation regime — so read the downside percentiles as floors on risk, not ceilings. Details in the <a href="method.html">methodology</a>.</p>')

# ---- competitive map -----------------------------------------------------------
rep('<p class="qhead">Where eXtra sits in its markets</p>', '<p class="qhead">Where Alpha Dhabi sits in its complex</p>')
rep('<p class="muted">eXtra is Saudi Arabia\'s largest organised electronics &amp; appliances retailer, defended by breadth, omnichannel and — decisively — embedded finance: by lending to its own big-ticket buyers through Tasheel it captures a high-return spread that pure retailers and online marketplaces cannot. This is a competitive map, not a price table.</p>',
    '<p class="muted">Alpha Dhabi is Abu Dhabi\u2019s second-largest listed investment holding — the mid-layer of the IHC ecosystem, above its own listed stakes and below the parent. Its moat is positional: proximity to the state-linked project pipeline, first-call capital, and board control of franchise assets. This is a structural map, not a price table.</p>')
rep('''      <table><thead><tr><th>Arena</th><th>eXtra's position</th><th>Main rivals</th></tr></thead>
      <tbody>
        <tr><td>Electronics &amp; appliances retail</td><td class="num">Category leader (KSA)</td><td>Jarir · online (noon, Amazon.sa)</td></tr>
        <tr><td>Embedded consumer finance</td><td class="num">Yes — Tasheel (68.75%)</td><td>Jarir limited · marketplaces none</td></tr>
        <tr><td>Trailing P/E</td><td class="num">~11× (at a 52-wk low)</td><td>Jarir ~18.5× — a ~40% discount</td></tr>
        <tr><td>Dividend yield</td><td class="num">~6.9% (payout ~76%)</td><td>Jarir ~5.4%</td></tr>
        <tr><td>Blended net margin</td><td class="num">~7% (thin retail + finance spread)</td><td>Jarir ~9% (richer mix)</td></tr>
        <tr><td>Finance share of profit</td><td class="num">~half of group NI on ~7% of revenue</td><td>structural differentiator</td></tr>
      </tbody></table>''',
    '''      <table><thead><tr><th>Layer / lens</th><th>Alpha Dhabi</th><th>Context</th></tr></thead>
      <tbody>
        <tr><td>Marked NAV vs price</td><td class="num">Spot ~+10% ABOVE par NAV (7.44)</td><td>GCC/EM holdcos usually trade at a 10–25% discount</td></tr>
        <tr><td>Largest stake — Aldar (31.63%)</td><td class="num">AED 20.5 bn · 8.6× trailing</td><td>Cheaper bought directly than through the wrapper (10.3×)</td></tr>
        <tr><td>NMDC Group (76.68%)</td><td class="num">AED 14.4 bn · 5.2×</td><td>Q1-26 EPS halved — the fragile earnings line</td></tr>
        <tr><td>PureHealth (35.06%) · NCTH (73.73%)</td><td class="num">AED 8.6 bn · 2.4 bn</td><td>12.3× associate · thin-float hotel platform</td></tr>
        <tr><td>Trojan Construction (51%)</td><td class="num">AED 5.2 bn (ADQ mark)</td><td>#1 UAE contractor; ALEC (DFM) and Orascom active</td></tr>
        <tr><td>Parent — IHC (~87%)</td><td class="num">Thin float, buyback running</td><td>IHC itself trades at a large, persistent NAV premium</td></tr>
      </tbody></table>''')
rep('<p class="muted" style="margin-top:10px">The debate is whether the market is right to price eXtra as a plain cyclical retailer at ~11× — giving no credit to the captive lender — or whether the split-legs value (retail DCF + Tasheel) near ~SAR 90 is closer to the truth. Competitive map, not advice.</p>',
    '<p class="muted" style="margin-top:10px">The debate is whether the market is right to pay a ~10% premium over marked NAV for the IHC ecosystem\u2019s deal flow and fair-value-gain engine — after two straight years of falling attributable EPS — or whether the price completes its trip toward the marks (6.3–7.4 depending on the discount). Structural map, not advice.</p>')

# ---- forms / share / edition / aside / related ---------------------------------
rep('value="Attack on the model — eXtra (4003), 10 Jul 2026 edition"', 'value="Attack on the model — Alpha Dhabi (ALPHADHABI), 10 Jul 2026 edition"')
rep('value="eXtra (4003) — 10 Jul 2026 edition"', 'value="Alpha Dhabi (ALPHADHABI) — 10 Jul 2026 edition"')
rep('<input type="hidden" name="stock" value="EXTRA">', '<input type="hidden" name="stock" value="ALPHADHABI">')
rep('data-share="See the odds on eXtra — testahil"', 'data-share="See the odds on Alpha Dhabi — testahil"')
rep('Edition: 09 Jul 2026.', 'Edition: 10 Jul 2026.')
rep('<p class="ss-h">Get the next eXtra update</p>', '<p class="ss-h">Get the next Alpha Dhabi update</p>')
rep('<div id="related" data-ticker="EXTRA"></div>', '<div id="related" data-ticker="ALPHADHABI"></div>')
rep('<a class="ctx-btn" href="compare.html?a=EXTRA">Compare eXtra vs peers &rarr;</a>', '<a class="ctx-btn" href="compare.html?a=ALPHADHABI">Compare Alpha Dhabi vs peers &rarr;</a>')
rep('const T=TICKERS.EXTRA;', 'const T=TICKERS.ALPHADHABI;')
rep('/* peers rendered statically for eXtra */', '/* peers rendered statically for Alpha Dhabi */')

open('alphadhabi.html', 'w').write(s)
print('alphadhabi.html written,', len(s), 'bytes; residual eXtra mentions:', s.count('eXtra'), '| EXTRA:', s.count('EXTRA'), '| SAR:', s.count('SAR'))
