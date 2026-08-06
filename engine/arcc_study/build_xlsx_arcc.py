"""ARCC_Valuation_Model_06082026_public.xlsx — 16 sheets, formula-first.

Blue = input · black = formula · green = cross-sheet link.

The workbook CALCULATES. Every quantity arithmetically derivable from a driver is a live
Excel formula, so the reader can change a blue cell on Assumptions and watch the model
reprice: the cost of capital is built from the risk-free rate net of the sovereign spread,
beta and the premium; the cost of debt is taxed in the sheet; the weights come from debt
and market capitalisation; the terminal rate is built from its own components; the glide
fractions are visibly derived from the cost-of-debt path; the discount factors compound;
the cash-flow waterfall chains from margin through EBIT, NOPAT and free cash flow to
present value; the terminal block chains from reinvestment = growth / return on capital;
the statements roll forward; and every ratio and per-share figure is a formula.

Only three classes of cell are pasted, named on READ FIRST:
  1. audited and disclosed history — the primary record, not a calculation;
  2. the output of a unit build that would be unreadable flattened into a grid — here, the
     probabilistic price map's percentile ladder, which is the output of a 50,000-path
     simulation;
  3. whole-model re-runs — the sensitivity grids, where each cell is a complete
     revaluation of the entire model.

Every formula cell also records the model's own value into xlsx_expected.json, and
recalc.py evaluates the delivered workbook independently and asserts the two agree.
"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

D = json.load(open(os.path.join(HERE, 'study_numbers.json')))
S0 = json.load(open(os.path.join(HERE, 'step0_result.json')))
STK = json.load(open(os.path.join(HERE, 'strike_result.json')))
BETA = json.load(open(os.path.join(HERE, 'beta_result.json')))

BLUE = Font(color='0000FF'); GREEN = Font(color='008000'); BLACK = Font(color='000000')
TITLE = Font(bold=True, size=13, color='F6F1E6'); SUB = Font(size=9, color='6E7B77')
FILL_T = PatternFill('solid', start_color='1C3A36')
FILL_H = PatternFill('solid', start_color='EAF0EE')
FILL_G = PatternFill('solid', start_color='F6F1E6')
NUM0 = '#,##0;(#,##0);"-"'
NUM3 = '#,##0.000'; NUM1 = '#,##0.0;(#,##0.0);"-"'; NUM2 = '#,##0.00;(#,##0.00);"-"'
PCT = '0.0%;(0.0%);"-"'; PCT2 = '0.00%'; PX = '0.00;(0.00);"-"'; MULT = '0.00x'; DF4 = '0.0000'

M, H, F = D['meta'], D['history'], D['forecast']
W, DCF, LN, SN = D['wacc'], D['dcf'], D['lenses'], D['sensitivity']
BU, PE, SHT, TR = D['bottom_up'], D['peers'], D['share_triangulation'], D['terminal_reconciliation']
DNAT, EQG, CON = D['dna_triangulation'], D['equity_gap'], D['contested']
IN = {k: v['value'] for k, v in D['inputs'].items()}
SPOT, SH, TAX = M['spot'], M['shares_mn'], IN['tax_stat']
TAXE = H['tax_eff']
YH = H['years']
YF = F['years']
HC = ['B', 'C', 'D']
FC = ['E', 'F', 'G', 'H', 'I']
DC = ['B', 'C', 'D', 'E', 'F']
BUC = ['B', 'C', 'D', 'E', 'F', 'G']
BUY = ['FY2025A'] + YF

wb = Workbook()
EXPECT = {}


def sheet(n):
    ws = wb.create_sheet(n) if wb.sheetnames != ['Sheet'] else wb.active
    ws.title = n
    return ws


def title(ws, t, s=None, w=10, awidth=46, cwidth=13):
    ws['A1'] = t; ws['A1'].font = TITLE; ws['A1'].fill = FILL_T
    for c in range(2, w + 1):
        ws.cell(row=1, column=c).fill = FILL_T
    if s:
        ws['A2'] = s; ws['A2'].font = SUB
    ws.column_dimensions['A'].width = awidth
    for c in range(2, w + 1):
        ws.column_dimensions[get_column_letter(c)].width = cwidth


def put(ws, ad, v, font=BLACK, fmt=NUM0, bold=False, fill=None, wrap=False):
    c = ws[ad]; c.value = v
    c.font = Font(color=font.color, bold=bold)
    if fmt: c.number_format = fmt
    if fill: c.fill = fill
    if wrap: c.alignment = Alignment(wrap_text=True, vertical='top')
    return c


def putf(ws, ad, formula, expect, fmt=NUM0, bold=False, green=False):
    """Write a live formula and record the model's own value for the same cell."""
    put(ws, ad, formula, GREEN if green else BLACK, fmt, bold=bold)
    if expect is not None:
        EXPECT.setdefault(ws.title, {})[ad] = float(expect)


def hdr(ws, row, labels, start=1):
    for i, l in enumerate(labels):
        c = ws.cell(row=row, column=start + i, value=l)
        c.font = Font(bold=True); c.fill = FILL_H


def band(ws, row, w=10):
    for c in range(1, w + 1):
        ws.cell(row=row, column=c).fill = FILL_G
        ws.cell(row=row, column=c).font = Font(bold=True)


def note(ws, row, text, w=10):
    ws.cell(row=row, column=1, value=text).font = SUB
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=w)


# ============ 1 READ FIRST ====================================================
ws = sheet('READ FIRST')
title(ws, 'Testahil — Arabian Cement Company S.A.E. (EGX: ARCC)', None, 9)
LINES = [
 'Companion model · Independent Valuation Study · Educational analysis · Not investment advice', '',
 'What this workbook is. A transparent companion to the Arabian Cement valuation study. Every blue cell is an',
 'input; every black cell is a formula; green cells link across sheets.', '',
 'IT IS FORMULA-DRIVEN, AND THAT CLAIM IS TESTED. Every figure derivable from a driver is a live formula, so',
 'you can change a blue cell on Assumptions and watch the model reprice. The cost of equity is BUILT from the',
 'risk-free rate NET of the sovereign default spread, beta and the premium rather than pasted; the cost of debt',
 'is taxed in the sheet; the capital-structure weights come from debt and market capitalisation; the terminal',
 'rate is built from its own components; the glide fractions are visibly derived from the cost-of-debt path;',
 'the discount factors compound through that path; the cash-flow waterfall chains from margin through EBITDA,',
 'D&A, EBIT, NOPAT, capital expenditure and working capital to free cash flow and present value; the terminal',
 'block chains from reinvestment = growth / return on capital; the statements roll property, working capital,',
 'equity and cash forward; and every ratio and per-share figure on every sheet is a formula. A driver test',
 'perturbs every input in place, re-evaluates the whole workbook and confirms the headline moves in the right',
 'direction — the claim in this paragraph is only made because that test passes.', '',
 'THREE CLASSES OF CELL ARE PASTED, and it is worth knowing exactly which.',
 '  1. Audited and disclosed history — the primary record, not a calculation. Where a line is both disclosed',
 '     and derivable, the DISCLOSED figure is carried. These sit on Assumptions and on the historical columns',
 '     of the Income Statement and Balance Sheet, and are labelled there.',
 '  2. The output of a unit build that cannot survive being flattened into a grid: the percentile ladder of the',
 '     probabilistic price map on the Monte Carlo sheet, which is the output of a 50,000-path simulation of a',
 '     separate engine. Everything downstream of it — probabilities, ranges, per-share conversions — is formula.',
 '  3. Whole-model re-runs — the sensitivity grids on the Sensitivity sheet, where each individual cell is a',
 '     COMPLETE revaluation of the entire model at a different pair of assumptions. THESE GRIDS DO NOT REDRAW',
 '     WHEN A DRIVER CHANGES. If you edit an input on Assumptions, the unit build, waterfall, statements,',
 '     ratios and all four lenses reprice, but the sensitivity tables and the price map keep the values',
 '     printed here.',
 '  Anything else pasted would be a defect.', '',
 'HOW THE COMPANY IS VALUED, and why. Arabian Cement is a single-segment cement operating company: essentially',
 'all revenue is grey cement and clinker from two lines in Suez governorate, about five million tonnes a year',
 'and roughly 6% of Egypt\'s nominal capacity. There is no property leg, no lending book, no concession and no',
 'portfolio of operating subsidiaries, so there is no second lens to blend and no sum of parts. It is valued',
 'with one operating-company lens, cross-read against relative multiples, normalised earnings power and',
 'replacement cost. With cash of about EGP 3.46bn against debt of about EGP 1.04bn it is NET CASH, and that',
 'cash is stripped out of the discount rate and added back in the enterprise-to-equity bridge, so it is priced',
 'once and at face value.', '',
 'THREE THINGS THE READER SHOULD KNOW BEFORE READING ANY NUMBER.',
 '  * FY2025 is a cyclical peak, not a run rate. Egypt abolished its cement production quota in May 2025;',
 '    realised prices rose about 35% and revenue 42.6% in one year. The forecast glides the margin DOWN every',
 '    year from that peak, and the normalised lens cuts both the margin and the revenue base.',
 '  * Depreciation is not separately disclosed anywhere retrievable. It is triangulated by three independent',
 '    methods on the Unit Build sheet and AVERAGED THERE, in the sheet, rather than asserted. The three methods',
 '    disagree by a wide margin and the spread is shown.',
 '  * Capital expenditure is set at the ECONOMIC maintenance level in dollars per tonne of capacity, not at',
 '    book depreciation. A historic-cost asset base in a currency that has devalued several times understates',
 '    what it costs to keep a plant running; setting capex equal to book depreciation would flatter free cash',
 '    flow by construction. The cost of that conservatism is computed on the Fundamental Valuation sheet.', '',
 'PROVENANCE LIMIT, STATED PLAINLY. The company\'s audited statements could not be retrieved when this was',
 'built: the environment\'s egress policy refused every external financial host. Revenue, profit, operating',
 'income, the balance-sheet totals and both dividend distributions are carried as disclosed via reporting of',
 'the EGX filings and via aggregations of S&P Global Market Intelligence data. Where two aggregations disagree',
 '— they do, on total liabilities — the disagreement is shown on the Balance Sheet sheet rather than averaged',
 'away, and the figure that closes against total assets is the one carried.', '',
 'No rating and no price target. Fair-value ranges and distributions only.',
]
for i, ln in enumerate(LINES):
    ws.cell(row=4 + i, column=1, value=ln).font = Font(size=10 if ln else 9)
ws.column_dimensions['A'].width = 120

# ============ 2 ASSUMPTIONS ===================================================
wsA = sheet('Assumptions')
title(wsA, 'Assumptions — every driver, including the whole cost stack',
      'Blue cells are inputs. Nothing below a driver is typed.', 9, 54, 13)
A = {}


def inp(row, label, key, val, fmt=NUM0, unit=''):
    wsA.cell(row=row, column=1, value=label)
    put(wsA, f'B{row}', val, BLUE, fmt)
    if unit:
        wsA.cell(row=row, column=3, value=unit).font = SUB
    A[key] = f'Assumptions!$B${row}'
    return A[key]


def inprow(row, label, key, vals, fmt=NUM0, unit=''):
    wsA.cell(row=row, column=1, value=label)
    for i, v in enumerate(vals):
        put(wsA, f'{BUC[i]}{row}', v, BLUE, fmt)
        A[f'{key}{i}'] = f"Assumptions!${BUC[i]}${row}"
    if unit:
        wsA.cell(row=row, column=9, value=unit).font = SUB


band(wsA, 4, 9); wsA['A4'] = 'MARKET'
inp(5, 'Spot price', 'spot', SPOT, PX, 'EGP, close 06-Aug-2026')
inp(6, 'Shares outstanding', 'shares', SH, NUM2, 'mn')
inp(7, 'Statutory tax rate', 'tax', IN['tax_stat'], PCT, '')
inp(8, 'USD/EGP at the valuation date', 'fx', IN['fx'], NUM1, '')
inp(9, 'Beta (own-stock weekly regression)', 'beta', W['beta'], NUM3, '')

