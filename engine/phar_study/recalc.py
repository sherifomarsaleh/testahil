"""Recalculate the DELIVERED workbook and reconcile it cell-by-cell against the model.

Three gates, in increasing strength:
  1. every formula in the workbook must evaluate — anything the evaluator cannot parse is a
     FAILURE, never a skip;
  2. EVERY formula cell must reproduce the value the model itself computed for that cell.
     The builder records those in xlsx_expected.json as it writes. This is the gate that makes
     a formula-driven workbook safe: a formula that computes the right thing the wrong way, or
     points one row off, fails here rather than shipping a different number from the study;
  3. a hand-written set of headline reconciliations against study_numbers.json, as an
     independent cross-check on the expected map itself.

Verification runs on the delivered file, not on the builder, and the evaluator is an
independent reimplementation rather than the library that wrote the workbook.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import openpyxl
import xlcalc

XLSX = os.path.join(HERE, 'EIPICO_Valuation_Model_09082026.xlsx')
wb = openpyxl.load_workbook(XLSX)
D = json.load(open(os.path.join(HERE, 'study_numbers.json')))
XP = json.load(open(os.path.join(HERE, 'xlsx_expected.json')))
EXPECT, PASTE = XP['expected'], XP['paste_counts']
W, LN, DCFD, M = D['wacc'], D['lenses'], D['dcf'], D['meta']

BK = xlcalc.Book(wb)

# ---- gate 1: every formula must evaluate -------------------------------------
nform, unresolvable = 0, []
for sh, coord in BK.formula_cells():
    nform += 1
    try:
        BK.cell_value(sh, coord)
    except Exception as ex:
        unresolvable.append(f'{sh}!{coord}: {ex}')
print(f'gate 1 — formulas found {nform}, unresolvable {len(unresolvable)}')
for e in unresolvable[:15]:
    print('   ', e)

# ---- gate 2: every formula cell reproduces the model --------------------------
checked, mismatches = 0, []
for key, exp in EXPECT.items():
    sh, coord = key.rsplit('!', 1)
    try:
        got = float(BK.cell_value(sh, coord))
    except Exception as ex:
        mismatches.append(f'{key}: could not evaluate ({ex})')
        continue
    checked += 1
    tol = max(abs(exp) * 1e-6, 1e-7)
    if abs(got - exp) > tol:
        mismatches.append(f'{key}: workbook {got:.8f} vs model {exp:.8f}')
unchecked = nform - checked
print(f'gate 2 — {checked} of {nform} formula cells reproduce the model, '
      f'{len(unresolvable)} unresolvable, {unchecked} unchecked, '
      f'{len(mismatches)} mismatched')
for m in mismatches[:25]:
    print('   ', m)

# ---- gate 3: headline reconciliations against the study ------------------------
V = BK.cell_value


def find(sheet, text, col=1):
    ws = wb[sheet]
    for row in ws.iter_rows(min_col=col, max_col=col):
        for c in row:
            if isinstance(c.value, str) and c.value.strip().startswith(text):
                return c.row
    raise KeyError(f'{sheet}: no row labelled {text!r}')


checks = [
    ('cost of equity', V('Assumptions', f'C{find("Assumptions", "Cost of equity = normalised")}'),
     W['ke']),
    ('weighted average cost of capital',
     V('Assumptions', f'C{find("Assumptions", "Weighted average cost of capital, year one")}'),
     W['wacc0']),
    ('terminal discount rate',
     V('Assumptions', f'C{find("Assumptions", "Terminal weighted average")}'), W['wacc_term']),
    ('core enterprise value', V('DCF', f'B{find("DCF", "CORE ENTERPRISE VALUE")}'),
     DCFD['frame_A']['ev_core']),
    ('terminal share of enterprise value',
     V('DCF', f'B{find("DCF", "Terminal value as a percentage")}'), DCFD['frame_A']['tv_share']),
    ('equity value', V('SOTP Bridge', f'B{find("SOTP Bridge", "EQUITY VALUE")}'),
     DCFD['frame_A']['equity']),
    ('value per share, Frame A',
     V('SOTP Bridge', f'C{find("SOTP Bridge", "Value per share — Frame A")}'),
     DCFD['frame_A']['per_share']),
    ('weighted central fair value',
     V('Fundamental Valuation', f'B{find("Fundamental Valuation", "WEIGHTED CENTRAL")}'),
     LN['fair_base']),
    ('summary sheet central value', V('Summary', f'B{find("Summary", "WEIGHTED CENTRAL")}'),
     LN['fair_base']),
    ('lens weights sum to one',
     V('Fundamental Valuation', f'C{find("Fundamental Valuation", "WEIGHTED CENTRAL")}'), 1.0),
]
bad = []
for name, got, exp in checks:
    ok = abs(float(got) - float(exp)) <= max(abs(exp) * 1e-6, 1e-7)
    print(f'gate 3 — {name:42s} {float(got):>14,.6f} vs {float(exp):>14,.6f}  '
          f'{"OK" if ok else "MISMATCH"}')
    if not ok:
        bad.append(name)

print(f'\npasted cells by permitted class: {PASTE}')
print(f'formula cells {nform} against pasted value cells '
      f'{PASTE["audited"] + PASTE["unit_build"] + PASTE["grid"]}')

json.dump(dict(formulas=nform, checked=checked, unresolvable=len(unresolvable),
               unchecked=unchecked, mismatched=len(mismatches),
               paste_counts=PASTE, headline_failures=bad),
          open(os.path.join(HERE, 'recalc_result.json'), 'w'), indent=1)

assert not unresolvable, f'{len(unresolvable)} formulas could not be evaluated'
assert not mismatches, f'{len(mismatches)} formula cells do not reproduce the model'
assert unchecked == 0, f'{unchecked} formula cells were never checked'
assert not bad, f'headline reconciliation failed: {bad}'
print('\nRECALCULATION PASSED — '
      f'{checked} of {nform} formula cells reproduce the model, 0 unresolvable, 0 unchecked.')
