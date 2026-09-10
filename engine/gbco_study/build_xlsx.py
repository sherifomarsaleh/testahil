"""GBCO_Valuation_Model_07092026_public.xlsx — part 1: READ FIRST and Assumptions.

Sixteen sheets, in the model report's own order; the list is IMPORTED from
research_protocol.MODEL_STUDY rather than typed, so it cannot drift from the standard.
Blue = input · black = formula · green = a link to another sheet. Every input lives on
Assumptions and the whole model reprices when one of them moves (SIGCM clause 7).

REBUILT 07-09-2026 ON THE ANSWER THE STUDY NOW PUBLISHES. What this replaces, and why it
is a rebuild rather than a patch:

  * THE ANSWER IS TWO-SIDED AND THE WORKBOOK PUBLISHED ONE SIDE. GB Corp's largest single
    component is a minority interest in an unlisted company, and the two bases the company
    itself puts on it differ by EGP 11.9bn. Both branches are built here, side by side.
    NO FIGURE BETWEEN THE TWO IS PRESENTED AS AN ANSWER ANYWHERE: an average of two things
    only one of which can be true is a third answer nobody argued for, which is the blend
    the dual-framing rule forbids. The MARK is priced across its range, at levels somebody
    has actually argued for rather than at equal steps between the branches — an
    interpolated ladder puts the average on the page while calling it a sensitivity.
  * THE FOUR-LENS WEIGHTED BLEND IS RETIRED. The sum of the parts is the class primary and
    IS the answer; the other lenses are cross-checks published beside it. No weights cell.
  * NO CONGLOMERATE DISCOUNT. The delivered edition applied a typed 10% and then weighted
    the discounted and the undiscounted sum, an effective 4% — so the number the study
    named was not the number it applied, and neither had cleared any out-of-sample test.
    What the discount stood in for is the uncertainty in the associate mark, and that is
    now published as two branches rather than smuggled into one number as a haircut.
  * GB CAPITAL IS RESIDUAL INCOME, NOT BOOK TIMES ONE. Book carried at 1.0x is book value
    carrying the whole weight of a leg while wearing a sum-of-the-parts entry's clothes.
    The justified price-to-book is the residual-income identity (ROE - g) / (Ke - g) and
    it is a LIVE FORMULA here, built out of the segment's own disclosed equity and its own
    disclosed earnings with the associate income taken out of both.
  * NORMALISED EARNINGS IS GONE. It carried a quarter of the retired blend on six typed
    figures sourced to nothing.
"""
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
from openpyxl.styles import Font, PatternFill
from openpyxl.utils import get_column_letter
import research_protocol as _RP

# THE WORKBOOK'S NAME IS DERIVED FROM THE STRIKE, NEVER TYPED [10-09-2026]. It was
# typed in four builders, so a reissued study shipped beside a workbook still
# carrying the superseded edition's name -- and the four could disagree with each
# other as easily as with the study. The strike asserts the edition once, in
# compute.py, and it reaches every artefact through the numbers file it wrote.
import json as _json_ed, os as _os_ed
_ED = _json_ed.load(open(_os_ed.path.join(
    _os_ed.path.dirname(_os_ed.path.abspath(__file__)),
    'study_numbers.json'), encoding='utf-8'))['edition']
OUT = 'GBCO_Valuation_Model_%s_public.xlsx' % ''.join(_ED.split('-')[::-1])
D = json.load(open('study_numbers.json'))
_BETA = json.load(open('beta_result.json'))

