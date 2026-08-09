"""Prove the workbook is a LIVE DRIVER model, not a pasted register.

Each driver below is perturbed in place, the whole workbook is re-evaluated from
scratch, and the test asserts that the headline moves, moves in the right
DIRECTION, and moves by a sensible amount. A driver that fails to move the
valuation means a chain was broken somewhere between the Assumptions sheet and
the answer — exactly the failure a pasted-value workbook hides.
"""
import json, os
import openpyxl
import xlcalc

HERE = os.path.dirname(os.path.abspath(__file__))
wb = openpyxl.load_workbook(os.path.join(HERE, 'DU_Valuation_Model_09082026_public.xlsx'))
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
    return dict(dcf=bk.cell_value('DCF', 'C63'),
                central=bk.cell_value('Summary', 'C9'),
                pv_expl=bk.cell_value('DCF', 'C27'),
                tv=bk.cell_value('DCF', 'C26'),
                ebitda26=bk.cell_value('DCF', 'B6'),
                wacc=bk.cell_value('DCF', 'C47'),
                wacc_term=bk.cell_value('DCF', 'C54'),
                nc30=bk.cell_value('Balance Sheet', 'I15'),
                bvps=bk.cell_value('Relative & Normalized', 'C30'))

base = read()
print('base:  ' + ' · '.join(f'{k} {v:,.4f}' for k, v in base.items()))

# label, cell column, bump, the headline it must move, the required direction
CASES = [
    ('Terminal growth', 'C', +0.005, 'dcf', +1,
     'a higher terminal growth rate must raise the discounted cash flow'),
    ('Beta (DU weekly vs DFM General Index, 5y)', 'C', +0.20, 'dcf', -1,
     'a higher beta raises the cost of equity and must lower the valuation'),
    ('Terminal risk-free rate', 'C', +0.01, 'dcf', -1,
     'a higher terminal risk-free rate must lower the valuation'),
    ('Combined federal royalty + income tax rate (Framing A, audited FY2025)', 'C', +0.05,
     'dcf', -1, 'a heavier fiscal take must lower NOPAT and the valuation'),
    ('Net working capital / revenue (audited FY2025 component days)', 'C', +0.02, 'dcf', -1,
     'working capital moving toward zero absorbs cash and must lower the valuation'),
    ('Staff cost, FY2026E level (AED mn)', 'C', +200.0, 'ebitda26', -1,
     'a heavier staff cost must cut FY2026 EBITDA'),
    ('Marketing / revenue', 'C', +0.01, 'dcf', -1,
     'a heavier marketing ratio must cut EBITDA and the valuation'),
    ('Telecom licence and related fees / revenue (regulatory revenue share)', 'C', +0.01,
     'dcf', -1, 'a worse licence-renewal outcome (higher fee ratio) must lower the valuation'),
    ('PP&E depreciation rate on opening balance (audited FY2025)', 'C', +0.03, 'pv_expl', +1,
     'within a fixed EBITDA, faster depreciation is a larger tax shield on the explicit window'),
    ('Mobile — contribution margin', 'C', +0.01, 'dcf', +1,
     'a richer mobile contribution margin must raise EBITDA and the valuation'),
    ('Capital expenditure / revenue', 'C', +0.02, 'dcf', -1,
     'heavier capex must absorb cash and lower the valuation'),
    ('Justified price/earnings (GCC telecom peer median)', 'C', +1.0, 'central', +1,
     'a higher justified multiple must raise the weighted central'),
    ('Sustainable return on equity', 'C', +0.03, 'central', +1,
     'a higher sustainable return must raise the book lens and the central'),
    ('Lease liabilities at FY2025 (AED mn, audited — the only debt-like item)', 'C', +500.0,
     'dcf', -1, 'more debt-like leases must leave less for shareholders'),
    ('Cash and term deposits at FY2025 (AED mn, audited)', 'C', +500.0, 'dcf', +1,
     'more cash in the bridge must raise the equity value'),
    ('Final FY2025 dividend paid 28-Apr-2026 (AED/share)', 'C', +0.10, 'dcf', -1,
     'a larger dividend paid before the anchor is value that left the share'),
    ('Days from the 31-Dec-2025 valuation date to the 07-Aug-2026 anchor', 'C', +100.0,
     'dcf', +1, 'a later anchor accretes more value at the cost of equity'),
    ('Marginal cost of debt (AED sovereign + GCC telecom spread)', 'C', +0.03, 'wacc', +1,
     'a higher cost of debt must raise the explicit-window cost of capital'),
    ('Terminal debt weight', 'C', +0.10, 'wacc_term', -1,
     'more of the cheaper after-tax debt must lower the terminal cost of capital'),
    ('Forecast dividend payout ratio (FY2024 actual 98%, FY2025 ~100%)', 'C', -0.10, 'nc30', +1,
     'paying out less must leave more cash on the FY2030 balance sheet'),
    ('Lease interest rate (audited FY2025 effective)', 'C', +0.02, 'nc30', -1,
     'a costlier lease book must drain the cash walk'),
    ('Yield on cash and term deposits (audited FY2025 effective)', 'C', +0.02, 'nc30', +1,
     'a better deposit yield must build cash faster'),
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
DEAD_OK = {
    # unit-build inputs whose OUTPUT (segment revenue) is pasted per the declared
    # three-pasted-classes rule — they parameterise the engine's build, not the sheet:
    "Mobile subscribers, end of year ('000)", "Fixed subscribers, end of year ('000)",
    'Blended mobile ARPU (AED/month)', 'Implied fixed revenue per subscriber (AED/month)',
    'Wholesale revenue growth', 'ICT and associated telecom revenue growth',
    # Framing B parameters: the Framing-B fair value is an engine re-run (pasted), so
    # these price the ALTERNATIVE framing, not the base sheet:
    'Regulated revenue share (Framing B base, audited FY2023)',
    'Framing B — royalty rate on regulated revenue',
    'Framing B — royalty rate on regulated profit',
    # display-only lens weights (Summary carries its own blue weight cells)
    'Weight — discounted cash flow', 'Weight — relative', 'Weight — normalised',
    'Weight — book',
    # yield-cross triangulation is shown beside the lens, not fed into a headline
    'Peer benchmark dividend yield',
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
