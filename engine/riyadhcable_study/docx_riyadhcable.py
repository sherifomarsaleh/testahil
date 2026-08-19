"""Riyadh Cables Group Company (Tadawul: 4142) — 16-section valuation study, TMPV house
style. Imports the shared base (doc + helpers), builds all sections, saves the .docx.
Written for an external reader: no internal-procedure vocabulary; calibration evidence is
plain-language in the price-map section; experts are Expert 1/2/3."""
import json, os
from docx_base import (doc, P, rich, H1, H2, caption, bullet, table, figure, box, masthead,
                       INK, GREY, BRASS, GOLD, WHITE)
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, 'study_numbers.json')))
SRC = json.load(open(os.path.join(HERE, 'source_financials.json')))
M, HI, HB, F = D['meta'], D['hist_is'], D['hist_bs'], D['fcst']
W, DCF, LN, SN = D['wacc'], D['dcf'], D['lenses'], D['sens']
REL, NRM, BKL, EXPP = D['rel'], D['norm'], D['book'], D['experts']
SEG, S0, STK, BT, TR = D['seg_fy25'], D['step0'], D['strike'], D['backtest'], D['terminal_recon']
IN = {k: v['value'] for k, v in D['inputs'].items()}
SPOT, SH = M['spot'], M['shares_mn']
H3 = STK['horizons']['3M']; H1H = STK['horizons']['1M']
ITM = D['interim']
BETA_OLS = json.load(open(os.path.join(HERE, 'beta_result.json')))['ols_crosscheck']

# section 2's technical sentences are COMPUTED from the price library — never hand-authored
# (the first edition hand-wrote "sits near its longer moving averages" while the price sat
# below all four averages; standing computed-technicals rule)
import pandas as _pd
_px = _pd.read_csv(os.path.join(HERE, '..', 'raw_ohlc', 'SA', 'RIYADHCABLE.csv'))
_px['Date'] = _pd.to_datetime(_px['Date'])
_px = _px.sort_values('Date')
_close = _px['Price'].astype(float)
SMA = {w: float(_close.rolling(w).mean().iloc[-1]) for w in (20, 50, 100, 200)}
LO52 = float(_close.tail(252).min()); HI52 = float(_close.tail(252).max())
assert abs(float(_close.iloc[-1]) - SPOT) < 0.01, 'library close does not match the anchor spot'
_below = [w for w in (20, 50, 100, 200) if SPOT < SMA[w]]
_stack_state = ('below all four of its moving averages' if len(_below) == 4 else
                'above all four of its moving averages' if not _below else
                f'below its {", ".join(str(w) for w in sorted(_below))}-session averages')


def sar(x, d=0):
    return f'{x:,.{d}f}'


def pct(x, d=1):
    return f'{x*100:.{d}f}%'


# ============ 1 MASTHEAD + READ FIRST ========================================
masthead()
P('Riyadh Cables Group Company', size=22, bold=True, space_after=1)
P('Tadawul: 4142  ·  Capital Goods — Electrical Equipment (wire & cable)  ·  Saudi Arabia',
  size=11, color=GREY, space_after=8)
rich([('Fair-value range (weighted central) ', {'bold': True}),
      (f'SAR {sar(LN["central"]["base"],0)} per share', {'bold': True, 'color': BRASS, 'size': 13}),
      (f'   ·   full span SAR {sar(D["span"][0],0)}–{sar(D["span"][1],0)}   ·   spot SAR {sar(SPOT,2)} '
       f'({pct(LN["central"]["base"]/SPOT-1,0)} to the central)', {'color': INK})], size=11, space_after=8)
box([('READ FIRST.  ', 'This is an independent, educational valuation study. It is not investment advice, '
      'not a recommendation, and not a price target. Every figure is a model output shown as a range, '
      'built only from Riyadh Cables’ own audited financial statements and its filed results. '
      'A companion workbook carries the full model; a companion bibliography lists every source.'),
     ('What the number means.  ', f'The four valuation lenses below place fair value between about SAR '
      f'{sar(min(LN[k]["base"] for k in ["dcf","relative","normalized","book"]),0)} and SAR '
      f'{sar(max(LN[k]["base"] for k in ["dcf","relative","normalized","book"]),0)} per share; weighting '
      f'them gives a central of SAR {sar(LN["central"]["base"],0)}, about {pct(LN["central"]["base"]/SPOT-1,0)} '
      f'above the SAR {sar(SPOT,2)} market price. The lenses disagree, and that disagreement is the point: '
      f'the intrinsic cash-flow lens sees clear value, the exit-multiple lens is more cautious.'),
     ('The one thing to watch.  ', 'Riyadh Cables is a metal converter — copper and aluminium are about '
      '95% of its cost of sales. Its gross margin is therefore an OUTPUT of the metal price, not a stable '
      'input. The study’s central judgement is the margin the business holds now that the 2024–25 '
      'metal tailwind has passed; it is anchored on the most recent reviewed half-year (15.3%) and shown '
      'both ways against the higher full-year 2025 print.')])

# ============ 2 HEADLINE ======================================================
H1('Headline')
P(f'Riyadh Cables is the largest Saudi manufacturer of electrical cables and wire. Revenue has grown '
  f'from SAR {sar(HI["FY23"]["rev"]/1000,1)}bn in 2023 to SAR {sar(HI["FY25"]["rev"]/1000,1)}bn in 2025 '
  f'(a {pct((HI["FY25"]["rev"]/HI["FY23"]["rev"])**0.5-1,0)} annual pace), and net profit has doubled to '
  f'SAR {sar(HI["FY25"]["pat"]/1000,2)}bn, as gross margin climbed from {pct(HI["FY23"]["gp"]/HI["FY23"]["rev"])} '
  f'to {pct(HI["FY25"]["gp"]/HI["FY25"]["rev"])}. Part of the 2025 step-up is acquired rather than organic: '
  f'Qatar Cables moved from a 50% associate to a wholly-owned subsidiary in April 2025, and a 51% stake in '
  f'Artikul Aziya Kabel (Uzbekistan) was added late in 2025. The company is lightly geared — net financial '
  f'debt of about SAR {sar(DCF["nd"],0)}mn is a fraction of its SAR {sar(M["mktcap"]/1000,1)}bn market value — '
  f'earns a return on equity of about {pct(BKL["roe_trailing"],0)} (a return on invested capital of about '
  f'{pct(TR["hist_roic25"],0)}), and paid out {pct(0.554,0)} of its 2025 earnings.')