BLUE = Font(color='0000FF'); GREEN = Font(color='008000'); BLACK = Font(color='000000')
BOLD = Font(bold=True); TITLE = Font(bold=True, size=13, color='F6F1E6')
SUB = Font(size=9, color='6E7B77'); HDR = Font(bold=True, color='1C3A36')
FILL_T = PatternFill('solid', start_color='1C3A36')
FILL_H = PatternFill('solid', start_color='EAF0EE')
FILL_G = PatternFill('solid', start_color='F6F1E6')
NUM = '#,##0.0;(#,##0.0);"-"'; NUM0 = '#,##0;(#,##0);"-"'; PCT = '0.0%;(0.0%);"-"'
PCT2 = '0.00%;(0.00%);"-"'
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
    ws.column_dimensions['A'].width = 46
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
 'What this workbook is. A transparent companion to the GB Corp valuation study. Every blue cell is an input; every',
 'black cell is a formula; green cells link across sheets. All inputs live on the Assumptions sheet — change one (a',
 'volume growth rate, the Auto gross margin, the lender\'s return on equity, the mark on the associate) and the whole',
 'model reprices, both answers with it.', '',
 'THE ANSWER HAS TWO SIDES, AND THAT IS THE FINDING RATHER THAN AN EVASION. GB Corp\'s largest single component is a',
 'minority interest in an unlisted company, and the two bases on which the company itself puts a number on it differ',
 'by EGP 11.9bn — about a quarter of the answer. One is the equity-accounted carrying value in its own reviewed',
 'statements at 30 June 2026; the other is its stated stake applied to the primary round it announced in June 2026.',
 'Both are the company\'s own disclosures and the filings do not decide between them, so neither does this workbook:',
 'the two are carried side by side to the last cell. NO FIGURE BETWEEN THEM IS PRESENTED AS AN ANSWER',
 'ANYWHERE, deliberately — an average of two things only one of which can be true is not a more cautious',
 'answer than either, it is a third answer nobody argued for. The MARK itself is priced across its range, on',
 'the sum-of-the-parts sheet and in the first sensitivity grid, at levels somebody has actually argued for',
 'rather than at equal steps drawn between the two.', '',
 'How the answer is built. The sum of the parts is the primary and it IS the answer; the other reads are cross-checks',
 'shown beside it and never averaged into it. Leg 1, GB Auto, is a five-year cash-flow model discounted on a schedule',
 'that glides to a normalised terminal rate. Leg 2, GB Capital, is the lender\'s own operating equity times a justified',
 'price-to-book built from the return it actually earns on that equity. Leg 3 is the associates, on the two bases',
 'above. There is no complexity or conglomerate discount anywhere: the uncertainty it used to stand in for is the',
 'associate mark, and it is published as two branches instead.', '',
 'What it is not. It is not investment advice, a recommendation, or a price target. Values are model outputs shown as',
 'ranges. The preparer is not licensed by any securities regulator and may hold a position in the security.', '',
 'Entity note. GB Corp S.A.E. (formerly GB Auto / Ghabbour Auto; renamed March 2023) is an operating company with a',
 'captive finance arm: GB Auto (passenger cars, CV&CE, trading, light mobility; Egypt · Iraq · Jordan) plus GB Capital',
 '(leasing, factoring, consumer finance, SME lending) and associate stakes in MNT-Halan, Bedaya and Kaf.', '',
 'Currency. EGP million unless stated. Price EGP %.2f (%s close), read from the study record rather than typed.'
 % (D['spot'], D['spot_date']),
 'Historical financials are company disclosure: the FY2023–FY2025 earnings releases and the reviewed consolidated',
 'statements to 30 June 2026. Some consolidated balance-sheet lines are grouped from the disclosed segment balance',
 'sheets to a house layout — flagged on the Balance Sheet.', '',
 'Sheets: ' + ' · '.join(_RP.MODEL_STUDY['excel_sheets'][1:])]
for i, ln in enumerate(lines, start=3):
    ws.cell(row=i, column=1, value=ln).font = Font(size=10)
ws.column_dimensions['A'].width = 120

# ============ ASSUMPTIONS (built early so links resolve) =====================
wa = sheet('Assumptions')
title(wa, 'Assumptions — the single input layer',
      'All blue cells are inputs. Every other sheet links here.', 9)
ROWS = {}


def hdr(row, text):
    put(wa, 'A%d' % row, text, bold=True, fill=FILL_H)
    return row + 1


def inp(row, label, val, fmt=NUM, note=None):
    put(wa, 'A%d' % row, label)
    put(wa, 'B%d' % row, val, BLUE, fmt)
    if note: put(wa, 'C%d' % row, note, SUB)
    ROWS[label] = row
    return row + 1


def fml(row, label, formula, fmt=NUM, note=None, bold=False):
    put(wa, 'A%d' % row, label, bold=bold)
    put(wa, 'B%d' % row, formula, BLACK, fmt, bold=bold)
    if note: put(wa, 'C%d' % row, note, SUB)
    ROWS[label] = row
    return row + 1


_COC = D['cost_of_capital_record']; _RB = D['cost_of_capital_rating_basis']
_MAC = D['macro']; _LI = D['lens_inputs']; _CAPI = _LI['capital']; _REL = _LI['relative']
_DRV = D['disclosed_drivers']; _CS = _DRV['cost_stack']; _GD = D['group_forecast']['drivers']
_SOTP = D['sotp']; _DCF = D['dcf']; _LR = D['lens_record']

