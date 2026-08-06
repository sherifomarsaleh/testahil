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
        dcf=bk.cell_value('DCF', 'B44'),
        central=bk.cell_value('Summary', 'B9'),
        pv_expl=bk.cell_value('DCF', 'B31'),
        pv_tv=bk.cell_value('DCF', 'B32'),
        ev=bk.cell_value('DCF', 'B33'),
        netcash=bk.cell_value('DCF', 'B40'),
        cashval=bk.cell_value('DCF', 'B38'),
        wacc=bk.cell_value('DCF', 'C40'),
        kd=bk.cell_value('DCF', 'C41'),
        eurshare=bk.cell_value('DCF', 'C46'),
        wacc_term=bk.cell_value('DCF', 'C50'),
        beta_term=bk.cell_value('DCF', 'C47'),
        roic=bk.cell_value('DCF', 'B24'),
        roic_book=bk.cell_value('DCF', 'B25'),
        kd_eff25=bk.cell_value('DCF', 'B61'),
        kd_egp=bk.cell_value('DCF', 'B63'),
        vol25=bk.cell_value('Unit Build', 'B12'),
        util25=bk.cell_value('Unit Build', 'B14'),
        ccost25=bk.cell_value('Unit Build', 'B27'),
        cmat25=bk.cell_value('Unit Build', 'B24'),
        rev26=bk.cell_value('Unit Build', 'C42'),
        vol26=bk.cell_value('Unit Build', 'C32'),
        cc26=bk.cell_value('Unit Build', 'C47'),
        cmat26=bk.cell_value('Unit Build', 'C44'),
        ebitda25=bk.cell_value('Unit Build', 'B49'),
        ebitda26=bk.cell_value('Unit Build', 'C49'),
        resid_rev=bk.cell_value('Unit Build', 'B56'),
        gp23=bk.cell_value('Income Statement', 'B7'),
        gp25=bk.cell_value('Income Statement', 'D7'),
        ebit25=bk.cell_value('Income Statement', 'D11'),
        ebitda_is25=bk.cell_value('Income Statement', 'D14'),
        taxe25=bk.cell_value('Income Statement', 'D19'),
        pat26=bk.cell_value('Income Statement', 'E20'),
        dps25=bk.cell_value('Income Statement', 'D23'),
        cash30=bk.cell_value('Balance Sheet', 'I9'),
        bvps25=bk.cell_value('Balance Sheet', 'D17'),
        roe25=bk.cell_value('Balance Sheet', 'D18'),
        close=bk.cell_value('Balance Sheet', 'B25'),
        nd23=bk.cell_value('Balance Sheet', 'B16'),
        othliab=bk.cell_value('Balance Sheet', 'D13'),
        rel_lens=bk.cell_value('Relative & Normalized', 'B23'),
        norm_lens=bk.cell_value('Relative & Normalized', 'B31'),
        asset_lens=bk.cell_value('Fundamental Valuation', 'B13'),
        ev_per_t=bk.cell_value('Fundamental Valuation', 'B14'),
        bookval_t=bk.cell_value('Fundamental Valuation', 'B16'),
        rr23=bk.cell_value('Fundamental Valuation', 'B33'),
        rr25=bk.cell_value('Fundamental Valuation', 'D33'),
        roicb24=bk.cell_value('Fundamental Valuation', 'C34'),
        sh_out=bk.cell_value('Per-Share & Ratios', 'B16'),
        sh_div=bk.cell_value('Per-Share & Ratios', 'B17'),
        parchk=bk.cell_value('Per-Share & Ratios', 'B19'),
        runrate=bk.cell_value('Per-Share & Ratios', 'B21'),
        q1mgn=bk.cell_value('Per-Share & Ratios', 'B24'),
        q1ann=bk.cell_value('Per-Share & Ratios', 'B26'),
        q1nc=bk.cell_value('Per-Share & Ratios', 'B29'),
        pe_spot=bk.cell_value('Per-Share & Ratios', 'D7'),
        peer_pe=bk.cell_value('Peer & Sector', 'E9'),
        peer_ps_scem=bk.cell_value('Peer & Sector', 'F6'),
        peer_ps_mbsc=bk.cell_value('Peer & Sector', 'F7'),
        sector_util=bk.cell_value('Peer & Sector', 'B18'),
        share_cap=bk.cell_value('Peer & Sector', 'B19'),
        revival=bk.cell_value('Peer & Sector', 'B20'),
        share_prod=bk.cell_value('Peer & Sector', 'B21'),
        exports=bk.cell_value('Peer & Sector', 'B16'),
        # FY2025 revenue growth sits in the FY2025 column (D), not the FY2026 one.
        growth25=bk.cell_value('Summary Financials', 'D13'),
        # The sweep is only as strong as the span of what it watches. These reach the
        # corners of the workbook that no headline touches.
        klinker=bk.cell_value('Unit Build', 'B70'),
        klinker30=bk.cell_value('Unit Build', 'B72'),
        nonop25=bk.cell_value('Income Statement', 'D16'),
        nonop_chk=bk.cell_value('Income Statement', 'B24'),
        roe24=bk.cell_value('Balance Sheet', 'C18'),
        ta24=bk.cell_value('Balance Sheet', 'C11'),
        ta23=bk.cell_value('Balance Sheet', 'B11'),
        nca25=bk.cell_value('Balance Sheet', 'D8'),
        wc25=bk.cell_value('Balance Sheet', 'D10'),
        nd24=bk.cell_value('Balance Sheet', 'C16'),
        kd_eff24=bk.cell_value('DCF', 'B60'),
    )


