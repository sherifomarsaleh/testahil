"""Part 4: the answer sheets — SOTP Bridge, cross-checks, Summary, Fundamental Valuation,
Summary Financials, Monte Carlo, Sensitivity, Per-Share & Ratios, Peer & Sector — and the
sheet order, which is IMPORTED from research_protocol rather than typed.

THIS IS WHERE THE 07-09-2026 REBUILD LANDS.

  * TWO BRANCHES, SIDE BY SIDE, TO THE LAST CELL. The sum of the parts is the class primary
    and it IS the answer; it has two sides because GB Corp's largest single component is a
    minority interest in an unlisted company and the two bases the company itself puts on it
    differ by EGP 11.9bn. NO FIGURE BETWEEN THEM IS PRESENTED AS AN ANSWER ANYWHERE — not on
    the summary, not in the football field, and not as a rung of a ladder, which is where it
    would otherwise arrive wearing a sensitivity's clothes. An average of two things only one
    of which can be true is a third answer nobody argued for.
  * NO WEIGHTS CELL, ANYWHERE. The superseded workbook carried a four-lens weighted central
    on typed weights that had never cleared an out-of-sample test.
  * NO CONGLOMERATE DISCOUNT, ANYWHERE — including in the sensitivity, where the superseded
    edition sensitised the answer across a discount it also applied.
  * NORMALISED EARNINGS IS ABSENT AND THE SHEET SAYS SO. Removing a lens silently and
    removing it with its reason are two different things, and only one of them tells a
    reader what happened.
"""
import os as _os_pathfix
_HERE = _os_pathfix.path.dirname(_os_pathfix.path.abspath(__file__))
_os_pathfix.chdir(_HERE)
import sys as _sys_pathfix
_sys_pathfix.path.insert(0, _HERE)
_sys_pathfix.path.insert(0, _os_pathfix.path.join(_HERE, '..'))

import json
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.utils import get_column_letter
import research_protocol as _RP

OUT = 'GBCO_Valuation_Model_07092026_public.xlsx'
wb = load_workbook(OUT)
D = json.load(open('study_numbers.json'))
A = json.load(open('_asm_rows.json')); SR = json.load(open('_seg_rows.json'))
IS = json.load(open('_is_rows.json')); BSJ = json.load(open('_bs_rows.json'))
CFJ = json.load(open('_cf_rows.json')); DCJ = json.load(open('_dcf_rows.json'))
BS = BSJ['BS']; CF = CFJ['CF']; DC = DCJ['DC']
BLUE = Font(color='0000FF'); GREEN = Font(color='008000'); BLACK = Font(color='000000')
TITLE = Font(bold=True, size=13, color='F6F1E6'); SUB = Font(size=9, color='6E7B77')
FILL_T = PatternFill('solid', start_color='1C3A36'); FILL_H = PatternFill('solid', start_color='EAF0EE')
FILL_G = PatternFill('solid', start_color='F6F1E6')
NUM0 = '#,##0;(#,##0);"-"'; NUM = '#,##0.0;(#,##0.0);"-"'
PCT = '0.0%;(0.0%);"-"'; PCT2 = '0.00%;(0.00%);"-"'; PX = '0.00'; MULT = '0.00x'
YF = ['FY26E', 'FY27E', 'FY28E', 'FY29E', 'FY30E']; FCOLS = ['E', 'F', 'G', 'H', 'I']
YH = ['FY23', 'FY24', 'FY25']
ALLC = ['B', 'C', 'D'] + FCOLS
_LR = D['lens_record']; _BR = D['central_two_sided']['branches']
_LI = D['lens_inputs']; _REL = _LI['relative']

# THE BRANCH LABELS ARE READ FROM THE RECORD, never retyped: two documents naming one
# branch differently is the same defect as two documents publishing one number differently.
LBL_B = _BR[0]['label']      # the reviewed carrying value
LBL_A = _BR[1]['label']      # the June-2026 round price
assert 'carrying value' in LBL_B and 'round price' in LBL_A, (LBL_B, LBL_A)

# Assumptions cells, by label rather than by remembered row number [L-017].
def AB(label):
    return "Assumptions!$B$%d" % A[label]


SPOT = AB('Price (EGP/share)'); SHARES = AB('Shares outstanding (mn)')
CAPLEG = AB('GB Capital lending leg (EGP mn)')
ASSOC_A = AB('Associates — branch A (round price)')
ASSOC_B = AB('Associates — branch B (reviewed carrying value)')
MNT_A = AB('BRANCH A — MNT-Halan at the June-2026 round price')
MNT_B = AB('BRANCH B — MNT-Halan at its reviewed carrying value, 30 June 2026')
OTHASSOC = AB("Other associates (Bedaya, Kaf) — by identity off the note's own total")
AUTO_ND = AB('GB Auto net debt (30 June 2026, reviewed)')
AUTO_NCI = AB('GB Auto non-controlling interests (30 June 2026)')
TG = AB('Terminal growth (nominal EGP, DERIVED)')
AEQ = "DCF!$B$%d" % DCJ['AEQ']


def sheet(n):
    """Replace the sheet if it is already there. These parts run in order on one file, and a
    part re-run on its own used to APPEND a second copy under a suffixed name — a workbook
    that opens perfectly, carries every sheet twice and fails the sheet-list standard for a
    reason nothing in the run explains."""
    if n in wb.sheetnames:
        del wb[n]
    ws = wb.create_sheet(n); ws.title = n; return ws


def title(ws, t, s=None, w=9):
    ws['A1'] = t; ws['A1'].font = TITLE; ws['A1'].fill = FILL_T
    for c in range(2, w + 1): ws.cell(row=1, column=c).fill = FILL_T
    if s: ws['A2'] = s; ws['A2'].font = SUB
    ws.column_dimensions['A'].width = 50
    for c in range(2, w + 1): ws.column_dimensions[get_column_letter(c)].width = 15


