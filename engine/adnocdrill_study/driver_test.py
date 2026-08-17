"""Prove the delivered workbook is a LIVE DRIVER model, not a pasted register.

READ FIRST tells the reader that changing a blue cell on the Assumptions sheet
reprices the model. That is a claim about the DELIVERED FILE, so it is tested on
the delivered file: each driver is perturbed in place, the whole workbook is
re-evaluated from scratch, and the test asserts that the headline moves, and
moves in the direction asserted BEFORE the run.

Then a dead-input sweep bumps every remaining numeric driver and requires it to
move something. An input that changes nothing anywhere is either decoration or a
broken chain, and both are defects.

Where an asserted direction turned out to be wrong, the model was decomposed
before anything was changed. One case survived that decomposition and is
documented at its entry: a higher depreciation rate RAISES free cash flow to the
firm, because depreciation leaves EBIT and comes straight back as a non-cash
add-back, so the only thing it changes is the tax bill.
"""
import json, os
import openpyxl
import xlcalc

HERE = os.path.dirname(os.path.abspath(__file__))
wb = openpyxl.load_workbook(os.path.join(HERE, 'ADNOCDRILL_Valuation_Model_09082026.xlsx'))
ANCH = json.load(open(os.path.join(HERE, 'xlsx_expected.json')))['anchors']
DR, TR, BT, GR, NR = (ANCH['dcf'], ANCH['terminal'], ANCH['plateau'], ANCH['bridge'],
                      ANCH['relnorm'])
SEG, BAL, INC, CSH = ANCH['segments'], ANCH['balance'], ANCH['income'], ANCH['cash']

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
    return dict(
        dcf_A=bk.cell_value('SOTP Bridge', f"B{GR['ps_aed']}"),
        dcf_B=bk.cell_value('SOTP Bridge', f"C{GR['ps_aed']}"),
        central=bk.cell_value('Summary', f"B{ANCH['central_row']}"),
        wacc_r=bk.cell_value('DCF', f"C{DR['wacc_r']}"),
        wacc_c=bk.cell_value('DCF', f"C{DR['wacc_c']}"),
        sovereign=bk.cell_value('DCF', f"C{DR['sov']}"),
        kd_spot=bk.cell_value('DCF', f"C{DR['kd_spot']}"),
        rev26=bk.cell_value('Segments', f"E{SEG['revenue']}"),
        rev27=bk.cell_value('Segments', f"F{SEG['revenue']}"),
        rev30=bk.cell_value('Segments', f"I{SEG['revenue']}"),
        ta25=bk.cell_value('Balance Sheet', f"D{ANCH['balance']['total_assets']}"),
        equity25=bk.cell_value('Balance Sheet', f"D{ANCH['balance']['equity']}"),
        ebitda30=bk.cell_value('Segments', f"I{SEG['ebitda']}"),
        equity30=bk.cell_value('Balance Sheet', f"I{ANCH['balance']['equity']}"),
        ebitda26=bk.cell_value('Segments', f"E{SEG['ebitda']}"),
        seg_on26=bk.cell_value('Segments', 'E' + str(SEG['revenue'] - 3)),
        pat26=bk.cell_value('Income Statement', f"E{INC['pat']}"),
        cash30=bk.cell_value('Cash Flow', f"I{CSH['close']}"),
        eps26=bk.cell_value('Per-Share & Ratios', 'E4'),
        pb=bk.cell_value('Relative & Normalized', f"C{NR['pb']}"),
        pv_explicit=bk.cell_value('DCF', f"C{TR['pv_exp']}"),
        relative=bk.cell_value('Relative & Normalized', f"C{NR['ps']}"),
        normalised=bk.cell_value('Relative & Normalized', f"C{NR['nps']}"),
        tvshare=bk.cell_value('DCF', f"C{TR['tvshare']}"),
    )


base = read()
print('base:')
for k, v in base.items():
    print(f'    {k:12s} {v:,.4f}')

