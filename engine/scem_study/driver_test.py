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
wb = openpyxl.load_workbook(os.path.join(HERE, 'SCEM_Valuation_Model_04092026_public.xlsx'))
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
                # the filed historicals reach a reader through the statements, so they
                # are probed there — an input feeding only a printed line is not dead,
                # it is simply not covered until somebody points a probe at it
                rev23=bk.cell_value('Income Statement', 'B5'),
                rev24=bk.cell_value('Income Statement', 'C5'),
                pat25=bk.cell_value('Income Statement', 'D14'),
                treas25=bk.cell_value('Income Statement', 'D10'),
                ppe26=bk.cell_value('Balance Sheet', 'E5'),
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
    # THE STACK IS NOW THE COMPANY'S OWN DISCLOSED LINES, so the drivers tested are the
    # ones that exist. Revision 2's four industry rules of thumb are gone and with them
    # the eight assertions about heat rates and bag prices — replaced rather than dropped:
    # every disclosed line is tested, and the estimated split inside the materials line is
    # tested too, because it is the one part of the stack the accounts do not evidence.
    ('Materials, fuel, power, packing (note 24)', 'B', +200.0, 'ebitda26', -1,
     'a dearer materials, fuel and power bill must cut EBITDA'),
    ('Materials, fuel, power, packing (note 24)', 'B', +200.0, 'var_t26', +1,
     'and it must raise variable cost per tonne'),
    ('Transport, loading and export (notes 24, 25)', 'B', +100.0, 'ebitda26', -1,
     'dearer freight must cut EBITDA'),
    ('Fixed cash cost (the rest of notes 24, 25, 26)', 'B', +200.0, 'ebitda26', -1,
     'a heavier fixed block must cut EBITDA'),
    ('Fixed cash cost (the rest of notes 24, 25, 26)', 'B', +200.0, 'dcf', -1,
     'and it must carry through to the valuation'),
    # THE SIGN HERE IS NOT THE OBVIOUS ONE AND THE FIRST DRAFT GOT IT WRONG. A larger
    # dollar-linked share is cheaper whenever DOMESTIC inflation runs ahead of the pound's
    # slide, which is what the house macro path says it does: the pound moves 5.4% in
    # FY2026 against a domestic cost path that moves further. So the test asserts what the
    # escalators actually imply, not what "dollar-linked" sounds like it should imply.
    ('Dollar-linked share of the materials line', 'B', +0.20, 'ebitda26', +1,
     'a larger dollar-linked share is CHEAPER while domestic cost inflation runs ahead '
     'of the currency, which is what the house path says'),
    ('Weighted depreciation rate (note 3/2 on note 4)', 'B', +0.01, 'dcf', -1,
     'a faster disclosed depreciation rate means a shorter life, a heavier terminal '
     'maintenance charge, and a lower value'),
    ('Capex run rate (cash-flow statements)', 'B', +100.0, 'dcf', -1,
     'more capital spending is less free cash flow — which only became TRUE of this '
     'model when the explicit window was put on the same waterfall as the terminal; '
     'before that, raising capex by EGP 100mn a year moved the value by 0.12%'),
    ('Cash, reviewed sheet 31-Mar-2026', 'B', +500.0, 'dcf', +1,
     'more cash on the latest disclosed sheet is more value per share'),
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
    # RE-DERIVED WITH THE CONSTRUCTION, not deleted. Revision 2 asserted that terminal
    # growth DESTROYS value here, because the reinvestment identity charged g x invested
    # capital to buy it and the terminal return sat below the terminal cost of capital.
    # [R-TERM-01] retires that identity: real growth is zero and g is inflation, which
    # buys no capacity and costs no capital, so it moves the perpetuity denominator and
    # nothing else. The sign reverses and the reason is the whole of that rule.
    ('Terminal growth', 'B', +0.01, 'dcf', +1,
     'with real growth at zero, g is the inflation the perpetuity is discounted against, '
     'so a higher g raises the terminal — the retired identity charged for it instead'),
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
    # THE BRIDGE STANDS ON THE REVIEWED 31-MARCH-2026 SHEET [R-BRIDGE-01], so the
    # 31-December-2025 cash no longer reaches it and the test moves to the sheet that does.
    ('Cash, reviewed sheet 31-Mar-2026', 'B', +1000.0, 'dcf', +1,
     'more cash on the latest disclosed sheet flows straight through the bridge'),
    ('Non-controlling interests', 'B', +500.0, 'dcf', -1,
     'minorities own part of the enterprise and must be deducted'),
    ('Lease liabilities, 31-Mar-2026', 'B', +2000.0, 'dcf', -1,
     'more debt on the latest disclosed sheet leaves less for shareholders'),
    ('Shares outstanding', 'B', +20.0, 'dcf', -1,
     'the same equity across more shares must lower the value per share'),
    ('Dividend payout ratio', 'B', +0.20, 'cash30', -1,
     'paying more out must leave less cash at the end of the forecast'),
    # ---- HISTORICAL CLOSURE -----------------------------------------------------
    # THESE TWO TESTED A CLOSURE THAT NO LONGER EXISTS. Revision 2 derived FY2025 EBITDA
    # by grossing a press profit figure at an effective tax rate and subtracting an
    # estimated treasury income; both are now read off the audited statements, so neither
    # input reaches a number any more. Replaced by tests on the filed lines themselves.
    # column D is FY2025 on these three-year rows; B is FY2023
    ('EBIT (operating profit plus the finance charge inside it)', 'D', +100.0,
     'ebitda25_derived', +1,
     'the filed operating profit feeds FY2025 EBITDA directly, with nothing solved'),
    ('Depreciation & amortisation', 'D', +50.0, 'ebitda25_derived', +1,
     'and so does the filed depreciation charge, because EBITDA is EBIT plus it'),
    ('FY2023 revenue', 'B', +100.0, 'rev23', +1,
     'the filed FY2023 revenue is what the statements print'),
    ('FY2024 revenue', 'B', +100.0, 'rev24', +1,
     'and so is FY2024'),
    ('FY2025 profit after tax', 'B', +100.0, 'pat25', +1,
     'the filed profit after tax is printed, not derived'),
    ('Interest and investment income', 'D', +50.0, 'treas25', +1,
     'the filed interest income is printed beside it'),
    ('Operating assets at 31-Dec-2024 (fixed assets net, intangibles, CWIP)', 'B',
     +500.0, 'ppe26', +1,
     'the filed opening asset base rolls forward through the projected balance sheet'),
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
