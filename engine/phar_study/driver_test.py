"""Does the delivered workbook actually reprice when a driver changes?

Recalculation proves the formulas reproduce the model as written. It does NOT prove the model
is wired: a workbook whose headline is a constant would pass it. This test perturbs each input
IN PLACE on the Assumptions sheet, re-evaluates the WHOLE workbook from scratch, and asserts
the headline value per share moves in the asserted DIRECTION.

A dead-input sweep runs over every remaining numeric input on the Assumptions sheet: each is
nudged and the headline must move at all. An input that moves nothing is either genuinely
inert or a wiring failure, and the test names it either way.

If a directional expectation fails, the first hypothesis is that the EXPECTATION is wrong, not
the model. Decompose the mechanism before changing anything.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import openpyxl
import xlcalc

XLSX = os.path.join(HERE, 'EIPICO_Valuation_Model_09082026.xlsx')
wb = openpyxl.load_workbook(XLSX)
wa = wb['Assumptions']


def row_of(text):
    for row in wa.iter_rows(min_col=1, max_col=1):
        for c in row:
            if isinstance(c.value, str) and c.value.strip().startswith(text):
                return c.row
    raise KeyError(text)


HEADLINE = ('SOTP Bridge', None)
for row in wb['SOTP Bridge'].iter_rows(min_col=1, max_col=1):
    for cc in row:
        if isinstance(cc.value, str) and cc.value.startswith('Value per share — Frame A'):
            HEADLINE = ('SOTP Bridge', f'C{cc.row}')


def headline(overrides=None):
    return float(xlcalc.Book(wb, overrides).cell_value(*HEADLINE))


HEADLINE_NAME = 'value per share, Frame A'
BASE = headline()
print(f'base headline value per share: {BASE:.4f}\n')

# (label, cell on Assumptions, multiplier, expected direction, why)
CASES = [
    ('Domestic pack volume growth', f'C{row_of("Domestic pack volume growth")}', 1.20, +1,
     'more packs, more revenue on a cost base that does not rise as fast'),
    ('Export pack volume growth', f'C{row_of("Export pack volume growth")}', 1.20, +1,
     'same, on the hard-currency book'),
    ('Domestic price per pack growth', f'C{row_of("Domestic price per pack growth")}', 1.20, +1,
     'price straight to the margin'),
    ('Export price per pack growth', f'C{row_of("Export price per pack growth")}', 1.50, +1,
     'price straight to the margin'),
    ('Exchange rate, year one', f'C{row_of("Exchange rate (EGP per USD")}', 1.10, -1,
     'a WEAKER pound raises export revenue but ALSO raises the imported ingredient and '
     'packaging cost, which is 79% of the cash cost stack against a 32% export share — the '
     'cost side dominates, so the net effect is negative'),
    ('Selling and marketing / revenue', f'C{row_of("Selling and marketing / revenue")}', 1.20,
     -1, 'a bigger cost share'),
    ('Provision charge, Frame A', f'C{row_of("FRAME A")}', 1.30, -1, 'a bigger cost share'),
    ('Capital expenditure / revenue', f'C{row_of("Capital expenditure / revenue")}', 1.30, -1,
     'cash out of free cash flow'),
    ('Depreciation rate', f'C{row_of("Depreciation rate on the property")}', 1.30, -1,
     'a bigger tax-effected charge; the add-back is not a full offset because the tax shield '
     'is worth less than the charge'),
    ('Inventory days', f'C{row_of("Inventory days")}', 1.20, -1, 'more cash tied up'),
    ('Receivable days', f'C{row_of("Receivable days")}', 1.20, -1, 'more cash tied up'),
    ('Payable days', f'C{row_of("Payable days")}', 1.20, +1, 'less cash tied up'),
    ('Ten-year government yield', f'C{row_of("Ten-year local-currency government yield")}',
     1.10, -1, 'a higher discount rate'),
    ('Sovereign swap spread', f'C{row_of("Sovereign credit-default-swap spread")}', 1.50, +1,
     'a LARGER spread is subtracted from the quoted yield, so the normalised risk-free rate '
     'FALLS and the discount rate with it — this is the whole point of the normalisation'),
    ('Country equity risk premium', f'C{row_of("Country equity risk premium (swap")}', 1.20,
     -1, 'a higher cost of equity'),
    ('Beta', f'C{row_of("Beta")}', 1.30, -1, 'a higher cost of equity'),
    ('Cost of local-currency debt', f'C{row_of("Cost of local-currency debt")}', 1.20, -1,
     'a higher cost of capital'),
    ('Terminal risk-free rate', f'C{row_of("Terminal risk-free rate")}', 1.20, -1,
     'a higher terminal discount rate against a 74% terminal weight'),
    ('Terminal growth', f'C{row_of("Terminal growth")}', 1.20, +1,
     'growth in the terminal numerator and a smaller denominator'),
    ('Terminal return on invested capital',
     f'C{row_of("Terminal return on invested capital")}', 1.30, +1,
     'less reinvestment needed to buy the same growth'),
    ('Normalised associate contribution',
     f'C{row_of("Normalised associate contribution")}', 1.30, +1,
     'a bigger addition in the bridge'),
    ('Associate earnings multiple', f'C{row_of("Associate earnings multiple")}', 1.30, +1,
     'a bigger addition in the bridge'),
    ('Tax rate', f'C{row_of("Corporate income tax rate")}', 1.20, -1,
     'less cash, partly offset by a bigger interest shield in the cost of capital'),
    ('Transfers out of construction', f'C{row_of("Transfers out of construction")}', 1.30, -1,
     'brings the depreciation charge forward'),
    ('Gross borrowings', f'C{row_of("Gross borrowings including leases")}', 1.20, -1,
     'more debt to subtract in the bridge'),
    ('Cash', f'C{row_of("Cash and bank balances")}', 1.50, +1, 'less net debt to subtract'),
    ('Finance cost charged to profit',
     f'C{row_of("Finance cost charged to profit")}', 1.20, -1,
     'lower attributable earnings feed the relative and normalised lenses; the free-cash-flow '
     'lens is unaffected because free cash flow to the firm is struck before financing, so the '
     'Frame A headline itself should NOT move — this case therefore asserts on the weighted '
     'central value, not on the bridge'),
    ('Active-ingredient company at cost',
     f'C{row_of("Active-ingredient company at carrying cost")}', 1.30, +1,
     'a bigger addition in the bridge'),
    ('Non-controlling interests in the bridge',
     f'C{row_of("Non-controlling interests deducted in the bridge")}', 2.00, -1,
     'a bigger deduction in the bridge'),
]

results, failures = [], []
CENTRAL = None
for row in wb['Fundamental Valuation'].iter_rows(min_col=1, max_col=1):
    for cc in row:
        if isinstance(cc.value, str) and cc.value.startswith('WEIGHTED CENTRAL'):
            CENTRAL = ('Fundamental Valuation', f'B{cc.row}')
CENTRAL_BASE = float(xlcalc.Book(wb).cell_value(*CENTRAL))

for label, cell, mult, want, why in CASES:
    base_v = wa[cell].value
    if label == 'Finance cost charged to profit':
        got = float(xlcalc.Book(wb, {('Assumptions', cell): base_v * mult}).cell_value(*CENTRAL))
        move = got - CENTRAL_BASE
        ok = move < -1e-6
        results.append(dict(driver=label, cell=cell, multiplier=mult,
                            base_input=float(base_v), headline=got, move=move,
                            expected='down (weighted central)', passed=bool(ok),
                            mechanism=why))
        print(f"{'PASS' if ok else 'FAIL'}  {label:38s} x{mult:<5.2f} "
              f"{CENTRAL_BASE:8.3f} -> {got:8.3f}  ({move:+8.3f})  expected down [central]")
        if not ok:
            failures.append(label)
        continue
    got = headline({('Assumptions', cell): base_v * mult})
    move = got - BASE
    ok = (move > 1e-6) if want > 0 else (move < -1e-6)
    results.append(dict(driver=label, cell=cell, multiplier=mult, base_input=float(base_v),
                        headline=got, move=move, expected='up' if want > 0 else 'down',
                        passed=bool(ok), mechanism=why))
    print(f"{'PASS' if ok else 'FAIL'}  {label:38s} x{mult:<5.2f} "
          f"{BASE:8.3f} -> {got:8.3f}  ({move:+8.3f})  expected "
          f"{'up' if want > 0 else 'down'}")
    if not ok:
        failures.append(label)
        print(f'       mechanism asserted: {why}')

# ---- dead-input sweep over everything else -----------------------------------
# An input is not "dead" merely because it leaves the Frame A headline alone. The model
# has several headlines and each input belongs to one of them: the effective tax rate
# drives reported earnings, not the free-cash-flow discount; the Frame B provision row
# drives the Frame B value BY CONSTRUCTION and must not touch Frame A; the rating-basis
# spread and premium drive the published alternative cost of equity. So the sweep tests
# each input against the FULL headline set and only calls it dead if it moves none of them.
def cellref(sheet, startswith, col='B'):
    for row in wb[sheet].iter_rows(min_col=1, max_col=1):
        for cc in row:
            if isinstance(cc.value, str) and cc.value.strip().startswith(startswith):
                return (sheet, f'{col}{cc.row}')
    raise KeyError(f'{sheet}: {startswith}')


def rowref(sheet, startswith, col):
    for row in wb[sheet].iter_rows(min_col=1, max_col=1):
        for cc in row:
            if isinstance(cc.value, str) and cc.value.strip().startswith(startswith):
                return (sheet, f'{col}{cc.row}')
    raise KeyError(f'{sheet}: {startswith}')


HEADLINES = {
    'value per share, Frame A': HEADLINE,
    'value per share, Frame B': cellref('DCF', 'VALUE PER SHARE ON FRAME B'),
    'weighted central fair value': cellref('Fundamental Valuation', 'WEIGHTED CENTRAL'),
    'FY2026E earnings per share': rowref('Income Statement', 'Earnings per share', 'E'),
    'FY2030E book value per share': rowref('Balance Sheet', 'Book value per share', 'I'),
    'FY2030E total assets': rowref('Balance Sheet', 'TOTAL ASSETS', 'I'),
    'FY2030E return on invested capital': rowref('Per-Share & Ratios',
                                                 'Return on invested', 'I'),
    'cost of equity, rating basis': ('Assumptions',
                                     f"C{row_of('Cost of equity, rating basis')}"),
}
BASES = {k: float(xlcalc.Book(wb).cell_value(*v)) for k, v in HEADLINES.items()}
print('\nheadline set used by the sweep:')
for k, v in BASES.items():
    print(f'   {k:38s} {v:14,.4f}')

print('\ndead-input sweep over every remaining numeric input on Assumptions:')
tested = {c for _, c, *_ in CASES}
dead, live, disclosure = [], [], []
for row in wa.iter_rows(min_col=3, max_col=7):
    for cell in row:
        if cell.coordinate in tested or not isinstance(cell.value, (int, float)):
            continue
        basis = wa[f'B{cell.row}'].value
        if isinstance(basis, str) and basis.strip() == 'calculated':
            continue                                   # a derived row, not an input
        if isinstance(basis, str) and basis.startswith('disclosure'):
            disclosure.append((wa[f'A{cell.row}'].value, cell.coordinate))
            continue
        base_v = cell.value
        if base_v == 0:
            continue
        ov = {('Assumptions', cell.coordinate): base_v * 1.15}
        bk = xlcalc.Book(wb, ov)
        moved = [k for k, v in HEADLINES.items()
                 if abs(float(bk.cell_value(*v)) - BASES[k]) > 1e-9]
        if moved:
            live.append((wa[f'A{cell.row}'].value, cell.coordinate, moved))
        else:
            dead.append((wa[f'A{cell.row}'].value, cell.coordinate))
print(f'  {len(live)} further inputs move at least one headline; {len(dead)} move none; '
      f'{len(disclosure)} are disclosure rows, excluded by design')
byhead = {}
for name, coord, moved in live:
    if HEADLINE_NAME not in moved:
        byhead.setdefault(', '.join(moved), []).append(f'{coord} {name}')
if byhead:
    print('  inputs that leave the Frame A headline alone, and what they DO move:')
    for heads, items in sorted(byhead.items()):
        print(f'    -> {heads}')
        for it in items:
            print(f'         {it}')
for name, coord in disclosure:
    print(f'  DISCLOSURE (not a driver)  {coord}  {name}')
for name, coord in dead:
    print(f'  DEAD  {coord}  {name}')

json.dump(dict(base=BASE, headline_bases=BASES, cases=results, failures=failures,
               dead_inputs=[[n, c] for n, c in dead],
               disclosure_rows=[[n, c] for n, c in disclosure],
               live_inputs=[[n, c, m] for n, c, m in live]),
          open(os.path.join(HERE, 'driver_test_result.json'), 'w'), indent=1)
assert not failures, f'{len(failures)} driver(s) did not move the headline as asserted: {failures}'
assert not dead, f'{len(dead)} dead input(s): {dead}'
print(f'\nDRIVER TEST PASSED — {len(CASES)} asserted directions all correct, '
      f'{len(live)} further inputs live against at least one headline, 0 dead '
      f'({len(disclosure)} disclosure rows excluded by design).')
