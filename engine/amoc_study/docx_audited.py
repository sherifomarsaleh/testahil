"""AMOC_Valuation_Study_06-08-2026_public.docx — the study, on the AUDITED statements.

Replaces the edition written around a per-tonne cost construction that the filings deleted.
"""
import json, math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from docx_base import (P, H1, H2, rich, caption, bullet, table, figure, box, masthead, doc,
                       INK, GREY)

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, 'study_numbers.json')))
IN = {k: v['value'] for k, v in D['inputs'].items()}
AU, U, F, W, DCF = D['audited'], D['unit'], D['fcst'], D['wacc'], D['dcf']
BASE, LN, SN, EXP = D['base'], D['lenses'], D['sens'], D['experts']
REL, NRM, BK, TR = D['rel'], D['norm'], D['book'], D['terminal_recon']
STK, BT, S0, BETA = D['strike'], D['backtest'], D['step0'], D['wacc']['beta']
H3M, H1M = STK['horizons']['3M'], STK['horizons']['1M']
BT5, BTF, BTP = BT['five_year'], BT['full'], BT['production']
SPOT, SH = D['spot'], IN['shares_mn']
YRS = F['years']
LINES, LBL = U['lines'], U['labels']
M = 1e6


def n0(x): return f"{x:,.0f}"
def n1(x): return f"{x:,.1f}"
def n3(x): return f"{x:,.3f}"
def p2(x): return f"{x:,.2f}"
def pc(x, dp=1): return f"{x*100:.{dp}f}%"
def sgn(x, dp=1): return f"{x*100:+.{dp}f}%"


masthead()
H2('Independent Valuation Study — Educational Analysis')
H1('Alexandria Mineral Oils Company S.A.E. (EGX: AMOC)')
P(f"Downstream petroleum processor — base and special mineral oils, paraffin wax, gas oil, "
  f"naphtha, liquefied petroleum gas and fuel oil · Egyptian Exchange · reporting currency EGP · "
  f"analysis anchored on the closing price of {p2(SPOT)} on 2026-08-06.", size=9.5, color=GREY)

box([('READ FIRST — what this document is. ',
      'An educational valuation study. It contains no recommendation, no rating and no price '
      'target. What it contains is a fair-value range built from the audited financial '
      'statements, a stated cost of capital and explicitly listed assumptions — together with a '
      'separate, probabilistic map of where the share price could trade over the next one and '
      'three months. The two are different objects and are never blended.'),
     ('THIS EDITION IS BUILT ON THE AUDITED STATEMENTS. ',
      'The consolidated financial statements for the transition period 1 July 2025 to 31 December '
      '2025, audited by Crowe (Dr A. M. Hegazy & Co) with an UNQUALIFIED opinion signed at Giza '
      'on 18 February 2026; the limited-review statements for the six months to 31 December 2024; '
      'and the reviewed statements for the three months to 31 March 2026. Every company figure in '
      'this study is read off one of those three, with the note number where the filing gives '
      'one.'),
     ('What that replaced, and why it matters. ',
      'A previous edition of this study was built WITHOUT the filings, which could not be reached '
      'from the environment in which it was produced. It triangulated revenue across press '
      'reports, reconstructed the balance sheet from four disclosed lines and a set of days '
      'assumptions, and BUILT a cost stack from house estimates of yields, energy intensity and a '
      'solved feedstock differential. Twelve of its published assumptions were overturned by the '
      'filings. The fair-value estimate moved from EGP 9.38 to EGP ' + p2(D['central']) + '. '
      'Section 1.1 lists every one of the twelve.'),
     ('What a fair value is not. ',
      'A fair-value estimate is a statement about what the business appears to be worth on the '
      'assumptions set out here. It is not a forecast of the share price and carries no implied '
      'timeframe.')])

# =========================== HEADLINE ========================================
H2('Headline')
P(f"Alexandria Mineral Oils is the only refinery listed on the Egyptian Exchange. It takes "
  f"feedstock from the Egyptian General Petroleum Corporation and separates it into eight "
  f"disclosed product lines: base and special mineral oils and paraffin wax at the high-value "
  f"end, and gas oil, naphtha, liquefied petroleum gas, fuel oil and heavy fuel oil in volume. "
  f"In the audited six months to December 2025 it sold {n0(U['tot_t'])} tonnes for EGP "
  f"{n0(U['tot_v'])}mn.")
P(f"The economics are those of a thin-margin pass-through processor, and the audited cost note "
  f"says so in one line: RAW MATERIALS ARE {pc(U['cost_share']['raw'],1)} OF COST OF SALES and "
  f"{pc(AU['raw_of_rev'],1)} OF NET SALES. Salaries are {pc(U['cost_share']['salaries'],1)} of "
  f"cost of sales, energy and maintenance {pc(U['cost_share']['other'],1)}, chemicals "
  f"{pc(U['cost_share']['support'],1)} and depreciation {pc(U['cost_share']['dep'],1)}. That is "
  f"the whole of it. The value is not in the revenue line, which is largely feedstock passed "
  f"through at world product prices, and it is not in cost control either — it is in the spread "
  f"between what the feedstock costs and what the slate fetches, and in the tonnage that spread "
  f"is earned on.")
P(f"Two structural facts shape everything that follows. The first is the year-end change: the "
  f"company moved from a 30 June financial year to 31 December, with July to December 2025 filed "
  f"as an audited six-month transition period. There is therefore NO clean audited twelve-month "
  f"period, and the base year used here is the nine contiguous audited months from 1 July 2025 to "
  f"31 March 2026, annualised. The second is the balance sheet: cash of EGP "
  f"{n0(AU['cash'])}mn against loans of EGP {n1(AU['debt'])}mn, so the company is NET CASH by EGP "
  f"{n0(-DCF['nd'])}mn — EGP {p2(-DCF['nd']/SH)} a share, {pc(-DCF['nd']/(SPOT*SH),0)} of the "
  f"market capitalisation.")
P(f"The third fact is the one that does most to the valuation, and it is visible only in the cash "
  f"flow statement. CASH CAPITAL EXPENDITURE IS RUNNING BELOW THE DEPRECIATION CHARGE: EGP "
  f"{n0(IN['capex_h2_25']/M)}mn paid in the audited half against EGP {n0(IN['dep_h2_25']/M)}mn "
  f"charged, and EGP {n0(IN['capex_q1_26']/M)}mn against EGP {n0(IN['dep_q1_26']/M)}mn in the "
  f"reviewed quarter. Annualised, capital expenditure is {AU['capex_ann']/AU['dep_ann']:.2f} times "
  f"depreciation. The plant is being run, not renewed. That lifts free cash flow now and it makes "
  f"the terminal growth rate hard to defend, and section 1.9 refuses to smooth the conflict.")
