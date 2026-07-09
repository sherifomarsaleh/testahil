"""GBCO_Valuation_Model_08072026_public.xlsx — 16 sheets mirroring the TMPV canonical model.
Blue = inputs · black = formulas · green = cross-sheet links. All inputs live on Assumptions."""
import json
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

D = json.load(open('study_numbers.json'))
BLUE = Font(color='0000FF'); GREEN = Font(color='008000'); BLACK = Font(color='000000')
BOLD = Font(bold=True); TITLE = Font(bold=True, size=13, color='F6F1E6')
SUB = Font(size=9, color='6E7B77'); HDR = Font(bold=True, color='1C3A36')
FILL_T = PatternFill('solid', start_color='1C3A36')
FILL_H = PatternFill('solid', start_color='EAF0EE')
FILL_G = PatternFill('solid', start_color='F6F1E6')
NUM = '#,##0.0;(#,##0.0);"-"'; NUM0 = '#,##0;(#,##0);"-"'; PCT = '0.0%;(0.0%);"-"'
MULT = '0.00x'; PX = '0.00'

wb = Workbook()

def sheet(name):
    ws = wb.create_sheet(name) if wb.sheetnames != ['Sheet'] else wb.active
    ws.title = name
    return ws

def title(ws, text, sub=None, width=10):
    ws['A1'] = text; ws['A1'].font = TITLE; ws['A1'].fill = FILL_T
    for c in range(2, width + 1):
        ws.cell(row=1, column=c).fill = FILL_T
    if sub:
        ws['A2'] = sub; ws['A2'].font = SUB
    ws.column_dimensions['A'].width = 42
    for c in range(2, width + 1):
        ws.column_dimensions[get_column_letter(c)].width = 12.5

def put(ws, addr, val, font=BLACK, fmt=None, bold=False, fill=None):
    c = ws[addr]; c.value = val
    c.font = Font(color=font.color, bold=bold) if font else (BOLD if bold else BLACK)
    if fmt: c.number_format = fmt
    if fill: c.fill = fill
    return c

# ============ READ FIRST =====================================================
ws = sheet('READ FIRST')
title(ws, 'Testahil — GB Corp S.A.E. (EGX: GBCO)', width=9)
lines = [
 'Companion model · Independent Valuation Study · Educational analysis · Not investment advice', '',
 'What this workbook is. A transparent companion to the GBCO valuation study. Every blue cell is an input; every',
 'black cell is a formula; green cells link across sheets. All inputs live on the Assumptions sheet — change one',
 '(the complexity discount, the Auto gross margin, a growth rate, the GB Capital multiple) and the whole model reprices.', '',
 'What it is not. It is not investment advice, a recommendation, or a price target. Values are model outputs shown',
 'as ranges. The preparer is not licensed by any securities regulator and may hold a position in the security.', '',
 'Entity note. GB Corp S.A.E. (formerly GB Auto / Ghabbour Auto; renamed March 2023) is an operating company with a',
 'captive finance arm: GB Auto (passenger cars, CV&CE, trading, light mobility; Egypt · Iraq · Jordan) plus GB Capital',
 '(leasing, factoring, consumer finance, SME lending) and associate stakes in MNT-Halan, Bedaya and Kaf.',
 'House lens: split the legs — Auto = FCFF DCF; captive lender = adjusted book × a return-justified multiple;',
 'the fintech associate = balance-sheet carrying value cross-checked to the June-2026 USD 1.4bn funding round.', '',
 'Currency. EGP million unless stated. Spot EGP 31.25 (7 Jul 2026 close). Historical financials are company disclosure',
 '(FY23–FY25 earnings releases; 1Q26 release 14 May 2026). Some consolidated balance-sheet lines are grouped from the',
 'disclosed segment balance sheets to a house layout — flagged on the Balance Sheet.', '',
 'Sheets: Summary · Fundamental Valuation · Assumptions · SOTP · Segments · Relative & Normalized · DCF ·',
 'Income Statement · Balance Sheet · Cash Flow · Summary Financials · Monte Carlo · Sensitivity · Per-Share & Ratios · Peer & Sector.']
for i, ln in enumerate(lines, start=3):
    ws.cell(row=i, column=1, value=ln).font = Font(size=10)
ws.column_dimensions['A'].width = 118

# ============ ASSUMPTIONS (built early so links resolve) =====================
wa = sheet('Assumptions')
title(wa, 'Assumptions — the single input layer', 'All blue cells are inputs. Every other sheet links here.', 9)
r = 4
def hdr(ws_, row, text):
    put(ws_, f'A{row}', text, bold=True, fill=FILL_H); return row + 1