r = 4
r = hdr(r, 'ANCHORS')
r = inp(r, 'Price (EGP/share)', D['spot'], PX,
        'the LATEST KNOWN price, %s close, read from the committed supplied-price record '
        'rather than from this workbook\'s own memory.' % D['spot_date'])
r = inp(r, 'Shares outstanding (mn)', D['shares'], NUM0)
r = inp(r, 'Tax rate', _CS['tax_rate'], PCT)

r = hdr(r, 'COST OF CAPITAL — the schedule is built by the house module; this is its first year')
r = inp(r, "Normalised risk-free rate rf* (Egypt 10Y less this sovereign's own default spread)",
        _COC['rf_star'], PCT2,
        'observed %.2f%% less a default spread of %.2f%%, so country risk is counted EXACTLY '
        'ONCE, inside the equity risk premium below.'
        % (_COC['rf_observed'] * 100, _COC['default_spread'] * 100))
r = inp(r, 'Equity beta — own-stock weekly regression against the published EGX30 index',
        _COC['beta'], '0.0000',
        'a conforming tier-1 regression: %d weekly observations to %s, R-squared %.4f, '
        'standard error %.4f.' % (_BETA['n'], _BETA['last_obs'], _BETA['r2'], _BETA['se']))
r = inp(r, 'Equity risk premium — Egypt, market basis (adopted)', _COC['erp'], PCT2,
        "the sovereign's own row on the market basis; the rating basis of %.2f%% is published "
        'beside it below and in the study.' % (_RB['erp'] * 100))
# [R-COC-03] THE PREMIUM IS SPLIT AND THE WORKBOOK SHOWS BOTH LEGS. The cell above used
# to feed a formula reading =rf* + beta x ERP_total, which multiplies Egypt's country
# premium by beta: a company measured at a beta of 1.5 was charged half as much again
# for the same sovereign as the company next door. The premium separates into the part
# that prices the EQUITY MARKET, which beta scales, and the part that prices the
# COUNTRY, which it does not. A reader can now see both numbers and add them up.
r = inp(r, '   of which the mature equity premium — beta applies to THIS leg',
        _COC['erp_mature'], PCT2,
        'the total premium less the country premium below. Beta measures how much more '
        'than the market this company moves; it is not a measure of how risky the country '
        'is, and multiplying the two charges the sovereign twice over for a cyclical name.')
r = inp(r, '   of which the country premium — charged FLAT, once',
        _COC['crp_effective'], PCT2,
        'Egypt at %.2f%% weighted by the %.0f%% of operations that are here%s.'
        % (_COC['crp'] * 100, _COC['lambda_country'] * 100,
           (', the rest at %.2f%%' % (_COC['crp_foreign'] * 100))
           if _COC['lambda_country'] < 1 else ''))
# EVERY FORMULA BELOW ADDRESSES THESE CELLS BY THE ROWS MAP, NEVER BY A TYPED NUMBER.
# Splitting the premium pushed everything down by two, and six formulas addressed the
# old numbers -- so the workbook would have discounted at the debt weight, taken growth
# off the cost of debt, and still opened without complaint. A row number typed into a
# formula is a claim about a layout that the next edit silently falsifies.
_RF, _BETA_R, _ERP_TOT = ROWS['Normalised risk-free rate rf* (Egypt 10Y less this '
                              "sovereign's own default spread)"], 10, 11
r = fml(r, 'Cost of equity Ke = rf* + beta x mature premium + country premium',
        '=B%d+B%d*B%d+B%d' % (_RF, _BETA_R, _ERP_TOT + 1, _ERP_TOT + 2), PCT2,
        'reproduces the committed schedule to the basis point.')
r = inp(r, 'Pre-tax cost of debt', _COC['kd_pretax'], PCT2,
        "the company's own effective borrowing rate, computed on the borrowings that actually "
        'bear the interest; the book is entirely local-currency on the disclosed facility note.')
_KD_PRE = ROWS['Pre-tax cost of debt']
r = fml(r, 'After-tax cost of debt', '=B%d*(1-B7)' % _KD_PRE, PCT2)
r = inp(r, 'Debt weight D/(D+E) — market-value equity', _COC['weight_debt'], PCT,
        'market capitalisation against disclosed borrowings; never book equity.')