P(f"On the primary construction the four lenses centre at EGP {p2(D['central'])} a share against "
  f"a market price of {p2(SPOT)} — {sgn(D['central']/SPOT-1,0)}. The lenses do not agree with "
  f"each other and that disagreement is the finding rather than a nuisance to be averaged away: "
  f"the cash-flow lens says EGP {p2(LN['dcf']['base'])}, normalised earnings power EGP "
  f"{p2(LN['normalized']['base'])}, relative multiples EGP {p2(LN['relative']['base'])} and book "
  f"value against a sustainable return EGP {p2(LN['book']['base'])}.", space_after=10)

# =========================== SUMMARY TABLE ===================================
H2('Valuation summary — every read at a glance')
rows = [['Read', 'Basis', 'Range (EGP)', 'Central', 'vs spot'],
        ['Free cash flow to the firm',
         f"Five-year forecast off the audited base year; cost of capital gliding "
         f"{pc(W['wacc_exp'])} → {pc(W['wacc_term'])}; terminal growth {pc(IN['g_term'],0)}. "
         f"TERMINAL VALUE = {pc(DCF['tv_share'],1)} OF ENTERPRISE VALUE",
         f"{p2(LN['dcf']['bear'])} – {p2(LN['dcf']['bull'])}", p2(LN['dcf']['base']),
         sgn(LN['dcf']['base']/SPOT-1, 0)],
        ['Relative multiples',
         f"{IN['ev_ebitda_just']}× enterprise value to {REL['year']} EBITDA, discounted back at "
         f"the model's own factor, with the interim free cash flow added back",
         f"{p2(LN['relative']['bear'])} – {p2(LN['relative']['bull'])}",
         p2(LN['relative']['base']), sgn(LN['relative']['base']/SPOT-1, 0)],
        ['Normalised earnings power',
         f"{IN['pe_just']}× on {NRM['year']} attributable earnings of EGP {p2(NRM['eps'])} a "
         f"share, struck on the AUDITED credit-interest line rather than a modelled interest path",
         f"{p2(LN['normalized']['bear'])} – {p2(LN['normalized']['bull'])}",
         p2(LN['normalized']['base']), sgn(LN['normalized']['base']/SPOT-1, 0)],
        ['Book value and sustainable return',
         f"Justified price-to-book {n1(BK['pb_just'])}× on AUDITED attributable book value of EGP "
         f"{p2(BK['bvps'])} a share, at a sustainable return of {pc(IN['roe_sust'],0)} and the "
         f"perpetual cost of equity {pc(W['ke_term'])}",
         f"{p2(LN['book']['bear'])} – {p2(LN['book']['bull'])}", p2(LN['book']['base']),
         sgn(LN['book']['base']/SPOT-1, 0)],
        ['WEIGHTED CENTRAL',
         f"Weights {pc(LN['dcf']['w'],0)} / {pc(LN['relative']['w'],0)} / "
         f"{pc(LN['normalized']['w'],0)} / {pc(LN['book']['w'],0)}",
         f"{p2(D['span'][0])} – {p2(D['span'][1])}", p2(D['central']),
         sgn(D['central']/SPOT-1, 0)],
        ['Market price', 'Closing price on 2026-08-06', '—', p2(SPOT), '—']]
table(rows, [1.42, 2.90, 1.06, 0.72, 0.68], size=8.3, band_rows={5}, left_cols={1})
caption(f"Terminal value is {pc(DCF['tv_share'],1)} of enterprise value, stated here and again in "
        f"the bridge in section 1.8. Bear and bull on the cash-flow lens are FIVE drivers moved "
        f"together and are not a confidence interval; the other three lenses take their ranges on "
        f"multiples and on the sustainable return, so the full span is an envelope of four "
        f"differently-constructed ranges and should not be read as a distribution.")

figure('fig1_football.png', 6.9,
       'Figure 1 — the four lenses and the weighted central, each shown bear to bull with the '
       'base marked. The vertical rule is the market price.')

# =========================== 1.1 WHAT THE FILINGS OVERTURNED =================
H1('1  Fundamental valuation')
H2('1.1  What the audited statements overturned')
P(f"This section exists because a previous edition of this study was published on triangulated "
  f"figures and is now known to have been wrong in twelve identifiable places. Listing them is "
  f"not penance; it is the only way a reader can judge how much weight to put on the parts that "
  f"did not change.")
rows = [['#', 'The published assumption', 'What the filing says'],
        ['1', 'Capital expenditure at 1.45%→1.25% of revenue, about EGP 604mn a year',
         f"Cash paid: EGP {n0(IN['capex_h2_25']/M)}mn in the audited half and EGP "
         f"{n0(IN['capex_q1_26']/M)}mn in the reviewed quarter — EGP {n0(AU['capex_ann'])}mn "
         f"annualised, about a fifth of the assumption"],
        ['2', 'Depreciation at 1.1% of revenue, about EGP 458mn a year',
         f"EGP {n0(AU['dep_ann'])}mn annualised, about a third"],
        ['3', 'A cost stack built from house yields, energy intensity and a solved feedstock '
              'differential; no salaries line inside cost of sales at all',
         f"Note 15-A: raw materials {pc(U['cost_share']['raw'],1)}, salaries "
         f"{pc(U['cost_share']['salaries'],1)}, other {pc(U['cost_share']['other'],1)}, "
         f"supporting materials {pc(U['cost_share']['support'],1)}, depreciation "
         f"{pc(U['cost_share']['dep'],1)}"],
        ['4', 'Chemicals charged at roughly five times the truth',
         f"Supporting materials are EGP {n0(IN['cos_support']/M)}mn in the half — "
         f"{pc(U['cost_share']['support'],2)} of cost of sales"],
        ['5', 'Three product lines from a table obtained via a reviewer',
         f"Note 14-A: EIGHT lines with tonnes AND value. Fuel oil (mix) alone is "
         f"{pc(U['mix_t']['fueloil'],0)} of tonnage, which the three-line build had merged with "
         f"gas oil, naphtha and LPG"],
        ['6', 'Operating expense at 1.25% of revenue',
         f"EGP {n0(AU['opex_ann'])}mn annualised — {pc(AU['opex_ann']/AU['base_rev'],2)} of "
         f"revenue, more than three times the assumption"],
        ['7', 'Property, plant and equipment reconstructed as a residual at EGP 2,403mn',
         f"Note 6: EGP {n0(IN['ppe_net']/M)}mn net, plus EGP {n0(IN['puc']/M)}mn of projects "
         f"under construction = EGP {n0(AU['ppe'])}mn"],
        ['8', 'Net working capital at 2.0% of revenue',
         f"EGP {n0(AU['nwc'])}mn — {pc(AU['nwc']/AU['base_rev'],1)} of the base year"],
        ['9', 'Minority interest inferred at 3.0% of group profit',
         f"Disclosed at {pc(AU['nci_share'],3)}. The subsidiary is Alexandria Wax Products, "
         f"86.45% owned"],
        ['10', 'The Egyptian General Petroleum Corporation described as a 20% shareholder',
         f"Note 18: Alexandria Petroleum Company holds {pc(IN['alexpet_stake'],2)}. EGPC is not a "
         f"shareholder at all — it is the counterparty, on both sides"],
        ['11', 'Historical other income read as devaluation FX gains and zeroed forward',
         'Note 14-B: mostly credit interest and provision reversals. The foreign-exchange gain '
         'line was ZERO in the transition half'],
        ['12', 'No tax-disputes provision carried',
         f"Note 10-1: EGP {n0(AU['provisions'])}mn — EGP {p2(AU['provisions']/SH)} a share"]]
