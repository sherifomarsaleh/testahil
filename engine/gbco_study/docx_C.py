"""Content part C: Appendices A–C, About, Disclosure, footer.

REBUILT 07-09-2026. Appendix A's history now comes from the walk-forward panel — the
company's own filed consolidated income statement, footed year by year — and its
forecast from the committed group build, rather than from three columns typed into this
file. Appendix A also now carries the far-year RANGES [R-FCAL-01] requires, which the
superseded edition did not publish at all.

THE CALIBRATION APPENDIX IS GONE [08-09-2026]. The model report's own skeleton says
calibration evidence appears in section 3 as plain-language sentences with the statistics
inline and that there is NO CALIBRATION APPENDIX; this study shipped four appendices where
the model ships three, so every address after A pointed one letter past its subject and
nine sections read as missing. Deleting it closes something worse than an address, and
that is the reason it goes rather than being renamed: the appendix published TWO COVERAGE
FIGURES FOR ONE BAND three sentences apart — its own replay RE-SCORED UNDER TODAY'S FIT
beside the record of the forecasts AS THEY WERE ACTUALLY STRUCK — with nothing on the page
saying they were different samples, so they read as one number and a typo of it. The
re-scored replay is an internal diagnostic and reaches no reader; what survives into
section 3 is the published band record alone. Peers move to B and the expert panel to C.
"""
import json
import os
from docx_base import *                                              # noqa: F401,F403
import table_residual as TR                                          # noqa: E402
from docx_A import (pc, sgn, n0, n1, paren, longdate, spot, SPOT_DATE, TA_CLOSE,
                    TA_DATE_L, SH, EDITION, EDITION_L, EDITION_STAMP, STAKE,
                    STAKE_PRIOR, STAKE_STATEMENTS, STAKE_STATEMENTS_PRIOR,
                    B_LO, B_HI, V_LO, V_HI, GAP_LO, GAP_HI, MARK_LO, MARK_HI,
                    EQ_LO, EQ_HI, REL, BOOK, CAP, PRICE_MARK, PRICE_ASSOC, PRICE_MNT_USD,
                    MNT_USD_AT_CARRYING, OPERATING_EQ, RATE_LO, RATE_HI,
                    QUALIFICATION, SHARE_OF_PROFIT, CJ)

HERE = os.path.dirname(os.path.abspath(__file__))
E = D['experts']; sotp = D['sotp']; dcf = D['dcf']
HIS = D['history']['income_statement']; PRV = D['history']['provenance']
GF = D['group_forecast']['rows']; DRV = D['disclosed_drivers']
COC = D['cost_of_capital_record']; MAC = D['macro']
HY = D['history']['years']
FY = [r['year'] for r in GF]
FYLABEL = ['FY%s' % (2026 + i) for i in range(len(FY))]

# ================= Appendix A ================================================
H1('Appendix A  Financial statements')
P('The historical columns are the company’s own consolidated income statement as originally reported, taken from the '
  'earnings release named against each year; every year is asserted to foot against its own arithmetic before it enters '
  'this study. The forecast columns are the model’s own build and reprice from the drivers in the companion workbook.')

H2('A.1  The far forecast years, published as ranges')
_WFB = json.load(open(os.path.join(HERE, '..', 'gbco_walkforward', 'forward_ranges.json'),
                      encoding='utf-8'))
_B = _WFB['bands']
_BASIS = _WFB['_basis'].split('—')[0].strip()
_ORIENT = _WFB['_orientation'].split('—')[0].strip()
P('The method behind this forecast was tested on GB Corp’s own history before it was trusted on its future: the '
  'driver model was rebuilt as it stood at a series of past origins, projected forward, and every driver scored against '
  'what the company actually went on to report. The table below carries what that record supports for the third, fourth '
  'and fifth forecast years — a RANGE rather than a point. Read the basis column: these bounds are the SPAN OF THE '
  'OBSERVED OUTCOMES, not percentiles. With the counts shown, a percentile would be a statistic invented for the '
  'occasion, and this study does not invent one.', size=9.8)
P('The bands are stated as the ratio of what the company REPORTED to what the method FORECAST, so a figure above one is '
  'a year the method came in low. They are applied by multiplying the point projection.', size=9.8)


def _band_rows(driver, points, label):
    out = []
    for h, (yr, pt) in zip(('h3', 'h4', 'h5'), points):
        b = _B[driver][h]
        out.append([yr, n0(pt * b['low']), n0(pt), n0(pt * b['high']),
                    f"{b['low']:.2f}–{b['high']:.2f}×", b['basis'], str(b['n'])])
    return out


_far = list(zip(FYLABEL[2:], [r['revenue'] for r in GF[2:]]))
_far_gp = list(zip(FYLABEL[2:], [r['gross_profit'] for r in GF[2:]]))
_far_op = list(zip(FYLABEL[2:], [r['operating_profit'] for r in GF[2:]]))
_far_np = list(zip(FYLABEL[2:], [r['net_profit'] for r in GF[2:]]))
rows = [['Forecast year', 'Low', 'Point', 'High', 'Band applied', 'Basis', 'Observations']]
rows.append(['Group revenue (EGP mn)', '', '', '', '', '', ''])
rows += _band_rows('revenue', _far, 'revenue')
rows.append(['Group gross profit (EGP mn)', '', '', '', '', '', ''])
rows += _band_rows('gross_profit', _far_gp, 'gross profit')
rows.append(['Group operating profit (EGP mn)', '', '', '', '', '', ''])
rows += _band_rows('operating_profit', _far_op, 'operating profit')
rows.append(['Group net profit (EGP mn)', '', '', '', '', '', ''])
rows += _band_rows('net_profit', _far_np, 'net profit')
table(rows, [1.45, 0.95, 0.95, 0.95, 1.05, 0.75, 0.95], size=8.4,
      band_rows=[1, 5, 9, 13])
caption('Table A0 — the third, fourth and fifth forecast years as ranges. Each band is the full span of that many past '
        'readings of how far out this method has been on this company, applied to the point projection above. The '
        'observation count falls as the horizon lengthens, because a five-year error can only be scored where five years '
        'of history have since resolved.')