def put(ws, ad, v, font=BLACK, fmt=NUM0, bold=False, fill=None, wrap=False):
    c = ws[ad]; c.value = v; c.font = Font(color=font.color, bold=bold)
    if fmt: c.number_format = fmt
    if fill: c.fill = fill
    return c


# ================= SOTP BRIDGE ==============================================
ws = sheet('SOTP Bridge')
title(ws, 'Sum of the parts — the class primary, and it IS the answer',
      'Three legs, and the third has two bases the company itself discloses. Both are '
      'carried to the end; nothing between them is computed anywhere in this workbook.', 5)
put(ws, 'A5', 'Leg', BLACK, None, True, FILL_H)
put(ws, 'B5', 'Basis', BLACK, None, True, FILL_H)
put(ws, 'C5', LBL_B, BLACK, None, True, FILL_H)
put(ws, 'D5', LBL_A, BLACK, None, True, FILL_H)
rows = [
 ('GB Auto operating leg',
  'five-year cash-flow model: enterprise value less the segment\'s own net debt and minority',
  '=' + AEQ, '=' + AEQ, NUM0, False),
 ('GB Capital lending leg',
  'operating equity x a justified price-to-book of (ROE - g) / (Ke - g)',
  '=' + CAPLEG, '=' + CAPLEG, NUM0, False),
 ('Associates (MNT-Halan, Bedaya, Kaf)',
  'the contested judgement: the reviewed carrying value against the June-2026 round price',
  '=' + ASSOC_B, '=' + ASSOC_A, NUM0, False),
 ('Equity value (EGP mn)', '', '=SUM(C6:C8)', '=SUM(D6:D8)', NUM0, True),
 ('Shares in issue (mn)', '', '=' + SHARES, '=' + SHARES, NUM0, False),
 ('FAIR VALUE PER SHARE (EGP)', '', '=C9/C10', '=D9/D10', PX, True),
 ('Latest known price (EGP)', '', '=' + SPOT, '=' + SPOT, PX, False),
 ('Difference against the price', '', '=C11/C12-1', '=D11/D12-1', PCT, True),
]
r = 6
for a, b, cb, ca, fmt, bold in rows:
    put(ws, 'A%d' % r, a, BLACK, None, bold)
    put(ws, 'B%d' % r, b, SUB, None)
    put(ws, 'C%d' % r, cb, GREEN if 'Assumptions' in cb or 'DCF' in cb else BLACK, fmt, bold)
    put(ws, 'D%d' % r, ca, GREEN if 'Assumptions' in ca or 'DCF' in ca else BLACK, fmt, bold)
    r += 1
ws.column_dimensions['B'].width = 72
r += 1
put(ws, 'A%d' % r, 'memo: MNT-Halan alone (EGP mn)')
put(ws, 'C%d' % r, '=' + MNT_B, GREEN, NUM0); put(ws, 'D%d' % r, '=' + MNT_A, GREEN, NUM0)
MNTROW = r; r += 1
put(ws, 'A%d' % r, 'memo: MNT-Halan alone, per share (EGP)')
put(ws, 'C%d' % r, '=C%d/C10' % MNTROW, BLACK, PX)
put(ws, 'D%d' % r, '=D%d/D10' % MNTROW, BLACK, PX)
r += 1
put(ws, 'A%d' % r, 'memo: MNT-Halan as a share of the equity value')
put(ws, 'C%d' % r, '=C%d/C9' % MNTROW, BLACK, PCT)
put(ws, 'D%d' % r, '=D%d/D9' % MNTROW, BLACK, PCT)
r += 1
put(ws, 'A%d' % r, 'memo: the distance between the two branches, per share (EGP)')
put(ws, 'D%d' % r, '=D11-C11', BLACK, PX)
put(ws, 'B%d' % r, 'the whole of it is the associate mark; the auto leg and the lender leg '
                   'are identical in both branches, to the pound.', SUB, None)
r += 2
put(ws, 'A%d' % r,
    'WHY THERE IS NO SINGLE NUMBER HERE. ' + D['central_two_sided']['why'] + ' The low end '
    'is the equity-accounted carrying value in the reviewed consolidated interim statements '
    'at 30 June 2026; the review conclusion on those statements is QUALIFIED at exactly that '
    'line, because the reviewers were not provided with the associate\'s own financial '
    'statements — so the conservative branch is not a safe harbour either, and this workbook '
    'says so rather than resting on it. The high end is the stake the company states applied '
    'to the primary round it announced on 9 June 2026. A primary round prices new money with '
    'whatever preferences ride with it, and GB Corp holds an ordinary equity-accounted '
    'minority: it is a mark, not a realisable price.', SUB, None)
r += 2
put(ws, 'A%d' % r, 'THE MARK, PRICED ACROSS ITS OWN RANGE', BLACK, None, True, FILL_H)
r += 1
put(ws, 'A%d' % r, 'MNT-Halan carried at (EGP mn)', BLACK, None, True)
put(ws, 'B%d' % r, 'as a multiple of the reviewed carrying value', BLACK, None, True)
put(ws, 'C%d' % r, 'Fair value per share (EGP)', BLACK, None, True)
put(ws, 'D%d' % r, '', BLACK, None, True)
r += 1
# THE RUNGS ARE EVIDENCED, NOT INTERPOLATED. A ladder drawn by cutting the distance between
# the two branches into equal steps would put a number halfway between them on the page, and
# a number halfway between two disclosures only one of which can be right is the average
# this study exists not to publish. Every rung here is a mark somebody has actually argued
# for: the two branches themselves, and the two haircuts on the round price that this
# study's own expert panel puts on a private mark held by a minority holder.
_HAIR = sorted(D['experts']['e1']['mark_haircut'].keys(), key=float)
_MNT_A_V = D['sotp']['mnt_halan_value']
_MNT_B_V = _LR['primary']['range_basis']['low']
LAD0 = r
# Ordered by the mark itself, so the ladder reads down. The order is settled here from the
# committed figures; the cells stay formulas, because a builder that sorted by value and
# then wrote the values would have turned a live model into a printed one.
_RUNGS = sorted(
    [(_MNT_A_V * float(h),
      '=%s*%s' % (MNT_A, h),
      'the round price haircut to %sx — this study\'s own expert panel\'s stated '
      'sensitivity on a private mark held by a minority holder' % h) for h in _HAIR]
    + [(_MNT_B_V, '=' + MNT_B, LBL_B), (_MNT_A_V, '=' + MNT_A, LBL_A)])
