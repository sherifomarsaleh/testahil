"""GBCO_Valuation_Model_07092026_public.xlsx — 16 sheets mirroring the TMPV canonical model.
Blue = inputs · black = formulas · green = cross-sheet links. All inputs live on Assumptions."""
import os as _os_pathfix
# EVERY PATH IN THIS BUILDER IS RELATIVE, SO THE RUN'S DIRECTORY DECIDED WHERE ITS
# INPUT WAS READ AND ITS OUTPUT WAS WRITTEN. Run from anywhere but this folder it
# either crashed or, worse, wrote a deliverable into the caller's directory.
_HERE = _os_pathfix.path.dirname(_os_pathfix.path.abspath(__file__))
_os_pathfix.chdir(_HERE)
import sys as _sys_pathfix
_sys_pathfix.path.insert(0, _HERE)
_sys_pathfix.path.insert(0, _os_pathfix.path.join(_HERE, '..'))

import json
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

D = json.load(open('study_numbers.json'))
_BETA = json.load(open('beta_result.json'))
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
 'the fintech associate = the company\'s own stated stake applied to the June-2026 funding round.', '',
 'Currency. EGP million unless stated. Price EGP %.2f (%s close), read from the study record. Historical' % (D['spot'], D['spot_date']),
 'financials are company disclosure: the FY2023-FY2025 earnings releases and the reviewed consolidated statements to',
 '30 June 2026. Some consolidated balance-sheet lines are grouped from the disclosed segment balance sheets to a house',
 'layout — flagged on the Balance Sheet.', '',
 'Sheets: Summary · Fundamental Valuation · Assumptions · SOTP Bridge · Segments · Relative & Normalized · DCF ·',
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
_COC = D['cost_of_capital_record']; _MAC = D['macro']; _LI = D['lens_inputs']
_DRV = D['disclosed_drivers']; _CS = _DRV['cost_stack']; _GD = D['group_forecast']['drivers']
_SOTP = D['sotp']; _DCF = D['dcf']; _W = D['lenses']['weights']
r = hdr(wa, r, 'ANCHORS')
r = inp(wa, r, 'Price (EGP/share)', D['spot'], PX,
        'the latest known price, %s close. REBUILT: the superseded workbook carried a price '
        'three months older than the study it accompanied.' % D['spot_date'])
r = inp(wa, r, 'Shares outstanding (mn)', D['shares'], NUM0)
r = inp(wa, r, 'Tax rate', _CS['tax_rate'], PCT)
r = hdr(wa, r, 'COST OF CAPITAL — read from the study record; the full schedule is in the detail block below')
r = inp(wa, r, 'Normalised risk-free rate rf* (Egypt 10Y less this sovereign\'s own default spread)',
        _COC['rf_star'], PCT,
        'REBUILT: observed %.2f%% less a default spread of %.2f%%, so country risk is counted EXACTLY ONCE, '
        'inside the equity risk premium below.' % (_COC['rf_observed']*100, _COC['default_spread']*100))
r = inp(wa, r, 'Equity beta — own-stock weekly regression vs the published EGX30 index', _COC['beta'], '0.0000',
        'REBUILT: a conforming tier-1 regression replaces an assumed 1.0.')
r = inp(wa, r, 'Equity risk premium — Egypt, market basis (adopted)', _COC['erp'], PCT,
        'the sovereign\'s own row, market basis; the rating basis of %.2f%% is published beside it in the study.'
        % (D['cost_of_capital_rating_basis']['erp']*100))
put(wa, f'A{r}', 'Cost of equity Ke = rf* + beta x ERP'); put(wa, f'B{r}', '=B9+B10*B11', BLACK, PCT); KE=f'B{r}'
put(wa, f'C{r}', 'reproduces the study record to the basis point.', SUB); r += 1
r = inp(wa, r, 'Pre-tax cost of debt', _COC['kd_pretax'], PCT,
        'the company\'s own effective borrowing rate, computed on the borrowings that actually bear the interest; '
        'the book is entirely local-currency on the disclosed facility note.')