try:
    import range_disclosure as RD
    _ns = sorted({_B[k][h]['n'] for k in _B for h in ('h3', 'h4', 'h5')})
    P('What a range of this kind can honestly promise, at each of the record lengths above:', size=9.6)
    for _n in _ns:
        P('· ' + RD.sentence(_n), size=9.2, space_after=3)
except Exception:                                                    # noqa: BLE001
    P('The disclosure module that states what a span of a given length can promise could not be read in this build; '
      'the counts above are printed so a reader can judge the bands directly.', size=9.4, italic=True)
P('One line of the table deserves its own sentence. The net-profit band rests on the fewest observations of any driver '
  'here, and at the fifth forecast year on a single one — a span of one reading is not a span at all, and it is printed '
  'with its count rather than dressed up. Net profit is the most geared line in this model: it sits below a finance cost '
  'and a tax charge, so a modest error on revenue arrives at the bottom multiplied. That is why the range widens down the '
  'table rather than narrowing.', size=9.6)

H2('A.2  Income statement — reported (EGP mn)')
_ISLINES = [
 ('revenue', 'Revenue', False),
 ('gross_profit', 'Gross profit', False),
 ('selling', 'Selling and marketing', False),
 ('admin', 'General and administration', False),
 ('other_income', 'Other income', False),
 ('provisions', 'Provisions', False),
 ('operating_profit', 'Operating profit', True),
 ('associates', 'Share of associates', False),
 ('ebit', 'Operating profit including associates', True),
 ('fx', 'Foreign-exchange gains (losses)', False),
 ('finance_net', 'Net finance cost', False),
 ('ebt', 'Profit before tax', True),
 ('tax', 'Income tax', False),
 ('npbmi', 'Profit before minority interest', True),
 ('minority', 'Minority interest', False),
 ('net_profit', 'Profit attributable to the parent', True),
]
rows = [['Line'] + ['FY%s' % y for y in HY]]
for key, lbl, _bold in _ISLINES:
    rows.append([lbl] + [n1(HIS[y][key]) for y in HY])
rows.append(['Gross margin'] + [pc(HIS[y]['gross_profit'] / HIS[y]['revenue'], 2) for y in HY])
rows.append(['Net margin'] + [pc(HIS[y]['net_profit'] / HIS[y]['revenue'], 2) for y in HY])
rows.append(['Earnings per share (EGP)'] + [f"{HIS[y]['net_profit']/SH:.2f}" for y in HY])
table(rows, [2.6, 1.5, 1.5, 1.5], first_col_bold=True, size=8.6,
      band_rows=[i + 1 for i, (_, _, b) in enumerate(_ISLINES) if b])
caption('Table A1 — the consolidated income statement as the company reported it, one column per year, every figure '
        'read from the study’s committed record. Deductions are printed as the negative figures the statement '
        'carries, so a reader adding the column reaches the subtotal beneath it. Sources: '
        + '; '.join('FY%s — %s, %s' % (y, PRV[y]['source'], PRV[y]['source_date']) for y in HY) + '.')

H2('A.3  Income statement — forecast (EGP mn)')
rows = [['Line'] + FYLABEL]
_FLINES = [
 ('auto_revenue', 'GB Auto revenue', False),
 ('capital_revenue', 'GB Capital revenue', False),
 ('eliminations', 'Intercompany eliminations', False),
 ('revenue', 'Total revenue', True),
 ('gross_profit', 'Gross profit', False),
 ('sga', 'Selling and administration', False),
 ('other_income', 'Other income', False),
 ('provisions', 'Provisions', False),
 ('operating_profit', 'Operating profit', True),
 ('associates', 'Share of associates', False),
 ('ebit', 'Operating profit including associates', True),
 ('finance_net', 'Net finance cost', False),
 ('ebt', 'Profit before tax', True),
 ('tax', 'Income tax', False),
 ('npbmi', 'Profit before minority interest', True),
 ('minority', 'Minority interest', False),
 ('net_profit', 'Profit attributable to the parent', True),
]
for key, lbl, _bold in _FLINES:
    rows.append([lbl] + [n0(r[key]) for r in GF])
rows.append(['Gross margin'] + [pc(r['gross_profit'] / r['revenue'], 2) for r in GF])
rows.append(['Earnings per share (EGP)'] + [f"{r['net_profit']/SH:.2f}" for r in GF])
table(rows, [2.15, 0.9, 0.9, 0.9, 0.9, 0.9], first_col_bold=True, size=8.4,
      band_rows=[i + 1 for i, (_, _, b) in enumerate(_FLINES) if b])
caption('Table A2 — the consolidated forecast, computed from the committed group drivers. It is one arithmetic, printed '
        'here and recomputed by the companion workbook, rather than a transcription of an Excel run. THE THIRD, FOURTH '
        'AND FIFTH COLUMNS ARE POINTS INSIDE THE RANGES OF TABLE A0 and should be read with that table open.')

H2('A.4  The Auto leg — free cash flow (EGP mn)')
rows = [['Line'] + [r['year'] for r in dcf['rows']]]
for key, lbl in [('rev', 'Auto revenue'), ('ebit', 'Operating profit'),
                 ('nopat', 'Operating profit after tax'), ('dna', 'Plus depreciation and amortisation'),
                 ('capex', 'Less capital expenditure'), ('dwc', 'Less increase in working capital'),
                 ('fcff', 'Free cash flow to the firm')]:
    row = [lbl]
    for r in dcf['rows']:
        v = r[key]
        row.append(paren(v) if key in ('capex', 'dwc') else n0(v))
    rows.append(row)
table(rows, [2.4, 0.86, 0.86, 0.86, 0.86, 0.86], first_col_bold=True, size=8.6, band_rows=[7])
for _r in dcf['rows']:
    TR.waterfall(_r['nopat'],
                 [('Plus depreciation and amortisation', _r['dna']),
                  ('Less capital expenditure', _r['capex']),
                  ('Less increase in working capital', _r['dwc'])],
                 _r['fcff'], dp=0, what='Table A3 free cash flow, %s' % _r['year'])
caption('Table A3 — the Auto leg’s cash flow, line for line as §1.2 discounts it. Deductions are printed as '
        'magnitudes in brackets and the labels state the operation, so the column can be followed to the result.')