table(rows, [0.35, 3.05, 3.55], size=8.0, left_cols={1, 2})
caption(f"Errors 1, 2 and 6 push in opposite directions and do not cancel: lower capital "
        f"expenditure and lower depreciation lift free cash flow, while an operating cost base "
        f"three times larger takes far more away. The net effect on the first forecast year's "
        f"operating profit is a fall of about 12%, and on the weighted central a fall from EGP "
        f"9.38 to EGP {p2(D['central'])}.")

# =========================== 1.2 THE BASE YEAR ===============================
H2('1.2  The base year is nine audited months, and here is why')
P(f"The company moved its year-end from 30 June to 31 December. July to December 2025 was filed "
  f"as an audited six-month transition period, and the three months to March 2026 have been "
  f"reviewed. The April-to-June 2025 quarter is not separately filed. There is therefore no clean "
  f"audited twelve-month period available, and constructing one would mean estimating the missing "
  f"quarter.")
P(f"This study does not estimate it. The base year is the NINE CONTIGUOUS AUDITED MONTHS from "
  f"1 July 2025 to 31 March 2026, annualised by four thirds. That scaling is the only step "
  f"between the filings and the base year, and no part of what it scales is estimated.")
rows = [['EGP mn', '6M to Dec-2025', '3M to Mar-2026', 'Nine months', 'Annualised'],
        ['Net sales', n0(IN['rev_h2_25']/M), n0(IN['rev_q1_26']/M), n0(AU['rev9']),
         n0(AU['base_rev'])],
        ['Cost of sales', f"({n0(IN['cogs_h2_25']/M)})", f"({n0(IN['cogs_q1_26']/M)})",
         f"({n0(AU['rev9']-AU['gp9'])})", f"({n0((AU['rev9']-AU['gp9'])*4/3)})"],
        ['GROSS PROFIT', n0((IN['rev_h2_25']-IN['cogs_h2_25'])/M),
         n0((IN['rev_q1_26']-IN['cogs_q1_26'])/M), n0(AU['gp9']), n0(AU['gp9']*4/3)],
        ['GROSS MARGIN', pc((IN['rev_h2_25']-IN['cogs_h2_25'])/IN['rev_h2_25'], 2),
         pc((IN['rev_q1_26']-IN['cogs_q1_26'])/IN['rev_q1_26'], 2), pc(AU['base_gm'], 3),
         pc(AU['base_gm'], 3)],
        ['Operating expense', f"({n0((IN['ga_h2_25']+IN['mkt_h2_25']+IN['othexp_h2_25'])/M)})",
         f"({n0((IN['ga_q1_26']+IN['mkt_q1_26']+IN['othexp_q1_26'])/M)})",
         f"({n0(AU['opex_ann']*3/4)})", f"({n0(AU['opex_ann'])})"],
        ['Depreciation and RoU amortisation', n0(IN['dep_h2_25']/M), n0(IN['dep_q1_26']/M),
         n0(AU['dep_ann']*3/4), n0(AU['dep_ann'])],
        ['CASH capital expenditure', n0(IN['capex_h2_25']/M), n0(IN['capex_q1_26']/M),
         n0(AU['capex_ann']*3/4), n0(AU['capex_ann'])],
        ['Net profit after tax', n0(IN['pat_h2_25']/M), n0(IN['pat_q1_26']/M), n0(AU['pat9']),
         n0(AU['pat9']*4/3)]]
table(rows, [2.15, 1.20, 1.20, 1.15, 1.20], size=8.3, band_rows={3, 4}, left_cols={0})
caption(f"Effective tax across the two filed periods is {pc(AU['tax_eff'],2)} — computed, not "
        f"assumed, and against a statutory {pc(IN['tax_stat'],1)}. Note the gross margin: "
        f"{pc((IN['rev_h2_25']-IN['cogs_h2_25'])/IN['rev_h2_25'],2)} in the audited half and "
        f"{pc((IN['rev_q1_26']-IN['cogs_q1_26'])/IN['rev_q1_26'],2)} in the reviewed quarter. The "
        f"March-2026 quarter is the strongest margin in the disclosed record by a wide margin and "
        f"it is a SINGLE quarter; the base year blends it with the half that precedes it rather "
        f"than annualising it alone.")

H2('1.3  The margin record, as filed')
rows = [[''] + AU['periods'],
        ['Net sales (EGP mn)'] + [n0(AU['rev'][k]) for k in AU['periods']],
        ['Gross profit (EGP mn)'] + [n0(AU['gp'][k]) for k in AU['periods']],
        ['GROSS MARGIN'] + [pc(AU['gm'][k], 2) for k in AU['periods']],
        ['Operating profit (EGP mn)'] + [n0(AU['ebit'][k]) for k in AU['periods']]]
table(rows, [2.05, 1.22, 1.22, 1.22, 1.22], size=8.4, band_rows={3})
caption(f"Four consecutively filed periods. This is not a modelled path: it is gross profit over "
        f"net sales as reported. The shape matters — {pc(AU['gm'][AU['periods'][0]],2)} in the "
        f"half to December 2024, a collapse to {pc(AU['gm'][AU['periods'][1]],2)} in the March-2025 "
        f"quarter, a recovery to {pc(AU['gm'][AU['periods'][2]],2)} in the half to December 2025, "
        f"and {pc(AU['gm'][AU['periods'][3]],2)} in the March-2026 quarter. A business whose "
        f"quarterly gross margin swings from 5% to 10% is not one whose margin can be forecast to "
        f"two decimal places, and this study does not pretend otherwise.")

# =========================== 1.4 REVENUE =====================================
H2('1.4  Revenue, from the audited product table')
P(f"Note 14-A gives eight product lines with tonnes AND value for the transition half. Every "
  f"realisation in this model is one disclosed number divided by another. Nothing is "
  f"reconstructed, no crude parity is invoked and no crack multiple is solved.")
rows = [['Product line', 'Tonnes', 'Value (EGP mn)', 'EGP / tonne', 'Share of tonnage',
         'Share of value']]
for k in LINES:
    rows.append([LBL[k], n0(IN['prod_t'][k]), n0(IN['prod_v'][k]/M), n0(U['px'][k]),
                 pc(U['mix_t'][k], 2), pc(U['mix_v'][k], 2)])
rows.append(['TOTAL', n0(U['tot_t']), n0(U['tot_v']), n0(U['tot_v']*M/U['tot_t']), '100.00%',
             '100.00%'])
