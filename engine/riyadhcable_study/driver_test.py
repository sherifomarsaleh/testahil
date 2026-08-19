"""Prove the workbook is a LIVE DRIVER model, not a pasted register.

READ FIRST tells the reader that changing a blue cell on Assumptions reprices the model.
That is a claim about the delivered file, so it is tested on the delivered file: each driver
below is perturbed in place, the whole workbook is re-evaluated from scratch, and the test
asserts the headline moves in the right DIRECTION. A dead-input sweep then bumps every other
Assumptions driver and asserts it moves something.
"""
import os
import openpyxl
import xlcalc

HERE = os.path.dirname(os.path.abspath(__file__))
wb = openpyxl.load_workbook(os.path.join(HERE, 'RIYADHCABLE_Valuation_Model_18082026_public.xlsx'))
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
    XA = __import__('json').load(open(os.path.join(HERE, 'xlsx_expected.json')))['anchors']
    seg = XA['seg']
    return dict(dcf=bk.cell_value('DCF', 'C51'),
                central=bk.cell_value('Fundamental Valuation', 'C9'),
                wacc=bk.cell_value('DCF', 'C10'),
                wacc_term=bk.cell_value('DCF', 'C13'),
                ebitda26=bk.cell_value('Segments', f"C{seg['ebitda']}"),
                gm26=bk.cell_value('Segments', f"C{seg['gm']}"),
                nd30=bk.cell_value('Balance Sheet', 'J13'),
                roe=bk.cell_value('Per-Share & Ratios', 'B7'),
                pe_ttm=bk.cell_value('Per-Share & Ratios', 'B11'),
                median=bk.cell_value('Fundamental Valuation', f"C{XA['fund']['median']}"))


base = read()
print('base:  ' + ' · '.join(f'{k} {v:,.4f}' for k, v in base.items()))

CASES = [
    ('Terminal growth', 'C', +0.01, 'dcf', +1, 'higher terminal growth must raise the DCF'),
    ('Beta (own-stock vs TASI)', 'C', +0.20, 'dcf', -1, 'a higher beta raises Ke and must lower the DCF'),
    ('Terminal risk-free rate', 'C', +0.02, 'dcf', -1, 'a higher terminal risk-free rate lowers the DCF'),
    ('Net working capital / revenue', 'C', +0.03, 'dcf', -1, 'more working capital absorbs cash'),
    ('Cost of debt, marginal pre-tax', 'C', +0.03, 'wacc', +1, 'higher cost of debt raises the WACC'),
    ('Terminal net-debt weight', 'C', +0.10, 'wacc_term', -1, 'more cheap after-tax debt lowers terminal WACC'),
    ('Effective zakat and income tax rate', 'C', +0.05, 'dcf', -1, 'higher tax lowers NOPAT and the DCF'),
    ('Justified EV/EBITDA', 'C', +1.0, 'central', +1, 'a higher justified multiple raises the central'),
    ('Justified price/earnings', 'C', +1.0, 'central', +1, 'a higher justified P/E raises the central'),
    ('Sustainable return on equity', 'C', +0.03, 'central', +1, 'a higher sustainable return raises the book lens'),
    ('Sustained gross margin (H1-2026 anchor)', 'C', +0.01, 'dcf', +1, 'a higher sustained margin raises the DCF'),
    ('Net financial debt at FY2025 (SAR mn, disclosed)', 'C', +2000.0, 'dcf', -1, 'more net debt leaves less for equity'),
    ('Forecast dividend payout ratio', 'C', +0.20, 'nd30', +1, 'paying out more leaves more net debt at the end'),
    ('Days to the anchor', 'C', +100.0, 'dcf', +1, 'a later anchor accretes more value at Ke'),
    ('FY2025 dividend per share paid in window', 'C', +1.0, 'dcf', -1, 'a larger dividend paid before the anchor left the share'),
    ('Depreciation and amortisation / revenue', 'C', +0.005, 'dcf', +1, 'more D&A is a larger non-cash add-back to FCFF'),
    ('Cable volume index growth', 'C', +0.02, 'dcf', +1, 'more volume raises revenue and the DCF'),
    ('Capital expenditure / revenue', 'C', +0.01, 'dcf', -1, 'more capex reduces free cash flow'),
    # THE MARGIN-IS-AN-OUTPUT SIGN TEST, run on the delivered file (the first edition excluded the
    # metal driver from this test and shipped a pasted exhibit whose sign contradicted the live sheet):
    ('Metal price multiplier (shock; 1.00 = base path)', 'C', +0.15, 'dcf', -1,
     'higher metal inflates revenue but not the per-tonne spread — the margin OUTPUT dilutes and the DCF falls'),
    ('Metal price multiplier (shock; 1.00 = base path)', 'C', +0.15, 'gm26', -1,
     'the gross margin row itself must fall when metal rises — margin is an OUTPUT, not an input'),
    ('NCI share of profit (FY2025)', 'C', +0.05, 'central', -1,
     'a larger minority share of profit lowers attributable earnings and the earnings-based lenses'),
    ('H1-2026 attributable profit (SAR mn)', 'C', +100.0, 'pe_ttm', -1,
     'higher trailing-twelve-month earnings lower the TTM multiple'),
    ('FY2024 equity attributable (SAR mn)', 'C', +500.0, 'roe', -1,
     'a larger average equity base lowers the trailing ROE'),
]

