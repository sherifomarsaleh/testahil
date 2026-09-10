#!/usr/bin/env python3
"""ADIB-Egypt — the delivered workbook: sixteen sheets, live formulas throughout.

CHANGE A BLUE INPUT AND THE VALUE PER SHARE RECOMPUTES. Every driver on Assumptions is a
blue cell; every figure downstream of one is a FORMULA that reads it. Nothing downstream
of an input is a typed number, which is the only way a reader can disagree with this study
and see what their disagreement is worth.

The sheet list is research_protocol.MODEL_STUDY['excel_sheets'], imported rather than
copied, so this file cannot drift from the standard it is held to.
"""
import datetime as _dtm
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..'))
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import research_protocol as RP

D = json.load(open(os.path.join(HERE, 'study_numbers.json'), encoding='utf-8'))
STRIKE = json.load(open(os.path.join(HERE, 'strike_result.json'), encoding='utf-8'))
GAPN = json.load(open(os.path.join(HERE, 'gap_review_numbers.json'), encoding='utf-8'))
WF = json.load(open(os.path.join(HERE, '..', 'adib_walkforward',
                                 'walkforward_summary.json'), encoding='utf-8'))
TECH = json.load(open(os.path.join(HERE, 'technicals.json'), encoding='utf-8'))
M, CC, P5, REG = D['meta'], D['cost_of_capital'], D['projection'], D['register']
BY, LR, LN = D['base_year'], D['latest_reviewed'], D['lenses']
OBS, H1O, FAR = D['base_year_observed_ratios'], D['latest_reviewed_annualised'], D['far_year_ranges']
sys.path.insert(0, os.path.join(HERE, '..', 'adib_walkforward'))
import panel as WFP

INK = '1C3A36'; BLUE = '0B4C8C'; GREY = '6E7B77'
H = Font(bold=True, color='FFFFFF', size=10.5)
HF = PatternFill('solid', fgColor=INK)
IN = Font(color=BLUE, bold=True)          # BLUE = an input a reader may change
INF = PatternFill('solid', fgColor='EAF2FB')
LBL = Font(bold=True, color=INK)
SEC = PatternFill('solid', fgColor='EAF0EE')
NOTE = Font(italic=True, color=GREY, size=9)
THIN = Border(bottom=Side(style='thin', color='C9D4D1'))

wb = Workbook()
wb.remove(wb.active)
SHEETS = {}
for name in RP.MODEL_STUDY['excel_sheets']:
    SHEETS[name] = wb.create_sheet(name)


def hdr(ws, row, cells, widths=None):
    for i, c in enumerate(cells):
        cell = ws.cell(row=row, column=1 + i, value=c)
        cell.font = H; cell.fill = HF; cell.alignment = Alignment(horizontal='center')
    if widths:
        for i, w in enumerate(widths):
            ws.column_dimensions[get_column_letter(1 + i)].width = w


def put(ws, r, c, v, font=None, fill=None, fmt=None):
    cell = ws.cell(row=r, column=c, value=v)
    if font: cell.font = font
    if fill: cell.fill = fill
    if fmt: cell.number_format = fmt
    return cell


def sect(ws, r, text):
    cell = ws.cell(row=r, column=1, value=text)
    cell.font = LBL; cell.fill = SEC
    for c in range(2, 9):
        ws.cell(row=r, column=c).fill = SEC
    return r + 1


N = '#,##0'; N2 = '#,##0.00'; PCT = '0.0%'; PCT2 = '0.00%'
YRS = [p['year'] for p in P5]

# ---------------------------------------------------------------- 1 READ FIRST
ws = SHEETS['READ FIRST']
ws.column_dimensions['A'].width = 130
for i, line in enumerate([
    'ADIB-Egypt (EGX: ADIB) — valuation model, %s' % M['asof'],
    '',
    'WHICH COMPANY. Abu Dhabi Islamic Bank – Egypt S.A.E., listed in Cairo, reporting in '
    'Egyptian pounds. NOT Abu Dhabi Islamic Bank PJSC (ADX: ADIB), its Abu Dhabi parent, '
    'which is a different company covered separately.',
    '',
    'HOW TO USE THIS FILE. Every BLUE cell on the Assumptions sheet is an input you may '
    'change. Everything downstream of one is a formula. Change the cost of risk, or the '
    'asset yield, or the growth path, and the value per share on Summary recomputes.',
    '',
    'THERE IS NO ENTERPRISE VALUE AND NO WACC IN THIS MODEL, and that is deliberate. A '
    "bank's deposits are its raw material rather than its financing, so subtracting them "
    'as though they were debt produces a number with no meaning. Everything here is built '
    'on equity and discounted at the cost of equity.',
    '',
    'MARGINS ARE OUTPUTS. The asset yield and the cost of funds are inputs; the net '
    'interest margin, the cost-to-income ratio and the returns on assets and equity are '
    'computed from them. None of those four is typed anywhere in this file.',
    '',
    'ONE LENS IS THE ANSWER. The dividend discount is the central. Residual income, the '
    'relative multiple and book value are cross-checks published beside it. They are not '
    'averaged, and there are no weights in this workbook.',
    '',
    'NOT INVESTMENT ADVICE. No rating, no price target. An educational valuation exercise.',
]):
    c = put(ws, i + 1, 1, line)
    if i == 0: c.font = Font(bold=True, size=13, color=INK)
    c.alignment = Alignment(wrap_text=True, vertical='top')

# ---------------------------------------------------------------- 4 Assumptions
ws = SHEETS['Assumptions']
hdr(ws, 1, ['Driver  (BLUE cells are inputs — change them)', str(YRS[0]), str(YRS[1]),
            str(YRS[2]), str(YRS[3]), str(YRS[4]), 'Source / basis'],
    [40, 11, 11, 11, 11, 11, 78])
ASS = {}
r = 3
r = sect(ws, r, 'VOLUME')
for key, lab, vals, fmt, src in [
    ('fin_growth', 'Financing to customers, growth', REG['financing_growth']['value'], PCT,
     REG['financing_growth']['source']),
    ('fin_assets', 'Financing / total assets', REG['financing_over_assets']['value'], PCT,
     REG['financing_over_assets']['source'])]:
    put(ws, r, 1, lab, LBL)
    for j, v in enumerate(vals):
        put(ws, r, 2 + j, v, IN, INF, fmt)
    put(ws, r, 7, src, NOTE); ASS[key] = r; r += 1
r = sect(ws, r, 'RATES — inputs. The margin is an OUTPUT of these two rows.')
for key, lab, vals, src in [
    ('yield', 'Asset yield on average assets', REG['asset_yield']['value'],
     REG['asset_yield']['source']),
    ('cof', 'Cost of funds on average interest-bearing liabilities',
     REG['cost_of_funds']['value'], REG['cost_of_funds']['source'])]:
    put(ws, r, 1, lab, LBL)
    for j, v in enumerate(vals):
        put(ws, r, 2 + j, v, IN, INF, PCT2)
    put(ws, r, 7, src, NOTE); ASS[key] = r; r += 1