P(f'Our central fair-value estimate is SAR {sar(LN["central"]["base"],0)} per share, about '
  f'{pct(LN["central"]["base"]/SPOT-1,0)} above the SAR {sar(SPOT,2)} price. The intrinsic discounted-cash-flow '
  f'lens is the most positive at SAR {sar(LN["dcf"]["base"],0)}; a cautious exit-multiple reading is the least, '
  f'at SAR {sar(LN["relative"]["base"],0)}; the earnings-power and book-value lenses sit in between at SAR '
  f'{sar(LN["normalized"]["base"],0)} and SAR {sar(LN["book"]["base"],0)}. The single most important assumption '
  f'is the sustained gross margin: at the recent half-year’s 15.3% the cash-flow lens is worth SAR '
  f'{sar(DCF["spread_base"],0)}; if the 2025 full-year 16.0% holds it is worth SAR {sar(DCF["spread_bull"],0)}; '
  f'if it compresses to 14.5% it is worth SAR {sar(DCF["spread_bear"],0)}.')
figure(os.path.join(HERE, 'fig1_football.png'), 6.9,
       'Figure 1. Valuation football field — the bear-to-bull span of each lens; the brass tick is the base '
       'case; the vertical line is the market price.')

# ============ 3 VALUATION SUMMARY — every read at a glance =====================
H1('Valuation summary — every read at a glance')
rows = [['Lens', 'Bear', 'Base', 'Bull', 'Weight', 'vs spot']]
for k in ['dcf', 'relative', 'normalized', 'book']:
    l = LN[k]
    rows.append([l['name'], sar(l['bear'], 0), sar(l['base'], 0), sar(l['bull'], 0), pct(l['w'], 0),
                 pct(l['base'] / SPOT - 1, 0)])
rows.append(['Weighted central', sar(LN['central']['bear'], 0), sar(LN['central']['base'], 0),
             sar(LN['central']['bull'], 0), '100%', pct(LN['central']['base'] / SPOT - 1, 0)])
rows.append(['Expert panel median', '', sar(D['panel_centre'], 0), '', '', pct(D['panel_centre'] / SPOT - 1, 0)])
rows.append(['Market price (anchor)', '', sar(SPOT, 2), '', '', '—'])
table(rows, [1.9, 0.85, 0.85, 0.85, 0.8, 0.95], band_rows={5}, size=9.4)
rich([('Terminal value as a share of the discounted-cash-flow enterprise value: ', {}),
      (f'{pct(DCF["tv_share"],0)}', {'bold': True, 'color': BRASS}),
      ('.  Enterprise value / EBITDA ', {}),
      (f'{REL["ev_ebitda_trailing"]:.1f}x', {'bold': True}),
      (f' and price / earnings {REL["pe_trailing"]:.1f}x on the FY2025 accounts ({ITM["pe_ttm"]:.1f}x on '
       f'trailing-twelve-month earnings). Cost of capital {pct(W["wacc"],1)} today, easing to '
       f'{pct(W["wacc_term"],1)} in perpetuity.', {})], size=9.6, space_after=8)
box([('The contested judgement, both ways.  ', f'The sustained gross margin drives the cash-flow lens more '
      f'than any other input. Anchored on the reviewed H1-2026 actual of {pct(IN["spread_anchor"],1)}: '
      f'SAR {sar(DCF["spread_base"],0)}/share. On the 2025 full-year 16.0%: SAR {sar(DCF["spread_bull"],0)}. On '
      f'a further compression to 14.5%: SAR {sar(DCF["spread_bear"],0)}. We publish the three side by side and '
      f'do not average them into one number.')])

# ============ 4 COMPANY OVERVIEW ==============================================
H1('Company overview')
P(f'Riyadh Cables Group Company is a Saudi joint-stock company founded in 1984 and listed on the Saudi '
  f'Exchange (Tadawul) in December 2022. It manufactures low-, medium-, high- and extra-high-voltage power '
  f'cables, building wire, and telecommunications cable, from plants in Riyadh’s industrial cities. It is '
  f'the largest cable maker in Saudi Arabia and a significant exporter into the wider Gulf.')
P(f'The business reports three segments. Cables and wire is by far the largest at SAR '
  f'{sar(SEG["rev"]["cables"]/1000,1)}bn, {pct(SEG["rev"]["cables"]/HI["FY25"]["rev"],0)} of 2025 revenue; '
  f'high-voltage turnkey projects add SAR {sar(SEG["rev"]["hv"],0)}mn ({pct(SEG["rev"]["hv"]/HI["FY25"]["rev"],1)}); '
  f'and other products — chiefly telephone cable and services — a further SAR {sar(SEG["rev"]["other"],0)}mn. '
  f'By destination, {pct(SEG["geo"]["ksa"]/HI["FY25"]["rev"],0)} of sales are inside Saudi Arabia and '
  f'{pct(SEG["geo"]["export"]/HI["FY25"]["rev"],0)} are exports, predominantly to the United Arab Emirates '
  f'(about SAR 2.2bn in 2025).')
P(f'Two corporate steps reshaped the perimeter recently and are named rather than blended away: on '
  f'17 April 2025 the group acquired the remaining 50% of Qatar Cables Company, consolidating a business it '
  f'had equity-accounted; and late in 2025 it acquired 51% of Artikul Aziya Kabel LLC in Uzbekistan — the '
  f'source of the SAR {sar(DCF["nci"],0)}mn non-controlling interest the value bridge deducts. An early-stage '
  f'memorandum of understanding on Syria was disclosed in 2026. The organic/acquired split of the 2025 '
  f'revenue step-up is not separately disclosed, and the study says so rather than estimating it.')
P(f'The balance sheet is that of a metal converter: inventory of copper and aluminium and a large trade-'
  f'receivables book (together about {pct((HB["FY25"]["inv"]+HB["FY25"]["recv"])/HI["FY25"]["rev"],0)} of revenue), '
  f'part-funded by trade payables and a supplier-finance facility, with only modest interest-bearing debt. '
  f'The company hedges copper, aluminium and lead through commodity forwards. It is not a bank, a developer or '
  f'a holding company; it is an operating manufacturer, and it is valued as one — a discounted-cash-flow model '
  f'first, cross-checked against multiples, earnings power and book value.')