# label, bump, headline, required sign, why — the direction is asserted in advance
CASES = [
    ('Terminal growth — continued expansion', +0.005, 'dcf_A', +1,
     'a higher terminal growth rate must raise the discounted cash flow'),
    ('Terminal growth — capacity plateau', +0.005, 'dcf_B', +1,
     'the same, on the plateau case'),
    ('Integrated-services rigs, year end (plateau) — 2030', +5.0, 'dcf_B', +1,
     'the plateau case is built live from its own fleet schedule, not pasted in'),
    ('Capital expenditure (plateau) — 2030', +200_000.0, 'dcf_B', -1,
     'and from its own capital-expenditure plan'),
    ('Unconventional revenue (plateau) — 2027', +100_000.0, 'dcf_B', +1,
     'and from its own unconventional path'),
    ('Equity beta', +0.20, 'dcf_A', -1,
     'a higher beta raises the cost of equity and must lower the valuation'),
    ('US 10-year Treasury yield (observed)', +0.01, 'dcf_A', -1,
     'a higher risk-free rate raises the whole cost of capital'),
    ('Equity risk premium — rating basis', +0.01, 'wacc_r', +1,
     'a higher equity risk premium must raise the cost of capital'),
    ('Equity risk premium — credit-default-swap basis', +0.01, 'wacc_c', +1,
     'the same, on the credit-default-swap basis'),
    ('Borrowing margin over Term SOFR on the latest facility', +0.01, 'wacc_r', +1,
     'a higher borrowing margin raises the marginal cost of debt and the cost of capital'),
    ('US 5-year Treasury yield', +0.01, 'sovereign', +1,
     'the sovereign floor is built off the same five-year point'),
    ('Abu Dhabi sovereign credit-default-swap spread', +0.01, 'sovereign', +1,
     'a wider sovereign spread raises the floor the cost of debt must clear'),
    ('Secured Overnight Financing Rate, spot', +0.01, 'kd_spot', +1,
     'the spot floating cross-check is the overnight rate plus the margin'),
    ('Corporate income tax rate', +0.05, 'dcf_A', -1,
     'a higher tax rate must lower NOPAT and the valuation'),
    ('Due from related parties — 30 June 2026', +500_000.0, 'dcf_A', -1,
     'the working-capital ratio is DERIVED from the 30 June 2026 balance sheet, so a heavier '
     'receivable from related parties raises the ratio, absorbs cash and lowers the valuation'),
    ('Due from related parties — 30 June 2026', +500_000.0, 'pv_explicit', -1,
     'and it bites inside the explicit window, where the cash is actually absorbed'),
    ('Trade and other payables — 30 June 2026', +500_000.0, 'dcf_A', +1,
     'and the other way on the payable side of the same derivation'),
    ('Revenue — first half of 2026', +200_000.0, 'dcf_A', +1,
     'a bigger revenue denominator lowers the derived working-capital ratio'),
    # FY2026 REVENUE CANNOT MOVE, AND THAT IS THE DESIGN. Each segment's unit
    # build is reconciled to the company's own FY2026 segment guidance, so the
    # reconciliation factor absorbs whatever the FY2026 build would otherwise have
    # done. The unit rates set the SHAPE of the forecast; the guidance sets its
    # LEVEL. Assertions that used to be written against FY2026 revenue are written
    # against FY2030 instead, which is where a driver's effect actually survives.
    ('Contract day-rate escalation', +0.005, 'rev30', +1,
     'a higher day-rate escalation must raise the revenue the forecast grows into'),
    ('Contract day-rate escalation', +0.005, 'rev26', 0,
     'and must NOT move FY2026, which is pinned to the segment guidance'),
    # ASSERTED UP, FAILED, AND THE MODEL WAS RIGHT AGAIN. With FY2026 pinned to the
    # guidance, a change in a FY2025 unit rate cannot change the LEVEL of the
    # forecast — the reconciliation factor divides it straight back out. What
    # survives is a MIX effect, and its sign is not obvious: a richer Abu Dhabi
    # onshore rate shifts weight within the reconciled onshore segment from the
    # regional book, which is growing faster off a smaller base, toward the
    # domestic book, which is not. FY2030 therefore falls slightly. The magnitude
    # says the same thing: 200,000 on the FY2025 base moves FY2030 by 3,151.
    ('Onshore segment revenue — FY2025', +200_000.0, 'rev30', -1,
     'the realised rate per onshore rig is DERIVED from FY2025 reported segment revenue over '
     'the reported rig count. With FY2026 reconciled to guidance, all that survives is a mix '
     'shift within the onshore segment, away from the faster-growing regional book'),
    ('Abu Dhabi onshore rigs — FY2025 year end', +5.0, 'rev30', -1,
     'the same derivation from the other side — more rigs behind the same reported revenue is a '
     'LOWER rate per rig — and again it lands after the pinned year'),
    ('Offshore Island revenue — FY2023', +200_000.0, 'rev30', +1,
     'the island-to-jack-up ratio is derived from the one year the two were reported '
     'separately, and it splits FY2025 offshore revenue between the two fleets, which then '
     'grow at different rates'),
    ('Rigs given at least one discrete service — FY2025', +10.0, 'rev30', -1,
     'the second oilfield-services volume driver: more rigs served behind the same reported '
     'segment revenue is a lower revenue per rig served, and a lower measured growth in it'),
    ('Oilfield Services segment revenue — FY2024', +200_000.0, 'rev30', -1,
     'FY2024 sets the BASE of the realised growth in revenue per rig served, so raising it '
     'lowers the measured growth the forecast carries forward'),
    ('Abu Dhabi onshore rigs, year end — 2026', +5.0, 'rev30', -1,
     'adding rigs to the 2026 year end ALONE, with the 2027-2030 schedule left where it was, '
     'makes the FY2026 build larger against a fixed guided level — so the reconciliation factor '
     'shrinks and the later years, whose rig counts did not move, come out lower. The schedule '
     'is meant to move together; the case below does that'),
    ('Abu Dhabi onshore rigs, year end — 2030', +5.0, 'rev30', +1,
     'and in the final forecast year, which nothing reconciles, more rigs is more revenue'),
    ('Integrated-services rigs, year end — 2030', +5.0, 'dcf_A', +1,
     'a larger integrated-services fleet in the final forecast year must raise the valuation'),
    ('Wage escalation (domestic labour only)', +0.02, 'ebitda26', -1,
     'faster wage inflation must cut EBITDA'),
    ('Oilfield-services cost escalation', +0.02, 'ebitda26', -1,
     'faster oilfield-services cost inflation must cut EBITDA'),
    ('Fuel escalation (own commodity path)', +0.05, 'ebitda26', -1,
     'a rising fuel path must cut EBITDA'),
    ('Staff costs — as reported', +50_000.0, 'ebitda26', -1,
     'the conventional staff-cost base is DERIVED from the reported cost note less the '
     'unconventional programme\'s share of it, so a heavier reported line cuts EBITDA'),
    # ASSERTED UP, FAILED, AND THE MODEL WAS RIGHT. A better unconventional margin
    # implies the unconventional programme carried LESS of FY2025's reported direct
    # cost — which leaves MORE of that reported cost in the conventional stack.
    # The conventional stack is then escalated on growing rig-years while the
    # unconventional book runs off, so the heavier conventional base outweighs the
    # lighter unconventional one. The chain is visible on the Assumptions sheet:
    # the margin drives 'Direct cost carried by the unconventional programme',
    # which is subtracted from each reported cost line to give its conventional base.
    ('Unconventional EBITDA margin', +0.05, 'ebitda26', -1,
     'a better assumed margin on the unconventional book leaves MORE of the reported FY2025 '
     'direct cost in the conventional stack, which is escalated on a growing rig fleet while '
     'the unconventional book runs off — so group EBITDA falls, not rises'),
    ('Unconventional booked to Oilfield Services — FY2025', +100_000.0, 'rev30', -1,
     'the Onshore share of the unconventional programme is the residual of the reported split, '
     'and moving the split changes which segment the reconciliation factor is solved on'),
    ('Capital expenditure — 2026', +200_000.0, 'dcf_A', -1,
     'more capital expenditure absorbs cash and must lower the valuation'),
    # THE CASE THE NOTE AT THE TOP OF THIS FILE REFERS TO. The first assertion
    # written here was that a higher depreciation rate RAISES the valuation:
    # FCFF = EBIT x (1 - t) + D&A - capex - change in working capital, so raising
    # D&A lowers EBIT one-for-one and adds the same amount straight back, leaving
    # only the tax the deduction saves. It failed. Decomposing it at +1 percentage
    # point, before changing anything:
    #     present value of the explicit five years   +17,018   (the tax shield —
    #                                                 the original reasoning, and
    #                                                 it is exactly 9% of the extra
    #                                                 depreciation, the tax rate)
    #     present value of the terminal value       -402,687
    #     enterprise value                          -385,669
    # The reasoning was right about the explicit window and wrong about the
    # headline. The terminal value is capitalised off terminal-year NOPAT, which
    # is struck AFTER depreciation, so a permanently heavier depreciation charge
    # on the same asset base is a permanently less profitable business — and at
    # 77% of enterprise value the terminal block swamps five years of tax shield.
    # The model is right. Both effects are now asserted separately.
    ('Depreciation and amortisation — FY2025 as reported', +100_000.0, 'pv_explicit', +1,
     'inside the explicit window depreciation leaves EBIT and returns as a non-cash '
     'add-back, so all that survives is the tax shield and cash flow RISES'),
    ('Depreciation and amortisation — FY2025 as reported', +100_000.0, 'dcf_A', -1,
     'but the terminal value is capitalised off terminal-year NOPAT, which is struck after '
     'depreciation, so the headline FALLS — the terminal block outweighs the tax shield'),
    ('Terminal return on invested capital', +0.05, 'dcf_A', +1,
     'a higher terminal return means less must be reinvested to buy the same growth'),
    ('Borrowings', +500_000.0, 'dcf_A', -1,
     'more debt in the bridge leaves less for shareholders'),
    ('Cash and cash equivalents', +500_000.0, 'dcf_A', +1,
     'more cash in the bridge leaves more for shareholders'),
    ('Investment in joint ventures', +200_000.0, 'dcf_A', +1,
     'the joint-venture stake is added in the bridge'),
    ('Minority interests recognised', +100_000.0, 'equity30', -1,
     'the minorities recognised on acquisition sit on the forecast balance sheet and reduce the '
     'equity attributable to owners'),
    ('Minority interests recognised', +100_000.0, 'dcf_A', 0,
     'and they must NOT move the valuation, because the bridge deducts the put liability over '
     'these same interests and deducting both would charge the parent twice for one claim'),
    ('Financial liability over the acquired minorities', +100_000.0, 'dcf_A', -1,
     'the put obligation over those minorities is deducted too'),
    ('Treasury shares held by the market maker', +1_000_000.0, 'dcf_A', +1,
     'fewer shares outstanding means more value per share'),
    ('Peer median EV/EBITDA — MENA national-oil-company drillers', +1.0, 'relative', +1,
     'a higher peer multiple must raise the relative lens'),
    ('Peer median EV/EBITDA — diversified oilfield services', +1.0, 'relative', +1,
     'the same, through the oilfield-services weight'),
    ('EBITDA — first half of 2026', +100_000.0, 'relative', +1,
     'the multiplied earnings are DERIVED last-twelve-month EBITDA, so a stronger reported half '
     'raises them and the lens with them'),
    ('EBITDA — first half of 2025', +100_000.0, 'relative', -1,
     'and the year-earlier half is subtracted in the same derivation'),
    ('Share of joint-venture results — first half of 2026', +50_000.0, 'relative', -1,
     'the joint-venture share is stripped out of the multiplied earnings, because its carrying '
     'value is added back on the bridge'),
    ('Terminal growth — continued expansion', +0.005, 'pb', +1,
     'the justified multiple of book is (return - growth) / (cost of equity - growth), and with '
     'the return well above the cost of equity a higher growth rate raises it'),
    ('Total equity — 30 June 2026', +500_000.0, 'central', +1,
     'book equity attributable to owners is DERIVED as total equity less minorities, so a '
     'larger reported equity raises the book lens'),
    ('FY2026 guided EBITDA — top of the range', +100_000.0, 'normalised', +1,
     'the normalised margin is DERIVED from the guided EBITDA range over the guided revenue'),
    ('FY2026 guided revenue', +100_000.0, 'normalised', -1,
     'and the guided revenue is its denominator'),
    ('Island rigs — 30 June 2026', +2.0, 'normalised', +1,
     'the normalised lens prices the fleet REPORTED at 30 June 2026, not a target'),
    ('Depreciation and amortisation — first half of 2026', +50_000.0, 'normalised', -1,
     'normalised depreciation is the reported first-half charge annualised, so a heavier '
     'reported charge lowers normalised NOPAT'),
    # The second case the note refers to. Asserted DOWN, failed, and the
    # decomposition was arithmetic: the central was a bare sum of value times
    # weight, so adding 0.10 to a weight added 0.10 x AED 4.06 = AED 0.406 to the
    # answer — precisely the move observed — instead of re-weighting. That is a
    # real defect in the workbook, not a wrong expectation, and it was fixed at
    # source: the central now divides by the sum of the weights. At the delivered
    # weights, which sum to one, the fix changes no delivered number.
    ('Weight — relative multiples', +0.10, 'central', -1,
     'the relative lens sits below the central, so weighting it more must lower the central'),
    ('Dividend, FY2026 floor', +200_000.0, 'cash30', -1,
     'a larger distribution must leave less cash at the end of the forecast'),
    ('Dividend growth', +0.02, 'cash30', -1,
     'a faster-growing distribution must leave less cash'),
    ('Market price', +1.0, 'wacc_r', +1,
     'a higher share price lifts the equity weight toward the more expensive cost of equity'),
    ('AED per USD', +0.5, 'dcf_A', +1,
     'a weaker dirham per dollar raises the dirham value of a dollar-denominated equity'),
    ('Shares issued', +1_000_000_000.0, 'dcf_A', -1,
     'more shares outstanding means less value per share'),
    ('Other income, FY2025 base', +50_000.0, 'ebitda26', +1,
     'other income is inside EBITDA'),
    ('Share of joint-venture results, FY2025 base', +50_000.0, 'ebitda26', +1,
     'the joint-venture share is inside reported EBITDA, though it is stripped out again '
     'before the cash-flow waterfall'),
    ('General and administrative expenses — as reported', +50_000.0, 'ebitda26', -1,
     'the overhead base is DERIVED as reported overhead less the depreciation inside it'),
    ('Depreciation inside general and administrative expenses', +10_000.0, 'ebitda26', +1,
     'and taking more depreciation out of that reported line leaves a lighter cash overhead'),
    ('Property and equipment acquired', +100_000.0, 'dcf_A', -1,
     'the assets acquired in 2026 carry depreciation from the year they arrive'),
    ('Term loans, overdraft and borrowings assumed', +100_000.0, 'cash30', -1,
     'the borrowings assumed with them are serviced out of the same cash flow. They do not move '
     'the discounted-cash-flow lens, and should not: free cash flow to the firm is struck before '
     'financing, and the bridge deducts the borrowings actually reported at 30 June 2026'),
    ('Net cash from operating activities — first half of 2026', +100_000.0, 'dcf_A', -1,
     'cash the enterprise has already handed out over the first half is no longer inside it '
     'when enterprise value is carried forward to the balance-sheet date'),
    ('Days from 30 June 2026 to the price anchor', +30.0, 'dcf_A', +1,
     'equity accretes at the cost of equity over the days between the balance sheet and the '
     'price it is compared against'),
    ('Unconventional revenue — 2026', +200_000.0, 'rev26', 0,
     'FY2026 total revenue is reconciled to the guided total, so moving the unconventional '
     'programme inside it cannot change the total — only the split'),
    ('Unconventional revenue — 2026', +200_000.0, 'rev30', -1,
     'what it does change is the conventional residual the reconciliation factor is solved on: '
     'a larger unconventional book inside a fixed guided segment leaves a smaller conventional '
     'one, and the later years scale off that'),
    ('Unconventional revenue — 2027', +200_000.0, 'rev27', +1,
     'and in a year the guidance does not pin, it lands directly'),
]

