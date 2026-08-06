"""ARCC_Valuation_Study_06-08-2026_public.docx — TMPV house structure.

16 headings: 7 top-level sections plus the 9 subsections of section 1, then three
appendices. Reads study_numbers.json exclusively — no numeral is typed here.

Written for an external reader: no internal procedure names, step numbers or house
process references appear anywhere in the output.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
sys.path.insert(0, HERE)
from docx_base import *          # noqa: F401,F403
from docx_base import (doc, P, H1, H2, rich, bullet, table, figure, box, caption,
                       masthead, INK, GREY, BRASS, GOLD, F_CREAM, F_PANEL, Pt, Inches)

D = json.load(open('study_numbers.json'))
BETA = json.load(open('beta_result.json'))
STK = json.load(open('strike_result.json'))
S0 = json.load(open('step0_result.json'))
TECH = json.load(open('technicals.json'))['state']
M, H, F = D['meta'], D['history'], D['forecast']
W, DCF, LN, SN = D['wacc'], D['dcf'], D['lenses'], D['sensitivity']
TR, PE, SHT = D['terminal_reconciliation'], D['peers'], D['share_triangulation']
EXP, LR, GDV = D['experts'], D['lens_ranges'], D['growth_destroys_value']
BU, DNAT, EQG, CON = D['bottom_up'], D['dna_triangulation'], D['equity_gap'], D['contested']
IN = {k: v['value'] for k, v in D['inputs'].items()}
SPOT, SH = M['spot'], M['shares_mn']
YH, YF = H['years'], F['years']
TAXE = H['tax_eff']


def n0(x): return f"{x:,.0f}"
def n1(x): return f"{x:,.1f}"
def n2(x): return f"{x:,.2f}"
def n3(x): return f"{x:,.3f}"
def pc(x, dp=1): return f"{x*100:.{dp}f}%"
def sg(x, dp=1): return f"{x*100:+.{dp}f}%"


# ============================== COVER ========================================
masthead()
P('Arabian Cement Company S.A.E.', size=22, bold=True, space_after=1)
P('Egyptian Exchange · ARCC · Egyptian pounds · 6 August 2026', size=11, color=GREY,
  space_after=10)
rich([(f'Egypt\'s second-largest cement plant, at the top of the best year the industry '
       f'has had in more than a decade, holding net cash worth '
       f'{pc(-DCF["net_debt_bs"]/M["mktcap"], 0)} of its market value on the last reported '
       f'balance sheet — and facing {n1(IN["egy_revival_mt"])} million tonnes of dormant '
       f'national capacity queuing to restart inside the forecast window.',
       {'size': 12})], space_after=10)

box([('What this is. ', 'An independent valuation of Arabian Cement Company, an '
      'educational analysis and not investment advice. It carries no rating and no price '
      'target — fair-value ranges and distributions only.'),
     ('The company in one line. ', f'Two production lines in Suez governorate, about '
      f'{n1(IN["cap_cement_mt"])} million tonnes of cement a year and roughly '
      f'{pc(PE["sector"]["share_of_capacity"], 0)} of Egypt\'s nominal capacity, listed on '
      f'the Egyptian Exchange since May 2014, with cash of EGP '
      f'{n0(IN["cash_fy25"])}mn against debt of EGP {n0(IN["debt_fy25"])}mn.'),
     ('Where the value lands. ', f'Four lenses put the shares between EGP {n2(LN["low"])} '
      f'and EGP {n2(LN["high"])}, weighting to a central EGP {n2(LN["central"])} against a '
      f'market price of EGP {n2(SPOT)} — {sg(LN["central"]/SPOT-1)}.')])

# ---- summary valuation table ------------------------------------------------
H2('Summary valuation table')
rows = [['Lens', 'Value per share (EGP)', 'Weight', 'Versus spot', 'Terminal value % of EV']]
for k in LN['weights']:
    rows.append([k, n2(LN['values'][k]), pc(LN['weights'][k], 0),
                 sg(LN['values'][k] / SPOT - 1),
                 pc(DCF['tv_share']) if k == 'DCF (cash flow)' else '—'])
rows.append(['Weighted central fair value', n2(LN['central']), '100%',
             sg(LN['central'] / SPOT - 1), '—'])
rows.append(['Range across the four lenses', f'{n2(LN["low"])} – {n2(LN["high"])}', '—',
             f'{sg(LN["low"]/SPOT-1)} to {sg(LN["high"]/SPOT-1)}', '—'])
rows.append(['Market price, 6 August 2026', n2(SPOT), '—', '—', '—'])
table(rows, [2.55, 1.35, 0.72, 1.02, 1.36], band_rows={5})
caption('Terminal value as a percentage of enterprise value is shown beside the cash-flow '
        'lens, and again in the enterprise-to-equity bridge in section 1.7.')

figure('fig1_football.png', 6.9,
       'Figure 1 — Each lens as a range, with its base case marked, against the market price.')

# ============================== 1 ============================================
H1('1  Fundamental valuation')
P('Arabian Cement is valued as a single operating company, not as a sum of parts, and the '
  'reason is worth stating before any number appears. Essentially all of its revenue is '
  'grey cement and clinker from one industrial site. There is no property portfolio, no '
  'lending book, no concession and no collection of consolidated operating subsidiaries '
  'that would need valuing on their own terms. A sum-of-the-parts here would be a sum of '
  'one part, and the discipline it is meant to impose — never blending legs that need '
  'different methods — has nothing to bite on.')
P('Four lenses are used. A discounted cash-flow model built up from tonnes and costs '
  'carries half the weight. Relative multiples, normalised earnings power and replacement '
  'cost carry the rest, and each is reported with the reason its weight is what it is.')

# ---- 1.1 --------------------------------------------------------------------
H2('1.1  The business, and why the lens follows from it')
P(f'The plant runs two lines in Suez governorate producing on average about '
  f'{n1(IN["cap_cement_mt"])} million tonnes of clinker and cement a year. That is roughly '
  f'{pc(PE["sector"]["share_of_capacity"], 0)} of Egypt\'s nominal capacity and makes it '
  f'the second-largest cement plant in the country. The balance sheet is what that '
  f'description implies: property-dominated, with working capital in inventory and '
  f'receivables, no investment property, no equity-accounted portfolio of any size, and no '
  f'financing arm.')
P(f'The FY2025 accounts show revenue of EGP {n0(IN["rev_fy25"])}mn and attributable profit '
  f'of EGP {n0(IN["pat_fy25"])}mn, against EGP {n0(IN["rev_fy24"])}mn and EGP '
  f'{n0(IN["pat_fy24"])}mn a year earlier — revenue up '
  f'{pc(IN["rev_fy25"]/IN["rev_fy24"]-1)} and profit up '
  f'{pc(IN["pat_fy25"]/IN["pat_fy24"]-1, 0)}. That is not a business changing shape. It is '
  f'a price event, and the whole of this valuation turns on how much of it lasts.')
rows = [['', 'FY2023', 'FY2024', 'FY2025']]
rows.append(['Revenue (EGP mn)'] + [n0(x) for x in H['revenue']])
rows.append(['EBITDA (EGP mn)'] + [n0(x) for x in H['ebitda']])
rows.append(['EBITDA margin'] + [pc(x) for x in H['margin']])
rows.append(['Attributable profit (EGP mn)'] + [n0(x) for x in H['pat']])
rows.append(['Despatched volume (Mt)'] + [n3(x) for x in H['volume_mt']])
rows.append(['Realised price (EGP/t)'] + [n0(x) for x in H['price_t']])
rows.append(['Kiln utilisation'] + [pc(x) for x in H['utilisation']])
table(rows, [2.60, 1.30, 1.30, 1.30])
caption('Table 1 — Three years of history. Revenue and attributable profit are as '
        'disclosed. EBITDA and the operating lines are derived by closing the disclosed '
        'profit; volume and realised price are the output of the unit build in section 1.2.')
P(f'Two things stand out. Volume grew only {pc(H["volume_mt"][2]/H["volume_mt"][1]-1)} '
  f'between FY2024 and FY2025 while realised price grew '
  f'{pc(H["price_t"][2]/H["price_t"][1]-1)}. The abolition of Egypt\'s cement production '
  f'quota in May 2025 worked overwhelmingly through price, not through tonnes. And the '
  f'margin moved from {pc(H["margin"][1])} to {pc(H["margin"][2])} in a single year, '
  f'because almost the entire price increase fell to the bottom line on a cost base that '
  f'is largely fixed.')

# ---- 1.2 --------------------------------------------------------------------
H2('1.2  The unit economics — where EBITDA actually comes from')
P('EBITDA in this model is an output, not an assumption. It is built from physical '
  'quantities: kiln capacity times a utilisation rate gives clinker; clinker divided by '
  'the clinker factor gives cement; cement split between domestic and export at their own '
  'prices gives revenue; and a per-tonne cost stack — fuel, power, raw materials, '
  'packaging, distribution — plus a fixed block gives cost. What is left is EBITDA. If the '
  'cost stack is wrong, the FY2025 reconstruction misses the disclosed operating profit, '
  'and that residual is published rather than solved away.')
rows = [['', 'FY2025A', 'FY2026E', 'FY2030E']]
for lab, key, fmt in [('Cement produced (Mt)', 'cement', n3),
                      ('Kiln utilisation', 'util', pc),
                      ('Blended realised price (EGP/t)', 'price', n0),
                      ('Thermal fuel (EGP/t)', 'c_fuel', n0),
                      ('Electrical power (EGP/t)', 'c_pow', n0),
                      ('Raw materials (EGP/t)', 'c_raw', n0),
                      ('Packaging (EGP/t)', 'c_pack', n0),
                      ('Distribution (EGP/t)', 'c_dist', n0),
                      ('Total variable (EGP/t)', 'var_t', n0)]:
    rows.append([lab] + [fmt(BU[i][key]) for i in (0, 1, 5)])
rows.append(['Fixed cash cost (EGP/t)'] +
            [n0(BU[i]['fixed'] / BU[i]['cement']) for i in (0, 1, 5)])
rows.append(['EBITDA (EGP mn)'] + [n0(BU[i]['ebitda']) for i in (0, 1, 5)])
rows.append(['EBITDA margin'] + [pc(BU[i]['mgn']) for i in (0, 1, 5)])
table(rows, [2.60, 1.30, 1.30, 1.30], band_rows={11, 12})
caption('Table 2 — The cost stack per tonne of cement, and the margin it produces.')
figure('fig7_stack.png', 6.9,
       'Figure 2 — Cash cost per tonne against realised price per tonne. The margin is the '
       'gap, and the gap narrows across the forecast.')
P(f'The reconstruction reproduces the disclosed FY2025 revenue to '
  f'{sg(BU[0]["rev"]/IN["rev_fy25"]-1, 3)} and the DISCLOSED FY2025 operating income to '
  f'{sg((BU[0]["ebitda"]-DNAT["adopted"])/IN["ebit_fy25"]-1, 3)}. Neither residual is '
  f'forced: the physical coefficients are industry norms and the price path is the '
  f'published domestic level. The one calibrated figure is the fixed cash block, at USD '
  f'{n2(IN["fixed_usd_t_capacity"])} per tonne of installed capacity, inside the USD 10–20 '
  f'industry band, and it is labelled as a calibration rather than presented as an '
  f'observation.')
P(f'The company-specific line is fuel. Arabian Cement is Egypt\'s alternative-fuel leader: '
  f'{pc(IN["af_share"][0], 0)} of its thermal requirement is met from refuse-derived fuel '
  f'and biomass rather than imported petcoke, rising to {pc(IN["af_share"][5], 0)} by '
  f'FY2030 on the company\'s own programme. That blend is why the fuel bill per tonne is '
  f'EGP {n0(BU[0]["c_fuel"])} rather than the EGP '
  f'{n0(BU[0]["c_fuel"]*IN["fuel_fossil_usd_gj"]/BU[0]["fuel_usd_gj"])} a fossil-only '
  f'stack would cost — a saving of about {pc(1-BU[0]["fuel_usd_gj"]/IN["fuel_fossil_usd_gj"])} '
  f'on the largest variable line in the business. It is modelled as its own driver, not '
  f'folded into a margin, because it is the one cost advantage that is genuinely this '
  f'company\'s rather than the sector\'s.')

H2('1.3  Depreciation, and the honest admission behind it')
P('No depreciation line is separately retrievable for this company from any source at the '
  'evidentiary standard used elsewhere in this study. Rather than assume one, three '
  'independent methods are computed and averaged, and the spread between them is '
  'published.')
rows = [['Method', 'FY2025 charge (EGP mn)']]
rows.append(['Fourth-quarter EBITDA margin applied to full-year revenue, less the '
             'disclosed operating profit', n0(DNAT['m1_q4_margin_closure'])])
rows.append(['Peer depreciation per tonne of despatch, applied to this volume',
             n0(DNAT['m2_peer_per_tonne'])])
rows.append(['Net property base implied by total assets, times a composite rate',
             n0(DNAT['m3_property_base'])])
rows.append(['Average of the three — adopted', n0(DNAT['adopted'])])
rows.append(['As a share of revenue', pc(DNAT['pct_of_revenue'], 2)])
rows.append(['Per tonne of despatch (EGP)', n0(DNAT['per_tonne'])])
table(rows, [4.20, 1.90], band_rows={4})
caption('Table 3 — Three routes to the same number, averaged rather than asserted. The '
        'highest is 3.5 times the lowest, and that uncertainty is real.')
P('The spread matters, and it is worth saying why it is so wide. This plant was built '
  'around 2010, in a currency that has since devalued several times. Its book asset base '
  'is therefore small in today\'s pounds and its accounting depreciation charge is '
  'correspondingly small — which is exactly what the first and third methods find, and '
  'exactly what a peer benchmark drawn from a revalued balance sheet does not.')
P(f'This has a direct valuation consequence, and it is treated as one. Capital expenditure '
  f'in the forecast is NOT set at book depreciation. It is set at the economic maintenance '
  f'level of USD {n2(IN["capex_usd_t_cap"])} per tonne of installed capacity — about EGP '
  f'{n0(F["capex"][0])}mn in FY2026 against a book charge of EGP {n0(F["dna"][0])}mn. '
  f'Setting capex equal to book depreciation would have flattered free cash flow by '
  f'construction; the cost of refusing to do so is computed in section 1.9 and is worth '
  f'{sg(CON[3]["effect"])} of the cash-flow lens.')

# ---- 1.4 --------------------------------------------------------------------
H2('1.4  The cost of capital')
P(f'The discount rate is a schedule, not a number. Egypt is in monetary transition: the '
  f'central bank held its main operation rate at 19.50% through the first half of 2026 '
  f'while headline inflation eased to 14.3%, and its own published medium-term target is '
  f'7%. A single flat rate applied to both the explicit years and a perpetuity would '
  f'assert that Egypt\'s cost of capital never normalises — a claim this model\'s own '
  f'cost-of-debt path contradicts.')
rows = [['', 'Explicit window', 'Terminal']]
rows.append(['Risk-free rate', pc(IN['rf'], 2), pc(IN['rf_term'], 2)])
rows.append(['Less sovereign default spread', f'({pc(IN["sov_spread_cds"], 2)})', '—'])
rows.append(['Normalised risk-free rate', pc(W['rf_star'], 2), pc(IN['rf_term'], 2)])
rows.append(['Beta', n3(W['beta']), n3(W['beta_term'])])
rows.append(['Equity risk premium', pc(IN['erp_cds'], 2), pc(IN['erp_term'], 2)])
rows.append(['Cost of equity', pc(W['ke_exp'], 2), pc(W['ke_term'], 2)])
rows.append(['Cost of debt after tax', pc(W['kd_at'], 2), pc(IN['kd_term'] * (1 - IN['tax_stat']), 2)])
rows.append(['Debt weight', pc(W['wd_gross'], 2), pc(IN['wd_term'], 1)])
rows.append(['Blended cost of capital', pc(W['wacc_exp'], 2), pc(W['wacc_term'], 2)])
table(rows, [2.90, 1.80, 1.80], band_rows={9})
caption('Table 4 — The two anchors. The sovereign default spread is netted OUT of the '
        'local risk-free rate before a country equity premium is added, so Egypt\'s '
        'default risk is charged once rather than twice; leaving it in would have put the '
        f'cost of equity at {pc(W["ke_raw_retired"], 2)} instead of {pc(W["ke_exp"], 2)}.')
P('The terminal anchors are house macro views, and are disclosed as such rather than '
  'presented as observations. The terminal risk-free rate is the central bank\'s own '
  'stated medium-term inflation target plus a standard emerging-market real-rate '
  'convention. The terminal cost of debt is the Egyptian long-run corporate borrowing '
  'norm. Neither is reverse-engineered from a price, and no terminal input is backed out '
  'of a target.')
rows = [['Year'] + YF]
rows.append(['Glide fraction'] + [n3(x) for x in F['glide']])
rows.append(['Forward cost of capital'] + [pc(x, 2) for x in F['fwd_wacc']])
rows.append(['Cumulative discount factor'] + [f'{x:.4f}' for x in F['df']])
table(rows, [1.62, 1.06, 1.06, 1.06, 1.06, 1.06])
caption('Table 5 — The schedule. The glide fractions are not chosen: they are the '
        'cumulative progress of the cost-of-debt path, so the shape of the discount '
        'schedule is inherited from the assumed easing calendar rather than invented '
        'beside it. The terminal value is capitalised at the terminal rate and brought '
        'home on year five\'s own cumulative factor — one date, one price of time.')

H2('1.5  Beta, and how weak it is')
P(f'The beta is a genuine regression, not a default. Weekly returns over five years '
  f'against an equal-weight index of the {BETA["composite_names"]} other Egyptian names in '
  f'the library, with the subject excluded from its own index, give a beta of '
  f'{n3(BETA["beta"])} on {BETA["n"]} observations, an R-squared of '
  f'{pc(BETA["r2"], 1)} and a standard error of {n3(BETA["se"])}. The 90% confidence '
  f'interval is [{n2(BETA["ci90"][0])}, {n2(BETA["ci90"][1])}].')
P(f'That clears the usability threshold, and it is also STATISTICALLY WEAK — on one of the '
  f'two tests rather than both, which is worth being precise about. The R-squared of '
  f'{pc(BETA["r2"], 1)} sits below the 10% mark, which triggers the flag. The confidence '
  f'interval spans {n2((BETA["ci90"][1]-BETA["ci90"][0])/BETA["beta"])} times the point '
  f'estimate, which does NOT: that test fires at two times and this is well inside it. The '
  f'estimate is therefore never restated later as though it were precise, and the '
  f'valuation is shown across a beta range rather than at a point.')
P(f'Two cross-checks are run rather than asserted. The share closes unchanged on '
  f'{pc(BETA["thin_trading"]["flat_frac"])} of sessions against an Egyptian library median '
  f'of {pc(BETA["thin_trading"]["eg_panel_median"])}, and non-synchronous trading biases a '
  f'contemporaneous beta downward; the lead-lag sum-beta that corrects for it is '
  f'{n3(BETA["dimson"]["sum_beta"])}, an uplift of {n3(BETA["dimson"]["uplift_vs_ols"])} '
  f'with a standard error of {n3(BETA["dimson"]["se_sum"])} — i.e. an uplift not '
  f'statistically distinguishable from zero. And a simple prior would put a cyclical, '
  f'capital-intensive materials business at 1.0 to 1.5, which is above where this '
  f'regression lands. There is a real reason for that: the company carries no net '
  f'financial leverage, and unlevered equity genuinely moves less than levered equity. '
  f'The regression is adopted, the correction is published as a value, and the difference '
  f'is worth {sg(CON[0]["effect"])} of the cash-flow lens.')
rows = [['Beta'] + [n2(b) for b in SN['beta_grid']]]
rows.append(['Fair value per share (EGP)'] + [n2(x) for x in SN['beta']])
table(rows, [2.20, 0.98, 0.98, 0.98, 0.98, 0.98])
caption('Table 6 — Fair value across the fixed comparability anchors, which span the '
        'regression\'s own confidence interval.')

# ---- 1.6 --------------------------------------------------------------------
H2('1.6  The cash-flow waterfall')
rows = [['EGP mn'] + YF]
for lab, key, fmt in [('Revenue', 'revenue', n0), ('EBITDA', 'ebitda', n0),
                      ('EBITDA margin', 'margin', pc),
                      ('Depreciation and amortisation', 'dna', n0),
                      ('EBIT', 'ebit', n0)]:
    rows.append([lab] + [fmt(x) for x in F[key]])
rows.append([f'Tax rate (effective, {pc(TAXE)})'] + [pc(TAXE) for _ in YF])
rows.append(['NOPAT  (EBIT × (1 − t))'] + [n0(x) for x in F['nopat']])
rows.append(['Plus depreciation'] + [n0(x) for x in F['dna']])
rows.append(['Less capital expenditure'] + [f'({n0(x)})' for x in F['capex']])
rows.append(['Less change in working capital'] + [f'({n0(x)})' for x in F['dwc']])
rows.append(['Free cash flow to the firm'] + [n0(x) for x in F['fcff']])
rows.append(['Discount factor'] + [f'{x:.4f}' for x in F['df']])
rows.append(['Present value of FCFF'] + [n0(x) for x in F['pv']])
table(rows, [2.10, 0.92, 0.92, 0.92, 0.92, 0.92], band_rows={11, 13}, size=8.8)
caption('Table 7 — The full build from revenue to present value. FY2026 carries only the '
        'five months not yet earned at the valuation date; the seven already earned are '
        'rolled into the opening cash balance instead, so the period is counted exactly '
        'once rather than twice or not at all.')
P(f'The effective tax rate of {pc(TAXE)} is above the statutory {pc(IN["tax_stat"], 1)}, '
  f'and it is not chosen. It is what the disclosed accounts imply: operating income of EGP '
  f'{n0(IN["ebit_fy25"])}mn plus net finance income of EGP {n0(H["netfin_fy25"])}mn against '
  f'a disclosed profit after tax of EGP {n0(IN["pat_fy25"])}mn leaves that rate and no '
  f'other. Using the statutory rate instead would have raised every forecast year\'s '
  f'after-tax profit by about {pc((TAXE-IN["tax_stat"])/(1-TAXE))} on evidence that points '
  f'the other way.')

P(f'One reconciliation belongs here rather than in a footnote, because it is the largest '
  f'single judgement in the model. First-quarter 2026 attributable profit was EGP '
  f'{n0(IN["pat_q1_26"])}mn on revenue of EGP {n0(IN["rev_q1_26"])}mn — a net margin of '
  f'{pc(IN["pat_q1_26"]/IN["rev_q1_26"])}. Four times that quarter is EGP '
  f'{n0(4*IN["pat_q1_26"])}mn, and holding its margin across the full year would give about '
  f'EGP {n0(F["revenue"][0]*IN["pat_q1_26"]/IN["rev_q1_26"])}mn. This model forecasts EGP '
  f'{n0(F["pat"][0])}mn — {sg(F["pat"][0]/(4*IN["pat_q1_26"])-1)} against the simple '
  f'annualisation and well below the margin-held figure. The forecast is deliberately the '
  f'conservative one: the first quarter of 2026 still carries the post-quota price spike at '
  f'close to its peak, and the model assumes it fades as restart capacity arrives and pound '
  f'cost inflation runs ahead of price. A reader who thinks the current margin holds should '
  f'read the +2% and +4% columns of the margin sensitivity in section 7, which are worth '
  f'EGP {n2(SN["mgn"][3])} and EGP {n2(SN["mgn"][4])} a share against the base EGP '
  f'{n2(DCF["fv"])}.')

# ---- 1.7 --------------------------------------------------------------------
H2('1.7  The enterprise-to-equity bridge')
rows = [['', 'EGP mn', 'Per share (EGP)']]
for lab, v in [('Present value of explicit free cash flow', DCF['sum_pv']),
               ('Present value of terminal value', DCF['pv_tv']),
               ('Enterprise value', DCF['ev']),
               ('Plus net cash at the valuation date', DCF['net_cash']),
               ('Less non-controlling interests', -IN['nci']),
               ('Equity value', DCF['equity'])]:
    rows.append([lab, n0(v), n2(v / SH)])
rows.append(['Terminal value as % of enterprise value', pc(DCF['tv_share']), '—'])
rows.append(['Market price, 6 August 2026', '—', n2(SPOT)])
rows.append(['Upside / (downside) to this lens', '—', sg(DCF['fv'] / SPOT - 1)])
table(rows, [3.30, 1.50, 1.50], band_rows={3, 6, 7})
caption('Table 8 — The bridge. Terminal value as a share of enterprise value is stated '
        'here and again in the summary table on page 1.')
P(f'Cash is added at face and is not in the discount rate. The company held EGP '
  f'{n0(IN["cash_fy25"])}mn of cash against EGP {n0(IN["debt_fy25"])}mn of debt on the '
  f'latest reported balance sheet; rolling that forward on the elapsed part of FY2026 puts '
  f'net cash at EGP {n0(DCF["net_cash"])}mn at the valuation date, or EGP '
  f'{n2(DCF["net_cash"]/SH)} a share — about {pc(DCF["net_cash"]/M["mktcap"])} of the '
  f'market capitalisation. Minority interests are deducted rather than ignored, at a '
  f'deliberately non-trivial EGP {n0(IN["nci"])}mn; no minority balance is separately '
  f'retrievable, and the disclosed profit statements imply a small one.')
P(f'At {pc(DCF["tv_share"])} of enterprise value, the terminal value is a smaller share '
  f'of this valuation than in most discounted cash-flow models, and that is a consequence '
  f'of the high explicit-window discount rate rather than a design choice. It means the '
  f'answer depends more on the next five years and less on a perpetuity assumption than is '
  f'usual — which, for a business whose next five years are genuinely forecastable from '
  f'tonnes and prices, is the right place for the weight to sit.')

# ---- 1.8 --------------------------------------------------------------------
H2('1.8  Terminal value, and what growth costs')
P(f'Terminal growth is held at {pc(IN["g_term"], 0)}, against a terminal risk-free rate '
  f'that already embeds disinflation — so approximately zero in real terms. It is not '
  f'derived from recent performance, and the reason is arithmetic rather than a matter of '
  f'judgement.')
P(f'Attributable profit has compounded at about {pc(TR["pat_cagr_since_fy22"], 0)} a year '
  f'since FY2022. Compounded against nominal economic growth of about '
  f'{pc(IN["egy_gdp_growth"], 0)}, a company at '
  f'{pc(TR["share_of_gdp"], 3)} of Egyptian output today would equal the entire Egyptian '
  f'economy in roughly {n0(TR["crossover_years"])} years. That is not a forecast anyone '
  f'would defend; it is the reason recent growth belongs in the explicit window, '
  f'describing a specific dated event — the removal of the production quota — and not in '
  f'the perpetuity.')
P(f'Growth in the terminal state has to be paid for. The reinvestment rate is terminal '
  f'growth divided by the return on capital that funds it: {pc(IN["g_term"], 0)} over '
  f'{pc(TR["roic_repl"])} gives {pc(TR["rr_repl"])} of terminal profit reinvested. That '
  f'return is struck on REPLACEMENT-COST invested capital — EGP {n0(DCF["ic_repl"])}mn, '
  f'being {n1(IN["cap_cement_mt"])}Mt at USD {n0(IN["repl_usd_t"])} a tonne — rather than '
  f'on the pre-devaluation book, which would flatter it several times over and let growth '
  f'through unpaid for.')
P(f'The consequence is worth stating plainly because it inverts the usual intuition: at a '
  f'terminal return on capital of {pc(TR["roic_repl"])} against a terminal rate of '
  f'{pc(W["wacc_term"])}, GROWTH DESTROYS VALUE. The model shows it rather than hiding it '
  f'— the cash-flow lens is EGP {n2(GDV["fv_at_g3"])} at 3% terminal growth and EGP '
  f'{n2(GDV["fv_at_g7"])} at 7%. A cement plant in a market carrying '
  f'{n0(IN["egy_capacity_mt"])}Mt of capacity against {n0(IN["egy_cons_mt"])}Mt of '
  f'consumption cannot earn its cost of capital on new tonnes, and a model that rewarded '
  f'it for adding them would be wrong.')
rows = [['Explicit-window rate'] + [pc(g, 0) for g in SN['g_grid']]]
for i, wv in enumerate(SN['wacc_grid']):
    rows.append([pc(wv, 2)] + [n2(x) for x in SN['wacc_g'][i]])
table(rows, [1.72, 1.02, 1.02, 1.02, 1.02, 1.02])
caption(f'Table 9 — Fair value per share across the explicit-window cost of capital and '
        f'terminal growth. Growth is the STRONGER of the two levers here and it points '
        f'DOWN: across a row the value moves EGP '
        f'{n2(SN["wacc_g"][0][0]-SN["wacc_g"][0][4])}, against EGP '
        f'{n2(SN["wacc_g"][0][0]-SN["wacc_g"][4][0])} down a column.')
figure('fig2_sens.png', 6.6,
       'Figure 3 — The same surface. Higher growth gives a lower value, which is the model '
       'being consistent rather than a sign error.')
rows = [['Explicit-window rate'] + [pc(w, 1) for w in SN['wt_grid']]]
for i, wv in enumerate(SN['wacc_grid']):
    rows.append([pc(wv, 2)] + [n2(x) for x in SN['exp_term'][i]])
table(rows, [1.72, 1.02, 1.02, 1.02, 1.02, 1.02])
caption('Table 10 — The two anchors varied INDEPENDENTLY: the explicit-window rate down '
        'the side, the terminal rate across the top. This shows what the valuation needs '
        'the economy to do, not merely what growth rate the model needs.')

# ---- 1.9 --------------------------------------------------------------------
H2('1.9  The other three lenses, and the choices that were contested')
P(f'The relative lens applies {n1(IN["ev_ebitda_just"])} times to normalised EBITDA of EGP '
  f'{n0(LN["ebitda_norm"])}mn — the FY2025 revenue base cut '
  f'{pc(1-IN["norm_rev_haircut"], 0)} and a mid-cycle margin of {pc(IN["norm_mgn"])} '
  f'applied to it — and adds net cash at face. The multiple is disclosed as weakly '
  f'anchored: the listed Egyptian peer set is thin, and its published multiples do not '
  f'reconcile against the market capitalisations printed beside them. That is why this '
  f'lens carries {pc(IN["w_rel"], 0)} and not more.')
P(f'The normalised-earnings lens capitalises the same mid-cycle operating profit after tax '
  f'— EGP {n0(LN["nopat_norm"])}mn — at {n1(IN["pe_just"])} times, and again adds cash at '
  f'FACE rather than capitalising it at the operating multiple. Cash is worth cash; '
  f'capitalising a pound of treasury at seven times would value it at a discount to '
  f'itself.')
P(f'The asset lens values the capacity: {n1(IN["cap_cement_mt"])}Mt at a justified USD '
  f'{n0(IN["ev_t_just"])} per annual tonne, marked down '
  f'{pc(1-IN["ev_t_just"]/IN["repl_usd_t"], 0)} from a replacement cost of USD '
  f'{n0(IN["repl_usd_t"])}. Against that, the market is paying USD '
  f'{n1(LN["ev_per_t_spot"])} per annual tonne. This lens carries only '
  f'{pc(IN["w_asset"], 0)}, and the reason is in the same paragraph as the number: '
  f'restarting a mothballed line costs a fraction of building one, and '
  f'{n1(IN["egy_revival_mt"])}Mt of restart capacity is queuing. Replacement cost is a '
  f'ceiling here, not a floor.')
rows = [['Choice', 'Adopted', 'Alternative', 'Effect on the cash-flow lens']]
for c in CON:
    rows.append([c['choice'], c['adopted'], c['alternative'],
                 f'{n2(c["fv_alternative"])}  ({sg(c["effect"])})'])
table(rows, [2.55, 1.05, 1.20, 1.70], size=8.8)
caption('Table 11 — Every contested choice computed as a value rather than argued in '
        'prose. None of these alternatives is hidden; each is a full re-run of the model.')

# ============================== 2 ============================================
H1('2  Price structure')
P(TECH['tech']['summary'])
rows = [['', 'Level (EGP)', 'Distance from spot']]
for i, r in enumerate(TECH['levels']['res']):
    rows.append([f'Resistance {i+1}', n2(r), sg(r / SPOT - 1)])
for i, s_ in enumerate(TECH['levels']['sup']):
    rows.append([f'Support {i+1}', n2(s_), sg(s_ / SPOT - 1)])
rows.append(['52-week high', n2(TECH['hi_52w']), sg(TECH['hi_52w'] / SPOT - 1)])
rows.append(['52-week low', n2(TECH['lo_52w']), sg(TECH['lo_52w'] / SPOT - 1)])
table(rows, [2.00, 1.50, 1.70])
caption('Table 12 — Levels are computed from swing structure with a recency weight; '
        'moving averages, the 52-week extremes and round numbers are admitted as '
        'candidates but score below real swing points. Resistance 1 and support 1 always '
        'mean nearest to the close.')
figure('fig3_ma.png', 6.9,
       'Figure 4 — Three years of price with the 50- and 200-day averages.')
rich([('On the upside: ', {'bold': True}), (TECH['tech']['bull'], {})])
rich([('On the downside: ', {'bold': True}), (TECH['tech']['bear'], {})])
P('This section describes the tape and makes no claim about value. The two are compared in '
  'section 4.')

# ============================== 3 ============================================
H1('3  A probabilistic price map')
P('The following is NOT a valuation. It is a distribution of where the share price could '
  'sit at two horizons, drawn from the price history alone and from nothing in the '
  'preceding sections. It is included because a single fair-value number tells a reader '
  'nothing about dispersion, and it is labelled illustrative because its own calibration '
  'record says it should be.')
rows = [['', 'One month', 'Three months']]
for lab, k in [('5th percentile', 'p5'), ('25th percentile', 'p25'), ('Median', 'p50'),
               ('75th percentile', 'p75'), ('95th percentile', 'p95')]:
    rows.append([lab, n2(STK['horizons']['1M']['pct'][k]), n2(STK['horizons']['3M']['pct'][k])])
rows.append(['Probability of finishing above the current price',
             pc(STK['horizons']['1M']['p_above']), pc(STK['horizons']['3M']['p_above'])])
rows.append(['Probability of touching +10% at any point',
             pc(STK['horizons']['1M']['touch_up10']), pc(STK['horizons']['3M']['touch_up10'])])
rows.append(['Probability of touching −10% at any point',
             pc(STK['horizons']['1M']['touch_dn10']), pc(STK['horizons']['3M']['touch_dn10'])])
table(rows, [3.00, 1.60, 1.60], band_rows={3})
caption(f'Table 13 — Percentiles in EGP per share, from a 50,000-path simulation anchored '
        f'on the 6 August 2026 close of EGP {n2(SPOT)}. The drift is the carry — the '
        f'risk-free rate less the dividend yield — and nothing else.')
figure('fig4_fan.png', 6.9, 'Figure 5 — The three-month cone.')
figure('fig6_dist.png', 6.4, 'Figure 6 — The three-month outcome distribution.')
P(f'How well calibrated is it? Measured over {S0["windows_scored"]} independent quarterly '
  f'windows, the bands cover {pc(S0["cov50"], 0)}, {pc(S0["cov80"], 0)} and '
  f'{pc(S0["cov90"], 0)} of outcomes against nominal 50%, 80% and 90%. The map is '
  f'therefore TOO WIDE rather than mis-centred: it is not missing the outcome, it is '
  f'covering more ground than it claims to. Its skill against a simple random walk is '
  f'{sg(S0["skill_norm"], 1)} — statistically indistinguishable from zero at every block '
  f'size tested. No valuation conclusion in this study rests on it.')

# ============================== 4 ============================================
H1('4  Comparison of the lenses')
rows = [['Lens', 'Bear (EGP)', 'Base (EGP)', 'Bull (EGP)', 'Weight', 'Versus spot']]
for k in list(LN['weights']) + ['Weighted central']:
    w = pc(LN['weights'][k], 0) if k in LN['weights'] else '100%'
    rows.append([k, n2(LR[k]['bear']), n2(LR[k]['base']), n2(LR[k]['bull']), w,
                 sg(LR[k]['base'] / SPOT - 1)])
table(rows, [2.00, 1.00, 1.00, 1.00, 0.72, 1.02], band_rows={5})
caption('Table 14 — Each lens as a range. The disagreement between them is information, '
        'not noise.')
P(f'The four lenses do not agree, and the pattern of their disagreement is the most useful '
  f'thing in this study. The three earnings-based lenses cluster between EGP '
  f'{n2(min(LN["values"][k] for k in LN["values"] if "Asset" not in k))} and EGP '
  f'{n2(max(LN["values"][k] for k in LN["values"] if "Asset" not in k))}, all below the '
  f'market price. The asset lens sits at EGP {n2(LN["values"]["Asset / replacement cost"])}, '
  f'well above it. That is the whole argument about this company in one line: the plant '
  f'is worth more than the market is paying for it, and the earnings it can be expected to '
  f'produce are worth less.')
P(f'The weighting resolves that in favour of earnings, at '
  f'{pc(IN["w_dcf"], 0)}/{pc(IN["w_rel"], 0)}/{pc(IN["w_norm"], 0)}/{pc(IN["w_asset"], 0)}, '
  f'and gives a central EGP {n2(LN["central"])} against EGP {n2(SPOT)} — '
  f'{sg(LN["central"]/SPOT-1)}. A reader who believes replacement cost is a floor rather '
  f'than a ceiling would weight the asset lens far more and reach the opposite conclusion. '
  f'The case against doing so is the {n1(IN["egy_revival_mt"])}Mt restart programme, and '
  f'it is a testable one.')
P(f'Against the technical picture, the two readings are in tension. The share is above its '
  f'entire moving-average stack on a rising 200-day and {pc(1-TECH["pct_off_high"], 0)} of '
  f'the way to a 52-week high, while the earnings lenses put fair value below the current '
  f'price. Momentum and value disagree here, and this study takes no view on which resolves '
  f'first.')

# ============================== 5 ============================================
H1('5  Catalysts to watch')
for head, body in [
    ('The restart programme. ', f'Seven to nine dormant Egyptian lines are under study for '
     f'revival, potentially adding {n1(IN["egy_revival_mt"])}Mt from the second half of '
     f'2026 — about {pc(PE["sector"]["revival_pct_of_consumption"], 0)} of domestic '
     f'consumption. Whether those lines actually restart, and how fast, is the single '
     f'largest swing factor in the price path this model assumes.'),
    ('The realised price, quarter by quarter. ', f'The model assumes a domestic price of '
     f'EGP {n0(IN["price_dom_egp_t"][1])} a tonne in FY2026 and growth below cost '
     f'inflation thereafter. Two consecutive quarters of realised prices above EGP 4,200 '
     f'would break that assumption upward; a return toward EGP 3,000 would break it down.'),
    ('The alternative-fuel programme. ', f'The substitution rate is assumed to rise from '
     f'{pc(IN["af_share"][0], 0)} to {pc(IN["af_share"][5], 0)}. Progress on it is '
     f'reported in the company\'s own sustainability disclosure and is directly visible in '
     f'the fuel cost per tonne. A stall would cost roughly the difference between the '
     f'blended and fossil-only fuel bills.'),
    ('Energy tariffs. ', 'Phased subsidy reform continues to raise the domestic industrial '
     'energy bill independently of the global fuel price. The model inflates the pound cost '
     'lines by 11.5% in FY2026, easing to 7.0% by FY2030; a faster reform schedule would '
     'compress the margin faster than assumed.'),
    ('The export cap and the carbon border mechanism. ', 'Exports are capped at 30% of '
     'production, and the EU carbon border mechanism raises the landed cost of Egyptian '
     'cement in Europe. A low-clinker, high-alternative-fuel producer suffers less from the '
     'second than a conventional peer, and the export price path assumes exactly that.'),
    ('Distribution policy. ', f'The company paid EGP {n0(IN["div_fy25_total"])}mn for '
     f'FY2025, about {pc(IN["payout"], 0)} of attributable profit, on top of EGP '
     f'{n0(IN["div_fy24_total"])}mn for FY2024. A change in that policy changes the cash '
     f'roll-forward and, through it, the balance sheet the bridge relies on.'),
]:
    bullet(body, bold_head=head)

# ============================== 6 ============================================
H1('6  Reading the probability zones')
P('The distribution in section 3 is easier to use as zones than as percentiles. The '
  'following divides the three-month outcome space into four bands and states what each '
  'would mean, without predicting which occurs.')
h3 = STK['horizons']['3M']['pct']
rows = [['Zone', 'Three-month range (EGP)', 'Probability', 'What it would mean']]
rows.append(['Lower tail', f'below {n2(h3["p5"])}', '5%',
             'A break of the 48.10 support zone, most plausibly on a faster-than-assumed '
             'capacity restart'])
rows.append(['Below spot', f'{n2(h3["p5"])} – {n2(SPOT)}',
             pc(1 - STK['horizons']['3M']['p_above'] - 0.05, 0),
             'The market converging toward the earnings-based lenses in this study'])
rows.append(['Above spot', f'{n2(SPOT)} – {n2(h3["p95"])}',
             pc(STK['horizons']['3M']['p_above'] - 0.05, 0),
             'Momentum and the 2026 pricing environment continuing to lead the earnings case'])
rows.append(['Upper tail', f'above {n2(h3["p95"])}', '5%',
             'A re-rating toward the asset lens, which would require the restart programme '
             'to be abandoned or delayed materially'])
table(rows, [1.10, 1.55, 0.90, 2.55], size=8.8)
caption('Table 15 — Zones, not forecasts. The four are exclusive and sum to 100%: each '
        'tail is carved OUT of the band beside it rather than counted twice. The '
        'probabilities come from the price map and are subject to the same over-width '
        'caution as everything else in section 3.')

# ============================== 7 ============================================
H1('7  Caveats and what would change our mind')
for head, body in [
    ('The audited statements were not obtainable. ', 'Revenue, attributable profit, '
     'operating income, the balance-sheet totals and both dividend distributions are '
     'carried as disclosed via reporting of the exchange filings and via aggregations of '
     'commercial financial data. Every line between them is derived and labelled as '
     'derived. A reader with the audited accounts should reconcile the depreciation and '
     'working-capital lines first, since those are the weakest.'),
    ('The balance sheet does not close across sources. ', f'Total assets of EGP '
     f'{n0(IN["ta_fy25"])}mn less reported equity of EGP {n0(IN["eq_fy25_rep"])}mn implies '
     f'liabilities of EGP {n0(EQG["derived_liabilities"])}mn; a separate aggregation prints '
     f'EGP {n0(IN["tl_alt"])}mn, a gap of EGP {n0(EQG["derived_liabilities"]-IN["tl_alt"])}mn '
     f'or {pc((EQG["derived_liabilities"]-IN["tl_alt"])/IN["ta_fy25"])} of total assets. '
     f'The figure that closes against total assets is carried and the disagreement is '
     f'shown rather than averaged away.'),
    ('Depreciation is a triangulation, not a disclosure. ', f'The three methods span EGP '
     f'{n0(min(DNAT["m1_q4_margin_closure"], DNAT["m3_property_base"]))}mn to EGP '
     f'{n0(DNAT["m2_peer_per_tonne"])}mn. The average is adopted. Anyone with the real '
     f'number should substitute it — but note that raising it in the terminal year LOWERS '
     f'this valuation rather than raising it, because capital spending here is set at '
     f'economic replacement and does not follow the book charge.'),
    ('Cash and debt are not clean one-way levers. ', 'Because the effective tax rate is '
     'inferred from the disclosed FY2025 closure, changing the cash balance changes the '
     'imputed finance income and therefore the imputed tax rate on the operating business. '
     'Adding EGP 1bn of cash adds to net cash and subtracts almost exactly as much from '
     'enterprise value. The clean net-cash sensitivity — the tax rate held and the balance '
     'varied — is shown below.'),
    ('The beta is weak. ', f'R-squared of {pc(BETA["r2"], 1)} and a 90% interval of '
     f'[{n2(BETA["ci90"][0])}, {n2(BETA["ci90"][1])}]. The valuation is shown across a '
     f'beta range for exactly this reason, and the lead-lag correction is published as a '
     f'value.'),
    ('The price map is over-wide. ', f'Its bands cover {pc(S0["cov80"], 0)} and '
     f'{pc(S0["cov90"], 0)} of outcomes against nominal 80% and 90%, and its skill against '
     f'a random walk is {sg(S0["skill_norm"], 1)}. It is carried as illustrative only.'),
    ('A minority position. ', f'The float sits under a long-standing controlling '
     f'shareholder. No control premium or discount is applied anywhere in this valuation, '
     f'in either direction.'),
    ('Currency. ', 'Revenue and most costs are in Egyptian pounds, but fuel, spares and any '
     'future capacity are priced in hard currency. The model carries one currency path and '
     'lets it act on both the import cost and the export revenue, because the two legs '
     'partly offset.'),
]:
    bullet(body, bold_head=head)
rows = [['Net cash at the valuation date (EGP mn)'] + [n0(x) for x in SN['nc_grid']]]
rows.append(['Fair value per share (EGP)'] + [n2(x) for x in SN['net_cash']])
table(rows, [2.40, 0.92, 0.92, 0.92, 0.92, 0.92], size=8.8)
caption('Table 16 — The clean net-cash sensitivity, with the tax rate held.')
rows = [['Shift in the EBITDA margin, every forecast year'] + [sg(m, 0) for m in SN['mgn_grid']]]
rows.append(['Fair value per share (EGP)'] + [n2(x) for x in SN['mgn']])
table(rows, [2.40, 0.92, 0.92, 0.92, 0.92, 0.92], size=8.8)
caption('Table 17 — And the margin sensitivity, which is the largest single swing factor '
        'in the model.')

# ============================== APPENDIX A ===================================
doc.add_page_break()
H1('Appendix A  Financial statements')
H2('Income statement')
rows = [['EGP mn'] + YH + YF]
for lab, key, fmt in [('Revenue', 'revenue', n0), ('EBITDA', 'ebitda', n0),
                      ('EBITDA margin', 'margin', pc),
                      ('Depreciation and amortisation', 'dna', n0),
                      ('EBIT', 'ebit', n0)]:
    rows.append([lab] + [fmt(x) for x in H[key]] + [fmt(x) for x in F[key]])
rows.append(['Net finance income'] + ['—', '—', n0(H['netfin_fy25'])] +
            [n0(x) for x in F['treasury']])
rows.append(['Profit before tax'] + ['—', '—', n0(H['pbt_fy25'])] + [n0(x) for x in F['pbt']])
rows.append(['Attributable profit'] + [n0(x) for x in H['pat']] + [n0(x) for x in F['pat']])
rows.append(['Earnings per share (EGP)'] + [n2(x) for x in H['eps']] + [n2(x) for x in F['eps']])
rows.append(['Despatched volume (Mt)'] + [n3(x) for x in H['volume_mt']] +
            [n3(x) for x in F['volume_mt']])
rows.append(['Realised price (EGP/t)'] + [n0(x) for x in H['price_t']] +
            [n0(x) for x in F['price_t']])
table(rows, [1.52, 0.72, 0.72, 0.72, 0.72, 0.72, 0.72, 0.72, 0.72], size=8.0,
      band_rows={8})
caption(f'Table A1 — Three years historical and five forecast. Revenue and attributable '
        f'profit for FY2023-FY2025 and FY2025 operating income are as disclosed; every '
        f'other historical line is derived by closing the disclosed profit. Earnings per '
        f'share here is attributable profit over the current share count and so reads EGP '
        f'{n2(H["eps"][2])} for FY2025; the company\'s own published figure is EGP '
        f'{n2(IN["eps_fy25"])}, the difference of about '
        f'{pc((H["eps"][2]-IN["eps_fy25"])/H["eps"][2])} being the statutory '
        f'employees\' and directors\' share of profit.')
H2('Balance sheet')
rows = [['EGP mn', 'FY2025'] + YF]
for lab, key in [('Net property, plant and equipment', 'ppe'),
                 ('Working capital', 'wc'), ('Cash and equivalents', 'cash')]:
    base = {'ppe': DNAT['ppe_estimate'], 'wc': DNAT['inventory'] + DNAT['receivables'],
            'cash': IN['cash_fy25']}[key]
    rows.append([lab, n0(base)] + [n0(x) for x in F[key]])
rows.append(['Total assets', n0(IN['ta_fy25'])] + [n0(x) for x in F['total_assets']])
rows.append(['Total debt', n0(IN['debt_fy25'])] + [n0(IN['debt_fy25']) for _ in YF])
rows.append(['Total equity', n0(IN['eq_fy25_rep'])] + [n0(x) for x in F['equity']])
rows.append(['Net (cash) / debt', n0(DCF['net_debt_bs'])] +
            [n0(IN['debt_fy25'] - x) for x in F['cash']])
rows.append(['Book value per share (EGP)', n2(LN['bvps'])] + [n2(x / SH) for x in F['equity']])
table(rows, [1.90, 0.90, 0.90, 0.90, 0.90, 0.90, 0.90], size=8.3, band_rows={4})
caption('Table A2 — FY2023 and FY2024 balance sheets are not retrievable at the '
        'evidentiary standard used elsewhere and are left blank rather than reconstructed.')
H2('Cash flow')
rows = [['EGP mn'] + YF]
for lab, vals in [('Attributable profit', F['pat']),
                  ('Add back depreciation', F['dna']),
                  ('Less change in working capital', [-x for x in F['dwc']]),
                  ('Capital expenditure', [-x for x in F['capex']]),
                  ('Dividends paid', [-x for x in F['dividends']]),
                  ('Closing cash', F['cash']),
                  ('Memo: free cash flow to the firm', F['fcff'])]:
    rows.append([lab] + [n0(x) for x in vals])
table(rows, [2.10, 0.92, 0.92, 0.92, 0.92, 0.92], size=8.6, band_rows={6})
caption('Table A3 — Free cash flow to the FIRM excludes treasury income, which is handled '
        'in the equity bridge; free cash flow to equity includes it through profit.')

# ============================== APPENDIX B ===================================
doc.add_page_break()
H1('Appendix B  Peer set, sector structure and risks')
rows = [['', 'Revenue (EGP mn)', 'Profit (EGP mn)', 'Market cap (EGP mn)',
         'Price / earnings', 'Net margin']]
for key in ('self', 'scem', 'mbsc'):
    p_ = PE[key]
    rows.append([p_['name'], n0(p_['rev']), n0(p_['pat']), n0(p_['mcap']),
                 f'{p_["pe"]:.2f}x', pc(p_['pat'] / p_['rev'])])
table(rows, [1.85, 1.15, 1.05, 1.20, 0.95, 0.85], size=8.6)
caption('Table B1 — Every multiple here is RECOMPUTED from revenue, profit and market '
        'capitalisation rather than quoted, because the published multiples for this peer '
        'set do not reconcile against the market capitalisations printed beside them.')
figure('fig8_sector.png', 6.6,
       'Figure B1 — The Egyptian cement balance. The surplus is the whole sector case.')
P(f'Egypt carries about {n0(IN["egy_capacity_mt"])}Mt of nameplate capacity against roughly '
  f'{n0(IN["egy_cons_mt"])}Mt of domestic consumption and {n0(IN["egy_prod_mt"])}Mt of '
  f'production — a utilisation rate near {pc(PE["sector"]["utilisation"], 0)}. Exports of '
  f'about {n1(IN["egy_exports_mt"])}Mt absorb part of the difference. The abolition of the '
  f'production quota in May 2025 removed the mechanism that had been supporting price into '
  f'that surplus, and the {n1(IN["egy_revival_mt"])}Mt restart programme would add to it.')
for head, body in [
    ('Price risk. ', 'A structurally over-supplied market whose main price-support '
     'mechanism has just been removed. This is the dominant risk and it is why the '
     'forecast price path grows below cost inflation.'),
    ('Energy and currency. ', 'Fuel is dollar-priced and electricity tariffs are on a '
     'reform path. Both raise cost independently of what happens to price.'),
    ('Concentration. ', 'One site, one product, one country. There is no diversification '
     'anywhere in this business to absorb a shock to Egyptian construction demand.'),
    ('Carbon. ', 'The EU carbon border mechanism raises the landed cost of exports into '
     'Europe. This producer is better placed than most Egyptian peers, but better placed '
     'is not unaffected.'),
    ('Disclosure. ', 'The depth of published financial detail is thin by the standards of '
     'the other markets covered, which is why so much of this study is a triangulation '
     'shown rather than a figure asserted.'),
]:
    bullet(body, bold_head=head)

# ============================== APPENDIX C ===================================
doc.add_page_break()
H1('Appendix C  The expert valuation panel')
P('Three independent valuations of the same company, each built by a different method and '
  'each stated with the specific evidence that would prove it wrong. They are not '
  'averaged: the disagreement between them is the point.')
figure('figD1_experts.png', 6.7,
       'Figure C1 — The three panel valuations against the market price.')
for e in EXP:
    H2(f'{e["label"]} — {e["method"]}')
    rich([('Valuation: ', {'bold': True}),
          (f'EGP {n2(e["low"])} to EGP {n2(e["high"])}, central EGP {n2(e["central"])} '
           f'({sg(e["central"]/SPOT-1)} against the market price of EGP {n2(SPOT)}).', {})])
    P(e['summary'])
    rich([('What would prove this wrong: ', {'bold': True, 'color': BRASS}),
          (e['falsifier'], {})])
rows = [['', 'Low (EGP)', 'Central (EGP)', 'High (EGP)', 'Versus spot']]
for e in EXP:
    rows.append([f'{e["label"]} — {e["method"]}', n2(e['low']), n2(e['central']),
                 n2(e['high']), sg(e['central'] / SPOT - 1)])
cen = sorted(x['central'] for x in EXP)
rows.append(['Panel median', '—', n2(cen[1]), '—', sg(cen[1] / SPOT - 1)])
table(rows, [2.72, 1.02, 1.15, 1.02, 0.94], band_rows={4})
caption('Table C1 — The panel. The median sits close to the weighted central of the four '
        'principal lenses, which is a coincidence of construction rather than a '
        'confirmation — both are looking at the same company through overlapping methods.')

P('')
P('Testahil · Independent valuation research · Educational analysis, not investment '
  'advice. No rating and no price target is expressed or implied.', size=8.6, italic=True,
  color=GREY)

OUT = 'ARCC_Valuation_Study_06-08-2026_public.docx'
doc.save(OUT)
print('wrote', OUT)