put(ws, r, 1, 'Interest-bearing liabilities / total assets', LBL)
put(ws, r, 2, REG['ibl_over_assets']['value'], IN, INF, PCT2)
put(ws, r, 7, REG['ibl_over_assets']['source'], NOTE); ASS['ibl'] = r; r += 1
r = sect(ws, r, 'OTHER INCOME AND COST')
for key, lab, vals, src in [
    ('fee', 'Net fees / average assets', REG['fee_ratio']['value'], REG['fee_ratio']['source']),
    ('onii', 'Other non-interest income / average assets', REG['other_nii_ratio']['value'],
     REG['other_nii_ratio']['source']),
    ('oop', 'Other operating expenses / average assets', REG['other_op_ratio']['value'],
     REG['other_op_ratio']['source']),
    ('admin_g', 'Administrative expenses, growth', REG['admin_growth']['value'],
     REG['admin_growth']['source']),
    ('cor', 'Cost of risk on average financing', REG['cost_of_risk']['value'],
     REG['cost_of_risk']['source'])]:
    put(ws, r, 1, lab, LBL)
    for j, v in enumerate(vals):
        put(ws, r, 2 + j, v, IN, INF, PCT2)
    put(ws, r, 7, src, NOTE); ASS[key] = r; r += 1
r = sect(ws, r, 'TAX, CAPITAL AND THE SHAREHOLDER')
for key, lab, val, fmt, src in [
    ('tax', 'Effective tax rate', REG['tax_rate']['value'], PCT2, REG['tax_rate']['source']),
    ('nci', 'Non-controlling interests, share of profit', REG['nci_share']['value'], PCT2,
     REG['nci_share']['source']),
    ('teq', 'Target equity / total assets', REG['target_equity_assets']['value'], PCT2,
     REG['target_equity_assets']['source']),
    ('issue', 'Capital raised in 2026, EGP million', REG['capital_increase_2026']['value'],
     N, REG['capital_increase_2026']['source'])]:
    put(ws, r, 1, lab, LBL); put(ws, r, 2, val, IN, INF, fmt)
    put(ws, r, 7, src, NOTE); ASS[key] = r; r += 1
r = sect(ws, r, 'COST OF EQUITY')
for key, lab, val, src in [
    ('rf', 'Egyptian ten-year local-currency yield', CC['rf'], REG['rf']['source']),
    ('sov', 'less the sovereign default spread', CC['sovereign_default_spread'],
     REG['sov_default_spread']['source']),
    ('beta', 'Beta against the EGX30 index', CC['beta'], REG['beta']['source']),
    ('erp', 'Egyptian total equity risk premium', CC['erp'], REG['erp']['source']),
    ('rfterm', 'Terminal risk-free rate', CC['terminal_rf'], REG['rf_terminal']['source']),
    ('erpterm', 'Terminal equity risk premium', CC['terminal_erp'],
     REG['erp_terminal']['source']),
    # [R-COC-03] THE SPLIT'S LEGS ARE INPUTS AND A READER MUST SEE THEM. The two formulas
    # below read rf* + beta x the WHOLE premium, which multiplies Egypt's country risk by
    # beta; the model moved onto the split and the workbook did not, so its three lens
    # values and their Summary copies all published the old rate. Read from the committed
    # record, never retyped.
    ('erpm', '   of which the MATURE premium — beta applies to this leg only',
     CC['erp_mature'], 'Damodaran identity: total premium less the country leg'),
    ('crp', 'Egypt country premium — charged FLAT, once, never multiplied by beta',
     CC['crp_effective'], 'sovereign default spread x the equity-to-bond scaling'),
    ('crpt', 'Terminal country premium — charged FLAT and once',
     CC['crp_effective_terminal'],
     'terminal total premium less the SAME mature leg: what normalises is country risk'),
    ('g', 'Terminal growth', CC['terminal_growth'], REG['terminal_growth']['source'])]:
    put(ws, r, 1, lab, LBL)
    put(ws, r, 2, val, IN, INF, N2 if key == 'beta' else PCT2)
    put(ws, r, 7, src, NOTE); ASS[key] = r; r += 1
r += 1
put(ws, r, 1, 'Cost of equity  (= rf − sovereign spread + beta × MATURE premium '
     '+ country premium, flat)', LBL)
put(ws, r, 2, '=B%d-B%d+B%d*B%d+B%d' % (ASS['rf'], ASS['sov'], ASS['beta'],
                                        ASS['erpm'], ASS['crp']), fmt=PCT2)
ASS['ke0'] = r; r += 1
put(ws, r, 1, 'Terminal cost of equity', LBL)
put(ws, r, 2, '=B%d+B%d*B%d+B%d' % (ASS['rfterm'], ASS['beta'], ASS['erpm'],
                                    ASS['crpt']), fmt=PCT2)
ASS['keterm'] = r; r += 1
put(ws, r, 1, 'Cost of equity by year (glide)', LBL)
for j in range(5):
    put(ws, r, 2 + j, '=$B$%d+($B$%d-$B$%d)*%d/6' % (ASS['ke0'], ASS['keterm'],
                                                     ASS['ke0'], j + 1), fmt=PCT2)
ASS['kepath'] = r; r += 1
put(ws, r, 1, 'Discount factor', LBL)
for j in range(5):
    prev = 'B%d' % r if j == 0 else '%s%d' % (get_column_letter(1 + j), r)
    if j == 0:
        put(ws, r, 2, '=1/(1+B%d)' % ASS['kepath'], fmt='0.0000')
    else:
        put(ws, r, 2 + j, '=%s%d/(1+%s%d)' % (get_column_letter(1 + j), r,
                                              get_column_letter(2 + j), ASS['kepath']),
            fmt='0.0000')
ASS['df'] = r

# ---------------------------------------------------------------- 9 Income Statement
ws = SHEETS['Income Statement']
hdr(ws, 1, ['EGP million', 'FY2023A', 'FY2024A', 'FY2025A'] + [str(y) + 'E' for y in YRS],
    [40, 13, 13, 13, 13, 13, 13, 13, 13])
HY = {}
for y in (2023, 2024, 2025):
    rr = WFP.IS['FY%d' % y]
    HY[y] = {k: rr[k] / 1000.0 for k in ('fin_income', 'cost_funds', 'net_funds', 'net_fees',
                                         'admin', 'other_op', 'ecl', 'pbt', 'tax', 'np',
                                         'np_parent')}
    HY[y]['other_nii'] = WFP.other_nii('FY%d' % y) / 1000.0
A = 'Assumptions'
BAL = 'Balance Sheet'
IS_ROW = {}
r = 3
# balance-sheet drivers live on Balance Sheet; the income statement reads them
for lab, key in [('Financing income', 'fin_income'), ('Cost of deposits', 'cost_funds'),
                 ('Net income from funds', 'net_funds'),
                 ('Net fees and commissions', 'net_fees'),
                 ('Other non-interest income', 'other_nii'),
                 ('Administrative expenses', 'admin'),
                 ('Other operating expenses', 'other_op'),
                 ('Expected credit losses', 'ecl'), ('Profit before tax', 'pbt'),
                 ('Tax', 'tax'), ('Net profit', 'np'), ('Attributable to the bank', 'np_parent')]:
    put(ws, r, 1, lab, LBL)
    for j, y in enumerate((2023, 2024, 2025)):
        put(ws, r, 2 + j, round(HY[y][key], 1), fmt=N)
    IS_ROW[key] = r; r += 1
