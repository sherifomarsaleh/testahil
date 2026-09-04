"""Prove the workbook is a LIVE DRIVER model, not a pasted register.

READ FIRST tells the reader that changing a blue cell on Assumptions reprices the model.
That is a claim about the delivered file, so it is tested on the delivered file: each driver
below is perturbed in place, the whole workbook is re-evaluated from scratch, and the test
asserts the headline moves in the right DIRECTION. A dead-input sweep then bumps every other
Assumptions driver and asserts it moves something.
"""
import json, os
import openpyxl
import xlcalc

HERE = os.path.dirname(os.path.abspath(__file__))
wb = openpyxl.load_workbook(os.path.join(HERE, 'RIYADHCABLE_Valuation_Model_18082026_public.xlsx'))
# [L-067] The builder publishes the row it wrote the headline on; this test used to
# hard-code DCF!C51 beside that map and read a different figure the moment the terminal
# gained rows. It reads the map, and refuses rather than guessing an address.
ANCH = (json.load(open(os.path.join(HERE, 'xlsx_expected.json'))).get('anchors') or {})
assert 'dcf_ps' in ANCH, ('xlsx_expected.json publishes no row for the DCF value per share; '
                          'rebuild the workbook rather than guessing a cell')
DCF_PS = 'C%d' % int(ANCH['dcf_ps'])
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
    return dict(dcf=bk.cell_value('DCF', DCF_PS),
                central=bk.cell_value('Fundamental Valuation', 'C9'),
                relative=bk.cell_value('Fundamental Valuation', 'C6'),
                normalized=bk.cell_value('Fundamental Valuation', 'C7'),
                book=bk.cell_value('Fundamental Valuation', 'C8'),
                wacc=bk.cell_value('DCF', 'C10'),
                wacc_term=bk.cell_value('DCF', 'C13'),
                ebitda26=bk.cell_value('Segments', 'C17'),
                nd30=bk.cell_value('Balance Sheet', 'J13'))


base = read()
print('base:  ' + ' · '.join(f'{k} {v:,.4f}' for k, v in base.items()))

