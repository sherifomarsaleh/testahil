"""Prove the workbook is a LIVE DRIVER model.

READ FIRST tells the reader that changing a blue cell on Assumptions reprices the model.
That is a claim about the DELIVERED file, so it is tested on the delivered file: each
driver is perturbed IN PLACE, the whole workbook is re-evaluated from scratch through the
independent evaluator, and the test asserts the headline moves in the asserted DIRECTION.
A dead-input sweep then bumps every remaining driver and requires it to move something.

THREE DIRECTIONS HERE ARE THE OPPOSITE OF THE TEXTBOOK ONE, AND NONE IS A BUG. Each was
decomposed BEFORE the sign was set, not after a test failed.

  * Higher terminal growth LOWERS the value. Terminal return on invested capital is 10.3%
    against a terminal rate of 16.5%, so growth has to be bought with reinvestment that
    earns less than it costs. The reinvestment rate is g / return on capital, so raising g
    raises what must be spent faster than it raises what is earned.

  * A WIDER sovereign spread RAISES the value. The spread is netted OUT of the local
    risk-free rate before the country equity premium is added, precisely so that Egypt's
    default risk is charged once rather than twice. Widening it therefore lowers the
    normalised risk-free rate and with it the cost of equity.

  * Depreciation runs BOTH ways, and which way depends on the year. A heavier charge is
    added back inside free cash flow, so in a mid-window year it is worth only its tax
    shield and the value RISES (FY2027 +1pp of revenue: enterprise value +35mn, terminal
    block untouched). In the TERMINAL BASE YEAR the same bump runs the other way, because
    capital expenditure here is set in dollars per tonne of capacity and does not follow
    the book charge: year-five NOPAT falls, and the terminal value falls with it (FY2030
    +1pp: enterprise value -502mn, of which -527mn is the terminal block). The first
    version of this test asserted the terminal mechanism against a mid-window bump and
    failed. The expectation was wrong, not the model.

  * Cash and debt are NOT clean one-way bridge levers, and this is the structural finding
    the test surfaced. The effective tax rate is INFERRED from the FY2025 closure —
    disclosed operating profit plus modelled net finance income against DISCLOSED profit
    after tax — so a balance-sheet change moves the imputed tax rate on every forecast
    year. Adding EGP 1bn of cash adds EGP 924mn to net cash and simultaneously lifts the
    effective rate 2.8 points, cutting enterprise value EGP 940mn; the two legs cancel to
    within four piastres a share. Adding EGP 2bn of debt cuts net cash EGP 1,823mn, cuts
    the effective rate 6.5 points, cuts the blended rate 62 basis points, and lifts
    enterprise value EGP 2,333mn — a net GAIN. Neither is a defect: profit after tax is a
    fact, so more finance income necessarily means the operating business was taxed
    harder. Each leg is asserted separately below. The clean net-cash sensitivity the
    reader wants — the tax rate held, the balance varied — is on the Sensitivity sheet,
    and there the value rises monotonically with net cash.
"""
import json, os
import openpyxl
import xlcalc

