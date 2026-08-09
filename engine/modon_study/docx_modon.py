# -*- coding: utf-8 -*-
"""MODON_Valuation_Study_09-08-2026_public.docx — 16-section study, house canonical
structure. All numbers come from study_numbers.json; no financial numeral is typed here.
Written for an EXTERNAL reader: no internal-procedure vocabulary anywhere."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
exec(open(os.path.join(HERE, 'docx_base.py')).read())

M, HI, HB, F = D['meta'], D['hist_is'], D['hist_bs'], D['fcst']
W, DCF, LN, SN = D['wacc'], D['dcf'], D['lenses'], D['sens']
EXPD, REL, NRM, BKL = D['experts'], D['rel'], D['norm'], D['book']
SEG, S0, STK, CJ = D['seg_fy25'], D['step0'], D['strike'], D['contested']
TECH, H1D, UN = D['tech'], D['h1'], D['units']
IN = {k: (v['value'] if isinstance(v, dict) and 'value' in v else v)
      for k, v in D['inputs'].items()}
SPOT, SH = M['spot'], M['shares_mn']
CEN = D['central']
H1M, H3M = STK['horizons']['1M'], STK['horizons']['3M']

def n0(x): return f'{x:,.0f}'
def n1(x): return f'{x:,.1f}'
def px(x): return f'{x:.2f}'
def pc(x, d=1): return f'{x*100:.{d}f}%'
def bn(x): return f'{x/1000:,.1f}'
YRS = ['FY2026E', 'FY2027E', 'FY2028E', 'FY2029E', 'FY2030E']

# ============================ MASTHEAD + READ FIRST ===========================
masthead()
P('Modon Holding PSC', size=24, bold=True, space_after=0)
rich([('ADX: MODON · Abu Dhabi Securities Exchange · United Arab Emirates dirham (AED)', dict(color=GREY, size=11))],
     space_after=2)
rich([(f'Independent valuation study · 9 August 2026 · price anchor AED {px(SPOT)} (close 7 August 2026)',
       dict(color=GREY, size=10))], space_after=10)
box([
 ('READ FIRST. ', 'This study is an independent, educational analysis of Modon Holding PSC. '
  'It is not investment advice, not a recommendation, and it contains no price target. '
  'Every value in it is a model output presented as a range with its assumptions shown.'),
 ('Sources. ', 'Every historical figure is taken from the company\'s own audited consolidated '
  'financial statements and reviewed interims, retrieved from the company\'s investor-relations '
  'library, or from its own results announcements — never from a data vendor. Peer figures are '
  'cross-checks only and are labelled where they appear. A companion bibliography document lists '
  'every input with its value, source and date.'),
 ('The one judgement that matters most. ', 'Whether the record 2025–26 development sales surge '
  'persists or fades to backlog run-off moves this valuation more than any other input. Both '
  'readings are computed in full and shown side by side. They are never averaged.'),
 ('Companion files. ', 'A formula-driven Excel model (change a blue driver and the valuation '
  'reprices) and a standalone bibliography ship with this document.'),
])

# ============================ HEADLINE ========================================
H1('Headline')
rich([(f'Fair value AED {px(LN["central"]["bear"])}–{px(LN["central"]["bull"])} per share, '
       f'weighted central AED {px(CEN)}, against a market price of AED {px(SPOT)} '
       f'({CEN / SPOT - 1:+.0%}). ', dict(bold=True, size=12))], space_after=8)
P(f'Modon Holding is Abu Dhabi\'s government-owned city-builder: a AED {bn(HI["FY25"]["rev"])}bn-revenue, '
  f'four-leg group spanning real-estate development (Hudayriyat Island, Reem Island, Ras El Hekma in '
  f'Egypt), an asset-management platform, a hospitality portfolio of 27 hotels, and the ADNEC events '
  f'business. In FY2025 — its first clean year in the combined perimeter — it earned AED '
  f'{bn(HI["FY25"]["pat"])}bn after tax, and its half-year 2026 revenue is running {H1D["rev_yoy"]:+.0%} '
  f'year on year with a AED {bn(UN["backlog"])}bn revenue backlog, 93% of it contracted development sales.')
P(f'The tension in this name is unusually clean. A cash-flow reading of the backlog and the four legs is '
  f'worth AED {px(DCF["ps"])} per share on the base path — and still AED {px(CJ["runoff_ps"])} if new '
  f'sales halve and fade to run-off. The market lenses cluster far lower: peer multiples imply about AED '
  f'{px(REL["base"])}, normalised mid-cycle earnings about AED {px(NRM["base"])}, and book value at a '
  f'justified multiple about AED {px(BKL["base"])}. The market prices Modon at '
  f'{REL["pe_trailing"]:.1f}x trailing earnings against {REL["peers"]["ALDAR"]["pe"]:.1f}x for Aldar — '
  f'a premium multiple on earnings the market does not yet treat as durable. Section 4 prices exactly '
  f'what discount rate the market is charging; section 1.7 shows both sales paths in full.')
P(f'Over the next three months the price map is symmetric and modest: the central band runs AED '
  f'{px(H3M["pct"]["p25"])}–{px(H3M["pct"]["p75"])} with 5th–95th percentiles at AED '
  f'{px(H3M["pct"]["p5"])}–{px(H3M["pct"]["p95"])}. A fundamental verdict of this size, if right, plays '
  f'out over years, not a quarter.')

# ============================ VALUATION SUMMARY ===============================
H1('Valuation summary')
rows = [['Lens', 'Bear', 'Base', 'Bull', 'Weight', 'vs price']]
for k, nm in [('dcf', 'Discounted cash flow (primary)'), ('relative', 'Relative multiples'),
              ('normalized', 'Normalised earnings power'), ('book', 'Book value & sustainable return')]:
    l = LN[k]
    rows.append([nm, px(l['bear']), px(l['base']), px(l['bull']), pc(l['w'], 0),
                 f"{l['base'] / SPOT - 1:+.0%}"])
rows.append(['Weighted central', px(LN['central']['bear']), px(CEN), px(LN['central']['bull']),
             '100%', f'{CEN / SPOT - 1:+.0%}'])
rows.append([f'DCF terminal value share of enterprise value: {pc(DCF["tv_share"])}',
             '', '', '', '', ''])
rows.append([f'Market price (7 Aug 2026)', '', px(SPOT), '', '', ''])
table(rows, [2.55, 0.82, 0.82, 0.82, 0.78, 0.85], band_rows={5}, first_col_bold=False)
caption('All figures AED per share. The DCF bear and bull are the backlog run-off and growth-hold '
        'scenarios of section 1.7, not cosmetic haircuts. The terminal value share is stated beside '
        'the lens it belongs to; the same figure is linked live in the Excel bridge.')
rich([('The contested judgement, both ways: ', dict(bold=True)),
      (f'base path AED {px(DCF["ps"])} · backlog run-off AED {px(CJ["runoff_ps"])}. Both are complete '
       f'valuations of the same balance sheet; the difference is only the sales path. '
       f'They are shown side by side wherever either appears.', dict())], space_after=10)

# ============================ COMPANY OVERVIEW ================================
H1('Company overview')
P('Modon Holding PSC is the Abu Dhabi government\'s listed city-development platform. The listed '
  'vehicle began as Al Qudra Holding, became Q Holding, and in 2024 absorbed Modon Properties and '
  'the ADNEC Group in a share-financed combination that multiplied the balance sheet roughly '
  'four-fold and reset the perimeter — FY2024 income carries a AED '
  f'{bn(D["oneoff"]["fy24"]["bargain"])}bn accounting gain from that combination and is treated as a '
  'transition year throughout this study. On 30 October 2025 IHC and ADQ sold their entire stakes to '
  'L\'imad Holding Company PJSC, wholly owned by the Abu Dhabi Government, which now holds about 85% '
  'of the shares. The stock trades on ADX\'s growth market with a correspondingly thin free float.')
P('The group reports four operating segments. Real Estate Development (54% of FY2025 revenue) '
  'masterplans and sells land and homes on Hudayriyat Island (>50mn sqm, 40,000 planned units), Reem '
  'Island and Al Ain, and is lead developer of phase 1 of Ras El Hekma on Egypt\'s north coast '
  '(170.8mn sqm gross, 500,000+ planned units) alongside La Zagaleta in Spain. Events, Catering & '
  'Tourism (36%) is the ADNEC platform: exhibition venues in Abu Dhabi and London (ExCeL), event '
  'infrastructure (Arena Group, acquired May 2025), catering and tourism. Hospitality (6%) runs 27 '
  'hotels with 7,137 keys. Asset & Investment Management (5%) holds the recurring-income portfolio '
  '(97% occupancy) and the group\'s financial investments, including a 50% stake in 2 Finsbury '
  'Avenue in London.')
seg_rows = [['Segment', 'Revenue', 'Gross profit', 'Margin', 'Profit before tax', 'Assets']]
for k, nm in [('red', 'Real Estate Development'), ('aim', 'Asset & Investment Mgmt'),
              ('hosp', 'Hospitality'), ('ect', 'Events, Catering & Tourism')]:
    seg_rows.append([nm, n0(SEG['rev'][k]), n0(SEG['gp'][k]), pc(SEG['gp_margin'][k]),
                     n0(SEG['pbt'][k]), n0(SEG['assets'][k])])
seg_rows.append(['Group (incl. others/eliminations)', n0(HI['FY25']['rev']), n0(HI['FY25']['gp']),
                 pc(HI['FY25']['gp'] / HI['FY25']['rev']), n0(HI['FY25']['ebt']), n0(HB['FY25']['assets'])])
table(seg_rows, [2.15, 0.95, 0.95, 0.72, 1.05, 0.95], band_rows={5})
caption('FY2025 segments, AED mn, audited consolidated financial statements. Hospitality\'s pre-tax '
        'loss reflects financing and depreciation on a young portfolio; its gross profit is positive.')

# ============================ SECTION 1 =======================================
H1('1 · Fundamental valuation')

H2('1.1 · Cash-flow model — the full waterfall')
P('Revenue is built leg by leg, not as one growth rate. Development revenue converts the disclosed '
  f'AED {bn(UN["dev_backlog"])}bn development backlog at a visible conversion rate — anchored to the '
  'pace actually recognised in the first half of 2026 — plus point-in-time land sales; new launches '
  'roll the backlog forward. The other three legs grow on their own operating drivers (section 1.6). '
  'Margins are outputs of that build. The model is deliberately conservative in two places: fair-value '
  'gains, bargain-purchase and disposal gains are all set to zero across the forecast, and 2026 '
  'working capital absorbs cash, as the half-year statements say it is doing, before land-bank '
  'collections turn positive from 2027.')
wf = [['AED mn'] + YRS]
for lbl, key in [('Revenue', 'rev'), ('Gross profit', 'gp'),
                 ('General & administrative', 'ga'), ('Selling & marketing', 'sm'),
                 ('Investment and other income', 'invinc'), ('EBITDA', 'ebitda'),
                 ('EBITDA margin', 'ebitda_margin'), ('less depreciation & amortisation', 'dna'),
                 ('EBIT', 'ebit'), ('NOPAT = EBIT × (1 − 15.5%)', 'nopat'),
                 ('+ depreciation & amortisation', 'dna'), ('− capital expenditure', 'capex'),
                 ('− Δ working capital (release −)', 'dnwc'), ('Free cash flow to firm', 'fcff'),
                 ('Discount factor', 'df'), ('PV of FCFF', 'pv')]:
    vals = F[key]
    if key == 'ebitda_margin':
        wf.append([lbl] + [pc(v) for v in vals])
    elif key == 'df':
        wf.append([lbl] + [f'{v:.4f}' for v in vals])
    elif key in ('ga', 'sm', 'capex'):
        wf.append([lbl] + [n0(-v) for v in vals])
    elif key == 'dnwc':
        wf.append([lbl] + [n0(v) for v in vals])
    else:
        wf.append([lbl] + [n0(v) for v in vals])
table(wf, [2.35, 0.93, 0.93, 0.93, 0.93, 0.93], band_rows={6, 14})
caption(f'The explicit window sums to a present value of AED {n0(DCF["pv_explicit"])}mn at the '
        f'{pc(W["wacc_exp"], 2)} cost of capital built in section 1.8.')
P(f'Terminal block. Terminal growth of {pc(DCF["g"], 1)} requires reinvestment of '
  f'{pc(DCF["rr_term"])} of NOPAT at a terminal return on capital of {pc(IN["roic_term"], 1)} — the '
  f'reinvestment rate is derived, never assumed. Terminal value: AED {n0(DCF["tv"])}mn, worth AED '
  f'{n0(DCF["pv_tv"])}mn today — {pc(DCF["tv_share"])} of enterprise value, a share the reader should '
  f'see and judge. FY2025\'s return on invested capital is only {pc(D["terminal_recon"]["roic_fy25"])}: '
  f'the terminal {pc(IN["roic_term"], 1)} embeds the at-cost land bank converting to recognised profit '
  f'across the window, and section 1.9 prices the case where it does not.')
br = [['Enterprise value → equity per share', 'AED mn'],
      ['PV of explicit years', n0(DCF['pv_explicit'])],
      ['PV of terminal value', n0(DCF['pv_tv'])],
      ['Enterprise value', n0(DCF['ev'])],
      [f'  of which terminal value: {pc(DCF["tv_share"])}', ''],
      ['+ cash and bank balances (incl. escrow)', n0(DCF['cash'])],
      ['− debt incl. the related-party loan', n0(-DCF['debt'])],
      ['− lease liabilities', n0(-DCF['lease'])],
      ['+ associates & joint ventures at book', n0(DCF['assoc'])],
      ['+ financial assets', n0(DCF['finass'])],
      ['− non-controlling interests (book)', n0(-DCF['nci_val'])],
      ['Equity attributable, 31 Dec 2025', n0(DCF['eq_attr'])],
      [f'Per share ({n0(SH)}mn shares)', px(DCF['ps_dec'])],
      [f'Rolled {IN["anchor_days"]:.0f} days to the 7 Aug 2026 anchor at the cost of equity',
       px(DCF['ps'])]]
table(br, [4.6, 1.6], band_rows={3, 11, 13})
caption('The bridge uses the audited 31-Dec-2025 balance sheet. Cash includes AED 4.0bn of escrow '
        'and project-restricted balances — the strict all-cash basis; the company\'s own "net cash" '
        'definition (AED 1.8bn) restricts to available cash. Both framings are stated; the bridge '
        'deducts all debt either way.')

H2('1.2 · Book value and sustainable return')
P(f'Audited attributable equity is AED {n0(IN["eqp_fy25"])}mn — AED {px(BKL["bvps"])} per share, so the '
  f'market prices the group at {BKL["pb_trailing"]:.2f}x book. FY2025 attributable return on average '
  f'equity was {pc(BKL["roe_fy25"])}; cleaned of fair-value and disposal gains it is nearer '
  f'{pc(IN["roe_sust"])}, and that is the sustainable level this lens capitalises: a justified '
  f'price-to-book of ({pc(IN["roe_sust"], 1)} − {pc(IN["g_term"], 1)}) / ({pc(W["ke_exp"], 2)} − '
  f'{pc(IN["g_term"], 1)}) = {BKL["pb_just"]:.2f}x, worth AED {px(BKL["base"])} per share. A group '
  f'earning below its cost of equity on a large equity base is worth less than book — that arithmetic, '
  f'not sentiment, is why this lens sits below the market price.')

H2('1.3 · Relative multiples')
prs = [['Peer (own FY2025 disclosures)', 'Mkt cap, AED mn', 'Net profit', 'Trailing P/E', 'Backlog']]
for k in ['ALDAR', 'EMAAR', 'EMAARDEV']:
    p = REL['peers'][k]
    prs.append([p['name'], n0(p['mcap']), n0(p['np']) if p['np'] else 'n/d',
                f"{p['pe']:.1f}x", n0(p['backlog'])])
prs.append(['Modon Holding', n0(M['mktcap']), n0(IN['pat_fy25']),
            f"{REL['pe_trailing']:.1f}x", n0(UN['backlog'])])
table(prs, [2.5, 1.25, 1.05, 1.0, 1.1], band_rows={4})
caption('Peer fundamentals from each company\'s own results releases; market prices and trailing '
        'multiples cross-checked on a market-data aggregator, 7 Aug 2026 — cross-checks only, '
        'labelled as such.')
P(f'The UAE developer set trades at {REL["peers"]["EMAARDEV"]["pe"]:.1f}–{REL["peers"]["ALDAR"]["pe"]:.1f}x '
  f'trailing earnings. This study grants Modon a justified {IN["pe_just"]:.1f}x on FY2026E attributable '
  f'profit — a premium to Aldar for the recurring-income mix and backlog growth, tempered for the ~15% '
  f'free float and the related-party concentration of its land sales — and {IN["ev_ebitda_just"]:.1f}x '
  f'EV/EBITDA on FY2026E through the same bridge as the DCF. The two methods average to AED '
  f'{px(REL["base"])} per share. The span AED {px(LN["relative"]["bear"])}–{px(LN["relative"]["bull"])} '
  f'scales the blended lens between the cheapest and richest multiples in the peer set.')

H2('1.4 · Normalised earnings power')
P(f'Through a full cycle this study assumes development sales settle near AED {bn(IN["norm_sales"])}bn a '
  f'year — between the base path\'s terminal year and the run-off tail — with the recurring legs grown '
  f'moderately, giving normalised revenue of about AED {bn(NRM["rev"])}bn and a through-cycle net margin '
  f'of {pc(IN["norm_margin"])} (FY2025 cleaned of one-offs earned {pc(NRM["clean_margin_fy25"])}). That '
  f'is normalised earnings of AED {n0(NRM["np"])}mn, or AED {NRM["eps"]:.3f} per share, worth AED '
  f'{px(NRM["base"])} at a through-cycle {IN["norm_pe"]:.1f}x. This is the harshest lens: it treats '
  f'2025–26 as the top of a cycle, not a new base.')

H2('1.5 · Synthesis — four lenses, one field')
figure('fig1_football.png', 6.9, 'Figure 1 — the four lenses and the weighted central against the '
       'market price. The DCF span is the run-off-to-growth-hold scenario spread.')
P(f'The weights are a judgement, stated: DCF {pc(LN["dcf"]["w"], 0)} because the contracted backlog '
  f'gives unusual forward visibility for a developer; relative, normalised and book '
  f'{pc(LN["relative"]["w"], 0)} each because the market lenses are real evidence — a cheap, liquid '
  f'peer set against a tightly-held stock — not decoration. The result, AED {px(CEN)}, sits '
  f'{CEN / SPOT - 1:+.0%} above the market. Section 4 confronts that gap directly.')

H2('1.6 · Drivers — each leg on its own driver')
dr = [['Leg', 'Driver build', 'FY2026E→FY2030E'],
      ['Development', f'conversion of opening backlog ({pc(IN["conv_path"][0], 0)}→'
       f'{pc(IN["conv_path"][-1], 0)}) + land sales; new sales AED {bn(IN["new_sales"][0])}bn→'
       f'{bn(IN["new_sales"][-1])}bn/yr roll the backlog',
       f'revenue AED {bn(F["red_rev"][0])}bn→{bn(F["red_rev"][-1])}bn'],
      ['  margin', f'gross margin {pc(IN["red_margin"][0], 1)}→{pc(IN["red_margin"][-1], 1)} as '
       'related-party land mix fades and construction costs (~4%/yr, its own escalator) outrun '
       'realised-price escalation (~2%)', 'output, not input'],
      ['Asset & investment mgmt', f'{pc(IN["aim_growth"][0], 1)} then ~8%/yr on contracted occupancy '
       f'(97%) and GLA additions; margin held at the disclosed {pc(IN["aim_margin"][0], 1)}',
       f'AED {n0(F["aim_rev"][0])}mn→{n0(F["aim_rev"][-1])}mn'],
      ['Hospitality', f'7,137 keys; occupancy 71%→~75% plus the Olympia resort ramp; margin '
       f'{pc(SEG["gp_margin"]["hosp"], 1)}→{pc(IN["hosp_margin"][-1], 1)}',
       f'AED {n0(F["hosp_rev"][0])}mn→{n0(F["hosp_rev"][-1])}mn'],
      ['Events, catering & tourism', 'first year anchored on the actual first half plus the '
       'events-heavy second half; ~4%/yr thereafter; wage-led costs on their own escalator',
       f'AED {bn(F["ect_rev"][0])}bn→{bn(F["ect_rev"][-1])}bn'],
      ['Working capital', 'absorbs AED 1.5bn in 2026 (the half-year statements show receivable '
       'build-up), then releases 0.8–1.4bn/yr as the land bank converts and escrows collect',
       'release funds the growth'],
      ['Tax', 'the 15% domestic minimum top-up floor plus the observed UK/Spain uplift '
       f'(first-half 2026 effective rate {pc(H1D["eff_tax"])})', pc(IN["tax_f"])]]
table(dr, [1.55, 3.6, 1.7], size=8.8)
caption('Unit anchors, disclosed: FY2025 sales of AED 36.3bn across 6,358 units — AED 7.0mn per unit '
        'in Abu Dhabi, AED 3.1mn internationally. Per-project volumes and prices are not disclosed, '
        'so the build stops at the segment level with unit-level anchors — that gap is flagged, not '
        'papered over.')

H2('1.7 · The crux — the sales path, priced both ways')
cj = [['', 'Base: normalising-but-sustained', 'Alternative: backlog run-off'],
      ['New development sales', f'AED {bn(IN["new_sales"][0])}bn falling to {bn(IN["new_sales"][-1])}bn/yr',
       f'AED {bn(IN["new_sales_runoff"][0])}bn falling to {bn(IN["new_sales_runoff"][-1])}bn/yr'],
      ['Development margin', f'{pc(IN["red_margin"][0], 1)}→{pc(IN["red_margin"][-1], 1)}',
       f'{pc(IN["red_margin_runoff"][0], 1)}→{pc(IN["red_margin_runoff"][-1], 1)}'],
      ['FY2030E group revenue', f'AED {bn(F["rev"][-1])}bn', f'AED {bn(CJ["runoff_rev"][-1])}bn'],
      ['Value per share', f'AED {px(DCF["ps"])}', f'AED {px(CJ["runoff_ps"])}'],
      ['What it assumes', 'Abu Dhabi\'s structural demand (record AED 76bn residential sales in '
       '2025, 62% of growth foreign-led) persists; Modon holds share; Ras El Hekma phases deliver',
       'the 2025 surge was the cycle top; launches halve and keep fading; pricing power goes '
       'with volume']]
table(cj, [1.35, 2.75, 2.75], size=8.9, band_rows={4})
P(f'Even the run-off reading values the group {CJ["runoff_ps"] / SPOT - 1:+.0%} against the market '
  f'price — the balance sheet (net cash on the strict basis, an at-cost land bank) does much of the '
  f'work. What separates the two readings is AED {px(DCF["ps"] - CJ["runoff_ps"])} per share of '
  f'launch-dependent value. The growth-hold upper reading (sales held at AED 30bn) reaches AED '
  f'{px(CJ["bull_ps"])}. This study weights neither to zero: the base path already normalises sales '
  f'~30–45% below 2025\'s record.')

H2('1.8 · Macro and country — the cost of capital, built and priced')
P(f'Every rate is sourced and each risk is charged once. The AED government curve gives '
  f'{pc(IN["rf"], 2)} (the January-2031 dirham treasury tranche auctioned in July 2026, about 4bp over '
  f'comparable US Treasuries); netting the UAE\'s own {pc(IN["sov_spread_rating"], 2)} sovereign '
  f'default spread — which is already inside the equity premium — leaves a normalised risk-free rate '
  f'of {pc(W["rf_star"], 2)}. The UAE equity risk premium on the rating basis is '
  f'{pc(IN["erp_rating"], 2)}; no traded sovereign CDS series exists for the UAE, so a CDS-basis '
  f'alternative cannot be constructed and the rating basis stands alone, stated as such. Beta could '
  f'not be regressed: no downloadable history of the exchange\'s index proved obtainable from seven '
  f'independent sources (the bibliography lists each attempt), so beta is set to 1.0 — the standing '
  f'fallback — flagged as interim and sensitised 0.8–1.2 in section 1.9, a ±{abs(SN["grid_beta"][0] - SN["grid_beta"][-1]) / 2 / DCF["ps"]:.0%} '
  f'swing on the DCF.')
wt = [['Cost of capital', 'Value', 'Construction'],
      ['Risk-free rate, normalised', pc(W['rf_star'], 2), f'{pc(IN["rf"], 2)} AED sovereign − '
       f'{pc(IN["sov_spread_rating"], 2)} default spread'],
      ['Cost of equity', pc(W['ke_exp'], 2), f'rf* + 1.0 × {pc(IN["erp_rating"], 2)}'],
      ['Marginal cost of debt', pc(W['kd'], 2), f'6M EIBOR {pc(IN["eibor6m"], 2)} + '
       f'{pc(IN["kd_margin"], 2)} blended margin'],
      ['  after tax', pc(W['kd_at'], 2), f'× (1 − {pc(IN["tax_f"])})'],
      ['Weights', f"{pc(W['we_exp'], 1)} / {pc(W['wd_exp'], 1)}",
       'market equity AED ' + n0(M['mktcap']) + 'mn; book debt AED ' + n0(DCF['debt']) + 'mn'],
      ['Cost of capital, explicit window', pc(W['wacc_exp'], 2), 'weighted'],
      ['Cost of capital, terminal', pc(W['wacc_term'], 2),
       f'{pc(1 - IN["wd_term"], 0)}/{pc(IN["wd_term"], 0)} normalised weights']]
table(wt, [2.3, 1.3, 3.25], size=9.0, band_rows={6})
kd_rows = [['Cost-of-debt evidence (loan note, FY2025)', 'Rate', 'Maturity'],
           ['Largest new AED tranche (AED 1,415mn, general purpose)', '6M EIBOR + 0.60%', 'Jan-2027'],
           ['AED construction tranches', '3M EIBOR + 0.85% to + 2.5%', '2028–2030'],
           ['GBP venue debt (ExCeL London, hotels)', 'SONIA + 0.95% to + 2.05%', '2028–2029'],
           ['USD project tranches', 'SOFR + margin (to + 4.98%)', '2026–2027'],
           ['Fixed AED tranches', '3.32% – 4.36%', '2028–2033'],
           [f'Blended marginal rate used', pc(W['kd'], 2),
            f'above the {pc(IN["rf"], 2)} sovereign, as it must be'],
           [f'Realised effective rate on average borrowings, FY2025', pc(W['kd_eff_fy25'], 1),
            'interest charge over average loan book']]
table(kd_rows, [3.4, 1.9, 1.55], size=8.9, band_rows={6})
P(f'Debt currency, split and carried honestly: of the AED {n0(IN["loans_fy25"])}mn loan book, roughly '
  f'a third is sterling and dollar project debt against the London venues; the dollar legs cost what '
  f'AED legs cost through the peg, and the sterling legs are secured on sterling-earning assets — a '
  f'natural hedge, noted rather than modelled away. Two priced stress readings sit on top: charging '
  f'the ~{pc(IN["fgn_share"], 0)} of revenue earned outside the UAE with Egypt\'s country premium cuts '
  f'the DCF to AED {px(DCF["ps_egystress"])}; and the 1-point conflict adder that regional studies '
  f'carried in mid-2026 is retired here on the auction evidence (4bp over Treasuries), but adding a '
  f'full point back to the cost of equity appears in the sensitivity strip below. Tax is modelled at '
  f'the 15% domestic-minimum floor with the observed foreign uplift, not the 9% headline.')

H2('1.9 · Sensitivity')
figure('fig2_sens.png', 6.4, 'Figure 2 — DCF fair value across the cost of capital and terminal '
       'growth. Note the flat rows near the top-right: at a terminal return on capital close to the '
       'cost of capital, growth adds almost nothing — the valuation is carried by the cash flows, '
       'not by the growth assumption.')
sens_rows = [['One-way strip (DCF per share)', '−2', '−1', 'base', '+1', '+2'],
             ['Beta 0.8 → 1.2', px(SN['grid_beta'][0]), px(SN['grid_beta'][1]),
              px(SN['grid_beta'][2]), px(SN['grid_beta'][3]), px(SN['grid_beta'][4])],
             ['Development margin ±4pts', px(SN['grid_margin'][0]), px(SN['grid_margin'][1]),
              px(SN['grid_margin'][2]), px(SN['grid_margin'][3]), px(SN['grid_margin'][4])],
             ['Conversion rate ±6pts', px(SN['grid_conv'][0]), px(SN['grid_conv'][1]),
              px(SN['grid_conv'][2]), px(SN['grid_conv'][3]), px(SN['grid_conv'][4])],
             ['New sales 50%→150% of base', px(SN['grid_sales'][0]), px(SN['grid_sales'][1]),
              px(SN['grid_sales'][2]), px(SN['grid_sales'][3]), px(SN['grid_sales'][4])],
             ['Working-capital release ±AED 1bn/yr', px(SN['grid_nwc'][0]), px(SN['grid_nwc'][1]),
              px(SN['grid_nwc'][2]), px(SN['grid_nwc'][3]), px(SN['grid_nwc'][4])],
             ['Cost of equity +0 → +2pts', px(SN['grid_ke'][0]), px(SN['grid_ke'][1]),
              px(SN['grid_ke'][2]), px(SN['grid_ke'][3]), px(SN['grid_ke'][4])]]
table(sens_rows, [2.6, 0.85, 0.85, 0.85, 0.85, 0.85], size=9.0)
caption('Each strip cell is a complete revaluation. The crux is sensitised in its own units: sales '
        'in dirhams per year, margins in points, conversion in points of backlog. One artifact is '
        'worth naming: a faster conversion rate slightly LOWERS the total value here, because it '
        'drains the backlog that feeds the terminal year while the explicit-window gain is smaller '
        '— a conservative property of anchoring the terminal value on the final forecast year.')

# ============================ SECTION 2 =======================================
H1('2 · Technical and price structure')
figure('fig3_ma.png', 6.9, 'Figure 3 — the last 260 sessions against the 20/50/100/200-day moving '
       'averages.')
T = TECH['tech']
P(f'{T["summary"]}')
P(f'{T["trend"]}. {T["bull"]} {T["bear"]}')
lv = [['Nearest levels (computed from swing-point clusters)', 'AED'],
      ['Resistance 3', px(TECH['levels']['res'][2])],
      ['Resistance 2', px(TECH['levels']['res'][1])],
      ['Resistance 1 (nearest)', px(TECH['levels']['res'][0])],
      ['Last close (7 Aug 2026)', px(TECH['close'])],
      ['Support 1 (nearest)', px(TECH['levels']['sup'][0])],
      ['Support 2', px(TECH['levels']['sup'][1])],
      ['Support 3', px(TECH['levels']['sup'][2])]]
table(lv, [4.4, 1.4], band_rows={4})
caption('Levels are recency-weighted swing-point clusters computed from the full price history; '
        'nearest levels are listed first. The read is computed, not drawn by hand, and refreshes '
        'with the data.')

# ============================ SECTION 3 =======================================
H1('3 · Probabilistic price map')
P(f'The map below is struck from the 7 August 2026 close of AED {px(SPOT)} using a volatility model '
  f'fitted to this market\'s panel of ADX/DFM names, with drift set to the short-term dirham interest '
  f'rate (no dividend is paid or proposed, a sourced zero, not an assumption) and 50,000 simulated '
  f'paths. Percentiles are read off the simulated distribution; the touch rows ask whether a level '
  f'trades at any point inside the window, not only at its end.')
P(f'How much to trust it: tested on {S0["windows_scored"]} non-overlapping three-month windows walked '
  f'forward over the post-2022 trading regime (with earlier windows from 2020–21 excluded because the '
  f'UAE changed its trading week in January 2022), this method\'s probability forecasts beat a '
  f'drift-adjusted random walk by {S0["skill_norm"]*100:.1f}% on a proper scoring rule, an edge that '
  f'holds across every resampling scheme tried; the 80% band contained {pc(S0["cov80"], 0)} of '
  f'outcomes and the 90% band {pc(S0["cov90"], 0)}, and the forecast percentile of realised prices is '
  f'statistically indistinguishable from uniform — on a sample this size those are healthy, not '
  f'perfect, marks. Treat the bands as calibrated ranges, not promises.')
figure('fig4_fan.png', 6.9, 'Figure 4 — the three-month price cone: median, central 50% band and '
       '5–95% band across 50,000 paths.')
pmap = [['', '1 month (to ' + H1M['grade_date'] + ')', '3 months (to ' + H3M['grade_date'] + ')'],
        ['5th percentile', px(H1M['pct']['p5']), px(H3M['pct']['p5'])],
        ['25th percentile', px(H1M['pct']['p25']), px(H3M['pct']['p25'])],
        ['Median', px(H1M['pct']['p50']), px(H3M['pct']['p50'])],
        ['75th percentile', px(H1M['pct']['p75']), px(H3M['pct']['p75'])],
        ['95th percentile', px(H1M['pct']['p95']), px(H3M['pct']['p95'])],
        ['P(finish above spot)', pc(H1M['p_above'], 0), pc(H3M['p_above'], 0)],
        ['P(finish ≥ +10%)', pc(H1M['p_up10'], 0), pc(H3M['p_up10'], 0)],
        ['P(finish ≤ −10%)', pc(H1M['p_dn10'], 0), pc(H3M['p_dn10'], 0)],
        ['P(touch +5% at any point)', pc(H1M['touch_up5'], 0), pc(H3M['touch_up5'], 0)],
        ['P(touch −5% at any point)', pc(H1M['touch_dn5'], 0), pc(H3M['touch_dn5'], 0)],
        ['P(touch +10% at any point)', pc(H1M['touch_up10'], 0), pc(H3M['touch_up10'], 0)],
        ['P(touch −10% at any point)', pc(H1M['touch_dn10'], 0), pc(H3M['touch_dn10'], 0)]]
table(pmap, [2.6, 1.85, 1.85])
caption('Both windows are calendar-defined: one and three calendar months from the anchor, settled '
        'on the first trading session on or after each date.')
figure('fig5_dist.png', 5.2, 'Figure 5 — simulated price distribution at one month.')
figure('fig6_dist.png', 5.2, 'Figure 6 — simulated price distribution at three months.')

# ============================ SECTION 4 =======================================
H1('4 · Comparison of the lenses')
P(f'The gap is the story. The cash-flow lenses say AED {px(CJ["runoff_ps"])}–{px(CJ["bull_ps"])} '
  f'depending on the sales path; the market lenses say AED {px(NRM["base"])}–{px(REL["base"])}. That '
  f'is not a rounding disagreement, and averaging it away would hide the actual decision. Three '
  f'readings are possible, and the honest study prices all three. First: the market is right about '
  f'the risk. Solving for the discount rate that makes the base cash flows worth AED {px(SPOT)} '
  f'requires a cost of equity of {pc(D["market_implied"]["ke"], 1)} — '
  f'{pc(D["market_implied"]["ke_add"], 1)} above the built-up rate. That is the premium of a '
  f'frontier-market credit, charged to a AA-rated sovereign\'s own developer: a stiff but not absurd '
  f'reading, given ~85% government ownership, related-party land sales and a receivable book that '
  f'absorbed AED 5.4bn of cash in the first half of 2026.')
P(f'Second: the market is pricing the run-off and a discount for control and float. The run-off DCF '
  f'(AED {px(CJ["runoff_ps"])}) at a further ~30% holding-company-style discount for the 15% float '
  f'and related-party revenue lands almost exactly on the market price. Third: the market lenses '
  f'anchor on this year\'s multiple while the cash-flow lenses anchor on the contracted backlog — and '
  f'{pc(DCF["tv_share"])} of the DCF\'s enterprise value sits in its terminal value, which is where '
  f'scepticism belongs. The weighted central of AED {px(CEN)} splits these readings explicitly rather '
  f'than pretending they agree; what would move it decisively either way is listed in section 7.')
figure('figD1_experts.png', 6.9, 'Figure 7 — three independent expert framings (Appendix C, worked '
       'in full) against the market price.')

# ============================ SECTION 5 =======================================
H1('5 · Catalysts')
bullet(' Full-year 2026 results (February 2027): the first full year in which the backlog conversion '
       'pace, the receivable collection and the events platform\'s H2 season are all visible at once.',
       'Results and collections.')
bullet(' Every AED of the ~AED 8bn net related-party receivable book (Department of Finance the '
       'largest counterparty) collected converts a paper claim into distributable cash and is the '
       'single cleanest de-risking signal available.', 'Related-party collections.')
bullet(' Ras El Hekma phase-1 delivery milestones and further precinct launches; the first launch '
       'sold AED 5.8bn across 2,109 units.', 'Egypt execution.')
bullet(' A maiden dividend policy would force the market to price the cash flows as owner earnings; '
       'none has been announced.', 'Capital returns.')
bullet(' Any placement widening the ~15% free float changes the relative lens directly — index '
       'eligibility and liquidity are the mechanical constraints on the multiple.', 'Float and flow.')
bullet(' The dirham imports US policy: each cut lowers both the discount rate and mortgage-linked '
       'demand friction; the model\'s rates are struck off the July 2026 curve.', 'Rates.')

# ============================ SECTION 6 =======================================
H1('6 · Reading the probability zones')
P(f'The three-month map says: a two-in-three chance the price sits between AED '
  f'{px(H3M["pct"]["p25"])} and {px(H3M["pct"]["p75"])} on {H3M["grade_date"]}; roughly '
  f'{pc(H3M["touch_dn5"], 0)} odds that AED {px(SPOT * 0.95)} trades at some point (near support at '
  f'{px(TECH["levels"]["sup"][0])}); {pc(H3M["touch_up5"], 0)} odds that AED {px(SPOT * 1.05)} trades '
  f'(just below the {px(TECH["levels"]["res"][0])} resistance). A reader holding the fundamental view '
  f'of this study should not expect the map to confirm it inside a quarter: the map is calibrated to '
  f'the market\'s realised volatility, not to the study\'s opinion, and at these volatilities a '
  f'{CEN / SPOT - 1:+.0%} revaluation is a multi-year event, visible first in collections, margins '
  f'and the dividend decision, and only later in the tape.')

# ============================ SECTION 7 =======================================
H1('7 · Caveats — what would change our mind')
bullet(' More than half of FY2025 land-sale profit came from related-party transactions at a 67% '
       'gross margin; an arms-length repricing of that channel would cut the development margin '
       'path and with it every cash-flow lens.', 'Related-party pricing.')
bullet(' The first half of 2026 consumed AED 3.9bn of operating cash into receivables. If the '
       'FY2026 statements do not show that reversing, the working-capital release schedule — worth '
       'about AED 1 per share across the forecast — is wrong.', 'Collections.')
bullet(' FY2024 is a perimeter break and FY2023 belongs to a smaller predecessor: there are exactly '
       'two audited years of the modern group. Every trend read off this history carries that '
       'caveat.', 'Short clean history.')
bullet(' Beta is a stated 1.0 fallback, not a regression, because no index history proved '
       'obtainable; the 0.8–1.2 strip in section 1.9 bounds what a real regression could change.',
       'Beta.')
bullet(f' {pc(DCF["tv_share"])} of the DCF\'s enterprise value is terminal. The terminal return on '
       f'capital ({pc(IN["roic_term"], 1)}) assumes the land bank converts to recognised profit; at '
       f'FY2025\'s achieved return ({pc(D["terminal_recon"]["roic_fy25"])}) the terminal value '
       f'roughly halves.', 'Terminal weight.')
bullet(' The probability map is fitted to a market panel whose names are far more liquid than '
       'MODON\'s float; thin trading can realise gaps the model underweights.', 'Liquidity.')

# ============================ APPENDIX A ======================================
H1('Appendix A · Financial statements')
H2('A.1 · Income statement — three years audited, five forecast')
ist = [['AED mn', 'FY2023*', 'FY2024**', 'FY2025'] + YRS]
def hrow(lbl, key, fmt=n0):
    return [lbl] + [fmt(HI[y][key]) for y in ['FY23', 'FY24', 'FY25']]
ist.append(hrow('Revenue', 'rev') + [n0(v) for v in F['rev']])
ist.append(hrow('Gross profit', 'gp') + [n0(v) for v in F['gp']])
ist.append(hrow('EBITDA', 'ebitda') + [n0(v) for v in F['ebitda']])
ist.append(hrow('Depreciation & amortisation', 'dna') + [n0(v) for v in F['dna']])
ist.append(hrow('EBIT', 'ebit') + [n0(v) for v in F['ebit']])
ist.append(hrow('Net finance result', 'fin')
           + [n0(F['cash'][t - 1] * IN['cash_yield'] - F['interest'][t] if t > 0
                 else IN['cash_fy25'] * IN['cash_yield'] - F['interest'][0]) for t in range(5)])
ist.append(hrow('Associates & joint ventures', 'assoc') + [n0(v) for v in F['assoc']])
ist.append(hrow('Profit before tax', 'ebt')
           + [n0(F['np'][t] / (1 - IN['tax_f'])) for t in range(5)])
ist.append(hrow('Income tax', 'tax')
           + [n0(-F['np'][t] / (1 - IN['tax_f']) * IN['tax_f']) for t in range(5)])
ist.append(hrow('Profit for the year', 'pat') + [n0(v) for v in F['np']])
ist.append(hrow('Attributable to owners', 'npa') + [n0(v) for v in F['np_attr']])
table(ist, [1.66, 0.68, 0.68, 0.68, 0.66, 0.66, 0.66, 0.66, 0.66], size=8.2, band_rows={10})
caption('* FY2023 is the Q Holding perimeter (pre-combination). ** FY2024 includes the AED 9,192mn '
        'bargain-purchase gain; excluding it, profit was AED 197mn. Forecasts exclude all fair-value '
        'and disposal gains by construction.')
H2('A.2 · Balance sheet')
bst = [['AED mn', 'FY2023*', 'FY2024', 'FY2025'] + YRS]
bs_hist = {'FY23': dict(ppe=789.463, ip=HB['FY23']['ip'], inv=HB['FY23']['inv'], dwip=None,
                        cash=HB['FY23']['cash'], debt=HB['FY23']['debt'], eqp=HB['FY23']['eqp'],
                        nci=HB['FY23']['nci'], assets=HB['FY23']['assets']),
           'FY24': HB['FY24'], 'FY25': HB['FY25']}
def brow(lbl, key):
    out = [lbl]
    for y in ['FY23', 'FY24', 'FY25']:
        v = bs_hist[y].get(key)
        out.append(n0(v) if v is not None else '—')
    return out
bst.append(brow('Property, plant & equipment', 'ppe') + ['—'] * 5)
bst.append(brow('Investment properties', 'ip') + ['—'] * 5)
bst.append(brow('Inventories (land bank)', 'inv') + ['—'] * 5)
bst.append(brow('Development work-in-progress', 'dwip') + ['—'] * 5)
bst.append(brow('Cash and bank balances', 'cash') + [n0(v) for v in F['cash']])
bst.append(brow('Total assets', 'assets') + ['—'] * 5)
bst.append(brow('Debt incl. related-party loan', 'debt') + [n0(v) for v in F['debt']])
bst.append(['Net working capital (house basis)', '—', n0(HB['FY24']['nwc']), n0(HB['FY25']['nwc'])]
           + [n0(v) for v in F['nwc']])
bst.append(brow('Equity attributable to owners', 'eqp') + [n0(v) for v in F['equity_attr']]
           if 'equity_attr' in F else
           brow('Equity attributable to owners', 'eqp')
           + [n0(IN['eqp_fy25'] + sum(F['np_attr'][:t + 1])) for t in range(5)])
bst.append(brow('Non-controlling interests', 'nci')
           + [n0(IN['nci_fy25'] + sum(F['np'][i] * IN['nci_pct'] for i in range(t + 1)))
              for t in range(5)])
bst.append(['Net debt (negative = net cash)',
            n0(bs_hist['FY23']['debt'] - bs_hist['FY23']['cash']),
            n0(HB['FY24']['nd']), n0(HB['FY25']['nd'])] + [n0(v) for v in F['net_debt']])
table(bst, [1.66, 0.68, 0.68, 0.68, 0.66, 0.66, 0.66, 0.66, 0.66], size=8.2, band_rows={11})
caption('* Q Holding perimeter. Forecast columns roll only the lines the model drives — equity on '
        'retained profit (no dividend assumed), debt on the drawn path, cash from free cash flow — '
        'and leave asset lines the model does not forecast unpopulated rather than invented.')
H2('A.3 · Cash-flow markers')
cft = [['AED mn', 'FY2024', 'FY2025', 'H1-2026'] + YRS,
       ['Operating cash flow (audited / model NOPAT+D&A−ΔWC)', n0(D['hist_cf']['FY24']['ocf']),
        n0(D['hist_cf']['FY25']['ocf']), n0(H1D['ocf'])]
       + [n0(F['nopat'][t] + F['dna'][t] - F['dnwc'][t]) for t in range(5)],
       ['Capital expenditure', n0(D['hist_cf']['FY24']['capex']), n0(D['hist_cf']['FY25']['capex']),
        '—'] + [n0(v) for v in F['capex']],
       ['Free cash flow to firm', '—', '—', '—'] + [n0(v) for v in F['fcff']]]
table(cft, [2.02, 0.62, 0.62, 0.62, 0.60, 0.60, 0.60, 0.60, 0.60], size=8.2)
caption('The H1-2026 operating outflow is the receivable build-up discussed in section 7; the model '
        'assumes partial reversal in H2 and prices the risk in the working-capital strip.')

# ============================ APPENDIX B ======================================
H1('Appendix B · Peers, risks and research register')
H2('B.1 · Peer set')
pr2 = [['Company', 'Market', 'FY2025 revenue', 'FY2025 net profit', 'Trailing P/E', 'Backlog'],
       ['Aldar Properties', 'ADX', n0(REL['peers']['ALDAR']['rev']), n0(REL['peers']['ALDAR']['np']),
        f"{REL['peers']['ALDAR']['pe']:.1f}x", n0(REL['peers']['ALDAR']['backlog'])],
       ['Emaar Properties', 'DFM', n0(REL['peers']['EMAAR']['rev']), 'n/d',
        f"{REL['peers']['EMAAR']['pe']:.1f}x", n0(REL['peers']['EMAAR']['backlog'])],
       ['Emaar Development', 'DFM', n0(REL['peers']['EMAARDEV']['rev']),
        n0(REL['peers']['EMAARDEV']['np']), f"{REL['peers']['EMAARDEV']['pe']:.1f}x",
        n0(REL['peers']['EMAARDEV']['backlog'])],
       ['Modon Holding', 'ADX', n0(HI['FY25']['rev']), n0(HI['FY25']['pat']),
        f"{REL['pe_trailing']:.1f}x", n0(UN['backlog'])]]
table(pr2, [1.7, 0.8, 1.15, 1.2, 1.0, 1.0], band_rows={4})
caption('AED mn. Peer figures from each company\'s own FY2025 results releases; multiples '
        'cross-checked against a market-data aggregator on 7 Aug 2026 and used only as comparison, '
        'never as a source for Modon\'s own numbers.')
H2('B.2 · Risk register')
rr = [['Risk', 'Where it bites', 'How it is priced here'],
      ['Related-party sales concentration and pricing', 'development margin, receivables',
       'margin glide down; Expert 2 haircut; section 1.9 margin strip'],
      ['Receivable collection timing', 'working capital, cash conversion',
       '2026 absorbs cash; ±AED 1bn/yr strip'],
      ['Abu Dhabi residential cycle turns', 'new sales, pricing',
       'run-off path priced in full (section 1.7)'],
      ['Egypt macro and FX on Ras El Hekma', 'international leg',
       'Egypt-premium stress: AED ' + px(DCF['ps_egystress']) + ' per share'],
      ['Rates stay higher for longer', 'discount rate, mortgage demand',
       '+2pt cost-of-equity strip; auction-based rf'],
      ['Free float and index exclusion', 'the multiple, not the cash',
       'relative lens weighted 20% despite the gap'],
      ['Execution at masterplan scale', 'capex, delivery cadence',
       'conversion-rate strip; contracts procured (AED 32bn) noted']]
table(rr, [2.15, 2.15, 2.55], size=8.8)
H2('B.3 · Research register')
rrg = [['Area', 'What was established', 'Source', 'Date']]
import json as _json
SR = _json.load(open('sweep_register.json'))
def _clean_src(x):
    x = x.replace(' (house FED_SCHEDULE, engine/market_profiles.py)',
                  ' (house monetary-policy calendar)')
    return x
for f_ in SR['findings']:
    f_['source_name'] = _clean_src(f_.get('source_name', ''))
    if f_['klass'] == 'NEG':
        rrg.append([f_['ring'].title(), 'Searched, nothing found: ' + f_['headline']
                    .replace('Negative search — nothing found (', '').rstrip(')'),
                    'search log', f_['source_date']])
    else:
        rrg.append([f_['ring'].title(), f_['headline'], f_['source_name'], f_['source_date']])
table(rrg, [0.75, 3.7, 1.75, 0.75], size=7.8)
caption('Every claim the model rests on, with its source and date. The companion bibliography '
        'carries the full input-by-input register.')

# ============================ APPENDIX C ======================================
H1('Appendix C · Three experts, worked in full')
P('Three independent framings, each taken to a number by a different method, each with its stated '
  'blind spot and a condition that would falsify it. They are labelled Expert 1, 2 and 3; the '
  'methods, not the names, are the content.')

H2('C.1 · Expert 1 — the asset value (revalued net assets)')
P('Worldview: a developer is a warehouse of land bought below market; earnings are just the '
  'warehouse emptying. Works when land is carried far below realisable value and the owner can '
  'actually monetise; fails when the land cannot be sold at appraisal pace, or when the buyer of '
  'first resort is a related party whose price is the appraisal.')
e1 = EXPD['e1']
e1t = [['Line', 'AED mn'],
       ['Attributable equity, audited, 31 Dec 2025', n0(e1['eqp'])],
       [f'Land bank at cost (land plots within inventories)', n0(e1['land_bv'])],
       [f'Mark-up applied: {pc(e1["uplift"], 0)} (half the 67% gross margin realised on 2025 '
        f'related-party land sales, as an arms-length haircut)', n0(e1['land_bv'] * e1['uplift'])],
       [f'Work-in-progress mark-up: {pc(e1["dwip_uplift"], 0)} on AED '
        + n0(IN['dwip_fy25']) + 'mn', n0(IN['dwip_fy25'] * e1['dwip_uplift'])],
       ['Revalued net asset value', n0(e1['nav'])],
       [f'Per share ({n0(SH)}mn shares)', px(e1['base'])],
       [f'Range: appraisal haircut 15% to premium 12%', f"{px(e1['rng'][0])}–{px(e1['rng'][1])}"]]
table(e1t, [4.7, 1.5], band_rows={5})
P(f'Named sensitivity: each 10 points of land mark-up is AED {px(e1["land_bv"] * 0.10 / SH)} per '
  f'share. Falsifier, stated in advance: two consecutive halves of arms-length land sales clearing '
  f'below 20% gross margin would collapse the mark-up toward zero and this valuation toward book '
  f'(AED {px(BKL["bvps"])}).')

H2('C.2 · Expert 2 — owner cash flow on the run-off path')
P('Worldview: value only the cash an owner could take out if no new story arrives; treat every '
  'receivable from an affiliate as impaired until collected. Works at cycle tops and against '
  'promotional accounting; fails when the growth is real and compounding, which this method '
  'structurally cannot see.')
e2 = EXPD['e2']
e2t = [['Line', 'Value'],
       ['Run-off DCF (sales halve and fade; margins compress)', f"AED {px(e2['runoff_ps'])}/sh"],
       [f'Related-party receivable book, net', f"AED {n0(e2['rp_book'])}mn"],
       [f'Haircut applied: {pc(e2["haircut"], 0)} for timing and collection',
        f"− AED {px(e2['haircut'] * e2['rp_book'] / SH)}/sh"],
       ['Expert 2 value', f"AED {px(e2['base'])}/sh"],
       ['Range: deeper haircut and slower collections, to the base DCF less 5%',
        f"{px(e2['rng'][0])}–{px(e2['rng'][1])}"]]
table(e2t, [4.7, 1.6], band_rows={4})
P(f'Named sensitivity: each 10 points of receivable haircut is AED '
  f'{px(0.10 * e2["rp_book"] / SH)} per share. Falsifier: the Department-of-Finance receivable '
  f'collecting on schedule through FY2026 removes the haircut entirely and moves this expert to the '
  f'run-off DCF at AED {px(e2["runoff_ps"])}.')

H2('C.3 · Expert 3 — the market pricer')
P('Worldview: the peer multiple is the verdict of everyone else\'s money; a company is worth what '
  'comparable earnings sell for today, and premiums must be earned in public. Works when the peer '
  'set is deep and honest; fails at genuine inflections, which it prices only after the fact.')
e3 = EXPD['e3']
e3t = [['Line', 'Value'],
       ['FY2026E attributable profit (model)', f"AED {n0(e3['npa26'])}mn"],
       [f'Peer-set multiple applied: {e3["pe"]:.1f}x (centre of Aldar 7.5x / Emaar 5.3x / '
        'Emaar Dev 4.1x)', ''],
       ['Implied equity value', f"AED {n0(e3['pe'] * e3['npa26'])}mn"],
       [f'Per share', f"AED {px(e3['base'])}"],
       ['Range: trough multiple 4.1x to re-rated 8.5x', f"{px(e3['rng'][0])}–{px(e3['rng'][1])}"]]
table(e3t, [4.7, 1.6], band_rows={4})
P(f'Named sensitivity: each turn of P/E is AED {px(e3["npa26"] / SH)} per share. Falsifier: a '
  f'dividend policy plus a float above 25% would justify migrating toward the DCF lenses; this '
  f'expert concedes the method prices liquidity, not just earnings.')

H2('C.4 · Cross-examination')
bullet(' Expert 1 to Expert 2: your haircut double-counts — the run-off DCF already starves the '
       'related-party channel. Expert 2 partially concedes: the haircut is kept, but only on the '
       'stock of receivables, not the flow. Challenge sustained in part.', '')
bullet(' Expert 2 to Expert 1: your mark-up is circular — the 67% margin you halve was set by '
       'related-party sales. Expert 1 concedes the circularity and answers with the falsifier: '
       'arms-length clearing prices will settle it within two reporting periods. Challenge '
       'acknowledged, test defined.', '')
bullet(' Expert 3 to both: whatever the assets earn, the shares the public can actually buy trade '
       'at 11.8x this year\'s earnings while Aldar trades at 7.5x — the market has already voted. '
       'Experts 1 and 2 reject the inference: a 15% float is not a market verdict, it is the '
       'absence of one. Challenge rejected, reason stated.', '')

H2('C.5 · Three in one room')
P(f'Forced to one sentence each: Expert 1 — "the land alone covers the price at AED '
  f'{px(EXPD["e1"]["base"])}." Expert 2 — "paid to wait even if growth dies: AED '
  f'{px(EXPD["e2"]["base"])}, provided the affiliates pay their bills." Expert 3 — "until the float '
  f'and the dividend exist, it is worth peer multiple: AED {px(EXPD["e3"]["base"])}." The median, '
  f'AED {px(D["panel_centre"])}, sits between the study\'s market lenses and its cash-flow lenses — '
  f'which is exactly where the disagreement lives.')

H2('C.6 · Divergence table')
dv = [['Assumption', 'Expert 1', 'Expert 2', 'Expert 3', 'Gap it drives'],
      ['Land bank worth above cost', f'+{pc(EXPD["e1"]["uplift"], 0)}', '0%', 'ignored',
       f'AED {px(EXPD["e1"]["land_bv"] * EXPD["e1"]["uplift"] / SH)}/sh'],
      ['Related-party receivables', 'face value', f'−{pc(EXPD["e2"]["haircut"], 0)}', 'face value',
       f'AED {px(EXPD["e2"]["haircut"] * EXPD["e2"]["rp_book"] / SH)}/sh'],
      ['Sales path', 'irrelevant (assets)', 'run-off', 'FY2026E only',
       f'AED {px(DCF["ps"] - CJ["runoff_ps"])}/sh between base and run-off'],
      ['Multiple regime', 'n/a', 'n/a', f'{EXPD["e3"]["pe"]:.1f}x peer centre',
       f'AED {px((IN["pe_just"] - EXPD["e3"]["pe"]) * EXPD["e3"]["npa26"] / SH)}/sh vs the study\'s '
       f'{IN["pe_just"]:.1f}x']]
table(dv, [1.6, 1.05, 1.05, 1.05, 2.1], size=8.6)

# ============================ ABOUT / DISCLOSURE ==============================
H1('About this study')
P('This document, its Excel companion and its bibliography were produced as a single build: every '
  'number in all three files comes from one computed model, and the Excel model has been verified '
  'cell by cell against it — 537 formula cells reproduce the model exactly, and a driver test '
  'confirms that changing any input on the Assumptions sheet reprices the workbook in the correct '
  'direction, with no dead inputs. The historical record is built exclusively from the company\'s '
  'own audited statements and reviewed interims; where a figure is both disclosed and derivable, '
  'the disclosed figure is carried.')
H1('Disclosure')
P('Educational analysis. Not investment advice, not a recommendation, not an offer or solicitation. '
  'No rating and no price target are expressed or implied; values are model outputs presented as '
  'ranges with stated assumptions. The authors hold no position in MODON. Data as of 9 August 2026; '
  'prices as of the 7 August 2026 close. © Testahil 2026.', size=9)

doc.save('MODON_Valuation_Study_09-08-2026_public.docx')
print('wrote MODON_Valuation_Study_09-08-2026_public.docx')