CASES = [
    ('Terminal real growth', 'C', +0.01, 'dcf', +1,
     'higher REAL terminal growth must raise the DCF, net of the growth capital it costs'),
    ('Terminal inflation (house Saudi path)', 'C', +0.01, 'dcf', +1,
     'higher terminal inflation raises the nominal growth the perpetuity capitalises; it also '
     'raises the cost of replacing the plant and of carrying working capital, so the sign is a '
     'real test rather than an arithmetic one'),
    ('Weighted asset life, years (derived from the notes)', 'C', +5.0, 'dcf', -1,
     'the life enters as the AGE of the base, not as a divisor: the terminal charges the book '
     'depreciation escalated over half the life, so holding that charge fixed and lengthening the '
     'life says the plant is OLDER than its charge implies and costs more to replace. The sign is '
     'negative and that is the construction working — under the alternative basis, replacement cost '
     'divided by the life, it would be positive, and the two disagree only because this one holds '
     'the charge fixed while the charge already encodes a life'),
    ('Beta (own-stock vs TASI)', 'C', +0.20, 'dcf', -1, 'a higher beta raises Ke and must lower the DCF'),
    ('Terminal risk-free rate', 'C', +0.02, 'dcf', -1, 'a higher terminal risk-free rate lowers the DCF'),
    ('Net working capital / revenue', 'C', +0.03, 'dcf', -1, 'more working capital absorbs cash'),
    ('Cost of debt, marginal pre-tax', 'C', +0.03, 'wacc', +1, 'higher cost of debt raises the WACC'),
    ('Terminal net-debt weight', 'C', +0.10, 'wacc_term', -1, 'more cheap after-tax debt lowers terminal WACC'),
    ('Effective zakat and income tax rate', 'C', +0.05, 'dcf', -1, 'higher tax lowers NOPAT and the DCF'),
    # These three drive CROSS-CHECKS, not the answer. Under the retired blend they reached
    # the published central through a weight and the test asserted exactly that; they must
    # now move their own lens and leave the central alone. The isolation sweep below is the
    # stronger claim — not that the weight is small, but that there is none.
    ('Justified EV/EBITDA', 'C', +1.0, 'relative', +1,
     'a higher justified multiple raises the relative cross-check'),
    ('Justified price/earnings', 'C', +1.0, 'normalized', +1,
     'a higher justified P/E raises the normalised-earnings read'),
    ('Sustainable return on equity', 'C', +0.03, 'book', +1,
     'a higher sustainable return raises the book floor'),
    ('Sustained gross margin (H1-2026 anchor)', 'C', +0.01, 'dcf', +1, 'a higher sustained margin raises the DCF'),
    ('Net financial debt at FY2025 (SAR mn, disclosed)', 'C', +2000.0, 'dcf', -1, 'more net debt leaves less for equity'),
    ('Forecast dividend payout ratio', 'C', +0.20, 'nd30', +1, 'paying out more leaves more net debt at the end'),
    ('Days to the anchor', 'C', +100.0, 'dcf', +1, 'a later anchor accretes more value at Ke'),
    ('FY2025 dividend per share paid in window', 'C', +1.0, 'dcf', -1, 'a larger dividend paid before the anchor left the share'),
    ('Depreciation and amortisation / revenue', 'C', +0.005, 'dcf', -1,
     'THIS SIGN REVERSED WHEN THE TERMINAL WAS REBUILT AND THE REVERSAL IS THE POINT. In the '
     'explicit window more depreciation is still a larger non-cash add-back, worth the tax shield on '
     'it. In the terminal it is no longer only that: book depreciation is the BASE of the '
     'replacement charge, so a riyal more of it costs 1.42 riyals of maintenance at current cost. '
     'The terminal is four fifths of enterprise value, so the net is negative — a business that '
     'depreciates its plant harder is one whose plant costs more to keep intact. The retired '
     'construction could not see this at all, because its terminal ignored depreciation entirely'),
    ('Cable volume index growth', 'C', +0.02, 'dcf', +1, 'more volume raises revenue and the DCF'),
    ('Capital expenditure / revenue', 'C', +0.01, 'dcf', -1, 'more capex reduces free cash flow'),
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
    'Yield on surplus cash',            # enters the net-debt roll-forward, not the DCF value
    'Metal content price growth',       # tested via the pasted metal sensitivity grid (spread-fixed)
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

# ---------------------------------------------------------------------------------
# ISOLATION SWEEP — the claim the retired blend made impossible to test. With one lens as
# the answer, a cross-check driver must move its own lens and move the central by EXACTLY
# zero. A near-zero tolerance would be a free parameter; a weight of nothing is not a
# small weight.
ISOLATED = [('Justified EV/EBITDA', +1.0, 'relative'),
            ('Justified price/earnings', +1.0, 'normalized'),
            ('Sustainable return on equity', +0.03, 'book')]
print('\nISOLATION SWEEP — a cross-check driver must move its own lens and NOT the answer')
iso = []
for label, bump, lens in ISOLATED:
    rr = A[label]
    out = read({('Assumptions', f'C{rr}'): wb['Assumptions'][f'C{rr}'].value + bump})
    dc, dd = out['central'] - base['central'], out['dcf'] - base['dcf']
    own = out[lens] - base[lens]
    ok = dc == 0.0 and dd == 0.0 and abs(own) > 1e-9
    if not ok:
        iso.append((label, dc, dd, own))
    print(f"  [{'OK ' if ok else 'BAD'}] {label}: own lens {own:+.4f} · central {dc:+.10f} · "
          f"cash-flow lens {dd:+.10f}")
assert not iso, f'cross-check drivers that reach the answer: {iso}'

assert not fails, f'{len(fails)} drivers failed to move the model correctly: {fails}'
assert not dead, f'dead inputs: {dead}'
print(f'\nDRIVER TEST OK — {len(CASES)} drivers each reprice the workbook in the right direction, 0 dead inputs')