band(wsA, 11, 9); wsA['A11'] = 'PLANT — PHYSICAL'
inp(12, 'Cement capacity', 'capcem', IN['cap_cement_mt'], NUM2, 'Mt/yr')
inp(13, 'Kiln clinker capacity', 'capclk', IN['cap_clinker_mt'], NUM2, 'Mt/yr')
inp(14, 'Clinker factor', 'cfac', IN['clinker_factor'], NUM3, 't clinker / t cement')

band(wsA, 16, 9); wsA['A16'] = 'COST STACK — PHYSICAL AND MARKET DRIVERS'
inp(17, 'Specific thermal energy', 'thermal', IN['thermal_gj_t_clinker'], NUM2, 'GJ/t clinker')
inp(18, 'Fossil fuel price', 'fuelfos', IN['fuel_fossil_usd_gj'], NUM2, 'USD/GJ')
inp(19, 'Alternative fuel price', 'fuelalt', IN['fuel_alt_usd_gj'], NUM2, 'USD/GJ')
inp(20, 'Specific electrical energy', 'powkwh', IN['power_kwh_t_cement'], NUM1, 'kWh/t cement')
inp(21, 'Industrial electricity tariff', 'powtar', IN['power_tariff'], NUM2, 'EGP/kWh')
inp(22, 'Raw materials and quarrying', 'rawmat', IN['rawmat_egp_t'], NUM0, 'EGP/t cement')
inp(23, 'Packaging', 'packt', IN['packaging_egp_t'], NUM0, 'EGP/t bagged')
inp(24, 'Bagged share of despatches', 'bagsh', IN['bagged_share'], PCT, '')
inp(25, 'Distribution and selling', 'distt', IN['distribution_egp_t'], NUM0, 'EGP/t cement')
inp(26, 'Fixed cash cost', 'fixedt', IN['fixed_usd_t_capacity'], NUM2, 'USD/t of capacity')

band(wsA, 28, 9); wsA['A28'] = 'PATHS — FY2025A then FY2026E to FY2030E'
hdr(wsA, 29, [''] + BUY)
inprow(30, 'Kiln utilisation', 'util', IN['kiln_util'], PCT)
inprow(31, 'Alternative-fuel substitution rate', 'af', IN['af_share'], PCT)
inprow(32, 'Domestic share of despatches', 'dom', IN['domestic_share'], PCT)
inprow(33, 'Domestic realised price', 'pdom', IN['price_dom_egp_t'], NUM0, 'EGP/t')
inprow(34, 'Export price', 'pexp', IN['price_exp_usd_t'], NUM1, 'USD/t')
inprow(35, 'USD/EGP path', 'fxp', IN['fx_path'], NUM1, '')
inprow(36, 'Local cost-inflation index', 'infl', IN['cost_infl'], NUM3, 'FY2025 = 1.000')

band(wsA, 38, 9); wsA['A38'] = 'CAPITAL INTENSITY AND DISTRIBUTION — FY2026E to FY2030E'
hdr(wsA, 39, [''] + YF)


def inprow5(row, label, key, vals, fmt=NUM0, unit=''):
    wsA.cell(row=row, column=1, value=label)
    for i, v in enumerate(vals):
        put(wsA, f'{DC[i]}{row}', v, BLUE, fmt)
        A[f'{key}{i}'] = f"Assumptions!${DC[i]}${row}"
    if unit:
        wsA.cell(row=row, column=8, value=unit).font = SUB


inprow5(40, 'Depreciation as % of revenue', 'dnap', IN['dna_pct'], PCT)
inprow5(41, 'Cost-of-debt path', 'kdp', IN['kd_path'], PCT)
inprow5(42, 'Yield earned on cash', 'cy', IN['cash_yield'], PCT)
inp(43, 'Maintenance capital expenditure', 'cxt', IN['capex_usd_t_cap'], NUM2,
    'USD/t of capacity')
inp(44, 'Change in working capital / change in revenue', 'wcp', IN['wc_pct_drev'], PCT)
inp(45, 'Dividend payout ratio', 'payout', IN['payout'], PCT)

band(wsA, 47, 9); wsA['A47'] = 'COST OF CAPITAL'
inp(48, 'Risk-free rate (EGP 10-year government)', 'rf', IN['rf'], PCT2)
inp(49, 'Sovereign default spread (netted out)', 'sov', IN['sov_spread_cds'], PCT2)
inp(50, 'Equity risk premium', 'erp', IN['erp_cds'], PCT2)
inp(51, 'Cost of debt, pre-tax', 'kd', IN['kd'], PCT2)
inp(52, 'Terminal risk-free rate', 'rft', IN['rf_term'], PCT2)
inp(53, 'Terminal equity risk premium', 'erpt', IN['erp_term'], PCT2)
inp(54, 'Terminal cost of debt', 'kdt', IN['kd_term'], PCT2)
inp(55, 'Terminal debt weight', 'wdt', IN['wd_term'], PCT)
inp(56, 'Terminal growth rate', 'g', IN['g_term'], PCT)
inp(57, 'Elapsed fraction of FY2026 at the valuation date', 'stub', IN['stub_years'], NUM3)

band(wsA, 59, 9); wsA['A59'] = 'DISCLOSED HISTORY — PASTED CLASS 1'
inp(60, 'FY2023 revenue', 'rev23', IN['rev_fy23'], NUM0, 'EGP mn')
inp(61, 'FY2024 revenue', 'rev24', IN['rev_fy24'], NUM0, 'EGP mn')
inp(62, 'FY2025 revenue', 'rev25', IN['rev_fy25'], NUM0, 'EGP mn')
inp(63, 'FY2023 attributable profit', 'pat23', IN['pat_fy23'], NUM0, 'EGP mn')
inp(64, 'FY2024 attributable profit', 'pat24', IN['pat_fy24'], NUM0, 'EGP mn')
inp(65, 'FY2025 attributable profit', 'pat25', IN['pat_fy25'], NUM0, 'EGP mn')
inp(66, 'FY2025 operating income (disclosed)', 'ebit25', IN['ebit_fy25'], NUM0, 'EGP mn')
inp(67, 'Q4-2025 revenue', 'revq4', IN['rev_q4_25'], NUM0, 'EGP mn')
inp(68, 'Q4-2025 EBITDA', 'ebitq4', IN['ebitda_q4_25'], NUM0, 'EGP mn')
inp(69, 'Trailing gross margin', 'gm', IN['gross_margin'], PCT)
inp(70, 'Total assets', 'ta25', IN['ta_fy25'], NUM0, 'EGP mn')
inp(71, 'Cash and equivalents', 'cash', IN['cash_fy25'], NUM0, 'EGP mn')
inp(72, 'Total debt', 'debt', IN['debt_fy25'], NUM0, 'EGP mn')
inp(73, 'Total equity (reported)', 'eq25', IN['eq_fy25_rep'], NUM0, 'EGP mn')
inp(74, 'Total liabilities (alternative print)', 'tlalt', IN['tl_alt'], NUM0, 'EGP mn')
inp(75, 'Non-controlling interests', 'nci', IN['nci'], NUM0, 'EGP mn')
inp(76, 'FY2024 dividend per share', 'dps24', IN['dps_fy24'], NUM2, 'EGP')
inp(77, 'FY2025 dividend per share', 'dps25', IN['dps_fy25'], NUM2, 'EGP')
inp(78, 'FY2024 total distribution', 'div24', IN['div_fy24_total'], NUM0, 'EGP mn')
inp(79, 'FY2025 total distribution', 'div25', IN['div_fy25_total'], NUM0, 'EGP mn')
inp(80, 'FY2023 kiln utilisation', 'u23', IN['util_fy23'], PCT)
inp(81, 'FY2024 kiln utilisation', 'u24', IN['util_fy24'], PCT)
inp(82, 'Yield earned on cash through FY2025', 'cy25', IN['cash_yield_fy25'], PCT)
inp(83, 'Q1-2026 revenue', 'revq126', IN['rev_q1_26'], NUM0, 'EGP mn')
inp(84, 'Q1-2025 revenue', 'revq125', IN['rev_q1_25'], NUM0, 'EGP mn')
inp(85, 'Q1-2026 attributable profit', 'patq126', IN['pat_q1_26'], NUM0, 'EGP mn')
inp(86, 'FY2025 disclosed earnings per share', 'eps25', IN['eps_fy25'], NUM2, 'EGP')

band(wsA, 88, 9); wsA['A88'] = 'DEPRECIATION TRIANGULATION AND LENS INPUTS'
inp(89, 'Peer depreciation per tonne', 'dnapeer', IN['dna_peer_egp_t'], NUM0, 'EGP/t')
inp(90, 'Inventory days on cost of sales', 'invd', IN['inv_days'], NUM0, 'days')
inp(91, 'Receivable days on revenue', 'recd', IN['recv_days'], NUM0, 'days')
inp(92, 'Composite depreciation rate on net property', 'deprate', IN['dep_rate'], PCT)
inp(93, 'Replacement cost per annual tonne', 'repl', IN['repl_usd_t'], NUM0, 'USD/t')
inp(94, 'Justified enterprise value per annual tonne', 'evt', IN['ev_t_just'], NUM0, 'USD/t')
inp(95, 'Justified EV/EBITDA', 'eveb', IN['ev_ebitda_just'], MULT, '')
inp(96, 'Justified price/earnings', 'pej', IN['pe_just'], MULT, '')
inp(97, 'Mid-cycle EBITDA margin', 'nmgn', IN['norm_mgn'], PCT)
inp(98, 'Normalised revenue haircut', 'nhc', IN['norm_rev_haircut'], PCT)
inp(99, 'Weight — cash-flow lens', 'wdcf', IN['w_dcf'], PCT)
inp(100, 'Weight — relative lens', 'wrel', IN['w_rel'], PCT)
inp(101, 'Weight — normalised lens', 'wnorm', IN['w_norm'], PCT)
inp(102, 'Weight — asset lens', 'wasset', IN['w_asset'], PCT)

band(wsA, 104, 9); wsA['A104'] = 'SECTOR AND PEERS'
inp(105, 'Egyptian nameplate capacity', 'egcap', IN['egy_capacity_mt'], NUM1, 'Mt')
inp(106, 'Egyptian production 2025', 'egprod', IN['egy_prod_mt'], NUM1, 'Mt')
inp(107, 'Egyptian consumption 2025', 'egcons', IN['egy_cons_mt'], NUM1, 'Mt')
inp(108, 'Egyptian exports 2025', 'egexp', IN['egy_exports_mt'], NUM1, 'Mt')
inp(109, 'Dormant capacity under revival', 'egrev', IN['egy_revival_mt'], NUM1, 'Mt')
inp(110, 'Peer — Sinai Cement revenue', 'pscrev', IN['peer_scem_rev'], NUM0, 'EGP mn')
inp(111, 'Peer — Sinai Cement profit', 'pscpat', IN['peer_scem_pat'], NUM0, 'EGP mn')
inp(112, 'Peer — Sinai Cement market capitalisation', 'pscmc', IN['peer_scem_mcap'], NUM0, 'EGP mn')
inp(113, 'Peer — Misr Beni Suef revenue', 'pmbrev', IN['peer_mbsc_rev'], NUM0, 'EGP mn')
inp(114, 'Peer — Misr Beni Suef profit', 'pmbpat', IN['peer_mbsc_pat'], NUM0, 'EGP mn')
inp(115, 'Peer — Misr Beni Suef market capitalisation', 'pmbmc', IN['peer_mbsc_mcap'], NUM0, 'EGP mn')
note(wsA, 117, 'Every cell on this sheet is BLUE — an input. Nothing here is computed from anything')
note(wsA, 118, 'else here. Everything on every other sheet that can be derived from these is a formula.')

