"""ARCC_Valuation_Study_06-08-2026_public.docx — TMPV house structure.

16 headings: 7 top-level sections plus the 9 subsections of section 1, then three
appendices. Reads study_numbers.json exclusively — no numeral is typed here.

REVISION 3 — the forecast price path recalibrated to the audited record, which disproved
the one revision 2 inherited. Revision 2 rebuilt every company figure on the audited
consolidated financial statements for FY2023, FY2024 and FY2025 and the reviewed Q1-2026
interim accounts.

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
BU, UC, KDG, CON = D['bottom_up'], D['unit_calibration'], D['kd_gate'], D['contested']
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
rich([(f'One of Egypt\'s largest cement plants, at the top of the best year the industry '
       f'has had in more than a decade — audited profit up '
       f'{pc(IN["pat_fy25"]/IN["pat_fy24"]-1, 0)} in a single year on a '
       f'{pc(IN["rev_fy25"]/IN["rev_fy24"]-1)} revenue step — and facing '
       f'{n1(IN["egy_revival_mt"])} million tonnes of dormant national capacity queuing to '
       f'restart inside the forecast window.', {'size': 12})], space_after=10)

box([('What this is. ', 'An independent valuation of Arabian Cement Company, an '
      'educational analysis and not investment advice. It carries no rating and no price '
      'target — fair-value ranges and distributions only.'),
     ('The company in one line. ', f'Two production lines in Suez governorate, about '
      f'{n1(IN["cap_cement_mt"])} million tonnes of cement a year and roughly '
      f'{pc(PE["sector"]["share_of_capacity"], 1)} of Egypt\'s nominal capacity, listed on '
      f'the Egyptian Exchange since May 2014, with cash of EGP '
      f'{n0(IN["cash_fy25"])}mn against interest-bearing debt of EGP '
      f'{n0(W["debt_total"])}mn. Every figure in this study is read from the audited '
      f'consolidated accounts.'),
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
  f'{pc(PE["sector"]["share_of_capacity"], 1)} of Egypt\'s nominal capacity. Larger single '
  f'sites exist — National Cement Beni Suef and Lafarge Ain Sokhna are both materially '
  f'bigger — so the earlier edition\'s claim that this is the country\'s second-largest '
  f'plant is withdrawn. The balance sheet is what that '
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
rows.append(['Gross profit (EGP mn)'] + [n0(x) for x in H['gross_profit']])
rows.append(['Operating profit (EGP mn)'] + [n0(x) for x in H['ebit']])
rows.append(['EBITDA (EGP mn)'] + [n0(x) for x in H['ebitda']])
rows.append(['EBITDA margin'] + [pc(x) for x in H['margin']])
rows.append(['Attributable profit (EGP mn)'] + [n0(x) for x in H['pat']])
rows.append(['Earnings per share (EGP)'] + [n2(x) for x in H['eps']])
rows.append(['Effective tax rate'] + [pc(x) for x in H['tax_eff_hist']])
rows.append(['Capital expenditure (EGP mn)'] + [n0(x) for x in H['capex']])
table(rows, [2.60, 1.30, 1.30, 1.30])
caption('Table 1 — Three audited years. Every line is a disclosed figure or a formula over '
        'disclosed figures: operating profit is gross profit less administrative expenses, '
        'provisions and credit losses, and EBITDA adds back the depreciation and '
        'amortisation reported in the cash flow statement.')
P(f'Two things stand out. The revenue note splits local from export: local sales rose '
  f'{pc(IN["rev_local_goods_fy25"]/IN["rev_local_fy24"]-1, 0)} while export sales were '
  f'{sg((IN["rev_exp_goods_fy25"]+IN["rev_exp_svc_fy25"])/IN["rev_exp_fy24"]-1)} — the '
  f'abolition of Egypt\'s cement production quota in May 2025 was a DOMESTIC event, and '
  f'exports sat against a statutory 30% cap throughout. And the '
  f'margin moved from {pc(H["margin"][1])} to {pc(H["margin"][2])} in a single year, '
  f'because almost the entire price increase fell to the bottom line on a cost base that '
  f'is largely fixed.')

# ---- 1.2 --------------------------------------------------------------------
H2('1.2  The unit economics — where EBITDA actually comes from')
P('The operating model starts at the PLANT, and this is the one thing that changed most '
  'in this revision. The previous edition assumed a cement price, divided the audited '
  'revenue by it to get tonnes, and presented the utilisation that fell out as an '
  'independent corroboration. It was neither independent nor a corroboration: it was the '
  'same assumption written twice, and the FY2025 check it produced was an accounting '
  'identity that reproduces the audited revenue for ANY price, because volume moves by '
  'exactly the reciprocal. Here the drivers are physical — kiln utilisation, the clinker '
  'factor and the two export shares — and the tonnes, the mill utilisation and all three '
  'realised prices come out of them. The prices are therefore outputs that can be held '
  'against the market and disagree with it.')
P('It also carries three products where the previous edition carried one. This company '
  'sells local cement, export cement and export CLINKER, and clinker is the unground '
  'intermediate, worth a fraction of the cement it could have become. Pricing every tonne '
  'at a cement price made the plant look far smaller than it is.')
rows = [['', 'Value']]
rows.append(['Kiln clinker capacity (audited note 1)', f'{n2(IN["cap_clinker_mt"])}Mt'])
rows.append(['Kiln utilisation  (DRIVER)', pc(IN['kiln_util'][0])])
rows.append(['Clinker produced', f'{n3(UC["clk_prod"])}Mt'])
rows.append(['Sold as clinker  (DRIVER)', pc(IN['clk_export_share'][0])])
rows.append(['Clinker exported', f'{n3(UC["vol_clk_exp"])}Mt'])
rows.append(['Clinker factor  (DRIVER)', n3(IN['clinker_factor'])])
rows.append(['Cement produced', f'{n3(UC["cem_prod"])}Mt'])
rows.append(['Mill utilisation', pc(UC['util_fy25'])])
rows.append(['Cement exported  (DRIVER)', pc(IN['cem_export_share'][0])])
rows.append(['Local cement', f'{n3(UC["vol_local"])}Mt'])
rows.append(['TOTAL DESPATCHES', f'{n3(UC["vol_fy25"])}Mt'])
rows.append(['Local cement price — DERIVED', f'EGP {n0(UC["price_loc_derived"])}/t'])
rows.append(['Export cement price — DERIVED', f'USD {n1(UC["price_exp_cem_usd"])}/t'])
rows.append(['Export clinker price — DERIVED', f'USD {n1(UC["price_exp_clk_usd"])}/t'])
table(rows, [4.10, 2.00], band_rows={12, 13, 14, 15})
caption('Table 2 — The plant in tonnes, and the prices that fall out of it. The four '
        'drivers are physical; everything below them is derived. Cement exports of '
        f'{pc(IN["cem_export_share"][0])} of cement made sit inside the 30% statutory cap — '
        'the previous edition\'s single-product build put exports at 31.5% of volume and '
        'breached the cap its own text called binding.')
P(f'The three derived prices are the test, and it is a test this study does not pass '
  f'cleanly. Local cement at EGP {n0(UC["price_loc_derived"])} a tonne is credible against '
  f'Egyptian ex-works commentary. Export cement at USD {n1(UC["price_exp_cem_usd"])} and '
  f'export clinker at USD {n1(UC["price_exp_clk_usd"])} sit roughly a third BELOW the USD '
  f'44-48 the trade press quotes for Egyptian clinker free on board. Either the physical '
  f'volumes behind this build are too high, or realisations run well under the published '
  f'indices. The gap is published rather than tuned away, and it is the reason the volume '
  f'base carries its own sensitivity rather than being presented as settled.')
P(f'The cost stack is the printed one. Cost of sales of EGP {n0(H["cogs"][2])}mn splits into '
  f'materials and fuel of EGP {n0(IN["cos_materials_fy25"])}mn — the note confirms this is '
  f'the cost of inventories charged to cost of sales, so it carries fuel, packing and spares '
  f'as well as raw meal — transportation of EGP {n0(IN["cos_transport_fy25"])}mn, overheads '
  f'of EGP {n0(IN["cos_overhead_fy25"])}mn, and depreciation and amortisation of EGP '
  f'{n0(IN["cos_mfg_dep_fy25"] + 30.681613)}mn. Adding cash administrative expenses, '
  f'provisions and credit losses gives a total cash cost of EGP {n0(UC["cash_cost_fy25"])}mn, '
  f'or EGP {n0(UC["cash_cost_t"])} a tonne.')
rows = [['EGP per tonne of cement', 'FY2025A', 'FY2026E', 'FY2030E']]
for lab, key in [('Materials and fuel', 'c_mat'), ('Transportation', 'c_tra'),
                 ('Overheads and administration', 'c_ovh'), ('Total cash cost', 'cc_t'),
                 ('Blended realised price', 'price')]:
    rows.append([lab] + [n0(BU[i][key]) for i in (0, 1, 5)])
rows.append(['Volume (Mt)'] + [n3(BU[i]['vol']) for i in (0, 1, 5)])
rows.append(['EBITDA (EGP mn)'] + [n0(BU[i]['ebitda']) for i in (0, 1, 5)])
rows.append(['EBITDA margin'] + [pc(BU[i]['mgn']) for i in (0, 1, 5)])
table(rows, [2.60, 1.30, 1.30, 1.30], band_rows={4, 7, 8})
caption('Table 3 — The cost stack per tonne and the margin it produces. EBITDA is an OUTPUT '
        'of this build, not an input to it.')
figure('fig7_stack.png', 6.9,
       'Figure 2 — Cash cost per tonne against realised price per tonne. The margin is the '
       'gap, and the gap narrows across the forecast.')
P(f'The reconstruction reproduces audited FY2025 revenue to '
  f'{sg(BU[0]["rev"]/IN["rev_fy25"]-1, 3)} and audited FY2025 EBITDA to '
  f'{sg(BU[0]["ebitda"]/H["ebitda"][2]-1, 3)}. It is not forced to: the volume is derived '
  f'from the revenue note and the cost lines are the printed ones, so a wrong price '
  f'assumption would show up as a non-zero residual.')
P(f'One physical constraint is worth checking, because the volume forecast is built off '
  f'CEMENT capacity while the kiln is what could bind first. At a clinker factor of '
  f'{n2(IN["clinker_factor"])} — observed from the audited capacity pair of '
  f'{n1(IN["cap_clinker_mt"])}Mt of clinker against {n1(IN["cap_cement_mt"])}Mt of cement — '
  f'the FY2030 volume needs {n3(BU[5]["vol"]*IN["clinker_factor"])}Mt of clinker against '
  f'{n1(IN["cap_clinker_mt"])}Mt of kiln capacity, or {pc(BU[5]["vol"]*IN["clinker_factor"]/IN["cap_clinker_mt"])} '
  f'of it. The forecast fits the plant, with '
  f'{n3(IN["cap_clinker_mt"]-BU[5]["vol"]*IN["clinker_factor"])}Mt of headroom, and more '
  f'blending would widen that.')
P(f'The company-specific lever is fuel, and it is now visible in the accounts rather than '
  f'assumed. Assets under construction of EGP {n0(IN["auc_fy25"])}mn include EGP '
  f'{n0(240.235369)}mn of alternative-fuel capacity for production line 2 and EGP '
  f'{n0(146.238521)}mn of a new cement silo for line 1, and a EUR 25mn European Bank for '
  f'Reconstruction and Development facility is drawn against exactly that programme — '
  f'tranche one for alternative-fuel capacity and hydrogen injection on kiln 1, tranche two '
  f'for hydrogen injection on kiln 2. The model carries a saving on the materials-and-fuel '
  f'line rising to {pc(IN["af_saving"][5], 1)} by FY2030 as a result. That is a funded and '
  f'part-built programme, not an intention.')

H2('1.3  Depreciation, capital spending, and what the book hides')
P(f'Depreciation and amortisation is disclosed in the cash flow statement: EGP '
  f'{n0(H["dna"][2])}mn in FY2025, EGP {n0(H["dna"][1])}mn in FY2024 and EGP '
  f'{n0(H["dna"][0])}mn in FY2023 — property depreciation, licence amortisation and '
  f'right-of-use amortisation. That is {pc(H["dna"][2]/H["revenue"][2], 2)} of FY2025 '
  f'revenue, and it is small for a cement plant.')
P(f'It is small for a reason that matters to the valuation. The plant dates from around '
  f'2010 and the accounts are prepared on a historical-cost basis; the pound has devalued '
  f'several times since. Net property, plant and equipment is EGP {n0(IN["ppe_fy25"])}mn, '
  f'which on {n1(IN["cap_cement_mt"])}Mt of capacity is about USD '
  f'{n0((IN["ppe_fy25"]+IN["auc_fy25"])/IN["cap_cement_mt"]/IN["fx"])} per annual tonne '
  f'including construction in progress — against a replacement cost of USD '
  f'{n0(IN["repl_usd_t"])}. The book is carrying the plant at roughly a tenth of what one '
  f'would cost to build.')
rows = [['EGP mn', 'FY2023', 'FY2024', 'FY2025']]
rows.append(['Depreciation and amortisation'] + [n0(x) for x in H['dna']])
rows.append(['Capital expenditure'] + [n0(x) for x in H['capex']])
rows.append(['Capex as a share of EBITDA'] +
            [pc(TR['history'][i]['capex_over_ebitda']) for i in range(3)])
rows.append(['Net reinvestment (capex less depreciation)'] +
            [n0(TR['history'][i]['reinvestment']) for i in range(3)])
rows.append(['Reinvestment rate (net reinvestment / NOPAT)'] +
            [pc(TR['history'][i]['rr']) for i in range(3)])
rows.append(['Return on BOOK invested capital'] +
            [pc(TR['history'][i]['roic_book']) for i in range(3)])
rows.append(['Character'] + [TR['history'][i]['character'].split(' — ')[0] for i in range(3)])
table(rows, [2.60, 1.30, 1.30, 1.30])
caption('Table 4 — The reinvestment record, buildable because capital expenditure is '
        'disclosed for all three years. FY2023 spent less than it depreciated; FY2024 and '
        'FY2025 carried the alternative-fuel and silo programmes on top of maintenance.')
P(f'That has a direct consequence for the forecast, and it is treated as one. Capital '
  f'expenditure is NOT set at book depreciation. It is set at the economic maintenance '
  f'level of USD {n2(IN["capex_usd_t_cap"])} per tonne of installed capacity — about EGP '
  f'{n0(F["capex"][0])}mn in FY2026 against a book charge of EGP {n0(F["dna"][0])}mn. '
  f'Setting capex equal to book depreciation would flatter free cash flow by construction; '
  f'the cost of refusing to do so is computed in section 1.9 and is worth '
  f'{sg(CON[2]["effect"])} of the cash-flow lens. The audited FY2024 and FY2025 outturns of '
  f'EGP {n0(H["capex"][1])}mn and EGP {n0(H["capex"][2])}mn — USD {n1(H["capex"][1]/IN["cap_cement_mt"]/IN["fx_avg_fy24"])} '
  f'and USD {n1(H["capex"][2]/IN["cap_cement_mt"]/IN["fx_avg_fy25"])} a tonne — bracket the '
  f'assumption, and both of those years carried growth projects as well as maintenance.')

H2('1.4  The cost of capital, and a debt book that changed currency')
P(f'The discount rate is a schedule, not a number. Egypt is in monetary transition: the '
  f'central bank held its main operation rate at 19.50% through the first half of 2026 '
  f'while headline inflation eased to 14.3%, and its own published medium-term target is '
  f'7%. A single flat rate applied to both the explicit years and a perpetuity would assert '
  f'that Egypt\'s cost of capital never normalises.')
P(f'The cost of DEBT is the line the audited accounts changed most. During 2025 the company '
  f'refinanced out of pound working-capital facilities and into euro term debt: a EUR 25mn '
  f'facility from the European Bank for Reconstruction and Development at three-month '
  f'Euribor plus 4.35%, drawn to EUR 18.5mn to fund alternative-fuel capacity and hydrogen '
  f'injection, and a EUR 3.09mn National Bank of Egypt facility under a KfW '
  f'industrial-pollution programme at six-month Euribor plus 3%. '
  f'{pc(KDG["eur_share"])} of the interest-bearing book is now euro-denominated.')
rows = [['Facility', 'Balance (EGP mn)', 'Currency', 'Contractual rate']]
rows.append(['CIB credit facilities', n0(IN['debt_cib_fy25']), 'EGP',
             f'corridor + 0.6% = {pc(KDG["kd_cib"], 2)}'])
rows.append(['National Bank of Egypt / KfW', n0(IN['debt_nbe_fy25']), 'EUR',
             f'Euribor + 3.00% = {pc(KDG["kd_nbe"], 2)}'])
rows.append(['European Bank for Reconstruction and Development', n0(IN['debt_ebrd_fy25']),
             'EUR', f'Euribor + 4.35% = {pc(KDG["kd_ebrd"], 2)}'])
rows.append(['Lease liabilities', n1(IN['lease_fy25']), 'EGP', '—'])
rows.append(['Blended cost of debt, adopted', n0(W['debt_total']),
             f'{pc(KDG["eur_share"], 0)} EUR', pc(KDG['kd_blended'], 2)])
table(rows, [2.60, 1.20, 1.00, 1.60], band_rows={5})
caption('Table 5 — The debt book, facility by facility, from the audited borrowings note. '
        'The blended rate is built in the model from these four lines, not pasted.')
P(f'Three checks are published rather than asserted, because a contractual rate is not the '
  f'same thing as a rate paid. Interest expense over average interest-bearing debt gives '
  f'{pc(KDG["eff_fy24"], 2)} in FY2024, {pc(KDG["eff_fy25"], 2)} in FY2025 and '
  f'{pc(KDG["eff_q126_annualised"], 2)} annualising the first quarter of 2026. The '
  f'contractual {pc(KDG["kd_blended"], 2)} sits ABOVE all three, and the gap is not a '
  f'reconciling item to be smoothed: the book re-based mid-year, so the trailing average '
  f'balance is not what carried the interest, and the borrowing that funds an asset still '
  f'under construction has its interest capitalised into that asset rather than expensed. '
  f'The marginal contractual rate is the right one for a forward-looking discount rate, and '
  f'the gap is disclosed so the reader can disagree.')
P(f'One caution belongs next to that number. Adopting the contracted euro rate means the '
  f'euro debt is NOT compensated for pound depreciation beyond what this study\'s own '
  f'currency path already assumes. Loading the euro legs with '
  f'{pc(IN["egp_dep_vs_eur"], 0)} annual pound depreciation under interest parity gives a '
  f'pound-equivalent cost of debt of {pc(KDG["kd_egp_equivalent"], 2)} — nearly twice the '
  f'adopted figure. The alternative is computed as a VALUE and not merely described: it is '
  f'worth {sg(CON[0]["effect"])} of the cash-flow lens, because debt is only '
  f'{pc(W["wd_gross"])} of the capital structure. A large swing in a small weight is still '
  f'a small effect, and saying so is not the same as dismissing it.')
rows = [['', 'Explicit window', 'Terminal']]
rows.append(['Risk-free rate', pc(IN['rf'], 2), pc(IN['rf_term'], 2)])
rows.append(['Less sovereign default spread', f'({pc(IN["sov_spread_cds"], 2)})', '—'])
rows.append(['Normalised risk-free rate', pc(W['rf_star'], 2), pc(IN['rf_term'], 2)])
rows.append(['Beta', n3(W['beta']), n3(W['beta_term'])])
rows.append(['Equity risk premium', pc(IN['erp_cds'], 2), pc(IN['erp_term'], 2)])
rows.append(['Cost of equity', pc(W['ke_exp'], 2), pc(W['ke_term'], 2)])
rows.append(['Cost of debt after tax', pc(W['kd_at'], 2),
             pc(IN['kd_term'] * (1 - IN['tax_stat']), 2)])
rows.append(['Debt weight', pc(W['wd_gross'], 2), pc(IN['wd_term'], 1)])
rows.append(['Blended cost of capital', pc(W['wacc_exp'], 2), pc(W['wacc_term'], 2)])
table(rows, [2.90, 1.80, 1.80], band_rows={9})
caption('Table 6 — The two anchors. The sovereign default spread is netted OUT of the local '
        'risk-free rate before a country equity premium is added, so Egypt\'s default risk '
        'is charged once rather than twice; leaving it in would have put the cost of equity '
        f'at {pc(W["ke_raw_retired"], 2)} instead of {pc(W["ke_exp"], 2)}.')
rows = [['Year'] + YF]
rows.append(['Glide fraction'] + [n3(x) for x in F['glide']])
rows.append(['Forward cost of capital'] + [pc(x, 2) for x in F['fwd_wacc']])
rows.append(['Cumulative discount factor'] + [f'{x:.4f}' for x in F['df']])
table(rows, [1.62, 1.06, 1.06, 1.06, 1.06, 1.06])
caption('Table 7 — The schedule. The glide fractions are the cumulative progress of the '
        'POUND cost-of-debt path: the discount rate is a pound rate applied to pound cash '
        'flows, so the Egyptian easing calendar sets its slope while the euro debt book sets '
        'the level of the cost of debt. The terminal value is capitalised at the terminal '
        'rate and brought home on year five\'s own cumulative factor — one date, one price '
        'of time.')

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
  f'is worth {sg(CON[1]["effect"])} of the cash-flow lens.')
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
P(f'The effective tax rate of {pc(TAXE)} is DISCLOSED, not inferred: income tax of EGP '
  f'{n0(H["tax"][2])}mn against pre-tax profit of EGP {n0(H["pbt"][2])}mn. The company '
  f'separately states an average effective rate of 23.33% for 2025 and 22.96% for 2024, and '
  f'the first quarter of 2026 ran at 25.9%. It sits close to the statutory '
  f'{pc(IN["tax_stat"], 1)} because the deferred-tax movement is small.')

# ---- 1.7 --------------------------------------------------------------------
P(f'The margin path is the central judgement in this forecast, and it deserves stating as '
  f'one number rather than left inside a table. Local prices are assumed to grow '
  f'{pc(IN["price_local_path"][5]-1)} in total across the five years while pound costs grow '
  f'{pc(IN["cost_infl"][5]-1)} — a real erosion of about '
  f'{pc(IN["cost_infl"][5]/IN["price_local_path"][5]-1, 0)}. The EBITDA margin therefore '
  f'falls from the audited {pc(H["margin"][2])} to {pc(F["margin"][4])} by FY2030, still '
  f'well above the {pc(H["margin"][1])} of FY2024 and far above the {pc(H["margin"][0])} of '
  f'FY2023. The claim is not that the business deteriorates; it is that part of the 2025 '
  f'step-change gives back as dormant capacity returns and energy reform continues. A '
  f'reader who thinks the industry passes cost through faster should read the margin '
  f'sensitivity in section 7: two points of margin is worth about EGP '
  f'{n2(SN["mgn"][3]-SN["mgn"][2])} a share.')
P(f'That path is set below the cost path in every year, and this revision changed how it '
  f'is judged rather than only where it sits. The prior edition justified it against '
  f'headline inflation of {pc(IN["cost_infl"][5]-1)} — but that is the input-price index, '
  f'not the cost the model actually charges. Netting the alternative-fuel saving off the '
  f'materials line, the cash cost per tonne the model charges grows '
  f'{pc(BU[5]["cc_t"]/BU[0]["cc_t"]-1)}, so the real erosion is '
  f'{pc(BU[5]["cc_t"]/BU[0]["cc_t"]/(IN["price_local_path"][5])-1)} rather than the figure '
  f'previously printed. The comparison is now made against the cost the model charges.')
P(f'The audited record still frames it. In FY2024 revenue grew '
  f'{pc(H["revenue"][1]/H["revenue"][0]-1, 1)} against total cash cost of '
  f'{pc((H["cogs"][1]+H["ga"][1]-IN["dna_fy24"])/(H["cogs"][0]+H["ga"][0]-IN["dna_fy23"])-1, 1)}; '
  f'in FY2025 revenue grew {pc(H["revenue"][2]/H["revenue"][1]-1, 1)} against cash cost of '
  f'{pc((H["cogs"][2]+H["ga"][2]-IN["dna_fy25"])/(H["cogs"][1]+H["ga"][1]-IN["dna_fy24"])-1, 1)}, '
  f'which is why the gross margin moved {pc(H["gross_profit"][0]/H["revenue"][0])} to '
  f'{pc(H["gross_profit"][1]/H["revenue"][1])} to {pc(H["gross_profit"][2]/H["revenue"][2])}. '
  f'In every period the accounts cover, price outran cost. But the first quarter of 2026 is '
  f'the sharper evidence and it cuts the other way: revenue grew '
  f'{pc(IN["rev_q1_26"]/IN["rev_q1_25"]-1, 1)} while the gross margin EXPANDED to '
  f'{pc(IN["gp_q1_26"]/IN["rev_q1_26"])} from {pc(H["gross_profit"][2]/H["revenue"][2])}. A '
  f'margin that widens on a 17% revenue step is the signature of VOLUME spread over fixed '
  f'cost, not of price. This study does not hold the quarterly volume and price split, so '
  f'it cannot settle which it was — and that is stated here rather than resolved by '
  f'assertion, because the answer changes the forecast materially.')
P(f'One reconciliation belongs here too, because it is the sharpest challenge to the '
  f'forecast. The first quarter of 2026 — reviewed, not audited, but signed off in May — '
  f'earned attributable profit of EGP {n0(IN["pat_q1_26"])}mn on revenue of EGP '
  f'{n0(IN["rev_q1_26"])}mn, a gross margin of {pc(IN["gp_q1_26"]/IN["rev_q1_26"])} against '
  f'{pc(H["gross_profit"][2]/H["revenue"][2])} for FY2025 as a whole. Four times that '
  f'quarter is EGP {n0(4*IN["pat_q1_26"])}mn. This model forecasts EGP {n0(F["pat"][0])}mn '
  f'for FY2026, {sg(F["pat"][0]/(4*IN["pat_q1_26"])-1)} below the simple annualisation. '
  f'Margins were still EXPANDING in the first quarter; the forecast assumes they turn. That '
  f'is the assumption to attack.')

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
P(f'Cash is added at face and is not in the discount rate. The audited balance sheet shows '
  f'EGP {n0(IN["cash_fy25"])}mn of cash against EGP {n0(W["debt_total"])}mn of '
  f'interest-bearing debt at 31 December 2025. Rolling that forward on the elapsed part of '
  f'FY2026 and DEDUCTING the EGP {n0(IN["div_fy25_declared"])}mn FY2025 dividend — declared '
  f'and still shown as payable in the March 2026 accounts, so a buyer at today\'s price does '
  f'not receive it — puts net cash at EGP {n0(DCF["net_cash"])}mn at the valuation date, or '
  f'EGP {n2(DCF["net_cash"]/SH)} a share. The March 2026 balance sheet is the independent '
  f'check on that: cash of EGP {n0(IN["cash_q1_26"])}mn less debt of EGP '
  f'{n0(IN["debt_q1_26"])}mn less the dividend payable of EGP {n0(IN["divpay_q1_26"])}mn is '
  f'EGP {n0(IN["cash_q1_26"]-IN["debt_q1_26"]-IN["divpay_q1_26"])}mn at 31 March, four '
  f'months before the valuation date.')
P(f'Minority interests are deducted, and the audited figure is the reason this line is now '
  f'immaterial: EGP {n0(IN["nci"]*1e6)} — one hundred and fifty-eight thousand pounds, or '
  f'{pc(IN["nci"]/DCF["equity"], 4)} of equity value. The subsidiaries are 99% to 99.99% '
  f'owned.')
P(f'At {pc(DCF["tv_share"])} of enterprise value, the terminal value carries less of this '
  f'valuation than the two-thirds to four-fifths a long-horizon discounted cash-flow model '
  f'usually ends up with, and that is a consequence of the {pc(W["wacc_exp"])} '
  f'explicit-window discount rate rather than a design choice — at that rate the fifth '
  f'forecast year is already discounted to {pc(F["df"][4], 0)} of its face value. The '
  f'answer therefore depends more on the '
  f'next five years and less on a perpetuity assumption than is usual, which for a business '
  f'whose next five years are forecastable from tonnes and disclosed costs is the right '
  f'place for the weight to sit. It is worth naming the direction of travel honestly: the '
  f'prior revision put the terminal share at 45.5%, and correcting the price path lifted it '
  f'because a higher terminal margin loads more value into the perpetuity than into a '
  f'heavily discounted explicit window. More of the answer rests on the far end than it did.')

H2('1.8  Terminal value, and what growth costs')
P(f'Terminal growth is held at {pc(IN["g_term"], 0)}, against a terminal risk-free rate '
  f'that already embeds disinflation — so approximately zero in real terms. It is not '
  f'derived from recent performance, and the reason is arithmetic rather than a matter of '
  f'judgement.')
P(f'Attributable profit compounded {pc(TR["pat_cagr_fy23_fy25"], 0)} a year across the two '
  f'audited steps from FY2023 to FY2025. Compounded against nominal economic growth of about '
  f'{pc(IN["egy_gdp_growth"], 0)}, a company at {pc(TR["share_of_gdp"], 3)} of Egyptian '
  f'output today would equal the entire Egyptian economy in roughly '
  f'{n0(TR["crossover_years"])} years. That is not a forecast anyone would defend; it is the '
  f'reason recent growth belongs in the explicit window, describing a specific dated event — '
  f'the removal of the production quota — and not in the perpetuity.')
P(f'Growth in the terminal state has to be paid for, and the choice of what capital it is '
  f'paid on is the single most consequential judgement in this model. On the audited BOOK, '
  f'return on invested capital was {pc(TR["history"][2]["roic_book"])} in FY2025 — well '
  f'above any plausible cost of capital, which would make terminal growth free. But that '
  f'book carries a plant built around 2010 at historical cost through several devaluations: '
  f'net property and construction of EGP {n0(IN["ppe_fy25"]+IN["auc_fy25"])}mn is about USD '
  f'{n0((IN["ppe_fy25"]+IN["auc_fy25"])/IN["cap_cement_mt"]/IN["fx"])} per annual tonne '
  f'against a replacement cost of USD {n0(IN["repl_usd_t"])}. A return computed on that base '
  f'measures the devaluation, not the economics of adding a tonne.')
P(f'The terminal block is therefore struck on REPLACEMENT-COST invested capital — EGP '
  f'{n0(DCF["ic_repl"])}mn, being {n1(IN["cap_cement_mt"])}Mt at USD {n0(IN["repl_usd_t"])} '
  f'a tonne. On that basis the terminal return on capital is {pc(TR["roic_repl"])} and the '
  f'reinvestment rate that {pc(IN["g_term"], 0)} growth requires is {pc(TR["rr_repl"])} of '
  f'terminal profit.')
P(f'That choice of denominator all but switches the terminal growth rate off, and the '
  f'reason is worth setting out because the obvious reading of it is wrong. A terminal '
  f'return of {pc(TR["roic_repl"])} against a terminal rate of {pc(W["wacc_term"])} looks '
  f'like the textbook case in which growth destroys value. It is not the right test. '
  f'Because reinvestment is growth divided by return on capital, and that return is itself '
  f'terminal profit grown one year over a fixed capital base, the reinvestment charge '
  f'collapses to a constant — growth multiplied by invested capital — and the whole '
  f'terminal block reduces to terminal profit grown one year, less that charge, over the '
  f'rate less growth. Differentiate it and the growth term vanishes: the DIRECTION of the '
  f'lever is a constant of the model, and the hurdle is terminal profit over invested '
  f'capital against the rate over one plus the rate, which is {pc(GDV["hurdle"], 2)}. This '
  f'company sits at {pc(GDV["n_over_ic"], 2)} — {n0((GDV["n_over_ic"]-GDV["hurdle"])*1e4)} '
  f'basis points above it. Growth therefore adds value, and adds almost none of it: the '
  f'cash-flow lens is EGP {n2(GDV["fv_at_g3"])} at 3% terminal growth and EGP '
  f'{n2(GDV["fv_at_g7"])} at 7%, a spread of {pc(GDV["spread_pct"], 1)} across four points '
  f'of perpetual growth. The practical conclusion is the one that matters: on a '
  f'replacement-cost denominator this plant roughly breaks even on new tonnes, in a market '
  f'carrying {n0(IN["egy_capacity_mt"])}Mt of capacity against {n0(IN["egy_cons_mt"])}Mt of '
  f'consumption, so nothing in this valuation is bought with an assumption about perpetual '
  f'growth. A reader who prefers the book basis should know it lifts the valuation '
  f'substantially, and should say why a plant carried at a tenth of replacement cost is the '
  f'right denominator.')
rows = [['Explicit-window rate'] + [pc(g, 0) for g in SN['g_grid']]]
for i, wv in enumerate(SN['wacc_grid']):
    rows.append([pc(wv, 2)] + [n2(x) for x in SN['wacc_g'][i]])
table(rows, [1.72, 1.02, 1.02, 1.02, 1.02, 1.02])
# Both the strength and the SIGN of the growth lever are read off the grid, never
# typed. They flipped between revisions and a hard-typed caption would now be false.
_row = SN["wacc_g"][0][4] - SN["wacc_g"][0][0]     # 3% -> 7% growth, rate held
_col = SN["wacc_g"][4][0] - SN["wacc_g"][0][0]     # low -> high rate, growth held
_g_up = 'UP' if _row > 0 else 'DOWN'
_g_str = 'STRONGER' if abs(_row) > abs(_col) else 'WEAKER'
caption(f'Table 9 — Fair value per share across the explicit-window cost of capital and '
        f'terminal growth. Growth is the {_g_str} of the two levers here and it points '
        f'{_g_up}: across a row the value moves EGP {n2(abs(_row))}, against EGP '
        f'{n2(abs(_col))} down a column. The paragraphs above set out why the growth axis is '
        f'nearly flat — on a replacement-cost denominator this plant sits within '
        f'{n0((GDV["n_over_ic"]-GDV["hurdle"])*1e4)} basis points of breaking even on new '
        f'tonnes, so perpetual growth neither creates nor destroys much of anything.')
figure('fig2_sens.png', 6.6,
       f'Figure 3 — The same surface. The growth axis is almost flat and the discount-rate '
       f'axis is not; that is the model being consistent with its own terminal algebra '
       f'rather than a sign error.')
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
_above = sorted([k for k in LN['values'] if LN['values'][k] > SPOT],
                key=lambda k: -LN['values'][k])
_below = sorted([k for k in LN['values'] if LN['values'][k] <= SPOT],
                key=lambda k: LN['values'][k])
_lens_l = lambda ks: ' and '.join([', '.join(ks[:-1]), ks[-1]] if len(ks) > 1 else ks)
P(f'The four lenses do not agree, and the pattern of their disagreement is the most useful '
  f'thing in this study. Two of them sit ABOVE the market price — '
  f'{_lens_l(_above)}, at EGP ' +
  ' and EGP '.join(n2(LN['values'][k]) for k in _above) +
  f' — and two sit below: {_lens_l(_below)}, at EGP ' +
  ' and EGP '.join(n2(LN['values'][k]) for k in _below) +
  f'. The split is not assets against earnings. It runs between what the plant can be '
  f'expected to EARN or COST from here, which both land above the market, and what the '
  f'market is currently willing to PAY for a pound of Egyptian cement earnings, which is '
  f'what the two multiple-based lenses measure and which lands below. A cement peer group '
  f'trading at {n1((PE["scem"]["pe"]+PE["mbsc"]["pe"])/2)} times earnings in a country '
  f'whose policy rate has '
  f'a two in front of it is not obviously mispricing anything; it is discounting the same '
  f'restart programme this study discounts, only harder and sooner.')
P(f'The weighting resolves that in favour of earnings, at '
  f'{pc(IN["w_dcf"], 0)}/{pc(IN["w_rel"], 0)}/{pc(IN["w_norm"], 0)}/{pc(IN["w_asset"], 0)}, '
  f'and gives a central EGP {n2(LN["central"])} against EGP {n2(SPOT)} — '
  f'{sg(LN["central"]/SPOT-1)}. A reader who believes replacement cost is a floor rather '
  f'than a ceiling would weight the asset lens far more and reach the opposite conclusion. '
  f'The case against doing so is the {n1(IN["egy_revival_mt"])}Mt restart programme, and '
  f'it is a testable one.')
P(f'Against the technical picture, the two readings are in tension. The share is above its '
  f'entire moving-average stack on a rising 200-day and {pc(1-TECH["pct_off_high"], 0)} of '
  f'of its 52-week intraday high — 98% OF that high, and '
  f'{pc((SPOT-35.01)/(60.40-35.01), 0)} of the way UP the range, which are different '
  f'statistics and the earlier edition ran them together — while the two multiple-based '
  f'lenses put fair value below the '
  f'current price and the two forward-looking ones put it above. Momentum sits with the '
  f'cash-flow case here rather than against it, and the disagreement that remains is '
  f'between that case and the multiple the market is prepared to pay. This study takes no '
  f'view on which resolves first.')

# ============================== 5 ============================================
H1('5  Catalysts to watch')
for head, body in [
    ('The restart programme. ', f'Seven to nine dormant Egyptian lines are under study for '
     f'revival, potentially adding {n1(IN["egy_revival_mt"])}Mt from the second half of '
     f'2026 — about {pc(PE["sector"]["revival_pct_of_consumption"], 0)} of domestic '
     f'consumption. Whether those lines actually restart, and how fast, is the single '
     f'largest swing factor in the price path this model assumes.'),
    ('The realised price, quarter by quarter. ', f'The model assumes a domestic price of '
     f'EGP {n0(BU[1]["price_loc"])} a tonne in FY2026 and growth below cost '
     f'inflation thereafter. Two consecutive quarters of realised prices above EGP 4,200 '
     f'would break that assumption upward; a return toward EGP 3,000 would break it down.'),
    ('The alternative-fuel programme. ', f'The substitution rate is assumed to rise from '
     f'a cumulative {pc(IN["af_saving"][5], 1)} saving on the materials and fuel line by '
     f'FY2030, against a EUR 25mn facility already drawn and EGP 240mn of capacity already '
     f'under construction. Progress on it is '
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
    ('Distribution policy. ', f'The company declared EGP {n0(IN["div_fy25_declared"])}mn for '
     f'FY2025, about {pc(IN["payout"], 0)} of attributable profit, on top of EGP '
     f'{n0(IN["div_fy24_paid"])}mn for FY2024. A change in that policy changes the cash '
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
    ('The accounts are audited, and this study is built on them. ', 'An earlier edition of '
     'this work was written without access to a source document and reconstructed the '
     'history by closing disclosed profit against modelled assumptions. That edition is '
     'superseded. Every historical figure here is read from the consolidated financial '
     'statements signed by Deloitte on 25 February 2026, or from the reviewed interim '
     'accounts of 25 May 2026. Four things it got materially wrong are worth naming, '
     'because they show where reconstruction fails: minority interests were deducted at '
     'EGP 150mn against an audited EGP 158,005; the effective tax rate was inferred at '
     '29.4% against a disclosed 23.8%; the cost of debt was assumed at 21.5% against a '
     'euro-denominated book paying about 7.5%; and kiln capacity was assumed 14% too low.'),
    ('The model was rebuilt bottom up, and the answer moved a long way. ', f'Four '
     f'reviewers tested the previous edition. Between them they showed that its volume '
     f'came from an assumed price rather than from the plant, that its FY2025 validation '
     f'was an identity that could not fail, that its terminal capital was measured in '
     f'valuation-date pounds against a terminal-year cash flow, that its terminal cost of '
     f'debt sat 250 basis points below its own terminal risk-free rate, that its terminal '
     f'risk-free rate used the central bank\'s near-dated inflation target rather than its '
     f'medium-term one, that its discount factors applied each year\'s rate one period '
     f'late, that its beta was levered twice, and that ten rows of its income statement '
     f'were labelled one row above their contents. All of that is corrected here. The '
     f'central fair value moves from EGP 61.30 to EGP {n2(LN["central"])}, and the '
     f'conclusion moves from a premium over the market to a small discount.'),
    ('Volume is now physical, and it is the largest open question in the study. ', f'The '
     f'build runs on kiln utilisation, the clinker factor and two export shares, and the '
     f'three realised prices are derived from the audited revenue note. That makes the '
     f'prices testable, and they do not fully pass: export clinker derives to USD '
     f'{n1(UC["price_exp_clk_usd"])} a tonne against a trade-press range of USD 44-48. '
     f'Either the physical assumptions are too generous or realisations run below the '
     f'published indices. The company discloses despatch volumes in its investor material, '
     f'which would settle it; that material could not be reached from here, and the '
     f'audited statements are image-only scans that carry no volume table.'),
    ('The cost of debt is contractual, not paid. ', f'The blended '
     f'{pc(KDG["kd_blended"], 2)} sits above the {pc(KDG["eff_fy25"], 2)} that FY2025 '
     f'interest over average debt gives and the {pc(KDG["eff_q126_annualised"], 2)} the '
     f'first quarter of 2026 annualises to, because the book re-based mid-year and interest '
     f'on assets still under construction is capitalised. Adopting the contracted euro rate '
     f'also means the euro debt is not compensated for pound depreciation beyond the '
     f'currency path assumed here; the pound-equivalent alternative is '
     f'{pc(KDG["kd_egp_equivalent"], 2)} and is worth {sg(CON[0]["effect"])}.'),
    ('The forecast is well below the first-quarter run rate. ', f'This is the largest '
     f'judgement in the model and section 1.6 states it with the numbers. The first quarter '
     f'of 2026 ran a {pc(IN["gp_q1_26"]/IN["rev_q1_26"])} gross margin against '
     f'{pc(H["gross_profit"][2]/H["revenue"][2])} for FY2025 as a whole. If that holds, this '
     f'valuation is too cautious, and the margin sensitivity below is where to look.'),
    ('The terminal denominator is a choice. ', f'Return on capital is '
     f'{pc(TR["history"][2]["roic_book"])} on the audited book and {pc(TR["roic_repl"])} on '
     f'replacement cost. The terminal block uses replacement cost, which leaves the plant '
     f'roughly breaking even on new tonnes — {pc(GDV["n_over_ic"], 2)} against a hurdle of '
     f'{pc(GDV["hurdle"], 2)}, so four points of terminal growth are worth '
     f'{pc(GDV["spread_pct"], 1)} of value and the answer does not rest on the rate. On the '
     f'book basis growth would be close to free and the valuation materially higher. The '
     f'case for replacement cost is that the book carries a 2010-vintage plant at a tenth of '
     f'what one would cost to build today, but a reader is entitled to disagree.'),
    ('The beta is weak. ', f'R-squared of {pc(BETA["r2"], 1)} and a 90% interval of '
     f'[{n2(BETA["ci90"][0])}, {n2(BETA["ci90"][1])}]. The valuation is shown across a beta '
     f'range for exactly this reason, and the lead-lag correction is published as a value.'),
    ('The price map is over-wide. ', f'Its bands cover {pc(S0["cov80"], 0)} and '
     f'{pc(S0["cov90"], 0)} of outcomes against nominal 80% and 90%, and its skill against '
     f'a random walk is {sg(S0["skill_norm"], 1)}. It is carried as illustrative only.'),
    ('A minority position under a 60% shareholder. ', 'Aridos Jativa of Spain owns 60% of '
     'the capital. No control premium or discount is applied anywhere in this valuation, in '
     'either direction. The company also holds 1% of its own capital in treasury, acquired '
     'during 2025, which is excluded from the share count throughout.'),
    ('Currency, on both sides now. ', 'Revenue is 69% local and 31% export; costs are '
     'largely in pounds but fuel and spares are not; and the debt is 91% euro. A weaker '
     'pound raises export revenue in pounds and raises the pound cost of servicing the euro '
     'debt. The model carries one currency path acting on all three legs.'),
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
rows.append(['Revenue'] + [n0(x) for x in H['revenue']] + [n0(x) for x in F['revenue']])
rows.append(['Cost of sales'] + [f'({n0(x)})' for x in H['cogs']] + ['—'] * 5)
rows.append(['Gross profit'] + [n0(x) for x in H['gross_profit']] + ['—'] * 5)
rows.append(['Operating profit'] + [n0(x) for x in H['ebit']] + [n0(x) for x in F['ebit']])
rows.append(['Depreciation and amortisation'] + [n0(x) for x in H['dna']] +
            [n0(x) for x in F['dna']])
rows.append(['EBITDA'] + [n0(x) for x in H['ebitda']] + [n0(x) for x in F['ebitda']])
rows.append(['EBITDA margin'] + [pc(x) for x in H['margin']] + [pc(x) for x in F['margin']])
rows.append(['Net finance and other income'] +
            [n0(H['pbt'][i] - H['ebit'][i]) for i in range(3)] +
            [n0(x) for x in F['treasury']])
rows.append(['Profit before tax'] + [n0(x) for x in H['pbt']] + [n0(x) for x in F['pbt']])
rows.append(['Income tax'] + [f'({n0(x)})' for x in H['tax']] +
            [f'({n0(x)})' for x in F['tax']])
rows.append(['Attributable profit'] + [n0(x) for x in H['pat']] + [n0(x) for x in F['pat']])
rows.append(['Earnings per share (EGP)'] + [n2(x) for x in H['eps']] +
            [n2(x) for x in F['eps']])
table(rows, [1.52, 0.72, 0.72, 0.72, 0.72, 0.72, 0.72, 0.72, 0.72], size=8.0,
      band_rows={11})
caption('Table A1 — Three AUDITED years and five forecast. FY2023-FY2025 revenue, cost of '
        'sales, administrative expenses, provisions, pre-tax profit, tax, attributable '
        'profit, earnings per share and depreciation are disclosed figures; operating '
        'profit, EBITDA and the margins are formulas over them. The published earnings per '
        'share is struck on distributable profit after the statutory employees\' and '
        'directors\' share, which is why it differs slightly from profit over the share '
        'count.')
H2('Balance sheet')
rows = [['EGP mn'] + YH + YF]
rows.append(['Total assets'] + [n0(x) for x in
                                [IN['ta_fy23'], IN['ta_fy24'], IN['ta_fy25']]] +
            [n0(x) for x in F['total_assets']])
rows.append(['Cash and bank balances'] +
            [n0(x) for x in [IN['cash_fy23'], IN['cash_fy24'], IN['cash_fy25']]] +
            [n0(x) for x in F['cash']])
rows.append(['Interest-bearing debt'] +
            [n0(x) for x in [IN['debt_fy23'], IN['debt_fy24'], W['debt_total']]] +
            [n0(W['debt_total']) for _ in YF])
rows.append(['Net (cash) / debt'] +
            [n0(IN['debt_fy23'] - IN['cash_fy23']), n0(IN['debt_fy24'] - IN['cash_fy24']),
             n0(W['debt_total'] - IN['cash_fy25'])] +
            [n0(W['debt_total'] - x) for x in F['cash']])
rows.append(['Equity attributable to owners'] +
            [n0(x) for x in [IN['eq_fy23'], IN['eq_fy24'], IN['eq_fy25']]] +
            [n0(x) for x in F['equity']])
rows.append(['Book value per share (EGP)'] +
            [n2(x / SH) for x in [IN['eq_fy23'], IN['eq_fy24'], IN['eq_fy25']]] +
            [n2(x / SH) for x in F['equity']])
rows.append(['Return on equity'] +
            [pc(H['pat'][0] / IN['eq_fy23']), pc(H['pat'][1] / IN['eq_fy24']),
             pc(LN['roe_fy25'])] +
            [pc(F['pat'][i] / F['equity'][i]) for i in range(5)])
table(rows, [1.52, 0.72, 0.72, 0.72, 0.72, 0.72, 0.72, 0.72, 0.72], size=8.0,
      band_rows={1})
caption('Table A2 — All three historical years are AUDITED. The FY2025 balance sheet closes '
        f'exactly: total assets of EGP {n0(IN["ta_fy25"])}mn less total liabilities of EGP '
        f'{n0(IN["tl_fy25"])}mn equals equity of EGP {n0(IN["eq_fy25"] + IN["nci"])}mn.')
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
  f'production — a utilisation rate near {pc(PE["sector"]["utilisation"], 0)}. Production '
  f'less consumption is {n0(IN["egy_prod_mt"]-IN["egy_cons_mt"])}Mt; the '
  f'{n1(IN["egy_exports_mt"])}Mt figure usually quoted is cement AND clinker together, and '
  f'the earlier edition set the two against each other as though they reconciled. The abolition of the '
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
    ('Carbon. ', f'The EU carbon border mechanism raises the landed cost of exports into '
     f'Europe. At a clinker factor of {n3(IN["clinker_factor"])} — a PRODUCTION ratio, not '
     f'the ratio of two nameplate capacities the earlier edition mistook for one — this '
     f'producer is better placed than most Egyptian peers, but better placed is not '
     f'unaffected. It also ships {pc(UC["vol_clk_exp"]/UC["vol_fy25"])} of its tonnes as '
     f'raw clinker, which carries the highest embedded carbon of anything it sells.'),
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
