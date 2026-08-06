"""Prove the workbook is a LIVE DRIVER model — revision 2.

READ FIRST tells the reader that changing a blue cell on Assumptions reprices the model.
That is a claim about the DELIVERED file, so it is tested on the delivered file: each
driver is perturbed in place, the whole workbook is re-evaluated from scratch, and the
test asserts the headline moves in the asserted DIRECTION. A dead-input sweep bumps every
remaining driver and requires it to move something.

WHAT IS NEW IN REVISION 2. The operating line is now built bottom-up, so the PHYSICAL
cost drivers are testable for the first time: specific thermal energy, fuel price,
specific power, electricity tariff, raw materials, packaging, distribution and the fixed
block all have to move EBITDA, and EBITDA has to move the valuation. In revision 1 the
EBITDA margin was an input and none of these existed.

TWO DIRECTIONS ARE THE OPPOSITE OF THE TEXTBOOK ONE, AND NEITHER IS A BUG:
  * Higher terminal growth LOWERS the value, because terminal return on capital sits
    below the terminal cost of capital, so growth must be bought with reinvestment that
    earns less than it costs.
  * A WIDER sovereign spread RAISES the value, because the spread is netted OUT of the
    local risk-free rate before the country premium is added.
Both mechanisms were decomposed before the sign was set, not after a test failed.
"""
import json, os
import openpyxl
import xlcalc

HERE = os.path.dirname(os.path.abspath(__file__))
wb = openpyxl.load_workbook(os.path.join(HERE, 'SCEM_Valuation_Model_06082026_public.xlsx'))
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
    return dict(dcf=bk.cell_value('DCF', 'B39'),
                central=bk.cell_value('Fundamental Valuation', 'D10'),
                pv_expl=bk.cell_value('DCF', 'B30'),
                tv=bk.cell_value('DCF', 'B26'),
                ebitda26=bk.cell_value('Unit Build', 'C34'),
                ebitda25=bk.cell_value('Unit Build', 'B34'),
                ebitda25_derived=bk.cell_value('Income Statement', 'D6'),
                var_t26=bk.cell_value('Unit Build', 'C28'),
                rev26=bk.cell_value('Unit Build', 'C19'),
                cement26=bk.cell_value('Unit Build', 'C10'),
                clinker_factor=bk.cell_value('Unit Build', 'B9'),
                wacc=bk.cell_value('DCF', 'C46'),
                wacc_term=bk.cell_value('DCF', 'C53'),
                beta_term=bk.cell_value('DCF', 'C56'),
                cash30=bk.cell_value('Balance Sheet', 'I7'),
                netcash=bk.cell_value('DCF', 'B36'),
                asset_lens=bk.cell_value('Relative & Normalized', 'B38'),
                rel_lens=bk.cell_value('Relative & Normalized', 'B15'),
                norm_lens=bk.cell_value('Relative & Normalized', 'B26'),
                roic=bk.cell_value('DCF', 'B24'),
                eps23=bk.cell_value('Income Statement', 'B16'),
                ebitda23=bk.cell_value('Income Statement', 'B6'),
                ebitda24=bk.cell_value('Income Statement', 'C6'),
                ebit24=bk.cell_value('Income Statement', 'C9'),
                gain24=bk.cell_value('Income Statement', 'C11'),
                eps24=bk.cell_value('Income Statement', 'C16'),
                tax24=bk.cell_value('Income Statement', 'C13'),
                ta24=bk.cell_value('Balance Sheet', 'C8'),
                eq24=bk.cell_value('Balance Sheet', 'C12'),
                bvps=bk.cell_value('Relative & Normalized', 'B41'))


base = read()
print('base: ' + ' · '.join(f'{k} {v:,.4f}' for k, v in base.items()))

