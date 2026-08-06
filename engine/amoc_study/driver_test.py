"""Prove the delivered workbook is a LIVE DRIVER model, not a pasted register.

READ FIRST tells the reader that changing a blue cell on Assumptions reprices the model.
That is a claim about the delivered file, so it is tested on the delivered file: each driver
below is perturbed in place, the whole workbook is re-evaluated from scratch, and the test
asserts the named headline moves in the asserted DIRECTION by a non-trivial amount. A
dead-input sweep then bumps every remaining driver and requires it to move something.

Two of the directions below are counter-intuitive and are asserted deliberately, because a
model that got them backwards would still look plausible:

  · A HIGHER COST OF DEBT RAISES the cost of capital here even though the company is net
    cash. Net debt is negative, so the debt WEIGHT is negative; and the cost of net debt is
    (cost of borrowing x debt less cash yield x cash) / (debt less cash), whose denominator
    is negative. Raising the borrowing rate therefore LOWERS the cost of net debt, and a
    negative weight on a lower rate raises the blend. Two sign flips, one result.

  · A HIGHER YIELD ON CASH LOWERS the cost of capital, by the same mechanism running the
    other way. It also raises the valuation, which is the intuitive half.

  · Depreciation pulls the two halves of the valuation in OPPOSITE directions and both legs
    are asserted, so the workbook cannot quietly lose either. In the explicit window a
    higher charge is a pure tax shield and lifts present value. In the terminal state capex
    is unchanged, so a permanently higher charge is a business consuming its own asset base.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import openpyxl
import xlcalc

wb = openpyxl.load_workbook(os.path.join(HERE, 'AMOC_Valuation_Model_06082026_public.xlsx'))
AN = json.load(open(os.path.join(HERE, 'xlsx_expected.json')))['anchors']
DC, BR, BS_, SU, RN = AN['dcf'], AN['bridge'], AN['bs'], AN['sum'], AN['rn']
FCC = AN['cols']['fcst']

A = {}
for row in wb['Assumptions'].iter_rows(min_col=1, max_col=1):
    c = row[0]
    if isinstance(c.value, str):
        A.setdefault(c.value, c.row)


def row_of(label):
    if label not in A:
        raise KeyError(f'no Assumptions row labelled {label!r}')
    return A[label]


def read(overrides=None):
    bk = xlcalc.Book(wb, overrides)
    return dict(
        dcf=bk.cell_value('EV Bridge', f"B{BR['ps']}"),
        central=bk.cell_value('Summary', f"C{SU['central']}"),
        pv_expl=bk.cell_value('DCF', f"B{DC['pv_explicit']}"),
        tv=bk.cell_value('DCF', f"B{DC['tv']}"),
        pat_cy25=bk.cell_value('Product Legs', f"B{AN['legs']['pat_cy25']}"),
        ppe25=bk.cell_value('Balance Sheet', f"E{BS_['ppe']}"),
        ev=bk.cell_value('DCF', f"B{DC['ev']}"),
        rev26=bk.cell_value('DCF', f"B{DC['rev']}"),
        ebitda26=bk.cell_value('DCF', f"B{DC['ebitda']}"),
        wacc=bk.cell_value('DCF', f"B{DC['wacc_exp']}"),
        wacc_term=bk.cell_value('DCF', f"B{DC['wacc_term']}"),
        nd30=bk.cell_value('Balance Sheet', f"{FCC[4]}{BS_['nd']}"),
        bvps=bk.cell_value('Relative & Normalized', f"B{RN['book'] - 5}"),
        nwc=bk.cell_value('Balance Sheet', f"E{BS_['nwc']}"),
        eq23=bk.cell_value('Balance Sheet', f"B{BS_['eq']}"),
        hist_ebitda=bk.cell_value('Income Statement', f"E{AN['is']['ebitda']}"),
        hist_other=bk.cell_value('Income Statement', f"E{AN['is']['other']}"),
        divyield=bk.cell_value('Summary', f"C{SU['central'] + 11}"),
    )


base = read()
print('base:  ' + ' · '.join(f'{k} {v:,.4f}' for k, v in base.items()))

# label, column, bump, headline it must move, required direction, why
CASES = [
    ('Terminal growth', 'C', +0.01, 'dcf', +1,
     'a higher terminal growth rate must raise the discounted cash flow value'),
    ('Beta', 'C', +0.20, 'dcf', -1,
     'a higher beta raises the cost of equity in both windows and must lower the value'),
    ('Terminal risk-free rate', 'C', +0.02, 'dcf', -1,
     'a higher terminal risk-free rate must lower the value'),
    ('Risk-free rate — Egypt 10-year', 'C', +0.02, 'wacc', +1,
     'a higher local risk-free rate must raise the explicit-window cost of capital'),
    ('Equity risk premium — Egypt', 'C', +0.02, 'dcf', -1,
     'a wider equity risk premium must lower the value'),
    ('Sovereign default spread', 'C', +0.01, 'wacc', -1,
     'a wider sovereign spread is NETTED OUT of the risk-free rate, so it lowers the rate'),
    ('Effective tax rate', 'C', +0.05, 'dcf', -1,
     'a higher tax rate must lower NOPAT and the value'),
    ('Receivable days', 'C', +5.0, 'dcf', -1,
     'slower collection absorbs cash into working capital and must lower the value'),
    ('Inventory days on cost of sales', 'C', +5.0, 'nwc', +1,
     'more inventory must raise net working capital'),
    ('Payable days on cost of sales', 'C', +5.0, 'dcf', +1,
     'longer payment terms fund the cycle and must raise the value'),
    ('Gross margin (forecast)', 'B', +0.005, 'ebitda26', +1,
     'a wider forecast gross margin must lift 2026E EBITDA'),
    ('Gross margin (historical)', 'E', +0.005, 'hist_ebitda', +1,
     'the base-year gross margin drives the base-year operating result'),
    ('Gross margin (historical)', 'E', +0.005, 'hist_other', -1,
     'and because disclosed profit is fixed, a wider operating margin must SHRINK the '
     'non-operating residual by exactly the same amount — the identity that keeps the '
     'reconstruction honest'),
    ('Operating cost load, % of revenue', 'B', +0.005, 'ebitda26', -1,
     'a heavier operating load must cut 2026E EBITDA'),
    ('Total volume growth', 'B', +0.02, 'rev26', +1,
     'faster throughput growth must lift 2026E revenue'),
    ('USD/EGP average rate path', 'B', +3.0, 'rev26', +1,
     'a weaker pound raises the pound value of dollar-benchmarked product and must lift revenue'),
    ('Depreciation, % of revenue', 'C', +0.005, 'pv_expl', +1,
     'in the explicit window a higher charge is a tax shield and must lift the present value'),
    ('Depreciation, % of revenue', 'C', +0.005, 'tv', -1,
     'in the terminal state, against unchanged capex, it must lower the terminal value'),
    ('Capital expenditure, % of revenue', 'B', +0.005, 'dcf', -1,
     'heavier capital spending must lower free cash flow and the value'),
    ('Justified EV / EBITDA', 'C', +1.0, 'central', +1,
     'a higher justified multiple must raise the weighted central'),
    ('Justified price / earnings', 'C', +1.0, 'central', +1,
     'a higher justified price-to-earnings must raise the weighted central'),
    ('Sustainable return on equity', 'C', +0.03, 'central', +1,
     'a higher sustainable return must raise the book lens and the central'),
    ('Cash and equivalents', 'C', +1000.0, 'dcf', +1,
     'more cash reaches the shareholder through the bridge and must raise the value'),
    ('Cost of debt', 'C', +0.03, 'wacc', +1,
     'COUNTER-INTUITIVE: a negative debt weight on a lower cost of net debt raises the blend'),
    ('Yield on cash', 'C', +0.02, 'wacc', -1,
     'COUNTER-INTUITIVE: the same mechanism in reverse lowers the blended rate'),
    ('Yield on cash', 'C', +0.02, 'dcf', +1,
     'and a lower cost of capital must raise the value'),
    ('Terminal debt weight', 'C', +0.10, 'wacc_term', -1,
     'more of the cheaper after-tax debt must lower the terminal cost of capital'),
    ('Terminal cost of debt', 'C', +0.03, 'wacc_term', +1,
     'a higher terminal borrowing rate must raise the terminal cost of capital'),
    ('Dividend payout ratio', 'C', +0.15, 'nd30', +1,
     'paying more out must leave less net cash (higher net debt) at the end of the forecast'),
    ('Total assets', 'C', +500.0, 'dcf', -1,
     'a larger residual asset base raises invested capital, lowers the terminal return and so '
     'raises the reinvestment the terminal growth requires'),
    ('Shares outstanding', 'C', +100.0, 'dcf', -1,
     'the same equity spread over more shares must be worth less per share'),
    ('Share price', 'C', +1.0, 'wacc', -1,
     'a higher market capitalisation shrinks the NEGATIVE net-debt weight toward zero, pulling '
     'the blended rate back down toward the cost of equity'),
    ('Specialty realised price', 'C', +100.0, 'rev26', +1,
     'a higher specialty realisation shifts mix into the faster-growing leg and must lift '
     'forecast revenue, even though the base year is held at the constructed total'),
    ('Specialty volume growth', 'B', +0.02, 'rev26', +1,
     'faster specialty growth must lift 2026E revenue'),
    ('Jul-Dec 2025 profit after tax', 'C', +100.0, 'pat_cy25', +1,
     'the transition half is one of the two legs of the constructed calendar-2025 base'),
    ('FY2024/25 profit after tax', 'C', +100.0, 'pat_cy25', +1,
     'the June year is the other leg of that construction'),
    ('Jul-Dec 2024 profit after tax', 'C', +100.0, 'pat_cy25', -1,
     'the prior-year half is SUBTRACTED to isolate January-June 2025, so it moves the base down'),
    ('Total liabilities', 'C', +200.0, 'bvps', -1,
     'DECOMPOSED: total liabilities does NOT touch the cash-flow lens — net working capital comes '
     'from days drivers and the asset base from total assets. What it drives is disclosed equity, '
     'and therefore book value per share and the book lens'),
    ('Total liabilities', 'C', +200.0, 'central', -1,
     'and through the book lens, the weighted central'),
    ('Dividend per share', 'C', +0.20, 'eq23', +1,
     'DECOMPOSED: closing equity is disclosed, so the dividend drives the roll-BACK, not the '
     'roll-forward. A larger dividend means more was paid out of each historical year, so opening '
     'equity three years ago must have been HIGHER, not lower'),
    ('Dividend per share', 'C', +0.20, 'divyield', +1,
     'and it raises the disclosed dividend yield'),
    ('USD/EGP spot', 'C', +2.0, 'central', 0,
     'the spot exchange rate translates the answer into dollars and must not move the pound answer'),
]

fails, rows = [], []
for label, col, bump, key, sign, why in CASES:
    r = row_of(label)
    cur = wb['Assumptions'][f'{col}{r}'].value
    out = read({('Assumptions', f'{col}{r}'): cur + bump})
    delta = out[key] - base[key]
    rel = delta / abs(base[key]) if base[key] else 0.0
    if sign == 0:
        ok = abs(rel) < 1e-12
    else:
        ok = (delta * sign > 0) and abs(rel) > 1e-6
    rows.append((label, bump, key, base[key], out[key], rel, ok, why))
    print(f"  [{'OK ' if ok else 'BAD'}] {label} {bump:+g} -> {key} {base[key]:,.4f} -> "
          f"{out[key]:,.4f} ({rel:+.3%})   {why}")
    if not ok:
        fails.append((label, key, delta, why))

# A driver that moves NOTHING anywhere is a dead input.
DEAD_OK = {
    # disclosed history that the CURRENT-year model does not consume downstream
    'FY2022/23 revenue', 'FY2022/23 gross profit', 'FY2022/23 cost of sales',
    'FY2022/23 profit after tax', 'FY2023/24 revenue — method A',
    'FY2023/24 revenue — method B', 'FY2023/24 profit after tax',
    'FY2024/25 sales volume', 'FY2024/25 oils and waxes output',
}
print('\nDEAD-INPUT SWEEP — every driver not covered above is bumped and must move something')
dead = []
covered = {c[0] for c in CASES}
for label, r in sorted(A.items(), key=lambda kv: kv[1]):
    if label in covered or label in DEAD_OK:
        continue
    for col in ('C', 'B'):
        cell = wb['Assumptions'][f'{col}{r}']
        if isinstance(cell.value, (int, float)):
            break
    else:
        continue
    out = read({('Assumptions', f'{col}{r}'): cell.value * 1.10 + 1e-6})
    if all(abs(out[k] - base[k]) < 1e-9 for k in base):
        dead.append(label)
if dead:
    print('  inputs that changed nothing:', dead)
else:
    print('  none — every remaining driver reprices the model')

json.dump([dict(driver=l, bump=b, headline=k, base=bv, bumped=ov, move=rel, ok=ok, why=w)
           for l, b, k, bv, ov, rel, ok, w in rows],
          open(os.path.join(HERE, 'driver_test_result.json'), 'w'), indent=1)

assert not fails, f'{len(fails)} drivers failed to move the model as asserted: {fails}'
assert not dead, f'dead inputs: {dead}'
print(f'\nDRIVER TEST OK — {len(CASES)} driver assertions, all in the asserted direction; '
      f'0 dead inputs')