H2('A.5  The balance-sheet anchors the bridge stands on')
# TWO DATES AND THEY ARE NOT THE SAME DATE. Every figure below is read off the SAME
# reviewed balance sheet, and the document a reader would go and find it in carries its own
# publication date. Printing one column headed "as at" and filling it with both is how a
# reader is told a bridge stands on a date it does not.
_BSDATE = longdate(D['forecast_anchor']['latest_reviewed_date'])
rows = [['Item', 'Value (EGP mn)', 'Balance sheet as at', 'Where it was read, and the date that document carries']]
for k, lbl in [('cash_jun2026', 'Cash and equivalents'), ('debt_jun2026', 'Borrowings, group'),
               ('debt_auto_jun2026', 'Borrowings, GB Auto segment'),
               ('eq_jun2026', 'Group total equity — a disclosed line, not a sum of the rows above')]:
    it = D['inputs'][k]
    rows.append([lbl, n1(it['value']), _BSDATE, '%s — %s' % (it['layer'], longdate(it['date']))])
rows.append(['Auto net debt used in the bridge', n1(dcf['auto_nd']), _BSDATE,
             'the segmented balance sheet, GB Auto column, on the company’s own net-debt definition'])
rows.append(['Auto non-controlling interests deducted', n1(dcf['auto_nci']), _BSDATE,
             'that leg’s own minority interest'])
table(rows, [2.1, 1.05, 1.15, 2.8], first_col_bold=True, size=8.6)
caption('Table A4 — the bridge stands on the latest disclosed balance sheet, the reviewed statements to 30 June 2026, '
        'and not on the prior year end. The deduction is the AUTO leg’s own net debt and the AUTO leg’s own '
        'minority, because the lender’s borrowings are its raw material rather than its leverage.')

# ================= Appendix B ================================================
# The calibration appendix that used to stand here is deleted, not moved: the band record
# belongs in section 3 as plain sentences with the statistics inline, and it is there.
H1('Appendix B  Peer frame, risk register and the research register')

H2('B.1  Peers and the sector frame')
P('GB Corp has no clean single comparable — an auto assembler-distributor, a non-bank lender and a fintech '
  'associate in one wrapper, and that is why the class primary is a sum of the parts rather than a multiple. The peer '
  'set is therefore split by leg, and it is used for cross-checks only: no peer is a source for GB Corp’s own reported '
  'figures, and no peer multiple is applied to the group as a whole.')
rows = [
 ['Leg', 'Closest peers', 'How they are typically valued', 'Caution'],
 ['Auto assembly and distribution', 'Gulf and regional auto distributors; listed consumer-durables names on this exchange', 'Enterprise value against operating profit; earnings multiples', 'None of them assembles under the same localisation regime or carries a captive lender'],
 ['Non-bank consumer and corporate finance', 'Listed Egyptian finance companies with a comparable book', 'Price to book against the return on that book', 'Funding mix and provisioning policy differ enough that the multiple travels badly'],
 ['Fintech associate', 'Listed payments and financial-technology names on this exchange', 'Private marks; the last round is the only observable price', 'A listed comparator has a price and this holding has none — which is the whole subject of this study'],
]
table(rows, [1.5, 2.1, 1.7, 1.8], first_col_bold=True, size=8.5)
P('The absence of a single clean comparable is itself a finding rather than a gap in the research, and it is why the '
  'relative multiple in §1.3 is taken from GB CORP’S OWN trailing rating at its own three year-end closes rather than '
  'from a peer set at all. Sector structure: the Egyptian passenger-car market is in a policy-assisted recovery, with '
  'the easing cycle restoring affordability, localisation incentives reshaping the assembled-versus-imported mix, and '
  'new entrants resetting price points. Consumer and corporate finance is growing faster than banking credit off a low '
  'base, with securitisation deepening as a funding market.', size=9.8)

H2('B.2  Risk register')
P('Every risk below is either PRICED — the study can put a number on what it is worth and does — or NAMED AND NOT '
  'PRICED, because the disclosure to price it does not exist. Nothing is left as an adjective. Where a risk is one of '
  'the study’s own contested judgements, the figure is what moving that judgement to its other framing does to the '
  'answer.', size=9.8)
_J = {j['name']: j for j in CJ['judgements']}


def _fork(name):
    # A KEY THAT MOVES RAISES RATHER THAN DEFAULTING. The register is the study's own and
    # a risk row silently losing its figure is worse than a build that stops.
    if name not in _J:
        raise KeyError('the judgements record no longer carries %r; it carries %r'
                       % (name, sorted(_J)))
    return _J[name]


rows = [['Risk', 'Mechanism', 'What it is worth']]
rows.append([
 'The basis on which the associate is marked',
 'GB Corp carries its MNT-Halan interest one way in its own reviewed balance sheet and announced a funding round that '
 'marks it another. Both are its own disclosures; the filings do not choose',
 f'THE ANSWER ITSELF: EGP {(MARK_HI-MARK_LO)/SH:.2f} a share between the two published branches, '
 f'{pc((MARK_HI-MARK_LO)/EQ_HI,1)} of the higher one'])
rows.append([
 'The associate’s own accounts cannot be verified',
 'The reviewers of the 30 June 2026 statements were not provided with that company’s financial statements and could '
 'not verify the group’s share of its profits; the same qualification stood on the prior audited year',
 'NAMED AND NOT PRICED. A qualification says a figure could not be verified, not what it should have been — but it is '
 'why the lower branch is not a safe harbour'])
_wc = _fork('working-capital intensity')
rows.append([
 'Working-capital intensity does not release',
 'The auto leg’s free cash flow is a thin residual, so the glide in receivables, inventory and payables moves it '
 'directly',
 f'PRICED: {pc(_wc["moves_the_carrying_branch_by"],1)} of the lower branch. Holding the first forecast year flat '
 f'across the window gives EGP {_wc["value_alternative_carrying_branch"]:.2f} against EGP {V_LO:.2f}'])
_erp = _fork('the equity risk premium basis')
_bta = _fork('the equity beta')
rows.append([
 'The cost of capital is higher than this study builds',
 'The premium basis and the beta are both estimates, and the whole ladder moves with either',
 f'PRICED: {pc(_erp["moves_the_carrying_branch_by"],1)} on the premium basis and '
 f'{pc(_bta["moves_the_carrying_branch_by"],1)} on the beta, each measured on the lower branch. §1.9 prices the '
 f'whole grid'])