# ============ 3 UNIT BUILD ====================================================
wsU = sheet('Unit Build')
title(wsU, 'Bottom-up build — physical units in, EBITDA out',
      'EBITDA is a RESULT of this sheet, never an input.', 10, 48, 13)
hdr(wsU, 4, [''] + BUY)
LBL = ['Kiln clinker capacity (Mt/yr)', 'Kiln utilisation', 'Clinker produced (Mt)',
       'Cement capacity (Mt/yr)', 'Clinker factor (t clinker / t cement)',
       'Cement produced (Mt)', 'Domestic share', 'Domestic volume (Mt)',
       'Export volume (Mt)', 'Domestic price (EGP/t)', 'Export price (USD/t)',
       'USD/EGP', 'Domestic revenue (EGP mn)', 'Export revenue (EGP mn)',
       'REVENUE (EGP mn)', 'Blended realised price (EGP/t)']
for j, l in enumerate(LBL):
    wsU.cell(row=5 + j, column=1, value=l)
for i in range(6):
    c = BUC[i]
    putf(wsU, f'{c}5', f"={A['capclk']}", IN['cap_clinker_mt'], NUM2, green=True)
    putf(wsU, f'{c}6', f"={A[f'util{i}']}", IN['kiln_util'][i], PCT, green=True)
    putf(wsU, f'{c}7', f"={c}5*{c}6", BU[i]['clinker'], NUM3)
    putf(wsU, f'{c}8', f"={A['capcem']}", IN['cap_cement_mt'], NUM2, green=True)
    putf(wsU, f'{c}9', f"={A['cfac']}", D['clinker_factor'], NUM3, green=True)
    putf(wsU, f'{c}10', f"={c}7/{c}9", BU[i]['cement'], NUM3)
    putf(wsU, f'{c}11', f"={A[f'dom{i}']}", IN['domestic_share'][i], PCT, green=True)
    putf(wsU, f'{c}12', f"={c}10*{c}11", BU[i]['dom'], NUM3)
    putf(wsU, f'{c}13', f"={c}10-{c}12", BU[i]['exp'], NUM3)
    putf(wsU, f'{c}14', f"={A[f'pdom{i}']}", IN['price_dom_egp_t'][i], NUM0, green=True)
    putf(wsU, f'{c}15', f"={A[f'pexp{i}']}", IN['price_exp_usd_t'][i], NUM1, green=True)
    putf(wsU, f'{c}16', f"={A[f'fxp{i}']}", IN['fx_path'][i], NUM1, green=True)
    putf(wsU, f'{c}17', f"={c}12*{c}14", BU[i]['dom'] * IN['price_dom_egp_t'][i], NUM0)
    putf(wsU, f'{c}18', f"={c}13*{c}15*{c}16",
         BU[i]['exp'] * IN['price_exp_usd_t'][i] * IN['fx_path'][i], NUM0)
    putf(wsU, f'{c}19', f"={c}17+{c}18", BU[i]['rev'], NUM0, bold=True)
    putf(wsU, f'{c}20', f"={c}19/{c}10", BU[i]['price'], NUM0)

band(wsU, 22, 10); wsU['A22'] = 'COST STACK — EGP PER TONNE OF CEMENT'
CL = ['Alternative-fuel substitution rate', 'Blended fuel price (USD/GJ)', 'Thermal fuel',
      'Electrical power', 'Raw materials and quarrying', 'Packaging',
      'Distribution and selling', 'TOTAL VARIABLE (EGP/t)']
for j, l in enumerate(CL):
    wsU.cell(row=23 + j, column=1, value=l)
for i in range(6):
    c = BUC[i]
    putf(wsU, f'{c}23', f"={A[f'af{i}']}", IN['af_share'][i], PCT, green=True)
    putf(wsU, f'{c}24', f"={c}23*{A['fuelalt']}+(1-{c}23)*{A['fuelfos']}",
         BU[i]['fuel_usd_gj'], NUM2)
    putf(wsU, f'{c}25', f"={A['thermal']}*{c}9*{c}24*{c}16", BU[i]['c_fuel'], NUM0)
    putf(wsU, f'{c}26', f"={A['powkwh']}*{A['powtar']}*{A[f'infl{i}']}", BU[i]['c_pow'], NUM0)
    putf(wsU, f'{c}27', f"={A['rawmat']}*{A[f'infl{i}']}", BU[i]['c_raw'], NUM0)
    putf(wsU, f'{c}28', f"={A['packt']}*{A['bagsh']}*{A[f'infl{i}']}", BU[i]['c_pack'], NUM0)
    putf(wsU, f'{c}29', f"={A['distt']}*{A[f'infl{i}']}", BU[i]['c_dist'], NUM0)
    putf(wsU, f'{c}30', f"=SUM({c}25:{c}29)", BU[i]['var_t'], NUM0, bold=True)

band(wsU, 32, 10); wsU['A32'] = 'PROFIT AND LOSS — EGP MILLION'
for j, l in enumerate(['Revenue', 'Variable cost', 'Fixed cost', 'EBITDA  (AN OUTPUT)',
                       'EBITDA margin', 'EBITDA per tonne (EGP)']):
    wsU.cell(row=33 + j, column=1, value=l)
for i in range(6):
    c = BUC[i]
    putf(wsU, f'{c}33', f"={c}19", BU[i]['rev'], NUM0, green=True)
    putf(wsU, f'{c}34', f"={c}30*{c}10", BU[i]['var'], NUM0)
    putf(wsU, f'{c}35', f"={A['fixedt']}*{c}8*{A['fxp0']}*{A[f'infl{i}']}", BU[i]['fixed'], NUM0)
    putf(wsU, f'{c}36', f"={c}33-{c}34-{c}35", BU[i]['ebitda'], NUM0, bold=True)
    putf(wsU, f'{c}37', f"={c}36/{c}33", BU[i]['mgn'], PCT)
    putf(wsU, f'{c}38', f"={c}36/{c}10", BU[i]['ebitda'] / BU[i]['cement'], NUM0)

band(wsU, 40, 10); wsU['A40'] = 'DEPRECIATION — THREE METHODS, AVERAGED HERE'
TRI = [('Method 1 — Q4-2025 EBITDA margin applied to FY2025 revenue, less disclosed EBIT',
        'B41', f"={A['ebitq4']}/{A['revq4']}*{A['rev25']}-{A['ebit25']}",
        DNAT['m1_q4_margin_closure']),
       ('Method 2 — peer depreciation per tonne times FY2025 despatched volume',
        'B42', f"={A['dnapeer']}*B10", DNAT['m2_peer_per_tonne']),
       ('  Cost of sales implied by the disclosed gross margin', 'B43',
        f"={A['rev25']}*(1-{A['gm']})", DNAT['cogs']),
       ('  Inventory implied by inventory days', 'B44', f"=B43*{A['invd']}/365", DNAT['inventory']),
       ('  Receivables implied by receivable days', 'B45',
        f"={A['rev25']}*{A['recd']}/365", DNAT['receivables']),
       ('  Net property implied by total assets less cash and working capital', 'B46',
        f"={A['ta25']}-{A['cash']}-B44-B45", DNAT['ppe_estimate']),
       ('Method 3 — net property times the composite depreciation rate', 'B47',
        f"=B46*{A['deprate']}", DNAT['m3_property_base']),
       ('ADOPTED — the average of the three methods', 'B48',
        "=AVERAGE(B41,B42,B47)", DNAT['adopted']),
       ('Adopted, as a share of FY2025 revenue', 'B49',
        f"=B48/{A['rev25']}", DNAT['pct_of_revenue']),
       ('Adopted, EGP per tonne of despatch', 'B50', "=B48/B10", DNAT['per_tonne']),
       ('Spread between the highest and lowest method', 'B51',
        "=MAX(B41,B42,B47)/MIN(B41,B42,B47)-1",
        max(DNAT['m1_q4_margin_closure'], DNAT['m2_peer_per_tonne'],
            DNAT['m3_property_base']) /
        min(DNAT['m1_q4_margin_closure'], DNAT['m2_peer_per_tonne'],
            DNAT['m3_property_base']) - 1)]
for lab, ad, fm, ex in TRI:
    wsU.cell(row=int(ad[1:]), column=1, value=lab)
    putf(wsU, ad, fm, ex, PCT if ad in ('B49', 'B51') else NUM0,
         bold=(ad == 'B48'))
wsU['B49'].number_format = PCT
wsU['B50'].number_format = NUM0
wsU['B51'].number_format = PCT

band(wsU, 53, 10); wsU['A53'] = 'VALIDATION — A TEST THAT CAN FAIL'
VAL = [('Bottom-up FY2025 revenue', 'B54', "=B19", BU[0]['rev'], NUM0),
       ('Disclosed FY2025 revenue', 'B55', f"={A['rev25']}", IN['rev_fy25'], NUM0),
       ('Difference', 'B56', "=B54/B55-1", BU[0]['rev'] / IN['rev_fy25'] - 1, PCT),
       ('Bottom-up FY2025 operating profit (EBITDA less adopted depreciation)', 'B57',
        "=B36-B48", BU[0]['ebitda'] - DNAT['adopted'], NUM0),
       ('DISCLOSED FY2025 operating income', 'B58', f"={A['ebit25']}", IN['ebit_fy25'], NUM0),
       ('Difference', 'B59', "=B57/B58-1",
        (BU[0]['ebitda'] - DNAT['adopted']) / IN['ebit_fy25'] - 1, PCT)]
for lab, ad, fm, ex, ft in VAL:
    wsU.cell(row=int(ad[1:]), column=1, value=lab)
    putf(wsU, ad, fm, ex, ft, green=(ad in ('B55', 'B58')))
note(wsU, 61, 'Nothing on this sheet is solved to force agreement. Every physical and market driver is an')
note(wsU, 62, 'independent norm, so a wrong cost stack shows up as a non-zero residual in rows 56 and 59.')
note(wsU, 63, 'The one calibrated figure is fixed cash cost per tonne of capacity, and it is disclosed as such')
note(wsU, 64, 'on Assumptions rather than presented as an observation.')

# ============ 4 DCF ===========================================================
wsD = sheet('DCF')
title(wsD, 'Discounted cash flow — the primary lens',
      'Cost of capital built here, never pasted.', 8, 52, 14)
hdr(wsD, 4, [''] + YF)
ROWS = ['Revenue', 'EBITDA margin', 'EBITDA', 'Depreciation and amortisation', 'EBIT',
        'Tax rate (effective)', 'NOPAT  (EBIT × (1 − t))', 'Plus depreciation',
        'Less capital expenditure', 'Less change in working capital',
        'FREE CASH FLOW TO THE FIRM', 'Glide fraction', 'Forward cost of capital',
        'Discount factor', 'PRESENT VALUE OF FCFF']
for j, lab in enumerate(ROWS):
    wsD.cell(row=5 + j, column=1, value=lab)