_RUNGS = [(f, n) for _v, f, n in _RUNGS]
_BRANCH_COL = {LBL_B: None, LBL_A: None}
for _k, (_f, _n) in enumerate(_RUNGS):
    if _n in _BRANCH_COL:
        _BRANCH_COL[_n] = get_column_letter(2 + _k)
assert all(_BRANCH_COL.values()), _BRANCH_COL
for mark, note in _RUNGS:
    put(ws, 'A%d' % r, mark, GREEN, NUM0)
    put(ws, 'B%d' % r, '=A%d/%s' % (r, MNT_B), BLACK, MULT)
    put(ws, 'C%d' % r, '=(%s+%s+A%d+%s)/%s' % (AEQ, CAPLEG, r, OTHASSOC, SHARES), BLACK, PX)
    put(ws, 'D%d' % r, note, SUB, None)
    r += 1
LAD1 = r - 1
put(ws, 'A%d' % (r + 1),
    'The two branch rows here ARE the two branches above, recomputed from the legs rather '
    'than copied — which is what makes this table a check on the bridge and not a '
    'restatement of it. The rungs are not sorted into a line between the branches on '
    'purpose: this prices a mark, it does not interpolate an answer.', SUB, None)

# ================= RELATIVE & NORMALIZED ====================================
ws = sheet('Relative & Normalized')
title(ws, 'The cross-checks — a relative multiple off the company\'s own history, and the '
          'disclosed floor',
      'Published beside the primary and never averaged into it. There is no normalised-'
      'earnings lens for this class, and the reason is at the foot of this sheet.', 6)
r = 5
put(ws, 'A%d' % r, 'GB Corp\'s OWN trailing price-to-earnings, at its last three year-end closes',
    BLACK, None, True, FILL_H)
for j, hd in enumerate(['Close (EGP)', 'Net profit attributable', 'EPS (EGP)', 'Trailing P/E']):
    put(ws, '%s%d' % (get_column_letter(2 + j), r), hd, BLACK, None, True, FILL_H)
r += 1
PE0 = r
for y in ('2023', '2024', '2025'):
    put(ws, 'A%d' % r, 'FY%s year-end' % y)
    put(ws, 'B%d' % r, '=' + AB('GB Corp close, year-end %s (EGP)' % y), GREEN, PX)
    put(ws, 'C%d' % r, '=' + AB('Net profit attributable, FY%s' % y), GREEN, NUM)
    put(ws, 'D%d' % r, '=C%d/%s' % (r, SHARES), BLACK, PX)
    put(ws, 'E%d' % r, '=B%d/D%d' % (r, r), BLACK, MULT)
    r += 1
PE1 = r - 1
put(ws, 'A%d' % r, 'Adopted multiple — the MEDIAN of those three', BLACK, None, True)
put(ws, 'E%d' % r, '=MEDIAN(E%d:E%d)' % (PE0, PE1), BLACK, MULT, True)
PEROW = r
put(ws, 'F%d' % r, 'THREE OBSERVATIONS IS THIN, and the count is published with the median '
                   'for exactly that reason.', SUB, None)
r += 1
put(ws, 'A%d' % r, 'Observations behind it', BLACK, None)
put(ws, 'E%d' % r, _REL['observations'], BLUE, NUM0)
r += 2
put(ws, 'A%d' % r, 'THE RELATIVE READ', BLACK, None, True, FILL_H)
r += 1
put(ws, 'A%d' % r, 'FY26E group net profit attributable (EGP mn)')
put(ws, 'B%d' % r, "='Income Statement'!E%d" % IS['Net profit (attributable)'], GREEN, NUM)
put(ws, 'C%d' % r, 'READ from this model\'s own consolidated forecast rather than typed.',
    SUB, None)
NP26 = r; r += 1
put(ws, 'A%d' % r, 'FY26E earnings per share (EGP)')
put(ws, 'B%d' % r, '=B%d/%s' % (NP26, SHARES), BLACK, PX)
EPS26 = r; r += 1
put(ws, 'A%d' % r, 'Relative multiple read (EGP/share)', BLACK, None, True)
put(ws, 'B%d' % r, '=B%d*E%d' % (EPS26, PEROW), BLACK, PX, True)
RELROW = r; r += 1
put(ws, 'A%d' % r, 'Difference against the price')
put(ws, 'B%d' % r, '=B%d/%s-1' % (RELROW, SPOT), BLACK, PCT)
r += 1
put(ws, 'A%d' % r, 'memo: the multiple the shares ALREADY trade at, on the same forward earnings')
put(ws, 'B%d' % r, '=%s*%s/B%d' % (SPOT, SHARES, NP26), BLACK, MULT)
TRADED = r
put(ws, 'C%d' % r, 'committed so the non-circularity claim is arithmetic rather than prose: '
                   'a lens whose multiple IS the traded one values the company at what it '
                   'already trades at. This row is NOT an input to anything.', SUB, None)