_lend = _fork("the return anchoring GB Capital's justified price-to-book")
rows.append([
 'The lender’s return is a credit cycle',
 'GB Capital is marked by the return it earns above the cost of that equity, and both move with the cycle',
 f'PRICED: {pc(_lend["moves_the_carrying_branch_by"],1)} between the reviewed half and the full prior year — EGP '
 f'{n0(CAP["value_fy25_framing"])} mn against EGP {n0(CAP["value"])} mn on that leg'])
_gm = _fork('the Auto gross-margin path')
rows.append([
 'The Auto margin does not hold where the reviewed half left it',
 'New entrants resetting price points, or the currency moving through imported assembly content',
 f'PRICED: {pc(_gm["moves_the_carrying_branch_by"],1)} between the forecast path and the latest reviewed half held '
 f'flat across the window'])
rows.append([
 'Terminal-value dependency, on an asset life that could not be sourced',
 f'{pc(dcf["tv_pct"],0)} of the auto leg’s enterprise value is terminal value, and the accounting-policy note '
 'discloses depreciation rate RANGES per class rather than a life',
 'NAMED AND NOT PRICED. A life this desk chose would not be a disclosed life, so none was chosen; B.3 records the '
 'search'])
rows.append([
 'Regional exposure to Iraq and Jordan',
 'Conflict has already cut volumes in markets that are part of passenger-car revenue',
 'NAMED AND NOT PRICED. No sourced split of that revenue for the reviewed half exists in the documents this study '
 'holds'])
rows.append([
 'The pound, on the round-price branch only',
 'The round is struck in dollars and translated; a step devaluation moves assembly costs, rates and the pound value of '
 'that mark at once',
 'NAMED AND NOT PRICED as a separate line. It moves the ROUND branch only — the carrying branch is a pound figure off '
 'a pound balance sheet and does not move with it at all'])
table(rows, [1.75, 2.75, 2.6], first_col_bold=True, size=8.4)
caption('Table B1 — the risk register. Every priced figure is the study’s own contested-judgement record read straight, '
        'measured on the branch that gives the larger relative number so the register errs strict.')

H2('B.3  The research register — layers, dated, negative results included')
P('Research for this study proceeded in four layers: the global backdrop, the country, the industry and the company '
  'itself. Figures GB CORP REPORTS ABOUT ITSELF come only from documents GB Corp published — its own audited and '
  'reviewed statements, its own earnings releases and its own investor material — and never from a data vendor, a '
  'broker or a press report. Where the company’s own document could not be obtained, the study says so below rather '
  'than substituting a weaker source. The standalone source register that accompanies this study carries every input '
  'with its value, its source, that source’s own date and the layer it belongs to.')
_seen, _srcrows = set(), []
for _y in HY:
    _p = PRV[_y]
    if _p['source'] not in _seen:
        _seen.add(_p['source'])
        _srcrows.append([_p['source'], 'Company', longdate(_p['source_date']),
                         'the consolidated income statement as originally reported for FY%s' % _y])
_bylayer = {}
for _k, _v in D['inputs'].items():
    _bylayer.setdefault(_v.get('layer', 'Unclassified'), []).append(_v)
for _layer in sorted(_bylayer):
    _items = _bylayer[_layer]
    _dates = sorted({_i['date'] for _i in _items})
    _srcrows.append(['GB Corp’s own reviewed statements, earnings releases and investor material',
                     _layer, '%s to %s' % (longdate(_dates[0]), longdate(_dates[-1])),
                     'the %d dated inputs the model consumes, each carried in the source register with its own '
                     'four fields' % len(_items)])
rows = [['Source', 'Layer', 'Date the source carries', 'What it provided']] + _srcrows
table(rows, [2.6, 1.15, 1.35, 2.0], first_col_bold=False, size=8.2)
P('Negative results. Each of these is a search that was actually run and did not find what it was looking for; each '
  'shaped the model as much as the evidence did.', size=9.8, space_before=6)
for _head, _body in [
 ('No disclosed useful life for the operating asset base. ',
  'A terminal is meant to rest on a life the company discloses. GB Corp’s accounting-policy note gives depreciation '
  'rate RANGES by asset class and no single figure; recovering an implied life from the property, plant and equipment '
  'note returns a span that depends on an undisclosed land split and produces per-class rates that contradict the '
  'disclosed bands. Finding a range is not finding a life, and a derived life that contradicts the policy it '
  'implements is not one either. No life was chosen and the refusal is printed in §1.2.'),
 ('No audited financial statements for the associate that dominates this valuation. ',
  'They were not available to this study and they were not available to GB Corp’s own reviewers either, who say so in '
  'a qualified conclusion. That absence is the reason this study publishes two answers rather than one.'),
 ('No sourced split of passenger-car revenue between the domestic and regional markets for the reviewed half. ',
  'The regional exposure is named as a risk and a reader is entitled to its size. It is not disclosed in the documents '
  'this study holds for that period, so the exposure is NAMED and NOT PRICED and no split was estimated.'),
 ('No usable beta from the first regression attempted on this name. ',
  'The first attempt used five annual observations and returned a negative slope with essentially no explanatory '
  'power. It was refused rather than used. A conforming weekly regression against the exchange’s published index has '
  'since been produced and is what this edition adopts; the superseded figure is recorded beside it in the source '
  'register rather than deleted.'),
 ('No terms for the second closing of the June-2026 round. ',
  'Public reporting describes that close as an initial tranche of an ongoing round. Size and terms are undisclosed, so '
  'neither a higher nor a lower mark has a number behind it and none was invented.'),
 ('No audited statements for the two earliest years of the intended history window. ',
  'The company’s own filings index does not reach those years, and the annual reports for them lay the statements out '
  'in a form the text layer cannot attach to labels. The affected balance-sheet items are recorded as MISSING with '
  'that reason rather than estimated, and the window was shortened instead.'),
]:
    bullet(_body, bold_head=_head)