for i in range(5):
    c = DC[i]
    putf(wsD, f'{c}5', f"='Unit Build'!{BUC[i+1]}33", F['revenue'][i], NUM0, green=True)
    putf(wsD, f'{c}7', f"='Unit Build'!{BUC[i+1]}36", F['ebitda'][i], NUM0, green=True)
    putf(wsD, f'{c}6', f"={c}7/{c}5", F['margin'][i], PCT)
    putf(wsD, f'{c}8', f"={c}5*{A[f'dnap{i}']}", F['dna'][i], NUM0)
    putf(wsD, f'{c}9', f"={c}7-{c}8", F['ebit'][i], NUM0)
    putf(wsD, f'{c}10', "=$C$47", TAXE, PCT, green=True)
    putf(wsD, f'{c}11', f"={c}9*(1-{c}10)", F['nopat'][i], NUM0)
    putf(wsD, f'{c}12', f"={c}8", F['dna'][i], NUM0)
    putf(wsD, f'{c}13', f"=-{A['capcem']}*{A['cxt']}*{A[f'fxp{i+1}']}", -F['capex'][i], NUM0)
    prev = A['rev25'] if i == 0 else f"{DC[i-1]}5"
    putf(wsD, f'{c}14', f"=-({c}5-{prev})*{A['wcp']}", -F['dwc'][i], NUM0)
    if i == 0:
        putf(wsD, f'{c}15', f"=({c}11+{c}12+{c}13+{c}14)*(1-{A['stub']})",
             F['fcff'][i], NUM0, bold=True)
    else:
        putf(wsD, f'{c}15', f"={c}11+{c}12+{c}13+{c}14", F['fcff'][i], NUM0, bold=True)
    putf(wsD, f'{c}16', f"=({A['kdp0']}-{A[f'kdp{i}']})/({A['kdp0']}-{A['kdp4']})",
         F['glide'][i], DF4)
    putf(wsD, f'{c}17', f"=$C$40-($C$40-$C$46)*{c}16", F['fwd_wacc'][i], PCT2)
    if i == 0:
        fm = f"=1/(1+B17)^((1-{A['stub']})/2)"
    elif i == 1:
        fm = f"=1/(1+B17)^(1-{A['stub']}+0.5)"
    else:
        pre = "*".join(f"(1+{DC[k]}17)" for k in range(i - 1))
        fm = f"=1/({pre}*(1+{DC[i-1]}17)^(1-{A['stub']}+0.5))"
    putf(wsD, f'{c}18', fm, F['df'][i], DF4)
    putf(wsD, f'{c}19', f"={c}15*{c}18", F['pv'][i], NUM0)

band(wsD, 21, 8); wsD['A21'] = 'TERMINAL BLOCK'
TB = [('Replacement-cost invested capital (EGP mn)', 'B22',
       f"={A['capcem']}*{A['repl']}*{A['fx']}", DCF['ic_repl'], NUM0),
      ('Terminal NOPAT  (year 5 NOPAT grown at g)', 'B23', f"=F11*(1+{A['g']})",
       DCF['nopat_term'], NUM0),
      ('Terminal return on invested capital', 'B24', "=B23/B22", DCF['roic_term'], PCT),
      ('Reinvestment rate  (g ÷ return on capital)', 'B25', f"={A['g']}/B24",
       DCF['rr_term'], PCT),
      ('Terminal value', 'B26', f"=B23*(1-B25)/($C$46-{A['g']})", DCF['tv'], NUM0),
      ('Present value of terminal value', 'B27', "=B26*F18", DCF['pv_tv'], NUM0)]
for lab, ad, fm, ex, ft in TB:
    wsD.cell(row=int(ad[1:]), column=1, value=lab)
    putf(wsD, ad, fm, ex, ft)

band(wsD, 29, 8); wsD['A29'] = 'ENTERPRISE TO EQUITY BRIDGE'
BR = [('Present value of explicit years (FY2026E-FY2030E)', 'B30', "=SUM(B19:F19)",
       DCF['sum_pv'], NUM0),
      ('Present value of terminal value', 'B31', "=B27", DCF['pv_tv'], NUM0),
      ('Enterprise value', 'B32', "=B30+B31", DCF['ev'], NUM0),
      ('TERMINAL VALUE AS % OF ENTERPRISE VALUE', 'B33', "=B31/B32", DCF['tv_share'], PCT),
      ('Cash at the valuation date', 'B34',
       f"={A['cash']}+B15/(1-{A['stub']})*{A['stub']}", DCF['cash_at_val'], NUM0),
      ('Less gross debt', 'B35', f"=-{A['debt']}", -IN['debt_fy25'], NUM0),
      ('Net cash (ADDED — the company is net cash)', 'B36', "=B34+B35", DCF['net_cash'], NUM0),
      ('Less non-controlling interests', 'B37', f"=-{A['nci']}", -IN['nci'], NUM0),
      ('Equity value', 'B38', "=B32+B36+B37", DCF['equity'], NUM0),
      ('Shares outstanding (mn)', 'B39', f"={A['shares']}", SH, NUM2),
      ('FAIR VALUE PER SHARE (EGP)', 'B40', "=B38/B39", DCF['fv'], PX)]
for lab, ad, fm, ex, ft in BR:
    wsD.cell(row=int(ad[1:]), column=1, value=lab)
    putf(wsD, ad, fm, ex, ft, bold=(ad in ('B32', 'B33', 'B38', 'B40')))

band(wsD, 34, 8)
for lab, ad, fm, ex, ft in BR:
    if ad == 'B34':
        wsD.cell(row=34, column=1, value=lab)
        putf(wsD, ad, fm, ex, ft)
band(wsD, 42, 8); wsD['A42'] = 'COST OF CAPITAL — BUILT HERE'
CC = [('Risk-free rate (observed EGP 10-year)', 'C36', f"={A['rf']}", IN['rf'], PCT2),
      ('Less sovereign default spread', 'C37', f"=-{A['sov']}", -IN['sov_spread_cds'], PCT2),
      ('Normalised risk-free rate', 'C38', "=C36+C37", W['rf_star'], PCT2),
      ('Cost of equity  (rf* + beta × premium)', 'C39',
       f"=C38+{A['beta']}*{A['erp']}", W['ke_exp'], PCT2),
      ('WACC — explicit window', 'C40', "=(1-C43)*C39+C43*C41", W['wacc_exp'], PCT2),
      ('Cost of debt after tax', 'C41', f"={A['kd']}*(1-{A['tax']})", W['kd_at'], PCT2),
      ('Market capitalisation', 'C42', f"={A['spot']}*{A['shares']}", M['mktcap'], NUM0),
      ('Debt weight  D/(D+E)', 'C43', f"={A['debt']}/({A['debt']}+C42)", W['wd_gross'], '0.000%'),
      ('Terminal beta, RE-LEVERED to the terminal structure', 'C44',
       f"={A['beta']}*(1+(1-{A['tax']})*{A['wdt']}/(1-{A['wdt']}))", W['beta_term'], NUM3),
      ('Terminal cost of equity  (rf_term + beta_L × premium_term)', 'C45',
       f"={A['rft']}+C44*{A['erpt']}", W['ke_term'], PCT2),
      ('WACC — terminal', 'C46',
       f"=(1-{A['wdt']})*C45+{A['wdt']}*{A['kdt']}*(1-{A['tax']})", W['wacc_term'], PCT2),
      ('Effective tax rate  (built from the FY2025 closure)', 'C47',
       f"=1-{A['pat25']}/({A['ebit25']}+{A['cash']}*{A['cy25']}-{A['debt']}*{A['kd']})",
       TAXE, PCT2),
      ('Memo: net finance income implied for FY2025', 'C48',
       f"={A['cash']}*{A['cy25']}-{A['debt']}*{A['kd']}", H['netfin_fy25'], NUM0),
      ('Memo: retired construction, risk-free NOT netted', 'C49',
       f"={A['rf']}+{A['beta']}*{A['erp']}", W['ke_raw_retired'], PCT2),
      ('Memo: sovereign double-count removed (basis points)', 'C50', "=(C49-C39)*10000",
       (W['ke_raw_retired'] - W['ke_exp']) * 10000, NUM0),
      ('Memo: WACC on NET-debt weights (alternative, not adopted)', 'C51',
       f"=(1-C52)*C39+C52*C41", W['wacc_exp_net_weights'], PCT2),
      ('Memo: net-debt weight', 'C52',
       f"=({A['debt']}-{A['cash']})/(({A['debt']}-{A['cash']})+C42)", W['wd_net'], PCT)]
for lab, ad, fm, ex, ft in CC:
    wsD.cell(row=int(ad[1:]), column=1, value=lab)
    putf(wsD, ad, fm, ex, ft, bold=(ad in ('C40', 'C46')))
note(wsD, 54, 'The glide fraction on row 16 is DERIVED from the cost-of-debt path on Assumptions, so the shape of')
note(wsD, 55, 'the discount schedule is inherited rather than invented. The terminal value is capitalised at the')
note(wsD, 56, 'terminal rate and discounted on year five\'s OWN cumulative factor — one date, one price of time.')
note(wsD, 57, 'Terminal return on capital is struck on REPLACEMENT-COST capacity rather than the pre-devaluation')
note(wsD, 58, 'book, which would flatter it and let terminal growth through unpaid for.')
note(wsD, 60, 'ONE COUPLING THE READER SHOULD KNOW ABOUT. The effective tax rate on row 47 is INFERRED from the')
note(wsD, 61, 'FY2025 closure: disclosed operating profit plus modelled net finance income, against DISCLOSED')
note(wsD, 62, 'profit after tax. Profit after tax is a fact, so raising the cash balance raises the imputed')
note(wsD, 63, 'finance income and therefore the imputed tax rate on the operating business. Cash and debt are')
note(wsD, 64, 'therefore NOT clean one-way bridge levers here: adding EGP 1bn of cash adds to net cash and')
note(wsD, 65, 'subtracts almost exactly as much from enterprise value. The clean net-cash sensitivity — the tax')
note(wsD, 66, 'rate held and the balance varied — is the last grid on the Sensitivity sheet.')

# ============ 5 EV BRIDGE =====================================================
wsB = sheet('EV Bridge')
title(wsB, 'Enterprise value to equity bridge', None, 6, 54, 16)
hdr(wsB, 4, ['', 'EGP mn', 'Per share (EGP)'])
BRW = [('Present value of explicit free cash flow', "=DCF!B30", DCF['sum_pv']),
       ('Present value of terminal value', "=DCF!B31", DCF['pv_tv']),
       ('Enterprise value', "=DCF!B32", DCF['ev']),
       ('Plus net cash', "=DCF!B36", DCF['net_cash']),
       ('Less non-controlling interests', "=DCF!B37", -IN['nci']),
       ('Equity value', "=DCF!B38", DCF['equity'])]
for j, (lab, fm, ex) in enumerate(BRW):
    wsB.cell(row=5 + j, column=1, value=lab)
    putf(wsB, f'B{5+j}', fm, ex, NUM0, green=True, bold=(j in (2, 5)))
    putf(wsB, f'C{5+j}', f"=B{5+j}/{A['shares']}", ex / SH, PX, bold=(j in (2, 5)))
wsB['A12'] = 'TERMINAL VALUE AS % OF ENTERPRISE VALUE'
putf(wsB, 'B12', "=DCF!B33", DCF['tv_share'], PCT, green=True, bold=True)
wsB['A13'] = 'Memo: spot price'
putf(wsB, 'C13', f"={A['spot']}", SPOT, PX, green=True)
wsB['A14'] = 'Fair value less spot'
putf(wsB, 'C14', "=C10-C13", DCF['fv'] - SPOT, PX)
wsB['A15'] = 'Upside / (downside) to the cash-flow lens'
putf(wsB, 'C15', "=C10/C13-1", DCF['fv'] / SPOT - 1, PCT)
wsB['A16'] = 'Memo: enterprise value per annual tonne of capacity (USD)'
putf(wsB, 'C16', f"=B7/{A['capcem']}/{A['fx']}", DCF['ev'] / IN['cap_cement_mt'] / IN['fx'], NUM1)
note(wsB, 18, 'Terminal value share is linked live to the DCF sheet — never typed. The company is net cash, so')
note(wsB, 19, 'the bridge ADDS cash and DEDUCTS minority interests; both signs are asserted in the build.')

# ============ 6 INCOME STATEMENT ==============================================
wsI = sheet('Income Statement')
title(wsI, 'Income statement — 3 years historical + 5-year forecast', 'EGP mn', 10, 46, 13)
hdr(wsI, 4, [''] + YH + YF)
IL = ['Revenue', 'EBITDA', 'EBITDA margin', 'Depreciation and amortisation', 'EBIT',
      'Net finance income', 'Profit before tax', 'Tax', 'Profit after tax',
      'Earnings per share (EGP)', 'Dividends', 'Dividend per share (EGP)']