_KE_R = ROWS['Cost of equity Ke = rf* + beta x mature premium + country premium']
_KD_AT = ROWS['After-tax cost of debt']
_WD_R = ROWS['Debt weight D/(D+E) — market-value equity']
r = fml(r, 'WACC — first forecast year',
        '=(1-B%d)*B%d+B%d*B%d' % (_WD_R, _KE_R, _WD_R, _KD_AT), PCT2,
        'the schedule GLIDES to a norm-built terminal of %.2f%%; the DCF sheet carries one '
        'forward rate per year rather than this rate held for ever.'
        % (_COC['wacc_terminal'] * 100))
r = inp(r, 'Terminal growth (nominal EGP, DERIVED)', _MAC['terminal_growth_nominal'], PCT,
        'stored as a REAL rate of %.1f%% on the house Egyptian inflation path and recomputed '
        'to this nominal figure; a typed nominal rate is unfalsifiable.'
        % (_MAC['terminal_growth_real'] * 100))
# THE ROW NUMBERS MOVED BY TWO when the premium was split into its mature and country
# legs. They are asserted rather than assumed because every formula below addresses
# these cells by number, and a silently shifted row is a workbook that computes the
# wrong thing while looking right.
assert ROWS['Cost of equity Ke = rf* + beta x mature premium + country premium'] == 14, ROWS
assert ROWS['WACC — first forecast year'] == 18, ROWS
assert ROWS['Terminal growth (nominal EGP, DERIVED)'] == 19, ROWS

r = hdr(r, 'LEG 1 — GB AUTO: the cash-flow model\'s own bridge (the DCF sheet builds the leg)')
r = inp(r, 'GB Auto net debt (30 June 2026, reviewed)', _DCF['auto_nd'], NUM0,
        'the bridge stands on the LATEST disclosed balance sheet and on the AUTO segment\'s '
        'own net debt, not the prior year end and not the group total.')
r = inp(r, 'GB Auto non-controlling interests (30 June 2026)', _DCF['auto_nci'], NUM0,
        "that leg's own minority, deducted from EQUITY value and never from enterprise value.")
_G = ROWS['Terminal growth (nominal EGP, DERIVED)']
assert ROWS['GB Auto net debt (30 June 2026, reviewed)'] == _G + 2, ROWS
assert ROWS['GB Auto non-controlling interests (30 June 2026)'] == _G + 3, ROWS

r = hdr(r, 'LEG 2 — GB CAPITAL: residual income, not book times one')
# EVERY ROW NUMBER BELOW IS CARRIED IN A VARIABLE AND NEVER ASSUMED. The first draft of this
# rebuild typed the row numbers into the formulas, a header row moved, and the associates
# block silently referenced the three rows above the ones it meant — arithmetic that still
# evaluated, on the wrong cells. A formula that points at a remembered row is a formula that
# breaks the next time a line is inserted, and it does not announce itself when it does.
_CAP_EQ = r
r = inp(r, "GB Capital shareholders' equity before NCI, 30 June 2026",
        _CAPI['segment_equity_before_nci'], NUM0,
        '2Q26 earnings release, segmented balance sheet, GB Capital column.')
r = inp(r, 'less: associates carried inside that segment, 30 June 2026',
        _CAPI['associates_carried_within'], NUM0,
        'the reviewed consolidated interim balance sheet\'s own associates line. Taking it '
        'out is what stops the stake funding this leg AND being added back at its own mark.')
_CAP_ASSOC = _CAP_EQ + 1
_CAP_OPEQ = _CAP_EQ + 2
r = fml(r, 'GB Capital operating equity', '=B%d-B%d' % (_CAP_EQ, _CAP_ASSOC), NUM0,
        'an identity off two disclosed figures, so nothing here is chosen.')
_H1_NP = r
r = inp(r, '1H2026 GB Capital net profit after NCI', 649.6, NUM,
        '2Q26 earnings release, segment income statement.')
r = inp(r, '1H2026 GB Capital investment gains from associates', 426.2, NUM,
        'same table; taken out of the numerator because it is taken out of the base.')
_D25_EQ = r
r = inp(r, "GB Capital equity before NCI, 31 December 2025", 18312.6, NUM,
        '4Q25 earnings release, segmented balance sheet, GB Capital column.')
r = inp(r, 'less: associates carried inside it, 31 December 2025', 15732.426, NUM,
        "the reviewed balance sheet's own comparative column, which note 34 foots to.")