put(wa, f'A{r}', 'After-tax Kd'); put(wa, f'B{r}', '=B13*(1-B7)', BLACK, PCT); r+=1
r = inp(wa, r, 'Debt weight D/(D+E) — market-value equity', _COC['weight_debt'], PCT,
        'market capitalisation against disclosed borrowings; never book equity.')
wa[f'B{r-1}'].font = BLACK
put(wa, f'A{r}', 'WACC — first forecast year'); put(wa, f'B{r}', f'=(1-B15)*B12+B15*B14', BLACK, PCT)
put(wa, f'C{r}', 'the schedule GLIDES to a norm-built terminal of %.2f%%; the DCF sheet carries one forward rate '
    'per year rather than this rate held for ever.' % (_COC['wacc_terminal']*100), SUB)
WACC='Assumptions!$B$16'; r+=1
r = inp(wa, r, 'Terminal growth (nominal EGP, DERIVED)', _MAC['terminal_growth_nominal'], PCT,
        'stored as a REAL rate of %.1f%% on the house Egyptian inflation path and recomputed to this nominal '
        'figure; a typed nominal rate is unfalsifiable.' % (_MAC['terminal_growth_real']*100))
TG='Assumptions!$B$17'
r = hdr(wa, r, 'SOTP — the three legs (split-the-legs, §3.5-F5)')
r = inp(wa, r, 'GB Auto net debt (30 June 2026, reviewed)', _DCF['auto_nd'], NUM0,
        'REBUILT: the bridge stands on the LATEST disclosed balance sheet and on the AUTO '
        "segment's own net debt, not the prior year end and not the group total.")
r = inp(wa, r, 'GB Auto non-controlling interests (30 June 2026)', _DCF['auto_nci'], NUM0,
        "that leg's own minority, deducted from equity value and never from enterprise value.")
r = inp(wa, r, 'GB Capital adjusted operating equity', _SOTP['cap_val'], NUM0,
        'from the disclosed adjusted-return basis')
r = inp(wa, r, 'GB Capital multiple (× adjusted book)', 1.0, MULT, 'return-justified ~1× book')
r = inp(wa, r, 'Associates carrying value (MNT-Halan + Bedaya + Kaf)', '=B79+B80', NUM0,
        'FY25 carrying 13,689.5 — split in the MNT-Halan detail block (rows 75–80)')
wa[f'B{r-1}'].font = BLACK  # this is a formula, not an input — override inp()'s default blue
r = inp(wa, r, 'Associates mark (× carrying)', 1.0, MULT)
r = inp(wa, r, 'Complexity / conglomerate discount', _SOTP['disc'], PCT,
        'sensitized across the whole grid on the Sensitivity sheet')
r = hdr(wa, r, 'RELATIVE & NORMALIZED')
r = inp(wa, r, 'FY26E group net profit for the relative lens', _LI['relative']['np_fy26e'], NUM0,
        'aligned to the income-statement build')