r += 2
put(ws, 'A%d' % r, 'THE DISCLOSED FLOOR', BLACK, None, True, FILL_H)
r += 1
put(ws, 'A%d' % r, "Shareholders' equity before NCI, 30 June 2026 (EGP mn)")
put(ws, 'B%d' % r, '=' + AB("Shareholders' equity before NCI, 30 June 2026"), GREEN, NUM0)
BOOK = r; r += 1
put(ws, 'A%d' % r, 'Book value per share (EGP)', BLACK, None, True)
put(ws, 'B%d' % r, '=B%d/%s' % (BOOK, SHARES), BLACK, PX, True)
BVPS = r; r += 1
put(ws, 'A%d' % r, 'Price to book, at the latest known price')
put(ws, 'B%d' % r, '=%s/B%d' % (SPOT, BVPS), BLACK, MULT)
put(ws, 'C%d' % r, 'A DISCLOSED FLOOR, published as such and carrying no weight in any '
                   'answer above. It is worth printing because the shares trade BELOW it.',
    SUB, None)
r += 2
put(ws, 'A%d' % r, 'NORMALISED EARNINGS POWER — ABSENT, AND HERE IS WHY', BLACK, None, True, FILL_H)
r += 1
put(ws, 'A%d' % r,
    'The superseded edition carried a normalised-earnings lens at a fifth of a weighted '
    'blend, on six typed figures — three mid-cycle profit levels and three through-cycle '
    'multiples — sourced to nothing. It is removed rather than re-sourced, and with this '
    'issuer\'s own numbers behind the decision: group earnings carry investment gains from '
    'associates that ran 451.6, 294.6 and 131.6 across three consecutive quarters, plus a '
    'revaluation on deconsolidating an associate that the company itself strips out of its '
    'own return measure. Normalising earnings that swing on associate marks normalises '
    'noise. The sheet keeps its name because the model report\'s sheet list is the standard '
    'and a study does not rename the standard to fit itself.', SUB, None)
ws.column_dimensions['A'].width = 58
ws.column_dimensions['C'].width = 60

# ================= SUMMARY ==================================================
ws = sheet('Summary')
title(ws, 'Valuation summary — GB Corp (EGX: GBCO)',
      'One class primary, published on both of its sides; the other reads are cross-checks '
      'beside it. Every cell here is a link — nothing on this sheet is typed.', 6)
r = 5
for j, hd in enumerate(['Read', 'Basis', 'EGP/share', 'vs the price']):
    put(ws, '%s%d' % (get_column_letter(1 + j), r), hd, BLACK, None, True, FILL_H)
r += 1
READ0 = r
reads = [
 ('Sum of the parts — ' + LBL_B, 'THE PRIMARY, branch B', "='SOTP Bridge'!C11"),
 ('Sum of the parts — ' + LBL_A, 'THE PRIMARY, branch A', "='SOTP Bridge'!D11"),
 ('Relative multiple on the company\'s own history', 'cross-check, never weighted',
  "='Relative & Normalized'!B%d" % RELROW),
]
for nm, basis, f in reads:
    put(ws, 'A%d' % r, nm, BLACK, None, True)
    put(ws, 'B%d' % r, basis, SUB, None)
    put(ws, 'C%d' % r, f, GREEN, PX, True)
    put(ws, 'D%d' % r, '=C%d/%s-1' % (r, SPOT), BLACK, PCT)
    r += 1
READ1 = r - 1
put(ws, 'A%d' % r, 'Book value per share', BLACK, None)
put(ws, 'B%d' % r, 'a DISCLOSED FLOOR — outside the envelope below, and never weighted', SUB, None)
put(ws, 'C%d' % r, "='Relative & Normalized'!B%d" % BVPS, GREEN, PX)
put(ws, 'D%d' % r, '=C%d/%s-1' % (r, SPOT), BLACK, PCT)
r += 2
put(ws, 'A%d' % r, 'Envelope — low', BLACK, None, True)
put(ws, 'B%d' % r, 'the RANGE of the present-value reads on one clock, never an average and '
                   'never a spread invented around a central', SUB, None)
put(ws, 'C%d' % r, '=MIN(C%d:C%d)' % (READ0, READ1), BLACK, PX, True)
put(ws, 'D%d' % r, '=C%d/%s-1' % (r, SPOT), BLACK, PCT)
ENVLO = r; r += 1
put(ws, 'A%d' % r, 'Envelope — high', BLACK, None, True)
put(ws, 'C%d' % r, '=MAX(C%d:C%d)' % (READ0, READ1), BLACK, PX, True)
put(ws, 'D%d' % r, '=C%d/%s-1' % (r, SPOT), BLACK, PCT)
ENVHI = r; r += 2
put(ws, 'A%d' % r, 'Latest known price (EGP), %s' % D['spot_date'], BLACK, None)
put(ws, 'C%d' % r, '=' + SPOT, GREEN, PX)
r += 2
put(ws, 'A%d' % r,
    'THERE IS NO CENTRAL, AND THAT IS THE ANSWER RATHER THAN AN OMISSION. ' +
    _LR['central_note'][0].upper() + _LR['central_note'][1:] +
    ' The two branches differ by the mark on one minority stake in an unlisted company, and '
    'the filings do not decide between them. Both are well above the price, so the reading '
    'the two share is that the market is paying less than either of the company\'s own '
    'disclosures on that stake would support — which is a claim about the mark, and the '
    'workbook prices it across its whole range on the SOTP Bridge sheet rather than '
    'resolving it.', SUB, None)
ws.column_dimensions['A'].width = 56
ws.column_dimensions['B'].width = 52

# ================= FUNDAMENTAL VALUATION ====================================
ws = sheet('Fundamental Valuation')
title(ws, 'Fundamental valuation — the football-field data',
      'Every read this study publishes, with the scenario span the study\'s own record '
      'carries for the primary. Links to Summary; no weights and no central.', 6)
r = 5
for j, hd in enumerate(['Read', 'Low', 'Published', 'High', 'Note']):
    put(ws, '%s%d' % (get_column_letter(1 + j), r), hd, BLACK, None, True, FILL_H)
