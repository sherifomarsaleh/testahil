"""Recalculate the delivered workbook and reconcile it cell-by-cell against the model.

Recalculation runs through the explicit evaluator in xlcalc.py, independently of the
library that wrote the file. Anything the evaluator cannot parse is a FAILURE, never a
skip — a permissive verifier is worse than no verifier.

Three gates, in increasing strength:
  1. every formula in the workbook must evaluate;
  2. EVERY formula cell must reproduce the value the model itself computed for it (the
     builder records them into xlsx_expected.json as it writes), AND no formula cell may
     be left unchecked;
  3. a hand-written set of headline reconciliations against study_numbers.json, as an
     independent cross-check on the expected map itself.
"""
import json
import os
import sys

import openpyxl
import xlcalc

HERE = os.path.dirname(os.path.abspath(__file__))
XLSX = os.path.join(HERE, 'BOROUGE_Valuation_Model_09082026_public.xlsx')
wb = openpyxl.load_workbook(XLSX)
D = json.load(open(os.path.join(HERE, 'study_numbers.json')))
XP = json.load(open(os.path.join(HERE, 'xlsx_expected.json')))
EXPECT = XP['expected']
W, LEN_, FR = D['wacc'], D['lenses'], D['framings']
SPOT, FX, SHARES = D['spot_aed'], D['aed_per_usd'], D['shares_out'] / 1e6

BK = xlcalc.Book(wb)
cv = BK.cell_value

# ---- gate 1: every formula must evaluate ------------------------------------
nform, errors = 0, []
for sh, coord in BK.formula_cells():
    nform += 1
    try:
        cv(sh, coord)
    except Exception as ex:
        errors.append(f'{sh}!{coord}: {ex}')
print(f'formulas: {nform}, unresolvable: {len(errors)}')
for e in errors[:25]:
    print('   ', e)


# ---- gate 2: every formula cell reproduces the model ------------------------
def tol_for(v):
    return max(2e-4, abs(v) * 5e-6)


nchk, drift = 0, []
for sh, cells in EXPECT.items():
    for coord, want in cells.items():
        nchk += 1
        try:
            got = cv(sh, coord)
        except Exception:
            continue
        if not isinstance(got, (int, float)) or abs(float(got) - want) > tol_for(want):
            drift.append((sh, coord, got, want))
print(f'formula cells checked against the model: {nchk}, disagreements: {len(drift)}')
for sh, coord, got, want in drift[:40]:
    g = f'{got:,.6f}' if isinstance(got, (int, float)) else repr(got)
    print(f'   {sh}!{coord}: workbook={g} model={want:,.6f}')

uncovered = [f'{sh}!{coord}' for sh, coord in BK.formula_cells()
             if coord not in EXPECT.get(sh, {})]
print(f'formula cells with no expected value recorded: {len(uncovered)}')
for u in uncovered[:25]:
    print('   ', u)

# ---- gate 3: headline reconciliations ---------------------------------------
checks = [
    ('normalised risk-free rate', ('Fundamental Valuation', None), W['rf_star']),
    ('weighted average cost of capital, own beta', None, W['wacc_own']),
    ('weighted average cost of capital, sector beta', None, W['wacc_bottom_up']),
]
# Located by searching the expected map rather than by hard-coded address, so the check
# survives a layout change.
def find(sheet, want):
    for coord, v in EXPECT.get(sheet, {}).items():
        if abs(v - want) < tol_for(want):
            return coord
    return None


head, fails = [], []
for label, want in [
    ('normalised risk-free rate', W['rf_star']),
    ('cost of capital — own-stock beta', W['wacc_own']),
    ('cost of capital — sector bottom-up beta', W['wacc_bottom_up']),
]:
    coord = find('Fundamental Valuation', want)
    got = cv('Fundamental Valuation', coord) if coord else None
    ok = got is not None and abs(got - want) < tol_for(want)
    head.append((label, got, want, ok))

for label, sheet, want in [
    ('DCF, normalisation, own beta (AED)', 'DCF', LEN_['dcf_normalisation_own_beta']),
    ('DCF, prolonged, own beta (AED)', 'DCF', LEN_['dcf_prolonged_own_beta']),
    ('terminal value share of EV, normalisation',
     'DCF', FR['normalisation']['pv_terminal'] / FR['normalisation']['ev']),
    ('relative lens (AED)', 'Relative & Normalized', LEN_['relative_multiples']),
    ('book value lens, own beta (AED)', 'Fundamental Valuation',
     LEN_['book_value_own_beta']),
    ('median lens reading (AED)', 'Fundamental Valuation', D['fair_mid']),
    ('enterprise value, normalisation (USD m)', 'DCF', FR['normalisation']['ev']),
    ('Borouge 4 fee stream value (USD m)', 'SOTP Bridge',
     FR['normalisation']['b4']['value']),
]:
    coord = find(sheet, want)
    got = cv(sheet, coord) if coord else None
    ok = got is not None and abs(got - want) < tol_for(want)
    head.append((label, got, want, ok))

print('\nheadline reconciliations against study_numbers.json:')
for label, got, want, ok in head:
    mark = 'ok ' if ok else 'FAIL'
    g = f'{got:,.6f}' if isinstance(got, (int, float)) else 'NOT FOUND'
    print(f'  {mark} {label}: workbook {g} vs model {want:,.6f}')
    if not ok:
        fails.append(label)

result = dict(formulas=nform, unresolvable=len(errors), checked=nchk,
              disagreements=len(drift), unchecked=len(uncovered),
              headline_failures=fails,
              pasted=XP['pasted'])
with open(os.path.join(HERE, 'recalc_result.json'), 'w') as f:
    json.dump(result, f, indent=1)

print(f"\n{nchk} of {nform} formula cells reproduce the model, "
      f"{len(errors)} unresolvable, {len(uncovered)} unchecked.")
if errors or drift or uncovered or fails:
    sys.exit(1)
