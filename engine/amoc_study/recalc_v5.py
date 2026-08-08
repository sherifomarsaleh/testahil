"""Recalculate the DELIVERED workbook and reconcile it cell by cell against the model.

Three gates, in increasing strength:

  1. every formula in the workbook must EVALUATE. Anything the evaluator cannot parse is a
     FAILURE, never a skip. A skipped cell is an unchecked cell.
  2. every formula cell must reproduce the value the MODEL computed for it. The builder records
     those as it writes. This is what makes a formula-driven workbook safe: a formula that
     computes the right thing the wrong way, or points one row off, fails here rather than
     shipping a different number from the study.
  3. headline reconciliations against study_numbers.json, as an independent check on the
     expected map itself.

Recalculation runs through the explicit evaluator in xlcalc.py rather than through the library
that wrote the file: an independent reimplementation that has to agree cell for cell is the
stronger check.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import openpyxl                                                        # noqa: E402
import xlcalc                                                          # noqa: E402

XLSX = os.path.join(HERE, 'AMOC_Valuation_Model_08082026_public.xlsx')
wb = openpyxl.load_workbook(XLSX)
D = json.load(open(os.path.join(HERE, 'study_numbers.json')))
XP = json.load(open(os.path.join(HERE, 'xlsx_expected_v5.json')))
EXPECT = XP['expected']
BK = xlcalc.Book(wb)
g = BK.cell_value

nform, unresolved, wrong, checked = 0, [], [], 0
for sh, coord in BK.formula_cells():
    nform += 1
    try:
        v = g(sh, coord)
        if v is None or (isinstance(v, float) and v != v):
            unresolved.append((sh, coord, 'evaluated to nothing'))
            continue
    except Exception as e:                                             # noqa: BLE001
        unresolved.append((sh, coord, f'{type(e).__name__}: {e}'))
        continue
    exp = EXPECT.get(sh, {}).get(coord)
    if exp is None:
        unresolved.append((sh, coord, 'no expected value recorded — cell is UNCHECKED'))
        continue
    checked += 1
    tol = max(abs(exp) * 2e-6, 5e-7)
    if abs(float(v) - exp) > tol:
        wrong.append((sh, coord, float(v), exp))

print(f'GATE 1  formula cells            {nform}')
print(f'GATE 1  unresolvable / unchecked {len(unresolved)}')
print(f'GATE 2  checked against model    {checked}')
print(f'GATE 2  disagreements            {len(wrong)}')
for s_, c_, why in unresolved[:15]:
    print(f'   UNRESOLVED {s_}!{c_}: {why}')
for s_, c_, got, exp in wrong[:20]:
    print(f'   DISAGREE   {s_}!{c_}: workbook {got:,.6f} vs model {exp:,.6f}')

# ---- gate 3: headline reconciliations, independent of the expected map -------
FR = {r for r in [XP.get('n_formula')]}
checks = []


def chk(name, got, want, tol=0.005):
    ok = abs(got - want) <= tol
    checks.append((name, got, want, ok))
    return ok


ps_row = None
for coord, val in EXPECT.get('Forecast', {}).items():
    pass
chk('weighted central, Lenses!B15', g('Lenses', 'B15'), D['central'])
chk('DCF lens, Lenses!B10', g('Lenses', 'B10'), D['lenses']['dcf']['base'])
chk('relative lens, Lenses!C11', g('Lenses', 'C11'), D['lenses']['relative']['base'])
chk('normalised lens, Lenses!D12', g('Lenses', 'D12'), D['lenses']['normalized']['base'])
chk('book lens, Lenses!E13', g('Lenses', 'E13'), D['lenses']['book']['base'])
chk('base-year revenue, Base Year!B19', g('Base Year', 'B19'), D['ttm']['rev'], 1.0)
chk('base-year gross margin, Base Year!B22', g('Base Year', 'B22'), D['ttm']['gm'], 1e-6)
chk('per-line cost foots, Product and Cost!B36', g('Product and Cost', 'B36'), 0.0, 1e-3)
chk('inventory days, Base Year!B44', g('Base Year', 'B44'), D['rates']['inv_days'], 1e-4)
chk('minority rate, Base Year!B41', g('Base Year', 'B41'), D['rates']['nci_op'], 1e-6)
chk('released-GP overstatement, Base Year!B17', g('Base Year', 'B17'), D['ttm']['ct3'], 1e-6)

print('\nGATE 3  headline reconciliations')
for nm, got, want, ok in checks:
    print(f"   {'PASS' if ok else 'FAIL'}  {nm}: {got:,.6f} vs {want:,.6f}")

bad = len(unresolved) + len(wrong) + sum(1 for *_, ok in checks if not ok)
print(f"\nFORMULA SHARE  {XP['n_formula']} formulas / {XP['n_pasted']} pasted = "
      f"{XP['n_formula']/(XP['n_formula']+XP['n_pasted']):.1%}")
print('RESULT:', 'PASS' if bad == 0 else f'FAIL — {bad} problem(s)')
sys.exit(1 if bad else 0)