r += 1
_PD = D['lenses']['prediscount']
put(ws, 'A%d' % r, 'Sum of the parts — ' + LBL_B, BLACK, None, True)
put(ws, 'C%d' % r, '=Summary!C%d' % READ0, GREEN, PX, True)
put(ws, 'E%d' % r, 'the primary, branch B', SUB, None)
r += 1
put(ws, 'A%d' % r, 'Sum of the parts — ' + LBL_A, BLACK, None, True)
put(ws, 'C%d' % r, '=Summary!C%d' % (READ0 + 1), GREEN, PX, True)
put(ws, 'B%d' % r, round(_PD['bear'], 4), BLUE, PX)
put(ws, 'D%d' % r, round(_PD['bull'], 4), BLUE, PX)
put(ws, 'E%d' % r, 'the primary, branch A. The low and high are the study\'s committed '
                   'scenario reads: a gross-margin shift, the WHOLE cost-of-capital ladder '
                   'moved together, a terminal growth shifted in REAL terms, and the marks '
                   'on the lender and the associates moved with them — a stress on the model '
                   'at once rather than one driver at a time, which is why they are read '
                   'from the record and not rebuilt in a cell here.', SUB, None)
r += 1
put(ws, 'A%d' % r, 'Relative multiple on the company\'s own history')
put(ws, 'C%d' % r, '=Summary!C%d' % (READ0 + 2), GREEN, PX)
put(ws, 'E%d' % r, 'cross-check; one value, because the multiple is a median of three '
                   'observations and a bear/bull around it would be invented.', SUB, None)
r += 1
put(ws, 'A%d' % r, 'Book value per share')
put(ws, 'C%d' % r, '=Summary!C%d' % (READ1 + 1), GREEN, PX)
put(ws, 'E%d' % r, 'a disclosed floor, outside the envelope and never weighted.', SUB, None)
r += 1
put(ws, 'A%d' % r, 'Envelope', BLACK, None, True)
put(ws, 'B%d' % r, '=Summary!C%d' % ENVLO, GREEN, PX, True)
put(ws, 'D%d' % r, '=Summary!C%d' % ENVHI, GREEN, PX, True)
put(ws, 'E%d' % r, 'the range of the present-value reads; there is no figure between the '
                   'two branches anywhere in this workbook.', SUB, None)
r += 1
put(ws, 'A%d' % r, 'Latest known price')
put(ws, 'C%d' % r, '=' + SPOT, GREEN, PX)
r += 1
put(ws, 'A%d' % r, 'GB Capital operating equity per share')
put(ws, 'C%d' % r, '=' + AB('memo: GB Capital operating equity per share — a DISCLOSED FLOOR, '
                            'never weighted'), GREEN, PX)
put(ws, 'E%d' % r, 'memo only: the lender leg\'s own book, to show what the residual-income '
                   'multiple does to it.', SUB, None)
ws.column_dimensions['E'].width = 70

# ================= SUMMARY FINANCIALS =======================================
ws = sheet('Summary Financials')
title(ws, 'Summary financials (EGP mn)', 'Every cell links to a statement sheet.', 10)
for j, hh in enumerate([''] + YH + YF):
    put(ws, '%s4' % get_column_letter(1 + j), hh, BLACK, None, True, FILL_H)
ws.column_dimensions['A'].width = 42
for c in range(2, 10): ws.column_dimensions[get_column_letter(c)].width = 11.5
r = 6
links = [
 ('Revenue', 'Income Statement', IS['Total revenue'], ALLC),
 ('EBITDA', 'Income Statement', IS['EBITDA (EBIT + D&A)'], ['D'] + FCOLS),
 ('EBIT', 'Income Statement', IS['EBIT'], ALLC),
 ('Net profit (attributable)', 'Income Statement', IS['Net profit (attributable)'], ALLC),
 ('Total assets', 'Balance Sheet', BS['TOTAL ASSETS'], ALLC),
 ('Total equity', 'Balance Sheet', BS['Total equity'], ALLC),
 ('Group net debt', 'Balance Sheet', BSJ['ND'], ALLC),
]
for nm, sh, rr, cols in links:
    put(ws, 'A%d' % r, nm)
    for col in cols:
        put(ws, '%s%d' % (col, r), "='%s'!%s%d" % (sh, col, rr), GREEN, NUM0)
    r += 1
put(ws, 'A%d' % r, 'Free cash flow (forecast)')
for col in FCOLS:
    put(ws, '%s%d' % (col, r), "='Cash Flow'!%s%d" % (col, CF['Free cash flow']), GREEN, NUM0)
r += 1
put(ws, 'A%d' % r, 'GB Auto free cash flow to the firm (the DCF leg)')
for j, col in enumerate(FCOLS):
    put(ws, '%s%d' % (col, r), "=DCF!%s%d" % (get_column_letter(2 + j), DCJ['FCFF']),
        GREEN, NUM0)
r += 2
put(ws, 'A%d' % r, 'EBITDA for FY2023 and FY2024 is not shown because the group depreciation '
                   'line for those two years is not carried in this study\'s committed '
                   'record; it is left empty rather than estimated.', SUB, None)

# ================= MONTE CARLO ==============================================
ws = sheet('Monte Carlo')
title(ws, 'Monte Carlo — the price engine\'s own lens, on its own clock',
      '50,000 paths, seed 42, computed by the Testahil price engine. It is a SEPARATE LENS '
      'from the valuation on the sheets before this one: no output of either is an input to '
      'the other, which is what makes agreement between them information rather than an echo.',
      8)