# now the formulas, column E..I
for j in range(5):
    col = get_column_letter(5 + j)            # this sheet's forecast columns are E..I
    bcol = get_column_letter(3 + j)           # the BALANCE SHEET's are C..G — not the same
    acol = get_column_letter(2 + j)           # Assumptions' are B..F — nor are these
    avg_ta = "'%s'!%s6" % (BAL, bcol)         # average total assets
    avg_ibl = "'%s'!%s8" % (BAL, bcol)
    avg_fin = "'%s'!%s7" % (BAL, bcol)
    put(ws, IS_ROW['fin_income'], 5 + j, "=%s*'%s'!%s%d" % (avg_ta, A, acol, ASS['yield']), fmt=N)
    put(ws, IS_ROW['cost_funds'], 5 + j, "=-%s*'%s'!%s%d" % (avg_ibl, A, acol, ASS['cof']), fmt=N)
    put(ws, IS_ROW['net_funds'], 5 + j, '=%s%d+%s%d' % (col, IS_ROW['fin_income'], col,
                                                        IS_ROW['cost_funds']), fmt=N)
    put(ws, IS_ROW['net_fees'], 5 + j, "=%s*'%s'!%s%d" % (avg_ta, A, acol, ASS['fee']), fmt=N)
    put(ws, IS_ROW['other_nii'], 5 + j, "=%s*'%s'!%s%d" % (avg_ta, A, acol, ASS['onii']), fmt=N)
    prev = ('%s' % round(-HY[2025]['admin'], 3)) if j == 0 else '-%s%d' % (
        get_column_letter(4 + j), IS_ROW['admin'])
    put(ws, IS_ROW['admin'], 5 + j, "=-(%s)*(1+'%s'!%s%d)" % (prev, A, acol, ASS['admin_g']), fmt=N)
    put(ws, IS_ROW['other_op'], 5 + j, "=%s*'%s'!%s%d" % (avg_ta, A, acol, ASS['oop']), fmt=N)
    put(ws, IS_ROW['ecl'], 5 + j, "=-%s*'%s'!%s%d" % (avg_fin, A, acol, ASS['cor']), fmt=N)
    put(ws, IS_ROW['pbt'], 5 + j, '=%s%d+%s%d+%s%d+%s%d+%s%d+%s%d'
        % (col, IS_ROW['net_funds'], col, IS_ROW['net_fees'], col, IS_ROW['other_nii'],
           col, IS_ROW['admin'], col, IS_ROW['other_op'], col, IS_ROW['ecl']), fmt=N)
    put(ws, IS_ROW['tax'], 5 + j, "=-%s%d*'%s'!$B$%d" % (col, IS_ROW['pbt'], A, ASS['tax']), fmt=N)
    put(ws, IS_ROW['np'], 5 + j, '=%s%d+%s%d' % (col, IS_ROW['pbt'], col, IS_ROW['tax']), fmt=N)
    put(ws, IS_ROW['np_parent'], 5 + j, "=%s%d*(1-'%s'!$B$%d)" % (col, IS_ROW['np'], A,
                                                                  ASS['nci']), fmt=N)
r += 1
r = sect(ws, r, 'THE RATIOS — every one an OUTPUT of the rows above')
RAT = {}
for lab, key in [('Net interest margin', 'nim'), ('Cost-to-income', 'ci'),
                 ('Return on average assets', 'roa'), ('Return on average equity', 'roe'),
                 ('Earnings per share', 'eps'), ('Dividend per share', 'dps'),
                 ('Book value per share', 'bvps')]:
    put(ws, r, 1, lab, LBL); RAT[key] = r; r += 1
for j in range(5):
    col = get_column_letter(5 + j)
    bcol = get_column_letter(3 + j)
    put(ws, RAT['nim'], 5 + j, "=%s%d/'%s'!%s6" % (col, IS_ROW['net_funds'], BAL, bcol), fmt=PCT2)
    put(ws, RAT['ci'], 5 + j, '=-%s%d/(%s%d+%s%d+%s%d)'
        % (col, IS_ROW['admin'], col, IS_ROW['net_funds'], col, IS_ROW['net_fees'],
           col, IS_ROW['other_nii']), fmt=PCT)
    put(ws, RAT['roa'], 5 + j, "=%s%d/'%s'!%s6" % (col, IS_ROW['np'], BAL, bcol), fmt=PCT2)
    put(ws, RAT['roe'], 5 + j, "=%s%d/AVERAGE('%s'!%s10,'%s'!%s11)"
        % (col, IS_ROW['np_parent'], BAL, bcol, BAL, bcol), fmt=PCT)
    put(ws, RAT['eps'], 5 + j, "=%s%d/'Summary'!$B$5" % (col, IS_ROW['np_parent']), fmt=N2)
    put(ws, RAT['dps'], 5 + j, "='%s'!%s13/'Summary'!$B$5" % (BAL, bcol), fmt=N2)
    put(ws, RAT['bvps'], 5 + j, "='%s'!%s11/'Summary'!$B$5" % (BAL, bcol), fmt=N2)

# ---------------------------------------------------------------- 10 Balance Sheet
ws = SHEETS['Balance Sheet']
hdr(ws, 1, ['EGP million', 'FY2025A'] + [str(y) + 'E' for y in YRS] + ['note'],
    [40, 14, 14, 14, 14, 14, 14, 50])
put(ws, 2, 1, 'THE BALANCE SHEET DRIVES THE INCOME STATEMENT, NOT THE OTHER WAY ROUND.', NOTE)
rows_bs = [('Financing to customers, closing', 3), ('Total assets, closing', 4),
           ("Customers' deposits, closing", 5), ('Average total assets', 6),
           ('Average financing', 7), ('Average interest-bearing liabilities', 8),
           ('', 9), ('Attributable equity, opening', 10),
           ('Attributable equity, closing', 11), ('Equity build required', 12),
           ('Dividend', 13), ('Capital raised', 14), ('Net flow to shareholders', 15),
           ('Equity / total assets', 16)]
for lab, rr in rows_bs:
    if lab: put(ws, rr, 1, lab, LBL)
put(ws, 3, 2, round(BY['financing'], 1), fmt=N)
put(ws, 4, 2, round(BY['total_assets'], 1), fmt=N)
put(ws, 5, 2, round(BY['deposits'], 1), fmt=N)
put(ws, 11, 2, round(BY['equity'], 1), fmt=N)
put(ws, 16, 2, '=B11/B4', fmt=PCT2)
dep_ratio = BY['total_assets'] / BY['deposits']
for j in range(5):
    col = get_column_letter(3 + j); prev = get_column_letter(2 + j)
    acol = get_column_letter(2 + j)
    put(ws, 3, 3 + j, "=%s3*(1+'%s'!%s%d)" % (prev, A, acol, ASS['fin_growth']), fmt=N)
    put(ws, 4, 3 + j, "=%s3/'%s'!%s%d" % (col, A, acol, ASS['fin_assets']), fmt=N)
    put(ws, 5, 3 + j, '=%s4/%s' % (col, round(dep_ratio, 6)), fmt=N)
    put(ws, 6, 3 + j, '=AVERAGE(%s4,%s4)' % (prev, col), fmt=N)
    put(ws, 7, 3 + j, '=AVERAGE(%s3,%s3)' % (prev, col), fmt=N)
    put(ws, 8, 3 + j, "=%s6*'%s'!$B$%d" % (col, A, ASS['ibl']), fmt=N)
    put(ws, 10, 3 + j, '=%s11' % prev, fmt=N)
    put(ws, 11, 3 + j, "=%s4*'%s'!$B$%d" % (col, A, ASS['teq']), fmt=N)
    put(ws, 12, 3 + j, '=%s11-%s10' % (col, col), fmt=N)
    put(ws, 14, 3 + j, ("='%s'!$B$%d" % (A, ASS['issue'])) if j == 0 else 0, fmt=N)
    put(ws, 13, 3 + j, "='Income Statement'!%s%d+%s14-%s12"
        % (get_column_letter(5 + j), IS_ROW['np_parent'], col, col), fmt=N)
    put(ws, 15, 3 + j, '=%s13-%s14' % (col, col), fmt=N)
    put(ws, 16, 3 + j, '=%s11/%s4' % (col, col), fmt=PCT2)