# ================= Appendix C ================================================
H1('Appendix C  The expert valuation panel')
P('Every study closes with a panel of standing expert personas, so that each accumulates a track record across studies '
  'and an update is a re-run rather than a re-training. For GB Corp we cast the industrial trio, adapted to what this '
  'group actually is: Expert 1 (the accountant — net asset value and the marks), Expert 2 (residual income — what '
  'the group’s own reported return justifies against its own book), Expert 3 (cash returns — return on capital '
  'against its cost). Each runs a different method, derives its value from shown workings, states a named sensitivity, '
  'and states in advance what would falsify it.')
P('One change since the last edition is worth naming, because it is a method being retired rather than a persona being '
  'renamed. Expert 2 used to capitalise mid-cycle earnings. That lens is gone from this study for the reason §1.4 gives '
  '— GB Corp’s reported earnings swing with what its associates are marked at rather than with an operating cycle — '
  'so an expert still running it would be working on a lens the study no longer holds. He now runs residual income on '
  'the whole group, which needs no mid-cycle figure anybody has to choose.', size=9.8)

_e1, _e2, _e3 = E['e1'], E['e2'], E['e3']

H2('C.1  Expert 1 — the split-legs net asset value and the marks')
P('Worldview. A group is worth the sum of its parts at realisable value, less a discount for the wrapper. Mark each leg '
  'to what it would fetch on its own; then argue only about the discount.', size=9.8)
P('When it works and when it fails. Best where the legs are separable and independently markable; it fails hardest when '
  'the discount applied to a private mark is itself contestable, which is exactly his position here. He also differs from '
  'the study on the lender: he marks it at its book rather than at what its return justifies, which is a real '
  'disagreement and is why his number is not the study’s round-price branch.', size=9.8)
rows = [
 ['Expert 1’s marks', 'EGP mn'],
 ['Auto leg (he accepts the §1.2 cash-flow value)', n0(sotp['auto_eq'])],
 ['Plus GB Capital at its operating book', n0(CAP['operating_equity'])],
 ['Plus associates: MNT-Halan at the round price, plus the residual holdings', n0(sotp['assoc'])],
 ['Sum before the discount', n0(sotp['auto_eq'] + CAP['operating_equity'] + sotp['assoc'])],
 [f"Less wrapper discount at {pc(_e1['wrapper_discount'],0)} — an operator, not a passive holding company", paren((sotp['auto_eq'] + CAP['operating_equity'] + sotp['assoc']) * _e1['wrapper_discount'])],
 ['Equity value', n0(_e1['base'] * SH)],
 ['Per share (EGP)', f"{_e1['base']:.2f}"],
]
table(rows, [4.4, 1.7], first_col_bold=True, size=9.0)
_e1_sum = sotp['auto_eq'] + CAP['operating_equity'] + sotp['assoc']
TR.waterfall(sotp['auto_eq'],
             [('Plus GB Capital at its operating book', CAP['operating_equity']),
              ('Plus associates', sotp['assoc'])],
             _e1_sum, dp=0, what='C.1 Expert 1, sum before the discount')
TR.waterfall(_e1_sum,
             [('Less wrapper discount', _e1_sum * _e1['wrapper_discount'])],
             _e1['base'] * SH, dp=0, what='C.1 Expert 1, equity value')
P(f"Sensitivity — the swing is the mark, not the ownership. Marking MNT-Halan at three quarters of the round’s "
  f"valuation takes his number to EGP {_e1['mark_haircut']['0.75']:.2f} per share; at half, to EGP "
  f"{_e1['mark_haircut']['0.5']:.2f}. He concedes the point openly: the stake is not the argument, the argument is what "
  f"a {pc(STAKE,2)} minority holding in an unlisted company is worth to a public-market buyer who cannot sell it.",
  size=9.8)
rich([('Verdict, falsification, and what the price implies. ', dict(bold=True)),
      (f"Fair value EGP {_e1['base']:.2f}, on a range of EGP {_e1['rng'][0]:.2f} to {_e1['rng'][1]:.2f} — the widest "
       "in the room, and driven by the discount debate rather than by an unconfirmed stake. HE IS FALSIFIED BY a real "
       "secondary transaction in the associate’s shares at a materially different price, or by a second closing "
       f"repricing the round. The traded price leaves EGP {n0(PRICE_ASSOC)} mn for all the associates together, which in "
       "his own view is evidence the market does not accept that the round’s marked value transfers cleanly to a "
       "minority holder.", {})])

H2('C.2  Expert 2 — residual income on the whole group')
P('Worldview. A company is worth its book value plus the present value of whatever it earns ABOVE the cost of that '
  'equity. If it earns exactly its cost of capital it is worth book; if it earns less, it is worth less than book, and no '
  'growth rate rescues it. He needs no mid-cycle earnings figure and no multiple anybody has to choose — only a book '
  'value, a return and a cost of equity, all three of which the accounts and the cost-of-capital schedule already carry.',
  size=9.8)
P('When it works and when it fails. Best where the accounts are clean and the return is durable. It fails where reported '
  'equity or reported profit is contaminated, and HE STATES THAT BOTH OF HIS OWN INPUTS ARE, in known directions: the '
  'earnings carry the group’s share of associate results, and the equity carries a revaluation booked on deconsolidating '
  'an associate. He runs the method anyway and says so, because the direction of the contamination is the argument. His '
  'is the harshest read in the study.', size=9.8)
rows = [
 ['Expert 2’s residual-income read', 'Value'],
 ['Group shareholders’ equity before minority interests, 30 June 2026 (EGP mn)', n1(_e2['book'])],
 ['Divided by shares in issue (mn)', n1(SH)],
 ['Book value per share (EGP)', f"{_e2['book_ps']:.2f}"],
 ['Return on that equity — FY2025 reported profit attributable over reported equity', pc(_e2['roe'], 2)],
 ['Cost of that equity — the terminal rate from the §1.8 schedule', pc(CAP['ke_terminal'], 2)],
 ['Long-run growth applied to both', pc(CAP['g'], 2)],
 ['Times the justified multiple of book — (return less growth) over (cost of equity less growth)', f"{_e2['pb']:.4f}×"],
 ['Fair value per share (EGP)', f"{_e2['base']:.2f}"],
]
table(rows, [4.4, 1.7], first_col_bold=True, size=9.0)
TR.waterfall(_e2['book'], [('Divided by shares in issue (mn)', SH)],
             _e2['book_ps'], dp=2, what='C.2 book value per share')