# ============ 5 SECTION 1 FUNDAMENTAL VALUATION ===============================
H1('1  Fundamental valuation')
H2('1.1  Cash-flow model — the free-cash-flow waterfall and the value bridge')
P('The primary lens is a five-year discounted cash flow to the firm. Operating profit is taxed at a forward '
  f'blended zakat-and-income-tax rate of {pct(IN["tax_eff"],1)} — set just above the audited 2025 effective '
  f'rate of 9.0% for the growing foreign share of profits; at the 2025 actual rate the lens would be about '
  f'half a percent higher. Depreciation is added back, and capital expenditure and the investment in working '
  f'capital are subtracted, to give free cash flow to the firm. Each year is discounted at its own cost of '
  f'capital, gliding from {pct(W["wacc"],1)} to {pct(W["wacc_term"],1)}. Discounting is year-end with annual '
  f'compounding (a mid-year convention would raise this lens by roughly 4%), and every lens in this study is '
  f'stated at 31-Dec-2025 and then rolled 230 days to the 18-Aug-2026 anchor at the cost of equity, less the '
  f'SAR {IN["div_window"]:.2f} dividend paid in May 2026 — the same roll the bridge below shows explicitly.')
wf = [['SAR mn', *[y for y in F['years']]]]
for lbl, key, d in [('Revenue', 'rev', 0), ('EBITDA', 'ebitda', 0), ('  EBITDA margin', 'ebitda_margin', None),
                    ('Depreciation & amortisation', 'dna', 0), ('EBIT', 'ebit', 0), ('NOPAT (EBIT×(1−t))', 'nopat', 0),
                    ('  + Depreciation & amortisation', 'dna', 0), ('  − Capital expenditure', 'capex', 0),
                    ('  − Change in working capital', 'dnwc', 0), ('Free cash flow to firm', 'fcff', 0),
                    ('Discount factor', 'df', None), ('PV of FCFF', 'pv', 0)]:
    if key == 'ebitda_margin':
        wf.append([lbl] + [pct(F[key][i]) for i in range(5)])
    elif key == 'df':
        wf.append([lbl] + [f'{F[key][i]:.4f}' for i in range(5)])
    else:
        vals = F[key]
        wf.append([lbl] + [sar(vals[i], 0) for i in range(5)])
table(wf, [2.15] + [0.98] * 5, size=8.6)
rich([('Sum of the present values of the five explicit years is SAR ', {}),
      (f'{sar(DCF["pv_explicit"],0)}mn', {'bold': True}),
      ('; the present value of the terminal value is SAR ', {}), (f'{sar(DCF["pv_tv"],0)}mn', {'bold': True}),
      (f' ({pct(DCF["tv_share"],0)} of enterprise value); together the enterprise value is SAR ', {}),
      (f'{sar(DCF["ev"],0)}mn', {'bold': True, 'color': BRASS}), ('.', {})], size=9.6)
br = [['Enterprise value to equity (SAR mn)', ''],
      ['Enterprise value', sar(DCF['ev'], 0)],
      [f'   of which terminal value ({pct(DCF["tv_share"],0)} of EV)', sar(DCF['pv_tv'], 0)],
      ['Less: net financial debt', sar(-DCF['nd'], 0)],
      ['Add: associates + non-operating assets', sar(DCF['assoc'] + DCF['nonop'], 0)],
      ['Less: non-controlling interests', sar(-DCF['nci'], 0)],
      ['Equity value attributable', sar(DCF['eq_attr'], 0)],
      ['Value per share at 31-Dec-2025 (SAR)', sar(DCF['ps_dec'], 2)],
      ['Rolled to the 18-Aug-2026 anchor, net of dividend (SAR)', sar(DCF['ps'], 2)]]
table(br, [4.6, 1.4], band_rows={6, 8}, size=9.2, align_right_from=1)
caption('The enterprise-to-equity bridge. The terminal-value share is shown on its own line, and again in the '
        'summary table and the companion workbook, where it is a live formula.')

H2('1.2  Book value and sustainable return')
P(f'Equity attributable to shareholders was SAR {sar(F["eqp_fy25"]/1000,2)}bn at end-2025, or SAR '
  f'{sar(BKL["bvps"],2)} per share. Trailing return on average equity is about {pct(BKL["roe_trailing"],0)} — '
  f'very high, but flattered by the 2024–25 metal tailwind and a large receivables book. We take a '
  f'sustainable return of {pct(IN["roe_sust"],0)}. Capitalised against a terminal cost of equity of '
  f'{pct(W["ke_term"],1)} and {pct(IN["g_term"],0)} growth, that supports a justified price-to-book of '
  f'{BKL["pb_just"]:.1f}x — SAR {sar(BKL["pb_just"]*BKL["bvps"],0)} at end-2025, SAR '
  f'{sar(LN["book"]["base"],0)} rolled to the anchor. One consistency is stated rather than hidden: '
  f'{pct(IN["roe_sust"],0)} sustainable return with {pct(IN["g_term"],0)} growth implies a terminal payout '
  f'near {pct(1-IN["g_term"]/IN["roe_sust"],0)}, above the {pct(F["payout"],0)} paid through the explicit '
  f'years — the lens prices the far steady state, where reinvestment needs fade, not the build-out decade. '
  f'The bear case discounts a lower return at the higher explicit-window cost of equity; the base and bull '
  f'use the terminal rate.')

H2('1.3  Relative multiples')
P(f'Riyadh Cables trades at about {REL["ev_ebitda_trailing"]:.1f}x enterprise value to EBITDA and '
  f'{REL["pe_trailing"]:.1f}x earnings on the 2025 accounts ({ITM["pe_ttm"]:.1f}x on trailing-twelve-month '
  f'earnings through June 2026 — the basis is labelled wherever a multiple appears). The global cable majors, '
  f'recomputed from their own market values and their own raised 2026 guidance at the study date, trade far '
  f'richer than the old rule of thumb: Prysmian about {IN["peer_prysmian_fwd"]:.0f}x forward EBITDA (guidance '
  f'raised 30-Jul-2026) and Nexans about {IN["peer_nexans_fwd"]:.1f}x, so the developed band runs roughly '
  f'8.5–14.5x; the fast-growing Indian names (Polycab, KEI) sit near {IN["peer_polycab_fwd"]:.0f}–'
  f'{IN["peer_kei_fwd"]:.0f}x on the next twelve months. We apply {IN["ev_ebitda_just"]:.1f}x to 2027 EBITDA '
  f'of SAR {sar(F["ebitda"][1],0)}mn — a deliberate discount to that band, not its mid-point, for a single-'
  f'country, single-customer-concentrated base — discount it at the year-two factor, add the interim cash '
  f'flows and roll to the anchor: SAR {sar(LN["relative"]["base"],0)} per share, still the most cautious lens.')