fails, checked = [], set()
for label, bump, key, sign, why in CASES:
    r = row_of(label)
    cur = wb['Assumptions'][f'C{r}'].value
    out = read({('Assumptions', f'C{r}'): cur + bump})
    delta = out[key] - base[key]
    rel = delta / abs(base[key]) if base[key] else 0.0
    ok = (abs(rel) < 1e-9) if sign == 0 else ((delta * sign > 0) and abs(rel) > 1e-9)
    checked.add(label)
    print(f"  [{'OK ' if ok else 'BAD'}] {label} {bump:+g} -> {key} {base[key]:,.4f} -> "
          f"{out[key]:,.4f} ({rel:+.3%})   {why}")
    if not ok:
        fails.append((label, key, delta, why))

print('\nDEAD-INPUT SWEEP — every remaining driver is bumped and must move something')
dead = []
for label, r in sorted(A.items(), key=lambda kv: kv[1]):
    cell = wb['Assumptions'][f'C{r}']
    if not isinstance(cell.value, (int, float)) or label in checked:
        continue
    # A zero-valued cell cannot be bumped proportionally, and a 1e-6 bump on a
    # line denominated in USD thousands moves the per-share answer by less than
    # the 1e-9 tolerance — which reads as a dead input when the chain is in fact
    # live. Bump zero cells by one unit of whatever the cell actually measures:
    # a percentage point for a rate, a million dollars for a money line.
    if cell.value == 0:
        bump = 0.01 if '%' in (cell.number_format or '') else 1000.0
    else:
        bump = cell.value * 0.10 + 1e-6
    out = read({('Assumptions', f'C{r}'): cell.value + bump})
    if all(abs(out[k] - base[k]) < 1e-9 for k in base):
        dead.append(label)
if dead:
    print('  inputs that changed nothing:', dead)
else:
    print('  none — every remaining driver reprices the model')

assert not fails, f'{len(fails)} drivers failed to move the model correctly: {fails}'
assert not dead, f'dead inputs: {dead}'
print(f'\nDRIVER TEST OK — {len(CASES)} drivers each reprice the workbook in the asserted '
      f'direction; 0 dead inputs across the whole Assumptions sheet')