pr = D['mc']['prob_read']; q20, q60 = D['mc']['q20'], D['mc']['q60']
r = 5
put(ws, 'A%d' % r, 'The probability read (three months)', BLACK, None, True, FILL_G); r += 1
prr = [
 ('Probability the price is above the anchor', pr['p_above'], PCT),
 ('P(+10%) against P(-10%) — odds',
  '%.0f%% vs %.0f%% · %.1f:1' % (pr['p_up10'] * 100, pr['p_dn10'] * 100, pr['odds']), '@'),
 ('Median level (EGP) and move',
  '%.2f (%+.1f%%)' % (pr['median'], pr['med_move'] * 100), '@'),
 ('50% band (25th to 75th percentile)',
  '%.1f - %.1f  (%+.0f%% / %+.0f%%)' % (pr['band50'][0], pr['band50'][1],
                                        pr['band50_pct'][0] * 100, pr['band50_pct'][1] * 100), '@'),
 ('Touch(+10%) / touch(-10%)',
  '%.0f%% / %.0f%%' % (pr['touch_up10'] * 100, pr['touch_dn10'] * 100), '@'),
]
for nm, v, fmt in prr:
    put(ws, 'A%d' % r, nm); put(ws, 'B%d' % r, v, BLUE, fmt); r += 1
r += 1
put(ws, 'A%d' % r, 'Percentile map (EGP/share)', BLACK, None, True, FILL_H); r += 1
for j, hd in enumerate(['Horizon', 'p5', 'p25', 'p50', 'p75', 'p95']):
    put(ws, '%s%d' % (get_column_letter(1 + j), r), hd, BLACK, None, True, FILL_H)
r += 1
for tag, q in [('1 month', q20), ('3 months', q60)]:
    put(ws, 'A%d' % r, tag)
    for j, p in enumerate(['5', '25', '50', '75', '95']):
        put(ws, '%s%d' % (get_column_letter(2 + j), r), round(q[p], 4), BLUE, PX)
    r += 1
r += 1
put(ws, 'A%d' % r, 'Engine inputs (from Assumptions)', BLACK, None, True, FILL_H); r += 1
for nm, lab in [('Anchor volatility (HAR, annualised)',
                 'Anchor volatility (HAR forecast, annualised)'),
                ('Secular drift (daily)', 'Secular drift (daily log-return, expanding window)'),
                ('Net factor drift per quarter', 'Net factor drift per quarter')]:
    put(ws, 'A%d' % r, nm); put(ws, 'B%d' % r, '=' + AB(lab), GREEN, PCT); r += 1
r += 1
put(ws, 'A%d' % r, 'Level-touch ladder (probability of touching by the horizon)',
    BLACK, None, True, FILL_H); r += 1
for j, hd in enumerate(['Level (EGP)', '1 month', '3 months']):
    put(ws, '%s%d' % (get_column_letter(1 + j), r), hd, BLACK, None, True, FILL_H)
r += 1
for L_, tv in sorted(D['mc']['touch'].items(), key=lambda kv: -float(kv[0])):
    put(ws, 'A%d' % r, float(L_), BLUE, PX)
    put(ws, 'B%d' % r, tv['t20'], BLUE, PCT); put(ws, 'C%d' % r, tv['t60'], BLUE, PCT); r += 1
put(ws, 'A%d' % (r + 1),
    'The cone is anchored on the last real session the exchange library holds, EGP %.2f on '
    '%s; the valuation is struck against the latest known price of EGP %.2f on %s. Two '
    'clocks, both published with their own dates.'
    % (D['valuation_gap']['mc_anchor'], D['valuation_gap']['mc_anchor_date'],
       D['spot'], D['spot_date']), SUB, None)
ws.column_dimensions['A'].width = 52

# ================= SENSITIVITY ==============================================
ws = sheet('Sensitivity')
title(ws, 'Sensitivity — the two things the answer actually turns on',
      'The mark on the associate, and the price of time. There is no complexity-discount '
      'axis: the superseded edition sensitised the answer across a discount it also applied, '
      'and that discount is gone.', 8)
gm = D['sens']['grid_margin']
put(ws, 'A4', 'GRID 1 — Auto gross-margin shift against the MNT-Halan mark',
    BLACK, None, True, FILL_H)
put(ws, 'A5', 'Gross-margin shift \\ mark (EGP mn)', BLACK, None, True, FILL_H)
# The SAME evidenced mark levels as the ladder — no interpolated column, for the same
# reason: a grid column halfway between the two branches would print the average.
for k, (mk, _n) in enumerate(_RUNGS):
    put(ws, '%s5' % get_column_letter(2 + k), mk, BLACK, NUM0, True, FILL_H)
G1_0 = 6
for i, mm in enumerate(gm):
    rr = G1_0 + i
    put(ws, 'A%d' % rr, mm, BLUE, '+0.0%;-0.0%;"base"')
    for k in range(len(_RUNGS)):
        col = get_column_letter(2 + k)
        put(ws, '%s%d' % (col, rr),
            '=(DCF!$B$%d+$A%d*100*DCF!$B$%d-%s-%s+%s+%s$5+%s)/%s'
            % (DCJ['EVR'], rr, DCJ['EVPP'], AUTO_ND, AUTO_NCI, CAPLEG, col, OTHASSOC, SHARES),
            BLACK, PX)
G1_1 = G1_0 + len(gm) - 1
r = G1_1 + 1
put(ws, 'A%d' % r,
    'Two of these columns ARE the two published branches, at a zero margin shift, and the '
    'other two are haircuts on the round price that this study\'s own expert panel argues '
    'for. A margin '
    'shift moves cost only, so it moves each '
    'year\'s free cash flow by revenue x shift x (1 - tax) — the helper row on the DCF sheet '
    'is that arithmetic exactly, not an approximation of it.', SUB, None)
r += 2
put(ws, 'A%d' % r, 'GRID 2 — the price of time: a shift in the WHOLE cost-of-capital ladder '
                   'against terminal growth', BLACK, None, True, FILL_H)
