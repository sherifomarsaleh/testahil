"""Recalculate the DELIVERED workbook and reconcile it cell-by-cell against the model.

Recalculation runs through the explicit evaluator in xlcalc.py, independently of the
library that wrote the file. Anything the evaluator cannot parse is a FAILURE, never a
skip — a permissive verifier is worse than no verifier.

Three gates:
  1. every formula in the workbook must evaluate;
  2. EVERY formula cell must reproduce the value the model computed for it as it wrote
     (xlsx_expected.json), and no formula cell may be left unchecked;
  3. headline reconciliations against study_numbers.json, as an independent cross-check
     on the expected map itself.
"""
import json, os, sys
import openpyxl, xlcalc

HERE = os.path.dirname(os.path.abspath(__file__))
XLSX = os.path.join(HERE, 'EGCH_Valuation_Model_03092026.xlsx')
wb = openpyxl.load_workbook(XLSX)
D = json.load(open(os.path.join(HERE, 'study_numbers.json')))
EXPECT = json.load(open(os.path.join(HERE, 'xlsx_expected.json')))
BK = xlcalc.Book(wb)
cv = BK.cell_value

nform, unresolvable, checked, mism = 0, [], 0, []
seen = set()
for sh, coord in BK.formula_cells():
    nform += 1
    key = f"{sh}!{coord}"
    seen.add(key)
    try:
        got = cv(sh, coord)
    except Exception as ex:
        unresolvable.append(f"{key}: {ex}")
        continue
    if key not in EXPECT:
        mism.append(f"{key}: formula cell with NO recorded model value (unchecked)")
        continue
    want = EXPECT[key]
    got = float(got if got is not None else 0.0)
    tol = max(abs(want) * 1e-6, 1e-6)
    checked += 1
    if abs(got - want) > tol:
        mism.append(f"{key}: workbook {got:,.6f} vs model {want:,.6f}")

orphan = [k for k in EXPECT if k not in seen]
print(f"formula cells in workbook : {nform}")
print(f"unresolvable              : {len(unresolvable)}")
_bad = len([m for m in mism if "vs model" in m])
print(f"reproduce the model       : {checked - _bad}")
print(f"mismatches                : {len([m for m in mism if 'vs model' in m])}")
print(f"unchecked formula cells   : {len([m for m in mism if 'unchecked' in m])}")
print(f"recorded but not in file  : {len(orphan)}")
for x in (unresolvable + mism + [f'ORPHAN {o}' for o in orphan])[:25]:
    print("  !", x)

# ---- gate 3: headline reconciliations, independent of the expected map -------
def close(a, b, tol=0.01):
    return abs(a - b) <= max(abs(b) * tol, 0.01)

LNS = json.load(open(os.path.join(HERE, 'lenses.json')))
checks = []
for case, col in [("base", "B"), ("halt", "D")]:
    b = D['cases'][case]['bridge']
    checks.append((f"{case} enterprise value", cv("DCF", f"{col}37"), b['ev']))
    checks.append((f"{case} terminal value share", cv("DCF", f"{col}38"), b['tv_pct_ev']))
    checks.append((f"{case} equity", cv("DCF", f"{col}45"), b['equity']))
    checks.append((f"{case} per share", cv("DCF", f"{col}44"), b['per_share']))
checks.append(("cost of capital, year one", cv("DCF", "B15"), D['drivers']['wacc_path'][0]))
ADDR = json.load(open(os.path.join(HERE, 'xlsx_addresses.json')))
checks.append(("terminal cost of capital", cv("Assumptions", ADDR['wacc_terminal']),
               D['drivers']['wacc_terminal']))
# the CENTRAL basis is the CDS one [R-COC-01]; this gate was still reconciling
# against the rating figure after the study moved [corrected 03-Sep-2026]
checks.append(("cost of equity", cv("Assumptions", ADDR['cost_of_equity']), D['wacc']['ke_cds']))
checks.append(("normalised risk-free rate", cv("Assumptions", ADDR['rf_star']),
               D['wacc']['rf_star_cds']))
checks.append(("lens 2 value per share", cv("Fundamental Valuation", "B18"),
               LNS['book']['value_per_share']))
checks.append(("lens 3 value per share", cv("Relative & Normalized", "B12"),
               LNS['relative']['value_per_share']))
checks.append(("lens 4 value per share", cv("Relative & Normalized", "B31"),
               LNS['normalised']['value_per_share']))
checks.append(("contested judgement gap", cv("Summary", "B22"), LNS['contested']['gap']))
bad = [(n, g, w) for n, g, w in checks if not close(float(g), float(w))]
print(f"\nheadline reconciliations  : {len(checks) - len(bad)}/{len(checks)} pass")
for n, g, w in bad:
    print(f"  ! {n}: {g} vs {w}")

ok = not unresolvable and not mism and not orphan and not bad
print(f"\n{'PASS' if ok else 'FAIL'}: "
      f"{checked - _bad} of {nform} formula cells reproduce the model, "
      f"{len(unresolvable)} unresolvable, "
      f"{len([m for m in mism if 'unchecked' in m])} unchecked")
# the verdict is written for attest.py to READ, never re-asserted there [R-ENF-01]
json.dump({"pass": bool(ok), "formula_cells": nform, "reproduce": checked - _bad,
           "mismatches": len(mism), "unresolvable": len(unresolvable), "orphans": len(orphan),
           "headline_checks": len(checks), "headline_failures": len(bad)},
          open("recalc_result.json", "w"), indent=1)
sys.exit(0 if ok else 1)
