"""Prove the delivered EMPOWER workbook is a LIVE DRIVER model, not a pasted register.

Each driver below is perturbed in place on the Assumptions sheet, the whole workbook is
re-evaluated from scratch with xlcalc.py, and the test asserts that the Summary central
fair value moves in the asserted direction. A dead-input sweep then bumps every pasted
numeric cell on the non-Assumptions sheets (the audited history, the price-map grid and
the re-run grids) and asserts none of them moves the headline — pasted history must be
display, never a hidden driver.
"""
import json, os
import openpyxl
import xlcalc

HERE = os.path.dirname(os.path.abspath(__file__))
wb = openpyxl.load_workbook(os.path.join(HERE, 'EMPOWER_Valuation_Model_09082026_public.xlsx'))
ANCH = json.load(open(os.path.join(HERE, 'xlsx_expected.json')))['anchors']
CEN_ROW = ANCH['summary']['central']
WACC_ROW = ANCH['dcf']['wacc_ct']

A = {}
for row in wb['Assumptions'].iter_rows(min_col=1, max_col=1):
    c = row[0]
    if isinstance(c.value, str):
        A[c.value] = c.row

def row_of(label):
    if label not in A:
        raise KeyError(f'no Assumptions row labelled {label!r}')
    return A[label]

def read(overrides=None):
    bk = xlcalc.Book(wb, overrides)
    return dict(central=bk.cell_value('Summary', f'B{CEN_ROW}'),
                dcf=bk.cell_value('SOTP Bridge', 'C13'),
                wacc=bk.cell_value('DCF', f'C{WACC_ROW}'),
                ebitda26=bk.cell_value('DCF', 'B6'),
                rev26=bk.cell_value('DCF', 'B5'),
                fcff26=bk.cell_value('DCF', 'B18'),
                tv=bk.cell_value('DCF', 'C29'),
                nd30=bk.cell_value('Balance Sheet', 'I16'))

base = read()
print('base:  ' + ' · '.join(f'{k} {v:,.4f}' for k, v in base.items()))

# label, column, bump, headline, required direction, why
CASES = [
    ('Spot price (AED)', 'C', +0.30, 'central', -1,
     'a higher spot raises the equity weight on the dearer cost of equity, so the '
     'discount rate rises and the valuation falls'),
    ('Beta (own-stock weekly regression vs the Dubai index)', 'C', +0.20, 'central', -1,
     'a higher beta raises the cost of equity and must lower the valuation'),
    ('Risk-free rate (AED sovereign)', 'C', +0.01, 'central', -1,
     'a higher risk-free rate raises the cost of equity and must lower the valuation'),
    ('Equity risk premium — rating basis', 'C', +0.01, 'central', -1,
     'a higher premium raises the cost of equity and must lower the valuation'),
    ('Marginal cost of debt', 'C', +0.01, 'central', -1,
     'a dearer debt book raises the discount rate and the finance charge'),
    ('Corporate tax rate (headline framing)', 'C', +0.03, 'central', -1,
     'a higher tax rate cuts NOPAT throughout and must lower the valuation'),
    ('Terminal growth', 'C', +0.005, 'central', +1,
     'with returns above the cost of capital, growth adds value'),
    ('New connections by year (k RT)', 'B', +50.0, 'central', +1,
     'each added RT earns regulated per-RT revenue worth a multiple of its capex'),
    ('Consumption per-RT recovery level from FY2027 (share of FY2025)', 'C', +0.03,
     'central', +1, 'a stronger consumption recovery lifts revenue from FY2027 onward'),
    ('Electricity and water cost as a share of consumption revenue', 'C', +0.03,
     'central', -1, 'a higher pass-through ratio absorbs more of every consumption '
     'dirham and must lower fair value'),
    ('Capital expenditure per added RT (AED mn per k RT)', 'C', +1.0, 'central', -1,
     'dearer growth capex cuts free cash flow and terminal return on capital'),
    ('Wage and services cost escalator', 'C', +0.01, 'central', -1,
     'faster cash-cost escalation compresses EBITDA every year'),
    ('Net working capital as a share of revenue', 'C', +0.05, 'central', -1,
     'a less negative working-capital ratio absorbs cash as revenue grows and raises '
     'terminal invested capital'),
]

fails = []
print('\nDRIVER DIRECTION TABLE')
for label, col, bump, key, sign, why in CASES:
    r = row_of(label)
    cur = wb['Assumptions'][f'{col}{r}'].value
    assert isinstance(cur, (int, float)), f'driver cell {label!r} {col}{r} is not a value'
    out = read({('Assumptions', f'{col}{r}'): cur + bump})
    delta = out[key] - base[key]
    rel = delta / abs(base[key]) if base[key] else 0.0
    ok = (delta * sign > 0) and abs(rel) > 1e-9
    flag = 'OK ' if ok else 'BAD'
    print(f'  [{flag}] {label} {bump:+g} -> {key} {base[key]:,.4f} -> {out[key]:,.4f} '
          f'({rel:+.2%})   {why}')
    if not ok:
        fails.append((label, key, delta, why))

# ---- dead-input sweep -------------------------------------------------------------
# Every pasted numeric cell OUTSIDE the Assumptions sheet is history, a price-map figure
# or a re-run grid figure. None of them may move the headline. The ONE exception is
# named, not silent: Segments!C20:G20 are the forecast credit-loss cells — pasted zeros
# that are deliberately live inputs in the EBITDA identity (the assumption "no reversal
# of credit losses is forecast" made visible), so bumping them SHOULD reprice the model.
LIVE_ZEROS = {('Segments', f'{c}20') for c in 'CDEFG'}
print('\nDEAD-INPUT SWEEP — pasted cells on non-Assumptions sheets must not move the headline')
dead_movers = []
nswept = 0
for sh in wb.sheetnames:
    if sh in ('Assumptions', 'READ FIRST'):
        continue
    for row in wb[sh].iter_rows():
        for c in row:
            v = c.value
            if not isinstance(v, (int, float)) or isinstance(v, bool):
                continue
            if (sh, c.coordinate) in LIVE_ZEROS:
                continue
            nswept += 1
            out = read({(sh, c.coordinate): v * 1.1 + 1e-3})
            if abs(out['central'] - base['central']) > 1e-9 * max(1, abs(base['central'])):
                dead_movers.append((sh, c.coordinate, v, out['central'] - base['central']))
print(f'  swept {nswept} pasted numeric cells')
if dead_movers:
    for sh, coord, v, dd in dead_movers[:20]:
        print(f'  MOVER: {sh}!{coord} (pasted {v}) shifts central by {dd:+.6g}')
else:
    print('  none moves the central fair value — pasted history is display, not a driver')

assert not fails, f'{len(fails)} drivers failed to move the model correctly: {fails}'
assert not dead_movers, f'pasted cells move the headline: {dead_movers[:10]}'
print(f'\nDRIVER TEST OK — {len(CASES)} drivers each reprice the workbook in the required '
      f'direction; {nswept} pasted cells verified inert')
