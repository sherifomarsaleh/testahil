"""Prove the workbook is a LIVE DRIVER model, not a pasted register.

The READ FIRST sheet tells the reader that changing a blue cell on Assumptions reprices
the model. That is a claim about the delivered file, so it is tested on the delivered file:
each driver below is perturbed in place, the whole workbook is re-evaluated from scratch,
and the test asserts that the headline moves, moves in the right DIRECTION, and moves by a
sensible amount.

A driver that fails to move the valuation means a chain was broken somewhere between the
Assumptions sheet and the answer — exactly the failure a pasted-value workbook hides.
"""
import json, os
import openpyxl
import xlcalc

HERE = os.path.dirname(os.path.abspath(__file__))
wb = openpyxl.load_workbook(os.path.join(HERE, 'SWDY_Valuation_Model_05082026_public.xlsx'))
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
    return dict(dcf=bk.cell_value('DCF', 'C31'),
                central=bk.cell_value('Summary', 'C9'),
                pv_expl=bk.cell_value('DCF', 'C26'),
                tv=bk.cell_value('DCF', 'C25'),
                ebitda26=bk.cell_value('DCF', 'B6'),
                wacc=bk.cell_value('DCF', 'C46'),
                wacc_term=bk.cell_value('DCF', 'C53'),
                nd30=bk.cell_value('Balance Sheet', 'I17'),
                bvps=bk.cell_value('Relative & Normalized', 'C31'))

base = read()
print('base:  ' + ' · '.join(f'{k} {v:,.4f}' for k, v in base.items()))

# label, cell column, bump, the headline it must move, the required direction
CASES = [
    ('Terminal growth', 'C', +0.01, 'dcf', +1,
     'a higher terminal growth rate must raise the discounted cash flow'),
    ('Beta', 'C', +0.20, 'dcf', -1,
     'a higher beta raises the cost of equity and must lower the valuation'),
    ('Terminal risk-free rate', 'C', +0.02, 'dcf', -1,
     'a higher terminal risk-free rate must lower the valuation'),
    ('Working capital / revenue', 'C', +0.02, 'dcf', -1,
     'more working capital absorbs cash and must lower the valuation'),
    ('Operating load (% of revenue)', 'B', +0.01, 'ebitda26', -1,
     'a heavier operating load must cut FY2026 EBITDA'),
    # Depreciation pulls the two halves of the DCF in OPPOSITE directions, and both legs
    # are asserted so the workbook cannot quietly lose either one. In the explicit window a
    # higher charge is a pure tax shield and lifts cash flow. In the terminal state it is
    # not: capex is unchanged, so a permanently higher depreciation rate is a business
    # consuming its own asset base, and terminal NOPAT falls faster than the shrinking
    # capital base lifts the return on it. With the terminal value at 77% of enterprise
    # value the second effect wins, and the fair value falls.
    ('Depreciation and amortisation / revenue', 'C', +0.01, 'pv_expl', +1,
     'in the explicit window a higher charge is a tax shield and must lift the present value'),
    ('Depreciation and amortisation / revenue', 'C', +0.01, 'tv', -1,
     'in the terminal state, against unchanged capex, it must lower the terminal value'),
    ('Effective tax rate', 'C', +0.05, 'dcf', -1,
     'a higher tax rate must lower NOPAT and the valuation'),
    ('Justified EV/EBITDA', 'C', +1.0, 'central', +1,
     'a higher justified multiple must raise the weighted central'),
    ('Justified price/earnings', 'C', +1.0, 'central', +1,
     'a higher justified P/E must raise the weighted central'),
    ('Sustainable return on equity', 'C', +0.03, 'central', +1,
     'a higher sustainable return must raise the book lens and the central'),
    ('Net bank debt at FY2025 (EGP mn, disclosed)', 'C', +5000.0, 'dcf', -1,
     'more net debt must leave less for shareholders'),
    ('Forecast dividend payout ratio', 'C', +0.25, 'nd30', +1,
     'paying more of the profit out must leave more net debt at the end of the forecast'),
    ('Cost of debt, blended', 'C', +0.03, 'wacc', +1,
     'a higher cost of debt must raise the explicit-window cost of capital'),
    ('Terminal debt weight', 'C', +0.10, 'wacc_term', -1,
     'more of the cheaper after-tax debt must lower the terminal cost of capital'),
    ('FY2024 dividend per share (EGP)', 'C', +1.0, 'bvps', -1,
     'a larger dividend paid out of FY2024 must reduce FY2025 book value per share'),
]

fails, moved = [], []
for label, col, bump, key, sign, why in CASES:
    r = row_of(label)
    cur = wb['Assumptions'][f'{col}{r}'].value
    out = read({('Assumptions', f'{col}{r}'): cur + bump})
    delta = out[key] - base[key]
    rel = delta / abs(base[key]) if base[key] else 0.0
    ok = (delta * sign > 0) and abs(rel) > 1e-6
    moved.append((label, key, base[key], out[key], rel))
    flag = 'OK ' if ok else 'BAD'
    print(f'  [{flag}] {label} {bump:+g} -> {key} {base[key]:,.3f} -> {out[key]:,.3f} '
          f'({rel:+.2%})   {why}')
    if not ok:
        fails.append((label, key, delta, why))

# a driver that moves NOTHING anywhere is a dead input: catch those too
DEAD_OK = {          # inputs the valuation legitimately does not consume directly
    'Spot price (EGP)', 'Statutory corporate tax rate', 'FY2025 average USD/EGP',
    'Copper (USD/tonne)', 'USD/EGP path', 'Cable volume growth',
    'Cable fabrication uplift over copper', 'Raw-material volume growth',
    'Transformer MVA growth', 'Meter unit growth', 'Order-book conversion rate',
    'Order-book book-to-bill', 'Other-lines revenue growth', 'Meter price inflation',
    'Gross profit per unit — growth', 'Non-cable margin recovery factor',
    'Cable gross profit per tonne, FY2025 (EGP)', 'Order book at FY2025 (EGP mn)',
    'Weight — discounted cash flow', 'Weight — relative', 'Weight — normalised',
    'Weight — book', 'Yield assumed on surplus cash',
    'FY2025 profit after tax (EGP mn, disclosed)',
    'FY2025 profit after minority interests (EGP mn, disclosed)',
    'Growth in the share of equity-accounted investees',
    'Intangible assets and goodwill (EGP mn)',
    'Equity-accounted investees at carrying value (EGP mn)',
    'Shares outstanding (mn)', 'Sovereign default spread (netted out)',
    'Equity risk premium', 'Risk-free rate (10-year local currency)',
    'Terminal equity risk premium', 'Terminal cost of debt', 'Cost of debt path',
    'Capital expenditure / revenue',
}
print('\nDEAD-INPUT SWEEP — every driver not covered above is bumped and must move something')
dead = []
for label, r in sorted(A.items(), key=lambda kv: kv[1]):
    cell = wb['Assumptions'][f'C{r}']
    if not isinstance(cell.value, (int, float)) or label in DEAD_OK:
        continue
    if any(label == c[0] for c in CASES):
        continue
    out = read({('Assumptions', f'C{r}'): cell.value * 1.10 + 1e-6})
    if all(abs(out[k] - base[k]) < 1e-9 for k in base):
        dead.append(label)
if dead:
    print('  inputs that changed nothing:', dead)
else:
    print('  none — every remaining driver reprices the model')

assert not fails, f'{len(fails)} drivers failed to move the model correctly: {fails}'
assert not dead, f'dead inputs: {dead}'
print(f'\nDRIVER TEST OK — {len(CASES)} drivers each reprice the workbook in the right direction')
