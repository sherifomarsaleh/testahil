"""Prove the workbook is a LIVE DRIVER model, not a pasted register.

READ FIRST tells the reader that changing an input on Assumptions reprices the model. That is
a claim about the delivered file, so it is tested on the delivered file: each driver below is
perturbed IN PLACE, the whole workbook is re-evaluated from scratch by xlcalc, and the test
asserts the headline moves, and moves in the right DIRECTION.

A driver that fails to move the valuation means a chain is broken somewhere between the
Assumptions sheet and the answer — exactly the failure a pasted-value workbook hides. The
dead-input sweep then bumps every remaining numeric input, in every column it occupies, and
requires it to move something.

Where a direction looks surprising, the mechanism is stated next to it: the expectation is
what gets checked first, not the model.
"""
import json
import os

import openpyxl

import xlcalc

HERE = os.path.dirname(os.path.abspath(__file__))
wb = openpyxl.load_workbook(os.path.join(HERE, 'Fertiglobe_Valuation_Model_09-08-2026.xlsx'))
D = json.load(open(os.path.join(HERE, 'study_numbers.json')))

A = {}
for row in wb['Assumptions'].iter_rows(min_col=1, max_col=1):
    c = row[0]
    if isinstance(c.value, str) and c.value.strip():
        A[c.value] = c.row


def row_of(label):
    if label not in A:
        raise KeyError(f'no Assumptions row labelled {label!r}')
    return A[label]


def read(overrides=None):
    bk = xlcalc.Book(wb, overrides)
    return dict(dcf=bk.cell_value('SOTP Bridge', 'B16'),
                central=bk.cell_value('Summary', 'B9'),
                ev_a=bk.cell_value('DCF', 'C59'),
                pv_expl=bk.cell_value('DCF', 'C57'),
                tv_a=bk.cell_value('DCF', 'C56'),
                ebitda26=bk.cell_value('DCF', 'B7'),
                wacc=bk.cell_value('DCF', 'C85'),
                wacc_term=bk.cell_value('DCF', 'C88'),
                tax=bk.cell_value('DCF', 'C103'),
                panel=bk.cell_value('Fundamental Valuation', 'D26'),
                nd30=bk.cell_value('Balance Sheet', 'I22'),
                bvps=bk.cell_value('Relative & Normalized', 'C32'),
                # the alternative minority basis, published beside the earnings basis
                psb_a=bk.cell_value('SOTP Bridge', 'B21'),
                # the trailing multiples that anchor the peer comparison
                ev_ebitda_t=bk.cell_value('Relative & Normalized', 'C14'),
                pe_t=bk.cell_value('Relative & Normalized', 'C15'))


base = read()
print('base:  ' + ' · '.join(f'{k} {v:,.4f}' for k, v in base.items()))

