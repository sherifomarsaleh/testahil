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


# EVERY ONE OF THESE WAS A HARD-CODED CELL ADDRESS and the terminal rebuild moved all
# of them — the same defect [L-067] records against this file's namesake, which read a
# superseded edition and reported clean. They are read from the anchors the builder
# publishes instead, so a row that moves takes its check with it.
#
# 'central' is gone with the blend it belonged to: it pointed at Summary B9, which the
# sheet itself labels NOT AVERAGED. A driver test asserting that inputs move the number
# the study refuses is the retired construction resurrected inside the test. The answer
# is two-sided, so a driver must move BOTH branches — a stronger claim than the one it
# replaces, and the honest one.
ANCH = json.load(open(os.path.join(HERE, 'xlsx_expected.json')))['anchors']


def read(overrides=None):
    bk = xlcalc.Book(wb, overrides)
    return dict(
                branch_a=bk.cell_value('Fundamental Valuation', ANCH['fv_branch_a']),
                branch_b=bk.cell_value('Fundamental Valuation', ANCH['fv_branch_b']),
                ev_a=bk.cell_value('DCF', ANCH['dcf_ev_a']),
                pv_expl=bk.cell_value('DCF', ANCH['dcf_pve_a']),
                tv_a=bk.cell_value('DCF', ANCH['dcf_tv_a']),
                ebitda26=bk.cell_value('DCF', ANCH['dcf_ebitda26_a']),
                wacc=bk.cell_value('DCF', ANCH['dcf_wacc']),
                wacc_term=bk.cell_value('DCF', ANCH['dcf_wacc_term']),
                tax=bk.cell_value('DCF', ANCH['dcf_tax']),
                panel=bk.cell_value('Fundamental Valuation', ANCH['panel_median']),
                nd30=bk.cell_value('Balance Sheet', ANCH['bs_nd30']),
                bvps=bk.cell_value('Relative & Normalized', ANCH['book_ps']),
                # the alternative minority basis, published beside the earnings basis
                psb_a=bk.cell_value('SOTP Bridge', ANCH['bridge_psb_a']),
                # the trailing multiples that anchor the peer comparison
                ev_ebitda_t=bk.cell_value('Relative & Normalized', ANCH['rel_evebt']),
                pe_t=bk.cell_value('Relative & Normalized', ANCH['rel_pet']),
                # the two cross-checks and the terminal return, which are published
                # beside the answer and are therefore things a driver may legitimately
                # move without moving the answer
                rel_lens=bk.cell_value('Fundamental Valuation', ANCH['fv_rel']),
                norm_lens=bk.cell_value('Relative & Normalized', ANCH['norm_ps']),
                roic_term=bk.cell_value('DCF', ANCH['dcf_roic_term_a']))


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
    ('Framing A — urea benchmark, Egypt free on board ($/t)', 'C', +50.0, 'branch_a', +1,
     'a higher urea price under framing A must raise framing A'),
    ('Framing A — ammonia benchmark, Middle East ($/t)', 'C', +50.0, 'branch_a', +1,
     'a higher ammonia price under framing A must raise framing A'),
    ('Framing B — urea benchmark, Egypt free on board ($/t)', 'C', +50.0, 'branch_b', +1,
     'a higher urea price under framing B must raise framing B'),
    ('Framing B — ammonia benchmark, Middle East ($/t)', 'C', +50.0, 'branch_b', +1,
     'a higher ammonia price under framing B must raise framing B'),
    ('Third-party traded price ($/t)', 'C', +50.0, 'dcf', +1,
     'a higher traded price must raise trading revenue and the valuation'),
    ('Third-party traded volume (kt)', 'B', +100.0, 'ebitda26', +1,
     'more traded volume at a positive margin must raise EBITDA'),
    # THE TERMINAL RETURN NO LONGER ENTERS THE TERMINAL. It set the reinvestment rate of
    # the retired construction; the terminal is now built from the capital the plants
    # need to be kept whole, so this input moves the published diagnostic and nothing
    # else. Asserted on what it actually moves rather than removed, because a reader is
    # still shown it.
    ('Long-run return on capital for merchant nitrogen', 'C', +0.03, 'roic_term', +1,
     'a higher sector return must raise the triangulated terminal return it is averaged '
     'into — which is published as a diagnostic and does not enter the valuation'),
    # Replacement cost is the capital base the maintenance charge is struck on. A higher
    # replacement cost means more capital to keep whole each year at the same asset life,
    # so terminal free cash flow falls and terminal value falls with it. Under the retired
    # construction the same direction came about a different way, through the reinvestment
    # rate; the direction survived the rebuild and the mechanism did not.
    ('Replacement cost of installed capacity ($ per tonne)', 'C', +250.0, 'tv_a', -1,
     'a larger capital base costs more to keep whole, lowering terminal free cash flow'),
    ('Justified enterprise value / EBITDA', 'C', +1.0, 'rel_lens', +1,
     'a higher justified multiple must raise the relative cross-check — which sits beside '
     'the answer and is not weighted into it'),
    ('Justified price / earnings', 'C', +1.0, 'norm_lens', +1,
     'a higher justified price/earnings must raise the normalised read, which the study '
     'computes and does not publish as a lens'),
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