table(rows, [1.85, 1.00, 1.10, 1.00, 1.05, 1.00], size=8.2, band_rows={9}, left_cols={0})
caption(f"The specialty slate — base and special oils plus paraffin wax — is "
        f"{pc(U['spec_share_t'],2)} of the tonnage and {pc(U['spec_share_v'],2)} of the value. "
        f"That gap is the whole investment case for the mix. Fuel oil (mix) is "
        f"{pc(U['mix_t']['fueloil'],1)} of tonnage at EGP {n0(U['px']['fueloil'])} a tonne against "
        f"EGP {n0(U['px']['oils'])} for oils and EGP {n0(U['px']['wax'])} for wax.")
P(f"Half-on-half value growth by line, against the December-2024 comparative in the same note: " +
  " · ".join(f"{LBL[k]} {sgn(U['growth_v'][k],1)}" for k in
             ('oils', 'wax', 'gasoil', 'naphtha', 'lpg', 'fueloil', 'hfo')) + ". Wax and fuel oil "
  f"led; gas oil and naphtha both FELL. The forecast volume ranking is taken from that measured "
  f"record rather than from a view, and the levels are struck well below those half-on-half rates "
  f"because a single half is not a trend.")

figure('fig7_mix.png', 6.9,
       'Figure 2 — revenue by audited product line, with the gross margin on the right axis: the '
       'base year as filed, then the forecast.')

# =========================== 1.5 COST ========================================
H2('1.5  Cost of sales, as filed — and what it says about the business')
P(f"Note 15-A splits cost of sales five ways. No part of it is built, estimated or solved.")
rows = [['Component', '6M to Dec-2025 (EGP mn)', '6M to Dec-2024 (EGP mn)',
         'Share of cost of sales', 'Share of net sales'],
        ['Raw materials', n0(IN['cos_raw']/M), n0(IN['cos_raw_24']/M),
         pc(U['cost_share']['raw'], 2), pc(IN['cos_raw']/IN['rev_h2_25'], 2)],
        ['Salaries', n0(IN['cos_salaries']/M), n0(IN['cos_salaries_24']/M),
         pc(U['cost_share']['salaries'], 2), pc(IN['cos_salaries']/IN['rev_h2_25'], 2)],
        ['Other — natural gas, electricity, water, spare parts, maintenance, EPROM contract',
         n0(IN['cos_other']/M), n0(IN['cos_other_24']/M), pc(U['cost_share']['other'], 2),
         pc(IN['cos_other']/IN['rev_h2_25'], 2)],
        ['Supporting materials (chemicals and additives)', n0(IN['cos_support']/M),
         n0(IN['cos_support_24']/M), pc(U['cost_share']['support'], 2),
         pc(IN['cos_support']/IN['rev_h2_25'], 2)],
        ['Depreciation', n0(IN['cos_dep']/M), n0(IN['cos_dep_24']/M),
         pc(U['cost_share']['dep'], 2), pc(IN['cos_dep']/IN['rev_h2_25'], 2)],
        ['COST OF SALES', n0(IN['cogs_h2_25']/M), n0(IN['cogs_h2_24']/M), '100.00%',
         pc(IN['cogs_h2_25']/IN['rev_h2_25'], 2)]]
table(rows, [2.45, 1.20, 1.20, 1.10, 1.05], size=8.1, band_rows={6}, left_cols={0})
caption(f"Raw materials are {pc(U['cost_share']['raw'],1)} of cost of sales and "
        f"{pc(AU['raw_of_rev'],1)} of net sales. Everything else together is "
        f"{pc(1-U['cost_share']['raw'],1)} of cost. This is a pass-through processor, and the "
        f"previous edition's attempt to build the stack from yields and energy intensity produced "
        f"a chemicals charge roughly five times the disclosed figure and carried NO salaries line "
        f"inside cost of sales at all — against an actual EGP {n0(IN['cos_salaries']/M)}mn in the "
        f"half.")
P(f"The forecast keeps that composition and moves each component the way its own economics "
  f"dictate: raw materials and supporting materials are PASS-THROUGH and move with volume and "
  f"realisation; salaries and the other line are POUND-DENOMINATED and inflate; depreciation is "
  f"the asset-register charge. The gross margin is what falls out. It is not a path and it is not "
  f"an input.")
rows = [[''] + [y.replace('E', '') for y in YRS],
        ['Revenue (EGP mn)'] + [n0(x) for x in F['rev']],
        ['Cost of sales (EGP mn)'] + [f"({n0(x)})" for x in U['cogs']],
        ['GROSS MARGIN — an output'] + [pc(x, 2) for x in F['gm']],
        ['Operating expense (EGP mn)'] + [f"({n0(x)})" for x in F['opex']],
        ['EBITDA (EGP mn)'] + [n0(x) for x in F['ebitda']],
        ['EBIT (EGP mn)'] + [n0(x) for x in F['ebit']]]
table(rows, [2.20, 0.94, 0.94, 0.94, 0.94, 0.94], size=8.3, band_rows={3})
caption(f"The margin drifts from {pc(F['gm'][0],2)} to {pc(F['gm'][4],2)} — narrowing slightly, "
        f"because the pound-denominated cost legs inflate faster than the realisation is assumed "
        f"to grow. That is a mechanical consequence of the disclosed composition, not a view. A "
        f"reader who thinks the company recovers currency in price faster should raise the "
        f"realisation growth path and watch the margin widen.")

# =========================== 1.6 COST OF CAPITAL =============================
H2('1.6  The cost of capital, built rather than asserted')
rows = [['Component', 'Explicit window', 'Terminal', 'Note'],
        ['Risk-free rate', pc(IN['rf']), pc(IN['rf_term']),
         "10-year local-currency government bond today; the terminal rate is norm-built from the "
         "central bank's published medium-term inflation target plus an emerging-market real-rate "
         "convention"],
        ['less sovereign default spread', f"({pc(IN['sov_spread_cds'])})", '—',
         'netted out so Egypt’s default risk is not charged twice — once inside the pound yield '
         'and again in the country premium'],
        ['Beta', n3(IN['beta']), n3(IN['beta']),
         f"own-stock regression, R-squared {pc(BETA['r2'])}, n = {BETA['n']}"],
        ['Equity risk premium', pc(IN['erp_cds']), pc(IN['erp_term']),
         'total premium on the credit-default-swap basis'],
        ['COST OF EQUITY', pc(W['ke_exp']), pc(W['ke_term']), ''],
        ['Cost of net debt, after tax', pc(W['k_nd_at']), pc(W['kd_term_at']),
         f"blend of what the EGP {n1(AU['debt'])}mn of borrowing costs and what the EGP "
         f"{n0(AU['cash'])}mn cash pile EARNS, taxed at the AUDITED effective rate "
         f"{pc(AU['tax_eff'],2)}"],
        ['Debt weight', pc(W['wd_exp']), pc(IN['wd_term'], 0),
         'NEGATIVE today, because the company is net cash'],
        ['WEIGHTED COST OF CAPITAL', pc(W['wacc_exp']), pc(W['wacc_term']), '']]