r = inp(wa, r, 'Justified multiple (base)', _LI['relative']['pe']['base'], MULT)
r = inp(wa, r, 'Mid-cycle group profit after tax (normalised)', _LI['normalized']['pat']['base'], NUM0)
r = inp(wa, r, 'Justified through-cycle multiple', _LI['normalized']['pe']['base'], MULT)
r = hdr(wa, r, 'SYNTHESIS WEIGHTS')
r = inp(wa, r, 'SOTP weight', _W['sotp'], PCT)
r = inp(wa, r, 'Pre-discount NAV weight', _W['prediscount'], PCT)
r = inp(wa, r, 'Relative weight', _W['relative'], PCT)
r = inp(wa, r, 'Normalized-earnings weight', _W['normalized'], PCT)
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
r = drv(r, 'PC volume growth', _DRV['growth']['pc_volume'])
r = drv(r, 'PC ASP growth', _DRV['growth']['pc_asp'])
r = drv(r, 'CV&CE volume growth', _DRV['growth']['cv_volume'])
r = drv(r, 'CV&CE ASP growth', _DRV['growth']['cv_asp'])
r = drv(r, 'Light-Mobility volume growth', _DRV['growth']['lm_volume'])
r = drv(r, 'Light-Mobility ASP growth', _DRV['growth']['lm_asp'])
r = drv(r, 'Trading revenue growth', _DRV['growth']['trading'])
r = drv(r, 'GB Capital revenue growth', _GD['capital_growth'])
r = drv(r, 'GB Capital loan-book growth', _GD['capital_loanbook_growth'])
r = drv(r, 'Auto gross margin', _CS['gross_margin'])
r = drv(r, 'Auto GS&A (% of revenue)', _CS['gsa_pct'])
r = drv(r, 'Auto other operating income (% rev)', [_CS['other_income_pct']]*5)
r = drv(r, 'Auto provisions (% rev)', [_CS['provisions_pct']]*5)
r = drv(r, 'Auto D&A (% of revenue)', _CS['dna_pct'])
r = drv(r, 'Auto capex (EGP mn)', _CS['capex'], NUM0)
r = drv(r, 'Rental-fleet & other capex (EGP mn)', _GD['rental_and_other_capex'], NUM0)
r = drv(r, 'GB Capital D&A (EGP mn)', _GD['capital_dna'], NUM0)
r = drv(r, 'Auto inventory (% of Auto rev)', _GD['auto_inventory_pct'])
r = drv(r, 'Auto receivables (% of Auto rev)', _GD['auto_receivables_pct'])
r = drv(r, 'Auto advances & debtors (% rev)', _GD['auto_advances_pct'])
r = drv(r, 'Auto payables (% of Auto rev)', _GD['auto_payables_pct'])
r = drv(r, 'Group opex S&M+Admin (% of group rev)', _GD['group_opex_pct'])
r = drv(r, 'Group other income (% of group rev)', _GD['group_other_income_pct'])
r = drv(r, 'Group provisions (% of group rev)', _GD['group_provisions_pct'])
r = drv(r, 'GB Capital gross margin', _GD['capital_gross_margin'])
r = drv(r, 'Associates income (EGP mn)', _GD['associates_income'], NUM0)
r = drv(r, 'Net finance cost (EGP mn)', _GD['net_finance_cost'], NUM0)
r = drv(r, 'Minority interest (% of NP before MI)', _GD['minority_pct'])
r = drv(r, 'Increase in borrowings, net (EGP mn)', _GD['net_new_borrowings'], NUM0)
r = drv(r, 'Dividend payout (of attributable NP)', _GD['dividend_payout'])
r = drv(r, 'Intercompany eliminations (% of gross revenue)', _GD['eliminations_pct'])
wa.column_dimensions['C'].width = 11

# ===== MNT-HALAN DETAIL (rows 75-80) — added 09-07-2026 to reflect the confirmed stake =====
r = hdr(wa, 75, 'MNT-HALAN DETAIL (feeds the associates line, row 23)')
r = inp(wa, r, 'MNT-Halan round valuation (USD mn, June-2026 first close)',
        _SOTP['mnt_halan_round_usd'], NUM0)
r = inp(wa, r, 'GB stake — the figure the company states', _SOTP['mnt_halan_stake'], PCT,
        _SOTP['mnt_halan_stake_source'] + '. Applying it to the round makes this one line '
        '%.0f%% of market capitalisation after the complexity discount, which the study flags '
        'as a genuine valuation puzzle — a steep implied private-mark discount, or '
        'mispricing — rather than a sourcing gap.'
        % (_SOTP['mnt_halan_value'] * (1 - _SOTP['disc']) / D['mktcap'] * 100))
r = inp(wa, r, 'EGP/USD applied to the mark', _SOTP['egp_usd'], PX,
        'a flagged estimate, and material to this one line')
put(wa, f'A{r}', 'MNT-Halan implied value (EGP mn)'); put(wa, f'B{r}', '=B76*B77*B78', BLACK, NUM0); r += 1
r = inp(wa, r, 'Other associates (Bedaya, Kaf) — residual carrying', _SOTP['other_assoc'], NUM0)