CASES = [
    # ---- THE COST STACK — testable only because EBITDA is now an output --------
    ('Specific thermal energy', 'B', +0.30, 'ebitda26', -1,
     'more heat per tonne of clinker must cost more and cut EBITDA'),
    ('Delivered fuel cost', 'B', +1.00, 'ebitda26', -1,
     'a dearer fuel must cut EBITDA'),
    ('Specific electrical energy', 'B', +10.0, 'ebitda26', -1,
     'more kWh per tonne must cut EBITDA'),
    ('Industrial electricity tariff', 'B', +0.50, 'ebitda26', -1,
     'a dearer tariff must cut EBITDA'),
    ('Raw materials & quarrying', 'B', +30.0, 'var_t26', +1,
     'a dearer raw-material bill must raise variable cost per tonne'),
    ('Packaging', 'B', +20.0, 'ebitda26', -1,
     'dearer bags must cut EBITDA'),
    ('Bagged share of despatches', 'B', +0.10, 'ebitda26', -1,
     'more bagged product carries more packaging cost'),
    ('Distribution & selling', 'B', +50.0, 'ebitda26', -1,
     'dearer freight must cut EBITDA'),
    ('Fixed cash cost', 'B', +2.00, 'ebitda26', -1,
     'a heavier fixed block must cut EBITDA'),
    ('Fixed cash cost', 'B', +2.00, 'dcf', -1,
     'and it must carry through to the valuation'),
    # ---- THE PHYSICAL BUILD -----------------------------------------------------
    ('Kiln clinker capacity', 'B', +0.30, 'cement26', +1,
     'more kiln capacity at the same utilisation must make more cement'),
    ('Clinker factor', 'B', -0.05, 'cement26', +1,
     'more blending means more cement per tonne of clinker'),
    ('Clinker factor', 'B', -0.05, 'ebitda26', +1,
     'and blending also cuts fuel per tonne of cement, so EBITDA rises'),
    ('Cement grinding capacity', 'B', +0.30, 'asset_lens', +1,
     'more capacity at the same value per tonne must raise the asset lens'),
    # ---- PRICE AND MIX ----------------------------------------------------------
    ('Kiln utilisation', 'C', +0.03, 'rev26', +1,
     'running the kiln harder must raise revenue'),
    ('Domestic realised price', 'C', +200.0, 'rev26', +1,
     'a higher domestic price must raise revenue'),
    ('Export price', 'C', +5.0, 'rev26', +1,
     'a higher export price must raise revenue'),
    ('Domestic share of despatches', 'C', +0.05, 'rev26', +1,
     'domestic realises more per tonne than export, so a heavier domestic mix lifts revenue'),
    ('Local cost inflation index', 'C', +0.10, 'ebitda26', -1,
     'inflating the EGP cost lines must cut EBITDA'),
    # ---- COST OF CAPITAL --------------------------------------------------------
    ('Terminal growth', 'B', +0.01, 'dcf', -1,
     'terminal return on capital sits BELOW the terminal cost of capital, so growth must '
     'be bought with reinvestment that earns less than it costs'),
    ('Beta', 'B', +0.20, 'dcf', -1, 'a higher beta must lower the valuation'),
    ('Beta', 'B', +0.20, 'beta_term', +1,
     'and it must re-lever through Hamada into the terminal beta'),
    ('Risk-free rate (EGP 10-year)', 'B', +0.02, 'dcf', -1,
     'a higher risk-free rate must lower the valuation'),
    ('Sovereign default spread (netted out)', 'B', +0.01, 'dcf', +1,
     'the spread is netted OUT of the risk-free rate, so a wider one LOWERS the cost of equity'),
    ('Equity risk premium (CDS basis)', 'B', +0.02, 'dcf', -1,
     'a higher premium must lower the valuation'),
    ('Terminal risk-free rate', 'B', +0.02, 'dcf', -1,
     'a higher terminal risk-free rate must lower the valuation'),
    ('Terminal equity risk premium', 'B', +0.02, 'dcf', -1,
     'a higher terminal premium must lower the valuation'),
    ('Terminal debt weight', 'B', +0.10, 'beta_term', +1,
     'more terminal leverage must RAISE the re-levered beta — the free lunch revision 1 took'),
    ('Terminal cost of debt', 'B', +0.03, 'wacc_term', +1,
     'dearer terminal debt must raise the terminal cost of capital'),
    ('Pre-tax cost of debt', 'B', +0.05, 'wacc', +1,
     'a dearer cost of debt must raise the explicit cost of capital, even if barely'),
    ('Elapsed fraction of FY2026 at valuation', 'B', +0.10, 'netcash', +1,
     'more of FY2026 already earned means more cash at the valuation date'),
    # ---- BALANCE SHEET AND BRIDGE ----------------------------------------------
    ('FY2025 cash (REPORTED)', 'B', +1000.0, 'dcf', +1,
     'more cash flows straight through the bridge'),
    ('Non-controlling interests', 'B', +500.0, 'dcf', -1,
     'minorities own part of the enterprise and must be deducted'),
    ('Gross debt', 'B', +2000.0, 'dcf', -1, 'more debt leaves less for shareholders'),
    ('Shares outstanding', 'B', +20.0, 'dcf', -1,
     'the same equity across more shares must lower the value per share'),
    ('Dividend payout ratio', 'B', +0.20, 'cash30', -1,
     'paying more out must leave less cash at the end of the forecast'),
    # ---- HISTORICAL CLOSURE -----------------------------------------------------
    ('Effective tax rate (historical closure)', 'B', +0.05, 'ebitda25_derived', +1,
     'a higher effective rate means MORE pre-tax profit stood behind the same disclosed '
     'profit after tax, so the derived FY2025 EBITDA rises'),
    ('FY2023 treasury income', 'B', +100.0, 'ebitda23', -1,
     'FY2023 EBIT is the disclosed loss LESS treasury income, so more treasury income '
     'means a worse underlying year'),
    ('FY2023 weighted-average shares', 'B', +20.0, 'eps23', +1,
     'FY2023 was a LOSS, so spreading it over more shares makes the per-share loss smaller'),
    ('FY2025 weighted-average shares', 'B', +20.0, 'bvps', -1,
     'the same book equity over more shares must lower book value per share'),
    # ---- LENSES ------------------------------------------------------------------
    ('Justified EV/EBITDA', 'B', +1.0, 'rel_lens', +1, 'a higher multiple lifts the lens'),
    ('Justified price/earnings', 'B', +1.0, 'norm_lens', +1, 'a higher multiple lifts the lens'),
    ('Justified EV per tonne', 'B', +10.0, 'asset_lens', +1, 'a higher value per tonne lifts it'),
    ('Mid-cycle EBITDA margin', 'B', +0.02, 'rel_lens', +1, 'a richer mid-cycle margin lifts it'),
    ('Normalised revenue haircut', 'B', +0.05, 'rel_lens', +1,
     'a smaller haircut leaves a bigger normalised base'),
    ('Replacement cost of capacity', 'B', +20.0, 'roic', -1,
     'more invested capital against the same terminal profit must lower the return on it'),
    ('Weight — asset', 'B', +0.05, 'central', +1,
     'the asset lens is the highest of the four, so weighting it more lifts the central'),
]