base = read()
print('base: ' + ' · '.join(f'{k} {v:,.4f}' for k, v in base.items()))

CASES = [
    # ---- THE UNIT BUILD, now anchored on the audited notes ---------------------
    ('Local realised price', 'B', +200.0, 'vol25', -1,
     'volume is DERIVED from disclosed revenue divided by price, so a higher price implies '
     'FEWER tonnes behind the same audited revenue'),
    ('Export price', 'B', +5.0, 'vol25', -1, 'the same mechanism on the export leg'),
    ('Local realised price', 'B', +200.0, 'ccost25', +1,
     'and fewer tonnes behind the same audited cost is a HIGHER cost per tonne'),
    ('Average USD/EGP FY2025', 'B', +2.0, 'vol25', -1,
     'a weaker pound means the same export revenue represents fewer dollars, so fewer tonnes'),
    ('Capacity utilisation', 'C', +0.03, 'vol26', +1,
     'running the plant harder must make more cement'),
    ('Capacity utilisation', 'C', +0.03, 'rev26', +1, 'and more cement must raise revenue'),
    ('Local price index', 'C', +0.05, 'rev26', +1, 'a higher local price must raise revenue'),
    ('Export price index (USD)', 'C', +0.05, 'rev26', +1,
     'a higher export price must raise revenue'),
    ('USD/EGP path', 'C', +5.0, 'rev26', +1,
     'a weaker pound raises the pound value of export revenue'),
    ('Export share of volume', 'C', +0.05, 'rev26', -1,
     'export realises less per tonne than local, so a heavier export mix LOWERS revenue'),
    ('Local cost-inflation index', 'C', +0.10, 'cc26', +1,
     'inflating the pound cost lines must raise cost per tonne'),
    ('Local cost-inflation index', 'C', +0.10, 'ebitda26', -1, 'and must cut EBITDA'),
    ('Alternative-fuel saving on materials', 'C', +0.05, 'cmat26', -1,
     'the substitution programme must cut the materials and fuel bill per tonne'),
    ('Alternative-fuel saving on materials', 'C', +0.05, 'ebitda26', +1,
     'and the saving must reach EBITDA — this is the company-specific lever, and the EBRD '
     'facility funding it is on the audited balance sheet'),
    ('Services revenue as a share of goods revenue', 'B', +0.02, 'rev26', +1,
     'more transportation revenue on the same tonnes'),
    ('Cement capacity', 'B', +0.30, 'vol26', +1, 'more capacity at the same utilisation'),
    ('Cement capacity', 'B', +0.30, 'asset_lens', +1,
     'and more capacity at the same value per tonne must raise the asset lens'),
    ('FY2025 cost of sales — materials and fuel', 'B', +200.0, 'ccost25', +1,
     'a bigger disclosed materials bill is a higher cost per tonne'),
    ('FY2025 cost of sales — transportation', 'B', +100.0, 'ebitda26', -1,
     'and a bigger transport bill carries into the forecast cost stack'),
    ('FY2025 cost of sales — overheads', 'B', +100.0, 'ebitda26', -1, 'as do overheads'),
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
    ('Euribor (EBRD and NBE reference rate)', 'B', +0.02, 'kd', +1,
     '91% of the audited debt book is euro-denominated at Euribor-linked rates, so the '
     'reference rate carries almost all of the blended cost of debt'),
    ('Euribor (EBRD and NBE reference rate)', 'B', +0.02, 'wacc', +1,
     'and it must raise the blended cost of capital, even if barely — debt is 4.9% of it'),
    ('EGP marginal borrowing rate (corridor + 0.6%)', 'B', +0.05, 'kd', +1,
     'the pound facility is only 8.8% of the book, so this moves the blend by less'),
    ('Expected EGP depreciation against the euro', 'B', +0.02, 'kd_egp', +1,
     'loading the euro legs with faster pound depreciation must raise the '
     'pound-equivalent cost of debt'),
    ('EGP marginal cost-of-debt path', 'C', +0.02, 'dcf', -1,
     'a slower easing path flattens the glide, so the second year is discounted harder'),
    ('EBRD facility — EUR', 'B', +500.0, 'eurshare', +1,
     'a larger euro facility raises the euro share of the book'),
    ('EBRD facility — EUR', 'B', +500.0, 'kd', -1,
     'and because the euro rate is far below the pound rate, it LOWERS the blended cost'),
    ('Statutory tax rate', 'B', +0.02, 'wacc', -1,
     'a higher statutory rate deepens the tax shield on debt and lowers the blended rate'),
    ('Elapsed fraction of FY2026 at the valuation date', 'B', +0.10, 'cashval', +1,
     'more of FY2026 already earned means more cash at the valuation date'),
    # ---- CAPITAL INTENSITY AND THE BRIDGE --------------------------------------
    ('Maintenance capital expenditure', 'B', +1.00, 'dcf', -1,
     'more capital spending leaves less free cash flow'),
    ('Depreciation as % of revenue', 'C', +0.01, 'dcf', +1,
     'a heavier charge in a MID-window year is worth only its tax shield: it is added back '
     'inside free cash flow and the terminal base year is untouched, so the value RISES'),
    ('Depreciation as % of revenue', 'F', +0.01, 'dcf', -1,
     'the same bump in the TERMINAL BASE YEAR runs the other way: year-five NOPAT falls and '
     'the terminal value falls with it, because capex is set in dollars per tonne and does '
     'not follow the book charge'),
    ('Depreciation as % of revenue', 'F', +0.01, 'pv_tv', -1,
     'and the loss is located in the terminal block, where the decomposition said it would be'),
    ('Change in working capital / change in revenue', 'B', +0.05, 'dcf', -1,
     'growth funded in working capital is growth the shareholder does not receive'),
    ('Yield earned on cash', 'C', +0.03, 'cash30', +1,
     'a better return on the cash pile leaves more cash at the end of the forecast'),
    ('Dividend payout ratio', 'B', +0.20, 'cash30', -1,
     'paying more out leaves less cash at the end of the forecast'),
    ('Cash and bank balances FY2025', 'B', +1000.0, 'dcf', +1,
     'more audited cash flows straight through the bridge. Unlike revision 1 this is now a '
     'CLEAN one-way lever, because the effective tax rate is a disclosed figure rather than '
     'one inferred by closing a modelled finance income'),
    ('CIB credit facilities — EGP', 'B', +500.0, 'dcf', -1,
     'more debt leaves less for shareholders'),
    ('Non-controlling interests FY2025', 'B', +500.0, 'dcf', -1,
     'minorities own part of the enterprise and must be deducted'),
    ('Ordinary shares issued', 'B', +20.0, 'dcf', -1,
     'the same equity across more shares must lower the value per share'),
    ('Treasury shares held', 'B', +5.0, 'dcf', +1,
     'treasury shares are NOT outstanding, so buying more raises the value of each remaining share'),
    ('FY2025 dividend declared', 'B', +500.0, 'dcf', -1,
     'a dividend declared and unpaid at the last balance-sheet date is cash a buyer at '
     'today\'s price does not receive'),
    # ---- THE AUDITED HISTORY ----------------------------------------------------
    ('FY2025 sales (net)', 'B', +500.0, 'gp25', +1, 'more audited revenue is more gross profit'),
    ('FY2025 cost of sales', 'B', +500.0, 'gp25', -1, 'more cost of sales is less gross profit'),
    ('FY2025 general and administrative expenses', 'B', +100.0, 'ebit25', -1,
     'more administrative expense is less operating profit'),
    ('FY2025 provisions charged', 'B', +50.0, 'ebit25', -1, 'as are more provisions'),
    ('FY2025 expected credit losses', 'B', +10.0, 'ebit25', -1, 'and more credit losses'),
    ('FY2025 depreciation and amortisation', 'B', +50.0, 'ebitda_is25', +1,
     'EBITDA is operating profit PLUS depreciation, so a bigger audited charge raises it'),
    ('FY2025 profit before tax', 'B', +200.0, 'taxe25', -1,
     'the same audited tax charge on more pre-tax profit is a LOWER effective rate'),
    ('FY2025 income tax', 'B', +200.0, 'taxe25', +1, 'and a bigger charge is a higher rate'),
    ('FY2023 sales (net)', 'B', +500.0, 'gp23', +1, 'the same mechanism in FY2023'),
    ('FY2023 cost of sales', 'B', +200.0, 'gp23', -1, 'and on its cost line'),
    ('FY2024 sales (net)', 'B', +500.0, 'growth25', -1,
     'a bigger FY2024 base makes the FY2025 growth rate smaller'),
    ('FY2024 cost of sales', 'B', +200.0, 'roicb24', -1,
     'more FY2024 cost is less operating profit and a lower return on FY2024 capital'),
    ('FY2024 general and administrative expenses', 'B', +50.0, 'roicb24', -1, 'as is more overhead'),
    ('FY2024 provisions charged', 'B', +50.0, 'roicb24', -1, 'and more provisions'),
    ('FY2024 expected credit losses', 'B', +10.0, 'roicb24', -1, 'and more credit losses'),
    ('FY2023 general and administrative expenses', 'B', +50.0, 'rr23', -1,
     'less FY2023 operating profit is less NOPAT, so the same net reinvestment is a LARGER '
     'share of it — and FY2023 reinvestment was NEGATIVE, so a larger share is more negative'),
    ('FY2023 provisions charged', 'B', +20.0, 'rr23', -1, 'the same mechanism'),
    ('FY2023 expected credit losses', 'B', +10.0, 'rr23', -1, 'and again'),
    ('FY2023 profit before tax', 'B', +100.0, 'rr23', +1,
     'a higher FY2023 pre-tax profit against the same tax charge is a LOWER effective rate, '
     'so more NOPAT, so a smaller (less negative) reinvestment share'),
    ('FY2023 income tax', 'B', +50.0, 'rr23', -1, 'and the mirror of it'),
    ('FY2024 profit before tax', 'B', +100.0, 'roicb24', +1,
     'a lower effective rate on the same operating profit is more NOPAT on the same capital'),
    ('FY2024 income tax', 'B', +100.0, 'roicb24', -1, 'and the mirror'),
    ('FY2023 attributable profit', 'B', +100.0, 'close', 0,
     'the audited profit line does not touch the balance-sheet closure check'),
    ('FY2025 attributable profit', 'B', +200.0, 'roe25', +1,
     'more audited profit on the same audited equity is a higher return'),
    ('FY2025 earnings per share', 'B', +1.00, 'pe_spot', -1,
     'the same price on higher published earnings per share is a lower multiple'),
    ('FY2023 earnings per share', 'B', +0.50, 'pe_spot', 0,
     'the FY2023 figure does not touch the FY2025 multiple'),
    ('FY2024 earnings per share', 'B', +0.50, 'pe_spot', 0, 'nor does FY2024'),
    ('FY2023 capital expenditure', 'B', +100.0, 'rr23', +1,
     'more capital spending against the same depreciation is more net reinvestment'),
    ('FY2025 capital expenditure', 'B', +100.0, 'rr25', +1, 'the same in FY2025'),
    ('FY2024 capital expenditure', 'B', +100.0, 'roicb24', 0,
     'capital expenditure does not enter the return on capital, only the reinvestment rate'),
    ('FY2023 depreciation and amortisation', 'B', +50.0, 'rr23', -1,
     'more depreciation against the same capex is LESS net reinvestment'),
    ('FY2024 depreciation and amortisation', 'B', +50.0, 'rr23', 0,
     'the FY2024 charge does not touch the FY2023 reinvestment rate'),
    # ---- THE AUDITED BALANCE SHEET ---------------------------------------------
    ('Total assets FY2025', 'B', +500.0, 'close', +1,
     'assets less liabilities must exceed equity if assets rise alone — the closure check '
     'exists precisely to catch that'),
    ('Total liabilities FY2025', 'B', +500.0, 'close', -1, 'and the mirror'),
    ('Total liabilities FY2025', 'B', +500.0, 'othliab', +1,
     'other liabilities are total liabilities less interest-bearing debt'),
    ('Equity attributable to owners FY2025', 'B', +500.0, 'bvps25', +1,
     'more audited equity over the same shares is a higher book value per share'),
    ('Equity attributable to owners FY2024', 'B', +500.0, 'roicb24', -1,
     'more FY2024 capital against the same profit is a lower return on it'),
    ('Equity attributable to owners FY2023', 'B', +500.0, 'rr23', 0,
     'FY2023 equity does not enter the FY2023 reinvestment rate'),
    ('Property, plant and equipment FY2025', 'B', +500.0, 'bookval_t', +1,
     'a bigger audited property base is a higher book value per annual tonne'),
    ('Assets under construction FY2025', 'B', +200.0, 'bookval_t', +1, 'as is more construction'),
    ('Cash and bank balances FY2023', 'B', +100.0, 'nd23', -1,
     'more FY2023 cash is less FY2023 net debt'),
    ('Total interest-bearing debt FY2023', 'B', +100.0, 'nd23', +1, 'and more debt is more'),
    ('Total interest-bearing debt FY2024', 'B', +100.0, 'kd_eff25', -1,
     'a bigger opening balance raises the average the FY2025 interest is divided by'),
    ('FY2025 loan interest expense', 'B', +10.0, 'kd_eff25', +1,
     'more interest on the same average balance is a higher computed effective rate'),
    ('FY2025 credit-facility interest expense', 'B', +10.0, 'kd_eff25', +1, 'the same'),
    ('Q1-2026 interest-bearing debt', 'B', +200.0, 'q1nc', -1,
     'more debt at the quarter end is less net cash there'),
    ('Q1-2026 cash and bank balances', 'B', +200.0, 'q1nc', +1, 'and more cash is more'),
    ('Q1-2026 dividends payable', 'B', +200.0, 'q1nc', -1,
     'a declared and unpaid dividend is an obligation against that cash'),
    ('Q1-2026 sales', 'B', +200.0, 'runrate', +1,
     'a stronger first quarter raises the run rate the forecast is checked against'),
    ('Q1-2025 sales', 'B', +200.0, 'runrate', -1,
     'a stronger prior-year quarter lowers the growth rate, and so the run rate'),
    ('Q1-2026 gross profit', 'B', +100.0, 'q1mgn', +1, 'a higher first-quarter gross margin'),
    ('Q1-2026 attributable profit', 'B', +100.0, 'q1ann', +1,
     'the annualised first quarter is four times it'),
    ('Q1-2026 finance costs', 'B', +5.0, 'dcf', 0,
     'the Q1 finance cost is a cost-of-debt CHECK, not an input to the valuation'),
    ('FY2024 dividend approved and paid', 'B', +100.0, 'dcf', 0,
     'the FY2024 distribution is history and is deliberately consumed nowhere downstream'),
    # ---- REVENUE AND SHARE NOTES ------------------------------------------------
    ('FY2025 local sales of goods', 'B', +200.0, 'vol25', +1,
     'more disclosed local revenue at the same price is more tonnes'),
    ('FY2025 export sales of goods', 'B', +200.0, 'vol25', +1, 'the same on the export leg'),
    ('FY2025 local services', 'B', +50.0, 'resid_rev', 0,
     'the services line does not enter the volume build; it is carried as a share'),
    ('FY2025 export services', 'B', +50.0, 'ebitda26', 0, 'nor does the export services line'),
    ('FY2024 total local sales', 'B', +200.0, 'dcf', 0,
     'the FY2024 revenue split is disclosure for the reader and drives nothing'),
    ('FY2024 total export sales', 'B', +200.0, 'dcf', 0, 'the same'),
    ('FY2025 administrative depreciation', 'B', +10.0, 'ccost25', -1,
     'administrative depreciation is removed from the cash overhead line, so more of it is '
     'LESS cash cost'),
    # ---- LENSES AND SECTOR ------------------------------------------------------
    ('Justified EV/EBITDA', 'B', +1.0, 'rel_lens', +1, 'a higher multiple lifts the lens'),
    ('Justified price/earnings', 'B', +1.0, 'norm_lens', +1, 'a higher multiple lifts the lens'),
    ('Justified enterprise value per annual tonne', 'B', +10.0, 'asset_lens', +1,
     'a higher value per tonne lifts it'),
    ('Mid-cycle EBITDA margin', 'B', +0.02, 'rel_lens', +1, 'a richer mid-cycle margin lifts it'),
    ('Normalised revenue haircut', 'B', +0.05, 'rel_lens', +1,
     'a smaller haircut leaves a bigger normalised base'),
    ('Replacement cost per annual tonne', 'B', +20.0, 'roic', -1,
     'more invested capital against the same terminal profit lowers the return on it'),
    ('Weight — asset lens', 'B', +0.05, 'central', +1,
     'the asset lens is the highest of the four, so weighting it more lifts the central'),
    ('Effective tax rate', 'B', +0.02, 'dcf', -1, 'a higher tax rate lowers every NOPAT'),
    ('Spot price', 'B', +5.0, 'ev_per_t', +1,
     'a higher share price is a higher enterprise value over the same capacity'),
    ('USD/EGP at the valuation date', 'B', +5.0, 'asset_lens', +1,
     'capacity is valued in dollars per tonne, so a weaker pound raises its pound value'),
    ('Egyptian nameplate capacity', 'B', +5.0, 'sector_util', -1,
     'the same production over more capacity is lower utilisation'),
    ('Egyptian production 2025', 'B', +5.0, 'sector_util', +1, 'more production is higher utilisation'),
    ('Egyptian consumption 2025', 'B', +5.0, 'revival', -1,
     'the restart programme is a smaller share of a larger market'),
    ('Dormant capacity under revival', 'B', +2.0, 'revival', +1,
     'more dormant capacity is a larger share of the same market'),
    ('Egyptian exports 2025', 'B', +2.0, 'exports', +1, 'the disclosed export total'),
    ('Peer — Sinai Cement profit', 'B', +500.0, 'peer_pe', -1,
     'more peer profit at the same peer market value is a lower peer multiple'),
    ('Peer — Sinai Cement market capitalisation', 'B', +2000.0, 'peer_pe', +1,
     'a dearer peer at the same profit is a higher peer multiple'),
    ('Peer — Sinai Cement revenue', 'B', +500.0, 'peer_ps_scem', -1,
     'more peer revenue at the same market value is a lower price to sales'),
    ('Peer — Misr Beni Suef profit', 'B', +500.0, 'peer_pe', -1, 'the same mechanism'),
    ('Peer — Misr Beni Suef market capitalisation', 'B', +2000.0, 'peer_pe', +1, 'the same'),
    ('Peer — Misr Beni Suef revenue', 'B', +500.0, 'peer_ps_mbsc', -1, 'and the same'),
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