for j, l in enumerate(IL):
    wsI.cell(row=5 + j, column=1, value=l)
HIST_REV = [A['rev23'], A['rev24'], A['rev25']]
HIST_PAT = [A['pat23'], A['pat24'], A['pat25']]
for i in range(3):
    c = HC[i]
    putf(wsI, f'{c}5', f"={HIST_REV[i]}", H['revenue'][i], NUM0, green=True)
    if i == 2:
        putf(wsI, f'{c}9', f"={A['ebit25']}", H['ebit'][i], NUM0, green=True)
    else:
        putf(wsI, f'{c}9', f"={HIST_PAT[i]}/(1-DCF!$C$47)", H['ebit'][i], NUM0)
    putf(wsI, f'{c}8', f"='Unit Build'!$B$50*{c}16", H['dna'][i], NUM0)
    putf(wsI, f'{c}6', f"={c}9+{c}8", H['ebitda'][i], NUM0, bold=True)
    putf(wsI, f'{c}7', f"={c}6/{c}5", H['margin'][i], PCT)
    putf(wsI, f'{c}13', f"={HIST_PAT[i]}", H['pat'][i], NUM0, green=True, bold=True)
    if i == 2:
        putf(wsI, f'{c}10', "=DCF!$C$48", H['netfin_fy25'], NUM0, green=True)
    else:
        putf(wsI, f'{c}10', "=0", 0.0, NUM0)
    putf(wsI, f'{c}11', f"={c}9+{c}10", H['ebit'][i] + (H['netfin_fy25'] if i == 2 else 0.0),
         NUM0)
    putf(wsI, f'{c}12', f"={c}11-{c}13",
         H['ebit'][i] + (H['netfin_fy25'] if i == 2 else 0.0) - H['pat'][i], NUM0)
    putf(wsI, f'{c}14', f"={c}13/{A['shares']}", H['eps'][i], PX)
wsI.cell(row=16, column=1, value='Memo: despatched volume (Mt)')
for i in range(3):
    putf(wsI, f'{HC[i]}16', f"={A['capclk']}*{[A['u23'], A['u24'], A['util0']][i]}/{A['cfac']}",
         H['volume_mt'][i], NUM3, green=True)
wsI.cell(row=17, column=1, value='Memo: blended realised price (EGP/t)')
for i in range(3):
    putf(wsI, f'{HC[i]}17', f"={HC[i]}5/{HC[i]}16", H['price_t'][i], NUM0)
put(wsI, 'B15', None, BLACK, NUM0)
put(wsI, 'C15', IN['div_fy24_total'], BLUE, NUM0)
put(wsI, 'D15', IN['div_fy25_total'], BLUE, NUM0)
for i in (1, 2):
    putf(wsI, f'{HC[i]}16b'.replace('16b', '18'),
         f"={HC[i]}15/{A['shares']}", [0, IN['div_fy24_total'], IN['div_fy25_total']][i] / SH,
         PX)
wsI.cell(row=15, column=1, value='Dividends declared (disclosed)')
wsI.cell(row=18, column=1, value='Dividend per share (EGP)')
for i in range(5):
    c = FC[i]
    putf(wsI, f'{c}5', f"=DCF!{DC[i]}5", F['revenue'][i], NUM0, green=True)
    putf(wsI, f'{c}6', f"=DCF!{DC[i]}7", F['ebitda'][i], NUM0, green=True, bold=True)
    putf(wsI, f'{c}7', f"={c}6/{c}5", F['margin'][i], PCT)
    putf(wsI, f'{c}8', f"=DCF!{DC[i]}8", F['dna'][i], NUM0, green=True)
    putf(wsI, f'{c}9', f"={c}6-{c}8", F['ebit'][i], NUM0)
    # Treasury income is earned on the OPENING cash balance — the prior year's close —
    # so the reference points one column LEFT. Pointing it at the same column would make
    # profit depend on a cash balance that itself depends on profit.
    open_cash = f"{A['cash']}" if i == 0 else f"'Balance Sheet'!{FC[i-1]}7"
    putf(wsI, f'{c}10', f"={open_cash}*{A[f'cy{i}']}-{A['debt']}*{A[f'kdp{i}']}",
         F['treasury'][i], NUM0)
    putf(wsI, f'{c}11', f"={c}9+{c}10", F['pbt'][i], NUM0)
    putf(wsI, f'{c}12', f"={c}11*DCF!$C$47", F['tax'][i], NUM0)
    putf(wsI, f'{c}13', f"={c}11-{c}12", F['pat'][i], NUM0, bold=True)
    putf(wsI, f'{c}14', f"={c}13/{A['shares']}", F['eps'][i], PX)
    putf(wsI, f'{c}15', f"={c}13*{A['payout']}", F['dividends'][i], NUM0)
    putf(wsI, f'{c}18', f"={c}15/{A['shares']}", F['dps'][i], PX)
    putf(wsI, f'{c}16', f"='Unit Build'!{BUC[i+1]}10", F['volume_mt'][i], NUM3, green=True)
    putf(wsI, f'{c}17', f"={c}5/{c}16", F['price_t'][i], NUM0)
note(wsI, 20, 'Revenue and profit after tax for FY2023-FY2025 and FY2025 operating income are DISCLOSED and')
note(wsI, 21, 'pasted on Assumptions. Every other historical line is DERIVED by closing the disclosed profit at')
note(wsI, 22, 'the effective tax rate built on the DCF sheet, and is a formula here. FY2023 and FY2024 net')
note(wsI, 23, 'finance income is set to zero: the cash pile that produces it was built during FY2025.')

# ============ 7 BALANCE SHEET =================================================
wsBS = sheet('Balance Sheet')
title(wsBS, 'Balance sheet — 3 years historical + 5-year forecast', 'EGP mn', 10, 46, 13)
hdr(wsBS, 4, [''] + YH + YF)
BL = ['Net property, plant and equipment', 'Working capital (inventory + receivables)',
      'Cash and equivalents', 'TOTAL ASSETS', 'Total debt', 'Other liabilities',
      'Total liabilities', 'Total equity', 'Net (cash) / debt',
      'Book value per share (EGP)', 'Return on equity']
for j, l in enumerate(BL):
    wsBS.cell(row=5 + j, column=1, value=l)
putf(wsBS, 'D5', "='Unit Build'!B46", DNAT['ppe_estimate'], NUM0, green=True)
putf(wsBS, 'D6', "='Unit Build'!B44+'Unit Build'!B45",
     DNAT['inventory'] + DNAT['receivables'], NUM0, green=True)
putf(wsBS, 'D7', f"={A['cash']}", IN['cash_fy25'], NUM0, green=True)
putf(wsBS, 'D8', f"={A['ta25']}", IN['ta_fy25'], NUM0, green=True, bold=True)
putf(wsBS, 'D9', f"={A['debt']}", IN['debt_fy25'], NUM0, green=True)
putf(wsBS, 'D12', f"={A['eq25']}", IN['eq_fy25_rep'], NUM0, green=True, bold=True)
putf(wsBS, 'D11', "=D8-D12", EQG['derived_liabilities'], NUM0)
putf(wsBS, 'D10', "=D11-D9", EQG['derived_liabilities'] - IN['debt_fy25'], NUM0)
putf(wsBS, 'D13', "=D9-D7", DCF['net_debt_bs'], NUM0)
putf(wsBS, 'D14', f"=D12/{A['shares']}", LN['bvps'], PX)
putf(wsBS, 'D15', f"={A['pat25']}/D12", LN['roe_sust'], PCT)
for i in range(5):
    c = FC[i]
    prev = 'D' if i == 0 else FC[i - 1]
    putf(wsBS, f'{c}5', f"={prev}5-DCF!{DC[i]}8-DCF!{DC[i]}13",
         F['ppe'][i], NUM0)
    putf(wsBS, f'{c}6', f"={prev}6-DCF!{DC[i]}14", F['wc'][i], NUM0)
    if i == 0:
        putf(wsBS, f'{c}7',
             f"=D7+'Income Statement'!{c}13+DCF!{DC[i]}8+DCF!{DC[i]}13+DCF!{DC[i]}14"
             f"-'Income Statement'!{c}15", F['cash'][i], NUM0)
    else:
        putf(wsBS, f'{c}7',
             f"={prev}7+'Income Statement'!{c}13+DCF!{DC[i]}8+DCF!{DC[i]}13+DCF!{DC[i]}14"
             f"-'Income Statement'!{c}15", F['cash'][i], NUM0)
    putf(wsBS, f'{c}8', f"={c}5+{c}6+{c}7", F['total_assets'][i], NUM0, bold=True)
    putf(wsBS, f'{c}9', f"={A['debt']}", IN['debt_fy25'], NUM0, green=True)
    putf(wsBS, f'{c}10', "=D10", EQG['derived_liabilities'] - IN['debt_fy25'], NUM0)
    putf(wsBS, f'{c}11', f"={c}9+{c}10", EQG['derived_liabilities'], NUM0)
    putf(wsBS, f'{c}12', f"={prev}12+'Income Statement'!{c}13-'Income Statement'!{c}15",
         F['equity'][i], NUM0, bold=True)
    putf(wsBS, f'{c}13', f"={c}9-{c}7", IN['debt_fy25'] - F['cash'][i], NUM0)
    putf(wsBS, f'{c}14', f"={c}12/{A['shares']}", F['equity'][i] / SH, PX)
    putf(wsBS, f'{c}15', f"='Income Statement'!{c}13/{c}12", F['pat'][i] / F['equity'][i], PCT)
band(wsBS, 17, 10); wsBS['A17'] = 'BALANCE-SHEET TRIANGULATION — THE DISAGREEMENT IS SHOWN, NOT SMOOTHED'
TRB = [('Total assets, as reported', 'B18', f"={A['ta25']}", IN['ta_fy25']),
       ('Total equity, as reported', 'B19', f"={A['eq25']}", IN['eq_fy25_rep']),
       ('Total liabilities DERIVED as assets less equity — carried', 'B20', "=B18-B19",
        EQG['derived_liabilities']),
       ('Total liabilities as printed by a second aggregation', 'B21', f"={A['tlalt']}",
        IN['tl_alt']),
       ('Gap between the two', 'B22', "=B20-B21", EQG['derived_liabilities'] - IN['tl_alt']),
       ('Gap as a share of total assets', 'B23', "=B22/B18",
        (EQG['derived_liabilities'] - IN['tl_alt']) / IN['ta_fy25'])]
for lab, ad, fm, ex in TRB:
    wsBS.cell(row=int(ad[1:]), column=1, value=lab)
    putf(wsBS, ad, fm, ex, PCT if ad == 'B23' else NUM0, bold=(ad == 'B20'))
note(wsBS, 25, 'FY2023 and FY2024 balance sheets are not retrievable at the evidentiary standard used elsewhere')
note(wsBS, 26, 'and are therefore left blank rather than reconstructed. The FY2025 column is the disclosed')
note(wsBS, 27, 'position; property and working capital within it are the estimates built on the Unit Build sheet,')
note(wsBS, 28, 'and they sum to total assets by construction because cash and total assets are both disclosed.')

# ============ 8 CASH FLOW =====================================================
wsC = sheet('Cash Flow')
title(wsC, 'Cash flow — linked to the valuation waterfall', 'EGP mn', 8, 50, 14)
hdr(wsC, 4, [''] + YF)
CFL = ['Profit after tax', 'Add back depreciation', 'Less change in working capital',
       'Cash from operations', 'Capital expenditure', 'Free cash flow to equity',
       'Dividends paid', 'Net change in cash', 'Closing cash',
       'Memo: free cash flow to the firm (from the DCF sheet)']