H2('1.4  Normalised earnings power')
P(f'Stripping cycle from the earnings, a mid-cycle EBITDA margin of {pct(NRM["margin"],1)} on current-scale '
  f'revenue of SAR {sar(NRM["rev"],0)}mn, after depreciation, financing and tax, yields normalised earnings of '
  f'about SAR {NRM["eps"]:.2f} per share. At a through-cycle {IN["pe_just"]:.0f}x — appropriate for a high-return, '
  f'low-leverage regional leader with a roughly {pct(W["ke"],0)} cost of equity — that is SAR '
  f'{sar(IN["pe_just"]*NRM["eps"],0)} at end-2025, SAR {sar(LN["normalized"]["base"],0)} rolled to the anchor.')

H2('1.5  Synthesis — four lenses, one field')
P(f'The four lenses span SAR {sar(min(LN[k]["base"] for k in ["dcf","relative","normalized","book"]),0)} to SAR '
  f'{sar(max(LN[k]["base"] for k in ["dcf","relative","normalized","book"]),0)}. We weight the discounted cash '
  f'flow most (45%) because the company’s cash flows are directly modelled from a disclosed cost structure; '
  f'the relative and earnings-power lenses each 20%; and book value least (15%), because book understates a '
  f'business earning a mid-20s return on invested capital and a high-30s return on equity. The weighted '
  f'central is SAR {sar(LN["central"]["base"],0)}.')

H2('1.6  The drivers — each segment on its own driver, margin as an output')
P(f'Revenue is not grown at one rate. A cable maker sells metal plus a conversion spread. We model a cable-'
  f'tonnage index, priced as metal content — on its own copper-and-aluminium path — plus a conversion spread '
  f'whose cost escalates on domestic inflation. Volume grows {pct(IN["vol_growth"][0])} in 2026, tapering to '
  f'{pct(IN["vol_growth"][4])}, anchored on the reviewed half-year statement that 2026 revenue rose 9.5% "due '
  f'to the increase in the volume of quantities sold." Metal prices are held broadly flat. Stated rather than '
  f'implied: with H1-2026 revenue of SAR {sar(ITM["h1_26_rev"],0)}mn (+{pct(ITM["h1_g"],1)}) in the books, the '
  f'full-year build implies second-half revenue of SAR {sar(ITM["h2_26_rev"],0)}mn, +{pct(ITM["h2_g"],1)} '
  f'against a second half of 2025 that already carried the strong-metal revenue base — a deliberate '
  f'deceleration, not an oversight. Gross margin is then an OUTPUT of the stack — {pct(F["gm"][0])} in 2026 '
  f'rising gently to {pct(F["gm"][4])}, and never back to the 2024–25 peak. In the companion workbook the '
  f'spread per tonne is calibrated to this margin path at the base metal price and held fixed under metal '
  f'shocks, so the margin cell falls when the metal cell rises — the mechanism is live, not narrated.')
figure(os.path.join(HERE, 'fig7_stack.png'), 6.7,
       'Figure 2. The cost stack. Materials (copper and aluminium) are about 95% of cost of sales; the gross '
       'margin, shown on the right axis, is what is left after materials and conversion cost — an output, not '
       'an input.')

H2('1.7  The crux — the sustained gross margin')
P(f'The crux is simple to state and consequential. Gross margin rose from {pct(HI["FY23"]["gp"]/HI["FY23"]["rev"])} '
  f'in 2023 to a {pct(HI["FY25"]["gp"]/HI["FY25"]["rev"])} peak in 2025 as metal prices moved the company’s '
  f'way. In the first half of 2026, on a {pct(ITM["h1_g"],1)} rise in revenue, gross profit was essentially '
  f'flat against a first half of 2025 at {pct(SRC["interims_2026"]["H1_2025_thousands"]["gross_profit"]/SRC["interims_2026"]["H1_2025_thousands"]["revenue"],1)} '
  f'— the like-for-like compression is about 1.5 points, and the half deteriorates within itself: '
  f'{pct(ITM["q1_gm"],1)} in the first quarter, {pct(ITM["q2_gm"],1)} in the second. That is the metal '
  f'pass-through working in reverse: volume-led growth at a normalising per-tonne spread. We anchor the '
  f'forecast on the reviewed half-year average ({pct(IN["spread_anchor"],1)}), not the higher full-year 2025 '
  f'print, and we show the value all three ways: at the anchor SAR {sar(DCF["spread_base"],0)}, at the '
  f'second-quarter exit rate held for the whole forecast SAR {sar(ITM["dcf_q2_exit"],0)}, and at the 14.5% '
  f'bear framing SAR {sar(DCF["spread_bear"],0)}. The falsifier is unchanged — a sustained margin below '
  f'14.5% — and the third-quarter print is the live test.')
figure(os.path.join(HERE, 'fig8_margin.png'), 6.8,
       'Figure 3. The gross-margin story: the 2024–25 metal-tailwind peak, the first-half-2026 '
       'normalisation to 15.3%, and a forecast that recovers only gently and stays below the peak. The shaded '
       'band is the contested range carried through the valuation.')

H2('1.8  Macro and country — the cost of capital, built up')
P(f'The cost of capital is built from sourced, dated components. The ten-year SAR risk-free rate is '
  f'{pct(IN["rf"],2)}, taken from the published Saudi government bond curve — the index provider’s factsheet '
  f'of 31-Jul-2026 puts the 7–10-year bucket’s yield at 5.52% on an upward-sloping curve — and corroborated '
  f'by the ten-year US Treasury (4.68–4.72% that week) plus Saudi Arabia’s dollar new-issue spread, and by '
  f'the SAR sukuk index level; it is sensitised ±50bp below. Saudi Arabia is rated Aa3; its adjusted '
  f'sovereign default spread is {pct(IN["sov_spread"],2)} and its equity risk premium {pct(IN["erp"],2)} (a '
  f'{pct(IN["erp_mature"],2)} mature-market base plus a {pct(IN["erp_crp"],2)} country premium, July-2026 '
  f'dataset). We subtract the sovereign’s own default spread from the risk-free rate to avoid charging '
  f'country risk twice, and add beta times the premium. Beta is {IN["beta"]:.3f} — a Dimson sum-beta on '
  f'{W["beta_res"]["n"]} weekly returns against the Tadawul All Share Index over the full listed history '
  f'(plain OLS {BETA_OLS:.3f}; R² {W["beta_res"]["r2"]:.2f}; 90% confidence '
  f'interval {W["beta_res"]["ci90"][0]:.2f}–{W["beta_res"]["ci90"][1]:.2f} — wide, and priced in the beta '
  f'grid below). That gives a cost of equity of {pct(W["ke"],1)}. Debt is marginal and cheap — variable-rate '
  f'Islamic Murabaha whose margin the filings do not disclose, estimated at about {pct(IN["kd"],1)} (three-'
  f'month SAIBOR plus a corporate margin), above the sovereign as a corporate must be. The weighted cost is '
  f'{pct(W["wacc"],1)}, easing to {pct(W["wacc_term"],1)} in perpetuity as the country premium narrows and '
  f'beta reverts toward one; the terminal is discounted all-equity because the model’s own forecast reaches '
  f'net cash from 2028.')