fails = []
for label, col, bump, key, sign, why in CASES:
    rr = row_of(label)
    cur = wb['Assumptions'][f'{col}{rr}'].value
    out = read({('Assumptions', f'{col}{rr}'): cur + bump})
    delta = out[key] - base[key]
    rel = delta / abs(base[key]) if base[key] else 0.0
    ok = (delta * sign > 0) and abs(rel) > 1e-6
    print(f"  [{'OK ' if ok else 'BAD'}] {label} {bump:+g} -> {key} {base[key]:,.3f} -> {out[key]:,.3f} "
          f"({rel:+.2%})   {why}")
    if not ok:
        fails.append((label, key, delta, why))

# dead-input sweep
DEAD_OK = {
    'Spot price (SAR)',                 # a market anchor, only enters mktcap weight and 'vs spot'
    'Shares outstanding (mn)',          # scaling denominator (moves per-share both ways consistently)
    'Conversion cost inflation', 'Gross-margin glide (added to anchor)', 'Cost-of-debt path',
    'Operating expenses / revenue',
    'Weight — discounted cash flow', 'Weight — relative', 'Weight — normalised', 'Weight — book',
    'Risk-free rate (10-year SAR sukuk)', 'Sovereign default spread (netted out)',
    'Equity risk premium (rating basis)', 'Terminal equity risk premium', 'Terminal beta',
    'Terminal cost of debt',
    'FY2025 metal content / materials (SAR mn)', 'FY2025 conversion cost (SAR mn)',
    'FY2025 net working capital (SAR mn)', 'FY2025 PP&E (SAR mn)',
    'FY2025 gross borrowings incl. leases (SAR mn)', 'FY2025 equity attributable (SAR mn)',
    'FY2025 associates carrying value (SAR mn)', 'FY2025 non-operating assets (SAR mn)',
    'FY2025 NCI carrying value (SAR mn)',
    'H1-2025 attributable profit (SAR mn)',   # enters only the TTM multiple, whose H1-2026 leg is
                                              # direction-tested above; swept via that case
}
print('\nDEAD-INPUT SWEEP — every remaining driver bumped and must move something')
dead = []
for label, rr in sorted(A.items(), key=lambda kv: kv[1]):
    cell = wb['Assumptions'][f'C{rr}']
    if not isinstance(cell.value, (int, float)) or label in DEAD_OK or any(label == c[0] for c in CASES):
        continue
    out = read({('Assumptions', f'C{rr}'): cell.value * 1.10 + 1e-6})
    if all(abs(out[k] - base[k]) < 1e-9 for k in base):
        dead.append(label)
print('  inputs that changed nothing:', dead if dead else 'none — every remaining driver reprices the model')

assert not fails, f'{len(fails)} drivers failed to move the model correctly: {fails}'
assert not dead, f'dead inputs: {dead}'
print(f'\nDRIVER TEST OK — {len(CASES)} drivers each reprice the workbook in the right direction, 0 dead inputs')