for j, l in enumerate(CFL):
    wsC.cell(row=5 + j, column=1, value=l)
for i in range(5):
    c = DC[i]
    ic = FC[i]
    putf(wsC, f'{c}5', f"='Income Statement'!{ic}13", F['pat'][i], NUM0, green=True)
    putf(wsC, f'{c}6', f"=DCF!{c}8", F['dna'][i], NUM0, green=True)
    putf(wsC, f'{c}7', f"=DCF!{c}14", -F['dwc'][i], NUM0, green=True)
    putf(wsC, f'{c}8', f"={c}5+{c}6+{c}7", F['pat'][i] + F['dna'][i] - F['dwc'][i], NUM0,
         bold=True)
    putf(wsC, f'{c}9', f"=DCF!{c}13", -F['capex'][i], NUM0, green=True)
    putf(wsC, f'{c}10', f"={c}8+{c}9",
         F['pat'][i] + F['dna'][i] - F['dwc'][i] - F['capex'][i], NUM0, bold=True)
    putf(wsC, f'{c}11', f"=-'Income Statement'!{ic}15", -F['dividends'][i], NUM0)
    putf(wsC, f'{c}12', f"={c}10+{c}11",
         F['pat'][i] + F['dna'][i] - F['dwc'][i] - F['capex'][i] - F['dividends'][i], NUM0)
    putf(wsC, f'{c}13', f"='Balance Sheet'!{ic}7", F['cash'][i], NUM0, green=True)
    putf(wsC, f'{c}14', f"=DCF!{c}15", F['fcff'][i], NUM0, green=True)
note(wsC, 16, 'The cash flow does not restate the model — it LINKS to it. Every line here points at the DCF or')
note(wsC, 17, 'Income Statement sheet, so the statement and the valuation cannot disagree by construction.')
note(wsC, 18, 'Free cash flow to the FIRM excludes treasury income; free cash flow to EQUITY includes it through')
note(wsC, 19, 'profit after tax. The cash balance is the one on the balance sheet, and closes to it exactly.')

# ============ 9 SUMMARY FINANCIALS ============================================
wsSF = sheet('Summary Financials')
title(wsSF, 'Summary financials — eight years on one screen', 'EGP mn', 10, 44, 13)
hdr(wsSF, 4, [''] + YH + YF)
SFL = [('Revenue', 'Income Statement', 5), ('EBITDA', 'Income Statement', 6),
       ('EBITDA margin', 'Income Statement', 7), ('EBIT', 'Income Statement', 9),
       ('Profit after tax', 'Income Statement', 13),
       ('Earnings per share (EGP)', 'Income Statement', 14),
       ('Despatched volume (Mt)', 'Income Statement', 16),
       ('Realised price (EGP/t)', 'Income Statement', 17)]
allc = HC + FC
vals = dict(zip([s[0] for s in SFL], [
    H['revenue'] + F['revenue'], H['ebitda'] + F['ebitda'], H['margin'] + F['margin'],
    H['ebit'] + F['ebit'], H['pat'] + F['pat'], H['eps'] + F['eps'],
    H['volume_mt'] + F['volume_mt'], H['price_t'] + F['price_t']]))
for j, (lab, sh, row) in enumerate(SFL):
    wsSF.cell(row=5 + j, column=1, value=lab)
    for i, c in enumerate(allc):
        ft = PCT if 'margin' in lab else (PX if 'per share' in lab else
                                          (NUM3 if 'Mt' in lab else NUM0))
        putf(wsSF, f'{c}{5+j}', f"='{sh}'!{c}{row}", vals[lab][i], ft, green=True)
band(wsSF, 14, 10); wsSF['A14'] = 'GROWTH'
for j, (lab, src) in enumerate([('Revenue growth', 5), ('EBITDA growth', 6),
                                ('Profit growth', 9)]):
    wsSF.cell(row=15 + j, column=1, value=lab)
    for i in range(1, 8):
        base = vals[['Revenue', 'EBITDA', 'Profit after tax'][j]]
        putf(wsSF, f'{allc[i]}{15+j}', f"={allc[i]}{src}/{allc[i-1]}{src}-1",
             base[i] / base[i - 1] - 1, PCT)
note(wsSF, 20, 'Every cell on this sheet is a link or a formula. Nothing is restated.')

# ============ 10 PER-SHARE & RATIOS ===========================================
wsR = sheet('Per-Share & Ratios')
title(wsR, 'Per-share figures and ratios — all formulas', None, 10, 46, 13)
hdr(wsR, 4, [''] + YH + YF)
RL = ['Earnings per share (EGP)', 'Dividend per share (EGP)', 'Book value per share (EGP)',
      'Price / earnings (at spot)', 'Dividend yield (at spot)',
      'Price / book (at spot)', 'EBITDA per tonne (EGP)', 'Net (cash) / EBITDA',
      'Return on equity']
for j, l in enumerate(RL):
    wsR.cell(row=5 + j, column=1, value=l)
for i, c in enumerate(allc):
    hist = i < 3
    putf(wsR, f'{c}5', f"='Income Statement'!{c}14", (H['eps'] + F['eps'])[i], PX, green=True)
    if i >= 1:
        dv = [0, IN['div_fy24_total'] / SH, IN['div_fy25_total'] / SH][i] if hist else F['dps'][i - 3]
        putf(wsR, f'{c}6', f"='Income Statement'!{c}18", dv, PX, green=True)
    if not hist:
        putf(wsR, f'{c}7', f"='Balance Sheet'!{c}14", F['equity'][i - 3] / SH, PX, green=True)
    elif i == 2:
        putf(wsR, f'{c}7', "='Balance Sheet'!D14", LN['bvps'], PX, green=True)
    putf(wsR, f'{c}8', f"={A['spot']}/{c}5", SPOT / (H['eps'] + F['eps'])[i], MULT)
    if i >= 1:
        dv = [0, IN['div_fy24_total'] / SH, IN['div_fy25_total'] / SH][i] if hist else F['dps'][i - 3]
        putf(wsR, f'{c}9', f"={c}6/{A['spot']}", dv / SPOT, PCT)
    if not hist or i == 2:
        bv = LN['bvps'] if i == 2 else F['equity'][i - 3] / SH
        putf(wsR, f'{c}10', f"={A['spot']}/{c}7", SPOT / bv, MULT)
    putf(wsR, f'{c}11', f"='Income Statement'!{c}6/'Income Statement'!{c}16",
         (H['ebitda'] + F['ebitda'])[i] / (H['volume_mt'] + F['volume_mt'])[i], NUM0)
    if not hist or i == 2:
        nd = DCF['net_debt_bs'] if i == 2 else IN['debt_fy25'] - F['cash'][i - 3]
        putf(wsR, f'{c}12', f"='Balance Sheet'!{c}13/'Income Statement'!{c}6",
             nd / (H['ebitda'] + F['ebitda'])[i], MULT)
        putf(wsR, f'{c}13', f"='Balance Sheet'!{c}15",
             LN['roe_sust'] if i == 2 else F['pat'][i - 3] / F['equity'][i - 3], PCT,
             green=True)
note(wsR, 15, 'Historical book value, net cash and return on equity are shown only for FY2025, the one year')
note(wsR, 16, 'with a retrievable balance sheet. Ratios at spot use the 06-Aug-2026 close on Assumptions.')
band(wsR, 18, 10); wsR['A18'] = 'RECONCILIATIONS — THE SHARE COUNT, THE EARNINGS PER SHARE, AND THE RUN RATE'
REC = [('Shares implied by the FY2024 distribution (total / per share)', 'B19',
        f"={A['div24']}/{A['dps24']}", SHT['from_fy24_distribution'], NUM2),
       ('Shares implied by the FY2025 distribution (total / per share)', 'B20',
        f"={A['div25']}/{A['dps25']}", SHT['from_fy25_distribution'], NUM2),
       ('Shares as quoted — ADOPTED', 'B21', f"={A['shares']}", SH, NUM2),
       ('Spread between the widest and narrowest route', 'B22',
        "=MAX(B19:B21)/MIN(B19:B21)-1", SHT['spread'], '0.000%'),
       ('Attributable profit implied by the disclosed earnings per share', 'B23',
        f"={A['eps25']}*{A['shares']}", IN['eps_fy25'] * SH, NUM0),
       ('Attributable profit as disclosed', 'B24', f"={A['pat25']}", IN['pat_fy25'], NUM0),
       ('Difference — the employees\' and directors\' statutory profit share', 'B25',
        "=B24-B23", IN['pat_fy25'] - IN['eps_fy25'] * SH, NUM0),
       ('  as a share of attributable profit', 'B26', "=B25/B24",
        (IN['pat_fy25'] - IN['eps_fy25'] * SH) / IN['pat_fy25'], PCT),
       ('Q1-2026 revenue growth on Q1-2025', 'B27',
        f"={A['revq126']}/{A['revq125']}-1", IN['rev_q1_26'] / IN['rev_q1_25'] - 1, PCT),
       ('FY2026 revenue implied by holding that growth rate', 'B28',
        f"={A['rev25']}*{A['revq126']}/{A['revq125']}",
        IN['rev_fy25'] * IN['rev_q1_26'] / IN['rev_q1_25'], NUM0),
       ('FY2026 revenue this model forecasts', 'B29', "=DCF!B5", F['revenue'][0], NUM0),
       ('The forecast against the run rate', 'B30', "=B29/B28-1",
        F['revenue'][0] / (IN['rev_fy25'] * IN['rev_q1_26'] / IN['rev_q1_25']) - 1, PCT),
       ('Q1-2026 attributable profit, annualised at four times', 'B31',
        f"=4*{A['patq126']}", 4 * IN['pat_q1_26'], NUM0),
       ('FY2026 profit this model forecasts', 'B32', "='Income Statement'!E13",
        F['pat'][0], NUM0),
       ('The forecast against the annualised first quarter', 'B33', "=B32/B31-1",
        F['pat'][0] / (4 * IN['pat_q1_26']) - 1, PCT)]
for lab, ad, fm, ex, ft in REC:
    wsR.cell(row=int(ad[1:]), column=1, value=lab)
    putf(wsR, ad, fm, ex, ft, bold=(ad in ('B21', 'B22')),
         green=(ad in ('B29', 'B32')))
note(wsR, 35, 'Three independent routes to the share count agree to within a fifth of one percent, which is why')
note(wsR, 36, 'the count is treated as known rather than estimated. The first-quarter run rate is shown because a')
note(wsR, 37, 'forecast that cannot be reconciled with the most recent actual quarter is not a forecast.')

# ============ 11 RELATIVE & NORMALIZED ========================================
wsN = sheet('Relative & Normalized')
title(wsN, 'Relative multiples and normalised earnings power', None, 7, 56, 16)
band(wsN, 4, 7); wsN['A4'] = 'NORMALISED EARNINGS BASE'
NB = [('FY2025 revenue (the cyclical peak)', 'B5', f"={A['rev25']}", IN['rev_fy25'], NUM0),
      ('Haircut to the revenue base', 'B6', f"={A['nhc']}", IN['norm_rev_haircut'], PCT),
      ('Normalised revenue', 'B7', "=B5*B6", IN['rev_fy25'] * IN['norm_rev_haircut'], NUM0),
      ('Mid-cycle EBITDA margin', 'B8', f"={A['nmgn']}", IN['norm_mgn'], PCT),
      ('Normalised EBITDA', 'B9', "=B7*B8", LN['ebitda_norm'], NUM0),
      ('Less depreciation', 'B10', "=-'Unit Build'!B48", -DNAT['adopted'], NUM0),
      ('Normalised EBIT', 'B11', "=B9+B10", LN['ebitda_norm'] - DNAT['adopted'], NUM0),
      ('Normalised NOPAT', 'B12', "=B11*(1-DCF!$C$47)", LN['nopat_norm'], NUM0),
      ('Memo: FY2025 EBITDA margin actually earned', 'B13', "='Unit Build'!B37",
       BU[0]['mgn'], PCT)]