TR.waterfall(_e2['book_ps'], [('Times the justified multiple of book', _e2['pb'])],
             _e2['base'], dp=2, what='C.2 Expert 2 fair value')
P(f"His arithmetic in one sentence: the group earns {pc(_e2['roe'],2)} on its own reported equity against a cost of "
  f"{pc(CAP['ke_terminal'],2)}, a shortfall of {abs(_e2['roe']-CAP['ke_terminal'])*100:.2f} points against its cost of capital, "
  f"so the accounts on their own justify {_e2['pb']:.4f}× book and no more — EGP {_e2['base']:.2f} a share against a "
  f"book value of EGP {_e2['book_ps']:.2f} and a traded price of EGP {spot:.2f}.", size=9.8)
P(f"Sensitivity — the swing is the return, and he names it as the only lever worth arguing about. A return one "
  f"percentage point lower takes him to EGP {_e2['rng'][0]:.2f}; two points higher, to EGP {_e2['rng'][1]:.2f}. That is "
  "the whole range: at this cost of equity the justified multiple is roughly ten times as sensitive to the return as it "
  "is to anything else on the page, which is why he refuses to argue about multiples.", size=9.8)
P('His own two admissions, stated before anyone puts them to him. FIRST, HIS EARNINGS ARE CONTAMINATED UPWARD: the '
  f'group’s share of associates’ results was EGP {n1(D["history"]["income_statement"]["2025"]["associates"])} mn in '
  f'FY2025, {pc(D["history"]["income_statement"]["2025"]["associates"]/D["history"]["income_statement"]["2025"]["net_profit"],0)} '
  'of profit attributable — so the return he measures is FLATTERED by the very associate the other two experts are '
  'arguing about, and the operating return is lower than the one in his table. SECOND, HIS EQUITY IS CONTAMINATED '
  'UPWARD TOO: it includes the revaluation booked when an associate was deconsolidated, which the company itself strips '
  'out of its own return measure. The two pull the ratio in opposite directions and he does not claim to net them. '
  'What survives both admissions is his one claim, and it does not depend on the size of either: on its own accounts, '
  'read as they stand, GB Corp does not earn its cost of equity — so the entire investment case rests on the associate '
  'being worth more than those accounts say.', size=9.8)
rich([('Verdict, falsification, and what the price implies. ', dict(bold=True)),
      (f"Fair value EGP {_e2['base']:.2f}, on a range of EGP {_e2['rng'][0]:.2f} to {_e2['rng'][1]:.2f} — far the most "
       f"conservative in the room and {sgn(_e2['base']/spot-1)} against the traded price, which is the one number in "
       "this study that reads the shares as expensive. HE IS FALSIFIED BY the group’s return on its own reported equity "
       "rising to its cost of equity and staying there for two consecutive reported years — which on his own arithmetic "
       "would take his value straight to book — or by the associate being realised at anything like either of the "
       "marks in §1.1, since a realisation converts the contaminated line into cash and settles the argument. What the "
       "price implies against him is that the market pays a premium to his number: he is the read a buyer of these "
       "shares is betting against.", {})])

H2('C.3  Expert 3 — cash returns: return on capital against its cost')
P('Worldview. A business creates value only when each pound of capital earns above its cost, in cash. He looks past the '
  'income statement to the economic-profit spread, and past reported returns to returns excluding one-offs.', size=9.8)
P('When it works and when it fails. Best for capital-intensive compounders where the reinvestment spread is the story; '
  'it fails where the capital base is temporarily inflated by a one-off build, which is his own caveat here.', size=9.8)
_ch = D['cap_hist']
rows = [
 ['Expert 3’s economic-profit test', 'Value'],
 ['Auto capital employed, FY2025 (EGP mn)', n0(E['e3_ce'])],
 ['Auto return on capital employed — FY2023 / FY2024 / FY2025', f"{pc(_ch['FY23']['roce'],1)} / {pc(_ch['FY24']['roce'],1)} / {pc(_ch['FY25']['roce'],1)}"],
 ['His hurdle — the first forecast year’s cost of capital', pc(COC['wacc_exp'], 2)],
 [f"Spread near nil, so the operating leg is marked at {E['e3']['params']['ev_mult']:.2f}× capital employed (EGP mn)", n0(E['e3']['ev_at_base'])],
 ['Less Auto net debt and minority interests (EGP mn)', paren(dcf['auto_nd'] + dcf['auto_nci'])],
 ['Operating-leg equity (EGP mn)', n0(E['e3']['equity_at_base'])],
 [f"Plus the lender at {E['e3']['params']['cap_mult']:.2f}× its operating book (EGP mn)", n0(CAP['operating_equity']*E['e3']['params']['cap_mult'])],
 [f"Plus the associates at {E['e3']['params']['assoc_mult']:.2f}× the round-price mark (EGP mn)", n0(sotp['assoc']*E['e3']['params']['assoc_mult'])],
 ['Equity value (EGP mn)', n0(_e3['base'] * SH)],
 ['Per share (EGP)', f"{_e3['base']:.2f}"],
]
table(rows, [4.4, 1.7], first_col_bold=True, size=9.0)
TR.waterfall(E['e3']['ev_at_base'],
             [('Less Auto net debt and minority interests', dcf['auto_nd'] + dcf['auto_nci'])],
             E['e3']['equity_at_base'], dp=0, what='C.3 Expert 3, operating-leg equity')
TR.waterfall(E['e3']['equity_at_base'],
             [('Plus the lender at its haircut multiple', CAP['operating_equity'] * E['e3']['params']['cap_mult']),
              ('Plus the associates at their haircut multiple', sotp['assoc'] * E['e3']['params']['assoc_mult'])],
             _e3['base'] * SH, dp=0, what='C.3 Expert 3, equity value')
P(f"Sensitivity — two levers, and he ranks them himself. Moving his haircut on the associate mark from "
  f"{E['e3']['params']['assoc_mult']:.2f}× to {E['e3']['params']['assoc_mult_bear']:.2f}× costs EGP "
  f"{abs(_e3['mark_lever']):.2f} per share; marking the operating leg at "
  f"{E['e3']['params']['ev_mult_bull']:.2f}× capital employed instead of "
  f"{E['e3']['params']['ev_mult']:.2f}×, which is what a recovery in the return on capital would buy, adds EGP "
  f"{_e3['roce_lever']:.2f}. The mark is the bigger lever by more than two to one, and that is his point.", size=9.8)