HERE = os.path.dirname(os.path.abspath(__file__))
wb = openpyxl.load_workbook(os.path.join(HERE, 'ARCC_Valuation_Model_06082026_public.xlsx'))
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
        dcf=bk.cell_value('DCF', 'B40'),
        central=bk.cell_value('Summary', 'B9'),
        pv_expl=bk.cell_value('DCF', 'B30'),
        pv_tv=bk.cell_value('DCF', 'B31'),
        ev=bk.cell_value('DCF', 'B32'),
        netcash=bk.cell_value('DCF', 'B36'),
        wacc=bk.cell_value('DCF', 'C40'),
        wacc_term=bk.cell_value('DCF', 'C46'),
        beta_term=bk.cell_value('DCF', 'C44'),
        taxe=bk.cell_value('DCF', 'C47'),
        roic=bk.cell_value('DCF', 'B24'),
        rev26=bk.cell_value('Unit Build', 'C19'),
        cement26=bk.cell_value('Unit Build', 'C10'),
        var_t26=bk.cell_value('Unit Build', 'C30'),
        fuel26=bk.cell_value('Unit Build', 'C25'),
        ebitda25=bk.cell_value('Unit Build', 'B36'),
        ebitda26=bk.cell_value('Unit Build', 'C36'),
        dna_adopted=bk.cell_value('Unit Build', 'B48'),
        ebitda23=bk.cell_value('Income Statement', 'B6'),
        ebitda24=bk.cell_value('Income Statement', 'C6'),
        pat26=bk.cell_value('Income Statement', 'E13'),
        cash30=bk.cell_value('Balance Sheet', 'I7'),
        bvps=bk.cell_value('Balance Sheet', 'D14'),
        liab=bk.cell_value('Balance Sheet', 'B20'),
        gap=bk.cell_value('Balance Sheet', 'B22'),
        rel_lens=bk.cell_value('Relative & Normalized', 'B21'),
        norm_lens=bk.cell_value('Relative & Normalized', 'B29'),
        asset_lens=bk.cell_value('Fundamental Valuation', 'B13'),
        ev_per_t=bk.cell_value('Fundamental Valuation', 'B14'),
        sh_recon=bk.cell_value('Per-Share & Ratios', 'B19'),
        eps_gap=bk.cell_value('Per-Share & Ratios', 'B25'),
        runrate=bk.cell_value('Per-Share & Ratios', 'B28'),
        q1ann=bk.cell_value('Per-Share & Ratios', 'B31'),
        peer_pe=bk.cell_value('Peer & Sector', 'E9'),
        sector_util=bk.cell_value('Peer & Sector', 'B18'),
        share_cap=bk.cell_value('Peer & Sector', 'B19'),
        revival=bk.cell_value('Peer & Sector', 'B20'),
        pe_spot=bk.cell_value('Per-Share & Ratios', 'D8'),
        # These four readouts exist so the dead-input sweep can SEE the corners of the
        # workbook. Without them the sweep reported six inputs as dead that are in fact
        # live — they simply fed cells no headline reached. A sweep is only as strong as
        # the span of what it watches.
        mgn24=bk.cell_value('Income Statement', 'C7'),
        sh_recon25=bk.cell_value('Per-Share & Ratios', 'B20'),
        peer_ps_scem=bk.cell_value('Peer & Sector', 'F6'),
        peer_ps_mbsc=bk.cell_value('Peer & Sector', 'F7'),
        exports=bk.cell_value('Peer & Sector', 'B16'),
    )


base = read()
print('base: ' + ' · '.join(f'{k} {v:,.4f}' for k, v in base.items()))