for lab, ad, fm, ex, ft in NB:
    wsN.cell(row=int(ad[1:]), column=1, value=lab)
    putf(wsN, ad, fm, ex, ft, bold=(ad in ('B9', 'B12')))
band(wsN, 15, 7); wsN['A15'] = 'RELATIVE LENS — EV/EBITDA ON NORMALISED EARNINGS'
RLN = [('Justified EV/EBITDA', 'B16', f"={A['eveb']}", IN['ev_ebitda_just'], MULT),
       ('Implied enterprise value', 'B17', "=B9*B16", LN['ebitda_norm'] * IN['ev_ebitda_just'], NUM0),
       ('Plus net cash', 'B18', "=DCF!B36", DCF['net_cash'], NUM0),
       ('Less non-controlling interests', 'B19', "=DCF!B37", -IN['nci'], NUM0),
       ('Equity value', 'B20', "=B17+B18+B19",
        LN['ebitda_norm'] * IN['ev_ebitda_just'] + DCF['net_cash'] - IN['nci'], NUM0),
       ('Value per share (EGP)', 'B21', f"=B20/{A['shares']}", LN['values']['Relative multiples'], PX)]
for lab, ad, fm, ex, ft in RLN:
    wsN.cell(row=int(ad[1:]), column=1, value=lab)
    putf(wsN, ad, fm, ex, ft, bold=(ad == 'B21'), green=(ad in ('B18', 'B19')))
band(wsN, 23, 7); wsN['A23'] = 'NORMALISED-EARNINGS LENS'
NLN = [('Justified price / earnings', 'B24', f"={A['pej']}", IN['pe_just'], MULT),
       ('Capitalised operating earnings', 'B25', "=B12*B24", LN['nopat_norm'] * IN['pe_just'], NUM0),
       ('Plus net cash, at FACE', 'B26', "=DCF!B36", DCF['net_cash'], NUM0),
       ('Less non-controlling interests', 'B27', "=DCF!B37", -IN['nci'], NUM0),
       ('Equity value', 'B28', "=B25+B26+B27",
        LN['nopat_norm'] * IN['pe_just'] + DCF['net_cash'] - IN['nci'], NUM0),
       ('Value per share (EGP)', 'B29', f"=B28/{A['shares']}", LN['values']['Normalised earnings'], PX)]
for lab, ad, fm, ex, ft in NLN:
    wsN.cell(row=int(ad[1:]), column=1, value=lab)
    putf(wsN, ad, fm, ex, ft, bold=(ad == 'B29'), green=(ad in ('B26', 'B27')))
note(wsN, 31, 'Cash is added at FACE in both lenses rather than capitalised at the operating multiple. Cash is')
note(wsN, 32, 'worth cash; capitalising it at seven times would value a pound of treasury at a discount to itself.')

# ============ 12 FUNDAMENTAL VALUATION ========================================
wsFV = sheet('Fundamental Valuation')
title(wsFV, 'Asset lens, and the choices that were contested', None, 7, 58, 15)
band(wsFV, 4, 7); wsFV['A4'] = 'ASSET / REPLACEMENT-COST LENS'
AL = [('Cement capacity (Mt/yr)', 'B5', f"={A['capcem']}", IN['cap_cement_mt'], NUM2),
      ('Replacement cost per annual tonne (USD)', 'B6', f"={A['repl']}", IN['repl_usd_t'], NUM0),
      ('Justified enterprise value per annual tonne (USD)', 'B7', f"={A['evt']}",
       IN['ev_t_just'], NUM0),
      ('Discount to replacement cost', 'B8', "=B7/B6-1", IN['ev_t_just'] / IN['repl_usd_t'] - 1, PCT),
      ('Implied enterprise value (EGP mn)', 'B9', f"=B7*B5*{A['fx']}", LN['ev_asset'], NUM0),
      ('Plus net cash', 'B10', "=DCF!B36", DCF['net_cash'], NUM0),
      ('Less non-controlling interests', 'B11', "=DCF!B37", -IN['nci'], NUM0),
      ('Equity value', 'B12', "=B9+B10+B11",
       LN['ev_asset'] + DCF['net_cash'] - IN['nci'], NUM0),
      ('Value per share (EGP)', 'B13', f"=B12/{A['shares']}", LN['values']['Asset / replacement cost'], PX),
      ('Memo: what the MARKET is paying per annual tonne (USD)', 'B14',
       f"=({A['spot']}*{A['shares']}-DCF!B36+{A['nci']})/{A['capcem']}/{A['fx']}",
       LN['ev_per_t_spot'], NUM1)]
for lab, ad, fm, ex, ft in AL:
    wsFV.cell(row=int(ad[1:]), column=1, value=lab)
    putf(wsFV, ad, fm, ex, ft, bold=(ad == 'B13'), green=(ad in ('B10', 'B11')))
band(wsFV, 16, 7); wsFV['A16'] = 'CONTESTED CHOICES — EACH COMPUTED, NOT ARGUED'
hdr(wsFV, 17, ['Choice', 'Adopted', 'Alternative', 'Fair value adopted',
               'Fair value alternative', 'Effect'])
for j, c in enumerate(CON):
    r = 18 + j
    wsFV.cell(row=r, column=1, value=c['choice']).alignment = Alignment(wrap_text=True,
                                                                       vertical='top')
    wsFV.cell(row=r, column=2, value=c['adopted'])
    wsFV.cell(row=r, column=3, value=c['alternative'])
    putf(wsFV, f'D{r}', "=DCF!$B$40", c['fv_adopted'], PX, green=True)
    put(wsFV, f'E{r}', c['fv_alternative'], BLUE, PX)
    putf(wsFV, f'F{r}', f"=E{r}/D{r}-1", c['effect'], PCT)
wsFV.column_dimensions['B'].width = 22
wsFV.column_dimensions['C'].width = 22
note(wsFV, 23, 'The alternative fair values in column E are whole-model re-runs — class 3 pasted cells. Each one')
note(wsFV, 24, 'is a complete revaluation at a different assumption and cannot be a formula in a grid. The EFFECT')
note(wsFV, 25, 'column is a live formula against the adopted value, so it moves when the model does.')
band(wsFV, 27, 7); wsFV['A27'] = 'TERMINAL-GROWTH RECONCILIATION'
TGR = [('Profit growth achieved since FY2022 (compound)', 'B28', None,
        TR['pat_cagr_since_fy22'], PCT),
       ('FY2025 revenue as a share of Egyptian nominal output', 'B29',
        f"={A['rev25']}/{IN['egy_gdp_egp_bn']*1000}", TR['share_of_gdp'], '0.0000%'),
       ('Years until that growth rate equals the whole economy', 'B30', None,
        TR['crossover_years'], NUM1),
       ('Terminal return on invested capital', 'B31', "=DCF!B24", TR['roic_repl'], PCT),
       ('Terminal rate', 'B32', "=DCF!$C$46", W['wacc_term'], PCT),
       ('Reinvestment rate that terminal growth requires', 'B33', "=DCF!B25", TR['rr_repl'], PCT),
       ('Terminal growth adopted', 'B34', f"={A['g']}", IN['g_term'], PCT)]
for lab, ad, fm, ex, ft in TGR:
    wsFV.cell(row=int(ad[1:]), column=1, value=lab)
    if fm:
        putf(wsFV, ad, fm, ex, ft, green=ad in ('B31', 'B32', 'B33'))
    else:
        put(wsFV, ad, ex, BLUE, ft)
note(wsFV, 36, 'Terminal return on capital sits BELOW the terminal rate, so faster terminal growth LOWERS the')
note(wsFV, 37, 'valuation rather than raising it. That is visible in the growth column of the Sensitivity sheet.')

# ============ 13 SUMMARY ======================================================
wsS = sheet('Summary')
title(wsS, 'Summary valuation table', 'Every value linked live from its own sheet.',
      7, 40, 18)
hdr(wsS, 4, ['Lens', 'Value per share (EGP)', 'Weight', 'Weighted contribution',
             'Versus spot', 'Terminal value % of EV'])
LK = [('DCF (cash flow)', "=DCF!B40", A['wdcf'], "=DCF!B33"),
      ('Relative multiples', "='Relative & Normalized'!B21", A['wrel'], None),
      ('Normalised earnings', "='Relative & Normalized'!B29", A['wnorm'], None),
      ('Asset / replacement cost', "='Fundamental Valuation'!B13", A['wasset'], None)]
for j, (name, fm, wkey, tvfm) in enumerate(LK):
    r = 5 + j
    wsS.cell(row=r, column=1, value=name)
    putf(wsS, f'B{r}', fm, LN['values'][name], PX, green=True, bold=True)
    putf(wsS, f'C{r}', f"={wkey}", LN['weights'][name], PCT, green=True)
    putf(wsS, f'D{r}', f"=B{r}*C{r}", LN['values'][name] * LN['weights'][name], PX)
    putf(wsS, f'E{r}', f"=B{r}/{A['spot']}-1", LN['values'][name] / SPOT - 1, PCT)
    if tvfm:
        putf(wsS, f'F{r}', tvfm, DCF['tv_share'], PCT, green=True, bold=True)
    else:
        wsS.cell(row=r, column=6, value='—')
wsS.cell(row=9, column=1, value='WEIGHTED CENTRAL FAIR VALUE')
putf(wsS, 'B9', "=SUMPRODUCT(B5:B8,C5:C8)", LN['central'], PX, bold=True)
putf(wsS, 'C9', "=SUM(C5:C8)", 1.0, PCT, bold=True)
putf(wsS, 'D9', "=SUM(D5:D8)", LN['central'], PX, bold=True)
putf(wsS, 'E9', f"=B9/{A['spot']}-1", LN['central'] / SPOT - 1, PCT, bold=True)
wsS.cell(row=10, column=1, value='Lowest lens')
putf(wsS, 'B10', "=MIN(B5:B8)", LN['low'], PX)
putf(wsS, 'E10', f"=B10/{A['spot']}-1", LN['low'] / SPOT - 1, PCT)
wsS.cell(row=11, column=1, value='Highest lens')
putf(wsS, 'B11', "=MAX(B5:B8)", LN['high'], PX)
putf(wsS, 'E11', f"=B11/{A['spot']}-1", LN['high'] / SPOT - 1, PCT)
wsS.cell(row=12, column=1, value='Market price, 6 August 2026')
putf(wsS, 'B12', f"={A['spot']}", SPOT, PX, green=True)
wsS.cell(row=13, column=1, value='Market capitalisation (EGP mn)')
putf(wsS, 'B13', "=DCF!C42", M['mktcap'], NUM0, green=True)
band(wsS, 15, 7); wsS['A15'] = 'THE THREE-PANEL VALUATIONS'
hdr(wsS, 16, ['', 'Low (EGP)', 'Central (EGP)', 'High (EGP)', 'Versus spot'])
for j, e in enumerate(D['experts']):
    r = 17 + j
    wsS.cell(row=r, column=1, value=f"{e['label']} — {e['method']}")
    for k, col in enumerate(['B', 'C', 'D']):
        put(wsS, f'{col}{r}', e[['low', 'central', 'high'][k]], BLUE, PX)
    putf(wsS, f'E{r}', f"=C{r}/{A['spot']}-1", e['central'] / SPOT - 1, PCT)
wsS.cell(row=20, column=1, value='Panel median')
putf(wsS, 'C20', "=MEDIAN(C17:C19)", sorted(e['central'] for e in D['experts'])[1], PX, bold=True)
putf(wsS, 'E20', f"=C20/{A['spot']}-1", sorted(e['central'] for e in D['experts'])[1] / SPOT - 1, PCT)
note(wsS, 22, 'Terminal value as a percentage of enterprise value is shown beside the cash-flow lens and links')
note(wsS, 23, 'live to the DCF sheet — it is never typed. The three panel valuations are whole-model re-runs on')
note(wsS, 24, 'different methods and are pasted; the versus-spot column beside them is a formula.')