def inp(ws_, row, label, val, fmt=NUM, note=None):
    put(ws_, f'A{row}', label)
    put(ws_, f'B{row}', val, BLUE, fmt)
    if note: put(ws_, f'C{row}', note, SUB)
    return row + 1
r = hdr(wa, r, 'ANCHORS')
r = inp(wa, r, 'Spot price (EGP/share)', 31.25, PX)
r = inp(wa, r, 'Shares outstanding (mn)', 1085.5, NUM0)
r = inp(wa, r, 'Tax rate', 0.28, PCT)
r = hdr(wa, r, 'COST OF CAPITAL (Ke published as rf + β × ERP — house rule §3.5-G)')
r = inp(wa, r, 'Risk-free rate (blended 5-yr EGP; 12M T-bill ~21.5% gliding to ~15%)', 0.19, PCT, 'flagged: house view of the CBE easing path')
r = inp(wa, r, 'Equity beta (house band 0.8–1.3)', 0.95, '0.00')
r = inp(wa, r, 'Equity risk premium (Egypt)', 0.07, PCT)
put(wa, f'A{r}', 'Cost of equity Ke = rf + β × ERP'); put(wa, f'B{r}', '=B9+B10*B11', BLACK, PCT); KE=f'B{r}'; r+=1
r = inp(wa, r, 'Pre-tax cost of debt', 0.21, PCT)
put(wa, f'A{r}', 'After-tax Kd'); put(wa, f'B{r}', '=B13*(1-B7)', BLACK, PCT); r+=1
r = inp(wa, r, 'Debt weight (target, market)', 0.35, PCT)
put(wa, f'A{r}', 'WACC'); put(wa, f'B{r}', f'=(1-B15)*B12+B15*B14', BLACK, PCT); WACC='Assumptions!$B$16'; r+=1
r = inp(wa, r, 'Terminal growth (nominal EGP)', 0.115, PCT)
TG='Assumptions!$B$17'
r = hdr(wa, r, 'SOTP — the three legs (split-the-legs, §3.5-F5)')
r = inp(wa, r, 'GB Auto net debt (31 Dec 2025)', 15210.0, NUM0, 'disclosed; 1Q26 ND/EBITDA 2.14x')
r = inp(wa, r, 'GB Auto non-controlling interests', 800.4, NUM0)
r = inp(wa, r, 'GB Capital adjusted operating equity', 9500.0, NUM0, 'from disclosed adjusted-ROAE basis (NP 1,366 / 15.1%)')
r = inp(wa, r, 'GB Capital multiple (× adjusted book)', 1.0, MULT, 'return-justified ~1× book')
r = inp(wa, r, 'Associates carrying value (MNT-Halan + Bedaya + Kaf)', 13689.5, NUM0, '≈ Jun-26 USD 1.4bn round × ~20% est. stake')
r = inp(wa, r, 'Associates mark (× carrying)', 1.0, MULT)
r = inp(wa, r, 'Complexity / conglomerate discount', 0.10, PCT, 'sensitized 0–20%')
r = hdr(wa, r, 'RELATIVE & NORMALIZED')
r = inp(wa, r, 'FY26E group net profit for the relative lens', 3300.0, NUM0, 'set slightly below the IS build for conservatism')
r = inp(wa, r, 'Justified P/E (base)', 9.5, MULT)
r = inp(wa, r, 'Mid-cycle group PAT (normalized)', 4200.0, NUM0)
r = inp(wa, r, 'Justified through-cycle P/E', 8.5, MULT)
r = hdr(wa, r, 'SYNTHESIS WEIGHTS')
r = inp(wa, r, 'SOTP weight', 0.40, PCT)
r = inp(wa, r, 'Pre-discount NAV weight', 0.15, PCT)
r = inp(wa, r, 'Relative weight', 0.20, PCT)
r = inp(wa, r, 'Normalized-earnings weight', 0.25, PCT)
r = hdr(wa, r, 'MONTE CARLO (YZ-HAR v2 — no KVOL; engine outputs on the Monte Carlo sheet)')
r = inp(wa, r, 'Anchor volatility (HAR forecast, annualized)', round(D['engine']['anchor_vol'], 4), PCT)
r = inp(wa, r, 'Secular drift (daily log-return, expanding window)', round(D['engine']['drift_daily'], 6), '0.0000%')
r = inp(wa, r, 'Net factor drift per quarter (16-factor stack)', round(D['engine']['factor_drift_q'], 4), PCT)
r = inp(wa, r, 'Paths / seed', '50,000 / 42', '@')
r = hdr(wa, r, 'FORECAST DRIVERS (FY26E–FY30E) — units × ASP build; drivers disclosed')
yrs = ['FY26E', 'FY27E', 'FY28E', 'FY29E', 'FY30E']
put(wa, f'A{r}', 'Driver \\ year', bold=True)
for j, y in enumerate(yrs):
    put(wa, f'{get_column_letter(3+j)}{r}', y, bold=True, fill=FILL_H)