table(rows, [1.62, 0.95, 0.82, 3.36], size=8.2, band_rows={5, 8}, left_cols={3})
P(f"The weighting runs the opposite way to the intuition most readers bring. Net debt is "
  f"negative, so the debt weight is {pc(W['wd_exp'])} and the equity weight {pc(W['we_exp'])}, "
  f"and the result — {pc(W['wacc_exp'])} — sits ABOVE the {pc(W['ke_exp'])} cost of equity rather "
  f"than below it. That is the point of the construction: a company holding "
  f"{pc(-DCF['nd']/(SPOT*SH),0)} of its market capitalisation in near-riskless cash has an "
  f"observed equity cost that UNDERSTATES the risk of its operating assets, and unlevering for "
  f"the cash is what recovers the operating rate.")
P(f"One figure in that table changed when the filings arrived and it is worth naming: the tax "
  f"rate inside the cost of net debt. The previous edition used an assumed {pc(0.235,1)}; the two "
  f"filed periods give {pc(AU['tax_eff'],2)}. Building the workbook is what caught it, because "
  f"the workbook computes the rate from the filings and the model was still carrying the "
  f"assumption.", size=10)

H2('1.7  The discount-rate schedule, year by year')
rows = [[''] + [y.replace('E', '') for y in YRS],
        ['Cost of debt path'] + [pc(x) for x in IN['kd_path']],
        ['Cumulative progress along that path'] + [f"{x:.3f}" for x in F['glide_frac']],
        ['Forward cost of capital'] + [pc(x) for x in F['fwd_wacc']],
        ['Cumulative discount factor'] + [f"{x:.4f}" for x in F['df']]]
table(rows, [2.35, 0.92, 0.92, 0.92, 0.92, 0.92], size=8.4, band_rows={3, 4})
caption('The glide fractions are the cost-of-debt path’s own cumulative progress, so the shape is '
        'inherited from one assumed easing calendar rather than being a second free parameter. '
        f"The terminal value is brought home on the year-five factor of {F['df'][4]:.4f}, the same "
        'factor that discounts year-five cash flow. One date, one price of time.')

# =========================== 1.8 WATERFALL AND BRIDGE ========================
H2('1.8  The free-cash-flow waterfall and the enterprise-value bridge')
rows = [['EGP mn'] + [y.replace('E', '') for y in YRS],
        ['EBIT'] + [n0(x) for x in F['ebit']],
        [f"NOPAT = EBIT × (1 − {pc(AU['tax_eff'],2)})"] + [n0(x) for x in F['nopat']],
        ['add back depreciation and amortisation'] + [n0(x) for x in F['dna']],
        ['less capital expenditure (ACTUAL run rate, inflated)'] + [f"({n0(x)})" for x in F['capex']],
        ['less change in net working capital'] + [f"({n0(x)})" if x >= 0 else n0(-x)
                                                  for x in F['dnwc']],
        ['FREE CASH FLOW TO THE FIRM'] + [n0(x) for x in F['fcff']],
        ['Discount factor'] + [f"{x:.4f}" for x in F['df']],
        ['PRESENT VALUE'] + [n0(x) for x in F['pv']]]
table(rows, [2.35, 0.92, 0.92, 0.92, 0.92, 0.92], size=8.3, band_rows={6, 8}, left_cols={0})
caption(f"Capital expenditure is held at the ACTUAL cash run rate from the two filings, inflated "
        f"— EGP {n0(F['capex'][0])}mn in the first forecast year against a depreciation charge of "
        f"EGP {n0(F['dna'][0])}mn. The previous edition modelled EGP 604mn. A reader who believes "
        f"the plant must eventually be renewed should raise this line; it is the sharpest single "
        f"criticism available of this valuation and section 1.9 and section 7 both say so.")

figure('fig8_waterfall.png', 6.6,
       'Figure 3 — the waterfall for the first forecast year, drawn to scale.')

rows = [['Enterprise value to equity', 'EGP mn', 'EGP / share'],
        ['Present value of the explicit five years', n0(DCF['pv_explicit']),
         p2(DCF['pv_explicit']/SH)],
        ['Present value of the terminal block', n0(DCF['pv_tv']), p2(DCF['pv_tv']/SH)],
        ['TERMINAL VALUE AS A PERCENTAGE OF ENTERPRISE VALUE', pc(DCF['tv_share'], 1), ''],
        ['ENTERPRISE VALUE (the operating assets)', n0(DCF['ev']), p2(DCF['ev']/SH)],
        [f"less minority interests at {pc(DCF['nci_share'],3)}, ON THE ENTERPRISE VALUE",
         f"({n0(DCF['nci_val'])})", f"({p2(DCF['nci_val']/SH)})"],
        ['= operating assets attributable to shareholders', n0(DCF['ev']-DCF['nci_val']),
         p2((DCF['ev']-DCF['nci_val'])/SH)],
        ['less net debt (negative — net cash is ADDED in full)', n0(DCF['nd']), p2(DCF['nd']/SH)],
        ['EQUITY ATTRIBUTABLE TO SHAREHOLDERS', n0(DCF['eq_attr']), p2(DCF['ps'])],
        ['Market price', '', p2(SPOT)]]
table(rows, [3.85, 1.45, 1.30], size=8.5, band_rows={3, 4, 8})
caption(f"The minority comes off the OPERATING enterprise value BEFORE the cash is added, because "
        f"deducting a percentage of a total that already includes the cash would hand the "
        f"minority a slice of the parent's balance. The rate is the DISCLOSED "
        f"{pc(DCF['nci_share'],3)}, not the 3.0% the previous edition inferred. Two disclosed "
        f"balances sit outside this bridge and are named rather than buried: EGP "
        f"{n0(AU['pledged'])}mn of deposits PLEDGED against credit facilities, which are not free "
        f"cash and are excluded from net debt, and the EGP {n0(AU['provisions'])}mn tax-disputes "
        f"and claims provision — EGP {p2(AU['provisions']/SH)} a share — which a reader who "
        f"thinks the exposure is incremental should subtract.")

# =========================== 1.9 TERMINAL ====================================
H2('1.9  The terminal block, and the check that now binds')
P(f"Growth in perpetuity has to be paid for with capital. The reinvestment rate is forced to "
  f"satisfy growth = return × reinvestment: at a terminal return of {pc(DCF['roic_term'])}, "
  f"funding {pc(IN['g_term'],0)} of growth requires reinvesting {pc(DCF['rr_term'])} of profit. "
  f"Terminal value is EGP {n0(DCF['tv'])}mn, {pc(DCF['tv_share'],1)} of enterprise value.")