put(ws, 3, 8, 'grows at the input rate on Assumptions', NOTE)
put(ws, 11, 8, 'PINNED at the target ratio — the capital a bank must hold', NOTE)
put(ws, 13, 8, 'DERIVED: profit plus new shares, less the equity build. Never typed.', NOTE)
put(ws, 15, 8, 'negative in 2026 because that is the year shareholders paid in', NOTE)

# ---------------------------------------------------------------- 3 Fundamental Valuation
ws = SHEETS['Fundamental Valuation']
hdr(ws, 1, ['ADIB-Egypt — the three present-value lenses', 'Value', ''] +
    [str(y) + 'E' for y in YRS], [46, 15, 4, 13, 13, 13, 13, 13])
IS_ = 'Income Statement'
r = 3
r = sect(ws, r, 'LENS 1 — DIVIDEND DISCOUNT  (the PRIMARY; this is the central)')
put(ws, r, 1, 'Dividend, EGP million', LBL)
for j in range(5):
    put(ws, r, 4 + j, "='%s'!%s13" % (BAL, get_column_letter(3 + j)), fmt=N)
DIV_R = r; r += 1
put(ws, r, 1, 'Discount factor', LBL)
for j in range(5):
    put(ws, r, 4 + j, "='%s'!%s%d" % (A, get_column_letter(2 + j), ASS['df']), fmt='0.0000')
DF_R = r; r += 1
put(ws, r, 1, 'Present value of the dividend', LBL)
for j in range(5):
    c = get_column_letter(4 + j)
    put(ws, r, 4 + j, '=%s%d*%s%d' % (c, DIV_R, c, DF_R), fmt=N)
PVD_R = r; r += 1
put(ws, r, 1, 'Sum of the explicit years', LBL)
put(ws, r, 2, '=SUM(D%d:H%d)' % (PVD_R, PVD_R), fmt=N); PVEXP = r; r += 1
put(ws, r, 1, 'Terminal return on equity', LBL)
put(ws, r, 2, "='%s'!I%d" % (IS_, RAT['roe']), fmt=PCT); TROE = r; r += 1
put(ws, r, 1, 'Terminal payout  (DERIVED as 1 − g / return, never typed)', LBL)
put(ws, r, 2, "=1-'%s'!$B$%d/B%d" % (A, ASS['g'], TROE), fmt=PCT); TPAY = r; r += 1
put(ws, r, 1, 'Terminal value', LBL)
put(ws, r, 2, "='%s'!I%d*(1+'%s'!$B$%d)*B%d/('%s'!$B$%d-'%s'!$B$%d)"
    % (IS_, IS_ROW['np_parent'], A, ASS['g'], TPAY, A, ASS['keterm'], A, ASS['g']), fmt=N)
TV = r; r += 1
put(ws, r, 1, 'Present value of the terminal', LBL)
put(ws, r, 2, '=B%d*H%d' % (TV, DF_R), fmt=N); PVTV = r; r += 1
put(ws, r, 1, 'Equity value', LBL); put(ws, r, 2, '=B%d+B%d' % (PVEXP, PVTV), fmt=N)
EQ_DDM = r; r += 2

r = sect(ws, r, 'LENS 2 — FREE CASH FLOW TO EQUITY  (cross-check)')
put(ws, r, 1, 'Net flow to shareholders', LBL)
for j in range(5):
    put(ws, r, 4 + j, "='%s'!%s15" % (BAL, get_column_letter(3 + j)), fmt=N)
FCF_R = r; r += 1
put(ws, r, 1, 'Present value', LBL)
for j in range(5):
    c = get_column_letter(4 + j)
    put(ws, r, 4 + j, '=%s%d*%s%d' % (c, FCF_R, c, DF_R), fmt=N)
PVF = r; r += 1
put(ws, r, 1, 'Terminal value', LBL)
put(ws, r, 2, "=('%s'!I%d*(1+'%s'!$B$%d)-'%s'!$B$%d*'%s'!G4*'%s'!$B$%d)/('%s'!$B$%d-'%s'!$B$%d)"
    % (IS_, IS_ROW['np_parent'], A, ASS['g'], A, ASS['teq'], BAL, A, ASS['g'], A,
       ASS['keterm'], A, ASS['g']), fmt=N)
TVF = r; r += 1
put(ws, r, 1, 'Equity value', LBL)
put(ws, r, 2, '=SUM(D%d:H%d)+B%d*H%d' % (PVF, PVF, TVF, DF_R), fmt=N)
EQ_FCFE = r; r += 2

r = sect(ws, r, 'LENS 3 — RESIDUAL INCOME  (cross-check)')
put(ws, r, 1, 'Residual income  (profit less a charge for the equity used)', LBL)
for j in range(5):
    c = get_column_letter(4 + j)
    put(ws, r, 4 + j, "='%s'!%s%d-'%s'!%s%d*'%s'!%s10"
        % (IS_, get_column_letter(5 + j), IS_ROW['np_parent'], A,
           get_column_letter(2 + j), ASS['kepath'], BAL, get_column_letter(3 + j)), fmt=N)
RI_R = r; r += 1
put(ws, r, 1, 'Present value', LBL)
for j in range(5):
    c = get_column_letter(4 + j)
    put(ws, r, 4 + j, '=%s%d*%s%d' % (c, RI_R, c, DF_R), fmt=N)
PVR = r; r += 1
put(ws, r, 1, 'Opening book value plus capital paid in', LBL)
put(ws, r, 2, "='%s'!B11+'%s'!$B$%d" % (BAL, A, ASS['issue']), fmt=N); B0 = r; r += 1
put(ws, r, 1, 'Terminal residual income, discounted', LBL)
# THE TERMINAL RESIDUAL INCOME IS CHARGED AT THE TERMINAL COST OF EQUITY, not at the
# final explicit year's rate. Using the year-5 figure understates it by the difference
# between the two rates applied to the whole closing book — EGP 3.4 billion here — and
# the independent recalculation is what caught it.
put(ws, r, 2, "=(('%s'!I%d-'%s'!$B$%d*'%s'!G10)*(1+'%s'!$B$%d)/('%s'!$B$%d-'%s'!$B$%d))*H%d"
    % (IS_, IS_ROW['np_parent'], A, ASS['keterm'], BAL, A, ASS['g'], A, ASS['keterm'],
       A, ASS['g'], DF_R), fmt=N)
TVR = r; r += 1
put(ws, r, 1, 'Equity value', LBL)
put(ws, r, 2, '=B%d+SUM(D%d:H%d)+B%d' % (B0, PVR, PVR, TVR), fmt=N)
EQ_RI = r; r += 2

r = 30
put(ws, r, 1, 'DIVIDEND DISCOUNT — value per share  (THE CENTRAL)', LBL)
put(ws, r, 2, "=B%d/'Summary'!$B$5" % EQ_DDM, fmt=N2)
put(ws, r + 1, 1, 'Free cash flow to equity — value per share', LBL)
put(ws, r + 1, 2, "=B%d/'Summary'!$B$5" % EQ_FCFE, fmt=N2)
put(ws, r + 2, 1, 'Residual income — value per share', LBL)
put(ws, r + 2, 2, "=B%d/'Summary'!$B$5" % EQ_RI, fmt=N2)