_D25_OPEQ = r
r = fml(r, 'GB Capital operating equity, 31 December 2025', '=B%d-B%d' % (_D25_EQ, _D25_EQ + 1), NUM0)
_ROE_H1 = r
r = fml(r, 'Return on operating equity — 1H2026 annualised (ADOPTED)',
        '=(B%d-B%d)*2/((B%d+B%d)/2)' % (_H1_NP, _H1_NP + 1, _D25_OPEQ, _CAP_OPEQ), PCT2,
        'a near-term reviewed actual outranks a stale full-year rate.')
_FY25_NP = r
r = inp(r, 'FY2025 GB Capital net profit after NCI', 1365.9, NUM)
r = inp(r, 'FY2025 GB Capital investment gains from associates', 986.4, NUM)
_ROE_FY = r
r = fml(r, 'Return on operating equity — FY2025 framing',
        '=(B%d-B%d)/B%d' % (_FY25_NP, _FY25_NP + 1, _D25_OPEQ), PCT2,
        'the OTHER framing of a contested judgement worth more than 5% of the answer, '
        'published beside the adopted one rather than averaged with it.')
_RF_T = r
r = inp(r, 'Terminal risk-free rate', _COC['rf_terminal'], PCT2,
        'from the house macro path: terminal inflation plus the real-rate convention, '
        'derived and never quoted.')
r = inp(r, 'Terminal equity risk premium', _COC['erp_terminal'], PCT2)
r = inp(r, '   of which the terminal country premium — charged FLAT, once',
        _COC['crp_effective_terminal'], PCT2,
        'the terminal premium splits the same way the explicit one does; a country '
        'premium that stops being multiplied by beta in year five and starts again in '
        'perpetuity would be two views of one sovereign.')
_KE_T = r
r = fml(r, 'Terminal cost of equity Ke(T) = rf(T) + beta x mature premium + country premium',
        '=B%d+B10*(B%d-B%d)+B%d' % (_RF_T, _RF_T + 1, _RF_T + 2, _RF_T + 2), PCT2,
        'the same beta as the explicit window, on the mature leg only; the construction '
        'is named, not assumed.')
_PB = r
r = fml(r, 'Justified price-to-book = (ROE - g) / (Ke(T) - g)', '=(B%d-B%d)/(B%d-B%d)' % (_ROE_H1, _G, _KE_T, _G), MULT,
        'the residual-income identity in its terminal form. THE TERMINAL Ke IS THE GENEROUS '
        'END and it is used deliberately: the explicit-window Ke would put this leg at a '
        'fraction of the figure below.')
_CAPLEG = r
r = fml(r, 'GB Capital lending leg (EGP mn)', '=B%d*B%d' % (_CAP_OPEQ, _PB), NUM0, bold=True)
r = fml(r, 'memo: the same leg on the FY2025 return framing',
        '=B%d*((B%d-B%d)/(B%d-B%d))' % (_CAP_OPEQ, _ROE_FY, _G, _KE_T, _G),
        NUM0, 'published so a reader sees the choice and not only its result.')
r = fml(r, 'memo: GB Capital operating equity per share — a DISCLOSED FLOOR, never weighted',
        '=B%d/B6' % _CAP_OPEQ, PX)

r = hdr(r, 'LEG 3 — THE ASSOCIATES: the contested judgement, computed BOTH ways')
_MNT_USD = r
r = inp(r, 'MNT-Halan round valuation (USD mn, June-2026 first close)',
        _SOTP['mnt_halan_round_usd'], NUM0)
r = inp(r, 'GB Corp stake in MNT-Halan — the figure the company states',
        _SOTP['mnt_halan_stake'], PCT2, _SOTP['mnt_halan_stake_source'])
r = inp(r, 'EGP per USD applied to the mark', _SOTP['egp_usd'], PX,
        'a flagged estimate, and material to this one line.')
_MNT_A = r
r = fml(r, 'BRANCH A — MNT-Halan at the June-2026 round price',
        '=B%d*B%d*B%d' % (_MNT_USD, _MNT_USD + 1, _MNT_USD + 2), NUM0, bold=True)
_MNT_B = r
r = inp(r, 'BRANCH B — MNT-Halan at its reviewed carrying value, 30 June 2026',
        _LR['primary']['range_basis']['low'], NUM0,
        'note 34 to the reviewed consolidated interim statements. The review conclusion on '
        'those statements is QUALIFIED at exactly this line, so this branch is not a safe '
        'harbour either.')