fails, rows = [], []
for label, col, bump, key, sign, why in CASES:
    r = row_of(label)
    cur = wb['Assumptions'][f'{col}{r}'].value
    out = read({('Assumptions', f'{col}{r}'): cur + bump})
    delta = out[key] - base[key]
    rel = delta / abs(base[key]) if base[key] else 0.0
    ok = (delta * sign > 0) and abs(rel) > 1e-9
    rows.append(dict(driver=label, col=col, bump=bump, headline=key, base=base[key],
                     bumped=out[key], rel=rel, direction=('up' if sign > 0 else 'down'),
                     passed=bool(ok), why=why))
    print(f"  [{'OK ' if ok else 'BAD'}] {label} [{col}] {bump:+g} -> {key} "
          f"{base[key]:,.3f} -> {out[key]:,.3f} ({rel:+.3%})")
    if not ok:
        fails.append((label, key, delta, why))

# ---- dead-input sweep --------------------------------------------------------
DEAD_OK = {
    'Spot price',                 # what fair value is COMPARED with, not an input to it
    'Vicat tender offer price',   # a disclosed reference the model deliberately consumes nowhere
}
print('\nDEAD-INPUT SWEEP — every remaining driver is bumped and must move something')
dead = []
seen = {c[0] for c in CASES}
for label, r in sorted(A.items(), key=lambda kv: kv[1]):
    if label in seen or label in DEAD_OK:
        continue
    for col in ('B', 'C', 'D', 'E', 'F', 'G'):
        cell = wb['Assumptions'][f'{col}{r}']
        if not isinstance(cell.value, (int, float)):
            continue
        out = read({('Assumptions', f'{col}{r}'): cell.value * 1.10 + 1e-6})
        if all(abs(out[k] - base[k]) < 1e-9 for k in base):
            dead.append(f'{label} [{col}{r}]')
        break
print('  inputs that changed nothing:', dead if dead else 'none — every driver reprices')

json.dump(dict(base=base, cases=rows, dead=dead, n_cases=len(CASES), n_failed=len(fails)),
          open(os.path.join(HERE, 'driver_test_result.json'), 'w'), indent=1, default=float)

assert not fails, f'{len(fails)} drivers failed: {fails}'
assert not dead, f'dead inputs: {dead}'
print(f'\nDRIVER TEST OK — {len(CASES)} drivers each reprice the workbook in the asserted '
      f'direction; 0 dead inputs')