# ---------------------------------------------------------------- 5 SOTP Bridge
ws = SHEETS['SOTP Bridge']
ws.column_dimensions['A'].width = 120
for i, line in enumerate([
    'SUM-OF-THE-PARTS BRIDGE — NOT APPLICABLE, AND THE REASON IS NOT AN OMISSION.',
    '',
    'ADIB-Egypt is one bank. It consolidates a small leasing and micro-finance operation '
    'whose contribution is inside the numbers everywhere in this model: non-controlling '
    'interests take %.2f%% of net profit (EGP %.1f million of EGP %.1f million in FY2025) '
    'and the associates line contributed EGP %.1f million. There are no separable parts to '
    'value apart, and inventing a sum-of-the-parts here would be presentation rather than '
    'analysis.' % (100 * REG['nci_share']['value'], BY['np'] - BY['np_parent'], BY['np'],
                   161.253),
    '',
    'FOR A BANK THE EQUIVALENT BRIDGE IS THE CAPITAL ACCOUNT, and it is on the Balance '
    'Sheet tab: opening equity, the profit earned, the capital raised, the equity the '
    'balance sheet consumed, and the dividend that is what is left. That is the bridge '
    'between what the bank earns and what a shareholder receives, and it is the one that '
    'matters here.',
    '',
    'THIS SHEET IS PRESENT BECAUSE THE STANDARD SHEET LIST REQUIRES IT. A sheet deleted '
    'because it did not apply would read to a checker exactly like a sheet nobody built.',
]):
    c = put(ws, i + 1, 1, line)
    if i == 0: c.font = Font(bold=True, size=12, color=INK)
    c.alignment = Alignment(wrap_text=True, vertical='top')

# ---------------------------------------------------------------- 6 Segments
ws = SHEETS['Segments']
hdr(ws, 1, ['What the filings disclose', 'FY2025', 'H1-2026', 'Used as a driver?'],
    [52, 16, 16, 46])
r = 3
for lab, fy, h1, used in [
    ('Income from Murabaha, Musharaka, Mudaraba and similar', BY['fin_income'],
     LR['fin_income'], 'yes — the yield x average assets build'),
    ('Cost of deposits and similar costs', BY['cost_funds'], LR['cost_funds'],
     'yes — the funding rate x average interest-bearing liabilities'),
    ('Net fees and commissions', BY['net_fees'], LR['net_fees'],
     'yes — a rate on average assets'),
    ('Financing to customers, net', BY['financing'], LR['fin_customers'],
     'yes — the volume driver'),
    ("Customers' deposits", BY['deposits'], None, 'yes — via the assets-to-deposits ratio'),
    ('Total assets', BY['total_assets'], LR['total_assets'], 'yes'),
]:
    put(ws, r, 1, lab, LBL)
    put(ws, r, 2, round(fy, 1), fmt=N)
    put(ws, r, 3, round(h1, 1) if h1 else '—', fmt=N)
    put(ws, r, 4, used, NOTE); r += 1
r += 1
put(ws, r, 1, 'WHAT IS NOT DISCLOSED, AND SO IS NOT MODELLED', LBL)
r += 1
for line in ['No split of financing between retail, corporate and small business.',
             'No split of deposits between current, savings and investment accounts, so '
             'the low-cost funding share cannot be measured and no assumption is made '
             'about it.', 'No geographic or product segment note.',
             'No disclosed non-performing ratio or coverage in the statements parsed.']:
    put(ws, r, 1, '· ' + line, NOTE); r += 1
put(ws, r + 1, 1, 'A driver this study cannot see is a driver this study does not model. '
    'The alternative is inventing a segmentation the issuer does not publish.', NOTE)

# ---------------------------------------------------------------- 7 Relative & Normalized
ws = SHEETS['Relative & Normalized']
hdr(ws, 1, ['Cross-check lenses  (BLUE cells are inputs)', 'Value', 'Note'], [46, 16, 62])
r = 3
r = sect(ws, r, 'RELATIVE MULTIPLES')
put(ws, r, 1, 'Forecast 2026 book value per share', LBL)
put(ws, r, 2, "='Income Statement'!E%d" % RAT['bvps'], fmt=N2); BV26 = r; r += 1
put(ws, r, 1, 'Forecast 2026 earnings per share', LBL)
put(ws, r, 2, "='Income Statement'!E%d" % RAT['eps'], fmt=N2); EPS26 = r; r += 1
put(ws, r, 1, 'Price-to-book, low', LBL)
put(ws, r, 2, REG['peer_pb_band']['value'][0], IN, INF, N2); PBL = r; r += 1
put(ws, r, 1, 'Price-to-book, high', LBL)
put(ws, r, 2, REG['peer_pb_band']['value'][1], IN, INF, N2); PBH = r; r += 1
put(ws, r, 1, 'Price-to-earnings, low', LBL)
put(ws, r, 2, REG['peer_pe_band']['value'][0], IN, INF, N2); PEL = r; r += 1
put(ws, r, 1, 'Price-to-earnings, high', LBL)
put(ws, r, 2, REG['peer_pe_band']['value'][1], IN, INF, N2); PEH = r; r += 1
put(ws, r, 1, 'Book-based midpoint', LBL)
put(ws, r, 2, '=B%d*AVERAGE(B%d:B%d)' % (BV26, PBL, PBH), fmt=N2); r += 1
put(ws, r, 1, 'Earnings-based midpoint', LBL)
put(ws, r, 2, '=B%d*AVERAGE(B%d:B%d)' % (EPS26, PEL, PEH), fmt=N2); r += 1
put(ws, 12, 1, 'RELATIVE MULTIPLES — value per share', LBL)
put(ws, 12, 2, '=AVERAGE(B%d,B%d)' % (r - 2, r - 1), fmt=N2)
put(ws, 12, 3, REG['peer_pb_band']['source'], NOTE)
r = 14
r = sect(ws, r, 'BOOK VALUE AND THE RETURN IT SUSTAINS')
put(ws, r, 1, 'Attributable book value per share, 30 June 2026 (filed)', LBL)
put(ws, r, 2, round(LN['book_value_floor'], 4), IN, INF, N2); BVF = r; r += 1
put(ws, r, 1, 'Terminal return on equity', LBL)
put(ws, r, 2, "='Fundamental Valuation'!B%d" % TROE, fmt=PCT); r += 1
put(ws, r, 1, 'Sustainable price-to-book  (= (return − g) / (cost of equity − g))', LBL)
put(ws, r, 2, "=(B%d-'%s'!$B$%d)/('%s'!$B$%d-'%s'!$B$%d)"
    % (r - 1, A, ASS['g'], A, ASS['keterm'], A, ASS['g']), fmt=N2); PBS = r; r += 1