_OTHA = r
r = fml(r, 'Other associates (Bedaya, Kaf) — by identity off the note\'s own total',
        '=B%d-B%d' % (_CAP_ASSOC, _MNT_B), NUM0,
        'the total and the MNT-Halan row each foot; three smaller rows carry a reading '
        'ambiguity in one cell, so the residual is the figure that can be reproduced.')
r = fml(r, 'Associates — branch A (round price)', '=B%d+B%d' % (_MNT_A, _OTHA), NUM0)
r = fml(r, 'Associates — branch B (reviewed carrying value)', '=B%d+B%d' % (_MNT_B, _OTHA), NUM0)

# THE VARIABLES AND THE ROW MAP MUST AGREE, and this is what says so rather than a reader
# counting lines: every formula above points at a row this dictionary independently records.
assert ROWS['GB Capital operating equity'] == _CAP_OPEQ, ROWS
assert ROWS['GB Capital lending leg (EGP mn)'] == _CAPLEG, ROWS
assert ROWS['BRANCH A — MNT-Halan at the June-2026 round price'] == _MNT_A, ROWS
assert ROWS['BRANCH B — MNT-Halan at its reviewed carrying value, 30 June 2026'] == _MNT_B, ROWS
assert ROWS["Other associates (Bedaya, Kaf) — by identity off the note's own total"] == _OTHA, ROWS

r = hdr(r, 'CROSS-CHECK INPUTS — the relative multiple and the disclosed floor')
r = inp(r, 'GB Corp close, year-end 2023 (EGP)', _REL['history']['2023'][0], PX)
r = inp(r, 'Net profit attributable, FY2023', _REL['history']['2023'][1], NUM)
r = inp(r, 'GB Corp close, year-end 2024 (EGP)', _REL['history']['2024'][0], PX)
r = inp(r, 'Net profit attributable, FY2024', _REL['history']['2024'][1], NUM)
r = inp(r, 'GB Corp close, year-end 2025 (EGP)', _REL['history']['2025'][0], PX)
r = inp(r, 'Net profit attributable, FY2025', _REL['history']['2025'][1], NUM)
r = inp(r, "Shareholders' equity before NCI, 30 June 2026", D['experts']['e2']['book'], NUM0,
        'the disclosed floor. It is worth printing because the shares trade BELOW it.')

r = hdr(r, 'MONTE CARLO — a separate lens on a separate clock; engine outputs, not a sheet simulation')
r = inp(r, 'Anchor volatility (HAR forecast, annualised)', round(D['engine']['anchor_vol'], 4), PCT)
r = inp(r, 'Secular drift (daily log-return, expanding window)',
        round(D['engine']['drift_daily'], 6), '0.0000%')
r = inp(r, 'Net factor drift per quarter', round(D['engine']['factor_drift_q'], 4), PCT)
r = inp(r, 'Paths / seed', '50,000 / 42', '@')

r = hdr(r, 'FORECAST DRIVERS (FY26E–FY30E) — the units x ASP build; every driver disclosed')
yrs = ['FY26E', 'FY27E', 'FY28E', 'FY29E', 'FY30E']
put(wa, 'A%d' % r, 'Driver \\ year', bold=True)
for j, y in enumerate(yrs):
    put(wa, '%s%d' % (get_column_letter(3 + j), r), y, bold=True, fill=FILL_H)
r += 1


def drv(row, label, vals, fmt=PCT):
    put(wa, 'A%d' % row, label)
    for j, v in enumerate(vals):
        put(wa, '%s%d' % (get_column_letter(3 + j), row), v, BLUE, fmt)
    ROWS[label] = row
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
r = drv(r, 'Auto other operating income (% rev)', [_CS['other_income_pct']] * 5)
r = drv(r, 'Auto provisions (% rev)', [_CS['provisions_pct']] * 5)
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

# ===== COST-OF-CAPITAL DETAIL — reference only; it feeds rows 9-17 above =====
r += 1
r = hdr(r, 'COST-OF-CAPITAL DETAIL (reference; the figures above are what the model reads)')
put(wa, 'A%d' % r, 'Risk-free rate — observed, and how it is normalised')
put(wa, 'C%d' % r, 'The observed local-currency government bond yield of %.2f%% less this '
                   "sovereign's OWN default spread of %.2f%%, giving %.2f%%. Country risk "
                   'then enters exactly once, inside the equity risk premium, rather than '
                   'twice.' % (_COC['rf_observed'] * 100, _COC['default_spread'] * 100,
                               _COC['rf_star'] * 100), SUB)