cc = [['Cost of capital', 'Explicit', 'Terminal'],
      ['Risk-free rate (SAR 10-year), normalised', pct(W['rf_star'], 2), pct(IN['rf_term'], 2)],
      ['Equity risk premium', pct(IN['erp'], 2), pct(IN['erp_term'], 2)],
      ['Beta', f'{IN["beta"]:.3f}', f'{IN["beta_term"]:.2f}'],
      ['Cost of equity', pct(W['ke'], 2), pct(W['ke_term'], 2)],
      ['Cost of debt (after tax)', pct(W['kd_at'], 2), pct(W['kd_term_at'], 2)],
      ['Net-debt weight', pct(W['wd'], 1), pct(IN['wd_term'], 0)],
      ['Weighted cost of capital', pct(W['wacc'], 2), pct(W['wacc_term'], 2)]]
table(cc, [3.2, 1.35, 1.35], band_rows={4, 7}, size=9.0, align_right_from=1)

H2('1.9  Sensitivity')
P(f'Fair value is most sensitive to the risk-free rate (a ±50bp move is worth roughly '
  f'SAR {sar(SN["grid_rf"][0],0)} / {sar(SN["grid_rf"][1],0)} / {sar(SN["grid_rf"][2],0)} on the cash-flow '
  f'lens, since it enters both the explicit and the terminal discount rate), then to the terminal growth '
  f'rate and terminal cost of capital, the sustained margin, beta and working-capital intensity. The grid '
  f'below revalues the cash-flow lens across the terminal cost of capital and terminal growth; cells where '
  f'the terminal spread falls below two points are shown as n/m rather than as numbers, because a growing '
  f'perpetuity is not meaningful there. The companion workbook carries the full set, and every block’s base '
  f'row reproduces the base case.')
figure(os.path.join(HERE, 'fig2_sens.png'), 6.2,
       'Figure 4. Cash-flow fair value (SAR/share) across the terminal cost of capital and terminal growth; '
       'the bold cells sit closest to the current price.')

# ============ 6 SECTION 2 TECHNICAL ==========================================
H1('2  Technical and price structure')
P(f'The shares last traded at SAR {sar(SPOT,2)}, near the lower end of a 52-week range of SAR '
  f'{sar(LO52,2)}–{sar(HI52,2)}. The price sits {_stack_state}: the 20-session average is SAR '
  f'{sar(SMA[20],1)}, the 50-session SAR {sar(SMA[50],1)}, the 100-session SAR {sar(SMA[100],1)} and the '
  f'200-session SAR {sar(SMA[200],1)} — the close is about {pct(SPOT/SMA[200]-1,0)} against the 200-session '
  f'average, after a strong multi-year run from the December 2022 listing. Every figure in this paragraph is '
  f'computed from the same price series the chart draws. This section is descriptive; it carries no '
  f'fundamental claim.')
figure(os.path.join(HERE, 'fig3_ma.png'), 6.9,
       'Figure 5. Price against its 20-, 50-, 100- and 200-session moving averages, last 260 sessions.')

# ============ 7 SECTION 3 PROBABILISTIC PRICE MAP ============================
H1('3  A probabilistic price map')
P(f'Separately from the fundamental value, we map the range of prices the shares could plausibly reach over '
  f'the next one and three months, from 50,000 simulated paths calibrated to the stock’s own volatility. '
  f'This is a statement about price risk, not about fair value.')
pm = [['Percentile', 'One month', 'Three months'],
      ['95th (upper)', sar(H1H['pct']['p95'], 1), sar(H3['pct']['p95'], 1)],
      ['75th', sar(H1H['pct']['p75'], 1), sar(H3['pct']['p75'], 1)],
      ['50th (median)', sar(H1H['pct']['p50'], 1), sar(H3['pct']['p50'], 1)],
      ['25th', sar(H1H['pct']['p25'], 1), sar(H3['pct']['p25'], 1)],
      ['5th (lower)', sar(H1H['pct']['p5'], 1), sar(H3['pct']['p5'], 1)],
      ['Chance of finishing above today', pct(H1H['p_above'], 0), pct(H3['p_above'], 0)]]
table(pm, [2.6, 1.5, 1.5], size=9.2, align_right_from=1)
figure(os.path.join(HERE, 'fig4_fan.png'), 6.9,
       'Figure 6. The forward price cone to three months — the shaded bands are the 25–75% and 5–95% '
       'ranges; the dashed brass line marks the fundamental central estimate.')
BT3 = BT['h3']['production']; BT1 = BT['h1']['production']
P(f'How well is the cone calibrated? The short listing allows only {BT3["windows"]} non-overlapping '
  f'three-month test windows, and on them the 50%, 80% and 90% bands contained {pct(BT3["cov50"],0)}, '
  f'{pct(BT3["cov80"],0)} and {pct(BT3["cov90"],0)} of actual outcomes — with ten windows, seven-in-ten '
  f'against a five-in-ten target is well inside sampling noise, and the formal uniformity tests agree '
  f'(chi-square p = {BT3["chi2_p"]:.2f}, Kolmogorov–Smirnov p = {BT3["ks_p"]:.2f}), so the three-month map '
  f'is consistent with its targets rather than proven precise; its bands also ran about '
  f'{pct(BT3["width_vs_benchmark"]-1,0)} wider than a naive benchmark, a caution against reading them as '
  f'tight. The one-month map is weaker and we say so: across {BT1["windows"]} one-month windows the cone '
  f'scored consistently a little behind a simple random-walk benchmark and its bands were too wide (the 80% '
  f'band covered {pct(BT1["cov80"],0)} of outcomes) — read the one-month table as conservative ranges, not '
  f'calibrated odds. On scored accuracy the three-month cone was statistically indistinguishable from the '
  f'benchmark; it neither reliably beat it nor lagged it, which for a liquid large-cap is the honest result. '
  f'Because the company only listed in December 2022, the calibration rests on that short own history '
  f'together with the broader Saudi-market evidence behind the same simulation model; a five-year single-'
  f'name record will exist in time. The level-touch chances above are read directly from the simulated '
  f'paths.')