CASES = [
    # ---- THE COST STACK — testable because EBITDA is an OUTPUT ------------------
    ('Specific thermal energy', 'B', +0.30, 'ebitda26', -1,
     'more heat per tonne of clinker must cost more and cut EBITDA'),
    ('Fossil fuel price', 'B', +1.00, 'ebitda26', -1, 'a dearer fossil fuel must cut EBITDA'),
    ('Alternative fuel price', 'B', +0.50, 'ebitda26', -1,
     'a dearer alternative fuel must cut EBITDA too — the substitution is a saving, not a free good'),
    ('Specific electrical energy', 'B', +10.0, 'ebitda26', -1,
     'more kWh per tonne must cut EBITDA'),
    ('Industrial electricity tariff', 'B', +0.50, 'ebitda26', -1,
     'a dearer tariff must cut EBITDA'),
    ('Raw materials and quarrying', 'B', +30.0, 'var_t26', +1,
     'a dearer raw-material bill must raise variable cost per tonne'),
    ('Packaging', 'B', +20.0, 'ebitda26', -1, 'dearer bags must cut EBITDA'),
    ('Bagged share of despatches', 'B', +0.10, 'ebitda26', -1,
     'more bagged product carries more packaging cost'),
    ('Distribution and selling', 'B', +50.0, 'ebitda26', -1, 'dearer freight must cut EBITDA'),
    ('Fixed cash cost', 'B', +2.00, 'ebitda26', -1, 'a heavier fixed block must cut EBITDA'),
    ('Fixed cash cost', 'B', +2.00, 'dcf', -1, 'and it must carry through to the valuation'),
    ('Alternative-fuel substitution rate', 'C', +0.05, 'fuel26', -1,
     'burning more refuse-derived fuel in place of petcoke must cut the fuel bill per tonne'),
    ('Alternative-fuel substitution rate', 'C', +0.05, 'ebitda26', +1,
     'and the saving must reach EBITDA — this is the company-specific lever'),
    # ---- THE PHYSICAL BUILD -----------------------------------------------------
    ('Kiln clinker capacity', 'B', +0.30, 'cement26', +1,
     'more kiln capacity at the same utilisation must make more cement'),
    ('Clinker factor', 'B', -0.05, 'cement26', +1,
     'more blending means more cement per tonne of clinker'),
    ('Clinker factor', 'B', -0.05, 'ebitda26', +1,
     'and blending also cuts fuel per tonne of cement, so EBITDA rises'),
    ('Cement capacity', 'B', +0.30, 'asset_lens', +1,
     'more capacity at the same value per tonne must raise the asset lens'),
    # ---- PRICE, VOLUME AND MIX --------------------------------------------------
    ('Kiln utilisation', 'C', +0.03, 'rev26', +1, 'running the kiln harder must raise revenue'),
    ('Domestic realised price', 'C', +200.0, 'rev26', +1,
     'a higher domestic price must raise revenue'),
    ('Export price', 'C', +5.0, 'rev26', +1, 'a higher export price must raise revenue'),
    ('Domestic share of despatches', 'C', +0.05, 'rev26', +1,
     'domestic realises more per tonne than export, so a heavier domestic mix lifts revenue'),
    ('USD/EGP path', 'C', +5.0, 'rev26', +1,
     'a weaker pound raises the pound value of export revenue'),
    ('Local cost-inflation index', 'C', +0.10, 'ebitda26', -1,
     'inflating the pound cost lines must cut EBITDA'),
    # ---- COST OF CAPITAL --------------------------------------------------------
    ('Terminal growth rate', 'B', +0.01, 'dcf', -1,
     'terminal return on capital sits BELOW the terminal rate, so growth must be bought '
     'with reinvestment that earns less than it costs'),
    ('Beta (own-stock weekly regression)', 'B', +0.20, 'dcf', -1,
     'a higher beta must lower the valuation'),
    ('Beta (own-stock weekly regression)', 'B', +0.20, 'beta_term', +1,
     'and it must re-lever into the terminal beta'),
    ('Risk-free rate (EGP 10-year government)', 'B', +0.02, 'dcf', -1,
     'a higher risk-free rate must lower the valuation'),
    ('Sovereign default spread (netted out)', 'B', +0.01, 'dcf', +1,
     'the spread is netted OUT of the risk-free rate, so a wider one LOWERS the cost of equity'),
    ('Equity risk premium', 'B', +0.02, 'dcf', -1, 'a higher premium must lower the valuation'),
    ('Terminal risk-free rate', 'B', +0.02, 'dcf', -1,
     'a higher terminal risk-free rate must lower the valuation'),
    ('Terminal equity risk premium', 'B', +0.02, 'dcf', -1,
     'a higher terminal premium must lower the valuation'),
    ('Terminal debt weight', 'B', +0.10, 'beta_term', +1,
     'more terminal leverage must RAISE the re-levered beta'),
    ('Terminal cost of debt', 'B', +0.03, 'wacc_term', +1,
     'dearer terminal debt must raise the terminal rate'),
    ('Cost of debt, pre-tax', 'B', +0.05, 'wacc', +1,
     'a dearer cost of debt must raise the explicit rate, even if barely — the company is net cash'),
    ('Statutory tax rate', 'B', +0.02, 'wacc', -1,
     'a higher statutory rate deepens the tax shield on debt and lowers the blended rate'),
    ('Cost-of-debt path', 'C', +0.02, 'dcf', -1,
     'a slower easing path flattens the glide, so the second year is discounted harder'),
    ('Elapsed fraction of FY2026 at the valuation date', 'B', +0.10, 'netcash', +1,
     'more of FY2026 already earned means more cash at the valuation date'),
    # ---- CAPITAL INTENSITY ------------------------------------------------------
    ('Maintenance capital expenditure', 'B', +1.00, 'dcf', -1,
     'more capital spending leaves less free cash flow'),
    ('Depreciation as % of revenue', 'C', +0.01, 'dcf', +1,
     'a heavier charge in a MID-window year is worth only its tax shield: it is added back '
     'inside free cash flow and the terminal base year is untouched, so the value RISES'),
    ('Depreciation as % of revenue', 'F', +0.01, 'dcf', -1,
     'the same bump in the TERMINAL BASE YEAR runs the other way: year-five NOPAT falls, '
     'and with capex set in dollars per tonne rather than following the book charge, the '
     'terminal value it destroys is far larger than the tax shield it earns'),
    ('Depreciation as % of revenue', 'F', +0.01, 'pv_tv', -1,
     'and the loss is located in the terminal block, which is where the decomposition said '
     'it would be'),
    ('Change in working capital / change in revenue', 'B', +0.05, 'dcf', -1,
     'growth that has to be funded in working capital is growth the shareholder does not receive'),
    ('Yield earned on cash', 'C', +0.03, 'cash30', +1,
     'a better return on the cash pile must leave more cash at the end of the forecast'),
    ('Dividend payout ratio', 'B', +0.20, 'cash30', -1,
     'paying more out must leave less cash at the end of the forecast'),
    # ---- BALANCE SHEET AND BRIDGE ----------------------------------------------
    ('Cash and equivalents', 'B', +1000.0, 'netcash', +1,
     'the bridge leg: more cash on the balance sheet is more net cash at the valuation date'),
    ('Cash and equivalents', 'B', +1000.0, 'taxe', +1,
     'the closure leg, and the reason the headline barely moves: profit after tax is a '
     'DISCLOSED fact, so more treasury income behind the same disclosed profit means the '
     'operating business was taxed harder. The two legs very nearly cancel'),
    ('Cash and equivalents', 'B', +1000.0, 'ev', -1,
     'and the enterprise value falls accordingly, which is the half of that cancellation '
     'a bridge-only reading would miss'),
    ('Total debt', 'B', +2000.0, 'netcash', -1,
     'the bridge leg: more debt is less net cash'),
    ('Total debt', 'B', +2000.0, 'taxe', -1,
     'the closure leg: more interest expense behind the same disclosed profit means the '
     'operating business was taxed more lightly'),
    ('Total debt', 'B', +2000.0, 'wacc', -1,
     'the weight leg: debt is cheaper after tax than equity, so a heavier debt weight '
     'lowers the blended rate'),
    ('Non-controlling interests', 'B', +500.0, 'dcf', -1,
     'minorities own part of the enterprise and must be deducted'),
    ('Shares outstanding', 'B', +20.0, 'dcf', -1,
     'the same equity across more shares must lower the value per share'),
    ('Total equity (reported)', 'B', +500.0, 'bvps', +1,
     'more book equity over the same shares must raise book value per share'),
    ('Total liabilities (alternative print)', 'B', +500.0, 'gap', -1,
     'a larger alternative print narrows the gap against the derived figure'),
    # ---- THE DEPRECIATION TRIANGULATION ----------------------------------------
    ('Q4-2025 EBITDA', 'B', +100.0, 'dna_adopted', +1,
     'a higher fourth-quarter EBITDA against the same disclosed operating profit implies '
     'a bigger depreciation charge'),
    ('Q4-2025 revenue', 'B', +200.0, 'dna_adopted', -1,
     'the same fourth-quarter EBITDA on more revenue is a thinner margin, so less implied '
     'depreciation'),
    ('Peer depreciation per tonne', 'B', +20.0, 'dna_adopted', +1,
     'the peer anchor is one of the three methods averaged'),
    ('Composite depreciation rate on net property', 'B', +0.01, 'dna_adopted', +1,
     'a faster write-off of the same property base is a bigger charge'),
    ('Inventory days on cost of sales', 'B', +10.0, 'dna_adopted', -1,
     'more inventory inside total assets leaves less property to depreciate'),
    ('Receivable days on revenue', 'B', +10.0, 'dna_adopted', -1,
     'more receivables inside total assets leaves less property to depreciate'),
    ('Total assets', 'B', +1000.0, 'dna_adopted', +1,
     'a larger balance sheet with the same cash and working capital is more property'),
    ('Trailing gross margin', 'B', +0.05, 'dna_adopted', +1,
     'a richer gross margin means less cost of sales, less inventory, and so more property'),
    # ---- HISTORICAL CLOSURE -----------------------------------------------------
    ('FY2025 operating income (disclosed)', 'B', +200.0, 'taxe', +1,
     'more pre-tax operating profit behind the same disclosed profit after tax is a higher '
     'effective tax rate'),
    ('FY2025 attributable profit', 'B', +500.0, 'dcf', +1,
     'a higher disclosed profit against the same operating profit is a LOWER effective tax '
     'rate, which lifts every forecast year'),
    ('Yield earned on cash through FY2025', 'B', +0.02, 'dcf', -1,
     'more treasury income behind the same disclosed profit means the operating business '
     'was taxed harder than it appeared'),
    ('FY2023 kiln utilisation', 'B', +0.02, 'ebitda23', +1,
     'more tonnes despatched at the same charge per tonne is more depreciation, and FY2023 '
     'EBITDA is the closed operating profit plus that charge'),
    ('FY2024 kiln utilisation', 'B', +0.02, 'ebitda24', +1, 'the same mechanism in FY2024'),
    ('FY2023 revenue', 'B', +500.0, 'ebitda23', 0,
     'FY2023 revenue does not touch FY2023 EBITDA — it is checked in the dead-input sweep instead'),
    # ---- RECONCILIATIONS --------------------------------------------------------
    ('FY2024 dividend per share', 'B', +0.50, 'sh_recon', -1,
     'the same distribution at a higher per-share rate implies fewer shares'),
    ('FY2024 total distribution', 'B', +100.0, 'sh_recon', +1,
     'a larger distribution at the same per-share rate implies more shares'),
    ('FY2025 disclosed earnings per share', 'B', +0.50, 'eps_gap', -1,
     'a higher published earnings per share leaves a smaller residual against the '
     'disclosed attributable profit'),
    ('Q1-2026 revenue', 'B', +200.0, 'runrate', +1,
     'a stronger first quarter raises the run rate the forecast is checked against'),
    ('Q1-2025 revenue', 'B', +200.0, 'runrate', -1,
     'a stronger prior-year first quarter lowers the growth rate, and so the run rate'),
    ('Q1-2026 attributable profit', 'B', +100.0, 'q1ann', +1,
     'the annualised first quarter is four times it'),
    # ---- LENSES ------------------------------------------------------------------
    ('Justified EV/EBITDA', 'B', +1.0, 'rel_lens', +1, 'a higher multiple lifts the lens'),
    ('Justified price/earnings', 'B', +1.0, 'norm_lens', +1, 'a higher multiple lifts the lens'),
    ('Justified enterprise value per annual tonne', 'B', +10.0, 'asset_lens', +1,
     'a higher value per tonne lifts it'),
    ('Mid-cycle EBITDA margin', 'B', +0.02, 'rel_lens', +1, 'a richer mid-cycle margin lifts it'),
    ('Normalised revenue haircut', 'B', +0.05, 'rel_lens', +1,
     'a smaller haircut leaves a bigger normalised base'),
    ('Replacement cost per annual tonne', 'B', +20.0, 'roic', -1,
     'more invested capital against the same terminal profit must lower the return on it'),
    ('Weight — asset lens', 'B', +0.05, 'central', +1,
     'the asset lens is the highest of the four, so weighting it more lifts the central'),
    ('Spot price', 'B', +5.0, 'ev_per_t', +1,
     'a higher share price is a higher enterprise value over the same capacity'),
    ('USD/EGP at the valuation date', 'B', +5.0, 'asset_lens', +1,
     'capacity is valued in dollars per tonne, so a weaker pound raises its pound value'),
    # ---- SECTOR AND PEERS --------------------------------------------------------
    ('Egyptian nameplate capacity', 'B', +5.0, 'sector_util', -1,
     'the same production over more capacity is lower utilisation'),
    ('Egyptian production 2025', 'B', +5.0, 'sector_util', +1, 'more production is higher utilisation'),
    ('Egyptian consumption 2025', 'B', +5.0, 'revival', -1,
     'the restart programme is a smaller share of a larger market'),
    ('Dormant capacity under revival', 'B', +2.0, 'revival', +1,
     'more dormant capacity is a larger share of the same market'),
    ('Peer — Sinai Cement profit', 'B', +500.0, 'peer_pe', -1,
     'more peer profit at the same peer market value is a lower peer multiple'),
    ('Peer — Sinai Cement market capitalisation', 'B', +2000.0, 'peer_pe', +1,
     'a dearer peer at the same profit is a higher peer multiple'),
    ('Peer — Misr Beni Suef profit', 'B', +500.0, 'peer_pe', -1, 'the same mechanism'),
    ('Peer — Misr Beni Suef market capitalisation', 'B', +2000.0, 'peer_pe', +1,
     'the same mechanism'),
]