ANSWER = ('branch_a', 'branch_b')

fails = []
for label, col, bump, key, sign, why in CASES:
    r = row_of(label)
    cur = wb['Assumptions'][f'{col}{r}'].value
    if not isinstance(cur, (int, float)):
        raise TypeError(f'{label!r} column {col} is not a numeric input (found {cur!r})')
    out = read({('Assumptions', f'{col}{r}'): cur + bump})
    keys = ANSWER if key == 'dcf' else (key,)
    for k in keys:
        delta = out[k] - base[k]
        rel = delta / abs(base[k]) if base[k] else 0.0
        ok = (delta * sign > 0) and abs(rel) > 1e-6
        print(f'  [{"OK " if ok else "BAD"}] {label} [{col}] {bump:+g} -> {k} '
              f'{base[k]:,.3f} -> {out[k]:,.3f} ({rel:+.2%})   {why}')
        if not ok:
            fails.append((label, k, delta, why))

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

# THE FRAMINGS ARE INDEPENDENT AND THAT IS TESTED, NOT ASSUMED. Publishing two readings
# instead of one is worth nothing if a price belonging to one of them leaks into the
# other; the claim is exact — a crossed bump must move the other branch by nothing at
# all — so it is asserted at zero rather than within a tolerance.
print('\nFRAMING INDEPENDENCE — each framing\'s prices must leave the other branch untouched')
crossed = []
for lab, own, other in (('Framing A — urea benchmark, Egypt free on board ($/t)',
                         'branch_a', 'branch_b'),
                        ('Framing A — ammonia benchmark, Middle East ($/t)',
                         'branch_a', 'branch_b'),
                        ('Framing B — urea benchmark, Egypt free on board ($/t)',
                         'branch_b', 'branch_a'),
                        ('Framing B — ammonia benchmark, Middle East ($/t)',
                         'branch_b', 'branch_a')):
    rr = row_of(lab)
    out = read({('Assumptions', f'C{rr}'): wb['Assumptions'][f'C{rr}'].value + 50.0})
    leak = out[other] - base[other]
    print(f'  [{"OK " if leak == 0.0 else "BAD"}] {lab} -> {other} moved {leak:+.6f}')
    if leak != 0.0:
        crossed.append((lab, other, leak))

assert not crossed, f'framing prices leaked across branches: {crossed}'
assert not fails, f'{len(fails)} drivers failed to move the model correctly: {fails}'
assert not dead, f'dead inputs: {dead}'
print(f'\nDRIVER TEST OK — {len(CASES)} drivers each reprice the workbook in the asserted '
      f'direction, 0 dead inputs')