r += 1
DRV = {}
def drv(row, label, vals, fmt=PCT):
    put(wa, f'A{row}', label)
    for j, v in enumerate(vals):
        put(wa, f'{get_column_letter(3+j)}{row}', v, BLUE, fmt)
    DRV[label] = row
    return row + 1
r = drv(r, 'PC volume growth', [0.12, 0.14, 0.10, 0.08, 0.06])
r = drv(r, 'PC ASP growth', [0.06, 0.07, 0.07, 0.06, 0.06])
r = drv(r, 'CV&CE volume growth', [0.25, 0.18, 0.12, 0.10, 0.08])
r = drv(r, 'CV&CE ASP growth', [0.05]*5)
r = drv(r, 'Light-Mobility volume growth', [0.30, 0.20, 0.15, 0.12, 0.10])
r = drv(r, 'Light-Mobility ASP growth', [0.05]*5)
r = drv(r, 'Trading revenue growth', [0.18, 0.15, 0.12, 0.10, 0.10])
r = drv(r, 'GB Capital revenue growth', [0.45, 0.30, 0.25, 0.20, 0.18])
r = drv(r, 'GB Capital loan-book growth', [0.35, 0.28, 0.24, 0.20, 0.18])
r = drv(r, 'Auto gross margin', [0.138, 0.142, 0.145, 0.145, 0.145])
r = drv(r, 'Auto GS&A (% of revenue)', [0.073, 0.072, 0.071, 0.070, 0.070])
r = drv(r, 'Auto other operating income (% rev)', [0.012]*5)
r = drv(r, 'Auto provisions (% rev)', [-0.003]*5)
r = drv(r, 'Auto D&A (% of revenue)', [0.011]*5)
r = drv(r, 'Auto capex (EGP mn)', [3000, 2400, 2500, 2600, 2800], NUM0)
r = drv(r, 'Rental-fleet & other capex (EGP mn)', [700, 800, 900, 1000, 1100], NUM0)
r = drv(r, 'GB Capital D&A (EGP mn)', [560, 640, 730, 830, 940], NUM0)
r = drv(r, 'Auto inventory (% of Auto rev)', [0.345, 0.325, 0.308, 0.296, 0.285])
r = drv(r, 'Auto receivables (% of Auto rev)', [0.08]*5)
r = drv(r, 'Auto advances & debtors (% rev)', [0.085, 0.083, 0.080, 0.078, 0.076])
r = drv(r, 'Auto payables (% of Auto rev)', [0.245, 0.238, 0.233, 0.229, 0.226])
r = drv(r, 'Group opex S&M+Admin (% of group rev)', [0.082, 0.081, 0.080, 0.079, 0.078])
r = drv(r, 'Group other income (% of group rev)', [0.011]*5)
r = drv(r, 'Group provisions (% of group rev)', [-0.003]*5)
r = drv(r, 'GB Capital gross margin', [0.188, 0.19, 0.192, 0.194, 0.196])
r = drv(r, 'Associates income (EGP mn)', [1180, 1360, 1560, 1760, 1960], NUM0)
r = drv(r, 'Net finance cost (EGP mn)', [-4100, -3800, -3500, -3300, -3100], NUM0)
r = drv(r, 'Minority interest (% of NP before MI)', [-0.02]*5)
r = drv(r, 'Increase in borrowings, net (EGP mn)', [4000, 3000, 2800, 2500, 2300], NUM0)
r = drv(r, 'Dividend payout (of attributable NP)', [0.14, 0.15, 0.16, 0.18, 0.20])
r = drv(r, 'Intercompany eliminations (% of gross revenue)', [0.011]*5)
wa.column_dimensions['C'].width = 11
ROWSA = {k: v for k, v in DRV.items()}
json.dump(ROWSA, open('_asm_rows.json', 'w'))
wb.save('GBCO_Valuation_Model_08072026_public.xlsx')
print('part1 ok; assumptions rows:', len(ROWSA))