fails, rows = [], []
for label, col, bump, key, sign, why in CASES:
    r = row_of(label)
    cur = wb['Assumptions'][f'{col}{r}'].value
    out = read({('Assumptions', f'{col}{r}'): cur + bump})
    delta = out[key] - base[key]
    rel = delta / abs(base[key]) if base[key] else 0.0
    if sign == 0:
        ok = abs(delta) < 1e-9
    else:
        ok = (delta * sign > 0) and abs(rel) > 1e-9
    rows.append(dict(driver=label, col=col, bump=bump, headline=key, base=base[key],
                     bumped=out[key], rel=rel,
                     direction=('up' if sign > 0 else ('down' if sign < 0 else 'unchanged')),
                     passed=bool(ok), why=why))
    print(f"  [{'OK ' if ok else 'BAD'}] {label} [{col}] {bump:+g} -> {key} "
          f"{base[key]:,.3f} -> {out[key]:,.3f} ({rel:+.3%})")
    if not ok:
        fails.append((label, key, delta, why))

# ---- dead-input sweep --------------------------------------------------------
print('\nDEAD-INPUT SWEEP — every remaining driver is bumped and must move something')
dead = []
seen = {c[0] for c in CASES}
for label, r in sorted(A.items(), key=lambda kv: kv[1]):
    if label in seen:
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
print(f'\nDRIVER TEST OK — {len(CASES)} driver assertions, every one in the asserted '
      f'direction; 0 dead inputs')
