"""Independent evaluation of the delivered workbook.

Every formula cell is recalculated by the in-house evaluator (xlcalc). Anything it cannot
parse is a FAILURE, never a skip. Key outputs are then reconciled against the committed
numbers file within tolerance; a driver-nudge test proves the workbook is live (changing a
blue driver reprices the fair value).
"""
import json, os
import openpyxl
from xlcalc import Book

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, 'study_numbers.json')))
wb = openpyxl.load_workbook(os.path.join(HERE, 'GBCO_Valuation_Model_19082026_public.xlsx'))
bk = Book(wb)

# 1) every formula must evaluate
n_ok = 0
fails = []
for sheet, coord in bk.formula_cells():
    try:
        bk.cell_value(sheet, coord)
        n_ok += 1
    except Exception as e:
        fails.append((sheet, coord, str(e)))
if fails:
    for f in fails[:20]:
        print("UNPARSEABLE:", f)
    raise SystemExit(f"RECALC FAIL: {len(fails)} formulas could not be evaluated")
print(f"formulas evaluated: {n_ok}, unparseable: 0")

# 2) reconcile the workbook against the committed model
def close(a, b, tol):
    return abs(a-b) <= tol
checks = [
 ("DCF equity value",        bk.cell_value('DCF', 'B34'),            D['dcf']['auto_eq'],           15.0),
 ("DCF enterprise value",    bk.cell_value('DCF', 'B31'),            D['dcf']['ev'],                15.0),
 ("SOTP/share — round mark", bk.cell_value('SOTP Bridge', 'B13'),    D['both_ways']['A']['sotp'],   0.03),
 ("SOTP/share — book mark",  bk.cell_value('SOTP Bridge', 'C13'),    D['both_ways']['B']['sotp'],   0.03),
 ("central — round mark",    bk.cell_value('Fundamental Valuation', 'B11'), D['lenses']['central']['A'], 0.03),
 ("central — book mark",     bk.cell_value('Fundamental Valuation', 'B12'), D['lenses']['central']['B'], 0.03),
 ("WACC (CDS basis)",        bk.cell_value('Assumptions', 'B29'),    D['wacc']['wacc_cds'],         0.0005),
 ("WACC (rating basis)",     bk.cell_value('Assumptions', 'B30'),    D['wacc']['wacc_rating'],      0.0005),
 ("FY26E group revenue",     bk.cell_value('Income Statement', 'E8'), D['fs_forecast'][0]['group_rev'], 60.0),
 ("FY26E EPS",               bk.cell_value('Income Statement', 'E17'), D['fs_forecast'][0]['eps'],   0.02),
 ("FY30E FCFF",              bk.cell_value('DCF', 'I18'),            D['dcf']['rows'][-1]['fcff'],  10.0),
 ("relative lens (base)",    bk.cell_value('Relative & Normalized', 'C6'), D['lenses']['relative']['base'], 0.05),
 ("normalized lens (base)",  bk.cell_value('Relative & Normalized', 'C14'), D['lenses']['normalized']['base'], 0.35),
 ("FY26E auto revenue",      bk.cell_value('Segments', 'E12'),       D['dcf']['rows'][0]['rev'],    1.0),
 ("FY26E auto gross profit", bk.cell_value('Segments', 'E13'),       D['dcf']['rows'][0]['gp'],     1.0),
 ("sens grid base cell",     bk.cell_value('Sensitivity', 'E9'),     D['sens']['table'][4][2],      0.05),
]
bad = []
for name, got, want, tol in checks:
    ok = close(got, want, tol)
    print(f"{'OK ' if ok else 'FAIL'} {name}: workbook {got:,.3f} vs model {want:,.3f}")
    if not ok:
        bad.append(name)
if bad:
    raise SystemExit(f"RECALC FAIL: {bad}")

# 3) the model is live: nudge a driver, the value must move the right way
base_central = bk.cell_value('Fundamental Valuation', 'B11')
bk2 = Book(wb, overrides={('Assumptions', 'B62'): 0.20})       # discount 10% -> 20%
lower = bk2.cell_value('Fundamental Valuation', 'B11')
bk3 = Book(wb, overrides={('Assumptions', 'B57'): 1800.0})     # round USD 1.4bn -> 1.8bn
higher = bk3.cell_value('Fundamental Valuation', 'B11')
assert lower < base_central < higher, (lower, base_central, higher)
print(f"driver test: central {base_central:.2f}; discount 20% -> {lower:.2f} (down), "
      f"round USD1.8bn -> {higher:.2f} (up) — the workbook reprices")
print("RECALC PASS")