# ============ 8 SECTION 4 COMPARISON OF THE LENSES ===========================
H1('4  Comparison of the lenses')
P(f'The lenses disagree by design, and the disagreement is informative. The intrinsic discounted-cash-flow '
  f'value (SAR {sar(LN["dcf"]["base"],0)}) is the highest: it rewards a high return on capital, durable mid-'
  f'single-digit growth and a low Saudi cost of capital, and it is terminal-heavy ({pct(DCF["tv_share"],0)} of '
  f'value beyond year five). The relative lens (SAR {sar(LN["relative"]["base"],0)}) is the most cautious: it '
  f'holds the company to a mid-range exit multiple below where it trades today. Earnings power (SAR '
  f'{sar(LN["normalized"]["base"],0)}) and book value (SAR {sar(LN["book"]["base"],0)}) sit between. Read '
  f'together: the market price sits {pct(LN["central"]["base"]/SPOT-1,0)} below the weighted central, inside '
  f'the span the four lenses draw, and which side of fair value one reads depends on how much credit one '
  f'gives the intrinsic economics versus the exit multiple. The weighted central of SAR '
  f'{sar(LN["central"]["base"],0)} splits that difference; the reader weighs it, this study does not '
  f'recommend.')

# ============ 9 SECTION 5 CATALYSTS ==========================================
H1('5  Catalysts to watch')
bullet(' the quarterly gross margin. The single most important number. Each quarter’s reviewed margin '
       'tests the sustained-spread judgement directly.', 'Margin prints —')
bullet(' copper and aluminium. A sustained metal move changes revenue and the reported margin; watch that '
       'gross profit per tonne, not the headline margin, holds.', 'Metal prices —')
bullet(' Saudi grid and construction spend (Saudi Electricity Company, giga-projects, housing) drives domestic '
       'volume, about three-quarters of sales.', 'Volume —')
bullet(' the export share (about a quarter of sales, mostly the UAE) and any new-market wins, including the '
       'early-stage Syrian memorandum of understanding disclosed in 2026.', 'Exports —')
bullet(' semi-annual dividends and any change in the payout; the shareholder-approved purchase of up to '
       '300,000 treasury shares for the employee incentive plan (May 2026, unexecuted at the study date; '
       'under 0.2% of shares if completed); capital returns; and the completion of the current capacity '
       'build.', 'Capital —')

# ============ 10 SECTION 6 READING THE PROBABILITY ZONES ======================
H1('6  Reading the probability zones')
P(f'The fundamental range and the price cone answer different questions. The fundamental central (SAR '
  f'{sar(LN["central"]["base"],0)}) is where the business is worth on its cash flows; the price cone (a three-'
  f'month 5–95% range of about SAR {sar(H3["pct"]["p5"],0)} to SAR {sar(H3["pct"]["p95"],0)}) is where the '
  f'price could travel on volatility alone. When the fundamental estimate sits above the price, as here, the '
  f'gap is the potential the intrinsic lens sees; the cone is a reminder that the path is wide and the outcome '
  f'uncertain over any short horizon.')

# ============ 11 SECTION 7 CAVEATS ===========================================
H1('7  Caveats and what would change our mind')
bullet(' if the sustained gross margin settles below 14.5% — a competitive or metal-driven squeeze on the '
       'conversion spread — the cash-flow lens falls toward SAR {}.'.format(sar(DCF["spread_bear"], 0)),
       'The margin —')
bullet(' the value is terminal-heavy ({} of enterprise value). A higher terminal cost of capital or lower '
       'growth cuts it materially, as the sensitivity grid shows.'.format(pct(DCF["tv_share"], 0)),
       'Terminal reliance —')
bullet(' revenue is single-country-concentrated and customer-concentrated (one customer was about 19% of 2025 '
       'revenue); the beta is estimated on a short listed history with a wide confidence interval.',
       'Concentration —')
bullet(' a working-capital-heavy model ties cash in copper inventory and receivables; a stretch in either '
       'absorbs the cash the cash-flow lens counts.', 'Working capital —')
bullet(' the price cone rests on a three-and-a-half-year listed history, shorter than the five-year ideal.',
       'Short record —')

# ============ 12 APPENDIX A STATEMENTS =======================================
doc.add_page_break()
H1('Appendix A  Financial statements')
H2('A.1  Income statement — three years actual, five years forecast')
is_rows = [['SAR mn'] + ['2023', '2024', '2025'] + [y for y in F['years']]]
def fc_line(label, hist, fc, d=0, ispct=False):
    r = [label]
    for v in hist:
        r.append(pct(v) if ispct else sar(v, d))
    for v in fc:
        r.append(pct(v) if ispct else sar(v, d))
    return r
is_rows.append(fc_line('Revenue', [HI[y]['rev'] for y in ['FY23', 'FY24', 'FY25']], F['rev']))
is_rows.append(fc_line('Gross profit', [HI[y]['gp'] for y in ['FY23', 'FY24', 'FY25']], F['gp']))
is_rows.append(fc_line('  Gross margin', [HI[y]['gp'] / HI[y]['rev'] for y in ['FY23', 'FY24', 'FY25']], F['gm'], ispct=True))
is_rows.append(fc_line('EBITDA', [HI[y]['ebitda'] for y in ['FY23', 'FY24', 'FY25']], F['ebitda']))
is_rows.append(fc_line('EBIT', [HI[y]['ebit'] for y in ['FY23', 'FY24', 'FY25']], F['ebit']))
is_rows.append(fc_line('Net finance cost', [HI[y]['fin'] for y in ['FY23', 'FY24', 'FY25']], [-x for x in F['interest']]))
is_rows.append(fc_line('Profit before zakat', [HI[y]['ebt'] for y in ['FY23', 'FY24', 'FY25']],
                       [F['ebit'][i] - F['interest'][i] for i in range(5)]))
is_rows.append(fc_line('Net profit', [HI[y]['pat'] for y in ['FY23', 'FY24', 'FY25']],
                       [(F['ebit'][i] - F['interest'][i]) * (1 - IN['tax_eff']) for i in range(5)]))
table(is_rows, [1.7] + [0.8] * 8, size=8.0)