G2_HDR = r + 1
G2_0 = G2_HDR + 1
SHIFTS = [-0.02, -0.01, 0.0, 0.01, 0.02]
TGS = [-0.02, -0.01, 0.0, 0.01, 0.02]
HELP_HDR = G2_0 + len(SHIFTS) + 2
HELP_0 = HELP_HDR + 1
put(ws, 'A%d' % G2_HDR, 'Ladder shift \\ terminal growth', BLACK, None, True, FILL_H)
for j, t in enumerate(TGS):
    put(ws, '%s%d' % (get_column_letter(2 + j), G2_HDR), '=%s+%s' % (TG, repr(t)),
        BLACK, PCT, True, FILL_H)
for i, s in enumerate(SHIFTS):
    rr = G2_0 + i
    hr = HELP_0 + i
    put(ws, 'A%d' % rr, s, BLUE, '+0.0%;-0.0%;"base"')
    for j in range(5):
        col = get_column_letter(2 + j)
        put(ws, '%s%d' % (col, rr),
            '=(SUMPRODUCT(DCF!$B$%d:$F$%d,$B$%d:$F$%d)'
            '+DCF!$F$%d*(1+%s$%d)/($G$%d-%s$%d)*$F$%d'
            '-%s-%s+%s+%s)/%s'
            % (DCJ['FCFF'], DCJ['FCFF'], hr, hr,
               DCJ['FCFF'], col, G2_HDR, hr, col, G2_HDR, hr,
               AUTO_ND, AUTO_NCI, CAPLEG, ASSOC_A, SHARES),
            BLACK, PX)
put(ws, 'A%d' % HELP_HDR,
    'helper — the shifted discount factors, one forward rate per year moved together',
    BLACK, None, True, FILL_H)
for j in range(5):
    put(ws, '%s%d' % (get_column_letter(2 + j), HELP_HDR), YF[j], BLACK, None, True, FILL_H)
put(ws, 'G%d' % HELP_HDR, 'terminal rate', BLACK, None, True, FILL_H)
for i, s in enumerate(SHIFTS):
    hr = HELP_0 + i
    put(ws, 'A%d' % hr, s, BLUE, '+0.0%;-0.0%;"base"')
    for j in range(5):
        col = get_column_letter(2 + j)
        dcol = get_column_letter(2 + j)
        if j == 0:
            f = '=1/(1+DCF!%s%d+$A%d)' % (dcol, DCJ['FWD'], hr)
        else:
            f = '=%s%d/(1+DCF!%s%d+$A%d)' % (get_column_letter(1 + j), hr, dcol, DCJ['FWD'], hr)
        put(ws, '%s%d' % (col, hr), f, BLACK, '0.0000')
    put(ws, 'G%d' % hr, '=DCF!$B$%d+$A%d' % (DCJ['WTR'], hr), BLACK, PCT2)
r = HELP_0 + len(SHIFTS) + 1
put(ws, 'A%d' % r,
    'Grid 2 is read on branch A — MNT-Halan at the June-2026 round price. Branch B is the '
    'same grid shifted DOWN by exactly the distance between the two marks per share, which '
    'the SOTP Bridge sheet prints; the price of time does not touch the associate mark, so '
    'the shift is a constant and there is nothing to recompute. The whole ladder moves '
    'together — moving one forward rate and leaving the others would price two different '
    'economies in one model.', SUB, None)
BRANCH_OFFSET = r + 1
put(ws, 'A%d' % BRANCH_OFFSET, 'the constant to subtract for branch B (EGP/share)')
put(ws, 'B%d' % BRANCH_OFFSET, "='SOTP Bridge'!D11-'SOTP Bridge'!C11", BLACK, PX)
ws.column_dimensions['A'].width = 52

# ================= PER-SHARE & RATIOS =======================================
ws = sheet('Per-Share & Ratios')
title(ws, 'Per share and ratios — the standing dashboard', 'Links to the statements and to '
      'Assumptions; nothing here is typed.', 10)
for j, hh in enumerate([''] + YH + YF):
    put(ws, '%s4' % get_column_letter(1 + j), hh, BLACK, None, True, FILL_H)
ws.column_dimensions['A'].width = 44
for c in range(2, 10): ws.column_dimensions[get_column_letter(c)].width = 11.5
NPR = IS['Net profit (attributable)']; REVR = IS['Total revenue']
EBITDAR = IS['EBITDA (EBIT + D&A)']; EQR = BSJ['EQ']; NDR = BSJ['ND']
r = 6


def prow(r, label, f, fmt=PX, cols=ALLC):
    put(ws, 'A%d' % r, label)
    for col in cols:
        v = f(col)
        if v is not None:
            put(ws, '%s%d' % (col, r), v, BLACK, fmt)
    return r + 1


r = prow(r, 'EPS (EGP)', lambda c: "='Income Statement'!%s%d/%s" % (c, NPR, SHARES))
r = prow(r, 'DPS (EGP)',
         lambda c: ("='Income Statement'!%s%d*Assumptions!%s$%d/%s"
                    % (c, NPR, ['C', 'D', 'E', 'F', 'G'][FCOLS.index(c)],
                       A['Dividend payout (of attributable NP)'], SHARES))
         if c in FCOLS else None)
DPSR = r - 1
r = prow(r, 'Book value per share (EGP)',
         lambda c: "='Balance Sheet'!%s%d/%s" % (c, EQR, SHARES))
r = prow(r, 'P/E at the latest known price', lambda c: "=%s/('Income Statement'!%s%d/%s)"
         % (SPOT, c, NPR, SHARES), MULT)
r = prow(r, 'P/B at the latest known price', lambda c: "=%s/('Balance Sheet'!%s%d/%s)"
         % (SPOT, c, EQR, SHARES), MULT)
r = prow(r, 'Dividend yield at the latest known price',
         lambda c: "=%s%d/%s" % (c, DPSR, SPOT) if c in FCOLS else None, PCT2)
