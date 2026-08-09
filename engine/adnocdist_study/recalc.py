"""Independent re-evaluation of the DELIVERED workbook.

This does not trust the builder. It opens the file that actually ships, walks every cell
whose value is a formula, evaluates it with an independent evaluator (xlcalc.py, a small
reimplementation that has to agree with the model cell for cell), and asserts three things:

  Gate 1  every formula evaluates. Anything the evaluator cannot parse is a FAILURE, never
          a skip — an unparseable cell is exactly where an error would hide.
  Gate 2  every formula cell reproduces the model's own value for it, and NO formula cell
          was left unchecked. A formula the builder wrote without recording an expected
          value is a failure, not a gap.
  Gate 3  the headline numbers reconcile to the committed numbers file, located by LABEL
          TEXT rather than by row number, so the check does not inherit the builder's own
          idea of where anything sits.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import openpyxl
import xlcalc

XLSX = os.path.join(HERE, 'ADNOCDIST_Valuation_Model_09082026.xlsx')
D = json.load(open(os.path.join(HERE, 'study_numbers.json')))
EXP = json.load(open(os.path.join(HERE, 'xlsx_expected.json')))
EXPECT, PASTE = EXP['expected'], EXP['paste_counts']
W, DCFD, L = D['wacc'], D['dcf'], D['lenses']
A_, B_ = DCFD['frame_A'], DCFD['frame_B']

wb = openpyxl.load_workbook(XLSX)
BK = xlcalc.Book(wb)

# ---- gate 1 — every formula evaluates ------------------------------------------
cells = list(BK.formula_cells())
unresolvable = []
for sh, co in cells:
    try:
        BK.cell_value(sh, co)
    except Exception as e:
        unresolvable.append(f'{sh}!{co}: {e}')
print(f'gate 1 — formulas found {len(cells)}, unresolvable {len(unresolvable)}')
for u in unresolvable[:15]:
    print('   ', u)

# ---- gate 2 — every formula reproduces the model -------------------------------
mismatches, checked = [], 0
for key, exp in EXPECT.items():
    sh, co = key.rsplit('!', 1)
    try:
        got = float(BK.cell_value(sh, co))
    except Exception as e:
        mismatches.append(f'{key}: could not evaluate ({e})')
        continue
    checked += 1
    tol = max(abs(exp) * 1e-6, 1e-7)
    if abs(got - exp) > tol:
        mismatches.append(f'{key}: workbook {got!r} vs model {exp!r}')
unchecked = len(cells) - checked
print(f'gate 2 — {checked} of {len(cells)} formula cells reproduce the model, '
      f'{len(mismatches)} mismatched, {unchecked} unchecked')
for m in mismatches[:15]:
    print('   ', m)


# ---- gate 3 — headline reconciliation, located by label ------------------------
def find(sheet, text, col=1):
    ws = wb[sheet]
    for row in ws.iter_rows(min_col=col, max_col=col):
        for c in row:
            if isinstance(c.value, str) and c.value.strip().startswith(text):
                return c.row
    raise KeyError(f'{sheet}: no row labelled {text!r}')


def at(sheet, text, col_letter, label_col=1):
    return float(BK.cell_value(sheet, f'{col_letter}{find(sheet, text, label_col)}'))


CHECKS = [
    ('cost of equity', at('Assumptions', 'Cost of equity', 'C'), W['ke']),
    ('cost of capital, first year', at('Assumptions', 'Cost of capital, first', 'C'),
     W['wacc']),
    ('terminal cost of capital', at('Assumptions', 'Terminal cost of capital', 'C'),
     W['wacc_terminal']),
    ('normalised risk-free rate', at('Assumptions', 'Normalised risk-free', 'C'),
     W['rf_star']),
    ('cost of debt after tax', at('Assumptions', 'Cost of debt after tax', 'C'),
     W['kd_aftertax']),
    ('enterprise value, Frame A', at('SOTP Bridge', 'ENTERPRISE VALUE', 'B'), A_['ev']),
    ('enterprise value, Frame B', at('SOTP Bridge', 'ENTERPRISE VALUE', 'C'), B_['ev']),
    ('terminal share of enterprise value, Frame A',
     at('SOTP Bridge', 'TERMINAL VALUE AS A PERCENTAGE', 'B'), A_['tv_share']),
    ('terminal share of enterprise value, Frame B',
     at('SOTP Bridge', 'TERMINAL VALUE AS A PERCENTAGE', 'C'), B_['tv_share']),
    ('terminal share shown on Summary',
     at('Summary', 'TERMINAL VALUE AS A PERCENTAGE', 'B'), A_['tv_share']),
    ('equity value, Frame A', at('SOTP Bridge', 'EQUITY VALUE', 'B'), A_['equity']),
    ('equity value, Frame B', at('SOTP Bridge', 'EQUITY VALUE', 'C'), B_['equity']),
    ('value per share, Frame A', at('SOTP Bridge', 'VALUE PER SHARE', 'B'),
     A_['per_share']),
    ('value per share, Frame B', at('SOTP Bridge', 'VALUE PER SHARE', 'C'),
     B_['per_share']),
    ('weighted centre, Frame A', at('Fundamental Valuation', 'WEIGHTED CENTRE', 'B'),
     L['centre_A']),
    ('weighted centre, Frame B', at('Fundamental Valuation', 'WEIGHTED CENTRE', 'C'),
     L['centre_B']),
    ('lens weights sum to one', at('Fundamental Valuation', 'SUM OF WEIGHTS', 'D'), 1.0),
    ('present value of five years, Frame A',
     at('SOTP Bridge', 'Present value of five years', 'B'), A_['pv_sum']),
    ('present value of the terminal, Frame A',
     at('SOTP Bridge', 'Present value of the terminal', 'B'), A_['pv_tv']),
    ('balance check, first forecast year', at('Balance Sheet', 'BALANCE CHECK', 'E'), 0.0),
    ('balance check, final forecast year', at('Balance Sheet', 'BALANCE CHECK', 'I'), 0.0),
]
bad = []
for name, got, exp in CHECKS:
    tol = max(abs(exp) * 1e-6, 1e-6)
    flag = 'ok' if abs(got - exp) <= tol else 'MISMATCH'
    if flag != 'ok':
        bad.append(f'{name}: workbook {got!r} vs model {exp!r}')
    print(f'   {flag:9s} {name}: {got:,.6f}')
print(f'gate 3 — {len(CHECKS)} headline reconciliations, {len(bad)} failures')

res = dict(formulas=len(cells), checked=checked, unresolvable=len(unresolvable),
           unchecked=unchecked, mismatched=len(mismatches),
           headline_checks=len(CHECKS), headline_failures=bad,
           paste_counts=PASTE)
json.dump(res, open(os.path.join(HERE, 'recalc_result.json'), 'w'), indent=1)

assert not unresolvable, f'{len(unresolvable)} formulas could not be evaluated'
assert not mismatches, f'{len(mismatches)} formula cells do not reproduce the model'
assert unchecked == 0, f'{unchecked} formula cells were never checked'
assert not bad, f'headline reconciliation failed: {bad}'
print(f'\n{checked} of {len(cells)} formula cells reproduce the model, '
      f'0 unresolvable, 0 unchecked')