H2('A.2  Balance sheet — three years actual')
bs_rows = [['SAR mn', '2023', '2024', '2025']]
for lbl, key in [('Property, plant & equipment', 'ppe'), ('Inventory', 'inv'), ('Trade & other receivables', 'recv'),
                 ('Cash & equivalents', 'cash'), ('Total assets', 'assets'), ('Gross borrowings incl. leases', 'debt'),
                 ('Net financial debt', 'nd'), ('Equity attributable', None)]:
    if key is None:
        bs_rows.append(['Equity attributable', sar(HB['FY23']['eqp'], 0),
                        sar(HB['FY24']['eqp'], 0), sar(HB['FY25']['eqp'], 0)])
    else:
        bs_rows.append([lbl, sar(HB['FY23'][key], 0), sar(HB['FY24'][key], 0), sar(HB['FY25'][key], 0)])
table(bs_rows, [2.6, 1.15, 1.15, 1.15], size=8.6)

H2('A.3  Forecast balance-sheet and cash-flow markers')
mk_rows = [['SAR mn'] + [y for y in F['years']]]
mk_rows.append(['Net working capital'] + [sar(F['nwc'][i], 0) for i in range(5)])
mk_rows.append(['Net financial debt (end)'] + [sar(F['net_debt'][i], 0) for i in range(5)])
mk_rows.append(['Capital expenditure'] + [sar(F['capex'][i], 0) for i in range(5)])
mk_rows.append(['Free cash flow to firm'] + [sar(F['fcff'][i], 0) for i in range(5)])
mk_rows.append(['Dividend'] + [sar(F['div'][i], 0) for i in range(5)])
mk_rows.append(['Attributable profit'] + [sar(F['np_attr'][i], 0) for i in range(5)])
table(mk_rows, [2.0] + [0.98] * 5, size=8.4)

# ============ 13 APPENDIX B PEERS / RISK / RESEARCH REGISTER ==================
H1('Appendix B  Peer frame, risk register, and the research register')
H2('B.1  Peer frame')
pr = [['Peer', 'Market', 'EV/EBITDA', 'Basis (each multiple recomputed from the peer’s own EV and guidance)'],
      ['Riyadh Cables (subject)', 'Tadawul', f'{REL["ev_ebitda_trailing"]:.1f}x', f'FY2025 accounts; P/E {REL["pe_trailing"]:.1f}x FY2025, {ITM["pe_ttm"]:.1f}x trailing twelve months'],
      ['Prysmian', 'Milan', f'~{IN["peer_prysmian_fwd"]:.0f}x', 'FY2026E on guidance raised 30-Jul-2026 (EUR 2.8–2.9bn) vs ~EUR 40bn EV'],
      ['Nexans', 'Paris', f'~{IN["peer_nexans_fwd"]:.1f}x', 'FY2026E on guidance raised 29-Jul-2026 (EUR 770–840mn) vs ~EUR 7.1bn EV'],
      ['Polycab India', 'NSE', f'~{IN["peer_polycab_fwd"]:.0f}x', 'next twelve months'],
      ['KEI Industries', 'NSE', f'~{IN["peer_kei_fwd"]:.0f}x', 'next twelve months (~24–25x only two fiscal years out)'],
      ['Ducab', 'UAE (private)', '—', 'regional peer, unlisted']]
table(pr, [1.55, 0.85, 0.85, 3.05], size=8.6)
P('Quotes as of 18-Aug-2026; cross-check context only, never a source for any Riyadh Cables figure. The '
  f'justified {IN["ev_ebitda_just"]:.1f}x applied in the relative lens is a deliberate discount to the '
  'developed band above for single-country and single-customer concentration.', size=8.8)
H2('B.2  Risk register')
bullet(' concentrated in the conversion spread; a normalising or competed margin is the main downside.', 'Margin —')
bullet(' copper/aluminium price and availability; hedged, but a sustained move still moves reported results.', 'Metal —')
bullet(' single-country and single-customer concentration (one customer ~19% of 2025 revenue).', 'Concentration —')
bullet(' working-capital intensity and receivables quality (a SAR 151mn receivables impairment in 2025).', 'Cash —')
bullet(' short listed history for the beta and the price-cone calibration.', 'Data —')
H2('B.3  Research register')
P('Every figure in this study traces to a primary source. The full register — each input with its value, date, '
  'source and how it was constructed — is in the companion bibliography document. In summary: the historical '
  'income statement, balance sheet, cash flow, segment, cost and inventory figures come from Riyadh Cables’ '
  'own audited consolidated financial statements for 2022 through 2025 (KPMG, unmodified opinions); the 2026 '
  'near-term anchor is the company’s Tadawul-filed reviewed half-year results; the cost of capital uses the '
  'published Saudi sovereign and equity-risk-premium data and the Tadawul index for beta; and metal prices are '
  'the London Metal Exchange copper and aluminium references. No data aggregator, broker note or press report '
  'is a source for any company figure.')

# ============ 14 APPENDIX C EXPERT PANEL =====================================
doc.add_page_break()
H1('Appendix C  Expert panel')
P('Three valuation methods on the same forecast base, each isolating a different driver of value, each '
  'worked in full with a condition that would prove it wrong. They are not independent evidence — they '
  'share the revenue build, the margin path and the cost of capital — and the study says so; what they '
  'add is where the value sits, not a second opinion on the forecasts. They are labelled Expert 1, 2 and '
  '3 and cast by method. Every figure below is a live formula in the companion workbook.')
E = EXPP
H2('C.1  Expert 1 — earnings power')
P(f'Worldview: value a stable manufacturer on mid-cycle earnings and a through-cycle multiple. Works when '
  f'earnings are recurring; fails if the cycle breaks structurally. Mid-cycle EBITDA margin {pct(E["e1"]["margin"],1)} '
  f'on revenue at the 2028 scale (SAR {sar(E["e1"]["rev"],0)}mn) gives EBIT of SAR {sar(E["e1"]["ebit"],0)}mn; '
  f'less a normalised net interest charge of SAR {sar(E["e1"]["interest"],0)}mn — the year-three cost of debt '
  f'on the 2025 gross debt, less deposit income on the 2025 cash, not any single forecast year’s line — then '
  f'tax and minorities, earnings are SAR {E["e1"]["eps"]:.2f} per share; at {E["e1"]["pe"]:.1f}x that is SAR '
  f'{sar(E["e1"]["pe"]*E["e1"]["eps"],0)} at end-2025 and SAR {sar(E["e1"]["base"],0)} rolled to the anchor '
  f'(range SAR {sar(E["e1"]["rng"][0],0)}–{sar(E["e1"]["rng"][1],0)}). Falsifier: a sustained margin below 14%.')