rich([('Verdict, falsification, and what the price implies. ', dict(bold=True)),
      (f"Fair value EGP {_e3['base']:.2f}, on a range of EGP {_e3['rng'][0]:.2f} to {_e3['rng'][1]:.2f} — even his "
       f"conservative method lands {sgn(_e3['base']/spot-1)} against the price once the stated stake is applied at a "
       "haircut to the round’s valuation. HE IS FALSIFIED BY a durable recovery in the return on capital well above the "
       "FY2025 figure, which would make his multiple of capital employed too low, or by a real secondary sale of the "
       "associate’s shares meaningfully below his own haircut.", {})])

H2('C.4  Cross-examination — each challenge, conceded or rejected')
P('Each expert puts one challenge to each of the others, and the answer is recorded as CONCEDED or REJECTED rather than '
  'left as an exchange of views.', size=9.8)
rows = [
 ['Challenge', 'From → to', 'The answer'],
 ['“Capitalising a return you admit is flattered by the associate double-counts an asset I have already marked at full value.”',
  'Expert 1 → Expert 2',
  'CONCEDED IN PART. Expert 2 accepts the return is flattered and that his read is therefore too HIGH rather than too '
  'low. He rejects the conclusion: correcting for it widens his discount to book, it does not close it.'],
 ['“A single-digit wrapper discount does not begin to capture the illiquidity of a minority stake in a company that has '
  'never had a public exit.”',
  'Expert 3 → Expert 1',
  'REJECTED, with a reason. Expert 1 argues the wrapper discount and the mark haircut are two different things and that '
  'he prices the second separately — his own sensitivity takes the mark to half the round. What he will not do is '
  'apply both at once and call it prudence.'],
 ['“Marking the lender at book ignores that its own disclosed return does not justify book.”',
  'Expert 2 → Expert 1',
  'CONCEDED. Expert 1 accepts that the study’s residual-income mark on GB Capital is the better construction and that '
  f'his own number is EGP {(CAP["operating_equity"]-sotp["cap_val"])*(1-_e1["wrapper_discount"])/SH:.2f} a share higher '
  'for that reason alone. He keeps his mark on the ground that a realisable-value method marks assets at what they '
  'would fetch, not at what a return identity supports.'],
 ['“Mid-cycle or residual income, you are still valuing a company whose largest asset produces no cash flow you can '
  'model — so your precision is misplaced.”',
  'Expert 1 → Expert 2',
  'REJECTED. Expert 2’s answer is that this is his point rather than an objection to it: he prices only what the '
  'accounts support and lets the gap to the traded price be the associate, which makes the disagreement measurable.'],
 ['“A return on capital employed struck on a capital base inflated by a one-off inventory and receivable build '
  'understates the business.”',
  'Expert 2 → Expert 3',
  'CONCEDED, and it is already his stated caveat. His bull lever is exactly that recovery and he prices it at EGP '
  f'{_e3["roce_lever"]:.2f} a share — which he notes is less than half his mark lever, so conceding it does not change '
  'his ranking of the two.'],
 ['“You accept the cash-flow value for the auto leg and then mark the same leg at a multiple of capital employed. Pick '
  'one.”',
  'Expert 1 → Expert 3',
  'REJECTED. Expert 3 says the two are different questions — what the leg is worth on its forecast cash flows and what '
  'its capital has historically earned — and that publishing both is the point of a panel. He notes his mark is the '
  f'lower of the two by EGP {(sotp["auto_eq"]-E["e3"]["equity_at_base"])/1000:.1f} bn.'],
]
table(rows, [2.6, 1.15, 3.35], size=8.6)

H2('C.5  The three in one room')
P('The stake question that dominated an earlier draft of this study is settled — the company stated its holding in '
  'writing. What the three disagree on is what that holding is worth, and this edition has added a second disagreement '
  'they had not had before: what the lender is worth.', size=9.8)
P('Expert 1: “The company told us what it owns. Fine — now the argument is honest: it is about the '
  'discount, not the number. I apply a single-digit wrapper discount to a clean sum of realisable marks. If you think '
  'that is too thin for an illiquid minority stake, argue the discount, not the disclosure.”', size=9.8)
P(f'Expert 3: “Your own arithmetic says a stated {pc(STAKE,2)} stake is worth '
  f'{pc(MARK_HI/D["mktcap"],0)} of the entire market capitalisation at the round price. That was true when the number '
  'was uncertain and it is just as true now that it is not. The company being straight about its ownership does not make '
  'the market’s scepticism about the mark go away — if anything it sharpens the question, and I take a haircut to it '
  'for exactly that reason.”', size=9.8)
P(f'Expert 2: “You are both arguing about an asset. I am arguing about a business. On its own reported accounts this '
  f'group earns {pc(_e2["roe"],2)} against a cost of equity of {pc(CAP["ke_terminal"],2)} — it destroys value on the '
  f'capital it already has, which is why my number is EGP {_e2["base"]:.2f} against a book value of EGP '
  f'{_e2["book_ps"]:.2f}. And my return is FLATTERED by the very associate you two are pricing. Take that out and it is '
  'worse. If the associate is worth what either of you says, the shares are cheap; if it is worth what the accounts can '
  'demonstrate, they are not cheap at all. That is the whole case, and neither of you has narrowed it.”', size=9.8)
P('Where they end up. All three accept the ownership percentage, the volumes, the working-capital path and the cost of '
  'capital, and none of them adopts the study’s own residual-income mark on the lender: Expert 1 concedes it is the '
  'better construction and keeps his book mark anyway, and Expert 3 marks the same book at a haircut. That second '
  'disagreement is worth a few pounds a share. What remains, and what the study publishes as two branches rather than '
  'resolving, is a basis question about one line that no amount of modelling can settle from outside — and, as Expert 2 '
  'keeps pointing out, one that the reviewers of GB Corp’s own statements could not settle from inside either.',
  size=9.8)

H2('C.6  Reading the divergence')
figure('figD1_experts.png', 6.0, 'Figure C-1 — the three experts’ fair-value ranges. Brass ticks are base cases; the '
       'gold band is the panel centre; the ink line is the price. The spread is almost entirely the associate mark and '
       'the lender basis.')