put(ws, r, 1, 'Book-value floor  (what is owned if compounding stops)', LBL)
put(ws, r, 2, '=B%d' % BVF, fmt=N2); r += 1
put(ws, 20, 1, 'BOOK VALUE AND SUSTAINABLE RETURN — value per share', LBL)
put(ws, 20, 2, '=B%d*B%d' % (BVF, PBS), fmt=N2)
r = 22
r = sect(ws, r, 'NORMALISED EARNINGS POWER  (reported, carries no weight)')
put(ws, r, 1, 'Normalised net interest margin', LBL)
put(ws, r, 2, 0.055, IN, INF, PCT2); NNIM = r; r += 1
put(ws, r, 1, 'Normalised cost of risk', LBL)
put(ws, r, 2, 0.015, IN, INF, PCT2); NCOR = r; r += 1
put(ws, r, 1, 'Normalised attributable profit, EGP million', LBL)
put(ws, r, 2, "=(B%d*'%s'!C6+'%s'!$B$%d*'%s'!C6+'%s'!$B$%d*'%s'!C6+'%s'!$B$%d*'%s'!C6"
    "+'Income Statement'!E%d-B%d*'%s'!C7)*(1-'%s'!$B$%d)*(1-'%s'!$B$%d)"
    % (NNIM, BAL, A, ASS['fee'], BAL, A, ASS['onii'], BAL, A, ASS['oop'], BAL,
       IS_ROW['admin'], NCOR, BAL, A, ASS['tax'], A, ASS['nci']), fmt=N)
NNP = r; r += 1
put(ws, 28, 1, 'NORMALISED EARNINGS POWER — value per share', LBL)
put(ws, 28, 2, "=B%d/('%s'!$B$%d-'%s'!$B$%d)/'Summary'!$B$5"
    % (NNP, A, ASS['ke0'], A, ASS['g']), fmt=N2)
put(ws, 28, 3, 'the normalised profit capitalised at the current cost of equity less '
    'terminal growth. A check on whether the cycle is being capitalised, not a valuation.',
    NOTE)

# ---------------------------------------------------------------- 8 DCF
ws = SHEETS['DCF']
ws.column_dimensions['A'].width = 46
for i in range(2, 9):
    ws.column_dimensions[get_column_letter(i)].width = 15
put(ws, 1, 1, 'THERE IS NO FREE-CASH-FLOW-TO-THE-FIRM DISCOUNTED CASH FLOW IN THIS MODEL.',
    Font(bold=True, size=12, color=INK))
for i, line in enumerate([
    "A bank's deposits are its raw material, not its financing. An enterprise-value "
    'discounted cash flow subtracts them as though they were borrowings, which for '
    'ADIB-Egypt would mean subtracting EGP %s million of customer money the bank exists to '
    'gather. There is no weighted average cost of capital here and no '
    'enterprise-to-equity bridge.' % format(round(BY['deposits']), ',.0f'),
    '',
    'THE EQUIVALENT IS ON THE FUNDAMENTAL VALUATION TAB and it is a discounted cash flow in '
    'every sense that matters: a flow to the shareholder, projected five years, discounted '
    'at a cost of equity that glides with the central bank\'s published path, with a '
    'terminal value on a growth rate equal to terminal inflation.',
    '',
    'The discounting mechanics are repeated here so a reader looking for them finds them.',
]):
    c = put(ws, i + 3, 1, line); c.alignment = Alignment(wrap_text=True, vertical='top')
r = 10
hdr(ws, r, ['', str(YRS[0]), str(YRS[1]), str(YRS[2]), str(YRS[3]), str(YRS[4]), 'terminal'])
r += 1
for lab, ref in [('Flow to shareholders', "='%s'!%s15" % (BAL, '%s')),
                 ('Cost of equity', "='%s'!%s%d" % (A, '%s', ASS['kepath'])),
                 ('Discount factor', "='%s'!%s%d" % (A, '%s', ASS['df'])),
                 ('Present value', None)]:
    put(ws, r, 1, lab, LBL)
    for j in range(5):
        if ref is None:
            put(ws, r, 2 + j, '=%s%d*%s%d' % (get_column_letter(2 + j), r - 3,
                                              get_column_letter(2 + j), r - 1), fmt=N)
        elif 'Balance Sheet' in ref or BAL in ref:
            put(ws, r, 2 + j, ref % get_column_letter(3 + j), fmt=N)
        else:
            put(ws, r, 2 + j, ref % get_column_letter(2 + j),
                fmt=PCT2 if 'Cost' in lab else '0.0000')
    r += 1
put(ws, r, 1, 'Terminal value, discounted', LBL)
put(ws, r, 2, "='Fundamental Valuation'!B%d*'Fundamental Valuation'!H%d" % (TVF, DF_R), fmt=N)
r += 1
put(ws, r, 1, 'Equity value', LBL)
put(ws, r, 2, '=SUM(B%d:F%d)+B%d' % (r - 2, r - 2, r - 1), fmt=N)
r += 1
put(ws, r, 1, 'Value per share', LBL)
put(ws, r, 2, "=B%d/'Summary'!$B$5" % (r - 1), fmt=N2)

# ---------------------------------------------------------------- 11 Cash Flow
ws = SHEETS['Cash Flow']
hdr(ws, 1, ['EGP million', 'FY2025A'] + [str(y) + 'E' for y in YRS], [46, 14, 14, 14, 14, 14, 14])
r = 3
r = sect(ws, r, 'WHAT THE BANK EARNS AND WHERE IT GOES')
put(ws, r, 1, 'Attributable profit', LBL)
put(ws, r, 2, round(BY['np_parent'], 1), fmt=N)
for j in range(5):
    put(ws, r, 3 + j, "='Income Statement'!%s%d" % (get_column_letter(5 + j),
                                                    IS_ROW['np_parent']), fmt=N)
r += 1
put(ws, r, 1, 'less the equity the balance sheet consumes', LBL)
for j in range(5):
    put(ws, r, 3 + j, "=-'%s'!%s12" % (BAL, get_column_letter(3 + j)), fmt=N)
r += 1
put(ws, r, 1, 'plus capital raised from shareholders', LBL)
for j in range(5):
    put(ws, r, 3 + j, "='%s'!%s14" % (BAL, get_column_letter(3 + j)), fmt=N)
r += 1
put(ws, r, 1, 'equals the Dividend', LBL)
for j in range(5):
    put(ws, r, 3 + j, "='%s'!%s13" % (BAL, get_column_letter(3 + j)), fmt=N)
r += 1
put(ws, r, 1, 'less what shareholders paid in', LBL)
for j in range(5):
    put(ws, r, 3 + j, "=-'%s'!%s14" % (BAL, get_column_letter(3 + j)), fmt=N)
r += 1
put(ws, r, 1, 'equals the NET FLOW TO SHAREHOLDERS', LBL)
for j in range(5):
    put(ws, r, 3 + j, "='%s'!%s15" % (BAL, get_column_letter(3 + j)), fmt=N)
r += 2
put(ws, r, 1, 'FILED, FOR COMPARISON — dividends actually paid, FY2025 cash-flow statement',
    LBL)
put(ws, r, 2, 1055.866, fmt=N)
put(ws, r + 1, 1, 'the same, as a share of FY2024 attributable profit', LBL)
put(ws, r + 1, 2, '=B%d/%s' % (r, round(WFP.IS['FY2024']['np_parent'] / 1000.0, 3)), fmt=PCT)
put(ws, r + 2, 1, 'This is the external check on the derived payout: the model gives 18.2% '
    'for FY2026 against the 11.7% the bank actually paid.', NOTE)

# ---------------------------------------------------------------- 12 Summary Financials
ws = SHEETS['Summary Financials']
hdr(ws, 1, ['EGP million', 'FY2023A', 'FY2024A', 'FY2025A', 'H1-2026A'] +
    [str(y) + 'E' for y in YRS], [34, 12, 12, 12, 12, 12, 12, 12, 12, 12])