H2('C.2  Expert 2 — owner cash earnings')
P(f'Worldview: an owner earns the free cash flow after real reinvestment; capitalise mid-cycle owner cash at the '
  f'cost of equity. Works for a cash-generative business; fails if reinvestment is understated. Mid-cycle free '
  f'cash flow to the firm (the 2028–30 average, SAR {sar(E["e2"]["fcff"],0)}mn), less after-tax net interest of '
  f'SAR {sar(E["e2"]["int_at"],0)}mn on the same normalised basis as Expert 1 and net of minorities, is owner '
  f'cash of about SAR {sar(E["e2"]["fcfe"],0)}mn; grown at {pct(IN["g_term"],0)} and capitalised at the '
  f'{pct(E["e2"]["ke"],1)} terminal cost of equity, then rolled to the anchor, that gives SAR '
  f'{sar(E["e2"]["base"],0)} (range SAR {sar(E["e2"]["rng"][0],0)}–{sar(E["e2"]["rng"][1],0)}). Falsifier: '
  f'free cash conversion staying below half of earnings.')
H2('C.3  Expert 3 — cash returns versus the cost of capital')
P(f'Worldview: value is invested capital plus the present value of returns above the cost of capital. Works when '
  f'returns are measurable and durable; fails if the return advantage erodes. Invested capital of SAR '
  f'{sar(E["e3"]["ic0"],0)}mn plus the present value of economic profit (SAR {sar(E["e3"]["pv_ep"]+E["e3"]["pv_ep_term"],0)}mn) '
  f'gives SAR {sar(E["e3"]["base"],0)} per share (range SAR {sar(E["e3"]["rng"][0],0)}–{sar(E["e3"]["rng"][1],0)}). '
  f'By construction this decomposition reproduces the cash-flow lens exactly — value equals capital plus '
  f'excess returns is the same money counted another way, and the workbook shows the two agree to the riyal; '
  f'what it isolates is how much of the value is excess return on capital rather than capital itself. '
  f'Falsifier: return on capital falling toward the cost of capital.')
figure(os.path.join(HERE, 'figD1_experts.png'), 6.7,
       'Figure 7. The three experts’ fair-value ranges; brass ticks are base cases, the gold band is the '
       'panel centre.')
H2('C.4  Cross-examination')
bullet(' Expert 1’s multiple is challenged as too high for a single-country name — conceded in the bear '
       'case (10x), rejected as the base given the return profile.', 'On the multiple:')
bullet(' Expert 2’s reinvestment is challenged as too light — rejected: capital expenditure ran at 2.2% of '
       'revenue in 2024 and 1.8% in 2025 on the audited cash-flow statements, the forecast never drops '
       'below the 2025 rate, and the model still charges working-capital investment.', 'On reinvestment:')
bullet(' Expert 3’s durability of returns is challenged — conceded that the mid-20s return on capital '
       'will fade toward the cost of capital eventually, which is why the terminal return is struck at 25% '
       'and terminal growth at 4%.', 'On durability:')
H2('C.5  The three in one room')
P(f'The three methods land at SAR {sar(E["e1"]["base"],0)}, SAR {sar(E["e2"]["base"],0)} and SAR '
  f'{sar(E["e3"]["base"],0)}, a median of SAR {sar(D["panel_centre"],0)} — which is Expert 3, and Expert 3 '
  f'is arithmetically the cash-flow lens, so the median is a restatement of the primary lens, not a second '
  f'vote for it. They agree the business is high-return and under-levered; they differ on how much of that '
  f'return the future keeps.')
H2('C.6  Reading the divergence')
P(f'The gap between the experts is almost entirely the terminal assumption: how durable the return advantage and '
  f'the growth are. Expert 2, which capitalises owner cash into perpetuity, is the most sensitive to it and sits '
  f'highest; Expert 1, on a fixed exit multiple, is the most anchored and sits lowest. The same single lever — '
  f'the sustained margin and the terminal cost of capital — moves all three, which is why it is the study’s '
  f'crux.')

# ============ 15 ABOUT & 16 DISCLOSURE =======================================
doc.add_page_break()
H1('About this series')
P('Testahil publishes independent, educational valuation studies. Each is built from a company’s own '
  'audited disclosures, values the business through several lenses, and states its assumptions and its '
  'uncertainty openly. A companion workbook carries the full model as live formulas; a companion bibliography '
  'lists every source. The studies are analysis, not advice.')
H2('Revision note — second edition, 19 August 2026')
P('This edition supersedes the first edition of 18 August 2026 following an external review; the valuation '
  'anchor remains 18 August 2026. The material corrections, all applied through the model rather than '
  'patched into the text: the ten-year SAR risk-free rate moves from an estimated 4.85% to the published '
  'curve’s 5.52% (entering both the explicit and the terminal discount rate); the May-2026 dividend netted '
  'in the anchor roll is the SAR 2.25 actually paid, not 1.90; the settled 18-Aug close of SAR 104.90 '
  'replaces an unsettled 104.80 print; the peer multiples are recomputed from the peers’ own guidance and '
  'the justified multiple re-set as a stated discount to the corrected band; capital expenditure is floored '
  'at the audited 2025 rate; the terminal is discounted all-equity, consistent with the model’s own '
  'net-cash forecast; the July-2026 sovereign-risk vintage is adopted; and the workbook’s cost-stack now '
  'carries the spread-per-tonne mechanics live, so margin is an output on the sheet, not only in the prose. '
  'Together these move the weighted central from SAR 119 to SAR 108 per share. Smaller corrections — the '
  'FY2023 depreciation transcription, the FY2023 payables definition, header alignment and ratio wiring in '
  'the workbook, and disclosure additions throughout — are listed in the companion bibliography and the '
  'repository’s response document.')
H1('Disclosure & disclaimer')
P('This document is an independent educational analysis and is not investment advice, an offer, a solicitation, '
  'or a recommendation to buy or sell any security. It is not a price target. All values are model outputs shown '
  'as ranges and depend on assumptions that may prove wrong. The author holds no position in Riyadh Cables Group '
  'Company and received no compensation from it. Figures derive from the company’s own audited and reviewed '
  'financial statements and from published market and sovereign-risk data; while care has been taken, no '
  'warranty is given as to accuracy or completeness. Readers must reach their own conclusions and, where '
  'appropriate, take professional advice. Past performance and modelled scenarios are not guarantees of future '
  f'results. Currency is Saudi riyals unless stated. Prices as at {M["asof"]}.', size=8.6, color=GREY)

OUT = os.path.join(HERE, 'RIYADHCABLE_Valuation_Study_18-08-2026_public.docx')
doc.save(OUT)
print('wrote', os.path.basename(OUT), '| paragraphs', len(doc.paragraphs), '| tables', len(doc.tables))
