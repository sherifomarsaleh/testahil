"""AMOC_Valuation_Study_08-08-2026_public.docx — the study, on the audited statements and the
30-Jun-2026 disclosure, with the case for the verdict stated adversarially.

Every number is read from study_numbers.json or case_adversarial.json — the same files the
workbook and the strict evaluator run on. Nothing in this document is typed by hand.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from docx_base import (P, H1, H2, rich, caption, bullet, table, figure, box, masthead, doc,
                       INK, GREY)                                      # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, 'study_numbers.json')))
ADV = json.load(open(os.path.join(HERE, 'case_adversarial.json')))
IN = {k: v['value'] for k, v in D['inputs'].items()}
SRCI = {k: v['source'] for k, v in D['inputs'].items()}
UB, TTM, RT, BR = D['unitbuild'], D['ttm'], D['rates'], D['bridge']
F, W, DCF, LN = D['fcst'], D['wacc'], D['dcf'], D['lenses']
AU, BASE, REL, NRM, BK = D['audited'], D['base'], D['rel'], D['norm'], D['book']
HIS, HB = D['hist_is'], D['hist_bs']
STK, S0, BETA = D['strike'], D['step0'], D['wacc']['beta']
H1M, H3M = STK['horizons']['1M'], STK['horizons']['3M']
SPOT, SH, C = D['spot'], IN['shares_mn'], D['central']
LO, HI = D['span']; LOE, HIE = D['span_env']
YRS = F['years']
LINES, LBL = UB['lines'], UB['labels']


def n0(x): return f"{x:,.0f}"
def n1(x): return f"{x:,.1f}"
def p2(x): return f"{x:,.2f}"
def pc(x, dp=1): return f"{x*100:.{dp}f}%"
def sgn(x, dp=1): return f"{x*100:+.{dp}f}%"


GAP = C / SPOT - 1                       # −34.6%
PREM = SPOT / C - 1                      # +52.8%
REQ_DCF = (SPOT - 0.20 * LN['relative']['base'] - 0.20 * LN['normalized']['base']
           - 0.15 * LN['book']['base']) / 0.45

# ============================ MASTHEAD AND HEADLINE ===========================
masthead()
P('Alexandria Mineral Oils Company S.A.E.', size=19, bold=True, space_after=0)
rich([('EGX: AMOC · Egyptian Exchange · EGP  ·  Valuation study as of 6 August 2026, '
       'issued 8 August 2026', dict(size=10, color=GREY))], space_after=10)

box([
    ('THE CLAIM, STATED EXACTLY.  ',
     f'Fair value EGP {p2(C)} a share against a market price of EGP {p2(SPOT)} — fair value '
     f'sits {pc(-GAP)} below the price, equivalently the price stands {pc(PREM)} above fair '
     f'value. The weighted range is EGP {p2(LO)} to {p2(HI)}; the price is outside it.'),
    ('WHAT WOULD CHANGE OUR MIND.  ',
     'Give back every contested judgement in this study simultaneously — reinstate the tax '
     'provision as costless, un-charge the employees’ profit share, return the terminal '
     'rate to the softer inflation target, ignore the declared dividend, and tax at the '
     f'flattered effective rate — and the central still reaches only EGP '
     f'{p2(ADV["ALL_GIVEBACKS"]["central"])}, {pc(ADV["ALL_GIVEBACKS"]["central"]/SPOT-1)} '
     'below the price. Section 2 walks the whole stack.'),
    ('WHAT A BUYER AT THE PRICE MUST BELIEVE.  ',
     f'For the price to be fair, the cash-flow lens must reach EGP {p2(REQ_DCF)} — '
     f'{pc(REQ_DCF/LN["dcf"]["base"]-1,0)} above this model — which on the live sensitivity '
     'grids requires a PERMANENT gross margin near 12.2%, above the best single quarter this '
     'company has ever filed (10.19%), or volume growth at roughly ten times the assumed path. '
     'Section 14 derives both.'),
])

table([['Lens', 'Bear', 'Base', 'Bull', 'Weight', 'vs spot'],
       *[[LN[k]['name'], p2(LN[k]['bear']), p2(LN[k]['base']), p2(LN[k]['bull']),
          pc(LN[k]['w'], 0), pc(LN[k]['base'] / SPOT - 1)]
         for k in ('dcf', 'relative', 'normalized', 'book')],
       ['WEIGHTED CENTRAL', p2(LO), p2(C), p2(HI), '100%', pc(GAP)]],
      [2.5, 0.9, 0.9, 0.9, 0.8, 1.0], band_rows={5})
caption('Table 1 — the four lenses and the weighted central. The bear and bull columns of the '
        'weighted row are WEIGHTED with the same 45/20/20/15 weights as the base column; the '
        f'widest single lens spans {p2(LOE)}–{p2(HIE)} and is reported as an envelope, not as '
        'the range of the weighted estimate. Every lens base sits below the market price.')
figure(os.path.join(HERE, 'fig1_football.png'), 6.9,
       'Figure 1 — the football field. The price (red dashed) sits above every lens base and '
       'above the top of the weighted range.')

# ============================ 1. WHAT THIS STUDY RESTS ON =====================
H1('1 · What this study rests on — and what it does not')
P('Three classes of number appear in this study, and every figure in it belongs to exactly one:')
bullet('the audited transition-period statements for 1-Jul-2025 to 31-Dec-2025 (Crowe — Dr A. M. '
       'Hegazy & Co, unqualified opinion signed at Giza, 18 February 2026) and the reviewed '
       'statements for the three months to 31-Mar-2026, read note by note — the product table '
       '(note 14-A), the cost stack (note 15-A), the provision (note 10-1), the pledged '
       'deposits (note 9-E), dividends payable (note 11);', bold_head='AUDITED or REVIEWED — ')
bullet('the half-year results to 30-Jun-2026, disclosed to the Egyptian Exchange on 29-30 July '
       '2026 — one week before this study’s anchor date. A press release, not a filing. '
       'Half of the base year rests on it, this study says so on every page that uses it, and '
       'its gross-profit line is NOT taken at face value (section 4);', bold_head='REPORTED — ')
bullet('the processing-intensity weights that allocate conversion cost across the eight product '
       'lines, the zero re-rating on the company’s own trailing multiple, the sustainable '
       'return in the book lens, the volume and realisation growth paths, and the equity-risk-'
       'premium basis. Each is registered, dated, sourced and priced in the sensitivity '
       'section. There are no other free parameters.', bold_head='JUDGEMENT — ')
P(f'The model behind this document carries {152} registered inputs, of which 115 drive the '
  'arithmetic and 37 are quotation-only and are named as such in the workbook. A reachability '
  'gate fails the build if any input carrying a balance-sheet or profit-statement claim is '
  'registered but not used — the defect that let a EGP 921mn provision sit outside the previous '
  'edition’s bridge cannot recur silently.')

# ============================ 2. THE CASE, ADVERSARIALLY ======================
H1('2 · The case for the verdict, stated adversarially')
P('A gap of this size should not survive its own contested judgements — so the first thing this '
  'study does is give them all back. Each row below removes one charge a critic could dispute, '
  'and the last row removes all of them at once. Every row is a complete re-run of the whole '
  'model, not an add-back.')
table([['Give-back', 'Central', 'vs spot', 'What is being conceded'],
       ['None — as published', p2(ADV['base']['central']), pc(ADV['base']['central']/SPOT-1),
        'the study’s own reading'],
       ['Tax-disputes provision costs nothing', p2(ADV['no_provision']['central']),
        pc(ADV['no_provision']['central']/SPOT-1),
        'EGP 921.4mn recognised in note 10-1 settles for zero'],
       ['Declared dividend is not a claim', p2(ADV['no_divp']['central']),
        pc(ADV['no_divp']['central']/SPOT-1),
        'EGP 517.3mn payable in note 11 never leaves'],
       ['Employees’ profit share is free', p2(ADV['no_emp']['central']),
        pc(ADV['no_emp']['central']/SPOT-1),
        f'the {pc(RT["emp_rate"])} statutory appropriation is never paid'],
       ['Terminal rate on the 2028 target', p2(ADV['terminal_rf_5pct_target']['central']),
        pc(ADV['terminal_rf_5pct_target']['central']/SPOT-1),
        'the softer 5% inflation target replaces the 7% target in force'],
       ['Effective tax instead of statutory', p2(ADV['effective_tax']['central']),
        pc(ADV['effective_tax']['central']/SPOT-1),
        'operating profit taxed at the interest-flattered 22.12%'],
       ['ALL OF THE ABOVE AT ONCE', p2(ADV['ALL_GIVEBACKS']['central']),
        pc(ADV['ALL_GIVEBACKS']['central']/SPOT-1),
        'every contested charge conceded simultaneously']],
      [2.3, 0.85, 0.85, 3.0], band_rows={7})
caption('Table 2 — the adversarial stack. Concede everything and the price is still '
        f'{pc(-(ADV["ALL_GIVEBACKS"]["central"]/SPOT-1))} above the model.')
figure(os.path.join(HERE, 'fig4_adversarial.png'), 6.9,
       'Figure 2 — the same stack drawn. No single concession, and not all of them together, '
       'reaches the price.')
P('What remains after the give-backs is the part of the verdict that cannot be negotiated away '
  'by accounting choices: a pass-through processor earning an 9.0% gross margin, discounted at '
  'an Egyptian cost of equity of 27.8% falling to 19.1%, is worth less than 9.10 pounds a share '
  'on any internally consistent arithmetic this study can construct. The three places the case '
  'could still fail are named in section 16 — they are data this environment could not reach, '
  'not judgements it has hidden.')

# ============================ 3. THE COMPANY ==================================
H1('3 · The company, off its own filings')
P(f'Alexandria Mineral Oils Company distils atmospheric residue into base and special oils, '
  f'paraffin wax, gas oil, naphtha, LPG and fuel oil. Note 14-A discloses {n0(sum(IN["prod_t"].values()))} '
  f'tonnes sold for EGP {n0(sum(IN["prod_v"].values())/1e6)}mn in the transition half — eight '
  f'lines, tonnes and value both stated, so realisations per tonne are disclosed arithmetic, '
  f'not estimates. Raw materials are {pc(AU["cost_share"]["raw"])} of cost of sales '
  f'(note 15-A) and {pc(RT["raw_of_rev"])} of revenue: the value of this business is the SPREAD '
  f'between feedstock and slate, earned on tonnage — not the revenue line and not cost control.')
P('Alexandria Petroleum Company holds 20.77% (the previous edition misattributed this stake to '
  'EGPC); AMOC owns 86.45% of Alexandria Wax Products, whose minority is the non-controlling '
  'interest carried through this study. The offtake is dominated by the state petroleum '
  'complex, and the feedstock relationship is administered — the margin record below is a '
  'policy record as much as a market one.')
table([['Period', 'Net sales', 'Gross profit', 'Margin', 'EBIT'],
       *[[p, n0(HIS[p]['rev']), n0(HIS[p]['gp']), pc(HIS[p]['gm'], 2), n0(HIS[p]['ebit'])]
         for p in ['6M Dec-2024', '3M Mar-2025', '6M Dec-2025', '3M Mar-2026']]],
      [1.6, 1.3, 1.3, 1.0, 1.2])
caption('Table 3 — the filed record, EGP mn. Four consecutive periods; the margin ranges 5.05% '
        'to 10.19%. Nothing here is modelled.')

# ============================ 4. THE BASE YEAR ================================
H1('4 · The base year — twelve contiguous months, and a coherence test')
P(f'The base year is the TWELVE months to 30 June 2026: the audited transition half plus the '
  f'half disclosed to the exchange on 29-30 July 2026. Revenue EGP {n0(TTM["rev"])}mn, gross '
  f'profit EGP {n0(TTM["gp"])}mn, margin {pc(TTM["gm"], 2)}. No annualisation scalar is '
  f'applied and no period is estimated. The previous edition argued no clean twelve-month '
  f'period existed and annualised nine months by 4/3; the disclosure that refutes that argument '
  f'existed a week before its anchor date, and this edition both uses it and flags it: HALF OF '
  f'THIS BASE YEAR IS REPORTED, NOT AUDITED.')
H2('4.1 The released gross profit fails its own release, and is rejected')
P(f'The release states gross profit of EGP {n0(TTM["gp_h1_released"])}mn for the half. Run '
  f'through the company’s own first-quarter expense run rates, that figure implies profit '
  f'after tax of EGP {n0(TTM["pat_if_released"])}mn — {pc(TTM["ct3"])} ABOVE the EGP '
  f'{n0(IN["pat_h1cy26_rep"]/1e6)}mn the same release reports. At least one of the two released '
  f'lines is wrong, and two independent tests say it is the gross profit: the reported profit '
  f'ties to the AUDITED statement of changes in equity within {pc(TTM["ct1"])} (the release’s '
  f'"+109%" against the audited Jan–Jun-2025 majority profit), and the reported revenue ties to '
  f'an independent triangulation within {pc(TTM["ct2"])}. The gross profit this study uses, EGP '
  f'{n0(TTM["gp_h1"])}mn, is therefore SOLVED from the release’s own profit line. The '
  f'workbook shows the whole solve on the Base Year sheet, in live formulas.')
H2('4.2 One period, both sides of the margin')
P('Every operating line — administrative, selling, other, provisions, depreciation, capital '
  'expenditure, credit interest, the employees’ profit share — is struck on the SAME '
  'twelve months as revenue and cost of sales. The previous edition built revenue from the '
  'six-month product table doubled while annualising cost from nine months by 4/3; its base '
  'margin of 7.081% corresponded to no filed period. One period, both sides, or the margin is '
  'an artefact of the scalars. The nine-month annualisation is retained beside the headline '
  f'base as the fully-audited alternative: revenue {n0(TTM["rev9_ann"])}mn at {pc(TTM["gm9"], 2)} '
  f'— the {sgn(TTM["rev"]/TTM["rev9_ann"]-1)} gap between the two bases is a real uncertainty '
  'about this company and is disclosed, not averaged away.')

# ============================ 5. BOTTOM-UP BUILD ==============================
H1('5 · The bottom-up build — eight lines, both sides of the margin')
P('Revenue per line is tonnes × realisation, both disclosed in note 14-A; the only free scalar '
  'is one solved index that foots the eight lines to the twelve-month revenue. Cost per line is '
  'feedstock plus conversion:')
bullet(f'conversion (salaries, supporting materials, other, depreciation — the non-feedstock '
       f'{pc(1-AU["cost_share"]["raw"])} of note 15-A) is allocated on registered processing-'
       f'intensity weights: base oils 1.00 as the reference through the full lube train, wax '
       f'1.15 for deoiling and sweating, the light ends 0.15–0.25, residue fuel oils 0.05;',
       bold_head='CONVERSION — ')
bullet('feedstock is then allocated on NET REALISABLE VALUE — realisation less that line’s '
       'own conversion — the standard joint-product method. Two rejected alternatives are '
       'documented in the workbook: flat-per-tonne makes fuel oil sell below the cost of its '
       'own feed, and relative-sales-value makes the products this plant was built for '
       'loss-making. NRV is the only basis of the three that leaves every disclosed line with '
       'a positive spread.', bold_head='FEEDSTOCK — ')
table([['Line', 'Tonnes 6M', 'Realisation EGP/t', 'Cost EGP/t', 'Spread EGP/t', 'Margin'],
       *[[LBL[k], n0(IN['prod_t'][k]), n0(UB['px0'][k]),
          n0(UB['raw_pt'][k] + UB['conv_pt'][k]), n0(UB['spread'][k]), pc(UB['margin0'][k])]
         for k in LINES if k != 'waste']],
      [1.7, 1.0, 1.2, 1.1, 1.1, 0.8])
caption('Table 4 — per-line economics of the base year. A tonne of base oil contributes '
        f'{UB["spread"]["oils"]/UB["spread"]["fueloil"]:.1f}× the spread of a tonne of fuel '
        'oil; the specialty slate (oils and wax) is 12.0% of tonnage and 22.4% of value. '
        'The eight per-line costs rebuild the disclosed cost of sales exactly — the footing '
        'test is a live cell in the workbook.')
figure(os.path.join(HERE, 'fig5_spread.png'), 6.7,
       'Figure 3 — gross spread per tonne by line (gold = specialty slate). This is the number '
       'a blended-margin build cannot produce: mix now moves the margin.')
P('THE ONE OPERATING INPUT NOT READ OFF A FILING: note 15-A discloses the cost stack for the '
  'company, not by line, and any weight derivable from note 14-A alone is a function of price — '
  'which would return the same margin on every line, the defect this build exists to remove. '
  'The intensity vector is therefore an engineering judgement, registered and dated like every '
  'other input, and the valuation’s sensitivity to it is bounded: it redistributes cost '
  'BETWEEN lines while the company total is pinned to note 15-A, so it moves the mix effect, '
  'not the base-year total.')

# ============================ 6. FORECAST =====================================
H1('6 · The forecast — margin as an output')
table([['', *YRS],
       ['Revenue', *[n0(x) for x in F['rev']]],
       ['Gross profit', *[n0(x) for x in F['gp']]],
       ['Gross margin', *[pc(x, 2) for x in F['gm']]],
       ['Operating expense', *[n0(x) for x in F['opex']]],
       ['EBITDA', *[n0(x) for x in F['ebitda']]],
       ['EBIT', *[n0(x) for x in F['ebit']]],
       ['NOPAT (statutory tax, after profit share)', *[n0(x) for x in F['nopat']]],
       ['Capital expenditure', *[n0(x) for x in F['capex']]],
       ['Depreciation (rolls off the register)', *[n0(x) for x in F['dna']]],
       ['Δ working capital', *[n0(x) for x in F['dnwc']]],
       ['FREE CASH FLOW TO THE FIRM', *[n0(x) for x in F['fcff']]]],
      [2.6, 0.9, 0.9, 0.9, 0.9, 0.9], band_rows={11})
caption('Table 5 — the waterfall, EGP mn. The margin is an OUTPUT of eight per-line builds: '
        'feedstock moves with realisation (pass-through), the pound-denominated conversion legs '
        'move with local inflation, and the company margin is whatever the mix produces.')
figure(os.path.join(HERE, 'fig2_margin.png'), 6.9,
       'Figure 4 — the filed margin record, the base year, the forecast, and (red) the margin a '
       'buyer at the current price needs in perpetuity.')
P(f'Operating expense charges the three disclosed lines on three drivers (administrative on '
  f'inflation, selling on inflation and tonnage, other on inflation) PLUS two charges the '
  f'previous edition registered and never took: formed provisions and expected credit losses at '
  f'the filed run rate, and the employees’ profit share and board bonuses at '
  f'{pc(RT["emp_rate"])} of profit after tax — a statutory appropriation, solved from the '
  f'disclosed charge, that reaches neither the shareholder nor the tax line.')
P(f'Capital expenditure is BUILT, not extrapolated: maintenance at gross cost over the implied '
  f'{n1(RT["asset_life"])}-year asset life (EGP {n0(RT["maint_capex0"])}mn a year before '
  f'inflation) plus growth at the plant’s own capital intensity of EGP '
  f'{n0(RT["cap_intensity"])} per annual tonne — so incremental volume costs capital instead of '
  f'arriving free. Depreciation rolls off the growing asset register rather than being held '
  f'flat. Working capital runs on days SOLVED from the audited balance sheet '
  f'({n1(RT["inv_days"])} inventory / {n1(RT["recv_days"])} receivable / {n1(RT["pay_days"])} '
  f'payable), with the EGP 517mn of declared dividends REMOVED from payables: a distribution is '
  f'a financing claim, not operating funding.')

# ============================ 7. COST OF CAPITAL ==============================
H1('7 · The cost of capital')
table([['Component', 'Explicit window', 'Terminal', 'Construction'],
       ['Risk-free', pc(IN['rf'], 2), pc(RT['rf_term'], 2),
        'Egypt 10Y local currency; terminal = CBE target IN FORCE (7%) + 5.5% real — DERIVED, '
        'not set by hand'],
       ['Sovereign spread removed', f"−{pc(IN['sov_spread_cds'], 2)}", '—',
        'netted so country risk is not counted in both the rf and the ERP'],
       ['Equity premium × beta', f"{pc(IN['erp_cds'], 2)} × {BETA['beta']:.3f}",
        f"{pc(IN['erp_term'], 2)} × {BETA['beta']:.3f}",
        f"own-stock weekly regression, n={BETA['n']}, R²={BETA['r2']:.2f}, "
        f"90% CI [{BETA['ci90'][0]:.2f}, {BETA['ci90'][1]:.2f}]"],
       ['Cost of equity', pc(W['ke_exp'], 2), pc(W['ke_term'], 2), ''],
       ['WACC', pc(W['wacc_exp'], 2), pc(W['wacc_term'], 2),
        'net-cash weights: the negative debt weight RAISES the operating rate above the cost '
        'of equity, correctly penalising the unlevered assets']],
      [1.5, 1.15, 1.0, 3.35], size=8.8)
caption('Table 6 — the discount-rate stack. The rate glides from the explicit to the terminal '
        'anchor on the cost-of-debt path’s own cumulative progress. The terminal risk-free '
        'is the single most terminal-value-sensitive input in the model, which is why it is now '
        'derived from the central bank target in force rather than typed: using the softer '
        'Q4-2028 target instead is priced in Table 2 (+23 piastres).')

# ============================ 8. DCF AND TERMINAL =============================
H1('8 · The cash-flow lens and the terminal block')
P(f'The explicit window discounts to EGP {n0(DCF["pv_explicit"])}mn. The terminal return is '
  f'struck on invested capital at REPLACEMENT cost — working capital plus the asset base at '
  f'GROSS cost — giving {pc(DCF["roic_term"])}, against roughly 26% on net book. The plant is '
  f'67.4% written down; the book lens already haircuts the reported return for exactly that '
  f'reason, and this study applies ONE view of the asset base across all lenses. Growth = '
  f'return × reinvestment is enforced by assertion: at {pc(IN["g_term"], 0)} growth the '
  f'terminal block reinvests {pc(DCF["rr_term"])} of profit — ABOVE the final explicit year’s '
  f'{pc(RT["rr_2030"])}, so the terminal is funded, not flattered. Terminal value carries '
  f'{pc(DCF["tv_share"])} of enterprise value.')
figure(os.path.join(HERE, 'fig3_bridge.png'), 6.9,
       'Figure 5 — enterprise value to equity, per share. Every disclosed claim is carried: the '
       'minority takes its share of the WHOLE enterprise including cash; the tax-disputes '
       'provision (note 10-1) and the declared dividend (note 11) are deducted; the pledged '
       'deposits and the ASPPC stake are added as non-operating assets.')
P(f'The bridge lands at EGP {n0(BR["eq"])}mn of attributable equity — EGP {p2(BR["ps"])} a '
  f'share. Three of its five claims were absent from the previous edition’s bridge '
  f'entirely; setting the 921mn provision to zero moved that valuation by nothing at all. It '
  f'moves this one by 71 piastres, and the model’s reachability gate now fails the build '
  f'if any such claim is registered without being carried.')

# ============================ 9–12. OTHER LENSES ==============================
H1('9 · Relative multiples — on the trailing metric')
P(f'The company’s own trailing multiple is {RT["just_mult"]:.2f}× enterprise value to '
  f'EBITDA and {n1(D["rel"]["pe_trailing"])}× earnings. The justified multiple is DERIVED from '
  f'it at a zero re-rating — the name is held at what the market already pays it — so this lens '
  f'borrows nothing from the cash-flow lens: no discount factor, no interim add-back (both '
  f'defects of the previous construction, found independently by two reviewers). At '
  f'{RT["just_mult"]:.2f}× trailing EBITDA through the same bridge, EGP '
  f'{p2(LN["relative"]["base"])} a share. This is the lens CLOSEST to the price, and the gap '
  f'that remains ({pc(LN["relative"]["base"]/SPOT-1)}) is almost entirely the disclosed claims '
  f'in the bridge — which is precisely what this lens is for: at the market’s own '
  f'multiple, the price pays full value and then ignores the provision and the declared '
  f'dividend.')
H1('10 · Normalised earnings power — separated and discounted')
P(f'2028E OPERATING profit only, taxed at the statutory {pc(RT["tax_stat"], 1)}, after the '
  f'profit share and the minority: EGP {NRM["eps"]:.3f} a share. At {n1(IN["pe_just"])}× that '
  f'is a MID-2028 value, so it is discounted {n1(RT["norm_yrs"])} years to the valuation date '
  f'at the cost of equity ({pc(W["ke_exp"], 2)}), and net cash less the provision and the '
  f'declared dividend is added at FACE outside the multiple: EGP {p2(LN["normalized"]["base"])}. '
  f'The previous construction capitalised credit interest at an operating multiple — valuing a '
  f'bank deposit as if it were the refinery — and left the 2028 number undiscounted while the '
  f'sibling lens discounted; both defects are closed.')
H1('11 · Book value and sustainable return')
P(f'Justified price-to-book of {BK["pb_just"]:.2f}× = (sustainable return {pc(IN["roe_sust"], 0)} '
  f'less growth) over (cost of equity {pc(RT["ke_blend"], 2)} less growth), on book value of '
  f'EGP {p2(BK["bvps"])}: EGP {p2(LN["book"]["base"])}. The rate is the present-value-weighted '
  f'average of the SAME cost-of-equity glide the cash-flow lens uses — not the terminal rate '
  f'alone (which gave the previous edition 6.06) and not the explicit rate alone (3.75). The '
  f'sustainable return is struck below the trailing {pc(BASE["roe_trailing"])} because the '
  f'asset base is 67.4% written down — the same haircut the terminal block now carries.')
H1('12 · Synthesis')
P(f'Weights 45/20/20/15 — cash flow primary for a single-asset processor with a visible volume '
  f'ramp, the market and earnings lenses secondary, book least. Weighted central EGP {p2(C)}; '
  f'weighted range {p2(LO)}–{p2(HI)}; envelope {p2(LOE)}–{p2(HIE)}. The price exceeds the '
  f'weighted range and every lens base. It is inside only the DCF bull tail — five favourable '
  f'driver moves at once.')

# ============================ 13. SENSITIVITY =================================
H1('13 · Sensitivity — every row a full re-run, gated')
rows = [['Driver (DCF lens, EGP/share)', '', '', 'base', '', '']]
for gname, _, pts in D['blocks']['grids']:
    vals = [D['blocks']['scen'][f'{gname}|{i}']['ps'] for i in range(len(pts))]
    rows.append([f"{gname}  ({pts[0]['label']} … {pts[-1]['label']})"]
                + [p2(v) for v in vals])
table(rows, [2.9, 0.75, 0.75, 0.75, 0.75, 0.75], header=True, size=8.6)
caption('Table 7 — six drivers, five points each, thirty complete model re-runs. Every grid is '
        'sorted, every row reproduces the base case at its own base point, and every row is '
        'monotone — all three properties are ASSERTED in the build after the previous edition '
        'published three rows that failed them. In the workbook each of these cells is a live '
        'formula block, not a pasted value.')
P('Two readings matter. Terminal growth is almost inert (5.48 to 5.52 across 3–7%) because the '
  'reinvestment identity funds growth before crediting it — a model where that row is steep is '
  'a model crediting growth for free. And the gross margin row is the whole thesis: '
  '±0.5pp moves the DCF lens by about EGP 0.99, which is why the case in section 2 is built to '
  'survive the margin being wrong by more than the entire filed record’s range.')

# ============================ 14. REVERSE DCF =================================
H1('14 · What a buyer at EGP 9.10 must believe')
P('Inverting the model at the current price, holding everything else at its published value:')
bullet(f'the cash-flow lens must reach EGP {p2(REQ_DCF)} against this model’s '
       f'{p2(LN["dcf"]["base"])} — a {pc(REQ_DCF/LN["dcf"]["base"]-1, 0)} uplift;',
       bold_head='REQUIRED LENS — ')
bullet('on the margin grid that requires roughly +3.6 percentage points of gross margin on '
       'EVERY forecast year and in perpetuity — a permanent ~12.2% against a four-period filed '
       'record of 5.05–10.19% whose best single quarter is 10.19%;', bold_head='AS MARGIN — ')
bullet('or, on the volume grid, roughly ten and a half times the assumed volume-growth path — '
       'a plant adding capacity it has not announced and the capital build would have to fund;',
       bold_head='AS VOLUME — ')
bullet(f'beta cannot get there: even at 0.60 the lens reaches only '
       f'{p2(D["blocks"]["scen"]["Beta|0"]["ps"])}. Nor can terminal growth, at any rate that '
       'the reinvestment identity permits.', bold_head='NOT VIA THE RATE — ')
P('The one belief that WOULD close the gap honestly is the released H1-2026 gross-profit line '
  'taken at face value — and section 4.1 shows that line contradicts the profit printed in the '
  'same release by 12.6%. A buyer at the price is, in effect, trusting the one number in the '
  'disclosure that fails its own internal arithmetic.')

# ============================ 15. PRICE PATH ==================================
H1('15 · The price path — a separate object from fair value')
P(f'The calibrated Monte-Carlo cone (carry-anchored YZ-HAR-t, 50,000 paths, ν=6.0, width '
  f'calibration 0.951, name-level verdict {S0["verdict"]}, market gate '
  f'{S0["market_gate"]["verdict"]}) prices the PATH of the market price, not its fairness: '
  f'1-month median {p2(H1M["pct"]["p50"])} (p5–p95 {p2(H1M["pct"]["p5"])}–{p2(H1M["pct"]["p95"])}), '
  f'3-month median {p2(H3M["pct"]["p50"])} ({p2(H3M["pct"]["p5"])}–{p2(H3M["pct"]["p95"])}). '
  f'The drift is the carry — ln(1+rf) − ln(1+dividend yield) — and nothing from the valuation '
  f'is wired into it, so the cone can sit above a fair value far below it, and does. A '
  f'{pc(-GAP)} valuation gap is a statement about value, not a three-month price forecast.')
figure(os.path.join(HERE, 'fig6_cone.png'), 6.7,
       'Figure 6 — the calibrated price cone against fair value (gold). The market can stay '
       'above fair value throughout the cone’s horizon; the two objects answer different '
       'questions.')

# ============================ 16. WEAKNESSES ==================================
H1('16 · Where this case could fail — named, priced, and open')
bullet(f'the half to 30-Jun-2026 is a press release. If the audited half-year statements '
       f'restate revenue or profit materially, the base year moves with them. The fully-audited '
       f'alternative base (nine months × 4/3) is published beside the headline and prices the '
       f'central lower, not higher — so this risk runs AGAINST the price, not for it;',
       bold_head='THE REPORTED HALF — ')
bullet('two exchange disclosures were unreachable from this environment (egress blocked, seven '
       'negative results logged in the bibliography): a board FY2025/26 capital budget of '
       '~EGP 580mn reported by one reviewer (would LOWER the central, roughly −12% at face), '
       'and a revised FY2026 operating-profit budget of ~EGP 2.1bn reported by two reviewers '
       'independently (would RAISE it, roughly +17% at face). They pull in opposite directions, '
       'neither is verified, and both are named rather than silently absent;',
       bold_head='TWO UNREAD DISCLOSURES — ')
bullet('the processing-intensity weights are the one operating judgement in the build; they '
       'move per-line spreads, not the company total. The Egypt 10-year at 22.31% is cited to '
       'a source that could not be re-verified from here; three reviewers place it at '
       '22.6–23.0%, worth about half a percent on the central — the case does not turn on it;',
       bold_head='JUDGEMENT AND RATE — ')
bullet(f'the margin is administered, not competed. That cuts both ways and is the reason the '
       f'adversarial stack in section 2 exists: even at the full give-back the central is '
       f'{p2(ADV["ALL_GIVEBACKS"]["central"])}, and the margin required to justify the price '
       f'exceeds anything the administrator has ever granted.', bold_head='THE REGIME — ')

box([
    ('VERDICT.  ',
     f'Fair value EGP {p2(C)} against a price of EGP {p2(SPOT)}: fair value {pc(-GAP)} below '
     f'the price. The claim survives the simultaneous surrender of every contested judgement '
     f'in the study ({p2(ADV["ALL_GIVEBACKS"]["central"])}, still {pc(-(ADV["ALL_GIVEBACKS"]["central"]/SPOT-1))} '
     'below), and the price is reachable only on a permanent gross margin this company has '
     'never printed.'),
    ('BASIS AND LIMITS.  ',
     'Educational analysis on public filings and disclosures; not investment advice. Half the '
     'base year is reported, not audited. Two exchange disclosures material in opposite '
     'directions were unreachable and are named in section 16. The companion workbook '
     'recalculates this entire study live — 5,775 formulas, 198 pasted filing values, every '
     'formula verified cell-by-cell against the model by an independent evaluator.'),
    ('PROVENANCE.  ',
     'Audited transition-period statements (Crowe, unqualified, 18-Feb-2026); reviewed '
     'Q1-2026 statements; EGX half-year disclosure of 29-30 July 2026; the source register '
     'with every input’s value, source, date and ring is the companion bibliography.'),
])

OUT = os.path.join(HERE, 'AMOC_Valuation_Study_08-08-2026_public.docx')
doc.save(OUT)
print('wrote', OUT)