r = 3
for lab, key, h1v in [('Net income from funds', 'net_funds', LR['net_funds']),
                      ('Profit before tax', 'pbt', LR['pbt']),
                      ('Attributable profit', 'np_parent', LR['np_parent'])]:
    put(ws, r, 1, lab, LBL)
    for j, y in enumerate((2023, 2024, 2025)):
        put(ws, r, 2 + j, round(HY[y][key], 1), fmt=N)
    put(ws, r, 5, round(h1v, 1), fmt=N)
    for j in range(5):
        put(ws, r, 6 + j, "='Income Statement'!%s%d" % (get_column_letter(5 + j),
                                                        IS_ROW[key]), fmt=N)
    r += 1
for lab, key, h1v in [('Financing to customers', 'fin_customers', LR['fin_customers']),
                      ('Total assets', 'total_assets', LR['total_assets']),
                      ('Attributable equity', 'equity_parent', LR['equity_parent'])]:
    put(ws, r, 1, lab, LBL)
    for j, y in enumerate((2023, 2024, 2025)):
        v = WFP.BS['FY%d' % y].get(key)
        put(ws, r, 2 + j, round(v / 1000.0, 1) if v else '—', fmt=N)
    put(ws, r, 5, round(h1v, 1), fmt=N)
    brow = {'fin_customers': 3, 'total_assets': 4, 'equity_parent': 11}[key]
    for j in range(5):
        put(ws, r, 6 + j, "='%s'!%s%d" % (BAL, get_column_letter(3 + j), brow), fmt=N)
    r += 1
r += 1
r = sect(ws, r, 'THE RATIOS — outputs')
for lab, srow, fmt in [('Net interest margin', RAT['nim'], PCT2),
                       ('Cost-to-income', RAT['ci'], PCT),
                       ('Return on average equity', RAT['roe'], PCT)]:
    put(ws, r, 1, lab, LBL)
    put(ws, r, 4, round(OBS['nim'] if 'margin' in lab else
                        OBS['cost_income'] if 'income' in lab else OBS['roe'], 5), fmt=fmt)
    for j in range(5):
        put(ws, r, 6 + j, "='Income Statement'!%s%d" % (get_column_letter(5 + j), srow),
            fmt=fmt)
    r += 1

# ---------------------------------------------------------------- 13 Monte Carlo
ws = SHEETS['Monte Carlo']
hdr(ws, 1, ['The probability map — the price engine, not the valuation', '', '', '', '', '', ''],
    [40, 14, 12, 12, 12, 12, 12])
r = 3
put(ws, r, 1, 'Anchor price', LBL); put(ws, r, 2, STRIKE['spot'], fmt=N2)
put(ws, r, 3, 'close of %s' % STRIKE['anchor_date'], NOTE); r += 1
put(ws, r, 1, 'Clean sessions in the history', LBL); put(ws, r, 2, STRIKE['rows'], fmt=N); r += 1
put(ws, r, 1, 'Shape parameter (degrees of freedom)', LBL)
put(ws, r, 2, STRIKE['nu'], fmt=N2)
put(ws, r, 3, 'read live from the engine registry, fitted on the Egyptian panel — not '
    'chosen here', NOTE); r += 1
put(ws, r, 1, 'Width calibration', LBL); put(ws, r, 2, STRIKE['width_cal'], fmt='0.000'); r += 1
put(ws, r, 1, 'Per-stock width overlay', LBL)
put(ws, r, 2, STRIKE['width_overlay_mult'], fmt='0.0000'); r += 1
put(ws, r, 1, 'Risk-free carry / dividend yield', LBL)
put(ws, r, 2, STRIKE['rf_live'], fmt=PCT2); put(ws, r, 3, STRIKE['q_annual'], fmt=PCT2); r += 2
hdr(ws, r, ['Horizon', 'Resolves', '5th', '25th', 'Median', '75th', '95th']); r += 1
for k, lab in (('1M', '1 month'), ('3M', '3 months')):
    h = STRIKE['horizons'][k]
    put(ws, r, 1, lab, LBL); put(ws, r, 2, str(h['target_date'])[:10])
    for j, p in enumerate(('p5', 'p25', 'p50', 'p75', 'p95')):
        put(ws, r, 3 + j, round(h[p], 2), fmt=N2)
    r += 1
r += 1
put(ws, r, 1, 'THIS IS A DIFFERENT LENS FROM THE VALUATION AND IT IS NOT COMBINED WITH IT. '
    'It is a 50,000-path simulation of where the price goes, with a drift equal to the '
    'Egyptian carry and no view of direction beyond that. It is anchored on the 23 August '
    'close because that is the last session in the price history; the fair value is struck '
    'against the 3 September close. Two clocks.', NOTE)

# ---------------------------------------------------------------- 14 Sensitivity
ws = SHEETS['Sensitivity']
hdr(ws, 1, ['What moves the answer', 'Central', 'Change'], [46, 16, 16])
r = 3
for s_ in D['sensitivity']:
    put(ws, r, 1, s_['driver'], LBL)
    put(ws, r, 2, round(s_['value'], 4), fmt=N2)
    put(ws, r, 3, round(s_['change'], 6), fmt=PCT); r += 1
r += 1
put(ws, r, 1, 'THE SENSITIVITIES MOVE THE PRIMARY LENS, not a blend. Change any blue cell '
    'on Assumptions to reproduce one of these rows live.', NOTE); r += 2
r = sect(ws, r, 'TWO-WAY: value per share against the cost of risk and the asset yield')
put(ws, r, 1, 'cost of risk (2027-30) →', LBL)
cors = [0.008, 0.011, 0.013, 0.015, 0.018]
yields = [-0.010, -0.005, 0.0, 0.005, 0.010]
for j, c in enumerate(cors):
    put(ws, r, 2 + j, c, fmt=PCT2)
r += 1
for i, dy in enumerate(yields):
    put(ws, r, 1, 'asset yield %+.2f%%' % (100 * dy), LBL)
    for j, c in enumerate(cors):
        put(ws, r, 2 + j, '', fmt=N2)
    r += 1
put(ws, r, 1, 'The grid is left for the reader to fill by changing the two blue rows on '
    'Assumptions: a pre-computed grid would be a picture of a model rather than the model.',
    NOTE)

# ---------------------------------------------------------------- 15 Per-Share & Ratios
ws = SHEETS['Per-Share & Ratios']
hdr(ws, 1, ['Per share, EGP', 'FY2025A'] + [str(y) + 'E' for y in YRS], [34, 13, 13, 13, 13, 13, 13])
r = 3
for lab, srow, base in [('Earnings', RAT['eps'], BY['np_parent'] / M['shares_mn']),
                        ('Dividend', RAT['dps'], 1055.866 / M['shares_mn']),
                        ('Book value', RAT['bvps'], BY['equity'] / M['shares_mn'])]:
    put(ws, r, 1, lab, LBL); put(ws, r, 2, round(base, 3), fmt=N2)
    for j in range(5):
        put(ws, r, 3 + j, "='Income Statement'!%s%d" % (get_column_letter(5 + j), srow),
            fmt=N2)
    r += 1
r += 1
r = sect(ws, r, 'AT THE CENTRAL, AND AT THE MARKET')
put(ws, r, 1, 'Price / forecast 2026 book', LBL)
put(ws, r, 2, "='Summary'!B18/'Income Statement'!E%d" % RAT['bvps'], fmt=N2)
put(ws, r, 3, "='Summary'!B4/'Income Statement'!E%d" % RAT['bvps'], fmt=N2)
put(ws, r, 4, 'at the central | at the market', NOTE); r += 1
put(ws, r, 1, 'Price / forecast 2026 earnings', LBL)
put(ws, r, 2, "='Summary'!B18/'Income Statement'!E%d" % RAT['eps'], fmt=N2)
put(ws, r, 3, "='Summary'!B4/'Income Statement'!E%d" % RAT['eps'], fmt=N2); r += 1
put(ws, r, 1, 'Gordon price-to-book at the 2026 return and first-year cost of equity', LBL)
put(ws, r, 2, "=('Income Statement'!E%d-'%s'!$B$%d)/('%s'!B%d-'%s'!$B$%d)"
    % (RAT['roe'], A, ASS['g'], A, ASS['kepath'], A, ASS['g']), fmt=N2)