_epanel = [_e1['base'], _e2['base'], _e3['base']]
rows = [
 ['Expert', 'Method', 'The single swing assumption', 'What it does to the associate', 'Base fair value'],
 ['Expert 1', 'Split-legs net asset value', f"The wrapper discount, at {pc(_e1['wrapper_discount'],0)}", 'Takes the round price at face value', f"EGP {_e1['base']:.2f}"],
 ['Expert 2', 'Residual income on the whole group', 'The return on reported equity', 'Prices it at nothing — it is the gap', f"EGP {_e2['base']:.2f}"],
 ['Expert 3', 'Cash returns against the cost of capital', f"A {E['e3']['params']['assoc_mult']:.2f}× haircut on the mark", 'Takes the round price and cuts it', f"EGP {_e3['base']:.2f}"],
]
table(rows, [0.85, 1.9, 1.65, 1.6, 1.1], first_col_bold=True, size=8.7)
P(f"The spread — EGP {min(_epanel):.2f} to {max(_epanel):.2f} at base — is wide for what is otherwise a set of "
  "broadly agreeing methods, and it is one disagreement with a second one riding on it. It is not the volumes, not the "
  "cash-conversion path, not the cost of capital and not the ownership percentage, which all three accept. It is how "
  "much of the associate mark to believe, and after that how the lender should be carried. Expert 2 sidesteps the first "
  "by pricing the associate at nothing and letting the gap to the market be the answer; Experts 1 and 3 both use the "
  "stated stake at the round price and disagree on the haircut. Unlike a business uncertainty that resolves with "
  "quarterly prints, this one may never fully resolve without a transaction, because private-mark discounts are a matter "
  "of judgment rather than a fact that appears on a schedule. Until a real secondary transaction supplies an independent "
  "data point, Expert 2’s number is the one estimate in the room that does not depend on the argument at all — which "
  "is exactly why it is also the lowest.")
caption(f'Each expert’s fair value is logged against this study’s date ({EDITION_L}) and the price it was '
        f'struck at (EGP {spot:.2f}, {SPOT_DATE}) as an internal per-expert track record.')

# ================= About / Disclaimer / footer ================================
H1('About this series')
P('Testahil publishes independent, educational valuation studies. Each is an attempt to reason transparently about what a '
  'security is worth, with every assumption shown and a companion model so readers can disagree productively. The house '
  'style is distributions, not tips: we describe ranges and probabilities, not targets, and we do not tell anyone what to '
  'do. Where a question cannot be settled from the evidence, as one cannot here, we publish the disagreement rather than '
  'an average of it. Studies are framed as educational analysis, the preparer is not licensed by any securities '
  'regulator, and holdings are disclosed.')
H1('Disclosure & Disclaimer')
for head, body in [
 ('Not investment advice. ', 'This document is educational and informational only. It is not, and must not be relied upon '
  'as, investment, financial, legal, accounting or tax advice, nor an offer, solicitation or recommendation to buy, sell or '
  'hold any security. It contains no price target and no rating.'),
 ('No licence; no advisory relationship. ', 'The preparer is not registered or licensed with any securities or financial '
  'regulator in any jurisdiction — including Egypt’s Financial Regulatory Authority — holds no brokerage or '
  'investment-advisory authorisation, and is not acting as your adviser or fiduciary. Nothing here is personalised to your '
  'circumstances.'),
 ('Two answers, not one. ', 'This study publishes two fair-value figures because GB Corp publishes two different values '
  'for its largest single asset and the filings do not decide between them. They are not a range, not a confidence '
  'interval and not an invitation to take the midpoint: they are two answers to one question under two of the company’s '
  'own disclosures.'),
 ('A qualified review conclusion, disclosed. ', 'The limited review of GB Corp’s consolidated statements to 30 June 2026 '
  'reaches a qualified conclusion at the associate line this study is built around: the reviewers state they were not '
  'provided with that associate’s own financial statements and could not verify the group’s share of its profits for the '
  'period. The same qualification stood on the 31 December 2025 audited statements. This is disclosed because it bears '
  'directly on both of the figures above.'),
 ('Holdings disclosure. ', 'The preparer may hold, and may in the future take or dispose of, a position in the security '
  'discussed in this report, and may transact at any time without notice. This is a potential conflict of interest you '
  'should weigh.'),
 ('Sources and accuracy. ', 'Reported financial and operating figures are drawn from the company’s public disclosure '
  'and other public sources believed reliable but not independently verified; they may contain errors or be superseded. '
  'Forward-looking inputs — the basis chosen for the associate mark, the mark on the lending arm, projections, '
  'multiples, the cash-flow model and the simulation’s factor probabilities — are the preparer’s own judgments and are '
  'inherently uncertain.'),
 ('Forward-looking statements. ', 'Any statements about the future are estimates subject to risks and uncertainties; actual '
  'results may differ materially. The simulation models price, not value, and encodes subjective probabilities for events '
  'that have not occurred.'),
 ('No reliance; your responsibility. ', 'Do your own research and consult a licensed professional before making any '
  'decision. You are solely responsible for your investment decisions and their outcomes. To the maximum extent permitted '
  'by law, the preparer accepts no liability for any loss arising from use of this document.'),
 ('Currency and figures. ', 'Figures are in Egyptian pounds, millions unless stated; bn denotes billion. The exchange rate '
  f'used for the round-price mark is EGP {sotp["egp_usd"]:.1f} to the US dollar, and it is a flagged estimate. Rounding may '
  f'cause totals to differ slightly. The price is EGP {spot:.2f} as at {SPOT_DATE}; the price cone and the technical read '
  f'are computed on the exchange library’s own last session, EGP {TA_CLOSE:.2f} on {TA_DATE_L}. Market data change '
  'continuously.'),
]:
    rich([(head, dict(bold=True, italic=True)), (body, {})], size=9.6, space_after=5)
P(f'TESTAHIL · Independent Valuation Study · Educational Analysis · GB Corp S.A.E. (EGX: GBCO) · edition '
  f'{EDITION_STAMP} · reporting currency EGP', size=8.8, color=GREY, align='center', space_before=10)