# ===== COST-OF-CAPITAL DETAIL (rows 82+) — reference only, feeds rows 9-17 =====
# REBUILT 07-09-2026. Every sentence in this block described the SUPERSEDED build: a
# risk-free rate from a data vendor, a beta of 1.0 with a paragraph explaining why, weights
# struck on a price three months old, and two repository filenames a reader outside this
# house has no use for. The schedule is now produced by the house module and every figure
# below is READ from the study's committed record.
_RB = D['cost_of_capital_rating_basis']
r = hdr(wa, 82, 'COST-OF-CAPITAL DETAIL (feeds rows 9-17 above; this block is reference only)')
put(wa, f'A{r}', 'Risk-free rate — observed, and how it is normalised')
put(wa, f'C{r}', 'The observed local-currency government bond yield of %.2f%% less this '
                 "sovereign's OWN default spread of %.2f%%, giving %.2f%%. Country risk then "
                 'enters exactly once, inside the equity risk premium, rather than twice.'
                 % (_COC['rf_observed']*100, _COC['default_spread']*100, _COC['rf_star']*100), SUB)
r += 1
r = inp(wa, r, 'Equity risk premium — rating basis (alternative to the adopted market basis)',
        _RB['erp'], PCT,
        'Both bases come from the same published country-risk file for this sovereign and both '
        'are published. The market basis is named CENTRAL because it is the market\'s own live '
        'pricing of that credit against an agency judgement updated in steps.')
put(wa, f'A{r}', 'Cost of equity, alternative (rating-basis premium)')
put(wa, f'B{r}', '=B9+B10*B84', BLACK, PCT); r += 1
put(wa, f'A{r}', 'Weighted cost of capital, alternative (rating-basis premium)')
put(wa, f'B{r}', '=(1-B15)*B85+B15*B14', BLACK, PCT); r += 1
put(wa, f'A{r}', 'Beta — how it was produced')
put(wa, f'C{r}', 'A %s regression of the shares against the published index of the exchange the '
                 'stock is listed on, over %.2f years to %s on %d observations: beta %.4f, '
                 'R-squared %.4f, standard error %.4f. It passes the usability gate and REPLACES '
                 'the assumed 1.0 this workbook previously carried, which was the correct fallback '
                 'at the time because the only regression then attempted, on five annual '
                 'observations, was unusable.'
                 % (_BETA['frequency'], _BETA['window_years'], _BETA['last_obs'], _BETA['n'],
                    _BETA['beta'], _BETA['r2'], _BETA['se']), SUB)
r += 1
put(wa, f'A{r}', 'Cost of debt — how it was produced')
put(wa, f'C{r}', "The company's own effective borrowing rate, computed independently from the "
                 'filings on the borrowings that ACTUALLY BEAR THE INTEREST rather than on a '
                 'broader liabilities total. Adopted %.2f%% against a latest effective rate of '
                 '%.2f%% and a peak of %.2f%%. The book is entirely local-currency on the '
                 'disclosed facility note, so no foreign tranche is blended in.'
                 % (_COC['kd_pretax']*100, _COC['kd_integrity']['latest_effective']*100,
                    _COC['kd_integrity']['peak_effective']*100), SUB)
r += 1
put(wa, f'A{r}', 'Weights')
put(wa, f'C{r}', 'Market-value equity — the price on row 5 times the shares on row 6 — '
                 'against disclosed borrowings. Never book equity.', SUB)
r += 1
put(wa, f'A{r}', 'The schedule, not a single rate')
put(wa, f'C{r}', 'One forward rate per explicit year on the DCF sheet, gliding from %.2f%% to a '
                 'norm-built terminal of %.2f%%, with the terminal brought home on the same '
                 'cumulative factor as the last explicit year: one date, one price of time. The '
                 'glide fractions are the policy-rate path\'s own cumulative progress rather than '
                 'a second assumption.'
                 % (_COC['wacc_exp']*100, _COC['wacc_terminal']*100), SUB)
r += 1

ROWSA = {k: v for k, v in DRV.items()}
json.dump(ROWSA, open('_asm_rows.json', 'w'))
wb.save('GBCO_Valuation_Model_07092026_public.xlsx')
print('part1 ok; assumptions rows:', len(ROWSA))