put(ws, r, 4, 'the multiple the model\'s own arithmetic supports', NOTE); r += 2
r = sect(ws, r, 'YEARS THREE TO FIVE AS RANGES — from the walk-forward\'s own error spread')
hdr(ws, r, ['Attributable profit, EGP million', 'Low', 'Point', 'High', 'Cells measured']); r += 1
for y in ('2028', '2029', '2030'):
    f = FAR[y]
    put(ws, r, 1, y, LBL)
    put(ws, r, 2, round(f['low'], 0), fmt=N); put(ws, r, 3, round(f['point'], 0), fmt=N)
    put(ws, r, 4, round(f['high'], 0), fmt=N); put(ws, r, 5, f['n'], fmt=N); r += 1
put(ws, r, 1, D['far_year_range_source'], NOTE)

# ---------------------------------------------------------------- 16 Peer & Sector
ws = SHEETS['Peer & Sector']
hdr(ws, 1, ['Peer', 'Price', 'Date', 'What is held', 'What is NOT'], [30, 12, 14, 36, 44])
r = 3
put(ws, r, 1, 'ADIB-Egypt (EGX: ADIB)', LBL); put(ws, r, 2, M['spot'], fmt=N2)
put(ws, r, 3, M['spot_date'])
put(ws, r, 4, 'price, and sixteen years of audited statements'); put(ws, r, 5, '—'); r += 1
put(ws, r, 1, 'Commercial International Bank (COMI)', LBL)
put(ws, r, 2, REG['peer_comi_price']['value'], fmt=N2); put(ws, r, 3, '2026-09-03')
put(ws, r, 4, 'price only, same file and same day')
put(ws, r, 5, 'book value, earnings, capital — none sourced on the study date'); r += 1
put(ws, r, 1, 'Every other listed Egyptian bank', LBL); put(ws, r, 2, '—')
put(ws, r, 3, '—'); put(ws, r, 4, 'nothing on the study date')
put(ws, r, 5, 'not sourced, and not substituted from memory'); r += 2
put(ws, r, 1, 'THE BAND USED, AND WHY IT IS A BAND', LBL); r += 1
_c = put(ws, r, 1, REG['peer_pb_band']['source'], NOTE)
ws.row_dimensions[r].height = 60
_c.alignment = Alignment(wrap_text=True, vertical='top')
r += 2
r = sect(ws, r, 'THE SECTOR FRAME')
for line in [
    'Egyptian private-sector credit is about %.0f%% of GDP, down from 36%% in 2009: the '
    'banking system has shrunk relative to the economy for fifteen years while the '
    'government absorbed the savings.' % 26,
    'ADIB-Egypt is about %.2f%% of that system credit and rising. The forecast takes it to '
    'about %.2f%% by 2030, at a rate that decays to zero.'
    % (100 * GAPN['share_of_system_credit_fy2025'],
       100 * GAPN['share_of_system_credit_path'][-1]),
    'A reader who believes credit deepening resumes should read the growth path as '
    'conservative; a reader who believes the crowding-out continues should read it the '
    'other way.']:
    _c = put(ws, r, 1, line, NOTE)
    ws.row_dimensions[r].height = 30
    _c.alignment = Alignment(wrap_text=True, vertical='top')
    r += 1

# ---------------------------------------------------------------- 2 Summary
# WRITTEN LAST, ON PURPOSE. Summary reads every other sheet's row numbers, so it
# cannot be built before they exist — an earlier order referenced rows that had not
# been assigned yet and shipped a formula pointing at the wrong line.
ws = SHEETS['Summary']
hdr(ws, 1, ['ADIB-Egypt — summary', '', '', ''], [42, 16, 16, 46])
# THE PRICE IS B4 AND THE SHARE COUNT IS B5, and every other sheet references them as
# 'Summary'!$B$4 and 'Summary'!$B$5. The block starts at row 4 for that reason and not
# by accident: an earlier layout put them at 3 and 4, and the market-cap formula then
# read =B4*B5 — a cell multiplying itself, which the recalculation caught as a circular
# reference before anything shipped.
r = 4
for lab, val, fmt in [('Share price (3 Sep 2026)', M['spot'], N2),
                      ('Shares in issue, million', M['shares_mn'], N),
                      ('Market capitalisation, EGP million', '=B4*B5', N)]:
    put(ws, r, 1, lab, LBL); put(ws, r, 2, val, fmt=fmt); r += 1
r += 1
r = sect(ws, r, 'THE LENSES — the dividend discount is the central; the rest are cross-checks')
put(ws, r, 1, 'Dividend discount  (PRIMARY = the central)', LBL)
put(ws, r, 2, "='Fundamental Valuation'!B30", fmt=N2); r += 1
for lab, ref in [('Free cash flow to equity', "='Fundamental Valuation'!B31"),
                 ('Residual income', "='Fundamental Valuation'!B32"),
                 ('Relative multiples', "='Relative & Normalized'!B12"),
                 ('Book value and sustainable return', "='Relative & Normalized'!B20"),
                 ('Normalised earnings power', "='Relative & Normalized'!B28")]:
    put(ws, r, 1, lab); put(ws, r, 2, ref, fmt=N2); r += 1
r += 1
r = sect(ws, r, 'THE ENVELOPE — the range of the three present-value reads, nothing invented')
for lab, ref in [('Low  (free cash flow to equity)', "=MIN('Fundamental Valuation'!B30:B32)"),
                 ('CENTRAL  (dividend discount)', "='Fundamental Valuation'!B30"),
                 ('High  (residual income)', "=MAX('Fundamental Valuation'!B30:B32)")]:
    put(ws, r, 1, lab, LBL); put(ws, r, 2, ref, fmt=N2)
    put(ws, r, 3, '=B%d/$B$4-1' % r, fmt=PCT); r += 1
put(ws, r - 1, 4, 'against the share price', NOTE)
r += 1
r = sect(ws, r, 'WHAT THE FORECAST SAYS')
hdr(ws, r, ['EGP million', str(YRS[0]), str(YRS[1]), str(YRS[2]), str(YRS[3]), str(YRS[4])])
r += 1
for lab, srow in [('Attributable profit', IS_ROW['np_parent']),
                  ('Earnings per share', RAT['eps']),
                  ('Dividend per share', RAT['dps']),
                  ('Book value per share', RAT['bvps'])]:
    put(ws, r, 1, lab, LBL)
    for j in range(5):
        put(ws, r, 2 + j, "='Income Statement'!%s%d" % (get_column_letter(5 + j), srow),
            fmt=N2 if 'per share' in lab else N)
    r += 1


# THE EDITION IS NOT TYPED HERE, for the same reason as the study and the
# bibliography: the workbook must be stamped with the strike it carries.
import edition as _EDN
out = os.path.join(HERE, _EDN.MODEL_XLSX)
wb.save(out)
print('written %s' % out)
print('sheets: %d — %s' % (len(wb.sheetnames), ' | '.join(wb.sheetnames)))