P(f"THAT IS NOT THE HONEST READING OF THIS COMPANY'S RECORD, AND THE STUDY WILL NOT SMOOTH IT.")
rows = [[''] + AU['periods'],
        ['Annualised return on invested capital'] + [pc(TR['roic'][k]) for k in AU['periods']],
        ['Reinvestment rate (capex less depreciation, over NOPAT)'] +
        [sgn(TR['rr'][k]) for k in AU['periods']],
        ['Implied steady-state growth'] + [sgn(TR['implied_g'][k]) for k in AU['periods']]]
table(rows, [2.55, 1.10, 1.10, 1.10, 1.10], size=8.3, band_rows={3})
caption(f"Reinvestment is NEGATIVE in every audited period, because cash capital expenditure runs "
        f"below the depreciation charge. Growth = return × reinvestment therefore implies a "
        f"steady-state rate of about {pc(TR['stable_g'],1)} — the company is shrinking its capital "
        f"base, not compounding it.")
P(f"So the adopted terminal rate of {pc(IN['g_term'],0)} is NOT supported by the reinvestment "
  f"identity. Two readings are defensible and both are published rather than one being chosen "
  f"quietly. Either the under-investment is temporary and capital expenditure must rise toward "
  f"depreciation — in which case free cash flow in the explicit window is overstated by roughly "
  f"EGP {n0(F['dna'][0]-F['capex'][0])}mn a year and the value falls — or it is durable, in which "
  f"case the terminal growth rate should be at or below zero and the terminal block, "
  f"{pc(DCF['tv_share'],1)} of enterprise value, is too large. The sensitivity grid runs terminal "
  f"growth down to 3% and a reader can go lower; section 7 carries this as the study's sharpest "
  f"unresolved weakness.")

# =========================== 1.10 SENSITIVITIES ==============================
H2('1.10  Sensitivities')
figure('fig2_sens.png', 6.3,
       'Figure 4 — fair value across the terminal cost of capital and the terminal growth rate.')
rows = [['Driver', 'Range tested', 'Fair value across the range (EGP)'],
        ['Terminal cost of capital', f"{pc(SN['wt_grid'][0])} – {pc(SN['wt_grid'][4])}",
         ' · '.join(p2(SN['grid_wacc_g'][i][2]) for i in range(5))],
        ['Terminal growth', f"{pc(SN['g_grid'][0],0)} – {pc(SN['g_grid'][4],0)}",
         ' · '.join(p2(SN['grid_wacc_g'][2][j]) for j in range(5))],
        ['Explicit-window cost of capital', f"{pc(SN['we_grid'][0])} – {pc(SN['we_grid'][4])}",
         ' · '.join(p2(SN['grid_exp_term'][i][2]) for i in range(5))],
        ['Beta', f"{SN['beta_grid'][0]:.2f} – {SN['beta_grid'][4]:.2f}",
         ' · '.join(p2(x) for x in SN['grid_beta'])],
        ['Gross margin shift', f"{sgn(SN['gm_grid'][0],1)} – {sgn(SN['gm_grid'][4],1)}",
         ' · '.join(p2(x) for x in SN['grid_margin'])],
        ['Volume growth', 'zero to double the assumed path',
         ' · '.join(p2(x) for x in SN['grid_vol'])],
        ['Realised price growth', '−10% to +10% on the assumed path',
         ' · '.join(p2(x) for x in SN['grid_fx'])],
        ['Net working capital', f"{pc(SN['nwc_grid'][0],0)} – {pc(SN['nwc_grid'][4],0)} of revenue",
         ' · '.join(p2(x) for x in SN['grid_nwc'])]]
table(rows, [1.85, 2.05, 3.05], size=8.2, left_cols={1, 2})
caption(f"The gross-margin row is the one to read first. A half-point either way on a business "
        f"whose gross margin is {pc(AU['base_gm'],2)} moves the answer by roughly EGP "
        f"{p2(abs(SN['grid_margin'][3]-SN['grid_margin'][2]))} a share — and the filed record "
        f"swings between {pc(AU['gm'][AU['periods'][1]],2)} and {pc(AU['gm'][AU['periods'][3]],2)} "
        f"from one quarter to the next. That is the honest measure of how much precision this "
        f"valuation admits.")

H2('1.11  The three cross-check lenses')
P(f"Relative multiples. {IN['ev_ebitda_just']}× on {REL['year']} EBITDA of EGP "
  f"{n0(REL['ebitda_mid'])}mn gives an enterprise value AS AT that year end; discounted back at "
  f"the model's own factor of {REL['df_rel']:.4f} and with the interim free cash flow of EGP "
  f"{n0(REL['pv_interim'])}mn added back rather than dropped, that is EGP "
  f"{p2(LN['relative']['base'])} a share.")
P(f"Normalised earnings power. Every component is taken from {NRM['year']}: EBIT of EGP "
  f"{n0(NRM['ebit'])}mn plus the AUDITED credit-interest line annualised at EGP "
  f"{n0(NRM['interest'])}mn, taxed at {pc(AU['tax_eff'],2)} and after minorities, gives EGP "
  f"{p2(NRM['eps'])} a share. At {IN['pe_just']}× that is EGP {p2(LN['normalized']['base'])}. The "
  f"interest line is disclosed in note 14-B and in both cash-flow statements; the previous "
  f"edition used a modelled interest path off a projected cash balance instead.")
P(f"Book value and sustainable return. The justified price-to-book identity gives "
  f"{n1(BK['pb_just'])}× = (sustainable return {pc(IN['roe_sust'],0)} less growth "
  f"{pc(IN['g_term'],0)}) ÷ (perpetual cost of equity {pc(W['ke_term'])} less growth), applied to "
  f"AUDITED attributable book value of EGP {p2(BK['bvps'])} a share, for EGP "
  f"{p2(LN['book']['base'])}. The book value is the filed parent equity divided by shares — not a "
  f"reconstruction.")

# =========================== 2 PRICE RECORD ==================================
H1('2  The price record')
figure('fig3_ma.png', 6.9,
       'Figure 5 — the closing price against its 20, 50, 100 and 200-session moving averages.')
P(f"The series runs from {S0['series_first']} to {S0['series_last']} and covers "
  f"{n0(S0['clean_rows'])} clean sessions out of {n0(S0['raw_rows'])} raw rows, over "
  f"{n1(S0['span_years'])} years at {n1(S0['density_rows_per_yr'])} sessions a year, which "
  f"matches the exchange's Sunday-to-Thursday calendar. One row carrying a non-positive price was "
  f"removed; {pc(S0['flat_frac'])} of sessions are flat. The largest single-session move in the "
  f"whole history is {S0['max_abs_log']:.4f} in log terms, just INSIDE the exchange's ±20% daily "
  f"price limit of {math.log(1.20):.4f}, so there is no unadjusted corporate action hiding in the "
  f"series.")

# =========================== 3 MONTE CARLO ===================================
H1('3  Where the price could trade')
P(f"This section is a different object from the valuation above and is never blended with it. It "
  f"is a probability map of the share price over one and three months, produced by simulating "
  f"50,000 paths from the cleaned price history with a volatility model fitted on the whole "
  f"Egyptian market rather than on this name alone.")