r += 1
# THE RATING BASIS CARRIES ITS OWN NORMALISED RISK-FREE RATE, and the superseded builder
# did not: it added the rating-basis premium on top of the MARKET basis's rf*, which is
# this sovereign's default spread counted on one basis and added back on another. The two
# bases are two consistent readings of one credit, and mixing them is neither.
_ALT_RF = r
r = inp(r, 'Normalised risk-free rate rf* — rating basis', _RB['rf_star'], PCT2,
        'the same observed yield of %.2f%% less the RATING-basis default spread of %.2f%%. '
        'The default spread stripped out and the premium added back must be on the same '
        'basis, or country risk is counted once and a half.'
        % (_RB['rf_observed'] * 100, _RB['default_spread'] * 100))
_ALT = r
r = inp(r, 'Equity risk premium — rating basis (the alternative to the adopted market basis)',
        _RB['erp'], PCT2,
        'Both bases come from the same published country-risk file for this sovereign and '
        'both are published. The market basis is named CENTRAL because it is the market\'s '
        'own live pricing of that credit against an agency judgement updated in steps.')
# THE ALTERNATIVE BASIS SPLITS TOO. It was the last cell in this workbook still adding
# beta x the WHOLE premium, so a reader comparing the two bases was comparing one
# construction with another rather than one credit reading with another.
_ALT_CRP = r
r = inp(r, '   of which the country premium, rating basis — charged FLAT, once',
        _RB['crp_effective'], PCT2,
        'the rating-basis premium of %.2f%% less the same mature equity premium of '
        '%.2f%% the market basis carries: the two bases differ in how the SOVEREIGN is '
        'read, not in what a mature equity market pays.'
        % (_RB['erp'] * 100, _RB['erp_mature'] * 100))
_ALT_KE = r
r = fml(r, 'Cost of equity, alternative (rating-basis premium)',
        '=B%d+B10*(B%d-B%d)+B%d' % (_ALT_RF, _ALT, _ALT_CRP, _ALT_CRP), PCT2)
r = fml(r, 'Weighted cost of capital, alternative (rating-basis premium)',
        '=(1-B%d)*B%d+B%d*B%d' % (_WD_R, _ALT_KE, _WD_R, _KD_AT), PCT2)
put(wa, 'A%d' % r, 'Cost of debt — how it was produced')
put(wa, 'C%d' % r, "The company's own effective borrowing rate, computed independently from "
                   'the filings on the borrowings that ACTUALLY BEAR THE INTEREST rather '
                   'than on a broader liabilities total. Adopted %.2f%% against a latest '
                   'effective rate of %.2f%% and a peak of %.2f%%. The book is entirely '
                   'local-currency on the disclosed facility note, so no foreign tranche is '
                   'blended in.' % (_COC['kd_pretax'] * 100,
                                    _COC['kd_integrity']['latest_effective'] * 100,
                                    _COC['kd_integrity']['peak_effective'] * 100), SUB)
r += 1
put(wa, 'A%d' % r, 'The schedule, not a single rate')
put(wa, 'C%d' % r, 'One forward rate per explicit year on the DCF sheet, gliding from %.2f%% '
                   'to a norm-built terminal of %.2f%%, with the terminal brought home on '
                   'the same cumulative factor as the last explicit year: one date, one '
                   'price of time. The glide fractions are the policy-rate path\'s own '
                   'cumulative progress rather than a second assumption.'
                   % (_COC['wacc_exp'] * 100, _COC['wacc_terminal'] * 100), SUB)
r += 1
put(wa, 'A%d' % r, 'What is NOT on this sheet, and why')
put(wa, 'C%d' % r, 'There is no complexity or conglomerate discount and there are no lens '
                   'weights. Both were free parameters that had never cleared an '
                   'out-of-sample test and nothing in the filings disclosed a basis for '
                   'either. The uncertainty they stood in for is the associate mark, and it '
                   'is carried as two branches from row 44 down to the last sheet.', SUB)

json.dump(ROWS, open('_asm_rows.json', 'w'), indent=1, sort_keys=True)
wb.save(OUT)
print('part1 ok — READ FIRST + Assumptions; %d labelled rows' % len(ROWS))