# ============ 14 MONTE CARLO ==================================================
wsM = sheet('Monte Carlo')
title(wsM, 'Probabilistic price map — ILLUSTRATIVE ONLY',
      'Percentiles are the output of a 50,000-path simulation: pasted, class 2.', 7, 44, 16)
note(wsM, 3, 'This map is NOT a valuation. It is a distribution of where the SHARE PRICE could sit, drawn from')
note(wsM, 4, 'the price history alone. It does not redraw when a valuation driver changes.')
hdr(wsM, 6, ['', 'One month', 'Three months'])
PCTL = [('5th percentile', 'p5'), ('25th percentile', 'p25'), ('Median', 'p50'),
        ('75th percentile', 'p75'), ('95th percentile', 'p95')]
for j, (lab, key) in enumerate(PCTL):
    r = 7 + j
    wsM.cell(row=r, column=1, value=lab)
    put(wsM, f'B{r}', STK['horizons']['1M']['pct'][key], BLUE, PX)
    put(wsM, f'C{r}', STK['horizons']['3M']['pct'][key], BLUE, PX)
wsM.cell(row=12, column=1, value='Spot')
putf(wsM, 'B12', f"={A['spot']}", SPOT, PX, green=True)
putf(wsM, 'C12', f"={A['spot']}", SPOT, PX, green=True)
for j, (lab, key) in enumerate([('Probability of finishing above spot', 'p_above'),
                                ('Probability of finishing 10% or more above', 'p_up10'),
                                ('Probability of finishing 10% or more below', 'p_dn10'),
                                ('Probability of TOUCHING +10% at any point', 'touch_up10'),
                                ('Probability of TOUCHING -10% at any point', 'touch_dn10')]):
    r = 14 + j
    wsM.cell(row=r, column=1, value=lab)
    put(wsM, f'B{r}', STK['horizons']['1M'][key], BLUE, PCT)
    put(wsM, f'C{r}', STK['horizons']['3M'][key], BLUE, PCT)
wsM.cell(row=20, column=1, value='Median versus spot')
putf(wsM, 'B20', "=B9/B12-1", STK['horizons']['1M']['pct']['p50'] / SPOT - 1, PCT)
putf(wsM, 'C20', "=C9/C12-1", STK['horizons']['3M']['pct']['p50'] / SPOT - 1, PCT)
wsM.cell(row=21, column=1, value='Width of the 5th-95th band, as % of spot')
putf(wsM, 'B21', "=(B11-B7)/B12", (STK['horizons']['1M']['pct']['p95'] -
                                   STK['horizons']['1M']['pct']['p5']) / SPOT, PCT)
putf(wsM, 'C21', "=(C11-C7)/C12", (STK['horizons']['3M']['pct']['p95'] -
                                   STK['horizons']['3M']['pct']['p5']) / SPOT, PCT)
band(wsM, 23, 7); wsM['A23'] = 'HOW WELL CALIBRATED IS THIS MAP? — MEASURED, NOT ASSERTED'
CAL = [('Windows scored', S0['windows_scored'], NUM0),
       ('Skill against a random walk', S0['skill_norm'], PCT),
       ('Coverage of the 50% band (nominal 50%)', S0['cov50'], PCT),
       ('Coverage of the 80% band (nominal 80%)', S0['cov80'], PCT),
       ('Coverage of the 90% band (nominal 90%)', S0['cov90'], PCT),
       ('Cone width against the benchmark', S0['w90_ratio'], MULT)]
for j, (lab, v, ft) in enumerate(CAL):
    r = 24 + j
    wsM.cell(row=r, column=1, value=lab)
    put(wsM, f'B{r}', v, BLUE, ft)
note(wsM, 31, 'The bands cover MORE than their nominal share, so the map is too wide rather than mis-centred.')
note(wsM, 32, 'It is carried as illustrative only and no valuation conclusion rests on it.')

# ============ 15 SENSITIVITY ==================================================
wsX = sheet('Sensitivity')
title(wsX, 'Sensitivity — whole-model re-runs (class 3, pasted)',
      'Each cell is a complete revaluation. THESE GRIDS DO NOT REDRAW.', 7, 44, 14)
wsX['A4'] = 'Fair value per share (EGP): explicit-window cost of capital against terminal growth'
wsX['A4'].font = Font(bold=True)
hdr(wsX, 5, [''] + [f'g = {g:.0%}' for g in SN['g_grid']])
for i, wv in enumerate(SN['wacc_grid']):
    r = 6 + i
    put(wsX, f'A{r}', wv, BLUE, PCT2)
    for j in range(5):
        put(wsX, f'{DC[j]}{r}', SN['wacc_g'][i][j], BLUE, PX)
wsX['A12'] = 'Fair value per share (EGP): explicit-window rate against TERMINAL rate'
wsX['A12'].font = Font(bold=True)
hdr(wsX, 13, [''] + [f'terminal {w:.1%}' for w in SN['wt_grid']])
for i, wv in enumerate(SN['wacc_grid']):
    r = 14 + i
    put(wsX, f'A{r}', wv, BLUE, PCT2)
    for j in range(5):
        put(wsX, f'{DC[j]}{r}', SN['exp_term'][i][j], BLUE, PX)
wsX['A20'] = 'Fair value per share (EGP): beta'
wsX['A20'].font = Font(bold=True)
hdr(wsX, 21, [''] + [f'{b:.2f}' for b in SN['beta_grid']])
wsX['A22'] = 'Fair value'
for j in range(5):
    put(wsX, f'{DC[j]}22', SN['beta'][j], BLUE, PX)
wsX['A24'] = 'Fair value per share (EGP): shift in the EBITDA margin, every forecast year'
wsX['A24'].font = Font(bold=True)
hdr(wsX, 25, [''] + [f'{m:+.0%}' for m in SN['mgn_grid']])
wsX['A26'] = 'Fair value'
for j in range(5):
    put(wsX, f'{DC[j]}26', SN['mgn'][j], BLUE, PX)
wsX['A28'] = 'Fair value per share (EGP): net cash at the valuation date (EGP mn)'
wsX['A28'].font = Font(bold=True)
hdr(wsX, 29, [''] + [f'{x:,.0f}' for x in SN['nc_grid']])
wsX['A30'] = 'Fair value'
for j in range(5):
    put(wsX, f'{DC[j]}30', SN['net_cash'][j], BLUE, PX)
note(wsX, 32, 'Note the growth column of the first grid: HIGHER terminal growth gives a LOWER value, because the')
note(wsX, 33, 'terminal return on capital sits below the terminal rate. That is the model being consistent, not a')
note(wsX, 34, 'sign error. Beta is varied over the fixed comparability anchors 0.60 / 0.80 / 1.00 / 1.15 / 1.30,')
note(wsX, 35, 'which span the regression\'s own confidence interval.')

# ============ 16 PEER & SECTOR ================================================
wsP = sheet('Peer & Sector')
title(wsP, 'Peer set and the Egyptian cement balance', None, 8, 44, 15)
hdr(wsP, 4, ['', 'Revenue (EGP mn)', 'Profit (EGP mn)', 'Market cap (EGP mn)',
             'Price / earnings', 'Price / sales', 'Net margin'])
PRW = [('Arabian Cement (ARCC)', A['rev25'], A['pat25'], "=DCF!C42", PE['self']),
       ('Sinai Cement (SCEM)', A['pscrev'], A['pscpat'], f"={A['pscmc']}", PE['scem']),
       ('Misr Beni Suef Cement (MBSC)', A['pmbrev'], A['pmbpat'], f"={A['pmbmc']}", PE['mbsc'])]
for j, (name, rk, pk, mfm, d) in enumerate(PRW):
    r = 5 + j
    wsP.cell(row=r, column=1, value=name)
    putf(wsP, f'B{r}', f"={rk}", d['rev'], NUM0, green=True)
    putf(wsP, f'C{r}', f"={pk}", d['pat'], NUM0, green=True)
    putf(wsP, f'D{r}', mfm, d['mcap'], NUM0, green=True)
    putf(wsP, f'E{r}', f"=D{r}/C{r}", d['pe'], MULT)
    putf(wsP, f'F{r}', f"=D{r}/B{r}", d['ps'], MULT)
    putf(wsP, f'G{r}', f"=C{r}/B{r}", d['pat'] / d['rev'], PCT)
wsP.cell(row=9, column=1, value='Peer average price / earnings (excluding the subject)')
putf(wsP, 'E9', "=AVERAGE(E6:E7)", (PE['scem']['pe'] + PE['mbsc']['pe']) / 2, MULT, bold=True)
wsP.cell(row=10, column=1, value='Subject premium / (discount) to the peer average')
putf(wsP, 'E10', "=E5/E9-1", PE['self']['pe'] / ((PE['scem']['pe'] + PE['mbsc']['pe']) / 2) - 1,
     PCT)
band(wsP, 12, 8); wsP['A12'] = 'THE EGYPTIAN CEMENT BALANCE'
SEC = [('Nameplate capacity (Mt)', 'B13', f"={A['egcap']}", PE['sector']['capacity_mt'], NUM1),
       ('Production 2025 (Mt)', 'B14', f"={A['egprod']}", PE['sector']['production_mt'], NUM1),
       ('Domestic consumption 2025 (Mt)', 'B15', f"={A['egcons']}", PE['sector']['consumption_mt'], NUM1),
       ('Exports 2025 (Mt)', 'B16', f"={A['egexp']}", PE['sector']['exports_mt'], NUM1),
       ('Dormant capacity under revival (Mt)', 'B17', f"={A['egrev']}", PE['sector']['revival_mt'], NUM1),
       ('Sector utilisation', 'B18', "=B14/B13", PE['sector']['utilisation'], PCT),
       ('The subject as a share of national capacity', 'B19', f"={A['capcem']}/B13",
        PE['sector']['share_of_capacity'], PCT),
       ('Revival capacity as a share of consumption', 'B20', "=B17/B15",
        PE['sector']['revival_pct_of_consumption'], PCT)]
for lab, ad, fm, ex, ft in SEC:
    wsP.cell(row=int(ad[1:]), column=1, value=lab)
    putf(wsP, ad, fm, ex, ft, green=(int(ad[1:]) <= 17))
note(wsP, 22, 'The Egyptian peer set is thin and its published multiples do not reconcile against the market')
note(wsP, 23, 'capitalisations printed beside them, which is why the relative lens carries only 20% of the weight.')
note(wsP, 24, 'Every multiple on this sheet is RECOMPUTED from revenue, profit and market capitalisation rather')
note(wsP, 25, 'than quoted.')

# ============ SAVE ============================================================
OUT = os.path.join(HERE, 'ARCC_Valuation_Model_06082026_public.xlsx')
wb.save(OUT)
with open(os.path.join(HERE, 'xlsx_expected.json'), 'w') as f:
    json.dump(EXPECT, f, indent=1)
nf = sum(len(v) for v in EXPECT.values())
nv = 0
from openpyxl import load_workbook
chk = load_workbook(OUT)
for s in chk.worksheets:
    for row in s.iter_rows():
        for c in row:
            if isinstance(c.value, str) and c.value.startswith('='):
                pass
            elif isinstance(c.value, (int, float)):
                nv += 1
print(f'wrote {os.path.basename(OUT)} — {len(wb.sheetnames)} sheets, '
      f'{nf} formula cells recorded, {nv} pasted numeric cells')
json.dump(dict(formulas=nf, pasted_values=nv, sheets=len(wb.sheetnames)),
          open(os.path.join(HERE, 'formula_count.json'), 'w'), indent=1)