figure('fig4_fan.png', 6.9,
       'Figure 6 — the forward price cone to three months. The dashed rule is the fundamental '
       'central estimate; the dotted rule is the market price.')
rows = [['', 'One month', 'Three months'],
        ['Calendar horizon date', H1M['target_date'], H3M['target_date']],
        ['Check date actually used', H1M['grade_date'], H3M['grade_date']],
        ['Sessions simulated', n0(H1M['h']), n0(H3M['h'])],
        ['5th percentile', p2(H1M['pct']['p5']), p2(H3M['pct']['p5'])],
        ['25th percentile', p2(H1M['pct']['p25']), p2(H3M['pct']['p25'])],
        ['Median', p2(H1M['pct']['p50']), p2(H3M['pct']['p50'])],
        ['75th percentile', p2(H1M['pct']['p75']), p2(H3M['pct']['p75'])],
        ['95th percentile', p2(H1M['pct']['p95']), p2(H3M['pct']['p95'])],
        ['Probability above today’s price', pc(H1M['p_above']), pc(H3M['p_above'])],
        ['Probability 10% or more up', pc(H1M['p_up10']), pc(H3M['p_up10'])],
        ['Probability 10% or more down', pc(H1M['p_dn10']), pc(H3M['p_dn10'])],
        ['Annualised volatility at the anchor', pc(H1M['anchor_vol_ann']),
         pc(H3M['anchor_vol_ann'])]]
table(rows, [3.20, 1.70, 1.70], size=8.5)
caption(f"The Egyptian Exchange trades Sunday to Thursday, so the three-month calendar target "
        f"{H3M['target_date']} falls on a non-trading day and the cone is graded on the first "
        f"session at or after it, {H3M['grade_date']}.")
P(f"The drift is not a view. Over three months the simulated log drift is "
  f"{H3M['drift_log_h']:+.4f} — the CARRY and nothing else: the local risk-free rate of "
  f"{pc(STK['rf_live'])} less the dividend yield of {pc(STK['q_annual'])}, less the half-variance "
  f"term. NO PART OF THE DRIFT COMES FROM THE VALUATION.", size=10)
P(f"THE NAME-LEVEL CALIBRATION VERDICT IS PARITY, NOT SKILL, and that is stated before the "
  f"favourable numbers rather than after them. On the production window set — the "
  f"{BTP['windows']} post-break origins the standing gate scores — the margin over a "
  f"carry-anchored random walk is {sgn(BTP['skill_norm'],2)} and the confidence interval straddles "
  f"zero at every bootstrap block size. What carries the cone into this study is the MARKET-level "
  f"gate: the {BT['fit']['panel_names']}-name Egyptian panel scores "
  f"{sgn(BT['fit']['market_skill'],2)} with a confidence interval of "
  f"[{BT['fit']['market_ci90'][0]:.3f}, {BT['fit']['market_ci90'][1]:.3f}], which is a PASS. A "
  f"reader looking for a name-level demonstration of forecasting edge will not find one here.")

# =========================== 4 SIDE BY SIDE ==================================
import numpy as _np
_p3 = _np.load(os.path.join(HERE, 'paths_3M.npy'))[:, -1]
P3 = float((_p3 > D['central']).mean())
H1('4  The two answers side by side')
rows = [['', 'What it says', 'Value'],
        ['Fundamental central', 'What the business appears to be worth on the audited figures',
         p2(D['central'])],
        ['Market price', 'What it costs today', p2(SPOT)],
        ['Gap', 'Fundamental against market', sgn(D['central']/SPOT-1)],
        ['Three-month median of the price map',
         'The centre of the simulated distribution, which knows nothing about the valuation',
         p2(H3M['pct']['p50'])],
        ['Probability the price is above the fundamental central in three months',
         'Read directly off the simulated distribution', pc(P3)]]
table(rows, [2.35, 3.35, 1.20], size=8.5, left_cols={1})

# =========================== 5 CATALYSTS =====================================
H1('5  What would move the answer')
bullet(f"The filed record swings from {pc(AU['gm'][AU['periods'][1]],2)} in the March-2025 quarter "
       f"to {pc(AU['gm'][AU['periods'][3]],2)} in the March-2026 quarter. A half-point across the "
       f"whole path is worth about EGP {p2(abs(SN['grid_margin'][3]-SN['grid_margin'][2]))} a "
       f"share. Nothing else in this study moves the answer as much per unit of uncertainty.",
       bold_head='The gross margin, which is genuinely volatile. ')
bullet(f"Cash capital expenditure is {AU['capex_ann']/AU['dep_ann']:.2f} times depreciation. If "
       f"that is a deferral rather than a permanent feature, free cash flow in the explicit "
       f"window is overstated by roughly EGP {n0(F['dna'][0]-F['capex'][0])}mn a year and the "
       f"terminal block is built on a return that will not persist.",
       bold_head='Whether the under-investment reverses. ')
bullet(f"Two points off the terminal cost of capital is worth about EGP "
       f"{p2(abs(SN['grid_wacc_g'][0][2]-SN['grid_wacc_g'][2][2]))} a share. The terminal rate is "
       f"built from the central bank's own published target; if disinflation stalls, that "
       f"assumption breaks first.", bold_head='The pace of Egyptian disinflation. ')
bullet(f"The Egyptian General Petroleum Corporation bought EGP {n0(IN['egpc_sales']/M)}mn of "
       f"product in the audited half — {pc(IN['egpc_sales']/IN['rev_h2_25'],1)} of net sales — and "
       f"supplied EGP 16.3bn of feedstock in the same period. It sits on both sides of the trade. "
       f"It is NOT a shareholder; Alexandria Petroleum Company holds "
       f"{pc(IN['alexpet_stake'],2)}. A change in either administered price moves the margin with "
       f"no change in the external environment.",
       bold_head='The counterparty, which is the state on both sides. ')
bullet(f"A tax-disputes provision of EGP {n0(AU['provisions'])}mn — EGP "
       f"{p2(AU['provisions']/SH)} a share — sits on the balance sheet, and EGP "
       f"{n0(AU['pledged'])}mn of deposits is pledged against credit facilities and is not free "
       f"cash. Neither is inside the bridge.", bold_head='Two disclosed balances outside the bridge. ')

# =========================== 6 ZONES =========================================
H1('6  Probability zones')
_C = D['central']
zones = [(f"Below EGP 7.50", float((_p3 < 7.5).mean())),
         (f"EGP 7.50 – {p2(_C)} (below the central estimate)",
          float(((_p3 >= 7.5) & (_p3 < _C)).mean())),
         (f"EGP {p2(_C)} – {p2(SPOT)} (central to today)",
          float(((_p3 >= _C) & (_p3 < SPOT)).mean())),
         (f"EGP {p2(SPOT)} – 11.00 (above today)",
          float(((_p3 >= SPOT) & (_p3 < 11.0)).mean())),
         ('Above EGP 11.00', float((_p3 >= 11.0).mean()))]