# label, column, bump, headline it must move, required direction, the mechanism
CASES = [
    ('Terminal growth', 'C', +0.005, 'dcf', +1,
     'a higher terminal growth rate must raise the discounted cash flow'),
    ('Beta — own-stock weekly regression against the local market', 'C', +0.20, 'dcf', -1,
     'a higher beta raises the cost of equity and must lower the valuation'),
    ('Ten-year United States Treasury yield', 'C', +0.02, 'dcf', -1,
     'a higher risk-free rate must lower the valuation'),
    ('Marginal debt spread — facilities B and C', 'C', +0.02, 'wacc', +1,
     'a wider marginal debt spread must raise the cost of capital'),
    ('Terminal debt weight', 'C', +0.10, 'wacc_term', -1,
     'more of the cheaper after-tax debt must lower the terminal cost of capital'),
    ('Statutory corporate tax rate — Egypt', 'C', +0.10, 'tax', +1,
     'a higher Egyptian statutory rate must raise the jurisdiction-weighted estimate'),
    ('Income taxes paid, FY2025 ($m)', 'C', +100.0, 'tax', +1,
     'more tax actually paid must raise the aggregate cash-rate estimate'),
    ('Net debt at 30 June 2026 ($m)', 'C', +200.0, 'dcf', -1,
     'more net debt must leave less for shareholders'),
    ('Minority share of group profit', 'C', +0.05, 'dcf', -1,
     'a larger minority claim must leave less equity attributable to owners'),
    ('Ordinary shares outstanding (mn)', 'C', +500.0, 'dcf', -1,
     'the same equity spread over more shares must be worth less per share'),
    ('Capital expenditure ($m)', 'B', +50.0, 'dcf', -1,
     'more capital expenditure absorbs cash and must lower the valuation'),
    ('Third-party trading EBITDA margin', 'C', +0.02, 'dcf', +1,
     'a wider trading margin must raise cash flow and the valuation'),
    ('Corporate and other segment EBITDA ($m)', 'B', +20.0, 'ebitda26', +1,
     'a smaller central cost drag must raise FY2026 EBITDA'),
    ('Urea capacity utilisation', 'B', +0.05, 'ebitda26', +1,
     'running the urea plants harder must raise FY2026 EBITDA'),
    ('Urea production capacity (kt)', 'C', +200.0, 'dcf', +1,
     'more installed capacity at the same utilisation must raise volume and value'),
    ('Framing A — urea benchmark, Egypt free on board ($/t)', 'C', +50.0, 'dcf', +1,
     'a higher urea price must raise the valuation'),
    ('Third-party traded price ($/t)', 'C', +50.0, 'dcf', +1,
     'a higher traded price must raise trading revenue and the valuation'),
    ('Third-party traded volume (kt)', 'B', +100.0, 'ebitda26', +1,
     'more traded volume at a positive margin must raise EBITDA'),
    ('Long-run return on capital for merchant nitrogen', 'C', +0.03, 'dcf', +1,
     'a higher terminal return needs less reinvestment to fund growth, raising terminal value'),
    # Replacement cost is one of the three bases the terminal return on capital averages. A
    # higher replacement cost means the same terminal profit sits on a larger capital base, so
    # the terminal return FALLS, the reinvestment rate rises, and terminal value falls with it.
    ('Replacement cost of installed capacity ($ per tonne)', 'C', +250.0, 'tv_a', -1,
     'a larger capital base lowers the terminal return and raises the reinvestment burden'),
    ('Justified enterprise value / EBITDA', 'C', +1.0, 'central', +1,
     'a higher justified multiple must raise the relative lens and the weighted central'),
    ('Justified price / earnings', 'C', +1.0, 'central', +1,
     'a higher justified price/earnings must raise the normalised lens and the central'),
    ('Weight — discounted cash flow', 'C', +0.10, 'central', +1,
     'the cash-flow lens sits above the central, so weighting it more must raise the central'),
    ('Dividend payout ratio in the forecast', 'C', +0.15, 'nd30', +1,
     'paying more of the profit out must leave more net debt at the end of the forecast'),
    ('Interest rate charged on net debt in the forecast', 'C', +0.02, 'nd30', +1,
     'a higher interest charge must leave more net debt at the end of the forecast'),
    ('Depreciation and amortisation ($m)', 'B', +50.0, 'dcf', +1,
     'depreciation is a non-cash charge whose tax shield raises free cash flow'),
    ('Minority interests at book value ($m)', 'C', +100.0, 'psb_a', -1,
     'on the book basis a larger minority deduction must leave less per share for owners'),
    ('Adjusted EBITDA, first half 2026 ($m)', 'C', +100.0, 'ev_ebitda_t', -1,
     'more trailing EBITDA against the same enterprise value must lower the trailing multiple'),
    ('Profit to owners, first half 2026 ($m)', 'C', +50.0, 'pe_t', -1,
     'more trailing profit against the same price must lower the trailing price/earnings'),
    ('Dirhams per US dollar (Central Bank peg)', 'C', +0.10, 'dcf', +1,
     'the model values in dollars and reports in dirhams, so a weaker dirham raises the '
     'dirham-denominated answer'),
]

fails = []
for label, col, bump, key, sign, why in CASES:
    r = row_of(label)
    cur = wb['Assumptions'][f'{col}{r}'].value
    if not isinstance(cur, (int, float)):
        raise TypeError(f'{label!r} column {col} is not a numeric input (found {cur!r})')
    out = read({('Assumptions', f'{col}{r}'): cur + bump})
    delta = out[key] - base[key]
    rel = delta / abs(base[key]) if base[key] else 0.0
    ok = (delta * sign > 0) and abs(rel) > 1e-6
    print(f'  [{"OK " if ok else "BAD"}] {label} [{col}] {bump:+g} -> {key} '
          f'{base[key]:,.3f} -> {out[key]:,.3f} ({rel:+.2%})   {why}')
    if not ok:
        fails.append((label, key, delta, why))

# ---- dead-input sweep -------------------------------------------------------
# Every numeric input on the sheet, in every column it occupies, must move something.
DEAD_OK = {
    # The market price is what the valuation is COMPARED WITH, never an input to it. If
    # bumping the spot moved the fair value, the model would be marking to market.
    ('Market price (AED per share)', 'C'),
}
covered = {(label, col) for label, col, *_ in CASES}
print('\nDEAD-INPUT SWEEP — every other numeric input is bumped and must move something')
dead = []
for label, r in sorted(A.items(), key=lambda kv: kv[1]):
    for col in ('B', 'C', 'D', 'E', 'F'):
        cell = wb['Assumptions'][f'{col}{r}']
        if not isinstance(cell.value, (int, float)):
            continue          # a label row, a blank, or a derived (formula) cell
        if (label, col) in covered or (label, col) in DEAD_OK:
            continue
        out = read({('Assumptions', f'{col}{r}'): cell.value * 1.10 + 1e-6})
        if all(abs(out[k] - base[k]) < 1e-9 for k in base):
            dead.append(f'{label} [{col}]')
if dead:
    print(f'  inputs that changed nothing ({len(dead)}):')
    for d in dead:
        print('   -', d)
else:
    print('  none — every remaining driver reprices the model')

assert not fails, f'{len(fails)} drivers failed to move the model correctly: {fails}'
assert not dead, f'dead inputs: {dead}'
print(f'\nDRIVER TEST OK — {len(CASES)} drivers each reprice the workbook in the asserted '
      f'direction, 0 dead inputs')