r = prow(r, 'EBITDA margin', lambda c: "='Income Statement'!%s%d/'Income Statement'!%s%d"
         % (c, EBITDAR, c, REVR) if c != 'B' and c != 'C' else None, PCT2)
r = prow(r, 'Net margin', lambda c: "='Income Statement'!%s%d/'Income Statement'!%s%d"
         % (c, NPR, c, REVR), PCT2)
r = prow(r, 'Return on average equity (attributable)',
         lambda c: "='Income Statement'!%s%d/'Balance Sheet'!%s%d" % (c, NPR, c, EQR), PCT2)
r = prow(r, 'Group net debt / EBITDA', lambda c: "='Balance Sheet'!%s%d/'Income Statement'!%s%d"
         % (c, NDR, c, EBITDAR) if c not in ('B', 'C') else None, MULT)
r = prow(r, 'Revenue year on year',
         lambda c: "='Income Statement'!%s%d/'Income Statement'!%s%d-1"
         % (c, REVR, chr(ord(c) - 1), REVR) if c != 'B' else None, PCT2)
r = prow(r, 'EPS year on year',
         lambda c: "='Income Statement'!%s%d/'Income Statement'!%s%d-1"
         % (c, NPR, chr(ord(c) - 1), NPR) if c != 'B' else None, PCT2)
put(ws, 'A%d' % (r + 1),
    'Group net debt against group EBITDA blends the lender\'s funding book, which is its raw '
    'material rather than its leverage; the measure the valuation bridge actually deducts is '
    'the AUTO segment\'s own net debt at 30 June 2026, on the Assumptions sheet. Dividends '
    'per share are shown for the forecast only, because the payout is a forecast driver and '
    'the historical distributions are not carried in this study\'s record.', SUB, None)

# ================= PEER & SECTOR ============================================
ws = sheet('Peer & Sector')
title(ws, 'Peer set and sector', 'There is no clean single comparable — GB Corp is an auto '
      'operator plus a non-bank lender plus a fintech associate. Split by leg.', 7)
r = 5
for j, hd in enumerate(['Leg', 'Closest peers', 'How that kind of business is usually valued']):
    put(ws, '%s%d' % (get_column_letter(1 + j), r), hd, BLACK, None, True, FILL_H)
r += 1
peers = [
 ('Auto assembly and distribution',
  'Al Watania (KSA autos), Saudi Co. for Vehicles, Turk Traktor, Astra Industrial; EGX '
  'consumer durables',
  'enterprise value to EBITDA in the mid single digits; earnings multiples around eight to '
  'twelve times'),
 ('Non-bank lender — leasing and consumer finance',
  'EFG Hermes (its non-bank arm), Contact Financial (CNFN), Raya Holding\'s finance leg',
  'price to book around one to two times on a mid-teens return on equity — which is exactly '
  'the relationship the GB Capital leg builds from this segment\'s OWN return rather than '
  'importing'),
 ('Fintech associate (MNT-Halan)',
  'Fawry (FWRY), e-Finance (EFIH), and MNT-Halan\'s own private rounds',
  'private marks; the last round GB Corp announced valued it at USD %s bn (June 2026), and '
  'what that mark is worth to a minority holder is the contested judgement this study '
  'publishes both ways' % ('%.1f' % (D['sotp']['mnt_halan_round_usd'] / 1000.0))),
]
for a, b, c in peers:
    put(ws, 'A%d' % r, a); put(ws, 'B%d' % r, b, BLACK, None); put(ws, 'C%d' % r, c, BLACK, None)
    r += 1
ws.column_dimensions['A'].width = 40
ws.column_dimensions['B'].width = 62; ws.column_dimensions['C'].width = 62
r += 1
put(ws, 'A%d' % r,
    'Sector context: Egyptian passenger-car registrations recovered sharply through 2025 and '
    'GB Corp is the largest assembler and distributor in the market; the central bank\'s '
    'easing cycle lowers the customer\'s instalment and the lender\'s funding cost at once, '
    'which is the single most mechanical catalyst on this name. Iraq and Jordan carry the '
    'regional drag. A peer multiple is used here as CONTEXT and never as a source for this '
    'company\'s own reported figures.', SUB, None)
put(ws, 'A%d' % (r + 1),
    'Analyst price targets and ratings are deliberately not used as a model input, and this '
    'study publishes neither.', SUB, None)

# ================= SHEET ORDER ==============================================
order = list(_RP.MODEL_STUDY['excel_sheets'])
assert sorted(order) == sorted(wb.sheetnames), (sorted(order), sorted(wb.sheetnames))
wb._sheets = [wb[n] for n in order]
wb.save(OUT)
json.dump(dict(SOTP=dict(branchB='C11', branchA='D11', eqB='C9', eqA='D9',
                         ladder0=LAD0, ladder1=LAD1, mnt=MNTROW),
               REL=dict(pe=PEROW, pe0=PE0, pe1=PE1, np26=NP26, eps26=EPS26, value=RELROW,
                        traded=TRADED, book=BOOK, bvps=BVPS),
               SUM=dict(read0=READ0, read1=READ1, envlo=ENVLO, envhi=ENVHI),
               SENS=dict(g1=G1_0, g2hdr=G2_HDR, g2=G2_0, help_hdr=HELP_HDR, help0=HELP_0,
                         shifts=SHIFTS, tgs=TGS, offset=BRANCH_OFFSET,
                         haircuts=[float(h) for h in _HAIR],
                         branch_cols={'B': _BRANCH_COL[LBL_B], 'A': _BRANCH_COL[LBL_A]}),
               PS=dict(dps=DPSR)),
          open('_ans_rows.json', 'w'), indent=1, sort_keys=True)
print('part4 ok — sheets in model-report order:', wb.sheetnames)