table([['Zone at three months', 'Probability']] + [[z, pc(p)] for z, p in zones],
      [4.20, 1.50], size=8.6)
caption('Cut at the market price and at the fundamental central estimate, so the reader can see '
        'how much of the simulated distribution sits on each side of each.')

# =========================== 7 CAVEATS =======================================
H1('7  Caveats — what is weak in this study')
bullet(f"Cash capital expenditure runs at {AU['capex_ann']/AU['dep_ann']:.2f} times depreciation "
       f"across both filed periods. The model carries that forward, which lifts free cash flow. "
       f"But growth = return × reinvestment then implies a NEGATIVE steady-state growth rate, "
       f"while the terminal block adopts {pc(IN['g_term'],0)} and carries "
       f"{pc(DCF['tv_share'],1)} of enterprise value. Those two statements cannot both be right. "
       f"This is the sharpest unresolved weakness in the study and it is not answered here — it "
       f"is disclosed, priced in the sensitivity grid, and left to the reader.",
       bold_head='THE TERMINAL RATE AND THE REINVESTMENT RECORD CONTRADICT EACH OTHER. ')
bullet(f"There is no clean audited twelve-month period. The base year is nine contiguous audited "
       f"months annualised by four thirds. If the missing April-to-June 2025 quarter was unusual "
       f"in either direction, the base year is off by that amount and everything scales with it.",
       bold_head='The base year is annualised, not filed. ')
bullet(f"The filed gross margin swings from {pc(AU['gm'][AU['periods'][1]],2)} to "
       f"{pc(AU['gm'][AU['periods'][3]],2)} between adjacent quarters. The forecast holds it near "
       f"{pc(F['gm'][0],2)}. A single quarter is not a trend in either direction, and a reader "
       f"who weights the March-2026 print more heavily would get a materially higher answer.",
       bold_head='The margin is genuinely volatile and the forecast smooths it. ')
bullet(f"{pc(DCF['tv_share'],1)} of enterprise value sits beyond year five. Both terminal anchors "
       f"are house views, disclosed as such, and neither is reverse-engineered from a price.",
       bold_head='The terminal value carries most of the weight. ')
bullet(f"The company neither buys its feedstock nor sells most of its output in an arm's-length "
       f"market: EGPC took {pc(IN['egpc_sales']/IN['rev_h2_25'],1)} of net sales in the audited "
       f"half and supplied the feedstock. A margin forecast for a business like that is a "
       f"forecast about an administered relationship.",
       bold_head='The counterparty is the state, on both sides. ')
bullet(f"The EGP {n0(AU['provisions'])}mn tax-disputes provision is recognised on the balance "
       f"sheet but is not deducted from equity value in the bridge, on the view that the earnings "
       f"discounted here are struck after the related tax charge. A reader who thinks the "
       f"exposure is incremental should subtract EGP {p2(AU['provisions']/SH)} a share.",
       bold_head='A provision sits outside the bridge. ')
bullet(f"Volume growth by line and the growth in the realised price per tonne are the only free "
       f"operating parameters left, and both are house judgements. Everything else — the margin "
       f"composition, the tax rate, the asset base, the minority share, the dividend — is read "
       f"off a filing.", bold_head='Two free parameters remain, and they are named. ')

# =========================== APPENDIX A ======================================
H1('Appendix A  The filed periods')
H2('A.1  Profit or loss, as filed')
rows = [['EGP mn'] + AU['periods'],
        ['Net sales'] + [n0(AU['rev'][k]) for k in AU['periods']],
        ['Cost of sales'] + [f"({n0(AU['rev'][k]-AU['gp'][k])})" for k in AU['periods']],
        ['GROSS PROFIT'] + [n0(AU['gp'][k]) for k in AU['periods']],
        ['Gross margin'] + [pc(AU['gm'][k], 2) for k in AU['periods']],
        ['Operating profit'] + [n0(AU['ebit'][k]) for k in AU['periods']]]
table(rows, [2.05, 1.22, 1.22, 1.22, 1.22], size=8.4, band_rows={3})
caption('Every column is as filed. No line is reconstructed, driven off a days assumption, or '
        'rolled back through profit and dividends — which is what the previous edition had to do '
        'for all four of its historical columns.')

H2('A.2  Balance sheet at 31 December 2025, as filed')
rows = [['EGP mn', 'Audited'],
        ['Fixed assets, net (note 6)', n0(IN['ppe_net']/M)],
        ['Projects under construction (note 7)', n0(IN['puc']/M)],
        ['Inventory, net (note 9-A)', n0(IN['inventory']/M)],
        ['Accounts receivable, net (note 9-B)', n0(IN['recv']/M)],
        ['Debtors and other debit balances', n0(IN['debtors']/M)],
        ['Cash at banks and on hand (note 9-E)', n0(IN['cash']/M)],
        ['Pledged deposits — not free cash', n0(IN['fin_inv']/M)],
        ['TOTAL ASSETS', n0(IN['assets_snap']/M)],
        ['Accounts and notes payable (note 10-3)', n0(IN['payables']/M)],
        ['Creditors and other credit balances (note 11)', n0(IN['creditors']/M)],
        ['Provisions (note 10-1)', n0(IN['provisions']/M)],
        ['Long-term and short-term loans', n1(AU['debt'])],
        ['TOTAL LIABILITIES', n0(IN['liab_snap']/M)],
        ['Total AMOC equity', n0(IN['eq_parent']/M)],
        ['Non-controlling interest', n0(IN['eq_nci']/M)],
        ['NET WORKING CAPITAL', n0(AU['nwc'])],
        ['INVESTED CAPITAL', n0(AU['ic'])],
        ['NET CASH', n0(-DCF['nd'])]]
table(rows, [4.20, 1.60], size=8.5, band_rows={8, 13, 18})
caption(f"Accounts and notes payable are EGP {n0(IN['payables']/M)}mn — the previous edition "
        f"modelled a trade payable of about EGP 2,500mn funding the working-capital cycle. The "
        f"funding actually sits in the EGPC current account of EGP {n0(IN['egpc_balance']/M)}mn "
        f"inside creditors, which is a different thing with a different counterparty risk.")

box([('What this is. ',
      'An independent, educational valuation study produced by Testahil. It carries no rating, '
      'no recommendation and no price target.'),
     ('Sources. ',
      'Every input carries a value, a source and a date, recorded in the accompanying source '
      'register issued as a separate document. Company figures are read off the audited and '
      'reviewed consolidated financial statements.'),
     ('Not investment advice. ',
      'Educational analysis and personal analytical opinion. The preparer is not licensed by '
      'Egypt\'s Financial Regulatory Authority, manages no money and accepts no clients.')])

OUT = os.path.join(HERE, 'AMOC_Valuation_Study_06-08-2026_public.docx')
doc.save(OUT)
print(f'wrote {os.path.basename(OUT)}')
